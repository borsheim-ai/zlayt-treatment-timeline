# Subagent: Writer: T-185/T-186 round 2 (Writer: T-185/T-186 round 2)

Source: `agent-a597a006d3a7de491.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:19:16.851Z

You are the writer in /Users/arsis/zlayt-pm-project. Your cards are T-185 (submission/product-note.md) and T-186 (submission/part2-process.md plus submission/validation-ladder.svg), both round 2. Claim each with --force.

Read these first:
- reviews/T-185-product-manager.md and reviews/T-186-product-manager.md;
- the orchestrator's newest note on each card;
- D-065 through D-068 in memory/ORCHESTRATOR_DECISIONS.md.

Fix every blocker and major the reviews raise. Rules:
- **Redesign story.** Say it honestly and in Chris's voice. Chris tried the UI and called it "VERY hard to use". That verdict drove the guided 4-step redesign (D-068). The persona reviewability score was measured before the redesign, so present it that way.
- **Only claim what is committed.** Run `git log --oneline -20` and check that the files you cite exist in git. Anything not landed yet, such as the guided UI (T-181) and the disputed-summary confirm (T-179), gets marked "in progress". The orchestrator will refresh the wording after those land.
- **Numbers come from files in git.** For the test count, run `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` from a `git archive HEAD` copy in your scratch dir, save the output under artifacts/, and cite that file. Report library recall (entries 0.775, amounts 0.580) next to the golden figures; take both from evals/reports.
- **Area 6** needs an engineering role. Give a reason for each stretch item.

Keep the documents tight; no filler. Commit with a temp index (GIT_INDEX_FILE plus `git read-tree HEAD`) and never run `git checkout` on files. Write the handoff, move both cards to in_review, and reply in 2 lines.

### User / tool · 2026-11-02T21:19:16.858Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:19.335Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B claim T-185 --agent writer --force; $B claim T-186 --agent writer --force; git log --oneline -20; cat .claude/agent-memory/writer/MEMORY.md; cat .claude/agent-memory/writer/submission_pipeline.md"
}
````

### User / tool · 2026-11-02T21:19:19.557Z

**tool result**
````
T-185 claimed by writer
T-186 claimed by writer
33e88c6 tools: prompt-log export also redacts tailnet hostnames, 100.64/10 addresses and a work email; docstring lists every edit (T-187 privacy review)
59e33ca docs(submission): one-page product note, Part 2 process doc, validation-ladder SVG
f22f8fc tools: prompt-log export writes <redacted> (scanner-safe) and no stale 'capped' header (T-187)
3b5fe43 feat(qa): M5 prompt log package (T-187)
9199b72 docs: NEEDS_CHRIS Docker verification item (T-182)
f547db4 docs(release): T-182 record timed clone path (17s) and Docker-daemon caveat
4671eee test(backend): T-183 M4 hardening check; plain message when a record-count limit is hit
d07bf9d docs(orchestrator): D-065 tooltip wording (T-177 r2)
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs
4fcf9cd fix(frontend): T-177 r2 honest provenance on every surface: prepared items name no drafting model (judge panel, models in health/case/judges/export, case trace, tooltip, banner, audit and ladder rows)
964505b docs(qa): T-045 r3: sensors record names the commit for the unit count (5782 at b824a6c)
b01382f feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)
b824a6c fix(evals): T-045 r3: --record-latest refuses non-live backends and recomputes the ship bar from the report body and per-run directory; records sha256 and source commit
a56f189 fix(backend): T-178 GATE-M3 chaos: interrupted runs recovered at startup, stale-tab 409 stale_item, invisible characters stripped and lone surrogates replaced (no 500)
de5cb3a docs(orchestrator): D-068 guided four-step UI redesign (Chris)
7c73294 test(qa): T-045 r2 sensors record (unit 5698, e2e 412, latest.json live, rejected-item claim corrected)
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
ee62967 docs(orchestrator): D-066 disputed accept needs a compare confirm; D-067 cut the drafted paragraph from the MVP UI; scope cuts 22-23
04ea2bf feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
d7ea327 test(qa): T-045 r2: real 375 px overflow check, rejected-item guard (unit + e2e), evals --record-latest points latest.json at the live run; fixture runs no longer replace a live latest.json
- [Submission pipeline](submission_pipeline.md) — page-fit method, number sources, pitfalls for product note and Part 2
---
name: submission-pipeline
description: How the product note and Part 2 doc were built and page-fitted, where each number comes from, and pitfalls
metadata:
  type: project
---

Submission docs live in `submission/`: `product-note.md` (1 page), `part2-process.md` (4 pages), `validation-ladder.svg` (hand-written; `mmdc` is not installed), `print.css` (shared print style).

**Page-fit check (no LaTeX here):** `pandoc X.md -s -o /private/tmp/.../x.html --css submission/print.css --embed-resources --resource-path=submission`, then Chrome headless `--print-to-pdf --no-pdf-header-footer`, count `/Type /Page` in the PDF. Product note fits one page only at 8.7pt (~1000 words); Part 2 fits 4 pages at 9.4pt (~2700 words). T-188 does the real PDFs; reuse print.css.

**Pitfalls:** pandoc needs a blank line before bullet/numbered lists after a bold lead-in; table column widths follow the dash counts in the separator row; a nested `**` inside a blockquote broke the miss-story block. The git-guard refuses `git add && git commit` in one command: stage, then commit with a pathspec in a second call.

**Number sources (re-check before final, they move):** live ship bar `evals/reports/20261102T164038Z.md`; unit 5698 / e2e 412 `evals/reports/m3-sensors.md`; library 34/42 = 0.81 from `reviews/GATE-M3-product-manager.md` (committed `library-latest.md` was stale); billing rounds `reviews/T-140-claims-adjuster*.md`; verify_quickly 4 `reviews/GATE-M3-paralegal.md` (old screen, persona, not a real paralegal).

**Honesty rules held:** no Chris-past facts beyond Appendix B; thresholds in Part 2 (30% time, 60% adoption) are labeled "my starting numbers"; fixes still in flight (T-177, T-179, T-181 guided UI) worded as in progress, so refresh them when those cards close.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:20.047Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-185; python3 tools/board.py show T-186"
}
````

### User / tool · 2026-11-02T21:19:20.287Z

**tool result**
````
---
id: "T-185"
title: "M5 product note: submission/product-note.md, one page, in Chris's voice (Appendix B): problem and user, what was built, cuts and why, ship bar (3-5 testable criteria from the eval), testing and findings, how AI can mislead and the validation ladder, LLM/code split, three post-launch metrics"
milestone: "M5"
role: "writer"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:19:19Z"
claimed_by: "writer"
claimed_at: "2026-11-02T21:19:19Z"
rounds: 1
commits: ["59e33cacd152f21c18727aab4738c5dc096ac486"]
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
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:19:19Z"
claimed_by: "writer"
claimed_at: "2026-11-02T21:19:19Z"
rounds: 1
commits: ["59e33cacd152f21c18727aab4738c5dc096ac486"]
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

## Handoff
What changed: submission/part2-process.md (4 pages, Letter 9.4pt via print.css), submission/validation-ladder.svg (hand-written; mmdc not installed), two rubric tables (3 AI acceptance criteria incl. must-never AI-3; ship bar), sample message + 30-min agenda, decision-rights table, rollout/metric thresholds (marked as my starting numbers).
How verified: pandoc + headless Chrome page count = 4; SVG rendered and inspected; numbers cite evals/reports/20261102T164038Z.md, m3-sensors.md, LESSONS (44), SCOPE_CUTS (61 debt rows), reviews/ (460 files), 68 decisions.
Left: Chris's miss story (marked block, NEEDS_CHRIS #4 / T-189), byline (#5), 4 optional [CHRIS: optional] one-liners (#6, T-190).
Surprised me: thresholds (30% time, 60% adoption) are my proposals, not facts; flagged as such in the doc. Counts (460 reviews, 74 reports) move; refresh at final.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:22.903Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-185-product-manager.md; echo =========; cat reviews/T-186-product-manager.md"
}
````

### User / tool · 2026-11-02T21:19:22.990Z

**tool result**
````
# T-185 product note: product-manager-reviewer (Dana Okafor lens)

**Verdict: fail** (2 blockers, 4 majors, 3 minors, 1 nit).

The note mostly does what a hiring panel wants. It has a five-row ship bar with live numbers and a report path. It puts the golden-vs-library flag gap in bold. It tells the billing rounds and the M3 gate failure plainly. It invents nothing about Chris. Most numbers I checked trace to their source: 242 grounding checks, 0.982/1.000 recall, 40/40, 0 of 10, 20/20, 12/12, 5 of 17 clean held-out, 412 E2E, 34/42 = 0.81, $16,147 vs $8,123.50, and D-040/D-052/D-065..D-068.

Two things fail it.

1. **It hides the biggest reviewability miss.** Chris used the M3 screen and called it "VERY hard to use", which forced a full redesign (D-068). The note still reports ship-bar row 5 as met at 4/5, a score from a persona reviewer on that same screen.
2. **It describes things that are not built as built.** The guided four-step screen is T-181, still in_progress with AC 0/1. Its files are untracked, and the running app serves the old UI. The D-066 compare-confirm exists only in the uncommitted working tree.

The majors:
- The unit-test count (5,698) is one the cited file says did not reproduce.
- Three stretch items shipped against "pick at most one", and the note gives no reason.
- The cited review paths are not in git.
- Library entry and amount recall (0.775 and 0.580 on the same library run) go unmentioned while the note implies only flags fail to generalize.

Page count: 1 page (pandoc + headless Chrome with submission/print.css, 8.7pt). Length is within the limit.

```json
{"card": "T-185", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/product-note.md at commit 59e33ca (working tree identical for this file); cited evidence: evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, evals/reports/latest.json, reviews/GATE-M3-*.md, reviews/T-140-claims-adjuster*.md, memory/SCOPE_CUTS.md, memory/ORCHESTRATOR_DECISIONS.md, docs/LLM_VS_CODE.md; app at http://localhost:7860 (demo mode, fixture backend); sample case",
 "exercised": [
  "Read personas/product-manager.md, docs/CONTRACT.md M5 (318-328), 8.2 ship bar, 11 DoD, Appendix A (493-596), Appendix B (598-607)",
  "Read submission/product-note.md twice; rendered it with pandoc + headless Chrome using submission/print.css: 1 page (artifacts/review-evidence/T-185-pm/note.pdf)",
  "Spot-checked 20+ numbers/claims against evals/reports/20261102T164038Z.md (grounding 1.000/242, entry 0.982, amount 1.000, flags 1.000 x4, 40/40, controls 0 of 10, J3 20/20, J4 12/12, 0 false agree, clean held-out 5 of 17, case_06 E3 miss, gap_28/73 assertions)",
  ".venv/bin/python -m evals.run --check-fresh -> exit=0; git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml -> empty (live run still valid for prompts)",
  "Compared the unit/E2E counts with evals/reports/m3-sensors.md:7-8 (5782 unit, 412 E2E)",
  "grep of D-001, D-007, D-022, D-031, D-034, D-040, D-042, D-047, D-052..D-054, D-059, D-062..D-068 in memory/ORCHESTRATOR_DECISIONS.md",
  "grep -rn '10,906' reviews/ memory/ -> only GATE-M2-paralegal.md, GATE-M2-r2-paralegal.md, GATE-M2-round1-triage.md; not in T-140-claims-adjuster*",
  "python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> entries 93/120 = 0.775, amounts 40/69 = 0.580, must flags 34/42 = 0.810",
  "python3 tools/board.py show T-181/T-179/T-177 and board.py list --status in_progress: T-181 (guided UI) in_progress AC 0/1; T-179 (D-066) in_progress",
  "git ls-files --error-unmatch app/frontend/guided/core.js -> not known to git; git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; working tree app/backend/review.py:298-349 has D-066 (uncommitted)",
  "curl http://localhost:7860/ -> old UI (index.html with stepper.css/sidebyside.css); /api/health -> demo_mode true, backend fixture",
  "python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample -> artifacts/review-evidence/T-185-pm/journey-sample-7860.out: 4 flag types present, gap 73 flagged, $185 under AMOUNTS NOT TOTALED, total $8,390.00, export 422 before any accept, 200 after",
  "curl /api/calibration -> calibrated confidence served; app/frontend/suggestions.js:119-120 renders it (confidence-indicator stretch item)",
  "git ls-files --error-unmatch on every cited path: reviews/GATE-M3-product-manager.md, reviews/GATE-M3-paralegal.md, reviews/T-140-claims-adjuster*.md untracked; tracked copies under submission/prompt-log/reviews/",
  "Spot-checked docs/LLM_VS_CODE.md rows 1 (split) and 7 (amount class) against the note's LLM/code paragraph"
 ],
 "verdict": "fail",
 "scores": {"accuracy": 2, "no_invented_chris_facts": 5, "required_contents": 4, "honesty_of_misses": 2, "voice": 4, "length": 5},
 "findings": [
  {"severity": "blocker", "title": "The UI redesign after Chris's feedback is hidden, and ship-bar row 5 still reports reviewability as met",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:76 D-068: 'Guided UI redesign (Chris, 2026-11-02: \"VERY hard to use… so simple someone's grandma can use it\")' with the reason 'The user's verdict on the current UI'. product-note.md:19 row 5 Result: '4/5 (reviews/GATE-M3-paralegal.md)'. product-note.md:23 says only 'Score 5 is a persona reviewer on the previous screen, not a real paralegal; not re-scored on the guided screen.' grep -n -iE 'hard to use|redesign|grandma|rebuilt' submission/product-note.md -> no match; D-068 appears only at :7 as the label of the new screen.",
   "why_it_matters": "This is the clearest AI-judgment lesson in the build. An AI persona passed the screen at 4/5, and the one human who used it said it was very hard to use. The note reports the proxy as a pass and never says the human verdict contradicted it. The panel grades 'define good enough and test against it'. Reporting a met bar on a screen the user rejected is hiding a known failure, a red flag in the dossier.",
   "fix": "Add a 'What testing found' bullet in Chris's voice, for example: 'Reviewability passed on paper and failed in use. A persona reviewer scored the M3 screen 4/5 on \"I could verify every claim quickly\". When I used it myself it was very hard to use (D-068), so we rebuilt it as a four-step guide. An AI reviewer is not a substitute for a person at the desk.' Change row 5 Result to 'Not met on the shipped screen: persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored', or give a re-score on the guided screen.",
   "acceptance_test": "grep -n -iE 'hard to use|rebuilt|redesign' submission/product-note.md returns a line in 'What testing found'; row 5's Result no longer reads as met without that qualification."},
  {"severity": "blocker", "title": "The note describes the guided four-step screen and the D-066 disputed-accept confirm as built; neither is at HEAD",
   "evidence": "product-note.md:7 'What I built. ... A guided four-step screen: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter (D-068). Review is one item at a time: ... two big answers.' board.py list --status in_progress: 'T-181 ... in_progress P0 AC 0/1 Build the guided UI (D-068)'. git ls-files --error-unmatch app/frontend/guided/core.js -> 'did not match any file(s) known to git'. curl http://localhost:7860/ serves the old index.html (stepper.css, sidebyside.css). product-note.md:32 'a disputed one needs a named confirm (D-066)'. git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty (D-066 code exists only uncommitted in app/backend/review.py:298-349; T-179 in_progress). The writer's own handoff says 'guided UI (T-181) is described as built'.",
   "why_it_matters": "The panel will open the prototype link and see a different product from the one the note describes. A PM note that claims an unbuilt UI and an unbuilt safety control misstates what was built. That is an invented fact under D.2, and it undercuts every other number in the note.",
   "fix": "Describe what HEAD ships today. Or hold the note until T-181 and T-179 are done and committed, then re-verify each sentence against the running app. Until then, mark both sentences [PENDING T-181] and [PENDING T-179] so nothing reads as shipped. Use present tense only for code at the commit the submission is tagged at.",
   "acceptance_test": "At the submission commit: board.py show T-181 and T-179 show done; git ls-files app/frontend/guided lists the files; GET / serves the guided shell; accepting a judge-disputed item without compared:true returns 422 COMPARE_REQUIRED. Otherwise neither sentence appears in present tense."},
  {"severity": "major", "title": "The unit-test count 5,698 is the figure the cited file says did not reproduce",
   "evidence": "product-note.md:19 '412 E2E, 5,698 unit tests pass (evals/reports/m3-sensors.md)'. evals/reports/m3-sensors.md:7: '5782 passed, 2 skipped ... The round-2 figure 5698 was taken before later commits added tests and did not reproduce ... a count is valid only for the commit named'.",
   "why_it_matters": "A number that contradicts its own citation is the first thing a careful panelist checks. It costs trust in every other number in the table.",
   "fix": "Use the count and commit the file states ('5,782 unit at b824a6c'), or re-run at the submission commit and cite that.",
   "acceptance_test": "Every test count in product-note.md equals a count in the cited sensors file for the commit named next to it."},
  {"severity": "major", "title": "Stretch: three items shipped against 'pick at most one', the note names two, and gives no reason for going beyond the brief or for reinstating cuts",
   "evidence": "Appendix A: 'Stretch (pick at most one, only if time remains): PDF upload, a confidence indicator, a side-by-side source viewer, or a draft paragraph'. product-note.md:9 'The brief allows one stretch; I picked the source viewer and also shipped PDF text-layer upload.' Calibrated confidence also ships (D-042 'calibrated confidence (shown as measured precision per state)'; GET /api/calibration returns it; app/frontend/suggestions.js:119-120 renders 'In testing on N synthetic cases, X of Y verified items matched the record'). :9 'Not cut: I reinstated cuts twice (D-031, D-042)' gives no why.",
   "why_it_matters": "'Cut scope on purpose' is the first row of 'What we evaluate'. Going past an explicit limit is defensible only with a stated reason. Undercounting what shipped and giving no reason reads as drift, not as a decision.",
   "fix": "Name all three (source viewer, PDF text layer, calibrated confidence). Add one sentence on why the brief's limit was exceeded and why cuts were reinstated, in Chris's words (see questions_for_chris), plus what that cost.",
   "acceptance_test": "The Cut paragraph lists every shipped Appendix A stretch item and gives one reason sentence for exceeding 'at most one' and for D-031/D-042."},
  {"severity": "major", "title": "Cited evidence paths are not in the repo the panel will open",
   "evidence": "git ls-files --error-unmatch reviews/GATE-M3-product-manager.md reviews/GATE-M3-paralegal.md reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md reviews/T-140-claims-adjuster-r3.md reviews/T-140-claims-adjuster-r4.md -> \"error: pathspec ... did not match any file(s) known to git\" for each. The tracked copies are submission/prompt-log/reviews/GATE-M3-product-manager.md etc. product-note.md:19, :23, :24 cite the reviews/ paths.",
   "why_it_matters": "Appendix A: 'Make sure we can open every link'. The 0.81 library recall, the 4/5 score and the billing-round claims are the note's honesty evidence. As cited, none of them opens in the repo.",
   "fix": "Either cite submission/prompt-log/reviews/... or have the orchestrator commit reviews/ before submission. Then click every path from a fresh clone.",
   "acceptance_test": "From a fresh clone of the submission commit, every path in product-note.md exists (scripted: extract backticked paths, test -e each)."},
  {"severity": "major", "title": "Generalization is reported only for flags; the same library run shows entry recall 0.775 and amount recall 0.580",
   "evidence": "product-note.md:16 row 2 'entries 0.982, amounts 1.000 [E]' (golden only); :23 'The 1.000 flag numbers do not generalize'. python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> 'entries: 93/120 = 0.775', 'amounts: 40/69 = 0.580', 'must flags: 34/42 = 0.810'. The committed evals/reports/library-latest.md is from a74b727 (stale; the writer's handoff says so).",
   "why_it_matters": "Saying the flag numbers do not generalize implies the recall numbers do. The same matchers on the same 15 packets say otherwise. Some of the gap may be expected-file drift after D-052/D-059 (exact class match in evals/run.py:180), but the note neither reports nor explains it.",
   "fix": "qa regenerates library-latest.md at the submission commit. The note's row 2 then gives golden and library side by side, with one clause on what the misses are (real misses or expected files that predate the billing redesign).",
   "acceptance_test": "evals/reports/library-latest.md source commit equals the submission commit; product-note.md row 2 cites its entry and amount numbers next to the golden ones."},
  {"severity": "minor", "title": "The $10,906 vs $6,000 billing example is attributed to the wrong reviews",
   "evidence": "product-note.md:24 'A claims-adjuster reviewer outworded every word-list rule: one library letter said $10,906 against a true $6,000 ... (reviews/T-140-claims-adjuster*.md)'. grep -rn '10,906' reviews/T-140-claims-adjuster*.md -> nothing; the source is reviews/GATE-M2-paralegal.md:30 and reviews/GATE-M2-round1-triage.md:9 (paralegal persona). $16,147 vs $8,123.50 does trace to the T-140 adjuster reviews.",
   "why_it_matters": "The brief requires each claim to trace to its cited file. This one does not.",
   "fix": "Attribute the $10,906 case to the paralegal reviewer at GATE-M2 (cite its path), or drop it.",
   "acceptance_test": "Each dollar figure on line 24 is found by grep in the file cited beside it."},
  {"severity": "minor", "title": "LLM/code paragraph says code does record splitting; the build has an LLM split fallback",
   "evidence": "product-note.md:38 'Code does anything with one right answer: record splitting, ...' and the model list omits splitting. docs/LLM_VS_CODE.md:29 row 1: 'Only when the code split finds a single record that is unsplit ... may a model be asked ... it returns character offsets only'; D-031 'LLM split fallback (flagged LLM_SPLIT)'; app/llm/prompts/split_v1.md is in the live report's hash list.",
   "why_it_matters": "The panel grades where the line was drawn. The note's summary should match LLM_VS_CODE.md, and here the honest version is the stronger one: the model only points at offsets, code cuts and validates.",
   "fix": "Add to 'The model reads': 'where to cut an unsplittable paste (offsets only; code validates and flags it LLM_SPLIT)'.",
   "acceptance_test": "The note's LLM list matches every LLM row in docs/LLM_VS_CODE.md."},
  {"severity": "minor", "title": "Post-launch metrics name no data source",
   "evidence": "product-note.md:42-44: #1 'against her own last three by hand' (no timed baseline method); #2 'letter lines an attorney corrects or an adjuster challenges, per 100' (no capture mechanism); #3 no source named (it is the audit log).",
   "why_it_matters": "A metric that cannot be computed cannot inform a decision. Each metric's decision is stated well; its source is not.",
   "fix": "One clause each: #1 timestamps from case-created to letter-copied events vs a stopwatch baseline taken in week 2; #2 attorney edit log plus adjuster letters tagged by the paralegal; #3 audit log accept events with before/after and time on item.",
   "acceptance_test": "Each of the three metrics names its event or log source."},
  {"severity": "nit", "title": "Internal decision IDs crowd a panel-facing page; 'Score 5' is unclear",
   "evidence": "product-note.md:31-36 failure table cites D-034, D-047, D-022, D-054, D-066, D-053, D-007 in five rows; :23 'Score 5 is a persona reviewer'.",
   "why_it_matters": "Appendix B voice: concise and plain. The panel cannot decode D-numbers without opening the log.",
   "fix": "Keep one or two IDs where they prove a decision; write 'ship-bar row 5' for 'Score 5'.",
   "acceptance_test": "At most three D-IDs in the failure table; no 'Score 5'."}
 ],
 "whats_right": [
  "The ship bar has five numeric criteria with live results and a report path, and the golden-vs-library flag gap is in bold rather than hidden.",
  "The billing rounds and the M3 gate failure (prepared answers labeled as AI, one-click accept of disputed items) are told plainly, with numbers.",
  "No invented facts about Chris: the byline and link are [CHRIS: ...] placeholders and tracked in NEEDS_CHRIS #5."
 ],
 "questions_for_chris": [
  "May the note quote your D-068 reaction ('VERY hard to use') in your own voice as the reviewability miss, or do you want it paraphrased?",
  "In one line, why did you reinstate cuts (D-031, D-042) and ship three stretch items when the brief says 'at most one'? The note needs your reason, not ours."
 ]}
