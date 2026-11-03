# Subagent: PM re-review: T-185/T-186 r2 (PM re-review: T-185/T-186 r2)

Source: `agent-ae8336b28468ce8e3.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:28:04.402Z

Re-review T-185 (submission/product-note.md) and T-186 (submission/part2-process.md plus submission/validation-ladder.svg), round 2, in /Users/arsis/zlayt-pm-project. You are the PM reviewer, starting from a fresh context.

Read your round-1 reviews (reviews/T-185-product-manager.md, reviews/T-186-product-manager.md) and both cards (`python3 tools/board.py show`). The fix commit is ddfbf6d. Verify every claim against git with `git show HEAD:<path>`, not the working tree, since others are mid-edit.

1. Check each round-1 blocker and major.
2. Two [CHRIS] placeholders are tracked as needs_chris cards T-191 and T-192, for a stretch-item reason and the area-6 engineering stance. Judge whether that is acceptable rather than a defect.
3. Library recall must match the committed evals/reports/library-latest.md. Any number not in a committed report is a defect.
4. Wording refreshes after T-181 and T-179 land are expected later and are not a defect, but anything shown as built must already be in git.

Write reviews/T-185-product-manager-r2.md and reviews/T-186-product-manager-r2.md in D.2 format, applying the verdict rule. Reply in 3 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:06.736Z

**tool call — Bash**
````
{
 "command": "cat personas/product-manager.md | head -50 && ls .claude/agent-memory/product-manager-reviewer/ && cat .claude/agent-memory/product-manager-reviewer/feedback_submission_doc_patterns.md .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md",
 "description": "Read dossier and relevant memory files"
}
````

### User / tool · 2026-11-02T21:28:06.855Z

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
feedback_gate_review_patterns.md
feedback_needs_chris_drift.md
feedback_plan_review_patterns.md
feedback_spec_review_patterns.md
feedback_submission_doc_patterns.md
project_t013_review_history.md
project_t017_t018_review_history.md
reference_reviewer_sandbox.md
reference_source_fetching.md
---
name: submission-doc-patterns
description: M5 product-note / Part 2 review checks that found real defects (T-185/T-186, 2026-11-02) - built-claims ahead of HEAD, proxy-vs-human reviewability, disowned counts, untracked cited paths
metadata:
  type: feedback
---

Run these checks on any submission doc (product note, Part 2, SVG, checklist). Each one found a real defect at T-185/T-186 r1 (commit 59e33ca). Both cards failed.

1. **Built-claims vs HEAD.** For every present-tense "I built" sentence, check the card's status with `board.py show` and check HEAD with `git grep ... HEAD -- app/`. Writers describe in-progress cards as shipped. Examples: the guided UI (T-181) and the D-066 confirm (T-179) were only in the uncommitted working tree.
2. **Proxy vs human.** A persona score (verify_quickly 4/5) passed the M3 screen, but Chris rejected that screen as "VERY hard to use" (D-068). The docs reported the persona score as met and left out the human verdict. Grep ORCHESTRATOR_DECISIONS for "Chris" reactions and check that each one is told.
3. **Counts vs cited file.** Sensor files can disown older counts. m3-sensors.md said 5698 "did not reproduce", yet both docs cited 5,698.
4. **Cited paths exist in git.** Most of reviews/ is untracked. The tracked copies are in submission/prompt-log/reviews/. Run `git ls-files --error-unmatch` on every backticked path.
5. **Library vs golden on all metrics, not just flags.** At d0b04bc the library scored entries 0.775, amounts 0.580 and flags 0.81. Script: artifacts/review-evidence/T-185-pm/lib_sums.py.
6. **Stretch count.** Count stretch items against the live UI. Calibrated confidence (GET /api/calibration, suggestions.js) is the Appendix A "confidence indicator", so the build ships 3 stretch items, not 2.

**Why:** the hiring panel grades over-claiming and AI judgment. All six of these get past a reading of the doc alone.

**How to apply:** render the docs with pandoc + headless Chrome using submission/print.css to get the page count. The demo app at :7860 serves the sample only; library cases need local mode. Related: [[gate-review-patterns]], [[needs-chris-drift]].
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
---
name: reviewer-sandbox
description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
metadata:
  type: reference
---

The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]].
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:08.503Z

**tool call — Bash**
````
{
 "command": "sed -n 50,200p personas/product-manager.md | head -80; echo ----; cat reviews/T-185-product-manager.md; echo -----; cat reviews/T-186-product-manager.md",
 "description": "Read rest of dossier and round-1 reviews"
}
````

### User / tool · 2026-11-02T21:28:08.621Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:09.589Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-185; python3 tools/board.py show T-186; python3 tools/board.py show T-191; python3 tools/board.py show T-192; git log --oneline -8; git show --stat ddfbf6d",
 "description": "Show cards and fix commit"
}
````

### User / tool · 2026-11-02T21:28:09.990Z

**tool result**
````
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
updated_at: "2026-11-02T21:27:58Z"
claimed_by: "writer"
claimed_at: "2026-11-02T21:19:19Z"
rounds: 1
commits: ["59e33cacd152f21c18727aab4738c5dc096ac486", "ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7"]
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-185-product-manager.md", "at": "2026-11-02T21:19:09Z"}
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
- 2026-11-02T21:19:09Z orchestrator: review product-manager-reviewer (claude-opus-5-5): fail — reviews/T-185-product-manager.md; round 1; findings:
    - [blocker] The UI redesign after Chris's feedback is hidden, and ship-bar row 5 still reports reviewability as met — fix: Add a 'What testing found' bullet in Chris's voice, for example: 'Reviewability passed on paper and failed in use. A persona reviewer scored the M3 screen 4/5 on "I could verify every claim quickly". When I used it myself it was very hard to use (D-068), so we rebuilt it a
    - [blocker] The note describes the guided four-step screen and the D-066 disputed-accept confirm as built; neither is at HEAD — fix: Describe what HEAD ships today. Or hold the note until T-181 and T-179 are done and committed, then re-verify each sentence against the running app. Until then, mark both sentences [PENDING T-181] and [PENDING T-179] so nothing reads as shipped. Use present tense
    - [major] The unit-test count 5,698 is the figure the cited file says did not reproduce — fix: Use the count and commit the file states ('5,782 unit at b824a6c'), or re-run at the submission commit and cite that.
    - [major] Stretch: three items shipped against 'pick at most one', the note names two, and gives no reason for going beyond the brief or for reinstating cuts — fix: Name all three (source viewer, PDF text layer, calibrated confidence). Add one sentence on why the brief's limit was exceeded and why cuts were reinstated, in Chris's words (see questions_for_chris), plus what that cost.
    - [major] Cited evidence paths are not in the repo the panel will open — fix: Either cite submission/prompt-log/reviews/... or have the orchestrator commit reviews/ before submission. Then click every path from a fresh clone.
    - [major] Generalization is reported only for flags; the same library run shows entry recall 0.775 and amount recall 0.580 — fix: qa regenerates library-latest.md at the submission commit. The note's row 2 then gives golden and library side by side, with one clause on what the misses are (real misses or expected files that predate the billing redesign).
    - [minor] The $10,906 vs $6,000 billing example is attributed to the wrong reviews — fix: Attribute the $10,906 case to the paralegal reviewer at GATE-M2 (cite its path), or drop it.
    - [minor] LLM/code paragraph says code does record splitting; the build has an LLM split fallback — fix: Add to 'The model reads': 'where to cut an unsplittable paste (offsets only; code validates and flags it LLM_SPLIT)'.
    - [minor] Post-launch metrics name no data source — fix: One clause each: #1 timestamps from case-created to letter-copied events vs a stopwatch baseline taken in week 2; #2 attorney edit log plus adjuster letters tagged by the paralegal; #3 audit log accept events with before/after and time on item.
- 2026-11-02T21:19:09Z orchestrator: Round 2: (a) state Chris's 'VERY hard to use' verdict and the D-068 redesign plainly as the turning point; reviewability score reported as pre-redesign; (b) describe T-181/T-179 only as what is committed, marking unfinished items 'in progress' — final wording refresh after T-181 lands; (c) use test counts from a fresh run cited by file; give reasons for the stretch items; cite only reviews in git; report library recall (entries 0.775, amounts 0.580) next to golden.
- 2026-11-02T21:19:19Z writer: claimed
- 2026-11-02T21:27:31Z writer: Round 2: redesign story added as first testing finding (persona 4/5 predates D-068; row 5 now 'not met on the screen I rejected'); guided screen T-181 and D-066 confirm T-179 marked in progress; unit 5,795 at 33e88c6 from fresh git-archive run (artifacts/unit-count-33e88c6.txt); library entries 0.775 / amounts 0.681 / flags 0.81 from committed evals/reports/library-latest.md (a74b727), 0.580 amounts noted as later run; three stretch items named with cost; metrics have sources; LLM split fallback added; all cited paths exist in git. Renders to 1 page.
- 2026-11-02T21:27:32Z writer: moved in_progress -> in_review
- 2026-11-02T21:27:58Z orchestrator: Library recall: cite the file in git (library-latest.md a74b727: entries 0.775, amounts 0.681, flags 0.81); drop the 0.580 mention unless a committed report shows it. Correct as written.
- 2026-11-02T21:27:58Z orchestrator: review dispatched: product-manager-reviewer

## Handoff
What changed: submission/product-note.md round 2, one page. Redesign finding first (persona 4/5 predates D-068, row 5 not met), T-181/T-179 marked in progress, three stretch items named with cost, library recall beside golden, metrics with data sources, LLM split fallback, $10,906 dropped. How verified: pandoc+Chrome page count 1; every backticked path git-tracked; unit 5,795 at 33e88c6 in artifacts/unit-count-33e88c6.txt. Left: [CHRIS: name, link, stretch reason] (NEEDS_CHRIS 5, 8); refresh when T-181/T-179 land and after qa regenerates library-latest.md. Surprised me: committed library report gives amounts 0.681, not the 0.580 of the d0b04bc run; I show both. One page has about 1 line of slack.

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
updated_at: "2026-11-02T21:27:58Z"
claimed_by: "writer"
claimed_at: "2026-11-02T21:19:19Z"
rounds: 1
commits: ["59e33cacd152f21c18727aab4738c5dc096ac486", "ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7"]
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-186-product-manager.md", "at": "2026-11-02T21:19:09Z"}
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
- 2026-11-02T21:19:09Z orchestrator: review product-manager-reviewer (claude-opus-5-5): fail — reviews/T-186-product-manager.md; round 1; findings:
    - [blocker] The UI redesign after Chris's feedback is missing; the quality-bar table and the SVG present reviewability as met — fix: Area 4: add a line under the table: 'Reviewability passed on a persona score and failed in use. I found the M3 screen very hard to use and we rebuilt it (D-068). The ship call now needs a real paralegal session, not a persona score.' Change the table and SVG Resu
    - [blocker] The SVG presents the D-066 compare-confirm as current product behavior; it is not at HEAD — fix: Re-verify once T-179 is done and committed. Until then, word rung 3 as 'Decided (D-066), in progress: a disputed summary will need a named confirm'.
    - [major] The unit-test count 5,698 is the figure the cited file says did not reproduce — fix: Cite '5,782 at b824a6c', or re-run at the submission commit and cite that.
    - [major] Area 6 never states engineering's role in product decisions — fix: Add an engineering column or two lines. For example: engineering decides how (stack, model routing inside the budget, test design) and has a veto on 'not safe to ship'; I decide what and when; the LLM/code line is drawn together and written down in an ADR.
    - [major] Cited evidence paths and artifact counts do not match what is in the repo — fix: Point at the paths that exist in the submitted repo (submission/prompt-log/reviews/), or have the orchestrator commit reviews/ and evals/reports/ first, then recount at the submission commit.
    - [minor] The SVG says record splitting is code only; the build has an LLM split fallback — fix: Change to 'Split records (a model may only point at cut offsets for an unsplittable paste; code validates)'.
    - [minor] A claim about how PI firms work is stated as fact; the assumption range is off by one — fix: 'Every matter with treatment needs one (assumption: confirm the share of matters that reach a demand letter)'; 'A-101 to A-109'.
- 2026-11-02T21:19:09Z orchestrator: Round 2: same redesign story; the svg shows only committed behavior (mark the disputed-summary confirm 'in progress' until T-179 lands); fix the test count, add the engineering role to area 6, and make paths and counts match git.
- 2026-11-02T21:19:19Z writer: claimed
- 2026-11-02T21:27:31Z writer: Round 2: redesign story in area 4 and area 7; table and SVG reworded (persona 4/5 on old screen, rejected in use; D-066 'in progress'); SVG split fallback fixed; area 6 gets an Engineering paragraph (decides how, not-safe-to-ship veto, evidence-first tiebreak; stance flagged NEEDS_CHRIS #9); unit 5,795 at 33e88c6; paths now submission/prompt-log/reviews/; counts 460 reviews, 27 dated reports, 68 decisions, 62 debt rows, A-101..A-109. 4 pages.
- 2026-11-02T21:27:32Z writer: moved in_progress -> in_review
- 2026-11-02T21:27:58Z orchestrator: review dispatched: product-manager-reviewer

## Handoff
What changed: part2-process.md and validation-ladder.svg round 2. Redesign story (areas 4, 7), reviewability row and SVG reworded, D-066 rung 3 'in progress', SVG split fallback, Engineering paragraph in area 6, A-109, assumption marker on matter volume, paths and counts matched to git. How verified: 4 pages by pandoc+Chrome; SVG rendered and read; backtick-path check; unit 5,795 at 33e88c6. Left: miss story (T-189), optional markers (T-190), engineering stance confirm (NEEDS_CHRIS 9). Refresh counts and T-179/T-181 wording at final.

---
id: "T-191"
title: "Chris: stretch-item reasons in the product note (NEEDS_CHRIS #8)"
milestone: "M5"
role: "writer"
status: "needs_chris"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:27:58Z"
updated_at: "2026-11-02T21:27:58Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Chris supplies or approves the one-line reason per stretch item; placeholder replaced", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)

## Handoff (filled when moving to in_review)

---
id: "T-192"
title: "Chris: area 6 engineering stance in Part 2 (NEEDS_CHRIS #9)"
milestone: "M5"
role: "writer"
status: "needs_chris"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:27:58Z"
updated_at: "2026-11-02T21:27:58Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Chris supplies or approves the engineering-role stance; placeholder replaced", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)

## Handoff (filled when moving to in_review)

ddfbf6d docs(submission): T-185/T-186 round 2: redesign story (persona 4/5 predates D-068), only-committed claims, fresh unit count, library recall beside golden, engineering role, stretch reasons
f3d42a2 feat(frontend): T-181 guided UI scaffold (D-068): / is the guided app, old screen at /classic
275e4ca feat(backend): public demo caps stored cases and runs in flight, plain 429 (T-183 r2)
ed0508e fix(qa): prompt-log redacts private-network details everywhere, README lists every edit with counts (T-187 r2)
33e88c6 tools: prompt-log export also redacts tailnet hostnames, 100.64/10 addresses and a work email; docstring lists every edit (T-187 privacy review)
59e33ca docs(submission): one-page product note, Part 2 process doc, validation-ladder SVG
f22f8fc tools: prompt-log export writes <redacted> (scanner-safe) and no stale 'capped' header (T-187)
3b5fe43 feat(qa): M5 prompt log package (T-187)
commit ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:27:41 2026 -0600

    docs(submission): T-185/T-186 round 2: redesign story (persona 4/5 predates D-068), only-committed claims, fresh unit count, library recall beside golden, engineering role, stretch reasons
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 .claude/agent-memory/writer/submission_pipeline.md | 18 +++++
 artifacts/unit-count-33e88c6.txt                   | 88 ++++++++++++++++++++++
 submission/NEEDS_CHRIS.md                          |  4 +-
 submission/part2-process.md                        | 22 +++---
 submission/product-note.md                         | 47 ++++++------
 submission/validation-ladder.svg                   | 47 ++++++------
 6 files changed, 170 insertions(+), 56 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:12.882Z

**tool call — Bash**
````
{
 "command": "sed -n 1,400p /Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/bpeb9fsga.txt | grep -n \"^-----\\|^----$\" ; wc -l reviews/T-185-product-manager.md reviews/T-186-product-manager.md",
 "description": "Locate review boundaries"
}
````

### User / tool · 2026-11-02T21:28:13.011Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:14.052Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-185-product-manager.md"
}
````

### User / tool · 2026-11-02T21:28:14.066Z

**tool result**
````
1	# T-185 product note: product-manager-reviewer (Dana Okafor lens)
2	
3	**Verdict: fail** (2 blockers, 4 majors, 3 minors, 1 nit).
4	
5	The note mostly does what a hiring panel wants. It has a five-row ship bar with live numbers and a report path. It puts the golden-vs-library flag gap in bold. It tells the billing rounds and the M3 gate failure plainly. It invents nothing about Chris. Most numbers I checked trace to their source: 242 grounding checks, 0.982/1.000 recall, 40/40, 0 of 10, 20/20, 12/12, 5 of 17 clean held-out, 412 E2E, 34/42 = 0.81, $16,147 vs $8,123.50, and D-040/D-052/D-065..D-068.
6	
7	Two things fail it.
8	
9	1. **It hides the biggest reviewability miss.** Chris used the M3 screen and called it "VERY hard to use", which forced a full redesign (D-068). The note still reports ship-bar row 5 as met at 4/5, a score from a persona reviewer on that same screen.
10	2. **It describes things that are not built as built.** The guided four-step screen is T-181, still in_progress with AC 0/1. Its files are untracked, and the running app serves the old UI. The D-066 compare-confirm exists only in the uncommitted working tree.
11	
12	The majors:
13	- The unit-test count (5,698) is one the cited file says did not reproduce.
14	- Three stretch items shipped against "pick at most one", and the note gives no reason.
15	- The cited review paths are not in git.
16	- Library entry and amount recall (0.775 and 0.580 on the same library run) go unmentioned while the note implies only flags fail to generalize.
17	
18	Page count: 1 page (pandoc + headless Chrome with submission/print.css, 8.7pt). Length is within the limit.
19	
20	```json
21	{"card": "T-185", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
22	 "scope": "submission/product-note.md at commit 59e33ca (working tree identical for this file); cited evidence: evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, evals/reports/latest.json, reviews/GATE-M3-*.md, reviews/T-140-claims-adjuster*.md, memory/SCOPE_CUTS.md, memory/ORCHESTRATOR_DECISIONS.md, docs/LLM_VS_CODE.md; app at http://localhost:7860 (demo mode, fixture backend); sample case",
23	 "exercised": [
24	  "Read personas/product-manager.md, docs/CONTRACT.md M5 (318-328), 8.2 ship bar, 11 DoD, Appendix A (493-596), Appendix B (598-607)",
25	  "Read submission/product-note.md twice; rendered it with pandoc + headless Chrome using submission/print.css: 1 page (artifacts/review-evidence/T-185-pm/note.pdf)",
26	  "Spot-checked 20+ numbers/claims against evals/reports/20261102T164038Z.md (grounding 1.000/242, entry 0.982, amount 1.000, flags 1.000 x4, 40/40, controls 0 of 10, J3 20/20, J4 12/12, 0 false agree, clean held-out 5 of 17, case_06 E3 miss, gap_28/73 assertions)",
27	  ".venv/bin/python -m evals.run --check-fresh -> exit=0; git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml -> empty (live run still valid for prompts)",
28	  "Compared the unit/E2E counts with evals/reports/m3-sensors.md:7-8 (5782 unit, 412 E2E)",
29	  "grep of D-001, D-007, D-022, D-031, D-034, D-040, D-042, D-047, D-052..D-054, D-059, D-062..D-068 in memory/ORCHESTRATOR_DECISIONS.md",
30	  "grep -rn '10,906' reviews/ memory/ -> only GATE-M2-paralegal.md, GATE-M2-r2-paralegal.md, GATE-M2-round1-triage.md; not in T-140-claims-adjuster*",
31	  "python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> entries 93/120 = 0.775, amounts 40/69 = 0.580, must flags 34/42 = 0.810",
32	  "python3 tools/board.py show T-181/T-179/T-177 and board.py list --status in_progress: T-181 (guided UI) in_progress AC 0/1; T-179 (D-066) in_progress",
33	  "git ls-files --error-unmatch app/frontend/guided/core.js -> not known to git; git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; working tree app/backend/review.py:298-349 has D-066 (uncommitted)",
34	  "curl http://localhost:7860/ -> old UI (index.html with stepper.css/sidebyside.css); /api/health -> demo_mode true, backend fixture",
35	  "python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample -> artifacts/review-evidence/T-185-pm/journey-sample-7860.out: 4 flag types present, gap 73 flagged, $185 under AMOUNTS NOT TOTALED, total $8,390.00, export 422 before any accept, 200 after",
36	  "curl /api/calibration -> calibrated confidence served; app/frontend/suggestions.js:119-120 renders it (confidence-indicator stretch item)",
37	  "git ls-files --error-unmatch on every cited path: reviews/GATE-M3-product-manager.md, reviews/GATE-M3-paralegal.md, reviews/T-140-claims-adjuster*.md untracked; tracked copies under submission/prompt-log/reviews/",
38	  "Spot-checked docs/LLM_VS_CODE.md rows 1 (split) and 7 (amount class) against the note's LLM/code paragraph"
39	 ],
40	 "verdict": "fail",
41	 "scores": {"accuracy": 2, "no_invented_chris_facts": 5, "required_contents": 4, "honesty_of_misses": 2, "voice": 4, "length": 5},
42	 "findings": [
43	  {"severity": "blocker", "title": "The UI redesign after Chris's feedback is hidden, and ship-bar row 5 still reports reviewability as met",
44	   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:76 D-068: 'Guided UI redesign (Chris, 2026-11-02: \"VERY hard to use… so simple someone's grandma can use it\")' with the reason 'The user's verdict on the current UI'. product-note.md:19 row 5 Result: '4/5 (reviews/GATE-M3-paralegal.md)'. product-note.md:23 says only 'Score 5 is a persona reviewer on the previous screen, not a real paralegal; not re-scored on the guided screen.' grep -n -iE 'hard to use|redesign|grandma|rebuilt' submission/product-note.md -> no match; D-068 appears only at :7 as the label of the new screen.",
45	   "why_it_matters": "This is the clearest AI-judgment lesson in the build. An AI persona passed the screen at 4/5, and the one human who used it said it was very hard to use. The note reports the proxy as a pass and never says the human verdict contradicted it. The panel grades 'define good enough and test against it'. Reporting a met bar on a screen the user rejected is hiding a known failure, a red flag in the dossier.",
46	   "fix": "Add a 'What testing found' bullet in Chris's voice, for example: 'Reviewability passed on paper and failed in use. A persona reviewer scored the M3 screen 4/5 on \"I could verify every claim quickly\". When I used it myself it was very hard to use (D-068), so we rebuilt it as a four-step guide. An AI reviewer is not a substitute for a person at the desk.' Change row 5 Result to 'Not met on the shipped screen: persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored', or give a re-score on the guided screen.",
47	   "acceptance_test": "grep -n -iE 'hard to use|rebuilt|redesign' submission/product-note.md returns a line in 'What testing found'; row 5's Result no longer reads as met without that qualification."},
48	  {"severity": "blocker", "title": "The note describes the guided four-step screen and the D-066 disputed-accept confirm as built; neither is at HEAD",
49	   "evidence": "product-note.md:7 'What I built. ... A guided four-step screen: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter (D-068). Review is one item at a time: ... two big answers.' board.py list --status in_progress: 'T-181 ... in_progress P0 AC 0/1 Build the guided UI (D-068)'. git ls-files --error-unmatch app/frontend/guided/core.js -> 'did not match any file(s) known to git'. curl http://localhost:7860/ serves the old index.html (stepper.css, sidebyside.css). product-note.md:32 'a disputed one needs a named confirm (D-066)'. git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty (D-066 code exists only uncommitted in app/backend/review.py:298-349; T-179 in_progress). The writer's own handoff says 'guided UI (T-181) is described as built'.",
50	   "why_it_matters": "The panel will open the prototype link and see a different product from the one the note describes. A PM note that claims an unbuilt UI and an unbuilt safety control misstates what was built. That is an invented fact under D.2, and it undercuts every other number in the note.",
51	   "fix": "Describe what HEAD ships today. Or hold the note until T-181 and T-179 are done and committed, then re-verify each sentence against the running app. Until then, mark both sentences [PENDING T-181] and [PENDING T-179] so nothing reads as shipped. Use present tense only for code at the commit the submission is tagged at.",
52	   "acceptance_test": "At the submission commit: board.py show T-181 and T-179 show done; git ls-files app/frontend/guided lists the files; GET / serves the guided shell; accepting a judge-disputed item without compared:true returns 422 COMPARE_REQUIRED. Otherwise neither sentence appears in present tense."},
53	  {"severity": "major", "title": "The unit-test count 5,698 is the figure the cited file says did not reproduce",
54	   "evidence": "product-note.md:19 '412 E2E, 5,698 unit tests pass (evals/reports/m3-sensors.md)'. evals/reports/m3-sensors.md:7: '5782 passed, 2 skipped ... The round-2 figure 5698 was taken before later commits added tests and did not reproduce ... a count is valid only for the commit named'.",
55	   "why_it_matters": "A number that contradicts its own citation is the first thing a careful panelist checks. It costs trust in every other number in the table.",
56	   "fix": "Use the count and commit the file states ('5,782 unit at b824a6c'), or re-run at the submission commit and cite that.",
57	   "acceptance_test": "Every test count in product-note.md equals a count in the cited sensors file for the commit named next to it."},
58	  {"severity": "major", "title": "Stretch: three items shipped against 'pick at most one', the note names two, and gives no reason for going beyond the brief or for reinstating cuts",
59	   "evidence": "Appendix A: 'Stretch (pick at most one, only if time remains): PDF upload, a confidence indicator, a side-by-side source viewer, or a draft paragraph'. product-note.md:9 'The brief allows one stretch; I picked the source viewer and also shipped PDF text-layer upload.' Calibrated confidence also ships (D-042 'calibrated confidence (shown as measured precision per state)'; GET /api/calibration returns it; app/frontend/suggestions.js:119-120 renders 'In testing on N synthetic cases, X of Y verified items matched the record'). :9 'Not cut: I reinstated cuts twice (D-031, D-042)' gives no why.",
60	   "why_it_matters": "'Cut scope on purpose' is the first row of 'What we evaluate'. Going past an explicit limit is defensible only with a stated reason. Undercounting what shipped and giving no reason reads as drift, not as a decision.",
61	   "fix": "Name all three (source viewer, PDF text layer, calibrated confidence). Add one sentence on why the brief's limit was exceeded and why cuts were reinstated, in Chris's words (see questions_for_chris), plus what that cost.",
62	   "acceptance_test": "The Cut paragraph lists every shipped Appendix A stretch item and gives one reason sentence for exceeding 'at most one' and for D-031/D-042."},
63	  {"severity": "major", "title": "Cited evidence paths are not in the repo the panel will open",
64	   "evidence": "git ls-files --error-unmatch reviews/GATE-M3-product-manager.md reviews/GATE-M3-paralegal.md reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md reviews/T-140-claims-adjuster-r3.md reviews/T-140-claims-adjuster-r4.md -> \"error: pathspec ... did not match any file(s) known to git\" for each. The tracked copies are submission/prompt-log/reviews/GATE-M3-product-manager.md etc. product-note.md:19, :23, :24 cite the reviews/ paths.",
65	   "why_it_matters": "Appendix A: 'Make sure we can open every link'. The 0.81 library recall, the 4/5 score and the billing-round claims are the note's honesty evidence. As cited, none of them opens in the repo.",
66	   "fix": "Either cite submission/prompt-log/reviews/... or have the orchestrator commit reviews/ before submission. Then click every path from a fresh clone.",
67	   "acceptance_test": "From a fresh clone of the submission commit, every path in product-note.md exists (scripted: extract backticked paths, test -e each)."},
68	  {"severity": "major", "title": "Generalization is reported only for flags; the same library run shows entry recall 0.775 and amount recall 0.580",
69	   "evidence": "product-note.md:16 row 2 'entries 0.982, amounts 1.000 [E]' (golden only); :23 'The 1.000 flag numbers do not generalize'. python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> 'entries: 93/120 = 0.775', 'amounts: 40/69 = 0.580', 'must flags: 34/42 = 0.810'. The committed evals/reports/library-latest.md is from a74b727 (stale; the writer's handoff says so).",
70	   "why_it_matters": "Saying the flag numbers do not generalize implies the recall numbers do. The same matchers on the same 15 packets say otherwise. Some of the gap may be expected-file drift after D-052/D-059 (exact class match in evals/run.py:180), but the note neither reports nor explains it.",
71	   "fix": "qa regenerates library-latest.md at the submission commit. The note's row 2 then gives golden and library side by side, with one clause on what the misses are (real misses or expected files that predate the billing redesign).",
72	   "acceptance_test": "evals/reports/library-latest.md source commit equals the submission commit; product-note.md row 2 cites its entry and amount numbers next to the golden ones."},
73	  {"severity": "minor", "title": "The $10,906 vs $6,000 billing example is attributed to the wrong reviews",
74	   "evidence": "product-note.md:24 'A claims-adjuster reviewer outworded every word-list rule: one library letter said $10,906 against a true $6,000 ... (reviews/T-140-claims-adjuster*.md)'. grep -rn '10,906' reviews/T-140-claims-adjuster*.md -> nothing; the source is reviews/GATE-M2-paralegal.md:30 and reviews/GATE-M2-round1-triage.md:9 (paralegal persona). $16,147 vs $8,123.50 does trace to the T-140 adjuster reviews.",
75	   "why_it_matters": "The brief requires each claim to trace to its cited file. This one does not.",
76	   "fix": "Attribute the $10,906 case to the paralegal reviewer at GATE-M2 (cite its path), or drop it.",
77	   "acceptance_test": "Each dollar figure on line 24 is found by grep in the file cited beside it."},
78	  {"severity": "minor", "title": "LLM/code paragraph says code does record splitting; the build has an LLM split fallback",
79	   "evidence": "product-note.md:38 'Code does anything with one right answer: record splitting, ...' and the model list omits splitting. docs/LLM_VS_CODE.md:29 row 1: 'Only when the code split finds a single record that is unsplit ... may a model be asked ... it returns character offsets only'; D-031 'LLM split fallback (flagged LLM_SPLIT)'; app/llm/prompts/split_v1.md is in the live report's hash list.",
80	   "why_it_matters": "The panel grades where the line was drawn. The note's summary should match LLM_VS_CODE.md, and here the honest version is the stronger one: the model only points at offsets, code cuts and validates.",
81	   "fix": "Add to 'The model reads': 'where to cut an unsplittable paste (offsets only; code validates and flags it LLM_SPLIT)'.",
82	   "acceptance_test": "The note's LLM list matches every LLM row in docs/LLM_VS_CODE.md."},
83	  {"severity": "minor", "title": "Post-launch metrics name no data source",
84	   "evidence": "product-note.md:42-44: #1 'against her own last three by hand' (no timed baseline method); #2 'letter lines an attorney corrects or an adjuster challenges, per 100' (no capture mechanism); #3 no source named (it is the audit log).",
85	   "why_it_matters": "A metric that cannot be computed cannot inform a decision. Each metric's decision is stated well; its source is not.",
86	   "fix": "One clause each: #1 timestamps from case-created to letter-copied events vs a stopwatch baseline taken in week 2; #2 attorney edit log plus adjuster letters tagged by the paralegal; #3 audit log accept events with before/after and time on item.",
87	   "acceptance_test": "Each of the three metrics names its event or log source."},
88	  {"severity": "nit", "title": "Internal decision IDs crowd a panel-facing page; 'Score 5' is unclear",
89	   "evidence": "product-note.md:31-36 failure table cites D-034, D-047, D-022, D-054, D-066, D-053, D-007 in five rows; :23 'Score 5 is a persona reviewer'.",
90	   "why_it_matters": "Appendix B voice: concise and plain. The panel cannot decode D-numbers without opening the log.",
91	   "fix": "Keep one or two IDs where they prove a decision; write 'ship-bar row 5' for 'Score 5'.",
92	   "acceptance_test": "At most three D-IDs in the failure table; no 'Score 5'."}
93	 ],
94	 "whats_right": [
95	  "The ship bar has five numeric criteria with live results and a report path, and the golden-vs-library flag gap is in bold rather than hidden.",
96	  "The billing rounds and the M3 gate failure (prepared answers labeled as AI, one-click accept of disputed items) are told plainly, with numbers.",
97	  "No invented facts about Chris: the byline and link are [CHRIS: ...] placeholders and tracked in NEEDS_CHRIS #5."
98	 ],
99	 "questions_for_chris": [
100	  "May the note quote your D-068 reaction ('VERY hard to use') in your own voice as the reviewability miss, or do you want it paraphrased?",
101	  "In one line, why did you reinstate cuts (D-031, D-042) and ship three stretch items when the brief says 'at most one'? The note needs your reason, not ours."
102	 ]}
103	```
104	
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:14.446Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-186-product-manager.md"
}
````

### User / tool · 2026-11-02T21:28:14.453Z

**tool result**
````
1	# T-186 Part 2 process doc: product-manager-reviewer (Dana Okafor lens)
2	
3	**Verdict: fail** (2 blockers, 3 majors, 2 minors).
4	
5	All eight areas are present, and most are specific to this build:
6	
7	- **Area 1:** three plus three discovery questions, specific enough to ask tomorrow.
8	- **Area 2:** reasons for doing this first, plus four concrete pieces of evidence that would change the decision.
9	- **Area 3:** three AI acceptance criteria, one of them a "must never", each with its checker.
10	- **Area 4:** a test set built from real work product, a held-out half, and regression discipline that works (`--check-fresh` exit 0).
11	- **Area 5:** four measures with expand and kill thresholds, labeled as proposals.
12	- **Area 7:** a real message and agenda.
13	- **Area 8:** supervision examples taken from LESSONS.
14	
15	The miss story is a correctly marked [CHRIS: ...] block, tracked in NEEDS_CHRIS #4 (T-189). The doc renders to 4 pages.
16	
17	Two things fail it:
18	
19	1. **It hides the UI redesign.** Chris rejected the M3 screen as "VERY hard to use" (D-068). The quality-bar table and the SVG still present reviewability as 4/5 met, and the area 7 answer on honest feedback skips the build's best example of it.
20	2. **The SVG claims an unbuilt control.** It presents the D-066 disputed-accept confirm as current behavior, but it is not at HEAD.
21	
22	The majors:
23	
24	- The unit-test count (5,698) is one the cited file says did not reproduce.
25	- Area 6 never says what engineering's role in product decisions is.
26	- The cited paths and counts (`reviews/GATE-M3-product-manager.md`, "460 review files", "74 dated reports") do not match what is in git.
27	
28	```json
29	{"card": "T-186", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
30	 "scope": "submission/part2-process.md and submission/validation-ladder.svg at commit 59e33ca; cited evidence: evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, reviews/GATE-M3-*.md, memory/{ORCHESTRATOR_DECISIONS,LESSONS,SCOPE_CUTS,ASSUMPTIONS}.md, spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md; app at http://localhost:7860 (demo mode); sample case",
31	 "exercised": [
32	  "Read personas/product-manager.md; docs/CONTRACT.md M5 (318-328), Appendix A Part 2 eight areas + One story + Format (565-586), Appendix B (598-607)",
33	  "Read submission/part2-process.md twice and marked each of the eight areas specific/generic/missing; read submission/validation-ladder.svg source",
34	  "Rendered with pandoc + headless Chrome (submission/print.css): artifacts/review-evidence/T-185-pm/part2.pdf = 4 pages; viewed page 1 (SVG renders with both columns and the measured box)",
35	  "Spot-checked counts: memory/ORCHESTRATOR_DECISIONS.md 68 unique D-IDs (D-001..D-068); grep -c '^- 20' memory/LESSONS.md = 44; grep -c '^| debt' memory/SCOPE_CUTS.md = 61; ls personas/*.md = 13; spec/REQUIREMENTS.md 62 unique R-IDs; R-TL-2 (:49), R-TL-10 (:57), R-CO-3 (:137) exist; A-101..A-109 in ASSUMPTIONS",
36	  "Checked the area 3/4 numbers against evals/reports/20261102T164038Z.md (grounding 1.000/242, 0.982/1.000, 40/40, J3 20/20, J4 12/12, 0 false agree, must_not 0)",
37	  "Checked area 8 examples against memory/LESSONS.md:43,45 (12/12 from uncommitted tree; HEAD broke twice), .git/hooks/pre-commit -> tools/check_index_imports.py, reviews/GATE-M3-chaos-tester.md:116 (run stuck after restart), reviews/GATE-M3-round1-triage.md (M3 failed, 2 blockers), board/milestones.md (M0-M2 pass)",
38	  ".venv/bin/python -m evals.run --check-fresh -> exit=0 (the regression claim in area 4 holds)",
39	  "git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; T-179 in_progress (board.py show)",
40	  "git ls-tree --name-only 59e33ca reviews/ | wc -l -> 136; git ls-files submission/prompt-log/reviews | wc -l -> 460; git ls-files evals/reports | grep -cE '[0-9]{8}T[0-9]{6}Z.md$' -> 33; git ls-files --error-unmatch reviews/GATE-M3-product-manager.md -> not known to git",
41	  "python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample (four flag types, 73-day gap, $185 not totaled, export only after accepts)",
42	  "Checked submission/NEEDS_CHRIS.md rows 4-7 against T-189/T-190 (both needs_chris)"
43	 ],
44	 "verdict": "fail",
45	 "scores": {"accuracy": 3, "no_invented_chris_facts": 5, "eight_areas_covered": 4, "ai_acceptance_criteria": 5, "honesty_of_misses": 2, "voice": 4, "length": 5, "visual": 4},
46	 "findings": [
47	  {"severity": "blocker", "title": "The UI redesign after Chris's feedback is missing; the quality-bar table and the SVG present reviewability as met",
48	   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:76 D-068: 'Guided UI redesign (Chris, 2026-11-02: \"VERY hard to use… so simple someone's grandma can use it\")'. part2-process.md:56 'Reviewable | ... at least 4/5 | 4/5 (persona reviewer)'. validation-ladder.svg:97 'every claim quickly\" 4 of 5'. grep -n -iE 'hard to use|redesign|grandma|D-068|guided' submission/part2-process.md -> no match. Area 7 (:87) answers 'How do you get honest, usable feedback' with no build example. The miss-story hooks (:124) list library recall, evidence checks and demo labels, not this.",
49	   "why_it_matters": "Part 2's quality bar is graded on 'what score means ship'. This build's own record says the persona score passed a screen the human rejected. Leaving that out overstates how well the bar worked, which is a dossier red flag (hides a known failure). It also wastes the most persuasive answer the doc could give to areas 4 and 7: AI reviewers are necessary but not enough, so a person at the desk comes before the ship call.",
50	   "fix": "Area 4: add a line under the table: 'Reviewability passed on a persona score and failed in use. I found the M3 screen very hard to use and we rebuilt it (D-068). The ship call now needs a real paralegal session, not a persona score.' Change the table and SVG Result to 'persona 4/5 on the old screen; rejected in use; guided screen not yet scored'. Area 7: use it as the example of honest feedback. Optionally add it to the miss-story hooks.",
51	   "acceptance_test": "grep -n -iE 'hard to use|rebuilt|D-068' submission/part2-process.md returns a line in area 4 or 7; the reviewability Result in the table and SVG no longer reads as met without qualification."},
52	  {"severity": "blocker", "title": "The SVG presents the D-066 compare-confirm as current product behavior; it is not at HEAD",
53	   "evidence": "validation-ladder.svg:58 'A summary the judge disputed needs a named \"I compared it with the quote.\"' (inside 'Rung 3: the paralegal decides'). git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; the enforcement is only in uncommitted app/backend/review.py:298-349; board.py show T-179 -> status in_progress. GATE-M3-product-manager.md:46 measured 5 of 5 disputed entries accepted with one click.",
54	   "why_it_matters": "The diagram is the visual the brief requires, and it claims a safety control on the path to the letter that the shipped code lacks. Overstating a guardrail in a hiring doc is an invented fact about the product (D.2).",
55	   "fix": "Re-verify once T-179 is done and committed. Until then, word rung 3 as 'Decided (D-066), in progress: a disputed summary will need a named confirm'.",
56	   "acceptance_test": "At the submission commit, accepting a judge-disputed item without compared:true returns 422 COMPARE_REQUIRED; otherwise the SVG line is in future tense."},
57	  {"severity": "major", "title": "The unit-test count 5,698 is the figure the cited file says did not reproduce",
58	   "evidence": "part2-process.md:108 'Unit tests (5,698 passed), E2E (412 passed, evals/reports/m3-sensors.md)'. evals/reports/m3-sensors.md:7: '5782 passed, 2 skipped ... The round-2 figure 5698 was taken before later commits added tests and did not reproduce'.",
59	   "why_it_matters": "Area 8 argues 'I check evidence, not claims'. Citing a number its own source disowns undercuts exactly that point.",
60	   "fix": "Cite '5,782 at b824a6c', or re-run at the submission commit and cite that.",
61	   "acceptance_test": "Each test count in part2-process.md equals the count in the cited file for the commit named."},
62	  {"severity": "major", "title": "Area 6 never states engineering's role in product decisions",
63	   "evidence": "Appendix A area 6: 'How are product decisions made among the founders, engineering and you?' part2-process.md:77-79: the table has three columns, 'I decide alone', 'I decide with the litigation lead' and 'A founder decides'. Engineering does not appear in :75-83.",
64	   "why_it_matters": "There is no product org at Zlayt, so who owns build-vs-buy, estimates, model and stack choices, and the LLM/code line is exactly what the founders asked. One of three named parties is missing.",
65	   "fix": "Add an engineering column or two lines. For example: engineering decides how (stack, model routing inside the budget, test design) and has a veto on 'not safe to ship'; I decide what and when; the LLM/code line is drawn together and written down in an ADR.",
66	   "acceptance_test": "Area 6 names at least two decisions engineering owns and how a disagreement with engineering is settled."},
67	  {"severity": "major", "title": "Cited evidence paths and artifact counts do not match what is in the repo",
68	   "evidence": "part2-process.md:44 cites reviews/GATE-M3-product-manager.md -> git ls-files --error-unmatch: 'did not match any file(s) known to git' (the tracked copy is submission/prompt-log/reviews/GATE-M3-product-manager.md). :3 'reviews/ (460 review files)': git ls-tree 59e33ca reviews/ -> 136 files; the 460 are under submission/prompt-log/reviews/. :3 'evals/reports/ (74 dated reports)': 33 tracked.",
69	   "why_it_matters": "The doc's argument is 'point at the artifacts as proof' (Appendix B). A panelist who opens reviews/ and finds 136 files, or a 404 on the gate review, reads it as over-claiming.",
70	   "fix": "Point at the paths that exist in the submitted repo (submission/prompt-log/reviews/), or have the orchestrator commit reviews/ and evals/reports/ first, then recount at the submission commit.",
71	   "acceptance_test": "From a fresh clone of the submission commit, every path in part2-process.md exists, and the counts on line 3 equal ls | wc -l of the named directory."},
72	  {"severity": "minor", "title": "The SVG says record splitting is code only; the build has an LLM split fallback",
73	   "evidence": "validation-ladder.svg:77-78 'Code, no model' / 'Split records.' docs/LLM_VS_CODE.md:29 row 1: 'Only when the code split finds a single record that is unsplit ... may a model be asked ... character offsets only'; D-031 'LLM split fallback (flagged LLM_SPLIT)'.",
74	   "why_it_matters": "The visual should match the graded LLM/code table, and the real design is the more impressive one.",
75	   "fix": "Change to 'Split records (a model may only point at cut offsets for an unsplittable paste; code validates)'.",
76	   "acceptance_test": "Every 'Code, no model' item in the SVG is code-only in docs/LLM_VS_CODE.md."},
77	  {"severity": "minor", "title": "A claim about how PI firms work is stated as fact; the assumption range is off by one",
78	   "evidence": "part2-process.md:23 '**Every matter needs one,** so volume is high.' (no assumption marker, while the line above marks 'assumption, to confirm'). :13 'A-101 to A-108', but memory/ASSUMPTIONS.md also has A-109.",
79	   "why_it_matters": "Appendix A ground rule: 'If you assume something about how personal injury firms work, state the assumption.'",
80	   "fix": "'Every matter with treatment needs one (assumption: confirm the share of matters that reach a demand letter)'; 'A-101 to A-109'.",
81	   "acceptance_test": "Each PI-practice claim in area 2 carries an assumption marker or an A-ID."}
82	 ],
83	 "whats_right": [
84	  "Discovery questions (3 + 3) and the paralegal message and agenda are specific enough to use tomorrow, and they ask for artifacts and errors, not opinions.",
85	  "Three AI acceptance criteria, including the must-never AI-3 on hedges, merged dates and the $185 rate, each with a named checker and a live result.",
86	  "Metrics table defines adoption, time saved, quality and retention with expand and kill thresholds, honestly labeled as starting proposals, and regression discipline is real (--check-fresh exit 0)."
87	 ],
88	 "questions_for_chris": [
89	  "For area 6: what decision rights do you want to give engineering (for example a 'not safe to ship' veto, model choice inside a budget)? The doc should state your stance, not ours."
90	 ]}
91	```
92	
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:15.423Z

Now the HEAD versions of the docs.

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:16.486Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/product-note.md | cat -n; git diff --stat HEAD -- submission/ ; git status --short submission/ evals/reports/library-latest.md",
 "description": "Show HEAD product note and working-tree diffs"
}
````

### User / tool · 2026-11-02T21:28:16.689Z

**tool result**
````
     1	# Treatment Timeline: product note
     2	
     3	Chris [CHRIS: full name] · Zlayt PM project, Part 1 · prototype: [CHRIS: public link] · synthetic data only · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`) · run: `README.md`
     4	
     5	**Problem and user.** A Zinda litigation lead says paralegals spend hours turning records into a treatment chronology before each demand letter, and mistakes cost credibility. The user is the paralegal. She reviews rather than trusts, so every line must be checkable against its source. The attorney signs (assumption A-101).
     6	
     7	**What I built.** Paste or upload records (text or PDF text layer). Each timeline entry shows the AI's summary beside the verbatim quote; she accepts, edits or dismisses it. Code finds the dollar amounts; she accepts each charge one at a time. The export is two blocks that never mix (D-001): a **letter section** (accepted items only, each with quote, provider, date and an `[Ex. __ / Bates __]` placeholder) and **internal notes, do not send** (gaps, conflicts, prior conditions, causation language, amounts not totaled). Every AI step sits behind the validation ladder: model drafts, code checks, a second model checks, she decides. **In progress, not yet in the app:** a guided four-step screen (D-068, T-181) and a confirm for disputed summaries (D-066, T-179).
     8	
     9	**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts, real patient data, EHR integrations, medical or legal judgment. After trying: the "patient said it" label (D-040), per-provider billing totals (D-052) and the drafted treatment paragraph (D-067). **Stretch:** the brief says at most one; I shipped three (source viewer, PDF text layer, calibrated confidence), because D-031 and D-042 reinstated every cut that needed no paid integration or login. [CHRIS: your reason, one line.] The cost: the paragraph went in with no eval and came back out; billing took four rounds.
    10	
    11	**Good enough to ship.** Live run, 3 runs, generator `claude-sonnet-5-5`, judge `claude-haiku-5-5`. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md` (15 packets, run at a74b727, before the billing redesign).
    12	
    13	| # | Criterion (bar) | Result |
    14	|-|-------------|-----------------------|
    15	| 1 | Grounding: every exported statement and amount has a quote in the input (100%) | 1.000, 242 checked [E] |
    16	| 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; report being regenerated). Misses cluster in ledgers, EOBs, scans, Spanish; real misses vs stale expected files not yet separated |
    17	| 3 | Flags: precision, recall 0.9 per type; 28-day gap not flagged, 73-day flagged | golden: 1.000/1.000, four types; 28 no, 73 yes [E]. **Library: 34 of 42 must-flags, 0.81 [L]** |
    18	| 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12, 0 false agrees [E] |
    19	| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Not met on the screen I rejected.** Persona 4/5 on the M3 screen (`submission/prompt-log/reviews/GATE-M3-paralegal.md`), which I found very hard to use; guided screen not scored. 5,795 unit tests passed at 33e88c6 (`artifacts/unit-count-33e88c6.txt`); 412 E2E at d7ea327 (`evals/reports/m3-sensors.md`) |
    20	
    21	**What testing found.**
    22	
    23	- **Reviewability passed on paper and failed in use.** A persona reviewer scored the M3 screen 4/5. When I used it, it was *very* hard to use. I wanted it simple enough for anyone (D-068), so it is being rebuilt as four fixed steps, one question at a time. The 4/5 predates the redesign and does not count for the new screen. An AI reviewer is no substitute for a person at the desk: the ship call needs a real paralegal.
    24	- **The 1.000 flag numbers do not generalize.** Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81 (`submission/prompt-log/reviews/GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes ("Left" against "Right shoulder pain"). Judge numbers are partly in-sample (5 of 17 "held-out" controls still clean).
    25	- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: one letter said $16,147 against a true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads "Billed charges accepted from these records."
    26	- **The M3 gate failed once.** Team-written demo answers were labeled as AI output (fixed in code, final check in progress). One click accepted a disputed summary, 5 of 5 times in 16 cases (same review); the confirm is in progress (T-179).
    27	
    28	**How the AI can mislead her, and what the design does.**
    29	
    30	| Failure | Design |
    31	|-----------|----------------------|
    32	| Changes a number, side or negation; drops a hedge | Code needs each in the quote: hard refusal on her edits, needs-review on AI text; failures go to a visible "could not verify" list |
    33	| Says more than the quote | Code removes unsupported clauses; the second check (scored on seeded wrong items) reads the rest; a disputed one will need a named confirm (D-066, in progress) |
    34	| Invents an amount, or obeys an order in a record | Only code finds money; she accepts each charge; models have no tools |
    35	| Rules on cause or diagnosis | Flag wording is a code template; the model returns a category and a quote only (D-007) |
    36	
    37	**LLM and code.** Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and class, totals, quote and number checks, flag wording, export. The model reads: summary and quote, flag category, one yes/no per code-proposed conflict pair, where to cut a paste code could not split (offsets only, code validates; LLM_SPLIT), and the second check. Table: `docs/LLM_VS_CODE.md`.
    38	
    39	**Three metrics after launch.**
    40	
    41	1. **Minutes from first paste to copied letter section, against her own last three by hand.** Source: case-created and letter-copied timestamps; stopwatch baseline, week 2. Read with #2: skipping review is no win.
    42	2. **Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100.** Source: attorney edit log, adjuster letters the paralegal tags. Target 0; each becomes an eval case.
    43	3. **Needs-review items accepted unchanged, and median seconds per item.** Source: audit log. Verifying or clicking through? (5 of 5 disputed took one click.)
