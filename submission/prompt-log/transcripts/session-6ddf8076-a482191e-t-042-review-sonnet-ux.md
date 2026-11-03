# Subagent: T-042 review (sonnet ux) (T-042 review (sonnet ux))

Source: `agent-a482191e39184d4c3.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:53:44.069Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-042 "Frontend: input, banners, timeline, Why?, rejected tray, source-record modal" (AC: `python3 tools/board.py show T-042`; card notes describe how to run it). The backend API (T-040) isn't ready, so the UI runs on its mock layer: serve app/frontend with `.venv/bin/python -m http.server 7865 --directory app/frontend` in the background (kill it after), drive it with Playwright at 1280 and 375 px, and screenshot to artifacts/review-evidence/T-042-*.png. Check each AC: 9 records found before any run; .pdf refused; empty/oversize error; needs_review above verified; Dates to confirm group; could-not-verify tray; Why? on entry 7 shows checks/verdict/state/backend; entry 8's source highlight equals the excerpt; synthetic-data banner on every view; `grep -c innerHTML app/frontend/*.js` is 0; data-testid ids per tests/e2e/conftest.py. Write reviews/T-042-ux-designer.md (D.2 JSON). Do not fix. Reply ≤ 3 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:45.355Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/ux-designer.md"
}
````

### User / tool · 2026-11-02T01:53:45.362Z

**tool result**
````
1	# Persona dossier — ux-designer-reviewer
2	
3	## 1. Identity
4	**Priya Raman (fictional), Principal UX Designer, enterprise workflow software — 12 years, last 4 on human-in-the-loop AI review tools (document review, claims triage).**
5	She has watched expert users abandon AI tools that hid where an answer came from, and others that made correcting the AI slower than doing the work by hand. Her incentive: the reviewer must finish faster *and* trust the result, so she grades the cost of verifying and correcting, not the beauty of the first screen.
6	
7	## 2. Day-to-day context
8	- Tools: Figma, Playwright scripts for walkthroughs, screen recordings, heuristic-evaluation sheets.
9	- Pressures: expert users with high volume who live on the keyboard; buyers who judge in a 3-minute demo.
10	- A bad day: usability sessions where every participant re-opens the source PDF because the tool's excerpt is hidden two clicks away.
11	
12	## 3. Goals and success criteria for this artifact
13	- The paralegal can see, for any entry, flag, or dollar amount, the exact source excerpt without leaving the screen.
14	- State is always visible: what is verified, what needs review and why, what has been accepted/edited/dismissed, how many remain.
15	- Correction is cheap: accept/edit/dismiss in one action each, keyboard-reachable, undoable.
16	- Errors, empty states, and model failure are designed, not default stack traces.
17	- The export is usable as pasted text in a demand letter.
18	
19	## 4. Review checklist
20	1. Every timeline entry shows date, provider, one-line summary, and the verbatim excerpt (or a one-click/one-key reveal that stays on the same screen).
21	2. `needs_review` items are visually distinct from `verified` and sorted first; the one-sentence reason is visible without hovering.
22	3. `rejected` (could-not-verify) items appear in a visible tray, not silently dropped.
23	4. Flags are grouped by type (gap, conflict, prior condition, causation language) and each shows the evidence excerpt(s); a conflict shows both excerpts side by side.
24	5. The charges table separates totaled charges from "unclear — not totaled" items; the $185/visit rate sits in the unclear group with its reason.
25	6. A progress indicator shows reviewed vs remaining (e.g., "7 of 12 reviewed") at all times during review.
26	7. Accept, edit, dismiss are each one click and have keyboard equivalents; the shortcuts are discoverable on screen.
27	8. Edit happens in place, preserves the original text for comparison, and marks the item as edited.
28	9. Any accept/dismiss can be undone without reloading.
29	10. Export is disabled or clearly warns while items remain unreviewed, and states exactly what will be included.
30	11. The exported text pastes cleanly into a word processor: one line per entry, no HTML artifacts, no UI labels, citations present.
31	12. Empty input, oversized input, and model/LLM failure each show a plain-language message near the input, preserve what the user pasted, and suggest the next step.
32	13. Long-running processing shows status (step names or progress), not a frozen screen.
33	14. The "synthetic data only" banner is persistent and does not obscure content or focused elements.
34	15. The AI's role is explained where it acts (e.g., "Summary drafted by AI, checked against the excerpt") — not a generic disclaimer.
35	16. Confidence is shown only as states that change a decision (verified / needs review / rejected), not as decorative percentages.
36	17. The layout works at 390 px width: no horizontal scroll for the review list; actions remain reachable.
37	18. Terminology matches the user's world (chronology, provider, excerpt, billed charges), not the developer's (chunk, span, token).
38	19. On first load of the sample-case results, the first focusable item in the results region is a `needs_review` item, and the 73-day gap flag is visible without scrolling at 1440x900.
39	20. Nothing in the interface claims more than the record supports (e.g., no "injury caused by accident" headers).
40	
41	## 5. Red flags / dealbreakers
42	Each item here is a **blocker** (rate it so; never major or minor).
43	- The source excerpt is not visible or reachable for an item (breaks "reviews rather than trusts").
44	- Export includes items the user did not accept, or there is no way to see what will be exported.
45	- An error state loses the user's pasted records.
46	- Unverified model output is styled identically to verified output.
47	
48	## 6. Vocabulary
49	visibility of system status, recognition over recall, error prevention, user control and freedom, accelerators, progressive disclosure, empty state, error state, inline validation, provenance / citation affordance, calibrated trust, efficient correction, efficient dismissal, scope of AI explanation, information scent, hierarchy, affordance.
50	
51	## 7. How I review
52	1. Read the brief; open the app at the given URL with Playwright (desktop 1440x900 and mobile 390x844).
53	2. Screenshot every state: empty, input pasted, processing, results, an item expanded, edit mode, flags panel, charges table, export preview, error (submit empty input; submit 500 KB of text), and model-failure if the brief provides a way to force it.
54	3. Complete the sample case end to end using only the keyboard first, then the mouse. Time both.
55	4. Try to export with items unreviewed; try to undo an accept; edit an entry and check the export shows the edit.
56	5. Paste the export into a plain text file and inspect it.
57	6. Score each of the four criteria (design quality, originality, craft, functionality) 1-5; any score ≤ 2 must have a matching major or blocker finding.
58	7. File findings with screenshot paths under `artifacts/review-evidence/`.
59	
60	Hard thresholds: functionality ≤ 2 → at least one blocker; verifying any single item takes more than 2 actions → major.
61	
62	## 8. Calibration
63	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
64	- **blocker — Excerpt hidden from conflict flag.** Evidence: screenshot shows "Conflicting accident dates" with no excerpts. Fix: show both quotes ("...2026-01-09..." EMS, "Date of accident per intake form: 2026-01-19") with record labels. Test: E2E asserts both excerpts visible in the flag card.
65	- **blocker — Error loses pasted input.** Evidence: submitting 600 KB shows "Error 413" and clears the textarea. Fix: inline message "This is over the 200 KB limit. Split the records and try again." with text preserved.
66	- **minor — No progress count.** Evidence: review screen with 12 entries has no remaining count. Fix: sticky "5 of 12 reviewed · 3 need review".
67	
68	## 9. Sources
69	- https://www.nngroup.com/articles/ten-usability-heuristics/ — NN/g: Nielsen's 10 heuristics (system status, user control, error prevention, recognition over recall, flexibility/accelerators, error recovery).
70	- https://www.nngroup.com/articles/error-message-guidelines/ — NN/g (2023): put errors near their source, don't rely on color alone, explain plainly with a fix, preserve user input.
71	- https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/ — Amershi et al., CHI 2019: 18 validated guidelines across initial use, during interaction, when wrong, over time.
72	- https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ — Microsoft HAX Toolkit: the same 18 guidelines grouped by stage, including when the AI system is wrong.
73	- https://pair.withgoogle.com/chapter/explainability-trust/ — Google PAIR: calibrate trust, explain data sources, scale detail to stakes, show confidence only when it improves decisions.
74	- Assumption: the "two actions to verify" threshold and the 390 px width are this project's choices, not from a source.
75	
76	## 10. Limits
77	Do not judge clinical correctness, adjuster tactics, legal ethics, or code quality. Accessibility conformance (WCAG) belongs to accessibility-reviewer — note obvious issues but defer severity to them.
78	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:46.262Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-042; ls app/frontend; ls .claude/agent-memory/ux-designer-reviewer/; grep -c innerHTML app/frontend/*.js"
}
````

### User / tool · 2026-11-02T01:53:46.405Z

**tool result**
````
---
id: "T-042"
title: "Frontend: input, banners, timeline, Why?, rejected tray, source-record modal"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: ["T-039"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:10Z"
updated_at: "2026-11-02T01:53:45Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T01:47:05Z"
rounds: 0
commits: ["117f2ec"]
reviews: []
ac:
  - {"n": 1, "text": "paste and .txt upload show '9 records found' before any model call; .pdf refused with a plain message; empty/oversize shows an error state (R-IN-1, R-IN-2, R-IN-4); proved by tests/e2e/test_input.py", "done": true, "evidence": "paste/.txt/sample -> record-count '9 records found' before run; .pdf -> role=alert plain msg; empty/oversize -> alert; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 2, "text": "timeline rows show date, provider, summary, excerpt, state; needs_review above verified; 'Dates to confirm' group after the timeline; rejected items in a 'could not verify' tray (R-TL-1, R-TL-5, R-IN-5); proved by test_timeline.py", "done": true, "evidence": "rows date/provider/summary/excerpt/state in queue (needs_review first), dates-to-confirm after timeline, rejected-tray; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 3, "text": "Why? on entry 7 shows check results, judge verdict, state and backend (R-TL-6); proved by test_timeline.py::test_why_entry7", "done": true, "evidence": "entry-why on entry 7: checks, judge, state, backend shown (why-modal); mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 4, "text": "opening entry 8's record highlights a span equal to the excerpt using API offsets (R-RV-9); proved by test_source_record.py::test_entry_highlight", "done": true, "evidence": "btn-source on entry 8: record-highlight text == entry-excerpt using excerpt_start/end - record.char_start; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 5, "text": "banner 'Synthetic data only — never paste real records' on every view and the AI banner on review (R-CO-5); `grep -c innerHTML app/frontend/*.js` is 0 (textContent only)", "done": true, "evidence": "banner-synthetic static in index.html (every view), banner-ai on review; grep -c innerHTML app/frontend/*.js = 0 for every file"}
  - {"n": 6, "text": "Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'.", "done": true, "evidence": "mock ?fail=4: record 4 appears in rejected-tray with 'could not process' + reason (AC6 part for T-042)"}
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": true, "evidence": "bookkeeping item (depends_on edits) - not a frontend change; T-042 depends_on already T-039"}
---
## Description
Input and read-only timeline against the api.md examples (R-IN-1, R-IN-2, R-IN-4, R-IN-5, R-TL-1, R-TL-5, R-TL-6, R-RV-9, R-CO-5). Can start now from the API draft; integrates with the real API when m3-be-api-review lands.

Plan key: m3-fe-input-timeline (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

Estimate: 40 min.

## Notes (append-only, newest last)
- 2026-11-02T01:22:46Z orchestrator: AC 6 added: Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 "could not process" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason "could not process"'.
- 2026-11-02T01:22:46Z orchestrator: AC 7 added: Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.
- 2026-11-02T01:22:47Z orchestrator: updated depends_on=['T-039']
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-042.md
- 2026-11-02T01:47:05Z frontend: claimed
- 2026-11-02T01:47:05Z frontend: Claimed with --force (T-039 in progress; building against api.md + mock layer). Shared module layout proposed for frontend-2/T-043: app/frontend/{index.html,styles.css,api.js (API_MODE const mock|real, fetch + mock),state.js (store+subscribe),dom.js (el() helper, textContent only),input.js,timeline.js,source.js,app.js (T-042 owned); flags.js,charges.js,review.js (T-043 owned)}. Hooks: window.ZL.state, ZL.api, ZL.dom.el, ZL.openSource(recordId, spans), ZL.registerPanel(name, renderFn) for T-043 panels, mount point <div id=side-panels>.
- 2026-11-02T01:47:13Z orchestrator: assigned: frontend-1
- 2026-11-02T01:53:21Z qa: FRONTEND CONTRACT FINAL: tests/e2e/conftest.py docstring (test ids, data-review/data-state/data-flag-type, role=alert, tabindex, a/d/Enter/j keys, no date/provider inputs, optional __debugInjectRecordHtml). Enforced by tests/unit/test_e2e_contract.py.
- 2026-11-02T01:53:31Z frontend: AC 1 checked: paste/.txt/sample -> record-count '9 records found' before run; .pdf -> role=alert plain msg; empty/oversize -> alert; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it
- 2026-11-02T01:53:31Z frontend: AC 2 checked: rows date/provider/summary/excerpt/state in queue (needs_review first), dates-to-confirm after timeline, rejected-tray; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it
- 2026-11-02T01:53:31Z frontend: AC 3 checked: entry-why on entry 7: checks, judge, state, backend shown (why-modal); mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it
- 2026-11-02T01:53:31Z frontend: AC 4 checked: btn-source on entry 8: record-highlight text == entry-excerpt using excerpt_start/end - record.char_start; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it
- 2026-11-02T01:53:31Z frontend: AC 5 checked: banner-synthetic static in index.html (every view), banner-ai on review; grep -c innerHTML app/frontend/*.js = 0 for every file
- 2026-11-02T01:53:31Z frontend: AC 6 checked: mock ?fail=4: record 4 appears in rejected-tray with 'could not process' + reason (AC6 part for T-042)
- 2026-11-02T01:53:32Z frontend: AC 7 checked: bookkeeping item (depends_on edits) - not a frontend change; T-042 depends_on already T-039
- 2026-11-02T01:53:32Z frontend: moved in_progress -> in_review
- 2026-11-02T01:53:45Z orchestrator: review dispatched: ux (sonnet)

## Handoff
Built app/frontend/{index.html,styles.css,dom.js,state.js,api.js,mock.js,mock_sample.js,input.js,timeline.js,source.js,app.js}; data-testids follow tests/e2e/conftest.py (btn-analyze=paste->create+run, btn-sample/file-input create only; entry-<seq>, queue, rejected-tray, record-modal/record-highlight). API_MODE const in api.js is 'real'; ?api=mock uses in-memory contract-shaped mock. Verified only against the mock (29 Playwright checks); real e2e specs not run (no server on :7860). Extension points for T-043: ZL.registerRowActions, ZL.registerPanel, ZL.openSource(spans), ZL.state.applyReview. Hash is #/case/<token>. AC7 (depends_on edits) is orchestrator bookkeeping, not code. Surprised: re-rendering the input view on /health wiped typed text; now the form renders once.

api.js
app.js
charges.js
dev
dom.js
flags.js
index.html
input.js
mock.js
mock_sample.js
review.css
review.js
source.js
state.js
styles.css
timeline.js
app/frontend/api.js:0
app/frontend/app.js:0
app/frontend/dom.js:0
app/frontend/input.js:0
app/frontend/flags.js:0
app/frontend/charges.js:0
app/frontend/source.js:0
app/frontend/review.js:0
app/frontend/mock_sample.js:0
app/frontend/mock.js:0
app/frontend/timeline.js:0
app/frontend/state.js:0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:47.814Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/e2e/conftest.py; ls tests/e2e; cat app/frontend/index.html; wc -l app/frontend/*; ls .venv/bin | grep -i -E \"python|playwright\""
}
````

### User / tool · 2026-11-02T01:53:47.916Z

**tool result**
````
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
Attributes (on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

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
    b.close()
__init__.py
conftest.py
test_api.py
test_charges.py
test_edit.py
test_export_ui.py
test_flags_panel.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_timeline.py
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment timeline (prototype)</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div id="banner-synthetic" class="banner synth" data-testid="banner-synthetic" role="note">Synthetic data only — never paste real records</div>
<header class="top">
  <h1>Treatment timeline</h1>
  <span id="badge" class="chip" hidden></span>
  <span id="retention" class="muted small" hidden></span>
  <button type="button" id="delete-now" class="btn small" hidden>Delete now</button>
</header>
<div id="banner-ai" class="banner ai" data-testid="banner-ai" role="note" hidden></div>
<main>
  <section id="view-input" class="card" aria-labelledby="h-input">
    <h2 id="h-input">1. Records</h2>
    <div id="input-body"></div>
  </section>
  <section id="view-review" class="card" aria-labelledby="h-review" hidden>
    <h2 id="h-review" class="sr">Review</h2>
    <div id="review-body"></div>
  </section>
</main>
<dialog id="source-modal" data-testid="record-modal" aria-labelledby="source-title">
  <div class="dlg-head"><h2 id="source-title">Source record</h2><button type="button" id="source-close" class="btn small" data-testid="btn-close-modal">Close</button></div>
  <div id="source-body"></div>
</dialog>
<dialog id="why-modal" data-testid="why-modal" aria-labelledby="why-title">
  <div class="dlg-head"><h2 id="why-title">Why?</h2><button type="button" class="btn small" data-testid="why-close" onclick="this.closest('dialog').close()">Close</button></div>
  <div id="why-body"></div>
</dialog>
<!-- load order matters; mock files are only used when API_MODE is "mock" -->
<script src="dom.js"></script>
<script src="mock_sample.js"></script>
<script src="mock.js"></script>
<script src="api.js"></script>
<script src="state.js"></script>
<script src="input.js"></script>
<script src="source.js"></script>
<script src="timeline.js"></script>
<!-- T-043 (frontend-2): add flags.js, charges.js, review.js here; register with ZL.registerRowActions / ZL.registerPanel -->
<script src="app.js"></script>
</body>
</html>
wc: app/frontend/dev: read: Is a directory
      39 app/frontend/api.js
      53 app/frontend/app.js
      74 app/frontend/charges.js
      29 app/frontend/dom.js
     100 app/frontend/flags.js
      48 app/frontend/index.html
      83 app/frontend/input.js
     206 app/frontend/mock.js
       2 app/frontend/mock_sample.js
      82 app/frontend/review.css
     246 app/frontend/review.js
      36 app/frontend/source.js
      26 app/frontend/state.js
      54 app/frontend/styles.css
     118 app/frontend/timeline.js
    1196 total
playwright
python
python3
python3.12
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:49.722Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat api.js app.js input.js timeline.js source.js state.js styles.css; ls dev; cat /Users/arsis/zlayt-pm-project/tests/e2e/test_input.py /Users/arsis/zlayt-pm-project/tests/e2e/test_timeline.py /Users/arsis/zlayt-pm-project/tests/e2e/test_source_record.py"
}
````

### User / tool · 2026-11-02T01:53:49.810Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:50.878Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat app.js input.js timeline.js source.js styles.css"
}
````

### User / tool · 2026-11-02T01:53:50.954Z

**tool result**
````
/* Bootstrap: health -> banners; restore case from #case=<token>; poll run status; render on every state change. */
(function () {
  const ZL = window.ZL, { $ } = ZL;
  const SYNTH = "Synthetic data only — never paste real records";
  let poller = null;

  function renderChrome(s) {
    const h = s.health;
    $("#banner-synthetic").textContent = (h && h.banner) || SYNTH;           // present on every view, even before /health answers
    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? "cached demo" : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : "";
    badge.hidden = !h;
    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
    live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
    $("#delete-now").hidden = live.hidden;
  }
  function render(s) {
    renderChrome(s);
    ZL.renderInput(s);
    $("#view-review").hidden = !(s.case && s.case.status === "ready");
    ZL.renderReview(s);
  }
  ZL.state.subscribe(render);

  ZL.pollRun = function () {
    clearInterval(poller);
    const tick = async () => {
      const s = ZL.state.get(); if (!s.token) return clearInterval(poller);
      try {
        const st = await ZL.api.status(s.token);
        if (st.status === "ready") { clearInterval(poller); ZL.state.set({ status: st, case: await ZL.api.getCase(s.token) }); }
        else if (st.status === "failed") { clearInterval(poller); ZL.state.set({ status: st, case: await ZL.api.getCase(s.token) }); }
        else ZL.state.set({ status: st });
      } catch (e) { clearInterval(poller); ZL.state.set({ status: { status: "failed", error: { message: e.message } } }); }
    };
    tick(); poller = setInterval(tick, 1000);
  };

  async function boot() {
    render(ZL.state.get());
    try { ZL.state.set({ health: await ZL.api.health() }); } catch (_) { /* banners fall back to static text */ }
    const m = /#\/case\/([^&/]+)/.exec(location.hash);
    if (m) {
      const token = decodeURIComponent(m[1]);
      try { const c = await ZL.api.getCase(token); ZL.state.set({ token, case: c }); if (c.status === "running") ZL.pollRun(); }
      catch (_) { history.replaceState(null, "", location.pathname + location.search); }
    }
  }
  document.addEventListener("DOMContentLoaded", () => {
    $("#delete-now").addEventListener("click", () => ZL.startOver());
    boot();
  });
})();
/* Input view: paste or .txt upload -> POST /cases -> "N records found" BEFORE any model call -> Run. (R-IN-1, R-IN-2, R-IN-4) */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  const PDF_MSG = "PDF files can't be read here. Save the records as plain text (.txt) or paste them.";
  let busy = false, pending = null; // pending = {text} read from an uploaded file

  function showError(msg) {
    const box = ZL.$("#input-error"); box.textContent = msg || ""; box.hidden = !msg;
  }
  async function create(payload, autoRun) {
    if (busy) return; busy = true; showError("");
    try {
      const resp = await ZL.api.createCase(payload);
      history.replaceState(null, "", "#/case/" + encodeURIComponent(resp.token));
      const c = await ZL.api.getCase(resp.token);
      ZL.state.set({ token: resp.token, created: resp, case: c, status: null });
      if (autoRun) await startRun();
    } catch (e) {
      showError(e.message);
    } finally { busy = false; }
  }
  function submitText(autoRun) {
    const text = (pending && pending.text != null) ? pending.text : ZL.$("#paste").value;
    const max = ZL.state.get().health && ZL.state.get().health.limits.max_chars;
    if (!text.trim()) return showError("There is no text to read. Paste records or choose a .txt file.");
    if (max && text.length > max) return showError(`That is ${text.length.toLocaleString("en-US")} characters; the limit is ${max.toLocaleString("en-US")}. Nothing was sent.`);
    create({ text }, autoRun);
  }
  function onFile(ev) {
    const f = ev.target.files && ev.target.files[0]; pending = null; showError("");
    if (!f) return;
    if (/\.pdf$/i.test(f.name) || f.type === "application/pdf") { ev.target.value = ""; return showError(PDF_MSG); }
    if (!/\.txt$/i.test(f.name) && f.type && f.type !== "text/plain") { ev.target.value = ""; return showError("Only .txt files are accepted. Paste the text instead, or save the file as plain text."); }
    const rd = new FileReader();
    rd.onerror = () => showError("That file could not be read.");
    rd.onload = () => { pending = { text: String(rd.result) }; ZL.$("#file-name").textContent = f.name; submitText(); };
    rd.readAsText(f);
  }

  ZL.renderInput = function (s) {
    const root = ZL.$("#input-body");
    const c = s.case, h = s.health;
    const limitTxt = "Limit: " + (h ? h.limits.max_chars.toLocaleString("en-US") : "—") + " characters. Plain text only; PDFs are not supported.";
    if (!c && root.dataset.mode === "form") { const l = ZL.$("#limit-note"); if (l) l.textContent = limitTxt; return; } // keep what she typed
    clear(root); root.dataset.mode = c ? "case" : "form";
    if (!c) {
      root.append(
        el("label", { for: "paste", class: "lbl" }, "Paste the records (each starts with a line like “=== Record 1 ===”)"),
        el("textarea", { id: "paste", "data-testid": "input-text", rows: "9", spellcheck: "false", placeholder: "=== Record 1 ===\nDate: 2026-01-09\nSource: ...\nExcerpt: \"...\"" }),
        el("div", { class: "row" },
          el("button", { type: "button", class: "btn primary", "data-testid": "btn-analyze", onclick: () => { pending = null; submitText(true); } }, "Analyze"),
          el("label", { class: "btn", for: "file" }, "Upload .txt"),
          el("input", { id: "file", type: "file", accept: ".txt,text/plain", "data-testid": "file-input", class: "sr", onchange: onFile }),
          el("button", { type: "button", class: "btn", "data-testid": "btn-sample", onclick: () => create({ sample: true }) }, "Use the sample case"),
          el("span", { id: "file-name", class: "muted" })),
        el("p", { id: "input-error", class: "error", role: "alert", "data-testid": "error", hidden: true }),
        el("p", { id: "limit-note", class: "muted small" }, limitTxt));
      return;
    }
    const n = c.records ? c.records.length : 0;
    const running = c.status === "running";
    root.append(...[
      el("p", { class: "found", "data-testid": "record-count", role: "status" }, `${n} ${n === 1 ? "record" : "records"} found`),
      el("p", { class: "muted small" }, "Read by code only. No model has been called yet."),
      el("ul", { class: "reclist", "data-testid": "record-list" }, c.records.map((r) => el("li", {}, `Record ${r.seq}: ${r.source_label} — ${r.date_status === "parsed" || r.date_status === "confirmed" ? ZL.fmtDate(r.date_iso) : r.date_status === "ambiguous" ? "date to confirm" : "no readable date"}`))),
      el("div", { class: "row" },
        c.status === "ingested" ? el("button", { type: "button", class: "btn primary", "data-testid": "btn-analyze", onclick: startRun }, "Analyze") : null,
        el("button", { type: "button", class: "btn", "data-testid": "start-over", onclick: startOver }, "Start over")),
      running || (s.status && s.status.status === "running") ? el("p", { class: "progress", "data-testid": "status-stage", role: "status" }, (s.status && s.status.progress && s.status.progress.label) || "Working…") : null,
      s.status && s.status.status === "failed" ? el("p", { class: "error", role: "alert", "data-testid": "run-error" }, (s.status.error && s.status.error.message) || "The run failed. Finished items are kept.") : null,
      el("p", { id: "input-error", class: "error", role: "alert", "data-testid": "error", hidden: true })].filter(Boolean));
  };
  async function startRun() {
    const s = ZL.state.get(); showError("");
    try { await ZL.api.run(s.token, false); ZL.pollRun(); } catch (e) { showError(e.message); }
  }
  async function startOver() {
    const s = ZL.state.get(); try { if (s.token) await ZL.api.remove(s.token); } catch (_) { /* already gone */ }
    pending = null; history.replaceState(null, "", location.pathname + location.search);
    ZL.state.set({ token: null, created: null, case: null, status: null });
  }
  ZL.startOver = startOver;
})();
/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
   T-043 plugs in through ZL.registerRowActions(fn(entry,rowEl)) and ZL.registerPanel(fn(case, mountEl)). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let sortMode = "review"; // "review" = needs_review first, then by date; "date" = chronological

  const STATE_LABEL = { verified: "Verified", needs_review: "Needs review", rejected: "Could not verify" };
  const REASON = { JUDGE_PARTIAL: "part of the summary isn't fully supported by the quote", JUDGE_UNSUPPORTED: "the summary isn't supported by the quote", DATE_AMBIGUOUS: "the date can be read two ways",
    LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled" };
  const reasonText = (r) => REASON[r] || String(r).toLowerCase().replace(/_/g, " ");

  function stateChip(e) {
    return el("span", { class: "chip st-" + e.state, "data-testid": "entry-state" }, STATE_LABEL[e.state] || e.state);
  }
  function entryRow(e, c) {
    const rec = c.records.find((r) => r.id === e.record_ids[0]);
    const row = el("article", { class: "entry st-" + e.state, "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
    row.append(...[
      el("div", { class: "entry-head" },
        el("span", { class: "date", "data-testid": "entry-date" }, e.date || "undated"),
        el("span", { class: "provider", "data-testid": "entry-provider" }, e.provider),
        stateChip(e),
        el("span", { class: "chip rs-" + e.review_status, "data-testid": "review-status" }, e.review_status)),
      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag" }, "AI-drafted") : null),
      e.edited ? el("p", { class: "muted small", "data-testid": "edited-note" }, "Edited by you. Original: " + e.edited.original_summary) : null,
      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt),
      e.duplicate_note ? el("p", { class: "muted small" }, e.duplicate_note) : null,
      e.state === "needs_review" && e.reasons.length ? el("p", { class: "reason", "data-testid": "entry-reasons" }, "Check: " + e.reasons.map(reasonText).join("; ")) : null,
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
        el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, "Open record"))].filter(Boolean));
    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    return row;
  }
  function sortedEntries(c) {
    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    const list = c.entries.slice().sort(byDate);
    if (sortMode === "date") return list;
    const rank = (e) => (e.state === "needs_review" ? 0 : 1);
    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
  }
  function datesToConfirm(c) {
    const box = el("section", { class: "group", "data-testid": "dates-to-confirm" }, el("h2", {}, "Dates to confirm"));
    if (!c.undated_entries.length && !c.dates_to_confirm.length) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records are left off the timeline and the gap check until you pick the right date. The tool never guesses."));
    c.undated_entries.forEach((e) => {
      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
      const rec = c.records.find((r) => r.id === e.record_ids[0]);
      const row = entryRow(e, c); row.classList.add("undated");
      if (d && d.candidates.length) {
        const bar = el("div", { class: "row", role: "group", "aria-label": "Choose the date" }, el("span", {}, `Written as “${d.date_raw}”. Which date?`));
        d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn small", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
          try { await ZL.api.confirmDate(ZL.state.get().token, d.record_id, cand); ZL.state.set({ case: await ZL.api.getCase(ZL.state.get().token) }); } catch (er) { alert(er.message); }
        } }, ZL.fmtDate(cand))));
        row.insertBefore(bar, row.querySelector(".row-actions"));
      } else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
      box.append(row);
    });
    return box;
  }
  function tray(c) {
    const box = el("section", { class: "group tray", "data-testid": "rejected-tray" }, el("h2", {}, `Could not verify (${c.tray.length})`));
    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here. Every record produced an entry that passed the code checks.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself."));
    c.tray.forEach((t) => {
      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip st-rejected" }, "Could not verify")),
        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
        el("p", { class: "summary" }, t.why),
        t.attempt ? el("p", { class: "muted small" }, "The model's attempt (not used): " + (t.attempt.summary || "") + " — “" + (t.attempt.excerpt || "") + "”") : null,
        el("div", { class: "row-actions" }, recs.map((r) => el("button", { type: "button", class: "btn small", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
      box.append(item);
    });
    return box;
  }

  // ---- Why? panel
  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
  async function openWhy(id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    ZL.$("#why-title").textContent = "Why? " + id;
    body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
    try {
      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
      clear(body);
      body.append(...[
        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
        el("dl", { class: "kv", "data-testid": "why-ladder" },
          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
          lad.generator ? [el("dt", {}, "Generator"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
            el("dt", {}, "Generator output"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
          el("dt", {}, "Code checks"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
          el("dt", {}, "Second check (judge)"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
    } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
  }
  ZL.openWhy = openWhy;

  ZL.renderReview = function (s) {
    const c = s.case, mount = ZL.$("#review-body"); clear(mount);
    if (!c || c.status !== "ready") return;
    const counts = c.review && c.review.counts;
    const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
    wrap.append(
      el("div", { class: "toolbar" },
        el("h2", {}, `Timeline (${c.entries.length} entries)`),
        counts ? el("span", { class: "muted small", "data-testid": "review-counts" }, `${counts.needs_review} need review · ${counts.verified} verified`) : null,
        el("label", { class: "muted small" }, "Order ",
          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
      el("div", { class: "timeline", "data-testid": "queue" }, sortedEntries(c).map((e) => entryRow(e, c))),
      datesToConfirm(c), tray(c));
    const side = el("div", { id: "side-panels", "data-testid": "side-panels" }); wrap.append(side);
    ZL.hooks.panels.forEach((fn) => fn(c, side));
  };
})();
/* Source-record modal (R-RV-9). ZL.openSource([{record_id, start, end}]) opens the full record text(s) with the span [start,end)
   (ABSOLUTE character offsets from the API, never computed from the model) highlighted. Used by entries here and by flags/charges in T-043. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  function recordView(rec, span, label) {
    const box = el("section", { class: "src-rec", "data-testid": "record-section", "data-record-id": rec.id });
    box.append(el("h3", {}, label || `Record ${rec.seq}: ${rec.source_label}`));
    const pre = el("pre", { class: "src-text" });
    const rs = span.start - rec.char_start, re = span.end - rec.char_start;
    if (span.start == null || rs < 0 || re > rec.text.length || re <= rs) {
      pre.append(document.createTextNode(rec.text));
      box.append(pre, el("p", { class: "error", role: "alert", "data-testid": "highlight-missing" }, "The exact position of this quote could not be found in the record, so nothing is highlighted. Check the whole record."));
      return { box, mark: null };
    }
    const mark = el("mark", { "data-testid": "record-highlight", tabindex: "-1" }, rec.text.slice(rs, re));
    pre.append(document.createTextNode(rec.text.slice(0, rs)), mark, document.createTextNode(rec.text.slice(re)));
    box.append(pre);
    return { box, mark };
  }
  ZL.openSource = function (spans, title) {
    const c = ZL.state.get().case; if (!c) return;
    const dlg = ZL.$("#source-modal"), body = ZL.$("#source-body"); clear(body);
    ZL.$("#source-title").textContent = title || "Source record";
    let first = null;
    spans.forEach((sp) => {
      const rec = c.records.find((r) => r.id === sp.record_id); if (!rec) return;
      const v = recordView(rec, sp); body.append(v.box); first = first || v.mark;
    });
    if (!dlg.open) dlg.showModal();
    if (first) first.scrollIntoView({ block: "center" });
  };
  ZL.entrySpans = (e) => e.record_ids.map((rid) => ({ record_id: rid, start: e.excerpt_start, end: e.excerpt_end }));
  document.addEventListener("DOMContentLoaded", () => {
    ZL.$("#source-close").addEventListener("click", () => ZL.$("#source-modal").close());
  });
})();
[hidden]{display:none!important}
:root{--bg:#f6f7f9;--panel:#fff;--ink:#16181d;--muted:#555d6b;--line:#d5dae2;--accent:#2f5bd3;--ok:#1d7a46;--warn:#8a5300;--bad:#b42318;--chip:#eef1f6;--mark:#ffe58a;--warnbg:#fff4e0;--aibg:#eaf1ff}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--panel:#171a21;--ink:#e7e9ee;--muted:#a3abb9;--line:#2c3240;--accent:#8fb0ff;--ok:#4cc38a;--warn:#f0b04a;--bad:#ff8a7e;--chip:#222734;--mark:#7a6200;--warnbg:#2b2214;--aibg:#17233d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.banner{padding:8px 16px;font-weight:600;text-align:center}
.banner.synth{background:#b42318;color:#fff;position:sticky;top:0;z-index:5}
.banner.ai{background:var(--aibg);border-bottom:1px solid var(--line);font-weight:500}
.top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 16px}
.top h1{font-size:20px;margin:0 auto 0 0}
main{max-width:980px;margin:0 auto;padding:0 12px 60px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:14px}
h2{font-size:18px;margin:0 0 8px}h3{font-size:15px;margin:10px 0 4px}
.muted{color:var(--muted)}.small{font-size:13px}
.lbl{display:block;font-weight:600;margin-bottom:4px}
textarea{width:100%;font:14px/1.4 ui-monospace,Menlo,monospace;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--line);border-radius:8px;background:var(--chip);color:var(--ink);font:inherit;font-weight:600;cursor:pointer}
.btn.small{min-height:36px;padding:0 10px;font-size:14px}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn:focus-visible,textarea:focus-visible,select:focus-visible,mark:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.error{background:var(--warnbg);border:1px solid var(--bad);color:var(--bad);border-radius:8px;padding:8px 10px;font-weight:600}
.error[hidden]{display:none}
.found{font-size:22px;font-weight:700;margin:0}
.reclist{padding-left:20px;margin:6px 0}
.progress{font-weight:600}
.chip{display:inline-block;background:var(--chip);border-radius:999px;padding:1px 10px;font-size:13px;font-weight:600}
.chip.st-verified{color:var(--ok)}.chip.st-needs_review{color:var(--warn);background:var(--warnbg)}.chip.st-rejected{color:var(--bad)}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.toolbar h2{margin:0}
select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px}
.entry{border:1px solid var(--line);border-left:5px solid var(--ok);border-radius:10px;padding:10px 12px;margin:10px 0;background:var(--panel)}
.entry.st-needs_review{border-left-color:var(--warn);background:var(--warnbg)}
.entry.st-rejected{border-left-color:var(--bad)}
.entry-head{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center}
.date{font-weight:700;font-variant-numeric:tabular-nums}.provider{font-weight:600}
.summary{margin:6px 0}
.tag{margin-left:8px;font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:0 4px}
.excerpt{margin:6px 0;padding:6px 10px;border-left:3px solid var(--line);color:var(--muted);font-style:italic;overflow-wrap:anywhere}
.reason{color:var(--warn);font-weight:600;margin:4px 0}
.row-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.group{margin-top:22px;padding-top:6px;border-top:2px solid var(--line)}
dialog{border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);width:min(820px,96vw);max-height:90vh;padding:0}
dialog::backdrop{background:rgba(0,0,0,.45)}
.dlg-head{display:flex;justify-content:space-between;align-items:center;gap:8px;position:sticky;top:0;background:var(--panel);padding:10px 14px;border-bottom:1px solid var(--line)}
.dlg-head h2{margin:0;font-size:17px}
#source-body,#why-body{padding:10px 14px}
.src-text{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;font:14px/1.5 ui-monospace,Menlo,monospace}
mark{background:var(--mark);color:inherit;padding:0 1px;border-radius:2px}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px}.kv dt{font-weight:700}.kv dd{margin:0;overflow-wrap:anywhere}
.checks{margin:0;padding-left:18px}.checks .bad{color:var(--bad);font-weight:700}
.why-sentence{font-weight:600}
@media (max-width:480px){.kv{grid-template-columns:1fr}.btn{min-height:44px}main{padding:0 8px 60px}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:51.356Z

**tool call — Bash**
````
{
 "command": "cat tests/e2e/test_input.py tests/e2e/test_timeline.py tests/e2e/test_source_record.py | head -150; ls app/frontend/dev"
}
````

### User / tool · 2026-11-02T01:53:51.441Z

**tool result**
````
"""Input screen. R-IN-1, R-IN-2, R-IN-3, R-IN-5, R-ST (synthetic banner)."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_synthetic_banner_always_visible(page):
    """CLAUDE.md data rule: the persistent 'synthetic data only' banner is on the first screen."""
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

def test_ambiguous_date_goes_to_dates_to_confirm(page):
    """R-IN-3/R-IN-5: case_01 record 8 (04/05/2026) is listed under 'Dates to confirm', not on the timeline."""
    page.goto(BASE); page.get_by_test_id("input-text").fill(golden_text("case_01_date_formats.txt")); page.get_by_test_id("btn-analyze").click()
    page.get_by_test_id("dates-to-confirm").wait_for(); assert "04/05/2026" in page.get_by_test_id("dates-to-confirm").inner_text()
"""Timeline. R-TL-1, R-TL-5, R-TL-3, R-RV-1."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_nine_entries_in_date_order(page, sample_case):
    """R-TL-1: nine entries, ISO dates non-decreasing, each with provider/summary/excerpt."""
    open_case(page, sample_case)
    dates = [page.get_by_test_id(f"entry-{i}").get_by_test_id("entry-date").inner_text() for i in range(1, 10)]
    assert dates == sorted(dates)

def test_record_7_dated_by_header_not_body(page, sample_case):
    """R-TL-3: entry 7 shows 2026-05-18, never 2026-01-19."""
    open_case(page, sample_case); assert page.get_by_test_id("entry-7").get_by_test_id("entry-date").inner_text() == "2026-05-18"

def test_needs_review_sorted_first_in_queue(page, sample_case):
    """R-TL-5: items in state needs_review appear above verified ones in the queue."""
    open_case(page, sample_case)
    states = [e.get_attribute("data-state") for e in page.get_by_test_id("queue").locator("[data-state]").all()]
    seen_verified = False
    for s in states:
        if s == "verified": seen_verified = True
        assert not (seen_verified and s == "needs_review")

def test_provider_is_header_label(page, sample_case):
    """R-TL-9: entry 4 provider reads 'Capital PT, initial evaluation'."""
    open_case(page, sample_case); assert page.get_by_test_id("entry-4").get_by_test_id("entry-provider").inner_text() == "Capital PT, initial evaluation"

def test_every_entry_shows_why(page, sample_case):
    """R-TL-5 / row 18: each entry exposes a 'Why?' sentence."""
    open_case(page, sample_case); page.get_by_test_id("entry-8").get_by_test_id("entry-why").click(); assert page.get_by_test_id("why-text").is_visible()
"""Open the source record. R-RV-9 (highlight by code offsets), R-ST-1."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_entry_8_highlight_equals_excerpt(page, sample_case):
    """R-RV-9: from entry 8 open the record; the highlighted span equals the excerpt string."""
    open_case(page, sample_case); page.get_by_test_id("entry-8").get_by_test_id("btn-source").click()
    ex = page.get_by_test_id("entry-8").get_by_test_id("entry-excerpt").inner_text()
    assert re.sub(r"\s+", " ", page.get_by_test_id("record-highlight").inner_text()).strip() == re.sub(r"\s+", " ", ex).strip()

def test_gap_flag_opens_both_records(page, sample_case):
    """R-RV-9: the 73-day gap flag opens records 6 and 7."""
    open_case(page, sample_case); page.get_by_test_id("flags-panel").locator("[data-flag-type=gap]").first.get_by_test_id("btn-source").click()
    t = page.get_by_test_id("record-modal").inner_text(); assert "Record 6" in t and "Record 7" in t

def test_record_text_is_inserted_as_text(page, sample_case):
    """Arch invariant: untrusted strings use textContent. The modal shows the record header literally ('=== Record 1 ===') and has no script/img/iframe; a test-only hook (window.__debugInjectRecordHtml) must show markup as literal text."""
    open_case(page, sample_case); page.get_by_test_id("entry-1").get_by_test_id("btn-source").click()
    m = page.get_by_test_id("record-modal"); assert "=== Record 1 ===" in m.inner_text() and m.locator("script, img, iframe").count() == 0
    if page.evaluate("typeof window.__debugInjectRecordHtml === 'function'"):
        page.evaluate("window.__debugInjectRecordHtml('<img src=x onerror=alert(1)>')"); assert "<img src=x" in m.inner_text() and m.locator("img").count() == 0
harness.js
mock-data.js
mock-review.js
panels.html
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:53:54.963Z

**tool call — Bash**
````
{
 "command": "grep -n \"fail\\|max_chars\\|limit\\|latency\\|setTimeout\\|progress\" app/frontend/mock.js | head -40; grep -n \"def open_case\" -A8 tests/e2e/conftest.py; (.venv/bin/python -m http.server 7865 --directory app/frontend >/dev/null 2>&1 & echo $! > /private/tmp/claude-501/ux_srv.pid); sleep 1; curl -s -o /dev/null -w \"%{http_code}\\n\" localhost:7865/index.html"
}
````

### User / tool · 2026-11-02T01:53:56.080Z

**tool result**
````
3:   Mock switches (URL query): ?fail=4 makes the stub backend fail every call for record 4 (tray shows "could not process"). */
77:  function build(token, name, text, sample, failN) {
81:      if (failN && r.seq === failN) {
136:  const failN = () => +(new URLSearchParams(location.search).get("fail") || 0);
142:      await new Promise((r) => setTimeout(r, 30));
145:        models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, limits: { max_chars: MAX_CHARS, max_records: 40 }, retention_hours: 24,
151:        if (text.length > MAX_CHARS) return err(413, "input_too_large", `That is more than ${MAX_CHARS.toLocaleString("en-US")} characters, which is the limit.`);
153:        const c = build(token, (body && body.sample) ? "Rivera sample" : "Pasted records", text, !!(body && body.sample), failN());
165:        if (c.status === "running") return err(409, "run_in_progress", "A run is already in progress.");
166:        c.status = "running"; c._run = Date.now(); setTimeout(() => { c.status = "ready"; recompute(c); }, 1800);
172:          progress: { done: Math.round(frac * total), total, label: `Checking summaries ${Math.round(frac * total)} of ${total}` }, counts: { entries: c.entries.length, amounts: c.amounts.length, flags: c.flags.length }, error: null, elapsed_ms: Date.now() - c._run });
180:          calls: [{ id: "c1", role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", attempt: 1, latency_ms: 5120, parsed_ok: !(it.state === "rejected"), verdict: null },
181:            { id: "c2", role: "judge", step: "judge_entries", backend: "fixture", model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", attempt: 1, latency_ms: 2210, parsed_ok: true, verdict: it.ladder && it.ladder.judge ? it.ladder.judge.verdict : null }], events: [] });
82:def open_case(page, tok):
83-    page.goto(f"{BASE}/#/case/{tok}")
84-    page.get_by_test_id("timeline").wait_for(timeout=15000)
200
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:54:11.255Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence && cat > artifacts/review-evidence/T-042-ux-designer-walk.py <<'EOF'\nimport re, json, tempfile, os\nfrom playwright.sync_api import sync_playwright\nU=\"http://localhost:7865/index.html?api=mock\"\nOUT=\"artifacts/review-evidence/T-042-\"\nlog=[]\ndef L(k,v): log.append((k,v)); print(k,\"=>\",v)\nwith sync_playwright() as p:\n    b=p.chromium.launch()\n    for W,H,tag in ((1280,900,\"1280\"),(375,812,\"375\")):\n        ctx=b.new_context(viewport={\"width\":W,\"height\":H}); pg=ctx.new_page()\n        errs=[]; pg.on(\"pageerror\",lambda e:errs.append(str(e))); pg.on(\"console\",lambda m: errs.append(m.text) if m.type==\"error\" else None)\n        pg.on(\"dialog\",lambda d:(errs.append(\"DIALOG \"+d.message), d.dismiss()))\n        pg.goto(U); pg.wait_for_timeout(500)\n        pg.screenshot(path=f\"{OUT}{tag}-01-empty.png\")\n        L(tag+\" banner\",pg.get_by_test_id(\"banner-synthetic\").inner_text())\n        # empty\n        pg.get_by_test_id(\"btn-analyze\").click(); pg.wait_for_timeout(200)\n        L(tag+\" empty alert\",pg.get_by_role(\"alert\").first.inner_text())\n        pg.screenshot(path=f\"{OUT}{tag}-02-empty-error.png\")\n        # oversize\n        big=\"=== Record 1 ===\\n\"+(\"x\"*600000)\n        pg.get_by_test_id(\"input-text\").fill(big); pg.get_by_test_id(\"btn-analyze\").click(); pg.wait_for_timeout(300)\n        L(tag+\" oversize alert\",pg.get_by_role(\"alert\").first.inner_text()); L(tag+\" textarea preserved len\",len(pg.get_by_test_id(\"input-text\").input_value()))\n        pg.screenshot(path=f\"{OUT}{tag}-03-oversize.png\")\n        # pdf\n        d=tempfile.mkdtemp(); f=os.path.join(d,\"x.pdf\"); open(f,\"wb\").write(b\"%PDF-1.4\")\n        pg.get_by_test_id(\"input-text\").fill(\"my pasted text keep me\")\n        pg.get_by_test_id(\"file-input\").set_input_files(f); pg.wait_for_timeout(200)\n        L(tag+\" pdf alert\",pg.get_by_role(\"alert\").first.inner_text()); L(tag+\" paste kept after pdf\",pg.get_by_test_id(\"input-text\").input_value())\n        pg.screenshot(path=f\"{OUT}{tag}-04-pdf.png\")\n        # sample\n        pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for()\n        L(tag+\" count\",pg.get_by_test_id(\"record-count\").inner_text())\n        pg.screenshot(path=f\"{OUT}{tag}-05-found.png\")\n        pg.get_by_test_id(\"btn-analyze\").click(); pg.wait_for_timeout(700)\n        L(tag+\" progress\",pg.get_by_test_id(\"status-stage\").inner_text() if pg.get_by_test_id(\"status-stage\").count() else \"none\")\n        pg.screenshot(path=f\"{OUT}{tag}-06-processing.png\")\n        pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        pg.screenshot(path=f\"{OUT}{tag}-07-results.png\")\n        pg.screenshot(path=f\"{OUT}{tag}-07b-results-full.png\",full_page=True)\n        L(tag+\" ai banner vis\",pg.get_by_test_id(\"banner-ai\").is_visible()); L(tag+\" synth vis\",pg.get_by_test_id(\"banner-synthetic\").is_visible())\n        rows=pg.get_by_test_id(\"queue\").locator(\"[data-state]\").all()\n        L(tag+\" queue states\",[r.get_attribute(\"data-state\") for r in rows])\n        L(tag+\" queue ids\",[r.get_attribute(\"data-testid\") for r in rows])\n        L(tag+\" first focusable in results\", pg.evaluate(\"()=>{const m=document.querySelector('#view-review');const f=m.querySelector('a[href],button,select,input,textarea,[tabindex]:not([tabindex=\\\"-1\\\"])');const r=f.closest('[data-state]');return f.outerHTML.slice(0,90)+' | row state='+(r?r.dataset.state:null)}\"))\n        L(tag+\" queue rows tabindex\",pg.evaluate(\"()=>[...document.querySelectorAll('[data-testid=queue] [data-state]')].map(e=>e.getAttribute('tabindex'))\"))\n        L(tag+\" horiz scroll\",pg.evaluate(\"()=>document.documentElement.scrollWidth>document.documentElement.clientWidth\"))\n        L(tag+\" review-counts\",pg.get_by_test_id(\"review-counts\").inner_text() if pg.get_by_test_id(\"review-counts\").count() else None)\n        L(tag+\" dates-to-confirm\",pg.get_by_test_id(\"dates-to-confirm\").inner_text()[:200])\n        L(tag+\" tray\",pg.get_by_test_id(\"rejected-tray\").inner_text()[:300])\n        # ordering of sections\n        L(tag+\" section order\",pg.evaluate(\"()=>[...document.querySelectorAll('[data-testid=timeline] > *')].map(e=>e.dataset.testid||e.className)\"))\n        e7=pg.get_by_test_id(\"entry-7\"); e7.scroll_into_view_if_needed(); pg.screenshot(path=f\"{OUT}{tag}-08-entry7.png\")\n        e7.get_by_test_id(\"entry-why\").click(); pg.wait_for_timeout(400)\n        L(tag+\" why\",pg.get_by_test_id(\"why-modal\").inner_text())\n        pg.screenshot(path=f\"{OUT}{tag}-09-why7.png\")\n        pg.get_by_test_id(\"why-close\").click()\n        e8=pg.get_by_test_id(\"entry-8\"); ex=e8.get_by_test_id(\"entry-excerpt\").inner_text()\n        e8.get_by_test_id(\"btn-source\").click(); pg.wait_for_timeout(300)\n        hl=pg.get_by_test_id(\"record-highlight\").inner_text()\n        L(tag+\" e8 highlight==excerpt\",re.sub(r\"\\s+\",\" \",hl).strip()==re.sub(r\"\\s+\",\" \",ex).strip()); L(tag+\" e8 excerpt\",ex[:100]); L(tag+\" hl\",hl[:100])\n        pg.screenshot(path=f\"{OUT}{tag}-10-source8.png\")\n        pg.get_by_test_id(\"btn-close-modal\").click()\n        # keyboard: tab order first 6\n        pg.reload(); \n        L(tag+\" errs\",errs)\n        ctx.close()\n        # fail=4\n        ctx=b.new_context(viewport={\"width\":W,\"height\":H}); pg=ctx.new_page()\n        pg.goto(U+\"&fail=4\"); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"btn-analyze\").click(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        L(tag+\" fail4 tray\",pg.get_by_test_id(\"rejected-tray\").inner_text()); pg.get_by_test_id(\"rejected-tray\").scroll_into_view_if_needed()\n        pg.screenshot(path=f\"{OUT}{tag}-11-fail4.png\")\n        ctx.close()\n    b.close()\nEOF\n.venv/bin/python artifacts/review-evidence/T-042-ux-designer-walk.py 2>&1 | cut -c1-900"
}
````

### User / tool · 2026-11-02T01:54:32.272Z

**tool result**
````
1280 banner => Synthetic data only — never paste real records
1280 empty alert => There is no text to read. Paste records or choose a .txt file.
1280 oversize alert => That is 600,017 characters; the limit is 60,000. Nothing was sent.
1280 textarea preserved len => 600017
1280 pdf alert => PDF files can't be read here. Save the records as plain text (.txt) or paste them.
1280 paste kept after pdf => my pasted text keep me
1280 count => 9 records found
1280 progress => Checking summaries 0 of 9
1280 ai banner vis => True
1280 synth vis => True
1280 queue states => ['needs_review', 'verified', 'verified', 'verified', 'verified', 'verified', 'verified', 'verified', 'verified']
1280 queue ids => ['entry-3', 'entry-1', 'entry-2', 'entry-4', 'entry-5', 'entry-6', 'entry-7', 'entry-8', 'entry-9']
1280 first focusable in results => <select data-testid="sort"><option value="review" selected="">Needs review first</option>< | row state=null
1280 queue rows tabindex => [None, None, None, None, None, None, None, None, None]
1280 horiz scroll => False
1280 review-counts => 2 need review · 11 verified
1280 dates-to-confirm => Dates to confirm

None. Every record has a readable date.
1280 tray => Could not verify (0)

Nothing here. Every record produced an entry that passed the code checks.
1280 section order => ['toolbar', 'queue', 'dates-to-confirm', 'rejected-tray', 'side-panels']
1280 why => Why? e7
Close

Quote found word for word, every number in the summary is in the quote, and the second check agreed.

State
verified
Backend
fixture
Generator
claude-sonnet-5-5 · extract_v1
Generator output
Summary: New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered. Excerpt: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.
Code checks
excerpt verbatim: passed
excerpt whole sentence: passed
qualifier carried: passed
date provider from header: passed
summary tokens not in excerpt: none
highlight found: passed
Second check (judge)
supported · claude-haiku-5-5 · judge_faithfulness_v1
Model calls (2)
1280 e8 highlight==excerpt => True
1280 e8 excerpt => C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative chang
1280 hl => C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative chang
1280 errs => []
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-ux-designer-walk.py", line 70, in <module>
    pg.goto(U+"&fail=4"); pg.get_by_test_id("btn-sample").click(); pg.get_by_test_id("btn-analyze").click(); pg.get_by_test_id("timeline").wait_for(timeout=15000)
                                                                                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 13635, in wait_for
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 767, in wait_for
    await self._frame.wait_for_selector(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 395, in wait_for_selector
    await self._channel.send(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for get_by_test_id("timeline") to be visible
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:54:40.402Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/ux_dbg.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nU=\"http://localhost:7865/index.html?api=mock&fail=4\"\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_page(viewport={\"width\":1280,\"height\":900})\n    pg.on(\"pageerror\",lambda e:print(\"ERR\",e)); pg.on(\"console\",lambda m:print(\"CON\",m.type,m.text))\n    pg.goto(U); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for()\n    pg.get_by_test_id(\"btn-analyze\").click(); pg.wait_for_timeout(4000)\n    print(pg.locator(\"main\").inner_text()[:1500])\n    pg.screenshot(path=\"artifacts/review-evidence/T-042-dbg.png\")\nEOF\n.venv/bin/python /private/tmp/claude-501/ux_dbg.py"
}
````

### User / tool · 2026-11-02T01:54:45.145Z

**tool result**
````
1. Records

9 records found

Read by code only. No model has been called yet.

Record 1: Austin EMS run report — January 9, 2026
Record 2: Central ER discharge summary — January 9, 2026
Record 3: Dr. Alvarez, primary care — January 16, 2026
Record 4: Capital PT, initial evaluation — January 23, 2026
Record 5: Capital PT, visit 8 — February 20, 2026
Record 6: Capital PT, visit 9 — March 6, 2026
Record 7: Hill Country Pain Management, new patient — May 18, 2026
Record 8: Austin Imaging, cervical MRI — May 29, 2026
Record 9: Hill Country Pain Management, follow-up — June 12, 2026
Start over
Review
Timeline (8 entries)
1 need review · 10 verified
Order 
Needs review first
By date
2026-01-16
Dr. Alvarez, primary care
Needs review
pending

Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.AI-drafted

Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.

Check: part of the summary isn't fully supported by the quote

Why?
Open record
Accept
Edit
Dismiss
2026-01-09
Austin EMS run report
Verified
pending

Restrained driver rear-ended at approx. 35 mph; reported neck pain 7/10 and headache; transported to Central ER.AI-drafted

41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.
Why?
Open record
Accept
Edit
Dismiss
2026-01-09
Central ER discharge summary
Verified
pending

Diagnosed with cervical strain and concussion without
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:54:48.944Z

**tool call — Bash**
````
{
 "command": "grep -n \"script\" app/frontend/index.html; ls -la app/frontend/*.js | head -20; python3 tools/board.py list 2>/dev/null | grep -E \"T-04[0-6]\""
}
````

### User / tool · 2026-11-02T01:54:49.098Z

**tool result**
````
38:<script src="dom.js"></script>
39:<script src="mock_sample.js"></script>
40:<script src="mock.js"></script>
41:<script src="api.js"></script>
42:<script src="state.js"></script>
43:<script src="input.js"></script>
44:<script src="source.js"></script>
45:<script src="timeline.js"></script>
47:<script src="review.js"></script>
48:<script src="flags.js"></script>
49:<script src="charges.js"></script>
50:<script src="app.js"></script>
-rw-r--r--@ 1 arsis  staff   2150 Nov  1 19:50 app/frontend/api.js
-rw-r--r--@ 1 arsis  staff   2631 Nov  1 19:50 app/frontend/app.js
-rw-r--r--@ 1 arsis  staff   5411 Nov  1 19:52 app/frontend/charges.js
-rw-r--r--@ 1 arsis  staff   1475 Nov  1 19:48 app/frontend/dom.js
-rw-r--r--@ 1 arsis  staff   6430 Nov  1 19:52 app/frontend/flags.js
-rw-r--r--@ 1 arsis  staff   5872 Nov  1 19:52 app/frontend/input.js
-rw-r--r--@ 1 arsis  staff  20005 Nov  1 19:49 app/frontend/mock.js
-rw-r--r--@ 1 arsis  staff   2098 Nov  1 19:49 app/frontend/mock_sample.js
-rw-r--r--@ 1 arsis  staff  16141 Nov  1 19:54 app/frontend/review.js
-rw-r--r--@ 1 arsis  staff   2200 Nov  1 19:50 app/frontend/source.js
-rw-r--r--@ 1 arsis  staff   1388 Nov  1 19:48 app/frontend/state.js
-rw-r--r--@ 1 arsis  staff   9990 Nov  1 19:53 app/frontend/timeline.js
T-040	M3	backend    	in_progress      	P0	AC 0/5	FastAPI routes, demo gate, review/edit/confirm_date with re-check
T-041	M3	backend    	in_review        	P0	AC 6/6	export.py: letter_text and internal_notes_text from accepted items only
T-042	M3	frontend   	in_review        	P0	AC 7/7	Frontend: input, banners, timeline, Why?, rejected tray, source-record modal
T-043	M3	frontend   	in_progress      	P0	AC 0/7	Frontend: flags panel, charges and unclear tray, accept/dismiss controls, keyboard, 375 px
T-044	M3	frontend   	ready            	P0	AC 0/6	Frontend: entry edit with re-check warning, export view, two copy buttons, counts
T-045	M3	qa         	ready            	P0	AC 0/7	Playwright E2E: full paralegal journey, adversarial inputs, all sensors
T-046	M3	frontend   	ready            	P2	AC 0/5	Stretch (first to cut): side-by-side source viewer at >= 1024 px
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:54:57.248Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='artifacts/review-evidence/T-042-ux-designer-walk.py'\ns=open(p).read()\ns=s.replace('pg.goto(U+\"&fail=4\"); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"btn-analyze\").click();','pg.goto(U+\"&fail=4\"); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for(); pg.get_by_test_id(\"btn-analyze\").click();')\ns=s.replace('        pg.reload(); \\n','')\ns=s.replace('    b.close()\\n','''    # dates to confirm via paste of case_01\n    ctx=b.new_context(viewport={\"width\":1280,\"height\":900}); pg=ctx.new_page(); pg.goto(U)\n    pg.get_by_test_id(\"input-text\").fill(open(\"evals/golden/case_01_date_formats.txt\").read()); pg.get_by_test_id(\"btn-analyze\").click()\n    pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n    L(\"case01 dates-to-confirm\",pg.get_by_test_id(\"dates-to-confirm\").inner_text()[:500])\n    pg.get_by_test_id(\"dates-to-confirm\").scroll_into_view_if_needed(); pg.screenshot(path=OUT+\"1280-12-dates-to-confirm.png\")\n    ctx.close()\n    # keyboard walk on sample\n    ctx=b.new_context(viewport={\"width\":1280,\"height\":900}); pg=ctx.new_page(); pg.goto(U); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for(); pg.get_by_test_id(\"btn-analyze\").click(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n    seq=[]\n    for i in range(8):\n        pg.keyboard.press(\"Tab\"); seq.append(pg.evaluate(\"()=>{const a=document.activeElement;return (a.dataset.testid||a.tagName)+':'+(a.textContent||'').trim().slice(0,20)}\"))\n    L(\"kbd tab order after load\",seq)\n    L(\"queue rows tabindex\",pg.evaluate(\"()=>[...document.querySelectorAll('[data-testid=queue] [data-state]')].map(e=>e.getAttribute('tabindex'))\"))\n    r=pg.locator(\"[data-testid=queue] [data-state]\").first; L(\"first row review attr\",r.get_attribute(\"data-review\")); \n    pg.screenshot(path=OUT+\"1280-13-kbd.png\")\n    ctx.close()\n    b.close()\n''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python artifacts/review-evidence/T-042-ux-designer-walk.py 2>&1 | grep -E \"fail4|case01|kbd|tabindex|first focusable|errs|375 (horiz|queue states|progress|section|first)|Traceback|Error\" | cut -c1-700"
}
````

### User / tool · 2026-11-02T01:55:18.677Z

**tool result**
````
1280 first focusable in results => <select data-testid="sort"><option value="review" selected="">Needs review first</option>< | row state=null
1280 queue rows tabindex => ['0', '0', '0', '0', '0', '0', '0', '0', '0']
1280 errs => []
1280 fail4 tray => Could not verify (1)
375 progress => Checking summaries 0 of 9
375 queue states => ['needs_review', 'verified', 'verified', 'verified', 'verified', 'verified', 'verified', 'verified', 'verified']
375 first focusable in results => <select data-testid="sort"><option value="review" selected="">Needs review first</option>< | row state=null
375 queue rows tabindex => ['0', '0', '0', '0', '0', '0', '0', '0', '0']
375 horiz scroll => False
375 section order => ['toolbar', 'queue', 'dates-to-confirm', 'rejected-tray', 'side-panels']
375 errs => []
375 fail4 tray => Could not verify (1)
case01 dates-to-confirm => Dates to confirm
kbd tab order after load => ['start-over:Start over', 'sort:Needs review firstBy', 'entry-3:2026-01-16Dr. Alvare', 'entry-why:Why?', 'btn-source:Open record', 'btn-accept:Accept', 'btn-edit:Edit', 'btn-dismiss:Dismiss']
queue rows tabindex => ['0', '0', '0', '0', '0', '0', '0', '0', '0']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:20.769Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-042-ux-designer-walk.py 2>&1 | grep -A12 -E \"1280 fail4|case01\" | cut -c1-500; ls artifacts/review-evidence/T-042-*.png | wc -l"
}
````

### User / tool · 2026-11-02T01:55:42.182Z

**tool result**
````
1280 fail4 tray => Could not verify (1)

These records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself.

Record 4: Capital PT, initial evaluation
Could not verify

could not process

Could not process this record: the language model did not return a usable answer.

Open record 4
375 banner => Synthetic data only — never paste real records
--
case01 dates-to-confirm => Dates to confirm

These records are left off the timeline and the gap check until you pick the right date. The tool never guesses.

undated
Pemberwick Physical Therapy, visit 1
Needs review
pending

AI summary (mock): Gait mildly antalgic.AI-drafted

Gait mildly antalgic. Pain 4/10.

      27
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:43.111Z

Now the screenshots.

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:43.796Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-1280-07-results.png"
}
````

### User / tool · 2026-11-02T01:55:43.804Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:44.110Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-375-07-results.png"
}
````

### User / tool · 2026-11-02T01:55:44.118Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:44.197Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-1280-10-source8.png"
}
````

### User / tool · 2026-11-02T01:55:44.205Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:51.709Z

**tool call — Bash**
````
{
 "command": "grep -n \"counts\" app/frontend/mock.js | head; grep -n -i \"counts\" docs/api.md | head"
}
````

### User / tool · 2026-11-02T01:55:51.800Z

**tool result**
````
131:    c.review = { queue: c._queue, counts: { pending: n((i) => i.review_status === "pending"), accepted: n((i) => i.review_status === "accepted"), edited: n((i) => i.review_status === "edited"),
172:          progress: { done: Math.round(frac * total), total, label: `Checking summaries ${Math.round(frac * total)} of ${total}` }, counts: { entries: c.entries.length, amounts: c.amounts.length, flags: c.flags.length }, error: null, elapsed_ms: Date.now() - c._run });
ugrep: warning: docs/api.md: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:52.070Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-375-10-source8.png"
}
````

### User / tool · 2026-11-02T01:55:52.077Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:52.546Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-1280-09-why7.png"
}
````

### User / tool · 2026-11-02T01:55:52.564Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:57.607Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/ux_m.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nU=\"http://localhost:7865/index.html?api=mock\"\nwith sync_playwright() as p:\n    b=p.chromium.launch()\n    for W,H in((1280,900),(375,812)):\n        pg=b.new_page(viewport={\"width\":W,\"height\":H}); pg.goto(U); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for(); pg.get_by_test_id(\"btn-analyze\").click(); pg.get_by_test_id(\"timeline\").wait_for()\n        print(W,\"first needs_review top y\",pg.locator(\"[data-state=needs_review]\").first.bounding_box()[\"y\"], \"flags-panel\", pg.get_by_test_id(\"flags-panel\").count() and pg.get_by_test_id(\"flags-panel\").bounding_box()[\"y\"])\n        print(W,\"focus after load:\",pg.evaluate(\"document.activeElement.tagName\"))\n        # chips on a verified row\n        print(W,pg.get_by_test_id(\"entry-1\").locator(\".entry-head\").inner_text().replace(\"\\n\",\" | \"))\n        print(W,\"entry-8 why testids present\", pg.get_by_test_id(\"entry-why\").count())\n        # ?api=mock edit text from unpaired selection: entry-count vs counts line\n        print(W,pg.get_by_test_id(\"review-counts\").inner_text())\n        pg.close()\nEOF\n.venv/bin/python /private/tmp/claude-501/ux_m.py"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:58.178Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-375-11-fail4.png"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:55:58.573Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-1280-06-processing.png"
}
````

### User / tool · 2026-11-02T01:56:03.133Z

**tool result**
````
1280 first needs_review top y 624.5 flags-panel 3108.5
1280 focus after load: BODY
1280 2026-01-09 | Austin EMS run report | Verified | pending
1280 entry-8 why testids present 9
1280 2 need review · 11 verified
375 first needs_review top y 955 flags-panel 4760.5
375 focus after load: BODY
375 2026-01-09 | Austin EMS run report | Verified | pending
375 entry-8 why testids present 9
375 2 need review · 11 verified
````

### User / tool · 2026-11-02T01:56:03.142Z

**tool result**
````
[image]
````

### User / tool · 2026-11-02T01:56:03.143Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:56:13.441Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/ux_t.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nU=\"http://localhost:7865/index.html?api=mock&fail=4\"\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_page(viewport={\"width\":1280,\"height\":900}); pg.goto(U); pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for(); pg.get_by_test_id(\"btn-analyze\").click(); pg.get_by_test_id(\"timeline\").wait_for()\n    pg.get_by_test_id(\"rejected-tray\").get_by_role(\"button\",name=\"Open record 4\").click(); pg.wait_for_timeout(300)\n    print(pg.get_by_test_id(\"record-modal\").inner_text())\n    pg.screenshot(path=\"artifacts/review-evidence/T-042-1280-14-tray-open-record.png\")\nEOF\n.venv/bin/python /private/tmp/claude-501/ux_t.py"
}
````

### User / tool · 2026-11-02T01:56:16.792Z

**tool result**
````
Record 4: Capital PT, initial evaluation
Close
Record 4: Capital PT, initial evaluation
=== Record 4 ===
Date: 2026-01-23
Source: Capital PT, initial evaluation
Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."

The exact position of this quote could not be found in the record, so nothing is highlighted. Check the whole record.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:56:49.914Z

**tool call — Bash**
````
{
 "command": "kill $(cat /private/tmp/claude-501/ux_srv.pid) 2>/dev/null; rm -f artifacts/review-evidence/T-042-dbg.png; cat > reviews/T-042-ux-designer.md <<'EOF'\n# T-042 UX review (ux-designer-reviewer)\n\nVerdict: changes. No blockers. Every T-042 AC behaves as written against the mock API. One major (status count contradicts the visible list) plus minors. Real backend (:7860) was not up, so this is mock-only (`?api=mock`); the real e2e specs were not run. T-043 code (Accept/Edit/Dismiss, flags, charges) was loading in index.html while I reviewed; I did not grade it.\n\nAC check (served `.venv/bin/python -m http.server 7865 --directory app/frontend`, Playwright 1280x900 and 375x812, script `artifacts/review-evidence/T-042-ux-designer-walk.py`):\n1. \"9 records found\" shown before Analyze with text \"Read by code only. No model has been called yet.\" PASS. .pdf refused: \"PDF files can't be read here. Save the records as plain text (.txt) or paste them.\" role=alert, pasted text kept. Empty: \"There is no text to read. Paste records or choose a .txt file.\" Oversize (600,017 chars): \"That is 600,017 characters; the limit is 60,000. Nothing was sent.\" Textarea preserved at full length. PASS.\n2. needs_review (entry-3) first, then verified by date; \"Dates to confirm\" after the queue (pasted case_01 shows the undated row); \"Could not verify\" tray after that. PASS.\n3. Why? on entry 7: state, backend, generator, code checks, judge verdict. PASS.\n4. Entry 8 highlight text == excerpt (True at both widths). PASS.\n5. Synthetic banner visible on empty, found, processing, results and modals at both widths; AI banner on review; `grep -c innerHTML app/frontend/*.js` = 0 for all 12 files. PASS.\n6. `?fail=4`: record 4 in tray with \"could not process\" + reason. PASS.\nNo horizontal scroll at 375. No console or page errors.\n\nScreenshots: artifacts/review-evidence/T-042-{1280,375}-01..11*.png, T-042-1280-12-dates-to-confirm.png, -13-kbd.png, -14-tray-open-record.png.\n\n```json\n{\"card\": \"T-042\", \"persona\": \"ux-designer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"app/frontend (index.html, input.js, timeline.js, source.js, app.js, mock.js) served statically on :7865 with ?api=mock; sample case + case_01 paste + ?fail=4; 1280x900 and 375x812. Real backend not exercised.\",\n \"exercised\": [\"Read personas/ux-designer.md, `python3 tools/board.py show T-042`, tests/e2e/conftest.py contract, test_input/test_timeline/test_source_record\",\n   \"`grep -c innerHTML app/frontend/*.js` -> 0 for all 12 files\",\n   \"Playwright 1280 and 375: empty submit, 600 KB submit, .pdf upload, sample load, Analyze/processing, results, entry-7 Why?, entry-8 Open record, ?fail=4 tray, tray Open record, case_01 paste (Dates to confirm), Tab order\",\n   \"Measured data-state order, tabindex on queue rows, first focusable in results, horizontal scroll, y-offsets of first needs_review row\"],\n \"verdict\": \"changes\",\n \"scores\": {\"design_quality\": 3, \"originality\": 3, \"craft\": 3, \"functionality\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Status count line contradicts the list on screen\", \"evidence\": \"artifacts/review-evidence/T-042-1280-07-results.png: toolbar reads 'Timeline (9 entries)' and 'testid=review-counts' = '2 need review · 11 verified', but the queue has 9 rows and exactly 1 needs_review (entry-3). With ?fail=4: '1 need review · 10 verified' next to 'Timeline (8 entries)'. Source: timeline.js renderReview uses c.review.counts (mock.js:131 counts entries + amounts + flags).\", \"why_it_matters\": \"This is the only status/progress line on the review screen. A paralegal counts one amber row and reads two, or 11 verified of 9 entries, and stops trusting the tool. Visibility of system status and calibrated trust.\", \"fix\": \"Show entry-only counts beside the entry list (e.g. '1 of 9 needs review'), or label the number as covering entries, amounts and flags. Do not print a number that cannot be reconciled with visible rows.\", \"acceptance_test\": \"E2E: text of review-counts needs_review count equals queue rows with data-state=needs_review, and verified+needs_review equals the entry count.\"},\n  {\"severity\": \"minor\", \"title\": \"Tray 'Open record' shows a false red error\", \"evidence\": \"artifacts/review-evidence/T-042-1280-14-tray-open-record.png: opening record 4 from the tray renders role=alert 'The exact position of this quote could not be found in the record, so nothing is highlighted.' source.js:11-14 treats start==null as a failure. Tray items have no quote.\", \"why_it_matters\": \"The expected path for a could-not-verify item reads as a fault, and an alert is announced to screen readers. It undermines the tray's purpose (read it yourself).\", \"fix\": \"When no span is requested, render the record plainly with no alert; keep the alert only when a span was requested but offsets are invalid.\", \"acceptance_test\": \"Open record from the tray: record-modal has no role=alert; open an entry with bad offsets: alert appears.\"},\n  {\"severity\": \"minor\", \"title\": \"Record list pushes the timeline down; first focusable item in results is the sort menu\", \"evidence\": \"At 375 the first needs_review row starts at y=955 (below the 812 fold); at 1280 it starts at y=624; the 9-line records list sits above the timeline after the run (T-042-375-07-results.png). Tab order after load: Start over, sort select, then entry-3 (T-042-1280-13-kbd.png). Checklist 19 wants the first focusable item to be needs_review. The gap flag is at y=3108 (1280) and 4760 (375); that flag belongs to T-043.\", \"why_it_matters\": \"On a returning visit or after Analyze, the reviewer must scroll past input echoes to reach the work. Keyboard users hit a sort control before the first item.\", \"fix\": \"Collapse the records list to a one-line summary ('9 records read') once the case is ready; move the sort control after the queue in DOM order or make the first needs_review row the first tab stop; focus it or scroll to the timeline when the run completes.\", \"acceptance_test\": \"After sample run at 1280x900, entry-3 top < 450 px and is the first focusable element inside the review region.\"},\n  {\"severity\": \"minor\", \"title\": \"Two state chips per row use ambiguous words\", \"evidence\": \"T-042-1280-10-source8.png: rows read 'Verified' + 'pending'. entry head text: '2026-01-09 | Austin EMS run report | Verified | pending'.\", \"why_it_matters\": \"'Verified' (machine check) next to 'pending' (human review) reads as a contradiction; the paralegal cannot tell which one means she still has work.\", \"fix\": \"Label the second chip by what the user owes: 'Not reviewed yet' / 'Accepted' / 'Edited' / 'Dismissed', and label the first 'Machine check: verified'.\", \"acceptance_test\": \"No row shows the bare word 'pending'; both chips carry a noun or prefix that names what they describe.\"},\n  {\"severity\": \"minor\", \"title\": \"Why? panel uses developer vocabulary and an internal id\", \"evidence\": \"T-042-1280-09-why7.png: title 'Why? e7'; rows 'Generator', 'Generator output', 'summary tokens not in excerpt: none', 'judge_faithfulness_v1', 'Backend fixture'.\", \"why_it_matters\": \"The first line is plain ('Quote found word for word...'), but the rest is for engineers. AC requires checks, verdict, state and backend, so keep them, in the user's words.\", \"fix\": \"Title it with the entry (e.g. 'Why? 2026-05-18 Hill Country Pain Management'); rename to 'Draft written by', 'Numbers in summary not in the quote', 'Second check (AI reviewer)'; put model and prompt versions in the collapsed Model calls details.\", \"acceptance_test\": \"why-modal text contains none of: 'e7', 'tokens', 'prompt_version', 'extract_v1' outside the collapsed details.\"},\n  {\"severity\": \"minor\", \"title\": \"Analyze stays clickable during a run; progress is text only\", \"evidence\": \"T-042-1280-06-processing.png: 'Analyze' button still shown and enabled under 'Checking summaries 0 of 9'; no bar. input.js:57 renders Analyze when status==='ingested' and the poll status lags.\", \"why_it_matters\": \"A second click returns an error (409 in the mock) that surfaces as a red alert in the middle of a normal run. The stage text does keep the screen from looking frozen, which is right.\", \"fix\": \"Disable or hide Analyze while status is running and add a progress element (role=progressbar or a simple bar).\", \"acceptance_test\": \"During a run btn-analyze is absent or disabled, and a progress element reports done/total.\"},\n  {\"severity\": \"minor\", \"title\": \"Sticky synthetic banner can cover focused elements\", \"evidence\": \"styles.css .banner.synth{position:sticky;top:0;z-index:5}; at 375 the banner wraps to two lines (~60 px) and overlays scrolled content (T-042-375-11-fail4.png). No scroll-margin-top on [tabindex] rows or buttons.\", \"why_it_matters\": \"Checklist 14: the banner must stay persistent without obscuring a focused control; Tab/scrollIntoView can park the focus under it. Defer severity to accessibility-reviewer.\", \"fix\": \"Add scroll-padding-top equal to the banner height on html, or shorten the mobile text.\", \"acceptance_test\": \"At 375, Tab through 10 controls: each focused element's top >= banner bottom.\"},\n  {\"severity\": \"nit\", \"title\": \"Duplicated modal heading\", \"evidence\": \"T-042-1280-10-source8.png: 'Record 8: Austin Imaging, cervical MRI' appears in the dialog title and again above the record text.\", \"why_it_matters\": \"Wasted vertical space on a 375 px screen.\", \"fix\": \"Drop the inner h3 when it equals the dialog title.\", \"acceptance_test\": \"Single heading per record in the modal.\"}\n ],\n \"whats_right\": [\"Input errors sit under the buttons in plain language, keep the pasted text, and the oversize message says 'Nothing was sent'.\",\n   \"Source modal highlights by API offsets and equals the entry excerpt at both widths; excerpt is on every row without an extra click.\",\n   \"Needs-review rows carry amber with a text chip and a visible 'Check: ...' reason; the could-not-verify tray explains it is not in the letter.\"],\n \"questions_for_chris\": [\"Is 'N need review' in the toolbar meant to count entries only, or entries plus amounts and flags? If the latter it needs its own label.\"]}\n```\nEOF\npython3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T01:56:50.066Z

**tool result**
````
ok (49 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:56:52.441Z

T-042 verdict: **changes**, with no blockers, because all 7 ACs pass against the mock API. The real backend wasn't up, so the real e2e specs weren't run. One major: the "2 need review · 11 verified" line sits beside "Timeline (9 entries)" and 1 amber row, so the numbers can't be reconciled. The rest are minors and a nit, including a false red error when you open a record from the could-not-verify tray.
Review is at `/Users/arsis/zlayt-pm-project/reviews/T-042-ux-designer.md` (board validate: ok, 49 files), with screenshots and the walk script under `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-*`.
One question for Chris: should that count cover entries only, or also amounts and flags?
