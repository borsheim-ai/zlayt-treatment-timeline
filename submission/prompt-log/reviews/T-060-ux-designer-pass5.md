# T-060 pass 5: enterprise UI/UX review (ux-designer-reviewer)

**Verdict: pass.** No blocker, no major. This is my third consecutive pass with no major (passes 3, 4, 5), so the stop rule is met on my side; the paralegal pass 5 and the accessibility result are not mine. Of the pass-4 findings, F1 (developer words in the row reason), F2 (disagreeing need-review counts), F3 (keyboard jump), F5 (doubled explanations) and the long-dates deferral in F6 are fixed. What remains is F4 (first screen and gap flag), the F6 leftovers, two nits, and one new minor the F2 fix created (the Timeline chip scope).

Scores (1 to 5), pass 1 -> 2 -> 3 -> 4 -> 5: design quality 2 -> 4 -> 4 -> 4 -> 4, originality 2 -> 3 -> 3 -> 3 -> 3, craft 2 -> 3 -> 4 -> 4 -> 4, functionality 3 -> 4 -> 4 -> 4 -> 4. Craft stays at 4: the wording leaks and the count disagreement are gone, but unclear charge rows still print two reasons and the accuracy line still says 'fixture backend'. No score is 2 or below.

## Scope and how I ran it

