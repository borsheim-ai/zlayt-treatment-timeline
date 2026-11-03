# GATE-M3M4 verify pass: product-manager-reviewer (Dana Okafor, fictional), final

This file replaces `reviews/GATE-M3M4-verify-pm.md`. I wrote that file before the unit run finished, and it still holds UNIT_RESULT placeholders. Reviews are write-once, so I could not fill them in there. The verdict and the findings are the same; this copy has the measured unit result.

**Verdict: changes.** All 4 blockers are fixed at HEAD 43ce6eb. I found no new blockers. Of the 5 majors, 3 are closed and 2 stay open:
1. The misleading "code can read" sentence is gone from the app, but it is still on screen in the demo video. The video was re-recorded at 38655da, before the wording fix landed in 43ce6eb.
2. Ship-bar row 5 still says "pending re-run" and cites the red f6d5c19 run. The suites are now green at 43ce6eb (unit 5951 passed and 0 failed in my own archive run; e2e 614/0 per T-216; check-spec all true), but no committed evidence file names a green commit, and the row has not been filled in.

## Blockers from GATE-M3M4-product-manager.md

| # | Blocker | Status at 43ce6eb | Evidence |
|---|---|---|---|
| B1 | Date rule over-claimed | **fixed** | product-note.md:25 and part2-process.md:116 say "every charge line prints a fillable 'date of service [__________]' ... no service date is extracted (D-073, row 28)". pdftotext on both HEAD PDFs (note 1 page, Part 2 4 pages) shows the same text at note.txt:45 and part2.txt:233. `grep 'date-of-service column'` on both PDF texts returns nothing. |
| B2 | Snapshot prunes video, screenshots, ladder svg | **fixed** | HEAD snapshot_tool.py ALLOW adds `artifacts/screenshots/final/`, `artifacts/demo.webm` and `app/frontend/`. prune_sim on a git-archive of 43ce6eb keeps 72 pngs under final/ (73 files with _captions.json), keeps demo.webm (21,575,056 B, the captioned one) and keeps guided/validation-ladder.svg. The 185 files it deletes are old `artifacts/screenshots/*.png`, and no README, submission, CAPTIONS, NARRATION or SNAPSHOT link points at them (the only hit is the frozen CONTRACT.md:252). SNAPSHOT.md:33 says the video pixels are not OCR-checked and must be looked at by eye. |
| B3 | SCOPE_CUTS rows 24-28 not committed | **fixed** | `git show HEAD:memory/SCOPE_CUTS.md` has rows 24-29. Row 28 now says "No service date is extracted for the letter: every charge line prints the fillable blank" (31122d7). The debt-row count of 65 in Part 2:116 matches `count_at_HEAD.sh HEAD`. |
| B4 | README reviews/ claim | **fixed** | README.md:91: "reviews/ holds the reviews tracked in git, and the full set is in submission/prompt-log/reviews/". At HEAD, reviews/ tracks 136 files and submission/prompt-log/reviews/ tracks 502. |

## Majors

| # | Major | Status | Evidence |
|---|---|---|---|
| M1 | "In progress (T-211)" statuses | **fixed** | Part 2:7 is in the present tense. The note has no "In progress (T-211)". The checklist §7 pending list matches `board.py show`: T-215, T-216 and T-217 are in_review, T-187 is blocked, T-022/T-190/T-191/T-193 are needs_chris. Some future tense remains (minor below). |
| M2 | Ship-bar row 5 at an old green commit | **open** | See finding 2. |
| M3 | "code can read" text | **app fixed, video not** | `git grep -n "code can read" HEAD -- .` returns only a prompt-log transcript about Replit. service_date.py:140 now reads "The letter does not take a date of service from the records." In demo.webm, frame t126 (MRI charge, Step 3) still shows "The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note)." |
| M4 | Silent video | **fixed** | 38655da burns captions into the video and adds artifacts/demo.vtt (50 cues). The frames I sampled at t054 ("code checks that the quote is in the record word"), t078 ("This page, linked at the top of every screen,"), t126 and t156 show the caption band. Duration 173.4 s, 1280x800. |
| M5 | (minors from round 1) | n/a | Under D-075 these are SCOPE_CUTS row 29 debt, so I did not re-check them. |

