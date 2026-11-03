# GATE-M3M4 — product-manager-reviewer (Dana Okafor, fictional), also Chris's double-check of the assets and the packet

**Verdict: fail.** There are 4 blockers, 5 majors and 4 minors.

The numbers are honest. Every eval figure in the note, Part 2 and the email traces to a committed report, and I recomputed them. Provenance is told truthfully everywhere: "Prepared by our team", "Found by code", "recorded AI answers", and "persona, not a real paralegal". The in-app ladder shows each item's code check, the second AI check with its model id, and the human decision, and the video and screenshots show all of it.

The packet still fails in four places:
1. **It over-claims the date feature.** The note and Part 2 describe the round-6 date-of-service rule as built. At HEAD the D-073 fallback is what shipped: every charge line prints a blank.
2. **The demo assets are lost in the public repo.** The repo Zlayt receives is the public snapshot, and its image allow-list deletes `artifacts/demo.webm`, all 72 `artifacts/screenshots/final/*.png` and the in-app ladder picture. No NEEDS_CHRIS row says where the video goes.
3. **The cited cut is missing.** "SCOPE_CUTS row 28", cited by the note, Part 2, LLM_VS_CODE and export.py, is not committed.
4. **The README misstates the reviews.** The front door says `reviews/` holds every review in full. HEAD tracks 136 of them, and the full set is in `submission/prompt-log/reviews/`.

**Scope.** Pinned at 5974034. HEAD moved to cc9386a during the review, but that commit only adds `artifacts/gate-M3M4-suite-f6d5c19.txt`. App code at HEAD equals f6d5c19 (`git diff --stat f6d5c19 HEAD -- app` is empty). Everything was read with `git show HEAD:<path>`.

## Commands and outputs (state claims)

- `git show HEAD:deploy/snapshot_tool.py` gives line 41: `ALLOW = ("artifacts/screenshots/guided/", "artifacts/mockups/", "submission/")`, and `.webm` is in MEDIA_EXT (line 43). `make_public_snapshot.sh:48` runs `prune`.
- `python3 -I artifacts/review-evidence/GATE-M3M4-pm/prune_sim.py …` run on a `git archive HEAD` copy of the assets gives `would delete 258 kept 39`: `delete 1 under artifacts` (demo.webm), `delete 72 under artifacts/screenshots/final`, `keep 37 under artifacts/screenshots/guided`, `keep 2 under submission`.
- `git ls-tree -r --name-only HEAD | grep -E '\.(svg|png|…)$' | grep -v '^artifacts/\|^submission/'` gives `app/frontend/guided/validation-ladder.svg`, which is used by `app/frontend/guided/how.js:33` (`src: "/validation-ladder.svg"`).
- `git show HEAD:memory/SCOPE_CUTS.md | grep -c "^| 2[4-8] "` gives `0`. `git diff HEAD -- memory/SCOPE_CUTS.md | grep -c "^+| 2[4-8] "` gives `5`, so rows 24 to 28 exist only in the working tree.
- `git ls-tree -r --name-only HEAD reviews | wc -l` gives `136`, `ls reviews | wc -l` gives `532`, and `submission/prompt-log/reviews` at HEAD holds 502 files.
- `git grep -n "__________" HEAD -- app/backend/` gives `export.py:212` "The code extracts no service date for the letter" and `service_date.py:111 BLANK = "date of service [__________]"`. Commit b50952d: "D-073 fallback applied: the letter and Step 3 print the fillable blank on every charge line, no service date extracted".
- `bash artifacts/review-evidence/GATE-M3M4-pm/count_at_HEAD.sh 9655f1d` gives `reviews 502 / reports 27 / decisions 68 / lessons 28 / debt rows 61 / personas 13 / reqs 62`. Every count in Part 2 matches.
- `git show HEAD:artifacts/gate-M3M4-suite-f6d5c19.txt` gives `unit … 10 failed, 5935 passed` and `e2e … 6 failed, 607 passed`, plus `{"spec_matches_golden": false, …}`.
- `pdfinfo` gives a note PDF of 1 page and a Part 2 PDF of 4 pages. `pdftotext` shows both PDFs carry the same stale date sentence and the same "In progress (T-211)" line as the md files.

