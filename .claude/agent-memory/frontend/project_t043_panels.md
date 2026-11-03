---
name: t043-panels-conventions
description: How flags/charges/review controls plug into frontend-1's app shell, and E2E testid pitfalls
metadata:
  type: project
---
Review UI is split: frontend-1 owns index/api/state/timeline/source; frontend-2 owns review.js, flags.js, charges.js, review.css. Plug-in points: ZL.registerPanel(fn(case, mountEl)), ZL.registerRowActions(fn(entry,rowEl)), ZL.state.applyReview(resp), ZL.openSource(spans,title).
**Why:** tests/e2e specs (qa) are the contract; strict locators mean exactly one btn-source per flag, data-review only on item roots (count of [data-review=accepted] must equal accepted items), no data-state outside queue rows.
**How to apply:** dev harness at app/frontend/dev/panels.html (?case=01|03|07) serves with `python3 -m http.server` from app/frontend; E2E assertions right after a click race the async review response.
