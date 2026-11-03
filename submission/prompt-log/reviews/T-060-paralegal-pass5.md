# T-060 pass 5: paralegal-reviewer (Maria Delgado persona)

Verdict: **changes** (0 blockers, 2 majors, 12 minors, 1 nit). Commit under review: b612176 (HEAD at review start: b6121766039c820e37a2a8df504b693103d89fc2; `git diff --stat b612176 HEAD -- app/frontend` is empty). I ran `git archive b612176` into the scratchpad (`p5-b612176`) and served it on 127.0.0.1:7899 (PID 16226), `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own SQLite in the scratchpad. Scripts and outputs: `artifacts/review-evidence/T-060-paralegal-pass5/`.

The letter is still clean: every quote is verbatim and the $185 rate stays out of the total. The state is still the problem. The edited record 3 can be recorded as compared by one `a` keypress, the row keeps "Needs review" next to "Accepted", and after that the export bar, the header and the copy warning all stop saying anything is open. The dismissed-item rows are fixed except for their grouping.

## Pass-4 majors, re-checked

| Pass-4 item | Status at b612176 | Evidence |
|---|---|---|
| M1: dismissed flag or amount keeps Accept, `a` turns it into Accepted | Mostly fixed. A dismissed flag and a dismissed amount show only Dismissed and Undo (plus Audit and links); `a` on either leaves progress and the row unchanged. Not fixed: they are not collected under "Dismissed (n)" (F2). | `artifacts/review-evidence/T-060-paralegal-pass5/p5-06-m1-probe.out.txt`; `p5-06-m1-flag-f_r7_1-after-a.png` |
| M2: edited entry marked Needs review has no control, counts as decided, export says "Nothing left to decide" | Partly fixed, partly regressed. Mouse path: the header counts the edit as open and the copy warning names it. But "I compared it with the quote" leaves the Needs review chip on the row, and a single `a` (Start review selects this row first) records a comparison without the check and removes the warning (F1). | `p5-10-m2-compare.stdout.txt`; `p5-10-after-a-on-edited.png`; `p5-11-case2-m2-mouse.out.txt`; `p5-11-case2-e3-after-compare.png` |

## Pass-4 minors, re-checked

- m1 (j/k coverage): open, F4.
- m2 (one-line letter has no control): fixed. The export panel has a "One line per entry (date, provider, quote)" radio; output is one line per entry and charge with the `[Ex. __ / Bates __]` placeholder. `p5-13-case1-dismiss-entry-oneline.out.txt`, `p5-13-letter-oneline.txt`.
- m3 (dismissed entry leaves its accepted charge in the letter and total): open, F5.
- m4 (`o` then `a` swallowed): open, F6.
- m5 (batch button, no question, "verified"): open, F7.
- m6 (ISO row dates): fixed. Rows read "January 9, 2026" (`p5-01-body.txt` line 51).
- m7 (dismissed amount not in notes): open, F8.
- m8 (refusal lingers; no live check line): open, F9.
- m9 (rate reads Accepted): open, F10.
- m10 (accuracy figure on case screen): open, F11.
- m11 (phrase list wording): open, F12.
- m12 (lib09 notice drops the record-4 assumption): open, F13.
- n1 (Causation language group): open, F15.

## What I ran

1. Pinned HEAD, archived b612176, started the app (PID 16226, port 7899). Confirmed `curl` returns 200.
2. Loaded the sample case as pasted text (`p5-01-load.py`, Analyze took 1.3 s; body dump `p5-01-body.txt`).
3. Full keyboard walk of the sample case (`p5-02-walk.py`, then `p5-04`, `p5-07`, `p5-08`): Start review, dismissed the accident-date duplicate flag with a reason, Keep in notes on the $185 rate, dismissed "missing 3 days of work", reworded record 3 with `e`, accepted the rest with `a`. The forward walk missed some items, which I picked up in `p5-08`.
4. Reopened the case from the case list in a fresh profile and read the Shortcuts sheet (`p5-03-resume-keys.py`, `p5-03b-open-walked.py`).
5. M1 probe: `a` on the dismissed flag and the dismissed amount (`p5-06-m1-probe.py`).
6. M2 keyboard path: `a` on the edited record 3 before any comparison, then Export and Copy letter (`p5-10-m2-compare.py`). The Go back / compare steps failed because no warning appeared on that path; the failure is the finding.
7. M2 mouse path on a second pasted case (23 items, `case-RBKmvN...`): Edit, Save, Export, Copy letter (warning shown), Go back, "I compared it with the quote" (`p5-11-case2-m2-mouse.py`).
8. Export of case 1 with the edit still open: export bar, notes, letter, Copy letter gating (`p5-09-export.py`).
9. Keyboard on case 2: 40 presses of j from Start review, 40 of k, `o` then `a`, the batch button (`p5-12-case2-keys-batch.py`).
10. Dismissed record 8 (accepted entry with an accepted $2,150 charge) with `d`; export status, letter, notes, one-line layout (`p5-13-case1-dismiss-entry-oneline.py`).
11. Edit refusal on case 2: `$9,000` saved, refused, corrected wording typed; same-page reload (`p5-14-case2-edit-refusal-reload.py`).
12. lib09 record 4 date confirmed, gap notice and card text read (`p5-15-lib09-gap-notice.py`, `p5-15b-lib09-caveat.py`).
13. Letter quotes checked against `evals/golden/sample.txt` (`p5-16-verbatim-copy.py`); Copy letter on case 1 with one-line layout: clipboard equals on-screen text.

Timings: Analyze 1.3 s. I did not time the whole review as a paralegal would; the walk scripts pressed keys with 250 to 700 ms waits, so their run time is not reading time.

## Findings

- **F1 (major): an edited row marked Needs review can be accepted by one `a` press, and the export then stops saying anything is open.** `Start review focus: e3`, then `a` gives `progress 23 of 23 decided`, the row reads "Needs review | Accepted", the header shows "0 items need review" and a banner "Everything is decided. Nothing is waiting on you." Copy goes straight through ("Copied the treatment section.", `p5-10-m2-compare.stdout.txt` lines 2, 4 and 7). On the mouse path the row still shows Needs review next to Accepted after "I compared it with the quote" (`p5-11-case2-m2-mouse.out.txt` line 10; `p5-11-case2-e3-after-compare.png`). The export bar says "0 items pending (0 flags)" while the header says "22 of 23 decided · 1 item needs review" (`p5-09-export-body.txt` line 538; `p5-09-after-copy-click.png`). When the copy warning does appear, it names the edit: "1 edited entry still marked Needs review (compare with the quote)" (`p5-11-case2-m2-mouse.out.txt` line 6). The export inclusion of the edited wording follows D-045b and I do not count it here; the cue is what fails.
- **F2 (major): dismissed flags and amounts are not collected under "Dismissed (n)".** Pass-4 M1's first fix item and its acceptance test require this. Entries get the group (`Dismissed (1)` in `p5-13-case1-dismiss-entry-oneline.out.txt` line 6), but no "Dismissed (" heading exists in the case body with the flag and amount dismissed (`p5-05-state-body.txt`: zero matches). The dismissed flag "Accident date source" and the dismissed amount "missing 3 days of work" stay in place (`p5-06-m1-flag-f_r7_1-after-a.png`).
- **F3 (minor): copy warning grammar and naming.** "A pending flag may be the attorney needs to see. Copy the letter anyway?" (`p5-09-after-copy-click.png`; case 2 reads "may be one the attorney needs to see", `p5-11-case2-copy-warning.png`). The warning says "1 edited entry", not which record.
- **F4 (minor, pass-4 m1): keyboard coverage.** From Start review on case 2, 40 presses of j visit 9 of 23 items and stop at a3; k from the end visits all 23 (`p5-12-case2-keys-batch.out.txt` lines 3 and 5). The shortcut sheet says j moves to the next item (`p5-03b-open-walked.out.txt`).
- **F5 (minor, pass-4 m3): a dismissed entry keeps its accepted charge.** After dismissing record 8 the letter still lists "Austin Imaging, cervical MRI, May 29, 2026: $2,150.00" and the total is $8,390.00; the export status says "8 of 9 records in letter" and nothing about the charge (`p5-13-case1-dismiss-entry-oneline.out.txt` lines 7 and 8; `p5-13-letter-e8-dismissed.txt`).
- **F6 (minor, pass-4 m4): `o` then `a` is swallowed silently.** The record dialog stays open and says nothing (`p5-12-case2-keys-batch.out.txt` lines 9-10; `p5-12-m4-o-then-a.png`).
- **F7 (minor, pass-4 m5): the batch button accepts eight entries in one click.** Label "Accept all verified entries (8)", no browser or in-app question, progress 1 of 23 to 9 of 23 (`p5-12-case2-keys-batch.out.txt` lines 11-14; `p5-01-body.txt` line 46).
- **F8 (minor, pass-4 m7): a dismissed amount leaves no trace in the internal notes.** "missing 3 days of work" is Dismissed on the row (`p5-05-a3-state.png`), while the notes say "DAMAGES MENTIONS (not charges)" then "- none" (`p5-09-export-body.txt` lines 621-622). The notes text is produced by the backend; the heading is still missing from what she copies.
- **F9 (minor, pass-4 m8): refusal lingers and no re-check line while typing.** After "$9,000" was refused on save, the corrected wording "Pain 4/10, improving." still shows "The summary has a number, date or dollar figure that is not in the quote: $9,000" 1.5 s later; no "Checking numbers and dates" line appears (`p5-14-case2-edit-refusal-reload.out.txt`).
- **F10 (minor, pass-4 m9): a rate kept in notes reads Accepted.** The row shows "Accepted" and "Kept in notes" together, with "Not counted: a rate, not a bill ... needs review" (`p5-05-a2-state.png`).
- **F11 (minor, pass-4 m10): accuracy figure on the case screen.** "Verified items matched the record 84/85 times in testing on the fixture backend" (`p5-01-body.txt` line 212).
- **F12 (minor, pass-4 m11): internal flag wording.** "The phrase list found this flag but the AI did not; check that it applies." (`p5-01-body.txt` line 315).
- **F13 (minor, pass-4 m12): gap notice drops the assumption.** "Gap recalculated after you confirmed record 4: now 40 days (was 42)." The card still says "This gap starts at record 4" (`p5-15-lib09-gap-notice.out.txt`; `p5-15b-lib09-caveat.out.txt`). The notice itself does not name the record-4 assumption.
- **F14 (minor, new): two sample cases look identical in the list.** Both are titled "Pasted records, Nov 2" with 6:18 AM and 6:19 AM (`p5-03-resume-keys.out.txt`, CASE LIST line). A paralegal with two versions of a file cannot tell them apart by name.
- **F15 (nit, pass-4 n1): the "Causation language (5)" group holds "Accident date source"** (`p5-01-body.txt` lines 309-310).

Out of my lens or owned elsewhere: the internal notes still read "every item in the treatment section was accepted by the paralegal. Items not reviewed: 0." while record 3 is still marked Needs review (`p5-09-export-body.txt` line 598). That is the backend notes text under T-134; I have not scored it, but the UI shows it verbatim.

## Right already

- Dismissed flag and dismissed amount: no Accept, Keep in notes or Edit note; `a` leaves progress unchanged (`p5-06-m1-probe.out.txt`).
- Letter quotes: all 11 two-line Source quotes and all 10 one-line quotes are verbatim substrings of `evals/golden/sample.txt`; the total line reads "Billed charges stated in these records: $8,390.00"; copy equals the on-screen one-line letter (`p5-16-verbatim-copy.out.txt`).
- Copy warning on the mouse path names the open edit and the unreviewed counts before anything is copied (`p5-11-case2-m2-mouse.out.txt` line 6).

```json
{"card": "T-060", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive b612176 (HEAD b6121766039c820e37a2a8df504b693103d89fc2 at review start) served on http://127.0.0.1:7899 (PID 16226); fixture backend, curated set, ZLAYT_MODE=local, scratchpad DB; sample case evals/golden/sample.txt pasted as two cases (9 records each, one walked to completion); library lib09 for the gap notice; 1440x900 Chromium",
 "exercised": [
  "git archive b612176 into scratchpad; app started with artifacts/review-evidence/T-060-paralegal-pass4-serve.py under .venv/bin/python -I; curl 200",
  "sample case pasted and analysed (p5-01); full keyboard walk to 22 of 23 decided with d (flag, with reason), Keep in notes (rate), d (amount), e (record 3 reword), a on the rest (p5-02, p5-04, p5-07, p5-08)",
  "reopened the walked case from the case list in a fresh profile; Shortcuts sheet text read (p5-03, p5-03b, p5-05)",
  "M1 probe: a on dismissed flag f_r7_1 and dismissed amount a3 (p5-06)",
  "M2 keyboard path: Start review then a on the edited record 3 (p5-10); copy warning and Go back attempted (warning absent on this path)",
  "M2 mouse path on a second pasted case: Edit, Save, Export, Copy letter (warning), Go back, I compared it with the quote, export, copy (p5-11)",
  "export of case 1 with the edit open: export bar, header, letter, notes, Copy letter gating, Download not used (p5-09)",
  "case 2 keyboard: 40 j presses from Start review, 40 k presses, o then a in the record dialog, batch button click (p5-12)",
  "dismissed record 8 with d; export status, letter, notes headings, one-line layout radio (p5-13)",
  "edit refusal: $9,000 saved and refused, corrected wording typed, timed re-read; same-page reload restores the case with decisions (p5-14)",
  "lib09 record 4 confirmed to March 5, 2026; gap-change note and card caveat read (p5-15, p5-15b)",
  "verbatim check of letter quotes against evals/golden/sample.txt (p5-16); copy equals on-screen one-line letter; clipboard has total line",
  "screenshots read: p5-01-analyzed.png, p5-09-after-copy-click.png, p5-10-after-a-on-edited.png, p5-11-case2-e3-after-compare.png, p5-11-case2-copy-warning.png, p5-12-m4-o-then-a.png, p5-05-a2-state.png, p5-06-m1-flag-f_r7_1-after-a.png"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "keyboard_flow": 3, "handoff_clarity": 3, "export_fit": 4, "trust_cues": 2, "information_density": 3},
 "findings": [
  {"severity": "major", "title": "Edited entry marked Needs review is recorded as compared by one a press; the row keeps Needs review beside Accepted; the export bar, header and copy warning then say nothing is open",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-10-m2-compare.stdout.txt lines 2 (Start review focus: e3), 4 (a on edited e3 before compare: progress 23 of 23 decided) and 7 (copy warning texts include 'Copied the treatment section.' and 'Nothing left to decide. Export is next.'); p5-10-after-a-on-edited.png (header '23 of 23 decided', chip '0 items need review', banner 'Everything is decided'; row chips 'Needs review' and 'Accepted'); p5-11-case2-m2-mouse.out.txt line 10 and p5-11-case2-e3-after-compare.png (Needs review still beside Accepted after I compared); p5-09-export-body.txt line 538 ('0 items pending (0 flags)') against p5-09-after-copy-click.png header '22 of 23 decided · 1 item needs review'; warning that does work: p5-11-case2-m2-mouse.out.txt line 6 names '1 edited entry still marked Needs review (compare with the quote)'",
   "why_it_matters": "Checklist 17 and 18: Maria walks the list with a and Start review selects this row first, so one habitual key records a comparison she did not make, clears the only warning that names the edit before copy, and leaves the row contradicting itself. The export inclusion follows D-045b and I do not count it; the cue is what fails, as in pass 4.",
   "fix": "(1) a on an edited row whose reason is JUDGE_UNAVAILABLE does not record the comparison; it focuses 'I compared it with the quote' and says so. (2) After the comparison the Needs review chip clears and the reason becomes 'Compared by you; second AI check not available'. (3) The export bar counts an edit still marked Needs review as open ('1 edit to check'), never '0 items pending' while the header says 1. (4) The copy warning names the record ('Record 3, Dr. Alvarez, primary care').",
   "acceptance_test": "Start review on a case with one edited entry (judge unavailable), press a: progress stays at N-1 of 23, the row keeps a 'Compare with the quote' control and no Accepted chip, Copy letter shows the warning naming Record 3; after clicking the compare control the row has no Needs review chip and the export bar and header agree."},
  {"severity": "major", "title": "Dismissed flags and amounts are not collected under Dismissed (n); only entries are (pass-4 M1 residual)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-05-state-body.txt has zero 'Dismissed (' headings with the flag f_r7_1 and the amount a3 dismissed; p5-13-case1-dismiss-entry-oneline.out.txt line 6 shows the only group, 'Dismissed (1)', for record 8 (an entry); p5-06-m1-flag-f_r7_1-after-a.png shows the dismissed flag in place among open flags; p5-05-a3-state.png shows the dismissed amount in place",
   "why_it_matters": "Pass-4 M1's acceptance test requires both kinds listed under Dismissed (n). The row states are now right (Dismissed and Undo only, a is a no-op), but a dismissed flag still sits in the open list where she is scanning for what needs her.",
   "fix": "Give dismissed flags and amounts the same collapsed Dismissed (n) group as entries, with the reason, and remove them from the open list.",
   "acceptance_test": "Dismiss one flag and one amount: both appear under a 'Dismissed (n)' group and not in the open list; a on either leaves progress unchanged; the group count matches the export's dismissed list."},
  {"severity": "minor", "title": "Copy warning: ungrammatical sentence and it names 'one edited entry' without the record",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-09-after-copy-click.png ('A pending flag may be the attorney needs to see. Copy the letter anyway?'); p5-11-case2-m2-mouse.out.txt line 6 (the case 2 wording 'A pending flag may be one the attorney needs to see')",
   "why_it_matters": "A warning she reads before she copies should be plain. Naming the record is what lets her go back and find the edit.",
   "fix": "Fix the sentence ('A pending flag may be one the attorney needs to see') and name the record in the warning.",
   "acceptance_test": "The warning text contains no 'may be the attorney needs' and names 'Record 3' when record 3 is the edited entry."},
  {"severity": "minor", "title": "From Start review, j reaches 9 of 23 items in 40 presses; entries above are not reachable by j (pass-4 m1, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-12-case2-keys-batch.out.txt line 3 ('40x j visited 9 distinct items: f_r7_1 ... a3') and line 5 ('40x k (from the end) visited 23 distinct items'); the shortcut sheet in p5-03b-open-walked.out.txt says 'Next / previous item (dates to confirm, then entries, flags, charges)'",
   "why_it_matters": "A keyboard reader who presses j from Start review never sees the nine entries. The sheet promises the whole list.",
   "fix": "Make j and k follow the same order as a, or wrap at the ends.",
   "acceptance_test": "From Start review on a case with all 23 items pending, 40 presses of j visit all 23 items."},
  {"severity": "minor", "title": "Dismissing an entry leaves its accepted charge in the letter and the total; the export status says nothing (pass-4 m3, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-13-case1-dismiss-entry-oneline.out.txt line 7 (export status '8 of 9 records in letter', no charge named) and line 8 ('letter mentions Austin Imaging charge: True; total line: Billed charges stated in these records: $8,390.00'); letter file p5-13-letter-e8-dismissed.txt",
   "why_it_matters": "A bill with no matching treatment entry is a gap the adjuster asks about (persona section 9). Maria would not see it at the export step.",
   "fix": "Name any accepted charge whose record has no entry in the letter in the export status and in the internal notes; the Question for Chris decides whether the charge also leaves the total.",
   "acceptance_test": "After dismissing record 8 the export status names 'Austin Imaging, cervical MRI, May 29, 2026: $2,150.00' as a charge with no entry in the letter."},
  {"severity": "minor", "title": "o then a is swallowed silently in the record dialog (pass-4 m4, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-12-case2-keys-batch.out.txt lines 8-10 ('m4 dialogs open after o: 1'; 'm4 after a in dialog: progress 1 of 23 decided · 3 items need review'); p5-12-m4-o-then-a.png (dialog open, no message)",
   "why_it_matters": "A keyboard reader loses a keystroke and is not told why.",
   "fix": "In the record dialog, a shows 'Close the record first (Esc)' or the dialog takes the key.",
   "acceptance_test": "With the record dialog open, pressing a shows the message or accepts the selected item; the message text is in the DOM."},
  {"severity": "minor", "title": "Batch button accepts eight entries in one click with no question; the label still says verified (pass-4 m5, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-12-case2-keys-batch.out.txt lines 11-14 ('Accept all verified entries (8)'; browser dialogs []; in-app dialogs []; progress 1 of 23 to 9 of 23); p5-01-body.txt line 46",
   "why_it_matters": "One click records eight quote checks she has not opened. Shift+A asks first; the button does not.",
   "fix": "Same count question as Shift+A ('Accept 8 entries that match their quote?') and a label without the word verified.",
   "acceptance_test": "Clicking the batch button asks with the count before anything changes; the button label contains no 'verified'."},
  {"severity": "minor", "title": "A dismissed amount leaves no trace in the internal notes (pass-4 m7, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-09-export-body.txt lines 621-622 ('DAMAGES MENTIONS (not charges)' then '- none') while 'missing 3 days of work' is Dismissed (p5-05-a3-state.png)",
   "why_it_matters": "The notes are her audit trail; a dismissed amount is missing from it entirely.",
   "fix": "Add a DISMISSED heading for amounts with the reason (the notes text is backend output; the UI shows it verbatim).",
   "acceptance_test": "The notes list 'missing 3 days of work' under a dismissed heading with its reason."},
  {"severity": "minor", "title": "Refusal for $9,000 lingers after the corrected wording; no re-check line while typing (pass-4 m8, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-14-case2-edit-refusal-reload.out.txt: after the save refusal, 'm8 after 1.5 s with corrected text' still returns 'The summary has a number, date or dollar figure that is not in the quote: $9,000. Remove it or change the quote.'; while typing the corrected text there is no 'Checking numbers and dates' line",
   "why_it_matters": "She may read an old refusal as the current state of her wording.",
   "fix": "Clear the refusal when the text changes; show a polite 'Checking numbers and dates...' line while typing.",
   "acceptance_test": "After the refused text is replaced with supported text, the refusal text is gone within 1 s and the live line shows while typing."},
  {"severity": "minor", "title": "A rate kept in notes shows an Accepted chip beside Kept in notes (pass-4 m9, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-05-a2-state.png (chip 'Accepted' and chip 'Kept in notes' on the $185 rate row; text 'Not counted: a rate, not a bill ... needs review')",
   "why_it_matters": "Accepted reads as counted; the figure is not in the total.",
   "fix": "Show 'Kept in notes' only and drop 'needs review' from the reason once kept.",
   "acceptance_test": "After Keep in notes the row has no Accepted chip and no 'needs review' text."},
  {"severity": "minor", "title": "The case screen still shows an accuracy claim she cannot check (pass-4 m10, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-01-body.txt line 212 ('Verified items matched the record 84/85 times in testing on the fixture backend ...')",
   "why_it_matters": "On her case file this reads as evidence about her records.",
   "fix": "Move the figure out of the case screen or drop it; do not use the word verified on the case screen.",
   "acceptance_test": "The case screen contains no accuracy figure."},
  {"severity": "minor", "title": "Flag card uses an internal term: 'The phrase list found this flag' (pass-4 m11, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-01-body.txt line 315 ('Needs review: The phrase list found this flag but the AI did not; check that it applies.')",
   "why_it_matters": "Maria cannot act on a phrase list. The sentence should say what found the item.",
   "fix": "Say what found the item in plain words, e.g. 'The wording check found this; the second AI check did not. Check that it applies.'",
   "acceptance_test": "No flag card contains 'phrase list'."},
  {"severity": "minor", "title": "The lib09 gap notice drops the record-4 assumption that the card states (pass-4 m12, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-15-lib09-gap-notice.out.txt ('Gap recalculated after you confirmed record 4: now 40 days (was 42).'); artifacts/review-evidence/T-060-paralegal-pass5/p5-15b-lib09-caveat.out.txt (the card: 'This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR)')",
   "why_it_matters": "The 40-day figure rests on counting an intake form as the gap start. The notice reads as settled.",
   "fix": "Name the assumption in the notice ('counting record 4, the intake form, as the start').",
   "acceptance_test": "The notice text names record 4 as the assumed start of the gap."},
  {"severity": "minor", "title": "Two sample cases look identical in the case list (new)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-03-resume-keys.out.txt, CASE LIST line 'case-list': 'Pasted records, Nov 2, 6:19 AM ... 18 pending' and 'Pasted records, Nov 2, 6:18 AM ... 23 pending'",
   "why_it_matters": "A paralegal with two versions of one file needs to tell them apart by name before she exports.",
   "fix": "Name the case from its first record's source and date, or let the user rename it.",
   "acceptance_test": "Two cases from the same paste have different names that include the first record's source."},
  {"severity": "nit", "title": "Causation language group holds the accident-date flag (pass-4 n1, still open)",
   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-01-body.txt lines 309-310 ('Causation language (5)' then 'Accident date source')",
   "why_it_matters": "The legal label should match the flag type.",
   "fix": "Separate group for accident-date source flags.",
   "acceptance_test": "Group names match flag types."}
 ],
 "whats_right": [
  "Dismissed flag and dismissed amount: no Accept, Keep in notes or Edit note; a leaves progress and the row unchanged (artifacts/review-evidence/T-060-paralegal-pass5/p5-06-m1-probe.out.txt)",
  "Letter quotes: all 11 two-line and all 10 one-line Source quotes are verbatim in evals/golden/sample.txt; total reads 'Billed charges stated in these records: $8,390.00'; copy equals the on-screen one-line letter (artifacts/review-evidence/T-060-paralegal-pass5/p5-16-verbatim-copy.out.txt)",
  "Copy warning on the mouse path names the open edit and the unreviewed counts before anything is copied (artifacts/review-evidence/T-060-paralegal-pass5/p5-11-case2-m2-mouse.out.txt line 6)"
 ],
 "questions_for_chris": [
  "Should a on an edited row that still needs a second check record the comparison at all, or should only the named 'I compared it with the quote' control do that (F1)?",
  "A dismissed entry leaves its accepted $2,150 charge in the letter total (F5, pass-4 question 1 still open). Should the charge follow its entry, or stay a separate decision?"
 ]}
```
