# T-136 paralegal re-check (paralegal-reviewer, Maria Delgado persona)

Verdict: **changes** (0 blockers, 2 majors, 5 minors). Commit 671f054 (HEAD at review start: 671f0543d489e66e62584ae11a61ee135f0f7889). I ran `git archive 671f054` into the scratchpad (`t136-archive`) and served it on 127.0.0.1:7901 (PID 69029, stopped: lsof exit 1, curl 000) with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. The live dev app on 7860 (PID 66274) was not touched. Scripts and outputs: `artifacts/review-evidence/T-136-paralegal/`.

## The two pass-5 majors

| Pass-5 item | Status at 671f054 | Evidence |
|---|---|---|
| F1 part 1: one `a` on an edited row records "I compared it with the quote" and clears the copy warning | Closed. One `a` and a second `a` both leave progress at 1 of 23, show the "Not recorded yet" prompt, and move focus to the compare button. The copy warning still shows before copy. Enter on the focused button records it. | `p2-f1-single-a.out.txt`; `p2-after-one-a.png`; `p2-after-enter-compare.png` |
| F2: dismissed flags and amounts not under "Dismissed (n)" | Closed. "Dismissed (1)" groups exist for flags (`dismissed-group-flags`) and amounts (`dismissed-group-amounts`). Neither item is in the open list. `a` on the dismissed flag leaves progress at 3 of 23. The letter omits the dismissed amount. | `p5-dismissed-groups.out.txt`; `p5-after-dismiss.png` |

The F1 residuals are not closed. The compare leaves "Needs review" beside "Accepted", and that is re-raised as F-1 below.

## Card checks

- **Quote-picker edit shows as open with compare-and-accept: passes.** I re-picked record 1's quote with "Change quote" (dropped "Transported to Central ER."). The server saved it (200). The row reads "Needs review | Edited" with "I compared it with the quote"; the header reads "4 items need review, including 1 edit to check"; the EDIT_NOT_CONFIRMED gate warning appears. Before compare the letter omits record 1. (`p4d-run.stdout.txt`; `p4d-letter-before-compare.txt`; `p4d-after-quote-pick.png`)
- **EDIT_NOT_CONFIRMED before export: present, but collapsed.** The warning is in the case-checks block, behind "Show", under the headline "Ready to export, 22 not reviewed" (F-3). The export view does not repeat it. (`p3-gate-warning.out.txt`; `p3b-gate-expand.out.txt`)
- **Export after compare: blocked for a quote edit (F-2), open for a summary edit.** Details below.
- **Persistence:** same-page reload kept the edit state (`p2-f1-single-a.out.txt`, "after-reload-same-page"). A fresh browser context, opened from the case list, still shows "including 1 edit to check" and the compare button (`p6-fresh-reopen.out.txt`).

## Letter and notes honesty

- The letter before compare holds only the accepted entry (record 1), with `Source [Ex. __ / Bates __]` placeholders. Its quote is verbatim in `evals/golden/sample.txt` (grep -F count 1). No charge is accepted, so the letter has no total line.
- After compare on a summary edit (record 3), the letter carries her reworded summary and the quote. The notes say "accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE)" (`p2g-letter-after-summary-compare.txt`; `p2g-summary-edit-letter-after-compare.out.txt`). That is honest. It is also allowed by D-045(b), which exempts her own summary wording from the judge.
- After compare on a quote-picker edit (record 1) the export is blocked, so there is no letter (F-2).
- The internal notes do not name the dismissed amount "missing 3 days of work" (F-6).

## Findings

**F-1 (major). After she compares an edit, the row still says "Needs review" beside "Accepted".** This is pass-5 F1 fix item 2, which the card did not take. Evidence: `p2-f1-single-a.out.txt`, "[after-enter-on-compare] e3 row: ... | Needs review | Accepted"; `p4d-after-mouse-compare.png` shows the same two chips on record 1 after the mouse compare. The row contradicts her decision. Fix: after the comparison, clear the Needs review chip and give the reason "Compared by you; second AI check not available". Acceptance test: after clicking the compare control on record 3, the row has no "Needs review" chip, and the header and export bar agree on the count.

