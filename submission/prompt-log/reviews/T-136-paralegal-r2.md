# T-136 round 2, paralegal re-check (paralegal-reviewer, Maria Delgado persona)

Verdict: **changes** (0 blockers, 1 major, 1 minor). Pinned commit 07c7558 (HEAD at review start; contains 4872cdb, the r2 commit). I ran `git archive 07c7558` into the scratchpad (`r2-07c7558`) and served it on 127.0.0.1:7931 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. The server (PID 11479) was stopped: `lsof -iTCP:7931 -sTCP:LISTEN` exit 1, curl 000. Port 7860 was not touched. Scripts and outputs: `artifacts/review-evidence/T-136-paralegal-r2/`.

## The two things I was asked to check

**1. After she compares an edit, the row no longer reads "Needs review" beside "Accepted": passes.**
- Summary edit on record 3 (sample case, fixture, judge unavailable). Before compare the row chips are "Needs review | Edited". After "I compared it with the quote" they are "Compared by you | Accepted". The row text has no "Needs review". The reason line reads "Compared by you with the quote. The second AI check did not run." Header "3 items need review" and progress "2 of 23 decided" agree. (`q1b-run.stdout.txt`, lines "[after compare]"; `q1-after-compare.png`)
- The same holds for the quote-picker edit on record 1 (`q3-run.stdout.txt`, "RESULT row has 'Write the summary': True ; 'Run the second check' in row: False ; 'Needs review' in row: False").
- The copy warning now names the record: "1 edited entry still marked Needs review (compare with the quote): Record 3, Dr. Alvarez, primary care." That closes round-1 F-5. After compare the warning drops that clause.
- The letter after the compare carries my reworded summary and the verbatim quote with `Source [Ex. __ / Bates __]`. The notes list it under EDITED ITEMS with "accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE)" (`q1b-notes-after-compare.txt`:36).

**2. A re-picked quote still held under D-058: the row and the blocker row are honest and offer "Write the summary"; the case-level steps still offer a rerun (major, F-1).**
- Before she accepts (record 1, quote re-picked, AI summary kept), the row says: "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter: the export stays blocked until the second check answers (Run the second check again) or you edit the summary in your own words." The EDIT_NOT_CONFIRMED warning says the same. (`q3-run.stdout.txt`, "[after quote pick (before accept)]" and "gate warnings")
- After compare, the row shows "Compared by you. You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it." with a "Write the summary" button and no rerun button in the row. The export blocker row (`gate-blocker`) shows only "Go to item" and "Write the summary". (`q3-after-compare.png`)
- "Write the summary" opens the textarea on the row with focus in it, prefilled. I saved my own wording (dropped "transported to Central ER"), compared again, and the letter then carried record 1 with the narrowed quote (`q3-letter-after-own-summary.txt`). That path works end to end.
- Not closed: see F-1.

## Findings

**F-1 (major). The case-level steps still offer "Run the second check again" for the held re-picked quote, and tell her to dismiss the item if it fails. D-058 says the way out is writing the summary.** The brief for this card says the UI must not offer a rerun that cannot clear the hold. With record 1 as the only blocker, I counted three rerun buttons on the export screen (`btn-rerun-judge`, `q4-run.stdout.txt`, "RERUN BUTTON" lines): in "Second AI check on every AI-made item" ("Run it again; accepted items it never checked cannot go in the letter"), in "Ready to export?" ("1 accepted item has not been double-checked by the second AI check, so the export is blocked. Run the second check again."), and in the case rail. The rail's own sentence is: "1 accepted item never got the second AI check, so the export is blocked. Run the second check again; if it still cannot answer, dismiss that item." (`app/frontend/stepper.js:275`; `app/frontend/judges.js:28`, `TODO_BLOCKED`, same wording). I clicked the first one. POST /rejudge returned `still_unavailable: [e1]` and the page said "The second check still did not answer for 1 item of 1. Try again, or dismiss it." (`q4-run.stdout.txt`, "after rerun click"). So in this build the button does nothing for the held item, and the sentence beside it sends her to dismiss an entry she could keep by writing the summary. The row and blocker row say the right thing; the three places a paralegal looks at the moment she presses Export say the old thing. Fix: when every `JUDGE_NOT_RUN` blocker is a compared re-picked quote under the AI summary (the same `secondCheckPending` and `comparedEdit` test the blocker row uses, `stepper.js:478-486`), the gate step and the second-check step say "Write the summary yourself, or wait for the second check", show "Write the summary", and show no rerun button for that item. Keep the rerun for items where it can clear. The server's gate sentence ("Run the second check again.") needs the same treatment, so this needs a backend line as well. Acceptance test: with record 1 as the only blocker (judge unavailable), none of the gate step, "Ready to export?" step and second-check panel contains "Run the second check again" or "dismiss that item", each offers "Write the summary", and clicking it focuses record 1's summary textarea.

**F-2 (minor). Round-1 items outside this card are not re-rated.** F-3 (headline "Ready to export" while an edit is held), F-6 (dismissed amount missing from the internal notes) and F-7 (pass-5 minors) were declared out of scope in the handoff. I did not re-test them. They stay open as the handoff says.

## What I ran

