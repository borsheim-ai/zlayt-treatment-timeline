# UI design brief (T-060 pass 1, DRAFT for frontend and the UX reviewer)

Status: draft by researcher; the frontend card T-060 owns implementation and may amend values with a note. Evidence for the choices is in
`research/ui-references.md` (sources actually opened; legal-tech pages are marketing text, so their lessons are marked as inferences there).
Binding product rules this brief must not break: `spec/REQUIREMENTS.md` R-RV-1..9, R-ST-1, R-TL-5; D-001 (adverse facts live in internal notes);
D-010/D-011 (accept / edit / dismiss, nothing accepted by default, no batch accept); D-019 (one total line); D-022 (self-report per quote);
ADR-005/013 (code composes state and flag text; the UI never invents wording).

**Design stance.** A quiet, dense, document-first review tool, closer to a claims workbench than to a marketing page. The reader is a paralegal who must
verify about twenty items against a source record. Everything that helps her check (quote, record, state, who made it) is visible without a click;
everything decorative is removed. No gradients, no emoji, no illustration except empty states, one accent color, status always shown with shape and word.

---

## 1. Type

Font stack: `"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif` (no web-font download; works offline on the demo Space).
Record text and quotes use the same family at the reading size. Money and counts use `font-variant-numeric: tabular-nums`.
Scale follows Fluent 2's web ramp (opened source) with one extra reading size; sizes are `rem` against a 16 px root so user zoom works.

| Token | px / line-height | Weight | Use |
|---|---|---|---|
| `--t-caption` | 12 / 16 | 400 | metadata, record numbers, chip text, helper text |
| `--t-caption-strong` | 12 / 16 | 600 | chip text, column headers (sentence case, no all-caps) |
| `--t-body-sm` | 13 / 18 | 400 | dense table cells, secondary lines |
| `--t-body` | 14 / 20 | 400 | default UI text, summaries |
| `--t-body-strong` | 14 / 20 | 600 | provider label, entry date, button text |
| `--t-read` | 15 / 24 | 400 | source record pane and evidence quotes (long-form reading) |
| `--t-subtitle` | 16 / 22 | 600 | group headers ("Dates to confirm"), card titles |
| `--t-title` | 20 / 26 | 600 | page section titles |
| `--t-page` | 24 / 32 | 600 | case title only |

Rules: max line length for record text 80 characters (`max-width: 80ch`); never below 12 px; no italics for emphasis except the verbatim quote marks;
quotes are set in `--t-read`, not smaller, because verifying is the job.

## 2. Spacing, shape, elevation

4 px base grid. Tokens: `--s-1 4`, `--s-2 8`, `--s-3 12`, `--s-4 16`, `--s-5 24`, `--s-6 32`, `--s-7 48`. Page gutter 16 px at 375 px, 24 px from 768 px.
Radius: 4 px on controls, chips and inputs; 6 px on cards; none on table rows. Borders instead of shadows: 1 px `--border`; one shadow token only for
menus and the record modal (`0 4px 16px rgb(0 0 0 / 0.16)`). No glass, no blur.

## 3. Density

Default is **comfortable**; a header toggle switches to **compact** and is remembered in `localStorage` (wrapped in try/catch; page works without it).
Row heights follow Carbon's scale (opened source: 24/32/40/48/64, 64 only for two-line rows).

| Surface | Comfortable | Compact |
|---|---|---|
| Table row (charges) | 40 px | 32 px |
| Timeline row (two lines: date + provider, summary) | 64 px minimum, grows with text | 52 px minimum |
| Flag card padding | 16 px | 12 px |
| Button / input height | 36 px | 28 px |
| Touch targets at ≤ 768 px | 44 px min, regardless of density | 44 px |

WCAG 2.2 target-size minimum is 24 px (from the standard; not re-opened in this pass); the 44 px touch rule is the stricter project choice.

## 4. Color tokens, light and dark

Tokens live on `:root`; the dark set sits under `@media (prefers-color-scheme: dark)` and `:root[data-theme="dark"]`, with `:root[data-theme="light"]` winning
over the media query. All ratios below were computed with the WCAG relative-luminance formula (script in Appendix A); text pairs must stay ≥ 4.5:1,
non-text boundaries ≥ 3:1 (WCAG 1.4.3 / 1.4.11, thresholds from the opened SC 1.4.3 page and the standard).

