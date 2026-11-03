# T-013 review — product-manager-reviewer

**Verdict: changes** (0 blockers, 5 majors, 8 minors, 2 nits).

Coverage is close to complete. Every Appendix A must-have, constraint and submission item has at least one R-ID. The only untraced item is the ground rule "tell us which AI tools". The ship bar matches CONTRACT §8.2 exactly, the sample-case truths are reproduced correctly, and the non-goals are deliberate cuts a hiring panel would respect: none of them hides a must-have.

The card does not pass because of five testability and workflow problems:
- The "edit each flag" half of the review step has no definition and no test.
- What an accepted flag becomes in the copy-ready letter text is undecidable.
- The stretch cut rule's start condition cannot be met inside M3, which is where CONTRACT puts the stretch.
- The "no invented facts" requirement R-TL-4 points at an R-ID that doesn't exist (R-QA-2).
- The R-CO-7 determinism test is ambiguous.

Exercised:
- Ran `tools/agent_prompt.py` and `board.py show T-013`.
- Confirmed with `git diff --stat 65894f6` that the file is unchanged since the commit.
- Read REQUIREMENTS.md end to end, SPEC.md, SAMPLE_CASE_TRUTHS.md, CONTRACT §5, §5.2, §8.1–8.2, §11, D.2 and D.4, plus memory/SCOPE_CUTS.md and memory/ASSUMPTIONS.md.
- Grepped the R-ID inventory: 47 IDs and one dangling ID.
- Built the full trace table: artifacts/review-evidence/T-013-trace.md.
- Sampled 10 R-IDs with a fixed seed: 5 decidable, 3 decidable but partial, 2 ambiguous.
- Checked the ship bar against §8.2 line by line and the arithmetic (8,390 − 6,240 = 2,150).

