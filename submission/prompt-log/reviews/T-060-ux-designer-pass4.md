# T-060 pass 4: enterprise UI/UX review (ux-designer-reviewer)

**Verdict: pass.** No blocker, no major. The four pass-3 items you asked about are fixed (plain titles, the collapsed Dismissed group, the AI-check row for a tray flag, the T-096 no-sentences copy), plus the pass-3 nit on the More button name. This is my second consecutive pass with no major (pass 3 and pass 4), so on my side the stop rule is met; the paralegal pass 4 and the accessibility result are not mine. Six minors and two nits remain; two of the minors are new this pass (developer words in the row reason line, disagreeing need-review counts) and one is a keyboard error-prevention concern.

Scores (1 to 5), pass 1 -> 2 -> 3 -> 4: design quality 2 -> 4 -> 4 -> 4, originality 2 -> 3 -> 3 -> 3, craft 2 -> 3 -> 4 -> 4, functionality 3 -> 4 -> 4 -> 4. Craft stays at 4: the pass-3 clipping, the Dismissed-row and the tray-row defects are gone, but the new row-reason wording leak and the unreconciled counts keep it from 5. No score is 2 or below.

## Scope and how I ran it

- Pinned: the card's frontend commit is e293daa. `git rev-parse --short HEAD` printed `433ac1c` (HEAD moved), `git status --short | wc -l` printed 1926 (dirty), and `git diff --stat e293daa HEAD -- app/frontend` printed nothing, so the frontend at HEAD is the e293daa one. I ran `git archive e293daa` into the session scratchpad (`.../scratchpad/app4`), `PORT=7991 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own `ZLAYT_DB`. Listener PID 26169, stopped with `kill 26169`; `curl http://127.0.0.1:7991/api/health` then printed `000`.
- Playwright (project venv) at 1440x900 and 390x844 touch: landing and case list (both widths), sample case (results, first screen, row buttons, edit open, bad number, save, flags, charges, export with pending items, Open record), library cases lib06, lib09, lib11 (and lib01 with a route rewrite to strip sentences, the same method as tests/e2e/test_suggestions.py) at both widths, dismiss then second dismiss then Undo then reload (Dismissed group), `d` and `a` and `j` and Start review keyboard paths, `?` from the page top, Tab count to the first Accept, the AI-check panel on lib06 (tray flag) at both widths, computed-style census, text scans for developer words.
- Not exercised: PDF upload, real-model latency, Safari and Firefox, WCAG conformance (accessibility-reviewer), dark mode (not re-walked; unchanged since pass 3), the failed-run stub and the empty and oversize input states (not re-walked; unchanged since pass 2), 1024 and 768 widths, the audit drawer. Competitor comparison is to their marketing text only (research/ui-references.md); I saw no UI of EvenUp, Supio, Filevine or Litify.
- Evidence and scripts: `artifacts/review-evidence/T-060-pass4/` (`ux4-*`).

## The four items you asked me to verify

| Item | Status | Evidence |
|---|---|---|
| Plain titles | **Fixed** | Header and tab title read 'Letter of protection, billed vs. adjusted', 'Spanish-language records, back pain', 'Prior conditions and charge ledger', 'ER visit, then a treatment gap'; case list tiles use the same names; a scan for `lib\d\d`, `case lib`, underscores found none on the case list at either width (ux4-walk2-results.json lib06_d_header, caselist_scan_d null; ux4-02-caselist-d.png). Residual: the calibration line still says 'on the fixture backend (recorded replies, 10 golden cases, small sample)' on every case (lib09_d_calib) |
| Collapsed Dismissed group | **Fixed** | Dismissed entry leaves `[data-testid=queue]` (`dis_d_in_queue` false), appears under 'Dismissed (1) Not in the letter. Open to read them or press Undo.', stays open for the one just dismissed, is collapsed after reload (`dis_d_reload_open` false), only the summary is struck through (`dis_d_strike` lists `summary` only, never the excerpt), Undo from the group returns the row to the queue and the count to '1 of 19 decided' (ux4-walk3-results.json; ux4-40-dismissed-group-d.png, ux4-43-dismissed-collapsed-d.png) |
| AI-check row agrees with the tray | **Fixed** | lib06 tray: 'Nothing to accept here. Read what the AI suggested below'. AI-check row for the same flag: chip 'Left out of the letter', no 'Your decision', action line 'Nothing to accept here. It is left out of the letter. If it matters, open the record and check it yourself.' (ux4-51-judge-panel-lib06-d.png, jp_d_text). 'See the steps' and 'Code said' are gone (now 'Why this status' and 'The code check said'). Residual: see F5 |
| T-096 copy | **Fixed** | With sentences stripped from a tray record, the form shows the backend reason once: 'This record has no Date and Source lines, so no sentence can be cut from it.' (`l01_d_nosent`, `l01_m_nosent`; the form text has the legend plus that one line and no second 'Why:' sentence; ux4-60-nosentences-d.png). Residual: the tray item above it doubles a different sentence (F5) |