| Token | Light | Dark | Role |
|---|---|---|---|
| `--page` | `#F5F6F8` | `#0E1116` | app background |
| `--panel` | `#FFFFFF` | `#151A21` | cards, rows, record pane |
| `--sunken` | `#EDEFF3` | `#1C222B` | table header, code-ish blocks, disabled areas |
| `--border` | `#D5DAE2` | `#2B3340` | decorative separators only |
| `--border-strong` | `#6F7B8B` | `#7A8696` | input, button and chip outlines |
| `--text` | `#14181F` | `#E7EAEF` | primary text |
| `--text-muted` | `#4A5565` | `#B0B9C6` | secondary text |
| `--text-subtle` | `#5B6676` | `#9AA5B4` | tertiary, timestamps |
| `--accent` | `#0B57D0` | `#8AB4FF` | links, primary button, focus ring |
| `--on-accent` | `#FFFFFF` | `#0E1116` | text on primary button |
| `--accent-soft` | `#E6EFFD` | `#16284A` | selected row, info background |
| `--ok` / `--ok-bg` | `#13613A` / `#E3F3E9` | `#7BD6A0` / `#12301F` | verified, accepted |
| `--warn` / `--warn-bg` | `#6B4400` / `#FFF1CC` | `#F2C265` / `#3A2A0A` | needs review, warnings |
| `--bad` / `--bad-bg` | `#8C1D1D` / `#FCE9E8` | `#FF9A92` / `#401A19` | rejected, errors |
| `--info` / `--info-bg` | `#0B4F9E` / `#E6EFFD` | `#9CC2FF` / `#16284A` | info banners, AI-made badge |
| `--mark` | `#FFE27A` | `#6B5800` | highlighted excerpt inside the record |

Measured contrast (WCAG ratio):

| Pair | Light | Dark |
|---|---|---|
| `--text` on `--page` | 16.46 | 15.68 |
| `--text` on `--panel` | 17.79 | 14.49 |
| `--text` on `--sunken` | 15.46 | 13.26 |
| `--text-muted` on `--panel` | 7.56 | 8.82 |
| `--text-muted` on `--sunken` | 6.57 | 8.07 |
| `--text-subtle` on `--panel` | 5.82 | 7.00 |
| `--text-subtle` on `--sunken` | 5.06 | 6.41 |
| `--accent` on `--panel` (links, focus ring) | 6.39 | 8.37 |
| `--on-accent` on `--accent` (primary button) | 6.39 | 9.05 |
| `--accent` on `--accent-soft` | 5.51 | 7.00 |
| `--ok` on `--ok-bg` | 6.53 | 8.15 |
| `--warn` on `--warn-bg` | 7.63 | 8.37 |
| `--bad` on `--bad-bg` | 7.78 | 7.46 |
| `--info` on `--info-bg` | 6.90 | 8.06 |
| `--text` on `--mark` (highlight) | 13.91 | 5.76 |
| `--border-strong` on `--panel` (non-text, needs 3:1) | 4.30 | 4.73 |
| focus ring `--accent` on `--page` | 5.91 | 9.05 |

Rules: status color is never the only signal (section 6); borders that define a control use `--border-strong`; `--border` is only for decoration;
`forced-colors` mode: chips keep their outline and icon, highlight uses `Highlight`/`HighlightText`; `prefers-reduced-motion`: no transitions longer than
0 ms except the skeleton shimmer, which becomes static.

## 5. Layout

- **≥ 1024 px (R-ST-1):** two panes. Left queue 40% (min 420 px), right source record 60%, each scrolls independently. The record pane scrolls to and highlights
  the excerpt of the selected item; it is a `role="region"` labelled "Source record".
- **< 1024 px:** single column; "Open record" opens a modal sheet (focus trapped, `Esc` closes, focus returns to the opener). At 375 px no horizontal scroll;
  the charges table reflows to label/value rows (summary-list pattern).
