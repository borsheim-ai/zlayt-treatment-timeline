# Subagent: Frontend: T-211 expose judge + HITL (Frontend: T-211 expose judge + HITL)

Source: `agent-a0f33ff7cf5bea78a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T04:34:11.852Z

You are the frontend worker in /Users/arsis/zlayt-pm-project. Your card is T-211, P0; claim it. Read D-074, D-065, D-066 and D-069 in memory/ORCHESTRATOR_DECISIONS.md, docs/LLM_VS_CODE.md, submission/validation-ladder.svg, memory/contracts/api.md (the item trace and judge fields), and the current guided UI in app/frontend/guided/.

Context: Chris is handing Zlayt only the demo and the repo, so the app itself must show and explain the AI checks and the human in the loop. Build two things.

**1. "How this was checked" on every Step 2 and Step 3 item.** Show three rows, in plain words:
- **Code check:** what code verified, e.g. "the quote is word-for-word in the record" or "the amount appears in the record".
- **Second AI check:** a different model with a different prompt. Show its verdict (agrees / disputes / could not check) and its one-line reason from the API. For prepared demo answers, say "Prepared by our team; the second AI check then checked it against the quote" (D-065).
- **You:** the user's decision, or "Waiting for you".

Keep it compact, for example a small three-row panel under the quote. It must not push the primary action below the fold at 1440x900, and it must fit at 390px.

**2. A "How each answer is checked" page,** linked from the header on every screen.
- Explain in about 150 words: AI drafts or prepared answers, then code checks (dates, amounts, exact quotes), then an independent AI judge with a different prompt and model, then you accept, edit or dismiss. Nothing reaches the letter without all three.
- Show the validation-ladder graphic: copy submission/validation-ladder.svg into app/frontend/guided/.
- Say what is code and what is AI, linking to the repo doc names in text.

**Also:** Step 3 must read `service_date.date_label` (new in T-202 r6) so record blanks say "record dated", not "statement dated".

Add e2e tests for the panel on items and the page, with no console errors, at 390px and 1440px. Run the full tests/e2e from a fresh `git archive` (E2E_REQUIRE_DB=1) and report the count. Commit only your paths through `git commit` with a temp index from the current HEAD. Write the handoff, move the card to in_review, and reply in 2 lines.

### User / tool · 2026-11-03T04:34:11.857Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:13.921Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-211 --agent frontend; $B show T-211; git log --oneline | head -3; git status --short | head -20"
}
````

### User / tool · 2026-11-03T04:34:14.162Z

**tool result**
````
T-211 claimed by frontend
---
id: "T-211"
title: "Guided UI exposes and explains the validation ladder: per-item code check, second AI check (judge) verdict + reason, your decision; a 'How each answer is checked' page from every screen"
milestone: "M4"
role: "frontend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T04:33:55Z"
updated_at: "2026-11-03T04:34:14Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T04:34:14Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "on every Step 2/3 item a visible 'How this was checked' section shows the code check result, the judge verdict and its reason (or 'prepared by our team' per D-065 plus the judge result), and the user's decision; a How-it-works page (header link) explains code check -> independent AI judge (different prompt/model) -> you decide, with the validation-ladder graphic; plain words; e2e + 390px; no console errors", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T04:34:14Z frontend: claimed

## Handoff (filled when moving to in_review)

9655f1d test(backend): T-202 r6 pin the 60-character UB-04 label window in production and the check; drop the unreachable statement-date branches of the check
756546b test(backend): T-202 r6 pin pipe cells, no-date bound, unlocated figure and visit ranges; heading cells gate the From/To pairing alone
3654cf9 test(backend): T-202 r6 sample letter golden chain: spec REQUIREMENTS block 1+2 and the hand-built export case carry the MRI blank and the new notes section
MM .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
D  .claude/agent-memory/backend/project_t202_r5_d073.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:14.844Z

**tool call — Bash**
````
{
 "command": "grep -n \"^## D-074\\|^### D-074\\|D-074\\|D-065\\|D-066\\|D-069\" memory/ORCHESTRATOR_DECISIONS.md | head -20; ls app/frontend/guided/ ; wc -l app/frontend/guided/*; ls tests/e2e | head -50"
}
````

### User / tool · 2026-11-03T04:34:14.939Z

**tool result**
````
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
74:| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
78:## D-069 — T-177 after 3 rounds: replace the swap table with a property test (§7.4)
79:Round 3 fixed the shipped sample but the failure paths (malformed or missing curated answer) still leak model names and "AI" wording through a word-swap table. A fourth round is authorised with a structural change instead of more swaps: (1) when an item or case is prepared, every user-facing string is built from a prepared-specific template keyed by the provenance field, never by rewriting AI text; (2) a malformed curated answer is treated as missing (never falls back to a model label); (3) a property test runs the demo over fault-injected curated sets (valid, malformed, missing, empty) for the sample and two library cases and fails if any API response for a prepared item or case matches /\bAI\b|claude|sonnet|haiku|opus|model/i outside the D-065 tooltip sentence. If round 4 fails, the demo hides failed prepared items behind one plain sentence ("This answer is not available in the demo") and the residual goes to SCOPE_CUTS.
102:## D-074 — The deliverable is the demo plus the repo (Chris, 2026-11-03)
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
     170 app/frontend/guided/app.js
     145 app/frontend/guided/core.js
      26 app/frontend/guided/home.css
     199 app/frontend/guided/home.js
      35 app/frontend/guided/index.html
     110 app/frontend/guided/review.css
     437 app/frontend/guided/review.js
      68 app/frontend/guided/step1.css
     303 app/frontend/guided/step1.js
       2 app/frontend/guided/step2.css
     387 app/frontend/guided/step2.js
      33 app/frontend/guided/step3.css
     153 app/frontend/guided/step3.js
      28 app/frontend/guided/step4.css
     173 app/frontend/guided/step4.js
     454 app/frontend/guided/styles.css
    2723 total
__init__.py
__pycache__
_scripted_server.py
conftest.py
guided
test_adversarial.py
test_adversarial_ui.py
test_api.py
test_change_the_quote.py
test_charge_confirm.py
test_charges.py
test_code_check_refusal.py
test_conflict_coverage.py
test_conflict_skipped.py
test_count_charge.py
test_count_duplicate.py
test_demo_provenance.py
test_edit.py
test_edit_to_check.py
test_export_ui.py
test_flags_panel.py
test_held_quote_gate.py
test_input.py
test_journey_modes.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_letter_matrix.py
test_local_mode.py
test_multicase.py
test_mvp_finish.py
test_mvp_polish.py
test_no_console_errors.py
test_polish_r3.py
test_polish_r4.py
test_polish_r5.py
test_prepared_first_paint.py
test_rerun_judge.py
test_rerun_note.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
test_two_cases_side_by_side.py
test_uncovered_ui.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:16.515Z

**tool call — Bash**
````
{
 "command": "sed -n 100,115p memory/ORCHESTRATOR_DECISIONS.md; cat submission/validation-ladder.svg | head -60; cat app/frontend/guided/index.html; cat app/frontend/guided/app.js"
}
````

### User / tool · 2026-11-03T04:34:16.603Z

**tool result**
````
- D-073 round-6 rules (§7.4, final; staff r5 + paralegal r5): (1) encounter_types.json holds whole document-type phrases only ("MRI report", "progress note", "emergency department record", "physical therapy note", "ambulance run report", "operative report", "discharge summary", "office visit note"); no single words (MRI, exam, evaluation, follow-up, new patient), because they occur in provider names; (2) a date-of-service column needs a real table: a header row naming at least two columns including the DOS column, and at least two data rows with a date in that column position; a lone "Date of service: X" line or a sentence mentioning DOS is not a heading; (3) several candidate dates, a month-year phrase or an "earlier/next/previous" phrase in the encounter sentence -> blank, each pinned by a test; the UB-04 period gets the same guard; (4) a blank on a non-bill record reads "(record dated X)", on a bill "(statement dated X)"; (5) the duplicate-promotion flag message never prints a prose date. The sample truths fix no charge dates, so sample lines may become blanks. If round 6 still prints a wrong date, the MVP letter prints the fillable blank on every charge line (no date extraction at all) and SCOPE_CUTS 28 covers it.

## D-074 — The deliverable is the demo plus the repo (Chris, 2026-11-03)
Chris will hand Zlayt only the running demo and the repo. So: (1) README.md is the front door: what it is, a two-command setup that works from a fresh clone, a 3-minute guided walk of the demo, and where the LLM-as-judge and the human-in-the-loop live (code, prompts, evals, decisions), with the validation-ladder diagram; (2) the app itself exposes and explains the ladder: each item shows its code check, the second AI check (judge) verdict and reason, and the human decision, and a plain "How each answer is checked" page is reachable from every screen; (3) the submission packet (checklist, product note, Part 2, prompt log) stays in submission/ and is linked from the README; (4) after T-184/T-188 an independent reviewer double-checks the assets and the packet.
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 600" width="820" height="600" font-family="-apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="t d">
  <title id="t">Validation ladder: nothing an AI wrote reaches the letter without a code check, a second model, and the paralegal</title>
  <desc id="d">A record's text goes to a model that drafts a summary and quote. Rung 1, code, checks the quote word for word and every number. Rung 2, a second model with a different prompt, answers a fixed choice. Code computes the state. Rung 3, the paralegal, accepts, edits or dismisses; a named confirm for a disputed summary is in progress. Code assembles the export from accepted items only. Items that fail are shown in a could-not-verify list and never exported. A separate code-only lane handles dates, gaps and amounts with no model; a model may only point at cut offsets for a paste code cannot split.</desc>
  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker>
  </defs>
  <rect width="820" height="600" fill="#ffffff"/>

  <!-- column headers -->
  <text x="20" y="26" font-size="13" font-weight="700" fill="#111">Language work: model drafts, then three checks</text>
  <text x="560" y="26" font-size="13" font-weight="700" fill="#111">Single right answer: code only</text>

  <!-- input -->
  <rect x="20" y="40" width="470" height="44" rx="6" fill="#f3f3f3" stroke="#888"/>
  <text x="34" y="60" font-size="12.5" font-weight="700" fill="#111">Record text</text>
  <text x="34" y="76" font-size="11.5" fill="#333">Untrusted data. Never treated as instructions. Models run with no tools.</text>

  <path d="M255,84 V104" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>

  <!-- generator -->
  <rect x="20" y="106" width="470" height="62" rx="6" fill="#e8f0fe" stroke="#3b6fd4"/>
  <text x="34" y="126" font-size="12.5" font-weight="700" fill="#0b3a8c">AI draft (generator model)</text>
  <text x="34" y="143" font-size="11.5" fill="#222">One-line summary + exact quote; flag category + quote.</text>
  <text x="34" y="158" font-size="11.5" fill="#222">Never supplies a date, an amount, or the wording of a warning.</text>

  <path d="M255,168 V188" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>

  <!-- rung 1 -->
  <rect x="20" y="190" width="470" height="86" rx="6" fill="#e9f6ec" stroke="#2f8f4e"/>
  <text x="34" y="210" font-size="12.5" font-weight="700" fill="#14572b">Rung 1: code check</text>
  <text x="34" y="227" font-size="11.5" fill="#222">Quote is in the record word for word (whole sentences).</text>
  <text x="34" y="242" font-size="11.5" fill="#222">Every number, date, $ figure, left/right, no/not/without is in the quote.</text>
  <text x="34" y="257" font-size="11.5" fill="#222">Hedges in the quote ("may represent", "approx.") are kept in the summary.</text>
  <text x="34" y="270" font-size="11.5" fill="#222">Clauses the quote does not support are removed by code, and shown.</text>

  <path d="M255,276 V296" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>

  <!-- rung 2 -->
  <rect x="20" y="298" width="470" height="70" rx="6" fill="#fdf3e0" stroke="#c78a1b"/>
  <text x="34" y="318" font-size="12.5" font-weight="700" fill="#7a4d00">Rung 2: independent second model (judge)</text>
  <text x="34" y="335" font-size="11.5" fill="#222">Different prompt and model. Sees only the record and the candidate.</text>
  <text x="34" y="350" font-size="11.5" fill="#222">Answers with a fixed choice and a reason code, never prose.</text>
  <text x="34" y="363" font-size="11.5" fill="#222">Disagree, unsure or no answer: the item is marked needs review.</text>

  <path d="M255,368 V388" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>

  <!-- state -->
  <rect x="20" y="390" width="470" height="40" rx="6" fill="#f3f3f3" stroke="#888"/>
  <text x="34" y="407" font-size="12.5" font-weight="700" fill="#111">State, computed by code</text>
  <text x="34" y="422" font-size="11.5" fill="#333">verified or needs review. Needs review sorts first. Verified is not accepted.</text>

  <path d="M255,430 V450" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>

  <!-- rung 3 -->
  <rect x="20" y="452" width="470" height="72" rx="6" fill="#f6e9f7" stroke="#8e44a0"/>
  <text x="34" y="472" font-size="12.5" font-weight="700" fill="#5a1f69">Rung 3: the paralegal decides</text>
  <text x="34" y="489" font-size="11.5" fill="#222">Accept, edit or dismiss, one item at a time, quote beside the line.</text>
  <text x="34" y="504" font-size="11.5" fill="#222">In progress (D-066, T-179): a summary the judge disputed</text>
  <text x="34" y="518" font-size="11.5" fill="#222">will need a named "I compared it with the quote."</text>

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
  // A case whose lines were written by a model (models.generator_prepared === false) is never described as prepared by the team, even when the server's curated set is on (T-181 r2, paralegal minor).
  G.provenance = function (c) {
    const hl = G.store.health, cur = c === undefined ? G.store.current : c, notPrepared = !!(cur && cur.models && cur.models.generator_prepared === false);
    const kind = hl && hl.demo_mode ? (hl.answers === "prepared" && !notPrepared ? "prepared" : "recorded") : "live";
    // T-204 r3: until /api/health says whose answers these are, the footer makes no claim about who wrote them (a prepared sample must never flash "drafted by AI", and a failed health call leaves the neutral line)
    return { kind, pending: !hl, label: DEMO[kind] ? DEMO[kind][0] : "", note: DEMO[kind] ? DEMO[kind][1] : hl ? "Summaries and warnings are drafted by AI and checked by code; you decide every item." : "Checked by code; you decide every item.",
      hours: hl && !hl.demo_mode ? hl.retention_hours : null };
  };
  function drawBanner() {
    const hl = G.store.health, p = G.provenance();
    $("#banner-text").textContent = (hl && hl.banner) || "Synthetic data only — never paste real records";
    $("#banner-demo").textContent = p.label;
    const f = $("#footer"); f.replaceChildren(...[h("span", { "data-testid": "footer-note" }, p.label ? p.label + ". " + p.note : p.note),
      p.hours ? h("span", { class: "f-live" }, `Pasted text is deleted after ${p.hours} hours.`) : null].filter(Boolean));     // replaceChildren(null) would print the text "null"
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
  G.store.healthP = G.api.health();
  G.store.healthP.then((hl) => { G.store.health = hl; drawBanner(); drawHeader(); G.emit("health", hl); }).catch(() => { /* the static banner stays; pages that need health read G.store.health and cope with null */ });

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
    G.store.current = null; headerState = { title: r.name === "new" ? "New case" : null, sub: null }; drawHeader(); drawBanner();
    let c = null;
    const ctx = {
      route: r.name, token: r.token, step: r.step, query: r.query, case: null, signal: ctrl.signal, view, get health() { return G.store.health; },
      layout: (m) => setLayout(m), go: G.go,
      setStepStatus: (n, text, state) => { (overrides[r.token] = overrides[r.token] || {})[n] = [text, state]; if (!stale()) drawBar(r.name, r.token, ctx.case, r.step); },
      setCaseTitle: (t) => { if (!stale()) { headerState.title = t; drawHeader(); } },
      setTitle: (t) => { if (!stale()) document.title = t + " – " + TITLE; },
      refresh: async () => { const j = await G.store.load(r.token, ctrl.signal); if (!stale()) { ctx.case = j; paintCase(j); } return j; },
    };
    function paintCase(j) { G.store.current = j; drawBanner(); headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, r.token, j, r.step); }
    drawBar(r.name, r.token, G.store.cases[r.token] || null, r.step);
    try {
      if (r.token) {
        try { c = await G.store.load(r.token, ctrl.signal); }
        catch (e) {
          if (e && e.name === "AbortError") return; if (stale()) return;
          setLayout("page"); drawBar(r.name, r.token, null, r.step);
          view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, e.status === 404 ? null : () => render(), e.status === 404 ? "This case is no longer here" : "We couldn't open this case")));
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
  G.on("case", (token, j) => { const r = now; if (r && r.token === token && r.name !== "redirect") { G.store.current = j; drawBanner(); headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, token, j, r.step); } });
  drawBanner(); drawHeader();
  render();
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:16.968Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"judge\\|trace\\|date_label\\|provenance\\|prepared\\|code_check\\|checks\" memory/contracts/api.md | head -80"
}
````

### User / tool · 2026-11-03T04:34:17.055Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:19.289Z

**tool call — Bash**
````
{
 "command": "grep -n -o -i \".\\{120\\}date_label.\\{200\\}\" memory/contracts/api.md | head -5; echo ----; grep -n -i \"judge_verdict\\|judge_reason\\|\\\"judge\\|judge:\" memory/contracts/api.md | cut -c1-400 | head -20; echo ---; grep -n \"trace\" memory/contracts/api.md | cut -c1-300 | head"
}
````

### User / tool · 2026-11-03T04:34:19.400Z

**tool result**
````
574: dated June 15, 2026)", "statement_date_iso": "2026-06-19"|null (the record's date; for a bill it is the statement's), "date_label": "statement"|"record" (T-202 r6: what that date is called: "statement" for a bill, "record" for any other record, so a client labels it "statement dated" or "record dated" and never calls an ED reco
----
51:  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
128:{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "judge_entries",
129:  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
134:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item fro
147:  "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
172:        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": "c21", "verdict": "supported"},
184:        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c31", "verdict": "agrees"},
190:      "review_status": "pending", "edited": null, "duplicate_note": null, "flag": null, "confirm_required": false, "accept_effect": "acknowledge", "judge_required_for_export": false,
194:        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c33", "verdict": "agrees"},
218:        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
232:        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
244:        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_flag_v2", "call_id": "c44", "verdict": "agrees"},
321:{ "item": { "id": "e4", "kind": "entry", "state": "needs_review", "reasons": ["JUDGE_PARTIAL"],
329:    { "id": "c27", "role": "judge", "step": "judge_entries", "backend": "fixture",
330:      "model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "attempt": 1,
363:{ "item": { "id": "e3", "review_status": "edited", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"],
368:  "warnings": [ {"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": "e3"} ] }
384:**D-066 (T-179): a disputed item is accepted only with her compare.** An item the second AI check disputed is one whose `ladder.judge.verdict` is `partially`, `unsupported`, `disagrees` (or the amount judge's `disagree`), or whose `reasons` hold `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_DISAGREES` (`unsure` / `unavailable` are not an objection). `POST .../items/{id}/review {action: "accep
402:- Anything not allowed: `422 reclassify_refused`, nothing changes, no event: `{error: {code, message, detail: {reason, check: "code"|"judge", wording?, error_class?}}}`. `detail.reason` is one of `NO_VALUE`, `INJECTION_SUSPECTED`, `NO_CHARGE_WORDING` (check `code`), `JUDGE_DISAGREES`, `JUDGE_UNSURE`, `JUDGE_UNAVAILABLE` (check `judge`; `JUDGE_UNAVAILABLE` includes no recorded answer in demo mo
404:- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: "reclassify", kind, wording, judge_verdict, judge_call_id, restored, note}`, `before` carries `{kind, review_status, state}`. The judge call is in `llm_calls` with `item_id`. The item's `ladder.reclassif
---
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409, re-run of a case that already has d
37:| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
38:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
109:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an ed
139:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `co
284:- A gap that starts or ends at record(s) that ALL look administrative has `computed.endpoint_warnings` (always present, `[]` when none) entries `{side: "start"|"end", record_no, record_type, date, warning, alternative, alternative_days, alternative_from, alternative_to}`. `warning` = "This gap e
376:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to expo
378:- Item trace (`GET /items/{id}/trace`, the "Why this status" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with "You edited this item; it is not accepted until you compare it with the quote a
380:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summa
417:**Flags that need a named confirm (D-059).** A charge can carry `flag` (else `null`): `{flag: "likely_duplicate" | "likely_total", name, message, confirm_with, of, confirmed_at?}` and `confirm_required: true` while it is `pending`. `likely_duplicate`: set only when a paralegal PROMOTES a figure
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:19.590Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/guided/step2.js"
}
````

### User / tool · 2026-11-03T04:34:19.671Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:21.329Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/step2.js",
 "offset": 30
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:21.410Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/step3.js"
}
````

### User / tool · 2026-11-03T04:34:21.418Z

**tool result**
````
1	/* Step 3: Check the bills (/case/<token>/bills[?item=<id>]). OWNER: frontend-B. Spec 6 (6.1 charge, 6.2 countable with a check, 6.3 never counted, 6.4 done); D-059 (a flagged charge needs its named confirm), D-060/D-064 (a line held back
2	   only for a missing detail is counted with count + confirm separate_charge), D-062 (the letter's total line), D-066 (compare box when the second check disputed the amount), T-178 (version + expected_status: review.js).
3	   Charges are never batched: there is no "count all". Record text, figures and reasons go in with textContent only. */
4	(function () {
5	  const G = window.G, { h } = G, R = G.review;
6	
7	  /* ---------- the queue (6): charges and countable amounts first (record order, then position), then the amounts that are never counted ---------- */
8	  const live = (c) => (c.amounts || []).filter(G.steps.live);
9	  const kindOf = (a) => (a.kind === "charge" ? "charge" : a.countable ? "count" : "never");
10	  function buildQueue(c) {
11	    const recs = Object.fromEntries((c.records || []).map((r) => [r.id, r]));
12	    const seq = (a) => { const r = recs[(a.record_ids || [])[0]]; return r ? r.seq : 9999; };
13	    return live(c).slice().sort((a, b) => (kindOf(a) === "never") - (kindOf(b) === "never") || seq(a) - seq(b) || (a.excerpt_start || 0) - (b.excerpt_start || 0) || (a.id < b.id ? -1 : 1)).map((a) => ({ id: a.id }));
14	  }
15	  const find = (c, id) => (c.amounts || []).find((a) => a.id === id) || null;
16	  const cents = (a) => (a.value_cents == null ? null : a.value_cents);
17	  const hasDollar = (t) => /\$\s*\d|\d\s*(?:USD|dollars)/i.test(t || "");
18	  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the statement date whenever it is not that day. Code only, no guessing. */
19	  const sdOf = (a) => (a && a.service_date && typeof a.service_date === "object" ? a.service_date : null);
20	  const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, not the day of the service
21	  /* T-206: a record's date is shown bare only when it is a certain service date. An amount with no service_date of its own (a ledger line not counted yet, a UB-04 or invoice total) never has one: a bill document's date is its statement's. */
22	  const BILL_DOC = /\b(ledger|invoice|statement|UB-?04|CMS-?1500|HCFA|EOB|explanation of benefits|itemi[sz]ed|billing|bill)\b/i;
23	  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
24	  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? "statement dated " + d : d) : "no date"; };
25	  const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, st)}`;
26	  const figure = (a) => (cents(a) != null ? R.money(cents(a)) : a.text || "");
27	  const FLAG_BOX = { likely_duplicate: "I checked: this is a separate charge, not the same one counted twice.", likely_total: "I checked: this is a charge of its own, not a total of the others." };
28	  const flagBox = (f) => FLAG_BOX[f.flag] || `I checked: ${String(f.name || f.flag || "this is right").replace(/\.$/, "")}.`;
29	
30	  /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
31	  const dateLine = (sd) => h("p", { class: "svc-date gap-top", "data-testid": "service-date", "data-state": sd.state },
32	    /^date of service/i.test(sd.text || "") ? null : h("span", { class: "label-cap" }, "Date of service "), h("b", { "data-testid": "service-date-text" }, sd.text || ""),
33	    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · statement dated ${R.longDate(sd.statement_date_iso)}`) : null);
34	  const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
35	  /* T-206/T-209 r3: the note above states the specific reason; this sentence is the same for every reason that is not certain, so it can never contradict the note: find the date outside this card's guess, write it in the letter's blank. The card has no control to type a date. */
36	  const confirmNext = (sd) => {
37	    const stmt = /\(statement dated/.test((sd && sd.text) || "") ? " The date in parentheses is the statement date, not the service date." : "";
38	    return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b", {}, "\u201Cdate of service [__________]\u201D"), " in your letter." + stmt,
39	      " Counting it adds the amount to the bill total.");
40	  };
41	
42	  function present(S, item) {
43	    const kind = kindOf(item), recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), rec = recs[0];
44	    const sd = sdOf(item), st = stmtDated(item, sd, rec);
45	    const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
46	    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r)) : null }));
47	    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, st) : "", nodes: srcNodes };
48	    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
49	    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null);
50	    const decided = item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited";
51	    const flag = item.flag && item.confirm_required ? item.flag : null;
52	    const note = item.duplicate_note ? h("p", { class: "explain muted gap-top", "data-testid": "duplicate-note" }, R.plain(item.duplicate_note)) : null;
53	    const compareBox = () => R.check(S, "compare", "I read this amount against the highlighted words myself.");
54	    const compareFoot = () => [h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you decide.", compareBox()];
55	    const ticked = (k) => R.ticked(S, k);
56	
57	    if (kind === "charge") {
58	      const foot = []; let cls = "plain";
59	      if (flag) { cls = "attn"; foot.push(h("strong", { "data-testid": "flag-message" }, R.plain(flag.message)), R.check(S, "flag", flagBox(flag))); }
60	      if (disp) { cls = "attn"; if (flag) foot.push(h("hr", { class: "foot-rule" })); foot.push(...compareFoot()); }
61	      if (!flag && !disp) {
62	        if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "not counted." : "counted in the bill total.", " You can change it."); }
63	        else if (!(sd && sd.confirm_note)) foot.push("If you count it, it's added to the bill total in the letter, with the highlighted words as its source.");
64	      }
65	      return { tag: { cls: "ok", text: "Charge" }, sub, src,
66	        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), sd ? dateLine(sd) : null, h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
67	        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), confirmNext(sd), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
68	        question: "Should this charge count toward the bill total?",
69	        yes: { label: "Yes, count it", disabled: () => (!!flag && !ticked("flag")) || (!!disp && !ticked("compare")),
70	          run: () => S.decide(item, "accept", { ...(flag ? { confirm: flag.confirm_with } : {}), ...(disp && ticked("compare") ? { compared: true } : {}) }) },
71	        no: { label: "No, don't count it", run: () => S.decide(item, "dismiss") }, third: null };
72	    }
73	
74	    if (kind === "count") {
75	      const cc = item.count_confirm, foot = [h("span", { "data-testid": "count-hint" }, "You can still count it if you checked the ledger yourself."), R.check(S, "separate", "I checked this is a separate charge for a service.")];
76	      if (cc) foot.push(h("p", { class: "foot-warn", "data-testid": "count-confirm-message" }, R.plain(cc.message)), R.check(S, "flag", flagBox(cc)));
77	      if (disp) foot.push(h("hr", { class: "foot-rule" }), h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), compareBox());
78	      return { tag: { cls: "warn", text: "Not counted yet" }, sub, src,
79	        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
80	        foot: { cls: "attn", nodes: foot },
81	        question: "Should this amount count toward the bill total?",
82	        yes: { label: "Yes, count it", disabled: () => !ticked("separate") || (!!cc && !ticked("flag")), run: () => S.decide(item, "count", { confirm: "separate_charge", ...(cc ? { confirm_flag: cc.confirm_with } : {}) }) },
83	        no: { label: "No, don't count it", disabled: () => !!disp && !ticked("compare"), run: () => S.decide(item, "accept", disp && ticked("compare") ? { compared: true } : undefined) }, third: null };
84	    }
85	
86	    const foot = [];
87	    let cls = "plain";
88	    if (disp) { cls = "attn"; foot.push(...compareFoot()); }
89	    else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "left out of the notes." : "listed in the notes for the attorney.", " It is never added to the bill total."); }
90	    else foot.push("Either way, it is never added to the bill total.");
91	    const money = hasDollar(item.text);
92	    return { tag: { cls: "never", text: "Never counted" }, sub, src,
93	      body: [money ? h("p", { class: "money", "data-testid": "figure" }, item.text) : h("p", { class: "line-text", "data-testid": "figure" }, h("span", { class: "muted" }, "Not a money amount: "), item.text || ""),
94	        h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
95	      foot: { cls, nodes: foot },
96	      question: "This amount is never added to the total. List it in the notes for the attorney?",
97	      yes: { label: "Yes, list it", disabled: () => !!disp && !ticked("compare"), run: () => S.decide(item, "accept", disp && ticked("compare") ? { compared: true } : undefined) },
98	      no: { label: "No, leave it out", run: () => S.decide(item, "dismiss") }, third: null };
99	  }
100	
101	  function statusFor(S, item, resp, action) {
102	    const f = item ? figure(item) : "this amount", kind = item ? kindOf(item) : "never";
103	    if (action === "count") return `${f} counted in the bill total`;
104	    if (action === "dismiss") return kind === "never" ? `${f} left out of the notes` : `${f} not counted`;
105	    if (kind === "charge") return `${f} counted in the bill total`;
106	    if (kind === "count") return `${f} not counted. It is noted for the attorney`;
107	    return `${f} listed in the notes for the attorney`;
108	  }
109	
110	  /* ---------- 6.4 done ---------- */
111	  function letterLine(c) { const t = c.totals || {}; return t.letter_line || `Billed charges accepted from these records: ${R.money((t.accepted || {}).cents || 0)}`; }
112	  function done(S) {
113	    const c = S.c, items = S.counted().map((q) => S.item(q.id)), recs = Object.fromEntries((c.records || []).map((r) => [r.id, r]));
114	    const left = items.filter(G.steps.undecided), changeHref = (a) => G.url.bills(S.token, a.id);
115	    const from = (a) => { const r = recs[(a.record_ids || [])[0]]; return r ? r.source_label || "" : ""; }, when = (a) => {
116	      const sd = sdOf(a); if (sd && sd.text) return sd.text;          // the letter's own date text
117	      const r = recs[(a.record_ids || [])[0]], d = r && r.date_iso ? R.longDate(r.date_iso) : "", by = a.ladder && a.ladder.code_checks && a.ladder.code_checks.classified_by;
118	      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's
119	    };
120	    const counted = items.filter((a) => a.kind === "charge" && (a.review_status === "accepted" || a.review_status === "edited") && !a.edit_to_check);
121	    const notCounted = items.filter((a) => (a.kind === "charge" && a.review_status === "dismissed") || (a.kind !== "charge" && a.countable));
122	    const never = items.filter((a) => a.kind !== "charge" && !a.countable);
123	    const row = (a, cols) => h("tr", { "data-testid": "bill-row", "data-item": a.id }, h("td", { class: "amt" }, !(a.kind === "charge" || a.countable) ? (hasDollar(a.text) ? a.text : "Not a money amount: " + (a.text || "")) : figure(a)), ...cols.map((x) => h("td", {}, x)), h("td", {}, h("a", { class: "btn", href: changeHref(a), "data-testid": "btn-change" }, "Change")));
124	    const table = (head, rows) => {
125	      rows.forEach((tr) => [...tr.children].forEach((td, i) => td.setAttribute("data-label", i < head.length ? head[i] : "")));       // phones show each row as a small card: the label comes from here
126	      return h("table", { class: "mini" }, h("thead", {}, h("tr", {}, ...head.map((x) => h("th", {}, x)), h("th", {}))), h("tbody", {}, rows));
127	    };
128	    const overlaps = ((c.totals || {}).possible_overlaps || []);
129	    const hero = left.length
130	      ? h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "!"), h("div", {}, h("h2", { "data-testid": "done-heading" }, `${left.length} amount${left.length === 1 ? " still needs" : "s still need"} a decision.`), h("p", {}, "Amounts you don't decide stay out of the bill total.")))
131	      : h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "You checked every bill amount."), h("p", {}, "This is the total line your letter will carry:")));
132	    return R.doneFrame(3, "Check the bills",
133	      h("div", { class: "panel" }, hero, h("p", { class: "total-line num", "data-testid": "letter-line" }, letterLine(c)),
134	        h("div", { class: "row-actions" }, left.length ? h("a", { class: "btn primary lg", href: G.url.bills(S.token, left[0].id), "data-testid": "btn-first-undecided" }, "Go to the first one") : null,
135	          h("a", { class: "btn lg " + (left.length ? "" : "primary"), href: G.url.letter(S.token), "data-testid": "btn-next-step" }, "Go to step 4: Get your letter"))),
136	      ...overlaps.map((o) => h("div", { class: "note-box overlap", "data-testid": "overlap" }, h("div", { class: "nb-text" }, "Check these two amounts", h("span", {}, R.plain(o.message))),
137	        h("div", { class: "row-actions tight" }, [o.statement_amount_id, o.covered_amount_id].map((id, i) => h("a", { class: "btn", href: G.url.bills(S.token, id) }, `Change ${i ? o.covered_text : o.statement_text}`))))),
138	      h("div", { class: "panel", "data-testid": "list-counted" }, h("h2", {}, `Counted (${counted.length})`),
139	        counted.length ? table(["Amount", "From", "Date of service"], counted.map((a) => row(a, [from(a), when(a)]))) : h("p", { class: "muted" }, "You didn't count any charge.")),
140	      h("div", { class: "panel", "data-testid": "list-not-counted" }, h("h2", {}, `Not counted by you (${notCounted.length})`),
141	        notCounted.length ? table(["Amount", "From", "Why"], notCounted.map((a) => row(a, [from(a), a.kind === "charge" ? "You chose not to count it." : R.plain(a.not_counted_reason || "")]))) : h("p", { class: "muted" }, "You didn't leave out any charge.")),
142	      h("div", { class: "panel", "data-testid": "list-never" }, h("h2", {}, `Never counted (${never.length})`), h("p", { class: "muted" }, "These are never added to the total. The ones you listed go in the notes for the attorney."),
143	        never.length ? table(["Amount", "From", "Why it's never counted"], never.map((a) => row(a, [from(a), R.plain(a.not_counted_reason || "")]))) : null));
144	  }
145	  function empty(S) {
146	    return R.doneFrame(3, "Check the bills", h("div", { class: "panel" }, h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "–"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "We didn't find any bill amounts in these records."), h("p", {}, "There is nothing to count."))),
147	      h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: G.url.letter(S.token), "data-testid": "btn-next-step" }, "Go to step 4: Get your letter"))));
148	  }
149	
150	  G.pages.bills = function (ctx) {
151	    return R.run(ctx, { step: 3, title: "Check the bills", unit: "Amount", chip: true, buildQueue, find, present, statusFor, done, empty });
152	  };
153	})();
154	
````

### User / tool · 2026-11-03T04:34:21.518Z

**tool result**
````
30	  function find(c, id) { return [].concat(c.entries || [], c.undated_entries || [], c.flags || [], c.tray || []).find((i) => i.id === id) || null; }
31	  const groupOf = (c, it) => ((c.tray || []).includes(it) ? "tray" : (c.undated_entries || []).includes(it) ? "undated" : (c.flags || []).includes(it) ? "flag" : "entry");
32	
33	  /* ---------- words ---------- */
34	  const FLAG_HEAD = [
35	    [(f) => f.type === "gap", (f) => (f.computed && f.computed.conditional ? "A possible break in treatment" : "A break in treatment")],
36	    [(f) => f.type === "conflict" && /^accident_date/.test(f.category || ""), () => "The records disagree about the accident date"],
37	    [(f) => f.type === "conflict" && f.category === "treatment_plan_vs_actual", () => "The plan and what happened differ"],
38	    [(f) => f.type === "conflict" && f.category === "provider_name_variant", () => "The provider's name is written differently"],
39	    [(f) => f.type === "conflict", () => "The records disagree"],
40	    [(f) => f.type === "pre_existing" && f.category === "degenerative_language", () => "Wording about wear and tear"],
41	    [(f) => f.type === "pre_existing", () => "An earlier health problem is mentioned"],
42	    [(f) => f.type === "causation" && f.category === "patient_report", () => "The patient, not a doctor, says what caused it"],
43	    [(f) => f.type === "causation" && f.category === "speculative_language", () => "Hedged wording (“may”, “possible”)"],
44	    [(f) => f.type === "causation" && f.category === "missed_care", () => "Missed or ended treatment"],
45	    [(f) => f.type === "causation" && f.category === "new_onset", () => "Wording about a new problem"],
46	    [(f) => f.type === "causation" && f.category === "accident_date_provenance", () => "Where the accident date comes from"],
47	    [(f) => f.type === "causation" && f.category === "credibility_language", () => "Wording about the patient's effort or credibility"],
48	    [(f) => f.type === "causation", () => "Wording the other side could use"],
49	    [(f) => f.type === "record_warning" && f.category === "injection_suspected", () => "This record contains text that looks like instructions to a computer"],
50	    [(f) => f.type === "record_warning" && f.category === "date_ambiguous", () => "This record's date is unclear"],
51	    [(f) => f.type === "record_warning" && f.category === "analysis_incomplete", () => "We couldn't finish comparing these records"],
52	    [(f) => f.type === "record_warning", () => "Something to check in this record"],
53	  ];
54	  const flagHeading = (f) => (FLAG_HEAD.find(([t]) => t(f)) || [null, () => "A warning for the attorney"])[1](f);
55	  const CODE_CHECK = new Set(["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_NUMBER_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CHARGE_TEXT_IN_ENTRY", "GROUNDING_EXCERPT_NOT_VERBATIM"]);
56	  const isCodeFail = (it) => (it.reasons || []).some((r) => CODE_CHECK.has(r) || /^EXCERPT_/.test(r));
57	  const quoteFail = (it) => (it.reasons || []).some((r) => /^EXCERPT_/.test(r) || r === "GROUNDING_EXCERPT_NOT_VERBATIM");
58	  const recLabel = (r) => `Record ${r.seq} · ${r.source_label || "Record"} · ${r.date_iso ? R.longDate(r.date_iso) : r.date_raw ? r.date_raw : "no date"}`;
59	  const lineHead = (it, rec) => [it.date ? R.longDate(it.date) : (rec && rec.date_raw) || "No date", it.provider || (rec && rec.source_label)].filter(Boolean).join(" · ");
60	
61	  /* ---------- source card ---------- */
62	  function uncoveredNote(recs, marks) {
63	    const rows = [];
64	    recs.forEach((r) => (r.uncovered || []).forEach((u) => { if (!marks.some(([a, b]) => u.start >= a && u.end <= b)) rows.push(u.text); }));
65	    if (!rows.length) return [];
66	    return [h("div", { class: "also", "data-testid": "uncovered" }, h("b", {}, "Also in this record, outside the highlighted words:"), ...rows.map((t) => h("div", {}, h("q", {}, t))))];
67	  }
68	  /* the part of a record to show when several records share the card: the highlighted words with about 80 characters of the record on each side, cut at a space or line end */
69	  function windowOf(rec, marks) {
70	    const t = rec.text || "", a = Math.min(...marks.map((m) => m[0])) - rec.char_start, b = Math.max(...marks.map((m) => m[1])) - rec.char_start;
71	    let from = Math.max(t.lastIndexOf("\n", Math.max(0, a - 1)) + 1, a - 80), to = b + 80;
72	    if (from > 0 && t[from - 1] !== "\n") { const sp = t.indexOf(" ", from); if (sp >= 0 && sp < a) from = sp + 1; }
73	    const nl = t.indexOf("\n", b); if (nl >= 0 && nl < to) to = nl;
74	    if (to < t.length && t[to] !== "\n") { const sp = t.lastIndexOf(" ", to); if (sp > b) to = sp; }
75	    to = Math.min(t.length, to);
76	    return from <= 0 && to >= t.length ? null : [Math.max(0, from), to];
77	  }
78	  function sourceFor(S, recs, marks, opt) {
79	    opt = opt || {};
80	    S.whole = S.whole || new Set();
81	    return () => {
82	      const many = recs.length > 1, nodes = [];
83	      if (opt.hint) nodes.push(h("p", { class: "muted src-hint" }, opt.hint));
84	      recs.forEach((r) => {
85	        const mine = marks.filter(([a]) => a >= r.char_start && a < r.char_end), win = many && mine.length && !opt.sentencesOf && !S.whole.has(r.id) ? windowOf(r, mine) : null;
86	        nodes.push(...R.recBlock(r, { marks: mine, win, head: many ? recLabel(r) : null, sentences: opt.sentencesOf === r.id ? r.sentences : null, picked: opt.picked, onPick: opt.onPick }));
87	        if (many && mine.length && !opt.sentencesOf && (win || S.whole.has(r.id))) {          // several records: each shows its highlighted sentence, so every highlight is on screen without scrolling
88	          nodes.push(h("button", { type: "button", class: "btn quiet src-toggle", "data-testid": "btn-whole-record", "aria-expanded": win ? "false" : "true",
89	            onclick: () => { win ? S.whole.add(r.id) : S.whole.delete(r.id); S.renderSource(); } }, win ? `Show the whole of record ${r.seq}` : `Show only the highlighted part of record ${r.seq}`));
90	        }
91	      });
92	      if (!opt.sentencesOf && opt.uncovered !== false) nodes.push(...uncoveredNote(recs, marks));
93	      return nodes;
94	    };
95	  }
96	  function headFor(recs) { const n = recs.map((r) => r.seq); return recs.length === 1 ? recLabel(recs[0]) : "Records " + n.slice(0, -1).join(", ") + " and " + n[n.length - 1]; }
97	
98	  /* ---------- sentence picking (fix the wording, write it yourself): whole sentences that follow each other ---------- */
99	  function pickedRange(rec, picked) {
100	    const sents = (rec.sentences || []).filter((s) => picked.has(s.start));
101	    if (!sents.length) return { error: "Pick at least one sentence." };
102	    const all = rec.sentences, idx = sents.map((s) => all.findIndex((x) => x.start === s.start)).sort((a, b) => a - b);
103	    if (idx.some((v, i) => i && v !== idx[i - 1] + 1)) return { error: "Pick sentences that follow each other." };
104	    const a = all[idx[0]], b = all[idx[idx.length - 1]];
105	    return { excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
106	  }
107	  function togglePick(S, sent) { const p = S.ui.picked || (S.ui.picked = new Set()); p.has(sent.start) ? p.delete(sent.start) : p.add(sent.start); S.renderSource(); }
108	  const warningsFoot = (S) => (S.ui.warnings || []).map((w) => h("p", { class: "foot-warn", "data-testid": "save-warning" }, R.plain(w.message || String(w))));
109	
110	  /* ---------- the words of a line that are not in the highlighted words (code, no AI): a deterministic word diff so she sees what to check (paralegal review T-181 major) ---------- */
111	  const WORD = /[\p{L}\p{N}]+(?:['’][\p{L}]+)?/gu;
112	  const SKIP = new Set("a an the of to and or is are was were be been for with by at in on as it its that this".split(" "));
113	  const ABBR = { pt: "patient", dx: "diagnosis", rx: "prescription", hx: "history", tx: "treatment", sx: "symptom" };      // chart shorthand reads as the word it stands for (paralegal r2 nit: "Pt" in the quote, "Patient" in the line)
114	  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return w === "PT" ? x : ABBR[x] || x; };      // "PT" in capitals is physical therapy, not a patient: it stays a word of its own, so a "Patient" in the line is still underlined
115	  function outsideParts(summary, quote) {
116	    const inQuote = new Set((String(quote || "").match(WORD) || []).map(stem)), parts = [];
117	    let last = 0, any = false;
118	    for (const m of String(summary || "").matchAll(WORD)) {
119	      const w = m[0], out = !SKIP.has(w.toLowerCase()) && !inQuote.has(stem(w));
120	      if (m.index > last) parts.push(summary.slice(last, m.index));
121	      parts.push(out ? h("u", { class: "out", "data-testid": "outside-word" }, w) : w); if (out) any = true;
122	      last = m.index + w.length;
123	    }
124	    if (last < summary.length) parts.push(summary.slice(last));
125	    return any ? parts : null;
126	  }
127	
128	  /* ---------- presenting an item ---------- */
129	  function present(S, item, q) {
130	    const c = S.c, g = groupOf(c, item);
131	    if (g === "tray") return item.kind === "flag" ? trayFlag(S, item) : trayEntry(S, item);
132	    if (g === "flag") return warning(S, item);
133	    if (g === "undated") return undated(S, item);
134	    return line(S, item);
135	  }
136	
137	  /* 5.2 / 5.3 / 5.4 a line */
138	  function line(S, item) {
139	    const ui = S.ui, recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), main = S.recOf(item.excerpt_start) || recs[0];
140	    const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
141	    if (ui.mode === "fix") return fixLine(S, item, main, recs);
142	    const srcRecs = recs.length ? recs : main ? [main] : [];
143	    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null), refusal = isCodeFail(item), edited = !!item.edit_to_check;
144	    const need = !refusal && (!!disp || edited), decided = (item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited") && !edited;
145	    const foot = [];
146	    let cls = "plain";
147	    if (refusal) { cls = "attn"; foot.push(h("strong", { "data-testid": "refusal" }, R.plain(item.why))); }
148	    else if (need) {
149	      cls = "attn";
150	      foot.push(h("strong", { "data-testid": "compare-reason" }, edited ? "You changed the wording. Read it against the highlighted words once more." : R.disputeText(disp, item)));
151	      if (!edited) foot.push(" Read it against the highlighted words before you say yes.");
152	      foot.push(R.check(S, "compare", "I read this line against the highlighted words myself.", { focus: true }));
153	    } else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "left out of the letter." : "kept in the letter.", " You can change it."); }
154	    else if (S.part2.has(item.id)) foot.push(h("span", { class: "label-cap" }, "Part 2 of 2"), h("br"), "The date is set. Now check the line itself.");
155	    else if (item.state === "needs_review") { cls = "attn"; foot.push(R.plain(item.why)); }
156	    else foot.push(h("span", { class: "label-cap" }, "How it was checked"), h("br"), R.plain(item.why));
157	    foot.push(...warningsFoot(S));
158	    return {
159	      tag: R.tagFor(item), sub: lineHead(item, main),
160	      body: [h("p", { class: "line-text", "data-testid": "line-text" }, ...(((need && outsideParts(item.summary, item.excerpt)) || [item.summary || ""]))),
161	        need && outsideParts(item.summary, item.excerpt) ? h("p", { class: "muted out-note", "data-testid": "outside-note" }, "Underlined words are not in the highlighted words.") : null],
162	      foot: { cls, nodes: foot },
163	      question: "Does this line say the same thing as the highlighted words?",
164	      yes: { label: "Yes, this matches", why: refusal ? R.plain(item.why) : "", disabled: () => refusal || (need && !R.ticked(S, "compare")), run: () => S.decide(item, "accept", need && R.ticked(S, "compare") ? { compared: true } : undefined) },
165	      no: { label: "No, leave it out", run: () => S.decide(item, "dismiss") },
166	      third: { label: quoteFail(item) ? "Change the words" : "Fix the wording", hint: refusal, run: () => { ui.mode = "fix"; ui.draft = null; ui.picked = null; S.err = null; S.say(null, null); S.render(); } },
167	      src: { head: headFor(srcRecs), nodes: sourceFor(S, srcRecs, marks) },
168	    };
169	  }
170	
171	  function fixLine(S, item, rec, recs) {
172	    const ui = S.ui;
173	    if (!ui.picked) ui.picked = new Set((rec.sentences || []).filter((s) => item.excerpt_start != null && s.start < item.excerpt_end && s.end > item.excerpt_start).map((s) => s.start));
174	    if (ui.draft == null) ui.draft = item.summary || "";
175	    const ta = h("textarea", { class: "edit", "data-testid": "edit-summary", "aria-label": "Your wording for this line", "data-autofocus": "" });
176	    ta.value = ui.draft; ta.addEventListener("input", () => { ui.draft = ta.value; });
177	    const save = () => {
178	      const r = pickedRange(rec, ui.picked);
179	      if (r.error) { S.err = { text: r.error }; S.render(true); return; }
180	      const summary = (ui.draft || "").trim();
181	      if (!summary) { S.err = { text: "Write the line first." }; S.render(true); return; }
182	      const qChanged = r.excerpt !== item.excerpt, sChanged = summary !== (item.summary || "").trim();
183	      if (!qChanged && !sChanged) { S.err = { text: "Nothing has changed yet." }; S.render(true); return; }
184	      return S.act(async () => {
185	        S.lastEdit = { excerpt: r.excerpt, summary, before: item.summary };       // a refusal that names dropped words reads these (review.js droppedText)
186	        const edits = {};                                   // one call: the server checks the new wording against the new quote together (two calls would test the old wording against the new quote)
187	        if (qChanged) edits.excerpt = r.excerpt;
188	        if (sChanged) edits.summary = summary;
189	        const resp = await S.post(item, "edit", { edits });
190	        S.c = await S.ctx.refresh(); ui.mode = "view"; ui.picked = null; ui.draft = null; ui.warnings = resp.warnings || [];
191	        S.say("Saved: your wording is in. Read it once more against the highlighted words.", null);
192	        S.render(false);
193	      });
194	    };
195	    return {
196	      tag: { cls: "you", text: "Your wording" }, sub: lineHead(item, rec), focus: "field",
197	      body: [h("p", { class: "muted fix-hint" }, "Change the line so it says only what the highlighted words say. Numbers, left or right, and words like “no” or “possible” must match."), ta],
198	      foot: { cls: "plain", nodes: [R.plain(item.why)] },
199	      question: "Change the line, then save it.",
200	      yes: { label: "Save my wording", run: save }, no: { label: "Cancel", run: () => { ui.mode = "view"; ui.picked = null; ui.draft = null; S.err = null; S.render(); } },
201	      third: null,
202	      src: { head: recLabel(rec), nodes: sourceFor(S, [rec], [], { hint: "To change which words are highlighted, tap whole sentences below.", sentencesOf: rec.id, picked: ui.picked, onPick: (s) => togglePick(S, s), uncovered: false }) },
203	    };
204	  }
205	
206	  /* 5.6 a date to pick */
207	  function undated(S, item) {
208	    const rec = S.record((item.record_ids || [])[0]), dtc = (S.c.dates_to_confirm || []).find((d) => d.record_id === (rec && rec.id));
209	    const cands = (dtc && dtc.candidates) || [];
210	    const raw = (dtc && dtc.raw) || (rec && rec.date_raw) || "";
211	    const at = rec && raw ? rec.text.indexOf("Date: " + raw) : -1, marks = at >= 0 ? [[rec.char_start + at, rec.char_start + at + 6 + raw.length]] : [];
212	    const src = { head: rec ? recLabel(rec) : "", nodes: sourceFor(S, rec ? [rec] : [], marks, { uncovered: false }) };
213	    if (!cands.length) {
214	      return {
215	        tag: { cls: "warn", text: "No date found" }, sub: item.provider || (rec && rec.source_label), src,
216	        body: [h("p", { class: "warn-title" }, "We couldn't find a date"), h("p", { class: "explain" }, "We couldn't find a date in this record, so it can't go on the timeline."),
217	          h("p", { class: "explain muted gap-top" }, "The line waiting for a date: “", item.summary || "", "”")],
218	        foot: { cls: "attn", nodes: ["Without a date the line cannot be placed between the other records. Leaving it out keeps it out of the timeline."] },
219	        question: "Read the record. Leave this line out?",
220	        yes: { label: "OK, leave it out", run: () => S.decide(item, "dismiss") }, no: { label: "Decide later", run: () => S.skip() }, third: null, later: false,
221	      };
222	    }
223	    const sug = dtc.suggestion && dtc.suggestion.iso, first = (/^(\d{1,2})[/.\-]/.exec(raw) || [])[1];
224	    const reading = (iso) => (first && +first === +iso.slice(5, 7) ? "month first" : first && +first === +iso.slice(8, 10) ? "day first" : "");
225	    const pick = (iso) => S.act(async () => {
226	      const resp = await G.api.confirmDate(S.token, rec.id, iso);
227	      S.c = await S.ctx.refresh(); S.part2.add(item.id); S.ui = {};
228	      const sentences = (resp.gap_changes || []).map((x) => x.sentence).filter(Boolean);
229	      S.say(sentences.length ? sentences.join(" ") : `Saved: record ${rec.seq} is dated ${R.longDate(iso)}.`, null);
230	      S.render(false);
231	    });
232	    const ans = (iso) => ({ label: R.longDate(iso), sub: [reading(iso), iso === sug ? "Suggested" : ""].filter(Boolean).join(" · "), plain: true, run: () => pick(iso) });
233	    const a = ans(cands[0]), b = ans(cands[1] || cands[0]);
234	    return {
235	      tag: { cls: "warn", text: "Pick the date" }, sub: item.provider || (rec && rec.source_label), src,
236	      body: [h("p", { class: "warn-title" }, "Which date is right?"), h("p", { class: "explain" }, "The record says ", h("b", {}, raw), ". That could be two different dates."),
237	        h("p", { class: "explain muted gap-top" }, "The line waiting for this date: “", item.summary || "", "”")],
238	      foot: { cls: "plain", nodes: sug ? [h("span", { class: "label-cap" }, "Suggested: " + R.longDate(sug)), h("br"), dtc.suggestion.reason] : ["Pick the reading that matches how the other dates in these records are written."] },
239	      question: "Which date is right for this record?", yes: a, no: cands.length > 1 ? b : null, third: null, later: { run: () => S.skip() },
240	    };
241	  }
242	
243	  /* 5.7 a warning for the attorney */
244	  function warning(S, item) {
245	    const ui = S.ui;
246	    const evid = item.evidence || [], ids = [...new Set(evid.map((e) => e.record_id))];
247	    const recs = (ids.length ? ids : item.record_ids || []).map((id) => S.record(id)).filter(Boolean).sort((a, b) => a.seq - b.seq);
248	    const marks = evid.map((e) => [e.start, e.end]);
249	    const src = { head: recs.length ? headFor(recs) : "", nodes: sourceFor(S, recs, marks) };
250	    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null), edited = !!item.edit_to_check;
251	    const noteMode = ui.mode === "note";
252	    const decided = (item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited") && !edited;
253	    const body = [h("p", { class: "warn-title", "data-testid": "warning-heading" }, flagHeading(item)),
254	      item.title && !(item.explanation || "").startsWith(item.title) ? h("p", { class: "explain", "data-testid": "warning-title" }, h("b", {}, item.title)) : null,
255	      h("p", { class: "explain", "data-testid": "warning-text" }, item.explanation || ""),
256	      item.gap_change && item.gap_change.sentence ? h("p", { class: "explain gap-top", "data-testid": "gap-change" }, item.gap_change.sentence) : null,
257	      item.reviewer_note && !noteMode ? h("p", { class: "explain muted gap-top" }, h("b", {}, "Your note: "), item.reviewer_note) : null];
258	    const tags = { tag: { cls: "warn", text: "Warning for the attorney" }, tag2: R.tagFor(item), src };
259	    if (noteMode) {
260	      const ta = h("textarea", { class: "edit", "data-testid": "edit-note", "aria-label": "Your note for the attorney", "data-autofocus": "" });
261	      ta.value = ui.draft != null ? ui.draft : item.reviewer_note || ""; ta.addEventListener("input", () => { ui.draft = ta.value; });
262	      return { ...tags, focus: "field", body: [h("p", { class: "warn-title" }, "Add a note for the attorney"), ta],
263	        foot: { cls: "plain", nodes: ["Your note goes in the notes for the attorney, next to this warning. It never goes in the letter."] },
264	        question: "Write your note, then save it.",
265	        yes: { label: "Save note", run: () => { const note = (ui.draft != null ? ui.draft : "").trim(); if (!note) { S.err = { text: "Write the note first." }; S.render(true); return undefined; } return S.decide(item, "edit", { edits: { note } }); } },
266	        no: { label: "Cancel", run: () => { ui.mode = "view"; ui.draft = null; S.err = null; S.render(); } }, third: null };
267	    }
268	    const foot = [];
269	    let cls = "plain";
270	    if (disp) {
271	      cls = "attn"; foot.push(h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you say yes.", R.check(S, "compare", "I read this warning against the highlighted words myself.", { focus: true }));
272	    } else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "not needed. It is listed as ruled out in the notes." : "the attorney will be told.", " You can change it."); }
273	    else foot.push("Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.");
274	    return { ...tags, sub: "", body, foot: { cls, nodes: foot },
275	      question: "Should the attorney be told about this?",
276	      yes: { label: "Yes, tell the attorney", disabled: () => !!disp && !R.ticked(S, "compare"), run: () => S.decide(item, "accept", disp && R.ticked(S, "compare") ? { compared: true } : undefined) },
277	      no: { label: "No, not needed", run: () => S.decide(item, "dismiss") },
278	      third: { label: "Add a note", run: () => { ui.mode = "note"; ui.draft = null; S.err = null; S.say(null, null); S.render(); } } };
279	  }
280	
281	  /* 5.5 could not check */
282	  function trayEntry(S, item) {
283	    const ui = S.ui, rec = S.record((item.record_ids || [])[0]) || S.record("r" + ((/^e(\d+)/.exec(item.id) || [])[1]));
284	    if (!rec) return { body: [h("p", {}, R.plain(item.why))], foot: { cls: "plain", nodes: [] }, question: "", yes: { label: "Skip it", run: () => S.decide(item, "dismiss") }, no: null, third: null };
285	    if (ui.mode === "write") {
286	      if (!ui.picked) ui.picked = new Set();
287	      if (ui.draft == null) ui.draft = "";
288	      const ta = h("textarea", { class: "edit", "data-testid": "edit-line", "aria-label": "Your line for the timeline", "data-autofocus": "" });
289	      ta.value = ui.draft; ta.addEventListener("input", () => { ui.draft = ta.value; });
290	      const save = () => {
291	        const r = pickedRange(rec, ui.picked), summary = (ui.draft || "").trim();
292	        if (r.error || !summary) { S.err = { text: r.error || "Write the line first." }; S.render(true); return undefined; }
293	        return S.act(async () => {
294	          const resp = await G.api.addEntry(S.token, rec.id, { summary, excerpt: r.excerpt });
295	          S.c = await S.ctx.refresh();
296	          const nid = (resp.item && resp.item.id) || (resp.entry && resp.entry.id);
297	          S.queue[S.idx] = { id: nid, optional: false }; S.ui = {}; S.screen = null;
298	          history.replaceState(history.state, "", G.url.timeline(S.token, nid));
299	          S.say("Saved: your line is in. Check it against the highlighted words once more.", null);
300	          S.render(false);
301	        });
302	      };
303	      return { tag: { cls: "you", text: "Written by you" }, sub: recLabel(rec), focus: "field",
304	        body: [h("label", { class: "sr", for: "mine" }, "Your line for the timeline"), ta],
305	        foot: { cls: "plain", nodes: ["Use only what the chosen sentences say. Numbers, left or right, and words like “no” or “possible” must match."] },
306	        question: "Write the line for the timeline, then save it.",
307	        yes: { label: "Save my line", run: save }, no: { label: "Cancel", run: () => { ui.mode = "view"; ui.picked = null; ui.draft = null; S.err = null; S.render(); } }, third: null,
308	        src: { head: recLabel(rec), nodes: sourceFor(S, [rec], [], { hint: "Tap the sentences your line is based on. They become the highlighted words.", sentencesOf: rec.id, picked: ui.picked, onPick: (s) => togglePick(S, s), uncovered: false }) } };
309	    }
310	    const tried = item.attempt && item.attempt.summary;
311	    return { tag: { cls: "warn", text: "We couldn't check this one" }, sub: recLabel(rec).replace(/^Record \d+ · /, ""),
312	      body: [h("p", { class: "explain", "data-testid": "tray-why" }, R.plain(item.why)), tried ? h("p", { class: "explain muted gap-top" }, "What was suggested (not used): “", tried, "”") : null],
313	      foot: { cls: "attn", nodes: ["Nothing from this suggestion goes in the letter unless you write the line yourself. Skipping it leaves this record out of the timeline."] },
314	      question: "Read the record. Do you want to write this line yourself?",
315	      yes: { label: "Write it myself", run: () => { ui.mode = "write"; ui.picked = null; ui.draft = null; S.err = null; S.render(); } },
316	      no: { label: "Skip it", run: () => S.decide(item, "dismiss") }, third: null,
317	      src: { head: recLabel(rec), nodes: sourceFor(S, [rec], [], { uncovered: false }) } };
318	  }
319	  function trayFlag(S, item) {
320	    const recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), a = item.attempt || {};
321	    return { tag: { cls: "warn", text: "We couldn't confirm this warning" }, sub: recs.length ? recLabel(recs[0]).replace(/^Record \d+ · /, "") : "",
322	      body: [h("p", { class: "explain", "data-testid": "tray-why" }, R.plain(item.why)), a.summary ? h("p", { class: "explain muted gap-top" }, h("b", {}, "The suggested warning: "), a.summary) : null,
323	        a.excerpt ? h("p", { class: "explain muted" }, "Its words in the record: “", a.excerpt, "”") : null],
324	      foot: { cls: "attn", nodes: ["This suggested warning is not in the notes for the attorney."] },
325	      question: "This warning can't go in the notes. Read it; if it matters, tell the attorney yourself.",
326	      yes: { label: "OK, leave it out", run: () => S.decide(item, "dismiss") }, no: { label: "Decide later", run: () => S.skip() }, third: null, later: false,
327	      src: { head: recs.length ? headFor(recs) : "", nodes: sourceFor(S, recs, [], { uncovered: false }) } };
328	  }
329	
330	  /* what the Saved line says */
331	  function statusFor(S, item, resp, action) {
332	    const q = S.queue.find((x) => x.id === (item && item.id)), flag = !!(item && (item.type || item.kind === "flag"));
333	    if (action === "dismiss") return q && q.optional ? "skipped. It stays out of the letter" : flag ? "marked not needed" : "left out of the letter";
334	    if (action === "edit") return "will go in the notes for the attorney, with your note";
335	    return flag ? "will go in the notes for the attorney" : "kept in the letter";
336	  }
337	
338	  /* ---------- 5.8 done ---------- */
339	  function done(S) {
340	    const c = S.c, items = S.counted().map((q) => ({ q, it: S.item(q.id) })), left = items.filter(({ it }) => G.steps.undecided(it));
341	    const kept = items.filter(({ it }) => groupOf(c, it) !== "flag" && it.review_status !== "dismissed" && !G.steps.undecided(it)).length;
342	    const out = items.filter(({ it }) => groupOf(c, it) !== "flag" && it.review_status === "dismissed").length;
343	    const told = items.filter(({ it }) => groupOf(c, it) === "flag" && (it.review_status === "accepted" || it.review_status === "edited") && !it.edit_to_check).length;
344	    const notNeeded = items.filter(({ it }) => groupOf(c, it) === "flag" && it.review_status === "dismissed").length;
345	    const nextHref = (c.amounts || []).some(G.steps.live) ? G.url.bills(S.token) : G.url.letter(S.token);
346	    const nextLabel = (c.amounts || []).some(G.steps.live) ? "Go to step 3: Check the bills" : "Go to step 4: Get your letter";
347	    const first = left[0];
348	    const hero = left.length
349	      ? h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "!"), h("div", {}, h("h2", { "data-testid": "done-heading" }, `${left.length} item${left.length === 1 ? " still needs" : "s still need"} a decision.`),
350	        h("p", {}, "Items you don't decide stay out of the letter.")))
351	      : h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "You checked every item on the timeline."),
352	        h("p", { "data-testid": "done-counts" }, `${kept} kept in the letter · ${out} left out · ${told} warning${told === 1 ? "" : "s"} for the attorney · ${notNeeded} not needed`)));
353	    const CHIP = { accepted: ["Kept", "ok"], edited: ["Kept", "ok"], dismissed: ["Left out", "never"] };
354	    const rows = items.map(({ q, it }, i) => {
355	      const fl = groupOf(c, it) === "flag", und = G.steps.undecided(it);
356	      const chip = und ? ["Not decided", "warn"] : fl ? (it.review_status === "dismissed" ? ["Not needed", "never"] : ["Tell the attorney", "warn"]) : CHIP[it.review_status] || ["Not decided", "warn"];
357	      const rec = S.record((citedIds(it)[0]));
358	      const label = fl ? flagHeading(it) : it.provider || (rec && rec.source_label) || "Line";
359	      return R.answerRow(i + 1, R.shortDate(it.date || (rec && rec.date_iso)), label, chip[0], chip[1], G.url.timeline(S.token, it.id));
360	    });
361	    const trayDone = S.queue.filter((q) => q.optional).map((q) => S.item(q.id)).filter(Boolean);
362	    const filtered = c.tray_filtered && c.tray_filtered.count > 0 ? c.tray_filtered : null, checks = c.checks;
363	    const labels = (checks && checks.labels) || {};
364	    return R.doneFrame(2, "Check the timeline",
365	      h("div", { class: "panel" }, hero, h("div", { class: "row-actions" },
366	        first ? h("a", { class: "btn primary lg", href: G.url.timeline(S.token, first.q.id), "data-testid": "btn-first-undecided" }, "Go to the first one") : null,
367	        h("a", { class: "btn lg " + (first ? "" : "primary"), href: nextHref, "data-testid": "btn-next-step" }, nextLabel))),
368	      h("div", { class: "panel" }, h("h2", {}, "Your answers"), h("p", { class: "muted" }, "Every item in the order you saw it. Change any answer here."), h("ol", { class: "answers", "data-testid": "answers-list" }, rows),
369	        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. " + (G.provenance().kind === "prepared" ? "" : "“AI draft” means an AI wrote it. ") + "“Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
370	      trayDone.length ? h("div", { class: "panel", "data-testid": "tray-done" }, h("h2", {}, "Items we couldn't check"), h("p", { class: "muted" }, "These are optional. They stay out of the letter unless you wrote the line yourself."),
371	        h("ul", { class: "plain-list" }, trayDone.map((t) => h("li", {}, h("a", { href: G.url.timeline(S.token, t.id) }, t.kind === "flag" ? "A suggested warning we couldn't confirm" : "A record with no line"), t.review_status === "dismissed" ? " (skipped)" : "")))) : null,
372	      filtered ? h("div", { class: "panel", "data-testid": "filtered-rules" }, h("h2", {}, "Suggestions a rule ruled out (nothing to do)"),
373	        ...(filtered.rules || []).map((r) => h("div", { class: "rule-out" }, h("p", {}, h("b", {}, r.label || r.rule), " ", r.explanation || ""), ...(r.items || []).map((i) => h("p", { class: "muted" }, "“", (i.attempt && i.attempt.excerpt) || "", "”"))))) : null,
374	      checks ? h("div", { class: "panel", "data-testid": "checks-panel" }, h("h2", {}, "What we compared between records"),
375	        h("p", {}, h("b", {}, "We checked for: "), (checks.conflict_types || []).map((t) => labels[t] || t).join("; ") || "nothing yet", "."),
376	        (checks.not_checked || []).length ? h("p", { class: "gap-top" }, h("b", {}, "Not checked: "), checks.not_checked.map((n) => n.label).join("; "), ".") : null) : null);
377	  }
378	  function empty(S) {
379	    return R.doneFrame(2, "Check the timeline", h("div", { class: "panel" }, h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "–"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "There are no timeline lines in this case."), h("p", {}, "Nothing here needs checking."))),
380	      h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: (S.c.amounts || []).some(G.steps.live) ? G.url.bills(S.token) : G.url.letter(S.token), "data-testid": "btn-next-step" }, (S.c.amounts || []).some(G.steps.live) ? "Go to step 3: Check the bills" : "Go to step 4: Get your letter"))));
381	  }
382	
383	  G.pages.timeline = function (ctx) {
384	    return R.run(ctx, { step: 2, title: "Check the timeline", unit: "Item", chip: false, buildQueue, find, present, statusFor, done, empty });
385	  };
386	  G.step2 = { buildQueue, find, flagHeading, outsideParts };
387	})();
388	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:25.184Z

**tool call — Bash**
````
{
 "command": "sed -n 574p memory/contracts/api.md | cut -c1-2500; echo; sed -n 160,200p memory/contracts/api.md | cut -c1-700"
}
````

### User / tool · 2026-11-03T04:34:25.291Z

**tool result**
````
Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`. **T-200 + D-071 + D-073 (T-202 r5, the conservative fallback): a charge line takes its date of service from exactly TWO sources.** The line before a charge's quote prints the service date the line itself states (`<provider>, <source label>, March 27, 2026: $250.00`), never the record's date for a bill (the statement's). A service period prints as a range (`June 9\u201312, 2026`, `June 28\u2013July 2, 2026`, its own stated year). Code (`app/backend/service_date.py`) reads a date from ONLY: **(1)** the date cell of the charge's own row in a bill table whose column header names the date of service (DOS, date of service, service date, visit date, from/to service, 24A; the CMS-1500 24A `From` and `To` cells together are one period, the same day twice is that day), or, for a coded line (CPT, HCPCS, revenue code) of a UB-04, the span its `statement covers period FROM ... THROUGH ...` states; **(2)** the record's own date, only when the record is identified as an encounter record by a **document-type word** in its source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, ambulance run report, operative report, evaluation, consult, new patient, follow-up ...: the declared table `app/backend/encounter_types.json`, read by `s

      "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
      "excerpt_start": 396, "excerpt_end": 532,
      "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
      "review_status": "pending", "edited": null, "duplicate_note": null,
      "ladder": {
        "item_id": "e2", "backend": "fixture",
        "generator": {"model": "claude-sonnet-5-5", "prompt_version": "extract_v1", "call_id": "c12",
                      "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T00:50:00Z"},
                      "output": {"summary": "Diagnosed with cervical strain ...", "excerpt": "Dx: cervical strain; ..."}},
        "code_checks": {"excerpt_verbatim": true, "excerpt_whole_sentence": true, "qualifier_carried": true,
                        "date_provider_from_header": true,
                        "summary_tokens_not_in_excerpt": [], "highlight_found": true},
        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": "c21", "verdict": "supported"},
        "state": "verified",
        "human": {"action": null, "edited_text": null, "at": null} }
    } ],
  "amounts": [
    { "id": "a1", "record_ids": ["r2"], "entry_id": "e2", "text": "$6,240", "value_cents": 624000, "kind": "charge",
      "excerpt": "ER charges: $6,240.", "excerpt_start": 533, "excerpt_end": 552,
      "state": "verified", "reasons": [], "why": "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
      "review_status": "pending", "edited": null, "duplicate_note": null,
      "ladder": {
        "item_id": "a1", "backend": "fixture", "generator": null,
        "code_checks": {"amount_in_text": true, "classified_by": "rule:charge_label", "injection_tag": false, "highlight_found": true},
        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c31", "verdict": "agrees"},
        "state": "verified", "human": {"action": null, "edited_text": null, "at": null} } },
    { "id": "a3", "record_ids": ["r4"], "entry_id": "e4", "text": "$185", "value_cents": 18500, "kind": "rate",
      "excerpt": "Charge per visit $185.", "excerpt_start": 929, "excerpt_end": 951,
      "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
      "why": "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled.",
      "review_status": "pending", "edited": null, "duplicate_note": null, "flag": null, "confirm_required": false, "accept_effect": "acknowledge", "judge_required_for_export": false,
      "not_counted_reason": "This figure is a rate, not a charge, so it is not added to the total.", "countable": false, "count_confirm": null, "service_date": null,
      "ladder": {"item_id": "a3", "backend": "fixture", "generator": null,
        "code_checks": {"amount_in_text": true, "classified_by": "rule:per_unit", "injection_tag": false, "highlight_found": true},
        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c33", "verdict": "agrees"},
        "state": "needs_review", "human": {"action": null, "edited_text": null, "at": null}} } ],
  "totals": {
    "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"},
    "pending": {"cents": 839000, "count": 2, "label": "Pending review"},
    "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"},
    "not_totaled": [{"id": "a3", "kind": "rate", "text": "$185"}],
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:25.443Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/review.js"
}
````

### User / tool · 2026-11-03T04:34:25.582Z

**tool result**
````
1	/* Shared one-item review engine for the two review pages (step 2 timeline, step 3 bills). OWNER: the Step 2 + Step 3 builder (frontend-B). Spec 2.5-2.7, 5, 6; D-066, D-065, D-067, T-178.
2	   A step module calls G.review.run(ctx, cfg) and describes each item as a SCREEN (see "screen" below); this file owns the fixed frame (title row, two cards, action bar), the queue, every
3	   write (version + expected_status on each review POST, 409 -> reload, COMPARE_REQUIRED -> compare box), Undo, keyboard (A yes, D no, E third, arrows move) and focus.
4	   Nothing here touches the shell. No innerHTML anywhere: record text, quotes and titles go in with textContent. No style attributes (CSSOM only, for the progress bar).
5	   cfg = { step, title, unit ("Item"|"Amount"), chip (bool), buildQueue(c) -> [{id, optional?}], find(c, id), present(S, item, q) -> screen, empty(S) -> node, done(S) -> node,
6	           statusFor(S, item, q, resp, action) -> "kept in the letter", onResponse?(S, resp) }
7	   screen = { tag?: {cls, text, title}, tag2?, sub, body: [Node], foot: {cls, nodes}, question, yes: {label, sub?, key?, disabled?: fn, run}, no: {...}|null, third: {label, run, hint?}|null,
8	              later: {label?, run}|false, src: {head, nodes: () => [Node]}, counter?: string, focus?: "yes"|"field" } */
9	(function () {
10	  const G = window.G, { h } = G;
11	  const R = (G.review = G.review || {});
12	
13	  /* ---------- words: server sentences get the plain vocabulary of spec section 10 (never the facts); text inside “curly quotes” is record text and is left alone ---------- */
14	  const WHY_OK = /^Quote found word for word, every number in the summary is in the quote, and the second check agreed\.?$/;
15	  R.plain = function (text) {
16	    if (text == null) return "";
17	    const s = String(text);
18	    if (WHY_OK.test(s.trim())) return "The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.";
19	    return s.split(/(“[^”]*”)/).map((part, i) => (i % 2 ? part : part
20	      .replace(/The quote carries (.+?) that the summary leaves out\. Put it back in the summary\./g, (m, what) => `Your line leaves out ${what.replace(/\bthe quote gives\b/, "the highlighted words give")} that the highlighted words have. Put it back in the line.`)
21	      .replace(/ \(the internal notes say why\), so none of them is in Billed charges; dismiss this (?:entry|line) unless it states treatment\./g, ". You decide in step 3, Check the bills, whether to count them. Dismiss this line unless it states treatment.")
22	      .replace(/\bpick a quote\b/g, "pick highlighted words").replace(/\ba quote\b/g, "highlighted words")
23	      .replace(/\b([Tt])he (?:AI )?second (?:AI )?check\b/g, (m, t) => (t === "T" ? "A second AI check" : "a second AI check"))
24	      .replace(/\bsecond check\b/g, "second AI check")
25	      .replace(/\bthe quoted text\b/g, "the highlighted words").replace(/\bquoted text\b/g, "highlighted words")
26	      .replace(/\b([Tt])he quote (does not|is not|is|has|says|contains|states|shows|carries|gives|labels)\b/g, (m, t, v) => `${t}he highlighted words ${v === "is" ? "are" : v === "has" ? "have" : v === "carries" ? "carry" : v === "gives" ? "give" : v === "labels" ? "label" : v === "does not" ? "do not" : v === "is not" ? "are not" : v === "says" ? "say" : v === "contains" ? "contain" : v === "states" ? "state" : "show"}`)
27	      .replace(/\bsummary or quote\b/g, "line or highlighted words").replace(/\bthe quotes?\b/g, "the highlighted words").replace(/\bQuote\b/g, "The highlighted words").replace(/\bquotes?\b/g, "highlighted words")
28	      .replace(/\bthe summary\b/g, "the line").replace(/\bThe summary\b/g, "The line").replace(/\bsummary\b/g, "line")
29	      .replace(/\ban itemized service line\b/g, "a single dated bill line").replace(/\bitemized service line\b/g, "single dated bill line").replace(/\ban itemized\b/g, "a line-by-line").replace(/\bitemized\b/g, "line-by-line")
30	      .replace(/\binternal notes\b/g, "notes for the attorney").replace(/\bthe model's\b/gi, G.provenance().kind === "prepared" ? "the prepared answer's" : "the AI's").replace(/\bmodel\b/g, G.provenance().kind === "prepared" ? "prepared answer" : "AI")
31	      .replace(/\bflags\b/g, "warnings").replace(/\bflag\b/g, "warning").replace(/\bthis entry\b/g, "this line"))).join("");
32	  };
33	
34	  /* ---------- a refused edit that dropped a qualifier: name the words (UX review T-181 major). The server says which KIND (detail.qualifiers); the words are found in the quote by code. ---------- */
35	  const QUAL = {
36	    self_report: { re: /\b(?:complained of|complains of|complaint of|c\/o|reports?|reported|states?|stated|says?|said|denies|denied|per (?:the )?patient|according to)\b/gi, because: "which says whose account this is" },
37	    hedge: { re: /\b(?:may|might|possibly|possible|probable|probably|likely|appears?|suspected|suggests?|suggestive of|consistent with|cannot be excluded|rule out|r\/o)\b/gi, because: "which shows it is not certain" },
38	    negation: { re: /\b(?:no|not|denies|denied|without|negative|none|never)\b/gi, because: "which says something is not there" },
39	    laterality: { re: /\b(?:left|right|bilateral)\b/gi, because: "which says which side" },
40	    approx: { re: /\b(?:approx\.?|approximately|about|around|roughly|estimated)\b/gi, because: "which shows the figure is only close" },
41	  };
42	  const FALLBACK_WORDS = { self_report: "a phrase that says whose account this is", hedge: "a word that shows it is not certain", negation: "a word that says something is not there", laterality: "the side (left or right)", approx: "a word that shows the figure is only close" };
43	  R.droppedText = function (kinds, quote, summary, before) {
44	    const low = String(summary || "").toLowerCase(), out = [];
45	    (kinds || []).forEach((k) => {
46	      const q = QUAL[k]; if (!q) return;
47	      const gone = (text) => [...new Set((String(text || "").match(q.re) || []).map((w) => w.toLowerCase()))].filter((w) => !low.includes(w));
48	      const found = gone(before).length ? gone(before) : gone(quote);          // the words she took out of the line first, else the quote's own words
49	      out.push(found.length ? `“${found.slice(0, 3).join("”, “")}”, ${q.because}` : FALLBACK_WORDS[k]);
50	    });
51	    if (!out.length) return null;
52	    return `Your line leaves out ${out.join("; and ")}. Put ${out.length === 1 && /^“[^”]+”,/.test(out[0]) && !/”, “/.test(out[0]) ? "it" : "those words"} back in the line.`;
53	  };
54	
55	  /* ---------- dates and money (code only) ---------- */
56	  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
57	  R.longDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? `${MONTHS[+m[2] - 1]} ${+m[3]}, ${m[1]}` : ""; };
58	  R.shortDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? `${MONTHS[+m[2] - 1].slice(0, 3)} ${+m[3]}, ${m[1]}` : "No date"; };
59	  R.money = (cents) => (cents < 0 ? "-" : "") + "$" + (Math.abs(cents) / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
60	
61	  /* ---------- provenance tags (D-065): a prepared answer says "Prepared answer", never "AI" ---------- */
62	  R.tagFor = function (item) {
63	    const p = G.provenance();
64	    if (item.entered_by_reviewer || (item.edited && item.edited.summary)) return { cls: "you", text: "Written by you" };
65	    if (item.prepared) return { cls: "prep", text: "Prepared answer", title: p.note };
66	    if (item.ai_drafted === false || item.origin === "code") return null;
67	    return { cls: "ai", text: "AI draft", title: p.kind === "live" ? p.note : "Drafted by an AI. " + p.note };
68	  };
69	  // G.provenance() follows the open case: a case whose lines an AI wrote says so, never "not written by an AI model" (T-181 r2)
70	  R.aiNote = () => { const p = G.provenance(), hl = G.store.health; return p.kind === "live" && hl && hl.ai_banner ? hl.ai_banner : p.note; };
71	
72	  /* ---------- the second check disputed this item (D-066; the same rule as review.judge_dispute) ---------- */
73	  const DISPUTE = { partially: "A second AI check found this only partly supported by the highlighted words.", unsupported: "A second AI check found this not supported by the highlighted words.",
74	    disagrees: "A second AI check disagreed with the first result for this item." };
75	  R.dispute = function (item) {
76	    const j = item && item.ladder && item.ladder.judge, vv = j && j.verdict, v = vv === "disagree" ? "disagrees" : vv;
77	    if (DISPUTE[v]) return v;
78	    const rs = (item && (item.state_reasons || item.reasons)) || [];
79	    return rs.includes("JUDGE_PARTIAL") ? "partially" : rs.includes("JUDGE_UNSUPPORTED") ? "unsupported" : rs.includes("JUDGE_DISAGREES") ? "disagrees" : null;
80	  };
81	  /* An amount's second check names the way it disagreed (judge reason_code): say which way, so the tick is not a formality (paralegal review T-181 minor). */
82	  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD_BE_DAMAGES: "a damages figure (for example lost wages)" };
83	  R.disputeText = function (v, item) {
84	    const code = item && item.ladder && item.ladder.judge && item.ladder.judge.reason_code;
85	    if (v === "disagrees" && AMOUNT_WAY[code]) return `A second AI check thought this may be ${AMOUNT_WAY[code]}, not what it was first sorted as.`;
86	    if (v === "disagrees" && (code === "SHOULD_BE_UNCLEAR" || code === "TEXT_AMBIGUOUS")) return "A second AI check could not read this figure with confidence.";
87	    return DISPUTE[v];
88	  };
89	
90	  /* ---------- the record, with the highlighted words marked, or its sentences tappable ---------- */
91	  R.recBlock = function (rec, opt) {
92	    opt = opt || {};
93	    let text = rec.text || "", base = rec.char_start || 0;
94	    const pre = /^[\s\S]*?\nExcerpt: ?/.exec(text);
95	    let preEnd = pre ? pre[0].length : 0;
96	    const full = text.length, win = opt.win && opt.win[0] > 0 || opt.win && opt.win[1] < full ? opt.win : null;       // opt.win = [from, to] in the record's own offsets: show only that part (several records in one warning)
97	    if (win) { text = text.slice(win[0], win[1]); base += win[0]; preEnd = Math.max(0, preEnd - win[0]); }
98	    const n = text.length;
99	    const marks = (opt.marks || []).map(([a, b]) => [Math.max(0, a - base), Math.min(n, b - base)]).filter(([a, b]) => b > a).sort((x, y) => x[0] - y[0]);
100	    const cuts = new Set([0, n, preEnd]);
101	    marks.forEach(([a, b]) => { cuts.add(a); cuts.add(b); });
102	    const sents = (opt.sentences || []).map((s) => ({ ...s, a: s.start - base, b: s.end - base }));
103	    sents.forEach((s) => { cuts.add(s.a); cuts.add(s.b); });
104	    const pts = [...cuts].filter((x) => x >= 0 && x <= n).sort((x, y) => x - y), body = [];
105	    for (let i = 0; i < pts.length - 1; i++) {
106	      const a = pts[i], b = pts[i + 1], piece = text.slice(a, b); if (!piece) continue;
107	      const sent = sents.find((s) => a >= s.a && b <= s.b), marked = marks.some(([x, y]) => a >= x && b <= y);
108	      if (sent) {
109	        if (!sent.__el) {
110	          const el = h("span", { class: "sent" + (opt.picked && opt.picked.has(sent.start) ? " on" : ""), role: "button", tabindex: "0", "aria-pressed": opt.picked && opt.picked.has(sent.start) ? "true" : "false",
111	            "data-testid": "sentence", "data-start": sent.start, onclick: () => opt.onPick(sent), onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); opt.onPick(sent); } } });
112	          sent.__el = el; body.push(el);
113	        }
114	        sent.__el.append(document.createTextNode(piece));
115	      } else {
116	        const el = h(marked ? "mark" : "span", { class: a < preEnd ? "meta" : null }, piece);
117	        body.push(el);
118	      }
119	    }
120	    if (win && win[0] > 0) body.unshift(h("span", { class: "ell" }, "… "));
121	    if (win && win[1] < full) body.push(h("span", { class: "ell" }, " …"));
122	    const out = [];
123	    if (opt.head) out.push(h("div", { class: "rec-h" }, opt.head));
124	    out.push(h("div", { class: "rec", "data-testid": "record-text", "data-record": rec.id }, body));
125	    return out;
126	  };
127	
128	  /* ---------- the engine ---------- */
129	  const undecided = (i) => !!i && G.steps.undecided(i);
130	  R.run = async function (ctx, cfg) {
131	    const token = ctx.token, body = document.body;
132	    const S = { ctx, cfg, token, c: ctx.case, queue: [], idx: -1, ui: {}, busy: false, alive: true, said: null, err: null, screen: null, forceCompare: new Map(), part2: new Set(), el: {} };
133	    const q$ = (id) => S.queue.find((q) => q.id === id);
134	    S.item = (id) => cfg.find(S.c, id);
135	    S.counted = () => S.queue.filter((q) => !q.optional && S.item(q.id));
136	    S.left = () => S.counted().filter((q) => undecided(S.item(q.id)));
137	    S.numberOf = (id) => { const i = S.counted().findIndex((q) => q.id === id); return i < 0 ? null : i + 1; };
138	    S.record = (rid) => (S.c.records || []).find((r) => r.id === rid);
139	    S.recOf = (pos) => (S.c.records || []).find((r) => pos >= r.char_start && pos < r.char_end);
140	
141	    function say(text, undo) { S.said = text ? { text, undo } : null; drawStatus(); }
142	    S.say = say;
143	    S.fail = async function (e) {
144	      if (e && e.name === "AbortError") return;
145	      if (e instanceof G.ApiError && e.status === 409 && e.code === "stale_item") {
146	        let now = "";
147	        try { await S.reload(); const it = S.cur(); now = it && it.review_status === "dismissed" ? " It is now left out." : it && (it.review_status === "accepted" || it.review_status === "edited") ? " It is now kept." : ""; } catch (_) { /* the message below is enough */ }
148	        S.err = { text: `This item changed in another tab. We've loaded the latest.${now} Choose again if that is wrong.` };
149	      } else if (e instanceof G.ApiError && e.code === "COMPARE_REQUIRED") {
150	        const it = S.cur(); if (it) S.forceCompare.set(it.id, (e.detail && e.detail.verdict) || "disagrees");       // the page did not know: show the compare box (the server's reason is in it), never a raw error
151	        S.err = null;
152	      } else if (e instanceof G.ApiError && e.code === "invalid_edit" && e.detail && Array.isArray(e.detail.qualifiers) && R.droppedText(e.detail.qualifiers, S.lastEdit && S.lastEdit.excerpt, S.lastEdit && S.lastEdit.summary, S.lastEdit && S.lastEdit.before)) {
153	        S.err = { text: R.droppedText(e.detail.qualifiers, S.lastEdit.excerpt, S.lastEdit.summary, S.lastEdit.before) };
154	      } else if (e instanceof G.ApiError && e.status === 409 && e.code === "item_rejected") {
155	        S.err = { text: "We couldn't check this one, so it can't be answered here. We've loaded the latest." };
156	        try { await S.reload(); } catch (_) { /* keep the message */ }
157	      } else if (e instanceof G.ApiError && e.code === "CONFIRM_REQUIRED" && e.detail && e.detail.message) {
158	        S.err = { text: R.plain(e.detail.message) };
159	      } else S.err = { text: R.plain(e && e.message ? e.message : "Something went wrong. Try again.") };
160	      render(true);
161	    };
162	    S.cur = () => (S.idx >= 0 && S.queue[S.idx] ? S.item(S.queue[S.idx].id) : null);
163	    S.reload = async function () { S.c = await ctx.refresh(); updateTitlebar(); };
164	    S.act = async function (fn) {
165	      if (S.busy || !S.alive) return undefined;
166	      S.busy = true; S.err = null; syncButtons();
167	      try { return await fn(); } catch (e) { await S.fail(e); return undefined; } finally {
168	        S.busy = false;
169	        if (S.alive) { syncButtons(); drawStatus(); if (!S.ended && S.screen && (!document.activeElement || document.activeElement === document.body)) focusFirst(S.screen); }     // the click disabled the button that had focus: put it on the next item's first answer
170	      }
171	    };
172	    /* every review POST carries version + expected_status of the item on screen (T-178) */
173	    S.post = (item, action, extra) => G.api.review(token, item.id, { action, version: item.version, expected_status: item.review_status, ...(extra || {}) });
174	    S.go = (item) => { const i = S.queue.findIndex((q) => q.id === item.id); S.open(i < 0 ? S.idx : i); };
175	
176	    /* ---- frame ---- */
177	    const E = S.el;
178	    E.eyebrow = h("div", { class: "eyebrow" }, `Step ${cfg.step} of 4`);
179	    E.toggle = h("button", { type: "button", class: "steps-toggle", "data-testid": "btn-steps", "aria-expanded": "false", "aria-controls": "step-list", onclick: () => toggleSteps() }, `Step ${cfg.step} of 4`, h("span", { "aria-hidden": "true" }, " ▾"));
180	    E.ai = h("div", { class: "t-ai", "data-testid": "ai-note" }, R.aiNote());
181	    E.count = h("span", { class: "num", "data-testid": "item-count" });
182	    E.prog = h("span", { class: "of num", "data-testid": "progress-text" });
183	    E.fill = h("i");
184	    E.bar = h("div", { class: "bar", role: "progressbar", "aria-label": "Progress in this step", "aria-valuemin": "0", "aria-valuemax": "100" }, E.fill);
185	    E.total = h("div", { class: "tc-v num", "data-testid": "total-value" }, "$0.00");
186	    E.titlebar = h("div", { class: "titlebar", "data-testid": "titlebar" },
187	      h("div", { class: "t-main" }, E.eyebrow, E.toggle, h("h1", { "data-testid": "page-title" }, cfg.title), E.ai),
188	      cfg.chip ? h("div", { class: "total-chip", "aria-live": "polite", "data-testid": "total-chip" }, h("div", { class: "tc-l" }, "Bill total so far"), E.total) : null,
189	      h("div", { class: "count-box", "data-testid": "count-box" }, h("div", { class: "count-line" }, E.count, E.prog), E.bar));
190	    E.srcHead = h("span", { class: "ch-sub", "data-testid": "src-head" });
191	    E.srcBody = h("div", { class: "card-b", "data-testid": "card-source", tabindex: "0", "aria-label": "The record" });
192	    E.lineHead = h("div", { class: "card-h", "data-testid": "line-head" });
193	    E.lineBody = h("div", { class: "card-b", "data-testid": "line-body" });
194	    E.foot = h("div", { class: "card-f plain", "data-testid": "card-foot", tabindex: "-1" });
195	    E.lineCard = h("section", { class: "card card-line", "aria-label": "To check", "data-testid": "card-line" }, E.lineHead, E.lineBody, E.foot);
196	    E.work = h("main", { class: "work", id: "main", "data-testid": "work" },
197	      h("section", { class: "card card-src", "aria-label": "From the record", "data-testid": "card-src" }, h("div", { class: "card-h" }, h("span", { class: "ch-title" }, "From the record"), E.srcHead), E.srcBody), E.lineCard);
198	    const btn = (cls, tid, key) => h("button", { type: "button", class: "btn " + cls, "data-testid": tid, "aria-keyshortcuts": key || null });
199	    E.question = h("p", { class: "question", id: "q", "data-testid": "question" });
200	    E.yes = btn("answer primary", "answer-yes", "a"); E.no = btn("answer", "answer-no", "d");
201	    E.yes.setAttribute("data-autofocus", "");
202	    E.back = btn("quiet", "btn-back", "ArrowLeft"); E.third = btn("quiet", "btn-third", "e"); E.later = btn("quiet", "btn-later", "ArrowRight");
203	    E.statusText = h("span", { class: "st-msg", "data-testid": "status-text" }); E.undo = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-undo", hidden: true }, "Undo");
204	    E.showBox = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-show-box", hidden: true }, "Show box");
205	    E.status = h("p", { class: "status", role: "status", "aria-live": "polite", "data-testid": "status-slot" }, E.statusText, E.undo, E.showBox);
206	    E.actions = h("div", { class: "actions", "data-testid": "actions" }, h("div", { class: "actions-in" }, E.question,
207	      h("div", { class: "big", role: "group", "aria-labelledby": "q" }, E.yes, E.no), h("div", { class: "small" }, E.back, E.third, E.later), E.status));
208	    E.back.textContent = "‹ Back"; E.later.textContent = "Decide later";
209	    E.back.onclick = () => back();
210	    E.later.onclick = () => { const l = S.screen && S.screen.later; if (l === false) return; if (l && l.run) l.run(); else S.skip(); };
211	    ctx.view.replaceChildren(E.titlebar, E.work, E.actions);
212	    ctx.layout("frame");
213	
214	    function toggleSteps(force) {
215	      const open = force != null ? force : !body.classList.contains("steps-open");
216	      body.classList.toggle("steps-open", open); E.toggle.setAttribute("aria-expanded", open ? "true" : "false");
217	    }
218	    const onDocClick = (e) => { if (body.classList.contains("steps-open") && !e.target.closest("#step-bar") && !e.target.closest("[data-testid=btn-steps]")) toggleSteps(false); };
219	
220	    function drawStatus() {
221	      const s = S.said;
222	      const box = E.yes && E.yes.disabled && !S.busy && E.foot.querySelector("input[type=checkbox]:not(:checked)");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)
223	      const tick = box ? (box.dataset.testid === "check-compare" ? "Tick the box to say you compared them." : "Tick the box first.") : "";      // no direction word: the box can be above the bar or below the screen
224	      const saved = s && !s.undo && /^Saved/.test(s.text);      // a "Saved" note must not hide the reason Yes is greyed: both stay until she ticks
225	      const why = box && (!s || saved);
226	      E.statusText.textContent = why ? (saved ? "Saved. " : "") + tick : s ? s.text : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
227	      E.status.classList.toggle("hint", !s && !why);
228	      E.status.dataset.why = why ? "tick" : "";
229	      E.undo.hidden = !(s && s.undo);
230	      E.undo.onclick = s && s.undo ? () => S.act(s.undo) : null;
231	      const hidden = !!why && boxHidden(box);      // the box is under the bar or below the screen: one tap brings it into view
232	      E.showBox.hidden = !hidden;
233	      E.showBox.onclick = hidden ? () => revealBox(box) : null;
234	    }
235	    function boxHidden(box) {
236	      const r = box.getBoundingClientRect(), bar = E.actions.getBoundingClientRect();
237	      return r.bottom > bar.top - 4 || r.top < 0;
238	    }
239	    function revealBox(box) {
240	      const bar = E.actions.getBoundingClientRect();
241	      box.style.scrollMarginBottom = Math.ceil(window.innerHeight - bar.top + 12) + "px";
242	      try { box.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* nothing to scroll */ }
243	      box.focus({ preventScroll: true }); drawStatus();
244	    }
245	
246	    function updateTitlebar() {
247	      const items = S.counted(), left = S.left().length, total = items.length, done = total - left;
248	      const q = S.queue[S.idx], n = q && !q.optional ? S.numberOf(q.id) : null;
249	      E.count.textContent = S.screen && S.screen.counter ? S.screen.counter : n ? `${cfg.unit} ${n} of ${total}` : q && q.optional ? "Optional" : `${total} ${cfg.unit.toLowerCase()}s`;
250	      E.prog.textContent = `${done} answered · ${left} to go`;
251	      const pct = total ? Math.round((done / total) * 100) : 100;
252	      E.fill.style.width = pct + "%"; E.bar.setAttribute("aria-valuenow", String(pct));
253	      if (cfg.chip) E.total.textContent = R.money(((S.c.totals || {}).accepted || {}).cents || 0);
254	    }
255	
256	    /* ---- render one screen ---- */
257	    function fillTag(tag, extra) { return tag ? h("span", { class: "tag " + tag.cls, title: tag.title || null, "data-testid": extra || "line-tag" }, tag.text) : null; }
258	    function syncButtons() {
259	      const sc = S.screen; if (!sc) return;
260	      const set = (el, def) => {                                    // an absent answer keeps its place (invisible), so nothing else moves
261	        if (!def) { el.style.visibility = "hidden"; el.disabled = true; el.setAttribute("aria-hidden", "true"); el.tabIndex = -1; return; }
262	        el.disabled = S.busy || (typeof def.disabled === "function" ? def.disabled() : !!def.disabled);
263	        el.style.visibility = ""; el.removeAttribute("aria-hidden"); el.removeAttribute("tabindex");
264	      };
265	      set(E.yes, sc.yes); set(E.no, sc.no); set(E.third, sc.third);
266	      E.back.disabled = S.busy || sc.back === false; E.later.disabled = S.busy;
267	      E.later.style.visibility = sc.later === false ? "hidden" : ""; E.later.tabIndex = sc.later === false ? -1 : 0;
268	      E.third.classList.toggle("hint", !!(sc.third && sc.third.hint));
269	      E.undo.disabled = S.busy;
270	    }
271	    function drawBtn(el, def, keep) {
272	      if (!def) { el.replaceChildren(keep || ""); el.classList.remove("two"); el.onclick = null; return; }
273	      el.replaceChildren(...[def.label, def.sub ? h("span", { class: "sub" }, def.sub) : null].filter(Boolean));
274	      el.classList.toggle("two", !!def.sub); el.onclick = () => def.run();
275	      if (el === E.yes) el.classList.toggle("primary", !def.plain);
276	    }
277	    function render(keepScroll) {
278	      const item = S.cur(), q = S.queue[S.idx];
279	      if (!item) return finish();
280	      const sc = (S.screen = cfg.present(S, item, q));
281	      E.lineCard.dataset.itemId = item.id; E.lineCard.dataset.kind = item.kind || ""; E.lineCard.dataset.mode = S.ui.mode || "view";
282	      const head = [fillTag(sc.tag), fillTag(sc.tag2, "line-tag2"), sc.sub ? h("span", { class: "ch-sub", "data-testid": "line-sub" }, sc.sub) : null];
283	      E.lineHead.replaceChildren(...head.filter(Boolean));
284	      const bodyScroll = E.lineBody.scrollTop;
285	      E.lineBody.replaceChildren(...[].concat(sc.body || []).filter(Boolean));
286	      E.lineBody.scrollTop = keepScroll ? bodyScroll : 0;
287	      if (!keepScroll) E.lineCard.scrollTop = 0;
288	      const err = S.err ? { cls: "bad", nodes: [h("strong", {}, "Not saved. "), S.err.text] } : null;
289	      const foot = err || sc.foot || { cls: "plain", nodes: [] };
290	      E.foot.className = "card-f " + (foot.cls || "plain"); E.foot.replaceChildren(...[].concat(foot.nodes || []).filter(Boolean));
291	      if (err) E.foot.setAttribute("role", "alert"); else E.foot.removeAttribute("role");
292	      E.question.textContent = sc.question || "";
293	      drawBtn(E.yes, sc.yes, "Yes"); drawBtn(E.no, sc.no, "No"); drawBtn(E.third, sc.third, "Fix the wording");
294	      E.later.textContent = sc.later && sc.later.label ? sc.later.label : "Decide later";
295	      // a phone: when any item of this step needs a tick box the line card gets the room for the whole visit (so nothing moves between items), and the line and its box are on screen together
296	      S.sticky = S.sticky || S.queue.some((q) => { const it = S.item(q.id); return !!it && (!!R.dispute(it) || !!it.edit_to_check || (it.countable && it.kind !== "charge") || (it.flag && it.confirm_required)); }) || !!E.foot.querySelector("input[type=checkbox]");
297	      E.work.classList.toggle("needs-check", !!S.sticky);      // before the record is drawn: the window is its final size when the highlight is scrolled into it
298	      renderSource(false);
299	      updateTitlebar(); syncButtons(); drawStatus();
300	      if (err) showRefusal();
301	      if (!keepScroll) focusFirst(sc);
302	    }
303	    function renderSource(keep) {
304	      const sc = S.screen; if (!sc || !sc.src) { E.srcHead.textContent = ""; E.srcBody.replaceChildren(); return; }
305	      const top = E.srcBody.scrollTop;
306	      E.srcHead.textContent = sc.src.head || ""; E.srcBody.replaceChildren(...sc.src.nodes().filter(Boolean));
307	      if (keep) E.srcBody.scrollTop = top;
308	      else alignMark();
309	    }
310	    /* the first highlighted word is in the record window: top-aligned with one line of the record above it on a phone (the window is small), a third down on a wide screen. Measured with rects, not offsetTop (the window is not the mark's offset parent). */
311	    function alignMark() {
312	      const box = E.srcBody, m = box.querySelector("mark, .sent.on");
313	      if (!m) { box.scrollTop = 0; return; }
314	      const narrow = matchMedia("(max-width: 760px)").matches, lead = narrow ? Math.min(30, box.clientHeight / 4) : box.clientHeight / 3;
315	      const at = m.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
316	      box.scrollTop = Math.max(0, at - lead);
317	    }
318	    S.alignMark = alignMark;
319	    /* a refused save: its words sit in the line card's foot, which on a phone can be below the visible part of the card (the card scrolls as one box) or under the action bar. Bring it into view, never under the bar. */
320	    function showRefusal() {
321	      const card = E.lineCard, f = E.foot;
322	      if (card.scrollHeight > card.clientHeight + 1) {
323	        const c = card.getBoundingClientRect(), r = f.getBoundingClientRect();
324	        if (r.bottom > c.bottom) card.scrollTop += r.bottom - c.bottom + 2;
325	      }
326	      try { f.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* the card scroll above is enough */ }
327	    }
328	    S.renderSource = () => renderSource(true);
329	    S.render = (keep) => render(!!keep);
330	    S.sync = () => { syncButtons(); if (!S.said || (!S.said.undo && /^Saved/.test(S.said.text))) drawStatus(); };
331	    function focusFirst(sc) {
332	      const f = sc.focus === "field" ? E.lineBody.querySelector("textarea, input") : null;
333	      const target = f || (!E.yes.disabled ? E.yes : E.foot.querySelector("input[type=checkbox]") || (sc.yes && !S.busy ? E.foot : (!E.no.disabled ? E.no : null)));      // a refused Yes with no tick box: focus the reason, never a button that would answer
334	      if (target && document.activeElement !== target && !S.firstPaint) target.focus({ preventScroll: true });
335	    }
336	
337	    /* ---- moving ---- */
338	    function writeUrl(id) { try { history.replaceState(history.state, "", id ? G.url.step(token, cfg.step, id) : G.url.step(token, cfg.step)); } catch (_) { /* the screen still works */ } }
339	    S.open = function (i) {
340	      if (i < 0 || i >= S.queue.length) return finish();
341	      S.idx = i; S.ui = {}; S.err = null; S.screen = null;
342	      writeUrl(S.queue[i].id); render(false);
343	    };
344	    function nextUndecided(from) { for (let i = from + 1; i < S.queue.length; i++) { const q = S.queue[i], it = S.item(q.id); if (it && !q.optional && undecided(it)) return i; } return -1; }
345	    S.next = function () { const i = nextUndecided(S.idx); if (i < 0) return finish(); S.open(i); };
346	    S.skip = function () {                                         // Decide later and the right arrow: the next item in the list, decided or not
347	      let i = S.idx + 1; while (i < S.queue.length && !S.item(S.queue[i].id)) i++;
348	      if (i >= S.queue.length) return finish(); S.open(i);
349	    };
350	    function back() {
351	      let i = S.idx - 1; while (i >= 0 && !S.item(S.queue[i].id)) i--;
352	      if (i < 0) { ctx.go(cfg.step === 2 ? G.url.records(token) : G.url.timeline(token)); return; }
353	      S.open(i);
354	    }
355	    S.firstUndecided = () => nextUndecided(-1);
356	    function finish() {
357	      writeUrl(null);
358	      const node = S.counted().length ? cfg.done(S) : cfg.empty(S);
359	      ctx.layout("page"); ctx.view.replaceChildren(node); window.scrollTo(0, 0);
360	      S.ended = true; document.title = cfg.title + " – Treatment Timeline"; const hh = G.$("h1", ctx.view); if (hh) { hh.tabIndex = -1; hh.focus({ preventScroll: true }); }
361	    }
362	
363	    /* ---- the common write: POST, refresh, say what was saved, move on ---- */
364	    S.decide = async function (item, action, extra, opt) {
365	      opt = opt || {};
366	      return S.act(async () => {
367	        const resp = await S.post(item, action, extra);
368	        S.c = await ctx.refresh();
369	        const fresh = S.item(item.id) || resp.item, num = S.numberOf(item.id);
370	        const label = (num ? `${cfg.unit.toLowerCase()} ${num}` : "this item"), said = cfg.statusFor ? cfg.statusFor(S, fresh, resp, action, extra) : "saved";
371	        const undo = async () => {
372	          const cur = S.item(item.id) || fresh;
373	          await S.post(cur, "reset"); S.c = await ctx.refresh(); S.ui = {}; S.go(cur); say(`Undone: ${label} is back to not decided.`, null); render(false);
374	        };
375	        if (cfg.onResponse) cfg.onResponse(S, resp);
376	        updateTitlebar();
377	        if (opt.stay) { say(`Saved: ${label} ${said}.`, undo); render(false); return resp; }
378	        say(`Saved: ${label} ${said}.`, undo);
379	        S.next();
380	        return resp;
381	      });
382	    };
383	
384	    /* ---- keyboard: A / D / E and the arrows (not while typing; not with a modifier) ---- */
385	    const onKey = (e) => {
386	      if (S.ended || e.ctrlKey || e.metaKey || e.altKey || e.defaultPrevented) return;
387	      const t = e.target, tag = t && t.tagName;
388	      if (tag === "TEXTAREA" || tag === "INPUT" && t.type !== "checkbox" || tag === "SELECT" || (t && t.isContentEditable)) return;
389	      const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
390	      const press = (el, def) => {
391	        if (!def) return; e.preventDefault();
392	        if (el.disabled) {
393	          const c = E.foot.querySelector("input[type=checkbox]:not(:checked)");
394	          if (c) c.focus();
395	          else if (!S.busy) say(`“${el.textContent}” is not available here.${def.why ? " " + def.why : ""}`, null);        // focus stays where it was: the next Space or Enter must never answer for her
396	          return;
397	        }
398	        el.click();
399	      };
400	      if (k === "a") press(E.yes, S.screen && S.screen.yes);
401	      else if (k === "d") press(E.no, S.screen && S.screen.no);
402	      else if (k === "e") press(E.third, S.screen && S.screen.third);
403	      else if (k === "ArrowRight") { if (!E.later.disabled && S.screen && S.screen.later !== false) { e.preventDefault(); E.later.click(); } }
404	      else if (k === "ArrowLeft") { if (!E.back.disabled) { e.preventDefault(); E.back.click(); } }
405	      else if (k === "Escape" && body.classList.contains("steps-open")) toggleSteps(false);
406	    };
407	    document.addEventListener("keydown", onKey); document.addEventListener("click", onDocClick);
408	
409	    /* ---- start ---- */
410	    S.queue = cfg.buildQueue(S.c);
411	    S.firstPaint = true;
412	    updateTitlebar();
413	    const want = ctx.query.get("item"), wi = want ? S.queue.findIndex((q) => q.id === want && S.item(q.id)) : -1;
414	    if (wi >= 0) S.open(wi);
415	    else { const f = S.firstUndecided(); if (f >= 0) S.open(f); else finish(); }
416	    S.firstPaint = false;
417	    return function cleanup() { S.alive = false; document.removeEventListener("keydown", onKey); document.removeEventListener("click", onDocClick); body.classList.remove("steps-open"); };
418	  };
419	
420	  /* ---------- pieces the step modules share ---------- */
421	  R.check = function (S, key, label, opt) {
422	    const box = h("input", { type: "checkbox", "data-testid": "check-" + key, "data-autofocus": opt && opt.focus ? "" : null });
423	    box.checked = !!S.ui["chk_" + key];
424	    box.addEventListener("change", () => { S.ui["chk_" + key] = box.checked; S.sync(); });
425	    return h("label", { class: "check" }, box, h("span", {}, label));
426	  };
427	  R.ticked = (S, key) => !!S.ui["chk_" + key];
428	
429	  /* An answers row for a done screen: number, date, label, chip, Change. */
430	  R.answerRow = function (n, date, label, chip, chipCls, href) {
431	    return h("li", { "data-testid": "answer-row" }, h("span", { class: "n" }, String(n)), h("span", { class: "d" }, date), h("span", { class: "lbl", title: label }, label),
432	      h("span", { class: "ans" }, h("span", { class: "tag " + chipCls, "data-testid": "answer-chip" }, chip)), h("a", { class: "btn", href, "data-testid": "btn-change" }, "Change"));
433	  };
434	  R.doneFrame = function (step, title, ...kids) {
435	    return h("main", { class: "wrap", id: "main", "data-testid": "done-page" }, h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("div", { class: "eyebrow" }, `Step ${step} of 4`), h("h1", { "data-testid": "page-title" }, title))), ...kids);
436	  };
437	})();
438	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:29.995Z

**tool call — Bash**
````
{
 "command": "cat tests/e2e/conftest.py | head -120; ls tests/e2e/guided | head -30; ls .claude/launch.json 2>/dev/null && cat .claude/launch.json"
}
````

### User / tool · 2026-11-03T04:34:30.090Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:30.850Z

**tool call — Bash**
````
{
 "command": "grep -n \"reason_code\\|judge_reason\\|\\\"reason\\\"\" memory/contracts/api.md | cut -c1-300 | head -30; grep -rn \"judge_note\\|judge_reason\\|\\.reason\\b\" app/backend/*.py | grep -i judge | head"
}
````

### User / tool · 2026-11-03T04:34:30.952Z

**tool result**
````
33:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset, and (D-064) `count` + `confirm: "separate_charge"` for an amount held back only for a missing detail (see `countable`).  D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (
113:**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY" | "EDIT_
134:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and ever
141:**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `
296:                  "reason": "Another date in this packet uses month first (Record 1: 03/14/2026)",
376:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to expo
384:**D-066 (T-179): a disputed item is accepted only with her compare.** An item the second AI check disputed is one whose `ladder.judge.verdict` is `partially`, `unsupported`, `disagrees` (or the amount judge's `disagree`), or whose `reasons` hold `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_DIS
417:**Flags that need a named confirm (D-059).** A charge can carry `flag` (else `null`): `{flag: "likely_duplicate" | "likely_total", name, message, confirm_with, of, confirmed_at?}` and `confirm_required: true` while it is `pending`. `likely_duplicate`: set only when a paralegal PROMOTES a figure 
419:`POST .../items/{id}/review` with `{"action": "count", "confirm": "separate_charge"}` (an amount only; `400 bad_request` for an entry or flag, `409 item_rejected` for a rejected amount) counts a countable amount: it becomes class `charge` and is `accepted` in one step, so the letter total (R-EX-
426:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every
574:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothin
604:**Judge rationale is a closed reason code plus a fixed sentence (D-028).** The judge returns `verdict` + `reason_code` from a closed list, never prose, so `rationale` is the fixed sentence for that code (`why.judge_detail`), written by code. `reason_code` is read from `ladder.judge.reason_code`;
612:  "reason_code": null,                  // closed code when status is fail, or when a pass still explains a state (e.g. AMOUNT_RATE_NOT_TOTALED); else null
618:`status` meaning: `pass` the check ran and passed (or the human decided to accept); `fail` the check ran and found a problem (the item is then `needs_review` or `rejected`); `skipped` not run on purpose (a step before it already rejected the item, no judge applies to code-made items, the judge d
622:`evidence` keys (all optional): `excerpt` `{record_id, start, end, text}` (offsets absolute into the case text); `spans[]` (same shape, for flags); `tokens[]` (summary tokens not in the quote); `values` (small object, for example `{"text": "$6,240", "value_cents": 624000, "kind": "charge", "clas
634:      "why": "The AI read this record and proposed a one-line summary and a quote.", "reason_code": null, "rule": "row 4", "blocks_export": false,
640:      "reason_code": "JUDGE_PARTIAL", "rule": "row 4", "blocks_export": false,
642:                    "call_id": "c27", "judge_verdict": "partially", "judge_reason_code": "DROPS_QUALIFIER",
648:- **amount:** `found_in_text` (code, `GROUNDING_AMOUNT_NOT_IN_TEXT`), `amount_class` (code; pass for a charge; pass with `reason_code` `AMOUNT_RATE_NOT_TOTALED`/`AMOUNT_ESTIMATE`/`AMOUNT_DAMAGES` for the classes that are never totaled; fail for `AMOUNT_UNCLEAR`), `injection_scan`, `judge_2` (llm
663:      "why": "9 records found.", "reason_code": null, "rule": "row 1",
666:    { "id": "dates", "n": 3, "label": "Dates read by code", "kind": "code", "status": "fail", "reason_code": "DATE_AMBIGUOUS",
675:    { "id": "export_gate", "n": 10, "label": "Ready to export?", "kind": "code", "status": "fail", "reason_code": "NOTHING_ACCEPTED",
678:      "blockers": [ { "item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "...", "next_action": {"code": "DECIDE", "text": "..."} } ],
679:      "warnings": [ { "reason_code": "ITEMS_NOT_REVIEWED", "count": 21, "why": "21 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "text": "...", "target": {"view": "queue"}} } ],
684:`verdict.code` for the case: `ready` (export gate open), `needs_attention` (nothing accepted yet, or accepted items not double-checked), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.judge.reason_code` for entries, amounts, flags, edits and manual entries (in `ladd
686:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the las
695:  "rejections": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "verdict": "partially", "reason_code": "DROPS_QUALIFIER",
710:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
724:            "gate_blockers": [ { "reason_code", "kind", "item_id", "why" } ], "gate_warnings": [ { "reason_code", "count", "why" } ] },
726:  "next_action": { "item_id": "f_r3_1" | null, "kind": "entry|flag|amount|case|run", "reason": "plain sentence" } | null,
app/backend/flags.py:355:def _to_tray(f: dict, code: str, judge_reason=None) -> None:
app/backend/flags.py:369:    detail = why.judge_detail(judge_reason) if judge_reason else ""
app/backend/trace.py:269:def _judge_reason_code(jd, call):
app/backend/trace.py:300:    rc = _judge_reason_code(jd, call)
app/backend/trace.py:301:    ev.update(judge_verdict=verdict, judge_reason_code=rc)
app/backend/trace.py:874:            ev.update(judge_verdict=verdict, judge_reason_code=jd.get("reason_code"))
app/backend/trace.py:960:                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:32.640Z

**tool call — Bash**
````
{
 "command": "sed -n 598,660p memory/contracts/api.md | cut -c1-900; grep -n \"def judge_detail\" -A40 app/backend/why.py | head -80"
}
````

### User / tool · 2026-11-03T04:34:32.742Z

**tool result**
````
## Check traces (D-042): per-item stepper, case stepper, judge summary
Three read-only GETs that feed the vertical steppers (pattern: <outside project> flow rail: each node has a status, label, detail and note, plus an overall progress count and a verdict). Everything is derived from data already stored (ladder, review status, `llm_calls`, `review_events`, case config); nothing is recomputed by a model. `404 not_found` for an unknown token or item.

**Visibility (same split as `/audit`, D-020/D-036).** Public/demo = **metadata only**. `ZLAYT_MODE=local` = **full**. Both modes return `"mode": "metadata" | "full"`. Metadata mode returns: model id, backend, prompt version and hash, call id, verdict, latency, closed reason codes and their fixed sentences, counts, the item's own excerpt spans and text (the case view already shows them), and the action and time of each human event. **Full mode adds, per step:** `evidence.response_raw` (the model's raw answer for an LLM step), and for the human step `evidence.events[].before/after` and `evidence.edited_text`. Prompt text (`system_text`/`user_text`) is **never** in a trace; use `/audit` in local mode. The frontend must not assume the full-only keys exist.

**Judge rationale is a closed reason code plus a fixed sentence (D-028).** The judge returns `verdict` + `reason_code` from a closed list, never prose, so `rationale` is the fixed sentence for that code (`why.judge_detail`), written by code. `reason_code` is read from `ladder.judge.reason_code`; for items stored before it was kept (amounts, edits, manual entries) it is read from the audited call's answer.

### Step (shared by all three endpoints)
```json
{ "id": "summary_tokens", "n": 5, "label": "Numbers and dates in the summary are in the quote",
  "kind": "code",                       // "code" | "llm" | "human"
  "status": "pass",                     // "pass" | "fail" | "skipped" | "pending"
  "why": "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.",
  "reason_code": null,                  // closed code when status is fail, or when a pass still explains a state (e.g. AMOUNT_RATE_NOT_TOTALED); else null
  "rule": "D-034",                      // decision or LLM_VS_CODE row behind the check, or null
  "blocks_export": false,               // true only for steps that stop this item reaching the letter right now (human pending, date unconfirmed)
  "evidence": { },                      // see below; keys are present only when they apply
  "next_action": null }                 // object when status is "fail" or "pending", else null
```
`status` meaning: `pass` the check ran and passed (or the human decided to accept); `fail` the check ran and found a problem (the item is then `needs_review` or `rejected`); `skipped` not run on purpose (a step before it already rejected the item, no judge applies to code-made items, the judge did not answer, or the human dismissed it) and `why`/`reason_code` say which; `pending` not done yet (the AI run has not reached this step, or the human has not decided).

`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `RERUN_JUDGE` (text "Run the second check again.", target `{item_id, judge}` or `{view: "judges"}`; the action is `POST /rejudge`), `SENTENCE_REMOVED` (narrative sentence left out of the draft), `CONFIRM_RERUN`. `text` is a fixed sentence written by code; `target` and `options` are optional.

`evidence` keys (all optional): `excerpt` `{record_id, start, end, text}` (offsets absolute into the case text); `spans[]` (same shape, for flags); `tokens[]` (summary tokens not in the quote); `values` (small object, for example `{"text": "$6,240", "value_cents": 624000, "kind": "charge", "classified_by": "code:amounts"}` or a gap's `{"from","to","days","threshold"}`); `date` `{record_id, date_raw, date_iso, date_status, candidates[]}`; `model` `{id, role, independent_of_generator}`; `prompt_version`; `prompt_sha256`; `call_id`; `backend`; `recorded_from`; `latency_ms`; `parsed_ok`; `judge_verdict` (ladder vocabulary: `supported|partially|unsupported|disagrees|unsure|unavailable`); `judge_reason_code` (the judge's own closed code, for example `NUMBER_MISMATCH`, or `NONE`); `rationale` (fixed sentence for that code); `action`, `at`, `events[]` `{action, at}` (human step); `response_raw`,

### GET /api/cases/{token}/items/{item_id}/trace
```json
{ "token": "k3Jf9x...", "item_id": "e4", "kind": "entry", "mode": "metadata",
  "state": "needs_review", "review_status": "pending",
  "state_reasons": [ {"code": "JUDGE_PARTIAL", "why": "A second AI check found the summary only partly supported by the quoted text.", "step_id": "judge_1"} ],
  "verdict": { "code": "needs_attention", "label": "Needs your attention", "blocks_export": true },
  "progress": { "done": 10, "total": 11, "label": "10 of 11 steps settled" },
  "next_action": { "code": "COMPARE_BY_HAND", "text": "...", "target": {"item_id": "e4"} },
  "steps": [
    { "id": "extracted", "n": 1, "label": "AI drafted a summary and picked a quote", "kind": "llm", "status": "pass",
      "why": "The AI read this record and proposed a one-line summary and a quote.", "reason_code": null, "rule": "row 4", "blocks_export": false,
      "evidence": { "model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null},
                    "prompt_version": "extract_v1", "prompt_sha256": "9f2c0a77", "call_id": "c18", "backend": "fixture",
                    "latency_ms": 5120, "parsed_ok": true, "excerpt": {"record_id": "r4", "start": 858, "end": 928, "text": "..."} }, "next_action": null },
    { "id": "judge_1", "n": 9, "label": "Second AI check: is the summary supported by the quote?", "kind": "llm", "status": "fail",
      "why": "A second AI check found the summary only partly supported by the quoted text. The summary leaves out a qualifier that the quote carries.",
      "reason_code": "JUDGE_PARTIAL", "rule": "row 4", "blocks_export": false,
      "evidence": { "model": {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true}, "prompt_version": "judge_faithfulness_v1",
                    "call_id": "c27", "judge_verdict": "partially", "judge_reason_code": "DROPS_QUALIFIER",
                    "rationale": "The summary leaves out a qualifier that the quote carries." },
      "next_action": { "code": "COMPARE_BY_HAND", "text": "..." } } ] }
```
**Steps by item kind, in order** (ids; a step that does not apply is omitted, not skipped, except where noted):
- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `summary_trimmed` (code, D-054, present only when code removed summary clauses the quote does not support: `why` lists each as "removed from the summary: not in the quote: '<clause>'"; `evidence.removed`, `evidence.original_summary`, `evidence.kept_summary`; the second AI check saw `kept_summary`), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION
- **amount:** `found_in_text` (code, `GROUNDING_AMOUNT_NOT_IN_TEXT`), `amount_class` (code; pass for a charge; pass with `reason_code` `AMOUNT_RATE_NOT_TOTALED`/`AMOUNT_ESTIMATE`/`AMOUNT_DAMAGES` for the classes that are never totaled; fail for `AMOUNT_UNCLEAR`), `injection_scan`, `judge_2` (llm; `skipped` for damages, which are not judged), `charge_flag` (code, D-059/T-159, only for a charge that carries a flag: pending until the named confirm, pass after, skipped when dismissed; see the D-059 paragraph in the case view), `total_inclusion` (code: pass when it is an accepted charge counted in the total, pending when a charge is undecided, skipped when it is not a charge or was dismissed), `human`.
- **flag, code-made (gap, accident-date or provider conflict):** `computed` (code, `evidence.values` has the dates and days), `spans_match` (code), `endpoints_confirmed` (code, `ENDPOINT_NOT_VERIFIED`), `judge_not_needed` (skipped: arithmetic over dates needs no judge), `human`.
- **flag, phrase list and/or AI (pre-existing, causation incl. credibility wording D-038/D-043, AI-proposed conflicts):** `proposed_by_phrase_list` (code; skipped with `LLM_ONLY` when only the AI found it), `proposed_by_ai` (llm; skipped with `LEXICON_ONLY` when only the phrase list found it), `agreement` (code: pass when both, fail with `LEXICON_ONLY`/`LLM_ONLY`), `credibility_wording` (code, only for category `credibility_language`: the sentence has a credibility term and is not a clean negation, D-043), `excerpt_verbatim` (code), `highlight` (code), `injection_scan` (code), `judge_4` (llm) or `judge_3` (llm, for a conflict the AI proposed); `skipped` when only the phrase list found the flag (`LEXICON_ONLY`), `human`.
- **flag, record warning:** `record_warning_check` (code; the category in `evidence.values.category`), `human`.
- **narrative sentence (`ns1`…, kept or removed):** `extracted` (llm), `cites_accepted_entry` (code, `NOT_AN_ACCEPTED_ENTRY`), `sentence_checks` (code: numbers/dates D-006, qualifiers D-022, no unquoted causation, severity or flag wording; failing codes are in `evidence.reasons`), `judge_1` (llm), `human` (the decision on the whole paragraph). A removed sentence has `status: "fail"` on the step that removed it and later steps `skipped`; `kind` is `narrative_sentence`; the item `verdict.code` is `removed`.

`verdict.code`: `accepted` (accepted or edited), `dismissed`, `rejected` (state rejected, kept out of the letter), `needs_attention` (any `fail` step on a live item), `ready_for_decision` (all machine steps pass or are skipped on purpose, human pending), `removed` (narrative sentence only), `waiting_for_run` (AI steps not run yet). `verdict.blocks_export` is true when the item is live and `review_status` is `pending` (it is what `/trace`'s export gate lists). `progress.done` counts steps that are not `pending`.

### GET /api/cases/{token}/trace
```json
{ "token": "k3Jf9x...", "mode": "metadata", "status": "ready",
  "verdict": { "code": "needs_attention", "label": "12 items still need your decision" },
  "progress": { "done": 8, "total": 10, "label": "8 of 10 steps settled" },
145:def judge_detail(code) -> str:
146-    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
147-    return _JUDGE_DETAIL.get(code, "")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:33.531Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/e2e/guided/conftest.py 2>/dev/null; ls tests/e2e/guided; grep -n \"def \\(server\\|base_url\\|page\\|case\\|fixture\\)\" tests/e2e/conftest.py | head -20; cat docs/RUNBOOK.md | head -40"
}
````

### User / tool · 2026-11-03T04:34:33.633Z

**tool result**
````
__init__.py
__pycache__
_helpers.py
test_golden_path.py
test_home.py
test_round2.py
test_round3.py
test_shell_smoke.py
test_step1.py
test_step2.py
test_step3.py
test_step4.py
test_t203.py
test_t205.py
test_t206.py
235:def base_url():
260:def page(pw):
# RUNBOOK (for Chris)

## URLs
| What | URL | Notes |
|---|---|---|
| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |

Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
We restored those and gave the board and app their own ports so nothing of yours was clobbered.

## Steer
- **Inbox:** Board → Inbox → type a note → Send. It lands in `board/inbox/` and the orchestrator acts on it next cycle.
- **Direct:** type into this Claude session (Remote Control / Desktop). Treated exactly like an inbox note.
- **Your items:** `submission/NEEDS_CHRIS.md` and the `needs_chris` column. Nothing there blocks the team.

## Stop
- Board → Inbox → **STOP** (type STOP to confirm) → creates `board/STOP`. The orchestrator finishes its current handoff and stops.
- Or on the Mac: `touch ~/zlayt-pm-project/board/STOP`.
- **Resume after STOP:** from the phone, type into this Claude session (Remote Control): "Delete board/STOP and continue the loop." On the Mac: `rm ~/zlayt-pm-project/board/STOP`, then continue the session.

## Restart (after a crash, reboot, or closing the session)
1. `cd ~/zlayt-pm-project`
2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
3. Session — either:
   - Desktop app: reopen this session from the sidebar (it keeps bypass-permissions mode), or
   - Terminal: `claude --continue --dangerously-skip-permissions --remote-control` (without the first flag the run stalls on permission prompts nobody answers; the second lets you steer and resume from your phone).
4. Say:
   > Re-read CLAUDE.md, memory/STATE.md and `python3 tools/board.py status`. Re-spawn the worker agents (general-purpose subagents whose first step is `python3 tools/agent_prompt.py <role>` unless native agent types are available), recreate the heartbeat cron (text in memory/STATE.md), continue the loop.
5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.

## Useful commands
```
python3 tools/board.py status          # where are we
python3 tools/board.py list --status in_review
tail -f board/activity.jsonl           # raw event log
.venv/bin/python -m pytest tools/tests -q   # harness tests
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:35.251Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/e2e/guided/_helpers.py; sed -n 1,60p tests/e2e/guided/test_t206.py; sed -n 200,300p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-03T04:34:35.339Z

**tool result**
````
"""Shared helpers for the guided specs of Builder A (home, step 1, step 4). T-181 (D-068). Not a test module."""
import json
import os
import re
import time
import uuid
import tests.e2e.conftest as C

SHOTS = os.path.join(C.ROOT, "artifacts", "screenshots", "guided")


def uid():
    return uuid.uuid4().hex[:6]


def api(method, path, body=None):
    return C.api(method, path, body)


def make_case(title, run=True, decide=False, sample=True):
    """A sample case over the API: ingested, or drafted (ready), or drafted with every item accepted."""
    st, c = api("POST", "/api/cases", {"sample": True, "title": title}); assert st == 201, c
    tok = c["token"]
    if run:
        assert api("POST", f"/api/cases/{tok}/run", {"confirm_rerun": False})[0] == 202
        for _ in range(240):
            s = api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(.5)
        assert s["status"] == "ready", s
    if decide:
        decide_all(tok)
    return tok


def decide_all(tok, action="accept"):
    """Step 2 and 3 are another builder's: answer every item over the API (accept)."""
    c = api("GET", f"/api/cases/{tok}")[1]
    for i in c["entries"] + c["undated_entries"] + c["flags"] + c["amounts"]:
        st, r = api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": action})
        assert st == 200, (i["id"], st, r)


def golden_letter():
    txt = open(os.path.join(C.SAMPLE_PATH, "sample.export.expected.txt")).read()
    return txt.split("=== LETTER_TEXT (block 1: paste into letter) ===\n")[1].split("=== INTERNAL_NOTES_TEXT")[0].rstrip("\n")


def golden_notes():
    txt = open(os.path.join(C.SAMPLE_PATH, "sample.export.expected.txt")).read()
    notes = txt.split("=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\n")[1].rstrip("\n")
    from app.backend import export      # D-069: the golden predates the prepared disclosure line the curated demo now prints
    return notes.replace(export.AI_LINE.split("{n}")[0], export.AI_LINE_PREPARED.split("{n}")[0])


def browser(pw, w, h, scheme="light", **kw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, permissions=["clipboard-read", "clipboard-write"], accept_downloads=True, **kw)
    return b, ctx.new_page()


def shot(page, name, w):
    os.makedirs(SHOTS, exist_ok=True)
    page.screenshot(path=os.path.join(SHOTS, f"{name}-{w}.png"))


def in_view(page, loc):
    """True when the element's whole box is inside the viewport with the page scrolled to the top (nothing to scroll to reach it)."""
    page.evaluate("window.scrollTo(0, 0)")
    b = loc.bounding_box(); vh = page.viewport_size["height"]; vw = page.viewport_size["width"]
    return bool(b) and b["y"] >= 0 and b["y"] + b["height"] <= vh and b["x"] >= 0 and b["x"] + b["width"] <= vw


def no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")


def go(page, path="/"):
    page.goto(C.SERVER + path)
"""T-206 (D-071 follow-up to T-205, paralegal review minors): a Step 3 card shows a bare date only when it is a certain service date. An uncounted ledger line (lib11 a2-a4) and every other amount
taken from a bill document (the rest of the ledger) names its record's date "statement dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
the words of the buttons the card has. Real browser, fixture backend, real API; the doubtful-date note is the backend's own sentence put into the case response (the fixture set has no such bill)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.guided.test_shell_smoke import watch, go
from tests.e2e.guided.test_step2 import make, phone, case, item, open_item   # noqa: F401  (make and phone are fixtures)
from tests.e2e.guided.test_t205 import LIB10, LIB11, SD
import tests.e2e.conftest as C

BARE = re.compile(r"(?<!statement dated )(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}")


def texts(page):
    return {k: page.get_by_test_id(k).inner_text() for k in ("card-line", "line-sub", "src-head")}


def test_lib11_uncounted_ledger_lines_never_show_a_bare_statement_date(page, make):
    seen = watch(page)
    tok = make(LIB11); amounts = {a["id"]: a for a in case(tok)["amounts"]}
    uncounted = [i for i, a in amounts.items() if a["kind"] != "charge"]
    assert {"a2", "a3", "a4"} <= set(uncounted) and amounts["a2"]["countable"] and amounts["a2"]["service_date"] is None
    for iid in uncounted:         # the three countable lines and the four never counted: all of them are the ledger
        open_item(page, tok, iid, step="bills")
        t = texts(page)
        assert "statement dated June 15, 2026" in t["src-head"] and "statement dated June 15, 2026" in t["line-sub"], (iid, t)
        for k, v in t.items():
            assert not BARE.search(v), (iid, k, v)
        assert page.get_by_test_id("confirm-note").count() == 0
    # the ED charge's source label names only the provider (D-073): no document type, so its header date is not lent and the blank prints with the statement date named
    open_item(page, tok, "a1", step="bills")
    assert page.get_by_test_id("service-date-text").inner_text() == "date of service [__________] (record dated March 18, 2026)"          # T-202 r6 rule 4: an ED record is a record, not a statement (src-head below still says statement: frontend card)
    assert "statement dated March 18, 2026" in page.get_by_test_id("src-head").inner_text()
    assert seen == [], seen


def test_lib11_a_counted_ledger_line_keeps_the_label_and_matches_the_letter(page, make):
    seen = watch(page)
    tok = make(LIB11); a = item(tok, "a2")
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    open_item(page, tok, "a2", step="bills")
    sd = item(tok, "a2")["service_date"]
    assert sd["state"] == "not_stated" and "statement dated June 15, 2026" in sd["text"]
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen


REASONS = [("ambiguous_numeric", "04/05/2026"), ("two_digit_year", "04/05/26"), ("no_year", "April 5"), ("invalid", "02/30/2026"), ("several_dates", "04/06/2026 and 04/20/2026"),
           ("implausible", "09/14/2026"), ("no_date", ""), ("non_service_date", "03/04/1980")]
NEXT = "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank"


def inject(page, tok, reason, raw):
    """Put the backend's own not-certain service_date (its sentences, SD.confirm_note) into a2's case response; the fixture set has no such bill."""
    a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason=reason, text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note(reason, raw))
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

def tray_entry_for_record(tok, record_id):
    """T-173 (T-168): put one record's entry into the could-not-verify tray the way the pipeline does when the extract step has no answer for it (FIXTURE_MISS). T-168 recorded lib01
    record 3's extract answer, so no library case has an entry tray item any more; the specs that need one overwrite that entry's stored row (needs_db, like the T-136 store writes)
    with the pipeline's own placeholder: generator.failure_entry(record, group, 'FIXTURE_MISS') (no summary, no quote, ladder.failure set, no generator or judge), written through
    pipeline._row, the same row builder the pipeline persists with, and the ladder's backend name kept. The tray is then read from the real backend view and DOM. Returns the item id."""
    import time
    path = needs_db()
    c = api("GET", f"/api/cases/{tok}")[1]
    e = next((x for x in c["entries"] if x["record_ids"] == [record_id]), None)
    if e is None:
        pytest.fail(f"tray_entry_for_record: case {tok} has no entry for record {record_id}; entries: {[x['record_ids'] for x in c['entries']]}")
    from app.db import db as DB
    from app.backend import generator, pipeline as PL, store
    conn = DB.connect(path)
    try:
        case = DB.get_case(conn, tok)
        recs = store.load_records(conn, tok, case["raw_text"])
        rec = next(r for r in recs if f"r{r['n']}" == record_id)
        f = generator.failure_entry(rec, [rec["n"]], "FIXTURE_MISS")
        assert f["id"] == e["id"], (f["id"], e["id"])
        old = DB.get_item(conn, e["id"], tok)
        f["ladder"]["backend"] = (old.get("ladder") or {}).get("backend")      # the pipeline stamps P.backend_name() on every item it stores
        DB.update_item(conn, e["id"], now=time.time(), case=tok, **PL._row("entry", PL._clean(f)))
    finally:
        conn.close()
    t = next((x for x in api("GET", f"/api/cases/{tok}")[1]["tray"] if x["id"] == e["id"]), None)       # what the paralegal gets: a placeholder, no attempt to show
    assert t and t["kind"] == "entry" and t["reasons"] == ["FIXTURE_MISS"] and t["attempt"] == {"summary": None, "excerpt": None}, t
    return e["id"]

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
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."

    def __init__(self, page, token, ids):
        self.page, self.token, self.ids = page, token, list(ids)
        self.base = {i: self._summary(i) for i in self.ids}
        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/export$", self._export)):
            page.route(self._re.compile(pat), fn)

    def _summary(self, i):
        c = api("GET", f"/api/cases/{self.token}")[1]
        e = next((x for x in c["entries"] + c["undated_entries"] if x["id"] == i), None)
        return e and (e["summary"], e["review_status"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:37.490Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/frontend/feedback_verify_from_archive.md; curl -s localhost:7860/api/health | head -c 600; sed -n 1,60p tests/e2e/conftest.py | grep -n \"SERVER\\|BASE\\|7860\\|E2E_\" "
}
````

### User / tool · 2026-11-03T04:34:37.606Z

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
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":false,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:41.693Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json,time,urllib.request as u\ndef api(m,p,b=None):\n    r=u.Request(\"http://localhost:7860\"+p,data=json.dumps(b).encode() if b is not None else None,method=m,headers={\"Content-Type\":\"application/json\"})\n    return json.load(u.urlopen(r))\nc=api(\"POST\",\"/api/cases\",{\"sample\":True,\"title\":\"scratch t211\"});t=c[\"token\"];print(t)\napi(\"POST\",f\"/api/cases/{t}/run\",{\"confirm_rerun\":False})\nwhile api(\"GET\",f\"/api/cases/{t}/status\")[\"status\"] not in(\"ready\",\"failed\"):time.sleep(.5)\nc=api(\"GET\",f\"/api/cases/{t}\")\ne=c[\"entries\"][0]\nprint(json.dumps({k:e[k] for k in e if k not in(\"excerpt\",)},indent=1)[:3500])\na=c[\"amounts\"][0];print(json.dumps(a,indent=1)[:2500])\nf=c[\"flags\"][0];print(json.dumps({k:f[k] for k in f if k in(\"ladder\",\"prepared\",\"why\",\"state\",\"reasons\")},indent=1)[:2500])\njson.dump(c,open(\"/tmp/t211case.json\",\"w\"))\nprint(t)\nEOF"
}
````

### User / tool · 2026-11-03T04:34:42.447Z

**tool result**
````
EXNPq1Q1Uese0eB-92gyCg
{
 "id": "e1",
 "state": "verified",
 "reasons": [],
 "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
 "review_status": "pending",
 "version": 1793680481.94307,
 "edited": null,
 "ladder": {
  "backend": "fixture",
  "code_checks": {
   "date_provider_from_header": true,
   "excerpt_verbatim": true,
   "excerpt_whole_sentence": true,
   "highlight_found": true,
   "qualifier_carried": true,
   "summary_tokens_not_in_excerpt": []
  },
  "generator": {
   "call_id": "ca13d2d41d586",
   "model": "hand-checked (qa)",
   "output": {
    "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.",
    "summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER."
   },
   "prompt_version": "extract_v1",
   "prepared": true
  },
  "human": {
   "action": null,
   "edited_text": null,
   "at": null
  },
  "item_id": "e1",
  "judge": {
   "call_id": "cf910776be0df",
   "model": "claude-haiku-5-5",
   "prompt_version": "judge_faithfulness_v1",
   "reason_code": "NONE",
   "verdict": "supported"
  },
  "state": "verified"
 },
 "rerun_note": null,
 "rerun_available": false,
 "seq": 1,
 "record_ids": [
  "r1"
 ],
 "date": "2026-01-09",
 "date_status": "parsed",
 "provider": "Austin EMS run report",
 "summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.",
 "ai_drafted": true,
 "entered_by_reviewer": false,
 "entered_by": null,
 "source_kind": "record",
 "excerpt_start": 180,
 "excerpt_end": 312,
 "duplicate_note": null,
 "translation": null,
 "edit_to_check": false,
 "prepared": true,
 "second_check_pending": false
}
{
 "id": "a1",
 "state": "verified",
 "reasons": [],
 "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
 "review_status": "pending",
 "version": 1793680481.94307,
 "edited": null,
 "ladder": {
  "backend": "fixture",
  "code_checks": {
   "amount_in_text": true,
   "classified_by": "code:amounts"
  },
  "generator": null,
  "human": {
   "action": null,
   "edited_text": null,
   "at": null
  },
  "item_id": "a1",
  "judge": {
   "call_id": "c03e8bbf2d487",
   "model": "claude-haiku-5-5",
   "prompt_version": "judge_amount_class_v1",
   "reason_code": "NONE",
   "verdict": "agree"
  },
  "state": "verified"
 },
 "rerun_note": null,
 "rerun_available": false,
 "flag": null,
 "confirm_required": false,
 "record_ids": [
  "r2"
 ],
 "entry_id": "e2",
 "text": "$6,240",
 "value_cents": 624000,
 "kind": "charge",
 "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.",
 "excerpt_start": 545,
 "excerpt_end": 551,
 "duplicate_note": null,
 "accept_effect": "letter_total",
 "judge_required_for_export": true,
 "not_counted_reason": null,
 "countable": false,
 "service_date": {
  "state": "stated",
  "date_iso": "2026-01-09",
  "end_iso": null,
  "text": "January 9, 2026",
  "statement_date_iso": "2026-01-09",
  "reason": null,
  "confirm_note": null
 },
 "count_confirm": null,
 "prepared": false,
 "second_check_pending": false
}
{
 "state": "verified",
 "reasons": [],
 "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
 "ladder": {
  "backend": "fixture",
  "code_checks": {
   "computed_by": "code",
   "spans_match_input": true
  },
  "generator": null,
  "human": {
   "action": null,
   "edited_text": null,
   "at": null
  },
  "item_id": "f_gap_r6_r7",
  "judge": null,
  "state": "verified"
 },
 "prepared": false
}
EXNPq1Q1Uese0eB-92gyCg
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:47.306Z

**tool call — Bash**
````
{
 "command": "T=EXNPq1Q1Uese0eB-92gyCg; for i in e1 a1 f_gap_r6_r7; do curl -s localhost:7860/api/cases/$T/items/$i/trace | .venv/bin/python -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint(d['item_id'],d['kind'],d['verdict'],d.get('state_reasons'))\nfor s in d['steps']: print(' ',s['id'],s['kind'],s['status'],'|',s['label'],'|',s['why'][:140],'|',s.get('reason_code'), {k:v for k,v in s.get('evidence',{}).items() if k in('judge_verdict','judge_reason_code','rationale','model')})\n\"; done; grep -n \"def _JUDGE_DETAIL\\|_JUDGE_DETAIL = \" -A30 app/backend/why.py | head -50"
}
````

### User / tool · 2026-11-03T04:34:47.551Z

**tool result**
````
e1 entry {'code': 'ready_for_decision', 'label': 'Ready for your decision', 'blocks_export': True} []
  extracted llm pass | Prepared answer | Prepared answer (hand-checked by the team for the demo) | None {'model': {'id': 'hand-checked (qa)', 'role': 'generator', 'independent_of_generator': None, 'prepared': True}}
  excerpt_verbatim code pass | Quote is word for word in the record | The quote was found in the record, character for character. | None {}
  excerpt_whole_sentence code pass | Quote is made of whole sentences | The quote starts and ends on whole sentences. | None {}
  excerpt_hedge code pass | Quote keeps the hedge sentence that qualifies it | No hedge sentence that qualifies the quote is left out. | None {}
  summary_tokens code pass | Numbers and dates in the summary are in the quote | Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote. | None {}
  summary_qualifier code pass | Summary keeps the quote's qualifiers | Every hedge, attribution, negation, side and approximation in the quote is in the summary. | None {}
  highlight code pass | Quote can be highlighted in the record | The quote's position in the record was found, so it can be highlighted. | None {}
  date_confirmed code pass | Date of service is confirmed | The date comes from the record's own header and is parsed or confirmed. | None {}
  injection_scan code pass | Record has no instruction-like text | The record has no instruction-like text. | None {}
  judge_1 llm pass | Second check: is the summary supported by the quote? | The second check found every statement in the summary in the quote. | None {'model': {'id': 'claude-haiku-5-5', 'role': 'judge', 'independent_of_generator': True, 'prepared': False}, 'judge_verdict': 'supported', 'judge_reason_code': 'NONE', 'rationale': 'The second check found every statement in the summary in the quote.'}
  human human pending | Your decision | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | PENDING_DECISION {}
a1 amount {'code': 'ready_for_decision', 'label': 'Ready for your decision', 'blocks_export': True} []
  found_in_text code pass | Dollar figure is in the record text | Code found this figure in the record by pattern; it is not a claim from any answer. | None {}
  amount_class code pass | Rule says what the figure is | A billing phrase in the record labels this figure a charge, so it counts toward the total once you accept it. | None {}
  injection_scan code pass | Record has no instruction-like text | The record has no instruction-like text. | None {}
  judge_2 llm pass | Second check: is this figure a charge, rate or estimate? | The second check agreed with the rule's reading of this figure. | None {'model': {'id': 'claude-haiku-5-5', 'role': 'judge', 'independent_of_generator': True, 'prepared': False}, 'judge_verdict': 'supported', 'judge_reason_code': 'NONE', 'rationale': "The second check agreed with the rule's reading of this figure."}
  total_inclusion code pending | Counted in the total | Detected but not in the accepted total until you accept it. | PENDING_DECISION {}
  human human pending | Your decision | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | PENDING_DECISION {}
f_gap_r6_r7 flag {'code': 'ready_for_decision', 'label': 'Ready for your decision', 'blocks_export': True} []
  computed code pass | Dates compared by code | Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient). | None {}
  spans_match code pass | Cited text matches the record | Every cited date line is in the record, character for character. | None {}
  endpoints_confirmed code pass | Dates at both ends are confirmed | Both dates are parsed or confirmed. | None {}
  injection_scan code pass | Record has no instruction-like text | The record has no instruction-like text. | None {}
  judge_not_needed llm skipped | Second check | Not needed: this is arithmetic over dates in the record, which code does exactly. | None {}
  human human pending | Your decision | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | PENDING_DECISION {}
121:_JUDGE_DETAIL = {
122-    "ADDS_DIAGNOSIS": "The summary adds a diagnosis the quote does not state.",
123-    "ADDS_SEVERITY": "The summary adds a severity the quote does not state.",
124-    "ADDS_CAUSATION": "The summary adds a cause the quote does not state.",
125-    "DROPS_QUALIFIER": "The summary leaves out a qualifier that the quote carries.",
126-    "NUMBER_MISMATCH": "A number in the summary does not match the quote.",
127-    "OTHER_UNSUPPORTED": "Part of the summary is not supported by the quote.",
128-    "SHOULD_BE_CHARGE": "The second check reads this figure as a billed charge.",
129-    "SHOULD_BE_RATE": "The second check reads this figure as a rate.",
130-    "SHOULD_BE_ESTIMATE": "The second check reads this figure as an estimate.",
131-    "SHOULD_BE_DAMAGES": "The second check reads this figure as a non-bill amount.",
132-    "SHOULD_BE_UNCLEAR": "The second check could not read this figure with confidence.",
133-    "TEXT_AMBIGUOUS": "The text does not settle the question.",
134-    "PLAN_VS_ACTUAL": "The second check reads the quotes as a plan and what followed.",
135-    "FACT_MISMATCH": "The second check reads the quotes as stating different facts.",
136-    "DIFFERENT_VISITS": "The second check reads the quotes as different visits that can both be true.",
137-    "CAN_BOTH_BE_TRUE": "The second check reads both quotes as possibly true together.",
138-    "WRONG_TYPE": "The second check does not think this flag type fits the quote.",
139-    "WRONG_CATEGORY": "The second check does not think this flag category fits the quote.",
140-    "NEGATED": "The second check reads the quote as negating the condition.",
141-    "NOT_SUPPORTED_BY_QUOTE": "The second check does not find this flag supported by the quote.",
142-}
143-
144-
145-def judge_detail(code) -> str:
146-    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
147-    return _JUDGE_DETAIL.get(code, "")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:57.541Z

**tool call — Bash**
````
{
 "command": "grep -n \"trace\" app/frontend/guided/*.js | cut -c1-220; sed -n 1,145p app/frontend/guided/core.js"
}
````

### User / tool · 2026-11-03T04:34:57.632Z

**tool result**
````
app/frontend/guided/core.js:79:    trace: (token, s) => call("GET", t(token) + "/trace", null, s),
app/frontend/guided/step4.js:24:      /* the check trace first: its export gate says "ready" or lists the blockers without a refused request (a 422 would show as a console error); the export is read only when it will be 
app/frontend/guided/step4.js:25:      try { const tr = await G.api.trace(token, sig), gate = (tr.steps || []).find((x) => x.id === "export_gate"); if (gate && !gate.ready && Array.isArray(gate.blockers) && gate.blockers.
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
  /* The server's health, once (shared with the shell's own request). `local_mode` (T-181 r2) says whether the list of cases and the test-case library exist: when it is false the page never asks for them,
     so a first paint makes no request that is going to fail. An older server without the field is asked (and a 404 there is expected). */
  G.healthNow = async function (signal) {
    if (G.store.health) return G.store.health;
    try { const hl = await (G.store.healthP || G.api.health(signal)); G.store.health = G.store.health || hl; return hl || {}; }
    catch (e) { if (e && e.name === "AbortError") throw e; return {}; }
  };
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
        G.h("a", { class: "btn lg" + (retry ? "" : " primary"), href: "/", "data-testid": "link-home" }, "Back to your cases")));
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:34:57.862Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/guided/styles.css | sed -n 1,200p"
}
````

### User / tool · 2026-11-03T04:34:57.945Z

**tool result**
````
/* Guided UI styles (T-181, D-068). Base = the T-180 mockup stylesheet (artifacts/mockups/guided/guided.css), copied so the app does not depend on the mockup folder.
   Shell-owned: tokens, banner, header, step bar, footer, frame/page layouts, buttons, cards, action bar and the shared single-panel classes below.
   Step builders add rules ONLY in their own file (home.css, step1.css ... step4.css, review.css); do not edit this one except to fix the shell. Spec: docs/GUIDED_UI_SPEC.md */
:root {
  color-scheme: light;
  --page: #F4F6F9; --panel: #FFFFFF; --sunken: #EEF1F5; --paper: #FFFFFF;
  --border: #DCE1E8; --border-strong: #6F7B8B;
  --text: #14181F; --muted: #4A5565; --subtle: #5B6676;
  --accent: #0B57D0; --accent-hover: #0948A8; --on-accent: #FFFFFF; --accent-soft: #E8F0FE;
  --ok: #13613A; --ok-bg: #E3F3E9; --ok-strong: #1E7D4C;
  --warn: #6B4400; --warn-bg: #FFF3D1; --warn-edge: #E2B44C;
  --bad: #8C1D1D; --bad-bg: #FCE9E8;
  --mark: #FFE27A; --on-mark: #14181F;
  --banner-bg: #FFF1C2; --banner-text: #4D3500;
  --shadow: 0 1px 2px rgb(16 24 40 / .06), 0 4px 12px rgb(16 24 40 / .06);
  --shadow-bar: 0 -4px 16px rgb(16 24 40 / .08);
  --font: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
  --r-card: 14px; --r-btn: 12px;
  --gutter: 32px;
  --banner-h: 32px; --header-h: 64px; --steps-h: 76px; --title-h: 104px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  color-scheme: dark;
  --page: #0F1216; --panel: #171B21; --sunken: #1E242C; --paper: #1B2027;
  --border: #2C343F; --border-strong: #7A8696;
  --text: #E8EBEF; --muted: #B4BDC9; --subtle: #9AA5B4;
  --accent: #8AB4FF; --accent-hover: #A8C7FF; --on-accent: #0E1116; --accent-soft: #1A2A47;
  --ok: #7BD6A0; --ok-bg: #13301F; --ok-strong: #7BD6A0;
  --warn: #F2C265; --warn-bg: #36280B; --warn-edge: #8A6A1F;
  --bad: #FF9A92; --bad-bg: #3D1A19;
  --mark: #6B5800; --on-mark: #FFF7D6;
  --banner-bg: #3A2D0B; --banner-text: #F6DE9B;
  --shadow: 0 1px 2px rgb(0 0 0 / .4); --shadow-bar: 0 -4px 16px rgb(0 0 0 / .4);
} }
:root[data-theme="dark"] {
  color-scheme: dark;
  --page: #0F1216; --panel: #171B21; --sunken: #1E242C; --paper: #1B2027;
  --border: #2C343F; --border-strong: #7A8696;
  --text: #E8EBEF; --muted: #B4BDC9; --subtle: #9AA5B4;
  --accent: #8AB4FF; --accent-hover: #A8C7FF; --on-accent: #0E1116; --accent-soft: #1A2A47;
  --ok: #7BD6A0; --ok-bg: #13301F; --ok-strong: #7BD6A0;
  --warn: #F2C265; --warn-bg: #36280B; --warn-edge: #8A6A1F;
  --bad: #FF9A92; --bad-bg: #3D1A19;
  --mark: #6B5800; --on-mark: #FFF7D6;
  --banner-bg: #3A2D0B; --banner-text: #F6DE9B;
  --shadow: 0 1px 2px rgb(0 0 0 / .4); --shadow-bar: 0 -4px 16px rgb(0 0 0 / .4);
}

* { box-sizing: border-box; }
[hidden] { display: none !important; }
html { font-size: 16px; scrollbar-gutter: stable; }
body { margin: 0; background: var(--page); color: var(--text); font: 400 1.125rem/1.75rem var(--font); -webkit-font-smoothing: antialiased; }
a { color: var(--accent); }
h1, h2, h3, p { margin: 0; }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; border-radius: 6px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.num { font-variant-numeric: tabular-nums; }

/* ---------- banner, header, footer ---------- */
.banner { height: var(--banner-h); display: flex; align-items: center; justify-content: center; gap: 8px; background: var(--banner-bg); color: var(--banner-text);
  font-size: .9375rem; font-weight: 600; text-align: center; padding: 0 16px; }
.banner .b-demo { display: none; font-weight: 400; }
.header { height: var(--header-h); display: flex; align-items: center; gap: 16px; padding: 0 var(--gutter); background: var(--panel); border-bottom: 1px solid var(--border); }
.brand { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.125rem; color: var(--text); text-decoration: none; white-space: nowrap; }
.brand-mark { width: 30px; height: 30px; border-radius: 9px; background: var(--accent); color: var(--on-accent); display: grid; place-items: center; font-size: .9rem; font-weight: 800; }
.back-cases { display: inline-flex; align-items: center; gap: 6px; height: 44px; padding: 0 14px 0 10px; border-radius: 10px; border: 1px solid var(--border); color: var(--text);
  text-decoration: none; font-weight: 600; font-size: 1rem; white-space: nowrap; background: var(--panel); }
.back-cases:hover { background: var(--sunken); }
.back-cases .short { display: none; }
.case-title { font-size: 1.25rem; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; }
.case-sub { color: var(--muted); font-size: .9375rem; white-space: nowrap; }
.header .spacer { flex: 1; }
.demo-pill { display: inline-flex; align-items: center; gap: 8px; height: 34px; padding: 0 14px; border-radius: 999px; background: var(--accent-soft); color: var(--text);
  font-size: .9375rem; font-weight: 600; white-space: nowrap; }
.demo-pill::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
.theme-btn { height: 44px; min-width: 124px; border-radius: 10px; border: 1px solid var(--border-strong); background: var(--panel); color: var(--text); font: 600 .9375rem var(--font); cursor: pointer; }
.theme-btn:hover { background: var(--sunken); }
.footer { padding: 14px var(--gutter) 20px; color: var(--subtle); font-size: .9375rem; display: flex; gap: 16px; flex-wrap: wrap; }
.footer a { color: var(--subtle); }

/* ---------- step bar ---------- */
.steps { height: var(--steps-h); background: var(--panel); border-bottom: 1px solid var(--border); padding: 0 var(--gutter); }
.steps ol { list-style: none; margin: 0 auto; padding: 0; height: 100%; display: grid; grid-template-columns: repeat(4, 1fr); max-width: 1376px; }
.steps li { position: relative; display: flex; }
.steps li + li::before { content: ""; position: absolute; left: -22px; width: 30px; top: 50%; border-top: 2px solid var(--border); }
.step { flex: 1; display: flex; align-items: center; gap: 12px; padding: 0 20px 0 0; text-decoration: none; color: var(--text); position: relative; min-width: 0; }
.step::after { content: ""; position: absolute; left: 0; right: 20px; bottom: 0; height: 4px; border-radius: 4px 4px 0 0; background: transparent; }
.step .dot { flex: none; width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font-weight: 700; font-size: 1rem; border: 2px solid var(--border-strong); color: var(--muted); background: var(--panel); }
.step .st-text { display: flex; flex-direction: column; min-width: 0; }
.step .st-label { font-weight: 600; font-size: 1.0625rem; line-height: 1.375rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.step .st-label .short { display: none; }
.step .st-status { font-size: .9375rem; line-height: 1.25rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.step.done .dot { background: var(--ok-strong); border-color: var(--ok-strong); color: #fff; }
.step.done .st-status { color: var(--ok); font-weight: 600; }
.step.current .dot { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }
.step.current .st-label { font-weight: 800; }
.step.current .st-status { color: var(--text); font-weight: 600; }
.step.current::after { background: var(--accent); }
.step.attn .dot { background: var(--warn-bg); border-color: var(--warn-edge); color: var(--warn); }
.step.attn .st-status { color: var(--warn); font-weight: 600; }
.step.locked { opacity: .6; cursor: default; }
a.step:not(.locked):hover .st-label { text-decoration: underline; }

/* ---------- review frame ---------- */
html:has(> body.frame) { overflow: hidden; scrollbar-gutter: auto; }
body.frame { height: 100vh; height: 100dvh; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1fr); grid-template-rows: var(--banner-h) var(--header-h) var(--steps-h) var(--title-h) minmax(0, 1fr) auto; }
.titlebar { display: flex; align-items: center; gap: 24px; padding: 0 var(--gutter) 8px; max-width: 1440px; width: 100%; margin: 0 auto; }
.titlebar .t-main { flex: 1; min-width: 0; }
.eyebrow { font-size: .9375rem; font-weight: 600; color: var(--accent); letter-spacing: .01em; }
.titlebar h1 { font-size: 1.75rem; line-height: 2.25rem; font-weight: 750; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.titlebar .t-ai { margin-top: 2px; font-size: .9375rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.count-box { width: 300px; flex: none; }
.count-line { display: flex; justify-content: space-between; font-size: 1rem; font-weight: 600; }
.count-line .of { color: var(--muted); font-weight: 400; }
.bar { height: 10px; border-radius: 999px; background: var(--sunken); overflow: hidden; margin-top: 8px; border: 1px solid var(--border); }
.bar > i { display: block; height: 100%; background: var(--accent); border-radius: 999px; }
.total-chip { flex: none; width: 250px; padding: 10px 16px; border-radius: 12px; background: var(--panel); border: 1px solid var(--border); box-shadow: var(--shadow); }
.total-chip .tc-l { font-size: .875rem; color: var(--muted); }
.total-chip .tc-v { font-size: 1.375rem; font-weight: 750; }

.work { min-height: 0; padding: 0 var(--gutter) 20px; max-width: 1440px; width: 100%; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.card { background: var(--panel); border: 1px solid var(--border); border-radius: var(--r-card); box-shadow: var(--shadow); display: flex; flex-direction: column; min-height: 0; overflow: hidden; }
.card-h { flex: none; padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; min-height: 64px; }
.card-h .ch-title { font-weight: 700; font-size: 1.0625rem; }
.card-h .ch-sub { color: var(--muted); font-size: 1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-b { position: relative; flex: 1; min-height: 0; overflow: auto; padding: 20px 24px; }
.card-f { flex: none; min-height: 112px; padding: 16px 24px; border-top: 1px solid var(--border); background: var(--sunken); font-size: 1rem; line-height: 1.5rem; color: var(--muted); }
.card-f.attn { background: var(--warn-bg); color: var(--text); border-top-color: var(--warn-edge); }
.card-f.ok { background: var(--ok-bg); color: var(--text); }
.card-f.bad { background: var(--bad-bg); color: var(--text); }
.card-f strong { color: var(--text); }
.label-cap { font-size: .875rem; font-weight: 700; color: var(--muted); text-transform: none; letter-spacing: .01em; }

.rec { font-size: 1.125rem; line-height: 1.8rem; white-space: pre-wrap; }
.rec + .rec-h { margin-top: 24px; padding-top: 20px; border-top: 1px dashed var(--border); }
.rec-h { font-weight: 700; font-size: 1rem; color: var(--muted); margin-bottom: 8px; }
.rec .meta { color: var(--muted); }
mark { background: var(--mark); color: var(--on-mark); border-radius: 4px; padding: 1px 2px; box-shadow: 0 0 0 2px var(--mark); }
.sent { border-radius: 6px; padding: 1px 2px; box-shadow: inset 0 0 0 2px var(--border-strong); cursor: pointer; }
.sent.on { background: var(--mark); color: var(--on-mark); box-shadow: inset 0 0 0 2px var(--warn-edge); }
.also { margin-top: 20px; padding: 14px 16px; border-radius: 10px; background: var(--sunken); font-size: 1rem; line-height: 1.5rem; color: var(--muted); }
.also q { color: var(--text); }

.tag { display: inline-flex; align-items: center; height: 28px; padding: 0 12px; border-radius: 999px; font-size: .875rem; font-weight: 700; white-space: nowrap; }
.tag.prep { background: var(--accent-soft); color: var(--text); }
.tag.ai { background: var(--accent-soft); color: var(--text); }
.tag.you { background: var(--ok-bg); color: var(--ok); }
.tag.warn { background: var(--warn-bg); color: var(--warn); border: 1px solid var(--warn-edge); }
.tag.ok { background: var(--ok-bg); color: var(--ok); }
.tag.never { background: var(--sunken); color: var(--muted); border: 1px solid var(--border); }
.tag.bad { background: var(--bad-bg); color: var(--bad); }
.line-when { font-weight: 700; font-size: 1.0625rem; margin-bottom: 10px; }
.line-text { font-size: 1.375rem; line-height: 2rem; font-weight: 500; }
.money { font-size: 2.5rem; line-height: 3rem; font-weight: 750; font-variant-numeric: tabular-nums; }
.warn-title { font-size: 1.25rem; line-height: 1.75rem; font-weight: 700; margin-bottom: 10px; }
.explain { font-size: 1.0625rem; line-height: 1.7rem; }
.muted { color: var(--muted); }
textarea.edit { width: 100%; height: 100%; min-height: 160px; resize: none; font: 500 1.375rem/2rem var(--font); color: var(--text); background: var(--panel); border: 2px solid var(--accent);
  border-radius: 10px; padding: 12px 14px; }
.check { display: flex; gap: 14px; align-items: flex-start; cursor: pointer; font-weight: 600; color: var(--text); font-size: 1.0625rem; line-height: 1.6rem; margin-top: 10px; }
.check input { flex: none; width: 28px; height: 28px; margin: 0; accent-color: var(--accent); cursor: pointer; }

/* ---------- action bar ---------- */
.actions { background: var(--panel); border-top: 1px solid var(--border); box-shadow: var(--shadow-bar); }
.actions-in { max-width: 1440px; margin: 0 auto; padding: 14px var(--gutter) 12px; display: grid; grid-template-columns: auto 1fr; grid-template-areas: "q q" "big small" "status status"; column-gap: 24px; row-gap: 10px; align-items: center; }
.question { grid-area: q; font-size: 1.25rem; line-height: 1.75rem; font-weight: 700; min-height: 1.75rem; }
.big { grid-area: big; display: flex; gap: 16px; }
.small { grid-area: small; display: flex; gap: 8px; justify-content: flex-end; }
.small .btn { width: 172px; }
.status { grid-area: status; min-height: 1.5rem; font-size: 1rem; line-height: 1.5rem; color: var(--muted); }
.status b { color: var(--ok); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; height: 48px; padding: 0 18px; border-radius: var(--r-btn); border: 2px solid var(--border-strong);
  background: var(--panel); color: var(--text); font: 650 1.0625rem var(--font); text-decoration: none; cursor: pointer; white-space: nowrap; }
.btn:hover { background: var(--sunken); }
.btn.answer { height: 56px; width: 270px; font-size: 1.1875rem; }
.btn.primary { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }
.btn.primary:hover { background: var(--accent-hover); border-color: var(--accent-hover); }
.btn.quiet { border-color: transparent; color: var(--accent); background: transparent; padding: 0 14px; }
.btn.quiet:hover { background: var(--accent-soft); }
.btn.go { background: var(--ok-strong); border-color: var(--ok-strong); color: #fff; }
.btn[aria-disabled="true"], .btn:disabled { opacity: .45; cursor: not-allowed; pointer-events: none; }
.btn.danger { color: var(--bad); border-color: var(--bad); }
.btn.wide { width: 100%; }
.btn.lg { height: 56px; font-size: 1.1875rem; padding: 0 28px; }
.chip-sug { display: inline-block; margin-left: 6px; padding: 0 7px; line-height: 1.25rem; border-radius: 999px; background: var(--ok-bg); color: var(--ok); font-size: .8125rem; font-weight: 700; }
.btn.answer .sub { display: block; font-size: .875rem; font-weight: 500; white-space: nowrap; }
.btn.answer.two { flex-direction: column; gap: 0; line-height: 1.3rem; }

/* ---------- single-panel pages (step 1, done screens, step 4) ---------- */
body.page { min-height: 100vh; display: flex; flex-direction: column; }
body.page .stick { position: sticky; top: 0; z-index: 5; }
.wrap { max-width: 1180px; width: 100%; margin: 0 auto; padding: 28px var(--gutter) 24px; flex: 1; }
.wrap.wide { max-width: 1440px; }
.page-h { display: flex; align-items: flex-end; gap: 24px; margin-bottom: 24px; }
.page-h .ph-main { flex: 1; }
.page-h h1 { font-size: 2rem; line-height: 2.5rem; font-weight: 750; }
.page-h p { color: var(--muted); margin-top: 6px; }
.panel { background: var(--panel); border: 1px solid var(--border); border-radius: var(--r-card); box-shadow: var(--shadow); padding: 28px; }
.panel + .panel { margin-top: 20px; }
.panel h2 { font-size: 1.375rem; line-height: 1.875rem; font-weight: 700; margin-bottom: 8px; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:35:36.189Z

**tool call — Bash**
````
{
 "command": "grep -n \"claude\\|re.compile\\|LEAK\\|haiku\" tests/e2e/test_demo_provenance.py tests/e2e/guided/*.py | cut -c1-260 | head -40; cat .claude/agent-memory/frontend/project_t204_prepared_fallback.md | head -40"
}
````

### User / tool · 2026-11-03T04:35:36.277Z

**tool result**
````
tests/e2e/guided/test_golden_path.py:18:        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=10000)
tests/e2e/guided/test_golden_path.py:23:        expect(page).to_have_url(re.compile(r"/case/[^/]+/timeline$"), timeout=10000)
tests/e2e/guided/test_step2.py:15:JARGON = re.compile(r"\b(model's|its quote|checked by code|itemized service line|tray|excerpt|judge|LLM|J[1-4])\b|\bflags?\b|\bpending\b|\bverified\b", re.I)
tests/e2e/guided/test_step2.py:252:    page.route(re.compile(r"/api/cases/[^/]+$"), strip)
tests/e2e/guided/test_step2.py:281:    page.route(re.compile(r"/api/cases/[^/]+$"), refuse)
tests/e2e/guided/test_step3.py:15:BILL_JARGON = re.compile(r"itemized service line|model's|its quote|\bmodel\b|\bexcerpt\b|\btray\b|\bjudge\b|\bLLM\b", re.I)
tests/e2e/guided/test_step3.py:116:    page.route(re.compile(r"/api/cases/[^/]+$"), inject)
tests/e2e/guided/test_step3.py:136:    page.route(re.compile(r"/api/cases/[^/]+/items/a1/review$"), refuse)
tests/e2e/guided/test_step3.py:174:    page.route(re.compile(r"/api/cases/[^/]+$"), inject)
tests/e2e/guided/test_step3.py:175:    page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), lambda route: route.fulfill(status=422, json={"error": {"code": "CONFIRM_REQUIRED", "message": "x", "detail": {"message": "stub"}}}) if route.request.post_da
tests/e2e/guided/test_step3.py:224:    page.route(re.compile(r"/api/cases/[^/]+$"), strip)
tests/e2e/guided/test_step3.py:303:    page.route(re.compile(r"/api/cases/[^/]+$"), overlap)
tests/e2e/guided/test_step3.py:321:    page.route(re.compile(r"/api/cases/[^/]+$"), none)
tests/e2e/guided/test_step4.py:36:        expect(page).to_have_url(re.compile(r"/new$"))
tests/e2e/guided/test_step4.py:39:        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
tests/e2e/guided/test_step4.py:44:        expect(page).to_have_url(re.compile(r"/timeline$"))
tests/e2e/guided/test_step4.py:47:        expect(page).to_have_url(re.compile(r"/letter$"))
tests/e2e/guided/test_step4.py:134:        b.click(); expect(page).to_have_url(re.compile(r"/timeline$"))
tests/e2e/guided/test_t205.py:118:    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
tests/e2e/guided/test_t205.py:144:    phone.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
tests/e2e/guided/test_t206.py:12:BARE = re.compile(r"(?<!statement dated )(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}")
tests/e2e/guided/test_t206.py:68:    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
tests/e2e/guided/test_t206.py:132:    phone.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
tests/e2e/test_demo_provenance.py:3:prepared by the team and its tooltip says the team prepared them and a second AI model checked them; /items/e1/trace's generator step is not claude-sonnet-5-5 and names a prepared answer; /audit rows for the generator carry
tests/e2e/test_demo_provenance.py:88:    assert gen["evidence"]["model"]["id"] != "claude-sonnet-5-5" and gen["evidence"]["model"]["id"] == PREPARED and gen["evidence"]["model"]["prepared"] is True
tests/e2e/test_demo_provenance.py:93:    assert not any(c["model"] == "claude-sonnet-5-5" for c in gens)
tests/e2e/test_demo_provenance.py:118:    assert "AI draft" not in body and "claude-sonnet-5-5" not in body and "The AI read this record" not in body
tests/e2e/test_demo_provenance.py:127:    assert PREPARED in drawer.inner_text() and "claude-sonnet-5-5" not in drawer.inner_text()
tests/e2e/test_demo_provenance.py:139:    assert gen["evidence"]["model"]["id"] == "claude-sonnet-5-5" and gen["evidence"]["model"]["prepared"] is False
tests/e2e/test_demo_provenance.py:175:    assert "claude-sonnet-5-5" not in line and "Drafted by" not in line, line
tests/e2e/test_demo_provenance.py:176:    assert "prepared by our team" in line.lower() and "not by an AI model" in line and "claude-haiku-5-5" in line, line
tests/e2e/test_demo_provenance.py:183:    """The judge panel, the Why dialog (stepper and recorded ladder), the audit drawer, tooltips and the banner, all open at once: no 'claude-sonnet', no 'Drafted by AI', no 'AI draft'."""
tests/e2e/test_demo_provenance.py:202:    for bad in ("claude-sonnet", "Drafted by AI", "drafted by AI", "AI draft", "recorded AI answers", "The AI's own answers"):
tests/e2e/test_demo_provenance.py:216:        assert "Drafted by claude-sonnet-5-5" in line and "claude-haiku-5-5" in line and "prepared" not in line.lower(), line
tests/e2e/test_demo_provenance.py:221:        assert "claude-sonnet-5-5" in gt and "extract_v1" in gt, gt
tests/e2e/guided/test_home.py:75:        expect(page).to_have_url(re.compile(rf"/case/{b}/timeline$"))
tests/e2e/guided/test_home.py:106:        expect(c.locator("[data-slot=meta]")).to_have_class(re.compile("bad"))
tests/e2e/guided/test_home.py:151:        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
tests/e2e/guided/test_home.py:246:        expect(card(page, title).get_by_test_id("case-next")).to_have_text(re.compile(r"^Next: Check the timeline\. \d+ of \d+ items left\.$"))
tests/e2e/guided/test_home.py:256:        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
---
name: t204-prepared-fallback
description: T-204 classic review.js fallback sentences keyed by item.prepared; input.js refusal rebuilt on zl:switcher; hold-the-route test recipe
metadata:
  type: project
---

Classic review.js paints fallback sentences (AI_HELD, ACCEPTED_HELD) until the server's trace sentence swaps in (withServerText). For a prepared item (`item.prepared` or case `models.generator_prepared`) it now paints PREPARED_HELD / PREPARED_ACCEPTED_HELD (same words as backend TRACE_WHY_PREPARED), via `isPrepared`/`heldText`. The guided UI has no such fallback (it renders item.why as given); "second AI check" stays allowed everywhere (the judge is a real model, api.md T-177 r3).

input.js demo refusal: `showError(..., {refusal:true})` sets `refusing`; switcher.js dispatches `zl:switcher` after draw(); input.js rebuilds the refusal then. Any other showError clears the flag.

**Test recipe (tests/e2e/test_prepared_first_paint.py):** hold requests with `page.route(re, lambda r: held.append(r))` and release with `route.continue_()` (a sync handler cannot sleep); a MutationObserver plus setInterval in `add_init_script` records every text the three nodes ever held. Undo needs a confirm click, so do not use btn-reset casually. Importing a fixture from another test module (`from tests.e2e.test_edit_to_check import edited_quote`) works.

**Round 2 (staff review blocker):** every static AI sentence is keyed too. `S.preparedFor(id)` / `S.allPrepared(ids)` in stepper.js (item.prepared OR case models.generator_prepared); `S.HELD_NO_RERUN(n, prep)` / `S.HELD_CAN_RERUN(n, prep)` take the flag (stepper heldWords, judges.js rows and group). Also keyed: judges.js label while loading (d null), rail legend, fmtCounts "AI" finder words, rerun button/errors, timeline tray flag/attempt sentences + REASON fallbacks, Why "Model calls", audit.js headings, app.js banner (case wins over health; hidden banner text is cleared), guided R.plain (model -> prepared answer) and the step2 legend. Judge wording ("second AI check", "AI objected", judge model id) stays.
**Test:** `test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai` (WATCH_ALL observer on document: text nodes, element text under 700 chars, title/aria-label, innerText every 40 ms; SECOND_CHECK allow-list strips judge phrases, LEAK regex on the rest). New wording anywhere must be either keyed on prepared or added to SECOND_CHECK with a reason. wait_for_function(string) is blocked by the page CSP: poll with page.evaluate through `_until`. The test server (ZLAYT_MODE=local) has health.answers != prepared but case.models.generator_prepared true, so key off the case, not health.
Known unkeyed: suggestions.js "tested on the claude-cli backend" accuracy line (allowed as an evaluation statement); guided step1 banner uses health.ai_banner.

**Round 3:** judges.js disagreement wording is keyed per item by who answered: `disLabel(x)` / `whoSaid(x)` (prepared + sources_disagree -> "the prepared answers"; prepared + judge_* -> "the second AI check"; live -> "the AI"); group heading "Where code and <who> read an item differently". Guided `G.provenance()` returns `pending: !health` and a neutral footer ("Checked by code; you decide every item.") until /api/health answers; pages themselves await health (core.js). Test allow-list is now whole sentences only (no open verb list; the calibration regex pins "matched the record N/M times in testing on the claude-cli backend (N golden cases, small sample)."). New tests: plain-sample panel, RERUN label (route stub sets a case step to status pending + next_action RERUN; the action only draws for fail/pending/skipped steps), guided walk with /api/health held. Rule: a verb list in an allow-list is how the next AI-attributing sentence slips through.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:35:42.732Z

**tool call — Bash**
````
{
 "command": "grep -n \"guided\\|case/\\|SPA\\|spa\" app/backend/main.py | head -40; sed -n 200,454p app/frontend/guided/styles.css"
}
````

### User / tool · 2026-11-03T04:35:42.825Z

**tool result**
````
ugrep: warning: app/backend/main.py: No such file or directory
.panel h2 { font-size: 1.375rem; line-height: 1.875rem; font-weight: 700; margin-bottom: 8px; }
.done-hero { display: flex; gap: 20px; align-items: center; }
.done-hero .big-check { flex: none; width: 64px; height: 64px; border-radius: 50%; background: var(--ok-strong); color: #fff; display: grid; place-items: center; font-size: 2rem; font-weight: 800; }
.done-hero .big-warn { flex: none; width: 64px; height: 64px; border-radius: 50%; background: var(--warn-bg); color: var(--warn); border: 2px solid var(--warn-edge); display: grid; place-items: center; font-size: 2rem; font-weight: 800; }
.done-hero h2 { font-size: 1.625rem; line-height: 2.125rem; margin: 0; }
.done-hero p { color: var(--muted); margin-top: 4px; }
.row-actions { display: flex; gap: 12px; margin-top: 24px; flex-wrap: wrap; }
.note-box { padding: 16px 20px; border-radius: 12px; border: 1px solid var(--warn-edge); background: var(--warn-bg); display: flex; gap: 16px; align-items: center; justify-content: space-between; }
.note-box.ok { border-color: transparent; background: var(--ok-bg); }
.note-box.bad { border-color: var(--bad); background: var(--bad-bg); }
.note-box .nb-text { font-weight: 600; }
.note-box .nb-text span { display: block; font-weight: 400; color: var(--muted); }

/* choice tiles */
.tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 20px 0; }
.tile { position: relative; display: block; padding: 22px; border-radius: 14px; border: 2px solid var(--border); background: var(--panel); cursor: pointer; min-height: 128px; }
.tile input { position: absolute; opacity: 0; }
.tile .tl-h { display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 1.1875rem; }
.tile .tl-h::before { content: ""; width: 22px; height: 22px; border-radius: 50%; border: 2px solid var(--border-strong); flex: none; }
.tile p { color: var(--muted); margin-top: 8px; font-size: 1rem; line-height: 1.5rem; }
.tile:has(input:checked) { border-color: var(--accent); background: var(--accent-soft); }
.tile:has(input:checked) .tl-h::before { border-color: var(--accent); background: var(--accent); box-shadow: inset 0 0 0 4px var(--panel); }
.tile:has(input:focus-visible) { outline: 3px solid var(--accent); outline-offset: 2px; }
.input-box { height: 280px; border-radius: 14px; border: 2px dashed var(--border-strong); background: var(--sunken); display: grid; place-items: center; text-align: center; padding: 24px; }
.input-box textarea { width: 100%; height: 100%; border: 0; background: transparent; font: 400 1rem/1.5rem var(--font); color: var(--text); resize: none; }
.input-box.solid { border-style: solid; background: var(--panel); place-items: stretch; padding: 16px; }
.field { display: flex; flex-direction: column; gap: 8px; max-width: 520px; }
.field label { font-weight: 700; }
.field input { height: 52px; padding: 0 14px; border-radius: 10px; border: 2px solid var(--border-strong); background: var(--panel); color: var(--text); font: 400 1.125rem var(--font); }
.field .hint { color: var(--muted); font-size: .9375rem; }
.err-slot { min-height: 28px; margin-top: 12px; color: var(--bad); font-weight: 600; font-size: 1rem; }

/* records list, stage checklist */
.list { list-style: none; margin: 0; padding: 0; border: 1px solid var(--border); border-radius: 12px; overflow: auto; }
.list li { display: grid; grid-template-columns: 44px 210px 1fr; gap: 12px; padding: 12px 16px; border-bottom: 1px solid var(--border); font-size: 1.0625rem; }
.list li:last-child { border-bottom: 0; }
.list .n { color: var(--muted); font-weight: 700; }
.stages { list-style: none; margin: 18px 0 0; padding: 0; display: grid; gap: 4px; }
.stages li { display: flex; align-items: center; gap: 14px; height: 44px; font-size: 1.0625rem; color: var(--muted); }
.stages .ic { width: 28px; height: 28px; border-radius: 50%; border: 2px solid var(--border-strong); flex: none; display: grid; place-items: center; font-size: .875rem; font-weight: 800; }
.stages li.done { color: var(--text); }
.stages li.done .ic { background: var(--ok-strong); border-color: var(--ok-strong); color: #fff; }
.stages li.now { color: var(--text); font-weight: 700; }
.stages li.now .ic { border-color: var(--accent); border-top-color: transparent; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .stages li.now .ic { animation: none; border-top-color: var(--accent); } }
.fixed-box { min-height: 520px; }

/* answers list */
.answers { list-style: none; margin: 12px 0 0; padding: 0; border: 1px solid var(--border); border-radius: 12px; }
.answers li { display: grid; grid-template-columns: 52px 170px 1fr 170px 110px; align-items: center; gap: 12px; padding: 10px 16px; border-bottom: 1px solid var(--border); font-size: 1rem; }
.answers li:last-child { border-bottom: 0; }
.answers .n { color: var(--muted); font-weight: 700; }
.answers .d { color: var(--muted); }
.answers .lbl { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.answers .btn { height: 44px; }

/* bills summary table */
.mini { width: 100%; border-collapse: collapse; font-size: 1.0625rem; }
.mini th { text-align: left; font-size: .9375rem; color: var(--muted); font-weight: 700; padding: 8px 12px; border-bottom: 1px solid var(--border); }
.mini td { padding: 12px; border-bottom: 1px solid var(--border); vertical-align: top; }
.mini td.amt { font-weight: 700; white-space: nowrap; font-variant-numeric: tabular-nums; }
.total-line { font-size: 1.5rem; line-height: 2rem; font-weight: 750; padding: 18px 20px; border-radius: 12px; background: var(--accent-soft); margin-top: 16px; }

/* letter */
.letter-grid { display: grid; grid-template-columns: 3fr 2fr; gap: 24px; }
.doc { margin: 0; font-family: var(--font); background: var(--paper); border: 1px solid var(--border); border-radius: 12px; height: 520px; overflow: auto; padding: 28px 32px; white-space: pre-wrap; font-size: 1.0625rem; line-height: 1.65rem; }
.doc.notes { background: var(--sunken); font-size: .9375rem; line-height: 1.45rem; }
.doc.placeholder { display: grid; place-items: center; color: var(--muted); text-align: center; white-space: normal; }
.doc-h { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.doc-h h2 { margin: 0; }
.doc-actions { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
.doc-actions .btn { min-width: 200px; }
.cfg { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)) auto; gap: 12px; align-items: end; margin-top: 12px; }
.cfg .field input { width: 100%; }
.blockers { list-style: none; margin: 16px 0 0; padding: 0; display: grid; gap: 10px; }
.blockers li { display: flex; gap: 16px; align-items: center; justify-content: space-between; padding: 14px 16px; border-radius: 10px; background: var(--panel); border: 1px solid var(--border); }

/* ---------- home ---------- */
.home-h { display: flex; align-items: flex-end; gap: 24px; margin-bottom: 8px; }
.home-h h1 { font-size: 2.25rem; line-height: 2.75rem; font-weight: 800; }
.home-h p { color: var(--muted); margin-top: 6px; }
.find { margin: 20px 0 8px; max-width: 420px; }
.find input { width: 100%; height: 48px; border-radius: 10px; border: 2px solid var(--border-strong); background: var(--panel); color: var(--text); font: 400 1.0625rem var(--font); padding: 0 14px; }
.sec-h { font-size: 1.25rem; font-weight: 750; margin: 28px 0 14px; display: flex; gap: 10px; align-items: baseline; }
.sec-h .c { color: var(--muted); font-weight: 600; }
.cases { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.ccard { grid-template-columns: minmax(0, 1fr); min-height: 244px; background: var(--panel); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 22px 24px; display: grid; grid-template-rows: auto auto auto 1fr auto; gap: 10px; }
.ccard .cc-top { display: flex; gap: 12px; align-items: center; }
.ccard .cc-top .btn { height: 36px; }
.ccard h3 { flex: 1; min-width: 0; font-size: 1.3125rem; line-height: 1.75rem; font-weight: 750; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ccard .cc-meta { color: var(--muted); font-size: .9375rem; line-height: 1.25rem; }
.track { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
.track li { display: flex; flex-direction: column; gap: 6px; font-size: .8125rem; line-height: 1rem; color: var(--muted); }
.track li i { display: block; height: 8px; border-radius: 999px; background: var(--sunken); border: 1px solid var(--border); }
.track li.done i { background: var(--ok-strong); border-color: var(--ok-strong); }
.track li.current i { background: var(--accent); border-color: var(--accent); }
.track li.current { color: var(--text); font-weight: 700; }
.track li.attn i { background: var(--warn-edge); border-color: var(--warn-edge); }
.track li.attn { color: var(--warn); font-weight: 700; }
.ccard .next { font-size: 1.0625rem; line-height: 1.5rem; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.ccard .next b { font-weight: 750; }
.ccard .next.ok { color: var(--ok); }
.ccard .next.warn { color: var(--warn); }
.ccard .cc-bottom { display: flex; gap: 10px; align-items: center; }
.ccard .cc-bottom .btn.lg { flex: 1; }
.skel { background: linear-gradient(90deg, var(--sunken), var(--panel), var(--sunken)); background-size: 200% 100%; animation: sk 1.4s ease infinite; border-radius: 8px; }
@keyframes sk { to { background-position: -200% 0; } }
@media (prefers-reduced-motion: reduce) { .skel { animation: none; } }
.empty { text-align: center; padding: 64px 24px; }
.empty .em-ic { width: 88px; height: 88px; margin: 0 auto 20px; border-radius: 24px; background: var(--accent-soft); color: var(--accent); display: grid; place-items: center; font-size: 2.5rem; font-weight: 800; }
.empty h2 { font-size: 1.75rem; line-height: 2.25rem; }
.empty p { color: var(--muted); margin: 8px auto 0; max-width: 520px; }
.empty .row-actions { justify-content: center; }

/* screens index */
.screens { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.screens a { display: block; padding: 16px 18px; border-radius: 12px; background: var(--panel); border: 1px solid var(--border); text-decoration: none; color: var(--text); }
.screens a b { display: block; }
.screens a span { color: var(--muted); font-size: .9375rem; line-height: 1.375rem; }
.variant { font-size: .8125rem; font-weight: 700; color: var(--warn); }

/* ---------- phones ---------- */
@media (max-width: 760px) {
  :root { --gutter: 16px; --banner-h: 44px; --header-h: 52px; --steps-h: 66px; --title-h: 48px; }
  body { font-size: 1.0625rem; line-height: 1.6rem; }
  .banner { font-size: .8125rem; line-height: 1.05rem; flex-direction: column; gap: 0; }
  .banner .b-demo { display: block; }
  .header { gap: 8px; }
  .demo-pill, .header .case-sub { display: none; }
  .brand span:last-child { font-size: 1rem; }
  .back-cases { height: 40px; padding: 0 10px 0 6px; font-size: .9375rem; }
  .back-cases .long { display: none; }
  .back-cases .short { display: inline; }
  .case-title { font-size: 1.0625rem; }
  .theme-btn { min-width: 0; width: 44px; height: 40px; font-size: 0; position: relative; }
  .theme-btn::after { content: "\25D0"; font-size: 1.25rem; }
  .steps { padding: 0 8px; }
  .steps li + li::before { display: none; }
  .step { flex-direction: column; justify-content: center; gap: 2px; padding: 0 2px 6px; text-align: center; }
  .step::after { left: 8px; right: 8px; }
  .step .dot { width: 24px; height: 24px; font-size: .75rem; border-width: 2px; }
  .step .st-text { align-items: center; }
  .step .st-label { font-size: .8125rem; line-height: 1rem; }
  .step .st-label .long { display: none; }
  .step .st-label .short { display: inline; }
  .step .st-status { font-size: .75rem; line-height: .95rem; }
  .titlebar { gap: 12px; padding-bottom: 4px; }
  .titlebar .eyebrow, .titlebar .t-ai { display: none; }
  .titlebar h1 { font-size: 1.25rem; line-height: 1.625rem; }
  .count-box { width: 132px; }
  .count-line { font-size: .875rem; }
  .count-line .of { display: none; }
  .bar { height: 8px; margin-top: 4px; }
  .titlebar:has(.total-chip) .t-main { display: none; }
  .total-chip { flex: 1; width: auto; padding: 4px 10px; display: flex; align-items: baseline; justify-content: space-between; gap: 8px; box-shadow: none; }
  .total-chip .tc-l { font-size: .75rem; line-height: 1rem; }
  .total-chip .tc-v { font-size: 1.0625rem; line-height: 1.4rem; }
  .work { grid-template-columns: minmax(0, 1fr); grid-template-rows: minmax(0, 1fr) 256px; gap: 8px; padding-bottom: 8px; }
  .card-src .card-h .ch-title { display: none; }
  .card-f .label-cap { display: none; }
  .card-f.plain { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .card-h { padding: 10px 14px; min-height: 48px; gap: 8px; }
  .card-h .ch-title { font-size: .9375rem; }
  .card-h .ch-sub { font-size: .875rem; }
  .card-b { padding: 12px 14px; }
  .card-f { min-height: 0; padding: 10px 14px; font-size: .875rem; line-height: 1.3rem; }
  .rec { font-size: 1rem; line-height: 1.6rem; }
  .line-when { font-size: .9375rem; margin-bottom: 4px; }
  .line-text { font-size: 1.125rem; line-height: 1.6rem; }
  .money { font-size: 2rem; line-height: 2.5rem; }
  .warn-title { font-size: 1.0625rem; line-height: 1.5rem; margin-bottom: 4px; }
  .explain { font-size: .9375rem; line-height: 1.4rem; }
  textarea.edit { font-size: 1.0625rem; line-height: 1.5rem; min-height: 0; height: 8rem; }      /* a fixed height: 100% of a body that grows with the hint above it ran over the card foot, hiding a refusal (UX r2) */
  .check { font-size: .9375rem; line-height: 1.35rem; gap: 10px; margin-top: 6px; }
  .check input { width: 26px; height: 26px; }
  .actions-in { grid-template-columns: minmax(0, 1fr); grid-template-areas: "q" "big" "small" "status"; padding: 8px 16px 6px; row-gap: 6px; }
  .question { font-size: 1rem; line-height: 1.35rem; min-height: 2.7rem; display: flex; align-items: center; }
  .big { gap: 10px; }
  .btn.answer { flex: 1; width: auto; min-width: 0; height: 54px; font-size: 1.0625rem; padding: 0 8px; white-space: normal; text-align: center; line-height: 1.25rem; }
  .btn.answer .sub { font-size: .75rem; }
  .small { justify-content: space-between; gap: 4px; }
  .small .btn { flex: 1 1 0; width: auto; min-width: 0; height: 40px; font-size: .875rem; padding: 0 4px; }
  .status { font-size: .875rem; min-height: 1.25rem; line-height: 1.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .wrap { padding: 20px 16px; }
  .page-h { flex-direction: column; align-items: stretch; gap: 12px; }
  .page-h h1 { font-size: 1.625rem; line-height: 2.125rem; }
  .panel { padding: 18px; }
  .tiles { grid-template-columns: 1fr; gap: 10px; }
  .tile { min-height: 0; padding: 16px; }
  .input-box { height: 220px; }
  .list li { grid-template-columns: 30px 1fr; }
  .list li .src { grid-column: 2; }
  .done-hero { align-items: flex-start; }
  .done-hero .big-check, .done-hero .big-warn { width: 48px; height: 48px; font-size: 1.5rem; }
  .done-hero h2 { font-size: 1.3125rem; line-height: 1.75rem; }
  .answers li { grid-template-columns: 34px minmax(0, 1fr) auto; grid-template-areas: "n lbl btn" "n d btn" "n ans btn"; row-gap: 2px; }
  .answers .n { grid-area: n; } .answers .d { grid-area: d; font-size: .875rem; } .answers .lbl { grid-area: lbl; } .answers .ans { grid-area: ans; } .answers .btn { grid-area: btn; }
  .note-box { flex-direction: column; align-items: stretch; }
  .letter-grid { grid-template-columns: 1fr; }
  .doc { height: 420px; padding: 18px; font-size: .9375rem; line-height: 1.45rem; }
  .doc.notes { height: 320px; font-size: .875rem; }
  .doc-actions .btn { min-width: 0; flex: 1; }
  .cfg { grid-template-columns: 1fr; }
  .mini { font-size: .9375rem; }
  .mini th:nth-child(3), .mini td:nth-child(3) { display: none; }
  .home-h { flex-direction: column; align-items: stretch; gap: 14px; }
  .home-h h1 { font-size: 1.875rem; line-height: 2.25rem; }
  .cases { grid-template-columns: minmax(0, 1fr); }
  .ccard { min-height: 0; padding: 18px; }
  .ccard h3 { font-size: 1.1875rem; }
  .track li { font-size: .6875rem; }
  .screens { grid-template-columns: 1fr; }
  .footer { padding: 12px 16px 16px; font-size: .875rem; }
  .row-actions .btn { flex: 1 1 100%; white-space: normal; text-align: center; height: auto; min-height: 56px; padding: 8px 16px; }
  .ccard .cc-bottom .btn.lg { min-width: 0; padding: 0 12px; }
}
@media (max-width: 359px) {
  .small .btn { font-size: .875rem; padding: 0 4px; }
  .mini td.amt { white-space: normal; }
  .mini th:nth-child(4), .mini td:nth-child(4) { display: none; }
  .mini { table-layout: fixed; }
}
/* Short phones (e.g. 320x640, landscape): the frame would leave no room for the record, so the page scrolls instead.
   Still nothing moves on click: the action bar stays pinned to the bottom and every box keeps its size. */
@media (max-width: 760px) and (max-height: 720px) {
  html:has(> body.frame) { overflow: visible; }
  body.frame { display: block; height: auto; overflow: visible; }
  body.frame .titlebar { height: var(--title-h); }
  .work { display: grid; grid-template-rows: none; grid-auto-rows: auto; }
  .work .card { max-height: none; }
  .work .card-src .card-b { max-height: 260px; }
  .work .card + .card .card-b { min-height: 120px; }
  .actions { position: sticky; bottom: 0; z-index: 4; }
}



/* ---------- shell additions (T-181) ---------- */
.view { display: contents; }                                    /* the page's own boxes become children of <body> (the frame grid needs titlebar, work and actions as grid rows) */
.stick { position: relative; }
body.page .stick { position: sticky; top: 0; z-index: 5; }
body.frame .stick { display: contents; }                        /* banner, header and step bar are three grid rows in the frame */
body.frame .footer { display: none; }                           /* provenance stays in the pill / title row: the frame has no room for a footer */
body.page .view { display: block; flex: 1; }
.skip { position: absolute; left: 8px; top: -64px; z-index: 100; background: var(--panel); color: var(--text); padding: 8px 16px; border: 2px solid var(--accent); border-radius: 10px; font-weight: 600; }
.skip:focus { top: 8px; }
.brand-mark, .step .dot { user-select: none; }
.footer .f-live { margin-left: auto; }
.errbox { max-width: 720px; margin: 48px auto; text-align: center; }
.errbox h1 { font-size: 2rem; line-height: 2.5rem; }
.errbox p { color: var(--muted); margin-top: 8px; }
.step.attn .st-status { white-space: nowrap; }
.hd-case { min-width: 0; display: flex; align-items: baseline; gap: 12px; }
html:has(> body.frame) { scrollbar-gutter: stable; }            /* with classic scrollbars the page layout reserves a gutter; the frame reserves the same one, so the chrome keeps its width when a step switches layout */
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:36:05.220Z

**tool call — Bash**
````
{
 "command": "grep -rn \"How it was checked\\|card-foot\" tests/e2e | cut -c1-200 | head -30; grep -rn \"card-f\\b\\|card-line\\|lineBody\\|line-body\" tests/e2e | cut -c1-160 | wc -l; cat app/frontend/guided/review.css | head -60"
}
````

### User / tool · 2026-11-03T04:36:05.337Z

**tool result**
````
tests/e2e/conftest.py:18:  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-
tests/e2e/test_stepper.py:105:    """Flags and charges have no Why? button; a 'How it was checked' button opens the same stepper (flags: code-made flags skip the judge on purpose)."""
tests/e2e/guided/test_t205.py:122:    note = page.get_by_test_id("confirm-note"); expect(note).to_be_visible(); assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() ==
tests/e2e/guided/test_round2.py:168:        foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved.")
tests/e2e/guided/test_round3.py:16:           chk: R(q('check-compare')), foot: R(q('card-foot')), scrollTop: body ? body.scrollTop : null, scrollH: body ? body.scrollHeight : null, lineH: mark ? pars
tests/e2e/guided/test_round3.py:89:        foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved.")
tests/e2e/guided/test_round3.py:91:        r = page.evaluate("""() => { const f = document.querySelector('[data-testid=card-foot]'), r = f.getBoundingClientRect(), bar = document.querySelector('[data-
tests/e2e/guided/test_step2.py:88:    foot = page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step2.py:104:        text = " ".join(page.get_by_test_id(t).inner_text() for t in ("card-line", "card-foot", "question", "src-head", "actions"))
tests/e2e/guided/test_step2.py:126:    assert "never in the letter" in page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step2.py:176:    foot = page.get_by_test_id("card-foot").inner_text(); assert foot.startswith("Your answer: kept in the letter.") and "You can change it" in foot, foot
tests/e2e/guided/test_step2.py:204:    foot = page.get_by_test_id("card-foot")
tests/e2e/guided/test_step2.py:211:    assert page.get_by_test_id("card-foot").inner_text().startswith("Your answer: left out of the letter.")
tests/e2e/guided/test_step2.py:227:    assert "second check found" not in page.get_by_test_id("card-foot").inner_text() and "quote" not in page.get_by_test_id("card-foot").inner_text().lower()
tests/e2e/guided/test_step2.py:257:    foot = page.get_by_test_id("card-foot").inner_text(); assert "A second AI check found this only partly supported" in foot and "Not saved" not in foot, foot      
tests/e2e/guided/test_step2.py:303:    foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved"); assert "9" in foot.inner_text() and "highlighted words" in foot.inner_text() 
tests/e2e/guided/test_step2.py:325:    expect(page.get_by_test_id("card-foot")).to_contain_text("Pick sentences that follow each other."); assert sent == []
tests/e2e/guided/test_step2.py:353:    assert dtc["suggestion"]["reason"] in page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step2.py:360:    assert "Part 2 of 2" in page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step2.py:386:    page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("card-foot")).to_contain_text("Pick at least one sentence.")
tests/e2e/guided/test_step2.py:387:    sents.nth(0).click(); page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("card-foot")).to_contain_text("Write the line first.")
tests/e2e/guided/test_step2.py:482:          "[data-testid=question]", "[data-testid=card-src]", "[data-testid=card-line]", "[data-testid=card-foot]", "[data-testid=actions]", "[data-testid=status-slo
tests/e2e/guided/test_step2.py:495:        skip = ("[data-testid=card-foot]",) if w < 761 else ()               # on a phone the line card scrolls as one box, so its footer may move inside it
tests/e2e/guided/test_step3.py:42:    assert "added to the bill total" in page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step3.py:82:    assert "never added to the bill total" in page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step3.py:97:    expect(page.get_by_test_id("card-foot")).to_contain_text("This item changed in another tab. We've loaded the latest.")
tests/e2e/guided/test_step3.py:101:    assert page.get_by_test_id("card-foot").inner_text().startswith("Your answer: not counted.")
tests/e2e/guided/test_step3.py:120:    assert "I checked: this is a separate charge, not the same one counted twice." in page.get_by_test_id("card-foot").inner_text()
tests/e2e/guided/test_step3.py:138:    foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("This looks like the same charge twice. Confirm it is a separate charge to count it.")
tests/e2e/guided/test_step3.py:180:    expect(page.get_by_test_id("card-foot")).to_contain_text("stub")
      33
/* Review pages (step 2 and 3): the fixed frame, the action bar, the phone layout. OWNER: frontend-B. Loaded after styles.css, so equal-specificity rules here win.
   Nothing moves when she answers: every box below has a fixed size on desktop (title row, cards, footer slot, action bar rows, status slot). Spec 0, 2.5-2.7, 8; T-180 review majors. */

/* ---------- desktop ---------- */
@media (min-width: 761px) {
  :root { --title-h: 120px; }
  .titlebar { padding-top: 12px; align-items: flex-start; }
  .titlebar .count-box { padding-top: 8px; }
  .titlebar .total-chip { margin-top: 4px; }
  .titlebar .t-ai { white-space: normal; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: .875rem; line-height: 1.2rem; max-width: 880px; }
  .steps-toggle { display: none; }
  .card-f { min-height: 0; height: 150px; overflow: auto; padding: 12px 24px; }
}
/* 1366x768 and other short desktops: give the cards the room */
@media (min-width: 761px) and (max-height: 820px) {
  :root { --title-h: 88px; }
  .titlebar .t-ai { display: none; }
  .titlebar { padding-top: 8px; }
  .card-f { height: 120px; padding: 10px 20px; }
  .card-h { min-height: 52px; padding-top: 10px; padding-bottom: 10px; }
  .actions-in { padding-top: 10px; padding-bottom: 8px; row-gap: 8px; }
}

/* ---------- action bar: the status slot holds the saved sentence and Undo, always whole ---------- */
.actions .status { grid-area: status; display: flex; align-items: center; gap: 8px; min-height: 40px; }
.actions .status .st-msg { flex: 1; min-width: 0; }
.actions .status.hint { color: var(--subtle); font-size: .9375rem; }
.actions .status .undo { flex: none; height: 36px; padding: 0 14px; border-color: var(--accent); }
.btn.hint { background: var(--accent-soft); border-color: var(--accent); }
.btn.answer .sub { white-space: normal; text-align: center; }

/* ---------- the cards ---------- */
.card-h .ch-title { flex: none; white-space: nowrap; }
.card-h .tag { flex: none; }
.card-b .line-text, .card-b .explain, .card-b .warn-title { overflow-wrap: anywhere; }
.gap-top { margin-top: 12px; }
.src-hint, .fix-hint { font-size: 1rem; margin-bottom: 12px; }
.fix-hint { margin-bottom: 10px; }
.foot-warn { margin-top: 8px; color: var(--text); font-weight: 600; }
.foot-rule { border: 0; border-top: 1px solid var(--warn-edge); margin: 10px 0 8px; }
.card-f .check { margin-top: 6px; font-size: 1rem; line-height: 1.4rem; }
.card-f .check input { width: 28px; height: 28px; }
.card-f .label-cap { color: var(--muted); }
.also q { display: inline; }
.also div { margin-top: 4px; }
.sent { display: inline; }
.sent:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
.rec .meta { opacity: .85; }

/* ---------- done screens ---------- */
.legend { margin-top: 12px; font-size: .9375rem; line-height: 1.4rem; }
.plain-list { margin: 8px 0 0; padding-left: 20px; }
.rule-out + .rule-out { margin-top: 12px; }
.note-box.overlap { margin-bottom: 20px; flex-wrap: wrap; }
.row-actions.tight { margin-top: 0; }
.answers .tag { max-width: 100%; overflow: hidden; text-overflow: ellipsis; }

/* ---------- phones: the step bar folds behind "Step N of 4" (an overlay, so no row changes size), the record gets the room ---------- */
@media (max-width: 760px) {
  body.frame { grid-template-rows: var(--banner-h) var(--header-h) 0 var(--title-h) minmax(0, 1fr) auto; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:36:27.886Z

**tool call — Bash**
````
{
 "command": "sed -n 470,520p tests/e2e/guided/test_step2.py | cut -c1-400"
}
````

### User / tool · 2026-11-03T04:36:27.970Z

**tool result**
````
    for _ in range(25):                                                                                           # Decide later walks the list; its end is the done screen
        if page.get_by_test_id("done-heading").count():
            break
        page.get_by_test_id("btn-later").click(); settle(page, 100)
    expect(page.get_by_test_id("done-heading")).to_have_text("2 items still need a decision.")
    assert page.get_by_test_id("step-2").get_attribute("data-state") in ("todo", "attn")
    page.get_by_test_id("btn-first-undecided").click(); expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e3")


# ------------------------------------------------------------------------------------------------ layout: nothing moves, above the fold, phones

STABLE = ("[data-testid=step-bar]", "[data-testid=titlebar]", "[data-testid=answer-yes]", "[data-testid=answer-no]", "[data-testid=btn-back]", "[data-testid=btn-third]", "[data-testid=btn-later]",
          "[data-testid=question]", "[data-testid=card-src]", "[data-testid=card-line]", "[data-testid=card-foot]", "[data-testid=actions]", "[data-testid=status-slot]")


def boxes(page, skip=()):
    return {s: rect(page, s) for s in STABLE if s not in skip}


@pytest.mark.parametrize("w,h", [(1440, 900), (1366, 768), (390, 844)])
def test_nothing_moves_when_she_answers_or_changes_mode_and_the_primary_action_is_above_the_fold(pw, make, w, h):
    tok = make(LIB10); b, pg = sized(pw, w, h)
    try:
        seen = watch(pg)
        open_item(pg, tok, "e1")
        skip = ("[data-testid=card-foot]",) if w < 761 else ()               # on a phone the line card scrolls as one box, so its footer may move inside it
        first = boxes(pg, skip)
        y = pg.get_by_test_id("answer-yes").bounding_box(); assert y["y"] + y["height"] <= h, f"the primary action is below the fold at {w}x{h}"
        assert rect(pg, "[data-testid=actions]")[1] + rect(pg, "[data-testid=actions]")[3] == h, "the action bar sits at the bottom of the window"
        assert pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight") and pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        pg.get_by_test_id("check-compare").check(); assert boxes(pg, skip) == first, "ticking the box moved something"
        pg.get_by_test_id("check-compare").uncheck(); assert boxes(pg, skip) == first
        pg.get_by_test_id("btn-third").click(); assert boxes(pg, skip) == first, "Fix the wording moved something"
        pg.get_by_test_id("answer-no").click(); assert boxes(pg, skip) == first, "Cancel moved something"
        pg.get_by_test_id("btn-later").click(); pg.wait_for_timeout(200)
        assert boxes(pg, skip) == first, "the next item sits in the same boxes"
        pg.get_by_test_id("answer-no").click(); pg.wait_for_timeout(300)
        assert boxes(pg, skip) == first, "an answer moved something (a Saved line, Undo)"
        pg.get_by_test_id("btn-back").click(); pg.wait_for_timeout(200); assert boxes(pg, skip) == first
        assert seen == [], seen
    finally:
        b.close()


def test_a_phone_shows_enough_of_the_record_keeps_undo_whole_and_folds_the_step_bar(phone, make):
    tok = make(); watch(phone)
    open_item(phone, tok, "e4")
    src = phone.get_by_test_id("card-source")
    ch, sh = src.evaluate("e => e.clientHeight"), src.evaluate("e => e.scrollHeight")
    assert ch >= 200 or sh - ch <= 24, f"the record shows {ch}px of {sh}px"
    assert phone.get_by_test_id("step-bar").evaluate("e => e.getBoundingClientRect().height") == 0, "the step bar is folded"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:36:56.605Z

**tool call — Bash**
````
{
 "command": "grep -rn \"guided\" app/backend/*.py | grep -v \"^app/backend/.*#\" | head -20; ls app/backend | head -50"
}
````

### User / tool · 2026-11-03T04:36:56.699Z

**tool result**
````
app/backend/api.py:681:        guided = sd / "guided"
app/backend/api.py:686:                """The guided app uses real paths (/case/<token>/timeline). A path that is not a file and has no extension is a screen: answer index.html, which routes it in the browser.
app/backend/api.py:694:                        return FileResponse(guided / "index.html")
app/backend/api.py:696:                        return FileResponse(guided / "index.html")
app/backend/api.py:700:                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
app/backend/api.py:711:            app.mount("/", GuidedFiles(directory=str(guided), html=True), name="frontend")
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
case_list.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
count_charge.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
encounter_types.json
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
limits.py
money.py
narrative.py
overlap.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
pdf_text.py
pipeline.py
present.py
reclassify.py
rejudge.py
review.py
schemas.py
sentences.py
service_date.py
spanish.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:36:58.478Z

**tool call — Bash**
````
{
 "command": "sed -n 675,715p app/backend/api.py; grep -n \"Content-Security\\|img-src\\|default-src\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-03T04:36:58.568Z

**tool result**
````
        finally:
            c.close()

    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
    if sd.is_dir():
        from fastapi.staticfiles import StaticFiles
        guided = sd / "guided"
        if (guided / "index.html").is_file():                                           # D-068: the guided app is the front door; the old screen stays reachable at /classic
            from fastapi.responses import FileResponse

            class GuidedFiles(StaticFiles):
                """The guided app uses real paths (/case/<token>/timeline). A path that is not a file and has no extension is a screen: answer index.html, which routes it in the browser.
                /api and /classic never fall through to it (an unknown /api path must stay a JSON 404)."""
                async def get_response(self, path, scope):
                    try:
                        resp = await super().get_response(path, scope)
                    except StarletteHTTPException as e:
                        if e.status_code != 404 or path.startswith(("api/", "classic/")) or path in ("api", "classic") or "." in path.rsplit("/", 1)[-1]:
                            raise
                        return FileResponse(guided / "index.html")
                    if resp.status_code == 404 and not path.startswith(("api/", "classic/")) and "." not in path.rsplit("/", 1)[-1]:
                        return FileResponse(guided / "index.html")
                    return resp

            def classic_open():
                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
                return local_mode() or os.environ.get("ZLAYT_CLASSIC") == "1"

            class ClassicFiles(StaticFiles):
                async def get_response(self, path, scope):
                    if not classic_open():
                        return RedirectResponse("/")
                    return await super().get_response(path, scope)

            app.add_api_route("/classic", lambda: RedirectResponse("/classic/" if classic_open() else "/"), include_in_schema=False)       # the mount only answers /classic/ ; /classic would fall to the guided mount
            app.mount("/classic", ClassicFiles(directory=str(sd), html=True), name="classic")
            app.mount("/", GuidedFiles(directory=str(guided), html=True), name="frontend")
        else:
            app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
    return app
app/backend/api.py:31:CSP = ("default-src 'none'; script-src 'self'; script-src-attr 'unsafe-hashes' 'sha256-%s'; style-src 'self'; img-src 'self' data:; "
app/backend/api.py:227:        resp.headers["Content-Security-Policy"] = CSP
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:37:02.737Z

**tool call — Bash**
````
{
 "command": "sed -n 60,200p submission/validation-ladder.svg; git log --oneline -3 -- submission/validation-ladder.svg; ls docs; ls evals | head; ls app/llm | head -30"
}
````

### User / tool · 2026-11-03T04:37:02.870Z

**tool result**
````
  <path d="M255,524 V534" stroke="#444" stroke-width="1.6" marker-end="url(#ar)"/>

  <!-- export -->
  <rect x="20" y="536" width="470" height="48" rx="6" fill="#111" stroke="#111"/>
  <text x="34" y="555" font-size="12.5" font-weight="700" fill="#fff">Export, assembled by code from accepted items only</text>
  <text x="34" y="572" font-size="11.5" fill="#ddd">Letter: quotes + charges. Internal notes (do not send): flags, unclear amounts.</text>

  <!-- rejected tray, right of rung 1 -->
  <path d="M490,233 H520 V300 H540" fill="none" stroke="#b3261e" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ar)"/>
  <rect x="542" y="262" width="258" height="78" rx="6" fill="#fdecea" stroke="#b3261e"/>
  <text x="554" y="282" font-size="12" font-weight="700" fill="#8c1d18">Could not verify (visible list)</text>
  <text x="554" y="298" font-size="11" fill="#222">Quote not in the record, or a number</text>
  <text x="554" y="312" font-size="11" fill="#222">the quote lacks. Never a flag, never in</text>
  <text x="554" y="326" font-size="11" fill="#222">the letter. She can write the entry herself.</text>

  <!-- code-only lane -->
  <rect x="542" y="40" width="258" height="202" rx="6" fill="#f3f3f3" stroke="#888"/>
  <text x="554" y="60" font-size="12" font-weight="700" fill="#111">Code, no model</text>
  <text x="554" y="78" font-size="11" fill="#222">Split records (a model may only point at</text>
  <text x="554" y="92" font-size="11" fill="#222">cut offsets for an unsplittable paste;</text>
  <text x="554" y="106" font-size="11" fill="#222">code validates). Parse dates (an ambiguous</text>
  <text x="554" y="120" font-size="11" fill="#222">date waits for her). Gap arithmetic: 29 and</text>
  <text x="554" y="134" font-size="11" fill="#222">30 days no, 31 yes; 28 no, 73 yes.</text>
  <text x="554" y="152" font-size="11" fill="#222">Find every dollar amount and its class (a</text>
  <text x="554" y="166" font-size="11" fill="#222">rate is never a charge). Totals of what she</text>
  <text x="554" y="180" font-size="11" fill="#222">accepted. Flag wording from templates.</text>
  <text x="554" y="198" font-size="11" fill="#222">Dates and amounts always need her accept.</text>
  <text x="554" y="212" font-size="11" fill="#222">Conflict pairs come from code; the judge</text>
  <text x="554" y="226" font-size="11" fill="#222">says only conflict or benign.</text>

  <!-- evidence -->
  <rect x="542" y="358" width="258" height="226" rx="6" fill="#ffffff" stroke="#888"/>
  <text x="554" y="378" font-size="12" font-weight="700" fill="#111">Measured (live run, 3 runs)</text>
  <text x="554" y="396" font-size="11" fill="#222">Rung 1: grounding 1.000, 242 checked</text>
  <text x="554" y="412" font-size="11" fill="#222">Rung 2: seeded wrong summaries caught</text>
  <text x="554" y="426" font-size="11" fill="#222">40/40; correct ones rejected 0 of 10</text>
  <text x="554" y="442" font-size="11" fill="#222">Conflict judge 20/20, flag judge 12/12,</text>
  <text x="554" y="456" font-size="11" fill="#222">0 false agrees</text>
  <text x="554" y="474" font-size="11" fill="#222">Rung 3: persona 4 of 5 on the old screen,</text>
  <text x="554" y="488" font-size="11" fill="#222">which I found very hard to use; rebuilding as</text>
  <text x="554" y="502" font-size="11" fill="#222">four steps (D-068), not yet scored. 5 of 5</text>
  <text x="554" y="516" font-size="11" fill="#222">disputed summaries took one click (T-179)</text>
  <text x="554" y="536" font-size="10" fill="#555">Sources: evals/reports/20261102T164038Z.md;</text>
  <text x="554" y="549" font-size="10" fill="#555">submission/prompt-log/reviews/GATE-M3-</text>
  <text x="554" y="562" font-size="10" fill="#555">paralegal.md, GATE-M3-product-manager.md;</text>
  <text x="554" y="575" font-size="10" fill="#555">docs/LLM_VS_CODE.md</text>
</svg>
6d6dc45 fix(submission): T-185/T-186 r3 library numbers cite only library-latest.md; counts computed at 18bfa69 with re-run commands; D-065 wording, CHRIS marker, card refs
ddfbf6d docs(submission): T-185/T-186 round 2: redesign story (persona 4/5 predates D-068), only-committed claims, fresh unit count, library recall beside golden, engineering role, stretch reasons
59e33ca docs(submission): one-page product note, Part 2 process doc, validation-ladder SVG
CONTRACT.md
GUIDED_UI_SPEC.md
LLM_VS_CODE.md
M2M3_COVERAGE.md
RUNBOOK.md
UI_DESIGN_BRIEF.md
__init__.py
__pycache__
adversarial
finalize_prompt_log.py
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
__init__.py
__pycache__
_types.py
audited.py
backends
lexicon.yaml
promptlib.py
prompts
provider.py
record.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:37:09.664Z

**tool call — Bash**
````
{
 "command": "ls app/llm/prompts | head -30; git remote -v | head -2; grep -n \"github\" README.md | head -3; grep -n \"^|\" docs/LLM_VS_CODE.md | head -30 | cut -c1-200"
}
````

### User / tool · 2026-11-03T04:37:09.782Z

**tool result**
````
extract_es_v1.md
extract_v1.md
flags_v1.md
judge_amount_class_v1.md
judge_conflict_v1.md
judge_conflict_v2.md
judge_conflict_v4.md
judge_conflict_v5.md
judge_conflict_v6.md
judge_faithfulness_es_v1.md
judge_faithfulness_v1.md
judge_flag_v1.md
judge_flag_v2.md
judge_flag_v3.md
narrative_v1.md
split_v1.md
16:git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt
27:| # | Pipeline step | Code or LLM | Why we drew the line here | How it is checked |
28:|---|---|---|---|---|
29:| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges in
30:| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on th
31:| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The
32:| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Re
33:| 5 | Clinical facts as a separate list | **Not built.** The summary and the verbatim excerpt carry the facts. | Every extra paraphrased field is another place to invent medical content. | n/a (del
34:| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are n
35:| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable figure is *unclear*
36:| 8 | Running total of charges | **Code**: sum of **accepted** amounts of class `charge`. The screen also shows "Pending review" separately and a "detected, not a total" figure. Rates, estimates, d
37:| 9 | Treatment gap longer than 30 days | **Code** over the code-parsed **record dates** of all (de-duplicated) clinical-encounter records (billing statements and phone notes are excluded), indepen
38:| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**: a lexicon of accide
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems versus a history sentence in another record | **Code proposes; the LLM only clas
40:| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by code on every record
41:| 13 | Language that weakens causation ("may represent degenerative change", "patient states", missed appointments, "new onset", scene facts such as refusing transport, an attorney referral; normal
42:| 14 | The wording of every flag | **Code**: a fixed template per flag type and category, filled with dates, source labels and the verbatim quote. For example "Gap of 73 days between March 6, 2026 
43:| 15 | Numbers and dates in a summary or in the paralegal's edit | **Code**: every number, date, dollar figure and left/right/no/not/without in the text must be in the excerpt (or the record's sour
44:| 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. Everything derived from that record needs revi
45:| 17 | Confidence state per item (`verified`, `needs_review`, `rejected`) | **Code**: a fixed rule over the checks (rejected if a grounding check fails; needs review on any doubt; verified only if 
46:| 18 | The "Why?" sentence | **Code**: one template per reason code. | A model explaining its own doubt would be another unverified claim. | Test: every reason code has a template. |
47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, a date of service, and an e
48:| 20 | Audit trail | **Code**: every model call stores model, backend, prompt version and hash, full prompt and response, verdict, latency, cost; every human action stores before and after. | If so
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:37:19.009Z

**tool call — Bash**
````
{
 "command": "grep -n \"date_label\" app/backend/*.py | head; grep -rn \"statement dated\\|statement date\" app/frontend/guided/*.js | cut -c1-180"
}
````

### User / tool · 2026-11-03T04:37:19.117Z

**tool result**
````
app/backend/service_date.py:113:def date_label(kind: str) -> str:
app/backend/service_date.py:122:        return f"{BLANK} ({date_label(kind)} dated {display(statement_iso)})"
app/backend/store.py:144:            "statement_date_iso": rd, "date_label": SD.date_label(kind), "reason": r["reason"], "confirm_note": note}
app/frontend/guided/step3.js:18:  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is cal
app/frontend/guided/step3.js:24:  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? "statement dated " + d : d) : "no 
app/frontend/guided/step3.js:30:  /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
app/frontend/guided/step3.js:33:    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · statement dated ${R.longDate(sd.stat
app/frontend/guided/step3.js:37:    const stmt = /\(statement dated/.test((sd && sd.text) || "") ? " The date in parentheses is the statement date, not the service date." : "";
app/frontend/guided/step3.js:48:    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_r
app/frontend/guided/step3.js:118:      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted state
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:37:26.337Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\nimport re\np=\"step3.js\"; s=open(p).read()\ndef rep(a,b,cnt=1):\n    global s\n    assert s.count(a)==cnt,(a,s.count(a)); s=s.replace(a,b)\nrep('''  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === \"count\" || BILL_DOC.test((rec && rec.source_label) || \"\")));\n  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || \"\"; return d ? (st ? \"statement dated \" + d : d) : \"no date\"; };\n  const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || \"Record\"} · ${recDate(r, st)}`;''',\n'''  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === \"count\" || BILL_DOC.test((rec && rec.source_label) || \"\")));\n  /* T-211 (T-202 r6): service_date.date_label says what the record's date is called: \"statement\" for a bill, \"record\" for any other record. No service_date (a ledger line not counted yet) is a bill document's: \"statement\". */\n  const dateWord = (sd) => (sd && sd.date_label === \"record\" ? \"record\" : \"statement\");\n  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || \"\"; return d ? (st ? st + \" dated \" + d : d) : \"no date\"; };      // st: false, or the word \"statement\" | \"record\"\n  const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || \"Record\"} · ${recDate(r, st)}`;''')\nrep('''` · statement dated ${R.longDate(sd.statement_date_iso)}`''','''` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`''')\nrep('''    const stmt = /\\\\(statement dated/.test((sd && sd.text) || \"\") ? \" The date in parentheses is the statement date, not the service date.\" : \"\";''',\n'''    const paren = /\\\\((statement|record) dated/.exec((sd && sd.text) || \"\"), stmt = paren ? ` The date in parentheses is the ${paren[1]} date, not the service date.` : \"\";''')\nrep('''    const sd = sdOf(item), st = stmtDated(item, sd, rec);''','''    const sd = sdOf(item), st = stmtDated(item, sd, rec) && dateWord(sd);''')\nrep('''head: many ? recLabel(r, stmtDated(item, sd, r)) : null''','''head: many ? recLabel(r, stmtDated(item, sd, r) && dateWord(sd)) : null''')\nrep('''(st ? \"statement dated \" + R.longDate(rec.date_iso) : R.longDate(rec.date_iso))''','''(st ? st + \" dated \" + R.longDate(rec.date_iso) : R.longDate(rec.date_iso))''')\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"stmtOnly(sd)\\|dateWord\" step3.js | cut -c1-200"
}
````

### User / tool · 2026-11-03T04:37:26.457Z

**tool result**
````
23:  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
25:  const dateWord = (sd) => (sd && sd.date_label === "record" ? "record" : "statement");
35:    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`) : null);
46:    const sd = sdOf(item), st = stmtDated(item, sd, rec) && dateWord(sd);
48:    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:37:28.729Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"core.js\"; s=open(p).read()\na='''    trace: (token, s) => call(\"GET\", t(token) + \"/trace\", null, s),'''\nassert a in s\ns=s.replace(a,a+'''\n    itemTrace: (token, id, s) => call(\"GET\", t(token) + \"/items/\" + enc(id) + \"/trace\", null, s),          // T-211: the per-item check trace (\"How this was checked\")''')\nopen(p,\"w\").write(s)\nEOF"
}
````

### User / tool · 2026-11-03T04:37:28.833Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:38:30.244Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"review.js\"; s=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)\n\n# 1. the pure helpers + panel builder, before \"the record, with the highlighted words marked\"\nblock = r'''  /* ---------- T-211 (D-074): \"How this was checked\" on every item: three rows in plain words, from the item's own check trace (GET .../items/<id>/trace; metadata only, no prompts).\n     1 Code check   what code verified (the passed steps with kind \"code\"), or what did not pass.\n     2 Second AI check   a different model with a different prompt: verdict (agrees / disputes / could not check) and the fixed one-line reason the server wrote for its reason code.\n                         A prepared demo answer (D-065) says so first: the team prepared it, then the second AI check read it against the quote.\n     3 You   her decision, or \"Waiting for you\".\n     The code and AI rows come from the trace (fetched once per item version); the You row is drawn at once from the item. A trace that cannot be read says so in the row, never a guess. ---------- */\n  const CODE_PHRASE = [          // [trace step id, what passing it means], in the order they are said; two are shown\n    [\"excerpt_verbatim\", \"the highlighted words are in the record word for word\"], [\"summary_tokens\", \"every number and date in the line is in them\"],\n    [\"found_in_text\", \"the amount appears in the record\"], [\"amount_class\", \"a rule sorted what kind of figure it is\"],\n    [\"computed\", \"the dates and the number of days were worked out by code\"], [\"spans_match\", \"the words it points to are in the record\"],\n    [\"record_warning_check\", \"the wording was found in the record by code\"], [\"date_confirmed\", \"the date comes from the record\"],\n  ];\n  const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);\n  const isCodeStep = (x) => x.kind === \"code\" && (x.status === \"pass\" || x.status === \"fail\");\n  R.howCode = function (tr) {\n    const codes = ((tr && tr.steps) || []).filter(isCodeStep), bad = codes.filter((x) => x.status === \"fail\");\n    if (!codes.length) return { state: \"none\", chip: \"Code: none\", text: \"No code check applies to this item.\", list: [] };\n    const list = codes.map((x) => ({ ok: x.status === \"pass\", label: R.plain(x.label) }));\n    if (bad.length) return { state: \"bad\", chip: \"Code: not passed\", text: \"Did not pass: \" + R.plain(bad[0].why || bad[0].label) + (bad.length > 1 ? ` (and ${bad.length - 1} more)` : \"\"), list };\n    const ok = new Set(codes.map((x) => x.id)), say = CODE_PHRASE.filter(([id]) => ok.has(id)).slice(0, 2).map(([, t]) => t);\n    return { state: \"ok\", chip: \"Code: passed\", text: \"Passed: \" + (say.length ? say.join(\", and \") : `${codes.length} check${codes.length === 1 ? \"\" : \"s\"} by code`) + \".\", list };\n  };\n  const VERDICT = { supported: [\"Agrees\", \"ok\", \"AI: agrees\"], agree: [\"Agrees\", \"ok\", \"AI: agrees\"], agrees: [\"Agrees\", \"ok\", \"AI: agrees\"],\n    partially: [\"Disputes\", \"bad\", \"AI: disputes\"], unsupported: [\"Disputes\", \"bad\", \"AI: disputes\"], disagrees: [\"Disputes\", \"bad\", \"AI: disputes\"], disagree: [\"Disputes\", \"bad\", \"AI: disputes\"],\n    unsure: [\"Could not check\", \"warn\", \"AI: could not check\"], unavailable: [\"Could not check\", \"warn\", \"AI: could not check\"] };\n  R.howJudge = function (tr, item) {\n    const steps = (tr && tr.steps) || [], st = steps.find((x) => x.kind === \"llm\" && x.evidence && x.evidence.model && x.evidence.model.role === \"judge\") || steps.find((x) => /^judge/.test(x.id));\n    const prep = !!(item && item.prepared), lead = prep ? \"Prepared by our team; the second AI check then checked it against the quote (the highlighted words).\" : \"\";\n    if (!st) return { state: \"none\", word: \"Not run\", chip: \"AI: not run\", lead, text: \"No second AI check applies to this item.\", model: \"\" };\n    const ev = st.evidence || {}, m = ev.model && ev.model.id && !ev.model.prepared ? ev.model.id : \"\";\n    const text = R.plain(ev.rationale || st.why || \"\");\n    if (st.status === \"skipped\" && !ev.judge_verdict) return { state: \"none\", word: \"Not needed\", chip: \"AI: not needed\", lead, text, model: \"\" };\n    if (st.status === \"pending\") return { state: \"warn\", word: \"Not run yet\", chip: \"AI: not run yet\", lead, text, model: m };\n    const v = VERDICT[ev.judge_verdict] || (st.status === \"fail\" ? VERDICT.disagrees : VERDICT.supported);\n    return { state: v[1], word: v[0], chip: v[2], lead, text, model: m };\n  };\n  R.howYou = function (S, item) {\n    const t = S.cfg.youText && S.cfg.youText(S, item);\n    if (t) return { state: \"ok\", chip: \"You: decided\", text: t };\n    return { state: \"wait\", chip: \"You: waiting\", text: item.edit_to_check ? \"You changed the wording. Waiting for you to compare it with the highlighted words.\" : \"Waiting for you.\" };\n  };\n  const TRACES = new Map();      // token|item|version -> Promise<trace>. A write changes the version, so the next look asks again. A failed read is forgotten.\n  R.traceOf = function (S, item) {\n    const key = S.token + \"|\" + item.id + \"|\" + item.version;\n    if (!TRACES.has(key)) TRACES.set(key, G.api.itemTrace(S.token, item.id).catch((e) => { TRACES.delete(key); throw e; }));\n    return TRACES.get(key);\n  };\n  R.howOpen = null;      // null until she toggles the panel; then it stays as she left it for the rest of the visit\n'''\nrep(\"  /* ---------- the record, with the highlighted words marked, or its sentences tappable ---------- */\", block + \"\\n  /* ---------- the record, with the highlighted words marked, or its sentences tappable ---------- */\")\n\n# 2. srcCard ref\nrep('''    E.work = h(\"main\", { class: \"work\", id: \"main\", \"data-testid\": \"work\" },\n      h(\"section\", { class: \"card card-src\", \"aria-label\": \"From the record\", \"data-testid\": \"card-src\" }, h(\"div\", { class: \"card-h\" }, h(\"span\", { class: \"ch-title\" }, \"From the record\"), E.srcHead), E.srcBody), E.lineCard);''',\n'''    E.srcCard = h(\"section\", { class: \"card card-src\", \"aria-label\": \"From the record\", \"data-testid\": \"card-src\" }, h(\"div\", { class: \"card-h\" }, h(\"span\", { class: \"ch-title\" }, \"From the record\"), E.srcHead), E.srcBody);\n    E.work = h(\"main\", { class: \"work\", id: \"main\", \"data-testid\": \"work\" }, E.srcCard, E.lineCard);\n    /* T-211: \"How this was checked\" sits under the quote in the record card on a wide screen (it never takes room from the line), and above the footer of the line card on a phone (the record card is already small there) */\n    E.how = h(\"details\", { class: \"how\", \"data-testid\": \"how-checked\", hidden: true });\n    const narrowMQ = matchMedia(\"(max-width: 760px)\");\n    const placeHow = () => { if (narrowMQ.matches) { if (E.how.parentNode !== E.lineCard) E.lineCard.insertBefore(E.how, E.foot); } else if (E.how.parentNode !== E.srcCard) E.srcCard.append(E.how); };\n    narrowMQ.addEventListener(\"change\", placeHow); placeHow();''')\n\n# 3. drawHow in render()\nrep('''      E.question.textContent = sc.question || \"\";\n      drawBtn(E.yes, sc.yes, \"Yes\");''','''      E.question.textContent = sc.question || \"\";\n      drawHow(item, sc);\n      drawBtn(E.yes, sc.yes, \"Yes\");''')\n\ndrawhow = r'''    /* ---- T-211: the three rows ---- */\n    let howTicket = 0;\n    function drawHow(item, sc) {\n      const mine = ++howTicket;\n      if (sc.how === false) { E.how.hidden = true; E.how.replaceChildren(); return; }\n      E.how.hidden = false;\n      const you = R.howYou(S, item);\n      const row = (key, label, sub) => { const v = h(\"div\", { class: \"how-v\", \"data-testid\": \"how-\" + key + \"-text\" }, \"Checking…\"), r = h(\"div\", { class: \"how-r\", \"data-testid\": \"how-\" + key }, h(\"div\", { class: \"how-l\" }, h(\"b\", {}, label), sub ? h(\"span\", { class: \"how-sub\" }, sub) : null), v); return [r, v]; };\n      const [rCode, vCode] = row(\"code\", \"Code check\", \"no AI\"), [rAi, vAi] = row(\"ai\", \"Second AI check\", \"different model and prompt\"), [rYou, vYou] = row(\"you\", \"You\");\n      vYou.textContent = you.text; rYou.dataset.state = you.state;\n      const chip = (key, text, state) => h(\"span\", { class: \"hchip \" + (state || \"\"), \"data-testid\": \"how-chip-\" + key }, text);\n      const cCode = chip(\"code\", \"Code: …\"), cAi = chip(\"ai\", \"AI: …\"), cYou = chip(\"you\", you.chip, you.state);\n      const sum = h(\"summary\", { \"data-testid\": \"how-summary\" }, h(\"span\", { class: \"how-t\" }, \"How this was checked\"), h(\"span\", { class: \"how-chips\" }, cCode, cAi, cYou));\n      E.how.replaceChildren(sum, h(\"div\", { class: \"how-rows\" }, rCode, rAi, rYou));\n      E.how.dataset.item = item.id; E.how.setAttribute(\"aria-busy\", \"true\");\n      E.how.open = R.howOpen == null ? !narrowMQ.matches : R.howOpen;\n      E.how.ontoggle = () => { R.howOpen = E.how.open; };\n      R.traceOf(S, item).then((tr) => {\n        if (mine !== howTicket || !S.alive) return;\n        const c = R.howCode(tr), j = R.howJudge(tr, item);\n        rCode.dataset.state = c.state; cCode.textContent = c.chip; cCode.className = \"hchip \" + c.state;\n        vCode.replaceChildren(c.text, c.list.length ? h(\"details\", { class: \"how-all\", \"data-testid\": \"how-all-checks\" }, h(\"summary\", {}, `All ${c.list.length} check${c.list.length === 1 ? \"\" : \"s\"}`),\n          h(\"ul\", {}, c.list.map((x) => h(\"li\", { class: x.ok ? \"ok\" : \"bad\" }, h(\"span\", { \"aria-hidden\": \"true\" }, x.ok ? \"✓ \" : \"✗ \"), h(\"span\", { class: \"sr\" }, x.ok ? \"Passed: \" : \"Did not pass: \"), x.label)))) : null);\n        rAi.dataset.state = j.state; cAi.textContent = j.chip; cAi.className = \"hchip \" + j.state;\n        vAi.replaceChildren(...[j.lead ? h(\"p\", { class: \"how-lead\", \"data-testid\": \"how-prepared\" }, j.lead) : null, h(\"p\", {}, h(\"b\", { class: \"how-verdict \" + j.state, \"data-testid\": \"how-verdict\" }, j.word), j.text ? \" \" + j.text : \"\"),\n          j.model ? h(\"p\", { class: \"how-model\", \"data-testid\": \"how-model\" }, \"Read by \" + j.model + \", not the model or person that wrote the first answer.\") : null].filter(Boolean));\n        E.how.removeAttribute(\"aria-busy\");\n      }).catch((e) => {\n        if (mine !== howTicket || !S.alive || (e && e.name === \"AbortError\")) return;\n        for (const [v, c, k] of [[vCode, cCode, \"Code\"], [vAi, cAi, \"AI\"]]) { v.textContent = \"We couldn't load this just now.\"; c.textContent = k + \": –\"; }\n        E.how.removeAttribute(\"aria-busy\");\n      });\n    }\n'''\nrep(\"    function renderSource(keep) {\", drawhow + \"    function renderSource(keep) {\")\nrep('''    return function cleanup() { S.alive = false;''','''    return function cleanup() { narrowMQ.removeEventListener(\"change\", placeHow); S.alive = false;''')\nopen(p,\"w\").write(s)\nEOF"
}
````

### User / tool · 2026-11-03T04:38:30.351Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:38:37.005Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"review.js\"; s=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)\nrep('''const ev = st.evidence || {}, m = ev.model && ev.model.id && !ev.model.prepared ? ev.model.id : \"\";''','''const ev = st.evidence || {}, m = ev.model && ev.model.id && !ev.model.prepared ? ev.model.id + (ev.prompt_version ? ` · prompt ${ev.prompt_version}` : \"\") : \"\";''')\nrep('''h(\"p\", { class: \"how-model\", \"data-testid\": \"how-model\" }, \"Read by \" + j.model + \", not the model or person that wrote the first answer.\")''','''h(\"p\", { class: \"how-model\", \"data-testid\": \"how-model\" }, \"Model \" + j.model)''')\nrep('''row(\"ai\", \"Second AI check\", \"different model and prompt\")''','''row(\"ai\", \"Second AI check\", \"separate model and prompt\")''')\nopen(p,\"w\").write(s)\nEOF"
}
````

### User / tool · 2026-11-03T04:38:37.106Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:38:44.464Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\n\nedit(\"step2.js\",[\n('''      tag: { cls: \"you\", text: \"Your wording\" }, sub: lineHead(item, rec), focus: \"field\",''','''      tag: { cls: \"you\", text: \"Your wording\" }, sub: lineHead(item, rec), focus: \"field\", how: false,'''),\n('''      return { ...tags, focus: \"field\", body: [h(\"p\", { class: \"warn-title\" }, \"Add a note for the attorney\"), ta],''','''      return { ...tags, focus: \"field\", how: false, body: [h(\"p\", { class: \"warn-title\" }, \"Add a note for the attorney\"), ta],'''),\n('''      return { tag: { cls: \"you\", text: \"Written by you\" }, sub: recLabel(rec), focus: \"field\",''','''      return { tag: { cls: \"you\", text: \"Written by you\" }, sub: recLabel(rec), focus: \"field\", how: false,'''),\n('''  /* what the Saved line says */''','''  /* T-211: the \"You\" row of \"How this was checked\": her decision in words (null = no decision yet) */\n  function youText(S, item) {\n    const st = item.review_status, flag = groupOf(S.c, item) === \"flag\" || item.kind === \"flag\" || !!item.type, tray = groupOf(S.c, item) === \"tray\";\n    if (item.edit_to_check || !st || st === \"pending\") return null;\n    if (st === \"dismissed\") return tray ? \"You skipped it.\" : flag ? \"You said the attorney does not need to be told.\" : \"You left it out of the letter.\";\n    if (st === \"edited\") return flag ? \"You added a note. The attorney will be told.\" : \"You wrote your own wording and kept it in the letter.\";\n    return flag ? \"You said the attorney should be told.\" : \"You kept it in the letter.\";\n  }\n\n  /* what the Saved line says */'''),\n('''buildQueue, find, present, statusFor, done, empty });\n  };\n  G.step2''','''buildQueue, find, present, statusFor, done, empty, youText });\n  };\n  G.step2'''),\n])\nedit(\"step3.js\",[\n('''  function statusFor(S, item, resp, action) {''','''  /* T-211: the \"You\" row of \"How this was checked\" (null = no decision yet) */\n  function youText(S, item) {\n    const st = item.review_status, k = kindOf(item);\n    if (!st || st === \"pending\") return null;\n    if (st === \"dismissed\") return k === \"charge\" ? \"You chose not to count it.\" : k === \"count\" ? \"You left it out of the notes.\" : \"You left it out of the notes for the attorney.\";\n    return k === \"charge\" ? \"You counted it in the bill total.\" : k === \"count\" ? \"You did not count it. It is noted for the attorney.\" : \"You listed it in the notes for the attorney. It is never added to the total.\";\n  }\n\n  function statusFor(S, item, resp, action) {'''),\n('''buildQueue, find, present, statusFor, done, empty });''','''buildQueue, find, present, statusFor, done, empty, youText });'''),\n])\nEOF\ngrep -n \"youText\" step2.js step3.js | cut -c1-120"
}
````

### User / tool · 2026-11-03T04:38:44.597Z

**tool result**
````
step3.js:104:  function youText(S, item) {
step3.js:161:    return R.run(ctx, { step: 3, title: "Check the bills", unit: "Amount", chip: true, buildQueue, find, pr
step2.js:331:  function youText(S, item) {
step2.js:393:    return R.run(ctx, { step: 2, title: "Check the timeline", unit: "Item", chip: false, buildQueue, find,
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:39:08.109Z

**tool call — Bash**
````
{
 "command": "ls app/backend/grounding.py app/backend/judges.py app/backend/judge_guard.py app/llm/prompts/judge_faithfulness_v1.md evals/ docs/LLM_VS_CODE.md memory/ORCHESTRATOR_DECISIONS.md >/dev/null && echo ok; ls evals | head -20; cp submission/validation-ladder.svg app/frontend/guided/validation-ladder.svg; cat app/frontend/guided/home.js | sed -n 1,30p | cut -c1-200"
}
````

### User / tool · 2026-11-03T04:39:08.219Z

**tool result**
````
ok
__init__.py
__pycache__
adversarial
finalize_prompt_log.py
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
privacy_tree_scan.py
reports
run.py
/* Your cases (/). T-181, D-068, spec section 3. Builder A.
   Local mode: GET /api/cases lists every case. Public/demo mode: that route is 404 by design, so the list is the cases THIS BROWSER started (tokens kept in localStorage by G.cases,
   try/catch), each read with GET /api/cases/{token}. One definition of the Next line and the Continue target (spec 3.2) for both sources.
   Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, case-card (data-token, data-title), case-next, btn-continue, btn-rename, btn-delete, btn-delete-yes, btn-delete-kee
   rename-input, btn-rename-save, btn-rename-cancel, btn-remove-gone, find-case, cases-mode, page-error, btn-retry. Text only (textContent); no inline style attributes. */
(function () {
  const G = window.G, { h } = G;

  /* ---- the cases this browser started (public mode). Shared with step1.js. Never throws: storage can be blocked. ---- */
  const KEY = "zl.guided.cases";
  G.cases = {
    list() { try { const v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v.filter((t) => typeof t === "string") : []; } catch (_) { return []; } },
    add(token) { try { const l = G.cases.list().filter((t) => t !== token); l.unshift(token); localStorage.setItem(KEY, JSON.stringify(l.slice(0, 100))); } catch (_) { /* not remembered */ } },
    remove(token) { try { localStorage.setItem(KEY, JSON.stringify(G.cases.list().filter((t) => t !== token))); } catch (_) { /* not remembered */ } },
  };

  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren turns null into the text "null"
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;
  const day = (iso) => { const d = new Date(iso); return isNaN(d) ? "" : d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); };
  const track = ["Add records", "Timeline", "Bills", "Letter"];

  /* ---- one view-model for a /api/cases row or a GET case JSON ---- */
  function fromRow(c) {
    const p = c.progress || {}, e = p.entries || { decided: 0, total: 0 }, f = p.flags || { decided: 0, total: 0 }, a = p.amounts || { decided: 0, total: 0 };
    const run = c.run || {};
    return { token: c.token, title: c.title || c.name || "Case", created: c.created_at, activity: c.last_activity_at || c.updated_at || c.created_at, records: c.record_count, status: c.status,
      stage: run.steps_done != null ? Math.min(run.steps_done + 1, run.steps_total || 8) : null, stages: run.steps_total || 8,
      err: !!c.status_error, errMsg: c.status_error_message || "We couldn't load this case's status",
      s2: { total: e.total + f.total, left: e.total + f.total - e.decided - f.decided }, s3: { total: a.total, left: a.total - a.decided },
      ready: !!c.export_ready, next: c.next_action, problems: c.hitl && c.hitl.gate_blockers ? c.hitl.gate_blockers.length : null, src: c };
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:39:25.638Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/how.js",
 "content": "/* \"How each answer is checked\" (/how-it-works). T-211, D-074. Reachable from the header on every screen (app.js draws the link).\n   A plain explanation of the validation ladder for a first-time reader: draft (AI, or prepared answers in the demo) -> code checks -> an independent second AI check -> you decide. What is code and what is AI, with the repo's doc names in text.\n   The wording about who drafted follows the same provenance rule as the rest of the app (G.provenance, D-065): a prepared demo never says an AI wrote the answers.\n   Page contract: G.pages.how = async (ctx) => cleanup. Text only (textContent); no inline style attributes. Test ids: how-page, how-steps, how-step-1..4, how-ladder-img, how-ladder-open, how-code-vs-ai, how-repo, how-back. */\n(function () {\n  const G = window.G, { h } = G;\n\n  const code = (t) => h(\"code\", {}, t);\n\n  G.pages.how = async function (ctx) {\n    await G.healthNow(ctx.signal);\n    const p = G.provenance();\n    const draft = p.kind === \"prepared\"\n      ? [\"Prepared by our team. \", \"In this demo the sample answers were written ahead of time, not by an AI model. A real run has an AI model draft a one-line summary of each record and pick the exact words it came from.\"]\n      : p.kind === \"recorded\"\n        ? [\"Drafted by an AI model. \", \"An AI model drafted a one-line summary of each record and picked the exact words it came from. In this demo those answers were recorded earlier.\"]\n        : [\"Drafted by an AI model. \", \"An AI model reads each record, drafts a one-line summary and picks the exact words it came from.\"];\n    const back = h(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": \"how-back\", onclick: () => { if (history.length > 1) history.back(); else ctx.go(\"/\"); } }, \"‹ Back\");\n    const step = (n, head, body) => h(\"li\", { \"data-testid\": \"how-step-\" + n }, h(\"span\", { class: \"how-n\", \"aria-hidden\": \"true\" }, String(n)), h(\"div\", {}, h(\"b\", {}, head), \" \", body));\n\n    ctx.view.append(h(\"main\", { class: \"wrap how-page\", id: \"main\", \"data-testid\": \"how-page\" },\n      h(\"div\", { class: \"page-h\" }, h(\"div\", { class: \"ph-main\" }, h(\"h1\", { \"data-testid\": \"page-title\" }, \"How each answer is checked\"),\n        h(\"p\", {}, \"Nothing reaches your letter until code has checked it, a second AI has checked it, and you have said yes.\")), back),\n      h(\"div\", { class: \"panel\" },\n        h(\"ol\", { class: \"how-steps\", \"data-testid\": \"how-steps\" },\n          step(1, draft[0], draft[1]),\n          step(2, \"Code checks it.\", \"Plain code, not AI, confirms the quote is in the record word for word and that every date, amount and number in the line is in the quote. Dates, gaps and totals are worked out by code alone.\"),\n          step(3, \"A second AI checks it.\", \"A different model, with a different prompt, reads the record and the answer. It says it agrees, disputes it or could not check, with a one-line reason. If it disputes, you must confirm you compared the line with the quote.\"),\n          step(4, \"You decide.\", \"You accept, edit or dismiss every item. Code builds the letter from what you accepted, and nothing else.\")),\n        h(\"p\", { class: \"muted how-note\" }, \"Each item in steps 2 and 3 shows these three checks under “How this was checked”. The second AI can be wrong too, which is why the last word is yours.\")),\n      h(\"div\", { class: \"panel\" }, h(\"h2\", {}, \"The checks, as a picture\"),\n        h(\"div\", { class: \"how-fig\", tabindex: \"0\", role: \"group\", \"aria-label\": \"The validation ladder picture. It scrolls sideways on a narrow screen.\" },\n          h(\"img\", { src: \"/validation-ladder.svg\", width: \"820\", height: \"600\", alt: \"Validation ladder. A record goes to a draft. Rung 1, code, checks the quote word for word and every number. Rung 2, a second AI with a different prompt, agrees, disputes or could not check. Rung 3, you accept, edit or dismiss. Code builds the export from accepted items only. Items that fail a check go to a could-not-verify list and never reach the letter.\", \"data-testid\": \"how-ladder-img\" })),\n        h(\"p\", { class: \"muted how-note\" }, h(\"a\", { href: \"/validation-ladder.svg\", target: \"_blank\", rel: \"noopener\", \"data-testid\": \"how-ladder-open\" }, \"Open the picture full size\"), \" (it opens in a new tab).\")),\n      h(\"div\", { class: \"panel\", \"data-testid\": \"how-code-vs-ai\" }, h(\"h2\", {}, \"What is code and what is AI\"),\n        h(\"div\", { class: \"how-cols\" },\n          h(\"div\", {}, h(\"h3\", {}, \"Code only, never AI\"),\n            h(\"ul\", {}, h(\"li\", {}, \"Splitting the pasted text into records\"), h(\"li\", {}, \"Reading dates, and the days between visits\"), h(\"li\", {}, \"Finding every dollar amount, saying what kind it is, and adding up the total\"),\n              h(\"li\", {}, \"Checking that a quote is in the record word for word, and that its numbers are in the quote\"), h(\"li\", {}, \"The wording of each warning, sorting, and building the letter\"))),\n          h(\"div\", {}, h(\"h3\", {}, \"AI, always checked\"),\n            h(\"ul\", {}, h(\"li\", {}, \"Drafting a one-line summary and picking the quote\" + (p.kind === \"prepared\" ? \" (prepared by our team in this demo)\" : \"\")), h(\"li\", {}, \"The second check that reads each answer against the record\"),\n              h(\"li\", {}, \"Spotting wording the other side could use, which code then checks and you decide\"))))),\n      h(\"div\", { class: \"panel\", \"data-testid\": \"how-repo\" }, h(\"h2\", {}, \"Where to read more in the repo\"),\n        h(\"ul\", { class: \"how-repo\" },\n          h(\"li\", {}, code(\"docs/LLM_VS_CODE.md\"), \": every step, whether it is code or AI, and how it is checked.\"),\n          h(\"li\", {}, code(\"app/llm/prompts/\"), \": the second check's prompts, for example \", code(\"judge_faithfulness_v1.md\"), \" and \", code(\"judge_amount_class_v1.md\"), \".\"),\n          h(\"li\", {}, code(\"app/backend/grounding.py\"), \": the word-for-word and number checks. \", code(\"app/backend/judges.py\"), \": how the second AI's answer becomes a verdict.\"),\n          h(\"li\", {}, code(\"evals/\"), \": the golden cases and reports that measure both checks.\"),\n          h(\"li\", {}, code(\"memory/ORCHESTRATOR_DECISIONS.md\"), \": D-065 (prepared answers are never called AI output) and D-066 (a disputed line needs your comparison).\")),\n        h(\"div\", { class: \"row-actions\" }, h(\"a\", { class: \"btn primary lg\", href: \"/\", \"data-testid\": \"how-home\" }, \"Back to your cases\")))));\n    ctx.setTitle(\"How each answer is checked\");\n    return undefined;\n  };\n})();\n"
}
````

### User / tool · 2026-11-03T04:39:25.692Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/frontend/guided/how.js (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:39:43.159Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && cat > how.css <<'EOF'\n/* T-211 (D-074): the header link, the \"How this was checked\" panel on Step 2 and 3 items, and the \"How each answer is checked\" page. OWNER: frontend. Loaded last. Tokens only; no inline styles. */\n\n/* ---------- header link (every screen) ---------- */\n.how-link { display: inline-flex; align-items: center; height: 44px; padding: 0 14px; border-radius: 10px; border: 1px solid var(--border-strong); background: var(--panel); color: var(--text);\n  font: 600 .9375rem var(--font); text-decoration: none; white-space: nowrap; flex: none; }\n.how-link:hover { background: var(--sunken); }\n.how-link[aria-current=\"page\"] { border-color: var(--accent); background: var(--accent-soft); }\n.how-link .short { display: none; }\n@media (max-width: 1100px) { .how-link .long { display: none; } .how-link .short { display: inline; } }\n@media (max-width: 760px) { .how-link { height: 40px; padding: 0 10px; font-size: .875rem; } }\n\n/* ---------- the panel: three rows ---------- */\n.how { flex: none; border-top: 1px solid var(--border); background: var(--sunken); font-size: .9375rem; line-height: 1.35rem; color: var(--text); }\n.how > summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 8px 12px; flex-wrap: wrap; padding: 8px 24px; min-height: 40px; }\n.how > summary::-webkit-details-marker { display: none; }\n.how > summary::before { content: \"\\25B8\"; color: var(--muted); flex: none; font-size: .875rem; }\n.how[open] > summary::before { content: \"\\25BE\"; }\n.how-t { font-weight: 700; font-size: .9375rem; }\n.how-chips { display: inline-flex; gap: 6px; flex-wrap: wrap; }\n.how[open] .how-chips { display: none; }\n.hchip { display: inline-flex; align-items: center; height: 24px; padding: 0 10px; border-radius: 999px; font-size: .8125rem; font-weight: 700; white-space: nowrap; background: var(--panel); border: 1px solid var(--border); color: var(--muted); }\n.hchip.ok { background: var(--ok-bg); color: var(--ok); border-color: transparent; }\n.hchip.bad { background: var(--bad-bg); color: var(--bad); border-color: transparent; }\n.hchip.warn, .hchip.wait { background: var(--warn-bg); color: var(--warn); border-color: var(--warn-edge); }\n.how-rows { padding: 0 24px 10px; display: grid; gap: 6px; }\n.how-r { display: grid; grid-template-columns: 9.25rem minmax(0, 1fr); gap: 4px 14px; align-items: start; }\n.how-l b { display: block; font-weight: 700; }\n.how-sub { display: block; font-size: .75rem; line-height: 1rem; color: var(--muted); }\n.how-v { color: var(--text); overflow-wrap: anywhere; min-height: 1.35rem; }\n.how-v p { margin: 0; }\n.how-v p + p { margin-top: 2px; }\n.how-lead { font-weight: 600; }\n.how-verdict { font-weight: 800; }\n.how-verdict.ok, .how-r[data-state=\"ok\"] .how-v:not(.x) { color: inherit; }\n.how-verdict.ok { color: var(--ok); }\n.how-verdict.bad { color: var(--bad); }\n.how-verdict.warn { color: var(--warn); }\n.how-r[data-state=\"bad\"] > .how-v { color: var(--bad); font-weight: 600; }\n.how-model { font-size: .8125rem; color: var(--muted); overflow-wrap: anywhere; }\n.how-all { margin-top: 2px; }\n.how-all > summary { cursor: pointer; color: var(--accent); font-size: .875rem; font-weight: 600; width: max-content; }\n.how-all ul { list-style: none; margin: 4px 0 0; padding: 0; font-size: .875rem; line-height: 1.25rem; color: var(--muted); }\n.how-all li.ok span:first-child { color: var(--ok); font-weight: 800; }\n.how-all li.bad { color: var(--bad); }\n\n@media (max-width: 760px) {\n  .how > summary { padding: 6px 14px; min-height: 36px; gap: 4px 8px; }\n  .how-t { font-size: .8125rem; }\n  .hchip { height: 22px; padding: 0 8px; font-size: .75rem; }\n  .how-rows { padding: 0 14px 8px; max-height: 9.5rem; overflow: auto; font-size: .875rem; line-height: 1.25rem; }\n  .how-r { grid-template-columns: 5.75rem minmax(0, 1fr); gap: 2px 8px; }\n  .how-sub { display: none; }\n}\n\n/* ---------- the page ---------- */\n.how-page .how-steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; }\n.how-page .how-steps li { display: grid; grid-template-columns: 40px minmax(0, 1fr); gap: 14px; align-items: start; }\n.how-n { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: var(--on-accent); display: grid; place-items: center; font-weight: 800; }\n.how-page .how-note { margin-top: 16px; font-size: 1rem; line-height: 1.5rem; }\n.how-fig { overflow-x: auto; border: 1px solid var(--border); border-radius: 12px; background: #fff; margin-top: 8px; }\n.how-fig img { display: block; width: 100%; height: auto; min-width: 640px; max-width: 820px; margin: 0 auto; }\n.how-cols { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; margin-top: 8px; }\n.how-cols h3 { font-size: 1.0625rem; margin-bottom: 6px; }\n.how-cols ul, .how-repo { margin: 0; padding-left: 20px; display: grid; gap: 6px; }\n.how-repo code, .how-page code { font: 600 .9375em ui-monospace, SFMono-Regular, Menlo, monospace; background: var(--sunken); padding: 1px 6px; border-radius: 6px; overflow-wrap: anywhere; }\n@media (max-width: 760px) {\n  .how-cols { grid-template-columns: 1fr; gap: 16px; }\n  .how-page .page-h { flex-direction: column; align-items: stretch; }\n  .how-page .page-h .btn { align-self: flex-start; }\n}\nEOF\npython3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\nedit(\"index.html\",[\n('<link rel=\"stylesheet\" href=\"/step4.css\">','<link rel=\"stylesheet\" href=\"/step4.css\">\\n<link rel=\"stylesheet\" href=\"/how.css\">'),\n('<script src=\"/step4.js\"></script>','<script src=\"/step4.js\"></script>\\n<script src=\"/how.js\"></script>'),\n])\nedit(\"app.js\",[\n('''     /case/<token>/letter      G.pages.letter    layout page   (step 4)''','''     /case/<token>/letter      G.pages.letter    layout page   (step 4)\n     /how-it-works             G.pages.how       layout page   (T-211: \"How each answer is checked\"; linked from the header on every screen; no step bar)'''),\n('''    [/^\\\\/$/, \"home\", 0], [/^\\\\/new$/, \"new\", 1],''','''    [/^\\\\/$/, \"home\", 0], [/^\\\\/new$/, \"new\", 1], [/^\\\\/how-it-works$/, \"how\", 0],'''),\n('''    headerEl.replaceChildren(...[].concat(left), h(\"span\", { class: \"spacer\" }), ...(p.label''','''    const how = h(\"a\", { class: \"how-link\", href: \"/how-it-works\", \"data-testid\": \"link-how\", \"aria-current\": now && now.name === \"how\" ? \"page\" : null },\n      h(\"span\", { class: \"long\" }, \"How each answer is checked\"), h(\"span\", { class: \"short\" }, \"How it's checked\"));      // T-211, D-074: on every screen\n    headerEl.replaceChildren(...[].concat(left), h(\"span\", { class: \"spacer\" }), ...(p.label'''),\n('''...(p.label ? [h(\"span\", { class: \"demo-pill\", \"data-testid\": \"demo-badge\", title: p.note }, p.label)] : []), themeButton());''','''...(p.label ? [h(\"span\", { class: \"demo-pill\", \"data-testid\": \"demo-badge\", title: p.note }, p.label)] : []), how, themeButton());'''),\n])\nEOF\ngrep -n \"now = null\\|let ctrl\" app.js | head"
}
````

### User / tool · 2026-11-03T04:39:43.327Z

**tool result**
````
95:  let ctrl = null, cleanup = null, ticket = 0, first = true, now = null;
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:39:48.952Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"how.css\"; s=open(p).read()\ns=s.replace('.how-verdict.ok, .how-r[data-state=\"ok\"] .how-v:not(.x) { color: inherit; }\\n','')\nopen(p,\"w\").write(s)\nEOF\ncurl -s localhost:7860/how.js | head -c 100; echo; curl -s -o /dev/null -w \"%{http_code} %{content_type}\\n\" localhost:7860/validation-ladder.svg; curl -s -o /dev/null -w \"%{http_code}\\n\" localhost:7860/how-it-works"
}
````

### User / tool · 2026-11-03T04:39:49.235Z

**tool result**
````
/* "How each answer is checked" (/how-it-works). T-211, D-074. Reachable from the header on every sc
200 image/svg+xml
200
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:39:53.247Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/scratch211 && cd /Users/arsis/zlayt-pm-project && cat > /private/tmp/claude-501/scratch211/shot.py <<'EOF'\nimport sys, json\nfrom playwright.sync_api import sync_playwright\nTOK = sys.argv[1]\nout = \"/private/tmp/claude-501/scratch211/\"\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in ((1440, 900), (390, 844)):\n        ctx = b.new_context(viewport={\"width\": w, \"height\": h})\n        pg = ctx.new_page(); errs = []\n        pg.on(\"console\", lambda m: errs.append(m.text) if m.type == \"error\" else None); pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n        for path, name in ((f\"/case/{TOK}/timeline?item=e1\", \"e1\"), (f\"/case/{TOK}/bills?item=a1\", \"a1\"), (f\"/case/{TOK}/timeline?item=f_gap_r6_r7\", \"gap\"), (\"/how-it-works\", \"how\")):\n            pg.goto(\"http://localhost:7860\" + path); pg.wait_for_selector(\"#view[data-ready]\"); pg.wait_for_timeout(500)\n            pg.screenshot(path=f\"{out}{name}-{w}.png\", full_page=(name == \"how\"))\n        print(w, errs)\n    b.close()\nEOF\n.venv/bin/python /private/tmp/claude-501/scratch211/shot.py EXNPq1Q1Uese0eB-92gyCg"
}
````

### User / tool · 2026-11-03T04:39:58.887Z

**tool result**
````
1440 []
390 []
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:40:00.562Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/e1-1440.png"
}
````

### User / tool · 2026-11-03T04:40:00.580Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:40:00.717Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/e1-390.png"
}
````

### User / tool · 2026-11-03T04:40:00.725Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:40:31.791Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch211/m.py <<'EOF'\nimport sys, json\nfrom playwright.sync_api import sync_playwright\nTOK = sys.argv[1]\nwith sync_playwright() as p:\n    b = p.chromium.launch(); ctx = b.new_context(viewport={\"width\": 390, \"height\": 844}); pg = ctx.new_page()\n    pg.goto(f\"http://localhost:7860/case/{TOK}/timeline?item=e1\"); pg.wait_for_selector(\"#view[data-ready]\"); pg.wait_for_timeout(500)\n    js = \"(sel)=>{const e=document.querySelector(sel);const r=e.getBoundingClientRect();return [Math.round(r.top),Math.round(r.height)]}\"\n    for s in (\"[data-testid=work]\",\"[data-testid=card-src]\",\"[data-testid=card-line]\",\"[data-testid=line-body]\",\"[data-testid=how-checked]\",\"[data-testid=card-foot]\",\"[data-testid=actions]\"):\n        print(s, pg.evaluate(js, s))\n    pg.evaluate(\"document.querySelector('[data-testid=how-checked]').hidden=true\")\n    print(\"hidden:\")\n    for s in (\"[data-testid=work]\",\"[data-testid=card-src]\",\"[data-testid=card-line]\"):\n        print(s, pg.evaluate(js, s))\n    b.close()\nEOF\n.venv/bin/python /private/tmp/claude-501/scratch211/m.py EXNPq1Q1Uese0eB-92gyCg"
}
````

### User / tool · 2026-11-03T04:40:32.993Z

**tool result**
````
[data-testid=work] [152, 507]
[data-testid=card-src] [152, 273]
[data-testid=card-line] [433, 218]
[data-testid=line-body] [512, 120]
[data-testid=how-checked] [632, 61]
[data-testid=card-foot] [693, 104]
[data-testid=actions] [659, 185]
hidden:
[data-testid=work] [152, 507]
[data-testid=card-src] [152, 273]
[data-testid=card-line] [433, 218]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:40:36.969Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && sed -n 60,110p review.css"
}
````

### User / tool · 2026-11-03T04:40:37.062Z

**tool result**
````
  body.frame { grid-template-rows: var(--banner-h) var(--header-h) 0 var(--title-h) minmax(0, 1fr) auto; }
  body.frame .steps { height: 0; padding: 0; border: 0; position: relative; z-index: 30; overflow: visible; }
  body.frame .steps ol { display: none; }
  body.frame.steps-open .steps ol { display: grid; position: absolute; top: 0; left: 0; right: 0; height: calc(var(--steps-h) + 36px); padding: 36px 8px 0; box-sizing: border-box; background: var(--panel); border-bottom: 1px solid var(--border); box-shadow: var(--shadow-bar); }
  :root { --title-h: 56px; }
  .titlebar { align-items: center; padding-bottom: 0; }
  .titlebar .t-main { display: flex; flex-direction: column; justify-content: center; }
  .titlebar h1 { font-size: 1.125rem; line-height: 1.5rem; }
  .steps-toggle { display: inline-flex; align-items: center; align-self: flex-start; height: 28px; padding: 0 10px 0 0; border: 0; background: transparent; color: var(--accent); font: 700 .8125rem var(--font); cursor: pointer; }
  body.steps-open .steps-toggle { position: relative; z-index: 40; }      /* the overlay leaves the top band free: tapping the toggle again closes the list (UX review T-181 major) */
  .steps-toggle:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  .titlebar:has(.total-chip) .t-main { display: flex; }
  .titlebar:has(.total-chip) .total-chip { flex: none; }
  .titlebar:has(.total-chip) h1 { display: none; }
  .titlebar:has(.total-chip) .count-box { width: 120px; }
  .titlebar .total-chip { width: auto; padding: 2px 10px; }
  .titlebar .total-chip .tc-v { font-size: 1rem; }
  /* the record gets the larger share; the line card scrolls as one box so its footer (a tick box, a refusal) is never cut off by a fixed row */
  body.frame .work { grid-template-rows: minmax(0, 1.25fr) minmax(0, 1fr); gap: 8px; }
  body.frame .work.needs-check { grid-template-rows: minmax(0, .8fr) minmax(0, 1.2fr); }      /* the record window holds the highlighted words with a line of context either side (UX r2 major); the line card still shows the line and its tick box */
  body.frame .work.needs-check .card-line .card-h { flex-wrap: nowrap; min-height: 0; padding-top: 8px; padding-bottom: 8px; }
  body.frame .work.needs-check .card-line .card-h .ch-sub { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; flex: 1 1 0; }
  body.frame .work.needs-check .card-line .card-b { padding-top: 10px; padding-bottom: 6px; }
  body.frame .work.needs-check .card-line .card-f { padding-top: 8px; padding-bottom: 8px; }      /* a line to compare + its tick box: both on screen together */
  .card-line { overflow: auto; }
  .card-line .card-b { flex: none; overflow: visible; }
  .card-line .card-f, .card-f.plain { flex: none; height: auto; min-height: 0; display: block; -webkit-line-clamp: unset; overflow: visible; }
  .card-line .card-h { position: sticky; top: 0; z-index: 2; background: var(--panel); flex-wrap: wrap; row-gap: 4px; }
  .card-src .card-h { min-height: 40px; padding: 6px 12px; }
  .card-src .card-h .ch-sub { font-size: .8125rem; }
  .actions-in { padding: 6px 12px 4px; row-gap: 4px; }
  .question { min-height: 2.4rem; font-size: .9375rem; line-height: 1.2rem; }
  .btn.answer { height: 50px; font-size: 1rem; }
  .small .btn { height: 38px; }
  .actions .status { min-height: 36px; font-size: .8125rem; line-height: 1.1rem; }
  .actions .status .st-msg { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; white-space: normal; }
  .actions .status .undo { height: 34px; padding: 0 12px; }
  .card-b .line-text { font-size: 1.0625rem; line-height: 1.5rem; }
}
@media (max-width: 760px) and (max-height: 720px) {
  body.frame .work { grid-template-rows: none; }
  .card-line { overflow: visible; }
  .card-line .card-h { position: static; }
  .card-line .card-f { scroll-margin-bottom: 200px; }      /* the page scrolls here: a refusal scrolled into view stops above the action bar */
}

/* ---------- words of a line that are not in the highlighted words (underlined by code) ---------- */
.line-text u.out { text-decoration: underline wavy var(--warn, #b45309); text-decoration-thickness: 2px; text-underline-offset: 3px; }
.out-note { margin: 6px 0 0; font-size: .875rem; }
.also q { display: block; }
.btn.src-toggle { height: auto; min-height: 0; padding: 0; margin: 0 0 8px; font-size: .875rem; font-weight: 600; justify-content: flex-start; text-decoration: underline; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:41:02.827Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\nedit(\"review.js\",[\n# phrases\n('''[\"summary_tokens\", \"every number and date in the line is in them\"]''','''[\"summary_tokens\", \"the line's numbers and dates are in them\"]'''),\n# lead shorter\n('''\"Prepared by our team; the second AI check then checked it against the quote (the highlighted words).\"''','''\"Prepared by our team; the second AI check then checked it against the quote.\"'''),\n# strip prefix\n('''    const text = R.plain(ev.rationale || st.why || \"\");''','''    const text = cap(R.plain(ev.rationale || st.why || \"\").replace(/^A second AI check (?:also )?/, \"\"));          // the row is already headed \"Second AI check\"'''),\n# phone placement: after the foot\n('''const placeHow = () => { if (narrowMQ.matches) { if (E.how.parentNode !== E.lineCard) E.lineCard.insertBefore(E.how, E.foot); } else if (E.how.parentNode !== E.srcCard) E.srcCard.append(E.how); };''',\n '''const placeHow = () => { const into = narrowMQ.matches ? E.lineCard : E.srcCard; if (E.how.parentNode !== into) into.append(E.how); };'''),\n('''and above the footer of the line card on a phone (the record card is already small there) */''','''and at the end of the line card on a phone (that card scrolls as one box; the footer with its tick box stays beside the line) */'''),\n# open default\n('''E.how.open = R.howOpen == null ? !narrowMQ.matches : R.howOpen;''','''E.how.open = R.howOpen == null ? !narrowMQ.matches && window.innerHeight >= 840 : R.howOpen;          // closed (chips only) on a phone and on a short window until she opens it'''),\n# label subs\n('''row(\"code\", \"Code check\", \"no AI\"), [rAi, vAi] = row(\"ai\", \"Second AI check\", \"separate model and prompt\")''','''row(\"code\", \"Code check\", \"no AI\"), [rAi, vAi, sAi] = row(\"ai\", \"Second AI check\", \"own model and prompt\")'''),\n('''const row = (key, label, sub) => { const v = h(\"div\", { class: \"how-v\", \"data-testid\": \"how-\" + key + \"-text\" }, \"Checking…\"), r = h(\"div\", { class: \"how-r\", \"data-testid\": \"how-\" + key }, h(\"div\", { class: \"how-l\" }, h(\"b\", {}, label), sub ? h(\"span\", { class: \"how-sub\" }, sub) : null), v); return [r, v]; };''',\n '''const row = (key, label, sub) => { const v = h(\"div\", { class: \"how-v\", \"data-testid\": \"how-\" + key + \"-text\" }, \"Checking…\"), s = sub ? h(\"span\", { class: \"how-sub\", \"data-testid\": \"how-\" + key + \"-sub\" }, sub) : null, r = h(\"div\", { class: \"how-r\", \"data-testid\": \"how-\" + key }, h(\"div\", { class: \"how-l\" }, h(\"b\", {}, label), s), v); return [r, v, s]; };'''),\n# code row: toggle instead of details\n('''        vCode.replaceChildren(c.text, c.list.length ? h(\"details\", { class: \"how-all\", \"data-testid\": \"how-all-checks\" }, h(\"summary\", {}, `All ${c.list.length} check${c.list.length === 1 ? \"\" : \"s\"}`),\n          h(\"ul\", {}, c.list.map((x) => h(\"li\", { class: x.ok ? \"ok\" : \"bad\" }, h(\"span\", { \"aria-hidden\": \"true\" }, x.ok ? \"✓ \" : \"✗ \"), h(\"span\", { class: \"sr\" }, x.ok ? \"Passed: \" : \"Did not pass: \"), x.label)))) : null);''',\n '''        const ul = h(\"ul\", { class: \"how-all\", \"data-testid\": \"how-all-list\", hidden: true }, c.list.map((x) => h(\"li\", { class: x.ok ? \"ok\" : \"bad\" }, h(\"span\", { \"aria-hidden\": \"true\" }, x.ok ? \"✓ \" : \"✗ \"), h(\"span\", { class: \"sr\" }, x.ok ? \"Passed: \" : \"Did not pass: \"), x.label)));\n        const more = c.list.length ? h(\"button\", { type: \"button\", class: \"how-more\", \"data-testid\": \"how-all-checks\", \"aria-expanded\": \"false\", onclick: () => { ul.hidden = !ul.hidden; more.setAttribute(\"aria-expanded\", ul.hidden ? \"false\" : \"true\"); } }, `All ${c.list.length} check${c.list.length === 1 ? \"\" : \"s\"}`) : null;\n        vCode.replaceChildren(c.text, \" \", more, ul);'''),\n# model into label sub\n('''          j.model ? h(\"p\", { class: \"how-model\", \"data-testid\": \"how-model\" }, \"Model \" + j.model) : null].filter(Boolean));''','''          ].filter(Boolean));\n        if (j.model) { sAi.textContent = j.model.split(\" · \")[0]; sAi.title = \"Model and prompt: \" + j.model; sAi.dataset.model = j.model; }'''),\n])\nEOF\ncd /Users/arsis/zlayt-pm-project/app/frontend/guided && sed -n '/R.traceOf(S, item).then/,/^      }).catch/p' review.js | head -30"
}
````

### User / tool · 2026-11-03T04:41:02.946Z

**tool result**
````
      R.traceOf(S, item).then((tr) => {
        if (mine !== howTicket || !S.alive) return;
        const c = R.howCode(tr), j = R.howJudge(tr, item);
        rCode.dataset.state = c.state; cCode.textContent = c.chip; cCode.className = "hchip " + c.state;
        const ul = h("ul", { class: "how-all", "data-testid": "how-all-list", hidden: true }, c.list.map((x) => h("li", { class: x.ok ? "ok" : "bad" }, h("span", { "aria-hidden": "true" }, x.ok ? "✓ " : "✗ "), h("span", { class: "sr" }, x.ok ? "Passed: " : "Did not pass: "), x.label)));
        const more = c.list.length ? h("button", { type: "button", class: "how-more", "data-testid": "how-all-checks", "aria-expanded": "false", onclick: () => { ul.hidden = !ul.hidden; more.setAttribute("aria-expanded", ul.hidden ? "false" : "true"); } }, `All ${c.list.length} check${c.list.length === 1 ? "" : "s"}`) : null;
        vCode.replaceChildren(c.text, " ", more, ul);
        rAi.dataset.state = j.state; cAi.textContent = j.chip; cAi.className = "hchip " + j.state;
        vAi.replaceChildren(...[j.lead ? h("p", { class: "how-lead", "data-testid": "how-prepared" }, j.lead) : null, h("p", {}, h("b", { class: "how-verdict " + j.state, "data-testid": "how-verdict" }, j.word), j.text ? " " + j.text : ""),
          ].filter(Boolean));
        if (j.model) { sAi.textContent = j.model.split(" · ")[0]; sAi.title = "Model and prompt: " + j.model; sAi.dataset.model = j.model; }
        E.how.removeAttribute("aria-busy");
      }).catch((e) => {
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:41:11.368Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\nedit(\"review.js\",[\n('vCode.replaceChildren(c.text, \" \", more, ul);','vCode.replaceChildren(...[c.text, \" \", more, ul].filter(Boolean));'),\n('''j.word), j.text ? \" \" + j.text : \"\")''','''j.word), j.text ? \". \" + j.text : \"\")'''),\n])\ns=open(\"how.css\").read()\na=s.index(\".how-all { margin-top: 2px; }\"); b=s.index(\".how-all li.bad\")\ns=s[:a]+'''.how-more { display: inline; border: 0; background: transparent; padding: 0; color: var(--accent); font: 600 .875rem var(--font); cursor: pointer; text-decoration: underline; }\n.how-all { list-style: none; margin: 4px 0 0; padding: 0; font-size: .875rem; line-height: 1.25rem; color: var(--muted); }\n.how-all li.ok span:first-child { color: var(--ok); font-weight: 800; }\n'''+s[b:]\ns=s.replace(\".how-rows { padding: 0 14px 8px; max-height: 9.5rem; overflow: auto; font-size: .875rem; line-height: 1.25rem; }\",\".how-rows { padding: 0 14px 8px; font-size: .875rem; line-height: 1.25rem; }\")\ns=s.replace(\".how-model { font-size: .8125rem; color: var(--muted); overflow-wrap: anywhere; }\\n\",\"\")\ns=s.replace(\".how-sub { display: block; font-size: .75rem; line-height: 1rem; color: var(--muted); }\",\".how-sub { display: block; font-size: .75rem; line-height: 1rem; color: var(--muted); overflow-wrap: anywhere; }\")\ns=s.replace(\"  .how-sub { display: none; }\\n\",\"\")\nopen(\"how.css\",\"w\").write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python /private/tmp/claude-501/scratch211/shot.py EXNPq1Q1Uese0eB-92gyCg"
}
````

### User / tool · 2026-11-03T04:41:17.025Z

**tool result**
````
1440 []
390 []
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:41:17.908Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/e1-1440.png"
}
````

### User / tool · 2026-11-03T04:41:17.919Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:41:18.157Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/a1-1440.png"
}
````

### User / tool · 2026-11-03T04:41:18.166Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:41:31.738Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/e1-390.png"
}
````

### User / tool · 2026-11-03T04:41:31.749Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:41:54.711Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\nedit(\"review.js\",[\n('''        E.how.removeAttribute(\"aria-busy\");\n      }).catch((e) => {''','''        E.how.removeAttribute(\"aria-busy\");\n        if (E.how.open && E.how.parentNode === E.srcCard && S.alignMark) S.alignMark();          // the rows now have their real height: the highlighted words stay in the record window\n      }).catch((e) => {'''),\n])\ns=open(\"how.css\").read()\ns=s.replace(\".how > summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 8px 12px; flex-wrap: wrap; padding: 8px 24px; min-height: 40px; }\",\n            \".how > summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 8px 12px; flex-wrap: wrap; padding: 6px 24px; min-height: 34px; }\")\ns=s.replace(\".how-rows { padding: 0 24px 10px; display: grid; gap: 6px; }\",\".how-rows { padding: 0 24px 8px; display: grid; gap: 4px; }\")\ns=s.replace(\".how { flex: none; border-top: 1px solid var(--border); background: var(--sunken); font-size: .9375rem; line-height: 1.35rem; color: var(--text); }\",\n            \".how { flex: none; border-top: 1px solid var(--border); background: var(--sunken); font-size: .875rem; line-height: 1.25rem; color: var(--text); }\")\ns=s.replace(\".how-v { color: var(--text); overflow-wrap: anywhere; min-height: 1.35rem; }\",\".how-v { color: var(--text); overflow-wrap: anywhere; min-height: 1.25rem; }\\n@media (min-width: 761px) { .how-r[data-testid=\\\"how-code\\\"] .how-v { min-height: 2.5rem; } .how-r[data-testid=\\\"how-ai\\\"] .how-v { min-height: 3.75rem; } }      /* the rows keep their height while the trace loads and from item to item */\")\ns=s.replace(\".how-r { display: grid; grid-template-columns: 9.25rem minmax(0, 1fr);\",\".how-r { display: grid; grid-template-columns: 8.5rem minmax(0, 1fr);\")\nopen(\"how.css\",\"w\").write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python /private/tmp/claude-501/scratch211/shot.py EXNPq1Q1Uese0eB-92gyCg"
}
````

### User / tool · 2026-11-03T04:42:00.341Z

**tool result**
````
1440 []
390 []
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:01.248Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/gap-1440.png"
}
````

### User / tool · 2026-11-03T04:42:01.260Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:01.498Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/how-1440.png"
}
````

### User / tool · 2026-11-03T04:42:01.837Z

**tool result**
````
[image]
````

### User / tool · 2026-11-03T04:42:01.833Z

[Image: original 1440x2260, displayed at 1274x2000. Multiply coordinates by 1.13 to map to original image.]

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:09.502Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"review.js\"; s=open(p).read()\na='''return { state: \"none\", word: \"Not needed\", chip: \"AI: not needed\", lead, text, model: \"\" };'''\nassert a in s\ns=s.replace(a,'''return { state: \"none\", word: \"Not needed\", chip: \"AI: not needed\", lead, text: cap(text.replace(/^Not needed: /, \"\")), model: \"\" };''')\nopen(p,\"w\").write(s)\nEOF\ncat > /private/tmp/claude-501/scratch211/phone.py <<'EOF'\nimport sys\nfrom playwright.sync_api import sync_playwright\nTOK=sys.argv[1]\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_context(viewport={\"width\":390,\"height\":844}).new_page(); errs=[]\n    pg.on(\"console\", lambda m: errs.append(m.text) if m.type==\"error\" else None)\n    pg.goto(f\"http://localhost:7860/case/{TOK}/timeline?item=e1\"); pg.wait_for_selector(\"#view[data-ready]\"); pg.wait_for_timeout(500)\n    pg.evaluate(\"document.querySelector('[data-testid=card-line]').scrollTop=9999\"); pg.wait_for_timeout(200)\n    pg.screenshot(path=\"/private/tmp/claude-501/scratch211/ph-closed.png\")\n    pg.get_by_test_id(\"how-summary\").click(); pg.evaluate(\"document.querySelector('[data-testid=card-line]').scrollTop=9999\"); pg.wait_for_timeout(200)\n    pg.screenshot(path=\"/private/tmp/claude-501/scratch211/ph-open.png\")\n    print(pg.evaluate(\"[document.documentElement.scrollWidth, document.documentElement.clientWidth]\"), errs)\n    pg.goto(\"http://localhost:7860/how-it-works\"); pg.wait_for_selector(\"#view[data-ready]\"); pg.wait_for_timeout(300)\n    pg.screenshot(path=\"/private/tmp/claude-501/scratch211/ph-how.png\", full_page=True)\n    print(pg.evaluate(\"[document.documentElement.scrollWidth, document.documentElement.clientWidth]\"))\n    b.close()\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python /private/tmp/claude-501/scratch211/phone.py EXNPq1Q1Uese0eB-92gyCg"
}
````

### User / tool · 2026-11-03T04:42:11.636Z

**tool result**
````
[375, 390] []
[393, 390]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:12.965Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/ph-open.png"
}
````

### User / tool · 2026-11-03T04:42:12.976Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:14.829Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch211/ov.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_context(viewport={\"width\":390,\"height\":844}).new_page()\n    pg.goto(\"http://localhost:7860/how-it-works\"); pg.wait_for_selector(\"#view[data-ready]\")\n    print(pg.evaluate(\"[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>390.5).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right)).slice(0,10)\"))\n    b.close()\nEOF\n.venv/bin/python /private/tmp/claude-501/scratch211/ov.py"
}
````

### User / tool · 2026-11-03T04:42:15.466Z

**tool result**
````
['IMG. 676']
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:18.877Z

**tool call — Bash**
````
{
 "command": "sed -i 's/print(pg.evaluate.*/print(pg.evaluate(\"[...document.querySelectorAll(\\x27body *\\x27)].filter(e=>e.scrollWidth>e.clientWidth+1 \\&\\& getComputedStyle(e).overflowX===\\x27visible\\x27).map(e=>e.tagName+\\x27.\\x27+e.className+\\x27 \\x27+e.scrollWidth+\\x27\\/\\x27+e.clientWidth).slice(0,10)\"))/' /private/tmp/claude-501/scratch211/ov.py && .venv/bin/python /private/tmp/claude-501/scratch211/ov.py"
}
````

### User / tool · 2026-11-03T04:42:18.972Z

**tool result (error)**
````
Exit code 1
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/scratch211/ov.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:21.425Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch211/ov.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_context(viewport={\"width\":390,\"height\":844}).new_page()\n    pg.goto(\"http://localhost:7860/how-it-works\"); pg.wait_for_selector(\"#view[data-ready]\")\n    print(pg.evaluate(\"[...document.querySelectorAll('body *')].filter(e=>e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflowX==='visible').map(e=>e.tagName+'.'+e.className+' '+e.scrollWidth+'/'+e.clientWidth).slice(0,10)\"))\n    b.close()\nEOF\n.venv/bin/python /private/tmp/claude-501/scratch211/ov.py"
}
````

### User / tool · 2026-11-03T04:42:22.040Z

**tool result**
````
['DIV.stick 393/375', 'HEADER.header 393/375', 'BUTTON.theme-btn 24/12']
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:28.667Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && cat >> how.css <<'EOF'\n\n/* the header has one more control now: on a phone the brand name gives way before anything runs past the edge */\n@media (max-width: 760px) {\n  .header .brand { min-width: 0; flex: 0 1 auto; }\n  .header .brand span:last-child { overflow: hidden; text-overflow: ellipsis; }\n  .header .how-link { flex: none; }\n  .header .case-title { flex: 1 1 0; }\n}\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python /private/tmp/claude-501/scratch211/ov.py; .venv/bin/python /private/tmp/claude-501/scratch211/phone.py EXNPq1Q1Uese0eB-92gyCg"
}
````

### User / tool · 2026-11-03T04:42:31.319Z

**tool result**
````
[]
[375, 390] []
[375, 390]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:32.161Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/scratch211/ph-closed.png"
}
````

### User / tool · 2026-11-03T04:42:32.174Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:42:34.860Z

**tool call — Bash**
````
{
 "command": "sed -n 1,75p tests/e2e/guided/test_step2.py | cut -c1-260; grep -n \"def watch\" -A12 tests/e2e/guided/test_shell_smoke.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T04:42:35.076Z

**tool result**
````
"""T-181 (D-068) guided Step 2, "Check the timeline" (docs/GUIDED_UI_SPEC.md section 5). Real browser, the fixture backend (curated set), the real API: every case is made over the API and deleted afterwards.
What is guarded: one item at a time with the highlighted record beside it; Yes / No / Fix / Add a note / pick a date / could-not-check; Undo fully visible; version + expected_status on every write (T-178) and
the plain 409 message; the D-066 compare box (disabled until ticked, compared:true sent, a COMPARE_REQUIRED the page did not expect becomes the box); D-065 tags; no jargon; the keyboard (A, D, E, arrows);
the done screen and its link to step 3; nothing moves when she answers; the primary action is above the fold at 1440x900 and 1366x768; a phone shows enough of the record. Screenshots go to artifacts/screenshots/guided/."""
import json
import os
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided.test_shell_smoke import watch, go, rect

SHOTS = os.path.join(C.ROOT, "artifacts", "screenshots", "guided")
LIB10, LIB09, LIB03, LIB02 = "case_lib10_eob_ub04_cms1500", "case_lib09_spanish_interpreter_espalda", "case_lib03_truck_rear_end_chiro", "case_lib02_slip_fall_prior_knee"
JARGON = re.compile(r"\b(model's|its quote|checked by code|itemized service line|tray|excerpt|judge|LLM|J[1-4])\b|\bflags?\b|\bpending\b|\bverified\b", re.I)


@pytest.fixture
def make():
    made = []

    def _make(lib=None):
        import time
        st, c = C.api("POST", "/api/cases", {"sample": True} if lib is None else {"library": lib}); assert st in (200, 201), (st, c)
        tok = c["token"]; made.append(tok)
        assert C.api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(300):
            s = C.api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(0.5)
        assert s["status"] == "ready", s
        return tok
    yield _make
    for t in made:
        C.api("DELETE", f"/api/cases/{t}")


def case(tok):
    return C.api("GET", f"/api/cases/{tok}")[1]


def item(tok, iid):
    c = case(tok)
    return next(i for g in ("entries", "undated_entries", "flags", "amounts", "tray") for i in c[g] if i["id"] == iid)


def open_item(page, tok, iid=None, step="timeline"):
    go(page, f"/case/{tok}/{step}" + (f"?item={iid}" if iid else ""))
    page.get_by_test_id("card-line").wait_for()


def line_id(page):
    return page.get_by_test_id("card-line").get_attribute("data-item-id")


def settle(page, ms=350):
    page.wait_for_timeout(ms)


@pytest.fixture
def phone(pw):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); pg = ctx.new_page()
    yield pg
    b.close()


def sized(pw, w, h):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}); return b, ctx.new_page()


# ------------------------------------------------------------------------------------------------ the screen

def test_opens_on_the_first_item_with_the_record_words_beside_it(page, make):
    seen = watch(page)
20:def watch(page, allow_404=()):
21-    """pageerror, console.error, failed requests (an asset 404 counts) and window.onerror / unhandledrejection (a hook that runs before any page script). Returns the list to assert empty."""
22-    seen = []
23-    page.add_init_script(HOOK)
24-    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
25-    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" and not any(a in m.text for a in allow_404) else None)
26-    page.on("response", lambda r: seen.append(f"http {r.status}: {r.url}") if r.status >= 400 and not any(a in r.url for a in allow_404) else None)
27-    page.on("requestfailed", lambda r: seen.append("requestfailed: " + r.url) if "ERR_ABORTED" not in (r.failure or "") else None)      # a fetch the app aborted on purpose when she moved on is not
28-    return seen
29-
30-
31-def go(page, path="/"):
32-    page.goto(C.SERVER + path)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:43:14.178Z

**tool call — Bash**
````
{
 "command": "cat > tests/e2e/guided/test_t211.py <<'EOF'\n\"\"\"T-211 (D-074): the app itself shows and explains the validation ladder. Real browser, fixture backend (curated set), real API; cases are made over the API and deleted afterwards.\nGuarded: every Step 2 and Step 3 item shows \"How this was checked\" with three rows (code check, second AI check with its verdict and reason, you); a prepared answer says it was prepared by our team and then\nchecked; a disputed or failed check is shown in words (the trace is rewritten the way the server answers for one); the panel never hides the highlighted words or the primary action at 1440x900 and fits at 390px;\nthe header link on every screen opens \"How each answer is checked\" (about 150 words, the ladder picture, what is code and what is AI, the repo doc names); no console error anywhere.\"\"\"\nimport json\nimport re\nimport pytest\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.guided.test_shell_smoke import watch, go\nfrom tests.e2e.guided.test_step2 import make, phone, sized, case, item, open_item, settle   # noqa: F401  (make and phone are fixtures)\n\nVERDICTS = {\"Agrees\", \"Disputes\", \"Could not check\", \"Not needed\"}\n\n\ndef rows(page):\n    t = lambda k: page.get_by_test_id(k).inner_text()\n    return t(\"how-code-text\"), t(\"how-ai-text\"), t(\"how-you-text\")\n\n\ndef wait_loaded(page):\n    expect(page.get_by_test_id(\"how-checked\")).not_to_have_attribute(\"aria-busy\", \"true\", timeout=10000)\n\n\ndef inside(outer, inner):\n    return inner[\"y\"] >= outer[\"y\"] - 1 and inner[\"y\"] + inner[\"height\"] <= outer[\"y\"] + outer[\"height\"] + 1\n\n\n# ------------------------------------------------------------------------------------------------ the three rows on every item\n\ndef test_every_item_of_steps_2_and_3_shows_code_check_second_ai_check_and_you(pw, make):\n    tok = make(); c = case(tok)\n    b, pg = sized(pw, 1440, 900)\n    try:\n        seen = watch(pg)\n        steps = [(\"timeline\", i[\"id\"]) for g in (\"entries\", \"undated_entries\", \"flags\") for i in c[g]] + [(\"bills\", a[\"id\"]) for a in c[\"amounts\"]]\n        assert len(steps) >= 15\n        for step, iid in steps:\n            open_item(pg, tok, iid, step=step); wait_loaded(pg)\n            code, ai, you = rows(pg)\n            assert code.startswith((\"Passed:\", \"Did not pass:\", \"No code check\")), (iid, code)\n            assert page_verdict(pg) in VERDICTS, (iid, page_verdict(pg))\n            assert ai.strip() and \"Checking\" not in ai and \"Checking\" not in code, (iid, ai)\n            assert you.strip() == \"Waiting for you.\", (iid, you)\n            for k in (\"how-code\", \"how-ai\", \"how-you\"):\n                expect(pg.get_by_test_id(k)).to_be_visible()\n            y = pg.get_by_test_id(\"answer-yes\").bounding_box(); assert y[\"y\"] + y[\"height\"] <= 900, f\"{iid}: the primary action is below the fold\"\n            assert pg.evaluate(\"document.documentElement.scrollHeight <= window.innerHeight\"), iid\n        assert seen == [], seen\n    finally:\n        b.close()\n\n\ndef page_verdict(pg):\n    return pg.get_by_test_id(\"how-verdict\").inner_text()\n\n\ndef test_a_prepared_answer_says_it_was_prepared_and_then_checked_and_names_the_second_check(page, make):\n    seen = watch(page)\n    tok = make(); e = item(tok, \"e1\"); assert e[\"prepared\"] is True\n    open_item(page, tok, \"e1\"); wait_loaded(page)\n    expect(page.get_by_test_id(\"how-prepared\")).to_have_text(\"Prepared by our team; the second AI check then checked it against the quote.\")\n    code, ai, _ = rows(page)\n    assert code.startswith(\"Passed:\") and \"word for word\" in code, code\n    assert page_verdict(page) == \"Agrees\" and \"found every statement\" in ai.lower(), ai\n    assert page.get_by_test_id(\"how-ai-sub\").inner_text().startswith(\"claude-haiku\"), \"the second check names its own model\"\n    page.get_by_test_id(\"how-all-checks\").click()\n    expect(page.get_by_test_id(\"how-all-list\")).to_be_visible()\n    assert page.get_by_test_id(\"how-all-list\").locator(\"li\").count() >= 5\n    # an amount is code-made: no \"prepared\" line, but the same second check\n    open_item(page, tok, \"a1\", step=\"bills\"); wait_loaded(page)\n    assert page.get_by_test_id(\"how-prepared\").count() == 0 and \"amount appears in the record\" in rows(page)[0]\n    # a warning made by code needs no second check, and says why\n    open_item(page, tok, \"f_gap_r6_r7\"); wait_loaded(page)\n    assert page_verdict(page) == \"Not needed\" and \"worked out by code\" in rows(page)[0]\n    assert seen == [], seen\n\n\ndef test_your_decision_shows_in_the_you_row(page, make):\n    seen = watch(page)\n    tok = make(); open_item(page, tok, \"e1\"); wait_loaded(page)\n    assert rows(page)[2] == \"Waiting for you.\"\n    page.get_by_test_id(\"answer-yes\").click(); settle(page, 500)\n    open_item(page, tok, \"e1\"); wait_loaded(page)\n    assert rows(page)[2] == \"You kept it in the letter.\"\n    page.get_by_test_id(\"answer-no\").click(); settle(page, 500)\n    open_item(page, tok, \"e1\"); wait_loaded(page)\n    assert rows(page)[2] == \"You left it out of the letter.\"\n    open_item(page, tok, \"a1\", step=\"bills\"); page.get_by_test_id(\"answer-yes\").click(); settle(page, 500)\n    open_item(page, tok, \"a1\", step=\"bills\"); wait_loaded(page)\n    assert rows(page)[2] == \"You counted it in the bill total.\"\n    assert seen == [], seen\n\n\n# ------------------------------------------------------------------------------------------------ a dispute or a failed check is shown in words\n\ndef rewrite_trace(page, fn):\n    def h(route):\n        r = route.fetch(); j = r.json(); fn(j); route.fulfill(response=r, json=j)\n    page.route(re.compile(r\"/api/cases/[^/]+/items/e2/trace$\"), h)\n\n\ndef test_a_disputed_item_shows_disputes_with_the_servers_reason_and_a_failed_code_check_says_what_failed(page, make):\n    seen = watch(page)\n    tok = make()\n    def fn(j):\n        for s in j[\"steps\"]:\n            if s[\"id\"] == \"judge_1\":\n                s[\"status\"] = \"fail\"; s[\"evidence\"].update(judge_verdict=\"partially\", judge_reason_code=\"DROPS_QUALIFIER\", rationale=\"The summary leaves out a qualifier that the quote carries.\")\n            if s[\"id\"] == \"summary_tokens\":\n                s[\"status\"] = \"fail\"; s[\"why\"] = \"The summary has a number that is not in the quote: 9.\"\n    rewrite_trace(page, fn)\n    open_item(page, tok, \"e2\"); wait_loaded(page)\n    code, ai, _ = rows(page)\n    assert page_verdict(page) == \"Disputes\" and \"leaves out a qualifier that the highlighted words carry\" in ai, ai\n    assert code.startswith(\"Did not pass:\") and \"number that is not in the highlighted words\" in code, code\n    expect(page.locator(\"[data-testid=how-chip-ai]\")).to_have_text(\"AI: disputes\"); expect(page.locator(\"[data-testid=how-chip-code]\")).to_have_text(\"Code: not passed\")\n    assert seen == [], seen\n\n\ndef test_a_trace_that_cannot_be_read_says_so_and_the_item_still_works(page, make):\n    tok = make()\n    page.route(re.compile(r\"/api/cases/[^/]+/items/e1/trace$\"), lambda r: r.fulfill(status=500, json={\"error\": {\"code\": \"x\", \"message\": \"x\"}}))\n    open_item(page, tok, \"e1\"); wait_loaded(page)\n    code, ai, you = rows(page)\n    assert \"couldn't load\" in code and \"couldn't load\" in ai and you == \"Waiting for you.\"\n    page.get_by_test_id(\"answer-yes\").click(); settle(page, 500)\n    assert page.get_by_test_id(\"card-line\").get_attribute(\"data-item-id\") != \"e1\" or page.get_by_test_id(\"done-heading\").count()\n\n\n# ------------------------------------------------------------------------------------------------ layout\n\ndef test_at_1440x900_the_panel_keeps_the_highlighted_words_and_the_primary_action_in_view(pw, make):\n    tok = make(); b, pg = sized(pw, 1440, 900)\n    try:\n        seen = watch(pg)\n        for iid in (\"e1\", \"e2\", \"e4\", \"e6\"):\n            open_item(pg, tok, iid); wait_loaded(pg); settle(pg, 150)\n            src = pg.get_by_test_id(\"card-source\").bounding_box(); how = pg.get_by_test_id(\"how-checked\").bounding_box()\n            assert how[\"y\"] >= src[\"y\"] + src[\"height\"] - 2, \"the panel sits under the record, not over it\"\n            m = pg.locator(\"[data-testid=card-source] mark\").first.bounding_box()\n            assert m and m[\"y\"] >= src[\"y\"] - 1 and m[\"y\"] + min(m[\"height\"], 30) <= src[\"y\"] + src[\"height\"], f\"{iid}: the highlighted words start in the record window\"\n            assert pg.get_by_test_id(\"answer-yes\").is_visible() and pg.evaluate(\"document.documentElement.scrollHeight <= window.innerHeight\")\n        assert seen == [], seen\n    finally:\n        b.close()\n\n\ndef test_at_390px_the_panel_is_pinned_to_the_end_of_the_line_card_closed_with_three_chips_and_opens_without_overflow(phone, make):\n    seen = watch(phone)\n    tok = make(); open_item(phone, tok, \"e1\"); wait_loaded(phone)\n    for k, t in ((\"how-chip-code\", \"Code: passed\"), (\"how-chip-ai\", \"AI: agrees\"), (\"how-chip-you\", \"You: waiting\")):\n        assert phone.get_by_test_id(k).inner_text() == t\n    phone.evaluate(\"document.querySelector('[data-testid=card-line]').scrollTop = 99999\")\n    expect(phone.get_by_test_id(\"how-summary\")).to_be_in_viewport()\n    assert phone.get_by_test_id(\"how-code\").is_visible() is False\n    phone.get_by_test_id(\"how-summary\").click()\n    phone.evaluate(\"document.querySelector('[data-testid=card-line]').scrollTop = 99999\")\n    for k in (\"how-code\", \"how-ai\", \"how-you\"):\n        expect(phone.get_by_test_id(k)).to_be_visible()\n    expect(phone.get_by_test_id(\"how-prepared\")).to_be_visible()\n    assert phone.evaluate(\"document.documentElement.scrollWidth <= document.documentElement.clientWidth\"), \"no sideways scroll\"\n    card = phone.get_by_test_id(\"card-line\").bounding_box(); assert phone.get_by_test_id(\"how-ai\").bounding_box()[\"x\"] + phone.get_by_test_id(\"how-ai\").bounding_box()[\"width\"] <= card[\"x\"] + card[\"width\"] + 1\n    y = phone.get_by_test_id(\"answer-yes\").bounding_box(); assert y[\"y\"] + y[\"height\"] <= 844, \"the primary action is in view\"\n    assert seen == [], seen\n\n\n# ------------------------------------------------------------------------------------------------ the page\n\n@pytest.mark.parametrize(\"path_of\", [lambda t: \"/\", lambda t: \"/new\", lambda t: f\"/case/{t}/records\", lambda t: f\"/case/{t}/timeline\", lambda t: f\"/case/{t}/bills\", lambda t: f\"/case/{t}/letter\"])\ndef test_every_screen_links_to_how_each_answer_is_checked(page, make, path_of):\n    seen = watch(page)\n    tok = make(); go(page, path_of(tok)); page.locator(\"#view[data-ready]\").wait_for()\n    link = page.get_by_test_id(\"link-how\"); expect(link).to_be_visible(); expect(link).to_have_attribute(\"href\", \"/how-it-works\")\n    link.click(); expect(page).to_have_url(re.compile(r\"/how-it-works$\")); expect(page.get_by_test_id(\"page-title\")).to_have_text(\"How each answer is checked\")\n    expect(page.get_by_test_id(\"link-how\")).to_have_attribute(\"aria-current\", \"page\")\n    assert seen == [], seen\n\n\ndef explain_words(page):\n    return len(re.findall(r\"\\w+\", page.get_by_test_id(\"how-steps\").inner_text()))\n\n\n@pytest.mark.parametrize(\"w,h\", [(1440, 900), (390, 844)])\ndef test_the_page_explains_the_ladder_shows_the_picture_and_names_code_and_ai(pw, w, h):\n    b, pg = sized(pw, w, h)\n    try:\n        seen = watch(pg)\n        go(pg, \"/how-it-works\"); pg.locator(\"#view[data-ready]\").wait_for()\n        assert 100 <= explain_words(pg) <= 200, explain_words(pg)\n        text = pg.get_by_test_id(\"how-steps\").inner_text()\n        for must in (\"Prepared by our team\", \"Code checks it\", \"A second AI checks it\", \"different model, with a different prompt\", \"You decide\", \"accept, edit or dismiss\"):\n            assert must in text, must\n        img = pg.get_by_test_id(\"how-ladder-img\"); expect(img).to_be_visible()\n        assert img.evaluate(\"e => e.complete && e.naturalWidth > 0\"), \"the validation-ladder picture loaded\"\n        assert (img.get_attribute(\"alt\") or \"\").startswith(\"Validation ladder\")\n        body = pg.get_by_test_id(\"how-code-vs-ai\").inner_text(); assert \"Code only, never AI\" in body and \"AI, always checked\" in body\n        repo = pg.get_by_test_id(\"how-repo\").inner_text()\n        for name in (\"docs/LLM_VS_CODE.md\", \"app/llm/prompts/\", \"evals/\", \"D-065\", \"D-066\"):\n            assert name in repo, name\n        assert pg.evaluate(\"document.documentElement.scrollWidth <= document.documentElement.clientWidth\"), \"no sideways scroll\"\n        assert not re.search(r\"\\bAI draft\\b|claude|sonnet\", pg.get_by_test_id(\"how-page\").inner_text(), re.I), \"a prepared demo never calls the answers AI output\"\n        pg.get_by_test_id(\"how-back\").click(); expect(pg.get_by_test_id(\"page-title\")).to_have_text(\"Your cases\")\n        assert seen == [], seen\n    finally:\n        b.close()\n\n\ndef test_the_picture_is_served_and_the_page_is_reachable_by_its_own_address(page):\n    seen = watch(page)\n    st, _ = C.api(\"GET\", \"/api/health\"); assert st == 200\n    go(page, \"/how-it-works\"); expect(page.get_by_test_id(\"how-page\")).to_be_visible()\n    r = page.request.get(C.SERVER + \"/validation-ladder.svg\"); assert r.status == 200 and \"svg\" in r.headers[\"content-type\"] and \"Validation ladder\" in r.text()\n    assert seen == [], seen\nEOF\nsed -i 's/assert \"statement dated March 18, 2026\" in page.get_by_test_id(\"src-head\").inner_text()/assert \"record dated March 18, 2026\" in page.get_by_test_id(\"src-head\").inner_text()          # T-211: the head reads service_date.date_label, so an ED record is a record here too/' tests/e2e/guided/test_t206.py\ngrep -n \"record dated March 18\" tests/e2e/guided/test_t206.py | cut -c1-160; grep -n \"SERVER\\b\" tests/e2e/conftest.py | head -3"
}
````

### User / tool · 2026-11-03T04:43:14.295Z

**tool result**
````
sed: 2: "tests/e2e/guided/test_t ...": undefined label 'ests/e2e/guided/test_t206.py'
33:    assert page.get_by_test_id("service-date-text").inner_text() == "date of service [__________] (record dated March 18, 2026)"          # T-202 r6 rule 4: 
107:SERVER = os.environ.get("E2E_BASE_URL", "http://localhost:7860")      # the app's root: the guided UI (D-068) is served here, and every /api call goes here
108:BASE = SERVER + "/classic"                                              # D-068: the old screen moved to /classic; the whole classic suite navigates from BASE, API calls use SERVER
122:    global BASE, SERVER
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:43:15.085Z

Use python for the edit; then run the new tests against the live server.

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:43:17.045Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/guided/test_t206.py\"; s=open(p).read()\na='assert \"statement dated March 18, 2026\" in page.get_by_test_id(\"src-head\").inner_text()'\nassert s.count(a)==1\ns=s.replace(a,'assert \"record dated March 18, 2026\" in page.get_by_test_id(\"src-head\").inner_text()          # T-211: the card heads read service_date.date_label too')\ns=s.replace(\"(src-head below still says statement: frontend card)\",\"\")\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"src-head below\" tests/e2e/guided/test_t206.py | head -2\n.venv/bin/python -m pytest tests/e2e/guided/test_t211.py -x -q 2>&1 | tail -25"
}
````

### User / tool · 2026-11-03T04:43:39.989Z

**tool result**
````
            for must in ("Prepared by our team", "Code checks it", "A second AI checks it", "different model, with a different prompt", "You decide", "accept, edit or dismiss"):
                assert must in text, must
            img = pg.get_by_test_id("how-ladder-img"); expect(img).to_be_visible()
            assert img.evaluate("e => e.complete && e.naturalWidth > 0"), "the validation-ladder picture loaded"
            assert (img.get_attribute("alt") or "").startswith("Validation ladder")
            body = pg.get_by_test_id("how-code-vs-ai").inner_text(); assert "Code only, never AI" in body and "AI, always checked" in body
            repo = pg.get_by_test_id("how-repo").inner_text()
            for name in ("docs/LLM_VS_CODE.md", "app/llm/prompts/", "evals/", "D-065", "D-066"):
                assert name in repo, name
            assert pg.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), "no sideways scroll"
            assert not re.search(r"\bAI draft\b|claude|sonnet", pg.get_by_test_id("how-page").inner_text(), re.I), "a prepared demo never calls the answers AI output"
>           pg.get_by_test_id("how-back").click(); expect(pg.get_by_test_id("page-title")).to_have_text("Your cases")
                                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: Locator expected to have text 'Your cases'
E           Actual value: None
E           Error: element(s) not found 
E           Call log:
E             - Expect "to_have_text" get_by_test_id("page-title") with timeout 5000ms
E             - waiting for get_by_test_id("page-title")

tests/e2e/guided/test_t211.py:203: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_t211.py::test_the_page_explains_the_ladder_shows_the_picture_and_names_code_and_ai[1440-900]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 13 passed in 21.80s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:43:41.744Z

**tool call — Bash**
````
{
 "command": "grep -n \"h1\" app/frontend/guided/home.js | cut -c1-200 | head -4"
}
````

### User / tool · 2026-11-03T04:43:41.829Z

**tool result**
````
133:    const head = (...extra) => h("div", { class: "home-h" }, h("div", { class: "hh-main" }, h("h1", { "data-testid": "page-title", tabindex: "-1" }, "Your cases"), h("p", {}, "Each case goes throu
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:43:45.478Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch211/back.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_context(viewport={\"width\":1440,\"height\":900}).new_page()\n    pg.on(\"console\", lambda m: print(\"C\", m.text)); pg.on(\"pageerror\", lambda e: print(\"E\", e))\n    pg.goto(\"http://localhost:7860/how-it-works\"); pg.wait_for_selector(\"#view[data-ready]\")\n    print(pg.evaluate(\"history.length\"))\n    pg.get_by_test_id(\"how-back\").click(); pg.wait_for_timeout(1500)\n    print(pg.url, pg.evaluate(\"document.querySelector('#view').dataset.route\"), pg.evaluate(\"document.body.innerText.slice(0,200)\"))\n    b.close()\nEOF\n.venv/bin/python /private/tmp/claude-501/scratch211/back.py"
}
````

### User / tool · 2026-11-03T04:43:47.622Z

**tool result (error)**
````
Exit code 1
2
Traceback (most recent call last):
  File "/private/tmp/claude-501/scratch211/back.py", line 8, in <module>
    print(pg.url, pg.evaluate("document.querySelector('#view').dataset.route"), pg.evaluate("document.body.innerText.slice(0,200)"))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 16843, in evaluate
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_page.py", line 476, in evaluate
    return await self._main_frame.evaluate(expression, arg)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 346, in evaluate
    await self._channel.send(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.evaluate: TypeError: Cannot read properties of null (reading 'dataset')
    at eval (eval at evaluate (:370:30), <anonymous>:1:32)
    at eval (<anonymous>)
    at UtilityScript.evaluate (<anonymous>:370:30)
    at UtilityScript.<anonymous> (<anonymous>:1:44)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:43:54.712Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\nedit(\"app.js\",[('''  G.go = function (path, opts) { (opts''','''  G.go = function (path, opts) { G.navigated = true; (opts''')])\nedit(\"how.js\",[('if (history.length > 1) history.back(); else ctx.go(\"/\");','if (G.navigated) history.back(); else ctx.go(\"/\");          // arrived by a link inside the app: back to where she was; opened directly (history.length also counts the blank tab): to the cases')])\nEOF\ncd /Users/arsis/zlayt-pm-project && python3 - <<'EOF'\np=\"tests/e2e/guided/test_t211.py\"; s=open(p).read()\na='''        pg.get_by_test_id(\"how-back\").click(); expect(pg.get_by_test_id(\"page-title\")).to_have_text(\"Your cases\")\n'''\nb='''        pg.get_by_test_id(\"how-back\").click(); expect(pg.get_by_test_id(\"page-title\")).to_have_text(\"Your cases\")      # opened directly: Back goes to the cases\n'''\nassert a in s; s=s.replace(a,b)\ns+='''\n\ndef test_back_returns_to_the_item_she_was_on(page, make):\n    seen = watch(page)\n    tok = make(); open_item(page, tok, \"e2\"); wait_loaded(page)\n    page.get_by_test_id(\"link-how\").click(); expect(page.get_by_test_id(\"how-page\")).to_be_visible()\n    page.get_by_test_id(\"how-back\").click(); expect(page).to_have_url(re.compile(r\"/timeline\\\\?item=e2$\"))\n    expect(page.get_by_test_id(\"card-line\")).to_have_attribute(\"data-item-id\", \"e2\")\n    assert seen == [], seen\n'''\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/e2e/guided/test_t211.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-03T04:45:53.981Z

**tool result**
````
FAILED tests/e2e/guided/test_t211.py::test_your_decision_shows_in_the_you_row
FAILED tests/e2e/guided/test_t211.py::test_a_disputed_item_shows_disputes_with_the_servers_reason_and_a_failed_code_check_says_what_failed
FAILED tests/e2e/guided/test_t211.py::test_at_1440x900_the_panel_keeps_the_highlighted_words_and_the_primary_action_in_view
FAILED tests/e2e/guided/test_t211.py::test_at_390px_the_panel_is_pinned_to_the_end_of_the_line_card_closed_with_three_chips_and_opens_without_overflow
FAILED tests/e2e/guided/test_t211.py::test_every_screen_links_to_how_each_answer_is_checked[<lambda>0]
FAILED tests/e2e/guided/test_t211.py::test_every_screen_links_to_how_each_answer_is_checked[<lambda>1]
FAILED tests/e2e/guided/test_t211.py::test_every_screen_links_to_how_each_answer_is_checked[<lambda>2]
FAILED tests/e2e/guided/test_t211.py::test_every_screen_links_to_how_each_answer_is_checked[<lambda>3]
FAILED tests/e2e/guided/test_t211.py::test_every_screen_links_to_how_each_answer_is_checked[<lambda>4]
FAILED tests/e2e/guided/test_t211.py::test_every_screen_links_to_how_each_answer_is_checked[<lambda>5]
FAILED tests/e2e/guided/test_t211.py::test_the_page_explains_the_ladder_shows_the_picture_and_names_code_and_ai[1440-900]
FAILED tests/e2e/guided/test_t211.py::test_the_page_explains_the_ladder_shows_the_picture_and_names_code_and_ai[390-844]
FAILED tests/e2e/guided/test_t211.py::test_the_picture_is_served_and_the_page_is_reachable_by_its_own_address
FAILED tests/e2e/guided/test_t211.py::test_back_returns_to_the_item_she_was_on
16 failed, 1 passed in 118.12s (0:01:58)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:45:56.358Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/e2e/guided/test_t211.py -x -q -k \"own_address\" 2>&1 | tail -20; curl -s -o /dev/null -w \"%{http_code}\\n\" localhost:7860/api/health; node --check app/frontend/guided/app.js 2>&1 | head; node --check app/frontend/guided/how.js 2>&1 | head"
}
````

### User / tool · 2026-11-03T04:46:03.411Z

**tool result**
````
E       - note: Synthetic data only — never paste real records
E       - banner:
E         - link "Treatment Timeline":
E           - /url: /
E         - text: "Demo: sample answers prepared by our team"
E         - link "How each answer is checked":
E           - /url: /how-it-works
E         - button "Dark mode"
E       - main:
E         - heading "We couldn't find that page" [level=1]
E         - paragraph: The link may be old or mistyped.
E         - link "Back to your cases":
E           - /url: /
E       - contentinfo: "Demo: sample answers prepared by our team. Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."

tests/e2e/guided/test_t211.py:212: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_t211.py::test_the_picture_is_served_and_the_page_is_reachable_by_its_own_address
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 16 deselected in 5.64s
200
/Users/arsis/zlayt-pm-project/app/frontend/guided/how.js:53
  };
   ^

SyntaxError: Unexpected token ';'
    at internalCompileFunction (node:internal/vm:128:18)
    at wrapSafe (node:internal/modules/cjs/loader:1279:20)
    at node:internal/main/check_syntax:81:41
    at loadESM (node:internal/process/esm_loader:28:13)
    at checkSyntax (node:internal/main/check_syntax:81:21)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:06.301Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"how.js\"; s=open(p).read()\ni=s.index(\"          // arrived by a link inside the app\"); j=s.index(\"\\n\",i)\nline=s[i:j]; print(repr(line[-60:]))\ns=s[:i]+s[j:]\ns=s.replace('else ctx.go(\"/\");','else ctx.go(\"/\"); /* arrived by a link inside the app: back to where she was; opened directly (history.length also counts the blank tab): to the cases */',1) if False else s\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"G.navigated\" how.js | cut -c1-250; node --check how.js"
}
````

### User / tool · 2026-11-03T04:46:06.462Z

**tool result (error)**
````
Exit code 1
'gth also counts the blank tab): to the cases } }, "‹ Back");'
18:    const back = h("button", { type: "button", class: "btn", "data-testid": "how-back", onclick: () => { if (G.navigated) history.back(); else ctx.go("/");
/Users/arsis/zlayt-pm-project/app/frontend/guided/how.js:53
  };
   ^

SyntaxError: Unexpected token ';'
    at internalCompileFunction (node:internal/vm:128:18)
    at wrapSafe (node:internal/modules/cjs/loader:1279:20)
    at node:internal/main/check_syntax:81:41
    at loadESM (node:internal/process/esm_loader:28:13)
    at checkSyntax (node:internal/main/check_syntax:81:21)

Node.js v21.7.1
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:07.276Z

I truncated the line's tail; restore it.

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:09.023Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"how.js\"; s=open(p).read()\na='else ctx.go(\"/\");\\n'\nassert s.count(a)==1\ns=s.replace(a,'else ctx.go(\"/\"); } }, \"‹ Back\");      // by a link inside the app: back to where she was; opened directly (history.length also counts the blank tab): to the cases\\n')\nopen(p,\"w\").write(s)\nEOF\nnode --check how.js && cd /Users/arsis/zlayt-pm-project && .venv/bin/python -m pytest tests/e2e/guided/test_t211.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-03T04:46:28.424Z

**tool result**
````
.................                                                        [100%]
17 passed in 18.26s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:31.404Z

**tool call — Bash**
````
{
 "command": "git status --short app/frontend tests/e2e | head -20; git diff --stat HEAD -- app/frontend tests/e2e | tail -15"
}
````

### User / tool · 2026-11-03T04:46:31.535Z

**tool result**
````
 M app/frontend/guided/app.js
 M app/frontend/guided/core.js
 M app/frontend/guided/index.html
MM app/frontend/guided/review.js
 M app/frontend/guided/step2.js
MM app/frontend/guided/step3.css
MM app/frontend/guided/step3.js
MM tests/e2e/conftest.py
MM tests/e2e/guided/test_t205.py
MM tests/e2e/guided/test_t206.py
?? app/frontend/guided/how.css
?? app/frontend/guided/how.js
?? app/frontend/guided/validation-ladder.svg
?? tests/e2e/guided/test_t211.py
 app/frontend/guided/app.js     |  9 ++--
 app/frontend/guided/core.js    |  1 +
 app/frontend/guided/index.html |  2 +
 app/frontend/guided/review.js  | 97 ++++++++++++++++++++++++++++++++++++++++--
 app/frontend/guided/step2.js   | 17 ++++++--
 app/frontend/guided/step3.js   | 24 ++++++++---
 tests/e2e/guided/test_t206.py  |  4 +-
 7 files changed, 135 insertions(+), 19 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:36.917Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/scratch211/idx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/frontend/guided/app.js app/frontend/guided/core.js app/frontend/guided/index.html app/frontend/guided/review.js app/frontend/guided/step2.js app/frontend/guided/step3.js app/frontend/guided/how.css app/frontend/guided/how.js app/frontend/guided/validation-ladder.svg tests/e2e/guided/test_t211.py tests/e2e/guided/test_t206.py && TREE=$(git write-tree) && echo $TREE && git diff --cached --stat HEAD | tail -14 && rm -rf /private/tmp/claude-501/scratch211/arch && mkdir -p /private/tmp/claude-501/scratch211/arch && git archive $TREE | tar -x -C /private/tmp/claude-501/scratch211/arch && echo extracted; unset GIT_INDEX_FILE; ls /private/tmp/claude-501/scratch211/arch | head -20; ls -d .venv; "
}
````

### User / tool · 2026-11-03T04:46:37.629Z

**tool result (error)**
````
Permission to use Bash with command export GIT_INDEX_FILE=/private/tmp/claude-501/scratch211/idx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/frontend/guided/app.js app/frontend/guided/core.js app/frontend/guided/index.html app/frontend/guided/review.js app/frontend/guided/step2.js app/frontend/guided/step3.js app/frontend/guided/how.css app/frontend/guided/how.js app/frontend/guided/validation-ladder.svg tests/e2e/guided/test_t211.py tests/e2e/guided/test_t206.py && TREE=$(git write-tree) && echo $TREE && git diff --cached --stat HEAD | tail -14 && rm -rf /private/tmp/claude-501/scratch211/arch && mkdir -p /private/tmp/claude-501/scratch211/arch && git archive $TREE | tar -x -C /private/tmp/claude-501/scratch211/arch && echo extracted; unset GIT_INDEX_FILE; ls /private/tmp/claude-501/scratch211/arch | head -20; ls -d .venv;  has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:40.252Z

**tool call — Bash**
````
{
 "command": "IDX=/private/tmp/claude-501/scratch211/idx2 && GIT_INDEX_FILE=$IDX git read-tree HEAD && GIT_INDEX_FILE=$IDX git add app/frontend/guided/app.js app/frontend/guided/core.js app/frontend/guided/index.html app/frontend/guided/review.js app/frontend/guided/step2.js app/frontend/guided/step3.js app/frontend/guided/how.css app/frontend/guided/how.js app/frontend/guided/validation-ladder.svg tests/e2e/guided/test_t211.py tests/e2e/guided/test_t206.py && GIT_INDEX_FILE=$IDX git write-tree"
}
````

### User / tool · 2026-11-03T04:46:41.030Z

**tool result**
````
1b19e97136521440fdbb8be3654c1843e78344b3
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:43.491Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/scratch211/archA && git archive 1b19e97136521440fdbb8be3654c1843e78344b3 | tar -x -C /private/tmp/claude-501/scratch211/archA && cd /private/tmp/claude-501/scratch211/archA && ls | head; ls -la | grep -i venv; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t204_prepared_fallback.md >/dev/null; grep -n \"E2E_REQUIRE_DB\\|venv\" /Users/arsis/zlayt-pm-project/tests/e2e/conftest.py | head"
}
````

### User / tool · 2026-11-03T04:46:44.663Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
121:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
167:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
172:        if os.environ.get("E2E_REQUIRE_DB") == "1":
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:45.340Z

Run the full e2e from the archive in the background.

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:46.476Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/scratch211/archA && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e -q -x -p no:cacheprovider > /private/tmp/claude-501/scratch211/full.log 2>&1; tail -15 /private/tmp/claude-501/scratch211/full.log",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-03T04:46:46.550Z

**tool result**
````
Command running in background with ID: ba1fp7zk5. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/ba1fp7zk5.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:55.779Z

**tool call — Bash**
````
{
 "command": "cat > .claude/agent-memory/frontend/project_t211_how_checked.md <<'EOF'\n---\nname: t211-how-checked\ndescription: T-211 guided \"How this was checked\" panel (review.js howPanel) and /how-it-works page hooks, placement rules, pitfalls\nmetadata:\n  type: project\n---\n\nPanel: `E.how` (details, testid how-checked) built by drawHow() in review.js from GET /items/<id>/trace (R.traceOf caches per token|id|version; failed read forgotten). Rows how-code / how-ai / how-you (+ -text, -sub), chips how-chip-code|ai|you, how-verdict, how-prepared (D-065 lead sentence, only when item.prepared), how-all-checks (toggle) + how-all-list. cfg.youText(S,item) per step supplies the You sentence (null = \"Waiting for you.\"); screen.how:false hides it in edit/write/note modes.\nPlacement: wide screen = bottom of the record card (card-src), open only when innerHeight >= 840; phone = END of the line card (after the foot; that card scrolls as one box), closed with three chips. Never between body and foot: the desktop foot is a fixed 150px and the phone foot holds the tick box. JS placeHow() re-places on the (max-width:760px) media change.\nPitfalls: a `//` comment appended after a one-line onclick swallowed the closing braces (node --check every edited file); history.length is 2 on a fresh tab so Back uses G.navigated (set in G.go); header gained a link so phone brand needs min-width:0 + ellipsis (scrollWidth 393 vs 375 otherwise); `replaceChildren(null)` prints \"null\" so filter(Boolean).\nPage: how.js (G.pages.how, route /how-it-works, step 0 = no step bar), how.css; ladder picture is a copy of submission/validation-ladder.svg (writer owns the original; it still says \"In progress (D-066)\" and has first-person text, so re-copy after the writer updates it). Step 3 reads service_date.date_label via dateWord(sd).\nTest: tests/e2e/guided/test_t211.py (trace rewritten with page.route + route.fetch().json() for a disputed / failed check).\nEOF\npython3 - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/MEMORY.md\"\ns=open(p).read().rstrip(\"\\n\")+\"\\n- [T-211 how this was checked](project_t211_how_checked.md) — trace-fed three-row panel, placement rules, /how-it-works page, pitfalls\\n\"\nopen(p,\"w\").write(s)\nEOF\nB=\"python3 tools/board.py\"; $B note T-211 --agent frontend --text \"Built: how-checked panel (review.js, trace-fed: code check / second AI check verdict+reason / you; prepared lead per D-065), /how-it-works page + header link on every screen, ladder SVG copy, Step 3 date_label. test_t211.py 17 pass on live server; full e2e from archive running.\""
}
````

### User / tool · 2026-11-03T04:46:55.971Z

**tool result**
````
/bin/bash: child setpgid (2074 to 2074): Operation not permitted
noted on T-211
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:56.905Z

**tool call — Bash**
````
{
 "command": "sleep 240; tail -c 600 /private/tmp/claude-501/scratch211/full.log",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T04:46:56.912Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 240 followed by: tail -c 600 /private/tmp/claude-501/scratch211/full.log. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:57.634Z

Waiting for the background run to finish; it will notify me.

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:46:57.965Z

**tool call — Monitor**
````
{
 "query": "select:Monitor",
 "max_results": "1"
}
````

### User / tool · 2026-11-03T04:46:57.970Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Monitor failed due to the following issue:
The required parameter `description` is missing

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 1800000ms are capped to 1800000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required":["description","timeout_ms"],"additionalProperties":false}</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:47:00.210Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/scratch211/full.log; do sleep 5; done; tail -c 700 /private/tmp/claude-501/scratch211/full.log",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T04:47:35.404Z

**tool result**
````
ssert m["y"] >= pane["y"] - 1 and m["y"] + m["height"] <= pane["y"] + pane["height"] + 1, (i, m, pane)
E               AssertionError: (2, {'x': 129.375, 'y': 639.390625, 'width': 367.6875, 'height': 23}, {'x': 33, 'y': 357, 'width': 666.5, 'height': 180})
E               assert (639.390625 >= (357 - 1) and (639.390625 + 23) <= ((357 + 180) + 1))

tests/e2e/guided/test_round2.py:374: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_round2.py::test_every_highlight_of_a_multi_record_warning_is_in_view_at_1440
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 30 passed in 46.79s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:48:05.780Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\ndef edit(p, pairs):\n    s=open(p).read()\n    for a,b in pairs:\n        assert s.count(a)==1,(p,a,s.count(a)); s=s.replace(a,b)\n    open(p,\"w\").write(s)\nedit(\"review.js\",[\n('''      E.how.ontoggle = () => { R.howOpen = E.how.open; };''','''      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };'''),\n('''        if (E.how.open && E.how.parentNode === E.srcCard && S.alignMark) S.alignMark();          // the rows now have their real height: the highlighted words stay in the record window\n      }).catch((e) => {''','''        fitHow();\n      }).catch((e) => {'''),\n('''    function renderSource(keep) {''','''    /* The highlighted words come first: when the open panel would push any of them out of the record window (several records in one warning, a long quote), and she has not chosen to keep it open,\n       it folds to its one-line chips. She can open it; her choice then stays for the rest of the visit. */\n    function fitHow() {\n      if (!E.how.open || R.howOpen != null || E.how.parentNode !== E.srcCard) { if (E.how.open && E.how.parentNode === E.srcCard && S.alignMark) S.alignMark(); return; }\n      const box = E.srcBody.getBoundingClientRect(), cut = [...E.srcBody.querySelectorAll(\"mark\")].some((m) => { const r = m.getBoundingClientRect(); return r.bottom > box.bottom + 1; });\n      if (cut) { E.how._auto = true; E.how.open = false; if (S.alignMark) S.alignMark(); } else if (S.alignMark) S.alignMark();\n    }\n    function renderSource(keep) {'''),\n('''      renderSource(false);\n      updateTitlebar(); syncButtons(); drawStatus();''','''      renderSource(false);\n      fitHow();\n      updateTitlebar(); syncButtons(); drawStatus();'''),\n])\nEOF\nnode --check review.js"
}
````

### User / tool · 2026-11-03T04:48:05.937Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:48:11.920Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend/guided && python3 - <<'EOF'\np=\"review.js\"; s=open(p).read()\na='''      E.how.open = R.howOpen == null ? !narrowMQ.matches && window.innerHeight >= 840 : R.howOpen;'''\nassert a in s\ns=s.replace(a,'''      const want = R.howOpen == null ? !narrowMQ.matches && window.innerHeight >= 840 : R.howOpen;\n      if (want !== E.how.open) { E.how._auto = true; E.how.open = want; }          // a change the page made is not her choice (the toggle event says which)''')\ns=s.replace('''      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };''','''      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };''')\nopen(p,\"w\").write(s)\nEOF\nnode --check review.js; grep -n \"how.ontoggle\\|_auto\" review.js | cut -c1-140"
}
````

### User / tool · 2026-11-03T04:48:12.084Z

**tool result**
````
375:      if (want !== E.how.open) { E.how._auto = true; E.how.open = want; }          // a change the page made is not her choice (the togg
376:      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };
401:      if (cut) { E.how._auto = true; E.how.open = false; if (S.alignMark) S.alignMark(); } else if (S.alignMark) S.alignMark();
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:48:25.656Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/guided/test_t211.py\"; s=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a; s=s.replace(a,b)\nrep('''def inside(outer, inner):''','''def open_panel(page):\n    \"\"\"At 1440x900 the panel folds to its chips when it would push a highlighted word out of the record window; she opens it with one click (and it then stays open).\"\"\"\n    if not page.get_by_test_id(\"how-code\").is_visible():\n        page.get_by_test_id(\"how-summary\").click()\n    expect(page.get_by_test_id(\"how-code\")).to_be_visible()\n\n\ndef inside(outer, inner):''')\nrep('''            code, ai, you = rows(pg)\n            assert code.startswith((\"Passed:\"''','''            expect(pg.get_by_test_id(\"how-summary\")).to_be_visible()\n            for k in (\"how-chip-code\", \"how-chip-ai\", \"how-chip-you\"):\n                assert pg.get_by_test_id(k).count() == 1, (iid, k)\n            open_panel(pg)\n            code, ai, you = rows(pg)\n            assert code.startswith((\"Passed:\"''')\nrep('''    tok = make(); e = item(tok, \"e1\"); assert e[\"prepared\"] is True\n    open_item(page, tok, \"e1\"); wait_loaded(page)\n''','''    tok = make(); e = item(tok, \"e1\"); assert e[\"prepared\"] is True\n    open_item(page, tok, \"e1\"); wait_loaded(page); open_panel(page)\n''')\nrep('''    open_item(page, tok, \"a1\", step=\"bills\"); wait_loaded(page)\n    assert page.get_by_test_id(\"how-prepared\").count() == 0''','''    open_item(page, tok, \"a1\", step=\"bills\"); wait_loaded(page); open_panel(page)\n    assert page.get_by_test_id(\"how-prepared\").count() == 0''')\nrep('''    open_item(page, tok, \"f_gap_r6_r7\"); wait_loaded(page)\n    assert page_verdict(page) == \"Not needed\"''','''    open_item(page, tok, \"f_gap_r6_r7\"); wait_loaded(page); open_panel(page)\n    assert page_verdict(page) == \"Not needed\"''')\nrep('''    tok = make(); open_item(page, tok, \"e1\"); wait_loaded(page)\n    assert rows(page)[2] == \"Waiting for you.\"''','''    tok = make(); open_item(page, tok, \"e1\"); wait_loaded(page); open_panel(page)\n    assert rows(page)[2] == \"Waiting for you.\"''')\nrep('''    open_item(page, tok, \"e2\"); wait_loaded(page)\n    code, ai, _ = rows(page)\n    assert page_verdict(page) == \"Disputes\"''','''    open_item(page, tok, \"e2\"); wait_loaded(page); open_panel(page)\n    code, ai, _ = rows(page)\n    assert page_verdict(page) == \"Disputes\"''')\nrep('''    open_item(page, tok, \"e1\"); wait_loaded(page)\n    code, ai, you = rows(page)\n    assert \"couldn't load\"''','''    open_item(page, tok, \"e1\"); wait_loaded(page); open_panel(page)\n    code, ai, you = rows(page)\n    assert \"couldn't load\"''')\n# layout test\ni=s.index(\"def test_at_1440x900_the_panel_keeps\"); j=s.index(\"def test_at_390px\")\ns=s[:i]+'''def test_at_1440x900_the_panel_never_pushes_a_highlighted_word_or_the_primary_action_out_of_view(pw, make):\n    tok = make(); b, pg = sized(pw, 1440, 900)\n    try:\n        seen = watch(pg)\n        opened = 0\n        for step, iid in ((\"timeline\", \"e1\"), (\"timeline\", \"e2\"), (\"timeline\", \"e4\"), (\"timeline\", \"f_gap_r6_r7\"), (\"timeline\", \"e6\"), (\"bills\", \"a1\")):\n            open_item(pg, tok, iid, step=step); wait_loaded(pg); settle(pg, 200)\n            src = pg.get_by_test_id(\"card-source\").bounding_box(); how = pg.get_by_test_id(\"how-checked\").bounding_box()\n            assert how[\"y\"] >= src[\"y\"] + src[\"height\"] - 2, \"the panel sits under the record, not over it\"\n            marks = pg.locator(\"[data-testid=card-source] mark\")\n            assert marks.count() >= 1\n            for i in range(marks.count()):\n                m = marks.nth(i).bounding_box()\n                assert m[\"y\"] >= src[\"y\"] - 1 and m[\"y\"] + m[\"height\"] <= src[\"y\"] + src[\"height\"] + 1, f\"{iid}: highlighted word {i} is in the record window\"\n            opened += pg.get_by_test_id(\"how-code\").is_visible()\n            expect(pg.get_by_test_id(\"how-summary\")).to_be_visible()\n            assert pg.get_by_test_id(\"answer-yes\").is_visible() and pg.evaluate(\"document.documentElement.scrollHeight <= window.innerHeight\")\n        assert opened >= 1, \"where there is room the rows are open without a click\"\n        assert seen == [], seen\n    finally:\n        b.close()\n\n\n'''+s[j:]\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/e2e/guided/test_t211.py tests/e2e/guided/test_round2.py -q 2>&1 | tail -15",
 "timeout": 400000
}
````

### User / tool · 2026-11-03T04:49:16.807Z

**tool result**
````
    def test_your_decision_shows_in_the_you_row(page, make):
        seen = watch(page)
        tok = make(); open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
        assert rows(page)[2] == "Waiting for you."
        page.get_by_test_id("answer-yes").click(); settle(page, 500)
        open_item(page, tok, "e1"); wait_loaded(page)
>       assert rows(page)[2] == "You kept it in the letter."
E       AssertionError: assert '' == 'You kept it in the letter.'
E         
E         - You kept it in the letter.

tests/e2e/guided/test_t211.py:96: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/guided/test_t211.py::test_your_decision_shows_in_the_you_row
1 failed, 39 passed in 50.09s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:49:19.704Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/guided/test_t211.py\"; s=open(p).read()\ni=s.index(\"def test_your_decision_shows\"); j=s.index(\"# ----\", i)\nblk=s[i:j].replace('open_item(page, tok, \"e1\"); wait_loaded(page)\\n','open_item(page, tok, \"e1\"); wait_loaded(page); open_panel(page)\\n').replace('open_item(page, tok, \"a1\", step=\"bills\"); wait_loaded(page)\\n','open_item(page, tok, \"a1\", step=\"bills\"); wait_loaded(page); open_panel(page)\\n')\ns=s[:i]+blk+s[j:]\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/e2e/guided/test_t211.py -q 2>&1 | tail -5",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T04:49:39.813Z

**tool result**
````
.................                                                        [100%]
17 passed in 19.04s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:49:40.561Z

Now rebuild the commit tree and rerun the full e2e from a fresh archive (without `-x`).

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:49:42.562Z

**tool call — Bash**
````
{
 "command": "node --check app/frontend/guided/step2.js && node --check app/frontend/guided/step3.js && node --check app/frontend/guided/app.js && IDX=/private/tmp/claude-501/scratch211/idx3 && GIT_INDEX_FILE=$IDX git read-tree HEAD && GIT_INDEX_FILE=$IDX git add app/frontend/guided/app.js app/frontend/guided/core.js app/frontend/guided/index.html app/frontend/guided/review.js app/frontend/guided/step2.js app/frontend/guided/step3.js app/frontend/guided/how.css app/frontend/guided/how.js app/frontend/guided/validation-ladder.svg tests/e2e/guided/test_t211.py tests/e2e/guided/test_t206.py && T=$(GIT_INDEX_FILE=$IDX git write-tree) && echo $T && mkdir -p /private/tmp/claude-501/scratch211/archB && git archive $T | tar -x -C /private/tmp/claude-501/scratch211/archB && echo ok"
}
````

### User / tool · 2026-11-03T04:49:44.496Z

**tool result**
````
6e16e9a30bdfc8ce6bc69aad2e4b94ea23243589
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:49:46.128Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/scratch211/archB && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e -q -p no:cacheprovider > /private/tmp/claude-501/scratch211/fullB.log 2>&1; tail -25 /private/tmp/claude-501/scratch211/fullB.log",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-03T04:49:46.203Z

**tool result**
````
Command running in background with ID: bu7dq1gk1. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bu7dq1gk1.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:49:47.410Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/scratch211/fullB.log; do sleep 10; done; tail -c 1800 /private/tmp/claude-501/scratch211/fullB.log",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T04:59:47.807Z

**tool result**
````
Command did not complete within its 600s timeout and was moved to the background (ID: bywcyp2e2). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bywcyp2e2.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T04:59:50.820Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/scratch211/fullB.log; do sleep 15; done; tail -c 1800 /private/tmp/claude-501/scratch211/fullB.log",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T05:04:21.212Z

**tool result**
````
8: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x1056ce570>
cb = <function Channel.send.<locals>.<lambda> at 0x10e0b2200>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        parsed_st = _attach_api_call_information(
            getattr(task, "__pw_stack__", None) or _capture_stack_trace(),
            is_internal,
            title,
        )
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
E           Call log:
E             - waiting for get_by_test_id("case-stepper").get_by_test_id("case-step").first to be visible
E               62 × locator resolved to hidden <li class="zs-step" data-kind="code" data-status="pass" data-step-id="ingest" data-testid="case-step">…</li>

/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:636: TimeoutError
=========================== short test summary info ============================
FAILED tests/e2e/test_charge_confirm.py::test_a_duplicate_sentence_names_the_other_line_not_an_internal_id
FAILED tests/e2e/test_held_quote_gate.py::test_before_a_rerun_the_case_steps_offer_it_beside_write_the_summary_and_never_say_dismiss
2 failed, 598 passed, 1 skipped in 868.27s (0:14:28)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:04:24.686Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/scratch211/archB && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_charge_confirm.py::test_a_duplicate_sentence_names_the_other_line_not_an_internal_id tests/e2e/test_held_quote_gate.py::test_before_a_rerun_the_case_steps_offer_it_beside_write_the_summary_and_never_say_dismiss -q -p no:cacheprovider 2>&1 | tail -5",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T05:04:29.739Z

**tool result**
````
tests/e2e/test_charge_confirm.py:266: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_charge_confirm.py::test_a_duplicate_sentence_names_the_other_line_not_an_internal_id
1 failed, 1 passed in 3.98s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:04:31.889Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/scratch211/archH && git archive HEAD | tar -x -C /private/tmp/claude-501/scratch211/archH && cd /private/tmp/claude-501/scratch211/archH && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_charge_confirm.py::test_a_duplicate_sentence_names_the_other_line_not_an_internal_id -q -p no:cacheprovider 2>&1 | tail -8",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T05:04:35.254Z

**tool result**
````
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: Likely duplicate This looks like the same charge as “04/09 Therapeutic exercise $150.00” in record 2: $150.00. Counting both would count one service twice.
E       assert ('Therapeutic exercise $150.00' in 'Likely duplicate This looks like the same charge as “04/09 Therapeutic exercise $150.00” in record 2: $150.00. Counting both would count one service twice.' and '$150.00 on 2026-04-09' in 'Likely duplicate This looks like the same charge as “04/09 Therapeutic exercise $150.00” in record 2: $150.00. Counting both would count one service twice.')

tests/e2e/test_charge_confirm.py:266: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_charge_confirm.py::test_a_duplicate_sentence_names_the_other_line_not_an_internal_id
1 failed in 1.39s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:04:38.720Z

**tool call — Bash**
````
{
 "command": "IDX=/private/tmp/claude-501/scratch211/idx3 && T=6e16e9a30bdfc8ce6bc69aad2e4b94ea23243589 && NEW=$(printf 'feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked page, Step 3 reads date_label\\n\\nPanel from the item trace: code check, second AI check verdict + reason (prepared answers say so, D-065), your decision. Header link on every screen; ladder picture copied from submission. e2e test_t211.py (17) at 1440 and 390.\\n\\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\\n' | git commit-tree $T -p HEAD -F -) && echo $NEW && git log -1 --format=%H HEAD"
}
````

### User / tool · 2026-11-03T05:04:38.776Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: git commit-tree rewrites or prunes history; blocked | command: IDX=/private/tmp/claude-501/scratch211/idx3 && T=6e16e9a30bdfc8ce6bc69aad2e4b94ea23243589 && NEW=$(printf 'feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:04:39.652Z

Use `git commit` with the temp index and a pathspec, as instructed.

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:04:41.115Z

**tool call — Bash**
````
{
 "command": "git log -1 --format=%h HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/scratch211/idx3 git commit -q -m \"feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked page, Step 3 reads date_label\n\nPanel from the item trace: code check, second AI check verdict and reason (prepared answers say so, D-065), your decision. Header link on every screen; ladder picture copied from submission. e2e test_t211.py (17) at 1440 and 390.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log -1 --format=\"%h %s\" && git show --stat --format= HEAD | tail -14"
}
````

### User / tool · 2026-11-03T05:05:09.468Z

**tool result**
````
3784bfb
check_secrets: ok (11 file(s) scanned staged)
82217e5 feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked page, Step 3 reads date_label
 app/frontend/guided/app.js                |   9 +-
 app/frontend/guided/core.js               |   1 +
 app/frontend/guided/how.css               |  75 ++++++++++
 app/frontend/guided/how.js                |  54 +++++++
 app/frontend/guided/index.html            |   2 +
 app/frontend/guided/review.js             | 106 ++++++++++++-
 app/frontend/guided/step2.js              |  17 ++-
 app/frontend/guided/step3.js              |  24 ++-
 app/frontend/guided/validation-ladder.svg | 107 +++++++++++++
 tests/e2e/guided/test_t206.py             |   4 +-
 tests/e2e/guided/test_t211.py             | 241 ++++++++++++++++++++++++++++++
 11 files changed, 621 insertions(+), 19 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:05:14.421Z

**tool call — Bash**
````
{
 "command": "git diff --stat 9655f1d 3784bfb | tail -5; B=\"python3 tools/board.py\"; $B ac T-211 --check 1 --agent frontend --evidence \"tests/e2e/guided/test_t211.py 17 pass (1440 and 390, no console errors); full tests/e2e from git archive 6e16e9a, E2E_REQUIRE_DB=1: 598 passed, 1 skipped, 2 failed (test_charge_confirm duplicate sentence fails at HEAD too, D-073 wording; test_held_quote_gate passes alone)\" ; $B commit T-211 --sha 82217e5 --agent frontend"
}
````

### User / tool · 2026-11-03T05:05:14.630Z

**tool result**
````
 submission/part2-process.pdf               | Bin 0 -> 259818 bytes
 submission/product-note.md                 |  40 +++++------
 submission/product-note.pdf                | Bin 0 -> 112722 bytes
 submission/validation-ladder.svg           |  12 ++--
 12 files changed, 290 insertions(+), 104 deletions(-)
AC 1 checked: tests/e2e/guided/test_t211.py 17 pass (1440 and 390, no console errors); full tests/e2e from git archive 6e16e9a, E2E_REQUIRE_DB=1: 598 passed, 1 skipped, 2 failed (test_charge_confirm duplicate sentence fails at HEAD too, D-073 wording; test_held_quote_gate passes alone)
T-211: commit 82217e5 recorded
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:05:19.059Z

**tool call — Bash**
````
{
 "command": "diff <(git show HEAD:app/frontend/guided/validation-ladder.svg) submission/validation-ladder.svg | head -30; git status --short submission/validation-ladder.svg"
}
````

### User / tool · 2026-11-03T05:05:19.181Z

**tool result**
````
3c3
<   <desc id="d">A record's text goes to a model that drafts a summary and quote. Rung 1, code, checks the quote word for word and every number. Rung 2, a second model with a different prompt, answers a fixed choice. Code computes the state. Rung 3, the paralegal, accepts, edits or dismisses; a named confirm for a disputed summary is in progress. Code assembles the export from accepted items only. Items that fail are shown in a could-not-verify list and never exported. A separate code-only lane handles dates, gaps and amounts with no model; a model may only point at cut offsets for a paste code cannot split.</desc>
---
>   <desc id="d">A record's text goes to a model that drafts a summary and quote. Rung 1, code, checks the quote word for word and every number. Rung 2, a second model with a different prompt, answers a fixed choice. Code computes the state. Rung 3, the paralegal, accepts, edits or dismisses; a disputed summary needs a ticked "I compared it with the quote" before it can be accepted. Code assembles the export from accepted items only. Items that fail are shown in a could-not-verify list and never exported. A separate code-only lane handles dates, gaps and amounts with no model; a model may only point at cut offsets for a paste code cannot split.</desc>
58,59c58,59
<   <text x="34" y="504" font-size="11.5" fill="#222">In progress (D-066, T-179): a summary the judge disputed</text>
<   <text x="34" y="518" font-size="11.5" fill="#222">will need a named "I compared it with the quote."</text>
---
>   <text x="34" y="504" font-size="11.5" fill="#222">A summary the judge disputed (D-066, T-179) can only be</text>
>   <text x="34" y="518" font-size="11.5" fill="#222">accepted with "I compared it with the quote" ticked.</text>
100,102c100,102
<   <text x="554" y="488" font-size="11" fill="#222">which I found very hard to use; rebuilding as</text>
<   <text x="554" y="502" font-size="11" fill="#222">four steps (D-068), not yet scored. 5 of 5</text>
<   <text x="554" y="516" font-size="11" fill="#222">disputed summaries took one click (T-179)</text>
---
>   <text x="554" y="488" font-size="11" fill="#222">which I found very hard to use; 4 of 5 on</text>
>   <text x="554" y="502" font-size="11" fill="#222">the guided one (D-068). No real paralegal yet.</text>
>   <text x="554" y="516" font-size="11" fill="#222">Before T-179, 5 of 5 disputed took one click</text>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:05:20.024Z

Writer updated the original; re-copy and commit that one file.

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:05:26.234Z

**tool call — Bash**
````
{
 "command": "cp submission/validation-ladder.svg app/frontend/guided/validation-ladder.svg && IDX=/private/tmp/claude-501/scratch211/idx4 && GIT_INDEX_FILE=$IDX git read-tree HEAD && GIT_INDEX_FILE=$IDX git add app/frontend/guided/validation-ladder.svg && GIT_INDEX_FILE=$IDX git commit -q -m \"chore(frontend): T-211 refresh the ladder picture from submission/validation-ladder.svg\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log -1 --format=\"%h\" && git show --stat --format= HEAD | tail -3\nB=\"python3 tools/board.py\"; $B commit T-211 --sha $(git log -1 --format=%h) --agent frontend\n$B handoff T-211 --agent frontend --text \"What changed: every Step 2/3 item has a 'How this was checked' panel (review.js drawHow, fed by GET /items/<id>/trace): Code check (what code verified or what failed, plus 'All N checks'), Second AI check (Agrees / Disputes / Could not check / Not needed + the server's one-line reason, its model; prepared items lead with 'Prepared by our team; the second AI check then checked it against the quote.' per D-065), You (decision or 'Waiting for you'). New page /how-it-works (how.js/how.css, ~150 words, ladder SVG copied from submission/, code vs AI lists, repo doc names) linked from the header on every screen. Step 3 reads service_date.date_label ('record dated' vs 'statement dated'). · Verified: tests/e2e/guided/test_t211.py 17 pass at 1440 and 390 with no console errors; full tests/e2e from git archive (E2E_REQUIRE_DB=1) 598 passed, 1 skipped, 2 failed: test_charge_confirm duplicate-sentence fails at HEAD too (D-073 wording, qa's), test_held_quote_gate passes alone (flaky timeout). · Left: placement rule: panel is under the record on desktop (open only when window height >= 840 and no highlighted word would be pushed out, else folds to three chips, one click opens); on a phone it is at the end of the line card (that card scrolls as one box), closed with chips. The SVG is a snapshot: re-copy when the writer changes submission/validation-ladder.svg. · Surprised: the multi-record warning test (round2) forces the record window to keep every highlight, so the open panel cannot always fit at 1440x900; history.length is 2 on a fresh tab so Back uses G.navigated.\" && $B move T-211 in_review --agent frontend"
}
````

### User / tool · 2026-11-03T05:05:26.320Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: cp submission/validation-ladder.svg app/frontend/guided/validation-ladder.svg && IDX=/private/tmp/claude-501/scratch211/idx4 && GIT_INDEX_FILE=$IDX git read-tree HEAD && GIT_INDEX_FILE=$IDX git add ap
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:05:27.749Z

**tool call — Bash**
````
{
 "command": "cp submission/validation-ladder.svg app/frontend/guided/validation-ladder.svg && GIT_INDEX_FILE=/private/tmp/claude-501/scratch211/idx5 git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/scratch211/idx5 git add app/frontend/guided/validation-ladder.svg"
}
````

### User / tool · 2026-11-03T05:05:28.532Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:05:29.996Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/scratch211/idx5 git commit -q -m \"chore(frontend): T-211 refresh the ladder picture from submission/validation-ladder.svg\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log -1 --format=\"%h\" && git show --stat --format= HEAD | tail -3"
}
````

### User / tool · 2026-11-03T05:05:57.215Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
4e4ff36
 app/frontend/guided/validation-ladder.svg | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:06:01.272Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-211 --sha 4e4ff36 --agent frontend; $B handoff T-211 --agent frontend --text \"What changed: every Step 2/3 item has a 'How this was checked' panel (review.js drawHow, fed by GET /items/<id>/trace): Code check (what code verified or what failed, plus 'All N checks'), Second AI check (Agrees / Disputes / Could not check / Not needed + the server's one-line reason and its model; prepared items lead with 'Prepared by our team; the second AI check then checked it against the quote.' per D-065), You (decision or 'Waiting for you'). New page /how-it-works (how.js, how.css, about 150 words, ladder SVG copied from submission/, code vs AI lists, repo doc names) linked from the header on every screen. Step 3 reads service_date.date_label. · Verified: tests/e2e/guided/test_t211.py 17 pass at 1440 and 390 with no console errors; full tests/e2e from git archive (E2E_REQUIRE_DB=1): 598 passed, 1 skipped, 2 failed (test_charge_confirm duplicate-sentence fails at HEAD too, D-073 wording; test_held_quote_gate passes alone). · Left: panel sits under the record on desktop (open when window height >= 840 and no highlighted word would be pushed out, else folds to three chips, one click opens); on a phone it is at the end of the line card, closed with chips. The SVG is a snapshot of submission/: re-copy if the writer changes it. · Surprised: the multi-record warning test forces every highlight into the record window, so the open panel cannot always fit at 1440x900; history.length is 2 on a fresh tab so Back uses G.navigated.\" && $B move T-211 in_review --agent frontend"
}
````

### User / tool · 2026-11-03T05:06:01.516Z

**tool result**
````
T-211: commit 4e4ff36 recorded
handoff written on T-211
T-211: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T05:06:03.712Z

T-211 is in_review (commits 82217e5 and 4e4ff36). Every Step 2/3 item now has a "How this was checked" panel (code check, second AI check with its reason, your decision), and a "How each answer is checked" page is linked from the header on every screen. Step 3 reads `date_label`.

Full `tests/e2e` from a fresh `git archive` with `E2E_REQUIRE_DB=1`: 598 passed, 1 skipped, 2 failed. `test_charge_confirm` (duplicate-sentence wording) fails at HEAD too, and `test_held_quote_gate` passes when run alone.

The 17 new tests in `tests/e2e/guided/test_t211.py` pass at 1440 and 390 with no console errors. On desktop the panel sits under the record and folds to its three chips when it would push a highlighted word out of view, so it is not always open.
