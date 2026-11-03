# Subagent: T-017/T-018 recheck (haiku) (T-017/T-018 recheck (haiku))

Source: `agent-a35821d035b1bbe8f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:33:05.986Z

Working directory: /Users/arsis/zlayt-pm-project. Re-run your own check: `.venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py . > artifacts/review-evidence/T-018-r3-applied-check.out.txt; grep -c NOT-APPLIED artifacts/review-evidence/T-018-r3-applied-check.out.txt` and list remaining NOT-APPLIED lines. Pass if no major/blocker remains (minors/nits allowed as findings). Write reviews/T-018-product-manager-r2.md (card T-018) and reviews/T-017-product-manager-r3.md (card T-017), D.2 JSON, model = what you run as. Reply ≤ 3 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:07.737Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/product-manager.md"
}
````

### User / tool · 2026-11-02T01:33:07.745Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:08.230Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/ /Users/arsis/zlayt-pm-project/reviews/ /Users/arsis/zlayt-pm-project/artifacts/review-evidence/ 2>&1",
 "description": "List memory, reviews, and evidence directories"
}
````

### User / tool · 2026-11-02T01:33:08.313Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/:
total 72
drwxr-xr-x@ 11 arsis  staff   352 Nov  1 19:31 .
drwxr-xr-x@ 12 arsis  staff   384 Nov  1 19:03 ..
-rw-r--r--@  1 arsis  staff  1328 Nov  1 19:31 MEMORY.md
-rw-r--r--@  1 arsis  staff  1844 Nov  1 18:42 feedback_calibration_vs_redflags.md
-rw-r--r--@  1 arsis  staff  1945 Nov  1 19:02 feedback_needs_chris_drift.md
-rw-r--r--@  1 arsis  staff  3872 Nov  1 19:31 feedback_plan_review_patterns.md
-rw-r--r--@  1 arsis  staff  2779 Nov  1 19:02 feedback_spec_review_patterns.md
-rw-r--r--@  1 arsis  staff  3046 Nov  1 19:05 project_t013_review_history.md
-rw-r--r--@  1 arsis  staff  1821 Nov  1 19:31 project_t017_t018_review_history.md
-rw-r--r--@  1 arsis  staff  1010 Nov  1 19:31 reference_reviewer_sandbox.md
-rw-r--r--@  1 arsis  staff   575 Nov  1 18:33 reference_source_fetching.md

/Users/arsis/zlayt-pm-project/artifacts/review-evidence/:
total 10456
drwxr-xr-x@ 193 arsis  staff    6176 Nov  1 19:27 .
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
-rw-r--r--@   1 arsis  staff   25788 Nov  1 19:27 T-018-r2-applied-check.out.txt
-rw-r--r--@   1 arsis  staff   17390 Nov  1 19:27 T-018-r2-applied-check.py
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

/Users/arsis/zlayt-pm-project/reviews/:
total 2136
drwxr-xr-x@ 72 arsis  staff   2304 Nov  1 19:31 .
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
-rw-r--r--@  1 arsis  staff  11398 Nov  1 19:31 T-017-product-manager-r2.md
-rw-r--r--@  1 arsis  staff   6826 Nov  1 19:21 T-017-product-manager.md
-rw-r--r--@  1 arsis  staff  24227 Nov  1 19:30 T-018-product-manager.md
-rw-r--r--@  1 arsis  staff  11578 Nov  1 19:05 T-025-product-manager-r2.md
-rw-r--r--@  1 arsis  staff  11996 Nov  1 19:02 T-025-product-manager.md
-rw-r--r--@  1 arsis  staff   3544 Nov  1 19:04 T-026-ux-designer.md
-rw-r--r--@  1 arsis  staff  23638 Nov  1 19:14 T-028-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff  17323 Nov  1 19:09 T-028-staff-engineer.md
-rw-r--r--@  1 arsis  staff  11015 Nov  1 19:23 T-047-ux-designer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:10.362Z

**tool call — Bash**
````
{
 "command": "for f in .claude/agent-memory/product-manager-reviewer/*.md; do echo \"=== $f\"; cat \"$f\"; echo; done",
 "description": "Read all reviewer memory files"
}
````

### User / tool · 2026-11-02T01:33:10.462Z

**tool result**
````
=== .claude/agent-memory/product-manager-reviewer/MEMORY.md
- [Spec review patterns](feedback_spec_review_patterns.md) — recurring REQUIREMENTS defects: phantom IDs, fix-induced contradictions, vocab drift, stale golden counts, scope creep
- [Calibration vs red flags](feedback_calibration_vs_redflags.md) — dossier calibration severities softer than dealbreakers; cross-check
- [Source fetching](reference_source_fetching.md) — curl+UA fallback when WebFetch is missing; blocked hosts
- [NEEDS_CHRIS drift](feedback_needs_chris_drift.md) — rows added without cards, non-Chris questions, vague actions; ADR facts vs live system
- [Reviewer sandbox](reference_reviewer_sandbox.md) — hooks block shell writes to scratchpad/memory and backtick python -c; scripts go in artifacts/review-evidence
- [Plan/contract review patterns](feedback_plan_review_patterns.md) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bar; apply-check defects (appended-not-edited, either/or, stale text); probe scripts
- [T-013/T-025 review history](project_t013_review_history.md) — r1-r3 + T-025 verdicts; open: false §8 'aligned' claims, circular authority, must_not M1–M14 vs M17
- [T-017/T-018 review history](project_t017_t018_review_history.md) — round-1 and round-2 apply-check verdicts (changes); open: gate decision, pass-condition column, 11 unowned tests

=== .claude/agent-memory/product-manager-reviewer/feedback_calibration_vs_redflags.md
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

=== .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
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

=== .claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md
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

## Apply-check defects (T-018 round 2, 2026-11-01)
When the orchestrator "applies" review findings, check the result, not the claim. Round 2 showed the same failure modes:
7. **Appended, not edited.** The fix was added as a new AC (e.g. T-039 AC9) and the wrong AC (T-039 AC1, AC2) was left in place, so the card contradicts itself. Rule used: an appended AC counts only if no in-place text on the same card contradicts it.
8. **'Either ... or' left in the AC.** "Either T-033 gains AC6 ... or an ADR edits row 10" is a decision the card never made. Count it as not applied until one branch is chosen and recorded in ORCHESTRATOR_DECISIONS.
9. **Estimates and timeboxes skipped.** "Per-card estimate in each Description" landed on 2 of 20 cards. Count the cards, not the doc sentence.
10. **Old text kept beside the new.** The coverage doc got a new critical-path section, but the old 5-card chain and '4 h, over budget' lines stayed 15 lines lower. grep for the stale phrase.
11. **Instruction copied to several cards.** 11 distinct 'Contract review (T-018):' ACs sit on 2-3 cards each, so nobody owns the outcome.
12. **Claim on the board that the check refutes.** T-018 AC2 said "every blocker/major applied"; 9 of 19 were not.
13. **Owner probe must skip instruction text.** An AC that says "name test_api.py ... by file" is not an owner. Exclude 'Contract review (T-018):' lines from the qa-owner probe, or the count reads 0 when it is 11.
14. **Patterns match in the wrong file.** A 'self-check|diff .* golden' pattern matched an unrelated lexicon decision (D-018). Anchor patterns to the file and section that must hold the text, then read each matched line.

**Script:** artifacts/review-evidence/T-018-r2-applied-check.py (68 checks, prints the matched line for each; output in T-018-r2-applied-check.out.txt). Re-run on every apply round before any 'applied' verdict. Related: [[needs-chris-drift]].

=== .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
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

=== .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
---
name: t013-review-history
description: T-013 REQUIREMENTS review rounds — verdicts, what stayed open after round 3 (as of 2026-11-01)
metadata:
  type: project
---

T-013 (spec/REQUIREMENTS.md) review history:
- **Round 1 (65894f6):** PM changes (5 majors); paralegal fail (flags exported into letter).
- **Round 2 (64f766e):** PM changes (5 majors).
- **Round 3 (b4f3924):** PM changes (2 majors, 4 minors, 1 nit). 4 of the 5 r2 majors are resolved.

Open after round 3. All of it is reconciliation; the content is sound.
1. Ship bar row 4 and R-TL-4 say "19 of 20" seeded hallucinations, but the golden has 34. The fix is to state the threshold as a rate.
2. §8 claims ADR-017 reconciled everything. These still disagree:
   - The api.md export example has dot leaders, different total wording and a different Source line.
   - The notes citation format differs across A-106, R-EX-4 and api.md.
   - confirm_date returns 422 `date_invalid` in api.md and `invalid_edit` in REQ.
   - REQ predates D-018's lexicon `hedge` booleans.
   - The source_kind spelling is `patient_report` in REQ/api and `patient_self_report` in golden.
   - K4/K5 are must in golden and should in REQ.
   - must_not goes to M14 in golden; REQ says M13.

Seeds used for R-ID samples: 13, 1302, 2026. The probe script is at artifacts/review-evidence/T-013-r3check.py.

**T-025 (split from T-013, commit 2e92535, reviewed 2026-11-01): changes, 3 majors.**
- The §8 "Checked and aligned" claims were false. The confirm_date code flipped sides: api.md now says invalid_edit and REQ says date_invalid. A-106 says "not record numbers", but R-EX-4 cites "record N (...)". DECISIONS.md:204 fixes the "single agreed AI line". The api.md confirm_date example adds a gap for a phone note.
- The notes block hand-off is circular: REQ says the golden is the authority, and T-015 r3 says REQ is the file that lags.
- must_not is still the fixed range M1–M14, and the golden is now at M1–M17.
- Probe: artifacts/review-evidence/T-025-pm-probe.py.

**Why:** Artifacts (golden, api.md, ASSUMPTIONS) landed minutes after the REQ commit. Every round's residual has been cross-artifact drift, not REQ content.

**How to apply:** In any round 4 or T-018 contract review, re-run the probe and diff REQ against the current golden and api.md commits. Check the commit timestamps against the REQ commit. Related: [[spec-review-patterns]].

T-025 r2 (changes, 4 majors): writer fixed the authority rule, date_invalid and ship bar 4, but only half-applied "fix every instance". R-FL-4 still said M1-M14 after R-CO-3 was fixed; REQ A-106 row still said "not record numbers" after ASSUMPTIONS.md changed; §8 row 5 owned by a done card; §6 block 2 != golden because qa rewrote the golden after the REQ commit. Probe: artifacts/review-evidence/T-025-pm-r2-probe.py.
**How to apply:** after any "fixed" handoff, grep every occurrence of the old pattern (M1–M14, "today N", "not record numbers"), not just the one the finding cited. Check each §8 owner card's status with board.py show.

=== .claude/agent-memory/product-manager-reviewer/project_t017_t018_review_history.md
---
name: t017-t018-review-history
description: T-017 plan / T-018 contract review rounds (2026-11-01 to 11-02) — round-1 verdicts all 'changes', round-2 apply-check verdicts 'changes' with 9 contract majors and 4 T-017 majors still open
metadata:
  type: project
---

State as of the round-2 apply-check (this review), not a live status. Re-check the board before acting on it.

- Round 1: CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md, all 'changes' (6 + 4 + 9 majors). reviews/T-017-product-manager.md 'changes' (4 majors). Source of the fix texts.
- Round 2 (this review): reviews/T-018-product-manager.md 'changes': 10 majors (9 of 19 contract majors not applied, plus N1, T-018 AC2 ticked on a refuted claim). reviews/T-017-product-manager-r2.md 'changes': 4 majors not applied.
- Still open: pass-condition column in docs/M2M3_COVERAGE.md; the lexicon-recall release gate (LLM_VS_CODE rows 12/16 vs T-038 AC9 'or'); row-10 engine decision; 11 unowned test files (applied-check qa:NONE=11); T-039 AC1/AC2 and T-033 AC1 contradictions left in place; stale 5-card chain at coverage lines 18-19.
- Applied and verified: T-048 qa card; deps T-031/T-042/T-043; T-034 max_retries=0 and FixtureMissing; judge error paths; boundary module list; paralegal edit-reload, two-date conflict and record-4 ACs; verify_quickly in the paralegal agent body.

**Why:** The orchestrator's round-2 claim ('every blocker/major applied') closed T-018 AC2. Without this record, a future reviewer would assume the M2 contract is settled.

**How to apply:** On any future apply round, re-run artifacts/review-evidence/T-018-r2-applied-check.py and compare against the open list above. Check the lexicon gate decision first: cut (3) of the M2 cut order depends on it. See [[plan-review-patterns]] for the apply-check defects.

=== .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
---
name: reviewer-sandbox
description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
metadata:
  type: reference
---

The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]].

=== .claude/agent-memory/product-manager-reviewer/reference_source_fetching.md
---
name: source-fetching
description: How to spot-check cited URLs when WebFetch isn't available to this reviewer; known blocked hosts
metadata:
  type: reference
---

WebFetch was not in this reviewer's toolset on 2026-11-02, even though the briefs ask for it. Use `curl -sL -A "<Safari UA>"` into a scratchpad dir, strip the HTML with a local `python3 -I` script, grep for the claimed text, and record the substitution in the evidence file. hhs.gov returns 403 to curl; https://web.archive.org/web/2025/<url> works. ABA PDFs are known to block fetches (researcher notes).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:11.045Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py . > artifacts/review-evidence/T-018-r3-applied-check.out.txt; echo \"exit=$?\"; grep -c NOT-APPLIED artifacts/review-evidence/T-018-r3-applied-check.out.txt; grep -n NOT-APPLIED artifacts/review-evidence/T-018-r3-applied-check.out.txt",
 "description": "Re-run T-018 applied check and count NOT-APPLIED lines"
}
````

### User / tool · 2026-11-02T01:33:11.179Z

**tool result**
````
exit=0
30
164:[NOT-APPLIED] m-PM1a T-046 AC5 cut clock from activity log (PM minor 1) want=present pattern='activity\\.jsonl|timestamp'
166:[NOT-APPLIED] m-PM1b T-037 AC1 names the five flag groups with counts (PM minor 1) want=present pattern='gap, conflict, pre_existing'
168:[NOT-APPLIED] m-PM1c T-040 AC5 test_no_token_in_logs (PM minor 1) want=present pattern='test_no_token_in_logs'
170:[NOT-APPLIED] m-PM2 golden variant E in SCOPE_CUTS or a card (PM minor 2) want=present pattern='variant E|forged'
174:[NOT-APPLIED] m-PL1 T-042 why-template sentence inline on needs_review rows (PL minor 1) want=present pattern='why.template|sentence inline'
176:[NOT-APPLIED] m-PL2 T-043 AC2 full R-CH-3 rate string (PL minor 2) want=present pattern='12 planned; discharged at visit 9'
178:[NOT-APPLIED] m-PL3a T-043 $6,240 charge highlight to record 2 (PL minor 3) want=present pattern='ER charges: \\$6,240'
180:[NOT-APPLIED] m-PL3b T-043 injection banner names record 3 (PL minor 3) want=present pattern='banner names record 3|names record 3'
182:[NOT-APPLIED] m-PL4 T-043 dismissed-flag reason reaches notes (PL minor 4) want=present pattern='treating elsewhere|dismiss.*reason.*notes'
184:[NOT-APPLIED] m-S1 xfail(strict) red marks instead of --collect-only (staff minor 1) want=present pattern='xfail'
186:[NOT-APPLIED] m-S2a T-034 AC2 retry changes prompt hash (staff minor 2) AC2 text: audited.py: fails 3 attempts -> LLM_FAILED_AFTER_RETRIES and app stays usable; fails twice then succeeds -> output returned; one llm_calls r
187:[NOT-APPLIED] m-S2b T-035 judge input isolation (staff minor 2) want=present pattern='judge.*(candidate|isolation)'
189:[NOT-APPLIED] m-S3 T-030 mutation guard for verifier stub (staff minor 3) want=present pattern='monkeypatch|mutation'
191:[NOT-APPLIED] m-S4 T-029 global no-network guard (staff minor 4) want=present pattern='socket|no network|conftest'
193:[NOT-APPLIED] m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed (T-017 minor) want=absent pattern='rows 1-20 all mapped'
209:   NOT-APPLIED: m-PM1a T-046 AC5 cut clock from activity log | PM minor 1
210:   NOT-APPLIED: m-PM1b T-037 AC1 names the five flag groups with counts | PM minor 1
211:   NOT-APPLIED: m-PM1c T-040 AC5 test_no_token_in_logs | PM minor 1
212:   NOT-APPLIED: m-PM2 golden variant E in SCOPE_CUTS or a card | PM minor 2
213:   NOT-APPLIED: m-PL1 T-042 why-template sentence inline on needs_review rows | PL minor 1
214:   NOT-APPLIED: m-PL2 T-043 AC2 full R-CH-3 rate string | PL minor 2
215:   NOT-APPLIED: m-PL3a T-043 $6,240 charge highlight to record 2 | PL minor 3
216:   NOT-APPLIED: m-PL3b T-043 injection banner names record 3 | PL minor 3
217:   NOT-APPLIED: m-PL4 T-043 dismissed-flag reason reaches notes | PL minor 4
218:   NOT-APPLIED: m-S1 xfail(strict) red marks instead of --collect-only | staff minor 1
219:   NOT-APPLIED: m-S2a | staff minor 2
220:   NOT-APPLIED: m-S2b T-035 judge input isolation | staff minor 2
221:   NOT-APPLIED: m-S3 T-030 mutation guard for verifier stub | staff minor 3
222:   NOT-APPLIED: m-S4 T-029 global no-network guard | staff minor 4
223:   NOT-APPLIED: m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed | T-017 minor
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:12.704Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r3-applied-check.out.txt"
}
````

### User / tool · 2026-11-02T01:33:12.717Z

**tool result**
````
1	=== PROBE: qa owner of every test file cited in non-instruction AC text (cards T-027..T-046, T-048)
2	   test_amounts             cited_by=['T-029', 'T-033'] qa_owner=['T-029']
3	   test_api                 cited_by=['T-039', 'T-040', 'T-041'] qa_owner=['T-039']
4	   test_audited             cited_by=['T-034', 'T-048'] qa_owner=['T-048']
5	   test_boundaries          cited_by=['T-029', 'T-030', 'T-041'] qa_owner=['T-029']
6	   test_charges             cited_by=['T-039', 'T-043'] qa_owner=['T-039']
7	   test_confidence          cited_by=['T-029', 'T-030'] qa_owner=['T-029']
8	   test_conflicts           cited_by=['T-033', 'T-048'] qa_owner=['T-048']
9	   test_dates               cited_by=['T-029', 'T-032'] qa_owner=['T-029']
10	   test_db                  cited_by=['T-029', 'T-031'] qa_owner=['T-029']
11	   test_edit                cited_by=['T-039', 'T-044'] qa_owner=['T-039']
12	   test_eval_runner         cited_by=['T-038'] qa_owner=['T-038']
13	   test_eval_spec_check     cited_by=['T-038'] qa_owner=['T-038']
14	   test_export              cited_by=['T-039', 'T-041'] qa_owner=['T-039']
15	   test_export_ui           cited_by=['T-039', 'T-044'] qa_owner=['T-039']
16	   test_flag_templates      cited_by=['T-033', 'T-048'] qa_owner=['T-048']
17	   test_flags_injection     cited_by=['T-036', 'T-048'] qa_owner=['T-048']
18	   test_flags_panel         cited_by=['T-039', 'T-043'] qa_owner=['T-039']
19	   test_flags_sample        cited_by=['T-036', 'T-048'] qa_owner=['T-048']
20	   test_gaps                cited_by=['T-029', 'T-033'] qa_owner=['T-029']
21	   test_grounding           cited_by=['T-029', 'T-030'] qa_owner=['T-029']
22	   test_ingest              cited_by=['T-029', 'T-032'] qa_owner=['T-029']
23	   test_input               cited_by=['T-039', 'T-042'] qa_owner=['T-039']
24	   test_judges              cited_by=['T-035', 'T-048'] qa_owner=['T-048']
25	   test_keyboard_mobile     cited_by=['T-039', 'T-043'] qa_owner=['T-039']
26	   test_ladder_gate         cited_by=['T-039', 'T-045'] qa_owner=['T-039', 'T-045']
27	   test_letter_isolation    cited_by=['T-039', 'T-045'] qa_owner=['T-039', 'T-045']
28	   test_pipeline            cited_by=['T-037', 'T-048'] qa_owner=['T-048']
29	   test_provider            cited_by=['T-034', 'T-048'] qa_owner=['T-048']
30	   test_review_matrix       cited_by=['T-039', 'T-043'] qa_owner=['T-039']
31	   test_review_rules        cited_by=['T-039', 'T-040'] qa_owner=['T-039']
32	   test_schemas             cited_by=['T-035', 'T-036', 'T-048'] qa_owner=['T-048']
33	   test_sentences           cited_by=['T-029', 'T-030'] qa_owner=['T-029']
34	   test_side_by_side        cited_by=['T-039', 'T-046'] qa_owner=['T-039']
35	   test_source_record       cited_by=['T-039', 'T-042', 'T-043', 'T-046'] qa_owner=['T-039']
36	   test_timeline            cited_by=['T-039', 'T-042'] qa_owner=['T-039']
37	   qa:NONE count = 0 -> []
38	
39	=== PROBE: deps and longest chains
40	   longest chain to T-038: T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029
41	   longest chain to T-045: T-045 -> T-044 -> T-043 -> T-040 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029
42	   deps T-031: ['T-029']
43	   deps T-042: ['T-039']
44	   deps T-043: ['T-039', 'T-040', 'T-042']
45	   deps T-034: ['T-031', 'T-048']
46	   deps T-036: ['T-027', 'T-033', 'T-035', 'T-048']
47	   deps T-027: []
48	
49	=== PM CONTRACT (6 majors)
50	[APPLIED] PM-1a M2 cut order section present (PM major 1 fix) want=present pattern='M2 cut order'
51	     evidence: 5: - M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) T-046 si
52	[APPLIED] PM-1b stale 5-card critical path removed from coverage doc (PM major 1 fix) want=absent pattern='T-029 \\(m2-qa-unit-first\\) -> T-030'
53	     evidence: no matching line
54	[APPLIED] PM-1c stale 'about 4 h' sentence removed (PM major 1 fix) want=absent pattern='This runs about 4 h'
55	     evidence: no matching line
56	[APPLIED] PM-1d per-card estimate in each card Description (PM major 1 fix) cards missing estimate: 0 of 20
57	     evidence: cards without an estimate in Description: []
58	[APPLIED] PM-2a T-027 priority is P0 (PM major 2 fix) evidence: T-027 priority=P0
59	[APPLIED] PM-2b T-027 Description carries timebox (PM major 2 fix) want=present pattern='[Tt]imebox|\\b\\d+ ?(h|min)\\b'
60	     evidence: 3: Estimate: 40 min (timebox).
61	[APPLIED] PM-3a T-038 ship_bar_met false on fixture (PM major 3 fix) want=present pattern='ship_bar_met is false when backend == fixture'
62	     evidence: T-038 AC6: ...en LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line o...
63	[APPLIED] PM-3b T-037 fixtures for all 50 judge lines and SE1-SE5 (PM major 3 fix) want=present pattern='hallucinations\\.jsonl.*SE1-SE5|SE1-SE5'
64	     evidence: T-037 AC6: ... T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_ba...
65	     evidence: T-037 AC7: ...'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'....
66	[APPLIED] PM-3c T-045 AC4 no longer requires ship_bar_met true on default (fixture) backend (PM major 3 fix) want=absent pattern='`python -m evals\\.run` \\(ship_bar_met true\\)'
67	     evidence: no matching AC line
68	[APPLIED] PM-3d T-045 claude-cli run named (PM major 3 fix) want=present pattern='LLM_BACKEND=claude-cli python -m evals\\.run'
69	     evidence: T-045 AC4: ...ensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `LLM_BACKEND=claude-cli python -m evals.run` (ship_bar_met true on the live backend; the fixture run reports not_...
70	     evidence: T-045 AC6: ...ations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'....
71	[APPLIED] PM-4a T-038 check-fresh + prompt sha256 (PM major 4 fix) want=present pattern='--check-fresh.*exits 1|sha256 of every app/llm/prompts'
72	     evidence: T-038 AC7: ...Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` ex...
73	[APPLIED] PM-4b T-035/T-036 handoff links report with prompt hashes = HEAD (PM major 4 fix) want=present pattern='prompt hashes equal HEAD'
74	     evidence: T-035 AC6: .... T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'....
75	     evidence: T-036 AC8: .... T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'....
76	[APPLIED] PM-5a paralegal agent body carries scores.verify_quickly (PM major 5 fix) count=1
77	     evidence: **Ship-bar score (D-015):** whenever you review the running app, your review JSON must include `scores.verify_quickly` (1–5): "I could verify every claim quickl
78	[APPLIED] PM-5b an M3 card (or the M3 gate) requests scores.verify_quickly (PM major 5 fix: 'New orchestrator card (M3)') M3 cards with the key: ['T-045']
79	[APPLIED] PM-5c ship-bar row -> card table covers rows 1-5 (PM major 5 fix) want=present pattern='^\\| [1-5] '
80	     evidence: 11: | 1 Grounding | T-038 (grounding_rate), T-041 (export grounding) |
81	     evidence: 12: | 2 Recall | T-038 |
82	     evidence: 13: | 3 Flags (incl. 28/73) | T-038, T-033 |
83	     evidence: 14: | 4 No invented facts (live backend only) | T-038, T-037 |
84	[APPLIED] PM-6a T-038 lexicon_recall_must_flags metric (PM major 6 fix) want=present pattern='lexicon_recall_must_flags'
85	     evidence: T-038 AC9: ...latest.json reports lexicon_recall_must_flags (pre_existing + causation, per golden case and pooled; R-FL-3, R-RV-6...
86	[APPLIED] PM-6d T-038 lexicon gate decided (no open 'or edit LLM_VS_CODE rows 12/16' alternative) (PM major 6 fix) want=absent pattern='or edit LLM_VS_CODE rows 12/16'
87	     evidence: no matching AC line
88	[APPLIED] PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR) (PM major 6 fix) want=present pattern='reported, not gated'
89	     evidence: 44: | 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. E
90	[APPLIED] PM-6c LLM_VS_CODE row 16 still says 'release gate' (PM major 6 fix) want=absent pattern='recall on the golden set is a release gate'
91	     evidence: no matching line
92	
93	=== PL CONTRACT (4 majors)
94	[APPLIED] PL-1a T-044 AC edit survives reload + EDITED ITEMS (PL major 1 fix) want=present pattern='EDITED ITEMS with original and new text'
95	     evidence: T-044 AC6: ... summary and "edited" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entr...
96	[APPLIED] PL-1b T-039 test_edited_items_section (PL major 1 fix) want=present pattern='test_edited_items_section'
97	     evidence: T-039 AC6: ...ED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirma...
98	[APPLIED] PL-2a T-039 reconciliation: entry 6 pending + 7 of 9 (appended) (PL major 2 fix) want=present pattern='entry 5 and leaving entry 6 pending gives'
99	     evidence: T-039 AC2: ...followed by (provider, date), bills-to-request line exact, dismissing entry 5 and leaving entry 6 pending gives 'Record 5 ... dismissed', 'Record 6 ... not reviewed' and 7 of 9 (R-E...
100	     evidence: T-039 AC7: ...Contract review (T-018): T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives "Record 5 ... dismissed", "Record 6 ... not reviewed" and 7 of 9'....
101	[APPLIED] PL-2b T-039 AC2 original 'entry 5 gives ... 7 of 9' removed (PL major 2 fix) want=absent pattern='dismissing entry 5 gives'
102	     evidence: no matching AC line
103	[APPLIED] PL-3 T-043 accident-date two dates, 2026-01-19 quote (PL major 3 fix) want=present pattern='Date of accident per intake form: 2026-01-19'
104	     evidence: T-043 AC6: ...ew (T-018): T-043 AC1 append: 'the accident-date conflict card shows "Date of accident per intake form: 2026-01-19." and the 2026-01-09 header line(s) of records 1 and 2 side by side, ...
105	[APPLIED] PL-4a T-042 record 4 could not process in tray (PL major 4 fix) want=present pattern='\\"could not process\\" with the reason'
106	     evidence: T-042 AC6: ...e stub backend failing every call for record 4, the UI shows record 4 "could not process" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed ...
107	[APPLIED] PL-4b T-041 record 4 under RECORDS NOT IN THE TREATMENT SECTION (PL major 4 fix) want=present pattern='RECORDS NOT IN THE TREATMENT SECTION'
108	     evidence: T-041 AC6: ...e could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason "could not process"'....
109	
110	=== S CONTRACT (9 majors)
111	[APPLIED] S-1a T-048 qa card exists with 9 named LLM-stage files (staff major 1 fix) want=present pattern='test_provider\\.py.*test_flag_templates\\.py'
112	     evidence: T-048 AC1: ...tests/unit/test_provider.py, test_audited.py, test_schemas.py, test_judges.py, test_flags_sample.py, test_flags_injection.py, test_pipeline.py, test_conflicts.py, test_flag_templates.py exist and fail only on NotImplemented; `pytest tests/unit --collect-o...
113	[APPLIED] S-1b T-039 names test_api.py and E2E files by file (not instruction text) (staff major 1 fix) want=present pattern='test_api\\.py.*test_(input|timeline|edit|flags_panel)\\.py'
114	     evidence: T-039 AC4: ...tests/e2e files written red: test_api.py, test_input.py, test_timeline.py, test_source_record.py, test_flags_panel.py, test_charges.py, test_review_matrix.py, test_keyboard_mobile.py, test_edit.py, test_export_ui.py, test_letter_isolation.py, test_ladder_gate.py, te...
115	[APPLIED] S-1c qa:NONE count is 0 after T-048 (staff major 1 acceptance) count=0
116	[APPLIED] S-2a T-031 depends_on includes T-029 evidence: ['T-029']
117	[APPLIED] S-2b T-042 depends_on includes T-039 evidence: ['T-039']
118	[APPLIED] S-2c T-043 depends_on includes T-039, T-040 evidence: ['T-039', 'T-040', 'T-042']
119	[APPLIED] S-3 T-034 anthropic-api max_retries=0 (staff major 3 fix) want=present pattern='max_retries=0'
120	     evidence: T-034 AC7: ... (T-018): T-034 AC4 append: 'anthropic-api client is constructed with max_retries=0 and an explicit timeout (<= 120 s); test_provider::test_sdk_no_intern...
121	[APPLIED] S-4a T-034 fixture miss raises FixtureMissing (staff major 4 fix) want=present pattern='FixtureMissing'
122	     evidence: T-034 AC8: ...Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_...
123	[APPLIED] S-4b T-037 replay reports 0 FixtureMissing (staff major 4 fix) want=present pattern='0 FixtureMissing'
124	     evidence: T-037 AC7: ....09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'....
125	[APPLIED] S-5a T-035 judge #2 unsure/error/timeout -> needs_review (staff major 5 fix) want=present pattern='JUDGE_UNSURE'
126	     evidence: T-035 AC7: ...T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5...
127	[APPLIED] S-5b T-036 judge #3/#4 error -> needs_review (staff major 5 fix) want=present pattern='judge #3/#4 error or timeout'
128	     evidence: T-036 AC9: ...NAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'....
129	[APPLIED] S-6 T-029 boundary module list incl. conflicts, flag_templates, injection scan (staff major 6 fix) want=present pattern='flag_templates.*injection scan'
130	     evidence: T-029 AC7: ..., amounts (find + classify), totals, gaps, conflicts (accident date), flag_templates, injection scan, export; scan transitive imports, not just direct ones....
131	[APPLIED] S-7a T-033 or T-036 decides provider-conflict engine (not an 'Either ... or' instruction) (staff major 7 fix) want=absent pattern='^Contract review \\(T-018\\): Either'
132	     evidence: no matching AC line
133	[APPLIED] S-7b coverage doc row 10 engine matches LLM_VS_CODE row 10 (Code) (staff major 7 fix) want=absent pattern='^\\| 10 \\| Structural conflicts .*provider variants'
134	     evidence: no matching line
135	[APPLIED] S-7c ADR/decision recording the row-10 engine (ORCHESTRATOR_DECISIONS) (staff major 7 fix) want=present pattern='row 10|case_05'
136	     evidence: 33: | D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_
137	[APPLIED] S-8a T-033 rate note derived by code (staff major 8 fix) want=present pattern='rate note numbers are code-derived'
138	     evidence: T-033 AC7: ...Contract review (T-018): T-033 new AC: 'rate note numbers are code-derived: N planned from the "Plan of care: N visits" match in a record with t...
139	[APPLIED] S-8b T-033 AC1 no longer says '$2,150 only' (damages mention added in place) (staff major 8 fix) want=absent pattern='\\$2,150 only'
140	     evidence: no matching AC line
141	[APPLIED] S-9a T-039 AC1 case_07 total corrected in place ($8,390 removed) (staff major 9 fix) want=absent pattern='incl\\. case_07 with a rate present'
142	     evidence: no matching AC line
143	[APPLIED] S-9b T-039 case_07 $420 AC present (staff major 9 fix) want=present pattern='\\$420\\.00'
144	     evidence: T-039 AC1: ...accepted the line is exactly 'Billed charges stated in these records: $420.00'; same accepted set -> byte-identical output; fixture sample equals s...
145	     evidence: T-039 AC9: ... $420 accepted it is exactly "Billed charges stated in these records: $420.00"; with the $185 rate non-dismissed the sample line is unchanged'. T-0...
146	[APPLIED] S-9c T-033 money as int cents (staff major 9 fix) want=present pattern='int 624000'
147	     evidence: T-033 AC8: ... the sample line is unchanged'. T-033 AC1 append: '"$6,240" parses to int 624000; app/backend/amounts.py contains no float('....
148	
149	=== T-017 PLAN REVIEW (4 majors)
150	[APPLIED] T17-1a coverage doc has pass-condition column (T-017 major 1 fix) want=present pattern='[Pp]ass condition'
151	     evidence: 20: Pass conditions live in each card's AC on the board (each names its test/eval/command); this table maps ownership. Numbers in AC are checked against t
152	[APPLIED] T17-2a plan self-check: AC numbers diffed against golden (in coverage doc) (T-017 major 2 fix) want=present pattern='self-check|every number in an AC|diffed against'
153	     evidence: 19: ## Plan self-check
154	[APPLIED] T17-3 row-10 mapping in coverage doc (see S-7b) (T-017 major 3 fix) want=absent pattern='T-036 \\(m2-be-llm-flags\\) \\(provider variants\\)'
155	     evidence: no matching line
156	[APPLIED] T17-4a M2 cut order section (T-017 major 4 fix) want=present pattern='M2 cut order'
157	     evidence: 5: - M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) T-046 si
158	[APPLIED] T17-4b ship-bar row -> card table (T-017 major 4 fix) want=present pattern='Ship bar row . card'
159	     evidence: 8: ## Ship bar row → card
160	[APPLIED] T17-4c cut order does not cut lexicon recall target that LLM_VS_CODE calls a release gate (T-017 major 4 fix) want=absent pattern='lexicon held-out target lowered'
161	     evidence: no matching line
162	
163	=== MINORS (informational; severities kept as in source)
164	[NOT-APPLIED] m-PM1a T-046 AC5 cut clock from activity log (PM minor 1) want=present pattern='activity\\.jsonl|timestamp'
165	     evidence: no matching AC line
166	[NOT-APPLIED] m-PM1b T-037 AC1 names the five flag groups with counts (PM minor 1) want=present pattern='gap, conflict, pre_existing'
167	     evidence: no matching AC line
168	[NOT-APPLIED] m-PM1c T-040 AC5 test_no_token_in_logs (PM minor 1) want=present pattern='test_no_token_in_logs'
169	     evidence: no matching AC line
170	[NOT-APPLIED] m-PM2 golden variant E in SCOPE_CUTS or a card (PM minor 2) want=present pattern='variant E|forged'
171	     evidence: no matching line
172	[APPLIED] m-PM4 T-041 AC4 endpoint spelled {token} (PM nit) want=present pattern='\\{token\\}/export'
173	     evidence: T-041 AC4: ...GET /api/cases/{token}/export returns the two fields separately; pending/dismissed/rejected items n...
174	[NOT-APPLIED] m-PL1 T-042 why-template sentence inline on needs_review rows (PL minor 1) want=present pattern='why.template|sentence inline'
175	     evidence: no matching AC line
176	[NOT-APPLIED] m-PL2 T-043 AC2 full R-CH-3 rate string (PL minor 2) want=present pattern='12 planned; discharged at visit 9'
177	     evidence: no matching AC line
178	[NOT-APPLIED] m-PL3a T-043 $6,240 charge highlight to record 2 (PL minor 3) want=present pattern='ER charges: \\$6,240'
179	     evidence: no matching AC line
180	[NOT-APPLIED] m-PL3b T-043 injection banner names record 3 (PL minor 3) want=present pattern='banner names record 3|names record 3'
181	     evidence: no matching AC line
182	[NOT-APPLIED] m-PL4 T-043 dismissed-flag reason reaches notes (PL minor 4) want=present pattern='treating elsewhere|dismiss.*reason.*notes'
183	     evidence: no matching AC line
184	[NOT-APPLIED] m-S1 xfail(strict) red marks instead of --collect-only (staff minor 1) want=present pattern='xfail'
185	     evidence: no matching AC line
186	[NOT-APPLIED] m-S2a T-034 AC2 retry changes prompt hash (staff minor 2) AC2 text: audited.py: fails 3 attempts -> LLM_FAILED_AFTER_RETRIES and app stays usable; fails twice then succeeds -> output returned; one llm_calls r
187	[NOT-APPLIED] m-S2b T-035 judge input isolation (staff minor 2) want=present pattern='judge.*(candidate|isolation)'
188	     evidence: no matching AC line
189	[NOT-APPLIED] m-S3 T-030 mutation guard for verifier stub (staff minor 3) want=present pattern='monkeypatch|mutation'
190	     evidence: no matching AC line
191	[NOT-APPLIED] m-S4 T-029 global no-network guard (staff minor 4) want=present pattern='socket|no network|conftest'
192	     evidence: no matching AC line
193	[NOT-APPLIED] m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed (T-017 minor) want=absent pattern='rows 1-20 all mapped'
194	     evidence: 21:   - {"n": 2, "text": "every row of the docs/LLM_VS_CODE.md table maps to an M2 card with its validation named in AC", "done": true, "evidence": "docs/
195	[INFO] instruction-style 'Contract review (T-018):' ACs copied onto more than one card: 10 distinct texts
196	     ['T-031', 'T-034', 'T-036']: Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card...
197	     ['T-029', 'T-039']: Contract review (T-018): T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], b...
198	     ['T-031', 'T-042', 'T-043']: Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depen...
199	     ['T-034', 'T-037']: Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged w...
200	     ['T-035', 'T-036']: Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_rev...
201	     ['T-037', 'T-038', 'T-045']: Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are compu...
202	     ['T-035', 'T-036', 'T-038']: Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompt...
203	     ['T-033', 'T-039']: Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $...
204	     ['T-041', 'T-042']: Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for r...
205	     ['T-039', 'T-044']: Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and "edited" label pe...
206	
207	=== SUMMARY
208	checks: 68 applied=53 not-applied=15
209	   NOT-APPLIED: m-PM1a T-046 AC5 cut clock from activity log | PM minor 1
210	   NOT-APPLIED: m-PM1b T-037 AC1 names the five flag groups with counts | PM minor 1
211	   NOT-APPLIED: m-PM1c T-040 AC5 test_no_token_in_logs | PM minor 1
212	   NOT-APPLIED: m-PM2 golden variant E in SCOPE_CUTS or a card | PM minor 2
213	   NOT-APPLIED: m-PL1 T-042 why-template sentence inline on needs_review rows | PL minor 1
214	   NOT-APPLIED: m-PL2 T-043 AC2 full R-CH-3 rate string | PL minor 2
215	   NOT-APPLIED: m-PL3a T-043 $6,240 charge highlight to record 2 | PL minor 3
216	   NOT-APPLIED: m-PL3b T-043 injection banner names record 3 | PL minor 3
217	   NOT-APPLIED: m-PL4 T-043 dismissed-flag reason reaches notes | PL minor 4
218	   NOT-APPLIED: m-S1 xfail(strict) red marks instead of --collect-only | staff minor 1
219	   NOT-APPLIED: m-S2a | staff minor 2
220	   NOT-APPLIED: m-S2b T-035 judge input isolation | staff minor 2
221	   NOT-APPLIED: m-S3 T-030 mutation guard for verifier stub | staff minor 3
222	   NOT-APPLIED: m-S4 T-029 global no-network guard | staff minor 4
223	   NOT-APPLIED: m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed | T-017 minor
224	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:19.438Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-018-product-manager.md",
 "description": "Read prior T-018 product-manager review"
}
````

### User / tool · 2026-11-02T01:33:19.518Z

**tool result**
````
# T-018 apply-check: contract-review findings (product-manager-reviewer, round 2)

**Verdict: changes.** 0 blockers. 10 majors: 9 of the 19 contract majors are not applied (or applied in a form that still contradicts the card), plus one new major (T-018 AC2 is ticked on evidence this check refutes). 4 minor groups remain unapplied and are not gating (scope is blocker/major per the brief; severities kept as in source).

Mechanical check: `artifacts/review-evidence/T-018-r2-applied-check.py`, run as `python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project`, output in `artifacts/review-evidence/T-018-r2-applied-check.out.txt`. 68 checks: 31 pass, 37 fail. The failures include the minors and the T-017 items.

Rule used: an appended `Contract review (T-018): ...` AC counts as the requested edit only if a worker can test it and no in-place text on the same card contradicts it. An AC that still says "Either ... or" or "add ... or edit" leaves the decision open, so it counts as not applied.

| Finding (source) | Status | Evidence (verbatim, from `board.py show` or the file) |
|---|---|---|
| PM1 critical path, estimates, cut order | NOT APPLIED | `docs/M2M3_COVERAGE.md:18` "Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 ..." and `:19` "This runs about 4 h, over the 3.5 h budget." remain beside the new text at `:4`. Estimate on 2 of 20 cards (check PM-1d). |
| PM2 T-027 P0 plus timebox | NOT APPLIED | `priority: "P0"` applied; Description has no timebox (PM-2b). |
| PM3 fixture cannot ship | NOT APPLIED | T-038 AC6 "ship_bar_met is false when backend == fixture" applied; T-045 AC4 still "`python -m evals.run` (ship_bar_met true)" (PM-3c). |
| PM4 regression freshness | APPLIED | T-038 AC7 "latest.json records sha256 of every app/llm/prompts/*.md ... `--check-fresh` exits 1"; T-035 AC6 and T-036 AC8 handoff text. |
| PM5 verify_quickly owner | NOT APPLIED | `.claude/agents/paralegal-reviewer.md:111` "`scores.verify_quickly` (1–5)" applied; no M3 card names the key (PM-5b, M3 list empty). |
| PM6 lexicon recall gate | NOT APPLIED | T-038 AC9 "...or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'" (open "or"); `docs/LLM_VS_CODE.md:44` "...whose recall on the golden set is a release gate" (PM-6c). |
| PL1 edits survive reload | APPLIED | T-044 AC6 "...export notes list record 3 under EDITED ITEMS with original and new text"; T-039 AC6 test_edited_items_section. |
| PL2 reconciliation "7 of 9" | NOT APPLIED | T-039 AC2 still "dismissing entry 5 gives 'Record 5 ... dismissed' and 7 of 9" (PL-2b); corrected wording only in AC7. |
| PL3 accident date as two dates | APPLIED | T-043 AC6 "Date of accident per intake form: 2026-01-19." |
| PL4 record 4 visible as failed | APPLIED | T-042 AC6 "'could not process' with the reason in the could-not-verify tray"; T-041 AC6 "RECORDS NOT IN THE TREATMENT SECTION with reason". |
| S1 qa author for 20 test files | NOT APPLIED | T-048 exists (applied, AC1 names 9 files). 11 files still have no qa owner (probe: "qa:NONE count = 11"). T-039 names none of them (S-1b). |
| S2 missing depends_on | APPLIED | T-031 `['T-029']`; T-042 `['T-039']`; T-043 `['T-039', 'T-040', 'T-042']`. |
| S3 SDK hidden retries | APPLIED | T-034 AC7 "max_retries=0 and an explicit timeout (<= 120 s)". |
| S4 fixture-miss behaviour | APPLIED | T-034 AC8 "a fixture miss raises FixtureMissing"; T-037 AC7 "reports 0 FixtureMissing". The weaker original T-037 AC2 remains and does not contradict. |
| S5 judges #2-4 error path | APPLIED | T-035 AC7 "JUDGE_UNSURE / JUDGE_UNAVAILABLE"; T-036 AC9 "judge #3/#4 error or timeout -> needs_review". |
| S6 boundary-test module list | APPLIED | T-029 AC7 "conflicts (accident date), flag_templates, injection scan". |
| S7 row-10 engine | NOT APPLIED | T-033 AC6 "Either T-033 gains AC6 ... or an ADR edits row 10"; `docs/M2M3_COVERAGE.md:96` "T-036 (m2-be-llm-flags) (provider variants)"; no decision in memory/ORCHESTRATOR_DECISIONS.md (S-7a, S-7b, S-7c). |
| S8 rate note derived by code, damages mention | APPLIED | T-033 AC7 "rate note numbers are code-derived ... one damages mention (record 5, value null)". The "only" left in T-033 AC1 is in the minors below. |
| S9 case_07 total | NOT APPLIED | T-039 AC1 still "'Billed charges stated in these records: $8,390.00' incl. case_07 with a rate present" (S-9a); $420 is only in AC9. |

## New finding
- **N1 (major).** T-018 AC2 is ticked as "every blocker/major applied ... verified by reviews/T-018-product-manager.md". This review refutes it (see F1-F9 below). The T-018 handoff's "~23 majors applied" is also wrong: 10 of 19 contract majors are applied.

## Things that landed and should not break
- T-048 exists and gates T-034..T-037; the test-first wiring for LLM stages is real.
- Fixture-cannot-ship is written into T-038 AC6 and T-037 AC7 (every hallucinations line and SE1-SE5 are named).
- The paralegal edit-reload, two-date accident conflict and record-4 visibility ACs are on the board (PL1, PL3, PL4).

```json
{"card": "T-018", "persona": "product-manager-reviewer", "model": "claude-haiku-5-5",
 "scope": "Apply-check of the T-018 contract-review findings: reviews/CONTRACT-M2M3-product-manager.md (6 majors, 3 minors, 1 nit), CONTRACT-M2M3-paralegal.md (4 majors, 4 minors), CONTRACT-M2M3-staff-engineer.md (9 majors, 4 minors), against the board working tree (board/cards T-017, T-018, T-027, T-029..T-046, T-048), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, .claude/agents/paralegal-reviewer.md, memory/ORCHESTRATOR_DECISIONS.md, memory/SCOPE_CUTS.md, memory/DECISIONS.md, evals/golden/README.md, memory/contracts/api.md. No app code exists; no sample-case run (contract review).",
 "exercised": [
  "read personas/product-manager.md in full; memory index and memory files plan_review_patterns, spec_review_patterns, reviewer_sandbox, needs_chris_drift, calibration_vs_redflags",
  "read reviews/CONTRACT-M2M3-product-manager.md, CONTRACT-M2M3-paralegal.md, CONTRACT-M2M3-staff-engineer.md and reviews/T-017-product-manager.md in full",
  "python3 tools/board.py validate -> 'ok (48 file(s))' (before writing this review)",
  "python3 tools/board.py list; show T-017, T-018, T-048; show T-027 and T-029..T-046 with grep for priority, depends_on, status and AC lines; show Descriptions of T-027, T-029, T-036, T-038, T-039, T-045",
  "cat -n docs/M2M3_COVERAGE.md (lines 3-19 critical path and cut order, 8-15 ship-bar table, 22 R-ID header, 96 row 10)",
  "python3 -c read of artifacts/tmp/contract_fixes.json: 19 entries (6 manag, 4 paral, 9 engin) mapped to the cards they name",
  "grep -n verify_quickly .claude/agents/paralegal-reviewer.md personas/paralegal.md -> agent body line 111",
  "sed/grep docs/LLM_VS_CODE.md rows 10, 12, 16 (lines 38, 40, 44); spec/REQUIREMENTS.md section 7 rows 3-5 (lines 327-329); memory/ORCHESTRATOR_DECISIONS.md and grep case_05 across docs, memory, spec (no row-10 decision); memory/SCOPE_CUTS.md (no variant E row); evals/golden/README.md:144 (case_07 total $420); memory/DECISIONS.md:169 (fixture by default); memory/contracts/api.md:26 ({token} export path)",
  "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt -> 68 checks, 31 pass, 37 fail; probe qa:NONE count = 11; longest chain to T-038: T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029"
 ],
 "verdict": "changes",
 "scores": {"majors_applied_in_full": 2, "ship_bar_traced": 3, "fixture_cannot_ship": 2, "regression_discipline": 4, "test_first_owners": 2, "golden_numbers_consistent": 2, "paralegal_journey_acs": 4},
 "findings": [
  {"severity": "major", "title": "PM1: stale 5-card critical path and 4 h sentence still in the coverage doc; per-card estimates missing; cut order touches the lexicon gate",
   "evidence": "docs/M2M3_COVERAGE.md:18 'Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 ... -> T-038' and :19 'This runs about 4 h, over the 3.5 h budget.' (check PM-1b, PM-1c). Estimates: 2 of 20 M2/M3 cards carry one (T-029 and T-039 'Timebox 1 h'); 18 do not (check PM-1d). docs/M2M3_COVERAGE.md:5 'M2 cut order (never touches ship-bar items) ... (3) lexicon held-out target lowered from 85% to reported'; docs/LLM_VS_CODE.md:44 '...whose recall on the golden set is a release gate'; spec/REQUIREMENTS.md:327 ship-bar row 3 'R-FL-1 to R-FL-4'.",
   "why_it_matters": "The doc now states two critical paths. At its own 30-45 min per card, seven cards is 3.5-5.25 h against a 3.5 h M2 budget, with no total and no cut trigger. Cut 3 lowers the floor under flag recall, which ship-bar row 3 measures per type, so 'never touches ship-bar items' is false as written.",
   "fix": "Delete coverage lines 18-19. Add an 'Estimate: N min' line to the Description of each of the 18 cards. State the total and the cut trigger in one sentence. Remove cut 3, or record in memory/SCOPE_CUTS.md that it touches R-FL-3/R-FL-4 (ship-bar row 3) before the cut is allowed.",
   "acceptance_test": "grep -c 'This runs about 4 h' docs/M2M3_COVERAGE.md = 0; board.py show prints an estimate in the Description of all 20 M2/M3 cards; the M2 cut order names no lever that touches REQUIREMENTS section 7 row 3 unless that impact is written next to it."},
  {"severity": "major", "title": "PM2: T-027 raised to P0 without the timebox the fix requires",
   "evidence": "python3 tools/board.py show T-027: priority \"P0\" (applied). Description: 'Debt from T-009 ... Fix the patterns rather than the examples, and score on a held-out set.' No timebox (check PM-2b). T-036 depends_on still includes T-027.",
   "why_it_matters": "A P0 card with no stop rule gates the M2 chain through T-036 with no limit on how long it can run.",
   "fix": "Add a timebox line to T-027 Description, e.g. 'Timebox N h; at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md' (N set by the orchestrator).",
   "acceptance_test": "board.py show T-027 Description contains 'Timebox'."},
  {"severity": "major", "title": "PM3: T-045 AC4 still requires ship_bar_met true on the default run, which T-038 AC6 makes false on fixture",
   "evidence": "python3 tools/board.py show T-045 AC4: 'sensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `python -m evals.run` (ship_bar_met true), ...' (check PM-3c). T-038 AC6: 'ship_bar_met is false when backend == fixture'. memory/DECISIONS.md:169: 'tests and eval iteration use `fixture` by default'.",
   "why_it_matters": "A worker who follows AC4 literally runs the default fixture backend and gets ship_bar_met false, so the card either cannot close or someone sets the flag by hand. The claude-cli form is only in appended AC6, so the replay path the PM review targeted is still the default one.",
   "fix": "Replace AC4's bare '`python -m evals.run` (ship_bar_met true)' with '`LLM_BACKEND=claude-cli python -m evals.run` (ship_bar_met true)' in place; keep the fixture run as its own sensor line.",
   "acceptance_test": "board.py show T-045 AC4 contains 'LLM_BACKEND=claude-cli' and no bare '`python -m evals.run` (ship_bar_met true)'."},
  {"severity": "major", "title": "PM5: verify_quickly is in the paralegal agent body, but no M3 card or gate AC asks for it",
   "evidence": ".claude/agents/paralegal-reviewer.md:111 '**Ship-bar score (D-015):** ... your review JSON must include `scores.verify_quickly` (1–5) ... ≥ 4 is the ship bar.' (applied). M3 cards whose ACs name the key: none (check PM-5b). The only other hits are T-025 and T-038 AC8, whose 'New orchestrator card (M3)' does not exist on the board.",
   "why_it_matters": "Ship-bar row 5 (spec/REQUIREMENTS.md:329) is the one human number. Without an M3 AC that requests it, the M3 gate can close on a paralegal review with no score.",
   "fix": "Create the M3 card the fix named, or add an AC to T-045: 'M3 gate paralegal review writes reviews/<card>-paralegal.md with scores.verify_quickly (D-015); ship bar 5 met when >= 4'.",
   "acceptance_test": "board.py show of an M3 card includes an AC naming scores.verify_quickly; grep -l verify_quickly board/cards/T-04*.md lists it."},
  {"severity": "major", "title": "PM6: the lexicon-recall release gate is undecided; T-038 AC9 is an 'or' and LLM_VS_CODE still calls it a gate",
   "evidence": "python3 tools/board.py show T-038 AC9: '...add `lexicon_recall_must_flags` ... and state the threshold in REQUIREMENTS section 7 by ADR, or edit LLM_VS_CODE rows 12/16 to \"reported, not gated\".' (open 'or', check PM-6d). docs/LLM_VS_CODE.md:44 '...whose recall on the golden set is a release gate' (check PM-6c). T-038 AC1 metric list has no lexicon metric.",
   "why_it_matters": "The injection defence (R-RV-6) is either gated or not, and the product note will say one or the other. The coverage cut order already treats it as ungated; the LLM/code table still says gated.",
   "fix": "Choose one and record it in memory/ORCHESTRATOR_DECISIONS.md. Either add lexicon_recall_must_flags to T-038 AC1 with a threshold, or edit LLM_VS_CODE rows 12 and 16 to 'reported, not gated' and delete 'release gate'. Remove the 'or' from T-038 AC9.",
   "acceptance_test": "grep -c 'release gate' docs/LLM_VS_CODE.md = 0 and T-038 has no 'or edit' text; or jq '.metrics.lexicon_recall_must_flags' evals/reports/latest.json returns a number after T-038 runs."},
  {"severity": "major", "title": "PL2: T-039 AC2 still says dismissing entry 5 alone gives '7 of 9'; the corrected AC is appended as AC7",
   "evidence": "python3 tools/board.py show T-039 AC2: '...dismissing entry 5 gives \"Record 5 ... dismissed\" and 7 of 9 (R-EX-4, R-EX-7)' (check PL-2b, not removed). Corrected text is AC7 only: 'dismissing entry 5 and leaving entry 6 pending gives ... and 7 of 9'.",
   "why_it_matters": "One card gives two counts for the same dismissal. With only entry 5 dismissed the letter holds 8 of 9 records, so the uncorrected AC2 encodes the wrong count and a correct build can fail it.",
   "fix": "Replace T-039 AC2's 'dismissing entry 5 gives ... 7 of 9' in place with the AC7 wording, and delete AC7.",
   "acceptance_test": "grep -c 'dismissing entry 5 gives' board/cards/T-039.md = 0."},
  {"severity": "major", "title": "S1: 11 test files still have no qa author; T-039 does not name them",
   "evidence": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... -> 'qa:NONE count = 11 -> [test_api, test_charges, test_edit, test_export_ui, test_flags_panel, test_input, test_keyboard_mobile, test_review_matrix, test_side_by_side, test_source_record, test_timeline]'. T-039 AC8 is the instruction 'name test_api.py plus the 10 E2E files above, by file'; no T-039 AC names any of the 11 (check S-1b).",
   "why_it_matters": "CONTRACT:240 gives tests/** to qa. These files are cited by backend and frontend ACs, so those cards cannot be test-first, and T-039's 'test-first' covers them only by R-ID.",
   "fix": "Rewrite T-039 AC4 to list the 11 files by name with the R-IDs each covers. test_api.py may move to T-048. Re-run the applied-check.",
   "acceptance_test": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... prints 'qa:NONE count = 0'."},
  {"severity": "major", "title": "S7: the row-10 engine is still an 'Either ... or' instruction; no decision is recorded",
   "evidence": "python3 tools/board.py show T-033 AC6: 'Either T-033 gains AC6 ... or an ADR edits row 10 and T-036 AC3 says ...' (check S-7a); same text on T-036 AC10. docs/M2M3_COVERAGE.md:96 '| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |'. docs/LLM_VS_CODE.md:38 row 10 '... the same provider spelled two ways | **Code**'. grep case_05 across docs, memory and spec: no decision (only spec/REQUIREMENTS.md).",
   "why_it_matters": "The table says code, the plan gives it to the LLM card, and the T-036 implementer will pick one. A provider-name conflict raised by both engines shows the panel the same flag twice.",
   "fix": "Decide and record it. Either provider-variant conflict is Code (a T-033 AC with no LLM call, row 10 unchanged), or row 10 changes by ADR. Replace the 'Either' text on T-033 AC6 and T-036 AC10 with the decision, and update docs/M2M3_COVERAGE.md row 10 to match.",
   "acceptance_test": "grep -c 'Either' board/cards/T-033.md board/cards/T-036.md = 0; coverage row 10 and LLM_VS_CODE row 10 name the same engine."},
  {"severity": "major", "title": "S9: T-039 AC1 still asserts $8,390.00 for case_07; the $420 line is appended as AC9",
   "evidence": "python3 tools/board.py show T-039 AC1: 'total line exactly \"Billed charges stated in these records: $8,390.00\" incl. case_07 with a rate present' (check S-9a). Golden: evals/golden/README.md:144 'Total $420; $50,000 never totaled'. Corrected text is AC9 only.",
   "why_it_matters": "A test-first card that asserts $8,390 for case_07 contradicts the golden $420 total and leaves the implementer to pick. A wrong money assertion is the bad-day case for this product.",
   "fix": "Replace AC1's case_07 clause in place with the AC9 wording ('on case_07 with $420 accepted it is exactly ... $420.00'), and delete AC9.",
   "acceptance_test": "board.py show T-039 AC1 contains '$420.00' on case_07 and does not contain '$8,390.00 incl. case_07'."},
  {"severity": "major", "title": "N1: T-018 AC2 is ticked on evidence this check refutes",
   "evidence": "python3 tools/board.py show T-018 AC2 evidence: 'every blocker/major applied as AC edit/new card (artifacts/tmp/contract_fixes.json); verified by reviews/T-018-product-manager.md'. T-018 Handoff: '~23 majors applied as AC edits/deps/new card T-048 before any M2 claim.' This check: 9 of 19 contract majors not applied (PM1, PM2, PM3, PM5, PM6, PL2, S1, S7, S9), see the table above.",
   "why_it_matters": "The gate that closes the contract review records a claim this check refutes. Later cards would treat the M2 contract as settled.",
   "fix": "Reopen T-018 AC2 (done false) or change its evidence to this review's verdict. Correct the handoff count to the applied number once PM1-S9 land.",
   "acceptance_test": "board.py show T-018 shows AC2 done false, or AC2 evidence cites reviews/T-018-product-manager.md with verdict pass."},
  {"severity": "minor", "title": "Unapplied PM minors (not gating): cut clock, flag-group count, token-log test, golden variant E, 'only' in T-033 AC1, {id} path",
   "evidence": "python3 tools/board.py show T-046 AC5: 'cut order per REQUIREMENTS section 4 recorded if M3 passes 100% of budget' (no clock, check m-PM1a). T-037 AC1: 'prints ... all flag groups' (m-PM1b). T-040 AC5: 'no access log of tokens' (m-PM1c). docs/LLM_VS_CODE.md:44 'documented as golden variant E, a qa item, not yet in the golden set'; no variant E in memory/SCOPE_CUTS.md or any card AC (m-PM2). T-033 AC1: 'sample yields $6,240, $185, $2,150 only' (S-8b). T-041 AC4: 'GET /api/cases/{id}/export' (nit; memory/contracts/api.md:26 spells {token}).",
   "why_it_matters": "Each is a check a worker can tick without proving anything. The variant E item is the one injection path only the human catches, and the note should cite it.",
   "fix": "T-046 AC5: quote M3 start and end timestamps from board activity and state the trigger. T-037 AC1: name the five groups with counts 1/2/2/5/0. T-040 AC5: add test_api::test_no_token_in_logs. Add variant E to T-038 or a SCOPE_CUTS row. T-033 AC1: replace 'only' with the damages mention. T-041 AC4: {token}.",
   "acceptance_test": "Each named test or command exists and fails when its condition is broken."},
  {"severity": "minor", "title": "Unapplied PL minors (not gating): reason sentence inline, full $185 string, charge highlight and banner record, dismissal reason to notes",
   "evidence": "python3 tools/board.py show T-042 AC2: 'timeline rows show date, provider, summary, excerpt, state' (no inline reason, m-PL1). T-043 AC2: \"$185 'rate $185/visit; visit count not stated'\" (truncated, m-PL2). T-043 AC1 'case_07 shows an injection warning' (no record 3, m-PL3b); T-043 AC5 'gap flag opens both records 6 and 7' (no $6,240 charge highlight, m-PL3a). T-043 AC3 'dismiss -> reset -> dismiss' (no reason, m-PL4).",
   "why_it_matters": "She reads why an item needs review on sight, and she reconciles $6,240 against the ER record. Each of these is a fact she checks in the first minute.",
   "fix": "T-042 AC2: 'every needs_review row shows its why-template sentence inline'. T-043 AC2: quote the full R-CH-3 string. T-043 AC1: 'case_07 banner names record 3 and says flags may be incomplete'. T-043 AC5: '$6,240 charge opens record 2 with \"ER charges: $6,240.\" highlighted'. T-043 AC3: dismiss the gap flag with a reason and check it in the notes FLAGS DISMISSED.",
   "acceptance_test": "tests/e2e/test_timeline.py::test_reason_inline; test_flags_panel.py::test_injection_banner_names_record; test_source_record.py::test_charge_highlight; test_review_matrix.py::test_dismiss_reason_in_notes."},
  {"severity": "minor", "title": "Unapplied staff minors (not gating): xfail instead of --collect-only, retry prompt hash, judge input isolation, verifier mutation guard, network guard",
   "evidence": "python3 tools/board.py show T-029 AC3: 'proved by `pytest tests/unit -q --collect-only` listing them' (m-S1). T-034 AC2: 'each retry with changed conditions' (no prompt-hash check, m-S2a). T-035 AC5: 'prompts are versioned files ... the generator and judge never share a prompt' (no input-isolation check, m-S2b). T-030 has 5 ACs, none naming monkeypatch or mutation (m-S3). T-029 AC5 names no socket or network guard (m-S4).",
   "why_it_matters": "Collected-but-broken red tests pass for 'red'; a retry that resends the same prompt passes; a verifier stubbed to pass goes unnoticed; one stray network call makes the suite flaky and costs money.",
   "fix": "T-029 AC3: each new test is xfail(strict=True, reason='T-0xx') and pytest -rx shows them. T-034 AC2: consecutive attempts have different prompt hashes in llm_calls. T-035 AC5: the rendered judge #1 prompt holds the record and candidate only. T-030 AC6: monkeypatching grounding.verify to pass fails test_grounding and test_pipeline. T-029 AC5: tests/conftest.py blocks socket.connect except localhost.",
   "acceptance_test": "test_provider::test_fixture_miss_raises style tests exist; each named test fails when its condition is broken."},
  {"severity": "minor", "title": "N2: instruction-style ACs copied onto 2-3 cards; one asks a db card to rewrite a planning doc at stale line numbers",
   "evidence": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... INFO line: \"instruction-style 'Contract review (T-018):' ACs copied onto more than one card: 11 distinct texts\"; ['T-031', 'T-034', 'T-036']: 'Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain ...' (T-031 AC6 is a db card); ['T-029', 'T-039']: 'T-029 AC4 or a new qa card ...'.",
   "why_it_matters": "Three workers tick copies of the same doc rewrite, and nobody owns the outcome. The line references are already stale (the doc moved).",
   "fix": "One owner per instruction. The coverage-doc change belongs to the orchestrator card, not to T-031, T-034 or T-036. Replace each copied instruction with a testable AC on the card that owns the outcome.",
   "acceptance_test": "the applied-check INFO line shows no 'Contract review (T-018):' text on more than one card."}
 ],
 "whats_right": [
  "T-048 exists with deps [] and T-034, T-035, T-036 and T-037 depend on it; T-031, T-042 and T-043 got their depends_on edges (S1 test-first wiring, S2 edges).",
  "The fixture-cannot-ship rule is on the board (T-038 AC6) with the 50 seeded judge lines and SE1-SE5 named (T-037 AC6-AC7), and the regression freshness check is on T-038 AC7.",
  "The paralegal journey gaps are now ACs: edited items survive reload (T-044 AC6), two accident dates shown side by side (T-043 AC6), record 4 visible as failed (T-042 AC6, T-041 AC6)."
 ],
 "questions_for_chris": ["Is the lexicon held-out recall (LLM_VS_CODE row 16, 'a release gate') a gate you will hold to? Your answer decides whether M2 cut 3 is allowed and whether T-038 gets a metric or the table changes (finding PM6)."]}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:19.758Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-017-product-manager-r2.md",
 "description": "Read prior T-017 r2 product-manager review"
}
````

### User / tool · 2026-11-02T01:33:19.835Z

**tool result**
````
# T-017 round 2: product-manager-reviewer apply-check of the round-1 plan findings

**Verdict: changes.** 0 blockers. 4 majors from `reviews/T-017-product-manager.md` are not applied (one of them is only partly applied). Plus 1 minor and 1 nit. Evidence comes from the same run as the T-018 review: `artifacts/review-evidence/T-018-r2-applied-check.py`, output in `artifacts/review-evidence/T-018-r2-applied-check.out.txt`.

What landed: the M2 cut order (`docs/M2M3_COVERAGE.md:5`), the ship-bar to card table (`:8-15`), the seven-card critical path in `:4`, T-048 as the qa card for LLM-stage tests, and T-027 at P0. What did not: the pass-condition column, the in-place AC fixes, the qa owner gap (11 files left), the row-10 decision, and the stale chain text that still sits in the same doc.

| Round-1 finding | Status | Evidence (verbatim) |
|---|---|---|
| Major 1: coverage counts mentions, not pass conditions | NOT APPLIED | `docs/M2M3_COVERAGE.md:22` "`| R-ID | Cards |`", no pass-condition column (T17-1a). |
| Major 2: three AC contradict golden or REQUIREMENTS; plan self-check | NOT APPLIED | T-039 AC1 still "'Billed charges stated in these records: $8,390.00' incl. case_07" (S-9a); T-039 AC2 still "dismissing entry 5 gives ... and 7 of 9" (PL-2b); T-033 AC1 still "$2,150 only" (S-8b). No plan self-check line in the coverage doc (T17-2a). |
| Major 3: unowned validation; row 10 engine | NOT APPLIED | Probe "qa:NONE count = 11". `docs/M2M3_COVERAGE.md:96` "T-036 (m2-be-llm-flags) (provider variants)"; `docs/LLM_VS_CODE.md:38` row 10 "...the same provider spelled two ways | **Code**"; no decision recorded (S-7c). |
| Major 4: critical path, budget, cut order, ship-bar trace | PARTLY APPLIED, NOT APPLIED AS A WHOLE | Applied: `:4` seven-card chain, `:5` M2 cut order, `:8-15` ship-bar table. Not applied: `:18` "Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 ..." and `:19` "This runs about 4 h, over the 3.5 h budget." still there (T17-4a/b; PM1). Cut `:5` item (3) "lexicon held-out target lowered from 85% to reported" conflicts with `docs/LLM_VS_CODE.md:44` "...whose recall on the golden set is a release gate" (T17-4c; PM6). |
| Minor: T-017 AC2 evidence overstates | NOT APPLIED | `python3 tools/board.py show T-017` AC2 evidence still "rows 1-20 all mapped" (m-T17); row 19 is M3 at `docs/M2M3_COVERAGE.md:105` and row 15 edit half at `:101`. |

## Findings

```json
{"card": "T-017", "persona": "product-manager-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round-2 apply-check of reviews/T-017-product-manager.md (4 majors, 1 minor) against the current plan: docs/M2M3_COVERAGE.md, board/cards T-027, T-029..T-039, T-041..T-048 (AC text and depends_on), docs/LLM_VS_CODE.md rows 10, 12, 16, evals/golden/README.md, spec/REQUIREMENTS.md section 7. No app code exists; plan review only.",
 "exercised": [
  "read reviews/T-017-product-manager.md in full (round-1 findings and the exact fix text)",
  "python3 tools/board.py show T-017 (AC1, AC2 evidence and round-1 notes); show T-018 Handoff",
  "cat -n docs/M2M3_COVERAGE.md (lines 3-19, 22, 84-108)",
  "python3 tools/board.py show on T-027, T-029..T-039, T-041..T-048 (AC lines, depends_on, Descriptions) to test each fix",
  "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt: T17-1a, T17-2a, T17-3, T17-4a/b/c, m-T17 (plus the card checks it depends on, S-7b, S-9a, PL-2b, S-8b); probe qa:NONE = 11; longest chain T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029",
  "probe depends_on: T-034 ['T-031', 'T-048'] and T-031 ['T-029'] (second seven-card path)",
  "grep -n 'row 10|row 16|release gate' docs/LLM_VS_CODE.md (rows 16 line 44 'release gate'); grep case_05 across docs, memory, spec (no decision)",
  "python3 tools/board.py validate -> ok (48 file(s)) before writing this review"
 ],
 "verdict": "changes",
 "scores": {"coverage_pass_conditions": 2, "ac_consistent_with_golden": 2, "qa_owned_tests": 2, "critical_path_and_cut_order": 2, "ship_bar_traced": 3},
 "findings": [
  {"severity": "major", "title": "Round-1 major 1 not applied: coverage still counts R-ID mentions; no pass-condition column",
   "evidence": "docs/M2M3_COVERAGE.md:22 '| R-ID | Cards |' (header unchanged, no pass-condition column; applied-check T17-1a: no match). The R-RV-8 test input 'accept 3 items, edit 1, reload' now has an AC (T-044 AC6, 'reload -> edited summary and \"edited\" label persist'), but the matrix does not point to it.",
   "why_it_matters": "T-017 AC1 was ticked by looking up mentions. Without a pass-condition column, the next R-ID can be marked covered by a card that never tests its REQUIREMENTS input, which is how the lost-edit and merged-date cases got through round 1.",
   "fix": "Add a 'Pass condition -> AC' column to docs/M2M3_COVERAGE.md for every R-ID row: quote the REQUIREMENTS test input and cite the AC id. Start with R-RV-8 -> T-044 AC6, R-CO-9 -> T-042 AC6 and T-041 AC6, R-EX-4(10) -> T-044 AC6 and T-039 AC6, R-FL-2(a) -> T-043 AC6.",
   "acceptance_test": "Every R-ID row in docs/M2M3_COVERAGE.md has a non-empty pass-condition cell; each cell quotes the REQUIREMENTS test input and names an AC that contains it (grep the AC text)."},
  {"severity": "major", "title": "Round-1 major 2 not applied: three ACs still contradict golden or REQUIREMENTS in place; no plan self-check",
   "evidence": "python3 tools/board.py show T-039 AC1: 'total line exactly \"Billed charges stated in these records: $8,390.00\" incl. case_07 with a rate present' (S-9a). T-039 AC2: 'dismissing entry 5 gives \"Record 5 ... dismissed\" and 7 of 9' (PL-2b). T-033 AC1: 'sample yields $6,240, $185, $2,150 only' (S-8b). The corrected wording exists only in appended ACs (T-039 AC9, T-039 AC7, T-033 AC7). docs/M2M3_COVERAGE.md has no plan self-check line (T17-2a).",
   "why_it_matters": "Under test-first, a card that contradicts itself is one the implementer will 'fix' by editing the test, which is the thing the plan says must not happen. The golden says case_07 total is $420 (evals/golden/README.md:144).",
   "fix": "Edit T-039 AC1, T-039 AC2 and T-033 AC1 in place to the corrected text and delete the appended duplicates (T-039 AC7, AC9). Add to docs/M2M3_COVERAGE.md: 'Plan self-check: every number in an AC is diffed against evals/golden expected values before in_review.'",
   "acceptance_test": "board.py show T-039 contains no 'incl. case_07' next to '$8,390.00', no 'dismissing entry 5 gives'; T-033 AC1 has no 'only' next to the three amounts; docs/M2M3_COVERAGE.md contains the self-check sentence."},
  {"severity": "major", "title": "Round-1 major 3 not applied: 11 test files still have no qa author; LLM_VS_CODE row 10 and the coverage row disagree",
   "evidence": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ...: 'qa:NONE count = 11 -> [test_api, test_charges, test_edit, test_export_ui, test_flags_panel, test_input, test_keyboard_mobile, test_review_matrix, test_side_by_side, test_source_record, test_timeline]' (T-048 covers 9 of 20). docs/M2M3_COVERAGE.md:96 '| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |' against docs/LLM_VS_CODE.md:38 '...the same provider spelled two ways | **Code**'. No ADR or decision (S-7c).",
   "why_it_matters": "T-017 AC2 says each card AC names its test. Eleven named test files have no author, and the engine for provider conflicts is still unresolved, so an implementer can produce the same conflict twice.",
   "fix": "Name the 11 files by path on T-039 (or T-048) with the R-IDs each covers. Decide row 10 by ADR or by a code AC on T-033, and make docs/M2M3_COVERAGE.md row 10 match the decision.",
   "acceptance_test": "The applied-check prints 'qa:NONE count = 0'; coverage row 10 and LLM_VS_CODE row 10 name the same engine."},
  {"severity": "major", "title": "Round-1 major 4 not applied as a whole: the doc still has two critical paths, no per-card estimates, and a cut that touches the lexicon gate",
   "evidence": "docs/M2M3_COVERAGE.md:4 'M2 critical path (7 cards): T-029/T-048 (tests first) -> T-032 ... -> T-038 eval runner.' (applied; matches the probe chain). But :18 'Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 ... -> T-038' and :19 'This runs about 4 h, over the 3.5 h budget.' remain (T17-4a/b). Per-card estimates absent on 18 of 20 cards (PM1). Cut :5 item (3) 'lexicon held-out target lowered from 85% to reported' vs docs/LLM_VS_CODE.md:44 '...recall on the golden set is a release gate' (T17-4c).",
   "why_it_matters": "A reader who reaches line 18 gets a different critical path and a '4 h, over budget' verdict. The table at :8-15 and the cut order at :5 are right in shape, but the cut order claims it 'never touches ship-bar items' while cut (3) lowers the floor under flag recall that ship-bar row 3 measures.",
   "fix": "Delete docs/M2M3_COVERAGE.md lines 18-19. Add 'Estimate: N min' to each card Description (PM1). Resolve the lexicon gate (PM6) before keeping cut (3), and state which ship-bar row each cut touches.",
   "acceptance_test": "grep -c 'T-030 (m2-be-grounding) -> T-035' docs/M2M3_COVERAGE.md = 0; estimates present on all 20 M2/M3 cards; the lexicon gate decision is recorded in ORCHESTRATOR_DECISIONS.md."},
  {"severity": "minor", "title": "T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-1 minor, not reworded)",
   "evidence": "python3 tools/board.py show T-017, AC2 evidence: \"docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval\" (m-T17). docs/M2M3_COVERAGE.md:105 row 19 maps to T-041 and T-045, both M3 cards; :101 row 15 edit half maps to T-040 (M3).",
   "why_it_matters": "The evidence claims more than the artifact shows about M2, which is the habit the gate looks for.",
   "fix": "Reword the AC2 evidence: 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.",
   "acceptance_test": "board.py show T-017 AC2 evidence does not contain 'rows 1-20 all mapped'."},
  {"severity": "nit", "title": "The seven-card critical path has a tie that the doc does not mention",
   "evidence": "Probe depends_on: T-034 ['T-031', 'T-048']; T-031 ['T-029']. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. docs/M2M3_COVERAGE.md:4 names only the T-032/T-033 route.",
   "why_it_matters": "Which path is longest decides which card the cut order protects. A reader can't tell from line 4 which path to watch.",
   "fix": "Add one clause to :4: 'ties with T-029 -> T-031 -> T-034 -> ... -> T-038'.",
   "acceptance_test": "docs/M2M3_COVERAGE.md:4 names both seven-card paths, or the probe shows one longest path."}
 ],
 "whats_right": [
  "The M2 cut order and the ship-bar to card table are on the page (docs/M2M3_COVERAGE.md:5 and :8-15), so the gate can point at them.",
  "T-048 is the qa card for the LLM-stage tests with deps []; T-034, T-035, T-036 and T-037 depend on it.",
  "T-027 is P0 and T-036 keeps its dependency, so the lexicon work sits on the path it gates."
 ],
 "questions_for_chris": ["Is the lexicon held-out recall (LLM_VS_CODE row 16, 'a release gate') a gate you will hold to? It decides whether M2 cut (3) is allowed and whether T-038 gets a metric or the table changes."]}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:20.078Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-017-product-manager.md",
 "description": "Read prior T-017 product-manager review"
}
````

### User / tool · 2026-11-02T01:33:20.159Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:29.798Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/board.py validate; echo \"---\"; .venv/bin/python tools/board.py show T-017; echo \"---\"; .venv/bin/python tools/board.py show T-018",
 "description": "Validate board and show T-017 and T-018 cards"
}
````

### User / tool · 2026-11-02T01:33:30.037Z

**tool result**
````
ok (48 file(s))
---
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
updated_at: "2026-11-02T01:33:03Z"
claimed_by: "orchestrator"
claimed_at: "2026-11-02T01:33:03Z"
rounds: 2
commits: []
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-017-product-manager.md", "at": "2026-11-02T01:23:10Z"}
  - {"persona": "product-manager-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-017-product-manager-r2.md", "at": "2026-11-02T01:32:41Z"}
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
- 2026-11-02T01:32:41Z orchestrator: review product-manager-reviewer (claude-haiku-5-5): changes — reviews/T-017-product-manager-r2.md; round 2; findings:
    - [major] Round-1 major 1 not applied: coverage still counts R-ID mentions; no pass-condition column — fix: Add a 'Pass condition -> AC' column to docs/M2M3_COVERAGE.md for every R-ID row: quote the REQUIREMENTS test input and cite the AC id. Start with R-RV-8 -> T-044 AC6, R-CO-9 -> T-042 AC6 and T-041 AC6, R-EX-4(10) -> T-044 AC6 and T-039 AC6, R-FL-2(a) -> T-043 AC6.
    - [major] Round-1 major 2 not applied: three ACs still contradict golden or REQUIREMENTS in place; no plan self-check — fix: Edit T-039 AC1, T-039 AC2 and T-033 AC1 in place to the corrected text and delete the appended duplicates (T-039 AC7, AC9). Add to docs/M2M3_COVERAGE.md: 'Plan self-check: every number in an AC is diffed against evals/golden expected values before in_review.'
    - [major] Round-1 major 3 not applied: 11 test files still have no qa author; LLM_VS_CODE row 10 and the coverage row disagree — fix: Name the 11 files by path on T-039 (or T-048) with the R-IDs each covers. Decide row 10 by ADR or by a code AC on T-033, and make docs/M2M3_COVERAGE.md row 10 match the decision.
    - [major] Round-1 major 4 not applied as a whole: the doc still has two critical paths, no per-card estimates, and a cut that touches the lexicon gate — fix: Delete docs/M2M3_COVERAGE.md lines 18-19. Add 'Estimate: N min' to each card Description (PM1). Resolve the lexicon gate (PM6) before keeping cut (3), and state which ship-bar row each cut touches.
    - [minor] T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-1 minor, not reworded) — fix: Reword the AC2 evidence: 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.
- 2026-11-02T01:33:03Z orchestrator: claimed
- 2026-11-02T01:33:03Z orchestrator: moved in_progress -> in_review
- 2026-11-02T01:33:03Z orchestrator: review dispatched: haiku recheck

## Handoff
In-place fixes (commit after 2329ac2): contradicting ACs edited (T-033, T-036, T-038, T-039, T-041, T-045), D-025/D-026, LLM_VS_CODE rows 12/16, coverage doc cleanup + self-check, per-card estimates, T-027 timebox, verify_quickly in T-045. The reviewer's own script artifacts/review-evidence/T-018-r2-applied-check.py now reports 0 unapplied majors.

---
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
updated_at: "2026-11-02T01:33:09Z"
claimed_by: "orchestrator"
claimed_at: "2026-11-02T01:33:09Z"
rounds: 1
commits: []
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-018-product-manager.md", "at": "2026-11-02T01:32:41Z"}
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
- 2026-11-02T01:32:41Z orchestrator: review product-manager-reviewer (claude-haiku-5-5): changes — reviews/T-018-product-manager.md; round 1; findings:
    - [major] PM1: stale 5-card critical path and 4 h sentence still in the coverage doc; per-card estimates missing; cut order touches the lexicon gate — fix: Delete coverage lines 18-19. Add an 'Estimate: N min' line to the Description of each of the 18 cards. State the total and the cut trigger in one sentence. Remove cut 3, or record in memory/SCOPE_CUTS.md that it touches R-FL-3/R-FL-4 (ship-
    - [major] PM2: T-027 raised to P0 without the timebox the fix requires — fix: Add a timebox line to T-027 Description, e.g. 'Timebox N h; at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md' (N set by the orchestrator).
    - [major] PM3: T-045 AC4 still requires ship_bar_met true on the default run, which T-038 AC6 makes false on fixture — fix: Replace AC4's bare '`python -m evals.run` (ship_bar_met true)' with '`LLM_BACKEND=claude-cli python -m evals.run` (ship_bar_met true)' in place; keep the fixture run as its own sensor line.
    - [major] PM5: verify_quickly is in the paralegal agent body, but no M3 card or gate AC asks for it — fix: Create the M3 card the fix named, or add an AC to T-045: 'M3 gate paralegal review writes reviews/<card>-paralegal.md with scores.verify_quickly (D-015); ship bar 5 met when >= 4'.
    - [major] PM6: the lexicon-recall release gate is undecided; T-038 AC9 is an 'or' and LLM_VS_CODE still calls it a gate — fix: Choose one and record it in memory/ORCHESTRATOR_DECISIONS.md. Either add lexicon_recall_must_flags to T-038 AC1 with a threshold, or edit LLM_VS_CODE rows 12 and 16 to 'reported, not gated' and delete 'release gate'. Remove the 'or' from T-038 AC9.
    - [major] PL2: T-039 AC2 still says dismissing entry 5 alone gives '7 of 9'; the corrected AC is appended as AC7 — fix: Replace T-039 AC2's 'dismissing entry 5 gives ... 7 of 9' in place with the AC7 wording, and delete AC7.
    - [major] S1: 11 test files still have no qa author; T-039 does not name them — fix: Rewrite T-039 AC4 to list the 11 files by name with the R-IDs each covers. test_api.py may move to T-048. Re-run the applied-check.
    - [major] S7: the row-10 engine is still an 'Either ... or' instruction; no decision is recorded — fix: Decide and record it. Either provider-variant conflict is Code (a T-033 AC with no LLM call, row 10 unchanged), or row 10 changes by ADR. Replace the 'Either' text on T-033 AC6 and T-036 AC10 with the decision, and update docs/M2M3_COVERAGE.md row 10 to match.
    - [major] S9: T-039 AC1 still asserts $8,390.00 for case_07; the $420 line is appended as AC9 — fix: Replace AC1's case_07 clause in place with the AC9 wording ('on case_07 with $420 accepted it is exactly ... $420.00'), and delete AC9.
    - [major] N1: T-018 AC2 is ticked on evidence this check refutes — fix: Reopen T-018 AC2 (done false) or change its evidence to this review's verdict. Correct the handoff count to the applied number once PM1-S9 land.
    - [minor] Unapplied PM minors (not gating): cut clock, flag-group count, token-log test, golden variant E, 'only' in T-033 AC1, {id} path — fix: T-046 AC5: quote M3 start and end timestamps from board activity and state the trigger. T-037 AC1: name the five groups with counts 1/2/2/5/0. T-040 AC5: add test_api::test_no_token_in_logs. Add variant E to T-038 or a SCOPE_CUTS row. T-033 AC1: repla
    - [minor] Unapplied PL minors (not gating): reason sentence inline, full $185 string, charge highlight and banner record, dismissal reason to notes — fix: T-042 AC2: 'every needs_review row shows its why-template sentence inline'. T-043 AC2: quote the full R-CH-3 string. T-043 AC1: 'case_07 banner names record 3 and says flags may be incomplete'. T-043 AC5: '$6,240 charge opens record 2 with "
    - [minor] Unapplied staff minors (not gating): xfail instead of --collect-only, retry prompt hash, judge input isolation, verifier mutation guard, network guard — fix: T-029 AC3: each new test is xfail(strict=True, reason='T-0xx') and pytest -rx shows them. T-034 AC2: consecutive attempts have different prompt hashes in llm_calls. T-035 AC5: the rendered judge #1 prompt holds the record and ca
    - [minor] N2: instruction-style ACs copied onto 2-3 cards; one asks a db card to rewrite a planning doc at stale line numbers — fix: One owner per instruction. The coverage-doc change belongs to the orchestrator card, not to T-031, T-034 or T-036. Replace each copied instruction with a testable AC on the card that owns the outcome.
- 2026-11-02T01:33:09Z orchestrator: claimed
- 2026-11-02T01:33:09Z orchestrator: moved in_progress -> in_review
- 2026-11-02T01:33:09Z orchestrator: review dispatched: haiku recheck

## Handoff
In-place fixes applied; the reviewer's own script reports 0 unapplied majors (see T-017 handoff). Contract review findings → AC edits, deps, T-048, D-025/D-026.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:30.202Z

**tool call — Bash**
````
{
 "command": "cat -n docs/M2M3_COVERAGE.md",
 "description": "Read the M2/M3 coverage doc with line numbers"
}
````

### User / tool · 2026-11-02T01:33:30.280Z

**tool result**
````
     1	# M2 + M3 coverage (T-017, revised after T-018 contract review)
     2	
     3	## Critical path and cut order (orchestrator)
     4	- M2 critical path (7 cards): T-029/T-048 (tests first) → T-032 ingest → T-033 amounts/gaps → T-035 generator+judges → T-036 LLM flags → T-037 pipeline+fixtures → T-038 eval runner. Estimates ~30–45 min each with 4 workers in parallel (T-030 grounding, T-031 db, T-034 provider, T-027 lexicon run beside the chain).
     5	- M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) T-046 side-by-side is M3's first cut; no ship-bar item is ever cut.
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
    18	
    19	## Plan self-check
    20	Pass conditions live in each card's AC on the board (each names its test/eval/command); this table maps ownership. Numbers in AC are checked against the golden set by T-038 (`--check-spec`) and the qa test-first cards (T-029, T-048, T-039).
    21	
    22	## R-ID -> card
    23	| R-ID | Cards |
    24	|---|---|
    25	| R-IN-1 | T-032 (m2-be-ingest-dates), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    26	| R-IN-2 | T-042 (m3-fe-input-timeline), T-039 (m3-qa-tests-first) |
    27	| R-IN-3 | T-032 (m2-be-ingest-dates), T-038 (m2-qa-eval-runner) |
    28	| R-IN-4 | T-032 (m2-be-ingest-dates), T-040 (m3-be-api-review), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    29	| R-IN-5 | T-032 (m2-be-ingest-dates), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
    30	| R-TL-1 | T-035 (m2-be-generator-judges), T-038 (m2-qa-eval-runner), T-042 (m3-fe-input-timeline) |
    31	| R-TL-2 | T-030 (m2-be-grounding), T-029 (m2-qa-unit-first) |
    32	| R-TL-3 | T-032 (m2-be-ingest-dates), T-035 (m2-be-generator-judges) |
    33	| R-TL-4 | T-035 (m2-be-generator-judges), T-038 (m2-qa-eval-runner) |
    34	| R-TL-5 | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    35	| R-TL-6 | T-040 (m3-be-api-review), T-042 (m3-fe-input-timeline) |
    36	| R-TL-7 | T-032 (m2-be-ingest-dates), T-038 (m2-qa-eval-runner) |
    37	| R-TL-8 | T-030 (m2-be-grounding), T-044 (m3-fe-edit-export) |
    38	| R-TL-9 | T-032 (m2-be-ingest-dates), T-035 (m2-be-generator-judges) |
    39	| R-TL-10 | T-030 (m2-be-grounding), T-040 (m3-be-api-review) |
    40	| R-FL-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
    41	| R-FL-2 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
    42	| R-FL-3 | T-036 (m2-be-llm-flags) |
    43	| R-FL-4 | T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner) |
    44	| R-FL-5 | T-030 (m2-be-grounding), T-036 (m2-be-llm-flags) |
    45	| R-FL-6 | T-043 (m3-fe-flags-charges-review) |
    46	| R-FL-7 | T-036 (m2-be-llm-flags), T-043 (m3-fe-flags-charges-review) |
    47	| R-FL-8 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
    48	| R-CH-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
    49	| R-CH-2 | T-033 (m2-be-amounts-gaps), T-035 (m2-be-generator-judges) |
    50	| R-CH-3 | T-033 (m2-be-amounts-gaps), T-043 (m3-fe-flags-charges-review), T-041 (m3-be-export) |
    51	| R-CH-4 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
    52	| R-CH-5 | T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review), T-039 (m3-qa-tests-first) |
    53	| R-CH-6 | T-033 (m2-be-amounts-gaps) |
    54	| R-CH-7 | T-040 (m3-be-api-review), T-039 (m3-qa-tests-first) |
    55	| R-RV-1 | T-043 (m3-fe-flags-charges-review), T-045 (m3-qa-e2e-journey) |
    56	| R-RV-2 | T-040 (m3-be-api-review), T-044 (m3-fe-edit-export), T-039 (m3-qa-tests-first) |
    57	| R-RV-3 | T-040 (m3-be-api-review), T-044 (m3-fe-edit-export) |
    58	| R-RV-4 | T-043 (m3-fe-flags-charges-review), T-045 (m3-qa-e2e-journey) |
    59	| R-RV-5 | T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
    60	| R-RV-6 | T-032 (m2-be-ingest-dates), T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner), T-045 (m3-qa-e2e-journey) |
    61	| R-RV-7 | withdrawn (D-011); no card |
    62	| R-RV-8 | T-031 (m2-db-schema), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
    63	| R-RV-9 | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline), T-043 (m3-fe-flags-charges-review) |
    64	| R-EX-1 | T-041 (m3-be-export), T-045 (m3-qa-e2e-journey) |
    65	| R-EX-2 | T-041 (m3-be-export), T-038 (m2-qa-eval-runner) |
    66	| R-EX-3 | T-041 (m3-be-export) |
    67	| R-EX-4 | T-041 (m3-be-export) |
    68	| R-EX-5 | T-044 (m3-fe-edit-export) |
    69	| R-EX-6 | T-041 (m3-be-export), T-044 (m3-fe-edit-export), T-038 (m2-qa-eval-runner) (spec = golden check) |
    70	| R-EX-7 | T-041 (m3-be-export), T-044 (m3-fe-edit-export) |
    71	| R-EX-8 | T-041 (m3-be-export) |
    72	| R-EX-9 | T-044 (m3-fe-edit-export) |
    73	| R-CO-1 | T-029 (m2-qa-unit-first) (boundary test), T-041 (m3-be-export) |
    74	| R-CO-2 | T-031 (m2-db-schema), T-037 (m2-be-pipeline-cli), T-045 (m3-qa-e2e-journey) |
    75	| R-CO-3 | T-038 (m2-qa-eval-runner) |
    76	| R-CO-4 | T-040 (m3-be-api-review) (demo gate). INST half is M4 (non-goal for M2/M3) |
    77	| R-CO-5 | T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    78	| R-CO-6 | T-034 (m2-be-provider-fixtures) |
    79	| R-CO-7 | T-038 (m2-qa-eval-runner) |
    80	| R-CO-8 | non-goal for M2/M3 cards: orchestrator logs SCOPE_CUTS; T-046 (m3-fe-side-by-side) AC logs R-ST-1 |
    81	| R-CO-9 | T-034 (m2-be-provider-fixtures) |
    82	| R-SU-1 .. R-SU-5 | non-goal for M2/M3: M4/M5 submission cards |
    83	| R-ST-1 | T-046 (m3-fe-side-by-side) |
    84	
    85	## LLM_VS_CODE row -> card
    86	| Row | Step | Cards |
    87	|---|---|---|
    88	| 1 | Split, merge duplicates | T-032 (m2-be-ingest-dates) |
    89	| 2 | Date parsing | T-032 (m2-be-ingest-dates) |
    90	| 3 | Date and provider by code | T-032 (m2-be-ingest-dates) |
    91	| 4 | Generator + rungs 1-2 | T-035 (m2-be-generator-judges), T-030 (m2-be-grounding) |
    92	| 5 | Clinical facts list: not built | T-035 (m2-be-generator-judges) (schema test enforces the omission) |
    93	| 6 | Find every amount | T-033 (m2-be-amounts-gaps) |
    94	| 7 | Amount class | T-033 (m2-be-amounts-gaps) (rules), T-035 (m2-be-generator-judges) (judge #2) |
    95	| 8 | Running total | T-033 (m2-be-amounts-gaps), T-041 (m3-be-export), T-043 (m3-fe-flags-charges-review) |
    96	| 9 | Gap > 30 days | T-033 (m2-be-amounts-gaps), T-037 (m2-be-pipeline-cli) |
    97	| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps): accident date and provider names, code only (D-025) |
    98	| 11 | Semantic conflicts + judge #3 | T-036 (m2-be-llm-flags) |
    99	| 12 | Pre-existing | T-036 (m2-be-llm-flags) |
   100	| 13 | Causation language | T-036 (m2-be-llm-flags) |
   101	| 14 | Flag wording by code | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
   102	| 15 | Numbers in summary/edit | T-030 (m2-be-grounding), T-040 (m3-be-api-review) |
   103	| 16 | Injection scan | T-032 (m2-be-ingest-dates), T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner) |
   104	| 17 | Confidence state | T-030 (m2-be-grounding) |
   105	| 18 | Why? sentence | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline) |
   106	| 19 | Sort, filter, export | T-041 (m3-be-export), T-045 (m3-qa-e2e-journey) |
   107	| 20 | Audit trail | T-031 (m2-db-schema), T-034 (m2-be-provider-fixtures), T-037 (m2-be-pipeline-cli) |
   108	
   109	Unmapped: none.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:55.586Z

**tool call — Bash**
````
{
 "command": "ls spec/ memory/ docs/ reviews/GATE* 2>&1; echo \"---REQ §7 ship bar---\"; grep -n \"\" spec/REQUIREMENTS.md | sed -n '315,335p'; echo \"---LLM_VS_CODE rows 10 12 16---\"; grep -n -E '^\\| (10|12|16) \\|' docs/LLM_VS_CODE.md",
 "description": "Read ship bar section and LLM_VS_CODE rows 10, 12, 16"
}
````

### User / tool · 2026-11-02T01:33:55.682Z

**tool result**
````
reviews/GATE-M0-summary.md
reviews/GATE-M1-summary.md

docs/:
CONTRACT.md
LLM_VS_CODE.md
M2M3_COVERAGE.md
RUNBOOK.md

memory/:
ASSUMPTIONS.md
DECISIONS.md
ENVIRONMENT.md
GLOSSARY.md
LESSONS.md
ORCHESTRATOR_DECISIONS.md
PROGRESS.md
SCOPE_CUTS.md
STATE.md
contracts

spec/:
REQUIREMENTS.md
SAMPLE_CASE_TRUTHS.md
SPEC.md
---REQ §7 ship bar---
315:If entry 5 were dismissed: the letter skips February 20, and "RECORDS NOT IN THE TREATMENT SECTION" reads "Record 5 (Capital PT, visit 8, February 20, 2026) — dismissed." The chronology never silently closes up.
316:
317:---
318:
319:## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
320:
321:These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.
322:
323:| # | Criterion (CONTRACT §8.2) | Number | Measured by | Run with | R-IDs |
324:|---|---|---|---|---|---|
325:| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
326:| 2 | **Recall** | ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set | `entry_recall`, `amount_recall` | `python -m evals.run` | R-TL-1, R-TL-7, R-CH-1 |
327:| 3 | **Flags** | Per flag type (gap, conflict, pre_existing, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
328:| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations.jsonl` (today 40, so at least 33). CONTRACT §5 M2 still says "qa injects 20"; the rate governs permanently and the product note quotes the rate. | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
329:| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` (1–5, D-015) ≥ 4; `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag content; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-6, R-RV-8, R-RV-9, R-EX-1 to R-EX-9 |
330:
331:Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).
332:
333:Rule for the product note: report what the eval **found**, including misses, not just the targets.
334:
335:---
---LLM_VS_CODE rows 10 12 16---
38:| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**: a lexicon of accident-date phrases ("date of accident", "DOA", "accident date", "collision on") plus date formats, compared with the earliest record date. Evidence is the stated-date quote and the `Date:` header line(s) of the earliest records. | Comparing two dates is not a language task, and the header line is part of the input text. | Unit test on the sample file with exact character offsets; both quotes ground; the two dates are shown side by side and never merged. No judge needed (arithmetic over quoted text). |
40:| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by code on every record as a second signal | Needs language judgment ("low back pain in 2023, resolved"). Running per record means one record's text never reaches the call that decides another record's flags; the phrase list is a second floor, trusted only as far as its measured recall on the golden set. | Quote check; **judge 4** confirms the category. If only the list or only the model fires, the item needs review and says which. |
44:| 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. Everything derived from that record needs review, its amounts cannot be charges, the cross-record conflict pass carries the warning, and a banner names the record and says flags may be incomplete. | A phrase list is easy to bypass, so it is a warning, not the defence. The defences are structural (rule 11). | Golden case 07: ordinary entry with a warning; the injected "$50,000" is in no total; the pre-existing flag from another record survives (per-record pass plus phrase list, whose recall on the golden set is reported, not gated (D-026)); nothing is accepted. A forged billing line in an untagged record is caught only by her accept (documented as golden variant E, a qa item, not yet in the golden set). |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:33:56.510Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"D-02[4-9]|lexicon|row 10|row 16|recall|reported, not gated|Plan self|pass.condition\" memory/ORCHESTRATOR_DECISIONS.md | head -60; echo \"---tail---\"; tail -n 25 memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Search orchestrator decisions for lexicon and row-10 entries"
}
````

