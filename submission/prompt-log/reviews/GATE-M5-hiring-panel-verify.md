# GATE-M5 hiring panel — verify at HEAD b05fa81

**Verdict: pass.** The one blocker is closed. Part 2, the product note and the checklist now match the committed record: the M3+M4 gate passed in round 2, the suite is 0 failed, and the prompt log is the final build. No blocker and no major remains. Two small status mismatches remain in the checklist. The [CHRIS] items (One story, stretch reason) are Chris's and are not scored.

## Blocker check (commands run, HEAD b05fa81)
| Claim in the packet | Committed record | Match |
|---|---|---|
| `part2-process.md:114`: gate "failed with four blockers, its fixes (T-215, T-216) are done, and it passed in round 2 ... suite at 0 failed" | `git show HEAD:reviews/GATE-M3-summary.md` line 3: "Result: **pass** (round 2, combined M3+M4 panel under D-075)"; `board.py show T-215` and `T-216`: status "done" | yes |
| 5,945 unit passed / 0 failed; 614 e2e passed / 0 failed | `git show HEAD:artifacts/gate-M3M4-suite-final.txt`: "unit ... 5945 passed, 0 failed, 12 skipped"; "e2e ... 614 passed, 0 failed, 1 skipped"; letter 0; spec true | yes |
| "The prompt log is the final build (commit e0d721d)"; checklist row 4 "final build (T-187, commit e0d721d: 767 transcripts)" | `git show --stat e0d721d`: "T-187 final prompt-log build ... 767 transcripts" | yes |
| `product-note.md:28`: gate passed after T-215/T-216, suite 0 failed | same sources | yes |
| `grep -nE 'in progress\|10 unit failures\|6 e2e failures\|interim\|being aligned\|gate fixes are in'` on the four submission .md files at HEAD | no status hit | yes |
| PDFs | `pdftotext` of `HEAD:submission/part2-process.pdf` (4 pages) and `product-note.pdf` carry the same "passed in round 2", "final build", "56 entries" wording | yes |

## Earlier minors
| Minor | State |
|---|---|
| Ship call after below-bar library result | Fixed: `product-note.md:21` "Ship call. ... stage-0 shadow ... not live matters" |
| "record or statement date" label | Fixed: `product-note.md:25` now "record dated X"; the remaining "statement date" in Part 2 line 116 describes the old bug, not the label |
| Lessons count | Fixed: Part 2 says 56; `bash submission/evidence/count_at.sh e0d721d` prints `lessons 56` |
| Paragraph "cut and shipped" | Fixed: "built without an eval, then cut, D-067" |
| [E] citation without commit | Fixed: "[E] ran at 312efe6; prompts, grounding, judges unchanged since" |
| README hides `FIXTURE_SET=recorded` | Not fixed: `git show HEAD:README.md | grep -n FIXTURE_SET` returns nothing |
| Nit: "cannot drift quietly" (`part2-process.md:36`) | Not fixed (optional) |

## Per-row scores
Unchanged from the first review: R1 4, R2 5, R3 4, R4 5, R5 5, R6 4, R7 4. The fixes remove the misreport that held R6 and R7 down, but R6 and R7 stay at 4 because the stretch reason and the One story are not yet written. Neither is scored here. Note that the writer has not added the time-box line the first review asked for.

**Hire call:** unchanged, lean hire. The packet no longer quotes its own gate as failing. What remains is Chris's to supply.

```json
{"card": "GATE-M5", "persona": "hiring-panel-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD b05fa81 verify of reviews/GATE-M5-hiring-panel.md; submission/{part2-process,product-note,SUBMISSION_CHECKLIST,email-draft}.md and PDFs, README.md, reviews/GATE-M3-summary.md, artifacts/gate-M3M4-suite-final.txt, commit e0d721d",
 "exercised": [
  "git rev-parse --short HEAD (b05fa81); git show --stat b05fa81 and e0d721d",
  "git show HEAD:reviews/GATE-M3-summary.md and HEAD:artifacts/gate-M3M4-suite-final.txt",
  "git show HEAD:<path> + grep for stale-status phrases in part2-process.md, product-note.md, SUBMISSION_CHECKLIST.md, email-draft.md, prompt-log/README.md, README.md",
  "pdftotext on HEAD copies of part2-process.pdf and product-note.pdf; pdfinfo page count",
  "board.py show T-187, T-215, T-216, T-217, T-218, T-193; board.py status --brief",
  "bash submission/evidence/count_at.sh e0d721d (lessons 56)"
 ],
 "verdict": "pass",
 "scores": {"R1_builder_mindset": 4, "R2_technical_fluency": 5, "R3_ai_judgment": 4, "R4_workflow_obsession": 5, "R5_communication": 5, "R6_delivery_leadership": 4, "R7_self_direction_clarity": 4},
 "findings": [
  {"severity": "minor", "title": "Checklist marks T-217 done, and T-187 built, while the board still has both in_review",
   "evidence": "submission/SUBMISSION_CHECKLIST.md:85 'T-215, T-216, T-217 | backend, frontend, qa | Done.'; `python3 tools/board.py show T-217` status \"in_review\"; `show T-187` status \"in_review\" (checklist :83 'Final prompt-log build is done (e0d721d)').",
   "why_it_matters": "Same class as the first blocker, but small: a status line that the board does not back. T-217 is an allow-list card, not something that misleads on the product.",
   "fix": "Say 'T-217 in review' (or wait for the review to close) and 'T-187 built, in review'.",
   "acceptance_test": "Every T-### status in SUBMISSION_CHECKLIST.md equals `board.py show` at the commit it is rendered from."},
  {"severity": "minor", "title": "Stretch line still has no time box or cost of the two extra items (writer part)",
   "evidence": "submission/product-note.md:9 'I shipped three ... [CHRIS: your reason, one line.] The cost: billing took four rounds.' Brief: 'pick at most one ... Time-box it.'",
   "why_it_matters": "Disclosed, and Chris's reason is excluded from the score. The writer-side line (time spent against the box) is still missing. This was a major in the first review; it is minor now because the remaining gap is Chris's input.",
   "fix": "Add one sentence with the hours spent on the three items from SCOPE_CUTS or the board; Chris adds the reason (T-191).",
   "acceptance_test": "The stretch line states time spent and has no placeholder once T-191 is answered."},
  {"severity": "minor", "title": "README still hides the offline way to see the model's own recorded answers",
   "evidence": "`git show HEAD:README.md | grep -n FIXTURE_SET` returns nothing (carried from the first review).",
   "why_it_matters": "Zlayt opens the demo and sees only prepared answers; the real recorded output needs no key and they would not find it.",
   "fix": "Add one README line: 'See the model's own recorded answers on the sample: FIXTURE_SET=recorded ./run.sh'.",
   "acceptance_test": "README names FIXTURE_SET=recorded."}
 ],
 "whats_right": [
  "Gate state, suite counts, prompt-log commit and lessons count now re-run to the same numbers as the committed files, in Markdown and in both PDFs.",
  "The product note now states a ship call (stage-0 shadow, not live matters) beside the below-bar library numbers.",
  "The first-review traps, export test and scores were not touched by this fix round."
 ],
 "questions_for_chris": [
  "Why three stretch items (T-191), and how many hours did they take?"
 ]}
```
