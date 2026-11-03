# T-060 pass 2: accessibility review (WCAG 2.2 AA)

Reviewer: accessibility-reviewer (model claude-haiku-5-5, as run). Date 2026-11-02. Review only; no product code changed.
Verdict: **changes**. No blockers. Four majors: a shortcut sheet that prints `[object HTMLElement]` (serious axe), a 320 CSS px reflow failure with Case checks open, a theme toggle whose accessible name contradicts its state, and an invisible focus stop on the file upload.

## Summary

Pass-1 blocker B1 is fixed. Every pass-1 dark-theme, focus-ring, input-boundary, Export-focus, Copy-anyway and error-association finding is fixed. The keyboard journey completes end to end without a mouse. Live announcements are present and their DOM nodes are stable.

What is still open: one serious axe violation (the shortcut sheet), reflow at 320 CSS px once the case-check chips are expanded, a stale theme-toggle name, and a focus stop that the sighted keyboard user cannot see on the Upload control. Several pass-1 minors are partial.

Screen reader: not available. Announcements were checked by DOM inspection only (`role`, `aria-live`, text and node identity before and after each action).

## Scope and method

- Commit audited: `b89b9d9401bbf03c01b089de5b8e26335ad7e84f` (HEAD). `git diff --quiet 9fcae9b HEAD -- app/frontend` is empty, so the audited frontend is the one that landed in 3e3f3b7, eabe2b8 and 9fcae9b. `git status --short app/frontend` was clean. Uncommitted edits in `app/backend` and other paths were not audited.
- Extracted with `git archive` into the scratchpad; served on http://127.0.0.1:7894 (`ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated`, DB in the scratchpad). Listener PID 80055, stopped at the end of this run.
- axe-core 4.10.3 (same pinned file as pass 1, sha256 880970c0...). Tags: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice.
- Synthetic sample only (`evals/golden` sample, 9 records).

**Harness correction disclosed.** Pass 1's Tab walk used `blur()` to reset the start point. That does not reset Chromium's sequential focus starting point, so the pass-1 walk began after the skip links and header controls. The pass-1 counts (232 stops, Export at stop 45, first Accept at stop 52) are therefore not reproducible as written. This pass resets the start with `documentElement.focus()` and re-measures every pass-1 item it touches. No verdict changes because of this.

## Pass-1 status

| Pass-1 id | Sev | Status | Evidence (this pass) |
|---|---|---|---|
| B1 single-key shortcuts | blocker | **fixed** | From Export focus, `j k p Shift+A a d e r o ?` change nothing (`s_from_export_focus`, all `states_changed: false`). From a row, Shift+A opens `batch-confirm` titled "Accept 9 verified entries?" with Cancel focused (`s_shift_a_row`). Row keys work: j to e2, k to e1, e opens edit, d dismisses e1 with "Dismissed: ..." in `rv-live` (row-keys probe). |
| M1 dark text contrast | major | **fixed** | Dark queue: 797 text nodes, 0 below 4.5:1, lowest 6.41:1. Dark flags heading 15.68:1 (was 1.11:1). Export 9.05:1 (was 2.14:1). axe color-contrast 0 in all dark states. |
| M2 dark focus rings | major | **fixed** | Dark Tab walk, 204 stops: minimum 7.0:1. Light: 5.51:1. |
| M3 input boundaries | major | **fixed** | Paste textarea 4.3:1 light, 4.73:1 dark. Order select 4.3 / 4.73. Config inputs 4.3 / 4.73. Every boundary checked is at or above 3:1. |
| M4 Export focus | major | **fixed** | After Enter on Export, focus is the Export heading inside `#view-export`, in the viewport. Copy letter is 1 Tab away. |
| M5 Copy anyway focus | major | **fixed** | After Copy anyway, focus is on Copy letter. The blocked notice is `role="alert"`. |
| M6 generic button names | major | **partial, now minor** | Timeline names are fixed: "Accept: Austin EMS run report, 2026-01-09", "Open record 1 for ...", "Change quote: ...", "Why this status: ..., date". Still generic on flags and charges: 14 "Why this status" buttons (N-5). |
| m1 live region | minor | **fixed** | `#rv-live` (`role=status`) is in the DOM at load. Same node before and after an accept; `progress-text` also keeps its node. |
| m2 refused edit association | minor | **fixed** | Textarea: `aria-invalid="true"`, `aria-describedby="rv-err-e2"`, and that element is a visible `role="alert"` with the refusal text. |
| m3 dismiss-with-reason | minor | **partial** | `aria-expanded` now toggles "false" to "true". `aria-controls` is still absent (N-6). |
| m4 blocked copy alert | minor | **fixed** | Blocked-copy message is `role="alert"`, class `error`. |
| m5 landmarks and headings | minor | **partial** | Banner is a named region. Judge title is an H3. Article `role="group"` removed. New `landmark-unique` finding (N-7). |
| m6 skip links | minor | **partial** | Four skip links exist and Enter moves focus to a real item each time. Their `href` targets do not exist, so axe `skip-link` fails in every queue state (N-8). |
| m7 row tab stops | minor | **open** | Each row article is a Tab stop (`tabindex="0"`, review.js:349), followed by its 4 to 5 buttons (N-9). |
| m8 Enter vs a | minor | **fixed** | Enter on Accept (e1) and `a` on row 4 both move focus to the next needs-review item, `flag-f_r7_1`. |
| n1 source dialog Tab | nit | open, unchanged | Tab alternates Close and browser chrome. Not a trap (N-15). |

