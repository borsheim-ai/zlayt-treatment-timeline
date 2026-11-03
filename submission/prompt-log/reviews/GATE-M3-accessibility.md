# GATE-M3 accessibility review (WCAG 2.2 AA)

Reviewer: accessibility-reviewer (claude-sonnet-5-5). Date 2026-11-02. Review only; no product code changed.
Verdict: **pass**. 0 blockers, 0 majors, 9 minors, 6 nits. Every must-have action (accept, edit, dismiss, undo, count, export, copy, new case, rename, open case) is reachable and operable by keyboard alone, with no trap and visible focus. axe-core found 0 serious or critical violations in 50 scans. The minors are listed below with fixes.

## Scope and method

- Commit audited: `d0b04bc8274a10c8ae08fc55cd4f7693e17024b4` (`git rev-parse d0b04bc`), extracted with `git archive d0b04bc | tar -x` into a fresh scratchpad directory (not the working tree).
- Served on http://127.0.0.1:7931 (`ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, `ZLAYT_DB` in the scratchpad). Listener PID 52031 (`lsof -nP -t -iTCP:7931 -sTCP:LISTEN`), stopped by PID at the end of this run.
- axe-core 4.10.3, `axe.min.js` sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` (same file as passes 1 to 3). Tags: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice.
- Synthetic data only: the Appendix A sample (9 records, 23 items), library cases `case_lib11_priors_and_ledger` (ledger, Count this charge, unclear tray) and `case_lib06_lop_billed_vs_adjusted` (flagged-charge dialog, with the worker's own route stub), and a pasted copy of `evals/golden/sample.txt` typed by keyboard.
- Screen reader: not available. Announcements were checked by DOM inspection only (a MutationObserver on the live regions, `role`, text, node identity). I make no claim about what NVDA or VoiceOver say.
- Tab start point reset with `documentElement.focus()` before every walk (harness note).
- The tray in the brief is read as the "Unclear - not totaled" tray in Charges (`data-testid=unclear-tray`) and the could-not-verify tray; both exercised.
- Not exercised: the demo-mode refused-paste explanation (this server runs local mode, where a paste is accepted), 200% and 400% browser zoom (320 CSS px emulated by viewport instead), Windows forced-colors, PDF input, the excerpt editor and manual-entry forms.

## Deterministic checks first

Worker e2e files run from the `d0b04bc` copy against my server (`E2E_BASE_URL=http://127.0.0.1:7931`):

```
$ .venv/bin/python -m pytest tests/e2e/test_keyboard_mobile.py tests/e2e/test_polish_r3.py tests/e2e/test_count_charge.py -q -rs -p no:cacheprovider -x
..............................                                           [100%]
30 passed in 41.06s

$ .venv/bin/python -m pytest tests/e2e/test_mvp_finish.py tests/e2e/test_multicase.py -q -rf -p no:cacheprovider
FAILED tests/e2e/test_mvp_finish.py::test_a_paste_the_demo_does_not_run_is_explained_with_real_actions
FAILED tests/e2e/test_mvp_finish.py::test_the_refused_paste_offers_the_library_by_keyboard
FAILED tests/e2e/test_multicase.py::test_new_case_button_is_in_the_first_screen_and_puts_the_cursor_in_the_name_field
3 failed, 59 passed, 1 skipped in 150.41s (0:02:30)
```

The 3 failures are environment mismatches, not accessibility evidence: two test the demo-mode refused paste (my server is local mode) and one compares an aria snapshot of the overview with an empty case list (my DB held cases). I did not use them as evidence and did not investigate further. I tested the same behaviours by hand: New case moves focus to Case name (kb1/kb2 below).

## axe-core: 25 states x light and dark = 50 scans

`artifacts/review-evidence/GATE-M3-accessibility-audit-results.json`. Script `GATE-M3-accessibility-audit.py`.

