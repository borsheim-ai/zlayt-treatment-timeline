# Office view: references (T-026)

Question: how do other projects show AI agents as characters in a space, and what should the board's Office tab borrow?
Only pages I opened and read (fetched 2026-11-02) are listed.

| # | Reference | One-line takeaway | What we borrowed |
|---|---|---|---|
| 1 | Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (Stanford/Google, 2023) https://arxiv.org/abs/2304.03442 | 25 agents live in a Sims-inspired sandbox town, so a spatial metaphor makes agent behaviour legible to a human observer. (The abstract page does not describe the UI; "Smallville" is not named there.) | The core idea: place = what the agent is doing. Rooms map to roles of work (desks, review room, break room). |
| 2 | Pixel Agents (VS Code extension / `npx pixel-agents`) https://github.com/pablodelucca/pixel-agents | One animated pixel character per Claude Code session; they walk to desks, type when editing, read when searching, and show speech bubbles when waiting for input or permission. State is derived from hook events / JSONL transcripts, not from the agent itself. | State-to-animation mapping (typing hands when working), speech bubble as the status badge (we show the card id), deriving state from logs we already have (activity.jsonl) rather than asking agents to report. |
| 3 | a16z AI Town https://github.com/a16z-infra/ai-town | Tile-map town with characters as spritesheets; frontend subscribes to backend state so the world updates live. Characters are plain data entries (name, description, sprite). | Characters are data-driven (one entry per `.claude/agents` file); the page re-renders from a single polled state payload (our `/api/office`, 5 s poll). We chose inline SVG over PixiJS/spritesheets because the CSP forbids image hosts and we want no build step. |
| 4 | ChatDev, "virtual software company" https://github.com/OpenBMB/ChatDev | Agents take software-company roles (CEO, CTO, programmer, reviewer, tester...) and the repo ships a visualizer with per-role icons plus log and replay modes. | Role identity through a distinct colour/prop per role (programmer, reviewer, designer icons) and the company framing: workers at desks, reviewers as a separate group. Replay mode is a possible later extension (activity.jsonl is already an event log). |
| 5 | Gather (virtual office) https://www.gather.town/ | Teams get avatars and customisable desks in a shared 2D office; position signals availability ("look around to see who's available"). | Glanceable availability: empty desk plus a person in the break room means idle; a person at a desk means busy. A "simplified view" idea: we add a plain list under the floor for small screens and screen readers. |

## Decisions that follow
- **Office floor, not a Matrix rain view.** A floor with named stations answers Chris's actual question ("what is each agent doing right now?") at a glance, and lets each character be tapped into its card. A Matrix-style view is atmospheric but anonymous and hard to read on a phone.
- **Inline SVG + CSS animation**, no images, no new script origins (page CSP: `img-src 'self' data:`).
- **Two layouts from one data model**: a wide floor (1200x508 viewBox) and a stacked phone layout (400x1334). Characters keep their DOM nodes between polls, so a state change produces a visible walk (CSS transform transition) instead of a re-draw.
- **State is derived, never reported**: `/api/office` reads cards, `board/activity.jsonl` and `reviews/` only.
