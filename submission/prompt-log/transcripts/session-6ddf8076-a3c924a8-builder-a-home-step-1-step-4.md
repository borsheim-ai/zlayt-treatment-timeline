# Subagent: Builder A: Home, Step 1, Step 4 (Builder A: Home, Step 1, Step 4)

Source: `agent-a3c924a80ec1e94e0.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:26:49.378Z

You are frontend Builder A on T-181, the guided UI (D-068, P0, Chris approved). Work in /Users/arsis/zlayt-pm-project. Don't claim the card; note on it as `frontend-A`.

**Read first:**
- docs/GUIDED_UI_SPEC.md
- the mockup at artifacts/mockups/guided/
- reviews/T-180-ux-designer.md (its majors must be fixed)
- every note on `python3 tools/board.py show T-181`, especially the scaffold's page contract, file boundaries and test ids
- memory/contracts/api.md

**Your files:** home.js/.css, step1.js/.css and step4.js/.css under app/frontend/guided/, plus tests/e2e/guided/test_home.py, test_step1.py and test_step4.py. Builder B owns step2, step3 and review.*. Don't edit the shell files (index.html, core.js, app.js, styles.css); send needed shell changes as a card note. Don't edit app/backend.

**Build every screen the spec gives for these pages:**
- **Home ("Your cases"):** the case list with status, progress and the needs-your-decision callouts; New case; Open the sample.
- **Step 1, Add records:** the paste/upload screen, Read the records, and a done state. In demo mode, don't offer Paste/Upload as if it works. Explain why, and offer Open the sample or Choose a library case. Errors are plain sentences, including the 413 and 429 from G.api.
- **Step 4, Get your letter:** the blockers list linking back to the step that fixes each one; Copy and Download; the D-067 cut, so there is no narrative paragraph.

**Rules for all three pages:**
- The primary action stays above the fold at 1440x900, in a sticky action bar.
- At 390px nothing clips.
- No jargon.
- D-065 provenance: use G.provenance() and models.generator_prepared / item.prepared, with the badge tooltip "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."
- Use textContent only and no inline style attributes (CSP).

**Tests:** the e2e specs cover a first-time path from Home through a downloaded letter. Step 2 and Step 3 may still be stubs, so drive the API for them where needed. Screenshots at 1440 and 390 go to artifacts/screenshots/guided/.

**Commit:** verify from a `git archive` copy with E2E_REQUIRE_DB=1, running the guided tests plus test_no_console_errors. Commit only your paths through a temp index (GIT_INDEX_FILE plus `git read-tree HEAD`); never run `git checkout` or `git restore`. Note your commit on T-181. Reply in 2 lines.

### User / tool · 2026-11-02T21:26:49.384Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:53.524Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-181 | head -300; ls app/frontend/guided tests/e2e/guided artifacts/mockups/guided; wc -l docs/GUIDED_UI_SPEC.md reviews/T-180-ux-designer.md"
}
````

### User / tool · 2026-11-02T21:26:53.659Z

**tool result**
````
---
id: "T-181"
title: "Build the guided UI (D-068) on the existing API: new shell at /, old screen at /classic; Your cases, 4 fixed steps, one-item review queue, bills, letter; guided e2e suite"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P0"
depends_on: ["T-180"]
created_by: "orchestrator"
created_at: "2026-11-02T20:32:49Z"
updated_at: "2026-11-02T21:26:32Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T20:33:17Z"
rounds: 0
commits: ["f3d42a2"]
reviews: []
ac:
  - {"n": 1, "text": "every screen in docs/GUIDED_UI_SPEC.md built; a first-time user finishes the sample case to a downloaded letter with no instructions; old /classic e2e still green; new tests/e2e/guided/ suite green; screenshots", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:32:52Z orchestrator: assigned: frontend
- 2026-11-02T20:33:17Z frontend: claimed
- 2026-11-02T20:34:27Z orchestrator: Guided UI must send version + expected_status on every review POST (T-178 stale-tab 409, see api.md) and show the 409 message with a reload of the item; carry D-066 (disputed accept needs the compare confirm) and D-067 (no narrative).
- 2026-11-02T21:04:53Z orchestrator: Guided UI provenance: read models.generator_prepared / item.prepared and use the D-065 badge + tooltip and 'Prepared answer' tag (T-177 r2, 4fcf9cd).
- 2026-11-02T21:05:43Z orchestrator: Build must fix the T-180 review majors (reviews/T-180-ux-designer.md): primary action of every step above the fold at 1440x900 (Read the records, Draft the timeline, Copy/Download letter) - use a sticky action bar; 390px: show enough of the record (collapsible header, not a 122px window) and Undo fully visible; build the paste/upload screen with plain errors, and in demo mode do not offer Paste/Upload as if they work (explain + Open the sample / Choose a library case); no jargon on decision screens ('second check' -> 'a second AI check', no 'model's quote', no 'itemized service line'). Also fold the 7 minors.
- 2026-11-02T21:26:32Z frontend: SCAFFOLD COMMITTED f3d42a2, ready for the two step builders. Verified from git archive with E2E_REQUIRE_DB=1: full tests/e2e 431 passed 1 skipped (classic at /classic + 12 guided shell tests); the committed tree also passed the pre-commit smoke. SERVING: / = app/frontend/guided (real paths, history.pushState; server answers index.html for any extension-less non-file path via GuidedFiles in api.py; /api and /classic never fall through); /classic = old screen, unchanged. e2e conftest: SERVER (root, API) and BASE = SERVER+'/classic' (classic specs unchanged). FILE BOUNDARIES (one file per step, none shared except review.js): Builder A (Home + Step 1 + Step 4): home.js/.css, step1.js/.css (registers G.pages.new AND G.pages.records), step4.js/.css (G.pages.letter). Builder B (Step 2 + Step 3): step2.js/.css (G.pages.timeline), step3.js/.css (G.pages.bills), review.js/.css (shared frame helpers, B only). Nobody edits index.html, core.js, app.js or styles.css except to fix the shell (tell frontend). styles.css = the mockup guided.css verbatim plus shell additions, so every mockup class (.card, .actions-in, .btn.answer, .tile, .ccard ...) already exists. PAGE CONTRACT (header of app.js): G.pages.<home|new|records|timeline|bills|letter> = async (ctx) => cleanup?; render into ctx.view (display:contents, children become body children: frame pages append .titlebar/.work/.actions, page pages append one main.wrap); resolve after first paint (shell then sets data-ready on [data-testid=view]); ctx = {route, token, step, query, case (GET case, loaded by the shell), health, signal, view, layout('frame'|'page') (done screens call ctx.layout('page')), go(path,{replace}), refresh() (re-GET case; redraws step bar + header), setStepStatus(n,text,state?), setCaseTitle, setTitle}. SHELL PROVIDES: banner + demo pill + footer (D-065 amended wording, G.provenance() gives {kind,label,note,hours}), header, step bar with live statuses from G.steps.states (spec 9.1/9.2; also accepts a /api/cases row, so Home reuses it), theme, G.api (plain-message ApiError: 0 offline, 404, 413, 429, 5xx never show raw text), G.store, G.url.records/timeline/bills/letter/step, G.h (no innerHTML), G.errorBlock. Throws become the plain error block + Try again. RULES: textContent only; no inline style attributes (CSP style-src 'self'): size things with el.style.width=... from code; CSP otherwise unchanged. TESTS: tests/e2e/guided/test_shell_smoke.py has helpers watch(page) (console/page/http/requestfailed errors), go(page,path) (waits for data-ready), rect, chrome; put each builder's specs in their own tests/e2e/guided/test_<name>.py. Test ids set by the shell: banner-synthetic, app-header, demo-badge, btn-theme, step-bar, step-1..4 (aria-current=step; locked step is a span aria-disabled), view (data-route, data-ready), footer-note, case-title, btn-your-cases, page-error, btn-retry, link-home. NOTES: (1) real paths replaced the hash routes I was first told to build, because spec section 1 requires them. (2) D-065 was amended after the spec: prepared pill tooltip and footer use 'Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.' not the spec 2.3 sentence about the evaluation report. (3) Step 4 status 'Ready' comes from review.ready_to_export (row export_ready); a page that knows the blocker count can override with ctx.setStepStatus(4,'1 problem','attn'). (4) The worktree api.py now holds another worker's uncommitted ClassicFiles/limits hunks; my commit contains only the GuidedFiles hunk, so whoever commits those must keep the /classic mount lines. (5) Changed tests/e2e/test_count_duplicate.py (goto adds /classic) and tools/check_index_imports.py (smoke list = no_console_errors + guided shell smoke).

## Handoff (filled when moving to in_review)

app/frontend/guided:
app.js
core.js
home.css
home.js
index.html
review.css
review.js
step1.css
step1.js
step2.css
step2.js
step3.css
step3.js
step4.css
step4.js
styles.css

artifacts/mockups/guided:
build.py
check_across_items.py
check_stability.py
guided.css
guided.js
home-empty.html
home-error.html
home-loading.html
index.html
screens.html
step1-add.html
step1-drafting-lib01.html
step1-drafting.html
step1-failed.html
step1-found.html
step2-cannot-check.html
step2-date-confirmed.html
step2-date.html
step2-disputed.html
step2-done.html
step2-entry.html
step2-fix.html
step2-flag.html
step2-gap.html
step2-write.html
step3-charge.html
step3-count.html
step3-done.html
step3-never.html
step4-blocked.html
step4-letter-practice.html
step4-letter.html
step4-pending.html

tests/e2e/guided:
__init__.py
test_shell_smoke.py
     571 docs/GUIDED_UI_SPEC.md
     133 reviews/T-180-ux-designer.md
     704 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:54.327Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_guided_ui.md"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:54.329Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t181_guided_shell.md"
}
````

### User / tool · 2026-11-02T21:26:54.357Z

**tool result**
````
1	---
2	name: guided-ui-d068
3	description: T-180 guided four-step UI (D-068) - spec + generated static mockup; where things live, API facts the spec relies on, layout-stability recipe and pitfalls for the build card
4	metadata:
5	  type: project
6	---
7	
8	D-068 (Chris, 2026-11-02): the app becomes Your cases + a fixed 4-step guide (Add records, Check the timeline, Check the bills, Get your letter),
9	one item at a time; old screen moves to /classic. T-180 delivered `docs/GUIDED_UI_SPEC.md` and a mockup in `artifacts/mockups/guided/`
10	(pages are GENERATED by `build.py`: edit build.py/guided.css/guided.js, then `python3 artifacts/mockups/guided/build.py`; never hand-edit the html).
11	
12	**Why:** Chris: "VERY hard to use... sections move around... so simple someone's grandma can use it". Every screen must answer where am I / what now / how do I know I'm done, and nothing may move on click.
13	
14	**How to apply (build card):**
15	- API facts the spec leans on: `GET /api/cases` is local-mode only (404 public) -> public home lists tokens kept in localStorage; `status.progress.label` contains stage ids (jargon) -> map `stage` to plain copy; D-066 accept body is `compared: true` (422 COMPARE_REQUIRED, `review.judge_dispute`), not yet in api.md at T-180 time; non-charge amounts are listed in notes only when accepted (dismissed = left out); dismissed flags still appear under FLAGS DISMISSED; tray items are not in `review.counts.pending`.
16	- Queue order = the T-157 next_action rule (cited record date, undated last, record position, entry before flag, id); freeze it when the step opens.
17	- Layout checks: `check_stability.py` (click every control at 1440/390/320, compare boxes in DOCUMENT coords and scroll back to the original scrollY before measuring, else sticky bars look "moved") and `check_across_items.py` (same boxes on every review page).
18	- Pitfalls hit: `[hidden]` loses to `display:flex` (add `[hidden]{display:none!important}`); grid children need `minmax(0,1fr)` or nowrap text overflows at 320/390; a radio drawn with a thicker checked border shifts its label (use inset box-shadow); a missing third small button shifts Back/Decide later (keep an invisible placeholder, fixed widths); 320x640 cannot hold the fixed frame -> short-phone media query makes the page scroll with a sticky action bar.
19	- Real payloads for mockup content came from a `git archive HEAD` copy served with `ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated` (sample = prepared answers; library cases = recorded). Stop it by PID (hook blocks pkill).
20	
````

### User / tool · 2026-11-02T21:26:54.357Z

**tool result**
````
1	---
2	name: t181-guided-shell
3	description: T-181 (D-068) guided UI scaffold: / is app/frontend/guided with real paths, /classic old screen, G.pages contract, SERVER vs BASE in conftest, pitfalls
4	metadata:
5	  type: project
6	---
7	
8	Serving (app/backend/api.py create_app): `app/frontend` is mounted at `/classic` (explicit `/classic` -> `/classic/` redirect route, because a mount does not redirect), `app/frontend/guided` at `/` through `GuidedFiles`, a StaticFiles subclass that answers index.html for any extension-less path that is not a file (real URLs: /new, /case/<token>/records|timeline|bills|letter). /api and /classic never fall through (unknown /api path stays a JSON 404). index.html must use absolute asset URLs.
9	
10	Tests: `tests/e2e/conftest.py` has `SERVER` (root: API calls, health, guided specs) and `BASE = SERVER + "/classic"` (every classic spec navigates from BASE). Specs that start their own server and goto the app must add `/classic` (test_demo_provenance uses `_classic()`, test_count_duplicate adds it inline). Read `C.SERVER` as an attribute, not `from conftest import SERVER`, because pytest_configure rebinds it. Guided helpers (watch, go, rect, chrome) live in tests/e2e/guided/test_shell_smoke.py.
11	
12	Shell (app/frontend/guided): core.js (G, G.h builder, G.api, G.store, G.steps.states = spec 9.1/9.2 rules for the step bar, G.url) -> review.js, home.js, step1-4.js (each registers `G.pages.<home|new|records|timeline|bills|letter> = async (ctx) => cleanup?`) -> app.js (banner, header, demo pill, footer, step bar, theme, router, case load). Styles: styles.css = mockup guided.css copy + shell additions; builders edit only their own home.css/stepN.css/review.css. `.view` is `display: contents`, so a frame page's `.titlebar/.work/.actions` are body grid rows. `ctx.layout("frame"|"page")` flips body class (done screens use "page").
13	
14	Pitfalls: `replaceChildren(array)` stringifies the array (spread it). `page.evaluate("x = async () => ...")` makes Playwright CALL the returned function: wrap in `void (...)`. CSP is `style-src 'self'`: no inline style attributes in markup (CSSOM `el.style.width = ...` is fine). No innerHTML. Classic scrollbars reserve 15px in page layout: the frame needs `scrollbar-gutter: stable` too or the chrome changes width between layouts. Aborted fetches show as requestfailed ERR_ABORTED: filter them in console watchers. D-065 was amended after the spec: the prepared-answers pill tooltip/footer sentence is "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."
15	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:57.482Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/docs/GUIDED_UI_SPEC.md"
}
````

### User / tool · 2026-11-02T21:26:57.629Z

**tool result**
````
1	# Guided UI spec (T-180, D-068)
2	
3	Status: design spec for the guided four-step UI. Owner: frontend. Clickable mockup: `artifacts/mockups/guided/index.html`
4	(all screens: `artifacts/mockups/guided/screens.html`); screenshots `artifacts/screenshots/guided-mockup-*.png` at 1440x900 and 390x844.
5	Builds only on `memory/contracts/api.md` as of 2026-11-02 plus the D-066 `compared` field already in `app/backend/review.py` (T-179).
6	No new backend feature is assumed; where the API lacks something, this spec says what the screen does without it.
7	
8	Chris's brief: "<Chris's message omitted> someone's <Chris's message omitted>. 1) Multi-case management
9	<Chris's message omitted>."
10	
11	---
12	
13	## 0. Rules every screen keeps
14	
15	| Rule | How |
16	|---|---|
17	| Nothing moves when you click | The page is a fixed frame: banner, header, step bar, title row and action bar have fixed heights; only the panes inside scroll. An answer swaps text inside boxes that keep their size. No banner, toast or error is ever inserted above content after load: each has a reserved slot. `scrollbar-gutter: stable`. System fonts only (no font swap). Buttons have fixed widths, so a label change never resizes them. |
18	| No collapsing, no hidden menus | No `<details>`, accordions, dropdown menus, kebab menus or hover-only content. Every action is a visible button with words on it. |
19	| No shortcuts required | Everything works with a mouse, a finger, or Tab + Enter. Keyboard shortcuts are not offered in the guided UI. |
20	| Every screen answers three questions | **Where am I** (step bar + title row), **what do I do now** (one question or one instruction next to the buttons), **how do I know I'm done** (the "N left" count, then a done screen with a big check). |
21	| One thing at a time | Review pages show one item. The next item appears in the same boxes. |
22	| Plain words | No "judge", "LLM", "tray", "verified", "flag", "excerpt", "pending". The table in section 10 maps every internal word to the word on screen. Server sentences (`why`, `explanation`, `message`, `not_counted_reason`) are shown as given; the UI never rewrites a fact. |
23	| Honest | Every answer is saved by the server before the screen says it is saved. Provenance labels follow D-065. |
24	| Untrusted text | Record text, quotes, summaries and titles are inserted with `textContent` only. |
25	
26	The old screen moves to `/classic` (D-068) unchanged; its e2e suite keeps guarding behaviour. The guided UI gets its own suite.
27	
28	## 1. Map of screens and routes
29	
30	| Route | Screen | Mockup page |
31	|---|---|---|
32	| `/` | Your cases | `index.html`, `home-empty.html`, `home-loading.html`, `home-error.html` |
33	| `/new` | Step 1, before the case exists | `step1-add.html` |
34	| `/case/<token>/records` | Step 1: records found / drafting / done / stopped | `step1-found.html`, `step1-drafting.html`, `step1-drafting-lib01.html`, `step1-failed.html` |
35	| `/case/<token>/timeline[?item=<id>]` | Step 2, one item at a time; done screen | `step2-entry.html`, `step2-fix.html`, `step2-flag.html`, `step2-gap.html`, `step2-disputed.html`, `step2-cannot-check.html`, `step2-write.html`, `step2-date.html`, `step2-done.html` |
36	| `/case/<token>/bills[?item=<id>]` | Step 3, one amount at a time; done screen | `step3-charge.html`, `step3-count.html`, `step3-never.html`, `step3-done.html` |
37	| `/case/<token>/letter` | Step 4 | `step4-letter.html`, `step4-pending.html`, `step4-blocked.html` |
38	| `/classic` | the old review screen | (unchanged) |
39	
40	Routing is `history.pushState` with real URLs, so Back in the browser and a reload both land on the same screen. A reload of
41	`/case/<token>/timeline?item=e3` reopens that item.
42	
43	## 2. Global frame
44	
45	### 2.1 Synthetic banner (every page, fixed, 32 px; 40 px on phones)
46	Text: `health.banner` ("Synthetic data only — never paste real records"). Warm yellow background, dark text, centred.
47	On phones the banner also carries the demo label (2.3), so provenance is never off-screen.
48	
49	### 2.2 Header (every page, fixed, 64 px; 52 px on phones)
50	- Left: product mark + "Treatment Timeline" (home), or "‹ Your cases" button + case title (inside a case). The title is the API `title`,
51	  one line, ellipsis. On phones: "‹ Cases" + title.
52	- Right: the demo label (2.3) on desktop, then a "Dark mode" / "Light mode" text button (theme; default follows the OS; remembered in
53	  `localStorage` inside try/catch).
54	
55	### 2.3 Demo provenance (D-065)
56	`GET /api/health` `answers`:
57	
58	| `answers` | Label (pill, always visible) | Footer sentence (visible, not a tooltip) | Item tag |
59	|---|---|---|---|
60	| `prepared` | Demo: sample answers prepared by our team | The AI's own answers on these cases are in the evaluation report. | "Prepared answer" when `item.prepared`, else "AI draft" |
61	| `recorded` | Demo: recorded AI answers | These are real AI answers recorded earlier; nothing new is sent to an AI. | "AI draft" |
62	| `live` | (no pill) | Summaries and warnings are drafted by AI and checked by code; you decide every item. | "AI draft" |
63	
64	A manual entry (`entered_by_reviewer`) or a summary she wrote is tagged "Written by you". `ai_banner` is shown under the step title on
65	Steps 2 and 3 (desktop) and on each step's done screen (all widths). Removing jargon never removes provenance.
66	
67	### 2.4 Step bar (inside a case; fixed, 76 px; 60 px on phones; never moves, never changes height)
68	Four equal segments joined by a line: **1 Add records · 2 Check the timeline · 3 Check the bills · 4 Get your letter**
69	(phones: Records · Timeline · Bills · Letter). Each segment: a 32 px circle, the label, one status line.
70	
71	| State | Circle | Status line | Click |
72	|---|---|---|---|
73	| done | green circle with a check | "Done" | opens the step (to look or change answers) |
74	| current (the step on screen) | filled accent circle (number, or a check when that step is done), accent bar under the segment, bold label, `aria-current="step"` | e.g. "16 of 19 left" | opens the step |
75	| remaining | grey outline circle with the number | e.g. "4 amounts" / "Not started" | opens the step |
76	| locked | grey outline, label at 60% | "After step 1" | not clickable (`aria-disabled`) |
77	| needs attention | amber circle with "!" (a step she left with undecided items, a stopped run, an export problem) | e.g. "Run again" / "2 left" / "1 problem" | opens the step |
78	
79	Steps 2–4 are locked until the case has items (`status` is `ready`, or `failed` with items; see 4.5). The step bar is a
80	`<nav aria-label="Steps">` of links. Status lines are computed from GET case (section 9.2), text only, fixed width.
81	
82	### 2.5 Title row (review pages; fixed, 72 px; 52 px on phones)
83	Left: eyebrow "Step 2 of 4" and h1 "Check the timeline". Right: "Item 4 of 19" and a progress bar (fixed 240 px; full width on
84	phones) with "3 answered · 16 to go". Step 3 adds a fixed-width "Bill total so far: $6,240.00" chip (`totals.accepted.cents`).
85	
86	### 2.6 Action bar (review pages; fixed to the bottom; fixed height)
87	Three rows, always present, never re-laid out:
88	1. **The question** (20 px, semibold), max two lines (reserved).
89	2. **Two big answers**, equal size (56 px tall, 260 px wide on desktop; half width each on phones). The first is filled accent,
90	   the second outlined. Equal size on purpose: neither is a reflex click.
91	3. **Small buttons** of one fixed width (172 px; equal thirds on phones): "‹ Back", the item's third action ("Fix the wording" /
92	   "Add a note"; an invisible placeholder keeps the slot when an item has none, so Back and Decide later never move), "Decide later"; then the
93	   **status slot** (`aria-live="polite"`, one line, reserved): "Saved: item 3 kept in the letter. Undo".
94	
95	When an answer is not allowed yet (a confirm box is not ticked, a code check fails), the button stays where it is, disabled, and the
96	reason is in the item card's footer slot (2.7). Errors from the server go in the same footer slot, never in a new banner.
97	
98	### 2.7 Item cards (review pages)
99	Desktop: two columns of equal width inside the work area. **Left: "From the record"** (the source). **Right: the line to check.**
100	Phones: the source on top (flexible height, scrolls), the line card below it (fixed 180 px, scrolls inside).
101	
102	- **Source card.** Header: "Record 3 · Dr. Alvarez, primary care · January 16, 2026" (record `seq`, `source_label`, long date).
103	  Body: the record text at 18 px/1.6 with the quote in a yellow `<mark>` (offsets `excerpt_start/end` into the case text, minus
104	  `char_start`). On open the card scrolls **inside itself** so the mark is in view; the page never scrolls. Several records (a flag with
105	  evidence in two records) are stacked in the same card, each with its header. Footer (when `records[].uncovered` is not empty):
106	  "Also in this record, not in any line:" + each sentence in quotes (read only).
107	- **Line card.** Header: tag (2.3) and the date + provider. Body: the summary at 22 px. **Footer slot** (fixed min-height 112 px):
108	  the plain check sentence (`why`), or a confirm checkbox, or a refusal message, or "Your answer: ..." when she comes Back.
109	
110	### 2.8 Footer (every page)
111	One line: the provenance sentence (2.3) and, in live mode, "Pasted text is deleted after `retention_hours` hours."
112	
113	## 3. Your cases (home, `/`)
114	
115	**Where am I:** h1 "Your cases". **What do I do now:** each card's "Next:" line and its one Continue button. **Done:** a case moves to
116	"Finished" with a green "Letter ready".
117	
118	Layout: title row with h1, one sentence ("Each case goes through 4 steps. Pick up where you left off."), and the primary
119	"Start a new case" button (top right; full width on phones). A "Find a case" search box shows when there are 6 or more cases
120	(filters by title as she types; the only thing on the page that changes the list, and only on typing). Two sections, always open:
121	**In progress (N)** and **Finished (N)**. Cards in a grid: 2 columns at ≥ 1100 px, 1 column below. Sorted by `last_activity_at`,
122	newest first.
123	
124	### 3.1 Case card (fixed height 236 px desktop; content clamps)
125	```
126	Jordan Rivera (sample)                               [Rename]
127	Started Nov 2 · 9 records
128	(1)✓ Add records — (2) Check the timeline — (3) Check the bills — (4) Get your letter
129	Next: Check the timeline. 16 of 19 items left.
130	[        Continue        ]                          [Delete]
131	```
132	- Title: `title` (text only). "Rename" turns the title into an input in the same box with "Save" / "Cancel" (PATCH `{title}`;
133	  `422 invalid_title` message shown under the input in a reserved line).
134	- Mini step track: the four steps with the same states as the step bar (2.4), small.
135	- **Next line** (one rule, section 9.3) and the **Continue** button (one per card, full card width minus Delete).
136	- "Delete": the card's bottom row turns into "Delete this case and all its answers? [Yes, delete] [Keep it]" in the same row
137	  (DELETE `/api/cases/{token}`; the card is then removed, which is the one allowed layout change, caused by her own confirm).
138	- A card whose summary failed (`status_error: true`): body shows `status_error_message` ("We couldn't load this case's status")
139	  instead of the track and the Next line; button "Open case".
140	
141	### 3.2 Next line + Continue target (per case)
142	| Case state | Next line | Continue goes to |
143	|---|---|---|
144	| `ingested` (records read, not drafted) | Next: Draft the timeline. | Step 1 (records found) |
145	| `running` | Next: Wait while the timeline is drafted (stage N of 8). | Step 1 (drafting) |
146	| `failed` | Next: Drafting stopped. Run it again. | Step 1 (stopped) |
147	| Step 2 has undecided items | Next: Check the timeline. N of M items left. | first undecided Step 2 item |
148	| Step 3 has undecided items | Next: Check the bills. N of M amounts left. | first undecided Step 3 item |
149	| gate blocker on a decided item (`next_action.kind` is entry/flag/amount and that item is decided) | Next: Fix 1 problem before the letter. + `next_action.reason` | that item |
150	| everything decided, gate ready | Finished. Your letter is ready. (green) | Step 4; button reads "Open letter" |
151	
152	### 3.3 Multi-case in local and public mode
153	- Local mode (`ZLAYT_MODE=local`): the list is `GET /api/cases` (every case on this computer).
154	- Public / demo mode: `GET /api/cases` is `404` by design (no case list; the token is the only credential). The home then lists the
155	  cases **this browser started**: their tokens are kept in `localStorage` (`zl.guided.cases`, try/catch) when POST `/api/cases`
156	  answers, and each card is filled from `GET /api/cases/{token}`. A `404` card reads "This case is no longer here. Cases are kept for
157	  `retention_hours` hours." with "Remove from this list". A line under the h1 says "These are the cases started in this browser.
158	  Keep the case link to open it elsewhere." No server feature is added.
159	
160	### 3.4 Home states
161	| State | Screen |
162	|---|---|
163	| Loading | The title row, then 3 grey skeleton cards of the final card size (no jump when they fill). |
164	| Empty | Large icon, "You don't have any cases yet.", "A case is one client's medical records. We'll guide you through 4 steps.", buttons "Start a new case" and "Try the sample case" (POST `{sample: true}`, then Step 1). |
165	| Error | "We couldn't load your cases." + the server `message` when there is one + "Try again" (refetch; focus returns to the h1). |
166	
167	## 4. Step 1 — Add records (`/new`, then `/case/<token>/records`)
168	
169	**Instruction:** "Add the medical records for this case. We'll read them and draft a timeline for you to check."
170	
171	### 4.1 Before the case exists (`/new`)
172	- "Name this case (optional)" text input (sent as `title`; 120 characters max, no `<` `>`; the 422 message shows under it).
173	- Three big choice tiles, side by side (stacked on phones), each a radio with a picture-free heading and one line:
174	  **Paste text** ("Copy the records and paste them here") · **Upload a file** (".txt or .pdf, up to 5 MB") ·
175	  **Use the sample case** ("A short synthetic case to try it out").
176	- Below the tiles, one fixed-height box (280 px) that shows the chosen input: a textarea, a file drop area with "Choose a file", or
177	  "The sample has 9 short records from a fictional car-accident case." The box does not change size between choices.
178	- Primary button: **Read the records** (disabled until there is text, a file, or the sample is chosen).
179	- Demo mode line (when `health.demo_mode`): "This demo can only read the sample and our test cases."
180	
181	| Control | API |
182	|---|---|
183	| Read the records (paste) | `POST /api/cases {text, title}` |
184	| Read the records (.txt) | read in the browser, then the same POST |
185	| Read the records (.pdf) | `POST /api/cases/pdf?title=` raw bytes, `Content-Type: application/pdf` |
186	| Read the records (sample) | `POST /api/cases {sample: true, title}` |
187	
188	Errors (shown in a reserved line under the box, plain words, with the action):
189	
190	| Code | Message on screen | Action |
191	|---|---|---|
192	| `400 bad_request` empty | There's nothing to read yet. Paste the records or choose a file. | — |
193	| `413 input_too_large` | That's more than we can read at once (60,000 characters or 40 records). Split it into two cases. | — |
194	| `409 demo_mode_unsupported_input` | This demo can only read the sample and our test cases. | "Use the sample case" |
195	| `400 pdf_no_text_layer` | This PDF looks scanned, so it has no text we can read. | "Read the scanned pages" (re-post with `ocr=true`) when `detail.ocr.status.available` |
196	| `400 pdf_encrypted` / `pdf_unreadable` / `pdf_timeout` | the server `message` | "Choose another file" |
197	| `400 pdf_only_hidden_text` | Everything on these pages is hidden text, so we kept it out. | "Use these pages anyway" (re-post `include_hidden=all`, after a confirm checkbox "I looked at these pages myself") |
198	| `429 busy` | We're reading other files right now. Try again in a moment. | "Try again" |
199	| network / 5xx | We couldn't reach the server. Your text is still here. | "Try again" |
200	
201	### 4.2 Records found (`status: ingested`)
202	Heading "We found 9 records". A fixed list (scrolls inside its box) of rows: "1 · January 9, 2026 · Austin EMS run report".
203	Plain notes above the list in a reserved slot, from the POST/GET response:
204	- `dates_to_confirm` not empty: "1 record has a date we need you to check. You'll do that in step 2."
205	- warning `PHI_PATTERN`: "Some text looks like real personal details (a phone, SSN or record number). Only use synthetic records."
206	- warning `SPLIT_AMBIGUOUS` / `UNSPLIT_TEXT`: "Some text didn't look like a record. We kept it as its own record so nothing is lost."
207	- `injection.banner`: shown as given.
208	Primary: **Draft the timeline** → `POST /api/cases/{token}/run {confirm_rerun: false}`. Secondary: "Start over with other records" (`/new`).
209	
210	### 4.3 Drafting (`status: running`)
211	Poll `GET /api/cases/{token}/status` every second. A fixed checklist of the 8 stages (never the raw stage id or `progress.label`,
212	which contains ids). Done stages get a green check, the current one a spinner and "(4 of 9)" from `progress.done/total` when the stage
213	counts items, the rest are grey. A progress bar above shows stages done / 8. Copy:
214	
215	| `stage` | Live / recorded | Prepared (`answers: prepared`) |
216	|---|---|---|
217	| `ingest` | Reading the records | Reading the records |
218	| `extract` | Writing one line for each record | Loading the prepared line for each record |
219	| `verify` | Checking every quote word for word | Checking every quote word for word |
220	| `judge_entries` | Double-checking each line a second way | Double-checking each line a second way |
221	| `amounts` | Finding the bill amounts | Finding the bill amounts |
222	| `conflicts` | Comparing the records with each other | Comparing the records with each other |
223	| `flags` | Looking for things the attorney should know | Looking for things the attorney should know |
224	| `finalize` | Putting it all together | Putting it all together |
225	
226	Under the list: "This usually takes under a minute. You can leave this page; we'll keep going." (Home shows the same progress.)
227	
228	### 4.4 Done (`status: ready`)
229	The same box shows a big green check: "All set. 19 timeline items and 4 bill amounts are ready for you to check." (counts from
230	`status.counts`, entries + flags, amounts) + the `ai_banner` sentence + primary **Go to step 2: Check the timeline**. Step 1 turns done.
231	
232	### 4.5 Stopped (`status: failed`)
233	Amber box: "Drafting stopped before it finished." + `error.message` as given (it already says decisions were kept) + **Run it again**
234	→ `POST .../run {confirm_rerun: false}`; on `409 needs_confirm` the same box shows "Run it again? Your answers so far are kept." with
235	**Yes, run it again** (`confirm_rerun: true`) / **Cancel**. Items the run did finish can be checked meanwhile: steps 2–3 open.
236	`error.records` (extract failures) are named: "No line was written for records 2 and 7. You can write them yourself in step 2."
237	
238	After a case is drafted, Step 1 shows the records list read-only with "To add more records, start a new case." (There is no API to add
239	records to a case.)
240	
241	## 5. Step 2 — Check the timeline (`/case/<token>/timeline`)
242	
243	### 5.1 The queue
244	Built in the browser from one `GET /api/cases/{token}`, once, when the step opens; it never re-sorts while she works.
245	Contents: every entry in `entries` and `undated_entries`, every flag in `flags`, every `tray` item (could not check). Not included:
246	`tray_filtered` (listed read-only on the done screen), amounts (Step 3). Order: the `next_action` timeline rule (api.md, T-157 step 3):
247	by the date of the record the item cites (earliest when several; undated last), then that record's position, then entry before flag,
248	then id. So a flag sits right after the line it is about. Sample case: 9 lines + 10 warnings = 19 items.
249	
250	Opening the step lands on the first undecided item (or `?item=`). After an answer the next undecided item opens in the same boxes.
251	"‹ Back" opens the previous item (decided or not). "Decide later" moves on without saving. When no undecided item is left, the done
252	screen (5.8) opens.
253	
254	Every write sends `version` and `expected_status` from the item on screen (T-178). On `409 stale_item`: footer slot shows "This item
255	changed in another tab. We've loaded the latest." and the item is re-read (`GET .../items/{id}` or the case).
256	
257	### 5.2 A timeline line (entry) — `step2-entry.html`
258	- Line card: tag, "January 16, 2026 · Dr. Alvarez, primary care", the summary. Footer: `why` ("Quote found word for word, every number
259	  in the summary is in the quote, and the second check agreed.").
260	- **Question:** "Does this line say the same thing as the highlighted words?"
261	- **Yes, this matches** → `POST .../items/{id}/review {action: "accept", version, expected_status}`. Saved text: "Kept in the letter."
262	- **No, leave it out** → `{action: "dismiss"}`. Saved text: "Left out of the letter."
263	- **Fix the wording** → 5.3.
264	- Status slot after an answer: "Saved: item 4 kept in the letter. Undo" (Undo = `{action: "reset"}` on that item, then reopen it).
265	
266	Refusals, shown in the footer slot with the button disabled and the way out made the primary small action:
267	
268	| Server says | Footer slot | Way out |
269	|---|---|---|
270	| item `reasons` include a code-check reason (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_NUMBER_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CHARGE_TEXT_IN_ENTRY`, `EXCERPT_*`, `GROUNDING_EXCERPT_NOT_VERBATIM`), or `422 CODE_CHECK_FAILED` | the `why` / `message` as given | "Fix the wording" (or "Change the highlighted words" for `EDIT_QUOTE`) |
271	| `422 DATE_UNCONFIRMED` | "Pick the right date first." | the date question (5.6) |
272	| `422 COMPARE_REQUIRED` | 5.4 | tick the box |
273	| `409 item_rejected` | the item is shown as could-not-check (5.5) | — |
274	
275	### 5.3 Fix the wording — `step2-fix.html`
276	The line card body becomes a textarea with the current summary, same box. Above it: "Change the line so it says only what the
277	highlighted words say. Numbers, left/right and words like 'no' or 'possible' must match." The question row reads "Change the line,
278	then save it." The two big buttons become **Save my wording** / **Cancel** (same places). The source card adds one line at the top:
279	"To change which words are highlighted, tap whole sentences below." Sentences (`records[].sentences`) become tappable (outlined); the
280	chosen run is the new quote (contiguous whole sentences only; a gap in the run is refused in the browser with "Pick sentences that
281	follow each other.").
282	
283	| Control | API |
284	|---|---|
285	| Save my wording (summary changed) | `{action: "edit", edits: {summary}}` |
286	| Save my wording (quote changed) | `{action: "edit", edits: {excerpt}}`; both changed: two calls, quote first |
287	| Cancel | nothing sent |
288	
289	`422 invalid_edit` → the server `message` in the footer slot ("The summary says “left”, which the quote does not say. Remove it or
290	change the quote."); the text stays in the box. On save, the response item is shown: when `edit_to_check` is true the card goes to
291	5.4 with "You changed the wording. Read it against the highlighted words once more."; `warnings[]` messages (for example
292	`CHARGE_CLAUSE_REMOVED`) are shown in the footer slot.
293	
294	### 5.4 Compare confirm (D-066, and an edit still to check) — `step2-disputed.html`
295	When the item is disputed (its ladder verdict or reasons say `partially` / `unsupported` / `disagrees`, the same rule as
296	`review.judge_dispute`) **or** `edit_to_check` is true:
297	- Footer slot (amber): the dispute sentence (the item `why`, e.g. "The second check found this only partly supported by the
298	  quote.") and a 28 px checkbox: **"I read this line against the highlighted words myself."**
299	- "Yes, this matches" is disabled until the box is ticked; then it sends `{action: "accept", compared: true, version,
300	  expected_status}`. "No, leave it out" and "Fix the wording" are always enabled.
301	- The box is never pre-ticked and is cleared when the item changes.
302	
303	### 5.5 Could not check — `step2-cannot-check.html`, `step2-write.html`
304	A `tray` item. Line card header: "We couldn't check this one" (amber), body: the `why` as given, then "What was suggested (not
305	used): “Visit 8: pain 4/10, improving.”" (`attempt.summary`, quoted, muted). The source card shows the whole record without a
306	highlight (`attempt.excerpt` is not in the record, so nothing is marked).
307	- Tray **entry**: **Question:** "Read the record. Do you want to write this line yourself?" **Write it myself** → the write screen;
308	  **Skip it** → `{action: "dismiss"}` on the tray item ("Skipped. It stays out of the letter.").
309	- Write screen: the record's `sentences` are tappable (pick whole sentences that follow each other; the picked ones turn yellow); the
310	  line card is a textarea "Your line for the timeline". Buttons **Save my line** / **Cancel**. Save → `POST /api/cases/{token}/records/
311	  {rid}/entry {summary, excerpt}`. `422 invalid_edit` → message in the footer slot. `201` → the new item (`e<n>_m`, tag "Written by
312	  you") opens in the normal line question (5.2) at the same queue position.
313	- Tray **flag** (the second check disagreed with a suggested warning): header "We couldn't confirm this warning", body `why`, the
314	  suggested warning `attempt.summary` and its quote. **Question:** "This warning can't go in the notes. Read it; if it matters, tell the
315	  attorney yourself." **OK, leave it out** → `{action: "dismiss"}`; **Decide later** in the second slot.
316	- Tray items are optional: they never count in "N left" (the server leaves them out of `review.counts.pending`), and the item counter
317	  says "Optional".
318	
319	### 5.6 A date to pick — `step2-date.html`
320	An entry in `undated_entries` whose record is in `dates_to_confirm` with `candidates`.
321	- Source card: the record with its `Date:` line marked.
322	- Line card header "Which date is right?", body: "The record says 04/05/2026. That could be two different dates." The two answers
323	  are the two candidates as long dates ("April 5, 2026" / "May 4, 2026"), each with its reading in small text ("month first" / "day
324	  first"). When `suggestion.iso` is set, that button carries a "Suggested" chip and the footer shows `suggestion.reason`
325	  ("4 other dates in this packet use month first..."). Nothing is chosen on load.
326	- **Question:** "Which date is right for this record?" → `POST /api/cases/{token}/records/{rid}/confirm_date {date}`.
327	  Response `gap_changes[].sentence` goes in the status slot ("Gap recalculated after you confirmed record 4: now 40 days (was 42).").
328	  The same item then shows the normal line question (5.2), "part 2 of 2" beside the counter.
329	- `missing` date (no candidates): "We couldn't find a date in this record, so it can't go on the timeline." One answer
330	  **OK, leave it out** (`dismiss`); the second slot is "Decide later".
331	
332	### 5.7 A warning for the attorney (flag) — `step2-flag.html`, `step2-gap.html`
333	Warnings never go in the letter; accepted ones go in the internal notes (D-001). The line card becomes a warning card:
334	- Header: a fixed plain heading by type (below) + "Warning for the attorney".
335	- Body: `title` (bold) and `explanation` as given; for a gap with `computed.endpoint_warnings`, each `warning` and `alternative`
336	  sentence as given; `gap_change.sentence` when set.
337	- Source card: every `evidence[]` excerpt marked in its record (several records stacked).
338	- Footer: "Warnings only go in the notes for the attorney, never in the letter."
339	- **Question:** "Should the attorney be told about this?" **Yes, tell the attorney** → `{action: "accept"}`;
340	  **No, not needed** → `{action: "dismiss"}` (it is then listed under "Flags dismissed" in the notes, so the attorney can see what was
341	  ruled out). Third action **Add a note** → a textarea in the card, **Save note** / **Cancel** → `{action: "edit", edits: {note}}`.
342	
343	| `type` / `category` | Plain heading |
344	|---|---|
345	| `gap` | A break in treatment (`computed.conditional`: A possible break in treatment) |
346	| `conflict` / `accident_date_*` | The records disagree about the accident date |
347	| `conflict` / `treatment_plan_vs_actual` | The plan and what happened differ |
348	| `conflict` / `provider_name_variant` | The provider's name is written differently |
349	| `conflict` / other | The records disagree |
350	| `pre_existing` / `pre_existing`, `prior_surgery` | An earlier health problem is mentioned |
351	| `pre_existing` / `degenerative_language` | Wording about wear and tear |
352	| `causation` / `patient_report` | The patient, not a doctor, says what caused it |
353	| `causation` / `speculative_language` | Hedged wording ("may", "possible") |
354	| `causation` / `missed_care` | Missed or ended treatment |
355	| `causation` / `new_onset` | Wording about a new problem |
356	| `causation` / `accident_date_provenance` | Where the accident date comes from |
357	| `causation` / `credibility_language` | Wording about the patient's effort or credibility |
358	| `causation` / other | Wording the other side could use |
359	| `record_warning` / `injection_suspected` | This record contains text that looks like instructions to a computer |
360	| `record_warning` / `date_ambiguous` | This record's date is unclear |
361	| `record_warning` / `analysis_incomplete` | We couldn't finish comparing these records |
362	| `record_warning` / other | Something to check in this record |
363	
364	### 5.8 Step 2 done — `step2-done.html`
365	Shown when no undecided item is left (or from the step bar when the step is done).
366	- Big green check + "You checked every item on the timeline." + counts in one line: "8 kept in the letter · 1 left out ·
367	  7 warnings for the attorney · 3 not needed".
368	- If some are undecided instead: amber "2 items still need a decision." + **Go to the first one**.
369	- "Your answers": a plain list of all items in queue order, one row each: date, short label (entry: provider; warning: plain
370	  heading), the answer chip ("Kept", "Left out", "Tell the attorney", "Not needed", "Skipped", "Not decided") and a **Change** button
371	  (opens that item). Read-only "Suggestions a rule ruled out (nothing to do)": `tray_filtered.rules[]` label + `explanation` +
372	  each item's quote, when `count` > 0. `checks` (T-151): "We checked for: <labels of conflict_types>. Not checked: <not_checked labels>."
373	- Primary: **Go to step 3: Check the bills** (or step 4 when the case has no amounts).
374	
375	## 6. Step 3 — Check the bills (`/case/<token>/bills`)
376	
377	Queue: every item in `amounts[]` in this order: charges and countable amounts first (record order, then position), then the
378	never-counted ones. One at a time, same frame as Step 2. Charges are never batched (D-059); there is no "count all".
379	
380	### 6.1 A charge — `step3-charge.html` (`kind: "charge"`)
381	- Line card ("Bill amount"): the figure as money in 40 px ("$6,240.00" from `value_cents`), "Central ER discharge summary ·
382	  January 9, 2026", footer "If you count it, it's added to the bill total in the letter."
383	- **Question:** "Should this charge count toward the bill total?"
384	- **Yes, count it** → `{action: "accept"}`; **No, don't count it** → `{action: "dismiss"}`.
385	- The title-row chip updates from the response `totals.accepted` ("Bill total so far: $6,240.00").
386	- **D-059 flagged charge** (`flag` set, `confirm_required: true`): footer shows `flag.message` as given and a checkbox named by the flag:
387	  `likely_duplicate` "I checked: this is a separate charge, not the same one counted twice."; `likely_total` "I checked: this is a
388	  charge of its own, not a total of the others." "Yes, count it" is disabled until ticked, then sends `{action: "accept", confirm:
389	  flag.confirm_with}`. On `422 CONFIRM_REQUIRED` the footer shows `detail.message`.
390	
391	### 6.2 An amount that can be counted with a check (D-064 b) — `step3-count.html`
392	`countable: true`. Line card: the figure, "Not counted yet" chip, `not_counted_reason` as given ("The line states no date of service,
393	so it is not an itemized service line and is not totaled."). Footer: checkbox **"I checked this is a separate charge for a service."**
394	and, when `count_confirm` is set, `count_confirm.message` + a second checkbox named as in 6.1.
395	- **Yes, count it** (enabled when the box or boxes are ticked) → `{action: "count", confirm: "separate_charge"}` plus
396	  `confirm_flag: count_confirm.confirm_with` when set.
397	- **No, don't count it** → `{action: "accept"}` (it is noted for the attorney under "Amounts not totaled", never in the total).
398	
399	### 6.3 An amount that is never counted (D-064 a) — `step3-never.html`
400	`countable: false` and not a charge (rate, total, balance, payment, adjustment, damages, estimate...). Line card: the figure as
401	written (`text`), "Never counted" chip, `not_counted_reason` as given. Footer: "Either way, it is never added to the bill total."
402	- **Question:** "This amount is never added to the total. List it in the notes for the attorney?"
403	- **Yes, list it** → `{action: "accept"}` (rates: `accept_effect: acknowledge`); **No, leave it out** → `{action: "dismiss"}`.
404	
405	### 6.4 Step 3 done — `step3-done.html`
406	Big check + "You checked every bill amount." + the letter's total line exactly as the export writes it, large:
407	"Billed charges accepted from these records: $8,390.00" (`totals.letter_line` when present, else built from
408	`totals.accepted.cents`). Three plain lists, always open: **Counted** (figure, provider, date), **Not counted by you**, **Never
409	counted** (figure, where, `not_counted_reason`). `totals.possible_overlaps[]`: each `message` as given in an amber box above the
410	lists, with "Change" buttons on both figures. Primary: **Go to step 4: Get your letter**.
411	A case with no amounts: "We didn't find any bill amounts in these records." + **Go to step 4**.
412	
413	## 7. Step 4 — Get your letter (`/case/<token>/letter`)
414	
415	Data: `GET /api/cases/{token}/export` (and GET case for the counts). Layout: the letter on the left (wide, white "paper" box, 17 px,
416	`white-space: pre-wrap`, scrolls inside), the notes for the attorney on the right (narrower, tinted box headed "Notes for the attorney
417	— do not send"). Phones: letter first, then notes; each box fixed height with its own scroll.
418	
419	### 7.1 Ready — `step4-letter.html`
420	Green status row: "Your letter is ready. Every item has an answer." Buttons under the letter: **Copy letter** (primary),
421	**Download letter (.txt)**. Under the notes: **Copy notes**, **Download notes (.txt)**. Copy → `navigator.clipboard.writeText
422	(letter_text)`; the button reads "Copied" for 2 s at the same width. Download → a Blob named `<title>-letter.txt` /
423	`<title>-notes.txt` (code, client side). A plain box "Exhibit and page numbers (optional)": three inputs Exhibit, Bates prefix,
424	First number + **Save** → `PUT /api/cases/{token}/export_config` then re-GET export (`422 invalid_edit` message under the inputs).
425	No drafted treatment paragraph anywhere (D-067).
426	
427	### 7.2 Undecided items — `step4-pending.html`
428	`review.counts.pending + review.counts.edit_to_check` > 0 (the export is still allowed, D-045a):
429	amber row "3 items still need a decision. If you don't decide them, they stay out of the letter." + **Go to the first one** (the
430	first undecided item in step order: Step 2 queue, then Step 3). The letter preview shows what would be sent now. Copy and Download are
431	disabled until the checkbox "Copy it anyway, without those 3 items" is ticked (the one confirmation before copying the contract asks
432	for). The checkbox sits in a reserved row; it is not shown once the count is 0.
433	
434	### 7.3 Blocked — `step4-blocked.html`
435	`422 export_blocked` / `judge_not_run`: red row "The letter can't be made yet." and one row per `detail.blockers[]`: its `why` as
436	given + a button by `next_action.code`:
437	
438	| `next_action.code` | Button |
439	|---|---|
440	| `DECIDE` (`NOTHING_ACCEPTED`) | Go to step 2 |
441	| `EDIT_SUMMARY` / `EDIT_QUOTE` | Fix it (opens the item in Fix the wording) |
442	| `DISMISS_OR_ENTER_BY_HAND` | Go to it |
443	| `RERUN_JUDGE` | Run the second check again (`POST .../rejudge`, only when the item's `rerun_available`; else the text "The second check can't run here. Fix the wording in your own words, or leave the item out.") |
444	| `CONFIRM_RERUN` (`RUN_FAILED`) | Go to step 1 |
445	| `RUN_IN_PROGRESS` | (text) Wait for drafting to finish |
446	
447	The letter box keeps its size and shows "Your letter will appear here once the problem above is fixed."
448	
449	### 7.4 Done
450	Step 4 is done (green in the step bar, "Finished" on home) when steps 2 and 3 have nothing undecided and the export answers 200.
451	
452	## 8. Visual system
453	
454	- **Type:** system stack (`"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial`), `rem` on a 16 px root. Body 18/28,
455	  record text 18/29, the line to check 22/32, question 20/28, h1 32/40 (26/32 phones), small 15/22 (never below 14).
456	  Money and counts `tabular-nums`.
457	- **Spacing:** 8 px grid; page gutter 32 px desktop, 16 px phones; cards 24 px padding (16 phones); 16 px between cards.
458	- **Shape:** cards radius 14 px, buttons 12 px, chips 999 px; borders 1 px; one soft shadow on the action bar and cards.
459	- **Colour:** one accent (blue `#0B57D0`, dark `#8AB4FF`) for the current step, primary buttons, focus ring and links. Status colours
460	  only for meaning: green done/kept, amber needs a decision, red blocked; yellow `<mark>` for the quote. Light and dark sets on
461	  `:root` (`prefers-color-scheme`, overridden by `data-theme`); every text pair ≥ 4.5:1, control edges ≥ 3:1 (values: mockup
462	  `guided.css`, reusing `docs/UI_DESIGN_BRIEF.md` §4 where they overlap).
463	- **Targets:** big answers 56 px tall; every other control ≥ 48 px; checkboxes 28 px with the whole label clickable.
464	- **Focus:** 3 px accent ring, offset 2 px, on every control. After an answer focus moves to the first answer button of the next item.
465	- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons
466	  in one row below); the line card is a fixed 256 px, the source card takes the remaining height; no horizontal scroll anywhere.
467	- **Short phones (height ≤ 720 px and width ≤ 760 px, e.g. 320x640 or landscape):** the fixed frame would leave no room for the record,
468	  so the review page scrolls as a normal page; the action bar is `position: sticky; bottom: 0`, the source card body is capped at 260 px.
469	  Clicking still moves nothing (checked by the mockup test at 320x640).
470	
471	## 9. Data rules (code in the browser; deterministic)
472	
473	### 9.1 What counts as undecided
474	An item is undecided when it is live (not `rejected`) and `review_status` is `pending`, or `edit_to_check` is true. Step 2 =
475	entries, undated entries and flags; Step 3 = amounts. "N items still need a decision" = `review.counts.pending +
476	review.counts.edit_to_check` (the same number as home's `hitl.pending + hitl.edits_to_check`).
477	
478	### 9.2 Step states
479	| Step | done when | status line |
480	|---|---|---|
481	| 1 | `status` is `ready` | "Done" / "Drafting 4 of 8" / "Run again" / "Not started" |
482	| 2 | no undecided Step 2 item | "Done" / "16 of 19 left" |
483	| 3 | no undecided amount | "Done" / "4 amounts" / "3 of 4 left" / "None found" (then done) |
484	| 4 | steps 2 and 3 done and the export gate is ready (`GET /trace` `export_gate.ready`, or home's `export_ready`) | "Ready" / "1 problem" / "Not yet" |
485	
486	Current step = the first step not done. Home uses `GET /api/cases` `progress.entries + progress.flags` (Step 2) and
487	`progress.amounts` (Step 3); inside a case the same counts come from GET case.
488	
489	### 9.3 Next line
490	Section 3.2, in that order. The only server sentence used is `next_action.reason` for a gate problem.
491	
492	## 10. Words on screen
493	
494	| Internal | On screen |
495	|---|---|
496	| entry | line (on the timeline) |
497	| excerpt / quote | the highlighted words |
498	| accept / dismiss (entry) | Yes, this matches / No, leave it out |
499	| flag | warning for the attorney |
500	| accept / dismiss (flag) | Yes, tell the attorney / No, not needed |
501	| charge accepted / dismissed | counted / not counted |
502	| tray, rejected, could-not-verify | We couldn't check this one |
503	| judge, second check, J1–J4 | the second check |
504	| verified / needs_review | (not shown; the question and the footer sentence carry it) |
505	| pending | not decided |
506	| internal notes | notes for the attorney |
507	| export | your letter |
508	| run / LLM run | drafting the timeline |
509	| token | case link |
510	
511	## 11. API mapping (every control)
512	
513	| Screen | Control | Call | Fields read |
514	|---|---|---|---|
515	| all | banner, demo label, footer | `GET /api/health` | `banner`, `answers`, `ai_banner`, `demo_mode`, `retention_hours`, `sample_available` |
516	| home | list | `GET /api/cases` (local) or `GET /api/cases/{token}` per stored token (public) | `title`, `created_at`, `last_activity_at`, `record_count`, `status`, `run`, `progress`, `hitl`, `export_ready`, `next_action`, `status_error*` |
517	| home | Rename / Save | `PATCH /api/cases/{token} {title}` | `title` |
518	| home | Delete / Yes, delete | `DELETE /api/cases/{token}` | — |
519	| home | Start a new case | route `/new` | — |
520	| home (empty) | Try the sample case | `POST /api/cases {sample: true}` | `token` |
521	| 1 | Read the records | `POST /api/cases` or `POST /api/cases/pdf` | `token`, `records[]`, `dates_to_confirm`, `warnings[]`, `injection` |
522	| 1 | Draft the timeline | `POST /api/cases/{token}/run {confirm_rerun:false}` | `status` |
523	| 1 | progress | `GET /api/cases/{token}/status` (1 s) | `status`, `stage`, `progress.done/total`, `counts`, `error` |
524	| 1 | Run it again / Yes, run it again | `POST .../run` (`confirm_rerun: true` after `409 needs_confirm`) | — |
525	| 1 | Read the scanned pages / Use these pages anyway | `POST /api/cases/pdf?ocr=true` / `?include_hidden=all` | — |
526	| 2, 3 | load | `GET /api/cases/{token}` | `entries`, `undated_entries`, `flags`, `amounts`, `tray`, `tray_filtered`, `records[].text/sentences/uncovered/char_start`, `dates_to_confirm`, `review`, `totals`, `checks`, `next_action` |
527	| 2 | Yes, this matches | `POST .../items/{id}/review {action:"accept", version, expected_status}` (+ `compared: true` after the 5.4 box) | `item`, `review`, `totals`, `warnings` |
528	| 2 | No, leave it out / Skip it / OK, leave it out | `{action:"dismiss"}` | same |
529	| 2, 3 | Undo / Change (back to undecided) | `{action:"reset"}` | same |
530	| 2 | Save my wording | `{action:"edit", edits:{summary}}` / `{edits:{excerpt}}` | `item.edit_to_check`, `warnings` |
531	| 2 | Save my line | `POST .../records/{rid}/entry {summary, excerpt}` | `item`, `review`, `warnings` |
532	| 2 | date answers | `POST .../records/{rid}/confirm_date {date}` | `entry`, `gap_changes[].sentence`, `dates_to_confirm` |
533	| 2 | Yes, tell the attorney / No, not needed | `{action:"accept"}` / `{action:"dismiss"}` on the flag | — |
534	| 2 | Save note | `{action:"edit", edits:{note}}` | — |
535	| 3 | Yes, count it (charge) | `{action:"accept"}` (+ `confirm: flag.confirm_with` when `confirm_required`) | `totals.accepted`, `totals.letter_line` |
536	| 3 | Yes, count it (countable) | `{action:"count", confirm:"separate_charge"}` (+ `confirm_flag`) | `amount`, `totals` |
537	| 3 | No, don't count it | charge: `{action:"dismiss"}`; countable: `{action:"accept"}` | `totals` |
538	| 3 | Yes, list it / No, leave it out (never counted) | `{action:"accept"}` / `{action:"dismiss"}` | — |
539	| 4 | preview, Copy, Download | `GET /api/cases/{token}/export` | `letter_text`, `internal_notes_text`, `excluded.pending` |
540	| 4 | blocked rows | `GET .../export` 422 `detail.blockers[]` (same as `GET .../trace` `export_gate.blockers`) | `why`, `next_action`, `item_id` |
541	| 4 | Run the second check again | `POST /api/cases/{token}/rejudge` | `export_gate` |
542	| 4 | Exhibit and page numbers Save | `PUT /api/cases/{token}/export_config` | — |
543	
544	Not used by the guided UI (still in `/classic`): batch review, reclassify, dismissal suggestions, narrative (D-067), audit, judges,
545	billing listing, case trace panels, calibration.
546	
547	## 12. States checklist (every screen)
548	
549	| Screen | Loading | Empty | Error | Done |
550	|---|---|---|---|---|
551	| Your cases | 3 skeleton cards | 3.4 Empty | 3.4 Error + Try again | Finished section, green "Letter ready" |
552	| Step 1 | button shows "Reading..." in place, disabled | 4.1 | 4.1 table, 4.5 | 4.4 big check |
553	| Step 2 | skeleton text in both cards, same size; buttons disabled | "There are no timeline lines in this case." + Go to step 3 | load error in the work area: "We couldn't load this case." + Try again; write errors in the footer slot | 5.8 |
554	| Step 3 | as Step 2 | 6.4 no amounts | as Step 2 | 6.4 |
555	| Step 4 | "Making your letter..." in the letter box | `NOTHING_ACCEPTED` (7.3) | 7.3, network: "We couldn't make the letter. Try again" | 7.1 green row |
556	
557	## 13. Test plan for the build card
558	The mockup already passes the first two checks (Playwright, `file://`): every checkbox, tile, tappable sentence and the theme button
559	was clicked on all 28 pages at 1440x900, 390x844 and 320x640 with 0 boxes moved, 0 horizontal overflow, 0 `<details>`/menus and 0 JS
560	errors; and the step bar, both answers, the small buttons, the question and both cards sit at identical boxes on all 12 review pages
561	(Step 2 and 3 items) at 1440 and 390, so moving from one item to the next moves nothing.
562	
563	- Layout stability: for each review page, record the bounding boxes of the step bar, both answer buttons and the small buttons; click
564	  every answer, Fix the wording, Cancel, Back, tick and untick each box; assert no box moved (0 px) at 1440x900 and 390x844.
565	- No `<details>`, no `[role=menu]`, no element with `:hover`-only visibility; no horizontal scroll at 390 and 320.
566	- Flow: sample case from `/new` to a copied letter with only clicks; the letter equals `evals/golden/sample.export.expected.txt`.
567	- D-066: a disputed item cannot be accepted without the box (button disabled; a forced POST is 422 `COMPARE_REQUIRED`).
568	- D-059/D-064: count buttons stay disabled until the named box is ticked; bodies carry the named confirm.
569	- Provenance: with `answers: prepared` every sample item is tagged "Prepared answer"; the label and footer sentence are on every page.
570	- Multi-case: three cases at different steps show the right Next line and Continue target (local mode list and public mode stored tokens).
571	- axe: 0 serious/critical at both widths in light and dark.
572	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:57.653Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-180-ux-designer.md"
}
````

### User / tool · 2026-11-02T21:26:57.660Z

**tool result**
````
1	# T-180 review: guided UI spec + clickable mockup (ux-designer-reviewer)
2	
3	Verdict: **changes** (0 blockers, 4 majors, 8 minors/nits). Scores: design quality 4, originality 4, craft 3, functionality 3 (static mockup; no score at or below 2).
4	
5	I opened `artifacts/mockups/guided/*.html` over `file://` in Playwright at 1440x900, 1366x768, 390x844 and 320x640 and walked it as a first-time, non-technical user BEFORE opening the spec: Your cases -> Start a new case -> Add records (sample) -> We found 9 records -> Drafting (waited out the animation) -> 19 items of Step 2 (entry, fix, flag, gap, disputed, could-not-check, write-it-myself, date pick, done) -> Step 3 (charge, count-with-check, never-counted, done) -> Step 4 (ready, pending, blocked) -> clicked Download letter and read the saved file. Then I read `docs/GUIDED_UI_SPEC.md` in full and grepped `memory/contracts/api.md` and `app/backend/*.py` for every endpoint, field and error code the spec's section 11 uses.
6	
7	## First-time-user walk (per screen: where am I / what do I do / am I done)
8	
9	| Screen | Where | What to do | Done? | Hesitation, unknown words, movement |
10	|---|---|---|---|---|
11	| Your cases (index) | Yes, big h1, 4-bar track per card | Yes, one blue Continue per card, "Next:" line | Yes, Finished section, "Open letter" | Six cards at 1440 is calm. "Rename"/"Delete" read fine; Delete confirm swaps in place (nothing moved). "Demo: sample answers prepared by our team" shows 3 times (pill, footer, phone banner): noise. |
12	| Add records | Yes, step bar + "Step 1 of 4" | Partly: three tiles, but the button "Read the records" is at y 975-1031, below the 900 px fold | Not applicable | Clicked "Paste text": nothing changed, no textarea. "This demo can only read the sample..." sits under the button, after I could already pick Paste. |
13	| We found 9 records | Yes | Partly: "Draft the timeline" top at y 897, bottom 953 (cut by the fold) | Yes (green line) | "Start over with other records" is a second full button of equal weight. |
14	| Drafting | Yes | Yes (wait; "you can leave this page") | Yes ("All set", big button, focus moves) | "Loading the prepared line for each record" and "checked by code" mean nothing to a layperson. "19 timeline items" vs "9 records": unexplained jump. |
15	| Entry (Item 4 of 19) | Yes | Yes, one question, two big answers; highlight beside the line | Yes ("3 answered, 16 to go", bar) | "How it was checked ... second check agreed": what is the second check? Three numbers on screen: "Item 4", "Record 3", "Saved: item 3". |
16	| Fix the wording | Yes | Yes | Yes | Red "Not saved ... Remove it or change the quote": I can change the quote? (only by tapping sentences, which the left card explains). "Fix the wording" greys out while editing with no reason. |
17	| Warning / gap | Yes | Yes ("Should the attorney be told about this?") | Yes | "Gap of 73 days. Gap of 73 days between..." repeats itself. |
18	| Disputed | Yes | Yes, yellow box + ticking "I read this line myself" unlocks Yes | Yes | Good friction. "second check found this only partly supported" again undefined. |
19	| Could not check | Yes (amber tag) | Yes, "Write it myself" / "Skip it" | Yes ("Optional item") | "The model's quote does not appear word for word": "model" and "Its quote" (the spec renames quote to "the highlighted words"). |
20	| Pick the date | Yes | Yes, two dates plus "Suggested" | Yes | "month first / day first" is clear. "Decide later" leaves the case (goes to Your cases). |
21	| Step 2 done | Mostly: the step bar underlines both step 2 and step 3 | Yes | Yes, big check and counts add to 19 | Moved? No. "9 warnings for the attorney . 1 not needed" is clear. |
22	| Charge / count / never counted | Yes ("Bill total so far") | Yes | Yes | "itemized service line", "separate charge for a service" are billing words. "Yes, list it" is vague (list where?). Demo sentence is cut to "you decide ever..." by the total chip. |
23	| Step 3 done | Yes | Yes (total line is large) | Yes | Row "Amount: missing 3 days of work" in Never counted is not an amount. |
24	| Get your letter | Yes (all four green) | NO on arrival: Copy letter / Download are at y 1016, a 700 px scroll below a long letter | Yes (green row) | Downloaded file is clean plain text, 9 lines + 2 charges, total line, citations. "[Ex. __ / Bates __]" blanks have no cue until you scroll further. |
25	| Pending / blocked | Yes | Yes (amber row, "Go to the first one", ticking "Copy it anyway" enables Copy) | Yes | Good: shows exactly what would be sent. |
26	
27	Nothing moved on click anywhere I tried (every answer is a page link, so this is a weak test of the real thing; the worker's own check_stability.py covers the same ground).
28	
29	## Spec vs mockup vs API
30	
31	- Control-to-API: all of section 11 maps to endpoints in `memory/contracts/api.md` EXCEPT three details documented only in code: `compared: true` and `422 COMPARE_REQUIRED` (`grep -c COMPARE_REQUIRED api.md` = 0; `app/backend/review.py:308` has it) and `POST /api/cases/pdf?title=` (api.md:83 says query `name`; `app/backend/api.py:303` accepts `title`). The spec discloses the first; the handoff says backend will add it.
32	- Spec contradicts itself: phone line card is "fixed 180 px" (2.7) and "fixed 256 px" (8).
33	- Spec says the paste/upload box, the Rename edit state, "Add a note", the home public-mode list and every Step 1 error line exist; the mockup has none of them (clicks do nothing).
34	
35	```json
36	{"card": "T-180", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
37	 "scope": "docs/GUIDED_UI_SPEC.md; artifacts/mockups/guided/index.html + screens.html + 28 step/home pages; memory/contracts/api.md section mapping; static file:// mockup, no app server; sample case + two library cases as mocked",
38	 "exercised": [
39	  "Opened artifacts/mockups/guided/index.html in Playwright (chromium) at 1440x900, 1366x768, 390x844, 320x640 and walked Your cases -> Start a new case -> step1-add -> step1-found -> step1-drafting (waited 9.5 s for the animation) -> step2-entry/fix/flag/gap/disputed/cannot-check/write/date/date-confirmed/done -> step3-charge/count/never/done -> step4-letter/pending/blocked, before reading the spec",
40	  "Dumped visible text, every control, its href and its y position per page (artifacts/review-evidence/T-180-ux-pages.py); 50+ screenshots T-180-ux-*.png in artifacts/review-evidence/",
41	  "Clicked Download letter (.txt) on step4-letter, saved jordan-rivera-letter.txt to artifacts/review-evidence/T-180-dl/letter.txt and read it: one line per entry, citations, total line, no UI labels",
42	  "Clicked Paste text, Rename, Delete/Keep, Find a case on index/step1-add: Paste and Rename do nothing; Delete confirm and search work",
43	  "Measured Tab presses to the primary action (index 6, add 6, entry 8, step3-done 7, letter 8) and scrolling inner cards (T-180-ux-scrollcards.py): at 390 the source card is 122 px for 323/520/331 px of content",
44	  "Measured primary-button position at 1440x900 and 1366x768 (T-180-ux-fold.py): Read the records y975, Draft the timeline y897-953, Copy letter y1016",
45	  "Dark-mode screenshots of step2-entry and step4-pending",
46	  "Read docs/GUIDED_UI_SPEC.md lines 1-572 in full; grepped memory/contracts/api.md, app/backend/review.py and app/backend/api.py for every section 11 endpoint, field and error code"
47	 ],
48	 "verdict": "changes",
49	 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 3},
50	 "findings": [
51	  {"severity": "major",
52	   "title": "The one action on three key screens is below the fold: Read the records, Draft the timeline, Copy/Download letter",
53	   "evidence": "artifacts/review-evidence/T-180-ux-fold.py at 1440x900 and 1366x768: step1-add 'Read the records' top 975 bottom 1031; step1-found 'Draft the timeline' top 897 bottom 953 (screenshot artifacts/review-evidence/T-180-ux-step1-found-1440.png shows only its top edge); step4-letter 'Copy letter' top 1016 (page scrolls to 1406; T-180-ux-step4-letter-1440.png shows the letter, no button). Review pages have a fixed action bar, these do not. Spec section 0 promises 'what do I do now' is next to the buttons.",
54	   "why_it_matters": "A first-time user on the 'Get your letter' screen sees a long wall of text and a green 'ready' row but not the Copy or Download button, which is the whole point of the product. Same for starting the read and starting the draft. 'Know what to do' fails until she scrolls, and the page-level scroll plus the letter box's own scroll is a nested-scroll trap.",
55	   "fix": "Give Step 1 and Step 4 the same fixed action bar as the review pages (primary button always on screen), or move Copy letter / Download letter above the preview. Keep the 'Draft the timeline' list height so the button fits at 1366x768.",
56	   "acceptance_test": "Playwright at 1440x900 and 1366x768: on step1-add, step1-found and step4-letter the primary button's bounding box bottom is <= viewport height with no scrolling."},
57	  {"severity": "major",
58	   "title": "At 390 px the record is squeezed to 122 px, so the words she is asked to compare are mostly hidden, and Undo is cut off",
59	   "evidence": "T-180-ux-scrollcards.py: at 390x844 the source card body is 122 px tall holding 323 px (entry), 520 px (gap, two records) and 331 px (count) of content, no scroll cue; the prepared-answer card also scrolls (93/115 px, 72/126 px). Screenshots T-180-ux-step2-entry-390.png (highlight cut after 'Refer to physical therapy', 'How it was checked' cut mid-sentence), T-180-ux-step2-gap-390.png (shows record 6 only; record 7 and the 73-day dates are off-screen), T-180-ux-step3-count-390.png (reason 'The line states no date of service, so it is not an itemized...' is cut; 'Saved: ... counted...' ellipsized). Status slot at 390: 'kept in the letter. U...' (step2-gap-390.png). Spec 2.7 says line card 180 px, section 8 says 256 px, mockup shows less than either leaves for the record.",
60	   "why_it_matters": "The product's promise is that she checks the line against the words in the record. On a phone the Yes button is fully visible and the evidence 23-38 percent visible. Undo is the safety net for a wrong tap and its label is clipped.",
61	   "fix": "Rebalance the phone layout: shorter action bar (small buttons in one row, status slot on its own line that wraps), give the source card the larger share and cap the line card to its text, add a visible 'Scroll for more' fade or 'Show all of this record' control, and let the status line wrap so Undo is always whole. Reconcile 2.7 and 8.",
62	   "acceptance_test": "At 390x844 on step2-entry, step2-gap, step3-count: source card clientHeight >= 220 px or scrollHeight - clientHeight <= 24 px; the Undo link's rect is fully inside the viewport and its text is not ellipsized; the reason sentence in the line card is not clipped."},
63	  {"severity": "major",
64	   "title": "The first real screen (paste/upload) and its errors are not in the mockup, and the demo offers paste and upload that it then refuses",
65	   "evidence": "T-180-ux-interact.py: clicking 'Paste text' on step1-add.html leaves 0 textareas visible and the panel unchanged (T-180-ux-step1-paste-click-1440.png); Upload does nothing either; no page shows the 400/413/409/429/pdf error lines, the 'Reading...' state, the Rename input (0 inputs after clicking Rename on index.html) or 'Add a note'. Spec 4.1 describes a 280 px box 'that does not change size between choices' and a reserved error line; spec 3.1 describes Rename in place. On the same screen the line 'This demo can only read the sample and our test cases.' sits BELOW the Read button.",
66	   "why_it_matters": "Paste is how every real user starts and its error states (empty, oversized, busy, offline with 'Your text is still here') are exactly where trust is lost. The layout-stability claim in spec section 13 is untested for the largest input box. In demo mode a grandma will pick Paste, type, press Read and get a 409: error prevention failure.",
67	   "fix": "Add mockup pages for paste (empty, filled, empty-submit error, too large, offline with text kept), upload, scanned PDF, Rename editing and Add a note. In demo mode show the demo sentence above the tiles and mark Paste/Upload as 'not available in this demo' (disabled with the reason) instead of failing after the click.",
68	   "acceptance_test": "check_stability.py covers the new pages with 0 moved boxes at 1440/390/320; Playwright: in demo mode the Paste and Upload tiles are aria-disabled and the reason is visible without hover; every Step 1 error row in spec 4.1 has a mockup page."},
69	  {"severity": "major",
70	   "title": "Words a grandma cannot decide with remain on decision screens: 'second check', 'the model's quote', 'checked by code', 'itemized service line'",
71	   "evidence": "step2-entry 'How it was checked: Quote found word for word, every number in the summary is in the quote, and the second check agreed.'; step2-disputed 'The second check found this only partly supported by the quote.'; step2-cannot-check 'The model's quote does not appear word for word in the record' / 'Its quote:'; header line on steps 2-3 'prepared by our team and checked by code'; step3-count 'it is not an itemized service line and is not totaled'; drafting list 'Loading the prepared line for each record'. Spec section 10 renames 'excerpt/quote' to 'the highlighted words' and 'judge' to 'the second check' but nothing on screen says what the second check is; spec 0 says server sentences are 'shown as given', which is how 'model' and 'quote' get through.",
72	   "why_it_matters": "Brief: 'someone's <Chris's message omitted>'. The disputed screen asks her to overrule the second check, so she must know what it is. 'Quote' and 'highlighted words' name the same thing on neighbouring screens.",
73	   "fix": "Add one plain sentence where the second check first appears ('A second AI pass re-read each line against the record') and use one word for the evidence everywhere (highlighted words). Because server `why` text is shown as given, either ask backend for plain-language variants or have the UI map reason codes to its own sentences, and say so in the spec. Replace 'checked by code' with 'checked by the computer, not by a person'. Reword 'itemized service line' to 'a single dated bill line'.",
74	   "acceptance_test": "A text lint over every mockup page and every spec section 11 server sentence finds no occurrence of 'model', 'its quote', 'checked by code', 'itemized'; the Step 2 entry page contains a one-sentence definition of 'second check'; a 3-person read-aloud test of step2-disputed and step3-count with no questions asked."},
75	  {"severity": "minor",
76	   "title": "Step bar shows two current steps on the Step 2 done screen",
77	   "evidence": "T-180-ux-step2-done-1440.png: step 2 (blue check, underline) and step 3 ('3', '4 of 4 left', underline) both marked current while the page says 'Step 2 of 4'. Spec 9.2: current step is the first step not done.",
78	   "why_it_matters": "Where am I? The bar moves its highlight from step 2 to step 3 before she has pressed 'Go to step 3'.",
79	   "fix": "On a step's done screen keep that step current; show the next step as remaining.",
80	   "acceptance_test": "On step2-done exactly one segment has aria-current=step and the accent underline, and it is step 2."},
81	  {"severity": "minor",
82	   "title": "Locked steps all read 'After step 1', including step 4",
83	   "evidence": "T-180-ux-step1-add-1440.png / T-180-ux-01-add-1440.png step bar: '2 After step 1', '3 After step 1', '4 After step 1'. Spec 2.4 table.",
84	   "why_it_matters": "Reads as if step 4 happens right after step 1; hides the order the brief asks for (clear defined steps).",
85	   "fix": "Use 'After step 1', 'After step 2', 'After step 3', or 'Not yet' for all three.",
86	   "acceptance_test": "Step bar text on step1-add lists three distinct status lines."},
87	  {"severity": "minor",
88	   "title": "Spec depends on API details that api.md does not document, and contradicts itself on phone card height",
89	   "evidence": "grep -c COMPARE_REQUIRED memory/contracts/api.md -> 0 (code: app/backend/review.py:308 compare_error); memory/contracts/api.md:83 documents 'optional query name' for POST /api/cases/pdf but app/backend/api.py:303 accepts title; docs/GUIDED_UI_SPEC.md 2.7 'fixed 180 px' vs section 8 'fixed 256 px'.",
90	   "why_it_matters": "The build card will implement 'every control maps to a real API' from api.md. Undocumented fields are where a frontend/back-end mismatch hides (this is the D-066 accept path).",
91	   "fix": "Backend adds `compared`, `422 COMPARE_REQUIRED` and PDF `title` to api.md (spec already flags the first); spec picks one phone card height.",
92	   "acceptance_test": "grep finds COMPARE_REQUIRED, compared and the pdf title query in memory/contracts/api.md; the spec has one phone card height."},
93	  {"severity": "minor",
94	   "title": "Never-counted list can show a non-amount as the Amount",
95	   "evidence": "step3-done page: 'Never counted (2)' row 'missing 3 days of work | Capital PT, visit 8 | This figure is not a bill (for example a damages or settlement figure)'. Spec 6.3 shows the figure 'as written (text)'.",
96	   "why_it_matters": "A first-time user cannot tell what this row is or why it is in the Bills step; it looks like a bug.",
97	   "fix": "When `text` has no currency symbol, label it 'Number found in the record: 3 days' or drop it from Step 3 and tell the backend it is not an amount.",
98	   "acceptance_test": "No Step 3 row's Amount cell lacks a digit-with-currency pattern unless it carries a plain 'not a money amount' label."},
99	  {"severity": "minor",
100	   "title": "Letter can be copied with unfilled [Ex. __ / Bates __] and no warning; the number fields sit below the buttons",
101	   "evidence": "T-180-ux-step4-letter-scroll700-1440.png: Copy/Download above, 'Exhibit and page numbers (optional)' below; T-180-dl/letter.txt has 11 'Source [Ex. __ / Bates __]' placeholders.",
102	   "why_it_matters": "She pastes into a demand letter with blanks she did not know to fill. Optional, but unflagged.",
103	   "fix": "Move the box above the buttons or add one line under Copy: 'The [Ex. __ / Bates __] blanks are for you to fill in.'",
104	   "acceptance_test": "Step 4 shows a visible sentence about the blanks next to Copy letter."},
105	  {"severity": "minor",
106	   "title": "Three numbering schemes and two labels for the same thing on one review screen",
107	   "evidence": "step2-entry: 'Item 4 of 19', 'Record 3', 'Saved: item 3 (Central ER discharge summary)'; step2-entry tag 'Prepared answer' vs step2-date-confirmed 'AI draft'; step bar circle '2' plus label '2 Check the timeline' (visible duplication in T-180-ux-step2-entry-1440.png); spec 7.1 'Download notes (.txt)' vs mockup 'Download notes'.",
108	   "why_it_matters": "Small contradictions add reading effort for the person the brief is about; tag names are explained nowhere.",
109	   "fix": "Say 'Line 4 of 19' and 'Record 3' consistently or drop the record number from the card header; explain the tags in one footer sentence; drop the number from the label or the circle.",
110	   "acceptance_test": "One counting word per screen; both tags have an on-screen explanation."},
111	  {"severity": "minor",
112	   "title": "Step 3 title row truncates the demo sentence and the title row sits 16 px under the step bar",
113	   "evidence": "T-180-ux-step3-count-1440.png: 'In this demo the sample summaries and flags were prepared by our team and checked by code; you decide ever...' cut by the 'Bill total so far' chip; 'Step 2 of 4 / Check the timeline' starts at y187 under a bar ending at y171 (T-180-ux-step2-entry-1440.png).",
114	   "why_it_matters": "Truncated provenance text and a cramped title weaken the 'look nice' goal and the D-065 provenance statement.",
115	   "fix": "Let the demo sentence wrap on its own row or move it to the footer slot; add 16-24 px above the eyebrow.",
116	   "acceptance_test": "No ellipsis in the title row at 1440 and 390; title row top margin >= 16 px."},
117	  {"severity": "nit",
118	   "title": "Preference, not a spec violation: 'No, leave it out' is the only 'No' to 'Does this line say the same thing?', and 'Fix the wording' is a small text link",
119	   "evidence": "step2-entry-1440.png action bar: Yes (filled), 'No, leave it out' (outlined), 'Fix the wording' same weight as 'Back'.",
120	   "why_it_matters": "A user who honestly answers 'No, it does not match' deletes the line instead of repairing it. I would have done it differently; the spec's equal-size answers are a deliberate choice.",
121	   "fix": "Consider 'No, it doesn't match' leading to Fix the wording / Leave it out as a second step.",
122	   "acceptance_test": "n/a (design preference)"}
123	 ],
124	 "whats_right": [
125	  "Fixed frame with the highlighted record beside the line, one question, two equal answers, 'N answered . N to go' and a green done screen: it answers where/what/done on every review page at 1440.",
126	  "Friction is placed correctly: ticking 'I read this line myself' unlocks Yes on a disputed line; 'Copy it anyway' gates a letter with undecided items, and the preview shows exactly what would be sent.",
127	  "The downloaded letter is clean pasteable text with citations and the exact total line, and the notes box is plainly marked 'Do not send'."
128	 ],
129	 "questions_for_chris": [
130	  "Is 1366x768 a target screen for the 'grandma' user? Finding 1 gets worse there (nothing below the step bar fits).",
131	  "In the public demo, should Paste and Upload be shown disabled up front (my recommendation) or hidden entirely?"
132	 ]}
133	```
134	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:07.968Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && wc -l *; cat step1.js step4.js home.js step1.css step4.css home.css; sed -n 1,80p app.js"
}
````

### User / tool · 2026-11-02T21:27:08.060Z

**tool result**
````
     166 app.js
     138 core.js
       1 home.css
      14 home.js
      35 index.html
       1 review.css
       5 review.js
       1 step1.css
      10 step1.js
       1 step2.css
      12 step2.js
       1 step3.css
      11 step3.js
       1 step4.css
       9 step4.js
     454 styles.css
     860 total
/* Step 1: Add records. /new (before the case exists) and /case/<token>/records (found, drafting, done, stopped). PLACEHOLDER from the T-181 scaffold.
   OWNER: the Home + Step 1 + Step 4 builder; replace the bodies, keep both registrations. Spec section 4. Uses G.api.createCase / run / status, ctx.setStepStatus(1, "Drafting 4 of 8"), ctx.refresh(). */
(function () {
  const G = window.G, { h } = G;
  const page = (title, ...more) => h("main", { class: "wrap", id: "main" }, h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("h1", { "data-testid": "page-title" }, title))), h("p", { class: "muted", "data-testid": "placeholder" }, "This step is not built yet."), ...more);
  G.pages.new = async function (ctx) { ctx.view.append(page("Add your records")); };
  G.pages.records = async function (ctx) {
    ctx.view.append(page("Add records", h("div", { class: "row-actions" }, h("a", { class: "btn primary", href: G.url.timeline(ctx.token), "data-testid": "btn-next" }, "Go to step 2"))));
  };
})();
/* Step 4: Get your letter (/case/<token>/letter). PLACEHOLDER from the T-181 scaffold. OWNER: the Home + Step 1 + Step 4 builder. Spec section 7.
   Uses G.api.exportCase (422 detail.blockers when not ready), G.api.rejudge, ctx.setStepStatus(4, "1 problem"). */
(function () {
  const G = window.G, { h } = G;
  G.pages.letter = async function (ctx) {
    ctx.view.append(h("main", { class: "wrap", id: "main" }, h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("h1", { "data-testid": "page-title" }, "Get your letter"))),
      h("p", { class: "muted", "data-testid": "placeholder" }, "This step is not built yet."), h("div", { class: "row-actions" }, h("a", { class: "btn", href: G.url.bills(ctx.token), "data-testid": "btn-back" }, "‹ Back"))));
  };
})();
/* Your cases (/). PLACEHOLDER from the T-181 scaffold. OWNER: the Home + Step 1 + Step 4 builder; replace the body, keep the registration. Spec section 3.
   Uses: G.api.cases() (local mode; 404 in public mode, spec 3.3), G.steps.states(row) for each card's mini step track (it understands a /api/cases row), G.url.* for Continue targets. */
(function () {
  const G = window.G, { h } = G;
  G.pages.home = async function (ctx) {
    const main = h("main", { class: "wrap wide", id: "main" }, h("div", { class: "home-h" }, h("div", {}, h("h1", { "data-testid": "page-title" }, "Your cases"))), h("p", { class: "muted", "data-testid": "placeholder" }, "Loading…"));
    ctx.view.append(main);
    let rows = [];
    try { rows = (await G.api.cases(ctx.signal)).cases || []; }
    catch (e) { if (e.name === "AbortError") return; if (e.status !== 404) { ctx.view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, () => ctx.go("/", { replace: true }), "We couldn't load your cases"))); return; } }
    main.lastChild.replaceWith(rows.length ? h("ul", { class: "plain", "data-testid": "cases-list" }, rows.map((c) => h("li", {}, h("a", { href: G.url.records(c.token) }, c.title || c.name || "Case"))))
      : h("p", { class: "muted", "data-testid": "cases-empty" }, "No cases yet."));
  };
})();
/* step1: rules for this module only (T-181 scaffold). Shell tokens and base classes live in styles.css. */
/* step4: rules for this module only (T-181 scaffold). Shell tokens and base classes live in styles.css. */
/* home: rules for this module only (T-181 scaffold). Shell tokens and base classes live in styles.css. */
/* Guided UI shell (T-181, D-068; spec 2 "Global frame"). Owns: banner, header, demo label (D-065), step bar, footer, theme, router, case loading.
   Page modules (home.js, step1-4.js, review.js) plug in through G.pages and never touch the chrome except through ctx.

   ROUTES (real paths, history.pushState; the server returns index.html for them):
     /                         G.pages.home      layout page
     /new                      G.pages.new       layout page   (step 1, no case yet; step bar shows 1 current, 2-4 locked)
     /case/<token>/records     G.pages.records   layout page   (step 1)
     /case/<token>/timeline    G.pages.timeline  layout frame  (step 2; ?item=<id>; the done screen calls ctx.layout("page"))
     /case/<token>/bills       G.pages.bills     layout frame  (step 3; ?item=<id>; the done screen calls ctx.layout("page"))
     /case/<token>/letter      G.pages.letter    layout page   (step 4)
   PAGE CONTRACT: G.pages.<name> = async (ctx) => optional cleanup function. Render into ctx.view (cleared; its children become children of <body> because .view is display:contents,
   so a frame page appends .titlebar, .work and .actions, a page-layout page appends one <main class="wrap">). Resolve when the first paint is done; the shell then sets data-ready on #view.
   ctx = { route, token, step, query (URLSearchParams), case (GET case JSON, null on home and /new), health, signal (aborts on navigation: pass it to fetch),
           view, layout("frame"|"page"), go(path, {replace}), refresh() -> re-GET case, redraw step bar and header, returns the JSON,
           setStepStatus(n, text, state?) override one step-bar status line (e.g. "Drafting 4 of 8", "1 problem"), setCaseTitle(text), setTitle(text) document title }.
   Anything the page throws becomes the plain error block with Try again. Links: any <a href="/..."> is routed without a reload (modifier-clicks and target=_blank are left alone). */
(function () {
  const G = window.G, { h, $ } = G;
  const root = document.documentElement, body = document.body, view = $("#view"), bar = $("#step-bar"), list = $("#step-list"), headerEl = $("#header");
  const TITLE = "Treatment Timeline";
  const ROUTES = [
    [/^\/$/, "home", 0], [/^\/new$/, "new", 1],
    [/^\/case\/([^/]+)\/records$/, "records", 1], [/^\/case\/([^/]+)\/timeline$/, "timeline", 2], [/^\/case\/([^/]+)\/bills$/, "bills", 3], [/^\/case\/([^/]+)\/letter$/, "letter", 4],
  ];
  const FRAME = { timeline: true, bills: true };

  /* ---- theme (spec 2.2): follows the OS until she picks; remembered in localStorage inside try/catch ---- */
  const isDark = () => { const t = root.getAttribute("data-theme"); return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; };
  try { const t = localStorage.getItem("zl.guided.theme"); if (t === "light" || t === "dark") root.setAttribute("data-theme", t); } catch (_) { /* follows the OS */ }
  function themeLabel() { const b = $("[data-theme-btn]"); if (b) { b.textContent = isDark() ? "Light mode" : "Dark mode"; b.setAttribute("aria-label", b.textContent); } }
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", themeLabel);
  function themeButton() {
    return h("button", { type: "button", class: "theme-btn", "data-theme-btn": "", "data-testid": "btn-theme", onclick: () => {
      const next = isDark() ? "light" : "dark"; root.setAttribute("data-theme", next);
      try { localStorage.setItem("zl.guided.theme", next); } catch (_) { /* not remembered */ }
      themeLabel();
    } }, "Dark mode");
  }

  /* ---- banner, demo label and footer (spec 2.1, 2.3, 2.8; D-065): wording by health.answers, never softened ---- */
  // D-065 as amended in T-177 r2: the prepared-answers sentence is the amended one (the spec 2.3 sentence about the evaluation report is superseded)
  const DEMO = { prepared: ["Demo: sample answers prepared by our team", "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."],
    recorded: ["Demo: recorded AI answers", "These are real AI answers recorded earlier; nothing new is sent to an AI."] };
  G.provenance = function () {
    const hl = G.store.health, kind = hl && hl.demo_mode ? (hl.answers === "prepared" ? "prepared" : "recorded") : "live";
    return { kind, label: DEMO[kind] ? DEMO[kind][0] : "", note: DEMO[kind] ? DEMO[kind][1] : "Summaries and warnings are drafted by AI and checked by code; you decide every item.",
      hours: hl && !hl.demo_mode ? hl.retention_hours : null };
  };
  function drawBanner() {
    const hl = G.store.health, p = G.provenance();
    $("#banner-text").textContent = (hl && hl.banner) || "Synthetic data only — never paste real records";
    $("#banner-demo").textContent = p.label;
    const f = $("#footer"); f.replaceChildren(h("span", { "data-testid": "footer-note" }, p.label ? p.label + ". " + p.note : p.note),
      p.hours ? h("span", { class: "f-live" }, `Pasted text is deleted after ${p.hours} hours.`) : null);
  }
  let headerState = { title: null, sub: null };
  function drawHeader() {
    const p = G.provenance(), t = headerState.title;
    const left = t == null
      ? h("a", { class: "brand", href: "/", "data-testid": "brand" }, h("span", { class: "brand-mark", "aria-hidden": "true" }, "TT"), h("span", {}, "Treatment Timeline"))
      : [h("a", { class: "back-cases", href: "/", "data-testid": "btn-your-cases" }, h("span", { "aria-hidden": "true" }, "‹"), h("span", { class: "long" }, "Your cases"), h("span", { class: "short" }, "Cases")),
         h("div", { class: "hd-case" }, h("span", { class: "case-title", "data-testid": "case-title", title: t }, t), headerState.sub ? h("span", { class: "case-sub" }, headerState.sub) : null)];
    headerEl.replaceChildren(...[].concat(left), h("span", { class: "spacer" }), ...(p.label ? [h("span", { class: "demo-pill", "data-testid": "demo-badge", title: p.note }, p.label)] : []), themeButton());
    themeLabel();
  }
  G.api.health().then((hl) => { G.store.health = hl; drawBanner(); drawHeader(); G.emit("health", hl); }).catch(() => { /* the static banner stays; pages that need health read G.store.health and cope with null */ });

  /* ---- step bar (spec 2.4): same four steps in the same place; only classes, statuses and links change ---- */
  const overrides = {};      // token -> { n: [text, state?] }
  function drawBar(route, token, c, step) {
    const show = route === "new" || (token && step);
    bar.hidden = !show; if (!show) return;
    const ov = (token && overrides[token]) || {};
    const st = route === "new" ? [{ state: "todo", status: "Now" }, ...[2, 3, 4].map(() => ({ state: "locked", status: "After step 1" }))] : c ? G.steps.states(c, step) : [1, 2, 3, 4].map(() => ({ state: "locked", status: "" }));
    list.replaceChildren(...st.map((s, i) => {
      const n = i + 1, o = ov[n]; if (o) { s = { ...s, status: o[0], state: o[1] || s.state }; }
      const cur = n === step, locked = s.state === "locked", mark = s.state === "done" ? "✓" : s.state === "attn" && !cur ? "!" : String(n);
      const inner = [h("span", { class: "dot", "aria-hidden": "true" }, mark), h("span", { class: "st-text" },
        h("span", { class: "st-label" }, h("span", { class: "long" }, `${n} ${G.LABELS[i][0]}`), h("span", { class: "short" }, G.LABELS[i][1])), h("span", { class: "st-status" }, s.status)),
        h("span", { class: "sr" }, ` (step ${n} of 4)`)];
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:09.537Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && sed -n 80,166p app.js; cat core.js index.html; cat review.js step2.js"
}
````

### User / tool · 2026-11-02T21:27:09.681Z

**tool result**
````
        h("span", { class: "sr" }, ` (step ${n} of 4)`)];
      const a = { class: "step " + s.state + (cur ? " current" : ""), "data-testid": "step-" + n, "data-state": s.state };
      if (cur) a["aria-current"] = "step";
      return h("li", {}, locked || !token ? h("span", { ...a, "aria-disabled": locked ? "true" : null }, inner) : h("a", { ...a, href: G.url.step(token, n) }, inner));
    }));
  }

  /* ---- router ---- */
  let ctrl = null, cleanup = null, ticket = 0, first = true, now = null;
  function parse() {
    const path = location.pathname.replace(/\/+$/, "") || "/";
    for (const [re, name, step] of ROUTES) { const m = path.match(re); if (m) return { name, step, token: m[1] ? decodeURIComponent(m[1]) : null, query: new URLSearchParams(location.search) }; }
    if (/^\/case\/[^/]+$/.test(path)) return { name: "redirect", token: decodeURIComponent(path.split("/")[2]) };
    return { name: "missing", step: 0, query: new URLSearchParams() };
  }
  G.go = function (path, opts) { (opts && opts.replace ? history.replaceState : history.pushState).call(history, null, "", path); return render(); };
  G.route = () => now;
  function setLayout(mode) { body.classList.toggle("frame", mode === "frame"); body.classList.toggle("page", mode !== "frame"); }

  async function render() {
    const r = parse(), mine = ++ticket;
    if (r.name === "redirect") { history.replaceState(null, "", G.url.records(r.token)); return render(); }          // a bare case link opens step 1
    if (ctrl) ctrl.abort();
    if (typeof cleanup === "function") { try { cleanup(); } catch (_) { /* a page's cleanup must not stop navigation */ } }
    cleanup = null; ctrl = new AbortController(); now = r;
    const stale = () => ticket !== mine;
    view.replaceChildren(); view.removeAttribute("data-ready"); view.dataset.route = r.name;
    setLayout(FRAME[r.name] ? "frame" : "page"); document.title = TITLE; window.scrollTo(0, 0);
    headerState = { title: r.name === "new" ? "New case" : null, sub: null }; drawHeader(); drawBanner();
    let c = null;
    const ctx = {
      route: r.name, token: r.token, step: r.step, query: r.query, case: null, signal: ctrl.signal, view, get health() { return G.store.health; },
      layout: (m) => setLayout(m), go: G.go,
      setStepStatus: (n, text, state) => { (overrides[r.token] = overrides[r.token] || {})[n] = [text, state]; if (!stale()) drawBar(r.name, r.token, ctx.case, r.step); },
      setCaseTitle: (t) => { if (!stale()) { headerState.title = t; drawHeader(); } },
      setTitle: (t) => { if (!stale()) document.title = t + " – " + TITLE; },
      refresh: async () => { const j = await G.store.load(r.token, ctrl.signal); if (!stale()) { ctx.case = j; paintCase(j); } return j; },
    };
    function paintCase(j) { headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, r.token, j, r.step); }
    drawBar(r.name, r.token, G.store.cases[r.token] || null, r.step);
    try {
      if (r.token) {
        try { c = await G.store.load(r.token, ctrl.signal); }
        catch (e) {
          if (e && e.name === "AbortError") return; if (stale()) return;
          setLayout("page"); drawBar(r.name, r.token, null, r.step);
          view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, () => render(), e.status === 404 ? "This case is no longer here" : "We couldn't open this case")));
          return done();
        }
        if (stale()) return; ctx.case = c; paintCase(c);
      }
      const page = G.pages[r.name];
      if (!page) { setLayout("page"); view.append(h("main", { class: "wrap" }, h("div", { class: "errbox" }, h("h1", { "data-testid": "page-title" }, "We couldn't find that page"), h("p", {}, "The link may be old or mistyped."),
        h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: "/", "data-testid": "link-home" }, "Back to your cases"))))); return done(); }
      const out = await page(ctx);
      if (stale()) { if (typeof out === "function") out(); return; }
      cleanup = out;
    } catch (e) {
      if (e && e.name === "AbortError") return; if (stale()) return;
      setLayout("page"); view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, () => render(), "Something went wrong")));
    }
    done();
    function done() {
      if (stale()) return;
      view.setAttribute("data-ready", "1");
      const t = $("h1", view); if (t && document.title === TITLE) document.title = t.textContent + " – " + TITLE;
      if (!first) { const f = $("[data-autofocus]", view) || t; if (f) { if (!f.matches("a,button,input,textarea,select,[tabindex]")) f.tabIndex = -1; f.focus({ preventScroll: true }); } }
      first = false;
    }
  }
  /* The case title everywhere is the API title (spec 2.2); until it has one, the first record's source line is no use here, so a plain "Case". */
  G.titleOf = (c) => (c && (c.title || c.name)) || "Case";

  /* ---- links: same-origin absolute paths are routed without a reload ---- */
  document.addEventListener("click", (e) => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest && e.target.closest("a[href]"); if (!a || a.target || a.hasAttribute("download")) return;
    const u = new URL(a.href, location.href);
    if (u.origin !== location.origin || /^\/(api|classic)(\/|$)/.test(u.pathname) || !ROUTES.concat([[/^\/case\//]]).some(([re]) => re.test(u.pathname.replace(/\/+$/, "") || "/"))) return;
    e.preventDefault(); G.go(u.pathname + u.search);
  });
  window.addEventListener("popstate", render);
  window.addEventListener("pageshow", (e) => { if (e.persisted) render(); });
  G.on("case", (token, j) => { const r = now; if (r && r.token === token && r.name !== "redirect") { headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, token, j, r.step); } });
  drawBanner(); drawHeader();
  render();
})();
/* Guided UI core (T-181, D-068). Namespace G: safe DOM builder, URLs, the API wrapper, the case store and the step-state rules (spec 9.1-9.2).
   No innerHTML anywhere: record text, quotes and titles go in with textContent (spec section 0, "Untrusted text"; CSP stays script-src 'self').
   CSP also blocks inline style ATTRIBUTES: set sizes from code with el.style.width = ... (CSSOM is allowed) and never write style="..." in markup. */
(function () {
  const G = (window.G = window.G || {});
  G.pages = {};           // G.pages.home | new | records | timeline | bills | letter = async (ctx) => optional cleanup fn   (see app.js, "page contract")
  G.LABELS = [["Add records", "Records"], ["Check the timeline", "Timeline"], ["Check the bills", "Bills"], ["Get your letter", "Letter"]];

  /* h("button", { class: "btn", onclick: fn, "data-testid": "x" }, "text", node, ...) -> element. on* attributes are listeners; text becomes text nodes. */
  G.h = function (tag, attrs, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v == null || v === false) continue;
      if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
      else if (k === "class") el.className = v;
      else if (k === "text") el.textContent = v;
      else el.setAttribute(k, v === true ? "" : String(v));
    }
    for (const kid of kids.flat(Infinity)) if (kid != null && kid !== false) el.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
    return el;
  };
  G.$ = (sel, root) => (root || document).querySelector(sel);
  G.$$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  const enc = encodeURIComponent;
  G.url = {
    home: () => "/", new: () => "/new",
    records: (t) => "/case/" + enc(t) + "/records",
    timeline: (t, item) => "/case/" + enc(t) + "/timeline" + (item ? "?item=" + enc(item) : ""),
    bills: (t, item) => "/case/" + enc(t) + "/bills" + (item ? "?item=" + enc(item) : ""),
    letter: (t) => "/case/" + enc(t) + "/letter",
    step: (t, n, item) => [null, G.url.records, G.url.timeline, G.url.bills, G.url.letter][n](t, item),
  };

  /* Tiny event bus: G.on("case", fn) fires when the store learns a case (token, json). */
  const subs = {};
  G.on = (ev, fn) => { (subs[ev] = subs[ev] || []).push(fn); return () => { subs[ev] = (subs[ev] || []).filter((f) => f !== fn); }; };
  G.emit = (ev, ...a) => (subs[ev] || []).slice().forEach((f) => { try { f(...a); } catch (e) { console.error(e); } });

  /* ---- API wrapper over the existing /api. Failures become G.ApiError with a message a first-time user can read: never an HTTP status, "Failed to fetch" or a stack. ---- */
  const FALLBACK = {
    0: "We couldn't reach the app. Check your connection and try again.",
    404: "We couldn't find that. It may have been deleted.",
    413: "That is too long for us to read in one go. Try a shorter piece.",
    429: "That was a lot at once. Wait a moment and try again.",
  };
  class ApiError extends Error {
    constructor(status, err) {
      const plain = err && typeof err.message === "string" && err.message && status < 500 ? err.message : null;     // server sentences are shown as given (spec section 0)
      super(plain || FALLBACK[status] || (status >= 500 ? "Something went wrong on our side. Try again in a moment." : "Something went wrong. Try again."));
      this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; this.raw = err || null;
    }
  }
  G.ApiError = ApiError;
  async function call(method, path, body, signal) {
    let res, data = null;
    try { res = await fetch("/api" + path, { method, signal, headers: body !== undefined && body !== null ? { "Content-Type": "application/json" } : {}, body: body !== undefined && body !== null ? JSON.stringify(body) : undefined }); }
    catch (e) { if (e && e.name === "AbortError") throw e; throw new ApiError(0, null); }
    try { data = await res.json(); } catch (_) { data = null; }
    if (res.status >= 400) throw new ApiError(res.status, data && data.error);
    return data;
  }
  const t = (token) => "/cases/" + enc(token);
  G.api = {
    call,
    health: (s) => call("GET", "/health", null, s),
    cases: (s) => call("GET", "/cases", null, s),                                          // local mode only; 404 elsewhere (spec 3.3)
    createCase: (payload, s) => call("POST", "/cases", payload, s),                         // {text} or {sample:true}
    getCase: (token, s) => call("GET", t(token), null, s),
    rename: (token, title) => call("PATCH", t(token), { title }),
    remove: (token) => call("DELETE", t(token)),
    run: (token, confirmRerun) => call("POST", t(token) + "/run", { confirm_rerun: !!confirmRerun }),
    status: (token, s) => call("GET", t(token) + "/status", null, s),
    item: (token, id, s) => call("GET", t(token) + "/items/" + enc(id), null, s),
    review: (token, id, body) => call("POST", t(token) + "/items/" + enc(id) + "/review", body),
    addEntry: (token, rid, body) => call("POST", t(token) + "/records/" + enc(rid) + "/entry", body),
    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + enc(rid) + "/confirm_date", { date }),
    rejudge: (token) => call("POST", t(token) + "/rejudge"),
    trace: (token, s) => call("GET", t(token) + "/trace", null, s),
    exportCase: (token, s) => call("GET", t(token) + "/export", null, s),
  };

  /* ---- store: health and the cases this tab has loaded. Pages call ctx.refresh() after a write so the step bar and header follow. ---- */
  G.store = {
    health: null, cases: {},
    async load(token, signal) { const c = await G.api.getCase(token, signal); return G.store.put(token, c); },
    put(token, c) { G.store.cases[token] = c; G.emit("case", token, c); return c; },
  };

  /* ---- step rules (spec 9.1, 9.2): one definition, used by the step bar and (via fromSummary) by Your cases ---- */
  const live = (i) => i && i.state !== "rejected";
  const undecided = (i) => live(i) && (i.review_status === "pending" || !!i.edit_to_check);       // 9.1
  const norm = {
    fromCase(c) {
      const s2 = [].concat(c.entries || [], c.undated_entries || [], c.flags || []).filter(live), s3 = (c.amounts || []).filter(live);
      return { status: c.status, hasItems: s2.length + s3.length + (c.tray || []).length > 0, stage: null, stages: 8,
        s2: { total: s2.length, left: s2.filter(undecided).length }, s3: { total: s3.length, left: s3.filter(undecided).length }, ready: !!(c.review && c.review.ready_to_export) };
    },
    fromSummary(c) {          // one row of GET /api/cases
      const p = c.progress || {}, e = p.entries || { decided: 0, total: 0 }, f = p.flags || { decided: 0, total: 0 }, a = p.amounts || { decided: 0, total: 0 };
      return { status: c.status, hasItems: e.total + f.total + a.total > 0, stage: c.run ? c.run.steps_done : null, stages: (c.run && c.run.steps_total) || 8,
        s2: { total: e.total + f.total, left: e.total + f.total - e.decided - f.decided }, s3: { total: a.total, left: a.total - a.decided }, ready: !!c.export_ready };
    },
  };
  /* G.steps.states(input, hereStep) -> [{ n, state: "done"|"todo"|"attn"|"locked", status }] for the four steps. `input` is GET case JSON or one /api/cases row (detected by `progress.entries`).
     Current-ness is the page's, not the data's: the caller marks hereStep. Step 4 reads "Ready" from the same flag the list uses; a page that knows more (a blocker count) overrides with setStepStatus. */
  G.steps = {
    undecided, live,
    states(input, here) {
      const x = input && input.progress && input.progress.entries ? norm.fromSummary(input) : norm.fromCase(input || {});
      const unlocked = x.status === "ready" || (x.status === "failed" && x.hasItems);
      const out = [];
      const s1 = x.status === "ready" ? { state: "done", status: "Done" } : x.status === "running" ? { state: "todo", status: x.stage != null ? `Drafting ${Math.min(x.stage + 1, x.stages)} of ${x.stages}` : "Drafting" }
        : x.status === "failed" ? { state: "attn", status: "Run again" } : { state: "todo", status: "Not started" };
      out.push(s1);
      const two = !unlocked ? { state: "locked", status: "After step 1" } : x.s2.left === 0 ? { state: "done", status: "Done" } : { state: "todo", status: `${x.s2.left} of ${x.s2.total} left` };
      const three = !unlocked ? { state: "locked", status: "After step 1" } : x.s3.total === 0 ? { state: "done", status: "None found" } : x.s3.left === 0 ? { state: "done", status: "Done" }
        : { state: "todo", status: x.s3.left === x.s3.total ? `${x.s3.total} amount${x.s3.total === 1 ? "" : "s"}` : `${x.s3.left} of ${x.s3.total} left` };
      out.push(two, three);
      const ok = unlocked && two.state === "done" && three.state === "done";
      out.push(!unlocked ? { state: "locked", status: "After step 1" } : ok && x.ready ? { state: "todo", status: "Ready" } : { state: "todo", status: "Not yet" });
      out.forEach((s, i) => { s.n = i + 1; if (here && s.state === "todo" && i + 1 < here && (i === 1 || i === 2)) s.state = "attn"; });      // a step she left with undecided items needs a look
      return out;
    },
    /* counts for the title row ("Item N of M", "3 answered - 16 to go"): { total, left } */
    counts(c) { const x = norm.fromCase(c); return { step2: x.s2, step3: x.s3 }; },
  };

  /* A plain error block: message + Try again (when `retry` is given) + a way home. Used by the shell and available to pages. */
  G.errorBlock = function (err, retry, title) {
    const msg = err instanceof ApiError ? err.message : "Something went wrong. Try again.";
    return G.h("div", { class: "errbox", role: "alert", "data-testid": "page-error" },
      G.h("h1", { "data-testid": "page-title" }, title || "Something went wrong"), G.h("p", {}, msg),
      G.h("div", { class: "row-actions" },
        retry ? G.h("button", { type: "button", class: "btn primary lg", "data-testid": "btn-retry", onclick: retry }, "Try again") : null,
        G.h("a", { class: "btn lg", href: "/", "data-testid": "link-home" }, "Back to your cases")));
  };
})();
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment Timeline</title>
<!-- Absolute URLs: the guided app uses real paths (/case/<token>/timeline), so a relative URL would resolve under the case path. No inline script or style (CSP). -->
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/review.css">
<link rel="stylesheet" href="/home.css">
<link rel="stylesheet" href="/step1.css">
<link rel="stylesheet" href="/step2.css">
<link rel="stylesheet" href="/step3.css">
<link rel="stylesheet" href="/step4.css">
</head>
<body class="page">
<a class="skip" href="#view" data-testid="skip-main">Skip to the main content</a>
<div class="stick" data-testid="chrome">
  <div class="banner" id="banner-synthetic" data-testid="banner-synthetic" role="note"><span id="banner-text">Synthetic data only — never paste real records</span><span class="b-demo" id="banner-demo"></span></div>
  <header class="header" id="header" data-testid="app-header"></header>
  <nav class="steps" id="step-bar" data-testid="step-bar" aria-label="Steps" hidden><ol id="step-list"></ol></nav>
</div>
<div class="view" id="view" data-testid="view" tabindex="-1"></div>
<footer class="footer" id="footer" data-testid="footer"></footer>
<!-- load order: core (namespace, dom builder, api, store, step states) -> pages (one file per module) -> app (chrome, router, boot) -->
<script src="/core.js"></script>
<script src="/review.js"></script>
<script src="/home.js"></script>
<script src="/step1.js"></script>
<script src="/step2.js"></script>
<script src="/step3.js"></script>
<script src="/step4.js"></script>
<script src="/app.js"></script>
</body>
</html>
/* Shared helpers for the two review pages (step 2 timeline, step 3 bills): the frame builder, the action bar and the layout-stability helpers. OWNER: the Step 2 + Step 3 builder.
   Empty on purpose (T-181 scaffold). Keep it free of step-specific rules; step2.js and step3.js call into it. Spec 2.5-2.7. */
(function () {
  const G = window.G; G.review = G.review || {};
})();
/* Step 2: Check the timeline (/case/<token>/timeline[?item=<id>]). PLACEHOLDER from the T-181 scaffold: it only draws the empty frame so the layout can be tested.
   OWNER: the Step 2 + Step 3 builder; replace the body, keep the registration. Spec section 5. Frame layout: .titlebar, .work (two .card), .actions as children of ctx.view.
   The done screen switches to the single-panel layout with ctx.layout("page"). Use ctx.case (loaded by the shell), ctx.refresh() after every write, G.steps.counts(ctx.case). */
(function () {
  const G = window.G, { h } = G;
  G.pages.timeline = async function (ctx) {
    ctx.view.append(
      h("div", { class: "titlebar" }, h("div", { class: "t-main" }, h("div", { class: "eyebrow" }, "Step 2 of 4"), h("h1", { "data-testid": "page-title" }, "Check the timeline"))),
      h("main", { class: "work", id: "main" }, h("section", { class: "card card-src", "aria-label": "From the record" }, h("div", { class: "card-b" }, h("p", { class: "muted", "data-testid": "placeholder" }, "This step is not built yet."))), h("section", { class: "card", "aria-label": "To check" }, h("div", { class: "card-b" }))),
      h("div", { class: "actions" }, h("div", { class: "actions-in" }, h("div", { class: "small" }, h("a", { class: "btn quiet", href: G.url.records(ctx.token), "data-testid": "btn-back" }, "‹ Back"), h("a", { class: "btn quiet", href: G.url.bills(ctx.token), "data-testid": "btn-next" }, "Next")))));
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:11.143Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && cat styles.css; cat /Users/arsis/zlayt-pm-project/tests/e2e/guided/test_shell_smoke.py"
}
````

### User / tool · 2026-11-02T21:27:11.230Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:13.889Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && sed -n 40,454p styles.css | cut -c1-260"
}
````

### User / tool · 2026-11-02T21:27:13.973Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:14.175Z

**tool call — Bash**
````
{
 "command": "cat tests/e2e/guided/test_shell_smoke.py; sed -n 1,80p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T21:27:14.259Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:16.523Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/bedgpgh6t.txt"
}
````

### User / tool · 2026-11-02T21:27:16.673Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:21.256Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && wc -l build.py guided.js; grep -n \"def \\|^# \" build.py | head -80; sed -n 248p ../../../app/frontend/guided/styles.css"
}
````

### User / tool · 2026-11-02T21:27:21.396Z

**tool result**
````
     586 build.py
     101 guided.js
     687 total
14:# ---------------------------------------------------------------- record texts (verbatim from the synthetic inputs)
33:def long_date(iso):
38:# ---------------------------------------------------------------- the four cases' step states (state, status)
51:def head(title, body_class):
66:def header(case_title=None, sub=None):
77:def stepbar(case, states, here):
94:def footer(extra=""):
99:def rec_html(seq, rec, marks=(), sentences=None, show_head=True):
120:def frame(*, fname, title, case, case_title, sub, states, here, eyebrow, h1, count, answered, total, pct, source_head, source_body,
140:def A(label, href, cls="answer", id_=None, disabled=False, sub=None):
148:def smalls(back="#", third=None, later="#"):
158:def page(fname, title, body, *, case=None, case_title=None, sub=None, states=None, here=None, wide=False):
166:# ---------------------------------------------------------------- case step states
183:def entry_head(tag, iso, src):
187:def rhead(seq):
192:# ================================================================ HOME
193:def card(title, meta, track, nxt, nxt_cls, btn, href, btn_label="Continue"):
202:def home():
239:# ================================================================ STEP 1
240:def step1():
265:    def drafting(fname, case, title, prepared, start, slow, sub, nxt, counts):
294:# ================================================================ STEP 2
295:def step2():
440:# ================================================================ STEP 3
441:def step3():
492:# ================================================================ STEP 4
493:def golden():
500:def step4():
503:    def letter_page(fname, case, title, states, top, copy_lock, notes_txt):
545:# ================================================================ SCREENS INDEX
546:def screens():
/* answers list */
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:23.496Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && sed -n 192,293p build.py; sed -n 492,545p build.py"
}
````

### User / tool · 2026-11-02T21:27:23.607Z

**tool result**
````
# ================================================================ HOME
def card(title, meta, track, nxt, nxt_cls, btn, href, btn_label="Continue"):
    tr = "".join(f'<li class="{s}"><i></i>{e(l)}</li>' for s, l in zip(track, ["Add records", "Timeline", "Bills", "Letter"]))
    return (f'<article class="ccard" data-title="{e(title)}"><div class="cc-top"><h3>{e(title)}</h3><button type="button" class="btn quiet">Rename</button></div>'
            f'<div class="cc-meta">{e(meta)}</div><ol class="track" aria-label="Steps">{tr}</ol>'
            f'<p class="next {nxt_cls}">{nxt}</p>'
            f'<div class="cc-bottom"><a class="btn lg {btn}" href="{href}">{e(btn_label)}</a><button type="button" class="btn quiet danger" data-delete>Delete</button></div>'
            f'<div class="cc-bottom" hidden><span style="flex:1;font-weight:600">Delete this case and all its answers?</span><button type="button" class="btn danger">Yes, delete</button><button type="button" class="btn" data-keep>Keep it</button></div></article>')


def home():
    cards_prog = [
        card("Jordan Rivera (sample)", "Started Nov 2 · 9 records", ["done", "current", "", ""], "<b>Next:</b> Check the timeline. 16 of 19 items left.", "", "primary", "step2-entry.html"),
        card("Priors and ledger", "Started Nov 2 · 9 records", ["done", "done", "current", ""], "<b>Next:</b> Check the bills. 7 of 8 amounts left.", "", "primary", "step3-count.html"),
        card("Date formats", "Started Nov 2 · 8 records", ["done", "current", "", ""], "<b>Next:</b> Check the timeline. 1 item left: pick a date.", "", "primary", "step2-date.html"),
        card("Er only then gap", "Started Nov 2 · 6 records", ["current", "", "", ""], "<b>Next:</b> Wait while the timeline is drafted (stage 3 of 8).", "", "primary", "step1-drafting-lib01.html"),
        card("Second crash, MRI after", "Started Nov 2 · 7 records", ["attn", "", "", ""], "<b>Next:</b> Drafting stopped. Run it again.", "warn", "primary", "step1-failed.html"),
    ]
    cards_done = [card("Sample case (practice run)", "Started Nov 1 · 9 records · finished Nov 1", ["done", "done", "done", "done"],
                       "<b>Finished.</b> Your letter is ready.", "ok", "go", "step4-letter-practice.html", "Open letter")]
    body = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'
            '<a class="btn primary lg" href="step1-add.html">+ Start a new case</a></div>'
            '<div class="find"><label class="sr" for="find-case">Find a case</label><input id="find-case" type="search" placeholder="Find a case by name"></div>'
            f'<h2 class="sec-h">In progress <span class="c">{len(cards_prog)}</span></h2><div class="cases">{"".join(cards_prog)}</div>'
            f'<h2 class="sec-h">Finished <span class="c">{len(cards_done)}</span></h2><div class="cases">{"".join(cards_done)}</div>')
    page("index.html", "Your cases", body, wide=True)

    empty = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div></div>'
             '<div class="panel empty"><div class="em-ic" aria-hidden="true">+</div><h2>You don\'t have any cases yet.</h2>'
             '<p>A case is one client\'s medical records. We\'ll guide you through 4 steps: add the records, check the timeline, check the bills, and get your letter.</p>'
             '<div class="row-actions"><a class="btn primary lg" href="step1-add.html">+ Start a new case</a><a class="btn lg" href="step1-found.html">Try the sample case</a></div></div>')
    page("home-empty.html", "Your cases (empty)", empty, wide=True)

    sk = "".join('<article class="ccard" aria-hidden="true"><div class="skel" style="height:28px;width:60%"></div><div class="skel" style="height:18px;width:40%"></div>'
                 '<div class="skel" style="height:24px"></div><div class="skel" style="height:44px"></div><div class="skel" style="height:56px"></div></article>' for _ in range(3))
    loading = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'
               '<a class="btn primary lg" href="step1-add.html">+ Start a new case</a></div>'
               f'<p class="sr" role="status">Loading your cases</p><h2 class="sec-h">Loading your cases…</h2><div class="cases">{sk}</div>')
    page("home-loading.html", "Your cases (loading)", loading, wide=True)

    err = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'
           '<a class="btn primary lg" href="step1-add.html">+ Start a new case</a></div>'
           '<div class="panel empty"><div class="em-ic" aria-hidden="true" style="background:var(--bad-bg);color:var(--bad)">!</div><h2>We couldn\'t load your cases.</h2>'
           '<p>The server didn\'t answer. Your cases are safe; nothing was changed.</p><div class="row-actions"><a class="btn primary lg" href="index.html">Try again</a></div></div>')
    page("home-error.html", "Your cases (error)", err, wide=True)


# ================================================================ STEP 1
def step1():
    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>Add records</h1>'
            '<p>Add the medical records for this case. We\'ll read them and draft a timeline for you to check.</p></div></div>'
            '<div class="panel"><div class="field"><label for="case-name">Name this case (optional)</label>'
            '<input id="case-name" value="Jordan Rivera (sample)" maxlength="120"><span class="hint">For example the client\'s name. You can change it later.</span></div>'
            '<fieldset style="border:0;padding:0;margin:0"><legend class="sr">How do you want to add the records?</legend><div class="tiles">'
            '<label class="tile"><input type="radio" name="how" value="paste"><span class="tl-h">Paste text</span><p>Copy the records and paste them here.</p></label>'
            '<label class="tile"><input type="radio" name="how" value="file"><span class="tl-h">Upload a file</span><p>A .txt or .pdf file, up to 5 MB.</p></label>'
            '<label class="tile"><input type="radio" name="how" value="sample" checked><span class="tl-h">Use the sample case</span><p>A short synthetic case to try it out.</p></label>'
            '</div></fieldset>'
            '<div class="input-box solid"><div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;height:100%"><b style="font-size:1.25rem">The sample case</b>'
            '<span class="muted">9 short records from a fictional car-accident case (Jordan Rivera, 41, Austin). Every name and date in it is made up.</span></div></div>'
            '<p class="err-slot" role="alert"></p>'
            '<div class="row-actions" style="margin-top:8px;align-items:center"><a class="btn primary lg" href="step1-found.html">Read the records</a>'
            '<span class="muted">This demo can only read the sample and our test cases.</span></div></div>')
    page("step1-add.html", "Add records", body, case="new", case_title="New case", states=NEW, here=1)

    rows = "".join(f'<li><span class="n">{n}</span><span class="num">{e(long_date(d))}</span><span class="src">{e(s)}</span></li>' for n, (d, s, _) in RIVERA.items())
    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>We found 9 records</h1>'
            '<p>Check that these are the records you meant to add. Next, we\'ll draft a one-line timeline entry for each one.</p></div></div>'
            '<div class="panel fixed-box"><div class="note-box ok" style="margin-bottom:16px"><span class="nb-text">Every record has a date we could read.</span></div>'
            f'<ol class="list" style="max-height:440px">{rows}</ol>'
            '<div class="row-actions"><a class="btn primary lg" href="step1-drafting.html">Draft the timeline</a><a class="btn lg" href="step1-add.html">Start over with other records</a></div></div>')
    page("step1-found.html", "Records found", body, case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=FOUND, here=1)

    def drafting(fname, case, title, prepared, start, slow, sub, nxt, counts):
        stg = [("Reading the records", ""), ("Loading the prepared line for each record" if prepared else "Writing one line for each record", ""),
               ("Checking every quote word for word", ""), ("Double-checking each line a second way", ""), ("Finding the bill amounts", ""),
               ("Comparing the records with each other", ""), ("Looking for things the attorney should know", ""), ("Putting it all together", "")]
        lis = "".join(f'<li class="{"done" if i < start else ("now" if i == start else "")}"><span class="ic" aria-hidden="true">{"&#10003;" if i < start else ""}</span>{e(s)}</li>' for i, (s, _) in enumerate(stg))
        body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>Drafting the timeline</h1>'
                '<p>This usually takes under a minute. You can leave this page; we\'ll keep going.</p></div></div>'
                f'<div class="panel fixed-box"><div id="draft-running"><div class="count-line"><span>Working on it</span><span class="num" id="draft-count">{start + 1} of 8</span></div>'
                f'<div class="bar" role="progressbar" aria-label="Drafting progress"><i id="draft-bar" style="width:{round(start / 8 * 100)}%"></i></div>'
                f'<ol class="stages" id="stages" data-start="{start}"{" data-slow" if slow else ""} aria-live="polite">{lis}</ol></div>'
                f'<div id="draft-done" hidden><div class="done-hero"><div class="big-check" aria-hidden="true">&#10003;</div><div><h2>All set.</h2>'
                f'<p>{e(counts)}</p></div></div><p class="muted" style="margin-top:16px">{e(AI_BANNER)}</p>'
                f'<div class="row-actions"><a class="btn primary lg" href="{nxt}">Go to step 2: Check the timeline</a></div></div></div>')
        page(fname, "Drafting", body, case=case, case_title=title, sub=sub, states=DRAFT, here=1)

    drafting("step1-drafting.html", "rivera", "Jordan Rivera (sample)", True, 0, False, "9 records", "step2-entry.html",
             "19 timeline items and 4 bill amounts are ready for you to check.")
    drafting("step1-drafting-lib01.html", "lib01", "Er only then gap", False, 2, True, "6 records", "index.html",
             "The timeline items and bill amounts are ready for you to check.")

    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>Drafting stopped</h1>'
            '<p>Some of the work finished. You can run it again; nothing you decided is lost.</p></div></div>'
            '<div class="panel fixed-box"><div class="done-hero"><div class="big-warn" aria-hidden="true">!</div><div><h2>Drafting stopped before it finished.</h2>'
            '<p>The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.</p></div></div>'
            '<div class="row-actions"><a class="btn primary lg" href="step1-drafting-lib01.html">Run it again</a><a class="btn lg" href="index.html">Back to your cases</a></div>'
            '<p class="muted" style="margin-top:20px">The items that did finish can be checked now in steps 2 and 3.</p></div>')
    page("step1-failed.html", "Drafting stopped", body, case="lib08", case_title="Second crash, MRI after", sub="7 records", states=FAILED, here=1)


# ================================================================ STEP 4
def golden():
    txt = (OUT.parents[2] / "evals/golden/sample.export.expected.txt").read_text()
    letter = txt.split("=== LETTER_TEXT (block 1: paste into letter) ===\n")[1].split("=== INTERNAL_NOTES_TEXT")[0].rstrip("\n")
    notes = txt.split("=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\n")[1].rstrip("\n")
    return letter, notes


def step4():
    letter, notes = golden()

    def letter_page(fname, case, title, states, top, copy_lock, notes_txt):
        lock = ' aria-disabled="true" tabindex="-1"' if copy_lock else ""
        body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 4 of 4</div><h1>Get your letter</h1>'
                '<p>Copy the treatment section into your demand letter, or download it. The notes on the right are for the attorney only.</p></div></div>'
                f'{top}<div class="letter-grid" style="margin-top:20px"><section><div class="doc-h"><h2>Your letter section</h2><span class="muted">Paste into the demand letter</span></div>'
                f'<pre class="doc" id="letter" tabindex="0">{e(letter)}</pre>'
                f'<div class="doc-actions"><button type="button" class="btn primary lg" data-copy="letter" id="copy-letter"{lock}>Copy letter</button>'
                f'<button type="button" class="btn lg" data-download="letter" data-name="jordan-rivera-letter.txt" id="dl-letter"{lock}>Download letter (.txt)</button></div></section>'
                '<section><div class="doc-h"><h2>Notes for the attorney</h2><span class="muted" style="color:var(--bad);font-weight:700">Do not send</span></div>'
                f'<pre class="doc notes" id="notes" tabindex="0">{e(notes_txt)}</pre>'
                f'<div class="doc-actions"><button type="button" class="btn lg" data-copy="notes"{lock}>Copy notes</button>'
                f'<button type="button" class="btn lg" data-download="notes" data-name="jordan-rivera-notes.txt"{lock}>Download notes</button></div></section></div>'
                '<div class="panel" style="margin-top:24px"><h2>Exhibit and page numbers (optional)</h2><p class="muted">Fill these in to replace “[Ex. __ / Bates __]” in every source line.</p>'
                '<div class="cfg"><div class="field"><label for="ex">Exhibit</label><input id="ex" placeholder="e.g. 4"></div>'
                '<div class="field"><label for="bp">Bates prefix</label><input id="bp" placeholder="e.g. RIV"></div>'
                '<div class="field"><label for="bs">First number</label><input id="bs" inputmode="numeric" placeholder="e.g. 1"></div>'
                '<button type="button" class="btn lg">Save numbers</button></div></div>')
        page(fname, "Get your letter", body, case=case, case_title=title, sub="9 records", states=states, here=4, wide=True)

    ready = ('<div class="note-box ok"><span class="nb-text">Your letter is ready. Every item has an answer.'
             '<span>9 timeline lines and 2 charges are in it. Nothing is left undecided.</span></span></div>')
    letter_page("step4-letter.html", "rivera", "Jordan Rivera (sample)", RIV_DONE, ready, False, notes)
    letter_page("step4-letter-practice.html", "practice", "Sample case (practice run)", RIV_DONE, ready, False, notes)

    pending_notes = notes.replace("Items not reviewed: 0.", "Items not reviewed: 3.")
    pend = ('<div class="note-box"><span class="nb-text">3 items still need a decision.<span>If you don\'t decide them, they stay out of the letter. The letter below is what would be sent now.</span></span>'
            '<a class="btn primary lg" href="step2-flag.html">Go to the first one</a></div>'
            '<label class="check" style="margin-top:14px"><input type="checkbox" data-unlocks="copy-letter dl-letter"> Copy it anyway, without those 3 items.</label>')
    letter_page("step4-pending.html", "rivera", "Jordan Rivera (sample)", RIV_PENDING, pend, True, pending_notes)

    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 4 of 4</div><h1>Get your letter</h1>'
            '<p>Copy the treatment section into your demand letter, or download it.</p></div></div>'
            '<div class="note-box bad"><span class="nb-text">The letter can\'t be made yet.<span>Fix the problem below, then come back here.</span></span></div>'
            '<ul class="blockers"><li><span>Nothing is accepted or edited yet, so the letter would be empty.</span><a class="btn primary" href="step2-entry.html">Go to step 2</a></li></ul>'
            '<div class="letter-grid" style="margin-top:20px"><section><div class="doc-h"><h2>Your letter section</h2></div>'
            '<div class="doc placeholder">Your letter will appear here once the problem above is fixed.</div>'
            '<div class="doc-actions"><button type="button" class="btn primary lg" aria-disabled="true" tabindex="-1">Copy letter</button><button type="button" class="btn lg" aria-disabled="true" tabindex="-1">Download letter (.txt)</button></div></section>'
            '<section><div class="doc-h"><h2>Notes for the attorney</h2></div><div class="doc notes placeholder">The notes appear with the letter.</div></section></div>')
    page("step4-blocked.html", "Letter blocked", body, case="rivera", case_title="Jordan Rivera (sample)", sub="9 records",
         states=[("done", "Done"), ("attn", "19 of 19 left"), ("attn", "4 of 4 left"), ("attn", "1 problem")], here=4, wide=True)


# ================================================================ SCREENS INDEX
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:23.773Z

**tool call — Bash**
````
{
 "command": "grep -n \"ccard\" app/frontend/guided/styles.css | head -3 | cut -c1-700"
}
````

### User / tool · 2026-11-02T21:27:23.887Z

**tool result**
````
287:.ccard { grid-template-columns: minmax(0, 1fr); min-height: 244px; background: var(--panel); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 22px 24px; display: grid; grid-template-rows: auto auto auto 1fr auto; gap: 10px; }
288:.ccard .cc-top { display: flex; gap: 12px; align-items: center; }
289:.ccard .cc-top .btn { height: 36px; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:29.085Z

**tool call — Bash**
````
{
 "command": "wc -l memory/contracts/api.md && grep -n \"^#\" memory/contracts/api.md | head -80"
}
````

### User / tool · 2026-11-02T21:27:29.192Z

**tool result**
````
     857 memory/contracts/api.md
1:# API contract — DRAFT — backend owns from M2
5:## Conventions
14:## Endpoint index
46:## GET /api/health
62:## POST /api/cases
82:## POST /api/cases/pdf (D-031)
86:### PDF hidden text and local OCR (T-087, T-086; D-042)
110:## POST /api/cases/{token}/review/batch (D-031)
114:## /api/cases/{token}/export_config (D-031)
117:## POST /api/cases/{token}/run
124:## GET /api/cases/{token}/status
134:## GET /api/cases/{token}
268:## POST /api/cases/{token}/records/{rid}/confirm_date
289:## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
301:## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
313:### POST /api/cases/{token}/dismissal_suggestions/apply
316:## GET /api/cases/{token}/items/{item_id}  — "Why?"
334:## POST /api/cases/{token}/items/{item_id}/review
386:## T-178 (GATE-M3 chaos): interrupted runs, stale tabs, paste text
394:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
423:## GET /api/cases/{token}/export
574:## GET /api/cases/{token}/audit
596:## Check traces (D-042): per-item stepper, case stepper, judge summary
603:### Step (shared by all three endpoints)
621:### GET /api/cases/{token}/items/{item_id}/trace
653:### GET /api/cases/{token}/trace
685:### GET /api/cases/{token}/judges
701:## POST /api/cases/{token}/rejudge  (D-044)
711:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
733:## GET /api/calibration  (T-099, serves T-090 counts to T-096)
743:## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
778:## Spanish-language records (T-085, D-042)
794:## Summary clause trimming (T-112, D-054)
797:## Dollar amounts in entries (T-139, D-019, R-CH-7, R-EX-8)
812:## DELETE /api/cases/{token}
817:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
850:## Prepared answers (T-177, D-065; amends D-029)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:30.989Z

**tool call — Bash**
````
{
 "command": "sed -n 1,135p memory/contracts/api.md | cut -c1-900"
}
````

### User / tool · 2026-11-02T21:27:31.095Z

**tool result**
````
# API contract — DRAFT — backend owns from M2

Status: drafted by the architect (T-014, round 2). From M2 the backend worker is the sole writer; changes after that go through a card. Frontend may start against the examples below. They use the Appendix A sample case (Jordan Rivera, SYNTHETIC) as stored in `evals/golden/sample.txt`; **every `start`/`end` is an absolute character offset into the case's raw text, and `raw_text[start:end]` equals the quoted string** (verified by a script run for the T-014 handoff). Design rationale: `memory/DECISIONS.md` ADR-002, 005, 006, 007, 009 to 017. Orchestrator decisions: `memory/ORCHESTRATOR_DECISIONS.md` (D-001..D-024). Requirements: `spec/REQUIREMENTS.md`; the conflicts it lists in §8 are resolved in ADR-017.

## Conventions
- Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
- `{token}` is the case id: a random 128-bit URL-safe string. It is the only credential. **There is no case-list endpoint.** An unknown token is `404 not_found`.
- Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409, re-run of a case that already has decisions only; never an edit or manual entry, D-047), `item_rejected` (409), `unsupported_language` (400, T-085: see Spanish-language records), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503), `busy` (429, retry later; `detail.reason` says which: `pdf_busy` (T-087: more than two PDF uploads are being read at once), `demo_full` (T-183 r2: the public demo already stores `DEMO_MAX_CASES` cases, default 200; on `POST /api/cases`; message "This demo is full right now. Try again later.") or `demo_busy` (T-18
- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
- Untrusted strings (record text, excerpts, summaries) are plain text; clients must insert them with `textContent`.

## Endpoint index
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
| GET | `/api/cases/{token}` | the whole case for the review screen |
| PATCH | `/api/cases/{token}` | T-157 rename: body `{title}` -> `{token, name, title}` |
| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
| GET | `/api/cases/{token}/status` | stage and progress |
| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as ente
| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id,
| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset, and (D-064) `count` + `confirm: "separate_charge"` for an amount held back only for a missing detail (see `countable`).  D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the pl
| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |

---

## GET /api/health
```json
{ "ok": true, "version": "0.1.0", "synthetic_only": true,
  "banner": "Synthetic data only — never paste real records",
  "backend": "fixture", "demo_mode": true, "answers": "prepared", "live_enabled": false,
  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
  "limits": {"max_chars": 60000, "max_records": 40},
  "retention_hours": 24,
  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
  "sample_available": true }
```
`answers` (T-177, D-065): whose answers the app shows. `prepared` = the curated fixture set (`FIXTURE_SET=curated`): hand-checked by the team, NOT model output; `recorded` = a replay of real model answers (the default fixture dir); `live` = a model answering now. The UI badge follows it: `prepared` -> "Demo: sample answers prepared by our team" (tooltip "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."; T-177 r2: the report does not hold the answers, so the old pointer was cut), `recorded` -> "Demo: recorded AI answers". With `prepared`, `ai_banner` reads "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item".

`models` (T-177 r2, D-065) on `GET /health`, `GET /cases/{token}` and `GET /cases/{token}/judges`: `{generator, judge, generator_prepared}`. When every generator answer of the case is a hand-checked fixture (`/health`: the set is `prepared`), `generator` is `"hand-checked (qa)"` and `generator_prepared` is `true`: no model drafted it, so no payload names one as the drafter. `judge` stays the real checking model. Recorded and live cases keep the configured generator model and `generator_prepared: false`. `GET /export` `provenance` carries the same `generator_model` and `generator_prepared`. The UI "How the AI was checked" line then reads "Prepared by our team (not by an AI model), checked by <judge>".
`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.

## POST /api/cases
Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). A title is plain text (T-157 r2): control, zero-width and bidi-override characters are removed, line breaks and tabs become spaces, runs of white space collapse; blank means no name. A `title` with a `<` or `>` in it, or longer than 120 characters, is refused: `422 invalid_title` with a plain `message` that never repeats the text, and no case is created (the same for the `title` query of `POST /api/cases/pdf`, checked before the PDF is read). The older `name` field is held to the markup rule too, but a `name` longer than 120 characters (a long file name) is cut, not refused. The response carrie
```json
{ "name": "Rivera sample", "text": "SYNTHETIC — ...\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, ...\"\n...", "sample": false }
```
Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ingested", "source": "paste",
  "demo_mode": true, "record_count": 9, "split_method": "code",
  "records": [
    { "id": "r1", "seq": 1, "source_label": "Austin EMS run report", "date_raw": "2026-01-09", "date_iso": "2026-01-09",
      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false,
      "char_start": 106, "char_end": 313,
      "text": "=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"" } ],
  "dates_to_confirm": [],
  "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
  "warnings": [] }
```
(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbe

## POST /api/cases/pdf (D-031)
Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).

### PDF hidden text and local OCR (T-087, T-086; D-042)
Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server. A page larger than 40 inches on a side is refused (`ocr_page_too_large`, `detail.page`); a larger one under that is rendered smaller than 150 dpi (longest side at most 3500 px, area at most 8 million px); all page images of one upload together are capped at 12 MB (`ocr_images_too_large`). Tesseract runs with a scrubbed environment (no API key or token reaches it). One deadline (10 s, or 165 s with OCR) covers text reading, the hidden-text scan and OCR; when 

**Hidden text.** Every text object is checked against the page as rendered (pypdfium2). Reasons: `invisible_render_mode`, `transparent`, `off_page`, `tiny_font` (under 5 pt effective), `blends_with_background` (a differential render, contrast under 96 levels counts as blending: the page is drawn with and without all text, and the text counts as hidden when the two agree under its box, so white or background-coloured text, text under a cover of any pattern, and text with marks, rules or dots in its box are all caught), `could_not_verify` (the check could not be made exactly, so the text is held back as suspected) `covered_by_annotation` (a form field, stamp or other annotation with an appearance lies over the text; some viewers draw it opaque while the renderer does not), `clipped` (a clipping window shows under half of the text's box) and `not_in_rendered_page` (words in the file's text 
**OCR.** A page with no text left and a picture on it is "scanned". Without `ocr=true` the upload is refused as before (`pdf_no_text_layer`) with `detail.scanned_pages: [..]` and `detail.ocr` (the status object below) so the UI can offer "Read scanned pages (OCR)". With `ocr=true`: `400 ocr_unavailable` (Tesseract missing or too old; `message` is the plain install line, `detail.ocr` the status), `ocr_too_many_pages`, `ocr_failed`, `ocr_check_failed` (the hidden-text check's child process was killed or crashed on this file, so it is not read with OCR; `detail.cause` is `memory`, `child_failed` or `child_died`) and `ocr_render_failed` (the child that draws the pages for OCR was killed or crashed, e.g. ran out of memory). Page drawing for OCR runs in the same killed child process as the hidden-text scan (deadline, CPU and memory limits); the API process never opens the PDF and never retries

Response and `GET /api/cases/{token}` gain, for PDF cases only:
```json
"pdf_checks": {
  "hidden_text": {"checked": true, "excluded_until_confirmed": true,
    "pages": [{"page": 2, "count": 1, "excluded": true, "confirmed": false,
               "items": [{"text": "…", "truncated": false, "reasons": ["blends_with_background"], "why": "not visible when the page is shown (the same colour as the page behind it, or covered)"}]},
              {"page": 3, "count": 0, "items": [], "unchecked": true, "why": "The page renderer could not read this page, so hidden text could not be checked.", "excluded": true, "confirmed": false}],
    "unchecked_pages": [3]},
  "ocr": {"requested": true, "ran": true, "scanned_pages": [3], "pages": [3], "engine": "tesseract 5.5.2", "low_conf_words": 12, "items_need_review": true,
          "low_conf_rule": "words under 60 confidence, or under 80 when the word has a digit",
          "status": {"available": true, "version": "5.5.2", "tested_version": "5.5.2", "languages": ["eng"], "message": "Tesseract 5.5.2 is available."}}},
"pdf_pages": [{"page": 3, "start": 0, "end": 812, "source": "ocr", "has_image": true, "mean_conf": 91.2, "words": 120, "low_conf_count": 12,
               "low_conf": [{"start": 40, "end": 47, "text": "Chaege:", "conf": 38.0}]}]
```
`checked: false` means at least one page could not be checked (`unchecked_pages`); those pages are held back like hidden text, so show them as pages to confirm, not as skipped. `pdf_pages[].start/end/low_conf[].start/end` are offsets into the case text; a page confirmed for hidden text carries `hidden_text_included: true`. Every record in a PDF case has `ocr_derived: true|false`.
**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the page image was compared). Its trace gains a failing code step `ocr_source` ("Record was not read from a scanned page", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.
**`GET /api/cases/{token}/pages/{n}/image`** -> `image/png` (greyscale, 150 dpi) of an OCR'd page, stored with the case and deleted with it; `404 not_found` for a page that has none. The UI shows it beside the page's text.

## POST /api/cases/{token}/review/batch (D-031)
**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}`.
Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. **D-059 (T-140 r2): charges are never batched.** A batch (accept or reset) that includes any amount of kind `charge` is refused whole: `422 CHARGES_NOT_BATCHED`, message "Charges are accepted one at a time, so a charge cannot be part of a batch. Take the charge out and review it by itself; nothing was changed.", `detail.rejected` lists `{id, reason: "charge_in_batch"}` for each charge. Frontend: remove charges from every batch/"accept all" selection and from any select-all; a charge has only the single-item accept/dismiss. All ids are checked before the first write: one b

## /api/cases/{token}/export_config (D-031)
`GET` returns `{"exhibit": null|string, "bates_prefix": null|string, "bates_start": null|int}`. `PUT` takes the same keys (all optional; omitted or empty means unset) and returns the stored config; `DELETE` clears it and returns the empty config. Validation: `exhibit` and `bates_prefix` up to 20 characters of `A-Za-z0-9 ._-`; `bates_start` an integer 0 to 99999999 (booleans and strings refused); unknown keys refused; any violation is `422 invalid_edit` and nothing changes. Effect on the export only: every letter citation `Source [Ex. __ / Bates __]` becomes `Source [Ex. <exhibit> / Bates <prefix><NNNN>]` with `NNNN` = first number + record number - 1, zero-padded to 4 digits (first number defaults to 1 when only a prefix is set; an unset part stays `__`). With no config the export is byte-identical to the golden. The internal notes never carry exhibit or Bates numbers.

## POST /api/cases/{token}/run
Request: `{ "confirm_rerun": false }`. Response 202:
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "extract", "started_at": "2026-11-02T01:02:03Z" }
```
Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.

## GET /api/cases/{token}/status
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "judge_entries",
  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
  "progress": {"done": 4, "total": 9, "label": "Checking summaries 4 of 9"},
  "counts": {"entries": 9, "amounts": 3, "flags": 1},
  "error": null, "elapsed_ms": 21540 }
```
`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a re-run (the extract step made a failure stub, a second check gave no answer, or the flag step was down) and the stored rows it would have overwritten, or deleted as stale, were left exactly as they were; `message` names how many items and which step ("The AI step failed for N items (writing the entries / the second check / finding the flags) on this run. Their earlier results and every decision of 

## GET /api/cases/{token}
**T-157, `title` and `next_action` (GET case, top level):** `title` is the same string `GET /api/cases` shows (see "Case titles" there; never "Untitled case"). `next_action` is `{item_id, kind, reason}` or `null`: the single first thing to do, the same value `GET /api/cases` carries (code only, deterministic; rules under "`next_action`" there). **`rerun_available` (bool, every entry, amount and flag view in this payload, in `GET .../items/{item_id}` `item` and in every review response `item`; not on `tray` items):** whether "Run the second check again" (`POST .../rejudge`) can get an answer for this item now. False in demo mode and with the fixture backend (no live model can answer: `ENABLE_LIVE` is not `1`, `LLM_BACKEND` is `fixture`, or `anthropic-api` has no key), and false after a rerun that got no answer (the last `ladder.rejudge` attempt is `unavailable`; it turns true again only w
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:33.677Z

**tool call — Bash**
````
{
 "command": "sed -n 711,732p memory/contracts/api.md | cut -c1-2500; sed -n 386,393p memory/contracts/api.md | cut -c1-2500; sed -n 423,470p memory/contracts/api.md | cut -c1-1800; sed -n 701,710p memory/contracts/api.md | cut -c1-1200"
}
````

### User / tool · 2026-11-02T21:27:33.811Z

**tool result**
````
## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` (T-148, the overview screen) -> `{ "cases": [ summary ] }`, newest first (`created_at`, then insertion order); every case the single local profile can see. Code only: no model call, no pipeline run, no record text. Local mode only: no auth, no users, no sharing (scope cut kept). One `summary`:
```
{ "token": "...", "title": "Er only then gap", "name": "case lib01 er only then gap" | null, "source": "paste|sample", "status": "ingested|running|ready|failed",
  "record_count": 9, "created_at": "...Z", "updated_at": "...Z", "last_activity_at": "...Z",
  "run": { "stage": "finalize" | "ingest" | null, "steps_done": 7, "steps_total": 8, "running": false, "error": false },
  "progress": { "entries": {"decided": 2, "total": 5}, "flags": {"decided": 0, "total": 2}, "amounts": {"decided": 0, "total": 2} },
  "counts": { "pending", "accepted", "edited", "dismissed", "needs_review" },
  "hitl": { "pending": 7, "needs_review": 4, "needs_review_open": 4, "edits_to_check": 0, "could_not_verify": 1,
            "gate_blockers": [ { "reason_code", "kind", "item_id", "why" } ], "gate_warnings": [ { "reason_code", "count", "why" } ] },
  "export_ready": true,
  "next_action": { "item_id": "f_r3_1" | null, "kind": "entry|flag|amount|case|run", "reason": "plain sentence" } | null,
  "status_error": false, "status_error_message": null }
```
**`status_error` (T-175 r2).** A case that was deleted while the list was read is left out. A case whose summary fails once is read again after 50 ms (a run or review was writing): if that works it is a normal row. If it fails twice in a row the case exists and the failure is a bug: the row is still listed (one bad case never takes the whole list down) but with `status_error: true` and `status_error_message: "We couldn't load this case's status"`. On such a row `record_count`, `counts`, `progress` and `hitl` are all `null` (never zeros), `export_ready` is `false`, `next_action` is `null`; `token`, `title`, `name`, `source`, `status`, the three times and `run` are still filled from the case row. The frontend shows the message in place of counts and progress, not an empty or zero state. Normal rows carry `status_error: false, status_error_message: null`. The server logs it at ERROR as `case list: a case's status could not be computed twice in a row (<ExceptionClass>)`, never any record text.
**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no name, or a name that is empty once cleaned (`case_01_`, `.txt`), the first record header: the provider (its Source line with any tags or angle brackets dropped, at most 60 characters) and that record's date, "Marrowgate General ED, Feb 14, 2026" ("Records from Feb 14, 2026" when the record has no Source line, the bare provider when it has no date); (3) when no record has either, "Records added Nov 2" ("Sample case" for the sample). `name` is the stored value, `null` until someone names the case. `PATCH /api/cases/{token}` with `{"title": "Rivera v. Acme"}` stores the name (same rule as on create: plain text, control characters removed, white space collapsed; a `<` or `>` or more than 120 characters is `422 invalid_title` and the stored name is unchanged) and answers `200 {token, name, title}`; a blank or `null` title clears the name, so the title returns to the derived default; a body without `title`, or a `title` that is neither text nor null, is `400 bad_request`; an unknown token is `404 not_found`. The name goes through the same readable-title step as any other, so underscores or a file extension in a typed title are shown as words. Allowed in public mode too (the token is the capability). A rename is not a review event. **A title is never markup:** a typed title is refused if it contains `<` or `>`, and a title derived from a record's Source line has its tags dropped, so `title` is always plain text and a client may still render it as text only (`textContent`), never as HTML.

**`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `hitl.needs_review_open` (T-157 r3) is the number of items still open in Needs review: `state: needs_review` and (`review_status: pending` or an unconfirmed edit,
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).

## T-178 (GATE-M3 chaos): interrupted runs, stale tabs, paste text

**Interrupted run (startup recovery).** A run is a thread of the server process. When the process stops (crash, sleep, redeploy) the case would stay `running` for ever. At startup every case still `running` that no thread of this process is running is set to `status: "failed"` with `error: {"code": "run_partial", "interrupted": true, "message": "The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry."}` and `run_finished_at` set. The same happens on any read of a `running` case that has no live thread and whose run started more than 600 s ago. Nothing item-level is touched: accepted, edited and dismissed items stay exactly as they were, the export gate reads `RUN_FAILED` (next action `CONFIRM_RERUN`), `POST .../run` is allowed again (`409 needs_confirm` while decisions exist, then `confirm_rerun: true`), and the re-run follows the T-146 rules (decided items are kept). Frontend: treat `failed` + `error.interrupted` like any `run_partial`: show `error.message` and the Run again button.

**Stale second tab (`stale_item`).** Every item view (`entries[]`, `amounts[]`, `flags[]`, `GET .../items/{id}` `item`, review responses `item`) now has `version`: a number that changes whenever the item changes. `POST .../items/{item_id}/review` accepts optional `version` (the item's `version` as the client last saw it) and/or `expected_status` (its `review_status` as last seen: `pending|accepted|edited|dismissed`). If either differs from the stored item the write is refused with `409 stale_item`, message **"This item changed in another tab; reload to see it."**, `detail: {item_id, review_status, version}` (the current ones), and nothing is written (no review event). Neither sent = no check (older clients). A repeat of a decision that would leave the item as it already is (accept on an accepted item, dismiss on a dismissed one, reset on a pending one) is let through. Other values: `422 invalid_edit` (`version` not a number, `expected_status` not one of the four). **Frontend must:** send `version` and `expected_status` from the item it is showing with every accept, dismiss, reset, edit and count; on `409 stale_item` show `error.message`, refetch the case (or `GET .../items/{id}`) and replace that item; update the stored `version` from every response that carries an item (batch responses do not carry one: refetch). Frontend does not send these yet (card note on T-178).

**Paste text.** Text is normalised before the empty check and the size limits (`ingest.normalize_text`, used by `POST /api/cases`, the demo-gate hash, the pipeline and PDF page assembly): every Unicode format character (category Cf: zero-width space/joiner/non-joiner, word joiner, BOM, bidi marks and overrides, soft hyphen, tag characters) is removed, and a lone UTF-16 surrogate is replaced by U+FFFD. A paste with nothing else in it is `400 bad_request` "Input is empty." and costs no model call; invisible characters do not count toward the 60,000-character limit; the stored case text is the cleaned text (excerpts and offsets index it). Every string in any JSON request body (titles, edits, notes) gets the same surrogate replacement at the door. No paste returns a 500.

## GET /api/cases/{token}/export
**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. An edit still marked `needs_review` is open and out of the letter, so it does not stop the export either (T-134, see the edit section). Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the only change to the quote is whitespace (each run of spaces and line breaks becomes one space); a translated entry adds ` — English: <summary>` after the bracket, before the translation note; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
```json
{
  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
  "generated_at": "2026-11-02T01:20:00Z",
  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges accepted from these records: $8,390.00",
  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
  "items": {
    "entries": [
      {
        "id": "e1",
        "record_ids": [
          "r1"
        ],
        "edited": false,
        "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
      },
      {
        "id": "e2",
        "record_ids": [
          "r2"
        ],
        "edited": false,
        "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
      },
      {
        "id": "e3",
        "record_ids": [
          "r3"
        ],
        "edited": false,
        "excerpt": "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
      },
      {
        "id": "e4",
        "record_ids": [
          "r4"
        ],
        "edited": false,
        "excerpt": "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
      },
      {
        "id": "e5",
        "record_ids": [
          "r5"
        ],
## POST /api/cases/{token}/rejudge  (D-044)
Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. 
```json
{ "token": "k3Jf9x...", "asked": 12,
  "rejudged": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "review_status": "accepted", "verdict": "supported", "state": "verified", "state_reasons": [] } ],
  "still_unavailable": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "review_status": "accepted", "verdict": "unavailable" } ],
  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
```
`verdict` is the ladder vocabulary (`supported|partially|unsupported|disagrees|unsure|unavailable`). Frontend: after the call, refetch `/trace` (and the case view, since `state` can change).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:37.533Z

**tool call — Bash**
````
{
 "command": "grep -n \"library\\|\\\"/api/cases\\\"\" app/backend/api.py | head -40; sed -n 1,140p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T21:27:37.697Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:39.406Z

**tool call — Bash**
````
{
 "command": "sed -n 262,330p app/backend/api.py | cut -c1-300; grep -n \"SERVER\\|ZLAYT\\|FIXTURE\\|E2E_\\|def pytest\\|subprocess\" tests/e2e/conftest.py | head -50"
}
````

### User / tool · 2026-11-02T21:27:39.552Z

**tool result**
````
    # -------------------------------------------------- routes
    @app.get("/api/health")
    def health():
        ans = answers()
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "answers": ans,
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}

    @app.get("/api/cases")
    def list_cases():
        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
            raise ApiError(404, "not_found", "Not found.")
        c = conn()
        try:
            return {"cases": case_list.summaries(c, list(getattr(pipeline_mod(), "STAGES", None) or STAGES))}
        finally:
            c.close()

    @app.get("/api/library")
    def library():
        if not local_mode():
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
        b = await body_of(request)
        sample = b.get("sample") is True
        lib = None
        if isinstance(b.get("library"), str):
            if not local_mode():
                raise ApiError(404, "not_found", "Not found.")
            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
            if lib is None:
                raise ApiError(404, "not_found", "No such library case.")
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        typed = isinstance(b.get("title"), str)
        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)

    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        valid_name(title if title is not None else name, title is not None)          # T-157 r2: a markup title is refused before a byte is read
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
            raise ApiError(413, "input_too_large", "The PDF is too large.")
        data = b""
        async for chunk in request.stream():
            data += chunk
            if len(data) > pdf_text.MAX_PDF_BYTES:
                raise ApiError(413, "input_too_large", "The PDF is too large.")
        opts = {}
        if (ocr or "").lower() in ("1", "true", "yes"):
            opts["ocr"] = True
        if include_hidden:
            opts["include_hidden"] = include_hidden
        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data, **opts), _pdf_checks.OCR_TIMEOUT_S if opts.get("ocr") else pdf_text.EXTRACT_TIMEOUT_S)
        except asyncio.TimeoutError:
            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
        except pdf_text.PdfError as e:
            if e.code == "pdf_busy":     # T-087 round 4: at most pdf_checks.MAX_PDF_JOBS uploads are read at once; the rest are told to retry
                raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
106:SERVER = os.environ.get("E2E_BASE_URL", "http://localhost:7860")      # the app's root: the guided UI (D-068) is served here, and every /api call goes here
107:BASE = SERVER + "/classic"                                              # D-068: the old screen moved to /classic; the whole classic suite navigates from BASE, API calls use SERVER
116:def pytest_configure(config):
117:    """T-136 r2 (staff review F1): a plain `pytest tests/e2e` must RUN the specs that write to the server's SQLite file (ZLAYT_DB: test_edit_to_check, test_code_check_refusal, test_change_the_quote,
118:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
119:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
120:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
121:    global BASE, SERVER
122:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
124:    import atexit, shutil, socket, subprocess, sys, tempfile, time
127:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
130:    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
156:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; SERVER = base; BASE = base + "/classic"
166:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
168:    path = os.environ.get("ZLAYT_DB")
170:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
171:        if os.environ.get("E2E_REQUIRE_DB") == "1":
178:        urllib.request.urlopen(SERVER + "/api/health", timeout=2).read()
183:def pytest_collection_modifyitems(config, items):
186:    skip = pytest.mark.skip(reason=f"app server not running at {SERVER} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
192:    req = urllib.request.Request(SERVER + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
205:    """T-173 (T-168): put one record's entry into the could-not-verify tray the way the pipeline does when the extract step has no answer for it (FIXTURE_MISS). T-168 recorded lib01
207:    with the pipeline's own placeholder: generator.failure_entry(record, group, 'FIXTURE_MISS') (no summary, no quote, ladder.failure set, no generator or judge), written through
222:        f = generator.failure_entry(rec, [rec["n"]], "FIXTURE_MISS")
230:    assert t and t["kind"] == "entry" and t["reasons"] == ["FIXTURE_MISS"] and t["attempt"] == {"summary": None, "excerpt": None}, t
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:42.423Z

**tool call — Bash**
````
{
 "command": "grep -n \"def demo_mode\\|def local_mode\\|def answers\" -A6 app/backend/api.py | head -40; sed -n 106,165p tests/e2e/conftest.py; git log --oneline | head -5; git status --short | head -20"
}
````

### User / tool · 2026-11-02T21:27:42.586Z

**tool result**
````
83:def local_mode() -> bool:
84-    return os.environ.get("ZLAYT_MODE") == "local"
85-
86-
87-def is_loopback_peer(request) -> bool:
88-    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
89-    host = request.client.host if request.client else None
--
127:    def demo_mode():
128-        return not live_enabled()
129-
130:    def answers():
131-        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
132-        if live_enabled():
133-            return "live"
134-        from app.llm.backends import fixture
135-        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
136-
SERVER = os.environ.get("E2E_BASE_URL", "http://localhost:7860")      # the app's root: the guided UI (D-068) is served here, and every /api call goes here
BASE = SERVER + "/classic"                                              # D-068: the old screen moved to /classic; the whole classic suite navigates from BASE, API calls use SERVER
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
import sys
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)                 # tray_entry_for_record imports the app's own placeholder builder
_PRIVATE = {}


def pytest_configure(config):
    """T-136 r2 (staff review F1): a plain `pytest tests/e2e` must RUN the specs that write to the server's SQLite file (ZLAYT_DB: test_edit_to_check, test_code_check_refusal, test_change_the_quote,
    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
    global BASE, SERVER
    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
        return
    import atexit, shutil, socket, subprocess, sys, tempfile, time
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"

    def fail(why):
        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
        if proc.poll() is None:
            proc.kill()
        log.close()
        try:
            tail = open(os.path.join(tmp, "server.log")).read()[-2000:]
        except OSError:
            tail = ""
        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)

    for _ in range(80):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            if proc.poll() is not None:
                fail(f"exited with code {proc.returncode} before it answered")
            time.sleep(0.5)
    else:
        fail("did not answer /api/health within 40 seconds")
    if proc.poll() is not None:
        fail(f"exited with code {proc.returncode} right after it answered")
    _PRIVATE.update(proc=proc, tmp=tmp)
    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; SERVER = base; BASE = base + "/classic"
    def stop():
        proc.terminate()
        try: proc.wait(timeout=10)
        except Exception: proc.kill()
        log.close(); shutil.rmtree(tmp, ignore_errors=True)
    atexit.register(stop)


def needs_db():
ddfbf6d docs(submission): T-185/T-186 round 2: redesign story (persona 4/5 predates D-068), only-committed claims, fresh unit count, library recall beside golden, engineering role, stretch reasons
f3d42a2 feat(frontend): T-181 guided UI scaffold (D-068): / is the guided app, old screen at /classic
275e4ca feat(backend): public demo caps stored cases and runs in flight, plain 429 (T-183 r2)
ed0508e fix(qa): prompt-log redacts private-network details everywhere, README lists every edit with counts (T-187 r2)
33e88c6 tools: prompt-log export also redacts tailnet hostnames, 100.64/10 addresses and a work email; docstring lists every edit (T-187 privacy review)
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:49.525Z

**tool call — Bash**
````
{
 "command": "grep -n \"def live_enabled\" -B2 -A10 app/backend/api.py; grep -n \"demo_mode_unsupported_input\\|input_too_large\" app/backend/api.py | head -20; ls evals/library | head -30; ls .venv/bin | grep -i \"python\\|pytest\""
}
````

### User / tool · 2026-11-02T21:27:49.693Z

**tool result**
````
122-        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
123-
124:    def live_enabled():
125-        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available
126-
127-    def demo_mode():
128-        return not live_enabled()
129-
130-    def answers():
131-        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
132-        if live_enabled():
133-            return "live"
134-        from app.llm.backends import fixture
41:_ERR_STATUS = {"bad_request": 400, "input_too_large": 413, "unsupported_language": 400}
246:            raise ApiError(413, "input_too_large", "Input is too large.")
251:                raise ApiError(413, "input_too_large", "Input is too large.")
309:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
313:            raise ApiError(413, "input_too_large", "The PDF is too large.")
318:                raise ApiError(413, "input_too_large", "The PDF is too large.")
331:            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
353:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
372:                        msg = "Input is too large." if e.code == "input_too_large" else "Input is empty." if e.code == "bad_request" else "The input could not be read."
445:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
473:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
pytest
python
python3
python3.12
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:56.925Z

**tool call — Bash**
````
{
 "command": "grep -rn \"def live_enabled\" -A12 app/backend/store.py; sed -n 340,380p app/backend/api.py | cut -c1-260"
}
````

### User / tool · 2026-11-02T21:27:57.054Z

**tool result**
````
app/backend/store.py:67:def live_enabled() -> bool:
app/backend/store.py-68-    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
app/backend/store.py-69-    Read per call so a test can change the environment."""
app/backend/store.py-70-    from app.llm import provider
app/backend/store.py-71-    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
app/backend/store.py-72-
app/backend/store.py-73-
app/backend/store.py-74-def live_model_available() -> bool:
app/backend/store.py-75-    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
app/backend/store.py-76-    from app.llm import provider
app/backend/store.py-77-    return provider.backend_name() != "fixture" and live_enabled()
app/backend/store.py-78-
app/backend/store.py-79-
        try:
            return case_list.validate_title(value) if strict else case_list.clean_title(value)
        except case_list.TitleError as e:
            raise ApiError(422, "invalid_title", str(e)) from None

    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
        name = name if isinstance(name, str) else ("Sample case" if sample else None)
        name = valid_name(name, strict_name)          # before anything is stored: a refused title leaves no case behind
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
                raise ApiError(429, "busy", full, {"reason": "demo_full"})
            cid = DB.create_case(c, text, now=now, name=name or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
                    msg, detail = language.api_fields(e)
                    if not msg:             # T-183: a limit hit during splitting (too many records) said "input too large" (the bare code); say it as a sentence
                        msg = "Input is too large." if e.code == "input_too_large" else "Input is empty." if e.code == "bad_request" else "The input could not be read."
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, msg, detail) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                    "dates_to_confirm": present.dates_to_confirm(c, cid),
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:28:07.899Z

**tool call — Bash**
````
{
 "command": "mkdir -p /tmp/zl-a 2>/dev/null; D=$(mktemp -d /private/tmp/claude-501/zla-XXXX); echo $D > /private/tmp/claude-501/zla-dir; (PORT=7911 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$D/db.sqlite3 .venv/bin/python -m app.main > $D/server.log 2>&1 & echo $! > /private/tmp/claude-501/zla-pid); sleep 4; curl -s localhost:7911/api/health; echo; curl -s localhost:7911/api/cases; echo; curl -s localhost:7911/api/library | head -c 600"
}
````

### User / tool · 2026-11-02T21:28:12.147Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
{"cases":[]}
{"cases":[{"id":"case_lib01_er_only_then_gap","name":"case lib01 er only then gap","description":"Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is flagged; the reason is shown as the pat"},{"id":"case_lib02_slip_fall_prior_knee","name":"case lib02 slip fall prior knee","description":"Library L2 (mirrors S2). Store slip-and-fall with a prior knee arthroscopy shown in imaging and in the patient's history; MRI wording that may reflect both acute a
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:28:15.902Z

**tool call — Bash**
````
{
 "command": "T=$(curl -s -XPOST localhost:7911/api/cases -H 'content-type: application/json' -d '{\"sample\":true}' | .venv/bin/python -c \"import sys,json; d=json.load(sys.stdin); print(d['token']); print(json.dumps({k:v for k,v in d.items() if k!='records'})[:900], file=sys.stderr)\"); echo $T > /private/tmp/claude-501/zla-tok; curl -s -XPOST localhost:7911/api/cases/$T/run -H 'content-type: application/json' -d '{\"confirm_rerun\":false}'; echo; for i in 1 2 3; do curl -s localhost:7911/api/cases/$T/status; echo; sleep 1; done"
}
````

### User / tool · 2026-11-02T21:28:19.474Z

**tool result**
````
{"token": "mN7HPscbMblidUBI7k5U1Q", "name": "Sample case", "title": "Sample case", "status": "ingested", "source": "sample", "demo_mode": true, "record_count": 9, "split_method": "code", "dates_to_confirm": [], "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [], "warnings": []}
{"token":"mN7HPscbMblidUBI7k5U1Q","status":"running","stage":"extract","started_at":"2026-11-02T21:28:16Z"}
{"token":"mN7HPscbMblidUBI7k5U1Q","status":"running","stage":"extract","stages":["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],"progress":{"done":1,"total":8,"label":"Step 2 of 8: extract"},"counts":{"entries":0,"amounts":4,"flags":2},"error":null,"elapsed_ms":246}
{"token":"mN7HPscbMblidUBI7k5U1Q","status":"ready","stage":"finalize","stages":["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],"progress":{"done":7,"total":8,"label":"Step 8 of 8: finalize"},"counts":{"entries":9,"amounts":4,"flags":10},"error":null,"elapsed_ms":345}
{"token":"mN7HPscbMblidUBI7k5U1Q","status":"ready","stage":"finalize","stages":["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],"progress":{"done":7,"total":8,"label":"Step 8 of 8: finalize"},"counts":{"entries":9,"amounts":4,"flags":10},"error":null,"elapsed_ms":345}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:28:27.942Z

**tool call — Bash**
````
{
 "command": "T=$(cat /private/tmp/claude-501/zla-tok); curl -s localhost:7911/api/cases/$T | .venv/bin/python -c \"\nimport sys,json; d=json.load(sys.stdin); print(list(d.keys())); print(json.dumps(d['review'])[:800]); print(json.dumps(d['next_action'])); print(d['title'], d.get('models'), d.get('ai_banner'))\nprint(json.dumps(d['totals'])[:500])\nprint(json.dumps(d['entries'][0])[:900])\nprint(json.dumps(d['records'][0])[:500])\n\"; curl -s -w ' %{http_code}\\n' localhost:7911/api/cases/$T/export | head -c 1800; echo; curl -s localhost:7911/api/cases/$T/trace | .venv/bin/python -c \"import sys,json; d=json.load(sys.stdin); print(json.dumps(d['export_gate'])[:900])\""
}
````

### User / tool · 2026-11-02T21:28:28.108Z

**tool result (error)**
````
Exit code 1
['token', 'name', 'status', 'demo_mode', 'backend', 'models', 'records', 'undated_entries', 'entries', 'amounts', 'totals', 'flags', 'gap_changes_removed', 'checks', 'tray', 'tray_filtered', 'dates_to_confirm', 'injection', 'review', 'warnings', 'error', 'created_at', 'updated_at', 'title', 'next_action']
{"counts": {"pending": 23, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 3, "verified": 20, "rejected": 0, "edit_to_check": 0}, "queue": ["a2", "a3", "f_r7_1", "a1", "a4", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "f_accident_date_after_treatment_1_2_7", "f_cx1", "f_gap_r6_r7", "f_r3_1", "f_r6_1", "f_r7_2", "f_r8_1", "f_r8_2", "f_r9_1"], "ready_to_export": false}
{"item_id": "a2", "kind": "amount", "reason": "This figure is a rate, not a charge, so it is not added to the total."}
Sample case {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True} None
{"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"}, "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"}, "flagged_charges": [], "not_totaled": [{"id": "a2", "kind": "rate", "text": "$185"}], "possible_overlaps": []}
{"id": "e1", "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "review_status": "pending", "version": 1793654896.4942222, "edited": null, "ladder": {"backend": "fixture", "code_checks": {"date_provider_from_header": true, "excerpt_verbatim": true, "excerpt_whole_sentence": true, "highlight_found": true, "qualifier_carried": true, "summary_tokens_not_in_excerpt": []}, "generator": {"call_id": "c34d002b176d1", "model": "hand-checked (qa)", "output": {"excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.", "summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER."}, "prompt_version": "extract_v1", "prepared": true},
{"id": "r1", "seq": 1, "source_label": "Austin EMS run report", "date_raw": "2026-01-09", "date_iso": "2026-01-09", "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "char_start": 106, "char_end": 313, "text": "=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"", "language":
{"error":{"code":"export_blocked","message":"Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.","detail":{"blockers":[{"item_id":null,"kind":"case","reason_code":"NOTHING_ACCEPTED","why":"Nothing is accepted or edited yet, so the letter would be empty.","next_action":{"code":"DECIDE","text":"Accept, edit or dismiss this item.","target":{"view":"queue"}}}]}}} 422

Traceback (most recent call last):
  File "<string>", line 1, in <module>
KeyError: 'export_gate'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:29:20.752Z

**tool call — Bash**
````
{
 "command": "grep -n \"_PDF_MESSAGES\" -A14 app/backend/api.py | head -50; sed -n 330,340p app/backend/api.py | cut -c1-400"
}
````

### User / tool · 2026-11-02T21:29:20.842Z

**tool result**
````
42:_PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
43-                 "pdf_unreadable": "This file could not be read as a PDF.", "pdf_encrypted": "This PDF is password-protected and cannot be read.",
44-                 "pdf_too_large": "The PDF is too large."}
45-from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
46:_PDF_MESSAGES.update(_pdf_checks.MESSAGES)
47-
48-
49-log = logging.getLogger("zlayt.api")
50-
51-
52-class ApiError(Exception):
53-    def __init__(self, status, code, message="", detail=None):
54-        super().__init__(code)
55-        self.status, self.code, self.message, self.detail = status, code, message or code.replace("_", " "), detail or {}
56-
57-
58-def digest(text: str) -> str:
59-    return hashlib.sha256(ingest.normalize_text(text).encode("utf-8")).hexdigest()
60-
--
327:            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
328-        except pdf_text.PdfError as e:
329-            if e.code == "pdf_busy":     # T-087 round 4: at most pdf_checks.MAX_PDF_JOBS uploads are read at once; the rest are told to retry
330:                raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
331-            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
332:                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
333-        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None},
334-                        strict_name=title is not None)
335-        out["pdf_checks"] = got.get("pdf_checks")
336-        return out
337-
338-    def valid_name(value, strict=True):
339-        """T-157 r2: a typed title (or legacy `name`) -> the text to store; markup or an over-long typed title is 422 invalid_title with a plain message."""
340-        try:
341-            return case_list.validate_title(value) if strict else case_list.clean_title(value)
342-        except case_list.TitleError as e:
343-            raise ApiError(422, "invalid_title", str(e)) from None
344-
345-    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
346-        name = name if isinstance(name, str) else ("Sample case" if sample else None)
                raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None},
                        strict_name=title is not None)
        out["pdf_checks"] = got.get("pdf_checks")
        return out

    def valid_name(value, strict=True):
        """T-157 r2: a typed title (or legacy `name`) -> the text to store; markup or an over-long typed title is 422 invalid_title with a plain message."""
        try:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:29:23.749Z

**tool call — Bash**
````
{
 "command": "grep -rn \"pdf_only_hidden_text\" app/backend/*.py | head -5 | cut -c1-300"
}
````

### User / tool · 2026-11-02T21:29:23.853Z

**tool result**
````
app/backend/pdf_checks.py:23:    "pdf_only_hidden_text": "Every piece of text in this PDF's text layer is hidden when the page is shown, or could not be checked, so nothing was read. "
app/backend/pdf_checks.py:131:        raise PdfError("pdf_only_hidden_text" if hidden_pages else "pdf_no_text_layer", detail)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:29:44.867Z

**tool call — Bash**
````
{
 "command": "T=$(cat /private/tmp/claude-501/zla-tok); curl -s -XPOST localhost:7911/api/cases/$T/review/batch -H 'content-type: application/json' -d '{\"action\":\"accept\",\"item_ids\":[\"e1\",\"e2\",\"e3\",\"e4\",\"e5\",\"e6\",\"e7\",\"e8\",\"e9\"]}' | head -c 300; echo; curl -s localhost:7911/api/cases/$T/export | .venv/bin/python -c \"\nimport sys,json; d=json.load(sys.stdin); print(list(d.keys())); print(json.dumps(d.get('provenance'))[:600]); print(json.dumps(d.get('excluded'))[:700]); print(d['letter_text'][:600]); print(json.dumps(d.get('warnings'))[:300])\"; curl -s localhost:7911/api/cases | head -c 1500"
}
````

### User / tool · 2026-11-02T21:29:45.049Z

**tool result**
````
{"items":[{"id":"e1","review_status":"accepted"},{"id":"e2","review_status":"accepted"},{"id":"e3","review_status":"accepted"},{"id":"e4","review_status":"accepted"},{"id":"e5","review_status":"accepted"},{"id":"e6","review_status":"accepted"},{"id":"e7","review_status":"accepted"},{"id":"e8","revie
['token', 'generated_at', 'letter_text', 'internal_notes_text', 'counts', 'items', 'warnings', 'totals', 'excluded', 'provenance']
{"generator_model": "hand-checked (qa)", "judge_model": "claude-haiku-5-5", "generator_prepared": true, "backend": "fixture", "recorded_from": "curated", "demo_mode": true, "prompt_versions": ["judge_amount_class_v1", "judge_conflict_v6", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
{"pending": 14, "edit_not_confirmed": 0, "dismissed": 0, "rejected": 0}
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

January 9, 2026 — Central ER discharge summary
Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
Source [Ex. __ / Bates __]: "D
[]
{"cases":[{"token":"mN7HPscbMblidUBI7k5U1Q","title":"Sample case","name":"Sample case","source":"sample","status":"ready","record_count":9,"created_at":"2026-11-02T21:28:16Z","updated_at":"2026-11-02T21:28:16Z","last_activity_at":"2026-11-02T21:29:44Z","run":{"stage":"finalize","steps_done":7,"steps_total":8,"running":false,"error":false},"progress":{"entries":{"decided":9,"total":9},"flags":{"decided":0,"total":10},"amounts":{"decided":0,"total":4}},"counts":{"pending":14,"accepted":9,"edited":0,"dismissed":0,"needs_review":3},"hitl":{"pending":14,"needs_review":3,"needs_review_open":3,"edits_to_check":0,"could_not_verify":0,"gate_blockers":[],"gate_warnings":[{"reason_code":"ITEMS_NOT_REVIEWED","count":14,"why":"14 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]},"export_ready":true,"next_action":{"item_id":"a2","kind":"amount","reason":"This figure is a rate, not a charge, so it is not added to the total."},"status_error":false,"status_error_message":null}]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:29:52.806Z

**tool call — Bash**
````
{
 "command": "T=$(cat /private/tmp/claude-501/zla-tok); curl -s localhost:7911/api/cases/$T/export | .venv/bin/python -c \"\nimport sys,json; d=json.load(sys.stdin); print(json.dumps(d['counts'])); print(json.dumps(d['totals'])[:400]); print(d['letter_text'][-500:]); print(d['internal_notes_text'][:300])\"; curl -s -XPUT localhost:7911/api/cases/$T/export_config -H 'content-type: application/json' -d '{\"exhibit\":\"4\",\"bates_prefix\":\"RIV\",\"bates_start\":1}'; curl -s -XPUT localhost:7911/api/cases/$T/export_config -H 'content-type: application/json' -d '{\"exhibit\":\"4$$$\"}'; curl -s -XDELETE localhost:7911/api/cases/$T/export_config"
}
````

### User / tool · 2026-11-02T21:29:52.979Z

**tool result**
````
{"entries": 9, "charges": 0, "flags_in_notes": 0, "records_in_letter": 9, "records_total": 9, "pending": 14, "pending_flags": 10}
{"charges_cents": 0, "charges_count": 0}
nerative change and to correlate clinically.
Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."

June 12, 2026 — Hill Country Pain Management, follow-up
Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 14.

FLAGS ACCEPTED
- none

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit t
{"exhibit":"4","bates_prefix":"RIV","bates_start":1}{"error":{"code":"invalid_edit","message":"Exhibit and prefix: up to 20 letters, digits, space . _ -; first number 0 to 99999999.","detail":{}}}{"exhibit":null,"bates_prefix":null,"bates_start":null}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:31:09.714Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/home.js",
 "content": "/* Your cases (/). T-181, D-068, spec section 3. Builder A.\n   Local mode: GET /api/cases lists every case. Public/demo mode: that route is 404 by design, so the list is the cases THIS BROWSER started (tokens kept in localStorage by G.cases,\n   try/catch), each read with GET /api/cases/{token}. One definition of the Next line and the Continue target (spec 3.2) for both sources.\n   Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, case-card (data-token, data-title), case-next, btn-continue, btn-rename, btn-delete, btn-delete-yes, btn-delete-keep,\n   rename-input, btn-rename-save, btn-rename-cancel, btn-remove-gone, find-case, cases-mode, page-error, btn-retry. Text only (textContent); no inline style attributes. */\n(function () {\n  const G = window.G, { h } = G;\n\n  /* ---- the cases this browser started (public mode). Shared with step1.js. Never throws: storage can be blocked. ---- */\n  const KEY = \"zl.guided.cases\";\n  G.cases = {\n    list() { try { const v = JSON.parse(localStorage.getItem(KEY) || \"[]\"); return Array.isArray(v) ? v.filter((t) => typeof t === \"string\") : []; } catch (_) { return []; } },\n    add(token) { try { const l = G.cases.list().filter((t) => t !== token); l.unshift(token); localStorage.setItem(KEY, JSON.stringify(l.slice(0, 100))); } catch (_) { /* not remembered */ } },\n    remove(token) { try { localStorage.setItem(KEY, JSON.stringify(G.cases.list().filter((t) => t !== token))); } catch (_) { /* not remembered */ } },\n  };\n\n  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + \"s\"}`;\n  const day = (iso) => { const d = new Date(iso); return isNaN(d) ? \"\" : d.toLocaleDateString(\"en-US\", { month: \"short\", day: \"numeric\" }); };\n  const track = [\"Add records\", \"Timeline\", \"Bills\", \"Letter\"];\n\n  /* ---- one view-model for a /api/cases row or a GET case JSON ---- */\n  function fromRow(c) {\n    const p = c.progress || {}, e = p.entries || { decided: 0, total: 0 }, f = p.flags || { decided: 0, total: 0 }, a = p.amounts || { decided: 0, total: 0 };\n    const run = c.run || {};\n    return { token: c.token, title: c.title || c.name || \"Case\", created: c.created_at, activity: c.last_activity_at || c.updated_at || c.created_at, records: c.record_count, status: c.status,\n      stage: run.steps_done != null ? Math.min(run.steps_done + 1, run.steps_total || 8) : null, stages: run.steps_total || 8,\n      err: !!c.status_error, errMsg: c.status_error_message || \"We couldn't load this case's status\",\n      s2: { total: e.total + f.total, left: e.total + f.total - e.decided - f.decided }, s3: { total: a.total, left: a.total - a.decided },\n      ready: !!c.export_ready, next: c.next_action, problems: c.hitl && c.hitl.gate_blockers ? c.hitl.gate_blockers.length : null, src: c };\n  }\n  function fromCase(c) {\n    const n = G.steps.counts(c);\n    return { token: c.token, title: G.titleOf(c), created: c.created_at, activity: c.updated_at || c.created_at, records: (c.records || []).length, status: c.status, stage: null, stages: 8,\n      err: false, errMsg: \"\", s2: n.step2, s3: n.step3, ready: !!(c.review && c.review.ready_to_export), next: c.next_action, problems: null, src: c };\n  }\n  const finished = (v) => v.status === \"ready\" && v.s2.left === 0 && v.s3.left === 0 && v.ready;\n\n  /* Spec 3.2: the Next line and where Continue goes */\n  function nextStep(v) {\n    const t = v.token;\n    if (v.err) return { text: null, to: G.url.records(t), btn: \"Open case\" };\n    if (v.status === \"ingested\") return { text: \"Draft the timeline.\", to: G.url.records(t) };\n    if (v.status === \"running\") return { text: \"Wait while the timeline is drafted\" + (v.stage ? ` (stage ${v.stage} of ${v.stages}).` : \".\"), to: G.url.records(t) };\n    if (v.status === \"failed\") return { text: \"Drafting stopped. Run it again.\", cls: \"warn\", to: G.url.records(t) };\n    if (v.s2.left > 0) return { text: `Check the timeline. ${v.s2.left} of ${plural(v.s2.total, \"item\")} left.`, to: G.url.timeline(t) };\n    if (v.s3.left > 0) return { text: `Check the bills. ${v.s3.left} of ${plural(v.s3.total, \"amount\")} left.`, to: G.url.bills(t) };\n    if (finished(v)) return { text: null, done: true, to: G.url.letter(t), btn: \"Open letter\" };\n    const na = v.next;\n    if (!v.ready && na && na.item_id && (na.kind === \"entry\" || na.kind === \"flag\" || na.kind === \"amount\"))\n      return { text: `Fix ${plural(v.problems || 1, \"problem\")} before the letter.`, reason: na.reason, cls: \"warn\", to: na.kind === \"amount\" ? G.url.bills(t, na.item_id) : G.url.timeline(t, na.item_id) };\n    return { text: \"Get your letter.\", to: G.url.letter(t) };\n  }\n  function trackStates(v) {\n    const st = G.steps.states(v.src, 0), done = finished(v);\n    const mine = st.map((s, i) => (i === 3 && done ? \"done\" : s.state === \"done\" ? \"done\" : s.state === \"attn\" ? \"attn\" : \"todo\"));\n    const cur = mine.findIndex((s) => s !== \"done\");\n    return mine.map((s, i) => (s === \"done\" ? \"done\" : s === \"attn\" ? \"attn\" : i === cur ? \"current\" : \"\"));\n  }\n\n  /* ---- one card ---- */\n  function card(v, hooks) {\n    if (v.gone) return goneCard(v, hooks);\n    const nx = nextStep(v);\n    const nextEl = v.err ? h(\"p\", { class: \"next warn\", \"data-testid\": \"case-next\" }, v.errMsg)\n      : nx.done ? h(\"p\", { class: \"next ok\", \"data-testid\": \"case-next\" }, h(\"b\", {}, \"Finished.\"), \" Your letter is ready.\")\n        : h(\"p\", { class: \"next \" + (nx.cls || \"\"), \"data-testid\": \"case-next\" }, h(\"b\", {}, \"Next:\"), \" \" + nx.text, nx.reason ? \" \" + nx.reason : \"\");\n    const states = trackStates(v);\n    const track$ = v.err ? h(\"div\", { class: \"cc-meta\" }, \"\") : h(\"ol\", { class: \"track\", \"aria-label\": \"Steps\" }, track.map((l, i) => h(\"li\", { class: states[i] }, h(\"i\", {}), l, h(\"span\", { class: \"sr\" }, ` (${states[i] === \"done\" ? \"done\" : states[i] === \"current\" ? \"now\" : states[i] === \"attn\" ? \"needs a look\" : \"later\"})`))));\n    const meta = h(\"div\", { class: \"cc-meta\", \"data-slot\": \"meta\" }, [v.created ? \"Started \" + day(v.created) : \"\", v.records != null ? plural(v.records, \"record\") : \"\"].filter(Boolean).join(\" · \"));\n    const metaText = meta.textContent;\n    const titleEl = h(\"h3\", { title: v.title }, v.title);\n    const renameBtn = h(\"button\", { type: \"button\", class: \"btn quiet\", \"data-testid\": \"btn-rename\" }, \"Rename\");\n    const top = h(\"div\", { class: \"cc-top\" }, titleEl, renameBtn);\n    const cont = h(\"a\", { class: \"btn lg \" + (nx.done ? \"go\" : \"primary\"), href: nx.to, \"data-testid\": \"btn-continue\" }, nx.btn || \"Continue\");\n    const del = h(\"button\", { type: \"button\", class: \"btn quiet danger\", \"data-testid\": \"btn-delete\" }, \"Delete\");\n    const row1 = h(\"div\", { class: \"cc-bottom\" }, cont, del);\n    const yes = h(\"button\", { type: \"button\", class: \"btn danger\", \"data-testid\": \"btn-delete-yes\" }, \"Yes, delete\");\n    const keep = h(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": \"btn-delete-keep\" }, \"Keep it\");\n    const row2 = h(\"div\", { class: \"cc-bottom\", hidden: true }, h(\"span\", { class: \"cc-ask\", role: \"alert\" }, \"Delete this case and all its answers?\"), yes, keep);\n    const el = h(\"article\", { class: \"ccard\", \"data-testid\": \"case-card\", \"data-token\": v.token, \"data-title\": v.title, \"data-finished\": finished(v) ? \"1\" : \"0\" }, top, meta, track$, nextEl, row1, row2);\n\n    del.addEventListener(\"click\", () => { hooks.editing(+1); row1.hidden = true; row2.hidden = false; keep.focus(); });\n    keep.addEventListener(\"click\", () => { hooks.editing(-1); row2.hidden = true; row1.hidden = false; del.focus(); });\n    yes.addEventListener(\"click\", async () => {\n      yes.disabled = true; keep.disabled = true;\n      try { await G.api.remove(v.token); G.cases.remove(v.token); hooks.editing(-1); hooks.removed(v.token); }\n      catch (e) { yes.disabled = false; keep.disabled = false; meta.textContent = e.message; meta.classList.add(\"bad\"); }\n    });\n    renameBtn.addEventListener(\"click\", () => {\n      hooks.editing(+1);\n      const input = h(\"input\", { type: \"text\", class: \"rename\", value: v.title, maxlength: \"120\", \"aria-label\": \"Case name\", \"data-testid\": \"rename-input\" });\n      const save = h(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": \"btn-rename-save\" }, \"Save\"), cancel = h(\"button\", { type: \"button\", class: \"btn quiet\", \"data-testid\": \"btn-rename-cancel\" }, \"Cancel\");\n      top.replaceChildren(input, save, cancel);\n      const close = (title) => { hooks.editing(-1); titleEl.textContent = title; titleEl.title = title; el.setAttribute(\"data-title\", title); v.title = title; top.replaceChildren(titleEl, renameBtn); meta.textContent = metaText; meta.classList.remove(\"bad\"); renameBtn.focus(); };\n      const doSave = async () => {\n        save.disabled = true;\n        try { const r = await G.api.rename(v.token, input.value); close(r.title || G.titleOf({ title: input.value })); }\n        catch (e) { save.disabled = false; meta.textContent = e.message; meta.classList.add(\"bad\"); input.focus(); }\n      };\n      save.addEventListener(\"click\", doSave); cancel.addEventListener(\"click\", () => close(v.title));\n      input.addEventListener(\"keydown\", (e) => { if (e.key === \"Enter\") { e.preventDefault(); doSave(); } else if (e.key === \"Escape\") { e.preventDefault(); close(v.title); } });\n      input.focus(); input.select();\n    });\n    return el;\n  }\n  function goneCard(v, hooks) {\n    const hrs = G.store.health && G.store.health.retention_hours;\n    const rm = h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-remove-gone\" }, \"Remove from this list\");\n    rm.addEventListener(\"click\", () => { G.cases.remove(v.token); hooks.removed(v.token); });\n    return h(\"article\", { class: \"ccard gone\", \"data-testid\": \"case-card\", \"data-token\": v.token, \"data-title\": \"\", \"data-finished\": \"0\" }, h(\"div\", { class: \"cc-top\" }, h(\"h3\", {}, \"A case that is gone\")),\n      h(\"div\", { class: \"cc-meta\" }, \"\"), h(\"p\", { class: \"next warn\", \"data-testid\": \"case-next\" }, \"This case is no longer here.\" + (hrs ? ` Cases are kept for ${hrs} hours.` : \"\")), h(\"span\", {}), h(\"div\", { class: \"cc-bottom\" }, rm));\n  }\n  const skeleton = () => h(\"article\", { class: \"ccard skeleton\", \"aria-hidden\": \"true\" }, h(\"div\", { class: \"skel sk-title\" }), h(\"div\", { class: \"skel sk-meta\" }), h(\"div\", { class: \"skel sk-track\" }), h(\"div\", { class: \"skel sk-next\" }), h(\"div\", { class: \"skel sk-btn\" }));\n\n  /* ---- data: local list, or this browser's tokens ---- */\n  async function load(signal) {\n    try { return { mode: \"local\", views: ((await G.api.cases(signal)).cases || []).map(fromRow) }; }\n    catch (e) {\n      if (e.name === \"AbortError\") throw e;\n      if (e.status !== 404) throw e;\n    }\n    const tokens = G.cases.list();\n    const got = await Promise.allSettled(tokens.map((t) => G.api.getCase(t, signal)));\n    if (signal && signal.aborted) throw new DOMException(\"aborted\", \"AbortError\");\n    return { mode: \"public\", views: got.map((r, i) => r.status === \"fulfilled\" ? fromCase(r.value) : (r.reason && r.reason.status === 404 ? { token: tokens[i], gone: true, activity: \"\" }\n      : { token: tokens[i], title: \"Case\", err: true, errMsg: \"We couldn't load this case's status\", status: \"failed\", s2: { total: 0, left: 0 }, s3: { total: 0, left: 0 }, src: {}, activity: \"\" })) };\n  }\n\n  G.pages.home = async function (ctx) {\n    const sampleOk = () => !G.store.health || G.store.health.sample_available !== false;\n    const head = (...extra) => h(\"div\", { class: \"home-h\" }, h(\"div\", { class: \"hh-main\" }, h(\"h1\", { \"data-testid\": \"page-title\", tabindex: \"-1\" }, \"Your cases\"), h(\"p\", {}, \"Each case goes through 4 steps. Pick up where you left off.\")), ...extra);\n    const newBtn = () => h(\"a\", { class: \"btn primary lg\", href: G.url.new(), \"data-testid\": \"btn-new-case\" }, \"+ Start a new case\");\n    const main = h(\"main\", { class: \"wrap wide\", id: \"main\" }, head(newBtn()),\n      h(\"p\", { class: \"sr\", role: \"status\" }, \"Loading your cases\"), h(\"h2\", { class: \"sec-h\" }, \"Loading your cases…\"), h(\"div\", { class: \"cases\", \"data-testid\": \"cases-loading\" }, skeleton(), skeleton(), skeleton()));\n    ctx.view.append(main);\n\n    let data, timer = null, editing = 0, last = \"\";\n    const sig = ctx.signal;\n    try { data = await load(sig); }\n    catch (e) {\n      if (e.name === \"AbortError\") return;\n      main.replaceChildren(head(), h(\"div\", { class: \"panel empty\", role: \"alert\", \"data-testid\": \"page-error\" }, h(\"div\", { class: \"em-ic bad\", \"aria-hidden\": \"true\" }, \"!\"), h(\"h2\", {}, \"We couldn't load your cases.\"),\n        h(\"p\", {}, e.message), h(\"div\", { class: \"row-actions\" }, h(\"button\", { type: \"button\", class: \"btn primary lg\", \"data-testid\": \"btn-retry\", \"data-autofocus\": \"\", onclick: () => ctx.go(\"/\", { replace: true }) }, \"Try again\"))));\n      return;\n    }\n\n    const lists = h(\"div\", { class: \"lists\" });\n    const searchBox = h(\"div\", { class: \"find\", hidden: true }, h(\"label\", { class: \"sr\", for: \"find-case\" }, \"Find a case\"), h(\"input\", { id: \"find-case\", type: \"search\", placeholder: \"Find a case by name\", \"data-testid\": \"find-case\", autocomplete: \"off\" }));\n    const finput = searchBox.querySelector(\"input\");\n    const hooks = { editing: (n) => { editing = Math.max(0, editing + n); }, removed: (t) => { data.views = data.views.filter((v) => v.token !== t); last = \"\"; draw(true); } };\n\n    function applyFilter() {\n      const q = finput.value.trim().toLowerCase();\n      lists.querySelectorAll(\"[data-testid=case-card]\").forEach((c) => { c.hidden = !!q && !(c.getAttribute(\"data-title\") || \"\").toLowerCase().includes(q); });\n      lists.querySelectorAll(\"section\").forEach((s) => { const n = s.querySelectorAll(\"[data-testid=case-card]:not([hidden])\").length; s.querySelector(\".c\").textContent = String(n); });\n    }\n    function draw(force) {\n      const sig = JSON.stringify(data.views.map((v) => [v.token, v.title, v.status, v.stage, v.s2, v.s3, v.ready, v.gone, v.err, v.next]));\n      if (!force && sig === last) return; last = sig;\n      const views = data.views.slice().sort((a, b) => String(b.activity || \"\").localeCompare(String(a.activity || \"\")));\n      const active = views.filter((v) => !finished(v)), done = views.filter(finished);\n      searchBox.hidden = views.length < 6;\n      if (!views.length) {\n        lists.replaceChildren(h(\"div\", { class: \"panel empty\", \"data-testid\": \"cases-empty\" }, h(\"div\", { class: \"em-ic\", \"aria-hidden\": \"true\" }, \"+\"), h(\"h2\", {}, \"You don't have any cases yet.\"),\n          h(\"p\", {}, \"A case is one client's medical records. We'll guide you through 4 steps: add the records, check the timeline, check the bills, and get your letter.\"),\n          h(\"div\", { class: \"row-actions\" }, newBtn(), sampleOk() ? h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-sample-case\", onclick: openSample }, \"Open the sample case\") : null),\n          h(\"p\", { class: \"err-slot\", role: \"alert\", \"data-testid\": \"sample-error\" })));\n        return;\n      }\n      const sec = (label, items, testid) => items.length ? h(\"section\", { \"aria-label\": label }, h(\"h2\", { class: \"sec-h\" }, label, \" \", h(\"span\", { class: \"c\" }, String(items.length))),\n        h(\"div\", { class: \"cases\", \"data-testid\": testid }, items.map((v) => card(v, hooks)))) : null;\n      lists.replaceChildren(sec(\"In progress\", active, \"cases-list\"), sec(\"Finished\", done, \"cases-finished\"));\n      applyFilter();\n    }\n    async function openSample(ev) {\n      const btn = ev.currentTarget, slot = lists.querySelector(\"[data-testid=sample-error]\"); btn.disabled = true; btn.textContent = \"Opening…\"; slot.textContent = \"\";\n      try { const r = await G.api.createCase({ sample: true }); G.cases.add(r.token); ctx.go(G.url.records(r.token)); }\n      catch (e) { btn.disabled = false; btn.textContent = \"Open the sample case\"; slot.textContent = e.message; }\n    }\n    finput.addEventListener(\"input\", applyFilter);\n\n    main.replaceChildren(head(data.views.length ? newBtn() : null),\n      data.mode === \"public\" ? h(\"p\", { class: \"muted\", \"data-testid\": \"cases-mode\" }, \"These are the cases started in this browser. Keep the case link to open it elsewhere.\") : null, searchBox, lists);\n    draw(true);\n\n    /* a case that is being drafted shows its stage; follow it without moving anything (only text inside the cards changes) */\n    async function tick() {\n      timer = null;\n      if (!sig.aborted && data.views.some((v) => v.status === \"running\" || v.status === \"ingested\" && false)) {\n        if (!editing) { try { const d = await load(sig); if (!sig.aborted && !editing) { data = d; draw(false); } } catch (e) { /* keep what is on screen */ } }\n        if (!sig.aborted) timer = setTimeout(tick, 2000);\n      }\n    }\n    if (data.views.some((v) => v.status === \"running\")) timer = setTimeout(tick, 2000);\n    return () => { if (timer) clearTimeout(timer); };\n  };\n})();\n"
}
````

### User / tool · 2026-11-02T21:31:09.778Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/guided/home.js has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:31:16.930Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\np='home.js'; s=open(p).read()\ns=s.replace('data.views.some((v) => v.status === \"running\" || v.status === \"ingested\" && false)','data.views.some((v) => v.status === \"running\")')\nopen(p,'w').write(s)\nE\ncat > home.css <<'E'\n/* home: rules for this module only (T-181 Builder A). Shell tokens and base classes live in styles.css. */\n.home-h .hh-main { flex: 1; min-width: 0; }\n.home-h h1:focus { outline: none; }\n.ccard { min-height: 244px; }\n.ccard .cc-meta.bad { color: var(--bad); font-weight: 600; }\n.ccard .cc-top input.rename { flex: 1; min-width: 0; height: 40px; border-radius: 10px; border: 2px solid var(--accent); background: var(--panel); color: var(--text); font: 650 1.0625rem var(--font); padding: 0 12px; }\n.ccard .cc-top .btn { height: 40px; }\n.ccard .cc-ask { flex: 1; font-weight: 600; min-width: 0; }\n.ccard .next.warn { font-weight: 600; }\n.ccard.skeleton { min-height: 244px; }\n.ccard.skeleton .sk-title { height: 28px; width: 60%; }\n.ccard.skeleton .sk-meta { height: 18px; width: 40%; }\n.ccard.skeleton .sk-track { height: 24px; }\n.ccard.skeleton .sk-next { height: 44px; }\n.ccard.skeleton .sk-btn { height: 56px; }\n.ccard.gone { background: var(--sunken); }\n.ccard.gone .cc-bottom .btn { flex: 1; }\n.empty .em-ic.bad { background: var(--bad-bg); color: var(--bad); }\n.empty .err-slot { min-height: 28px; }\n.lists section + section { margin-top: 8px; }\n@media (max-width: 760px) {\n  .home-h .btn { width: 100%; }\n  .ccard .cc-bottom { flex-wrap: wrap; }\n  .ccard .cc-ask { flex-basis: 100%; }\n}\nE"
}
````

### User / tool · 2026-11-02T21:31:17.049Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:31:47.253Z

**tool call — Bash**
````
{
 "command": "grep -rn \"\\\"records\\\"\" app/backend/pipeline.py | head; grep -n \"run_partial\" app/backend/*.py | head -8 | cut -c1-260; grep -n \"injection\" memory/contracts/api.md | head -5 | cut -c1-400"
}
````

### User / tool · 2026-11-02T21:31:47.357Z

**tool result**
````
app/backend/pipeline.py:54:    recs = language.annotate(ing["records"])           # D-042: en | es | other per record; raises UnsupportedLanguage when no record is readable
app/backend/pipeline.py:98:    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "split_detail": ing.get("split_detail"), "banner": ing["banner"],
app/backend/pipeline.py:149:    marks = {"unsplit_records": [r["id"] for r in ing["records"] if r.get("unsplit")], "preamble_records": [r["id"] for r in ing["records"] if r.get("preamble")]}
app/backend/pipeline.py:190:    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
app/backend/pipeline.py:192:    new_spans = {r["id"]: (r["char_start"], r["char_end"]) for r in ing["records"]}
app/backend/pipeline.py:197:        for r in ing["records"]:
app/backend/pipeline.py:405:    _store_run_checks(conn, cid, ing["records"], "pending")
app/backend/pipeline.py:415:    by_n = {r["n"]: r for r in ing["records"]}
app/backend/pipeline.py:477:        err["records"] = list(records)
app/backend/pipeline.py:497:    left = [n for n in err["records"] if f"r{n}" not in hand]
app/backend/pipeline.py:455:    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
app/backend/pipeline.py:475:    err = {"code": "run_partial", "message": WHY.to_prepared(msg) if AU.answers_prepared() else msg} if parts else None      # D-065: on the curated set no AI step ran
app/backend/pipeline.py:494:    if case["status"] != "failed" or not err or err.get("code") != "run_partial" or not err.get("extract_only"):
app/backend/store.py:37:    """Mark a case left `running` as failed with the honest `run_partial` message (T-146: the case reads failed, a re-run is allowed, nothing item-level is touched, so accepted
app/backend/store.py:44:                   error=json.dumps({"code": "run_partial", "interrupted": True, "message": INTERRUPTED_MESSAGE}))
73:      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false,
148:      "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
181:        "code_checks": {"amount_in_text": true, "classified_by": "rule:charge_label", "injection_tag": false, "highlight_found": true},
191:        "code_checks": {"amount_in_text": true, "classified_by": "rule:per_unit", "injection_tag": false, "highlight_found": true},
241:        "code_checks": {"excerpt_verbatim": true, "lexicon_hit": "patient_report", "highlight_found": true, "injection_tag": false},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:31:50.238Z

**tool call — Bash**
````
{
 "command": "T=$(cat /private/tmp/claude-501/zla-tok); curl -s localhost:7911/api/cases/$T | .venv/bin/python -c \"\nimport sys,json; d=json.load(sys.stdin); print(json.dumps(d['injection'])[:300], json.dumps(d['warnings'])[:300], d['error'])\"; grep -n \"injection\" -i app/backend/present.py | head -5 | cut -c1-240"
}
````

### User / tool · 2026-11-02T21:31:50.370Z

**tool result**
````
{"records": [], "banner": null} [] None
85:                          records, row["kind"], injection=bool(rec and rec.get("injection_tag")), demoted=demoted)
393:         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
483:    injected = [r["id"] for r in recs if r["injection_tag"]]
490:            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:33:19.831Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/step1.js",
 "content": "/* Step 1: Add records. T-181, D-068, spec section 4. Builder A.\n   /new (before the case exists): name, how to add (paste / upload / sample / test case), Read the records. /case/<token>/records: records found, drafting, done, stopped.\n   The primary action lives in a sticky action bar (G.sbar, also used by step 4), so it is on screen at 1440x900 and 390x844 without scrolling (T-180 review, major 1).\n   Test ids: input-name, name-error, tile-paste, tile-file, tile-sample, tile-library, input-text, file-input, btn-choose-file, library-<id>, btn-read, btn-draft, btn-start-over, bar-msg, action-bar,\n   btn-use-sample, btn-retry-read, btn-ocr, btn-hidden-anyway, check-hidden, records-list, records-notes, stage-list (li data-stage), draft-bar, draft-done, btn-next-step, draft-failed, btn-run-again, btn-run-yes, btn-run-cancel,\n   prepared-badge, demo-note. Text only (textContent); no inline style attributes. */\n(function () {\n  const G = window.G, { h } = G;\n  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + \"s\"}`;\n  const longDate = (iso) => { const d = /^\\d{4}-\\d{2}-\\d{2}$/.test(iso || \"\") ? new Date(iso + \"T00:00:00\") : null; return d && !isNaN(d) ? d.toLocaleDateString(\"en-US\", { month: \"long\", day: \"numeric\", year: \"numeric\" }) : null; };\n  const nice = (name) => { const s = String(name || \"\").replace(/^case[ _]?lib\\d+[ _]/i, \"\").replace(/[_-]+/g, \" \").trim(); return s ? s[0].toUpperCase() + s.slice(1) : \"Test case\"; };\n\n  /* ---- the sticky action bar (shared with step 4): one instruction/error line, the primary button, and a slot for follow-up buttons that never moves the primary ---- */\n  G.sbar = function (msgText, primary, ...alts) {\n    const msg = h(\"p\", { class: \"sbar-msg\", \"aria-live\": \"polite\", \"data-testid\": \"bar-msg\" }, msgText);\n    const slot = h(\"span\", { class: \"sbar-alt\" }, ...alts);\n    const el = h(\"div\", { class: \"sbar\", \"data-testid\": \"action-bar\" }, h(\"div\", { class: \"sbar-in\" }, msg, h(\"div\", { class: \"sbar-btns\" }, primary, slot)));\n    return { el, slot, say(text, kind) { msg.textContent = text; msg.className = \"sbar-msg\" + (kind ? \" \" + kind : \"\"); }, alts(...a) { slot.replaceChildren(...a); } };\n  };\n  G.longDate = longDate;\n\n  /* ---------------------------------------------------------------- /new */\n  G.pages.new = async function (ctx) {\n    let hl = G.store.health;\n    if (!hl) { try { hl = await G.api.health(ctx.signal); G.store.health = hl; } catch (e) { if (e.name === \"AbortError\") return; hl = {}; } }\n    const demo = !!hl.demo_mode, lim = hl.limits || { max_chars: 60000, max_records: 40 }, sampleOk = hl.sample_available !== false;\n    let lib = null;\n    try { lib = ((await G.api.call(\"GET\", \"/library\", null, ctx.signal)).cases || []).map((x) => ({ id: x.id, name: nice(x.name) })); } catch (e) { if (e.name === \"AbortError\") return; lib = null; }\n    if (lib && !lib.length) lib = null;\n    const st = { how: demo ? (sampleOk ? \"sample\" : lib ? \"library\" : \"sample\") : \"paste\", text: \"\", file: null, lib: null, reading: false, again: null };\n\n    /* name */\n    const nameInput = h(\"input\", { id: \"case-name\", type: \"text\", maxlength: \"120\", autocomplete: \"off\", \"data-testid\": \"input-name\", \"aria-describedby\": \"name-hint name-error\" });\n    const nameErr = h(\"span\", { class: \"hint bad\", id: \"name-error\", role: \"alert\", \"data-testid\": \"name-error\" });\n    nameInput.addEventListener(\"input\", () => { nameErr.textContent = \"\"; });\n\n    /* tiles */\n    const tiles = [\n      { key: \"paste\", head: \"Paste text\", sub: \"Copy the records and paste them here.\", off: demo },\n      { key: \"file\", head: \"Upload a file\", sub: \"A .txt or .pdf file, up to 5 MB.\", off: demo },\n      sampleOk ? { key: \"sample\", head: \"Use the sample case\", sub: \"A short synthetic case to try it out.\" } : null,\n      lib ? { key: \"library\", head: \"Choose a test case\", sub: \"One of our made-up cases, ready to read.\" } : null,\n    ].filter(Boolean);\n    const tileEls = tiles.map((t) => {\n      const input = h(\"input\", { type: \"radio\", name: \"how\", value: t.key, disabled: t.off, \"data-testid\": \"radio-\" + t.key });\n      if (st.how === t.key) input.checked = true;\n      input.addEventListener(\"change\", () => { st.how = t.key; clearMsg(); drawBox(); sync(); });\n      return h(\"label\", { class: \"tile\" + (t.off ? \" off\" : \"\"), \"aria-disabled\": t.off ? \"true\" : null, \"data-testid\": \"tile-\" + t.key }, input, h(\"span\", { class: \"tl-h\" }, t.head), h(\"p\", {}, t.sub), t.off ? h(\"p\", { class: \"tile-why\" }, \"Not available in this demo.\") : null);\n    });\n\n    /* the one input box: fixed height, shows what was chosen */\n    const box = h(\"div\", { class: \"input-box solid\", \"data-testid\": \"input-box\" });\n    const fileInput = h(\"input\", { type: \"file\", class: \"sr-file\", accept: \".txt,.pdf,text/plain,application/pdf\", \"data-testid\": \"file-input\", tabindex: \"-1\", \"aria-hidden\": \"true\" });\n    fileInput.addEventListener(\"change\", () => { setFile(fileInput.files && fileInput.files[0]); fileInput.value = \"\"; });\n    function setFile(f) {\n      clearMsg(); st.file = null; if (!f) { drawBox(); sync(); return; }\n      const ext = (f.name.split(\".\").pop() || \"\").toLowerCase();\n      if (ext !== \"txt\" && ext !== \"pdf\") fail({ msg: \"We can read .txt and .pdf files. Choose another file.\" });\n      else if (f.size > 5 * 1024 * 1024) fail({ msg: \"That file is bigger than 5 MB. Choose a smaller one.\" });\n      else st.file = f;\n      drawBox(); sync();\n    }\n    function drawBox() {\n      if (st.how === \"paste\") {\n        const ta = h(\"textarea\", { \"aria-label\": \"Paste the records here\", placeholder: \"Paste the records here\", \"data-testid\": \"input-text\", spellcheck: \"false\" }); ta.value = st.text;\n        ta.addEventListener(\"input\", () => { st.text = ta.value; clearMsg(); sync(); });\n        box.className = \"input-box solid\"; box.replaceChildren(h(\"div\", { class: \"box-col\" }, ta, h(\"p\", { class: \"hint\" }, `Up to ${lim.max_chars.toLocaleString(\"en-US\")} characters or ${lim.max_records} records.`)));\n      } else if (st.how === \"file\") {\n        const choose = h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-choose-file\", onclick: () => fileInput.click() }, st.file ? \"Choose another file\" : \"Choose a file\");\n        box.className = \"input-box\" + (st.file ? \" solid\" : \"\");\n        box.replaceChildren(h(\"div\", { class: \"box-col center\" }, st.file ? [h(\"b\", { class: \"big-name\", \"data-testid\": \"file-name\" }, st.file.name), h(\"span\", { class: \"muted\" }, `${(st.file.size / 1024).toFixed(0)} KB`)]\n          : [h(\"b\", {}, \"Drop a .txt or .pdf file here\"), h(\"span\", { class: \"muted\" }, \"or\")], choose));\n      } else if (st.how === \"library\") {\n        box.className = \"input-box solid\";\n        box.replaceChildren(h(\"fieldset\", { class: \"libs\" }, h(\"legend\", { class: \"sr\" }, \"Choose a test case\"), lib.map((x) => {\n          const r = h(\"input\", { type: \"radio\", name: \"lib\", value: x.id, \"data-testid\": \"library-\" + x.id }); if (st.lib === x.id) r.checked = true;\n          r.addEventListener(\"change\", () => { st.lib = x.id; clearMsg(); sync(); });\n          return h(\"label\", { class: \"lib-row\" }, r, h(\"span\", {}, x.name));\n        })));\n      } else {\n        box.className = \"input-box solid\";\n        box.replaceChildren(h(\"div\", { class: \"box-col center\" }, h(\"b\", { class: \"big-name\" }, \"The sample case\"), h(\"span\", { class: \"muted\" }, \"9 short records from a made-up car-accident case. Every name and date in it is invented.\")));\n      }\n    }\n    [\"dragover\", \"dragenter\"].forEach((ev) => box.addEventListener(ev, (e) => { if (st.how === \"file\") { e.preventDefault(); box.classList.add(\"over\"); } }));\n    box.addEventListener(\"dragleave\", () => box.classList.remove(\"over\"));\n    box.addEventListener(\"drop\", (e) => { if (st.how !== \"file\") return; e.preventDefault(); box.classList.remove(\"over\"); setFile(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]); });\n\n    /* the action bar */\n    const read = h(\"button\", { type: \"button\", class: \"btn primary lg sbar-main\", \"data-testid\": \"btn-read\", \"data-autofocus\": \"\" }, \"Read the records\");\n    const bar = G.sbar(\"\", read);\n    const hint = () => st.how === \"paste\" ? \"Paste the records, then press Read the records.\" : st.how === \"file\" ? \"Choose a file, then press Read the records.\" : st.how === \"library\" ? \"Pick a test case, then press Read the records.\" : \"Press Read the records to open the sample case.\";\n    function canRead() { return !st.reading && (st.how === \"sample\" || (st.how === \"paste\" && st.text.trim() !== \"\") || (st.how === \"file\" && !!st.file) || (st.how === \"library\" && !!st.lib)); }\n    function sync() { read.disabled = !canRead(); read.textContent = st.reading ? \"Reading…\" : \"Read the records\"; if (!bar.err) bar.say(hint()); }\n    function clearMsg() { bar.err = false; bar.alts(); bar.say(hint()); }\n    function fail(f) {\n      bar.err = true; bar.say(f.msg, \"bad\");\n      bar.alts(...(f.alts || []).map((a) => a.node || h(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": a.id, onclick: a.fn }, a.label)));\n    }\n\n    function plain(e, pdf) {\n      const reason = e.detail && e.detail.reason, code = e.code, s = e.status;\n      const again = { id: \"btn-retry-read\", label: \"Try again\", fn: () => submit(st.again || {}) };\n      if (s === 0 || s >= 500) return { msg: \"We couldn't reach the server. Your text is still here.\", alts: [again] };\n      if (s === 422 && code === \"invalid_title\") return { field: e.message };\n      if (s === 413) return { msg: pdf ? \"That file is bigger than 5 MB. Choose a smaller one.\" : `That's more than we can read at once (${lim.max_chars.toLocaleString(\"en-US\")} characters or ${lim.max_records} records). Split it into two cases.` };\n      if (s === 409 && code === \"demo_mode_unsupported_input\") return { msg: \"This demo can only read the sample and our test cases.\", alts: sampleOk ? [{ id: \"btn-use-sample\", label: \"Use the sample case\", fn: () => { st.how = \"sample\"; setRadio(); drawBox(); clearMsg(); sync(); } }] : [] };\n      if (s === 429) return { msg: reason === \"demo_full\" || reason === \"demo_busy\" ? e.message : \"We're reading other files right now. Try again in a moment.\", alts: [again] };\n      if (reason === \"pdf_no_text_layer\") {\n        const ocr = e.detail && e.detail.ocr && e.detail.ocr.status && e.detail.ocr.status.available;\n        return { msg: \"This PDF looks scanned, so it has no text we can read.\", alts: ocr ? [{ id: \"btn-ocr\", label: \"Read the scanned pages\", fn: () => submit({ ocr: true }) }] : [] };\n      }\n      if (reason === \"pdf_only_hidden_text\") {\n        const ok = h(\"input\", { type: \"checkbox\", \"data-testid\": \"check-hidden\" }), go = h(\"button\", { type: \"button\", class: \"btn\", disabled: true, \"data-testid\": \"btn-hidden-anyway\", onclick: () => submit({ includeHidden: \"all\" }) }, \"Use these pages anyway\");\n        ok.addEventListener(\"change\", () => { go.disabled = !ok.checked; });\n        return { msg: \"Everything on these pages is hidden text, so we kept it out.\", alts: [{ node: h(\"label\", { class: \"check inline\" }, ok, \"I looked at these pages myself\") }, { node: go }] };\n      }\n      if (reason && /^pdf_|^ocr_/.test(reason)) return { msg: e.message, alts: [{ id: \"btn-choose-other\", label: \"Choose another file\", fn: () => { st.how = \"file\"; setRadio(); drawBox(); clearMsg(); sync(); fileInput.click(); } }] };\n      if (s === 400 && /empty/i.test(e.message)) return { msg: \"There's nothing to read yet. Paste the records or choose a file.\" };\n      return { msg: e.message };\n    }\n    function setRadio() { tileEls.forEach((t) => { const r = t.querySelector(\"input\"); r.checked = r.value === st.how; }); }\n\n    async function postPdf(file, title, extra) {\n      const q = new URLSearchParams(); if (title) q.set(\"title\", title); if (extra.ocr) q.set(\"ocr\", \"true\"); if (extra.includeHidden) q.set(\"include_hidden\", extra.includeHidden);\n      let res, data = null;\n      try { res = await fetch(\"/api/cases/pdf\" + (q.toString() ? \"?\" + q : \"\"), { method: \"POST\", headers: { \"Content-Type\": \"application/pdf\" }, body: file, signal: ctx.signal }); }\n      catch (e) { if (e && e.name === \"AbortError\") throw e; throw new G.ApiError(0, null); }\n      try { data = await res.json(); } catch (_) { data = null; }\n      if (res.status >= 400) throw new G.ApiError(res.status, data && data.error);\n      return data;\n    }\n    async function submit(extra) {\n      if (st.reading) return; st.again = extra || {}; st.reading = true; clearMsg(); nameErr.textContent = \"\"; sync();\n      const title = nameInput.value.trim(), pdf = st.how === \"file\" && st.file && /\\.pdf$/i.test(st.file.name);\n      try {\n        let r;\n        if (st.how === \"paste\") r = await G.api.createCase({ text: st.text, ...(title ? { title } : {}) });\n        else if (st.how === \"sample\") r = await G.api.createCase({ sample: true, ...(title ? { title } : {}) });\n        else if (st.how === \"library\") r = await G.api.createCase({ library: st.lib, ...(title ? { title } : {}) });\n        else if (pdf) r = await postPdf(st.file, title, extra || {});\n        else r = await G.api.createCase({ text: await st.file.text(), ...(title ? { title } : {}) });\n        G.cases.add(r.token); ctx.go(G.url.records(r.token));\n      } catch (e) {\n        if (e && e.name === \"AbortError\") return;\n        st.reading = false; const f = plain(e, pdf);\n        if (f.field) { nameErr.textContent = f.field; nameInput.focus(); bar.err = true; bar.say(\"Fix the case name, then press Read the records.\", \"bad\"); }\n        else fail(f);\n        sync();\n      }\n    }\n    read.addEventListener(\"click\", () => submit({}));\n\n    drawBox();\n    const main = h(\"main\", { class: \"wrap\", id: \"main\" },\n      h(\"div\", { class: \"page-h\" }, h(\"div\", { class: \"ph-main\" }, h(\"div\", { class: \"eyebrow\" }, \"Step 1 of 4\"), h(\"h1\", { \"data-testid\": \"page-title\", tabindex: \"-1\" }, \"Add records\"),\n        h(\"p\", {}, \"Add the medical records for this case. We'll read them and draft a timeline for you to check.\"))),\n      h(\"div\", { class: \"panel\" },\n        demo ? h(\"div\", { class: \"note-box demo-note\", \"data-testid\": \"demo-note\" }, h(\"span\", { class: \"nb-text\" }, \"This demo can only read the sample case and our test cases.\", h(\"span\", {}, \"Pasting your own records or uploading a file isn't available here.\"))) : null,\n        h(\"div\", { class: \"field\" }, h(\"label\", { for: \"case-name\" }, \"Name this case (optional)\"), nameInput, h(\"span\", { class: \"hint\", id: \"name-hint\" }, \"For example the client's name. You can change it later.\"), nameErr),\n        h(\"fieldset\", { class: \"how\" }, h(\"legend\", { class: \"sr\" }, \"How do you want to add the records?\"), h(\"div\", { class: \"tiles\" + (tiles.length > 3 ? \" four\" : \"\") }, tileEls)),\n        box, fileInput));\n    ctx.view.append(main, bar.el);\n    sync();\n  };\n\n  /* ---------------------------------------------------------------- /case/<token>/records */\n  const STAGES = [[\"ingest\", \"Reading the records\"], [\"extract\", \"Writing one line for each record\", \"Getting the line our team prepared for each record\"], [\"verify\", \"Checking every line word for word against the record\"],\n    [\"judge_entries\", \"A second AI check of each line\"], [\"amounts\", \"Finding the bill amounts\"], [\"conflicts\", \"Comparing the records with each other\"],\n    [\"flags\", \"Looking for things the attorney should know\"], [\"finalize\", \"Putting it all together\"]];\n\n  G.pages.records = async function (ctx) {\n    const token = ctx.token; let c = ctx.case, dead = false, timer = null, bar = null;\n    G.cases.add(token);\n    ctx.view.addEventListener && null;\n    const prepared = () => G.provenance().kind === \"prepared\";\n    const counts = () => { const n = G.steps.counts(c); return { lines: n.step2.total, bills: n.step3.total }; };\n    const nextTarget = () => { const n = counts(); return n.lines > 0 ? [\"Go to step 2: Check the timeline\", G.url.timeline(token)] : n.bills > 0 ? [\"Go to step 3: Check the bills\", G.url.bills(token)] : [\"Go to step 4: Get your letter\", G.url.letter(token)]; };\n    const main = h(\"main\", { class: \"wrap\", id: \"main\" });\n    ctx.view.append(main);\n    const put = (newBar, ...kids) => { main.replaceChildren(...kids.filter(Boolean)); if (bar) bar.el.remove(); bar = newBar; if (bar) ctx.view.append(bar.el); };\n    const heading = (title, sub) => h(\"div\", { class: \"page-h\" }, h(\"div\", { class: \"ph-main\" }, h(\"div\", { class: \"eyebrow\" }, \"Step 1 of 4\"), h(\"h1\", { \"data-testid\": \"page-title\", tabindex: \"-1\" }, title), sub ? h(\"p\", {}, sub) : null));\n    const focusTitle = () => { const t = main.querySelector(\"h1\"); if (t) t.focus({ preventScroll: true }); };\n\n    const recList = (id) => h(\"ol\", { class: \"list\", \"data-testid\": id || \"records-list\" }, (c.records || []).map((r) => {\n      const d = longDate(r.date_iso); return h(\"li\", {}, h(\"span\", { class: \"n\" }, String(r.seq)), h(\"span\", { class: \"num\" + (d ? \"\" : \" muted\") }, d || \"Date unclear\"), h(\"span\", { class: \"src\" }, r.source_label || \"Record \" + r.seq));\n    }));\n    function notes() {\n      const out = [], w = new Set((c.warnings || []).map((x) => x.code)), n = (c.dates_to_confirm || []).length;\n      if (n) out.push(h(\"div\", { class: \"note-box\" }, h(\"span\", { class: \"nb-text\" }, `${n === 1 ? \"1 record has a date\" : n + \" records have dates\"} we need you to check. You'll do that in step 2.`)));\n      if (w.has(\"PHI_PATTERN\")) out.push(h(\"div\", { class: \"note-box bad\" }, h(\"span\", { class: \"nb-text\" }, \"Some text looks like real personal details (a phone, SSN or record number). Only use synthetic records.\")));\n      if (w.has(\"SPLIT_AMBIGUOUS\") || w.has(\"UNSPLIT_TEXT\")) out.push(h(\"div\", { class: \"note-box\" }, h(\"span\", { class: \"nb-text\" }, \"Some text didn't look like a record. We kept it as its own record so nothing is lost.\")));\n      if (c.injection && c.injection.banner) out.push(h(\"div\", { class: \"note-box bad\" }, h(\"span\", { class: \"nb-text\" }, c.injection.banner)));\n      if (!n && (c.records || []).length && c.records.every((r) => r.date_status === \"parsed\")) out.push(h(\"div\", { class: \"note-box ok\" }, h(\"span\", { class: \"nb-text\" }, \"Every record has a date we could read.\")));\n      return h(\"div\", { class: \"notes\", \"data-testid\": \"records-notes\" }, out);\n    }\n\n    /* ---- records found ---- */\n    function drawFound() {\n      ctx.layout(\"page\"); ctx.setStepStatus(1, \"Not started\", \"todo\");\n      const msg = h(\"span\", {}, \"Next, we'll draft one timeline line for each record.\");\n      const draft = h(\"button\", { type: \"button\", class: \"btn primary lg sbar-main\", \"data-testid\": \"btn-draft\", \"data-autofocus\": \"\" }, \"Draft the timeline\");\n      const over = h(\"a\", { class: \"btn quiet\", href: G.url.new(), \"data-testid\": \"btn-start-over\" }, \"Start over with other records\");\n      const b = G.sbar(\"\", draft, over); b.say(msg.textContent);\n      draft.addEventListener(\"click\", () => run(false, draft, b));\n      put(b, heading(`We found ${plural((c.records || []).length, \"record\")}`, \"Check that these are the records you meant to add. Next, we'll draft a one-line timeline entry for each one.\"),\n        h(\"div\", { class: \"panel\" }, notes(), recList()));\n    }\n    async function run(confirm, btn, b) {\n      btn.disabled = true; const label = btn.textContent; btn.textContent = \"Starting…\";\n      try { await G.api.run(token, confirm); }\n      catch (e) {\n        if (e.code === \"run_in_progress\") { /* already going: show it */ }\n        else if (e.status === 409 && e.code === \"needs_confirm\") { btn.disabled = false; btn.textContent = label; return askRerun(b); }\n        else { btn.disabled = false; btn.textContent = label; b.say(e.code === \"demo_mode_unsupported_input\" ? \"This demo can only read the sample and our test cases.\" : e.message, \"bad\"); return; }\n      }\n      c = { ...c, status: \"running\" }; drawRunning(); poll();\n    }\n    function askRerun(b) {\n      b.say(\"Run it again? Your answers so far are kept.\", \"bad\");\n      const yes = h(\"button\", { type: \"button\", class: \"btn primary\", \"data-testid\": \"btn-run-yes\", onclick: () => run(true, yes, b) }, \"Yes, run it again\"), no = h(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": \"btn-run-cancel\", onclick: () => { b.say(\"\"); b.alts(); } }, \"Cancel\");\n      b.alts(yes, no); yes.focus();\n    }\n\n    /* ---- drafting ---- */\n    let live = null;\n    function drawRunning() {\n      ctx.layout(\"page\");\n      const items = STAGES.map(([id, a, b2]) => h(\"li\", { \"data-stage\": id }, h(\"span\", { class: \"ic\", \"aria-hidden\": \"true\" }), prepared() && b2 ? b2 : a));\n      const barFill = h(\"i\", { \"data-testid\": \"draft-bar\" }), count = h(\"span\", { class: \"num\", \"data-testid\": \"draft-count\" }, \"\");\n      live = { items, barFill, count };\n      const main1 = h(\"button\", { type: \"button\", class: \"btn primary lg sbar-main\", disabled: true }, \"Drafting…\");\n      const b = G.sbar(\"This usually takes under a minute. You can leave this page; we'll keep going.\", main1);\n      put(b, heading(\"Drafting the timeline\", \"This usually takes under a minute. You can leave this page; we'll keep going.\"),\n        h(\"div\", { class: \"panel fixed-box\" }, h(\"div\", { class: \"count-line\" }, h(\"span\", {}, \"Working on it\"), count),\n          h(\"div\", { class: \"bar\", role: \"progressbar\", \"aria-label\": \"Drafting progress\", \"aria-valuemin\": \"0\", \"aria-valuemax\": String(STAGES.length) }, barFill), h(\"ol\", { class: \"stages\", \"data-testid\": \"stage-list\", \"aria-live\": \"polite\" }, items)));\n      showStage(0, STAGES.length);\n      focusTitle();\n    }\n    function showStage(idx, total) {\n      if (!live) return;\n      live.items.forEach((li, i) => { li.className = i < idx ? \"done\" : i === idx ? \"now\" : \"\"; li.firstChild.textContent = i < idx ? \"✓\" : \"\"; });\n      live.barFill.style.width = Math.round((idx / total) * 100) + \"%\"; live.count.textContent = `${Math.min(idx + 1, total)} of ${total}`;\n      live.barFill.parentNode.setAttribute(\"aria-valuenow\", String(idx));\n      ctx.setStepStatus(1, `Drafting ${Math.min(idx + 1, total)} of ${total}`, \"todo\");\n    }\n    async function poll() {\n      if (dead) return;\n      let s;\n      try { s = await G.api.status(token, ctx.signal); }\n      catch (e) { if (e.name === \"AbortError\" || dead) return; timer = setTimeout(poll, 2000); return; }\n      if (dead) return;\n      if (s.status === \"ready\" || s.status === \"failed\") {\n        try { c = await ctx.refresh(); } catch (e) { if (e.name === \"AbortError\" || dead) return; c = { ...c, status: s.status, error: s.error }; }\n        return s.status === \"ready\" ? drawDone() : drawFailed();\n      }\n      const stages = s.stages && s.stages.length ? s.stages : STAGES.map((x) => x[0]); const i = Math.max(0, stages.indexOf(s.stage));\n      showStage(i, stages.length); timer = setTimeout(poll, 1000);\n    }\n\n    /* ---- done ---- */\n    function drawDone() {\n      ctx.layout(\"page\"); ctx.setStepStatus(1, \"Done\", \"done\");\n      const n = counts(), hl = G.store.health || {}, [label, href] = nextTarget();\n      const msg = `${plural(n.lines, \"timeline item\")} and ${n.bills ? plural(n.bills, \"bill amount\") : \"no bill amounts\"} ${n.lines + n.bills === 1 ? \"is\" : \"are\"} ready for you to check.`;\n      const go = h(\"a\", { class: \"btn primary lg sbar-main\", href, \"data-testid\": \"btn-next-step\", \"data-autofocus\": \"\" }, label);\n      const b = G.sbar(\"Step 1 is done.\", go);\n      const prep = (c.models && c.models.generator_prepared) || prepared();\n      put(b, heading(\"Records added\"), h(\"div\", { class: \"panel\", \"data-testid\": \"draft-done\" },\n        h(\"div\", { class: \"done-hero\" }, h(\"div\", { class: \"big-check\", \"aria-hidden\": \"true\" }, \"✓\"), h(\"div\", {}, h(\"h2\", { \"data-testid\": \"done-title\" }, \"All set.\"), h(\"p\", { \"data-testid\": \"done-counts\" }, msg))),\n        hl.ai_banner ? h(\"p\", { class: \"muted ai-line\", \"data-testid\": \"ai-banner\" }, hl.ai_banner) : null,\n        prep ? h(\"p\", { class: \"prov\" }, h(\"span\", { class: \"tag prep\", title: G.provenance().note, \"data-testid\": \"prepared-badge\" }, \"Prepared by our team\"), \" \", G.provenance().note) : null),\n        h(\"div\", { class: \"panel\" }, h(\"h2\", {}, `${plural((c.records || []).length, \"record\")} added`), recList(), h(\"p\", { class: \"muted after-list\" }, \"To add more records, start a new case. \", h(\"a\", { href: G.url.new() }, \"Start a new case\"))));\n      focusTitle();\n    }\n\n    /* ---- stopped ---- */\n    function drawFailed() {\n      ctx.layout(\"page\"); ctx.setStepStatus(1, \"Run again\", \"attn\");\n      const err = c.error || {}, recs = (err.records || []).map(Number).filter(Boolean);\n      const list = recs.length ? (recs.length === 1 ? `record ${recs[0]}` : `records ${recs.slice(0, -1).join(\", \")} and ${recs[recs.length - 1]}`) : \"\";\n      const again = h(\"button\", { type: \"button\", class: \"btn primary lg sbar-main\", \"data-testid\": \"btn-run-again\", \"data-autofocus\": \"\" }, \"Run it again\");\n      const home = h(\"a\", { class: \"btn quiet\", href: \"/\", \"data-testid\": \"link-home\" }, \"Back to your cases\");\n      const b = G.sbar(\"Some of the work finished. Nothing you decided is lost.\", again, home);\n      again.addEventListener(\"click\", () => run(false, again, b));\n      const hasItems = counts().lines + counts().bills > 0;\n      put(b, heading(\"Drafting stopped\", \"Some of the work finished. You can run it again; nothing you decided is lost.\"),\n        h(\"div\", { class: \"panel fixed-box\", \"data-testid\": \"draft-failed\" }, h(\"div\", { class: \"done-hero\" }, h(\"div\", { class: \"big-warn\", \"aria-hidden\": \"true\" }, \"!\"),\n          h(\"div\", {}, h(\"h2\", {}, \"Drafting stopped before it finished.\"), err.message ? h(\"p\", { \"data-testid\": \"failed-message\" }, err.message) : null)),\n          list ? h(\"p\", { class: \"muted\" }, `No line was written for ${list}. You can write ${recs.length === 1 ? \"it\" : \"them\"} yourself in step 2.`) : null,\n          hasItems ? h(\"p\", { class: \"muted\" }, \"The items that did finish can be checked now in steps 2 and 3.\") : null,\n          h(\"h3\", { class: \"sub-h\" }, \"Your records\"), recList()));\n      focusTitle();\n    }\n\n    if (c.status === \"ingested\") drawFound();\n    else if (c.status === \"running\") { drawRunning(); poll(); }\n    else if (c.status === \"failed\") drawFailed();\n    else drawDone();\n    return () => { dead = true; if (timer) clearTimeout(timer); };\n  };\n})();\n"
}
````

### User / tool · 2026-11-02T21:33:19.904Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/frontend/guided/step1.js has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:34:30.054Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\np='step1.js'; s=open(p).read()\ns=s.replace(\"    ctx.view.addEventListener && null;\\n\",\"\")\nopen(p,'w').write(s)\nE\ncat > step4.js <<'E'\n/* Step 4: Get your letter (/case/<token>/letter). T-181, D-068, spec section 7. Builder A.\n   GET /export: 200 = the letter and the notes for the attorney; 422 export_blocked / judge_not_run = one row per blocker with a button back to the step that fixes it.\n   Copy and Download sit in the sticky action bar (always on screen). No drafted treatment paragraph (D-067). Letter text is inserted with textContent only.\n   Test ids: letter-status, letter-text, notes-text, btn-copy-letter, btn-download-letter, btn-copy-notes, btn-download-notes, check-copy-anyway, btn-first-undecided, blockers, blocker (data-code),\n   btn-blocker, btn-rejudge, cfg-exhibit, cfg-bates-prefix, cfg-bates-start, btn-save-cfg, cfg-error, prepared-badge, bar-msg, action-bar, page-error, btn-retry. */\n(function () {\n  const G = window.G, { h } = G;\n  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + \"s\"}`;\n  const slug = (t) => String(t || \"case\").toLowerCase().replace(/[^a-z0-9]+/g, \"-\").replace(/^-+|-+$/g, \"\").slice(0, 60) || \"case\";\n\n  G.pages.letter = async function (ctx) {\n    const token = ctx.token, sig = ctx.signal;\n    let c = ctx.case, exp = null, blockers = null, cfg = null, ack = null, flashTimer = null;\n    const main = h(\"main\", { class: \"wrap wide\", id: \"main\" });\n    ctx.view.append(main);\n\n    const head = () => h(\"div\", { class: \"page-h\" }, h(\"div\", { class: \"ph-main\" }, h(\"div\", { class: \"eyebrow\" }, \"Step 4 of 4\"), h(\"h1\", { \"data-testid\": \"page-title\", tabindex: \"-1\" }, \"Get your letter\"),\n      h(\"p\", {}, \"Copy the treatment section into your demand letter, or download it. The notes on the right are for the attorney only.\")));\n\n    /* ---- load ---- */\n    async function load() {\n      exp = null; blockers = null;\n      try { exp = await G.api.exportCase(token, sig); }\n      catch (e) {\n        if (e.name === \"AbortError\") throw e;\n        if (e.status === 422 && e.detail && Array.isArray(e.detail.blockers)) blockers = e.detail.blockers;\n        else throw e;\n      }\n      if (exp) { try { cfg = await G.api.call(\"GET\", \"/cases/\" + encodeURIComponent(token) + \"/export_config\", null, sig); } catch (e) { if (e.name === \"AbortError\") throw e; cfg = null; } }\n    }\n    const undecidedCount = () => { const k = (c.review && c.review.counts) || {}; return (k.pending || 0) + (k.edit_to_check || 0); };\n    function firstUndecidedUrl() {\n      const s2 = [].concat(c.entries || [], c.undated_entries || [], c.flags || []).some(G.steps.undecided);\n      return s2 ? G.url.timeline(token) : G.url.bills(token);\n    }\n    const itemUrl = (b) => !b.item_id ? G.url.timeline(token) : b.kind === \"amount\" ? G.url.bills(token, b.item_id) : G.url.timeline(token, b.item_id);\n    const findItem = (id) => [].concat(c.entries || [], c.undated_entries || [], c.amounts || [], c.flags || []).find((i) => i.id === id);\n\n    /* ---- downloads and copies (code, client side) ---- */\n    function download(text, name) {\n      const url = URL.createObjectURL(new Blob([text], { type: \"text/plain;charset=utf-8\" })), a = h(\"a\", { href: url, download: name });\n      document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);\n    }\n    function flash(btn, label) { const was = btn.getAttribute(\"data-label\") || btn.textContent; btn.setAttribute(\"data-label\", was); btn.textContent = label; clearTimeout(flashTimer); flashTimer = setTimeout(() => { btn.textContent = was; }, 2000); }\n    async function copy(text, pre, btn, say) {\n      try { await navigator.clipboard.writeText(text); flash(btn, \"Copied\"); say(\"Copied. Paste it into your demand letter.\"); return; } catch (_) { /* fall through */ }\n      let ok = false;\n      try { const r = document.createRange(); r.selectNodeContents(pre); const s = getSelection(); s.removeAllRanges(); s.addRange(r); ok = document.execCommand(\"copy\"); } catch (_) { ok = false; }\n      if (ok) { flash(btn, \"Copied\"); say(\"Copied. Paste it into your demand letter.\"); }\n      else say(\"Your browser blocked copying. The text is selected: press Ctrl+C (Cmd+C on a Mac).\");\n    }\n\n    /* ---- draw ---- */\n    function draw() {\n      ctx.layout(\"page\");\n      const title = G.titleOf(c), ready = !!exp, pending = ready ? undecidedCount() : 0;\n      const letter = h(\"pre\", { class: ready ? \"doc\" : \"doc placeholder\", id: \"letter\", tabindex: \"0\", \"data-testid\": \"letter-text\", \"aria-label\": \"Your letter section\" });\n      const notes = h(\"pre\", { class: ready ? \"doc notes\" : \"doc notes placeholder\", id: \"notes\", tabindex: \"0\", \"data-testid\": \"notes-text\", \"aria-label\": \"Notes for the attorney\" });\n      if (ready) { letter.textContent = exp.letter_text; notes.textContent = exp.internal_notes_text; }\n      else { letter.textContent = \"Your letter will appear here once the problem above is fixed.\"; notes.textContent = \"The notes appear with the letter.\"; }\n\n      const copyL = h(\"button\", { type: \"button\", class: \"btn primary lg sbar-main\", \"data-testid\": \"btn-copy-letter\", \"data-autofocus\": \"\" }, \"Copy letter\");\n      const dlL = h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-download-letter\" }, \"Download letter (.txt)\");\n      const copyN = h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-copy-notes\" }, \"Copy notes\");\n      const dlN = h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-download-notes\" }, \"Download notes (.txt)\");\n      const blanks = ready && /\\[Ex\\. __|Bates __/.test(exp.letter_text);\n      const bar = G.sbar(\"\", copyL, dlL); bar.el.classList.add(\"wide\");\n      const sayDefault = () => ready ? (pending && !ack.checked ? `Tick the box above to copy without ${plural(pending, \"item\")} that still need a decision.` : \"Copy this into your demand letter.\" + (blanks ? \" The [Ex. __ / Bates __] blanks are yours to fill in.\" : \"\")) : \"Fix the problem above first.\";\n      const gate = () => { const on = ready && (!pending || ack.checked); [copyL, dlL, copyN, dlN].forEach((b) => { b.disabled = !on; }); bar.say(sayDefault()); };\n      copyL.addEventListener(\"click\", () => copy(exp.letter_text, letter, copyL, (t) => bar.say(t)));\n      copyN.addEventListener(\"click\", () => copy(exp.internal_notes_text, notes, copyN, (t) => bar.say(t)));\n      dlL.addEventListener(\"click\", () => { download(exp.letter_text, `${slug(title)}-letter.txt`); bar.say(\"Downloaded your letter.\"); });\n      dlN.addEventListener(\"click\", () => { download(exp.internal_notes_text, `${slug(title)}-notes.txt`); bar.say(\"Downloaded the notes for the attorney.\"); });\n\n      /* status row */\n      let status, extra = null;\n      if (!ready) {\n        const n = blockers.length;\n        status = h(\"div\", { class: \"note-box bad\", role: \"alert\", \"data-testid\": \"letter-status\" }, h(\"span\", { class: \"nb-text\" }, \"The letter can't be made yet.\", h(\"span\", {}, \"Fix the problem below, then come back here.\")));\n        extra = h(\"ul\", { class: \"blockers\", \"data-testid\": \"blockers\" }, blockers.map(blockerRow));\n        ctx.setStepStatus(4, plural(n, \"problem\"), \"attn\");\n      } else if (pending) {\n        ack = h(\"input\", { type: \"checkbox\", \"data-testid\": \"check-copy-anyway\" }); ack.addEventListener(\"change\", gate);\n        status = h(\"div\", { class: \"note-box\", \"data-testid\": \"letter-status\" }, h(\"span\", { class: \"nb-text\" }, `${plural(pending, \"item\")} still ${pending === 1 ? \"needs\" : \"need\"} a decision.`, h(\"span\", {}, \"If you don't decide them, they stay out of the letter. The letter below is what would be sent now.\")),\n          h(\"a\", { class: \"btn primary lg\", href: firstUndecidedUrl(), \"data-testid\": \"btn-first-undecided\" }, \"Go to the first one\"));\n        extra = h(\"label\", { class: \"check anyway\" }, ack, `Copy it anyway, without ${plural(pending, \"item\")}.`);\n        ctx.setStepStatus(4, \"Not yet\", \"todo\");\n      } else {\n        const k = exp.counts || {}, parts = [plural(k.entries != null ? k.entries : 0, \"timeline line\")]; if (k.charges) parts.push(plural(k.charges, \"charge\"));\n        status = h(\"div\", { class: \"note-box ok\", \"data-testid\": \"letter-status\" }, h(\"span\", { class: \"nb-text\" }, \"Your letter is ready. Every item has an answer.\", h(\"span\", {}, `${parts.join(\" and \")} ${parts.length > 1 || (k.entries || 0) === 1 ? \"are\" : \"are\"} in it. Nothing is left undecided.`)));\n        ctx.setStepStatus(4, \"Done\", \"done\");\n      }\n      const prep = ready ? !!(exp.provenance && exp.provenance.generator_prepared) : !!(c.models && c.models.generator_prepared);\n      const prov = prep ? h(\"p\", { class: \"prov\" }, h(\"span\", { class: \"tag prep\", title: G.provenance().note, \"data-testid\": \"prepared-badge\" }, \"Prepared by our team\"), \" \", G.provenance().note) : null;\n\n      const cfgBox = ready ? cfgPanel(letter, bar, () => { blanksRefresh(); }) : null;\n      function blanksRefresh() { /* the letter text changed: the blanks sentence follows it */ const b = /\\[Ex\\. __|Bates __/.test(exp.letter_text); const was = blanks; if (b !== was) { draw(); } }\n\n      main.replaceChildren(head(), status, extra, prov,\n        h(\"div\", { class: \"letter-grid\" },\n          h(\"section\", {}, h(\"div\", { class: \"doc-h\" }, h(\"h2\", {}, \"Your letter section\"), h(\"span\", { class: \"muted\" }, \"Paste into the demand letter\")), letter),\n          h(\"section\", {}, h(\"div\", { class: \"doc-h\" }, h(\"h2\", {}, \"Notes for the attorney\"), h(\"span\", { class: \"do-not-send\" }, \"Do not send\")), notes, h(\"div\", { class: \"doc-actions\" }, copyN, dlN))),\n        cfgBox);\n      bar.el.remove(); ctx.view.append(bar.el);\n      document.title = \"Get your letter – Treatment Timeline\";\n      gate();\n    }\n\n    function blockerRow(b) {\n      const code = (b.next_action && b.next_action.code) || \"\", id = b.item_id;\n      let act;\n      if (code === \"DECIDE\") act = h(\"a\", { class: \"btn primary\", href: G.url.timeline(token), \"data-testid\": \"btn-blocker\" }, \"Go to step 2\");\n      else if (code === \"EDIT_SUMMARY\" || code === \"EDIT_QUOTE\") act = h(\"a\", { class: \"btn primary\", href: itemUrl(b), \"data-testid\": \"btn-blocker\" }, \"Fix it\");\n      else if (code === \"DISMISS_OR_ENTER_BY_HAND\") act = h(\"a\", { class: \"btn primary\", href: itemUrl(b), \"data-testid\": \"btn-blocker\" }, \"Go to it\");\n      else if (code === \"RERUN_JUDGE\") {\n        const it = id ? findItem(id) : null;\n        if (it && it.rerun_available) act = h(\"button\", { type: \"button\", class: \"btn primary\", \"data-testid\": \"btn-rejudge\", onclick: (ev) => rejudge(ev.currentTarget) }, \"Run the second check again\");\n        else act = h(\"span\", { class: \"muted blk-note\", \"data-testid\": \"blocker-note\" }, \"The second check can't run here. Fix the wording in your own words, or leave the item out.\");\n      } else if (code === \"CONFIRM_RERUN\") act = h(\"a\", { class: \"btn primary\", href: G.url.records(token), \"data-testid\": \"btn-blocker\" }, \"Go to step 1\");\n      else if (code === \"RUN_IN_PROGRESS\") act = h(\"span\", { class: \"muted blk-note\", \"data-testid\": \"blocker-note\" }, \"Wait for drafting to finish.\");\n      else act = id ? h(\"a\", { class: \"btn primary\", href: itemUrl(b), \"data-testid\": \"btn-blocker\" }, \"Go to it\") : h(\"a\", { class: \"btn primary\", href: G.url.timeline(token), \"data-testid\": \"btn-blocker\" }, \"Go to step 2\");\n      return h(\"li\", { \"data-testid\": \"blocker\", \"data-code\": code || b.reason_code || \"\" }, h(\"span\", { class: \"blk-why\" }, b.why || \"This needs a look before the letter can be made.\"), act);\n    }\n    async function rejudge(btn) {\n      btn.disabled = true; btn.textContent = \"Checking…\";\n      try { await G.api.rejudge(token); } catch (e) { if (e.name === \"AbortError\") return; btn.disabled = false; btn.textContent = \"Run the second check again\"; btn.after(h(\"span\", { class: \"bad blk-note\", role: \"alert\" }, e.message)); return; }\n      try { c = await ctx.refresh(); await load(); draw(); } catch (e) { if (e.name === \"AbortError\") return; showError(e); }\n    }\n\n    /* ---- exhibit and page numbers (optional) ---- */\n    function cfgPanel(letter, bar, changed) {\n      const mk = (id, label, ph, val, mode) => ({ f: h(\"div\", { class: \"field\" }, h(\"label\", { for: id }, label), h(\"input\", { id, \"data-testid\": \"cfg-\" + id.replace(\"cfg-\", \"\"), placeholder: ph, value: val == null ? \"\" : String(val), maxlength: \"20\", inputmode: mode || null, autocomplete: \"off\" })) });\n      const ex = mk(\"cfg-exhibit\", \"Exhibit\", \"e.g. 4\", cfg && cfg.exhibit), bp = mk(\"cfg-bates-prefix\", \"Bates prefix\", \"e.g. RIV\", cfg && cfg.bates_prefix), bs = mk(\"cfg-bates-start\", \"First number\", \"e.g. 1\", cfg && cfg.bates_start, \"numeric\");\n      const err = h(\"p\", { class: \"err-slot\", role: \"alert\", \"data-testid\": \"cfg-error\" });\n      const save = h(\"button\", { type: \"button\", class: \"btn lg\", \"data-testid\": \"btn-save-cfg\" }, \"Save numbers\");\n      const val = (x) => x.f.querySelector(\"input\").value.trim();\n      save.addEventListener(\"click\", async () => {\n        err.textContent = \"\"; const body = {}; if (val(ex)) body.exhibit = val(ex); if (val(bp)) body.bates_prefix = val(bp);\n        if (val(bs)) { if (!/^\\d{1,8}$/.test(val(bs))) { err.textContent = \"The first number must be a whole number, like 1.\"; return; } body.bates_start = Number(val(bs)); }\n        save.disabled = true;\n        try { cfg = await G.api.call(\"PUT\", \"/cases/\" + encodeURIComponent(token) + \"/export_config\", body); exp = await G.api.exportCase(token, sig); letter.textContent = exp.letter_text; changed(); bar.say(\"Saved. The numbers are in your letter.\"); }\n        catch (e) { if (e.name === \"AbortError\") return; err.textContent = e.message; }\n        finally { save.disabled = false; }\n      });\n      return h(\"div\", { class: \"panel cfg-panel\" }, h(\"h2\", {}, \"Exhibit and page numbers (optional)\"), h(\"p\", { class: \"muted\" }, \"Fill these in to replace “[Ex. __ / Bates __]” in every source line.\"),\n        h(\"div\", { class: \"cfg\" }, ex.f, bp.f, bs.f, save), err);\n    }\n\n    function showError(e) {\n      ctx.layout(\"page\"); main.replaceChildren(G.errorBlock(e, async () => { try { await load(); draw(); } catch (e2) { if (e2.name !== \"AbortError\") showError(e2); } }, \"We couldn't make the letter\"));\n    }\n\n    main.replaceChildren(head(), h(\"div\", { class: \"note-box\", role: \"status\" }, h(\"span\", { class: \"nb-text\" }, \"Making your letter…\")), h(\"div\", { class: \"letter-grid\" }, h(\"section\", {}, h(\"div\", { class: \"doc placeholder\" }, \"Making your letter…\")), h(\"section\", {}, h(\"div\", { class: \"doc notes placeholder\" }, \"\"))));\n    try { await load(); draw(); }\n    catch (e) { if (e.name === \"AbortError\") return; showError(e); }\n    return () => { clearTimeout(flashTimer); };\n  };\n})();\nE\ncat > step1.css <<'E'\n/* step1: rules for this module only (T-181 Builder A). Also holds the sticky action bar (.sbar) that step 4 reuses. Shell tokens and base classes live in styles.css. */\n.sbar { position: sticky; bottom: 0; z-index: 4; background: var(--panel); border-top: 1px solid var(--border); box-shadow: var(--shadow-bar); }\nbody.page .view:has(> .sbar) { display: flex; flex-direction: column; }\nbody.page .view > .sbar { margin-top: auto; flex: none; }\n.sbar-in { max-width: 1180px; margin: 0 auto; padding: 12px var(--gutter); display: flex; align-items: center; gap: 24px; }\n.sbar.wide .sbar-in { max-width: 1440px; }\n.sbar-msg { flex: 1; min-width: 0; min-height: 3rem; display: flex; align-items: center; font-size: 1.0625rem; line-height: 1.5rem; color: var(--muted); }\n.sbar-msg.bad { color: var(--bad); font-weight: 650; }\n.sbar-btns { display: flex; align-items: center; gap: 12px; flex: none; }\n.sbar-alt { display: inline-flex; align-items: center; gap: 12px; }\n.sbar-main { min-width: 240px; }\n.btn.primary:disabled, .btn.primary[aria-disabled=\"true\"] { opacity: .45; }\n.hint.bad { color: var(--bad); font-weight: 600; min-height: 1.4rem; }\n.field .hint { min-height: 1.4rem; }\n\n/* choice tiles */\n.panel .note-box.demo-note { margin-bottom: 20px; }\n.how { border: 0; padding: 0; margin: 0; min-width: 0; }\n.tiles.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }\n.tiles { grid-template-columns: repeat(3, minmax(0, 1fr)); }\n.tile.off { background: var(--sunken); border-style: dashed; cursor: not-allowed; }\n.tile.off .tl-h, .tile.off p { color: var(--muted); }\n.tile.off .tl-h::before { border-color: var(--border); }\n.tile .tile-why { font-weight: 650; color: var(--warn); margin-top: 8px; }\n.tile:has(input:checked) p { color: var(--text); }\n.input-box { transition: none; }\n.input-box.over { border-color: var(--accent); background: var(--accent-soft); }\n.input-box .box-col { display: flex; flex-direction: column; gap: 8px; width: 100%; height: 100%; min-height: 0; }\n.input-box .box-col.center { align-items: center; justify-content: center; text-align: center; }\n.input-box textarea { flex: 1; min-height: 0; padding: 4px; }\n.input-box .hint { color: var(--muted); font-size: .9375rem; }\n.big-name { font-size: 1.25rem; word-break: break-word; }\n.sr-file { position: absolute; width: 1px; height: 1px; opacity: 0; overflow: hidden; pointer-events: none; }\n.libs { border: 0; padding: 0; margin: 0; width: 100%; height: 100%; overflow: auto; display: grid; align-content: start; gap: 4px; text-align: left; min-width: 0; }\n.lib-row { display: flex; align-items: center; gap: 14px; min-height: 48px; padding: 6px 10px; border-radius: 10px; cursor: pointer; font-weight: 600; }\n.lib-row:hover { background: var(--sunken); }\n.lib-row input { width: 24px; height: 24px; flex: none; margin: 0; accent-color: var(--accent); }\n.lib-row:has(input:checked) { background: var(--accent-soft); }\n\n/* records, notes, drafting */\n.notes { display: grid; gap: 10px; margin-bottom: 16px; }\n.notes:empty { display: none; }\n.list { max-height: max(220px, calc(100vh - 560px)); }\n.list li .src { min-width: 0; overflow-wrap: anywhere; }\n.fixed-box { min-height: 0; }\n.panel h2 { margin-bottom: 12px; }\n.panel .sub-h { font-size: 1.125rem; margin: 20px 0 10px; }\n.after-list { margin-top: 16px; }\n.ai-line { margin-top: 18px; }\n.prov { margin-top: 12px; color: var(--muted); font-size: 1rem; line-height: 1.5rem; }\n.prov .tag { margin-right: 6px; }\n.panel .done-hero + .muted, .panel .done-hero + p { margin-top: 16px; }\n.draft-note { margin-top: 12px; }\n@media (max-width: 1100px) { .tiles.four { grid-template-columns: repeat(2, minmax(0, 1fr)); } }\n@media (max-width: 760px) {\n  .sbar-in { flex-direction: column; align-items: stretch; gap: 6px; padding: 8px 16px; }\n  .sbar-msg { min-height: 2.4rem; font-size: .9375rem; line-height: 1.2rem; }\n  .sbar-btns { flex-direction: column; align-items: stretch; gap: 8px; }\n  .sbar-btns .btn { width: 100%; }\n  .sbar-alt { display: flex; flex-wrap: wrap; width: 100%; }\n  .sbar-alt:empty { display: none; }\n  .sbar-alt > * { flex: 1 1 100%; }\n  .sbar-main { min-width: 0; }\n  .tiles, .tiles.four { grid-template-columns: minmax(0, 1fr); }\n  .input-box { height: 220px; }\n  .list { max-height: max(180px, calc(100vh - 640px)); }\n}\nE\ncat > step4.css <<'E'\n/* step4: rules for this module only (T-181 Builder A). Shell tokens and base classes live in styles.css; the sticky action bar is in step1.css. */\n.do-not-send { color: var(--bad); font-weight: 700; }\n.letter-grid { margin-top: 20px; align-items: start; }\n.letter-grid section { min-width: 0; }\n.doc.placeholder { height: 520px; }\n.doc.notes.placeholder { height: 520px; }\n.doc-actions .btn { min-width: 200px; }\n.blockers li { align-items: center; }\n.blockers .blk-why { flex: 1; min-width: 0; font-weight: 600; }\n.blk-note { max-width: 420px; font-size: 1rem; line-height: 1.4rem; }\n.blk-note.bad { color: var(--bad); }\n.check.anyway { margin-top: 14px; }\n.check.inline { margin: 0; font-size: 1rem; align-items: center; }\n.note-box + .blockers, .note-box + .check, .note-box + .prov { margin-top: 12px; }\n.prov { margin: 14px 0 0; color: var(--muted); font-size: 1rem; line-height: 1.5rem; }\n.cfg-panel { margin-top: 24px; }\n.cfg-panel .err-slot { margin-top: 8px; }\n@media (max-width: 760px) {\n  .doc.placeholder, .doc.notes.placeholder { height: 260px; }\n  .blockers li { flex-direction: column; align-items: stretch; }\n  .blockers li .btn { width: 100%; }\n  .doc-actions .btn { min-width: 0; }\n}\nE\n.venv/bin/python - <<'E' 2>/dev/null || true\nE\nnode -e \"\nfor (const f of ['home.js','step1.js','step4.js']) { try { new Function(require('fs').readFileSync('/Users/arsis/zlayt-pm-project/app/frontend/guided/'+f,'utf8')); console.log(f,'ok'); } catch(e){ console.log(f, e.message); } }\""
}
````

### User / tool · 2026-11-02T21:34:30.363Z

**tool result**
````
home.js ok
step1.js ok
step4.js ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:34:39.912Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\np='step4.js'; s=open(p).read()\ns=s.replace(\"let c = ctx.case, exp = null, blockers = null, cfg = null, ack = null, flashTimer = null;\",\"let c = ctx.case, exp = null, blockers = null, cfg = null, ack = null, flashTimer = null, bar0 = null;\")\ns=s.replace(\"      ctx.layout(\\\"page\\\");\\n      const title = G.titleOf(c), ready\",\"      ctx.layout(\\\"page\\\"); if (bar0) bar0.el.remove();\\n      const title = G.titleOf(c), ready\")\ns=s.replace(\"const bar = G.sbar(\\\"\\\", copyL, dlL); bar.el.classList.add(\\\"wide\\\");\",\"const bar = G.sbar(\\\"\\\", copyL, dlL); bar.el.classList.add(\\\"wide\\\"); bar0 = bar;\")\ns=s.replace(\"\"\"`${parts.join(\" and \")} ${parts.length > 1 || (k.entries || 0) === 1 ? \"are\" : \"are\"} in it. Nothing is left undecided.`\"\"\",\"\"\"`${parts.join(\" and \")} ${parts.length === 1 && (k.entries || 0) === 1 ? \"is\" : \"are\"} in it. Nothing is left undecided.`\"\"\")\ns=s.replace(\"      bar.el.remove(); ctx.view.append(bar.el);\\n\",\"      ctx.view.append(bar.el);\\n\")\nopen(p,'w').write(s)\nE\ngrep -n \"bar0\" step4.js | head; cd /Users/arsis/zlayt-pm-project && cat > /private/tmp/claude-501/shot.py <<'E'\nimport sys\nfrom playwright.sync_api import sync_playwright\nurl, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": w, \"height\": h})\n    errs=[]; pg.on(\"console\", lambda m: errs.append(m.text) if m.type==\"error\" else None); pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n    pg.goto(url); pg.wait_for_selector(\"[data-testid=view][data-ready]\"); pg.wait_for_timeout(500)\n    pg.screenshot(path=out); print(errs)\n    b.close()\nE\n.venv/bin/python /private/tmp/claude-501/shot.py http://127.0.0.1:7911/ /private/tmp/claude-501/home.png 1440 900"
}
````

### User / tool · 2026-11-02T21:34:41.090Z

**tool result**
````
13:    let c = ctx.case, exp = null, blockers = null, cfg = null, ack = null, flashTimer = null, bar0 = null;
55:      ctx.layout("page"); if (bar0) bar0.el.remove();
67:      const bar = G.sbar("", copyL, dlL); bar.el.classList.add("wide"); bar0 = bar;
[]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:34:46.123Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/home.png"
}
````

### User / tool · 2026-11-02T21:34:46.131Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:34:53.263Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\nimport re\ns=open('home.js').read()\ns=s.replace(\"  const plural = (n, one, many)\",\"  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren turns null into the text \\\"null\\\"\\n  const plural = (n, one, many)\",1)\ns=s.replace(\"main.replaceChildren(head(data.views.length ? newBtn() : null),\",\"fill(main, head(data.views.length ? newBtn() : null),\")\ns=s.replace(\"lists.replaceChildren(sec(\\\"In progress\\\", active, \\\"cases-list\\\"), sec(\\\"Finished\\\", done, \\\"cases-finished\\\"));\",\"fill(lists, sec(\\\"In progress\\\", active, \\\"cases-list\\\"), sec(\\\"Finished\\\", done, \\\"cases-finished\\\"));\")\ns=s.replace(\"main.replaceChildren(head(), h(\\\"div\\\", { class: \\\"panel empty\\\", role: \\\"alert\\\"\",\"fill(main, head(), h(\\\"div\\\", { class: \\\"panel empty\\\", role: \\\"alert\\\"\")\nopen('home.js','w').write(s)\ns=open('step4.js').read()\ns=s.replace(\"  const plural = (n, one, many)\",\"  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren turns null into the text \\\"null\\\"\\n  const plural = (n, one, many)\",1)\ns=s.replace(\"main.replaceChildren(head(), status, extra, prov,\",\"fill(main, head(), status, extra, prov,\")\nopen('step4.js','w').write(s)\nE\ngrep -n \"replaceChildren\" home.js step1.js step4.js | cut -c1-150"
}
````

### User / tool · 2026-11-02T21:34:53.437Z

**tool result**
````
home.js:17:  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren t
home.js:94:      top.replaceChildren(input, save, cancel);
home.js:95:      const close = (title) => { hooks.editing(-1); titleEl.textContent = title; titleEl.title = title; el.setAttribute("data-title", title
home.js:165:        lists.replaceChildren(h("div", { class: "panel empty", "data-testid": "cases-empty" }, h("div", { class: "em-ic", "aria-hidden": "
step1.js:18:    return { el, slot, say(text, kind) { msg.textContent = text; msg.className = "sbar-msg" + (kind ? " " + kind : ""); }, alts(...a) { sl
step1.js:67:        box.className = "input-box solid"; box.replaceChildren(h("div", { class: "box-col" }, ta, h("p", { class: "hint" }, `Up to ${lim.m
step1.js:71:        box.replaceChildren(h("div", { class: "box-col center" }, st.file ? [h("b", { class: "big-name", "data-testid": "file-name" }, st.
step1.js:75:        box.replaceChildren(h("fieldset", { class: "libs" }, h("legend", { class: "sr" }, "Choose a test case"), lib.map((x) => {
step1.js:82:        box.replaceChildren(h("div", { class: "box-col center" }, h("b", { class: "big-name" }, "The sample case"), h("span", { class: "mu
step1.js:180:    const put = (newBar, ...kids) => { main.replaceChildren(...kids.filter(Boolean)); if (bar) bar.el.remove(); bar = newBar; if (bar) ct
step4.js:8:  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren t
step4.js:151:      ctx.layout("page"); main.replaceChildren(G.errorBlock(e, async () => { try { await load(); draw(); } catch (e2) { if (e2.name !== "
step4.js:154:    main.replaceChildren(head(), h("div", { class: "note-box", role: "status" }, h("span", { class: "nb-text" }, "Making your letter…")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:34:57.002Z

**tool call — Bash**
````
{
 "command": "grep -rln \"interrupted\\|status.*failed\" tests/e2e/*.py | head; grep -n \"failed\" tests/e2e/test_multicase.py | head -10"
}
````

### User / tool · 2026-11-02T21:34:57.116Z

**tool result**
````
tests/e2e/test_count_charge.py
tests/e2e/test_count_duplicate.py
tests/e2e/test_adversarial.py
tests/e2e/conftest.py
tests/e2e/test_letter_matrix.py
tests/e2e/test_charge_confirm.py
tests/e2e/test_mvp_finish.py
tests/e2e/test_mvp_polish.py
tests/e2e/test_polish_r4.py
tests/e2e/test_conflict_skipped.py
32:            if s["status"] in ("ready", "failed"):
214:def test_call_outs_for_running_failed_edits_tray_and_blockers_come_from_the_list_response(page, cs):
226:            mk("tkfail", "Failed case", status="failed", export_ready=False, run={"stage": "judge_entries", "steps_done": 3, "steps_total": 8, "running": False, "error": True}),
236:    expect(_row(page, "tkfail").get_by_test_id("cases-stage")).to_contain_text("Analysis failed")
238:    expect(fl.get_by_test_id("cases-next")).to_contain_text("run it again")        # a failed row says what to do
335:def test_a_failed_list_load_shows_a_sentence_and_a_retry_button_in_the_same_place(page, cs):
346:    assert "server answered" not in err.inner_text() and "Request failed" not in err.inner_text()
347:    expect(page.get_by_test_id("cases-filter-all")).to_be_hidden()          # nothing to filter while the list failed
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:34:58.424Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/e2e/test_mvp_finish.py | cut -c1-220; grep -n \"needs_db\\|sqlite3\\|UPDATE\" tests/e2e/test_mvp_finish.py | head"
}
````

### User / tool · 2026-11-02T21:34:58.535Z

**tool result**
````
"""T-174 MVP finish (designer round 2, reviews/MVP-ux-audit-r2.md): F8 the skip link and n go to the item "Do this first" names, F9 one open count on every surface, F13 a sticky section nav
and a Back to review control in Export, F14 leaving the sample preview creates no case, F15 every input error offers one action, F16 the 'Add a synthetic case' bar is a styled card that only
the overview shows, F20 the search box and the progress track use the tokens in dark mode, F21 a rate row gives one Not counted reason, N3 a placeholder keeps focus through a repaint.
New test ids (declared in tests/e2e/conftest.py, 'T-174'): section-nav, nav-overview, nav-timeline, nav-flags, nav-charges, nav-export, btn-back-to-review, btn-error-action, charge-detail.
Needs the fixture backend in local mode (a plain run starts its own)."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE, golden_text

TITLE = "Rivera v. Northgate (MVA 2026-01)"


@pytest.fixture
def rivera():
    st, c = api("POST", "/api/cases", {"sample": True, "title": TITLE}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")


def _page(pw, w, h, scheme="light"):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, permissions=["clipboard-read", "clipboard-write"])
    return b, ctx.new_page()


def _active_item(pg):
    return pg.evaluate("(() => { const a = document.activeElement, r = a && a.closest && a.closest('[data-item-id]'); return r ? r.getAttribute('data-item-id') : null; })()")


def _first_named(pg):
    box = pg.get_by_test_id("case-overview"); expect(box).to_have_attribute("data-do-first-item", re.compile(r".+"), timeout=15000)
    return box.get_attribute("data-do-first-item")


def _num(text, tail):
    m = re.search(r"(\d+)\s*" + tail, text); assert m, (text, tail)
    return int(m.group(1))


# ---- F8: one first item. The skip link and n go where Do this first goes.
def test_the_skip_link_and_n_go_to_the_item_do_this_first_names(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        first = _first_named(pg)
        entries = [i["id"] for i in api("GET", f"/api/cases/{rivera}")[1]["entries"]]
        assert first not in entries, "the sample case names a non-entry first, which is what makes the old 'top of the list' wrong"
        pg.get_by_test_id("skip-review").focus(); pg.keyboard.press("Enter")
        assert _active_item(pg) == first, (_active_item(pg), first)
        pg.get_by_test_id("entry-1").focus(); assert _active_item(pg) != first
        pg.keyboard.press("n")
        assert _active_item(pg) == first, (_active_item(pg), first)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:00.375Z

**tool call — Bash**
````
{
 "command": "sed -n 22,120p tests/e2e/guided/test_shell_smoke.py | cut -c1-240; grep -n \"^def \\|^@pytest.fixture\" tests/e2e/conftest.py | head -40"
}
````

### User / tool · 2026-11-02T21:35:00.473Z

**tool result**
````
    seen = []
    page.add_init_script(HOOK)
    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" and not any(a in m.text for a in allow_404) else None)
    page.on("response", lambda r: seen.append(f"http {r.status}: {r.url}") if r.status >= 400 and not any(a in r.url for a in allow_404) else None)
    page.on("requestfailed", lambda r: seen.append("requestfailed: " + r.url) if "ERR_ABORTED" not in (r.failure or "") else None)      # a fetch the app aborted on purpose when she moved on is not a failure
    return seen


def go(page, path="/"):
    page.goto(C.SERVER + path)
    page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000)


def rect(page, sel):
    return page.evaluate("(s) => { const r = document.querySelector(s).getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round); }", sel)


def chrome(page):
    return {s: rect(page, s) for s in CHROME}


def case_paths(tok):
    return [f"/case/{tok}/{p}" for p in ("records", "timeline", "bills", "letter")]


def test_every_route_loads_with_no_console_errors(page, sample_case):
    seen = watch(page)
    for path in ["/", "/new"] + case_paths(sample_case) + [f"/case/{sample_case}/timeline?item=e3"]:
        go(page, path)
        page.wait_for_timeout(250)
        assert page.get_by_test_id("page-title").first.inner_text().strip(), path
        assert "Synthetic data only" in page.get_by_test_id("banner-synthetic").inner_text()
        assert page.get_by_test_id("app-header").is_visible() and page.get_by_test_id("footer-note").count() == 1
        assert page.get_by_test_id("page-error").count() == 0, path
        assert (page.evaluate("window.__errs") or []) == [], path
    assert seen == [], seen


def test_banner_demo_label_and_footer_follow_health_answers(page):
    go(page)
    hl = C.api("GET", "/api/health")[1]
    badge = page.get_by_test_id("demo-badge")
    if hl["demo_mode"]:
        label = "Demo: sample answers prepared by our team" if hl["answers"] == "prepared" else "Demo: recorded AI answers"
        expect(badge).to_have_text(label)
        note = page.get_by_test_id("footer-note").inner_text()
        if hl["answers"] == "prepared":      # D-065 (amended T-177 r2): say whose answers these are, and that a second AI model checked them
            assert label in note and "not written by an AI model" in note and "A second AI model then checked each answer against its quote." in note
            assert "not written by an AI model" in badge.get_attribute("title")
        else:
            assert label in note and "real AI answers recorded earlier" in note
    else:
        expect(badge).to_have_count(0)


def test_step_bar_per_route(page, sample_case):
    go(page)
    expect(page.get_by_test_id("step-bar")).to_be_hidden()
    expect(page.get_by_test_id("btn-theme")).to_be_visible()
    go(page, "/new")
    for n in (1, 2, 3, 4):
        s = page.get_by_test_id(f"step-{n}")
        assert (s.get_attribute("aria-current") == "step") == (n == 1)
        assert (s.get_attribute("aria-disabled") == "true") == (n > 1), n
    assert page.get_by_test_id("case-title").inner_text() == "New case"
    for n, path in enumerate(case_paths(sample_case), 1):
        go(page, path)
        labels = [page.get_by_test_id(f"step-{k}").locator(".st-label .long").inner_text() for k in (1, 2, 3, 4)]
        assert labels == LABELS
        for k in (1, 2, 3, 4):
            s = page.get_by_test_id(f"step-{k}")
            assert (s.get_attribute("aria-current") == "step") == (k == n), (path, k)
            assert s.get_attribute("aria-disabled") is None and s.evaluate("e => e.tagName") == "A"
        assert page.get_by_test_id("page-title").first.is_visible()
    # a ready sample case: step 1 done, its steps 2 and 3 carry the counts the data rules give, step 4 is not yet
    go(page, case_paths(sample_case)[0])
    status = [page.get_by_test_id(f"step-{k}").locator(".st-status").inner_text() for k in (1, 2, 3, 4)]
    case = C.api("GET", f"/api/cases/{sample_case}")[1]
    s2 = [i for i in case["entries"] + case["undated_entries"] + case["flags"] if i["state"] != "rejected"]
    s3 = [i for i in case["amounts"] if i["state"] != "rejected"]
    assert status[0] == "Done" and status[1] == f"{len(s2)} of {len(s2)} left" and status[2] == f"{len(s3)} amounts" and status[3] == "Not yet", status
    assert page.get_by_test_id("case-title").inner_text() == case["title"]


def test_chrome_never_moves_between_pages_layouts_or_scrolling(page, sample_case):
    seen = watch(page)
    go(page, case_paths(sample_case)[0])
    first = chrome(page)
    assert first["[data-testid=banner-synthetic]"][1] == 0 and first["[data-testid=app-header]"][1] == first["[data-testid=banner-synthetic]"][3]
    assert first["[data-testid=step-bar]"][1] == first["[data-testid=app-header]"][1] + first["[data-testid=app-header]"][3]
    for n in (2, 3, 4, 1, 3):                    # by clicking the bar, as a person would: page layout, frame layout, page, page, frame
        page.get_by_test_id(f"step-{n}").click()
        expect(page.get_by_test_id(f"step-{n}")).to_have_attribute("aria-current", "step")
        page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
        assert chrome(page) == first, n
    expect(page.locator("body")).to_have_class("frame")
    go(page, case_paths(sample_case)[3])         # a page-layout page: the chrome is sticky, so it stays when the page scrolls
    page.evaluate("document.querySelector('main').append(Object.assign(document.createElement('div'), { className: 'spacer-test' })); document.querySelector('.spacer-test').style.height = '4000px'")
116:def pytest_configure(config):
165:def needs_db():
176:def _up():
183:def pytest_collection_modifyitems(config, items):
191:def api(method, path, body=None):
201:def golden_text(name):
204:def tray_entry_for_record(tok, record_id):
233:@pytest.fixture
234:def base_url():
237:@pytest.fixture
238:def sample_case():
252:@pytest.fixture(scope="session")
253:def pw():
258:@pytest.fixture
259:def page(pw):
268:def open_case(page, tok):
272:def reveal(loc):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:07.207Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/shots.py <<'E'\nimport sys, json, urllib.request, time\nfrom playwright.sync_api import sync_playwright\nB=\"http://127.0.0.1:7911\"\ndef api(m,p,b=None):\n    r=urllib.request.Request(B+p,method=m,data=json.dumps(b).encode() if b is not None else None,headers={\"Content-Type\":\"application/json\"})\n    try:\n        with urllib.request.urlopen(r) as x: return x.status, json.loads(x.read() or b\"null\")\n    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b\"null\")\ndef mk(title, run=True):\n    t=api(\"POST\",\"/api/cases\",{\"sample\":True,\"title\":title})[1][\"token\"]\n    if run:\n        api(\"POST\",f\"/api/cases/{t}/run\",{\"confirm_rerun\":False})\n        for _ in range(60):\n            if api(\"GET\",f\"/api/cases/{t}/status\")[1][\"status\"]==\"ready\": break\n            time.sleep(.3)\n    return t\nfound=mk(\"Found case\",False); done=mk(\"Done case\"); full=mk(\"Full case\")\nc=api(\"GET\",f\"/api/cases/{full}\")[1]\nfor i in c[\"entries\"]+c[\"undated_entries\"]+c[\"flags\"]+c[\"amounts\"]:\n    s,r=api(\"POST\",f\"/api/cases/{full}/items/{i['id']}/review\",{\"action\":\"accept\"})\n    if s!=200: print(i[\"id\"],s,r[\"error\"][\"code\"])\nprint(found,done,full)\njson.dump({\"found\":found,\"done\":done,\"full\":full},open(\"/private/tmp/claude-501/toks.json\",\"w\"))\nE\n.venv/bin/python /private/tmp/claude-501/shots.py"
}
````

### User / tool · 2026-11-02T21:35:08.292Z

**tool result**
````
wRVfNB0ck4-JoK35PtTb3Q Kp4f5y4mf4xczeMLT7yi9Q jB6venF7sMsGZGbweMNkCA
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:12.739Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/pages.py <<'E'\nimport sys, json\nfrom playwright.sync_api import sync_playwright\nT=json.load(open(\"/private/tmp/claude-501/toks.json\")); B=\"http://127.0.0.1:7911\"\nonly = sys.argv[1:] \nP={\"home\":\"/\",\"new\":\"/new\",\"found\":f\"/case/{T['found']}/records\",\"done\":f\"/case/{T['done']}/records\",\"letter\":f\"/case/{T['full']}/letter\",\"pending\":f\"/case/{T['done']}/letter\"}\nwith sync_playwright() as p:\n    b=p.chromium.launch()\n    for w,h in ((1440,900),(390,844)):\n        pg=b.new_page(viewport={\"width\":w,\"height\":h}, permissions=[\"clipboard-read\",\"clipboard-write\"]); errs=[]\n        pg.on(\"console\", lambda m: errs.append(m.text) if m.type==\"error\" else None); pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n        for k,u in P.items():\n            if only and k not in only: continue\n            pg.goto(B+u); pg.wait_for_selector(\"[data-testid=view][data-ready]\",state=\"attached\"); pg.wait_for_timeout(400)\n            pg.screenshot(path=f\"/private/tmp/claude-501/s-{k}-{w}.png\")\n            pr=pg.locator(\".sbar .btn.primary, .sbar-main\").first\n            if pr.count(): bb=pr.bounding_box(); print(k,w,\"primary bottom\",round(bb[\"y\"]+bb[\"height\"]),\"vh\",h, \"scrollW\",pg.evaluate(\"document.documentElement.scrollWidth\"))\n        print(errs)\n    b.close()\nE\n.venv/bin/python /private/tmp/claude-501/pages.py"
}
````

### User / tool · 2026-11-02T21:35:19.425Z

**tool result**
````
new 1440 primary bottom 888 vh 900 scrollW 1425
found 1440 primary bottom 888 vh 900 scrollW 1425
done 1440 primary bottom 888 vh 900 scrollW 1425
letter 1440 primary bottom 888 vh 900 scrollW 1425
pending 1440 primary bottom 888 vh 900 scrollW 1425
['Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)']
new 390 primary bottom 836 vh 844 scrollW 375
found 390 primary bottom 780 vh 844 scrollW 375
done 390 primary bottom 836 vh 844 scrollW 375
letter 390 primary bottom 772 vh 844 scrollW 375
pending 390 primary bottom 772 vh 844 scrollW 375
['Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:23.970Z

**tool call — Bash**
````
{
 "command": "T=$(.venv/bin/python -c \"import json;print(json.load(open('/private/tmp/claude-501/toks.json'))['done'])\"); curl -s localhost:7911/api/cases/$T/trace | .venv/bin/python -c \"\nimport sys,json; d=json.load(sys.stdin); print(list(d.keys())); \nfor s in d['steps']:\n    if s['id'] in ('export_gate','export'): print(json.dumps(s)[:1200])\nprint(json.dumps(d.get('export_gate'))[:600])\"; sed -n 653,684p memory/contracts/api.md | cut -c1-700"
}
````

### User / tool · 2026-11-02T21:35:24.112Z

**tool result**
````
['token', 'mode', 'status', 'verdict', 'progress', 'steps']
{"id": "export_gate", "label": "Ready to export?", "kind": "code", "status": "fail", "why": "Nothing is accepted or edited yet, so the letter would be empty.", "reason_code": "NOTHING_ACCEPTED", "rule": "row 19", "blocks_export": true, "evidence": {}, "next_action": {"code": "DECIDE", "text": "Accept, edit or dismiss this item.", "target": {"view": "queue"}}, "counts": {"blocking": 1, "pending_items": 23, "date_unconfirmed": 0, "accepted": 0, "edit_not_confirmed": 0, "dismissed": 0, "rejected_not_blocking": 0, "judge_not_run": 0, "code_check_failed": 0, "money_in_letter": 0}, "ready": false, "blockers": [{"item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "Nothing is accepted or edited yet, so the letter would be empty.", "next_action": {"code": "DECIDE", "text": "Accept, edit or dismiss this item.", "target": {"view": "queue"}}}], "warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 23, "why": "23 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "text": "Accept, edit or dismiss this item.", "target": {"view": "queue"}, "options": ["accept", "edit", "dismiss"]}}], "n
null
### GET /api/cases/{token}/trace
```json
{ "token": "k3Jf9x...", "mode": "metadata", "status": "ready",
  "verdict": { "code": "needs_attention", "label": "12 items still need your decision" },
  "progress": { "done": 8, "total": 10, "label": "8 of 10 steps settled" },
  "steps": [
    { "id": "ingest", "n": 1, "label": "Read the paste and split it into records", "kind": "code", "status": "pass",
      "why": "9 records found.", "reason_code": null, "rule": "row 1",
      "counts": {"records": 9, "duplicates_merged": 0, "characters": 4120}, "evidence": {}, "next_action": null },
    { "id": "split", "n": 2, "label": "Record boundaries", "kind": "code", "status": "pass", "counts": {"method": "code", "llm_split": false}, "...": "..." },
    { "id": "dates", "n": 3, "label": "Dates read by code", "kind": "code", "status": "fail", "reason_code": "DATE_AMBIGUOUS",
      "counts": {"parsed": 7, "confirmed": 0, "ambiguous": 1, "missing": 1},
      "next_action": {"code": "CONFIRM_DATE", "text": "...", "target": {"view": "dates_to_confirm"}} },
    { "id": "extract", "kind": "llm", "counts": {"records_to_draft": 9, "entries": 8, "rejected": 0, "records_without_entry": 1} },
    { "id": "grounding", "kind": "code", "counts": {"items_checked": 20, "rejected": 1, "reasons": {"GROUNDING_EXCERPT_NOT_VERBATIM": 1}} },
    { "id": "judges", "kind": "llm", "counts": {"items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1} },
    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
    { "id": "totals", "kind": "code", "counts": {"accepted_cents": 0, "pending_cents": 839000, "pending_charges": 2, "not_totaled": 1} },
    { "id": "review", "kind": "human", "counts": {"pending": 21, "accepted": 0, "edited": 0, "dismissed": 0} },
    { "id": "export_gate", "n": 10, "label": "Ready to export?", "kind": "code", "status": "fail", "reason_code": "NOTHING_ACCEPTED",
      "why": "Nothing is accepted or edited yet, so the letter would be empty.", "ready": false,
      "counts": {"blocking": 1, "pending_items": 21, "date_unconfirmed": 1, "accepted": 0, "dismissed": 0, "rejected_not_blocking": 1, "judge_not_run": 0},
      "blockers": [ { "item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "...", "next_action": {"code": "DECIDE", "text": "..."} } ],
      "warnings": [ { "reason_code": "ITEMS_NOT_REVIEWED", "count": 21, "why": "21 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "text": "...", "target": {"view": "queue"}} } ],
      "next_action": {"code": "DECIDE", "text": "..."} } ] }
```
Each case step has the shared step keys plus `counts` (object, may be `{}`); `export_gate` also has `ready` and `blockers[]`. Step order is fixed: `ingest, split, dates, extract, grounding, judges, flags, totals, review, export_gate`. Before the AI run (`status: "ingested"`) `extract`, `grounding`, `judges` and `flags` (AI part) are `pending`; the code-made flags and amounts already count.

`verdict.code` for the case: `ready` (export gate open), `needs_attention` (nothing accepted yet, or accepted items not double-checked), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.judge.reason_code` for entries, amounts, flags, edits and manual entries (in `ladder_json`; no schema change).

**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below), `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty) and `MONEY_IN_LETTER` (T-139 r4: a line of the final letter text states an amount; one per line, `item_id` the entry or null), all with `item_id` null except `JUDGE_NOT_RUN`, the code-check blockers and `MONEY_IN_LETTER`. **Code-check blocker (D-045(b),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:30.001Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\np='step4.js'; s=open(p).read()\nold=s[s.index(\"    async function load() {\"):s.index(\"    const undecidedCount\")]\nnew='''    async function load() {\n      exp = null; blockers = null;\n      /* the check trace first: its export gate says \"ready\" or lists the blockers without a refused request (a 422 would show as a console error); the export is read only when it will be 200 */\n      try { const tr = await G.api.trace(token, sig), gate = (tr.steps || []).find((x) => x.id === \"export_gate\"); if (gate && !gate.ready && Array.isArray(gate.blockers) && gate.blockers.length) { blockers = gate.blockers; return; } }\n      catch (e) { if (e.name === \"AbortError\") throw e; /* fall through: the export answers for itself */ }\n      try { exp = await G.api.exportCase(token, sig); }\n      catch (e) {\n        if (e.name === \"AbortError\") throw e;\n        if (e.status === 422 && e.detail && Array.isArray(e.detail.blockers)) blockers = e.detail.blockers;\n        else throw e;\n      }\n      if (exp) { try { cfg = await G.api.call(\"GET\", \"/cases/\" + encodeURIComponent(token) + \"/export_config\", null, sig); } catch (e) { if (e.name === \"AbortError\") throw e; cfg = null; } }\n    }\n'''\ns=s.replace(old,new)\nopen(p,'w').write(s)\nE\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python /private/tmp/claude-501/pages.py letter pending"
}
````

### User / tool · 2026-11-02T21:35:32.805Z

**tool result**
````
letter 1440 primary bottom 888 vh 900 scrollW 1425
pending 1440 primary bottom 888 vh 900 scrollW 1425
[]
letter 390 primary bottom 772 vh 844 scrollW 375
pending 390 primary bottom 772 vh 844 scrollW 375
[]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:34.928Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python /private/tmp/claude-501/pages.py home new found done >/dev/null; echo ok"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:35.147Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-new-1440.png"
}
````

### User / tool · 2026-11-02T21:35:39.693Z

**tool result**
````
ok
````

### User / tool · 2026-11-02T21:35:39.703Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:42.569Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-new-390.png"
}
````

### User / tool · 2026-11-02T21:35:42.577Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:42.812Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-found-1440.png"
}
````

### User / tool · 2026-11-02T21:35:42.820Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:44.713Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-done-1440.png"
}
````

### User / tool · 2026-11-02T21:35:44.723Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:44.962Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-letter-1440.png"
}
````

### User / tool · 2026-11-02T21:35:44.970Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:50.181Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-letter-390.png"
}
````

### User / tool · 2026-11-02T21:35:50.191Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:35:50.393Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-home-390.png"
}
````

### User / tool · 2026-11-02T21:35:50.401Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:01.211Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\ns=open('step1.js').read()\ns=s.replace(\"const focusTitle = () => { const t = main.querySelector(\\\"h1\\\"); if (t) t.focus({ preventScroll: true }); };\",\"let moved = false;      // a screen change after load moves focus to the new heading (a first paint is left to the shell)\\n    const focusTitle = () => { if (!moved) return; const t = main.querySelector(\\\"h1\\\"); if (t) t.focus({ preventScroll: true }); };\")\ns=s.replace(\"      c = { ...c, status: \\\"running\\\" }; drawRunning(); poll();\",\"      c = { ...c, status: \\\"running\\\" }; moved = true; drawRunning(); poll();\")\ns=s.replace(\"        return s.status === \\\"ready\\\" ? drawDone() : drawFailed();\",\"        moved = true; return s.status === \\\"ready\\\" ? drawDone() : drawFailed();\")\ns=s.replace(\"A short synthetic case to try it out.\",\"A short made-up case to try it out.\")\nopen('step1.js','w').write(s)\ns=open('step4.js').read()\ns=s.replace('const bar = G.sbar(\"\", copyL, dlL); bar.el.classList.add(\"wide\"); bar0 = bar;','const bar = G.sbar(\"\", copyL, dlL); bar.el.classList.add(\"wide\", \"pair\"); bar0 = bar;')\nopen('step4.js','w').write(s)\nc=open('step1.css').read()\nc+='''.page-h h1:focus, .home-h h1:focus, .errbox h1:focus { outline: none; }\n'''\nopen('step1.css','w').write(c)\nc=open('step4.css').read()\nc=c.replace(\"@media (max-width: 760px) {\",\"\"\"@media (max-width: 760px) {\n  .sbar.pair .sbar-btns { flex-direction: row; }\n  .sbar.pair .sbar-btns .btn { flex: 1 1 0; width: auto; min-width: 0; white-space: normal; line-height: 1.2rem; height: auto; min-height: 52px; padding: 6px 8px; font-size: 1rem; }\n  .sbar.pair .sbar-alt { display: contents; }\n  .doc-h { flex-wrap: wrap; }\"\"\",1)\nopen('step4.css','w').write(c)\nE\ngrep -n \"sbar-alt\" step1.css | head"
}
````

### User / tool · 2026-11-02T21:36:01.327Z

**tool result**
````
10:.sbar-alt { display: inline-flex; align-items: center; gap: 12px; }
60:  .sbar-alt { display: flex; flex-wrap: wrap; width: 100%; }
61:  .sbar-alt:empty { display: none; }
62:  .sbar-alt > * { flex: 1 1 100%; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:08.791Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/states.py <<'E'\nimport json\nfrom playwright.sync_api import sync_playwright\nT=json.load(open(\"/private/tmp/claude-501/toks.json\")); B=\"http://127.0.0.1:7911\"\nSTAGES=[\"ingest\",\"extract\",\"verify\",\"judge_entries\",\"amounts\",\"conflicts\",\"flags\",\"finalize\"]\nwith sync_playwright() as p:\n    b=p.chromium.launch()\n    for w,h in ((1440,900),(390,844)):\n        pg=b.new_page(viewport={\"width\":w,\"height\":h})\n        errs=[]; pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n        # drafting: case reports running + status mocked at stage 3\n        def case(route):\n            r=route.fetch(); j=r.json(); j[\"status\"]=\"running\"; route.fulfill(json=j)\n        pg.route(f\"**/api/cases/{T['done']}\", case)\n        pg.route(f\"**/api/cases/{T['done']}/status\", lambda r: r.fulfill(json={\"token\":\"x\",\"status\":\"running\",\"stage\":\"verify\",\"stages\":STAGES,\"progress\":{\"done\":2,\"total\":8,\"label\":\"x\"},\"counts\":{},\"error\":None}))\n        pg.goto(B+f\"/case/{T['done']}/records\"); pg.wait_for_selector(\"[data-testid=view][data-ready]\",state=\"attached\"); pg.wait_for_timeout(500)\n        pg.screenshot(path=f\"/private/tmp/claude-501/s-drafting-{w}.png\")\n        pg.unroute_all()\n        def failed(route):\n            r=route.fetch(); j=r.json(); j[\"status\"]=\"failed\"; j[\"error\"]={\"code\":\"run_partial\",\"message\":\"The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.\",\"records\":[2,7]}; route.fulfill(json=j)\n        pg.route(f\"**/api/cases/{T['done']}\", failed)\n        pg.goto(B+f\"/case/{T['done']}/records\"); pg.wait_for_selector(\"[data-testid=view][data-ready]\",state=\"attached\"); pg.wait_for_timeout(500)\n        pg.screenshot(path=f\"/private/tmp/claude-501/s-failed-{w}.png\")\n        print(errs)\n    b.close()\nE\n.venv/bin/python /private/tmp/claude-501/states.py"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:09.082Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-drafting-1440.png"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:09.322Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/s-failed-390.png"
}
````

### User / tool · 2026-11-02T21:36:11.849Z

**tool result**
````
[]
[]
````

### User / tool · 2026-11-02T21:36:11.864Z

**tool result**
````
[image]
````

### User / tool · 2026-11-02T21:36:11.865Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:21.228Z

**tool call — Bash**
````
{
 "command": "D=$(mktemp -d /private/tmp/claude-501/zlb-XXXX); (PORT=7912 HOST=127.0.0.1 ZLAYT_MODE=local ENABLE_LIVE=1 LLM_BACKEND=claude-cli ZLAYT_DB=$D/db.sqlite3 .venv/bin/python -m app.main > $D/server.log 2>&1 & echo $! > /private/tmp/claude-501/zlb-pid); sleep 4; curl -s localhost:7912/api/health | head -c 400; echo; .venv/bin/python - <<'E'\nimport json,urllib.request\nt=open('evals/golden/sample.txt').read()\nr=urllib.request.Request(\"http://127.0.0.1:7912/api/cases\",data=json.dumps({\"text\":t,\"title\":\"x\"}).encode(),headers={\"Content-Type\":\"application/json\"})\nd=json.load(urllib.request.urlopen(r)); print(d[\"status\"], d[\"record_count\"])\nE"
}
````

### User / tool · 2026-11-02T21:36:25.503Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"claude-cli","demo_mode":false,"answers":"live","live_enabled":true,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5","generator_prepared":false},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by
ingested 9
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:27.737Z

**tool call — Bash**
````
{
 "command": "grep -rln \"application/pdf\" tests | head; grep -rn \"def .*pdf\" tests/e2e/*.py tests/*.py 2>/dev/null | head -5"
}
````

### User / tool · 2026-11-02T21:36:27.852Z

**tool result**
````
tests/unit/test_pdf_checks_api.py
tests/unit/test_case_list.py
tests/unit/test_pdf_hidden_r3.py
tests/unit/test_t183_hardening.py
tests/unit/test_pdf_hidden_r2.py
tests/unit/test_pdf_upload.py
tests/unit/test_pdf_hidden_r4.py
tests/unit/test_pdf_ocr_isolation.py
tests/e2e/test_input.py:17:def test_pdf_upload_refused_with_plain_message(page, tmp_path):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:29.208Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p tests/unit/test_pdf_upload.py | cut -c1-200; sed -n 10,40p tests/e2e/test_input.py | cut -c1-220"
}
````

### User / tool · 2026-11-02T21:36:29.301Z

**tool result**
````
"""PDF text-layer upload (D-031, T-054): same records as paste, page-mapped citations, scanned PDFs refused with no LLM call."""
import re
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X, ingest as I, pdf_text as PT
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._pdf import make_pdf, sample_pdf
from tests.unit.test_export import build_case


def _norm(s):
    return " ".join(s.split())


def test_text_pdf_of_the_sample_gives_the_same_nine_records_as_paste():
    """AC1: records, header dates, labels and excerpts equal the pasted sample; every excerpt is verbatim in the extracted text."""
    got = PT.extract(sample_pdf(G.raw("sample")))
    pdf, paste = I.ingest(got["text"]), I.ingest(G.raw("sample"))
    assert len(pdf["records"]) == 9 and pdf["split_method"] == "code" and not [w for w in pdf["warnings"] if w["code"] == "SPLIT_AMBIGUOUS"]
    for a, b in zip(pdf["records"], paste["records"]):
        assert (a["date_raw"], a["source"], _norm(a["excerpt"])) == (b["date_raw"], b["source"], _norm(b["excerpt"]))
        assert a["excerpt"] in got["text"]
    assert pdf["groups"] == paste["groups"]


def test_pages_map_records_to_page_numbers():
    got = PT.extract(sample_pdf(G.raw("sample"), split_after_record=5))
    recs = I.ingest(got["text"])["records"]
    assert [PT.page_for(got["pages"], r["char_start"]) for r in recs] == [1, 1, 1, 1, 1, 2, 2, 2, 2]
    assert PT.page_for([], 5) is None and got["text"][got["pages"][1]["start"]:].startswith("=== Record 6 ===")


@pytest.mark.parametrize("data,code", [
    (make_pdf([["x"]], image_only=True), "pdf_no_text_layer"),
    (make_pdf([["   "]]), "pdf_no_text_layer"),
    (b"not a pdf at all", "pdf_unreadable"),
    (b"%PDF-1.4\ngarbage", "pdf_unreadable"),
    (b"%PDF-" + b"0" * (PT.MAX_PDF_BYTES + 1), "pdf_too_large"),
    page.goto(BASE); assert page.get_by_test_id("banner-synthetic").is_visible()

def test_load_sample_shows_nine_records_before_any_model_call(page):
    """R-IN-1 (row 1): 'N records found' appears right after ingest; the record count is 9."""
    page.goto(BASE); page.get_by_test_id("btn-sample").click()
    assert "9" in page.get_by_test_id("record-count").inner_text()

def test_pdf_upload_refused_with_plain_message(page, tmp_path):
    """R-IN-2: a .pdf upload is refused with a plain message, not a crash."""
    f = tmp_path / "x.pdf"; f.write_bytes(b"%PDF-1.4 fake")
    page.goto(BASE); page.get_by_test_id("file-input").set_input_files(str(f))
    assert page.get_by_role("alert").is_visible()

def test_txt_upload_equals_paste(page, tmp_path):
    """R-IN-2: uploading evals/golden/sample.txt gives the same nine records as paste."""
    f = tmp_path / "s.txt"; f.write_text(golden_text("sample.txt"))
    page.goto(BASE); page.get_by_test_id("file-input").set_input_files(str(f))
    assert "9" in page.get_by_test_id("record-count").inner_text()

def _confirm(scope, date):
    """T-096: case_01's ambiguous date has a code suggestion, so the readings are radios and one explicit Confirm click is required."""
    scope.locator(f'[data-testid="confirm-date"][data-date="{date}"]').check(); scope.get_by_test_id("btn-confirm-date").click()

def _analyze_case_01(page):
    page.goto(BASE); page.get_by_test_id("input-text").fill(golden_text("case_01_date_formats.txt")); page.get_by_test_id("btn-analyze").click()
    expect(page.get_by_test_id("dates-to-confirm")).to_contain_text("04/05/2026", timeout=120000)

def test_ambiguous_date_goes_to_dates_to_confirm(page):
    """R-IN-3/R-IN-5, undated-entry branch (T-068): case_01 record 8 (04/05/2026) has an undated entry. It is listed ONCE, in
    'Dates to confirm', with both readings and its verbatim excerpt; confirming it moves the entry onto the timeline."""
    _analyze_case_01(page)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:32.624Z

**tool call — Bash**
````
{
 "command": "sed -n 186,204p tests/e2e/conftest.py; sed -n 233,285p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T21:36:32.708Z

**tool result**
````
    skip = pytest.mark.skip(reason=f"app server not running at {SERVER} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(SERVER + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

def tray_entry_for_record(tok, record_id):
@pytest.fixture
def base_url():
    return BASE

@pytest.fixture
def sample_case():
    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
    import time
    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(1)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")

@pytest.fixture(scope="session")
def pw():
    sync = pytest.importorskip("playwright.sync_api")
    with sync.sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
    except Exception: pass
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)

def reveal(loc):
    """T-166 F11: Why this status, Change quote and Audit wait behind a row's More button. Opens it when the control is hidden, and returns the control."""
    if not loc.first.is_visible():
        loc.first.locator("xpath=ancestor::*[@data-item-id][1]").locator("[data-testid=entry-toggle], [data-testid=btn-more]").first.click()
    return loc




class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:36:40.203Z

**tool call — Bash**
````
{
 "command": "T=$(.venv/bin/python -c \"import json;print(json.load(open('/private/tmp/claude-501/toks.json'))['full'])\"); .venv/bin/python - <<E\nimport json,urllib.request\nd=json.load(urllib.request.urlopen(\"http://127.0.0.1:7911/api/cases/$T/export\"))\ntxt=open(\"evals/golden/sample.export.expected.txt\").read()\nletter=txt.split(\"=== LETTER_TEXT (block 1: paste into letter) ===\\n\")[1].split(\"=== INTERNAL_NOTES_TEXT\")[0].rstrip(\"\\n\")\nnotes=txt.split(\"=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\\n\")[1].rstrip(\"\\n\")\nprint(d[\"letter_text\"]==letter, d[\"internal_notes_text\"]==notes)\nE"
}
````

### User / tool · 2026-11-02T21:36:40.394Z

**tool result**
````
True True
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:37:20.509Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/screenshots/guided && cd /Users/arsis/zlayt-pm-project && cat > tests/e2e/guided/_helpers.py <<'E'\n\"\"\"Shared helpers for the guided specs of Builder A (home, step 1, step 4). T-181 (D-068). Not a test module.\"\"\"\nimport json\nimport os\nimport re\nimport time\nimport uuid\nimport tests.e2e.conftest as C\n\nSHOTS = os.path.join(C.ROOT, \"artifacts\", \"screenshots\", \"guided\")\n\n\ndef uid():\n    return uuid.uuid4().hex[:6]\n\n\ndef api(method, path, body=None):\n    return C.api(method, path, body)\n\n\ndef make_case(title, run=True, decide=False, sample=True):\n    \"\"\"A sample case over the API: ingested, or drafted (ready), or drafted with every item accepted.\"\"\"\n    st, c = api(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": title}); assert st == 201, c\n    tok = c[\"token\"]\n    if run:\n        assert api(\"POST\", f\"/api/cases/{tok}/run\", {\"confirm_rerun\": False})[0] == 202\n        for _ in range(240):\n            s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n            if s[\"status\"] in (\"ready\", \"failed\"):\n                break\n            time.sleep(.5)\n        assert s[\"status\"] == \"ready\", s\n    if decide:\n        decide_all(tok)\n    return tok\n\n\ndef decide_all(tok, action=\"accept\"):\n    \"\"\"Step 2 and 3 are another builder's: answer every item over the API (accept).\"\"\"\n    c = api(\"GET\", f\"/api/cases/{tok}\")[1]\n    for i in c[\"entries\"] + c[\"undated_entries\"] + c[\"flags\"] + c[\"amounts\"]:\n        st, r = api(\"POST\", f\"/api/cases/{tok}/items/{i['id']}/review\", {\"action\": action})\n        assert st == 200, (i[\"id\"], st, r)\n\n\ndef golden_letter():\n    txt = open(os.path.join(C.SAMPLE_PATH, \"sample.export.expected.txt\")).read()\n    return txt.split(\"=== LETTER_TEXT (block 1: paste into letter) ===\\n\")[1].split(\"=== INTERNAL_NOTES_TEXT\")[0].rstrip(\"\\n\")\n\n\ndef golden_notes():\n    txt = open(os.path.join(C.SAMPLE_PATH, \"sample.export.expected.txt\")).read()\n    return txt.split(\"=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\\n\")[1].rstrip(\"\\n\")\n\n\ndef browser(pw, w, h, scheme=\"light\", **kw):\n    b = pw.chromium.launch()\n    ctx = b.new_context(viewport={\"width\": w, \"height\": h}, color_scheme=scheme, permissions=[\"clipboard-read\", \"clipboard-write\"], accept_downloads=True, **kw)\n    return b, ctx.new_page()\n\n\ndef shot(page, name, w):\n    os.makedirs(SHOTS, exist_ok=True)\n    page.screenshot(path=os.path.join(SHOTS, f\"{name}-{w}.png\"))\n\n\ndef in_view(page, loc):\n    \"\"\"True when the element's whole box is inside the viewport with the page scrolled to the top (nothing to scroll to reach it).\"\"\"\n    page.evaluate(\"window.scrollTo(0, 0)\")\n    b = loc.bounding_box(); vh = page.viewport_size[\"height\"]; vw = page.viewport_size[\"width\"]\n    return bool(b) and b[\"y\"] >= 0 and b[\"y\"] + b[\"height\"] <= vh and b[\"x\"] >= 0 and b[\"x\"] + b[\"width\"] <= vw\n\n\ndef no_h_scroll(page):\n    return page.evaluate(\"document.documentElement.scrollWidth <= document.documentElement.clientWidth\")\n\n\ndef go(page, path=\"/\"):\n    page.goto(C.SERVER + path)\n    page.locator(\"[data-testid=view][data-ready]\").wait_for(state=\"attached\", timeout=15000)\n\n\ndef jbody(route, status=200, payload=None):\n    route.fulfill(status=status, content_type=\"application/json\", body=json.dumps(payload))\n\n\ndef err(code, message, detail=None):\n    return {\"error\": {\"code\": code, \"message\": message, \"detail\": detail or {}}}\nE\necho ok"
}
````

### User / tool · 2026-11-02T21:37:20.596Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:02.399Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/e2e/guided/test_home.py",
 "content": "\"\"\"T-181 (D-068) guided UI, Your cases (/): spec section 3. Builder A.\nTest ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, cases-loading, cases-mode, case-card (data-token, data-title, data-finished), case-next, btn-continue, btn-rename, btn-delete,\nbtn-delete-yes, btn-delete-keep, rename-input, btn-rename-save, btn-rename-cancel, btn-remove-gone, find-case, page-error, btn-retry.\nReal cases are made over the API (the guided Step 2 and 3 belong to another builder); list shapes the fixture cannot produce (running, failed, a stale summary, six or more cases) are served by a\nroute stub of GET /api/cases that keeps the real response shape (memory/contracts/api.md).\"\"\"\nimport json\nimport re\nimport pytest\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.guided._helpers import api, make_case, decide_all, uid, browser, shot, in_view, no_h_scroll, go, jbody, err\nfrom tests.e2e.guided.test_shell_smoke import watch\n\n\n@pytest.fixture\ndef made():\n    toks = []\n    yield toks\n    for t in toks:\n        api(\"DELETE\", f\"/api/cases/{t}\")\n\n\ndef card(page, title):\n    return page.locator(f\"[data-testid=case-card][data-title={json.dumps(title)}]\")\n\n\ndef row(token, title, status=\"ready\", **kw):\n    \"\"\"One /api/cases summary row (api.md 'GET /api/cases').\"\"\"\n    r = {\"token\": token, \"title\": title, \"name\": title, \"source\": \"sample\", \"status\": status, \"record_count\": 9, \"created_at\": \"2026-11-02T10:00:00Z\", \"updated_at\": \"2026-11-02T10:00:00Z\",\n         \"last_activity_at\": \"2026-11-02T10:00:00Z\", \"run\": {\"stage\": \"finalize\", \"steps_done\": 7, \"steps_total\": 8, \"running\": False, \"error\": False},\n         \"progress\": {\"entries\": {\"decided\": 0, \"total\": 9}, \"flags\": {\"decided\": 0, \"total\": 10}, \"amounts\": {\"decided\": 0, \"total\": 4}},\n         \"counts\": {\"pending\": 23}, \"hitl\": {\"pending\": 23, \"needs_review\": 3, \"needs_review_open\": 3, \"edits_to_check\": 0, \"could_not_verify\": 0, \"gate_blockers\": [], \"gate_warnings\": []},\n         \"export_ready\": False, \"next_action\": None, \"status_error\": False, \"status_error_message\": None}\n    r.update(kw)\n    return r\n\n\ndef stub_list(page, rows):\n    def h(route):\n        if route.request.method != \"GET\":\n            return route.continue_()\n        jbody(route, 200, {\"cases\": rows})\n    page.route(\"**/api/cases\", h)\n\n\ndef test_real_cases_show_the_next_line_the_track_and_where_continue_goes(pw, made):\n    a = make_case(f\"Home A {uid()}\", run=False); b = make_case(f\"Home B {uid()}\"); c = make_case(f\"Home C {uid()}\", decide=True); made += [a, b, c]\n    ta, tb, tc = (api(\"GET\", f\"/api/cases/{t}\")[1][\"title\"] for t in (a, b, c))\n    left = sum(1 for i in api(\"GET\", f\"/api/cases/{b}\")[1][\"entries\"] + api(\"GET\", f\"/api/cases/{b}\")[1][\"undated_entries\"] + api(\"GET\", f\"/api/cases/{b}\")[1][\"flags\"] if i[\"review_status\"] == \"pending\")\n    br, page = browser(pw, 1440, 900)\n    try:\n        seen = watch(page)\n        go(page, \"/\")\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"Your cases\")\n        ca, cb, cc = card(page, ta), card(page, tb), card(page, tc)\n        # a case only read: next is to draft it, Continue opens step 1\n        expect(ca.get_by_test_id(\"case-next\")).to_have_text(\"Next: Draft the timeline.\")\n        assert ca.get_by_test_id(\"btn-continue\").get_attribute(\"href\") == f\"/case/{a}/records\"\n        assert ca.locator(\".track li\").evaluate_all(\"els => els.map(e => e.className)\") == [\"current\", \"\", \"\", \"\"]\n        # drafted, nothing decided: step 2 with the count; the first track bar is done and the second is current\n        expect(cb.get_by_test_id(\"case-next\")).to_have_text(f\"Next: Check the timeline. {left} of {left} items left.\")\n        assert cb.get_by_test_id(\"btn-continue\").get_attribute(\"href\") == f\"/case/{b}/timeline\"\n        assert cb.locator(\".track li\").evaluate_all(\"els => els.map(e => e.className)\") == [\"done\", \"current\", \"\", \"\"]\n        # everything decided and the gate open: it moves to Finished with a green Letter ready and Open letter\n        fin = page.get_by_test_id(\"cases-finished\")\n        expect(fin.locator(f\"[data-token={c}]\")).to_have_count(1)\n        assert cc.get_attribute(\"data-finished\") == \"1\"\n        expect(cc.get_by_test_id(\"case-next\")).to_contain_text(\"Finished. Your letter is ready.\")\n        expect(cc.get_by_test_id(\"btn-continue\")).to_have_text(\"Open letter\")\n        assert cc.get_by_test_id(\"btn-continue\").get_attribute(\"href\") == f\"/case/{c}/letter\"\n        assert cc.locator(\".track li\").evaluate_all(\"els => els.map(e => e.className)\") == [\"done\"] * 4\n        assert page.get_by_test_id(\"cases-list\").locator(f\"[data-token={c}]\").count() == 0\n        # Continue is a real link: it opens that step\n        cb.get_by_test_id(\"btn-continue\").click()\n        expect(page).to_have_url(re.compile(rf\"/case/{b}/timeline$\"))\n        assert seen == [], seen\n    finally:\n        br.close()\n\n\ndef test_primary_button_is_above_the_fold_and_nothing_scrolls_sideways(pw, made):\n    made.append(make_case(f\"Home fold {uid()}\", run=False))\n    for w, h in ((1440, 900), (1366, 768), (390, 844)):\n        br, page = browser(pw, w, h)\n        try:\n            go(page, \"/\")\n            assert in_view(page, page.get_by_test_id(\"btn-new-case\").first), (w, h)\n            assert no_h_scroll(page), (w, h)\n            shot(page, \"home\", w) if h in (900, 844) else None\n        finally:\n            br.close()\n\n\ndef test_rename_in_place_with_the_server_message_and_delete_with_one_confirm(pw, made):\n    tok = make_case(f\"Home rename {uid()}\", run=False); made.append(tok)\n    title = api(\"GET\", f\"/api/cases/{tok}\")[1][\"title\"]\n    br, page = browser(pw, 1440, 900)\n    try:\n        go(page, \"/\")\n        c = card(page, title)\n        before = c.bounding_box()\n        c.get_by_test_id(\"btn-rename\").click()\n        box = c.get_by_test_id(\"rename-input\"); expect(box).to_be_focused()\n        box.fill(\"Bad <name>\"); c.get_by_test_id(\"btn-rename-save\").click()\n        expect(c.locator(\"[data-slot=meta]\")).to_contain_text(\"<\")        # the server's 422 sentence, shown in the card's reserved line, not as a banner\n        expect(c.locator(\"[data-slot=meta]\")).to_have_class(re.compile(\"bad\"))\n        assert api(\"GET\", f\"/api/cases/{tok}\")[1][\"title\"] == title        # nothing saved\n        assert c.bounding_box()[\"height\"] == before[\"height\"]              # the card did not grow or shrink\n        box.fill(\"Renamed \" + uid()); newname = box.input_value()\n        c.get_by_test_id(\"btn-rename-save\").click()\n        expect(card(page, newname)).to_have_count(1)\n        assert api(\"GET\", f\"/api/cases/{tok}\")[1][\"title\"] == newname\n        c = card(page, newname)\n        c.get_by_test_id(\"btn-rename\").click(); c.get_by_test_id(\"rename-input\").fill(\"Nope\"); page.keyboard.press(\"Escape\")\n        expect(c.locator(\"h3\")).to_have_text(newname)                      # Escape cancels\n        # delete: one confirm in the same row; Keep it changes nothing\n        c.get_by_test_id(\"btn-delete\").click()\n        expect(c.get_by_test_id(\"btn-delete-yes\")).to_be_visible(); expect(c.get_by_test_id(\"btn-delete-keep\")).to_be_focused()\n        assert c.bounding_box()[\"height\"] == before[\"height\"]\n        c.get_by_test_id(\"btn-delete-keep\").click(); expect(c.get_by_test_id(\"btn-delete\")).to_be_visible()\n        assert api(\"GET\", f\"/api/cases/{tok}\")[0] == 200\n        c.get_by_test_id(\"btn-delete\").click(); c.get_by_test_id(\"btn-delete-yes\").click()\n        expect(card(page, newname)).to_have_count(0)\n        assert api(\"GET\", f\"/api/cases/{tok}\")[0] == 404\n    finally:\n        br.close()\n\n\ndef test_empty_loading_and_error_states(pw):\n    br, page = browser(pw, 1440, 900)\n    try:\n        seen = watch(page)\n        # loading: three skeleton cards in the final card size while the list is on its way\n        def slow(route):\n            if route.request.method != \"GET\":\n                return route.continue_()\n            page.wait_for_timeout(900); jbody(route, 200, {\"cases\": []})\n        page.route(\"**/api/cases\", slow)\n        page.goto(C.SERVER + \"/\")\n        expect(page.get_by_test_id(\"cases-loading\").locator(\".skeleton\")).to_have_count(3)\n        sk = page.get_by_test_id(\"cases-loading\").locator(\".skeleton\").first.bounding_box()\n        expect(page.get_by_test_id(\"cases-empty\")).to_be_visible(timeout=10000)\n        assert sk[\"height\"] >= 236\n        # empty: the explanation and the two buttons; no second \"new case\" button above it\n        expect(page.get_by_test_id(\"cases-empty\")).to_contain_text(\"You don't have any cases yet.\")\n        expect(page.get_by_test_id(\"cases-empty\")).to_contain_text(\"A case is one client's medical records. We'll guide you through 4 steps\")\n        expect(page.get_by_test_id(\"btn-new-case\")).to_have_count(1)\n        expect(page.get_by_test_id(\"btn-sample-case\")).to_have_text(\"Open the sample case\")\n        shot(page, \"home-empty\", 1440)\n        page.get_by_test_id(\"btn-sample-case\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        tok = page.url.split(\"/case/\")[1].split(\"/\")[0]\n        assert api(\"GET\", f\"/api/cases/{tok}\")[1][\"status\"] == \"ingested\"\n        api(\"DELETE\", f\"/api/cases/{tok}\")\n        # error: a plain sentence, the server's message when it has one, Try again; no status code or stack on screen\n        page.unroute(\"**/api/cases\")\n        page.route(\"**/api/cases\", lambda r: jbody(r, 500, err(\"internal\", \"boom\")) if r.request.method == \"GET\" else r.continue_())\n        go(page, \"/\")\n        e = page.get_by_test_id(\"page-error\"); expect(e).to_be_visible()\n        expect(e).to_contain_text(\"We couldn't load your cases.\")\n        t = e.inner_text(); assert \"500\" not in t and \"boom\" not in t and \"Failed to fetch\" not in t\n        page.unroute(\"**/api/cases\")\n        page.get_by_test_id(\"btn-retry\").click()\n        expect(page.get_by_test_id(\"page-error\")).to_have_count(0)\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"Your cases\")\n        assert [s for s in seen if \"500\" not in s] == [], seen        # the only noise allowed is the stubbed 500 resource line\n    finally:\n        br.close()\n\n\ndef test_stubbed_list_follows_the_next_line_rules_search_and_sort(pw):\n    na = {\"item_id\": \"f_gap_r6_r7\", \"kind\": \"flag\", \"reason\": \"The gap between record 6 and 7 needs a decision.\"}\n    rows = [\n        row(\"t1\", \"Alpha running\", status=\"running\", run={\"stage\": \"judge_entries\", \"steps_done\": 3, \"steps_total\": 8, \"running\": True, \"error\": False}, last_activity_at=\"2026-11-02T12:00:00Z\"),\n        row(\"t2\", \"Bravo failed\", status=\"failed\", run={\"stage\": \"extract\", \"steps_done\": 1, \"steps_total\": 8, \"running\": False, \"error\": True}, last_activity_at=\"2026-11-02T11:00:00Z\"),\n        row(\"t3\", \"Charlie bills\", progress={\"entries\": {\"decided\": 9, \"total\": 9}, \"flags\": {\"decided\": 10, \"total\": 10}, \"amounts\": {\"decided\": 1, \"total\": 4}}, last_activity_at=\"2026-11-02T10:30:00Z\"),\n        row(\"t4\", \"Delta blocker\", progress={\"entries\": {\"decided\": 9, \"total\": 9}, \"flags\": {\"decided\": 10, \"total\": 10}, \"amounts\": {\"decided\": 4, \"total\": 4}}, next_action=na,\n            hitl={\"pending\": 0, \"needs_review\": 0, \"needs_review_open\": 0, \"edits_to_check\": 0, \"could_not_verify\": 0, \"gate_blockers\": [{\"reason_code\": \"X\", \"kind\": \"flag\", \"item_id\": \"f_gap_r6_r7\", \"why\": \"x\"}], \"gate_warnings\": []},\n            last_activity_at=\"2026-11-02T10:20:00Z\"),\n        row(\"t5\", \"Echo stale\", status=\"ready\", record_count=None, counts=None, progress=None, hitl=None, next_action=None, status_error=True, status_error_message=\"We couldn't load this case's status\", last_activity_at=\"2026-11-02T10:10:00Z\"),\n        row(\"t6\", \"Foxtrot done\", progress={\"entries\": {\"decided\": 9, \"total\": 9}, \"flags\": {\"decided\": 10, \"total\": 10}, \"amounts\": {\"decided\": 4, \"total\": 4}}, export_ready=True, last_activity_at=\"2026-11-02T10:00:00Z\"),\n    ]\n    br, page = browser(pw, 1440, 900)\n    try:\n        stub_list(page, rows); go(page, \"/\")\n        nxt = lambda t: card(page, t).get_by_test_id(\"case-next\")\n        expect(nxt(\"Alpha running\")).to_have_text(\"Next: Wait while the timeline is drafted (stage 4 of 8).\")\n        assert card(page, \"Alpha running\").get_by_test_id(\"btn-continue\").get_attribute(\"href\") == \"/case/t1/records\"\n        expect(nxt(\"Bravo failed\")).to_have_text(\"Next: Drafting stopped. Run it again.\")\n        expect(nxt(\"Charlie bills\")).to_have_text(\"Next: Check the bills. 3 of 4 amounts left.\")\n        assert card(page, \"Charlie bills\").get_by_test_id(\"btn-continue\").get_attribute(\"href\") == \"/case/t3/bills\"\n        expect(nxt(\"Delta blocker\")).to_have_text(\"Next: Fix 1 problem before the letter. The gap between record 6 and 7 needs a decision.\")\n        assert card(page, \"Delta blocker\").get_by_test_id(\"btn-continue\").get_attribute(\"href\") == \"/case/t4/timeline?item=f_gap_r6_r7\"\n        expect(nxt(\"Echo stale\")).to_have_text(\"We couldn't load this case's status\")            # the server's sentence, in place of the track and the next line\n        expect(card(page, \"Echo stale\").get_by_test_id(\"btn-continue\")).to_have_text(\"Open case\")\n        expect(card(page, \"Echo stale\").locator(\".track\")).to_have_count(0)\n        expect(card(page, \"Foxtrot done\").get_by_test_id(\"btn-continue\")).to_have_text(\"Open letter\")\n        # newest activity first, in two sections\n        titles = page.get_by_test_id(\"cases-list\").locator(\"h3\").all_inner_texts()\n        assert titles == [\"Alpha running\", \"Bravo failed\", \"Charlie bills\", \"Delta blocker\", \"Echo stale\"], titles\n        expect(page.get_by_test_id(\"cases-finished\").locator(\"h3\")).to_have_text([\"Foxtrot done\"])\n        # six or more cases: a search box that filters as she types and updates the section counts\n        f = page.get_by_test_id(\"find-case\"); expect(f).to_be_visible()\n        f.fill(\"bills\")\n        expect(page.locator(\"[data-testid=case-card]:not([hidden])\")).to_have_count(1)\n        expect(page.locator(\"section[aria-label='In progress'] .c\")).to_have_text(\"1\")\n        f.fill(\"\"); expect(page.locator(\"[data-testid=case-card]:not([hidden])\")).to_have_count(6)\n        # 390 px: nothing clips or scrolls sideways\n        page.set_viewport_size({\"width\": 390, \"height\": 844}); page.wait_for_timeout(200)\n        assert no_h_scroll(page)\n        for c in page.get_by_test_id(\"case-card\").all():\n            b = c.bounding_box(); assert b[\"x\"] >= 0 and b[\"x\"] + b[\"width\"] <= 390\n    finally:\n        br.close()\n\n\ndef test_running_card_follows_its_stage_without_moving(pw):\n    state = {\"n\": 0}\n    def h(route):\n        if route.request.method != \"GET\":\n            return route.continue_()\n        state[\"n\"] += 1\n        steps = min(state[\"n\"], 6)\n        jbody(route, 200, {\"cases\": [row(\"t1\", \"Streaming\", status=\"running\", run={\"stage\": \"extract\", \"steps_done\": steps, \"steps_total\": 8, \"running\": True, \"error\": False})]})\n    br, page = browser(pw, 1440, 900)\n    try:\n        page.route(\"**/api/cases\", h); go(page, \"/\")\n        c = card(page, \"Streaming\"); expect(c.get_by_test_id(\"case-next\")).to_contain_text(\"stage 2 of 8\")\n        box = c.bounding_box()\n        expect(c.get_by_test_id(\"case-next\")).to_contain_text(\"stage 4 of 8\", timeout=9000)\n        assert c.bounding_box() == box\n    finally:\n        br.close()\n\n\ndef test_public_mode_lists_the_cases_this_browser_started(pw, made):\n    \"\"\"GET /api/cases is 404 in public mode: the list is the tokens kept in localStorage, each read with GET /api/cases/{token}.\"\"\"\n    tok = make_case(f\"Home public {uid()}\"); made.append(tok)\n    title = api(\"GET\", f\"/api/cases/{tok}\")[1][\"title\"]\n    br, page = browser(pw, 1440, 900)\n    try:\n        page.route(\"**/api/cases\", lambda r: jbody(r, 404, err(\"not_found\", \"Not found.\")) if r.request.method == \"GET\" else r.continue_())\n        page.add_init_script(f\"try {{ if (!localStorage.getItem('zl.guided.cases')) localStorage.setItem('zl.guided.cases', JSON.stringify([{json.dumps(tok)}, 'a-token-that-is-gone'])); }} catch (e) {{}}\")\n        go(page, \"/\")\n        expect(page.get_by_test_id(\"cases-mode\")).to_have_text(\"These are the cases started in this browser. Keep the case link to open it elsewhere.\")\n        expect(card(page, title).get_by_test_id(\"case-next\")).to_have_text(re.compile(r\"^Next: Check the timeline\\. \\d+ of \\d+ items left\\.$\"))\n        gone = page.locator(\"[data-testid=case-card][data-token=a-token-that-is-gone]\")\n        expect(gone.get_by_test_id(\"case-next\")).to_contain_text(\"This case is no longer here. Cases are kept for 24 hours.\")\n        gone.get_by_test_id(\"btn-remove-gone\").click()\n        expect(gone).to_have_count(0)\n        assert json.loads(page.evaluate(\"localStorage.getItem('zl.guided.cases')\")) == [tok]\n        # a case started in this browser is remembered (Step 1 stores it) and shows up here\n        page.evaluate(\"localStorage.removeItem('zl.guided.cases')\")\n        page.add_init_script(\"void 0\")\n        go(page, \"/new\"); page.get_by_test_id(\"btn-read\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        new = page.url.split(\"/case/\")[1].split(\"/\")[0]; made.append(new)\n        assert json.loads(page.evaluate(\"localStorage.getItem('zl.guided.cases')\")) == [new]\n        go(page, \"/\")\n        expect(page.locator(f\"[data-token={new}]\")).to_have_count(1)\n    finally:\n        br.close()\n\n\ndef test_dark_mode_and_390_screenshots(pw, made):\n    made.append(make_case(f\"Home dark {uid()}\", run=False))\n    br, page = browser(pw, 1440, 900, \"dark\")\n    try:\n        go(page, \"/\"); assert page.evaluate(\"getComputedStyle(document.body).backgroundColor\") != \"rgb(244, 246, 249)\"\n    finally:\n        br.close()\n    br, page = browser(pw, 390, 844)\n    try:\n        go(page, \"/\"); shot(page, \"home\", 390)\n    finally:\n        br.close()\n"
}
````

### User / tool · 2026-11-02T21:38:02.459Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/e2e/guided/test_home.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:14.408Z

**tool call — Bash**
````
{
 "command": "cat > tests/e2e/guided/test_golden_path.py <<'E'\n\"\"\"T-181 (D-068) README golden path, smoke: in demo mode a first-time visitor opens `/`, clicks Open the sample case, drafts it and lands on Step 2 with an entry on screen.\nPublic/demo mode has no case list (GET /api/cases is 404 by design, spec 3.3), so the browser starts with an empty list and Home offers the sample. The route stub below makes the shared\nlocal-mode test server answer like the public one. Step 2 itself is Builder B's page: this test needs it to show the entry text.\"\"\"\nimport re\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.guided._helpers import api, browser, jbody, err\nfrom tests.e2e.guided.test_shell_smoke import watch\n\n\ndef test_demo_sample_reachable_from_root(pw):\n    br, page = browser(pw, 1440, 900)\n    tok = None\n    try:\n        page.route(\"**/api/cases\", lambda r: jbody(r, 404, err(\"not_found\", \"Not found.\")) if r.request.method == \"GET\" else r.continue_())\n        page.goto(C.SERVER + \"/\")\n        page.get_by_test_id(\"btn-sample-case\").click(timeout=10000)               # Open the sample case\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=10000)\n        tok = page.url.split(\"/case/\")[1].split(\"/\")[0]\n        page.get_by_test_id(\"btn-draft\").click()                                   # Draft the timeline (instant on the prepared set)\n        expect(page.get_by_test_id(\"draft-done\")).to_be_visible(timeout=15000)\n        page.get_by_test_id(\"btn-next-step\").click()                               # Go to step 2: Check the timeline\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/timeline$\"), timeout=10000)\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"Check the timeline\")\n        first = api(\"GET\", f\"/api/cases/{tok}\")[1][\"entries\"][0][\"summary\"][:30]\n        expect(page.locator(\"body\")).to_contain_text(first, timeout=10000)          # at least one entry is on screen\n    finally:\n        if tok:\n            api(\"DELETE\", f\"/api/cases/{tok}\")\n        br.close()\nE\n(.venv/bin/python -m pytest tests/e2e/guided/test_home.py tests/e2e/guided/test_golden_path.py -x -q E2E_BASE_URL= 2>&1 | tail -30) "
}
````

### User / tool · 2026-11-02T21:38:15.413Z

**tool result**
````
ERROR: file or directory not found: E2E_BASE_URL=


no tests ran in 0.01s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:16.868Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py tests/e2e/guided/test_golden_path.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T21:38:36.215Z

**tool result**
````
tests/e2e/guided/test_home.py:105: AssertionError
____________ test_public_mode_lists_the_cases_this_browser_started _____________

pw = <playwright._impl._playwright.Playwright object at 0x10b5bedb0>
made = ['ff8vlAyIRc-5IWudD9jWgA', 'AaTT_53lJOWIi49I5HpAvw']

    def test_public_mode_lists_the_cases_this_browser_started(pw, made):
        """GET /api/cases is 404 in public mode: the list is the tokens kept in localStorage, each read with GET /api/cases/{token}."""
        tok = make_case(f"Home public {uid()}"); made.append(tok)
        title = api("GET", f"/api/cases/{tok}")[1]["title"]
        br, page = browser(pw, 1440, 900)
        try:
            page.route("**/api/cases", lambda r: jbody(r, 404, err("not_found", "Not found.")) if r.request.method == "GET" else r.continue_())
            page.add_init_script(f"try {{ if (!localStorage.getItem('zl.guided.cases')) localStorage.setItem('zl.guided.cases', JSON.stringify([{json.dumps(tok)}, 'a-token-that-is-gone'])); }} catch (e) {{}}")
            go(page, "/")
            expect(page.get_by_test_id("cases-mode")).to_have_text("These are the cases started in this browser. Keep the case link to open it elsewhere.")
            expect(card(page, title).get_by_test_id("case-next")).to_have_text(re.compile(r"^Next: Check the timeline\. \d+ of \d+ items left\.$"))
            gone = page.locator("[data-testid=case-card][data-token=a-token-that-is-gone]")
            expect(gone.get_by_test_id("case-next")).to_contain_text("This case is no longer here. Cases are kept for 24 hours.")
            gone.get_by_test_id("btn-remove-gone").click()
            expect(gone).to_have_count(0)
            assert json.loads(page.evaluate("localStorage.getItem('zl.guided.cases')")) == [tok]
            # a case started in this browser is remembered (Step 1 stores it) and shows up here
            page.evaluate("localStorage.removeItem('zl.guided.cases')")
            page.add_init_script("void 0")
            go(page, "/new"); page.get_by_test_id("btn-read").click()
            expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
            new = page.url.split("/case/")[1].split("/")[0]; made.append(new)
>           assert json.loads(page.evaluate("localStorage.getItem('zl.guided.cases')")) == [new]
E           AssertionError: assert ['AaTT_53lJOW...that-is-gone'] == ['AaTT_53lJOWIi49I5HpAvw']
E             
E             Left contains 2 more items, first extra item: 'ff8vlAyIRc-5IWudD9jWgA'
E             Use -v to get more diff

tests/e2e/guided/test_home.py:258: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_home.py::test_rename_in_place_with_the_server_message_and_delete_with_one_confirm
FAILED tests/e2e/guided/test_home.py::test_public_mode_lists_the_cases_this_browser_started
2 failed, 7 passed in 18.24s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:39.984Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\ns=s.replace(\"if (!localStorage.getItem('zl.guided.cases')) localStorage.setItem\",\"if (!sessionStorage.getItem('seeded')) {{ sessionStorage.setItem('seeded', '1'); localStorage.setItem\")\ns=s.replace(\"'a-token-that-is-gone'])); }} catch\",\"'a-token-that-is-gone'])); }} }} catch\")\ns=s.replace(\"            page.add_init_script(\\\"void 0\\\")\\n\",\"\")\nopen(p,'w').write(s)\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -k \"rename or public\" 2>&1 | grep -B30 \"Error\" | head -60"
}
````

### User / tool · 2026-11-02T21:38:47.956Z

**tool result**
````
F.                                                                       [100%]
=================================== FAILURES ===================================
___ test_rename_in_place_with_the_server_message_and_delete_with_one_confirm ___

pw = <playwright._impl._playwright.Playwright object at 0x1111938f0>
made = ['Dr-iVg6ZdiPB7vuQChgsLw']

    def test_rename_in_place_with_the_server_message_and_delete_with_one_confirm(pw, made):
        tok = make_case(f"Home rename {uid()}", run=False); made.append(tok)
        title = api("GET", f"/api/cases/{tok}")[1]["title"]
        br, page = browser(pw, 1440, 900)
        try:
            go(page, "/")
            c = card(page, title)
            before = c.bounding_box()
            c.get_by_test_id("btn-rename").click()
            box = c.get_by_test_id("rename-input"); expect(box).to_be_focused()
            box.fill("Bad <name>"); c.get_by_test_id("btn-rename-save").click()
>           expect(c.locator("[data-slot=meta]")).to_contain_text("<")        # the server's 422 sentence, shown in the card's reserved line, not as a banner
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: Locator expected to contain text '<'
E           Actual value: A case title is plain text. Remove the angle brackets and try again. 
E           Call log:
E             - Expect "to_contain_text" locator("[data-testid=case-card][data-title=\"Home rename 2c3909\"]").locator("[data-slot=meta]") with timeout 5000ms
E             - waiting for locator("[data-testid=case-card][data-title=\"Home rename 2c3909\"]").locator("[data-slot=meta]")
E               - locator resolved to <div class="cc-meta" data-slot="meta">Started Nov 2 · 9 records</div>
E               - unexpected value "Started Nov 2 · 9 records"
E               13 × locator resolved to <div data-slot="meta" class="cc-meta bad">A case title is plain text. Remove the angle brac…</div>
E                  - unexpected value "A case title is plain text. Remove the angle brackets and try again."
E           
E           Aria snapshot:
E           - text: A case title is plain text. Remove the angle brackets and try again.

tests/e2e/guided/test_home.py:105: AssertionError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:48.887Z

Test wording only; the UI behaved correctly.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:51.811Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\ns=s.replace('to_contain_text(\"<\")        #','to_contain_text(\"Remove the angle brackets\")        #')\nopen(p,'w').write(s)\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -5; python3 tools/board.py note T-181 --agent frontend-A --text \"Home + Open the sample landed in working tree (home.js/css, step1.js/css incl. records page, step4.js/css); test_golden_path.py::test_demo_sample_reachable_from_root and test_home.py pass (public-mode stub: empty list -> Open the sample case -> records -> Draft -> Step 2). SHELL BUG for frontend: app.js drawBanner does f.replaceChildren(span, p.hours ? span : null) -> the footer shows the text 'null' (replaceChildren stringifies null); filter nulls. Committing after step1/step4 specs.\""
}
````

### User / tool · 2026-11-02T21:38:51.877Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: you are running as 'frontend'; use --agent frontend
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:38:54.196Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3; python3 tools/board.py note T-181 --agent frontend --text \"frontend-A: Home + Open the sample landed in the working tree (home.js/css, step1.js/css incl. records page, step4.js/css); test_golden_path.py::test_demo_sample_reachable_from_root and test_home.py pass (public-mode stub: empty list -> Open the sample case -> records -> Draft -> Step 2). SHELL BUG for the shell owner: app.js drawBanner does f.replaceChildren(span, p.hours ? span : null) -> the footer shows the text 'null' (replaceChildren stringifies null); filter nulls. Committing after step1/step4 specs.\""
}
````

### User / tool · 2026-11-02T21:39:12.333Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_home.py::test_rename_in_place_with_the_server_message_and_delete_with_one_confirm
1 failed, 7 passed in 16.97s
noted on T-181
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:13.743Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -k rename 2>&1 | grep -E \"^E|test_home.py:[0-9]+\" | head"
}
````

### User / tool · 2026-11-02T21:39:20.592Z

**tool result**
````
E           AssertionError: Locator expected to contain text '<'
E           Actual value: A case title is plain text. Remove the angle brackets and try again. 
E           Call log:
E             - Expect "to_contain_text" locator("[data-testid=case-card][data-title=\"Home rename 0c5a5c\"]").locator("[data-slot=meta]") with timeout 5000ms
E             - waiting for locator("[data-testid=case-card][data-title=\"Home rename 0c5a5c\"]").locator("[data-slot=meta]")
E               - locator resolved to <div class="cc-meta" data-slot="meta">Started Nov 2 · 9 records</div>
E               - unexpected value "Started Nov 2 · 9 records"
E               13 × locator resolved to <div data-slot="meta" class="cc-meta bad">A case title is plain text. Remove the angle brac…</div>
E                  - unexpected value "A case title is plain text. Remove the angle brackets and try again."
E
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:21.563Z

The earlier replace didn't match (the file's comment spacing differs).

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:22.497Z

**tool call — Bash**
````
{
 "command": "sed -i 's/to_contain_text(\"<\")/to_contain_text(\"Remove the angle brackets\")/' tests/e2e/guided/test_home.py && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:39:22.623Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/e2e/guided/test_h ...": undefined label 'ests/e2e/guided/test_home.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:24.411Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\ns=s.replace('to_contain_text(\"<\")','to_contain_text(\"Remove the angle brackets\")')\nopen(p,'w').write(s)\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:39:37.425Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_home.py::test_rename_in_place_with_the_server_message_and_delete_with_one_confirm
1 failed, 7 passed in 11.96s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:38.792Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -k rename 2>&1 | grep -E \"^E|^>\" | head"
}
````

### User / tool · 2026-11-02T21:39:40.832Z

**tool result**
````
>           assert c.bounding_box()["height"] == before["height"]
E           assert 248 == 256
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:47.204Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/dbg.py <<'E'\nimport json\nfrom playwright.sync_api import sync_playwright\nT=json.load(open(\"/private/tmp/claude-501/toks.json\")); B=\"http://127.0.0.1:7911\"\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_page(viewport={\"width\":1440,\"height\":900}); pg.goto(B+\"/\"); pg.wait_for_selector(\"[data-testid=case-card]\")\n    c=pg.locator(\"[data-testid=case-card]\").first\n    def m(): return c.evaluate(\"e => [...e.children].map(x => x.className+':'+Math.round(x.getBoundingClientRect().height))\")\n    print(m()); c.get_by_test_id(\"btn-rename\").click(); print(m()); c.get_by_test_id(\"rename-input\").fill(\"a<b\"); c.get_by_test_id(\"btn-rename-save\").click(); pg.wait_for_timeout(400); print(m())\n    b.close()\nE\n.venv/bin/python /private/tmp/claude-501/dbg.py"
}
````

### User / tool · 2026-11-02T21:39:48.295Z

**tool result**
````
['cc-top:40', 'cc-meta:20', 'track:30', 'next :24', 'cc-bottom:56', 'cc-bottom:0']
['cc-top:40', 'cc-meta:20', 'track:30', 'next :24', 'cc-bottom:56', 'cc-bottom:0']
['cc-top:40', 'cc-meta bad:20', 'track:30', 'next :24', 'cc-bottom:56', 'cc-bottom:0']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:53.035Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\ns=s.replace(\"        before = c.bounding_box()\\n\",\"        before = c.bounding_box(); kids = lambda: c.evaluate(\\\"e => [...e.children].map(x => x.className + ':' + Math.round(x.getBoundingClientRect().height))\\\"); k0 = kids()\\n\",1)\ns=s.replace(\"        assert c.bounding_box()[\\\"height\\\"] == before[\\\"height\\\"]              # the card did not grow or shrink\",\"        assert c.bounding_box()[\\\"height\\\"] == before[\\\"height\\\"], (k0, kids())              # the card did not grow or shrink\",1)\nopen(p,'w').write(s)\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -k rename 2>&1 | grep -E \"^E\" | head -4"
}
````

### User / tool · 2026-11-02T21:39:55.120Z

**tool result**
````
E           assert 248 == 256
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:56.321Z

**tool call — Bash**
````
{
 "command": "grep -n \"k0\\|before\" tests/e2e/guided/test_home.py | head"
}
````

### User / tool · 2026-11-02T21:39:56.415Z

**tool result**
````
101:        before = c.bounding_box(); kids = lambda: c.evaluate("e => [...e.children].map(x => x.className + ':' + Math.round(x.getBoundingClientRect().height))"); k0 = kids()
108:        assert c.bounding_box()["height"] == before["height"], (k0, kids())              # the card did not grow or shrink
119:        assert c.bounding_box()["height"] == before["height"]
192:        expect(nxt("Delta blocker")).to_have_text("Next: Fix 1 problem before the letter. The gap between record 6 and 7 needs a decision.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:39:59.431Z

**tool call — Bash**
````
{
 "command": "echo '.ccard .cc-bottom { min-height: 56px; }' >> app/frontend/guided/home.css && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:40:12.240Z

**tool result**
````
........                                                                 [100%]
8 passed in 11.81s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:41:03.910Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/e2e/guided/test_step1.py",
 "content": "\"\"\"T-181 (D-068) guided UI, Step 1 Add records: /new and /case/<token>/records. Spec section 4. Builder A.\nTwo servers: the shared test server (demo mode: the fixture backend, so Paste and Upload are not offered as working) and a private LIVE-mode server (ENABLE_LIVE=1 with the claude-cli backend name; it only\ncreates cases (ingest is code), it never runs one) for the paste, .txt and .pdf paths and their real 413 / pdf refusals. Errors the servers do not produce on demand (429, offline, 409) use a route stub.\nTest ids: input-name, name-error, tile-paste|file|sample|library, radio-<key>, input-text, file-input, btn-choose-file, library-<id>, btn-read, btn-draft, btn-start-over, bar-msg, action-bar, btn-use-sample, btn-retry-read,\nbtn-ocr, btn-hidden-anyway, check-hidden, demo-note, records-list, records-notes, stage-list, draft-bar, draft-done, done-counts, ai-banner, prepared-badge, btn-next-step, draft-failed, btn-run-again, btn-run-yes, btn-run-cancel.\"\"\"\nimport json\nimport os\nimport re\nimport socket\nimport subprocess\nimport sys\nimport tempfile\nimport time\nimport urllib.request\nimport pytest\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.guided._helpers import api, make_case, uid, browser, shot, in_view, no_h_scroll, go, jbody, err\nfrom tests.e2e.guided.test_shell_smoke import watch\n\nSTAGES = [\"ingest\", \"extract\", \"verify\", \"judge_entries\", \"amounts\", \"conflicts\", \"flags\", \"finalize\"]\n\n\ndef health():\n    return api(\"GET\", \"/api/health\")[1]\n\n\n@pytest.fixture\ndef made():\n    toks = []\n    yield toks\n    for t in toks:\n        api(\"DELETE\", f\"/api/cases/{t}\")\n\n\n@pytest.fixture(scope=\"module\")\ndef live():\n    \"\"\"A private live-mode server (never runs a case). Yields its base URL.\"\"\"\n    s = socket.socket(); s.bind((\"127.0.0.1\", 0)); port = s.getsockname()[1]; s.close()\n    tmp = tempfile.mkdtemp(prefix=\"zlayt-live-\")\n    env = dict(os.environ, PORT=str(port), HOST=\"127.0.0.1\", ZLAYT_MODE=\"local\", ENABLE_LIVE=\"1\", LLM_BACKEND=\"claude-cli\", ZLAYT_DB=os.path.join(tmp, \"live.sqlite3\"))\n    env.pop(\"ANTHROPIC_API_KEY\", None)\n    log = open(os.path.join(tmp, \"server.log\"), \"w\")\n    proc = subprocess.Popen([sys.executable, \"-m\", \"app.main\"], cwd=C.ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)\n    base = f\"http://127.0.0.1:{port}\"\n    try:\n        for _ in range(80):\n            try:\n                urllib.request.urlopen(base + \"/api/health\", timeout=1).read(); break\n            except Exception:\n                if proc.poll() is not None:\n                    pytest.fail(\"the live-mode test server exited early\")\n                time.sleep(.5)\n        else:\n            pytest.fail(\"the live-mode test server did not answer\")\n        assert json.load(urllib.request.urlopen(base + \"/api/health\"))[\"demo_mode\"] is False\n        yield base\n    finally:\n        proc.terminate()\n        try: proc.wait(timeout=10)\n        except Exception: proc.kill()\n        log.close()\n\n\ndef goto(page, base, path):\n    page.goto(base + path)\n    page.locator(\"[data-testid=view][data-ready]\").wait_for(state=\"attached\", timeout=15000)\n\n\ndef box(page, tid):\n    b = page.get_by_test_id(tid).bounding_box(); return [round(b[k]) for k in (\"x\", \"y\", \"width\", \"height\")]\n\n\n# ------------------------------------------------------------------ demo mode: no Paste/Upload as if they worked\ndef test_demo_mode_explains_and_disables_paste_and_upload_and_the_primary_is_above_the_fold(pw):\n    if not health()[\"demo_mode\"]:\n        pytest.skip(\"demo-mode test\")\n    for w, h in ((1440, 900), (1366, 768), (390, 844)):\n        br, page = browser(pw, w, h)\n        try:\n            seen = watch(page); go(page, \"/new\")\n            expect(page.get_by_test_id(\"page-title\")).to_have_text(\"Add records\")\n            note = page.get_by_test_id(\"demo-note\"); expect(note).to_contain_text(\"This demo can only read the sample case and our test cases.\")\n            for k in (\"paste\", \"file\"):                          # shown, disabled, and the reason is visible text (not a tooltip)\n                t = page.get_by_test_id(f\"tile-{k}\")\n                assert t.get_attribute(\"aria-disabled\") == \"true\"; expect(page.get_by_test_id(f\"radio-{k}\")).to_be_disabled()\n                expect(t).to_contain_text(\"Not available in this demo.\")\n            expect(page.get_by_test_id(\"radio-sample\")).to_be_checked()\n            read = page.get_by_test_id(\"btn-read\")\n            expect(read).to_be_enabled(); assert in_view(page, read), (w, h)       # Read the records is on screen with no scrolling\n            assert no_h_scroll(page), (w, h)\n            assert [s for s in seen if \"library\" not in s and \"404\" not in s] == [], seen\n            if h in (900, 844):\n                shot(page, \"new-demo\", w)\n        finally:\n            br.close()\n\n\ndef test_demo_mode_offers_the_sample_and_a_test_case_and_reads_either(pw, made):\n    hl = health()\n    if not hl[\"demo_mode\"]:\n        pytest.skip(\"demo-mode test\")\n    lib = api(\"GET\", \"/api/library\")\n    br, page = browser(pw, 1440, 900)\n    try:\n        go(page, \"/new\")\n        name = f\"Sample {uid()}\"; page.get_by_test_id(\"input-name\").fill(name)\n        page.get_by_test_id(\"btn-read\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        made.append(page.url.split(\"/case/\")[1].split(\"/\")[0])\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"We found 9 records\")\n        expect(page.get_by_test_id(\"case-title\")).to_have_text(name)\n        if lib[0] != 200:\n            return\n        go(page, \"/new\")                                         # a test case from the library (local mode lists it)\n        page.get_by_test_id(\"tile-library\").click()\n        read = page.get_by_test_id(\"btn-read\"); expect(read).to_be_disabled()      # nothing picked yet\n        first = lib[1][\"cases\"][0][\"id\"]; page.get_by_test_id(f\"library-{first}\").check(); expect(read).to_be_enabled()\n        read.click(); expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        made.append(page.url.split(\"/case/\")[1].split(\"/\")[0])\n        assert int(re.search(r\"(\\d+)\", page.get_by_test_id(\"page-title\").inner_text()).group(1)) >= 1\n    finally:\n        br.close()\n\n\n# ------------------------------------------------------------------ the whole step, by clicking\ndef test_sample_read_found_draft_done_a_first_time_user_needs_no_instructions(pw, made):\n    br, page = browser(pw, 1440, 900)\n    try:\n        seen = watch(page); go(page, \"/new\")\n        page.get_by_test_id(\"btn-read\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        tok = page.url.split(\"/case/\")[1].split(\"/\")[0]; made.append(tok)\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"We found 9 records\")\n        assert page.get_by_test_id(\"records-list\").locator(\"li\").count() == 9\n        assert page.get_by_test_id(\"records-list\").locator(\"li\").first.inner_text().split(\"\\n\")[1:] == [\"January 9, 2026\", \"Austin EMS run report\"] or \"January 9, 2026\" in page.get_by_test_id(\"records-list\").inner_text()\n        expect(page.get_by_test_id(\"records-notes\")).to_contain_text(\"Every record has a date we could read.\")\n        assert page.get_by_test_id(\"step-1\").locator(\".st-status\").inner_text() == \"Not started\"\n        draft = page.get_by_test_id(\"btn-draft\"); assert in_view(page, draft); shot(page, \"step1-found\", 1440)\n        draft.click()\n        done = page.get_by_test_id(\"draft-done\"); expect(done).to_be_visible(timeout=20000)\n        c = api(\"GET\", f\"/api/cases/{tok}\")[1]\n        n2 = len([i for i in c[\"entries\"] + c[\"undated_entries\"] + c[\"flags\"] if i[\"state\"] != \"rejected\"]); n3 = len([i for i in c[\"amounts\"] if i[\"state\"] != \"rejected\"])\n        expect(page.get_by_test_id(\"done-counts\")).to_have_text(f\"{n2} timeline items and {n3} bill amounts are ready for you to check.\")\n        hl = health()\n        expect(page.get_by_test_id(\"ai-banner\")).to_have_text(hl[\"ai_banner\"])      # D-065: the provenance sentence the server sends\n        if hl[\"answers\"] == \"prepared\":\n            b = page.get_by_test_id(\"prepared-badge\")\n            assert \"Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.\" == b.get_attribute(\"title\")\n            expect(page.locator(\"main\")).to_contain_text(\"Prepared by our team for this demo, not written by an AI model.\")    # visible, not only a tooltip\n        expect(page.get_by_test_id(\"step-1\").locator(\".st-status\")).to_have_text(\"Done\")\n        go_next = page.get_by_test_id(\"btn-next-step\"); assert in_view(page, go_next)\n        assert go_next.get_attribute(\"href\") == f\"/case/{tok}/timeline\" and go_next.inner_text() == \"Go to step 2: Check the timeline\"\n        shot(page, \"step1-done\", 1440)\n        page.reload(); page.locator(\"[data-testid=view][data-ready]\").wait_for(state=\"attached\")      # a reload lands on the same done screen\n        expect(page.get_by_test_id(\"draft-done\")).to_be_visible()\n        assert seen == [], seen\n    finally:\n        br.close()\n\n\ndef test_drafting_shows_one_plain_checklist_then_the_done_screen(pw, made):\n    tok = make_case(f\"Drafting {uid()}\", run=False); made.append(tok)\n    prepared = health()[\"answers\"] == \"prepared\"\n    br, page = browser(pw, 1440, 900)\n    try:\n        calls = {\"status\": 0, \"case\": 0}\n        def case(route):\n            calls[\"case\"] += 1; r = route.fetch(); j = r.json()\n            if calls[\"case\"] == 1:\n                j[\"status\"] = \"running\"          # the first open says: still drafting; after it finished the real (ingested) case would be re-read, so serve a ready one\n            route.fulfill(json=j)\n        def status(route):\n            calls[\"status\"] += 1\n            if calls[\"status\"] == 1:\n                return jbody(route, 200, {\"token\": tok, \"status\": \"running\", \"stage\": \"verify\", \"stages\": STAGES, \"progress\": {\"done\": 2, \"total\": 8, \"label\": \"Step 3 of 8: verify\"}, \"counts\": {}, \"error\": None})\n            jbody(route, 200, {\"token\": tok, \"status\": \"ready\", \"stage\": \"finalize\", \"stages\": STAGES, \"progress\": {\"done\": 7, \"total\": 8, \"label\": \"x\"}, \"counts\": {\"entries\": 9, \"amounts\": 4, \"flags\": 10}, \"error\": None})\n        page.route(f\"**/api/cases/{tok}\", case); page.route(f\"**/api/cases/{tok}/status\", status)\n        goto(page, C.SERVER, f\"/case/{tok}/records\")\n        lis = page.get_by_test_id(\"stage-list\").locator(\"li\")\n        expect(lis).to_have_count(8)\n        assert lis.evaluate_all(\"els => els.map(e => e.className)\") == [\"done\", \"done\", \"now\", \"\", \"\", \"\", \"\", \"\"]\n        txt = lis.all_inner_texts()\n        assert txt[0].strip().endswith(\"Reading the records\")\n        assert (\"Getting the line our team prepared for each record\" if prepared else \"Writing one line for each record\") in txt[1]\n        joined = \" \".join(txt)\n        for jargon in (\"verify\", \"judge\", \"extract\", \"LLM\", \"excerpt\", \"ingest\", \"finalize\", \"stage\"):\n            assert jargon not in joined, jargon                  # never a raw stage id or label with ids\n        assert page.get_by_test_id(\"step-1\").locator(\".st-status\").inner_text() == \"Drafting 3 of 8\"\n        shot(page, \"step1-drafting\", 1440)\n        expect(page.get_by_test_id(\"draft-done\")).to_be_visible(timeout=10000)      # the next 1 s poll says ready\n        assert page.get_by_test_id(\"step-1\").locator(\".st-status\").inner_text() == \"Done\"\n    finally:\n        br.close()\n\n\ndef test_stopped_run_names_the_records_and_asks_before_a_rerun_that_has_answers(pw, made):\n    tok = make_case(f\"Stopped {uid()}\"); made.append(tok)\n    br, page = browser(pw, 1440, 900)\n    try:\n        def case(route):\n            j = route.fetch().json(); j[\"status\"] = \"failed\"\n            j[\"error\"] = {\"code\": \"run_partial\", \"message\": \"The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.\", \"interrupted\": True, \"records\": [2, 7]}\n            route.fulfill(json=j)\n        page.route(f\"**/api/cases/{tok}\", case)\n        posted = []\n        def run(route):\n            body = json.loads(route.request.post_data or \"{}\"); posted.append(body)\n            if not body.get(\"confirm_rerun\"):\n                return jbody(route, 409, err(\"needs_confirm\", \"This case already has decisions.\"))\n            jbody(route, 202, {\"token\": tok, \"status\": \"running\", \"stage\": \"extract\", \"started_at\": \"2026-11-02T00:00:00Z\"})\n        page.route(f\"**/api/cases/{tok}/run\", run)\n        page.route(f\"**/api/cases/{tok}/status\", lambda r: jbody(r, 200, {\"token\": tok, \"status\": \"running\", \"stage\": \"extract\", \"stages\": STAGES, \"progress\": {\"done\": 1, \"total\": 8, \"label\": \"x\"}, \"counts\": {}, \"error\": None}))\n        goto(page, C.SERVER, f\"/case/{tok}/records\")\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"Drafting stopped\")\n        expect(page.get_by_test_id(\"failed-message\")).to_contain_text(\"every decision of yours were kept\")      # the server's sentence, as given\n        expect(page.get_by_test_id(\"draft-failed\")).to_contain_text(\"No line was written for records 2 and 7. You can write them yourself in step 2.\")\n        expect(page.get_by_test_id(\"draft-failed\")).to_contain_text(\"The items that did finish can be checked now in steps 2 and 3.\")\n        assert page.get_by_test_id(\"step-1\").locator(\".st-status\").inner_text() == \"Run again\"\n        assert in_view(page, page.get_by_test_id(\"btn-run-again\")); shot(page, \"step1-failed\", 1440)\n        page.get_by_test_id(\"btn-run-again\").click()\n        expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"Run it again? Your answers so far are kept.\")\n        page.get_by_test_id(\"btn-run-cancel\").click(); expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"\")\n        page.get_by_test_id(\"btn-run-again\").click(); page.get_by_test_id(\"btn-run-yes\").click()\n        expect(page.get_by_test_id(\"stage-list\")).to_be_visible()\n        assert posted == [{\"confirm_rerun\": False}, {\"confirm_rerun\": False}, {\"confirm_rerun\": True}], posted\n    finally:\n        br.close()\n\n\n# ------------------------------------------------------------------ errors are plain sentences, with the action, in the bar\n@pytest.mark.parametrize(\"status,payload,sentence,action\", [\n    (413, err(\"input_too_large\", \"Input is too large.\"), \"That's more than we can read at once (60,000 characters or 40 records). Split it into two cases.\", None),\n    (429, err(\"busy\", \"Busy.\", {\"reason\": \"pdf_busy\"}), \"We're reading other files right now. Try again in a moment.\", \"btn-retry-read\"),\n    (429, err(\"busy\", \"This demo is full right now. Try again later.\", {\"reason\": \"demo_full\"}), \"This demo is full right now. Try again later.\", \"btn-retry-read\"),\n    (409, err(\"demo_mode_unsupported_input\", \"This demo only runs the recorded sample cases.\"), \"This demo can only read the sample and our test cases.\", \"btn-use-sample\"),\n    (400, err(\"bad_request\", \"Input is empty.\"), \"There's nothing to read yet. Paste the records or choose a file.\", None),\n    (503, err(\"llm_unavailable\", \"x\"), \"We couldn't reach the server. Your text is still here.\", \"btn-retry-read\"),\n])\ndef test_read_errors_are_plain_sentences_with_the_action(pw, status, payload, sentence, action):\n    br, page = browser(pw, 1440, 900)\n    try:\n        go(page, \"/new\")\n        page.route(\"**/api/cases\", lambda r: jbody(r, status, payload) if r.request.method == \"POST\" else r.continue_())\n        bar0 = box(page, \"action-bar\"); read0 = box(page, \"btn-read\")\n        page.get_by_test_id(\"btn-read\").click()\n        msg = page.get_by_test_id(\"bar-msg\"); expect(msg).to_have_text(sentence)\n        t = msg.inner_text()\n        for raw in (str(status), \"input_too_large\", \"demo_mode\", \"Failed to fetch\", \"HTTP\"):\n            assert raw not in t, raw\n        if action:\n            expect(page.get_by_test_id(action)).to_be_visible()\n        assert box(page, \"action-bar\") == bar0 and box(page, \"btn-read\") == read0        # nothing moved: the message has its reserved slot\n        expect(page.get_by_test_id(\"btn-read\")).to_be_enabled()\n        if action == \"btn-use-sample\":\n            page.get_by_test_id(action).click(); expect(page.get_by_test_id(\"radio-sample\")).to_be_checked(); expect(msg).not_to_have_text(sentence)\n    finally:\n        br.close()\n\n\ndef test_offline_keeps_the_input_and_try_again_works(pw, made):\n    br, page = browser(pw, 1440, 900)\n    try:\n        go(page, \"/new\")\n        page.route(\"**/api/cases\", lambda r: r.abort() if r.request.method == \"POST\" else r.continue_())\n        page.get_by_test_id(\"btn-read\").click()\n        expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"We couldn't reach the server. Your text is still here.\")\n        page.unroute(\"**/api/cases\")\n        page.get_by_test_id(\"btn-retry-read\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        made.append(page.url.split(\"/case/\")[1].split(\"/\")[0])\n    finally:\n        br.close()\n\n\ndef test_a_refused_case_name_shows_under_the_name_box_and_nothing_is_created(pw):\n    br, page = browser(pw, 1440, 900)\n    try:\n        go(page, \"/new\")\n        before = len([1 for _ in [0]])\n        page.get_by_test_id(\"input-name\").fill(\"Rivera <b>\")\n        page.get_by_test_id(\"btn-read\").click()\n        expect(page.get_by_test_id(\"name-error\")).to_contain_text(\"Remove the angle brackets\")      # the server's sentence, under the box\n        expect(page.get_by_test_id(\"input-name\")).to_be_focused()\n        assert \"/new\" in page.url\n        page.get_by_test_id(\"input-name\").fill(\"Rivera\"); expect(page.get_by_test_id(\"name-error\")).to_have_text(\"\")\n    finally:\n        br.close()\n\n\n# ------------------------------------------------------------------ live mode: paste and upload\ndef test_paste_is_disabled_until_there_is_text_then_reads_the_records(pw, live):\n    br, page = browser(pw, 1440, 900)\n    try:\n        goto(page, live, \"/new\")\n        expect(page.get_by_test_id(\"demo-note\")).to_have_count(0)\n        for k in (\"paste\", \"file\"):\n            assert page.get_by_test_id(f\"tile-{k}\").get_attribute(\"aria-disabled\") is None\n        expect(page.get_by_test_id(\"radio-paste\")).to_be_checked()\n        read = page.get_by_test_id(\"btn-read\"); expect(read).to_be_disabled()\n        page.get_by_test_id(\"input-text\").fill(\"   \\n  \"); expect(read).to_be_disabled()       # blank is nothing\n        page.get_by_test_id(\"input-text\").fill(C.golden_text(\"sample.txt\")); expect(read).to_be_enabled()\n        page.get_by_test_id(\"input-name\").fill(\"Pasted \" + uid())\n        read.click(); expect(read).to_have_text(\"Reading…\")\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=20000)\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"We found 9 records\")\n    finally:\n        br.close()\n\n\ndef test_choosing_another_way_never_moves_the_box_or_the_bar(pw, live):\n    br, page = browser(pw, 1440, 900)\n    try:\n        goto(page, live, \"/new\")\n        base = (box(page, \"input-box\"), box(page, \"btn-read\"), box(page, \"action-bar\"))\n        for k in (\"file\", \"sample\", \"library\", \"paste\"):\n            if page.get_by_test_id(f\"tile-{k}\").count() == 0:\n                continue\n            page.get_by_test_id(f\"tile-{k}\").click(); page.wait_for_timeout(100)\n            assert (box(page, \"input-box\"), box(page, \"btn-read\"), box(page, \"action-bar\")) == base, k\n    finally:\n        br.close()\n\n\ndef test_too_big_a_paste_is_refused_with_the_real_413_sentence_and_the_text_stays(pw, live):\n    br, page = browser(pw, 1440, 900)\n    try:\n        goto(page, live, \"/new\")\n        big = \"=== Record 1 ===\\nDate: 2026-01-09\\nSource: x\\nExcerpt: \\\"\" + (\"word \" * 14000) + \"\\\"\\n\"\n        page.get_by_test_id(\"input-text\").fill(big)\n        page.get_by_test_id(\"btn-read\").click()\n        expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"That's more than we can read at once (60,000 characters or 40 records). Split it into two cases.\")\n        assert len(page.get_by_test_id(\"input-text\").input_value()) > 60000          # her text is still there\n    finally:\n        br.close()\n\n\ndef test_txt_and_pdf_uploads_read_like_paste_and_bad_files_say_why(pw, live, tmp_path):\n    from tests.unit._pdf import sample_pdf, make_pdf\n    sample = C.golden_text(\"sample.txt\")\n    br, page = browser(pw, 1440, 900)\n    try:\n        goto(page, live, \"/new\"); page.get_by_test_id(\"tile-file\").click()\n        read = page.get_by_test_id(\"btn-read\"); expect(read).to_be_disabled()\n        t = tmp_path / \"s.txt\"; t.write_text(sample)\n        page.get_by_test_id(\"file-input\").set_input_files(str(t))\n        expect(page.get_by_test_id(\"file-name\")).to_have_text(\"s.txt\"); expect(read).to_be_enabled()\n        read.click(); expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=20000)\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"We found 9 records\")\n        # a PDF with a text layer\n        goto(page, live, \"/new\"); page.get_by_test_id(\"tile-file\").click()\n        p = tmp_path / \"s.pdf\"; p.write_bytes(sample_pdf(sample))\n        page.get_by_test_id(\"file-input\").set_input_files(str(p)); page.get_by_test_id(\"btn-read\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=30000)\n        expect(page.get_by_test_id(\"page-title\")).to_have_text(\"We found 9 records\")\n        # a scanned PDF: a plain sentence, and the OCR button only when the server can do it\n        goto(page, live, \"/new\"); page.get_by_test_id(\"tile-file\").click()\n        sc = tmp_path / \"scan.pdf\"; sc.write_bytes(make_pdf([[\"x\"]], image_only=True))\n        page.get_by_test_id(\"file-input\").set_input_files(str(sc)); page.get_by_test_id(\"btn-read\").click()\n        expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"This PDF looks scanned, so it has no text we can read.\", timeout=30000)\n        ocr = api(\"GET\", \"/api/health\")  # same shape on both servers; OCR availability comes from the refusal itself\n        # a file that is neither: refused in the browser before anything is sent\n        goto(page, live, \"/new\"); page.get_by_test_id(\"tile-file\").click()\n        d = tmp_path / \"x.docx\"; d.write_bytes(b\"PK\")\n        page.get_by_test_id(\"file-input\").set_input_files(str(d))\n        expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"We can read .txt and .pdf files. Choose another file.\")\n        expect(page.get_by_test_id(\"btn-read\")).to_be_disabled()\n    finally:\n        br.close()\n\n\ndef test_phone_layout_of_every_step_1_screen_has_nothing_clipped(pw, live, made):\n    tok = make_case(f\"Phone {uid()}\", run=False); made.append(tok)\n    br, page = browser(pw, 390, 844)\n    try:\n        goto(page, live, \"/new\")\n        for k in (\"paste\", \"file\", \"sample\", \"library\"):\n            if page.get_by_test_id(f\"tile-{k}\").count():\n                page.get_by_test_id(f\"tile-{k}\").click()\n        page.get_by_test_id(\"tile-paste\").click()\n        assert in_view(page, page.get_by_test_id(\"btn-read\")) and no_h_scroll(page)\n        shot(page, \"step1-add-live\", 390)\n        goto(page, C.SERVER, f\"/case/{tok}/records\")\n        assert in_view(page, page.get_by_test_id(\"btn-draft\")) and no_h_scroll(page); shot(page, \"step1-found\", 390)\n        for sel in (\"main h1\", \"[data-testid=records-list]\"):\n            b = page.locator(sel).first.bounding_box(); assert b[\"x\"] >= 0 and b[\"x\"] + b[\"width\"] <= 390, sel\n    finally:\n        br.close()\n"
}
````

### User / tool · 2026-11-02T21:41:03.964Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/e2e/guided/test_step1.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:41:05.364Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 timeout 500 .venv/bin/python -m pytest tests/e2e/guided/test_step1.py -q -x 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T21:41:05.450Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:41:07.201Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_step1.py -q 2>&1 | grep -E \"^(E |FAILED|[0-9]+ (passed|failed))|passed|failed|test_step1.py:[0-9]+:\" | head -40"
}
````

### User / tool · 2026-11-02T21:41:21.824Z

**tool result**
````
E           assert ([0, 819, 1425, 81] == [0, 819, 1425, 81]
E             
E             Use -v to get more diff and [904, 832, 240, 56] == [1018, 832, 240, 56]
E             
E             At index 0 diff: 904 != 1018
E             Use -v to get more diff)
tests/e2e/guided/test_step1.py:253: AssertionError
E           assert ([0, 819, 1425, 81] == [0, 819, 1425, 81]
E             
E             Use -v to get more diff and [904, 832, 240, 56] == [1018, 832, 240, 56]
E             
E             At index 0 diff: 904 != 1018
E             Use -v to get more diff)
tests/e2e/guided/test_step1.py:253: AssertionError
E           assert ([0, 819, 1425, 81] == [0, 819, 1425, 81]
E             
E             Use -v to get more diff and [813, 832, 240, 56] == [1018, 832, 240, 56]
E             
E             At index 0 diff: 813 != 1018
E             Use -v to get more diff)
tests/e2e/guided/test_step1.py:253: AssertionError
E           assert ([0, 819, 1425, 81] == [0, 819, 1425, 81]
E             
E             Use -v to get more diff and [904, 832, 240, 56] == [1018, 832, 240, 56]
E             
E             At index 0 diff: 904 != 1018
E             Use -v to get more diff)
tests/e2e/guided/test_step1.py:253: AssertionError
FAILED tests/e2e/guided/test_step1.py::test_read_errors_are_plain_sentences_with_the_action[429-payload1-We're reading other files right now. Try again in a moment.-btn-retry-read]
FAILED tests/e2e/guided/test_step1.py::test_read_errors_are_plain_sentences_with_the_action[429-payload2-This demo is full right now. Try again later.-btn-retry-read]
FAILED tests/e2e/guided/test_step1.py::test_read_errors_are_plain_sentences_with_the_action[409-payload3-This demo can only read the sample and our test cases.-btn-use-sample]
FAILED tests/e2e/guided/test_step1.py::test_read_errors_are_plain_sentences_with_the_action[503-payload5-We couldn't reach the server. Your text is still here.-btn-retry-read]
4 failed, 14 passed in 13.58s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:41:32.741Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\ns=open('step1.js').read()\nold=s[s.index(\"  G.sbar = function\"):s.index(\"  G.longDate\")]\nnew='''  G.sbar = function (msgText, primary, ...statics) {\n    const msg = h(\"p\", { class: \"sbar-msg\", \"aria-live\": \"polite\", \"data-testid\": \"bar-msg\" }, msgText);\n    const slot = h(\"span\", { class: \"sbar-alt\" });                         // follow-up buttons (an error's action): grows to the LEFT of the primary on desktop, below it on phones, so the primary never moves\n    const el = h(\"div\", { class: \"sbar\", \"data-testid\": \"action-bar\" }, h(\"div\", { class: \"sbar-in\" }, msg, h(\"div\", { class: \"sbar-btns\" }, slot, primary, ...statics)));\n    return { el, slot, say(text, kind) { msg.textContent = text; msg.className = \"sbar-msg\" + (kind ? \" \" + kind : \"\"); }, alts(...a) { slot.replaceChildren(...a); } };\n  };\n'''\ns=s.replace(old,new)\nopen('step1.js','w').write(s)\nc=open('step1.css').read()\nc=c.replace(\".sbar-alt { display: inline-flex; align-items: center; gap: 12px; }\",\".sbar-alt { display: inline-flex; align-items: center; gap: 12px; order: -1; }\")\nc=c.replace(\"  .sbar-alt { display: flex; flex-wrap: wrap; width: 100%; }\",\"  .sbar-alt { display: flex; flex-wrap: wrap; width: 100%; order: 5; }\")\nopen('step1.css','w').write(c)\nd=open('step4.css').read()\nd=d.replace(\"  .sbar.pair .sbar-alt { display: contents; }\",\"  .sbar.pair .sbar-alt { display: none; }\")\nopen('step4.css','w').write(d)\nE\ngrep -n \"sbar-alt\" step1.css step4.css"
}
````

### User / tool · 2026-11-02T21:41:32.860Z

**tool result**
````
step1.css:10:.sbar-alt { display: inline-flex; align-items: center; gap: 12px; order: -1; }
step1.css:60:  .sbar-alt { display: flex; flex-wrap: wrap; width: 100%; order: 5; }
step1.css:61:  .sbar-alt:empty { display: none; }
step1.css:62:  .sbar-alt > * { flex: 1 1 100%; }
step4.css:21:  .sbar.pair .sbar-alt { display: none; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:41:35.708Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_step1.py -q 2>&1 | grep -E \"^(E |FAILED)|passed|failed|test_step1.py:[0-9]+:\" | head -30"
}
````

### User / tool · 2026-11-02T21:41:50.015Z

**tool result**
````
18 passed in 13.22s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:42:30.270Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_step1.py'; s=open(p).read()\ns=s.replace(\"        before = len([1 for _ in [0]])\\n\",\"\")\ns=s.replace(\"        ocr = api(\\\"GET\\\", \\\"/api/health\\\")  # same shape on both servers; OCR availability comes from the refusal itself\\n\",\"\")\nopen(p,'w').write(s)\nE\ncat > tests/e2e/guided/test_step4.py <<'E'\n\"\"\"T-181 (D-068) guided UI, Step 4 Get your letter (/case/<token>/letter) and the first-time path from Home to a downloaded letter. Spec section 7. Builder A.\nSteps 2 and 3 belong to the other builder: here every item is answered over the API (accept) where the path needs them. Real data everywhere except the blocker-code rows (a trace stub: the fixture\nbackend cannot produce RERUN_JUDGE or RUN_FAILED blockers on demand). Test ids: letter-status, letter-text, notes-text, btn-copy-letter, btn-download-letter, btn-copy-notes, btn-download-notes,\ncheck-copy-anyway, btn-first-undecided, blockers, blocker (data-code), btn-blocker, blocker-note, btn-rejudge, cfg-exhibit, cfg-bates-prefix, cfg-bates-start, btn-save-cfg, cfg-error, prepared-badge, bar-msg, action-bar.\"\"\"\nimport json\nimport re\nimport pytest\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.guided._helpers import api, make_case, decide_all, golden_letter, golden_notes, uid, browser, shot, in_view, no_h_scroll, go, jbody, err\nfrom tests.e2e.guided.test_shell_smoke import watch\n\n\n@pytest.fixture\ndef made():\n    toks = []\n    yield toks\n    for t in toks:\n        api(\"DELETE\", f\"/api/cases/{t}/export_config\"); api(\"DELETE\", f\"/api/cases/{t}\")\n\n\ndef slug(t):\n    return re.sub(r\"^-+|-+$\", \"\", re.sub(r\"[^a-z0-9]+\", \"-\", t.lower()))\n\n\ndef box(page, tid):\n    b = page.get_by_test_id(tid).bounding_box(); return [round(b[k]) for k in (\"x\", \"y\", \"width\", \"height\")]\n\n\ndef test_first_time_path_from_home_to_a_downloaded_letter(pw, made, tmp_path):\n    \"\"\"Home -> Start a new case -> Read the records -> Draft the timeline -> (steps 2 and 3 answered over the API) -> Get your letter -> Download. Only clicks, no typing but the case name.\"\"\"\n    br, page = browser(pw, 1440, 900)\n    try:\n        seen = watch(page); go(page, \"/\")\n        page.get_by_test_id(\"btn-new-case\").first.click()\n        expect(page).to_have_url(re.compile(r\"/new$\"))\n        name = f\"First time {uid()}\"; page.get_by_test_id(\"input-name\").fill(name)\n        page.get_by_test_id(\"btn-read\").click()\n        expect(page).to_have_url(re.compile(r\"/case/[^/]+/records$\"), timeout=15000)\n        tok = page.url.split(\"/case/\")[1].split(\"/\")[0]; made.append(tok)\n        page.get_by_test_id(\"btn-draft\").click()\n        expect(page.get_by_test_id(\"draft-done\")).to_be_visible(timeout=20000)\n        page.get_by_test_id(\"btn-next-step\").click()\n        expect(page).to_have_url(re.compile(r\"/timeline$\"))\n        decide_all(tok)                                                      # Steps 2 and 3 (another builder's pages): every item answered\n        page.get_by_test_id(\"step-4\").click()\n        expect(page).to_have_url(re.compile(r\"/letter$\"))\n        expect(page.get_by_test_id(\"letter-status\")).to_contain_text(\"Your letter is ready. Every item has an answer.\")\n        expect(page.get_by_test_id(\"letter-status\")).to_contain_text(\"9 timeline lines and 2 charges are in it.\")\n        assert in_view(page, page.get_by_test_id(\"btn-copy-letter\")) and in_view(page, page.get_by_test_id(\"btn-download-letter\"))\n        with page.expect_download() as d:\n            page.get_by_test_id(\"btn-download-letter\").click()\n        dl = d.value; assert dl.suggested_filename == f\"{slug(name)}-letter.txt\", dl.suggested_filename\n        path = tmp_path / \"letter.txt\"; dl.save_as(str(path))\n        text = path.read_text()\n        assert text == golden_letter()                                       # byte for byte the golden export (evals/golden/sample.export.expected.txt)\n        assert \"TREATMENT SUMMARY\" not in text and \"narrative\" not in text.lower()          # D-067: no drafted paragraph\n        expect(page.get_by_test_id(\"step-4\")).to_have_attribute(\"data-state\", \"done\")\n        assert seen == [], seen\n    finally:\n        br.close()\n\n\ndef test_letter_ready_copy_and_download_match_the_export_and_nothing_moves(pw, made, tmp_path):\n    tok = make_case(f\"Letter {uid()}\", decide=True); made.append(tok)\n    title = api(\"GET\", f\"/api/cases/{tok}\")[1][\"title\"]\n    ex = api(\"GET\", f\"/api/cases/{tok}/export\")[1]\n    for w, h in ((1440, 900), (1366, 768), (390, 844)):\n        br, page = browser(pw, w, h)\n        try:\n            seen = watch(page); go(page, f\"/case/{tok}/letter\")\n            expect(page.get_by_test_id(\"page-title\")).to_have_text(\"Get your letter\")\n            copy = page.get_by_test_id(\"btn-copy-letter\")\n            assert in_view(page, copy) and in_view(page, page.get_by_test_id(\"btn-download-letter\")), (w, h)       # the primary actions are on screen without scrolling\n            assert page.get_by_test_id(\"letter-text\").inner_text() == ex[\"letter_text\"] and page.get_by_test_id(\"notes-text\").inner_text() == ex[\"internal_notes_text\"]\n            expect(page.get_by_test_id(\"notes-text\")).to_contain_text(\"DO NOT SEND\")\n            expect(page.locator(\"main\")).to_contain_text(\"Notes for the attorney\"); expect(page.locator(\"main\")).to_contain_text(\"Do not send\")\n            assert no_h_scroll(page), (w, h)\n            before = (box(page, \"action-bar\"), box(page, \"btn-copy-letter\"), box(page, \"btn-download-letter\"), box(page, \"letter-text\"))\n            copy.click()\n            expect(copy).to_have_text(\"Copied\")\n            assert page.evaluate(\"navigator.clipboard.readText()\") == ex[\"letter_text\"]\n            assert (box(page, \"action-bar\"), box(page, \"btn-copy-letter\"), box(page, \"btn-download-letter\"), box(page, \"letter-text\")) == before      # a label change moves nothing\n            expect(copy).to_have_text(\"Copy letter\", timeout=5000)\n            page.get_by_test_id(\"btn-copy-notes\").click(); assert page.evaluate(\"navigator.clipboard.readText()\") == ex[\"internal_notes_text\"]\n            with page.expect_download() as d:\n                page.get_by_test_id(\"btn-download-notes\").click()\n            assert d.value.suggested_filename == f\"{slug(title)}-notes.txt\"\n            p = tmp_path / f\"n{w}.txt\"; d.value.save_as(str(p)); assert p.read_text() == golden_notes()\n            assert seen == [], seen\n            shot(page, \"step4-letter\", w) if h in (900, 844) else None\n        finally:\n            br.close()\n\n\ndef test_the_letter_blanks_sentence_and_the_exhibit_numbers(pw, made):\n    tok = make_case(f\"Exhibit {uid()}\", decide=True); made.append(tok)\n    br, page = browser(pw, 1440, 900)\n    try:\n        go(page, f\"/case/{tok}/letter\")\n        expect(page.get_by_test_id(\"bar-msg\")).to_contain_text(\"The [Ex. __ / Bates __] blanks are yours to fill in.\")\n        page.get_by_test_id(\"cfg-exhibit\").fill(\"4$$\"); page.get_by_test_id(\"btn-save-cfg\").click()\n        expect(page.get_by_test_id(\"cfg-error\")).to_contain_text(\"Exhibit and prefix:\")             # the server's sentence, under the inputs\n        assert api(\"GET\", f\"/api/cases/{tok}/export_config\")[1][\"exhibit\"] is None\n        page.get_by_test_id(\"cfg-exhibit\").fill(\"4\"); page.get_by_test_id(\"cfg-bates-prefix\").fill(\"RIV\"); page.get_by_test_id(\"cfg-bates-start\").fill(\"1\")\n        page.get_by_test_id(\"btn-save-cfg\").click()\n        expect(page.get_by_test_id(\"bar-msg\")).to_have_text(\"Saved. The numbers are in your letter.\")\n        assert \"[Ex. 4 / Bates RIV0001]\" in page.get_by_test_id(\"letter-text\").inner_text()\n        page.get_by_test_id(\"cfg-bates-start\").fill(\"x\"); page.get_by_test_id(\"btn-save-cfg\").click()\n        expect(page.get_by_test_id(\"cfg-error\")).to_have_text(\"The first number must be a whole number, like 1.\")\n        page.reload(); page.locator(\"[data-testid=view][data-ready]\").wait_for(state=\"attached\")\n        assert page.get_by_test_id(\"cfg-exhibit\").input_value() == \"4\"                                 # remembered\n    finally:\n        br.close()\n\n\ndef test_blocked_letter_lists_each_problem_with_the_step_that_fixes_it(pw, made):\n    tok = make_case(f\"Blocked {uid()}\"); made.append(tok)           # drafted, nothing answered: NOTHING_ACCEPTED\n    br, page = browser(pw, 1440, 900)\n    try:\n        seen = watch(page); go(page, f\"/case/{tok}/letter\")           # no refused request: the trace says blocked, the export is not asked for\n        expect(page.get_by_test_id(\"letter-status\")).to_contain_text(\"The letter can't be made yet.\")\n        rows = page.get_by_test_id(\"blocker\"); expect(rows).to_have_count(1)\n        assert rows.first.get_attribute(\"data-code\") == \"DECIDE\"\n        expect(rows.first).to_contain_text(\"Nothing is accepted or edited yet, so the letter would be empty.\")      # the server's sentence, as given\n        b = page.get_by_test_id(\"btn-blocker\"); expect(b).to_have_text(\"Go to step 2\"); assert b.get_attribute(\"href\") == f\"/case/{tok}/timeline\"\n        expect(page.get_by_test_id(\"letter-text\")).to_have_text(\"Your letter will appear here once the problem above is fixed.\")\n        expect(page.get_by_test_id(\"btn-copy-letter\")).to_be_disabled(); expect(page.get_by_test_id(\"btn-download-letter\")).to_be_disabled()\n        assert page.get_by_test_id(\"step-4\").locator(\".st-status\").inner_text() == \"1 problem\"\n        assert in_view(page, page.get_by_test_id(\"btn-copy-letter\"))\n        shot(page, \"step4-blocked\", 1440)\n        assert seen == [], seen\n        page.set_viewport_size({\"width\": 390, \"height\": 844}); assert no_h_scroll(page); shot(page, \"step4-blocked\", 390)\n        b.click(); expect(page).to_have_url(re.compile(r\"/timeline$\"))\n    finally:\n        br.close()\n\n\ndef test_every_blocker_code_gets_its_own_button_or_sentence(pw, made):\n    tok = make_case(f\"Codes {uid()}\", decide=True); made.append(tok)\n    na = lambda code, **t: {\"code\": code, \"text\": \"x\", \"target\": t}\n    blockers = [\n        {\"item_id\": \"e3\", \"kind\": \"entry\", \"reason_code\": \"SUMMARY_NUMBER_NOT_IN_EXCERPT\", \"why\": \"The summary says 8 but the quote says 6.\", \"next_action\": na(\"EDIT_SUMMARY\", item_id=\"e3\")},\n        {\"item_id\": \"e4\", \"kind\": \"entry\", \"reason_code\": \"EXCERPT_NOT_VERBATIM\", \"why\": \"The quote is not in the record.\", \"next_action\": na(\"EDIT_QUOTE\", item_id=\"e4\")},\n        {\"item_id\": \"a2\", \"kind\": \"amount\", \"reason_code\": \"X\", \"why\": \"This amount needs a look.\", \"next_action\": na(\"DISMISS_OR_ENTER_BY_HAND\", item_id=\"a2\")},\n        {\"item_id\": \"e5\", \"kind\": \"entry\", \"reason_code\": \"JUDGE_NOT_RUN\", \"why\": \"This accepted line has no second check.\", \"next_action\": na(\"RERUN_JUDGE\", item_id=\"e5\", judge=\"j1\")},\n        {\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"RUN_FAILED\", \"why\": \"The last run stopped.\", \"next_action\": na(\"CONFIRM_RERUN\")},\n        {\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"RUN_IN_PROGRESS\", \"why\": \"A run is going.\", \"next_action\": na(\"RUN_IN_PROGRESS\")},\n    ]\n    gate = {\"id\": \"export_gate\", \"ready\": False, \"blockers\": blockers}\n    br, page = browser(pw, 1440, 900)\n    try:\n        page.route(f\"**/api/cases/{tok}/trace\", lambda r: jbody(r, 200, {\"token\": tok, \"status\": \"ready\", \"steps\": [gate]}))\n        go(page, f\"/case/{tok}/letter\")\n        rows = page.get_by_test_id(\"blocker\"); expect(rows).to_have_count(6)\n        act = lambda i: rows.nth(i)\n        assert act(0).locator(\"a\").get_attribute(\"href\") == f\"/case/{tok}/timeline?item=e3\" and act(0).locator(\"a\").inner_text() == \"Fix it\"\n        assert act(1).locator(\"a\").get_attribute(\"href\") == f\"/case/{tok}/timeline?item=e4\" and act(1).locator(\"a\").inner_text() == \"Fix it\"\n        assert act(2).locator(\"a\").get_attribute(\"href\") == f\"/case/{tok}/bills?item=a2\" and act(2).locator(\"a\").inner_text() == \"Go to it\"\n        expect(act(3).get_by_test_id(\"blocker-note\")).to_have_text(\"The second check can't run here. Fix the wording in your own words, or leave the item out.\")    # rerun_available is false in demo mode\n        assert act(4).locator(\"a\").get_attribute(\"href\") == f\"/case/{tok}/records\" and act(4).locator(\"a\").inner_text() == \"Go to step 1\"\n        expect(act(5).get_by_test_id(\"blocker-note\")).to_have_text(\"Wait for drafting to finish.\")\n        assert page.get_by_test_id(\"step-4\").locator(\".st-status\").inner_text() == \"6 problems\"\n    finally:\n        br.close()\n\n\ndef test_rerun_the_second_check_when_the_item_can_be_rerun(pw, made):\n    tok = make_case(f\"Rejudge {uid()}\", decide=True); made.append(tok)\n    blockers = [{\"item_id\": \"e5\", \"kind\": \"entry\", \"reason_code\": \"JUDGE_NOT_RUN\", \"why\": \"This accepted line has no second check.\", \"next_action\": {\"code\": \"RERUN_JUDGE\", \"text\": \"x\", \"target\": {\"item_id\": \"e5\", \"judge\": \"j1\"}}}]\n    state = {\"posted\": 0}\n    br, page = browser(pw, 1440, 900)\n    try:\n        def trace(route):\n            if state[\"posted\"]:\n                return route.continue_()\n            jbody(route, 200, {\"token\": tok, \"status\": \"ready\", \"steps\": [{\"id\": \"export_gate\", \"ready\": False, \"blockers\": blockers}]})\n        def case(route):\n            j = route.fetch().json()\n            for i in j[\"entries\"]:\n                if i[\"id\"] == \"e5\":\n                    i[\"rerun_available\"] = True\n            route.fulfill(json=j)\n        def rejudge(route):\n            state[\"posted\"] += 1; jbody(route, 200, {\"token\": tok, \"asked\": 1, \"rejudged\": [], \"still_unavailable\": [], \"export_gate\": {\"ready\": True, \"blockers\": []}})\n        page.route(f\"**/api/cases/{tok}/trace\", trace); page.route(f\"**/api/cases/{tok}\", case); page.route(f\"**/api/cases/{tok}/rejudge\", rejudge)\n        go(page, f\"/case/{tok}/letter\")\n        b = page.get_by_test_id(\"btn-rejudge\"); expect(b).to_have_text(\"Run the second check again\"); b.click()\n        expect(page.get_by_test_id(\"letter-status\")).to_contain_text(\"Your letter is ready.\")      # the gate is re-read after the check\n        assert state[\"posted\"] == 1\n    finally:\n        br.close()\n\n\ndef test_undecided_items_need_one_tick_before_copying_and_the_link_goes_to_the_first(pw, made):\n    tok = make_case(f\"Pending {uid()}\"); made.append(tok)\n    c = api(\"GET\", f\"/api/cases/{tok}\")[1]\n    st, r = api(\"POST\", f\"/api/cases/{tok}/review/batch\", {\"action\": \"accept\", \"item_ids\": [e[\"id\"] for e in c[\"entries\"]]}); assert st == 200, r\n    left = api(\"GET\", f\"/api/cases/{tok}\")[1][\"review\"][\"counts\"]; n = left[\"pending\"] + left[\"edit_to_check\"]\n    br, page = browser(pw, 1440, 900)\n    try:\n        seen = watch(page); go(page, f\"/case/{tok}/letter\")\n        s = page.get_by_test_id(\"letter-status\")\n        expect(s).to_contain_text(f\"{n} items still need a decision.\")\n        expect(s).to_contain_text(\"If you don't decide them, they stay out of the letter.\")\n        first = page.get_by_test_id(\"btn-first-undecided\"); expect(first).to_have_text(\"Go to the first one\")\n        assert first.get_attribute(\"href\") == f\"/case/{tok}/timeline\"        # steps are in order: the first undecided item is in step 2\n        copy, dl = page.get_by_test_id(\"btn-copy-letter\"), page.get_by_test_id(\"btn-download-letter\")\n        expect(copy).to_be_disabled(); expect(dl).to_be_disabled()\n        expect(page.get_by_test_id(\"bar-msg\")).to_contain_text(\"Tick the box above\")\n        assert page.get_by_test_id(\"letter-text\").inner_text().startswith(\"TREATMENT CHRONOLOGY\")          # the preview is what would be sent now\n        tick = page.get_by_test_id(\"check-copy-anyway\"); tick.check()\n        expect(copy).to_be_enabled(); expect(dl).to_be_enabled()\n        copy.click(); expect(copy).to_have_text(\"Copied\")\n        assert page.evaluate(\"navigator.clipboard.readText()\") == api(\"GET\", f\"/api/cases/{tok}/export\")[1][\"letter_text\"]\n        tick.uncheck(); expect(copy).to_be_disabled()\n        assert page.get_by_test_id(\"step-4\").locator(\".st-status\").inner_text() == \"Not yet\"\n        assert seen == [], seen\n        shot(page, \"step4-pending\", 1440)\n    finally:\n        br.close()\n\n\ndef test_provenance_badge_and_no_narrative_anywhere(pw, made):\n    tok = make_case(f\"Prov {uid()}\", decide=True); made.append(tok)\n    hl = api(\"GET\", \"/api/health\")[1]\n    br, page = browser(pw, 1440, 900)\n    try:\n        asked = []\n        page.on(\"request\", lambda r: asked.append(r.url) if \"/narrative\" in r.url else None)\n        go(page, f\"/case/{tok}/letter\")\n        text = page.locator(\"main\").inner_text()\n        assert \"TREATMENT SUMMARY\" not in text and \"treatment paragraph\" not in text.lower() and asked == []\n        if hl[\"answers\"] == \"prepared\":\n            b = page.get_by_test_id(\"prepared-badge\")\n            assert b.get_attribute(\"title\") == \"Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.\"\n            expect(page.locator(\"main\")).to_contain_text(\"Prepared by our team for this demo, not written by an AI model.\")\n        else:\n            expect(page.get_by_test_id(\"prepared-badge\")).to_have_count(0)\n        for jargon in (\"tray\", \"judge\", \"LLM\", \"excerpt\", \"export gate\"):\n            assert jargon not in text.split(\"DO NOT SEND\")[0].split(\"TREATMENT CHRONOLOGY\")[0], jargon      # the page chrome around the two text boxes is plain words\n    finally:\n        br.close()\n\n\ndef test_a_failed_load_says_so_in_a_sentence_and_try_again_works(pw, made):\n    tok = make_case(f\"Offline {uid()}\", decide=True); made.append(tok)\n    br, page = browser(pw, 1440, 900)\n    try:\n        page.route(f\"**/api/cases/{tok}/trace\", lambda r: r.abort())\n        page.route(f\"**/api/cases/{tok}/export\", lambda r: r.abort())\n        go(page, f\"/case/{tok}/letter\")\n        e = page.get_by_test_id(\"page-error\"); expect(e).to_contain_text(\"We couldn't make the letter\")\n        assert \"Failed to fetch\" not in e.inner_text()\n        page.unroute(f\"**/api/cases/{tok}/trace\"); page.unroute(f\"**/api/cases/{tok}/export\")\n        page.get_by_test_id(\"btn-retry\").click()\n        expect(page.get_by_test_id(\"letter-status\")).to_contain_text(\"Your letter is ready.\")\n    finally:\n        br.close()\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_step4.py -q 2>&1 | grep -E \"^(E |FAILED)|passed|failed|test_step4.py:[0-9]+:\" | head -40"
}
````

### User / tool · 2026-11-02T21:42:55.511Z

**tool result**
````
E           AssertionError: Locator expected to have text 'Saved. The numbers are in your letter.'
E           Actual value: Copy this into your demand letter. 
E           Call log:
E             - Expect "to_have_text" get_by_test_id("bar-msg") with timeout 5000ms
E             - waiting for get_by_test_id("bar-msg")
E               2 × locator resolved to <p class="sbar-msg" aria-live="polite" data-testid="bar-msg">Copy this into your demand letter. The [Ex. __ / …</p>
E                 - unexpected value "Copy this into your demand letter. The [Ex. __ / Bates __] blanks are yours to fill in."
E               12 × locator resolved to <p class="sbar-msg" aria-live="polite" data-testid="bar-msg">Copy this into your demand letter.</p>
E                  - unexpected value "Copy this into your demand letter."
E           
E           Aria snapshot:
E           - paragraph: Copy this into your demand letter.
tests/e2e/guided/test_step4.py:107: AssertionError
FAILED tests/e2e/guided/test_step4.py::test_the_letter_blanks_sentence_and_the_exhibit_numbers
1 failed, 8 passed in 24.22s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:43:02.057Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'E'\ns=open('step4.js').read()\ns=s.replace(\"    function draw() {\\n      ctx.layout\",\"    function draw(note) {\\n      ctx.layout\")\ns=s.replace(\"const cfgBox = ready ? cfgPanel(letter, bar, () => { blanksRefresh(); }) : null;\\n      function blanksRefresh() { /* the letter text changed: the blanks sentence follows it */ const b = /\\\\[Ex\\\\. __|Bates __/.test(exp.letter_text); const was = blanks; if (b !== was) { draw(); } }\",\n \"const cfgBox = ready ? cfgPanel(letter, bar, (said) => { /* the letter text changed: the blanks sentence follows it */ if (/\\\\[Ex\\\\. __|Bates __/.test(exp.letter_text) !== blanks) draw(said); else bar.say(said); }) : null;\")\ns=s.replace(\"      gate();\\n    }\\n\\n    function blockerRow\",\"      gate(); if (note) bar.say(note);\\n    }\\n\\n    function blockerRow\")\ns=s.replace(\"letter.textContent = exp.letter_text; changed(); bar.say(\\\"Saved. The numbers are in your letter.\\\"); }\",\"letter.textContent = exp.letter_text; changed(\\\"Saved. The numbers are in your letter.\\\"); }\")\nopen('step4.js','w').write(s)\nE\ngrep -n \"changed\\|blanksRefresh\\|gate(); if\" step4.js | cut -c1-160; cd /Users/arsis/zlayt-pm-project && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_step4.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:43:23.105Z

**tool result**
````
100:      const cfgBox = ready ? cfgPanel(letter, bar, (said) => { /* the letter text changed: the blanks sentence follows it */ if (/\[Ex\. __|Bates __/.test(e
109:      gate(); if (note) bar.say(note);
134:    function cfgPanel(letter, bar, changed) {
144:        try { cfg = await G.api.call("PUT", "/cases/" + encodeURIComponent(token) + "/export_config", body); exp = await G.api.exportCase(token, sig); lette
.........                                                                [100%]
9 passed in 20.02s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:43:26.748Z

**tool call — Bash**
````
{
 "command": "ls tests/e2e | grep -i console; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py -q 2>&1 | tail -8; ls artifacts/screenshots/guided | head -40"
}
````

### User / tool · 2026-11-02T21:45:27.286Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: bovc0ifr4). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bovc0ifr4.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:45:29.026Z

**tool call — Bash**
````
{
 "command": "ls tests/e2e | grep -i \"console\\|no_con\"; sleep 60; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bovc0ifr4.output | tail -8"
}
````

### User / tool · 2026-11-02T21:46:29.157Z

**tool result**
````
test_no_console_errors.py
step2-warning-390.png
step4-blocked-1440.png
step4-blocked-390.png
step4-letter-1440.png
step4-letter-390.png
step4-pending-1440.png

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:46:31.172Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bovc0ifr4.output | head -30"
}
````

### User / tool · 2026-11-02T21:46:31.247Z

**tool result**
````
test_no_console_errors.py
FAILED tests/e2e/guided/test_shell_smoke.py::test_links_route_without_a_reload_and_back_and_deep_links_work
FAILED tests/e2e/guided/test_step2.py::test_fix_the_wording_refusal_stays_in_the_footer_and_a_good_edit_asks_for_the_compare
FAILED tests/e2e/guided/test_step2.py::test_changing_the_highlighted_sentences_sends_the_quote_and_wording_together
FAILED tests/e2e/guided/test_step2.py::test_a_record_with_no_line_can_be_written_by_hand_from_whole_sentences
FAILED tests/e2e/guided/test_step2.py::test_keyboard_a_d_e_and_the_arrow_keys
FAILED tests/e2e/guided/test_step2.py::test_the_done_screen_says_when_some_items_are_still_undecided
FAILED tests/e2e/guided/test_step2.py::test_nothing_moves_when_she_answers_or_changes_mode_and_the_primary_action_is_above_the_fold[390-844]
7 failed, 73 passed in 142.93s (0:02:22)
home-1440.png
home-390.png
home-empty-1440.png
new-demo-1440.png
new-demo-390.png
step1-add-live-390.png
step1-done-1440.png
step1-drafting-1440.png
step1-failed-1440.png
step1-found-1440.png
step1-found-390.png
step2-date-1440.png
step2-date-390.png
step2-disputed-1440.png
step2-disputed-390.png
step2-done-1440.png
step2-done-390.png
step2-entry-1440.png
step2-entry-390.png
step2-fix-1440.png
step2-fix-390.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:46:33.177Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_shell_smoke.py -q -k links_route 2>&1 | grep -E \"^(E|>)|test_shell_smoke.py:[0-9]+\" | head -15"
}
````

### User / tool · 2026-11-02T21:47:06.060Z

**tool result**
````
>       page.get_by_test_id("btn-next").click()
tests/e2e/guided/test_shell_smoke.py:148: 
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
E           Call log:
E             - waiting for get_by_test_id("btn-next")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:47:08.594Z

**tool call — Bash**
````
{
 "command": "sed -n 135,175p tests/e2e/guided/test_shell_smoke.py | cut -c1-230; git status --short tests/e2e/guided | head"
}
````

### User / tool · 2026-11-02T21:47:08.693Z

**tool result**
````
                assert rect(page, ".actions")[1] + rect(page, ".actions")[3] == h, f"the action bar is not at the bottom at {w}: {path}"
        b = rect(page, "[data-testid=step-bar]"); assert b[3] > 0
        for n in (1, 2, 3, 4):
            sb = page.get_by_test_id(f"step-{n}").bounding_box(); assert sb and sb["x"] >= 0 and sb["x"] + sb["width"] <= w, (w, n, sb)


def test_links_route_without_a_reload_and_back_and_deep_links_work(page, sample_case):
    seen = watch(page)
    go(page, case_paths(sample_case)[0])
    page.evaluate("window.__marker = 42")
    page.get_by_test_id("step-3").click()
    expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "bills")
    assert page.url.endswith(f"/case/{sample_case}/bills") and page.evaluate("window.__marker") == 42, "a click must not reload the page"
    page.get_by_test_id("btn-next").click()
    expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "letter")
    page.go_back(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "bills")
    page.go_back(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "records")
    assert page.evaluate("window.__marker") == 42
    page.get_by_test_id("btn-your-cases").click()
    expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "home"); expect(page.get_by_test_id("step-bar")).to_be_hidden()
    go(page, f"/case/{sample_case}/timeline?item=e3")                 # a reload of a deep link lands on the same screen
    assert page.locator("[data-testid=view]").get_attribute("data-route") == "timeline" and page.evaluate("location.search") == "?item=e3"
    go(page, f"/case/{sample_case}")                                  # a bare case link opens step 1
    assert page.url.endswith(f"/case/{sample_case}/records")
    assert seen == [], seen


def test_bad_links_and_unknown_cases_are_plain(page):
    seen = watch(page, allow_404=("/api/cases/",))
    go(page, "/nonsense/here")
    assert "couldn't find that page" in page.get_by_test_id("page-title").inner_text()
    page.get_by_test_id("link-home").click(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "home")
    go(page, "/case/does-not-exist/timeline")
    assert "no longer here" in page.get_by_test_id("page-title").inner_text()
    body = page.locator("body").inner_text()
    assert "Failed to fetch" not in body and "404" not in body
    expect(page.get_by_test_id("link-home")).to_be_visible(); expect(page.get_by_test_id("step-bar")).to_be_visible()
    assert [s for s in seen if "does-not-exist" not in s and "Failed to load resource" not in s] == [], seen


def test_theme_button_switches_between_light_and_dark(page):
?? tests/e2e/guided/_helpers.py
?? tests/e2e/guided/test_golden_path.py
?? tests/e2e/guided/test_home.py
?? tests/e2e/guided/test_step1.py
?? tests/e2e/guided/test_step2.py
?? tests/e2e/guided/test_step4.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:47:12.142Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/frontend/feedback_verify_from_archive.md; git status --short app/frontend tests | head -20"
}
````

### User / tool · 2026-11-02T21:47:12.242Z

**tool result**
````
---
name: verify-from-git-archive
description: Verify a frontend commit from a git archive of the commit tree, never the dirty tree; temp-index commit recipe and the confirm-dialog Escape race
metadata:
  type: feedback
---

Run e2e from `git archive <tree>` (tree from `GIT_INDEX_FILE=tmp git write-tree`) with `E2E_REQUIRE_DB=1`; a plain pytest there starts its own private server on a free port.

**Why:** T-154 r2 committed the a-key guard inside mountSection() (ReferenceError on every case load) while 12/12 passed on the dirty tree where other workers' hunks and the guard sat elsewhere. tests/e2e/test_no_console_errors.py now fails CI on any pageerror.

**How to apply:** build the commit with a temp index (`git read-tree HEAD`, `update-index --cacheinfo` for a file with others' hunks, `--add` for my own files); the check_stale_index hook blocks it if HEAD moved, so re-read-tree and recheck `git diff --stat OLD HEAD -- app/frontend tests/e2e`. The shared scratchpad has many dirs named arch/head0/etc; use a fresh name with mkdir -p.

Pitfall: ZL.confirmCharge (charges.js) must settle on the `cancel` event and ignore a stale `close` when the dialog is open again, else Escape then `a` is dropped (item still busy) or the reopened window is shut.
MM app/frontend/api.js
MM app/frontend/app.js
MM app/frontend/audit.js
MM app/frontend/batch.js
MM app/frontend/charges.js
MM app/frontend/dom.js
MM app/frontend/export.js
MM app/frontend/flags.js
 M app/frontend/guided/home.css
 M app/frontend/guided/home.js
 M app/frontend/guided/review.css
 M app/frontend/guided/review.js
 M app/frontend/guided/step1.css
 M app/frontend/guided/step1.js
 M app/frontend/guided/step2.css
 M app/frontend/guided/step2.js
 M app/frontend/guided/step3.css
 M app/frontend/guided/step3.js
 M app/frontend/guided/step4.css
 M app/frontend/guided/step4.js
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:47:20.442Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/zla-index && rm -f $GIT_INDEX_FILE && git read-tree HEAD && FILES=\"app/frontend/guided/home.js app/frontend/guided/home.css app/frontend/guided/step1.js app/frontend/guided/step1.css app/frontend/guided/step4.js app/frontend/guided/step4.css tests/e2e/guided/_helpers.py tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_golden_path.py\" && for f in $FILES artifacts/screenshots/guided/home-1440.png artifacts/screenshots/guided/home-390.png artifacts/screenshots/guided/home-empty-1440.png artifacts/screenshots/guided/new-demo-1440.png artifacts/screenshots/guided/new-demo-390.png artifacts/screenshots/guided/step1-*.png artifacts/screenshots/guided/step4-*.png; do git update-index --add $f; done && TREE=$(git write-tree) && echo $TREE && unset GIT_INDEX_FILE && A=/private/tmp/claude-501/arch-a-$$ && mkdir -p $A && git archive $TREE | tar -x -C $A && ls $A | head -3 && ln -s /Users/arsis/zlayt-pm-project/.venv $A/.venv 2>/dev/null; echo $A > /private/tmp/claude-501/arch-dir; echo $TREE > /private/tmp/claude-501/tree"
}
````

### User / tool · 2026-11-02T21:47:23.480Z

**tool result (error)**
````
Exit code 1
3368d2feaabd59f921a596e4ca30835d12050949
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
/bin/bash: /private/tmp/claude-501/tree: Is a directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:47:25.487Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/arch-a-* && pwd && ls -d .venv; (E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_shell_smoke.py tests/e2e/test_no_console_errors.py -q -p no:cacheprovider > /private/tmp/claude-501/arch-run.txt 2>&1; tail -8 /private/tmp/claude-501/arch-run.txt)"
}
````

### User / tool · 2026-11-02T21:48:32.658Z

**tool result**
````
/private/tmp/claude-501/arch-a-19124
.venv
E           Call log:
E             - Expect "to_have_count" get_by_test_id("cases-finished").locator("[data-token=4rgclwTUTAEl4saPjGpSfQ]") with timeout 5000ms
E             - waiting for get_by_test_id("cases-finished").locator("[data-token=4rgclwTUTAEl4saPjGpSfQ]")

tests/e2e/guided/test_home.py:66: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_home.py::test_real_cases_show_the_next_line_the_track_and_where_continue_goes
1 failed, 50 passed in 66.17s (0:01:06)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:48:35.374Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/arch-a-* && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -p no:cacheprovider -k real_cases 2>&1 | tail -5; cd /Users/arsis/zlayt-pm-project && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -k real_cases 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:48:41.660Z

**tool result**
````
.                                                                        [100%]
1 passed, 7 deselected in 1.99s
.                                                                        [100%]
1 passed, 7 deselected in 2.24s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:48:44.701Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/arch-a-* && for i in 1 2; do E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q -p no:cacheprovider 2>&1 | tail -3; done"
}
````

### User / tool · 2026-11-02T21:49:10.350Z

**tool result**
````
........                                                                 [100%]
8 passed in 11.64s
........                                                                 [100%]
8 passed in 12.05s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:16.940Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\nold=\"\"\"        fin = page.get_by_test_id(\"cases-finished\")\n        expect(fin.locator(f\"[data-token={c}]\")).to_have_count(1)\"\"\"\nnew=\"\"\"        fin = page.get_by_test_id(\"cases-finished\")\n        for _ in range(3):             # one cold first read of a server can still be settling the gate: look again before judging\n            if fin.locator(f\"[data-token={c}]\").count() == 1:\n                break\n            page.wait_for_timeout(1500); go(page, \"/\")\n        expect(fin.locator(f\"[data-token={c}]\")).to_have_count(1, msg=cc.inner_text() if cc.count() else \"no card\")\"\"\"\nassert old in s\nopen(p,'w').write(s.replace(old,new))\nE\nsed -n 1,3p /private/tmp/claude-501/arch-run.txt | head -2; grep -n \"Error\\|assert\" /private/tmp/claude-501/arch-run.txt | head"
}
````

### User / tool · 2026-11-02T21:49:17.046Z

**tool result**
````
F..................................................                      [100%]
=================================== FAILURES ===================================
20:            assert ca.get_by_test_id("btn-continue").get_attribute("href") == f"/case/{a}/records"
21:            assert ca.locator(".track li").evaluate_all("els => els.map(e => e.className)") == ["current", "", "", ""]
24:            assert cb.get_by_test_id("btn-continue").get_attribute("href") == f"/case/{b}/timeline"
25:            assert cb.locator(".track li").evaluate_all("els => els.map(e => e.className)") == ["done", "current", "", ""]
29:E           AssertionError: Locator expected to have count '1'
31:E           Error: SyntaxError: Failed to execute 'querySelectorAll' on 'Element': '[data-token=4rgclwTUTAEl4saPjGpSfQ]' is not a valid selector.
46:tests/e2e/guided/test_home.py:66: AssertionError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:20.596Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='tests/e2e/guided/test_home.py'; s=open(p).read()\ns=s.replace('[data-token={c}]','[data-token=\"{c}\"]').replace('[data-token={new}]','[data-token=\"{new}\"]').replace(\"[data-token=a-token-that-is-gone]\",'[data-token=\"a-token-that-is-gone\"]')\n# revert the retry loop: it was not the cause\ni=s.index(\"        for _ in range(3):             # one cold\"); j=s.index(\"        expect(fin.locator(f\\\"[data-token=\\\"{c}\\\"]\\\")).to_have_count(1, msg\")\ns=s[:i]+s[j:]\ns=re.sub(r'to_have_count\\(1, msg=cc\\.inner_text\\(\\) if cc\\.count\\(\\) else \"no card\"\\)','to_have_count(1)',s)\nopen(p,'w').write(s)\nE\ngrep -n 'data-token' tests/e2e/guided/*.py | grep -v '\"{' | head; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:49:21.760Z

**tool result**
````
tests/e2e/guided/test_home.py:2:Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, cases-loading, cases-mode, case-card (data-token, data-title, data-finished), case-next, btn-continue, btn-rename, btn-delete,
tests/e2e/guided/test_home.py:247:        gone = page.locator("[data-testid=case-card][data-token="a-token-that-is-gone"]")
ERROR tests/e2e/guided/test_home.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.11s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:23.612Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\ns=s.replace('\"[data-testid=case-card][data-token=\"a-token-that-is-gone\"]\"','\\'[data-testid=case-card][data-token=\"a-token-that-is-gone\"]\\'')\nopen(p,'w').write(s)\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:49:24.798Z

**tool result**
````
ERROR tests/e2e/guided/test_home.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.10s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:26.074Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m py_compile tests/e2e/guided/test_home.py 2>&1 | head -5; grep -n 'data-token' tests/e2e/guided/test_home.py | cut -c1-170"
}
````

### User / tool · 2026-11-02T21:49:26.187Z

**tool result**
````
  File "tests/e2e/guided/test_home.py", line 66
    expect(fin.locator(f"[data-token="{c}"]")).to_have_count(1)
                       ^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
2:Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, cases-loading, cases-mode, case-card (data-token, data-title, data-finished), case-nex
66:        expect(fin.locator(f"[data-token="{c}"]")).to_have_count(1)
72:        assert page.get_by_test_id("cases-list").locator(f"[data-token="{c}"]").count() == 0
247:        gone = page.locator('[data-testid=case-card][data-token="a-token-that-is-gone"]')
260:        expect(page.locator(f"[data-token="{new}"]")).to_have_count(1)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:28.188Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/guided/test_home.py'; s=open(p).read()\nfor v in (\"c\",\"new\"):\n    s=s.replace('f\"[data-token=\"{%s}\"]\"'%v, 'f\\'[data-token=\"{%s}\"]\\''%v)\nopen(p,'w').write(s)\nE\n.venv/bin/python -m py_compile tests/e2e/guided/test_home.py && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:49:40.937Z

**tool result**
````
FAILED tests/e2e/guided/test_home.py::test_real_cases_show_the_next_line_the_track_and_where_continue_goes
FAILED tests/e2e/guided/test_home.py::test_empty_loading_and_error_states - A...
2 failed, 6 passed in 11.65s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:42.289Z

**tool call — Bash**
````
{
 "command": "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py -q 2>&1 | grep -E \"^E|^>\" | head -12"
}
````

### User / tool · 2026-11-02T21:49:55.020Z

**tool result**
````
>           assert seen == [], seen
E           AssertionError: ["pageerror: Unexpected identifier 'h'"]
E           assert ["pageerror: ...entifier 'h'"] == []
E             
E             Left contains one more item: "pageerror: Unexpected identifier 'h'"
E             Use -v to get more diff
>           assert [s for s in seen if "500" not in s] == [], seen        # the only noise allowed is the stubbed 500 resource line
E           AssertionError: ["pageerror: Unexpected identifier 'h'", "pageerror: Unexpected identifier 'h'", 'http 500: http://127.0.0.1:49576/api/cases', 'console.error: Failed to load resource: the server responded with a status of 500 (Internal Server Error)']
E           assert ["pageerror: ...entifier 'h'"] == []
E             
E             Left contains 2 more items, first extra item: "pageerror: Unexpected identifier 'h'"
E             Use -v to get more diff
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:57.247Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && for f in *.js; do node -e \"try{new Function(require('fs').readFileSync('$f','utf8'))}catch(e){console.log('$f',e.message)}\"; done"
}
````

### User / tool · 2026-11-02T21:49:57.649Z

**tool result**
````
step3.js Unexpected identifier 'h'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:02.276Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/zla-index && rm -f $GIT_INDEX_FILE && git read-tree HEAD && for f in app/frontend/guided/home.js app/frontend/guided/home.css app/frontend/guided/step1.js app/frontend/guided/step1.css app/frontend/guided/step4.js app/frontend/guided/step4.css tests/e2e/guided/_helpers.py tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_golden_path.py artifacts/screenshots/guided/home-1440.png artifacts/screenshots/guided/home-390.png artifacts/screenshots/guided/home-empty-1440.png artifacts/screenshots/guided/new-demo-1440.png artifacts/screenshots/guided/new-demo-390.png artifacts/screenshots/guided/step1-*.png artifacts/screenshots/guided/step4-*.png; do git update-index --add $f; done; TREE=$(git write-tree); unset GIT_INDEX_FILE; echo $TREE; rm -rf /private/tmp/claude-501/arch-b && mkdir -p /private/tmp/claude-501/arch-b && git archive $TREE | tar -x -C /private/tmp/claude-501/arch-b && ln -s /Users/arsis/zlayt-pm-project/.venv /private/tmp/claude-501/arch-b/.venv; cd /private/tmp/claude-501/arch-b && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_shell_smoke.py tests/e2e/test_no_console_errors.py -q -p no:cacheprovider 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T21:50:17.635Z

**tool result (error)**
````
Permission to use Bash with command export GIT_INDEX_FILE=/private/tmp/claude-501/zla-index && rm -f $GIT_INDEX_FILE && git read-tree HEAD && for f in app/frontend/guided/home.js app/frontend/guided/home.css app/frontend/guided/step1.js app/frontend/guided/step1.css app/frontend/guided/step4.js app/frontend/guided/step4.css tests/e2e/guided/_helpers.py tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_golden_path.py artifacts/screenshots/guided/home-1440.png artifacts/screenshots/guided/home-390.png artifacts/screenshots/guided/home-empty-1440.png artifacts/screenshots/guided/new-demo-1440.png artifacts/screenshots/guided/new-demo-390.png artifacts/screenshots/guided/step1-*.png artifacts/screenshots/guided/step4-*.png; do git update-index --add $f; done; TREE=$(git write-tree); unset GIT_INDEX_FILE; echo $TREE; rm -rf /private/tmp/claude-501/arch-b && mkdir -p /private/tmp/claude-501/arch-b && git archive $TREE | tar -x -C /private/tmp/claude-501/arch-b && ln -s /Users/arsis/zlayt-pm-project/.venv /private/tmp/claude-501/arch-b/.venv; cd /private/tmp/claude-501/arch-b && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_shell_smoke.py tests/e2e/test_no_console_errors.py -q -p no:cacheprovider 2>&1 | tail -5 has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:21.975Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/zla-index2 && git read-tree HEAD && for f in app/frontend/guided/home.js app/frontend/guided/home.css app/frontend/guided/step1.js app/frontend/guided/step1.css app/frontend/guided/step4.js app/frontend/guided/step4.css tests/e2e/guided/_helpers.py tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_golden_path.py artifacts/screenshots/guided/home-1440.png artifacts/screenshots/guided/home-390.png artifacts/screenshots/guided/home-empty-1440.png artifacts/screenshots/guided/new-demo-1440.png artifacts/screenshots/guided/new-demo-390.png artifacts/screenshots/guided/step1-*.png artifacts/screenshots/guided/step4-*.png; do git update-index --add $f; done; TREE=$(git write-tree); unset GIT_INDEX_FILE; echo $TREE > /private/tmp/claude-501/tree.txt; D=/private/tmp/claude-501/arch-c-$$; mkdir -p $D && git archive $TREE | tar -x -C $D && ln -s /Users/arsis/zlayt-pm-project/.venv $D/.venv; echo $D; cd $D && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_home.py tests/e2e/guided/test_step1.py tests/e2e/guided/test_step4.py tests/e2e/guided/test_shell_smoke.py tests/e2e/test_no_console_errors.py -q -p no:cacheprovider 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T21:51:40.651Z

**tool result**
````
/private/tmp/claude-501/arch-c-26715
...................................................                      [100%]
51 passed in 60.85s (0:01:00)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:47.683Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -2 && GIT_INDEX_FILE=/private/tmp/claude-501/zla-index2 git commit -q -m \"feat(frontend): T-181 guided Home, Step 1 (Add records) and Step 4 (Get your letter) + e2e\n\nYour cases (local list or this browser's cases in public mode, Next line, rename, delete, search), Step 1 (name, paste/upload/sample/test case with demo mode explained and Paste/Upload disabled, plain errors incl. 413/429, found/drafting/done/stopped), Step 4 (blockers back to the step that fixes each, Copy/Download in a sticky bar, exhibit numbers, no narrative per D-067). D-065 provenance badge. Specs: test_home, test_step1, test_step4, test_golden_path (needs Step 2).\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && SHA=$(git rev-parse --short HEAD) && echo $SHA && git show --stat --oneline HEAD | tail -30 | head -40 && python3 tools/board.py commit T-181 --sha $SHA --agent frontend && python3 tools/board.py note T-181 --agent frontend --text \"frontend-A: COMMITTED $SHA (Home + Step 1 + Step 4, 4 specs). Verified from a git archive of the commit tree with E2E_REQUIRE_DB=1: test_home + test_step1 + test_step4 + test_shell_smoke + test_no_console_errors = 51 passed. test_golden_path::test_demo_sample_reachable_from_root passes in the working tree with Builder B's step 2 but needs it (HEAD still has the stub). Notes for the shell owner: (1) app.js drawBanner footer shows the text 'null' (replaceChildren(null) stringifies); (2) test_shell_smoke::test_links_route... clicks btn-next on the bills page, which is Builder B's page now. Screenshots at 1440/390 in artifacts/screenshots/guided/ (home, home-empty, new-demo, step1-*, step4-*). Shared: G.sbar (sticky action bar, step1.js, CSS in step1.css), G.cases (home.js), G.longDate.\""
}
````

### User / tool · 2026-11-02T21:52:27.062Z

**tool result**
````
fa4f79e fix(qa): T-187 r3 prompt-log redaction: escaped forms, outside-repo omission, third-party and personal names, self-test
f17c991 feat(backend): T-179 D-066 disputed accept needs compared:true (422 COMPARE_REQUIRED, stored on the accept event, batch excludes); D-067 narrative never reaches letter or notes; classic keeps compare button, narrative hidden
check_secrets: ok (27 file(s) scanned staged)
848bbad
848bbad feat(frontend): T-181 guided Home, Step 1 (Add records) and Step 4 (Get your letter) + e2e
 app/frontend/guided/home.css                       |  27 +-
 app/frontend/guided/home.js                        | 200 ++++++++++-
 app/frontend/guided/step1.css                      |  69 +++-
 app/frontend/guided/step1.js                       | 302 +++++++++++++++-
 app/frontend/guided/step4.css                      |  28 +-
 app/frontend/guided/step4.js                       | 160 ++++++++-
 artifacts/screenshots/guided/home-1440.png         | Bin 0 -> 73454 bytes
 artifacts/screenshots/guided/home-390.png          | Bin 0 -> 60814 bytes
 artifacts/screenshots/guided/home-empty-1440.png   | Bin 0 -> 81421 bytes
 artifacts/screenshots/guided/new-demo-1440.png     | Bin 0 -> 133997 bytes
 artifacts/screenshots/guided/new-demo-390.png      | Bin 0 -> 66502 bytes
 .../screenshots/guided/step1-add-live-390.png      | Bin 0 -> 61094 bytes
 artifacts/screenshots/guided/step1-done-1440.png   | Bin 0 -> 118576 bytes
 .../screenshots/guided/step1-drafting-1440.png     | Bin 0 -> 116582 bytes
 artifacts/screenshots/guided/step1-failed-1440.png | Bin 0 -> 138071 bytes
 artifacts/screenshots/guided/step1-found-1440.png  | Bin 0 -> 115398 bytes
 artifacts/screenshots/guided/step1-found-390.png   | Bin 0 -> 67789 bytes
 .../screenshots/guided/step4-blocked-1440.png      | Bin 0 -> 117232 bytes
 artifacts/screenshots/guided/step4-blocked-390.png | Bin 0 -> 79929 bytes
 artifacts/screenshots/guided/step4-letter-1440.png | Bin 0 -> 193869 bytes
 artifacts/screenshots/guided/step4-letter-390.png  | Bin 0 -> 78740 bytes
 .../screenshots/guided/step4-pending-1440.png      | Bin 0 -> 185343 bytes
 tests/e2e/guided/_helpers.py                       |  87 +++++
 tests/e2e/guided/test_golden_path.py               |  30 ++
 tests/e2e/guided/test_home.py                      | 276 +++++++++++++++
 tests/e2e/guided/test_step1.py                     | 386 +++++++++++++++++++++
 tests/e2e/guided/test_step4.py                     | 259 ++++++++++++++
 27 files changed, 1804 insertions(+), 20 deletions(-)
T-181: commit 848bbad recorded
noted on T-181
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:34.933Z

**tool call — Bash**
````
{
 "command": "kill $(cat /private/tmp/claude-501/zla-pid) $(cat /private/tmp/claude-501/zlb-pid) 2>&1 | head -2; cat > /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t181_builder_a.md <<'E'\n---\nname: t181-builder-a-home-step1-step4\ndescription: T-181 Builder A (Home, Step 1, Step 4) hooks, shared helpers (G.sbar, G.cases), pitfalls found while building and testing\nmetadata:\n  type: project\n---\n\nHome/Step 1/Step 4 live in app/frontend/guided/{home,step1,step4}.js; specs tests/e2e/guided/{test_home,test_step1,test_step4,test_golden_path}.py + _helpers.py.\nShared: `G.sbar(msg, primary, ...statics)` (step1.js, CSS in step1.css) = sticky bottom action bar for page-layout screens (primary always above the fold; dynamic follow-up buttons go in `.alts()` slot, which grows LEFT of the primary so the primary never moves); `G.cases` (home.js) = tokens started in this browser (localStorage `zl.guided.cases`), used for public mode where GET /api/cases is 404.\n**Pitfalls:** `el.replaceChildren(a, null)` writes the text \"null\" (use a filtering helper); `[data-token=<token>]` unquoted selector breaks when a token starts with a digit; GET /export 422 shows as a console error, so Step 4 reads GET /trace's `export_gate` first and only calls export when ready (test_no_console_errors visits /letter of an undecided case); the e2e server is local mode with demo_mode true (no ENABLE_LIVE), so paste/upload specs run against a private ENABLE_LIVE=1 + LLM_BACKEND=claude-cli server (ingest only, never run); a confirm row must keep the card height (min-height on `.cc-bottom`).\n**Demo mode rule:** Paste/Upload tiles stay visible but aria-disabled with \"Not available in this demo.\" as text; library tile only when GET /api/library answers (local mode).\nE\necho \"- [T-181 Builder A: Home/Step 1/Step 4](project_t181_builder_a.md) — G.sbar, G.cases, trace-before-export, demo-mode tiles, pitfalls\" >> /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/MEMORY.md"
}
````

### User / tool · 2026-11-02T21:52:34.988Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: kill $(cat /private/tmp/claude-501/zla-pid) $(cat /private/tmp/claude-501/zlb-pid) 2>&1 | head -2; cat > /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t181_builder_a.md <<'E'
---
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:39.055Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t181_builder_a.md",
 "content": "---\nname: t181-builder-a-home-step1-step4\ndescription: T-181 Builder A (Home, Step 1, Step 4) hooks, shared helpers (G.sbar, G.cases), pitfalls found while building and testing\nmetadata:\n  type: project\n---\n\nHome/Step 1/Step 4 live in app/frontend/guided/{home,step1,step4}.js; specs tests/e2e/guided/{test_home,test_step1,test_step4,test_golden_path}.py + _helpers.py.\nShared: `G.sbar(msg, primary, ...statics)` (step1.js, CSS in step1.css) = sticky bottom action bar for page-layout screens (primary always above the fold; dynamic follow-up buttons go in `.alts()` slot, which grows LEFT of the primary so the primary never moves); `G.cases` (home.js) = tokens started in this browser (localStorage `zl.guided.cases`), used for public mode where GET /api/cases is 404.\n\n**Pitfalls:** `el.replaceChildren(a, null)` writes the text \"null\" (use a filtering helper); `[data-token=<token>]` unquoted selector breaks when a token starts with a digit; GET /export 422 shows as a console error, so Step 4 reads GET /trace's `export_gate` first and only calls export when ready (test_no_console_errors visits /letter of an undecided case); the e2e server is local mode with demo_mode true (no ENABLE_LIVE), so paste/upload specs run against a private ENABLE_LIVE=1 + LLM_BACKEND=claude-cli server (ingest only, never run); a confirm row must keep the card height (min-height on `.cc-bottom`).\n\n**Demo mode rule:** Paste/Upload tiles stay visible but aria-disabled with \"Not available in this demo.\" as text; the library tile shows only when GET /api/library answers (local mode).\n"
}
````

### User / tool · 2026-11-02T21:52:39.105Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t181_builder_a.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:40.014Z

**tool call — Bash**
````
{
 "command": "echo \"- [T-181 Builder A: Home/Step 1/Step 4](project_t181_builder_a.md) — G.sbar, G.cases, trace-before-export, demo-mode tiles, pitfalls\" >> .claude/agent-memory/frontend/MEMORY.md; cat /private/tmp/claude-501/zla-pid /private/tmp/claude-501/zlb-pid"
}
````

### User / tool · 2026-11-02T21:52:40.101Z

**tool result**
````
91430
5289
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:40.919Z

**tool call — Bash**
````
{
 "command": "kill 91430 5289; echo done"
}
````

### User / tool · 2026-11-02T21:52:40.994Z

**tool result**
````
done
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:44.032Z

Home, Step 1 and Step 4 are committed as `848bbad` and noted on T-181. From a `git archive` copy with `E2E_REQUIRE_DB=1`, test_home, test_step1, test_step4, the shell smoke and test_no_console_errors passed (51). The golden-path test (`test_golden_path.py::test_demo_sample_reachable_from_root`) passes in my working tree with Builder B's Step 2 but fails in the committed tree, whose Step 2 is still the stub, so it only goes green once Builder B commits.

Two shell issues are noted on T-181 for the shell owner: the footer prints the text "null" (`replaceChildren(null)` in `app.js`), and `test_shell_smoke::test_links_route…` clicks `btn-next` on the bills page, which is Builder B's page now. Builder B's `step3.js` also had a JS syntax error in the working tree when I last checked.

Screenshots at 1440 and 390 are in `/Users/arsis/zlayt-pm-project/artifacts/screenshots/guided/`.

### User / tool · 2026-11-02T21:52:47.667Z

The coordinator sent a message while you were working:
Orchestrator here. You're now the shell owner for this fix: change `replaceChildren(null)` in app.js so the footer never prints "null", and add an assertion for it to test_shell_smoke. Leave the `btn-next` bills-page test to Builder B; I'll pass it on. Commit only app.js and test_shell_smoke.py through a temp index, verified from a git archive copy. Reply in 1 line.

Address this before completing your current task.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:49.285Z

**tool call — Bash**
````
{
 "command": "grep -n \"replaceChildren\" app/frontend/guided/app.js | cut -c1-200; git status --short app/frontend/guided/app.js tests/e2e/guided/test_shell_smoke.py; git log --oneline | head -3"
}
````

### User / tool · 2026-11-02T21:52:49.466Z

**tool result**
````
53:    const f = $("#footer"); f.replaceChildren(h("span", { "data-testid": "footer-note" }, p.label ? p.label + ". " + p.note : p.note),
63:    headerEl.replaceChildren(...[].concat(left), h("span", { class: "spacer" }), ...(p.label ? [h("span", { class: "demo-pill", "data-testid": "demo-badge", title: p.note }, p.label)] : []), themeB
75:    list.replaceChildren(...st.map((s, i) => {
106:    view.replaceChildren(); view.removeAttribute("data-ready"); view.dataset.route = r.name;
126:          view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, () => render(), e.status === 404 ? "This case is no longer here" : "We couldn't open this case")));
139:      setLayout("page"); view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, () => render(), "Something went wrong")));
848bbad feat(frontend): T-181 guided Home, Step 1 (Add records) and Step 4 (Get your letter) + e2e
fa4f79e fix(qa): T-187 r3 prompt-log redaction: escaped forms, outside-repo omission, third-party and personal names, self-test
f17c991 feat(backend): T-179 D-066 disputed accept needs compared:true (422 COMPARE_REQUIRED, stored on the accept event, batch excludes); D-067 narrative never reaches letter or notes; classic keeps compare button, narrative hidden
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:51.042Z

**tool call — Bash**
````
{
 "command": "sed -n 53,54p app/frontend/guided/app.js | cut -c1-300"
}
````

### User / tool · 2026-11-02T21:52:51.195Z

**tool result**
````
    const f = $("#footer"); f.replaceChildren(h("span", { "data-testid": "footer-note" }, p.label ? p.label + ". " + p.note : p.note),
      p.hours ? h("span", { class: "f-live" }, `Pasted text is deleted after ${p.hours} hours.`) : null);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:56.008Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/frontend/guided/app.js'; s=open(p).read()\ns=s.replace('''const f = $(\"#footer\"); f.replaceChildren(h(\"span\", { \"data-testid\": \"footer-note\" }, p.label ? p.label + \". \" + p.note : p.note),\n      p.hours ? h(\"span\", { class: \"f-live\" }, `Pasted text is deleted after ${p.hours} hours.`) : null);''','''const f = $(\"#footer\"); f.replaceChildren(...[h(\"span\", { \"data-testid\": \"footer-note\" }, p.label ? p.label + \". \" + p.note : p.note),\n      p.hours ? h(\"span\", { class: \"f-live\" }, `Pasted text is deleted after ${p.hours} hours.`) : null].filter(Boolean));     // replaceChildren(null) would print the text \"null\"''')\nopen(p,'w').write(s)\np='tests/e2e/guided/test_shell_smoke.py'; s=open(p).read()\ns+='''\n\ndef test_footer_and_chrome_never_print_the_word_null(page, sample_case):\n    \"\"\"replaceChildren(a, null) writes the text \"null\": the footer (no retention sentence in demo mode) and the rest of the chrome must not.\"\"\"\n    for path in (\"/\", \"/new\", f\"/case/{sample_case}/records\"):\n        go(page, path)\n        for sel in (\"#footer\", \"#header\", \"[data-testid=banner-synthetic]\", \"[data-testid=step-bar]\"):\n            assert \"null\" not in page.locator(sel).inner_text().lower().split(), (path, sel)\n        assert page.get_by_test_id(\"footer-note\").count() == 1 and page.locator(\"#footer\").evaluate(\"e => e.childNodes.length\") == (2 if C.api(\"GET\", \"/api/health\")[1][\"demo_mode\"] is False else 1)\n'''\nopen(p,'w').write(s)\nE\nE2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_shell_smoke.py -q -k null 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:53:01.268Z

**tool result**
````
.                                                                        [100%]
1 passed, 12 deselected in 3.68s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:53:04.451Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/zla-index3 && git read-tree HEAD && git update-index --add app/frontend/guided/app.js tests/e2e/guided/test_shell_smoke.py && TREE=$(git write-tree) && unset GIT_INDEX_FILE && D=/private/tmp/claude-501/arch-d-$$ && mkdir -p $D && git archive $TREE | tar -x -C $D && ln -s /Users/arsis/zlayt-pm-project/.venv $D/.venv && cd $D && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided/test_shell_smoke.py tests/e2e/guided/test_home.py tests/e2e/test_no_console_errors.py -q -p no:cacheprovider 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T21:55:20.765Z

**tool result**
````
.........................                                                [100%]
25 passed in 98.88s (0:01:38)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:55:23.348Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/zla-index3 git commit -q -m \"fix(frontend): T-181 shell footer never prints the word null; smoke asserts it\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && SHA=$(git rev-parse --short HEAD) && python3 tools/board.py commit T-181 --sha $SHA --agent frontend && python3 tools/board.py note T-181 --agent frontend --text \"frontend (shell owner): $SHA footer 'null' fixed in app.js (filter before replaceChildren) + test_footer_and_chrome_never_print_the_word_null in test_shell_smoke; verified from a git archive: smoke + test_home + test_no_console_errors 25 passed. btn-next bills test left to Builder B.\""
}
````

### User / tool · 2026-11-02T21:56:03.211Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
T-181: commit 3944cc2 recorded
noted on T-181
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:56:04.564Z

The footer no longer prints "null". `app.js` now filters empty children before `replaceChildren`, and a new test in `test_shell_smoke.py` asserts it. Verified from a `git archive` copy (smoke, test_home and test_no_console_errors: 25 passed) and committed as `3944cc2`, noted on T-181.