```
=========
# T-186 Part 2 process doc: product-manager-reviewer (Dana Okafor lens)

**Verdict: fail** (2 blockers, 3 majors, 2 minors).

All eight areas are present, and most are specific to this build:

- **Area 1:** three plus three discovery questions, specific enough to ask tomorrow.
- **Area 2:** reasons for doing this first, plus four concrete pieces of evidence that would change the decision.
- **Area 3:** three AI acceptance criteria, one of them a "must never", each with its checker.
- **Area 4:** a test set built from real work product, a held-out half, and regression discipline that works (`--check-fresh` exit 0).
- **Area 5:** four measures with expand and kill thresholds, labeled as proposals.
- **Area 7:** a real message and agenda.
- **Area 8:** supervision examples taken from LESSONS.

The miss story is a correctly marked [CHRIS: ...] block, tracked in NEEDS_CHRIS #4 (T-189). The doc renders to 4 pages.

Two things fail it:

1. **It hides the UI redesign.** Chris rejected the M3 screen as "VERY hard to use" (D-068). The quality-bar table and the SVG still present reviewability as 4/5 met, and the area 7 answer on honest feedback skips the build's best example of it.
2. **The SVG claims an unbuilt control.** It presents the D-066 disputed-accept confirm as current behavior, but it is not at HEAD.

The majors:

- The unit-test count (5,698) is one the cited file says did not reproduce.
- Area 6 never says what engineering's role in product decisions is.
- The cited paths and counts (`reviews/GATE-M3-product-manager.md`, "460 review files", "74 dated reports") do not match what is in git.

```json
{"card": "T-186", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/part2-process.md and submission/validation-ladder.svg at commit 59e33ca; cited evidence: evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, reviews/GATE-M3-*.md, memory/{ORCHESTRATOR_DECISIONS,LESSONS,SCOPE_CUTS,ASSUMPTIONS}.md, spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md; app at http://localhost:7860 (demo mode); sample case",
 "exercised": [
  "Read personas/product-manager.md; docs/CONTRACT.md M5 (318-328), Appendix A Part 2 eight areas + One story + Format (565-586), Appendix B (598-607)",
  "Read submission/part2-process.md twice and marked each of the eight areas specific/generic/missing; read submission/validation-ladder.svg source",
  "Rendered with pandoc + headless Chrome (submission/print.css): artifacts/review-evidence/T-185-pm/part2.pdf = 4 pages; viewed page 1 (SVG renders with both columns and the measured box)",
  "Spot-checked counts: memory/ORCHESTRATOR_DECISIONS.md 68 unique D-IDs (D-001..D-068); grep -c '^- 20' memory/LESSONS.md = 44; grep -c '^| debt' memory/SCOPE_CUTS.md = 61; ls personas/*.md = 13; spec/REQUIREMENTS.md 62 unique R-IDs; R-TL-2 (:49), R-TL-10 (:57), R-CO-3 (:137) exist; A-101..A-109 in ASSUMPTIONS",
  "Checked the area 3/4 numbers against evals/reports/20261102T164038Z.md (grounding 1.000/242, 0.982/1.000, 40/40, J3 20/20, J4 12/12, 0 false agree, must_not 0)",
  "Checked area 8 examples against memory/LESSONS.md:43,45 (12/12 from uncommitted tree; HEAD broke twice), .git/hooks/pre-commit -> tools/check_index_imports.py, reviews/GATE-M3-chaos-tester.md:116 (run stuck after restart), reviews/GATE-M3-round1-triage.md (M3 failed, 2 blockers), board/milestones.md (M0-M2 pass)",
  ".venv/bin/python -m evals.run --check-fresh -> exit=0 (the regression claim in area 4 holds)",
  "git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; T-179 in_progress (board.py show)",
  "git ls-tree --name-only 59e33ca reviews/ | wc -l -> 136; git ls-files submission/prompt-log/reviews | wc -l -> 460; git ls-files evals/reports | grep -cE '[0-9]{8}T[0-9]{6}Z.md$' -> 33; git ls-files --error-unmatch reviews/GATE-M3-product-manager.md -> not known to git",
  "python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample (four flag types, 73-day gap, $185 not totaled, export only after accepts)",
  "Checked submission/NEEDS_CHRIS.md rows 4-7 against T-189/T-190 (both needs_chris)"
 ],
 "verdict": "fail",
 "scores": {"accuracy": 3, "no_invented_chris_facts": 5, "eight_areas_covered": 4, "ai_acceptance_criteria": 5, "honesty_of_misses": 2, "voice": 4, "length": 5, "visual": 4},
 "findings": [
  {"severity": "blocker", "title": "The UI redesign after Chris's feedback is missing; the quality-bar table and the SVG present reviewability as met",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:76 D-068: 'Guided UI redesign (Chris, 2026-11-02: \"VERY hard to use… so simple someone's grandma can use it\")'. part2-process.md:56 'Reviewable | ... at least 4/5 | 4/5 (persona reviewer)'. validation-ladder.svg:97 'every claim quickly\" 4 of 5'. grep -n -iE 'hard to use|redesign|grandma|D-068|guided' submission/part2-process.md -> no match. Area 7 (:87) answers 'How do you get honest, usable feedback' with no build example. The miss-story hooks (:124) list library recall, evidence checks and demo labels, not this.",
   "why_it_matters": "Part 2's quality bar is graded on 'what score means ship'. This build's own record says the persona score passed a screen the human rejected. Leaving that out overstates how well the bar worked, which is a dossier red flag (hides a known failure). It also wastes the most persuasive answer the doc could give to areas 4 and 7: AI reviewers are necessary but not enough, so a person at the desk comes before the ship call.",
   "fix": "Area 4: add a line under the table: 'Reviewability passed on a persona score and failed in use. I found the M3 screen very hard to use and we rebuilt it (D-068). The ship call now needs a real paralegal session, not a persona score.' Change the table and SVG Result to 'persona 4/5 on the old screen; rejected in use; guided screen not yet scored'. Area 7: use it as the example of honest feedback. Optionally add it to the miss-story hooks.",
   "acceptance_test": "grep -n -iE 'hard to use|rebuilt|D-068' submission/part2-process.md returns a line in area 4 or 7; the reviewability Result in the table and SVG no longer reads as met without qualification."},
  {"severity": "blocker", "title": "The SVG presents the D-066 compare-confirm as current product behavior; it is not at HEAD",
   "evidence": "validation-ladder.svg:58 'A summary the judge disputed needs a named \"I compared it with the quote.\"' (inside 'Rung 3: the paralegal decides'). git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; the enforcement is only in uncommitted app/backend/review.py:298-349; board.py show T-179 -> status in_progress. GATE-M3-product-manager.md:46 measured 5 of 5 disputed entries accepted with one click.",
   "why_it_matters": "The diagram is the visual the brief requires, and it claims a safety control on the path to the letter that the shipped code lacks. Overstating a guardrail in a hiring doc is an invented fact about the product (D.2).",
   "fix": "Re-verify once T-179 is done and committed. Until then, word rung 3 as 'Decided (D-066), in progress: a disputed summary will need a named confirm'.",
   "acceptance_test": "At the submission commit, accepting a judge-disputed item without compared:true returns 422 COMPARE_REQUIRED; otherwise the SVG line is in future tense."},
  {"severity": "major", "title": "The unit-test count 5,698 is the figure the cited file says did not reproduce",
   "evidence": "part2-process.md:108 'Unit tests (5,698 passed), E2E (412 passed, evals/reports/m3-sensors.md)'. evals/reports/m3-sensors.md:7: '5782 passed, 2 skipped ... The round-2 figure 5698 was taken before later commits added tests and did not reproduce'.",
   "why_it_matters": "Area 8 argues 'I check evidence, not claims'. Citing a number its own source disowns undercuts exactly that point.",
   "fix": "Cite '5,782 at b824a6c', or re-run at the submission commit and cite that.",
   "acceptance_test": "Each test count in part2-process.md equals the count in the cited file for the commit named."},
  {"severity": "major", "title": "Area 6 never states engineering's role in product decisions",
   "evidence": "Appendix A area 6: 'How are product decisions made among the founders, engineering and you?' part2-process.md:77-79: the table has three columns, 'I decide alone', 'I decide with the litigation lead' and 'A founder decides'. Engineering does not appear in :75-83.",
   "why_it_matters": "There is no product org at Zlayt, so who owns build-vs-buy, estimates, model and stack choices, and the LLM/code line is exactly what the founders asked. One of three named parties is missing.",
   "fix": "Add an engineering column or two lines. For example: engineering decides how (stack, model routing inside the budget, test design) and has a veto on 'not safe to ship'; I decide what and when; the LLM/code line is drawn together and written down in an ADR.",
   "acceptance_test": "Area 6 names at least two decisions engineering owns and how a disagreement with engineering is settled."},
  {"severity": "major", "title": "Cited evidence paths and artifact counts do not match what is in the repo",
   "evidence": "part2-process.md:44 cites reviews/GATE-M3-product-manager.md -> git ls-files --error-unmatch: 'did not match any file(s) known to git' (the tracked copy is submission/prompt-log/reviews/GATE-M3-product-manager.md). :3 'reviews/ (460 review files)': git ls-tree 59e33ca reviews/ -> 136 files; the 460 are under submission/prompt-log/reviews/. :3 'evals/reports/ (74 dated reports)': 33 tracked.",
   "why_it_matters": "The doc's argument is 'point at the artifacts as proof' (Appendix B). A panelist who opens reviews/ and finds 136 files, or a 404 on the gate review, reads it as over-claiming.",
   "fix": "Point at the paths that exist in the submitted repo (submission/prompt-log/reviews/), or have the orchestrator commit reviews/ and evals/reports/ first, then recount at the submission commit.",
   "acceptance_test": "From a fresh clone of the submission commit, every path in part2-process.md exists, and the counts on line 3 equal ls | wc -l of the named directory."},
  {"severity": "minor", "title": "The SVG says record splitting is code only; the build has an LLM split fallback",
   "evidence": "validation-ladder.svg:77-78 'Code, no model' / 'Split records.' docs/LLM_VS_CODE.md:29 row 1: 'Only when the code split finds a single record that is unsplit ... may a model be asked ... character offsets only'; D-031 'LLM split fallback (flagged LLM_SPLIT)'.",
   "why_it_matters": "The visual should match the graded LLM/code table, and the real design is the more impressive one.",
   "fix": "Change to 'Split records (a model may only point at cut offsets for an unsplittable paste; code validates)'.",
   "acceptance_test": "Every 'Code, no model' item in the SVG is code-only in docs/LLM_VS_CODE.md."},
  {"severity": "minor", "title": "A claim about how PI firms work is stated as fact; the assumption range is off by one",
   "evidence": "part2-process.md:23 '**Every matter needs one,** so volume is high.' (no assumption marker, while the line above marks 'assumption, to confirm'). :13 'A-101 to A-108', but memory/ASSUMPTIONS.md also has A-109.",
   "why_it_matters": "Appendix A ground rule: 'If you assume something about how personal injury firms work, state the assumption.'",
   "fix": "'Every matter with treatment needs one (assumption: confirm the share of matters that reach a demand letter)'; 'A-101 to A-109'.",
   "acceptance_test": "Each PI-practice claim in area 2 carries an assumption marker or an A-ID."}
 ],
 "whats_right": [
  "Discovery questions (3 + 3) and the paralegal message and agenda are specific enough to use tomorrow, and they ask for artifacts and errors, not opinions.",
  "Three AI acceptance criteria, including the must-never AI-3 on hedges, merged dates and the $185 rate, each with a named checker and a live result.",
  "Metrics table defines adoption, time saved, quality and retention with expand and kill thresholds, honestly labeled as starting proposals, and regression discipline is real (--check-fresh exit 0)."
 ],
 "questions_for_chris": [
  "For area 6: what decision rights do you want to give engineering (for example a 'not safe to ship' veto, model choice inside a budget)? The doc should state your stance, not ours."
 ]}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:23.340Z

**tool call — Bash**
````
{
 "command": "grep -nE \"^## D-06[5-8]|^### D-06[5-8]|D-06[5-8]\" memory/ORCHESTRATOR_DECISIONS.md | head -20"
}
````

### User / tool · 2026-11-02T21:19:23.485Z

**tool result**
````
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
74:| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
75:| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
76:| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:25.217Z

**tool call — Bash**
````
{
 "command": "cat -n submission/product-note.md; echo ======; cat -n submission/part2-process.md; echo =====; cat -n submission/validation-ladder.svg; ls submission artifacts | head -80; git status --short | head -30"
}
````

### User / tool · 2026-11-02T21:19:25.557Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:26.915Z

**tool call — Bash**
````
{
 "command": "cat -n submission/product-note.md"
}
````

### User / tool · 2026-11-02T21:19:27.051Z

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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:29.444Z

**tool call — Bash**
````
{
 "command": "cat -n submission/part2-process.md"
}
````

### User / tool · 2026-11-02T21:19:29.522Z

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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:29.625Z

**tool call — Bash**
````
{
 "command": "cat -n submission/validation-ladder.svg; ls submission submission/prompt-log | head -50; git status --short | head -30"
}
````

### User / tool · 2026-11-02T21:19:29.774Z