MM submission/NEEDS_CHRIS.md
MM submission/part2-process.md
MM submission/product-note.md
MM submission/validation-ladder.svg
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:18.530Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 -- evals/reports/library-latest.md; git show HEAD:evals/reports/library-latest.md | head -60; git diff --stat HEAD -- evals/reports/library-latest.md",
 "description": "Inspect committed library report"
}
````

### User / tool · 2026-11-02T21:28:18.706Z

**tool result**
````
ce70bd2 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
328428f feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
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

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:20.656Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-185-pm/ ; git show HEAD:evals/reports/library-latest.md > artifacts/review-evidence/T-185-pm/library-HEAD.md && python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/T-185-pm/library-HEAD.md",
 "description": "Sum committed library report recall"
}
````

### User / tool · 2026-11-02T21:28:20.809Z

**tool result (error)**
````
Exit code 1
journey-sample-7860.out
lib_sums.py
lib_sweep-7860.out
note.html
note.pdf
part2.html
part2.pdf
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/lib_sums.py", line 12, in <module>
    n, d = cells[cols.index(name)].split("/")
    ^^^^
ValueError: not enough values to unpack (expected 2, got 1)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:22.433Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-185-pm/lib_sums.py",
 "description": "View lib_sums script"
}
````

### User / tool · 2026-11-02T21:28:22.513Z

