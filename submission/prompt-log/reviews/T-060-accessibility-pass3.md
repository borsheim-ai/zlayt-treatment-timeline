# T-060 pass 3: accessibility review (WCAG 2.2 AA)

Reviewer: accessibility-reviewer (model claude-haiku-5-5, as run). Date 2026-11-02. Review only; no product code changed.
Verdict: **pass**. No blockers, no majors. All four pass-2 majors are fixed. Four minors and seven nits remain (listed below).

## Summary

All four pass-2 majors are fixed and verified in the running build: the shortcut sheet prints its keys, the 320 CSS px reflow holds with Case checks and the AI-check panel both open, the theme toggle name follows the visible state, and the Upload control shows a focus ring that opens the file chooser on Enter and Space.

Pass-2 N-8 (skip-link targets) is partial: the queue views are fixed, but in the Export and copy views three of the four skip links point at elements that are not rendered. Pass-2 N-9 (timeline rows as Tab stops) is still open. Two new minors: the entry More/Less control's name omits its visible text and changes with state, and the timeline container carries an `aria-labelledby` with no role. Two new nits: the Export heading has no visible focus indicator, and a decided Accept keeps `aria-pressed="true"` while a second press does nothing.

Screen reader: not available. Announcements were checked by DOM inspection only (`role`, `aria-live`, text and node identity before and after each action).

## Scope and method

- Commit audited: `e1ce8dc620e6ec0778320456ac79a25f1832bfee` (HEAD), extracted with `git archive` into the scratchpad. `git log b89b9d9..HEAD -- app/frontend` lists c8e36fb, 5d975ed and 7d5a45f as the only frontend commits since pass 2, so the audited frontend is the one from 7d5a45f. d9efc5c is the test commit. e1ce8dc and the two commits before it (f8f358e, 1b93582) are backend. Uncommitted edits in the working tree (`app/backend/api.py`, `app/backend/pipeline.py`, board and memory files) were not audited.
- Served on http://127.0.0.1:7895 (`ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, DB in the scratchpad). Listener PID 49599, stopped at the end of this run.
- axe-core 4.10.3 from `npm pack axe-core@4.10.3`; `axe.min.js` sha256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb (same file as passes 1 and 2). Tags: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice.
- Synthetic sample only (`evals/golden` sample, 9 records, 23 queue items).
- Tab start point reset with `documentElement.focus()` (pass-2 harness note).

## Deterministic check first

`tests/e2e/test_polish_r3.py` run from the HEAD copy against this server (`E2E_BASE_URL=http://127.0.0.1:7895`):

```
$ .venv/bin/python -m pytest tests/e2e/test_polish_r3.py -q -rs -p no:cacheprovider
..................                                                       [100%]
18 passed in 23.25s
```

Coverage gap in that file: the skip-link href test (`test_skip_link_hrefs_resolve_to_elements`) runs in the queue view only, so it does not catch the Export-view finding N-8 below. The file-input test checks only that the label has an outline after focus; it does not check contrast or that Enter opens the chooser.

## Pass-2 status

