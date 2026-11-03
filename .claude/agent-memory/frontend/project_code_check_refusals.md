---
name: code-check-refusals
description: T-097/T-104 hooks for CODE_CHECK_FAILED refusals (accept, batch, edit), the Change the quote action, and the Why-dialog lead
metadata:
  type: project
---

CODE_CHECK_FAILED (422) arrives on accept, batch accept and edit (review.set_review is the backend choke point). `detail.next_action.code` is EDIT_SUMMARY or EDIT_QUOTE.
- review.js: `refusals[id]={id,code,message,label}` paints `accept-refused` (button `btn-accept-refused-edit` or, for EDIT_QUOTE, `btn-accept-refused-quote`). An edit refusal goes to `showEditRefusal` (`edit-refused-msg` inside the `.rv-error` line, box stays open, typed text kept; `btn-edit-refused-quote` only for EDIT_QUOTE).
- batch.js: per-row `next_action.code` -> `btn-batch-refused-quote`; message says "entries" when any row is a quote check.
- excerpt.js owns the quote picker; `ZL.openQuoteEditor(id)` / `ZL.hasQuoteEditor(id)` open it from anywhere. `ZL.stepper.changeQuote(id)` = goto item + picker, falling back to the record when the row has no picker. `ZL.stepper.wordingFix/wordingEditText(id, next_action, verdictLabel)` choose the button for the Why dialog, rail blocker and judge panel rows.
- Why dialog lead (`S.wordingLead(id, verdictLabel)`) follows the backend verdict string ("this summary" vs "your wording"); only rail/panel rows with no verdict fall back to `mine(id)`.

**Pitfall:** the sample record prints `Excerpt: "..."` as sentence units, so the picker cannot rebuild the original quote there (saving always 422s). E2E specs stop at "picker is open".
**Pitfall:** to break a quote on the real backend, set the item's `excerpt` column to words[1:] via `app.db.db.update_item` (needs ZLAYT_DB); a summary-only edit and an accept then both return EDIT_QUOTE.
**Why:** the orchestrator's T-098 r3 handoff left the frontend saying "Edit the summary" for quote failures.
