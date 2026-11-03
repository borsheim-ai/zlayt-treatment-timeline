# T-011 review — product-manager-reviewer

**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit).

The 8 product/engineering dossiers have all 10 §6.3 sections, at least 3 sources each, and 16-20 checklist items each. The hiring-panel checklist maps R1-R7 onto Appendix A's seven "What we evaluate" rows in order, including each row's "Where we see it" column. I spot-checked 3 sources from these dossiers (Built In Zlayt profile, Institute of AI PM, Hamel), and all 3 match their takeaways. The filler-word grep finds nothing.

Two problems block the gate.

1. **Severity anchors are softer than the dossiers' own dealbreakers in 6 of 8 files.** The installer rates a 7m40s install as **major**, although Appendix A's "under 5 minutes" is a hard constraint and the dossier's own §5 calls it a dealbreaker. The chaos-tester rates a silently guessed date as **minor**, while its §5 calls that a dealbreaker and Appendix A says to "say so instead of guessing". Security, UX, staff-engineer and my own PM dossier show the same contradiction, and the PM dossier has no blocker example at all.
2. **The M5 gate dossiers (PM and hiring-panel) don't check several Part 2 requirements that the spec names explicitly:**
   - the **retention** metric in area 5
   - area 6, which asks about decision rights and the first 30 days
   - area 3's "three acceptance criteria ... including one about what it must never do"
   - area 7's "keep the founders informed without creating extra meetings"

   As written, the gate panel would pass a Part 2 that omits any of these.

Exercised: `python3 tools/board.py show T-011` (in_review, commit 0a10094, 2 AC checked); `git show --stat 0a10094` (8 files, 589 insertions); the scripted section/source/checklist count in `artifacts/review-evidence/T-010-011-sections.txt` found all 8 files with sections 1-10, unique URLs PM 5, UX 5, staff 4, security 10, chaos 8, a11y 5, installer 4, hiring 5, and checklist items 20/20/20/18/20/20/16/20. I compared hiring-panel R1-R7 row by row against spec/SPEC.md:21-30. I checked PM and hiring-panel coverage against the eight Part 2 areas (SPEC.md:78-94) and grepped for retention, first 30 days, operating rhythm and founders-informed, with no matches. I checked file and section references (CONTRACT.md §8.2 at :417, M5 gate at :326, the `app.pipeline` CLI at :302, UX criteria at :355; "Zinda" at SPEC.md:8). I curl-fetched 3 sources (see `artifacts/review-evidence/T-010-011-source-check.md`) and cross-checked each dossier's red flags against its calibration severities.

