# T-131 review (ux-designer-reviewer): keyboard focus, one need-review count, plain reasons, long dates

**Verdict: pass.** Every T-131 acceptance item holds on the running app at 1440 and 390. No blocker, no major. One minor (the Timeline chip now carries the case-wide count) and one nit (Filtered by rule header at 390). Evidence: `artifacts/review-evidence/T-131-pass5/` (`ux5-*`).

## Scope and how I ran it

- Pinned: `git rev-parse --short HEAD` printed `b612176`, the card commit; `git status --short | wc -l` printed `2011` (dirty tree), so I did not serve the repo root. I ran `git archive b612176` into the session scratchpad (`.../scratchpad/app5`), `PORT=7995 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own `ZLAYT_DB`. Listener PID 16797, stopped with `kill 16797`; `curl http://127.0.0.1:7995/api/health` then printed `000`.
- Playwright (project venv) at 1440x900 and 390x844 touch: sample case first load and rows; keyboard `a`, `a`, `a`, `d`, `d` from entry-1 and a long `a` run; Start review then `a` and `d` runs inside the Flags panel; fresh lib09 and lib11 (dismiss entry, dismiss flag, accept, Undo, reload, header/pill/chip read each time); lib01, lib06, lib09, lib11 rows, tray and Filtered by rule group at both widths; AI-check panel on lib06 (tray flag); edited sample row; dismissed flag and amount; export with the Letter layout radios (mouse and ArrowUp).
- Not exercised: the e2e suite (QA's), PDF upload, real-model latency, Safari and Firefox, WCAG conformance (accessibility-reviewer), dark mode, the failed-run stub, empty and oversize input, 1024 and 768 widths.

## T-131 acceptance items

| Item | Status | Evidence |
|---|---|---|
| After `a` or `d` focus stays in the same list | **Pass** | Sample, entry-1 then `a a a d d`: focus lands on entry-2, 3, 4, 5, 6 (every `inQueue` true, `inFlags` false), scrollY 0 to 76 on desktop; at 390 it follows the row (scrollY 590 to 1,185). Pass 4 jumped to `flag-f_r7_1` at scrollY 2,960 (ux5-walk2-results.json steps; ux5-02-keys-d.png) |
| A second `a` never accepts an unfocused conflict flag | **Pass** | After `a a a` the two conflict flags are `pending`, `flags_accepted` 0, `charges_accepted` 0; a run of 12 `a` presses ends on entry-9 with the live line 'Nothing more to decide in this list. 14 items are still open in other lists. Press Start review to go to the next one.' and 0 flags or charges accepted. Inside Flags, `a`/`d` stay in the focused group (causation to causation, gap stays on the gap card) (ux5-walk2-results.json, ux5-walk9-results.json) |
| One need-review count shows everywhere and updates on dismiss | **Pass** | Fresh lib09: header '13 items need review', pill '13 items need review', chip '13 items need review'; dismiss an entry: 12/12/12; dismiss a flag: 11/11/11; accept a verified entry: 11/11/11; Undo and reload: 11/11/11. Fresh lib11: 11, 10, 9, 9, 9, 9. Same on sample (3), lib01 (2), lib06 (6) at both widths (ux5-walk5-results.json, ux5-walk4-results.json; ux5-20-lib09-counts-after.png) |
| Rows show plain why sentences, no codes | **Pass** | lib06 entry-5: 'The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.'; lib09 entries 2 and 7: 'AI translation — check against the original.'; lib11 entries 1, 2, 4: 'A second AI check found the summary only partly supported by the quoted text.'; edited sample row: 'The second AI check did not run or did not finish, so this item has not been double-checked.' Scan for `[A-Z]+_[A-Z]+`, token, judge unavailable, lexicon, fixture in rows and tray: none (the one 'llm' hit is the provider name 'Quillmere') |
| Each reason is stated once | **Pass** | lib01 tray item says 'The demo has no recorded AI answer for this step, so this item has not been checked.' once (ux5-walk4-results.json tray_items). lib06 AI-check row for the tray flag 'Degenerative wording · Record 5' now has the lead, the chip 'Left out of the letter' and one action line, and no 'The code check said / The AI said' pair (ux5-walk6-results.json jp_d; ux5-30-judge-panel-lib06-d.png) |
| Rows show long dates | **Pass** | Every row is `<time datetime="2026-01-09">January 9, 2026</time>` (tag TIME, `datetime` ISO, text long) on sample, lib01, lib06, lib09, lib11 at both widths; the row date now matches the gap card and the letter (ux5-walk1-results.json rows) |
| 'Filtered by rule (n)' group present | **Pass** | On lib01, lib06, lib09, lib11 (backend `tray_filtered`, no route rewrite): collapsed by default, header 'Filtered by rule (1) Nothing to decide. These are not flags and are not in the letter.', opens to 'Normal or negative findings (1)', the rule explanation and 'Record 2 “X-ray negative.”'; no buttons, no raw rule name. Sits under 'Could not verify (0): Nothing here.' so the tray is not silently empty (ux5-10-lib0*-filtered-d.png, ux5-12-lib06-top-m.png). The sample case has no filtered item, so the group is absent there |
| Letter layout radio works | **Pass** | Fieldset 'Letter layout' with two radios (`letter-style-standard` checked by default); choosing 'One line per entry (date, provider, quote)' rewrites the preview to one line per entry with the quote and '[Ex. __ / Bates __]'; ArrowUp returns to the two-line layout; scrollWidth 390 at 390 (ux5-walk6-results.json letter_*; ux5-33-export-oneline-d.png) |

## Findings

### F1 (minor): the Timeline chip now shows the case-wide count, so it contradicts the rows under it
The chip row inside the Timeline header reads '9 entries · 3 items need review · 9 quote match' on the sample while all nine rows are Verified; lib06 reads '7 entries · 6 items need review' with one row needing review; lib09 '7 entries · 13 items need review' with two. The number matches the header and the pill, which is what T-131 asked for and what my pass-4 fix said, but sitting beside '7 entries' it reads as 13 of 7. The sort control beside it says 'Needs review first' over a list with none. Evidence: ux5-walk1-results.json (`chips`, rows all `verified`), ux5-walk4-results.json lib06_d, lib09_d; ux5-01-sample-d.png.
**Fix:** give the chip a scope ('3 items need review in this case', or link it to Start review), or show the entries-only figure as '0 entries need review' and keep the case number in the header and the pill.
**Test:** sample at 1440: the Timeline chip text includes the word 'case' or 'in total', or equals the number of `[data-testid=queue] [data-state=needs_review]` rows.

### N1 (nit): the Filtered by rule bar at 390 wraps into a narrow column
'Filtered by rule (1)' takes about 80 px with 'Nothing to decide. These are not flags and are not in the letter.' beside it, wrapping to four lines (ux5-12-lib06-top-m.png). Fix: stack the label and sentence at narrow widths. Test: at 390 the summary text has at most two lines.

## What is right (do not break)

- One need-review number in the header, the pill and the chip, moving together on every dismiss, accept, Undo and reload.
- `a` and `d` walk the list you are in, say when it ends and where the other items are, and say 'press r or Undo first' on a dismissed row.
- The Filtered by rule group: collapsed, names the rule in plain words, no action to take, and the empty tray still says 'Could not verify (0)'.

```json
{
 "card": "T-131",
 "persona": "ux-designer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "app/frontend at b612176 (git archive b612176; repo tree dirty, 2011 changed files); app at http://127.0.0.1:7995 (fixture backend, ZLAYT_MODE=local); sample case, lib01, lib06, lib09, lib11; 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (b612176), git status --short | wc -l (2011, dirty), git archive b612176 into scratchpad, server PID 16797 stopped with kill, port returns 000",
  "Playwright at 1440x900 and 390x844 touch: sample first load and rows; keyboard a, a, a, d, d from entry-1 and a long a run; Start review then a and d inside Flags; focus target, scrollY and live line read after each key",
  "Fresh lib09 and lib11: dismiss entry, dismiss flag, accept verified entry, Undo, reload; header, pill and chip text read after each step",
  "lib01, lib06, lib09, lib11 rows, reason text, dates (TIME tag, datetime, text), tray items, Filtered by rule group (closed, opened, buttons, raw rule name), AI-check panel on lib06; edited sample row; dismissed flag and amount; export Letter layout radios by mouse and ArrowUp",
  "not exercised: e2e suite, PDF upload, real-model latency, Safari and Firefox, WCAG conformance, dark mode, failed-run stub, empty and oversize input, 1024 and 768 widths"
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
   "title": "F1. The Timeline chip shows the case-wide need-review count beside '7 entries', so '9 entries, 3 items need review' sits over nine Verified rows",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-walk1-results.json (chips '9 entries','3 items need review','9 quote match'; all rows state verified); ux5-walk4-results.json lib06_d ('7 entries','6 items need review', one needs_review row) and lib09_d ('13 items need review', two needs_review rows); ux5-01-sample-d.png",
   "why_it_matters": "The count matches the header and the pill as required, but in the Timeline's own chip row it reads as a statement about the entries; a reader sees 13 of 7 and a 'Needs review first' sort with nothing to review.",
   "fix": "Scope the chip ('3 items need review in this case', linked to Start review) or show the entries-only number there and keep the case number in the header and pill.",
   "acceptance_test": "Sample at 1440: the Timeline chip text contains 'in this case' or equals the count of queue rows with data-state=needs_review."
  },
  {
   "severity": "nit",
   "title": "N1. Filtered by rule bar at 390 wraps its label into an ~80 px column",
   "evidence": "artifacts/review-evidence/T-131-pass5/ux5-12-lib06-top-m.png",
   "why_it_matters": "The group works; the narrow label wraps to three lines beside four lines of explanation and reads as cramped.",
   "fix": "Stack label and sentence at narrow widths.",
   "acceptance_test": "At 390 the Filtered by rule summary text is at most two lines."
  }
 ],
 "whats_right": [
  "One need-review number in header, pill and chip, moving together on dismiss, accept, Undo and reload",
  "a and d stay in the focused list, say when it ends, and say 'press r or Undo first' on a dismissed row",
  "Filtered by rule: collapsed, plain rule name, no action, and the tray still shows 'Could not verify (0)'"
 ],
 "questions_for_chris": []
}
```