- Pinned: card commit b612176. `git rev-parse --short HEAD` printed `b612176`; `git status --short | wc -l` printed `2011` (dirty tree), so I did not serve the repo root. I ran `git archive b612176` into the session scratchpad (`.../scratchpad/app5`), `PORT=7995 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own `ZLAYT_DB`. Listener PID 16797, stopped with `kill 16797`; `curl http://127.0.0.1:7995/api/health` then printed `000`.
- Playwright (project venv) at 1440x900 and 390x844 touch: sample first load and rows; keyboard `a`, `d`, a long `a` run, Start review then `a` and `d` in Flags; fresh lib09 and lib11 with dismiss, accept, Undo, reload and the three counts read each time; lib01, lib06, lib09, lib11 rows, tray, Filtered by rule group at both widths; AI-check panel on lib06; edit open and saved on sample entry-3; dismissed flag, amount and entry; export with Letter layout radios; unclear charge rows; Open record; `?` from the page top.
- Not exercised: e2e suite (QA's), PDF upload, real-model latency, Safari and Firefox, WCAG conformance (accessibility-reviewer), dark mode, the failed-run stub, empty and oversize input (not re-walked; unchanged since pass 2), 1024 and 768 widths, the audit drawer, the landing and case list (not re-walked; unchanged since pass 4). Competitor comparison is to their marketing text only (research/ui-references.md); I saw no UI of EvenUp, Supio, Filevine or Litify.
- Evidence and scripts: `artifacts/review-evidence/T-131-pass5/` (`ux5-*`; the T-131 review shares it).

## Pass-4 findings re-checked

| Pass-4 item | Status | Evidence |
|---|---|---|
| F1 row reason in developer words | **Fixed** | lib06 entry-5 'The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.'; edited sample row 'The second AI check did not run or did not finish, so this item has not been double-checked.'; no code-shaped word, token, judge unavailable, lexicon or fixture in any row or tray on sample, lib01, lib06, lib09, lib11 (ux5-walk4-results.json raw_in_rows; ux5-walk8-results.json edited_d) |
| F2 three need-review numbers | **Fixed**, side effect in F1 below | Header, pill and chip read the same on every case and move together on dismiss, accept, Undo and reload (lib09 13, 12, 11, 11, 11, 11; lib11 11, 10, 9, 9, 9, 9) (ux5-walk5-results.json) |
| F3 `a`/`d` jump 2,900 px to a flag | **Fixed** | Entry-1 then `a a a d d`: focus entry-2 to entry-6, scrollY 0 to 76; second `a` accepts nothing in Flags or Charges; a 12-press run ends on entry-9 with 'Nothing more to decide in this list. 14 items are still open in other lists. Press Start review to go to the next one.' (ux5-walk2-results.json). In Flags the keys stay in the focused group (ux5-walk9-results.json) |
| F5 doubled explanations | **Fixed** | lib01 tray item says 'no recorded AI answer' once; the lib06 AI-check row for the tray flag has the lead, 'Left out of the letter' and one action line, no code/AI pair (ux5-walk6-results.json jp_d; ux5-30-judge-panel-lib06-d.png) |
| F6 m3 ISO dates in rows | **Fixed** | `<time datetime="2026-01-09">January 9, 2026</time>` on every row at both widths; the row, the gap card and the letter now agree (ux5-walk1-results.json) |
| F4 first screen and gap flag | **Open, minor** | See F2 below |
| F6 m1, m2, m4 | **Open, minor** | See F3 below |
| N1 Dismissed affordance | **Partly fixed** | The secondary Accept is gone from dismissed flags, amounts and entries (buttons: Open records, Why this status, Dismissed, Undo, Audit; the Dismiss button is hidden), and `a` on a dismissed row says 'This item is dismissed. Press r or Undo to bring it back first.' The word 'Dismissed' still shows twice on a flag and an amount (chip and footer) (ux5-walk7-results.json; ux5-31-dismissed-flag-d.png) |
| N2 `?` from page top | **Open, nit** | `q_open` 0 at both widths (ux5-walk8-results.json) |

Also new and good since pass 4: an edited row that is still Needs review keeps the chips 'Needs review' and 'Edited', shows the original beside the new text ('Original: Persistent neck pain 6/10 and daily headaches; …'), counts as open (header 0 of 23, 4 items need review) and offers a primary 'I compared it with the quote' (ux5-41-edit-saved-d.png); the Letter layout radios; the Filtered by rule group on every library case (see the T-131 review).

## Screen polish, 1 to 5 (pass 1 -> 2 -> 3 -> 4 -> 5; 4 = would pass in a Carbon or Atlassian product)

| Screen | P1 | P2 | P3 | P4 | P5 | Why |
|---|---|---|---|---|---|---|
| Case list and library | 2 | 3 | 3 | 4 | 4 | Not re-walked |
| Paste / upload | 3 | 4 | 4 | 4 | 4 | Not re-walked |
| Processing and failure | 2 | 4 | 4 | 4 | 4 | Not re-walked |
| Timeline and review queue | 2 | 3 | 4 | 4 | 4 | Long dates, plain one-sentence reasons, one count, focus stays; first row still at 464 with 3 rows; chip scope (F1) |
| Case checks and AI check | 3 | 3 | 4 | 4 | 4 | Tray-flag row now has one lead and one action; 'Technical details' nested in each row, text-link toggles |
| Flags | 2 | 4 | 4 | 4 | 4 | Dismissed flag drops Accept and Needs review; still two 'Dismissed' labels; gap flag y 2,024; panel 2,930 px |
| Charges and billing | 2 | 3 | 3 | 3 | 3 | Unchanged: unclear rows 196 and 183 px (406 at 390) with two reasons each ('Not counted: a rate, not a bill. rate $185/visit; …' plus 'This figure is not a bill…') (ux5-walk10-results.json) |
| Source record | 3 | 4 | 4 | 4 | 4 | 'Open record' still opens a modal at 1440 over a pane that prints '=== Record 2 ===' (ux5-51-open-record-d.png) |
| Dates, tray, manual entry | 2 | 3 | 4 | 4 | 4 | Tray reason once; Filtered by rule group collapsed and actionless |
| Export and paragraph | 3 | 4 | 4 | 4 | 4 | Letter layout radios work by mouse and arrow key and the preview changes; summary line states what is in the letter (ux5-33-export-oneline-d.png) |
| Mobile 390 | 2 | 3 | 4 | 4 | 4 | scrollWidth 390 on sample, lib01, lib06, lib09, lib11, export; rows 246 to 407 px; a dismissed flag is 732 px tall; Filtered by rule bar cramped (N1) |
| Dark mode | 1 | 4 | 4 | 4 | 4 | Not re-walked |
| Keyboard | 2 | 3 | 4 | 4 | 4 | The auto-advance concern is fixed and the live line says what to do next; `?` from the top still opens nothing (N2); j and k coverage is in the paralegal pass, not re-tested here |

## Does it read as a polished enterprise tool?

Yes, for a prototype, and the text-level tells I named in pass 4 are gone: no row says 'token' or 'judge unavailable', dates read the same in the row, the flag card and the letter, and one number says how much is left. What still shows the build is smaller: the accuracy line says 'fixture backend', the unclear charge rows say the same thing twice, and the Timeline chip row mixes a case number with an entry number. Beside the marketing descriptions of EvenUp, Supio, Filevine and Litify (no UI seen) the review mechanics (verbatim quote beside every summary, undoable decisions, keyboard sheet, side-by-side conflict, the reviewer's own edit kept beside the original) are what their pages lead with; their text-level polish I cannot judge.

## Findings

### F1 (minor, new): the Timeline chip shows the case-wide count beside the entry count
'9 entries · 3 items need review · 9 quote match' over nine Verified rows on the sample; '7 entries · 6 items need review' on lib06 with one such row; '7 entries · 13 items need review' on lib09 with two. The number agrees with the header and pill (my pass-4 fix), but in that chip row it reads as a statement about the entries (ux5-walk1-results.json chips; ux5-walk4-results.json lib06_d, lib09_d; ux5-01-sample-d.png).
**Fix:** scope it ('3 items need review in this case', linked to Start review) or show the entries-only number there.
**Test:** sample 1440: the chip text contains 'in this case' or equals the count of queue rows with `data-state=needs_review`.

### F2 (minor, carried from pass 4 F4): first screen and gap flag
First row top 464 (target < 450), 3 rows fully visible at 1440 and 0 at 390; the 73-day gap card is at y 2,024 at 1440 (pass 4: 2,090) and 4,105 at 390 (pass 4: 4,181); the flags panel is 2,930 px at 1440 and 4,946 at 390 (ux5-walk1-results.json gap_y, rows; ux5-walk10-results.json flags_h). The 'Show gap flag' button and skip link stay the accepted workaround. Dossier check 19 (gap visible without scrolling) still fails.
**Fix:** as in pass 4: fold the Records card into the header, drop the 'What you need to do' strip when Start review is shown, add a one-line gap headline to Open decisions.
**Test:** sample 1440x900 scroll 0: first entry top < 450, at least 4 rows fully visible, gap headline in the viewport.

### F3 (minor, carried bundle from pass 4 F6): leftovers none above minor
- m1: 'Verified items matched the record 84/85 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).' still on every case (ux5-12-lib09-top-d.png, ux5-12-lib11-top-d.png). Fix: 'Measured on 10 synthetic test cases: verified items matched the record 84 of 85 times. Small sample.'
- m2: unclear charge rows print two reasons and are 196 and 183 px at 1440, 406 at 390 (ux5-walk10-results.json unclear_rows_d, unclear_rows_m; ux5-50-charges-d.png). Fix: one reason per row.
- m4: 'Open record' opens a modal at 1440 (`open_record_dialog_d` 1) over a pane that already shows the record and prints '=== Record 2 ==='. Fix: scroll and highlight in the pane at 1024 and wider; hide the marker.
- m5, m7, m8 (live edit check while typing, double dismiss on flag cards, text-link toggles): not re-measured this pass; carried unchanged from pass 4.
**Tests:** unchanged from pass 2.

### N1 (nit): two 'Dismissed' labels on a dismissed flag or amount, no chevron on the collapsed group bar
A dismissed flag and amount show 'Dismissed' as a chip at the top and again in the footer next to Undo (ux5-walk7-results.json `flag_dismissed_labels_d` 2; ux5-31-dismissed-flag-d.png). **Fix:** one label. **Test:** a dismissed row's text contains 'Dismissed' once.

### N2 (nit): `?` opens nothing from the page top
`q_open_d` and `q_open_m` 0 (ux5-walk8-results.json). **Fix:** open the sheet from anywhere except a text field. **Test:** focus on body, press `?`: the Keyboard shortcuts dialog opens; in a textarea it types a question mark.

### N3 (nit): Filtered by rule bar wraps into a narrow column at 390
See the T-131 review N1 (ux5-12-lib06-top-m.png).

## What is right (do not break)

- The review loop is now safe from the keyboard: a and d stay in the list you are in, say where the rest are, and refuse to flip a dismissed row.
- An edited row stays Needs review, shows the original beside the new wording, counts as open, and has one primary 'I compared it with the quote'.
- Row dates, flag dates and the letter all read 'January 9, 2026' with the ISO date kept in `datetime`.

```json
{
 "card": "T-060",
 "persona": "ux-designer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "app/frontend at b612176 (git archive b612176; repo tree dirty, 2011 changed files); app at http://127.0.0.1:7995 (fixture backend, ZLAYT_MODE=local); sample case, lib01, lib06, lib09, lib11; 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (b612176), git status --short | wc -l (2011, dirty), git archive b612176 into scratchpad; server PID 16797 stopped with kill, port returns 000",
  "Playwright at 1440x900 and 390x844 touch: sample first load, rows, dates, reasons, gap flag position, first-screen rows; keyboard a, d, long a run, Start review then a and d in Flags; fresh lib09 and lib11 dismiss, accept, Undo, reload with header, pill and chip read each step",
  "lib01, lib06, lib09, lib11 rows, tray, Filtered by rule group, AI-check panel on lib06; edit open and saved on sample entry-3; dismissed flag, amount and entry; export Letter layout radios by mouse and ArrowUp; unclear charge rows, flags panel height, Open record, ? from page top",
  "not exercised: e2e suite, PDF upload, real-model latency, Safari and Firefox, WCAG conformance, dark mode, failed-run stub, empty and oversize input, 1024 and 768 widths, audit drawer, landing and case list; EvenUp, Supio, Filevine and Litify compared by marketing text only"
 ],
 "verdict": "pass",
 "scores": {
  "design_quality": 4,
  "originality": 3,
  "craft": 4,
  "functionality": 4
 },
 "findings": [
  {
   "severity": "minor",
   "title": "F1. Timeline chip shows the case-wide need-review count beside the entry count ('9 entries, 3 items need review' over nine Verified rows)",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-walk1-results.json (chips; all rows verified); ux5-walk4-results.json lib06_d and lib09_d; ux5-01-sample-d.png",
   "why_it_matters": "The count agrees with the header and pill as intended, but in the Timeline's own chip row it reads as 13 of 7 entries and sits above a 'Needs review first' sort with nothing to review.",
   "fix": "Scope the chip ('3 items need review in this case', linked to Start review) or show the entries-only number there.",
   "acceptance_test": "Sample 1440: the chip text contains 'in this case' or equals the count of queue rows with data-state=needs_review."
  },
  {
   "severity": "minor",
   "title": "F2. First screen still 464 px to the first row and 3 rows; the 73-day gap flag is 2,024 px down at 1440 and 4,105 at 390 (carried pass-4 F4)",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-walk1-results.json (gap_y 2024 and 4105, entry-1 y 464, fully_visible_rows 3 and 0); ux5-walk10-results.json flags_h_d 2930, flags_h_m 4946; ux5-01-sample-d.png",
   "why_it_matters": "Dossier check 19 (gap visible without scrolling) still fails; the Show gap flag button and skip link are the accepted alternative, so minor.",
   "fix": "Fold the Records card into the header, drop the next-step strip when Start review is shown, add a gap headline to Open decisions.",
   "acceptance_test": "Sample 1440x900 scroll 0: first entry top < 450, at least 4 rows fully visible, gap headline in the viewport."
  },
  {
   "severity": "minor",
   "title": "F3. Leftovers: 'fixture backend' accuracy line (m1), unclear charge rows with two reasons at 196 and 183 px (m2), Open record modal over the pane that prints '=== Record 2 ===' (m4); m5, m7, m8 not re-measured",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-12-lib09-top-d.png ('on the fixture backend (recorded replies, 10 golden cases, small sample)'); ux5-walk10-results.json unclear_rows_d [196, 183], unclear_rows_m [406, 406], open_record_dialog_d 1; ux5-50-charges-d.png; ux5-51-open-record-d.png",
   "why_it_matters": "Small leftovers that separate this from a finished product; none blocks a demo or hides an excerpt.",
   "fix": "Plain accuracy sentence; one reason per unclear row; open the record in the pane at 1024 and wider and hide the marker.",
   "acceptance_test": "Pass-2 acceptance tests for m1, m2, m4 unchanged."
  },
  {
   "severity": "nit",
   "title": "N1. A dismissed flag or amount shows 'Dismissed' twice (chip and footer)",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-walk7-results.json flag_dismissed_labels_d 2, amount_text_d ('Dismissed\\n\\t\\nDismissed\\nUndo\\nAudit'); ux5-31-dismissed-flag-d.png",
   "why_it_matters": "The row works and Accept is gone; the repeated label is clutter.",
   "fix": "One 'Dismissed' label per row.",
   "acceptance_test": "A dismissed row's text contains 'Dismissed' once."
  },
  {
   "severity": "nit",
   "title": "N2. '?' opens nothing from the page top",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-walk8-results.json q_open_d 0, q_open_m 0",
   "why_it_matters": "A help key should work before anything is selected.",
   "fix": "Open the sheet from anywhere except a text field.",
   "acceptance_test": "Focus on body, press ?: the Keyboard shortcuts dialog opens; inside a textarea it types a question mark."
  },
  {
   "severity": "nit",
   "title": "N3. Filtered by rule bar wraps into an ~80 px column at 390",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-12-lib06-top-m.png",
   "why_it_matters": "The group works; the label reads cramped at phone width.",
   "fix": "Stack label and sentence at narrow widths.",
   "acceptance_test": "At 390 the Filtered by rule summary text is at most two lines."
  }
 ],
 "whats_right": [
  "a and d stay in the list you are in, say where the rest are, and refuse to flip a dismissed row",
  "An edited row stays Needs review, shows the original beside the new wording, counts as open, and has one primary 'I compared it with the quote'",
  "Row dates, flag dates and the letter all read 'January 9, 2026' with the ISO date kept in datetime"
 ],
 "questions_for_chris": [
  "The Timeline chip now carries the case-wide need-review count (F1). Should it be the case number with a scope word, or the entries-only number, given that Start review is the single way into the rest?"
 ]
}
```