## New and open findings

### Major

**N-1. Shortcut sheet prints `[object HTMLElement]` instead of key names. Serious axe `definition-list` in both themes.** (SC 1.3.1, 4.1.2; checklist item 20)
- Evidence: `review.js:296` (b89b9d9): `el("dl", { class: "kv kv--keys" }, KEYS.map(([k, v]) => [el("dt", {}, el("kbd", {}, k)), el("dd", {}, v)]))`. The mapped pairs are nested arrays, so the helper stringifies them. Details JSON: `sheet_has_object_html_text: true`, `sheet_kbd_count: 0`. Screenshot `artifacts/review-evidence/T-060-accessibility-pass2-details-shortcut-sheet-light.png` shows repeated "[object HTMLElement]" in place of the key list. axe `10-shortcuts-sheet|light` and `|dark`: `definition-list`, serious, 1 node (`.kv--keys`).
- Why it matters: this is the only in-app key reference. A screen reader user hears "[object HTMLElement]" repeated, and a sighted user sees no keys. It is the one serious axe violation in the audited states.
- Fix: flatten the pairs: `KEYS.flatMap(([k, v]) => [el("dt", {}, el("kbd", {}, k)), el("dd", {}, v)])`.
- Acceptance test: open the sheet; it contains 9 `kbd` elements and no text "[object"; axe `definition-list` count 0 in light and dark.

**N-2. At 320 CSS px, with Case checks expanded, the page scrolls sideways. Two chips cannot wrap.** (SC 1.4.10 Reflow, AA)
- Evidence: `T-060-accessibility-pass2-reflow-probe.json`: `collapsed_case_checks.scrollWidth` 320; `expanded_case_checks.scrollWidth` 370 (`horizontal_overflow: true`). `T-060-accessibility-pass2-reflow-check2.json`: the chips' ancestor `details.zs-case-det` goes from `open: false` to `open: true`, and `scrollWidth` goes 320 to 370. Chips "kinds: gap 1, conflict 2, pre existing 2, causation 5" (right edge 363 px) and "found by: code 3, phrase list and AI 6, phrase list 1" (366 px). Screenshot `T-060-accessibility-pass2-reflow-320-chip-clip.png`: the sticky header and chip text are cut at the right edge.
- Cause: `styles.css:81-82` gives `.zs-chip` `display: inline-flex` and `white-space: nowrap`; chips are built at `stepper.js:503`.
- Why it matters: the audit at 320 px with Case checks collapsed showed no overflow, so this would not have been seen by default. Once a paralegal opens the case checks, the chip text is cut and 2-D scrolling is needed.
- Fix: let `.zs-chip` wrap (`white-space: normal`, `max-width: 100%`, wrapping flex row).
- Acceptance test: at 320x640 with the case checks open, `document.documentElement.scrollWidth` equals 320 and no `.zs-chip` has a right edge beyond 320.

