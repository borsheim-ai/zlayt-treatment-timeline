# T-047 UX review: 3D Office view (commit cf1f874)

Persona: ux-designer-reviewer. Scope is the four ACs from `python3 tools/board.py show T-047`, plus the Office tab's
UX at 1440 and 390. The sample case does not apply here; this is the board's Office tab at http://localhost:7777.

**Verdict: pass.** No blockers and no majors. All four ACs hold in the live app. Three minors and one nit.

## What I exercised
- `python3 tools/board.py show T-047`: status in_review, commits [cf1f874], AC 1-4 all `done: true`.
- `git show --stat cf1f874`: 5 files changed (board_ui.html +161, board_server.py, tests, two screenshots).
- `python3 tools/board.py validate` returned `ok (47 file(s))`.
- `curl -s localhost:7777/api/office`: live data, frontend active on T-047, reviewers carry a `counterpart` field.
- Playwright, 1440x900 (`artifacts/review-evidence/T-047-ux-designer-check.py`): clicked Office, waited 3 s,
  screenshot, console and page errors, failed requests, canvas state, list state, tap-to-dialog, horizontal overflow.
- Playwright, 390x844 touch (same script): tapped Office, screenshot (viewport and full page), tapped a list item.
- Playwright, forced `reviewing` state via route interception (`artifacts/review-evidence/T-047-ux-designer-ac2-forced.py`):
  checked the reviewer's walk target against the counterpart desk.
- Playwright side check (`artifacts/review-evidence/T-047-ux-designer-nav-keyboard.py`): nav overflow on load at 390,
  tabindex of list items and canvas.
- Viewed screenshots: `T-047-desktop-1440.png`, `T-047-mobile-390.png`, `T-047-mobile-390-dialog.png`,
  `T-047-desktop-1440-forced-reviewing.png`.

Results, verbatim from the run:
- 1440: `canvas_display: "block"`, `canvas_box: [1240, 744]`, `canvas_has_webgl_ctx: true`, `three_loaded: true`,
  `o3_ok: true`, `list_items: 22`, `list_items_tappable: 7`, `doc_scroll_w: 1440 / doc_client_w: 1440`,
  `console_errors: []`, `page_errors: []`, `failed_requests: []`, `dialog_opened_on_click: true`.
- 390: `canvas_box: [358, 376]`, `doc_scroll_w: 390 / doc_client_w: 390`, `console_errors: []`, `page_errors: []`,
  `failed_requests: []`, `dialog_opened_on_tap: true`.
- Forced reviewing: `accessibility-reviewer` key `besidefrontend0`, pos (4.10, -5.40), target (4.10, -5.40); frontend desk
  at (2.80, -5.40). Idle `qa` key `lounge4`.
- Nav at 390: `nav_scrollW: 507`, `nav_clientW: 358`; `of_list_li_tabindex: -1`; `canvas_tabindex: -1`.

Not exercised: orbit drag, wheel zoom and pinch (AC 1 "touch"); tapping a 3D figure (raycast path); live walking
mid-transit at 390; a live reviewing state (none in the data at capture, covered only by the forced run).

## Findings
1. **minor: The Office list and 3D canvas cannot be reached by keyboard, so cards open by mouse or touch only.**
   The list `li` elements have `tabIndex -1` and no role. The canvas has `tabindex -1`. The keydown Enter handler is
   scoped to `#office-svg .ch[tabindex]` (tools/board_ui.html:497), so in 3D mode nothing on the Office tab can be
   reached or activated from the keyboard. AC 3 says "2D list remains below for accessibility", and the list is not
   accessible by keyboard. Severity for conformance is deferred to accessibility-reviewer.
   Fix: give `#of-list li[data-card],li[data-file]` tabindex 0, role button and an Enter/Space handler, the same
   pattern the SVG path uses at tools/board_ui.html:314.
   Test: Playwright, Office tab in 3D mode at 1440, Tab until `#of-list li[data-card]` is focused, press Enter, assert `#dlg[open]`.

2. **minor: Room names are occluded or clipped, and at 390 they are hard to read (AC 3 says "still legible").**
   `T-047-desktop-1440.png`: the "BREAK ROOM" floor label is covered by the figures standing in it.
   `T-047-mobile-390.png`: "ORCHESTRATOR OFFIC" is cut off by the wall, and the room labels are about 6 CSS px.
   The figure names and bubbles are legible, so the information survives; the room signage does not.
   Fix: draw room labels above the figures (lift the label `y` or render it as an HTML overlay), or enlarge them at narrow widths.
   Test: screenshot at 390 shows all four room names whole and unobscured.