```json
{"card": "GATE-M3M4", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "verify pass at HEAD 43ce6eb (commits 9ea3af8, db36531, ada93fc, 31122d7, 38655da, 6371a28, 43ce6eb since cc9386a); README.md, submission/{product-note,part2-process}.md + PDFs, SUBMISSION_CHECKLIST.md, NEEDS_CHRIS.md, email-draft.md, memory/SCOPE_CUTS.md, deploy/snapshot_tool.py + SNAPSHOT.md, artifacts/{demo.webm,demo.vtt,NARRATION.md,CAPTIONS.md,screenshots/final}, app/backend/service_date.py; git-archive copy of 43ce6eb in artifacts/review-evidence/GATE-M3M4-verify-pm/tree",
 "exercised": [
  "Read personas/product-manager.md, my memory, reviews/GATE-M3M4-product-manager.md, and D-075 at HEAD",
  "git log/show --stat for the seven fix commits; git rev-parse --short HEAD gives 43ce6eb",
  "git show HEAD: grep of the note, Part 2, checklist, email, NEEDS_CHRIS, README, CAPTIONS and NARRATION for the date rule, status words and video",
  "pdfinfo + pdftotext on both HEAD PDFs (artifacts/review-evidence/GATE-M3M4-verify-pm/note.txt, part2.txt)",
  "git archive 43ce6eb into review-evidence/GATE-M3M4-verify-pm/tree, then prune_sim.py with the HEAD ALLOW literals: would delete 185 (old artifacts/screenshots/*.png, none linked), keep 72 final + demo.webm + validation-ladder.svg + 37 guided + 3 submission",
  "evals.run --check-spec in the archive: {\"spec_matches_golden\": true, \"letter_equal\": true, \"internal_notes_equal\": true}",
  "pytest tests/unit in the archive (ANTHROPIC_API_KEY unset): 1 failed, 5950 passed, 6 skipped in 446 s; the one failure (test_t045_r2 committed latest.json) was caused by my own earlier --check-spec run rewriting the archive copy of latest.json; after restoring it from HEAD, test_t045_r2.py gives 19 passed, so the run is 5951 passed, 0 failed",
  "frames.py on the HEAD demo.webm every 6 s (30 frames in review-evidence/GATE-M3M4-verify-pm/frames/); viewed t054, t078, t126, t156",
  "Viewed artifacts/screenshots/final/27-step3-charge-1440.png (ER charge, new wording)",
  "count_at_HEAD.sh HEAD (debt rows 65); git ls-tree counts for reviews/ (136) and prompt-log/reviews (502)",
  "board.py show on T-022, T-184, T-187, T-188, T-190, T-191, T-193, T-202, T-207, T-211..T-217; git diff --cached --stat on the cited suite file"
 ],
 "verdict": "changes",
 "scores": {"date_rule_stated_truthfully": 5, "assets_survive_snapshot": 5, "cuts_committed": 5, "readme_true": 5, "statuses_current": 4, "ship_bar_row5_backed_by_final_run": 2, "video_explains_ladder": 4, "video_matches_app": 2},
 "findings": [
  {"severity": "major", "title": "The demo video still shows the 'code can read' date sentence; the app fix (43ce6eb) landed after the re-recording (38655da)",
   "evidence": "artifacts/review-evidence/GATE-M3M4-verify-pm/frames/t126.png (Step 3, Austin Imaging MRI $2,150.00): 'The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line.' HEAD app/backend/service_date.py:140: '\"no_date\": \"The letter does not take a date of service from the records.\"'. Commit order: 38655da (re-record, 07:55:57) comes before 43ce6eb (wording fix, 08:04:55). The note at product-note.md:25 says 'no service date is extracted'",
   "why_it_matters": "This is my round-1 major M3 (mislead, which D-075 keeps in fix scope). The video is the asset Zlayt watches. It tells them the code reads date-of-service columns and visit-note dates, while the note and the code say it reads none. The asset now also disagrees with the app it claims to show.",
   "fix": "QA: re-record demo.webm (and the .vtt timings if they shift) from 43ce6eb or later. Re-capture any final screenshot that shows a no_date charge note. Shot 27-1440 already shows the new wording, so check the 390 shot and any other Step 3 MRI shots.",
   "acceptance_test": "A frame sampled on the Step 3 MRI charge in the HEAD demo.webm reads 'The letter does not take a date of service from the records.' No frame shows 'the code can read'."},
  {"severity": "major", "title": "Ship-bar row 5 still reports the red f6d5c19 run as 'pending re-run'; the green 43ce6eb results are not committed or cited",
   "evidence": "product-note.md:19: 'Tests **pending re-run**: 10 unit and 6 E2E failures at f6d5c19 ... fixes in progress (T-215, T-216). Last green: 6,815 unit at 9655f1d'. part2-process.md:114 says the same. SUBMISSION_CHECKLIST.md §7 'Gate suite | qa | Re-run unit and e2e on the final commit ... the counts in ship-bar row 5 are filled then'. Latest results at 43ce6eb: unit 5951 passed, 6 skipped, 0 failed (my archive run), e2e '614 passed, 1 skipped, 0 failed' (T-216 AC1), check-spec all true (my run). `git ls-tree -r --name-only HEAD artifacts | grep suite` gives only gate-M3M4-suite-f6d5c19.txt, and `git diff --cached --stat` shows that file staged for deletion in the shared index (55 deletions) while the note and Part 2 cite it",
   "why_it_matters": "Round-1 acceptance was: 'the cited evidence file names the final submission commit with 0 failed and spec_matches_golden true'. That is not met. As shipped, the note tells Zlayt that the tests are red and fixes are in progress, when the build is green. It also cites an evidence file that one commit without a pathspec would delete.",
   "fix": "QA: run the gate suite once on the final commit and commit artifacts/gate-M3M4-suite-<sha>.txt. Keep the f6d5c19 file, or unstage its deletion with a pathspec restore. Writer: fill row 5, Part 2:114 and checklist §7 with those counts, drop 'fixes in progress' from note:26 and Part 2:114, and re-render both PDFs (the note stays 1 page).",
   "acceptance_test": "git show HEAD:submission/product-note.md | grep -c 'pending re-run' returns 0. Row 5 cites a committed suite file whose header names the final commit, with 0 failed for unit and e2e and spec_matches_golden true. Both pdftotext outputs match."},
  {"severity": "minor", "title": "Future tense and stale numbers on the captions",
   "evidence": "SUBMISSION_CHECKLIST.md:12 'with captions burned into the video once the caption pass lands' and '174 s'; NEEDS_CHRIS.md:26 'the narration will be burned in as on-screen captions' and '174 s'. 38655da landed the captions, and frames.py gives duration 173.4 s",
   "why_it_matters": "These are small status errors in the files Chris acts from.",
   "fix": "Use the present tense: 'captions are burned in (38655da), 173 s'.",
   "acceptance_test": "grep -n 'will be burned\\|once the caption pass' on submission/*.md returns nothing."},
  {"severity": "minor", "title": "The caption band covers the app's bottom line (keys hint, 'Saved ... counted' confirmation, Undo)",
   "evidence": "frames/t054.png: the band hides 'Keys: A says yes, D says no...'. frames/t126.png: it hides 'Saved: amount 1 $6,240.00 counted in the...' and leaves the Undo button half visible behind it",
   "why_it_matters": "The confirmation and Undo show that her decision is recorded and reversible, which is part of the human-step story, and the band hides them. This does not mislead.",
   "fix": "Grow the viewport by the band height or place the band below the page, not over it.",
   "acceptance_test": "In a frame sampled after an accept, both the 'Saved' line and Undo are fully visible."},
  {"severity": "nit", "title": "Checklist §7 lists T-217's owner as qa; the card's role is release",
   "evidence": "SUBMISSION_CHECKLIST.md §7 '| T-217 | qa |'; board.py show T-217 gives role 'release'",
   "why_it_matters": "This is a small inconsistency with the board.",
   "fix": "Change the owner to release.",
   "acceptance_test": "The §7 owner matches board.py show."},
  {"severity": "nit", "title": "(Outside my lens; for staff-engineer) `evals.run --check-spec` rewrites evals/reports/latest.json, so a unit run afterwards fails test_t045_r2",
   "evidence": "In the 43ce6eb archive, after `python -m evals.run --check-spec` the archive latest.json differs from HEAD (`cmp` reports a difference at line 24 and adds letter_equal and internal_notes_equal). The unit run then gives '1 failed ... test_the_committed_latest_json_still_matches_what_record_latest_would_write'. After `git show HEAD:evals/reports/latest.json` overwrote it, test_t045_r2.py gives 19 passed",
   "why_it_matters": "A reviewer or QA who runs the documented check before the suite gets a false red run.",
   "fix": "Make --check-spec read-only, or run it last in the gate script.",
   "acceptance_test": "After --check-spec, `git diff --quiet -- evals/reports/latest.json` succeeds."}
 ],
 "whats_right": [
  "The D-073 fallback is now told truthfully and well in the note, Part 2, both PDFs, SCOPE_CUTS row 28 and the app: every charge line prints the blank, no service date is extracted, and six rounds led to a pre-declared fallback.",
  "The public snapshot now keeps the captioned video, all 72 final screenshots and the How-page ladder svg, and drops only unlinked legacy pictures.",
  "The burned-in captions carry the three-rung explanation on screen ('a different AI model checks the line', 'The AI never has the last word'), so the video explains the judge and the human step without the narration file."
 ],
 "questions_for_chris": []}
```