- **Order in the queue:** `needs_review` first (R-TL-5), then `verified`, within each by date. "Dates to confirm" is its own group after the timeline (R-IN-5).
  Dismissed items collapse under "Dismissed (n)" with a Reset action (R-RV-5).
- **Persistent header strip:** case name, progress ("12 of 20 reviewed", with a text count, not just a bar), density toggle, theme toggle, Export.
- **Charges** are a separate section below flags; totals show `Accepted charges` as the only total (D-019) and `Pending review` / `Detected (not a total)` as labelled secondary figures.

## 6. Status vocabulary (shape + word + color)

Carbon's rule (opened): use at least three of symbol, shape, color and text, never reuse a shape for a different meaning, stay legible in grayscale.

| State | Shape / icon (16 px) | Word | Colors | Meaning |
|---|---|---|---|---|
| `verified` | filled circle with check | Verified | `--ok` on `--ok-bg` | code checks and judge passed; still needs a human decision |
| `needs_review` | triangle with exclamation | Needs review | `--warn` on `--warn-bg` | something failed or is advisory; reason text follows |
| `rejected` | square with cross | Rejected | `--bad` on `--bad-bg` | failed a hard check |
| Accepted (human) | circle with check, outlined, plus "Accepted" | Accepted | `--ok` outline | reviewer decision |
| Edited | pencil | Edited | `--info` | reviewer changed summary text |
| Dismissed | circle with dash | Dismissed | `--text-muted` | reviewer dismissed |
| `AI-made` | rounded rectangle "AI" | AI-made | `--info` on `--info-bg` | origin of the text |
| `Patient self-report` | speech bubble | Patient self-report | `--text-muted` outline | only where code set `source_kind=patient_report` (T-061 narrows this) |

"Verified" is never styled as approval: no green row background, no check on the primary action. Machine verification and human acceptance are two separate chips.

## 7. Components

### 7.1 Timeline row (entry)

Two-line row, 64 px minimum. Structure, left to right:
1. **Rail:** 8 px dot + 1 px line on `--border-strong`; dot shape follows the state shape, so the rail is readable in grayscale.
2. **Line 1:** `--t-body-strong` long date ("January 9, 2026") · provider label exactly as written (D-014) in `--t-body` · record number chip `Rec 2` (`--t-caption`).
   Right side: state chip(s) (section 6), at most two visible, overflow into "+1".
3. **Line 2:** the summary (`--t-body`, up to 3 lines, then "Show more"), followed by the verbatim quote block (7.3), collapsed to one line by default in compact density
   and expanded when the row is selected.
4. **Actions** (right, on hover/focus and always on touch): Accept, Edit, Dismiss as text+icon buttons, `Open record` as a link. Disabled actions stay visible with a
   tooltip reason ("Date needs confirming first").
- Selected row: `--accent-soft` background, 3 px `--accent` left bar, and the record pane scrolls to the excerpt.
- Edited rows show an "Edited" chip and the original summary under a disclosure ("Original").
- An ambiguous-date entry shows "Date to confirm" in place of the date and the allowed readings as radio buttons (`confirm_date`).

### 7.2 Flag card

Card, 6 px radius, 1 px `--border-strong`. No colored top bar: the flag type is a labelled chip with its own shape, so color is not the signal.
- Header: type chip (`Gap`, `Conflict`, `Pre-existing`, `Causation`, `Record warning`) with a distinct shape each, category in `--t-caption`, state chip.
- Title and explanation are the code-rendered template text (ADR-013); the UI renders them as data and never rewrites them. Explanation is `--t-body`, 2-3 lines.
- Evidence: one quote block per cited record (7.3); two-record flags (gap, conflict) show both side by side at ≥ 640 px, stacked below.
- Footer actions: Accept, Dismiss (with optional reason field, R-RV-5), Add note (500 characters, counter at 450+). The note is labeled "Reviewer note".
- Adverse-fact flags (causation, pre-existing) carry the line "Internal notes only. Not in the letter." in `--t-caption` (D-001/D-018).

### 7.3 Evidence quote