```json
{"card": "T-013", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md at commit 65894f6 (unchanged in working tree) against spec/SPEC.md Appendix A Part 1, spec/SAMPLE_CASE_TRUTHS.md, docs/CONTRACT.md §5, §5.2, §8.2; no app (M1)",
 "exercised": [
  "python3 tools/agent_prompt.py product-manager-reviewer; python3 tools/board.py show T-013",
  "git diff --stat 65894f6 -- spec/REQUIREMENTS.md -> empty (reviewed content == commit)",
  "read spec/REQUIREMENTS.md (193 lines), spec/SPEC.md, spec/SAMPLE_CASE_TRUTHS.md, CONTRACT §5 M1-M5, §5.2, §8.1, §8.2, §11, D.2, D.4",
  "R-ID inventory via grep '^| R-' -> 47 unique; grep 'R-QA' -> only REQ:40 (dangling)",
  "built trace table of 22 must-have atoms, stretch, 6 constraints, 4 ground rules, 5 submission items, 5 ship-bar rows, 7 truths -> artifacts/review-evidence/T-013-trace.md",
  "random 10 R-IDs (python random.seed(13)): R-CO-5, R-CO-7, R-EX-1, R-EX-3, R-EX-5, R-SU-4, R-TL-1, R-TL-2, R-TL-3, R-TL-4 -> 5 decidable, 3 partial, 2 ambiguous",
  "ship bar REQ:157-163 vs CONTRACT:417-422 compared number by number",
  "non-goals REQ:139-149 vs Appendix A must-haves and memory/SCOPE_CUTS.md rows 1-11",
  "memory/ASSUMPTIONS.md A-101..A-108 vs REQ §7"
 ],
 "verdict": "changes",
 "scores": {"traceability": 4, "test_decidability": 3, "stretch_rationale": 4, "cut_rule": 2, "non_goals": 5, "ship_bar_fidelity": 5, "workflow_fit": 3},
 "findings": [
  {"severity": "major",
   "title": "Review-step must-have: 'edit each flag' is undefined and no test exercises the action-by-item matrix",
   "evidence": "SPEC:41 'accept, edit or dismiss each entry and each flag before export'. REQ:71 R-RV-1 test is only 'fresh load -> all items unaccepted; export is empty until she accepts something'. REQ:72 R-RV-2 'Editing changes the summary text only' and is tested on entry 3 only; flags have no summary, so flag edit has no meaning. REQ:75 R-RV-5 dismiss test names no item type. REQ:71 also claims charges are editable, with no definition of what editing an amount means.",
   "why_it_matters": "This is a named must-have. As written, M3 can pass every R-RV test while flags cannot be edited at all, or while charge amounts can be freely overwritten. That would violate the rule that numbers come from code and amounts get explicit acceptance (CONTRACT §5.2).",
   "fix": "Define the edit field for each item type: entry = summary; flag = reason or note text, with the excerpt fixed; charge = classification only, or not editable, stated explicitly. Add an E2E row covering {accept, edit, dismiss} x {entry, flag} (6 cells) plus the decided charge behaviour.",
   "acceptance_test": "REQ lists the edit field per item type, and R-RV-1 or R-RV-2 names an E2E case for each of the 6 entry/flag x action cells."},
  {"severity": "major",
   "title": "What an accepted flag becomes in the copy-ready letter export is undecidable and risky for the user's job",
   "evidence": "REQ:85 R-EX-4 'A flag she accepted exports as a reviewer note, worded as the record words it.' The test is 'E2E with seeded items.' REQ:82 R-EX-1 tests only set equality by item ID. Nothing tests that the output is a usable 'treatment section of a demand letter' (SPEC:42). The flags include weaknesses an adjuster would use (prior low back pain, missed appointments, 'may represent degenerative change').",
   "why_it_matters": "The demand letter goes to the opposing carrier. If accepting a flag puts its text inside the paste-ready section, a paralegal who accepts it to mean 'I've seen this' pastes the case's weaknesses into the letter. Two testers could also disagree on whether 'worded as the record words it' passed. This is the 'Workflow obsession' row of What we evaluate.",
   "fix": "Decide and state what accepting a flag means: acknowledged or include in letter. Specify the export layout, for example a treatment section of entries and charges, followed by a separated 'Reviewer notes, not for the letter' block for flags. Make R-EX-4's wording rule a check: the note text equals the flag's verbatim excerpt plus its type label. Record the decision as an assumption or ADR.",
   "acceptance_test": "E2E: accept 2 entries, 1 charge and 1 flag; the export's treatment section contains no flag text; the flag appears only under the reviewer-notes heading, with excerpt == source substring. A paralegal-persona review of the export has no major on 'copy-ready'."},
  {"severity": "major",
   "title": "Stretch cut rule's start condition can never be met inside M3",
   "evidence": "REQ:126 'Start only when every must-have R-ID has a passing test, E2E is green and the M3 gate has zero blockers.' Must-have R-IDs include R-CO-4 (INST, an M4 item per CONTRACT §5 M4), R-CO-5 (banner, M4), R-CO-8 and R-SU-1..4 (M5). CONTRACT §5 M3 lists 'the chosen stretch item if still inside budget' as an M3 card, and the M3 gate is M3's exit.",
   "why_it_matters": "Read literally, the stretch never starts. Read loosely, it starts after the M3 gate, so it ships without the ux, paralegal, accessibility and chaos gate review. In either case, 'cut on purpose' turns into an unclear or unreviewed decision, which is the opposite of what Builder mindset grades. The rule also gives two fallbacks ('ship the minimum ... or cut it entirely') with no rule for choosing between them.",
   "fix": "Scope the start condition to M3: all R-IDs with M2/M3 checkers passing (name them, or 'all R-IN/TL/FL/CH/RV/EX + R-CO-1..3,6,7,9'), E2E green, and M3 under 100% of budget. Then build the stretch before the M3 gate so the gate reviews it. Say which fallback applies when: minimum modal if >= 20 of the 45 min remain, else cut.",
   "acceptance_test": "Every R-ID named in the start condition has an M2 or M3 checker. The stretch card sits before the M3 gate card on the board. The cut rule names a single outcome for each time state."},
  {"severity": "major",
   "title": "R-TL-4 (no invented facts) cites nonexistent R-QA-2 and has no catch threshold",
   "evidence": "REQ:40 'seeded unsupported summaries are caught (see R-QA-2)'. `grep -rn R-QA spec docs board` hits only REQ:40. The threshold (>= 95%, 20 seeded) appears only in ship bar row 4 (REQ:162), not in the R-TL-4 test.",
   "why_it_matters": "This is the requirement behind the spec's hardest constraint ('Do not let the tool invent medical facts', SPEC:48). The file's own rule (REQ:4) is that a card unable to name its R-ID is wrong. Here the doc itself points at an ID that doesn't exist, and 'caught' can be read as all, most or any.",
   "fix": "Replace '(see R-QA-2)' with the threshold inline: 'judge #1 flags >= 95% of the 20 seeded unsupported summaries (metric hallucination_catch_rate)'. Alternatively, create R-QA-2 with that text.",
   "acceptance_test": "Every R-ID referenced in REQUIREMENTS.md is defined in it (script: referenced set minus defined set is empty). The R-TL-4 test names a numeric threshold."},
  {"severity": "major",
   "title": "R-CO-7 determinism test is circular and does not test what the requirement claims",
   "evidence": "REQ:100 requirement: 'Same input, same config -> same timeline, flags and totals'. Test: 'identical code-derived results (gaps, totals, states for the same verified items); LLM text may differ only in wording'. Prior and causation flags and semantic conflicts are LLM-derived (CONTRACT §5.2), so they are excluded from the test. 'states for the same verified items' lets an item that flips verified->needs_review drop out of the comparison.",
   "why_it_matters": "If a paralegal re-runs the case and sees a different set of prior or causation flags, she stops trusting the tool. The test as written would still pass. Two reviewers would disagree on whether 'differs only in wording' holds.",
   "fix": "Test the claim directly: across 3 runs, the set of entry IDs, the set of (flag type, record IDs, excerpt) tuples, every item's state and the totals are identical. Summary text may vary but must be judged `supported` each run. If LLM flag sets cannot be held identical, change the requirement to a stated tolerance, such as flag-set Jaccard >= 0.9, and say so.",
   "acceptance_test": "The R-CO-7 test names the compared fields as sets and has a numeric pass condition. It contains no phrase like 'same verified items' or 'only in wording'."},
  {"severity": "minor",
   "title": "R-SU-3 product-note test is a panel opinion, not a checklist",
   "evidence": "REQ:112 test: 'Hiring-panel and product-manager review. Numbers in the note equal the numbers in the latest eval report.' SPEC:70 lists 7 required contents plus 'one-page'.",
   "why_it_matters": "This is a graded deliverable. 'One page', '3 to 5 criteria' and 'three metrics and what each tells you' are countable, yet the test leaves them to judgement.",
   "fix": "Add a checklist: 7 headings present, 3-5 ship criteria, exactly 3 metrics each with a 'tells you' line, and a page limit (for example the pandoc PDF is 1 page, or <= 650 words).",
   "acceptance_test": "A qa script reports each checklist item as pass or fail on submission/product-note.md."},
  {"severity": "minor",
   "title": "Ground rule 'tell us which AI tools' has no R-ID; R-SU-4 does not test 'unedited'",
   "evidence": "SPEC:16 'Tell us which ones, and keep your prompts.' REQ:113 R-SU-4 test: 'submission/prompt-log/ present with reading guide.' CONTRACT §5 M5 requires TOOLS.md, but no R-ID traces to it.",
   "why_it_matters": "The hiring panel will look for this, and an untraced item is the kind that gets dropped under M5 time pressure.",
   "fix": "Add the TOOLS.md requirement to R-SU-4 (tools, models, team organisation) and require that the export is produced by tools/export_prompt_log.py with no manual edits (diff against a re-run).",
   "acceptance_test": "R-SU-4 test names submission/prompt-log/TOOLS.md and an unedited check."},
  {"severity": "minor",
   "title": "R-FL-4 'labeled as patient self-report' has no decidable check",
   "evidence": "REQ:53 'Record 9 is labeled as patient self-report, not a physician opinion.'",
   "why_it_matters": "This is exactly the distinction an adjuster attacks. Without a named field or string, two testers could disagree on whether the label is there.",
   "fix": "Name the field, for example flag.source_kind == 'patient_report', and the UI text, for example 'Patient self-report'.",
   "acceptance_test": "EV assertion on the record-9 flag's source_kind, plus E2E text match."},
  {"severity": "minor",
   "title": "Placement of an ambiguous-date record in the timeline and gap math is unspecified",
   "evidence": "REQ:30 R-IN-3 raises `date_ambiguous` and keeps the raw string. Nothing says whether that record appears in the chronology, where, or whether R-FL-1 (REQ:50) skips it.",
   "why_it_matters": "An ambiguous date next to a 30-day boundary can create or hide a gap flag.",
   "fix": "State the rule, for example 'excluded from ordering and gap math, shown in a Dates to confirm tray; once she confirms a date it re-enters'.",
   "acceptance_test": "UT: a golden case with an ambiguous date between two records 40 days apart yields no gap flag until the date is confirmed."},
  {"severity": "minor",
   "title": "R-EX-3 and R-EX-2 tests cover less than their requirements",
   "evidence": "REQ:84 'Chronological order, deterministic', but the test is 'export twice, compare' (no order assertion). REQ:83 'for every exported line, the excerpt is a substring', but header and count lines have no excerpt.",
   "why_it_matters": "An export that is byte-identical but out of order passes R-EX-3.",
   "fix": "Add an order assertion on exported item dates. Restrict R-EX-2 to statement and amount lines.",
   "acceptance_test": "UT asserts that the exported dates are non-decreasing, and that statement lines are identified by a marker."},
  {"severity": "minor",
   "title": "Ship bar row 5 measurement path and score key don't match repo convention",
   "evidence": "REQ:163 `reviews/<card>-paralegal-reviewer.md score field`. Existing review files use the short persona name (reviews/T-005-product-manager.md, reviews/T-007-staff-engineer.md). D.2 scores are free-form keys, and no key is named for 'I could verify every claim quickly'.",
   "why_it_matters": "qa cannot compute ship-bar item 5 automatically without a fixed key and path.",
   "fix": "Use `reviews/<card>-paralegal.md`, `scores.verify_every_claim_quickly >= 4`, and name it in the paralegal reviewer brief.",
   "acceptance_test": "The path pattern matches files the board validator accepts, and the key is named in REQ §6 and in the paralegal agent body."},
  {"severity": "minor",
   "title": "§7 proposed assumptions are stale and R-RV-3 is unconfirmed but sits in the must-have table",
   "evidence": "REQ:182 'Proposed additions (not yet in ASSUMPTIONS.md)', but memory/ASSUMPTIONS.md:18-22 now holds them as A-104..A-108. REQ:73 R-RV-3 says '(Design decision for architect to confirm ...)'.",
   "why_it_matters": "Traceability goes stale on day one, and an unconfirmed requirement can't be a ship gate.",
   "fix": "Cite A-104..A-108 by ID in §7. Mark R-RV-3 as 'proposed' in the table, or confirm it via ADR.",
   "acceptance_test": "grep 'not yet in' spec/REQUIREMENTS.md returns nothing, and R-RV-3 has an ADR ref or a 'proposed' tag."},
  {"severity": "minor",
   "title": "Running total reads $0 on first load (I would do differently)",
   "evidence": "REQ:63 R-CH-3 'Running total sums only charge amounts that the paralegal has accepted.' REQ:65 R-CH-5 says amounts always require acceptance.",
   "why_it_matters": "SPEC:40 asks for 'a running total'. A first screen showing $0 next to two $ amounts invites a 'broken?' reaction in the demo. Showing pending and accepted totals side by side keeps the safety and makes the state clear.",
   "fix": "Show 'Accepted: $X · Pending review: $Y (N charges)'. Only Accepted exports.",
   "acceptance_test": "E2E: fresh load shows Pending $8,390 and Accepted $0; after accepting both, Accepted shows $8,390."},
  {"severity": "nit",
   "title": "R-ID count in the card note doesn't match the file",
   "evidence": "T-013 note: '48 R-IDs'. `grep '^| R-' spec/REQUIREMENTS.md | wc -l` -> 47.",
   "why_it_matters": "Small, but handoff numbers should match the artifact.",
   "fix": "Correct the note in the next handoff.",
   "acceptance_test": "Handoff count == grep count."},
  {"severity": "nit",
   "title": "Stretch 'line 3' is four sentences, mostly about the rejected options",
   "evidence": "REQ:124",
   "why_it_matters": "The AC asks for a 3-line rationale. The why-not-the-others content is good but buries the cost argument.",
   "fix": "Move the rejected-alternative sentences into a separate 'Why not the others' line.",
   "acceptance_test": "The three rationale lines are one sentence each."}
 ],
 "whats_right": [
  "The ship bar (REQ:157-163) matches CONTRACT §8.2 number for number, and each row names a metric, a run command and R-IDs.",
  "The sample-case truths are exact: 73/28-day gaps, all five causation items, $8,390, the $185 rate with no PT total, and the five must-nots as named negative assertions (REQ:96).",
  "Non-goals are deliberate, each has a reason, all 11 are logged in SCOPE_CUTS, none hides a must-have, and folding the confidence indicator into core is well argued."
 ],
 "questions_for_chris": []}
```
