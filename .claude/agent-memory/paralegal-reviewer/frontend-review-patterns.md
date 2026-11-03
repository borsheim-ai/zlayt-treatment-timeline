---
name: frontend-review-patterns
description: How to drive and what to check on Zlayt frontend cards (T-042/T-043/T-044): static server on mock, harness vs integrated mock, recurring gaps
metadata:
  type: feedback
---

Serve with `.venv/bin/python -m http.server 7866 --directory app/frontend` (pkill after). The integrated `index.html?api=mock` mock only emits gap flags; conflict/pre-existing/causation cards exist only in `dev/panels.html` (variants ?case=01|03|07). Sample load = `btn-sample` then `btn-analyze`.

**Why:** T-043 review (2026-11-01): frontend cards tick ACs "proved by tests/e2e" while the backend is down, so the real flag shapes are unverified.

**How to apply:** check whether the card's proof specs were actually run; state in the review what was mock-only. Recurring checks: keyboard `a`/`d` advance jumps focus to the timeline queue (scroll yank), dismiss reason not displayed, $185 row lacks "12 planned; discharged at visit 9", needs-review-first sort inside groups. Related: [[reviewer-hook-constraints]].