**F-2 (major). Compare-and-accept on a quote-picker edit leads to an export block that the offered action does not clear.** Before compare the warning says the edit "stays out of the letter until you compare it with the quote and accept it" (`app/backend/trace.py:43`). She compared and accepted record 1 (`p4d-run.stdout.txt`, "progress: 2 of 23 decided"). Export then refused: "The export is blocked. 1 accepted item has not had the second AI check, so the export is blocked. Run the second check again." (`p4e-export-after-compare-debug.out.txt`). The red banner adds: "accepting does not replace it" (`p4d-after-mouse-compare.png`). "Run the second check again" was clicked and the block stayed (`p4f-rerun-after-quote-compare.out.txt`). The block itself follows D-044 (`memory/ORCHESTRATOR_DECISIONS.md:52`; `app/backend/trace.py:820-822`; `app/backend/export_routes.py:63`), so this is not a safety defect. The defect is the guidance: she is told compare-and-accept puts it in the letter, and it does not on this backend. Fix: say before she accepts that the export stays blocked until the second check runs, in the edit row and in the EDIT_NOT_CONFIRMED text. Or, if Chris decides a re-picked quote is human-authored (see questions), let it through and say so in the notes. Acceptance test: on a quote-picker edit with the judge unavailable, the compare prompt and the warning both state that the export stays blocked, and nothing says compare-and-accept puts the entry in the letter.

**F-3 (minor). The EDIT_NOT_CONFIRMED warning sits behind "Show", under the headline "Ready to export".** The case-checks headline reads "Ready to export, 22 not reviewed" with "Show" collapsed (`p3-gate-warning.out.txt`, "case-checks text"). The edit warning appears only after expanding Show: "Edit to check (1): 1 edit is still marked Needs review ... not in the letter" (`p3b-gate-expand.out.txt`). The header does say "including 1 edit to check" (`p3-case-screen-before-export.png`). Fix: the verdict should not read "Ready to export" while an edit is held out; repeat the EDIT_NOT_CONFIRMED sentence in the export view above the letter. Acceptance test: with one edit to check, the case-checks verdict does not start with "Ready to export", and the export view shows the EDIT_NOT_CONFIRMED sentence before Copy is pressed.

**F-4 (minor). A quote-only edit prints "Original: undefined".** The row reads "Edited by you; the code checked your wording against the quote when you saved. Original: undefined" (`p4d-after-mouse-compare.png`; `app/frontend/timeline.js:52` prints `e.edited.original_summary`, which is unset for a quote edit). The original quote is still in Audit ("Excerpt: 41M restrained driver ... Transported to Central ER.", `p4e-export-after-compare-debug.out.txt`), so nothing is lost. The row still misstates what she changed. Fix: for a quote-only edit say "Quote changed by you" and show the original excerpt; never print "undefined". Acceptance test: a quote-only edit row contains no "undefined" and shows the original excerpt text.

**F-5 (minor). The copy warning still does not name the record.** The warning says "1 edited entry still marked Needs review (compare with the quote)" (`p2-f1-single-a.out.txt`, "[no-compare] copy-confirm text"; `app/frontend/export.js:39`). Two parts of pass-5 F1/F3 are fixed: "may be one the attorney needs to see" now reads correctly, and the export bar now says "22 items pending (10 flags)" against the header's "1 of 23 decided", so the two agree. Fix: name the record ("Record 3, Dr. Alvarez, primary care"). Acceptance test: the copy warning contains "Record 3" when record 3 is the open edit.

**F-6 (minor). The internal notes never name the dismissed amount.** "missing 3 days of work" is Dismissed on the row, but the notes have no line for it. `p5-notes.txt` shows "DAMAGES MENTIONS (not charges)" then "- none"; `p5-dismissed-groups.out.txt` says "notes mention 'missing 3 days': False". This is pass-5 F8, still open. Fix: a DISMISSED heading for amounts with the reason. Acceptance test: the notes contain "missing 3 days of work" under a dismissed heading.