```json
{"card": "T-011", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 0a10094: personas/{product-manager,ux-designer,staff-engineer,security,chaos-tester,accessibility,installer,hiring-panel}.md; no app (M1 research card); reference = spec/SPEC.md Appendix A 'What we evaluate' + Part 2 areas, docs/CONTRACT.md §6.3, §7.4, §8.2, M5",
 "exercised": [
  "python3 tools/board.py show T-011 -> status in_review, commits [0a10094], AC 1-2 done:true",
  "git show --stat 0a10094 -> 8 persona files, 589 insertions; no later drift in personas/",
  "scripted section/source/checklist/calibration count -> artifacts/review-evidence/T-010-011-sections.txt: all 8 have sections [1..10]; unique URLs PM 5, UX 5, staff-eng 4, security 10, chaos 8, a11y 5, installer 4, hiring-panel 5 (all >=3); checklist 20/20/20/18/20/20/16/20 (all 12-25); 3 calibration examples each; PM severities = [major, major, minor]",
  "hiring-panel R1-R7 headers (personas/hiring-panel.md:19,23,28,33,38,43,47) compared to spec/SPEC.md:24-30 rows and 'Where we see it' column -> 1:1, same order; each of 20 items sits in exactly one row",
  "PM + hiring-panel checklists compared to Part 2 areas 1-8 (spec/SPEC.md:80-87) and Format (SPEC.md:94); grep -n -i 'retention|first 30|operating rhythm|founders informed' on both files -> no matches",
  "verified references: Zinda (SPEC.md:8), CONTRACT §8.2 (:417), M5 gate 'any row <= 2 fails' (:326), CLI app.pipeline (:302), UX four criteria (:355)",
  "curl spot-check of 3 cited URLs from these dossiers (builtinaustin.com/company/zlayt-ai, institutepm.com how-to-hire-an-ai-pm, hamel.dev evals) -> 3/3 supported",
  "grep for AI-filler terms -> only hiring-panel:26 and product-manager:22 'not just', both literal and acceptable",
  "cross-check of each section 5 red flag against section 8 calibration severity, Appendix A constraints and CONTRACT.md:676"
 ],
 "verdict": "changes",
 "scores": {"structure_6_3": 5, "source_grounding": 4, "checklist_concreteness": 4, "calibration_severity": 2, "appendix_a_mapping": 3, "lane_discipline": 5},
 "findings": [
  {"severity": "major",
   "title": "Calibration examples rate spec-constraint violations and self-declared dealbreakers as major or minor (6 of 8 dossiers)",
   "evidence": "personas/installer.md:54 '**major — 7m40s to first success.**' vs installer.md:36 red flag 'Time to first success over 5 minutes' and spec/SPEC.md:49 'run it from a link, or from your repo in under 5 minutes'; personas/chaos-tester.md:58 '**minor — Ambiguous date silently parsed.** ... \"05/07/11\" shown as 2011-05-07 with no flag' vs chaos-tester.md:42 'A date or amount silently guessed from ambiguous input' and SPEC.md:40 'If an amount is unclear, say so instead of guessing' / SPEC.md:48 'must contain nothing that is not in the records'; personas/staff-engineer.md:60 '**minor — Money as float.**' vs staff-engineer.md:42 'Float arithmetic on money'; personas/security.md:58 '**major — XSS via record text.**' vs security.md:41 'Stored or reflected XSS'; personas/ux-designer.md:63 '**major — Error loses input.**' vs ux-designer.md:44 'An error state loses the user's pasted records'; personas/product-manager.md:60 '**major — Ship bar is untested.**' vs product-manager.md:41 'A ship bar with no numbers, or numbers with no test result next to them' (and the PM dossier has no blocker example at all); docs/CONTRACT.md:676 'blocker = violates a spec constraint, invents or loses facts, unsafe'",
   "why_it_matters": "These examples become the severity anchors in the compiled reviewer prompts. An installer reviewer would return 'changes' on a submission that breaks Zlayt's explicit 5-minute run constraint, and a chaos reviewer would file a guessed date (an invented fact) as 'should fix'. Each such call lets a gate pass that the spec says must fail. For the PM reviewer specifically, the missing blocker anchor means Appendix A's AI-judgment row ('defines good enough to ship and tests against it') can never fail the gate on its own.",
   "fix": "In each listed dossier, either raise the example to blocker or replace it with a case that is genuinely major or minor. Add to every section 5: 'Each item here is a blocker.' For the PM dossier, add a blocker example such as 'product note claims a ship-bar result that evals/reports/latest.json contradicts' or 'a must-have is neither shown working nor listed as cut'.",
   "acceptance_test": "The red-flag/calibration cross-check (artifacts/review-evidence/T-010-011-sections.txt, second block) shows no section 8 example rated below blocker that matches a section 5 bullet or an Appendix A constraint. product-manager.md section 8 contains a blocker."},
  {"severity": "major",
   "title": "Gate dossiers (PM, hiring-panel) do not check several Part 2 requirements that the spec names explicitly",
   "evidence": "spec/SPEC.md:85 area 5 'Define how you would measure adoption, time saved, output quality and retention' vs personas/product-manager.md:28 '10. Three post-launch metrics ... adoption ..., time saved ..., quality ...' (no retention; hiring-panel has no metrics item); SPEC.md:86 area 6 (decision rights, 'What would you set up in your first 30 days?') -> no item in either dossier; SPEC.md:82 area 3 'Write three acceptance criteria for the AI's behavior, including one about what it must never do' -> product-manager.md:25 #7 and hiring-panel.md:29 #6 check only the Part 1 ship bar; SPEC.md:87 area 7 'How do you keep the founders informed without creating extra meetings?' -> hiring-panel.md:40 #13 covers unhappy/silent/conflicting only; hiring-panel.md:51 #20 checks only that the eight areas are 'covered'. grep -n -i 'retention|first 30|operating rhythm|founders informed' personas/product-manager.md personas/hiring-panel.md -> no matches",
   "why_it_matters": "Per CONTRACT.md:326, the M5 gate panel is hiring-panel + product-manager + litigation-lead, and none of them checks these items. Part 2 could ship without a retention metric or a first-30-days plan, and every gate reviewer would pass it because 'covers all eight areas' is satisfied by a heading. Zlayt wrote 'Specifics beat frameworks' (SPEC.md:94). Missing a sub-question they asked by name is exactly the specifics gap they grade.",
   "fix": "product-manager.md #10: four metrics, adoption, time saved, output quality and retention, each with formula, source and the decision it drives. Add PM items for (a) area 3: exactly three AI-behavior ACs, one a must-never; (b) area 6: a named list of decisions Chris makes alone vs needs a founder for, an expected founder turnaround time, and a first-30-days list. Add 'keeps founders informed without new meetings (names the artifact, e.g., weekly async note)' to hiring-panel R5 #13. Optionally add a hiring-panel item that reads each area's sub-questions as a checklist.",
   "acceptance_test": "grep -n -i 'retention' personas/product-manager.md and grep -n -i 'first 30' personas/product-manager.md each match a checklist line. Every sub-question in SPEC.md:80-87 maps to at least one checklist item in product-manager.md or hiring-panel.md (a table in the dossier or the card handoff shows the mapping)."},
  {"severity": "minor",
   "title": "hiring-panel review procedure says 'seven traps' but item 7 lists six",
   "evidence": "personas/hiring-panel.md:65 '2. Check the seven traps in item 7 directly in the running app' vs hiring-panel.md:30 item 7: (1) 73-day gap flagged, (2) 28-day not, (3) 01-09 vs 01-19, (4) $185 rate not totaled, (5) total $8,390, (6) 'may represent degenerative change' not converted",
   "why_it_matters": "A gate reviewer told to find seven will either invent a seventh or report one as 'not checked'. Either one adds noise to the gate's evidence table.",
   "fix": "Change to 'six traps', or add the intended seventh (likely 'concussion without loss of consciousness' preserved, or the prompt-injection record) to item 7.",
   "acceptance_test": "The count stated at hiring-panel.md:65 equals the number of traps enumerated at hiring-panel.md:30."},
  {"severity": "minor",
   "title": "A few checklist items are generic engineering or design advice, not checks specific to a treatment-timeline tool",
   "evidence": "personas/staff-engineer.md:34 '17. Names describe domain meaning (`billed_charge`, `rate_per_visit`), and comments explain why, not what.'; staff-engineer.md:36 '19. No dead code, commented-out blocks, or TODOs that hide missing must-haves.'; personas/ux-designer.md:38 '19. Visual hierarchy: on first load of the sample case, the eye lands on what needs review, not on navigation chrome.'",
   "why_it_matters": "Generic items produce subjective findings that cannot be checked, and they crowd out sharper checks. §6.3 asks for 'concrete, checkable heuristics'.",
   "fix": "Replace each with something checkable on this tool, for example staff-eng: 'the `unclear` amount class has a test with the record-4 rate'; UX: 'on first load, the first focusable item in the results region is a needs_review item'.",
   "acceptance_test": "Each replacement item names an input, a UI state or a file and says what result counts as pass or fail."},
  {"severity": "nit",
   "title": "hiring-panel R1 and R6 each rest a 1-5 score on two items",
   "evidence": "personas/hiring-panel.md:20-21 (R1: items 1-2) and :44-45 (R6: items 15-16); gate rule 'any row <= 2 fails' (CONTRACT.md:326)",
   "why_it_matters": "With two items, a single missed sub-point can swing a gate-failing row, and the scores will be noisy.",
   "fix": "Add one item to each. R1: 'cut list ties at least one cut to a measured time cost'. R6: 'release sign-off owner and a bug-reached-users playbook are named'.",
   "acceptance_test": "Each R-row in hiring-panel.md has at least 3 items."}
 ],
 "whats_right": [
  "hiring-panel R1-R7 mirrors Appendix A's seven rows in order with each row's 'Where we see it' column; each of the 20 items belongs to exactly one row.",
  "Writing is specific and free of filler (grep clean). Assumptions are labeled where sources were thin (a11y SC numbers, UX 390 px, installer rationale).",
  "PM calibration's ship-bar fix example reports a failing result ('conflict 0.83/1.0'), which models the honest reporting Appendix A rewards."
 ],
 "questions_for_chris": []}
```
