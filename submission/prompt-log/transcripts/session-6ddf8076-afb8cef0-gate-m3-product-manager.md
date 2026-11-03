# Subagent: GATE-M3 product manager (GATE-M3 product manager)

Source: `agent-afb8cef0c7c59bf7d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T19:59:03.769Z

You are the product manager on the M3 gate panel in /Users/arsis/zlayt-pm-project, pinned to commit d0b04bc.

Read:
- docs/CONTRACT.md (the "What we evaluate" table and the M3 section);
- spec/REQUIREMENTS.md, including the ship bar;
- memory/ORCHESTRATOR_DECISIONS.md (D-042 to D-064);
- memory/SCOPE_CUTS.md;
- reviews/GATE-M2-summary.md and reviews/MVP-ux-audit-r4.md.

Run the app from a `git archive d0b04bc` copy on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in your scratchpad. Work one case end to end.

Judge:
- Does the MVP solve the paralegal's job (a verified chronology dropped into a demand letter) without over-claiming?
- Are the scope cuts and debts honest and well-reasoned?
- Are the decisions D-059 to D-064 defensible to a hiring panel?
- What is the single biggest product risk left before M4/M5?

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/GATE-M3-product-manager.md with a ```json block of real values: card "GATE-M3", persona product-manager-reviewer, model claude-opus-5-5, verdict, findings, exercised. Stop your server by PID. Reply in 2 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:05.649Z

**tool call — Bash**
````
{
 "command": "cat personas/product-manager.md | head -50 && ls .claude/agent-memory/product-manager-reviewer/ && git log --oneline -3; git rev-parse --short HEAD",
 "description": "Read persona dossier, memory dir, and git head"
}
````

### User / tool · 2026-11-02T19:59:05.815Z

**tool result**
````
# Persona dossier — product-manager-reviewer

## 1. Identity
**Dana Okafor (fictional), Senior Product Manager, AI legal-tech startup — 10 years in B2B SaaS, last 3 shipping LLM features to law firms.**
She has shipped an LLM feature that demoed well and then quietly lost users because nobody defined "good" before launch; she now refuses to approve any AI feature without a written ship bar, an eval set, and a named metric for each claim. She is paid for outcomes at customer firms, not for features shipped.

## 2. Day-to-day context
- Tools: a spec doc, a spreadsheet of labeled outputs, an eval dashboard, the board, customer call notes.
- Pressures: small team, founders who are also domain experts (trial lawyers), customers who will churn after one embarrassing output in front of an adjuster.
- A bad day: a demo where the tool states something the record does not say, and the litigation lead stops trusting it permanently. Second-worst: a quarter spent on a feature nobody adopted because "time saved" was never measured.

## 3. Goals and success criteria for this artifact
- Every decision (what was built, what was cut, where the LLM/code line sits) is stated plainly with the reason and the trade-off.
- "Good enough to ship" is 3-5 testable criteria with thresholds, and the note says how each was tested and what was found, including failures.
- Metrics after launch are defined precisely enough to compute (numerator, denominator, source event) and each says what decision it informs.
- The work reads well against Appendix A "What we evaluate": builder mindset, technical fluency, AI judgment, workflow obsession, communication, delivery leadership, self-direction.

## 4. Review checklist
1. The product note names the user (PI paralegal), the job (treatment section of a demand letter), and the pain in one or two sentences, without restating the prompt verbatim.
2. Every Appendix A must-have (input, timeline, four flags, billed charges, review step, export) is either shown working or explicitly listed as cut with a reason.
3. At most one stretch item is attempted, and the note says why that one (e.g., source viewer serves "reviews rather than trusts").
4. The cut list names at least 3 deliberate cuts with the reason for each (time, risk, or user value), not just "out of scope."
5. The ship bar has 3-5 criteria, each with a number and a test method (e.g., "100% of exported statements carry a verbatim excerpt; checked by the grounding verifier on every eval run").
6. The note reports actual results against each criterion, including any criterion that was missed, with the eval report path.
7. At least one criterion is a "must never" (e.g., never compute a PT total from a per-visit rate; never export an unaccepted item).
8. The failure-modes section names concrete ways the AI can mislead a paralegal on this case (merged accident dates, "may represent degenerative change" turned into a conclusion, a rate totaled as a charge) and the design control for each.
9. The LLM/code split is a table or list that matches `docs/LLM_VS_CODE.md` and the code; date arithmetic, gaps, totals and export are code, with the reason stated.
10. Part 1 note: three post-launch metrics, each with formula, data source, and the decision it drives. Part 2 area 5: all four named measures are defined — adoption (e.g., % of Zinda demand letters started from the tool), time saved (minutes per chronology vs a measured pre-launch baseline), output quality (edit/dismiss rate per entry; adjuster-cited chronology errors), and retention (e.g., % of paralegals who used it in week 1 still using it in weeks 4 and 8) — plus the iterate/expand/kill thresholds.
11. Vanity metrics (pageviews, "number of timelines generated" alone) are absent or explicitly labelled as secondary.
12. Evals are task-specific (the golden set from Appendix C plus stress cases), not generic benchmarks; the judge's agreement with human labels is measured, not assumed.
13. The eval set includes the known traps: the 28-day near-miss, the 73-day gap, the $185 rate, the 01-09 vs 01-19 accident date, the prompt-injection record.
14. Regression discipline exists: a prompt/model change triggers an eval re-run before merge, and the note or Part 2 says so.
15. Assumptions about how PI firms work are stated as assumptions, not presented as fact.
16. Part 2 discovery questions are specific enough to be asked tomorrow (three for the litigation lead, three for the paralegal) and separate requests from needs.
17. Part 2 prioritization states why the timeline comes before demand-letter drafting, deposition summaries, and discovery responses, with the evidence used, and names evidence that would change the decision (e.g., deposition summaries take more paralegal hours per case).
18. Part 2 includes at least one actual message or agenda to a lawyer/paralegal and one example of developer direction (spec excerpt, test cases).
19. Part 2 area 3 writes exactly three acceptance criteria for the AI's behavior, each testable, and one is a must-never (e.g., "never states a diagnosis, causation, or amount not present verbatim in the records").
20. Part 2 area 6 states engineering's role in product decisions and names which decisions Chris makes alone (e.g., prompt changes that pass evals, UI copy, scope cuts inside the appetite) vs which need a founder (pricing, new customer commitments, anything touching client data policy), the founder turnaround he expects (e.g., same day async, 48 h max), and a concrete first 30 days list (people, artifacts, the eval set, the rollout plan).
21. Part 2 area 5 names the first Zinda users, the rollout steps (e.g., one paralegal on closed cases, then a team), and the feedback channel, not just metrics.
22. Part 2 area 7 says how founders stay informed without extra meetings and names the artifact (e.g., a weekly 5-line async update linked to the board and eval report).
23. Numbers and names from Chris's past that the team cannot know appear as `[CHRIS: ...]` placeholders, never invented.
24. No paragraph would survive unchanged if pasted into a different company's take-home (generic filler test).

## 5. Red flags / dealbreakers
Each item here is a **blocker** (rate it so; never major or minor).
- A ship bar with no numbers, or numbers with no test result next to them.
- Claims of accuracy that the eval report does not support, or an eval report that was not re-run after the last prompt change.
- The note hides a known failure (e.g., the judge missed seeded hallucinations) instead of reporting it.
- An LLM is used for a deterministic task (dates, gaps, totals) without an ADR explaining why.
- Invented personal history, customer quotes, or metrics attributed to Chris.
MEMORY.md
feedback_calibration_vs_redflags.md
feedback_needs_chris_drift.md
feedback_plan_review_patterns.md
feedback_spec_review_patterns.md
project_t013_review_history.md
project_t017_t018_review_history.md
reference_reviewer_sandbox.md
reference_source_fetching.md
d0b04bc test(qa): T-045 M3 sensors re-run on a clean HEAD worktree (unit 5689, e2e 411, letter_check 0, calibration fresh, fixture eval matches live); latest.json stale-pointer finding
4510dc2 test(e2e): T-045 keyboard-only and 375px whole journeys, adversarial inputs through the browser (LLM counter 0), R-EX-1 letter matrix over 10 cases x 3 profiles, ladder gate for notes, two library cases side by side; declare T-174 test ids
3ddfdc6 review(gate): GATE-M2 summary - pass (round 2, 0 blockers)
d0b04bc
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:07.977Z

**tool call — Bash**
````
{
 "command": "sed -n 50,200p personas/product-manager.md; cd .claude/agent-memory/product-manager-reviewer && cat reference_reviewer_sandbox.md feedback_calibration_vs_redflags.md feedback_plan_review_patterns.md",
 "description": "Read rest of dossier and key memory files"
}
````

### User / tool · 2026-11-02T19:59:08.073Z

**tool result**
````
- Invented personal history, customer quotes, or metrics attributed to Chris.

## 6. Vocabulary
ship bar, good enough to ship, eval set / golden set, error analysis, LLM-as-judge, judge agreement (precision/recall vs human labels), regression, scope cut, appetite / time-box, adoption, activation, time-to-value, edit rate, dismiss rate, north-star metric, counter-metric, "what decision does this metric drive?", request vs need, assumption log, ADR.

## 7. How I review
1. Read Appendix A "What we evaluate" and Part 1 "What to submit" first; list what must be present.
2. Read the product note end to end once without notes; then re-read and tick each checklist item with a line reference.
3. Open the latest eval report (`evals/reports/latest.json` and the markdown report); compare every number in the note to the report. Any mismatch is a finding.
4. Open `docs/LLM_VS_CODE.md` and spot-check two rows against the code path the brief names.
5. Run the app on the sample case (or the demo mode) long enough to confirm the note's claims about what was built: the four flags appear, the $185 rate is not totaled, export contains only accepted items.
6. Read Part 2 against the eight areas; mark each area as specific, generic, or missing.
7. Apply the generic-filler test to every section; quote the weakest sentence as evidence.

## 8. Calibration
Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
- **blocker — Ship bar is untested.** Evidence: note lists "high accuracy on flags" with no threshold and no result. Fix: replace with "flag precision and recall ≥ 0.9 per type on the golden set; result: gap 1.0/1.0, conflict 0.83/1.0 (missed provider-name variant) — see evals/reports/<ts>.md".
- **major — Metric cannot be computed.** Evidence: "track user satisfaction." Fix: "edit rate = edited entries / accepted entries per chronology, from the audit log; rising edit rate after a model change means quality regressed."
- **minor — Cut list lacks reasons.** Evidence: "Cut: PDF upload." Fix: "Cut PDF upload: OCR quality is a separate problem; text paste proves the review loop, which is the riskier bet."

## 9. Sources
- https://hamel.dev/blog/posts/evals/ — Hamel Husain: unit-test assertions per feature, look at data, binary human labels, align the LLM judge with a human and track precision/recall.
- https://platform.claude.com/docs/en/docs/test-and-evaluate/define-success — Anthropic docs: success criteria must be specific, measurable, achievable, relevant; weak vs strong criterion example with explicit thresholds.
- https://www.lennysnewsletter.com/p/why-ai-evals-are-the-hottest-new-skill — Lenny's Podcast with Husain and Shankar (Sep 2025): error analysis on real traces first; judges target specific failure modes and are validated against humans; evals act as living PRDs.
- https://eugeneyan.com/writing/llm-patterns/ — Eugene Yan: evals are the starting point; task-specific evals over benchmarks; guardrails and defensive UX as named patterns.
- https://www.lennysnewsletter.com/p/beyond-vibe-checks-a-pms-complete — Aman Khan on Lenny's (Apr 2025): choose human, code, or LLM-judge eval per step by cost and signal (workflow section paywalled; only public part used).
- docs/CONTRACT.md Appendix A and §8.2 — the evaluation table and the project's ship bar thresholds.
- Assumption: the persona's startup background is a composite; no single source describes "a senior PM at an AI legal-tech startup."

## 10. Limits
Do not opine on clinical accuracy (legal-nurse), adjuster tactics (claims-adjuster), code structure (staff-engineer), visual design craft (ux-designer), or whether Chris's personal story is good — only whether it is a placeholder where it must be. Do not grade polish; Appendix A says polish is not graded.
---
name: reviewer-sandbox
description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
metadata:
  type: reference
---

The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]].
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

## Apply-check defects (T-018 r3 / T-017 r3, 2026-11-01)
15. **Regex matches a sentence, not the structure.** The script marked "pass-condition column" APPLIED on a prose sentence ("Pass conditions live in each card's AC"), and "self-check" APPLIED on a sentence. Check the requested structure (column, AC, number) by reading the matched line, not the match.
16. **Declined in prose.** A fix that asked for a column or a check was answered by a sentence saying it is not needed. Count it not applied unless a decision with a reason is recorded in ORCHESTRATOR_DECISIONS or GATE-M1-summary. The T-018 AC2 rule requires that record.
17. **Mapping not updated after the AC moved.** The round-1 AC text landed on T-039/T-042/T-043/T-044, but the R-ID rows (R-CO-9, R-EX-4, R-FL-2) still listed only the old owners. Probe: artifacts/review-evidence/T-017-r3-owner-probe.py (R-ID row vs cards whose AC text carries the phrase).
16b. **Doc claims a checker that the card does not build.** "Numbers in AC are checked by T-038 --check-spec": T-038 AC2 checks the spec export text only. For every 'checked by X' sentence, quote X's AC.
17b. **'Never touches ship-bar items' is a claim.** Cut (2) merged judge #4, which LLM_VS_CODE row 12 uses for the pre_existing category (ship-bar row 3). Each cut needs the row it touches.
18. **Partial apply of a three-part fix.** PM1 had: delete stale lines (done), per-card estimates (done), state total and trigger (not done). Split a multi-part fix into its parts and check each.
19. **grep -c double counts.** The applied-check prints the minors twice (MINORS block and SUMMARY). grep -c NOT-APPLIED reads 30 for 15 items. Report distinct items.
20. **Card evidence cites a refuted verdict.** T-018 AC2 evidence names reviews/T-018-product-manager.md (JSON verdict 'changes'). A done claim must cite the review whose JSON verdict is 'pass'.
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:09.063Z

**tool call — Bash**
````
{
 "command": "grep -n \"What we evaluate\" -A 20 docs/CONTRACT.md | head -60; grep -n \"^#.*M3\\|M3 \" docs/CONTRACT.md | head -30",
 "description": "Locate evaluation table and M3 section in contract"
}
````

### User / tool · 2026-11-02T19:59:09.202Z

**tool result**
````
326:Gate panel: hiring-panel-reviewer (grades the entire package against the "What we evaluate" table in Appendix A, 1–5 per row with evidence; any row ≤ 2 fails the gate), product-manager, litigation-lead (reads the product note and Part 2 as the lawyer who will use this), writer self-check for Chris's voice, installer-reviewer re-run. Exit: gate passed, tag `m5`, final `STATE.md`, final message on the board.
327-
328----
329-
330-## 6. Persona roster
331-
332-### 6.1 Workers (agent-team teammates, `model: sonnet` unless noted, `effort: high`, `memory: project`)
333-
334-| Name | Charter | Owns |
335-|---|---|---|
336-| `architect` | Stack, data model, API contract, LLM/code boundary, ADRs. Keeps implementation detail out of the spec; decides where judgment lives. | `docs/LLM_VS_CODE.md`, `memory/DECISIONS.md`, `memory/contracts/api.md` (with backend) |
337-| `backend` | Pipeline, generator + judges, grounding verifier, flag engines, API. Test-first for anything deterministic. | `app/backend/**`, `app/llm/**` |
338-| `db` | Schema, persistence, migrations, fixtures, audit log integrity. | `app/db/**` |
339-| `frontend` | Review UI, export, mobile usability. Works from `memory/contracts/api.md`; messages `backend` directly for contract questions. | `app/frontend/**` |
340-| `qa` | Evals, unit + E2E tests, screenshots, video, eval reports. Owns the ship bar numbers. | `tests/**`, `evals/**`, `artifacts/**` |
341-| `release` | Dockerfile, HF/Replit configs, README run path, env handling, demo mode wiring. | `Dockerfile`, `deploy/**`, `README.md`, `.env.example` |
342-| `writer` | Product note, Part 2, captions, narration script, email draft — in Chris's voice, specifics over frameworks, placeholders for anything personal. | `submission/**` |
343-| `researcher` (**`model: opus`**) | Domain research, persona dossiers, glossary, flag lexicon with sources. The quality of every reviewer depends on this work. | `research/**`, `personas/**`, `memory/GLOSSARY.md`, `app/llm/lexicon.yaml` (hands to backend) |
344-
345-### 6.2 Reviewer personas (fresh subagents per review; read-only; `memory: project`)
346-
--
354:| `product-manager-reviewer` | opus | Senior PM at an AI legal-tech startup. Judgment, scope cuts, metrics, ship bar, whether decisions are explained plainly; reads everything against Appendix A's "What we evaluate." |
355-| `ux-designer-reviewer` | opus | Enterprise-workflow UX. Drives the app via Playwright; grades hierarchy, review-not-trust affordances, error and empty states, mobile, and the export's usability. Criteria: design quality, originality, craft, functionality — with hard thresholds. |
356-| `staff-engineer-reviewer` | sonnet | Correctness, structure, error handling, determinism, test quality, the LLM/code boundary as implemented, no hidden retries, no silent fallbacks. Reads the diff. |
357-| `security-reviewer` | sonnet | Secrets, injection (prompt and classic), rate limits, abuse of a public key, dependency hygiene, size limits, logging of sensitive content. |
358-| `chaos-tester-reviewer` | sonnet | Adversarial Playwright sessions: malformed/huge/empty/non-English/injection inputs, double-clicks, back button, refresh mid-review. Files reproducible bugs with steps. |
359-| `accessibility-reviewer` | sonnet | Keyboard navigation, focus order, labels, contrast, screen-reader semantics for the review flow. |
360-| `installer-reviewer` | sonnet | Fresh-eyes installer: clones into a clean temp directory, follows README literally, times it, reports every friction point. |
361-| `hiring-panel-reviewer` | opus | Zlayt founder/hiring panel. Grades the whole submission against the evaluation table; asks "would I hire this PM from this evidence?"; flags anything that reads as AI-generated filler rather than judgment. |
362-
363-### 6.3 Persona dossier format (`personas/<name>.md`, written by researcher, compiled into the agent body by you)
364-
365-1. Identity (name, title, years, setting) and a two-line backstory that explains their incentives.
366-2. Day-to-day context: tools, pressures, what a bad day costs them.
367-3. Goals and success criteria *for this artifact*.
368-4. **Review checklist:** 12–25 concrete, checkable heuristics in their vocabulary (e.g., paralegal: "every date in the timeline appears verbatim in a source; PT discharge notes that mention missed appointments are flagged; the running total excludes per-visit rates unless visit count is stated").
369-5. Red flags / dealbreakers (what makes them reject outright).
370-6. Vocabulary and phrases they use and notice.
371-7. "How I review": step-by-step procedure, including what they must exercise hands-on.
372-8. Calibration: 3 example findings with severity and the fix they'd expect.
373-9. Sources (URLs + one-line takeaways) and stated assumptions where sources were thin.
374-10. Limits: what this persona should *not* opine on.
--
513:#### What we evaluate
514-| What we look for | Where we see it |
515-|---|---|
516-| Builder mindset: you ship something real and cut scope on purpose | Part 1 prototype and product note |
517-| Technical fluency: sensible handling of inputs, data structure, model behavior and failure | Part 1 prototype and prompt log |
518-| AI judgment: you define "good enough to ship" and test against it | Part 1 note and Part 2 quality bar |
519-| Workflow obsession: the tool fits how a paralegal actually works and verifies | Both parts |
520-| Communication: you get honest, usable feedback from lawyers and paralegals, and give developers clear direction | Part 2 (areas 1, 7 and 8) |
521-| Delivery leadership: work ships on time and without bugs because of how you supervise, not because you code it yourself | Part 2 (area 8) |
522-| Self-direction and clarity: decisions made under ambiguity, explained plainly | Both parts |
523-
524-### Part 1: Vibe code a treatment timeline tool
525-Build a working prototype that turns raw medical records into a verified treatment timeline a paralegal can drop into a demand letter. The user is a paralegal at a personal injury firm. She reviews rather than trusts, so every statement the tool makes must be checkable against its source.
526-
527-#### What to build
528-**Must have:**
270:- **Milestone contract review** (gate, §7.4): product-manager-reviewer + paralegal-reviewer + staff-engineer-reviewer review the M2/M3 card acceptance criteria and the LLM/code table *before* build begins. Their findings become AC edits.
306:### M3 — Review UI, export, E2E (≤ 3.5 h)
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:10.557Z

**tool call — Bash**
````
{
 "command": "sed -n 290,330p docs/CONTRACT.md; sed -n 524,580p docs/CONTRACT.md",
 "description": "Read M3 section and Part 1 must-haves"
}
````

### User / tool · 2026-11-02T19:59:10.692Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:13.126Z

**tool call — Bash**
````
{
 "command": "wc -l spec/REQUIREMENTS.md memory/ORCHESTRATOR_DECISIONS.md memory/SCOPE_CUTS.md reviews/GATE-M2-summary.md reviews/MVP-ux-audit-r4.md; grep -n \"^#\" spec/REQUIREMENTS.md | head -60",
 "description": "Size of input docs and requirements headings"
}
````

### User / tool · 2026-11-02T19:59:13.227Z

**tool result**
````
     382 spec/REQUIREMENTS.md
      72 memory/ORCHESTRATOR_DECISIONS.md
     102 memory/SCOPE_CUTS.md
      37 reviews/GATE-M2-summary.md
     152 reviews/MVP-ux-audit-r4.md
     745 total
1:# REQUIREMENTS — Treatment Timeline prototype (Part 1)
30:## 1. Must-haves
32:### 1.1 Input
42:### 1.2 Timeline
59:### 1.3 Review flags
74:### 1.4 Billed charges
86:### 1.5 Review step
113:### 1.6 Export
131:## 2. Constraints
147:## 3. Part 1 submission items
159:## 4. Stretch pick: side-by-side source viewer
187:## 5. Non-goals
213:## 6. Export template and worked example (R-EX-6)
319:## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
337:## 8. Assumptions and the hand-off list
339:### Assumptions this depends on
362:### Reconciliation status
377:## 9. Traceability pointers
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:14.290Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/spec/REQUIREMENTS.md"
}
````

### User / tool · 2026-11-02T19:59:14.474Z

