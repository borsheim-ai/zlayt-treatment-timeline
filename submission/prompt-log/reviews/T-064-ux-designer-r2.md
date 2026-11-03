# T-064 round-2 review: 3D Office view, phone (ux-designer-reviewer)

Verdict: pass. No blockers, no majors. All four round-1 majors are resolved on measured evidence at 390x844 with touch. Four minors and one judgement point are new this round.

Scope: commit 4e9914a (HEAD), tools/board_ui.html, tools/board_server.py served at http://localhost:7798/?view=office, live board data (92 cards). Desktop 1440x900 was not in this round's brief and was not exercised.

## Round-1 majors, re-checked

1. Kanban illegible on phone: resolved. Board opens an HTML kanban sheet. Minimum text in the sheet is 12 CSS px (walk.json `board_sheet.kb.minFs`). Screenshot: `artifacts/review-evidence/T-064-r2/m-08-board-sheet.png`.
2. Canvas traps page scroll: resolved. A 300 px vertical swipe on the canvas at the framed view moved `window.scrollY` from 7 to 292, with camera `ty` unchanged (9.4 to 9.4). Pinch zooms (r 35.4 to 15.2, `visualScale` 1). Once zoomed, a horizontal drag panned `tx` (-0.01 to 8.62), a vertical drag panned `ty` (9.4 to 13.7), and `scrollY` stayed 0 in both. Reset returned r, tx, ty to the exact pre-pinch values (35.39, 0, 9.4) with `touchAction` back to `pan-y`.
3. Default frame cropped with empty band: resolved. The building projects to 94% of canvas height and 96% of canvas width (`default_cover.covY` 0.941, `covX` 0.963). The canvas is 390x228 CSS px starting at y=50. Screenshot `m-01-default.png` shows the whole building with no dead tan band. Horizontal page overflow is 0.
4. Floor buttons do not move the view: resolved. Engineering, Office and Break set distinct framings (ty 13.2, 7.6, 2.9). Each floor centre sits within 5.2% of the canvas centre, each floor covers about 96-97% of canvas width, and the floor name tag reads ENGINEERING, OFFICE and BREAK ROOM (`m-06-floor2.png`, `m-06-floor1.png`, `m-06-floor0.png`).

Camera: fixed. `O3.cam.rotation` is (-0.2793, 0, 0) at start and end of the walk, and it stays fixed through every gesture. The only camera-angle constant is `O3_EL=16` (tools/board_ui.html:365). A grep finds no code that writes `cam.rotation`. The camera has a fixed 16 degree downward pitch with no orbit input. Whether that counts as "no tilt" is an open question for Chris (see questions_for_chris).

Exercised:
- Ran `.venv/bin/python artifacts/review-evidence/T-064-ux-designer-r2-walk.py` with BOARD_PORT=7798. No page errors, no console errors (`console_errors` and `page_errors` both empty).
- Started `BOARD_ROOT=$PWD python3 tools/board_server.py --port 7798` in the background. Checked `curl /?view=office` returned 200. Stopped it afterwards; `curl` then returned connection refused.
- Phone walk at 390x844, DPR 2, `is_mobile`, `has_touch`, CDP `Input.dispatchTouchEvent`: default load, vertical swipe up and down on canvas, two-finger pinch in, one-finger horizontal and vertical drag while zoomed, Reset, Eng/Office/Break floor buttons, All, Board (open and close via its X).
- Read computed font sizes of every text node in the kanban sheet, and chip sizes.
- Read the building projection, floor projection and label visibility from `O3` in-page.
- Viewed screenshots m-00 (full page), m-01, m-03, m-06 (three floors), m-08.

## New findings (all minor)

