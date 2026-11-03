# T-218 review: product-manager-reviewer (Dana Okafor, fictional)

**Verdict: pass.** Both majors left open in `reviews/GATE-M3M4-verify-pm-r2.md` are closed at HEAD e0d721d. I found no blockers and no majors. Four minors and one nit remain.

## The two open majors

| Major (from verify-pm-r2) | Status at HEAD e0d721d | Evidence |
|---|---|---|
| Ship-bar row 5 said "pending re-run" and cited the red f6d5c19 run | **closed** | `git show HEAD:submission/product-note.md` row 5 (line 19): "Tests at 43ce6eb, fresh archive: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run ... `artifacts/gate-M3M4-suite-f6d5c19.txt`)". Part 2 line 114 says the same ("5,945 passed, 0 failed, 12 skipped", "614 passed, 0 failed, 1 skipped"). `git show HEAD:artifacts/gate-M3M4-suite-final.txt` is committed in c2dd104 and reads "unit 5945 passed, 0 failed, 12 skipped exit 0", "e2e 614 passed, 0 failed, 1 skipped exit 0", "letter ... value 0", "spec ... spec_matches_golden true, letter_equal true, internal_notes_equal true". `git ls-tree HEAD` keeps both suite files. "pending re-run" is absent from the note, Part 2, NEEDS_CHRIS, the checklist and the email. |
| The video still showed the old date sentence | **closed** | c2dd104 (08:50:49) re-recorded `artifacts/demo.webm` (21,575,056 to 24,236,670 B), after the wording fix in 43ce6eb (08:04:55). The working tree file equals HEAD (`git hash-object` = `git rev-parse HEAD:artifacts/demo.webm` = 5de844ef). I sampled 30 frames every 6 s (`artifacts/review-evidence/T-218-pm/frames/`) and ran tesseract on all of them: 0 hits for "code can read", "statement dated", "will be burned" or "pending re-run". Frame t126 (Step 3, Austin Imaging MRI $2,150.00) reads "The letter does not take a date of service from the records." The Saved line and the Undo button are fully visible above the caption band. Frames t156 and t162 show the exported letter: "date of service [__________] (record dated May 29, 2026): $2,150.00". |

## The other checks you listed

- **"will be burned in":** `git show HEAD:<file> | grep` on the note, Part 2, NEEDS_CHRIS, the checklist, the email draft, README, CAPTIONS and NARRATION returns nothing. NEEDS_CHRIS:26 and checklist row 2 say the captions are burned in.
- **"statement dated":** zero hits in the note, Part 2, NEEDS_CHRIS, the checklist, the email, README, `docs/LLM_VS_CODE.md`, SCOPE_CUTS and `app/`. It remains only in `submission/prompt-log/` transcripts, reviews and decision logs, which are history. One related phrase survives (finding 1).
- **PDFs match:** `pdfinfo` gives 1 page for the note and 4 for Part 2. `pdftotext` of both HEAD PDFs shows the 5,945/614 counts, both suite paths and no "pending re-run". Both PDFs and both .md files last changed in a932fc9, and `cmp` shows the working-tree PDFs are identical to HEAD.
- **Check I ran beyond your list:** a fresh `git archive HEAD` unit run (ANTHROPIC_API_KEY unset) gave **5951 passed, 6 skipped, 0 failed** in 466 s. The skip count differs from the file's 12 and the total is the same, 5957, so it is an environment difference. `python -m evals.letter_check` at HEAD returns value 0 over 25 cases. I did not re-run e2e at HEAD (about 14 min), so I make no claim about it.

## Why it is a pass, and what remains

The ship-bar row now has a number, a method and a result, and the failed run is disclosed next to it. The video matches the app at HEAD for the sample case. What is left is stale status wording and one gap in the evidence trail, listed as minors below.

