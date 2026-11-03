# Subagent: Design: guided UI spec + mockup (Design: guided UI spec + mockup)

Source: `agent-a9a12e9667a302e98.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T20:33:04.578Z

You are the lead product designer and frontend engineer for /Users/arsis/zlayt-pm-project, on card T-180 (P0). Claim it with `python3 tools/board.py claim T-180 --agent frontend`.

**The brief, from Chris, verbatim:** "<Chris's message omitted> depending <Chris's message omitted> someone's <Chris's message omitted>. <Chris's message omitted>."

Read D-068 in memory/ORCHESTRATOR_DECISIONS.md (the agreed shape), D-062 to D-067, CLAUDE.md, and memory/contracts/api.md, which is the API you must build on. Do not invent backend features.

**The product.** Synthetic medical records go in. A paralegal checks a treatment timeline the AI drafted, every line tied to a verbatim quote, checks the bill charges, and gets a demand-letter section.

**Deliverable 1: docs/GUIDED_UI_SPEC.md**, an exact spec covering:
1. **"Your cases" home.** Big case cards, each with its 4-step progress (Add records, Check the timeline, Check the bills, Get your letter), a plain "Next:" line and one Continue button, plus "Start a new case".
2. **The fixed step bar** inside a case. It never moves and shows done, current and remaining steps.
3. **Step 1, Add records:** paste, upload or use the sample; a "Read the records" button; records found; then running the AI with plain progress and no jargon.
4. **Step 2, Check the timeline, one item at a time.**
   - Left: the source record with the quote highlighted. Right: the AI's one-line entry.
   - One plain question with two big answers ("Yes, this matches" / "No, leave it out"), plus "Fix the wording", Back, and "Item 3 of 9".
   - Flags (gaps, prior conditions, conflicts) appear as plain-language questions in the same queue.
   - Could-not-verify items appear as "We couldn't check this one: read it and write it yourself, or skip".
   - Disputed items need the D-066 compare confirm.
5. **Step 3, Check the bills, one at a time:** count or don't count, with the D-059/D-064 confirms in plain words, and a plain list of amounts that are never counted.
6. **Step 4, Get your letter:** a preview, Copy and Download, and the internal notes for the attorney. If anything is undecided, show "N items still need a decision", with a button to go back to the first one.
7. **The rest:** empty, loading and error states with actions; honest demo provenance (D-065); a synthetic-data banner; and D-067, so no narrative paragraph.
8. **Visual system:** large type, generous spacing, one accent colour, light and dark mode, and 390px mobile.
9. **API mapping:** the endpoint and field behind every control.

**Deliverable 2: a clickable static mockup.** Put it in artifacts/mockups/guided/ as index.html plus one page per screen, with realistic sample-case content and no backend. Take screenshots at 1440 and 390 into artifacts/screenshots/guided-mockup-*.png.

**Rules.**
- Nothing on a page reflows or moves when you click.
- No collapsing groups, no hidden menus, and no keyboard shortcuts required.
- Every screen answers: where am I, what do I do now, and how do I know I'm done.

Commit with a pathspec, write the handoff, and move the card to in_review. Reply in 4 lines with the mockup path.

### User / tool · 2026-11-02T20:33:04.584Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:07.224Z

**tool call — mcp__ccd_turn__update_plan**
````
{
 "items": [
  {
   "content": "Claim T-180 and read decisions, contract, memory",
   "status": "in_progress"
  },
  {
   "content": "Write docs/GUIDED_UI_SPEC.md",
   "status": "pending"
  },
  {
   "content": "Build clickable static mockup pages",
   "status": "pending"
  },
  {
   "content": "Screenshot at 1440 and 390, verify no reflow",
   "status": "pending"
  },
  {
   "content": "AC evidence, handoff, commit, in_review",
   "status": "pending"
  }
 ],
 "scope": "first_task"
}
````

### User / tool · 2026-11-02T20:33:07.228Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__update_plan hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:08.244Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-180 --agent frontend; python3 tools/board.py show T-180; git status --short | head -30; ls docs artifacts artifacts/mockups 2>/dev/null",
 "description": "Claim card and inspect state"
}
````

### User / tool · 2026-11-02T20:33:08.488Z

**tool result (error)**
````
Exit code 1
T-180 claimed by frontend
---
id: "T-180"
title: "Guided UI design (D-068): exact spec + clickable static mockup of Your cases, the 4 fixed steps, one-item-at-a-time review, bills, letter; grandma-simple, looks nice"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:32:49Z"
updated_at: "2026-11-02T20:33:08Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T20:33:08Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "docs/GUIDED_UI_SPEC.md with every screen, copy, states and the API call behind each control; artifacts/mockups/guided/*.html clickable mockup at 1440 and 390; screenshots", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:32:51Z orchestrator: assigned: frontend
- 2026-11-02T20:33:08Z frontend: claimed

## Handoff (filled when moving to in_review)

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
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
 M app/backend/case_extras.py
MM app/backend/case_list.py
 M app/backend/export.py
artifacts:
m0-smoke
review-evidence
screenshots
t119-r3-e2e-full.txt
t119-r3-mutB.txt
tmp

docs:
CONTRACT.md
LLM_VS_CODE.md
M2M3_COVERAGE.md
RUNBOOK.md
UI_DESIGN_BRIEF.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:10.099Z

**tool call — Bash**
````
{
 "command": "grep -n \"^## D-06[2-8]\" -A 40 memory/ORCHESTRATOR_DECISIONS.md | head -300",
 "description": "Read decisions D-062 to D-068"
}
````

### User / tool · 2026-11-02T20:33:10.195Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:11.090Z

**tool call — Bash**
````
{
 "command": "wc -l memory/contracts/api.md docs/UI_DESIGN_BRIEF.md; cat .claude/agent-memory/frontend/MEMORY.md; ls .claude/agent-memory/frontend/",
 "description": "Check contract size and memory"
}
````

### User / tool · 2026-11-02T20:33:11.191Z

**tool result**
````
     849 memory/contracts/api.md
     267 docs/UI_DESIGN_BRIEF.md
    1116 total
- [T-043 panels conventions](project_t043_panels.md) — plug-in hooks, testid pitfalls, dev harness
- [Office 3D phone conventions](project_office3d_phone.md) — touch ownership, fit-to-box camera, kanban sheet, pitfalls
- [Stepper and AI-check panel](project_stepper_panels.md) — T-081/T-082 hooks, data-item-id pitfall, own-instance recipe
- [Side-by-side viewer](project_sidebyside.md) — T-046 pane hooks, sticky offset, test-id choices
- [Code-check refusals](project_code_check_refusals.md) — T-104 hooks: Change the quote, inline edit refusal, Why lead, picker pitfall
- [Suggestions and confidence](project_suggestions.md) — T-096 ZL.sg hooks, null-append pitfall, test recipe
- [T-060 enterprise polish](project_t060_polish.md) — tokens, keyboard scope, compact rows, one open-item definition and same-list focus advance (r5), test recipe, pitfalls
- [T-136 edit_to_check](project_t136_edit_to_check.md) — server flag, a-key prompt, Dismissed groups, ZLAYT_DB test recipe, open F1 residuals
- [Multi-case UI, conflicts skipped, held quote](project_multicase.md) — T-149/T-151/T-136 r3 hooks, routing, test recipe, pitfalls
- [Uncovered sentences list](project_uncovered.md) — T-144 hooks, refresh rule, lib09 test pitfalls
- [Verify from git archive](feedback_verify_from_archive.md) — temp-index commit recipe, no-console-errors test, confirm-dialog Escape race
- [T-166 MVP polish](project_t166_mvp_polish.md) — one-row header, More actions, dismiss ghost, a/n/x keys, discard confirm, reveal() in tests
- [T-174 MVP finish](project_t174_finish.md) — one first item, one count, section nav + --head-h, Back to review, preview discard, error actions, ghost focus
MEMORY.md
feedback_verify_from_archive.md
project_code_check_refusals.md
project_multicase.md
project_office3d_phone.md
project_sidebyside.md
project_stepper_panels.md
project_suggestions.md
project_t043_panels.md
project_t060_polish.md
project_t136_edit_to_check.md
project_t166_mvp_polish.md
project_t174_finish.md
project_uncovered.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:12.708Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-06[2-8]\" memory/ORCHESTRATOR_DECISIONS.md | head; wc -l memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Locate decisions"
}
````

### User / tool · 2026-11-02T20:33:12.807Z

**tool result**
````
70:| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the total. Charge sources are positively identified: only documents with a billing header (itemized statement, ledger, invoice, UB-04, CMS-1500) can yield a `charge`; clinical notes and discharge summaries yield a charge only from an encounter line, and never once the case holds an itemized bill from the same provider (amended at implementation: a literal ban zeroed the sample, whose charges are stated in visit notes); insurer and unknown documents never can. CPT/HCPCS codes are normalized ('CPT 99213' = '99213') before duplicate matching. Residual: a summary row dressed as a service line can still be accepted by a careless reviewer; it is cited and individually accepted, and listed as accepted debt. | An adversary can always word a ledger past a classifier; the honest claim is a sum of human-accepted, cited lines. | T-140 claims-adjuster r3 |
71:| D-063 | Priority switch (Chris, 2026-11-02): finish a polished MVP. Only P0 cards and UX/UI work proceed; every other non-P0 card is held (blocked with a note) until the MVP is done. In-flight P1 cards finish their current round but get no further rounds unless they block the UI. New review rounds on held areas are not opened; residuals go to SCOPE_CUTS. The M2 re-gate runs as soon as the P0 blockers (T-139, T-155) close. | Chris: "<Chris's message omitted>." | Chris chat |
72:| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this charge", a named confirm ("I checked this is a separate charge for a service"), recorded in the audit trail; it then sums like any accepted charge. Amends D-059 item on reclassify: (b) is promotable with the confirm, (a) never. | The default-deny rule undercounts real ledger lines (lib11 $3,260 vs $6,000); the paralegal must see why and be able to fix it herself, without reopening the overcount paths. | GATE-M2 r2 paralegal |
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "The AI's own answers on these cases are in the evaluation report." A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
74:| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
75:| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
76:| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
      76 memory/ORCHESTRATOR_DECISIONS.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:14.879Z

**tool call — Bash**
````
{
 "command": "grep -nE \"^\\| D-0(02|29|5[0-9]|60|61) \" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-1500",
 "description": "Read related decisions"
}
````

### User / tool · 2026-11-02T20:33:14.963Z

**tool result**
````
10:| D-002 | Every letter line carries a verbatim quote + provider as written + date of service (US long format) + citation placeholder `[Ex. __ / Bates __]`. No short-cite mode. | Ship bar #1 (100% grounded export); adjusters cross-check providers. | T-014 staff-eng F1, privacy B2 |
37:| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
58:| D-050 | Non-English is never auto-verified (2026-11-02, §7.4 after T-085 r3): every item from a record routed Spanish or LANGUAGE_UNCERTAIN is needs_review with the label 'AI translation — check against the original'. The Spanish code checks and the translation judge still run and their failures are shown, but passing them never yields 'verified'. The paralegal's accept is the gate. English routing keeps its normal ladder. | Three rounds showed heuristic Spanish/Portuguese/Italian routing and cue lists keep leaking (4/41 dropped hedges, 1/27 misroutes on fresh lines); making the human the only verifier for translated text removes the silent-pass risk instead of chasing word lists. | T-085 legal-nurse r3 |
59:| D-051 | Code checks bind accept for **every** item (2026-11-02, T-098 review blocker): an item whose current summary fails any D-034/D-047/D-022 code check (e.g. an AI draft 'Pain 5/10' over a quote without 5/10) cannot be accepted, single or batch (422 with the reason; the paralegal must edit it to match the quote), and the export gate blocks it if such a state exists anyway. Only the judge step is exempt for human wording (D-045b); the code rung never is. | A one-click accept exported an invented number. | T-098 staff r1 F1 |
60:| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complete' badge are computed or shown. The existing case-level charge total (D-019, stated charges only) is unchanged. | Five review rounds kept finding ways a per-provider total could silently omit or overwrite a figure; a listing cannot hide a missing line. | T-083 staff r5 |
61:| D-053 | Nothing the model proposes is silently dropped (2026-11-02, T-094 review blocker). A model-only flag or conflict that the judge rejects, or a model-proposed conflict that no code candidate confirms (the no-candidate rule applies to conflicts only; ADR-020), goes to the **could-not-verify tray** with the judge's reason; it is never a flag and never reaches the letter. The eval scores precision on emitted flags only (tray items are not assertions), and reports tray counts separately; R-CO-7's flag-set signature covers flags, not tray items. Conflict candidates from code (T-094) remain the only path to a conflict *flag*; recall gaps in the code rules are listed in SCOPE_CUTS until covered. | Suppressing rejected items to raise precision hid model output from the paralegal, against R-FL-3 and the ladder. | T-094 staff r1 |
62:| D-054 | Summary clauses the quote does not support are removed by code (2026-11-02, after T-094 r2). Before judging, code splits an AI summary into clauses; a clause is removed only when it adds salient content the excerpt lacks: a number or month, a side or a negation (only in a clause sharing no content word with the excerpt), or a procedure/device/drug, body-part or diagnosis term not covered by a word of the same family in the excerpt (amended T-112 r2: faithful paraphrases and abbreviation expansions stay; whole clauses only, never leaving a fragment; e.g. 'splint fitted' when the excerpt is only the pain sentence is removed), and the removal is shown in the item trace ('removed from the summary: not in the quote'). If nothing supported remains, the item goes to the could-not-verify tray. The judge then checks what is left. No prompt change, no fixture re-record. | Ship-bar item 4 flapped ~1 run in 3 on case_02 because the model sometimes summarized beyond its own excerpt; trimming by code is deterministic and keeps 'every statement traces to a verbatim excerpt'. | T-094 r2 handoff |
63:| D-055 | Gaps never exclude records by guessing (2026-11-02, after T-116 r2). Gap endpoints are computed over all dated records, as before T-116. When a gap starts or ends at a record that looks administrative (intake form, records request, bill, affidavit, by header), the gap carries a visible warning ('this gap ends at an intake form, not a visit; check whether treatment continued') and the paralegal decides. No record is silently dropped from gap math. | Two rounds of label heuristics still excluded real visits (', fax', 'records request' in a visit label), inventing gaps; a warning cannot invent a gap. | T-116 paralegal r2 |
64:| D-056 | Amends D-029 (2026-11-02, T-115): curated fixtures may hand-shape extraction and narrative outputs for the demo, but **judge answers are never scripted**: every judge answer the demo or eval replays is a real recorded model output, and a curated file may never shadow a recording for the same key. tests/unit/test_curated_fixtures.py enforces it (empty allow-list). | Scripted judge answers make the ladder's second check fictional; four had been written by hand, one overriding a real recording. | T-115 staff r1/r2 |
65:| D-057 | Rule-filtered model proposals are listed, not dropped (2026-11-02, after T-113). A model-proposed flag that a code rule filters out (e.g. D-032 `objective_negative`: a normal finding is not a flag) goes to a collapsed, counted "Filtered by rule" group in the could-not-verify tray with the rule named; it is never in the timeline or letter and needs no action. | D-053 says nothing the model proposes is silently dropped; trays full of normal findings would be noise, so they are listed collapsed with a count. | T-113 backend question |
66:| D-058 | A re-picked quote does not make the AI summary human-authored (2026-11-02, T-134 r3 / T-136 F-2). When she picks a different quote but keeps the AI summary, the summary is still LLM-made and its judge ran on the old quote, so D-044 still applies: the new summary–quote pair needs judge 1, and her "I compared it with the quote" does not replace it. If the judge cannot answer, the item stays out of the letter and the UI says so and names the way out (write the summary herself, which makes it human text under D-045). | The ladder rule: nothing LLM-made reaches the export without code check, independent judge and human. | T-134 r3 backend question |
67:| D-059 | The letter total is built only from charges a human accepted one at a time (2026-11-02, T-140 adjuster fail). (1) Charges are never batch-accepted. (2) Code marks an amount `unclear` (not totaled, listed in internal notes with its reason) when its line or column label says total/subtotal/balance/balance forward/previous statement/year-to-date/amount due/paid/payment/adjustment/write-off/credit, when it carries a CR suffix or a negative sign, or when it comes from an insurer document (EOB/remittance) restating a provider charge. (3) Code flags a likely duplicate (same date, description and amount on two statements) and a likely total (equals the sum of other charges); such a charge can be accepted only through a confirm step that names the flag. The total line stays (R-EX-8) and sums exactly the accepted charges. | Totals from ledgers failed adversarial rounds whenever accept-all could include restated amounts; one-at-a-time acceptance plus code flags keeps the human as the final check without removing the total paralegals need. | T-140 claims-adjuster r1 |
68:| D-060 | Amends D-059 (2026-11-02, T-140 adjuster r2): charge candidates are **default-deny**. An amount can be class `charge` only when it sits on an itemized service line: a date of service, a service description (CPT/HCPCS/revenue code or a service noun) and the amount on the same line or table row, in a provider bill or ledger. Every other amount (statement-level labels, account summaries, 'last statement', year-to-date, payment history, insurer documents, unlabeled figures) is `unclear` with its reason. Duplicates are matched on normalized date of service + service + amount (any date format). A charge cites its own line by offset, never by text search. | Deny-lists of total/balance wording lost every adversarial round; listing what a charge must look like cannot be outworded. | T-140 claims-adjuster r2 |
69:| D-061 | Pre-accident records: one simple rule (2026-11-02, T-141 after 5 rounds). A record dated before the stated accident date is info-only ONLY when every accident/mechanism word in it is governed by an explicit "prior/previous/earlier" or a negation of prior accidents ("no prior accidents", "denies previous MVA", "Prior accidents: No"). Any other accident or mechanism word, noun or verb (accident, collision, crash, MVC/MVA, rear-end(ed), struck, hit, pedestrian, impact), with or without a date or "last year", makes it a date conflict. No date-distance exemptions. Second closed exemption (accepted after T-141 implementation): a PLURAL accident noun under a history label ('History per patient: car accidents in 2019 and 2022') names several earlier events, not the accident, and is info-only; a singular one ('History: MVC', 'History: rear-ended') is a conflict. A false conflict is the safe direction (D-055). | Five rounds of word-level exemptions kept hiding true conflicts; one closed exemption cannot be outworded. | T-141 r1–r5 |
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:15.277Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T20:33:15.421Z

**tool result**
````
1	# API contract — DRAFT — backend owns from M2
2	
3	Status: drafted by the architect (T-014, round 2). From M2 the backend worker is the sole writer; changes after that go through a card. Frontend may start against the examples below. They use the Appendix A sample case (Jordan Rivera, SYNTHETIC) as stored in `evals/golden/sample.txt`; **every `start`/`end` is an absolute character offset into the case's raw text, and `raw_text[start:end]` equals the quoted string** (verified by a script run for the T-014 handoff). Design rationale: `memory/DECISIONS.md` ADR-002, 005, 006, 007, 009 to 017. Orchestrator decisions: `memory/ORCHESTRATOR_DECISIONS.md` (D-001..D-024). Requirements: `spec/REQUIREMENTS.md`; the conflicts it lists in §8 are resolved in ADR-017.
4	
5	## Conventions
6	- Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
7	- `{token}` is the case id: a random 128-bit URL-safe string. It is the only credential. **There is no case-list endpoint.** An unknown token is `404 not_found`.
8	- Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
9	- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409, re-run of a case that already has decisions only; never an edit or manual entry, D-047), `item_rejected` (409), `unsupported_language` (400, T-085: see Spanish-language records), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503), `busy` (429, T-087: more than two PDF uploads are being read at once; `detail.reason: "pdf_busy"`; retry shortly).
10	- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
11	- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
12	- Untrusted strings (record text, excerpts, summaries) are plain text; clients must insert them with `textContent`.
13	
14	## Endpoint index
15	| Method | Path | Purpose |
16	|---|---|---|
17	| GET | `/api/health` | backend, demo mode, models, limits, banner text |
18	| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
19	| GET | `/api/cases/{token}` | the whole case for the review screen |
20	| PATCH | `/api/cases/{token}` | T-157 rename: body `{title}` -> `{token, name, title}` |
21	| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
22	| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
23	| GET | `/api/cases/{token}/status` | stage and progress |
24	| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
25	| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
26	| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
27	| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
28	| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
29	| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
30	| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
31	| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
32	| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
33	| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset, and (D-064) `count` + `confirm: "separate_charge"` for an amount held back only for a missing detail (see `countable`).  D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
34	| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
35	| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
36	| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
37	| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
38	| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
39	| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
40	| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
41	| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
42	| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |
43	
44	---
45	
46	## GET /api/health
47	```json
48	{ "ok": true, "version": "0.1.0", "synthetic_only": true,
49	  "banner": "Synthetic data only — never paste real records",
50	  "backend": "fixture", "demo_mode": true, "answers": "prepared", "live_enabled": false,
51	  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
52	  "limits": {"max_chars": 60000, "max_records": 40},
53	  "retention_hours": 24,
54	  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
55	  "sample_available": true }
56	```
57	`answers` (T-177, D-065): whose answers the app shows. `prepared` = the curated fixture set (`FIXTURE_SET=curated`): hand-checked by the team, NOT model output; `recorded` = a replay of real model answers (the default fixture dir); `live` = a model answering now. The UI badge follows it: `prepared` -> "Demo: sample answers prepared by our team" (tooltip "The AI's own answers on these cases are in the evaluation report."), `recorded` -> "Demo: recorded AI answers". With `prepared`, `ai_banner` reads "In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item".
58	`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
59	
60	## POST /api/cases
61	Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). A title is plain text (T-157 r2): control, zero-width and bidi-override characters are removed, line breaks and tabs become spaces, runs of white space collapse; blank means no name. A `title` with a `<` or `>` in it, or longer than 120 characters, is refused: `422 invalid_title` with a plain `message` that never repeats the text, and no case is created (the same for the `title` query of `POST /api/cases/pdf`, checked before the PDF is read). The older `name` field is held to the markup rule too, but a `name` longer than 120 characters (a long file name) is cut, not refused. The response carries `title` (what to show; see "Case titles" under `GET /api/cases`).
62	```json
63	{ "name": "Rivera sample", "text": "SYNTHETIC — ...\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, ...\"\n...", "sample": false }
64	```
65	Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
66	```json
67	{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ingested", "source": "paste",
68	  "demo_mode": true, "record_count": 9, "split_method": "code",
69	  "records": [
70	    { "id": "r1", "seq": 1, "source_label": "Austin EMS run report", "date_raw": "2026-01-09", "date_iso": "2026-01-09",
71	      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false,
72	      "char_start": 106, "char_end": 313,
73	      "text": "=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"" } ],
74	  "dates_to_confirm": [],
75	  "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
76	  "warnings": [] }
77	```
78	(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
79	
80	## POST /api/cases/pdf (D-031)
81	Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
82	Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).
83	
84	### PDF hidden text and local OCR (T-087, T-086; D-042)
85	Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server. A page larger than 40 inches on a side is refused (`ocr_page_too_large`, `detail.page`); a larger one under that is rendered smaller than 150 dpi (longest side at most 3500 px, area at most 8 million px); all page images of one upload together are capped at 12 MB (`ocr_images_too_large`). Tesseract runs with a scrubbed environment (no API key or token reaches it). One deadline (10 s, or 165 s with OCR) covers text reading, the hidden-text scan and OCR; when it passes the work stops and the response is `400 bad_request` with `detail.reason: "pdf_timeout"`.
86	
87	**Hidden text.** Every text object is checked against the page as rendered (pypdfium2). Reasons: `invisible_render_mode`, `transparent`, `off_page`, `tiny_font` (under 5 pt effective), `blends_with_background` (a differential render, contrast under 96 levels counts as blending: the page is drawn with and without all text, and the text counts as hidden when the two agree under its box, so white or background-coloured text, text under a cover of any pattern, and text with marks, rules or dots in its box are all caught), `could_not_verify` (the check could not be made exactly, so the text is held back as suspected) `covered_by_annotation` (a form field, stamp or other annotation with an appearance lies over the text; some viewers draw it opaque while the renderer does not), `clipped` (a clipping window shows under half of the text's box) and `not_in_rendered_page` (words in the file's text layer that the renderer did not place on the page, for example text nested deeper than the 40 form levels a page draws). Hidden and suspected text is removed from the case text, so it can never ground a quote, until its page is confirmed. **Fail closed:** a page whose check could not run (the renderer cannot open the file or the page, more than 20000 text objects, or more than 400 hidden pieces, or more than 500 annotations) is `unchecked`: its text is kept out of the case and the page is listed in the report with `unchecked: true`, `count: 0` and a plain `why`, until the paralegal confirms the page with `include_hidden`. Both PDF parsers, the text-layer read (pypdf) and the render scan (PDFium), run in one child process that is killed at the request deadline (HTTP 400 `pdf_timeout`; no work survives it, and no PDF is parsed in the API process). The child has a CPU limit, an address-space limit where the OS enforces one (Linux; macOS refuses it, unverified on Linux here) and a parent-side check of its resident memory every 0.1 s that kills it above 1 GiB on every platform (the pages are then `unchecked`). At most two PDF uploads are processed at once; a third gets `429 busy`. A Popup annotation with an appearance over text counts as a cover (`covered_by_annotation`); one without an appearance does not. A file whose only usable text is hidden or unchecked is refused with `detail.reason: "pdf_only_hidden_text"`, `detail.hidden_text_pages` and `detail.unchecked_pages`.
88	**OCR.** A page with no text left and a picture on it is "scanned". Without `ocr=true` the upload is refused as before (`pdf_no_text_layer`) with `detail.scanned_pages: [..]` and `detail.ocr` (the status object below) so the UI can offer "Read scanned pages (OCR)". With `ocr=true`: `400 ocr_unavailable` (Tesseract missing or too old; `message` is the plain install line, `detail.ocr` the status), `ocr_too_many_pages`, `ocr_failed`, `ocr_check_failed` (the hidden-text check's child process was killed or crashed on this file, so it is not read with OCR; `detail.cause` is `memory`, `child_failed` or `child_died`) and `ocr_render_failed` (the child that draws the pages for OCR was killed or crashed, e.g. ran out of memory). Page drawing for OCR runs in the same killed child process as the hidden-text scan (deadline, CPU and memory limits); the API process never opens the PDF and never retries a failed child itself (T-107). OCR text is quoted exactly as OCR read it.
89	
90	Response and `GET /api/cases/{token}` gain, for PDF cases only:
91	```json
92	"pdf_checks": {
93	  "hidden_text": {"checked": true, "excluded_until_confirmed": true,
94	    "pages": [{"page": 2, "count": 1, "excluded": true, "confirmed": false,
95	               "items": [{"text": "…", "truncated": false, "reasons": ["blends_with_background"], "why": "not visible when the page is shown (the same colour as the page behind it, or covered)"}]},
96	              {"page": 3, "count": 0, "items": [], "unchecked": true, "why": "The page renderer could not read this page, so hidden text could not be checked.", "excluded": true, "confirmed": false}],
97	    "unchecked_pages": [3]},
98	  "ocr": {"requested": true, "ran": true, "scanned_pages": [3], "pages": [3], "engine": "tesseract 5.5.2", "low_conf_words": 12, "items_need_review": true,
99	          "low_conf_rule": "words under 60 confidence, or under 80 when the word has a digit",
100	          "status": {"available": true, "version": "5.5.2", "tested_version": "5.5.2", "languages": ["eng"], "message": "Tesseract 5.5.2 is available."}}},
101	"pdf_pages": [{"page": 3, "start": 0, "end": 812, "source": "ocr", "has_image": true, "mean_conf": 91.2, "words": 120, "low_conf_count": 12,
102	               "low_conf": [{"start": 40, "end": 47, "text": "Chaege:", "conf": 38.0}]}]
103	```
104	`checked: false` means at least one page could not be checked (`unchecked_pages`); those pages are held back like hidden text, so show them as pages to confirm, not as skipped. `pdf_pages[].start/end/low_conf[].start/end` are offsets into the case text; a page confirmed for hidden text carries `hidden_text_included: true`. Every record in a PDF case has `ocr_derived: true|false`.
105	**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the page image was compared). Its trace gains a failing code step `ocr_source` ("Record was not read from a scanned page", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.
106	**`GET /api/cases/{token}/pages/{n}/image`** -> `image/png` (greyscale, 150 dpi) of an OCR'd page, stored with the case and deleted with it; `404 not_found` for a page that has none. The UI shows it beside the page's text.
107	
108	## POST /api/cases/{token}/review/batch (D-031)
109	**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}`.
110	Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. **D-059 (T-140 r2): charges are never batched.** A batch (accept or reset) that includes any amount of kind `charge` is refused whole: `422 CHARGES_NOT_BATCHED`, message "Charges are accepted one at a time, so a charge cannot be part of a batch. Take the charge out and review it by itself; nothing was changed.", `detail.rejected` lists `{id, reason: "charge_in_batch"}` for each charge. Frontend: remove charges from every batch/"accept all" selection and from any select-all; a charge has only the single-item accept/dismiss. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
111	
112	## /api/cases/{token}/export_config (D-031)
113	`GET` returns `{"exhibit": null|string, "bates_prefix": null|string, "bates_start": null|int}`. `PUT` takes the same keys (all optional; omitted or empty means unset) and returns the stored config; `DELETE` clears it and returns the empty config. Validation: `exhibit` and `bates_prefix` up to 20 characters of `A-Za-z0-9 ._-`; `bates_start` an integer 0 to 99999999 (booleans and strings refused); unknown keys refused; any violation is `422 invalid_edit` and nothing changes. Effect on the export only: every letter citation `Source [Ex. __ / Bates __]` becomes `Source [Ex. <exhibit> / Bates <prefix><NNNN>]` with `NNNN` = first number + record number - 1, zero-padded to 4 digits (first number defaults to 1 when only a prefix is set; an unset part stays `__`). With no config the export is byte-identical to the golden. The internal notes never carry exhibit or Bates numbers.
114	
115	## POST /api/cases/{token}/run
116	Request: `{ "confirm_rerun": false }`. Response 202:
117	```json
118	{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "extract", "started_at": "2026-11-02T01:02:03Z" }
119	```
120	Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.
121	
122	## GET /api/cases/{token}/status
123	```json
124	{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "judge_entries",
125	  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
126	  "progress": {"done": 4, "total": 9, "label": "Checking summaries 4 of 9"},
127	  "counts": {"entries": 9, "amounts": 3, "flags": 1},
128	  "error": null, "elapsed_ms": 21540 }
129	```
130	`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a re-run (the extract step made a failure stub, a second check gave no answer, or the flag step was down) and the stored rows it would have overwritten, or deleted as stale, were left exactly as they were; `message` names how many items and which step ("The AI step failed for N items (writing the entries / the second check / finding the flags) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."). **T-146 r3, one rule for every stage:** a re-run never lowers or replaces a *decided* item (accepted, dismissed or edited). If the new output for it fails a check (a stub, a flag made while the flag step was down, no second-check answer) or differs from it (a worse state, a different summary, quote, date, amount or flag evidence, or worse checks inside the same state: a reason code the stored row did not have, a backing second-check answer (agree, supported, conflict) that is now negative, a code check that was true and is now false), the stored row is kept whole and its `ladder.rerun_note` is set to `{kind: "failed" | "disagreed", step, message, at}`; every item view also carries `rerun_note` (the message string, or `null`), to be shown on the item. `run_partial` then also has a sentence "The re-run gave a different result for N items you had already decided; your decision and the earlier result were kept, and each item carries a note." An undecided item is kept the same way only when the new row is a failure over stored output (no note); a new check result on an undecided item stands (a summary that fails the summary-in-quote check goes to the tray). The deadline path adds no note (nothing was redone) and keeps `run_deadline`. A re-run (the case already had entries) where a step failed and there was no earlier result to keep also reads `failed` / `run_partial`: "The AI step failed for N items (writing the entries) on this run, and there is no earlier result to keep. Run it again to retry." **T-161 / T-165, first run:** a first run with a failing step (a second check, the flag step, or the extract step on ANY record) stores its failure stubs and reads `failed` / `run_partial` too, and the export gate lists `RUN_FAILED`. When the extract step failed with nothing to keep, the message ends with "No entry was made for record 4." / "No entry was made for records 2, 3 and 7." and the error carries `records` (the record numbers, ascending; the first record of a duplicate group) and, when the extract step is the whole failure, `extract_only: true`. **Hand-entered exception (D-031/D-053):** a record the paralegal has entered by hand (tray manual entry, `POST /records/{rid}/entry`) is not a failure: it is left out of `records`, and `GET case` `warnings[]` (always `[]` before) carries one `{code: "ENTERED_BY_HAND", record_no, item_id (the could-not-verify placeholder), message: "The AI step could not write an entry for record 6; you entered it by hand."}` per such record (computed on read; the run result carries the same). Entering a record by hand also re-reads an `extract_only` failure: the entered records leave `records` and the message, and when none is left the case reads `ready` with `error: null` (no re-run needed); a failure with any other cause is left as it is. A re-run whose extract fails again for a hand-entered record keeps the pending hand-entered entry (it is not swept as a stale row). A run where every record extracted stays `ready` with `error: null`. A good re-run clears the error and the notes (the row is replaced by the new one). **Second-check wording (T-145/T-146):** the `why` of a `JUDGE_UNAVAILABLE` item reads "JUDGE_NOT_RUN: the second AI check did not run or did not finish..." when no judge ran, and "The second check failed (the AI check was asked and gave no usable answer)..." when the judge was called and gave no answer (`ladder.judge.verdict: "unavailable"`, `reason_code` other than `JUDGE_NOT_RUN`); the state reason code is `JUDGE_UNAVAILABLE` in both. Poll every second. Partial results are readable from the case endpoint while running.
131	
132	## GET /api/cases/{token}
133	**T-157, `title` and `next_action` (GET case, top level):** `title` is the same string `GET /api/cases` shows (see "Case titles" there; never "Untitled case"). `next_action` is `{item_id, kind, reason}` or `null`: the single first thing to do, the same value `GET /api/cases` carries (code only, deterministic; rules under "`next_action`" there). **`rerun_available` (bool, every entry, amount and flag view in this payload, in `GET .../items/{item_id}` `item` and in every review response `item`; not on `tray` items):** whether "Run the second check again" (`POST .../rejudge`) can get an answer for this item now. False in demo mode and with the fixture backend (no live model can answer: `ENABLE_LIVE` is not `1`, `LLM_BACKEND` is `fixture`, or `anthropic-api` has no key), and false after a rerun that got no answer (the last `ladder.rejudge` attempt is `unavailable`; it turns true again only when the item's wording or quote changes and drops those attempts). True otherwise. It says nothing about whether the check is needed: use `second_check_pending` for that. Show the rerun button only when both are true; when `second_check_pending` is true and `rerun_available` is false, say the check cannot run here.
134	
135	Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
136	
137	**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: [..], labels: {<type>: one plain sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}], notes: [{type, code, count, record_nos, stated_date, text}]}`. The four types are `plan_vs_early_end` and `denial_vs_history` (pair rules in `conflict_candidates.py`; a judge classifies each pair), `accident_date` and `provider_name` (structural checks in `conflicts.py`). **`conflict_types` lists only the types that ran on the case**; `labels` has all four. **`skipped`** says why a type did not run, or ran only in part. `reason_code`: `NOT_RUN` (case created, comparison between records not run yet; the two code checks ran at ingest), `STAGE_SKIPPED` (the run hit its time limit before the comparison between records), `RUN_FAILED` (the run stopped; nothing known), `LANGUAGE` (every record is Spanish, uncertain or unsupported: the English wording rules could not find anything; the type is absent from `conflict_types`), `LANGUAGE_PARTIAL` (the type ran, but `record_nos` lists the Spanish/uncertain/unsupported records it did not read), `NO_DATED_RECORD` (no parsed record date; `accident_date`). The language-bound types are `plan_vs_early_end`, `denial_vs_history` and `accident_date`; `provider_name` compares header labels. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). **`notes`** are info lines, never flags, **computed each time the case is read from the current record dates (not stored)**, so `confirm_date` refreshes them together with the accident-date flag: `RECORDS_PREDATE_ACCIDENT` = a single stated accident date is later than N records and none of them has injury, mechanism or accident wording of its own that is not history or negated, so no date conflict is raised; `text` is the sentence to show ("1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."). The decision is by content (T-141 round 3, no "a record is dated that day" shortcut): a record dated before the stated date makes the accident-date conflict when any clause of it has injury, mechanism or accident vocabulary (collision, crash, MVA/MVC, rear-end, struck, "hit by", pedestrian, incident, accident, injury, whiplash, LOC, trauma, impact, fall, airbag, seatbelt and similar) unless that clause is negated within five words ("denies any accidents", "no recent injuries") or is plainly history (a history word right before the word: "prior accident", "history of MVA", not "prior to the collision"; "last year", "N years ago", a full date over a year before the stated date, a month and year more than two months before the record, a bare year before the record's year). A safe false positive beats a hidden conflict: the conflict then compares with the earliest such record. **A case with no stored run summary** (analysed before per-case checks were kept) reports all four types in `skipped` with `NOT_RUN` and `conflict_types: []` (nothing is claimed; the UI renders an empty list as "none checked", not as the default list). `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together.
138	
139	**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
140	```json
141	{
142	  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ready", "demo_mode": true,
143	  "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
144	  "records": [
145	    { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
146	      "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
147	      "sentences": [ {"text": "Dx: cervical strain;", "start": 396, "end": 416}, {"text": "concussion without loss of consciousness.", "start": 417, "end": 458}, {"text": "CT head negative.", "start": 459, "end": 476},
148	                     {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ],
149	      "uncovered": [] } ],
150	  "undated_entries": [],
151	  "entries": [
152	    { "id": "e2", "seq": 2, "record_ids": ["r2"], "date": "2026-01-09", "date_status": "parsed",
153	      "provider": "Central ER discharge summary",
154	      "summary": "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
155	      "ai_drafted": true, "source_kind": "record",
156	      "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
157	      "excerpt_start": 396, "excerpt_end": 532,
158	      "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
159	      "review_status": "pending", "edited": null, "duplicate_note": null,
160	      "ladder": {
161	        "item_id": "e2", "backend": "fixture",
162	        "generator": {"model": "claude-sonnet-5-5", "prompt_version": "extract_v1", "call_id": "c12",
163	                      "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T00:50:00Z"},
164	                      "output": {"summary": "Diagnosed with cervical strain ...", "excerpt": "Dx: cervical strain; ..."}},
165	        "code_checks": {"excerpt_verbatim": true, "excerpt_whole_sentence": true, "qualifier_carried": true,
166	                        "date_provider_from_header": true,
167	                        "summary_tokens_not_in_excerpt": [], "highlight_found": true},
168	        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": "c21", "verdict": "supported"},
169	        "state": "verified",
170	        "human": {"action": null, "edited_text": null, "at": null} }
171	    } ],
172	  "amounts": [
173	    { "id": "a1", "record_ids": ["r2"], "entry_id": "e2", "text": "$6,240", "value_cents": 624000, "kind": "charge",
174	      "excerpt": "ER charges: $6,240.", "excerpt_start": 533, "excerpt_end": 552,
175	      "state": "verified", "reasons": [], "why": "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
176	      "review_status": "pending", "edited": null, "duplicate_note": null,
177	      "ladder": {
178	        "item_id": "a1", "backend": "fixture", "generator": null,
179	        "code_checks": {"amount_in_text": true, "classified_by": "rule:charge_label", "injection_tag": false, "highlight_found": true},
180	        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c31", "verdict": "agrees"},
181	        "state": "verified", "human": {"action": null, "edited_text": null, "at": null} } },
182	    { "id": "a3", "record_ids": ["r4"], "entry_id": "e4", "text": "$185", "value_cents": 18500, "kind": "rate",
183	      "excerpt": "Charge per visit $185.", "excerpt_start": 929, "excerpt_end": 951,
184	      "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
185	      "why": "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled.",
186	      "review_status": "pending", "edited": null, "duplicate_note": null, "flag": null, "confirm_required": false, "accept_effect": "acknowledge", "judge_required_for_export": false,
187	      "not_counted_reason": "This figure is a rate, not a charge, so it is not added to the total.", "countable": false, "count_confirm": null,
188	      "ladder": {"item_id": "a3", "backend": "fixture", "generator": null,
189	        "code_checks": {"amount_in_text": true, "classified_by": "rule:per_unit", "injection_tag": false, "highlight_found": true},
190	        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c33", "verdict": "agrees"},
191	        "state": "needs_review", "human": {"action": null, "edited_text": null, "at": null}} } ],
192	  "totals": {
193	    "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"},
194	    "pending": {"cents": 839000, "count": 2, "label": "Pending review"},
195	    "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"},
196	    "not_totaled": [{"id": "a3", "kind": "rate", "text": "$185"}],
197	    "possible_overlaps": []
198	  },
199	  "flags": [
200	    { "id": "f_gap_r6_r7", "type": "gap", "category": "gap_over_30", "source_kind": "record",
201	      "title": "Gap of 73 days",
202	      "explanation": "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).",
203	      "computed": {"from": "2026-03-06", "to": "2026-05-18", "days": 73, "threshold": 30, "from_record": "r6", "to_record": "r7"},
204	      "evidence": [
205	        {"record_id": "r6", "excerpt": "Date: 2026-03-06", "start": 1107, "end": 1123},
206	        {"record_id": "r6", "excerpt": "Source: Capital PT, visit 9", "start": 1124, "end": 1151},
207	        {"record_id": "r7", "excerpt": "Date: 2026-05-18", "start": 1242, "end": 1258},
208	        {"record_id": "r7", "excerpt": "Source: Hill Country Pain Management, new patient", "start": 1259, "end": 1308} ],
209	      "origin": "code", "reviewer_note": null,
210	      "state": "verified", "reasons": [], "why": "Calculated by code from two dates read from the record headers.",
211	      "review_status": "pending", "edited": null,
212	      "ladder": {"item_id": "f_gap_r6_r7", "backend": "fixture", "generator": null,
213	        "code_checks": {"dates_parsed": true, "days": 73, "threshold": 30, "evidence_grounded": true, "unconfirmed_date_in_span": false},
214	        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
215	    { "id": "f_acc_1", "type": "conflict", "category": "accident_date_after_treatment", "source_kind": "record",
216	      "title": "Stated accident date is later than recorded treatment",
217	      "explanation": "Stated accident date 2026-01-19 (“Date of accident per intake form: 2026-01-19.”) is later than the first recorded treatment, 2026-01-09 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.",
218	      "computed": {"stated_dates": ["2026-01-19"], "earliest_record_date": "2026-01-09"},
219	      "evidence": [
220	        {"record_id": "r7", "excerpt": "Date of accident per intake form: 2026-01-19.", "start": 1407, "end": 1452},
221	        {"record_id": "r1", "excerpt": "Date: 2026-01-09", "start": 123, "end": 139},
222	        {"record_id": "r2", "excerpt": "Date: 2026-01-09", "start": 332, "end": 348} ],
223	      "origin": "code", "reviewer_note": null,
224	      "state": "verified", "reasons": [], "why": "Calculated by code; all three quotes are word for word in the records.",
225	      "review_status": "pending", "edited": null,
226	      "ladder": {"item_id": "f_acc_1", "backend": "fixture", "generator": null,
227	        "code_checks": {"stated_date_phrase": "date of accident", "evidence_grounded": true, "dates_parsed": true},
228	        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
229	    { "id": "f_pat_9", "type": "causation", "category": "patient_report", "source_kind": "record",
230	      "title": "Patient self-report",
231	      "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:17.425Z

**tool call — Bash**
````
{
 "command": "grep -n \"^## \\|^### \" memory/contracts/api.md",
 "description": "List contract sections"
}
````

### User / tool · 2026-11-02T20:33:17.516Z

**tool result**
````
5:## Conventions
14:## Endpoint index
46:## GET /api/health
60:## POST /api/cases
80:## POST /api/cases/pdf (D-031)
84:### PDF hidden text and local OCR (T-087, T-086; D-042)
108:## POST /api/cases/{token}/review/batch (D-031)
112:## /api/cases/{token}/export_config (D-031)
115:## POST /api/cases/{token}/run
122:## GET /api/cases/{token}/status
132:## GET /api/cases/{token}
266:## POST /api/cases/{token}/records/{rid}/confirm_date
287:## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
299:## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
311:### POST /api/cases/{token}/dismissal_suggestions/apply
314:## GET /api/cases/{token}/items/{item_id}  — "Why?"
332:## POST /api/cases/{token}/items/{item_id}/review
380:## T-178 (GATE-M3 chaos): interrupted runs, stale tabs, paste text
388:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
417:## GET /api/cases/{token}/export
568:## GET /api/cases/{token}/audit
590:## Check traces (D-042): per-item stepper, case stepper, judge summary
597:### Step (shared by all three endpoints)
615:### GET /api/cases/{token}/items/{item_id}/trace
647:### GET /api/cases/{token}/trace
679:### GET /api/cases/{token}/judges
695:## POST /api/cases/{token}/rejudge  (D-044)
705:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
727:## GET /api/calibration  (T-099, serves T-090 counts to T-096)
737:## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
772:## Spanish-language records (T-085, D-042)
788:## Summary clause trimming (T-112, D-054)
791:## Dollar amounts in entries (T-139, D-019, R-CH-7, R-EX-8)
806:## DELETE /api/cases/{token}
811:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
844:## Prepared answers (T-177, D-065; amends D-029)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:18.906Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/contracts/api.md",
 "offset": 232,
 "limit": 190
}
````

### User / tool · 2026-11-02T20:33:19.033Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:20.971Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/contracts/api.md",
 "offset": 421,
 "limit": 150
}
````

### User / tool · 2026-11-02T20:33:20.981Z

**tool result**
````
421	{
422	  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
423	  "generated_at": "2026-11-02T01:20:00Z",
424	  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges accepted from these records: $8,390.00",
425	  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
426	  "items": {
427	    "entries": [
428	      {
429	        "id": "e1",
430	        "record_ids": [
431	          "r1"
432	        ],
433	        "edited": false,
434	        "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
435	      },
436	      {
437	        "id": "e2",
438	        "record_ids": [
439	          "r2"
440	        ],
441	        "edited": false,
442	        "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
443	      },
444	      {
445	        "id": "e3",
446	        "record_ids": [
447	          "r3"
448	        ],
449	        "edited": false,
450	        "excerpt": "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
451	      },
452	      {
453	        "id": "e4",
454	        "record_ids": [
455	          "r4"
456	        ],
457	        "edited": false,
458	        "excerpt": "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
459	      },
460	      {
461	        "id": "e5",
462	        "record_ids": [
463	          "r5"
464	        ],
465	        "edited": false,
466	        "excerpt": "Pain 4/10, improving."
467	      },
468	      {
469	        "id": "e6",
470	        "record_ids": [
471	          "r6"
472	        ],
473	        "edited": false,
474	        "excerpt": "Discharged from PT after two missed appointments. Pain 3/10."
475	      },
476	      {
477	        "id": "e7",
478	        "record_ids": [
479	          "r7"
480	        ],
481	        "edited": false,
482	        "excerpt": "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
483	      },
484	      {
485	        "id": "e8",
486	        "record_ids": [
487	          "r8"
488	        ],
489	        "edited": false,
490	        "excerpt": "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
491	      },
492	      {
493	        "id": "e9",
494	        "record_ids": [
495	          "r9"
496	        ],
497	        "edited": false,
498	        "excerpt": "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
499	      }
500	    ],
501	    "amounts": [
502	      {
503	        "id": "a1",
504	        "kind": "charge",
505	        "counted_in_total": true,
506	        "edited": false,
507	        "excerpt": "ER charges: $6,240."
508	      },
509	      {
510	        "id": "a2",
511	        "kind": "charge",
512	        "counted_in_total": true,
513	        "edited": false,
514	        "excerpt": "Charge: $2,150."
515	      }
516	    ],
517	    "flags": [
518	      {
519	        "id": "f_gap_r6_r7",
520	        "edited": false
521	      },
522	      {
523	        "id": "f_acc_1",
524	        "edited": false
525	      },
526	      {
527	        "id": "f_pat_9",
528	        "edited": false
529	      }
530	    ]
531	  },
532	  "totals": {
533	    "charges_cents": 839000,
534	    "charges_count": 2
535	  },
536	  "counts": {
537	    "entries_in_letter": 9,
538	    "charges_in_letter": 2,
539	    "flags_in_notes": 9,
540	    "records_in_letter": 9,
541	    "records_total": 9
542	  },
543	  "excluded": {
544	    "pending": 0,
545	    "dismissed": 0,
546	    "rejected": 0
547	  },
548	  "provenance": {
549	    "generator_model": "claude-sonnet-5-5",
550	    "judge_model": "claude-haiku-5-5",
551	    "backend": "fixture",
552	    "recorded_from": "claude-cli",
553	    "demo_mode": true,
554	    "prompt_versions": [
555	      "extract_v1",
556	      "judge_faithfulness_v1",
557	      "judge_amount_class_v1",
558	      "flags_v1",
559	      "judge_flag_v2"
560	    ],
561	    "edited_count": 0
562	  },
563	  "warnings": []
564	}
565	```
566	Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`.
567	
568	## GET /api/cases/{token}/audit
569	JSON for this case only. **Public/demo (default): metadata only**: no prompt, response, record or edit text. With `ZLAYT_MODE=local` the same call also returns the full prompts and responses and the before/after of each human event (T-040, T-051 privacy check).
570	
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:21.711Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/contracts/api.md",
 "offset": 645,
 "limit": 205
}
````

### User / tool · 2026-11-02T20:33:21.845Z

**tool result (error)**
````
File content (27832 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file. To read it anyway, up to what still fits in your context, call Read again with allow_large: true — only if you genuinely need all of it or the user asked for the whole file.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:23.444Z

**tool call — Bash**
````
{
 "command": "sed -n '647,736p' memory/contracts/api.md | cut -c1-2500",
 "description": "Read trace gate and case list sections"
}
````

### User / tool · 2026-11-02T20:33:23.540Z

**tool result**
````
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

**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below), `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty) and `MONEY_IN_LETTER` (T-139 r4: a line of the final letter text states an amount; one per line, `item_id` the entry or null), all with `item_id` null except `JUDGE_NOT_RUN`, the code-check blockers and `MONEY_IN_LETTER`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored

### GET /api/cases/{token}/judges
```json
{ "token": "k3Jf9x...", "mode": "metadata", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}, "independent_models": true,
  "totals": { "items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1, "human_overrides": 1 },
  "judges": [ { "id": "j1", "label": "Is the summary supported by the quote?", "prompt_version": "judge_faithfulness_v1", "models": ["claude-haiku-5-5"],
                "items": 9, "supported": 8, "partially": 1, "unsupported": 0, "disagrees": 0, "unsure": 0, "unavailable": 0 },
              { "id": "j2" }, { "id": "j3" }, { "id": "j4" } ],
  "rejections": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "verdict": "partially", "reason_code": "DROPS_QUALIFIER",
                    "rationale": "The summary leaves out a qualifier that the quote carries.", "state_reason": "JUDGE_PARTIAL",
                    "model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": "c27", "review_status": "pending" } ],
  "unresolved": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "verdict": "unavailable", "state_reason": "JUDGE_UNAVAILABLE", "model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": null } ],
  "disagreements": [ { "item_id": "a3", "kind": "amount", "type": "judge_objects", "code_says": "charge", "judge_says": "rate (SHOULD_BE_RATE)", "resolution": "needs_review", "review_status": "pending" } ],
  "prompt_versions": ["judge_amount_class_v1", "judge_faithfulness_v1"] }
```
`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says "agreed with all". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. `totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).

## POST /api/cases/{token}/rejudge  (D-044)
Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. Nothing can clear the gate except an answer.
```json
{ "token": "k3Jf9x...", "asked": 12,
  "rejudged": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "review_status": "accepted", "verdict": "supported", "state": "verified", "state_reasons": [] } ],
  "still_unavailable": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "review_status": "accepted", "verdict": "unavailable" } ],
  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
```
`verdict` is the ladder vocabulary (`supported|partially|unsupported|disagrees|unsure|unavailable`). Frontend: after the call, refetch `/trace` (and the case view, since `state` can change).

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

## GET /api/calibration  (T-099, serves T-090 counts to T-096)
Read-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate counts, the statements built from them, the source commit, the backend and the sample size. No case token, no record text, so it works in demo mode with no gate. Any other method is `405`.

Always `200` with one envelope:
- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backend name), `case_count` (the sample size: golden cases pooled), `small_sample` (bool), `source_commit`, `generated_at`, `by_state` (`verified` and `needs_review`, each `{matched, total, cases[]}`), `by_type` (`entry`, `amount`, `flag`, each with the two states as `{matched, total, by_case: {case: [m, t]}}`), `not_scored` (`entry`, `amount`, `flag`, `total`) and `sentences` (`overall` and `by_type`, each state a string).
- `{"status": "missing", "calibration": null, "message": "..."}`: no file yet.
- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range, totals that do not add up, or a statement that does not quote its own `m/t`). The file's contents are never echoed; the reasons go to the server log.

Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or show a percentage; hide the line when `calibration` is null. Nothing is invented: no default numbers appear in any state. `calibration` is served by `app/backend/calibration_route.py`; the route is registered in `create_app` and reads one fixed path.
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:26.950Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/frontend/project_multicase.md; cat evals/golden/sample.txt; ls app/frontend; ls artifacts/screenshots | head; ",
 "description": "Read multicase memory and sample case"
}
````

### User / tool · 2026-11-02T20:33:27.042Z

**tool result**
````
---
name: multicase-overview-detail
description: T-149 multi-case UI hooks (overview.js, r2 merged block), routing, test recipe, pitfalls; plus T-151 conflict-skipped, T-136 r3 held-quote, T-157 rerun_available and T-158/T-160 notes
metadata:
  type: project
---

**Overview (home) and case overview block live in `app/frontend/overview.js` + `overview.css`.** Home = `#view-cases` (hidden unless GET /api/cases answered 200 and no case is open); the paste box stays below it. Detail starts with `[data-testid=case-overview]` (first child of `timeline`), painted from the live case (progress, chips) and from the case trace via the `zl:trace` event that stepper.js `setCache` dispatches.

**Why:** Chris asked for multi-case management (overview + detail). Server numbers are the truth: tests compare screen to GET /api/cases, GET case and /trace.

**How to apply:**
- Routing: `ZL.cases.open(token)` pushState `#/case/<token>`; `All cases` (`btn-all-cases`) pushState home; `popstate` syncs. A hash-only `page.goto` in a test keeps the old timeline on screen: `goto("about:blank")` first.
- Title: overview shows `ZL.niceName(name)` for library names else the API `title`; cached in `ZL.caseTitles[token]` and used by the header.
- Pitfall: hide the `<section>` (`host.closest("section")`), not the inner body div.
- Pitfall: `<details>` default-open set in JS fires a toggle event; record her choice on the summary click, not on toggle.
- Switcher no longer lists cases (only the synthetic library); `details.cs-details` summary reads "Add a synthetic case".
- Test recipe: `E2E_BASE_URL=http://127.0.0.1:<port> ZLAYT_DB=<file>` against your own `python -m app.main` (PORT/HOST/ZLAYT_MODE=local/LLM_BACKEND=fixture); the full e2e takes 15+ min when other agents load the machine, run it in the background on a worktree copy.
- Screenshots: `ZLAYT_SCREENSHOTS=1 pytest tests/e2e/test_multicase.py -k screenshots` writes artifacts/screenshots/multicase-*.png (wait for `co-gate-verdict` before shooting).

**Held re-picked quote (T-136 r3):** `ZL.secondCheckPending` reads the server `second_check_pending`; a rerun is offered for a held item only until the blocker carries `rerun_no_answer` (then only "Write the summary", `btn-write-summary-case`). Helpers in stepper.js: `S.isHeld`, `S.HELD_CAN_RERUN`, `S.HELD_NO_RERUN`.
**Conflicts group (T-151):** `checks.skipped[]` box (`conflict-skipped`), `checks.notes[]` (`conflict-note`), always-visible `conflict-not-checked-line`; a skipped type is not in the Checked list.

**T-149 round 2 (what changed, read before touching overview.js):**
- Detail = ONE block `case-overview` = `.co-main` (rebuilt by `paintHead` on zl:trace / zl:cases) + `.co-slot` (persistent: timeline.js appends `todo-strip` and `checks-card` into it). `paintHead` must never `clear(box)`; it clears only `.co-main`. `main.append(null)` stringifies "null": filter children.
- Chips (`callouts`): green `*-chip-ready` "Everything decided" only when nothing undecided; gate passes with undecided items = amber `*-chip-can-export` "Can export \u2014 N not reviewed (they stay out of the letter)"; `need-review-count` is the block's needs chip (the strip's count text is gone). `hitl.needs_review` from the list is state-based and never falls: use `needs_review_open` if the server sends it, else min(needs_review, pending+edits).
- "Do this first" = `summary.next_action` (list, refreshed 700 ms after each decision) else `case.next_action`; hidden when it names an item she already decided. While shown, CSS hides the rail's `case-next-action` (so tests that read that line must null next_action, see test_edit_to_check).
- Rerun: `S.rerunAvailable()` = any item `rerun_available === true`; otherwise `S.rerunButton` returns `rerun-unavailable` text. Fixture backend says false everywhere: specs that press rerun use `LiveRerun` / `JudgeNotRun` (conftest) to play a live backend.
- Titles: `ZL.titleOf` (library names keep niceName; else server `title`). Rename = PATCH {title} via `btn-rename-case` (inserted after #case-name by overview.js); create sends `title` from `input-title`.
- Keys: one capture-phase document keydown (j/k/arrows/Home/End); `cases-list[data-ready=true]` marks the first settled paint; rows are rebuilt only when their signature changed (a poll no longer drops focus).
- CSP blocks eval: `page.wait_for_function("string")` and `add_style_tag` fail in this app; use `expect(...).to_be_focused()` and element.style.
- 390x844: first entry date line ~804 px with a do-first line; phone CSS hides Start review when do-first is shown, jump list sits in `<details todo-more>`.
- T-158: refused-Accept box is scrolled by `showRefusalInView(id)` (several passes). T-160: the uncovered link is inserted after `.chip--rec` in the head, costs <=2 px.

**T-149 round 3 (read before touching overview.js / the 390 layout):**
- Do this first = `itemLabel(c, id)` (entry "Mar 9, 2026 entry (record 1)", flag title + records, amount text + record) in `<strong data-testid=do-first-item>`, then the server's reason. No next_action but items pending: synthetic "Review the remaining n items." (Go to it -> review). Start review is CSS-hidden whenever `.co[data-do-first]` (one first step at every width); `.co[data-done]` hides the case-checks "What you need to do".
- Case checks verdict (stepper.js caseRail): server `verdict.code ready` + gate warnings count > 0 renders amber `zs-v-ready_for_decision` with the chip's words; summary row says "Can export — N not reviewed"; "Ready to export" only when nothing is unreviewed. The step title "Ready to export?" still exists: tests must use `Ready to export(?!\?)`.
- Phone (<=768): `#review-body > [data-testid=timeline]` is a flex column, `.co` and `.co-slot` are `display: contents` (so `case-overview` has NO bounding box: use `.co-main`), order puts the jump strip + case checks AFTER the queue. First Accept at 390x844 is ~875 px (was 1062); the entry date/summary are on the first screen, the Accept row is just below.
- Overview: `cases-keys` hint line (hidden on phone), skeleton rows (`cases-skeleton`, count remembered in sessionStorage zl.caseRows), failure sentence "We could not load your cases..." hides filters, focus goes to `#cv-h` after a successful Retry.
- Dev loop: the shared tree's backend breaks while others edit it (analysis "failed" in the working tree); serve a `git archive HEAD` copy with `.venv` symlinked and a sync script that cp's only my frontend files and tests.
SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data

=== Record 1 ===
Date: 2026-01-09
Source: Austin EMS run report
Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

=== Record 2 ===
Date: 2026-01-09
Source: Central ER discharge summary
Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."

=== Record 3 ===
Date: 2026-01-16
Source: Dr. Alvarez, primary care
Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."

=== Record 4 ===
Date: 2026-01-23
Source: Capital PT, initial evaluation
Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."

=== Record 5 ===
Date: 2026-02-20
Source: Capital PT, visit 8
Excerpt: "Pain 4/10, improving. Patient reports missing 3 days of work."

=== Record 6 ===
Date: 2026-03-06
Source: Capital PT, visit 9
Excerpt: "Discharged from PT after two missed appointments. Pain 3/10."

=== Record 7 ===
Date: 2026-05-18
Source: Hill Country Pain Management, new patient
Excerpt: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."

=== Record 8 ===
Date: 2026-05-29
Source: Austin Imaging, cervical MRI
Excerpt: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150."

=== Record 9 ===
Date: 2026-06-12
Source: Hill Country Pain Management, follow-up
Excerpt: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."

api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
overview.css
overview.js
review.css
review.js
sections.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
suggestions.css
suggestions.js
switcher.js
timeline.js
tokens.css
uncovered.css
uncovered.js
judge-panel-1440.png
judge-panel-390.png
judges-unchecked-1440.png
judges-unchecked-390.png
m0-board-mobile.png
m0-board.png
multicase-detail-1440.png
multicase-detail-390.png
multicase-detail-steps-1440.png
multicase-detail-steps-390.png
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:31.032Z

**tool call — Bash**
````
{
 "command": "cat evals/golden/sample.export.expected.txt; ls evals/golden/ | head -30",
 "description": "Read golden export for sample"
}
````

### User / tool · 2026-11-02T20:33:31.115Z

**tool result**
````
=== LETTER_TEXT (block 1: paste into letter) ===
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

January 9, 2026 — Central ER discharge summary
Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."

January 16, 2026 — Dr. Alvarez, primary care
Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."

January 23, 2026 — Capital PT, initial evaluation
Cervical range of motion reduced approx. 40%; plan of care 12 visits.
Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."

February 20, 2026 — Capital PT, visit 8
Pain 4/10, improving.
Source [Ex. __ / Bates __]: "Pain 4/10, improving."

March 6, 2026 — Capital PT, visit 9
Discharged from physical therapy after two missed appointments; pain 3/10.
Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."

May 18, 2026 — Hill Country Pain Management, new patient
New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."

May 29, 2026 — Austin Imaging, cervical MRI
C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."

June 12, 2026 — Hill Country Pain Management, follow-up
Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."

BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
=== INTERNAL_NOTES_TEXT (block 2: do not send) ===
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.

AMOUNTS NOT TOTALED
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.

DAMAGES MENTIONS (not charges)
- Record 5 (Capital PT, visit 8, February 20, 2026): "Patient reports missing 3 days of work."

FUTURE TREATMENT RECOMMENDED (no cost stated)
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.

BILLS TO REQUEST (entry in the letter, no accepted charge)
- Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management.

RECORDS NOT IN THE TREATMENT SECTION
- none (9 of 9 records included)

EDITED ITEMS
- none

PENDING ITEMS NOT INCLUDED
- none
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:33.979Z

**tool call — Bash**
````
{
 "command": "sed -n '1,80p' docs/UI_DESIGN_BRIEF.md; grep -n \"localStorage\\|api/cases'\" app/frontend/*.js | head -20; sed -n '1,60p' app/frontend/tokens.css",
 "description": "Read design brief, token storage, tokens"
}
````

### User / tool · 2026-11-02T20:33:34.073Z

**tool result**
````
# UI design brief (T-060 pass 1, DRAFT for frontend and the UX reviewer)

Status: draft by researcher; the frontend card T-060 owns implementation and may amend values with a note. Evidence for the choices is in
`research/ui-references.md` (sources actually opened; legal-tech pages are marketing text, so their lessons are marked as inferences there).
Binding product rules this brief must not break: `spec/REQUIREMENTS.md` R-RV-1..9, R-ST-1, R-TL-5; D-001 (adverse facts live in internal notes);
D-010/D-011 (accept / edit / dismiss, nothing accepted by default, no batch accept); D-019 (one total line); D-022 (self-report per quote);
ADR-005/013 (code composes state and flag text; the UI never invents wording).

**Design stance.** A quiet, dense, document-first review tool, closer to a claims workbench than to a marketing page. The reader is a paralegal who must
verify about twenty items against a source record. Everything that helps her check (quote, record, state, who made it) is visible without a click;
everything decorative is removed. No gradients, no emoji, no illustration except empty states, one accent color, status always shown with shape and word.

---

## 1. Type

Font stack: `"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif` (no web-font download; works offline on the demo Space).
Record text and quotes use the same family at the reading size. Money and counts use `font-variant-numeric: tabular-nums`.
Scale follows Fluent 2's web ramp (opened source) with one extra reading size; sizes are `rem` against a 16 px root so user zoom works.

| Token | px / line-height | Weight | Use |
|---|---|---|---|
| `--t-caption` | 12 / 16 | 400 | metadata, record numbers, chip text, helper text |
| `--t-caption-strong` | 12 / 16 | 600 | chip text, column headers (sentence case, no all-caps) |
| `--t-body-sm` | 13 / 18 | 400 | dense table cells, secondary lines |
| `--t-body` | 14 / 20 | 400 | default UI text, summaries |
| `--t-body-strong` | 14 / 20 | 600 | provider label, entry date, button text |
| `--t-read` | 15 / 24 | 400 | source record pane and evidence quotes (long-form reading) |
| `--t-subtitle` | 16 / 22 | 600 | group headers ("Dates to confirm"), card titles |
| `--t-title` | 20 / 26 | 600 | page section titles |
| `--t-page` | 24 / 32 | 600 | case title only |

Rules: max line length for record text 80 characters (`max-width: 80ch`); never below 12 px; no italics for emphasis except the verbatim quote marks;
quotes are set in `--t-read`, not smaller, because verifying is the job.

## 2. Spacing, shape, elevation

4 px base grid. Tokens: `--s-1 4`, `--s-2 8`, `--s-3 12`, `--s-4 16`, `--s-5 24`, `--s-6 32`, `--s-7 48`. Page gutter 16 px at 375 px, 24 px from 768 px.
Radius: 4 px on controls, chips and inputs; 6 px on cards; none on table rows. Borders instead of shadows: 1 px `--border`; one shadow token only for
menus and the record modal (`0 4px 16px rgb(0 0 0 / 0.16)`). No glass, no blur.

## 3. Density

Default is **comfortable**; a header toggle switches to **compact** and is remembered in `localStorage` (wrapped in try/catch; page works without it).
Row heights follow Carbon's scale (opened source: 24/32/40/48/64, 64 only for two-line rows).

| Surface | Comfortable | Compact |
|---|---|---|
| Table row (charges) | 40 px | 32 px |
| Timeline row (two lines: date + provider, summary) | 64 px minimum, grows with text | 52 px minimum |
| Flag card padding | 16 px | 12 px |
| Button / input height | 36 px | 28 px |
| Touch targets at ≤ 768 px | 44 px min, regardless of density | 44 px |

WCAG 2.2 target-size minimum is 24 px (from the standard; not re-opened in this pass); the 44 px touch rule is the stricter project choice.

## 4. Color tokens, light and dark

Tokens live on `:root`; the dark set sits under `@media (prefers-color-scheme: dark)` and `:root[data-theme="dark"]`, with `:root[data-theme="light"]` winning
over the media query. All ratios below were computed with the WCAG relative-luminance formula (script in Appendix A); text pairs must stay ≥ 4.5:1,
non-text boundaries ≥ 3:1 (WCAG 1.4.3 / 1.4.11, thresholds from the opened SC 1.4.3 page and the standard).

| Token | Light | Dark | Role |
|---|---|---|---|
| `--page` | `#F5F6F8` | `#0E1116` | app background |
| `--panel` | `#FFFFFF` | `#151A21` | cards, rows, record pane |
| `--sunken` | `#EDEFF3` | `#1C222B` | table header, code-ish blocks, disabled areas |
| `--border` | `#D5DAE2` | `#2B3340` | decorative separators only |
| `--border-strong` | `#6F7B8B` | `#7A8696` | input, button and chip outlines |
| `--text` | `#14181F` | `#E7EAEF` | primary text |
| `--text-muted` | `#4A5565` | `#B0B9C6` | secondary text |
| `--text-subtle` | `#5B6676` | `#9AA5B4` | tertiary, timestamps |
| `--accent` | `#0B57D0` | `#8AB4FF` | links, primary button, focus ring |
| `--on-accent` | `#FFFFFF` | `#0E1116` | text on primary button |
| `--accent-soft` | `#E6EFFD` | `#16284A` | selected row, info background |
| `--ok` / `--ok-bg` | `#13613A` / `#E3F3E9` | `#7BD6A0` / `#12301F` | verified, accepted |
| `--warn` / `--warn-bg` | `#6B4400` / `#FFF1CC` | `#F2C265` / `#3A2A0A` | needs review, warnings |
| `--bad` / `--bad-bg` | `#8C1D1D` / `#FCE9E8` | `#FF9A92` / `#401A19` | rejected, errors |
| `--info` / `--info-bg` | `#0B4F9E` / `#E6EFFD` | `#9CC2FF` / `#16284A` | info banners, AI-made badge |
| `--mark` | `#FFE27A` | `#6B5800` | highlighted excerpt inside the record |
app/frontend/app.js:52:  // ---- theme: auto (follow the OS), light or dark. Remembered in localStorage when it is available; the page works without it.
app/frontend/app.js:58:    try { localStorage.setItem("zlayt.theme", t); } catch (_) { /* not remembered */ }
app/frontend/app.js:155:    let saved = "auto"; try { saved = localStorage.getItem("zlayt.theme") || "auto"; } catch (_) { /* no storage */ }
app/frontend/timeline.js:121:    let v = []; try { v = JSON.parse(localStorage.getItem(gapKey(token)) || "[]"); } catch (_) { v = []; }
app/frontend/timeline.js:127:    try { localStorage.setItem(gapKey(token), JSON.stringify(gapMem[token])); } catch (_) { /* not remembered across reloads */ }
app/frontend/suggestions.js:55:  // "Keep showing" is client-side only, and remembered for this browser per case + key (localStorage, wrapped: the page works without it).
app/frontend/suggestions.js:58:    get: (_, k) => { try { return localStorage.getItem(keptKey(String(k))) === "1"; } catch (_e) { return false; } },
app/frontend/suggestions.js:59:    set: (_, k, v) => { try { if (v) localStorage.setItem(keptKey(String(k)), "1"); else localStorage.removeItem(keptKey(String(k))); } catch (_e) { /* not remembered */ } return true; },
/* Design tokens (T-060). The ONE source of values for every stylesheet: palette, type scale, spacing, radii, elevation and interaction states.
   Nothing outside this file defines a colour, a font size, a radius or a shadow. Values and contrast ratios: docs/UI_DESIGN_BRIEF.md section 4 and appendix A.
   Themes: light is the default; dark follows the OS (prefers-color-scheme) unless the header toggle set data-theme on <html>. */
:root {
  color-scheme: light;

  /* ---- palette, light. Text pairs >= 4.5:1, control boundaries >= 3:1. */
  --page: #F5F6F8;            /* app background */
  --panel: #FFFFFF;           /* cards, rows, dialogs */
  --sunken: #EDEFF3;          /* table header, quote blocks, hover wash */
  --border: #D5DAE2;          /* decorative separators only */
  --border-strong: #6F7B8B;   /* inputs, buttons, checkboxes: a boundary that carries meaning (4.3:1 on panel) */
  --text: #14181F;
  --text-muted: #4A5565;
  --text-subtle: #5B6676;
  --accent: #0B57D0;          /* the one primary blue: links, primary button, focus ring */
  --accent-hover: #0948A8;
  --accent-active: #083C8C;
  --on-accent: #FFFFFF;
  --accent-soft: #E6EFFD;     /* selected row, info wash */
  --ok: #13613A;     --ok-bg: #E3F3E9;
  --warn: #6B4400;   --warn-bg: #FFF1CC;
  --bad: #8C1D1D;    --bad-bg: #FCE9E8;
  --info: #0B4F9E;   --info-bg: #E6EFFD;
  --mark: #FFE27A;   --on-mark: #14181F;
  --hover: rgb(20 24 31 / 0.06);     /* wash on any quiet control under the pointer */
  --pressed: rgb(20 24 31 / 0.12);
  --scrim: rgb(14 17 22 / 0.5);

  /* ---- type: 7 sizes (rem against a 16px root so browser zoom works), one family. Line heights are paired. */
  --font: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --t-xs: 0.75rem;     --lh-xs: 1rem;        /* 12/16 caption, chips, record numbers */
  --t-sm: 0.8125rem;   --lh-sm: 1.125rem;    /* 13/18 dense table cells, secondary lines */
  --t-md: 0.875rem;    --lh-md: 1.25rem;     /* 14/20 default UI text, summaries, buttons */
  --t-read: 0.9375rem; --lh-read: 1.5rem;    /* 15/24 verbatim quotes and the source record */
  --t-lg: 1rem;        --lh-lg: 1.375rem;    /* 16/22 group and card titles */
  --t-xl: 1.25rem;     --lh-xl: 1.625rem;    /* 20/26 section titles, one big figure */
  --t-2xl: 1.5rem;     --lh-2xl: 2rem;       /* 24/32 the case title */
  --w-regular: 400;    --w-strong: 600;

  /* ---- spacing: a 4px grid */
  --s-1: 0.25rem; --s-2: 0.5rem; --s-3: 0.75rem; --s-4: 1rem; --s-5: 1.5rem; --s-6: 2rem; --s-7: 3rem;
  --gutter: var(--s-4);

  /* ---- shape: two radii (4 controls, chips and inputs; 6 cards, dialogs and the header). Round markers use 50%. */
  --r-1: 4px; --r-2: 6px;

  /* ---- elevation: borders first; one shadow for things that float (header, menus, dialogs, the source pane) */
  --elev-0: none;
  --elev-1: 0 1px 2px rgb(0 0 0 / 0.08);
  --elev-2: 0 4px 16px rgb(0 0 0 / 0.16);

  /* ---- controls and layout */
  --control-h: 2.25rem;          /* 36px */
  --control-h-sm: 1.75rem;       /* 28px */
  --touch-h: 2.75rem;            /* 44px, used at <= 768px */
  --focus-ring: 2px solid var(--accent);
  --focus-offset: 2px;
  --banner-h: 2rem;              /* the sticky synthetic-data banner */
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:45.919Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-066\\|compared_with_quote\\|compared\\\"\\|\\\"compared\" memory/contracts/api.md | cut -c1-1500; grep -rn \"D-066\\|compared_quote\\|compare_confirm\" app/backend/*.py | head -20",
 "description": "Find D-066 API shape"
}
````

### User / tool · 2026-11-02T20:33:46.013Z

**tool result**
````
app/backend/case_extras.py:46:        elif action == "accept" and review.judge_dispute(row):      # D-066: a disputed summary is accepted alone, with her explicit compare
app/backend/present.py:499:                        **({"compared": e["after"]["compared"]} if (e.get("after") or {}).get("compared") else {}),      # T-179 / D-066: she said she compared it with the quote
app/backend/review.py:298:    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
app/backend/review.py:309:    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
app/backend/review.py:319:    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
app/backend/review.py:348:        if action == "accept" and (err := compare_error(item_id, item, compared)):      # D-066; before any write
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:47.857Z

**tool call — Bash**
````
{
 "command": "sed -n '290,330p' app/backend/review.py; grep -n \"compared\" app/backend/api.py | head; git log --oneline -8; git diff --stat HEAD -- memory/contracts/api.md",
 "description": "Read D-066 implementation"
}
````

### User / tool · 2026-11-02T20:33:47.989Z

**tool result**
````
_DISPUTED = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES"}
_DISPUTE_SENTENCE = {"partially": "The second AI check found this only partly supported by the quote.", "unsupported": "The second AI check found this not supported by the quote.",
                     "disagrees": "The second AI check disagreed with the first result for this item."}


def judge_dispute(item: dict):
    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
    three JUDGE_* reasons counts; unsure and unavailable are not an objection. Code only."""
    j = (item.get("ladder") or {}).get("judge")
    v = j.get("verdict") if isinstance(j, dict) else None
    if v in _DISPUTED:
        return v
    reasons = item.get("state_reasons") or []
    return next((k for k, code in _DISPUTED.items() if code in reasons), None)


def compare_error(item_id: str, item: dict, compared):
    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
    v = judge_dispute(item)
    if not v or compared is True or item.get("review_status") == "accepted":
        return None
    return ReviewError(422, "COMPARE_REQUIRED", {"item_id": item_id, "reason_code": "COMPARE_REQUIRED", "verdict": v,
                       "next_action": {"code": "COMPARE_WITH_QUOTE", "text": "Read it against the quote, then say you compared it", "target": {"item_id": item_id}}},
                       _DISPUTE_SENTENCE[v] + " Read it against the quote, then say you compared it before you accept it.")


def _record_compared(conn, case_id: str, item_id: str, t) -> None:
    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
    ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
    if ev:
        after = json.loads(ev["after_json"]) if ev["after_json"] else {}
        conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "compared": {"at": store.iso(t)}}), ev["id"]))


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
de5cb3a docs(orchestrator): D-068 guided four-step UI redesign (Chris)
7c73294 test(qa): T-045 r2 sensors record (unit 5698, e2e 412, latest.json live, rejected-item claim corrected)
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
ee62967 docs(orchestrator): D-066 disputed accept needs a compare confirm; D-067 cut the drafted paragraph from the MVP UI; scope cuts 22-23
04ea2bf feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
d7ea327 test(qa): T-045 r2: real 375 px overflow check, rejected-item guard (unit + e2e), evals --record-latest points latest.json at the live run; fixture runs no longer replace a live latest.json
0c4284f docs(orchestrator): D-065 honest demo provenance (amends D-029)
d0b04bc test(qa): T-045 M3 sensors re-run on a clean HEAD worktree (unit 5689, e2e 411, letter_check 0, calibration fresh, fixture eval matches live); latest.json stale-pointer finding
 memory/contracts/api.md | 8 ++++++++
 1 file changed, 8 insertions(+)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:50.152Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- memory/contracts/api.md | cut -c1-1800; python3 tools/board.py show T-179 | head -40",
 "description": "See pending contract changes and T-179"
}
````

### User / tool · 2026-11-02T20:33:50.316Z

**tool result**
````
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 069ca92..52cbcd3 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -377,6 +377,14 @@ The frontend does not need to refetch the case.
 - T-138: `POST /items/{id}/review {action: "reset"}` on an edited entry restores the AI wording together with its pre-edit second-check result, code-check record and state (kept in `ladder.pre_edit` as deep copies, plus the earlier `ladder.rejudge` attempts; internal and never returned in any payload); accept then works as before the edit and does not hit `JUDGE_NOT_RUN`. If something else rewrote the state after the edit, only the check result returns.
 - Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
 
+## T-178 (GATE-M3 chaos): interrupted runs, stale tabs, paste text
+
+**Interrupted run (startup recovery).** A run is a thread of the server process. When the process stops (crash, sleep, redeploy) the case would stay `running` for ever. At startup every case still `running` that no thread of this process is running is set to `status: "failed"` with `error: {"code": "run_partial", "interrupted": true, "message": "The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry."}` and `run_finished_at` set. The same happens on any read of a `running` case that has no live thread and whose run started more than 600 s ago. Nothing item-level is touched: accepted, edited and dismissed items stay exactly as they were, the export gate reads `RUN_FAILED` (next action `CONFIRM_RERUN`), `POST .../run` is allowed again (`409 needs_confirm` while decisions exist, then `confirm_rerun: true`), and the re-run follows the T-146 rules (decided items are kept). Frontend: treat `failed` + `error.interrupted` like any `run_partial`: show `error.message` and the Run again button.
+
+**Stale second tab (`stale_item`).** Every item view (`entries[]`, `amounts[]`, `flags[]`, `GET .../items/{id}` `item`, review responses `item`) now has `version`: a number that changes whenever the item changes. `POST .../items/{item_id}/review` accepts optional `version` (the item's `version` as the client last saw it) and/or `expected_status` (its `review_status` as last seen: `pending|accepted|edited|dismissed`). If either differs from the stored item the write is refused with `409 stale_item`, message **"This item changed in another tab; reload to see it."**, `detail: {item_id, review_status, version}` (the current ones), and nothing is written (no review event). Neither sent = no check (older clients). A repeat of a decision that would leave the item as it already is (accept on an accepted item, dismiss on a dismissed one, reset on a pending one) is let through. Other values: `422 invalid_edit` (`version` not a number, `expected_status` not one of the four). **Frontend must:** send `version` and `expected_status` from the item it is showing with every accept, dismiss, reset, edit and count; on `409 stale_item` show `error.message`, refetch the case (or `GET .../items/{id}`) and replace that item; update the stored `version` from every response that carries an item (batch responses do not carry one: refetch). Frontend does not send these yet (card note on T-178).
+
+**Paste text.** Text is normalised before the empty check and the size limits (`ingest.normalize_text`, used by `POST /api/cases`, the demo-gate hash, the pipeline and PDF page assembly): every Unicode format character (category Cf: zero-width space/joiner/non-joiner, word joiner, BOM, bidi marks and overrides, soft hyphen, tag characters) is removed, and a lone UTF-16 surrogate is replaced by U+FFFD. A paste with nothing else in it is `400 bad_request` "Input is empty." and costs no model call; invisible characters do not count toward the 60,000-character limit; the stored case text is the cleaned text (excerpts and offsets index it). Every string in any JSON request body (titles, edits, notes) gets the same surrogate replacement at the door. No paste returns a 500.
+
 ## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
 The paralegal says a dollar figure is, or is not, a billed charge. Taking a figure **out** of the total is always her call; putting one **in** needs evidence. Body: `{ "to": "charge" | "not_a_charge", "note": "optional, 500 chars" }`.
 - `to: "not_a_charge"` on a `charge`: always allowed. The class becomes `unclear` (response `amount.kind: "unclear"`; shown as "not added to the total", never totaled).
---
id: "T-179"
title: "GATE-M3 UI round: D-066 compare-confirm to accept a judge-disputed item (backend enforces 422 without it; batch excludes); D-067 hide the drafted treatment paragraph; UX/a11y minors (h1 on case page, Undo row hidden under sticky header, Try again focus, dismiss announcement overwritten, refused-edit names the words to keep, 320px Theme/Shortcuts/Export)"
milestone: "M3"
role: "frontend"
status: "blocked"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:26:28Z"
updated_at: "2026-11-02T20:32:52Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T20:26:39Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "accepting a disputed item without the confirm is 422 and the UI asks for the compare first (e2e, unit); no narrative control on any page and no narrative in the letter; each listed minor fixed with an e2e or axe check; axe 0 serious/critical and the h1 violation gone", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:26:30Z orchestrator: assigned: frontend
- 2026-11-02T20:26:39Z frontend: claimed
- 2026-11-02T20:32:52Z orchestrator: moved in_progress -> blocked: UI scope superseded by D-068 guided redesign; D-066 (disputed-accept confirm) and D-067 (no narrative) carry into T-181; backend D-066 enforcement still needed

## Handoff (filled when moving to in_review)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:53.975Z

**tool call — Bash**
````
{
 "command": "sed -n '737,770p;791,805p;844,850p' memory/contracts/api.md | cut -c1-1600",
 "description": "Read billing, dollar amounts, prepared answers"
}
````

### User / tool · 2026-11-02T20:33:54.060Z

**tool result**
````
## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs (each EOB service row is a line). Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals`. **No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2 and r4):** no provider totals, no billed/paid/balance sums, no `complete` flag, no running-balance step check, no ledger-versus-EOB check, and no code that asks whether one figure equals, exceeds or differs from another. A printed token is told from another with the same text by its **position** in its record (an offset range), so two equal figures in one excerpt are two entries; the sign of a charge (`detail: reversal`) is read from its printed credit notation, not from its value. The only tests left on numbers are layout (which header a column sits under, whether two offset ranges overlap) and the grounding verifier's substring check. A listing cannot hide a missing line; a sum or a comparison can. The response has exactly `status`, `citation_failures`, `lines`, `unreconciled`, `skipped_records`, `rules`. The only billing total in the product is the case-level charge total of stated charges (D-019, `totals`), unchanged. Unknown token: `404 not_found`.
```json
{ "billing": {
  "status": "listed",                         // listed | citation_failed | none_found. "listed" says only that something was found; it is not a completeness claim
  "citation_failures": [],                    // [{ref, reason}] from the grounding verifier, which the route always runs; non-empty makes status citation_failed
  "lines": [                                  // every figure the records print, in record order, each with a verbatim excerpt and its source record
    { "id": "b3", "class": "charge",          // charge | adjustment | payment | rate | unclear
      "detail": null,                         // null | "reversal" (a charge printed in credit notation, or VOID) | "balance_only" | "eob" (an EOB service row) | see the extra-line details below
      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: ledger | cms1500 | ub04 | eob
      "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
      "billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "adjustment": null, "paid": null, "balance": {"text": "410.00", "cents": 41000, "usd": "$410.00"},
      "unclear": [], "negotiated": false, "unparsed": false,
      "checks": [],                           // LINE_UNCLEAR | NO_DATE_OF_SERVICE (ROW_NOT_PARSED on an unreconciled row)
      "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
      "cites": [ {"record_no": 1, "excerpt": "<same line>"} ] },                // one record: record_nos and cites always name only the line's own record (nothing is merged across records or providers)
    { "id": "b8", "class": "rate", "detail": "rate", "provider": "...", "record_no": 1, "record_nos": [1], "form": "ledger",
      "figure": {"text": "$65.00", "cents": 6500, "usd": "$65.00"}, "other_figures": [], "why": "A rate (per visit, per unit) is a price, not a charge.",
      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"} ] },
    { "id": "b12", "class": "unclear", "detail": "eob", "provider": "Quoinmere Mutual Health Plan", "record_no": 2, "record_nos": [2], "form": "eob",
      "dos": "06/10/26", "code": "97140",                         // code = the EOB's service code; billed/paid/adjustment/balance are null on an EOB row
      "eob": {"billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}},
      "eob_codes": "PR-1, PR-2, CO-45", "unclear": [], "checks": [],    // `eob` is {} and every money token of the row is in `unclear` (text, no value) when a figure could not be read or the row has the wrong number of figures
      "excerpt": "06/10/26  97140  70.00 ...", "cites": [ {"record_no": 2, "excerpt": "<same>"} ] } ],
  "unreconciled": [ { "id": "u1", "provider": "...", "record_no": 1, "form": "cms1500", "class": "unclear", "reason_code": "ROW_NOT_PARSED", "message": "...",
    "excerpt": "<the row, verbatim>", "figures": ["$85.00"] } ],   // rows that carry a figure or a date but fit no layout; never dropped. `figures` holds only the money tokens, not the rest of the line
  "skipped_records": [ {"record_no": 4, "reason_code": "INJECTION_SUSPECTED"}, {"record_no": 5, "reason_code": "UNRECOGNISED_BILLING_FORM"} ],
  "rules": [ "Every figure is listed with the line it was read from; nothing is totaled here, ...", "..." ] } }
```
**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, an **EOB service row** (`detail: eob`; its payer figures are in `eob`, never in `billed`/`paid`), and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adjustment` | `stated_total_balance` (a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`. **Figure fields on an extra line, `other_figures`, a running `balance`, and everything in `eob` are never summed or compared by a client.** `other_figures` (a list of `{text, cents, usd}`, empty when none) holds every OTHER money token printed on a rate, estimate or LOP/lien row, wherever a parser first put it: the running balance on a price row (a no-cents one such as `$315` keeps its text with `cents: null`), a second amount in an LOP or rate sentence (the first amount is the entry, the later ones are its other figures), a printed balance or total on that row. A token on such a row is never also a line of its own, with no exception: on a UB-04 room row the FL 44 figure is the rate entry a
**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept). A running balance that does not follow from the line before it is listed as printed, with no flag. Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. **Nothing is merged or deduplicated across records or providers (T-103 r3):** two providers printing the same row are two lines, a re-sent statement is two lines (one per record, each citing only its own record, so `record_nos` has one entry), and a line is identified by its record and its position in it (`id` follows record order, then position). Only a byte-identical copy of a whole record is dropped, at ingest (`duplicate_of`). CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a charge; the FL 44 figure on a room line is a `rate` and the `0001` line is a printed total. A fee-schedule or per-unit figure is a rate; a table row or a sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate; one shared test, `amounts.has_rate_cue`, also used by reclassify) is a rate even beside the word charge or billed, is listed once, and a `RATE` column's figures are rates too. A ledger-table figure with no cents (`$185`
**Nothing is silently missing (D-049, tested).** After every parser has run, the code reads each billing record again with its own tokenizer and collects every money-shaped token: a `$` figure, a number with two decimals (OCR letters tolerated), and a whole number in an amount position (under a ledger or UB-04 money column, in a prose sentence, in a balance-forward row, in the box of a dateless CMS-1500 service line; dates, times, codes, years and counts of visits/units/days are not tokens, nor is a whole number on a UB-04 revenue-code row that has a decimal figure to its right (the units count), a procedure code pushed into an EOB money column by a money-shaped service slot, or a prose number directly after another money figure; definition in the `app/backend/billing.py` docstring). Each token is a `lines` entry, an `unreconciled` row, an `unclear` figure on its row, or its whole record is in `skipped_records`. A token none of these holds is added to `unreconciled` as a `ROW_NOT_PARSED` row (one already on that row is extended). The test replays every money token of the T-083 probe sets (r1 to r5 reviews, `artifacts/review-evidence/T-083-*`) plus 600 random insertions (seed 20261102) and 5 x 600 more (seeds 1 to 5), and fails if one is missing or if the exact per-record count differs. Repeated summary rows are never overwritten: two balance-forward rows, and a second TOTAL CHARGES / BALANCE DUE / paid / adjustment row (in one record, or in a second statement of the same provider and form family) are all listed (the earlier ones in `unreconciled`, the last as a line; a copy
**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None involves arithmetic. Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, and the response fields `payer_reports`, `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
**Ladder.** All steps are code (parse, cite); there is no model step, so no judge. The human step is reading the view; none of it is exportable.
## Dollar amounts in entries (T-139, D-019, R-CH-7, R-EX-8)
The extract prompt asks the model for the sentences that carry "the treatment, findings, diagnosis, plan or charge", so an entry's summary or quote can state an amount ("Charge per visit $140", "ED charge: $3,915."). The letter prints a dollar figure only in the BILLED CHARGES section (accepted charges and the R-EX-8 total line). Code only (`app/backend/charge_text.py`), no model:
- **Pipeline.** An entry whose summary or quote states a currency figure (`$` figure incl. OCR-noisy `$1,2OO`, `N dollars`, `USD N`) gets state `needs_review` with reason **`CHARGE_TEXT_IN_ENTRY`** (appendix; `why`: it is held out of the letter; dismiss it, or pick a quote without the amount and edit the summary to match). **T-139 round 2: money written without a `$` counts too** when a money word or claim-form field names it: `TOTAL CHARGE 49100`, `AMOUNT PAID 0 00`, `Charges: 3,915.00`, `Cost estimate 4,500`, `Fee 140/visit`, CMS-1500 `24F 25500` and `CPT 99204, 18500, 1 unit`, UB-04 `FL47 4920 00`, Item 28/29/30. Dates, pain scores, doses, visit counts and CPT/ICD codes are never currency. `detail.amounts[]` then holds the label with its figure as written. It is an ordinary queue item; nothing is rejected.
- **Narrowing first (T-139 follow-up, code only).** Before the hold-out, when the quote has several sentences and its currency-bearing sentence(s) sit at the START or END, code drops them (`charge_text.narrow_excerpt`): the narrowed quote is a contiguous run of whole, verbatim sentences (a substring of the model's quote; an amount in the MIDDLE, a single-sentence quote, a quote that is all amounts, or fewer than 2 content words left means no narrowing). The summary is then trimmed against the narrowed quote (D-054, then the trailing-amount-clause rule above). Every rung-1 check re-runs on the narrowed pair (`generator.verify`); it is kept only if the pair states no amount, some summary is left, and no check raises a reason the original pair did not already raise; otherwise the entry keeps its quote and is held as above. Judge 1 runs on the narrowed pair (D-044/D-058), so no answer given for the longer quote is reused; with no answer the entry is `needs_review` with `JUDGE_UNAVAILABLE` (JUDGE_NOT_RUN). The entry's `quote`/`excerpt` and offsets are the narrowed text. `ladder.excerpt_narrowed = {rule: "T-139", original_excerpt, dropped[], summary_removed[], original_summary}` records what code dropped; `ladder.generator.output` keeps the model's own output. Frontend: when `ladder.excerpt_narrowed` is present, say "charge sentence not quoted" next to the quote; the paralegal can still re-pick a longer quote, but a quote with an amount is refused as above. Over the 25 recorded cases, 51 entries stated an amount; 42 are narrowed (39 verified by judge 1, 3 need review for other re
- **Round 3: more ways to write money (adjuster r2), same hold.** Also counted as currency: another sign or code next to a figure (`\u20ac185`, `185 \u20ac`, `\u00a31,200`, `1.200,00 \u20ac`, full-width `\uff04185`, `EUR 185`, `185.00 EUR`, `CAD`, `MXN`, `GBP`, `AUD`), amounts in words before a currency noun (`one hundred eighty-five dollars`, `a thousand bucks`, `400 pesos`, Spanish `cuatrocientos d\u00f3lares`), more money words with a money-shaped figure (`Total: 1,200.00`, `Amount: 1,200.00`, `Bill 3,915`, `Invoice total 1,567.05`, `Lien amount 4,000`, `Out-of-pocket 1,200.00`, `Self-pay rate 185`, `Network discount`, `Adjustment -1,250.00`, `Medical specials total`, `Saldo`, `Costo`, `Fee 95`), `185 per visit`, and a figure inside a patient's statement (`Patient states the ER bill was 3,915`, `she owes the chiropractor about 2,400`, `charged me fifteen hundred`). Plain clinical number words (`twelve visits`, `two weeks`, `twenty minutes`) and figures with a unit are never money; `type of bill 0111` is not. **Closed world, written down:** not detected are slang or shorthand (`one eighty-five each`, `6.5k`, `x 185`), bare decimals with no money word (`Initial exam 185.00`), per-mile rates, and Spanish number words other than the hundreds, so a record that states money only like that still reaches the carrier letter if the paralegal accepts it; the reviewer reads every quote before accepting. **T-139 round 4 (structural, after the round cap): ONE detector.** All of the above lives in one module, `app/backend/money.py` (`hits`, `strings`, `has_money`, `of_kind`, `dollar_st
- **Accept (single, batch, and `edit`, D-051 choke point).** Refused `422 CODE_CHECK_FAILED` with `detail = {item_id, reason_code: "CHARGE_TEXT_IN_ENTRY", step_id: "charge_text", failed_steps: ["charge_text"], tokens: [], amounts: [...], next_action: {code: "EDIT_QUOTE" | "EDIT_SUMMARY", text, target}}`; `EDIT_QUOTE` when the quote states the amount (the quote picker), else `EDIT_SUMMARY`. Same shape as the D-051 code checks.
- **Edit.** `edits.excerpt` (the quote picker) with a quote that has no amount: if the summary still states one and the AI wrote that summary (she has not edited it), code removes the trailing clause(s) that state an amount under the D-054 suffix rule (only a run of clauses at the end, never the first clause, the kept prefix keeps at least 2 content words; otherwise nothing is trimmed) and the edit saves with the trimmed summary (`edited.summary`, the original is kept; the internal notes' EDITED ITEMS line shows both). The response `warnings[]` gains `{code: "CHARGE_CLAUSE_REMOVED", item_id, removed: [clause...], message}`. If code cannot trim, the edit is `422 invalid_edit` (`detail.reason "CHARGE_TEXT_IN_ENTRY"`); the paralegal edits the summary. A quote is never rewritten by code.
- **The held-out hint says the true cause (T-139 rounds 3 and 4).** The entry `why` (case view, `GET /items/{id}`), the 422 `message` of accept and of `edit`, and the internal notes' reason all follow one rule (`charge_text.bill_state` over the amount items on the entry's records, not rejected): a record with an accepted charge says "This record is a bill and its charges are already listed under Billed charges, so dismiss this entry unless it states treatment."; a record whose charge is not yet accepted says its charges go under Billed charges once she accepts them; a record whose charge she dismissed says "You dismissed this record's charge, so none of its figures is counted in Billed charges; ..."; **a record whose amounts were read but none is a charge (rates, unclear figures, estimates; 6 of the 11 held entries in the eval corpus) says "Its amounts were read but not totaled (the internal notes say why), so none of them is in Billed charges; dismiss this entry unless it states treatment."**; only a record with no amount at all says "No amount was read from this record, so its figures are not counted in the Billed charges section; the internal notes name them so you can request the bill." When the amount is only in a summary she edited and no amount row of the record carries it (a figure she typed), the message has no bill sentence at all. The static `why` for the code (appendix, trace `state_reasons`) makes no claim about where charges are.
- **Trace (T-139 r3).** Whenever code shortens a quote or strips a summary clause for an amount (narrowing, the trailing-clause trim, the quote-picker edit trim), the item trace carries a code step (`excerpt_narrowed`, `charge_clause_removed`) with the removed text verbatim, the reason, and the before and after quote and summary (see the entry steps in the trace section). The step is internal; the letter and the internal notes carry no trace text.
- **Export gate on the final text (T-139 round 4).** `export.build_export` builds the letter and then scans the FINAL letter text with the one detector: any money expression in the treatment part (everything before the `BILLED CHARGES` section; the section is found by structure, the last `BILLED CHARGES` line before the total line, never by the words in a quote) blocks the export. The accepted-charge lines and the total line are exempt. This catches what no item check saw, including a paralegal's own summary edit stored before a rule existed. An accepted entry whose summary or quote states money is therefore no longer dropped silently from the letter; it blocks. `GET /export` is `422 export_blocked` with `detail.blockers[]` holding one element per offending line: `{item_id (the entry, or null), kind: "entry" | "letter", reason_code: "MONEY_IN_LETTER", line (1-based line of letter_text), text (the line), expressions[] (the money as written), why: "Line N of the letter states an amount (\u2018billed at two thousand one hundred fifty\u2019): \u201c...\u201d. Amounts go only in the Billed charges section, never in a treatment entry.", next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}`; `message` is the first `why` plus "The export is blocked." **The trace gate lists it (T-139 r4, D-044/D-045):** `trace.export_blockers` runs `export.money_blockers_for_case` on the case's final letter text (both styles, merged), so the same `MONEY_IN_LETTER` elements appear in `GET /trace` `export_gate.blockers[]` (with `line`, `text`, `expressions`, `item_id` or null w
- **Billed charges section scanned too (T-139 round 5, the last fix; D-063).** `export.letter_money_blockers` also scans the `BILLED CHARGES` section, charge by charge (a header line ends `: $X.XX`; the lines after it, up to the next header, are that charge's quote). A charge line carries its own amount only: on the quote lines the one figure equal to X is allowed; any other money expression (a paid or adjusted figure, patient responsibility, wages, a second charge, number words) and any money in the header (provider, date) is a `MONEY_IN_LETTER` blocker with `kind: "amount"`, `item_id` the charge, `line`, `text`, `expressions`, `why` ("Line N of the letter is a Billed charges line for $X and also states ..."), `next_action` `{code: "DISMISS_OR_ENTER_BY_HAND", target: {item_id}, text}`. Before blocking, code trims: `_amount_quote` removes any other money expression (the one detector, not only `$` figures) from the shown quote by taking a clause of the sentence (between `;` or `,`, cut before a parenthesis, or the line up to the end of the charge's own figure, as in a ledger row `date  service  $150.00  $0.00  $730.00`), still word for word from the record; `Charge: $2,150 (ins paid $1,412.50).` shows `Charge: $2,150`. When no such clause is free of other money (`Insurer paid $1,412.50 of the $2,150 charge.`) the sentence stays and the export is blocked. The trace gate lists the same blockers (`gate.ready == GET /export allowed`), and `evals/letter_check.py` uses the same section rule. **Number words after a money label are money (round 5):** `copay of twenty`, `deductible o
- **Dismissed charge.** A provider with a dismissed `charge` amount is not listed under BILLS TO REQUEST. **T-139 round 2:** BILLS TO REQUEST lists treating providers and facilities only: a record whose source is a law firm, attorney, payer or EOB, or records custodian (`export._treating`: closed source-word list, or first-person firm wording such as "this firm represents" in the record) is never listed. No dismissed amount is quoted in the letter (the BILLED CHARGES section lists accepted charges only, and an entry quoting the figure is held out as above).
- **Eval.** `python -m evals.letter_check` (also a row and a blocker in `python -m evals.run`): the fixture-backend export of the sample, every golden case and every library packet has 0 currency strings outside BILLED CHARGES, 0 non-accepted amounts inside it, the exact total line, and (all charges dismissed) none anywhere. Round 4: it uses the same `money.py` detector as the hold and the gate, splits the letter by structure (`export.split_letter`), and counts a letter the gate blocks as a violation (`the export gate blocked this letter`).
- **Recommendation (not done, prompt owner):** `app/llm/prompts/extract_v1.md` line 12 should stop asking for the sentence that carries the "charge"; then the models stop quoting amounts and fewer entries are held out. Frontend: show the `charge_text` step reason in the Why text (`why` already carries the plain sentence) and offer the quote picker on a held-out entry.

## Prepared answers (T-177, D-065; amends D-029)
Provenance of every generator answer comes from the fixture's own `recorded_from`. A **curated** fixture (`recorded_from.backend == "curated"`, model `hand-checked (qa)`) is a *prepared answer*, never model output:
- **Item** (`entries[]`, `amounts[]`, `flags[]`, `GET /items/{id}`): `prepared: boolean`. `ladder.generator` carries `prepared` and, when true, `model: "hand-checked (qa)"` (not `claude-sonnet-5-5`). `ai_drafted` keeps its meaning (a person did not write the summary); the UI tag is "Prepared answer" when `prepared`, "AI draft" otherwise.
- **Audit** (`GET /audit` `calls[]`, also `/items/{id}` `calls[]`): each call has `prepared: boolean`; for a prepared call `model` is `hand-checked (qa)` (what is stored in `llm_calls.model`). Judge answers are real recordings (D-056): `prepared: false`, real model id.
- **Trace** (`GET /items/{id}/trace`): `evidence.model.prepared: boolean`, and `evidence.model.id` is `hand-checked (qa)` for a prepared generator step. That step (`extracted`, a flag's `proposed_by_ai`, a narrative sentence's `extracted`) has label "Prepared answer, standing in for the AI draft" and `why` "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft". Recorded and live steps keep "AI drafted a summary and picked a quote" / "The AI read this record and proposed a one-line summary and a quote." and the real model id.
- **Narrative** (`GET/POST /narrative`): `narrative.prepared` and `narrative.generator.prepared` (model `hand-checked (qa)` when true).
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:33:59.540Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json;d=json.load(open('evals/golden/sample.expected.json'));print(d.keys())\nfor k in d:\n  v=d[k]\n  if isinstance(v,list): print(k,len(v)); [print('  ',json.dumps(x)[:300]) for x in v[:12]]\n\"; ls evals/library | head -40",
 "description": "Inspect sample expected flags and library"
}
````

### User / tool · 2026-11-02T20:33:59.647Z

**tool result**
````
dict_keys(['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_excluded_records', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated', 'record_warnings', 'seeded_edits', 'must_not', 'notes'])
stress_types 10
   "sample_case"
   "near_miss_28_day_gap"
   "73_day_gap"
   "rate_not_charge"
   "accident_date_conflict"
   "treatment_plan_conflict"
   "pre_existing"
   "causation_language"
   "diagnosis_inference_trap"
   "header_date_vs_body_date"
records 9
   {"record_no": 1, "raw_date": "2026-01-09", "date": "2026-01-09", "kind": "encounter", "source": "Austin EMS run report"}
   {"record_no": 2, "raw_date": "2026-01-09", "date": "2026-01-09", "kind": "encounter", "source": "Central ER discharge summary"}
   {"record_no": 3, "raw_date": "2026-01-16", "date": "2026-01-16", "kind": "encounter", "source": "Dr. Alvarez, primary care"}
   {"record_no": 4, "raw_date": "2026-01-23", "date": "2026-01-23", "kind": "encounter", "source": "Capital PT, initial evaluation"}
   {"record_no": 5, "raw_date": "2026-02-20", "date": "2026-02-20", "kind": "encounter", "source": "Capital PT, visit 8"}
   {"record_no": 6, "raw_date": "2026-03-06", "date": "2026-03-06", "kind": "encounter", "source": "Capital PT, visit 9"}
   {"record_no": 7, "raw_date": "2026-05-18", "date": "2026-05-18", "kind": "encounter", "source": "Hill Country Pain Management, new patient"}
   {"record_no": 8, "raw_date": "2026-05-29", "date": "2026-05-29", "kind": "encounter", "source": "Austin Imaging, cervical MRI"}
   {"record_no": 9, "raw_date": "2026-06-12", "date": "2026-06-12", "kind": "encounter", "source": "Hill Country Pain Management, follow-up"}
entries 9
   {"id": "E1", "record_nos": [1], "date": "2026-01-09", "date_status": "parsed", "encounter": true, "provider": "Austin EMS run report", "must_contain_excerpt": "rear-ended at approx. 35 mph", "required_terms": ["rear-ended", ["approx", "about", "approximately"], ["C/O", "complain", "reports", "report
   {"id": "E2", "record_nos": [2], "date": "2026-01-09", "date_status": "parsed", "encounter": true, "provider": "Central ER discharge summary", "must_contain_excerpt": "Dx: cervical strain; concussion without loss of consciousness", "required_terms": ["cervical strain", "concussion", ["without loss of
   {"id": "E3", "record_nos": [3], "date": "2026-01-16", "date_status": "parsed", "encounter": true, "provider": "Dr. Alvarez, primary care", "must_contain_excerpt": "Persistent neck pain 6/10", "required_terms": ["neck pain", "physical therapy"]}
   {"id": "E4", "record_nos": [4], "date": "2026-01-23", "date_status": "parsed", "encounter": true, "provider": "Capital PT, initial evaluation", "must_contain_excerpt": "Plan of care: 12 visits", "required_terms": ["12 visits", ["approx", "about", "approximately"]]}
   {"id": "E5", "record_nos": [5], "date": "2026-02-20", "date_status": "parsed", "encounter": true, "provider": "Capital PT, visit 8", "must_contain_excerpt": "Pain 4/10, improving", "required_terms": ["4/10"]}
   {"id": "E6", "record_nos": [6], "date": "2026-03-06", "date_status": "parsed", "encounter": true, "provider": "Capital PT, visit 9", "must_contain_excerpt": "Discharged from PT after two missed appointments", "required_terms": ["discharged", "two missed appointments"]}
   {"id": "E7", "record_nos": [7], "date": "2026-05-18", "date_status": "parsed", "encounter": true, "provider": "Hill Country Pain Management, new patient", "must_contain_excerpt": "New onset pain radiating to right arm with numbness in fingers", "required_terms": ["new onset", "right arm", "numbness"
   {"id": "E8", "record_nos": [8], "date": "2026-05-29", "date_status": "parsed", "encounter": true, "provider": "Austin Imaging, cervical MRI", "must_contain_excerpt": ["C5-C6 disc protrusion with mild right foraminal narrowing", "Findings may represent degenerative change; correlate clinically"], "re
   {"id": "E9", "record_nos": [9], "date": "2026-06-12", "date_status": "parsed", "encounter": true, "provider": "Hill Country Pain Management, follow-up", "must_contain_excerpt": "Patient states symptoms began after the January collision", "required_terms": ["recommend", "epidural steroid injection", 
gap_excluded_records 0
gap_table 7
   {"from_date": "2026-01-09", "to_date": "2026-01-16", "from_records": [1, 2], "to_records": [3], "days": 7, "flag": false}
   {"from_date": "2026-01-16", "to_date": "2026-01-23", "from_records": [3], "to_records": [4], "days": 7, "flag": false}
   {"from_date": "2026-01-23", "to_date": "2026-02-20", "from_records": [4], "to_records": [5], "days": 28, "flag": false}
   {"from_date": "2026-02-20", "to_date": "2026-03-06", "from_records": [5], "to_records": [6], "days": 14, "flag": false}
   {"from_date": "2026-03-06", "to_date": "2026-05-18", "from_records": [6], "to_records": [7], "days": 73, "flag": true}
   {"from_date": "2026-05-18", "to_date": "2026-05-29", "from_records": [7], "to_records": [8], "days": 11, "flag": false}
   {"from_date": "2026-05-29", "to_date": "2026-06-12", "from_records": [8], "to_records": [9], "days": 14, "flag": false}
amounts 4
   {"id": "A1", "record_no": 2, "raw": "$6,240", "value": 6240, "class": "charge", "excerpt": "ER charges: $6,240", "in_total": true, "required": true, "needs_review": false}
   {"id": "A2", "record_no": 8, "raw": "$2,150", "value": 2150, "class": "charge", "excerpt": "Charge: $2,150", "in_total": true, "required": true, "needs_review": false}
   {"id": "A3", "record_no": 4, "raw": "$185", "value": 185, "class": "rate", "excerpt": "Charge per visit $185", "in_total": false, "required": true, "needs_review": true, "note": "Rate, not a charge: visits billed are never stated (12 planned; discharged at visit 9)."}
   {"id": "A4", "record_no": 5, "raw": "missing 3 days of work", "value": null, "class": "damages", "excerpt": "Patient reports missing 3 days of work", "in_total": false, "required": false, "needs_review": true, "note": "Damages mention, not a billed charge; no dollar amount. Optional to surface; neve
flags 10
   {"id": "G1", "type": "gap", "level": "must", "from_date": "2026-03-06", "to_date": "2026-05-18", "days": 73, "cite": {"all": [6, 7], "any": []}, "evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}, {"record_no": 7, "field": "excerpt", "exc
   {"id": "C1", "type": "conflict", "level": "must", "cite": {"all": [7], "any": [1, 2]}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-19"}, {"record_no": 1, "field": "date", "excerpt": "2026-01-09"}, {"record_no": 1, "field": "excerpt", "excer
   {"id": "C2", "type": "conflict", "level": "must", "cite": {"all": [4, 6], "any": []}, "evidence": [{"record_no": 4, "field": "excerpt", "excerpt": "Plan of care: 12 visits"}, {"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}], "summary": "Treatment-p
   {"id": "P1", "type": "pre_existing", "level": "must", "cite": {"all": [3], "any": []}, "evidence": [{"record_no": 3, "field": "excerpt", "excerpt": "Patient reports low back pain in 2023, resolved"}], "summary": "Prior low back pain (2023), reported resolved. Different body region from the cervical 
   {"id": "P2", "type": "pre_existing", "level": "must", "cite": {"all": [8], "any": []}, "evidence": [{"record_no": 8, "field": "excerpt", "excerpt": "Findings may represent degenerative change"}], "summary": "MRI wording (\"may represent degenerative change\") that an adjuster may argue shows a pre-e
   {"id": "K1", "type": "causation", "level": "must", "cite": {"all": [8], "any": []}, "evidence": [{"record_no": 8, "field": "excerpt", "excerpt": "may represent degenerative change; correlate clinically"}], "summary": "Hedged imaging language that an adjuster can use against causation.", "subtype": "
   {"id": "K2", "type": "causation", "level": "must", "cite": {"all": [6], "any": []}, "evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}], "summary": "Missed appointments / early discharge weaken the treatment-compliance narrative.", "subty
   {"id": "K3", "type": "causation", "level": "must", "cite": {"all": [9], "any": []}, "evidence": [{"record_no": 9, "field": "excerpt", "excerpt": "Patient states symptoms began after the January collision"}], "summary": "Causation rests on patient self-report, not a physician's causation opinion.", "
   {"id": "K4", "type": "causation", "level": "must", "cite": {"all": [7], "any": []}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "New onset pain"}], "summary": "'New onset' symptoms after a 73-day gap can be argued as a new cause. Must be a causation-type flag (see README: type match
   {"id": "K5", "type": "causation", "level": "must", "cite": {"all": [7], "any": []}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-19"}], "summary": "Wrong accident date on the intake form undermines reliability of the history. Must be a causa
must_not_flag 2
   {"id": "N1", "type": "gap", "from_date": "2026-01-23", "to_date": "2026-02-20", "days": 28, "statement": "28-day interval (records 4 to 5) is a near-miss and must NOT be flagged as a gap."}
   {"id": "N2", "type": "gap", "statement": "No gap flag for any other interval (7, 7, 14, 11, 14 days)."}
tolerated 0
record_warnings 0
seeded_edits 5
   {"id": "SE1", "entry_id": "E5", "record_no": 5, "kind": "number", "new_summary": "Visit 8: pain 4/10, improving; billed $9,000.", "introduced": ["9000"], "expected_state": "needs_review", "expected_reason": "number_not_in_excerpt", "accept_requires_keep_my_wording_confirm": true, "rule": "R-RV-3 / R
   {"id": "SE2", "entry_id": "E5", "record_no": 5, "kind": "number", "new_summary": "Visit 8: pain 5/10, improving.", "introduced": ["5"], "expected_state": "needs_review", "expected_reason": "number_not_in_excerpt", "accept_requires_keep_my_wording_confirm": true, "rule": "R-TL-10: excerpt says 4/10"}
   {"id": "SE3", "entry_id": "E8", "record_no": 8, "kind": "judge", "new_summary": "Cervical MRI: C5-C6 disc herniation with mild right foraminal narrowing.", "introduced": ["herniation"], "expected_state": "needs_review", "expected_reason": "judge_partially_or_unsupported", "accept_requires_keep_my_wo
   {"id": "SE5", "entry_id": "E5", "record_no": 5, "kind": "judge_masked", "new_summary": "Visit 8: pain 8/10, improving.", "introduced": ["8/10"], "expected_state": "needs_review", "expected_reason": "judge_partially_or_unsupported", "accept_requires_keep_my_wording_confirm": true, "rule": "R-RV-3: th
   {"id": "SE4", "entry_id": "E5", "record_no": 5, "kind": "control", "new_summary": "Visit 8: pain 4/10 and improving.", "introduced": [], "expected_state": "no_new_warning", "expected_reason": null, "accept_requires_keep_my_wording_confirm": false, "rule": "control: adds no number, date or $ outside 
must_not 17
   {"id": "M1", "statement": "States or implies a disc herniation (record says 'protrusion'); never says the collision caused one. 'Not herniation' wording is allowed.", "check": "regex", "bad_examples": ["C5-C6 disc herniation caused by the collision.", "MRI shows a herniated disc at C5-C6.", "Herniat
   {"id": "M2", "statement": "Asserts that the collision or trauma caused, aggravated or produced a condition (caused by / due to / from / resulted in / because of / injured in / aggravated by / X-related / traumatic) - in the tool's own voice OR put in the patient's mouth: the record says only that sy
   {"id": "M3", "statement": "Presents the MRI hedge as a finding: 'degenerative' / 'age-related' / 'wear and tear' / 'DDD' without a hedge (may/might/could/possible) in the same clause, or upgrades 'may' to 'likely/consistent with/confirmed'.", "check": "regex", "bad_examples": ["MRI confirmed degener
   {"id": "M4", "statement": "Computes a PT total or a grand total that includes PT (9x185=1,665; 12x185=2,220; 8x185=1,480; 8,390 plus those).", "check": "regex", "bad_examples": ["PT charges totaled $1,665 (9 visits at $185).", "Total billed: $10,055.", "12 visits at $185 = $2,220.", "Physical therap
   {"id": "M5", "statement": "Merges the two accident dates into one, or states a single accident date without the conflict.", "check": "judge", "bad_examples": ["Accident date: 2026-01-09, confirmed by the intake form.", "The collision occurred on January 9, 2026 (the intake form agrees).", "Date of a
   {"id": "M6", "statement": "Reverses or upgrades 'concussion without loss of consciousness' (lost consciousness, with/+ LOC, knocked out, TBI, mild/moderate/severe concussion, post-concussion syndrome, 'no concussion'). Negated wording (without / w/o / no / denies / without any) is faithful and allow
   {"id": "M7", "statement": "Treats '10 mg', '35 mph', visit counts, pain scores or '3 days' as a dollar amount.", "check": "amount_value", "bad_examples": [{"raw": "$10", "value": 10, "class": "charge"}, {"raw": "$35", "value": 35, "class": "charge"}, {"raw": "$7", "value": 7, "class": "charge"}], "g
   {"id": "M8", "statement": "Invents or substitutes a diagnosis not in the records (whiplash, radiculopathy/radicular, stenosis, sprain, disc bulge, nerve root/impingement, spondylosis, myelopathy, fracture).", "check": "regex", "bad_examples": ["Cervical radiculopathy.", "Radicular symptoms in right 
   {"id": "M9", "statement": "States the patient recovered / was symptom-free (pain was 3/10 at discharge). 'Not fully recovered' and the 2023 low back pain being resolved are allowed.", "check": "regex", "bad_examples": ["Patient made a full recovery.", "Patient completed all 12 planned PT visits with
   {"id": "M10", "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.", "check": "judge", "bad_examples": ["The treating physician concluded the symptoms were caused by the January collision.", "Dr. at Hill Country attributes the symptoms to t
   {"id": "M11", "statement": "Relates the 2023 low back pain to the cervical injury, or says it was ongoing.", "check": "judge", "bad_examples": ["Patient has ongoing low back pain from 2023.", "The 2023 low back pain contributes to the current cervical condition.", "Prior low back injury was aggravat
   {"id": "M12", "statement": "Counts 'missing 3 days of work' as a billed charge or adds it to any total.", "check": "judge", "bad_examples": ["Billed charges include 3 missed work days.", "Lost wages are added to the $8,390 total.", "Total damages: $8,390 plus 3 days of work.", "Lost wages: 3 days."]
notes 2
   "Records 1 and 2 share a date (2026-01-09) but are different providers: separate entries. Appendix C pairing '1->3: 7' means distinct-date gap 2026-01-09 to 2026-01-16."
   "sample.export.expected.txt is the byte-exact expected export (letter block + internal notes), copied from REQUIREMENTS section 6."
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:35:04.754Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/head && git archive HEAD | tar -x -C $S/head && ln -sf /Users/arsis/zlayt-pm-project/.venv $S/head/.venv && cd $S/head && (PORT=8766 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$S/t180.db nohup .venv/bin/python -m app.main > $S/server.log 2>&1 &) ; sleep 4; curl -s http://127.0.0.1:8766/api/health",
 "description": "Serve HEAD copy with fixture backend"
}
````

### User / tool · 2026-11-02T20:35:09.413Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:35:19.211Z

**tool call — Bash**
````
{
 "command": "cd /tmp && B=http://127.0.0.1:8766/api; T=$(curl -s -X POST $B/cases -H 'content-type: application/json' -d '{\"sample\":true}' | python3 -c \"import sys,json;print(json.load(sys.stdin)['token'])\"); echo $T; curl -s -X POST $B/cases/$T/run -H 'content-type: application/json' -d '{}' >/dev/null; for i in 1 2 3 4 5 6 7 8 9 10; do s=$(curl -s $B/cases/$T/status | python3 -c \"import sys,json;print(json.load(sys.stdin)['status'])\"); [ \"$s\" != running ] && break; sleep 1; done; echo $s; curl -s $B/cases/$T > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/sample_case.json; python3 - <<'EOF'\nimport json\nd=json.load(open('/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/sample_case.json'))\nprint(d['title'], d['status'], d['next_action'])\nprint('queue', d['review']['queue']); print(d['review']['counts'])\nfor e in d['entries']: print('E',e['id'],e['date'],e['state'],e['reasons'],e.get('prepared'),e['summary'][:90]); print('   why:',e['why'][:200])\nfor a in d['amounts']: print('A',a['id'],a['text'],a['kind'],a['state'],a['reasons'],a.get('not_counted_reason'),a.get('countable'),a.get('flag')); print('   why:',a['why'][:200])\nfor f in d['flags']: print('F',f['id'],f['type'],f['category'],f['state'],f['reasons'],'|',f['title'],'|',f['explanation'][:250]); print('   ev:',[x['excerpt'] for x in f['evidence']])\nprint('tray',[(t['id'],t['reasons']) for t in d['tray']]); print('filtered', d['tray_filtered']['count'])\nprint('totals', json.dumps(d['totals'])[:500])\nprint('uncovered', [(r['id'],[u['text'] for u in r['uncovered']]) for r in d['records']])\nEOF",
 "description": "Create sample case, run, dump queue"
}
````

### User / tool · 2026-11-02T20:35:20.669Z

**tool result**
````
1MFDLCqOioc5LIygQzGFyQ
ready
Sample case ready {'item_id': 'a2', 'kind': 'amount', 'reason': 'This figure is a rate, not a charge, so it is not added to the total.'}
queue ['a2', 'a3', 'f_r7_1', 'a1', 'a4', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_gap_r6_r7', 'f_r3_1', 'f_r6_1', 'f_r7_2', 'f_r8_1', 'f_r8_2', 'f_r9_1']
{'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0, 'edit_to_check': 0}
E e1 2026-01-09 verified [] True Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache;
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e2 2026-01-09 verified [] True Diagnosed with cervical strain and concussion without loss of consciousness; CT head negat
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e3 2026-01-16 verified [] True Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e4 2026-01-23 verified [] True Cervical range of motion reduced approx. 40%; plan of care 12 visits.
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e5 2026-02-20 verified [] True Pain 4/10, improving.
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e6 2026-03-06 verified [] True Discharged from physical therapy after two missed appointments; pain 3/10.
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e7 2026-05-18 verified [] True New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e8 2026-05-29 verified [] True C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may 
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
E e9 2026-06-12 verified [] True Cervical epidural steroid injection recommended; patient states symptoms began after the J
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
A a1 $6,240 charge verified [] None False None
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
A a2 $185 rate needs_review ['AMOUNT_RATE_NOT_TOTALED'] This figure is a rate, not a charge, so it is not added to the total. False None
   why: This figure is a rate, not a charge, so it is not added to the total.
A a4 $2,150 charge verified [] None False None
   why: Quote found word for word, every number in the summary is in the quote, and the second check agreed.
A a3 missing 3 days of work damages needs_review ['AMOUNT_DAMAGES'] This figure is not a bill (for example a damages or settlement figure), so it is not added to the total. False None
   why: This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.
F f_gap_r6_r7 gap gap_over_30 verified [] | Gap of 73 days | Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).
   ev: ['Date: 2026-03-06', 'Source: Capital PT, visit 9', 'Date: 2026-05-18', 'Source: Hill Country Pain Management, new patient']
F f_accident_date_after_treatment_1_2_7 conflict accident_date_after_treatment verified [] | Stated accident date is later than recorded treatment | Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose b
   ev: ['Date of accident per intake form: 2026-01-19', 'Date: 2026-01-09', 'Date: 2026-01-09']
F f_cx1 conflict treatment_plan_vs_actual verified [] | Treatment plan and what followed differ | Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.” Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.”
   ev: ['Plan of care: 12 visits.', 'Discharged from PT after two missed appointments.']
F f_r3_1 pre_existing pre_existing verified [] | Mention of a prior or pre-existing condition | Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.”
   ev: ['Patient reports low back pain in 2023, resolved.']
F f_r8_1 pre_existing degenerative_language verified [] | Degenerative wording | Austin Imaging, cervical MRI (May 29, 2026) uses degenerative wording: “Findings may represent degenerative change”.
   ev: ['Findings may represent degenerative change']
F f_r6_1 causation missed_care verified [] | Missed or ended care | Wording about missed appointments or ending care in Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.”
   ev: ['Discharged from PT after two missed appointments.']
F f_r7_1 causation accident_date_provenance needs_review ['LEXICON_ONLY'] | Accident date source | Accident date as stated in Hill Country Pain Management, new patient (May 18, 2026): “Date of accident per intake form: 2026-01-19.”
   ev: ['Date of accident per intake form: 2026-01-19.']
F f_r7_2 causation new_onset verified [] | New-onset wording | New-onset wording in Hill Country Pain Management, new patient (May 18, 2026): “New onset pain”.
   ev: ['New onset pain']
F f_r8_2 causation speculative_language verified [] | Hedged wording | Hedged wording in Austin Imaging, cervical MRI (May 29, 2026): “may represent degenerative change; correlate clinically”.
   ev: ['may represent degenerative change; correlate clinically']
F f_r9_1 causation patient_report verified [] | Reported onset | Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”
   ev: ['Patient states symptoms began after the January collision.']
tray []
filtered 0
totals {"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"}, "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"}, "flagged_charges": [], "not_totaled": [{"id": "a2", "kind": "rate", "text": "$185"}], "possible_overlaps": []}
uncovered [('r1', []), ('r2', []), ('r3', ['Patient reports low back pain in 2023, resolved.']), ('r4', []), ('r5', ['Patient reports missing 3 days of work.']), ('r6', []), ('r7', ['Date of accident per intake form: 2026-01-19.']), ('r8', []), ('r9', [])]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:35:37.005Z

**tool call — Bash**
````
{
 "command": "grep -n \"dismiss\" app/backend/export.py | head -30; grep -n \"accept_effect\" -r app/backend/*.py | head -5",
 "description": "Check how dismissed amounts appear in notes"
}
````

### User / tool · 2026-11-02T20:35:37.100Z

**tool result**
````
11:review_status in (accepted, edited) is "in"; dismissed/rejected is "out"; anything else is pending.
37:                   "dismiss the entry to remove it; hedge sentences cannot be removed)")
45:OUT = ("dismissed", "rejected")
431:    """R-EX-4(4): letter entries whose excerpt contains the evidence of a flag that is not dismissed (D-012)."""
529:            line += " Both figures are in the charges total, so this service may be counted twice. Check the records and dismiss one of the two."
569:    dismissed = {_provider(v.source(a["record_no"])) for a in v.amounts if a["cls"] == "charge" and _status(a) == "out"}    # T-139: a dismissed charge is never asked for
574:        if p and _treating(v, e["record_no"]) and p not in paid and p not in dismissed and p not in names:
583:    dismiss the entry (always clears the hold); a quote without the amount WITH a matching summary in the same edit (a quote-only change is refused when the summary
587:    rows = [{"kind": a["cls"], "review_status": a.get("review_status"), "state": "rejected" if (_status(a) == "out" and a.get("review_status") != "dismissed") else "",
590:    if state in ("listed", "pending", "dismissed", "not_totaled"):
594:        fix = "dismiss this entry, or pick a quote that does not state it and change the summary to match in the same edit"
596:        fix = "dismiss this entry, or edit the summary to remove it"
623:            why = "dismissed"
684:            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
715:    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
734:    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
740:        "FLAGS DISMISSED", *_flag_block(v, dismissed), "",
812:                "text": ("Edit the summary to remove the amount, or dismiss the entry." if in_summary else "Pick a quote that does not state the amount (and make the summary match), or dismiss the entry.")
814:               if owner else {"code": "EDIT_SUMMARY", "text": "Remove the amount from the line named above, or dismiss the item it comes from. The export stays blocked until it passes."})
app/backend/present.py:68:def accept_effect(row) -> str:
app/backend/present.py:146:            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate" and not counted,
app/backend/trace.py:928:    No second AI check is needed for that, so a missing one never blocks export. The one source for the amount view's `accept_effect` and the gate."""
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:35:39.030Z

**tool call — Bash**
````
{
 "command": "sed -n '60,80p' app/backend/present.py; grep -n \"AMOUNTS NOT TOTALED\\|DAMAGES MENTIONS\" app/backend/export.py | head; sed -n '610,640p' app/backend/export.py",
 "description": "Read accept_effect and not totaled notes logic"
}
````

### User / tool · 2026-11-02T20:35:39.124Z

**tool result**
````
def _translation(row):
    """D-042: set on an entry made from a Spanish record: its summary is an English translation, its quote the original Spanish."""
    t = (row.get("ladder") or {}).get("translation")
    return spanish.translation_info(t.get("source_language", "es"), "summary" in (row.get("edited") or {}) or bool(t.get("human_written"))) if t else None


def accept_effect(row) -> str:
    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
    never totaled, and no second AI check is needed), `internal_notes` (estimate, unclear: noted for the paralegal, never in the total)."""
    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")


def amount_flag(row):
    """D-059: the flag a charge carries (likely_duplicate | likely_total) and whether accepting it now needs the confirm step. (None, False) for any other amount."""
    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
    return (None, False) if not f else ({k: f.get(k) for k in ("flag", "name", "message", "confirm_with", "of", "confirmed_at")}, row["review_status"] == "pending")


def not_counted_info(row, records):
742:        "AMOUNTS NOT TOTALED", *_amounts_not_totaled(v), "",
744:        "DAMAGES MENTIONS (not charges)", *_damages(v), "",
        elif any(_status(e) == "in" and not v.verbatim(e) for e in ents):
            why = "excerpt not found in record, not exported"
        elif any(_status(e) == "in" and not v.date_of(e) for e in ents):
            why = "date not confirmed, not exported"
        elif any(_status(e) != "out" and v.states_amount(e) for e in ents):
            why = _held_amount_note(v, n, ents)      # T-139
        elif any(e.get("edit_unconfirmed") for e in ents):
            why = "edited, not yet confirmed against the quote"      # T-134
        elif any(_status(e) == "pending" for e in ents):
            why = "not reviewed"
        elif any(e.get("review_status") == "rejected" for e in ents):
            why = "rejected"
        elif ents:
            why = "dismissed"
        else:
            why = r.get("reason") or "no entry"
        lines.append(f"- {_cap(v.cite(n))} — {why}")
    return lines or [f"- none ({len(v.records)} of {len(v.records)} records included)"]


def _was_edited(e):
    """T-069: an entry stays an edited item after the paralegal accepts it (accept keeps the edit payload and only flips the status),
    so edited-ness is the status OR a stored original that differs from the exported text. Out-of-letter entries are not listed."""
    if e.get("review_status") == "edited" or e.get("edit_unconfirmed"):
        return True
    if _status(e) != "in":
        return False
    return ((e.get("original_summary") is not None and e["original_summary"] != e["summary"])
            or (e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]))
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:35:51.410Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _amounts_not_totaled\\|def _damages\" -A 14 app/backend/export.py | head -45",
 "description": "Read amounts not totaled notes builder"
}
````

### User / tool · 2026-11-02T20:35:51.492Z

**tool result**
````
494:def _amounts_not_totaled(v):
495-    out = [f'- {_cap(v.cite(a["record_no"]))}: charge {_money(a["cents"])} not exported and not totaled: excerpt not found in record.'
496-           for a in v.amounts if a["cls"] == "charge" and a.get("cents") is not None and _status(a) == "in" and not v.verbatim(a)]
497-    for a in v.amounts:
498-        if a["cls"] in ("charge", "damages") or _status(a) != "in":
499-            continue
500-        n, cls = a["record_no"], a["cls"]
501-        q = f'"{_amount_quote(v, a)}"'
502-        m = _money_short(a.get("cents"), a.get("raw", ""))
503-        if cls == "rate":
504-            per = "/visit" if re.search(r"per visit", a["excerpt"], re.I) else ""
505-            body = f"Rate {m}{per}; visit count not stated{_plan_note(v, n)}. Request itemized {_ledger_label(v, n)}."
506-        elif cls == "estimate":
507-            body = f"Estimate {m}; not a billed charge. Request clean copy of bill."
508-        elif cls == "unclear" and language.translated_record(v.records.get(n)):
--
538:def _damages(v):
539-    out = [f'- {_cap(v.cite(a["record_no"]))}: "{_amount_quote(v, a)}"'
540-           for a in v.amounts if a["cls"] == "damages" and _status(a) == "in"]
541-    return out or ["- none"]
542-
543-
544-def _future(v):
545-    out = []
546-    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
547-        for s in _sentences(r.get("excerpt", "")):
548-            if _FUTURE_RE.match(s) and "$" not in s:
549-                out.append(f'- {_cap(v.cite(r["n"]))}: "{s.strip()}" Request cost estimate.')
550-    return out or ["- none"]
551-
552-
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:36:58.916Z

**tool call — Bash**
````
{
 "command": "cd /tmp && B=http://127.0.0.1:8766/api; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for L in case_lib11_priors_and_ledger case_01_date_formats; do T=$(curl -s -X POST $B/cases -H 'content-type: application/json' -d \"{\\\"library\\\":\\\"$L\\\"}\" | python3 -c \"import sys,json;d=json.load(sys.stdin);print(d.get('token') or d)\"); echo $L $T; curl -s -X POST $B/cases/$T/run -H 'content-type: application/json' -d '{}' | head -c 200; echo; sleep 6; curl -s $B/cases/$T > $S/$L.json; done; python3 - <<EOF\nimport json\nfor L in ['case_lib11_priors_and_ledger','case_01_date_formats']:\n  d=json.load(open('$S/'+L+'.json'))\n  print('==',L,d.get('title'),d.get('status'),d.get('error'))\n  for a in d.get('amounts',[]): print('A',a['id'],a['text'],a['kind'],a['review_status'],a.get('countable'),'|',a.get('not_counted_reason'),'|',a.get('count_confirm'),'|',a['excerpt'][:100])\n  print('dates',json.dumps(d.get('dates_to_confirm'))[:800])\n  for e in d.get('undated_entries',[]): print('U',e['id'],e['summary'][:100],e['excerpt'][:100])\n  print('tray',[(t['id'],t['reasons'],t['why'][:100]) for t in d.get('tray',[])])\nEOF",
 "description": "Load two library cases for realistic states"
}
````

### User / tool · 2026-11-02T20:37:11.189Z

**tool result (error)**
````
Exit code 1
case_lib11_priors_and_ledger NVyyeaE-VdpLKKvEndUTkw
{"token":"NVyyeaE-VdpLKKvEndUTkw","status":"running","stage":"extract","started_at":"2026-11-02T20:36:59Z"}
case_01_date_formats {'error': {'code': 'not_found', 'message': 'No such library case.', 'detail': {}}}

== case_lib11_priors_and_ledger Priors and ledger ready None
A a1 $3,260 charge pending False | None | None | Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge
A a2 $250.00 unclear pending True | The line states no date of service, so it is not an itemized service line and is not totaled. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
A a3 $180.00 unclear pending True | The line states no date of service, so it is not an itemized service line and is not totaled. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
A a4 $2,310.00 unclear pending True | The line states no date of service, so it is not an itemized service line and is not totaled. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
A a5 $2,740.00 unclear pending False | Total or subtotal line: it repeats the charges listed with it, so it is not totaled. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
A a6 $300.00 unclear pending False | Payment: money received, not a charge. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
A a7 $274.00 unclear pending False | Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
A a8 $2,166.00 unclear pending False | Balance or amount due: worked out from charges, payments and adjustments, not a charge. | None | Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; t
dates []
tray [('f_r4_2', ['JUDGE_DISAGREES', 'LLM_ONLY'], 'A second AI check disagreed with the first result for this item. The AI found this flag but the phra'), ('f_r6_3', ['JUDGE_DISAGREES', 'LLM_ONLY'], 'A second AI check disagreed with the first result for this item. The AI found this flag but the phra')]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 293, in load
    return loads(fp.read(),
           ^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:37:20.666Z

**tool call — Bash**
````
{
 "command": "cd /tmp && B=http://127.0.0.1:8766/api; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 -c \"import json;print(json.dumps({'text':open('/Users/arsis/zlayt-pm-project/evals/golden/case_01_date_formats.txt').read(),'title':'Date formats'}))\" > $S/c1.json; T=$(curl -s -X POST $B/cases -H 'content-type: application/json' -d @$S/c1.json | python3 -c \"import sys,json;d=json.load(sys.stdin);print(d.get('token') or d)\"); echo $T; curl -s -X POST $B/cases/$T/run -H 'content-type: application/json' -d '{}' >/dev/null; sleep 6; curl -s $B/cases/$T > $S/c01.json; python3 - <<EOF\nimport json\nd=json.load(open('$S/c01.json'))\nprint(d['title'],d['status'],len(d['entries']),len(d['flags']),len(d['amounts']))\nprint('dates',json.dumps(d.get('dates_to_confirm'))[:1200])\nfor e in d.get('undated_entries',[]): print('U',e['id'],e['record_ids'],e['summary'][:140],'|',e['excerpt'][:140], e['reasons'])\nfor r in d['records']:\n  if r['date_status']!='parsed': print(r['id'], r['date_raw'], r['source_label'], r['text'][:300])\nd=json.load(open('$S/case_lib11_priors_and_ledger.json'))\nfor t in d['tray']: print(json.dumps(t)[:700])\nfor r in d['records']: print(r['id'],r['date_iso'],r['source_label'])\nprint([r['text'] for r in d['records'] if 'ledger' in r['text'].lower()][0][:900])\nprint(len(d['entries']),len(d['flags']))\nEOF\ncurl -s $B/cases | python3 -c \"import sys,json;d=json.load(sys.stdin);[print(json.dumps(c)[:900]) for c in d['cases'][:1]]\"",
 "description": "Load case_01 and inspect dates, lib11 tray and ledger"
}
````

### User / tool · 2026-11-02T20:37:26.920Z

**tool result**
````
eRcaFR_oo7OU_kyICD59Fw
Date formats ready 7 1 1
dates [{"record_id": "r8", "raw": "04/05/2026", "candidates": ["2026-04-05", "2026-05-04"], "status": "ambiguous", "suggestion": {"convention": "MDY", "label": "MM/DD", "iso": "2026-04-05", "reason": "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)", "evidence": [{"record_id": "r2", "raw": "02/17/2026"}, {"record_id": "r6", "raw": "03-17-26"}], "evidence_count": 4, "auto_applied": false}}]
U e8 ['r8'] Patient reports no new symptoms. | Patient reports no new symptoms. ['DATE_AMBIGUOUS']
r8 04/05/2026 Dr. Orla Pennywhistle, phone note === Record 8 ===
Date: 04/05/2026
Source: Dr. Orla Pennywhistle, phone note
Excerpt: "Patient reports no new symptoms."
{"id": "f_r4_2", "kind": "flag", "record_ids": ["r4"], "state": "rejected", "reasons": ["JUDGE_DISAGREES", "LLM_ONLY"], "why": "A second AI check disagreed with the first result for this item. The AI found this flag but the phrase list did not; check that it applies. The second check does not find this flag supported by the quote.", "flag": {"type": "causation", "category": "litigation_referral"}, "attempt": {"summary": "Attorney referral", "excerpt": "This firm represents the client for injuries from a collision on 2026-03-18."}, "ladder": {"item_id": "f_r4_2", "state": "rejected"}}
{"id": "f_r6_3", "kind": "flag", "record_ids": ["r6"], "state": "rejected", "reasons": ["JUDGE_DISAGREES", "LLM_ONLY"], "why": "A second AI check disagreed with the first result for this item. The AI found this flag but the phrase list did not; check that it applies. The second check does not find this flag supported by the quote.", "flag": {"type": "causation", "category": "accident_date_provenance"}, "attempt": {"summary": "Accident date source", "excerpt": "Date of injury: 3/l8/26."}, "ladder": {"item_id": "f_r6_3", "state": "rejected"}}
r1 2026-03-04 Dr. Hesper Alderton, primary care
r2 2026-03-18 Ashgrove Fire-Rescue run report
r3 2026-03-18 Wexcombe Memorial ED
r4 2026-03-26 Pellingham and Rook PLLC, correspondence (letter of protection)
r5 2026-03-27 Fennimoor Spine Clinic, new patient
r6 2026-03-27 Fennimoor Spine Clinic, new patient intake form (OCR text)
r7 2026-04-24 Fennimoor Spine Clinic, visit 8
r8 2026-05-29 Fennimoor Spine Clinic, visit 14
r9 2026-06-15 Fennimoor Spine Clinic, itemized ledger
=== Record 9 ===
Date: 2026-06-15
Source: Fennimoor Spine Clinic, itemized ledger
Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
9 12
{"token": "eRcaFR_oo7OU_kyICD59Fw", "title": "Date formats", "name": "Date formats", "source": "paste", "status": "ready", "record_count": 8, "created_at": "2026-11-02T20:37:20Z", "updated_at": "2026-11-02T20:37:20Z", "last_activity_at": "2026-11-02T20:37:20Z", "run": {"stage": "finalize", "steps_done": 7, "steps_total": 8, "running": false, "error": false}, "progress": {"entries": {"decided": 0, "total": 8}, "flags": {"decided": 0, "total": 1}, "amounts": {"decided": 0, "total": 1}}, "counts": {"pending": 10, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 2}, "hitl": {"pending": 10, "needs_review": 2, "needs_review_open": 2, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:37:42.135Z

**tool call — Bash**
````
{
 "command": "cd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 - <<EOF\nimport json\nfor f in ['case_lib11_priors_and_ledger','c01','sample_case']:\n  d=json.load(open('$S/'+f+'.json'))\n  print(f,[ (e['id'],e.get('prepared')) for e in d['entries']][:4], [(x['id'],x.get('prepared')) for x in d['flags']][:3])\nd=json.load(open('$S/sample_case.json'))\nr=[r for r in d['records'] if r['id']=='r3'][0]; print(r['text'], r['sentences'])\nEOF\ngrep -n \"label\\|stage\" /Users/arsis/zlayt-pm-project/app/backend/*.py | grep -i \"progress.*label\\|\\\"label\\\": f\\\"\" | head",
 "description": "Check provenance flags and record sentences"
}
````

### User / tool · 2026-11-02T20:37:42.249Z

**tool result**
````
case_lib11_priors_and_ledger [('e1', False), ('e2', False), ('e3', False), ('e4', False)] [('f_gap_r7_r8', False), ('f_cx1', False), ('f_cx2', False)]
c01 [('e1', False), ('e2', False), ('e3', False), ('e4', False)] [('f_date_r8', False)]
sample_case [('e1', True), ('e2', True), ('e3', True), ('e4', True)] [('f_gap_r6_r7', False), ('f_accident_date_after_treatment_1_2_7', False), ('f_cx1', False)]
=== Record 3 ===
Date: 2026-01-16
Source: Dr. Alvarez, primary care
Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved." [{'text': 'Persistent neck pain 6/10, daily headaches.', 'start': 633, 'end': 676}, {'text': 'Refer to physical therapy 2x/week for 6 weeks.', 'start': 677, 'end': 723}, {'text': 'Patient reports low back pain in 2023, resolved.', 'start': 724, 'end': 772}]
/Users/arsis/zlayt-pm-project/app/backend/api.py:479:                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
/Users/arsis/zlayt-pm-project/app/backend/trace.py:124:    return {"done": done, "total": len(steps), "label": f"{done} of {len(steps)} steps settled"}
/Users/arsis/zlayt-pm-project/app/backend/trace.py:1179:    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
/Users/arsis/zlayt-pm-project/app/backend/trace.py:1181:               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:40:04.931Z

Now I have the full picture (contract, decisions, real sample/lib11/case_01 payloads from a fixture server). Writing the spec.

### Assistant · claude-opus-5-5 · 2026-11-02T20:40:07.854Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-180 --agent frontend --text \"Read D-059..D-068, api.md, T-179 backend D-066 (review.py compare_error: body compared:true, 422 COMPARE_REQUIRED; not yet in api.md). Pulled real payloads from a HEAD fixture server (sample, lib11, case_01) for mockup content. Plan: docs/GUIDED_UI_SPEC.md + generated static mockup in artifacts/mockups/guided/ (paths assigned by orchestrator in the T-180 brief, outside app/frontend).\" >/dev/null; grep -n \"judge_dispute\\|compared\" app/backend/case_extras.py | head -5; sed -n '40,52p' app/backend/case_extras.py",
 "description": "Note progress and check batch D-066 handling"
}
````

### User / tool · 2026-11-02T20:40:08.024Z

**tool result**
````
46:        elif action == "accept" and review.judge_dispute(row):      # D-066: a disputed summary is accepted alone, with her explicit compare
47:            bad.append({"id": i, "reason": "judge_disputed"})
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind == "amount" and row["kind"] == "charge":      # D-059: a charge is accepted one at a time, never in a batch
            bad.append({"id": i, "reason": "charge_in_batch"})
        elif kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.judge_dispute(row):      # D-066: a disputed summary is accepted alone, with her explicit compare
            bad.append({"id": i, "reason": "judge_disputed"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and (err := _code_check_refusal(conn, case_id, i, row, cache)):     # D-051: same check as a single accept
            bad.append(err)
        elif action == "accept" and row["state"] != "verified":
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:42:52.355Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/docs/GUIDED_UI_SPEC.md",
 "content": "# Guided UI spec (T-180, D-068)\n\nStatus: design spec for the guided four-step UI. Owner: frontend. Clickable mockup: `artifacts/mockups/guided/index.html`\n(all screens: `artifacts/mockups/guided/screens.html`); screenshots `artifacts/screenshots/guided-mockup-*.png` at 1440x900 and 390x844.\nBuilds only on `memory/contracts/api.md` as of 2026-11-02 plus the D-066 `compared` field already in `app/backend/review.py` (T-179).\nNo new backend feature is assumed; where the API lacks something, this spec says what the screen does without it.\n\nChris's brief: \"<Chris's message omitted> someone's <Chris's message omitted>. <Chris's message omitted>.\"\n\n---\n\n## 0. Rules every screen keeps\n\n| Rule | How |\n|---|---|\n| Nothing moves when you click | The page is a fixed frame: banner, header, step bar, title row and action bar have fixed heights; only the panes inside scroll. An answer swaps text inside boxes that keep their size. No banner, toast or error is ever inserted above content after load: each has a reserved slot. `scrollbar-gutter: stable`. System fonts only (no font swap). Buttons have fixed widths, so a label change never resizes them. |\n| No collapsing, no hidden menus | No `<details>`, accordions, dropdown menus, kebab menus or hover-only content. Every action is a visible button with words on it. |\n| No shortcuts required | Everything works with a mouse, a finger, or Tab + Enter. Keyboard shortcuts are not offered in the guided UI. |\n| Every screen answers three questions | **Where am I** (step bar + title row), **what do I do now** (one question or one instruction next to the buttons), **how do I know I'm done** (the \"N left\" count, then a done screen with a big check). |\n| One thing at a time | Review pages show one item. The next item appears in the same boxes. |\n| Plain words | No \"judge\", \"LLM\", \"tray\", \"verified\", \"flag\", \"excerpt\", \"pending\". The table in section 10 maps every internal word to the word on screen. Server sentences (`why`, `explanation`, `message`, `not_counted_reason`) are shown as given; the UI never rewrites a fact. |\n| Honest | Every answer is saved by the server before the screen says it is saved. Provenance labels follow D-065. |\n| Untrusted text | Record text, quotes, summaries and titles are inserted with `textContent` only. |\n\nThe old screen moves to `/classic` (D-068) unchanged; its e2e suite keeps guarding behaviour. The guided UI gets its own suite.\n\n## 1. Map of screens and routes\n\n| Route | Screen | Mockup page |\n|---|---|---|\n| `/` | Your cases | `index.html`, `home-empty.html`, `home-loading.html`, `home-error.html` |\n| `/new` | Step 1, before the case exists | `step1-add.html` |\n| `/case/<token>/records` | Step 1: records found / drafting / done / stopped | `step1-found.html`, `step1-drafting.html`, `step1-drafting-lib01.html`, `step1-failed.html` |\n| `/case/<token>/timeline[?item=<id>]` | Step 2, one item at a time; done screen | `step2-entry.html`, `step2-fix.html`, `step2-flag.html`, `step2-gap.html`, `step2-disputed.html`, `step2-cannot-check.html`, `step2-write.html`, `step2-date.html`, `step2-done.html` |\n| `/case/<token>/bills[?item=<id>]` | Step 3, one amount at a time; done screen | `step3-charge.html`, `step3-count.html`, `step3-never.html`, `step3-done.html` |\n| `/case/<token>/letter` | Step 4 | `step4-letter.html`, `step4-pending.html`, `step4-blocked.html` |\n| `/classic` | the old review screen | (unchanged) |\n\nRouting is `history.pushState` with real URLs, so Back in the browser and a reload both land on the same screen. A reload of\n`/case/<token>/timeline?item=e3` reopens that item.\n\n## 2. Global frame\n\n### 2.1 Synthetic banner (every page, fixed, 32 px; 40 px on phones)\nText: `health.banner` (\"Synthetic data only — never paste real records\"). Warm yellow background, dark text, centred.\nOn phones the banner also carries the demo label (2.3), so provenance is never off-screen.\n\n### 2.2 Header (every page, fixed, 64 px; 52 px on phones)\n- Left: product mark + \"Treatment Timeline\" (home), or \"‹ Your cases\" button + case title (inside a case). The title is the API `title`,\n  one line, ellipsis. On phones: \"‹ Cases\" + title.\n- Right: the demo label (2.3) on desktop, then a \"Dark mode\" / \"Light mode\" text button (theme; default follows the OS; remembered in\n  `localStorage` inside try/catch).\n\n### 2.3 Demo provenance (D-065)\n`GET /api/health` `answers`:\n\n| `answers` | Label (pill, always visible) | Footer sentence (visible, not a tooltip) | Item tag |\n|---|---|---|---|\n| `prepared` | Demo: sample answers prepared by our team | The AI's own answers on these cases are in the evaluation report. | \"Prepared answer\" when `item.prepared`, else \"AI draft\" |\n| `recorded` | Demo: recorded AI answers | These are real AI answers recorded earlier; nothing new is sent to an AI. | \"AI draft\" |\n| `live` | (no pill) | Summaries and warnings are drafted by AI and checked by code; you decide every item. | \"AI draft\" |\n\nA manual entry (`entered_by_reviewer`) or a summary she wrote is tagged \"Written by you\". `ai_banner` is shown under the step title on\nSteps 2 and 3 (desktop) and on each step's done screen (all widths). Removing jargon never removes provenance.\n\n### 2.4 Step bar (inside a case; fixed, 76 px; 60 px on phones; never moves, never changes height)\nFour equal segments joined by a line: **1 Add records · 2 Check the timeline · 3 Check the bills · 4 Get your letter**\n(phones: Records · Timeline · Bills · Letter). Each segment: a 32 px circle, the label, one status line.\n\n| State | Circle | Status line | Click |\n|---|---|---|---|\n| done | green circle with a check | \"Done\" | opens the step (to look or change answers) |\n| current | filled accent circle with the number, accent bar under the segment, bold label, `aria-current=\"step\"` | e.g. \"16 of 19 left\" | opens the step |\n| remaining | grey outline circle with the number | e.g. \"4 amounts\" / \"Not started\" | opens the step |\n| locked | grey outline, label at 60% | \"After step 1\" | not clickable (`aria-disabled`) |\n| needs attention | amber circle with \"!\" | e.g. \"Run again\" / \"1 problem\" | opens the step |\n\nSteps 2–4 are locked until the case has items (`status` is `ready`, or `failed` with items; see 4.5). The step bar is a\n`<nav aria-label=\"Steps\">` of links. Status lines are computed from GET case (section 9.2), text only, fixed width.\n\n### 2.5 Title row (review pages; fixed, 72 px; 52 px on phones)\nLeft: eyebrow \"Step 2 of 4\" and h1 \"Check the timeline\". Right: \"Item 4 of 19\" and a progress bar (fixed 240 px; full width on\nphones) with \"3 answered · 16 to go\". Step 3 adds a fixed-width \"Bill total so far: $6,240.00\" chip (`totals.accepted.cents`).\n\n### 2.6 Action bar (review pages; fixed to the bottom; fixed height)\nThree rows, always present, never re-laid out:\n1. **The question** (20 px, semibold), max two lines (reserved).\n2. **Two big answers**, equal size (56 px tall, 260 px wide on desktop; half width each on phones). The first is filled accent,\n   the second outlined. Equal size on purpose: neither is a reflex click.\n3. **Small buttons**: \"‹ Back\", the item's third action (\"Fix the wording\" / \"Add a note\" / none), \"Decide later\", and the\n   **status slot** (`aria-live=\"polite\"`, one line, reserved): \"Saved: item 3 kept in the letter. Undo\".\n\nWhen an answer is not allowed yet (a confirm box is not ticked, a code check fails), the button stays where it is, disabled, and the\nreason is in the item card's footer slot (2.7). Errors from the server go in the same footer slot, never in a new banner.\n\n### 2.7 Item cards (review pages)\nDesktop: two columns of equal width inside the work area. **Left: \"From the record\"** (the source). **Right: the line to check.**\nPhones: the source on top (flexible height, scrolls), the line card below it (fixed 180 px, scrolls inside).\n\n- **Source card.** Header: \"Record 3 · Dr. Alvarez, primary care · January 16, 2026\" (record `seq`, `source_label`, long date).\n  Body: the record text at 18 px/1.6 with the quote in a yellow `<mark>` (offsets `excerpt_start/end` into the case text, minus\n  `char_start`). On open the card scrolls **inside itself** so the mark is in view; the page never scrolls. Several records (a flag with\n  evidence in two records) are stacked in the same card, each with its header. Footer (when `records[].uncovered` is not empty):\n  \"Also in this record, not in any line:\" + each sentence in quotes (read only).\n- **Line card.** Header: tag (2.3) and the date + provider. Body: the summary at 22 px. **Footer slot** (fixed min-height 112 px):\n  the plain check sentence (`why`), or a confirm checkbox, or a refusal message, or \"Your answer: ...\" when she comes Back.\n\n### 2.8 Footer (every page)\nOne line: the provenance sentence (2.3) and, in live mode, \"Pasted text is deleted after `retention_hours` hours.\"\n\n## 3. Your cases (home, `/`)\n\n**Where am I:** h1 \"Your cases\". **What do I do now:** each card's \"Next:\" line and its one Continue button. **Done:** a case moves to\n\"Finished\" with a green \"Letter ready\".\n\nLayout: title row with h1, one sentence (\"Each case goes through 4 steps. Pick up where you left off.\"), and the primary\n\"Start a new case\" button (top right; full width on phones). A \"Find a case\" search box shows when there are more than 6 cases\n(filters by title as she types; the only thing on the page that changes the list, and only on typing). Two sections, always open:\n**In progress (N)** and **Finished (N)**. Cards in a grid: 2 columns at ≥ 1100 px, 1 column below. Sorted by `last_activity_at`,\nnewest first.\n\n### 3.1 Case card (fixed height 236 px desktop; content clamps)\n```\nJordan Rivera (sample)                               [Rename]\nStarted Nov 2 · 9 records\n(1)✓ Add records — (2) Check the timeline — (3) Check the bills — (4) Get your letter\nNext: Check the timeline. 16 of 19 items left.\n[        Continue        ]                          [Delete]\n```\n- Title: `title` (text only). \"Rename\" turns the title into an input in the same box with \"Save\" / \"Cancel\" (PATCH `{title}`;\n  `422 invalid_title` message shown under the input in a reserved line).\n- Mini step track: the four steps with the same states as the step bar (2.4), small.\n- **Next line** (one rule, section 9.3) and the **Continue** button (one per card, full card width minus Delete).\n- \"Delete\": the card's bottom row turns into \"Delete this case and all its answers? [Yes, delete] [Keep it]\" in the same row\n  (DELETE `/api/cases/{token}`; the card is then removed, which is the one allowed layout change, caused by her own confirm).\n- A card whose summary failed (`status_error: true`): body shows `status_error_message` (\"We couldn't load this case's status\")\n  instead of the track and the Next line; button \"Open case\".\n\n### 3.2 Next line + Continue target (per case)\n| Case state | Next line | Continue goes to |\n|---|---|---|\n| `ingested` (records read, not drafted) | Next: Draft the timeline. | Step 1 (records found) |\n| `running` | Next: Wait while the timeline is drafted (stage N of 8). | Step 1 (drafting) |\n| `failed` | Next: Drafting stopped. Run it again. | Step 1 (stopped) |\n| Step 2 has undecided items | Next: Check the timeline. N of M items left. | first undecided Step 2 item |\n| Step 3 has undecided items | Next: Check the bills. N of M amounts left. | first undecided Step 3 item |\n| gate blocker on a decided item (`next_action.kind` is entry/flag/amount and that item is decided) | Next: Fix 1 problem before the letter. + `next_action.reason` | that item |\n| everything decided, gate ready | Finished. Your letter is ready. (green) | Step 4; button reads \"Open letter\" |\n\n### 3.3 Multi-case in local and public mode\n- Local mode (`ZLAYT_MODE=local`): the list is `GET /api/cases` (every case on this computer).\n- Public / demo mode: `GET /api/cases` is `404` by design (no case list; the token is the only credential). The home then lists the\n  cases **this browser started**: their tokens are kept in `localStorage` (`zl.guided.cases`, try/catch) when POST `/api/cases`\n  answers, and each card is filled from `GET /api/cases/{token}`. A `404` card reads \"This case is no longer here. Cases are kept for\n  `retention_hours` hours.\" with \"Remove from this list\". A line under the h1 says \"These are the cases started in this browser.\n  Keep the case link to open it elsewhere.\" No server feature is added.\n\n### 3.4 Home states\n| State | Screen |\n|---|---|\n| Loading | The title row, then 3 grey skeleton cards of the final card size (no jump when they fill). |\n| Empty | Large icon, \"You don't have any cases yet.\", \"A case is one client's medical records. We'll guide you through 4 steps.\", buttons \"Start a new case\" and \"Try the sample case\" (POST `{sample: true}`, then Step 1). |\n| Error | \"We couldn't load your cases.\" + the server `message` when there is one + \"Try again\" (refetch; focus returns to the h1). |\n\n## 4. Step 1 — Add records (`/new`, then `/case/<token>/records`)\n\n**Instruction:** \"Add the medical records for this case. We'll read them and draft a timeline for you to check.\"\n\n### 4.1 Before the case exists (`/new`)\n- \"Name this case (optional)\" text input (sent as `title`; 120 characters max, no `<` `>`; the 422 message shows under it).\n- Three big choice tiles, side by side (stacked on phones), each a radio with a picture-free heading and one line:\n  **Paste text** (\"Copy the records and paste them here\") · **Upload a file** (\".txt or .pdf, up to 5 MB\") ·\n  **Use the sample case** (\"A short synthetic case to try it out\").\n- Below the tiles, one fixed-height box (280 px) that shows the chosen input: a textarea, a file drop area with \"Choose a file\", or\n  \"The sample has 9 short records from a fictional car-accident case.\" The box does not change size between choices.\n- Primary button: **Read the records** (disabled until there is text, a file, or the sample is chosen).\n- Demo mode line (when `health.demo_mode`): \"This demo can only read the sample and our test cases.\"\n\n| Control | API |\n|---|---|\n| Read the records (paste) | `POST /api/cases {text, title}` |\n| Read the records (.txt) | read in the browser, then the same POST |\n| Read the records (.pdf) | `POST /api/cases/pdf?title=` raw bytes, `Content-Type: application/pdf` |\n| Read the records (sample) | `POST /api/cases {sample: true, title}` |\n\nErrors (shown in a reserved line under the box, plain words, with the action):\n\n| Code | Message on screen | Action |\n|---|---|---|\n| `400 bad_request` empty | There's nothing to read yet. Paste the records or choose a file. | — |\n| `413 input_too_large` | That's more than we can read at once (60,000 characters or 40 records). Split it into two cases. | — |\n| `409 demo_mode_unsupported_input` | This demo can only read the sample and our test cases. | \"Use the sample case\" |\n| `400 pdf_no_text_layer` | This PDF looks scanned, so it has no text we can read. | \"Read the scanned pages\" (re-post with `ocr=true`) when `detail.ocr.status.available` |\n| `400 pdf_encrypted` / `pdf_unreadable` / `pdf_timeout` | the server `message` | \"Choose another file\" |\n| `400 pdf_only_hidden_text` | Everything on these pages is hidden text, so we kept it out. | \"Use these pages anyway\" (re-post `include_hidden=all`, after a confirm checkbox \"I looked at these pages myself\") |\n| `429 busy` | We're reading other files right now. Try again in a moment. | \"Try again\" |\n| network / 5xx | We couldn't reach the server. Your text is still here. | \"Try again\" |\n\n### 4.2 Records found (`status: ingested`)\nHeading \"We found 9 records\". A fixed list (scrolls inside its box) of rows: \"1 · January 9, 2026 · Austin EMS run report\".\nPlain notes above the list in a reserved slot, from the POST/GET response:\n- `dates_to_confirm` not empty: \"1 record has a date we need you to check. You'll do that in step 2.\"\n- warning `PHI_PATTERN`: \"Some text looks like real personal details (a phone, SSN or record number). Only use synthetic records.\"\n- warning `SPLIT_AMBIGUOUS` / `UNSPLIT_TEXT`: \"Some text didn't look like a record. We kept it as its own record so nothing is lost.\"\n- `injection.banner`: shown as given.\nPrimary: **Draft the timeline** → `POST /api/cases/{token}/run {confirm_rerun: false}`. Secondary: \"Start over with other records\" (`/new`).\n\n### 4.3 Drafting (`status: running`)\nPoll `GET /api/cases/{token}/status` every second. A fixed checklist of the 8 stages (never the raw stage id or `progress.label`,\nwhich contains ids). Done stages get a green check, the current one a spinner and \"(4 of 9)\" from `progress.done/total` when the stage\ncounts items, the rest are grey. A progress bar above shows stages done / 8. Copy:\n\n| `stage` | Live / recorded | Prepared (`answers: prepared`) |\n|---|---|---|\n| `ingest` | Reading the records | Reading the records |\n| `extract` | Writing one line for each record | Loading the prepared line for each record |\n| `verify` | Checking every quote word for word | Checking every quote word for word |\n| `judge_entries` | Double-checking each line a second way | Double-checking each line a second way |\n| `amounts` | Finding the bill amounts | Finding the bill amounts |\n| `conflicts` | Comparing the records with each other | Comparing the records with each other |\n| `flags` | Looking for things the attorney should know | Looking for things the attorney should know |\n| `finalize` | Putting it all together | Putting it all together |\n\nUnder the list: \"This usually takes under a minute. You can leave this page; we'll keep going.\" (Home shows the same progress.)\n\n### 4.4 Done (`status: ready`)\nThe same box shows a big green check: \"All set. 19 timeline items and 4 bill amounts are ready for you to check.\" (counts from\n`status.counts`, entries + flags, amounts) + the `ai_banner` sentence + primary **Go to step 2: Check the timeline**. Step 1 turns done.\n\n### 4.5 Stopped (`status: failed`)\nAmber box: \"Drafting stopped before it finished.\" + `error.message` as given (it already says decisions were kept) + **Run it again**\n→ `POST .../run {confirm_rerun: false}`; on `409 needs_confirm` the same box shows \"Run it again? Your answers so far are kept.\" with\n**Yes, run it again** (`confirm_rerun: true`) / **Cancel**. Items the run did finish can be checked meanwhile: steps 2–3 open.\n`error.records` (extract failures) are named: \"No line was written for records 2 and 7. You can write them yourself in step 2.\"\n\nAfter a case is drafted, Step 1 shows the records list read-only with \"To add more records, start a new case.\" (There is no API to add\nrecords to a case.)\n\n## 5. Step 2 — Check the timeline (`/case/<token>/timeline`)\n\n### 5.1 The queue\nBuilt in the browser from one `GET /api/cases/{token}`, once, when the step opens; it never re-sorts while she works.\nContents: every entry in `entries` and `undated_entries`, every flag in `flags`, every `tray` item (could not check). Not included:\n`tray_filtered` (listed read-only on the done screen), amounts (Step 3). Order: the `next_action` timeline rule (api.md, T-157 step 3):\nby the date of the record the item cites (earliest when several; undated last), then that record's position, then entry before flag,\nthen id. So a flag sits right after the line it is about. Sample case: 9 lines + 10 warnings = 19 items.\n\nOpening the step lands on the first undecided item (or `?item=`). After an answer the next undecided item opens in the same boxes.\n\"‹ Back\" opens the previous item (decided or not). \"Decide later\" moves on without saving. When no undecided item is left, the done\nscreen (5.8) opens.\n\nEvery write sends `version` and `expected_status` from the item on screen (T-178). On `409 stale_item`: footer slot shows \"This item\nchanged in another tab. We've loaded the latest.\" and the item is re-read (`GET .../items/{id}` or the case).\n\n### 5.2 A timeline line (entry) — `step2-entry.html`\n- Line card: tag, \"January 16, 2026 · Dr. Alvarez, primary care\", the summary. Footer: `why` (\"Quote found word for word, every number\n  in the summary is in the quote, and the second check agreed.\").\n- **Question:** \"Does this line say the same thing as the highlighted words?\"\n- **Yes, this matches** → `POST .../items/{id}/review {action: \"accept\", version, expected_status}`. Saved text: \"Kept in the letter.\"\n- **No, leave it out** → `{action: \"dismiss\"}`. Saved text: \"Left out of the letter.\"\n- **Fix the wording** → 5.3.\n- Status slot after an answer: \"Saved: item 4 kept in the letter. Undo\" (Undo = `{action: \"reset\"}` on that item, then reopen it).\n\nRefusals, shown in the footer slot with the button disabled and the way out made the primary small action:\n\n| Server says | Footer slot | Way out |\n|---|---|---|\n| item `reasons` include a code-check reason (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_NUMBER_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CHARGE_TEXT_IN_ENTRY`, `EXCERPT_*`, `GROUNDING_EXCERPT_NOT_VERBATIM`), or `422 CODE_CHECK_FAILED` | the `why` / `message` as given | \"Fix the wording\" (or \"Change the highlighted words\" for `EDIT_QUOTE`) |\n| `422 DATE_UNCONFIRMED` | \"Pick the right date first.\" | the date question (5.6) |\n| `422 COMPARE_REQUIRED` | 5.4 | tick the box |\n| `409 item_rejected` | the item is shown as could-not-check (5.5) | — |\n\n### 5.3 Fix the wording — `step2-fix.html`\nThe line card body becomes a textarea with the current summary, same box. Above it: \"Change the line so it says only what the\nhighlighted words say. Numbers, left/right and words like 'no' or 'possible' must match.\" The question row reads \"Change the line,\nthen save it.\" The two big buttons become **Save my wording** / **Cancel** (same places). The source card adds one line at the top:\n\"To change which words are highlighted, tap whole sentences below.\" Sentences (`records[].sentences`) become tappable (outlined); the\nchosen run is the new quote (contiguous whole sentences only; a gap in the run is refused in the browser with \"Pick sentences that\nfollow each other.\").\n\n| Control | API |\n|---|---|\n| Save my wording (summary changed) | `{action: \"edit\", edits: {summary}}` |\n| Save my wording (quote changed) | `{action: \"edit\", edits: {excerpt}}`; both changed: two calls, quote first |\n| Cancel | nothing sent |\n\n`422 invalid_edit` → the server `message` in the footer slot (\"The summary says “left”, which the quote does not say. Remove it or\nchange the quote.\"); the text stays in the box. On save, the response item is shown: when `edit_to_check` is true the card goes to\n5.4 with \"You changed the wording. Read it against the highlighted words once more.\"; `warnings[]` messages (for example\n`CHARGE_CLAUSE_REMOVED`) are shown in the footer slot.\n\n### 5.4 Compare confirm (D-066, and an edit still to check) — `step2-disputed.html`\nWhen the item is disputed (its ladder verdict or reasons say `partially` / `unsupported` / `disagrees`, the same rule as\n`review.judge_dispute`) **or** `edit_to_check` is true:\n- Footer slot (amber): the dispute sentence (the item `why`, e.g. \"The second check found this only partly supported by the\n  quote.\") and a 28 px checkbox: **\"I read this line against the highlighted words myself.\"**\n- \"Yes, this matches\" is disabled until the box is ticked; then it sends `{action: \"accept\", compared: true, version,\n  expected_status}`. \"No, leave it out\" and \"Fix the wording\" are always enabled.\n- The box is never pre-ticked and is cleared when the item changes.\n\n### 5.5 Could not check — `step2-cannot-check.html`, `step2-write.html`\nA `tray` item. Line card header: \"We couldn't check this one\" (amber), body: the `why` as given, then \"What was suggested (not\nused): “Visit 8: pain 4/10, improving.”\" (`attempt.summary`, quoted, muted). The source card shows the whole record without a\nhighlight (`attempt.excerpt` is not in the record, so nothing is marked).\n- Tray **entry**: **Question:** \"Read the record. Do you want to write this line yourself?\" **Write it myself** → the write screen;\n  **Skip it** → `{action: \"dismiss\"}` on the tray item (\"Skipped. It stays out of the letter.\").\n- Write screen: the record's `sentences` are tappable (pick whole sentences that follow each other; the picked ones turn yellow); the\n  line card is a textarea \"Your line for the timeline\". Buttons **Save my line** / **Cancel**. Save → `POST /api/cases/{token}/records/\n  {rid}/entry {summary, excerpt}`. `422 invalid_edit` → message in the footer slot. `201` → the new item (`e<n>_m`, tag \"Written by\n  you\") opens in the normal line question (5.2) at the same queue position.\n- Tray **flag** (the second check disagreed with a suggested warning): header \"We couldn't confirm this warning\", body `why`, the\n  suggested warning `attempt.summary` and its quote. **Question:** \"This warning can't go in the notes. Read it; if it matters, tell the\n  attorney yourself.\" **OK, leave it out** → `{action: \"dismiss\"}`; **Decide later** in the second slot.\n- Tray items are optional: they never count in \"N left\" (the server leaves them out of `review.counts.pending`), and the item counter\n  says \"Optional\".\n\n### 5.6 A date to pick — `step2-date.html`\nAn entry in `undated_entries` whose record is in `dates_to_confirm` with `candidates`.\n- Source card: the record with its `Date:` line marked.\n- Line card header \"Which date is right?\", body: \"The record says 04/05/2026. That could be two different dates.\" The two answers\n  are the two candidates as long dates (\"April 5, 2026\" / \"May 4, 2026\"), each with its reading in small text (\"month first\" / \"day\n  first\"). When `suggestion.iso` is set, that button carries a \"Suggested\" chip and the footer shows `suggestion.reason`\n  (\"4 other dates in this packet use month first...\"). Nothing is chosen on load.\n- **Question:** \"Which date is right for this record?\" → `POST /api/cases/{token}/records/{rid}/confirm_date {date}`.\n  Response `gap_changes[].sentence` goes in the status slot (\"Gap recalculated after you confirmed record 4: now 40 days (was 42).\").\n  The same item then shows the normal line question (5.2), \"part 2 of 2\" beside the counter.\n- `missing` date (no candidates): \"We couldn't find a date in this record, so it can't go on the timeline.\" One answer\n  **OK, leave it out** (`dismiss`); the second slot is \"Decide later\".\n\n### 5.7 A warning for the attorney (flag) — `step2-flag.html`, `step2-gap.html`\nWarnings never go in the letter; accepted ones go in the internal notes (D-001). The line card becomes a warning card:\n- Header: a fixed plain heading by type (below) + \"Warning for the attorney\".\n- Body: `title` (bold) and `explanation` as given; for a gap with `computed.endpoint_warnings`, each `warning` and `alternative`\n  sentence as given; `gap_change.sentence` when set.\n- Source card: every `evidence[]` excerpt marked in its record (several records stacked).\n- Footer: \"Warnings only go in the notes for the attorney, never in the letter.\"\n- **Question:** \"Should the attorney be told about this?\" **Yes, tell the attorney** → `{action: \"accept\"}`;\n  **No, not needed** → `{action: \"dismiss\"}` (it is then listed under \"Flags dismissed\" in the notes, so the attorney can see what was\n  ruled out). Third action **Add a note** → a textarea in the card, **Save note** / **Cancel** → `{action: \"edit\", edits: {note}}`.\n\n| `type` / `category` | Plain heading |\n|---|---|\n| `gap` | A break in treatment (`computed.conditional`: A possible break in treatment) |\n| `conflict` / `accident_date_*` | The records disagree about the accident date |\n| `conflict` / `treatment_plan_vs_actual` | The plan and what happened differ |\n| `conflict` / `provider_name_variant` | The provider's name is written differently |\n| `conflict` / other | The records disagree |\n| `pre_existing` / `pre_existing`, `prior_surgery` | An earlier health problem is mentioned |\n| `pre_existing` / `degenerative_language` | Wording about wear and tear |\n| `causation` / `patient_report` | The patient, not a doctor, says what caused it |\n| `causation` / `speculative_language` | Hedged wording (\"may\", \"possible\") |\n| `causation` / `missed_care` | Missed or ended treatment |\n| `causation` / `new_onset` | Wording about a new problem |\n| `causation` / `accident_date_provenance` | Where the accident date comes from |\n| `causation` / `credibility_language` | Wording about the patient's effort or credibility |\n| `causation` / other | Wording the other side could use |\n| `record_warning` / `injection_suspected` | This record contains text that looks like instructions to a computer |\n| `record_warning` / `date_ambiguous` | This record's date is unclear |\n| `record_warning` / `analysis_incomplete` | We couldn't finish comparing these records |\n| `record_warning` / other | Something to check in this record |\n\n### 5.8 Step 2 done — `step2-done.html`\nShown when no undecided item is left (or from the step bar when the step is done).\n- Big green check + \"You checked every item on the timeline.\" + counts in one line: \"8 kept in the letter · 1 left out ·\n  7 warnings for the attorney · 3 not needed\".\n- If some are undecided instead: amber \"2 items still need a decision.\" + **Go to the first one**.\n- \"Your answers\": a plain list of all items in queue order, one row each: date, short label (entry: provider; warning: plain\n  heading), the answer chip (\"Kept\", \"Left out\", \"Tell the attorney\", \"Not needed\", \"Skipped\", \"Not decided\") and a **Change** button\n  (opens that item). Read-only \"Suggestions a rule ruled out (nothing to do)\": `tray_filtered.rules[]` label + `explanation` +\n  each item's quote, when `count` > 0. `checks` (T-151): \"We checked for: <labels of conflict_types>. Not checked: <not_checked labels>.\"\n- Primary: **Go to step 3: Check the bills** (or step 4 when the case has no amounts).\n\n## 6. Step 3 — Check the bills (`/case/<token>/bills`)\n\nQueue: every item in `amounts[]` in this order: charges and countable amounts first (record order, then position), then the\nnever-counted ones. One at a time, same frame as Step 2. Charges are never batched (D-059); there is no \"count all\".\n\n### 6.1 A charge — `step3-charge.html` (`kind: \"charge\"`)\n- Line card (\"Bill amount\"): the figure as money in 40 px (\"$6,240.00\" from `value_cents`), \"Central ER discharge summary ·\n  January 9, 2026\", footer \"If you count it, it's added to the bill total in the letter.\"\n- **Question:** \"Should this charge count toward the bill total?\"\n- **Yes, count it** → `{action: \"accept\"}`; **No, don't count it** → `{action: \"dismiss\"}`.\n- The title-row chip updates from the response `totals.accepted` (\"Bill total so far: $6,240.00\").\n- **D-059 flagged charge** (`flag` set, `confirm_required: true`): footer shows `flag.message` as given and a checkbox named by the flag:\n  `likely_duplicate` \"I checked: this is a separate charge, not the same one counted twice.\"; `likely_total` \"I checked: this is a\n  charge of its own, not a total of the others.\" \"Yes, count it\" is disabled until ticked, then sends `{action: \"accept\", confirm:\n  flag.confirm_with}`. On `422 CONFIRM_REQUIRED` the footer shows `detail.message`.\n\n### 6.2 An amount that can be counted with a check (D-064 b) — `step3-count.html`\n`countable: true`. Line card: the figure, \"Not counted yet\" chip, `not_counted_reason` as given (\"The line states no date of service,\nso it is not an itemized service line and is not totaled.\"). Footer: checkbox **\"I checked this is a separate charge for a service.\"**\nand, when `count_confirm` is set, `count_confirm.message` + a second checkbox named as in 6.1.\n- **Yes, count it** (enabled when the box or boxes are ticked) → `{action: \"count\", confirm: \"separate_charge\"}` plus\n  `confirm_flag: count_confirm.confirm_with` when set.\n- **No, don't count it** → `{action: \"accept\"}` (it is noted for the attorney under \"Amounts not totaled\", never in the total).\n\n### 6.3 An amount that is never counted (D-064 a) — `step3-never.html`\n`countable: false` and not a charge (rate, total, balance, payment, adjustment, damages, estimate...). Line card: the figure as\nwritten (`text`), \"Never counted\" chip, `not_counted_reason` as given. Footer: \"Either way, it is never added to the bill total.\"\n- **Question:** \"This amount is never added to the total. List it in the notes for the attorney?\"\n- **Yes, list it** → `{action: \"accept\"}` (rates: `accept_effect: acknowledge`); **No, leave it out** → `{action: \"dismiss\"}`.\n\n### 6.4 Step 3 done — `step3-done.html`\nBig check + \"You checked every bill amount.\" + the letter's total line exactly as the export writes it, large:\n\"Billed charges accepted from these records: $8,390.00\" (`totals.letter_line` when present, else built from\n`totals.accepted.cents`). Three plain lists, always open: **Counted** (figure, provider, date), **Not counted by you**, **Never\ncounted** (figure, where, `not_counted_reason`). `totals.possible_overlaps[]`: each `message` as given in an amber box above the\nlists, with \"Change\" buttons on both figures. Primary: **Go to step 4: Get your letter**.\nA case with no amounts: \"We didn't find any bill amounts in these records.\" + **Go to step 4**.\n\n## 7. Step 4 — Get your letter (`/case/<token>/letter`)\n\nData: `GET /api/cases/{token}/export` (and GET case for the counts). Layout: the letter on the left (wide, white \"paper\" box, 17 px,\n`white-space: pre-wrap`, scrolls inside), the notes for the attorney on the right (narrower, tinted box headed \"Notes for the attorney\n— do not send\"). Phones: letter first, then notes; each box fixed height with its own scroll.\n\n### 7.1 Ready — `step4-letter.html`\nGreen status row: \"Your letter is ready. Every item has an answer.\" Buttons under the letter: **Copy letter** (primary),\n**Download letter (.txt)**. Under the notes: **Copy notes**, **Download notes (.txt)**. Copy → `navigator.clipboard.writeText\n(letter_text)`; the button reads \"Copied\" for 2 s at the same width. Download → a Blob named `<title>-letter.txt` /\n`<title>-notes.txt` (code, client side). A plain box \"Exhibit and page numbers (optional)\": three inputs Exhibit, Bates prefix,\nFirst number + **Save** → `PUT /api/cases/{token}/export_config` then re-GET export (`422 invalid_edit` message under the inputs).\nNo drafted treatment paragraph anywhere (D-067).\n\n### 7.2 Undecided items — `step4-pending.html`\n`review.counts.pending + review.counts.edit_to_check` > 0 (the export is still allowed, D-045a):\namber row \"3 items still need a decision. If you don't decide them, they stay out of the letter.\" + **Go to the first one** (the\nfirst undecided item in step order: Step 2 queue, then Step 3). The letter preview shows what would be sent now. Copy and Download are\ndisabled until the checkbox \"Copy it anyway, without those 3 items\" is ticked (the one confirmation before copying the contract asks\nfor). The checkbox sits in a reserved row; it is not shown once the count is 0.\n\n### 7.3 Blocked — `step4-blocked.html`\n`422 export_blocked` / `judge_not_run`: red row \"The letter can't be made yet.\" and one row per `detail.blockers[]`: its `why` as\ngiven + a button by `next_action.code`:\n\n| `next_action.code` | Button |\n|---|---|\n| `DECIDE` (`NOTHING_ACCEPTED`) | Go to step 2 |\n| `EDIT_SUMMARY` / `EDIT_QUOTE` | Fix it (opens the item in Fix the wording) |\n| `DISMISS_OR_ENTER_BY_HAND` | Go to it |\n| `RERUN_JUDGE` | Run the second check again (`POST .../rejudge`, only when the item's `rerun_available`; else the text \"The second check can't run here. Fix the wording in your own words, or leave the item out.\") |\n| `CONFIRM_RERUN` (`RUN_FAILED`) | Go to step 1 |\n| `RUN_IN_PROGRESS` | (text) Wait for drafting to finish |\n\nThe letter box keeps its size and shows \"Your letter will appear here once the problem above is fixed.\"\n\n### 7.4 Done\nStep 4 is done (green in the step bar, \"Finished\" on home) when steps 2 and 3 have nothing undecided and the export answers 200.\n\n## 8. Visual system\n\n- **Type:** system stack (`\"Segoe UI\", system-ui, -apple-system, \"Helvetica Neue\", Arial`), `rem` on a 16 px root. Body 18/28,\n  record text 18/29, the line to check 22/32, question 20/28, h1 32/40 (26/32 phones), small 15/22 (never below 14).\n  Money and counts `tabular-nums`.\n- **Spacing:** 8 px grid; page gutter 32 px desktop, 16 px phones; cards 24 px padding (16 phones); 16 px between cards.\n- **Shape:** cards radius 14 px, buttons 12 px, chips 999 px; borders 1 px; one soft shadow on the action bar and cards.\n- **Colour:** one accent (blue `#0B57D0`, dark `#8AB4FF`) for the current step, primary buttons, focus ring and links. Status colours\n  only for meaning: green done/kept, amber needs a decision, red blocked; yellow `<mark>` for the quote. Light and dark sets on\n  `:root` (`prefers-color-scheme`, overridden by `data-theme`); every text pair ≥ 4.5:1, control edges ≥ 3:1 (values: mockup\n  `guided.css`, reusing `docs/UI_DESIGN_BRIEF.md` §4 where they overlap).\n- **Targets:** big answers 56 px tall; every other control ≥ 48 px; checkboxes 28 px with the whole label clickable.\n- **Focus:** 3 px accent ring, offset 2 px, on every control. After an answer focus moves to the first answer button of the next item.\n- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons\n  in one row below); the source card takes the remaining height; no horizontal scroll anywhere.\n\n## 9. Data rules (code in the browser; deterministic)\n\n### 9.1 What counts as undecided\nAn item is undecided when it is live (not `rejected`) and `review_status` is `pending`, or `edit_to_check` is true. Step 2 =\nentries, undated entries and flags; Step 3 = amounts. \"N items still need a decision\" = `review.counts.pending +\nreview.counts.edit_to_check` (the same number as home's `hitl.pending + hitl.edits_to_check`).\n\n### 9.2 Step states\n| Step | done when | status line |\n|---|---|---|\n| 1 | `status` is `ready` | \"Done\" / \"Drafting 4 of 8\" / \"Run again\" / \"Not started\" |\n| 2 | no undecided Step 2 item | \"Done\" / \"16 of 19 left\" |\n| 3 | no undecided amount | \"Done\" / \"4 amounts\" / \"3 of 4 left\" / \"None found\" (then done) |\n| 4 | steps 2 and 3 done and the export gate is ready (`GET /trace` `export_gate.ready`, or home's `export_ready`) | \"Ready\" / \"1 problem\" / \"Not yet\" |\n\nCurrent step = the first step not done. Home uses `GET /api/cases` `progress.entries + progress.flags` (Step 2) and\n`progress.amounts` (Step 3); inside a case the same counts come from GET case.\n\n### 9.3 Next line\nSection 3.2, in that order. The only server sentence used is `next_action.reason` for a gate problem.\n\n## 10. Words on screen\n\n| Internal | On screen |\n|---|---|\n| entry | line (on the timeline) |\n| excerpt / quote | the highlighted words |\n| accept / dismiss (entry) | Yes, this matches / No, leave it out |\n| flag | warning for the attorney |\n| accept / dismiss (flag) | Yes, tell the attorney / No, not needed |\n| charge accepted / dismissed | counted / not counted |\n| tray, rejected, could-not-verify | We couldn't check this one |\n| judge, second check, J1–J4 | the second check |\n| verified / needs_review | (not shown; the question and the footer sentence carry it) |\n| pending | not decided |\n| internal notes | notes for the attorney |\n| export | your letter |\n| run / LLM run | drafting the timeline |\n| token | case link |\n\n## 11. API mapping (every control)\n\n| Screen | Control | Call | Fields read |\n|---|---|---|---|\n| all | banner, demo label, footer | `GET /api/health` | `banner`, `answers`, `ai_banner`, `demo_mode`, `retention_hours`, `sample_available` |\n| home | list | `GET /api/cases` (local) or `GET /api/cases/{token}` per stored token (public) | `title`, `created_at`, `last_activity_at`, `record_count`, `status`, `run`, `progress`, `hitl`, `export_ready`, `next_action`, `status_error*` |\n| home | Rename / Save | `PATCH /api/cases/{token} {title}` | `title` |\n| home | Delete / Yes, delete | `DELETE /api/cases/{token}` | — |\n| home | Start a new case | route `/new` | — |\n| home (empty) | Try the sample case | `POST /api/cases {sample: true}` | `token` |\n| 1 | Read the records | `POST /api/cases` or `POST /api/cases/pdf` | `token`, `records[]`, `dates_to_confirm`, `warnings[]`, `injection` |\n| 1 | Draft the timeline | `POST /api/cases/{token}/run {confirm_rerun:false}` | `status` |\n| 1 | progress | `GET /api/cases/{token}/status` (1 s) | `status`, `stage`, `progress.done/total`, `counts`, `error` |\n| 1 | Run it again / Yes, run it again | `POST .../run` (`confirm_rerun: true` after `409 needs_confirm`) | — |\n| 1 | Read the scanned pages / Use these pages anyway | `POST /api/cases/pdf?ocr=true` / `?include_hidden=all` | — |\n| 2, 3 | load | `GET /api/cases/{token}` | `entries`, `undated_entries`, `flags`, `amounts`, `tray`, `tray_filtered`, `records[].text/sentences/uncovered/char_start`, `dates_to_confirm`, `review`, `totals`, `checks`, `next_action` |\n| 2 | Yes, this matches | `POST .../items/{id}/review {action:\"accept\", version, expected_status}` (+ `compared: true` after the 5.4 box) | `item`, `review`, `totals`, `warnings` |\n| 2 | No, leave it out / Skip it / OK, leave it out | `{action:\"dismiss\"}` | same |\n| 2, 3 | Undo / Change (back to undecided) | `{action:\"reset\"}` | same |\n| 2 | Save my wording | `{action:\"edit\", edits:{summary}}` / `{edits:{excerpt}}` | `item.edit_to_check`, `warnings` |\n| 2 | Save my line | `POST .../records/{rid}/entry {summary, excerpt}` | `item`, `review`, `warnings` |\n| 2 | date answers | `POST .../records/{rid}/confirm_date {date}` | `entry`, `gap_changes[].sentence`, `dates_to_confirm` |\n| 2 | Yes, tell the attorney / No, not needed | `{action:\"accept\"}` / `{action:\"dismiss\"}` on the flag | — |\n| 2 | Save note | `{action:\"edit\", edits:{note}}` | — |\n| 3 | Yes, count it (charge) | `{action:\"accept\"}` (+ `confirm: flag.confirm_with` when `confirm_required`) | `totals.accepted`, `totals.letter_line` |\n| 3 | Yes, count it (countable) | `{action:\"count\", confirm:\"separate_charge\"}` (+ `confirm_flag`) | `amount`, `totals` |\n| 3 | No, don't count it | charge: `{action:\"dismiss\"}`; countable: `{action:\"accept\"}` | `totals` |\n| 3 | Yes, list it / No, leave it out (never counted) | `{action:\"accept\"}` / `{action:\"dismiss\"}` | — |\n| 4 | preview, Copy, Download | `GET /api/cases/{token}/export` | `letter_text`, `internal_notes_text`, `excluded.pending` |\n| 4 | blocked rows | `GET .../export` 422 `detail.blockers[]` (same as `GET .../trace` `export_gate.blockers`) | `why`, `next_action`, `item_id` |\n| 4 | Run the second check again | `POST /api/cases/{token}/rejudge` | `export_gate` |\n| 4 | Exhibit and page numbers Save | `PUT /api/cases/{token}/export_config` | — |\n\nNot used by the guided UI (still in `/classic`): batch review, reclassify, dismissal suggestions, narrative (D-067), audit, judges,\nbilling listing, case trace panels, calibration.\n\n## 12. States checklist (every screen)\n\n| Screen | Loading | Empty | Error | Done |\n|---|---|---|---|---|\n| Your cases | 3 skeleton cards | 3.4 Empty | 3.4 Error + Try again | Finished section, green \"Letter ready\" |\n| Step 1 | button shows \"Reading...\" in place, disabled | 4.1 | 4.1 table, 4.5 | 4.4 big check |\n| Step 2 | skeleton text in both cards, same size; buttons disabled | \"There are no timeline lines in this case.\" + Go to step 3 | load error in the work area: \"We couldn't load this case.\" + Try again; write errors in the footer slot | 5.8 |\n| Step 3 | as Step 2 | 6.4 no amounts | as Step 2 | 6.4 |\n| Step 4 | \"Making your letter...\" in the letter box | `NOTHING_ACCEPTED` (7.3) | 7.3, network: \"We couldn't make the letter. Try again\" | 7.1 green row |\n\n## 13. Test plan for the build card\n- Layout stability: for each review page, record the bounding boxes of the step bar, both answer buttons and the small buttons; click\n  every answer, Fix the wording, Cancel, Back, tick and untick each box; assert no box moved (0 px) at 1440x900 and 390x844.\n- No `<details>`, no `[role=menu]`, no element with `:hover`-only visibility; no horizontal scroll at 390 and 320.\n- Flow: sample case from `/new` to a copied letter with only clicks; the letter equals `evals/golden/sample.export.expected.txt`.\n- D-066: a disputed item cannot be accepted without the box (button disabled; a forced POST is 422 `COMPARE_REQUIRED`).\n- D-059/D-064: count buttons stay disabled until the named box is ticked; bodies carry the named confirm.\n- Provenance: with `answers: prepared` every sample item is tagged \"Prepared answer\"; the label and footer sentence are on every page.\n- Multi-case: three cases at different steps show the right Next line and Continue target (local mode list and public mode stored tokens).\n- axe: 0 serious/critical at both widths in light and dark.\n"
}
````

### User / tool · 2026-11-02T20:42:52.409Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/docs/GUIDED_UI_SPEC.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:42:54.020Z

Now the mockup: shared CSS, a tiny JS, and a generator script that writes every page.

### Assistant · claude-opus-5-5 · 2026-11-02T20:44:41.370Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/mockups/guided/guided.css",
 "content": "/* Guided UI mockup (T-180, D-068). Static; no backend. Spec: docs/GUIDED_UI_SPEC.md */\n:root {\n  color-scheme: light;\n  --page: #F4F6F9; --panel: #FFFFFF; --sunken: #EEF1F5; --paper: #FFFFFF;\n  --border: #DCE1E8; --border-strong: #6F7B8B;\n  --text: #14181F; --muted: #4A5565; --subtle: #5B6676;\n  --accent: #0B57D0; --accent-hover: #0948A8; --on-accent: #FFFFFF; --accent-soft: #E8F0FE;\n  --ok: #13613A; --ok-bg: #E3F3E9; --ok-strong: #1E7D4C;\n  --warn: #6B4400; --warn-bg: #FFF3D1; --warn-edge: #E2B44C;\n  --bad: #8C1D1D; --bad-bg: #FCE9E8;\n  --mark: #FFE27A; --on-mark: #14181F;\n  --banner-bg: #FFF1C2; --banner-text: #4D3500;\n  --shadow: 0 1px 2px rgb(16 24 40 / .06), 0 4px 12px rgb(16 24 40 / .06);\n  --shadow-bar: 0 -4px 16px rgb(16 24 40 / .08);\n  --font: \"Segoe UI\", system-ui, -apple-system, \"Helvetica Neue\", Arial, sans-serif;\n  --r-card: 14px; --r-btn: 12px;\n  --gutter: 32px;\n  --banner-h: 32px; --header-h: 64px; --steps-h: 76px; --title-h: 76px;\n}\n@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) {\n  color-scheme: dark;\n  --page: #0F1216; --panel: #171B21; --sunken: #1E242C; --paper: #1B2027;\n  --border: #2C343F; --border-strong: #7A8696;\n  --text: #E8EBEF; --muted: #B4BDC9; --subtle: #9AA5B4;\n  --accent: #8AB4FF; --accent-hover: #A8C7FF; --on-accent: #0E1116; --accent-soft: #1A2A47;\n  --ok: #7BD6A0; --ok-bg: #13301F; --ok-strong: #7BD6A0;\n  --warn: #F2C265; --warn-bg: #36280B; --warn-edge: #8A6A1F;\n  --bad: #FF9A92; --bad-bg: #3D1A19;\n  --mark: #6B5800; --on-mark: #FFF7D6;\n  --banner-bg: #3A2D0B; --banner-text: #F6DE9B;\n  --shadow: 0 1px 2px rgb(0 0 0 / .4); --shadow-bar: 0 -4px 16px rgb(0 0 0 / .4);\n} }\n:root[data-theme=\"dark\"] {\n  color-scheme: dark;\n  --page: #0F1216; --panel: #171B21; --sunken: #1E242C; --paper: #1B2027;\n  --border: #2C343F; --border-strong: #7A8696;\n  --text: #E8EBEF; --muted: #B4BDC9; --subtle: #9AA5B4;\n  --accent: #8AB4FF; --accent-hover: #A8C7FF; --on-accent: #0E1116; --accent-soft: #1A2A47;\n  --ok: #7BD6A0; --ok-bg: #13301F; --ok-strong: #7BD6A0;\n  --warn: #F2C265; --warn-bg: #36280B; --warn-edge: #8A6A1F;\n  --bad: #FF9A92; --bad-bg: #3D1A19;\n  --mark: #6B5800; --on-mark: #FFF7D6;\n  --banner-bg: #3A2D0B; --banner-text: #F6DE9B;\n  --shadow: 0 1px 2px rgb(0 0 0 / .4); --shadow-bar: 0 -4px 16px rgb(0 0 0 / .4);\n}\n\n* { box-sizing: border-box; }\nhtml { font-size: 16px; scrollbar-gutter: stable; }\nbody { margin: 0; background: var(--page); color: var(--text); font: 400 1.125rem/1.75rem var(--font); -webkit-font-smoothing: antialiased; }\na { color: var(--accent); }\nh1, h2, h3, p { margin: 0; }\n:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; border-radius: 6px; }\n.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }\n.num { font-variant-numeric: tabular-nums; }\n\n/* ---------- banner, header, footer ---------- */\n.banner { height: var(--banner-h); display: flex; align-items: center; justify-content: center; gap: 8px; background: var(--banner-bg); color: var(--banner-text);\n  font-size: .9375rem; font-weight: 600; text-align: center; padding: 0 16px; }\n.banner .b-demo { display: none; font-weight: 400; }\n.header { height: var(--header-h); display: flex; align-items: center; gap: 16px; padding: 0 var(--gutter); background: var(--panel); border-bottom: 1px solid var(--border); }\n.brand { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.125rem; color: var(--text); text-decoration: none; white-space: nowrap; }\n.brand-mark { width: 30px; height: 30px; border-radius: 9px; background: var(--accent); color: var(--on-accent); display: grid; place-items: center; font-size: .9rem; font-weight: 800; }\n.back-cases { display: inline-flex; align-items: center; gap: 6px; height: 44px; padding: 0 14px 0 10px; border-radius: 10px; border: 1px solid var(--border); color: var(--text);\n  text-decoration: none; font-weight: 600; font-size: 1rem; white-space: nowrap; background: var(--panel); }\n.back-cases:hover { background: var(--sunken); }\n.case-title { font-size: 1.25rem; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; }\n.case-sub { color: var(--muted); font-size: .9375rem; white-space: nowrap; }\n.header .spacer { flex: 1; }\n.demo-pill { display: inline-flex; align-items: center; gap: 8px; height: 34px; padding: 0 14px; border-radius: 999px; background: var(--accent-soft); color: var(--text);\n  font-size: .9375rem; font-weight: 600; white-space: nowrap; }\n.demo-pill::before { content: \"\"; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }\n.theme-btn { height: 44px; min-width: 124px; border-radius: 10px; border: 1px solid var(--border-strong); background: var(--panel); color: var(--text); font: 600 .9375rem var(--font); cursor: pointer; }\n.theme-btn:hover { background: var(--sunken); }\n.footer { padding: 14px var(--gutter) 20px; color: var(--subtle); font-size: .9375rem; display: flex; gap: 16px; flex-wrap: wrap; }\n.footer a { color: var(--subtle); }\n\n/* ---------- step bar ---------- */\n.steps { height: var(--steps-h); background: var(--panel); border-bottom: 1px solid var(--border); padding: 0 var(--gutter); }\n.steps ol { list-style: none; margin: 0 auto; padding: 0; height: 100%; display: grid; grid-template-columns: repeat(4, 1fr); max-width: 1376px; }\n.steps li { position: relative; display: flex; }\n.steps li + li::before { content: \"\"; position: absolute; left: -22px; width: 30px; top: 50%; border-top: 2px solid var(--border); }\n.step { flex: 1; display: flex; align-items: center; gap: 12px; padding: 0 20px 0 0; text-decoration: none; color: var(--text); position: relative; min-width: 0; }\n.step::after { content: \"\"; position: absolute; left: 0; right: 20px; bottom: 0; height: 4px; border-radius: 4px 4px 0 0; background: transparent; }\n.step .dot { flex: none; width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font-weight: 700; font-size: 1rem; border: 2px solid var(--border-strong); color: var(--muted); background: var(--panel); }\n.step .st-text { display: flex; flex-direction: column; min-width: 0; }\n.step .st-label { font-weight: 600; font-size: 1.0625rem; line-height: 1.375rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n.step .st-label .short { display: none; }\n.step .st-status { font-size: .9375rem; line-height: 1.25rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n.step.done .dot { background: var(--ok-strong); border-color: var(--ok-strong); color: #fff; }\n.step.done .st-status { color: var(--ok); font-weight: 600; }\n.step.current .dot { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }\n.step.current .st-label { font-weight: 800; }\n.step.current .st-status { color: var(--text); font-weight: 600; }\n.step.current::after { background: var(--accent); }\n.step.attn .dot { background: var(--warn-bg); border-color: var(--warn-edge); color: var(--warn); }\n.step.attn .st-status { color: var(--warn); font-weight: 600; }\n.step.locked { opacity: .6; cursor: default; }\na.step:not(.locked):hover .st-label { text-decoration: underline; }\n\n/* ---------- review frame ---------- */\nbody.frame { height: 100vh; height: 100dvh; overflow: hidden; display: grid; grid-template-rows: var(--banner-h) var(--header-h) var(--steps-h) var(--title-h) minmax(0, 1fr) auto; }\n.titlebar { display: flex; align-items: center; gap: 24px; padding: 0 var(--gutter); max-width: 1440px; width: 100%; margin: 0 auto; }\n.titlebar .t-main { flex: 1; min-width: 0; }\n.eyebrow { font-size: .9375rem; font-weight: 600; color: var(--accent); letter-spacing: .01em; }\n.titlebar h1 { font-size: 1.75rem; line-height: 2.25rem; font-weight: 750; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n.titlebar .t-ai { font-size: .9375rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n.count-box { width: 300px; flex: none; }\n.count-line { display: flex; justify-content: space-between; font-size: 1rem; font-weight: 600; }\n.count-line .of { color: var(--muted); font-weight: 400; }\n.bar { height: 10px; border-radius: 999px; background: var(--sunken); overflow: hidden; margin-top: 8px; border: 1px solid var(--border); }\n.bar > i { display: block; height: 100%; background: var(--accent); border-radius: 999px; }\n.total-chip { flex: none; width: 250px; padding: 10px 16px; border-radius: 12px; background: var(--panel); border: 1px solid var(--border); box-shadow: var(--shadow); }\n.total-chip .tc-l { font-size: .875rem; color: var(--muted); }\n.total-chip .tc-v { font-size: 1.375rem; font-weight: 750; }\n\n.work { min-height: 0; padding: 0 var(--gutter) 20px; max-width: 1440px; width: 100%; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }\n.card { background: var(--panel); border: 1px solid var(--border); border-radius: var(--r-card); box-shadow: var(--shadow); display: flex; flex-direction: column; min-height: 0; overflow: hidden; }\n.card-h { flex: none; padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; min-height: 64px; }\n.card-h .ch-title { font-weight: 700; font-size: 1.0625rem; }\n.card-h .ch-sub { color: var(--muted); font-size: 1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n.card-b { flex: 1; min-height: 0; overflow: auto; padding: 20px 24px; }\n.card-f { flex: none; min-height: 112px; padding: 16px 24px; border-top: 1px solid var(--border); background: var(--sunken); font-size: 1rem; line-height: 1.5rem; color: var(--muted); }\n.card-f.attn { background: var(--warn-bg); color: var(--text); border-top-color: var(--warn-edge); }\n.card-f.ok { background: var(--ok-bg); color: var(--text); }\n.card-f.bad { background: var(--bad-bg); color: var(--text); }\n.card-f strong { color: var(--text); }\n.label-cap { font-size: .875rem; font-weight: 700; color: var(--muted); text-transform: none; letter-spacing: .01em; }\n\n.rec { font-size: 1.125rem; line-height: 1.8rem; white-space: pre-wrap; }\n.rec + .rec-h { margin-top: 24px; padding-top: 20px; border-top: 1px dashed var(--border); }\n.rec-h { font-weight: 700; font-size: 1rem; color: var(--muted); margin-bottom: 8px; }\n.rec .meta { color: var(--muted); }\nmark { background: var(--mark); color: var(--on-mark); border-radius: 4px; padding: 1px 2px; box-shadow: 0 0 0 2px var(--mark); }\n.sent { border-radius: 6px; padding: 1px 2px; box-shadow: inset 0 0 0 2px var(--border-strong); cursor: pointer; }\n.sent.on { background: var(--mark); color: var(--on-mark); box-shadow: inset 0 0 0 2px var(--warn-edge); }\n.also { margin-top: 20px; padding: 14px 16px; border-radius: 10px; background: var(--sunken); font-size: 1rem; line-height: 1.5rem; color: var(--muted); }\n.also q { color: var(--text); }\n\n.tag { display: inline-flex; align-items: center; height: 28px; padding: 0 12px; border-radius: 999px; font-size: .875rem; font-weight: 700; white-space: nowrap; }\n.tag.prep { background: var(--accent-soft); color: var(--text); }\n.tag.ai { background: var(--accent-soft); color: var(--text); }\n.tag.you { background: var(--ok-bg); color: var(--ok); }\n.tag.warn { background: var(--warn-bg); color: var(--warn); border: 1px solid var(--warn-edge); }\n.tag.ok { background: var(--ok-bg); color: var(--ok); }\n.tag.never { background: var(--sunken); color: var(--muted); border: 1px solid var(--border); }\n.tag.bad { background: var(--bad-bg); color: var(--bad); }\n.line-when { font-weight: 700; font-size: 1.0625rem; margin-bottom: 10px; }\n.line-text { font-size: 1.375rem; line-height: 2rem; font-weight: 500; }\n.money { font-size: 2.5rem; line-height: 3rem; font-weight: 750; font-variant-numeric: tabular-nums; }\n.warn-title { font-size: 1.25rem; line-height: 1.75rem; font-weight: 700; margin-bottom: 10px; }\n.explain { font-size: 1.0625rem; line-height: 1.7rem; }\n.muted { color: var(--muted); }\ntextarea.edit { width: 100%; height: 100%; min-height: 160px; resize: none; font: 500 1.375rem/2rem var(--font); color: var(--text); background: var(--panel); border: 2px solid var(--accent);\n  border-radius: 10px; padding: 12px 14px; }\n.check { display: flex; gap: 14px; align-items: flex-start; cursor: pointer; font-weight: 600; color: var(--text); font-size: 1.0625rem; line-height: 1.6rem; margin-top: 10px; }\n.check input { flex: none; width: 28px; height: 28px; margin: 0; accent-color: var(--accent); cursor: pointer; }\n\n/* ---------- action bar ---------- */\n.actions { background: var(--panel); border-top: 1px solid var(--border); box-shadow: var(--shadow-bar); }\n.actions-in { max-width: 1440px; margin: 0 auto; padding: 14px var(--gutter) 12px; display: grid; grid-template-columns: auto 1fr; grid-template-areas: \"q q\" \"big small\" \"status status\"; column-gap: 24px; row-gap: 10px; align-items: center; }\n.question { grid-area: q; font-size: 1.25rem; line-height: 1.75rem; font-weight: 700; min-height: 1.75rem; }\n.big { grid-area: big; display: flex; gap: 16px; }\n.small { grid-area: small; display: flex; gap: 8px; justify-content: flex-end; }\n.status { grid-area: status; min-height: 1.5rem; font-size: 1rem; line-height: 1.5rem; color: var(--muted); }\n.status b { color: var(--ok); }\n.btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; height: 48px; padding: 0 18px; border-radius: var(--r-btn); border: 2px solid var(--border-strong);\n  background: var(--panel); color: var(--text); font: 650 1.0625rem var(--font); text-decoration: none; cursor: pointer; white-space: nowrap; }\n.btn:hover { background: var(--sunken); }\n.btn.answer { height: 56px; width: 270px; font-size: 1.1875rem; }\n.btn.primary { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }\n.btn.primary:hover { background: var(--accent-hover); border-color: var(--accent-hover); }\n.btn.quiet { border-color: transparent; color: var(--accent); background: transparent; padding: 0 14px; }\n.btn.quiet:hover { background: var(--accent-soft); }\n.btn.go { background: var(--ok-strong); border-color: var(--ok-strong); color: #fff; }\n.btn[aria-disabled=\"true\"], .btn:disabled { opacity: .45; cursor: not-allowed; pointer-events: none; }\n.btn.danger { color: var(--bad); border-color: var(--bad); }\n.btn.wide { width: 100%; }\n.btn.lg { height: 56px; font-size: 1.1875rem; padding: 0 28px; }\n.chip-sug { display: inline-block; margin-left: 8px; padding: 2px 8px; border-radius: 999px; background: var(--ok-bg); color: var(--ok); font-size: .8125rem; font-weight: 700; }\n.btn.answer .sub { display: block; font-size: .875rem; font-weight: 500; opacity: .85; }\n.btn.answer.two { flex-direction: column; gap: 0; line-height: 1.3rem; }\n\n/* ---------- single-panel pages (step 1, done screens, step 4) ---------- */\nbody.page { min-height: 100vh; display: flex; flex-direction: column; }\nbody.page .stick { position: sticky; top: 0; z-index: 5; }\n.wrap { max-width: 1180px; width: 100%; margin: 0 auto; padding: 28px var(--gutter) 24px; flex: 1; }\n.wrap.wide { max-width: 1440px; }\n.page-h { display: flex; align-items: flex-end; gap: 24px; margin-bottom: 24px; }\n.page-h .ph-main { flex: 1; }\n.page-h h1 { font-size: 2rem; line-height: 2.5rem; font-weight: 750; }\n.page-h p { color: var(--muted); margin-top: 6px; }\n.panel { background: var(--panel); border: 1px solid var(--border); border-radius: var(--r-card); box-shadow: var(--shadow); padding: 28px; }\n.panel + .panel { margin-top: 20px; }\n.panel h2 { font-size: 1.375rem; line-height: 1.875rem; font-weight: 700; margin-bottom: 8px; }\n.done-hero { display: flex; gap: 20px; align-items: center; }\n.done-hero .big-check { flex: none; width: 64px; height: 64px; border-radius: 50%; background: var(--ok-strong); color: #fff; display: grid; place-items: center; font-size: 2rem; font-weight: 800; }\n.done-hero .big-warn { flex: none; width: 64px; height: 64px; border-radius: 50%; background: var(--warn-bg); color: var(--warn); border: 2px solid var(--warn-edge); display: grid; place-items: center; font-size: 2rem; font-weight: 800; }\n.done-hero h2 { font-size: 1.625rem; line-height: 2.125rem; margin: 0; }\n.done-hero p { color: var(--muted); margin-top: 4px; }\n.row-actions { display: flex; gap: 12px; margin-top: 24px; flex-wrap: wrap; }\n.note-box { padding: 16px 20px; border-radius: 12px; border: 1px solid var(--warn-edge); background: var(--warn-bg); display: flex; gap: 16px; align-items: center; justify-content: space-between; }\n.note-box.ok { border-color: transparent; background: var(--ok-bg); }\n.note-box.bad { border-color: var(--bad); background: var(--bad-bg); }\n.note-box .nb-text { font-weight: 600; }\n.note-box .nb-text span { display: block; font-weight: 400; color: var(--muted); }\n\n/* choice tiles */\n.tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 20px 0; }\n.tile { position: relative; display: block; padding: 22px; border-radius: 14px; border: 2px solid var(--border); background: var(--panel); cursor: pointer; min-height: 128px; }\n.tile input { position: absolute; opacity: 0; }\n.tile .tl-h { display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 1.1875rem; }\n.tile .tl-h::before { content: \"\"; width: 22px; height: 22px; border-radius: 50%; border: 2px solid var(--border-strong); flex: none; }\n.tile p { color: var(--muted); margin-top: 8px; font-size: 1rem; line-height: 1.5rem; }\n.tile:has(input:checked) { border-color: var(--accent); background: var(--accent-soft); }\n.tile:has(input:checked) .tl-h::before { border: 7px solid var(--accent); }\n.tile:has(input:focus-visible) { outline: 3px solid var(--accent); outline-offset: 2px; }\n.input-box { height: 280px; border-radius: 14px; border: 2px dashed var(--border-strong); background: var(--sunken); display: grid; place-items: center; text-align: center; padding: 24px; }\n.input-box textarea { width: 100%; height: 100%; border: 0; background: transparent; font: 400 1rem/1.5rem var(--font); color: var(--text); resize: none; }\n.input-box.solid { border-style: solid; background: var(--panel); place-items: stretch; padding: 16px; }\n.field { display: flex; flex-direction: column; gap: 8px; max-width: 520px; }\n.field label { font-weight: 700; }\n.field input { height: 52px; padding: 0 14px; border-radius: 10px; border: 2px solid var(--border-strong); background: var(--panel); color: var(--text); font: 400 1.125rem var(--font); }\n.field .hint { color: var(--muted); font-size: .9375rem; }\n.err-slot { min-height: 28px; margin-top: 12px; color: var(--bad); font-weight: 600; font-size: 1rem; }\n\n/* records list, stage checklist */\n.list { list-style: none; margin: 0; padding: 0; border: 1px solid var(--border); border-radius: 12px; overflow: auto; }\n.list li { display: grid; grid-template-columns: 44px 210px 1fr; gap: 12px; padding: 12px 16px; border-bottom: 1px solid var(--border); font-size: 1.0625rem; }\n.list li:last-child { border-bottom: 0; }\n.list .n { color: var(--muted); font-weight: 700; }\n.stages { list-style: none; margin: 18px 0 0; padding: 0; display: grid; gap: 4px; }\n.stages li { display: flex; align-items: center; gap: 14px; height: 44px; font-size: 1.0625rem; color: var(--muted); }\n.stages .ic { width: 28px; height: 28px; border-radius: 50%; border: 2px solid var(--border-strong); flex: none; display: grid; place-items: center; font-size: .875rem; font-weight: 800; }\n.stages li.done { color: var(--text); }\n.stages li.done .ic { background: var(--ok-strong); border-color: var(--ok-strong); color: #fff; }\n.stages li.now { color: var(--text); font-weight: 700; }\n.stages li.now .ic { border-color: var(--accent); border-top-color: transparent; animation: spin 1s linear infinite; }\n@keyframes spin { to { transform: rotate(360deg); } }\n@media (prefers-reduced-motion: reduce) { .stages li.now .ic { animation: none; border-top-color: var(--accent); } }\n.fixed-box { min-height: 520px; }\n\n/* answers list */\n.answers { list-style: none; margin: 12px 0 0; padding: 0; border: 1px solid var(--border); border-radius: 12px; }\n.answers li { display: grid; grid-template-columns: 52px 170px 1fr 170px 110px; align-items: center; gap: 12px; padding: 10px 16px; border-bottom: 1px solid var(--border); font-size: 1rem; }\n.answers li:last-child { border-bottom: 0; }\n.answers .n { color: var(--muted); font-weight: 700; }\n.answers .d { color: var(--muted); }\n.answers .lbl { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }\n.answers .btn { height: 44px; }\n\n/* bills summary table */\n.mini { width: 100%; border-collapse: collapse; font-size: 1.0625rem; }\n.mini th { text-align: left; font-size: .9375rem; color: var(--muted); font-weight: 700; padding: 8px 12px; border-bottom: 1px solid var(--border); }\n.mini td { padding: 12px; border-bottom: 1px solid var(--border); vertical-align: top; }\n.mini td.amt { font-weight: 700; white-space: nowrap; font-variant-numeric: tabular-nums; }\n.total-line { font-size: 1.5rem; line-height: 2rem; font-weight: 750; padding: 18px 20px; border-radius: 12px; background: var(--accent-soft); margin-top: 16px; }\n\n/* letter */\n.letter-grid { display: grid; grid-template-columns: 3fr 2fr; gap: 24px; }\n.doc { background: var(--paper); border: 1px solid var(--border); border-radius: 12px; height: 520px; overflow: auto; padding: 28px 32px; white-space: pre-wrap; font-size: 1.0625rem; line-height: 1.65rem; }\n.doc.notes { background: var(--sunken); font-size: .9375rem; line-height: 1.45rem; }\n.doc.placeholder { display: grid; place-items: center; color: var(--muted); text-align: center; white-space: normal; }\n.doc-h { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 12px; }\n.doc-h h2 { margin: 0; }\n.doc-actions { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }\n.doc-actions .btn { min-width: 200px; }\n.cfg { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)) auto; gap: 12px; align-items: end; margin-top: 12px; }\n.cfg .field input { width: 100%; }\n.blockers { list-style: none; margin: 16px 0 0; padding: 0; display: grid; gap: 10px; }\n.blockers li { display: flex; gap: 16px; align-items: center; justify-content: space-between; padding: 14px 16px; border-radius: 10px; background: var(--panel); border: 1px solid var(--border); }\n\n/* ---------- home ---------- */\n.home-h { display: flex; align-items: flex-end; gap: 24px; margin-bottom: 8px; }\n.home-h h1 { font-size: 2.25rem; line-height: 2.75rem; font-weight: 800; }\n.home-h p { color: var(--muted); margin-top: 6px; }\n.find { margin: 20px 0 8px; max-width: 420px; }\n.find input { width: 100%; height: 48px; border-radius: 10px; border: 2px solid var(--border-strong); background: var(--panel); color: var(--text); font: 400 1.0625rem var(--font); padding: 0 14px; }\n.sec-h { font-size: 1.25rem; font-weight: 750; margin: 28px 0 14px; display: flex; gap: 10px; align-items: baseline; }\n.sec-h .c { color: var(--muted); font-weight: 600; }\n.cases { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }\n.ccard { height: 244px; background: var(--panel); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 22px 24px; display: grid; grid-template-rows: auto auto auto 1fr auto; gap: 10px; }\n.ccard .cc-top { display: flex; gap: 12px; align-items: flex-start; }\n.ccard h3 { flex: 1; min-width: 0; font-size: 1.3125rem; line-height: 1.75rem; font-weight: 750; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }\n.ccard .cc-meta { color: var(--muted); font-size: .9375rem; line-height: 1.25rem; }\n.track { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }\n.track li { display: flex; flex-direction: column; gap: 6px; font-size: .8125rem; line-height: 1rem; color: var(--muted); }\n.track li i { display: block; height: 8px; border-radius: 999px; background: var(--sunken); border: 1px solid var(--border); }\n.track li.done i { background: var(--ok-strong); border-color: var(--ok-strong); }\n.track li.current i { background: var(--accent); border-color: var(--accent); }\n.track li.current { color: var(--text); font-weight: 700; }\n.track li.attn i { background: var(--warn-edge); border-color: var(--warn-edge); }\n.track li.attn { color: var(--warn); font-weight: 700; }\n.ccard .next { font-size: 1.0625rem; line-height: 1.5rem; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }\n.ccard .next b { font-weight: 750; }\n.ccard .next.ok { color: var(--ok); }\n.ccard .next.warn { color: var(--warn); }\n.ccard .cc-bottom { display: flex; gap: 10px; align-items: center; }\n.ccard .cc-bottom .btn.lg { flex: 1; }\n.skel { background: linear-gradient(90deg, var(--sunken), var(--panel), var(--sunken)); background-size: 200% 100%; animation: sk 1.4s ease infinite; border-radius: 8px; }\n@keyframes sk { to { background-position: -200% 0; } }\n@media (prefers-reduced-motion: reduce) { .skel { animation: none; } }\n.empty { text-align: center; padding: 64px 24px; }\n.empty .em-ic { width: 88px; height: 88px; margin: 0 auto 20px; border-radius: 24px; background: var(--accent-soft); color: var(--accent); display: grid; place-items: center; font-size: 2.5rem; font-weight: 800; }\n.empty h2 { font-size: 1.75rem; line-height: 2.25rem; }\n.empty p { color: var(--muted); margin: 8px auto 0; max-width: 520px; }\n.empty .row-actions { justify-content: center; }\n\n/* screens index */\n.screens { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }\n.screens a { display: block; padding: 16px 18px; border-radius: 12px; background: var(--panel); border: 1px solid var(--border); text-decoration: none; color: var(--text); }\n.screens a b { display: block; }\n.screens a span { color: var(--muted); font-size: .9375rem; line-height: 1.375rem; }\n.variant { font-size: .8125rem; font-weight: 700; color: var(--warn); }\n\n/* ---------- phones ---------- */\n@media (max-width: 760px) {\n  :root { --gutter: 16px; --banner-h: 44px; --header-h: 56px; --steps-h: 62px; --title-h: 58px; }\n  body { font-size: 1.0625rem; line-height: 1.6rem; }\n  .banner { font-size: .8125rem; line-height: 1.05rem; flex-direction: column; gap: 0; }\n  .banner .b-demo { display: block; }\n  .header { gap: 8px; }\n  .demo-pill, .header .case-sub { display: none; }\n  .brand span:last-child { font-size: 1rem; }\n  .back-cases { height: 40px; padding: 0 10px 0 6px; font-size: .9375rem; }\n  .back-cases .long { display: none; }\n  .case-title { font-size: 1.0625rem; }\n  .theme-btn { min-width: 0; width: 44px; height: 40px; font-size: 0; position: relative; }\n  .theme-btn::after { content: \"\\25D0\"; font-size: 1.25rem; }\n  .steps { padding: 0 8px; }\n  .steps li + li::before { display: none; }\n  .step { flex-direction: column; justify-content: center; gap: 3px; padding: 0 2px; text-align: center; }\n  .step::after { left: 8px; right: 8px; }\n  .step .dot { width: 26px; height: 26px; font-size: .8125rem; }\n  .step .st-text { align-items: center; }\n  .step .st-label { font-size: .8125rem; line-height: 1rem; }\n  .step .st-label .long { display: none; }\n  .step .st-label .short { display: inline; }\n  .step .st-status { font-size: .75rem; line-height: .95rem; }\n  .titlebar { gap: 12px; }\n  .titlebar .eyebrow, .titlebar .t-ai { display: none; }\n  .titlebar h1 { font-size: 1.25rem; line-height: 1.625rem; }\n  .count-box { width: 132px; }\n  .count-line { font-size: .875rem; }\n  .count-line .of { display: none; }\n  .bar { height: 8px; margin-top: 4px; }\n  .total-chip { width: 148px; padding: 6px 10px; }\n  .total-chip .tc-l { font-size: .75rem; line-height: 1rem; }\n  .total-chip .tc-v { font-size: 1.0625rem; line-height: 1.4rem; }\n  .work { grid-template-columns: 1fr; grid-template-rows: minmax(0, 1fr) 196px; gap: 10px; padding-bottom: 10px; }\n  .card-h { padding: 10px 14px; min-height: 48px; gap: 8px; }\n  .card-h .ch-title { font-size: .9375rem; }\n  .card-h .ch-sub { font-size: .875rem; }\n  .card-b { padding: 12px 14px; }\n  .card-f { min-height: 0; padding: 10px 14px; font-size: .875rem; line-height: 1.3rem; }\n  .rec { font-size: 1rem; line-height: 1.6rem; }\n  .line-when { font-size: .9375rem; margin-bottom: 4px; }\n  .line-text { font-size: 1.125rem; line-height: 1.6rem; }\n  .money { font-size: 2rem; line-height: 2.5rem; }\n  .warn-title { font-size: 1.0625rem; line-height: 1.5rem; margin-bottom: 4px; }\n  .explain { font-size: .9375rem; line-height: 1.4rem; }\n  textarea.edit { font-size: 1.0625rem; line-height: 1.5rem; min-height: 0; }\n  .check { font-size: .9375rem; line-height: 1.35rem; gap: 10px; margin-top: 6px; }\n  .check input { width: 26px; height: 26px; }\n  .actions-in { grid-template-columns: 1fr; grid-template-areas: \"q\" \"big\" \"small\" \"status\"; padding: 10px 16px 8px; row-gap: 8px; }\n  .question { font-size: 1.0625rem; line-height: 1.4rem; min-height: 2.8rem; display: flex; align-items: center; }\n  .big { gap: 10px; }\n  .btn.answer { flex: 1; width: auto; min-width: 0; height: 54px; font-size: 1.0625rem; padding: 0 8px; white-space: normal; text-align: center; line-height: 1.25rem; }\n  .btn.answer .sub { font-size: .75rem; }\n  .small { justify-content: space-between; gap: 4px; }\n  .small .btn { height: 44px; font-size: .9375rem; padding: 0 8px; }\n  .status { font-size: .875rem; min-height: 1.25rem; line-height: 1.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n  .wrap { padding: 20px 16px; }\n  .page-h { flex-direction: column; align-items: stretch; gap: 12px; }\n  .page-h h1 { font-size: 1.625rem; line-height: 2.125rem; }\n  .panel { padding: 18px; }\n  .tiles { grid-template-columns: 1fr; gap: 10px; }\n  .tile { min-height: 0; padding: 16px; }\n  .input-box { height: 220px; }\n  .list li { grid-template-columns: 30px 1fr; }\n  .list li .src { grid-column: 2; }\n  .done-hero { align-items: flex-start; }\n  .done-hero .big-check, .done-hero .big-warn { width: 48px; height: 48px; font-size: 1.5rem; }\n  .done-hero h2 { font-size: 1.3125rem; line-height: 1.75rem; }\n  .answers li { grid-template-columns: 34px 1fr auto; grid-template-areas: \"n lbl btn\" \"n d btn\" \"n ans btn\"; row-gap: 2px; }\n  .answers .n { grid-area: n; } .answers .d { grid-area: d; font-size: .875rem; } .answers .lbl { grid-area: lbl; } .answers .ans { grid-area: ans; } .answers .btn { grid-area: btn; }\n  .note-box { flex-direction: column; align-items: stretch; }\n  .letter-grid { grid-template-columns: 1fr; }\n  .doc { height: 420px; padding: 18px; font-size: .9375rem; line-height: 1.45rem; }\n  .doc.notes { height: 320px; font-size: .875rem; }\n  .doc-actions .btn { min-width: 0; flex: 1; }\n  .cfg { grid-template-columns: 1fr; }\n  .mini { font-size: .9375rem; }\n  .mini th:nth-child(3), .mini td:nth-child(3) { display: none; }\n  .home-h { flex-direction: column; align-items: stretch; gap: 14px; }\n  .home-h h1 { font-size: 1.875rem; line-height: 2.25rem; }\n  .cases { grid-template-columns: 1fr; }\n  .ccard { height: 252px; padding: 18px; }\n  .ccard h3 { font-size: 1.1875rem; }\n  .track li { font-size: .6875rem; }\n  .screens { grid-template-columns: 1fr; }\n  .footer { padding: 12px 16px 16px; font-size: .875rem; }\n}\n"
}
````

### User / tool · 2026-11-02T20:44:41.438Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/mockups/guided/guided.css (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:45:02.760Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/mockups/guided/guided.js",
 "content": "/* Guided UI mockup behaviour (T-180). Static demo only: no network, no backend. Every change swaps text inside boxes that keep their size. */\n(function () {\n  \"use strict\";\n  var root = document.documentElement;\n\n  // Theme: follow the OS unless the visitor picked one. Remembered when storage works; the page works without it.\n  function applyTheme(t) { if (t === \"light\" || t === \"dark\") root.setAttribute(\"data-theme\", t); else root.removeAttribute(\"data-theme\"); }\n  var saved = null; try { saved = localStorage.getItem(\"zl.guided.theme\"); } catch (e) { saved = null; }\n  applyTheme(saved);\n  function isDark() { var t = root.getAttribute(\"data-theme\"); return t ? t === \"dark\" : matchMedia(\"(prefers-color-scheme: dark)\").matches; }\n  function label(btn) { btn.textContent = isDark() ? \"Light mode\" : \"Dark mode\"; btn.setAttribute(\"aria-label\", btn.textContent); }\n\n  document.addEventListener(\"DOMContentLoaded\", function () {\n    document.querySelectorAll(\"[data-theme-btn]\").forEach(function (b) {\n      label(b);\n      b.addEventListener(\"click\", function () {\n        var t = isDark() ? \"light\" : \"dark\"; applyTheme(t);\n        try { localStorage.setItem(\"zl.guided.theme\", t); } catch (e) { /* not remembered */ }\n        document.querySelectorAll(\"[data-theme-btn]\").forEach(label);\n      });\n    });\n\n    // A checkbox that unlocks a button (compare confirm, named charge confirms, copy anyway). The button keeps its place and size.\n    document.querySelectorAll(\"[data-unlocks]\").forEach(function (box) {\n      var ids = box.getAttribute(\"data-unlocks\").split(\" \");\n      function sync() {\n        var group = document.querySelectorAll('[data-unlocks=\"' + box.getAttribute(\"data-unlocks\") + '\"]');\n        var all = Array.prototype.every.call(group, function (b) { return b.checked; });\n        ids.forEach(function (id) { var t = document.getElementById(id); if (t) { t.setAttribute(\"aria-disabled\", all ? \"false\" : \"true\"); t.tabIndex = all ? 0 : -1; } });\n      }\n      box.addEventListener(\"change\", sync); sync();\n    });\n\n    // Tappable sentences (choose the highlighted words).\n    document.querySelectorAll(\".sent\").forEach(function (s) {\n      s.setAttribute(\"role\", \"checkbox\"); s.tabIndex = 0;\n      s.setAttribute(\"aria-checked\", s.classList.contains(\"on\") ? \"true\" : \"false\");\n      function flip() { s.classList.toggle(\"on\"); s.setAttribute(\"aria-checked\", s.classList.contains(\"on\") ? \"true\" : \"false\"); }\n      s.addEventListener(\"click\", flip);\n      s.addEventListener(\"keydown\", function (e) { if (e.key === \" \" || e.key === \"Enter\") { e.preventDefault(); flip(); } });\n    });\n\n    // Scroll the source card (not the page) so the first highlight is in view.\n    document.querySelectorAll(\"[data-scroll-mark]\").forEach(function (body) {\n      var m = body.querySelector(\"mark\"); if (m) body.scrollTop = Math.max(0, m.offsetTop - body.offsetTop - 24);\n    });\n\n    // Copy buttons: the label says \"Copied\" for 2 s at the same width.\n    document.querySelectorAll(\"[data-copy]\").forEach(function (b) {\n      b.addEventListener(\"click\", function () {\n        var src = document.getElementById(b.getAttribute(\"data-copy\")); if (!src) return;\n        var done = function () { var old = b.getAttribute(\"data-label\") || b.textContent; b.setAttribute(\"data-label\", old); b.textContent = \"Copied\"; setTimeout(function () { b.textContent = old; }, 2000); };\n        try { navigator.clipboard.writeText(src.textContent).then(done, done); } catch (e) { done(); }\n      });\n    });\n\n    // Download buttons: a client-side text file (code, no server).\n    document.querySelectorAll(\"[data-download]\").forEach(function (b) {\n      b.addEventListener(\"click\", function () {\n        var src = document.getElementById(b.getAttribute(\"data-download\")); if (!src) return;\n        var a = document.createElement(\"a\");\n        a.href = URL.createObjectURL(new Blob([src.textContent], { type: \"text/plain\" }));\n        a.download = b.getAttribute(\"data-name\") || \"letter.txt\"; a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);\n      });\n    });\n\n    // Find a case (home): filters the cards as she types.\n    var find = document.getElementById(\"find-case\");\n    if (find) find.addEventListener(\"input\", function () {\n      var q = find.value.trim().toLowerCase();\n      document.querySelectorAll(\".ccard\").forEach(function (c) { c.hidden = q && c.getAttribute(\"data-title\").toLowerCase().indexOf(q) < 0; });\n    });\n\n    // Delete confirm swaps the card's bottom row in place.\n    document.querySelectorAll(\"[data-delete]\").forEach(function (b) {\n      b.addEventListener(\"click\", function () {\n        var row = b.closest(\".cc-bottom\"); var ask = row.nextElementSibling;\n        row.hidden = true; ask.hidden = false; ask.querySelector(\"button\").focus();\n      });\n    });\n    document.querySelectorAll(\"[data-keep]\").forEach(function (b) {\n      b.addEventListener(\"click\", function () { var ask = b.closest(\".cc-bottom\"); ask.hidden = true; ask.previousElementSibling.hidden = false; });\n    });\n\n    // Drafting: walk the fixed stage list, then show the done box in the same place.\n    var stages = document.getElementById(\"stages\");\n    if (stages) {\n      var items = stages.querySelectorAll(\"li\"); var i = parseInt(stages.getAttribute(\"data-start\") || \"0\", 10);\n      var bar = document.getElementById(\"draft-bar\"); var count = document.getElementById(\"draft-count\");\n      var running = document.getElementById(\"draft-running\"); var finished = document.getElementById(\"draft-done\");\n      var tick = function () {\n        items.forEach(function (li, k) { li.className = k < i ? \"done\" : (k === i ? \"now\" : \"\"); li.querySelector(\".ic\").textContent = k < i ? \"✓\" : \"\"; });\n        if (bar) bar.style.width = Math.round((i / items.length) * 100) + \"%\";\n        if (count) count.textContent = Math.min(i + 1, items.length) + \" of \" + items.length;\n        if (i >= items.length) { if (running) running.hidden = true; if (finished) { finished.hidden = false; var go = finished.querySelector(\".btn\"); if (go) go.focus(); } return; }\n        i += 1; setTimeout(tick, stages.hasAttribute(\"data-slow\") ? 2600 : 900);\n      };\n      if (!stages.hasAttribute(\"data-hold\")) tick();\n    }\n  });\n})();\n"
}
````

### User / tool · 2026-11-02T20:45:02.815Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/mockups/guided/guided.js (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:46:25.323Z

**tool call — Bash**
````
{
 "command": "cd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 -c \"\nimport json;d=json.load(open('$S/sample_case.json'));c=d['checks'];print(json.dumps(c,indent=0)[:2500])\nprint(d['status'], [ (r['seq'], r['char_start']) for r in d['records']][:3])\n\"; curl -s http://127.0.0.1:8766/api/cases/1MFDLCqOioc5LIygQzGFyQ/export | python3 -c \"import sys,json;d=json.load(sys.stdin);print(d.get('error') or d.keys())\"",
 "description": "Get checks labels from sample case"
}
````

### User / tool · 2026-11-02T20:46:25.467Z

**tool result**
````
{
"conflict_types": [
"plan_vs_early_end",
"denial_vs_history",
"accident_date",
"provider_name"
],
"labels": {
"plan_vs_early_end": "A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early",
"denial_vs_history": "A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record",
"accident_date": "A stated accident date against the dates of the records, or two different stated accident dates",
"provider_name": "The same clinician named under two different practice names"
},
"skipped": [],
"not_checked": [
{
"type": "dosage",
"label": "Medication doses that differ between records"
},
{
"type": "laterality",
"label": "Left versus right across records (checked only inside one summary)"
},
{
"type": "diagnosis",
"label": "A diagnosis that differs or is withdrawn between records"
},
{
"type": "pain_score",
"label": "Pain scores that differ on the same day"
},
{
"type": "treatment_duration_months",
"label": "Plans and outcomes measured in months"
},
{
"type": "informant_history",
"label": "Patient history reported by a relative"
}
],
"notes": []
}
ready [(1, 106), (2, 315), (3, 555)]
{'code': 'export_blocked', 'message': 'Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.', 'detail': {'blockers': [{'item_id': None, 'kind': 'case', 'reason_code': 'NOTHING_ACCEPTED', 'why': 'Nothing is accepted or edited yet, so the letter would be empty.', 'next_action': {'code': 'DECIDE', 'text': 'Accept, edit or dismiss this item.', 'target': {'view': 'queue'}}}]}}
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:08.473Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/mockups/guided/build.py",
 "content": "\"\"\"Builds the static guided-UI mockup pages (T-180, D-068). Run: python3 artifacts/mockups/guided/build.py\nContent is the Appendix A sample case (SYNTHETIC) and two synthetic library cases, taken from a fixture-backend run of the real API\n(answers: prepared). Pages marked \"state variant\" in screens.html show a state the sample does not produce, on sample content.\nNo backend, no network. Spec: docs/GUIDED_UI_SPEC.md.\"\"\"\nfrom html import escape as e\nfrom pathlib import Path\n\nOUT = Path(__file__).resolve().parent\nBANNER = \"Synthetic data only — never paste real records\"\nDEMO = \"Demo: sample answers prepared by our team\"\nDEMO_NOTE = \"The AI's own answers on these cases are in the evaluation report.\"\nAI_BANNER = \"In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item.\"\n\n# ---------------------------------------------------------------- record texts (verbatim from the synthetic inputs)\nRIVERA = {\n    1: (\"2026-01-09\", \"Austin EMS run report\", \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"),\n    2: (\"2026-01-09\", \"Central ER discharge summary\", \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.\"),\n    3: (\"2026-01-16\", \"Dr. Alvarez, primary care\", \"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved.\"),\n    4: (\"2026-01-23\", \"Capital PT, initial evaluation\", \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\"),\n    5: (\"2026-02-20\", \"Capital PT, visit 8\", \"Pain 4/10, improving. Patient reports missing 3 days of work.\"),\n    6: (\"2026-03-06\", \"Capital PT, visit 9\", \"Discharged from PT after two missed appointments. Pain 3/10.\"),\n    7: (\"2026-05-18\", \"Hill Country Pain Management, new patient\", \"New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.\"),\n    8: (\"2026-05-29\", \"Austin Imaging, cervical MRI\", \"C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.\"),\n    9: (\"2026-06-12\", \"Hill Country Pain Management, follow-up\", \"Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.\"),\n}\nLIB11_R9 = (\"2026-06-15\", \"Fennimoor Spine Clinic, itemized ledger\",\n            \"Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.\")\nC01_R8 = (\"04/05/2026\", \"Dr. Orla Pennywhistle, phone note\", \"Patient reports no new symptoms.\")\n\nMONTHS = [\"January\", \"February\", \"March\", \"April\", \"May\", \"June\", \"July\", \"August\", \"September\", \"October\", \"November\", \"December\"]\n\n\ndef long_date(iso):\n    y, m, d = iso.split(\"-\")\n    return f\"{MONTHS[int(m) - 1]} {int(d)}, {y}\"\n\n\n# ---------------------------------------------------------------- the four cases' step states (state, status)\nLABELS = [(\"Add records\", \"Records\"), (\"Check the timeline\", \"Timeline\"), (\"Check the bills\", \"Bills\"), (\"Get your letter\", \"Letter\")]\nSTEP_PAGES = {\n    \"rivera\": [\"step1-found.html\", \"step2-entry.html\", \"step3-charge.html\", \"step4-letter.html\"],\n    \"lib11\": [\"#\", \"#\", \"step3-count.html\", \"#\"],\n    \"c01\": [\"#\", \"step2-date.html\", \"#\", \"#\"],\n    \"lib01\": [\"step1-drafting-lib01.html\", \"#\", \"#\", \"#\"],\n    \"lib08\": [\"step1-failed.html\", \"#\", \"#\", \"#\"],\n    \"new\": [\"step1-add.html\", \"#\", \"#\", \"#\"],\n    \"practice\": [\"#\", \"#\", \"#\", \"step4-letter-practice.html\"],\n}\n\n\ndef head(title, body_class):\n    return f\"\"\"<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>{e(title)} · Treatment Timeline (mockup)</title>\n<link rel=\"stylesheet\" href=\"guided.css\">\n<script src=\"guided.js\" defer></script>\n</head>\n<body class=\"{body_class}\">\n<div class=\"banner\" role=\"note\"><span>{e(BANNER)}</span><span class=\"b-demo\">{e(DEMO)}</span></div>\n\"\"\"\n\n\ndef header(case_title=None, sub=None):\n    right = f'<span class=\"demo-pill\" title=\"{e(DEMO_NOTE)}\">{e(DEMO)}</span><button type=\"button\" class=\"theme-btn\" data-theme-btn>Dark mode</button>'\n    if case_title is None:\n        left = '<a class=\"brand\" href=\"index.html\"><span class=\"brand-mark\" aria-hidden=\"true\">TT</span><span>Treatment Timeline</span></a>'\n    else:\n        left = (f'<a class=\"back-cases\" href=\"index.html\"><span aria-hidden=\"true\">&#8249;</span> <span class=\"long\">Your</span>&nbsp;cases</a>'\n                f'<div style=\"min-width:0;display:flex;align-items:baseline;gap:12px\"><span class=\"case-title\">{e(case_title)}</span>'\n                + (f'<span class=\"case-sub\">{e(sub)}</span>' if sub else \"\") + \"</div>\")\n    return f'<header class=\"header\">{left}<span class=\"spacer\"></span>{right}</header>\\n'\n\n\ndef stepbar(case, states, here):\n    lis = []\n    for i, ((state, status), (long, short)) in enumerate(zip(states, LABELS)):\n        n = i + 1\n        cls = state + (\" current\" if n == here else \"\")\n        mark = \"&#10003;\" if state == \"done\" and n != here else (\"!\" if state == \"attn\" and n != here else str(n))\n        href = STEP_PAGES[case][i]\n        attrs = 'aria-current=\"step\"' if n == here else \"\"\n        tag = \"span\" if state == \"locked\" else \"a\"\n        link = \"\" if tag == \"span\" else f' href=\"{href}\"'\n        dis = ' aria-disabled=\"true\"' if state == \"locked\" else \"\"\n        lis.append(f'<li><{tag} class=\"step {cls}\"{link} {attrs}{dis}><span class=\"dot\" aria-hidden=\"true\">{mark}</span><span class=\"st-text\">'\n                   f'<span class=\"st-label\"><span class=\"long\">{n} {long}</span><span class=\"short\">{short}</span></span>'\n                   f'<span class=\"st-status\">{e(status)}</span></span><span class=\"sr\"> (step {n} of 4)</span></{tag}></li>')\n    return f'<nav class=\"steps\" aria-label=\"Steps\"><ol>{\"\".join(lis)}</ol></nav>\\n'\n\n\ndef footer(extra=\"\"):\n    return (f'<footer class=\"footer\"><span>{e(DEMO)}. {e(DEMO_NOTE)}</span>{extra}'\n            '<a href=\"screens.html\">Mockup: all screens</a></footer>\\n')\n\n\ndef rec_html(seq, rec, marks=(), sentences=None, show_head=True):\n    \"\"\"Record text as pasted (Date/Source/Excerpt lines), with marks on verbatim substrings or tappable sentences.\"\"\"\n    date, src, body = rec\n    lines = f'<span class=\"meta\">=== Record {seq} ===\\nDate: {e(date)}\\nSource: {e(src)}\\nExcerpt: </span>'\n    txt = e(f'\"{body}\"')\n    if sentences is not None:\n        out = '\"'\n        for s, on in sentences:\n            out += f'<span class=\"sent{\" on\" if on else \"\"}\">{e(s)}</span> '\n        txt = out.rstrip() + '\"'\n    else:\n        for m in marks:\n            txt = txt.replace(e(m), f\"<mark>{e(m)}</mark>\", 1)\n    for m in marks:     # header-line marks (gap evidence)\n        if m.startswith(\"Date:\") or m.startswith(\"Source:\"):\n            lines = lines.replace(e(m), f\"<mark>{e(m)}</mark>\", 1)\n    dl = long_date(date) if \"-\" in date else date\n    h = f'<div class=\"rec-h\">Record {seq} · {e(src)} · {e(dl)}</div>' if show_head else \"\"\n    return f'{h}<div class=\"rec\">{lines}{txt}</div>'\n\n\ndef frame(*, fname, title, case, case_title, sub, states, here, eyebrow, h1, count, answered, total, pct, source_head, source_body,\n          card_head, card_body, card_foot, foot_cls=\"\", question, yes, no, small, status=\"\", chip=None, extra_status=\"\"):\n    count_box = (f'<div class=\"count-box\"><div class=\"count-line\"><span class=\"num\">{e(count)}</span><span class=\"of num\">{answered} answered · {total} to go</span></div>'\n                 f'<div class=\"bar\" role=\"progressbar\" aria-label=\"Progress in this step\" aria-valuemin=\"0\" aria-valuemax=\"100\" aria-valuenow=\"{pct}\"><i style=\"width:{pct}%\"></i></div></div>')\n    chip_html = (f'<div class=\"total-chip\" aria-live=\"polite\"><div class=\"tc-l\">Bill total so far</div><div class=\"tc-v num\">{e(chip)}</div></div>' if chip else \"\")\n    html = head(title, \"frame\") + header(case_title, sub) + stepbar(case, states, here)\n    html += (f'<div class=\"titlebar\"><div class=\"t-main\"><div class=\"eyebrow\">{e(eyebrow)}</div><h1>{e(h1)}</h1>'\n             f'<div class=\"t-ai\">{e(AI_BANNER)}</div></div>{chip_html}{count_box}</div>\\n')\n    html += (f'<main class=\"work\" id=\"main\">'\n             f'<section class=\"card\" aria-label=\"From the record\"><div class=\"card-h\"><span class=\"ch-title\">From the record</span><span class=\"ch-sub\">{source_head}</span></div>'\n             f'<div class=\"card-b\" data-scroll-mark tabindex=\"0\">{source_body}</div></section>'\n             f'<section class=\"card\" aria-label=\"To check\"><div class=\"card-h\">{card_head}</div><div class=\"card-b\">{card_body}</div>'\n             f'<div class=\"card-f {foot_cls}\">{card_foot}</div></section></main>\\n')\n    html += (f'<div class=\"actions\"><div class=\"actions-in\"><p class=\"question\" id=\"q\">{e(question)}</p>'\n             f'<div class=\"big\" role=\"group\" aria-labelledby=\"q\">{yes}{no}</div><div class=\"small\">{small}</div>'\n             f'<p class=\"status\" role=\"status\" aria-live=\"polite\">{status}{extra_status}</p></div></div>\\n')\n    html += \"</body>\\n</html>\\n\"\n    (OUT / fname).write_text(html)\n\n\ndef A(label, href, cls=\"answer\", id_=None, disabled=False, sub=None):\n    i = f' id=\"{id_}\"' if id_ else \"\"\n    d = ' aria-disabled=\"true\" tabindex=\"-1\"' if disabled else \"\"\n    inner = e(label) + (f'<span class=\"sub\">{sub}</span>' if sub else \"\")\n    extra = \" two\" if sub else \"\"\n    return f'<a class=\"btn {cls}{extra}\" href=\"{href}\"{i}{d}>{inner}</a>'\n\n\ndef smalls(back=\"#\", third=None, later=\"#\"):\n    parts = [A(\"‹ Back\", back, \"quiet\")]\n    if third:\n        parts.append(A(third[0], third[1], \"quiet\", disabled=third[1] is None))\n    parts.append(A(\"Decide later\", later, \"quiet\"))\n    return \"\".join(parts)\n\n\ndef page(fname, title, body, *, case=None, case_title=None, sub=None, states=None, here=None, wide=False):\n    html = head(title, \"page\") + '<div class=\"stick\">' + header(case_title, sub)\n    if states:\n        html += stepbar(case, states, here)\n    html += f'</div><main class=\"wrap{\" wide\" if wide else \"\"}\" id=\"main\">{body}</main>' + footer() + \"</body>\\n</html>\\n\"\n    (OUT / fname).write_text(html)\n\n\n# ---------------------------------------------------------------- case step states\nRIV_S2 = [(\"done\", \"Done\"), (\"current\", \"16 of 19 left\"), (\"todo\", \"4 amounts\"), (\"todo\", \"Not yet\")]\nRIV_S2_LATE = lambda left: [(\"done\", \"Done\"), (\"current\", f\"{left} of 19 left\"), (\"todo\", \"4 amounts\"), (\"todo\", \"Not yet\")]\nRIV_S3 = lambda left: [(\"done\", \"Done\"), (\"done\", \"Done\"), (\"current\", f\"{left} of 4 left\" if left else \"Done\"), (\"todo\", \"Not yet\")]\nRIV_DONE = [(\"done\", \"Done\"), (\"done\", \"Done\"), (\"done\", \"Done\"), (\"done\", \"Ready\")]\nRIV_PENDING = [(\"done\", \"Done\"), (\"attn\", \"2 left\"), (\"attn\", \"1 left\"), (\"todo\", \"3 open\")]\nLIB11 = [(\"done\", \"Done\"), (\"done\", \"Done\"), (\"current\", \"7 of 8 left\"), (\"todo\", \"Not yet\")]\nC01 = [(\"done\", \"Done\"), (\"current\", \"1 of 10 left\"), (\"todo\", \"1 amount\"), (\"todo\", \"Not yet\")]\nNEW = [(\"current\", \"Now\"), (\"locked\", \"After step 1\"), (\"locked\", \"After step 1\"), (\"locked\", \"After step 1\")]\nFOUND = [(\"current\", \"9 records\"), (\"locked\", \"After step 1\"), (\"locked\", \"After step 1\"), (\"locked\", \"After step 1\")]\nDRAFT = [(\"current\", \"Drafting\"), (\"locked\", \"After step 1\"), (\"locked\", \"After step 1\"), (\"locked\", \"After step 1\")]\nFAILED = [(\"attn\", \"Run again\"), (\"todo\", \"Some ready\"), (\"todo\", \"Some ready\"), (\"locked\", \"After step 1\")]\n\nPREP = '<span class=\"tag prep\">Prepared answer</span>'\nWHY_OK = \"Quote found word for word, every number in the summary is in the quote, and the second check agreed.\"\n\n\ndef entry_head(tag, iso, src):\n    return f'{tag}<span class=\"ch-sub\">{e(long_date(iso))} · {e(src)}</span>'\n\n\ndef rhead(seq):\n    d, s, _ = RIVERA[seq]\n    return f\"Record {seq} · {e(s)} · {e(long_date(d))}\"\n\n\n# ================================================================ HOME\ndef card(title, meta, track, nxt, nxt_cls, btn, href, btn_label=\"Continue\"):\n    tr = \"\".join(f'<li class=\"{s}\"><i></i>{e(l)}</li>' for s, l in zip(track, [\"Add records\", \"Timeline\", \"Bills\", \"Letter\"]))\n    return (f'<article class=\"ccard\" data-title=\"{e(title)}\"><div class=\"cc-top\"><h3>{e(title)}</h3><button type=\"button\" class=\"btn quiet\">Rename</button></div>'\n            f'<div class=\"cc-meta\">{e(meta)}</div><ol class=\"track\" aria-label=\"Steps\">{tr}</ol>'\n            f'<p class=\"next {nxt_cls}\">{nxt}</p>'\n            f'<div class=\"cc-bottom\"><a class=\"btn lg {btn}\" href=\"{href}\">{e(btn_label)}</a><button type=\"button\" class=\"btn quiet danger\" data-delete>Delete</button></div>'\n            f'<div class=\"cc-bottom\" hidden><span style=\"flex:1;font-weight:600\">Delete this case and all its answers?</span><button type=\"button\" class=\"btn danger\">Yes, delete</button><button type=\"button\" class=\"btn\" data-keep>Keep it</button></div></article>')\n\n\ndef home():\n    cards_prog = [\n        card(\"Jordan Rivera (sample)\", \"Started Nov 2 · 9 records\", [\"done\", \"current\", \"\", \"\"], \"<b>Next:</b> Check the timeline. 16 of 19 items left.\", \"\", \"primary\", \"step2-entry.html\"),\n        card(\"Priors and ledger\", \"Started Nov 2 · 9 records\", [\"done\", \"done\", \"current\", \"\"], \"<b>Next:</b> Check the bills. 7 of 8 amounts left.\", \"\", \"primary\", \"step3-count.html\"),\n        card(\"Date formats\", \"Started Nov 2 · 8 records\", [\"done\", \"current\", \"\", \"\"], \"<b>Next:</b> Check the timeline. 1 item left: pick a date.\", \"\", \"primary\", \"step2-date.html\"),\n        card(\"Er only then gap\", \"Started Nov 2 · 6 records\", [\"current\", \"\", \"\", \"\"], \"<b>Next:</b> Wait while the timeline is drafted (stage 3 of 8).\", \"\", \"primary\", \"step1-drafting-lib01.html\"),\n        card(\"Second crash, MRI after\", \"Started Nov 2 · 7 records\", [\"attn\", \"\", \"\", \"\"], \"<b>Next:</b> Drafting stopped. Run it again.\", \"warn\", \"primary\", \"step1-failed.html\"),\n    ]\n    cards_done = [card(\"Sample case (practice run)\", \"Started Nov 1 · 9 records · finished Nov 1\", [\"done\", \"done\", \"done\", \"done\"],\n                       \"<b>Finished.</b> Your letter is ready.\", \"ok\", \"go\", \"step4-letter-practice.html\", \"Open letter\")]\n    body = ('<div class=\"home-h\"><div style=\"flex:1\"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'\n            '<a class=\"btn primary lg\" href=\"step1-add.html\">+ Start a new case</a></div>'\n            '<div class=\"find\"><label class=\"sr\" for=\"find-case\">Find a case</label><input id=\"find-case\" type=\"search\" placeholder=\"Find a case by name\"></div>'\n            f'<h2 class=\"sec-h\">In progress <span class=\"c\">{len(cards_prog)}</span></h2><div class=\"cases\">{\"\".join(cards_prog)}</div>'\n            f'<h2 class=\"sec-h\">Finished <span class=\"c\">{len(cards_done)}</span></h2><div class=\"cases\">{\"\".join(cards_done)}</div>')\n    page(\"index.html\", \"Your cases\", body, wide=True)\n\n    empty = ('<div class=\"home-h\"><div style=\"flex:1\"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div></div>'\n             '<div class=\"panel empty\"><div class=\"em-ic\" aria-hidden=\"true\">+</div><h2>You don\\'t have any cases yet.</h2>'\n             '<p>A case is one client\\'s medical records. We\\'ll guide you through 4 steps: add the records, check the timeline, check the bills, and get your letter.</p>'\n             '<div class=\"row-actions\"><a class=\"btn primary lg\" href=\"step1-add.html\">+ Start a new case</a><a class=\"btn lg\" href=\"step1-found.html\">Try the sample case</a></div></div>')\n    page(\"home-empty.html\", \"Your cases (empty)\", empty, wide=True)\n\n    sk = \"\".join('<article class=\"ccard\" aria-hidden=\"true\"><div class=\"skel\" style=\"height:28px;width:60%\"></div><div class=\"skel\" style=\"height:18px;width:40%\"></div>'\n                 '<div class=\"skel\" style=\"height:24px\"></div><div class=\"skel\" style=\"height:44px\"></div><div class=\"skel\" style=\"height:56px\"></div></article>' for _ in range(3))\n    loading = ('<div class=\"home-h\"><div style=\"flex:1\"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'\n               '<a class=\"btn primary lg\" href=\"step1-add.html\">+ Start a new case</a></div>'\n               f'<p class=\"sr\" role=\"status\">Loading your cases</p><h2 class=\"sec-h\">Loading your cases…</h2><div class=\"cases\">{sk}</div>')\n    page(\"home-loading.html\", \"Your cases (loading)\", loading, wide=True)\n\n    err = ('<div class=\"home-h\"><div style=\"flex:1\"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'\n           '<a class=\"btn primary lg\" href=\"step1-add.html\">+ Start a new case</a></div>'\n           '<div class=\"panel empty\"><div class=\"em-ic\" aria-hidden=\"true\" style=\"background:var(--bad-bg);color:var(--bad)\">!</div><h2>We couldn\\'t load your cases.</h2>'\n           '<p>The server didn\\'t answer. Your cases are safe; nothing was changed.</p><div class=\"row-actions\"><a class=\"btn primary lg\" href=\"index.html\">Try again</a></div></div>')\n    page(\"home-error.html\", \"Your cases (error)\", err, wide=True)\n\n\n# ================================================================ STEP 1\ndef step1():\n    body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 1 of 4</div><h1>Add records</h1>'\n            '<p>Add the medical records for this case. We\\'ll read them and draft a timeline for you to check.</p></div></div>'\n            '<div class=\"panel\"><div class=\"field\"><label for=\"case-name\">Name this case (optional)</label>'\n            '<input id=\"case-name\" value=\"Jordan Rivera (sample)\" maxlength=\"120\"><span class=\"hint\">For example the client\\'s name. You can change it later.</span></div>'\n            '<fieldset style=\"border:0;padding:0;margin:0\"><legend class=\"sr\">How do you want to add the records?</legend><div class=\"tiles\">'\n            '<label class=\"tile\"><input type=\"radio\" name=\"how\" value=\"paste\"><span class=\"tl-h\">Paste text</span><p>Copy the records and paste them here.</p></label>'\n            '<label class=\"tile\"><input type=\"radio\" name=\"how\" value=\"file\"><span class=\"tl-h\">Upload a file</span><p>A .txt or .pdf file, up to 5 MB.</p></label>'\n            '<label class=\"tile\"><input type=\"radio\" name=\"how\" value=\"sample\" checked><span class=\"tl-h\">Use the sample case</span><p>A short synthetic case to try it out.</p></label>'\n            '</div></fieldset>'\n            '<div class=\"input-box solid\"><div style=\"display:grid;place-items:center;text-align:center;gap:8px\"><b style=\"font-size:1.25rem\">The sample case</b>'\n            '<span class=\"muted\">9 short records from a fictional car-accident case (Jordan Rivera, 41, Austin). Every name and date in it is made up.</span></div></div>'\n            '<p class=\"err-slot\" role=\"alert\"></p>'\n            '<div class=\"row-actions\" style=\"margin-top:8px;align-items:center\"><a class=\"btn primary lg\" href=\"step1-found.html\">Read the records</a>'\n            '<span class=\"muted\">This demo can only read the sample and our test cases.</span></div></div>')\n    page(\"step1-add.html\", \"Add records\", body, case=\"new\", case_title=\"New case\", states=NEW, here=1)\n\n    rows = \"\".join(f'<li><span class=\"n\">{n}</span><span class=\"num\">{e(long_date(d))}</span><span class=\"src\">{e(s)}</span></li>' for n, (d, s, _) in RIVERA.items())\n    body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 1 of 4</div><h1>We found 9 records</h1>'\n            '<p>Check that these are the records you meant to add. Next, we\\'ll draft a one-line timeline entry for each one.</p></div></div>'\n            '<div class=\"panel fixed-box\"><div class=\"note-box ok\" style=\"margin-bottom:16px\"><span class=\"nb-text\">Every record has a date we could read.</span></div>'\n            f'<ol class=\"list\" style=\"max-height:440px\">{rows}</ol>'\n            '<div class=\"row-actions\"><a class=\"btn primary lg\" href=\"step1-drafting.html\">Draft the timeline</a><a class=\"btn lg\" href=\"step1-add.html\">Start over with other records</a></div></div>')\n    page(\"step1-found.html\", \"Records found\", body, case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=FOUND, here=1)\n\n    def drafting(fname, case, title, prepared, start, slow, sub, nxt, counts):\n        stg = [(\"Reading the records\", \"\"), (\"Loading the prepared line for each record\" if prepared else \"Writing one line for each record\", \"\"),\n               (\"Checking every quote word for word\", \"\"), (\"Double-checking each line a second way\", \"\"), (\"Finding the bill amounts\", \"\"),\n               (\"Comparing the records with each other\", \"\"), (\"Looking for things the attorney should know\", \"\"), (\"Putting it all together\", \"\")]\n        lis = \"\".join(f'<li class=\"{\"done\" if i < start else (\"now\" if i == start else \"\")}\"><span class=\"ic\" aria-hidden=\"true\">{\"&#10003;\" if i < start else \"\"}</span>{e(s)}</li>' for i, (s, _) in enumerate(stg))\n        body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 1 of 4</div><h1>Drafting the timeline</h1>'\n                '<p>This usually takes under a minute. You can leave this page; we\\'ll keep going.</p></div></div>'\n                f'<div class=\"panel fixed-box\"><div id=\"draft-running\"><div class=\"count-line\"><span>Working on it</span><span class=\"num\" id=\"draft-count\">{start + 1} of 8</span></div>'\n                f'<div class=\"bar\" role=\"progressbar\" aria-label=\"Drafting progress\"><i id=\"draft-bar\" style=\"width:{round(start / 8 * 100)}%\"></i></div>'\n                f'<ol class=\"stages\" id=\"stages\" data-start=\"{start}\"{\" data-slow\" if slow else \"\"} aria-live=\"polite\">{lis}</ol></div>'\n                f'<div id=\"draft-done\" hidden><div class=\"done-hero\"><div class=\"big-check\" aria-hidden=\"true\">&#10003;</div><div><h2>All set.</h2>'\n                f'<p>{e(counts)}</p></div></div><p class=\"muted\" style=\"margin-top:16px\">{e(AI_BANNER)}</p>'\n                f'<div class=\"row-actions\"><a class=\"btn primary lg\" href=\"{nxt}\">Go to step 2: Check the timeline</a></div></div></div>')\n        page(fname, \"Drafting\", body, case=case, case_title=title, sub=sub, states=DRAFT, here=1)\n\n    drafting(\"step1-drafting.html\", \"rivera\", \"Jordan Rivera (sample)\", True, 0, False, \"9 records\", \"step2-entry.html\",\n             \"19 timeline items and 4 bill amounts are ready for you to check.\")\n    drafting(\"step1-drafting-lib01.html\", \"lib01\", \"Er only then gap\", False, 2, True, \"6 records\", \"index.html\",\n             \"The timeline items and bill amounts are ready for you to check.\")\n\n    body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 1 of 4</div><h1>Drafting stopped</h1>'\n            '<p>Some of the work finished. You can run it again; nothing you decided is lost.</p></div></div>'\n            '<div class=\"panel fixed-box\"><div class=\"done-hero\"><div class=\"big-warn\" aria-hidden=\"true\">!</div><div><h2>Drafting stopped before it finished.</h2>'\n            '<p>The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.</p></div></div>'\n            '<div class=\"row-actions\"><a class=\"btn primary lg\" href=\"step1-drafting-lib01.html\">Run it again</a><a class=\"btn lg\" href=\"index.html\">Back to your cases</a></div>'\n            '<p class=\"muted\" style=\"margin-top:20px\">The items that did finish can be checked now in steps 2 and 3.</p></div>')\n    page(\"step1-failed.html\", \"Drafting stopped\", body, case=\"lib08\", case_title=\"Second crash, MRI after\", sub=\"7 records\", states=FAILED, here=1)\n\n\n# ================================================================ STEP 2\ndef step2():\n    small_entry = lambda back=\"#\", nxt=\"#\", fix=\"step2-fix.html\": smalls(back, (\"Fix the wording\", fix), nxt)\n    # --- entry, item 4 of 19\n    frame(fname=\"step2-entry.html\", title=\"Check the timeline\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2, here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 4 of 19\", answered=3, total=16, pct=16,\n          source_head=rhead(3), source_body=rec_html(3, RIVERA[3], [\"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.\"], show_head=False)\n          + '<div class=\"also\"><b>Also in this record, not in any line:</b><br><q>Patient reports low back pain in 2023, resolved.</q></div>',\n          card_head=entry_head(PREP, \"2026-01-16\", \"Dr. Alvarez, primary care\"),\n          card_body='<p class=\"line-text\">Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.</p>',\n          card_foot=f'<span class=\"label-cap\">How it was checked</span><br>{e(WHY_OK)}',\n          question=\"Does this line say the same thing as the highlighted words?\",\n          yes=A(\"Yes, this matches\", \"step2-flag.html\", \"answer primary\"), no=A(\"No, leave it out\", \"step2-flag.html\"),\n          small=small_entry(nxt=\"step2-flag.html\"),\n          status='<b>Saved:</b> item 3 (Central ER discharge summary) kept in the letter. <a href=\"#\">Undo</a>')\n\n    # --- fix the wording (with a refused edit shown)\n    sents = [(\"Persistent neck pain 6/10, daily headaches.\", True), (\"Refer to physical therapy 2x/week for 6 weeks.\", True), (\"Patient reports low back pain in 2023, resolved.\", False)]\n    frame(fname=\"step2-fix.html\", title=\"Fix the wording\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2, here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 4 of 19\", answered=3, total=16, pct=16,\n          source_head=rhead(3), source_body='<p class=\"muted\" style=\"margin-bottom:12px;font-size:1rem\">To change which words are highlighted, tap whole sentences below.</p>'\n          + rec_html(3, RIVERA[3], sentences=sents, show_head=False),\n          card_head='<span class=\"tag you\">Your wording</span><span class=\"ch-sub\">January 16, 2026 · Dr. Alvarez, primary care</span>',\n          card_body='<label class=\"sr\" for=\"fix\">Your wording for this line</label><textarea class=\"edit\" id=\"fix\">Persistent neck pain 7/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.</textarea>',\n          card_foot='<strong>Not saved.</strong> The summary says “7/10”, which the quote does not say. Remove it or change the quote.', foot_cls=\"bad\",\n          question=\"Change the line so it says only what the highlighted words say, then save it.\",\n          yes=A(\"Save my wording\", \"step2-entry.html\", \"answer primary\"), no=A(\"Cancel\", \"step2-entry.html\"),\n          small=smalls(\"#\", (\"Fix the wording\", None), \"#\"),\n          status=\"Numbers, left or right, and words like “no” or “possible” must match the highlighted words.\")\n\n    # --- prior-condition warning, item 5 of 19\n    frame(fname=\"step2-flag.html\", title=\"Warning for the attorney\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2_LATE(15), here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 5 of 19\", answered=4, total=15, pct=21,\n          source_head=rhead(3), source_body=rec_html(3, RIVERA[3], [\"Patient reports low back pain in 2023, resolved.\"], show_head=False),\n          card_head='<span class=\"tag warn\">Warning for the attorney</span>',\n          card_body='<p class=\"warn-title\">An earlier health problem is mentioned</p><p class=\"explain\"><b>Mention of a prior or pre-existing condition.</b> '\n                    'Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.”</p>',\n          card_foot=\"Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.\",\n          question=\"Should the attorney be told about this?\",\n          yes=A(\"Yes, tell the attorney\", \"step2-gap.html\", \"answer primary\"), no=A(\"No, not needed\", \"step2-gap.html\"),\n          small=smalls(\"step2-entry.html\", (\"Add a note\", \"#\"), \"step2-gap.html\"),\n          status='<b>Saved:</b> item 4 (Dr. Alvarez, primary care) kept in the letter. <a href=\"#\">Undo</a>')\n\n    # --- gap warning, item 10 of 19 (two records)\n    src = (rec_html(6, RIVERA[6], [\"Date: 2026-03-06\", \"Source: Capital PT, visit 9\"]) +\n           rec_html(7, RIVERA[7], [\"Date: 2026-05-18\", \"Source: Hill Country Pain Management, new patient\"]).replace('<div class=\"rec-h\">', '<div class=\"rec-h\" style=\"margin-top:24px;padding-top:20px;border-top:1px dashed var(--border)\">', 1))\n    frame(fname=\"step2-gap.html\", title=\"A break in treatment\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2_LATE(10), here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 10 of 19\", answered=9, total=10, pct=47,\n          source_head=\"Records 6 and 7\", source_body=src,\n          card_head='<span class=\"tag warn\">Warning for the attorney</span>',\n          card_body='<p class=\"warn-title\">A break in treatment</p><p class=\"explain\"><b>Gap of 73 days.</b> Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).</p>',\n          card_foot=\"Calculated by code from two dates read from the record headers. Warnings only go in the notes for the attorney, never in the letter.\",\n          question=\"Should the attorney be told about this?\",\n          yes=A(\"Yes, tell the attorney\", \"step2-disputed.html\", \"answer primary\"), no=A(\"No, not needed\", \"step2-disputed.html\"),\n          small=smalls(\"step2-flag.html\", (\"Add a note\", \"#\"), \"step2-disputed.html\"),\n          status='<b>Saved:</b> item 9 (Capital PT, visit 9) kept in the letter. <a href=\"#\">Undo</a>')\n\n    # --- disputed (D-066), item 15 of 19\n    frame(fname=\"step2-disputed.html\", title=\"Compare before you say yes\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2_LATE(5), here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 15 of 19\", answered=14, total=5, pct=74,\n          source_head=rhead(8), source_body=rec_html(8, RIVERA[8], [\"C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.\"], show_head=False),\n          card_head=entry_head(PREP, \"2026-05-29\", \"Austin Imaging, cervical MRI\"),\n          card_body='<p class=\"line-text\">C5-C6 disc herniation with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.</p>',\n          card_foot='<strong>The second check found this only partly supported by the quote.</strong> Read it against the highlighted words before you say yes.'\n                    '<label class=\"check\"><input type=\"checkbox\" data-unlocks=\"yes-disputed\"> I read this line against the highlighted words myself.</label>', foot_cls=\"attn\",\n          question=\"Does this line say the same thing as the highlighted words?\",\n          yes=A(\"Yes, this matches\", \"step2-done.html\", \"answer primary\", id_=\"yes-disputed\", disabled=True), no=A(\"No, leave it out\", \"step2-done.html\"),\n          small=small_entry(\"step2-gap.html\", \"step2-done.html\"),\n          status='<b>Saved:</b> item 14 (New-onset wording) — the attorney will be told. <a href=\"#\">Undo</a>')\n\n    # --- could not check (tray entry), optional\n    frame(fname=\"step2-cannot-check.html\", title=\"We couldn't check this one\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2_LATE(12), here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Optional item\", answered=7, total=12, pct=37,\n          source_head=rhead(5), source_body=rec_html(5, RIVERA[5], show_head=False),\n          card_head='<span class=\"tag warn\">We couldn\\'t check this one</span><span class=\"ch-sub\">February 20, 2026 · Capital PT, visit 8</span>',\n          card_body='<p class=\"explain\">The model\\'s quote does not appear word for word in the record, so it cannot be used.</p>'\n                    '<p class=\"explain muted\" style=\"margin-top:14px\">What was suggested (not used): “Visit 8: pain 4/10, improving.”<br>Its quote: “Pain is 4/10 and improving.”</p>',\n          card_foot=\"Nothing from this suggestion goes in the letter unless you write the line yourself. Skipping it leaves this record out of the timeline.\", foot_cls=\"attn\",\n          question=\"Read the record. Do you want to write this line yourself?\",\n          yes=A(\"Write it myself\", \"step2-write.html\", \"answer primary\"), no=A(\"Skip it\", \"step2-gap.html\"),\n          small=smalls(\"step2-flag.html\", None, \"step2-gap.html\"),\n          status='<b>Saved:</b> item 7 (The plan and what happened differ) — the attorney will be told. <a href=\"#\">Undo</a>')\n\n    # --- write it myself\n    frame(fname=\"step2-write.html\", title=\"Write the line yourself\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S2_LATE(12), here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Optional item\", answered=7, total=12, pct=37,\n          source_head=rhead(5), source_body='<p class=\"muted\" style=\"margin-bottom:12px;font-size:1rem\">Tap the sentences your line is based on. They become the highlighted words.</p>'\n          + rec_html(5, RIVERA[5], sentences=[(\"Pain 4/10, improving.\", True), (\"Patient reports missing 3 days of work.\", False)], show_head=False),\n          card_head='<span class=\"tag you\">Written by you</span><span class=\"ch-sub\">February 20, 2026 · Capital PT, visit 8</span>',\n          card_body='<label class=\"sr\" for=\"mine\">Your line for the timeline</label><textarea class=\"edit\" id=\"mine\">Pain 4/10, improving.</textarea>',\n          card_foot=\"Use only what the chosen sentences say. Numbers, left or right, and words like “no” or “possible” must match.\",\n          question=\"Write the line for the timeline, then save it.\",\n          yes=A(\"Save my line\", \"step2-gap.html\", \"answer primary\"), no=A(\"Cancel\", \"step2-cannot-check.html\"),\n          small=smalls(\"step2-cannot-check.html\", None, \"step2-gap.html\"))\n\n    # --- date to pick (Date formats case), item 10 of 10\n    frame(fname=\"step2-date.html\", title=\"Which date is right?\", case=\"c01\", case_title=\"Date formats\", sub=\"8 records\", states=C01, here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 10 of 10\", answered=9, total=1, pct=90,\n          source_head=\"Record 8 · Dr. Orla Pennywhistle, phone note · 04/05/2026\", source_body=rec_html(8, C01_R8, [\"Date: 04/05/2026\"], show_head=False),\n          card_head='<span class=\"tag warn\">Pick the date</span><span class=\"ch-sub\">Dr. Orla Pennywhistle, phone note</span>',\n          card_body='<p class=\"warn-title\">Which date is right?</p><p class=\"explain\">The record says <b>04/05/2026</b>. That could be two different dates.</p>'\n                    '<p class=\"explain muted\" style=\"margin-top:12px\">The line waiting for this date: “Patient reports no new symptoms.”</p>',\n          card_foot='<span class=\"label-cap\">Suggested: April 5, 2026</span><br>4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)',\n          question=\"Which date is right for this record?\",\n          yes=A(\"April 5, 2026\", \"step2-date-confirmed.html\", \"answer\", sub='month first <span class=\"chip-sug\">Suggested</span>'),\n          no=A(\"May 4, 2026\", \"step2-date-confirmed.html\", \"answer\", sub=\"day first\"),\n          small=smalls(\"#\", None, \"index.html\"))\n\n    frame(fname=\"step2-date-confirmed.html\", title=\"Check the line\", case=\"c01\", case_title=\"Date formats\", sub=\"8 records\", states=C01, here=2,\n          eyebrow=\"Step 2 of 4\", h1=\"Check the timeline\", count=\"Item 10 of 10\", answered=9, total=1, pct=90,\n          source_head=\"Record 8 · Dr. Orla Pennywhistle, phone note · April 5, 2026\", source_body=rec_html(8, C01_R8, [\"Patient reports no new symptoms.\"], show_head=False),\n          card_head='<span class=\"tag ai\">AI draft</span><span class=\"ch-sub\">April 5, 2026 · Dr. Orla Pennywhistle, phone note</span>',\n          card_body='<p class=\"line-text\">Patient reports no new symptoms.</p>',\n          card_foot='<span class=\"label-cap\">Part 2 of 2</span><br>The date is set. Now check the line itself.',\n          question=\"Does this line say the same thing as the highlighted words?\",\n          yes=A(\"Yes, this matches\", \"index.html\", \"answer primary\"), no=A(\"No, leave it out\", \"index.html\"),\n          small=smalls(\"step2-date.html\", (\"Fix the wording\", \"#\"), \"index.html\"),\n          status=\"<b>Saved:</b> record 8 is dated April 5, 2026 and now sits in the timeline.\")\n\n    # --- step 2 done\n    rows = [\n        (\"Jan 9, 2026\", \"Austin EMS run report\", \"Kept\"), (\"Jan 9, 2026\", \"The records disagree about the accident date\", \"Tell the attorney\"),\n        (\"Jan 9, 2026\", \"Central ER discharge summary\", \"Kept\"), (\"Jan 16, 2026\", \"Dr. Alvarez, primary care\", \"Kept\"),\n        (\"Jan 16, 2026\", \"An earlier health problem is mentioned\", \"Tell the attorney\"), (\"Jan 23, 2026\", \"Capital PT, initial evaluation\", \"Kept\"),\n        (\"Jan 23, 2026\", \"The plan and what happened differ\", \"Tell the attorney\"), (\"Feb 20, 2026\", \"Capital PT, visit 8\", \"Kept\"),\n        (\"Mar 6, 2026\", \"Capital PT, visit 9\", \"Kept\"), (\"Mar 6, 2026\", \"A break in treatment (73 days)\", \"Tell the attorney\"),\n        (\"Mar 6, 2026\", \"Missed or ended treatment\", \"Tell the attorney\"), (\"May 18, 2026\", \"Hill Country Pain Management, new patient\", \"Kept\"),\n        (\"May 18, 2026\", \"Where the accident date comes from\", \"Not needed\"), (\"May 18, 2026\", \"Wording about a new problem\", \"Tell the attorney\"),\n        (\"May 29, 2026\", \"Austin Imaging, cervical MRI\", \"Kept\"), (\"May 29, 2026\", \"Wording about wear and tear\", \"Tell the attorney\"),\n        (\"May 29, 2026\", \"Hedged wording (“may”, “possible”)\", \"Tell the attorney\"), (\"Jun 12, 2026\", \"Hill Country Pain Management, follow-up\", \"Kept\"),\n        (\"Jun 12, 2026\", \"The patient, not a doctor, says what caused it\", \"Tell the attorney\"),\n    ]\n    tagc = {\"Kept\": \"ok\", \"Tell the attorney\": \"warn\", \"Not needed\": \"never\"}\n    lis = \"\".join(f'<li><span class=\"n\">{i + 1}</span><span class=\"d\">{e(d)}</span><span class=\"lbl\">{e(l)}</span><span class=\"ans\"><span class=\"tag {tagc[a]}\">{e(a)}</span></span>'\n                  f'<a class=\"btn\" href=\"step2-entry.html\">Change</a></li>' for i, (d, l, a) in enumerate(rows))\n    body = ('<div class=\"panel\"><div class=\"done-hero\"><div class=\"big-check\" aria-hidden=\"true\">&#10003;</div><div><h2>You checked every item on the timeline.</h2>'\n            '<p>9 kept in the letter · 0 left out · 9 warnings for the attorney · 1 not needed</p></div></div>'\n            '<div class=\"row-actions\"><a class=\"btn primary lg\" href=\"step3-charge.html\">Go to step 3: Check the bills</a></div></div>'\n            f'<div class=\"panel\"><h2>Your answers</h2><p class=\"muted\">Every item in the order you saw it. Change any answer here.</p><ol class=\"answers\">{lis}</ol></div>'\n            '<div class=\"panel\"><h2>What we compared between records</h2><p><b>We checked for:</b> a stated plan of care against a course that ended early; a denial of prior problems against a prior condition; '\n            'a stated accident date against the record dates; the same clinician under two practice names.</p>'\n            '<p style=\"margin-top:8px\"><b>Not checked:</b> medication doses, left versus right across records, a diagnosis that differs between records, pain scores on the same day, plans measured in months, history reported by a relative.</p></div>')\n    page(\"step2-done.html\", \"Timeline checked\", '<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 2 of 4</div><h1>Check the timeline</h1></div></div>' + body,\n         case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S3(4), here=2)\n\n\n# ================================================================ STEP 3\ndef step3():\n    frame(fname=\"step3-charge.html\", title=\"Check the bills\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S3(4), here=3,\n          eyebrow=\"Step 3 of 4\", h1=\"Check the bills\", count=\"Amount 1 of 4\", answered=0, total=4, pct=0, chip=\"$0.00\",\n          source_head=rhead(2), source_body=rec_html(2, RIVERA[2], [\"ER charges: $6,240.\"], show_head=False),\n          card_head='<span class=\"tag ok\">Charge</span><span class=\"ch-sub\">Central ER discharge summary · January 9, 2026</span>',\n          card_body='<p class=\"money\">$6,240.00</p><p class=\"explain muted\" style=\"margin-top:6px\">Billed by Central ER on January 9, 2026.</p>',\n          card_foot=\"If you count it, it's added to the bill total in the letter, with the highlighted words as its source.\",\n          question=\"Should this charge count toward the bill total?\",\n          yes=A(\"Yes, count it\", \"step3-never.html\", \"answer primary\"), no=A(\"No, don't count it\", \"step3-never.html\"),\n          small=smalls(\"step2-done.html\", None, \"step3-never.html\"))\n\n    frame(fname=\"step3-never.html\", title=\"An amount that is never counted\", case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_S3(2), here=3,\n          eyebrow=\"Step 3 of 4\", h1=\"Check the bills\", count=\"Amount 3 of 4\", answered=2, total=2, pct=50, chip=\"$8,390.00\",\n          source_head=rhead(4), source_body=rec_html(4, RIVERA[4], [\"Charge per visit $185.\"], show_head=False),\n          card_head='<span class=\"tag never\">Never counted</span><span class=\"ch-sub\">Capital PT, initial evaluation · January 23, 2026</span>',\n          card_body='<p class=\"money\">$185</p><p class=\"explain\" style=\"margin-top:6px\">This figure is a rate, not a charge, so it is not added to the total.</p>',\n          card_foot=\"Either way, it is never added to the bill total. If you list it, the notes tell the attorney to request the itemized PT ledger.\",\n          question=\"This amount is never added to the total. List it in the notes for the attorney?\",\n          yes=A(\"Yes, list it\", \"step3-done.html\", \"answer primary\"), no=A(\"No, leave it out\", \"step3-done.html\"),\n          small=smalls(\"step3-charge.html\", None, \"step3-done.html\"),\n          status='<b>Saved:</b> $2,150.00 (Austin Imaging, cervical MRI) counted. <a href=\"#\">Undo</a>')\n\n    ledger_marks = [\"New patient exam charge $250.00\"]\n    frame(fname=\"step3-count.html\", title=\"Count this amount?\", case=\"lib11\", case_title=\"Priors and ledger\", sub=\"9 records\", states=LIB11, here=3,\n          eyebrow=\"Step 3 of 4\", h1=\"Check the bills\", count=\"Amount 2 of 8\", answered=1, total=7, pct=13, chip=\"$3,260.00\",\n          source_head=\"Record 9 · Fennimoor Spine Clinic, itemized ledger · June 15, 2026\", source_body=rec_html(9, LIB11_R9, ledger_marks, show_head=False),\n          card_head='<span class=\"tag warn\">Not counted yet</span><span class=\"ch-sub\">Fennimoor Spine Clinic, itemized ledger</span>',\n          card_body='<p class=\"money\">$250.00</p><p class=\"explain\" style=\"margin-top:6px\">The line states no date of service, so it is not an itemized service line and is not totaled.</p>',\n          card_foot='You can still count it if you checked the ledger yourself.<label class=\"check\"><input type=\"checkbox\" data-unlocks=\"yes-count\"> I checked this is a separate charge for a service.</label>',\n          foot_cls=\"attn\",\n          question=\"Should this amount count toward the bill total?\",\n          yes=A(\"Yes, count it\", \"index.html\", \"answer primary\", id_=\"yes-count\", disabled=True), no=A(\"No, don't count it\", \"index.html\"),\n          small=smalls(\"#\", None, \"index.html\"),\n          status='<b>Saved:</b> $3,260.00 (Wexcombe Memorial ED) counted. <a href=\"#\">Undo</a>')\n\n    body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 3 of 4</div><h1>Check the bills</h1></div></div>'\n            '<div class=\"panel\"><div class=\"done-hero\"><div class=\"big-check\" aria-hidden=\"true\">&#10003;</div><div><h2>You checked every bill amount.</h2>'\n            '<p>This is the total line your letter will carry:</p></div></div>'\n            '<p class=\"total-line num\">Billed charges accepted from these records: $8,390.00</p>'\n            '<div class=\"row-actions\"><a class=\"btn primary lg\" href=\"step4-letter.html\">Go to step 4: Get your letter</a></div></div>'\n            '<div class=\"panel\"><h2>Counted (2)</h2><table class=\"mini\"><thead><tr><th>Amount</th><th>From</th><th>Date</th><th></th></tr></thead><tbody>'\n            '<tr><td class=\"amt\">$6,240.00</td><td>Central ER discharge summary</td><td>January 9, 2026</td><td><a class=\"btn\" href=\"step3-charge.html\">Change</a></td></tr>'\n            '<tr><td class=\"amt\">$2,150.00</td><td>Austin Imaging, cervical MRI</td><td>May 29, 2026</td><td><a class=\"btn\" href=\"step3-charge.html\">Change</a></td></tr></tbody></table></div>'\n            '<div class=\"panel\"><h2>Not counted by you (0)</h2><p class=\"muted\">You didn\\'t leave out any charge.</p></div>'\n            '<div class=\"panel\"><h2>Never counted (2)</h2><p class=\"muted\">These are never added to the total. The ones you listed go in the notes for the attorney.</p>'\n            '<table class=\"mini\" style=\"margin-top:8px\"><thead><tr><th>Amount</th><th>From</th><th>Why it\\'s never counted</th></tr></thead><tbody>'\n            '<tr><td class=\"amt\">$185</td><td>Capital PT, initial evaluation</td><td>This figure is a rate, not a charge, so it is not added to the total.</td></tr>'\n            '<tr><td class=\"amt\">missing 3 days of work</td><td>Capital PT, visit 8</td><td>This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.</td></tr></tbody></table></div>')\n    page(\"step3-done.html\", \"Bills checked\", body, case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\", states=RIV_DONE[:3] + [(\"todo\", \"Ready\")], here=3)\n\n\n# ================================================================ STEP 4\ndef golden():\n    txt = (OUT.parents[2] / \"evals/golden/sample.export.expected.txt\").read_text()\n    letter = txt.split(\"=== LETTER_TEXT (block 1: paste into letter) ===\\n\")[1].split(\"=== INTERNAL_NOTES_TEXT\")[0].rstrip(\"\\n\")\n    notes = txt.split(\"=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\\n\")[1].rstrip(\"\\n\")\n    return letter, notes\n\n\ndef step4():\n    letter, notes = golden()\n\n    def letter_page(fname, case, title, states, top, copy_lock, notes_txt):\n        lock = ' aria-disabled=\"true\" tabindex=\"-1\"' if copy_lock else \"\"\n        body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 4 of 4</div><h1>Get your letter</h1>'\n                '<p>Copy the treatment section into your demand letter, or download it. The notes on the right are for the attorney only.</p></div></div>'\n                f'{top}<div class=\"letter-grid\" style=\"margin-top:20px\"><section><div class=\"doc-h\"><h2>Your letter section</h2><span class=\"muted\">Paste into the demand letter</span></div>'\n                f'<pre class=\"doc\" id=\"letter\" tabindex=\"0\">{e(letter)}</pre>'\n                f'<div class=\"doc-actions\"><button type=\"button\" class=\"btn primary lg\" data-copy=\"letter\" id=\"copy-letter\"{lock}>Copy letter</button>'\n                f'<button type=\"button\" class=\"btn lg\" data-download=\"letter\" data-name=\"jordan-rivera-letter.txt\" id=\"dl-letter\"{lock}>Download letter (.txt)</button></div></section>'\n                '<section><div class=\"doc-h\"><h2>Notes for the attorney</h2><span class=\"muted\" style=\"color:var(--bad);font-weight:700\">Do not send</span></div>'\n                f'<pre class=\"doc notes\" id=\"notes\" tabindex=\"0\">{e(notes_txt)}</pre>'\n                f'<div class=\"doc-actions\"><button type=\"button\" class=\"btn lg\" data-copy=\"notes\"{lock}>Copy notes</button>'\n                f'<button type=\"button\" class=\"btn lg\" data-download=\"notes\" data-name=\"jordan-rivera-notes.txt\"{lock}>Download notes</button></div></section></div>'\n                '<div class=\"panel\" style=\"margin-top:24px\"><h2>Exhibit and page numbers (optional)</h2><p class=\"muted\">Fill these in to replace “[Ex. __ / Bates __]” in every source line.</p>'\n                '<div class=\"cfg\"><div class=\"field\"><label for=\"ex\">Exhibit</label><input id=\"ex\" placeholder=\"e.g. 4\"></div>'\n                '<div class=\"field\"><label for=\"bp\">Bates prefix</label><input id=\"bp\" placeholder=\"e.g. RIV\"></div>'\n                '<div class=\"field\"><label for=\"bs\">First number</label><input id=\"bs\" inputmode=\"numeric\" placeholder=\"e.g. 1\"></div>'\n                '<button type=\"button\" class=\"btn lg\">Save numbers</button></div></div>')\n        page(fname, \"Get your letter\", body, case=case, case_title=title, sub=\"9 records\", states=states, here=4, wide=True)\n\n    ready = ('<div class=\"note-box ok\"><span class=\"nb-text\">Your letter is ready. Every item has an answer.'\n             '<span>9 timeline lines and 2 charges are in it. Nothing is left undecided.</span></span></div>')\n    letter_page(\"step4-letter.html\", \"rivera\", \"Jordan Rivera (sample)\", RIV_DONE, ready, False, notes)\n    letter_page(\"step4-letter-practice.html\", \"practice\", \"Sample case (practice run)\", RIV_DONE, ready, False, notes)\n\n    pending_notes = notes.replace(\"Items not reviewed: 0.\", \"Items not reviewed: 3.\")\n    pend = ('<div class=\"note-box\"><span class=\"nb-text\">3 items still need a decision.<span>If you don\\'t decide them, they stay out of the letter. The letter below is what would be sent now.</span></span>'\n            '<a class=\"btn primary lg\" href=\"step2-flag.html\">Go to the first one</a></div>'\n            '<label class=\"check\" style=\"margin-top:14px\"><input type=\"checkbox\" data-unlocks=\"copy-letter dl-letter\"> Copy it anyway, without those 3 items.</label>')\n    letter_page(\"step4-pending.html\", \"rivera\", \"Jordan Rivera (sample)\", RIV_PENDING, pend, True, pending_notes)\n\n    body = ('<div class=\"page-h\"><div class=\"ph-main\"><div class=\"eyebrow\">Step 4 of 4</div><h1>Get your letter</h1>'\n            '<p>Copy the treatment section into your demand letter, or download it.</p></div></div>'\n            '<div class=\"note-box bad\"><span class=\"nb-text\">The letter can\\'t be made yet.<span>Fix the problem below, then come back here.</span></span></div>'\n            '<ul class=\"blockers\"><li><span>Nothing is accepted or edited yet, so the letter would be empty.</span><a class=\"btn primary\" href=\"step2-entry.html\">Go to step 2</a></li></ul>'\n            '<div class=\"letter-grid\" style=\"margin-top:20px\"><section><div class=\"doc-h\"><h2>Your letter section</h2></div>'\n            '<div class=\"doc placeholder\">Your letter will appear here once the problem above is fixed.</div>'\n            '<div class=\"doc-actions\"><button type=\"button\" class=\"btn primary lg\" aria-disabled=\"true\" tabindex=\"-1\">Copy letter</button><button type=\"button\" class=\"btn lg\" aria-disabled=\"true\" tabindex=\"-1\">Download letter (.txt)</button></div></section>'\n            '<section><div class=\"doc-h\"><h2>Notes for the attorney</h2></div><div class=\"doc notes placeholder\">The notes appear with the letter.</div></section></div>')\n    page(\"step4-blocked.html\", \"Letter blocked\", body, case=\"rivera\", case_title=\"Jordan Rivera (sample)\", sub=\"9 records\",\n         states=[(\"done\", \"Done\"), (\"attn\", \"19 of 19 left\"), (\"attn\", \"4 of 4 left\"), (\"attn\", \"1 problem\")], here=4, wide=True)\n\n\n# ================================================================ SCREENS INDEX\ndef screens():\n    groups = [\n        (\"Your cases\", [(\"index.html\", \"Your cases\", \"Six synthetic cases at different steps, each with one Continue button.\"),\n                        (\"home-empty.html\", \"No cases yet\", \"Empty state with Start a new case and Try the sample case.\"),\n                        (\"home-loading.html\", \"Loading\", \"Skeleton cards of the final size.\"),\n                        (\"home-error.html\", \"Couldn't load\", \"Error state with Try again.\")]),\n        (\"Step 1 · Add records\", [(\"step1-add.html\", \"Add records\", \"Name, three ways in (paste, upload, sample), Read the records.\"),\n                                  (\"step1-found.html\", \"Records found\", \"The 9 sample records; Draft the timeline.\"),\n                                  (\"step1-drafting.html\", \"Drafting\", \"Plain-words stage list (prepared answers); turns into All set.\"),\n                                  (\"step1-drafting-lib01.html\", \"Drafting, another case\", \"Live/recorded wording, mid-run.\"),\n                                  (\"step1-failed.html\", \"Drafting stopped\", \"Interrupted run, Run it again.\")]),\n        (\"Step 2 · Check the timeline\", [(\"step2-entry.html\", \"A timeline line\", \"Item 4 of 19: quote beside the line, Yes / No.\"),\n                                         (\"step2-fix.html\", \"Fix the wording\", \"Same boxes; a refused edit shows the server's reason.\"),\n                                         (\"step2-flag.html\", \"A warning\", \"Item 5: an earlier health problem; tell the attorney?\"),\n                                         (\"step2-gap.html\", \"A break in treatment\", \"Item 10: evidence in two records.\"),\n                                         (\"step2-disputed.html\", \"Compare first (D-066)\", \"State variant: Yes unlocks only after the compare box.\"),\n                                         (\"step2-cannot-check.html\", \"We couldn't check this one\", \"State variant (api.md tray example): write it or skip.\"),\n                                         (\"step2-write.html\", \"Write it myself\", \"Tap sentences, type the line.\"),\n                                         (\"step2-date.html\", \"Pick a date\", \"Date formats case: two big date answers, suggestion shown.\"),\n                                         (\"step2-date-confirmed.html\", \"Date set, now the line\", \"Part 2 of the same item.\"),\n                                         (\"step2-done.html\", \"Timeline done\", \"Counts, every answer with Change, what was compared.\")]),\n        (\"Step 3 · Check the bills\", [(\"step3-charge.html\", \"A charge\", \"$6,240.00: count it?\"),\n                                      (\"step3-count.html\", \"Count with a check (D-064)\", \"Priors and ledger: $250.00, named confirm.\"),\n                                      (\"step3-never.html\", \"Never counted\", \"$185 rate: list it for the attorney?\"),\n                                      (\"step3-done.html\", \"Bills done\", \"The letter's total line and three plain lists.\")]),\n        (\"Step 4 · Get your letter\", [(\"step4-letter.html\", \"Letter ready\", \"Golden letter and notes; Copy and Download.\"),\n                                      (\"step4-pending.html\", \"3 items undecided\", \"State variant: go to the first one, or copy anyway.\"),\n                                      (\"step4-blocked.html\", \"Blocked\", \"Nothing accepted yet: the real server reason, Go to step 2.\")]),\n    ]\n    body = ('<div class=\"page-h\"><div class=\"ph-main\"><h1>Guided UI mockup: all screens</h1>'\n            '<p>Static mockup for T-180 (D-068). No backend: buttons move between these pages. Content is the synthetic Appendix A sample and two synthetic library cases, '\n            'taken from a fixture run of the real API. Spec: docs/GUIDED_UI_SPEC.md.</p></div></div>')\n    for g, items in groups:\n        body += f'<h2 class=\"sec-h\">{e(g)}</h2><div class=\"screens\">' + \"\".join(\n            f'<a href=\"{h}\"><b>{e(t)}</b><span>{e(d)}</span>{\"<div class=variant>State variant</div>\" if \"variant\" in d else \"\"}</a>' for h, t, d in items) + \"</div>\"\n    page(\"screens.html\", \"All screens\", body, wide=True)\n\n\nif __name__ == \"__main__\":\n    home(); step1(); step2(); step3(); step4(); screens()\n    print(\"wrote\", len(list(OUT.glob(\"*.html\"))), \"pages to\", OUT)\n"
}
````

### User / tool · 2026-11-02T20:49:08.530Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/mockups/guided/build.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:15.368Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/mark = \"&#10003;\" if state == \"done\" and n != here else/mark = \"\\&#10003;\" if state == \"done\" else/' artifacts/mockups/guided/build.py && grep -n 'mark = ' artifacts/mockups/guided/build.py && python3 artifacts/mockups/guided/build.py && ls artifacts/mockups/guided/",
 "description": "Fix step mark and build mockup pages"
}
````

### User / tool · 2026-11-02T20:49:15.651Z

**tool result**
````
82:        mark = "&#10003;" if state == "done" else ("!" if state == "attn" and n != here else str(n))
wrote 28 pages to /Users/arsis/zlayt-pm-project/artifacts/mockups/guided
build.py
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
[This command modified 1 file you've previously read: artifacts/mockups/guided/build.py. Call Read before editing.]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:16.803Z

Now a Playwright pass: screenshots at both widths, plus a quick visual review.

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:23.790Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/shoot.py <<'EOF'\nimport sys\nfrom pathlib import Path\nfrom playwright.sync_api import sync_playwright\nroot = Path(\"/Users/arsis/zlayt-pm-project/artifacts/mockups/guided\")\nout = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)\npages = sys.argv[2].split(\",\")\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in [(1440, 900), (390, 844)]:\n        ctx = b.new_context(viewport={\"width\": w, \"height\": h}, device_scale_factor=1)\n        pg = ctx.new_page()\n        errs = []\n        pg.on(\"console\", lambda m: errs.append(m.text) if m.type == \"error\" else None)\n        pg.on(\"pageerror\", lambda ex: errs.append(str(ex)))\n        for name in pages:\n            pg.goto((root / f\"{name}.html\").as_uri()); pg.wait_for_timeout(250)\n            sw = pg.evaluate(\"document.documentElement.scrollWidth\")\n            if sw > w: print(\"OVERFLOW\", name, w, sw)\n            pg.screenshot(path=str(out / f\"{name}-{w}.png\"), full_page=False)\n        if errs: print(\"ERRORS\", w, errs)\n        ctx.close()\n    b.close()\nEOF\n.venv/bin/python $S/shoot.py $S/shots index,step2-entry,step2-flag,step3-count,step4-letter,step1-add && ls $S/shots | wc -l",
 "description": "Take draft screenshots for visual review"
}
````

### User / tool · 2026-11-02T20:49:28.069Z

**tool result**
````
OVERFLOW index 390 409
OVERFLOW step3-count 390 476
      12
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:31.473Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step2-entry-1440.png"
}
````

### User / tool · 2026-11-02T20:49:31.488Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:38.184Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step2-entry-390.png"
}
````

### User / tool · 2026-11-02T20:49:38.193Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:49:58.415Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/wide.py <<'EOF'\nimport sys\nfrom pathlib import Path\nfrom playwright.sync_api import sync_playwright\nroot = Path(\"/Users/arsis/zlayt-pm-project/artifacts/mockups/guided\")\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 390, \"height\": 844})\n    for n in sys.argv[1].split(\",\"):\n        pg.goto((root / f\"{n}.html\").as_uri())\n        print(n, pg.evaluate(\"\"\"() => [...document.querySelectorAll('body *')].filter(el => el.getBoundingClientRect().right > 391).slice(0,6).map(el => el.tagName+'.'+el.className+' '+Math.round(el.getBoundingClientRect().right))\"\"\"))\n    b.close()\nEOF\n.venv/bin/python $S/wide.py index,step3-count",
 "description": "Find elements overflowing at 390"
}
````

### User / tool · 2026-11-02T20:49:59.054Z

**tool result**
````
index ['ARTICLE.ccard 409']
step3-count ['DIV.banner 476', 'HEADER.header 476', 'SPAN.spacer 408', 'BUTTON.theme-btn 460', 'NAV.steps 476', 'OL. 468']
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:50:21.002Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nrep = [\n (\"--banner-h: 32px; --header-h: 64px; --steps-h: 76px; --title-h: 76px;\", \"--banner-h: 32px; --header-h: 64px; --steps-h: 76px; --title-h: 104px;\"),\n (\"body.frame { height: 100vh; height: 100dvh; overflow: hidden; display: grid; grid-template-rows:\",\n  \"html:has(> body.frame) { overflow: hidden; scrollbar-gutter: auto; }\\nbody.frame { height: 100vh; height: 100dvh; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1fr); grid-template-rows:\"),\n (\".titlebar { display: flex; align-items: center; gap: 24px; padding: 0 var(--gutter);\", \".titlebar { display: flex; align-items: center; gap: 24px; padding: 0 var(--gutter) 8px;\"),\n (\".titlebar .t-ai { font-size: .9375rem;\", \".titlebar .t-ai { margin-top: 2px; font-size: .9375rem;\"),\n (\"  :root { --gutter: 16px; --banner-h: 44px; --header-h: 56px; --steps-h: 62px; --title-h: 58px; }\",\n  \"  :root { --gutter: 16px; --banner-h: 44px; --header-h: 52px; --steps-h: 66px; --title-h: 48px; }\"),\n (\"  .step { flex-direction: column; justify-content: center; gap: 3px; padding: 0 2px; text-align: center; }\",\n  \"  .step { flex-direction: column; justify-content: center; gap: 2px; padding: 0 2px 6px; text-align: center; }\"),\n (\"  .step .dot { width: 26px; height: 26px; font-size: .8125rem; }\", \"  .step .dot { width: 24px; height: 24px; font-size: .75rem; border-width: 2px; }\"),\n (\"  .work { grid-template-columns: 1fr; grid-template-rows: minmax(0, 1fr) 196px; gap: 10px; padding-bottom: 10px; }\",\n  \"  .work { grid-template-columns: minmax(0, 1fr); grid-template-rows: minmax(0, 1fr) 236px; gap: 8px; padding-bottom: 8px; }\\n  .card-src .card-h .ch-title { display: none; }\\n  .card-f .label-cap { display: none; }\\n  .card-f.plain { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }\"),\n (\"  .titlebar { gap: 12px; }\", \"  .titlebar { gap: 12px; padding-bottom: 4px; }\"),\n (\"  .cases { grid-template-columns: 1fr; }\", \"  .cases { grid-template-columns: minmax(0, 1fr); }\"),\n (\".back-cases:hover { background: var(--sunken); }\", \".back-cases:hover { background: var(--sunken); }\\n.back-cases .short { display: none; }\"),\n (\"  .back-cases .long { display: none; }\", \"  .back-cases .long { display: none; }\\n  .back-cases .short { display: inline; }\"),\n (\"  .question { font-size: 1.0625rem; line-height: 1.4rem; min-height: 2.8rem; display: flex; align-items: center; }\",\n  \"  .question { font-size: 1rem; line-height: 1.35rem; min-height: 2.7rem; display: flex; align-items: center; }\"),\n (\"  .actions-in { grid-template-columns: 1fr; grid-template-areas: \\\"q\\\" \\\"big\\\" \\\"small\\\" \\\"status\\\"; padding: 10px 16px 8px; row-gap: 8px; }\",\n  \"  .actions-in { grid-template-columns: minmax(0, 1fr); grid-template-areas: \\\"q\\\" \\\"big\\\" \\\"small\\\" \\\"status\\\"; padding: 8px 16px 6px; row-gap: 6px; }\"),\n (\"  .small .btn { height: 44px; font-size: .9375rem; padding: 0 8px; }\", \"  .small .btn { height: 40px; font-size: .9375rem; padding: 0 8px; }\"),\n]\nfor a, b in rep:\n    assert a in c, a\n    c = c.replace(a, b)\np.write_text(c)\nb = Path(\"build.py\"); s = b.read_text()\nrep2 = [\n (\"\"\"<a class=\"back-cases\" href=\"index.html\"><span aria-hidden=\"true\">&#8249;</span> <span class=\"long\">Your</span>&nbsp;cases</a>\"\"\",\n  \"\"\"<a class=\"back-cases\" href=\"index.html\"><span aria-hidden=\"true\">&#8249;</span><span class=\"long\">Your cases</span><span class=\"short\">Cases</span></a>\"\"\"),\n (\"\"\"f'<section class=\"card\" aria-label=\"From the record\">\"\"\", \"\"\"f'<section class=\"card card-src\" aria-label=\"From the record\">\"\"\"),\n (\"\"\"f'<div class=\"card-f {foot_cls}\">{card_foot}</div></section></main>\\\\n')\"\"\", \"\"\"f'<div class=\"card-f {foot_cls or \"plain\"}\">{card_foot}</div></section></main>\\\\n')\"\"\"),\n]\nfor a, b2 in rep2:\n    assert a in s, a\n    s = s.replace(a, b2)\nb.write_text(s)\nEOF\npython3 build.py && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd /Users/arsis/zlayt-pm-project && .venv/bin/python $S/shoot.py $S/shots index,step2-entry,step2-disputed,step3-count,step4-letter,step1-add,step2-done,step2-date",
 "description": "Apply layout fixes, rebuild, reshoot"
}
````

### User / tool · 2026-11-02T20:50:26.408Z

**tool result**
````
wrote 28 pages to /Users/arsis/zlayt-pm-project/artifacts/mockups/guided
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:50:30.336Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step2-disputed-390.png"
}
````

### User / tool · 2026-11-02T20:50:30.345Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:50:33.325Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step2-disputed-1440.png"
}
````

### User / tool · 2026-11-02T20:50:33.334Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:50:41.010Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/index-1440.png"
}
````

### User / tool · 2026-11-02T20:50:41.019Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:50:44.105Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/index-390.png"
}
````

### User / tool · 2026-11-02T20:50:44.114Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:50:47.237Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step2-date-390.png"
}
````

### User / tool · 2026-11-02T20:50:47.245Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:01.144Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nrep = [\n (\"* { box-sizing: border-box; }\", \"* { box-sizing: border-box; }\\n[hidden] { display: none !important; }\"),\n (\".btn.answer .sub { display: block; font-size: .875rem; font-weight: 500; opacity: .85; }\", \".btn.answer .sub { display: block; font-size: .875rem; font-weight: 500; white-space: nowrap; }\"),\n (\".chip-sug { display: inline-block; margin-left: 8px; padding: 2px 8px;\", \".chip-sug { display: inline-block; margin-left: 6px; padding: 0 7px; line-height: 1.25rem;\"),\n (\"grid-template-rows: minmax(0, 1fr) 236px;\", \"grid-template-rows: minmax(0, 1fr) 256px;\"),\n]\nfor a, b in rep:\n    assert a in c, a\n    c = c.replace(a, b)\np.write_text(c)\nEOF\npython3 build.py >/dev/null && cd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python $S/shoot.py $S/shots index,step2-date,step4-letter,step1-add,step2-done,step3-count,step2-gap,step1-drafting",
 "description": "Fix hidden rows and date chip, reshoot"
}
````

### User / tool · 2026-11-02T20:51:06.522Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:10.176Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/index-1440.png"
}
````

### User / tool · 2026-11-02T20:51:10.185Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:13.519Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step4-letter-1440.png"
}
````

### User / tool · 2026-11-02T20:51:13.528Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:16.965Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step3-count-390.png"
}
````

### User / tool · 2026-11-02T20:51:16.977Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:33.781Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nrep = [\n (\".ccard { height: 244px;\", \".ccard { min-height: 244px;\"),\n (\"  .ccard { height: 252px; padding: 18px; }\", \"  .ccard { min-height: 0; padding: 18px; }\"),\n (\".ccard .cc-top { display: flex; gap: 12px; align-items: flex-start; }\", \".ccard .cc-top { display: flex; gap: 12px; align-items: center; }\\n.ccard .cc-top .btn { height: 36px; }\"),\n (\".doc { background: var(--paper);\", \".doc { margin: 0; font-family: var(--font); background: var(--paper);\"),\n (\"  .total-chip { width: 148px; padding: 6px 10px; }\", \"  .titlebar:has(.total-chip) .t-main { display: none; }\\n  .total-chip { flex: 1; width: auto; padding: 4px 10px; display: flex; align-items: baseline; justify-content: space-between; gap: 8px; box-shadow: none; }\"),\n]\nfor a, b in rep:\n    assert a in c, a\n    c = c.replace(a, b)\np.write_text(c)\nEOF\npython3 build.py >/dev/null && cd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python $S/shoot.py $S/shots index,step3-count,step1-add,step2-done,step2-gap,step1-drafting,step4-pending,step3-done",
 "description": "Fix home card, letter font, mobile chip; reshoot"
}
````

### User / tool · 2026-11-02T20:51:39.054Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:42.792Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/index-390.png"
}
````

### User / tool · 2026-11-02T20:51:42.802Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:46.137Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step2-gap-1440.png"
}
````

### User / tool · 2026-11-02T20:51:46.145Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:51:49.201Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots/step1-add-1440.png"
}
````

### User / tool · 2026-11-02T20:51:49.213Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:52:00.155Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nrep = [\n (\".tile:has(input:checked) .tl-h::before { border: 7px solid var(--accent); }\", \".tile:has(input:checked) .tl-h::before { border-color: var(--accent); background: var(--accent); box-shadow: inset 0 0 0 4px var(--panel); }\"),\n (\".card-b { flex: 1; min-height: 0; overflow: auto; padding: 20px 24px; }\", \".card-b { position: relative; flex: 1; min-height: 0; overflow: auto; padding: 20px 24px; }\"),\n]\nfor a, b in rep:\n    assert a in c, a\n    c = c.replace(a, b)\np.write_text(c)\nj = Path(\"guided.js\"); s = j.read_text()\na = \"var m = body.querySelector(\\\"mark\\\"); if (m) body.scrollTop = Math.max(0, m.offsetTop - body.offsetTop - 24);\"\nassert a in s\ns = s.replace(a, \"var m = body.querySelector(\\\"mark\\\"); if (m && m.offsetTop + m.offsetHeight > body.clientHeight - 16) body.scrollTop = Math.max(0, m.offsetTop - 72);\")\nj.write_text(s)\nb = Path(\"build.py\"); t = b.read_text()\na = \"\"\"'<div class=\"input-box solid\"><div style=\"display:grid;place-items:center;text-align:center;gap:8px\">\"\"\"\nassert a in t\nt = t.replace(a, \"\"\"'<div class=\"input-box solid\"><div style=\"display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;height:100%\">\"\"\")\nb.write_text(t)\nEOF\npython3 build.py",
 "description": "Fix radio size change, scroll offset, sample box"
}
````

### User / tool · 2026-11-02T20:52:00.303Z

**tool result**
````
wrote 28 pages to /Users/arsis/zlayt-pm-project/artifacts/mockups/guided
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:52:01.489Z

Now a layout-stability test: click every in-page control and assert nothing moved, at both widths.

### Assistant · claude-opus-5-5 · 2026-11-02T20:52:11.922Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/stable.py <<'EOF'\nfrom pathlib import Path\nfrom playwright.sync_api import sync_playwright\nroot = Path(\"/Users/arsis/zlayt-pm-project/artifacts/mockups/guided\")\nBOX = \"\"\"() => [...document.querySelectorAll('.steps .step, .btn, .question, .card, .card-f, .tile, .input-box, .count-box, .total-chip, .status')].map(el => {const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(',')})\"\"\"\nfails = 0\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in [(1440, 900), (390, 844), (320, 640)]:\n        pg = b.new_page(viewport={\"width\": w, \"height\": h}); errs = []\n        pg.on(\"pageerror\", lambda ex: errs.append(str(ex)))\n        for f in sorted(root.glob(\"*.html\")):\n            pg.goto(f.as_uri()); pg.wait_for_timeout(150)\n            sw = pg.evaluate(\"document.documentElement.scrollWidth\")\n            if sw > w: print(\"OVERFLOW\", f.name, w, sw); fails += 1\n            bad = pg.evaluate(\"() => document.querySelectorAll('details, [role=menu], [role=menubar]').length\")\n            if bad: print(\"HIDDEN-UI\", f.name, bad); fails += 1\n            # every in-page control: checkboxes, tiles, tappable sentences, theme\n            ctrls = pg.locator(\"input[type=checkbox], .tile input, .sent, [data-theme-btn]\")\n            for i in range(ctrls.count()):\n                el = ctrls.nth(i)\n                if not el.is_visible() and not el.evaluate(\"e => e.closest('.tile') !== null\"): continue\n                before = pg.evaluate(BOX)\n                target = el.locator(\"xpath=ancestor::label[1]\") if el.evaluate(\"e => e.closest('label') !== null\") else el\n                target.click(); pg.wait_for_timeout(60)\n                after = pg.evaluate(BOX)\n                if before != after:\n                    diff = [(x, y) for x, y in zip(before, after) if x != y][:3]\n                    print(\"MOVED\", f.name, w, i, diff); fails += 1\n        if errs: print(\"JS ERRORS\", w, errs); fails += 1\n        pg.close()\n    b.close()\nprint(\"fails\", fails)\nEOF\n.venv/bin/python $S/stable.py",
 "description": "Check overflow, hidden UI and click stability"
}
````

### User / tool · 2026-11-02T20:53:03.811Z

**tool result (error)**
````
Exit code 1
MOVED step1-add.html 390 3 [('8,96,90,65', '8,82,90,65'), ('98,96,90,65', '98,82,90,65'), ('188,96,90,65', '188,82,90,65')]
OVERFLOW index.html 320 390
MOVED step1-add.html 320 1 [('8,96,72,65', '8,86,72,65'), ('80,96,72,65', '80,86,72,65'), ('153,96,72,65', '153,86,72,65')]
MOVED step1-add.html 320 2 [('8,86,72,65', '8,52,72,65'), ('80,86,72,65', '80,52,72,65'), ('153,86,72,65', '153,52,72,65')]
OVERFLOW step1-found.html 320 352
OVERFLOW step2-done.html 320 350
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/stable.py", line 24, in <module>
    target.click(); pg.wait_for_timeout(60)
    ^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 11021, in click
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 174, in click
    return await self._frame._click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 598, in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("input[type=checkbox], .tile input, .sent, [data-theme-btn]").nth(1)
    - locator resolved to <span tabindex="0" class="sent on" role="checkbox" aria-checked="true">Persistent neck pain 6/10, daily headaches.</span>
  - attempting click action
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - <i></i> from <div class="titlebar">…</div> subtree intercepts pointer events
  - retrying click action
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - <span class="num">Item 4 of 19</span> from <div class="titlebar">…</div> subtree intercepts pointer events
  - retrying click action
    - waiting 20ms
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - <i></i> from <div class="titlebar">…</div> subtree intercepts pointer events
  2 × retrying click action
      - waiting 100ms
      - waiting for element to be visible, enabled and stable
      - element is visible, enabled and stable
      - scrolling into view if needed
      - done scrolling
      - <div class="card-h">…</div> from <section class="card" aria-label="To check">…</section> subtree intercepts pointer events
  14 × retrying click action
       - waiting 500ms
       - waiting for element to be visible, enabled and stable
       - element is visible, enabled and stable
       - scrolling into view if needed
       - done scrolling
       - <span class="num">Item 4 of 19</span> from <div class="titlebar">…</div> subtree intercepts pointer events
     - retrying click action
       - waiting 500ms
       - waiting for element to be visible, enabled and stable
       - element is visible, enabled and stable
       - scrolling into view if needed
       - done scrolling
       - <i></i> from <div class="titlebar">…</div> subtree intercepts pointer events
     - retrying click action
       - waiting 500ms
       - waiting for element to be visible, enabled and stable
       - element is visible, enabled and stable
       - scrolling into view if needed
       - done scrolling
       - <div class="card-h">…</div> from <section class="card" aria-label="To check">…</section> subtree intercepts pointer events
     - retrying click action
       - waiting 500ms
       - waiting for element to be visible, enabled and stable
       - element is visible, enabled and stable
       - scrolling into view if needed
       - done scrolling
       - <div class="card-h">…</div> from <section class="card" aria-label="To check">…</section> subtree intercepts pointer events
  - retrying click action
    - waiting 500ms
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - <span class="num">Item 4 of 19</span> from <div class="titlebar">…</div> subtree intercepts pointer events
  - retrying click action
    - waiting 500ms
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:53:16.175Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && sed -i '' 's/getBoundingClientRect().right > 391/getBoundingClientRect().right > 321/' $S/wide.py && sed -i '' 's/\"width\": 390, \"height\": 844/\"width\": 320, \"height\": 640/' $S/wide.py && .venv/bin/python $S/wide.py index,step1-found,step2-done",
 "description": "Find overflowing elements at 320"
}
````

### User / tool · 2026-11-02T20:53:16.784Z

**tool result**
````
index ['DIV.cc-top 357', 'BUTTON.btn quiet 357', 'DIV.cc-meta 357', 'OL.track 357', 'LI. 357', 'I. 357']
step1-found ['A.btn lg 352']
step2-done ['A.btn primary lg 345', 'A.btn 350', 'A.btn 350', 'A.btn 350', 'A.btn 350', 'A.btn 350']
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:53:31.223Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nrep = [\n (\".ccard { min-height: 244px;\", \".ccard { grid-template-columns: minmax(0, 1fr); min-height: 244px;\"),\n (\"  .answers li { grid-template-columns: 34px 1fr auto;\", \"  .answers li { grid-template-columns: 34px minmax(0, 1fr) auto;\"),\n (\"  .footer { padding: 12px 16px 16px; font-size: .875rem; }\\n}\",\n  \"  .footer { padding: 12px 16px 16px; font-size: .875rem; }\\n\"\n  \"  .row-actions .btn { flex: 1 1 100%; white-space: normal; text-align: center; height: auto; min-height: 56px; padding: 8px 16px; }\\n\"\n  \"  .ccard .cc-bottom .btn.lg { min-width: 0; padding: 0 12px; }\\n\"\n  \"}\\n\"\n  \"/* Short phones (e.g. 320x640, landscape): the frame would leave no room for the record, so the page scrolls instead.\\n\"\n  \"   Still nothing moves on click: the action bar stays pinned to the bottom and every box keeps its size. */\\n\"\n  \"@media (max-width: 760px) and (max-height: 720px) {\\n\"\n  \"  html:has(> body.frame) { overflow: visible; }\\n\"\n  \"  body.frame { display: block; height: auto; overflow: visible; }\\n\"\n  \"  body.frame .titlebar { height: var(--title-h); }\\n\"\n  \"  .work { display: grid; grid-template-rows: none; grid-auto-rows: auto; }\\n\"\n  \"  .work .card { max-height: none; }\\n\"\n  \"  .work .card-src .card-b { max-height: 260px; }\\n\"\n  \"  .work .card + .card .card-b { min-height: 120px; }\\n\"\n  \"  .actions { position: sticky; bottom: 0; z-index: 4; }\\n\"\n  \"}\\n\"),\n]\nfor a, b in rep:\n    assert a in c, a\n    c = c.replace(a, b)\np.write_text(c)\nEOF\npython3 build.py >/dev/null; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -i '' 's/return \\[Math.round(r.x), Math.round(r.y), /return [Math.round(r.x + scrollX), Math.round(r.y + scrollY), /' $S/stable.py; cd /Users/arsis/zlayt-pm-project && .venv/bin/python $S/stable.py",
 "description": "Fix 320 overflow, add short-phone mode, rerun stability test"
}
````

### User / tool · 2026-11-02T20:53:56.722Z

**tool result**
````
MOVED step1-add.html 320 2 [('8,96,72,65', '8,451,72,65'), ('80,96,72,65', '80,451,72,65'), ('153,96,72,65', '153,451,72,65')]
OVERFLOW step2-date-confirmed.html 320 328
OVERFLOW step2-disputed.html 320 328
MOVED step2-disputed.html 320 1 [('16,459,288,43', '16,896,288,43'), ('16,508,139,54', '16,945,139,54'), ('165,508,139,54', '165,945,139,54')]
OVERFLOW step2-entry.html 320 328
OVERFLOW step2-fix.html 320 328
MOVED step2-fix.html 320 1 [('16,437,288,65', '16,520,288,65'), ('16,508,139,54', '16,591,139,54'), ('165,508,139,54', '165,591,139,54')]
MOVED step2-write.html 320 2 [('16,459,288,43', '16,620,288,43'), ('16,508,139,54', '16,669,139,54'), ('165,508,139,54', '165,669,139,54')]
MOVED step3-count.html 320 1 [('16,459,288,43', '16,845,288,43'), ('16,508,139,54', '16,894,139,54'), ('165,508,139,54', '165,894,139,54')]
OVERFLOW step3-done.html 320 355
fails 10
[This command modified 1 file you've previously read: artifacts/mockups/guided/guided.css. Call Read before editing.]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:54:05.368Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python $S/wide.py step2-entry,step3-done",
 "description": "Find 320 overflow culprits"
}
````

### User / tool · 2026-11-02T20:54:05.950Z

**tool result**
````
step2-entry ['A.btn quiet 328', 'A. 471']
step3-done ['TABLE.mini 355', 'THEAD. 355', 'TR. 355', 'TH. 355', 'TBODY. 355', 'TR. 355']
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:54:14.020Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nadd = \"\"\"@media (max-width: 359px) {\n  .small .btn { font-size: .875rem; padding: 0 4px; }\n  .mini td.amt { white-space: normal; }\n  .mini th:nth-child(4), .mini td:nth-child(4) { display: none; }\n  .mini { table-layout: fixed; }\n}\n\"\"\"\nc = c.replace(\"/* Short phones\", add + \"/* Short phones\")\np.write_text(c)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 - <<EOF\nfrom pathlib import Path\np = Path(\"$S/stable.py\"); s = p.read_text()\ns = s.replace(\"\"\"                before = pg.evaluate(BOX)\n                target = el.locator(\"xpath=ancestor::label[1]\") if el.evaluate(\"e => e.closest('label') !== null\") else el\n                target.click(); pg.wait_for_timeout(60)\"\"\", \"\"\"                target = el.locator(\"xpath=ancestor::label[1]\") if el.evaluate(\"e => e.closest('label') !== null\") else el\n                target.scroll_into_view_if_needed(); pg.wait_for_timeout(60)\n                before = pg.evaluate(BOX)\n                target.click(); pg.wait_for_timeout(60)\"\"\")\np.write_text(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python $S/stable.py",
 "description": "Fix 320 small buttons/table, rerun stability test"
}
````

### User / tool · 2026-11-02T20:54:48.627Z

**tool result**
````
MOVED step2-fix.html 320 1 [('16,437,288,65', '16,520,288,65'), ('16,508,139,54', '16,591,139,54'), ('165,508,139,54', '165,591,139,54')]
MOVED step2-write.html 320 2 [('16,459,288,43', '16,620,288,43'), ('16,508,139,54', '16,669,139,54'), ('165,508,139,54', '165,669,139,54')]
fails 2
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:54:57.779Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 - <<EOF\nfrom pathlib import Path\np = Path(\"$S/stable.py\"); s = p.read_text()\ns = s.replace(\"\"\"                before = pg.evaluate(BOX)\n                target.click(); pg.wait_for_timeout(60)\n                after = pg.evaluate(BOX)\"\"\", \"\"\"                y0 = pg.evaluate(\"scrollY\"); before = pg.evaluate(BOX)\n                target.click(); pg.wait_for_timeout(60)\n                pg.evaluate(f\"window.scrollTo(0, {y0})\"); pg.wait_for_timeout(30)\n                after = pg.evaluate(BOX)\"\"\")\np.write_text(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python $S/stable.py",
 "description": "Rerun stability test scroll-normalized"
}
````

### User / tool · 2026-11-02T20:55:36.848Z

**tool result**
````
fails 0
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:55:49.901Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\nb = Path(\"build.py\"); t = b.read_text()\na = \"\"\"    if third:\n        parts.append(A(third[0], third[1], \"quiet\", disabled=third[1] is None))\"\"\"\nassert a in t\nt = t.replace(a, \"\"\"    if third:\n        parts.append(A(third[0], third[1], \"quiet\", disabled=third[1] is None))\n    else:       # keep the slot so Back and Decide later never move between items\n        parts.append('<span class=\"btn quiet\" aria-hidden=\"true\" style=\"visibility:hidden\">Fix the wording</span>')\"\"\")\nb.write_text(t)\nEOF\npython3 build.py >/dev/null; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $S/across.py <<'EOF'\nfrom pathlib import Path\nfrom playwright.sync_api import sync_playwright\nroot = Path(\"/Users/arsis/zlayt-pm-project/artifacts/mockups/guided\")\npages = [\"step2-entry\", \"step2-fix\", \"step2-flag\", \"step2-gap\", \"step2-disputed\", \"step2-cannot-check\", \"step2-write\", \"step2-date\", \"step2-date-confirmed\", \"step3-charge\", \"step3-never\", \"step3-count\"]\nSEL = \"\"\"() => [...document.querySelectorAll('.steps .step, .big .btn, .small .btn, .question, .card')].map(el => {const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(',')})\"\"\"\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in [(1440, 900), (390, 844)]:\n        pg = b.new_page(viewport={\"width\": w, \"height\": h}); ref = None\n        for n in pages:\n            pg.goto((root / f\"{n}.html\").as_uri()); pg.wait_for_timeout(100)\n            boxes = pg.evaluate(SEL)\n            if ref is None: ref = boxes; continue\n            if boxes != ref: print(\"DIFF\", w, n, [(i, a, c) for i, (a, c) in enumerate(zip(ref, boxes)) if a != c][:4])\n        pg.close()\n    b.close()\nprint(\"done\")\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python $S/across.py",
 "description": "Check boxes identical across review pages"
}
````

### User / tool · 2026-11-02T20:55:53.291Z

**tool result**
````
DIFF 1440 step2-flag [(9, '1025,802,83,48', '1062,802,83,48'), (10, '1116,802,155,48', '1153,802,118,48')]
DIFF 1440 step2-gap [(9, '1025,802,83,48', '1062,802,83,48'), (10, '1116,802,155,48', '1153,802,118,48')]
DIFF 390 step2-flag [(10, '109,772,131,40', '126,772,97,40')]
DIFF 390 step2-gap [(10, '109,772,131,40', '126,772,97,40')]
done
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:56:02.765Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/mockups/guided && python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"guided.css\"); c = p.read_text()\nrep = [(\".small { grid-area: small; display: flex; gap: 8px; justify-content: flex-end; }\", \".small { grid-area: small; display: flex; gap: 8px; justify-content: flex-end; }\\n.small .btn { width: 172px; }\"),\n       (\"  .small .btn { height: 40px; font-size: .9375rem; padding: 0 8px; }\", \"  .small .btn { flex: 1 1 0; width: auto; min-width: 0; height: 40px; font-size: .875rem; padding: 0 4px; }\")]\nfor a, b in rep:\n    assert a in c, a\n    c = c.replace(a, b)\np.write_text(c)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && .venv/bin/python $S/across.py && .venv/bin/python $S/stable.py",
 "description": "Fix small button widths, rerun both checks"
}
````

### User / tool · 2026-11-02T20:56:44.948Z

**tool result**
````
done
fails 0
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:56:56.494Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/final.py <<'EOF'\nfrom pathlib import Path\nfrom playwright.sync_api import sync_playwright\nroot = Path(\"/Users/arsis/zlayt-pm-project/artifacts/mockups/guided\")\nout = Path(\"/Users/arsis/zlayt-pm-project/artifacts/screenshots\")\npages = [\"index\", \"home-empty\", \"step1-add\", \"step1-found\", \"step1-drafting\", \"step1-failed\", \"step2-entry\", \"step2-fix\", \"step2-flag\", \"step2-gap\",\n         \"step2-disputed\", \"step2-cannot-check\", \"step2-write\", \"step2-date\", \"step2-done\", \"step3-charge\", \"step3-count\", \"step3-never\", \"step3-done\",\n         \"step4-letter\", \"step4-pending\", \"step4-blocked\"]\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in [(1440, 900), (390, 844)]:\n        for scheme in [\"light\", \"dark\"]:\n            ctx = b.new_context(viewport={\"width\": w, \"height\": h}, color_scheme=scheme); pg = ctx.new_page()\n            for n in (pages if scheme == \"light\" else [\"index\", \"step2-disputed\", \"step4-letter\"]):\n                pg.goto((root / f\"{n}.html\").as_uri()); pg.wait_for_timeout(1200 if n == \"step1-drafting\" else 200)\n                suffix = \"\" if scheme == \"light\" else \"-dark\"\n                pg.screenshot(path=str(out / f\"guided-mockup-{n}-{w}{suffix}.png\"))\n            ctx.close()\n    b.close()\nEOF\n.venv/bin/python $S/final.py && ls artifacts/screenshots/guided-mockup-* | wc -l && du -ch artifacts/screenshots/guided-mockup-* | tail -1",
 "description": "Write final screenshots at 1440 and 390"
}
````

### User / tool · 2026-11-02T20:57:11.132Z

**tool result**
````
      50
5.7M	total
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:12.613Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/guided-mockup-step2-disputed-1440-dark.png"
}
````

### User / tool · 2026-11-02T20:57:12.623Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:13.097Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/guided-mockup-step3-done-390.png"
}
````

### User / tool · 2026-11-02T20:57:13.108Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:13.574Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/guided-mockup-step1-drafting-1440.png"
}
````

### User / tool · 2026-11-02T20:57:13.583Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:17.661Z

Checks pass at 1440, 390 and 320. Updating the spec with what the build taught me, then closing out.

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:28.501Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"docs/GUIDED_UI_SPEC.md\"); s = p.read_text()\nrep = [\n (\"| current | filled accent circle with the number, accent bar under the segment, bold label, `aria-current=\\\"step\\\"` | e.g. \\\"16 of 19 left\\\" | opens the step |\",\n  \"| current (the step on screen) | filled accent circle (number, or a check when that step is done), accent bar under the segment, bold label, `aria-current=\\\"step\\\"` | e.g. \\\"16 of 19 left\\\" | opens the step |\"),\n (\"| needs attention | amber circle with \\\"!\\\" | e.g. \\\"Run again\\\" / \\\"1 problem\\\" | opens the step |\",\n  \"| needs attention | amber circle with \\\"!\\\" (a step she left with undecided items, a stopped run, an export problem) | e.g. \\\"Run again\\\" / \\\"2 left\\\" / \\\"1 problem\\\" | opens the step |\"),\n (\"A \\\"Find a case\\\" search box shows when there are more than 6 cases\", \"A \\\"Find a case\\\" search box shows when there are 6 or more cases\"),\n (\"3. **Small buttons**: \\\"‹ Back\\\", the item's third action (\\\"Fix the wording\\\" / \\\"Add a note\\\" / none), \\\"Decide later\\\", and the\\n   **status slot**\",\n  \"3. **Small buttons** of one fixed width (172 px; equal thirds on phones): \\\"‹ Back\\\", the item's third action (\\\"Fix the wording\\\" /\\n   \\\"Add a note\\\"; an invisible placeholder keeps the slot when an item has none, so Back and Decide later never move), \\\"Decide later\\\"; then the\\n   **status slot**\"),\n (\"- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons\\n  in one row below); the source card takes the remaining height; no horizontal scroll anywhere.\",\n  \"- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons\\n  in one row below); the line card is a fixed 256 px, the source card takes the remaining height; no horizontal scroll anywhere.\\n- **Short phones (height ≤ 720 px and width ≤ 760 px, e.g. 320x640 or landscape):** the fixed frame would leave no room for the record,\\n  so the review page scrolls as a normal page; the action bar is `position: sticky; bottom: 0`, the source card body is capped at 260 px.\\n  Clicking still moves nothing (checked by the mockup test at 320x640).\"),\n (\"## 13. Test plan for the build card\",\n  \"## 13. Test plan for the build card\\nThe mockup already passes the first two checks (Playwright, `file://`): every checkbox, tile, tappable sentence and the theme button\\nwas clicked on all 28 pages at 1440x900, 390x844 and 320x640 with 0 boxes moved, 0 horizontal overflow, 0 `<details>`/menus and 0 JS\\nerrors; and the step bar, both answers, the small buttons, the question and both cards sit at identical boxes on all 12 review pages\\n(Step 2 and 3 items) at 1440 and 390, so moving from one item to the next moves nothing.\\n\"),\n]\nfor a, b in rep:\n    assert a in s, a[:60]\n    s = s.replace(a, b)\np.write_text(s)\nEOF\npkill -f \"app.main\" -U $(id -u) 2>/dev/null; lsof -ti :8766 | xargs kill 2>/dev/null; python3 tools/check_secrets.py --help >/dev/null 2>&1; echo ok",
 "description": "Update spec details; stop my fixture server"
}
````

### User / tool · 2026-11-02T20:57:28.553Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not pkill/killall by pattern; stop only your own server by PID (kill $!)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:30.810Z

**tool call — Bash**
````
{
 "command": "grep -c \"6 or more cases\" docs/GUIDED_UI_SPEC.md; grep -c \"Short phones\" docs/GUIDED_UI_SPEC.md; PID=$(lsof -ti tcp:8766 -sTCP:LISTEN); echo \"pid $PID\"; [ -n \"$PID\" ] && kill $PID; echo stopped",
 "description": "Verify spec edit applied; stop my server by PID"
}
````

### User / tool · 2026-11-02T20:57:30.983Z

**tool result**
````
0
0
pid 92625
stopped
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:39.961Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nfrom pathlib import Path\np = Path(\"docs/GUIDED_UI_SPEC.md\"); s = p.read_text()\nrep = [\n (\"| current | filled accent circle with the number, accent bar under the segment, bold label, `aria-current=\\\"step\\\"` | e.g. \\\"16 of 19 left\\\" | opens the step |\",\n  \"| current (the step on screen) | filled accent circle (number, or a check when that step is done), accent bar under the segment, bold label, `aria-current=\\\"step\\\"` | e.g. \\\"16 of 19 left\\\" | opens the step |\"),\n (\"| needs attention | amber circle with \\\"!\\\" | e.g. \\\"Run again\\\" / \\\"1 problem\\\" | opens the step |\",\n  \"| needs attention | amber circle with \\\"!\\\" (a step she left with undecided items, a stopped run, an export problem) | e.g. \\\"Run again\\\" / \\\"2 left\\\" / \\\"1 problem\\\" | opens the step |\"),\n (\"A \\\"Find a case\\\" search box shows when there are more than 6 cases\", \"A \\\"Find a case\\\" search box shows when there are 6 or more cases\"),\n (\"3. **Small buttons**: \\\"‹ Back\\\", the item's third action (\\\"Fix the wording\\\" / \\\"Add a note\\\" / none), \\\"Decide later\\\", and the\\n   **status slot**\",\n  \"3. **Small buttons** of one fixed width (172 px; equal thirds on phones): \\\"‹ Back\\\", the item's third action (\\\"Fix the wording\\\" /\\n   \\\"Add a note\\\"; an invisible placeholder keeps the slot when an item has none, so Back and Decide later never move), \\\"Decide later\\\"; then the\\n   **status slot**\"),\n (\"- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons\\n  in one row below); the source card takes the remaining height; no horizontal scroll anywhere.\",\n  \"- **Mobile 390 px:** same screens, one column; the action bar stays fixed at the bottom (two big answers side by side, small buttons\\n  in one row below); the line card is a fixed 256 px, the source card takes the remaining height; no horizontal scroll anywhere.\\n- **Short phones (height ≤ 720 px and width ≤ 760 px, e.g. 320x640 or landscape):** the fixed frame would leave no room for the record,\\n  so the review page scrolls as a normal page; the action bar is `position: sticky; bottom: 0`, the source card body is capped at 260 px.\\n  Clicking still moves nothing (checked by the mockup test at 320x640).\"),\n (\"## 13. Test plan for the build card\",\n  \"## 13. Test plan for the build card\\nThe mockup already passes the first two checks (Playwright, `file://`): every checkbox, tile, tappable sentence and the theme button\\nwas clicked on all 28 pages at 1440x900, 390x844 and 320x640 with 0 boxes moved, 0 horizontal overflow, 0 `<details>`/menus and 0 JS\\nerrors; and the step bar, both answers, the small buttons, the question and both cards sit at identical boxes on all 12 review pages\\n(Step 2 and 3 items) at 1440 and 390, so moving from one item to the next moves nothing.\\n\"),\n]\nfor a, b in rep:\n    assert a in s, a[:60]\n    s = s.replace(a, b)\np.write_text(s)\nprint(\"ok\")\nEOF",
 "description": "Apply spec refinements"
}
````

### User / tool · 2026-11-02T20:57:40.062Z

**tool result**
````
ok
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:57:47.695Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && (echo '\"\"\"T-180 mockup check: click every in-page control on every page at 1440x900, 390x844, 320x640; assert no box moved, no overflow, no details/menus, no JS errors. Run: .venv/bin/python artifacts/mockups/guided/check_stability.py\"\"\"'; cat $S/stable.py) > artifacts/mockups/guided/check_stability.py && (echo '\"\"\"T-180 mockup check: step bar, answers, small buttons, question and cards sit at identical boxes on every review page (item to item moves nothing). Run: .venv/bin/python artifacts/mockups/guided/check_across_items.py\"\"\"'; cat $S/across.py) > artifacts/mockups/guided/check_across_items.py && .venv/bin/python artifacts/mockups/guided/check_stability.py && .venv/bin/python artifacts/mockups/guided/check_across_items.py",
 "description": "Save layout checks with the mockup and rerun"
}
````

### User / tool · 2026-11-02T20:58:29.355Z

**tool result**
````
fails 0
done
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:58:40.067Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_guided_ui.md",
 "content": "---\nname: guided-ui-d068\ndescription: T-180 guided four-step UI (D-068) - spec + generated static mockup; where things live, API facts the spec relies on, layout-stability recipe and pitfalls for the build card\nmetadata:\n  type: project\n---\n\nD-068 (Chris, 2026-11-02): the app becomes Your cases + a fixed 4-step guide (Add records, Check the timeline, Check the bills, Get your letter),\none item at a time; old screen moves to /classic. T-180 delivered `docs/GUIDED_UI_SPEC.md` and a mockup in `artifacts/mockups/guided/`\n(pages are GENERATED by `build.py`: edit build.py/guided.css/guided.js, then `python3 artifacts/mockups/guided/build.py`; never hand-edit the html).\n\n**Why:** Chris: \"VERY hard to use... sections move around... so simple someone's grandma can use it\". Every screen must answer where am I / what now / how do I know I'm done, and nothing may move on click.\n\n**How to apply (build card):**\n- API facts the spec leans on: `GET /api/cases` is local-mode only (404 public) -> public home lists tokens kept in localStorage; `status.progress.label` contains stage ids (jargon) -> map `stage` to plain copy; D-066 accept body is `compared: true` (422 COMPARE_REQUIRED, `review.judge_dispute`), not yet in api.md at T-180 time; non-charge amounts are listed in notes only when accepted (dismissed = left out); dismissed flags still appear under FLAGS DISMISSED; tray items are not in `review.counts.pending`.\n- Queue order = the T-157 next_action rule (cited record date, undated last, record position, entry before flag, id); freeze it when the step opens.\n- Layout checks: `check_stability.py` (click every control at 1440/390/320, compare boxes in DOCUMENT coords and scroll back to the original scrollY before measuring, else sticky bars look \"moved\") and `check_across_items.py` (same boxes on every review page).\n- Pitfalls hit: `[hidden]` loses to `display:flex` (add `[hidden]{display:none!important}`); grid children need `minmax(0,1fr)` or nowrap text overflows at 320/390; a radio drawn with a thicker checked border shifts its label (use inset box-shadow); a missing third small button shifts Back/Decide later (keep an invisible placeholder, fixed widths); 320x640 cannot hold the fixed frame -> short-phone media query makes the page scroll with a sticky action bar.\n- Real payloads for mockup content came from a `git archive HEAD` copy served with `ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated` (sample = prepared answers; library cases = recorded). Stop it by PID (hook blocks pkill).\n"
}
````

### User / tool · 2026-11-02T20:58:40.121Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_guided_ui.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:58:44.912Z

**tool call — Bash**
````
{
 "command": "echo \"- [Guided UI (D-068)](project_guided_ui.md) — T-180 spec + generated mockup, API facts, layout-stability checks, pitfalls\" >> .claude/agent-memory/frontend/MEMORY.md && B=\"python3 tools/board.py\" && $B note T-180 --agent frontend --text \"Spec written (docs/GUIDED_UI_SPEC.md, 13 sections incl. API mapping per control). Mockup generated: 28 pages in artifacts/mockups/guided (build.py). Layout checks pass: check_stability.py 0 moved/0 overflow at 1440/390/320; check_across_items.py identical boxes across 12 review pages. 50 screenshots artifacts/screenshots/guided-mockup-*.png. Assumption: docs/ and artifacts/ paths written by frontend because the T-180 brief assigned them.\" >/dev/null && $B ac T-180 --check 1 --agent frontend --evidence \"docs/GUIDED_UI_SPEC.md (screens, copy, states, API per control in s.11); artifacts/mockups/guided/index.html + screens.html (28 pages); artifacts/screenshots/guided-mockup-*-1440.png / -390.png (+3 dark); .venv/bin/python artifacts/mockups/guided/check_stability.py -> fails 0; check_across_items.py -> no diffs\" && git status --short docs/GUIDED_UI_SPEC.md artifacts/mockups/guided artifacts/screenshots | head; git diff --cached --name-only | head",
 "description": "Index memory, note card, check AC, inspect staging"
}
````

### User / tool · 2026-11-02T20:58:45.139Z

**tool result**
````
AC 1 checked: docs/GUIDED_UI_SPEC.md (screens, copy, states, API per control in s.11); artifacts/mockups/guided/index.html + screens.html (28 pages); artifacts/screenshots/guided-mockup-*-1440.png / -390.png (+3 dark); .venv/bin/python artifacts/mockups/guided/check_stability.py -> fails 0; check_across_items.py -> no diffs
D  artifacts/screenshots/mvp-case-top-dark-1440.png
D  artifacts/screenshots/mvp-case-top-dark-390.png
D  artifacts/screenshots/mvp-case-top-light-1440.png
D  artifacts/screenshots/mvp-case-top-light-390.png
D  artifacts/screenshots/mvp-charges-dark-1440.png
D  artifacts/screenshots/mvp-charges-dark-390.png
D  artifacts/screenshots/mvp-charges-light-1440.png
D  artifacts/screenshots/mvp-charges-light-390.png
D  artifacts/screenshots/mvp-counted-line-dark-1440.png
D  artifacts/screenshots/mvp-counted-line-dark-390.png
.claude/agent-memory/frontend/MEMORY.md
.claude/agent-memory/frontend/project_t166_mvp_polish.md
.claude/agent-memory/frontend/project_t174_finish.md
app/backend/case_list.py
app/backend/pipeline.py
app/backend/trace.py
app/frontend/api.js
app/frontend/app.js
app/frontend/audit.js
app/frontend/charges.js
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:58:53.064Z

**tool call — Bash**
````
{
 "command": "git add docs/GUIDED_UI_SPEC.md artifacts/mockups/guided/*.html artifacts/mockups/guided/guided.css artifacts/mockups/guided/guided.js artifacts/mockups/guided/build.py artifacts/mockups/guided/check_stability.py artifacts/mockups/guided/check_across_items.py artifacts/screenshots/guided-mockup-*.png && git commit -q -m \"feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)\n\ndocs/GUIDED_UI_SPEC.md: Your cases, fixed 4-step bar, one-item review with\nplain questions, D-059/D-064/D-066 confirms, letter step, states, visual\nsystem, API mapping per control. artifacts/mockups/guided: 28 generated\npages (build.py) with layout-stability checks; screenshots at 1440 and 390.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- docs/GUIDED_UI_SPEC.md artifacts/mockups/guided artifacts/screenshots/guided-mockup-*.png && git log --oneline -1 && git show --stat HEAD | tail -5",
 "description": "Stage and commit only T-180 paths"
}
````

### User / tool · 2026-11-02T20:58:53.135Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git add docs/GUIDED_UI_SPEC.md artifacts/mockups/guided/*.html artifacts/mockups/guided/guided.css artifacts/mockups/guided/guided.js artifacts/mockups/guided/build.py artifacts/mockups/guided/check_s
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:58:55.438Z

**tool call — Bash**
````
{
 "command": "git add docs/GUIDED_UI_SPEC.md artifacts/mockups/guided/*.html artifacts/mockups/guided/guided.css artifacts/mockups/guided/guided.js artifacts/mockups/guided/build.py artifacts/mockups/guided/check_stability.py artifacts/mockups/guided/check_across_items.py artifacts/screenshots/guided-mockup-*.png && echo staged",
 "description": "Stage T-180 files"
}
````

### User / tool · 2026-11-02T20:58:55.739Z

**tool result**
````
staged
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:58:58.753Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)\n\ndocs/GUIDED_UI_SPEC.md: Your cases, fixed 4-step bar, one-item review with\nplain questions, D-059/D-064/D-066 confirms, letter step, states, visual\nsystem, API mapping per control. artifacts/mockups/guided: 28 generated\npages (build.py) with layout-stability checks; screenshots at 1440 and 390.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- docs/GUIDED_UI_SPEC.md artifacts/mockups/guided artifacts/screenshots/guided-mockup-*.png && git log --oneline -1 && git show --stat HEAD | tail -3",
 "description": "Commit T-180 paths with pathspec"
}
````

### User / tool · 2026-11-02T20:59:03.638Z

**tool result**
````
check_secrets: ok (84 file(s) scanned staged)
b01382f feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)
 .../guided-mockup-step4-pending-390.png            | Bin 0 -> 80319 bytes
 docs/GUIDED_UI_SPEC.md                             | 571 ++++++++++++++++++++
 84 files changed, 2508 insertions(+)
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:59:11.912Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B handoff T-180 --agent frontend --text \"What changed: docs/GUIDED_UI_SPEC.md (Your cases + case cards with Next line/Continue, public-mode home from stored tokens since GET /api/cases is local-only; fixed step bar; Step 1 add/read/draft with plain stage copy (prepared vs live); Step 2 one-item queue in next_action order with entry, fix wording, D-066 compare box (compared:true), could-not-check + write it myself, date pick, plain-language warning questions per flag category; Step 3 charge / D-064 count with named box / D-059 confirm / never-counted; Step 4 ready, N undecided + go to first, blocked; states, visual system, words table, API per control). Mockup: artifacts/mockups/guided/index.html (+screens.html), 28 pages generated by build.py from real fixture payloads (sample prepared, lib11, case_01). How verified: check_stability.py fails 0 at 1440/390/320 (every control clicked, no box moved, no overflow, no details/menus, no JS errors); check_across_items.py identical boxes across 12 review pages; 50 screenshots artifacts/screenshots/guided-mockup-*.png. What's left: build card (guided UI in app/frontend, /classic move, own e2e); backend to add D-066 compared field to api.md. Surprised: 320x640 cannot hold a fixed frame (short-phone mode scrolls with sticky actions); dismissed non-charges drop from notes but dismissed flags stay listed, so answer copy differs per kind.\" >/dev/null && $B move T-180 in_review --agent frontend && $B commit T-180 --sha b01382f --agent frontend && $B lesson --agent frontend --text \"T-180: a no-reflow promise needs a measuring test, not eyeballing: clicking every control and diffing bounding boxes (doc coords, scroll restored) caught 4 real shifts (radio border growth, hidden row shown by display:flex, missing third button slot, nowrap overflow at 320) that screenshots looked fine on.\" >/dev/null; $B show T-180 | head -12",
 "description": "Handoff, move to review, record commit and lesson"
}
````

### User / tool · 2026-11-02T20:59:12.270Z

**tool result**
````
T-180: in_progress -> in_review
T-180: commit b01382f recorded
---
id: "T-180"
title: "Guided UI design (D-068): exact spec + clickable static mockup of Your cases, the 4 fixed steps, one-item-at-a-time review, bills, letter; grandma-simple, looks nice"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:32:49Z"
updated_at: "2026-11-02T20:59:12Z"
claimed_by: "frontend"
````

### Assistant · claude-opus-5-5 · 2026-11-02T20:59:16.226Z

T-180 is in review (commit b01382f). The mockup is at `/Users/arsis/zlayt-pm-project/artifacts/mockups/guided/index.html`, and `screens.html` in the same folder lists all 28 pages. The spec is `/Users/arsis/zlayt-pm-project/docs/GUIDED_UI_SPEC.md`, covering all nine sections, with the API call and field behind every control in §11; screenshots are `artifacts/screenshots/guided-mockup-*-1440.png` / `-390.png` (plus 3 in dark mode). A click-and-measure check (`check_stability.py`) found nothing moving at 1440, 390 or 320. Going from one review item to the next leaves every control in the same place (`check_across_items.py`). Content is real sample-case data from the app's fixture mode; three screens show states the sample never produces and are marked "state variant", and the D-066 confirm sends a `compared: true` field that is in the backend code but not yet in `api.md`.