- Kanban chip tap targets are 32 CSS px tall (minimum 46x32, `board_sheet.kb.chipMinWH`). Below the 44 px target this review applies to the rest of the phone controls.
- While zoomed, the badge "Zoomed: drag to move · double-tap to reset" sits over the lower labels in `m-03-pinch-zoomed.png` and hides the "security" and "architect" name plates.
- Floor views crop edge name plates: "installer" and "privacy" are cut at the left canvas edge in `m-06-floor2.png`, and "architect" is cut at the bottom.
- At the default frame the canvas is 228 CSS px tall, 27% of the 844 px viewport. The whole building fits, but it is small, and only 4 of 22 name plates show (`default_labels`). This is a judgement call, not a spec violation.
- Carried forward from round 1, not re-graded and not re-measured this round: label collisions (visible in m-06-floor2.png, "chg T-067" over "adjuster"), no real-device fps reading, and the graphics style judgement.

## Outside my lens

WCAG conformance (contrast, focus order, target size as a standard) belongs to accessibility-reviewer. I noted the tap sizes as a UX point only.

```json
{"card": "T-064", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 4e9914a (HEAD); tools/board_ui.html; tools/board_server.py on http://localhost:7798/?view=office; 390x844 DPR2 touch via CDP; live board data (92 cards); sample case not applicable",
 "exercised": ["started BOARD_ROOT=$PWD python3 tools/board_server.py --port 7798; curl /?view=office -> 200; stopped server, curl -> connection refused",
   "artifacts/review-evidence/T-064-ux-designer-r2-walk.py run with BOARD_PORT=7798 -> artifacts/review-evidence/T-064-r2/walk.json; errors/console_errors/page_errors all empty",
   "vertical swipe up on canvas at framed view: scrollY 7 -> 292, camera ty 9.4 -> 9.4; swipe down: scrollY back to 7",
   "two-finger pinch in: r 35.39 -> 15.17, touchAction none, hint shown, visualScale 1, scrollY 0",
   "zoomed one-finger horizontal drag: tx -0.01 -> 8.62, scrollY 0 -> 0; zoomed vertical drag: ty 9.4 -> 13.75, scrollY 0 -> 0",
   "Reset tap: r, tx, ty equal pre-pinch values (35.39, 0, 9.4); touchAction back to pan-y; hint hidden",
   "default frame coverage from projected O3_BOX: covY 0.941, covX 0.963, canvas 390x228 at y=50; hScroll 0; screenshot m-01-default.png and m-00-default-full.png viewed",
   "floor buttons floor2/floor1/floor0: ty 13.23 / 7.64 / 2.90; floor centre offset 0.2%-5.2% of canvas; floor coverage 96-97% width; tags ENGINEERING / OFFICE / BREAK ROOM; screenshots m-06-*.png viewed",
   "Board tap: #of-kb visible, 55 text nodes, minFs 12, maxFs 20, chips min 46x32; close via X returns kbHidden true; screenshot m-08-board-sheet.png viewed",
   "camera: O3.cam.rotation (-0.27925, 0, 0) at start and end of walk; grep tools/board_ui.html for cam.rotation writes: none; O3_EL=16 at line 365",
   "grep of tools/board_ui.html for touch handlers and o3View/o3Touch/o3Fit (read, not edited)"],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 4, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "Kanban chip tap targets are 32 px tall, under the 44 px target used for the rest of the phone controls",
   "evidence": "artifacts/review-evidence/T-064-r2/walk.json steps.board_sheet.kb.chipMinWH = [46, 32]; screenshot artifacts/review-evidence/T-064-r2/m-08-board-sheet.png shows chips such as T-046 at about 46x32 CSS px",
   "why_it_matters": "The board sheet is the phone's status view and each chip opens a card. A 32 px target is easy to miss with a thumb, so a mis-tap opens the wrong card.",
   "fix": "Give .kb-chip min-height 44px (and keep the grid gap) so each chip meets the 44 px target. Chips in a column can scroll if the column gets tall.",
   "acceptance_test": "Playwright 390x844 with touch: open Board, assert every .kb-chip bounding box has height >= 44 and width >= 44."},
  {"severity": "minor", "title": "Zoom hint badge covers name labels while zoomed",
   "evidence": "artifacts/review-evidence/T-064-r2/m-03-pinch-zoomed.png: the 'Zoomed: drag to move · double-tap to reset' badge sits over the 'security' and 'architect' name plates at the bottom of the canvas",
   "why_it_matters": "The badge is useful feedback, but it hides the people it is meant to help a user find while zoomed in.",
   "fix": "Move the badge to the top edge of the canvas (under the floor tag), or fade it to 60% opacity after 3 s. Keep the text.",
   "acceptance_test": "Playwright 390x844: pinch in, then assert the #of-hint rect does not intersect the rect of any visible name label, or that the hint is at top < 40 px of canvas."},
  {"severity": "minor", "title": "Floor framing crops edge name plates",
   "evidence": "artifacts/review-evidence/T-064-r2/m-06-floor2.png: 'installer' is cut at the left canvas edge and 'architect' is cut at the bottom edge; m-06-floor0.png crops 'lit-lead' at the top",
   "why_it_matters": "The floor buttons now frame each floor, which is what round 1 asked for. A name plate cut in half reads as unfinished and can hide who is on that floor.",
   "fix": "Add about 6% margin to the floor fit (O3_FRM widths or the o3Fit margin argument), and keep labels inside the canvas by nudging them in when they are at the edge.",
   "acceptance_test": "Playwright 390x844: for floor2, floor1 and floor0, every visible name label rect lies fully inside the canvas rect."},
  {"severity": "minor", "title": "Default phone canvas is short (228 px) and shows only 4 of 22 name plates",
   "evidence": "walk.json steps.default_state.canvas = {w: 390, h: 228}; steps.default_labels: labelVisible true for 4 of 22 agents; screenshot artifacts/review-evidence/T-064-r2/m-01-default.png",
   "why_it_matters": "The whole building now fits, which fixes the round-1 crop. But at 27% of the phone height the people are small, and most of them have no name on the default view. Chris asked for phone visibility that is top notch.",
   "fix": "Judgement call for Chris: either keep the building-fit canvas and accept the small figures, or let the default canvas grow to about 40% of viewport height and show more name plates on the default view.",
   "acceptance_test": "Chris signs off the default phone screenshot at 390x844, or the canvas height and the visible label count on load are set to the values he picks."},
  {"severity": "minor", "title": "Zoomed canvas takes every drag from the page; exit only via Reset or double-tap",
   "evidence": "walk.json steps.pinch_in.touchAction = 'none' and zoomed drags kept scrollY at 0; the badge text states the exit ('double-tap to reset') and Reset sits under the canvas",
   "why_it_matters": "Once zoomed, a vertical swipe on the canvas cannot scroll the page. The badge and the visible Reset button make the exit clear, so this is a minor cost rather than a trap, but it is the kind of lock a user will hit unawares.",
   "fix": "When the camera reaches its vertical clamp in the zoomed state, let further vertical drags fall through to page scroll (set touch-action to pan-y at the clamp). Keep the badge.",
   "acceptance_test": "Playwright 390x844: zoom in, drag vertically until the camera clamp, drag again; assert window.scrollY changes by more than 50."}
 ],
 "whats_right": [
  "All four round-1 majors are resolved on measured evidence: kanban text min 12 px, a 285 px page scroll from a canvas swipe at the framed view, building covers 94% x 96% of the canvas, and each floor button frames its floor within 5.2% of centre.",
  "Pinch, zoomed pan and Reset all behave as specified, and Reset restores the exact framed state; no console or page errors and no horizontal overflow at 390 px.",
  "The camera pitch and rotation are fixed through every gesture (rotation.x -0.2793, y and z 0), and no code writes the camera rotation."
 ],
 "questions_for_chris": [
  "The camera has a fixed 16 degree downward pitch (O3_EL=16; rotation.x -0.279 rad). It is fixed and cannot be tilted by the user. Is that 'no tilt' for you, or do you want a flat side elevation? This question carries over from round 1.",
  "This review ran as claude-haiku-5-5. CLAUDE.md section 6 says judgment reviewers run on Opus. Do you want this review re-run on Opus before the M2 gate?"
 ]}
```
