# T-064 review: 3D Office view (ux-designer-reviewer)

Verdict: changes. No blockers, four majors. Desktop (1440x900) is good: three floors visible at once, fixed camera, kanban legible (about 14px card ids at Board view), agents ride escalators, vending trips happen, pickleball ball moves, orchestrator visits desks. The phone experience, which Chris called out as "top notch" territory, is not there yet: kanban text is about 5px, the canvas swallows page scroll, the default frame crops the building and wastes space, and the floor buttons barely move the view.

Exercised (server on :7799, headless Chromium with SwiftShader, CDP touch events):
- `.venv/bin/python -m pytest tools/tests/test_board_server.py -q` -> `20 passed`.
- Walk at 390x844 (DPR2, touch) and 1440x900: default framing, each floor button, All, Board, Reset, +/-; button sizes read from the DOM (all >= 44x44 CSS px, pass); console errors: none.
- Touch: swipe up/down x3, horizontal pan, pinch in/out, double-tap x3 (zoom, reset, zoom), page-scroll attempts from header vs canvas.
- Camera: `O3.cam.rotation` = (-0.279, 0, 0) constant, no orbit input exists (no tilt/rotation control; pass).
- 80 s sampler of `O3.agents` at 1 Hz on desktop: escalator rides (y passes 0 -> 1.9 -> 3.3 -> 4.5 -> 5.6 -> ... -> 11.2 for researcher and claims-adjuster-reviewer), `vtrip0/1/2` vending errands by 6 reviewers, orchestrator `visitT-068/-076/-072/-064/-067` and return, ball moving.
- FPS via requestAnimationFrame over 3 s: 17.6 fps at 390px, 10.0 fps at 1440px. Both are software GL (SwiftShader), so this is a floor, not a device number.

Evidence is in `artifacts/review-evidence/T-064/` (m-01-default.png, m-02-*.png, m-03-*.png, m-04-pinch-in.png, m-06-board.png, d-01-default.png, d-10-anim-15.png, walk1.json, touch.json, touch2.json, anim.json; scripts T-064-ux-*.py).

On the "empty space above the canvas, canvas looks small" question: not acceptable as shipped. Measured: toolbar takes 157 CSS px (19% of 844) before the canvas starts at y=157, and inside the 657 px canvas the building occupies about 432 px (m-01-default.png: tan band above y=575/2 and below), about 28% of the canvas is dead tan. At the same time the building is cropped horizontally (frontend, ux, staff-eng labels clipped at the right edge). So the phone shows neither the whole building nor a useful close-up.

