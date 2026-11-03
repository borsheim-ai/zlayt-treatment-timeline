# T-060 pass 3: enterprise UI/UX review (ux-designer-reviewer)

**Verdict: pass.** No blocker, no major. The three pass-2 majors are closed: M1 fixed, M2 fixed with a minor residual (row density, first screen), M3 fixed for accepted rows and partial for dismissed rows (now a minor). This is the first pass from me with no major; the stop rule (two consecutive passes with no major) needs one more clean pass, and the accessibility pass is not mine to judge. Eleven minors and two nits remain, none of them new defects of the pass-2 kind.

Scores against pass 1 and pass 2 (1 to 5): design quality 2 -> 4 -> 4, originality 2 -> 3 -> 3, craft 2 -> 3 -> 4, functionality 3 -> 4 -> 4. Craft rises because the dialog defect, the 208 to 275 px rows and the filled Accept on decided rows are gone. Originality stays at 3: it is a clean Carbon-style review list, not a distinctive one. No score is 2 or below.

## Scope and how I ran it

- Pinned: `git rev-parse --short HEAD` printed `e1ce8dc`; `git diff --stat 7d5a45f HEAD -- app/frontend` printed nothing, so the frontend at HEAD is the one in the T-060 round-3 commits (c8e36fb, 5d975ed, d9efc5c, 7d5a45f). `git status --short | wc -l` printed 1742 (dirty), so I used `git archive HEAD` into the session scratchpad (`.../scratchpad/app3`), `PORT=7981 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own `ZLAYT_DB`. Listener PID 49349, stopped with `kill 49349`; `curl http://127.0.0.1:7981/api/health` then printed `000`.
- Playwright (project venv) at 1440x900 and 390x844 touch: landing, sample case (results, first screen, every panel), five library cases (lib01, lib06, lib09, lib11, lib14) at both widths, the Shortcuts button and `?`, Start review, keyboard (Tab order, skip links, `a`, `d`, `k`, `r`, `e`, Shift+A with its dialog), More, Open record, Edit with an unsupported number, Accept, Dismiss, Undo, Accept all verified (button) then Undo last batch, flags, charges, export open with pending items, dark mode, computed-style census, DOM text scans, a real dismissal-suggestion case (three prior dismissals through the real route), the AI-check panel on five cases at two widths.
- Not exercised: PDF upload, real-model latency, Safari and Firefox, WCAG conformance (accessibility-reviewer), the audit drawer, 1024 and 768 widths, a stubbed failed run (unchanged since pass 2), the Exhibit/Bates form. Comparisons to EvenUp, Supio, Filevine and Litify are to what their marketing pages state (research/ui-references.md); I saw no UI of theirs.
- Probe scripts and results are in `artifacts/review-evidence/T-060-pass3/` (`ux3-*`).

## Pass-2 findings, one by one