**tool result**
````
"""Sum entries / amounts / must-flags columns of a library report table.
Usage: python3 -I lib_sums.py <library-report.md>"""
import sys

rows = [l for l in open(sys.argv[1]) if l.startswith("| case_lib")]
hdr = [l for l in open(sys.argv[1]) if l.startswith("| packet")][0]
cols = [c.strip() for c in hdr.strip().strip("|").split("|")]
tot = {}
for r in rows:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    for name in ("entries", "amounts", "must flags"):
        n, d = cells[cols.index(name)].split("/")
        a, b = tot.get(name, (0, 0))
        tot[name] = (a + int(n), b + int(d))
print(len(rows), "packets")
for k, (n, d) in tot.items():
    print(f"{k}: {n}/{d} = {n / d:.3f}")
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:23.417Z

It trips on the second table's case_lib01 row. I'll write a variant restricted to the first table.

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:26.665Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/lib_sums_r2.py",
 "content": "\"\"\"Sum entries / amounts / must-flags columns of the FIRST table of a library report.\nUsage: python3 -I lib_sums_r2.py <library-report.md>\"\"\"\nimport sys\n\nlines = open(sys.argv[1]).read().splitlines()\nstart = next(i for i, l in enumerate(lines) if l.startswith(\"| packet\") and \"entries\" in l)\ncols = [c.strip() for c in lines[start].strip().strip(\"|\").split(\"|\")]\nrows = []\nfor l in lines[start + 2:]:\n    if not l.startswith(\"|\"):\n        break\n    rows.append(l)\ntot = {}\nfor r in rows:\n    cells = [c.strip() for c in r.strip().strip(\"|\").split(\"|\")]\n    for name in (\"entries\", \"amounts\", \"must flags\"):\n        n, d = cells[cols.index(name)].split(\"/\")\n        a, b = tot.get(name, (0, 0))\n        tot[name] = (a + int(n), b + int(d))\nprint(len(rows), \"packets\")\nfor k, (n, d) in tot.items():\n    print(f\"{k}: {n}/{d} = {n / d:.3f}\")\n"
}
````

### User / tool · 2026-11-02T21:28:26.771Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/lib_sums_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:28.721Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-185-pm/lib_sums_r2.py artifacts/review-evidence/T-185-pm/library-HEAD.md; git grep -n -E \"0\\.580|0\\.775|0\\.681\" HEAD -- evals/reports/ submission/*.md | head -20",
 "description": "Compute library recall and search for 0.580 source"
}
````

### User / tool · 2026-11-02T21:28:28.853Z

**tool result**
````
15 packets
entries: 93/120 = 0.775
amounts: 47/69 = 0.681
must flags: 34/42 = 0.810
HEAD:submission/part2-process.md:44:**Building the test set from real work product.** Zinda picks about 20 closed matters (clean, messy, scanned, billing-heavy, two crashes), the attorney approves them, and they never leave Zinda's environment; access is logged (D-016). The senior paralegal's finished chronology is the answer key. A second paralegal marks entries, amounts, must-flags and must-nots independently; I list the disagreements and the attorney settles them. Answers are written before any run: in `evals/golden/` no expected output was ever produced by running the tool. I split the set, tune on one half, and look at the other half once per release. Part 1 shows why: the golden cases written beside the rules score 1.000 on flags, and 15 separate library packets score 0.81 on must-flags, with entry recall 0.775 and amount recall 0.681 (`evals/reports/library-latest.md`; `submission/prompt-log/reviews/GATE-M3-product-manager.md`).
HEAD:submission/product-note.md:16:| 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; report being regenerated). Misses cluster in ledgers, EOBs, scans, Spanish; real misses vs stale expected files not yet separated |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:31.541Z

**tool call — Bash**
````
{
 "command": "git ls-files --error-unmatch artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md 2>&1; git grep -l \"0.580\\|40/69\" HEAD 2>/dev/null | head; git grep -n \"0\\.580\" HEAD -- . | head",
 "description": "Check whether 0.580 appears in any committed file"
}
````

### User / tool · 2026-11-02T21:28:32.757Z

