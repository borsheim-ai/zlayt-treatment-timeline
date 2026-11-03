# Guided UI spec (T-180, D-068)

Status: design spec for the guided four-step UI. Owner: frontend. Clickable mockup: `artifacts/mockups/guided/index.html`
(all screens: `artifacts/mockups/guided/screens.html`); screenshots `artifacts/screenshots/guided-mockup-*.png` at 1440x900 and 390x844.
Builds only on `memory/contracts/api.md` as of 2026-11-02 plus the D-066 `compared` field already in `app/backend/review.py` (T-179).
No new backend feature is assumed; where the API lacks something, this spec says what the screen does without it.

Chris's brief: "<Chris's message omitted> someone's <Chris's message omitted>. <Chris's message omitted>."

---

## 0. Rules every screen keeps

| Rule | How |
|---|---|
| Nothing moves when you click | The page is a fixed frame: banner, header, step bar, title row and action bar have fixed heights; only the panes inside scroll. An answer swaps text inside boxes that keep their size. No banner, toast or error is ever inserted above content after load: each has a reserved slot. `scrollbar-gutter: stable`. System fonts only (no font swap). Buttons have fixed widths, so a label change never resizes them. |
| No collapsing, no hidden menus | No `<details>`, accordions, dropdown menus, kebab menus or hover-only content. Every action is a visible button with words on it. |
| No shortcuts required | Everything works with a mouse, a finger, or Tab + Enter. Keyboard shortcuts are not offered in the guided UI. |
| Every screen answers three questions | **Where am I** (step bar + title row), **what do I do now** (one question or one instruction next to the buttons), **how do I know I'm done** (the "N left" count, then a done screen with a big check). |
| One thing at a time | Review pages show one item. The next item appears in the same boxes. |
| Plain words | No "judge", "LLM", "tray", "verified", "flag", "excerpt", "pending". The table in section 10 maps every internal word to the word on screen. Server sentences (`why`, `explanation`, `message`, `not_counted_reason`) are shown as given; the UI never rewrites a fact. |
| Honest | Every answer is saved by the server before the screen says it is saved. Provenance labels follow D-065. |
| Untrusted text | Record text, quotes, summaries and titles are inserted with `textContent` only. |

The old screen moves to `/classic` (D-068) unchanged; its e2e suite keeps guarding behaviour. The guided UI gets its own suite.

## 1. Map of screens and routes

| Route | Screen | Mockup page |
|---|---|---|
| `/` | Your cases | `index.html`, `home-empty.html`, `home-loading.html`, `home-error.html` |
| `/new` | Step 1, before the case exists | `step1-add.html` |
| `/case/<token>/records` | Step 1: records found / drafting / done / stopped | `step1-found.html`, `step1-drafting.html`, `step1-drafting-lib01.html`, `step1-failed.html` |
| `/case/<token>/timeline[?item=<id>]` | Step 2, one item at a time; done screen | `step2-entry.html`, `step2-fix.html`, `step2-flag.html`, `step2-gap.html`, `step2-disputed.html`, `step2-cannot-check.html`, `step2-write.html`, `step2-date.html`, `step2-done.html` |
| `/case/<token>/bills[?item=<id>]` | Step 3, one amount at a time; done screen | `step3-charge.html`, `step3-count.html`, `step3-never.html`, `step3-done.html` |
| `/case/<token>/letter` | Step 4 | `step4-letter.html`, `step4-pending.html`, `step4-blocked.html` |
| `/classic` | the old review screen | (unchanged) |

Routing is `history.pushState` with real URLs, so Back in the browser and a reload both land on the same screen. A reload of
`/case/<token>/timeline?item=e3` reopens that item.

## 2. Global frame

### 2.1 Synthetic banner (every page, fixed, 32 px; 40 px on phones)
Text: `health.banner` ("Synthetic data only — never paste real records"). Warm yellow background, dark text, centred.
On phones the banner also carries the demo label (2.3), so provenance is never off-screen.

### 2.2 Header (every page, fixed, 64 px; 52 px on phones)
- Left: product mark + "Treatment Timeline" (home), or "‹ Your cases" button + case title (inside a case). The title is the API `title`,
  one line, ellipsis. On phones: "‹ Cases" + title.
- Right: the demo label (2.3) on desktop, then a "Dark mode" / "Light mode" text button (theme; default follows the OS; remembered in
  `localStorage` inside try/catch).

### 2.3 Demo provenance (D-065)
`GET /api/health` `answers`:

| `answers` | Label (pill, always visible) | Footer sentence (visible, not a tooltip) | Item tag |
|---|---|---|---|
| `prepared` | Demo: sample answers prepared by our team | The AI's own answers on these cases are in the evaluation report. | "Prepared answer" when `item.prepared`, else "AI draft" |
| `recorded` | Demo: recorded AI answers | These are real AI answers recorded earlier; nothing new is sent to an AI. | "AI draft" |
| `live` | (no pill) | Summaries and warnings are drafted by AI and checked by code; you decide every item. | "AI draft" |

A manual entry (`entered_by_reviewer`) or a summary she wrote is tagged "Written by you". `ai_banner` is shown under the step title on
Steps 2 and 3 (desktop) and on each step's done screen (all widths). Removing jargon never removes provenance.

### 2.4 Step bar (inside a case; fixed, 76 px; 60 px on phones; never moves, never changes height)
Four equal segments joined by a line: **1 Add records · 2 Check the timeline · 3 Check the bills · 4 Get your letter**
(phones: Records · Timeline · Bills · Letter). Each segment: a 32 px circle, the label, one status line.