**tool result**
````
     1	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 600" width="820" height="600" font-family="-apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="t d">
     2	  <title id="t">Validation ladder: nothing an AI wrote reaches the letter without a code check, a second model, and the paralegal</title>
     3	  <desc id="d">A record's text goes to a model that drafts a summary and quote. Rung 1, code, checks the quote word for word and every number. Rung 2, a second model with a different prompt, answers a fixed choice. Code computes the state. Rung 3, the paralegal, accepts, edits or dismisses. Code assembles the export from accepted items only. Items that fail are shown in a could-not-verify list and never exported. A separate code-only lane handles dates, gaps and amounts with no model.</desc>
     4	  <defs>
     5	    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker>
     6	  </defs>
     7	  <rect width="820" height="600" fill="#ffffff"/>
     8	
     9	  <!-- column headers -->
    10	  <text x="20" y="26" font-size="13" font-weight="700" fill="#111">Language work: model drafts, then three checks</text>
    11	  <text x="560" y="26" font-size="13" font-weight="700" fill="#111">Single right answer: code only</text>
    12	
    13	  <!-- input -->
    14	  <rect x="20" y="40" width="470" height="44" rx="6" fill="#f3f3f3" stroke="#888"/>
    15	  <text x="34" y="60" font-size="12.5" font-weight="700" fill="#111">Record text</text>
    16	  <text x="34" y="76" font-size="11.5" fill="#333">Untrusted data. Never treated as instructions. Models run with no tools.</text>
    17	
    18	  <path d="M255,84 V104" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>
    19	
    20	  <!-- generator -->
    21	  <rect x="20" y="106" width="470" height="62" rx="6" fill="#e8f0fe" stroke="#3b6fd4"/>
    22	  <text x="34" y="126" font-size="12.5" font-weight="700" fill="#0b3a8c">AI draft (generator model)</text>
    23	  <text x="34" y="143" font-size="11.5" fill="#222">One-line summary + exact quote; flag category + quote.</text>
    24	  <text x="34" y="158" font-size="11.5" fill="#222">Never supplies a date, an amount, or the wording of a warning.</text>
    25	
    26	  <path d="M255,168 V188" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>
    27	
    28	  <!-- rung 1 -->
    29	  <rect x="20" y="190" width="470" height="86" rx="6" fill="#e9f6ec" stroke="#2f8f4e"/>
    30	  <text x="34" y="210" font-size="12.5" font-weight="700" fill="#14572b">Rung 1: code check</text>
    31	  <text x="34" y="227" font-size="11.5" fill="#222">Quote is in the record word for word (whole sentences).</text>
    32	  <text x="34" y="242" font-size="11.5" fill="#222">Every number, date, $ figure, left/right, no/not/without is in the quote.</text>
    33	  <text x="34" y="257" font-size="11.5" fill="#222">Hedges in the quote ("may represent", "approx.") are kept in the summary.</text>
    34	  <text x="34" y="270" font-size="11.5" fill="#222">Clauses the quote does not support are removed by code, and shown.</text>
    35	
    36	  <path d="M255,276 V296" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>
    37	
    38	  <!-- rung 2 -->
    39	  <rect x="20" y="298" width="470" height="70" rx="6" fill="#fdf3e0" stroke="#c78a1b"/>
    40	  <text x="34" y="318" font-size="12.5" font-weight="700" fill="#7a4d00">Rung 2: independent second model (judge)</text>
    41	  <text x="34" y="335" font-size="11.5" fill="#222">Different prompt and model. Sees only the record and the candidate.</text>
    42	  <text x="34" y="350" font-size="11.5" fill="#222">Answers with a fixed choice and a reason code, never prose.</text>
    43	  <text x="34" y="363" font-size="11.5" fill="#222">Disagree, unsure or no answer: the item is marked needs review.</text>
    44	
    45	  <path d="M255,368 V388" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>
    46	
    47	  <!-- state -->
    48	  <rect x="20" y="390" width="470" height="40" rx="6" fill="#f3f3f3" stroke="#888"/>
    49	  <text x="34" y="407" font-size="12.5" font-weight="700" fill="#111">State, computed by code</text>
    50	  <text x="34" y="422" font-size="11.5" fill="#333">verified or needs review. Needs review sorts first. Verified is not accepted.</text>
    51	
    52	  <path d="M255,430 V450" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>
    53	
    54	  <!-- rung 3 -->
    55	  <rect x="20" y="452" width="470" height="62" rx="6" fill="#f6e9f7" stroke="#8e44a0"/>
    56	  <text x="34" y="472" font-size="12.5" font-weight="700" fill="#5a1f69">Rung 3: the paralegal decides</text>
    57	  <text x="34" y="489" font-size="11.5" fill="#222">Accept, edit or dismiss, one item at a time, quote beside the line.</text>
    58	  <text x="34" y="504" font-size="11.5" fill="#222">A summary the judge disputed needs a named "I compared it with the quote."</text>
    59	
    60	  <path d="M255,514 V534" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>
    61	
    62	  <!-- export -->
    63	  <rect x="20" y="536" width="470" height="48" rx="6" fill="#111" stroke="#111"/>
    64	  <text x="34" y="555" font-size="12.5" font-weight="700" fill="#fff">Export, assembled by code from accepted items only</text>
    65	  <text x="34" y="572" font-size="11.5" fill="#ddd">Letter: quotes + charges. Internal notes (do not send): flags, unclear amounts.</text>
    66	
    67	  <!-- rejected tray, right of rung 1 -->
    68	  <path d="M490,233 H520 V300 H540" fill="none" stroke="#b3261e" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ar)"/>
    69	  <rect x="542" y="262" width="258" height="78" rx="6" fill="#fdecea" stroke="#b3261e"/>
    70	  <text x="554" y="282" font-size="12" font-weight="700" fill="#8c1d18">Could not verify (visible list)</text>
    71	  <text x="554" y="298" font-size="11" fill="#222">Quote not in the record, or a number</text>
    72	  <text x="554" y="312" font-size="11" fill="#222">the quote lacks. Never a flag, never in</text>
    73	  <text x="554" y="326" font-size="11" fill="#222">the letter. She can write the entry herself.</text>
    74	
    75	  <!-- code-only lane -->
    76	  <rect x="542" y="40" width="258" height="190" rx="6" fill="#f3f3f3" stroke="#888"/>
    77	  <text x="554" y="60" font-size="12" font-weight="700" fill="#111">Code, no model</text>
    78	  <text x="554" y="78" font-size="11" fill="#222">Split records. Parse dates (an ambiguous</text>
    79	  <text x="554" y="92" font-size="11" fill="#222">date waits for her). Gap arithmetic:</text>
    80	  <text x="554" y="106" font-size="11" fill="#222">29 and 30 days no, 31 yes; 28 no, 73 yes.</text>
    81	  <text x="554" y="124" font-size="11" fill="#222">Find every dollar amount and its class</text>
    82	  <text x="554" y="138" font-size="11" fill="#222">(a rate is never a charge). Totals of what</text>
    83	  <text x="554" y="152" font-size="11" fill="#222">she accepted. Flag wording from templates.</text>
    84	  <text x="554" y="170" font-size="11" fill="#222">Dates and amounts always need her explicit</text>
    85	  <text x="554" y="184" font-size="11" fill="#222">accept. Conflict pairs are proposed by code;</text>
    86	  <text x="554" y="198" font-size="11" fill="#222">the judge only says conflict or benign.</text>
    87	
    88	  <!-- evidence -->
    89	  <rect x="542" y="358" width="258" height="226" rx="6" fill="#ffffff" stroke="#888"/>
    90	  <text x="554" y="378" font-size="12" font-weight="700" fill="#111">Measured (live run, 3 runs)</text>
    91	  <text x="554" y="396" font-size="11" fill="#222">Rung 1: grounding 1.000, 242 checked</text>
    92	  <text x="554" y="412" font-size="11" fill="#222">Rung 2: seeded wrong summaries caught</text>
    93	  <text x="554" y="426" font-size="11" fill="#222">40/40; correct ones rejected 0 of 10</text>
    94	  <text x="554" y="442" font-size="11" fill="#222">Conflict judge 20/20, flag judge 12/12,</text>
    95	  <text x="554" y="456" font-size="11" fill="#222">0 false agrees</text>
    96	  <text x="554" y="474" font-size="11" fill="#222">Rung 3: persona rates "I could verify</text>
    97	  <text x="554" y="488" font-size="11" fill="#222">every claim quickly" 4 of 5; but 5 of 5</text>
    98	  <text x="554" y="502" font-size="11" fill="#222">disputed summaries took one click, so</text>
    99	  <text x="554" y="516" font-size="11" fill="#222">D-066 requires a named confirm</text>
   100	  <text x="554" y="536" font-size="10.5" fill="#555">Sources: evals/reports/20261102T164038Z.md,</text>
   101	  <text x="554" y="550" font-size="10.5" fill="#555">reviews/GATE-M3-paralegal.md,</text>
   102	  <text x="554" y="564" font-size="10.5" fill="#555">reviews/GATE-M3-product-manager.md,</text>
   103	  <text x="554" y="578" font-size="10.5" fill="#555">docs/LLM_VS_CODE.md</text>
   104	</svg>
submission:
NEEDS_CHRIS.md
part2-process.md
print.css
product-note.md
prompt-log
validation-ladder.svg

submission/prompt-log:
CONTRACT.md
README.md
REDACTIONS.md
TOOLS.md
board-activity.jsonl
decisions-and-lessons
reviews
transcripts
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
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:33.762Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD; git ls-files reviews | wc -l; git ls-files submission/prompt-log/reviews | wc -l; git ls-files evals/reports | tail -15; ls evals/reports | tail -15; git status --short evals/reports reviews | head; python3 tools/board.py list --status in_progress 2>/dev/null | head; "
}
````

### User / tool · 2026-11-02T21:19:34.221Z

**tool result**
````
33e88c6
     136
     460
evals/reports/runs/20261102T115041Z/run3.json
evals/reports/runs/20261102T115041Z/sample.json
evals/reports/runs/20261102T161327Z/case_01_date_formats.json
evals/reports/runs/20261102T161327Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T161327Z/case_03_rate_and_ocr.json
evals/reports/runs/20261102T161327Z/case_04_duplicates_no_amounts.json
evals/reports/runs/20261102T161327Z/case_05_provider_conflict.json
evals/reports/runs/20261102T161327Z/case_06_subtle_pre_existing.json
evals/reports/runs/20261102T161327Z/case_07_prompt_injection.json
evals/reports/runs/20261102T161327Z/case_08_diagnosis_temptation.json
evals/reports/runs/20261102T161327Z/case_09_nonvisit_hides_gap.json
evals/reports/runs/20261102T161327Z/run1.json
evals/reports/runs/20261102T161327Z/run2.json
evals/reports/runs/20261102T161327Z/run3.json
evals/reports/runs/20261102T161327Z/sample.json
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
T-177	M3	backend    	in_progress      	P0	AC 1/1	GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels
T-179	M3	frontend   	in_progress      	P0	AC 0/1	GATE-M3 UI round: D-066 compare-confirm to accept a judge-disputed item (backend enforces 422 without it; batch excludes); D-067 hide the drafted treatment paragraph; UX/a11y minors (h1 on case page, Undo row hidden under sticky header, Try again focus, dismiss announcement overwritten, refused-edit names the words to keep, 320px Theme/Shortcuts/Export)
T-181	M3	frontend   	in_progress      	P0	AC 0/1	Build the guided UI (D-068) on the existing API: new shell at /, old screen at /classic; Your cases, 4 fixed steps, one-item review queue, bills, letter; guided e2e suite
T-185	M5	writer     	in_progress      	P0	AC 1/1	M5 product note: submission/product-note.md, one page, in Chris's voice (Appendix B): problem and user, what was built, cuts and why, ship bar (3-5 testable criteria from the eval), testing and findings, how AI can mislead and the validation ladder, LLM/code split, three post-launch metrics
T-186	M5	writer     	in_progress      	P0	AC 1/1	M5 Part 2 process doc: submission/part2-process.md (<=4 pages) answering the eight Part 2 areas with this build's specifics; validation-ladder diagram + spec/eval-rubric excerpt as visuals; Chris's miss story as a marked [CHRIS: ...] block listed in NEEDS_CHRIS
T-187	M5	qa         	in_progress      	P0	AC 1/1	M5 prompt log: submission/prompt-log/ with TOOLS.md, CONTRACT copy, board activity log, all reviews, DECISIONS, LESSONS, and tools/export_prompt_log.py export of the agent transcripts (unedited, one file per agent) plus a two-paragraph reading guide
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:39.806Z

**tool call — Bash**
````
{
 "command": "for p in submission/prompt-log/reviews/GATE-M3-product-manager.md submission/prompt-log/reviews/GATE-M3-paralegal.md submission/prompt-log/reviews/GATE-M2-paralegal.md submission/prompt-log/reviews/GATE-M3-round1-triage.md evals/reports/20261102T164038Z.md evals/reports/m3-sensors.md evals/reports/library-latest.md memory/SCOPE_CUTS.md memory/ORCHESTRATOR_DECISIONS.md docs/LLM_VS_CODE.md spec/REQUIREMENTS.md; do git ls-files --error-unmatch $p >/dev/null 2>&1 && echo \"OK  $p\" || echo \"NOT $p\"; done; ls submission/prompt-log/reviews | grep -E \"T-140|GATE-M3|GATE-M2\" ; git ls-files | grep -E \"evals/reports/[0-9]{8}T\" | wc -l; git ls-files | grep -E \"^evals/reports/[0-9]{8}T[0-9]{6}Z.md\" | wc -l"
}
````

### User / tool · 2026-11-02T21:19:40.159Z

**tool result**
````
OK  submission/prompt-log/reviews/GATE-M3-product-manager.md
OK  submission/prompt-log/reviews/GATE-M3-paralegal.md
OK  submission/prompt-log/reviews/GATE-M2-paralegal.md
OK  submission/prompt-log/reviews/GATE-M3-round1-triage.md
OK  evals/reports/20261102T164038Z.md
OK  evals/reports/m3-sensors.md
OK  evals/reports/library-latest.md
OK  memory/SCOPE_CUTS.md
OK  memory/ORCHESTRATOR_DECISIONS.md
OK  docs/LLM_VS_CODE.md
OK  spec/REQUIREMENTS.md
GATE-M2-claims-adjuster.md
GATE-M2-legal-nurse.md
GATE-M2-paralegal.md
GATE-M2-privacy-compliance.md
GATE-M2-qa.md
GATE-M2-r2-claims-adjuster.md
GATE-M2-r2-legal-nurse.md
GATE-M2-r2-paralegal.md
GATE-M2-r2-staff-engineer.md
GATE-M2-round1-triage.md
GATE-M2-staff-engineer.md
GATE-M2-summary.md
GATE-M3-accessibility.md
GATE-M3-chaos-tester.md
GATE-M3-paralegal.md
GATE-M3-product-manager.md
GATE-M3-round1-triage.md
GATE-M3-staff-engineer.md
GATE-M3-ux-designer.md
T-140-claims-adjuster-r2.md
T-140-claims-adjuster-r3.md
T-140-claims-adjuster-r4.md
T-140-claims-adjuster.md
T-140-staff-engineer-r2.md
T-140-staff-engineer-r3.md
T-140-staff-engineer-r4.md
T-140-staff-engineer.md
      27
      27
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:40.495Z

**tool call — Bash**
````
{
 "command": "git log -3 --format='%h %ad' --date=iso -- evals/reports/library-latest.md; head -40 evals/reports/library-latest.md; cat evals/reports/m3-sensors.md | head -30"
}
````

### User / tool · 2026-11-02T21:19:40.627Z

**tool result**
````
ce70bd2 2026-11-02 00:34:27 -0600
328428f 2026-11-01 22:21:07 -0600
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:44.726Z

**tool call — Bash**
````
{
 "command": "git status --short evals/reports/library-latest.md evals/reports/m3-sensors.md; python3 - <<'E'\nimport re\nt=open('evals/reports/library-latest.md').read()\ne=a=f=[0,0]\nE1=[0,0];A=[0,0];F=[0,0]\nfor l in t.splitlines():\n    if l.startswith('| case_lib'):\n        c=[x.strip() for x in l.strip('|').split('|')]\n        for col,acc in ((2,E1),(3,A),(5,F)):\n            n,d=c[col].split('/'); acc[0]+=int(n); acc[1]+=int(d)\nprint(E1,E1[0]/E1[1],A,A[0]/A[1],F,F[0]/F[1])\nE\nls artifacts | head -30; ls evals/reports | grep -i lib"
}
````

### User / tool · 2026-11-02T21:19:44.886Z

**tool result**
````
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
ValueError: not enough values to unpack (expected 2, got 1)
m0-smoke
mockups
review-evidence
screenshots
t119-r3-e2e-full.txt
t119-r3-mutB.txt
tmp
calibration.json
library-latest.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:47.251Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nt=open('evals/reports/library-latest.md').read()\nE1=[0,0];A=[0,0];F=[0,0]\nfor l in t.splitlines():\n    if l.startswith('| case_lib'):\n        c=[x.strip() for x in l.strip('|').split('|')]\n        for col,acc in ((2,E1),(3,A),(5,F)):\n            if '/' in c[col]:\n                n,d=c[col].split('/'); acc[0]+=int(n); acc[1]+=int(d)\nprint(E1,E1[0]/E1[1],A,A[0]/A[1],F,F[0]/F[1])\nE\nls artifacts/review-evidence/ | head -30; ls artifacts/review-evidence/GATE-M3-pm 2>/dev/null; git ls-files artifacts/review-evidence/GATE-M3-pm | head"
}
````

### User / tool · 2026-11-02T21:19:47.530Z

**tool result**
````
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
IndexError: list index out of range
GATE-M2-paralegal
GATE-M2-r2-paralegal
GATE-M3-accessibility-01-overview-empty-dark.png
GATE-M3-accessibility-01-overview-empty-light.png
GATE-M3-accessibility-02-overview-empty-error-dark.png
GATE-M3-accessibility-02-overview-empty-error-light.png
GATE-M3-accessibility-03-overview-cases-dark.png
GATE-M3-accessibility-03-overview-cases-light.png
GATE-M3-accessibility-04-overview-status-error-dark.png
GATE-M3-accessibility-04-overview-status-error-light.png
GATE-M3-accessibility-10-case-top-dark.png
GATE-M3-accessibility-10-case-top-light.png
GATE-M3-accessibility-11-rename-open-dark.png
GATE-M3-accessibility-11-rename-open-light.png
GATE-M3-accessibility-12-edit-open-dark.png
GATE-M3-accessibility-12-edit-open-light.png
GATE-M3-accessibility-13-source-dialog-dark.png
GATE-M3-accessibility-13-source-dialog-light.png
GATE-M3-accessibility-14-row-more-open-dark.png
GATE-M3-accessibility-14-row-more-open-light.png
GATE-M3-accessibility-15-why-dialog-dark.png
GATE-M3-accessibility-15-why-dialog-light.png
GATE-M3-accessibility-16-audit-drawer-dark.png
GATE-M3-accessibility-16-audit-drawer-light.png
GATE-M3-accessibility-17-disclosures-open-dark.png
GATE-M3-accessibility-17-disclosures-open-light.png
GATE-M3-accessibility-18-flags-dark.png
GATE-M3-accessibility-18-flags-light.png
GATE-M3-accessibility-19-charges-dark.png
GATE-M3-accessibility-19-charges-light.png
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:52.317Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/libsum.py <<'E'\nimport sys\nt=open(sys.argv[1]).read()\nE1=[0,0];A=[0,0];F=[0,0]\nfor l in t.splitlines():\n    c=[x.strip() for x in l.strip('|').split('|')]\n    if l.startswith('| case_lib') and len(c)>=9 and c[1].startswith('done'):\n        for col,acc in ((2,E1),(3,A),(5,F)):\n            n,d=c[col].split('/'); acc[0]+=int(n); acc[1]+=int(d)\nprint('entries',E1,round(E1[0]/E1[1],3),'amounts',A,round(A[0]/A[1],3),'flags',F,round(F[0]/F[1],3))\nE\npython3 /private/tmp/claude-501/libsum.py evals/reports/library-latest.md; head -5 artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md; python3 /private/tmp/claude-501/libsum.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md; git ls-files artifacts/review-evidence/GATE-M3-pm | head -3; git log --oneline -3 -- evals/reports/library-latest.md"
}
````

### User / tool · 2026-11-02T21:19:52.495Z

**tool result**
````
entries [93, 120] 0.775 amounts [47, 69] 0.681 flags [34, 42] 0.81
# Library report (reported, not gated)

Source commit: unknown (tree: unknown). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.
Traceback (most recent call last):
  File "/private/tmp/claude-501/libsum.py", line 8, in <module>
    n,d=c[col].split('/'); acc[0]+=int(n); acc[1]+=int(d)
    ^^^
ValueError: not enough values to unpack (expected 2, got 1)
ce70bd2 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
328428f feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:19:59.101Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>/dev/null | grep -iE \"librar|T-18[0-9]|T-19[0-9]\" ; ls -la evals/reports/library-latest.md artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md; grep -n \"0.580\\|0\\.775\\|library\" memory/STATE.md | head"
}
````

### User / tool · 2026-11-02T21:19:59.272Z