| Pass-2 id | Sev (pass 2) | Status | Evidence (this pass) |
|---|---|---|---|
| N-1 shortcut sheet prints `[object HTMLElement]` | major | **fixed** | `review.js:301` now `KEYS.flatMap(...)`. Sheet: 9 `kbd`, 9 `dt`, 9 `dd`, no "[object" (`T-060-accessibility-pass3-details.json`: `sheet_has_object_html_text` false, `sheet_kbd_count` 9). axe `10-shortcuts-sheet` has no `definition-list` in light or dark. |
| N-2 320 px reflow with Case checks open | major | **fixed** | `styles.css:250` `.zs-chip { white-space: normal; max-width: 100% }`. With Case checks open, `scrollWidth` 320 (`T-060-accessibility-pass3-reflow-probe.json`). With Case checks and "How the AI was checked" both open, 320 px, `scrollWidth` 320 and 0 chips past the edge in queue, edit, flags, charges, Export and the source dialog (`T-060-accessibility-pass3-extra.json` `b_reflow320_*`, 42 visible chips each). |
| N-3 theme toggle name stale | major | **fixed** | `app.js:40` sets `aria-label` on every change. Keyboard: after 1 press "Theme: light. Press to change it."; after 2, "Theme: dark. Press to change it."; after 3, "Theme: auto. Press to change it." (`T-060-accessibility-pass3-names.json` `theme_three_presses`; `T-060-accessibility-pass3-keyboard-results.json` `k_theme_name_after_*`). |
| N-4 Upload control: 1x1 clipped focus stop | major | **fixed** | `styles.css:248` `label.btn:has(+ #file:focus-visible)` draws a 2 px ring. At 3x zoom the ring is visible around "Upload .txt" (`T-060-accessibility-pass3-file-ring-zoom.png`); computed `solid 2px rgb(11, 87, 208)`, 6.39:1 against the label background. Enter and Space each open a file chooser (`T-060-accessibility-pass3-file-ring-zoom.json`). |
| N-5 "Why this status" buttons share a name | minor | **fixed** | `stepper.js:466` names each button with its item. 23 visible buttons, 23 unique names (`T-060-accessibility-pass3-details.json` `why_status_buttons`). |
| N-6 dismiss-with-reason has no `aria-controls` | minor | **fixed** | `review.js:240` `aria-controls` = `dr-f_gap_r6_r7`, and the input has that id (`j_dismiss_reason_attrs_after`, `j_dismiss_reason_input_labelled`). |
| N-7 `landmark-unique` on the side-by-side pane | minor | **fixed** | axe `landmark-unique` absent in all 36 scans. |
| N-8 skip-link targets | minor | **partial** | Queue views: all four `#skip-nav` hrefs resolve (`skip_targets_exist` true) and axe `skip-link` passes. Export and copy views (audit states 14 to 16, light and dark): `#skip-to-review`, `#skip-to-flags` and `#skip-to-charges` do not exist, so axe `skip-link` (moderate, 3 nodes, "No skip link target") in 6 scans. Activation still works through `onclick` (`T-060-accessibility-pass3-extra.json` `a_export_view_skip`). See finding P3-3 below, folded into N-8. |
| N-9 each timeline row is a Tab stop and also holds buttons | minor | **open** | `review.js:358` still sets `tabindex="0"` on the row. At 1280 px light the walk has 19 row stops, each followed by 8 buttons (Accept, Edit, Dismiss, Why, Open record, Audit, Change quote, More). `walk_1280_names|light`. |
| N-10 edit textarea name drops the visible rule | minor | **fixed** | No `aria-label` on the textarea. Accessible name = "Summary wording (the quoted excerpt, date and provider cannot be changed)". Refused edit: `aria-describedby` = `rv-err-e2`, role=alert, visible (`T-060-accessibility-pass3-details.json` `edit_label_chain`, `refused_describedby_target`). |
| N-11 focus after Accept goes to Flags | nit | open, unchanged | Accept e1 by Enter moves focus to `flag-f_r7_1` "Accident date source". Announcement unchanged. Product question. |
| N-12 two polite regions per decision | nit | open | Accept e1: `rv-live` ("Accepted: Austin EMS run report, 2026-01-09. 22 left to review.") and `progress-text` (role=status, "1 of 23 decided") both change (`j_accept_e1.live_after`). |
| N-13 two stops partly under the sticky header at 320 px | nit | open | `walk_320|light` `partly_hidden_by_sticky_or_other`: stop 109 visible on 3 of 9 points (covered by `#case-name` and `#btn-export`), stop 117 visible on 6 of 9. `entirely_hidden_count` 0, so SC 2.4.11 AA passes. |
| N-14 twelve "Technical details" summaries share a name | nit | open | 12 visible (`technical_details_visible` 12). |
| N-15 source dialog Tab goes to browser chrome and back | nit | open, unchanged | `source_modal_tab_targets` alternates BODY (browser chrome) and Close. Batch-confirm shows the same pattern (`s_shift_a_tab_inside_4`). Not a trap. |
| m1 live region node | minor | fixed | `rv-live` and `progress-text` keep their nodes across an Accept (`l_after_accept_identity`: `rvSame` true, `ptSame` true). |
| m3 dismiss-with-reason | minor | fixed | See N-6. |
| m4 blocked-copy alert | minor | fixed | Copy anyway blocked: `role="alert"`, class `error` (`j_copy_anyway_status`). |
| m5 landmarks and headings | minor | fixed | See N-7. |
| m6 skip links | minor | partial | See N-8. |
| m7 row tab stops | minor | open | See N-9. |
| m8 Enter vs a | minor | fixed (unchanged) | Enter on Accept e1 moves focus to the next needs-review item, `flag-f_r7_1`, as in pass 2. |
| M6 generic button names | major, now minor | fixed | Timeline names, flag and charge "Why this status" names all fixed (N-5). |
| B1, M1 to M5 (pass 1) | blocker, majors | fixed | Letter keys from Export or an input change nothing (`s_from_export_focus`, `T-060-accessibility-pass3-keyboard-results.json`). Dark and light contrast 0 failing (below). Export focus on the heading in view, Copy letter one Tab away. Copy anyway returns focus to Copy letter. |

