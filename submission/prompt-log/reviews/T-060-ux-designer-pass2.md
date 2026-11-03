# T-060 pass 2: enterprise UI/UX review (ux-designer-reviewer)

**Verdict: changes.** No blocker. 3 majors, 8 minors, 1 nit. Pass 1 had 15 majors and 11 minors. Of the 26 pass-1 findings: 16 fixed (several with a small residual minor), 8 partial and 2 open (F20 ISO dates, F25 edit preview). The three majors are one new defect (the Shortcuts dialog prints `[object HTMLElement]`), one density gap (F1/F6 residual) and one decided-row gap (F4/F5 residual). The stop rule (two consecutive passes with no major) is not met yet.

Scores against pass 1 (1 to 5): design quality 2 -> 4, originality 2 -> 3, craft 2 -> 3, functionality 3 -> 4. Craft stays at 3 because of the `[object HTMLElement]` dialog, the `Starting......` label and the misaligned panel titles. No score is 2 or below, so no score needs a matching major; M1 to M3 are filed on their own merits.

## Scope and how I ran it

- Pinned: `git rev-parse --short HEAD` printed `b89b9d9`; `git diff --stat 9fcae9b HEAD -- app/frontend` printed nothing, so the UI at HEAD is the one in the three T-060 commits (3e3f3b7 keyboard, eabe2b8 tokens, 9fcae9b layout). `git archive HEAD` into the session scratchpad (`.../scratchpad/app2`), `ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, own `ZLAYT_DB`, 127.0.0.1:7971, PID 79331. I stopped it with `kill 79331`; `curl http://127.0.0.1:7971/api/health` then printed `000`.
- Playwright (project venv), 1440x900 and 390x844 (touch): landing, paste, empty submit, 61,117-character paste, sample case (analyze with the processing state at 0.4 s, results, every panel), library cases lib01, lib06, lib09, lib11, lib14 run to ready, Why dialog, Open record, Edit with an unsupported number, Accept, Reset, Dismiss, Accept all verified, Shift+A, dates to confirm, could-not-verify tray, flags, charges, export blocked then export open, Copy letter with pending items, narrative panel before and after an accept, case switcher opened, dark mode, 1280 / 1024 / 768 widths, a stubbed failed run, keyboard (Tab counts, skip links, `?`, j / a / d / r / e / Shift+A), hover and focus computed styles, font-size / radius / button / chip census, DOM text scans over five library cases, `grep` over app/frontend/*.css.
- Not exercised: PDF upload, real-model latency, Safari and Firefox, WCAG conformance (accessibility-reviewer), the audit drawer, the Exhibit/Bates form, the edit-then-export round trip (covered by earlier cards). Comparisons to EvenUp, Supio, Filevine and Litify are to what their marketing pages state (research/ui-references.md); no UI of theirs was seen. Carbon comparisons follow the pages opened in pass 1; Atlassian is general knowledge. First sample load took 1.3 s at both widths (no stall this time).
- Probe scripts and results sit beside the screenshots in `artifacts/review-evidence/T-060-pass2/` (`ux2-*`; the folder also holds the paralegal reviewer's files, unprefixed).

## Pass-1 findings, one by one

| # | Pass-1 finding | Status | Evidence |
|---|---|---|---|
| F1 | Cases and 15-button library above the work | **Fixed (residual m1, M2)** | Landing 900 px tall (was 1,966). Cases collapse into one disclosure; library tiles are outlined cards, not solid blue. First row top 676 px at 1440 with 10 cases open (was 2,292), 1,205 to 1,417 at 390 (was 4,376). ux2-01-landing-d.png, ux2-60-switcher-open.png, ux2-scan-results.json |
| F2 | No persistent case header | **Fixed** | Sticky header: case name, '0 of 23 decided · 3 need review', progress bar, Export primary; visible at charges and export (ux2-15, ux2-44). At 390: 32 + 88 px sticky (ux2-50m-top.png) |
| F3 | No tokens, 3 palettes, 21 sizes, 7 radii, no hover | **Fixed** | `tokens.css` (91 lines); no hex literal in the other five stylesheets; 6 computed font sizes (14, 12, 16, 13, 20, 15); radii 4 / 6 / 50% (plus one 2 px); one primary `rgb(11, 87, 208)`; buttons 28 and 36 px (44 at <= 768); 9 `:hover` rules; one `:focus-visible` ring (2 px accent, 2 px offset); hover verified: primary -> `rgb(9, 72, 168)`, secondary and ghost -> `rgba(20, 24, 31, .06)` (ux2-walk8-results.json) |
| F4 | Row action cluster | **Partial -> M3** | Edit collision gone; Accept / Edit / Dismiss all 36 px, the four helpers are 28 px text links. Decided rows still show a filled Accept (ux2-37) |
| F5 | State by colour only; amber row fill | **Partial -> M3, m6** | White card with a left bar; machine-state chip plus separate decision chip with glyph icons (ux2-37, ux2-39, ux2-80-lib11-tray.png). Dismissed items not collapsed; Verified chip has no icon |
| F6 | Rows 224 to 302 px; italic grey quote | **Partial -> M2** | Quote is now an upright 15/24 block with the caption 'Excerpt · Record 1 · Austin EMS run report'; AI tag is 'AI draft' and does not wrap; rows 208 to 275 px (was 224 to 302), 446 px at 390 (was 583) (ux2-13-entry1.png) |
| F7 | Eight labels for 'how it was checked' | **Fixed (residual m8)** | 'Why this status' on every row, flag and charge; zero matches for 'How it was checked', 'See the steps', 'Show the checks', 'Technical details' on five cases; 'Ready to export, 18 not reviewed' replaced by 'Export blocked by 1'. 'Audit' still on every item (10 to 29 per page) |
| F8 | Developer vocabulary | **Partial -> m1** | Stage labels mapped, 'translated by AI; read the original quote yourself', no underscores or 'Step n of n:' anywhere. Slugs, 'fixture backend' and 'Starting……' remain |
| F9 | Processing: no progress, contradicting copy | **Fixed** | `progress` element present (2 nodes), 'Drafting summaries (step 2 of 8)' plus 5 skeleton rows (ux2-03-processing-d.png); the 'No model has been called' line is hidden while running; failed run shows 'The analysis did not finish. Your records are kept and finished items are saved.' with a 'Try again' button (ux2-70-failed-d.png, ux2-walk8-results.json failed_text) |
| F10 | Stale 'export is blocked' | **Fixed (residual m8)** | After Accept all verified the notice reads 'Nothing blocks the export now. Click Export again to open it.' (ux2-walk6-results.json); lead sentence is no longer duplicated by 'The export is blocked.' |
| F11 | Literal 'null' under Draft button | **Fixed** | `null` absent before and after an accept (ux2-walk8-results.json null_after false; scan n=0 on five cases) |
| F12 | Dark mode half shipped | **Fixed** | No `rgb(255, 255, 255)` background in dark mode; headings, flag cards, buttons and Export all follow the tokens (ux2-65, ux2-66, ux2-67) |
| F13 | Keyboard orientation | **Partial -> M1** | Four skip links; first Tab on lib01 is 'Skip to the first item to review'; Enter lands on the first needs-review item (sample: the accident-date flag; lib09: entry 4); Tab count to the first row without the skip link is 20 and 23 (was 35); single keys act only from an item (j from the page top is a no-op by design, stated in the dialog); `a` moves to the next needs-review item, `d`, `r`, Shift+A (with a count dialog) work (ux2-walk9-results.json). The `?` dialog is unreadable (M1) |
| F14 | Flag cards | **Fixed (residual m7)** | Gap flag 282 px; two quote blocks side by side with record captions; conflict shows 3 side by side; the 'Quote found word for word' sentence once per section (ux2-14-flags-panel.png, ux2-54m-gap-card.png). Two dismiss controls remain |
| F15 | Charges table | **Partial -> m2** | Right-aligned amounts, 'Keep in notes', unclear group with reasons; row height, duplicate reasons, column geometry open |
| F16 | Red synthetic banner | **Fixed** | 32 px, amber, info icon, sticky, not the error colour (ux2-01-landing-d.png); the blue AI strip is one line (two at 390) |
| F17 | Source pane | **Partial -> m4** | Sticky column beside the list, no longer over the case tiles; exact-offset highlight; modal still opens on top at 1440; raw markers |
| F18 | Toolbar | **Fixed (residual m6)** | Heading, three count chips and the Order select on one row (ux2-04-results-d.png); Export moved to the header |
| F19 | Touch targets and mobile row | **Fixed (residual n1)** | At 390 every row button is 44 px (ux2-walk7-results.json row_btns); row 446 px (was 583). Skip links 40 px, export inputs 38 px |
| F20 | ISO dates in rows | **Open -> m3** | `entry-date` still '2026-01-09' on all rows |
| F21 | Zero-count sections | **Fixed** | 'Could not verify (0)' plus 'Nothing here.' is 18 px; the tray with items is a real section (ux2-80-lib11-tray.png) |
| F22 | Dates-to-confirm card | **Partial -> m7** | Radio choice, 'Suggested · DD/MM' chip, one primary 'Confirm date', 'Date to confirm' chip; disabled Accept row remains |
| F23 | Selected and focused look the same | **Fixed** | Selected row = soft blue wash; focus = 2 px ring with 2 px offset on the button only (ux2-64-focus-in-selected-row.png; computed outline `solid 2px rgb(11, 87, 208)`, offset 2 px) |
| F24 | Copy-letter confirmation | **Fixed** | 'Copy anyway' is the one primary and 'Copy letter' turns secondary; text 'N charges not reviewed · N unclear amounts not reviewed · N flags not reviewed' names the types (ux2-92-copy-confirm.png) |
| F25 | Edit preview | **Open -> m5** | No live check or original in the row (ux2-36) |
| F26 | Page chrome and title | **Fixed** | Title 'Treatment timeline · Sample case' (no 'prototype'); heading 'Records' (no '1.'); header shows product and case name |
| carried | 'other items not reviewed' copy | **Fixed** | See F24 |

Count: fixed 16 (F1, F2, F3, F7, F9, F10, F11, F12, F14, F16, F18, F19, F21, F23, F24, F26) plus the carried copy item; partial 8 (F4, F5, F6, F8, F13, F15, F17, F22); open 2 (F20, F25). Severity of each partial is set by what remains, not by the original rating.

## Token system: applied consistently?

Yes, with small exceptions. `tokens.css` is loaded first; `grep` finds no hex colour in styles.css, review.css, stepper.css, sidebyside.css or suggestions.css, and `var(--` is used 140 / 78 / 83 / 11 / 16 times in them. One palette (light and dark share one token layer), one primary blue (`#0B57D0`), 28 / 36 px controls and 44 px at <= 768, chips all 22 px high with a 4 px radius and 12 px text (four class names, one look), radii 4 and 6 only (plus one 2 px and two `50%`), one focus ring, hover on `.btn`, `.btn--primary`, `.btn--link`, links, form fields, summaries and table rows. Exceptions: two `0.7em` glyph rules (styles.css:84, :137), a type scale whose 12/13/14/15/16 steps are 1 px apart (n1), blue doing four jobs (accent, Verified, AI draft, selected row; m6), and the class prefixes `rv-`, `zs-`, `cs-` still mark three authors although they now read one token set.

## Screen polish, 1 to 5 (pass 1 -> pass 2; 4 = would pass in a Carbon or Atlassian product)

| Screen | Pass 1 | Pass 2 | Why |
|---|---|---|---|
| Case list and library | 2 | 3 | One collapsed disclosure and outlined tiles; slugs, mid-word clamps, unstyled summary row (m1) |
| Paste / upload | 3 | 4 | Clean card, banner, inline errors that keep the paste (ux2-40, ux2-41) |
| Processing and failure | 2 | 4 | Progress bar, mapped stage, skeletons, 'Try again' (ux2-03, ux2-70); 'Starting……' nit |
| Timeline and review queue | 2 | 3 | Header, chips, captioned quotes, one button system; still 208 to 275 px rows, eight panels above (M2), decided rows (M3) |
| Case checks and AI check | 3 | 3 | Text and counts consistent now; misaligned titles, text-link toggles (m8) |
| Flags | 2 | 4 | Side-by-side evidence, one verification line per section, readable cards (ux2-14) |
| Charges and billing | 2 | 3 | Right-aligned, grouped, renamed action; row height and duplicate reasons (m2) |
| Source record | 3 | 4 | Sticky column, exact highlight; double with the modal (m4) |
| Dates, tray, manual entry | 2 | 3 | Radio choice, clear tray cards (ux2-31, ux2-80); redundant disabled row (m7) |
| Export and paragraph | 3 | 4 | One primary at a time, typed warning, long dates, citations (ux2-92, ux2-44) |
| Mobile 390 | 2 | 3 | 44 px targets, no horizontal scroll (no horizontal scroll on the landing, results and export views at 390), 446 to 569 px rows |
| Dark mode | 1 | 4 | Complete and consistent (ux2-65 to ux2-67) |
| Keyboard | 2 | 3 | Skip links, one linear queue, auto-advance; dialog broken (M1) |

## What is still short of the enterprise bar (prioritized)

1. **M1** Shortcuts dialog prints `[object HTMLElement]` (review.js:296). Smallest fix, visible on a '?'.
2. **M2** First screen is status panels, not work: collapse the eight panels above the first row into one strip, let quotes use the row width, target first row < 450 px and rows <= 140 px. This is also what keeps dossier check 19 (gap flag on the first screen) failing at 3,015 px; the pane's 'Show gap flag' button remains the one-click path.
3. **M3** Decided rows: replace the filled Accept with an 'Accepted' state plus 'Undo'; collapse dismissed rows under 'Dismissed (n)'.
4. **m1** Library names, case names and the 'fixture backend' sentence: a manifest edit plus one sentence.
5. **m2** Charges: shared column grid, one reason per row, secondary 'Keep in notes'.
6. **m3, m4, m5** Long dates in rows; open-record in the pane at >= 1024; live check in edit.
7. **m6, m7, m8** Verified icon and colour, header vs chip nouns; redundant controls; panel alignment and chevrons.
8. **n1** Five-step type scale, SVG icon set, 48 px mobile header.

Against the named products (marketing text only for EvenUp, Supio, Filevine, Litify; Carbon pages as opened in pass 1; Atlassian from general knowledge): the app now has what those lists lead with (case header with progress and the primary action, state chips with icons, evidence beside the claim, a record pane, skeleton loading, one theme layer in light and dark). It still lacks what separates a shipped list from a good prototype: a dense first screen (M2), row state that changes the row's controls (M3), consistent names (m1) and a working shortcut sheet (M1).

## What is right (do not break)

- The token layer and the single `.btn` / chip system: one place to change the product's look, verified in light and dark, hover and focus.
- Evidence placement: captioned verbatim quote in every row, flags with record-labelled quote blocks side by side, and the Copy-anyway confirmation that names what is unreviewed.
- Keyboard flow: skip link to the first needs-review item, `a` advancing to the next undecided item, Shift+A asking first with a count.

```json
{
 "card": "T-060",
 "persona": "ux-designer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "app/frontend at HEAD b89b9d9 (frontend identical to 9fcae9b; commits 3e3f3b7, eabe2b8, 9fcae9b); app at http://127.0.0.1:7971 (git archive HEAD, fixture backend, ZLAYT_MODE=local); sample case and library cases lib01, lib06, lib09, lib11, lib14; 1440x900 and 390x844",
 "exercised": [
  "git archive HEAD copy served on 127.0.0.1:7971 (PID 79331, stopped with kill; port returns 000)",
  "Playwright walk at 1440x900 and 390x844 touch: landing, empty submit, 61,117-character paste, sample case processing and results, five library cases, Why dialog, Open record, Edit with unsupported number, Accept, Reset, Dismiss, Accept all verified, Shift+A, dates to confirm, tray, flags, charges, export blocked and open, Copy letter with pending items, narrative panel, case switcher, dark mode, 1280/1024/768, stubbed failed run",
  "keyboard: Tab counts, skip links, ? dialog, j/a/d/r/e/Shift+A",
  "computed-style census (font sizes, radii, buttons, chips), hover and focus styles, DOM text scans over five cases, grep of app/frontend/*.css, reading review.js, input.js, api.py",
  "not exercised: PDF upload, real-model latency, Safari/Firefox, WCAG conformance, audit drawer, Exhibit/Bates form; EvenUp, Supio, Filevine, Litify compared by marketing text only"
 ],
 "verdict": "changes",
 "scores": {
  "design_quality": 4,
  "originality": 3,
  "craft": 3,
  "functionality": 4
 },
 "findings": [
  {
   "severity": "major",
   "title": "M1. The Shortcuts dialog (button and '?') prints '[object HTMLElement]' instead of the shortcut list",
   "evidence": "Press '?' or click Shortcuts at 1440x900 on lib01 or lib09: the dialog body is the intro sentence followed by about 20 lines of '[object HTMLElement],[object HTMLElement]' (artifacts/review-evidence/T-060-pass2/ux2-23-lib01-help.png, artifacts/review-evidence/T-060-pass2/ux2-23-lib09-help.png, artifacts/review-evidence/T-060-pass2/ux2-walk4-results.json). Cause: app/frontend/review.js:296 passes `KEYS.map(([k, v]) => [el(\"dt\"...), el(\"dd\"...)])`, an array of arrays, as one child of `el('dl', ...)`; only one level is flattened. There is no other on-screen shortcut hint: the old 'Keyboard:' paragraph in the Flags panel is gone and no footer hint exists (text scan of the results page, ux2-walk2-results.json text_d).",
   "why_it_matters": "Dossier check 7 (accelerators discoverable on screen) and pass-1 F13. The keys themselves work (skip link, a, d, r, j, Shift+A all verified, ux2-walk9-results.json) but a reviewer cannot find out what they are; the only list is a defect of the same kind as the 'null' under the Draft button in pass 1 (F11). The fix is small but the defect sits on the one discoverability surface.",
   "fix": "Flatten the rows: `KEYS.flatMap(([k, v]) => [el('dt', {}, el('kbd', {}, k)), el('dd', {}, v)])`. Add a Playwright assertion that no dialog or page text contains '[object' or 'undefined' or 'null'. Optionally add the one-line footer hint from pass-1 F13.",
   "acceptance_test": "Press '?' on the sample case: the dialog contains 'Accept the selected item' and 'Dismiss the selected item' and does not contain '[object'. A page-wide text scan for /\\[object|undefined|\\bnull\\b/ is empty in every state of the walk."
  },
  {
   "severity": "major",
   "title": "M2. Entry rows are still 208 to 275 px at 1440, and eight stacked panels sit above the first row, so one entry (without its buttons) is visible at load",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-04-results-d.png, artifacts/review-evidence/T-060-pass2/ux2-13-entry1.png, artifacts/review-evidence/T-060-pass2/ux2-walk3-results.json, artifacts/review-evidence/T-060-pass2/ux2-scan-results.json. ux2-walk3-results.json entry_heights (sample, 1440): 252, 252, 208, 208, 208, 208, 208, 252, 252. ux2-scan-results.json rows_h: lib01 252/252/208..., lib06 275/252/208..., lib11 275/275/252/252/252/252/208/208/252. First row top: 676 (sample, lib01, lib06, lib11), 744 (lib14), 780 (lib09). In ux2-04-results-d.png the stack between the header and row 1 is: Records card, Open decisions, Case checks, 'What you need to do', 'How the AI was checked', Timeline toolbar, 'Accept all verified entries' bar, and a three-line accuracy paragraph (about 545 px, y 131 to 676); at 900 px the first row's Accept / Edit / Dismiss are cut off at the bottom edge. The quote block is capped at about 725 px of a 985 px row, leaving a blank right quarter. At 390, a needs-review row is 569 px and the first entry is at y 1,205 (sample) to 1,417 (lib09) (ux2-walk7-results.json). Pass-1 acceptance test for F6 (at least 5 rows fully visible, collapsed row <= 120 px) is not met.",
   "why_it_matters": "Pass 1 F1 and F6 are mostly fixed (first row 2,300 -> 676 px; rows 224-302 -> 208-275; case list collapsed), but the workspace still opens on status panels, not on the work. A paralegal at 1440x900 sees one verified entry, and the decision buttons are below the fold. Carbon and Atlassian review lists put the first 4 to 6 items on the first screen. Dossier check 19 (73-day gap visible without scrolling) still fails: the sample gap flag is at y 3,015 (pass 1: 4,161 with 12 cases open); the 'Show gap flag' button in the source pane and the 'Open decisions' strip are the workaround.",
   "fix": "1) Merge 'Case checks', 'What you need to do' and 'How the AI was checked' into one 40 px strip that expands (one chevron, one status chip), and fold the accuracy paragraph into the info popover or the Why dialog. 2) Move 'Accept all verified entries' into the Timeline toolbar as a secondary button. 3) Let the quote use the full row width and clamp it to 2 lines with a keyboard-reachable 'Show full excerpt'; put the four text links (Why this status, Open record, Audit, Change quote) in a 'More' menu or on the caption line so the row is two lines of text plus one button row. Target: collapsed undecided row <= 140 px, first row top < 450 px, at least 4 rows and their buttons in the first 900 px.",
   "acceptance_test": "Playwright, sample case, 1440x900, scroll 0: the first entry's Accept button is inside the viewport and at least 4 `[data-testid^=entry-]` rows are fully visible; every collapsed undecided row is <= 140 px; at 390 a needs-review row is <= 420 px."
  },
  {
   "severity": "major",
   "title": "M3. A decided row still looks and acts undecided: Accept stays a filled primary button, the dismissed row stays in the list with Accept offered",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-37-after-accept.png, artifacts/review-evidence/T-060-pass2/ux2-39-after-dismiss.png, artifacts/review-evidence/T-060-pass2/ux2-59m-lib09-nr-row.png, artifacts/review-evidence/T-060-pass2/ux2-walk5-results.json. ux2-walk5-results.json after_accept_btns on an accepted needs-review row: Accept (36 px, rgb(9, 72, 168), enabled), Edit, Dismiss, Reset. After Dismiss the row keeps its strikethrough text, the 'Needs review' and 'Dismissed' chips and a full-colour blue Accept (ux2-39, ux2-59m at 390). `dismissed_section` is empty: there is no 'Dismissed (n)' group; a dismissed item stays in the main queue. Pass-1 F4 acceptance test ('exactly one primary per undecided row and none on a decided row') and F5 ('a dismissed row is not in the main list') are not met.",
   "why_it_matters": "The chips are now right (Needs review has a triangle, Accepted a check, Dismissed a circle-dash, separate from the machine state; ux2-37), so the state is readable. The controls disagree with it: a reviewer who accepted an item is still offered the primary button for the same decision, and ux2-walk5 shows the progress count does not change if it is clicked again. Undo exists and works (Reset: '1 of 20 decided' -> '0 of 20'), but the row presents Reset as a fourth ghost button, not as the way back.",
   "fix": "Decided rows: replace the filled Accept with a disabled 'Accepted' (check icon, `--ok` text) or hide it, keep Edit, and show 'Undo' as the text link beside the chip; set the summary to `--text-muted`. Dismissed rows: collapse under a 'Dismissed (n)' disclosure at the end of the queue with Reset. Keep one primary on undecided rows only.",
   "acceptance_test": "After Accept, the row has no filled primary button and exposes 'Undo' (one click returns '0 of N decided'); after Dismiss the row is no longer a child of `[data-testid=queue]` and appears under 'Dismissed (1)'."
  },
  {
   "severity": "minor",
   "title": "m1. Case labels and the library are still file slugs, and one developer term reaches every case",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-60-switcher-open.png, artifacts/review-evidence/T-060-pass2/ux2-walk8-results.json, artifacts/review-evidence/T-060-pass2/ux2-scan-results.json, artifacts/review-evidence/T-060-pass2/ux2-04-results-d.png. Header case name, tab title and case-list tiles read 'case lib01 er only then gap', 'case lib11 priors and ledger'; library tiles 'Add: L1 · er only then gap' (lowercase slug; app/backend/api.py:75 `meta.get(\"name\") or p.stem.replace(\"_\", \" \")`); four tiles are all 'Sample case' and differ only by time; library descriptions are cut mid-word by the server ('hedged chronic', 'plastic-surgery fo', ux2-60). The accuracy line printed above the first row of every case says 'on the fixture backend (recorded replies, 10 golden cases, small sample)' (fixture n=1 on all five library cases, ux2-scan-results.json). The 'Cases (n) and synthetic library' disclosure has no padding or chevron (ux2-01-landing-d.png). Processing shows 'Starting……' (input.js:97 label 'Starting…' plus input.js:91 appends '…').",
   "why_it_matters": "Pass-1 F8 is fixed for stage labels, 'ai translation', 'fixture miss', '(local mode)' and 'Step n of 8: judge_entries' (scan: zero matches for underscores, 'Step n of n:', 'local mode', 'How it was checked'). These remain.",
   "fix": "Add a `name` (title case) and a short `description` to every library manifest entry; derive case names from it; drop the 'Add:' prefix; clamp text in CSS only. Reword the accuracy line without 'fixture' ('Measured on 10 synthetic test cases: verified items matched the record 84 of 85 times'). Style the disclosure as a 40 px row with a chevron. Remove the trailing '…' when the label already ends in one.",
   "acceptance_test": "DOM scan of the five library cases: no match for /case lib/, /fixture/, /…{2,}/ or two tiles with the same label."
  },
  {
   "severity": "minor",
   "title": "m2. Charges table: reasons duplicated, column geometry differs between the two tables, 'Keep in notes' is a primary button",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-15-charges-panel.png, artifacts/review-evidence/T-060-pass2/ux2-55m-charges.png, artifacts/review-evidence/T-060-pass2/ux2-walk3-results.json, artifacts/review-evidence/T-060-pass2/ux2-82-lib06-charges.png. Fixed since pass 1: amounts right-aligned (amount_align right), class under the amount, 'Accept as noted' renamed 'Keep in notes', $185 rate in 'Unclear — not totaled (2)' with its reason, totals header clear. Still open: row heights 133, 133, 147, 147 px (pass-1 target <= 96); each unclear row prints two reasons ('Not counted: a rate, not a bill. rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review' and the amber box 'This figure is a rate, not a charge, so it is not added to the total.'); Status sits at x 778 in the first table and x 452 in the second; the amount cell of the damages row is the text 'missing 3 days of work'; 'Keep in notes' is a filled blue primary on an item that is explicitly not totaled; Accept / Dismiss / Audit stack in the Decision column with Audit off-axis (mobile: same, ux2-55m).",
   "why_it_matters": "The required content is right (this is why it is minor and not major: dossier check 5 is met). What is left is polish against the Carbon data-table bar: the number a paralegal checks should line up across the two tables, and a not-totaled row should not carry the primary colour.",
   "fix": "One shared `<colgroup>` for both tables (Amount 120 / Description 1fr / Class 112 / Status 150 / Actions 180); keep the amber sentence and drop the code reason from the status cell (or the reverse); make 'Keep in notes' secondary; put Accept and Dismiss on one line and Audit in the row menu.",
   "acceptance_test": "At 1440 the Status column's x is equal in the Detected and Unclear tables; an unclear row is <= 100 px; the page has no `.btn--primary` inside the Unclear table."
  },
  {
   "severity": "minor",
   "title": "m3. Row dates are ISO ('2026-01-09'); the letter, flags and records list use long dates",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-13-entry1.png, artifacts/review-evidence/T-060-pass2/ux2-walk3-results.json. ux2-walk3-results.json iso_dates: '2026-01-09', '2026-01-09', '2026-01-16', ... on all nine rows; gap-flag quote blocks show 'Date: 2026-03-06' under a sentence that says 'March 6, 2026'. The exported letter uses 'January 9, 2026' (ux2-44-export-after-accept-all.png). Pass-1 F20 open.",
   "why_it_matters": "The reviewer compares row, flag and letter; two formats force a mental conversion on every row.",
   "fix": "Format row dates with Intl.DateTimeFormat('en-US', {dateStyle:'medium'}) inside <time datetime>; keep the verbatim record date untouched in the record pane and quote blocks.",
   "acceptance_test": "No text node matching ^\\d{4}-\\d{2}-\\d{2}$ in `[data-testid=entry-date]`."
  },
  {
   "severity": "minor",
   "title": "m4. 'Open record' still opens a modal on top of the source pane that already shows the same record; the pane prints raw '=== Record 2 ===' markers",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-34-open-record.png, artifacts/review-evidence/T-060-pass2/ux2-39-after-dismiss.png, artifacts/review-evidence/T-060-pass2/ux2-walk5-results.json. ux2-walk5-results.json modal_open true after 'Open record' at 1440 while sbs-pane shows 'Record 2: ...' with the excerpt highlighted; pane body begins '=== Record 2 ===' / 'Date: 14/04/2026' / 'Source:' / 'Excerpt:'. Pass-1 F17: the overlap with the case list is fixed (pane is now a sticky column beside the list at >= 1024: position fixed, list 867 px at 1280, 624 px at 1024; static below 768).",
   "why_it_matters": "The record is the proof; it should open once, in the place already reserved for it.",
   "fix": "At >= 1024 px 'Open record' scrolls and highlights in the pane and moves focus there; the modal stays for narrow widths. Hide the '=== Record n ===' marker line in the pane header.",
   "acceptance_test": "At 1440 'Open record' opens no `<dialog>`; the pane's highlighted excerpt is in view."
  },
  {
   "severity": "minor",
   "title": "m5. Edit has no live check, original comparison or counter",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-35-edit-open.png, artifacts/review-evidence/T-060-pass2/ux2-36-edit-bad-number.png, artifacts/review-evidence/T-060-pass2/ux2-walk5-results.json. After typing ' Extra 99 mg.' into the summary textarea and waiting 1 s, nothing in the row reacts (ux2-36); label still reads 'Summary wording (the quoted excerpt, date and provider cannot be changed)'; the form sits below the action row. Pass-1 F25 open.",
   "why_it_matters": "Dossier check 8: edit in place, preserve the original, mark edited. Marking works; the preview does not exist, so an unsupported number is found only after Save.",
   "fix": "Debounced (400 ms) polite live line under the textarea ('Checking numbers and dates against the excerpt...' then the code reason); 'Original' as a muted line above the field; Cmd/Ctrl+Enter saves.",
   "acceptance_test": "Typing a number that is not in the excerpt shows the reason inside the row before Save is pressed."
  },
  {
   "severity": "minor",
   "title": "m6. 'Verified' chip has no icon and shares the blue of 'AI draft', the accent and the selected row; header and timeline disagree on 'need review'",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-13-entry1.png, artifacts/review-evidence/T-060-pass2/ux2-04-results-d.png. ux2-13: 'Verified' is blue outline text only; 'AI draft' is the same blue outline; Needs review has a triangle, Accepted a check, Dismissed a circle-dash, Could not verify a cross (ux2-80-lib11-tray.png). Header reads '0 of 23 decided · 3 need review' while the Timeline chips directly below read '0 need review · 9 verified' (ux2-04-results-d.png): the header counts flags and charges, the chip counts entries.",
   "why_it_matters": "Carbon requires a shape or icon per state so it survives grayscale (pass-1 F5); the machine state with the most trust weight is the one without one. Two 'need review' numbers on one screen cost trust.",
   "fix": "Verified: circle-check icon in `--ok`; 'AI draft' neutral (`--info` is fine but not the accent blue). Label the header count 'items'; label the Timeline chips 'entries needing review'.",
   "acceptance_test": "Under `filter: grayscale(1)` every state chip differs by an icon attribute as well as text; the header and the Timeline chip use different nouns or the same number."
  },
  {
   "severity": "minor",
   "title": "m7. Dates-to-confirm card and flag footers keep redundant controls",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-31-dates-to-confirm.png, artifacts/review-evidence/T-060-pass2/ux2-14-flags-panel.png. Dates card: radio choice with 'Suggested · DD/MM' and one primary 'Confirm date' (fixed since pass 1), but a disabled Accept / Edit row and 'Confirm the date first. Go to its date choices' remain below it. Flag cards: 'Dismiss' and 'Dismiss with reason…' sit side by side on every flag, plus 'Audit'; 'Edit note' sits next to 'Accept'.",
   "why_it_matters": "Pass-1 F22 and F14 partial. Two dismiss controls per flag; a link to controls 60 px above it.",
   "fix": "Hide Accept/Edit/Dismiss until the date is confirmed and drop the 'Go to its date choices' link; make 'Dismiss' open the reason field (one control), move Audit to the row menu.",
   "acceptance_test": "Before confirmation the card has exactly one button ('Confirm date') plus the text links; a flag card has one dismiss control."
  },
  {
   "severity": "minor",
   "title": "m8. Case-checks and AI-check panels: title baseline misaligned, text-link toggles with a tiny triangle, long text-only notice when export is blocked",
   "evidence": "artifacts/review-evidence/T-060-pass2/ux2-04-results-d.png, artifacts/review-evidence/T-060-pass2/ux2-42-export-first-click.png. 'How the AI was checked' sits about 8 px lower than 'checked 19, all agreed with the draft' on the same row; both panels use an underlined 'Show▾' link (the ▾ is a 0.7em glyph) instead of a chevron button; the red export-blocked box says 'The export is blocked. Nothing is accepted or edited yet, so the letter would be empty.' then 'Blocking the export (1): Whole case Nothing is accepted or edited yet, so the letter would be empty.' (same sentence twice) in the error colour for what is guidance. The stale-notice bug is fixed: after 'Accept all verified entries' it reads 'Nothing blocks the export now. Click Export again to open it.' (ux2-walk6-results.json after_acceptall_notice).",
   "why_it_matters": "Small craft misses on the panels that carry the product's trust story.",
   "fix": "One header row per panel (`display:flex; align-items:center`), a 16 px chevron button as the toggle, the blocker list rendered once, the notice in `--warn` not `--bad`.",
   "acceptance_test": "Panel title and summary share a baseline (bounding boxes within 2 px); the blocked message contains its reason once."
  },
  {
   "severity": "nit",
   "title": "n1. Type scale and small details",
   "evidence": "ux2-walk2-results.json census_d.fs: 14, 12, 16, 13, 20, 15 px (was 21 sizes); tokens.css:33-39 defines 12 / 13 / 14 / 15 / 16 / 20 / 24, five steps inside 4 px, so 13 and 15 are visually the same as 12/14 and 14/16. styles.css:84 and :137 use `font-size: 0.7em` for the triangle glyph; border-radius 2px on one element. Status icons are Unicode glyphs (✓ ▲ ✕ ⊖), not one icon set. At 390 the sticky banner plus header is 120 px (ux2-walk7-results.json sticky: 32 + 88), 14% of the screen; skip links are 40 px high and the Bates/Exhibit inputs 38 px.",
   "why_it_matters": "Not defects; they keep the type hierarchy shallow and the glyphs uneven in weight.",
   "fix": "Drop 13 and 15 from the scale (12 / 14 / 16 / 20 / 24) or give them one job each; replace glyphs with one 16 px SVG icon set; collapse the 390 header to one 48 px row.",
   "acceptance_test": "At most 5 distinct computed font sizes on the review page; every icon is an SVG with a data-icon attribute."
  }
 ],
 "whats_right": [
  "One token layer (tokens.css) read by every stylesheet, correct in light and dark, with hover and focus states",
  "Verbatim captioned quote in every row and record-labelled side-by-side evidence in every conflict and gap flag",
  "Skip link to the first needs-review item, auto-advance on accept, and Copy anyway naming the unreviewed item types"
 ],
 "questions_for_chris": [
  "Should the library manifest carry paralegal-facing titles (name field) so the case list stops showing file slugs, or is the slug display intentional for the demo?"
 ]
}
```