```json
{"card": "T-218", "persona": "product-manager-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD e0d721d (T-218 fixes in c2dd104 and a932fc9; D-075 code change cd7fd27 after them); submission/{product-note,part2-process}.md + PDFs, SUBMISSION_CHECKLIST.md, NEEDS_CHRIS.md, email-draft.md, artifacts/{demo.webm,demo.vtt,gate-M3M4-suite-final.txt}; no app URL used; sample case via the video",
 "exercised": [
  "Read personas/product-manager.md and reviews/GATE-M3M4-verify-pm-r2.md",
  "git rev-parse --short HEAD gives e0d721d; git log for the video, PDFs, notes and service_date.py; git show --stat c2dd104 and cd7fd27",
  "git show HEAD:artifacts/gate-M3M4-suite-final.txt (header and RESULTS block)",
  "git show HEAD: grep of product-note.md, part2-process.md, NEEDS_CHRIS.md, SUBMISSION_CHECKLIST.md, email-draft.md, README.md, SCOPE_CUTS.md, LLM_VS_CODE.md, CAPTIONS.md, NARRATION.md for 'pending re-run', 'will be burned', 'statement dated', 'code can read'; git grep over app/",
  "pdfinfo + pdftotext on both HEAD PDFs; cmp of HEAD PDFs against the working tree; grep of the extracted text for 5,945, 614, the suite paths and stale phrases",
  "git hash-object artifacts/demo.webm against git rev-parse HEAD:artifacts/demo.webm; frames.py every 6 s (30 frames in artifacts/review-evidence/T-218-pm/frames); viewed t114, t126, t138, t156, t162; tesseract OCR over all 30 frames",
  "git archive HEAD into artifacts/review-evidence/T-218-pm/tree; pytest tests/unit there: 5951 passed, 6 skipped, 0 failed (artifacts/review-evidence/T-218-pm/unit-head.txt)",
  "python -m evals.letter_check at HEAD: value 0, 25 cases",
  "board.py show T-218; board.py list for T-211, T-212, T-215, T-216, T-217; reviews/GATE-M3-summary.md; board/milestones.md"
 ],
 "verdict": "pass",
 "scores": {"ship_bar_row5_backed_by_committed_run": 5, "video_matches_app_at_head": 5, "pdfs_match_markdown": 5, "stale_wording_removed": 4, "status_statements_current": 3, "evidence_trail_reaches_head": 3},
 "findings": [
  {"severity": "minor", "title": "The note and Part 2 still say the blank shows 'the record or statement date', but D-075 prints only 'record dated'",
   "evidence": "product-note.md:25 and part2-process.md:116: 'a fillable \"date of service [__________]\" with the record or statement date in parentheses, and no service date is extracted'. HEAD docs/LLM_VS_CODE.md:31 and memory/SCOPE_CUTS.md:113 say '(record dated X)', and the video frames t156 and t162 show '(record dated ...)'. cd7fd27 (D-075) made the label always 'record'",
   "why_it_matters": "This is the same date-rule wording that was my round-1 blocker B1. The product never prints a statement date any more, and the note says it sometimes does. It is mild because the blank is still unfilled either way.",
   "fix": "Writer: change to 'with the record date in parentheses', then re-render both PDFs.",
   "acceptance_test": "git show HEAD:submission/product-note.md | grep -c 'record or statement' returns 0, likewise for part2-process.md, and pdftotext on both PDFs finds no 'record or statement'."},
  {"severity": "minor", "title": "The cited green run is one code commit behind HEAD, and the note does not say so",
   "evidence": "Row 5 says 'Tests at 43ce6eb'. git log shows cd7fd27 (D-075, 09:12) changed app/backend/export.py, service_date.py, store.py, app/frontend/guided/step3.js, evals/letter_check.py and 6 test files, after the 08:50 suite record. The only post-change check on the board is the backend note: '124 unit + 110 guided e2e + test_round2 pass; letter_check 0 violations; check-spec true (archive copy)'. My own HEAD unit run is green (5951/0), but no committed file covers e2e at HEAD",
   "why_it_matters": "A reader takes 'tests green' as the shipped build. The label is true for 43ce6eb. The changed code is the exact text of the charge line in the letter, which is the one place a wrong word is expensive.",
   "fix": "Either re-run unit and e2e on the final commit and cite the new file, or add one clause to row 5 and Part 2:114: 'cd7fd27 (record-dated label) came after this run; unit re-run at HEAD: 5,951 passed, 0 failed'.",
   "acceptance_test": "Row 5 names a suite file whose header commit has no later change under app/ or tests/, or states the later commit and what was re-run on it."},
  {"severity": "minor", "title": "The gate-status sentence is stale: 'fixes in progress' and 'fix round is in progress'",
   "evidence": "product-note.md:26 'The combined M3+M4 gate failed with four blockers; fixes in progress.' part2-process.md:114 'failed with four blockers, and its fix round is in progress.' Both PDFs repeat it (note.txt:48, part2.txt:226). reviews/GATE-M3-summary.md says 'Result: pass (round 2, combined M3+M4 panel under D-075)', and board/milestones.md shows the M3 gate_result pass at 2026-11-03T15:18:34Z. T-215 and T-216 are done on the board",
   "why_it_matters": "This is the 'In progress' status defect from round 1 in a new place. The note undersells a passed gate and tells Zlayt the build is still being fixed.",
   "fix": "Say what happened in the past tense: 'the combined M3+M4 gate failed with four blockers, all fixed and verified (fixes at 43ce6eb and later)'. Re-render both PDFs; the note must stay at 1 page.",
   "acceptance_test": "grep -c 'fixes in progress\\|fix round is in progress' on both .md files returns 0; the note PDF is still 1 page."},
  {"severity": "minor", "title": "Checklist section 7 still lists T-215 and T-216 as pending with their failure counts",
   "evidence": "SUBMISSION_CHECKLIST.md:85 '| T-215 | backend | ... 10 unit failures |', :86 '| T-216 | frontend | ... 6 e2e failures |', :30 '(the spec copy of it is being aligned, T-215)'. The same §7 row 88 says 'Gate suite ... Done'. board.py list: T-215 done, T-216 done",
   "why_it_matters": "The page Chris acts from contradicts itself and the board: red counts are listed as pending next to a row that says the suite is green.",
   "fix": "Move T-215 and T-216 out of 'pending' (or mark them done at 43ce6eb) and drop 'is being aligned' from line 30.",
   "acceptance_test": "§7 lists only cards that are not done on the board; grep 'being aligned' returns nothing."},
  {"severity": "nit", "title": "Small leftovers from my round-2 notes: the T-217 owner and the video length",
   "evidence": "SUBMISSION_CHECKLIST.md:87 '| T-217 | qa |' while board.py shows role release. Checklist row 2 and NEEDS_CHRIS:26 say '174 s'; frames.py measured 173.16 s for the HEAD video",
   "why_it_matters": "These are small mismatches with the board and the file.",
   "fix": "Owner release; '173 s'.",
   "acceptance_test": "The §7 owner matches board.py show T-217; the stated length is within 1 s of the video."}
 ],
 "whats_right": [
  "Row 5 now carries a number, a method, a committed evidence file and the earlier red run side by side, so a reader can see that the failure was found and fixed.",
  "The re-recorded video matches the app: the new date sentence on the MRI charge, '(record dated ...)' in the Step 3 list and the exported letter, and Saved and Undo no longer hidden by the caption band.",
  "The PDFs were re-rendered in the same commit as the markdown (1 and 4 pages) and match it line for line on the counts and paths."
 ],
 "questions_for_chris": []}
```
