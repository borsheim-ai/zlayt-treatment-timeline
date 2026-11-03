---
name: stepper-and-judge-panel
description: T-081/T-082 stepper + AI-check panel: where it lives, how it hooks in, pitfalls
metadata:
  type: project
---
app/frontend/stepper.js (ZL.stepper: item, itemSection, openTrace, traceButton, mountCase, goto) + stepper.css (--zs-* tokens over styles.css vars) + judges.js (RV.registerPanel "judges"). Data: api.trace / caseTrace / judges (api.js).
Hooks: timeline.js openWhy appends itemSection; renderReview calls mountCase; flags/charges/tray get a btn-trace "How it was checked" button.
**Pitfalls:** never put data-item-id on rows outside real review items (review.js j/k and [data-panel] scans pick them up) -> judge rows use data-target-item, gate rows data-jump-item. Case rail is a details whose open state is kept in a module var; `[data-testid=case-stepper] summary` also matches the inner "Show the other N" details (use .first or .zs-case-det > summary).
**Dev:** own instance needs DATA_DIR=<dir> (not ZLAYT_DB) for a clean DB: `DATA_DIR=artifacts/tmp/fe-data LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local PORT=7871 .venv/bin/python -m app.main`; run e2e with E2E_BASE_URL. Library case_lib06 has 3 judge objections (good for screenshots/tests).
**Round 3 (D-044/D-045, e92b6ed):** one handler S.rejudge (stepper.js) behind S.rerunButton (data-testid btn-rerun-judge); status sentence lives in module var rerunNote and is rendered into every [data-testid=rerun-status], so repaints keep it. Refused export (422) -> S.showExportBlocked paints section[data-testid=export-blocked] under the Export toolbar (timeline.js mounts S.exportNotice); export.js no longer opens #view-export on error. Pending items = gate.warnings (not blockers); NOTHING_ACCEPTED export is 422.
**Test recipe:** tests/e2e/conftest.py JudgeNotRun(page, token, ids, mode, hold) route-stubs the "judge never ran" state (fixtures cannot make it); page fixture unroute_all before close. For a clean verify while others edit app/backend, run the server from `git archive HEAD` in scratchpad with app/frontend copied over. A stray `cat > /tmp/x` before a heredoc swallows the heredoc (old script silently re-ran).

## T-097 r3 (D-051 refusals)
- Refused Accept: review.js `refusals{}` map + `.rv-refused` box (testid accept-refused) under the button bar in RV.controls; batch.js `refused` + batch-refused inside the batch bar. Server message shown verbatim; scroll the box with a 16px margin (scrollIntoView nearest leaves it flush on the fold).
- Rerun: one group button per list ("for these N"); never per-row, one POST reruns all (reviewer m-2 recurred 3 rounds).
- Real-backend e2e for a failing summary: write `summary` via `app.db.db.update_item` on the server's ZLAYT_DB (tests skip without it); route stubs cannot be composed (later route wins), so one stub per test.