## New findings

### Minor

**P3-1. The row More/Less control's name omits its visible text and changes with its state.** (SC 2.5.3 Label in Name, Level A; same class as pass-2 N-10, rated minor there.)
- Evidence: `review.js:35` `aria-label: (openRows.has(e.id) ? "Show less of " : "Show all of ") + who`. Collapsed: visible "More", name "Show all of Austin EMS run report, 2026-01-09", `aria-expanded` "false". Expanded: visible "Less", name "Show less of Austin EMS run report, 2026-01-09", `aria-expanded` "true" (`T-060-accessibility-pass3-names.json` `pending.toggle`, `toggle_after_open`).
- Why it matters: the collapsed name does not contain the visible word "More". The name also changes with `aria-expanded`, so a screen reader can say the state twice.
- Fix: keep one name that contains the visible word, for example `aria-label` "More: <item>" / "Less: <item>", or drop `aria-label` and use the visible word plus `aria-expanded` with the row name supplied another way. Pick one and keep it stable across states.
- Acceptance test: the toggle's accessible name contains its visible text in both states; `aria-expanded` is the only state change.

**P3-2. The timeline container has `aria-labelledby` but no role, so its name is not exposed.** (SC 4.1.2; axe reports `aria-prohibited-attr` as needs-review, serious.)
- Evidence: `timeline.js:261` `el("div", { class: "timeline", "data-testid": "queue", "aria-labelledby": "h-timeline" }, ...)`. The element is also the skip-link target `#skip-to-review`. axe `aria-prohibited-attr` (incomplete, serious, message "aria-labelledby attribute is not well supported on a div with no valid role attribute") in 22 of 36 scans: 11 states, both themes (`T-060-accessibility-pass3-audit-results.json`, `d_incomplete_aria_prohibited_attr` in the extra probe).
- Why it matters: the attribute is prohibited on a generic `div`, so AT ignores it. The heading "Timeline" still exists visually, but the list has no programmatic name or role. This is a needs-review item in axe, not a violation, so it is a minor here.
- Fix: either remove `aria-labelledby` (the `h2` precedes the list), or give the container a role that allows a name, for example `role="region"` with `aria-labelledby` (only if a region landmark is wanted here).
- Acceptance test: axe `aria-prohibited-attr` incomplete count 0 in the queue states, and the element has either no `aria-labelledby` or a role that allows it.

**P3-3 (folded into N-8). Export-view skip links are dead.** Evidence: `T-060-accessibility-pass3-extra.json` `a_export_view_skip.targets`: `#skip-to-review`, `#skip-to-flags`, `#skip-to-charges` do not exist in the Export view; `#btn-export` does. Fix and test as in N-8.