| State | Circle | Status line | Click |
|---|---|---|---|
| done | green circle with a check | "Done" | opens the step (to look or change answers) |
| current (the step on screen) | filled accent circle (number, or a check when that step is done), accent bar under the segment, bold label, `aria-current="step"` | e.g. "16 of 19 left" | opens the step |
| remaining | grey outline circle with the number | e.g. "4 amounts" / "Not started" | opens the step |
| locked | grey outline, label at 60% | "After step 1" | not clickable (`aria-disabled`) |
| needs attention | amber circle with "!" (a step she left with undecided items, a stopped run, an export problem) | e.g. "Run again" / "2 left" / "1 problem" | opens the step |

Steps 2–4 are locked until the case has items (`status` is `ready`, or `failed` with items; see 4.5). The step bar is a
`<nav aria-label="Steps">` of links. Status lines are computed from GET case (section 9.2), text only, fixed width.

### 2.5 Title row (review pages; fixed, 72 px; 52 px on phones)
Left: eyebrow "Step 2 of 4" and h1 "Check the timeline". Right: "Item 4 of 19" and a progress bar (fixed 240 px; full width on
phones) with "3 answered · 16 to go". Step 3 adds a fixed-width "Bill total so far: $6,240.00" chip (`totals.accepted.cents`).

### 2.6 Action bar (review pages; fixed to the bottom; fixed height)
Three rows, always present, never re-laid out:
1. **The question** (20 px, semibold), max two lines (reserved).
2. **Two big answers**, equal size (56 px tall, 260 px wide on desktop; half width each on phones). The first is filled accent,
   the second outlined. Equal size on purpose: neither is a reflex click.
3. **Small buttons** of one fixed width (172 px; equal thirds on phones): "‹ Back", the item's third action ("Fix the wording" /
   "Add a note"; an invisible placeholder keeps the slot when an item has none, so Back and Decide later never move), "Decide later"; then the
   **status slot** (`aria-live="polite"`, one line, reserved): "Saved: item 3 kept in the letter. Undo".

When an answer is not allowed yet (a confirm box is not ticked, a code check fails), the button stays where it is, disabled, and the
reason is in the item card's footer slot (2.7). Errors from the server go in the same footer slot, never in a new banner.

### 2.7 Item cards (review pages)
Desktop: two columns of equal width inside the work area. **Left: "From the record"** (the source). **Right: the line to check.**
Phones: the source on top (flexible height, scrolls), the line card below it (fixed 180 px, scrolls inside).

- **Source card.** Header: "Record 3 · Dr. Alvarez, primary care · January 16, 2026" (record `seq`, `source_label`, long date).
  Body: the record text at 18 px/1.6 with the quote in a yellow `<mark>` (offsets `excerpt_start/end` into the case text, minus
  `char_start`). On open the card scrolls **inside itself** so the mark is in view; the page never scrolls. Several records (a flag with
  evidence in two records) are stacked in the same card, each with its header. Footer (when `records[].uncovered` is not empty):
  "Also in this record, not in any line:" + each sentence in quotes (read only).
- **Line card.** Header: tag (2.3) and the date + provider. Body: the summary at 22 px. **Footer slot** (fixed min-height 112 px):
  the plain check sentence (`why`), or a confirm checkbox, or a refusal message, or "Your answer: ..." when she comes Back.

### 2.8 Footer (every page)
One line: the provenance sentence (2.3) and, in live mode, "Pasted text is deleted after `retention_hours` hours."

## 3. Your cases (home, `/`)

**Where am I:** h1 "Your cases". **What do I do now:** each card's "Next:" line and its one Continue button. **Done:** a case moves to
"Finished" with a green "Letter ready".

Layout: title row with h1, one sentence ("Each case goes through 4 steps. Pick up where you left off."), and the primary
"Start a new case" button (top right; full width on phones). A "Find a case" search box shows when there are 6 or more cases
(filters by title as she types; the only thing on the page that changes the list, and only on typing). Two sections, always open:
**In progress (N)** and **Finished (N)**. Cards in a grid: 2 columns at ≥ 1100 px, 1 column below. Sorted by `last_activity_at`,
newest first.

### 3.1 Case card (fixed height 236 px desktop; content clamps)
```
Jordan Rivera (sample)                               [Rename]
Started Nov 2 · 9 records
(1)✓ Add records — (2) Check the timeline — (3) Check the bills — (4) Get your letter
Next: Check the timeline. 16 of 19 items left.
[        Continue        ]                          [Delete]
```
- Title: `title` (text only). "Rename" turns the title into an input in the same box with "Save" / "Cancel" (PATCH `{title}`;
  `422 invalid_title` message shown under the input in a reserved line).
- Mini step track: the four steps with the same states as the step bar (2.4), small.
- **Next line** (one rule, section 9.3) and the **Continue** button (one per card, full card width minus Delete).
- "Delete": the card's bottom row turns into "Delete this case and all its answers? [Yes, delete] [Keep it]" in the same row
  (DELETE `/api/cases/{token}`; the card is then removed, which is the one allowed layout change, caused by her own confirm).
- A card whose summary failed (`status_error: true`): body shows `status_error_message` ("We couldn't load this case's status")
  instead of the track and the Next line; button "Open case".

### 3.2 Next line + Continue target (per case)
| Case state | Next line | Continue goes to |
|---|---|---|
| `ingested` (records read, not drafted) | Next: Draft the timeline. | Step 1 (records found) |
| `running` | Next: Wait while the timeline is drafted (stage N of 8). | Step 1 (drafting) |
| `failed` | Next: Drafting stopped. Run it again. | Step 1 (stopped) |
| Step 2 has undecided items | Next: Check the timeline. N of M items left. | first undecided Step 2 item |
| Step 3 has undecided items | Next: Check the bills. N of M amounts left. | first undecided Step 3 item |
| gate blocker on a decided item (`next_action.kind` is entry/flag/amount and that item is decided) | Next: Fix 1 problem before the letter. + `next_action.reason` | that item |
| everything decided, gate ready | Finished. Your letter is ready. (green) | Step 4; button reads "Open letter" |

