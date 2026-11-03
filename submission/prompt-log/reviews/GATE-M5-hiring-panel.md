# GATE-M5 — hiring panel (Zlayt founders) — HEAD e0d721d

**Verdict: fail.** There is one blocker, and it is a text fix. The submitted packet tells Zlayt that the M3+M4 gate "failed with four blockers" and that its fix round is "in progress". The checklist still lists open "10 unit failures" and "6 e2e failures". The committed record says the opposite: the gate passed, and both suites are at 0 failed. Everything else is major-or-below. No "What we evaluate" row scores ≤ 2.

## How we ran it (as Zlayt would, from README.md)
- `git archive HEAD` into a new empty directory, then `PORT=7896 ./run.sh`. `.venv` was created and the server answered `/api/health` in **10 s**. A first copy went into a reused scratch dir that held a stale `probe_7/`, which is not in HEAD (`git ls-tree -r HEAD --name-only | grep '^probe_7'` returns nothing). We discarded that copy and re-ran on the clean one. Every server we started (7895, 7896, 7897) was stopped, and `lsof` shows 0 listeners.
- We drove the README 3-minute walk with Playwright (`artifacts/review-evidence/GATE-M5-hiring-panel/walk.py`). Every README label was found verbatim: "We found 9 records"; "19 timeline items and 4 bill amounts are ready for you to check"; "You checked every item on the timeline"; "You checked every bill amount"; "$8,390.00"; "Your letter is ready". The walk took 16.4 s. Screenshots are `01-home.png` to `09-how.png`, plus `fresh/`.
- We tried to break the export through the API. We dismissed e5 (Feb 20 PT), MRI charge a4, flag f_r9_1 and damages a3. The letter then had no Feb 20 entry and no MRI line, and read "Billed charges accepted from these records: $6,240.00". Re-accepting a4 brought it to $8,390.00. Exporting before any review returned `export_blocked` / `NOTHING_ACCEPTED`.
- We also ran the sample with `FIXTURE_SET=recorded`, which replays real `claude-sonnet-5-5` / `claude-haiku-5-5` answers. The same traps held.

## Seven traps (running app, clean copy)
| Trap | Result |
|---|---|
| 73-day gap flagged | `f_gap_r6_r7` "Gap of 73 days"; it is the only gap flag |
| 28-day interval not flagged | no gap flag on r4→r5 |
| 01-09 vs 01-19 not merged | `f_accident_date_after_treatment_1_2_7`; notes: "The tool does not choose between the dates." |
| $185 rate not totaled | `a2` kind `rate`, `not_totaled`; notes: "Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger." |
| Explicit charges = $8,390 | letter "Billed charges accepted from these records: $8,390.00" |
| "may represent degenerative change" kept | e8 "the record states findings may represent degenerative change and to correlate clinically" |
| "concussion without loss of consciousness" kept | e2 "Diagnosed with cervical strain and concussion without loss of consciousness" |

## Per-row scores
| Row | Score | Evidence |
|---|---|---|
| R1 Builder mindset | 4 | It runs in 10 s and works end to end. The cuts are tied to failure modes: D-073 date extraction was cut after six rounds; the paragraph was cut because it had no eval and no verbatim quote (SCOPE_CUTS 22, 28). Against that, the note says it shipped **three** stretch items against "pick at most one", and the reason is a placeholder (`submission/product-note.md:9`). |
| R2 Technical fluency | 5 | Empty input → 400 "Input is empty."; 70k chars → 413; bad JSON → 400. OCR "$1,2OO" stays `unclear`. An injection record gets a banner (golden case_03, case_07). Entries carry date, provider, summary, excerpt and state. Amounts are typed charge, rate, damages or unclear. Prompts are versioned (`judge_conflict_v6`, `judge_flag_v3`), and there are judge controls and `--check-fresh` (exit 0). |
| R3 AI judgment | 4 | Five criteria with bars, results and a must-never (`product-note.md:13-19`; `part2-process.md:38-58`). Library recall below the bar is published (0.775 / 0.681 / 0.81). The note never states the ship call that follows from it. |
| R4 Workflow obsession | 5 | The quote is highlighted beside each line, one item at a time. There is yes / no / fix / later. The letter and the "DO NOT SEND" notes are kept apart. The letter has `[Ex. __ / Bates __]` and a date-of-service blank. The paralegal questions are about how she re-checks today (`part2-process.md:19-21`). |
| R5 Communication | 5 | A real message with a "not this week" escape, and a 30-minute agenda with minute marks (`part2-process.md:97-101`). Concrete moves for unhappy, silent and conflicting users. A Friday one-pager for founders. The developer brief lists spec R-IDs, contract, golden set and card AC. |
| R6 Delivery leadership | 4 | The weekly checks, release counts, sign-off, late-work and escaped-bug sections all use real examples (T-177, T-179, D-073), and AI used vs not is stated (`part2-process.md:110-118`). But area 8 itself misreports the gate state (the blocker). |
| R7 Self-direction and clarity | 4 | A-101..A-109 assumptions, 75 decisions and NEEDS_CHRIS. Placeholders are correct and the One story scaffold is in place. Part 2 is 4 PDF pages with a visual. Some facts are stale or wrong: the lessons count, the "statement date" label, and the paragraph described as both cut and shipped. |