| # | Pass-2 finding | Status | Evidence |
|---|---|---|---|
| M1 | Shortcuts dialog printed `[object HTMLElement]` | **Fixed** | Shortcuts button opens a dialog with 9 `kbd` rows (j/k, a, d, e, r, o, p, Shift+A, ?) and an intro; `dialog_object` false; page-wide scan for `[object`, `undefined`, `null` false (ux3-walk1-results.json, ux3-23-shortcuts.png). Residual: `?` pressed from the page top (nothing selected) opens nothing, `?` on a selected item does (nit N1) |
| M2 | Rows 208 to 275 px, eight panels above the first row | **Fixed, residual minor (m-new1)** | Rows now 110 to 138 px (was 208 to 275); first row top 464 (was 676); first Accept's bottom edge at 593, inside 900; case checks, next step and AI check are one card; Accept-all moved to the Timeline toolbar. Short of my own target: first row at 464 not < 450, 3 rows fully visible not 4 (ux3-walk1-results.json). At 390: first row at 893 (was 1,205), rows 246 to 330 px (was 446 to 569), target <= 420 met |
| M3 | Decided row kept a filled Accept; dismissed rows stayed | **Fixed for Accepted, partial for Dismissed (m-new2)** | Accepted row: no Accept button, a green check and 'Accepted', Edit, Dismiss, 'Undo' link; Undo returns '0 of 20 decided' (ux3-37-after-accept.png, ux3-walk2-results.json). Dismissed row: 'Dismissed' label with Undo, but still in the queue, quote struck through, Accept (secondary) offered (ux3-39-after-dismiss.png; `dismissed_section` empty) |
| m1 | Slugs and 'fixture backend' | **Open** | Header on lib09 and lib11 reads 'case lib09 spanish interpreter espalda' and 'case lib11 priors and ledger'; calibration line still 'on the fixture backend (recorded replies, 10 golden cases, small sample)' (ux3-walk8-results.json lib11_header, ux3-92-1440-calibration.png). The handoff lists it as backend. Landing is 900 px |
| m2 | Charges geometry, duplicate reasons, primary 'Keep in notes' | **Partial** | Status and Decision columns now start at x 578 / 786 in both tables (was 778 vs 452). Still: unclear rows print two reasons, 'Keep in notes' is a filled primary (2 in the unclear table), rows 197 and 199 px (was 147), amount cell 'missing 3 days of work' (ux3-15-charges.png) |
| m3 | ISO dates in rows | **Open** | `entry-date` '2026-01-09' on all nine rows; the export uses 'January 9, 2026' (ux3-walk1-results.json iso_dates). Handoff: e2e filters on ISO |
| m4 | Modal over the pane; raw `=== Record n ===` marker | **Open** | 'Open record' at 1440 opens a dialog (`open_record_modal` true) while the pane shows the same record with '=== Record 4 ===' (ux3-74-open-record.png, ux3-walk3-results.json) |
| m5 | Edit has no live check | **Open** | Typing ' Extra 99 mg.' and waiting 1.2 s: nothing reacts, label unchanged (ux3-75-edit-bad.png). Handoff lists it as not done |
| m6 | Verified chip icon, two 'need review' counts | **Partial** | Timeline chips now say 'entries' ('0 entries need review') while the header says '3 need review', so the nouns differ; 'Quote matches' chip still has no icon (ux3-04-results-d.png) |
| m7 | Redundant controls | **Open** | Date card keeps disabled Accept and Edit plus 'Confirm the date first. Go to its date choices' (ux3-39-after-dismiss.png); every flag card keeps 'Dismiss' and 'Dismiss with reason…' (ux3-14-flags-panel.png; gap card buttons: Accept, Edit note, Dismiss, Dismiss with reason…, Audit) |
| m8 | Panel alignment, text-link toggles | **Partial** | Case checks, next step and AI check are one card with aligned titles (ux3-04-results-d.png); toggles are still underlined 'Show▾' links. Export-blocked notice not re-measured |
| n1 | Type scale, glyph icons, 120 px mobile header | **Open** | Computed font sizes 14, 12, 16, 13, 20, 15 (6); glyph icons; mobile sticky 32 + 88 px (ux3-walk4-results.json) |

Count of the 12 pass-2 findings: fixed 2 (M1, M2 with residual), partial 4 (M3, m2, m6, m8), open 6 (m1, m3, m4, m5, m7, n1). No open item is above minor.

## Scope cuts: accepted

- **Density toggle: accepted.** The toggle existed to make rows compact. The default rows are now 110 to 138 px and 246 to 330 px at 390; a second control would add a setting for a need that no longer exists. If the first row at 464 px and 3 visible rows (m-new1) are fixed, nobody needs it.
- **Accept-all confirm: accepted.** The conftest contract keeps the labelled button one step. The batch is entries only ('Charges, flags and anything marked needs review always need your own decision'), the button turns into 'Undo last batch (9)' immediately (ux3-80-after-acceptall.png) and nine per-row Undo links appear, so the action is reversible in one click. Shift+A, the key that can fire by accident, asks first and states the count (ux3-72-shiftA.png). That meets dossier check 9 and the error-prevention heuristic better than a confirm on every click would.

## Screen polish, 1 to 5 (pass 1 -> pass 2 -> pass 3; 4 = would pass in a Carbon or Atlassian product)