1. `git rev-parse --short HEAD` gave 07c7558. `git archive 07c7558 | tar -x -C <scratchpad>/r2-07c7558`. Server launched with `artifacts/review-evidence/T-060-paralegal-pass4-serve.py` under `.venv/bin/python -I`; curl 200. One slip: my first extract went into the scratchpad root, so a copy of the repo tree now sits among old scratch files; no repo file was touched.
2. `q1-summary-edit-compare.py` (edit with unchanged text) and `q1b-summary-edit-compare.py` (a real reword): save, copy warning before compare, compare, chips, header, export, copy warning after compare.
3. `q2-noop-edit-api.py`: control (plain accept) against an unchanged-text edit, to see whether an unchanged edit could slip an unjudged AI summary into the letter. It cannot: the control summary is judged "verified" in the fixture and the notes are correct. Not a finding.
4. `q3-quote-pick-held.py`: record 1 quote re-pick, row and warnings before compare, compare, row and blocker row, export blocked, "Write the summary", own summary saved, compared, letter and notes.
5. `q4-rerun-offered.py`: located every rerun button on the blocked export screen, clicked one, read the result.
6. `tests/e2e/test_conflict_coverage.py` and `test_edit_to_check.py` from the archive with plain pytest: 23 passed (`artifacts/review-evidence/T-142-legal-nurse/n0-e2e-run.txt`).
7. Screenshot read: `q3-after-compare.png`.

```json
{"card": "T-136", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2; git archive 07c7558 (HEAD at review start, includes r2 commit 4872cdb) served on http://127.0.0.1:7931 (PID 11479, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case evals/golden/sample.txt; live dev app 7860 not touched",
 "exercised": [
  "git archive 07c7558 into a fresh scratchpad dir; server on 7931 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 11479 (lsof exit 1, curl 000)",
  "summary edit on record 3 in the browser: save, copy warning, compare, chips, header, export letter and notes (q1-summary-edit-compare.py, q1b-summary-edit-compare.py)",
  "API control: plain accept against unchanged-text edit, export result (q2-noop-edit-api.py); no finding",
  "quote re-pick on record 1 with the AI summary kept: row and EDIT_NOT_CONFIRMED text before compare, compare, row, blocker row, export blocked, Write the summary, own summary, second compare, letter and notes (q3-quote-pick-held.py)",
  "every rerun button on the blocked export screen located and one clicked; POST /rejudge result read (q4-rerun-offered.py)",
  "tests/e2e/test_conflict_coverage.py and test_edit_to_check.py from the archive: 23 passed",
  "read r1 review reviews/T-136-paralegal.md and D-058 in memory/ORCHESTRATOR_DECISIONS.md; read app/frontend/stepper.js, judges.js, review.js in the archive; screenshot q3-after-compare.png"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "edit_state_agreement": 5, "held_quote_honesty_row": 5, "held_quote_honesty_case_level": 2, "write_summary_path": 5},
 "findings": [
  {"severity": "major", "title": "Case-level steps still offer 'Run the second check again' (and 'dismiss that item') for a held re-picked quote; D-058 says the way out is writing the summary",
   "evidence": "app/frontend/stepper.js:275 'Run the second check again; if it still cannot answer, dismiss that item.'; app/frontend/judges.js:28 TODO_BLOCKED same wording; artifacts/review-evidence/T-136-paralegal-r2/q4-run.stdout.txt: three btn-rerun-judge buttons on the export screen with record 1 as the only blocker; click result 'The second check still did not answer for 1 item of 1. Try again, or dismiss it.' and POST /rejudge still_unavailable [e1]; server gate text '1 accepted item has not been double-checked by the second AI check, so the export is blocked. Run the second check again.'",
   "why_it_matters": "The row and the blocker row say write the summary, but the rail, the Ready to export step and the second-check panel, which are what she reads when she presses Export, still send her to a rerun that cannot clear the hold and then to dismiss an entry she could keep. The brief says the UI must not offer a rerun that cannot clear it.",
   "fix": "When every JUDGE_NOT_RUN blocker is a compared re-picked quote under the AI summary (secondCheckPending and comparedEdit, as in stepper.js:478-486), have the gate step, the Ready to export step and the second-check panel say to write the summary yourself or wait for the second check, show Write the summary, and show no rerun button or 'dismiss that item' for that item. Keep the rerun where it can clear. The server gate sentence needs the same change (backend line).",
   "acceptance_test": "e2e: record 1 re-picked, compared, judge unavailable, only blocker: none of the gate step, Ready to export step and second-check panel contains 'Run the second check again' or 'dismiss that item'; each offers Write the summary; clicking it focuses record 1's summary textarea."},
  {"severity": "minor", "title": "Round-1 items declared out of scope are not re-rated and stay open",
   "evidence": "memory handoff on card T-136: 'case-checks headline still says Ready to export while an edit is held (backend, F-3); F-6/F-7 not in scope'; reviews/T-136-paralegal.md F-3, F-6, F-7",
   "why_it_matters": "A held edit under a Ready to export headline, and a dismissed amount that the internal notes never name, are still what the round-1 review said. Not re-tested here.",
   "fix": "As in reviews/T-136-paralegal.md F-3, F-6 and F-7.",
   "acceptance_test": "As in reviews/T-136-paralegal.md F-3 and F-6."}
 ],
 "whats_right": [
  "After compare the row reads 'Compared by you | Accepted' with 'Compared by you with the quote. The second AI check did not run.'; header, progress and copy warning agree (copy warning now names 'Record 3, Dr. Alvarez, primary care').",
  "A held re-picked quote says so before she accepts and after (row, EDIT_NOT_CONFIRMED text, blocker row), and 'Write the summary' opens the summary textarea on the row and gets record 1 into the letter with her own wording.",
  "A quote-only edit now reads 'Quote changed by you ... Original quote: ...' with the original excerpt; no 'undefined'."
 ],
 "questions_for_chris": []}
```
