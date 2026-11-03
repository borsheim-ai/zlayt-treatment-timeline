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