**Carried: N-8 (partial) and N-9 (open)** are listed in the pass-2 table above; their fixes are unchanged.

### Nit

**P3-4. Export heading has no visible focus indicator after Enter on Export.** (SC 2.4.7 applies to the focused element; the checklist scopes the rule to interactive elements, so this is a nit.)
- Evidence: `T-060-accessibility-pass3-keyboard-results.json` `j_export_focus`: tag `h2`, name "Export", `outlineStyle` "none". The same value is in the pass-2 keyboard JSON, so it was not new in this build; it was not logged in pass 2.
- Fix: give the focused heading a focus style, for example `h2[tabindex="-1"]:focus-visible { outline: var(--focus-ring); }`.
- Acceptance test: after Enter on Export, the heading shows a 2 px ring with at least 3:1 contrast.

**P3-5. Accept on a decided row keeps `aria-pressed="true"` but a second press does nothing.** (SC 4.1.2 value; the announcement is correct.)
- Evidence: `T-060-accessibility-pass3-names.json` `accepted.accept`: `aria_pressed` "true", name "Accepted: Austin EMS run report, 2026-01-09". `T-060-accessibility-pass3-noop.json`: second press leaves `data-review` "accepted" and `aria-pressed` "true", and `rv-live` says "Accepted already. Use Undo to change it."
- Why it matters: `aria-pressed` means a toggle. A button that cannot turn off is a button, and Undo is the separate control.
- Fix: drop `aria-pressed` on a decided Accept (the state is already in the visible text and label), or make the control a real toggle.
- Acceptance test: a decided Accept has no `aria-pressed` attribute, or pressing it changes the value.

**Carried nits (unchanged or open):** N-11 (focus after Accept, product question), N-12 (two polite regions), N-13 (two stops partly under the sticky header at 320 px), N-14 (twelve "Technical details" names), N-15 (source dialog Tab through browser chrome). Fixes and acceptance tests are in the pass-2 review.

## Checks that passed this pass

- **axe-core, 18 states x light and dark (36 scans):** 0 serious or critical violations. Moderate `skip-link` in 6 scans (Export and copy views, N-8). `landmark-unique` gone. `definition-list` gone. Axe "incomplete" items (needs review): `color-contrast` in the empty states, why dialog and dialogs; `aria-prohibited-attr` (P3-2). My own computed contrast found 0 failures for these, so the axe incomplete items are not text-contrast failures.
- **Computed contrast (own script, all 36 scans):** 22,034 visible text nodes checked, 0 below threshold; 136 control boundaries checked, 0 below 3:1.
- **Focus ring (keyboard walk):** 215 stops light, 215 dark, 211 at 320 px. Minimum ring contrast 5.51:1 light, 6.63:1 dark. 0 entirely hidden. Two partly hidden at 320 px (N-13).
- **Target size (SC 2.5.8, 24 x 24 CSS px):** 0 undersized in the queue at 1280 and 375 (367 and 368 controls, audit). 0 undersized with Case checks open, and in the flags, charges and Export views at 1280 and 375 (270 to 276 visible controls per state, `T-060-accessibility-pass3-extra.json` `c_targets_*`).
- **Reduced motion:** `prefers-reduced-motion: reduce` gives 0 running transitions or animations; no preference gives 40.
- **Keyboard-only sample journey:** skip link to the first item (Enter), Accept e1 (Enter), Dismiss e3 (Tab to button, Enter), Edit e2 with Escape, a refused edit (announced, `role=alert`, `aria-describedby`), source dialog and Why dialog (Escape returns focus to the opener), audit drawer, dismiss-with-reason (Enter, input focused), Export (Enter), Copy letter (confirm shown), Copy anyway (blocked notice `role=alert`, focus back on Copy letter), Shortcut sheet from the Shortcuts button, Shift+A confirm from a row (Cancel focused, Accept 9 with `role=status` and focus on Undo).
- **Shortcut gating (SC 2.1.4):** j, k, p, Shift+A, a, d, e, r, o and ? from the Export button change nothing (`s_from_export_focus`).
- **Live regions (DOM only):** `rv-live` (`role=status`) and `progress-text` (`role=status`) exist at load and keep their nodes across actions. Accept, dismiss, Accept 9 and "Accepted already" each announce text.
- **Names and states:** decided rows expose `aria-pressed` on Accept or Dismiss and change the label to "Accepted:" or "Dismissed:"; Undo has a name with the item. Edit textarea name includes the visible rule. Dismiss-with-reason exposes `aria-expanded` and `aria-controls`.

