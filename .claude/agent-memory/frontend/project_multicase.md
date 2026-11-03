---
name: multicase-overview-detail
description: T-149 multi-case UI hooks (overview.js), routing, test recipe, pitfalls; plus T-151 conflict-skipped and T-136 r3 held-quote hooks
metadata:
  type: project
---

**Overview (home) and case overview block live in `app/frontend/overview.js` + `overview.css`.** Home = `#view-cases` (hidden unless GET /api/cases answered 200 and no case is open); the paste box stays below it. Detail starts with `[data-testid=case-overview]` (first child of `timeline`), painted from the live case (progress, chips) and from the case trace via the `zl:trace` event that stepper.js `setCache` dispatches.

**Why:** Chris asked for multi-case management (overview + detail). Server numbers are the truth: tests compare screen to GET /api/cases, GET case and /trace.

**How to apply:**
- Routing: `ZL.cases.open(token)` pushState `#/case/<token>`; `All cases` (`btn-all-cases`) pushState home; `popstate` syncs. A hash-only `page.goto` in a test keeps the old timeline on screen: `goto("about:blank")` first.
- Title: overview shows `ZL.niceName(name)` for library names else the API `title`; cached in `ZL.caseTitles[token]` and used by the header.
- Pitfall: hide the `<section>` (`host.closest("section")`), not the inner body div.
- Pitfall: `<details>` default-open set in JS fires a toggle event; record her choice on the summary click, not on toggle.
- Switcher no longer lists cases (only the synthetic library); `details.cs-details` summary reads "Add a synthetic case".
- Test recipe: `E2E_BASE_URL=http://127.0.0.1:<port> ZLAYT_DB=<file>` against your own `python -m app.main` (PORT/HOST/ZLAYT_MODE=local/LLM_BACKEND=fixture); the full e2e takes 15+ min when other agents load the machine, run it in the background on a worktree copy.
- Screenshots: `ZLAYT_SCREENSHOTS=1 pytest tests/e2e/test_multicase.py -k screenshots` writes artifacts/screenshots/multicase-*.png (wait for `co-gate-verdict` before shooting).

**Held re-picked quote (T-136 r3):** `ZL.secondCheckPending` reads the server `second_check_pending`; a rerun is offered for a held item only until the blocker carries `rerun_no_answer` (then only "Write the summary", `btn-write-summary-case`). Helpers in stepper.js: `S.isHeld`, `S.HELD_CAN_RERUN`, `S.HELD_NO_RERUN`.
**Conflicts group (T-151):** `checks.skipped[]` box (`conflict-skipped`), `checks.notes[]` (`conflict-note`), always-visible `conflict-not-checked-line`; a skipped type is not in the Checked list.