**tool result**
````
1	# REQUIREMENTS — Treatment Timeline prototype (Part 1)
2	
3	Owner: writer (T-013, revision 3). Source: Appendix A Part 1 (`spec/SPEC.md`), CONTRACT §5 (M1), §5.2, §8.2. Truth values: `spec/SAMPLE_CASE_TRUTHS.md`.
4	Binding product decisions: `memory/ORCHESTRATOR_DECISIONS.md` (D-001 to D-022); cited below by D-ID. Authority: golden outputs are `evals/golden/` (qa, T-015); the API is `memory/contracts/api.md` and `memory/DECISIONS.md` (architect, T-014). Where this file and either differ, §8 names the open card.
5	Design it must agree with: `docs/LLM_VS_CODE.md`, `memory/contracts/api.md`, `memory/DECISIONS.md`. ADR-017 in `memory/DECISIONS.md` reconciled the earlier differences (§8); what is still open is listed there.
6	Every later card and eval cites an R-ID from this file. If a card can't name the R-ID it serves, the card is wrong or this file is.
7	
8	**User.** A paralegal at a personal-injury firm. She reviews rather than trusts. Every statement the tool makes must be checkable against its source (A-101: she builds the chronology, the attorney signs the letter).
9	
10	**Two outputs, kept apart (D-001).** The export has two blocks and they never mix:
11	1. **Treatment section (paste into letter)**: accepted entries and accepted charges. Nothing else. It holds no tool-authored flag content (no flag type, title, reason, day count or count line). The records' own words can appear in it, but only inside an accepted excerpt (D-012), and block 2 tells the attorney which quotes carry flagged language.
12	2. **Internal review notes — do not send**: accepted flags, flagged language quoted in the letter, amounts not totaled, damages mentions, future treatment recommended, bills to request, records left out, edits, pending items, and a one-line AI-assistance statement (D-009).
13	
14	**Checkers.**
15	
16	| Checker | Meaning |
17	|---|---|
18	| **UT** | unit test under `tests/unit` (code only, no LLM) |
19	| **EV** | metric from `python -m evals.run` (golden set in `evals/golden/`, writes `evals/reports/latest.json`) |
20	| **E2E** | Playwright test under `tests/e2e` |
21	| **PR** | persona review file `reviews/<card>-<persona>.md`; pass = no blocker or major on that item |
22	| **INST** | `tools/install_test.sh` clean-clone timed run |
23	
24	Pass/fail wording is literal. "Pass" means the stated condition holds on every golden case unless one is named.
25	
26	**Vocabulary (D-013).** Flag types: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection suspicion). Lexicon types `causation_weakening` and `compliance` map to `causation`. States: `verified`, `needs_review`, `rejected`. Review statuses: `pending`, `accepted`, `edited`, `dismissed`.
27	
28	---
29	
30	## 1. Must-haves
31	
32	### 1.1 Input
33	
34	| ID | Requirement | Pass / fail test | Checker |
35	|---|---|---|---|
36	| R-IN-1 | Accept records pasted as text. | Pasting the 9 sample records produces 9 timeline entries and the UI shows "9 records found" before any model call. Fail if the count is wrong or not shown. | E2E + UT (splitter; pieces concatenated equal the input) |
37	| R-IN-2 | Accept records uploaded as a `.txt` file. No PDF or OCR (non-goal 1). | Uploading `evals/golden/sample.txt` gives the same 9 entries as paste. A `.pdf` upload is refused with a plain message, not a crash. | E2E |
38	| R-IN-3 | Date parsing is code, from an explicit format list. A numeric date is **ambiguous** when its first two numbers are both 1–12 and differ (`04/05/2026`: April 5 or May 4). It is never guessed, and no per-packet convention is inferred (non-goal 18). | Golden `case_01_date_formats`: seven formats parse (ISO, `02/17/2026`, `Feb 24, 2026`, `3 March 2026`, `March 10th, 2026`, `03-17-26`, `3/25/26`); `04/05/2026` is `date_ambiguous` with date null and `date_candidates` 2026-04-05 and 2026-05-04. Fail on any silent guess. | UT + EV (`case_01`) |
39	| R-IN-4 | Input size is bounded; empty or oversize input fails visibly without calling the LLM. | Empty input and input over `limits.max_chars` each show an error state; the LLM call counter stays 0. | E2E + UT |
40	| R-IN-5 | **Dates to confirm.** An entry with an ambiguous date is excluded from ordering and gap math, shown in a "Dates to confirm" group placed after the timeline (a `record_warning`), and is `needs_review`. She resolves it with the `confirm_date` action (R-RV-2), choosing one of the code-proposed readings. An undated entry sits in the same group with "no date found"; this build offers no way to type one in. | `case_01` record 8: absent from the timeline order until confirmed; after `confirm_date` 2026-05-04 it sorts into the timeline after 03-25. The gap table is unchanged because record 8 is a phone note (D-003 counts clinical encounters only). With no readings (no date found) an entry can't be confirmed and stays excluded. | UT + E2E |
41	
42	### 1.2 Timeline
43	
44	An **entry** is one timeline row: date, provider, one-line summary, exact source excerpt.
45	
46	| ID | Requirement | Pass / fail test | Checker |
47	|---|---|---|---|
48	| R-TL-1 | Entries are chronological, one per distinct source record (R-TL-7 covers duplicates), each with date, provider, one-line summary and excerpt. | Sample: 9 entries in date order, none of the four fields empty. Same-date records from different providers (records 1, 2) stay separate and keep source order (A-108). | UT + EV `entry_recall` |
49	| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/flag evidence and the excerpt-edit UI): the text up to and including a terminator, where a terminator is `.`, `?` or `!` followed by whitespace and then an uppercase letter, digit or end of text; `;`; or a line break. A period after an abbreviation on a fixed list (`approx.`, `Dr.`, `Mr.`, `Mrs.`, `Ms.`, `vs.`, `etc.`, `e.g.`, `i.e.`, `mg.`) or inside a number (`1.5`) is not a terminator. | UT: for every golden record, the units concatenated equal the record text, and `approx. 35 mph.` in record 1 is one unit. Grounding verifier passes every `verified` entry. An excerpt that is not verbatim is `rejected` (tray only, never timeline or export). An excerpt that starts or ends mid-unit is `needs_review`. | UT + EV `grounding_rate` |
50	| R-TL-3 | **Date of service is the record's header date, parsed by code.** Dates inside the body are facts for the conflict check, never the entry date. | Seeded test on **record 7**: header 2026-05-18, body "Date of accident per intake form: 2026-01-19". If the model returns 2026-01-19, the entry is `rejected` (`GROUNDING_DATE_MISMATCH`). Normal path: entry 7 dated 2026-05-18, sorted between entries 6 and 8. | UT + EV (`sample`) |
51	| R-TL-4 | **Summary adds nothing**: no fact, diagnosis, severity or causation absent from its excerpt. Judge #1 (faithfulness) checks every summary; `partially` or `unsupported` makes the entry `needs_review` with a one-sentence reason. | (a) Judge #1 returns `supported` on all 9 sample entries in each of 3 runs. (b) `hallucination_catch_rate` ≥ 0.95 over **every item in** `evals/golden/hallucinations.jsonl` (today 40, so at least 33 caught); the threshold is a rate, so it holds as the file grows. (c) Over **every control in** `hallucinations_controls.jsonl` (today 10) none returns `unsupported`. | EV |
52	| R-TL-5 | Every entry carries a state composed by code (ADR-005). `needs_review` sorts first in the review queue. | Unit tests cover the full composition table. E2E: a seeded `needs_review` entry appears above `verified` ones. | UT + E2E |
53	| R-TL-6 | "Why?" on every item shows the ladder record (generator output, code checks, judge verdict, state, backend) and the fixed-template one-sentence reason. | E2E: Why? on entry 7 shows check results and judge verdict; the audit record matches D.4 plus `backend`. | E2E |
54	| R-TL-7 | **Duplicate records are merged by code**: same date + same provider (case and whitespace normalized) + same normalized text → one entry citing every source record, with a visible "duplicate of record N" note. There is no split action (non-goal 16). | `case_04_duplicates_no_amounts`: 6 records give 4 entries, E1 cites records 1 and 2, E2 cites 3 and 4. Fail if 6 entries, or if a merged entry cites one record. | UT + EV (`case_04`) |
55	| R-TL-8 | **A hedge travels with its finding (D-018, D-021).** The **hedge set** is the lexicon entries with `hedge: true` in `app/llm/lexicon.yaml` (D-018); today `may_represent`, `correlate_clinically`, `possibility_terms`, `cannot_exclude`, `suggestive_versus_hedges`, `nonspecific_indeterminate`, `likely_alternative_cause`. When a selected sentence unit is qualified by a hedge unit, in the same unit or in the immediately following unit(s) of the same record, the hedge unit(s) must be in the excerpt, or the entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Other lexicon sentences (`pre_existing`, `compliance`, self-report) are **not** forced into the excerpt; they surface as flags. A unit is never cut (R-TL-2). | UT: the hedge set loads from `lexicon.yaml` (`hedge: true`), is non-empty and contains `may_represent` and `correlate_clinically`. Seeded entry 8 with excerpt "C5-C6 disc protrusion with mild right foraminal narrowing." → `needs_review` (`EXCERPT_OMITS_QUALIFIER`); with "…narrowing. Findings may represent degenerative change; correlate clinically." → `verified`. Entry 3 with excerpt "Persistent neck pain 6/10, daily headaches." and entry 5 with "Pain 4/10, improving." stay `verified` (their other sentences are `pre_existing` and damages wording, not hedges). Entry 6's default excerpt is checked by `entry_recall` (`must_contain_excerpt`: "Discharged from PT after two missed appointments"). | UT + EV |
56	| R-TL-9 | **Provider is the record's source label exactly as written (D-014), set by code.** Code copies the header/source label into the entry; the generator schema has no provider field, so a model can't supply or alter it (ADR-017). | UT: for every record in every golden file, the entry's provider equals the header label after whitespace normalization (record 4: "Capital PT, initial evaluation"). UT: the generator output schema has no provider field. Every provider and alias in the golden files must equal or be a substring of its record's label (qa, §8). | UT + EV |
57	| R-TL-10 | **Summaries keep the numbers and the qualifiers (D-006, D-022).** (a) A number, date, dollar figure or the word left, right, no, not or without in a summary must appear in the item's excerpt, the record's source label or its parsed date (token set: ADR-012 `grounding.new_tokens`) (so "visit 8" and a heading year don't trip it), or the entry is `needs_review` (`SUMMARY_TOKEN_NOT_IN_EXCERPT`). (b) If the excerpt contains a qualifier (a hedge, a self-report marker, a negation such as "without loss of consciousness", laterality, "approx.") and the **summary** omits it, the entry is `needs_review` (`SUMMARY_DROPS_QUALIFIER`). Both are code checks and don't rely on the judge. | UT: summary "pain 4/10" with excerpt "Pain 3/10." → `needs_review` (a). Summary "Diagnosed with concussion" for entry 2 → `needs_review` (b, drops "without loss of consciousness"). Sample entries pass, including "Visit 8: …" where "8" comes from the label "Capital PT, visit 8". Golden `required_terms` are checked against the summary alone (qa, §8). | UT + EV |
58	
59	### 1.3 Review flags
60	
61	Four types: `gap`, `conflict`, `pre_existing`, `causation`. Gap math is code over the header dates of clinical-encounter records (D-003): billing statements and phone notes are excluded, duplicates collapsed, ambiguous dates excluded, and the result does not change when the paralegal dismisses or edits an entry. Every flag shows its evidence.
62	
63	| ID | Requirement | Pass / fail test | Checker |
64	|---|---|---|---|
65	| R-FL-1 | **Treatment gap.** Flag when days between consecutive dates of service across all providers (A-102) is **greater than 30** (A-104). Only clinical-encounter records count (D-003): billing statements and phone notes are excluded. Evidence is the two bounding entries (date, provider, excerpt). | Sample: flag 2026-03-06 → 2026-05-18, 73 days, citing entries 6 and 7. No flag on 2026-01-23 → 2026-02-20 (28 days). `case_02_gap_boundaries`: 29 and 30 do not flag, 31 does (3 flags, 4 near-misses). UT: dismissing entry 6 leaves the gap flag and its days unchanged. | UT (29/30/31) + EV `flag_*[gap]` |
66	| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**, with the records cited (R-EX-4) and no choice made between the dates or any "delay from the accident" computed; the tool may state "first recorded treatment: January 9, 2026" (D-017); (b) PT plan of 12 visits (record 4) vs discharge at visit 9 after two missed appointments (record 6). `case_05_provider_conflict` raises its required flag and tolerates the name variants. | EV `flag_*[conflict]` + PR (legal-nurse) |
67	| R-FL-3 | **Prior / pre-existing conditions.** LLM classification plus lexicon scan; if only one fires, the flag is `needs_review` (`LEXICON_ONLY` or `LLM_ONLY`). | Sample must raise record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("degenerative change"). `case_06_subtle_pre_existing` is caught, and its 28-day near-miss does not flag. | EV `flag_*[pre_existing]` |
68	| R-FL-4 | **Language that weakens causation.** The tool quotes the wording; it never rules on causation. All five Appendix C items are `must` (K1–K5): records 8, 6 and 9, "New onset" in record 7, and the wrong accident date in record 7's intake line. Matching is one-to-one: each golden flag is satisfied by at most one tool flag, matched on type, cited records and overlapping evidence excerpt, so one record-7 flag about "new onset" can't also count for the intake date. | Sample: the tool emits a `causation` flag whose evidence is "New onset pain radiating to right arm" (K4) and a separate `causation` flag whose evidence is "Date of accident per intake form: 2026-01-19." (K5); the K5 line appears in the internal notes. Golden `must_not` every `must_not` item in `evals/golden` all pass (no "herniation", no "degenerative" in the tool's own voice, no "traumatic", no recovery claim). | EV `flag_*[causation]` + negative assertions + PR (claims-adjuster) |
69	| R-FL-5 | Every flag cites verbatim excerpt(s) that pass the grounding check. An ungrounded flag is `rejected`. | Verifier test on flags, same as R-TL-2. | UT + EV `grounding_rate` |
70	| R-FL-6 | Flags are grouped by type (four groups) with a fifth "Record warnings" group (dates to confirm, injection suspicion). Each shows its state and, when `needs_review`, a one-sentence reason. | E2E: the sample shows at least one flag in each of the four type groups; `case_01` shows a dates-to-confirm item; `case_07` shows an injection warning. | E2E |
71	| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion. | No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes. | UT + E2E |
72	| R-FL-8 | **Flag text is code (D-007).** Titles and explanations come from code templates. The LLM returns only the category and excerpt spans for a flag. | UT: the LLM output schema for flags has no free-text field; every flag title and explanation equals the template output for its type and computed values. | UT |
73	
74	### 1.4 Billed charges
75	
76	| ID | Requirement | Pass / fail test | Checker |
77	|---|---|---|---|
78	| R-CH-1 | List **every dollar amount** found, each with source record and verbatim excerpt. Extraction is code (currency pattern, money as whole cents). Noisy forms (`$1,2OO`) are listed as `unclear` with no value, never corrected. | Sample lists $6,240, $185, $2,150 and nothing else. `case_03_rate_and_ocr`: `$1,2OO` and `$9S.00` are `unclear`, value null. Amount recall ≥ 95% over `required` golden amounts. | UT + EV `amount_recall` |
79	| R-CH-2 | Each amount is classed `charge`, `rate`, `estimate`, `damages` or `unclear` (golden classes). **Code classifies, by explicit billing-phrase rules; there is no LLM amount classifier** (ADR-011). Judge #2 re-reads every classification, rule-made or not (D-004). A rate can never become a charge. | $6,240 and $2,150 → `charge`; $185 → `rate`; "missing 3 days of work" → `damages` (no value). UT: 20 phrasings of "Charge per visit $185" all classify `rate`. A rule-made class that judge #2 disputes → `needs_review` (`JUDGE_DISAGREES`). | UT + EV |
80	| R-CH-3 | **The total counts only accepted amounts of class `charge`.** The screen shows "Accepted charges: $X" and, separately, "Detected, not yet accepted: $Y (not a total)". Rates, estimates, damages and unclear amounts are listed as "unclear — not totaled" and never added. | Sample: after accepting both charges, Accepted = **$8,390**. Dismissing the ER charge drops it to $2,150. $185 reads "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review". **No PT total is computed** (golden `must_not` M4: none of 1,665 / 2,220 / 1,480 / 10,055 / 10,610 / 9,870 appears). | UT (totals) + E2E + EV |
81	| R-CH-4 | Non-billing figures are not charges. "Rx cyclobenzaprine 10 mg" and other doses never appear as amounts. | Golden `must_not` M7: no amount valued 10, 35, 6, 7, 12, 40 or 2. | EV |
82	| R-CH-5 | Amounts always need an explicit accept, even when `verified`. **Accepting a non-charge amount** (rate, estimate, damages, unclear) means "noted": it appears in the internal notes only, never in the letter or the total. An unreadable amount (`$1,2OO`, value null) can never count as a charge, accepted or not; its note reads "request clean copy of bill". | E2E: no amount reaches the letter or total without an accept click. Accept `$1,2OO` in `case_03` → it appears in the notes with "request clean copy of bill", not in `letter_text`, total unchanged. | E2E + UT |
83	| R-CH-6 | **Duplicate charges are merged by code**: same date + provider + amount → one amount citing every source record, with a visible "duplicate of" note. The total can never count it twice. There is no split action (non-goal 16). | Seeded unit test: the same $6,240 on 2026-01-09 from Central ER in two records → one amount; total after accept $6,240, not $12,480. | UT + E2E |
84	| R-CH-7 | **Charges are accept / dismiss only (D-010, ADR-017).** A charge's class comes from code and judge #2; the paralegal can't reclassify or edit it, so no path turns a rate, estimate or unreadable amount into a totaled charge. Reclassification is non-goal 15. | UT: any edit on a charge (amount, class, excerpt) → 422 `invalid_edit`; the review endpoint accepts only `accept`, `dismiss` and `reset` for amounts. After accepting the $185 rate the Accepted total is still $8,390 and `letter_text` has no $185. | UT + E2E |
85	
86	### 1.5 Review step
87	
88	An **item** is an entry, a flag or a charge. Everything starts `pending`.
89	
90	| ID | Requirement | Pass / fail test | Checker |
91	|---|---|---|---|
92	| R-RV-1 | Each entry and each flag can be **accepted, edited or dismissed**; each charge **accepted or dismissed** (D-010). Nothing is accepted by default. | E2E matrix: {accept, edit, dismiss} × {entry, flag} (6 cells) and {accept, dismiss} × {charge} (2 cells). Fresh load → all `pending`, letter block empty. | E2E |
93	| R-RV-2 | **What each action does (D-010, D-012).** See the table below the requirements. Originals are kept. "Edited" shows in the review UI and in the internal notes, never in the letter text. | UT, each → 422 `invalid_edit`: edit an entry's date or provider; edit a flag's evidence, type or title; edit a charge's amount or class; any other key. `confirm_date` (`POST /records/{rid}/confirm_date`): a date that is not one of the code-proposed readings → 422 `date_invalid`; a record with no readable date (no readings) cannot be confirmed. Also → 422 `invalid_edit`: an excerpt edit that is not a contiguous run of whole sentence units of the same record; an excerpt edit that drops a hedge-set unit (R-TL-8). `confirm_date` on `case_01` record 8 with 2026-05-04 → 200, a review event is logged, the entry joins the timeline. E2E: edit entry 3's summary → "edited" label in the UI; the letter shows the new summary with its citation and no "edited" mark; the notes list the original and the new text. | UT + E2E |
94	| R-RV-3 | **Edited text is re-checked.** The D-006 code check (numbers, dates, `$` in the new summary must appear in the excerpt) and judge #1 run on every edited summary and on every re-selected excerpt. If the code check or the judge objects (`partially`/`unsupported`), nothing is saved and the response is 409 `needs_confirm` with the reasons; if she chooses "keep my wording" the edit is resent with confirmation, saved, logged and shown in the internal notes. If the code check passes but the judge is unavailable (error, timeout, no recorded answer; always so in demo mode), the edit is saved as `edited` with state `needs_review` (`JUDGE_UNAVAILABLE`). | UT: summary edited to add "$9,000" → 409 `needs_confirm` (code token check). Seeded edit adding "herniation" → judge returns `partially` or `unsupported` → 409 `needs_confirm`. Resending with confirmation saves it. Judge unavailable → saved, `needs_review`, `JUDGE_UNAVAILABLE`. Structurally invalid edits are 422 `invalid_edit` (R-RV-2); judge or token objections are 409, never 422. | UT + EV (judge) + E2E |
95	| R-RV-4 | Review is keyboard-drivable (accept / edit / dismiss / next) and usable at 375 px. | E2E completes the sample case by keyboard only. At 375 px no horizontal scroll and every action is reachable. | E2E |
96	| R-RV-5 | Dismissed items never export to the letter and are recoverable (reset) until export. A dismissed flag may carry an optional reason. | E2E: dismiss, reset, dismiss again → absent from the letter and listed only under "dismissed" in the notes. | E2E |
97	| R-RV-6 | **No LLM output is auto-accepted. Record text is data (D-005).** A record with an injection warning forces all its items to `needs_review` (an advisory state, ADR-008), its amounts can't be charges, and it can't suppress flags from other records (the lexicon is the floor; the prior/causation flag pass runs per record, D-021). | Golden `case_07_prompt_injection`: the record produces an ordinary entry with an `INJECTION_SUSPECTED` warning, `needs_review`; no item's `review_status` changes and no flag is created resolved; the injected `$50,000` is never totaled (total stays $420). | EV + PR (privacy-compliance) |
98	| R-RV-8 | **Decisions survive a reload.** Accept, edit, dismiss, notes and `confirm_date` persist (SQLite) and restore on reload or reopen of the case. | E2E: accept 3 items, edit 1, reload → same statuses and the same Accepted total. | E2E |
99	| R-RV-9 | **Open the full source record from any item.** Entries, flags (both records for a two-record flag) and charges open the full record text with the excerpt highlighted, in a modal or panel. The highlight range comes from code offsets, not the model. If the offset can't be found, the item drops to `needs_review` and the UI says so. This is core; only the side-by-side layout is the stretch (§4). | E2E: from entry 8 open the record → the highlighted span equals the excerpt string. From the 73-day gap flag, records 6 and 7 both open. UT with a mutated record: offset lookup fails → `needs_review`. | E2E + UT |
100	
101	**R-RV-2 action table.**
102	
103	| Item | Accept | Edit allows | Edit never allows | Other |
104	|---|---|---|---|---|
105	| Entry | yes | summary text; re-selecting the excerpt as another contiguous run of whole sentence units of the **same** record (never dropping a hedge-set unit) | date, provider, record | `confirm_date` (below) |
106	| Charge | yes | nothing | amount, class, excerpt | dismiss |
107	| Flag | yes | a reviewer note (plain text, up to 500 characters, printed verbatim in the notes, labeled "reviewer note") | type, title, explanation, evidence | dismiss with optional reason |
108	
109	`confirm_date` is a separate review action, valid only for an entry whose date is `date_ambiguous`. Allowed values are the code-proposed readings only. It is logged as a review event with the previous state.
110	
111	*Withdrawn (D-011):* R-RV-7 (batch accept) is non-goal 14.
112	
113	### 1.6 Export
114	
115	Both blocks are assembled by code from items with `review_status` in {accepted, edited}. API: `GET /api/cases/{id}/export` returns `letter_text` and `internal_notes_text` separately.
116	
117	| ID | Requirement | Pass / fail test | Checker |
118	|---|---|---|---|
119	| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted `charge` amounts only. It holds no tool-authored flag content: no flag note, type label, title, explanation, day count, count line or AI-assistance line. Record words appear only inside an accepted entry's excerpt or summary. | E2E: accept all 9 entries, both charges and all flags, add a reviewer note to the gap flag. Assert `letter_text` contains none of: the reviewer note text, "REVIEWER NOTE", any flag type label, any flag title or explanation string produced from `sample.expected.json`'s flags, "73 days", "AI assistance", or any count line. UT: every line of `letter_text` is a fixed heading, a date + provider heading, an entry summary, a `Source` line whose quote is a substring of the accepted excerpt, an amount line or the total line; the letter builder takes no flags argument. Set equality: with a chosen subset accepted, the item IDs in `letter_text` equal that subset. | E2E + UT |
120	| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
121	| R-EX-3 | Chronological and deterministic: same accepted set → byte-identical `letter_text` and `internal_notes_text`. | UT: dates in `letter_text` are non-decreasing; export twice and compare. | UT |
122	| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
123	| R-EX-5 | The UI shows counts outside the copied text: "N entries, N charges in letter · N flags in internal notes · N of 9 records in letter · N items pending (N flags)". The count line is part of neither block. **Copy asks for one confirmation when anything is pending**, stating the pending numbers and naming pending flags separately (a pending flag may be one the attorney needs to see). | E2E: leave the 73-day gap flag pending, click Copy letter → the confirm reads "1 flag not reviewed"; the count line shows it. Click Copy for each block, read the clipboard, assert no count line in either. | E2E |
124	| R-EX-6 | **Template and worked example.** The letter follows the template in §6: US long dates ("January 9, 2026"), provider as written in the header, a `Source [Ex. __ / Bates __]:` line with the verbatim quote (the placeholder is literal text she fills in after pasting), money as `$1,234.00`, no dot leaders. The full expected export for the sample case is `evals/golden/sample.export.expected.txt` (qa, T-015), whose `LETTER_TEXT` and `INTERNAL_NOTES_TEXT` sections are §6's two blocks. | E2E on the **`fixture` backend** (recorded sample responses, so summary wording is fixed): with all 9 entries and both charges accepted and nothing edited, `letter_text` equals the golden file's `LETTER_TEXT` section and `internal_notes_text` equals its `INTERNAL_NOTES_TEXT` section, byte for byte (delimiter lines excluded). Every amount line and the total line match `\$[\d,]+\.\d{2}`; `Source` quotes are verbatim and exempt. No `..` run in the golden file. On a live backend the check covers structure only (R-EX-1, R-EX-2). | E2E + UT |
125	| R-EX-7 | **Reconciliation.** Every input record not represented in the letter is listed in the internal notes with its reason: rejected, dismissed or not reviewed. The UI shows "N of 9 records in letter" before copy. | E2E: dismiss entry 5 and leave entry 6 pending → notes list record 5 (dismissed) and record 6 (not reviewed); the on-screen count reads "7 of 9". | E2E |
126	| R-EX-8 | **The total line is exactly** `Billed charges accepted from these records: $X` (D-019, wording per D-062), where X is the sum of accepted `charge` amounts, formatted `$8,390.00`. **No parenthetical and no "excludes …" clause, ever.** Rates, estimates, unclear amounts, exclusions and injection-tagged amounts appear only in the internal notes ("Amounts not totaled"), because any clause built from unaccepted or injected amounts would leak into the carrier letter. | UT: on the sample the line equals `Billed charges accepted from these records: $8,390.00`. UT: with a non-dismissed rate, estimate or unclear amount present, and on `case_07`, the line is still exactly the template; `letter_text` contains none of "excludes", "supplement", "visit count", "rate". | UT + E2E |
127	| R-EX-9 | Two separate copy buttons, one per block, each copying exactly that block. | E2E: clipboard after each click equals the matching API field. | E2E |
128	
129	---
130	
131	## 2. Constraints
132	
133	| ID | Requirement | Pass / fail test | Checker |
134	|---|---|---|---|
135	| R-CO-1 | **LLM used for at least one step, and the line is documented.** `docs/LLM_VS_CODE.md` has the §5.2 table and matches the code. | Staff-engineer review checks each pipeline step against the table. UT: gap, total, date-parse, dedupe, sentence-splitter and export modules import no LLM client. | PR (staff-engineer) + UT |
136	| R-CO-2 | **Validation ladder on every LLM-derived item**: code check → independent judge (own prompt, preferably another model) → human accept/edit/dismiss. Nothing LLM-made reaches an export block without all three. | Audit record (D.4) exists for each LLM-derived item. E2E: an LLM-derived item with no human action is absent from both export blocks. | UT + E2E |
137	| R-CO-3 | **Nothing in the output that is not in the records.** | Ship bar items 1 and 4. On the sample case every `must_not` item in `evals/golden` holds (no fixed range), including: no disc herniation caused by the collision; "may represent degenerative change" not turned into "degenerative" or "traumatic"; no PT total; the two accident dates not merged; "concussion without loss of consciousness" kept as written. Any hit is a blocker. | EV (negative assertions) + PR (claims-adjuster) |
138	| R-CO-4 | **Runs from a link or from the repo in under 5 minutes.** The public link works without a key: public deployment is demo-only by default (D-008), replaying the cached sample run through the real pipeline code (A-002). In demo mode `POST /api/cases` accepts only text whose normalized hash equals a recorded fixture; anything else is rejected and not stored (D-020). Local mode (`ZLAYT_MODE=local`, loopback only) also admits the synthetic `evals/library` packets by exact hash (D-036). | `tools/install_test.sh`: clean clone to first screen with the sample loaded < 300 s. The public link opens with no login. | INST + PR (installer-reviewer) |
139	| R-CO-5 | **Synthetic data only**, shown on screen. | Banner "Synthetic data only — never paste real records" on every view (E2E). `python tools/check_secrets.py` passes. | E2E + UT |
140	| R-CO-6 | **Model and backend are swappable by config** (`claude-cli`, `anthropic-api`, `fixture`). A backend or prompt change requires an eval re-run with the report attached. | Unit tests run on `fixture` with no key. Handoff of any prompt/model change links an `evals/reports/*.md`. | UT + board check |
141	| R-CO-7 | **Determinism across 3 runs of the sample case, on a live-model backend** (`claude-cli` or `anthropic-api`; a `fixture` replay proves nothing). *Code outputs identical*: record split, parsed dates, entry-ID set, gap flags, amount list and classes from code, totals. *LLM-derived item states must match*: every entry, amount and flag has the same state in all 3 runs. *Flags are compared by (type, set of cited record IDs, evidence excerpt)*; the three runs must produce the same flag set. Summary wording may differ but must be `supported` in every run. | `determinism_3run` = 1.0 on `sample`; any difference fails and the report lists it. Other golden cases are reported, not gated. | EV |
142	| R-CO-8 | **Time-box and say what was cut.** | `memory/SCOPE_CUTS.md` has a row for every non-goal in §5 and §5 has an item for every row; the product note's "cut" section matches. | PR (product-manager) |
143	| R-CO-9 | Retries: at most 2 retries (3 attempts in all), each with changed conditions; failure is visible. | UT: the call fails on all 3 attempts → `LLM_FAILED_AFTER_RETRIES` and the item shows "could not process" with the reason, and the app stays usable; fails twice then succeeds → the entry is produced. | UT |
144	
145	---
146	
147	## 3. Part 1 submission items
148	
149	| ID | Requirement | Pass / fail test | Checker |
150	|---|---|---|---|
151	| R-SU-1 | Prototype link or repo with run instructions. README has a timed run path. | See R-CO-4. | INST |
152	| R-SU-2 | Demo ≤ 3 minutes, or annotated screenshots. Screenshots cover each of these states: input, processing, timeline with `needs_review` first, flags panel, charges with the unclear tray, edit with warning, source-record view, export (both blocks), "could not verify" tray, error/empty input. | `artifacts/demo.webm` duration ≤ 180 s (ffprobe). `artifacts/CAPTIONS.md` has one caption per listed state. | qa check |
153	| R-SU-3 | One-page product note. Checklist: the 7 required contents are present as headings (problem and user; what was built; what was cut and why; ship bar with 3–5 testable criteria, how tested, what was found; where AI can fail and how design handles it; model/code split; three metrics, each with a "tells you" line); exactly 3 post-launch metrics; renders to 1 page (≤ 650 words). Numbers in the note equal the latest eval report. | Checklist run by the writer self-check, then PR (hiring-panel, product-manager). | PR |
154	| R-SU-4 | **Which AI tools, and the prompts, unedited.** `submission/prompt-log/TOOLS.md` names tools, models and how the team was organized. The transcript export is produced by `tools/export_prompt_log.py` with no manual edits, plus a two-paragraph reading guide. | Re-run the exporter into a temp dir; `diff` against the submitted files is empty. `TOOLS.md` exists and names the tools and models. | qa check + PR (hiring-panel) |
155	| R-SU-5 | **Assumptions stated, links open.** The product note links the assumptions (A-101 to A-108 and any added); every link in the email draft opens without requesting access. | Checklist: note references `memory/ASSUMPTIONS.md` content; qa opens each submitted link in a logged-out browser. | PR + qa check |
156	
157	---
158	
159	## 4. Stretch pick: side-by-side source viewer
160	
161	**Chosen.** The two-pane layout. Left, the item queue. Right, the full source record, always visible, scrolled to the highlighted excerpt as she moves through the queue. Opening the full record (modal or panel, highlight by code offsets) is already core (R-RV-9), so what the stretch adds is the layout that removes the open-and-close step.
162	
163	**Why (3 lines).**
164	1. The spec says she "reviews rather than trusts." Each claim sits next to its context with no extra click per item, which is what about 20 decisions per case need.
165	2. A quote can mislead by omission (the MRI line without its hedge). R-TL-8 stops the tool from dropping the hedge; the viewer lets her see the rest of the record anyway.
166	3. It is cheap: the highlight range already comes from the grounding check, so there is no new LLM step.
167	
168	**Why not the others.** PDF upload puts unverifiable extraction upstream of the grounding check. The confidence indicator already ships as `verified / needs_review / rejected`. A firm-voice paragraph is generated prose that would need its own verification.
169	
170	**Cut rule.**
171	- **Start** only when every M3 must-have card is done with no open blockers, and M3 is inside its 3.5 h budget. The stretch is built before the M3 gate so the gate reviews it.
172	- **Stop** at 45 minutes, or when the M3 gate is due, whichever comes first.
173	- **Fallback (one):** cut it entirely. The core record modal from R-RV-9 stays and nothing else changes. Log the cut in `memory/SCOPE_CUTS.md`.
174	
175	| ID | Requirement | Pass / fail test | Checker |
176	|---|---|---|---|
177	| R-ST-1 | At viewport ≥ 1024 px the source record sits beside the queue; selecting an item scrolls the record to its highlighted excerpt without opening a modal. Below 1024 px it falls back to the R-RV-9 modal. | E2E at 1280 px: step through three items by keyboard; the record pane updates each time and the highlighted span equals the excerpt. At 375 px the modal opens instead. | E2E |
178	
179	**M3 cut order if M3 passes 100% of its budget** (each cut is logged in `memory/SCOPE_CUTS.md`):
180	1. R-ST-1, the side-by-side layout.
181	2. Excerpt re-selection (R-RV-2): edit becomes summary text only. Entries can still be dismissed, and the notes still list flagged language.
182	3. R-EX-4 sections 7 and 8 (future treatment, bills to request).
183	4. R-RV-9 drops to an inline full-record expand with no highlight; the highlight check stays in the E2E as a *should*.
184	
185	---
186	
187	## 5. Non-goals
188	
189	These are out on purpose. The orchestrator logs each in `memory/SCOPE_CUTS.md` with the reason; R-CO-8 checks that the two lists match.
190	
191	1. **PDF upload and OCR.** Text only. Extraction errors would sit upstream of the grounding check. Pasted PDF text with page headers is a chaos-test input, not a feature.
192	2. **Multi-case and matter management.** One case at a time, no search across cases, no case list.
193	3. **Accounts, auth, roles, sharing.** One anonymous session.
194	4. **Real data or PHI handling.** Synthetic only. No HIPAA, retention or BAA claim. The privacy review checks the design for what a real build would need; the prototype doesn't implement it. After launch a test set may be built from real work product, but only inside the firm's environment, attorney-approved and access-logged (D-016); this repo stays synthetic.
195	5. **Drafting demand-letter prose in a firm's voice.** Export is a structured treatment section from accepted items. No generated narrative, no advocacy language.
196	6. **Medical or legal judgment.** No diagnosis, severity rating, causation opinion or statement of what a record "means." Flags point at the record's own words. Whether a flagged sentence goes out in the letter is the attorney's call (D-012), not the tool's. The tool never picks between conflicting accident dates and never computes delay from the accident (D-017).
197	7. **Billing analysis.** No PT total from a rate, no reasonableness of charges, liens, insurance adjustments or paid-vs-billed.
198	8. **Integrations.** No EHR, case-management or document-system connectors, no email intake.
199	9. **Per-user learning.** Dismissals are logged for metrics, not fed back into prompts.
200	10. **Numeric confidence scores.** Three states only. A made-up percentage implies precision we can't verify.
201	11. **Non-English records and handwriting.** The chaos test confirms a clear failure message, not support.
202	12. **Manually adding an entry for a record the pipeline rejected.** The record stays in the "could not verify" tray; she writes that entry herself (SCOPE_CUTS 12).
203	13. **LLM fallback for splitting records** (SCOPE_CUTS 13). An unsplittable paste becomes one record, marked uncertain.
204	14. **Batch accept.** Every item takes an individual decision (D-011; SCOPE_CUTS 14).
205	15. **Charge reclassification.** A charge is accepted or dismissed; its class comes from code and judge #2, and a rate can never become a charge (D-011; SCOPE_CUTS 15).
206	16. **A "not a duplicate" split action.** The duplicate merge stays, visible with a "duplicate of" note (D-011; SCOPE_CUTS 16).
207	17. **Smaller cuts (D-011; SCOPE_CUTS 17).** LLM date pointing, bring-your-own-key, the full-prompt audit view, edits to flag titles or explanations, a case list.
208	18. **Per-packet date-convention inference.** An ambiguous numeric date always asks once, even when the packet has `02/17/2026` elsewhere; golden `case_01` expects exactly that. Inferring the convention would cut confirmations and add a silent-guess risk; it needs its own eval first.
209	19. **Exhibit and Bates numbering** (SCOPE_CUTS 19). The export carries an `[Ex. __ / Bates __]` placeholder she fills in; the tool assigns no numbers.
210	
211	---
212	
213	## 6. Export template and worked example (R-EX-6)
214	
215	Sample case, all 9 entries and both charges accepted, nothing edited, all flags accepted. Summaries are one line, written from the excerpt only. Dates are US long form in the export; the UI and API keep ISO. `[Ex. __ / Bates __]` is literal text. The qa golden file `evals/golden/sample.export.expected.txt` is this text.
216	
217	**Block 1 — Treatment section (paste into letter)**
218	
219	```
220	TREATMENT CHRONOLOGY
221	
222	January 9, 2026 — Austin EMS run report
223	Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
224	Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
225	
226	January 9, 2026 — Central ER discharge summary
227	Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
228	Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
229	
230	January 16, 2026 — Dr. Alvarez, primary care
231	Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
232	Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
233	
234	January 23, 2026 — Capital PT, initial evaluation
235	Cervical range of motion reduced approx. 40%; plan of care 12 visits.
236	Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
237	
238	February 20, 2026 — Capital PT, visit 8
239	Pain 4/10, improving.
240	Source [Ex. __ / Bates __]: "Pain 4/10, improving."
241	
242	March 6, 2026 — Capital PT, visit 9
243	Discharged from physical therapy after two missed appointments; pain 3/10.
244	Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."
245	
246	May 18, 2026 — Hill Country Pain Management, new patient
247	New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
248	Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
249	
250	May 29, 2026 — Austin Imaging, cervical MRI
251	C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
252	Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
253	
254	June 12, 2026 — Hill Country Pain Management, follow-up
255	Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
256	Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
257	
258	BILLED CHARGES
259	
260	Central ER discharge summary, January 9, 2026: $6,240.00
261	Source [Ex. __ / Bates __]: "ER charges: $6,240."
262	Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
263	Source [Ex. __ / Bates __]: "Charge: $2,150."
264	
265	Billed charges accepted from these records: $8,390.00
266	```
267	
268	**Block 2 — Internal review notes — do not send**
269	
270	```
271	INTERNAL REVIEW NOTES — DO NOT SEND
272	
273	This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
274	
275	FLAGS ACCEPTED
276	- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
277	- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
278	- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
279	- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
280	- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
281	
282	FLAGS DISMISSED
283	- none
284	
285	FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
286	- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
287	- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
288	- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
289	- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
290	- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
291	- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
292	
293	AMOUNTS NOT TOTALED
294	- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
295	
296	DAMAGES MENTIONS (not charges)
297	- Record 5 (Capital PT, visit 8, February 20, 2026): "Patient reports missing 3 days of work."
298	
299	FUTURE TREATMENT RECOMMENDED (no cost stated)
300	- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.
301	
302	BILLS TO REQUEST (entry in the letter, no accepted charge)
303	- Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.
304	
305	RECORDS NOT IN THE TREATMENT SECTION
306	- none (9 of 9 records included)
307	
308	EDITED ITEMS
309	- none
310	
311	PENDING ITEMS NOT INCLUDED
312	- none
313	```
314	
315	If entry 5 were dismissed: the letter skips February 20, and "RECORDS NOT IN THE TREATMENT SECTION" reads "Record 5 (Capital PT, visit 8, February 20, 2026) — dismissed." The chronology never silently closes up.
316	
317	---
318	
319	## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
320	
321	These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.
322	
323	| # | Criterion (CONTRACT §8.2) | Number | Measured by | Run with | R-IDs |
324	|---|---|---|---|---|---|
325	| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
326	| 2 | **Recall** | ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set | `entry_recall`, `amount_recall` | `python -m evals.run` | R-TL-1, R-TL-7, R-CH-1 |
327	| 3 | **Flags** | Per flag type (gap, conflict, pre_existing, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
328	| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations.jsonl` (today 40, so at least 33). CONTRACT §5 M2 still says "qa injects 20"; the rate governs permanently and the product note quotes the rate. Seeded J3/J4 control sets must also catch every seeded wrong item with 0 false agrees (D-046). | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
329	| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` (1–5, D-015) ≥ 4; `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag content; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-6, R-RV-8, R-RV-9, R-EX-1 to R-EX-9 |
330	
331	Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).
332	
333	Rule for the product note: report what the eval **found**, including misses, not just the targets.
334	
335	---
336	
337	## 8. Assumptions and the hand-off list
338	
339	### Assumptions this depends on
340	
341	Live list: `memory/ASSUMPTIONS.md`.
342	
343	| Ref | Assumption | Requirements that break if it's wrong |
344	|---|---|---|
345	| A-001 / A-002 | Dev runs on `claude-cli`; reviewers get demo mode with cached sample output and no key. | R-CO-4, R-CO-6 |
346	| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1, R-EX-4 |
347	| A-102 | A gap is measured between consecutive dates of service across all providers. | R-FL-1 |
348	| A-103 | The chronology feeds the medical-treatment section of a pre-suit demand letter to a carrier. | R-EX-1 to R-EX-8 |
349	| A-104 | "Longer than 30 days" is strict: 30 is not a gap, 31 is. | R-FL-1 |
350	| A-105 | Each pasted record carries its date and source on its first line or table row; undated or ambiguous records go to "Dates to confirm". | R-IN-3, R-IN-5, R-TL-3 |
351	| A-106 | The export cites each line by provider as written in the header + date of service with an `[Ex. __ / Bates __]` placeholder; the tool assigns no numbers; internal notes cite `record N (provider as written, date)` per R-EX-4 | R-EX-2, R-EX-4, R-EX-6 |
352	| A-107 | A per-visit rate is not billable until visits are itemized, so no PT total is shown. | R-CH-2, R-CH-3, R-EX-8 |
353	| A-108 | Same-day records from different providers stay separate entries. | R-TL-1, R-TL-7 |
354	
355	**Team decisions, not yet in `ASSUMPTIONS.md`** (Chris can override through the NEEDS_CHRIS FYI list):
356	- The date of service is the record's header date. Body dates are conflict evidence only (R-TL-3).
357	- Accepting a flag means "I've seen it and it's real," not "send it to the carrier." Flags go to the internal notes only (D-001). A flagged record sentence can still appear in the letter inside an accepted excerpt; the notes list those so the attorney decides (D-012).
358	- Numeric dates whose first two numbers are both 1–12 and differ are ambiguous even though Texas records are normally month/day; she confirms once per date (R-IN-3, non-goal 18).
359	- Providers with an entry in the letter but no stated charge are "bills to request" (R-EX-4).
360	- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).
361	
362	### Reconciliation status
363	
364	Everything above follows `memory/ORCHESTRATOR_DECISIONS.md` (D-001 to D-024). **Authority rule:** `evals/golden/*` is the authority on expected outputs, and this file matches it. §6 block 2 equals the golden `INTERNAL_NOTES_TEXT` block and §6 block 1 equals `LETTER_TEXT`; the writer asks qa for no golden changes. `memory/contracts/api.md` and `memory/DECISIONS.md` are the authority for the API and are aligned to this file and the golden by the architect on **T-028**. Each row has a grep that shows the difference.
365	
366	| # | File | Difference | Check | Owner |
367	|---|---|---|---|---|
368	| 1 | `memory/contracts/api.md` export example | The example references `evals/golden/sample.export.expected.txt` instead of copying it (one source of truth). | `grep -n "sample.export.expected.txt" memory/contracts/api.md` (expect ≥ 1) | T-028 | resolved |
369	| 2 | `memory/contracts/api.md` reason codes | No `SUMMARY_DROPS_QUALIFIER` (D-022, R-TL-10(b)); `EXCERPT_OMITS_QUALIFIER` reads "the record has a hedge sentence the excerpt leaves out", D-021 limits it to a hedge that qualifies a selected sentence. | `grep -c "SUMMARY_DROPS_QUALIFIER" memory/contracts/api.md` (expect 1 or more) | T-028 (architect) |
370	| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
371	| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
372	| 5 | M3 paralegal review brief (orchestrator, T-018/M3 gate) | `scores.verify_quickly` (D-015) must be requested in the brief. | `grep -c "verify_quickly" .claude/agents/paralegal-reviewer.md` (expect 1 or more) | T-016 (orchestrator) |
373	| 6 | `docs/CONTRACT.md` §5 M2 | "qa injects 20"; closed as permanent. The ship bar here is a rate over the file and the product note quotes the rate. CONTRACT is never edited. | none | closed |
374	
375	Already aligned, checked at this commit: `memory/ASSUMPTIONS.md` A-106 matches R-EX-4 (provider + date; record numbers appear only in the internal notes) and R-EX-6; `memory/SCOPE_CUTS.md` rows 1–19 match §5 non-goals 1–19; the golden letter block has no parenthetical on the total line.
376	
377	## 9. Traceability pointers
378	
379	- LLM/code table and ladder: `docs/LLM_VS_CODE.md`. Names used here: generator, judge #1 faithfulness, judge #2 amount classification, judge #3 conflict, states `verified | needs_review | rejected`.
380	- Golden set: `evals/golden/` (qa). Expected values: `spec/SAMPLE_CASE_TRUTHS.md`. Every metric above must be computable from it.
381	- Cards cite R-IDs in their AC text. `evals.run` report rows carry the R-ID next to each metric.
382	- The withdrawn ID R-RV-7 (batch accept, D-011) is not reused.
383	
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:14.787Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md"
}
````

### User / tool · 2026-11-02T19:59:14.934Z

**tool result**
````
1	# ORCHESTRATOR DECISIONS (orchestrator is the sole writer)
2	
3	Cross-cutting product decisions made while triaging reviews. The architect mirrors the technical ones into ADRs
4	(memory/DECISIONS.md); the writer mirrors the product ones into spec/REQUIREMENTS.md. Each: decision · why · source review.
5	Questions that are really Chris's are in submission/NEEDS_CHRIS.md with the assumption we act on.
6	
7	| ID | Decision | Why | Source |
8	|---|---|---|---|
9	| D-001 | Export = two blocks: **Treatment section** (paste into letter: accepted entries + accepted charges) and **Internal review notes — do not send** (accepted flags, unclear amounts, records not included, bills to request, damages mentions, AI-assistance line). Flag notes/labels/counts never enter the letter. | Accepting a flag means "I've seen it", not "tell the carrier". | T-013 paralegal r1 (blocker) |
10	| D-002 | Every letter line carries a verbatim quote + provider as written + date of service (US long format) + citation placeholder `[Ex. __ / Bates __]`. No short-cite mode. | Ship bar #1 (100% grounded export); adjusters cross-check providers. | T-014 staff-eng F1, privacy B2 |
11	| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
12	| D-004 | *(Partly superseded: guarded charge reclassification reinstated by D-042 (T-084); totals replaced by a cited line listing, D-052.)* Amounts: code extracts and classifies with explicit billing-phrase rules; judge #2 validates every classification; a rate can never become a charge; running total = accepted charges only; "detected" is shown separately and labelled not-a-total. Total line wording: "Billed charges stated in these records: $X". | Texas paid-or-incurred (§41.0105) — never "damages"; no PT total from a rate. | T-014 privacy B1; research T-008 |
13	| D-005 | Any record carrying an injection warning forces all its items to needs_review; its amounts can't be charges; it can't suppress flags from other records (lexicon is the floor). | Injected "$50,000" reached the total via code path alone. | T-014 privacy B1 |
14	| D-006 | Numbers/dates/$ in a summary or a user edit must appear in that item's excerpt (code check) or the item is needs_review with a reason. | Don't rely on the judge for swapped numerals. | T-014 staff-eng F5, privacy |
15	| D-007 | Flag titles/explanations are code templates; the LLM returns only category + excerpt spans. | No free LLM prose in the attorney's notes. | T-014 staff-eng F8, privacy |
16	| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
17	| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. (Listed under "Decided by the team" in NEEDS_CHRIS.) | Candor without telling the carrier how the chronology was made. | T-014 privacy |
18	| D-010 | Edits: entry = summary text only; charge = accept/dismiss only (no reclassification, no amount edit); flag = reviewer note only. Ambiguous dates are resolved with a separate `confirm_date` action (choose one of the code-proposed readings), not an edit. Originals are kept; "edited" shows in UI + internal notes. | Keep code-owned facts code-owned. | T-013 PM r2 (major 1, 2) |
19	| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-have. | T-013 PM r2, T-014 staff-eng F12 |
20	| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged language may appear in the letter **only** as part of an accepted excerpt, and the internal notes list "flagged language quoted in the letter" so the attorney decides. NEEDS_CHRIS #10. | The records' own words are the record; hiding them is the attorney's call, not the tool's. | T-013 paralegal r2 M1/M2, PM r2 M3/M4 |
21	| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
22	| D-014 | Provider = the source label exactly as written in the record header; golden aliases must match header text. | Grounding (R-TL-9). | T-013 PM r2 |
23	| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
24	| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreaker. | Part 2 area 4 asks for it; Texas Op. 705 allows confidential info in AI tools with precautions. | T-010 litigation-lead Q |
25	| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
26	| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
27	| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28	| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29	| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30	| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31	| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
32	| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
33	| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
34	| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
35	| D-027 | Two-digit years are never guessed: `03-17-98` is `date_ambiguous` with candidates (1998, 2098) and excluded from gap math until confirmed. Text outside recognised record blocks is never dropped: it becomes an 'unsplit text' record flagged for the paralegal. | 'Say so instead of guessing' (spec); silent drops lose facts. | T-032 staff review |
36	| D-028 | Judges return a verdict enum plus a `reason_code` from a closed list (e.g. ADDS_DIAGNOSIS, ADDS_SEVERITY, ADDS_CAUSATION, DROPS_QUALIFIER, NUMBER_MISMATCH, OTHER_UNSUPPORTED); no free-text reason. The UI's Why? renders the code through a code template. | Model prose must not reach the attorney or the UI (consistent with D-007); ADR-008.5 enum-only. | T-035 staff review (Chris Q answered by orchestrator) |
37	| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
38	| D-030 | Flag evidence is the **verbatim phrase span** that triggered the flag (lexicon match or LLM-returned span), e.g. "Findings may represent degenerative change", "New onset pain" — not the whole sentence. Entry excerpts stay whole sentences (D-021). Internal notes quote flag spans; the golden notes block is the authority. | Precise flag quotes; matches the hand-written golden; entries keep context. | T-051/backend-4 |
39	| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
40	| D-032 | Narrows D-018: normal/negative findings (`objective_negative`: 'negative for fracture', 'WNL', 'full ROM') are **context only, never flags**; `scene_facts` raise a causation flag only on specific adjuster phrases ('minimal damage', 'refused transport', 'ambulatory at scene', 'no airbag deployment'), never on a plain mechanism description ('Cyclist struck by a car'). | First eval: causation precision 0.5 from these two categories; golden case_05 must_not N2. | T-038 eval report 20261102T020824Z |
41	| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
42	| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit or manual entry that is not in that item's excerpt (or its source label/parsed date) is a **hard 422** — no 'keep my wording' override. The 409 confirm path remains only for non-numeric judge objections, and any override is listed in internal notes ('reviewer override: <reason code>'). | An override let 'Pain 9/10' into the letter against a 4/10 quote — an invented fact. | T-056 paralegal review |
43	| D-035 | Simplifies D-033: `patient_report` is attached only to a **clause** that begins with an explicit patient subject ('Patient', 'Pt', 'The patient') followed by a reporting verb (states, reports, notes, says, endorses, complains of, c/o, denies); the tag spans that clause only (to the next ';' or sentence end). Everything else — EMS, family, any other or unknown speaker, header labels — gets **no tag**. Default is no tag: a missing chip is safe, a wrong chip is not. | Speaker-list regexes kept missing new speakers (girlfriend, co-worker). | T-061 r2 |
44	| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
45	| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
46	| D-038 | Narrows D-032 (2026-11-02): normal or negative objective findings stay context-only, but defense **credibility phrases** from the lexicon (e.g. 'Waddell signs', 'out of proportion', 'symptom magnification', 'non-physiologic', 'inconsistent effort') raise a flag so the paralegal sees them before the adjuster does. | These are what an adjuster quotes against the claimant; hiding them defeats the prep purpose. | T-063 staff r1 major 6 |
47	| D-039 | Re-run with decided items (2026-11-02): once any entry in a case is accepted, edited or dismissed, the case's records are frozen. A re-run reuses the stored records and never re-splits, so decided items keep their record ids and excerpts. Re-splitting is allowed only while every entry is still pending. | Provenance of an accepted item is what the paralegal verified against; it must never silently move. | T-057 staff r3 blocker |
48	| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
49	| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
50	| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51	| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52	| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53	| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
54	| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
55	| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
56	| D-048 | Language routing fails safe (2026-11-02, after T-085 r2): a record or line runs as English only when it is **confidently English** (enough English function and clinical words, and no non-English evidence). Everything else is Spanish if confidently Spanish, otherwise LANGUAGE_UNCERTAIN: needs_review, labeled, and never passes on English token checks alone. On mixed lines, the English **and** Spanish token and qualifier checks both run (union), so a dropped 'posible' is caught whichever language leads. Routing gets a held-out measurement set. | Two rounds of heuristic detection let fresh Spanish and other-language lines through as unlabeled English. | T-085 legal-nurse r2 |
57	| D-049 | Billing completeness is decided by a code accounting pass (2026-11-02, after T-083 r3): every money-shaped token in a billing record ($-prefixed, a number with two decimals, or a no-cents figure in an amount column) must be accounted for as a parsed row, an unreconciled line, an excluded rate or an on-row 'unclear'. If any token is unaccounted for, the provider is complete: false and the record is listed. Repeated summary rows (e.g. two balance-forward lines) are all listed, never overwritten. On-row 'unclear' with complete: false is acceptable (nothing is lost). | Three rounds of per-format parsing still let bare figures vanish with complete: true; a token-level accounting pass makes silent loss impossible regardless of format. | T-083 staff r3 |
58	| D-050 | Non-English is never auto-verified (2026-11-02, §7.4 after T-085 r3): every item from a record routed Spanish or LANGUAGE_UNCERTAIN is needs_review with the label 'AI translation — check against the original'. The Spanish code checks and the translation judge still run and their failures are shown, but passing them never yields 'verified'. The paralegal's accept is the gate. English routing keeps its normal ladder. | Three rounds showed heuristic Spanish/Portuguese/Italian routing and cue lists keep leaking (4/41 dropped hedges, 1/27 misroutes on fresh lines); making the human the only verifier for translated text removes the silent-pass risk instead of chasing word lists. | T-085 legal-nurse r3 |
59	| D-051 | Code checks bind accept for **every** item (2026-11-02, T-098 review blocker): an item whose current summary fails any D-034/D-047/D-022 code check (e.g. an AI draft 'Pain 5/10' over a quote without 5/10) cannot be accepted, single or batch (422 with the reason; the paralegal must edit it to match the quote), and the export gate blocks it if such a state exists anyway. Only the judge step is exempt for human wording (D-045b); the code rung never is. | A one-click accept exported an invented number. | T-098 staff r1 F1 |
60	| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complete' badge are computed or shown. The existing case-level charge total (D-019, stated charges only) is unchanged. | Five review rounds kept finding ways a per-provider total could silently omit or overwrite a figure; a listing cannot hide a missing line. | T-083 staff r5 |
61	| D-053 | Nothing the model proposes is silently dropped (2026-11-02, T-094 review blocker). A model-only flag or conflict that the judge rejects, or a model-proposed conflict that no code candidate confirms (the no-candidate rule applies to conflicts only; ADR-020), goes to the **could-not-verify tray** with the judge's reason; it is never a flag and never reaches the letter. The eval scores precision on emitted flags only (tray items are not assertions), and reports tray counts separately; R-CO-7's flag-set signature covers flags, not tray items. Conflict candidates from code (T-094) remain the only path to a conflict *flag*; recall gaps in the code rules are listed in SCOPE_CUTS until covered. | Suppressing rejected items to raise precision hid model output from the paralegal, against R-FL-3 and the ladder. | T-094 staff r1 |
62	| D-054 | Summary clauses the quote does not support are removed by code (2026-11-02, after T-094 r2). Before judging, code splits an AI summary into clauses; a clause is removed only when it adds salient content the excerpt lacks: a number or month, a side or a negation (only in a clause sharing no content word with the excerpt), or a procedure/device/drug, body-part or diagnosis term not covered by a word of the same family in the excerpt (amended T-112 r2: faithful paraphrases and abbreviation expansions stay; whole clauses only, never leaving a fragment; e.g. 'splint fitted' when the excerpt is only the pain sentence is removed), and the removal is shown in the item trace ('removed from the summary: not in the quote'). If nothing supported remains, the item goes to the could-not-verify tray. The judge then checks what is left. No prompt change, no fixture re-record. | Ship-bar item 4 flapped ~1 run in 3 on case_02 because the model sometimes summarized beyond its own excerpt; trimming by code is deterministic and keeps 'every statement traces to a verbatim excerpt'. | T-094 r2 handoff |
63	| D-055 | Gaps never exclude records by guessing (2026-11-02, after T-116 r2). Gap endpoints are computed over all dated records, as before T-116. When a gap starts or ends at a record that looks administrative (intake form, records request, bill, affidavit, by header), the gap carries a visible warning ('this gap ends at an intake form, not a visit; check whether treatment continued') and the paralegal decides. No record is silently dropped from gap math. | Two rounds of label heuristics still excluded real visits (', fax', 'records request' in a visit label), inventing gaps; a warning cannot invent a gap. | T-116 paralegal r2 |
64	| D-056 | Amends D-029 (2026-11-02, T-115): curated fixtures may hand-shape extraction and narrative outputs for the demo, but **judge answers are never scripted**: every judge answer the demo or eval replays is a real recorded model output, and a curated file may never shadow a recording for the same key. tests/unit/test_curated_fixtures.py enforces it (empty allow-list). | Scripted judge answers make the ladder's second check fictional; four had been written by hand, one overriding a real recording. | T-115 staff r1/r2 |
65	| D-057 | Rule-filtered model proposals are listed, not dropped (2026-11-02, after T-113). A model-proposed flag that a code rule filters out (e.g. D-032 `objective_negative`: a normal finding is not a flag) goes to a collapsed, counted "Filtered by rule" group in the could-not-verify tray with the rule named; it is never in the timeline or letter and needs no action. | D-053 says nothing the model proposes is silently dropped; trays full of normal findings would be noise, so they are listed collapsed with a count. | T-113 backend question |
66	| D-058 | A re-picked quote does not make the AI summary human-authored (2026-11-02, T-134 r3 / T-136 F-2). When she picks a different quote but keeps the AI summary, the summary is still LLM-made and its judge ran on the old quote, so D-044 still applies: the new summary–quote pair needs judge 1, and her "I compared it with the quote" does not replace it. If the judge cannot answer, the item stays out of the letter and the UI says so and names the way out (write the summary herself, which makes it human text under D-045). | The ladder rule: nothing LLM-made reaches the export without code check, independent judge and human. | T-134 r3 backend question |
67	| D-059 | The letter total is built only from charges a human accepted one at a time (2026-11-02, T-140 adjuster fail). (1) Charges are never batch-accepted. (2) Code marks an amount `unclear` (not totaled, listed in internal notes with its reason) when its line or column label says total/subtotal/balance/balance forward/previous statement/year-to-date/amount due/paid/payment/adjustment/write-off/credit, when it carries a CR suffix or a negative sign, or when it comes from an insurer document (EOB/remittance) restating a provider charge. (3) Code flags a likely duplicate (same date, description and amount on two statements) and a likely total (equals the sum of other charges); such a charge can be accepted only through a confirm step that names the flag. The total line stays (R-EX-8) and sums exactly the accepted charges. | Totals from ledgers failed adversarial rounds whenever accept-all could include restated amounts; one-at-a-time acceptance plus code flags keeps the human as the final check without removing the total paralegals need. | T-140 claims-adjuster r1 |
68	| D-060 | Amends D-059 (2026-11-02, T-140 adjuster r2): charge candidates are **default-deny**. An amount can be class `charge` only when it sits on an itemized service line: a date of service, a service description (CPT/HCPCS/revenue code or a service noun) and the amount on the same line or table row, in a provider bill or ledger. Every other amount (statement-level labels, account summaries, 'last statement', year-to-date, payment history, insurer documents, unlabeled figures) is `unclear` with its reason. Duplicates are matched on normalized date of service + service + amount (any date format). A charge cites its own line by offset, never by text search. | Deny-lists of total/balance wording lost every adversarial round; listing what a charge must look like cannot be outworded. | T-140 claims-adjuster r2 |
69	| D-061 | Pre-accident records: one simple rule (2026-11-02, T-141 after 5 rounds). A record dated before the stated accident date is info-only ONLY when every accident/mechanism word in it is governed by an explicit "prior/previous/earlier" or a negation of prior accidents ("no prior accidents", "denies previous MVA", "Prior accidents: No"). Any other accident or mechanism word, noun or verb (accident, collision, crash, MVC/MVA, rear-end(ed), struck, hit, pedestrian, impact), with or without a date or "last year", makes it a date conflict. No date-distance exemptions. Second closed exemption (accepted after T-141 implementation): a PLURAL accident noun under a history label ('History per patient: car accidents in 2019 and 2022') names several earlier events, not the accident, and is info-only; a singular one ('History: MVC', 'History: rear-ended') is a conflict. A false conflict is the safe direction (D-055). | Five rounds of word-level exemptions kept hiding true conflicts; one closed exemption cannot be outworded. | T-141 r1–r5 |
70	| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the total. Charge sources are positively identified: only documents with a billing header (itemized statement, ledger, invoice, UB-04, CMS-1500) can yield a `charge`; clinical notes and discharge summaries yield a charge only from an encounter line, and never once the case holds an itemized bill from the same provider (amended at implementation: a literal ban zeroed the sample, whose charges are stated in visit notes); insurer and unknown documents never can. CPT/HCPCS codes are normalized ('CPT 99213' = '99213') before duplicate matching. Residual: a summary row dressed as a service line can still be accepted by a careless reviewer; it is cited and individually accepted, and listed as accepted debt. | An adversary can always word a ledger past a classifier; the honest claim is a sum of human-accepted, cited lines. | T-140 claims-adjuster r3 |
71	| D-063 | Priority switch (Chris, 2026-11-02): finish a polished MVP. Only P0 cards and UX/UI work proceed; every other non-P0 card is held (blocked with a note) until the MVP is done. In-flight P1 cards finish their current round but get no further rounds unless they block the UI. New review rounds on held areas are not opened; residuals go to SCOPE_CUTS. The M2 re-gate runs as soon as the P0 blockers (T-139, T-155) close. | Chris: "<Chris's message omitted>." | Chris chat |
72	| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this charge", a named confirm ("I checked this is a separate charge for a service"), recorded in the audit trail; it then sums like any accepted charge. Amends D-059 item on reclassify: (b) is promotable with the confirm, (a) never. | The default-deny rule undercounts real ledger lines (lib11 $3,260 vs $6,000); the paralegal must see why and be able to fix it herself, without reopening the overcount paths. | GATE-M2 r2 paralegal |
73	
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:15.229Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/SCOPE_CUTS.md"
}
````

### User / tool · 2026-11-02T19:59:15.364Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:22.843Z

**tool call — Bash**
````
{
 "command": "cat reviews/GATE-M2-summary.md; cat reviews/MVP-ux-audit-r4.md",
 "description": "Read M2 gate summary and UX audit r4"
}
````

### User / tool · 2026-11-02T19:59:22.958Z

**tool result**
````
# GATE-M2 summary — Core pipeline + evals green

Result: **pass** (round 2). Pinned commit for the panel: 7cfdb0b; fixes verified through da0c7fe.

## Evidence
- Live ship bar: `evals/reports/20261102T164038Z.md` (claude-cli, 3 runs, source 312efe6, clean tree): `ship_bar_met True`; grounding 1.0, entry recall 0.982, determinism 1.0, unsupported 0, hallucination catch 40/40, J3 20/20 and J4 12/12 with 0 false agrees. Live calibration regenerated in the same run (7cfdb0b).
- Earlier three consecutive live 3-runs at 63e18ed (5dfba88) also met the bar.
- `evals/letter_check.py`: 0 money expressions outside the total and accepted-charge lines over 25 cases.
- Unit suite at da0c7fe: 5683 passed, 8 skipped, 0 failed (T-175 r2 review). E2E: full suite green on clean archives (T-155/T-164 reviews; T-174 381 passed, the one red spec fixed in 30c04e6).

## Round 1 (0c24f5f) — fail, 3 blockers
Triage: `reviews/GATE-M2-round1-triage.md`. Every finding at major or above was mapped to a card and closed or decided:
| Finding | Card | Outcome |
|---|---|---|
| Rates/dismissed charges in the letter (adjuster blocker) | T-139 | done (export gate scans the final letter, one money detector; residual slang = scope cut 7c) |
| Ledger totals counted as charges (paralegal blocker) | T-140 | done (D-059..D-062 default-deny, total line states a sum of accepted lines; residuals 7d-7f) |
| Deadline run shows 'verified' (staff blocker) | T-145 | done |
| Timed-out re-run deletes items | T-146, T-161, T-165 | done (decided and hand-entered work is never lowered or deleted) |
| lib11 conflict missed / false date conflict | T-141 | done (D-061; residuals 13f) |
| "No conflicts found" overclaims | T-142, T-151 | done |
| Clinical sentences silently dropped | T-143, T-144 | done |
| Live evidence not at HEAD | QA confirming run | done (above) |

## Round 2 (7cfdb0b) — 0 blockers
| Reviewer | Verdict | Majors and resolution |
|---|---|---|
| staff-engineer | changes | unit suite red (calibration tests, e2e ids) — fixed by T-169, T-166; suite green at da0c7fe |
| claims-adjuster | changes | internal notes: lib15 estimate labelled 'Rate'; pre-accident visit called 'First recorded treatment' — T-170 (held per D-063; carrier letter clean on all cases) |
| paralegal | changes | lib11 ledger lines undercounted with no way to count — D-064, T-171/T-172 done (lib11 counts to $6,000.00) |
| legal-nurse | pass | minors only |
| privacy (round 1) | pass | — |

## Accepted debt
SCOPE_CUTS rows 7c-7g, 13c-13f; held cards per D-063: T-130, T-135, T-137, T-147, T-150, T-153, T-156, T-158, T-163, T-170, T-176. Test-rigor debts accepted on T-162, T-169, T-173.

## MVP
The UX designer's walk calls the build a finished, polished MVP for its scope (`reviews/MVP-ux-audit-r4.md`, 489f1bc).
# T-174 MVP UX audit, round 4: final scoped check

Reviewer: ux-designer-reviewer (Priya Raman persona), model claude-opus-5-5. Date 2026-11-02. Baseline: reviews/MVP-ux-audit-r3.md (da0c7fe, changes, 2 majors).

**Build.** `git archive 489f1bc`. `git rev-parse --short HEAD` gave `489f1bc` at the start and at the end.
- Two servers ran from the scratch copy, both with `LLM_BACKEND=fixture FIXTURE_SET=curated` and each with its own scratch `ZLAYT_DB`:
  - 127.0.0.1:7981 with `ZLAYT_MODE=local`. The library is on the page. `/api/cases` returned `{"cases":[]}` at the start.
  - 127.0.0.1:7982 in public mode, with no library, to check the "where the library exists" branch.
- Both servers were stopped by PID (python 20424 and 20460). Both ports then returned `000`.

**Evidence.** Everything is in `artifacts/review-evidence/mvp-audit-r4/`:
- the scripts `r4w1..r4w4*.py`
- their raw output `r4w*.out`
- the screenshots `NN-*.png`

**Verdict: pass.** Both r3 majors are fixed on the real path, with no stubs. F14 is fixed. What is left is 5 minors and 3 nits.

**Scores:** design quality 4, originality 3, craft 4, functionality 4.

## Deterministic check first
- I ran `pytest tests/e2e/test_mvp_finish.py` with its own private server (empty DB): `22 passed in 33.08s`.
- Against my :7981 server, which already held 6 cases: `2 failed, 20 passed in 56.95s`. Both failures are the new refusal specs (`btn-error-library` count 0). r4w4 shows why: see minor F2.

## Major 1: the demo refusal (r3 F15). **Fixed.**
I drove the real POST /api/cases with no stubs (r4w1.out, r4w1b.out). The paste was a synthetic PT note with no record markers.
- **Message.** The box reads: "This demo only runs the recorded sample and library cases, so it can't analyze other text. Nothing was started."
  - It is shown as `role="alert"`.
  - The pasted text is kept (154 of 154 characters).
  - The only call made was the POST, and the case count did not change (0 to 0, 1 to 1, 2 to 2).
- **Buttons with the library (local).** "Open the sample" and "Choose a library case".
- **Buttons without the library (public).** Only "Open the sample". The copy changes to "the recorded sample case".
- **Run-live note.** "To run your own records, start the app on your own computer with ENABLE_LIVE=1 and a model key."
- **There is no "Edit the text" button anywhere.**
- **Choose a library case.** It opens the group and moves focus to the first library case, in view at 1440 and 390. The pasted text stays.
- **Open the sample.** It opens the 9-record sample preview, ready for Analyze.
- **Keyboard.** From Analyze, it is Tab, Tab, then the two buttons in order.
- **Layout.** No horizontal scroll at 390. Buttons are 44 px tall on touch (10-refusal-local-light-1440.png, 10-refusal-local-dark-390.png, 10-refusal-public-*).

## Major 2: the counted charge on lib11. **Fixed.**
I opened lib11 through "Add a synthetic case", then measured the row after "Count this charge" (r4w2.out, 21-counted-row-light-1440.png, 25-counted-row-dark-390.png, 26-counted-row-*.png).
- **The row reads:** chip "✓ Counted by you", then "You confirmed it is a separate charge for a service. No AI check was asked about it."
- **Wording.** "flag" appears 0 times, "confirm" once and "separate charge" once. The old present.py sentence is suppressed (charges.js:228).
- **Colour.** The chip is `chip--info`, not amber: rgb(230,239,253) on rgb(11,79,158) in light, and rgb(22,40,74) on rgb(156,194,255) in dark. The row has 0 `chip--warn`.
- **Fit.** At 1440 the chip spans x 586–716 inside its 578–786 cell (scrollWidth 128 = clientWidth 128). At 390 it spans 27–157 inside 19–373, with no horizontal scroll. I checked light and dark at both widths.
- **Other flags keep their warning.** The $2,740 and $300 rows still show amber "Needs review".
- **Feedback and keyboard.** The live region says "Counted $250.00 as a separate charge. Accepted charges now $250.00." Focus returns to the row. By keyboard it is 3 Tabs, then Enter, Tab, Enter.

## F14: the sample preview is deleted when she leaves (r4w3.out). **Fixed.**
- For each way of leaving, the case count went from 4 (before) to 5 (during the preview) to 4 (after), with no Ghost case left. I tried:
  - reload
  - browser Back
  - tab close (`page.close(run_before_unload=True)`)
  - navigating to about:blank
  - All cases
  - Back then Forward
- A reload lands on the overview, not on a missing case.
- No regression: an analyzed sample and a library case both survive a reload.
- Only a hard browser kill, which fires no page events, leaves the preview (nit N3).

## Remaining findings (none blocks)
- **F1 minor.** The Why dialog still uses the old flag wording for her count.
- **F2 minor.** The refusal specs race the library list.
- **F3 minor.** The refusal can land below the fold.
- **F4 minor, carried from r3.** The letter prints the ledger's statement date as if it were the date of service.
- **F5 minor, carried from r3, now card T-176.** Undo on a counted line half-reverses it. Noted only, not blocking.
- **Nits.** After "Open the sample", focus falls to `<body>`. The live note uses an env-var name. A hard browser kill leaves the preview.

## As the designer: is this a finished, polished MVP?
**Yes, for its stated scope.**
- The paralegal loop is complete and consistent. She sees every excerpt in place, has one first item and one count, and has one-key accept, edit and dismiss with undo.
- She can reach any section in one action and get back from Export.
- The export is a clean letter.
- The demo's most likely error now explains itself and offers two working ways forward.
- Her own decisions now read as hers, not as warnings.

What is left is wording and robustness polish:
- F1: one backend copy line.
- F2: the e2e wait.
- F3: scroll the error into view.
- F4: the letter date.
- T-176: undo.

A pilot can carry all of these. None makes a must-have unusable or hides provenance.

## What is right (keep)
- The refusal names what happened, says nothing was started, keeps her text and offers only actions that work, with the copy adjusted to the mode.
- "Counted by you" in calm info blue, said once and fitting its cell at both widths: her decision reads as hers.
- The preview cleanup covers reload, Back, close and navigate, without touching analyzed or library cases.

```json
{"card": "T-174", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 489f1bc (HEAD 489f1bc at start and end); app at 127.0.0.1:7981 (fixture curated, ZLAYT_MODE=local, scratch ZLAYT_DB) and 127.0.0.1:7982 (fixture curated, public mode); library case case_lib11_priors_and_ledger, sample case evals/golden/sample.txt; baseline reviews/MVP-ux-audit-r3.md",
 "exercised": [
  "pytest tests/e2e/test_mvp_finish.py with its own private server: 22 passed in 33.08s; against :7981 holding 6 cases: 2 failed, 20 passed in 56.95s (both refusal specs)",
  "r4w1: real unstubbed paste refused at POST /api/cases on local and public servers, 1440 light pointer, 390 dark touch, 1440 keyboard; error text, buttons, note, text kept, case count, both buttons pressed",
  "r4w1b: position of the refusal right after Analyze, before any scroll, local and public at 390 and 1440",
  "r4w2: lib11 opened via Add a synthetic case; Count this charge on $250, $180, $2,310 by pointer, touch and keyboard; chip class, colours, box vs cell at 1440/390 light/dark; flag and confirm word counts; Why this status dialog; Undo; letter export via API",
  "r4w3: sample preview left by reload, Back, tab close, navigate away, All cases, Back+Forward, browser kill; analyzed sample and library case reloaded",
  "r4w4: refusal at 0, 0.5, 1.5 and 3 s after the form appears, 1440 and 390, library switcher state at click time",
  "read the 489f1bc diff of charges.js, input.js, review.css, styles.css; trace.py:526-537; stepper.js:481"
 ],
 "verdict": "pass",
 "scores": {"design quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "The Why dialog for a counted line still says 'Flagged by the code' and 'You confirmed this flag by name'",
   "evidence": "artifacts/review-evidence/mvp-audit-r4/22-counted-why-light-1440.png; r4w2.out 'WHY flag words: 4 | confirm mentions: 5'; step reads 'Flagged by the code: Counted as a separate charge ... You confirmed this flag by name (Counted as a separate charge) on 2026-11-02'; source app/backend/trace.py:530 and :533; app/frontend/stepper.js:481 skips the new chargeFlagNote whenever a charge_flag step exists, so the frontend fix never shows here",
   "why_it_matters": "The row now says her count is her own decision, but one click away the same decision is called a code flag she confirmed. That is the wording r3 asked to remove, still shown on a second surface.",
   "fix": "For flag separate_charge, trace.py labels the step 'Counted by you' and says once: 'You confirmed it is a separate charge for a service on <date>.' No 'flag' wording. (Backend card.)",
   "acceptance_test": "E2E: after Count this charge, open More > Why this status; the dialog contains 'Counted by you' and no word 'flag'; 'confirm' appears once in that step."},
  {"severity": "minor", "title": "The refusal specs race the library list: red against a server that already has cases",
   "evidence": "pytest tests/e2e/test_mvp_finish.py against :7981 (6 cases): '2 failed, 20 passed' (btn-error-library count 0); private empty server: '22 passed'. r4w4.out: Analyze at 0 s after input-text appears gives buttons ['Open the sample'] with switcher absent; at 0.5 s and later gives both buttons. input.js:39-41 decides once, at refusal time",
   "why_it_matters": "The acceptance evidence for the main fix depends on server state. A quick Analyze also gets the refusal without the library option, even though the list arrives a moment later.",
   "fix": "The spec waits for [data-testid=library-list] before Analyze. demoRefusal re-renders when the case switcher finishes loading.",
   "acceptance_test": "test_mvp_finish.py passes 5 runs in a row against a server pre-loaded with 6+ cases."},
  {"severity": "minor", "title": "The refusal is not scrolled into view and can appear just below the fold",
   "evidence": "r4w1b.out local 1440 with 3 cases: Analyze at viewport y 864-900, error top at y 912 with vh 900, 'error top inside viewport: False'; 13-refusal-as-seen-local-light-1440.png",
   "why_it_matters": "She clicks Analyze and nothing on screen changes. Errors belong next to their source and in view (NN/g error guidelines).",
   "fix": "On showError, call scrollIntoView({block: 'nearest'}) on #input-error.",
   "acceptance_test": "With 3+ cases at 1440x900, after Analyze on a refused paste, the error box's top and its first button are inside the viewport."},
  {"severity": "minor", "title": "Carried from r3: a counted ledger line prints the statement date as its service date",
   "evidence": "r4w2.out letter_text: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00'; the same line was held back because 'The line states no date of service'",
   "why_it_matters": "The letter implies a date of service the record does not state.",
   "fix": "Print 'itemized ledger (statement dated June 15, 2026; no service date stated)' for counted no-date lines.",
   "acceptance_test": "Export of lib11 with $180 counted contains 'statement dated' and no bare 'June 15, 2026: $180.00'."},
  {"severity": "minor", "title": "Carried from r3, now backend card T-176: Undo on a counted line half-reverses it",
   "evidence": "r4w2.out AFTER UNDO $250: stays in group charges, review pending, chip 'Count taken back', and the text says both 'You took back your count' and 'You counted this line as a separate charge and confirmed it by name'; pending reads '$3,510.00 (not a total)'; 23-after-undo-light-1440.png",
   "why_it_matters": "Undo should return her to where she was. The row contradicts itself and the pending figure double-counts the line. Noted only; tracked on T-176.",
   "fix": "Per T-176: Undo returns the line to 'Unclear — not totaled' with Count this charge.",
   "acceptance_test": "Per T-176."},
  {"severity": "nit", "title": "After 'Open the sample', focus drops to <body>",
   "evidence": "r4w1.out OPEN SAMPLE => focus {'tag': 'BODY'} in all 5 walks",
   "why_it_matters": "A keyboard user has to Tab from the top to reach Analyze. Accessibility severity is deferred to accessibility-reviewer.",
   "fix": "Focus the records heading or Analyze after the preview loads.",
   "acceptance_test": "After Open the sample, document.activeElement is the records heading or btn-analyze."},
  {"severity": "nit", "title": "The run-live note names an environment variable",
   "evidence": "'To run your own records, start the app on your own computer with ENABLE_LIVE=1 and a model key.' (10-refusal-local-light-1440.png)",
   "why_it_matters": "This is developer terms, not paralegal terms (checklist 18). It is acceptable for a demo whose audience runs it, but it could link to the README instead.",
   "fix": "'To run your own records, run the app on your own computer (see README, Run live).'",
   "acceptance_test": "The note has no ENABLE_LIVE text and links to the README section."},
  {"severity": "nit", "title": "A hard browser kill leaves the sample preview behind",
   "evidence": "r4w3.out 'GHOST browser-kill: ... after 5 | ghost left: [\"Ghost browser-kill\"]'",
   "why_it_matters": "A crash fires no page events, so client-side cleanup cannot cover it. It is rare.",
   "fix": "Server-side expiry for never-run sample previews.",
   "acceptance_test": "An unrun preview older than N minutes is not listed."}
 ],
 "whats_right": [
  "The refusal names what happened, says nothing was started, keeps her text and offers only working actions, with copy matched to the mode (local vs public).",
  "'Counted by you' in calm info blue, said once and fitting its cell at 1440 and 390, light and dark: her decision reads as hers.",
  "Preview cleanup covers reload, Back, tab close, navigate away and Back+Forward, and never deletes an analyzed or library case."
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:27.251Z

**tool call — Bash**
````
{
 "command": "ls; ls app app/backend | head -50; grep -rn \"uvicorn\\|7860\" run.sh Makefile docs/RUNBOOK.md 2>/dev/null | head -20; ls submission evals/reports | tail -30",
 "description": "Inspect repo layout and run commands"
}
````

### User / tool · 2026-11-02T19:59:27.408Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
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
app:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

app/backend:
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
case_list.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
count_charge.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
money.py
narrative.py
overlap.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
docs/RUNBOOK.md:8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
docs/RUNBOOK.md:9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
20261102T164038Z.md
20261102T195748Z.md
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

submission:
NEEDS_CHRIS.md
prompt-log
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:28.867Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh; cat evals/reports/m3-sensors.md | head -80",
 "description": "Read serve script and M3 sensors report"
}
````

### User / tool · 2026-11-02T19:59:28.995Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
# M3 sensors (qa, T-045), re-run 2026-11-02 at HEAD 4510dc2

All runs in a clean worktree of HEAD 4510dc2 (no uncommitted files), `E2E_REQUIRE_DB=1`. This replaces the 02:39Z record, which predated the fixes and the live run.

| Sensor | Command | Result |
|---|---|---|
| Unit | `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/unit -q` | **5689 passed, 2 skipped**, 0 failed (395 s) |
| E2E (fixture backend, curated set, private local-mode server and SQLite file) | `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e -q -rsx` | **411 passed, 2 skipped**, 0 failed, 0 xfail (575 s). Skips: `test_ladder_gate::test_rejected_attempt_visible_but_not_exportable` (the sample fixture run has no rejected item; the 409 is unit-covered) and `test_multicase::test_screenshots` (opt-in, `ZLAYT_SCREENSHOTS=1`). No DB spec skipped. |
| Live eval | `LLM_BACKEND=claude-cli python -m evals.run` | `evals/reports/20261102T164038Z.md`: **ship_bar_met True**, backend claude-cli, generator claude-sonnet-5-5, judge claude-haiku-5-5, 3 runs, determinism 1.0, unsupported_count_3run 0, J3 20/20 and J4 12/12 caught x3 with 0 false agree. Source commit 312efe6, tree clean. |
| Fixture eval at HEAD | `python -m evals.run` | `evals/reports/20261102T195748Z.md`: ship_bar_met False **by design** (fixture cannot measure determinism, unsupported_count_3run, judge controls). Every measurable metric equals the live run: grounding 1.000 (241 checked), entry_recall 0.982, amount_recall 1.000, all eight flag P/R 1.000, hallucination_catch 40/40, controls 0 of 10, must_not 0, case_07_total_420 True, letter_currency_outside_charges 0. |
| letter_check | `python -m evals.letter_check` | exit 0, value 0 across 25 cases (R-CH-7, R-EX-8, R-EX-1) |
| Spec check | `python -m evals.run --check-spec` | exit 0 (letter and internal notes equal the golden export) |
| Calibration | `python -m evals.run --check-fresh` | calibration.json: no complaint (fresh at HEAD; regenerated from the live run in 7cfdb0b). Exit 1 only because of `latest.json`, see below. |
| Secrets | `python tools/check_secrets.py` | exit 0 (2280 files) |

## Is the live run still valid at HEAD?
- Prompts and lexicon: `git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml` is empty, so the live run's prompt hashes equal HEAD's.
- Code since 312efe6 (34 commits): `app/backend` changes are presentation and review-flow (plain wording in notes T-167, hand-entry kept on re-run T-165, case-list T-175, count-charge T-172, why/present/trace); none touches extraction, grounding or the flag engines. The fixture eval at HEAD reproduces every deterministic live number, which is the check that matters here.
- Not re-run live: a fresh `claude-cli` 3-run at HEAD (about 40 min and model cost). The orchestrator may order one before the gate if it wants the number at the exact gate commit.

## Finding: `latest.json` is a stale pointer
The committed `evals/reports/latest.json` is a fixture run from 14:39Z (ship_bar_met False). The live run's markdown and `runs/` were committed in 7cfdb0b, but not the live `latest.json`, and every fixture run overwrites that file. `--check-fresh` therefore exits 1 on two hash lines (`lexicon.yaml`, `judge_conflict_v6.md`) although those files did not change after the live run. The evidence is fine; the pointer is not. Fix by the next live run committing its `latest.json` (qa will do it with the gate re-run if ordered).

## AC to evidence
| AC | Evidence |
|---|---|
| 1 journey, decisions survive reload | `test_review_matrix.py`, `test_timeline.py::test_needs_review_sorted_first_in_queue`, `test_edit.py::test_notes_list_edited_item_with_both_texts`, `test_export_ui.py`, and the new `test_journey_modes.py` (reload keeps both dismissals) |
| 2 R-EX-1 matrix | `test_letter_isolation.py` (sample, one note) plus new `test_letter_matrix.py`: 10 recorded cases x 3 decision profiles, letter independent of flag decisions and notes, planted-leak self-test |
| 3 keyboard, 375 px, adversarial | new `test_journey_modes.py` (keyboard-only with a pointer-click counter at 0; 375 px with 44 px targets and no sideways scroll on four screens), new `test_adversarial_ui.py` (empty, whitespace, oversize, non-English, pasted PDF text: whole-database llm_calls/cases unchanged; case_07 total $420.00 on screen and in the letter), `test_adversarial.py` (API) |
| 4 sensors | this file |
| 5 ladder gate | `test_ladder_gate.py::test_llm_item_with_no_human_action_is_absent_from_the_letter_and_from_every_accepted_part_of_the_notes` and the edited-item test |
| 6 contract review | T-038 AC4: `latest.json` records backend and models, fixture run reports ship_bar False and determinism/unsupported None (above). T-037 AC2: fixtures for sample, case_01..09, hallucinations and controls replay in the fixture eval: hallucination_catch 40/40 and controls 0 of 10 are measured from the recorded fixtures (the three blockers listed there are the live-only ones). T-045 AC4: live report path above. |
| 7 paralegal verify_quickly >= 4 | left for the M3 gate |
| 8 two library cases | new `test_two_cases_side_by_side.py` (two tabs, same item ids, alternating decisions, reload, case list, letters), `test_local_mode.py` (API) |

## Where an AC's literal text is stale (the current rule is tested)
- AC5 says an unacted LLM item is absent from "both blocks". Spec s.6 and D-045 keep `PENDING ITEMS NOT INCLUDED` in the notes so the reader is told what is out. The test requires absence from the letter and from every notes section that reports accepted or quoted content, and presence only under that titled section.
- AC2/R-EX-1 total line: the matrix uses D-062's "Billed charges accepted from these records: $X".
- An edit alone no longer opens the export (D-045); the edited-item test edits then accepts.
- D-034 hard 422 for new numbers and D-047 (no keep-my-wording confirm) are reflected in the existing edit specs.
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:33.747Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep -i \"GATE-M3\\|paralegal\" | tail; python3 tools/board.py status --brief 2>&1 | head -40",
 "description": "List M3 gate reviews and board status"
}
````

### User / tool · 2026-11-02T19:59:34.569Z

**tool result**
````
T-120-paralegal-r3.md
T-120-paralegal-r4.md
T-120-paralegal.md
T-121-paralegal.md
T-123-paralegal.md
T-136-paralegal-r2.md
T-136-paralegal-r3.md
T-136-paralegal.md
T-149-paralegal-r2.md
T-149-paralegal.md
[board] 92.2% done | M0:done M1:done M2:done M3:gate_running M4:planned M5:planned
[board] ready=0 in_progress=0 in_review=1 changes=0 blocked=12 needs_chris=3 done=154 | inbox_unread=0 stalled=0
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:36.753Z

**tool call — Bash**
````
{
 "command": "grep -l \"verify_quickly\" reviews/*.md | xargs grep -ho '\"verify_quickly\": *[0-9]' | sort | uniq -c; grep -l '\"verify_quickly\"' reviews/*.md | tail -5; python3 tools/board.py list --status blocked; python3 tools/board.py list --status needs_chris; python3 tools/board.py list --status in_review",
 "description": "Check paralegal verify_quickly scores and held cards"
}
````

### User / tool · 2026-11-02T19:59:37.358Z

**tool result**
````
   3 "verify_quickly": 2
  16 "verify_quickly": 3
  22 "verify_quickly": 4
reviews/T-120-paralegal-r2.md
reviews/T-136-paralegal-r3.md
reviews/T-136-paralegal.md
reviews/T-149-paralegal-r2.md
reviews/T-149-paralegal.md
T-059	M3	backend    	blocked          	P2	AC 2/3	Draft treatment paragraph in firm voice (grounded, judged, internal until accepted)
T-130	M3	backend    	blocked          	P2	AC 0/1	T-105 leftovers: Waddell count forms in credibility.py, statement-line service nouns as charge context, bare insurance/seguro wording
T-135	M3	qa         	blocked          	P2	AC 0/1	Rename the J3 'agrees' test and fix its docstring to the v6 labels (T-109 r3 minor 7)
T-137	M3	qa         	blocked          	P2	AC 0/1	Held-out audit hardening: kill 7 surviving audit mutants, qualify held-out report cells, audit J4, extend scope cut 13c to the plan side (T-113 r2 minors)
T-147	M3	backend    	blocked          	P1	AC 0/1	Perf: flags._hedge_run is quadratic when many hits share one huge unit (24k-char attribution chain takes ~11 s); add a per-unit memo
T-150	M3	backend    	blocked          	P1	AC 0/1	extract prompt: stop asking for 'charge' sentences in treatment entries (extract_v1 line 12 -> v2); re-record fixtures live; T-139 recommendation
T-153	M3	backend    	blocked          	P2	AC 0/1	Fee vocabulary: 'Surgeon fee', 'referral fee' and Spanish figures (lib04/05/06/09) stay unclear and undercount the total; classify fee lines as charges with a J2 re-record
T-156	M3	backend    	blocked          	P2	AC 0/1	Conflict coverage polish: export notes carry a coverage line (which conflict checks ran / were skipped and why); server not_checked list names LOC and side; info notes name their record; lead sentence differs for partial/all-skipped runs (T-151/T-142 nurse minors)
T-163	M3	backend    	blocked          	P2	AC 0/1	Internal notes list each flagged charge accepted through a named confirm (T-159 AC1 leftover; needs export.py after T-139/T-140 land)
T-167	M3	backend    	blocked          	P0	AC 1/1	MVP backend wording (T-166 audit F4/F7): no developer codes or test-mode wording in paralegal-facing text or the exported notes (JUDGE_UNAVAILABLE, fixture backend, curated responses, 'server answered 500'); demo-mode edit wording is plain
T-170	M3	backend    	blocked          	P1	AC 0/1	Internal notes accuracy (GATE-M2 r2 adjuster majors): lib15 a 12-visit future-care estimate is labelled 'Rate $1,800/visit'; the accident-date line can call a pre-accident visit the 'First recorded treatment'
T-176	M3	backend    	blocked          	P2	AC 0/1	Undo on a counted line should restore it to Unclear (kind unclear, Count this charge button), not leave a pending Charge
T-019	M5	orchestrator	needs_chris      	P1	AC 0/1	Provide a real Anthropic API key for the public deployment (NEEDS_CHRIS #1)
T-022	M5	orchestrator	needs_chris      	P1	AC 0/1	Public link: demo-only or live? (NEEDS_CHRIS #2)
T-023	M5	orchestrator	needs_chris      	P2	AC 0/1	Live-model eval budget on claude.ai plan (NEEDS_CHRIS #3)
T-045	M3	qa         	in_review        	P0	AC 7/8	Playwright E2E: full paralegal journey, adversarial inputs, all sensors
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:40.647Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-167 | tail -25; python3 tools/board.py show T-170 | tail -15",
 "description": "Show T-167 and T-170 card details"
}
````

### User / tool · 2026-11-02T19:59:40.829Z

**tool result**
````
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-167-staff-engineer.md", "at": "2026-11-02T16:35:29Z"}
ac:
  - {"n": 1, "text": "grep of every user-facing string and the notes export for reason codes / test jargon finds none; the demo-mode edit message says plainly that the AI check is not available in the demo and what to do; unit tests", "done": true, "evidence": "tests/unit/test_t167_plain_wording.py (grep-style: no SHOUTING_CODE and no fixture/curated/older version/server answered/recorded replies in why sentences x judge shapes, narrative/trace/reclassify/calibration strings, notes export, golden notes; demo edit end-to-end says AI second check not available in this demo + compare + accept); full unit suite from git archive HEAD copy + my hunks: 5266 passed, 8 skipped; golden sample notes unchanged"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T16:06:40Z orchestrator: assigned: backend
- 2026-11-02T16:06:56Z backend: claimed
- 2026-11-02T16:12:56Z backend: tests first (tests/unit/test_t167_plain_wording.py, grep-style over why sentences x judge shapes, narrative/trace/reclassify/calibration strings, notes export, demo edit end-to-end); why.py JUDGE_DEMO/JUDGE_FAILED/NOT_RUN sentences, review.py edit warning, export.py notes phrases + removed-narrative lines, calibration stale reason. Not mine: 'server answered 500'/'Request failed' (frontend api.js), chip 'curated responses' (frontend app.js), calibration box heading and 'fixture backend (recorded replies...)' (evals/run.py statements + suggestions.js). Running suite from git archive copy.
- 2026-11-02T16:20:42Z backend: AC 1 checked: tests/unit/test_t167_plain_wording.py (grep-style: no SHOUTING_CODE and no fixture/curated/older version/server answered/recorded replies in why sentences x judge shapes, narrative/trace/reclassify/calibration strings, notes export, golden notes; demo edit end-to-end says AI second check not available in this demo + compare + accept); full unit suite from git archive HEAD copy + my hunks: 5266 passed, 8 skipped; golden sample notes unchanged
- 2026-11-02T16:20:42Z backend: moved in_progress -> in_review
- 2026-11-02T16:20:49Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T16:35:29Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-167-staff-engineer.md; round 1; findings:
    - [major] Unit suite is red at da6afb2; the card's AC1 evidence (5266 passed) does not reproduce — fix: The owning card (qa for tests/**, or frontend) adds the three ids to the conftest contract docstring or renames them to declared ids; re-run at the closing commit.
    - [major] AC1 'grep of every user-facing string finds none' is false: backend-served calibration sentences still carry test wording — fix: Either narrow AC1 to backend-authored strings and record the rest as a SCOPE_CUT with cards (qa: evals/run.py:314 caveat builder and its rebuild check; T-166: chip and api.js), or bring the builder into scope. Do not close AC1 with the universal claim.
    - [minor] A prose field embeds a reason code in parentheses (judge_says) — fix: Add a reason_code key carrying the code; set judge_says to the plain sentence only.
    - [minor] _removed_why fallback doubles a phrase in the notes export — fix: Give each branch its own fallback phrase; the Removed fallback ends with a period.
    - [minor] FIXTURE_MISS sentence is replay wording with no next step — fix: Reuse the JUDGE_DEMO wording for FIXTURE_MISS items.
- 2026-11-02T16:35:29Z orchestrator: moved changes_requested -> blocked: both majors are owned by the T-166 frontend round in flight (e2e contract test ids from f7a8f2a; served calibration text shown plainly); re-check after T-166 lands

## Handoff
What changed: why.py (no JUDGE_NOT_RUN prefix; JUDGE_DEMO 'The AI second check is not available in this demo... compare the summary with the quote yourself; if they match, accept it'; JUDGE_FAILED 'not available right now' + same advice; picked from judge error_class FixtureMiss), review.py edit warning uses the same sentence, export.py notes (reason codes removed from edit phrases and removed-narrative lines), calibration_route stale reason ('older version of the prompts' gone). Codes unchanged in API fields. How verified: new tests/unit/test_t167_plain_wording.py (written first, failed first); 4 older tests updated for the new sentences; sample golden unchanged (no codes in it); full unit suite from git archive copy 5266 passed. Left (not mine, frontend/qa): 'server answered 500'/'Request failed' in app/frontend/api.js, header chip 'cached demo (curated responses)' app.js:11, calibration box heading suggestions.js:138 and 'fixture backend (recorded replies, N golden cases)' statements built in evals/run.py:314. Surprised: sentence advice 'accept it' is right for edits but generic for AI-drafted items (why() does not know the item was edited).

claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "estimates are labelled as estimates (never 'Rate'); 'First recorded treatment' is the first record on/after the stated accident date that describes treatment; tests on lib15 and the reviewer's case", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T17:14:40Z orchestrator: moved ready -> blocked: held per D-063 (P1, internal notes only; carrier letter is clean); resume after the MVP

## Handoff (filled when moving to in_review)
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:46.567Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/app-d0b04bc && cd /Users/arsis/zlayt-pm-project && git archive d0b04bc | tar -x -C $S/app-d0b04bc && ls $S/app-d0b04bc | head; lsof -iTCP -sTCP:LISTEN -P | grep -E \":79[0-9][0-9]|:7860\" ",
 "description": "Extract pinned commit into scratchpad and check ports"
}
````

### User / tool · 2026-11-02T19:59:48.731Z

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
Python    19991 arsis    9u  IPv4 0xe658f3cecdb9407b      0t0  TCP localhost:7860 (LISTEN)
Python    49280 arsis    9u  IPv4 0xcb4826752527c91d      0t0  TCP localhost:7941 (LISTEN)
Python    49978 arsis    9u  IPv4 0x434421ef80be0d8b      0t0  TCP localhost:7991 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:50.478Z

**tool call — Bash**
````
{
 "command": "grep -n \"PORT\\|port\\|HOST\" app/main.py | head; grep -rn \"ENABLE_LIVE\\|ZLAYT_MODE\" app/config.py app/main.py 2>/dev/null | head",
 "description": "Find port and mode env vars"
}
````

### User / tool · 2026-11-02T19:59:50.630Z

**tool result**
````
2:import os
4:import uvicorn
6:from app.backend.api import create_app
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
````

### Assistant · claude-opus-5-5 · 2026-11-02T19:59:54.441Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/app-d0b04bc && (PORT=7973 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/pm-gate.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/server.log 2>&1 & echo PID $!); sleep 4; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7973/; cat $S/server.log | tail -5",
 "description": "Start app server on port 7973 with fixture backend"
}
````

### User / tool · 2026-11-02T19:59:58.641Z

**tool result**
````
PID 50240
200
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:00.465Z

**tool call — Bash**
````
{
 "command": "grep -n \"^#\\+ \\|^| *\\`\\(GET\\|POST\\|PUT\\|PATCH\\|DELETE\\)\" memory/contracts/api.md | head -60",
 "description": "List API endpoints from the contract"
}
````

### User / tool · 2026-11-02T20:00:00.593Z

**tool result**
````
1:# API contract — DRAFT — backend owns from M2
5:## Conventions
14:## Endpoint index
46:## GET /api/health
59:## POST /api/cases
79:## POST /api/cases/pdf (D-031)
83:### PDF hidden text and local OCR (T-087, T-086; D-042)
107:## POST /api/cases/{token}/review/batch (D-031)
111:## /api/cases/{token}/export_config (D-031)
114:## POST /api/cases/{token}/run
121:## GET /api/cases/{token}/status
131:## GET /api/cases/{token}
265:## POST /api/cases/{token}/records/{rid}/confirm_date
286:## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
298:## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
310:### POST /api/cases/{token}/dismissal_suggestions/apply
313:## GET /api/cases/{token}/items/{item_id}  — "Why?"
331:## POST /api/cases/{token}/items/{item_id}/review
379:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
408:## GET /api/cases/{token}/export
559:## GET /api/cases/{token}/audit
581:## Check traces (D-042): per-item stepper, case stepper, judge summary
588:### Step (shared by all three endpoints)
606:### GET /api/cases/{token}/items/{item_id}/trace
638:### GET /api/cases/{token}/trace
670:### GET /api/cases/{token}/judges
686:## POST /api/cases/{token}/rejudge  (D-044)
696:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
718:## GET /api/calibration  (T-099, serves T-090 counts to T-096)
728:## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
763:## Spanish-language records (T-085, D-042)
779:## Summary clause trimming (T-112, D-054)
782:## Dollar amounts in entries (T-139, D-019, R-CH-7, R-EX-8)
797:## DELETE /api/cases/{token}
802:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:02.213Z

**tool call — Bash**
````
{
 "command": "sed -n 59,78p memory/contracts/api.md; sed -n 114,135p memory/contracts/api.md; sed -n 331,350p memory/contracts/api.md",
 "description": "Read create, run, and review endpoint contract"
}
````

### User / tool · 2026-11-02T20:00:02.331Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:04.495Z

**tool call — Bash**
````
{
 "command": "sed -n 408,440p memory/contracts/api.md; sed -n 696,716p memory/contracts/api.md",
 "description": "Read export and library endpoint contracts"
}
````

### User / tool · 2026-11-02T20:00:04.638Z

**tool result**
````
## GET /api/cases/{token}/export
**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. An edit still marked `needs_review` is open and out of the letter, so it does not stop the export either (T-134, see the edit section). Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the only change to the quote is whitespace (each run of spaces and line breaks becomes one space); a translated entry adds ` — English: <summary>` after the bracket, before the translation note; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
```json
{
  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
  "generated_at": "2026-11-02T01:20:00Z",
  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges accepted from these records: $8,390.00",
  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
  "items": {
    "entries": [
      {
        "id": "e1",
        "record_ids": [
          "r1"
        ],
        "edited": false,
        "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
      },
      {
        "id": "e2",
        "record_ids": [
          "r2"
        ],
        "edited": false,
        "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
      },
      {
        "id": "e3",
        "record_ids": [
          "r3"
        ],
        "edited": false,
## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` (T-148, the overview screen) -> `{ "cases": [ summary ] }`, newest first (`created_at`, then insertion order); every case the single local profile can see. Code only: no model call, no pipeline run, no record text. Local mode only: no auth, no users, no sharing (scope cut kept). One `summary`:
```
{ "token": "...", "title": "Er only then gap", "name": "case lib01 er only then gap" | null, "source": "paste|sample", "status": "ingested|running|ready|failed",
  "record_count": 9, "created_at": "...Z", "updated_at": "...Z", "last_activity_at": "...Z",
  "run": { "stage": "finalize" | "ingest" | null, "steps_done": 7, "steps_total": 8, "running": false, "error": false },
  "progress": { "entries": {"decided": 2, "total": 5}, "flags": {"decided": 0, "total": 2}, "amounts": {"decided": 0, "total": 2} },
  "counts": { "pending", "accepted", "edited", "dismissed", "needs_review" },
  "hitl": { "pending": 7, "needs_review": 4, "needs_review_open": 4, "edits_to_check": 0, "could_not_verify": 1,
            "gate_blockers": [ { "reason_code", "kind", "item_id", "why" } ], "gate_warnings": [ { "reason_code", "count", "why" } ] },
  "export_ready": true,
  "next_action": { "item_id": "f_r3_1" | null, "kind": "entry|flag|amount|case|run", "reason": "plain sentence" } | null,
  "status_error": false, "status_error_message": null }
```
**`status_error` (T-175 r2).** A case that was deleted while the list was read is left out. A case whose summary fails once is read again after 50 ms (a run or review was writing): if that works it is a normal row. If it fails twice in a row the case exists and the failure is a bug: the row is still listed (one bad case never takes the whole list down) but with `status_error: true` and `status_error_message: "We couldn't load this case's status"`. On such a row `record_count`, `counts`, `progress` and `hitl` are all `null` (never zeros), `export_ready` is `false`, `next_action` is `null`; `token`, `title`, `name`, `source`, `status`, the three times and `run` are still filled from the case row. The frontend shows the message in place of counts and progress, not an empty or zero state. Normal rows carry `status_error: false, status_error_message: null`. The server logs it at ERROR as `case list: a case's status could not be computed twice in a row (<ExceptionClass>)`, never any record text.
**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no name, or a name that is empty once cleaned (`case_01_`, `.txt`), the first record header: the provider (its Source line with any tags or angle brackets dropped, at most 60 characters) and that record's date, "Marrowgate General ED, Feb 14, 2026" ("Records from Feb 14, 2026" when the record has no Source line, the bare provider when it has no date); (3) when no record has either, "Records added Nov 2" ("Sample case" for the sample). `name` is the stored value, `null` until someone names the case. `PATCH /api/cases/{token}` with `{"title": "Rivera v. Acme"}` stores the name (same rule as on create: plain text, control characters removed, white space collapsed; a `<` or `>` or more than 120 characters is `422 invalid_title` and the stored name is unchanged) and answers `200 {token, name, title}`; a blank or `null` title clears the name, so the title returns to the derived default; a body without `title`, or a `title` that is neither text nor null, is `400 bad_request`; an unknown token is `404 not_found`. The name goes through the same readable-title step as any other, so underscores or a file extension in a typed title are shown as words. Allowed in public mode too (the token is the capability). A rename is not a review event. **A title is never markup:** a typed title is refused if it contains `<` or `>`, and a title derived from a record's Source line has its tags dropped, so `title` is always plain text and a client may still render it as text only (`textContent`), never as HTML.

**`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `hitl.needs_review_open` (T-157 r3) is the number of items still open in Needs review: `state: needs_review` and (`review_status: pending` or an unconfirmed edit, `edit_to_check`), i.e. exactly the set `next_action` picks from and the items of `GET /api/cases/{token}` that wait for the paralegal; a reworded entry counts, an accepted item that is still `needs_review` does not (so it is at most `needs_review`). `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:05.420Z

Now let me write a journey script driving the sample case end to end through the API.

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:18.296Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/journey.py",
 "content": "\"\"\"GATE-M3 PM journey: sample case end to end through the real API (fixture backend, curated set).\nUsage: python3 -I journey.py http://127.0.0.1:7973 [sample|<library id>]\"\"\"\nimport json, sys, time, urllib.request, urllib.error\n\nBASE = sys.argv[1]\nWHICH = sys.argv[2] if len(sys.argv) > 2 else \"sample\"\n\n\ndef call(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    req = urllib.request.Request(BASE + path, data=data, method=method, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            return r.status, json.loads(r.read() or b\"{}\")\n    except urllib.error.HTTPError as e:\n        raw = e.read()\n        try:\n            return e.code, json.loads(raw)\n        except Exception:\n            return e.code, {\"raw\": raw.decode(errors=\"replace\")[:300]}\n\n\nbody = {\"sample\": True} if WHICH == \"sample\" else {\"library\": WHICH}\ns, c = call(\"POST\", \"/api/cases\", body)\nprint(\"CREATE\", s, \"records\", c.get(\"record_count\"), \"gap_flags\", c.get(\"gap_flags\"), \"warnings\", c.get(\"warnings\"))\ntok = c[\"token\"]\ns, r = call(\"POST\", f\"/api/cases/{tok}/run\", {\"confirm_rerun\": False})\nprint(\"RUN\", s, r.get(\"status\"))\nfor _ in range(120):\n    s, st = call(\"GET\", f\"/api/cases/{tok}/status\")\n    if st.get(\"status\") in (\"ready\", \"failed\"):\n        break\n    time.sleep(1)\nprint(\"STATUS\", st.get(\"status\"), st.get(\"error\"), st.get(\"counts\"))\ns, case = call(\"GET\", f\"/api/cases/{tok}\")\nprint(\"TITLE\", case.get(\"title\"), \"| next_action\", case.get(\"next_action\"))\nprint(\"REVIEW COUNTS\", case.get(\"review\", {}).get(\"counts\"))\nprint(\"\\nENTRIES\")\nfor e in case.get(\"entries\", []):\n    print(\" \", e[\"id\"], e.get(\"date\"), \"|\", e.get(\"provider\"), \"|\", e.get(\"state\"), e.get(\"reasons\"), \"|\", (e.get(\"summary\") or \"\")[:90])\nprint(\"UNDATED\", [u.get(\"id\") for u in case.get(\"undated_entries\", [])])\nprint(\"\\nFLAGS\")\nfor f in case.get(\"flags\", []):\n    print(\" \", f[\"id\"], f.get(\"type\"), \"|\", f.get(\"state\"), \"|\", (f.get(\"title\") or \"\")[:90], \"| ev:\", [ (x.get(\"excerpt\") or \"\")[:60] for x in f.get(\"evidence\", [])][:2])\nprint(\"\\nAMOUNTS\")\nfor a in case.get(\"amounts\", []):\n    print(\" \", a[\"id\"], a.get(\"kind\"), a.get(\"value_cents\"), \"|\", a.get(\"state\"), a.get(\"reasons\"), \"|\", (a.get(\"excerpt\") or \"\")[:60], \"|\", (a.get(\"why\") or \"\")[:120])\nprint(\"\\nTRAY\", [(t[\"id\"], t.get(\"kind\"), t.get(\"reasons\")) for t in case.get(\"tray\", [])])\nprint(\"TRAY_FILTERED count\", (case.get(\"tray_filtered\") or {}).get(\"count\"))\nprint(\"TOTALS\", json.dumps(case.get(\"totals\") or case.get(\"charges_total\") or {k: v for k, v in case.items() if \"total\" in k})[:400])\n\n# export before any decision\ns, ex = call(\"GET\", f\"/api/cases/{tok}/export\")\nprint(\"\\nEXPORT BEFORE DECISIONS\", s, json.dumps(ex)[:300])\n\n# accept every entry and flag, accept only charge-kind amounts, accept the rate too (noted)\nresults = {}\nfor kind in (\"entries\", \"flags\", \"amounts\"):\n    for it in case.get(kind, []):\n        s, rr = call(\"POST\", f\"/api/cases/{tok}/items/{it['id']}/review\", {\"action\": \"accept\"})\n        results[it[\"id\"]] = (s, (rr.get(\"error\") or {}).get(\"code\") if isinstance(rr.get(\"error\"), dict) else rr.get(\"detail\"))\nprint(\"\\nACCEPT RESULTS\", results)\ns, ex = call(\"GET\", f\"/api/cases/{tok}/export\")\nprint(\"\\nEXPORT\", s)\nif s == 200:\n    print(\"----- LETTER -----\")\n    print(ex[\"letter_text\"])\n    print(\"----- NOTES -----\")\n    print(ex[\"internal_notes_text\"])\nelse:\n    print(json.dumps(ex)[:1500])\ns, tr = call(\"GET\", f\"/api/cases/{tok}/trace\")\nprint(\"\\nTRACE gate\", json.dumps([st for st in tr.get(\"steps\", []) if st.get(\"id\") in (\"export_gate\",)])[:800])\nprint(\"TOKEN\", tok)\n"
}
````

### User / tool · 2026-11-02T20:00:18.452Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/journey.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:20.009Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && python3 -I journey.py http://127.0.0.1:7973 sample 2>&1 | tee journey-sample.out | head -150",
 "description": "Run sample-case journey against the app"
}
````

### User / tool · 2026-11-02T20:00:21.893Z

**tool result**
````
CREATE 201 records 9 gap_flags ['f_gap_r6_r7'] warnings []
RUN 202 running
STATUS ready None {'entries': 9, 'amounts': 4, 'flags': 10}
TITLE Sample case | next_action {'item_id': 'a2', 'kind': 'amount', 'reason': 'This figure is a rate, not a charge, so it is not added to the total.'}
REVIEW COUNTS {'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0, 'edit_to_check': 0}

ENTRIES
  e1 2026-01-09 | Austin EMS run report | verified [] | Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache;
  e2 2026-01-09 | Central ER discharge summary | verified [] | Diagnosed with cervical strain and concussion without loss of consciousness; CT head negat
  e3 2026-01-16 | Dr. Alvarez, primary care | verified [] | Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 
  e4 2026-01-23 | Capital PT, initial evaluation | verified [] | Cervical range of motion reduced approx. 40%; plan of care 12 visits.
  e5 2026-02-20 | Capital PT, visit 8 | verified [] | Pain 4/10, improving.
  e6 2026-03-06 | Capital PT, visit 9 | verified [] | Discharged from physical therapy after two missed appointments; pain 3/10.
  e7 2026-05-18 | Hill Country Pain Management, new patient | verified [] | New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
  e8 2026-05-29 | Austin Imaging, cervical MRI | verified [] | C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may 
  e9 2026-06-12 | Hill Country Pain Management, follow-up | verified [] | Cervical epidural steroid injection recommended; patient states symptoms began after the J
UNDATED []

FLAGS
  f_gap_r6_r7 gap | verified | Gap of 73 days | ev: ['Date: 2026-03-06', 'Source: Capital PT, visit 9']
  f_accident_date_after_treatment_1_2_7 conflict | verified | Stated accident date is later than recorded treatment | ev: ['Date of accident per intake form: 2026-01-19', 'Date: 2026-01-09']
  f_cx1 conflict | verified | Treatment plan and what followed differ | ev: ['Plan of care: 12 visits.', 'Discharged from PT after two missed appointments.']
  f_r3_1 pre_existing | verified | Mention of a prior or pre-existing condition | ev: ['Patient reports low back pain in 2023, resolved.']
  f_r8_1 pre_existing | verified | Degenerative wording | ev: ['Findings may represent degenerative change']
  f_r6_1 causation | verified | Missed or ended care | ev: ['Discharged from PT after two missed appointments.']
  f_r7_1 causation | needs_review | Accident date source | ev: ['Date of accident per intake form: 2026-01-19.']
  f_r7_2 causation | verified | New-onset wording | ev: ['New onset pain']
  f_r8_2 causation | verified | Hedged wording | ev: ['may represent degenerative change; correlate clinically']
  f_r9_1 causation | verified | Reported onset | ev: ['Patient states symptoms began after the January collision.']

AMOUNTS
  a1 charge 624000 | verified [] | Dx: cervical strain; concussion without loss of consciousnes | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
  a2 rate 18500 | needs_review ['AMOUNT_RATE_NOT_TOTALED'] | Cervical range of motion reduced approx. 40%. Plan of care:  | This figure is a rate, not a charge, so it is not added to the total.
  a4 charge 215000 | verified [] | C5-C6 disc protrusion with mild right foraminal narrowing. F | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
  a3 damages None | needs_review ['AMOUNT_DAMAGES'] | Pain 4/10, improving. Patient reports missing 3 days of work | This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.

TRAY []
TRAY_FILTERED count 0
TOTALS {"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"}, "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"}, "flagged_charges": [], "not_totaled": [{"id": "a2", "kind": "rate", "text": "$185"}], "possible_overlaps": []}

EXPORT BEFORE DECISIONS 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "Nothing is accepted or edited yet, so the letter would be em

ACCEPT RESULTS {'e1': (200, None), 'e2': (200, None), 'e3': (200, None), 'e4': (200, None), 'e5': (200, None), 'e6': (200, None), 'e7': (200, None), 'e8': (200, None), 'e9': (200, None), 'f_gap_r6_r7': (200, None), 'f_accident_date_after_treatment_1_2_7': (200, None), 'f_cx1': (200, None), 'f_r3_1': (200, None), 'f_r8_1': (200, None), 'f_r6_1': (200, None), 'f_r7_1': (200, None), 'f_r7_2': (200, None), 'f_r8_2': (200, None), 'f_r9_1': (200, None), 'a1': (200, None), 'a2': (200, None), 'a4': (200, None), 'a3': (200, None)}

EXPORT 200
----- LETTER -----
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

January 9, 2026 — Central ER discharge summary
Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."

January 16, 2026 — Dr. Alvarez, primary care
Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
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
----- NOTES -----
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.

AMOUNTS NOT TOTALED
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.

DAMAGES MENTIONS (not charges)
- Record 5 (Capital PT, visit 8, February 20, 2026): "Patient reports missing 3 days of work."

FUTURE TREATMENT RECOMMENDED (no cost stated)
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.

BILLS TO REQUEST (entry in the letter, no accepted charge)
- Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.

RECORDS NOT IN THE TREATMENT SECTION
- none (9 of 9 records included)

EDITED ITEMS
- none

PENDING ITEMS NOT INCLUDED
- none

TRACE gate [{"id": "export_gate", "label": "Ready to export?", "kind": "code", "status": "pass", "why": "At least one item is accepted and every accepted item has its checks, so the export can be built.", "reason_code": null, "rule": "row 19", "blocks_export": false, "evidence": {}, "next_action": null, "counts": {"blocking": 0, "pending_items": 0, "date_unconfirmed": 0, "accepted": 23, "edit_not_confirmed": 0, "dismissed": 0, "rejected_not_blocking": 0, "judge_not_run": 0, "code_check_failed": 0, "money_in_letter": 0}, "ready": true, "blockers": [], "warnings": [], "n": 10}]
TOKEN Opa0ZJmKS9ZTCvbrskKx8A
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:25.588Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7973/api/library | python3 -c 'import json,sys; [print(c[\"id\"], \"|\", c.get(\"name\")) for c in json.load(sys.stdin)[\"cases\"]]'",
 "description": "List library cases"
}
````

### User / tool · 2026-11-02T20:00:25.757Z

**tool result**
````
case_lib01_er_only_then_gap | case lib01 er only then gap
case_lib02_slip_fall_prior_knee | case lib02 slip fall prior knee
case_lib03_truck_rear_end_chiro | case lib03 truck rear end chiro
case_lib04_dog_bite_scar_revision | case lib04 dog bite scar revision
case_lib05_pedestrian_orif_hardware | case lib05 pedestrian orif hardware
case_lib06_lop_billed_vs_adjusted | case lib06 lop billed vs adjusted
case_lib07_parking_lot_fall_outside_records | case lib07 parking lot fall outside records
case_lib08_second_crash_mri_after | case lib08 second crash mri after
case_lib09_spanish_interpreter_espalda | case lib09 spanish interpreter espalda
case_lib10_eob_ub04_cms1500 | case lib10 eob ub04 cms1500
case_lib11_priors_and_ledger | case lib11 priors and ledger
case_lib12_records_review_credibility | case lib12 records review credibility
case_lib13_cloned_notes_cross_provider | case lib13 cloned notes cross provider
case_lib14_handwritten_chiro_scans | case lib14 handwritten chiro scans
case_lib15_conclusory_letter_mist | case lib15 conclusory letter mist
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:27.648Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && python3 -I journey.py http://127.0.0.1:7973 case_lib11_priors_and_ledger > journey-lib11.out 2>&1; sed -n 1,200p journey-lib11.out | grep -v \"^  e[0-9]\" | head -120",
 "description": "Run lib11 ledger case journey"
}
````

### User / tool · 2026-11-02T20:00:29.364Z

**tool result**
````
CREATE 201 records 9 gap_flags ['f_gap_r7_r8'] warnings []
RUN 202 running
STATUS ready None {'entries': 9, 'amounts': 8, 'flags': 15}
TITLE Priors and ledger | next_action {'item_id': 'e1', 'kind': 'entry', 'reason': 'A second AI check found the summary only partly supported by the quoted text.'}
REVIEW COUNTS {'pending': 29, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 17, 'verified': 12, 'rejected': 2, 'edit_to_check': 0}

ENTRIES
UNDATED []

FLAGS
  f_gap_r7_r8 gap | verified | Gap of 35 days | ev: ['Date: 2026-04-24', 'Source: Fennimoor Spine Clinic, visit 8']
  f_cx1 conflict | verified | Records differ on a fact | ev: ['Prior accidents? Yes [ ] No [X].', 'History per patient: car accidents in 2019 and 2022 with nec']
  f_cx2 conflict | verified | Records differ on a fact | ev: ['Prior injuries? Yes [ ] No IX].', 'History per patient: car accidents in 2019 and 2022 with nec']
  f_r1_1 pre_existing | verified | Mention of a prior or pre-existing condition | ev: ['Problem list: hypertension, type 2 diabetes, chronic low bac']
  f_r1_2 pre_existing | needs_review | Mention of a prior or pre-existing condition | ev: ['History per patient: car accidents in 2019 and 2022 with nec']
  f_r6_1 pre_existing | needs_review | Mention of a prior or pre-existing condition | ev: ['Prior accidents?']
  f_r6_2 pre_existing | needs_review | Mention of a prior or pre-existing condition | ev: ['Prior injuries?']
  f_r2_1 causation | verified | Scene facts | ev: ['Ambulatory at scene.']
  f_r4_1 causation | needs_review | Attorney referral | ev: ['Letter of protection to Fennimoor Spine Clinic.']
  f_r5_1 causation | verified | Attorney referral | ev: ['Patient referred by attorney.']
  f_r5_2 causation | needs_review | Attorney referral | ev: ['Treating under a letter of protection.']
  f_r9_1 causation | needs_review | Attorney referral | ev: ['Account held under letter of protection.']

AMOUNTS
  a1 charge 326000 | verified [] | Dx: cervical strain, lumbar strain. X-ray cervical and lumba | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
  a2 unclear 25000 | needs_review ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | A second AI check disagreed with the first result for this item. The line states no date of service, so it is not an ite
  a3 unclear 18000 | needs_review ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | A second AI check disagreed with the first result for this item. The line states no date of service, so it is not an ite
  a4 unclear 231000 | needs_review ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | A second AI check disagreed with the first result for this item. The line states no date of service, so it is not an ite
  a5 unclear 274000 | needs_review ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | A second AI check disagreed with the first result for this item. Total or subtotal line: it repeats the charges listed w
  a6 unclear 30000 | needs_review ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | A second AI check disagreed with the first result for this item. Payment: money received, not a charge.
  a7 unclear 27400 | needs_review ['AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
  a8 unclear 216600 | needs_review ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR'] | Itemized ledger, statement date 06/15/2026. New patient exam | A second AI check disagreed with the first result for this item. Balance or amount due: worked out from charges, payment

TRAY [('f_r4_2', 'flag', ['JUDGE_DISAGREES', 'LLM_ONLY']), ('f_r6_3', 'flag', ['JUDGE_DISAGREES', 'LLM_ONLY'])]
TRAY_FILTERED count 1
TOTALS {"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 326000, "count": 1, "label": "Pending review"}, "detected_not_a_total": {"cents": 326000, "count": 1, "label": "Detected (not a total)"}, "flagged_charges": [], "not_totaled": [{"id": "a2", "kind": "unclear", "text": "$250.00"}, {"id": "a3", "kind": "unclear", "text": "$180.00"}, {"id": "a4", "kind": "unclear"

EXPORT BEFORE DECISIONS 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "Nothing is accepted or edited yet, so the letter would be em

ACCEPT RESULTS {'e1': (200, None), 'e2': (200, None), 'e3': (200, None), 'e4': (200, None), 'e5': (200, None), 'e6': (200, None), 'e7': (200, None), 'e8': (200, None), 'e9': (422, 'CODE_CHECK_FAILED'), 'f_gap_r7_r8': (200, None), 'f_cx1': (200, None), 'f_cx2': (200, None), 'f_r1_1': (200, None), 'f_r1_2': (200, None), 'f_r6_1': (200, None), 'f_r6_2': (200, None), 'f_r2_1': (200, None), 'f_r4_1': (200, None), 'f_r5_1': (200, None), 'f_r5_2': (200, None), 'f_r9_1': (200, None), 'a1': (200, None), 'a2': (200, None), 'a3': (200, None), 'a4': (200, None), 'a5': (200, None), 'a6': (200, None), 'a7': (200, None), 'a8': (200, None)}

EXPORT 200
----- LETTER -----
TREATMENT CHRONOLOGY

March 4, 2026 — Dr. Hesper Alderton, primary care
Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
Source [Ex. __ / Bates __]: "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."

March 18, 2026 — Ashgrove Fire-Rescue run report
Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED.
Source [Ex. __ / Bates __]: "Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."

March 18, 2026 — Wexcombe Memorial ED
Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negative for fracture.
Source [Ex. __ / Bates __]: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture."

March 26, 2026 — Pellingham and Rook PLLC, correspondence (letter of protection)
Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending.
Source [Ex. __ / Bates __]: "This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending."

March 27, 2026 — Fennimoor Spine Clinic, new patient
Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.
Source [Ex. __ / Bates __]: "Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."

March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)
Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuries marked No; pain today 7.
Source [Ex. __ / Bates __]: "How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7."

April 24, 2026 — Fennimoor Spine Clinic, visit 8
Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.
Source [Ex. __ / Bates __]: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."

May 29, 2026 — Fennimoor Spine Clinic, visit 14
Neck pain 4/10, low back pain 5/10. Care continues.
Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."

BILLED CHARGES

Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."

Billed charges accepted from these records: $3,260.00
----- NOTES -----
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 1.

FLAGS ACCEPTED
- Gap: 35 days, April 24, 2026 to May 29, 2026: record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026) to record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026).
- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents? Yes [ ] No [X]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries? Yes [ ] No IX]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
- Prior condition: record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Problem list: hypertension, type 2 diabetes, chronic low back pain."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents?"; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries?".
- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to Fennimoor Spine Clinic."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Patient referred by attorney."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Treating under a letter of protection."; record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) "Account held under letter of protection."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Dr. Hesper Alderton, primary care, March 4, 2026): "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy." Conflict, other fact mismatch; prior condition.
- Record 2 (Ashgrove Fire-Rescue run report, March 18, 2026): "Ambulatory at scene." Causation language.
- Record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026): "Treating under a letter of protection." Causation language.
- Record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026): "Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]." Conflict, other fact mismatch; prior condition.
- Record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026): "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued." Gap.
- Record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026): "Neck pain 4/10, low back pain 5/10. Care continues." Gap.

AMOUNTS NOT TOTALED
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "New patient exam charge $250.00" Not totaled ($250.00): The line states no date of service, so it is not an itemized service line and is not totaled.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "x-ray charge $180.00" Not totaled ($180.00): The line states no date of service, so it is not an itemized service line and is not totaled.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "treatment visits 1 through 14 charge $2,310.00" Not totaled ($2,310.00): The line states no date of service, so it is not an itemized service line and is not totaled.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00." Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00." Not totaled ($300.00): Payment: money received, not a charge.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00." Not totaled ($2,166.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.

DAMAGES MENTIONS (not charges)
- none

FUTURE TREATMENT RECOMMENDED (no cost stated)
- none
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:39.281Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && grep \"^  e[0-9]\" journey-lib11.out; grep -n \"Record 1\\b\\|Alderton\" -A6 /Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.txt | head -20",
 "description": "Show lib11 entries and record 1 text"
}
````

### User / tool · 2026-11-02T20:00:39.448Z

**tool result**
````
  e1 2026-03-04 | Dr. Hesper Alderton, primary care | needs_review ['JUDGE_PARTIAL'] | Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back
  e2 2026-03-18 | Ashgrove Fire-Rescue run report | needs_review ['JUDGE_PARTIAL'] | Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind;
  e3 2026-03-18 | Wexcombe Memorial ED | verified [] | Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negativ
  e4 2026-03-26 | Pellingham and Rook PLLC, correspondence (letter of protection) | needs_review ['JUDGE_PARTIAL'] | Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the cli
  e5 2026-03-27 | Fennimoor Spine Clinic, new patient | verified [] | Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chir
  e6 2026-03-27 | Fennimoor Spine Clinic, new patient intake form (OCR text) | verified [] | Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuri
  e7 2026-04-24 | Fennimoor Spine Clinic, visit 8 | verified [] | Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.
  e8 2026-05-29 | Fennimoor Spine Clinic, visit 14 | verified [] | Neck pain 4/10, low back pain 5/10. Care continues.
  e9 2026-06-15 | Fennimoor Spine Clinic, itemized ledger | needs_review ['CHARGE_TEXT_IN_ENTRY'] | Itemized ledger lists new patient exam charge $250.00, x-ray charge $180.00, treatment vis
3:=== Record 1 ===
4-Date: 2026-03-04
5:Source: Dr. Hesper Alderton, primary care
6-Excerpt: "Annual visit. History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. Problem list: hypertension, type 2 diabetes, chronic low back pain. Low back pain 3/10 today."
7-
8-=== Record 2 ===
9-Date: 2026-03-18
10-Source: Ashgrove Fire-Rescue run report
11-Excerpt: "Passenger vehicle struck from behind. Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:51.726Z

**tool call — Bash**
````
{
 "command": "ls app/frontend; grep -n \"needs_review\" app/frontend/*.js | grep -i \"accept\\|confirm\" | head -20",
 "description": "Check frontend handling of accept on needs_review"
}
````

### User / tool · 2026-11-02T20:00:51.833Z

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
app/frontend/dom.js:59:  ZL.comparedEdit = (i) => !!i && i.review_status === "accepted" && i.state === "needs_review" && !!i.edited && !ZL.editToCheck(i);
app/frontend/mock.js:94:      else { e.state = "needs_review"; e.reasons = ["DATE_AMBIGUOUS"]; e.why = "The date can be read two ways; confirm which one is right."; undated.push(e);
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:54.203Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c 'import playwright; print(\"ok\")'; grep -n \"data-testid\" app/frontend/timeline.js | head -30",
 "description": "Check playwright and timeline test ids"
}
````

### User / tool · 2026-11-02T20:00:54.341Z

**tool result**
````
ok
28:      el("span", { class: "chip chip--" + t[0], "data-icon": t[1], "data-testid": "entry-state" }, cmp ? "Compared by you" : STATE_LABEL[e.state] || e.state),
29:      d ? el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status) : null);
37:      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt));
39:    const more = el("button", { type: "button", class: "btn btn--link quote-more", "data-testid": "btn-show-excerpt", "aria-expanded": String(fullQuotes.has(e.id)), "aria-label": label(fullQuotes.has(e.id)),
50:    const row = el("article", { class: "entry st-" + e.state + (openRows.has(e.id) ? " is-open" : ""), "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
56:        e.date ? ZL.timeEl(e.date, { class: "date", "data-testid": "entry-date" }) : el("span", { class: "chip chip--warn", "data-icon": "calendar", "data-testid": "entry-date" }, "Date to confirm"),
57:        el("span", { class: "provider", "data-testid": "entry-provider" }, (!e.date && rec ? `Record ${rec.seq}: ` : "") + e.provider),
59:        reasonText_ ? el("p", { class: "reason" + (e.reasons.includes("AI_TRANSLATION") ? " reason--caution" : ""), "data-testid": "entry-reasons", title: fullReason(e) }, reasonText_) : null,
61:      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
62:      e.edited ? el("p", { class: "muted small note", "data-testid": "edited-note" }, e.edited.original_summary != null
67:      el("div", { class: "row-actions", "data-testid": "row-actions" },
68:        el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-why", "aria-label": "Why this status: " + e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : ""), onclick: () => openWhy(e.id) }, "Why this status"),
69:        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": `Open record ${rec ? rec.seq : ""} for ${e.provider}`, onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"),
75:      const rest = Array.from(ra.children).filter((b) => b.getAttribute("data-testid") !== "btn-source");
87:    const body = el("div", { class: "timeline", "data-testid": "dismissed-queue" }, rows.map((e) => entryRow(e, c)));
88:    const d = el("details", { class: "dismissed-group", "data-testid": "dismissed-group", open: ZL.dismissedOpen || null },
89:      el("summary", { "data-testid": "dismissed-summary" }, `Dismissed (${rows.length})`, el("span", { class: "muted small" }, " Not in the letter. Open to read them or press Undo."), ZL.rv.rerunMarker(body)),
152:    const left = ZL.$('[data-testid="missing-entry"][data-record-id="' + recordId + '"]');
158:      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
166:    return el("section", { class: "notice notice--info", "data-testid": "gap-change-note", role: "status", "aria-label": "Gap figures changed" },
168:      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-dismiss-gap-note", onclick: (ev) => { gapNote = null; ev.target.closest("section").remove(); } }, "Got it"));
172:    const box = el("section", { class: "group" + (none ? " group--empty" : ""), "data-testid": "dates-to-confirm", "aria-labelledby": "h-dates" }, el("h2", { id: "h-dates" }, "Dates to confirm"));
181:      d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
184:      if (d.suggestion && d.suggestion.reason) bar.append(el("p", { class: "muted small", "data-testid": "date-suggestion-reason" }, "Hint: " + d.suggestion.reason + ". It does not point to one date, so none is selected."));
203:      const row = el("article", { class: "entry undated", "data-testid": "date-to-confirm-item", "data-record-id": d.record_id },
205:        quote ? el("blockquote", { class: "excerpt", "data-testid": "date-to-confirm-excerpt" }, quote) : null);
207:      row.append(el("p", { class: "muted small", "data-testid": "date-to-confirm-note" }, "No entry was drafted for this record. After you pick the date it is listed under Records without an entry, where you enter it by hand."));
208:      if (rec) row.append(el("div", { class: "row-actions" }, el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", onclick: () => ZL.openSource([{ record_id: rec.id, start: null, end: null }], `Record ${rec.seq}: ${rec.source_label}`) }, `Open record ${rec.seq}`)));
218:    const box = el("section", { class: "group tray" + (c.tray.length ? "" : " group--empty"), "data-testid": "rejected-tray", "aria-labelledby": "h-tray" }, el("h2", { id: "h-tray" }, `Could not verify (${c.tray.length})`));
224:      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id, "data-tray-kind": t.kind || "entry" },
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:00:55.256Z

Let me drive the UI with Playwright to see how a judge-disputed entry looks and accepts.

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:06.341Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/ui_walk.py",
 "description": "x",
 "content": "\"\"\"GATE-M3 PM UI walk: open a fresh lib11 case and the sample in the browser, screenshot, try Accept on a judge-partial entry.\nUsage: python3 -I ui_walk.py http://127.0.0.1:7973 <outdir>\"\"\"\nimport json, sys, time, urllib.request\nfrom playwright.sync_api import sync_playwright\n\nBASE, OUT = sys.argv[1], sys.argv[2]\n\n\ndef post(path, body):\n    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), method=\"POST\", headers={\"Content-Type\": \"application/json\"})\n    with urllib.request.urlopen(req) as r:\n        return json.loads(r.read())\n\n\ndef get(path):\n    with urllib.request.urlopen(BASE + path) as r:\n        return json.loads(r.read())\n\n\ndef fresh(body):\n    tok = post(\"/api/cases\", body)[\"token\"]\n    post(f\"/api/cases/{tok}/run\", {\"confirm_rerun\": False})\n    for _ in range(60):\n        if get(f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(1)\n    return tok\n\n\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    dialogs = []\n    pg.on(\"dialog\", lambda d: (dialogs.append(d.message), d.dismiss()))\n    # lib11\n    tok = fresh({\"library\": \"case_lib11_priors_and_ledger\"})\n    pg.goto(f\"{BASE}/#/case/{tok}\")\n    pg.wait_for_timeout(2500)\n    if not pg.locator('[data-entry-id=\"e2\"]').count():\n        pg.goto(f\"{BASE}/?case={tok}\")\n        pg.wait_for_timeout(2500)\n    print(\"URL\", pg.url)\n    body = pg.inner_text(\"body\")\n    print(\"BANNER synthetic:\", \"Synthetic data only\" in body)\n    pg.screenshot(path=f\"{OUT}/01-lib11-top.png\", full_page=False)\n    row = pg.locator('[data-entry-id=\"e2\"]').first\n    print(\"e2 rows found\", pg.locator('[data-entry-id=\"e2\"]').count())\n    if row.count():\n        row.scroll_into_view_if_needed()\n        print(\"E2 ROW TEXT:\\n\", row.inner_text()[:900])\n        row.screenshot(path=f\"{OUT}/02-lib11-e2-row.png\")\n        acc = pg.locator('[data-controls-for=\"e2\"] [data-action=\"accept\"]').first\n        if not acc.count():\n            acc = row.locator('[data-action=\"accept\"]').first\n        print(\"accept buttons\", acc.count())\n        if acc.count():\n            acc.click()\n            pg.wait_for_timeout(1200)\n            print(\"DIALOGS\", dialogs)\n            mod = pg.locator('[role=\"dialog\"]:visible, dialog[open]')\n            print(\"visible dialogs after accept\", mod.count(), (mod.first.inner_text()[:400] if mod.count() else \"\"))\n            it = get(f\"/api/cases/{tok}/items/e2\")\n            itm = it.get(\"item\", it)\n            print(\"E2 AFTER CLICK review_status\", itm.get(\"review_status\"), \"state\", itm.get(\"state\"))\n            pg.screenshot(path=f\"{OUT}/03-lib11-after-accept-e2.png\")\n    # sample overview\n    tok2 = fresh({\"sample\": True})\n    pg.goto(f\"{BASE}/#/case/{tok2}\")\n    pg.wait_for_timeout(2500)\n    pg.screenshot(path=f\"{OUT}/04-sample-top.png\", full_page=True)\n    t = pg.inner_text(\"body\")\n    for needle in (\"Gap of 73 days\", \"$185\", \"8,390\", \"not a total\", \"Accepted charges\", \"Could not verify\"):\n        print(\"SAMPLE has\", repr(needle), needle in t)\n    b.close()\n"
}
````

### User / tool · 2026-11-02T20:01:06.504Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/ui_walk.py (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `description` was ignored.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:08.231Z

**tool call — Bash**
````
{
 "command": "grep -n \"location.hash\\|#/case\\|case=\" app/frontend/app.js app/frontend/switcher.js app/frontend/overview.js | head -8",
 "description": "Find frontend case URL routing"
}
````

### User / tool · 2026-11-02T20:01:08.407Z

**tool result**
````
app/frontend/switcher.js:23:    history.replaceState(null, "", "#/case/" + encodeURIComponent(token));
app/frontend/overview.js:108:    const a = el("a", { class: "cv-open", href: "#/case/" + encodeURIComponent(s.token), "data-testid": "cases-open", onclick: (ev) => {
app/frontend/overview.js:234:      if (push) history.pushState(null, "", "#/case/" + encodeURIComponent(token));
app/frontend/overview.js:253:    const m = /#\/case\/([^&/]+)/.exec(location.hash), s = ZL.state.get();
app/frontend/app.js:1:/* Bootstrap: health -> banners; restore case from #case=<token>; poll run status; render on every state change. */
app/frontend/app.js:141:    const m = /#\/case\/([^&/]+)/.exec(location.hash);
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:10.592Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && /Users/arsis/zlayt-pm-project/.venv/bin/python -I ui_walk.py http://127.0.0.1:7973 . 2>&1 | tee ui_walk.out | head -60",
 "description": "Run Playwright UI walk on lib11 and sample",
 "timeout": 240000
}
````

### User / tool · 2026-11-02T20:01:20.424Z

**tool result**
````
URL http://127.0.0.1:7973/#/case/l47HxqmIGUJxpPfub-u6Zg
BANNER synthetic: True
e2 rows found 1
E2 ROW TEXT:
 March 18, 2026
Ashgrove Fire-Rescue run report
Rec 2
Not in an entry (1)

A second AI check found the summary only partly supported by the quoted text.

Needs review

Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED.draft

Excerpt · Record 2 · Ashgrove Fire-Rescue run report
Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.
Accept
Edit
Dismiss
Open record
More
accept buttons 1
DIALOGS []
visible dialogs after accept 0 
E2 AFTER CLICK review_status accepted state needs_review
SAMPLE has 'Gap of 73 days' True
SAMPLE has '$185' True
SAMPLE has '8,390' True
SAMPLE has 'not a total' True
SAMPLE has 'Accepted charges' True
SAMPLE has 'Could not verify' True
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:21.589Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/02-lib11-e2-row.png"
}
````

### User / tool · 2026-11-02T20:01:21.600Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:33.320Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && TOK=$(grep TOKEN journey-lib11.out | awk '{print $2}'); curl -s -X POST -H 'Content-Type: application/json' -d '{\"action\":\"count\",\"confirm\":\"separate_charge\"}' http://127.0.0.1:7973/api/cases/$TOK/items/a3/review | python3 -c 'import json,sys; d=json.load(sys.stdin); i=d.get(\"item\",d); print(i.get(\"kind\"), i.get(\"review_status\"), i.get(\"why\",\"\")[:200])'; curl -s http://127.0.0.1:7973/api/cases/$TOK/export | python3 -c 'import json,sys; d=json.load(sys.stdin); t=d[\"letter_text\"]; print(t[t.index(\"BILLED CHARGES\"):])' | tee lib11-counted-letter.out",
 "description": "Count a no-date ledger line and check letter date"
}
````