### User / tool · 2026-11-02T01:33:56.602Z

**tool result**
````
13:| D-005 | Any record carrying an injection warning forces all its items to needs_review; its amounts can't be charges; it can't suppress flags from other records (lexicon is the floor). | Injected "$50,000" reached the total via code path alone. | T-014 privacy B1 |
20:| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged language may appear in the letter **only** as part of an accepted excerpt, and the internal notes list "flagged language quoted in the letter" so the attorney decides. NEEDS_CHRIS #10. | The records' own words are the record; hiding them is the attorney's call, not the tool's. | T-013 paralegal r2 M1/M2, PM r2 M3/M4 |
26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
29:| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
32:| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
33:| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
34:| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
---tail---
| D-002 | Every letter line carries a verbatim quote + provider as written + date of service (US long format) + citation placeholder `[Ex. __ / Bates __]`. No short-cite mode. | Ship bar #1 (100% grounded export); adjusters cross-check providers. | T-014 staff-eng F1, privacy B2 |
| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
| D-004 | Amounts: code extracts and classifies with explicit billing-phrase rules; judge #2 validates every classification; a rate can never become a charge; running total = accepted charges only; "detected" is shown separately and labelled not-a-total. Total line wording: "Billed charges stated in these records: $X". | Texas paid-or-incurred (§41.0105) — never "damages"; no PT total from a rate. | T-014 privacy B1; research T-008 |
| D-005 | Any record carrying an injection warning forces all its items to needs_review; its amounts can't be charges; it can't suppress flags from other records (lexicon is the floor). | Injected "$50,000" reached the total via code path alone. | T-014 privacy B1 |
| D-006 | Numbers/dates/$ in a summary or a user edit must appear in that item's excerpt (code check) or the item is needs_review with a reason. | Don't rely on the judge for swapped numerals. | T-014 staff-eng F5, privacy |
| D-007 | Flag titles/explanations are code templates; the LLM returns only category + excerpt spans. | No free LLM prose in the attorney's notes. | T-014 staff-eng F8, privacy |
| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. (Listed under "Decided by the team" in NEEDS_CHRIS.) | Candor without telling the carrier how the chronology was made. | T-014 privacy |
| D-010 | Edits: entry = summary text only; charge = accept/dismiss only (no reclassification, no amount edit); flag = reviewer note only. Ambiguous dates are resolved with a separate `confirm_date` action (choose one of the code-proposed readings), not an edit. Originals are kept; "edited" shows in UI + internal notes. | Keep code-owned facts code-owned. | T-013 PM r2 (major 1, 2) |
| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-have. | T-013 PM r2, T-014 staff-eng F12 |
| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged language may appear in the letter **only** as part of an accepted excerpt, and the internal notes list "flagged language quoted in the letter" so the attorney decides. NEEDS_CHRIS #10. | The records' own words are the record; hiding them is the attorney's call, not the tool's. | T-013 paralegal r2 M1/M2, PM r2 M3/M4 |
| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
| D-014 | Provider = the source label exactly as written in the record header; golden aliases must match header text. | Grounding (R-TL-9). | T-013 PM r2 |
| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreaker. | Part 2 area 4 asks for it; Texas Op. 705 allows confidential info in AI tools with precautions. | T-010 litigation-lead Q |
| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:34:01.967Z

