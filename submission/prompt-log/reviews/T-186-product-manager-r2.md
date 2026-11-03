# T-186 Part 2 process doc + validation-ladder SVG, round 2: product-manager-reviewer (Dana Okafor lens)

**Verdict: changes** (0 blockers, 1 major, 2 minors, 2 nits).

I graded `git show HEAD:` for `submission/part2-process.md` and `submission/validation-ladder.svg`. HEAD is 2e58e18, and both files are byte-identical to ddfbf6d. I did not grade the working tree.

**Round-1 findings: 6 of 7 closed.**
- **Redesign blocker: fixed.** The area 4 table now reads "persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored" (:56), and a new paragraph follows it (:58). Area 7 uses the redesign as its honest-feedback example (:91). The SVG Rung 3 measured box says the same (svg:99-102).
- **SVG D-066 blocker: fixed.** Rung 3 now reads "In progress (D-066, T-179): a summary the judge disputed will need a named ..." (svg:58-59).
- **Unit count: fixed.** It now reads 5,795 at 33e88c6, and that file is in HEAD.
- **Area 6 engineering: fixed.** Engineering decides how, holds a not-safe-to-ship veto, and disagreements go to evidence first (:83).
- **SVG split fallback: fixed** (svg:79-81).
- **Assumption marker and A-109: fixed** (:13, :23).
- **Still open (major): counts.** Every cited path now exists in HEAD. But the doc says "counts are at the commit this doc was last edited", and three of the seven counts are not what that commit holds: 460 reviews (467 at HEAD), "44 entries" in LESSONS (28 at HEAD), and 62 debt rows (61 at HEAD). The 44 and 62 match the uncommitted working tree.

**Placeholder for the area-6 stance (T-192): acceptable, not a defect.** The decision rights Chris would give engineering are his management stance, and the panel will question him on it. The team drafted a concrete default, labeled it as a stance pending a founder, and carded it, so the area reads complete either way. One flaw remains: the marker "(NEEDS_CHRIS #9)" sits in panel-facing text outside the `[CHRIS: ...]` form, so the pre-send scrub will not find it (minor).

The doc renders to 4 pages with the committed print.css (`artifacts/review-evidence/T-185-pm/r2/part2-process.pdf`).