| Screen | P1 | P2 | P3 | Why |
|---|---|---|---|---|
| Case list and library | 2 | 3 | 3 | Landing is one 900 px screen; slugs and mid-word clamps remain (m1) |
| Paste / upload | 3 | 4 | 4 | Not re-walked beyond the landing; unchanged |
| Processing and failure | 2 | 4 | 4 | Not re-walked; code unchanged since pass 2 |
| Timeline and review queue | 2 | 3 | 4 | 110 to 138 px rows, quote beside the summary, first Accept on screen, decided rows read as decided; ISO dates, clipped caution line (m-new3) |
| Case checks and AI check | 3 | 3 | 4 | One card, one next step; text-link toggles |
| Flags | 2 | 4 | 4 | Side-by-side evidence unchanged; double dismiss (m7); gap flag at y 2,090 (m-new1) |
| Charges and billing | 2 | 3 | 3 | Columns aligned; rows taller, reasons doubled, primary on not-totaled (m2) |
| Source record | 3 | 4 | 4 | Sticky pane; modal duplicate and raw marker (m4) |
| Dates, tray, manual entry | 2 | 3 | 4 | Radio with suggested reading and reason; tray row has plain lead and 'Nothing to accept here'; disabled row remains |
| Export and paragraph | 3 | 4 | 4 | Summary line names what is in and out ('9 entries, 0 charges in letter ... 14 items pending (10 flags)'), pending items under their own heading, Copy letter and Download .txt |
| Mobile 390 | 2 | 3 | 4 | No horizontal scroll on any page; every row button 44 px; rows 246 to 330 px; first row at 893 px behind about one screen of status panels; link row is 36 px |
| Dark mode | 1 | 4 | 4 | Spot-checked on lib09 (ux3-65-dark-top.png) |
| Keyboard | 2 | 3 | 4 | Skip links reach dates, the dismissal suggestion or the first item in Tab + Enter; shortcut sheet works; Start review button |

## Does it read as a polished enterprise tool?

On the sample case, yes, for a prototype: a sticky case header with progress and the primary action, state chips with icons, captioned verbatim evidence in every row, side-by-side conflict quotes, a source pane, an undoable batch action, a keyboard sheet, light and dark from one token layer. Set beside the marketing descriptions of EvenUp, Supio, Filevine and Litify (no UI seen), it now has what their lists lead with. Three things still give it away as a prototype: library cases show file slugs as titles (m1), row dates are ISO while the letter uses long dates (m3), and two small copy-and-control leftovers (two reasons per unclear charge, two dismiss buttons per flag). None blocks a demo; all are cheap.

## Findings

### m-new1 (minor): first screen is close but not at the target; the gap flag is still 2,090 px down
`ux3-walk1-results.json`: first row top 464 (target < 450), `rows_fully_visible` 3 (target 4), gap flag at y 2,090 at 1440x900 (pass 2: 3,015; pass 1: 4,161). Three status blocks above the Timeline (Records, Open decisions, Case checks) take 464 - 131 = 333 px. Dossier check 19 (73-day gap visible without scrolling) still fails; the pane's 'Show gap flag' button and 'Skip to the gap flag' link are the workaround. I rate it minor because the work (first Accept in view, 110 to 138 px rows) is now above the fold; this is my judgement against the pass-2 target, not a spec constraint.

### m-new2 (minor): a dismissed row stays in the queue, with its verbatim quote struck through and Accept offered
`ux3-39-after-dismiss.png`, `ux3-59m-lib09-dismissed.png`. The Accepted half of M3 is fixed. The dismissed row keeps its place in the list, strikes through the record's own quote (the record did not change, only the decision), and shows a secondary Accept beside 'Undo'. The handoff names the 'Dismissed (n)' group as not done.

### m-new3 (minor): the AI-translation caution and the summary are clipped to one line in collapsed rows
`ux3-39-after-dismiss.png` (1440): '▲ Check: translated by AI; read the o…' and, on decided rows, 'Patient reports pain 6/10 that worsens when raising the arm. Denies lo…'. At 390 the caution wraps in full; at 1440 the safety sentence is cut. A sentence whose job is to say 'read the original yourself' should not be the clipped one.

### m-new4 (minor): the AI-check panel row for a could-not-verify flag contradicts the tray
`ux3-117-judge-panel-lib06.png` and `ux3-117-tray-lib06.png`: the panel row says 'Your decision: Not reviewed' and 'What you need to do: ... Edit it, accept it if you agree with it, or dismiss it', while the tray says 'Nothing to accept here'. Same panel still uses 'See the steps', 'Technical details', 'Code said' and 'phrase list'. See T-117 review.