**N-3. Theme toggle accessible name is fixed at "Colour theme: automatic" and contradicts the visible state.** (SC 4.1.2 name and value, Level A; SC 2.5.3 Label in Name, Level A)
- Evidence: `index.html:31`: `aria-label="Colour theme: automatic. Press to change."`. `app.js:40` changes only `textContent` ("Theme: " + t) and `data-theme-choice`. Keyboard run `k_theme_name_after_2`: visible text "Theme: dark", accessible name "Colour theme: automatic. Press to change.". Theme probe, both forced cases: the same stale name.
- Why it matters: a screen reader user toggling to dark hears "automatic". The name states a wrong value, and the visible label is not contained in the name.
- Fix: update `aria-label` in `app.js:40` on every change (e.g. "Colour theme: dark. Press to change."), or drop the `aria-label` and let the visible text be the name.
- Acceptance test: after each press, the accessible name contains the visible text and the current theme. Repeat for auto, light and dark.

**N-4. Upload control: the focusable file input is 1x1 px and clipped, so its Tab stop shows no focus indicator.** (SC 2.4.7 Focus Visible, AA)
- Evidence: `input.js:53` `el("label", { class: "btn", for: "file" }, "Upload .txt")` is the visible control and is not focusable (`tabIndex` -1, `T-060-accessibility-pass2-file-probe.json`). `input.js:54` `class: "sr"` on the input. Probe: presses to the input from the top = 4; `file_input_box` `w 1, h 1, clip rect(0,0,0,0)`; `labels: ["Upload .txt"]`. Crop `T-060-accessibility-pass2-file-focus-shot.png`: at the file-input stop, no ring on "Upload .txt".
- Accessible name is fine (the label is associated). Operation by Space or Enter opening the file chooser was not tested.
- Why it matters: a keyboard user Tabs to an invisible stop between Analyze and "Use the sample case".
- Fix: keep the input focusable and draw the ring on the label (`#file:focus-visible + label` with the 2 px accent outline), or make the label a real button that calls `input.click()`.
- Acceptance test: Tab from Analyze reaches a control that shows a 2 px ring with at least 3:1 contrast on "Upload .txt"; Enter or Space opens the file chooser.

### Minor

**N-5. 14 "Why this status" buttons on flags and charges have no context in their names.** (SC 2.4.6, 4.1.2; carries pass-1 M6)
- Evidence: `flags.js:65`, `charges.js:72` call `stepper.js:457` `traceButton`, which sets no `aria-label`. Button list: 10 flag cards and 4 charge rows, each named "Why this status" (`T-060-accessibility-pass2-details.json` `why_status_buttons`, `container: btn-trace`).
- Fix: `aria-label` "Why this status: <flag or charge title>" in `traceButton` (pass `id` through to the title).
- Acceptance test: every visible "Why this status" button name includes its item title; no two visible buttons share a name.

**N-6. Dismiss-with-reason: `aria-expanded` now toggles, but there is no `aria-controls`.** (SC 4.1.2; carries pass-1 m3)
- Evidence: `review.js:235` sets `aria-expanded`. Keyboard run: `expanded: "false"` then `"true"`. `aria-controls` is null before and after. The reason input has `aria-label` but no `id` (`j_dismiss_reason_input_labelled`).
- Fix: give the input an id and set `aria-controls` to it while the row is open.
- Acceptance test: after Enter on the button, `aria-controls` equals the input's id, and the input exists.

**N-7. `landmark-unique`: the side-by-side pane and its region are both named "Source record".** (SC 1.3.1; axe moderate)
- Evidence: `sidebyside.js:34` `section.sbs-pane` with `aria-labelledby="sbs-title"` and `sidebyside.js:32` `div.sbs-body` with `role="region"` and `aria-labelledby="sbs-title"`. Axe `landmark-unique` on `.sbs-pane` in 16 of 18 states.
- Fix: label the region differently ("Source record preview") or drop `role="region"` from `.sbs-body`.
- Acceptance test: axe `landmark-unique` count 0.