```json
{"card": "T-186", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/part2-process.md and submission/validation-ladder.svg at HEAD 2e58e18 (identical to fix commit ddfbf6d); cited evidence at HEAD: memory/{LESSONS,SCOPE_CUTS,ORCHESTRATOR_DECISIONS,ASSUMPTIONS}.md, spec/REQUIREMENTS.md, personas/, evals/reports/, submission/prompt-log/reviews/, artifacts/unit-count-33e88c6.txt, evals/reports/m3-sensors.md, evals/reports/library-latest.md, submission/NEEDS_CHRIS.md",
 "exercised": [
  "Read personas/product-manager.md, my round-1 review reviews/T-186-product-manager.md, board.py show T-186/T-191/T-192, board.py list (T-177, T-179, T-181 in_progress)",
  "git show --stat ddfbf6d; git diff ddfbf6d HEAD --stat -- submission/ -> empty",
  "git show HEAD:submission/part2-process.md read end to end; rendered with committed print.css via pandoc + headless Chrome -> artifacts/review-evidence/T-185-pm/r2/part2-process.pdf = 4 pages",
  "git show HEAD:submission/validation-ladder.svg | grep -n text -> read every text line (rung 3 'In progress (D-066, T-179)', split fallback, measured box)",
  "python3 -I artifacts/review-evidence/T-185-pm/paths_in_head.py <repo> submission/part2-process.md -> 21 of 21 backticked paths OK in HEAD tree",
  "Counts at HEAD: git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | wc -l -> 467 (same at ddfbf6d); git ls-tree --name-only HEAD evals/reports/ | grep -cE '^evals/reports/[0-9]{8}T' -> 27; ORCHESTRATOR_DECISIONS unique D-IDs -> 68 (D-001..D-068); git show HEAD:memory/LESSONS.md | grep -cE '^- ' -> 28 (same at ddfbf6d); git show HEAD:memory/SCOPE_CUTS.md | grep -ciE '^\\| *debt' -> 61; personas/*.md -> 13; REQUIREMENTS row R-IDs -> 62; ASSUMPTIONS A-101..A-109",
  "git diff --stat HEAD -- memory/LESSONS.md memory/SCOPE_CUTS.md -> 16 and 2 uncommitted insertions (source of 44 and 62)",
  "python3 -I artifacts/review-evidence/T-185-pm/lib_sums_r2.py on HEAD library-latest.md -> entries 0.775, amounts 0.681, must flags 0.810 (matches :44 and :54)",
  "git show HEAD:artifacts/unit-count-33e88c6.txt tail -> '5795 passed, 8 skipped'; m3-sensors.md:8 -> '412 passed' at d7ea327",
  "board.py show T-177 -> staff-engineer r2 'fail' at 21:15:23Z (before ddfbf6d at 21:27:41), card in_progress; git log --grep T-177 -> 04ea2bf, 4fcf9cd, then r3 2e58e18 after the fix commit",
  "git show HEAD:submission/NEEDS_CHRIS.md rows 8-9 -> '(card pending)'; board.py show T-192 -> P2 needs_chris",
  "git show HEAD:docs/CONTRACT.md:601 -> OutSystems AI Agent Builder is Chris-supplied (area 5 optional marker is not invented)",
  ".venv/bin/python -m evals.run --check-fresh -> exit=0 (area 4 regression claim holds)"
 ],
 "verdict": "changes",
 "scores": {"accuracy": 3, "no_invented_chris_facts": 5, "eight_areas_covered": 5, "ai_acceptance_criteria": 5, "honesty_of_misses": 5, "voice": 4, "length": 5, "visual": 5},
 "findings": [
  {"severity": "major", "title": "Three of the seven artifact counts are not what the commit holds, although the doc says 'counts are at the commit this doc was last edited'",
   "evidence": "HEAD:submission/part2-process.md:3 'Paths are as committed; counts are at the commit this doc was last edited' and 'submission/prompt-log/reviews/ (460 review files)': git ls-tree -r --name-only HEAD submission/prompt-log/reviews/ | wc -l -> 467 (467 at ddfbf6d too). :110 '(memory/LESSONS.md, 44 entries)': git show HEAD:memory/LESSONS.md | grep -cE '^- ' -> 28 (28 at ddfbf6d); the working tree has 44 (git diff --stat HEAD -- memory/LESSONS.md -> 16 insertions). :114 '62 rows in memory/SCOPE_CUTS.md': git show HEAD:memory/SCOPE_CUTS.md | grep -ciE '^\\| *debt' -> 61; the working tree adds one. The other four counts match HEAD: 27 dated reports, 68 decisions, 62 R-IDs, 13 personas.",
   "why_it_matters": "Round 1 asked for counts that match git, and the doc now claims they do. A panelist who opens memory/LESSONS.md finds 28 entries, not 44. In a doc whose area 8 says 'I check evidence, not claims', a count that is 57% too high reads as over-claiming.",
   "fix": "Writer: recount from git show <commit> at the commit you edit in. Or ask the orchestrator to commit memory/LESSONS.md and memory/SCOPE_CUTS.md first, then recount all seven, including the prompt-log reviews after the final prompt-log export.",
   "acceptance_test": "At the submission commit, each of the seven counts on :3, :13, :34, :110 and :114 equals the count from git ls-tree / git show of that commit, using the same grep rule each time."},
  {"severity": "minor", "title": "Area 8 says the D-065 fix 'is committed' as if it were complete; its review had failed twice when this was written",
   "evidence": "HEAD:submission/part2-process.md:114 'demo answers prepared by our team were labeled as AI output; the decision is D-065 and the fix is committed.' board.py show T-177 -> 'review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-177-staff-engineer-r2.md; round 2' at 21:15:23Z, before ddfbf6d (21:27:41); status in_progress. The product note says it accurately: 'fixed in code, final check in progress'.",
   "why_it_matters": "Area 8's example is 'when a bug reaches users'. Calling the fix done while its review is still failing is the exact pattern area 8 says Chris guards against. The two submission docs also disagree on the state of the same fix.",
   "fix": "Match the product note: 'the decision is D-065; the fix is in code and its final review is in progress (T-177)'. Change it to 'done' only when T-177 is done.",
   "acceptance_test": "The D-065 wording in part2-process.md and product-note.md agrees with board.py show T-177 status at the submission commit."},
  {"severity": "minor", "title": "'(NEEDS_CHRIS #9)' is an internal tracking marker in panel-facing text and is not in [CHRIS: ...] form",
   "evidence": "HEAD:submission/part2-process.md:83 'This is my stance until a founder says otherwise (NEEDS_CHRIS #9).' Every other open item in the doc uses '[CHRIS: ...]' (:3, :13, :66, :104, :116, :120). HEAD:submission/NEEDS_CHRIS.md:23 row 9 says '(card pending)', though T-192 exists.",
   "why_it_matters": "The pre-send scrub looks for '[CHRIS:'. This marker would survive into the doc Zlayt reads, and an internal ticket reference in Chris's voice is confusing there. The stale '(card pending)' shows the row-to-card parity check was not re-run.",
   "fix": "Write it as '[CHRIS: confirm or change this stance (NEEDS_CHRIS #9)]' after the paragraph, and keep the sentence 'This is my stance until a founder says otherwise.' Set row 9's card column to T-192.",
   "acceptance_test": "grep -n 'NEEDS_CHRIS #' submission/part2-process.md returns only lines inside [CHRIS: ...] markers; NEEDS_CHRIS row 9 names T-192."},
  {"severity": "nit", "title": "SVG and area 6 wording: 'rebuilt as four steps' reads as done; the engineering example names no card",
   "evidence": "HEAD:submission/validation-ladder.svg:100-101 'which I found very hard to use; rebuilt as four steps (D-068), not yet scored' while T-181 is in_progress (area 4 :58 correctly says 'We are rebuilding'). part2-process.md:83 'In this build a blocker from the staff-engineer reviewer kept a card open until it was fixed.'",
   "why_it_matters": "The tense in the SVG differs from the text. The area 6 example fails the generic-filler test because it does not say which card or what the blocker was.",
   "fix": "SVG: 'being rebuilt as four steps (D-068)'. Area 6: name one card and its blocker in a clause.",
   "acceptance_test": "SVG uses the same tense as area 4; the area 6 example names a card ID."},
  {"severity": "nit", "title": "The cited unit-count file is staged for deletion in the shared index",
   "evidence": "git status --short artifacts/unit-count-33e88c6.txt -> 'D ' plus '??'; git ls-tree HEAD -> present (blob b7958bd).",
   "why_it_matters": "A sweeping commit would remove the evidence for the area 8 test count from git.",
   "fix": "Orchestrator: git restore --staged artifacts/unit-count-33e88c6.txt before the next commit.",
   "acceptance_test": "git ls-files --error-unmatch artifacts/unit-count-33e88c6.txt succeeds."}
 ],
 "whats_right": [
  "Area 4 now says 'a persona score is a screen, not a ship call', which makes the D-068 miss the doc's strongest quality-bar argument. Area 7 reuses it as the honest-feedback example.",
  "The SVG shows only behavior that is committed. The D-066 confirm is labeled in progress, and the split fallback matches docs/LLM_VS_CODE.md.",
  "Area 6 now covers all three parties: engineering's 'how' rights and veto, evidence first, then the safer answer, then the founder. It also gives turnaround times and a week-by-week 30-day plan."
 ],
 "questions_for_chris": []}
```
