# T-060 pass 4 — paralegal-reviewer (Maria Delgado persona)

Verdict: **changes** (0 blockers, 2 majors, 12 minors, 1 nit). Commit under review: e293daa. The UI is byte-identical at HEAD (`git diff --stat e293daa HEAD -- app/frontend` is empty), and I ran the same probes on HEAD f7829c1: the letter and the internal notes for the sample case were identical (`p5-export-letter-e293daa.txt` vs `p5-export-letter-head.txt`, `diff` empty).

The facts hold: every quote I checked is verbatim, both conflicts stay open with both excerpts, the $185 rate never reaches the total, and the 73-day gap is flagged. The problems are state. A dismissed flag can be re-accepted with one key and still says "Needs review". An edited entry that the app says still needs review is counted as decided, and the export says "Nothing left to decide".

## What I ran
- `git archive e293daa` into the scratchpad (`p4-e293daa`), app on 127.0.0.1:7897, PID 27007, `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own SQLite in the scratchpad. Also `git archive HEAD` (f7829c1) on 127.0.0.1:7898, PID 61750. Launcher: `artifacts/review-evidence/T-060-paralegal-pass4-serve.py` under `.venv/bin/python -I`.
- Playwright, Chromium, 1440x900. Scripts and outputs are in `artifacts/review-evidence/T-060-paralegal-pass4/`.
- Full case, keyboard-first: paste `evals/golden/sample.txt` (Appendix A, 9 records), Analyze, Start review, then a/d/e/j/k. I accepted 9 entries (one edited), 2 charges, kept the $185 rate in notes, accepted 10 flags, dismissed 2 items (the accident-date duplicate flag and "missing 3 days of work"). Script time about 16 s, with a 450 ms wait per key, so not reading time.
- Edit path: `e` on record 3, a `$9,000` figure and a "No ..." negation (both refused, nothing saved), then the correct wording (saved, Needs review). Reload mid-review: decisions and the edit persisted.
- Dismissed entry: `d` on record 8 (`p7-dismiss-entry-dismissed-group.py`).
- Export, copy letter (clipboard equals the on-screen letter, 2718 chars, no HTML or markdown), Download .txt.
- Verbatim check of letter and notes against `evals/golden/sample.txt` (`p14-verbatim-check.py`).
- Batch button, `o` then `a`, export box size, case-checks bar (`p9`). Library lib09 first Tab, prior-condition flags, unclear tray (`p10`). Export one-line style on the API (`p11`).

## Pass-2 items, re-checked
| Pass-2 item | Status at e293daa | Evidence |
|---|---|---|
| F5 unclear/charge rows, tray under 700 px | Fixed: lib09 tray 680 px, rows 77-95 px | `p10-lib09-pass2-recheck-head.out` |
| F6 accepted rows look settled | Mostly fixed: no primary Accept on accepted rows, about 116 px | `p4-edit-e3-saved.png` |
| F7 "Verified" chip | Chip fixed ("Quote matches"); batch button still says "verified" and accepts with no question (m5) | `p9-sample-pass2-recheck.out.txt` |
| F8 letter box, download | Fixed: box 1298 px vs scrollHeight 1296; "Download .txt" present | `p9-sample-pass2-recheck.out.txt` |
| F9 one-line letter, no "AI translation:" | Open: default letter is two lines per entry; one-line exists only as the API parameter `?style=oneline` (m2) | `p11-export-style-probe.out.txt` |
| F11 `o` then `a` | Open: the `a` is swallowed with no message (m4) | `p9-sample-pass2-recheck.out.txt` |
| F12 currency and dates | Partly: cents everywhere; row dates still ISO (m6) | `p2-first-screen.png` |
| F13 "Hx obtained via ..." prior-condition flag | Fixed on lib09: no prior-condition flag raised | `p10-lib09-pass2-recheck-head.out` |
| F14 bar says "1 need you" at the end | Fixed: "10/10 checks passed · Ready to export" | `p9-sample-pass2-recheck.out.txt` |
| N1 first Tab after library load | Fixed: first Tab reaches "Skip to dates to confirm" at y 0 | `p10-lib09-pass2-recheck-head.out` |

## Majors

**M1 (major). A dismissed flag or charge still reads "Needs review", keeps an enabled Accept, and one `a` turns it into "Accepted".**
Flags and amounts that I dismissed stay where they were. Their chips read "Needs review" and "Dismissed" together, the quote is struck through, and Accept, Edit note and Keep in notes stay enabled. Pressing `a` on the dismissed flag changed it to "Accepted" with no message. Only timeline entries get the "Dismissed (n)" group (`p7` output: `Dismissed (1)` lists `e8` only). Accepted flags go to FLAGS ACCEPTED in the notes, so a dismissal can silently become an accepted item in her audit trail.
Evidence: `artifacts/review-evidence/T-060-paralegal-pass4/p13-dismissed-flag-row-e293daa.png` (also `p13-dismissed-flag-row-head.png`); output `p13-dismissed-flag-row-head.out`: "after a on dismissed flag: progress 1 of 23 decided · 2 need review | row: Accident date source | Needs review | Accepted". Body text `p5-after-walk-body-e293daa.txt` lines 345-357 (flag) and 506-516 (amount "missing 3 days of work": "Needs review / Dismissed / ... Keep in notes / Dismissed / Undo").
Why it matters: checklist 14 and 16-18. She cannot tell from the card whether a dismissed item is decided, and one key press reverses a dismissal without a question.
Fix: give dismissed flags and amounts the same collapsed "Dismissed (n)" group as entries. Remove Accept, Edit note and Keep in notes from dismissed rows, leaving Undo. Drop the "Needs review" chip and reason on dismissed rows. `a` on a dismissed row does nothing, or says "Undo first".
Acceptance test: dismiss one flag and one amount. Each row has no button named Accept, Keep in notes or Edit note, shows only "Dismissed" and Undo, and is listed under "Dismissed (n)". Pressing `a` on it leaves progress and chips unchanged.

**M2 (major). An edited entry the app marks "Needs review" has no Accept control, is counted as decided, and the export says "Nothing left to decide".**
After my edit of record 3 the row shows "Needs review" and "Check: judge unavailable", with the note "The second check was not available; the item stays marked for review. Compare it with the quote yourself." Its buttons are Edited, Edit, Dismiss and Undo. There is no Accept. The header still counts it as decided ("23 of 23 decided"). The stepper says "Nothing left to decide. Export is next." The letter carries the edited wording, and the notes say "every item in the treatment section was accepted by the paralegal".
Evidence: `artifacts/review-evidence/T-060-paralegal-pass4/p4-edit-e3-saved.png`; `p9-sample-pass2-recheck.out.txt`: "status lines end: ['23 of 23 decided', ..., 'Nothing left to decide. Export is next.']"; `p5-export-notes-e293daa.txt`: "every item in the treatment section was accepted by the paralegal" and EDITED ITEMS; `p12-edit-refusals-and-reload-head.out`: after reload the row is still "Needs review | Edited".
Spec: `memory/contracts/api.md:341` (D-045b) says the judge never blocks a human-written edit and the item "stays marked for review". The export inclusion is therefore by design. My finding is the cue: the counter, the stepper and the notes contradict the row, and she has no control that records her own comparison.
Why it matters: checklist 17 (know what remains before export) and 18 (the letter holds accepted items). She would export believing nothing is left, while the row says it still needs her.
Fix: count a needs-review edit as remaining ("1 edit to check"). Add "I compared it with the quote" on edited rows, which clears the needs-review state and keeps the JUDGE_UNAVAILABLE reason in the notes. The notes should say "edited; second check not available" instead of "accepted".
Acceptance test: edit an entry while the judge has no fixture. The header shows 1 remaining, the stepper does not say "Nothing left to decide", the row has a control that clears Needs review, and the notes EDITED ITEMS line says the second check was not available.

## Minors (should fix)
- **m1. Keyboard walk does not cover the list from Start review.** `p3b-walk-order.out.txt`: Start review focuses `f_r7_1`, and 40 presses of `j` visit only `f_r6_1, f_r7_2, f_r8_2, f_r9_1, a1, a4, a2, a3` and then stop. `p3c-walk-k-and-wrap.out.txt`: `k` from the same point reaches `e1` only after 14 presses. The sheet says "j / k: Next / previous item". Fix: make `j` and `k` follow the same order as `a`, or wrap. Test: from Start review, 40 presses of `j` visit all 23 items.
- **m2. One-line letter (D-002) has no control.** The default letter is 46 lines for the sample, with a summary line and a Source line per entry. `GET .../export?style=oneline` gives 20 lines in the form `January 9, 2026 — Austin EMS run report: "..." [Ex. __ / Bates __]` (`p11-export-style-probe.out.txt`), and the export panel has no control for it. This is the F9 carry. Test: the export panel offers "One line per entry"; choosing it gives one line per entry and charge.
- **m3. Dismissing an entry leaves its accepted charge in the letter and total, with no warning.** After I dismissed record 8, the letter still has "Austin Imaging, cervical MRI, May 29, 2026: $2,150.00" and the total is still "$8,390.00", while the status says "8 of 9 records in letter" (`p7-export-letter-e8-dismissed.txt` line 39). A bill with no treatment entry is a gap the adjuster will ask about (persona section 9). Question 1 below. Test: the export status names any accepted charge whose record has no entry in the letter.
- **m4. `o` then `a` is swallowed (F11 carry).** `o` opens the record dialog and focuses its close button. `a` does nothing and nothing says why (`p9-sample-pass2-recheck.out.txt`: "F11 after o then a: progress 9 of 23 decided · dialog open? True"). Test: `a` in the dialog shows "Close the record first (Esc)".
- **m5. Batch button accepts nine entries in one click with no question (F7 carry).** `p9-sample-pass2-recheck.out.txt`: "F7 batch click: browser dialogs: [] | progress: 9 of 23 decided". Shift+A asks first. The button and the Open decisions chip still say "verified" ("9 verified entries not yet accepted"). Test: the click asks with the count, and the label avoids "verified".
- **m6. Row dates are ISO; the letter and flags use long dates (F12 carry).** `p2-first-screen.png` shows "2026-01-09" in rows; the letter has "January 9, 2026".
- **m7. A kept or dismissed amount leaves no trace in the notes.** "missing 3 days of work" was dismissed and appears nowhere in the notes ("DAMAGES MENTIONS (not charges) — none", `p5-export-notes-e293daa.txt`), while dismissed flags are listed under FLAGS DISMISSED. Test: dismissed amounts appear under a DISMISSED heading with their reason.
- **m8. Refusal text lingers while she types the next wording; no live check line while typing.** `p12-edit-refusals-and-reload-head.out`: "[negation] live/status while typing: ['The summary has a number, date or dollar figure that is not in the quote: $9,000. ...']". The refusal copy itself is right: "The summary says “no”, which the quote does not say. Remove it or change the quote." The pass-4 AC asked for a re-check hint on edit. Test: changing the text clears the old refusal, and a "Checking numbers and dates..." line shows while typing.
- **m9. A rate kept in notes reads "Accepted".** `p5-after-walk-body-e293daa.txt` lines 476-493: chip "Accepted" beside "Not counted: a rate ... needs review" and "Kept in the internal notes only; not in the letter or the total." "Accepted" reads as counted. Test: after Keep in notes, the chip reads "Kept in notes" and the reason no longer says "needs review".
- **m10. The case screen shows an accuracy claim she cannot check.** `p1-sample-body.txt`: "Verified items matched the record 84/85 times in testing on the fixture backend ... These numbers come from an older version of the AI prompts." On her case file this reads as evidence about her records. Test: no accuracy figure on the case screen; if kept, it sits under Shortcuts or About and does not say "verified".
- **m11. Flag wording uses internal terms.** "The phrase list found this flag but the AI did not; check that it applies." (`p13-dismissed-flag-row.png`; lib09 output in `p10-lib09-pass2-recheck-head.out`). Maria does not know what a phrase list is. Test: flag cards say what found the item in plain words.
- **m12. The lib09 gap notice drops the card's own caveat.** The notice says "now 40 days (was 42)". The same card says "This gap starts at record 4 ... which looks like paperwork, not a visit ... If record 4 ... is paperwork, not a visit, the gap would be 42 days" (`p8c-t114-confirm-gotit-reload-e293daa.out.txt`; screenshot `p8c-01-after-confirm.png`). Question 4. Test: the notice names the assumption ("counting record 4 as the start").

## Nit
- **n1. "Causation language (5)" contains "Accident date source" and "New-onset wording".** The notes file the dismissed accident-date flag under "Causation language" (`p7-export-notes-e8-dismissed.txt`). The label is a legal term and should match the flag. Test: group names match flag types.

## Enterprise or prototype?
Closer. A paralegal can move a case from the keyboard, the record pane shows the quote highlighted, the letter is clean and the copy is exact. The states still contradict each other on dismissed flags and on edited rows (M1, M2). Those two are what I would fix before the pass-5 gate.

## Right already
- Verbatim: all 11 letter Source quotes and 20 of 21 quoted phrases in the notes are substrings of `evals/golden/sample.txt` (`p14-verbatim-check.py`). The one miss is the AI draft summary the notes label "summary was".
- Conflicts stay open: accident date (January 9 vs 2026-01-19) and PT plan vs discharge are in the notes with both quotes. The tool does not pick. The $185 rate never reaches the total ("Accepted charges: $8,390.00").
- Decisions persist: reload keeps accepts and the edit with "Original:" shown, the dismissed entry leaves the letter and is listed as "RECORDS NOT IN THE TREATMENT SECTION", and Copy letter writes exactly the on-screen text (`p15-copy-and-download.out.txt`: "equals on-screen letter: True").

```json
{"card": "T-060", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive e293daa (pass-4 commit) served on http://127.0.0.1:7897 (PID 27007); git archive HEAD f7829c1 served on http://127.0.0.1:7898 (PID 61750) for comparison (identical frontend, identical letter and notes); fixture backend, curated set, ZLAYT_MODE=local; sample case evals/golden/sample.txt (Appendix A, 9 records); library lib09; 1440x900; pass 4 review, no code changes",
 "exercised": [
  "git archive e293daa and HEAD into scratchpad; app started with artifacts/review-evidence/T-060-paralegal-pass4-serve.py under .venv/bin/python -I",
  "sample case pasted and analysed; Start review; 23 items decided by keyboard (a, d, e, k, j), one Start review click; Shortcuts sheet read",
  "j-walk and k-walk from Start review (p3b, p3c outputs); a-walk order (p3d)",
  "edit of record 3: $9,000 refused, negation refused, correct wording saved; reload mid-review (p4, p12 outputs and screenshots)",
  "dismiss of timeline entry 8: Dismissed (1) group, export without it (p7 output and letter/notes files)",
  "dismissed flag row: screenshot and re-accept with a (p13 png and output)",
  "batch button click and o then a (p9 output); case-checks bar at the end; export box size; Download .txt",
  "export: letter and notes read in full; verbatim check of 11 letter quotes and 21 note quotes (p14); copy letter read from the clipboard and compared (p15 output)",
  "one-line export through the API parameter style=oneline (p11 output); no UI control found in the export panel",
  "lib09 load: first Tab order, flags list, unclear tray and row heights, Hx flag absent (p10 output, both commits)",
  "pass-2 findings re-checked against the above (table in the review)"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "keyboard_flow": 3, "handoff_clarity": 3, "export_fit": 4, "trust_cues": 3, "information_density": 3},
 "findings": [
  {"severity": "major", "title": "Dismissed flags and amounts still read Needs review, keep an enabled Accept, and one a turns them into Accepted",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p13-dismissed-flag-row-e293daa.png; p13-dismissed-flag-row-head.out: 'after a on dismissed flag: progress 1 of 23 decided · 2 need review | row: Accident date source | Needs review | Accepted'; p5-after-walk-body-e293daa.txt lines 345-357 and 506-516; p7-dismiss-entry-dismissed-group.out.txt: 'Dismissed (1) ... rows: [e8]' (entries only)",
   "why_it_matters": "Checklist 14, 16-18: a dismissed item still looks undecided and one key reverses the decision; accepted flags land in FLAGS ACCEPTED in her audit notes. Only entries get the Dismissed group.",
   "fix": "Give dismissed flags and amounts the same collapsed Dismissed (n) group as entries; on dismissed rows keep Undo only; drop the Needs review chip and reason; a on a dismissed row does nothing or says Undo first.",
   "acceptance_test": "Dismiss one flag and one amount: no button named Accept, Keep in notes or Edit note in those rows, only Dismissed and Undo shown, both listed under Dismissed (n); pressing a on them leaves progress and chips unchanged."},
  {"severity": "major", "title": "Edited entry marked Needs review has no Accept control, is counted as decided, and the export says Nothing left to decide",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p4-edit-e3-saved.png (chips Needs review and Edited; note 'The second check was not available; the item stays marked for review. Compare it with the quote yourself.'; buttons Edited, Edit, Dismiss, Undo); p9-sample-pass2-recheck.out.txt: 'Nothing left to decide. Export is next.' with 23 of 23 decided; p5-export-notes-e293daa.txt: 'every item in the treatment section was accepted by the paralegal'; spec memory/contracts/api.md:341 (D-045b)",
   "why_it_matters": "Checklist 17 and 18: she cannot see that one wording is still unconfirmed, and she has no control to record her own comparison. The export inclusion itself follows D-045b; the cue and the counter are what fail her.",
   "fix": "Count a needs-review edit as remaining ('1 edit to check'); add 'I compared it with the quote' on edited rows that clears Needs review and keeps JUDGE_UNAVAILABLE in the notes; notes say 'edited; second check not available' instead of 'accepted'.",
   "acceptance_test": "Edit an entry with no judge fixture: header shows 1 remaining, stepper does not say Nothing left to decide, the row has a control that clears Needs review, and the notes EDITED ITEMS line names the unavailable second check."},
  {"severity": "minor", "title": "j and k from Start review do not cover the list; k needs 14 presses to reach record 1",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p3b-walk-order.out.txt (40 presses of j visit f_r6_1, f_r7_2, f_r8_2, f_r9_1, a1, a4, a2, a3, then stop); p3c-walk-k-and-wrap.out.txt (k reaches e1 after 14 presses)",
   "why_it_matters": "A keyboard reader who presses j from Start review never sees the nine entries; the shortcut sheet says j moves to the next item.",
   "fix": "Make j and k follow the order a uses, or wrap.",
   "acceptance_test": "From Start review, 40 presses of j visit all 23 items."},
  {"severity": "minor", "title": "One-line letter (D-002) exists only as an API parameter; no export control",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p11-export-style-probe.out.txt: default 46 lines, style=oneline 20 lines, form 'January 9, 2026 — Austin EMS run report: \"...\" [Ex. __ / Bates __]'; export panel has no such control (p9 output)",
   "why_it_matters": "Pass-2 F9 carry: the paste is still two lines per entry, and the AI translation prefix work is not visible to her.",
   "fix": "Add a One line per entry option to the export panel.",
   "acceptance_test": "Export panel offers the option; choosing it gives one line per entry and charge."},
  {"severity": "minor", "title": "Dismissing an entry leaves its accepted charge in the letter and total with no warning",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p7-export-letter-e8-dismissed.txt line 39 'Austin Imaging, cervical MRI, May 29, 2026: $2,150.00' and line 42 total '$8,390.00'; status '8 of 9 records in letter'",
   "why_it_matters": "A bill with no matching treatment entry is a gap the adjuster will ask about (persona section 9).",
   "fix": "Name any accepted charge whose record has no entry in the letter in the export status and in the notes.",
   "acceptance_test": "After dismissing record 8, the export status names the Austin Imaging charge."},
  {"severity": "minor", "title": "o then a is swallowed silently (F11 carry)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p9-sample-pass2-recheck.out.txt: 'F11 after o then a: progress 9 of 23 decided · 3 need review | dialog open? True'",
   "why_it_matters": "A keyboard reader loses a keystroke and is not told why.",
   "fix": "Say Close the record first (Esc), or move focus to the source pane.",
   "acceptance_test": "Pressing a in the record dialog shows the message or accepts."},
  {"severity": "minor", "title": "Batch button accepts nine entries in one click with no question (F7 carry); label still says verified",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p9-sample-pass2-recheck.out.txt: 'F7 batch click: browser dialogs: [] | progress: 9 of 23 decided'; Open decisions chip '9 verified entries not yet accepted' (p1-sample-body.txt)",
   "why_it_matters": "Shift+A asks; the button does not. One click accepts nine unopened quotes.",
   "fix": "Same count question as Shift+A; label without the word verified.",
   "acceptance_test": "Clicking the batch button asks with the count first."},
  {"severity": "minor", "title": "Row dates are ISO while the letter and flags use long dates (F12 carry)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p2-first-screen.png (row '2026-01-09'); p5-export-letter-e293daa.txt ('January 9, 2026')",
   "why_it_matters": "Two date styles to reconcile against the demand.",
   "fix": "US long date in rows; keep the verbatim record date in the record pane.",
   "acceptance_test": "No ISO date in the timeline rows."},
  {"severity": "minor", "title": "Dismissed amount leaves no trace in the internal notes",
   "evidence": "p5-export-notes-e293daa.txt: 'DAMAGES MENTIONS (not charges) - none' after 'missing 3 days of work' was dismissed (p5-after-walk-body-e293daa.txt line ~506)",
   "why_it_matters": "The notes are her audit trail; dismissed flags are listed, dismissed amounts are not.",
   "fix": "Add a DISMISSED heading for amounts with the reason.",
   "acceptance_test": "The notes list missing 3 days of work under a dismissed heading."},
  {"severity": "minor", "title": "Refusal copy lingers while typing; no live re-check line while typing",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p12-edit-refusals-and-reload-head.out: '[negation] live/status while typing: [The summary has a number, date or dollar figure that is not in the quote: $9,000 ...]'",
   "why_it_matters": "She may read an old refusal as a current one. The pass-4 AC asked for a re-check hint on edit.",
   "fix": "Clear the refusal when the text changes; show Checking numbers and dates while typing.",
   "acceptance_test": "Changing the text removes the old refusal; the live line shows while typing."},
  {"severity": "minor", "title": "Rate kept in notes shows an Accepted chip and still says needs review",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p5-after-walk-body-e293daa.txt lines 476-493",
   "why_it_matters": "Accepted reads as counted; the figure is not in the total.",
   "fix": "Chip reads Kept in notes; drop needs review from the reason once kept.",
   "acceptance_test": "After Keep in notes the row has no Accepted chip and no needs review text."},
  {"severity": "minor", "title": "Case screen shows an accuracy figure she cannot check",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p1-sample-body.txt: 'Verified items matched the record 84/85 times in testing on the fixture backend ... These numbers come from an older version of the AI prompts.'",
   "why_it_matters": "On her case file this reads as evidence about her records.",
   "fix": "Move it out of the case screen or drop it; do not say verified.",
   "acceptance_test": "No accuracy figure on the case screen."},
  {"severity": "minor", "title": "Flag wording uses internal terms (phrase list)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p13-dismissed-flag-row.png: 'Needs review: The phrase list found this flag but the AI did not; check that it applies.'",
   "why_it_matters": "Maria cannot act on a phrase list.",
   "fix": "Say what found the item in plain words.",
   "acceptance_test": "Flag cards contain no phrase list wording."},
  {"severity": "minor", "title": "Lib09 gap notice drops the card's own caveat about record 4",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass4/p8c-t114-confirm-gotit-reload-e293daa.out.txt ('now 40 days (was 42)'); same card: 'This gap starts at record 4 ... which looks like paperwork, not a visit ... the gap would be 42 days'; p8c-01-after-confirm.png",
   "why_it_matters": "The 40 figure rests on an assumption the card itself raises.",
   "fix": "Name the assumption in the notice. See question 4.",
   "acceptance_test": "The notice text includes the record 4 assumption."},
  {"severity": "nit", "title": "Causation language group holds accident-date and new-onset flags",
   "evidence": "p1-sample-body.txt ('Causation language (5)' contains 'Accident date source' and 'New-onset wording'); p7-export-notes-e8-dismissed.txt (dismissed accident-date flag under Causation language)",
   "why_it_matters": "The legal label should match the flag.",
   "fix": "Separate group for date-source flags.",
   "acceptance_test": "Group names match flag types."}
 ],
 "whats_right": [
  "All 11 letter Source quotes and 20 of 21 quoted phrases in the notes are verbatim in evals/golden/sample.txt; the one miss is an AI draft summary labelled 'summary was' (p14-verbatim-check.py)",
  "Conflicts stay open with both excerpts; $185 rate never totaled; total reads Billed charges stated in these records: $8,390.00 (R-EX-8 format)",
  "Reload keeps accepts and the edit with Original shown; the dismissed entry leaves the letter; Copy letter equals the on-screen letter with no HTML or markdown"
 ],
 "questions_for_chris": [
  "A dismissed entry leaves its accepted $2,150 charge in the letter total. Should a charge follow its entry, or stay a separate decision (m3)?",
  "An edited row whose second check is unavailable is exported as accepted under D-045b. Should the counter treat it as still to check (M2)?",
  "Persona checklist item 21 writes the total as $8,390; R-EX-8 says $8,390.00 and the app shows $8,390.00. I graded to R-EX-8. Should the persona file change?",
  "The lib09 record 4 intake form is still the gap start in the 40-day figure (open since T-114 r1). Is an intake form a treatment endpoint (m12)?"
 ]}
```