### User / tool · 2026-11-02T20:01:33.570Z

**tool result**
````
amount accepted You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no AI check was asked about it.
BILLED CHARGES

Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"

Billed charges accepted from these records: $3,440.00
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:40.042Z

**tool call — Bash**
````
{
 "command": "grep -l \"statement date\\|statement dated\" board/cards/*.md | head; grep -n \"F4\\|statement dated\" board/cards/T-17[4-9].md | head",
 "description": "Search cards for the statement-date letter finding"
}
````

### User / tool · 2026-11-02T20:01:40.262Z

**tool result**
````
board/cards/T-140.md
board/cards/T-174.md
board/cards/T-174.md:37:    - [minor] Letter prints a counted ledger line with the statement date as if it were the service date — fix: For a counted line with no service date, print 'itemized ledger (statement dated June 15, 2026)'.
board/cards/T-174.md:48:R2. What changed: F15 a paste the demo does not run (real 409 at create, no stub) now says so plainly and offers Open the sample, Choose a library case (only where the library is on the page) and one line on running live (ENABLE_LIVE=1); run-start 500 no longer says Try again twice. Counted line: neutral 'Counted by you' chip plus her confirm said once (server why hidden, no amber, no flag wording; chip wraps inside its cell; Audit/Why note the same). F14: preview deleted on reload/close/Back (pagehide keepalive DELETE, hash reset). How verified: full e2e from git archive tree c720fc4 own port E2E_REQUIRE_DB=1 384 passed; 6 new specs red on HEAD first. Left: Undo of a count leaves a pending Charge (backend; filed T-176; the row now says Count taken back); letter 'statement dated' wording (backend/export) not done; focus-after-run nit untouched. Surprised: the shared git index has others' staged deletions, so trees come from a temp index.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:44.377Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7973/api/health | python3 -m json.tool | head -40; head -5 app/frontend/narrative.js; grep -n \"narrative\" app/frontend/index.html app/frontend/app.js | head",
 "description": "Check health features and narrative wiring"
}
````

