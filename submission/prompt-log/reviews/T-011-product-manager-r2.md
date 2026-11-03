# T-011 round 2 review: product-manager-reviewer

**Verdict: pass** (0 blockers, 0 majors, 2 minors, 2 nits).

All five round-1 findings are resolved against their own acceptance tests. Line refs are in `artifacts/review-evidence/T-010-011-source-check.md` under "T-011 round 2".

- **Severity anchors.** Every non-blocker calibration example in the 8 dossiers is now consistent with its own §5 and with CONTRACT D.2. The six soft anchors from round 1 are now blockers: installer:56, chaos:60, staff-eng:62, security:60, ux:65, PM:65. All 13 dossiers open §5 with "Each item here is a **blocker**".
- **Part 2 coverage.** Retention, first 30 days, the three ACs with a must-never, and founders-informed each now match a checklist line in both PM and HP. HP:55 now requires "every sub-question ... not just the headings".
- **Traps.** There are now seven traps, and the reference points to item 8. I re-checked the arithmetic: 73 d, 28 d, $8,390.
- **Generic items.** The generic items were replaced with specific ones that match the sample records verbatim.
- **Row sizes.** R1 and R6 now have 3 items each.

Two residual minors:
1. Five Part 2 sub-questions have no dedicated item and map only to the HP:55 catch-all: who you talk to first, why this feature before the others, rollout to Zinda, collecting feedback, and engineering's role in decisions. Neither dossier checks the content of the "One story" (what was missed, the process change, how it applies here). Both only check that it is a placeholder.
2. The new "Severity rule" line is worded more broadly than D.2: "anything violating Appendix A". It also drops D.2's "unsafe". Read literally, it would make PM's own major and minor examples blockers.

Exercised:
- `python3 tools/board.py show T-011`
- `git show --stat 6559f5a`
- `git diff 0a10094..6559f5a -- personas/`
- `git diff --stat 6559f5a..HEAD` on the 8 files (empty)
- re-ran the count script: `artifacts/review-evidence/T-011-r2-check.py`
- §5/§8 extraction per dossier, with a hand cross-check against D.2 (CONTRACT.md:676)
- a sub-question map against SPEC.md:80-94, plus grep
- a python check of the trap arithmetic
- checked that the compiled `.claude/agents/*-reviewer.md` files carry the new anchors