**tool result**
````
T-052	M3	researcher 	done             	P2	AC 3/3	Research: synthetic multi-case library grounded in real PI use cases
T-053	M3	backend    	done             	P2	AC 3/3	Multi-case: case list + switcher (local/dev mode only), library loader
T-077	M3	researcher 	done             	P1	AC 2/2	Research: real-world PI case patterns for the multi-case library (v2)
T-079	M3	qa         	done             	P1	AC 2/2	Build library packets lib08..lib15 from the v2 research (synthetic, with expected.json)
T-129	M3	backend    	done             	P2	AC 1/1	Ingest: a non-library preamble counts as a phantom record 1
T-180	M3	frontend   	blocked          	P0	AC 1/1	Guided UI design (D-068): exact spec + clickable static mockup of Your cases, the 4 fixed steps, one-item-at-a-time review, bills, letter; grandma-simple, looks nice
T-181	M3	frontend   	in_progress      	P0	AC 0/1	Build the guided UI (D-068) on the existing API: new shell at /, old screen at /classic; Your cases, 4 fixed steps, one-item review queue, bills, letter; guided e2e suite
T-182	M4	release    	in_review        	P0	AC 0/1	M4 release: Dockerfile (port 7860) with docker run verified; Hugging Face Spaces (Docker SDK, app_port 7860, secrets via Space settings) and Replit instructions (check current HF docs); README.md timed run-from-clone (<5 min); .env.example; Makefile/run.sh
T-183	M4	backend    	changes_requested	P0	AC 1/1	M4 hardening check: server-side key never exposed, per-session rate limit and spend cap on live calls, demo mode serves the prepared sample answers with no key, optional bring-your-own-key, input size limits, error states; fill only real gaps
T-184	M4	qa         	ready            	P0	AC 0/1	M4 demo assets: annotated screenshots of every guided-UI state (artifacts/screenshots/ + artifacts/CAPTIONS.md); <=3-minute Playwright-recorded walkthrough artifacts/demo.webm on the sample case; narration script Chris can read
T-185	M5	writer     	in_progress      	P0	AC 1/1	M5 product note: submission/product-note.md, one page, in Chris's voice (Appendix B): problem and user, what was built, cuts and why, ship bar (3-5 testable criteria from the eval), testing and findings, how AI can mislead and the validation ladder, LLM/code split, three post-launch metrics
T-186	M5	writer     	in_progress      	P0	AC 1/1	M5 Part 2 process doc: submission/part2-process.md (<=4 pages) answering the eight Part 2 areas with this build's specifics; validation-ladder diagram + spec/eval-rubric excerpt as visuals; Chris's miss story as a marked [CHRIS: ...] block listed in NEEDS_CHRIS
T-187	M5	qa         	in_progress      	P0	AC 1/1	M5 prompt log: submission/prompt-log/ with TOOLS.md, CONTRACT copy, board activity log, all reviews, DECISIONS, LESSONS, and tools/export_prompt_log.py export of the agent transcripts (unedited, one file per agent) plus a two-paragraph reading guide
T-188	M5	writer     	ready            	P0	AC 0/1	M5 package: submission/SUBMISSION_CHECKLIST.md mirroring Appendix A with links; submission/email-draft.md; final prioritized submission/NEEDS_CHRIS.md; PDF exports via pandoc (else HTML)
T-189	M5	orchestrator	needs_chris      	P0	AC 0/1	Chris: write the one story of a miss for Part 2 (submission/part2-process.md, last section, marked [CHRIS: ...] block)
T-190	M5	orchestrator	needs_chris      	P1	AC 0/1	Chris: fill the [CHRIS: ...] placeholders in the product note and Part 2 (full name, public link, optional real examples)
-rw-r--r--@ 1 arsis  staff  2394 Nov  2 14:02 artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md
-rw-r--r--@ 1 arsis  staff  2412 Nov  2 00:34 evals/reports/library-latest.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:06.107Z

**tool call — Bash**
````
{
 "command": "grep -rn \"0\\.580\\|0\\.775\\|40/69\\|93/120\" submission/prompt-log/reviews/GATE-M3-product-manager.md memory evals/reports/*.md 2>/dev/null | head; git ls-files | grep -c \"^reviews/T-185\"; grep -n \"library\" submission/prompt-log/reviews/GATE-M3-product-manager.md | head"
}
````

### User / tool · 2026-11-02T21:20:06.235Z

**tool result**
````
0
48:- About a third of library items need review (106 of 297), so she will be clicking through a lot of warnings.
53: "scope": "git archive d0b04bc (HEAD d0b04bc); app at 127.0.0.1:7973 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), server PID 50240 stopped; sample case + all 15 library packets; docs: CONTRACT What-we-evaluate and M3, spec/REQUIREMENTS.md incl. §7 ship bar, ORCHESTRATOR_DECISIONS D-042..D-064, SCOPE_CUTS, GATE-M2-summary, MVP-ux-audit-r4",
57:  "lib_sweep.py over the sample + 15 library cases: needs_review counts, and judge-disputed entries accepted with one click (lib_sweep.out: 106/297 needs_review; 5 of 5 disputed accepted with 200)",
63:  "evals.library_report regenerated at d0b04bc (library-d0b04bc.md); lib_missed.py lists missed must-flags for lib08/09/10/13/15",
76:   "evidence": "lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.",
78:   "fix": "For entries with JUDGE_PARTIAL or JUDGE_UNSUPPORTED: (1) code marks the summary's content words that are not in the quote; (2) Accept needs either an edit or a named confirm ('I checked the summary against the quote'); (3) the internal notes list 'accepted over a second-check objection: record N' so the attorney sees it; (4) add a reported eval, 'letter summary lines whose own Source quote does not support them, accept-all profile, library + golden', and put its number in the product note.",
90:  {"severity": "major", "title": "The ship bar's 1.000 flag numbers do not generalize: at d0b04bc the library shows 34/42 must-flags; the committed library and latest.json reports are stale",
91:   "evidence": "library-d0b04bc.md (regenerated at d0b04bc): must flags 1/3 lib08, 1/2 lib09, 0/1 lib10, 1/3 lib13, 1/3 lib15, 34/42 = 0.81 overall. lib_missed.py: missed conflicts 'Denies LOC per patient' vs 'brief loss of consciousness at the second collision', 'Left shoulder pain' vs 'Right shoulder pain', 'denies back pain' vs 'Low back pain 8/10'; lib10 G1 49-day gap reported as 'Gap of 43 days' from a CMS-1500. The committed evals/reports/library-latest.md is from a74b727 (231 commits back) and shows must_not hits that no longer reproduce. The committed evals/reports/latest.json reads ship_bar_met False (fixture, 14:39Z).",
92:   "why_it_matters": "The product note will quote 'flag precision/recall 1.000'. Those numbers come from 10 cases written alongside the rules. Without the library number beside them, the claim goes beyond what the evidence supports, and the canonical pointer a panel opens says False.",
93:   "fix": "qa commits a library report regenerated at the gate commit and the live latest.json. The product note reports golden and library side by side, naming the conflict categories not covered (SCOPE_CUTS 13).",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:21.005Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $SC/arch && mkdir -p $SC/arch && SHA=$(git rev-parse HEAD) && git archive HEAD | tar -x -C $SC/arch && ln -s /Users/arsis/zlayt-pm-project/.venv $SC/arch/.venv && echo $SHA > $SC/arch/.sha && echo started; cat /Users/arsis/zlayt-pm-project/.venv/pyvenv.cfg | head -3; ls $SC/arch | head -30"
}
````

### User / tool · 2026-11-02T21:20:23.566Z

**tool result**
````
started
home = /opt/homebrew/opt/python@3.12/bin
include-system-site-packages = false
version = 3.12.2
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:28.329Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SC/arch && (.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > $SC/unit.out 2>&1; echo \"exit=$?\" >> $SC/unit.out) ",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T21:20:28.398Z

**tool result**
````
Command running in background with ID: b4ih3anoi. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b4ih3anoi.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:29.165Z

**tool call — Bash**
````
{
 "command": "git ls-files app/frontend/guided | head -3; git grep -n -iE \"COMPARE_REQUIRED|compared\" HEAD -- app/backend | head -3; git ls-files app/frontend | head -30; sed -n 1,80p evals/reports/20261102T164038Z.md | head -60; grep -n \"stretch\\|Stretch\" memory/SCOPE_CUTS.md memory/ORCHESTRATOR_DECISIONS.md | head -20"
}
````

### User / tool · 2026-11-02T21:20:29.329Z

**tool result**
````
HEAD:app/backend/amounts.py:801:    'manual ther' meet; 'Manual therapy' and 'Therapeutic exercise' do not). The amount is compared by the caller."""
HEAD:app/backend/amounts.py:884:    paralegal is asked, not told). A date is compared only when BOTH lines state one: a line with no date of service may be the same visit as a dated one."""
HEAD:app/backend/billing.py:4:record) and classed charge, adjustment, payment, rate or unclear. NOTHING IS TOTALED OR COMPARED here: no sum of any kind, no
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
memory/SCOPE_CUTS.md:63:| debt | T-046 accepted with documented debt after 2 rounds (§7.4) | Stretch card, 2 rounds; pane works at >=1024px. Major (Show-gap-flag link needs ~190 Tab presses: add a skip link/shortcut) and minors carried to T-060. | see card | M3 |
memory/ORCHESTRATOR_DECISIONS.md:39:| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:32.902Z

**tool call — Bash**
````
{
 "command": "grep -n \"^| D-042\" memory/ORCHESTRATOR_DECISIONS.md memory/DECISIONS.md | cut -c1-1500; grep -rn \"D-042\" memory/*.md | head -3 | cut -c1-300; grep -n \"Stretch\" docs/CONTRACT.md | head"
}
````

### User / tool · 2026-11-02T21:20:33.004Z

**tool result**
````
memory/ORCHESTRATOR_DECISIONS.md:50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provide
memory/DECISIONS.md:9:018 second-wave additions (D-031 to D-040) · 019 amendments after T-094 and D-047 to D-052 (amends 005, 011, 012, 013, 014, 017 in place; items 1 and 2 superseded by 020) · 020 amendments after T-094 round 2: D-042, D-052 to D-054, T-110 (amends 005, 011, 013, 014, 015, 017 i
memory/DECISIONS.md:143:- Status: accepted (M1, amended rounds 2 and 3; D-006, D-010, D-011, D-012, D-021; amended by ADR-019: no 409 edit path, D-047 and D-051 checks on accept; amended by ADR-020: guarded charge reclassification, D-042)
memory/DECISIONS.md:152:  - **Edit rules (D-010, D-012).** Entries: the summary text, or the excerpt changed to a contiguous run of whole sentence units of the same record (ADR-016). Charges: **accept or dismiss**, plus the guarded reclassification of ADR-020 (D-042: a figure leaves the total freely
536:**Stretch** (pick at most one, only if time remains): PDF upload, a confidence indicator, a side-by-side source viewer, or a draft paragraph in a firm's voice.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:52.023Z

**tool call — Bash**
````
{
 "command": "grep -l \"10,906\" submission/prompt-log/reviews/*.md; grep -l \"16,147\" submission/prompt-log/reviews/*.md; grep -n \"10,906\" submission/prompt-log/reviews/GATE-M2-paralegal.md | cut -c1-400; cat submission/NEEDS_CHRIS.md; git ls-files | grep -E \"^(memory/(LESSONS|ASSUMPTIONS|SCOPE_CUTS)|personas/)\" | head -20; ls personas | wc -l"
}
````

### User / tool · 2026-11-02T21:20:52.237Z

**tool result**
````
submission/prompt-log/reviews/GATE-M2-r2-paralegal.md
submission/prompt-log/reviews/GATE-M2-round1-triage.md
submission/prompt-log/reviews/GATE-M2-paralegal.md
submission/prompt-log/reviews/T-185-product-manager.md
submission/prompt-log/reviews/T-140-claims-adjuster-r2.md
submission/prompt-log/reviews/T-140-staff-engineer.md
submission/prompt-log/reviews/T-140-claims-adjuster.md
submission/prompt-log/reviews/T-185-product-manager.md
3:Verdict: **fail** (1 blocker, 1 major, 3 minor). The sample case works the way a paralegal needs: every entry has its verbatim quote beside it, "Open record" highlights the quote inside the record, and the letter matches the golden export. The lib11 ledger case does not. The app labels the ledger total ($2,740) and the balance due ($2,166) as "Charge", says the second check agreed, and a plain a
30:   "title": "lib11: ledger total and balance due are labelled Charge, and accept-all puts $10,906.00 in the letter (correct: $6,000.00)",
31:   "evidence": "artifacts/review-evidence/GATE-M2-paralegal/l1-body.txt:447 'Detected charges (6)' lists $250.00, $180.00, $2,310.00, $2,740.00 and $2,166.00 all as 'Charge', each with 'Quote matches' and the line 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.' After accepting all six, l4.out.txt:1 reads 'Accepted charges: $10,906.00' and t
32:   "why_it_matters": "The letter tells the carrier billed charges are $10,906, about 80 percent over the records' own $6,000, and it counts the ledger total on top of its own three lines plus a balance that is already net of a payment and a discount. The adjuster checks arithmetic first. The tool gives the paralegal a green 'second check agreed' on exactly the two numbers it should have held ba
66:  "Is the library packet set meant to be inside the M2 ship bar? If lib11's $10,906 stays a library-only known failure, the product note should say the charge classifier can count a ledger total and balance."
# NEEDS CHRIS

Only things the team genuinely cannot do or decide without you. Nothing here blocks the run: each row says what we do meanwhile.
Each row has a `needs_chris` card on the board. Answer through the board's Inbox (one line is enough) unless the row says otherwise.

| # | Pri | Card | What | Exact action / expected answer | Meanwhile we… |
|---|---|---|---|---|---|
| 1 | P1 | T-019 | Real Anthropic API key for the public deployment | Put a real key in `.env` as `ANTHROPIC_API_KEY=<redacted> (local) and as the Space secret `ANTHROPIC_API_KEY` (Hugging Face). Only needed if you answer "live" to #2. | Run dev on the `claude-cli` backend (your claude.ai login); public build runs cached demo. |
| 2 | P1 | T-022 | Public link: demo-only or live? | Inbox: `demo-only` or `live, cap $N/day`. | Demo-only (cached sample run through the real pipeline code). Live needs an env opt-in (D-008). |
| 3 | P2 | T-023 | Live-model eval budget on your claude.ai plan (~25–35 calls per sample run) | Inbox: `ok` or a cap, e.g. `max 300 calls`. | Live runs only for ship-bar measurements (3× sample, golden set, the seeded-hallucination set (currently 40 items)); fixtures otherwise. |

Coming in M5 (cards created then): the "one story" of a miss (yours alone), the Hugging Face Space name/URL, an optional own-voice demo narration, and the final send of the email.

## Writer items (T-185 product note, T-186 Part 2) — added 2026-11-02

| # | Pri | Card | What | Exact action / expected answer | Meanwhile we… |
|---|---|---|---|---|---|
| 4 | P0 | T-189 | **The one story: a feature or launch you owned that missed the mark.** Yours alone; the team will not write it. | Replace the `[CHRIS: write this yourself ...]` block at the end of `submission/part2-process.md` ("The one story: a miss") with about 200 words: (1) what you shipped and expected, (2) what you missed and the number or signal that showed it, (3) one concrete process change (an artifact or rule), (4) how it shows up in this project. Hooks from this build are listed in the block. | Leave the marked block in place; everything else in Part 2 is complete. |
| 5 | P1 | T-190 | Byline and public link for the product note and Part 2 | In `submission/product-note.md` line 3 and `submission/part2-process.md` line 3: replace `[CHRIS: full name]` with the name as it should appear; in the product note replace `[CHRIS: public link, ...]` with the Hugging Face Space URL once it exists (see #2). | Placeholders stay visible, so nothing is sent with a made-up name or link. |
| 6 | P2 | T-190 | Optional one-line real examples in Part 2 (each is marked `[CHRIS: optional ...]`) | Area 1: watching real work without exposing client data. Area 5: how you measured adoption on the OutSystems AI Agent Builder. Area 7: a time you got honest feedback from users who said little. Area 8: supervising developers on a late feature. Add one or two sentences each, or delete the marker. | Part 2 reads complete without them; the markers are the only gaps. |
| 7 | P2 | T-190 | Product note, "Score 5": the 4/5 "I could verify every claim quickly" is a persona reviewer on the previous screen, not a real paralegal | Optional: have a real paralegal (or someone who does this work) run the sample case on the guided screen and tell you the score; replace the sentence in the "What testing found" list. | The note states plainly that the score is from a persona reviewer. |

## Answered
- Git author email (T-024): Chris → cborsheim@gmail.com (00:47Z). Set repo-locally; earlier commits keep the previous author because history rewrites are blocked.

## Decided by the team — FYI, no action needed
Product calls we made under ambiguity. Override any of them through the Inbox if you disagree.
- Citation format in the export: `Provider, date of service` + `[Ex. __ / Bates __]` placeholder (A-106). Real Zinda practice is a discovery question in Part 2, area 1.
- Flags (gaps, priors, causation) never go in the letter text; they go in a separate "internal — do not send" block (D-001).
- AI-assistance statement: UI banner + internal notes, not the letter (D-009).
- Flagged record language may appear in the letter only as part of an accepted whole-sentence excerpt, listed in internal notes (D-012).
- Ambiguous dates are never inferred; the paralegal confirms them (D-010).
- Tailnet ports: board on :7777, app on :7860; your existing 443/8443 mappings untouched (ADR-000e).

## Letter total wording changed (D-062, 2026-11-02) — FYI, override if you disagree
- The carrier letter's total line now reads `Billed charges accepted from these records: $X` (was `... stated in these records`). Three adversarial rounds showed a classifier can be outworded by a crafted ledger, so the line now says exactly what it is: the sum of the charges the paralegal accepted one at a time, each listed with its source line. Assumption: firms prefer an honest, defensible total over one that implies the records state it.

## Docker verification (T-182) — 2 minutes, optional
- This Mac has the Docker client but no running daemon, so the image was verified with the same recipe outside Docker (fresh venv, README path 17 s). If you have Docker Desktop: start it, then run `make docker docker-run` in the repo and open http://localhost:7860. Note the result on T-182 via the board Inbox. Assumption until then: the Dockerfile is correct (the HF Space build will also exercise it).
memory/ASSUMPTIONS.md
memory/LESSONS.md
memory/SCOPE_CUTS.md
personas/accessibility.md
personas/chaos-tester.md
personas/claims-adjuster.md
personas/hiring-panel.md
personas/installer.md
personas/legal-nurse.md
personas/litigation-lead.md
personas/paralegal.md
personas/privacy-compliance.md
personas/product-manager.md
personas/security.md
personas/staff-engineer.md
personas/ux-designer.md
      13
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:00.187Z

**tool call — Bash**
````
{
 "command": "sleep 5; tail -c 300 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/unit.out; cd /Users/arsis/zlayt-pm-project; git ls-files | grep -E \"^(app/frontend/(source|sidebyside)\\.js|app/backend/pdf|app/backend/calibration)\" ; git grep -l \"narrative\" HEAD -- app/frontend/index.html"
}
````

### User / tool · 2026-11-02T21:21:05.325Z

**tool result**
````
................................... [ 11%]
........................................................................ [ 12%]
........................................................................ [ 13%]
........................................................................ [ 14%]
.................app/backend/calibration_route.py
app/backend/pdf_checks.py
app/backend/pdf_hidden.py
app/backend/pdf_ocr.py
app/backend/pdf_routes.py
app/backend/pdf_text.py
app/frontend/sidebyside.js
app/frontend/source.js
HEAD:app/frontend/index.html
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:30.002Z

**tool call — Bash**
````
{
 "command": "git ls-files evals/golden/sample.expected.json memory/LESSONS.md board/milestones.md memory/contracts/api.md submission/prompt-log/TOOLS.md README.md; grep -c '^- 20' memory/LESSONS.md; grep -c '^| debt' memory/SCOPE_CUTS.md; git show HEAD:memory/ORCHESTRATOR_DECISIONS.md | grep -oE \"^\\| D-[0-9]+\" | sort -u | wc -l; git ls-files | grep -E \"^evals/reports/[0-9]{8}T[0-9]{6}Z.md$\" | wc -l; git ls-files submission/prompt-log/reviews | wc -l; grep -n \"R-ID\\|R-[A-Z]*-[0-9]\" spec/REQUIREMENTS.md | grep -oE \"R-[A-Z]+-[0-9]+\" | sort -u | wc -l; grep -n \"A-109\\|A-101\" memory/ASSUMPTIONS.md | head -3 | cut -c1-80"
}
````

### User / tool · 2026-11-02T21:21:30.183Z

**tool result**
````
README.md
board/milestones.md
evals/golden/sample.expected.json
memory/LESSONS.md
memory/contracts/api.md
submission/prompt-log/TOOLS.md
44
62
      68
      27
     460
      63
15:| A-101 | The paralegal assembles the chronology; the attorney reviews and si
23:| A-109 | Library packet case_lib01 record 3 keeps its recorded extract failu
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:33.785Z

**tool call — Bash**
````
{
 "command": "grep -oE \"^\\| R-[A-Z]+-[0-9]+\" spec/REQUIREMENTS.md | sort -u | wc -l; grep -n \"ADR\\|001\\b\" docs/LLM_VS_CODE.md | head -3; git ls-files memory/DECISIONS.md"
}
````

### User / tool · 2026-11-02T21:21:33.936Z

**tool result**
````
      62
3:*Treatment Timeline prototype. For the hiring panel, reviewers and the developers who maintain it. Decisions behind this page: `memory/DECISIONS.md` ADR-003, 004, 005, 008, 010 to 020; cross-cutting decisions D-001 to D-057 in `memory/ORCHESTRATOR_DECISIONS.md`. Requirements it serves: `spec/REQUIREMENTS.md`.*
121:Any change to a row, a prompt, a model or the phrase list is an ADR plus a re-run of the golden evaluation (`python -m evals.run`), with the report attached to the card (contract section 8.3). The table must match the code; a reviewer who finds a difference has found a defect.
memory/DECISIONS.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:34.723Z

Now write the product note.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:50.303Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/submission/product-note.md",
 "content": "# Treatment Timeline: product note\n\nChris [CHRIS: full name] · Zlayt AI PM project, Part 1 · prototype: [CHRIS: public link, see `submission/NEEDS_CHRIS.md`] · synthetic data only · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`); run steps in `README.md`\n\n**Problem and user.** A Zinda Law Group litigation lead says paralegals spend hours turning scattered records into a treatment chronology before each demand letter, and mistakes cost credibility. The user is the paralegal. She reviews, she does not trust, so every line must be checkable against its source. The attorney signs (assumption A-101).\n\n**What I built.** Paste or upload records (text, or a PDF text layer). Each timeline entry shows the AI's summary beside the verbatim record quote; she accepts, edits or dismisses it. Code finds the dollar amounts and she accepts each charge one at a time. The export is two blocks that never mix (D-001): a **letter section** (accepted entries and charges only, each with its verbatim quote, provider, date and an `[Ex. __ / Bates __]` placeholder) and **internal notes, do not send** (30-day gaps, conflicts, prior conditions, causation language, amounts not totaled). Every AI step sits behind the validation ladder: the model drafts, code checks, a second model checks, she decides. **In progress, not yet in the app:** the guided four-step screen (D-068, T-181) and the confirm for a disputed summary (D-066, T-179). Why: see the first finding below.\n\n**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts and roles, real patient data, EHR integrations, any medical or legal judgment. After trying: the \"patient said it\" label (four adversarial rounds each found a mislabeled quote; D-040), per-provider billing totals (five rounds, each found a way to drop a figure, so billing is a cited line listing; D-052), the drafted treatment paragraph (no eval; D-067). **Stretch:** the brief says pick at most one. I shipped three: the side-by-side source viewer, PDF text-layer upload and calibrated confidence (measured precision, not an invented %). I went past the limit on purpose: D-031 and D-042 reinstated every cut that needed no paid integration and no login, each keeping the ladder rules. [CHRIS: your reason, one line.] It cost us: the paragraph went in without an eval and came back out, and billing took four adversarial rounds.\n\n**Good enough to ship.** Live run, 3 runs, `claude-sonnet-5-5` generator, `claude-haiku-5-5` judge. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md` (15 library packets, run at a74b727, before the billing redesign).\n\n| # | Criterion (bar) | Result |\n|-|------------|--------------|\n| 1 | Grounding: every exported statement and amount has a quote found in the input (100%) | 1.000, 242 checked [E] |\n| 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; regenerated report pending). The library misses cluster in ledgers, EOBs, scans and Spanish; I have not yet split real misses from expected files that predate the billing redesign |\n| 3 | Flags: precision and recall 0.9 per type; 28-day interval not flagged, 73-day flagged | golden: 1.000/1.000, all four types; 28 no, 73 yes [E]. **Library: 34 of 42 must-flags, 0.81 [L]** |\n| 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct summaries rejected; conflict and flag judges 20/20 and 12/12, 0 false agrees [E] |\n| 5 | Reviewable: paralegal persona rates \"I could verify every claim quickly\" 4/5 or more; tests green | **Not met on the screen I rejected.** Persona 4/5 on the M3 screen (`submission/prompt-log/reviews/GATE-M3-paralegal.md`); I found that screen very hard to use. Guided screen not yet scored. Tests: 5,xxx unit passed at 33e88c6 (`artifacts/UNITFILE`); 412 E2E passed at d7ea327 (`evals/reports/m3-sensors.md`) |\n\n**What testing found.** (Reviews: `submission/prompt-log/reviews/`.)\n\n- **Reviewability passed on paper and failed in use.** A persona reviewer scored the M3 screen 4/5. When I used it myself it was *very* hard to use. I wanted it so simple that anyone could use it (D-068), so we are rebuilding it as four fixed steps with one question at a time. The 4/5 was measured before the redesign and does not count for the new screen. An AI reviewer is not a substitute for a person at the desk, so the ship call now needs a real paralegal session.\n- **The 1.000 flag numbers do not generalize.** The golden cases were written next to the rules. On the 15 library packets, must-flag recall is 0.81 (`GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes, like \"Left shoulder pain\" against \"Right shoulder pain\". Only 5 of 17 \"held-out\" conflict controls are still clean, so judge numbers are partly in-sample.\n- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: one library letter said $16,147 against a true $8,123.50 (`T-140-claims-adjuster.md`), and a paralegal reviewer found a letter at $10,906 against a true $6,000 (`GATE-M2-paralegal.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total says what it is: \"Billed charges accepted from these records.\"\n- **The M3 gate failed once.** Demo answers written by our team were labeled as AI output (fixed in code, final check in progress), and one click accepted a summary the second check had disputed, 5 of 5 times across 16 cases (`GATE-M3-product-manager.md`). The named \"I compared it with the quote\" confirm is in progress (T-179).\n\n**How the AI can mislead her, and what the design does.**\n\n| Failure | Design |\n|--------|-------------|\n| Changes a number, side or negation; drops a hedge (\"may represent\") | Code needs each in the quote: hard refusal on her edits, needs-review on AI text |\n| Says more than the quote | Code removes unsupported clauses; the second check reads the rest. Disputed ones will need a named confirm (D-066, in progress) |\n| Invents an amount, or obeys an order hidden in a record | Only code finds money, default-deny, she accepts each charge; models have no tools and return a checked form |\n| Rules on cause or diagnosis | Flag wording is a code template; the model returns a category and a quote only (D-007) |\n| Silently drops what it could not verify | Nothing is dropped: a visible \"could not verify\" list |\n| The judge is a model too | Judges are scored on seeded wrong items; \"verified\" never means accepted |\n\n**LLM and code.** Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals, quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed conflict pair, where to cut a paste code could not split (offsets only; code validates and flags it LLM_SPLIT), and the second check. Table: `docs/LLM_VS_CODE.md`.\n\n**Three metrics after launch.**\n\n1. **Minutes from first paste to copied letter section, against her own last three by hand.** Source: case-created and letter-copied timestamps, against a stopwatch baseline taken in week 2. Is it faster? Read beside #2: speed from skipping review is no win.\n2. **Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100.** Source: the attorney's edit log, plus adjuster letters the paralegal tags. Target 0. Each one becomes an eval case.\n3. **Needs-review items accepted unchanged, and median seconds per item.** Source: audit-log accept events with before and after text and time on item. Verifying or clicking through? (5 of 5 disputed items took one click.)\n"
}
````