### User / tool · 2026-11-02T20:01:44.587Z

**tool result**
````
{
    "ok": true,
    "version": "0.1.0",
    "synthetic_only": true,
    "banner": "Synthetic data only \u2014 never paste real records",
    "backend": "fixture",
    "demo_mode": true,
    "live_enabled": false,
    "models": {
        "generator": "claude-sonnet-5-5",
        "judge": "claude-haiku-5-5"
    },
    "limits": {
        "max_chars": 60000,
        "max_records": 40
    },
    "retention_hours": 24,
    "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
    "sample_available": true
}
/* Draft treatment paragraph (T-059, D-031): drafted by the server from ACCEPTED entries only, every sentence cited and checked. Shown with the
   internal notes; it enters the letter only after the paralegal accepts it. GET/POST /narrative, POST /narrative/review. Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  const cache = {};   // token -> {nar|null} | {loading:true}
app/frontend/index.html:87:<script src="narrative.js"></script>
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:47.456Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && TOK=$(grep TOKEN journey-sample.out | awk '{print $2}'); curl -s http://127.0.0.1:7973/api/cases/$TOK/narrative | head -c 1500; echo; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py show T-059 | grep -E \"status|^  - \\{\\\"n\\\"\" | head; grep -n \"narrative\\|paragraph\" app/frontend/export.js | head -5",
 "description": "Probe the draft paragraph feature on the sample"
}
````

### User / tool · 2026-11-02T20:01:47.712Z

**tool result**
````
{"narrative":null}
status: "blocked"
  - {"n": 1, "text": "every sentence carries a citation to an accepted entry; unsupported sentence -> removed with reason (test with seeded hallucination)", "done": true, "evidence": "tests/unit/test_narrative.py::test_each_code_check_removes_a_seeded_sentence_with_its_own_reason (12 exact-reason cases, no j1 call), test_sentence_citing_an_entry_that_is_not_accepted_is_removed, judge tests; mutant dropping the D-006 token check now fails 5 tests"}
  - {"n": 2, "text": "never contains flag content, adverse facts not in accepted entries, or causation language not quoted (test)", "done": true, "evidence": "tests/unit/test_narrative.py: exact reason per check (CAUSATION_NOT_QUOTED, FLAG_CONTENT, SEVERITY_NOT_QUOTED new code backstop for severity/outcome words), test_entry_edited_after_the_draft_drops_its_sentence_from_the_letter (kills stale-basis mutant), only-accepted-entries test"}
  - {"n": 3, "text": "eval: 0 unsupported sentences across 3 runs on the sample (live backend) recorded in evals report", "done": false, "evidence": null}
    - [minor] A failed re-draft overwrites an accepted paragraph, and neither the failure path nor the routes are tested — fix: On failure, keep the existing narrative and return the error separately (or store it under narrative.error without clearing sentences/status). Add tests: failure path (stub raising AU.LLMFailed, and an invalid schema), and route tests for GET before draft, POST with no ac
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:52.331Z

**tool call — Bash**
````
{
 "command": "grep -n \"live_enabled\\|demo_mode\\|rerun_available\\|btn-\\|POST\" app/frontend/narrative.js | head -20; TOK=$(grep TOKEN artifacts/review-evidence/GATE-M3-pm/journey-sample.out | awk '{print $2}'); curl -s -X POST -H 'Content-Type: application/json' -d '{}' http://127.0.0.1:7973/api/cases/$TOK/narrative | head -c 800; echo",
 "description": "Check narrative UI gating and try drafting"
}
````

### User / tool · 2026-11-02T20:01:52.585Z

**tool result**
````
2:   internal notes; it enters the letter only after the paralegal accepts it. GET/POST /narrative, POST /narrative/review. Text via ZL.el only. */
27:      const r = await RV.http("POST", base(c.token) + path, body);
50:      root.append(...[el("div", { class: "rv-actions" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-draft-narrative", disabled: accepted === 0, onclick: () => call(c, "", {}, "Draft written. Read each sentence before you accept it.") }, "Draft paragraph from accepted entries")),
67:        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-accept-narrative", "aria-pressed": String(nar.status === "accepted"), disabled: !(nar.sentences || []).length, onclick: () => act("accept", "Paragraph accepted.") }, "Accept paragraph"),
68:        el("button", { type: "button", class: "btn", "data-testid": "btn-dismiss-narrative", "aria-pressed": String(nar.status === "dismissed"), onclick: () => act("dismiss", "Paragraph dismissed.") }, "Dismiss"),
69:        nar.status !== "pending" ? el("button", { type: "button", class: "btn", "data-testid": "btn-reset-narrative", onclick: () => act("reset", "Paragraph back to draft.") }, "Reset") : null,
70:        el("button", { type: "button", class: "btn", "data-testid": "btn-redraft-narrative", disabled: accepted === 0, onclick: () => call(c, "", {}, "New draft written. Read each sentence before you accept it.") }, "Draft again")));
{"narrative":{"status":"pending","generated_at":"2026-11-02T20:01:52Z","sentences":[{"id":"ns1","entry_id":"e1","text":"On January 9, 2026, Austin EMS run report: Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.","code_checks":{"reasons":[]},"judge":{"model":"claude-haiku-5-5","prompt_version":"judge_faithfulness_v1","call_id":"cdaa0e049eece","verdict":"supported","reason_code":"NONE"},"cite":"record 1 (Austin EMS run report, January 9, 2026)"},{"id":"ns2","entry_id":"e2","text":"On January 9, 2026, Central ER discharge summary: Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.","code_checks":{"
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:01:56.493Z

**tool call — Bash**
````
{
 "command": "TOK=$(grep TOKEN artifacts/review-evidence/GATE-M3-pm/journey-sample.out | awk '{print $2}'); curl -s -X POST -H 'Content-Type: application/json' -d '{\"action\":\"accept\"}' http://127.0.0.1:7973/api/cases/$TOK/narrative/review | head -c 200; echo; curl -s http://127.0.0.1:7973/api/cases/$TOK/export | python3 -c 'import json,sys; d=json.load(sys.stdin); t=d[\"letter_text\"]; i=t.find(\"BILLED\"); print(t[:300]); print(\"...\"); print(t[i-1500:i])' | tee artifacts/review-evidence/GATE-M3-pm/sample-narrative-letter.out",
 "description": "Accept the draft paragraph and view letter"
}
````

### User / tool · 2026-11-02T20:01:56.700Z

**tool result**
````
{"narrative":{"basis":{"e1":"878d72cc5fa5c917","e2":"6118756b5fde7cd7","e3":"4217797834f2a07d","e4":"199dc1b8d6a6fd98","e5":"7e2f2d58621e3f29","e6":"de8c4688dd32244f","e7":"000937058f032c11","e8":"d47
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10
...
ischarge summary: Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week. (Central ER discharge summary, January 9, 2026)
On January 16, 2026, Dr. Alvarez, primary care: Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks. (Dr. Alvarez, primary care, January 16, 2026)
On January 23, 2026, Capital PT, initial evaluation: Cervical range of motion reduced approx. 40%; plan of care 12 visits. (Capital PT, initial evaluation, January 23, 2026)
On February 20, 2026, Capital PT, visit 8: Pain 4/10, improving. (Capital PT, visit 8, February 20, 2026)
On March 6, 2026, Capital PT, visit 9: Discharged from PT after two missed appointments; pain 3/10. (Capital PT, visit 9, March 6, 2026)
On May 18, 2026, Hill Country Pain Management, new patient: New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered. (Hill Country Pain Management, new patient, May 18, 2026)
On May 29, 2026, Austin Imaging, cervical MRI: C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically. (Austin Imaging, cervical MRI, May 29, 2026)
On June 12, 2026, Hill Country Pain Management, follow-up: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. (Hill Country Pain Management, follow-up, June 12, 2026)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:01.499Z

**tool call — Bash**
````
{
 "command": "grep -ci \"narrative\" evals/reports/20261102T164038Z.md evals/run.py; grep -n \"ship_bar\\|grounding_rate\\|entry_recall\\|amount_recall\\|unsupported\\|determinism\\|hallucination\\|flag_precision\\|flag_recall\" evals/reports/20261102T164038Z.md | head -30",
 "description": "Check eval coverage of the narrative and ship-bar numbers"
}
````

### User / tool · 2026-11-02T20:02:01.645Z

**tool result**
````
evals/run.py:0
evals/reports/20261102T164038Z.md:1
3:**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
8:| grounding_rate | 1.000 (242 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
9:| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
10:| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
11:| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
12:| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
13:| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
14:| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
15:| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
16:| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
17:| unsupported_count_3run | 0 | 0 | R-TL-4 |
18:| determinism_3run | 1.0 | 1.0 | R-CO-7 |
128:- seeded hallucinations not caught: []
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:03.354Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"narrative\" evals/reports/20261102T164038Z.md; sed -n 1,7p evals/reports/20261102T164038Z.md; sed -n 19,60p evals/reports/20261102T164038Z.md",
 "description": "Read live eval report header and narrative mention"
}
````

### User / tool · 2026-11-02T20:02:03.513Z

**tool result**
````
149:- `app/llm/prompts/narrative_v1.md` 3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac
# Eval report 2026-11-02T16:40:38Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:07.626Z

**tool call — Bash**
````
{
 "command": "grep -n \"matched the record\\|def .*calib\" evals/run.py evals/*.py | head; python3 -c 'import json; d=json.load(open(\"evals/reports/calibration.json\")); print(json.dumps(d)[:1500])'",
 "description": "Find meaning of calibration matched counts"
}
````

### User / tool · 2026-11-02T20:02:07.772Z

**tool result**
````
evals/run.py:270:def score_calibration(exp, out, unscored=None):
evals/run.py:310:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
evals/run.py:321:    label = {"verified": "Verified items matched the record {m}/{t} times in testing",
evals/run.py:322:             "needs_review": "Items marked needs review matched the record {m}/{t} times in testing"}
evals/run.py:335:            sentences["by_type"][t][s] = (f"{('Verified' if s == 'verified' else 'Needs-review')} {noun[t]} matched the record {c['matched']}/{c['total']} "
evals/run.py:341:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
evals/run.py:1041:def render_calibration(c):
evals/run.py:1097:def write_calibration_refusal(src):
evals/run.py:1111:def write_report(r, outdir=REPORTS, write_calibration=False, scratch_ts=None):
evals/run.py:1153:def check_calibration(path, root=ROOT):
{"backend": "claude-cli", "by_state": {"needs_review": {"cases": ["case_01_date_formats", "case_03_rate_and_ocr", "case_07_prompt_injection", "case_09_nonvisit_hides_gap", "sample"], "matched": 11, "total": 11}, "verified": {"cases": ["case_01_date_formats", "case_02_gap_boundaries", "case_03_rate_and_ocr", "case_04_duplicates_no_amounts", "case_05_provider_conflict", "case_06_subtle_pre_existing", "case_07_prompt_injection", "case_08_diagnosis_temptation", "case_09_nonvisit_hides_gap", "sample"], "matched": 82, "total": 83}}, "by_type": {"amount": {"needs_review": {"by_case": {"case_03_rate_and_ocr": [3, 3], "case_07_prompt_injection": [1, 1], "sample": [2, 2]}, "matched": 6, "total": 6}, "verified": {"by_case": {"case_01_date_formats": [1, 1], "case_03_rate_and_ocr": [2, 2], "case_05_provider_conflict": [1, 1], "case_07_prompt_injection": [1, 1], "case_08_diagnosis_temptation": [1, 1], "case_09_nonvisit_hides_gap": [1, 1], "sample": [2, 2]}, "matched": 9, "total": 9}}, "entry": {"needs_review": {"by_case": {"case_01_date_formats": [1, 1], "case_03_rate_and_ocr": [1, 1], "case_07_prompt_injection": [1, 1], "case_09_nonvisit_hides_gap": [1, 1]}, "matched": 4, "total": 4}, "verified": {"by_case": {"case_01_date_formats": [7, 7], "case_02_gap_boundaries": [8, 8], "case_03_rate_and_ocr": [4, 4], "case_04_duplicates_no_amounts": [4, 4], "case_05_provider_conflict": [5, 5], "case_06_subtle_pre_existing": [4, 5], "case_07_prompt_injection": [3, 3], "case_08_diagnosis_temptation": [
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:10.993Z

**tool call — Bash**
````
{
 "command": "head -30 evals/reports/library-latest.md",
 "description": "Read library eval report header"
}
````

### User / tool · 2026-11-02T20:02:11.125Z

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

| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:15.952Z

**tool call — Bash**
````
{
 "command": "git log -3 --format='%h %ad %s' --date=iso -- evals/reports/library-latest.md; git log -1 --format='%h %ad' --date=iso a74b727; git rev-list --count a74b727..d0b04bc; sed -n 30,80p evals/reports/library-latest.md",
 "description": "Check library report age and failure detail"
}
````

### User / tool · 2026-11-02T20:02:16.483Z

**tool result**
````
ce70bd2 2026-11-02 00:34:27 -0600 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
328428f 2026-11-01 22:21:07 -0600 feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
a74b727 2026-11-02 00:34:10 -0600
231

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:20.350Z

**tool call — Bash**
````
{
 "command": "ls evals; grep -n \"argparse\\|add_argument\" evals/library_report.py 2>/dev/null | head; grep -rln \"library-latest\" evals/*.py tools/*.py 2>/dev/null",
 "description": "Find library report generator"
}
````

### User / tool · 2026-11-02T20:02:20.619Z

**tool result**
````
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
9:import argparse
76:    ap = argparse.ArgumentParser(prog="python -m evals.library_report")
77:    ap.add_argument("--out", default=str(R.ROOT / "evals" / "reports" / "library-latest.md"))
evals/library_report.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:21.947Z

**tool call — Bash**
````
{
 "command": "sed -n 1,100p evals/library_report.py",
 "description": "Read library report script"
}
````

### User / tool · 2026-11-02T20:02:22.103Z

**tool result**
````
#!/usr/bin/env python3
"""Library report (T-079): scores every evals/library packet with evals.run's scoring functions. REPORTED, NOT GATED (D-031): no exit code
depends on a score; the ship bar (evals.run) still measures only evals/golden. It only exits non-zero when a packet cannot be run at all.

Run:  .venv/bin/python -m evals.library_report [--out evals/reports/library-latest.md]     (fixture backend; no network)
Honest failures are shown, not hidden: a record whose extract call has no recorded fixture shows as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS),
the same rule as lib01.
"""
import argparse
import json
import pathlib
import subprocess
import sys

from evals import run as R

LIB = R.ROOT / "evals" / "library"


def expected_accept_all_cents(exp):
    """The total the letter should print when every acceptable line is accepted one at a time (D-059): `totals.accept_all_total` when the packet records one
    (with its written reason), else the hand-verified `explicit_charges_total`."""
    t = exp["totals"]
    return round(t.get("accept_all_total", t["explicit_charges_total"]) * 100)


def accept_all_total_cents(out):
    """T-140 / D-059: the total the letter would print if the paralegal accepted every amount the tool found (charges, unclear, rate, estimate) ONE AT A TIME,
    through the real export builder (export.build_export), not a sum of charge-class figures. A charge carrying a likely-duplicate or likely-total flag cannot
    be accepted without a named confirm, so it is not accepted here. Items rejected by the code check are not offered for review and are left out.
    None when the letter has no total line (no accepted charge)."""
    from app.backend import export
    case = dict(records=[dict(n=r["n"], source=r.get("source"), date_iso=r.get("date_iso"), excerpt=r["excerpt"], text=r.get("text") or r["excerpt"]) for r in out["records"]],
                entries=[], flags=[], pending_count=0, events=[],
                amounts=[dict(id=a["id"], record_no=a["record_nos"][0], cents=a["cents"], cls=a["kind"], raw=a["raw"], excerpt=a["excerpt"], review_status="accepted")
                         for a in out.get("amounts") or [] if a.get("state") != "rejected" and not a.get("confirm") and not (a.get("ladder") or {}).get("confirm")])
    for line in export.build_export(case)["letter_text"].splitlines():
        if line.startswith("Billed charges accepted from these records: $"):
            return round(float(line.rsplit("$", 1)[1].replace(",", "")) * 100)
    return None


def score(name, text, exp, pipeline):
    out = pipeline.run_case(text, "fixture")
    want = expected_accept_all_cents(exp)
    got = accept_all_total_cents(out)
    accept_all = "ok" if (got or 0) == want else f"WRONG {export_usd(got)} vs {export_usd(want)}"
    e, a, f = R.score_entries(exp, out), R.score_amounts(exp, out), R.score_flags(exp, out)
    errs = [(x.get("code"), x.get("record_no"), x.get("cause")) for x in out.get("errors") or []]
    must = sum(v["must"] for v in f["per_type"].values())
    found = sum(v["must_found"] for v in f["per_type"].values())
    return {"case": name, "accept_all": accept_all, "accept_all_ok": accept_all == "ok", "entries": f"{e['found']}/{e['total']}", "amounts": f"{a['found']}/{a['total']}", "total_ok": a["total_ok"],
            "must_flags": f"{found}/{must}", "must_not_flag_hits": len(f["must_not_flag_hits"]), "must_not_hits": R.check_must_not(exp, out),
            "gap_rows_wrong": len(f["gap_rows_wrong"]), "errors": errs, "status": out.get("status")}


def export_usd(cents):
    return "none" if cents is None else f"${cents // 100:,}.{cents % 100:02d}"


def _git(*args):
    try:
        return subprocess.run(["git", *args], cwd=R.ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:   # noqa: BLE001 - provenance is best effort; the report still prints
        return ""


def provenance():
    """Source commit and dirty state of the tree the report ran in (a report is only reproducible from a clean tree)."""
    sha = _git("rev-parse", "HEAD") or "unknown"
    dirty = [l for l in _git("status", "--porcelain", "--untracked-files=no").splitlines() if l.strip()]
    return sha, ("clean" if not dirty and sha != "unknown" else f"DIRTY ({len(dirty)} tracked paths differ)" if dirty else "unknown")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m evals.library_report")
    ap.add_argument("--out", default=str(R.ROOT / "evals" / "reports" / "library-latest.md"))
    a = ap.parse_args(argv)
    pipeline = R.load_pipeline()
    rows = []
    for p in sorted(LIB.glob("case_*.txt")):
        rows.append(score(p.stem, p.read_text(), json.loads(p.with_name(p.stem + ".expected.json").read_text()), pipeline))
    sha, state = provenance()
    lines = ["# Library report (reported, not gated)", "", f"Source commit: {sha} (tree: {state}). Regenerate from a clean worktree of the commit you cite.", "",
             "Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.", "",
             "| packet | status | entries | amounts | total ok | accept-all total | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['case']} | {r['status']} | {r['entries']} | {r['amounts']} | {r['total_ok']} | {r['accept_all']} | {r['must_flags']} | {r['must_not_flag_hits']} | "
                     f"{', '.join(r['must_not_hits']) or '-'} | {r['gap_rows_wrong']} | {'; '.join(f'{c} r{n} {k}' for c, n, k in r['errors']) or '-'} |")
    lines += ["", "## Known honest failures (generated from the run above)", ""]
    fails = [(r["case"], c, n, k) for r in rows for c, n, k in r["errors"]]
    if fails:
        lines += ["| packet | record | code | cause |", "|---|---|---|---|"] + [f"| {p} | r{n} | {c} | {k or 'not captured'} |" for p, c, n, k in fails]
    else:
        lines += ["None at this commit: every record of every packet replays from a recorded fixture on the fixture backend."]
    lines += ["", "History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt "
              "in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract "
              "(T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call)."]
    pathlib.Path(a.out).write_text("\n".join(lines) + "\n")
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:28.643Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/app-d0b04bc && LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.library_report --out /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md 2>&1 | tail -5; sed -n 1,25p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md",
 "description": "Regenerate library report at pinned commit",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:02:32.118Z

**tool result**
````
## Known honest failures (generated from the run above)

None at this commit: every record of every packet replays from a recorded fixture on the fixture backend.

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:42.705Z

**tool call — Bash**
````
{
 "command": "grep -n \"def score_flags\" -A40 evals/run.py | grep -n \"must_found\\|missed\\|return\" | head",
 "description": "Inspect score_flags return fields"
}
````

### User / tool · 2026-11-02T20:02:42.852Z

**tool result**
````
5:220-    per = {t: {"must": 0, "must_found": 0, "cands": 0, "cands_ok": 0} for t in FLAG_TYPES}
9:224-            per[g["type"]]["must_found"] += g["id"] in matched_ids
30:245-    return {"per_type": per, "missed_must": [g["id"] for g in golden if g["level"] == "must" and g["id"] not in matched_ids],
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:48.234Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/lib_missed.py",
 "content": "\"\"\"List missed must-flags per library packet (fixture backend). Run from a git-archive copy root: python -m ... not needed; pass root.\nUsage: cd <root> && python <this> lib08 lib10 lib13 lib15\"\"\"\nimport json, pathlib, sys\nsys.path.insert(0, \".\")\nfrom evals import run as R\n\npipeline = R.load_pipeline()\nfor stem in sorted(pathlib.Path(\"evals/library\").glob(\"case_*.txt\")):\n    if not any(k in stem.name for k in sys.argv[1:]):\n        continue\n    exp = json.loads(stem.with_name(stem.stem + \".expected.json\").read_text())\n    out = pipeline.run_case(stem.read_text(), \"fixture\")\n    f = R.score_flags(exp, out)\n    gold = {g[\"id\"]: g for g in exp.get(\"flags\", [])}\n    print(\"==\", stem.stem, \"missed_must\", f[\"missed_must\"], \"must_not_flag_hits\", f.get(\"must_not_flag_hits\"), \"gap_rows_wrong\", f.get(\"gap_rows_wrong\"))\n    for gid in f[\"missed_must\"]:\n        g = gold.get(gid, {})\n        print(\"   \", gid, g.get(\"type\"), \"|\", json.dumps({k: g.get(k) for k in (\"records\", \"record_ids\", \"evidence\", \"excerpt\", \"note\", \"why\") if g.get(k)})[:260])\n"
}
````

### User / tool · 2026-11-02T20:02:48.385Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/lib_missed.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:02:52.889Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/app-d0b04bc && LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/lib_missed.py lib08 lib09 lib10 lib13 lib15 2>&1 | tail -30",
 "description": "Dump missed must-flags on weak library packets",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:02:54.406Z

**tool result**
````
== case_lib08_second_crash_mri_after missed_must ['C1', 'C2'] must_not_flag_hits [] gap_rows_wrong []
    C1 conflict | {"evidence": [{"record_no": 9, "field": "excerpt", "excerpt": "Denies LOC per patient"}, {"record_no": 12, "field": "excerpt", "excerpt": "Patient states brief loss of consciousness at the second collision"}]}
    C2 conflict | {"evidence": [{"record_no": 3, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-12"}, {"record_no": 8, "field": "excerpt", "excerpt": "Restrained driver in a second collision"}]}
== case_lib09_spanish_interpreter_espalda missed_must ['C1'] must_not_flag_hits [] gap_rows_wrong []
    C1 conflict | {"evidence": [{"record_no": 1, "field": "excerpt", "excerpt": "Left shoulder pain 7/10"}, {"record_no": 3, "field": "excerpt", "excerpt": "Right shoulder pain 6/10"}]}
== case_lib10_eob_ub04_cms1500 missed_must ['G1'] must_not_flag_hits [{'must_not_flag': 'N1', 'candidate_type': 'gap'}] gap_rows_wrong [('2026-07-08', '2026-08-26', 49)]
    G1 gap | {"evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Continue home exercises"}, {"record_no": 9, "field": "excerpt", "excerpt": "Left knee pain 2/10"}]}
== case_lib13_cloned_notes_cross_provider missed_must ['C1', 'C3'] must_not_flag_hits [] gap_rows_wrong []
    C1 conflict | {"evidence": [{"record_no": 3, "field": "excerpt", "excerpt": "denies back pain"}, {"record_no": 4, "field": "excerpt", "excerpt": "Low back pain 8/10"}]}
    C3 conflict | {"evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Low back pain 8/10"}, {"record_no": 8, "field": "excerpt", "excerpt": "denies back pain"}]}
== case_lib15_conclusory_letter_mist missed_must ['C1', 'K1'] must_not_flag_hits [] gap_rows_wrong []
    C1 conflict | {"evidence": [{"record_no": 1, "field": "excerpt", "excerpt": "Minor damage to the rear bumper"}, {"record_no": 3, "field": "excerpt", "excerpt": "Patient states the impact was violent and she was thrown against the seat belt."}]}
    K1 causation | {"evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "The collision of 2026-10-04 caused all of the injuries and treatment described in this letter."}]}
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:03:00.259Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && python3 -I journey.py http://127.0.0.1:7973 case_lib08_second_crash_mri_after > journey-lib08.out 2>&1; sed -n '/^FLAGS/,/^AMOUNTS/p' journey-lib08.out; grep -c \"second collision\" journey-lib08.out; grep -n \"second collision\" journey-lib08.out | head",
 "description": "Run lib08 and check second-collision flagging"
}
````

### User / tool · 2026-11-02T20:03:01.696Z

**tool result**
````
FLAGS
  f_gap_r11_r12 gap | verified | Gap of 42 days | ev: ['Date: 2026-06-02', 'Source: Dr. Philippa Wenlock, orthopedics, follow-up']
  f_r12_1 causation | needs_review | Mention of another injury or event | ev: ['Patient states brief loss of consciousness at the second col']
  f_r1_1 causation | verified | Scene facts | ev: ['Ambulatory at scene.']
  f_r3_1 causation | verified | Accident date source | ev: ['Date of accident per intake form: 2026-01-12.']
  f_r8_1 causation | verified | Mention of another injury or event | ev: ['Restrained driver in a second collision, struck on the drive']

AMOUNTS
FLAGS ACCEPTED
- Gap: 42 days, June 2, 2026 to July 14, 2026: record 11 (Dr. Philippa Wenlock, orthopedics, follow-up, June 2, 2026) to record 12 (Dr. Ansgar Kellerman, neurology, July 14, 2026).
- Causation language: record 3 (Dr. Philippa Wenlock, orthopedics, new patient, January 16, 2026) "Date of accident per intake form: 2026-01-12."; record 12 (Dr. Ansgar Kellerman, neurology, July 14, 2026) "Patient states brief loss of consciousness at the second collision."; record 1 (Pelham Ridge EMS run report, January 12, 2026) "Ambulatory at scene."; record 8 (Pelham Ridge EMS run report, April 24, 2026) "Restrained driver in a second collision, struck on the driver side."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Pelham Ridge EMS run report, January 12, 2026): "Ambulatory at scene." Causation language.
- Record 3 (Dr. Philippa Wenlock, orthopedics, new patient, January 16, 2026): "Date of accident per intake form: 2026-01-12." Causation language.
- Record 8 (Pelham Ridge EMS run report, April 24, 2026): "Restrained driver in a second collision, struck on the driver side." Causation language.
- Record 11 (Dr. Philippa Wenlock, orthopedics, follow-up, June 2, 2026): "Neck pain 7/10 with left arm numbness since the rear-end collision of 2026-01-12. MRI reviewed. Recommend referral to neurosurgery." Gap.
- Record 12 (Dr. Ansgar Kellerman, neurology, July 14, 2026): "Patient states brief loss of consciousness at the second collision." Gap; causation language.

AMOUNTS NOT TOTALED
10
15:  e8 2026-04-24 | Pelham Ridge EMS run report | verified [] | Restrained driver struck on the driver side in a second collision had a hard cervical coll
19:  e12 2026-07-14 | Dr. Ansgar Kellerman, neurology | verified [] | Patient states brief loss of consciousness at the second collision, with headaches and wor
27:  f_r8_1 causation | verified | Mention of another injury or event | ev: ['Restrained driver in a second collision, struck on the drive']
76:Restrained driver struck on the driver side in a second collision had a hard cervical collar applied; patient states neck pain 8/10 and left arm numbness; transported to Thornbury Regional ED.
77:Source [Ex. __ / Bates __]: "Restrained driver in a second collision, struck on the driver side. Hard cervical collar applied. Pt states neck pain 8/10 and left arm numbness. Transported to Thornbury Regional ED."
92:Patient states brief loss of consciousness at the second collision, with headaches and word-finding difficulty since; referred for neuropsychological testing.
93:Source [Ex. __ / Bates __]: "Patient states brief loss of consciousness at the second collision. Headaches and word-finding difficulty since. Referred for neuropsychological testing."
112:- Causation language: record 3 (Dr. Philippa Wenlock, orthopedics, new patient, January 16, 2026) "Date of accident per intake form: 2026-01-12."; record 12 (Dr. Ansgar Kellerman, neurology, July 14, 2026) "Patient states brief loss of consciousness at the second collision."; record 1 (Pelham Ridge EMS run report, January 12, 2026) "Ambulatory at scene."; record 8 (Pelham Ridge EMS run report, April 24, 2026) "Restrained driver in a second collision, struck on the driver side."
120:- Record 8 (Pelham Ridge EMS run report, April 24, 2026): "Restrained driver in a second collision, struck on the driver side." Causation language.
122:- Record 12 (Dr. Ansgar Kellerman, neurology, July 14, 2026): "Patient states brief loss of consciousness at the second collision." Gap; causation language.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:03:10.730Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && python3 -I journey.py http://127.0.0.1:7973 case_lib10_eob_ub04_cms1500 > journey-lib10.out 2>&1; grep \"^  e[0-9]\\|gap\" journey-lib10.out | head -20; grep -n '\"G1\"\\|\"N1\"' -A6 /Users/arsis/zlayt-pm-project/evals/library/case_lib10_eob_ub04_cms1500.expected.json | head -30",
 "description": "Inspect lib10 gap handling"
}
````

### User / tool · 2026-11-02T20:03:12.288Z

**tool result**
````
CREATE 201 records 9 gap_flags ['f_gap_r8_r9'] warnings []
  e1 2026-06-09 | Rainhollow Fire-Rescue run report | needs_review ['JUDGE_PARTIAL'] | Driver of a pickup struck at an intersection; patient states chest wall and left knee pain
  e2 2026-06-09 | Saltmarrow General Hospital ED | verified [] | Diagnosed with left knee contusion and chest wall contusion; left knee X-ray negative for 
  e3 2026-06-12 | Saltmarrow General Hospital, discharge summary | verified [] | Discharged after 3 days of observation; diagnosis left knee contusion; follow up with orth
  e4 2026-06-19 | Saltmarrow General Hospital, UB-04 itemized bill | needs_review ['JUDGE_UNSUPPORTED'] | UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.
  e5 2026-06-24 | Dr. Ignatius Wardlaw, orthopedics, new patient | verified [] | Left knee pain 5/10; MRI of the left knee ordered.
  e6 2026-07-03 | Quoinmere Mutual Health Plan, EOB | verified [] | Explanation of benefits, not a bill.
  e7 2026-07-08 | Dr. Ignatius Wardlaw, orthopedics, follow-up | verified [] | Left knee pain 3/10. Injection performed. Continue home exercises.
  e8 2026-07-14 | Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim) | needs_review ['CHARGE_TEXT_IN_ENTRY'] | Claim lists CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units;
  e9 2026-08-26 | Dr. Ignatius Wardlaw, orthopedics, follow-up | verified [] | Left knee pain 2/10. Discharged from care.
  f_gap_r8_r9 gap | verified | Gap of 43 days | ev: ['Date: 2026-07-14', 'Source: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)']
ACCEPT RESULTS {'e1': (200, None), 'e2': (200, None), 'e3': (200, None), 'e4': (200, None), 'e5': (200, None), 'e6': (200, None), 'e7': (200, None), 'e8': (422, 'CODE_CHECK_FAILED'), 'e9': (200, None), 'f_gap_r8_r9': (200, None), 'f_r1_1': (200, None), 'a1': (200, None), 'a2': (200, None), 'a3': (200, None), 'a4': (200, None), 'a5': (200, None), 'a6': (200, None), 'a7': (200, None), 'a8': (200, None), 'a9': (200, None), 'a10': (200, None), 'a11': (200, None)}
564:      "id": "G1",
565-      "type": "gap",
566-      "level": "must",
567-      "from_date": "2026-07-08",
568-      "to_date": "2026-08-26",
569-      "days": 49,
570-      "cite": {
--
594:      "id": "N1",
595-      "type": "gap",
596-      "statement": "No gap flag for the 3, 12 and 14-day intervals; the UB-04 (record 4), EOB (record 6) and CMS-1500 (record 8) are not gap endpoints."
597-    }
598-  ],
599-  "tolerated": [
600-    {
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:03:19.607Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && TOK=$(grep TOKEN journey-lib10.out | awk '{print $2}'); curl -s http://127.0.0.1:7973/api/cases/$TOK | python3 -c '\nimport json,sys\nd=json.load(sys.stdin)\nfor f in d[\"flags\"]:\n    if f[\"type\"]==\"gap\": print(json.dumps({k:f.get(k) for k in (\"title\",\"explanation\",\"why\",\"warnings\",\"state\",\"reasons\",\"days\")}, indent=1)[:1500])\n'; grep -n \"Gap:\" journey-lib10.out",
 "description": "Show lib10 gap flag text and warnings"
}
````

### User / tool · 2026-11-02T20:03:19.774Z

**tool result**
````
{
 "title": "Gap of 43 days",
 "explanation": "Gap of 43 days between July 14, 2026 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)) and August 26, 2026 (Dr. Ignatius Wardlaw, orthopedics, follow-up). This gap starts at record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), which looks like paperwork, not a visit. Check whether treatment continued. If record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim) is paperwork, not a visit, the gap would be 49 days (July 8, 2026 to August 26, 2026).",
 "why": "This gap starts at record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), which looks like paperwork, not a visit. Check whether treatment continued. If record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim) is paperwork, not a visit, the gap would be 49 days (July 8, 2026 to August 26, 2026).",
 "warnings": null,
 "state": "verified",
 "reasons": [],
 "days": null
}
98:- Gap: 43 days, July 14, 2026 to August 26, 2026: record 8 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), July 14, 2026) to record 9 (Dr. Ignatius Wardlaw, orthopedics, follow-up, August 26, 2026).
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:03:31.788Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-031\\|D-063\\|reinstat\" memory/SCOPE_CUTS.md spec/REQUIREMENTS.md | head; grep -n \"^1[0-9]\\.\\|^[0-9]\\.\" spec/REQUIREMENTS.md | sed -n 1,3p; git log --oneline -1 -- spec/REQUIREMENTS.md; git log --oneline -1 -- memory/SCOPE_CUTS.md",
 "description": "Check whether reinstatements are reflected in cut lists"
}
````

### User / tool · 2026-11-02T20:03:31.967Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:03:40.938Z

**tool call — Bash**
````
{
 "command": "grep -n \"^### 8\\.\\|^## 8\" docs/CONTRACT.md; sed -n \"$(grep -n '^### 8.2' docs/CONTRACT.md | cut -d: -f1),+25p\" docs/CONTRACT.md",
 "description": "Read CONTRACT ship bar and regression sections"
}
````

### User / tool · 2026-11-02T20:03:41.043Z

**tool result**
````
408:## 8. Quality system
410:### 8.1 Sensors (all deterministic, all runnable with one command each, all run by qa before any gate)
417:### 8.2 The ship bar (these numbers are the product note's "good enough to ship" criteria; adjust only with an ADR)
424:### 8.3 Regression discipline
### 8.2 The ship bar (these numbers are the product note's "good enough to ship" criteria; adjust only with an ADR)
1. **Grounding:** 100% of exported statements and amounts carry a verbatim excerpt that exists in the input (automated; any failure is a blocker).
2. **Recall:** ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set.
3. **Flags:** per flag type, precision ≥ 0.9 and recall ≥ 0.9 against the golden flags; the 28-day near-miss must not flag; the 73-day gap must.
4. **No invented facts:** 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding); judge recall on seeded hallucinations ≥ 95%.
5. **Reviewability:** the paralegal persona completes the sample case end to end and rates "I could verify every claim quickly" ≥ 4/5; E2E export test green.

### 8.3 Regression discipline
Any change to a prompt, model, lexicon, or schema requires re-running `evals.run` before `in_review`; the eval report path goes in the card handoff. Store prompts in versioned files (`app/llm/prompts/*.md`) with a changelog line each.

---

## 9. Autonomy and continuity

- **Your loop, every cycle:** `board.py inbox` (act on Chris's notes first, acknowledge them in `PROGRESS.md`) → `board.py status` → ensure the active milestone has cards for all remaining scope → ensure every worker has a claimable card (message idle teammates by name) → dispatch Tier-1 reviews for `in_review` cards → triage returned reviews into verdicts and cards → run the gate when a milestone's cards are all done → rewrite `STATE.md`, append `PROGRESS.md`, commit → end turn only if nothing is actionable (the Stop hook will tell you).
- **Workers' loop:** claim via `board.py next` → read the card and relevant memory → do the work in their owned paths → tests → `board.py note` at each step → `board.py ac --check` with evidence → handoff section → `move in_review` → reply to you in ≤ 15 lines. `TeammateIdle` sends them back for the next card.
- **Heartbeat:** at the end of M0 create a scheduled task (ask Claude Code's cron tools, e.g., "every 20 minutes run: `python3 tools/board.py status --brief`; if any in-progress card has no note for 45 minutes, message its owner or reassign; if any teammate is idle with claimable work, assign it; if reviews are pending, dispatch them; append one line to `memory/PROGRESS.md`"). Scheduled tasks expire after a few days and live only in this session — recreate it after any restart.
- **Usage limits:** `autoContinueAtUsageLimit` is on; if the session pauses for a limit, it resumes by itself. Do not treat a pause as a reason to shrink scope.
- **Stalls:** the Stop hook's stall guard and the heartbeat handle you; you handle workers (45-minute rule). A teammate that errors out is replaced by spawning a fresh one with the same definition and the card's handoff notes.
- **Context hygiene:** keep subagent reports short; details live in files. Before any `/compact` risk (you'll feel it), rewrite `STATE.md`. After compaction, re-read `CLAUDE.md`, `STATE.md`, `board.py status`.
- **Restart protocol (for Chris, in RUNBOOK):** `claude --continue` → "Re-read memory/STATE.md and board status, re-spawn the worker teammates, recreate the heartbeat, continue." In-process teammates do not survive a restart; the board and memory do.
- **Stop sentinel:** `board/STOP` (or the board's STOP button) lets you stop at the next turn boundary; finish the current card handoff first.
- **Messages from Chris:** this session is likely connected to the Claude app through Remote Control, so Chris may type directly into this conversation from his phone or desktop. Treat such a message exactly like an inbox note: act on it, acknowledge it in `memory/PROGRESS.md`, keep the loop running. It never changes the rule that you do not ask him questions or wait for him; silence from Chris is the normal state.
- **Auth hygiene:** Remote Control requires claude.ai sign-in, so never `export ANTHROPIC_API_KEY` into the session's shell environment and never add it to a settings `env` block; the prototype's run script loads it from `.env` for the app process only.
- **Push notifications:** when Remote Control is connected you can request a mobile push in your own output. Do it exactly four times per milestone at most: gate started, gate passed or failed (one line with the verdict), and once if you hit the stall guard or move something to `needs_chris` that is P0. Never push for routine progress; the board carries that.
- **Agent teams caveats you must plan around:** one team per session; teammates cannot spawn teammates (reviewers are *your* subagents, dispatched by you); task-status lag is irrelevant because the board is truth; give each teammate its full context in the spawn prompt (they don't see your conversation); keep 4–6 teammates active, not more.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:03:45.504Z

**tool call — Bash**
````
{
 "command": "for f in $(ls -t reviews/*paralegal*.md | head -8); do echo \"$f $(git log -1 --format=%ad --date=format:%H:%M -- $f) $(grep -o '\"verify_quickly\": *[0-9]' $f | head -1) $(grep -o '\"verdict\": *\"[a-z]*\"' $f | head -1)\"; done",
 "description": "List latest paralegal reviews with scores"
}
````

### User / tool · 2026-11-02T20:03:46.509Z

**tool result**
````
reviews/GATE-M2-r2-paralegal.md  "verify_quickly": 4 "verdict": "changes"
reviews/T-149-paralegal-r2.md  "verify_quickly": 4 "verdict": "changes"
reviews/T-136-paralegal-r3.md  "verify_quickly": 4 "verdict":"unavailable"
reviews/T-149-paralegal.md  "verify_quickly": 3 "verdict": "changes"
reviews/T-136-paralegal-r2.md  "verify_quickly": 4 "verdict": "changes"
reviews/GATE-M2-paralegal.md  "verify_quickly": 4 "verdict": "fail"
reviews/T-136-paralegal.md  "verify_quickly": 3 "verdict": "changes"
reviews/T-060-paralegal-pass5.md  "verify_quickly": 4 "verdict": "changes"
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:04:01.246Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p app/backend/count_charge.py",
 "description": "Read count-charge rule code"
}
````

### User / tool · 2026-11-02T20:04:01.325Z

**tool result**
````
"""Count an amount the code held back for a missing detail (D-064, GATE-M2 r2 paralegal major; amends D-059/D-060).

Two kinds of 'not counted' amount. (a) Rule-excluded (total, balance, payment, adjustment, credit, year-to-date, insurer restatement, a note restating the same
provider's bill, a second figure on a line ...): never countable. (b) Held back only because the line lacks something D-060 needs (no date of service, a document with no
bill header): the paralegal reads the line and counts it with the named confirm "separate_charge" ("I checked this is a separate charge for a service").
`POST /api/cases/{token}/items/{id}/review {"action": "count", "confirm": "separate_charge"}`:
  - the amount must be countable (amounts.not_counted, computed from the record, never from anything the client sends), else 422 NOT_COUNTABLE with the plain reason;
  - the named confirm is required, else 422 CONFIRM_REQUIRED and nothing changes;
  - a figure that would double another line (same service and amount, any record; a date only has to agree when both lines state one, so an UNDATED line matching an accepted charge
    or another countable line always matches) or equals the sum of its record's charges also needs that flag named in `confirm_flag`; `separate_charge` alone is never enough then;
  - then the amount becomes class `charge` and is accepted in one step; the letter total sums it like any accepted charge. Two audit events are written: the count
    (action `reclassify`, `after.event == "count"`, `after.confirm` = the flag she confirmed) and the accept (carries the confirm stamp of the flag the charge now holds).
No model is asked: the class is a code reading plus a human confirm (ladder steps a and c), so the item is human-decided like a hand-written entry and the second AI check is not required."""
from app.backend import amounts as AM, confidence, language, reclassify, review, store
from app.db import db as DB

CONFIRM = AM.SEPARATE_CHARGE
NAME = "Counted as a separate charge"
MESSAGE = ("You counted this line as a separate charge for a service. If you take the decision back, you confirm that again to count it. "
           "Counting a line that is not a separate charge would count the same money twice.")
REQUIRED = ("Count this line only if you checked that it is a separate charge for a service, and not a total or a repeat of another line. "
            f"Confirm that by name ({CONFIRM}) to count it.")


def _flag(confirmed_at=None) -> dict:
    return {"flag": CONFIRM, "name": NAME, "message": MESSAGE, "confirm_with": CONFIRM, "of": None, **({"confirmed_at": confirmed_at} if confirmed_at else {})}


def is_counted(row: dict) -> bool:
    """True for an amount the paralegal counted through this route (human-decided: no second AI check applies to it)."""
    return bool((row.get("ladder") or {}).get("counted"))


def _err(code: str, text: str, **detail):
    return review.ReviewError(422, code, {"reason_code": code, **detail}, text)


def count(conn, case_id: str, item_id: str, body: dict, *, now=None) -> dict:
    t = review._now(now)
    kind, row = review._item(conn, case_id, item_id)
    if kind != "amount":
        raise review._bad("Only a dollar figure can be counted as a charge.")
    if row["state"] == "rejected":
        raise review.ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    confirm = (body or {}).get("confirm")
    confirm_flag = (body or {}).get("confirm_flag")
    for v in (confirm, confirm_flag):
        if v is not None and not isinstance(v, str):
            raise review._bad("The confirm must be the name of the flag.")
    from app.backend import present          # lazy: present imports review
    records = store.load_records(conn, case_id)
    rec = next((r for r in records if r["id"] == (row["record_ids"] or [None])[0]), None)
    if row["kind"] == "charge":
        raise _err("NOT_COUNTABLE", "This amount is already a charge. Accept it to count it.", item_id=item_id, not_counted_reason=None)
    info = present.not_counted_info(row, records)
    if not info["countable"]:
        raise _err("NOT_COUNTABLE", f"This amount cannot be counted. {info['reason']}", item_id=item_id, not_counted_reason=info["reason"])
    if confirm != CONFIRM:
        raise _err("CONFIRM_REQUIRED", REQUIRED + ("" if confirm is None else " The confirm you sent does not name it."), item_id=item_id, flag=CONFIRM, name=NAME,
                   confirm_with=CONFIRM, of=None, message=REQUIRED, not_counted_reason=info["reason"])
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:04:11.845Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && sed -n '/----- LETTER -----/,/----- NOTES -----/p' journey-lib10.out | grep -n -A2 \"UB-04\\|Fire-Rescue\"",
 "description": "Check if judge-unsupported lib10 entries reached letter"
}
````

### User / tool · 2026-11-02T20:04:11.973Z

**tool result**
````
4:June 9, 2026 — Rainhollow Fire-Rescue run report
5-Driver of a pickup struck at an intersection; patient states chest wall and left knee pain.
6-Source [Ex. __ / Bates __]: "Pt states chest wall and left knee pain."
--
16:June 19, 2026 — Saltmarrow General Hospital, UB-04 itemized bill
17:UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.
18:Source [Ex. __ / Bates __]: "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026."
19-
20-June 24, 2026 — Dr. Ignatius Wardlaw, orthopedics, new patient
--
38:Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $4,920.00
39-Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."
40:Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $2,105.00
41-Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
42:Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $386.50
43-Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."
44:Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $712.00
45-Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."
46-
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:04:16.243Z

**tool call — Bash**
````
{
 "command": "grep -n \"UB-04\" -A8 evals/library/case_lib10_eob_ub04_cms1500.txt | head -24; sed -n '/BILLED CHARGES/,/Billed charges accepted/p' artifacts/review-evidence/GATE-M3-pm/journey-lib10.out; grep -n \"accept_all_total\\|explicit_charges_total\" -A2 evals/library/case_lib10_eob_ub04_cms1500.expected.json | head",
 "description": "Compare lib10 UB-04 record with letter charges"
}
````

### User / tool · 2026-11-02T20:04:16.364Z

**tool result**
````
20:Source: Saltmarrow General Hospital, UB-04 itemized bill
21:Excerpt: "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 pharmacy, 14 units, FL47 total charges $386.50. Rev 0300 laboratory, 6 units, FL47 total charges $712.00. Rev 0001 total charges $8,123.50."
22-
23-=== Record 5 ===
24-Date: 2026-06-24
25-Source: Dr. Ignatius Wardlaw, orthopedics, new patient
26-Excerpt: "Left knee pain 5/10. MRI left knee ordered. Patient states his health plan was billed for the hospital stay."
27-
28-=== Record 6 ===
29-Date: 2026-07-03
BILLED CHARGES

Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $4,920.00
Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."
Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $2,105.00
Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $386.50
Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."
Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $712.00
Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."

Billed charges accepted from these records: $8,123.50
479:    "explicit_charges_total": 8123.5,
480-    "counted_amount_ids": [
481-      "A2",
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:04:28.253Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/lib_sweep.py",
 "content": "\"\"\"Sweep all library cases + sample: counts of needs_review, judge-disputed entries that a one-click accept would put in the letter.\nUsage: python3 -I lib_sweep.py http://127.0.0.1:7973\"\"\"\nimport json, sys, time, urllib.request, urllib.error\n\nBASE = sys.argv[1]\n\n\ndef call(method, path, body=None):\n    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None, method=method,\n                                 headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            return r.status, json.loads(r.read() or b\"{}\")\n    except urllib.error.HTTPError as e:\n        return e.code, json.loads(e.read() or b\"{}\")\n\n\n_, lib = call(\"GET\", \"/api/library\")\nids = [\"sample\"] + [c[\"id\"] for c in lib[\"cases\"]]\ntot = {\"items\": 0, \"nr\": 0, \"disputed\": 0, \"disputed_accept_ok\": 0}\nfor cid in ids:\n    _, c = call(\"POST\", \"/api/cases\", {\"sample\": True} if cid == \"sample\" else {\"library\": cid})\n    tok = c[\"token\"]\n    call(\"POST\", f\"/api/cases/{tok}/run\", {\"confirm_rerun\": False})\n    for _ in range(90):\n        _, st = call(\"GET\", f\"/api/cases/{tok}/status\")\n        if st[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(1)\n    _, case = call(\"GET\", f\"/api/cases/{tok}\")\n    items = case[\"entries\"] + case[\"flags\"] + case[\"amounts\"]\n    nr = [i for i in items if i[\"state\"] == \"needs_review\"]\n    disputed = [e for e in case[\"entries\"] if any(r in (\"JUDGE_PARTIAL\", \"JUDGE_UNSUPPORTED\") for r in e.get(\"reasons\") or [])]\n    ok = []\n    for e in disputed:\n        s, _ = call(\"POST\", f\"/api/cases/{tok}/items/{e['id']}/review\", {\"action\": \"accept\"})\n        if s == 200:\n            ok.append(e[\"id\"])\n    tot[\"items\"] += len(items); tot[\"nr\"] += len(nr); tot[\"disputed\"] += len(disputed); tot[\"disputed_accept_ok\"] += len(ok)\n    print(f\"{cid:48s} status={st['status']:6s} items={len(items):3d} needs_review={len(nr):3d} tray={len(case['tray']):2d} judge_disputed_entries={len(disputed)} accepted_with_one_click={len(ok)}\")\n    for e in disputed[:2]:\n        print(\"      \", e[\"id\"], e.get(\"reasons\"), \"| SUMMARY:\", (e.get(\"summary\") or \"\")[:110], \"| QUOTE:\", (e.get(\"excerpt\") or \"\")[:90])\n    call(\"DELETE\", f\"/api/cases/{tok}\")\nprint(\"TOTAL\", tot)\n"
}
````

### User / tool · 2026-11-02T20:04:28.451Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/lib_sweep.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:04:30.228Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && python3 -I lib_sweep.py http://127.0.0.1:7973 2>&1 | tee lib_sweep.out",
 "description": "Sweep all cases for judge-disputed one-click accepts",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:04:47.491Z

**tool result**
````
sample                                           status=ready  items= 23 needs_review=  3 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib01_er_only_then_gap                      status=ready  items= 10 needs_review=  2 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib02_slip_fall_prior_knee                  status=ready  items= 18 needs_review=  6 tray= 1 judge_disputed_entries=0 accepted_with_one_click=0
case_lib03_truck_rear_end_chiro                  status=ready  items= 14 needs_review=  4 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib04_dog_bite_scar_revision                status=ready  items= 11 needs_review=  2 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib05_pedestrian_orif_hardware              status=ready  items= 16 needs_review=  4 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib06_lop_billed_vs_adjusted                status=ready  items= 19 needs_review=  9 tray= 1 judge_disputed_entries=0 accepted_with_one_click=0
case_lib07_parking_lot_fall_outside_records      status=ready  items= 15 needs_review=  2 tray= 2 judge_disputed_entries=0 accepted_with_one_click=0
case_lib08_second_crash_mri_after                status=ready  items= 21 needs_review=  2 tray= 1 judge_disputed_entries=0 accepted_with_one_click=0
case_lib09_spanish_interpreter_espalda           status=ready  items= 18 needs_review= 12 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib10_eob_ub04_cms1500                      status=ready  items= 22 needs_review= 10 tray= 0 judge_disputed_entries=2 accepted_with_one_click=2
       e1 ['JUDGE_PARTIAL'] | SUMMARY: Driver of a pickup struck at an intersection; patient states chest wall and left knee pain. | QUOTE: Pt states chest wall and left knee pain.
       e4 ['JUDGE_UNSUPPORTED'] | SUMMARY: UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room. | QUOTE: UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026.
case_lib11_priors_and_ledger                     status=ready  items= 29 needs_review= 17 tray= 2 judge_disputed_entries=3 accepted_with_one_click=3
       e1 ['JUDGE_PARTIAL'] | SUMMARY: Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with  | QUOTE: History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated w
       e2 ['JUDGE_PARTIAL'] | SUMMARY: Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene | QUOTE: Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memori
case_lib12_records_review_credibility            status=ready  items= 25 needs_review= 11 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib13_cloned_notes_cross_provider           status=ready  items= 14 needs_review=  1 tray= 0 judge_disputed_entries=0 accepted_with_one_click=0
case_lib14_handwritten_chiro_scans               status=ready  items= 15 needs_review=  6 tray= 1 judge_disputed_entries=0 accepted_with_one_click=0
case_lib15_conclusory_letter_mist                status=ready  items= 27 needs_review= 15 tray= 1 judge_disputed_entries=0 accepted_with_one_click=0
TOTAL {'items': 297, 'nr': 106, 'disputed': 5, 'disputed_accept_ok': 5}
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:02.410Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/app-d0b04bc && P=/Users/arsis/zlayt-pm-project/.venv/bin/python; LLM_BACKEND=fixture $P -m evals.run --check-spec > /dev/null 2>&1; echo \"check-spec exit $?\"; LLM_BACKEND=fixture $P -m evals.letter_check 2>&1 | tail -2; echo \"letter_check exit $?\"; time (LLM_BACKEND=fixture $P -m evals.run 2>&1 | tail -4)",
 "description": "Run spec check, letter check, fixture eval at pinned commit",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:05:17.094Z

**tool result**
````
check-spec exit 0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
letter_check exit 0
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/app-d0b04bc/evals/reports/20261102T200517Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured

real	0m7.983s
user	0m5.472s
sys	0m2.187s
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:22.476Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -n 1,22p $S/app-d0b04bc/evals/reports/20261102T200517Z.md; cp $S/app-d0b04bc/evals/reports/20261102T200517Z.md /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/fixture-eval-d0b04bc.md; cd /Users/arsis/zlayt-pm-project && python3 -c 'import json; d=json.load(open(\"evals/reports/latest.json\")); print(\"committed latest.json:\", d.get(\"generated_at\"), d.get(\"backend\"), \"ship_bar_met\", d.get(\"ship_bar_met\"))'",
 "description": "Show fixture eval summary and committed latest.json"
}
````

### User / tool · 2026-11-02T20:05:22.597Z

**tool result**
````
# Eval report 2026-11-02T20:05:17Z

**ship_bar_met: False**  backend `fixture`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `unknown`, tree unknown.

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
committed latest.json: 2026-11-02T14:39:59Z fixture ship_bar_met False
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:29.414Z

**tool call — Bash**
````
{
 "command": "git log --oneline 312efe6..d0b04bc -- app/llm/prompts app/llm/lexicon.yaml app/llm/schemas* 2>&1 | head; echo \"---\"; git rev-list --count 312efe6..d0b04bc; git diff --stat 312efe6 d0b04bc -- app/backend app/llm | tail -1",
 "description": "Check prompt/lexicon changes since live eval"
}
````

### User / tool · 2026-11-02T20:05:29.573Z

**tool result**
````
---
35
 15 files changed, 585 insertions(+), 45 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:38.831Z

**tool call — Bash**
````
{
 "command": "TOK=$(grep TOKEN artifacts/review-evidence/GATE-M3-pm/journey-sample.out | awk '{print $2}'); curl -s http://127.0.0.1:7973/api/cases/$TOK/export | python3 -c 'import json,sys; d=json.load(sys.stdin); t=d[\"letter_text\"]; [print(i, l[:110]) for i,l in enumerate(t.splitlines()) if l.isupper() or l.startswith(\"On \") or \"TREATMENT\" in l or \"Billed\" in l]' | tee artifacts/review-evidence/GATE-M3-pm/sample-narrative-structure.out",
 "description": "Show letter structure with accepted paragraph"
}
````

### User / tool · 2026-11-02T20:05:38.980Z

**tool result**
````
0 TREATMENT CHRONOLOGY
38 TREATMENT SUMMARY
40 On January 9, 2026, Austin EMS run report: Restrained driver rear-ended at approx. 35 mph; complained of neck 
41 On January 9, 2026, Central ER discharge summary: Diagnosed with cervical strain and concussion without loss o
42 On January 16, 2026, Dr. Alvarez, primary care: Persistent neck pain 6/10 and daily headaches; referred to phy
43 On January 23, 2026, Capital PT, initial evaluation: Cervical range of motion reduced approx. 40%; plan of car
44 On February 20, 2026, Capital PT, visit 8: Pain 4/10, improving. (Capital PT, visit 8, February 20, 2026)
45 On March 6, 2026, Capital PT, visit 9: Discharged from PT after two missed appointments; pain 3/10. (Capital P
46 On May 18, 2026, Hill Country Pain Management, new patient: New onset pain radiating to right arm with numbnes
47 On May 29, 2026, Austin Imaging, cervical MRI: C5-C6 disc protrusion with mild right foraminal narrowing; the 
48 On June 12, 2026, Hill Country Pain Management, follow-up: Cervical epidural steroid injection recommended; pa
50 BILLED CHARGES
57 Billed charges accepted from these records: $8,390.00
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:49.009Z

**tool call — Bash**
````
{
 "command": "sed -n 8,14p app/frontend/app.js; grep -n \"server answered\\|Request failed\" app/frontend/api.js | head -3; grep -c \"JUDGE_\\|FIXTURE\\|curated\\|fixture\" artifacts/review-evidence/GATE-M3-pm/journey-sample.out artifacts/review-evidence/GATE-M3-pm/journey-lib11.out",
 "description": "Check for developer jargon in UI and notes"
}
````

### User / tool · 2026-11-02T20:05:49.114Z

**tool result**
````
    const h = s.health;
    $("#banner-synthetic").textContent = (h && h.banner) || SYNTH;           // present on every view, even before /health answers
    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
    // T-166 F7: no test or developer wording on screen. The demo says what it is in the paralegal's words; the longer explanation is the tooltip. A live backend has nothing to announce.
    const badge = $("#badge"); const demo = !!(h && h.demo_mode), mock = ZL.API_MODE === "mock";
    badge.textContent = demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
    badge.title = demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
10:    constructor(status, err) { super((err && err.message) || "Something went wrong. Try again."); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }   // T-166 F7: never a raw "Request failed" or an HTTP status on screen
artifacts/review-evidence/GATE-M3-pm/journey-sample.out:0
artifacts/review-evidence/GATE-M3-pm/journey-lib11.out:10
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:54.292Z

**tool call — Bash**
````
{
 "command": "ls tests/fixtures/llm/ ; ls tests/fixtures/llm/curated | head; ls tests/fixtures/llm/curated | wc -l; cat tests/fixtures/llm/curated/README* 2>/dev/null | head -30",
 "description": "Inspect curated fixture set provenance"
}
````

### User / tool · 2026-11-02T20:05:54.392Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:05:59.211Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/curated_provenance.py",
 "content": "\"\"\"Count curated fixture files by provenance markers (hand-shaped vs recorded). Usage: python3 -I curated_provenance.py <repo root>\"\"\"\nimport collections, json, pathlib, sys\n\nroot = pathlib.Path(sys.argv[1]) / \"tests\" / \"fixtures\" / \"llm\"\nfor sub in (\"curated\", \"recorded\"):\n    d = root / sub\n    files = sorted(d.glob(\"*.json\"))\n    keys = collections.Counter()\n    marks = collections.Counter()\n    for f in files:\n        try:\n            j = json.loads(f.read_text())\n        except Exception:\n            marks[\"unparseable\"] += 1\n            continue\n        keys.update(j.keys() if isinstance(j, dict) else [\"<list>\"])\n        meta = json.dumps({k: j.get(k) for k in (\"label\", \"source\", \"provenance\", \"curated\", \"kind\", \"note\", \"origin\")} if isinstance(j, dict) else {})\n        for m in (\"CURATED\", \"curated\", \"hand\", \"recorded\", \"live\"):\n            if m in meta:\n                marks[m] += 1\n    print(sub, \"files\", len(files))\n    print(\"  top keys\", keys.most_common(12))\n    print(\"  provenance markers\", dict(marks))\nothers = [p.name for p in root.iterdir() if p.is_file()]\nprint(\"other files in fixtures/llm:\", others[:20])\n"
}
````

### User / tool · 2026-11-02T20:05:59.353Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/curated_provenance.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:00.931Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/GATE-M3-pm/curated_provenance.py . ; ls tests/fixtures/llm/ | grep -v json | head",
 "description": "Count curated vs recorded fixture provenance"
}
````

### User / tool · 2026-11-02T20:06:01.063Z

**tool result**
````
curated files 19
  top keys [('CURATED', 19), ('output', 19), ('recorded_from', 19)]
  provenance markers {'curated': 19}
recorded files 0
  top keys []
  provenance markers {}
other files in fixtures/llm: ['bff4fa443b80adfa04ccefc73d4a53af6a051da1e1086772007e3b34b835a517.json', '3829c1a32c6a391a6f22ed0424e791b2113bbae599b6d0384412896c5b0a966d.json', '9b7270f2dfd3c5e9aaf7def593d955e0e70b73de945795408427e897e88d41a9.json', '7e12a6a26c9523e5147b42fcdcbd8aba0f6c5f58e7294a73e5ed516c66eca7c9.json', '6ee72f3acf2c89bb95c2eb46a7048e308adbb10dc2c1399b3ced8aaf9d55f155.json', 'bc66f801341fe95dcff0620870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json', 'a320ede9d535279fb882b00f9a4d07b7bde89ead126e48cfaa3f6154faaa8436.json', '7daa680755944d135152c3ae96f637e9077a6df1c8479faf51c66efd989ed194.json', '273599fd2c6ed0efea9a55146c9a266e3f2d89910b609e4ab99c1048e57fc8d3.json', '14af2eb4f4173a437b33e0c097c6b0e08318795f9f32cde901ec35d0964ae1a9.json', 'a3b3a3e0be44d1a0be62b770f6d3420b7a91a06c2dae11227dbcd25f02891ceb.json', 'bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json', 'cbbbf92fd93aa51246ee3b7e23f2086c791afbd468d717dbce50fc98768e298a.json', '22ec6b147bf4e38a1f1d6e27b7d29c3a760ee67fad1d6cddf3661e7cdeecbb8b.json', '957312c478e021dac549142d19d93307972fc26db2c2e928cb10197fa6375fad.json', '0ff418db1a19494f33fef5be5c27686fbf1880c659c3f06286ebc5b4958a3126.json', 'b1984b86f98824907b4cf248f1a9d7ec7a74ea4e9010e6bac5424ac11c38f575.json', 'b2247882efd0c3ef5d1e4ae049dd62bcb624bfe2f8abe903eb8aec421dd74deb.json', '62ef2c1ef679464eb6e25bb26ce6dd25e6b46f64f6662759391a44bf2aaf29a0.json', '8783db663e5763bd857792e87d730cfbefa8faf4fe013836f556a184d3c693db.json']
curated
narrative
split
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:03.879Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/tests/fixtures/llm && ls curated | grep -v '\\.json$'; find curated -name '*.json' | wc -l; find . -maxdepth 1 -name '*.json' | wc -l; f=$(ls curated/*.json | head -1); python3 -c 'import json,sys; j=json.load(open(sys.argv[1])); print(j[\"CURATED\"], \"| recorded_from:\", str(j[\"recorded_from\"])[:200])' $f",
 "description": "Inspect curated fixture contents"
}
````

### User / tool · 2026-11-02T20:06:04.037Z

**tool result**
````
      19
    1208
CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029). | recorded_from: {'backend': 'curated', 'model': 'hand-checked (qa)', 'recorded_at': '2026-11-02T02:46:58Z'}
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:12.538Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/tests/fixtures/llm && for f in curated/*.json; do python3 -c 'import json,sys; j=json.load(open(sys.argv[1])); o=j[\"output\"]; print(sorted(o.keys())[:4] if isinstance(o,dict) else type(o).__name__, \"|\", j[\"CURATED\"][:70])' $f; done | sort | uniq -c; ls curated/narrative curated/split 2>/dev/null | head; grep -rn \"FIXTURE_SET\\|curated\" /Users/arsis/zlayt-pm-project/app/llm/provider.py | head -8",
 "description": "Classify curated fixture call types"
}
````

### User / tool · 2026-11-02T20:06:13.070Z

**tool result**
````
   9 ['excerpt', 'summary'] | CURATED: hand-checked response written by qa from evals/golden (summar
   9 ['flags'] | CURATED: hand-checked response written by qa from evals/golden (summar
   1 ['sentences'] | CURATED: hand-checked response written by qa from evals/golden (summar
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:15.190Z

**tool call — Bash**
````
{
 "command": "grep -rn \"curated\" app/llm/*.py | head -8; grep -rn \"recorded AI answers\\|curated\" app/frontend/*.js app/frontend/index.html | grep -v \"^.*mock\" | head -8; grep -rn \"recorded AI\\|curated\" docs/RUNBOOK.md README.md 2>/dev/null | head -5",
 "description": "Trace how curated set is loaded and labeled"
}
````

### User / tool · 2026-11-02T20:06:15.303Z

**tool result**
````
app/frontend/app.js:14:    badge.title = demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
docs/RUNBOOK.md:8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
docs/RUNBOOK.md:9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:18.839Z

**tool call — Bash**
````
{
 "command": "grep -rln \"FIXTURE_SET\" app | head; grep -rn \"FIXTURE_SET\" app | head -5; curl -s http://127.0.0.1:7973/api/cases/$(grep TOKEN artifacts/review-evidence/GATE-M3-pm/journey-sample.out | awk '{print $2}')/audit | python3 -c 'import json,sys; d=json.load(sys.stdin); c=d.get(\"calls\") or d.get(\"llm_calls\") or d; import collections; print(type(c).__name__, (list(c.keys())[:8] if isinstance(c,dict) else len(c))); \ncalls = c if isinstance(c,list) else []\nprint(collections.Counter((x.get(\"backend\"), x.get(\"model\"), x.get(\"prompt_version\") or x.get(\"prompt\")) for x in calls).most_common(8))'",
 "description": "Check which fixtures served the sample and audit labels"
}
````

### User / tool · 2026-11-02T20:06:18.958Z

**tool result**
````
app/llm/backends/fixture.py
app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
list 47
[(('fixture', 'claude-haiku-5-5', 'judge_faithfulness_v1'), 18), (('fixture', 'claude-sonnet-5-5', 'extract_v1'), 9), (('fixture', 'claude-sonnet-5-5', 'flags_v1'), 9), (('fixture', 'claude-haiku-5-5', 'judge_flag_v3'), 6), (('fixture', 'claude-haiku-5-5', 'judge_amount_class_v1'), 3), (('fixture', 'claude-haiku-5-5', 'judge_conflict_v6'), 1), (('fixture', 'claude-sonnet-5-5', 'narrative_v1'), 1)]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:24.504Z

**tool call — Bash**
````
{
 "command": "TOK=$(grep TOKEN artifacts/review-evidence/GATE-M3-pm/journey-sample.out | awk '{print $2}'); curl -s http://127.0.0.1:7973/api/cases/$TOK/items/e1/trace | python3 -c 'import json,sys; d=json.load(sys.stdin); \nfor s in d.get(\"steps\",[]): print(\"-\", s.get(\"label\"), \"|\", (s.get(\"why\") or \"\")[:160], \"|\", json.dumps(s.get(\"evidence\"))[:200])' | tee artifacts/review-evidence/GATE-M3-pm/sample-e1-trace.out; curl -s http://127.0.0.1:7973/api/cases/$TOK/audit | python3 -c 'import json,sys; d=json.load(sys.stdin); x=[c for c in d if c.get(\"prompt_version\")==\"extract_v1\"][0]; print(json.dumps({k:x.get(k) for k in (\"backend\",\"model\",\"prompt_version\",\"prompt_hash\",\"latency_ms\",\"cost_usd\",\"recorded_from\",\"fixture\")})[:600])' | tee -a artifacts/review-evidence/GATE-M3-pm/sample-e1-trace.out",
 "description": "Show item trace and audit record for a curated entry"
}
````

### User / tool · 2026-11-02T20:06:24.669Z

**tool result**
````
- AI drafted a summary and picked a quote | The AI read this record and proposed a one-line summary and a quote. | {"model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null}, "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1
- Quote is word for word in the record | The quote was found in the record, character for character. | {"excerpt": {"record_id": "r1", "start": 180, "end": 312, "text": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
- Quote is made of whole sentences | The quote starts and ends on whole sentences. | {}
- Quote keeps the hedge sentence that qualifies it | No hedge sentence that qualifies the quote is left out. | {}
- Numbers and dates in the summary are in the quote | Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote. | {"tokens": []}
- Summary keeps the quote's qualifiers | Every hedge, attribution, negation, side and approximation in the quote is in the summary. | {}
- Quote can be highlighted in the record | The quote's position in the record was found, so it can be highlighted. | {}
- Date of service is confirmed | The date comes from the record's own header and is parsed or confirmed. | {"date": {"record_id": "r1", "date_raw": "2026-01-09", "date_iso": "2026-01-09", "date_status": "parsed", "candidates": []}}
- Record has no instruction-like text | The record has no instruction-like text. | {}
- Second AI check: is the summary supported by the quote? | The second check found every statement in the summary in the quote. | {"model": {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "636239bec8cb1f0bedd4a1dec8e691ef3e4d43c35ee74fae0b
- Your decision | You accepted this item. | {"action": "accept", "at": "2026-11-02T20:00:21Z", "events": [{"action": "accept", "at": "2026-11-02T20:00:21Z", "before": {"edited": null, "review_status": "pending"}, "after": {"edited": null, "revi
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: 'str' object has no attribute 'get'
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:06:42.873Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm && grep -n -i \"override\\|second check\\|partly\\|objection\" journey-lib11.out journey-lib10.out | head",
 "description": "Look for accepted-over-objection notes in exports"
}
````

### User / tool · 2026-11-02T20:06:42.966Z

**tool result**
````
journey-lib10.out:4:TITLE Eob ub04 cms1500 | next_action {'item_id': 'e1', 'kind': 'entry', 'reason': 'A second AI check found the summary only partly supported by the quoted text.'}
journey-lib10.out:25:  a2 charge 492000 | verified [] | UB-04 type of bill 0111, statement period 06/09/2026 to 06/1 | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
journey-lib10.out:26:  a3 charge 210500 | verified [] | UB-04 type of bill 0111, statement period 06/09/2026 to 06/1 | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
journey-lib10.out:27:  a4 charge 38650 | verified [] | UB-04 type of bill 0111, statement period 06/09/2026 to 06/1 | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
journey-lib10.out:28:  a5 charge 71200 | verified [] | UB-04 type of bill 0111, statement period 06/09/2026 to 06/1 | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
journey-lib11.out:4:TITLE Priors and ledger | next_action {'item_id': 'e1', 'kind': 'entry', 'reason': 'A second AI check found the summary only partly supported by the quoted text.'}
journey-lib11.out:34:  a1 charge 326000 | verified [] | Dx: cervical strain, lumbar strain. X-ray cervical and lumba | Quote found word for word, every number in the summary is in the quote, and the second check agreed.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:07:07.675Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/04-sample-top.png"
}
````

### User / tool · 2026-11-02T20:07:07.801Z

**tool result**
````
[image]
````

### User / tool · 2026-11-02T20:07:07.797Z

[Image: original 1440x6602, displayed at 436x2000. Multiply coordinates by 3.30 to map to original image.]

### Assistant · claude-opus-5-5 · 2026-11-02T20:07:11.470Z

<details><summary>thinking</summary>

The screenshot shows the demo badge, the AI-draft tags on the sample entries, the batch-accept button, and the live draft section. I'm stopping the server and writing up the review now.



</details>

### Assistant · claude-opus-5-5 · 2026-11-02T20:07:11.912Z

**tool call — Bash**
````
{
 "command": "kill 50240; sleep 1; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7973/; lsof -iTCP:7973 -sTCP:LISTEN -P | wc -l",
 "description": "Stop the review server by PID and confirm port closed"
}
````

### User / tool · 2026-11-02T20:07:13.114Z

**tool result**
````
000
       0
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:08:24.645Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/GATE-M3-product-manager.md",
 "content": "# GATE-M3: product-manager-reviewer (Dana Okafor persona)\n\n**Commit:** pinned at d0b04bc. `git rev-parse --short HEAD` printed `d0b04bc`.\n\n**Run:** from a `git archive d0b04bc` copy in the scratchpad, on 127.0.0.1:7973, with these settings:\n- `LLM_BACKEND=fixture`\n- `FIXTURE_SET=curated`\n- `ZLAYT_MODE=local`\n- `ZLAYT_DB` pointing to the scratchpad\n\n**Server:** stopped by PID 50240. After that the port returned `000`.\n\n**Evidence:** `artifacts/review-evidence/GATE-M3-pm/`\n\n**Verdict: fail (1 blocker).**\n\n## Answers to the brief\n\n**Does the MVP do the paralegal's job without over-claiming?** On the job itself, yes. I ran the sample case end to end:\n- 9 entries came out, and the 73-day gap was flagged.\n- The 28-day interval was not flagged.\n- The two accident dates are shown as a conflict, and the tool does not pick one.\n- The $185 rate goes to \"Amounts not totaled\".\n- The letter total is `$8,390.00`.\n- The export is blocked until she accepts something.\n- The letter and notes match the golden export exactly (`--check-spec` exit 0).\n\nOn over-claiming, no:\n- The demo sample replays 19 hand-written QA responses. Each file says \"Not a model output.\"\n- The app labels them \"Demo: recorded AI answers\" and tags each entry \"AI draft\".\n- The Why trace says \"The AI read this record and proposed a one-line summary\". It names `claude-sonnet-5-5`.\n- The audit log records `extract_v1` / `claude-sonnet-5-5` for all 9 of those calls.\n- D-029 required the label \"cached demo (curated responses)\". T-166 F7 removed it as jargon, and no decision replaced it.\n\n**Are the cuts and debts honest?** The per-card debts (7c to 7g, 13 to 13f) are specific and honest, and they give a cost to add each one. The cut list as a whole is no longer true:\n- SCOPE_CUTS rows 2, 5, 12, 13, 14, 16, 17 and 19 still read as cut, but they were built under D-031.\n- REQUIREMENTS §4 argues against building PDF upload and the firm-voice paragraph. Both are now in the app, along with all four Appendix A stretch items.\n\n**Are D-059 to D-064 defensible?** Mostly:\n- **D-059, D-060, D-062 and D-064** form one coherent story: charges are default-deny, and a person confirms each line by name. The total line is honest (\"accepted from these records\"). On lib10 the total sums to `$8,123.50`, the expected figure.\n- **D-061** is defensible because it fails toward a false conflict.\n- **D-063** is Chris's call. But it held T-059 (the draft paragraph) with its eval unmet while the feature stays live in the UI. It also left the P0 card T-167 blocked.\n- **D-064 conflicts with the spec.** SCOPE_CUTS row 7g says 'Proposed' and 'Quoted' lines can still be counted. R-CH-3 and R-CH-7 say estimates are never totaled, and REQUIREMENTS was not amended.\n\n**Biggest product risk before M4/M5:** the human step is the only gate on AI summaries that the second check disputed, and it is a one-click Accept that does not say what is wrong.\n- Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click.\n- Each one put a summary into the carrier letter that its own Source quote does not support. For example, lib11 e2 adds \"after passenger vehicle was struck from behind\".\n- About a third of library items need review (106 of 297), so she will be clicking through a lot of warnings.\n- Nothing measures what actually reaches the letter after a realistic accept pattern.\n\n```json\n{\"card\": \"GATE-M3\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"git archive d0b04bc (HEAD d0b04bc); app at 127.0.0.1:7973 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), server PID 50240 stopped; sample case + all 15 library packets; docs: CONTRACT What-we-evaluate and M3, spec/REQUIREMENTS.md incl. §7 ship bar, ORCHESTRATOR_DECISIONS D-042..D-064, SCOPE_CUTS, GATE-M2-summary, MVP-ux-audit-r4\",\n \"exercised\": [\n  \"journey.py on the sample (API, real pipeline, fixture/curated): create, run, read, export 422 before any accept, accept every item one at a time, export 200; letter and notes in journey-sample.out (gap 73 flagged; $185 under Amounts not totaled; total $8,390.00; accident dates not merged)\",\n  \"journey.py on lib11, lib08 and lib10 (journey-lib11.out, journey-lib08.out, journey-lib10.out); Count this charge on lib11 a3 (lib11-counted-letter.out)\",\n  \"lib_sweep.py over the sample + 15 library cases: needs_review counts, and judge-disputed entries accepted with one click (lib_sweep.out: 106/297 needs_review; 5 of 5 disputed accepted with 200)\",\n  \"ui_walk.py (Playwright 1440): lib11 e2 row screenshot (02-lib11-e2-row.png), Accept click (no dialog, review_status accepted), full sample page (04-sample-top.png: badge 'Demo: recorded AI answers', 'AI draft' tags, 'Accept all verified entries', draft paragraph panel)\",\n  \"POST /narrative + /narrative/review accept on the sample; the letter then gains a 'TREATMENT SUMMARY' block (sample-narrative-structure.out)\",\n  \"GET /items/e1/trace and /audit on the sample (sample-e1-trace.out): generator step says 'The AI read this record...' model claude-sonnet-5-5; audit counts 9 extract_v1 + 9 flags_v1 + 1 narrative_v1 calls as claude-sonnet-5-5\",\n  \"curated_provenance.py: tests/fixtures/llm/curated has 19 files, each with CURATED 'hand-checked response written by qa ... Not a model output', recorded_from model 'hand-checked (qa)'\",\n  \"In the d0b04bc copy: evals.run --check-spec exit 0; evals.letter_check value 0 over 25 cases; evals.run fixture (fixture-eval-d0b04bc.md: grounding 1.000, entry_recall 0.982, all flag P/R 1.000, hallucination 40/40, must_not 0; ship_bar False by design on fixture)\",\n  \"evals.library_report regenerated at d0b04bc (library-d0b04bc.md); lib_missed.py lists missed must-flags for lib08/09/10/13/15\",\n  \"git log 312efe6..d0b04bc -- app/llm/prompts app/llm/lexicon.yaml: empty (regression discipline holds); committed evals/reports/latest.json: 2026-11-02T14:39:59Z fixture ship_bar_met False\",\n  \"board.py status/list/show: T-045 in_review; T-059, T-167 (P0), T-170 blocked; paralegal verify_quickly 4 in GATE-M2-r2 and T-149-r2\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"solves_paralegal_job\": 4, \"no_over_claiming\": 2, \"scope_cut_honesty\": 2, \"decisions_defensible\": 4, \"ai_judgment_ship_bar\": 3, \"workflow_fit\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"The demo shows hand-written QA answers as AI output: badge, 'AI draft' tags, Why trace and audit all name the model\",\n   \"evidence\": \"tests/fixtures/llm/curated/*.json (19 files, 9 extract + 9 flags + 1 narrative): CURATED 'hand-checked response written by qa from evals/golden ... Not a model output', recorded_from.model 'hand-checked (qa)'. app/frontend/app.js:13-14 badge 'Demo: recorded AI answers', tooltip 'This demo replays recorded AI answers for its sample cases.' 04-sample-top.png shows the badge and an 'AI draft' tag on every sample entry. sample-e1-trace.out: 'AI drafted a summary and picked a quote | The AI read this record and proposed a one-line summary and a quote. | model claude-sonnet-5-5'. /audit counts ('fixture','claude-sonnet-5-5','extract_v1') x9. D-029 (binding): 'the UI labels it cached demo (curated responses) ... honesty needs the label'; no decision supersedes it (T-166 F7 removed the wording as jargon)\",\n   \"why_it_matters\": \"The public demo and the video are built on this sample. A panel that opens a fixture file will find that the output it saw labeled as the AI's was written by the team to match the golden file. The real model picks different excerpts (D-029 says so). This is the over-claim that ends trust, and the audit trail, which is a product feature, states something false.\",\n   \"fix\": \"Put back an honest label in plain words, e.g. badge 'Demo: sample answers prepared by our team'; tooltip 'The AI's own answers on this case are in the eval report'. Curated items get a 'prepared answer' tag, not 'AI draft'. The trace step for a curated response reads 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'. The audit stores model 'hand-checked (qa)' from recorded_from. Alternatively, point the demo at the recorded live set and change the R-EX-6 byte test to structure only. Record whichever is chosen as a D-entry that amends D-029.\",\n   \"acceptance_test\": \"E2E on FIXTURE_SET=curated: no element contains 'AI draft' or 'recorded AI answers' for a curated item; /items/e1/trace generator step evidence.model.id is not claude-sonnet-5-5 and its why names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'. With the recorded set, labels say AI.\"},\n  {\"severity\": \"major\", \"title\": \"Biggest product risk: a one-click Accept puts a summary the second check disputed into the carrier letter, and nobody is told which words are unsupported\",\n   \"evidence\": \"lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.\",\n   \"why_it_matters\": \"Ship bar 4 measures the model before the human. What reaches the letter depends on a tired paralegal clicking through a third of the items. The failure the persona fears most, the letter saying something its own Source line does not, is one click away and leaves no trace for the attorney.\",\n   \"fix\": \"For entries with JUDGE_PARTIAL or JUDGE_UNSUPPORTED: (1) code marks the summary's content words that are not in the quote; (2) Accept needs either an edit or a named confirm ('I checked the summary against the quote'); (3) the internal notes list 'accepted over a second-check objection: record N' so the attorney sees it; (4) add a reported eval, 'letter summary lines whose own Source quote does not support them, accept-all profile, library + golden', and put its number in the product note.\",\n   \"acceptance_test\": \"lib11 e2 accept without confirm or edit returns 422 with a plain reason; with the confirm it is 200 and internal_notes_text names record 2 under the objection section; the new eval metric appears in the report.\"},\n  {\"severity\": \"major\", \"title\": \"The cut list and the spec no longer describe the product (R-CO-8 fails): 'cut' items are built, all four stretch items ship, and R-CH-7 is contradicted\",\n   \"evidence\": \"memory/SCOPE_CUTS.md:6-23 rows 2 (multi-case), 5 (firm-voice prose), 12 (manual entry), 13 (LLM split), 14 (batch accept, 'single-key accept is fast enough'), 16, 17, 19 still read as cut. :54 lists only D-042 reinstatements, not D-031's. 04-sample-top.png shows 'Accept all verified entries (9)', 'All cases', 'Draft treatment paragraph', 'Exhibit and Bates numbers'. spec/REQUIREMENTS.md:159-168 names one stretch (side-by-side) and argues against PDF upload and the firm-voice paragraph; §5 non-goals 1, 2, 9-14, 16, 19 contradict the build. R-CH-7 (:84) says 'no path turns a rate, estimate or unreadable amount into a totaled charge', but SCOPE_CUTS 7g says 'Proposed'/'Quoted' charge lines are still countable (D-064). Appendix A: 'Stretch (pick at most one ...)'.\",\n   \"why_it_matters\": \"Appendix A grades 'cut scope on purpose and tell us what you cut'. Right now the written reasons argue against features the panel will see working. That reads as either not knowing the product or not cutting at all. An estimate counted into 'Billed charges accepted' is a false statement in the letter that the spec still forbids.\",\n   \"fix\": \"Rewrite SCOPE_CUTS as the current truth: one table with status cut / built (D-031/D-042) / held (D-063), each with its reason. Amend REQUIREMENTS §4/§5 and R-CH-3/R-CH-7 by ADR, or make 'Proposed'/'Quoted'/estimate lines not countable (class a). Get Chris's answer on presenting four stretch items (questions_for_chris) and write that reason into the note draft.\",\n   \"acceptance_test\": \"Script: every REQUIREMENTS §5 non-goal maps to a SCOPE_CUTS row whose status matches the running app (route or testid present = built). R-CH-7 text agrees with count_charge.py; a 'Proposed charge $X' line is NOT_COUNTABLE, or the spec says why it is countable.\"},\n  {\"severity\": \"major\", \"title\": \"The draft paragraph (stretch, T-059 held with its eval unmet) is live and writes a second copy of the chronology into the letter\",\n   \"evidence\": \"board.py show T-059: status blocked, AC3 'eval: 0 unsupported sentences across 3 runs on the sample (live backend)' done:false. grep -c narrative evals/run.py prints 0. After POST /narrative + accept, sample-narrative-structure.out shows the letter gains 'TREATMENT SUMMARY' (lines 38-48): 9 sentences 'On January 9, 2026, Austin EMS run report: <same summary> (<same citation>)', restating the chronology above it.\",\n   \"why_it_matters\": \"This is an LLM output that reaches the carrier letter with no ship-bar number. It is the firm-voice stretch that REQUIREMENTS said 'would need its own verification', and it repeats the chronology without adding anything. It weakens the builder-mindset story and adds risk with no user value shown.\",\n   \"fix\": \"Default it off (config flag) in the M3/M4 build until T-059 AC3 passes and evals.run reports a narrative unsupported count; or remove it and list it as a cut with the reason.\",\n   \"acceptance_test\": \"With default config, GET /narrative returns 404 or the panel is absent (no btn-draft-narrative). With the flag on, the eval report has a narrative metric with a value.\"},\n  {\"severity\": \"major\", \"title\": \"The ship bar's 1.000 flag numbers do not generalize: at d0b04bc the library shows 34/42 must-flags; the committed library and latest.json reports are stale\",\n   \"evidence\": \"library-d0b04bc.md (regenerated at d0b04bc): must flags 1/3 lib08, 1/2 lib09, 0/1 lib10, 1/3 lib13, 1/3 lib15, 34/42 = 0.81 overall. lib_missed.py: missed conflicts 'Denies LOC per patient' vs 'brief loss of consciousness at the second collision', 'Left shoulder pain' vs 'Right shoulder pain', 'denies back pain' vs 'Low back pain 8/10'; lib10 G1 49-day gap reported as 'Gap of 43 days' from a CMS-1500. The committed evals/reports/library-latest.md is from a74b727 (231 commits back) and shows must_not hits that no longer reproduce. The committed evals/reports/latest.json reads ship_bar_met False (fixture, 14:39Z).\",\n   \"why_it_matters\": \"The product note will quote 'flag precision/recall 1.000'. Those numbers come from 10 cases written alongside the rules. Without the library number beside them, the claim goes beyond what the evidence supports, and the canonical pointer a panel opens says False.\",\n   \"fix\": \"qa commits a library report regenerated at the gate commit and the live latest.json. The product note reports golden and library side by side, naming the conflict categories not covered (SCOPE_CUTS 13).\",\n   \"acceptance_test\": \"evals/reports/library-latest.md source commit equals the gate tag; evals/reports/latest.json ship_bar_met True with backend claude-cli; the note draft cites both numbers.\"},\n  {\"severity\": \"minor\", \"title\": \"lib10: the internal notes drop the gap's paperwork caveat, and the flag is 'verified' although its start point is a claim form\",\n   \"evidence\": \"journey-lib10.out notes: '- Gap: 43 days, July 14, 2026 to August 26, 2026: record 8 (Wardlaw Orthopedics, CMS-1500 ...)'. The UI explanation adds 'looks like paperwork ... the gap would be 49 days'; the flag state is 'verified'. D-062 already identifies CMS-1500 as a billing header.\",\n   \"why_it_matters\": \"The attorney reads the notes, not the UI. They show an understated gap with no warning.\",\n   \"fix\": \"The notes line carries the same caveat and the 49-day alternative. An endpoint that looks like paperwork makes the gap needs_review.\",\n   \"acceptance_test\": \"lib10 export notes contain '49 days' and 'paperwork'; f_gap_r8_r9 state is needs_review.\"},\n  {\"severity\": \"minor\", \"title\": \"A counted ledger line prints the statement date where every other line puts the date of service (UX F4, carried, no card)\",\n   \"evidence\": \"lib11-counted-letter.out: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00'. The line was held back because 'The line states no date of service'. board/cards/T-174.md:48 'letter statement dated wording ... not done'.\",\n   \"why_it_matters\": \"The letter implies a service date that the record does not state.\",\n   \"fix\": \"Write 'itemized ledger (statement dated June 15, 2026; no service date stated)'. Open a card.\",\n   \"acceptance_test\": \"lib11 export with a3 counted contains 'statement dated' and not 'June 15, 2026: $180.00'.\"},\n  {\"severity\": \"minor\", \"title\": \"P0 card T-167 is blocked, against D-063 ('Only P0 cards ... proceed')\",\n   \"evidence\": \"board.py list --status blocked: 'T-167 M3 backend blocked P0 AC 1/1 MVP backend wording'; note: 'moved changes_requested -> blocked ... re-check after T-166 lands'\",\n   \"why_it_matters\": \"A P0 with no owner and no re-check is how the D-029 label regression slipped through. The wording work removed an honesty label.\",\n   \"fix\": \"Re-dispatch T-167's check now that T-166 has landed, or close it with a decision.\",\n   \"acceptance_test\": \"T-167 is done or cancelled with a D-entry before the M3 tag.\"},\n  {\"severity\": \"nit\", \"title\": \"D-061 and D-062 read as tuned to the sample: 'one simple rule' plus a second exemption, and a ban 'amended at implementation' because it 'zeroed the sample'\",\n   \"evidence\": \"memory/ORCHESTRATOR_DECISIONS.md:69 and :70\",\n   \"why_it_matters\": \"A panel reading the decision log may see the golden case shaping the rule.\",\n   \"fix\": \"In the Part 2 / prompt-log reading guide, summarize D-059..D-064 as one arc (default-deny, then a named human count) and give the sample-driven amendment as an explicit trade-off.\",\n   \"acceptance_test\": \"The reading guide has one paragraph naming D-059..D-064 and the residuals 7d-7g.\"}\n ],\n \"whats_right\": [\n  \"Sample end to end holds every trap: 73-day gap flagged, 28-day not, accident dates not merged, $185 never totaled, letter equals golden, export blocked until something is accepted.\",\n  \"Default-deny charges plus a named 'Count this charge': lib10 UB-04 totals $8,123.50 as expected, and totals, payments and adjustments are listed in the notes with plain reasons.\",\n  \"Regression discipline holds: no prompt or lexicon change since the live run at 312efe6, and the fixture eval at d0b04bc reproduces every measurable live number.\"\n ],\n \"questions_for_chris\": [\n  \"Appendix A says 'pick at most one' stretch item; the build now ships all four (side-by-side viewer, PDF/OCR, calibrated confidence, draft paragraph). Present all four in the note with your reason, or show only the side-by-side viewer in the submitted demo? Assumption until you answer: side-by-side stays on, the draft paragraph defaults off, and the note names the rest as built-after-the-timebox at your request.\",\n  \"Should the public demo replay the team's hand-checked sample answers (byte-exact letter, labeled as prepared by the team) or the recorded live model answers (labeled AI, wording may differ from the golden)? Assumption: the hand-checked set with an honest label.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T20:08:24.795Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/GATE-M3-product-manager.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:08:26.386Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/GATE-M3-product-manager.md",
 "description": "Validate review file format"
}
````

### User / tool · 2026-11-02T20:08:26.516Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:08:27.369Z

Now I'll record the recurring pattern in memory.

### Assistant · claude-opus-5-5 · 2026-11-02T20:08:36.013Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_gate_review_patterns.md",
 "content": "---\nname: gate-review-patterns\ndescription: Milestone-gate PM review checks that found real issues at GATE-M3 (2026-11-02) — demo provenance labels, one-click accept of judge-disputed items, stale cut lists, ungated stretch features, golden-vs-library gap\nmetadata:\n  type: feedback\n---\n\nRun these checks first on any MVP or gate review. Each one found a real issue at GATE-M3 (d0b04bc).\n\n1. **Demo provenance.** Read `tests/fixtures/llm/curated/*.json`, where the `CURATED` field says \"Not a model output\". Then check that the UI badge, the \"AI draft\" tags, the `/items/<id>/trace` generator step and `/audit` do not present those answers as AI output. D-029 requires an honest label. \"Plain wording\" cards (T-166 F7) removed that label as jargon, so check it again after any wording round.\n2. **The human rung is the only gate.** Accept every JUDGE_PARTIAL or JUDGE_UNSUPPORTED entry and check the result. Script: artifacts/review-evidence/GATE-M3-pm/lib_sweep.py. Compare each letter summary with its own Source quote. Ship bar 4 measures the model before the human, so nothing measures what reaches the letter.\n3. **Cut-list truth.** Compare SCOPE_CUTS rows and REQUIREMENTS §4/§5 with the running UI testids. Chris reinstated cuts twice (D-031, D-042), and both docs lagged.\n4. **Held cards whose feature still ships.** Under D-063, a blocked card such as T-059 (the narrative) can still be live in the UI with its eval AC unmet. Grep `evals/run.py` for the feature name.\n5. **Golden vs library.** Regenerate `python -m evals.library_report --out <evidence>` from the archive copy. At d0b04bc, must-flags were 34/42 on the library against 1.000 on golden. The committed library-latest.md and latest.json were stale.\n\n**Why:** the panel grades over-claiming and \"cut scope on purpose\". These problems were invisible on the sample alone.\n\n**How to apply:** reuse `journey.py`, `lib_sweep.py`, `ui_walk.py` and `lib_missed.py` in that folder. Run each with `python3 -I` against an archive-copy server. Related: [[plan-review-patterns]], [[calibration-vs-redflags]].\n"
}
````

### User / tool · 2026-11-02T20:08:36.123Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_gate_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:08:37.553Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [T-017/T-018 review history]",
 "new_string": "- [Gate review patterns](feedback_gate_review_patterns.md) — GATE-M3: curated-as-AI labels, one-click accept of judge-disputed items, stale cut list, library gap\n- [T-017/T-018 review history]"
}
````

### User / tool · 2026-11-02T20:08:37.653Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:08:40.717Z

GATE-M3 PM verdict is fail with 1 blocker: the sample demo plays answers the team wrote by hand, but the badge, "AI draft" tags, Why trace and audit present them as output from claude-sonnet-5-5, against D-029. Of 4 majors, the biggest risk is that one click on Accept puts a summary the second AI check disputed into the letter (5 of 5 across 16 cases); the others are a stale cut list and spec, the draft paragraph live with no eval, and library flag recall of 0.81 against 1.000 on golden (server stopped; review in `/Users/arsis/zlayt-pm-project/reviews/GATE-M3-product-manager.md`, evidence in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/`).
