# T-060 pass 1: accessibility review (WCAG 2.2 AA)

Reviewer: accessibility-reviewer (model claude-haiku-5-5, as run). Date 2026-11-02. Review only; no product code changed.
Verdict: **fail**. One blocker (single-key shortcuts that act outside the focused item, including a one-keystroke accept of all 9 verified entries), six majors, seven minors, one nit.

## Summary

The light theme is in good shape: no serious or critical axe violations in any of the 13 light states, no text or focus-ring contrast failures, no target under 24 CSS px, and no horizontal scrolling at 320 CSS px. The keyboard path works end to end (accept, dismiss, edit with Escape, refused edit, record dialogs, export, copy).

The dark theme (prefers-color-scheme: dark, the only theme that exists) is not shippable as is. Review-panel headings, helper text and the AI-check titles render at 1.1:1 to 2.8:1, the Export button is 2.14:1, and focus rings are 2.73:1 on 94 of 160 tab stops. Separately, global single-letter shortcuts (j, k, p, Shift+A) are not gated to a focused item, and focus is lost or left off-screen at the Export and Copy steps.

## Scope and method

- Commit audited: `f187a307e44fca87a9e09c834d51081c8ae33535` (HEAD when the run started), extracted with `git archive` into the scratchpad. HEAD later moved to `3223e5017dfcd02e4f79d67d1674a95aa3b1c5be`; `git diff --stat f187a30 3223e50 -- app/frontend` is empty, so the audited frontend is current. Uncommitted frontend edits in the working tree (api.js, charges.js, flags.js, index.html, manual.js, review.js, timeline.js, new suggestions.css/js) were not audited and may change these results.
- Server: `ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, `HOST=127.0.0.1 PORT=7893`, DB in the scratchpad. Synthetic sample case only (`evals/golden` sample, 9 records).
- axe-core 4.10.3 (npm, sha256 880970c0...), injected with `bypass_csp` (test-only, so the script can run; the app's CSP is unchanged). Tags: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice.
- Playwright (Chromium 156) with prefers-color-scheme light and dark, prefers-reduced-motion both values, viewports 1280x900, 375x812 and 320x640.
- Scripts and outputs are in `artifacts/review-evidence/` (files prefixed `T-060-accessibility-`).

Exercised (all run against the live app):
1. axe-core on 13 states per theme: empty, empty with error (Analyze with no text), queue, edit open, source-record dialog, Why? dialog, audit drawer, flags, charges, export blocked, export, copy confirmation, side-by-side. Results: `T-060-accessibility-audit-results.json`, logs in `T-060-accessibility-audit.log`.
2. Computed contrast of every visible text node (711 in the light queue state, 715 in dark) and of text-field boundaries, both themes. Focus-ring contrast on all 160 tab stops of a walk from the top, both themes (`T-060-accessibility-focus-contrast-results.json`).
3. Keyboard-only walkthrough: start the sample, Analyze, accept entry 1, dismiss entry 3, edit entry 2 (Escape cancel, refused edit with an invented number), open the source dialog and close it, open Export, Copy letter, the copy confirmation (`T-060-accessibility-keyboard-results.json`).
4. Full Tab walk from the document top on the queue (232 stops, `T-060-accessibility-tabwalk-from-top.json`).
5. Dialogs: Why?, audit drawer, source record, and the flag dismiss-with-reason disclosure (`T-060-accessibility-dialogs-results.json`).
6. Case-checks stepper and AI-check panel: disclosure, a step action button, focus after activation (`T-060-accessibility-stepper-results.json`).
7. Single-key shortcuts with focus on Export (j, Shift+A, p), 1280 px (keyboard results).
8. Reflow at 320 CSS px: empty, queue, edit, export, source dialog, flags, charges (horizontal overflow and offenders).
9. Target sizes at 1280 and 375 (251 and 250 controls).
10. Reduced motion: computed transitions and animations, both preferences.
11. Headings, landmarks, accessible names of all buttons (inventory in the audit JSON).
12. Screenshots: `T-060-accessibility-*.png` (dark flags: `T-060-accessibility-08-flags-dark.png`).

Screen reader: not available. Live-region behaviour is checked by DOM inspection only; no announcement was heard.

## Findings

### Blocker

**B1. Single-key shortcuts act outside the focused item. Shift+A accepts all 9 verified entries from Export focus.** (SC 2.1.4 Character Key Shortcuts, Level A; unsafe state change, D.2)
- Selectors: document-level keydown handlers. `batch.js:98` (`ev.key !== "A"` then `acceptAll()`); `review.js:290` (global `j`/`k` branch, `focusItem(n)`); `sidebyside.js:102` (`p` moves focus into `[data-testid=sbs-pane]`).
- Evidence: keyboard run, focus on `[data-testid=btn-export]`: `key_shift_a_with_focus_on_export` = `{accepted_before: 0, accepted_after: 9}`; `key_j_with_focus_on_export` = `{moved_to_item: true, after: "a2"}`; `key_p_with_focus_on_export_1280` = focus moves to `[data-testid=sbs-body]`.
- Why it matters: the shortcuts are not turned off, remapped, or limited to the component that has focus. A single keystroke, typed with focus on an unrelated control (or from browse mode in a screen reader), accepts every verified entry into the letter path with no confirmation. Only `a/d/e/r/o` are gated to an item (`review.js:~305`), so the gating is inconsistent.
- Fix: remove the document-level `j`, `k`, `p` and `Shift+A` listeners, or scope them to the element carrying `data-item-id` (`review.js:290` must not run when the target has no item). Keep batch accept as a button with a confirmation step. If shortcuts stay, add a visible "turn off shortcuts" setting (SC 2.1.4 second option).
- Acceptance test (Playwright): focus Export, press `j`, `p`, `Shift+A`; focus does not move and accepted count stays 0. Focus an entry row, press `a`, `d`, `e`; those still work and advance as designed.
- Note: whether batch accept should exist at all is a product question (D-011 cut it; T-055/D-031 appears to reinstate it). I rate the accessibility defect; the product decision is outside my lens. See questions_for_chris.

### Major

**M1. Dark theme: review headings, helper text and AI-check titles fail 1.4.3 (1.1:1 to 2.8:1); Export button 2.14:1.** (SC 1.4.3, AA)
- Selectors: `#rv-flags-h`, `#rv-g-gap`, `#rv-g-conflict`, `#rv-g-pre_existing`, `#rv-g-causation`, `#rv-charges-h`, `#rv-unclear-h`, `#zj-h`, `h2` "Audit", `th` "Amount", `p.rv-help`, `p.rv-keys`, `p.rv-empty`, `button[data-testid=btn-export].btn.primary`.
- Evidence: computed check, dark queue state: 80 text nodes below threshold, e.g. `h2#rv-flags-h` "Flags" rgb(28,36,48) on rgb(23,26,33) = 1.11:1. axe (dark, queue) reports `color-contrast` serious, 38 nodes; dark flags, charges, export and side-by-side states the same. Light: 0 nodes. Root causes: `review.css:3` defines `--rv-ink:#1c2430` on `:root` with no dark value; `review.css:7` `.rv-panel{color:var(--rv-ink)}`; `styles.css:21` `.btn.primary{color:#fff}` on the dark accent `#8fb0ff` (`styles.css:3`). Screenshot: `T-060-accessibility-08-flags-dark.png`.
- Why it matters: card headings and group labels are how a paralegal navigates 20 flags and charges; in dark mode they are nearly invisible. The flag card bodies are readable (white cards), so this is an AA failure that is not yet a loss of a must-have action.
- Fix: add dark values in `review.css` for `--rv-ink` (#E7EAEF), `--rv-muted` (#B0B9C6, 8.8:1 on the panel), `--rv-bg`, `--rv-soft`, `--rv-line`, using the same `prefers-color-scheme: dark` and `:root[data-theme=dark]` pattern as `styles.css:3`. For `.btn.primary` in dark, use text `#0E1116` on `#8FB0FF` (about 8.8:1).
- Acceptance test: rerun `T-060-accessibility-focus-contrast.py` and `T-060-accessibility-audit.py`; in dark, 0 text nodes below 4.5:1 (3:1 for large text) in queue, flags, charges, export and AI-check states; axe `color-contrast` 0.

**M2. Dark theme: focus rings 2.73:1 on 94 of 160 tab stops.** (SC 1.4.11 Non-text Contrast, AA; SC 2.4.7 is met only with a visible ring)
- Selectors: `.rv-btn:focus` (accept, edit, dismiss, audit in every row: 36 stops), `.cs-btn` case-switcher buttons (28 stops), `.rv-btn` library buttons (15 stops).
- Evidence: `review.css:5` `--rv-focus:#0b57d0` has no dark value; `review.css:19` applies it. Measured outline `rgb(11,87,208)` on `rgb(23,26,33)` = 2.73:1 (`T-060-accessibility-focus-contrast-results.json`, `focus|dark`). Light: 0 of 160 below 3:1, minimum 5.9:1.
- Fix: `--rv-focus: #8FB0FF` in the dark block (8.1:1 on `#171A21`).
- Acceptance test: dark Tab walk from the top of the queue, 160 stops, minimum ratio at least 3.0.

**M3. Paste box and Order select: input boundaries 1.4:1 in both themes.** (SC 1.4.11, AA)
- Selectors: `textarea[data-testid=input-text]` (paste), `select[data-testid=sort]` (Order). Border `rgb(213,218,226)` on white = 1.40:1 light; `rgb(44,50,64)` on the dark panel = 1.36:1 dark (dark sort select 1.36:1).
- Evidence: `styles.css:17` (`textarea{...border:1px solid var(--line)}`) and `styles.css:32` (`select{...border:1px solid var(--line)}`); `T-060-accessibility-focus-contrast-results.json` (`boundary|light`, `boundary-empty|dark`).
- Why it matters: the paste box is the first control of the flow and has no other visual cue of its edges.
- Fix: input, textarea and select borders use `--border-strong` (`#6F7B8B` light, `#7A8696` dark; the brief gives 4.3:1 and 4.7:1 on panels).
- Acceptance test: boundary check at least 3:1 for every textarea, select and text input in both themes. The edit box (`edit-summary`) is at exactly 3.00:1 light and passes; it should be kept at or above 3:1 after the fix.

**M4. Export: focus stays on the Export button, which is then scrolled far off screen. Copy letter is 231 Tab presses away.** (SC 2.4.3 Focus Order, SC 2.4.7 Focus Visible, AA)
- Selectors: `[data-testid=btn-export]` then `#view-export`, `[data-testid=btn-copy-letter]`.
- Evidence: after Enter on Export, `focus_after_export_open` = `{testid: "btn-export", rect: [188, -9159, 80, 44]}` (top at -9159 px in a 900 px viewport). From there, `tab_to_copy_letter` = 231 presses.
- Cause: `export.js:48` scrolls `#view-export` into view but never moves focus into it.
- Fix: after `render()` in `load()` (export.js:48 scroll branch), focus the export section heading (`#ex-h1` container with `tabindex="-1"`) or the first control of the export.
- Acceptance test: after Enter on `btn-export`, `document.activeElement` is inside `#view-export` and within the viewport; Tab from there reaches `btn-copy-letter` in at most 3 presses.

**M5. Focus is lost to the document after "Copy anyway".** (SC 2.4.3 Focus Order, AA; checklist item 6)
- Selectors: `[data-testid=btn-copy-anyway]`, `[data-testid=copy-confirm]`.
- Evidence: `export.js:23` `onclick: () => { box.hidden = true; then(); }` hides the focused button and moves focus nowhere. Result: `copy_anyway_focus` = `BODY` (`T-060-accessibility-dialogs-results.json`). The copy itself works: with clipboard permission the status reads "Copied the treatment section." in `role="status"`.
- Fix: after hiding the confirmation, focus `#export-status` (give it `tabindex="-1"`) or the Copy letter button.
- Acceptance test: after Copy anyway, `document.activeElement` is the Copy letter button or the status element; status text is "Copied the treatment section."

**M6. Repeated generic button names with no entry context.** (SC 2.4.6 Headings and Labels, AA; SC 4.1.2 supporting; checklist item 9)
- Selectors: `[data-testid=entry-why]` "Why?" (9 visible), `[data-testid=btn-source]` "Open record" (9), `[data-testid=btn-edit-excerpt]` "Change quote" (9). Accept and Edit names carry only the provider, with no date: `aria-label` "Accept: Capital PT, initial evaluation" (`review.js:217,221`).
- Evidence: button inventory in `T-060-accessibility-audit-results.json` (`button_inventory`). Source: `timeline.js:31` (Why?), `timeline.js:32` (Open record).
- Why it matters: in a list of buttons (screen-reader rotor, or voice control "click Why") nine identical "Why?" and "Open record" buttons cannot be told apart.
- Fix: add context. Examples: `aria-label="Why? Austin EMS run report, 2026-01-09"`, `aria-label="Open record 2 for Central ER discharge summary"`, `aria-label="Accept: Capital PT, initial evaluation, 2026-01-23"` (date added).
- Acceptance test: for every visible button in the queue, accessible name includes provider and date; no two visible buttons share a name.

### Minor

**m1. Live-region placement and churn.** (SC 4.1.3, DOM inspection only)
- `review.js:55` creates `#rv-live` (`role=status`) lazily on the first decision; `live_region_in_dom_at_load` = false. `export.js:33` (`[data-testid=count-line]`, `role=status`) is a new node on every re-render: `count_line_node_replaced_by_decision` = `same: false` after an accept.
- Fix: render `<div id="rv-live" role="status" aria-live="polite" class="sr"></div>` once in `index.html`; keep the count-line node stable across re-renders (update its text).
- Acceptance test: `#rv-live` exists before the first action; identity is preserved across a decision. Announcements still need checking with VoiceOver or NVDA.

**m2. Refused edit is not linked to its field.** (SC 3.3.1 and 3.3.3 are met by text; checklist item 12 association is not)
- The message "The summary has a number, date or dollar figure that is not in the quote: 2031, 99. Remove it or change the quote." appears in `.rv-error` with `role="alert"` (`review.js:128,134`), but the textarea has `aria-describedby` null and `aria-invalid` null (`refused_edit_entry2`).
- Fix: `aria-invalid="true"` and `aria-describedby` pointing at the error element while it is shown.
- Acceptance test: DOM check after a refused edit.

**m3. Dismiss-with-reason disclosure does not expose its state.** (SC 4.1.2, AA)
- `review.js:225` button "Dismiss with reason…" has no `aria-expanded` and no `aria-controls` (`dismiss_reason_button_attrs`). The input appears on activation and focus moves to it correctly.
- Fix: `aria-expanded` toggled with the reason row, and `aria-controls` pointing at the form.
- Acceptance test: attribute values change with each activation.

**m4. "Copy blocked" failure is announced as a status, not an alert.** (SC 4.1.3, checklist item 11)
- `export.js:11` `status(msg, bad)` sets a class but leaves `role="status"`; the message "The browser blocked copying. Select the text in the box and copy it by hand." is therefore polite.
- Fix: set `role="alert"` when `bad` is true.
- Acceptance test: `status(..., true)` yields `role="alert"`.

**m5. Landmarks and headings.** (SC 1.3.1 and 2.4.1 supporting; axe best-practice `region`, `landmark-complementary-is-top-level`, `aria-allowed-role`)
- `index.html:13` `#banner-synthetic` (`role=note`) sits outside any landmark (axe `region`, moderate, 1 node).
- `sidebyside.js:34` `aside` inside `main` (`landmark-complementary-is-top-level`, moderate).
- `flags.js:64` `article` with `role="group"` on each of 10 flags (`aria-allowed-role`, minor, 10 nodes).
- `judges.js:146` "How the AI was checked" is a `span` labelled into the section (`judges.js:143`), so it is not a heading in the heading list.
- Fix: move the banner into a labelled `region` or `header`; make the side-by-side pane a `section` with `aria-labelledby`; drop the `role="group"` on articles (use `section` or `div`); render the judge title as a heading (h2 or h3 to match the level).
- Acceptance test: axe best-practice `region`, `landmark-complementary-is-top-level` and `aria-allowed-role` at 0; heading list includes "How the AI was checked".

**m6. Keyboard path length; no skip link.** (SC 2.4.1 is met by landmarks, so this is a usability finding; the T-046 note and brief section 9 ask for skip links)
- 52 Tab presses from the top of the page to the first Accept; 232 stops in total; Export is stop 45 (`T-060-accessibility-tabwalk-from-top.json`). The case switcher (6 cases, 15 library buttons) and the case-checks rail come before the queue.
- Fix: a "Skip to review queue" link as the first focusable element; collapse the library list by default.
- Acceptance test: first Tab shows the skip link; Enter lands on the first needs-review row.

**m7. Each timeline row is a tab stop and also contains 4 to 5 buttons.** (checklist item 7, APG composite pattern)
- `review.js:322` sets `tabindex="0"` on each entry `article`, and each contains Why?, Open record, Accept, Edit, Dismiss, Audit: two stops per entry, with the arrow-key model (`j`/`k`) on top.
- Fix: choose one model. Either a roving tabindex across the queue (use `j`/`k`/arrows, one stop), or remove the row tabindex and keep the buttons as the stops.
- Acceptance test: one tab stop per entry, or the pattern documented in the card.

**m8. Enter on Accept and the `a` key move focus differently.** (SC 3.2.2 spirit, checklist item 6)
- Enter on Accept keeps focus on the same button (`focus_after_enter_accept_button_2`: item e2, pressed=true). The `a` key advances to the next row (`focus_after_key_a_on_row_4`). The brief (section 9) says Accept advances.
- Fix: one behaviour for both paths.
- Acceptance test: Enter and `a` on the same item leave focus on the same next item.

### Nit

**n1.** Dialogs: in the source-record modal the only focusable element is Close, so Tab alternates between Close and the browser chrome. This is standard for a modal with one focusable and is not a trap; a longer record may need a scrollable focusable region (not tested: the sample records are short).

## What is right

- Light theme: zero serious or critical axe violations in all 13 light states; 0 of 711 text nodes below threshold in the light queue; focus rings at least 5.9:1 on all 160 stops.
- Keyboard flow completes: Enter on Accept and Dismiss announce "Accepted: Austin EMS run report. 22 left to review." in `role="status"`; Edit moves focus into the textarea, Escape returns it to Edit, Tab leaves the textarea (no trap); a refused edit names the offending numbers in an alert. Why?, source record and audit drawer take focus, close on Escape, and return focus to the opener.
- Reflow and targets: no horizontal overflow at 320 CSS px in 7 states (empty, queue, edit, export, source dialog, flags, charges); 0 of 251 (1280) and 0 of 250 (375) controls under 24x24 CSS px; no element under the sticky synthetic-data banner on any of 232 stops; no transitions or animations running in the queue under either motion setting (the stepper's outline transition is gated to no-preference at `stepper.css:90`).

## Not exercised and limits

- No screen reader; live-region checks are DOM only.
- Dark theme was tested by emulating prefers-color-scheme in Chromium only; no forced-colors mode, no Windows high-contrast mode, no 200% or 400% zoom.
- Undated and ambiguous-date rows (the disabled Accept and the Dates to confirm path, D-041), the excerpt editor, manual entry, the narrative paragraph, the PDF upload, and library cases 02 to 15 were not walked by keyboard.
- The stepper's "Go to item" and "See the steps" buttons were checked for names only, not operated.
- Design brief items not present yet (theme toggle, density toggle, skip links, shortcut sheet, Undo) were not graded as defects; WCAG criteria were graded where the current app has the control.
- This is pass 1 of the card's stop rule; it does not claim WCAG conformance for the app.

## Prioritized top 10

1. **B1** (blocker) Global single-key shortcuts: Shift+A accepts all 9 entries from Export focus; j, k, p act without item focus (`batch.js:98`, `review.js:290`, `sidebyside.js:102`). Scope to item focus or remove; batch accept behind a confirmation.
2. **M1** (major) Dark theme text at 1.1 to 2.8:1 in flags, charges, AI-check headings and helper text; Export at 2.14:1 (`review.css:3`, `review.css:7`, `styles.css:21`).
3. **M4** (major) Export: focus left on an off-screen button; 231 presses to Copy letter (`export.js:48`).
4. **M5** (major) Focus lost to the document after "Copy anyway" (`export.js:23`).
5. **M2** (major) Dark focus rings 2.73:1 on 94 of 160 stops (`review.css:5`, `review.css:19`).
6. **M3** (major) Paste box and Order select boundaries 1.4:1 (`styles.css:17`, `styles.css:32`).
7. **M6** (major) Nine identical "Why?", "Open record" and "Change quote" buttons; Accept names lack the date (`timeline.js:31-32`, `review.js:217`).
8. **m5** (minor) Banner outside landmarks, side-by-side `aside` inside `main`, `role="group"` on articles, judge title not a heading (`index.html:13`, `sidebyside.js:34`, `flags.js:64`, `judges.js:146`).
9. **m1** (minor) Live region created lazily and count line node replaced on each render (`review.js:55`, `export.js:33`).
10. **m2, m3, m4** (minor) Refused edit not linked to its field; reason disclosure lacks aria-expanded; blocked-copy message is a status, not an alert (`review.js:225`, `export.js:11`).

Next: m6 (skip link), m7 (double tab stops), m8 (Enter and `a` focus) and n1 follow in the card's fix round.

```json
{"card": "T-060", "persona": "accessibility-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD f187a307e44fca87a9e09c834d51081c8ae33535 (git archive into scratchpad; HEAD later 3223e50, frontend unchanged between them); app http://127.0.0.1:7893 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated); sample case evals/golden sample (9 synthetic records); uncommitted working-tree frontend edits NOT audited",
 "exercised": [
  "axe-core 4.10.3 (pinned npm, sha256 880970c0...) on 13 states x light and dark: empty, empty-error, queue, edit open, source dialog, Why dialog, audit drawer, flags, charges, export blocked, export, copy confirmation, side-by-side (artifacts/review-evidence/T-060-accessibility-audit-results.json)",
  "computed contrast of 711 (light) and 715 (dark) text nodes in queue, text-field boundaries, focus-ring contrast on 160 Tab stops in light and dark (T-060-accessibility-focus-contrast-results.json)",
  "keyboard-only walkthrough: sample -> Analyze -> accept entry 1 -> dismiss entry 3 -> edit entry 2 (Escape; refused edit with invented number) -> source dialog open/Tab/Escape -> Export -> Copy letter -> copy confirmation (T-060-accessibility-keyboard-results.json)",
  "full Tab walk from document top on queue: 232 stops, sticky-banner overlap and outline checks (T-060-accessibility-tabwalk-from-top.json)",
  "Why?, audit drawer, dismiss-with-reason disclosure, copy status with and without clipboard permission (T-060-accessibility-dialogs-results.json)",
  "case-checks stepper disclosure, step action button, judge panel focus (T-060-accessibility-stepper-results.json)",
  "single-key shortcuts j, p, Shift+A with focus on Export (keyboard results)",
  "reflow at 320 CSS px in 7 states; target sizes at 1280 and 375 (251 and 250 controls); reduced-motion computed state both preferences; heading, landmark and button-name inventory",
  "screenshots artifacts/review-evidence/T-060-accessibility-*.png incl. 08-flags-dark.png; source inspected at HEAD with git show (line numbers cited)"],
 "verdict": "fail",
 "scores": {"keyboard_operability": 3, "focus_order_and_visibility": 2, "names_roles_states": 3, "status_announcements": 3, "contrast_light": 5, "contrast_dark": 1, "target_size": 5, "reflow_320": 5, "reduced_motion": 4, "landmarks_headings": 3},
 "findings": [
  {"severity": "blocker", "title": "Single-key shortcuts act outside the focused item; Shift+A accepts all 9 verified entries from Export focus",
   "evidence": "keyboard results key_shift_a_with_focus_on_export={accepted_before:0, accepted_after:9}; key_j_with_focus_on_export={moved_to_item:true, after:a2}; key_p_with_focus_on_export_1280 focus -> sbs-body; code app/frontend/batch.js:98, app/frontend/review.js:290, app/frontend/sidebyside.js:102 (HEAD f187a30)",
   "why_it_matters": "WCAG 2.1.4 (Level A): letter-key shortcuts must be turned off, remapped or active only when their component has focus; here j/k/p/Shift+A are global. One stray keystroke from an unrelated control accepts every verified entry into the letter path with no confirmation (unsafe, D.2).",
   "fix": "Remove the document-level j/k/p and Shift+A listeners or scope them to elements carrying data-item-id (review.js:290 must not run without an item target). Keep batch accept as a button with a confirmation. If shortcuts stay, add a setting to turn them off.",
   "acceptance_test": "Playwright: focus btn-export; press j, p, Shift+A; focus unchanged and accepted count stays 0. Focus an entry row; a, d, e still act on that entry."},
  {"severity": "major", "title": "Dark theme: review headings, helper text and AI-check titles at 1.11:1 to 2.77:1; Export button 2.14:1",
   "evidence": "computed: h2#rv-flags-h 'Flags' rgb(28,36,48) on rgb(23,26,33) = 1.11:1; 80 dark text nodes below threshold in queue; axe color-contrast serious 38 nodes (dark queue/flags/charges/export/side-by-side); light 0. Root: app/frontend/review.css:3 (--rv-ink #1c2430 on :root, no dark value), review.css:7 (.rv-panel color), styles.css:21 (.btn.primary color #fff on dark accent #8fb0ff from styles.css:3). Screenshot artifacts/review-evidence/T-060-accessibility-08-flags-dark.png",
   "why_it_matters": "WCAG 1.4.3 (AA). Group headings (Treatment gaps, Causation language, Charges, Audit) and helper text are how the paralegal navigates the flags and charges in dark mode; the card AC4 requires AA contrast in both themes.",
   "fix": "Add dark values in review.css for --rv-ink #E7EAEF, --rv-muted #B0B9C6 (8.8:1 on panel), --rv-bg, --rv-soft, --rv-line using the same prefers-color-scheme and :root[data-theme=dark] pattern as styles.css:3. Dark primary button text #0E1116 on #8FB0FF (about 8.8:1).",
   "acceptance_test": "Rerun T-060-accessibility-focus-contrast.py and T-060-accessibility-audit.py: in dark, 0 text nodes below 4.5:1 (3:1 large) in queue, flags, charges, export and AI-check states; axe color-contrast 0."},
  {"severity": "major", "title": "Dark theme: focus rings 2.73:1 on 94 of 160 tab stops",
   "evidence": "focus|dark in T-060-accessibility-focus-contrast-results.json: outline rgb(11,87,208) on rgb(23,26,33) = 2.73:1; failing controls: case-switcher buttons (28), rv-btn accept/edit/dismiss/audit (36), library buttons (15). Cause app/frontend/review.css:5 (--rv-focus #0b57d0, no dark value) applied at review.css:19. Light minimum 5.9:1 over 160 stops",
   "why_it_matters": "WCAG 1.4.11 (AA) focus indicator needs 3:1; in dark mode most controls lose a visible keyboard focus ring.",
   "fix": "Set --rv-focus #8FB0FF in the dark block (8.1:1 on #171A21).",
   "acceptance_test": "Dark Tab walk from queue top, 160 stops: minimum outline contrast at least 3.0."},
  {"severity": "major", "title": "Paste textarea and Order select: control boundaries 1.40:1 light, 1.36:1 dark",
   "evidence": "boundary-empty: textarea[data-testid=input-text] border rgb(213,218,226) on white = 1.40:1; select[data-testid=sort] same (boundary|light 1.4). Cause app/frontend/styles.css:17 (textarea border var(--line)) and styles.css:32 (select border var(--line)). Edit textarea edit-summary 3.00:1 light (passes at the limit)",
   "why_it_matters": "WCAG 1.4.11 (AA): the paste box is the first control of the flow and has no other visible edge.",
   "fix": "Use --border-strong (#6F7B8B light, #7A8696 dark; 4.3:1 and 4.7:1 on panels per brief) for textarea, select and text input borders.",
   "acceptance_test": "Boundary check at least 3:1 for every textarea, select and text input in both themes."},
  {"severity": "major", "title": "Export: focus stays on the Export button, now off screen; Copy letter is 231 Tab presses away",
   "evidence": "keyboard results focus_after_export_open = {testid: btn-export, rect: [188, -9159, 80, 44]} at 1280x900; tab_to_copy_letter presses = 231. Cause app/frontend/export.js:48 scrolls #view-export into view without moving focus",
   "why_it_matters": "WCAG 2.4.3 (focus order) and 2.4.7 (focus visible): focus lands on an element the sighted keyboard user cannot see, and the export block is not reachable in a sensible number of steps.",
   "fix": "After render in load() (export.js:48 scroll branch), focus the export heading container (tabindex=-1) or the first control.",
   "acceptance_test": "After Enter on btn-export, document.activeElement is inside #view-export and within the viewport; Tab reaches btn-copy-letter within 3 presses."},
  {"severity": "major", "title": "Focus lost to the document after 'Copy anyway'",
   "evidence": "app/frontend/export.js:23 onclick box.hidden = true; then(); hides the focused button; dialogs results copy_anyway_focus = BODY. Copy itself works: with clipboard permission the status reads 'Copied the treatment section.' in role=status",
   "why_it_matters": "WCAG 2.4.3 (focus order, AA): after completing a must-have action the keyboard user is dropped at the top of the document.",
   "fix": "After hiding the confirmation, focus #export-status (tabindex=-1) or the Copy letter button.",
   "acceptance_test": "After Copy anyway, document.activeElement is the Copy letter button or the status element; status text 'Copied the treatment section.'."},
  {"severity": "major", "title": "Repeated generic button names: nine 'Why?', nine 'Open record', nine 'Change quote'; Accept names lack the date",
   "evidence": "button_inventory in T-060-accessibility-audit-results.json; app/frontend/timeline.js:31 (entry-why 'Why?'), timeline.js:32 (btn-source 'Open record'), app/frontend/review.js:217 and :221 (aria-label 'Accept: <provider>' with no date, e.g. 'Accept: Capital PT, initial evaluation')",
   "why_it_matters": "WCAG 2.4.6 (AA) labels must describe purpose; 4.1.2 supporting. In a rotor or voice list, identical names cannot be told apart; checklist item 9 asks for the entry in the name.",
   "fix": "Add context to aria-label: 'Why? Austin EMS run report, 2026-01-09'; 'Open record 2 for Central ER discharge summary'; 'Accept: Capital PT, initial evaluation, 2026-01-23'.",
   "acceptance_test": "Every visible queue button's accessible name includes provider and date; no two visible buttons share a name."},
  {"severity": "minor", "title": "Live region created lazily; count-line status node replaced on every render",
   "evidence": "app/frontend/review.js:55 creates #rv-live on first decision; keyboard results live_region_in_dom_at_load=false; app/frontend/export.js:33 count-line role=status; dialogs results count_line_node_replaced_by_decision same=false after an accept. DOM inspection only",
   "why_it_matters": "WCAG 4.1.3: a live region inserted with its first message is not reliably announced, and replaced nodes drop announcements.",
   "fix": "Render <div id=rv-live role=status aria-live=polite class=sr> once in index.html; keep the count-line node and update its text.",
   "acceptance_test": "#rv-live exists before any action; count-line identity preserved across a decision. Confirm announcements with VoiceOver or NVDA."},
  {"severity": "minor", "title": "Refused edit: textarea not linked to its error (no aria-invalid, no aria-describedby)",
   "evidence": "keyboard results refused_edit_entry2: error text in .rv-error role=alert ('The summary has a number, date or dollar figure that is not in the quote: 2031, 99. ...'), textarea_described_by={describedby:null, invalid:null}; code app/frontend/review.js:128,134",
   "why_it_matters": "WCAG 3.3.1 and 3.3.3 are met by text; checklist item 12 association is not (error must be associated with its field).",
   "fix": "aria-invalid=true and aria-describedby pointing at the error element while it is shown.",
   "acceptance_test": "DOM check after a refused edit: textarea has aria-invalid=true and aria-describedby resolving to the error text."},
  {"severity": "minor", "title": "Dismiss-with-reason disclosure does not expose expanded state",
   "evidence": "dialogs results dismiss_reason_button_attrs: expanded=null, controls=null for 'Dismiss with reason...'; app/frontend/review.js:225",
   "why_it_matters": "WCAG 4.1.2: the disclosure's state is not programmatically determined.",
   "fix": "aria-expanded toggled with the reason row and aria-controls pointing at the form.",
   "acceptance_test": "Attribute values change on each activation."},
  {"severity": "minor", "title": "'Browser blocked copying' failure is announced as status, not alert",
   "evidence": "app/frontend/export.js:11 status(msg, bad) sets class error but keeps role=status; dialogs results copy_anyway_status role=status cls=error",
   "why_it_matters": "WCAG 4.1.3: a failed copy should interrupt, as an alert does.",
   "fix": "Set role=alert when bad is true.",
   "acceptance_test": "status(msg, true) renders role=alert."},
  {"severity": "minor", "title": "Landmarks and headings: banner outside landmarks, aside inside main, role=group on articles, judge title not a heading",
   "evidence": "axe best-practice: region (index.html:13 #banner-synthetic, 1 node, moderate), landmark-complementary-is-top-level (sidebyside.js:34 aside in main, moderate), aria-allowed-role (flags.js:64 article role=group, 10 nodes); judges.js:143 aria-labelledby=zj-h on judges.js:146 span",
   "why_it_matters": "WCAG 1.3.1 (structure) and 2.4.1 (landmarks support bypass); the AI-check section cannot be reached by heading navigation.",
   "fix": "Put the banner in a labelled region or header; make the side-by-side pane a section with aria-labelledby; drop role=group from articles; render the judge title as a heading.",
   "acceptance_test": "axe best-practice region, landmark-complementary-is-top-level and aria-allowed-role at 0; heading list includes 'How the AI was checked'."},
  {"severity": "minor", "title": "52 Tab presses to the first Accept; no skip link",
   "evidence": "T-060-accessibility-tabwalk-from-top.json: first btn-accept at stop 52, btn-export at stop 45, 232 stops total; case switcher (6 cases, 15 library buttons) precedes the queue",
   "why_it_matters": "Usability; WCAG 2.4.1 is met by landmarks, but the T-046 note and brief section 9 ask for skip links.",
   "fix": "'Skip to review queue' as the first focusable element; collapse the library list by default.",
   "acceptance_test": "First Tab shows the skip link; Enter lands on the first needs-review row."},
  {"severity": "minor", "title": "Each timeline row is a tab stop and also holds 4 to 5 buttons",
   "evidence": "app/frontend/review.js:322 sets tabindex=0 on each entry article; tab walk shows row stop (e.g. stop 48) followed by btn-accept (stop 52)",
   "why_it_matters": "Checklist item 7 (APG composite pattern): two stops per entry, plus j/k arrow model, is a mix rather than one model.",
   "fix": "Pick one: roving tabindex across the queue, or remove the row tabindex.",
   "acceptance_test": "One tab stop per entry, or the chosen pattern documented."},
  {"severity": "minor", "title": "Enter on Accept and the 'a' key move focus differently",
   "evidence": "keyboard results focus_after_enter_accept_button_2 = same button e2 pressed=true; focus_after_key_a_on_row_4 = next row (tr amount-$185); brief section 9 says Accept advances",
   "why_it_matters": "Checklist item 6: focus after accept should be predictable and the same on every path.",
   "fix": "One behaviour for both paths (advance to next pending item).",
   "acceptance_test": "Enter and a on the same item leave focus on the same next item."},
  {"severity": "nit", "title": "Source-record modal has one focusable element; Tab alternates with browser chrome",
   "evidence": "debug run: Tab moves Close -> document (BODY) -> Close; app/frontend/source.js:30 showModal",
   "why_it_matters": "Standard for a modal with one focusable; not a trap. A longer record may need a keyboard-reachable scroll region (not tested with long records).",
   "fix": "None required now; check scroll-region focusability when long records are used.",
   "acceptance_test": "Load a record longer than the dialog and confirm the text region is keyboard reachable."}
 ],
 "whats_right": [
  "Light theme: zero serious or critical axe violations in 13 states; 0 of 711 light queue text nodes below threshold; focus rings at least 5.9:1 on 160 stops.",
  "Keyboard flow completes: Accept and Dismiss announce 'Accepted: Austin EMS run report. 22 left to review.' in role=status; Edit focus, Escape return, and refused-edit alert all behave; Why?, source and audit dialogs return focus to their opener.",
  "Reflow and targets: no horizontal overflow at 320 CSS px in 7 states; 0 controls under 24x24 CSS px at 1280 or 375; no stop hidden under the sticky banner; no motion in the queue under either motion setting."
 ],
 "questions_for_chris": [
  "Should batch accept ('Accept all verified entries', Shift+A) exist at all? D-011 cut it, and T-055/D-031 seems to reinstate it. The keyboard fix for B1 depends on the answer; the accessibility rule (no global letter shortcut) applies either way."
 ]}
```