**N-8. Skip-link targets do not exist in the DOM. Axe `skip-link` fails in every queue state.** (SC 2.4.1; carries pass-1 m6)
- Evidence: `app.js:66` builds `href="#review"`, `#flags`, `#charges`, `#export`. None of those ids exists (`skip_targets_exist`, all false). Activation works only because `onclick` calls `preventDefault()` and moves focus (`skip_activation`: each Enter lands on a real item). Axe `skip-link` (moderate) in 11 queue states.
- Fix: give each target a real id (`review`, `flags`, `charges`, `export`) on the section it should land on, or point `href` at the focus target that the handler uses.
- Acceptance test: every `#skip-nav a` href resolves to an element in the DOM; axe `skip-link` count 0.

**N-9. Each timeline row is a Tab stop and also holds 4 to 5 buttons.** (APG composite pattern; carries pass-1 m7, open)
- Evidence: `review.js:349` sets `tabindex="0"` on each row article. Tab walk from the top, 1280 px light: 19 article stops, each followed by its own buttons (stops 20, 28, 36, ...; `walk_1280|light`).
- Fix: one model. Either a roving tabindex across the queue with j/k as the arrow model, or remove the row tabindex and keep the buttons as the only stops.
- Acceptance test: one Tab stop per row, or the chosen pattern documented on the card.

**N-10. Edit textarea name drops the visible label guidance.** (SC 2.5.3 Label in Name, Level A; SC 3.3.2 instructions)
- Evidence: `review.js:252` `aria-label: "Summary wording"` overrides the visible label at `review.js:260`: "Summary wording (the quoted excerpt, date and provider cannot be changed)". `aria-describedby` is not set. Same pattern for the flag note: "Reviewer note (...)" against "Your note (...)". Keyboard run `j_edit_textarea_attrs`.
- Why it matters: the rule that the quote and date cannot change is announced by no one until a refusal.
- Fix: remove `aria-label` and let the label set the name, or set `aria-describedby` to a hint element with the rule.
- Acceptance test: textarea name contains the visible label text, or the rule is exposed via `aria-describedby`.

### Nit

**N-11. Focus after Accept or Dismiss goes to the next needs-review item in Flags, and the announcement does not say where.** (checklist item 6, predictability)
- Evidence: Accept e1 moves focus to `flag-f_r7_1` ("Accident date source"), far down the page. The announcement is "Accepted: Austin EMS run report, 2026-01-09. 22 left to review." The rule is documented in the shortcut sheet.
- Fix (optional): append the destination to the announcement, or keep focus in the timeline. Product choice; see questions.

**N-12. Two polite status regions update on each decision.** `rv-live` and `progress-text` both change on one Accept ("1 of 23 decided"). Screen readers may read both. Consider one region for the decision and leave the progress count silent or on a separate cadence.

**N-13. At 320 CSS px, two stops are partly under the sticky header.** `flag-f_accident_date_after_treatment_1_2_7` (3 of 9 sample points visible) and `flag-f_cx1` (6 of 9). No stop is entirely hidden, so SC 2.4.11 (AA) passes. Adding `scroll-padding-top` to the header height would remove the partial overlap. Reflow walk: `T-060-accessibility-pass2-keyboard-results.json` `walk_320|light`.

**N-14. Twelve "Technical details" summaries share one name.** (SC 2.4.6; nit)
- Evidence: `judges.js:72`, `judges.js:178`; 12 visible summaries named "Technical details".
- Fix: name each with its item, or leave as is if the summary sits under a labelled heading.

**N-15. Source record dialog: Tab goes from Close to browser chrome and back (pass-1 n1, unchanged).** Not a trap. Chromium `showModal` behaviour. A longer record may need a scrollable focusable region; the sample records are short.

## What is right