Also fixed since pass 3: the translation caution now wraps in full and decided summaries clamp to two lines (ux4-40-dismissed-group-d.png: 'Check: translated by AI; read the original quote yourself' complete); the More button's accessible name starts with its label (`more_by_role` 1; aria-label 'More of Austin EMS run report, 2026-01-09'); the unclear-amount 'Keep in notes' is no longer a primary button (`ch_d_primary` is the two detected-charge Accept buttons only).

## Scope cuts

- **Density toggle: accepted.** Rows are 110 to 138 px at 1440 and 246 to 330 px at 390 (ux4-walk1-results.json rows_d, rows_m), 3 rows fully visible on the sample first screen. A second control for a need that the default already meets would only add a setting. If F4 (first row at 464, gap flag far down) is fixed, nobody asks for it.
- **Long dates in rows: accepted as a deferral for this milestone, not as final; still a minor (carried in F6).** Rows say '2026-01-09' while the gap card says 'March 6, 2026' and the letter says 'January 9, 2026', so one screen mixes formats. ISO is unambiguous and the record itself prints ISO, which is why I do not call it a major. But the stated reason (the e2e filters on the text) is a test constraint, not a user one: `<time datetime="2026-01-09">January 9, 2026</time>` and an e2e filter on `datetime` keep both. Competitors' marketing shows human-formatted dates (inference).

## Screen polish, 1 to 5 (pass 1 -> 2 -> 3 -> 4; 4 = would pass in a Carbon or Atlassian product)

| Screen | P1 | P2 | P3 | P4 | Why |
|---|---|---|---|---|---|
| Case list and library | 2 | 3 | 3 | 4 | Plain titles and one-line descriptions; two identical 'Sample case' tiles (my own runs) differ only by time; the collapsed disclosure 'Cases (n) and synthetic library' has no chevron or padding (ux4-01-landing-d.png) |
| Paste / upload | 3 | 4 | 4 | 4 | Landing is one 900 px screen; error and oversize states not re-walked |
| Processing and failure | 2 | 4 | 4 | 4 | Not re-walked; code unchanged since pass 2 |
| Timeline and review queue | 2 | 3 | 4 | 4 | Dismissed group, wrapped caution, 2-line summaries, first Accept on screen; row reason in developer words (F1), counts disagree (F2), ISO dates |
| Case checks and AI check | 3 | 3 | 4 | 4 | Tray row agrees with the tray; the row still prints two 'code check said / AI said' pairs (F5); text-link toggles |
| Flags | 2 | 4 | 4 | 4 | Side-by-side conflict evidence unchanged; double dismiss (gap card: Accept, Edit note, Dismiss, Dismiss with reason…, Audit); gap flag at y 2,090 |
| Charges and billing | 2 | 3 | 3 | 3 | 'Keep in notes' no longer primary; unclear rows still print two reasons ('Not counted: a rate, not a bill. rate $185/visit; …' plus an amber box 'This figure is a rate, not a charge…') and are 197 to 199 px (ux4-15-charges-d.png); amount cell 'missing 3 days of work' |
| Source record | 3 | 4 | 4 | 4 | Sticky pane; 'Open record' still opens a modal over it at 1440 and the pane prints '=== Record 2 ===' (ux4-walk5-results.json open_record_modal true) |
| Dates, tray, manual entry | 2 | 3 | 4 | 4 | Dates card with suggested reading and reason is the strongest screen (ux4-30b-lib09-top-d.png); no-sentences copy once; tray entry item doubles a sentence (F5) |
| Export and paragraph | 3 | 4 | 4 | 4 | Blocked notice states why and what is blocking; copy not changed; not re-walked in detail |
| Mobile 390 | 2 | 3 | 4 | 4 | No horizontal scroll on any page (scrollWidth 390 on sample, lib06, lib09, lib11, export, charges); header is one sticky row; dismissed rows are 387 to 407 px with two 'Dismissed' labels (ux4-41-two-dismissed-m.png) |
| Dark mode | 1 | 4 | 4 | 4 | Not re-walked |
| Keyboard | 2 | 3 | 4 | 4 | Skip links, Start review, shortcut sheet work; auto-advance after `a` and `d` jumps across panels (F3) |

