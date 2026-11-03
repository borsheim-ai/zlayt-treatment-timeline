# T-026 Board Office view: UX review (ux-designer-reviewer)

Nice-to-have tooling for Chris, not the product; graded against the 4 AC only. Drove http://localhost:7777 with Playwright at 1440x900 and 390x844. All 4 AC hold. Characters, labels, card bubbles and states match `/api/office`, and tapping a character opens the card dialog. Two minor polish items; no blockers or majors.

```json
{"card": "T-026", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 158219b; tools/board_ui.html Office tab; http://localhost:7777 (board, not the product app); AC 1-4 only",
 "exercised": [
  "python3 tools/board.py show T-026 (AC read)",
  "curl -s localhost:7777/api/office; compared worker/reviewer states and card ids to what the floor and list render (architect working T-028, frontend active T-026, ux-designer-reviewer reviewing T-026 all match)",
  "artifacts/review-evidence/T-026-ux-designer-office.py: clicked Office at 1440 and 390, full-page screenshots T-026-desktop-office.png, T-026-mobile-office.png",
  "tapped a character (frontend) at both widths: card dialog opened (T-026-desktop-dialog.png, T-026-mobile-dialog.png)",
  "clicked Board, Activity, Inbox after Office at both widths: render, no page errors",
  "document scrollWidth at 390 = 390 (no horizontal scroll)"],
 "verdict": "pass",
 "scores": {"design quality": 4, "originality": 4, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "Floor labels are 10-11 px; legibility is borderline at 390",
   "evidence": "Playwright min rendered svg text height: 11.0 px desktop, 10.0 px mobile; mobile desk labels (e.g. 'privacy', 'prod-mgr') and station captions in artifacts/review-evidence/T-026-mobile-office.png are small. The card list below carries the same state in readable text, so this is a polish gap, not a loss of information.",
   "why_it_matters": "Character names and card bubbles are the whole point of the view; small text weakens the glance-read on a phone.",
   "fix": "Raise SVG label and bubble font sizes on the 400-unit phone layout to at least 12 px rendered, or drop station captions that duplicate the desk name.",
   "acceptance_test": "At 390 px every svg text element renders at 12 px or taller (assert in the Playwright check)."},
  {"severity": "minor", "title": "Mobile tab bar clips the first tab and the mobile review room shows empty benches",
   "evidence": "T-026-mobile-office.png: tab row shows 'oard' (Board cut off) when Office is selected; break-room area shows two empty purple benches. Page scrollWidth is 390, so the clipping is inside the tab strip, and Board is still reachable. Pre-existing tab-strip behaviour made more visible by the extra tab.",
   "why_it_matters": "A cut-off label reads as a bug; empty benches add scroll length on mobile.",
   "fix": "Scroll the active tab into view with the strip's left edge visible, and size the mobile break room to the number of occupants.",
   "acceptance_test": "At 390 px after clicking Office, the Board tab text is fully inside the viewport or the strip scrolls so the active tab is fully visible."}
 ],
 "whats_right": [
  "State is encoded three ways (position on the floor, card bubble, text list below), so it does not depend on the small drawing.",
  "The floor and list use the same /api/office data; no drift observed, and the footer says it refreshes every 5 s.",
  "Tap a character opens the card dialog at both widths; other tabs unaffected; no horizontal scroll at 390."],
 "questions_for_chris": []}
```