### 3.3 Multi-case in local and public mode
- Local mode (`ZLAYT_MODE=local`): the list is `GET /api/cases` (every case on this computer).
- Public / demo mode: `GET /api/cases` is `404` by design (no case list; the token is the only credential). The home then lists the
  cases **this browser started**: their tokens are kept in `localStorage` (`zl.guided.cases`, try/catch) when POST `/api/cases`
  answers, and each card is filled from `GET /api/cases/{token}`. A `404` card reads "This case is no longer here. Cases are kept for
  `retention_hours` hours." with "Remove from this list". A line under the h1 says "These are the cases started in this browser.
  Keep the case link to open it elsewhere." No server feature is added.

### 3.4 Home states
| State | Screen |
|---|---|
| Loading | The title row, then 3 grey skeleton cards of the final card size (no jump when they fill). |
| Empty | Large icon, "You don't have any cases yet.", "A case is one client's medical records. We'll guide you through 4 steps.", buttons "Start a new case" and "Try the sample case" (POST `{sample: true}`, then Step 1). |
| Error | "We couldn't load your cases." + the server `message` when there is one + "Try again" (refetch; focus returns to the h1). |

## 4. Step 1 — Add records (`/new`, then `/case/<token>/records`)

**Instruction:** "Add the medical records for this case. We'll read them and draft a timeline for you to check."

### 4.1 Before the case exists (`/new`)
- "Name this case (optional)" text input (sent as `title`; 120 characters max, no `<` `>`; the 422 message shows under it).
- Three big choice tiles, side by side (stacked on phones), each a radio with a picture-free heading and one line:
  **Paste text** ("Copy the records and paste them here") · **Upload a file** (".txt or .pdf, up to 5 MB") ·
  **Use the sample case** ("A short synthetic case to try it out").
- Below the tiles, one fixed-height box (280 px) that shows the chosen input: a textarea, a file drop area with "Choose a file", or
  "The sample has 9 short records from a fictional car-accident case." The box does not change size between choices.
- Primary button: **Read the records** (disabled until there is text, a file, or the sample is chosen).
- Demo mode line (when `health.demo_mode`): "This demo can only read the sample and our test cases."

| Control | API |
|---|---|
| Read the records (paste) | `POST /api/cases {text, title}` |
| Read the records (.txt) | read in the browser, then the same POST |
| Read the records (.pdf) | `POST /api/cases/pdf?title=` raw bytes, `Content-Type: application/pdf` |
| Read the records (sample) | `POST /api/cases {sample: true, title}` |

Errors (shown in a reserved line under the box, plain words, with the action):

| Code | Message on screen | Action |
|---|---|---|
| `400 bad_request` empty | There's nothing to read yet. Paste the records or choose a file. | — |
| `413 input_too_large` | That's more than we can read at once (60,000 characters or 40 records). Split it into two cases. | — |
| `409 demo_mode_unsupported_input` | This demo can only read the sample and our test cases. | "Use the sample case" |
| `400 pdf_no_text_layer` | This PDF looks scanned, so it has no text we can read. | "Read the scanned pages" (re-post with `ocr=true`) when `detail.ocr.status.available` |
| `400 pdf_encrypted` / `pdf_unreadable` / `pdf_timeout` | the server `message` | "Choose another file" |
| `400 pdf_only_hidden_text` | Everything on these pages is hidden text, so we kept it out. | "Use these pages anyway" (re-post `include_hidden=all`, after a confirm checkbox "I looked at these pages myself") |
| `429 busy` | We're reading other files right now. Try again in a moment. | "Try again" |
| network / 5xx | We couldn't reach the server. Your text is still here. | "Try again" |

### 4.2 Records found (`status: ingested`)
Heading "We found 9 records". A fixed list (scrolls inside its box) of rows: "1 · January 9, 2026 · Austin EMS run report".
Plain notes above the list in a reserved slot, from the POST/GET response:
- `dates_to_confirm` not empty: "1 record has a date we need you to check. You'll do that in step 2."
- warning `PHI_PATTERN`: "Some text looks like real personal details (a phone, SSN or record number). Only use synthetic records."
- warning `SPLIT_AMBIGUOUS` / `UNSPLIT_TEXT`: "Some text didn't look like a record. We kept it as its own record so nothing is lost."
- `injection.banner`: shown as given.
Primary: **Draft the timeline** → `POST /api/cases/{token}/run {confirm_rerun: false}`. Secondary: "Start over with other records" (`/new`).

### 4.3 Drafting (`status: running`)
Poll `GET /api/cases/{token}/status` every second. A fixed checklist of the 8 stages (never the raw stage id or `progress.label`,
which contains ids). Done stages get a green check, the current one a spinner and "(4 of 9)" from `progress.done/total` when the stage
counts items, the rest are grey. A progress bar above shows stages done / 8. Copy:

| `stage` | Live / recorded | Prepared (`answers: prepared`) |
|---|---|---|
| `ingest` | Reading the records | Reading the records |
| `extract` | Writing one line for each record | Loading the prepared line for each record |
| `verify` | Checking every quote word for word | Checking every quote word for word |
| `judge_entries` | Double-checking each line a second way | Double-checking each line a second way |
| `amounts` | Finding the bill amounts | Finding the bill amounts |
| `conflicts` | Comparing the records with each other | Comparing the records with each other |
| `flags` | Looking for things the attorney should know | Looking for things the attorney should know |
| `finalize` | Putting it all together | Putting it all together |