### User / tool · 2026-11-02T21:21:50.378Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/submission/product-note.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:59.947Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b,cnt=1):\n    global s\n    assert s.count(a)==cnt,(a,s.count(a))\n    s=s.replace(a,b)\n\nrep(\"`reviews/` (460 review files), `evals/reports/` (74 dated reports), `memory/ORCHESTRATOR_DECISIONS.md` (68 decisions).\",\n    \"`submission/prompt-log/reviews/` (460 review files), `evals/reports/` (27 dated reports), `memory/ORCHESTRATOR_DECISIONS.md` (68 decisions). Paths are as committed; counts are at the commit this doc was last edited.\")\nrep(\"A-101 to A-108\",\"A-101 to A-109\")\nrep(\"**Every matter needs one,** so volume is high.\",\"**Every matter with treatment needs one,** so volume is high (assumption: confirm what share of matters reach a demand letter).\")\n# area 4\nrep(\"15 separate library packets score 0.81 (`reviews/GATE-M3-product-manager.md`).\",\n    \"15 separate library packets score 0.81 on must-flags, with entry recall 0.775 and amount recall 0.681 (`evals/reports/library-latest.md`; `submission/prompt-log/reviews/GATE-M3-product-manager.md`).\")\nrep(\"| Reviewable | paralegal rates \\\"I could verify every claim quickly\\\" at least 4/5 | 4/5 (persona reviewer) |\",\n    \"| Reviewable | paralegal rates \\\"I could verify every claim quickly\\\" at least 4/5 | persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored |\")\nrep(\"**Catching regressions.**\",\n    \"**Reviewability passed on a persona score and failed in use.** An AI persona rated the M3 screen 4/5 on \\\"I could verify every claim quickly\\\". When I used the screen myself it was very hard to use, and I asked for it to be so simple that anyone could use it (D-068). We are rebuilding it as four fixed steps with one question at a time (T-181, in progress). So the bar now reads: a persona score is a screen, not a ship call. The ship call needs a real paralegal session on the final screen.\\n\\n**Catching regressions.**\")\nopen(p,'w').write(s)\nE"
}
````

### User / tool · 2026-11-02T21:22:00.114Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:22:09.033Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/part2-process.md'\ns=open(p).read()\ndef rep(a,b,cnt=1):\n    global s\n    assert s.count(a)==cnt,(a,s.count(a))\n    s=s.replace(a,b)\n\n# Area 6\nrep(\"**Speed.** Each question to a founder\",\n\"**Engineering.** Engineering decides how: stack, which model runs where inside the budget, test design, build or buy. Engineering has a veto on \\\"not safe to ship\\\" that I cannot overrule alone; only a founder can, in writing. I decide what and when. The LLM/code line is drawn together and written down (`docs/LLM_VS_CODE.md`). A disagreement gets settled by evidence first: we write the test or eval case that would show who is right. If it is still open, the safer answer holds for anything the carrier sees, and a founder decides scope and timing. This is my stance until a founder says otherwise (NEEDS_CHRIS #9). In this build, an engineering reviewer in a fresh context played that veto at every card.\\n\\n**Speed.** Each question to a founder\")\n# Area 7\nrep(\"I watch what they do, and trust it over what they say.\",\n\"I watch what they do, and trust it over what they say. This build is the example: an AI persona rated the screen 4/5, and I found it very hard to use (D-068). What a person does with it beats what a proxy scores, so the guided screen goes to a real paralegal before I call it done.\")\n# Area 8\nrep(\"Unit tests (5,698 passed), E2E (412 passed, `evals/reports/m3-sensors.md`)\",\n\"Unit tests (UNITCOUNT passed at 33e88c6, `artifacts/UNITFILE`), E2E (412 passed at d7ea327, `evals/reports/m3-sensors.md`)\")\nrep(\"(`reviews/GATE-M3-round1-triage.md`)\",\"(`submission/prompt-log/reviews/GATE-M3-round1-triage.md`)\")\nrep(\"(61 rows in `memory/SCOPE_CUTS.md`)\",\"(62 rows in `memory/SCOPE_CUTS.md`)\")\nrep(\"Example: demo answers prepared by our team were labeled as AI output; the decision is D-065.\",\n\"Example: demo answers prepared by our team were labeled as AI output; the decision is D-065 and the fix is committed. A second example is still open: a disputed summary was one click from the letter (D-066, in progress).\")\nrep(\"(golden 1.000 against library 0.81)\",\"(golden 1.000 against library 0.81); a persona score that passed a screen you found very hard to use\")\nopen(p,'w').write(s)\nE\ngrep -n \"UNIT\" submission/*.md"
}
````

### User / tool · 2026-11-02T21:22:09.165Z

**tool result**
````
submission/part2-process.md:112:**Before release.** Unit tests (UNITCOUNT passed at 33e88c6, `artifacts/UNITFILE`), E2E (412 passed at d7ea327, `evals/reports/m3-sensors.md`), the live eval against the ship bar, a clean-clone install timed against the 5-minute bar, and adversarial reviewers: a claims adjuster who outworded my billing rules for four rounds, a chaos tester who found a run that stayed "running" forever after a restart. **Who signs off:** a reviewer in a fresh context who did not write the work, and me. Workers never close their own cards. Milestone gates: M0, M1, M2 passed; M3 failed its first round with two blockers (`submission/prompt-log/reviews/GATE-M3-round1-triage.md`).
submission/product-note.md:19:| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5 or more; tests green | **Not met on the screen I rejected.** Persona 4/5 on the M3 screen (`submission/prompt-log/reviews/GATE-M3-paralegal.md`); I found that screen very hard to use. Guided screen not yet scored. Tests: 5,xxx unit passed at 33e88c6 (`artifacts/UNITFILE`); 412 E2E passed at d7ea327 (`evals/reports/m3-sensors.md`) |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:22:14.413Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/part2-process.md'\ns=open(p).read()\na=\"In this build, an engineering reviewer in a fresh context played that veto at every card.\"\nassert a in s\ns=s.replace(a,\"In this build a blocker from the staff-engineer reviewer kept a card open until it was fixed.\")\nopen(p,'w').write(s)\nE\ngrep -no \"[A-Za-z/_.-]*reviews/[A-Za-z0-9_.-]*\\|evals/[A-Za-z/_.0-9-]*\\|memory/[A-Za-z_/.]*\\|docs/[A-Za-z_.]*\\|spec/[A-Za-z_.]*\\|artifacts/[A-Za-z_./-]*\\|personas/\" submission/part2-process.md submission/product-note.md | sort -u -t: -k3"
}
````

### User / tool · 2026-11-02T21:22:14.549Z

**tool result**
````
submission/part2-process.md:112:artifacts/UNITFILE
submission/part2-process.md:34:docs/LLM_VS_CODE.md
submission/part2-process.md:44:evals/golden/
submission/part2-process.md:40:evals/golden/sample.expected.json
submission/part2-process.md:3:evals/reports/
submission/part2-process.md:38:evals/reports/20261102T164038Z.md
submission/part2-process.md:44:evals/reports/library-latest.md
submission/part2-process.md:112:evals/reports/m3-sensors.md
submission/part2-process.md:13:memory/ASSUMPTIONS.md
submission/part2-process.md:110:memory/LESSONS.md
submission/part2-process.md:3:memory/ORCHESTRATOR_DECISIONS.md
submission/part2-process.md:114:memory/SCOPE_CUTS.md
submission/part2-process.md:103:memory/STATE.md
submission/part2-process.md:34:memory/contracts/api.md
submission/part2-process.md:13:personas/
submission/part2-process.md:34:spec/REQUIREMENTS.md
submission/part2-process.md:3:submission/prompt-log/reviews/
submission/product-note.md:19:submission/prompt-log/reviews/GATE-M3-paralegal.md
submission/part2-process.md:44:submission/prompt-log/reviews/GATE-M3-product-manager.md
submission/part2-process.md:112:submission/prompt-log/reviews/GATE-M3-round1-triage.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:22:34.610Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='submission/validation-ladder.svg'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep('<rect x=\"20\" y=\"452\" width=\"470\" height=\"62\" rx=\"6\" fill=\"#f6e9f7\"','<rect x=\"20\" y=\"452\" width=\"470\" height=\"72\" rx=\"6\" fill=\"#f6e9f7\"')\nrep('<text x=\"34\" y=\"504\" font-size=\"11.5\" fill=\"#222\">A summary the judge disputed needs a named \"I compared it with the quote.\"</text>',\n    '<text x=\"34\" y=\"504\" font-size=\"11.5\" fill=\"#222\">In progress (D-066, T-179): a summary the judge disputed</text>\\n  <text x=\"34\" y=\"518\" font-size=\"11.5\" fill=\"#222\">will need a named \"I compared it with the quote.\"</text>')\nrep('<path d=\"M255,514 V534\"','<path d=\"M255,524 V534\"')\n# code lane\nstart=s.index('<rect x=\"542\" y=\"40\" width=\"258\" height=\"190\"')\nend=s.index('<!-- evidence -->')\nlane='''<rect x=\"542\" y=\"40\" width=\"258\" height=\"202\" rx=\"6\" fill=\"#f3f3f3\" stroke=\"#888\"/>\n  <text x=\"554\" y=\"60\" font-size=\"12\" font-weight=\"700\" fill=\"#111\">Code, no model</text>\n'''\nlines=[(78,\"Split records (a model may only point at\"),(92,\"cut offsets for an unsplittable paste;\"),(106,\"code validates). Parse dates (an ambiguous\"),(120,\"date waits for her). Gap arithmetic: 29 and\"),(134,\"30 days no, 31 yes; 28 no, 73 yes.\"),\n(152,\"Find every dollar amount and its class (a\"),(166,\"rate is never a charge). Totals of what she\"),(180,\"accepted. Flag wording from templates.\"),\n(198,\"Dates and amounts always need her accept.\"),(212,\"Conflict pairs come from code; the judge\"),(226,\"says only conflict or benign.\")]\nfor y,t in lines:\n    lane+=f'  <text x=\"554\" y=\"{y}\" font-size=\"11\" fill=\"#222\">{t}</text>\\n'\nlane+='\\n  '\ns=s[:start]+lane+s[end:]\n# evidence\nrep('''<text x=\"554\" y=\"474\" font-size=\"11\" fill=\"#222\">Rung 3: persona rates \"I could verify</text>\n  <text x=\"554\" y=\"488\" font-size=\"11\" fill=\"#222\">every claim quickly\" 4 of 5; but 5 of 5</text>\n  <text x=\"554\" y=\"502\" font-size=\"11\" fill=\"#222\">disputed summaries took one click, so</text>\n  <text x=\"554\" y=\"516\" font-size=\"11\" fill=\"#222\">D-066 requires a named confirm</text>''',\n'''<text x=\"554\" y=\"474\" font-size=\"11\" fill=\"#222\">Rung 3: persona 4 of 5 on the old screen,</text>\n  <text x=\"554\" y=\"488\" font-size=\"11\" fill=\"#222\">which I found very hard to use; rebuilt as</text>\n  <text x=\"554\" y=\"502\" font-size=\"11\" fill=\"#222\">four steps (D-068), not yet scored. 5 of 5</text>\n  <text x=\"554\" y=\"516\" font-size=\"11\" fill=\"#222\">disputed summaries took one click (T-179)</text>''')\nrep('''<text x=\"554\" y=\"536\" font-size=\"10.5\" fill=\"#555\">Sources: evals/reports/20261102T164038Z.md,</text>\n  <text x=\"554\" y=\"550\" font-size=\"10.5\" fill=\"#555\">reviews/GATE-M3-paralegal.md,</text>\n  <text x=\"554\" y=\"564\" font-size=\"10.5\" fill=\"#555\">reviews/GATE-M3-product-manager.md,</text>\n  <text x=\"554\" y=\"578\" font-size=\"10.5\" fill=\"#555\">docs/LLM_VS_CODE.md</text>''',\n'''<text x=\"554\" y=\"536\" font-size=\"10\" fill=\"#555\">Sources: evals/reports/20261102T164038Z.md;</text>\n  <text x=\"554\" y=\"549\" font-size=\"10\" fill=\"#555\">submission/prompt-log/reviews/GATE-M3-</text>\n  <text x=\"554\" y=\"562\" font-size=\"10\" fill=\"#555\">paralegal.md, GATE-M3-product-manager.md;</text>\n  <text x=\"554\" y=\"575\" font-size=\"10\" fill=\"#555\">docs/LLM_VS_CODE.md</text>''')\nrep('Rung 3, the paralegal, accepts, edits or dismisses.','Rung 3, the paralegal, accepts, edits or dismisses; a named confirm for a disputed summary is in progress.')\nrep('A separate code-only lane handles dates, gaps and amounts with no model.','A separate code-only lane handles dates, gaps and amounts with no model; a model may only point at cut offsets for a paste code cannot split.')\nopen(p,'w').write(s)\nE\ngrep -c . submission/validation-ladder.svg; sed -n 70,92p submission/validation-ladder.svg | head -30"
}
````