**Would we hire from this?** Lean hire; we need more evidence on one thing. On the evidence that matters to us, this is the strongest kind of take-home. The tool would hold up in front of an adjuster. The ship bar is real and is published, failures included. Part 2 reads like someone who has run discovery and supervised builds. It names artifacts, not frameworks. Two things hold us back. First, the One story is still Chris's to write. Second, "I shipped three stretch items" with no reason given reads as over-building against an explicit time-box. We would ask both in a 30-minute call. Fix the stale status lines before sending: a packet that says its own gate is failing is the first thing we would quote back.

**Filler test (three weakest sentences; none outweighs its section):** "I trust what they do over what they say." (`part2-process.md:93`); "...so the spec and the build cannot drift quietly." (`:36`, overclaim); "Then I iterate: the cheapest fix that moves the weakest number." (`:77`).

```json
{"card": "GATE-M5", "persona": "hiring-panel-reviewer", "model": "claude-opus-5-5",
 "scope": "HEAD e0d721d (git archive into an empty dir); app at http://127.0.0.1:7896 (fresh copy, demo mode) and :7897 (FIXTURE_SET=recorded); sample case Jordan Rivera; README.md, submission/{product-note,part2-process,SUBMISSION_CHECKLIST,email-draft,NEEDS_CHRIS}.md, submission/prompt-log/{README,TOOLS}.md, artifacts/{demo.webm,CAPTIONS.md,NARRATION.md}, docs/LLM_VS_CODE.md, evals/reports/, memory/SCOPE_CUTS.md",
 "exercised": [
  "git archive HEAD into an empty dir; PORT=7896 ./run.sh created .venv and was healthy in 10 s",
  "Playwright README walk (artifacts/review-evidence/GATE-M5-hiring-panel/walk.py): all README labels found verbatim; screenshots 01-09 plus fresh/",
  "API: POST /api/cases sample, /run, GET case: checked all 7 traps on the clean copy",
  "Export break test: dismissed e5, a4, f_r9_1, a3; letter lost Feb 20 and MRI, total $6,240.00; re-accepted a4, total $8,390.00; pre-review export returned export_blocked",
  "Inputs: empty -> 400, 70k chars -> 413, bad JSON -> 400, unknown text in demo -> 409; golden case_03 (OCR $1,2OO unclear) and case_07 (injection banner)",
  "FIXTURE_SET=recorded on :7897: real sonnet/haiku answers, labelled 'drafted by AI', same traps hold",
  "ffmpeg: demo.webm duration 00:02:53.16; frames at 125 s and 158 s (video-125.png, video-158.png) show 'record dated' and $8,390.00",
  "Read product note, Part 2, checklist, email draft, prompt-log README and TOOLS, NARRATION, LLM_VS_CODE head, SCOPE_CUTS rows 22, 26",
  "Verified citations exist at HEAD with git cat-file -e (13 paths, all present); bash submission/evidence/count_at.sh db36531; python -m evals.run --check-fresh (exit 0)",
  "board.py status --brief / show T-187, T-215, T-216, T-217, T-218 / list in_review and blocked; reviews/GATE-M3-summary.md; artifacts/gate-M3M4-suite-final.txt",
  "git diff --stat 312efe6 HEAD -- app/backend app/llm app/llm/prompts (prompts, grounding.py, judges.py unchanged since the live run)"
 ],
 "verdict": "fail",
 "scores": {"R1_builder_mindset": 4, "R2_technical_fluency": 5, "R3_ai_judgment": 4, "R4_workflow_obsession": 5, "R5_communication": 5, "R6_delivery_leadership": 4, "R7_self_direction_clarity": 4},
 "findings": [
  {"severity": "blocker", "title": "Packet tells Zlayt the gate failed and tests are failing; the committed record says pass and green (R6/R7)",
   "evidence": "submission/part2-process.md:114 'the combined M3+M4 gate (D-075) failed with four blockers, and its fix round is in progress'; submission/product-note.md:26 'The combined M3+M4 gate failed with four blockers; fixes in progress.'; submission/SUBMISSION_CHECKLIST.md:85 'T-215 | backend | Gate fix A: ...; 10 unit failures', :86 'T-216 | frontend | Gate fix B: 6 e2e failures', :14 prompt log 'pending: an interim build', :30 'being aligned, T-215', :32 'its gate fixes are in T-216'. Contradicted by reviews/GATE-M3-summary.md:3 'Result: **pass** (round 2, combined M3+M4 panel under D-075)'; artifacts/gate-M3M4-suite-final.txt 'unit ... 5945 passed, 0 failed' / 'e2e ... 614 passed, 0 failed'; `board.py show T-215` status 'done', `show T-216` status 'done'; HEAD e0d721d 'T-187 final prompt-log build'.",
   "why_it_matters": "D-075 blocker class: it misleads Zlayt. A founder reading Part 2 area 8, the section on supervising developers, concludes the delivered build is mid-fix with failing tests. It is not, and the misstatement sits in the very section meant to prove supervision.",
   "fix": "Writer (T-218): state the M3+M4 gate result as passed in round 2 (reviews/GATE-M3-summary.md) in product-note.md:26 and part2-process.md:114. In SUBMISSION_CHECKLIST.md, move T-215/T-216 out of 'Pending', update rows 4, 30 and 32 to the committed state, and mark T-187 as built. Re-render both PDFs with build_pdfs.sh.",
   "acceptance_test": "grep -nE 'in progress|10 unit failures|6 e2e failures|interim build|being aligned|gate fixes are in' submission/*.md returns no status claim that contradicts reviews/GATE-M3-summary.md or board.py; the PDFs contain the same wording (pdftotext | grep)."},
  {"severity": "major", "title": "Three stretch items shipped against 'pick at most one', and the reason is a placeholder (R1)",
   "evidence": "submission/product-note.md:9 '**Stretch:** at most one; I shipped three (source viewer, PDF text layer, calibrated confidence) ... [CHRIS: your reason, one line.]'; brief (docs/CONTRACT.md Appendix A): 'Stretch (pick at most one, only if time remains)' and 'Time-box it.' The note gives no time spent.",
   "why_it_matters": "Disclosed, so it does not mislead. But it is a spec deviation in the row that grades cutting scope on purpose, and with no reason it reads as over-building.",
   "fix": "Chris writes the one-line reason (T-191). The writer adds one line with the time box against the time actually spent, and what the two extra items cost, from SCOPE_CUTS or the board.",
   "acceptance_test": "product-note.md has no placeholder on the stretch line, and it states the time box and the cost of the extra items in one sentence."},
  {"severity": "minor", "title": "No explicit ship call after a below-bar library result (R3)",
   "evidence": "product-note.md:16-17: library entries 0.775, amounts 0.681, must-flags 0.81 against a 0.95/0.9 bar; lines 21-26 explain the misses but never say whether this ships. email-draft.md:25 leads with 'The ship bar is met on my golden set'.",
   "why_it_matters": "We want to see the decision, not just the data.",
   "fix": "Add one sentence, e.g. 'Verdict: meets the bar on golden, below it on unseen packets; ready for a stage-0 shadow only (Part 2 area 5), not live matters.'",
   "acceptance_test": "The product note's ship-bar section contains an explicit ship / no-ship / shadow-only statement."},
  {"severity": "minor", "title": "Date-blank label described as 'record or statement date'; app and video print only 'record dated' (R7)",
   "evidence": "product-note.md:25 and part2-process.md:116 'with the record or statement date in parentheses'. Clean-copy export: 'Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00'. D-075 label simplification (cd7fd27) dropped the statement variant.",
   "why_it_matters": "A small factual mismatch between the documents and the running app.",
   "fix": "Say '(record dated X)' in both places.",
   "acceptance_test": "grep -n 'statement date' submission/product-note.md submission/part2-process.md returns nothing."},
  {"severity": "minor", "title": "Lessons count is wrong in Part 2 (R7)",
   "evidence": "part2-process.md:112 '(`memory/LESSONS.md`, 28 entries)'; `bash submission/evidence/count_at.sh db36531` prints 'lessons    55'; HEAD has 56 '- ' lines.",
   "why_it_matters": "Part 2 promises every count is re-runnable, and this one does not re-run to the same number.",
   "fix": "Use the count_at.sh value.",
   "acceptance_test": "The number in part2-process.md:112 equals count_at.sh output at the stated commit."},
  {"severity": "minor", "title": "Product note says the drafted paragraph was both cut and shipped (R1/R7)",
   "evidence": "product-note.md:9 'Tried, then cut: ... the drafted treatment paragraph (D-067)' and, same line, 'the paragraph shipped with no eval'; memory/SCOPE_CUTS.md:103 row 22 'Cut from the MVP by D-067 ... The route stays in the backend.'",
   "why_it_matters": "A founder reading for cut discipline sees a contradiction.",
   "fix": "Say 'the paragraph was built without an eval, then cut (D-067)'.",
   "acceptance_test": "The note's cut line has no 'shipped' for the paragraph."},
  {"severity": "minor", "title": "README hides the offline way to see the model's own answers (R2)",
   "evidence": "Clean copy with FIXTURE_SET=recorded: /api/health models {'generator': 'claude-sonnet-5-5', 'generator_prepared': False}, banner 'Summaries and flags are drafted by AI', and all traps hold. README mentions FIXTURE_SET nowhere; it says demo answers are 'prepared answers' and live needs ENABLE_LIVE plus a model.",
   "why_it_matters": "We open the demo and see no generator output. The real recorded output exists in the repo and needs no key, but we would not find it.",
   "fix": "Add one README line: 'See the model's own recorded answers on the sample: FIXTURE_SET=recorded ./run.sh'.",
   "acceptance_test": "README names FIXTURE_SET=recorded, and running it shows 'drafted by AI' on the sample."},
  {"severity": "minor", "title": "Live ship-bar run commit not named in the note; 153 commits since (R3)",
   "evidence": "product-note.md:11 cites [E] evals/reports/20261102T164038Z.md, whose line 4 says 'Source commit 312efe66'. `git log --oneline 312efe6..HEAD | wc -l` = 153; `git diff --stat 312efe6 HEAD -- app/backend app/llm` = 29 files, +2037. Prompts, grounding.py and judges.py are unchanged; generator.py changed by 1 line.",
   "why_it_matters": "The numbers likely still hold for the LLM rungs, but the note should say so, as it already does for [L] ('pre-billing redesign').",
   "fix": "Append 'at 312efe6; prompts, grounding and judges unchanged since' to the [E] citation.",
   "acceptance_test": "The [E] citation names its commit and what changed since."},
  {"severity": "nit", "title": "Three weakest sentences (filler test passes)",
   "evidence": "part2-process.md:93 'I trust what they do over what they say.'; :36 '...so the spec and the build cannot drift quietly.'; :77 'Then I iterate: the cheapest fix that moves the weakest number.'",
   "why_it_matters": "Isolated. No section fails the filler test.",
   "fix": "Optional: replace :36 'cannot drift quietly' with the mechanism (check-fresh, spec check).",
   "acceptance_test": "n/a"}
 ],
 "whats_right": [
  "All seven traps hold in the running app on both prepared and recorded real-model answers; a dismissed item leaves the letter and the total moves from $8,390 to $6,240.",
  "Honest quality bar: library recall 0.775 / 0.681 / 0.81 and 'no real paralegal yet' are published beside the golden 1.000s.",
  "The clean-copy ./run.sh is healthy in 10 s and every README walk label matches the app verbatim; the video (2:53) matches HEAD output."
 ],
 "questions_for_chris": [
  "Why three stretch items (T-191)? One line, tied to user value or risk.",
  "How long did this take in wall-clock time, and how many of your own hours? The founders will ask, given 'Time-box it.'"
 ]}
```