```json
{"card": "T-011", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 6559f5a (diff 0a10094..6559f5a -- personas/), HEAD f413e84; personas/{product-manager,ux-designer,staff-engineer,security,chaos-tester,accessibility,installer,hiring-panel}.md; no app (M1 research card); reference spec/SPEC.md Appendix A + Part 2 (lines 21-94), docs/CONTRACT.md D.2 (:659-676), §6.3",
 "exercised": [
  "python3 tools/board.py show T-011 -> status in_review, rounds 1, commits [0a10094, 6559f5a], AC 1-2 done:true; AC2 evidence text still 'checklists 16-20 items'",
  "git show --stat 6559f5a -> 8 persona files, 57 insertions, 34 deletions",
  "git diff --stat 6559f5a..HEAD -- <8 T-011 files> -> empty (later commit 6404549 touched only the 5 T-010 domain dossiers)",
  "python3 -I artifacts/review-evidence/T-011-r2-check.py (same script as T-010-011-sections.txt) -> all 8: sections 1-10, unique URLs 5/8/5/4/5/10/4/5 (all >=3), checklists 20/20/24/16/23/18/20/20 (all 12-25), 3 calibration examples each; PM sev [blocker, major, minor], HP [blocker, blocker, minor]",
  "grep -c 'Each item here is a **blocker**' personas/*.md -> 1 in all 13; grep -c '^Severity rule:' -> 1 in all 13",
  "per-dossier extraction of §5 bullets and §8 examples; hand cross-check of each of the 10 non-blocker examples against its §5 and D.2 -> none softer (table in evidence file)",
  "mapped every Part 2 sub-question (SPEC.md:80-87), One story and Format to PM/HP checklist items; grep -n -i 'talk to first|roll out|rollout|collect feedback|one story|engineering' on both files -> only PM:38 'rollout plan' (inside first 30 days) and HP:54 'one story' placeholder",
  "python3 date/sum check -> 2026-03-06..05-18 = 73 d, 01-23..02-20 = 28 d, 6240+2150 = 8390; staff-eng #17 strings ('10 mg','35 mph','7/10','approx. 40%','missing 3 days of work','Charge per visit $185') found verbatim in SPEC records 1,2,4,5",
  "grep of .claude/agents/{installer,chaos-tester,product-manager,hiring-panel}-reviewer.md -> compiled bodies contain the new Severity rule and raised anchors",
  "appended 'T-011 round 2' section (resolution table, re-run output, calibration table, sub-question map) to artifacts/review-evidence/T-010-011-source-check.md"
 ],
 "verdict": "pass",
 "scores": {"structure_6_3": 5, "source_grounding": 4, "checklist_concreteness": 5, "calibration_severity": 4, "appendix_a_mapping": 4, "lane_discipline": 5},
 "findings": [
  {"severity": "minor",
   "title": "Five Part 2 sub-questions map only to the hiring-panel catch-all, and 'One story' content is checked by neither gate dossier",
   "evidence": "spec/SPEC.md:80 'Who do you talk to first'; :81 'Why would this feature come before demand letter drafting, deposition summaries or discovery responses?'; :84 'How do you roll out to Zinda, collect feedback'; :85 'How are product decisions made among the founders, engineering and you?'. Their only match is personas/hiring-panel.md:55 '...answers every sub-question of all eight areas'. product-manager.md:35 (#17) checks only 'evidence that would change the decision'; PM:38 and HP:49 cover founder vs alone, with no engineering role. SPEC One story: 'Say what you missed, what you changed in your process afterwards, and how you would apply it here' vs product-manager.md:40 (#22) and hiring-panel.md:54 (#23), which check only that personal content is a placeholder. grep -n -i 'talk to first|roll out|collect feedback|one story|engineering' -> only PM:38, HP:54.",
   "why_it_matters": "The catch-all puts the enumeration back on the reviewer, which is the 'covers the headings' failure from round 1 in a weaker form. A Part 2 that never says why the timeline beats deposition summaries, or whose story scaffold leaves out 'how I'd apply it here', could still pass both gate reviewers. Zlayt asks each of these by name.",
   "fix": "PM #17: add 'states why the timeline comes before drafting, depositions and discovery, with the evidence used'. Add a PM item for area 5 rollout: 'names the first Zinda users, the rollout steps and the feedback channel'. PM #20 / HP #20: add 'and engineering's role in decisions'. Add one HP item (R7) or PM item: 'the One story scaffold has three labelled parts (what was missed, the process change, how it applies to this feature), with Chris's facts as [CHRIS: ...] placeholders'.",
   "acceptance_test": "grep -n -i 'roll out\\|rollout' personas/product-manager.md matches an item that is not the first-30-days item. grep -n -i 'one story' matches an item that names all three parts. Every row of the sub-question map in the evidence file has a dedicated item (not only HP #24)."},
  {"severity": "minor",
   "title": "New 'Severity rule' line is broader than CONTRACT D.2 and omits 'unsafe'; read literally, it contradicts PM's own major and minor examples",
   "evidence": "personas/product-manager.md:64 (identical line in all 13): 'anything violating Appendix A or the contract (invents/loses facts, breaks a must-have or constraint), is a blocker' vs docs/CONTRACT.md:676 'blocker = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable'. Part 1 What-to-submit asks for cuts 'and why' and metrics 'and what each one tells you', yet product-manager.md:66 rates an uncomputable metric as major and :67 rates 'Cut list lacks reasons' as minor.",
   "why_it_matters": "These lines are compiled into every reviewer prompt. One reviewer may read 'anything violating Appendix A' as covering any weak Part 2 answer and file blockers, while another follows the parenthetical, so the same submission gets different verdicts. Dropping 'unsafe' takes away the D.2 anchor that security and privacy reviewers lean on for findings §5 does not list.",
   "fix": "Replace the line in all 13 dossiers with D.2's definition verbatim, plus: 'Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.'",
   "acceptance_test": "grep -n '^Severity rule' personas/*.md shows 13 identical lines containing 'unsafe' and not containing 'anything violating Appendix A'."},
  {"severity": "nit",
   "title": "Hiring-panel rows hold items from Part 2 areas their 'Where we see it' column does not list, with no stated assumption",
   "evidence": "personas/hiring-panel.md:46 R6 header '(Part 2 area 8)' but item 20 at :49 is area 6. R3 header :29 '(Part 1 note, Part 2 quality bar)' holds item 10 (area 3) and item 11 (area 5). spec/SPEC.md:29 assigns Delivery leadership to 'Part 2 (area 8)' only.",
   "why_it_matters": "With 'any row <= 2 fails' (CONTRACT M5), a weak area-6 answer can now fail Delivery leadership, a row Zlayt ties to area 8 alone. This is a judgment call, not a spec violation, but it should be visible.",
   "fix": "Either move item 20 to R7 (decisions under ambiguity), or add the areas to the row headers and record the mapping as an assumption in §9.",
   "acceptance_test": "Each item's Part 2 area appears in its row header, or §9 lists the deviation as an assumption."},
  {"severity": "nit",
   "title": "Board AC 2 evidence is stale after round 2",
   "evidence": "python3 tools/board.py show T-011 -> AC 2 evidence 'checklists 16-20 items' vs re-run counts: hiring-panel 24, product-manager 23",
   "why_it_matters": "AC evidence on the board is what the gate reads. It still passes (<= 25), but the evidence does not describe the current files.",
   "fix": "Update the AC 2 evidence to 'checklists 16-24 items (HP 24, PM 23)'.",
   "acceptance_test": "board show T-011 AC 2 evidence matches the count script output."}
 ],
 "whats_right": [
  "No §8 example is now softer than its own §5 or D.2; the hiring-panel filler red flag was narrowed with an explicit 'isolated sentence is a minor' carve-out rather than left contradicting its example.",
  "New checks are executable on the sample: staff-eng #17/#19 and UX #19 name exact strings, cents values, dates and viewport, all verified against SPEC records.",
  "PM #10/#19-#21 and HP #10/#11/#16/#20 name Zlayt's Part 2 sub-questions in Zlayt's own words (retention, first 30 days, must-never, founders informed without meetings)."
 ],
 "questions_for_chris": []}
```