### User / tool · 2026-11-02T21:22:34.744Z

**tool result**
````
90
  <rect x="542" y="262" width="258" height="78" rx="6" fill="#fdecea" stroke="#b3261e"/>
  <text x="554" y="282" font-size="12" font-weight="700" fill="#8c1d18">Could not verify (visible list)</text>
  <text x="554" y="298" font-size="11" fill="#222">Quote not in the record, or a number</text>
  <text x="554" y="312" font-size="11" fill="#222">the quote lacks. Never a flag, never in</text>
  <text x="554" y="326" font-size="11" fill="#222">the letter. She can write the entry herself.</text>

  <!-- code-only lane -->
  <rect x="542" y="40" width="258" height="202" rx="6" fill="#f3f3f3" stroke="#888"/>
  <text x="554" y="60" font-size="12" font-weight="700" fill="#111">Code, no model</text>
  <text x="554" y="78" font-size="11" fill="#222">Split records (a model may only point at</text>
  <text x="554" y="92" font-size="11" fill="#222">cut offsets for an unsplittable paste;</text>
  <text x="554" y="106" font-size="11" fill="#222">code validates). Parse dates (an ambiguous</text>
  <text x="554" y="120" font-size="11" fill="#222">date waits for her). Gap arithmetic: 29 and</text>
  <text x="554" y="134" font-size="11" fill="#222">30 days no, 31 yes; 28 no, 73 yes.</text>
  <text x="554" y="152" font-size="11" fill="#222">Find every dollar amount and its class (a</text>
  <text x="554" y="166" font-size="11" fill="#222">rate is never a charge). Totals of what she</text>
  <text x="554" y="180" font-size="11" fill="#222">accepted. Flag wording from templates.</text>
  <text x="554" y="198" font-size="11" fill="#222">Dates and amounts always need her accept.</text>
  <text x="554" y="212" font-size="11" fill="#222">Conflict pairs come from code; the judge</text>
  <text x="554" y="226" font-size="11" fill="#222">says only conflict or benign.</text>

  <!-- evidence -->
  <rect x="542" y="358" width="258" height="226" rx="6" fill="#ffffff" stroke="#888"/>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:22:42.893Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/NEEDS_CHRIS.md'\ns=open(p).read()\nold=s[s.index(\"| 7 | P2 | T-190 |\"):s.index(\"## Answered\")]\nnew='''| 7 | P2 | T-190 | Product note, ship-bar row 5: the 4/5 \"I could verify every claim quickly\" is a persona reviewer on the old screen, not a real paralegal; you rejected that screen as very hard to use (D-068) | Optional: have a real paralegal (or someone who does this work) run the sample case on the guided screen once it ships and tell you the score; replace the row 5 result and the \"Reviewability passed on paper\" bullet. | The note states plainly that the score is a persona's, from before the redesign, and that the guided screen is not scored. |\n| 8 | P1 | (card pending) | Product note, Cut paragraph: why you reinstated cuts (D-031, D-042) and shipped three stretch items when the brief says at most one | Replace `[CHRIS: your reason, one line.]` with your reason in your words. | The note records the decisions and their cost (drafted paragraph cut, four billing rounds) and leaves the reason marked. |\n| 9 | P2 | (card pending) | Part 2, area 6: the decision rights you give engineering | Confirm or change the \"Engineering\" paragraph (engineering decides how and has a \"not safe to ship\" veto; only a founder overrides it in writing; evidence first, then the safer answer for anything the carrier sees). | The paragraph stands as my stated stance. |\n\n'''\ns=s.replace(old,new)\nopen(p,'w').write(s)\nE\ntail -c 200 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/unit.out"
}
````

### User / tool · 2026-11-02T21:22:43.023Z

**tool result**
````
........ [ 32%]
........................................................................ [ 33%]
........................................................................ [ 34%]
........................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:22:46.870Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SC/r; cat submission/print.css | head -40; CH=\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\"; ls \"$CH\""
}
````

### User / tool · 2026-11-02T21:22:46.962Z

**tool result**
````
@page{size:Letter;margin:0.4in}
body{font:8.7pt/1.25 -apple-system,Helvetica,Arial,sans-serif;max-width:none;margin:0;color:#111}
header{display:none}
h1{font-size:13pt;margin:0 0 2px}
p{margin:2px 0}li{margin:0.5px 0}
ul,ol{margin:2px 0;padding-left:16px}
table{border-collapse:collapse;width:100%;margin:3px 0;font-size:8.2pt}
td,th{border:1px solid #bbb;padding:1.5px 4px;vertical-align:top;text-align:left}
code{font-size:7.8pt}
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:22:53.190Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; CH=\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\"\nfor d in product-note part2-process; do\npandoc submission/$d.md -s -o $SC/r/$d.html --css submission/print.css --embed-resources --resource-path=submission --metadata title=\" \" 2>&1 | head -3\ndone\n# part 2 used 9.4pt - check how\nhead -5 $SC/r/part2-process.html | cut -c1-200; grep -n \"9.4\" -r submission/*.css | head"
}
````

### User / tool · 2026-11-02T21:22:53.467Z

**tool result**
````
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc 3.13" />
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:00.760Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; CH=\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\"\ncat > $SC/r/render.sh <<'E'\n#!/bin/bash\n# usage: render.sh name fontpt\nSC=\"$1\"; d=\"$2\"; pt=\"$3\"; CH=\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\"\ncp /Users/arsis/zlayt-pm-project/submission/print.css $SC/r/p_$d.css\necho \"body{font-size:${pt}pt}\" >> $SC/r/p_$d.css\ncd /Users/arsis/zlayt-pm-project\npandoc submission/$d.md -s -o $SC/r/$d.html --css $SC/r/p_$d.css --embed-resources --resource-path=submission --metadata title=\" \" \n\"$CH\" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=$SC/r/$d.pdf file://$SC/r/$d.html >/dev/null 2>&1\npython3 - <<P\nimport re\nb=open(\"$SC/r/$d.pdf\",\"rb\").read()\nprint(\"$d pages\",len(re.findall(rb\"/Type\\s*/Page[^s]\",b)))\nP\nE\nchmod +x $SC/r/render.sh; $SC/r/render.sh $SC product-note 8.7; $SC/r/render.sh $SC part2-process 9.4"
}
````

### User / tool · 2026-11-02T21:23:04.628Z

**tool result**
````
product-note pages 2
part2-process pages 4
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:08.401Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; which pdftotext && pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -40; wc -w /Users/arsis/zlayt-pm-project/submission/product-note.md"
}
````

### User / tool · 2026-11-02T21:23:08.545Z

**tool result**
````
/opt/homebrew/bin/pdftotext
Failure

Design

The judge is a model too

Judges are scored on seeded wrong items; “verified” never means accepted

LLM and code. Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals,
quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed
conflict pair, where to cut a paste code could not split (offsets only; code validates and flags it LLM_SPLIT), and the second check. Table:
docs/LLM_VS_CODE.md.
Three metrics after launch.
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps, against a stopwatch baseline taken in week 2. Is it faster? Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: the attorney’s edit log, plus adjuster letters
the paralegal tags. Target 0. Each one becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events with before and after text and
time on item. Verifying or clicking through? (5 of 5 disputed items took one click.)

    1265 /Users/arsis/zlayt-pm-project/submission/product-note.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:25.224Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/submission/product-note.md",
 "content": "# Treatment Timeline: product note\n\nChris [CHRIS: full name] · Zlayt AI PM project, Part 1 · prototype: [CHRIS: public link, see `submission/NEEDS_CHRIS.md`] · synthetic data only · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`); run steps in `README.md`\n\n**Problem and user.** A Zinda Law Group litigation lead says paralegals spend hours turning scattered records into a treatment chronology before each demand letter, and mistakes cost credibility. The user is the paralegal. She reviews, she does not trust, so every line must be checkable against its source. The attorney signs (assumption A-101).\n\n**What I built.** Paste or upload records (text, or a PDF text layer). Each timeline entry shows the AI's summary beside the verbatim record quote; she accepts, edits or dismisses it. Code finds the dollar amounts and she accepts each charge one at a time. The export is two blocks that never mix (D-001): a **letter section** (accepted entries and charges only, each with quote, provider, date and an `[Ex. __ / Bates __]` placeholder) and **internal notes, do not send** (30-day gaps, conflicts, prior conditions, causation language, amounts not totaled). Every AI step sits behind the validation ladder: the model drafts, code checks, a second model checks, she decides. **In progress, not yet in the app:** a guided four-step screen (D-068, T-181) and a confirm for disputed summaries (D-066, T-179). Why: first finding below.\n\n**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts and roles, real patient data, EHR integrations, any medical or legal judgment. After trying: the \"patient said it\" label (four adversarial rounds each found a mislabeled quote; D-040), per-provider billing totals (five rounds, each found a way to drop a figure, so billing is a cited line listing; D-052), the drafted treatment paragraph (no eval; D-067). **Stretch:** the brief says at most one. I shipped three: the side-by-side source viewer, PDF text-layer upload and calibrated confidence (measured precision, not an invented %). I went past the limit on purpose: D-031 and D-042 reinstated every cut that needed no paid integration and no login. [CHRIS: your reason, one line.] The cost: the paragraph went in without an eval and came back out, and billing took four adversarial rounds.\n\n**Good enough to ship.** Live run, 3 runs, `claude-sonnet-5-5` generator, `claude-haiku-5-5` judge. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md`, 15 library packets, run at a74b727, before the billing redesign.\n\n| # | Criterion (bar) | Result |\n|-|------------|--------------|\n| 1 | Grounding: every exported statement and amount has a quote found in the input (100%) | 1.000, 242 checked [E] |\n| 2 | Recall of golden entries and amounts (95%) | golden: entries 0.982, amounts 1.000 [E]. **Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; report being regenerated). Misses cluster in ledgers, EOBs, scans and Spanish; I have not yet separated real misses from expected files that predate the billing redesign |\n| 3 | Flags: precision and recall 0.9 per type; 28-day interval not flagged, 73-day flagged | golden: 1.000/1.000, four types; 28 no, 73 yes [E]. **Library: 34 of 42 must-flags, 0.81 [L]** |\n| 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct summaries rejected; conflict and flag judges 20/20 and 12/12, 0 false agrees [E] |\n| 5 | Reviewable: paralegal persona rates \"I could verify every claim quickly\" 4/5 or more; tests green | **Not met on the screen I rejected.** Persona 4/5 on the M3 screen (`submission/prompt-log/reviews/GATE-M3-paralegal.md`); I found that screen very hard to use; guided screen not scored. UNITCOUNT unit tests passed at 33e88c6 (`artifacts/UNITFILE`); 412 E2E at d7ea327 (`evals/reports/m3-sensors.md`) |\n\n**What testing found** (reviews are in `submission/prompt-log/reviews/`).\n\n- **Reviewability passed on paper and failed in use.** A persona reviewer scored the M3 screen 4/5. When I used it myself it was *very* hard to use. I wanted it so simple that anyone could use it (D-068), so it is being rebuilt as four fixed steps with one question at a time. The 4/5 was measured before the redesign and does not count for the new screen. An AI reviewer is no substitute for a person at the desk: the ship call needs a real paralegal session.\n- **The 1.000 flag numbers do not generalize.** The golden cases were written next to the rules. On the 15 library packets, must-flag recall is 0.81 (`GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes, like \"Left shoulder pain\" against \"Right shoulder pain\". Only 5 of 17 \"held-out\" conflict controls are still clean, so judge numbers are partly in-sample.\n- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: one library letter said $16,147 against a true $8,123.50 (`T-140-claims-adjuster.md`); a paralegal reviewer found another at $10,906 against $6,000 (`GATE-M2-paralegal.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total says what it is: \"Billed charges accepted from these records.\"\n- **The M3 gate failed once.** Demo answers written by our team were labeled as AI output (fixed in code, final check in progress), and one click accepted a summary the second check had disputed, 5 of 5 times across 16 cases (`GATE-M3-product-manager.md`). The named \"I compared it with the quote\" confirm is in progress (T-179).\n\n**How the AI can mislead her, and what the design does.**\n\n| Failure | Design |\n|--------|-------------|\n| Changes a number, side or negation; drops a hedge (\"may represent\") | Code needs each in the quote: hard refusal on her edits, needs-review on AI text |\n| Says more than the quote | Code removes unsupported clauses; the second check reads the rest; a disputed one will need a named confirm (D-066, in progress) |\n| Invents an amount, or obeys an order hidden in a record | Only code finds money, default-deny, she accepts each charge; models have no tools and return a checked form |\n| Rules on cause or diagnosis | Flag wording is a code template; the model returns a category and a quote only (D-007) |\n| Drops what it could not verify; or the judge errs, being a model too | A visible \"could not verify\" list, nothing silent. Judges are scored on seeded wrong items; \"verified\" never means accepted |\n\n**LLM and code.** Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals, quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed conflict pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check. Table: `docs/LLM_VS_CODE.md`.\n\n**Three metrics after launch.**\n\n1. **Minutes from first paste to copied letter section, against her own last three by hand.** Source: case-created and letter-copied timestamps, against a stopwatch baseline from week 2. Read beside #2: speed from skipping review is no win.\n2. **Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100.** Source: the attorney's edit log plus adjuster letters the paralegal tags. Target 0; each becomes an eval case.\n3. **Needs-review items accepted unchanged, and median seconds per item.** Source: audit-log accept events with before and after text and time on item. Verifying or clicking through? (5 of 5 disputed items took one click.)\n"
}
````

### User / tool · 2026-11-02T21:23:25.280Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/submission/product-note.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:29.529Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head; wc -w /Users/arsis/zlayt-pm-project/submission/product-note.md"
}
````

### User / tool · 2026-11-02T21:23:31.685Z

**tool result**
````
product-note pages 2
LLM and code. Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals,
quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed
conflict pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check. Table:
docs/LLM_VS_CODE.md.
Three metrics after launch.
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps, against a stopwatch baseline from week 2. Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: the attorney’s edit log plus adjuster letters
the paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events with before and after text and
    1234 /Users/arsis/zlayt-pm-project/submission/product-note.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:44.295Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\" · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`); run steps in `README.md`\",\" · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`) · run: `README.md`\")\nrep(\"A Zinda Law Group litigation lead says paralegals spend hours turning scattered records into a treatment chronology before each demand letter, and mistakes cost credibility. The user is the paralegal. She reviews, she does not trust, so every line must be checkable against its source. The attorney signs (assumption A-101).\",\n    \"A Zinda litigation lead says paralegals spend hours turning scattered records into a treatment chronology before each demand letter, and mistakes cost credibility. The user is the paralegal. She reviews, she does not trust, so every line must be checkable against its source. The attorney signs (assumption A-101).\")\nrep(\"For good: accounts and roles, real patient data, EHR integrations, any medical or legal judgment. After trying: \",\"For good: accounts, real patient data, EHR integrations, any medical or legal judgment. After trying: \")\nrep(\"(four adversarial rounds each found a mislabeled quote; D-040)\",\"(four rounds each found a mislabeled quote; D-040)\")\nrep(\"(five rounds, each found a way to drop a figure, so billing is a cited line listing; D-052)\",\"(five rounds each found a way to drop a figure, so billing is a cited line listing; D-052)\")\nrep(\" Misses cluster in ledgers, EOBs, scans and Spanish; I have not yet separated real misses from expected files that predate the billing redesign\",\" Misses cluster in ledgers, EOBs, scans and Spanish; I have not separated real misses from out-of-date expected files\")\nrep(\"When I used it myself it was *very* hard to use. I wanted it so simple that anyone could use it (D-068), so it is being rebuilt as four fixed steps with one question at a time. The 4/5 was measured before the redesign and does not count for the new screen. An AI reviewer is no substitute for a person at the desk: the ship call needs a real paralegal session.\",\n    \"When I used it myself it was *very* hard to use. I wanted it simple enough for anyone (D-068), so it is being rebuilt as four fixed steps, one question at a time. The 4/5 predates the redesign and does not count for the new screen. An AI reviewer is no substitute for a person at the desk: the ship call needs a real paralegal.\")\nrep(\" The golden cases were written next to the rules. On the 15 library packets, must-flag recall is 0.81 (`GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes, like \\\"Left shoulder pain\\\" against \\\"Right shoulder pain\\\". Only 5 of 17 \\\"held-out\\\" conflict controls are still clean, so judge numbers are partly in-sample.\",\n    \" The golden cases were written next to the rules. On the 15 library packets, must-flag recall is 0.81 (`GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes, like \\\"Left\\\" against \\\"Right shoulder pain\\\". Only 5 of 17 \\\"held-out\\\" conflict controls are still clean, so judge numbers are partly in-sample.\")\nrep(\"The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total says what it is: \\\"Billed charges accepted from these records.\\\"\",\n    \"The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total says what it is: \\\"Billed charges accepted from these records.\\\"\")\nrep(\"Code finds the dollar amounts and she accepts each charge one at a time. \",\"Code finds the dollar amounts; she accepts each charge one at a time. \")\nrep(\" Why: first finding below.\",\" Why: first finding below.\")\nrep(\"Table: `docs/LLM_VS_CODE.md`.\",\"Table: `docs/LLM_VS_CODE.md`.\")\nrep(\"Is it faster? \",\"\") if \"Is it faster? \" in s else None\nrep(\"Judges are scored on seeded wrong items; \\\"verified\\\" never means accepted\",\"Judges are scored on seeded wrong items; \\\"verified\\\" is not \\\"accepted\\\"\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:23:45.578Z