3. **minor (pre-existing, outside T-047's ACs): The top nav scrolls horizontally at 390 and hides the Office tab on load.**
   tools/board_ui.html:18 `nav{display:flex;gap:6px;overflow-x:auto}`; the same rule is at line 17 at the parent commit,
   so this is not from cf1f874. Measured `nav_scrollW: 507` vs `nav_clientW: 358`. After tapping Office, `scrollLeft` is 23
   and the Board tab is clipped (`T-047-mobile-390.png`, top left). Document-level horizontal scroll is 0, so the
   Office view itself is fine.
   Fix: wrap the nav (`flex-wrap: wrap`) or make it a visible two-row control.
   Test: at 390, all six tab buttons are fully visible on load, or the nav wraps.

4. **nit: "chg T-028" bubble label is developer shorthand.** tools/board_ui.html:306 maps the verdict to `chg`.
   "changes T-028" or "requests changes" reads more clearly to a non-developer viewer. Optional.

## Persona lens
The Office tab is a status display, not the review workflow, so most of my 20-item checklist does not apply. I graded
it on information scent and on whether the status it shows can be trusted. The footer line
("Derived from board data only (cards, activity log, review files); refreshes every 5 s") says where the data comes from.
That matches what I saw: no claim beyond the board data.

## What's right
- Zero console errors, zero page errors and zero failed requests at both widths. The pinned three.js r128 with SRI loaded and ran.
- The list carries the same information as text (name, state, card, activity line). Tapping an item opens the card dialog at 1440 and at 390.
- Pairing works: a reviewing reviewer walks to a station beside the counterpart's desk, and idle agents go to the break room.

```json
{"card": "T-047", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit cf1f874 (tools/board_ui.html, board_server.py, tests); app http://localhost:7777 Office tab; sample case not applicable",
 "exercised": [
   "python3 tools/board.py show T-047 (status in_review, AC 1-4 done)",
   "git show --stat cf1f874 (5 files)",
   "python3 tools/board.py validate -> ok (47 file(s))",
   "curl -s localhost:7777/api/office (live data; counterpart field present on reviewers)",
   "Playwright 1440x900: Office click + 3 s wait, screenshot, console/page errors, failed requests, canvas/list state, list click opens #dlg, overflow check (artifacts/review-evidence/T-047-ux-designer-check.py)",
   "Playwright 390x844 touch: Office tap, screenshots (viewport + full page), list tap opens #dlg, overflow check (same script)",
   "Playwright forced reviewing state via route interception: reviewer walk target vs counterpart desk (artifacts/review-evidence/T-047-ux-designer-ac2-forced.py)",
   "Playwright nav/keyboard side check at 390: nav scrollW/clientW, li and canvas tabindex (artifacts/review-evidence/T-047-ux-designer-nav-keyboard.py)",
   "Viewed screenshots T-047-desktop-1440.png, T-047-mobile-390.png, T-047-mobile-390-dialog.png, T-047-desktop-1440-forced-reviewing.png"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 4},
 "findings": [
   {"severity": "minor",
    "title": "Office list and 3D canvas are not keyboard-reachable; cards open by mouse or touch only",
    "evidence": "tools/board_ui.html:330 (list li rendered without tabindex/role); keyboard check: li[data-card] tabIndex -1, canvas tabindex -1; tools/board_ui.html:497 Enter handler scoped to '#office-svg .ch[tabindex]' only (hidden in 3D mode)",
    "why_it_matters": "AC 3 says the 2D list stays below 'for accessibility', but a keyboard user cannot reach or open any card from the Office tab when WebGL is on. Conformance severity is deferred to accessibility-reviewer.",
    "fix": "Give '#of-list li[data-card], #of-list li[data-file]' tabindex=0, role=button and an Enter/Space handler, matching the SVG pattern at tools/board_ui.html:314.",
    "acceptance_test": "Playwright at 1440 in 3D mode: Tab until '#of-list li[data-card]' has focus, press Enter, assert '#dlg[open]' exists."},
   {"severity": "minor",
    "title": "Room names occluded by figures (1440) and clipped or unreadable at 390 (AC 3 says 'still legible')",
    "evidence": "artifacts/review-evidence/T-047-desktop-1440.png: 'BREAK ROOM' label covered by figures; artifacts/review-evidence/T-047-mobile-390.png: 'ORCHESTRATOR OFFIC' clipped by wall, room labels about 6 CSS px; room labels set at tools/board_ui.html:367",
    "why_it_matters": "Figure names and bubbles remain legible, so the status survives, but the room signage that AC 1 requires is not reliably readable.",
    "fix": "Raise room labels above the figure layer (larger y offset or HTML overlay), or enlarge them at narrow widths.",
    "acceptance_test": "Screenshot at 390x844 after 3 s shows all four room names whole and not occluded."},
   {"severity": "minor",
    "title": "Pre-existing (outside T-047 ACs): top nav scrolls horizontally at 390 and hides the Office tab on load",
    "evidence": "tools/board_ui.html:18 'nav{display:flex;gap:6px;overflow-x:auto}' (same rule at line 17 of parent commit, so not introduced by cf1f874); measured nav_scrollW 507 vs nav_clientW 358; after tapping Office scrollLeft=23 and 'Board' is clipped (artifacts/review-evidence/T-047-mobile-390.png)",
    "why_it_matters": "At 390 the user must scroll the nav sideways to reach tabs; document-level overflow is 0, so the Office view itself is fine.",
    "fix": "Wrap the nav (flex-wrap: wrap) or present the tabs as a visible two-row control.",
    "acceptance_test": "At 390x844, all six tab buttons are fully visible on load, or the nav wraps with no clipped button."},
   {"severity": "nit",
    "title": "'chg T-028' bubble is developer shorthand",
    "evidence": "tools/board_ui.html:306 maps verdict 'changes' to 'chg'; screenshot artifacts/review-evidence/T-047-desktop-1440-forced-reviewing.png shows 'chg T-028'",
    "why_it_matters": "A non-developer viewer reads 'chg' less quickly than 'changes'.",
    "fix": "Use 'changes T-028' (optional).",
    "acceptance_test": "Bubble text reads 'changes T-028' for a changes verdict."}
 ],
 "whats_right": [
   "Zero console errors, page errors and failed requests at 1440 and 390; pinned three.js r128 with SRI loaded and ran (O3.ok true).",
   "The 2D list carries the same information as text, and tapping an item opens the card dialog at both widths with no document horizontal overflow.",
   "Pairing works: a reviewing reviewer walks to the station beside the counterpart desk (forced state), and idle agents go to the break room."
 ],
 "questions_for_chris": [
   "The persona file expects model claude-opus-5-5, but this review ran as claude-haiku-5-5 (dispatch said 'ux (haiku)'). The record uses claude-haiku-5-5. Confirm which model the ux-designer reviewer should be pinned to."
 ]}
```