- B1 is closed: letter keys act only from an item row. Shift+A asks first with the count, Cancel is the default focus, and Enter on OK accepts 9 with "Accepted 9 verified entries. Undo is available." Focus lands on Undo.
- Export and copy: Enter on Export puts focus on the Export heading inside the viewport; Copy letter is one Tab away; the copy success message is `role="status"` ("Copied the treatment section.") and the blocked notice is `role="alert"`.
- Contrast, focus and targets: 0 text nodes below threshold in light or dark across 18 states (queue, flags, charges, export, dialogs, forced themes); 0 control boundaries under 3:1; focus rings at least 5.51:1 (light) and 7.0:1 (dark) over 204 stops; 0 of 411 controls under 24x24 at 1280 px and 0 of 412 at 375 px; reduced motion stops all transitions.

## Not exercised and limits

- No screen reader. Live-region checks are DOM only.
- Undated rows and "Dates to confirm" (none in the sample); excerpt editor; manual entry; PDF and file-chooser operation; library cases beyond the sample; the Undo button's keyboard reach was observed (focus lands on it) but not walked in order.
- Stepper buttons "Go to the first pending item" and "Show this step" were checked for names only, not operated.
- 200% and 400% zoom and Windows high-contrast mode not run; forced-colors not tested.
- This is one review. It does not claim WCAG 2.2 AA conformance for the app; it reports what was tested.

## Questions for Chris

- Should focus after Accept stay in the timeline (next row), or keep the current needs-review-first rule into Flags (N-11)?