**F-7 (minor). Pass-5 minors outside this card are still visible at 671f054.** Not re-rated here: "Accept all verified entries (9)" (`p1-body.txt:46`, F7); the accuracy figure "Verified items matched the record 84/85 times" (`p1-body.txt:215`, F11); "The phrase list found this flag but the AI did not" (`p1-body.txt:318`, F12); "Causation language (5)" holding the accident-date flag (`p1-body.txt:312-313`, F15, nit). Fix: as in pass 5. Acceptance test: as in pass 5.

## What I ran

1. `git rev-parse HEAD` gave 671f0543d489e66e62584ae11a61ee135f0f7889. `git archive 671f054 | tar -x` into the scratchpad. Server started with `artifacts/review-evidence/T-060-paralegal-pass4-serve.py` under `.venv/bin/python -I`; `curl` returned 200.
2. P1 load: sample pasted and analysed in 1.4 s; "9 entries | 3 items need review | 9 quote match" (`p1-load.out.txt`, `p1-body.txt`).
3. P2 single `a` on the edited record 3 (after accepting record 1 by mouse); two `a` presses; export and copy (warning); Enter on compare; export and copy (`p2-f1-single-a.py`).
4. P2b/P2c: export refusal on an untouched case ("Nothing is accepted or edited yet") and the export debug.
5. P3/P3b: gate warnings before export, with and without "Show" (`p3-gate-warning.py`, `p3b-gate-expand.py`).
6. P4/P4b/P4c: quote picker on record 3. Narrow pick refused 422 SUMMARY_NUMBER_NOT_IN_EXCERPT (visible). Wider pick refused 422 SUMMARY_DROPS_QUALIFIER. Recorded as a refusal, not a finding (`p4-run.stdout.txt`, `p4b-quote-save-debug.out.txt`, `p4c-run.stdout.txt`).
7. P4d: quote-picker edit on record 1 saved 200; open row; one `a` (prompt only); export before compare (letter omits record 1); mouse compare; `p4d-run.stdout.txt`.
8. P4e/P4f: export after compare (blocked), audit read, "Run the second check again" clicked, export again (still blocked).
9. P2g: summary edit on record 3, mouse compare, export: letter and notes captured.
10. P5: Dismiss flag f_r7_1 and amount a3; groups; open list; `a` on the dismissed flag; export letter and notes.
11. P6: fresh browser context, case list, reopened the case with the edit; state read.
12. Screenshots read: `p2-after-one-a.png`, `p3-case-screen-before-export.png`, `p4d-after-mouse-compare.png`.

Timings: analyse 1.4 s. Probe scripts used 0.5 to 2 s waits; this is not reading time.