**tool result**
````
error: pathspec 'artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md' did not match any file(s) known to git
Did you forget to 'git add'?
HEAD:.claude/agent-memory/writer/submission_pipeline.md
HEAD:evals/reports/20261102T040933Z.md
HEAD:submission/product-note.md
HEAD:submission/prompt-log/board-activity.jsonl
HEAD:submission/prompt-log/reviews/T-093-staff-engineer.md
HEAD:submission/prompt-log/reviews/T-185-product-manager.md
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a116f535-t-094-review-sonnet-staff.md
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a164cf78-t-090-review-haiku-staff.md
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a16fff30-t-093-r2-check-relabel-review.md
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a1f2e420-t-100-r2-check-eval-impact.md
HEAD:.claude/agent-memory/writer/submission_pipeline.md:12:**Round 2 (after PM review fail):** render with a scratch copy of print.css plus `body{font-size:Npt}` (script pattern: pandoc --css <copy> then Chrome). Product note needed ~1050 words at 8.7pt; table column widths (dash counts) and orphan last lines matter more than words. Cite only paths `git ls-files` knows: reviews are tracked at `submission/prompt-log/reviews/`, not `reviews/`. Run a backtick-path existence check before handoff. Unit count: `git archive HEAD` into scratch, symlink `.venv`, pytest (about 6 min), save under `artifacts/unit-count-<sha>.txt`; a count is valid only for its commit. Library recall: committed `evals/reports/library-latest.md` (a74b727) gives entries 0.775, amounts 0.681, flags 0.81; the PM reviewer's d0b04bc run (untracked evidence) gave amounts 0.580 — flag the mismatch, don't pick silently. Never present T-181/T-179 as built until committed.
HEAD:submission/product-note.md:16:| 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; report being regenerated). Misses cluster in ledgers, EOBs, scans, Spanish; real misses vs stale expected files not yet separated |
HEAD:submission/prompt-log/board-activity.jsonl:4396:{"ts": "2026-11-02T21:19:09Z", "event": "note", "agent": "orchestrator", "card": "T-185", "text": "Round 2: (a) state Chris's 'VERY hard to use' verdict and the D-068 redesign plainly as the turning point; reviewability score reported as pre-redesign; (b) describe T-181/T-179 only as what is committed, marking unfinished items 'in progress' — final wording refresh after T-181 lands; (c) use test counts from a fresh run cited by file; give reasons for the stretch items; cite only reviews in git; report library recall (entries 0.775, amounts 0.580) next to golden."}
HEAD:submission/prompt-log/reviews/T-185-product-manager.md:16:- Library entry and amount recall (0.775 and 0.580 on the same library run) go unmentioned while the note implies only flags fail to generalize.
HEAD:submission/prompt-log/reviews/T-185-product-manager.md:31:  "python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> entries 93/120 = 0.775, amounts 40/69 = 0.580, must flags 34/42 = 0.810",
HEAD:submission/prompt-log/reviews/T-185-product-manager.md:68:  {"severity": "major", "title": "Generalization is reported only for flags; the same library run shows entry recall 0.775 and amount recall 0.580",
HEAD:submission/prompt-log/reviews/T-185-product-manager.md:69:   "evidence": "product-note.md:16 row 2 'entries 0.982, amounts 1.000 [E]' (golden only); :23 'The 1.000 flag numbers do not generalize'. python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> 'entries: 93/120 = 0.775', 'amounts: 40/69 = 0.580', 'must flags: 34/42 = 0.810'. The committed evals/reports/library-latest.md is from a74b727 (stale; the writer's handoff says so).",
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a231474a-backend-t-143-round-2.md:1989:### Assistant · claude-sonnet-5-5 · 2026-11-02T13:24:30.580Z
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a26f2e65-t-046-r2-check-haiku-ux.md:2479:### User / tool · 2026-11-02T04:55:10.580Z
HEAD:submission/prompt-log/transcripts/session-6ddf8076-a597a006-writer-t-185-t-186-round-2.md:17:- **Numbers come from files in git.** For the test count, run `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` from a `git archive HEAD` copy in your scratch dir, save the output under artifacts/, and cite that file. Report library recall (entries 0.775, amounts 0.580) next to the golden figures; take both from evals/reports.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:28:50.570Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/part2-process.md | cat -n",
 "description": "Show HEAD Part 2 doc"
}
````

### User / tool · 2026-11-02T21:28:50.668Z

**tool result**
````
     1	# Part 2: from Zinda's request to a shipped, measured feature
     2	
     3	Chris [CHRIS: full name] · Zlayt AI PM project. Part 1 was built by a team of AI agents on a board that I directed, so where I can, I answer with that process and point at its artifacts: `board/`, `submission/prompt-log/reviews/` (460 review files), `evals/reports/` (27 dated reports), `memory/ORCHESTRATOR_DECISIONS.md` (68 decisions). Paths are as committed; counts are at the commit this doc was last edited. Assumptions about how Zinda works are marked as assumptions.
     4	
     5	![Validation ladder: what stands between an AI draft and the letter](validation-ladder.svg){width=88%}
     6	
     7	## 1. Discovery
     8	
     9	**Who first.** The litigation lead who asked, then two or three paralegals who build chronologies, then the attorney who signs the demand. In that order, because the lead tells me what a mistake costs and the paralegals tell me where the time goes.
    10	
    11	**Request versus need.** The request is "faster." The need is "faster without a new way to be wrong." I ask for artifacts, not opinions: the last finished chronology, the letter it went into, and the adjuster's reply. Then I compare what they say with what they did, and note every point where she opens the source to check a line, because that is the step the tool must make cheap, not remove.
    12	
    13	**Watching real work without client data.** She works on her own machine on a closed matter; I watch, I copy nothing, I record nothing, and I write down steps, never content. If the firm prefers, she redoes a closed matter from a redacted copy, or we use synthetic records as in Part 1. In this build I had no access to Zinda's people, so my first interviews are the assumptions I wrote down (`memory/ASSUMPTIONS.md`, A-101 to A-109, each with "what changes if wrong" and "how to check") plus 13 researched persona dossiers (`personas/`). [CHRIS: optional, one real example of watching work without exposing client data.]
    14	
    15	| First three questions to the litigation lead | First three to a paralegal |
    16	|--------------|--------------|
    17	| 1. Take the last demand letter that went out. Where did the chronology wait on the way from records arriving to letter sent? | 1. Walk me through the last chronology you built, starting from the first record you opened. |
    18	| 2. Tell me about the last time an adjuster pushed back on a date or a fact. What did it cost: days, or dollars off the offer? | 2. Which entries do you always re-check against the source, and how? Which one burned you once? |
    19	| 3. What will you never let software write in a letter, and what would you check before you signed one it helped with? | 3. When two records disagree, or there is a long gap, where do you write that down, and who sees it? |
    20	
    21	## 2. Prioritization
    22	
    23	Chronology comes before demand drafting, deposition summaries and discovery responses for four reasons. **It sits upstream:** a letter drafted on an unchecked chronology repeats its errors. **It is checkable:** every output line traces to a source line, so I can measure quality before anyone uses it (this build has 40 seeded wrong summaries, a 73-day gap that must flag and a 28-day one that must not). Drafting prose from facts is harder to ground; depositions and discovery come later in a matter (assumption, to confirm). **The cost of error is concentrated here:** the lead said mistakes cost credibility with adjusters. **Every matter with treatment needs one,** so volume is high (assumption: confirm what share of matters reach a demand letter).
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
    44	**Building the test set from real work product.** Zinda picks about 20 closed matters (clean, messy, scanned, billing-heavy, two crashes), the attorney approves them, and they never leave Zinda's environment; access is logged (D-016). The senior paralegal's finished chronology is the answer key. A second paralegal marks entries, amounts, must-flags and must-nots independently; I list the disagreements and the attorney settles them. Answers are written before any run: in `evals/golden/` no expected output was ever produced by running the tool. I split the set, tune on one half, and look at the other half once per release. Part 1 shows why: the golden cases written beside the rules score 1.000 on flags, and 15 separate library packets score 0.81 on must-flags, with entry recall 0.775 and amount recall 0.681 (`evals/reports/library-latest.md`; `submission/prompt-log/reviews/GATE-M3-product-manager.md`).
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
    56	| Reviewable | paralegal rates "I could verify every claim quickly" at least 4/5 | persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored |
    57	
    58	**Reviewability passed on a persona score and failed in use.** An AI persona rated the M3 screen 4/5 on "I could verify every claim quickly". When I used the screen myself it was very hard to use, and I asked for it to be so simple that anyone could use it (D-068). We are rebuilding it as four fixed steps with one question at a time (T-181, in progress). So the bar now reads: a persona score is a screen, not a ship call. The ship call needs a real paralegal session on the final screen.
    59	
    60	**Catching regressions.** Any change to a prompt, model, phrase list or schema reruns the eval before review. Prompts are versioned files; each report records the source commit and prompt hashes; `python -m evals.run --check-fresh` fails if the recorded report no longer matches the files. Every bug that escapes becomes a case. A fixture replay is quick; a live run takes about 40 minutes and model spend, so live runs happen before gates.
    61	
    62	## 5. Ship and learn
    63	
    64	**Rollout.** Stage 0, shadow: she builds her chronology as usual on 5 closed matters while the tool builds its own, and we compare. Stage 1: two paralegals use it on live matters; the attorney sees the internal notes. Stage 2: the whole team. Each stage opens only when the one before meets its numbers.
    65	
    66	**Feedback.** A 20-minute weekly check-in per paralegal (agenda in area 7), plus the audit log: every accept, edit and dismiss is stored with before and after, so I see where it was wrong without asking. [CHRIS: optional, one line on how you measured adoption on the OutSystems AI Agent Builder.]
    67	
    68	| Measure | Definition | Expand if | Kill if |
    69	|----|----------|-------|-------|
    70	| Adoption | Share of demand letters whose chronology started in the tool | at least 60% after 20 matters | under 25% after 6 weeks of fixes |
    71	| Time saved | Median minutes, first paste to copied letter section, against her last three by hand | down at least 30% | down under 10% after 6 weeks |
    72	| Output quality | Escaped errors per 100 letter lines (found by the attorney or an adjuster); share of needs-review items accepted unchanged | 0 escaped errors; accept-unchanged rate stable | two unsupported facts reach a carrier |
    73	| Retention | Paralegals using it on two or more matters in week 8, among those active in week 4 | at least 80% | under 50% |
    74	
    75	These are my starting numbers; the lead and I agree them in week 1. In between, I iterate: the cheapest fix that moves the weakest number.
    76	
    77	## 6. Operating rhythm and fast decisions
    78	
    79	| I decide alone, same day | I decide with the litigation lead | A founder decides |
    80	|-------|---------|---------|
    81	| copy and wording, queue order, which eval cases to add, bug triage, a scope cut inside a feature | anything that changes what leaves the firm in a letter (flags stay out of the letter, D-001; the total line wording, D-062), what counts as an error | spend and vendors (model provider, data retention), any real client data in any environment, public exposure, expand or kill |
    82	
    83	**Engineering.** Engineering decides how: stack, which model runs where inside the budget, test design, build or buy. Engineering has a veto on "not safe to ship" that I cannot overrule alone; only a founder can, in writing. I decide what and when. The LLM/code line is drawn together and written down (`docs/LLM_VS_CODE.md`). A disagreement gets settled by evidence first: we write the test or eval case that would show who is right. If it is still open, the safer answer holds for anything the carrier sees, and a founder decides scope and timing. This is my stance until a founder says otherwise (NEEDS_CHRIS #9). In this build a blocker from the staff-engineer reviewer kept a card open until it was fixed.
    84	
    85	**Speed.** Each question to a founder is one line with my default and what it unblocks. I ask for an answer within one business day (three for a vendor or spend call). No answer, and the default goes ahead and is logged, if it is reversible. This is how the build ran: `submission/NEEDS_CHRIS.md` holds only what needs a human, each row with its assumption, and nothing waits.
    86	
    87	**First 30 days.** Week 1: shadow three paralegals and the attorney; start the assumptions list, the decision log and the board. Week 2: timed baselines; pick and annotate the 20 matters. Week 3: spec and API contract signed off; first slice running on the test set. Week 4: ship-bar run, stage 0 shadow, go or no-go for stage 1.
    88	
    89	## 7. Communicating with the team
    90	
    91	**Honest feedback from busy people.** I do not ask whether they like it. I put output in front of them and ask them to find the error. In a "find the error" session I hand a paralegal a chronology with planted mistakes mixed in with the tool's own, and see what she catches. It is the same idea as the seeded wrong items that grade our judges. I sit with the paralegals without the lead present, since people say less in front of the person who assigns the work. I watch what they do, and trust it over what they say. This build is the example: an AI persona rated the screen 4/5, and I found it very hard to use (D-068). What a person does with it beats what a proxy scores, so the guided screen goes to a real paralegal before I call it done.
    92	
    93	**A message I would send a paralegal**
    94	
    95	> Subject: 20 minutes on one chronology?
    96	>
    97	> Hi [name], I'm building the tool that drafts the treatment chronology, and I need to hear where it's wrong, not whether it's nice. Could I have 20 minutes at your desk this week? Pick a matter that's already closed. You'll build the chronology the way you normally do while I watch; I won't copy or record anything. Then I'll hand you one the tool made for a different closed matter, with a few mistakes I planted, and you mark what you'd catch. Most useful to me: the entry you always re-check, and the one that burned you. If this week is bad, say "not this week." That helps too. Chris
    98	
    99	**Meeting agenda, 30 minutes, one paralegal:** 0-3 why I'm here and what I will not do (no client data leaves your machine). 3-13 you walk me through a closed matter. 13-23 you mark the tool's chronology: lines you'd trust, lines you wouldn't, why. 23-28 what would make you stop using it. 28-30 what I'll change and when you'll hear back.
   100	
   101	**Unhappy, silent, or conflicting users.** Unhappy: reproduce the problem on her own example in the room, tell her what changes and by when, then close the loop in writing within the week. Silent: I read the audit log first (items dismissed, time per item), then ask about one specific item, never "any feedback?" Conflicting: the person who signs the letter decides what goes in it; the person doing the work decides how the work flows. I tell both what I decided and why. The same call came up in the build: a paralegal reviewer blocked the first spec because accepted flags would have gone to the carrier. Accepting a flag now means "I've seen it," and flags live in internal notes (D-001).
   102	
   103	**Founders, without more meetings.** One page every Friday: shipped, the four numbers above, decisions I need with my default, risks. A decision log they can read at any time. No standing meeting. This build ran the same way: `memory/STATE.md` and `submission/NEEDS_CHRIS.md`.
   104	[CHRIS: optional, one line on a time you got honest feedback from users who said little.]
   105	
   106	## 8. Supervising developers
   107	
   108	**Before they start:** the spec with R-IDs, the API contract, the golden set, the LLM/code table, non-goals, and a card per task whose acceptance criteria name the exact check. A developer who cannot say how a card will be tested does not start it.
   109	
   110	**Each week:** the board (cards by state, review rounds per card), the eval report against the last one (did a metric drop, did a prompt hash change), bugs that escaped, review findings by severity, decisions waiting on me. I check evidence, not claims. Two examples from this build: a worker's "12/12 pass" came from an uncommitted working tree and the committed code rendered no charges panel; two partial commits broke HEAD. The rule now is to verify from `git archive HEAD`, and pre-commit compiles every staged file (`memory/LESSONS.md`, 44 entries).
   111	
   112	**Before release.** Unit tests (5,795 passed at 33e88c6, `artifacts/unit-count-33e88c6.txt`), E2E (412 passed at d7ea327, `evals/reports/m3-sensors.md`), the live eval against the ship bar, a clean-clone install timed against the 5-minute bar, and adversarial reviewers: a claims adjuster who outworded my billing rules for four rounds, a chaos tester who found a run that stayed "running" forever after a restart. **Who signs off:** a reviewer in a fresh context who did not write the work, and me. Workers never close their own cards. Milestone gates: M0, M1, M2 passed; M3 failed its first round with two blockers (`submission/prompt-log/reviews/GATE-M3-round1-triage.md`).
   113	
   114	**When work is late or a bug reaches users.** Late: I cut scope, not checks. D-063 held every non-P0 card to finish the MVP. After three review rounds I either accept with written debt (62 rows in `memory/SCOPE_CUTS.md`) or cut. A bug in front of users: stop, reproduce, write the failing test or eval case first, fix, then record the lesson. Example: demo answers prepared by our team were labeled as AI output; the decision is D-065 and the fix is committed. A second example is still open: a disputed summary was one click from the letter (D-066, in progress).
   115	
   116	**AI used:** to build (orchestrator on Opus, workers on Sonnet, reviewers as adversarial personas), to draft documents, to red-team. **AI not used:** to approve its own work, to set the ship-bar numbers, to draw the LLM/code line, to talk to users, to send anything. [CHRIS: optional, one real example of supervising developers on a late feature.]
   117	
   118	## The one story: a miss
   119	
   120	> **[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark, and the team will not write it for you.**
   121	> Suggested shape, about 200 words:
   122	>
   123	> 1. What you shipped and what you expected it to do.
   124	> 2. What you missed, and the number or signal that showed it.
   125	> 3. One concrete thing you changed in your process afterward: an artifact or a rule, not "communicate more."
   126	> 4. How that change shows up in this project.
   127	>
   128	> Hooks from this build you can tie it to: a "must never" acceptance criterion written before building; a held-out test set looked at once (golden 1.000 against library 0.81); a persona score that passed a screen you found very hard to use; checking evidence instead of a worker's claim; the demo that labeled prepared answers as AI output.**]**
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:06.983Z

**tool call — Bash**
````
{
 "command": "echo \"reviews:\"; git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | wc -l; echo \"dated reports:\"; git ls-tree --name-only HEAD evals/reports/ | grep -cE '[0-9]{8}T[0-9]{6}Z\\.md$'; git ls-tree --name-only HEAD evals/reports/ | grep -cE '[0-9]{8}T[0-9]{6}Z'; echo \"D-IDs:\"; git show HEAD:memory/ORCHESTRATOR_DECISIONS.md | grep -oE '^[#*| -]*D-[0-9]{3}' | grep -oE 'D-[0-9]{3}' | sort -u | wc -l; git show HEAD:memory/ORCHESTRATOR_DECISIONS.md | grep -oE 'D-[0-9]{3}' | sort -u | tail -2; echo \"debt rows:\"; git show HEAD:memory/SCOPE_CUTS.md | grep -c '^| debt'; echo lessons; git show HEAD:memory/LESSONS.md | grep -c '^- 20'; echo personas; git ls-tree --name-only HEAD personas/ | grep -c '\\.md$'; echo assumptions; git show HEAD:memory/ASSUMPTIONS.md | grep -oE 'A-1[0-9]{2}' | sort -u | tr '\\n' ' '; echo; echo RIDs; git show HEAD:spec/REQUIREMENTS.md | grep -oE 'R-[A-Z]+-[0-9]+' | sort -u | wc -l",
 "description": "Recount Part 2 artifact counts at HEAD"
}
````

### User / tool · 2026-11-02T21:29:07.309Z

**tool result**
````
reviews:
     467
dated reports:
33
39
D-IDs:
      68
D-067
D-068
debt rows:
61
lessons
28
personas
13
assumptions
A-101 A-102 A-103 A-104 A-105 A-106 A-107 A-108 A-109 
RIDs
      63
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:12.612Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD; git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | grep -c '\\.md$'; git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | grep -v '\\.md$' | head; git ls-tree --name-only HEAD evals/reports/ | grep -E '[0-9]{8}T[0-9]{6}Z' | sed 's/\\..*//' | sort -u | wc -l; git ls-tree --name-only HEAD evals/reports/ | head -50",
 "description": "Investigate review and report counts"
}
````

### User / tool · 2026-11-02T21:29:12.807Z

**tool result**
````
2e58e18f4e6800a5bebfb57eeb22fe57fa3efab8
466
submission/prompt-log/reviews/T-103-staff-engineer-r4-CORRECTION-1.txt
      33
evals/reports/20261102T020824Z.md
evals/reports/20261102T020933Z.md
evals/reports/20261102T021029Z.md
evals/reports/20261102T021046Z.md
evals/reports/20261102T022701Z.md
evals/reports/20261102T022927Z.md
evals/reports/20261102T023039Z.md
evals/reports/20261102T025219Z.md
evals/reports/20261102T025715Z.md
evals/reports/20261102T032823Z.md
evals/reports/20261102T035750Z.md
evals/reports/20261102T040933Z.md
evals/reports/20261102T081339Z.md
evals/reports/20261102T083252Z.md
evals/reports/20261102T085207Z.md
evals/reports/20261102T095640Z.md
evals/reports/20261102T104043Z.md
evals/reports/20261102T111004Z.md
evals/reports/20261102T113305Z.md
evals/reports/20261102T115041Z.md
evals/reports/20261102T115607Z.md
evals/reports/20261102T120809Z.md
evals/reports/20261102T121612Z.md
evals/reports/20261102T123428Z.md
evals/reports/20261102T124856Z.md
evals/reports/20261102T164038Z.md
evals/reports/20261102T195748Z.md
evals/reports/calibration.json
evals/reports/controls-20261102T042306Z.json
evals/reports/controls-20261102T042306Z.md
evals/reports/controls-20261102T063331Z.json
evals/reports/controls-20261102T063331Z.md
evals/reports/controls-20261102T075238Z.json
evals/reports/controls-20261102T075238Z.md
evals/reports/controls-20261102T090925Z.json
evals/reports/controls-20261102T090925Z.md
evals/reports/controls-20261102T102626Z.json
evals/reports/controls-20261102T102626Z.md
evals/reports/controls-20261102T123937Z.json
evals/reports/controls-20261102T123937Z.md
evals/reports/determinism-diagnosis.md
evals/reports/latest.json
evals/reports/library-latest.md
evals/reports/m3-sensors.md
evals/reports/runs
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:16.670Z

**tool call — Bash**
````
{
 "command": "git log --oneline ddfbf6d..HEAD; for c in ddfbf6d HEAD; do echo $c; git ls-tree -r --name-only $c submission/prompt-log/reviews/ | wc -l; git show $c:memory/LESSONS.md | grep -cE '^- '; git show $c:memory/SCOPE_CUTS.md | grep -ciE '^\\| *debt'; done; git diff ddfbf6d HEAD --stat -- submission/product-note.md submission/part2-process.md submission/validation-ladder.svg submission/NEEDS_CHRIS.md evals/reports/library-latest.md",
 "description": "Check commits after fix and counts at ddfbf6d"
}
````

### User / tool · 2026-11-02T21:29:16.921Z

**tool result**
````
2e58e18 fix(backend): T-177 r3 every backend sentence for a prepared item says prepared answer (flag steps and why, failed and missing curated answers, run messages); /classic redirects to the guided UI in demo and public mode
c031483 fix(release): T-182 r2 one-line startup errors, claude_cli kept out of the image, make evals documented, digest-pinned base, troubleshooting
ddfbf6d
     467
28
61
HEAD
     467
28
61
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:21.112Z

**tool call — Bash**
````
{
 "command": "git show HEAD:memory/LESSONS.md | head -20; git show HEAD:memory/LESSONS.md | grep -cE '^(- |\\* |[0-9]+\\. |## )'; git show HEAD:memory/LESSONS.md | wc -l; git diff --stat HEAD -- memory/LESSONS.md memory/SCOPE_CUTS.md",
 "description": "Inspect LESSONS format at HEAD"
}
````

### User / tool · 2026-11-02T21:29:21.266Z

**tool result**
````
# LESSONS (append-only via `board.py lesson`)

What worked, what didn't, and what harness change it caused.

- 2026-11-02T00:10:23Z **orchestrator**: git-guard fired on a destructive-git phrase inside heredoc file content and again inside a quoted --text note (the hook went live mid-session via settings hot-reload). Harness change: strip heredoc bodies and quoted args before matching, except when the command executes a string (bash -c, eval, xargs, ssh); rm checks use the raw command via shlex. Regression tests added. Rule: file content and note text are data, not commands.
- 2026-11-02T00:12:12Z **orchestrator**: A stale root-level needs_chris.md from a previous attempt (MASTER_PROMPT missing) was superseded by submission/NEEDS_CHRIS.md, the lane the contract defines.
- 2026-11-02T00:15:25Z **orchestrator**: tailscale serve --https=443 silently replaced an existing mapping on Chris's tailnet (443 -> 127.0.0.1:4173). Restored it; board now on :7777, app will use :7860. Rule: run 'tailscale serve status' before any serve command and never reuse an occupied port.
- 2026-11-02T00:15:25Z **orchestrator**: Agent definitions written mid-session are not loaded by the Desktop host (Agent tool: 'Agent type not found'). Fallback: general-purpose subagent whose first step is 'python3 tools/agent_prompt.py <name>'; model set per definition. Reviewer write-guard hook is not attached in fallback — instruction-only, plus board-validate on review files. NEEDS_CHRIS: restart the session once to load native definitions.
- 2026-11-02T00:20:17Z **orchestrator**: A haiku mechanical reviewer filed a major on two false state claims (said PROGRESS marked a check PASS; said T-006 was READY). Harness change: reviewer rules now require any claim about state (board, files, git) to quote the command and its output as evidence; the orchestrator re-verifies a finding's evidence before acting on it.
- 2026-11-02T00:21:19Z **orchestrator**: Stop-guard counted queued work (cards assigned to a busy worker, reviews already dispatched) as actionable, which would trap the orchestrator in block loops while waiting. Harness change: board.py assign/dispatch markers; status excludes recently assigned ready cards (180 min) and dispatched reviews (90 min). Test added.
- 2026-11-02T00:22:43Z **orchestrator**: Native agent types appeared ~20 min after the definitions were written (host reloaded .claude/agents mid-session). Switched reviewers/workers to native types (write-guard hook now attached); agent_prompt.py stays as fallback. NEEDS_CHRIS #2 withdrawn.
- 2026-11-02T00:27:32Z **researcher**: Persona dossiers: fanning source-gathering out to parallel subagents (each told to fetch-verify every URL and mark unverified) gave 4-12 verified sources per persona fast; americanbar.org and PubMed block fetch, use ABA press releases/Europe PMC and mark secondary. Concurrent subagent cap hit at 4th spawn — plan for it.
- 2026-11-02T00:30:38Z **researcher**: statutes.capitol.texas.gov, americanbar.org, ecfr.gov, hhs.gov and ajnr.org return nav-only/403/redirect to WebFetch; use mirrors (rulesofcivilprocedure.com, texas.public.law, law.cornell.edu, codes.findlaw.com) and court PDFs extracted with pdftotext, and label read depth per source. Lexicon: ship test vectors (hit/miss/negated) + a strength tier inside the YAML so precision risk from context-only phrases is explicit and testable.
- 2026-11-02T00:33:54Z **orchestrator**: The hardened secret scanner blocked my own commit: a test fixture held a literal key-shaped assignment. Fixed by building the string by concatenation. The PreToolUse guard scans before the command runs, so the fix and the commit must be separate tool calls.
- 2026-11-02T00:51:53Z **researcher**: Round-1 lexicon passed its own examples but failed 37/78 + 38/63 reviewer probes: a self-check that only replays the author's vectors proves nothing. Harness change: lexicon_selfcheck.py now runs every golden case (recall per must-flag, must_not) and both reviewer probe sets, with an FP bar. Negation must be clause-bounded, with an explicit list exception.
- 2026-11-02T00:54:18Z **orchestrator**: Native agent definitions appear to be snapshotted when the host loads them; a recompile mid-session may not reach the next reviewer (litigation-lead r3 saw pre-round-3 text). Harness change: every reviewer's first step is to read its live personas/<slug>.md, which supersedes the compiled body. Drift test (compile_agents --check) still guards the files.
- 2026-11-02T00:54:30Z **orchestrator**: Research text invented a fact about the sample case ('referral to pain management'). Research is an input to personas, lexicon and golden files, so an invented fact there propagates. Harness change: research rows that describe the sample case must quote the record (adjuster r2 caught it).
- 2026-11-02T00:56:08Z **researcher**: T-008 r2 failed on one invented sample-case fact ('referral to pain management') written as a paraphrase in a research table. Rule: every statement about the sample case in research/ quotes the record (or names the header date); before handoff, grep for rec/record/Rivera and check each hit.
- 2026-11-02T00:59:29Z **orchestrator**: M1 burned ~10% of the weekly plan largely on 2-reviewer x 3-round review churn with opus reviewers. Harness change (D-024): one sonnet reviewer per card, opus only at gates, 2-round cap on docs with debt, short briefs/replies.
- 2026-11-02T01:52:00Z **backend**: Parallel backend workers share one git index: 'git add X' then commit can include another worker's staged files. Use 'git commit <paths> -m' (path-limited) so only your files go in.
28
      32
 memory/LESSONS.md    | 16 ++++++++++++++++
 memory/SCOPE_CUTS.md |  2 ++
 2 files changed, 18 insertions(+)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:30.664Z

**tool call — Bash**
````
{
 "command": "git show HEAD:spec/REQUIREMENTS.md | grep -oE '^\\| *\\*?\\*?R-[A-Z]+-[0-9]+' | grep -oE 'R-[A-Z]+-[0-9]+' | sort -u | wc -l; git show HEAD:spec/REQUIREMENTS.md | grep -oE 'R-[A-Z]+-[0-9]+' | sort | uniq -c | sort -n | head -5; git show HEAD:memory/SCOPE_CUTS.md | grep -iE '^\\| *debt' | wc -l; git diff HEAD -- memory/SCOPE_CUTS.md | grep '^+' ",
 "description": "Verify R-ID and debt row counts"
}
````

### User / tool · 2026-11-02T21:29:30.835Z

**tool result**
````
      62
   1 R-CH-4
   1 R-CH-5
   1 R-CH-6
   1 R-CO-1
   1 R-CO-2
      61
+++ b/memory/SCOPE_CUTS.md
+| 24 | Per-client rate limit and spend cap on the public demo (D-020, CONTRACT §314) | The public build makes no model calls (demo mode serves prepared answers), so there is no wallet to protect. Storage and in-flight run caps (T-183) bound disk and CPU; a per-IP limiter is not built, so one scripted client can fill the 200-case table and lock visitors out until the 24 h purge (T-183 r2 minor). | Per-IP token bucket + spend ledger if a live key is ever exposed publicly; ~0.5 day. | post-MVP |
+| debt | T-045 accepted with documented debt after 2 rounds (§7.4) | staff r3 pass; residual: a consistent body+header forgery of a live report is caught only by recompute (full metrics never committed) | see card | M3 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:34.260Z

**tool call — Bash**
````
{
 "command": "git ls-files --error-unmatch artifacts/unit-count-33e88c6.txt && git show HEAD:artifacts/unit-count-33e88c6.txt | head -5; git show HEAD:artifacts/unit-count-33e88c6.txt | tail -5; git show HEAD:evals/reports/m3-sensors.md | sed -n 1,15p",
 "description": "Verify unit and E2E count sources"
}
````

### User / tool · 2026-11-02T21:29:34.392Z

**tool result**
````
error: pathspec 'artifacts/unit-count-33e88c6.txt' did not match any file(s) known to git
Did you forget to 'git add'?
........................................................................ [ 98%]
........................................................................ [ 99%]
...........................................                              [100%]
5795 passed, 8 skipped in 356.75s (0:05:56)
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:39.123Z

**tool call — Bash**
````
{
 "command": "git ls-tree HEAD artifacts/unit-count-33e88c6.txt; git status --short artifacts/unit-count-33e88c6.txt; git show HEAD:artifacts/unit-count-33e88c6.txt | head -8",
 "description": "Check unit-count file in HEAD tree"
}
````

### User / tool · 2026-11-02T21:29:39.259Z

**tool result**
````
100644 blob b7958bd6573000ee96ccda9ba23523d656e2b283	artifacts/unit-count-33e88c6.txt
D  artifacts/unit-count-33e88c6.txt
?? artifacts/unit-count-33e88c6.txt
# Unit test count, writer, T-185/T-186 round 2, 2026-11-02
# Commit: 33e88c6862f4838648c6ce6bc7f27327123f2267 (git archive HEAD, extracted to a scratch directory; .venv symlinked from the working tree)
# Command: .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider   (E2E_REQUIRE_DB not set, so DB-gated unit tests skip: 8 skipped here, 2 skipped in evals/reports/m3-sensors.md)
# Result line: 5795 passed, 8 skipped in 356.75s (0:05:56), exit 0

........................................................................ [  1%]
........................................................................ [  2%]
........................................................................ [  3%]
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:45.655Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/paths_in_head.py",
 "content": "\"\"\"List backticked paths in a doc at HEAD and whether each exists in the HEAD tree.\nUsage: python3 -I paths_in_head.py <repo> <path-in-repo> [...]\"\"\"\nimport re\nimport subprocess\nimport sys\n\nrepo = sys.argv[1]\nfor doc in sys.argv[2:]:\n    text = subprocess.run([\"git\", \"-C\", repo, \"show\", \"HEAD:\" + doc], capture_output=True, text=True).stdout\n    paths = sorted(set(re.findall(r\"`([^`\\s]+)`\", text)))\n    print(\"==\", doc)\n    for p in paths:\n        if \"/\" not in p and \".\" not in p:\n            continue\n        clean = p.rstrip(\"/\")\n        rc = subprocess.run([\"git\", \"-C\", repo, \"cat-file\", \"-e\", \"HEAD:\" + clean], capture_output=True).returncode\n        print(\"OK  \" if rc == 0 else \"MISS\", p)\n"
}
````