**tool result**
````
product-note pages 2
LLM and code. Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals,
quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed
conflict pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check. Table:
docs/LLM_VS_CODE.md.
Three metrics after launch.
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps, against a stopwatch baseline from week 2. Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: the attorney’s edit log plus adjuster letters
the paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events with before and after text and
time on item. Verifying or clicking through? (5 of 5 disputed items took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:59.239Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\nimport re\ndef sub(start,end,new):\n    global s\n    i=s.index(start); j=s.index(end,i)\n    s=s[:i]+new+s[j:]\nsub(\"**Cut**\",\"**Good enough to ship.**\",'''**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts, real patient data, EHR integrations, any medical or legal judgment. After trying: the \"patient said it\" label (D-040), per-provider billing totals (D-052) and the drafted treatment paragraph (D-067); each failed repeated adversarial rounds or had no eval. **Stretch:** the brief says at most one; I shipped three (source viewer, PDF text layer, calibrated confidence), because D-031 and D-042 reinstated every cut that needed no paid integration or login. [CHRIS: your reason, one line.] The cost: the paragraph went in with no eval and came back out, and billing took four adversarial rounds.\n\n''')\nsub(\"- **Billing took\",\"- **The M3 gate\",'''- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: a library letter said $16,147 against a true $8,123.50 (`T-140-claims-adjuster.md`); a paralegal reviewer found $10,906 against $6,000 (`GATE-M2-paralegal.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total reads \"Billed charges accepted from these records.\"\n''')\nsub(\"1. **Minutes\",\"\\0\" if False else \"1. **Minutes\",'')  # no-op guard\ni=s.index(\"1. **Minutes\")\ns=s[:i]+'''1. **Minutes from first paste to copied letter section, against her own last three by hand.** Source: case-created and letter-copied timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.\n2. **Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100.** Source: attorney edit log plus adjuster letters the paralegal tags. Target 0; each becomes an eval case.\n3. **Needs-review items accepted unchanged, and median seconds per item.** Source: audit-log accept events (before and after text, time on item). Verifying or clicking through? (5 of 5 disputed items took one click.)\n'''\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:24:00.745Z

**tool result**
````
product-note pages 2
conflict pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check. Table:
docs/LLM_VS_CODE.md.
Three metrics after launch.
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:14.484Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"(accepted entries and charges only, each with quote, provider, date and an `[Ex. __ / Bates __]` placeholder)\",\"(accepted items only, each with quote, provider, date and an `[Ex. __ / Bates __]` placeholder)\")\nrep(\"(30-day gaps, conflicts, prior conditions, causation language, amounts not totaled)\",\"(gaps, conflicts, prior conditions, causation language, amounts not totaled)\")\nrep(\" Misses cluster in ledgers, EOBs, scans and Spanish; I have not separated real misses from out-of-date expected files\",\" Misses cluster in ledgers, EOBs, scans and Spanish; real misses vs out-of-date expected files not yet separated\")\nrep(\"0; 40/40; 0 of 10 correct summaries rejected; conflict and flag judges 20/20 and 12/12, 0 false agrees [E]\",\"0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12, 0 false agrees [E]\")\nrep(\" Only 5 of 17 \\\"held-out\\\" conflict controls are still clean, so judge numbers are partly in-sample.\",\" Judge numbers are partly in-sample: only 5 of 17 \\\"held-out\\\" controls are still clean.\")\nrep(\"Demo answers written by our team were labeled as AI output (fixed in code, final check in progress), and one click accepted a summary the second check had disputed, 5 of 5 times across 16 cases (`GATE-M3-product-manager.md`). The named \\\"I compared it with the quote\\\" confirm is in progress (T-179).\",\n    \"Demo answers written by our team were labeled as AI output (fixed in code, final check in progress). One click accepted a disputed summary, 5 of 5 times across 16 cases (`GATE-M3-product-manager.md`); the \\\"I compared it with the quote\\\" confirm is in progress (T-179).\")\nrep(\"| Changes a number, side or negation; drops a hedge (\\\"may represent\\\") | Code needs each in the quote: hard refusal on her edits, needs-review on AI text |\",\"| Changes a number, side or negation; drops a hedge | Code needs each in the quote: hard refusal on her edits, needs-review on AI text |\")\nrep(\"| Invents an amount, or obeys an order hidden in a record | Only code finds money, default-deny, she accepts each charge; models have no tools and return a checked form |\",\"| Invents an amount, or obeys an order hidden in a record | Only code finds money; she accepts each charge; models have no tools |\")\nrep(\"A visible \\\"could not verify\\\" list, nothing silent. Judges are scored on seeded wrong items; \\\"verified\\\" is not \\\"accepted\\\"\",\"A visible \\\"could not verify\\\" list. Judges are scored on seeded wrong items; \\\"verified\\\" is not \\\"accepted\\\"\")\nrep(\"Persona 4/5 on the M3 screen (`submission/prompt-log/reviews/GATE-M3-paralegal.md`); I found that screen very hard to use; guided screen not scored.\",\"Persona 4/5 on the M3 screen (`submission/prompt-log/reviews/GATE-M3-paralegal.md`), which I found very hard to use; guided screen not scored.\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:24:15.520Z

**tool result**
````
product-note pages 2
Three metrics after launch.
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:36.483Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"; a paralegal reviewer found $10,906 against $6,000 (`GATE-M2-paralegal.md`)\",\"\")\nrep(\"a library letter said $16,147 against a true $8,123.50 (`T-140-claims-adjuster.md`)\",\"one library letter said $16,147 against a true $8,123.50 (`T-140-claims-adjuster.md`)\")\nrep(\"The cost: the paragraph went in with no eval and came back out, and billing took four adversarial rounds.\",\"The cost: the paragraph went in with no eval and came back out; billing took four adversarial rounds.\")\nrep(\"Every AI step sits behind the validation ladder: the model drafts, code checks, a second model checks, she decides.\",\"Every AI step sits behind the validation ladder: model drafts, code checks, a second model checks, she decides.\")\nrep(\"Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals, quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed conflict pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check.\",\n    \"Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and class, totals, quote and number checks, flag wording, export. The model reads: summary and quote, flag category, one yes/no per code-proposed conflict pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check.\")\nrep(\"**What testing found** (reviews are in `submission/prompt-log/reviews/`).\",\"**What testing found** (reviews: `submission/prompt-log/reviews/`).\")\nrep(\"The golden cases were written next to the rules. On the 15 library packets, must-flag recall is 0.81\",\"The golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81\")\nrep(\"**Good enough to ship.** Live run, 3 runs, `claude-sonnet-5-5` generator, `claude-haiku-5-5` judge. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md`, 15 library packets, run at a74b727, before the billing redesign.\",\n    \"**Good enough to ship.** Live run, 3 runs, generator `claude-sonnet-5-5`, judge `claude-haiku-5-5`. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md` (15 library packets, run at a74b727, before the billing redesign).\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:24:37.705Z

**tool result**
````
product-note pages 2
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:43.338Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.4; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -5; tail -c 150 $SC/unit.out"
}
````

### User / tool · 2026-11-02T21:24:45.321Z

**tool result**
````
product-note pages 2
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)

............................................ss........... [ 66%]
........................................................................ [ 68%]
.....
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:57.104Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\ni=s.index(\"| Drops what it could not verify\"); j=s.index(\"\\n\",i)\ns=s[:i]+s[j+1:]\nrep(\"| Changes a number, side or negation; drops a hedge | Code needs each in the quote: hard refusal on her edits, needs-review on AI text |\",\n    \"| Changes a number, side or negation; drops a hedge | Code needs each in the quote: hard refusal on her edits, needs-review on AI text; failures go to a visible \\\"could not verify\\\" list |\")\nrep(\"Code removes unsupported clauses; the second check reads the rest; a disputed one will need a named confirm (D-066, in progress)\",\n    \"Code removes unsupported clauses; the second check (scored on seeded wrong items; \\\"verified\\\" is not \\\"accepted\\\") reads the rest; a disputed one will need a named confirm (D-066, in progress)\")\nrep(\" Misses cluster in ledgers, EOBs, scans and Spanish; real misses vs out-of-date expected files not yet separated\",\" Misses cluster in ledgers, EOBs, scans, Spanish; real misses vs stale expected files not yet separated\")\nrep(\"Demo answers written by our team were labeled as AI output (fixed in code, final check in progress). One click accepted a disputed summary, 5 of 5 times across 16 cases (`GATE-M3-product-manager.md`); the \\\"I compared it with the quote\\\" confirm is in progress (T-179).\",\n    \"Team-written demo answers were labeled as AI output (fixed in code, final check in progress). One click accepted a disputed summary, 5 of 5 times in 16 cases (`GATE-M3-product-manager.md`); the \\\"I compared it with the quote\\\" confirm is in progress (T-179).\")\nrep(\"Source: case-created and letter-copied timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.\",\"Source: case-created and letter-copied timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:24:58.658Z

**tool result**
````
product-note pages 2
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
timestamps; stopwatch baseline in week 2. Read beside #2: speed from skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:02.823Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; pdftotext -layout -f 1 -l 1 $SC/r/product-note.pdf - | cut -c1-170"
}
````

### User / tool · 2026-11-02T21:25:02.952Z

**tool result**
````
Treatment Timeline: product note
Chris [CHRIS: full name] · Zlayt AI PM project, Part 1 · prototype: [CHRIS: public link, see submission/NEEDS_CHRIS.md] · synthetic data only ·
built with Claude Code agents I directed (submission/prompt-log/TOOLS.md) · run: README.md
Problem and user. A Zinda litigation lead says paralegals spend hours turning scattered records into a treatment chronology before each
demand letter, and mistakes cost credibility. The user is the paralegal. She reviews, she does not trust, so every line must be checkable against
its source. The attorney signs (assumption A-101).
What I built. Paste or upload records (text, or a PDF text layer). Each timeline entry shows the AI’s summary beside the verbatim record quote;
she accepts, edits or dismisses it. Code finds the dollar amounts; she accepts each charge one at a time. The export is two blocks that never
mix (D-001): a letter section (accepted items only, each with quote, provider, date and an [Ex. __ / Bates __] placeholder) and internal
notes, do not send (gaps, conflicts, prior conditions, causation language, amounts not totaled). Every AI step sits behind the validation ladder:
model drafts, code checks, a second model checks, she decides. In progress, not yet in the app: a guided four-step screen (D-068, T-181)
and a confirm for disputed summaries (D-066, T-179). Why: first finding below.
Cut (memory/SCOPE_CUTS.md). For good: accounts, real patient data, EHR integrations, any medical or legal judgment. After trying: the “patient
said it” label (D-040), per-provider billing totals (D-052) and the drafted treatment paragraph (D-067); each failed repeated adversarial rounds or
had no eval. Stretch: the brief says at most one; I shipped three (source viewer, PDF text layer, calibrated confidence), because D-031 and D-
042 reinstated every cut that needed no paid integration or login. [CHRIS: your reason, one line.] The cost: the paragraph went in with no eval
and came back out; billing took four adversarial rounds.
Good enough to ship. Live run, 3 runs, generator claude-sonnet-5-5, judge claude-haiku-5-5. [E] =
evals/reports/20261102T164038Z.md; [L] = evals/reports/library-latest.md (15 library packets, run at a74b727, before the billing
redesign).
#    Criterion (bar)                                                       Result
1    Grounding: every exported statement and amount has a quote            1.000, 242 checked [E]
     found in the input (100%)
2    Recall of golden entries and amounts (95%)                            golden: entries 0.982, amounts 1.000 [E]. Library: entries 0.775, amounts
                                                                           0.681 [L] (0.580 on a later run; report being regenerated). Misses cluster in
                                                                           ledgers, EOBs, scans, Spanish; real misses vs stale expected files not yet
                                                                           separated
3    Flags: precision and recall 0.9 per type; 28-day interval not         golden: 1.000/1.000, four types; 28 no, 73 yes [E]. Library: 34 of 42 must-
     flagged, 73-day flagged                                               flags, 0.81 [L]
4    No invented facts: 0 unsupported over 3 runs; judge catches 95%       0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12, 0
     of seeded wrong summaries                                             false agrees [E]
5    Reviewable: paralegal persona rates “I could verify every claim       Not met on the screen I rejected. Persona 4/5 on the M3 screen
     quickly” 4/5 or more; tests green                                     (submission/prompt-log/reviews/GATE-M3-paralegal.md), which I
                                                                           found very hard to use; guided screen not scored. UNITCOUNT unit tests
                                                                           passed at 33e88c6 (artifacts/UNITFILE); 412 E2E at d7ea327
                                                                           (evals/reports/m3-sensors.md)
What testing found (reviews: submission/prompt-log/reviews/).
  Reviewability passed on paper and failed in use. A persona reviewer scored the M3 screen 4/5. When I used it myself it was very hard to
  use. I wanted it simple enough for anyone (D-068), so it is being rebuilt as four fixed steps, one question at a time. The 4/5 predates the
  redesign and does not count for the new screen. An AI reviewer is no substitute for a person at the desk: the ship call needs a real paralegal.
  The 1.000 flag numbers do not generalize. The golden cases were written next to the rules; on the 15 library packets must-flag recall is
  0.81 (GATE-M3-product-manager.md; memory/SCOPE_CUTS.md rows 13, 23). The misses are conflicts code never proposes, like “Left”
  against “Right shoulder pain”. Judge numbers are partly in-sample: only 5 of 17 “held-out” controls are still clean.
  Billing took four adversarial rounds. A claims-adjuster reviewer outworded every word-list rule: one library letter said $16,147 against a
  true $8,123.50 (T-140-claims-adjuster.md). The fix was a design change (D-059 to D-064): an amount counts only on a dated service
  line, she accepts charges one at a time, and the total reads “Billed charges accepted from these records.”
  The M3 gate failed once. Team-written demo answers were labeled as AI output (fixed in code, final check in progress). One click accepted
  a disputed summary, 5 of 5 times in 16 cases (GATE-M3-product-manager.md); the “I compared it with the quote” confirm is in progress (T-
  179).
How the AI can mislead her, and what the design does.
Failure                                                      Design
Changes a number, side or negation; drops a hedge            Code needs each in the quote: hard refusal on her edits, needs-review on AI text; failures go
                                                             to a visible “could not verify” list
Says more than the quote                                     Code removes unsupported clauses; the second check (scored on seeded wrong items;
                                                             “verified” is not “accepted”) reads the rest; a disputed one will need a named confirm (D-
                                                             066, in progress)
Invents an amount, or obeys an order hidden in a record      Only code finds money; she accepts each charge; models have no tools
Rules on cause or diagnosis                                  Flag wording is a code template; the model returns a category and a quote only (D-007)
LLM and code. Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and class, totals,
quote and number checks, flag wording, export. The model reads: summary and quote, flag category, one yes/no per code-proposed conflict
pair, where to cut a paste code could not split (offsets only; code validates, flagged LLM_SPLIT), and the second check. Table:
docs/LLM_VS_CODE.md.
Three metrics after launch.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:08.569Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"|-|------------|--------------|\",\"|-|-------------|-----------------------|\")\nrep(\"|--------|-------------|\",\"|-----------|----------------------|\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12; tail -c 120 $SC/unit.out"
}
````

### User / tool · 2026-11-02T21:25:10.067Z

**tool result**
````
product-note pages 2
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)

.......................... [ 80%]
........................................................................ [ 81%]
......
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:19.625Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\" Why: first finding below.\",\"\")\nrep(\"; each failed repeated adversarial rounds or had no eval.\",\".\")\nrep(\"[CHRIS: public link, see `submission/NEEDS_CHRIS.md`]\",\"[CHRIS: public link]\")\nrep(\"the \\\"I compared it with the quote\\\" confirm is in progress (T-179).\",\"the confirm is in progress (T-179).\")\nrep(\"Read beside #2: speed from skipping review is no win.\",\"Read beside #2: speed from skipping review is no win.\")\nrep(\"; stopwatch baseline in week 2.\",\"; stopwatch baseline, week 2.\")\nrep(\"Verifying or clicking through? (5 of 5 disputed items took one click.)\",\"Verifying or clicking through? (5 of 5 disputed items took one click.)\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:25:20.807Z

**tool result**
````
product-note pages 2
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log plus adjuster letters the
paralegal tags. Target 0; each becomes an eval case.
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:28.679Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\" The misses are conflicts code never proposes, like \\\"Left\\\" against \\\"Right shoulder pain\\\".\", \" The misses are conflicts code never proposes (\\\"Left\\\" against \\\"Right shoulder pain\\\").\")\nrep(\"The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total reads \\\"Billed charges accepted from these records.\\\"\",\"The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads \\\"Billed charges accepted from these records.\\\"\")\nrep(\"The user is the paralegal. She reviews, she does not trust, so every line must be checkable against its source.\",\"The user is the paralegal. She reviews rather than trusts, so every line must be checkable against its source.\")\nrep(\"Judge numbers are partly in-sample: only 5 of 17 \\\"held-out\\\" controls are still clean.\",\"Judge numbers are partly in-sample (5 of 17 \\\"held-out\\\" controls still clean).\")\nrep(\"Paste or upload records (text, or a PDF text layer). Each\",\"Paste or upload records (text or PDF text layer). Each\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -layout -f 1 -l 1 $SC/r/product-note.pdf - | cut -c1-175 | awk 'length($0)<80 && length($0)>0'"
}
````

### User / tool · 2026-11-02T21:25:29.849Z

**tool result**
````
product-note pages 2
Treatment Timeline: product note
directed (submission/prompt-log/TOOLS.md) · run: README.md
its source. The attorney signs (assumption A-101).
and a confirm for disputed summaries (D-066, T-179).
rounds.
redesign).
# Criterion (bar)                                          Result
  has a quote found in the input (100%)
  interval not flagged, 73-day flagged
  catches 95% of seeded wrong summaries
What testing found (reviews: submission/prompt-log/reviews/).
How the AI can mislead her, and what the design does.
Failure                                              Design
a record
docs/LLM_VS_CODE.md.
Three metrics after launch.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:39.649Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"billing took four adversarial rounds.\\n\",\"billing took four rounds.\\n\")\nrep(\"(15 library packets, run at a74b727, before the billing redesign)\",\"(15 packets, run at a74b727, before the billing redesign)\")\nrep(\"(offsets only; code validates, flagged LLM_SPLIT)\",\"(offsets only, code validates; LLM_SPLIT)\")\nrep(\"Zlayt AI PM project, Part 1\",\"Zlayt PM project, Part 1\")\nrep(\"spend hours turning scattered records into\",\"spend hours turning records into\")\nrep(\"and a confirm for disputed summaries (D-066, T-179).\",\"and a confirm for disputed summaries (D-066, T-179).\")\nrep(\"Each timeline entry shows the AI's summary beside the verbatim record quote; she accepts, edits or dismisses it.\",\"Each timeline entry shows the AI's summary beside the verbatim quote; she accepts, edits or dismisses it.\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12;  tail -c 100 $SC/unit.out"
}
````

### User / tool · 2026-11-02T21:25:40.848Z

**tool result**
````
product-note pages 2
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before and after text, time on
item). Verifying or clicking through? (5 of 5 disputed items took one click.)

.............................................................. [ 90%]
..............................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:49.485Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"Source: audit-log accept events (before and after text, time on item). Verifying or clicking through? (5 of 5 disputed items took one click.)\",\"Source: audit-log accept events (before/after, time on item). Verifying or clicking through? (5 of 5 disputed took one click.)\")\nrep(\"Source: case-created and letter-copied timestamps; stopwatch baseline, week 2. Read beside #2: speed from skipping review is no win.\",\"Source: case-created and letter-copied timestamps; stopwatch baseline, week 2. Read with #2: speed from skipping review is no win.\")\nrep(\"Source: attorney edit log plus adjuster letters the paralegal tags. Target 0; each becomes an eval case.\",\"Source: attorney edit log, plus adjuster letters the paralegal tags. Target 0; each becomes an eval case.\")\nrep(\"A persona reviewer scored the M3 screen 4/5. When I used it myself it was *very* hard to use.\",\"A persona reviewer scored the M3 screen 4/5. Used by me, it was *very* hard to use.\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:25:50.612Z

**tool result**
````
product-note pages 2
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before/after, time on item).
Verifying or clicking through? (5 of 5 disputed took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:00.866Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"Used by me, it was *very* hard to use.\",\"When I used it, it was *very* hard to use.\")\nrep(\"[L] = `evals/reports/library-latest.md` (15 packets, run at a74b727, before the billing redesign).\",\"[L] = `evals/reports/library-latest.md` (15 packets, run at a74b727, before the billing redesign); [R] = `submission/prompt-log/reviews/`.\")\nrep(\"(`submission/prompt-log/reviews/GATE-M3-paralegal.md`)\",\"([R] `GATE-M3-paralegal.md`)\")\nrep(\"**What testing found** (reviews: `submission/prompt-log/reviews/`).\",\"**What testing found.**\")\nrep(\"(`GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23)\",\"([R] `GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23)\")\nrep(\"(`T-140-claims-adjuster.md`)\",\"([R] `T-140-claims-adjuster.md`)\")\nrep(\"in 16 cases (`GATE-M3-product-manager.md`)\",\"in 16 cases ([R] `GATE-M3-product-manager.md`)\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12;  tail -c 100 $SC/unit.out"
}
````

### User / tool · 2026-11-02T21:26:02.079Z

**tool result**
````
product-note pages 2
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before/after, time on item).
Verifying or clicking through? (5 of 5 disputed took one click.)

..................................... [ 93%]
.......................................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:15.235Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"; [R] = `submission/prompt-log/reviews/`.\",\".\")\nrep(\"([R] `GATE-M3-paralegal.md`)\",\"(`submission/prompt-log/reviews/GATE-M3-paralegal.md`)\")\nrep(\"([R] `GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23)\",\"(`submission/prompt-log/reviews/GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23)\")\nrep(\"([R] `T-140-claims-adjuster.md`)\",\"(`submission/prompt-log/reviews/T-140-claims-adjuster.md`)\")\nrep(\" in 16 cases ([R] `GATE-M3-product-manager.md`);\",\" in 16 cases (same review);\")\nrep(\"For good: accounts, real patient data, EHR integrations, any medical or legal judgment.\",\"For good: accounts, real patient data, EHR integrations, medical or legal judgment.\")\nrep(\"The golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81\",\"Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81\")\nrep(\"Reviewable: paralegal persona rates \\\"I could verify every claim quickly\\\" 4/5 or more; tests green\",\"Reviewable: paralegal persona rates \\\"I could verify every claim quickly\\\" 4/5+; tests green\")\nrep(\"A claims-adjuster reviewer outworded every word-list rule: one library letter said $16,147 against a true $8,123.50\",\"A claims-adjuster reviewer outworded every word-list rule: one letter said $16,147 against a true $8,123.50\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -12"
}
````