**tool call — Bash**
````
{
 "command": "cat reviews/GATE-M1-summary.md 2>/dev/null | head -80; echo \"--- grep stale phrases across board cards ---\"; grep -rn -E '8,390|dismissing entry 5 gives|Either|\\$2,150 only|sample yields|rows 1-20 all mapped|or edit LLM_VS_CODE|ship_bar_met true\\)' board/cards/ | cut -c1-260",
 "description": "Read GATE-M1 summary and grep stale phrases on cards"
}
````

### User / tool · 2026-11-02T01:34:02.063Z

**tool result**
````
# GATE M1 — Research, personas, requirements, architecture — PASS (pending T-017/T-018 recheck)

Date: 2026-11-02 · Orchestrator synthesis · Budget 2.5 h; actual ≈ 3.5 h (review rounds; see D-024 response)

## Deliverables
| Card | Output | Reviews (rounds) | Outcome |
|---|---|---|---|
| T-008 domain research | research/chronology-practice.md, adjuster-attacks.md, texas-pi-notes.md, GLOSSARY (46 terms) | claims-adjuster (4) | pass; invented fact ("referral", "radicular") caught and removed |
| T-009 flag lexicon | app/llm/lexicon.yaml v2 (66 entries, D-018 shape) | legal-nurse + claims-adjuster (2) | debt → T-027 (held-out recall) |
| T-010/T-011 persona dossiers | personas/*.md (13), compiled into reviewer agents | PM + litigation-lead (3) / PM (2) | pass |
| T-012 PHI + AI supervision | research/phi-and-ai-supervision.md (19 sources) | privacy-compliance (3) | pass |
| T-013/T-025 requirements | spec/REQUIREMENTS.md (62 R-IDs), §6 export = golden | paralegal + PM (3) / PM (2) | debt closed via T-025 |
| T-014/T-028 architecture | memory/DECISIONS.md ADR-000a..017, docs/LLM_VS_CODE.md (20 rows), api.md | staff-engineer + privacy (3) / staff (2) | debt → M2 cards |
| T-015 golden set | evals/golden/ (sample + 9 synthetic, 40 hallucinations, 10 controls, export golden) | paralegal + legal-nurse (4) | accepted; check_golden.py green |
| T-016 compile agents | 13 reviewers compiled, drift test | staff-engineer | pass |
| T-017/T-018 M2/M3 plan + contract review | 20 M2/M3 cards, docs/M2M3_COVERAGE.md | PM+paralegal+staff contract review | edits applied (0 unapplied majors per reviewer's script) |
| T-026/T-047 board Office view (Chris) | 2D → 3D office with overhead kanban | ux (haiku) | pass |

## What review changed (selected)
- Flags never enter the letter (D-001); every letter line quotes the record (D-002); total line exact, no parenthetical (D-019).
- Gaps computed by code over all clinical-encounter dates (D-003); injected text can't reach totals (D-004/D-005, case_07).
- Dropped qualifiers → needs_review (D-022); hedges kept whole (D-021); provider conflicts are code (D-025).
- 26 orchestrator decisions in memory/ORCHESTRATOR_DECISIONS.md; scope cuts 1–19 + debt rows in memory/SCOPE_CUTS.md.

## Open blockers: 0. Debt: T-027 (lexicon), golden-export byte test (T-041/T-038), minors carried in card notes.
## Questions for Chris (non-blocking): NEEDS_CHRIS #1–#3 (key, demo-only vs live, eval budget).
--- grep stale phrases across board cards ---
board/cards/T-004.md:38:    - [minor] The write guard does not cover Bash, but every reviewer holds Bash and each body says 'a hook enforces this' — fix: Either add a Bash matcher to the reviewer hook that denies redirections/sed -i/tee/mv/cp/git-write outsi
board/cards/T-004.md:46:    - [major] Wrapper shells and common writers bypass both the identity rules and the shell-write rules, while the persona body says hooks enforce shell writes — fix: Either (a) recursively parse payloads of `bash|sh|zsh -c`, `eval`,
board/cards/T-014.md:46:    - [major] F3 Judge #2 does not validate code-classified amounts; deviation from 5.2 and R-CH-2 is not argued in any ADR — fix: Either run J2 on every classification (about 3 cheap calls on the sample) or add an ADR deviation: code
board/cards/T-010.md:40:    - [minor] Section 5 'dealbreakers' carry no severity, so the dossiers contradict themselves (privacy-compliance) — fix: Either rate the logging example as a blocker, or reword the red flag so it is narrower than the calibration ex
board/cards/T-010.md:66:Round 3 (commit 3f9dd58). Lit-lead r2 M1: lit-lead #19, adjuster #21, paralegal #12/#21 and lit-lead major calibration -> letter total line 'Billed charges stated in these records: $8,390 (physical therapy charges to be supplemented)' (
board/cards/T-015.md:27:  - {"n": 2, "text": "sample.expected.json encodes every Appendix C truth incl. gaps 7/7/28/14/73/11/14, total $8,390, PT rate unclear, and the must-not list", "done": true, "evidence": "sample.expected.json: gaps 7/7/28/14/73/11/14, to
board/cards/T-038.md:39:- 2026-11-02T01:22:45Z orchestrator: AC 9 added: Contract review (T-018): T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case, pooled) with R-IDs R-FL-3, R-RV-6, and state the threshold in REQUIREMENTS 
board/cards/T-018.md:34:    - [major] PM3: T-045 AC4 still requires ship_bar_met true on the default run, which T-038 AC6 makes false on fixture — fix: Replace AC4's bare '`python -m evals.run` (ship_bar_met true)' with '`LLM_BACKEND=claude-cli python -m eva
board/cards/T-018.md:36:    - [major] PM6: the lexicon-recall release gate is undecided; T-038 AC9 is an 'or' and LLM_VS_CODE still calls it a gate — fix: Choose one and record it in memory/ORCHESTRATOR_DECISIONS.md. Either add lexicon_recall_must_flags to T
board/cards/T-018.md:37:    - [major] PL2: T-039 AC2 still says dismissing entry 5 alone gives '7 of 9'; the corrected AC is appended as AC7 — fix: Replace T-039 AC2's 'dismissing entry 5 gives ... 7 of 9' in place with the AC7 wording, and delete AC7.
board/cards/T-018.md:39:    - [major] S7: the row-10 engine is still an 'Either ... or' instruction; no decision is recorded — fix: Decide and record it. Either provider-variant conflict is Code (a T-033 AC with no LLM call, row 10 unchanged), or row 10 chan
board/cards/T-018.md:40:    - [major] S9: T-039 AC1 still asserts $8,390.00 for case_07; the $420 line is appended as AC9 — fix: Replace AC1's case_07 clause in place with the AC9 wording ('on case_07 with $420 accepted it is exactly ... $420.00'), and delet
board/cards/T-039.md:18:  - {"n": 1, "text": "tests/unit/test_export.py: every letter line is heading / date+provider / summary / Source quote / amount / total; builder signature has no flags argument; total line exactly 'Billed charges stated in these records
board/cards/T-039.md:20:  - {"n": 3, "text": "tests/unit/test_review_rules.py: 422 invalid_edit matrix (entry date/provider, flag evidence/type/title, charge amount/class, non-contiguous excerpt, hedge-dropping excerpt), 422 date_invalid, 409 needs_confirm for
board/cards/T-039.md:26:  - {"n": 9, "text": "Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample 
board/cards/T-039.md:39:- 2026-11-02T01:22:47Z orchestrator: AC 9 added: Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly "Billed charges stated in these records: $420.00"; with the $185 rate 
board/cards/T-039.md:40:- 2026-11-02T01:32:26Z orchestrator: AC 1 edited: tests/unit/test_export.py: every letter line is heading / date+provider / summary / Source quote / amount / total; builder signature has no flags argument; total line exactly 'Billed cha
board/cards/T-008.md:43:    - [minor] Unlisted source cited: 'Australian PIC' — fix: Either add the PIC source with a URL and a 'non-US' label, or remove the clause and keep only what src 17 supports (impeachment with the claimant's intake forms).
board/cards/T-036.md:38:- 2026-11-02T01:22:45Z orchestrator: AC 7 added: Contract review (T-018): Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-036 depends_on and add a T-036 AC: 'runs against app/llm/lexicon.yaml at HEAD; 
board/cards/T-036.md:41:- 2026-11-02T01:22:46Z orchestrator: AC 10 added: Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the L
board/cards/T-012.md:53:    - [minor] §3.1 option 2 (remote screen share) is itself an electronic disclosure of PHI to a non-employee through a conferencing vendor; hiding name, DOB and claim number is not de-identification — fix: Either drop option 2 or co
board/cards/T-043.md:19:  - {"n": 2, "text": "charges table: Accepted $8,390 then $2,150 after dismissing ER, 'Detected, not yet accepted' labelled not a total, $185 'rate $185/visit; visit count not stated', no PT total; accepting $1,2OO keeps it in the uncle
board/cards/T-028.md:42:    - [major] Spec section 8 row 1 check cannot pass: the api.md export example abbreviates the notes block — fix: Either amend spec section 8 row 1 to 'the example names the golden file; a pytest compares real export output with it' 
board/cards/T-017.md:21:  - {"n": 2, "text": "every row of the docs/LLM_VS_CODE.md table maps to an M2 card with its validation named in AC", "done": true, "evidence": "docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names i
board/cards/T-017.md:32:- 2026-11-02T01:14:19Z orchestrator: AC 2 checked: docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval
board/cards/T-017.md:49:    - [minor] T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-1 minor, not reworded) — fix: Reword the AC2 evidence: 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.
board/cards/T-037.md:18:  - {"n": 1, "text": "`python -m app.pipeline evals/golden/sample.txt` (fixture backend) prints 9 entries, the 73-day gap flag, charges $8,390 total, all flag groups, exit 0 in under 60 s (CONTRACT M2 CLI)", "done": false, "evidence": n
board/cards/T-033.md:18:  - {"n": 1, "text": "`pytest tests/unit/test_amounts.py` green: sample yields $6,240, $185, $2,150 as charges/rate, plus 'missing 3 days of work' recorded as a damages mention (not an amount); 20 phrasings -> rate; $1,2OO and $9S.00 un
board/cards/T-033.md:19:  - {"n": 2, "text": "totals: accepted $8,390, dismiss ER -> $2,150, detected shown separately and labelled not-a-total, no PT total (golden must_not M4), duplicate $6,240 counted once; injected $50,000 in case_07 never charge (R-CH-3, 
board/cards/T-033.md:25:  - {"n": 8, "text": "Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample 
board/cards/T-033.md:35:- 2026-11-02T01:22:46Z orchestrator: AC 6 added: Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the LL
board/cards/T-033.md:37:- 2026-11-02T01:22:47Z orchestrator: AC 8 added: Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly "Billed charges stated in these records: $420.00"; with the $185 rate 
board/cards/T-033.md:38:- 2026-11-02T01:32:26Z orchestrator: AC 1 edited: `pytest tests/unit/test_amounts.py` green: sample yields $6,240, $185, $2,150 as charges/rate, plus 'missing 3 days of work' recorded as a damages mention (not an amount); 20 phrasings -
board/cards/T-013.md:71:    - [minor] Total-line parenthetical is tool-authored text in the carrier block that volunteers a weakness; the placeholder name is inconsistent — fix: Letter wording: 'Billed charges stated in these records: $8,390.00 (physical the
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:34:02.646Z

**tool call — Bash**
````
{
 "command": "for c in T-039 T-033; do echo \"=== $c\"; .venv/bin/python tools/board.py show $c | grep -n -E '^- \\[|^  - |^ac:|\"n\": ' | cut -c1-400; done",
 "description": "Show AC lines for T-039 and T-033"
}
````

### User / tool · 2026-11-02T01:34:02.834Z

**tool result**
````
=== T-039
17:ac:
18:  - {"n": 1, "text": "tests/unit/test_export.py: every letter line is heading / date+provider / summary / Source quote / amount / total; builder signature has no flags argument; total line exactly 'Billed charges stated in these records: $8,390.00' with the $185 rate non-dismissed; on case_07 with $420 accepted the line is exactly 'Billed charges stated in these records: $420.00'; same accepted
19:  - {"n": 2, "text": "test_export notes: sections in R-EX-4 order, every 'record N' followed by (provider, date), bills-to-request line exact, dismissing entry 5 and leaving entry 6 pending gives 'Record 5 ... dismissed', 'Record 6 ... not reviewed' and 7 of 9 (R-EX-4, R-EX-7)", "done": false, "evidence": null}
20:  - {"n": 3, "text": "tests/unit/test_review_rules.py: 422 invalid_edit matrix (entry date/provider, flag evidence/type/title, charge amount/class, non-contiguous excerpt, hedge-dropping excerpt), 422 date_invalid, 409 needs_confirm for +$9,000 and seeded 'herniation', keep-my-wording resend saves, judge unavailable -> JUDGE_UNAVAILABLE; accept $1,2OO -> notes 'request clean copy of bill', not 
21:  - {"n": 4, "text": "tests/e2e files written red: test_api.py, test_input.py, test_timeline.py, test_source_record.py, test_flags_panel.py, test_charges.py, test_review_matrix.py, test_keyboard_mobile.py, test_edit.py, test_export_ui.py, test_letter_isolation.py, test_ladder_gate.py, test_side_by_side.py (marked skip if the T-046 stretch is cut); `pytest tests/e2e --collect-only` lists all", "
22:  - {"n": 5, "text": "all new tests cite R-IDs in docstrings and use the fixture backend only (no key, no network)", "done": false, "evidence": null}
23:  - {"n": 6, "text": "Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirmation'.", "done": false, "evidence": null}
24:  - {"n": 7, "text": "Contract review (T-018): T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives \"Record 5 ... dismissed\", \"Record 6 ... not reviewed\" and 7 of 9'.", "done": false, "evidence": null}
25:  - {"n": 8, "text": "Contract review (T-018): T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], blocks T-034..T-037): write test_provider, test_audited, test_schemas, test_judges, test_flags_sample, test_flags_injection, test_pipeline, test_conflicts, test_flag_templates red. T-039 AC4: name test_api.py plus the 10 E2E files above, by file.", "done": false, "evidence": null}
26:  - {"n": 9, "text": "Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample line is unchanged'. T-033 AC1 append: '\"$6,240\" parses to int 624000; app/backend/amounts.py contains no float('.", "done": false, "evidence": null}
=== T-033
17:ac:
18:  - {"n": 1, "text": "`pytest tests/unit/test_amounts.py` green: sample yields $6,240, $185, $2,150 as charges/rate, plus 'missing 3 days of work' recorded as a damages mention (not an amount); 20 phrasings -> rate; $1,2OO and $9S.00 unclear/null; doses (10 mg etc.) never amounts; all golden amounts get golden class (R-CH-1, R-CH-2, R-CH-4, rows 6, 7)", "done": false, "evidence": null}
19:  - {"n": 2, "text": "totals: accepted $8,390, dismiss ER -> $2,150, detected shown separately and labelled not-a-total, no PT total (golden must_not M4), duplicate $6,240 counted once; injected $50,000 in case_07 never charge (R-CH-3, R-CH-6, R-RV-6, row 8); proved by test_amounts::test_totals", "done": false, "evidence": null}
20:  - {"n": 3, "text": "`pytest tests/unit/test_gaps.py` green: 29/30 no flag, 31 flags (case_02), sample 73 flagged and 28 not, case_09 56-day gap with billing/phone excluded, dismissing entry 6 leaves the gap unchanged (R-FL-1, D-003, row 9)", "done": false, "evidence": null}
21:  - {"n": 4, "text": "accident-date rule: sample conflict cites record 7 intake line vs records 1/2 header dates, never picks a date, no 'delay' text (R-FL-2a, D-017, row 10); proved by test_conflicts::test_accident_date", "done": false, "evidence": null}
22:  - {"n": 5, "text": "every flag title/explanation equals flag_templates output; no free-text field accepted (R-FL-8, row 14); proved by test_flag_templates::test_text_is_template", "done": false, "evidence": null}
23:  - {"n": 6, "text": "Contract review (T-018), decided by D-025: case_05 provider-name conflict is raised by code (normalized-name rule: same header provider prefix, differing names), no LLM call; tests/unit/test_conflicts.py::test_provider_names", "done": false, "evidence": null}
24:  - {"n": 7, "text": "Contract review (T-018): T-033 new AC: 'rate note numbers are code-derived: N planned from the \"Plan of care: N visits\" match in a record with the same provider prefix, M from the highest \"visit M\" in a header label; omitted when not found; test on sample and a variant (plan 10, last visit 7)'. T-033 AC1: add 'one damages mention (record 5, value null) from the lexicon
25:  - {"n": 8, "text": "Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample line is unchanged'. T-033 AC1 append: '\"$6,240\" parses to int 624000; app/backend/amounts.py contains no float('.", "done": false, "evidence": null}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:34:30.601Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/board.py show T-038 | grep -E '^  - \\{\"n\"' | cut -c1-600; echo \"=== T-045 AC4\"; .venv/bin/python tools/board.py show T-045 | grep -E '\"n\": 4' | cut -c1-500; echo \"=== T-027\"; .venv/bin/python tools/board.py show T-027 | grep -n -i -E 'priority|timebox|estimate' | cut -c1-300",
 "description": "Show T-038 ACs, T-045 AC4, and T-027 timebox"
}
````

### User / tool · 2026-11-02T01:34:30.853Z

**tool result**
````
  - {"n": 1, "text": "`python -m evals.run` writes evals/reports/latest.json and a timestamped .md; `jq '.ship_bar_met, .metrics | keys' evals/reports/latest.json` shows ship_bar_met plus grounding_rate, entry_recall, amount_recall, flag_precision[type], flag_recall[type], hallucination_catch_rate, unsupported_count_3run, determinism_3run, each with its R-ID and gap_28_not_flagged / gap_73_flagged", "done": false, "evidence": null}
  - {"n": 2, "text": "spec-vs-golden check: `python -m evals.run --check-spec` compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt LETTER_TEXT/INTERNAL_NOTES_TEXT and writes spec_matches_golden to latest.json; changing one character in a temp copy makes it false (tests/unit/test_eval_spec_check.py)", "done": false, "evidence": null}
  - {"n": 3, "text": "hallucination_catch_rate >= 0.95 computed as a rate over every line of hallucinations.jsonl (today 40) and no control in hallucinations_controls.jsonl returns unsupported (R-TL-4, ship bar 4)", "done": false, "evidence": null}
  - {"n": 4, "text": "determinism_3run measured only on a live backend (claude-cli or anthropic-api): 3 runs on sample, code outputs identical, same states and same flag set = 1.0; on fixture the field is null/not_measured and cannot satisfy ship_bar_met (R-CO-7)", "done": false, "evidence": null}
  - {"n": 5, "text": "ship_bar_met is false when any bar is missed (test with a tampered report), golden must_not hits are counted (R-CO-3), and case_07 total stays $420 (R-RV-6); proved by tests/unit/test_eval_runner.py", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.", "done": false, "evidence": null}
  - {"n": 8, "text": "Contract review (T-018): Add a 'Ship bar row -> card' table to M2M3_COVERAGE.md (rows 1-4 -> T-038, row 5 -> T-045 + M3 gate). New orchestrator card (M3): 'paralegal-reviewer agent body and M3 gate brief request scores.verify_quickly 1-5 (D-015)'.", "done": false, "evidence": null}
  - {"n": 9, "text": "latest.json reports lexicon_recall_must_flags (pre_existing + causation, per golden case and pooled; R-FL-3, R-RV-6). Per D-026 it is reported, not gated; ship_bar_met is unaffected", "done": false, "evidence": null}
=== T-045 AC4
  - {"n": 4, "text": "sensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `LLM_BACKEND=claude-cli python -m evals.run` (ship_bar_met true on the live backend; the fixture run reports not_measured for live-only metrics), `python tools/check_secrets.py` exit 0, e2e green", "done": false, "evidence": null}
=== T-027
7:priority: "P0"
25:Estimate: 40 min (timebox).
28:- 2026-11-02T01:22:47Z orchestrator: updated priority=P0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:34:32.149Z

**tool call — Bash**
````
{
 "command": "echo \"=== estimates per card\"; for f in board/cards/T-0{27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48}.md; do n=$(grep -c -i -E 'estimate|timebox' \"$f\"); echo \"$(basename $f) $n\"; done | tr '\\n' ' '; echo; echo \"=== trigger/total/budget words in coverage doc\"; grep -n -i -E 'trigger|total|budget|3\\.5|hour|\\bh\\b' docs/M2M3_COVERAGE.md; echo \"=== T-036 AC list\"; .venv/bin/python tools/board.py show T-036 | grep -E '\"n\": (3|7|10)' | cut -c1-420; echo \"=== T-018 AC2 evidence cites\"; .venv/bin/python tools/board.py show T-018 | grep -n '\"n\": 2' | cut -c1-300",
 "description": "Check estimates, coverage-doc budget and trigger words, T-036 ACs"
}
````

### User / tool · 2026-11-02T01:34:32.507Z

**tool result**
````
=== estimates per card
T-027.md 1 T-029.md 2 T-030.md 1 T-031.md 3 T-032.md 1 T-033.md 1 T-034.md 3 T-035.md 1 T-036.md 4 T-037.md 1 T-038.md 1 T-039.md 2 T-040.md 1 T-041.md 1 T-042.md 1 T-043.md 1 T-044.md 1 T-045.md 1 T-046.md 2 T-048.md 1 
=== trigger/total/budget words in coverage doc
95:| 8 | Running total | T-033 (m2-be-amounts-gaps), T-041 (m3-be-export), T-043 (m3-fe-flags-charges-review) |
=== T-036 AC list
  - {"n": 3, "text": "only one of LLM/lexicon fires -> needs_review with LEXICON_ONLY or LLM_ONLY; case_06 28-day near-miss does not flag; case_05 provider-name conflict raised and name variants tolerated (R-FL-3, R-FL-2)", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033); the LLM conflict pass covers semantic conflicts only; exactly one accident-date conflict flag on the sample", "done": false, "evidence": null}
  - {"n": 10, "text": "Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033); the LLM conflict pass covers semantic conflicts only; exactly one accident-date conflict flag on the sample", "done": false, "evidence": null}
=== T-018 AC2 evidence cites
20:  - {"n": 2, "text": "every blocker/major finding is applied as an AC edit/new card or rejected with a recorded reason in reviews/GATE-M1-summary.md", "done": true, "evidence": "every blocker/major applied as AC edit/new card (artifacts/tmp/contract_fixes.json); verified by reviews/T-018-product-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:34:48.795Z

**tool call — Bash**
````
{
 "command": "grep -n -E '^\\| R-(RV-8|CO-9|EX-4|FL-2|CH-3|TL-2|EX-8|FL-1|IN-5|RV-6) ' spec/REQUIREMENTS.md | cut -c1-500; echo; grep -n -E '^\\| ID|^\\| R-ID|^\\| Req' spec/REQUIREMENTS.md | head; echo \"=== 3.5 budget source\"; grep -rn -E '3\\.5 ?h' docs/ memory/ spec/ 2>/dev/null | head -5",
 "description": "Inspect REQUIREMENTS test rows for sampled R-IDs and budget source"
}
````

### User / tool · 2026-11-02T01:34:48.896Z

**tool result**
````
40:| R-IN-5 | **Dates to confirm.** An entry with an ambiguous date is excluded from ordering and gap math, shown in a "Dates to confirm" group placed after the timeline (a `record_warning`), and is `needs_review`. She resolves it with the `confirm_date` action (R-RV-2), choosing one of the code-proposed readings. An undated entry sits in the same group with "no date found"; this build offers no way to type one in. | `case_01` record 8: absent from the timeline order until confirmed; after `conf
49:| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/flag evidence and the excerpt-edit UI): the text up to and including a terminator, where a terminator is `.`, `?` or `!` followed by whitespace and then an uppercase letter, digit or end of text; `;`; or a line break. A per
65:| R-FL-1 | **Treatment gap.** Flag when days between consecutive dates of service across all providers (A-102) is **greater than 30** (A-104). Only clinical-encounter records count (D-003): billing statements and phone notes are excluded. Evidence is the two bounding entries (date, provider, excerpt). | Sample: flag 2026-03-06 → 2026-05-18, 73 days, citing entries 6 and 7. No flag on 2026-01-23 → 2026-02-20 (28 days). `case_02_gap_boundaries`: 29 and 30 do not flag, 31 does (3 flags, 4 ne
66:| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**, with the records cited (R-EX-4) and no choice made between the dates or any "delay from the accident" computed; the tool may state "first recorded treatment: January 9, 2026" (D-017); (b) PT plan of 12 visits (record 4) vs discharge a
80:| R-CH-3 | **The total counts only accepted amounts of class `charge`.** The screen shows "Accepted charges: $X" and, separately, "Detected, not yet accepted: $Y (not a total)". Rates, estimates, damages and unclear amounts are listed as "unclear — not totaled" and never added. | Sample: after accepting both charges, Accepted = **$8,390**. Dismissing the ER charge drops it to $2,150. $185 reads "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review". **No
97:| R-RV-6 | **No LLM output is auto-accepted. Record text is data (D-005).** A record with an injection warning forces all its items to `needs_review` (an advisory state, ADR-008), its amounts can't be charges, and it can't suppress flags from other records (the lexicon is the floor; the prior/causation flag pass runs per record, D-021). | Golden `case_07_prompt_injection`: the record produces an ordinary entry with an `INJECTION_SUSPECTED` warning, `needs_review`; no item's `review_status` ch
98:| R-RV-8 | **Decisions survive a reload.** Accept, edit, dismiss, notes and `confirm_date` persist (SQLite) and restore on reload or reopen of the case. | E2E: accept 3 items, edit 1, reload → same statuses and the same Accepted total. | E2E |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) *
126:| R-EX-8 | **The total line is exactly** `Billed charges stated in these records: $X` (D-019), where X is the sum of accepted `charge` amounts, formatted `$8,390.00`. **No parenthetical and no "excludes …" clause, ever.** Rates, estimates, unclear amounts, exclusions and injection-tagged amounts appear only in the internal notes ("Amounts not totaled"), because any clause built from unaccepted or injected amounts would leak into the carrier letter. | UT: on the sample the line equals `Bill
143:| R-CO-9 | Retries: at most 2 retries (3 attempts in all), each with changed conditions; failure is visible. | UT: the call fails on all 3 attempts → `LLM_FAILED_AFTER_RETRIES` and the item shows "could not process" with the reason, and the app stays usable; fails twice then succeeds → the entry is produced. | UT |

34:| ID | Requirement | Pass / fail test | Checker |
46:| ID | Requirement | Pass / fail test | Checker |
63:| ID | Requirement | Pass / fail test | Checker |
76:| ID | Requirement | Pass / fail test | Checker |
90:| ID | Requirement | Pass / fail test | Checker |
117:| ID | Requirement | Pass / fail test | Checker |
133:| ID | Requirement | Pass / fail test | Checker |
149:| ID | Requirement | Pass / fail test | Checker |
175:| ID | Requirement | Pass / fail test | Checker |
=== 3.5 budget source
docs/CONTRACT.md:300:### M2 — Core pipeline + evals green (≤ 3.5 h)
docs/CONTRACT.md:306:### M3 — Review UI, export, E2E (≤ 3.5 h)
spec/REQUIREMENTS.md:171:- **Start** only when every M3 must-have card is done with no open blockers, and M3 is inside its 3.5 h budget. The stretch is built before the M3 gate so the gate reviews it.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:35:01.142Z

**tool call — Bash**
````
{
 "command": "grep -rn -E 'of 9|7 of 9|8 of 9' spec/REQUIREMENTS.md evals/golden/ 2>/dev/null | cut -c1-300; echo \"=== case_07 total\"; grep -rn -E 'Total \\$|\\$420' evals/golden/README.md | cut -c1-240; echo \"=== T-038 AC2 is spec-vs-golden only (confirmed above); any AC anywhere that diffs AC numbers vs golden?\"; grep -rln -E 'AC numbers|every number in an AC|self-check' board/cards/ | head; echo \"=== coverage self-check claim\"; sed -n '19,20p' docs/M2M3_COVERAGE.md",
 "description": "Verify 7 of 9 and case_07 golden values and self-check control"
}
````

### User / tool · 2026-11-02T01:35:01.253Z

**tool result**
````
spec/REQUIREMENTS.md:123:| R-EX-5 | The UI shows counts outside the copied text: "N entries, N charges in letter · N flags in internal notes · N of 9 records in letter · N items pending (N flags)". The count line is part of neither block. **Copy asks for one confirmation when anything is pending*
spec/REQUIREMENTS.md:125:| R-EX-7 | **Reconciliation.** Every input record not represented in the letter is listed in the internal notes with its reason: rejected, dismissed or not reviewed. The UI shows "N of 9 records in letter" before copy. | E2E: dismiss entry 5 and leave entry 6 pending → not
spec/REQUIREMENTS.md:306:- none (9 of 9 records included)
evals/golden/sample.export.expected.txt:84:- none (9 of 9 records included)
evals/golden/case_03_rate_and_ocr.expected.json:207:      "note": "OCR noise (letter S). Value stays null; a suggestion of 95 is allowed only as an unconfirmed hint."
=== case_07 total
evals/golden/README.md:132:**case_01** (2026): 02-03→02-17: 14; 02-17→02-24: 7; 02-24→03-03: 4 (to Feb 28) + 3 = 7; 03-03→03-10: 7; 03-10→03-17: 7; 03-17→03-25: 8. Record 8 (phone note, `04/05/2026`, April 5 or May 4) is exclude
evals/golden/README.md:144:**case_07**: 03-02→03-09: 7; 03-09→03-16: 7; 03-16→05-04: 15 (to Mar 31) + 30 (Apr) + 4 = **49** flag. Total $420; $50,000 never totaled (no 50,420).
=== T-038 AC2 is spec-vs-golden only (confirmed above); any AC anywhere that diffs AC numbers vs golden?
board/cards/T-027.md
board/cards/T-017.md
=== coverage self-check claim
## Plan self-check
Pass conditions live in each card's AC on the board (each names its test/eval/command); this table maps ownership. Numbers in AC are checked against the golden set by T-038 (`--check-spec`) and the qa test-first cards (T-029, T-048, T-039).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:35:03.298Z

**tool call — Bash**
````
{
 "command": "sed -n '125p' spec/REQUIREMENTS.md; echo; grep -n -i -E 'self-check|AC numbers' board/cards/T-027.md | cut -c1-300",
 "description": "Read full R-EX-7 test row and self-check mentions on T-027"
}
````

### User / tool · 2026-11-02T01:35:03.385Z

**tool result**
````
| R-EX-7 | **Reconciliation.** Every input record not represented in the letter is listed in the internal notes with its reason: rejected, dismissed or not reviewed. The UI shows "N of 9 records in letter" before copy. | E2E: dismiss entry 5 and leave entry 6 pending → notes list record 5 (dismissed) and record 6 (not reviewed); the on-screen count reads "7 of 9". | E2E |

20:  - {"n": 3, "text": "Category names match the ADR-013 closed list; self-check counts low-only hits as non-flags", "done": false, "evidence": null}
23:Debt from T-009 (reviews/T-009-legal-nurse-r2.md majors 1-5). The probe sets were copied into the lexicon examples, so the self-check measures memorization. Fix the patterns rather than the examples, and score on a held-out set.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:35:14.942Z

**tool call — Bash**
````
{
 "command": "for c in T-031 T-040 T-043 T-044 T-042 T-041 T-039; do echo \"=== $c\"; .venv/bin/python tools/board.py show $c | grep -E '^  - \\{\"n\"' | grep -i -E 'reload|could not process|EDITED|two dates|2026-01-19|not merged|RECORDS NOT IN|edit' | cut -c1-260; done",
 "description": "Find ACs on likely owner cards that carry R-ID pass conditions"
}
````

### User / tool · 2026-11-02T01:35:15.373Z

**tool result**
````
=== T-031
  - {"n": 4, "text": "review_status and edits (originals kept) persist across a new connection (R-RV-8); proved by test_db::test_review_status_roundtrip", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": false, "evidence": null}
=== T-040
  - {"n": 1, "text": "`pytest tests/unit/test_review_rules.py` green: 422 invalid_edit matrix, 409 needs_confirm then keep-my-wording, JUDGE_UNAVAILABLE, charges accept/dismiss/reset only (R-RV-2, R-RV-3, R-CH-7, R-RV-5, row 15 for edits)", "done": false, "evi
=== T-043
  - {"n": 3, "text": "review matrix {accept, edit-note, dismiss} x flag, {accept, dismiss} x charge, entry accept/dismiss; fresh load all pending; dismiss -> reset -> dismiss; reload restores statuses and total (R-RV-1, R-RV-5, R-RV-8); proved by test_review_m
  - {"n": 4, "text": "keyboard-only completion (accept/edit/dismiss/next) and 375 px with no horizontal scroll and every action reachable (R-RV-4); proved by test_keyboard_mobile.py", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-043 AC1 append: 'the accident-date conflict card shows \"Date of accident per intake form: 2026-01-19.\" and the 2026-01-09 header line(s) of records 1 and 2 side by side, and contains none of \"resolved\", \"co
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": false, "evidence": null}
=== T-044
  - {"n": 1, "text": "edit entry 3 summary -> 'edited' label in UI; letter shows new summary and citation with no 'edited' mark; adding '$9,000' shows the 409 reasons and 'keep my wording' (R-RV-2, R-RV-3); proved by tests/e2e/test_edit.py", "done": false, "ev
  - {"n": 2, "text": "excerpt re-selection lists sentence units of the same record only; dropping a hedge unit shows the invalid_edit message (R-RV-2, R-TL-8); proved by test_edit.py::test_excerpt_units", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with e
=== T-042
  - {"n": 6, "text": "Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECO
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": false, "evidence": null}
=== T-041
  - {"n": 6, "text": "Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECO
=== T-039
  - {"n": 3, "text": "tests/unit/test_review_rules.py: 422 invalid_edit matrix (entry date/provider, flag evidence/type/title, charge amount/class, non-contiguous excerpt, hedge-dropping excerpt), 422 date_invalid, 409 needs_confirm for +$9,000 and seeded 'her
  - {"n": 4, "text": "tests/e2e files written red: test_api.py, test_input.py, test_timeline.py, test_source_record.py, test_flags_panel.py, test_charges.py, test_review_matrix.py, test_keyboard_mobile.py, test_edit.py, test_export_ui.py, test_letter_isolation
  - {"n": 6, "text": "Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with e
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:35:36.164Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/board.py show T-045 | grep -n -E 'verify_quickly|paralegal' | cut -c1-400; echo \"=== T-034 AC7 and T-046 AC5\"; .venv/bin/python tools/board.py show T-034 | grep -E '\"n\": 7' | cut -c1-300; echo \"=== coverage lines 41,62,67,81 (R-ID rows named in finding)\"; sed -n '41p;62p;67p;81p' docs/M2M3_COVERAGE.md; echo \"=== agent body\"; grep -n 'verify_quickly' .claude/agents/paralegal-reviewer.md | cut -c1-200",
 "description": "Verify verify_quickly on M3 card and cited coverage rows"
}
````

### User / tool · 2026-11-02T01:35:36.368Z

**tool result**
````
3:title: "Playwright E2E: full paralegal journey, adversarial inputs, all sensors"
24:  - {"n": 7, "text": "M3 gate: the paralegal-reviewer completes the sample case in the running app and its review JSON has scores.verify_quickly >= 4 (D-015, ship bar 5)", "done": false, "evidence": null}
37:- 2026-11-02T01:32:26Z orchestrator: AC 7 added: M3 gate: the paralegal-reviewer completes the sample case in the running app and its review JSON has scores.verify_quickly >= 4 (D-015, ship bar 5)
=== T-034 AC7 and T-046 AC5
  - {"n": 7, "text": "Contract review (T-018): T-034 AC4 append: 'anthropic-api client is constructed with max_retries=0 and an explicit timeout (<= 120 s); test_provider::test_sdk_no_internal_retry asserts both on the constructed client'.", "done": false, "evidence": null}
=== coverage lines 41,62,67,81 (R-ID rows named in finding)
| R-FL-2 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
| R-RV-8 | T-031 (m2-db-schema), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
| R-EX-4 | T-041 (m3-be-export) |
| R-CO-9 | T-034 (m2-be-provider-fixtures) |
=== agent body
111:**Ship-bar score (D-015):** whenever you review the running app, your review JSON must include `scores.verify_quickly` (1–5): "I could verify every claim quickly." ≥ 4 is the ship bar.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:36:27.310Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-017-r3-owner-probe.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-017 r3 owner probe (product-manager-reviewer).\n\nFor each R-ID whose REQUIREMENTS pass condition was named in round-1 finding 1,\nlist the board cards whose AC text carries the pass-condition phrase, and check\nwhether at least one of them is in the R-ID's row of docs/M2M3_COVERAGE.md.\nRead-only: calls `tools/board.py show` and reads the coverage doc.\n\nUsage: .venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project\n\"\"\"\nimport re\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nroot = Path(sys.argv[1]).resolve()\npy = sys.executable\ncards = [f\"T-0{n:02d}\" for n in range(27, 49)]\n\n# AC text per card (only AC lines, i.e. lines starting with '  - {\"n\":')\nac_lines = {}\nfor c in cards:\n    out = subprocess.run([py, str(root / \"tools/board.py\"), \"show\", c],\n                         capture_output=True, text=True, cwd=root).stdout\n    ac_lines[c] = [l for l in out.splitlines() if l.startswith('  - {\"n\"')]\n\n# coverage rows\ncov = (root / \"docs/M2M3_COVERAGE.md\").read_text(encoding=\"utf-8\").splitlines()\nrows = {}\nfor line in cov:\n    m = re.match(r\"^\\| (R-[A-Z]{2}-\\d+)(?:\\(\\w\\))? \\|(.*)\\|\\s*$\", line)\n    if m and m.group(1) not in rows:\n        rows[m.group(1)] = set(re.findall(r\"T-0\\d\\d\", m.group(2)))\n\n# (R-ID, [phrases that must all appear in one AC line])\nchecks = [\n    (\"R-FL-2\", [\"2026-01-19\"]),\n    (\"R-CO-9\", [\"could not process\"]),\n    (\"R-EX-4\", [\"EDITED ITEMS\"]),\n    (\"R-RV-8\", [\"reload\", \"edit\"]),\n]\n\nfail = 0\nfor rid, phrases in checks:\n    owners = sorted({c for c in cards for l in ac_lines[c]\n                     if all(p in l for p in phrases)})\n    mapped = rows.get(rid, set())\n    hit = sorted(set(owners) & mapped)\n    unmapped = sorted(set(owners) - mapped)\n    status = \"PASS\" if hit else \"FAIL\"\n    if not hit:\n        fail += 1\n    print(f\"[{status}] {rid} row={sorted(mapped)} ac_owners={owners} \"\n          f\"mapped_owners={hit} owners_missing_from_row={unmapped}\")\n\nprint(f\"RESULT: {len(checks) - fail} of {len(checks)} R-IDs have a mapped owner carrying the pass condition\")\n"
}
````

### User / tool · 2026-11-02T01:36:27.405Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-017-r3-owner-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:36:28.976Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project | tee artifacts/review-evidence/T-017-r3-owner-probe.out.txt; echo \"=== T-027 description\"; .venv/bin/python tools/board.py show T-027 | sed -n '18,27p' | cut -c1-300",
 "description": "Run owner probe for four named R-IDs and read T-027 description"
}
````

### User / tool · 2026-11-02T01:36:30.292Z

**tool result**
````
[FAIL] R-FL-2 row=['T-033', 'T-036'] ac_owners=['T-043'] mapped_owners=[] owners_missing_from_row=['T-043']
[FAIL] R-CO-9 row=['T-034'] ac_owners=['T-041', 'T-042'] mapped_owners=[] owners_missing_from_row=['T-041', 'T-042']
[FAIL] R-EX-4 row=['T-041'] ac_owners=['T-039', 'T-044'] mapped_owners=[] owners_missing_from_row=['T-039', 'T-044']
[PASS] R-RV-8 row=['T-031', 'T-040', 'T-043'] ac_owners=['T-039', 'T-043', 'T-044', 'T-045'] mapped_owners=['T-043'] owners_missing_from_row=['T-039', 'T-044', 'T-045']
RESULT: 1 of 4 R-IDs have a mapped owner carrying the pass condition
=== T-027 description
  - {"n": 1, "text": "A held-out probe set (>=40 sentences, never copied into lexicon.yaml) lives in evals/ and the lexicon scores >=85% on it", "done": false, "evidence": null}
  - {"n": 2, "text": "Covers spinal levels and 'since <year>' in prior history, the hedges (may be degenerative/post-traumatic, favors, probable, uncertain chronicity), 'attributes/relates ... to'; no high pre_existing flag on post-accident wording", "done": false, "evidence": null}
  - {"n": 3, "text": "Category names match the ADR-013 closed list; self-check counts low-only hits as non-flags", "done": false, "evidence": null}
---
## Description
Debt from T-009 (reviews/T-009-legal-nurse-r2.md majors 1-5). The probe sets were copied into the lexicon examples, so the self-check measures memorization. Fix the patterns rather than the examples, and score on a held-out set.

Estimate: 40 min (timebox).

## Notes (append-only, newest last)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:37:11.461Z

**tool call — Bash**
````
{
 "command": "echo \"--- pass-condition decision records:\"; grep -n -i -E 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md; echo \"exit=$? (1 = no match)\"; echo \"--- AC-number self-check owners:\"; grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/ spec/REQUIREMENTS.md docs/CONTRACT.md | cut -c1-160; echo \"--- T-038 AC2 text:\"; .venv/bin/python tools/board.py show T-038 | grep -E '\"n\": 2' | cut -c1-200",
 "description": "Check for recorded pass-condition decision and self-check owner"
}
````

### User / tool · 2026-11-02T01:37:11.619Z

**tool result**
````
--- pass-condition decision records:
exit=1 (1 = no match)
--- AC-number self-check owners:
board/cards/T-017.md:37:    - [major] Three AC contradict the golden or REQUIREMENTS, so they can't pass on a correct build — fix: Apply the exact edits in re
board/cards/T-017.md:46:    - [major] Round-1 major 2 not applied: three ACs still contradict golden or REQUIREMENTS in place; no plan self-check — fix: Edit 
--- T-038 AC2 text:
  - {"n": 2, "text": "spec-vs-golden check: `python -m evals.run --check-spec` compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt LETTER_TEXT/INTERNAL_NOTES_TEX
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:37:37.610Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md",
 "content": "# T-018 round-2 apply-check: contract-review findings (product-manager-reviewer)\n\n**Verdict: changes.** 0 blockers, 2 majors, 3 minors.\n\nThe applied-check script (`artifacts/review-evidence/T-018-r2-applied-check.py`, re-run to `T-018-r3-applied-check.out.txt`) reports 15 distinct NOT-APPLIED lines. `grep -c NOT-APPLIED` prints 30 because the MINORS block and the SUMMARY block each list the same 15. All 15 are minors, so the script's own pass rule holds. Two things the script does not test keep this from passing:\n\n1. PM1 has three parts. The script checks the stale-text removal and the per-card estimates. It does not check the total and the cut trigger, and those are missing (F1).\n2. T-018 AC2 is still ticked on the superseded verdict (F2).\n\nI also do not accept the script's APPLIED on T17-1a and T17-2a. Those checks match a sentence, not the column or the AC control the round-1 finding asked for. The T-017 r3 review (`reviews/T-017-product-manager-r3.md`) records them.\n\n## Status of the round-1 contract majors (CONTRACT-M2M3-product-manager, -paralegal, -staff-engineer)\n\n| Major | Status | Evidence (checked by me, not only by the script) |\n|---|---|---|\n| PM1 critical path, estimates, cut order | PARTIAL | Stale 5-card path and \"4 h\" line gone (`docs/M2M3_COVERAGE.md:4-5`). 20 of 20 cards have an estimate line. No total and no cut trigger (F1). |\n| PM2 T-027 P0 + timebox | APPLIED | `board.py show T-027`: priority \"P0\"; \"Estimate: 40 min (timebox).\" (no stop action, minor F3) |\n| PM3 fixture cannot ship | APPLIED | T-038 AC4 (determinism null on fixture), AC5; T-045 AC4 now `LLM_BACKEND=claude-cli python -m evals.run` |\n| PM4 regression freshness | APPLIED | T-038 AC7 `--check-fresh` and sha256 of prompts |\n| PM5 verify_quickly owner | APPLIED | T-045 AC7 \"M3 gate: ... scores.verify_quickly >= 4 (D-015, ship bar 5)\" |\n| PM6 lexicon recall gate | APPLIED | D-026 (`memory/ORCHESTRATOR_DECISIONS.md:34`) \"reported, not gated\"; T-038 AC9 \"Per D-026 it is reported, not gated\"; no \"or\" left. Needs Chris to confirm (question below). |\n| PL1 edits survive reload | APPLIED | T-044 AC6 \"EDITED ITEMS with original and new text\"; T-039 AC6 |\n| PL2 \"7 of 9\" reconciliation | APPLIED | T-039 AC2 in place: \"dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9\" (matches `spec/REQUIREMENTS.md:125` R-EX-7) |\n| PL3 accident date as two dates | APPLIED | T-043 AC6 \"Date of accident per intake form: 2026-01-19.\" |\n| PL4 record 4 visible as failed | APPLIED | T-042 AC6 \"could not process\" in the tray; T-041 AC6 RECORDS NOT IN THE TREATMENT SECTION |\n| S1 qa author for test files | APPLIED | Probe `qa:NONE count = 0` (applied-check out.txt lines 2-37); T-048 AC1 names 9 files; T-039 AC4 names the E2E files |\n| S2 depends_on | APPLIED | T-031 ['T-029']; T-042 ['T-039']; T-043 ['T-039','T-040','T-042'] |\n| S3 SDK hidden retries | APPLIED | T-034 AC7 `max_retries=0` and timeout |\n| S4 fixture-miss behaviour | APPLIED | T-034 AC8 FixtureMissing; T-037 AC7 \"0 FixtureMissing\" |\n| S5 judges #2-4 error path | APPLIED | T-035 AC7 JUDGE_UNSURE/JUDGE_UNAVAILABLE; T-036 AC9 |\n| S6 boundary module list | APPLIED | T-029 AC7 \"conflicts (accident date), flag_templates, injection scan\" |\n| S7 row-10 engine | APPLIED | D-025 (`memory/ORCHESTRATOR_DECISIONS.md:33`) code; T-033 AC6 \"decided by D-025\"; `docs/M2M3_COVERAGE.md:97` and `docs/LLM_VS_CODE.md:38` both say Code |\n| S8 rate note by code, damages mention | APPLIED | T-033 AC7 \"rate note numbers are code-derived\" |\n| S9 case_07 total | APPLIED | T-039 AC1 in place: \"on case_07 with $420 accepted ... $420.00\"; no \"$8,390 incl. case_07\" left (grep) |\n| N1 (round 2) T-018 AC2 ticked on refuted claim | NOT APPLIED | F2 |\n\n## Findings\n\n**F1 (major). The M2 critical path has no total against the 3.5 h budget and no cut trigger.**\n- Evidence: `docs/M2M3_COVERAGE.md:4` \"Estimates ~30–45 min each with 4 workers in parallel\"; `:5` lists cut levers with no trigger. `grep -n -i -E 'trigger|budget|3\\.5' docs/M2M3_COVERAGE.md` prints nothing. `docs/CONTRACT.md:300` \"### M2 — Core pipeline + evals green (≤ 3.5 h)\". Seven serial cards at 30–45 min is 3.5 to 5.25 h.\n- Why it matters: the round-1 fix had three parts. Two are done. The third (state the total and the cut trigger) is not, so at the low estimate the chain uses the whole M2 budget, at the high estimate it overruns, and nothing says when cut (1) or (2) is pulled.\n- Fix: add one sentence under `:4`: \"Serial chain = 7 × 30–45 min = 3.5–5.25 h against the 3.5 h M2 budget; if T-035 or T-036 is not green by estimate + N min, pull cut (1), then (2).\" N is the orchestrator's call.\n- Acceptance test: `grep -n -i 'trigger' docs/M2M3_COVERAGE.md` returns a line that holds the chain total in hours and a minute threshold.\n\n**F2 (major). T-018 AC2 is done on evidence that cites the superseded verdict.**\n- Evidence: `.venv/bin/python tools/board.py show T-018`: AC2 `\"done\": true`, evidence \"every blocker/major applied ... verified by reviews/T-018-product-manager.md\". That file's JSON verdict is `\"changes\"`.\n- Why it matters: the claim is closer to true now (the script finds 0 unapplied majors), but the gate reads the cited file and finds the opposite. Round 2 raised this as N1 (major). F1 is still open, so AC2 cannot be verified yet.\n- Fix: set T-018 AC2 `done: false` until F1 closes. Then change the evidence to cite this review's file, `reviews/T-018-product-manager-r2.md`, once its JSON verdict is `pass`.\n- Acceptance test: `board.py show T-018` shows AC2 `done: false`, or its evidence names a review file whose JSON verdict is `pass`.\n\n**F3 (minor, not gating). T-027 timebox has no stop action.**\n- Evidence: `board.py show T-027` Description: \"Estimate: 40 min (timebox).\" and nothing after it. The round-1 fix asked for \"at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md\".\n- Fix: add to the T-027 Description: \"At 40 min, stop; held-out recall is reported, not gated (D-026); log the gap in memory/SCOPE_CUTS.md.\"\n- Acceptance test: `board.py show T-027` Description contains \"SCOPE_CUTS\" and \"reported, not gated\".\n\n**F4 (minor, not gating). Fifteen round-1 minors are still unapplied.**\n- Evidence: `artifacts/review-evidence/T-018-r3-applied-check.out.txt` lines 164-193: m-PM1a, m-PM1b, m-PM1c, m-PM2, m-PL1, m-PL2, m-PL3a, m-PL3b, m-PL4, m-S1, m-S2a, m-S2b, m-S3, m-S4, m-T17.\n- Why it matters: each is a check a worker can tick without proving the failure it names (cut clock, the xfail for red tests, judge input isolation, the verifier mutation guard, the network guard, the charge highlight, the banner record). None of them gates, but each is a test that would miss its failure.\n- Fix: apply each as an in-place AC edit, or record a deferral in `memory/SCOPE_CUTS.md`.\n- Acceptance test: re-run `T-018-r2-applied-check.py`; its NOT-APPLIED count is 0, or each unapplied item has a SCOPE_CUTS row.\n\n**F5 (minor, not gating). Instruction ACs are copied across cards; T-036 has two identical ACs.**\n- Evidence: applied-check out.txt lines 195-205 (INFO: 10 distinct texts on 2-3 cards each, e.g. ['T-031','T-034','T-036'] \"Rewrite M2M3_COVERAGE.md ...\"). `board.py show T-036`: AC7 and AC10 both read \"Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033) ...\".\n- Why it matters: three workers tick copies of one instruction and nobody owns the result. The duplicate on T-036 is appended text, so a reader cannot tell which AC is the contract.\n- Fix: keep one owner for the coverage-doc rewrite (the orchestrator, T-017/T-018) and delete the copies on T-031, T-034 and T-036. Delete the duplicate T-036 AC10.\n- Acceptance test: the applied-check INFO line shows no 'Contract review (T-018):' text on more than one card, and `board.py show T-036` has one D-025 AC.\n\n## Things that landed and should not break\n- The lexicon gate and the row-10 engine are decided and recorded (D-025, D-026), and no \"or\" alternative is left on T-033 AC6 or T-038 AC9.\n- The fixture cannot ship: T-038 AC4/AC5 and T-045 AC4 name the live backend, and T-045 AC7 gives the M3 gate its verify_quickly key.\n- The qa owner gap is closed (probe `qa:NONE count = 0`; T-048 owns the nine LLM-stage test files).\n\n## Exercised\n- Read `personas/product-manager.md`, the memory index and its files, and the three prior reviews (`reviews/T-018-product-manager.md`, `reviews/T-017-product-manager.md`, `reviews/T-017-product-manager-r2.md`).\n- `.venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py . > artifacts/review-evidence/T-018-r3-applied-check.out.txt`; exit 0. `grep -c NOT-APPLIED` returned 30. Summary line 208: `checks: 68 applied=53 not-applied=15`. All 15 are minors (lines 209-223 list them).\n- `.venv/bin/python tools/board.py validate` returned `ok (48 file(s))`.\n- `board.py show` on T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-045. Grep over `board/cards/` for \"8,390\", \"dismissing entry 5 gives\", \"Either\", \"$2,150 only\", \"rows 1-20 all mapped\", \"or edit LLM_VS_CODE\".\n- `cat -n docs/M2M3_COVERAGE.md`; grep for trigger/budget/3.5 (no hits).\n- `docs/LLM_VS_CODE.md` rows 10, 12, 16 (lines 38, 40, 44); `spec/REQUIREMENTS.md` section 7 (lines 319-331) and R-EX-7 (line 125); `docs/CONTRACT.md:300`; `memory/ORCHESTRATOR_DECISIONS.md:33-34` (D-025, D-026).\n- Estimate-line count on 20 cards (all ≥ 1); `evals/golden/README.md:144` ($420 for case_07).\n- Not run: no app, no eval run (contract review of the plan, no code exists).\n\n```json\n{\"card\": \"T-018\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Round-2 apply-check of the T-018 contract review: reviews/CONTRACT-M2M3-product-manager.md (6 majors, 3 minors, 1 nit), CONTRACT-M2M3-paralegal.md (4 majors, 4 minors), CONTRACT-M2M3-staff-engineer.md (9 majors, 4 minors) against the board working tree (T-017, T-018, T-027, T-029..T-046, T-048), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, memory/ORCHESTRATOR_DECISIONS.md (D-025, D-026), spec/REQUIREMENTS.md section 7, docs/CONTRACT.md. No app code exists; no eval run.\",\n \"exercised\": [\n  \"read personas/product-manager.md in full; memory index and all memory files; reviews/T-018-product-manager.md, reviews/T-017-product-manager.md, reviews/T-017-product-manager-r2.md\",\n  \".venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py . > artifacts/review-evidence/T-018-r3-applied-check.out.txt (exit 0); grep -c NOT-APPLIED = 30 (15 distinct lines, all minors, printed twice); summary 'checks: 68 applied=53 not-applied=15'\",\n  \".venv/bin/python tools/board.py validate -> ok (48 file(s))\",\n  \"board.py show T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-045; grep -rn over board/cards/ for stale phrases (8,390; dismissing entry 5 gives; Either; $2,150 only; rows 1-20 all mapped; or edit LLM_VS_CODE)\",\n  \"cat -n docs/M2M3_COVERAGE.md; grep -n -i -E 'trigger|budget|3\\\\.5' docs/M2M3_COVERAGE.md -> no hits\",\n  \"sed of docs/LLM_VS_CODE.md rows 10, 12, 16; spec/REQUIREMENTS.md lines 319-331 and 125; docs/CONTRACT.md:300; memory/ORCHESTRATOR_DECISIONS.md:33-34\",\n  \"estimate/timebox line count on 20 M2/M3 cards (all >= 1); evals/golden/README.md:144 ($420 case_07)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"contract_majors_applied\": 3, \"critical_path_budget_and_trigger\": 2, \"ship_bar_fixture_cannot_ship\": 5, \"lexicon_gate_decided\": 5, \"qa_owner_coverage\": 5, \"claims_match_board\": 2, \"paralegal_journey_acs\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"PM1 not fully applied: M2 critical path has no total against the 3.5 h budget and no cut trigger\",\n   \"evidence\": \"docs/M2M3_COVERAGE.md:4 'Estimates ~30–45 min each with 4 workers in parallel'; :5 cut levers with no trigger; grep -n -i -E 'trigger|budget|3\\\\.5' docs/M2M3_COVERAGE.md prints nothing; docs/CONTRACT.md:300 '### M2 — Core pipeline + evals green (≤ 3.5 h)'; 7 serial cards x 30-45 min = 3.5-5.25 h\",\n   \"why_it_matters\": \"The round-1 fix had three parts; two are done. Without the total and the trigger, the cut order cannot be executed at the moment it is needed: at the low estimate the chain uses the whole M2 budget, at the high estimate it overruns.\",\n   \"fix\": \"Add one sentence under docs/M2M3_COVERAGE.md:4: 'Serial chain = 7 x 30-45 min = 3.5-5.25 h against the 3.5 h M2 budget; if T-035 or T-036 is not green by estimate + N min, pull cut (1), then (2).' N set by the orchestrator.\",\n   \"acceptance_test\": \"grep -n -i 'trigger' docs/M2M3_COVERAGE.md returns a line holding the chain total in hours and a minute threshold.\"},\n  {\"severity\": \"major\", \"title\": \"T-018 AC2 is done on evidence that cites the superseded verdict (round-2 N1 still open)\",\n   \"evidence\": \"board.py show T-018: AC2 done true, evidence 'every blocker/major applied ... verified by reviews/T-018-product-manager.md'; that file's JSON verdict is 'changes'\",\n   \"why_it_matters\": \"The gate reads the cited file and finds the opposite of the claim. The claim is closer to true now, but AC2 cannot be verified until F1 closes.\",\n   \"fix\": \"Set T-018 AC2 done false until F1 closes; then cite reviews/T-018-product-manager-r2.md in its evidence once that file's JSON verdict is pass.\",\n   \"acceptance_test\": \"board.py show T-018 shows AC2 done false, or its evidence names a review file whose JSON verdict is pass.\"},\n  {\"severity\": \"minor\", \"title\": \"T-027 timebox has no stop action\",\n   \"evidence\": \"board.py show T-027 Description: 'Estimate: 40 min (timebox).' with no stop rule; round-1 fix asked for 'at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md'\",\n   \"why_it_matters\": \"A timebox with no stop rule leaves the lexicon card open-ended in practice.\",\n   \"fix\": \"Add to the T-027 Description: 'At 40 min, stop; held-out recall is reported, not gated (D-026); log the gap in memory/SCOPE_CUTS.md.'\",\n   \"acceptance_test\": \"board.py show T-027 Description contains 'SCOPE_CUTS' and 'reported, not gated'.\"},\n  {\"severity\": \"minor\", \"title\": \"Fifteen round-1 minors are still unapplied (non-gating)\",\n   \"evidence\": \"artifacts/review-evidence/T-018-r3-applied-check.out.txt lines 164-193: m-PM1a, m-PM1b, m-PM1c, m-PM2, m-PL1, m-PL2, m-PL3a, m-PL3b, m-PL4, m-S1, m-S2a, m-S2b, m-S3, m-S4, m-T17\",\n   \"why_it_matters\": \"Each named check can be ticked without proving its failure (cut clock, xfail on red tests, judge input isolation, verifier mutation guard, network guard, charge highlight, banner record). None gates, but each would miss its failure.\",\n   \"fix\": \"Apply each as an in-place AC edit, or record a deferral in memory/SCOPE_CUTS.md.\",\n   \"acceptance_test\": \"Re-run artifacts/review-evidence/T-018-r2-applied-check.py: NOT-APPLIED count 0, or each unapplied item has a SCOPE_CUTS row.\"},\n  {\"severity\": \"minor\", \"title\": \"Instruction ACs are copied across cards; T-036 has two identical D-025 ACs\",\n   \"evidence\": \"artifacts/review-evidence/T-018-r3-applied-check.out.txt lines 195-205 (10 distinct INFO texts on 2-3 cards each); board.py show T-036: AC7 and AC10 both 'Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033) ...'\",\n   \"why_it_matters\": \"Several workers tick copies of one instruction with no owner for the result; the duplicate is appended text, so the contract is unclear.\",\n   \"fix\": \"One owner for the coverage-doc rewrite (orchestrator); delete the copies on T-031, T-034, T-036 and the duplicate T-036 AC10.\",\n   \"acceptance_test\": \"The applied-check INFO line shows no 'Contract review (T-018):' text on more than one card; board.py show T-036 has one D-025 AC.\"}\n ],\n \"whats_right\": [\n  \"D-025 (row 10 is code) and D-026 (lexicon recall reported, not gated) are recorded in memory/ORCHESTRATOR_DECISIONS.md:33-34, and no 'or' alternative is left on T-033 AC6 or T-038 AC9.\",\n  \"The fixture cannot ship: T-038 AC4/AC5 and T-045 AC4 name the live backend (claude-cli), and T-045 AC7 gives the M3 gate its scores.verify_quickly key.\",\n  \"The qa owner gap is closed: probe qa:NONE count = 0, and T-048 owns the nine LLM-stage test files.\"\n ],\n \"questions_for_chris\": [\"D-026 makes lexicon recall reported, not gated, and says the ship bar is unchanged. REQUIREMENTS section 7 row 3 still reads 'per flag type ... recall >= 0.9'. Do you accept that the gate is system-level flag recall and the lexicon recall is only reported? T-038 AC9 depends on the answer.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T01:37:37.756Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:37:41.137Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md",
 "old_string": "- The fixture cannot ship: T-038 AC4/AC5 and T-045 AC4 name the live backend, and T-045 AC7 gives the M3 gate its verify_quickly key.",
 "new_string": "- The fixture cannot ship: T-038 AC4 makes determinism null on fixture and T-045 AC4 names the live backend (claude-cli); T-038 AC5 keeps ship_bar_met false when a bar is missed, and T-045 AC7 gives the M3 gate its verify_quickly key."
}
````

### User / tool · 2026-11-02T01:37:41.283Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:37:41.645Z

**tool call — Bash**
````
{
 "command": "grep -n 'T-038 AC4/AC5' reviews/T-018-product-manager-r2.md | cut -c1-200",
 "description": "Check for remaining AC4/AC5 wording in T-018 review"
}
````

### User / tool · 2026-11-02T01:37:41.731Z

**tool result**
````
126:  "The fixture cannot ship: T-038 AC4/AC5 and T-045 AC4 name the live backend (claude-cli), and T-045 AC7 gives the M3 gate its scores.verify_quickly key.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:37:43.513Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md",
 "old_string": "  \"The fixture cannot ship: T-038 AC4/AC5 and T-045 AC4 name the live backend (claude-cli), and T-045 AC7 gives the M3 gate its scores.verify_quickly key.\",",
 "new_string": "  \"The fixture cannot ship: T-038 AC4 makes determinism null on fixture and T-045 AC4 names the live backend (claude-cli); T-038 AC5 keeps ship_bar_met false when a bar is missed, and T-045 AC7 gives the M3 gate its scores.verify_quickly key.\","
}
````

### User / tool · 2026-11-02T01:37:43.659Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:20.530Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-017-product-manager-r3.md",
 "content": "# T-017 round-3: product-manager-reviewer apply-check of reviews/T-017-product-manager-r2.md\n\n**Verdict: changes.** 0 blockers, 3 majors, 2 minors, 1 nit.\n\nThe round-2 review had 4 majors and 1 minor. Status now:\n\n| Round-2 finding | Status | Evidence |\n|---|---|---|\n| Major 1: coverage counts R-ID mentions, not pass conditions | NOT APPLIED (F1) | Owner probe: 1 of 4 named R-IDs has a mapped card carrying its pass condition (`artifacts/review-evidence/T-017-r3-owner-probe.out.txt`). The column was declined in prose, with no recorded decision. |\n| Major 2: three ACs contradict golden or REQUIREMENTS; no plan self-check | PARTLY APPLIED | The three ACs are fixed in place (T-039 AC1, T-039 AC2, T-033 AC1). The self-check sentence is there, but it describes a control that no card builds (F2). |\n| Major 3: 11 unowned test files; row 10 engine | APPLIED | Probe `qa:NONE count = 0` (`artifacts/review-evidence/T-018-r3-applied-check.out.txt` lines 2-37). Row 10 is code: D-025 (`memory/ORCHESTRATOR_DECISIONS.md:33`), coverage `:97`, LLM_VS_CODE `:38`. |\n| Major 4: critical path, budget, cut order, ship-bar trace | PARTLY APPLIED (F3) | Applied: the 7-card chain (`:4`), the ship-bar to card table (`:8-15`), per-card estimates on all 20 cards, the stale 4 h lines deleted, cut (3) removed. Not applied: the total and cut trigger, the per-cut ship-bar mapping, and the claim \"never touches ship-bar items\" (cut 2 does). |\n| Minor: T-017 AC2 evidence \"rows 1-20 all mapped\" | NOT APPLIED (F4) | `board.py show T-017` AC2 evidence unchanged. |\n\n**Note on the applied-check script.** `T-018-r2-applied-check.py` marks T17-1a (\"coverage has pass-condition column\") and T17-2a (\"plan self-check\") APPLIED. Both matches are a sentence in the coverage doc (`docs/M2M3_COVERAGE.md:20` and `:19`), not the requested column or a working control. I am overriding those two results here and in `reviews/T-018-product-manager-r2.md`. I have not edited the script, so its output stays as the orchestrator received it.\n\n## Findings\n\n**F1 (major). The R-ID rows still name the wrong owners for three dealbreaker pass conditions.**\n- Evidence: `artifacts/review-evidence/T-017-r3-owner-probe.py` output: `[FAIL] R-FL-2 row=['T-033','T-036'] ac_owners=['T-043'] mapped_owners=[]`; `[FAIL] R-CO-9 row=['T-034'] ac_owners=['T-041','T-042'] mapped_owners=[]`; `[FAIL] R-EX-4 row=['T-041'] ac_owners=['T-039','T-044'] mapped_owners=[]`; `[PASS] R-RV-8` (T-043 AC3 carries \"edit-note\" and \"reload\"). The rows are `docs/M2M3_COVERAGE.md:41`, `:81`, `:67`. The owning ACs are T-043 AC6 (\"Date of accident per intake form: 2026-01-19\", side by side), T-042 AC6 and T-041 AC6 (\"could not process\"), T-039 AC6 and T-044 AC6 (\"EDITED ITEMS with original and new text\"). The column was declined at `docs/M2M3_COVERAGE.md:20`: \"Pass conditions live in each card's AC on the board ... this table maps ownership.\" No decision is recorded: `grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md` returns nothing.\n- Why it matters: this is the defect round 1 was about. A reader who looks up \"could not process\" (R-CO-9) or \"EDITED ITEMS\" (R-EX-4) finds a card that does not test the visible behaviour. The sentence at `:20` says the matrix maps ownership, and for these three rows it does not. T-017 AC1 (\"covered by >=1 M2/M3 card AC\") is still a mention test.\n- Fix: add the owning cards to rows `:41`, `:67`, `:81`, or add the \"Pass condition -> AC\" column the round-1 fix asked for. If the column is declined, record the decision with its reason in `memory/ORCHESTRATOR_DECISIONS.md` (the T-018 AC2 rule says rejected majors need a recorded reason).\n- Acceptance test: `.venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project` prints `RESULT: 4 of 4`.\n\n**F2 (major). The \"plan self-check\" names a control no card builds.**\n- Evidence: `docs/M2M3_COVERAGE.md:20`: \"Numbers in AC are checked against the golden set by T-038 (`--check-spec`) and the qa test-first cards (T-029, T-048, T-039).\" `board.py show T-038` AC2: \"`python -m evals.run --check-spec` compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt\". That checks the spec's export text, not AC numbers. `grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/` finds only the notes in T-017 and a lexicon line in T-027. No AC on any card diffs an AC's numbers against `evals/golden`.\n- Why it matters: the round-1 fix asked for a real check (\"every number in an AC is diffed against evals/golden expected values before in_review\"). The doc now says the check exists and names the wrong card for it. A worker who trusts line 20 will not write the numbers check, and the $8,390/$420 error this round fixed by hand could come back.\n- Fix: add an AC to T-038, for example \"`python -m evals.run --check-acs` diffs every number quoted in an M2/M3 card AC that matches a golden value against evals/golden expected JSON; a seeded wrong number in a temp copy makes it fail (tests/unit/test_ac_numbers.py)\". Or delete the sentence and name the risk in SCOPE_CUTS.\n- Acceptance test: T-038 has an AC naming `--check-acs` (or the sentence is removed), and `grep -c 'checked against the golden set by T-038' docs/M2M3_COVERAGE.md` is 0 or the AC exists.\n\n**F3 (major). The cut order says it \"never touches ship-bar items\", and cut (2) does.**\n- Evidence: `docs/M2M3_COVERAGE.md:5`: \"M2 cut order (never touches ship-bar items): (1) ... (2) judge #4 merged into judge #3 prompt; (3) T-046 side-by-side is M3's first cut; no ship-bar item is ever cut.\" `docs/LLM_VS_CODE.md:40` (row 12): \"**judge 4** confirms the category\" for pre_existing. Ship-bar row 3 (`spec/REQUIREMENTS.md:327`) measures \"Per flag type (gap, conflict, pre_existing, causation): precision >= 0.9 and recall >= 0.9\". Merging judge #4 into judge #3 changes the pre_existing path. The doc has no per-cut ship-bar mapping and no trigger; `grep -n -i trigger docs/M2M3_COVERAGE.md` is empty. The M2 budget (`docs/CONTRACT.md:300`, 3.5 h) is not stated against the 7-card chain (same as T-018 F1).\n- Why it matters: the cut order is the plan's answer to \"what goes when we run out of time\". If it says a cut is safe when it is not, the first lever pulled can break the flag gate with no test failing.\n- Fix: rewrite `:5` so each cut names the ship-bar row it touches, or \"none\" with the reason. Either drop \"never touches ship-bar items\", or keep cut (2) only with a T-036 AC that holds pre_existing precision and recall on the fixture after the merge. Add the trigger sentence from T-018 F1.\n- Acceptance test: every cut in `docs/M2M3_COVERAGE.md:5` names a ship-bar row or \"none (reason)\"; `grep -c 'never touches ship-bar items' docs/M2M3_COVERAGE.md` is 0 unless each cut carries a row.\n\n**F4 (minor, not gating). T-017 AC2 evidence still says \"rows 1-20 all mapped\".**\n- Evidence: `board.py show T-017` AC2 evidence: \"docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped\". Row 19 maps to T-041 and T-045, both M3 (`docs/M2M3_COVERAGE.md:106`); row 15 edit half maps to T-040, M3 (`:102`).\n- Fix: reword to \"rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design\".\n- Acceptance test: `board.py show T-017` AC2 evidence does not contain \"rows 1-20 all mapped\".\n\n**F5 (minor, not gating). Appended ACs now duplicate in-place text.**\n- Evidence: T-039 AC7 repeats AC2 (\"dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9\"); T-039 AC9 repeats AC1 (\"on case_07 with $420 accepted ... $420.00\"); T-036 AC7 and AC10 are identical (\"decided by D-025: provider-name conflicts come from code\").\n- Why it matters: no contradiction, but two ACs with the same text make it unclear which one is the contract, and round 2 asked for the appended copies to be deleted.\n- Fix: delete T-039 AC7 and AC9 and T-036 AC10.\n- Acceptance test: `board.py show T-039` and `T-036` have no two ACs with the same text.\n\n**F6 (nit). The critical path has a tie the doc does not name.**\n- Evidence: `board.py show T-034` depends_on includes T-031 and T-048; T-031 depends on T-029. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. `docs/M2M3_COVERAGE.md:4` names only the T-032/T-033 route.\n- Fix: add \"(ties with T-029 -> T-031 -> T-034 -> ... -> T-038)\" to `:4`.\n\n## Things that landed and should not break\n- T-039 AC1 and AC2 are fixed in place: \"$420.00\" for case_07 and \"dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9\" (matches `spec/REQUIREMENTS.md:125`, R-EX-7). T-033 AC1 no longer says \"only\".\n- Row 10 is decided and consistent across three files (D-025, `docs/LLM_VS_CODE.md:38`, `docs/M2M3_COVERAGE.md:97`); the probe finds 0 unowned test files.\n- The ship-bar to card table (`docs/M2M3_COVERAGE.md:8-15`) and per-card estimates on all 20 cards are in place.\n\n## Exercised\n- Read `personas/product-manager.md`, the memory index and its files, and `reviews/T-017-product-manager.md` and `reviews/T-017-product-manager-r2.md` (the findings and the fix text).\n- `.venv/bin/python tools/board.py validate` -> `ok (48 file(s))`.\n- `board.py show` on T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-044, T-045.\n- `cat -n docs/M2M3_COVERAGE.md` (lines 1-20, 22-109); `sed -n` of `docs/LLM_VS_CODE.md` rows 10, 12, 16; `spec/REQUIREMENTS.md` lines 98, 125, 143, 319-331 (R-RV-8, R-EX-7, R-CO-9, section 7); `docs/CONTRACT.md:300`.\n- `grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md` (no hits); `grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/` (no AC owner).\n- `.venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project` -> 1 of 4 PASS; output saved to `artifacts/review-evidence/T-017-r3-owner-probe.out.txt`.\n- `.venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py` (re-run, output read); its T17-1a and T17-2a results are overridden above.\n- Not run: no app, no eval (plan review; no code exists).\n\n```json\n{\"card\": \"T-017\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Round-3 apply-check of reviews/T-017-product-manager-r2.md (4 majors, 1 minor, 1 nit) against docs/M2M3_COVERAGE.md, board cards T-017, T-027, T-029..T-046, T-048, docs/LLM_VS_CODE.md rows 10, 12, 16, memory/ORCHESTRATOR_DECISIONS.md D-025/D-026, spec/REQUIREMENTS.md sections 7 and R-IDs, docs/CONTRACT.md:300. No app code exists; plan review only; no eval run.\",\n \"exercised\": [\n  \"read personas/product-manager.md in full; memory index and files; reviews/T-017-product-manager.md and reviews/T-017-product-manager-r2.md\",\n  \".venv/bin/python tools/board.py validate -> ok (48 file(s))\",\n  \"board.py show T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-044, T-045\",\n  \"cat -n docs/M2M3_COVERAGE.md; sed of docs/LLM_VS_CODE.md rows 10, 12, 16; sed of spec/REQUIREMENTS.md lines 98, 125, 143, 319-331; docs/CONTRACT.md:300\",\n  \"grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md -> no hits; grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/ -> no AC owner\",\n  \".venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project -> 1 of 4 R-IDs PASS (R-FL-2, R-CO-9, R-EX-4 FAIL); saved to artifacts/review-evidence/T-017-r3-owner-probe.out.txt\",\n  \".venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py re-run; T17-1a and T17-2a APPLIED results overridden (sentence matches, not the requested column or control)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"coverage_pass_conditions\": 2, \"ac_consistent_with_golden\": 4, \"qa_owned_tests\": 5, \"self_check_is_a_real_control\": 1, \"critical_path_and_cut_order\": 2, \"ship_bar_traced\": 4, \"board_claims_match_artifact\": 2},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"R-ID rows still name the wrong owners for three dealbreaker pass conditions (round-2 major 1 not applied; column declined in prose with no recorded decision)\",\n   \"evidence\": \"artifacts/review-evidence/T-017-r3-owner-probe.out.txt: R-FL-2 row ['T-033','T-036'] vs AC owner T-043 (AC6, 2026-01-19 side by side); R-CO-9 row ['T-034'] vs AC owners T-041, T-042 ('could not process'); R-EX-4 row ['T-041'] vs AC owners T-039, T-044 ('EDITED ITEMS'). Rows at docs/M2M3_COVERAGE.md:41, :81, :67. Declined at docs/M2M3_COVERAGE.md:20 'Pass conditions live in each card's AC on the board ... this table maps ownership'. grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md -> no hits. R-RV-8 passes (T-043 AC3 'edit-note' and 'reload').\",\n   \"why_it_matters\": \"This is the defect round 1 was about: a lookup by mention says covered while the visible behaviour (could not process; edited items; two accident dates side by side) has no mapped owner. T-017 AC1 remains a mention test.\",\n   \"fix\": \"Add the owning cards to the three rows (T-043 to R-FL-2; T-042 and T-041 to R-CO-9; T-039 and T-044 to R-EX-4), or add the 'Pass condition -> AC' column. If the column is declined, record the decision and reason in memory/ORCHESTRATOR_DECISIONS.md.\",\n   \"acceptance_test\": \".venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project prints RESULT: 4 of 4 R-IDs have a mapped owner carrying the pass condition.\"},\n  {\"severity\": \"major\", \"title\": \"The plan self-check names a control that no card builds\",\n   \"evidence\": \"docs/M2M3_COVERAGE.md:20 'Numbers in AC are checked against the golden set by T-038 (--check-spec) and the qa test-first cards (T-029, T-048, T-039).' board.py show T-038 AC2: --check-spec 'compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt'. grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/ -> only T-017 notes and a T-027 lexicon line.\",\n   \"why_it_matters\": \"The round-2 fix asked for a real check on AC numbers before in_review. The doc states the check exists and names a card that does not do it. The $8,390/$420 error fixed by hand this round can return with no test failing.\",\n   \"fix\": \"Add a T-038 AC: 'python -m evals.run --check-acs diffs every number in an M2/M3 card AC that matches a golden value against evals/golden expected JSON; a seeded wrong number in a temp copy makes it fail (tests/unit/test_ac_numbers.py)'. Or delete the sentence at docs/M2M3_COVERAGE.md:20 and record the risk in memory/SCOPE_CUTS.md.\",\n   \"acceptance_test\": \"T-038 has an AC naming --check-acs with a failing-on-seeded-error test, or docs/M2M3_COVERAGE.md:20 no longer names T-038 as the checker.\"},\n  {\"severity\": \"major\", \"title\": \"The cut order says it 'never touches ship-bar items', and cut (2) does (no per-cut row, no trigger)\",\n   \"evidence\": \"docs/M2M3_COVERAGE.md:5 'M2 cut order (never touches ship-bar items): ... (2) judge #4 merged into judge #3 prompt ...'. docs/LLM_VS_CODE.md:40 (row 12) '**judge 4** confirms the category' for pre_existing. spec/REQUIREMENTS.md:327 (ship-bar row 3) 'Per flag type (gap, conflict, pre_existing, causation): precision >= 0.9 and recall >= 0.9'. grep -n -i trigger docs/M2M3_COVERAGE.md -> no hits. docs/CONTRACT.md:300 'M2 ... (<= 3.5 h)' not stated against the 7-card chain.\",\n   \"why_it_matters\": \"The cut order is the plan's answer to 'what goes when time runs out'. If it says a cut is safe when cut (2) changes the pre_existing path that ship-bar row 3 measures, the first lever pulled can break the flag gate with no test failing.\",\n   \"fix\": \"Rewrite docs/M2M3_COVERAGE.md:5 so each cut names the ship-bar row it touches (or 'none' with the reason). Either drop 'never touches ship-bar items' or keep cut (2) only with a T-036 AC holding pre_existing precision and recall on the fixture after the merge. Add the total-and-trigger sentence from T-018 F1.\",\n   \"acceptance_test\": \"Every cut in docs/M2M3_COVERAGE.md:5 names a ship-bar row or 'none (reason)'; grep -c 'never touches ship-bar items' docs/M2M3_COVERAGE.md is 0 unless each cut carries a row.\"},\n  {\"severity\": \"minor\", \"title\": \"T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-2 minor not applied)\",\n   \"evidence\": \"board.py show T-017 AC2 evidence: \\\"docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped\\\". Row 19 maps to T-041 and T-045, both M3 (docs/M2M3_COVERAGE.md:106); row 15 edit half maps to T-040, M3 (:102).\",\n   \"why_it_matters\": \"The evidence claims more than the artifact shows about M2, which is the habit the gate looks for.\",\n   \"fix\": \"Reword to 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.\",\n   \"acceptance_test\": \"board.py show T-017 AC2 evidence does not contain 'rows 1-20 all mapped'.\"},\n  {\"severity\": \"minor\", \"title\": \"Appended ACs now duplicate in-place text (T-039 AC7/AC2, T-039 AC9/AC1, T-036 AC7/AC10)\",\n   \"evidence\": \"board.py show T-039: AC7 'Contract review (T-018): T-039 AC2: dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9' repeats AC2; AC9 repeats AC1's '$420.00' clause. board.py show T-036: AC7 and AC10 identical ('decided by D-025: provider-name conflicts come from code (T-033)').\",\n   \"why_it_matters\": \"No contradiction, but identical ACs leave it unclear which is the contract, and round 2 asked for the appended copies to be deleted.\",\n   \"fix\": \"Delete T-039 AC7 and AC9 and T-036 AC10.\",\n   \"acceptance_test\": \"board.py show T-039 and T-036 have no two ACs with the same text.\"},\n  {\"severity\": \"nit\", \"title\": \"The seven-card critical path has a tie the doc does not name\",\n   \"evidence\": \"Probe depends_on: T-034 ['T-031','T-048']; T-031 ['T-029']. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. docs/M2M3_COVERAGE.md:4 names only the T-032/T-033 route.\",\n   \"why_it_matters\": \"Which path is longest decides which card the cut order protects.\",\n   \"fix\": \"Add '(ties with T-029 -> T-031 -> T-034 -> ... -> T-038)' to docs/M2M3_COVERAGE.md:4.\",\n   \"acceptance_test\": \"docs/M2M3_COVERAGE.md:4 names both seven-card paths.\"}\n ],\n \"whats_right\": [\n  \"T-039 AC1 and AC2 are fixed in place: $420.00 for case_07 and 'dismissing entry 5 and leaving entry 6 pending ... 7 of 9' (matches spec/REQUIREMENTS.md:125), and T-033 AC1 no longer says 'only'.\",\n  \"Row 10 is decided and consistent across memory/ORCHESTRATOR_DECISIONS.md:33 (D-025), docs/LLM_VS_CODE.md:38 and docs/M2M3_COVERAGE.md:97; the probe finds 0 unowned test files.\",\n  \"The ship-bar to card table (docs/M2M3_COVERAGE.md:8-15) and per-card estimates on all 20 cards are in place.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T01:38:20.675Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-017-product-manager-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:23.250Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/board.py validate reviews/T-018-product-manager-r2.md; echo \"exit=$?\"; .venv/bin/python tools/board.py validate reviews/T-017-product-manager-r3.md; echo \"exit=$?\"",
 "description": "Validate both review files against the D.2 schema"
}
````

### User / tool · 2026-11-02T01:38:23.429Z

**tool result**
````
ok (1 file(s))
exit=0
ok (1 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:28.713Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t017_t018_review_history.md"
}
````

### User / tool · 2026-11-02T01:38:28.723Z

**tool result**
````
1	---
2	name: t017-t018-review-history
3	description: T-017 plan / T-018 contract review rounds (2026-11-01 to 11-02) — round-1 verdicts all 'changes', round-2 apply-check verdicts 'changes' with 9 contract majors and 4 T-017 majors still open
4	metadata:
5	  type: project
6	---
7	
8	State as of the round-2 apply-check (this review), not a live status. Re-check the board before acting on it.
9	
10	- Round 1: CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md, all 'changes' (6 + 4 + 9 majors). reviews/T-017-product-manager.md 'changes' (4 majors). Source of the fix texts.
11	- Round 2 (this review): reviews/T-018-product-manager.md 'changes': 10 majors (9 of 19 contract majors not applied, plus N1, T-018 AC2 ticked on a refuted claim). reviews/T-017-product-manager-r2.md 'changes': 4 majors not applied.
12	- Still open: pass-condition column in docs/M2M3_COVERAGE.md; the lexicon-recall release gate (LLM_VS_CODE rows 12/16 vs T-038 AC9 'or'); row-10 engine decision; 11 unowned test files (applied-check qa:NONE=11); T-039 AC1/AC2 and T-033 AC1 contradictions left in place; stale 5-card chain at coverage lines 18-19.
13	- Applied and verified: T-048 qa card; deps T-031/T-042/T-043; T-034 max_retries=0 and FixtureMissing; judge error paths; boundary module list; paralegal edit-reload, two-date conflict and record-4 ACs; verify_quickly in the paralegal agent body.
14	
15	**Why:** The orchestrator's round-2 claim ('every blocker/major applied') closed T-018 AC2. Without this record, a future reviewer would assume the M2 contract is settled.
16	
17	**How to apply:** On any future apply round, re-run artifacts/review-evidence/T-018-r2-applied-check.py and compare against the open list above. Check the lexicon gate decision first: cut (3) of the M2 cut order depends on it. See [[plan-review-patterns]] for the apply-check defects.
18	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:28.944Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md"
}
````

### User / tool · 2026-11-02T01:38:28.955Z

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
21	## Apply-check defects (T-018 round 2, 2026-11-01)
22	When the orchestrator "applies" review findings, check the result, not the claim. Round 2 showed the same failure modes:
23	7. **Appended, not edited.** The fix was added as a new AC (e.g. T-039 AC9) and the wrong AC (T-039 AC1, AC2) was left in place, so the card contradicts itself. Rule used: an appended AC counts only if no in-place text on the same card contradicts it.
24	8. **'Either ... or' left in the AC.** "Either T-033 gains AC6 ... or an ADR edits row 10" is a decision the card never made. Count it as not applied until one branch is chosen and recorded in ORCHESTRATOR_DECISIONS.
25	9. **Estimates and timeboxes skipped.** "Per-card estimate in each Description" landed on 2 of 20 cards. Count the cards, not the doc sentence.
26	10. **Old text kept beside the new.** The coverage doc got a new critical-path section, but the old 5-card chain and '4 h, over budget' lines stayed 15 lines lower. grep for the stale phrase.
27	11. **Instruction copied to several cards.** 11 distinct 'Contract review (T-018):' ACs sit on 2-3 cards each, so nobody owns the outcome.
28	12. **Claim on the board that the check refutes.** T-018 AC2 said "every blocker/major applied"; 9 of 19 were not.
29	13. **Owner probe must skip instruction text.** An AC that says "name test_api.py ... by file" is not an owner. Exclude 'Contract review (T-018):' lines from the qa-owner probe, or the count reads 0 when it is 11.
30	14. **Patterns match in the wrong file.** A 'self-check|diff .* golden' pattern matched an unrelated lexicon decision (D-018). Anchor patterns to the file and section that must hold the text, then read each matched line.
31	
32	**Script:** artifacts/review-evidence/T-018-r2-applied-check.py (68 checks, prints the matched line for each; output in T-018-r2-applied-check.out.txt). Re-run on every apply round before any 'applied' verdict. Related: [[needs-chris-drift]].
33	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:34.101Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t017_t018_review_history.md",
 "content": "---\nname: t017-t018-review-history\ndescription: T-017 plan / T-018 contract review rounds (2026-11-01 to 11-02) — r1 all 'changes'; r2 apply-check 'changes'; T-018 r2 and T-017 r3 apply-check 'changes' (2 and 3 majors, all small)\nmetadata:\n  type: project\n---\n\nState as of the T-018 r2 and T-017 r3 apply-check (2026-11-01). Not a live status: re-check the board before acting on it.\n\n- Round 1: CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md, all 'changes' (6 + 4 + 9 majors). reviews/T-017-product-manager.md 'changes' (4 majors).\n- Round 2: reviews/T-018-product-manager.md 'changes' (10 majors, incl. N1). reviews/T-017-product-manager-r2.md 'changes' (4 majors, 1 minor, 1 nit).\n- Round 3 (this apply-check): reviews/T-018-product-manager-r2.md 'changes': 2 majors. (F1) PM1 total against the 3.5 h budget and a cut trigger are missing from docs/M2M3_COVERAGE.md. (F2) T-018 AC2 still done on evidence that cites the 'changes' file. Script: 15 distinct NOT-APPLIED, all minors. reviews/T-017-product-manager-r3.md 'changes': 3 majors. (F1) R-FL-2, R-CO-9, R-EX-4 rows do not name the cards whose ACs carry their pass conditions (owner probe 1 of 4). (F2) the 'plan self-check' names T-038 --check-spec as an AC-number check; it is not. (F3) cut order says 'never touches ship-bar items' and cut (2) merges judge #4, which row 12 uses for pre_existing.\n- Applied and verified in round 3: lexicon gate (D-026, T-038 AC9 'reported, not gated'); row 10 (D-025, code); T-045 AC4 uses claude-cli; T-045 AC7 verify_quickly; T-027 P0 + 40 min timebox; qa:NONE = 0 (T-048); deps; estimates on all 20 cards; T-039 AC1/AC2 and T-033 AC1 fixed in place; the ship-bar to card table.\n\n**Why:** A round-2 apply check passed the script's pass rule (only minors left) while the card still cited a refuted verdict and a fix was only half done. Without this record a future reviewer would take the M2 contract as settled.\n\n**How to apply:** Re-run artifacts/review-evidence/T-018-r2-applied-check.py and artifacts/review-evidence/T-017-r3-owner-probe.py on any apply round. Check T-018 AC2's evidence, the coverage doc total/trigger, and cut (2) first. See [[plan-review-patterns]] for the apply-check defects.\n"
}
````

### User / tool · 2026-11-02T01:38:34.197Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t017_t018_review_history.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:38.409Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md",
 "old_string": "**Script:** artifacts/review-evidence/T-018-r2-applied-check.py (68 checks, prints the matched line for each; output in T-018-r2-applied-check.out.txt). Re-run on every apply round before any 'applied' verdict. Related: [[needs-chris-drift]].",
 "new_string": "**Script:** artifacts/review-evidence/T-018-r2-applied-check.py (68 checks, prints the matched line for each; output in T-018-r2-applied-check.out.txt). Re-run on every apply round before any 'applied' verdict. Related: [[needs-chris-drift]].\n\n## Apply-check defects (T-018 r3 / T-017 r3, 2026-11-01)\n15. **Regex matches a sentence, not the structure.** The script marked \"pass-condition column\" APPLIED on a prose sentence (\"Pass conditions live in each card's AC\"), and \"self-check\" APPLIED on a sentence. Check the requested structure (column, AC, number) by reading the matched line, not the match.\n16. **Declined in prose.** A fix that asked for a column or a check was answered by a sentence saying it is not needed. Count it not applied unless a decision with a reason is recorded in ORCHESTRATOR_DECISIONS or GATE-M1-summary. The T-018 AC2 rule requires that record.\n17. **Mapping not updated after the AC moved.** The round-1 AC text landed on T-039/T-042/T-043/T-044, but the R-ID rows (R-CO-9, R-EX-4, R-FL-2) still listed only the old owners. Probe: artifacts/review-evidence/T-017-r3-owner-probe.py (R-ID row vs cards whose AC text carries the phrase).\n16b. **Doc claims a checker that the card does not build.** \"Numbers in AC are checked by T-038 --check-spec\": T-038 AC2 checks the spec export text only. For every 'checked by X' sentence, quote X's AC.\n17b. **'Never touches ship-bar items' is a claim.** Cut (2) merged judge #4, which LLM_VS_CODE row 12 uses for the pre_existing category (ship-bar row 3). Each cut needs the row it touches.\n18. **Partial apply of a three-part fix.** PM1 had: delete stale lines (done), per-card estimates (done), state total and trigger (not done). Split a multi-part fix into its parts and check each.\n19. **grep -c double counts.** The applied-check prints the minors twice (MINORS block and SUMMARY). grep -c NOT-APPLIED reads 30 for 15 items. Report distinct items.\n20. **Card evidence cites a refuted verdict.** T-018 AC2 evidence names reviews/T-018-product-manager.md (JSON verdict 'changes'). A done claim must cite the review whose JSON verdict is 'pass'."
}
````

### User / tool · 2026-11-02T01:38:38.507Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:41.036Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [T-017/T-018 review history](project_t017_t018_review_history.md) — round-1 and round-2 apply-check verdicts (changes); open: gate decision, pass-condition column, 11 unowned tests",
 "new_string": "- [T-017/T-018 review history](project_t017_t018_review_history.md) — r1, r2, and r3 apply-check verdicts (all changes); open: owner rows, self-check claim, cut-order claim, T-018 AC2 evidence"
}
````

### User / tool · 2026-11-02T01:38:41.135Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:38:45.427Z

T-018 r2: changes (0 blockers, 2 majors): the M2 critical path has no total against the 3.5 h budget or a cut trigger, and T-018 AC2 is still ticked on the 'changes' review. The script's 15 NOT-APPLIED lines (30 grep hits, all minors) pass its own rule, but I overrode its T17-1a and T17-2a results. `/Users/arsis/zlayt-pm-project/reviews/T-018-product-manager-r2.md`
T-017 r3: changes (0 blockers, 3 majors): R-FL-2, R-CO-9 and R-EX-4 rows name no card that tests their pass condition; the "self-check" cites a T-038 check that does not exist; the cut order's "never touches ship-bar items" is contradicted by cut (2). `/Users/arsis/zlayt-pm-project/reviews/T-017-product-manager-r3.md`
Both pass `board.py validate`; model `claude-haiku-5-5`.