The most important component: it is what makes the claim checkable.
- Left border 3 px `--border-strong`, padding 8 px 12 px, `--t-read`, `--panel` background.
- Verbatim text in typographic quotation marks; the cited span is **not** altered, abbreviated or ellipsized by the UI. If it is long, show the whole sentence with a
  fade and "Show full excerpt" (keyboard reachable), never a mid-sentence truncation.
- Footer line `--t-caption`: `Rec 8 · Austin Imaging, cervical MRI · 2026-05-29` and the link `Open in record`.
- Hedge and negation words are not decorated; the highlight is for the excerpt as a whole inside the record pane (`--mark`), exactly the code offsets (R-RV-9).
- If the offset can't be found: the quote shows a `needs_review` chip and the line "The excerpt could not be located in the record." (copy from R-RV-9).

### 7.4 Charges table

Semantic `<table>` with `<caption>` ("Charges detected in the records"). Columns: Description / source (provider, Rec n) · Amount (right-aligned, tabular) · Class · Status · Actions.
- Class is a word chip: Charge, Rate, Estimate, Damages, Unclear. Only Charge rows can be Accepted; other rows show Dismiss and the reason text.
- Amount cell shows the raw string as written in the record; unclear values show the raw text and "value not read" (never a guess).
- Footer (not a body row): `Accepted charges $8,390.00` in `--t-subtitle`; below it `Pending review` and `Detected (not a total)` in `--t-body-sm`. No parenthetical on the total (D-019).
- Row actions have accessible names that include the amount and source ("Dismiss $185 rate from Capital PT, initial evaluation"), after GOV.UK's hidden-text rule.
- At 375 px each row becomes a summary-list block (label / value / action).
- Sorting: by record order by default; amount sortable, arrow shown on the sorted column and on hover for others (Carbon).

### 7.5 Review controls

- **Accept** (primary, `--accent`), **Edit** (secondary, `--border-strong` outline), **Dismiss** (tertiary text button). One primary per row. Nothing is pre-selected (D-010).
- State after action is shown as a chip plus a 4 s inline "Undo" link in the row (not a toast: toasts vanish, Carbon notes about 5 s); Reset stays available until export.
- **Edit** opens inline: textarea (summary only; date/provider/record never editable, R-RV-2), character counter, `Save` / `Cancel`, and the live re-check result ("Checking numbers and dates against the excerpt…", then pass or the code reason).
  Accepting an edit that failed the number check requires the "Keep my wording" confirmation checkbox; its label states what changed.
- **Export** button sits in the header strip. If anything is unreviewed: clicking opens the error-summary pattern (7.6) with links to each open item; it does not export silently, and it
  does not block once the paralegal confirms, because the letter holds accepted items only (R-EX-1) and the internal notes state "Items not reviewed: N" (R-EX-4).
- Buttons: height 36 px (28 compact), 4 px radius, text+icon, never icon-only except Close and the density/theme toggles (which carry `aria-label` and a tooltip).

### 7.6 Banners and messages

Follow Carbon (placement, length) and Fluent (severity order, assertive vs polite). Copy is two lines maximum, title without a final period, one action.

| Kind | Where | Persistence | Announce | Example |
|---|---|---|---|---|
| Error summary (blocked export, failed save) | top of main, below header, focus moves to it | until resolved | `role="alert"` | "There is a problem · 3 items still need review · [Go to first]" with links to each |
| Run warning (e.g. cross-record check did not finish) | inline, top of the queue | persists across reload while true | `role="alert"` for errors/warnings | "Cross-record check did not finish · Conflicts may be missing · [Retry]" |
| Record warning (injection suspected, date ambiguous) | on the affected record header and row | until the item is resolved | `role="status"` | "Text in this record reads like an instruction. Treated as data." |
| Info (demo mode, sample case) | top strip, dismissible | dismissed per session | `role="status"` | "Sample case. Synthetic records." |
| Success after export | inline in header strip | 8 s, then a persistent "Exported at 14:32" label | `role="status"` | "Letter text and internal notes exported" |

Rules: warnings and errors always include an action (Fluent); stacked errors first; dismissed-but-unresolved run warnings return on reload; never a modal for non-destructive messages;
the page `<title>` is prefixed "Error:" while an error summary is shown (GOV.UK).

## 8. States