## Does it read as a polished enterprise tool?

Yes, for a prototype, and a notch closer than pass 3: the library now reads as a case list a paralegal would recognise, a decided row leaves the working queue, and the AI-check panel and the tray no longer give opposite instructions. What still marks it as built by developers is the wording that falls through from code, not the layout: 'Check: summary token not in excerpt' and 'Check: judge unavailable' in a row, 'fixture backend' in the accuracy line, and three different 'need review' numbers on the first screen. Beside the marketing descriptions of EvenUp, Supio, Filevine and Litify (no UI seen), the review mechanics here (verbatim quote beside every summary, undoable batch, keyboard sheet, side-by-side conflict) are what their pages lead with; their polish at the text level I cannot judge.

## Findings

### F1 (minor): the one-line reason in a row falls back to developer words
`app/frontend/timeline.js:12` maps 9 reason codes to plain words and otherwise prints the lowercased code. The backend already has a plain sentence for about 35 codes (`app/backend/why.py:2-40`). Live: lib06 Record 5 row reads 'Check: summary token not in excerpt' (ux4-walk2-results.json lib06_d_scan, ux4-30-lib06-top.png); the edited sample row reads 'Check: judge unavailable' (ux4-walk4-results.json edit_d_saved). 'token' is on the dossier's developer-word list (check 18), and SUMMARY_TOKEN_NOT_IN_EXCERPT is the code for the product's headline check (a number in the summary that is not in the quote). The Why dialog and the AI-check panel already show the plain sentence ('The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.'), so the row is the only place the paralegal sees the code.
**Fix:** use the server's plain sentence (the `why` text the case JSON already carries for the Why dialog) for every code, and keep the 9-entry map only as a shorter wording where it exists. Never print a lowercased code.
**Test:** for every reason code in `why.py`, the row's 'Check:' text contains no underscore-derived word list; assert `not re.search(r'token|judge|lexicon|llm|fixture', row_text, re.I)` on lib06 entry-5 and on an edited row.

### F2 (minor): three 'need review' numbers on one screen, and the Timeline chip does not move when you decide
Fresh lib09: header '0 of 19 decided · 13 need review', Open-decisions pill '2 entries need review', Timeline chip '3 entries need review'. After one Dismiss: header 12, pill '1 entry needs review', chip still '3 entries need review' (ux4-walk8-results.json before/after; ux4-90-counts-after-dismiss.png). The chip counts entries by state, so a dismissed entry and the undated one still count; the pill and header count what is left to decide. On the sample the header says '3 need review' while the chip says '0 entries need review' (ux4-04-results-d.png). This is the 'State is always visible: how many remain' goal; the header progress is right, so I rate it minor, but it is the closest of my minors to a major: a chip that says 3 after you decided one reads as a stale screen.
**Fix:** the chip counts undecided entries needing review (same number as the pill, the undated entry shown as its own chip, 'In Dates to confirm'); give the header number a noun ('12 items need review') and make the pill list the same items it sums.
**Test:** lib09 fresh: chip number equals pill number; Dismiss entry-2: both drop by one.

### F3 (minor): after `a` or `d` focus jumps to the first remaining blocker 2,900 px away, so the next keystroke decides an item you did not choose
Sample, click Entry 1, press `a`: focus goes to `flag-f_r7_1` ('Accident date source', Needs review) at scrollY 2,960; the second `a` accepts that flag, the third lands on the $185 rate row (ux4-walk6-results.json steps; ux4-81-kb-rows.png). A reviewer running down nine verified entries with `a a a` skips entries 2 to 9 and accepts a conflict flag. Harm is bounded (an accepted flag goes to the internal notes, not the letter, per the Flags panel intro) and the page does scroll to it and announces it, so I rate it minor; it is still error prevention. Shift+A is the only key that asks.
**Fix:** after a decision, move to the next row in the same list (entry, flag or charge), and reserve 'next item that needs review' for Start review and one key (`n`). Or keep the jump but make it only when the row decided was itself a blocker.
**Test:** sample, select entry-1, press `a`: the selected row is entry-2 and the page did not scroll more than one row.