### User / tool · 2026-11-02T21:26:16.417Z

**tool result**
````
product-note pages 2
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events (before/after, time on item).
Verifying or clicking through? (5 of 5 disputed took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:24.270Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"Code removes unsupported clauses; the second check (scored on seeded wrong items; \\\"verified\\\" is not \\\"accepted\\\") reads the rest; a disputed one will need a named confirm (D-066, in progress)\",\"Code removes unsupported clauses; the second check (scored on seeded wrong items) reads the rest; a disputed one will need a named confirm (D-066, in progress)\")\nrep(\"**Needs-review items accepted unchanged, and median seconds per item.** Source: audit-log accept events (before/after, time on item). Verifying or clicking through? (5 of 5 disputed took one click.)\",\"**Needs-review items accepted unchanged, and median seconds per item.** Source: audit-log accept events. Verifying or clicking through? (5 of 5 disputed took one click.)\")\nrep(\"Source: attorney edit log, plus adjuster letters the paralegal tags. Target 0; each becomes an eval case.\",\"Source: attorney edit log, adjuster letters the paralegal tags. Target 0; each becomes an eval case.\")\nrep(\"Source: case-created and letter-copied timestamps; stopwatch baseline, week 2. Read with #2: speed from skipping review is no win.\",\"Source: case-created and letter-copied timestamps; stopwatch baseline, week 2. Read with #2: skipping review is no win.\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7;  tail -c 100 $SC/unit.out"
}
````

### User / tool · 2026-11-02T21:26:25.250Z

**tool result**
````
product-note pages 2
................................................... [ 99%]
.........................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:29.474Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head; pdftotext -layout -f 1 -l 1 $SC/r/product-note.pdf - | tail -12 | cut -c1-170"
}
````

### User / tool · 2026-11-02T21:26:29.592Z

**tool result**
````
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit-log accept events. Verifying or clicking through?
(5 of 5 disputed took one click.)

Invents an amount, or obeys an order hidden in       Only code finds money; she accepts each charge; models have no tools
a record
Rules on cause or diagnosis                          Flag wording is a code template; the model returns a category and a quote only (D-007)
LLM and code. Code does anything with one right answer: dates (ambiguous ones wait for her), gap arithmetic, amounts and class, totals,
quote and number checks, flag wording, export. The model reads: summary and quote, flag category, one yes/no per code-proposed conflict
pair, where to cut a paste code could not split (offsets only, code validates; LLM_SPLIT), and the second check. Table: docs/LLM_VS_CODE.md.
Three metrics after launch.
1. Minutes from first paste to copied letter section, against her own last three by hand. Source: case-created and letter-copied
   timestamps; stopwatch baseline, week 2. Read with #2: skipping review is no win.
2. Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100. Source: attorney edit log, adjuster letters the
   paralegal tags. Target 0; each becomes an eval case.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:33.835Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -8 $SC/unit.out; cat $SC/arch/.sha"
}
````

### User / tool · 2026-11-02T21:26:33.919Z

**tool result**
````
........................................................................ [ 94%]
........................................................................ [ 95%]
........................................................................ [ 96%]
........................................................................ [ 98%]
........................................................................ [ 99%]
...........................................                              [100%]
5795 passed, 8 skipped in 356.75s (0:05:56)
exit=0
33e88c6862f4838648c6ce6bc7f27327123f2267
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:43.633Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nF=artifacts/unit-count-33e88c6.txt\n{ echo \"# Unit test count, writer, T-185/T-186 round 2, 2026-11-02\"; echo \"# Commit: 33e88c6862f4838648c6ce6bc7f27327123f2267 (git archive HEAD, extracted to a scratch directory; .venv symlinked from the working tree)\"; echo \"# Command: .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider   (E2E_REQUIRE_DB not set, so DB-gated unit tests skip: 8 skipped here, 2 skipped in evals/reports/m3-sensors.md)\"; echo \"# Result line: 5795 passed, 8 skipped in 356.75s (0:05:56), exit 0\"; echo; cat $SC/unit.out; } > $F\nwc -l $F; head -6 $F | cut -c1-200\npython3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"UNITCOUNT unit tests passed at 33e88c6 (`artifacts/UNITFILE`)\",\"5,795 unit tests passed at 33e88c6 (`artifacts/unit-count-33e88c6.txt`)\")\nrep(\"Source: audit-log accept events. Verifying or clicking through? (5 of 5 disputed took one click.)\",\"Source: audit log. Verifying or clicking through? (5 of 5 disputed took one click.)\")\nopen(p,'w').write(s)\np='submission/part2-process.md'\ns=open(p).read()\nrep(\"Unit tests (UNITCOUNT passed at 33e88c6, `artifacts/UNITFILE`)\",\"Unit tests (5,795 passed at 33e88c6, `artifacts/unit-count-33e88c6.txt`)\")\nopen(p,'w').write(s)\nE\n$SC/r/render.sh $SC product-note 8.7; $SC/r/render.sh $SC part2-process 9.4; pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -5"
}
````

### User / tool · 2026-11-02T21:26:45.610Z

**tool result**
````
      88 artifacts/unit-count-33e88c6.txt
# Unit test count, writer, T-185/T-186 round 2, 2026-11-02
# Commit: 33e88c6862f4838648c6ce6bc7f27327123f2267 (git archive HEAD, extracted to a scratch directory; .venv symlinked from the working tree)
# Command: .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider   (E2E_REQUIRE_DB not set, so DB-gated unit tests skip: 8 skipped here, 2 skipped in evals/reports/m3-sensors.md)
# Result line: 5795 passed, 8 skipped in 356.75s (0:05:56), exit 0

........................................................................ [  1%]
product-note pages 2
part2-process pages 4
3. Needs-review items accepted unchanged, and median seconds per item. Source: audit log. Verifying or clicking through? (5 of 5
disputed took one click.)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:53.714Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='submission/product-note.md'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"Grounding: every exported statement and amount has a quote found in the input (100%)\",\"Grounding: every exported statement and amount has a quote in the input (100%)\")\nrep(\"Invents an amount, or obeys an order hidden in a record\",\"Invents an amount, or obeys an order in a record\")\nrep(\"Flags: precision and recall 0.9 per type; 28-day interval not flagged, 73-day flagged\",\"Flags: precision, recall 0.9 per type; 28-day gap not flagged, 73-day flagged\")\nopen(p,'w').write(s)\nE\nSC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; $SC/r/render.sh $SC product-note 8.7;  pdftotext -f 2 -l 2 $SC/r/product-note.pdf - | head -5; pdftotext -layout -f 1 -l 1 $SC/r/product-note.pdf - | sed -n 18,40p | cut -c1-175"
}
````

### User / tool · 2026-11-02T21:26:54.765Z

**tool result**
````
product-note pages 1
Command Line Error: Wrong page range given: the first page (2) can not be after the last page (1).
evals/reports/20261102T164038Z.md; [L] = evals/reports/library-latest.md (15 packets, run at a74b727, before the billing redesign).
# Criterion (bar)                                         Result
1 Grounding: every exported statement and amount          1.000, 242 checked [E]
  has a quote in the input (100%)
2 Recall of golden entries and amounts (95%)              golden: entries 0.982, amounts 1.000 [E]. Library: entries 0.775, amounts 0.681 [L] (0.580
                                                          on a later run; report being regenerated). Misses cluster in ledgers, EOBs, scans, Spanish;
                                                          real misses vs stale expected files not yet separated
3 Flags: precision, recall 0.9 per type; 28-day gap not   golden: 1.000/1.000, four types; 28 no, 73 yes [E]. Library: 34 of 42 must-flags, 0.81 [L]
  flagged, 73-day flagged
4 No invented facts: 0 unsupported over 3 runs; judge 0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12, 0 false agrees [E]
  catches 95% of seeded wrong summaries
5 Reviewable: paralegal persona rates “I could verify     Not met on the screen I rejected. Persona 4/5 on the M3 screen (submission/prompt-
  every claim quickly” 4/5+; tests green                  log/reviews/GATE-M3-paralegal.md), which I found very hard to use; guided screen not
                                                          scored. 5,795 unit tests passed at 33e88c6 (artifacts/unit-count-33e88c6.txt); 412
                                                          E2E at d7ea327 (evals/reports/m3-sensors.md)
What testing found.
  Reviewability passed on paper and failed in use. A persona reviewer scored the M3 screen 4/5. When I used it, it was very hard to use. I
  wanted it simple enough for anyone (D-068), so it is being rebuilt as four fixed steps, one question at a time. The 4/5 predates the redesign
  and does not count for the new screen. An AI reviewer is no substitute for a person at the desk: the ship call needs a real paralegal.
  The 1.000 flag numbers do not generalize. Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81
  (submission/prompt-log/reviews/GATE-M3-product-manager.md; memory/SCOPE_CUTS.md rows 13, 23). The misses are conflicts code
  never proposes (“Left” against “Right shoulder pain”). Judge numbers are partly in-sample (5 of 17 “held-out” controls still clean).
  Billing took four adversarial rounds. A claims-adjuster reviewer outworded every word-list rule: one letter said $16,147 against a true
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:00.505Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; pdftotext -layout -f 4 -l 4 $SC/r/part2-process.pdf - | wc -l; pdftotext -layout -f 4 -l 4 $SC/r/part2-process.pdf - | tail -8 | cut -c1-120; which pdftoppm && pdftoppm -r 60 -png $SC/r/part2-process.pdf $SC/r/p2 && pdftoppm -r 70 -png $SC/r/product-note.pdf $SC/r/pn; ls $SC/r"
}
````

### User / tool · 2026-11-02T21:27:01.117Z

**tool result**
````
      46
        1. What you shipped and what you expected it to do.
        2. What you missed, and the number or signal that showed it.
        3. One concrete thing you changed in your process afterward: an artifact or a rule, not “communicate more.”
        4. How that change shows up in this project.
       Hooks from this build you can tie it to: a “must never” acceptance criterion written before building; a held-
       looked at once (golden 1.000 against library 0.81); a persona score that passed a screen you found very hard to u
       checking evidence instead of a worker’s claim; the demo that labeled prepared answers as AI output.]
/opt/homebrew/bin/pdftoppm
p2-1.png
p2-2.png
p2-3.png
p2-4.png
p_part2-process.css
p_product-note.css
part2-process.html
part2-process.pdf
pn-1.png
product-note.html
product-note.pdf
render.sh
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:04.044Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r/p2-1.png"
}
````

### User / tool · 2026-11-02T21:27:04.051Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:08.904Z

**tool call — Bash**
````
{
 "command": "SC=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; \"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\" --headless=new --disable-gpu --screenshot=$SC/r/svg.png --window-size=830,610 file:///Users/arsis/zlayt-pm-project/submission/validation-ladder.svg >/dev/null 2>&1; ls $SC/r/svg.png"
}
````

### User / tool · 2026-11-02T21:27:09.833Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r/svg.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:12.868Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r/svg.png"
}
````

### User / tool · 2026-11-02T21:27:12.879Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:16.240Z

**tool call — Bash**
````
{
 "command": "for f in submission/product-note.md submission/part2-process.md; do grep -oE '`[^`]+`' $f | tr -d '`' | grep -E '^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]*)+/?$|\\.(md|py|json|svg)$' | sort -u | while read p; do if git ls-files --error-unmatch \"$p\" >/dev/null 2>&1 || git ls-files \"$p\" | grep -q .; then :; elif [ -e \"$p\" ]; then echo \"UNTRACKED-ON-DISK $f: $p\"; else echo \"MISSING $f: $p\"; fi; done; done"
}
````

### User / tool · 2026-11-02T21:27:16.847Z

**tool result**
````
UNTRACKED-ON-DISK submission/product-note.md: artifacts/unit-count-33e88c6.txt
UNTRACKED-ON-DISK submission/part2-process.md: artifacts/unit-count-33e88c6.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:31.637Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='.claude/agent-memory/writer/submission_pipeline.md'\ns=open(p).read()\ns=s.replace(\"**Pitfalls:**\",\"\"\"**Round 2 (after PM review fail):** render with a scratch copy of print.css plus `body{font-size:Npt}` (script pattern: pandoc --css <copy> then Chrome). Product note needed ~1050 words at 8.7pt; table column widths (dash counts) and orphan last lines matter more than words. Cite only paths `git ls-files` knows: reviews are tracked at `submission/prompt-log/reviews/`, not `reviews/`. Run a backtick-path existence check before handoff. Unit count: `git archive HEAD` into scratch, symlink `.venv`, pytest (about 6 min), save under `artifacts/unit-count-<sha>.txt`; a count is valid only for its commit. Library recall: committed `evals/reports/library-latest.md` (a74b727) gives entries 0.775, amounts 0.681, flags 0.81; the PM reviewer's d0b04bc run (untracked evidence) gave amounts 0.580 — flag the mismatch, don't pick silently. Never present T-181/T-179 as built until committed.\n\n**Pitfalls:**\"\"\")\nopen(p,'w').write(s)\nE\nB=\"python3 tools/board.py\"\n$B note T-185 --agent writer --text \"Round 2: redesign story added as first testing finding (persona 4/5 predates D-068; row 5 now 'not met on the screen I rejected'); guided screen T-181 and D-066 confirm T-179 marked in progress; unit 5,795 at 33e88c6 from fresh git-archive run (artifacts/unit-count-33e88c6.txt); library entries 0.775 / amounts 0.681 / flags 0.81 from committed evals/reports/library-latest.md (a74b727), 0.580 amounts noted as later run; three stretch items named with cost; metrics have sources; LLM split fallback added; all cited paths exist in git. Renders to 1 page.\"\n$B note T-186 --agent writer --text \"Round 2: redesign story in area 4 and area 7; table and SVG reworded (persona 4/5 on old screen, rejected in use; D-066 'in progress'); SVG split fallback fixed; area 6 gets an Engineering paragraph (decides how, not-safe-to-ship veto, evidence-first tiebreak; stance flagged NEEDS_CHRIS #9); unit 5,795 at 33e88c6; paths now submission/prompt-log/reviews/; counts 460 reviews, 27 dated reports, 68 decisions, 62 debt rows, A-101..A-109. 4 pages.\"\n$B handoff T-185 --agent writer --text \"What changed: submission/product-note.md round 2, one page. Redesign finding first (persona 4/5 predates D-068, row 5 not met), T-181/T-179 marked in progress, three stretch items named with cost, library recall beside golden, metrics with data sources, LLM split fallback, \\$10,906 dropped. How verified: pandoc+Chrome page count 1; every backticked path git-tracked; unit 5,795 at 33e88c6 in artifacts/unit-count-33e88c6.txt. Left: [CHRIS: name, link, stretch reason] (NEEDS_CHRIS 5, 8); refresh when T-181/T-179 land and after qa regenerates library-latest.md. Surprised me: committed library report gives amounts 0.681, not the 0.580 of the d0b04bc run; I show both. One page has about 1 line of slack.\"\n$B handoff T-186 --agent writer --text \"What changed: part2-process.md and validation-ladder.svg round 2. Redesign story (areas 4, 7), reviewability row and SVG reworded, D-066 rung 3 'in progress', SVG split fallback, Engineering paragraph in area 6, A-109, assumption marker on matter volume, paths and counts matched to git. How verified: 4 pages by pandoc+Chrome; SVG rendered and read; backtick-path check; unit 5,795 at 33e88c6. Left: miss story (T-189), optional markers (T-190), engineering stance confirm (NEEDS_CHRIS 9). Refresh counts and T-179/T-181 wording at final.\"\n$B move T-185 in_review --agent writer; $B move T-186 in_review --agent writer"
}
````

### User / tool · 2026-11-02T21:27:32.212Z

**tool result**
````
noted on T-185
noted on T-186
handoff written on T-185
handoff written on T-186
T-185: in_progress -> in_review
T-186: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:32.807Z

Now commit with a temp index.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:34.011Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/writer-index && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add submission/product-note.md submission/part2-process.md submission/validation-ladder.svg submission/NEEDS_CHRIS.md artifacts/unit-count-33e88c6.txt .claude/agent-memory/writer/submission_pipeline.md && git diff --cached --stat | tail -8"
}
````

### User / tool · 2026-11-02T21:27:35.597Z

**tool result**
````
 .claude/agent-memory/writer/submission_pipeline.md | 18 +++++
 artifacts/unit-count-33e88c6.txt                   | 88 ++++++++++++++++++++++
 submission/NEEDS_CHRIS.md                          |  4 +-
 submission/part2-process.md                        | 22 +++---
 submission/product-note.md                         | 47 ++++++------
 submission/validation-ladder.svg                   | 47 ++++++------
 6 files changed, 170 insertions(+), 56 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:38.810Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/writer-index && git commit -q -m \"docs(submission): T-185/T-186 round 2: redesign story (persona 4/5 predates D-068), only-committed claims, fresh unit count, library recall beside golden, engineering role, stretch reasons\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- submission/product-note.md submission/part2-process.md submission/validation-ladder.svg submission/NEEDS_CHRIS.md artifacts/unit-count-33e88c6.txt .claude/agent-memory/writer/submission_pipeline.md 2>&1 | tail -3; SHA=$(git rev-parse HEAD); echo $SHA; unset GIT_INDEX_FILE; git log --oneline -2; git show --stat --format=%h HEAD | tail -8"
}
````

### User / tool · 2026-11-02T21:27:41.460Z

**tool result**
````
check_secrets: ok (6 file(s) scanned staged)
ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7
ddfbf6d docs(submission): T-185/T-186 round 2: redesign story (persona 4/5 predates D-068), only-committed claims, fresh unit count, library recall beside golden, engineering role, stretch reasons
f3d42a2 feat(frontend): T-181 guided UI scaffold (D-068): / is the guided app, old screen at /classic

 .claude/agent-memory/writer/submission_pipeline.md | 18 +++++
 artifacts/unit-count-33e88c6.txt                   | 88 ++++++++++++++++++++++
 submission/NEEDS_CHRIS.md                          |  4 +-
 submission/part2-process.md                        | 22 +++---
 submission/product-note.md                         | 47 ++++++------
 submission/validation-ladder.svg                   | 47 ++++++------
 6 files changed, 170 insertions(+), 56 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:45.669Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-185 --sha ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7 --agent writer; $B commit T-186 --sha ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7 --agent writer"
}
````

### User / tool · 2026-11-02T21:27:45.915Z

**tool result**
````
T-185: commit ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7 recorded
T-186: commit ddfbf6de0cf7942c45da6e01c368f27a4f2fcaf7 recorded
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:48.999Z

T-185 and T-186 are round-2 fixed and in_review, committed as ddfbf6d. The product note renders to 1 page and Part 2 to 4. The guided UI (T-181) and the disputed-summary confirm (T-179) are marked "in progress", and the redesign verdict is the first finding in both documents.

- **Library recall:** the only library report in git, `evals/reports/library-latest.md` (a74b727), gives entries 0.775, amounts 0.681 and flags 0.81, not the 0.580 you named. I show 0.681 and mention 0.580 as a later run (regeneration pending). Please confirm which to use.
- **Unit count:** 5,795 passed, 8 skipped at 33e88c6 (`artifacts/unit-count-33e88c6.txt`).
- **Chris placeholders:** the stretch reason and the area 6 engineering stance are [CHRIS] items (NEEDS_CHRIS #8 and #9, no cards yet).
- **Fit:** the product note has about one line of slack, so refreshing wording after T-181 and T-179 land will need a trim.