### Pass-2 minors still open (m1, m3, m4, m5, m7, n1) and partial (m2, m6, m8)
Evidence in the table above; fixes unchanged from pass 2. Of these, the quickest wins for a demo are m1 (library names), m3 (`Intl.DateTimeFormat` inside `<time>` and an e2e filter on `datetime`), m7 (one dismiss control) and m2 (secondary 'Keep in notes').

### N1 (nit): `?` does nothing from the page top
Mouse at (5,5), focus on body, `?` pressed: no dialog. After Start review, `?` opens it. The dialog intro says letter keys need a selected item, but `?` is a help key. Fix: open the sheet from anywhere except a text field.

### N2 (nit): 'More' has a different accessible name from its label
`aria-label` 'Show all of Dr. Alvarez, primary care, 2026-01-16' on a button that reads 'More'; Playwright `get_by_role('button', name='More')` finds nothing. Deferred to accessibility-reviewer.

## What is right (do not break)

- The decided-row treatment and 'Undo last batch (n)': one click reverses the batch, and Shift+A is the only path that asks.
- Skip links that land on the most blocking work (dates form, dismissal suggestion, first item) in Tab + Enter, at both widths.
- Compact row with the quote beside the summary, captioned with record and provider, 110 to 138 px, and More for the full excerpt in the same row.