## What is right

- All four pass-2 majors are closed, and each fix was measured in the running build, not read from the code.
- The keyboard-only journey completes end to end. Export and copy confirmations take focus and announce, and the letter keys act only from an item row.
- Contrast, focus rings, target size and 320 px reflow hold with the disclosures open. The r3 e2e file passes 18 of 18 on this build.

## Not exercised and limits

- No screen reader. Announcements were checked by DOM inspection only.
- Not run in this pass: 200% and 400% zoom, Windows high-contrast or forced-colors mode, the excerpt editor, manual entry, PDF and file-chooser content beyond opening it, library cases other than the sample, the `Undo` tab order beyond focus landing on it.
- Pass-2 reflow and keyboard scripts were re-run with the port and commit changed (`artifacts/review-evidence/T-060-accessibility-pass3-*.py`). New probes: `file-ring-zoom`, `extra`, `names`, `noop`.
- This is one review. It does not claim WCAG 2.2 AA conformance for the app. It reports what was tested.

## Questions for Chris

- Should focus after Accept stay in the timeline (next row), or keep the needs-review-first rule into Flags (N-11)?

```json
{"card": "T-060", "persona": "accessibility-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD e1ce8dc620e6ec0778320456ac79a25f1832bfee via git archive into the scratchpad (frontend last changed in 7d5a45f; the r3 commits c8e36fb, 5d975ed, d9efc5c and 7d5a45f are ancestors; e1ce8dc is backend only); uncommitted working-tree edits not audited; app http://127.0.0.1:7895 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated); sample case evals/golden sample (9 synthetic records, 23 items)",
 "exercised": [
  "pytest tests/e2e/test_polish_r3.py against the HEAD copy (E2E_BASE_URL=http://127.0.0.1:7895): 18 passed in 23.25s",
  "axe-core 4.10.3 (sha256 880970c0...) on 18 states x light and dark with WCAG 2.2 AA tags and best-practice: 0 serious or critical violations; moderate skip-link in 6 scans; aria-prohibited-attr incomplete in 22 scans (artifacts/review-evidence/T-060-accessibility-pass3-audit-results.json)",
  "computed contrast of every visible text node (22,034 across 36 scans) and every control boundary (136): 0 failing (T-060-accessibility-pass3-audit-results.json)",
  "target size (24x24 CSS px) at 1280 and 375 in the queue (367 and 368 controls, 0 undersized); with Case checks open, flags, charges and Export at 1280 and 375 (270 to 276 visible controls each, 0 undersized) (T-060-accessibility-pass3-extra.json)",
  "keyboard-only Tab walk from the top: 215 stops light, 215 dark, 211 at 320 px; focus ring minimum 5.51 light and 6.63 dark; entirely hidden 0; per-row stops and button names (T-060-accessibility-pass3-keyboard-results.json, walk_1280_names|light)",
  "keyboard-only sample journey: skip link, Accept e1, Dismiss e3, edit with Escape, refused edit, source and Why dialogs, audit drawer, dismiss-with-reason, Export, Copy letter, Copy anyway, shortcut sheet, theme toggle x3, Shift+A confirm, letter keys from Export (T-060-accessibility-pass3-keyboard-results.json)",
  "320 CSS px reflow: queue, edit, flags, charges, Export, source dialog, with Case checks and the AI-check panel both open; Case checks open only (T-060-accessibility-pass3-reflow-probe.json, reflow-check2.json, T-060-accessibility-pass3-extra.json b_reflow320_*)",
  "Upload .txt focus: stop 4 from the top; 3x zoom ring and contrast; Enter and Space open a file chooser (T-060-accessibility-pass3-file-probe.json, file-ring-zoom.json, file-ring-zoom.png)",
  "theme toggle accessible name after 1, 2 and 3 presses, and forced dark and light (T-060-accessibility-pass3-names.json, theme-probe.json)",
  "accessible names and states: Why this status names (23, all unique), edit textarea name and refused-edit association, dismiss-with-reason aria-controls, decided-row aria-pressed and labels, More/Less name and aria-expanded (T-060-accessibility-pass3-details.json, names.json, noop.json)",
  "skip links: queue hrefs resolve; Export and copy view hrefs checked and activated (T-060-accessibility-pass3-skip-probe.json, extra.json a_export_view_skip)",
  "live regions by DOM: rv-live and progress-text node identity and text across Accept, dismiss, Accept 9 and a second Accept (T-060-accessibility-pass3-keyboard-results.json l_*, noop.json)",
  "reduced motion: reduce 0 transitions or animations; no preference 40 (T-060-accessibility-pass3-audit-results.json)",
  "headings, landmarks and duplicate landmark names (axe landmark-unique absent); html lang and title (theme-probe.json)"],
 "verdict": "pass",
 "scores": {"keyboard_operability": 5, "focus_order_and_visibility": 4, "names_roles_states": 4, "status_announcements": 4, "contrast_light": 5, "contrast_dark": 5, "target_size": 5, "reflow_320": 5, "reduced_motion": 5, "landmarks_headings": 4, "axe_serious_critical": 4},
 "findings": [
  {"severity": "minor", "title": "N-8 (partial): skip-link hrefs in the Export and copy views point at elements that do not exist; axe skip-link moderate in 6 scans",
   "evidence": "T-060-accessibility-pass3-extra.json a_export_view_skip.targets: #skip-to-review, #skip-to-flags, #skip-to-charges target_exists false in the Export view; #btn-export exists. axe skip-link 'No skip link target' n=3 in 14-export, 15-copy-confirm, 16-copy-blocked-status, light and dark (T-060-accessibility-pass3-audit-results.json). Queue-view hrefs resolve (skip_targets_exist true). app.js:68-69 builds the hrefs from elements found at nav build time.",
   "why_it_matters": "SC 2.4.1 (AA). Activation still works through the onclick handler, so the keyboard path is not broken, but the href is dead in those views and assistive tech and no-JS readers get a dead link. The r3 test covers the queue view only.",
   "fix": "Resolve the hrefs in every view: rebuild the skip-nav targets when the view changes, or point each href at an element that exists in that view (for example the Export heading for Export).",
   "acceptance_test": "In the Export view and the copy-confirm view, every #skip-nav a href resolves to a rendered element; axe skip-link count 0 in all 18 states x 2 themes; add the Export view to test_skip_link_hrefs_resolve_to_elements."},
  {"severity": "minor", "title": "N-9 (open): each timeline row is a Tab stop and is followed by 8 buttons (pass-1 m7, pass-2 N-9)",
   "evidence": "review.js:358 `if (!rowEl.hasAttribute('tabindex')) rowEl.setAttribute('tabindex', '0')`. At 1280 px light the walk has 19 row article stops, each followed by Accept, Edit, Dismiss, Why this status, Open record, Audit, Change quote and More (T-060-accessibility-pass3-keyboard-results.json walk_1280_names|light, stops 20 to 28).",
   "why_it_matters": "APG composite pattern: a row that is both a stop and a container of stops gives a mixed model, and the sample needs about 215 Tab presses to walk the page. Every action is still reachable, so this is minor.",
   "fix": "Choose one model. Either a roving tabindex across the queue with j and k as the arrow keys, or remove the row tabindex and keep the buttons as the only stops (or keep the row stop and move its buttons behind it).",
   "acceptance_test": "One Tab model documented on the card and visible in the walk: either one stop per row with arrow keys, or no row stops; the Tab walk count to Export drops from the current value and every action stays reachable."},
  {"severity": "minor", "title": "P3-1: the row More/Less control's name omits its visible text and changes with state (SC 2.5.3)",
   "evidence": "review.js:35 aria-label: (openRows.has(e.id) ? 'Show less of ' : 'Show all of ') + who. Collapsed: visible 'More', name 'Show all of Austin EMS run report, 2026-01-09', aria-expanded 'false'. Expanded: visible 'Less', name 'Show less of ...', aria-expanded 'true' (T-060-accessibility-pass3-names.json pending.toggle and toggle_after_open).",
   "why_it_matters": "SC 2.5.3 Label in Name (Level A): the collapsed name does not contain the visible text 'More'. The name also changes with aria-expanded, so state is announced twice. Same class as pass-2 N-10, rated minor there.",
   "fix": "Keep one stable name that contains the visible word, for example aria-label 'More: <item>' and 'Less: <item>', or let the visible word be the name and give the row context another way. Keep aria-expanded as the only state change.",
   "acceptance_test": "The toggle's accessible name contains its visible text ('More' or 'Less') in both states, and does not change except for the visible word."},
  {"severity": "minor", "title": "P3-2: the timeline container has aria-labelledby with no role; axe aria-prohibited-attr (incomplete, serious) in 22 scans",
   "evidence": "timeline.js:261 el('div', { class: 'timeline', 'data-testid': 'queue', 'aria-labelledby': 'h-timeline' }, ...). The same element is the skip-link target #skip-to-review. axe aria-prohibited-attr needs-review message 'aria-labelledby attribute is not well supported on a div with no valid role attribute' in 03-queue, 04-edit-open, 08-flags, 09-charges, 12-dismiss-reason-open, 13-export-blocked, 14-export, 15-copy-confirm, 16-copy-blocked-status, 17-side-by-side, 18-case-switcher-open, both themes (T-060-accessibility-pass3-audit-results.json; T-060-accessibility-pass3-extra.json d_incomplete_aria_prohibited_attr).",
   "why_it_matters": "SC 4.1.2. The attribute is prohibited on a generic div, so the list has no programmatic name and AT ignores it. The visible h2 'Timeline' still titles the list. axe marks it needs-review, not violation, so this is minor.",
   "fix": "Remove aria-labelledby from the div (the h2 precedes the list), or give the container a role that allows a name (for example role='region' with aria-labelledby, only if a landmark is wanted).",
   "acceptance_test": "axe aria-prohibited-attr incomplete count 0 in the queue states; the container has no aria-labelledby, or a role that allows it."},
  {"severity": "nit", "title": "P3-4: the Export heading has no visible focus indicator after Enter on Export (outline none)",
   "evidence": "T-060-accessibility-pass3-keyboard-results.json j_export_focus: tag h2, name 'Export', outlineStyle 'none', outlineWidth 3px. The same value is in T-060-accessibility-pass2-keyboard-results.json j_export_focus (not logged in pass 2).",
   "why_it_matters": "SC 2.4.7 applies to the focused element. The checklist scopes the visible indicator to interactive elements, so this is a nit; a sighted keyboard user cannot see where focus went after Enter.",
   "fix": "Give the focused heading a focus style, for example h2[tabindex='-1']:focus-visible { outline: var(--focus-ring); }.",
   "acceptance_test": "After Enter on Export, the heading shows a ring of at least 2 px with at least 3:1 contrast against its background."},
  {"severity": "nit", "title": "P3-5: Accept on a decided row keeps aria-pressed='true' but a second press does nothing",
   "evidence": "T-060-accessibility-pass3-names.json accepted.accept: aria_pressed 'true', name 'Accepted: Austin EMS run report, 2026-01-09'. T-060-accessibility-pass3-noop.json: second press leaves data-review 'accepted' and aria-pressed 'true'; rv-live says 'Accepted already. Use Undo to change it.'",
   "why_it_matters": "SC 4.1.2 value. aria-pressed means a toggle; this button cannot turn off. The announcement is correct, so this is a nit.",
   "fix": "Drop aria-pressed on a decided Accept (the state is already in the label and the visible text), or make it a real toggle.",
   "acceptance_test": "A decided Accept has no aria-pressed attribute, or pressing it changes the value."},
  {"severity": "nit", "title": "N-11 (carried): focus after Accept moves to the next needs-review item in Flags; the announcement does not name the destination",
   "evidence": "T-060-accessibility-pass3-keyboard-results.json j_accept_e1: focus flag-f_r7_1 'Accident date source'; live 'Accepted: Austin EMS run report, 2026-01-09. 22 left to review.'",
   "why_it_matters": "Predictable by the documented rule, but the user cannot tell where focus went without looking. Product choice.",
   "fix": "Optional: add the destination to the announcement, or keep focus in the timeline (see question for Chris).",
   "acceptance_test": "The announcement names the item that now has focus, if the rule is kept."},
  {"severity": "nit", "title": "N-12 (carried): two polite status regions update on each decision",
   "evidence": "T-060-accessibility-pass3-keyboard-results.json j_accept_e1 live_after: rv-live 'Accepted: ...' (review.js:57, role=status) and progress-text '1 of 23 decided' (index.html:22, role=status).",
   "why_it_matters": "A screen reader may read both on one action.",
   "fix": "Keep one decision announcement; update the progress count without a second polite announcement.",
   "acceptance_test": "One decision produces one polite announcement."},
  {"severity": "nit", "title": "N-13 (carried): at 320 CSS px two stops are partly under the sticky header",
   "evidence": "T-060-accessibility-pass3-keyboard-results.json walk_320|light partly_hidden_by_sticky_or_other: stop 109 visible on 3 of 9 points (covered by #case-name and #btn-export), stop 117 on 6 of 9; entirely_hidden_count 0.",
   "why_it_matters": "SC 2.4.11 (AA) passes because no stop is entirely hidden. The checklist asks for no overlap.",
   "fix": "scroll-padding-top equal to the sticky header height.",
   "acceptance_test": "No focus box intersects the sticky header at 320x640 on the sample walk."},
  {"severity": "nit", "title": "N-14 (carried): twelve 'Technical details' summaries share one name",
   "evidence": "T-060-accessibility-pass3-details.json technical_details_visible = 12.",
   "why_it_matters": "SC 2.4.6 weak; the summary sits under a heading, so context exists visually.",
   "fix": "Name each with its item, or leave as is.",
   "acceptance_test": "Optional."},
  {"severity": "nit", "title": "N-15 (carried): source and batch dialogs: Tab goes from Close or Cancel to browser chrome and back",
   "evidence": "T-060-accessibility-pass3-details.json source_modal_tab_targets: BODY (browser chrome) and Close alternate; T-060-accessibility-pass3-keyboard-results.json s_shift_a_tab_inside_4.",
   "why_it_matters": "Not a trap: focus returns to the dialog. Standard showModal behaviour. A long record may need a scrollable focusable region.",
   "fix": "None now; check with a long record.",
   "acceptance_test": "Load a record longer than the dialog and confirm the text region is keyboard reachable."}
 ],
 "whats_right": [
  "All four pass-2 majors are fixed and measured in the running build: shortcut sheet keys, 320 px reflow with Case checks and the AI-check panel open, theme toggle name, and the Upload control ring that opens the chooser on Enter and Space.",
  "The keyboard-only sample journey completes end to end, letter keys act only from an item row, and the Accept and Copy confirmations move focus and announce.",
  "0 serious or critical axe violations in 36 scans; 0 failing text or control contrast in 22,034 text nodes and 136 boundaries; 0 undersized targets; 320 px reflow passes with both disclosures open."
 ],
 "questions_for_chris": [
  "Should focus after Accept stay in the timeline (next row), or keep the needs-review-first rule into Flags (N-11)?"
 ]}
```