```json
{"card": "T-136", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive 671f054 (HEAD 671f0543d489e66e62584ae11a61ee135f0f7889 at review start) served on http://127.0.0.1:7901 (PID 69029, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case evals/golden/sample.txt pasted (9 records); live dev app 7860 not touched",
 "exercised": [
  "git archive 671f054 into scratchpad; server on 7901 under .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py; curl 200; stopped by PID 69029 (lsof exit 1, curl 000)",
  "sample case pasted and analysed (p1-load.py, p1-body.txt)",
  "single a and second a on the edited record 3, Enter on the compare control, same-page reload (p2-f1-single-a.py -> p2-f1-single-a.out.txt)",
  "export refusal on an untouched case (p2c-export-refusal.py); export debug (p2b-export-debug.py)",
  "gate warnings before export, with and without the case-checks Show (p3-gate-warning.py, p3b-gate-expand.py)",
  "quote picker on record 3: narrow pick refused 422 SUMMARY_NUMBER_NOT_IN_EXCERPT, wider pick refused 422 SUMMARY_DROPS_QUALIFIER (p4-quote-picker.py, p4b-quote-save-debug.py, p4c-quote-refusal-and-wider-pick.py)",
  "quote-picker edit on record 1: saved 200, open row, one a, export before compare, mouse compare (p4d-quote-edit-open.py)",
  "export after compare blocked; Audit read; Run the second check again clicked; export again (p4e-export-after-compare-debug.py, p4f-rerun-after-quote-compare.py)",
  "summary edit on record 3, mouse compare, export letter and notes (p2g-summary-edit-letter-after-compare.py)",
  "dismissed flag f_r7_1 and amount a3; dismissed groups; open list; a on the dismissed flag; export letter and notes (p5-dismissed-groups.py)",
  "fresh browser context, case list, reopened the case with the edit (p6-fresh-reopen.py, p6b-list-debug.py)",
  "screenshots read: p2-after-one-a.png, p3-case-screen-before-export.png, p4d-after-mouse-compare.png"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "edit_guard": 4, "dismissed_grouping": 4, "edit_state_agreement": 2, "export_honesty": 4, "keyboard_compare": 4},
 "findings": [
  {"severity": "major", "title": "After she compares an edit, the row still reads Needs review beside Accepted (pass-5 F1 fix item 2, not taken)",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p2-f1-single-a.out.txt: '[after-enter-on-compare] e3 row: ... | Needs review | Accepted'; artifacts/review-evidence/T-136-paralegal/p4d-after-mouse-compare.png (record 1 row shows both chips after the mouse compare)",
   "why_it_matters": "The row contradicts the decision she just made. Pass-5 F1 was major and its fix list included this; the card's handoff lists it as not done.",
   "fix": "After the comparison, clear the Needs review chip and set the reason to 'Compared by you; second AI check not available'.",
   "acceptance_test": "After clicking the compare control on record 3, the row has no Needs review chip, and the header and export bar agree on the open count."},
  {"severity": "major", "title": "Compare-and-accept on a quote-picker edit leads to an export block that the offered action does not clear",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p4d-run.stdout.txt ('progress: 2 of 23 decided' after compare); p4e-export-after-compare-debug.out.txt (role=alert: 'The export is blocked. 1 accepted item has not had the second AI check ... Run the second check again.'); p4f-rerun-after-quote-compare.out.txt (same block after the RERUN_JUDGE click); p4d-after-mouse-compare.png (red banner: accepting does not replace it); pre-compare warning app/backend/trace.py:43 ('stays out of the letter until you compare it with the quote and accept it'); gate app/backend/trace.py:820-822 and app/backend/export_routes.py:63; D-044 at memory/ORCHESTRATOR_DECISIONS.md:52",
   "why_it_matters": "She does what the warning says and the letter still refuses; the only offered action fails on this backend. The block follows D-044 and is not a safety defect, so this is a guidance defect on the path the card was built for.",
   "fix": "Before she accepts, say that the export stays blocked until the second check runs, in the edit row and in the EDIT_NOT_CONFIRMED text. If Chris decides a re-picked quote is human-authored (question 1), let it through and say so in the notes.",
   "acceptance_test": "On a quote-picker edit with the judge unavailable, the compare prompt and the warning both say the export stays blocked, and no text says compare-and-accept puts the entry in the letter."},
  {"severity": "minor", "title": "EDIT_NOT_CONFIRMED sits behind Show under the headline Ready to export, 22 not reviewed",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p3-gate-warning.out.txt ('case-checks text: ... | Ready to export, 22 not reviewed | Show'); p3b-gate-expand.out.txt (after Show: 'Edit to check (1): 1 edit is still marked Needs review ... not in the letter'); app/backend/trace.py:1062 (verdict 'Ready to export' when no blockers)",
   "why_it_matters": "Before export she sees a Ready headline; the edit that is held out is named only after she expands the block. The header does say 'including 1 edit to check'.",
   "fix": "Do not show Ready to export while an edit is held out; repeat the EDIT_NOT_CONFIRMED sentence in the export view above the letter.",
   "acceptance_test": "With one edit to check, the case-checks verdict does not start with 'Ready to export', and the export view shows the EDIT_NOT_CONFIRMED sentence before Copy letter is pressed."},
  {"severity": "minor", "title": "A quote-only edit prints 'Original: undefined' on the row",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p4d-after-mouse-compare.png (row text 'Original: undefined'); app/frontend/timeline.js:52 (prints e.edited.original_summary); p4e-export-after-compare-debug.out.txt (Audit keeps 'Excerpt: 41M restrained driver ... Transported to Central ER.')",
   "why_it_matters": "The row misstates what she changed. The original quote is still in Audit, so nothing is lost.",
   "fix": "For a quote-only edit say 'Quote changed by you' and show the original excerpt on the row; never print 'undefined'.",
   "acceptance_test": "A quote-only edit row contains no 'undefined' and shows the original excerpt text."},
  {"severity": "minor", "title": "The copy warning still does not name the record (pass-5 F1 fix 4, F3 naming)",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p2-f1-single-a.out.txt ('[no-compare] copy-confirm text: ... 1 edited entry still marked Needs review (compare with the quote)'); app/frontend/export.js:39. Fixed in the same run: 'may be one the attorney needs to see'; export bar '22 items pending (10 flags)' agrees with header '1 of 23 decided'.",
   "why_it_matters": "She cannot go back and find the edit from the warning without searching the list.",
   "fix": "Name the record in the warning, for example 'Record 3, Dr. Alvarez, primary care'.",
   "acceptance_test": "The copy warning contains 'Record 3' when record 3 is the open edit."},
  {"severity": "minor", "title": "The internal notes never name the dismissed amount (pass-5 F8, still open)",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p5-notes.txt ('DAMAGES MENTIONS (not charges)' then '- none'); p5-dismissed-groups.out.txt ('notes mention missing 3 days of work: False'); the amount is Dismissed on the row (p5-dismissed-groups.out.txt, 'amount a3 state after Dismiss')",
   "why_it_matters": "The notes are her audit trail; a dismissed amount is missing from it.",
   "fix": "Add a DISMISSED heading for amounts with the reason.",
   "acceptance_test": "The notes contain 'missing 3 days of work' under a dismissed heading with its reason."},
  {"severity": "minor", "title": "Pass-5 minors outside this card are still visible at 671f054 (not re-rated)",
   "evidence": "artifacts/review-evidence/T-136-paralegal/p1-body.txt:46 ('Accept all verified entries (9)', F7); p1-body.txt:215 ('Verified items matched the record 84/85 times', F11); p1-body.txt:318 ('The phrase list found this flag but the AI did not', F12); p1-body.txt:312-313 ('Causation language (5)' then 'Accident date source', F15)",
   "why_it_matters": "Each is a claim or label she cannot act on in her own case file; pass 5 rated them and they are still open.",
   "fix": "As in the pass-5 review (reviews/T-060-paralegal-pass5.md).",
   "acceptance_test": "As in the pass-5 review: the batch label has no 'verified', the case screen has no accuracy figure, no flag card contains 'phrase list', and the accident-date flag is not in the causation group."}
 ],
 "whats_right": [
  "One a and a second a on the edited row record nothing and show the Not recorded yet prompt with focus on the compare control (artifacts/review-evidence/T-136-paralegal/p2-f1-single-a.out.txt)",
  "Dismissed flags and amounts collapse under Dismissed (1) groups, leave the open list, ignore a, and stay out of the letter (artifacts/review-evidence/T-136-paralegal/p5-dismissed-groups.out.txt)",
  "The held-out edit is named in the pre-compare notes and letter, and same-page reload and a fresh browser context both keep the edit open (artifacts/review-evidence/T-136-paralegal/p3-notes-before-compare.txt; p6-fresh-reopen.out.txt)"
 ],
 "questions_for_chris": [
  "For an entry whose AI summary never got a second check, should a re-picked quote be treated as human-authored (as D-045(b) treats her own summary wording) so it can go into the letter after compare, or stay blocked under D-044? Today a reworded summary goes in after compare (p2g-letter-after-summary-compare.txt, notes say second check not available), while a re-picked quote is blocked (p4e-export-after-compare-debug.out.txt). I am not deciding this.",
  "Is the split between those two paths intended, or should the compare control say which of the two applies before she clicks?"
 ]}
```