### User / tool · 2026-11-02T21:29:45.768Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/paths_in_head.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:47.328Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-185-pm/paths_in_head.py /Users/arsis/zlayt-pm-project submission/product-note.md submission/part2-process.md",
 "description": "Check every cited path exists in HEAD"
}
````

### User / tool · 2026-11-02T21:29:48.049Z

**tool result**
````
== submission/product-note.md
OK   README.md
OK   artifacts/unit-count-33e88c6.txt
OK   docs/LLM_VS_CODE.md
OK   evals/reports/20261102T164038Z.md
OK   evals/reports/library-latest.md
OK   evals/reports/m3-sensors.md
OK   memory/SCOPE_CUTS.md
OK   submission/prompt-log/TOOLS.md
OK   submission/prompt-log/reviews/GATE-M3-paralegal.md
OK   submission/prompt-log/reviews/GATE-M3-product-manager.md
OK   submission/prompt-log/reviews/T-140-claims-adjuster.md
== submission/part2-process.md
OK   artifacts/unit-count-33e88c6.txt
OK   board/
OK   docs/LLM_VS_CODE.md
OK   evals/golden/
OK   evals/golden/sample.expected.json
OK   evals/reports/
OK   evals/reports/20261102T164038Z.md
OK   evals/reports/library-latest.md
OK   evals/reports/m3-sensors.md
OK   memory/ASSUMPTIONS.md
OK   memory/LESSONS.md
OK   memory/ORCHESTRATOR_DECISIONS.md
OK   memory/SCOPE_CUTS.md
OK   memory/STATE.md
OK   memory/contracts/api.md
OK   personas/
OK   spec/REQUIREMENTS.md
OK   submission/NEEDS_CHRIS.md
OK   submission/prompt-log/reviews/
OK   submission/prompt-log/reviews/GATE-M3-product-manager.md
OK   submission/prompt-log/reviews/GATE-M3-round1-triage.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:29:53.531Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/prompt-log/reviews/T-140-claims-adjuster.md | grep -n -E '16,147|8,123' | head -3; echo ---; git show HEAD:submission/prompt-log/reviews/GATE-M3-product-manager.md | grep -n -E '5 of 5|16 cases|one click|0\\.81|34/42' | head -8; echo ---; git show HEAD:submission/prompt-log/reviews/T-140-claims-adjuster.md | grep -n -E '5 of 5|16 cases' | head; echo ---; git show HEAD:memory/ORCHESTRATOR_DECISIONS.md | grep -n -E '^\\S*.{0,10}D-0(31|42|59|62|63|64|65|66|67|68)\\b' | cut -c1-400",
 "description": "Verify billing, gate and decision claims"
}
````

### User / tool · 2026-11-02T21:29:53.703Z

**tool result**
````
10:- Across the library, lib10 (EOB) still prints **$16,147.00**. The records state $8,123.50.
14:Deterministic checks first: `pytest tests/unit/test_amounts_t140.py tests/unit/test_amounts.py tests/unit/test_billing.py tests/unit/test_export.py -q` on the HEAD tree gave `457 passed in 5.89s`. `python -m evals.library_report` on the HEAD tree reported the accept-all column `WRONG $16,147.00 vs $8,123.50` for lib10 and WRONG for lib04/05/06/09. The other 10 cases were ok.
29:| lib10 | **$16,147.00** | $8,123.50 | **over: EOB "Amount billed $8,023.50" counted on top of the UB-04 lines** |
---
46:- Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click.
57:  "lib_sweep.py over the sample + 15 library cases: needs_review counts, and judge-disputed entries accepted with one click (lib_sweep.out: 106/297 needs_review; 5 of 5 disputed accepted with 200)",
76:   "evidence": "lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.",
77:   "why_it_matters": "Ship bar 4 measures the model before the human. What reaches the letter depends on a tired paralegal clicking through a third of the items. The failure the persona fears most, the letter saying something its own Source line does not, is one click away and leaves no trace for the attorney.",
90:  {"severity": "major", "title": "The ship bar's 1.000 flag numbers do not generalize: at d0b04bc the library shows 34/42 must-flags; the committed library and latest.json reports are stale",
91:   "evidence": "library-d0b04bc.md (regenerated at d0b04bc): must flags 1/3 lib08, 1/2 lib09, 0/1 lib10, 1/3 lib13, 1/3 lib15, 34/42 = 0.81 overall. lib_missed.py: missed conflicts 'Denies LOC per patient' vs 'brief loss of consciousness at the second collision', 'Left shoulder pain' vs 'Right shoulder pain', 'denies back pain' vs 'Low back pain 8/10'; lib10 G1 49-day gap reported as 'Gap of 43 days' from a CMS-1500. The committed evals/reports/library-latest.md is from a74b727 (231 commits back) and shows must_not hits that no longer reproduce. The committed evals/reports/latest.json reads ship_bar_met False (fixture, 14:39Z).",
---
---
39:| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified en
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spani
67:| D-059 | The letter total is built only from charges a human accepted one at a time (2026-11-02, T-140 adjuster fail). (1) Charges are never batch-accepted. (2) Code marks an amount `unclear` (not totaled, listed in internal notes with its reason) when its line or column label says total/subtotal/balance/balance forward/previous statement/year-to-date/amount due/paid/payment/adjustment/write-o
70:| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the total. Charge sources are positively identified: only documents with a
71:| D-063 | Priority switch (Chris, 2026-11-02): finish a polished MVP. Only P0 cards and UX/UI work proceed; every other non-P0 card is held (blocked with a note) until the MVP is done. In-flight P1 cards finish their current round but get no further rounds unless they block the UI. New review rounds on held areas are not opened; residuals go to SCOPE_CUTS. The M2 re-gate runs as soon as the P0 
72:| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item 
74:| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the 
75:| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, 
76:| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; revie
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:05.479Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>/dev/null | grep -E 'T-17[79]|T-181|T-18[89]|T-19[0-9]'; git grep -n -iE 'COMPARE_REQUIRED|D-066' HEAD -- app/backend | head -5; git ls-tree -r --name-only HEAD app/frontend/guided | head",
 "description": "Check status of dependent cards and committed code"
}
````

### User / tool · 2026-11-02T21:30:05.679Z