```json
{
 "card": "T-060",
 "persona": "ux-designer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "app/frontend at HEAD e1ce8dc (frontend identical to 7d5a45f; commits c8e36fb, 5d975ed, d9efc5c, 7d5a45f); app at http://127.0.0.1:7981 (git archive HEAD, fixture backend, ZLAYT_MODE=local); sample case and library cases lib01, lib06, lib09, lib11, lib14; 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (e1ce8dc), git diff --stat 7d5a45f HEAD -- app/frontend (empty), git status --short | wc -l (1742, dirty), git archive HEAD into scratchpad; server PID 49349 stopped with kill, port returns 000",
  "Playwright at 1440x900 and 390x844 touch: landing, sample results, five library cases, Shortcuts button and ? key, Start review, Tab order and skip links, a/d/k/r/e/Shift+A, More, Open record, Edit with unsupported number, Accept, Dismiss, Undo, Accept all verified and Undo last batch, flags, charges, export with pending items, dark mode, computed-style census, AI-check panel on five cases at two widths",
  "real dismissal-suggestion case (three prior dismissals via the real route), calibration route (real stale state), reading present.py and manual.js for the sentences_reason copy",
  "not exercised: PDF upload, real-model latency, Safari/Firefox, WCAG conformance, audit drawer, 1024 and 768 widths, failed-run stub, Exhibit/Bates form; EvenUp, Supio, Filevine, Litify compared by marketing text only"
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
   "title": "m-new1. First row at 464 px and 3 rows on the first screen (target < 450 and 4); the 73-day gap flag is still 2,090 px down",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-walk1-results.json: landmarks entry1 464, gap 2090; rows_fully_visible 3; entry heights 110 to 138; artifacts/review-evidence/T-060-pass3/ux3-04-results-d.png",
   "why_it_matters": "Dossier check 19 (gap flag visible without scrolling) still fails; the pass-2 M2 target was 4 rows on the first screen. The work itself is now above the fold, so this is minor.",
   "fix": "Fold the Records card into the header or the Open decisions card, and drop the 'What you need to do' strip when Start review is shown. Optionally promote a one-line gap headline into the Open decisions card with a link to the gap card.",
   "acceptance_test": "Sample case, 1440x900, scroll 0: first entry top < 450, at least 4 [data-entry-id] rows fully visible; the gap flag headline is in the viewport."
  },
  {
   "severity": "minor",
   "title": "m-new2. Dismissed rows stay in the queue with the record's quote struck through and Accept offered",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-39-after-dismiss.png, artifacts/review-evidence/T-060-pass3/ux3-59m-lib09-dismissed.png, artifacts/review-evidence/T-060-pass3/ux3-walk2-results.json (dismissed_section [])",
   "why_it_matters": "The Accepted half of pass-2 M3 is fixed; a dismissed row still takes full row space and strikes through verbatim record text, which did not change.",
   "fix": "Collapse dismissed rows under a 'Dismissed (n)' disclosure at the end of the queue with Undo; strike through the summary only, never the quote.",
   "acceptance_test": "After Dismiss the row is not a child of [data-testid=queue] and appears under 'Dismissed (1)'; the excerpt block has no line-through."
  },
  {
   "severity": "minor",
   "title": "m-new3. The 'translated by AI; read the original quote yourself' caution and decided summaries are clipped with an ellipsis at 1440",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-39-after-dismiss.png ('Check: translated by AI; read the o...'), artifacts/review-evidence/T-060-pass3/ux3-37-after-accept.png",
   "why_it_matters": "The caution exists to make the reviewer read the original; clipping it removes the instruction. Clipping the summary of an accepted row hides what will go into the letter until More is pressed.",
   "fix": "Let the caution wrap (it already does at 390) and give it its own line; clamp decided summaries to 2 lines, not 1.",
   "acceptance_test": "At 1440 the caution text of a translated row is fully visible (scrollWidth <= clientWidth)."
  },
  {
   "severity": "minor",
   "title": "m-new4. AI-check panel row for a could-not-verify flag tells the reviewer to accept it; the tray says nothing can be accepted",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-117-judge-panel-lib06.png ('Degenerative wording · Record 5 ... Your decision: Not reviewed ... accept it if you agree with it, or dismiss it'), artifacts/review-evidence/T-060-pass3/ux3-117-tray-lib06.png ('Nothing to accept here')",
   "why_it_matters": "Two surfaces give opposite instructions for the same item; the panel also still uses 'See the steps', 'Technical details', 'Code said' and 'phrase list', which pass 2 reported gone on the closed panel.",
   "fix": "For tray items the panel row shows 'Left out of the letter' and no decision line or action sentence; use 'Why this status' as the one label for the steps.",
   "acceptance_test": "The judge row for a [data-tray-kind=flag] item contains no 'accept' and no 'Your decision'."
  },
  {
   "severity": "minor",
   "title": "Pass-2 m1/m3/m4/m5/m7/n1 still open; m2/m6/m8 partial",
   "evidence": "Table in this review; artifacts/review-evidence/T-060-pass3/ux3-walk1-results.json (iso_dates), ux3-walk3-results.json (open_record_modal true, edit_live unchanged), ux3-walk8-results.json (lib11_header 'case lib11 priors and ledger', primary_in_unclear 2, census font sizes 6), ux3-14-flags-panel.png, ux3-15-charges.png",
   "why_it_matters": "Slug titles, ISO row dates, a duplicate record modal, no live edit check, two dismiss controls and primary 'Keep in notes' are what remain between this and a product that looks finished.",
   "fix": "As in pass 2: manifest names; Intl long dates in rows; open the record in the pane at >= 1024; debounced edit check; one dismiss control; secondary 'Keep in notes'; one reason per unclear row.",
   "acceptance_test": "Pass-2 acceptance tests for m1 to m8 and n1 unchanged."
  },
  {
   "severity": "nit",
   "title": "N1. '?' opens nothing when no item is selected",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-walk1-results.json (q_dialog_open false from the page top) versus ux3-walk3-results.json (q_dialog_open_on_item true)",
   "why_it_matters": "The help key should work where help is needed, which is before anything is selected.",
   "fix": "Open the sheet from anywhere except a text field.",
   "acceptance_test": "Focus on body, press ?: the Keyboard shortcuts dialog opens."
  },
  {
   "severity": "nit",
   "title": "N2. 'More' button's accessible name does not contain its visible label",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-dbg.py output: aria-label 'Show all of Dr. Alvarez, primary care, 2026-01-16' on a button reading 'More'",
   "why_it_matters": "Voice-control users say 'click More'. Severity is for accessibility-reviewer.",
   "fix": "Start the aria-label with 'More'.",
   "acceptance_test": "get_by_role('button', name='More') resolves on a row."
  }
 ],
 "whats_right": [
  "Decided rows read as decided, and 'Undo last batch (n)' reverses the batch in one click, with Shift+A the only path that asks",
  "Skip links land on the most blocking work in Tab + Enter at both widths",
  "Compact 110 to 138 px rows with the captioned quote beside the summary and the full excerpt one click away in the same row"
 ],
 "questions_for_chris": [
  "Should library cases carry paralegal-facing titles in the manifest so the header and case list stop showing file slugs (m1, carried from pass 2)?"
 ]
}
```