| Surface | Empty | Loading | Error |
|---|---|---|---|
| Case list / start | "No case yet. Paste records or open the sample case." + two buttons | skeleton card | "Could not load cases. [Retry]" |
| Timeline queue | "Nothing to review. All items are decided." (when finished) / "No entries yet. The records have not been read." | skeleton rows at the real row height (64 px) with a text status "Reading records 4 of 9" (from the API `progress.label`); no spinner-only state | error summary (7.6) with the code reason and Retry; the pasted text is never lost |
| Flags | "No flags raised for this case." (not "No problems found": absence of flags is not a finding) | skeleton cards | "Flag check did not finish. [Retry]" |
| Charges | "No dollar amounts found in the records." | skeleton table rows | "Charges could not be read. [Retry]" |
| Source record pane | "Select an item to see its record." | skeleton lines | "Record could not be shown. [Retry]" |
| Edit re-check | n/a | inline "Checking…" with `aria-live="polite"` | code reason in `--bad`, with the offending number named |

Long operations show a progress count from the API, never a fake percentage. Skeletons are static under `prefers-reduced-motion`.

## 9. Keyboard model

The review is keyboard-drivable end to end (R-RV-4). Shortcuts are single keys and are disabled while focus is in a text field, textarea, select or the edit box.

| Key | Action |
|---|---|
| `↓` / `j`, `↑` / `k` | next / previous item in the queue (roving tabindex; the row is the single tab stop for the list) |
| `n` | next item that is still `needs_review` and undecided (wraps) |
| `a` | accept the focused item |
| `e` | edit the focused item (focus goes to the textarea); `Ctrl/Cmd+Enter` saves, `Esc` cancels |
| `d` | dismiss the focused item (focus lands on the optional reason field for flags) |
| `u` | undo the last decision on the focused item / reset a dismissed one |
| `o` or `Enter` | open the full record (modal below 1024 px; at ≥ 1024 px moves focus to the record pane) |
| `Esc` | close modal / leave edit / return focus from the record pane to the queue row |
| `Tab` / `Shift+Tab` | standard order: header strip → queue → record pane → charges → export |
| `g` then `t` / `f` / `c` | jump to Timeline / Flags / Charges |
| `?` | open the shortcut sheet (a dialog listing this table; `Esc` closes) |

Focus management: after Accept or Dismiss, focus moves to the next undecided `needs_review` row (or the next row if none) and a polite live region says
"Accepted. 12 of 20 reviewed." Closing a modal returns focus to the control that opened it. Visible focus ring everywhere: 2 px `--accent` outline,
2 px offset (6.39:1 light, 9.05:1 dark on the page color). Skip links: "Skip to review queue", "Skip to charges". Tab order never depends on DOM tricks;
`aria-keyshortcuts` is set on the buttons that have a key.

## 10. Content rules for the UI

- Sentence case everywhere; no exclamation marks; no "AI-powered" language; no "oops".
- The UI says what the record says and what the code checked; it never says a record means something. "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient)." is the register.
- Adverse facts appear only in the review UI and internal notes (D-001); the letter preview contains accepted entries and the one total line.
- Numbers are shown as the record wrote them next to any normalized value.

## 11. Open decisions for the frontend / UX reviewer

1. Whether the shortcut sheet and `g`-prefixed jumps ship in M2 or are a stretch (they are cheap; cut order: `g` jumps, then shortcut sheet; core keys `j/k/a/e/d/u/o/n` stay).
2. Accept-and-advance: this brief advances focus automatically (speeds twenty decisions) but a reviewer may prefer staying put; add a header preference only if the UX reviewer asks.
3. Density default: comfortable. Compact is for the power user and the demo video at 1280 px; the UX reviewer may prefer compact as default on desktop.
4. Dark mode is specified and contrast-checked here, but the demo video should be recorded in light mode.

## Appendix A. Contrast check script

```python
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb); return (hi + 0.05) / (lo + 0.05)
# ratio('#14181F', '#FFFFFF') -> 17.79 ; ratio('#13613A', '#E3F3E9') -> 6.53
```
Threshold values come from WCAG 2.2 SC 1.4.3 (opened). Re-run after any token change; a token PR must show the table above regenerated.