```json
{"card": "T-060", "persona": "accessibility-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD b89b9d9401bbf03c01b089de5b8e26335ad7e84f via git archive into the scratchpad; app/frontend identical to 9fcae9b and to commits 3e3f3b7, eabe2b8, 9fcae9b (git diff --quiet 9fcae9b HEAD -- app/frontend clean); uncommitted app/backend edits not audited; app http://127.0.0.1:7894 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated); sample case evals/golden sample (9 synthetic records)",
 "exercised": [
  "axe-core 4.10.3 (pinned, sha256 880970c0...) on 18 states x light and dark: empty, empty-error, queue, edit open, source dialog, Why dialog, audit drawer, flags, charges, shortcut sheet, Shift+A confirm, dismiss-with-reason open, export blocked, export, copy confirm, copy blocked status, side-by-side, case switcher open (artifacts/review-evidence/T-060-accessibility-pass2-audit-results.json and .log)",
  "computed contrast of every visible text node and control boundary per state; minimum values per theme (T-060-accessibility-pass2-contrast-values.json); forced dark on light OS and forced light on dark OS (T-060-accessibility-pass2-theme-probe.json)",
  "keyboard-only walk from the top with reset Tab start: skip links (4), full queue walk 204 stops light and dark, 200 stops at 320x640; focus ring contrast and 3x3 focus visibility per stop (T-060-accessibility-pass2-keyboard-results.json)",
  "keyboard-only sample journey: sample, Analyze, accept e1, dismiss e3, edit e2 with Escape, refused edit with invented numbers and its aria-describedby, source dialog open/Tab/Escape, Why dialog, audit drawer, dismiss-with-reason, Export, Copy letter, Copy anyway (same file)",
  "single-key shortcuts from Export focus (j k p Shift+A a d e r o ?) and from a row (j k e Escape d a); Shift+A confirm by keyboard to Accept 9 (T-060-accessibility-pass2-probe.json, T-060-accessibility-pass2-row-keys-probe.json, keyboard results)",
  "shortcut sheet text and definition-list children (T-060-accessibility-pass2-details.json, details-shortcut-sheet-light.png)",
  "copy success with clipboard permission, export-blocked focus (T-060-accessibility-pass2-copy-probe.json)",
  "reflow at 320 CSS px: empty, queue, edit, export, flags, charges, source dialog; Case checks expanded and collapsed (T-060-accessibility-pass2-reflow-probe.json, reflow-check2.json, reflow-320-chip-clip.png)",
  "file input focus and label association on the empty state (T-060-accessibility-pass2-file-probe.json, file-focus-shot.png)",
  "target sizes at 1280 and 375 (411 and 412 controls); reduced motion both preferences; headings, landmarks, button names and duplicates; html lang and title (audit JSON, theme probe)",
  "source line references read from git show b89b9d9 for every cited file:line"],
 "verdict": "changes",
 "scores": {"keyboard_operability": 4, "focus_order_and_visibility": 3, "names_roles_states": 3, "status_announcements": 4, "contrast_light": 5, "contrast_dark": 5, "target_size": 5, "reflow_320": 2, "reduced_motion": 5, "landmarks_headings": 3, "axe_serious_critical": 3},
 "findings": [
  {"severity": "major", "title": "Shortcut sheet prints [object HTMLElement] instead of key names; serious axe definition-list in light and dark",
   "evidence": "app/frontend/review.js:296 (b89b9d9) el('dl', ..., KEYS.map(([k, v]) => [el('dt',...), el('dd',...)])); T-060-accessibility-pass2-details.json sheet_has_object_html_text=true, sheet_kbd_count=0; screenshot artifacts/review-evidence/T-060-accessibility-pass2-details-shortcut-sheet-light.png; axe 10-shortcuts-sheet definition-list serious in both themes (T-060-accessibility-pass2-audit-results.json)",
   "why_it_matters": "The only in-app key reference reads as '[object HTMLElement]' to screen reader users and shows no keys to sighted users. It is the one serious axe violation in the audited states (checklist item 20).",
   "fix": "Flatten the pairs: KEYS.flatMap(([k, v]) => [el('dt', {}, el('kbd', {}, k)), el('dd', {}, v)]).",
   "acceptance_test": "Open the sheet: 9 kbd elements, no text '[object'; axe definition-list count 0 in light and dark."},
  {"severity": "major", "title": "At 320 CSS px with Case checks expanded the page scrolls sideways (scrollWidth 370); two chips cannot wrap",
   "evidence": "T-060-accessibility-pass2-reflow-probe.json expanded_case_checks.scrollWidth=370 vs collapsed 320; T-060-accessibility-pass2-reflow-check2.json details.zs-case-det open false->true; chips right edge 363 and 366 px; screenshot artifacts/review-evidence/T-060-accessibility-pass2-reflow-320-chip-clip.png; styles.css:81-82 (.zs-chip inline-flex, white-space: nowrap); stepper.js:503",
   "why_it_matters": "SC 1.4.10 (AA). Once the paralegal opens the case checks the chip text is cut at the viewport edge and needs 2-D scrolling. The default collapsed state passes, which is why it was not caught earlier.",
   "fix": "Let .zs-chip wrap: white-space normal, max-width 100%, wrapping flex row.",
   "acceptance_test": "At 320x640 with the case checks open, document.documentElement.scrollWidth = 320 and no .zs-chip right edge beyond 320."},
  {"severity": "major", "title": "Theme toggle accessible name is fixed at 'Colour theme: automatic' and contradicts the visible theme",
   "evidence": "app/frontend/index.html:31 aria-label='Colour theme: automatic. Press to change.'; app/frontend/app.js:40 updates only textContent and data-theme-choice; keyboard run k_theme_name_after_2: text 'Theme: dark', aria 'Colour theme: automatic. Press to change.'; theme probe shows the same stale name in forced dark and forced light",
   "why_it_matters": "SC 4.1.2 (value is wrong for AT users, Level A) and SC 2.5.3 (visible label 'Theme: dark' is not contained in the name, Level A). A screen reader user toggling to dark hears 'automatic'.",
   "fix": "Set aria-label from the current theme in app.js:40 on every change, or drop aria-label so the visible text is the name.",
   "acceptance_test": "After each press (auto, light, dark) the accessible name contains the visible text and the current theme."},
  {"severity": "major", "title": "Upload .txt: the focusable file input is 1x1 px and clipped; its Tab stop has no visible focus indicator",
   "evidence": "app/frontend/input.js:53 label for=file 'Upload .txt' (not focusable); input.js:54 class 'sr' on the input; T-060-accessibility-pass2-file-probe.json: stop 4 from top, box 1x1, clip rect(0,0,0,0), labels ['Upload .txt']; crop artifacts/review-evidence/T-060-accessibility-pass2-file-focus-shot.png shows no ring at that stop",
   "why_it_matters": "SC 2.4.7 (AA). A keyboard user Tabs to an invisible stop between Analyze and 'Use the sample case'. Accessible name is fine via the label.",
   "fix": "Draw the focus ring on the label (#file:focus-visible + label with 2px accent outline), or make the label a button that calls input.click().",
   "acceptance_test": "Tab from Analyze reaches a control with a visible 2px ring at 3:1 or more on 'Upload .txt'; Enter or Space opens the file chooser."},
  {"severity": "minor", "title": "14 'Why this status' buttons on flags and charges have no context in their names (pass-1 M6 partial)",
   "evidence": "app/frontend/flags.js:65 and charges.js:72 call stepper.js:457 traceButton, which sets no aria-label; T-060-accessibility-pass2-details.json why_status_buttons (container btn-trace)",
   "why_it_matters": "SC 2.4.6 and 4.1.2. In a button list or voice control, 14 identical names cannot be told apart. Timeline entries are fixed.",
   "fix": "aria-label 'Why this status: <item title>' passed through traceButton.",
   "acceptance_test": "Every visible 'Why this status' name includes its item title; no two visible buttons share a name."},
  {"severity": "minor", "title": "Dismiss-with-reason: aria-expanded toggles but aria-controls is missing (pass-1 m3 partial)",
   "evidence": "app/frontend/review.js:235 aria-expanded; keyboard run j_dismiss_reason_attrs_before expanded false, after expanded true, controls null; j_dismiss_reason_input_labelled has no id",
   "why_it_matters": "SC 4.1.2. The disclosure state is exposed but its controlled element is not.",
   "fix": "Give the reason input an id; set aria-controls to it while the row is open.",
   "acceptance_test": "After Enter, aria-controls equals the reason input id and that input exists."},
  {"severity": "minor", "title": "landmark-unique: side-by-side pane and its region are both named 'Source record' (pass-1 m5 partial)",
   "evidence": "app/frontend/sidebyside.js:34 section.sbs-pane aria-labelledby sbs-title; sidebyside.js:32 div.sbs-body role=region aria-labelledby sbs-title; axe landmark-unique moderate in 16 of 18 states",
   "why_it_matters": "SC 1.3.1. Duplicate landmark names make the landmark list ambiguous.",
   "fix": "Label the region differently or drop role=region from .sbs-body.",
   "acceptance_test": "axe landmark-unique count 0."},
  {"severity": "minor", "title": "Skip-link targets (#review, #flags, #charges, #export) do not exist; axe skip-link fails in every queue state (pass-1 m6 partial)",
   "evidence": "app/frontend/app.js:66 href='#'+id with no matching element (T-060-accessibility-pass2-keyboard-results.json skip_targets_exist all false); activation works via onclick preventDefault (skip_activation: each Enter lands on a real item); axe skip-link moderate in 11 queue states",
   "why_it_matters": "SC 2.4.1. Works through the JS handler, but the href targets are dead without it.",
   "fix": "Add real ids (review, flags, charges, export) to the target sections, or point href at the element the handler focuses.",
   "acceptance_test": "Every #skip-nav href resolves in the DOM; axe skip-link count 0."},
  {"severity": "minor", "title": "Each timeline row is a Tab stop and also holds 4 to 5 buttons (pass-1 m7 open)",
   "evidence": "app/frontend/review.js:349 tabindex=0 on each row article; Tab walk 1280 light (T-060-accessibility-pass2-keyboard-results.json walk_1280|light): 19 article stops, each followed by its buttons",
   "why_it_matters": "APG composite pattern: a mix of row stops and button stops, not one model.",
   "fix": "Choose one: roving tabindex across the queue with j/k as the arrow model, or remove the row tabindex.",
   "acceptance_test": "One Tab stop per row, or the chosen pattern documented on the card."},
  {"severity": "minor", "title": "Edit textarea accessible name omits the visible label guidance (SC 2.5.3, Level A)",
   "evidence": "app/frontend/review.js:252 aria-label 'Summary wording' overrides the visible label at review.js:260 'Summary wording (the quoted excerpt, date and provider cannot be changed)'; no aria-describedby (j_edit_textarea_attrs). Same for the flag note at review.js:252 and 260",
   "why_it_matters": "The rule that the quote and date cannot change is not exposed until a refusal happens.",
   "fix": "Let the label set the name, or expose the rule via aria-describedby.",
   "acceptance_test": "Textarea name contains the visible label text, or the rule is exposed through aria-describedby."},
  {"severity": "nit", "title": "Focus after Accept goes to the next needs-review item in Flags; the announcement does not name the destination",
   "evidence": "T-060-accessibility-pass2-keyboard-results.json j_accept_e1: focus flag-f_r7_1 'Accident date source'; live 'Accepted: Austin EMS run report, 2026-01-09. 22 left to review.'",
   "why_it_matters": "Predictable by the documented rule, but the user cannot tell where focus went without looking.",
   "fix": "Optional: add the destination to the announcement, or keep focus in the timeline (product choice).",
   "acceptance_test": "Announcement names the item that now has focus, if the rule is kept."},
  {"severity": "nit", "title": "Two polite status regions update on each decision (rv-live and progress-text)",
   "evidence": "T-060-accessibility-pass2-keyboard-results.json j_accept_e1 live_after: rv-live 'Accepted: ...' and progress-text '1 of 23 decided'",
   "why_it_matters": "Screen readers may read both messages on one action.",
   "fix": "Keep one decision announcement; update the progress count without a second polite announcement.",
   "acceptance_test": "One decision produces one polite announcement."},
  {"severity": "nit", "title": "At 320 CSS px two stops are partly under the sticky header (AA 2.4.11 met)",
   "evidence": "T-060-accessibility-pass2-keyboard-results.json walk_320|light: flag-f_accident_date_after_treatment_1_2_7 (3 of 9 points visible), flag-f_cx1 (6 of 9); entirely_hidden_count 0",
   "why_it_matters": "SC 2.4.11 AA passes (not entirely hidden). Checklist item 5 asks for no overlap at all.",
   "fix": "scroll-padding-top equal to the sticky header height.",
   "acceptance_test": "No focus box intersects the sticky header at 320x640 on the sample walk."},
  {"severity": "nit", "title": "Twelve 'Technical details' summaries share one name",
   "evidence": "app/frontend/judges.js:72 and judges.js:178; 12 visible summaries named 'Technical details' (T-060-accessibility-pass2-details.json technical_details_visible)",
   "why_it_matters": "SC 2.4.6 weak; the summary sits under a heading, so context exists visually.",
   "fix": "Name each with its item, or leave as is.",
   "acceptance_test": "Optional."},
  {"severity": "nit", "title": "Source record dialog: Tab goes from Close to browser chrome and back (pass-1 n1, unchanged)",
   "evidence": "T-060-accessibility-pass2-details.json source_modal_tab_targets: BODY (browser chrome) and Close alternate; no page element receives focus",
   "why_it_matters": "Not a trap; standard showModal behaviour. A long record may need a scrollable focusable region.",
   "fix": "None now; check with a long record.",
   "acceptance_test": "Load a record longer than the dialog and confirm the text region is keyboard reachable."}
 ],
 "whats_right": [
  "B1 closed: letter keys act only from an item row; Shift+A asks first with the count (Cancel focused) and Enter on OK accepts 9 with a role=status message and focus on Undo.",
  "Export and copy: Enter on Export focuses the Export heading in the viewport, Copy letter is one Tab away, copy success is role=status and the blocked notice is role=alert.",
  "Contrast, focus and targets: 0 text nodes below threshold in light or dark, 0 boundaries under 3:1, focus rings 5.51:1 light and 7.0:1 dark over 204 stops, 0 of 411 controls under 24px, reduced motion stops transitions."
 ],
 "questions_for_chris": [
  "Should focus after Accept stay in the timeline (next row), or keep the needs-review-first rule into Flags (finding 11)?"
 ]}
```