### F4 (minor, carried from pass 3 as m-new1): the first screen still shows 3 rows and the gap flag is 2,090 px down
First row top 464 on the sample (target < 450), 452 on lib06 and lib11, 3 rows fully visible; gap flag y 2,090 at 1440 (pass 3: 2,090; pass 2: 3,015) and 4,181 at 390; the flags panel alone is 2,930 px tall at 1440 (ux4-walk1-results.json lm_d, rows_d; ux4-walk4-results.json flags_d_h). The 'Show gap flag' button and 'Skip to the gap flag' link stay the accepted workaround (T-046 precedent). Records card ('9 records found · Records (9) · Start over') and Open decisions still take 333 px above the Timeline.
**Fix:** as in pass 3: fold the Records card into the header, drop the 'What you need to do' strip when Start review is shown, add a one-line gap headline to Open decisions linking to the card.
**Test:** sample, 1440x900, scroll 0: first entry top < 450, at least 4 rows fully visible, gap headline in the viewport.

### F5 (minor): duplicated explanations remain in two places
(a) Tray entry item (lib01): 'the demo has no recorded answer for this step' as the reason line, then 'The demo has no recorded AI answer for this step, so this item has not been checked.' directly under it (ux4-walk4-results.json l01_d_tray_text). The T-096 fix removed this pattern for no-sentences, not here. (b) AI-check row for the tray flag prints two 'The code check said / The AI said' pairs, and the second pair contradicts the lead: lead 'The second check does not find this flag supported', then 'The AI said: The AI found it.' (ux4-51-judge-panel-lib06-d.png, 'Degenerative wording · Record 5').
**Fix:** one reason line per tray item (keep the sentence, drop the short code reason); for a tray flag show only the lead and 'Left out of the letter', and move the code and AI lines into 'Why this status'.
**Test:** lib01 tray item text contains 'no recorded' once; lib06 judge row for the tray flag has at most one 'The AI said'.

### F6 (minor, carried bundle): pass-2 and pass-3 leftovers, none above minor
- m1 (second half): 'on the fixture backend (recorded replies, 10 golden cases, small sample)' on every case (ux4-walk2-results.json lib09_d_calib; ux4-43-dismissed-collapsed-d.png). Fix: 'Measured on 10 synthetic test cases: verified items matched the record 84 of 85 times. Small sample.'
- m2: unclear charge rows print two reasons and are 197 to 199 px at 1440 (302 to 406 at 390).
- m3: ISO dates in rows (accepted deferral above).
- m4: 'Open record' modal at 1440 over a pane that already shows the record; pane prints '=== Record 2 ==='.
- m5: edit has a static line ('When you save, the code checks every number, date and negation…') and a post-save note ('Saved and re-checked… found no difference'), both new and good, but typing ' Extra 99 mg.' still gives no reaction until Save (ux4-71-edit-bad-m.png). The 'Original' text is shown after save on the row (ux4-72-edit-saved-d.png), not above the field while editing.
- m7: every flag card has 'Dismiss' and 'Dismiss with reason…'; the date card keeps disabled Accept and Edit.
- m8: 'Show▾' text-link toggles; the blocked-export notice is red rather than amber.
**Tests:** unchanged from pass 2.

### N1 (nit): Dismissed group affordance
The collapsed bar ('Dismissed (1) Not in the letter. Open to read them or press Undo.') has no chevron, the open rows keep a secondary Accept beside 'Dismissed' and 'Undo', and show 'Needs review' and 'Dismissed' chips together; at 390 each dismissed row is 387 to 407 px (ux4-43-dismissed-collapsed-d.png, ux4-41-two-dismissed-m.png). **Fix:** chevron on the bar, drop Accept in the group (Undo restores), one chip.

### N2 (nit): `?` opens nothing from the page top
Unchanged (`q_top_open` false). Accepted by you in the handoff because the negative key test asserts it; the test should assert a text field is not hijacked, not that help is unavailable. **Fix:** open the sheet from anywhere except a text field.

## What is right (do not break)

- The Dismissed round trip: the row leaves the queue, the header count moves, Undo from the group restores it in one click, and the group is collapsed on reload.
- The Dates-to-confirm card: both readings as radios, the suggested one pre-selected with its reason, 'The tool never guesses' stated above it (ux4-30b-lib09-top-d.png).
- Row verbatim excerpt beside the summary with a record and provider caption, and 'More' expanding in place (entry row 138 to 176 px).

