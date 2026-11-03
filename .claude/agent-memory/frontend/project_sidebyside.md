---
name: side-by-side-source-viewer
description: T-046 two-pane source viewer: module, hooks, pitfalls
metadata:
  type: project
---
app/frontend/sidebyside.js + sidebyside.css (R-ST-1). Pane is appended to #view-review (outside #review-body, so renderReview never wipes it); follows focusin/click on any [data-item-id] via ZL.rv.find + ZL.rv.sourceTargets; body.sbs-on toggles the grid. Only active when matchMedia(min-width:1024px). Test ids sbs-* (distinct from record-modal/record-highlight so strict locators stay unique). Open record button / o still open the modal at all widths (test_source_record needs that at 1280).
**Pitfalls:** the sticky pane top must clear the sticky synthetic banner (48px). `#view-review[hidden]` needs an explicit display:none when grid is applied. j from the charges panel sticks (review.js panel branch), so step tests start from an entry row. Never `pkill -f app.main` to stop your instance: it kills other workers' servers; kill by PID.
