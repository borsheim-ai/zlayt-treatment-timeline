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