Under the list: "This usually takes under a minute. You can leave this page; we'll keep going." (Home shows the same progress.)

### 4.4 Done (`status: ready`)
The same box shows a big green check: "All set. 19 timeline items and 4 bill amounts are ready for you to check." (counts from
`status.counts`, entries + flags, amounts) + the `ai_banner` sentence + primary **Go to step 2: Check the timeline**. Step 1 turns done.

### 4.5 Stopped (`status: failed`)
Amber box: "Drafting stopped before it finished." + `error.message` as given (it already says decisions were kept) + **Run it again**
→ `POST .../run {confirm_rerun: false}`; on `409 needs_confirm` the same box shows "Run it again? Your answers so far are kept." with
**Yes, run it again** (`confirm_rerun: true`) / **Cancel**. Items the run did finish can be checked meanwhile: steps 2–3 open.
`error.records` (extract failures) are named: "No line was written for records 2 and 7. You can write them yourself in step 2."

After a case is drafted, Step 1 shows the records list read-only with "To add more records, start a new case." (There is no API to add
records to a case.)

## 5. Step 2 — Check the timeline (`/case/<token>/timeline`)

### 5.1 The queue
Built in the browser from one `GET /api/cases/{token}`, once, when the step opens; it never re-sorts while she works.
Contents: every entry in `entries` and `undated_entries`, every flag in `flags`, every `tray` item (could not check). Not included:
`tray_filtered` (listed read-only on the done screen), amounts (Step 3). Order: the `next_action` timeline rule (api.md, T-157 step 3):
by the date of the record the item cites (earliest when several; undated last), then that record's position, then entry before flag,
then id. So a flag sits right after the line it is about. Sample case: 9 lines + 10 warnings = 19 items.

Opening the step lands on the first undecided item (or `?item=`). After an answer the next undecided item opens in the same boxes.
"‹ Back" opens the previous item (decided or not). "Decide later" moves on without saving. When no undecided item is left, the done
screen (5.8) opens.

Every write sends `version` and `expected_status` from the item on screen (T-178). On `409 stale_item`: footer slot shows "This item
changed in another tab. We've loaded the latest." and the item is re-read (`GET .../items/{id}` or the case).