```json
{
 "card": "T-060",
 "persona": "ux-designer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "app/frontend at e293daa (git archive e293daa; HEAD 433ac1c has an identical app/frontend); app at http://127.0.0.1:7991 (fixture backend, ZLAYT_MODE=local); sample case, lib06, lib09, lib11, lib01 (route rewrite); 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (433ac1c), git status --short | wc -l (1926, dirty), git diff --stat e293daa HEAD -- app/frontend (empty), git archive e293daa into scratchpad; server PID 26169 stopped with kill, port returns 000",
  "Playwright at 1440x900 and 390x844 touch: landing and case list, sample results, first screen, row buttons, edit open, bad number, save, flags, charges, export with pending items, Open record; lib06, lib09, lib11 headers, titles, scans, rows, tray, AI-check panel; lib01 with sentences stripped by route rewrite",
  "Dismiss, second dismiss, Undo from the Dismissed group, reload persistence; keyboard Start review, j, a, d, Tab count to first Accept, ? from page top; need-review counts before and after dismiss on a fresh lib09; computed-style census; text scans for developer words; reading timeline.js:12 and backend/why.py",
  "not exercised: PDF upload, real-model latency, Safari and Firefox, WCAG conformance, dark mode, failed-run stub, empty and oversize input, 1024 and 768 widths, audit drawer; EvenUp, Supio, Filevine and Litify compared by marketing text only"
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
   "title": "F1. Row reason line falls back to lowercased reason codes: 'Check: summary token not in excerpt', 'Check: judge unavailable'",
   "evidence": "app/frontend/timeline.js:12 (9-code map, else toLowerCase().replace(/_/g,' ')); app/backend/why.py:2-40 (plain sentence for ~35 codes); artifacts/review-evidence/T-060-pass4/ux4-walk2-results.json lib06_d_scan; ux4-walk4-results.json edit_d_saved; ux4-30-lib06-top.png",
   "why_it_matters": "The one-sentence reason is what tells the paralegal why a row needs review; 'token' is developer vocabulary (dossier check 18) on the product's headline check, and the plain sentence already exists server-side.",
   "fix": "Render the server's plain sentence for every code; never print a lowercased code.",
   "acceptance_test": "On lib06 entry-5 and on an edited row, the 'Check:' text matches none of token, judge, lexicon, llm, fixture, and contains no word list derived from a code."
  },
  {
   "severity": "minor",
   "title": "F2. Three different 'need review' numbers on one screen; the Timeline chip does not drop after a decision",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-walk8-results.json (fresh lib09: header 13, pill '2 entries need review', chip '3 entries need review'; after Dismiss: header 12, pill 1, chip 3); ux4-90-counts-after-dismiss.png; sample header '3 need review' vs chip '0 entries need review' in ux4-04-results-d.png",
   "why_it_matters": "Remaining work is the number the reviewer steers by; a chip that stays at 3 after a decision reads as stale, and the header number has no noun.",
   "fix": "Chip counts undecided entries needing review (same as the pill); undated entry has its own chip; header says '12 items need review'.",
   "acceptance_test": "Fresh lib09: chip number equals pill number; after Dismiss on entry-2 both drop by one."
  },
  {
   "severity": "minor",
   "title": "F3. Keyboard a and d jump focus to the first remaining blocker (a flag 2,900 px away), so the next key decides an unchosen item",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-walk6-results.json steps (click entry-1, a -> flag-f_r7_1 scrollY 2960, a -> amount-$185); ux4-walk5-results.json after_d; ux4-81-kb-rows.png",
   "why_it_matters": "Error prevention: a run of a-key presses on verified entries accepts a conflict flag instead. Bounded harm (flags go to internal notes) and the page scrolls and announces, so minor.",
   "fix": "Advance to the next row in the same list after a decision; keep 'next item needing review' for Start review and a separate key.",
   "acceptance_test": "Sample, select entry-1, press a: selected row is entry-2 and the page scrolled less than one row height."
  },
  {
   "severity": "minor",
   "title": "F4. First screen still 464 px to the first row and 3 rows; the 73-day gap flag is 2,090 px down at 1440 and 4,181 at 390 (carried m-new1)",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-walk1-results.json (lm_d gap 2090, entry1 464; fully_visible_d 3; lm_m gap 4181); ux4-walk4-results.json flags_d_h 2930; ux4-04-results-d.png",
   "why_it_matters": "Dossier check 19 (gap visible without scrolling) still fails; the Show gap flag button and skip link are the accepted alternative, so minor.",
   "fix": "Fold the Records card into the header, drop the next-step strip when Start review is shown, add a gap headline to Open decisions.",
   "acceptance_test": "Sample, 1440x900, scroll 0: first entry top < 450, at least 4 rows fully visible, gap headline in the viewport."
  },
  {
   "severity": "minor",
   "title": "F5. Doubled explanations remain: tray entry item says 'no recorded answer' twice; the tray-flag AI-check row prints two code/AI pairs, the second contradicting the lead",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-walk4-results.json l01_d_tray_text; ux4-walk3-results.json jp_d_text ('The AI said: The AI found it.' under 'The second check does not find this flag supported'); ux4-51-judge-panel-lib06-d.png",
   "why_it_matters": "The same defect class the T-096 fix removed for no-sentences; contradictory 'AI said' lines on a flag the AI left out of the letter confuse the reviewer about what to trust.",
   "fix": "One reason line per tray item; for a tray flag show the lead and 'Left out of the letter' and move the code and AI lines into 'Why this status'.",
   "acceptance_test": "lib01 tray item text contains 'no recorded' once; lib06 judge row for the tray flag has at most one 'The AI said'."
  },
  {
   "severity": "minor",
   "title": "F6. Pass-2 and pass-3 leftovers (m1 fixture line, m2 duplicate charge reasons and 197-199 px rows, m3 ISO row dates [deferral accepted], m4 Open record modal and raw marker, m5 no live edit check, m7 double dismiss, m8 text-link toggles)",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-walk2-results.json lib09_d_calib ('fixture backend'); ux4-15-charges-d.png; ux4-walk1-results.json iso_d; ux4-walk5-results.json open_record_modal true and pane_text '=== Record 2 ==='; ux4-71-edit-bad-m.png; ux4-walk4-results.json gap_d_btns ['Open records 6 and 7','Why this status','Accept','Edit note','Dismiss','Dismiss with reason…','Audit']",
   "why_it_matters": "Small leftovers that separate this from a finished product; none blocks a demo. The long-dates cut and the density-toggle cut are accepted for this milestone.",
   "fix": "As in pass 2 and pass 3: plain accuracy sentence; one reason per unclear row; Intl date inside <time datetime>; open the record in the pane at 1024 and wider and hide the marker; debounced live check; one dismiss control; chevron toggles.",
   "acceptance_test": "Pass-2 acceptance tests for m1 to m8 unchanged."
  },
  {
   "severity": "nit",
   "title": "N1. Dismissed group: no chevron on the collapsed bar, secondary Accept kept inside the group, two chips ('Needs review' and 'Dismissed'), 387 to 407 px rows at 390",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-43-dismissed-collapsed-d.png, ux4-41-two-dismissed-m.png, ux4-walk3-results.json dis_m_btns",
   "why_it_matters": "The group works; the bar reads as a label not a control, and the row repeats 'Dismissed' twice.",
   "fix": "Chevron on the bar; drop Accept in the group (Undo restores); one chip.",
   "acceptance_test": "The Dismissed bar has an expand icon; a dismissed row has one 'Dismissed' label and no Accept button."
  },
  {
   "severity": "nit",
   "title": "N2. '?' opens nothing from the page top",
   "evidence": "artifacts/review-evidence/T-060-pass4/ux4-walk5-results.json q_top_open false",
   "why_it_matters": "A help key should work before anything is selected; the handoff says the negative key test asserts it does nothing.",
   "fix": "Open the sheet from anywhere except a text field; change the test to assert a text field is not hijacked.",
   "acceptance_test": "Focus on body, press ?: the Keyboard shortcuts dialog opens; inside a textarea it types a question mark."
  }
 ],
 "whats_right": [
  "The Dismissed round trip: row leaves the queue, count moves, Undo from the group restores it in one click, group collapsed after reload",
  "The Dates-to-confirm card with both readings, the suggested one pre-selected with its reason, and 'The tool never guesses' above it",
  "Verbatim excerpt beside the summary in every row with a record and provider caption, and More expanding in place"
 ],
 "questions_for_chris": [
  "Should 'after a decision, move to the next item that needs review' (even in another panel) stay as the keyboard default, or move to the next row in the same list (F3)? It is a product choice, not a defect in the code."
 ]
}
```
