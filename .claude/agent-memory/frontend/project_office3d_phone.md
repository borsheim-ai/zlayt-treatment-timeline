---
name: office3d-phone-conventions
description: tools/board_ui.html 3D office phone design (touch ownership, fit-to-box camera, kanban sheet) and pitfalls
metadata:
  type: project
---
Office 3D lives in tools/board_ui.html (o3* functions). Phone (<820px) rules: canvas height = building aspect (o3Fit on O3_BOX), bleeds to screen edges; touch-action pan-y at framed view, none once r<0.9*r0 (o3Touch); Board button opens HTML kanban sheet (#of-kb), 3D wall texture is only ~5px on phones.
**Why:** UX review of T-064 flagged 5px kanban, trapped page scroll, dead band, floor buttons not moving the view.
**How to apply:** test with CDP Input.dispatchTouchEvent (real gestures); canvas width is NOT viewport width (main padding), use #of-stage width; macOS sed needs `-i ''`; git-guard forbids `git add && git commit` in one command; new files need a separate `git add` before pathspec commit.