**tool result**
````
T-177	M3	backend    	in_progress      	P0	AC 1/1	GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels
T-179	M3	frontend   	in_progress      	P0	AC 0/1	GATE-M3 UI round: D-066 compare-confirm to accept a judge-disputed item (backend enforces 422 without it; batch excludes); D-067 hide the drafted treatment paragraph; UX/a11y minors (h1 on case page, Undo row hidden under sticky header, Try again focus, dismiss announcement overwritten, refused-edit names the words to keep, 320px Theme/Shortcuts/Export)
T-181	M3	frontend   	in_progress      	P0	AC 0/1	Build the guided UI (D-068) on the existing API: new shell at /, old screen at /classic; Your cases, 4 fixed steps, one-item review queue, bills, letter; guided e2e suite
T-188	M5	writer     	ready            	P0	AC 0/1	M5 package: submission/SUBMISSION_CHECKLIST.md mirroring Appendix A with links; submission/email-draft.md; final prioritized submission/NEEDS_CHRIS.md; PDF exports via pandoc (else HTML)
T-189	M5	orchestrator	needs_chris      	P0	AC 0/1	Chris: write the one story of a miss for Part 2 (submission/part2-process.md, last section, marked [CHRIS: ...] block)
T-190	M5	orchestrator	needs_chris      	P1	AC 0/1	Chris: fill the [CHRIS: ...] placeholders in the product note and Part 2 (full name, public link, optional real examples)
T-191	M5	writer     	needs_chris      	P2	AC 0/1	Chris: stretch-item reasons in the product note (NEEDS_CHRIS #8)
T-192	M5	writer     	needs_chris      	P2	AC 0/1	Chris: area 6 engineering stance in Part 2 (NEEDS_CHRIS #9)
app/frontend/guided/app.js
app/frontend/guided/core.js
app/frontend/guided/home.css
app/frontend/guided/home.js
app/frontend/guided/index.html
app/frontend/guided/review.css
app/frontend/guided/review.js
app/frontend/guided/step1.css
app/frontend/guided/step1.js
app/frontend/guided/step2.css
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:09.548Z

**tool call — Bash**
````
{
 "command": "git log --oneline --grep='T-177' | head; git log --oneline --grep='T-179' | head -3; python3 tools/board.py show T-177 | grep -E 'verdict|review ' | tail -4 | cut -c1-300",
 "description": "Check T-177 and T-179 commit history"
}
````

### User / tool · 2026-11-02T21:30:09.733Z

**tool result**
````
2e58e18 fix(backend): T-177 r3 every backend sentence for a prepared item says prepared answer (flag steps and why, failed and missing curated answers, run messages); /classic redirects to the guided UI in demo and public mode
f3d42a2 feat(frontend): T-181 guided UI scaffold (D-068): / is the guided app, old screen at /classic
d07bf9d docs(orchestrator): D-065 tooltip wording (T-177 r2)
4fcf9cd fix(frontend): T-177 r2 honest provenance on every surface: prepared items name no drafting model (judge panel, models in health/case/judges/export, case trace, tooltip, banner, audit and ladder rows)
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
04ea2bf feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
- 2026-11-02T20:33:30Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T20:38:36Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-177-staff-engineer.md; round 1; findings:
- 2026-11-02T21:04:53Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T21:15:23Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-177-staff-engineer-r2.md; round 2; findings:
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:15.424Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/validation-ladder.svg | grep -oE '>[^<>]+<' | sed 's/^>//; s/<$//' | grep -v '^\\s*$'",
 "description": "Extract SVG text at HEAD"
}
````

### User / tool · 2026-11-02T21:30:15.476Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to [^<>]+<)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:17.175Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/validation-ladder.svg | grep -n '<text' | sed -E 's/<[^>]*>//g' | sed -E 's/^ +//'",
 "description": "Extract SVG text lines at HEAD"
}
````

### User / tool · 2026-11-02T21:30:17.235Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to ]*>//g)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:18.569Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/validation-ladder.svg | grep -n 'text' | cut -c1-260",
 "description": "Show SVG text lines at HEAD"
}
````

### User / tool · 2026-11-02T21:30:18.670Z

**tool result**
````
3:  <desc id="d">A record's text goes to a model that drafts a summary and quote. Rung 1, code, checks the quote word for word and every number. Rung 2, a second model with a different prompt, answers a fixed choice. Code computes the state. Rung 3, the parale
10:  <text x="20" y="26" font-size="13" font-weight="700" fill="#111">Language work: model drafts, then three checks</text>
11:  <text x="560" y="26" font-size="13" font-weight="700" fill="#111">Single right answer: code only</text>
15:  <text x="34" y="60" font-size="12.5" font-weight="700" fill="#111">Record text</text>
16:  <text x="34" y="76" font-size="11.5" fill="#333">Untrusted data. Never treated as instructions. Models run with no tools.</text>
22:  <text x="34" y="126" font-size="12.5" font-weight="700" fill="#0b3a8c">AI draft (generator model)</text>
23:  <text x="34" y="143" font-size="11.5" fill="#222">One-line summary + exact quote; flag category + quote.</text>
24:  <text x="34" y="158" font-size="11.5" fill="#222">Never supplies a date, an amount, or the wording of a warning.</text>
30:  <text x="34" y="210" font-size="12.5" font-weight="700" fill="#14572b">Rung 1: code check</text>
31:  <text x="34" y="227" font-size="11.5" fill="#222">Quote is in the record word for word (whole sentences).</text>
32:  <text x="34" y="242" font-size="11.5" fill="#222">Every number, date, $ figure, left/right, no/not/without is in the quote.</text>
33:  <text x="34" y="257" font-size="11.5" fill="#222">Hedges in the quote ("may represent", "approx.") are kept in the summary.</text>
34:  <text x="34" y="270" font-size="11.5" fill="#222">Clauses the quote does not support are removed by code, and shown.</text>
40:  <text x="34" y="318" font-size="12.5" font-weight="700" fill="#7a4d00">Rung 2: independent second model (judge)</text>
41:  <text x="34" y="335" font-size="11.5" fill="#222">Different prompt and model. Sees only the record and the candidate.</text>
42:  <text x="34" y="350" font-size="11.5" fill="#222">Answers with a fixed choice and a reason code, never prose.</text>
43:  <text x="34" y="363" font-size="11.5" fill="#222">Disagree, unsure or no answer: the item is marked needs review.</text>
49:  <text x="34" y="407" font-size="12.5" font-weight="700" fill="#111">State, computed by code</text>
50:  <text x="34" y="422" font-size="11.5" fill="#333">verified or needs review. Needs review sorts first. Verified is not accepted.</text>
56:  <text x="34" y="472" font-size="12.5" font-weight="700" fill="#5a1f69">Rung 3: the paralegal decides</text>
57:  <text x="34" y="489" font-size="11.5" fill="#222">Accept, edit or dismiss, one item at a time, quote beside the line.</text>
58:  <text x="34" y="504" font-size="11.5" fill="#222">In progress (D-066, T-179): a summary the judge disputed</text>
59:  <text x="34" y="518" font-size="11.5" fill="#222">will need a named "I compared it with the quote."</text>
65:  <text x="34" y="555" font-size="12.5" font-weight="700" fill="#fff">Export, assembled by code from accepted items only</text>
66:  <text x="34" y="572" font-size="11.5" fill="#ddd">Letter: quotes + charges. Internal notes (do not send): flags, unclear amounts.</text>
71:  <text x="554" y="282" font-size="12" font-weight="700" fill="#8c1d18">Could not verify (visible list)</text>
72:  <text x="554" y="298" font-size="11" fill="#222">Quote not in the record, or a number</text>
73:  <text x="554" y="312" font-size="11" fill="#222">the quote lacks. Never a flag, never in</text>
74:  <text x="554" y="326" font-size="11" fill="#222">the letter. She can write the entry herself.</text>
78:  <text x="554" y="60" font-size="12" font-weight="700" fill="#111">Code, no model</text>
79:  <text x="554" y="78" font-size="11" fill="#222">Split records (a model may only point at</text>
80:  <text x="554" y="92" font-size="11" fill="#222">cut offsets for an unsplittable paste;</text>
81:  <text x="554" y="106" font-size="11" fill="#222">code validates). Parse dates (an ambiguous</text>
82:  <text x="554" y="120" font-size="11" fill="#222">date waits for her). Gap arithmetic: 29 and</text>
83:  <text x="554" y="134" font-size="11" fill="#222">30 days no, 31 yes; 28 no, 73 yes.</text>
84:  <text x="554" y="152" font-size="11" fill="#222">Find every dollar amount and its class (a</text>
85:  <text x="554" y="166" font-size="11" fill="#222">rate is never a charge). Totals of what she</text>
86:  <text x="554" y="180" font-size="11" fill="#222">accepted. Flag wording from templates.</text>
87:  <text x="554" y="198" font-size="11" fill="#222">Dates and amounts always need her accept.</text>
88:  <text x="554" y="212" font-size="11" fill="#222">Conflict pairs come from code; the judge</text>
89:  <text x="554" y="226" font-size="11" fill="#222">says only conflict or benign.</text>
93:  <text x="554" y="378" font-size="12" font-weight="700" fill="#111">Measured (live run, 3 runs)</text>
94:  <text x="554" y="396" font-size="11" fill="#222">Rung 1: grounding 1.000, 242 checked</text>
95:  <text x="554" y="412" font-size="11" fill="#222">Rung 2: seeded wrong summaries caught</text>
96:  <text x="554" y="426" font-size="11" fill="#222">40/40; correct ones rejected 0 of 10</text>
97:  <text x="554" y="442" font-size="11" fill="#222">Conflict judge 20/20, flag judge 12/12,</text>
98:  <text x="554" y="456" font-size="11" fill="#222">0 false agrees</text>
99:  <text x="554" y="474" font-size="11" fill="#222">Rung 3: persona 4 of 5 on the old screen,</text>
100:  <text x="554" y="488" font-size="11" fill="#222">which I found very hard to use; rebuilt as</text>
101:  <text x="554" y="502" font-size="11" fill="#222">four steps (D-068), not yet scored. 5 of 5</text>
102:  <text x="554" y="516" font-size="11" fill="#222">disputed summaries took one click (T-179)</text>
103:  <text x="554" y="536" font-size="10" fill="#555">Sources: evals/reports/20261102T164038Z.md;</text>
104:  <text x="554" y="549" font-size="10" fill="#555">submission/prompt-log/reviews/GATE-M3-</text>
105:  <text x="554" y="562" font-size="10" fill="#555">paralegal.md, GATE-M3-product-manager.md;</text>
106:  <text x="554" y="575" font-size="10" fill="#555">docs/LLM_VS_CODE.md</text>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:22.978Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/NEEDS_CHRIS.md | grep -nE '^\\| *[0-9]+ ' | cut -c1-420; git grep -n -i 'outsystems' HEAD -- docs/CONTRACT.md board/inbox memory/ submission/NEEDS_CHRIS.md spec/ | head -5",
 "description": "Check NEEDS_CHRIS rows and OutSystems source"
}
````

### User / tool · 2026-11-02T21:30:23.096Z