States: overview empty, overview empty after Analyze with no text (error), overview with 2 cases, overview with a `status_error` row (route stub, as the worker's own e2e), case top, rename open, edit open, source dialog, row More open, Why dialog, audit drawer, Case checks and AI-check disclosures open, flags, charges, shortcut sheet, batch confirm, dismiss placeholder, export blocked, export, copy confirm (granted and not granted), Copy anyway blocked, side-by-side, lib11 charges with the unclear tray, Count this charge dialog. Each state was reached with fresh cases per theme so one theme's actions did not leak into the other.

- Serious or critical: **0** in all 50 scans.
- Violations: `page-has-heading-one` (moderate, best-practice) in 32 scans (every case-view state, both themes). Nothing else.
- Needs-review ("incomplete"): `color-contrast` in 26 scans (dialogs, empty states, charges). My own computed contrast found 0 failures in the same scans, so these are not contrast failures.
- Computed contrast (own script, same scans): 29,684 visible text nodes checked, 0 below threshold; 204 form-control boundaries checked, 0 below 3:1. Progress track border 4.30:1 light and 4.73:1 dark against the card (the track fill itself is 1.15:1, but a numeric "n of m" label sits next to every bar, so the bar is not the only carrier).
- The flagged-charge dialog (worker's route stub on lib06) scanned separately in both themes: 0 violations (`GATE-M3-accessibility-kb7.json`).

## Keyboard-only job (no mouse, no click calls)

Scripts `GATE-M3-accessibility-kb1..kb12.py`, JSON next to them. The whole job completed:

1. Overview: Tab from the top reaches Theme, New case, 3 filters, Search, Sort, each case link, Case name, Records textarea, Analyze, Upload (label ring), Use the sample case, Add a synthetic case. The filters expose `aria-pressed` (true/false).
2. New case by keyboard: Enter on New case puts focus in "Case name"; typed a name; Tab to the Records textarea (visible label); inserted the sample; Tab to Analyze; Enter. The run finished and the case opened. Progress was announced as "9 records found", "Starting...", "Drafting summaries (step 2 of 8)".
3. Case: first Tab is the skip link "Skip to the first item to review"; all four skip hrefs resolve; Enter moves focus to the item named by "Do this first".
4. Accept by Enter on a charge ("Keep in notes: $185") announces "Accepted: $185. 22 left to review." and moves focus to the next needs-review row.
5. Dismiss by Enter leaves an Undo placeholder ("Dismissed: Austin EMS run report, January 9, 2026 Undo"); the button is named "Undo dismissing Austin EMS run report, January 9, 2026" (visible "Undo" is inside the name). One Shift+Tab reaches it. When the six seconds end with focus on that Undo, focus moves to the next row, not to the page body. The item stays in the open Dismissed (1) group with its own Undo.
6. Edit: Enter opens the textarea with focus; Tab runs Save and accept, Save, Cancel, Open record; Escape closes. No trap. Save announces "Saved edit to: ...". Undo on an edited item asks first (`role=group` "Confirm undo", Keep focused, Escape returns to Undo).
7. Rename: Rename this case, Enter, input named "Case name", Save returns focus to Rename. An empty name shows "Type a name for the case." as `role=alert` with focus kept in the input.
8. Section nav: `<nav aria-label="Sections of this case">`, buttons "Timeline, 9 items open" etc., `aria-current="location"` on the current one. It is `visibility: hidden` and 0 px tall at scrollY 0 (so it is not in the Tab walk from the top) and appears, tabbable, once scrolled (Tab from the header Export reaches "Overview"). Enter on Flags moves focus to the Flags heading with a 2 px ring; Enter on Export lands on "Why the export is blocked" or the Export heading.
9. Count this charge (lib11): 3 buttons named "Count this charge: $250.00", "...: $180.00", "...: $2,310.00" (visible "Count this charge" inside each). Enter opens a modal dialog labelled "Count this charge?" with focus on Cancel; Tab cycles Confirm, Cancel (browser chrome between, as with any showModal); Escape returns focus to the button; the named confirm ("I checked this is a separate charge for a service: count $250.00") announces "Counted $250.00 as a separate charge. Accepted charges now $250.00." and focus lands on the row. The flagged-charge dialog behaves the same ("Count this flagged charge?", Cancel first, "Accepted: $2,880. 18 left to review.").
10. Export: Enter on Export puts focus on the Export heading with a 2 px ring (pass-3 nit P3-4 is fixed); the next Tab is "Back to review", then the letter-style radios, then Copy letter. Copy letter with unreviewed items shows `role=alert` text and focus moves to "Copy anyway"; Enter there copies, focus returns to Copy letter, `role=status` says "Copied the treatment section." and the clipboard holds "TREATMENT CHRONOLOGY". Back to review returns focus to the first entry. All cases returns to the overview with focus on the first case link; Enter on a case link opens it with focus on the case heading.
11. Dialogs (shortcut sheet, source record, Why, batch confirm by Shift+A, count, flagged charge): modal, labelled, Escape returns focus to the opener, no trap.

## Focus order and visible focus

`GATE-M3-accessibility-walk.json`, script `GATE-M3-accessibility-walk.py`. One full Tab cycle from the top of lib11 (12 flags, 8 amounts):

| Run | Stops | Entirely hidden (SC 2.4.11) | Partly hidden | No indicator | Unnamed | Min ring contrast |
|---|---|---|---|---|---|---|
| light 1280 | 213 | 0 | 0 | 0 | 0 | 5.51:1 |
| dark 1280 | 213 | 0 | 0 | 0 | 0 | 6.85:1 |
| light 320 | 205 | 0 | 1 ("Records differ on a fact", 6 of 9 sample points visible) | 0 | 0 | 5.55:1 |
| overview 1280 | 28 | 0 (the visually hidden file input; the "Upload .txt" label draws the ring: solid 2px rgb(11, 87, 208)) | 0 | 0 | 0 | 6.39:1 |

All rings are 2 px solid. The tab order follows the visual order.

## 320 CSS px reflow and target size

`GATE-M3-accessibility-reflow.json`, script `GATE-M3-accessibility-reflow.py`. At 320, 375 and 1280 across overview, case top (Case checks and AI-check disclosures opened first), row More open, edit, scrolled with the section nav showing, flags, charges, source dialog, export, lib11 charges and the Count dialog: `scrollWidth` equals the viewport in every state (no two-dimensional scroll). Visible controls checked 26 to 279 per state: 0 below 24 x 24 CSS px at 320, 375 and 1280. Two clipped items at 320 are listed as findings R-1 and R-2.

## Pass-3 items on this build

| Pass-3 id | Status now | Evidence |
|---|---|---|
| P3-1 More/Less name | fixed in substance | collapsed name "More actions: Austin EMS run report, January 9, 2026" contains the visible "More"; expanded "Less actions: ..." contains "Less" (`GATE-M3-accessibility-prior.json`). The name still changes with state (nit N-1) |
| P3-2 timeline `aria-labelledby` with no role | fixed | container is `role="group"` with `aria-labelledby="h-timeline"`; no `aria-prohibited-attr` in any of the 50 scans |
| N-8 Export-view skip hrefs | fixed | axe `skip-link` absent in export, copy-confirm and copy-blocked scans, both themes |
| P3-4 Export heading focus ring | fixed | ring 2 px solid on the heading |
| N-9 row Tab model | open (minor, F-1) | 9 of 9 rows `tabindex=0`; 213 stops |
| P3-5 decided Accept `aria-pressed` | open (nit N-2) | decided Accept: `aria-pressed="true"`, name "Accepted: ..." |
| N-12 two polite regions | open (nit N-3) | "Accepted: $185. 22 left to review." and "1 of 23 decided" both change |
| N-14 twelve "Technical details" | open (nit N-4) | `tech_details` count 12 |

## Findings

### Minor

**F-1 (carried N-9). Each timeline row is a Tab stop and holds 8 buttons.** One lib11 walk is 213 stops; a dismiss on a charge in the tray took 134 Tab presses from the entry above it (`GATE-M3-accessibility-kb3.json`). All actions stay reachable and the skip links and "Do this first" shortcut reduce the cost, hence minor.

**F-2. The case page has no level-one heading.** axe `page-has-heading-one` (moderate) in 32 of 50 scans. `h1.brand` "Treatment timeline" has `display: none` in the case view; the case name is a `<span>` (`h1_case`: `['Treatment timeline', 'none', 0]`, `case_name_markup`: SPAN). SC 1.3.1 and 2.4.6.

**F-3. The section nav "Overview" button shows "Top" under about 480 px but is named "Overview".** At 480, 375 and 320 px the visible text is "Top" and `aria-label` is "Overview" (`nav_overview_label_480`: `['Top', 'Overview', ...]`). SC 2.5.3 Label in Name (Level A): a voice-control user saying "click Top" gets nothing.

**F-4. The overview's j and k keys act when nothing has focus.** With focus on BODY, `j` moved focus to the first case link (`GATE-M3-accessibility-keys.json` `j_from_body` -> `('a','Sample case','cases-open')`). From a header button, a filter, the sort select and the search box they do nothing, so the gating is partial. In the case view the same keys do nothing from BODY (`GATE-M3-accessibility-keys2.json`, 11 keys, 0 changes). SC 2.1.4 and checklist item 8 want a shortcut active only when its component has focus, or a way to turn it off. Impact is small (focus moves; nothing is changed or opened), so minor; this is the one a stricter reader could call major.

**F-5. "Try again" on a status-error case row drops focus to the page.** Enter on `cases-status-retry` repainted the row; `document.activeElement` became BODY (`GATE-M3-accessibility-kb10.json` `after_retry_focus`). The whole-list "Try again" (`cases-retry`) moves focus to the Cases heading, so the two retries disagree. The announcement is only "Showing 14 of 14 cases". The button is named just "Try again" with no case name (`retry_name`: `[None, 'Try again', None]`). SC 2.4.3 and 4.1.2.

**F-6. A step-complete message overwrites "Dismissed: ..." 8 ms later in the same polite region.** Dismissing the last needs-review amount: `rv-live` text went '' (t=1933), "Dismissed: missing 3 days of work. 21 left to review." (t=1955), "Unclear amounts done. Next: Timeline, Austin EMS run report, January 9, 2026. 21 items are still open." (t=1963) (`GATE-M3-accessibility-kb4.json`). A screen reader may speak only the last message, so the user may not hear what was dismissed. DOM only; not checked in a screen reader. SC 4.1.3.

**F-7. At 320 px the Theme and Shortcuts controls are removed.** `display: none` at 640 px and below (`nav_overview_label_640`: Theme 'none', Shortcuts 'none'; `probe320`: both display none). A keyboard user at 400% zoom (320 CSS px) cannot open the shortcut sheet or switch theme; the review actions themselves are unaffected. SC 1.4.10 asks for no loss of functionality.

**F-8. At 320 px the case name is cut to "Sam..." / "Prior..." and the full name is not on screen.** `case-name` scrollWidth exceeds clientWidth at 320 (`nav_overview_label_320` last value true); the case heading is "Case overview" and carries the name only in its `aria-label`; the full name is only in a `title` tooltip (`case_name_markup`: title 'Sample case'). SC 1.4.10 (information loss). Screenshot `GATE-M3-accessibility-320-top.png`.

**F-9. The section nav clips its Export tab at 320 px with two-digit counts.** lib11: `button[nav-export] l=290 r=343` in a 320 px viewport; the strip scrolls sideways (`GATE-M3-accessibility-reflow.json`, `reflow lib11-charges|320`; screenshot `GATE-M3-accessibility-reflow-charges-320.png` shows "Exp"). Export is also in the header and the skip links, and keyboard focus scrolls the strip, so this is minor.

### Nit

**N-1.** The More toggle's name changes with state ("More actions: X" / "Less actions: X"). `aria-expanded` already carries the state; "Less actions" reads oddly.
**N-2 (carried P3-5).** A decided Accept keeps `aria-pressed="true"` while a second press does nothing.
**N-3 (carried N-12).** Two polite regions update on each decision (`rv-live` and `progress-text`).
**N-4 (carried N-14).** Twelve "Technical details" summaries share one name.
**N-5.** After Analyze finishes, focus goes to `nav#skip-nav` ("Skip links"), which has `outline: none` and 0 of 9 visible sample points (`GATE-M3-accessibility-kb2.json` step C; kb10 `focus_after_run`). A sighted keyboard user sees no focus until the next Tab.
**N-6.** Rename's empty-name error is `role=alert` but the input has no `aria-describedby` or `aria-invalid` (`rename_empty_error`). Also, during a case load the polite region repeats "Loading the case checks..." four times and "Loading the AI checks..." three times, and the first run message reads "Starting......" (`kb10 run_live_history`).

## Checks that passed

- Keyboard operability of every action in the journey; modal dialogs close with Escape and return focus; no trap anywhere (checklist 1, 2).
- Focus ring: 2 px solid everywhere, at least 5.51:1 (checklist 4); no focus entirely hidden by the sticky banner, header or nav at 1280 or 320 (checklist 5).
- Accept, dismiss, undo, count, edit, copy and batch each announce through `role=status` or `role=alert` (checklist 11); decided rows expose state by text and `aria-pressed` (checklist 10, 15).
- Names: New case ("New case"), Count this charge ("Count this charge: $250.00"), section nav ("Flags, 10 items open"), Undo placeholders ("Undo dismissing ..."), Try again ("Try again"), Rename ("Rename this case"), all dialogs labelled. Roles: filters are toggle buttons, the nav is `<nav>`, dialogs are modal `<dialog>`, `aria-current="location"` on the active section.
- Light and dark contrast, target size, 320 px reflow (apart from F-7 to F-9), reduced-motion not re-tested this gate.

## What is right

- Undo placeholders are real buttons with item-specific names, keep focus through a repaint, and fall back to the next row, never the page body, when they expire.
- Every modal dialog is labelled, opens on its safe answer, and returns focus to its opener on Escape; the Count and flagged-charge dialogs announce the result.
- Contrast, ring, target-size and reflow numbers held across 50 axe scans, 213-stop walks and 3 widths with the new overview, section nav and tray.

## Questions for Chris

- Should the overview's j and k keys also require focus inside the case list (F-4), or is body-level j/k on the overview intended?

```json
{"card": "GATE-M3", "persona": "accessibility-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git d0b04bc8274a10c8ae08fc55cd4f7693e17024b4 via git archive into the scratchpad (not the working tree); app http://127.0.0.1:7931 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated, DB in scratchpad); synthetic sample case (9 records, 23 items), library cases lib11 and lib06 (flagged-charge dialog via the worker's route stub); overview, case, tray, dialogs, export, section nav, Undo placeholders, Try again; demo-mode refused paste not exercised",
 "exercised": [
  "git rev-parse d0b04bc -> d0b04bc8274a10c8ae08fc55cd4f7693e17024b4; git archive d0b04bc | tar -x into a fresh scratchpad dir; server started with env -i ... ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated HOST=127.0.0.1 PORT=7931, listener PID 52031",
  "pytest tests/e2e/test_keyboard_mobile.py test_polish_r3.py test_count_charge.py against my server: 30 passed in 41.06s; test_mvp_finish.py + test_multicase.py: 59 passed, 3 failed, 1 skipped (the 3 failures are demo-mode and empty-DB environment mismatches with my local-mode populated server, not used as evidence)",
  "axe-core 4.10.3 (sha256 880970c0...) with wcag2a/aa/21a/21aa/22aa + best-practice on 25 states x light and dark = 50 scans (overview empty, empty error, overview with cases, status_error row stub, case top, rename, edit, source dialog, row More, Why dialog, audit drawer, disclosures open, flags, charges, shortcut sheet, batch confirm, dismiss placeholder, export blocked, export, copy confirm, Copy anyway blocked, side-by-side, lib11 charges + tray, Count dialog): 0 serious or critical; page-has-heading-one moderate in 32 scans (artifacts/review-evidence/GATE-M3-accessibility-audit-results.json)",
  "flagged-charge confirm dialog (lib06 with the worker's route stub) axe light and dark: 0 violations, keyboard path Accept -> Cancel focused -> Tab -> Confirm -> 'Accepted: $2,880. 18 left to review.' (GATE-M3-accessibility-kb7.json)",
  "computed contrast over 29,684 visible text nodes and 204 control boundaries in the 50 scans: 0 failing; progress track border 4.30 light and 4.73 dark (GATE-M3-accessibility-audit-results.json, GATE-M3-accessibility-prior.json)",
  "keyboard-only job: overview Tab walk, New case (focus to Case name), typed name and pasted sample by keyboard, Analyze by Enter, skip link, Accept, Dismiss, Undo placeholder (Shift+Tab to Undo, expiry while focused), Edit and Escape, Rename (save, empty error, Escape), section nav (hidden at scrollY 0, tabbable when scrolled; Enter and Space), Count this charge dialog, Export, Back to review, Copy letter, Copy anyway, All cases, open a case row (GATE-M3-accessibility-kb1..kb12.json)",
  "dialogs by keyboard: shortcut sheet, source record, Why, batch confirm (Shift+A), Count this charge, flagged charge, Undo-on-edited discard confirm: labelled, modal, Escape returns focus, no trap (kb6, kb7, kb12)",
  "full Tab walk from the top, lib11: 213 stops light 1280, 213 dark 1280, 205 light 320, 28 on the overview; 0 entirely hidden, 1 partly hidden at 320, min ring contrast 5.51 light and 6.85 dark, all 2 px solid (GATE-M3-accessibility-walk.json)",
  "320, 375 and 1280 px reflow and target size across overview, case top with disclosures open, row More, edit, scrolled nav, flags, charges, source dialog, export, lib11 charges and Count dialog: scrollWidth equals viewport everywhere, 0 controls under 24x24 (GATE-M3-accessibility-reflow.json)",
  "single-key shortcuts: overview j/k from body, header button, filter, sort, search, row link; case-view letters from BODY, nav, theme, all cases, rename, export (GATE-M3-accessibility-keys.json, keys2.json)",
  "live-region DOM history with a MutationObserver: Accept, Dismiss, last-in-step dismiss (two messages 8 ms apart), Count, flagged confirm, Copy letter/Copy anyway, run progress, status-error retry, load-error retry (kb2, kb4, kb6, kb9, kb10, kb11)",
  "names and states of the new controls: New case, Count this charge, section nav buttons and aria-current, Undo placeholders, Try again (row and list), filter aria-pressed, Rename input, More/Less toggles, decided Accept aria-pressed, timeline container role (kb1, kb3, kb5, kb6, prior.json)",
  "section nav label-in-name at 1280, 900, 640, 480, 375, 320 px and header Theme/Shortcuts display at each width (keys.json); h1 presence (keys.json h1_case)"],
 "verdict": "pass",
 "scores": {"keyboard_operability": 4, "focus_order_and_visibility": 5, "names_roles_states": 4, "status_announcements": 4, "contrast_light": 5, "contrast_dark": 5, "target_size": 5, "reflow_320": 4, "landmarks_headings": 3, "axe_serious_critical": 5},
 "findings": [
  {"severity": "minor", "title": "F-1 (carried N-9): each timeline row is a Tab stop followed by 8 buttons; 213 stops per page",
   "evidence": "GATE-M3-accessibility-walk.json lib11|light|1280 stops=213; prior.json row_tabindex [9, 9]; kb3.json 'tabs to tray Dismiss' 134 presses from the entry above",
   "why_it_matters": "APG composite pattern: a row that is both a stop and a container of stops gives a mixed model and a long walk. Every action stays reachable, and the skip links and Do this first shortcut cut the cost.",
   "fix": "Choose one model: roving tabindex across the rows with j and k as the arrows, or no row tab stop (buttons only).",
   "acceptance_test": "One documented Tab model; the Tab count from the first row to Export drops from the current value and every action stays reachable."},
  {"severity": "minor", "title": "F-2: the case page has no level-one heading (axe page-has-heading-one, 32 of 50 scans)",
   "evidence": "GATE-M3-accessibility-audit-results.json 10-case-top|light violations page-has-heading-one moderate, targets ['html']; keys.json h1_case [['Treatment timeline', 'none', 0, False]]; case_name_markup ['SPAN', 'Sample case', 'Sample case']",
   "why_it_matters": "SC 1.3.1 and 2.4.6: heading navigation in the case view starts at h2, and nothing names the page or the case as the top heading.",
   "fix": "Keep the h1 in the case view (visually hidden if the brand is hidden) or make the case name the h1.",
   "acceptance_test": "axe page-has-heading-one reports 0 in every case-view state; exactly one visible-to-AT h1 per view."},
  {"severity": "minor", "title": "F-3: section nav Overview button shows 'Top' under about 480 px but is named 'Overview' (SC 2.5.3)",
   "evidence": "GATE-M3-accessibility-keys.json nav_overview_label_480 ['Top', 'Overview', 'none', 'none', False]; the same at 375 and 320; nav-short span is aria-hidden in the markup",
   "why_it_matters": "Label in Name is Level A: voice control users say the visible word 'Top' and the button has no such name.",
   "fix": "Make the accessible name contain the visible text at every width (for example aria-label 'Top, Overview' or show 'Overview' and drop the short form).",
   "acceptance_test": "At 320, 375 and 1280 px, the accessible name of nav-overview contains its visible text."},
  {"severity": "minor", "title": "F-4: the overview's j and k keys act with nothing focused (SC 2.1.4)",
   "evidence": "GATE-M3-accessibility-keys.json j_from_body ('a', 'Sample case', 'cases-open'); j_from_new_case_btn, k_from_filter, j_from_sort, j_from_theme: no change; keys2.json: case view from BODY, 11 keys, 0 changes",
   "why_it_matters": "A single-character shortcut must be off-able, remappable or active only when its component has focus. j/k only move focus (no data change, no dialog), so this is minor, but it is the same class as pass-1 B1 and a stricter reader could rate it higher.",
   "fix": "Act on j/k only when focus is inside the case list, as the case view already does for item rows; or add a Keys on/off control.",
   "acceptance_test": "On the overview with focus on BODY, j and k change nothing; with focus on a case link they move to the next or previous link."},
  {"severity": "minor", "title": "F-5: Try again on a status-error row drops focus to the page, and its name does not say which case",
   "evidence": "GATE-M3-accessibility-kb10.json after_retry_focus {'tag': 'BODY'}; retry_name [None, 'Try again', None]; retry_live [['cases-count','status','Showing 14 of 14 cases']]. The list-level retry moves focus to the Cases heading (after_load_retry_focus h2 'Cases').",
   "why_it_matters": "SC 2.4.3: activating the control removes it and focus goes to the document. SC 4.1.2: two rows in error would expose two identical 'Try again' buttons.",
   "fix": "After the repaint, focus the retried row's link or its next control; name the button 'Try again: <case name>'.",
   "acceptance_test": "Enter on the row's Try again leaves focus on a control in that row or on the list; the button name includes the case name."},
  {"severity": "minor", "title": "F-6: the step-complete announcement replaces 'Dismissed: ...' within 8 ms in the same polite region",
   "evidence": "GATE-M3-accessibility-kb4.json live history: [1933, ''], [1955, 'Dismissed: missing 3 days of work. 21 left to review.'], [1963, 'Unclear amounts done. Next: Timeline, Austin EMS run report, January 9, 2026. 21 items are still open.']. DOM only; no screen reader.",
   "why_it_matters": "SC 4.1.3: a screen reader may speak only the last message, so the user may not hear what was dismissed.",
   "fix": "Write one combined message ('Dismissed: X. Unclear amounts done. Next: ...') or delay the second message until the first has been spoken.",
   "acceptance_test": "Dismissing the last needs-review item of a step produces one rv-live update that names the dismissed item and the next step."},
  {"severity": "minor", "title": "F-7: Theme and Shortcuts controls are removed at 640 px and below (loss of functionality at 320 px)",
   "evidence": "GATE-M3-accessibility-keys.json nav_overview_label_640 ['Overview','Overview','none','none',False] (columns 3 and 4 are Theme and Shortcuts display); probe320 output: btn-theme display none, btn-shortcuts display none; Tab walk at 320 has no Theme or Shortcuts stop (kb5.json w320 tab_walk_top)",
   "why_it_matters": "SC 1.4.10 expects content and functionality to survive reflow. A keyboard user at 400% zoom (320 CSS px) cannot open the shortcut sheet or change the theme. The review actions themselves are unaffected.",
   "fix": "Move both into an overflow menu or the Records disclosure at narrow widths instead of display: none.",
   "acceptance_test": "At 320 px, Theme and Shortcuts are reachable by Tab and operable."},
  {"severity": "minor", "title": "F-8: the case name is truncated at 320 px and the full name is not otherwise on screen",
   "evidence": "GATE-M3-accessibility-keys.json nav_overview_label_320 last value true (case-name scrollWidth > clientWidth); case_name_markup title 'Sample case'; screenshot artifacts/review-evidence/GATE-M3-accessibility-320-top.png shows 'Sam...'; reflow-charges-320.png shows 'Prior...'",
   "why_it_matters": "SC 1.4.10 information loss: a title attribute is not available to touch or keyboard users, and the heading 'Case overview' carries the name only in its aria-label.",
   "fix": "Let the name wrap on its own line at narrow widths, or show it in the case overview heading.",
   "acceptance_test": "At 320 px a 34-character case name is fully readable without hover."},
  {"severity": "minor", "title": "F-9: the section nav strip clips its Export tab at 320 px when counts are two digits",
   "evidence": "GATE-M3-accessibility-reflow.json reflow lib11-charges|320 offenders ['button[nav-export] l=290 r=343']; screenshot GATE-M3-accessibility-reflow-charges-320.png shows 'Exp' cut off; scrollWidth stays 320 because the strip scrolls inside itself",
   "why_it_matters": "SC 1.4.10: a sideways-scrolling strip is a second scroll direction. Export is also in the header and the skip links, and focus scrolls the strip, so minor.",
   "fix": "Wrap the nav at narrow widths, or shorten the labels so five tabs fit in 320 px.",
   "acceptance_test": "At 320 px with lib11 counts, all five nav buttons lie inside the viewport."},
  {"severity": "nit", "title": "N-1: the More toggle's name changes with its state ('More actions: X' / 'Less actions: X')",
   "evidence": "GATE-M3-accessibility-prior.json toggle_collapsed and toggle_expanded: ['entry-toggle','More actions: Austin EMS run report, January 9, 2026','More','false'] then 'Less actions: ...','Less','true'",
   "why_it_matters": "aria-expanded already carries the state; 'Less actions' reads oddly. The visible text is now inside the name, so SC 2.5.3 passes.",
   "fix": "Use one stable name such as 'More actions: X' with aria-expanded as the only state signal.",
   "acceptance_test": "The toggle's accessible name is identical collapsed and expanded."},
  {"severity": "nit", "title": "N-2 (carried P3-5): a decided Accept keeps aria-pressed='true' while a second press does nothing",
   "evidence": "GATE-M3-accessibility-prior.json decided_accept ['true', 'Accepted: Austin EMS run report, 2026-01-09', 'Accepted', 'Undo: Austin EMS run report, 2026-01-09']",
   "why_it_matters": "aria-pressed means a toggle; the way back is the separate Undo button.",
   "fix": "Drop aria-pressed on a decided Accept or make it a real toggle.",
   "acceptance_test": "A decided Accept has no aria-pressed or pressing it changes the value."},
  {"severity": "nit", "title": "N-3 (carried N-12): two polite regions change on each decision",
   "evidence": "GATE-M3-accessibility-kb2.json E2: rv-live 'Accepted: $185. 22 left to review.' and progress-text '1 of 23 decided · 2 to review' both role=status",
   "why_it_matters": "A screen reader may read both for one action.",
   "fix": "Keep one polite announcement per decision.",
   "acceptance_test": "One decision, one polite announcement."},
  {"severity": "nit", "title": "N-4 (carried N-14): twelve 'Technical details' summaries share one name",
   "evidence": "GATE-M3-accessibility-prior.json tech_details {'Technical details': 12, ...}",
   "why_it_matters": "SC 2.4.6 weak; each sits under its item.",
   "fix": "Name each with its item, or leave.",
   "acceptance_test": "Optional."},
  {"severity": "nit", "title": "N-5: after Analyze finishes, focus is on the invisible 'Skip links' nav with no focus indicator",
   "evidence": "GATE-M3-accessibility-kb2.json step C: tag nav, name 'Skip links', outlineStyle none, visible_points 0 (covered by #banner-synthetic); kb10.json focus_after_run: same",
   "why_it_matters": "The next Tab lands on the first skip link, which is the intent, but a sighted keyboard user sees no focus until then (SC 2.4.7 on a programmatic target).",
   "fix": "Move focus to the visible case heading, or show the skip links while the nav has focus.",
   "acceptance_test": "After Analyze, the focused element shows a 2 px ring or the skip links are visible."},
  {"severity": "nit", "title": "N-6: rename empty-name error is not tied to the input; run messages repeat and one reads 'Starting......'",
   "evidence": "GATE-M3-accessibility-kb9.json rename_empty_error {'text': 'Type a name for the case.', 'role': 'alert', 'inputDescribedby': None, 'invalid': None}; kb10.json run_live_history: 'Loading the case checks…' x4, 'Loading the AI checks…' x3, 'Starting……'",
   "why_it_matters": "SC 3.3.1 association is by role=alert and kept focus only; repeated polite text may be spoken more than once.",
   "fix": "Add aria-describedby and aria-invalid on the rename input; update the loading message once; fix the double ellipsis.",
   "acceptance_test": "The input references the error id; one loading message per phase."}
 ],
 "whats_right": [
  "Undo placeholders are real buttons named for their item, keep focus through a repaint, and fall back to the next row when they expire, never to the page body.",
  "Every modal dialog is labelled, opens on its safe answer and returns focus to its opener on Escape; the Count and flagged-charge dialogs announce the result.",
  "Contrast, focus ring, target size and 320 px reflow held across 50 axe scans (0 serious or critical), 213-stop walks and three widths with the new overview, section nav and unclear tray."
 ],
 "questions_for_chris": [
  "Should the overview's j and k keys also require focus inside the case list (F-4), or is body-level j/k on the overview intended?"
 ]}
```