```json
{"card": "GATE-M3M4", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "HEAD 5974034 (then cc9386a, +1 qa results file); README.md, artifacts/{demo.webm,CAPTIONS.md,NARRATION.md,screenshots/final/}, submission/{SUBMISSION_CHECKLIST,email-draft,NEEDS_CHRIS,product-note,part2-process}.md + both PDFs, memory/SCOPE_CUTS.md, docs/LLM_VS_CODE.md rows 2-3, deploy/snapshot_tool.py + make_public_snapshot.sh; app at http://127.0.0.1:7860 (fixture/demo, app tree == HEAD); sample case",
 "exercised": [
  "Read personas/product-manager.md, my memory files, D-065..D-075 in memory/ORCHESTRATOR_DECISIONS.md, and Appendix A of docs/CONTRACT.md",
  "links_in_head.py (artifacts/review-evidence/GATE-M3M4-pm/) over README, the checklist, email, NEEDS_CHRIS, the note, Part 2, CAPTIONS and NARRATION: every markdown link resolves at HEAD; the only misses are globs and dirs relative to prompt-log",
  "Sampled demo.webm every 6 s in headless Chromium (no ffmpeg): duration 171.96 s, 1280x800, 30 frames in artifacts/review-evidence/GATE-M3M4-pm/frames/; viewed t000, t024, t072, t078, t102, t126, t150, t156 and t168 against the NARRATION.md timings",
  "Viewed 15 final screenshots: 07-step1-found, 11b, 11c, 15, 16, 18, 22, 23, 29, 31, 32-classic and 42 at 1440; 47-step1-add-demo; 40-step4-letter-390; 11d-how-it-works-390. Diffed the CAPTIONS file list against the committed final/: 72/72 present",
  "prune_sim.py over a git-archive copy of the assets, using the HEAD ALLOW/MEDIA_EXT literals",
  "Recomputed the library sums from evals/reports/library-latest.md (entries 93/120, amounts 47/69 = 0.681, must-flags 34/42 = 0.81) and checked 20261102T164038Z.md (grounding 1.000/242, entry 0.982, amounts 1.000, 40/40, 0 of 10, J3 20/20, J4 12/12): all match the note, Part 2 and the email",
  "git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml app/backend/judges.py: empty, so the live eval is not stale on prompts",
  "count_at.sh 9655f1d (Part 2 counts) and unit-count-9655f1d.txt (6815 passed)",
  "GATE-M3-pm/journey.py against :7860 on the sample (output in GATE-M3M4-pm/journey-sample-7860.out): export blocked before any decision; after accepts the letter has 2 charge lines with the date-of-service blank, total $8,390.00, and the $185 rate is under AMOUNTS NOT TOTALED",
  "pdfinfo/pdftotext on both PDFs at HEAD",
  "board.py show on T-177/T-179/T-181/T-184/T-187/T-188/T-194/T-195/T-202/T-207/T-211..T-214/T-022/T-189..T-191"
 ],
 "verdict": "fail",
 "scores": {"readme_front_door": 4, "judge_and_hitl_explained": 5, "demo_assets_match_screens": 4, "demo_assets_reach_zlayt": 1, "appendix_a_coverage": 2, "numbers_traceable": 5, "built_claims_match_head": 2, "honesty_provenance_persona_cuts": 4},
 "findings": [
  {"severity": "blocker", "title": "The note and Part 2 describe the round-6 date rule as built; HEAD ships the D-073 fallback (a blank on every charge line)",
   "evidence": "submission/product-note.md:25 says 'a charge line prints a service date only from a bill's date-of-service column or its encounter record's own date, else a blank for her (D-071 to D-073, memory/SCOPE_CUTS.md row 28; T-202 review open)'. submission/part2-process.md:116 says 'the pre-declared fallback took over (D-071 to D-073): a service date prints only from a bill's date-of-service column or its encounter record's own date'. Both PDFs carry the same text (pdftotext lines 45-46 and 231-232). HEAD app/backend/export.py:212: 'The code extracts no service date for the letter'. Commit b50952d and the D-074 log: 'the MVP letter prints the fillable blank ... on every charge line; no service date is extracted'. docs/LLM_VS_CODE.md:30: 'is not extracted for the letter'",
   "why_it_matters": "This claims a capability that is not in the build, and the Appendix A note is graded on judgment. Part 2 also calls the round-6 rule 'the pre-declared fallback', which misstates D-073. The real story is stronger: four rounds failed, the team fell back to the most conservative rule as declared in advance, and the cut is recorded. That story is lost.",
   "fix": "Replace both sentences: 'Date reading failed the same way. After six rounds the pre-declared fallback applies: every charge line prints a fillable \"date of service [____]\" with the record or statement date in parentheses, and no service date is extracted (D-073; memory/SCOPE_CUTS.md row 28).' Drop 'T-202 review open' once the gate closes. Re-render with submission/build_pdfs.sh.",
   "acceptance_test": "git show HEAD:submission/product-note.md HEAD:submission/part2-process.md | grep -c 'date-of-service column' returns 0. pdftotext on both PDFs shows 'every charge line'. The note stays 1 page."},
  {"severity": "blocker", "title": "The public snapshot deletes the demo video, all 72 final screenshots and the in-app ladder picture; no delivery path for the Appendix A demo item",
   "evidence": "HEAD deploy/snapshot_tool.py:41 ALLOW = ('artifacts/screenshots/guided/', 'artifacts/mockups/', 'submission/'); .webm in MEDIA_EXT:43; make_public_snapshot.sh:48 runs prune. prune_sim.py gives 'would delete 258': demo.webm, 72 under artifacts/screenshots/final. app/frontend/guided/validation-ladder.svg is also outside ALLOW, and how.js:33 loads it on the 'How each answer is checked' page (D-074(2)). artifacts/CAPTIONS.md:3 says 'Files are in artifacts/screenshots/final/'. README.md:90, SUBMISSION_CHECKLIST.md:12 and email-draft.md:18 ('annotated screenshots in artifacts/screenshots/') point at deleted paths. NEEDS_CHRIS #3 asks for a 'video link' but no row says where to host the video",
   "why_it_matters": "Under D-074, Zlayt receives the demo link and the repo, and NEEDS_CHRIS #2 (P0) makes the snapshot the only repo that may be published. In it, Appendix A item 2 ('demo video or annotated screenshots') is missing, CAPTIONS.md describes 72 files that do not exist, and the in-app ladder picture that explains the judge and the human step 404s when the app runs from a clone. hf_push.sh archives app/ itself, so the hosted demo keeps the svg; the repo does not.",
   "fix": "Add artifacts/screenshots/final/, artifacts/demo.webm and app/frontend/guided/validation-ladder.svg to ALLOW. Give the video its own check: frame-sample it for OCR the way frames.py does, or have Chris look at it by eye and say so in SNAPSHOT.md. Or move the assets under submission/demo/ and update CAPTIONS, README, the checklist and the email. Add a NEEDS_CHRIS row: where the video is hosted (in-repo file vs an unlisted link) and the exact field to paste it into.",
   "acceptance_test": "Run make_public_snapshot.sh, then in the snapshot dir: ls artifacts/demo.webm app/frontend/guided/validation-ladder.svg and ls artifacts/screenshots/final | wc -l returns 73. Every CAPTIONS filename resolves. The snapshot app's /validation-ladder.svg returns 200."},
  {"severity": "blocker", "title": "The cited cut 'SCOPE_CUTS row 28' (and rows 24-27) is not committed",
   "evidence": "`git show HEAD:memory/SCOPE_CUTS.md | grep -c \"^| 2[4-8] \"` gives 0. `git diff HEAD -- memory/SCOPE_CUTS.md | grep -c \"^+| 2[4-8] \"` gives 5. The row is cited by product-note.md:25, part2-process.md:116, docs/LLM_VS_CODE.md:30 and app/backend/export.py:212 ('SCOPE_CUTS row 28'). README.md:97 sends Zlayt to memory/SCOPE_CUTS.md for 'what was deliberately left out'. The working-tree row 28 also still describes the round-6 rule ('Charge lines take a date only from a DOS table cell/period or the encounter record's own date'), not the fallback",
   "why_it_matters": "Appendix A asks you to 'tell us what you cut'. The cut list in the repo Zlayt receives lacks the date-extraction cut, the demo spend-cap cut (24) and the compare-stamp cut (25) that the docs point to. A panel member who follows the citation finds nothing.",
   "fix": "Orchestrator: correct row 28 to the fallback ('no service date is extracted; every charge line prints the blank; reading DOS tables and prose is post-MVP'), then commit rows 24-28 with a pathspec commit.",
   "acceptance_test": "`git show HEAD:memory/SCOPE_CUTS.md | grep '^| 28 '` returns one row that says no service date is extracted."},
  {"severity": "blocker", "title": "The README front door says reviews/ 'holds every review in full'; HEAD tracks 136 of 532",
   "evidence": "README.md:91: '[`reviews/`](reviews/) holds every review in full'. `git ls-tree -r --name-only HEAD reviews | wc -l` gives 136, while `ls reviews | wc -l` gives 532. The full set is submission/prompt-log/reviews/ (502 at HEAD), which is the path the note and Part 2 cite (e.g. submission/prompt-log/reviews/GATE-M3-product-manager.md)",
   "why_it_matters": "This is a false claim in the one file Zlayt is told to start with (D-074). A reviewer who follows it to look at supervision finds most reviews missing, including the ones the note cites.",
   "fix": "Point the row at submission/prompt-log/reviews/ ('every review and gate summary, copied at the final prompt-log build') and describe reviews/ as a partial working copy, or drop it.",
   "acceptance_test": "git show HEAD:README.md | grep -n 'every review' names submission/prompt-log/reviews/. That directory's file count at HEAD is at least the count the README states."},
  {"severity": "major", "title": "The packet still says the D-074 ladder display and the demo assets are 'in progress' or 'pending'",
   "evidence": "product-note.md:7: '**In progress (T-211):** each item will show its code check...'. part2-process.md:7: same. SUBMISSION_CHECKLIST.md:12 (row 2 'pending: T-184'), :13 ('two items in progress'), :32 ('ladder display is pending: T-211'), and §7 lists T-184/T-211/T-212 as pending. All are committed at HEAD: 82217e5 and e22cae8 (T-211), cda2856 and 5974034 (T-184), 6be191f (T-212). The video shows the panel and the page at 1:07-1:28",
   "why_it_matters": "D-074's main ask is that the judge and the human step be visible. The packet under-reports it as future work, and the checklist reads as unfinished.",
   "fix": "After the blocker round: present tense in the note and Part 2 ('Each item shows its code check, the second AI check's verdict and reason, and her decision; a \"How each answer is checked\" page is linked from every screen'). Refresh the checklist statuses and §7 from board.py show, then re-render the PDFs.",
   "acceptance_test": "grep -c 'In progress (T-211)' on both md files and both pdftotext outputs returns 0. Every checklist 'pending' cell names a card whose board.py show status is not done."},
  {"severity": "major", "title": "Ship-bar row 5 ('tests green') is reported at 9655f1d; the gate commit's suite is red and spec_matches_golden is false",
   "evidence": "product-note.md:19 and part2-process.md:114: '6,815 unit tests passed at 9655f1d'. HEAD artifacts/gate-M3M4-suite-f6d5c19.txt: 'unit ... 10 failed, 5935 passed', 'e2e ... 6 failed, 607 passed', '{\"spec_matches_golden\": false, \"letter_equal\": false, ...}'. SUBMISSION_CHECKLIST.md:30 cites 'Byte-exact template evals/golden/sample.export.expected.txt'",
   "why_it_matters": "A ship-bar result must be measured on what ships. At the gate commit, criterion 5's 'tests green' and the spec-equals-golden export check do not hold. Citing an older green commit is the proxy-over-reality pattern the note criticises elsewhere.",
   "fix": "After the fix round, re-run the unit and e2e suites and check-spec on the final commit, and cite that commit's counts and evidence file in the note, Part 2 and the checklist. If anything stays red, report it in row 5 as missed.",
   "acceptance_test": "The cited evidence file names the final submission commit with 0 failed and spec_matches_golden true, or row 5 says 'missed' with the failing count."},
  {"severity": "major", "title": "In-app copy says the code can read service dates; under the fallback it reads none",
   "evidence": "HEAD app/backend/service_date.py:140 'no_date': 'The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note).' It is shown on Step 3 for the MRI charge (demo.webm frame t126) and in the attorney notes (journey-sample-7860.out:130). The ER charge in the same notes reads 'The letter does not take a date of service from the records.' (line 129). CAPTIONS.md:52 describes the second wording, not the one on screen",
   "why_it_matters": "This tells the paralegal, and Zlayt, that a DOS column or a visit-note date would have been read. The fallback reads neither (D-073; export.py:212). Two different reasons appear for the same behaviour in one note. D-075 keeps 'mislead' findings in scope.",
   "fix": "Backend: one reason for every charge line, 'The letter does not take a date of service from the records; fill the blank from the quote or request a dated itemized bill.' Re-capture shot 27 and the Step 3 video segment, or at least align CAPTIONS 27.",
   "acceptance_test": "`git grep -n 'code can read' HEAD -- app` returns nothing. The sample journey's CHARGES WITHOUT A CERTAIN DATE OF SERVICE lines carry identical reasons."},
  {"severity": "major", "title": "The demo video is silent and the narration is optional, so the video does not explain the judge or the human step",
   "evidence": "demo.webm is a Playwright recording (tests/demo_assets/video.py) with no subtitle or caption track. `git grep -i 'audio|vtt|subtitle' HEAD -- tests/demo_assets` returns nothing. NEEDS_CHRIS.md:26: 'Optional, not blocking: read the demo narration (T-184) in your own voice, or leave it as a script.' NARRATION.md 0:49-1:28 carries the three-rung explanation",
   "why_it_matters": "The explanation of the ladder lives in a separate text file a video viewer won't open. On screen the viewer sees clicks and has to find the rung text in the UI on their own. Appendix A grades AI judgment, and D-074 asks the assets to explain the judge and the human step.",
   "fix": "Burn in captions from the NARRATION timings (or ship a .vtt beside the video and play it in an HTML wrapper), or make the voice-over a P1 NEEDS_CHRIS row with the exact recording steps.",
   "acceptance_test": "A frame sampled at 0:55 and at 1:20 shows the narration text, or NEEDS_CHRIS lists the voice-over as P1 with an action and a default."},
  {"severity": "minor", "title": "'Summaries and flags are prepared answers' is no longer exact after T-214 (code-found flags)",
   "evidence": "README.md:66: 'The sample's summaries and flags are **prepared answers** ... labelled \"Prepared by our team\"'. NARRATION.md:11: 'the summaries and warnings were prepared by our team'. Screens 15 and 16 and video t102 show the gap and PT-plan warnings tagged 'Found by code' with 'AI: not needed'",
   "why_it_matters": "This is a small provenance inaccuracy in the files that exist to be exact about provenance (D-065).",
   "fix": "'The sample's summaries and model-proposed warnings are prepared answers; warnings found by code (gaps, the phrase list) are tagged Found by code.'",
   "acceptance_test": "README and NARRATION mention 'Found by code' next to the prepared-answers sentence."},
  {"severity": "minor", "title": "Captions don't say that several shots come from library cases running recorded AI answers; two small caption/narration mismatches",
   "evidence": "Shots 11c, 18, 19, 22, 23 and 29 carry the badge 'Demo: recorded AI answers' and the case names 'Disputed line', 'Warning not confirmed', 'Date to pick' and 'Ledger'. CAPTIONS.md:4 says only that 'the sample lines and warnings were prepared by our team'. CAPTIONS.md:75 says '(this demo can only read the sample case and our test cases)', but the screen reads 'This demo can only read the sample case.' NARRATION.md:25 says 'says Letter ready', but frame t168 reads 'Finished. Your letter is ready.'",
   "why_it_matters": "A reader can't tell which pictures show prepared answers and which show real model output. That is the distinction D-065/D-056 exist for.",
   "fix": "Add '(library case, recorded AI answers)' to those captions and fix the two strings.",
   "acceptance_test": "Each caption whose screen shows 'recorded AI answers' says so, and the two strings match the screen."},
  {"severity": "minor", "title": "The email puts agent-done work in Chris's first person",
   "evidence": "email-draft.md:11 '17 seconds when I timed it'; :25 'On 15 separate test packets I wrote later'. Both were done by agents (deploy/TIMING.md; the library cards)",
   "why_it_matters": "Point 3 of the email discloses the agent team, but these two sentences claim personal actions. The persona red flag is anything attributed to Chris that he did not do.",
   "fix": "'17 seconds when we timed it'; 'On 15 separate test packets written after the golden set'.",
   "acceptance_test": "grep -n 'I timed\\|I wrote' submission/email-draft.md returns nothing."},
  {"severity": "minor", "title": "/classic has no 'How each answer is checked' link (D-074(2): 'reachable from every screen')",
   "evidence": "artifacts/screenshots/final/32-classic-1440.png: the header shows only the 'Demo: sample answers prepared by our team' badge and 'Theme: auto'. CAPTIONS.md:61 presents /classic as kept 'for people who want every control on one page'",
   "why_it_matters": "This is a gap in the literal D-074 requirement on a screen the assets advertise. It is low impact because the guided UI is the front door.",
   "fix": "Add the link to the classic header, or say in SCOPE_CUTS that /classic is exempt.",
   "acceptance_test": "GET /classic contains the how-it-works link test id, or a SCOPE_CUTS row names the exemption."}
 ],
 "whats_right": [
  "Every eval number in the note, Part 2 and the email traces to a committed report and recomputes: grounding 1.000/242, 40/40, J3 20/20, J4 12/12, library 93/120, 47/69, 34/42, and the Part 2 counts at 9655f1d.",
  "Honesty holds where it matters most: 'Prepared by our team' on every sample screen, 'recorded AI answers' on library cases, the persona-not-real-paralegal caveat in the note, Part 2 and the email, and the golden-vs-library gap stated, not hidden.",
  "The ladder is visible per item (Code check: no AI; Second AI check: claude-haiku-5-5 with its verdict and reason; You), a disputed line can't be accepted without the tick, the export holds only accepted items, $185 is never totaled, and the total is $8,390.00."
 ],
 "questions_for_chris": [
  "Where should the demo video live for Zlayt: committed in the public repo (needs the snapshot allow-list change) or an unlisted link (YouTube, Loom or Drive) pasted into the email?",
  "Will you record the narration as a voice-over, or should the team burn the narration in as on-screen captions?"
 ]}
```