**tool result**
````
8:| 1 | P1 | T-019 | Real Anthropic API key for the public deployment | Put a real key in `.env` as `ANTHROPIC_API_KEY=<redacted> (local) and as the Space secret `ANTHROPIC_API_KEY` (Hugging Face). Only needed if you answer "live" to #2. | Run dev on the `claude-cli` backend (your claude.ai login); public build runs cached demo. |
9:| 2 | P1 | T-022 | Public link: demo-only or live? | Inbox: `demo-only` or `live, cap $N/day`. | Demo-only (cached sample run through the real pipeline code). Live needs an env opt-in (D-008). |
10:| 3 | P2 | T-023 | Live-model eval budget on your claude.ai plan (~25–35 calls per sample run) | Inbox: `ok` or a cap, e.g. `max 300 calls`. | Live runs only for ship-bar measurements (3× sample, golden set, the seeded-hallucination set (currently 40 items)); fixtures otherwise. |
18:| 4 | P0 | T-189 | **The one story: a feature or launch you owned that missed the mark.** Yours alone; the team will not write it. | Replace the `[CHRIS: write this yourself ...]` block at the end of `submission/part2-process.md` ("The one story: a miss") with about 200 words: (1) what you shipped and expected, (2) what you missed and the number or signal that showed it, (3) one concrete process change (an artifac
19:| 5 | P1 | T-190 | Byline and public link for the product note and Part 2 | In `submission/product-note.md` line 3 and `submission/part2-process.md` line 3: replace `[CHRIS: full name]` with the name as it should appear; in the product note replace `[CHRIS: public link, ...]` with the Hugging Face Space URL once it exists (see #2). | Placeholders stay visible, so nothing is sent with a made-up name or link. |
20:| 6 | P2 | T-190 | Optional one-line real examples in Part 2 (each is marked `[CHRIS: optional ...]`) | Area 1: watching real work without exposing client data. Area 5: how you measured adoption on the OutSystems AI Agent Builder. Area 7: a time you got honest feedback from users who said little. Area 8: supervising developers on a late feature. Add one or two sentences each, or delete the marker. | Part 2 reads c
21:| 7 | P2 | T-190 | Product note, ship-bar row 5: the 4/5 "I could verify every claim quickly" is a persona reviewer on the old screen, not a real paralegal; you rejected that screen as very hard to use (D-068) | Optional: have a real paralegal (or someone who does this work) run the sample case on the guided screen once it ships and tell you the score; replace the row 5 result and the "Reviewability passed on pape
22:| 8 | P1 | (card pending) | Product note, Cut paragraph: why you reinstated cuts (D-031, D-042) and shipped three stretch items when the brief says at most one | Replace `[CHRIS: your reason, one line.]` with your reason in your words. | The note records the decisions and their cost (drafted paragraph cut, four billing rounds) and leaves the reason marked. |
23:| 9 | P2 | (card pending) | Part 2, area 6: the decision rights you give engineering | Confirm or change the "Engineering" paragraph (engineering decides how and has a "not safe to ship" veto; only a founder overrides it in writing; evidence first, then the safer answer for anything the carrier sees). | The paragraph stands as my stated stance. |
HEAD:docs/CONTRACT.md:601:- Owned OutSystems' first Generative AI portfolio, including an AI Agent Builder with LLM/RAG integration; that work reached ~80% adoption and significant ARR. Product-strategy work at Zuora on AI product strategy. Internal platform/applied-AI product work at <outside project> (<outside project>). Earlier PM roles at Mouseflow, <redacted-private> (sole PM, 0-to-1), nDivision, cPanel, and HostGator.
HEAD:submission/NEEDS_CHRIS.md:20:| 6 | P2 | T-190 | Optional one-line real examples in Part 2 (each is marked `[CHRIS: optional ...]`) | Area 1: watching real work without exposing client data. Area 5: how you measured adoption on the OutSystems AI Agent Builder. Area 7: a time you got honest feedback from users who said little. Area 8: supervising developers on a late feature. Add one or two sentences each, or delete the marker. | Part 2 reads complete without them; the markers are the only gaps. |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:27.940Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- submission/NEEDS_CHRIS.md | grep -E '^[-+]\\| *[89] ' | cut -c1-120; git diff HEAD --stat -- submission/",
 "description": "Compare working-tree NEEDS_CHRIS rows 8-9"
}
````

### User / tool · 2026-11-02T21:30:28.099Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:29.378Z

**tool call — Bash**
````
{
 "command": "git status --short submission/ | head; git diff --cached --stat -- submission/ | tail -3",
 "description": "Check staged vs unstaged submission changes"
}
````

### User / tool · 2026-11-02T21:30:29.497Z

**tool result**
````
MM submission/NEEDS_CHRIS.md
MM submission/part2-process.md
MM submission/product-note.md
MM submission/validation-ladder.svg
 submission/product-note.md       | 47 ++++++++++++++++++++--------------------
 submission/validation-ladder.svg | 47 +++++++++++++++++++---------------------
 4 files changed, 56 insertions(+), 64 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:34.030Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-185-pm/r2 && for f in product-note.md part2-process.md validation-ladder.svg print.css; do git show HEAD:submission/$f > artifacts/review-evidence/T-185-pm/r2/$f; done; ls artifacts/review-evidence/T-185-pm/r2; which pandoc; ls \"/Applications/Google Chrome.app/Contents/MacOS/\" 2>/dev/null; git show HEAD:.claude/agent-memory/writer/submission_pipeline.md | head -12",
 "description": "Extract HEAD docs for rendering"
}
````

### User / tool · 2026-11-02T21:30:34.204Z

**tool result**
````
part2-process.md
print.css
product-note.md
validation-ladder.svg
/opt/homebrew/bin/pandoc
Google Chrome
---
name: submission-pipeline
description: How the product note and Part 2 doc were built and page-fitted, where each number comes from, and pitfalls
metadata:
  type: project
---

Submission docs live in `submission/`: `product-note.md` (1 page), `part2-process.md` (4 pages), `validation-ladder.svg` (hand-written; `mmdc` is not installed), `print.css` (shared print style).

**Page-fit check (no LaTeX here):** `pandoc X.md -s -o /private/tmp/.../x.html --css submission/print.css --embed-resources --resource-path=submission`, then Chrome headless `--print-to-pdf --no-pdf-header-footer`, count `/Type /Page` in the PDF. Product note fits one page only at 8.7pt (~1000 words); Part 2 fits 4 pages at 9.4pt (~2700 words). T-188 does the real PDFs; reuse print.css.

**Round 2 (after PM review fail):** render with a scratch copy of print.css plus `body{font-size:Npt}` (script pattern: pandoc --css <copy> then Chrome). Product note needed ~1050 words at 8.7pt; table column widths (dash counts) and orphan last lines matter more than words. Cite only paths `git ls-files` knows: reviews are tracked at `submission/prompt-log/reviews/`, not `reviews/`. Run a backtick-path existence check before handoff. Unit count: `git archive HEAD` into scratch, symlink `.venv`, pytest (about 6 min), save under `artifacts/unit-count-<sha>.txt`; a count is valid only for its commit. Library recall: committed `evals/reports/library-latest.md` (a74b727) gives entries 0.775, amounts 0.681, flags 0.81; the PM reviewer's d0b04bc run (untracked evidence) gave amounts 0.580 — flag the mismatch, don't pick silently. Never present T-181/T-179 as built until committed.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:38.508Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/r2 && grep -n 'font-size\\|@page' print.css | head; for d in product-note part2-process; do pandoc $d.md -s -o $d.html --css print.css --embed-resources --resource-path=. --metadata title=\" \" 2>&1 | tail -2; \"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=$PWD/$d.pdf file://$PWD/$d.html 2>/dev/null; echo \"$d pages: $(grep -c '/Type /Page$\\|/Type /Page[^s]' $d.pdf)\"; done",
 "description": "Render HEAD docs with committed print.css and count pages"
}
````

### User / tool · 2026-11-02T21:30:40.493Z

**tool result**
````
1:@page{size:Letter;margin:0.4in}
4:h1{font-size:13pt;margin:0 0 2px}
7:table{border-collapse:collapse;width:100%;margin:3px 0;font-size:8.2pt}
9:code{font-size:7.8pt}
product-note pages: 
part2-process pages:
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:42.731Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/r2 && ls -la; cat print.css | head -5 | cut -c1-200; for d in product-note part2-process; do python3 -I -c 'import sys,re;d=open(sys.argv[1],\"rb\").read();print(sys.argv[1], len(re.findall(rb\"/Type\\s*/Page[^s]\",d)))' $d.pdf; done",
 "description": "Count PDF pages for rendered docs"
}
````

### User / tool · 2026-11-02T21:30:42.860Z

**tool result**
````
total 872
drwxr-xr-x@ 10 arsis  staff     320 Nov  2 15:30 .
drwxr-xr-x@ 13 arsis  staff     416 Nov  2 15:30 ..
-rw-r--r--@  1 arsis  staff   33940 Nov  2 15:30 part2-process.html
-rw-r--r--@  1 arsis  staff   18175 Nov  2 15:30 part2-process.md
-rw-r--r--@  1 arsis  staff  235530 Nov  2 15:30 part2-process.pdf
-rw-r--r--@  1 arsis  staff     433 Nov  2 15:30 print.css
-rw-r--r--@  1 arsis  staff    9101 Nov  2 15:30 product-note.html
-rw-r--r--@  1 arsis  staff    6680 Nov  2 15:30 product-note.md
-rw-r--r--@  1 arsis  staff  112493 Nov  2 15:30 product-note.pdf
-rw-r--r--@  1 arsis  staff    8687 Nov  2 15:30 validation-ladder.svg
@page{size:Letter;margin:0.4in}
body{font:8.7pt/1.25 -apple-system,Helvetica,Arial,sans-serif;max-width:none;margin:0;color:#111}
header{display:none}
h1{font-size:13pt;margin:0 0 2px}
p{margin:2px 0}li{margin:0.5px 0}
product-note.pdf 1
part2-process.pdf 4
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:44.758Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/r2/product-note.pdf"
}
````

### User / tool · 2026-11-02T21:30:44.793Z

**tool result**
````
PDF file read: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/r2/product-note.pdf (109.9KB)
[document]
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:52.168Z

**tool call — Bash**
````
{
 "command": "git log --oneline 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml | head; .venv/bin/python -m evals.run --check-fresh >/dev/null 2>&1; echo check-fresh exit=$?; git show HEAD:evals/reports/20261102T164038Z.md | grep -n -iE 'held-out|5 of 17|clean|generator|judge model|runs' | head -8; for c in $(git log --format=%h -S'D-059' -- memory/ORCHESTRATOR_DECISIONS.md | tail -1); do echo D-059 first commit $c; git merge-base --is-ancestor a74b727 $c && echo \"a74b727 precedes D-059\"; done; python3 tools/board.py list 2>/dev/null | grep -iE 'library' | cut -c1-200",
 "description": "Check eval freshness, held-out claim, library regen card"
}
````

### User / tool · 2026-11-02T21:30:52.440Z

**tool result**
````
check-fresh exit=0
3:**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
4:Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.
19:| J3 judge_conflict_v6 seeded catch rate | 1.000 (20/20 wrong caught x3 runs; in-sample 14/14; held-out 6/6; false agree 0 []; correct accepted 21/21; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
20:| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
42:In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says whether it is still held out. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).
70:| H3V2 | j3 | held-out | correct | plan_vs_outcome:Twelve visits authorized. | variant | conflict | conflict / conflict / conflict | yes |
71:| H3V4 | j3 | held-out | correct | plan_vs_outcome:PT x 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
72:| H3V5 | j3 | held-out | correct | plan_vs_outcome:Chiropractic 3x/week for 4 weeks. | variant | conflict | conflict / conflict / conflict | yes |
D-059 first commit 07c7558
a74b727 precedes D-059
T-052	M3	researcher 	done             	P2	AC 3/3	Research: synthetic multi-case library grounded in real PI use cases
T-053	M3	backend    	done             	P2	AC 3/3	Multi-case: case list + switcher (local/dev mode only), library loader
T-077	M3	researcher 	done             	P1	AC 2/2	Research: real-world PI case patterns for the multi-case library (v2)
T-079	M3	qa         	done             	P1	AC 2/2	Build library packets lib08..lib15 from the v2 research (synthetic, with expected.json)
T-129	M3	backend    	done             	P2	AC 1/1	Ingest: a non-library preamble counts as a phantom record 1
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:30:58.135Z

**tool call — Bash**
````
{
 "command": "git show HEAD:evals/reports/20261102T164038Z.md | grep -n -iE '17|still held|clean' | head -8",
 "description": "Verify 5 of 17 held-out claim"
}
````

### User / tool · 2026-11-02T21:30:58.232Z

**tool result**
````
4:Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.
42:In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says whether it is still held out. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).
69:| J3V17 | j3 | in-sample | wrong | history_denial:Patient denies any prior neck injury. | variant | benign | benign / benign / benign | yes |
74:| H3V17 | j3 | held-out | wrong | plan_vs_outcome:Ten visits of PT were authorized. | variant | benign | benign / benign / benign | yes |
115:Held-out status is derived from git (evals/heldout_audit.py), not from the label. Clean held-out J3 controls: 5 of 17 ['H3V17', 'H3V18', 'H3V19', 'H3V20', 'H3V21']. A control is clean when it was written apart from the prompt, none of its words is in the current prompt, and no prompt version was added after its first run.
116:Not clean: H3V2 seen_before_edit; H3V4 seen_before_edit; H3V5 seen_before_edit; H3V6 seen_before_edit; H3V8 seen_before_edit; H3V9 seen_before_edit; H3V10 seen_before_edit; H3V11 seen_before_edit; H3V12 seen_before_edit; H3V13 seen_before_edit; H3V14 seen_before_edit; H3V15 seen_before_edit. These are still reported as held-out rows above because they were authored separately; read them as seen.
136:- `app/llm/prompts/extract_v1.md` 11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2
149:- `app/llm/prompts/narrative_v1.md` 3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:31:06.465Z

**tool call — Bash**
````
{
 "command": "curl -s -m 5 http://localhost:7860/ | grep -oE '<title>[^<]*|guided/[a-z0-9]+\\.(js|css)' | head -5; curl -s -m 5 -o /dev/null -w 'classic %{http_code} %{redirect_url}\\n' http://localhost:7860/classic; curl -s -m 5 http://localhost:7860/api/health | head -c 300; echo; git show HEAD:app/frontend/guided/review.js | grep -n -iE 'accept|dismiss|edit' | head -5",
 "description": "Check what the running app serves at / and /classic"
}
````

### User / tool · 2026-11-02T21:31:06.524Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to [^<]*|guided/[a-z0-9]+\.(js|css))
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:31:08.998Z

**tool call — Bash**
````
{
 "command": "curl -s -m 5 http://localhost:7860/ | grep -oE 'title.{0,60}|guided/[a-z0-9]+[.](js|css)' | head -5; curl -s -m 5 -o /dev/null -w 'classic %{http_code} %{redirect_url}\\n' http://localhost:7860/classic; curl -s -m 5 http://localhost:7860/api/health | head -c 300; echo; git show HEAD:app/frontend/guided/review.js | grep -n -iE 'accept|dismiss' | head -5",
 "description": "Check what the running app serves at root and classic"
}
````

### User / tool · 2026-11-02T21:31:09.163Z

**tool result**
````
title>Treatment timeline</title>
title">
title">Source record</h2><button type="button" id="source-close" 
title">
title">Why?</h2><button type="button" class="btn btn--sm" data-te
classic 404 
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:31:12.311Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/frontend/guided/review.js | wc -l; git grep -n -iE \"'/api/[a-z/]*(review|accept|decision)\" HEAD -- app/frontend/guided | head -5; git show HEAD:app/backend/server.py 2>/dev/null | grep -n -iE 'classic|guided' | head -8",
 "description": "Check guided UI scaffold review capability at HEAD"
}
````

### User / tool · 2026-11-02T21:31:12.458Z

**tool result**
````
       5
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:31:14.318Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/frontend/guided/review.js; git grep -n -iE 'classic' HEAD -- 'app/backend/*.py' | head -6; git grep -l -iE 'accept' HEAD -- app/frontend/guided | head",
 "description": "Inspect guided review stub and classic routing"
}
````

### User / tool · 2026-11-02T21:31:14.454Z

**tool result**
````
/* Shared helpers for the two review pages (step 2 timeline, step 3 bills): the frame builder, the action bar and the layout-stability helpers. OWNER: the Step 2 + Step 3 builder.
   Empty on purpose (T-181 scaffold). Keep it free of step-specific rules; step2.js and step3.js call into it. Spec 2.5-2.7. */
(function () {
  const G = window.G; G.review = G.review || {};
})();
HEAD:app/backend/api.py:682:        if (guided / "index.html").is_file():                                           # D-068: the guided app is the front door; the old screen stays reachable at /classic
HEAD:app/backend/api.py:687:                /api and /classic never fall through to it (an unknown /api path must stay a JSON 404)."""
HEAD:app/backend/api.py:692:                        if e.status_code != 404 or path.startswith(("api/", "classic/")) or path in ("api", "classic") or "." in path.rsplit("/", 1)[-1]:
HEAD:app/backend/api.py:695:                    if resp.status_code == 404 and not path.startswith(("api/", "classic/")) and "." not in path.rsplit("/", 1)[-1]:
HEAD:app/backend/api.py:699:            def classic_open():
HEAD:app/backend/api.py:700:                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
HEAD:app/frontend/guided/step3.js
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:31:21.922Z

**tool call — Bash**
````
{
 "command": "for f in step1 step2 step3 step4 home app core; do printf \"%s \" $f; git show HEAD:app/frontend/guided/$f.js 2>/dev/null | wc -l; done; git show HEAD:app/frontend/guided/step2.js | head -4; git show HEAD:app/backend/api.py | sed -n 699,712p",
 "description": "Gauge guided scaffold completeness at HEAD"
}
````

### User / tool · 2026-11-02T21:31:22.160Z

**tool result**
````
step1       10
step2       12
step3       11
step4        9
home       14
app      166
core      138
/* Step 2: Check the timeline (/case/<token>/timeline[?item=<id>]). PLACEHOLDER from the T-181 scaffold: it only draws the empty frame so the layout can be tested.
   OWNER: the Step 2 + Step 3 builder; replace the body, keep the registration. Spec section 5. Frame layout: .titlebar, .work (two .card), .actions as children of ctx.view.
   The done screen switches to the single-panel layout with ctx.layout("page"). Use ctx.case (loaded by the shell), ctx.refresh() after every write, G.steps.counts(ctx.case). */
(function () {
            def classic_open():
                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
                return local_mode() or os.environ.get("ZLAYT_CLASSIC") == "1"

            class ClassicFiles(StaticFiles):
                async def get_response(self, path, scope):
                    if not classic_open():
                        return RedirectResponse("/")
                    return await super().get_response(path, scope)

            app.add_api_route("/classic", lambda: RedirectResponse("/classic/" if classic_open() else "/"), include_in_schema=False)       # the mount only answers /classic/ ; /classic would fall to the guided mount
            app.mount("/classic", ClassicFiles(directory=str(sd), html=True), name="classic")
            app.mount("/", GuidedFiles(directory=str(guided), html=True), name="frontend")
        else:
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:32:34.223Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-185-product-manager-r2.md",
 "content": "# T-185 product note, round 2: product-manager-reviewer (Dana Okafor lens)\n\n**Verdict: changes** (0 blockers, 1 major, 3 minors, 2 nits).\n\nGraded at `git show HEAD:submission/product-note.md`. HEAD is 2e58e18, and the note is byte-identical to ddfbf6d (`git diff ddfbf6d HEAD --stat -- submission/` is empty). The working tree is not graded.\n\n**Round-1 findings: 9 of 10 closed.**\n- **Both blockers are fixed.**\n  - Row 5 now reads \"Not met on the screen I rejected\".\n  - The first \"What testing found\" bullet tells the D-068 story plainly.\n  - T-181 and T-179 are marked \"In progress, not yet in the app\".\n  - The failure table says D-066 \"will need ... (in progress)\".\n- **Unit count is fixed.** 5,795 at 33e88c6 is in the HEAD tree (`artifacts/unit-count-33e88c6.txt`).\n- **Stretch is fixed.** The note names all three items, gives the D-042 reason (verified verbatim against the decision) and states the cost.\n- **Every cited path exists in HEAD** (script output below).\n- **All three minors and the nit are fixed:** the $10,906 claim is dropped, the LLM_SPLIT fallback is listed, the metrics name their sources, and \"Score 5\" is gone.\n\n**Still open (major).** Library recall in row 2 is partly fixed. Entries 0.775 and amounts 0.681 match the committed `evals/reports/library-latest.md` (93/120, 47/69, 34/42). But the row adds \"(0.580 on a later run; report being regenerated)\". 0.580 is in no committed report, and no card regenerates the report.\n\n**Placeholders (brief item 2): acceptable, not a defect.**\n- D-031 and D-042 are Chris's own calls (decision log: \"Chris, inbox 02:05Z\" and \"Chris, chat\"), so his motive is a fact only he has. The note already states what was decided and what it cost, so it reads complete without him. T-191 tracks the placeholder.\n- One flaw: NEEDS_CHRIS row 8 is P1 and says \"(card pending)\", while T-191 is P2.\n\nPage count: 1. Rendered from HEAD with the committed `submission/print.css` (8.7pt), output in `artifacts/review-evidence/T-185-pm/r2/product-note.pdf`.\n\n```json\n{\"card\": \"T-185\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"submission/product-note.md at HEAD 2e58e18 (identical to fix commit ddfbf6d); cited evidence at HEAD: evals/reports/library-latest.md, evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, artifacts/unit-count-33e88c6.txt, submission/prompt-log/reviews/{GATE-M3-paralegal,GATE-M3-product-manager,T-140-claims-adjuster}.md, memory/ORCHESTRATOR_DECISIONS.md, submission/NEEDS_CHRIS.md; app code at HEAD (app/backend/api.py, app/frontend/guided/); running app http://localhost:7860\",\n \"exercised\": [\n  \"Read personas/product-manager.md, my round-1 review reviews/T-185-product-manager.md, board.py show T-185/T-191/T-192, board.py list (T-177, T-179, T-181 in_progress; no library-regeneration card)\",\n  \"git log --oneline -8; git show --stat ddfbf6d; git diff ddfbf6d HEAD --stat -- submission/ -> empty (note unchanged since the fix commit)\",\n  \"git show HEAD:submission/product-note.md read end to end twice; rendered HEAD copy with committed print.css via pandoc + headless Chrome -> artifacts/review-evidence/T-185-pm/r2/product-note.pdf = 1 page\",\n  \"git show HEAD:evals/reports/library-latest.md -> python3 -I artifacts/review-evidence/T-185-pm/lib_sums_r2.py artifacts/review-evidence/T-185-pm/library-HEAD.md -> '15 packets', 'entries: 93/120 = 0.775', 'amounts: 47/69 = 0.681', 'must flags: 34/42 = 0.810'\",\n  \"git grep -n '0\\\\.580' HEAD -- evals/reports/ -> no match; only hits are the note itself, writer memory, the prompt-log copy of my r1 review and transcripts\",\n  \"python3 -I artifacts/review-evidence/T-185-pm/paths_in_head.py <repo> submission/product-note.md -> 11 of 11 backticked paths OK in HEAD tree\",\n  \"git ls-tree HEAD artifacts/unit-count-33e88c6.txt -> blob b7958bd; file tail '5795 passed, 8 skipped in 356.75s'; git status --short on it -> 'D ' staged and '??' (staged deletion in the shared index)\",\n  \"git show HEAD:evals/reports/m3-sensors.md:7-8 -> E2E '412 passed' at d7ea327 (matches note)\",\n  \"git show HEAD:evals/reports/20261102T164038Z.md -> models generator claude-sonnet-5-5 / judge claude-haiku-5-5; 'Clean held-out J3 controls: 5 of 17' (:115); J3 20/20, J4 12/12\",\n  \".venv/bin/python -m evals.run --check-fresh -> exit=0; git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml -> empty\",\n  \"git show HEAD:submission/prompt-log/reviews/T-140-claims-adjuster.md:10 -> '$16,147.00 ... The records state $8,123.50'; GATE-M3-product-manager.md:46 -> 'Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click'\",\n  \"memory/ORCHESTRATOR_DECISIONS.md at HEAD: D-031 'Scope reinstated (Chris, inbox 02:05Z)', D-042 'Second scope reinstatement (Chris, chat) ... every remaining cut that needs neither a paid third-party integration nor auth/multi-user'; D-059 first commit 07c7558, git merge-base --is-ancestor a74b727 07c7558 -> true ('before the billing redesign' holds)\",\n  \"git show HEAD:submission/NEEDS_CHRIS.md rows 8-9 vs board.py show T-191 (P2) / T-192 (P2)\",\n  \"git show HEAD:app/backend/api.py:699-712 and HEAD:app/frontend/guided/{review,step2}.js; curl http://localhost:7860/ (old UI, older server), /classic -> 404, /api/health -> demo_mode true\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"accuracy\": 4, \"no_invented_chris_facts\": 5, \"required_contents\": 5, \"honesty_of_misses\": 5, \"voice\": 4, \"length\": 5},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Row 2 cites a library amount recall (0.580) that no committed report contains, plus a regeneration that no card owns\",\n   \"evidence\": \"HEAD:submission/product-note.md:16 '**Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; report being regenerated)'. lib_sums_r2.py on HEAD:evals/reports/library-latest.md -> 'amounts: 47/69 = 0.681'. git grep -n '0\\\\.580' HEAD -- evals/reports/ -> no match. The 0.580 came from my untracked r1 evidence (artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md; git ls-files --error-unmatch -> 'did not match any file(s) known to git'). board.py list | grep -i library -> only done cards (T-052, T-053, T-077, T-079, T-129); no open card regenerates library-latest.md. The orchestrator's T-185 note at 21:27:58Z: 'drop the 0.580 mention unless a committed report shows it.'\",\n   \"why_it_matters\": \"The brief and AC 1 require every number to trace to a committed report. A panelist who opens [L] finds 0.681 and no trace of 0.580. 'Report being regenerated' promises work that nobody is doing. The note's credibility rests on its numbers opening to their source.\",\n   \"fix\": \"Delete '(0.580 on a later run; report being regenerated)'. Or have qa regenerate evals/reports/library-latest.md at the submission commit under a card, commit it, and cite that single report's numbers.\",\n   \"acceptance_test\": \"Every library number in product-note.md row 2 equals a value computed from git show HEAD:evals/reports/library-latest.md, and the note contains no '0.580' unless that report shows it.\"},\n  {\"severity\": \"minor\", \"title\": \"'(same review)' points at the wrong source: the nearest citation is the T-140 adjuster review, but the 5 of 5 / 16 cases figure is from GATE-M3-product-manager\",\n   \"evidence\": \"HEAD:submission/product-note.md:25 cites 'submission/prompt-log/reviews/T-140-claims-adjuster.md'; :26 'One click accepted a disputed summary, 5 of 5 times in 16 cases (same review)'. The figure is at GATE-M3-product-manager.md:46 'Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click'. git show HEAD:submission/prompt-log/reviews/T-140-claims-adjuster.md | grep -E '5 of 5|16 cases' -> no match.\",\n   \"why_it_matters\": \"A panelist following 'same review' opens the billing review and does not find the number. It is a small break in traceability on the note's key honesty bullet.\",\n   \"fix\": \"Replace '(same review)' with '(`submission/prompt-log/reviews/GATE-M3-product-manager.md`)', or move the bullet next to the GATE-M3 citation.\",\n   \"acceptance_test\": \"The source named next to '5 of 5 times in 16 cases' contains that figure (grep).\"},\n  {\"severity\": \"minor\", \"title\": \"'Misses cluster in ledgers, EOBs, scans, Spanish' leaves out two of the four worst library packets\",\n   \"evidence\": \"HEAD:evals/reports/library-latest.md entries column: lib11 priors_and_ledger 4/9, lib15 conclusory_letter_mist 4/8, lib13 cloned_notes_cross_provider 5/9, lib09 spanish 4/7, lib10 eob 6/9, lib14 scans 6/8. The named categories (lib09, lib10, lib11, lib14) account for 13 of the 27 missed entries. The unnamed cloned-notes (lib13) and conclusory-letter (lib15) packets account for 8.\",\n   \"why_it_matters\": \"Error analysis is the point of the library run. Naming only the input-format causes (ledger, EOB, scan, language) hides the content-type misses (cloned notes, conclusory letters) that a paralegal would hit on ordinary records.\",\n   \"fix\": \"'Largest misses: ledgers, conclusory letters, cloned notes, Spanish, EOBs' (or list the packets by recall), still followed by 'real misses vs stale expected files not yet separated'.\",\n   \"acceptance_test\": \"Each packet with entry recall below 0.6 in library-latest.md falls in a category the row names.\"},\n  {\"severity\": \"minor\", \"title\": \"NEEDS_CHRIS row 8 (the stretch reason) is P1 and says '(card pending)', while its card T-191 exists at P2\",\n   \"evidence\": \"HEAD:submission/NEEDS_CHRIS.md:22 '| 8 | P1 | (card pending) | Product note, Cut paragraph: why you reinstated cuts ...'. board.py show T-191 -> 'priority: \\\"P2\\\"', title 'Chris: stretch-item reasons in the product note (NEEDS_CHRIS #8)'.\",\n   \"why_it_matters\": \"Chris works from the needs_chris column on his phone. If the row and the card disagree on priority, he may under-prioritize the one placeholder that sits in the note's graded 'cut scope on purpose' paragraph. A stale '(card pending)' also shows the parity check was not re-run.\",\n   \"fix\": \"Set row 8's card column to T-191 and make the priorities agree (P1 on both, since the placeholder is visible in the one-page note).\",\n   \"acceptance_test\": \"For every NEEDS_CHRIS row, the card column names an existing card with the same priority (board.py show).\"},\n  {\"severity\": \"nit\", \"title\": \"Outside the verdict per brief item 4, but a release risk: at HEAD the public/demo front door is the empty T-181 scaffold, so 'not yet in the app' is already untrue and 'What I built' is not reachable in demo mode\",\n   \"evidence\": \"HEAD:app/backend/api.py:700 'in demo or public mode it sends the visitor to the guided UI at /'; HEAD:app/frontend/guided/review.js 'Empty on purpose (T-181 scaffold)'; step2.js 'PLACEHOLDER from the T-181 scaffold: it only draws the empty frame'. product-note.md:7 'Each timeline entry shows the AI's summary beside the verbatim quote; she accepts, edits or dismisses it ... In progress, not yet in the app: a guided four-step screen'.\",\n   \"why_it_matters\": \"If the submission is tagged before T-181 is done, the panel's prototype link shows empty steps. The note would then describe a review screen they cannot reach.\",\n   \"fix\": \"Orchestrator: do not tag a submission commit while / serves the scaffold in demo mode. Refresh line 7 when T-181 lands, as already planned.\",\n   \"acceptance_test\": \"At the submission commit, in demo mode, every action in 'What I built' can be done from /.\"},\n  {\"severity\": \"nit\", \"title\": \"The cited unit-count file is staged for deletion in the shared index\",\n   \"evidence\": \"git status --short artifacts/unit-count-33e88c6.txt -> 'D ' plus '??'; git ls-files --error-unmatch -> not known; git ls-tree HEAD -> present (blob b7958bd).\",\n   \"why_it_matters\": \"A path-limited commit that sweeps this path would remove the note's test-count evidence from git.\",\n   \"fix\": \"Orchestrator: git restore --staged artifacts/unit-count-33e88c6.txt (non-destructive) before the next commit.\",\n   \"acceptance_test\": \"git ls-files --error-unmatch artifacts/unit-count-33e88c6.txt succeeds.\"}\n ],\n \"whats_right\": [\n  \"Row 5 'Not met on the screen I rejected' and the first testing bullet turn the D-068 human verdict into the note's clearest AI-judgment lesson. Keep that order.\",\n  \"Present tense is used only for what HEAD ships. T-181 and T-179 are labeled in progress in the build paragraph, the failure table and the M3 bullet.\",\n  \"Stretch paragraph names all three items, gives the verifiable D-042 rule, states the cost and leaves only Chris's motive as a tracked placeholder.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T21:32:34.365Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-185-product-manager-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:33:16.312Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-186-product-manager-r2.md",
 "content": "# T-186 Part 2 process doc + validation-ladder SVG, round 2: product-manager-reviewer (Dana Okafor lens)\n\n**Verdict: changes** (0 blockers, 1 major, 2 minors, 2 nits).\n\nI graded `git show HEAD:` for `submission/part2-process.md` and `submission/validation-ladder.svg`. HEAD is 2e58e18, and both files are byte-identical to ddfbf6d. I did not grade the working tree.\n\n**Round-1 findings: 6 of 7 closed.**\n- **Redesign blocker: fixed.** The area 4 table now reads \"persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored\" (:56), and a new paragraph follows it (:58). Area 7 uses the redesign as its honest-feedback example (:91). The SVG Rung 3 measured box says the same (svg:99-102).\n- **SVG D-066 blocker: fixed.** Rung 3 now reads \"In progress (D-066, T-179): a summary the judge disputed will need a named ...\" (svg:58-59).\n- **Unit count: fixed.** It now reads 5,795 at 33e88c6, and that file is in HEAD.\n- **Area 6 engineering: fixed.** Engineering decides how, holds a not-safe-to-ship veto, and disagreements go to evidence first (:83).\n- **SVG split fallback: fixed** (svg:79-81).\n- **Assumption marker and A-109: fixed** (:13, :23).\n- **Still open (major): counts.** Every cited path now exists in HEAD. But the doc says \"counts are at the commit this doc was last edited\", and three of the seven counts are not what that commit holds: 460 reviews (467 at HEAD), \"44 entries\" in LESSONS (28 at HEAD), and 62 debt rows (61 at HEAD). The 44 and 62 match the uncommitted working tree.\n\n**Placeholder for the area-6 stance (T-192): acceptable, not a defect.** The decision rights Chris would give engineering are his management stance, and the panel will question him on it. The team drafted a concrete default, labeled it as a stance pending a founder, and carded it, so the area reads complete either way. One flaw remains: the marker \"(NEEDS_CHRIS #9)\" sits in panel-facing text outside the `[CHRIS: ...]` form, so the pre-send scrub will not find it (minor).\n\nThe doc renders to 4 pages with the committed print.css (`artifacts/review-evidence/T-185-pm/r2/part2-process.pdf`).\n\n```json\n{\"card\": \"T-186\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"submission/part2-process.md and submission/validation-ladder.svg at HEAD 2e58e18 (identical to fix commit ddfbf6d); cited evidence at HEAD: memory/{LESSONS,SCOPE_CUTS,ORCHESTRATOR_DECISIONS,ASSUMPTIONS}.md, spec/REQUIREMENTS.md, personas/, evals/reports/, submission/prompt-log/reviews/, artifacts/unit-count-33e88c6.txt, evals/reports/m3-sensors.md, evals/reports/library-latest.md, submission/NEEDS_CHRIS.md\",\n \"exercised\": [\n  \"Read personas/product-manager.md, my round-1 review reviews/T-186-product-manager.md, board.py show T-186/T-191/T-192, board.py list (T-177, T-179, T-181 in_progress)\",\n  \"git show --stat ddfbf6d; git diff ddfbf6d HEAD --stat -- submission/ -> empty\",\n  \"git show HEAD:submission/part2-process.md read end to end; rendered with committed print.css via pandoc + headless Chrome -> artifacts/review-evidence/T-185-pm/r2/part2-process.pdf = 4 pages\",\n  \"git show HEAD:submission/validation-ladder.svg | grep -n text -> read every text line (rung 3 'In progress (D-066, T-179)', split fallback, measured box)\",\n  \"python3 -I artifacts/review-evidence/T-185-pm/paths_in_head.py <repo> submission/part2-process.md -> 21 of 21 backticked paths OK in HEAD tree\",\n  \"Counts at HEAD: git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | wc -l -> 467 (same at ddfbf6d); git ls-tree --name-only HEAD evals/reports/ | grep -cE '^evals/reports/[0-9]{8}T' -> 27; ORCHESTRATOR_DECISIONS unique D-IDs -> 68 (D-001..D-068); git show HEAD:memory/LESSONS.md | grep -cE '^- ' -> 28 (same at ddfbf6d); git show HEAD:memory/SCOPE_CUTS.md | grep -ciE '^\\\\| *debt' -> 61; personas/*.md -> 13; REQUIREMENTS row R-IDs -> 62; ASSUMPTIONS A-101..A-109\",\n  \"git diff --stat HEAD -- memory/LESSONS.md memory/SCOPE_CUTS.md -> 16 and 2 uncommitted insertions (source of 44 and 62)\",\n  \"python3 -I artifacts/review-evidence/T-185-pm/lib_sums_r2.py on HEAD library-latest.md -> entries 0.775, amounts 0.681, must flags 0.810 (matches :44 and :54)\",\n  \"git show HEAD:artifacts/unit-count-33e88c6.txt tail -> '5795 passed, 8 skipped'; m3-sensors.md:8 -> '412 passed' at d7ea327\",\n  \"board.py show T-177 -> staff-engineer r2 'fail' at 21:15:23Z (before ddfbf6d at 21:27:41), card in_progress; git log --grep T-177 -> 04ea2bf, 4fcf9cd, then r3 2e58e18 after the fix commit\",\n  \"git show HEAD:submission/NEEDS_CHRIS.md rows 8-9 -> '(card pending)'; board.py show T-192 -> P2 needs_chris\",\n  \"git show HEAD:docs/CONTRACT.md:601 -> OutSystems AI Agent Builder is Chris-supplied (area 5 optional marker is not invented)\",\n  \".venv/bin/python -m evals.run --check-fresh -> exit=0 (area 4 regression claim holds)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"accuracy\": 3, \"no_invented_chris_facts\": 5, \"eight_areas_covered\": 5, \"ai_acceptance_criteria\": 5, \"honesty_of_misses\": 5, \"voice\": 4, \"length\": 5, \"visual\": 5},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Three of the seven artifact counts are not what the commit holds, although the doc says 'counts are at the commit this doc was last edited'\",\n   \"evidence\": \"HEAD:submission/part2-process.md:3 'Paths are as committed; counts are at the commit this doc was last edited' and 'submission/prompt-log/reviews/ (460 review files)': git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | wc -l -> 467 (467 at ddfbf6d too). :110 '(memory/LESSONS.md, 44 entries)': git show HEAD:memory/LESSONS.md | grep -cE '^- ' -> 28 (28 at ddfbf6d); the working tree has 44 (git diff --stat HEAD -- memory/LESSONS.md -> 16 insertions). :114 '62 rows in memory/SCOPE_CUTS.md': git show HEAD:memory/SCOPE_CUTS.md | grep -ciE '^\\\\| *debt' -> 61; the working tree adds one. The other four counts match HEAD: 27 dated reports, 68 decisions, 62 R-IDs, 13 personas.\",\n   \"why_it_matters\": \"Round 1 asked for counts that match git, and the doc now claims they do. A panelist who opens memory/LESSONS.md finds 28 entries, not 44. In a doc whose area 8 says 'I check evidence, not claims', a count that is 57% too high reads as over-claiming.\",\n   \"fix\": \"Writer: recount from git show <commit> at the commit you edit in. Or ask the orchestrator to commit memory/LESSONS.md and memory/SCOPE_CUTS.md first, then recount all seven, including the prompt-log reviews after the final prompt-log export.\",\n   \"acceptance_test\": \"At the submission commit, each of the seven counts on :3, :13, :34, :110 and :114 equals the count from git ls-tree / git show of that commit, using the same grep rule each time.\"},\n  {\"severity\": \"minor\", \"title\": \"Area 8 says the D-065 fix 'is committed' as if it were complete; its review had failed twice when this was written\",\n   \"evidence\": \"HEAD:submission/part2-process.md:114 'demo answers prepared by our team were labeled as AI output; the decision is D-065 and the fix is committed.' board.py show T-177 -> 'review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-177-staff-engineer-r2.md; round 2' at 21:15:23Z, before ddfbf6d (21:27:41); status in_progress. The product note says it accurately: 'fixed in code, final check in progress'.\",\n   \"why_it_matters\": \"Area 8's example is 'when a bug reaches users'. Calling the fix done while its review is still failing is the exact pattern area 8 says Chris guards against. The two submission docs also disagree on the state of the same fix.\",\n   \"fix\": \"Match the product note: 'the decision is D-065; the fix is in code and its final review is in progress (T-177)'. Change it to 'done' only when T-177 is done.\",\n   \"acceptance_test\": \"The D-065 wording in part2-process.md and product-note.md agrees with board.py show T-177 status at the submission commit.\"},\n  {\"severity\": \"minor\", \"title\": \"'(NEEDS_CHRIS #9)' is an internal tracking marker in panel-facing text and is not in [CHRIS: ...] form\",\n   \"evidence\": \"HEAD:submission/part2-process.md:83 'This is my stance until a founder says otherwise (NEEDS_CHRIS #9).' Every other open item in the doc uses '[CHRIS: ...]' (:3, :13, :66, :104, :116, :120). HEAD:submission/NEEDS_CHRIS.md:23 row 9 says '(card pending)', though T-192 exists.\",\n   \"why_it_matters\": \"The pre-send scrub looks for '[CHRIS:'. This marker would survive into the doc Zlayt reads, and an internal ticket reference in Chris's voice is confusing there. The stale '(card pending)' shows the row-to-card parity check was not re-run.\",\n   \"fix\": \"Write it as '[CHRIS: confirm or change this stance (NEEDS_CHRIS #9)]' after the paragraph, and keep the sentence 'This is my stance until a founder says otherwise.' Set row 9's card column to T-192.\",\n   \"acceptance_test\": \"grep -n 'NEEDS_CHRIS #' submission/part2-process.md returns only lines inside [CHRIS: ...] markers; NEEDS_CHRIS row 9 names T-192.\"},\n  {\"severity\": \"nit\", \"title\": \"SVG and area 6 wording: 'rebuilt as four steps' reads as done; the engineering example names no card\",\n   \"evidence\": \"HEAD:submission/validation-ladder.svg:100-101 'which I found very hard to use; rebuilt as four steps (D-068), not yet scored' while T-181 is in_progress (area 4 :58 correctly says 'We are rebuilding'). part2-process.md:83 'In this build a blocker from the staff-engineer reviewer kept a card open until it was fixed.'\",\n   \"why_it_matters\": \"The tense in the SVG differs from the text. The area 6 example fails the generic-filler test because it does not say which card or what the blocker was.\",\n   \"fix\": \"SVG: 'being rebuilt as four steps (D-068)'. Area 6: name one card and its blocker in a clause.\",\n   \"acceptance_test\": \"SVG uses the same tense as area 4; the area 6 example names a card ID.\"},\n  {\"severity\": \"nit\", \"title\": \"The cited unit-count file is staged for deletion in the shared index\",\n   \"evidence\": \"git status --short artifacts/unit-count-33e88c6.txt -> 'D ' plus '??'; git ls-tree HEAD -> present (blob b7958bd).\",\n   \"why_it_matters\": \"A sweeping commit would remove the evidence for the area 8 test count from git.\",\n   \"fix\": \"Orchestrator: git restore --staged artifacts/unit-count-33e88c6.txt before the next commit.\",\n   \"acceptance_test\": \"git ls-files --error-unmatch artifacts/unit-count-33e88c6.txt succeeds.\"}\n ],\n \"whats_right\": [\n  \"Area 4 now says 'a persona score is a screen, not a ship call', which makes the D-068 miss the doc's strongest quality-bar argument. Area 7 reuses it as the honest-feedback example.\",\n  \"The SVG shows only behavior that is committed. The D-066 confirm is labeled in progress, and the split fallback matches docs/LLM_VS_CODE.md.\",\n  \"Area 6 now covers all three parties: engineering's 'how' rights and veto, evidence first, then the safer answer, then the founder. It also gives turnaround times and a week-by-week 30-day plan.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T21:33:16.462Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-186-product-manager-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:33:18.817Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-185-product-manager-r2.md; python3 tools/board.py validate reviews/T-186-product-manager-r2.md",
 "description": "Validate both review files"
}
````

