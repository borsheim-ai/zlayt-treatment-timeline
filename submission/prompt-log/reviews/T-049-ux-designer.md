# T-049 Office view: UX review (ux-designer-reviewer)

Quick check against the three briefed checks at 390x844 with touch enabled, on commit ef18e64 running at http://localhost:7777. All three hold: the 3D canvas has `touch-action: none` at runtime, the Full screen button resizes the office container, and `/?view=office` renders a canvas. No blockers or majors. Three polish items. The two-finger pinch gesture (the core of AC 1) was not in this brief and was not exercised. Esc exit is untestable headless and was not tested.

Model note: I ran as claude-haiku-5-5. The dossier's expected id is claude-opus-5-5; the record reports the model I actually ran as.

```json
{"card": "T-049", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit ef18e64 (tools/board_ui.html); http://localhost:7777 (board server, running); T-049 AC 1-3 as briefed: canvas touch-action, Full screen button and fallback, /?view=office canvas, pytest tools/tests/test_board_server.py",
 "exercised": [
  "python3 tools/board.py show T-049 (AC and handoff read)",
  "git cat-file -t ef18e64 -> commit",
  ".venv/bin/python -m pytest tools/tests/test_board_server.py -q -> '18 passed in 0.76s', exit 0",
  "curl -s -o /dev/null -w '%{http_code}' http://localhost:7777/ -> 200",
  "artifacts/review-evidence/T-049-ux-designer-check.py (Python Playwright, chromium, viewport 390x844, has_touch=True): loaded /, clicked button[data-v=office]; read computed touch-action, display, bounding boxes of #office3d, #office-svg, #office-wrap, #of-fs; document scrollWidth vs viewport; window.THREE loaded",
  "same script: clicked #of-fs; recorded #office-wrap 358x1995 -> 390x844, fullscreenElement = office-wrap, popups opened = none, label -> '✕ Exit full screen'; clicked again to exit (wrap back to 358x1995)",
  "same script: opened /?view=office in a second page; recorded canvases (#office3d 374x707, touch-action none), header display none, #of-close visible, scrollWidth 390, console errors none, failed requests none",
  "artifacts/review-evidence/T-049-ux-designer-check.out.json (full machine-readable results)",
  "grep of tools/board_ui.html and curl of served HTML (artifacts/review-evidence/T-049-served-index.html): located touch-action assignment at line 437 and the fullscreen wiring at lines 527-537, button markup at line 146",
  "viewed screenshots T-049-ux-designer-02-office-390.png, -03-fullscreen-390.png, -04-view-office-390.png"],
 "verdict": "pass",
 "scores": {"design quality": 4, "originality": 4, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "minor",
   "title": "Full screen button's accessible name does not follow its state",
   "evidence": "tools/board_ui.html:146 `<button type=\"button\" id=\"of-fs\" class=\"act\" aria-label=\"Full screen\">` (static aria-label); tools/board_ui.html:535 ofFsChanged() rewrites only innerHTML. Runtime: artifacts/review-evidence/T-049-ux-designer-check.out.json steps.2_fullscreen_click.of-fs_label_after = \"✕ Exit full screen\" while the aria-label stays \"Full screen\". Accessibility conformance is accessibility-reviewer's call; I grade the UX consequence only.",
   "why_it_matters": "In fullscreen the visible action is 'Exit full screen' but the announced name is 'Full screen'. The system-status signal that the view is in fullscreen is not carried to assistive tech.",
   "fix": "Remove the static aria-label so the visible text names the button, or set aria-label inside ofFsChanged() to match the visible label.",
   "acceptance_test": "Playwright: after the first click on #of-fs the accessible name contains 'Exit'; #of-fs has no static aria-label attribute in the served HTML."},
  {"severity": "minor",
   "title": "touch-action:none over the whole 3D canvas leaves a thin page-scroll area on a 390 px phone (design opinion; AC 1 requires it)",
   "evidence": "artifacts/review-evidence/T-049-ux-designer-check.out.json steps.1_office_click: #office3d x=16 w=358 h=508 touchAction=none; #office-wrap h=1995. The only non-canvas gutters are 16 px on each side. Screenshot artifacts/review-evidence/T-049-ux-designer-02-office-390.png.",
   "why_it_matters": "A thumb that starts on the 508 px scene cannot scroll the page, so the text list that follows the canvas (#of-list) is reachable only from the 16 px gutters. This is what AC 1 asks for, so it is not a spec violation; it is a reach problem on a phone.",
   "fix": "Let one-finger vertical drag scroll the page once the camera is at its tilt limit, or keep a non-canvas scroll handle beside the scene. Decide with Chris whether 'vertical drag = tilt' applies at every tilt.",
   "acceptance_test": "At 390 px, a vertical touch swipe that starts on the canvas with the camera at its tilt limit increases window.scrollY, or the trade-off is recorded in the card as an accepted decision."},
  {"severity": "nit",
   "title": "Rightmost figure and its name bubble are cut by the canvas edge at 390 px",
   "evidence": "artifacts/review-evidence/T-049-ux-designer-03-fullscreen-390.png and artifacts/review-evidence/T-049-ux-designer-04-view-office-390.png: the rightmost figure ('chaos' bubble) runs into the right edge of the canvas.",
   "why_it_matters": "A clipped label reads as a layout bug on a phone. The same people appear in the text list, so no information is lost.",
   "fix": "Pad the camera framing or clamp the view so every station and name bubble fits inside the canvas at 390 px.",
   "acceptance_test": "At 390 px every projected name bubble's bounding box lies inside the canvas bounds (assert in the Playwright check)."}
 ],
 "whats_right": [
  "Full screen is a labelled 115x44 px button in the Office header row at 390 px; one click took #office-wrap from 358x1995 to 390x844 with fullscreenElement set.",
  "/?view=office is a clean pop-out: header hidden, #office3d renders 374x707 with the scene visible, Close is shown, zero console errors and zero failed requests.",
  "No page-level horizontal scroll at 390 (document scrollWidth 390 = viewport), and touch-action none is set at runtime on the canvas in both the office view and the pop-out (source tools/board_ui.html:437)."],
 "questions_for_chris": [
  "AC 1 says one-finger drag pans/orbits and the page must not scroll while gesturing on the canvas. Is the thin 16 px page-scroll gutter acceptable on phones, or should vertical drag scroll the page once the tilt is at its limit?"]}
```