### 5.2 A timeline line (entry) — `step2-entry.html`
- Line card: tag, "January 16, 2026 · Dr. Alvarez, primary care", the summary. Footer: `why` ("Quote found word for word, every number
  in the summary is in the quote, and the second check agreed.").
- **Question:** "Does this line say the same thing as the highlighted words?"
- **Yes, this matches** → `POST .../items/{id}/review {action: "accept", version, expected_status}`. Saved text: "Kept in the letter."
- **No, leave it out** → `{action: "dismiss"}`. Saved text: "Left out of the letter."
- **Fix the wording** → 5.3.
- Status slot after an answer: "Saved: item 4 kept in the letter. Undo" (Undo = `{action: "reset"}` on that item, then reopen it).

Refusals, shown in the footer slot with the button disabled and the way out made the primary small action:

| Server says | Footer slot | Way out |
|---|---|---|
| item `reasons` include a code-check reason (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_NUMBER_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CHARGE_TEXT_IN_ENTRY`, `EXCERPT_*`, `GROUNDING_EXCERPT_NOT_VERBATIM`), or `422 CODE_CHECK_FAILED` | the `why` / `message` as given | "Fix the wording" (or "Change the highlighted words" for `EDIT_QUOTE`) |
| `422 DATE_UNCONFIRMED` | "Pick the right date first." | the date question (5.6) |
| `422 COMPARE_REQUIRED` | 5.4 | tick the box |
| `409 item_rejected` | the item is shown as could-not-check (5.5) | — |

### 5.3 Fix the wording — `step2-fix.html`
The line card body becomes a textarea with the current summary, same box. Above it: "Change the line so it says only what the
highlighted words say. Numbers, left/right and words like 'no' or 'possible' must match." The question row reads "Change the line,
then save it." The two big buttons become **Save my wording** / **Cancel** (same places). The source card adds one line at the top:
"To change which words are highlighted, tap whole sentences below." Sentences (`records[].sentences`) become tappable (outlined); the
chosen run is the new quote (contiguous whole sentences only; a gap in the run is refused in the browser with "Pick sentences that
follow each other.").

| Control | API |
|---|---|
| Save my wording (summary changed) | `{action: "edit", edits: {summary}}` |
| Save my wording (quote changed) | `{action: "edit", edits: {excerpt}}`; both changed: two calls, quote first |
| Cancel | nothing sent |

`422 invalid_edit` → the server `message` in the footer slot ("The summary says “left”, which the quote does not say. Remove it or
change the quote."); the text stays in the box. On save, the response item is shown: when `edit_to_check` is true the card goes to
5.4 with "You changed the wording. Read it against the highlighted words once more."; `warnings[]` messages (for example
`CHARGE_CLAUSE_REMOVED`) are shown in the footer slot.

### 5.4 Compare confirm (D-066, and an edit still to check) — `step2-disputed.html`
When the item is disputed (its ladder verdict or reasons say `partially` / `unsupported` / `disagrees`, the same rule as
`review.judge_dispute`) **or** `edit_to_check` is true:
- Footer slot (amber): the dispute sentence (the item `why`, e.g. "The second check found this only partly supported by the
  quote.") and a 28 px checkbox: **"I read this line against the highlighted words myself."**
- "Yes, this matches" is disabled until the box is ticked; then it sends `{action: "accept", compared: true, version,
  expected_status}`. "No, leave it out" and "Fix the wording" are always enabled.
- The box is never pre-ticked and is cleared when the item changes.

### 5.5 Could not check — `step2-cannot-check.html`, `step2-write.html`
A `tray` item. Line card header: "We couldn't check this one" (amber), body: the `why` as given, then "What was suggested (not
used): “Visit 8: pain 4/10, improving.”" (`attempt.summary`, quoted, muted). The source card shows the whole record without a
highlight (`attempt.excerpt` is not in the record, so nothing is marked).
- Tray **entry**: **Question:** "Read the record. Do you want to write this line yourself?" **Write it myself** → the write screen;
  **Skip it** → `{action: "dismiss"}` on the tray item ("Skipped. It stays out of the letter.").
- Write screen: the record's `sentences` are tappable (pick whole sentences that follow each other; the picked ones turn yellow); the
  line card is a textarea "Your line for the timeline". Buttons **Save my line** / **Cancel**. Save → `POST /api/cases/{token}/records/
  {rid}/entry {summary, excerpt}`. `422 invalid_edit` → message in the footer slot. `201` → the new item (`e<n>_m`, tag "Written by
  you") opens in the normal line question (5.2) at the same queue position.
- Tray **flag** (the second check disagreed with a suggested warning): header "We couldn't confirm this warning", body `why`, the
  suggested warning `attempt.summary` and its quote. **Question:** "This warning can't go in the notes. Read it; if it matters, tell the
  attorney yourself." **OK, leave it out** → `{action: "dismiss"}`; **Decide later** in the second slot.
- Tray items are optional: they never count in "N left" (the server leaves them out of `review.counts.pending`), and the item counter
  says "Optional".

### 5.6 A date to pick — `step2-date.html`
An entry in `undated_entries` whose record is in `dates_to_confirm` with `candidates`.
- Source card: the record with its `Date:` line marked.
- Line card header "Which date is right?", body: "The record says 04/05/2026. That could be two different dates." The two answers
  are the two candidates as long dates ("April 5, 2026" / "May 4, 2026"), each with its reading in small text ("month first" / "day
  first"). When `suggestion.iso` is set, that button carries a "Suggested" chip and the footer shows `suggestion.reason`
  ("4 other dates in this packet use month first..."). Nothing is chosen on load.
- **Question:** "Which date is right for this record?" → `POST /api/cases/{token}/records/{rid}/confirm_date {date}`.
  Response `gap_changes[].sentence` goes in the status slot ("Gap recalculated after you confirmed record 4: now 40 days (was 42).").
  The same item then shows the normal line question (5.2), "part 2 of 2" beside the counter.
- `missing` date (no candidates): "We couldn't find a date in this record, so it can't go on the timeline." One answer
  **OK, leave it out** (`dismiss`); the second slot is "Decide later".

### 5.7 A warning for the attorney (flag) — `step2-flag.html`, `step2-gap.html`
Warnings never go in the letter; accepted ones go in the internal notes (D-001). The line card becomes a warning card:
- Header: a fixed plain heading by type (below) + "Warning for the attorney".
- Body: `title` (bold) and `explanation` as given; for a gap with `computed.endpoint_warnings`, each `warning` and `alternative`
  sentence as given; `gap_change.sentence` when set.
- Source card: every `evidence[]` excerpt marked in its record (several records stacked).
- Footer: "Warnings only go in the notes for the attorney, never in the letter."
- **Question:** "Should the attorney be told about this?" **Yes, tell the attorney** → `{action: "accept"}`;
  **No, not needed** → `{action: "dismiss"}` (it is then listed under "Flags dismissed" in the notes, so the attorney can see what was
  ruled out). Third action **Add a note** → a textarea in the card, **Save note** / **Cancel** → `{action: "edit", edits: {note}}`.

| `type` / `category` | Plain heading |
|---|---|
| `gap` | A break in treatment (`computed.conditional`: A possible break in treatment) |
| `conflict` / `accident_date_*` | The records disagree about the accident date |
| `conflict` / `treatment_plan_vs_actual` | The plan and what happened differ |
| `conflict` / `provider_name_variant` | The provider's name is written differently |
| `conflict` / other | The records disagree |
| `pre_existing` / `pre_existing`, `prior_surgery` | An earlier health problem is mentioned |
| `pre_existing` / `degenerative_language` | Wording about wear and tear |
| `causation` / `patient_report` | The patient, not a doctor, says what caused it |
| `causation` / `speculative_language` | Hedged wording ("may", "possible") |
| `causation` / `missed_care` | Missed or ended treatment |
| `causation` / `new_onset` | Wording about a new problem |
| `causation` / `accident_date_provenance` | Where the accident date comes from |
| `causation` / `credibility_language` | Wording about the patient's effort or credibility |
| `causation` / other | Wording the other side could use |
| `record_warning` / `injection_suspected` | This record contains text that looks like instructions to a computer |
| `record_warning` / `date_ambiguous` | This record's date is unclear |
| `record_warning` / `analysis_incomplete` | We couldn't finish comparing these records |
| `record_warning` / other | Something to check in this record |

### 5.8 Step 2 done — `step2-done.html`
Shown when no undecided item is left (or from the step bar when the step is done).
- Big green check + "You checked every item on the timeline." + counts in one line: "8 kept in the letter · 1 left out ·
  7 warnings for the attorney · 3 not needed".
- If some are undecided instead: amber "2 items still need a decision." + **Go to the first one**.
- "Your answers": a plain list of all items in queue order, one row each: date, short label (entry: provider; warning: plain
  heading), the answer chip ("Kept", "Left out", "Tell the attorney", "Not needed", "Skipped", "Not decided") and a **Change** button
  (opens that item). Read-only "Suggestions a rule ruled out (nothing to do)": `tray_filtered.rules[]` label + `explanation` +
  each item's quote, when `count` > 0. `checks` (T-151): "We checked for: <labels of conflict_types>. Not checked: <not_checked labels>."
- Primary: **Go to step 3: Check the bills** (or step 4 when the case has no amounts).

## 6. Step 3 — Check the bills (`/case/<token>/bills`)

Queue: every item in `amounts[]` in this order: charges and countable amounts first (record order, then position), then the
never-counted ones. One at a time, same frame as Step 2. Charges are never batched (D-059); there is no "count all".

### 6.1 A charge — `step3-charge.html` (`kind: "charge"`)
- Line card ("Bill amount"): the figure as money in 40 px ("$6,240.00" from `value_cents`), "Central ER discharge summary ·
  January 9, 2026", footer "If you count it, it's added to the bill total in the letter."
- **Question:** "Should this charge count toward the bill total?"
- **Yes, count it** → `{action: "accept"}`; **No, don't count it** → `{action: "dismiss"}`.
- The title-row chip updates from the response `totals.accepted` ("Bill total so far: $6,240.00").
- **D-059 flagged charge** (`flag` set, `confirm_required: true`): footer shows `flag.message` as given and a checkbox named by the flag:
  `likely_duplicate` "I checked: this is a separate charge, not the same one counted twice."; `likely_total` "I checked: this is a
  charge of its own, not a total of the others." "Yes, count it" is disabled until ticked, then sends `{action: "accept", confirm:
  flag.confirm_with}`. On `422 CONFIRM_REQUIRED` the footer shows `detail.message`.

### 6.2 An amount that can be counted with a check (D-064 b) — `step3-count.html`
`countable: true`. Line card: the figure, "Not counted yet" chip, `not_counted_reason` as given ("The line states no date of service,
so it is not an itemized service line and is not totaled."). Footer: checkbox **"I checked this is a separate charge for a service."**
and, when `count_confirm` is set, `count_confirm.message` + a second checkbox named as in 6.1.
- **Yes, count it** (enabled when the box or boxes are ticked) → `{action: "count", confirm: "separate_charge"}` plus
  `confirm_flag: count_confirm.confirm_with` when set.
- **No, don't count it** → `{action: "accept"}` (it is noted for the attorney under "Amounts not totaled", never in the total).

### 6.3 An amount that is never counted (D-064 a) — `step3-never.html`
`countable: false` and not a charge (rate, total, balance, payment, adjustment, damages, estimate...). Line card: the figure as
written (`text`), "Never counted" chip, `not_counted_reason` as given. Footer: "Either way, it is never added to the bill total."
- **Question:** "This amount is never added to the total. List it in the notes for the attorney?"
- **Yes, list it** → `{action: "accept"}` (rates: `accept_effect: acknowledge`); **No, leave it out** → `{action: "dismiss"}`.

### 6.4 Step 3 done — `step3-done.html`
Big check + "You checked every bill amount." + the letter's total line exactly as the export writes it, large:
"Billed charges accepted from these records: $8,390.00" (`totals.letter_line` when present, else built from
`totals.accepted.cents`). Three plain lists, always open: **Counted** (figure, provider, date), **Not counted by you**, **Never
counted** (figure, where, `not_counted_reason`). `totals.possible_overlaps[]`: each `message` as given in an amber box above the
lists, with "Change" buttons on both figures. Primary: **Go to step 4: Get your letter**.
A case with no amounts: "We didn't find any bill amounts in these records." + **Go to step 4**.

## 7. Step 4 — Get your letter (`/case/<token>/letter`)

Data: `GET /api/cases/{token}/export` (and GET case for the counts). Layout: the letter on the left (wide, white "paper" box, 17 px,
`white-space: pre-wrap`, scrolls inside), the notes for the attorney on the right (narrower, tinted box headed "Notes for the attorney
— do not send"). Phones: letter first, then notes; each box fixed height with its own scroll.

### 7.1 Ready — `step4-letter.html`
Green status row: "Your letter is ready. Every item has an answer." Buttons under the letter: **Copy letter** (primary),
**Download letter (.txt)**. Under the notes: **Copy notes**, **Download notes (.txt)**. Copy → `navigator.clipboard.writeText
(letter_text)`; the button reads "Copied" for 2 s at the same width. Download → a Blob named `<title>-letter.txt` /
`<title>-notes.txt` (code, client side). A plain box "Exhibit and page numbers (optional)": three inputs Exhibit, Bates prefix,
First number + **Save** → `PUT /api/cases/{token}/export_config` then re-GET export (`422 invalid_edit` message under the inputs).
No drafted treatment paragraph anywhere (D-067).

### 7.2 Undecided items — `step4-pending.html`
`review.counts.pending + review.counts.edit_to_check` > 0 (the export is still allowed, D-045a):
amber row "3 items still need a decision. If you don't decide them, they stay out of the letter." + **Go to the first one** (the
first undecided item in step order: Step 2 queue, then Step 3). The letter preview shows what would be sent now. Copy and Download are
disabled until the checkbox "Copy it anyway, without those 3 items" is ticked (the one confirmation before copying the contract asks
for). The checkbox sits in a reserved row; it is not shown once the count is 0.

### 7.3 Blocked — `step4-blocked.html`
`422 export_blocked` / `judge_not_run`: red row "The letter can't be made yet." and one row per `detail.blockers[]`: its `why` as
given + a button by `next_action.code`:

| `next_action.code` | Button |
|---|---|
| `DECIDE` (`NOTHING_ACCEPTED`) | Go to step 2 |
| `EDIT_SUMMARY` / `EDIT_QUOTE` | Fix it (opens the item in Fix the wording) |
| `DISMISS_OR_ENTER_BY_HAND` | Go to it |
| `RERUN_JUDGE` | Run the second check again (`POST .../rejudge`, only when the item's `rerun_available`; else the text "The second check can't run here. Fix the wording in your own words, or leave the item out.") |
| `CONFIRM_RERUN` (`RUN_FAILED`) | Go to step 1 |
| `RUN_IN_PROGRESS` | (text) Wait for drafting to finish |

The letter box keeps its size and shows "Your letter will appear here once the problem above is fixed."

### 7.4 Done
Step 4 is done (green in the step bar, "Finished" on home) when steps 2 and 3 have nothing undecided and the export answers 200.

## 8. Visual system

- **Type:** system stack (`"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial`), `rem` on a 16 px root. Body 18/28,
  record text 18/29, the line to check 22/32, question 20/28, h1 32/40 (26/32 phones), small 15/22 (never below 14).
  Money and counts `tabular-nums`.
- **Spacing:** 8 px grid; page gutter 32 px desktop, 16 px phones; cards 24 px padding (16 phones); 16 px between cards.
- **Shape:** cards radius 14 px, buttons 12 px, chips 999 px; borders 1 px; one soft shadow on the action bar and cards.
- **Colour:** one accent (blue `#0B57D0`, dark `#8AB4FF`) for the current step, primary buttons, focus ring and links. Status colours
  only for meaning: green done/kept, amber needs a decision, red blocked; yellow `<mark>` for the quote. Light and dark sets on
  `:root` (`prefers-color-scheme`, overridden by `data-theme`); every text pair ≥ 4.5:1, control edges ≥ 3:1 (values: mockup
  `guided.css`, reusing `docs/UI_DESIGN_BRIEF.md` §4 where they overlap).
- **Targets:** big answers 56 px tall; every other control ≥ 48 px; checkboxes 28 px with the whole label clickable.
- **Focus:** 3 px accent ring, offset 2 px, on every control. After an answer focus moves to the first answer button of the next item.
- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons
  in one row below); the line card is a fixed 256 px, the source card takes the remaining height; no horizontal scroll anywhere.
- **Short phones (height ≤ 720 px and width ≤ 760 px, e.g. 320x640 or landscape):** the fixed frame would leave no room for the record,
  so the review page scrolls as a normal page; the action bar is `position: sticky; bottom: 0`, the source card body is capped at 260 px.
  Clicking still moves nothing (checked by the mockup test at 320x640).

## 9. Data rules (code in the browser; deterministic)

### 9.1 What counts as undecided
An item is undecided when it is live (not `rejected`) and `review_status` is `pending`, or `edit_to_check` is true. Step 2 =
entries, undated entries and flags; Step 3 = amounts. "N items still need a decision" = `review.counts.pending +
review.counts.edit_to_check` (the same number as home's `hitl.pending + hitl.edits_to_check`).

### 9.2 Step states
| Step | done when | status line |
|---|---|---|
| 1 | `status` is `ready` | "Done" / "Drafting 4 of 8" / "Run again" / "Not started" |
| 2 | no undecided Step 2 item | "Done" / "16 of 19 left" |
| 3 | no undecided amount | "Done" / "4 amounts" / "3 of 4 left" / "None found" (then done) |
| 4 | steps 2 and 3 done and the export gate is ready (`GET /trace` `export_gate.ready`, or home's `export_ready`) | "Ready" / "1 problem" / "Not yet" |

Current step = the first step not done. Home uses `GET /api/cases` `progress.entries + progress.flags` (Step 2) and
`progress.amounts` (Step 3); inside a case the same counts come from GET case.

### 9.3 Next line
Section 3.2, in that order. The only server sentence used is `next_action.reason` for a gate problem.

## 10. Words on screen

| Internal | On screen |
|---|---|
| entry | line (on the timeline) |
| excerpt / quote | the highlighted words |
| accept / dismiss (entry) | Yes, this matches / No, leave it out |
| flag | warning for the attorney |
| accept / dismiss (flag) | Yes, tell the attorney / No, not needed |
| charge accepted / dismissed | counted / not counted |
| tray, rejected, could-not-verify | We couldn't check this one |
| judge, second check, J1–J4 | the second check |
| verified / needs_review | (not shown; the question and the footer sentence carry it) |
| pending | not decided |
| internal notes | notes for the attorney |
| export | your letter |
| run / LLM run | drafting the timeline |
| token | case link |

## 11. API mapping (every control)

| Screen | Control | Call | Fields read |
|---|---|---|---|
| all | banner, demo label, footer | `GET /api/health` | `banner`, `answers`, `ai_banner`, `demo_mode`, `retention_hours`, `sample_available` |
| home | list | `GET /api/cases` (local) or `GET /api/cases/{token}` per stored token (public) | `title`, `created_at`, `last_activity_at`, `record_count`, `status`, `run`, `progress`, `hitl`, `export_ready`, `next_action`, `status_error*` |
| home | Rename / Save | `PATCH /api/cases/{token} {title}` | `title` |
| home | Delete / Yes, delete | `DELETE /api/cases/{token}` | — |
| home | Start a new case | route `/new` | — |
| home (empty) | Try the sample case | `POST /api/cases {sample: true}` | `token` |
| 1 | Read the records | `POST /api/cases` or `POST /api/cases/pdf` | `token`, `records[]`, `dates_to_confirm`, `warnings[]`, `injection` |
| 1 | Draft the timeline | `POST /api/cases/{token}/run {confirm_rerun:false}` | `status` |
| 1 | progress | `GET /api/cases/{token}/status` (1 s) | `status`, `stage`, `progress.done/total`, `counts`, `error` |
| 1 | Run it again / Yes, run it again | `POST .../run` (`confirm_rerun: true` after `409 needs_confirm`) | — |
| 1 | Read the scanned pages / Use these pages anyway | `POST /api/cases/pdf?ocr=true` / `?include_hidden=all` | — |
| 2, 3 | load | `GET /api/cases/{token}` | `entries`, `undated_entries`, `flags`, `amounts`, `tray`, `tray_filtered`, `records[].text/sentences/uncovered/char_start`, `dates_to_confirm`, `review`, `totals`, `checks`, `next_action` |
| 2 | Yes, this matches | `POST .../items/{id}/review {action:"accept", version, expected_status}` (+ `compared: true` after the 5.4 box) | `item`, `review`, `totals`, `warnings` |
| 2 | No, leave it out / Skip it / OK, leave it out | `{action:"dismiss"}` | same |
| 2, 3 | Undo / Change (back to undecided) | `{action:"reset"}` | same |
| 2 | Save my wording | `{action:"edit", edits:{summary}}` / `{edits:{excerpt}}` | `item.edit_to_check`, `warnings` |
| 2 | Save my line | `POST .../records/{rid}/entry {summary, excerpt}` | `item`, `review`, `warnings` |
| 2 | date answers | `POST .../records/{rid}/confirm_date {date}` | `entry`, `gap_changes[].sentence`, `dates_to_confirm` |
| 2 | Yes, tell the attorney / No, not needed | `{action:"accept"}` / `{action:"dismiss"}` on the flag | — |
| 2 | Save note | `{action:"edit", edits:{note}}` | — |
| 3 | Yes, count it (charge) | `{action:"accept"}` (+ `confirm: flag.confirm_with` when `confirm_required`) | `totals.accepted`, `totals.letter_line` |
| 3 | Yes, count it (countable) | `{action:"count", confirm:"separate_charge"}` (+ `confirm_flag`) | `amount`, `totals` |
| 3 | No, don't count it | charge: `{action:"dismiss"}`; countable: `{action:"accept"}` | `totals` |
| 3 | Yes, list it / No, leave it out (never counted) | `{action:"accept"}` / `{action:"dismiss"}` | — |
| 4 | preview, Copy, Download | `GET /api/cases/{token}/export` | `letter_text`, `internal_notes_text`, `excluded.pending` |
| 4 | blocked rows | `GET .../export` 422 `detail.blockers[]` (same as `GET .../trace` `export_gate.blockers`) | `why`, `next_action`, `item_id` |
| 4 | Run the second check again | `POST /api/cases/{token}/rejudge` | `export_gate` |
| 4 | Exhibit and page numbers Save | `PUT /api/cases/{token}/export_config` | — |

Not used by the guided UI (still in `/classic`): batch review, reclassify, dismissal suggestions, narrative (D-067), audit, judges,
billing listing, case trace panels, calibration.

## 12. States checklist (every screen)

| Screen | Loading | Empty | Error | Done |
|---|---|---|---|---|
| Your cases | 3 skeleton cards | 3.4 Empty | 3.4 Error + Try again | Finished section, green "Letter ready" |
| Step 1 | button shows "Reading..." in place, disabled | 4.1 | 4.1 table, 4.5 | 4.4 big check |
| Step 2 | skeleton text in both cards, same size; buttons disabled | "There are no timeline lines in this case." + Go to step 3 | load error in the work area: "We couldn't load this case." + Try again; write errors in the footer slot | 5.8 |
| Step 3 | as Step 2 | 6.4 no amounts | as Step 2 | 6.4 |
| Step 4 | "Making your letter..." in the letter box | `NOTHING_ACCEPTED` (7.3) | 7.3, network: "We couldn't make the letter. Try again" | 7.1 green row |

## 13. Test plan for the build card
The mockup already passes the first two checks (Playwright, `file://`): every checkbox, tile, tappable sentence and the theme button
was clicked on all 28 pages at 1440x900, 390x844 and 320x640 with 0 boxes moved, 0 horizontal overflow, 0 `<details>`/menus and 0 JS
errors; and the step bar, both answers, the small buttons, the question and both cards sit at identical boxes on all 12 review pages
(Step 2 and 3 items) at 1440 and 390, so moving from one item to the next moves nothing.

- Layout stability: for each review page, record the bounding boxes of the step bar, both answer buttons and the small buttons; click
  every answer, Fix the wording, Cancel, Back, tick and untick each box; assert no box moved (0 px) at 1440x900 and 390x844.
- No `<details>`, no `[role=menu]`, no element with `:hover`-only visibility; no horizontal scroll at 390 and 320.
- Flow: sample case from `/new` to a copied letter with only clicks; the letter equals `evals/golden/sample.export.expected.txt`.
- D-066: a disputed item cannot be accepted without the box (button disabled; a forced POST is 422 `COMPARE_REQUIRED`).
- D-059/D-064: count buttons stay disabled until the named box is ticked; bodies carry the named confirm.
- Provenance: with `answers: prepared` every sample item is tagged "Prepared answer"; the label and footer sentence are on every page.
- Multi-case: three cases at different steps show the right Next line and Continue target (local mode list and public mode stored tokens).
- axe: 0 serious/critical at both widths in light and dark.