### User / tool · 2026-11-02T21:33:19.000Z

**tool result**
````
ok (1 file(s))
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:33:19.790Z

Now updating memory with the new recurring pattern.

### Assistant · claude-opus-5-5 · 2026-11-02T21:33:25.071Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_submission_doc_patterns.md",
 "old_string": "**Why:** the hiring panel",
 "new_string": "7. **Counts from the working tree, not git.** At r2 (HEAD 2e58e18), \"44 LESSONS entries\" and \"62 debt rows\" matched the uncommitted tree, while HEAD had 28 and 61. Recount every count with `git show HEAD:` and the same grep rule each time.\n8. **Shared-index hazards.** A cited evidence file was staged for deletion ('D ' + '??') by someone else. `ls-files` lies here, so use `git ls-tree HEAD` / `git cat-file -e HEAD:path` (script: artifacts/review-evidence/T-185-pm/paths_in_head.py).\n9. **Front door at HEAD.** A committed scaffold (T-181) can replace the built UI in demo mode (/classic redirects). Check api.py routing at HEAD, not the running server, which may be older.\n10. **Placeholder judgment.** A [CHRIS:] for a motive behind Chris's own decision (D-031/D-042 were Chris inbox/chat) or for his management stance is acceptable if the doc reads complete without it and a card tracks it. Still check that row and card priority match, and that no unbracketed \"NEEDS_CHRIS #n\" leaks into panel text.\n\n**Why:** the hiring panel"
}
````

### User / tool · 2026-11-02T21:33:25.172Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_submission_doc_patterns.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:33:27.190Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [Submission doc patterns](feedback_submission_doc_patterns.md) — M5 note/Part 2: built-claims ahead of HEAD, persona-vs-human reviewability, disowned counts, untracked paths",
 "new_string": "- [Submission doc patterns](feedback_submission_doc_patterns.md) — M5 note/Part 2: built-claims ahead of HEAD, proxy-vs-human, working-tree counts, shared-index hazards, placeholder judgment (r1 fail, r2 changes)"
}
````

### User / tool · 2026-11-02T21:33:27.296Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:33:30.753Z

Both cards get **changes** (no blockers, one major each). All four round-1 blockers are fixed, and the T-191/T-192 placeholders are acceptable. T-185 major: row 2 still cites library amounts 0.580, which no committed report has (library-latest gives 0.681), and says the report is "being regenerated" with no card owning that.
T-186 major: three counts don't match the commit, though the doc says they do: LESSONS 44 vs 28, reviews 460 vs 467, debt rows 62 vs 61. Separately (not graded, brief item 4): at HEAD, demo mode sends `/` to the empty T-181 scaffold, so "What I built" can't be reached there; don't tag a submission commit until T-181 lands.
Reviews: /Users/arsis/zlayt-pm-project/reviews/T-185-product-manager-r2.md and /Users/arsis/zlayt-pm-project/reviews/T-186-product-manager-r2.md (both pass `board.py validate`).