```json
{"card": "T-064", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commits 87ed185, 7986d22; tools/board_ui.html, tools/board_server.py; http://localhost:7799/?view=office at 390x844 and 1440x900; live board data",
 "exercised": ["pytest tools/tests/test_board_server.py -> 20 passed", "Playwright 390x844 touch (CDP): swipe, pinch, double-tap, floor buttons, Reset, +/-, Board", "Playwright 1440x900: default, floors, Board, 80 s agent sampler", "DOM button size measurement", "rAF fps counter (SwiftShader)", "O3.cam rotation read-back", "page-scroll attempts from canvas vs header"],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 4, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "Kanban is illegible on a phone (about 5 px text)",
   "evidence": "touch2.json board_px: board_css_width 279, id_text_css_px 4.9, hdr_text_css_px 4.6 at 390px in Board view; screenshot artifacts/review-evidence/T-064/m-06-board.png (card ids unreadable, agent labels T-067/orchestrator sit on top of the IN REVIEW / NEEDS CHRIS columns). Desktop Board view is 14.5 px, fine (d-09-board-view.png).",
   "why_it_matters": "Chris asked for the kanban back and for mobile legibility; on the phone the board is texture decoration, not information. State visibility is the point of the board.",
   "fix": "On narrow screens make the Board button zoom to a board-only crop where ids are >= 12 CSS px (about 2.5x current), and re-lay the canvas texture for portrait: 2 rows of 4 columns (or 3 visible columns with horizontal pan), card chips at least 90 px wide in a 1024 px texture. Hide agent labels within the board's screen rect while in Board view. Alternative: Board button opens the existing 2D kanban in a bottom sheet on phones.",
   "acceptance_test": "Playwright 390x844 click Board; project the board quad to screen; assert card-id text height >= 12 CSS px and no agent label rect intersects the board rect."},
  {"severity": "major", "title": "Canvas traps page scroll on phones; vertical swipe does nothing at default zoom",
   "evidence": "touch.json: swipe up/down on canvas leaves ty at 9.7 and scrollY at 8 (3 swipes); pagescroll_from_canvas [65, 65] while pagescroll_from_header [0, 65]. Canvas is 657 of 844 px tall with touch-action:none (board_ui.html o3Size: style.touchAction='none'), leaving a 29 px strip under it. At default zoom the whole building fits so o3Clamp locks ty (board_ui.html:546-547).",
   "why_it_matters": "Chris asked to 'just scroll vertically if needed'. A user's natural vertical swipe on the building does nothing and cannot reach the agent list/cards below; the only way out is to find the 157 px toolbar.",
   "fix": "Use touch-action: pan-y on the canvas and, when the camera is at its vertical clamp (or at default zoom), let the one-finger vertical drag fall through to page scroll; only capture drags when zoomed in (r < r0*0.9) or for two-finger gestures. Add a visible 'Agents list below' affordance or shrink phone canvas height to about 70vh so there is always page background to grab.",
   "acceptance_test": "Playwright touch 390x844: at default view a 300 px vertical swipe on the canvas changes window.scrollY by > 100; when zoomed in, the same swipe changes O3.v.ty and not scrollY until the clamp is hit."},
  {"severity": "major", "title": "Phone default framing: building cropped sideways, 28% of canvas empty, toolbar eats 157 px",
   "evidence": "m-01-default.png (390x844): canvas y=157..814, building occupies about 432 px of 657, tan empty bands above and below; frontend/ux/staff-eng labels cut at the right edge, 'lease' and 'staller' cut on the left in m-02-floor0.png. touch.json: default view floor1, r 49.4, tx 2.75 (fit width 17 of a 28-unit building). Toolbar = chips row + 3 buttons rows (m-01-default.png top 157 px).",
   "why_it_matters": "Chris called phone visibility 'really poor'. The default neither shows all floors whole (his stated wish) nor zooms in usefully; dead space plus clipping reads as a bug on first load.",
   "fix": "Default phone frame = 'All floors' with height fit: set r so the 3 floors fill the canvas height (building is about 20 units tall, canvas 657 px), centre horizontally on the most active agents, allow horizontal pan only. Collapse the toolbar to one row (floor chips 44 px, zoom/Reset as a floating column over the canvas) so the canvas starts within about 60 px of the top. Clamp ty so empty ground never exceeds 5% of canvas height.",
   "acceptance_test": "Playwright 390x844 on load: building bounding box (projected) covers >= 85% of canvas height; canvas top <= 80 px; no agent label is clipped by the canvas edge for agents on the visible floors."},
  {"severity": "major", "title": "Floor buttons Engineering / Office / Break barely change the phone view",
   "evidence": "walk1.json m_floor2/m_floor1/m_floor0: view.ty is 9.7 for all three and r is 47.7-48.5; only tx differs (4.9, 2.75, 0). Screenshots m-02-floor2.png, m-02-floor0.png show all three floors in nearly the same position with only a horizontal shift. Selected chip highlights, but the scene does not move to that floor.",
   "why_it_matters": "Controls that do not visibly do what they say break feedback and user control; users will not trust the selector, and 'Office' being pre-selected on load (m-01-default.png) implies a focus that is not shown.",
   "fix": "Make each floor button frame that floor: ty = floor centre, r so the floor fills the canvas width and about 60% of its height, with an eased 300 ms camera move; pre-select 'All' on load when all floors are visible. Show the floor name as a sign inside the scene (O3_FLN exists but is not rendered).",
   "acceptance_test": "Playwright 390x844: click each floor button; assert O3.v.ty differs between Engineering, Office, Break by >= 4 units and the clicked floor's projected centre is within 10% of canvas centre."},
  {"severity": "minor", "title": "Name labels overlap each other and cover the people they name",
   "evidence": "m-02-all.png (prod-mgr / nurse / architect / security stacked on each other and on the escalator), m-01-default.png (T-045/chaos pill on top of the figure), d-10-anim-15.png (security/privacy/release/hiring cluster). Labels are about 15 px CSS tall on a figure about 40 px tall at the phone default.",
   "why_it_matters": "Names are readable at 390 px without zooming (pass), but the collision means you cannot tell who is who or see the agents' poses, which are the animated part.",
   "fix": "Add simple screen-space label de-collision (nudge down/up by label height, leader line), shrink idle labels to initials or a coloured dot on phones, and offset labels above the head (+0.3 units) instead of at the figure centre.",
   "acceptance_test": "Playwright 390x844: pairwise intersection area between visible label rects is 0 for all but at most one pair; idle labels are hidden until zoom r < 0.6*r0."},
  {"severity": "minor", "title": "Kanban column count digits overprint the column titles",
   "evidence": "m-02-floor2.png: 'IN PROGRES2', 'NEEDS CHR3'; d-10-anim-15.png: 'IN PROGRES 8', 'NEEDS CHRIS 5' overlapped. Source: board_ui.html o3Board draws the count right-aligned at 64 px in a 256 px column next to a 34 px bold title.",
   "why_it_matters": "Two of the eight headers are damaged on the one screen meant to show status.",
   "fix": "Shorten the titles ('IN PROG', 'NEEDS ME') or draw the count on a second line under the title; measure with g.measureText and shrink font until title + count fit cw.",
   "acceptance_test": "Unit/Playwright: for each column, measureText(title).width + measureText(count).width <= cw - 28 at the used fonts."},
  {"severity": "minor", "title": "Graphics are stylised toy low-poly, not the 'more realistic' Chris asked for (judgement call, not a spec violation)",
   "evidence": "d-01-default.png, m-01-default.png: box-limbed figures with flat saturated colours, neon cyan court, uniform-colour walls; shadows are blob sprites for agents (handoff says so).",
   "why_it_matters": "Chris's request was explicit. The jump from the earlier version is real but the look is still cartoon. I would do it differently: this is labelled preference, not a hard fail.",
   "fix": "Cheap wins: desaturate the court to a muted green/blue, add baseboards and a window light-spill on floors, use a subtle noise normal on walls, soft contact shadows under desks, and tone-map (ACES) with slightly warmer lights.",
   "acceptance_test": "Side-by-side screenshot review by Chris at 1440x900 and 390x844; accept or reject on 'more realistic' wording."},
  {"severity": "minor", "title": "Frame rate on a real phone is unmeasured; only SwiftShader numbers exist",
   "evidence": "rAF counter: 17.6 fps at 390px, 10.0 fps at 1440px in headless SwiftShader (software GL). Handoff: 'not profiled on a real phone'.",
   "why_it_matters": "Chris asked for 'top notch' mobile; I cannot confirm 30+ fps. Software GL is a worst case, so this is not a failure, but an unmeasured claim.",
   "fix": "Add an adaptive quality governor: if the 30-frame average dt > 40 ms, drop DPR to 1, turn off the two point lights, update animation at 30 Hz, and pause rendering when the tab is hidden or the camera and agents are idle. Record a fps number from one real iPhone/Android in the card.",
   "acceptance_test": "Card evidence includes a real-device fps reading >= 30 at 390 px default view, or the governor is exercised in a Playwright test that forces slow frames and asserts DPR drops to 1."}
 ],
 "whats_right": [
  "Camera is fixed (rotation constant at -0.279 rad, no orbit input), all three floors visible together, as Chris asked.",
  "Every control is >= 44x44 CSS px; pinch, double-tap zoom/reset and Reset work; vertical pan works once zoomed in.",
  "Escalator rides, vending errands, pickleball rally and orchestrator desk visits all observably happen (anim.json), with no console errors."
 ],
 "questions_for_chris": [
  "The fixed camera still looks down about 16 degrees with perspective, so walls converge in the All view. Is that 'no tilt' for you, or do you want a flat orthographic side elevation?",
  "On a phone, would you rather see the whole building small (current intent) or one floor large with vertical scroll between floors? Fix 3 above assumes whole building filling the height."
 ]}
```
