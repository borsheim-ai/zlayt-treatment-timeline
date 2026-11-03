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
