# Subagent: Full-stack: T-177 honest provenance (Full-stack: T-177 honest provenance)

Source: `agent-ab0f85b97ad25a443.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T20:09:07.675Z

You are a full-stack worker in /Users/arsis/zlayt-pm-project on T-177, the M3 gate blocker (P0). Claim it with `python3 tools/board.py claim T-177 --agent backend`. You may edit both app/backend and app/frontend for this card only; no other worker is in these areas right now.

Read:
- D-065 (new) and D-029 in memory/ORCHESTRATOR_DECISIONS.md;
- the blocker in reviews/GATE-M3-product-manager.md, with its evidence in artifacts/review-evidence/GATE-M3-pm/.

**Backend.** Each item's provenance comes from its fixture's `recorded_from`. A curated answer is marked `prepared: true`, with model 'hand-checked (qa)', in the item, the trace and the audit rows. The trace generator step for a curated item reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft". Recorded and live answers keep their real model ids.

**Frontend.**
- Badge: "Demo: sample answers prepared by our team".
- Tooltip: "The AI's own answers on these cases are in the evaluation report."
- Curated items get a "Prepared answer" tag, never "AI draft". Recorded and live items keep "AI draft".

**Tests and finish.**
- Write tests first, using the PM's acceptance test as e2e and unit tests, on both the curated and the recorded sets.
- Verify only from a `git archive HEAD` copy on your own port with E2E_REQUIRE_DB=1.
- Update memory/contracts/api.md.
- Commit via a temp index; never run `git checkout` on files.
- Write the handoff, move the card to in_review, and restart the shared app with tools/serve_app.sh.

Reply in 2 lines.

### User / tool · 2026-11-02T20:09:07.681Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:11.610Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-177 --agent backend; python3 tools/board.py show T-177; grep -n \"D-065\\|D-029\" memory/ORCHESTRATOR_DECISIONS.md | head"
}
````

### User / tool · 2026-11-02T20:09:11.802Z

**tool result**
````
T-177 claimed by backend
---
id: "T-177"
title: "GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:09:00Z"
updated_at: "2026-11-02T20:09:11Z"
claimed_by: "backend"
claimed_at: "2026-11-02T20:09:11Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "E2E on FIXTURE_SET=curated: no 'AI draft' or 'recorded AI answers' on a curated item; /items/e1/trace generator step model is not claude-sonnet-5-5 and names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'; with the recorded set, labels say AI; unit + e2e", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:09:02Z orchestrator: assigned: backend
- 2026-11-02T20:09:11Z backend: claimed

## Handoff (filled when moving to in_review)

37:| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
64:| D-056 | Amends D-029 (2026-11-02, T-115): curated fixtures may hand-shape extraction and narrative outputs for the demo, but **judge answers are never scripted**: every judge answer the demo or eval replays is a real recorded model output, and a curated file may never shadow a recording for the same key. tests/unit/test_curated_fixtures.py enforces it (empty allow-list). | Scripted judge answers make the ladder's second check fictional; four had been written by hand, one overriding a real recording. | T-115 staff r1/r2 |
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "The AI's own answers on these cases are in the evaluation report." A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:13.485Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p reviews/GATE-M3-product-manager.md | head -150; ls artifacts/review-evidence/GATE-M3-pm/; git status --short | head -20; git log --oneline | head -3; cat tools/serve_app.sh | head -40"
}
````

### User / tool · 2026-11-02T20:09:13.646Z

**tool result**
````
# GATE-M3: product-manager-reviewer (Dana Okafor persona)

**Commit:** pinned at d0b04bc. `git rev-parse --short HEAD` printed `d0b04bc`.

**Run:** from a `git archive d0b04bc` copy in the scratchpad, on 127.0.0.1:7973, with these settings:
- `LLM_BACKEND=fixture`
- `FIXTURE_SET=curated`
- `ZLAYT_MODE=local`
- `ZLAYT_DB` pointing to the scratchpad

**Server:** stopped by PID 50240. After that the port returned `000`.

**Evidence:** `artifacts/review-evidence/GATE-M3-pm/`

**Verdict: fail (1 blocker).**

## Answers to the brief

**Does the MVP do the paralegal's job without over-claiming?** On the job itself, yes. I ran the sample case end to end:
- 9 entries came out, and the 73-day gap was flagged.
- The 28-day interval was not flagged.
- The two accident dates are shown as a conflict, and the tool does not pick one.
- The $185 rate goes to "Amounts not totaled".
- The letter total is `$8,390.00`.
- The export is blocked until she accepts something.
- The letter and notes match the golden export exactly (`--check-spec` exit 0).

On over-claiming, no:
- The demo sample replays 19 hand-written QA responses. Each file says "Not a model output."
- The app labels them "Demo: recorded AI answers" and tags each entry "AI draft".
- The Why trace says "The AI read this record and proposed a one-line summary". It names `claude-sonnet-5-5`.
- The audit log records `extract_v1` / `claude-sonnet-5-5` for all 9 of those calls.
- D-029 required the label "cached demo (curated responses)". T-166 F7 removed it as jargon, and no decision replaced it.

**Are the cuts and debts honest?** The per-card debts (7c to 7g, 13 to 13f) are specific and honest, and they give a cost to add each one. The cut list as a whole is no longer true:
- SCOPE_CUTS rows 2, 5, 12, 13, 14, 16, 17 and 19 still read as cut, but they were built under D-031.
- REQUIREMENTS §4 argues against building PDF upload and the firm-voice paragraph. Both are now in the app, along with all four Appendix A stretch items.

**Are D-059 to D-064 defensible?** Mostly:
- **D-059, D-060, D-062 and D-064** form one coherent story: charges are default-deny, and a person confirms each line by name. The total line is honest ("accepted from these records"). On lib10 the total sums to `$8,123.50`, the expected figure.
- **D-061** is defensible because it fails toward a false conflict.
- **D-063** is Chris's call. But it held T-059 (the draft paragraph) with its eval unmet while the feature stays live in the UI. It also left the P0 card T-167 blocked.
- **D-064 conflicts with the spec.** SCOPE_CUTS row 7g says 'Proposed' and 'Quoted' lines can still be counted. R-CH-3 and R-CH-7 say estimates are never totaled, and REQUIREMENTS was not amended.

**Biggest product risk before M4/M5:** the human step is the only gate on AI summaries that the second check disputed, and it is a one-click Accept that does not say what is wrong.
- Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click.
- Each one put a summary into the carrier letter that its own Source quote does not support. For example, lib11 e2 adds "after passenger vehicle was struck from behind".
- About a third of library items need review (106 of 297), so she will be clicking through a lot of warnings.
- Nothing measures what actually reaches the letter after a realistic accept pattern.

```json
{"card": "GATE-M3", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive d0b04bc (HEAD d0b04bc); app at 127.0.0.1:7973 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), server PID 50240 stopped; sample case + all 15 library packets; docs: CONTRACT What-we-evaluate and M3, spec/REQUIREMENTS.md incl. §7 ship bar, ORCHESTRATOR_DECISIONS D-042..D-064, SCOPE_CUTS, GATE-M2-summary, MVP-ux-audit-r4",
 "exercised": [
  "journey.py on the sample (API, real pipeline, fixture/curated): create, run, read, export 422 before any accept, accept every item one at a time, export 200; letter and notes in journey-sample.out (gap 73 flagged; $185 under Amounts not totaled; total $8,390.00; accident dates not merged)",
  "journey.py on lib11, lib08 and lib10 (journey-lib11.out, journey-lib08.out, journey-lib10.out); Count this charge on lib11 a3 (lib11-counted-letter.out)",
  "lib_sweep.py over the sample + 15 library cases: needs_review counts, and judge-disputed entries accepted with one click (lib_sweep.out: 106/297 needs_review; 5 of 5 disputed accepted with 200)",
  "ui_walk.py (Playwright 1440): lib11 e2 row screenshot (02-lib11-e2-row.png), Accept click (no dialog, review_status accepted), full sample page (04-sample-top.png: badge 'Demo: recorded AI answers', 'AI draft' tags, 'Accept all verified entries', draft paragraph panel)",
  "POST /narrative + /narrative/review accept on the sample; the letter then gains a 'TREATMENT SUMMARY' block (sample-narrative-structure.out)",
  "GET /items/e1/trace and /audit on the sample (sample-e1-trace.out): generator step says 'The AI read this record...' model claude-sonnet-5-5; audit counts 9 extract_v1 + 9 flags_v1 + 1 narrative_v1 calls as claude-sonnet-5-5",
  "curated_provenance.py: tests/fixtures/llm/curated has 19 files, each with CURATED 'hand-checked response written by qa ... Not a model output', recorded_from model 'hand-checked (qa)'",
  "In the d0b04bc copy: evals.run --check-spec exit 0; evals.letter_check value 0 over 25 cases; evals.run fixture (fixture-eval-d0b04bc.md: grounding 1.000, entry_recall 0.982, all flag P/R 1.000, hallucination 40/40, must_not 0; ship_bar False by design on fixture)",
  "evals.library_report regenerated at d0b04bc (library-d0b04bc.md); lib_missed.py lists missed must-flags for lib08/09/10/13/15",
  "git log 312efe6..d0b04bc -- app/llm/prompts app/llm/lexicon.yaml: empty (regression discipline holds); committed evals/reports/latest.json: 2026-11-02T14:39:59Z fixture ship_bar_met False",
  "board.py status/list/show: T-045 in_review; T-059, T-167 (P0), T-170 blocked; paralegal verify_quickly 4 in GATE-M2-r2 and T-149-r2"
 ],
 "verdict": "fail",
 "scores": {"solves_paralegal_job": 4, "no_over_claiming": 2, "scope_cut_honesty": 2, "decisions_defensible": 4, "ai_judgment_ship_bar": 3, "workflow_fit": 3},
 "findings": [
  {"severity": "blocker", "title": "The demo shows hand-written QA answers as AI output: badge, 'AI draft' tags, Why trace and audit all name the model",
   "evidence": "tests/fixtures/llm/curated/*.json (19 files, 9 extract + 9 flags + 1 narrative): CURATED 'hand-checked response written by qa from evals/golden ... Not a model output', recorded_from.model 'hand-checked (qa)'. app/frontend/app.js:13-14 badge 'Demo: recorded AI answers', tooltip 'This demo replays recorded AI answers for its sample cases.' 04-sample-top.png shows the badge and an 'AI draft' tag on every sample entry. sample-e1-trace.out: 'AI drafted a summary and picked a quote | The AI read this record and proposed a one-line summary and a quote. | model claude-sonnet-5-5'. /audit counts ('fixture','claude-sonnet-5-5','extract_v1') x9. D-029 (binding): 'the UI labels it cached demo (curated responses) ... honesty needs the label'; no decision supersedes it (T-166 F7 removed the wording as jargon)",
   "why_it_matters": "The public demo and the video are built on this sample. A panel that opens a fixture file will find that the output it saw labeled as the AI's was written by the team to match the golden file. The real model picks different excerpts (D-029 says so). This is the over-claim that ends trust, and the audit trail, which is a product feature, states something false.",
   "fix": "Put back an honest label in plain words, e.g. badge 'Demo: sample answers prepared by our team'; tooltip 'The AI's own answers on this case are in the eval report'. Curated items get a 'prepared answer' tag, not 'AI draft'. The trace step for a curated response reads 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'. The audit stores model 'hand-checked (qa)' from recorded_from. Alternatively, point the demo at the recorded live set and change the R-EX-6 byte test to structure only. Record whichever is chosen as a D-entry that amends D-029.",
   "acceptance_test": "E2E on FIXTURE_SET=curated: no element contains 'AI draft' or 'recorded AI answers' for a curated item; /items/e1/trace generator step evidence.model.id is not claude-sonnet-5-5 and its why names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'. With the recorded set, labels say AI."},
  {"severity": "major", "title": "Biggest product risk: a one-click Accept puts a summary the second check disputed into the carrier letter, and nobody is told which words are unsupported",
   "evidence": "lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.",
   "why_it_matters": "Ship bar 4 measures the model before the human. What reaches the letter depends on a tired paralegal clicking through a third of the items. The failure the persona fears most, the letter saying something its own Source line does not, is one click away and leaves no trace for the attorney.",
   "fix": "For entries with JUDGE_PARTIAL or JUDGE_UNSUPPORTED: (1) code marks the summary's content words that are not in the quote; (2) Accept needs either an edit or a named confirm ('I checked the summary against the quote'); (3) the internal notes list 'accepted over a second-check objection: record N' so the attorney sees it; (4) add a reported eval, 'letter summary lines whose own Source quote does not support them, accept-all profile, library + golden', and put its number in the product note.",
   "acceptance_test": "lib11 e2 accept without confirm or edit returns 422 with a plain reason; with the confirm it is 200 and internal_notes_text names record 2 under the objection section; the new eval metric appears in the report."},
  {"severity": "major", "title": "The cut list and the spec no longer describe the product (R-CO-8 fails): 'cut' items are built, all four stretch items ship, and R-CH-7 is contradicted",
   "evidence": "memory/SCOPE_CUTS.md:6-23 rows 2 (multi-case), 5 (firm-voice prose), 12 (manual entry), 13 (LLM split), 14 (batch accept, 'single-key accept is fast enough'), 16, 17, 19 still read as cut. :54 lists only D-042 reinstatements, not D-031's. 04-sample-top.png shows 'Accept all verified entries (9)', 'All cases', 'Draft treatment paragraph', 'Exhibit and Bates numbers'. spec/REQUIREMENTS.md:159-168 names one stretch (side-by-side) and argues against PDF upload and the firm-voice paragraph; §5 non-goals 1, 2, 9-14, 16, 19 contradict the build. R-CH-7 (:84) says 'no path turns a rate, estimate or unreadable amount into a totaled charge', but SCOPE_CUTS 7g says 'Proposed'/'Quoted' charge lines are still countable (D-064). Appendix A: 'Stretch (pick at most one ...)'.",
   "why_it_matters": "Appendix A grades 'cut scope on purpose and tell us what you cut'. Right now the written reasons argue against features the panel will see working. That reads as either not knowing the product or not cutting at all. An estimate counted into 'Billed charges accepted' is a false statement in the letter that the spec still forbids.",
   "fix": "Rewrite SCOPE_CUTS as the current truth: one table with status cut / built (D-031/D-042) / held (D-063), each with its reason. Amend REQUIREMENTS §4/§5 and R-CH-3/R-CH-7 by ADR, or make 'Proposed'/'Quoted'/estimate lines not countable (class a). Get Chris's answer on presenting four stretch items (questions_for_chris) and write that reason into the note draft.",
   "acceptance_test": "Script: every REQUIREMENTS §5 non-goal maps to a SCOPE_CUTS row whose status matches the running app (route or testid present = built). R-CH-7 text agrees with count_charge.py; a 'Proposed charge $X' line is NOT_COUNTABLE, or the spec says why it is countable."},
  {"severity": "major", "title": "The draft paragraph (stretch, T-059 held with its eval unmet) is live and writes a second copy of the chronology into the letter",
   "evidence": "board.py show T-059: status blocked, AC3 'eval: 0 unsupported sentences across 3 runs on the sample (live backend)' done:false. grep -c narrative evals/run.py prints 0. After POST /narrative + accept, sample-narrative-structure.out shows the letter gains 'TREATMENT SUMMARY' (lines 38-48): 9 sentences 'On January 9, 2026, Austin EMS run report: <same summary> (<same citation>)', restating the chronology above it.",
   "why_it_matters": "This is an LLM output that reaches the carrier letter with no ship-bar number. It is the firm-voice stretch that REQUIREMENTS said 'would need its own verification', and it repeats the chronology without adding anything. It weakens the builder-mindset story and adds risk with no user value shown.",
   "fix": "Default it off (config flag) in the M3/M4 build until T-059 AC3 passes and evals.run reports a narrative unsupported count; or remove it and list it as a cut with the reason.",
   "acceptance_test": "With default config, GET /narrative returns 404 or the panel is absent (no btn-draft-narrative). With the flag on, the eval report has a narrative metric with a value."},
  {"severity": "major", "title": "The ship bar's 1.000 flag numbers do not generalize: at d0b04bc the library shows 34/42 must-flags; the committed library and latest.json reports are stale",
   "evidence": "library-d0b04bc.md (regenerated at d0b04bc): must flags 1/3 lib08, 1/2 lib09, 0/1 lib10, 1/3 lib13, 1/3 lib15, 34/42 = 0.81 overall. lib_missed.py: missed conflicts 'Denies LOC per patient' vs 'brief loss of consciousness at the second collision', 'Left shoulder pain' vs 'Right shoulder pain', 'denies back pain' vs 'Low back pain 8/10'; lib10 G1 49-day gap reported as 'Gap of 43 days' from a CMS-1500. The committed evals/reports/library-latest.md is from a74b727 (231 commits back) and shows must_not hits that no longer reproduce. The committed evals/reports/latest.json reads ship_bar_met False (fixture, 14:39Z).",
   "why_it_matters": "The product note will quote 'flag precision/recall 1.000'. Those numbers come from 10 cases written alongside the rules. Without the library number beside them, the claim goes beyond what the evidence supports, and the canonical pointer a panel opens says False.",
   "fix": "qa commits a library report regenerated at the gate commit and the live latest.json. The product note reports golden and library side by side, naming the conflict categories not covered (SCOPE_CUTS 13).",
   "acceptance_test": "evals/reports/library-latest.md source commit equals the gate tag; evals/reports/latest.json ship_bar_met True with backend claude-cli; the note draft cites both numbers."},
  {"severity": "minor", "title": "lib10: the internal notes drop the gap's paperwork caveat, and the flag is 'verified' although its start point is a claim form",
   "evidence": "journey-lib10.out notes: '- Gap: 43 days, July 14, 2026 to August 26, 2026: record 8 (Wardlaw Orthopedics, CMS-1500 ...)'. The UI explanation adds 'looks like paperwork ... the gap would be 49 days'; the flag state is 'verified'. D-062 already identifies CMS-1500 as a billing header.",
   "why_it_matters": "The attorney reads the notes, not the UI. They show an understated gap with no warning.",
   "fix": "The notes line carries the same caveat and the 49-day alternative. An endpoint that looks like paperwork makes the gap needs_review.",
   "acceptance_test": "lib10 export notes contain '49 days' and 'paperwork'; f_gap_r8_r9 state is needs_review."},
  {"severity": "minor", "title": "A counted ledger line prints the statement date where every other line puts the date of service (UX F4, carried, no card)",
   "evidence": "lib11-counted-letter.out: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00'. The line was held back because 'The line states no date of service'. board/cards/T-174.md:48 'letter statement dated wording ... not done'.",
   "why_it_matters": "The letter implies a service date that the record does not state.",
   "fix": "Write 'itemized ledger (statement dated June 15, 2026; no service date stated)'. Open a card.",
   "acceptance_test": "lib11 export with a3 counted contains 'statement dated' and not 'June 15, 2026: $180.00'."},
  {"severity": "minor", "title": "P0 card T-167 is blocked, against D-063 ('Only P0 cards ... proceed')",
   "evidence": "board.py list --status blocked: 'T-167 M3 backend blocked P0 AC 1/1 MVP backend wording'; note: 'moved changes_requested -> blocked ... re-check after T-166 lands'",
   "why_it_matters": "A P0 with no owner and no re-check is how the D-029 label regression slipped through. The wording work removed an honesty label.",
   "fix": "Re-dispatch T-167's check now that T-166 has landed, or close it with a decision.",
   "acceptance_test": "T-167 is done or cancelled with a D-entry before the M3 tag."},
  {"severity": "nit", "title": "D-061 and D-062 read as tuned to the sample: 'one simple rule' plus a second exemption, and a ban 'amended at implementation' because it 'zeroed the sample'",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:69 and :70",
   "why_it_matters": "A panel reading the decision log may see the golden case shaping the rule.",
   "fix": "In the Part 2 / prompt-log reading guide, summarize D-059..D-064 as one arc (default-deny, then a named human count) and give the sample-driven amendment as an explicit trade-off.",
   "acceptance_test": "The reading guide has one paragraph naming D-059..D-064 and the residuals 7d-7g."}
 ],
 "whats_right": [
  "Sample end to end holds every trap: 73-day gap flagged, 28-day not, accident dates not merged, $185 never totaled, letter equals golden, export blocked until something is accepted.",
  "Default-deny charges plus a named 'Count this charge': lib10 UB-04 totals $8,123.50 as expected, and totals, payments and adjustments are listed in the notes with plain reasons.",
  "Regression discipline holds: no prompt or lexicon change since the live run at 312efe6, and the fixture eval at d0b04bc reproduces every measurable live number."
 ],
 "questions_for_chris": [
  "Appendix A says 'pick at most one' stretch item; the build now ships all four (side-by-side viewer, PDF/OCR, calibrated confidence, draft paragraph). Present all four in the note with your reason, or show only the side-by-side viewer in the submitted demo? Assumption until you answer: side-by-side stays on, the draft paragraph defaults off, and the note names the rest as built-after-the-timebox at your request.",
  "Should the public demo replay the team's hand-checked sample answers (byte-exact letter, labeled as prepared by the team) or the recorded live model answers (labeled AI, wording may differ from the golden)? Assumption: the hand-checked set with an honest label."
 ]}
```
01-lib11-top.png
02-lib11-e2-row.png
03-lib11-after-accept-e2.png
04-sample-top.png
curated_provenance.py
fixture-eval-d0b04bc.md
journey-lib08.out
journey-lib10.out
journey-lib11.out
journey-sample.out
journey.py
lib11-counted-letter.out
lib_missed.py
lib_sweep.out
lib_sweep.py
library-d0b04bc.md
sample-e1-trace.out
sample-narrative-letter.out
sample-narrative-structure.out
ui_walk.out
ui_walk.py
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
0c4284f docs(orchestrator): D-065 honest demo provenance (amends D-029)
d0b04bc test(qa): T-045 M3 sensors re-run on a clean HEAD worktree (unit 5689, e2e 411, letter_check 0, calibration fresh, fixture eval matches live); latest.json stale-pointer finding
4510dc2 test(e2e): T-045 keyboard-only and 375px whole journeys, adversarial inputs through the browser (LLM counter 0), R-EX-1 letter matrix over 10 cases x 3 profiles, ladder gate for notes, two library cases side by side; declare T-174 test ids
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:17.312Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/GATE-M3-pm/sample-e1-trace.out | head -60; grep -rn \"claude-sonnet-5-5\\|recorded AI\\|AI draft\\|AI drafted\\|recorded_from\\|The AI read this\" app --include=*.py --include=*.js --include=*.html | grep -v \"^app/llm/prompts\" | head -60; ls tests/fixtures/llm/curated | head -5; python3 -c \"\nimport json,glob\nf=sorted(glob.glob('tests/fixtures/llm/curated/*.json'))[0]\nd=json.load(open(f));print(f,{k:(v if k!='response' else '...') for k,v in d.items()})\""
}
````

### User / tool · 2026-11-02T20:09:17.438Z

**tool result**
````
- AI drafted a summary and picked a quote | The AI read this record and proposed a one-line summary and a quote. | {"model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null}, "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1
- Quote is word for word in the record | The quote was found in the record, character for character. | {"excerpt": {"record_id": "r1", "start": 180, "end": 312, "text": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
- Quote is made of whole sentences | The quote starts and ends on whole sentences. | {}
- Quote keeps the hedge sentence that qualifies it | No hedge sentence that qualifies the quote is left out. | {}
- Numbers and dates in the summary are in the quote | Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote. | {"tokens": []}
- Summary keeps the quote's qualifiers | Every hedge, attribution, negation, side and approximation in the quote is in the summary. | {}
- Quote can be highlighted in the record | The quote's position in the record was found, so it can be highlighted. | {}
- Date of service is confirmed | The date comes from the record's own header and is parsed or confirmed. | {"date": {"record_id": "r1", "date_raw": "2026-01-09", "date_iso": "2026-01-09", "date_status": "parsed", "candidates": []}}
- Record has no instruction-like text | The record has no instruction-like text. | {}
- Second AI check: is the summary supported by the quote? | The second check found every statement in the summary in the quote. | {"model": {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "636239bec8cb1f0bedd4a1dec8e691ef3e4d43c35ee74fae0b
- Your decision | You accepted this item. | {"action": "accept", "at": "2026-11-02T20:00:21Z", "events": [{"action": "accept", "at": "2026-11-02T20:00:21Z", "before": {"edited": null, "review_status": "pending"}, "after": {"edited": null, "revi
app/llm/_types.py:34:    recorded_from: dict = field(default_factory=dict)
app/llm/audited.py:104:                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
app/llm/audited.py:134:    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}
app/llm/backends/fixture.py:33:                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})
app/llm/backends/fixture.py:42:           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
app/frontend/mock_extra.js:21:        calls.push(Object.assign({ id: "c" + i * 2, role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", prompt_sha256: "9f2c0a77" + i, item_id: e.id, attempt: 1, latency_ms: 5120, cost_usd: 0.0041, tokens_in: 812, tokens_out: 150, parsed_ok: true, verdict: null },
app/frontend/stepper.js:41:    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
app/frontend/stepper.js:149:  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
app/frontend/stepper.js:151:  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
app/frontend/stepper.js:385:      kv("recorded from", ev.recorded_from && ev.recorded_from.backend), kv("latency", ev.latency_ms != null ? ev.latency_ms + " ms" : null), kv("parsed", ev.parsed_ok == null ? null : ev.parsed_ok ? "yes" : "no"));
app/frontend/audit.js:21:    const rf = c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
app/frontend/timeline.js:268:            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
app/frontend/mock.js:72:      generator: { model: "claude-sonnet-5-5", prompt_version: "extract_v1", call_id: "c" + id, recorded_from: { backend: "claude-cli", model: "claude-sonnet-5-5", recorded_at: "2026-11-02T00:50:00Z" }, output: { summary: opts.summary, excerpt: ex.text } },
app/frontend/mock.js:118:    const c = { token, name, status: "ingested", demo_mode: false, backend: "fixture", models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, records,
app/frontend/mock.js:146:        models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, limits: { max_chars: MAX_CHARS, max_records: 40 }, retention_hours: 24,
app/frontend/mock.js:181:          calls: [{ id: "c1", role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", attempt: 1, latency_ms: 5120, parsed_ok: !(it.state === "rejected"), verdict: null },
app/frontend/app.js:13:    badge.textContent = demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
app/frontend/app.js:14:    badge.title = demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
app/frontend/dom.js:52:  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
app/backend/why.py:17:    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
app/backend/trace.py:179:        for k in ("prompt_sha256", "backend", "recorded_from", "latency_ms", "parsed_ok"):
app/backend/trace.py:290:    if gated:      # whose words: only the paralegal's own summary is "your wording"; an AI draft is "this summary"
app/backend/trace.py:386:        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
app/backend/trace.py:394:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
app/backend/trace.py:397:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
app/backend/trace.py:401:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL,
app/backend/trace.py:405:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
app/backend/trace.py:406:                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
app/backend/trace.py:1056:        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PENDING, "The AI run has not started.", rule="row 4", counts=ecounts, next_action=na("RERUN")))
app/backend/trace.py:1060:        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no AI-made entry. "
app/backend/trace.py:1064:        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PASS, f"The AI drafted an entry for all {len(firsts)} records.", rule="row 4", counts=ecounts))
app/backend/present.py:448:    rf = c.get("recorded_from")
app/backend/present.py:449:    d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": c["model"],
app/backend/api.py:124:        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
app/backend/api.py:590:                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
app/backend/judges.py:12:DEFAULT_GENERATOR_MODEL = "claude-sonnet-5-5"
0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
228350fb06e4cf872348f390212b959eebee7313b76f0edf051977846aacbc56.json
37318d752543b06d4add14f3ab3aa71dc4e089522d392b500a6057b9fc790d1d.json
3e70853a6fadff0e4991350de156ea38d30b396597dbab5bc74601b2508eb6d7.json
tests/fixtures/llm/curated/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json {'CURATED': 'CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).', 'output': {'excerpt': 'New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.', 'summary': 'New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.'}, 'recorded_from': {'backend': 'curated', 'model': 'hand-checked (qa)', 'recorded_at': '2026-11-02T02:46:58Z'}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:20.146Z

**tool call — Bash**
````
{
 "command": "cat app/llm/backends/fixture.py; sed -n 60,175p app/llm/audited.py; python3 -c \"\nimport json,glob\nf=sorted(glob.glob('tests/fixtures/llm/recorded/*.json'))[0]\nd=json.load(open(f));print(list(d), d.get('recorded_from'))\""
}
````

### User / tool · 2026-11-02T20:09:20.266Z

**tool result (error)**
````
Exit code 1
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p
    return "VALIDATION_FAILED" if isinstance(e, ValueError) else type(e).__name__


def role_for(step: str) -> str:
    s = str(step)
    return "judge" if s.startswith("judge") or (len(s) == 2 and s[0] == "j" and s[1].isdigit()) else "generator"


def _t(now):
    return now() if callable(now) else (time.time() if now is None else now)


def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
    cwm = complete_with_meta or P.complete_with_meta
    last_err = "unknown"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        u = user + _RETRY_NOTES[attempt - 1]
        h = P.prompt_hash(model, system, u, json_schema)
        t0 = time.monotonic()
        res, err, fixture_miss, bug = None, None, False, None
        try:
            with (T.lenient_json() if step in LENIENT_JSON_STEPS else contextlib.nullcontext()):
                res = cwm(model, system, u, json_schema)
            if validate is not None:
                try:
                    validate(res.output)
                except RETRYABLE_VALIDATION_ERRORS as e:
                    err = _error_code(e)               # schema-invalid output: a failed attempt, retried with a stricter note
        except P.FixtureMissing as e:
            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
        except RETRYABLE_PROVIDER_ERRORS as e:          # only our own error codes are stored, never model- or record-derived text
            err = _error_code(e)
        except Exception as e:                         # a bug in our code: keep the row (class name only), then let it propagate below
            err, bug = _error_code(e), e
        ms = int((time.monotonic() - t0) * 1000)
        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(res.model_resolved if res and res.model_resolved else model),
                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
                      parsed_ok=1 if err is None else 0, error=err)
        if item_id:
            fields["item_id"] = item_id
        if res:
            import json as _j
            fields.update(cost_usd=res.cost_usd, tokens_in=res.tokens_in, tokens_out=res.tokens_out,
                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
        with _DB_LOCK:
            call_id = DB.add_llm_call(conn, case_id, u, (res.raw or _dump(res.output)) if res else None, now=_t(now), system=system, **fields)
        if err is None:
            return res.output, call_id
        if bug is not None:
            log.error("llm call raised a programmer error call_id=%s step=%s class=%s", call_id, step, type(bug).__name__)
            raise bug
        last_err = err
        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
        if fixture_miss:
            raise LLMFailedFixtureMiss(h)
        if sleep is not None and attempt < MAX_ATTEMPTS:
            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed", last_error=(last_err or "LLM_ERROR").split()[0])


def _dump(o):
    import json
    return json.dumps(o, sort_keys=True)


PROMPT_OF_STEP = {"extract": "extract_v1", "j1": "judge_faithfulness_v1", "j2": "judge_amount_class_v1", "j3": "judge_conflict_v6",
                  "j4": "judge_flag_v3", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
PROMPT_OF_STEP.update({"extract_es": "extract_es_v1", "judge_faithfulness_es": "judge_faithfulness_es_v1"})     # Spanish records (D-042, T-085)


def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}

    def call(step, system, user, schema, *, item_id=None, validate=None):
        # a live backend that just failed (rate limit, timeout) is retried after a short pause, not at once (T-075); the fixture backend never sleeps
        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate,
                            prompt_version=PROMPT_OF_STEP.get(step), sleep=None if P.backend_name() == "fixture" else time.sleep)
    return call
Traceback (most recent call last):
  File "<string>", line 3, in <module>
IndexError: list index out of range
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:20.898Z

**tool call — Bash**
````
{
 "command": "sed -n 370,420p app/backend/trace.py; sed -n 435,470p app/backend/present.py; sed -n 575,600p app/backend/api.py; grep -n \"def trace_for\\|def .*calls\\|llm_calls\" app/backend/trace.py | head -20"
}
````

### User / tool · 2026-11-02T20:09:21.010Z

**tool result**
````
def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    # D-051: all five code checks (and the highlight) are recomputed from the CURRENT summary and quote, as accept does, and also honour what was stored
    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
    placeholder = lad.get("failure")                      # could-not-verify tray placeholder: the AI made no usable summary, so there is no quote to check (T-112 r2)
    verbatim_fail = not placeholder and ("GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False or "GROUNDING_EXCERPT_NOT_VERBATIM" in live)
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else (placeholder or ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None))
    st = []
    # 1 extracted
    if lad.get("entered_by"):
        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
                       evidence={"excerpt": exc}))
    else:
        gen = lad.get("generator") or {}
        call = cx.call(gen.get("call_id"), row["id"], "extract")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
        ev["excerpt"] = exc
        if schema_fail:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
                           evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "LLM_FAILED_AFTER_RETRIES" in R:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
                           rule="row 4", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "SUMMARY_NOT_IN_QUOTE" in R:                     # D-054: code removed every clause; the notes say which
            ev["removed"] = (lad.get("summary_trim") or {}).get("removed") or []
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL,
                           " ".join((lad.get("summary_trim") or {}).get("notes") or []) + " " + reason_text("SUMMARY_NOT_IN_QUOTE"), reason="SUMMARY_NOT_IN_QUOTE",
                           rule="D-054", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        else:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
            trim = lad.get("summary_trim")
            if trim and trim.get("removed"):                  # D-054: shown, never silent. The judge saw the trimmed summary.
                st.append(step("summary_trimmed", "Code removed summary parts the quote does not support", "code", PASS, " ".join(trim.get("notes") or []),
                               rule="D-054", evidence={"removed": trim["removed"], "original_summary": trim.get("original_summary"), "kept_summary": trim.get("kept_summary")}))
            st.extend(_narrow_steps(lad, row))                # T-139: code shortened the AI's quote / removed an amount clause; shown, never silent, never in the letter
    st.extend(_edit_trim_steps(row))                          # T-139: the quote-picker edit removed the amount clause from the AI summary

    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
        if stop:
            st.append(_skipped(sid, label, "code", stop, rule))
        elif failed if failed is not None else code in R:
            st.append(step(sid, label, "code", FAIL, reason_text(code), reason=code, rule=rule, evidence=evidence, next_action=fail_na))
        else:
            st.append(step(sid, label, "code", PASS, ok_text, rule=rule, evidence=evidence))
    seen, src = set(), []
    for rid in ids:
        if rid in recs and rid not in seen:
            seen.add(rid)
            r = recs[rid]
            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
    calls = [_call(c) for c in DB.list_llm_calls(conn, case_id, item_id)]
    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
    return {"item": item, "source": src, "calls": calls, "events": events}


def _call(c, full=False):
    rf = c.get("recorded_from")
    d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": c["model"],
         "prompt_version": c["prompt_version"], "prompt_sha256": c["prompt_sha256"], "item_id": c["item_id"], "attempt": c["attempt"],
         "latency_ms": c["latency_ms"], "cost_usd": c["cost_usd"], "tokens_in": c["tokens_in"], "tokens_out": c["tokens_out"],
         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"]}
    if full:
        d.update(system_text=c["system_text"], user_text=c["user_text"], response_raw=c["response_raw"], error=c["error"])
    return d


def audit_view(conn, case_id, full=False):
    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
    calls = DB.list_llm_calls(conn, case_id)
    by = {}
    for c in calls:
        by[c["backend"]] = by.get(c["backend"], 0) + 1
    return {"token": case_id, "calls": [_call(c, full) for c in calls],
            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
                        **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)
                        **({"before": e["before"], "after": e["after"]} if full else {})}
                       for e in DB.list_events(conn, case_id)],
            "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
                        "latency_ms_total": sum(c["latency_ms"] or 0 for c in calls), "by_backend": by}}
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case, style=style)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": present.rejected_count(c, token)}
            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}/trace")
    def item_trace(token: str, item_id: str):
        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
        c = conn()
141:        calls = DB.list_llm_calls(conn, case_id)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:25.906Z

**tool call — Bash**
````
{
 "command": "grep -n \"\\\"generator\\\"\\|'generator'\\|call_id\" app/backend/*.py | grep -v \"^app/backend/trace.py\" | head -40; grep -n \"def _llm_evidence\" -A25 app/backend/trace.py; grep -n \"def call\\b\" -B2 -A12 app/backend/trace.py | head -40; ls tests/fixtures/llm/; ls tests/fixtures/llm/recorded | head -3"
}
````

### User / tool · 2026-11-02T20:09:26.036Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:29.789Z

**tool call — Bash**
````
{
 "command": "sed -n 40,70p app/backend/generator.py; grep -n \"ladder\" app/backend/present.py | head -30; grep -n \"ladder\\|AI draft\\|ai_draft\\|entered_by\" app/frontend/*.js | grep -v \"mock\" | head -50; grep -n \"recorded_from\\|llm_calls\" app/db/*.py | head -20"
}
````

### User / tool · 2026-11-02T20:09:29.901Z

**tool result**
````
    return {"id": f"e{record['n']}", "seq": record["n"], "record_id": record["id"], "record_ids": [f"r{n}" for n in group],
            "date": record.get("date_iso"), "date_status": record.get("date_status", "parsed"),
            "provider": record["source"], "ai_drafted": True, "review_status": "pending"}


def extract_one(record: dict, group: list, *, call, case_text: str = "") -> dict:
    """One generator call. Returns an entry dict (pre-judge) or {'failure': code, 'record_no': n} when no output exists."""
    lang = language.record_lang(record)
    if lang == "other":                                   # D-042: only English and Spanish are read; say so, never guess
        return {"failure": "UNSUPPORTED_LANGUAGE", "record_no": record["n"]}
    step, item = (spanish.EXTRACT_STEP if language.is_translated(lang) else "extract"), f"e{record['n']}"
    n = promptlib.nonce(case_text, step, item)
    prompt = promptlib.load(spanish.EXTRACT_PROMPT if language.is_translated(lang) else "extract_v1")
    try:
        out, call_id = call(step, prompt.text, extract_prompt(record, n), schemas.ExtractOutput.model_json_schema(), item_id=item)
    except P.FixtureMiss:
        return {"failure": "FIXTURE_MISS", "record_no": record["n"]}
    except AU.LLMFailed:
        return {"failure": "LLM_FAILED_AFTER_RETRIES", "record_no": record["n"]}
    e = _entry_base(record, group, case_text)
    e["ladder"] = {"item_id": e["id"], "generator": {"model": judges.generator_model(), "prompt_version": prompt.name,
                                                      "call_id": call_id, "output": out if isinstance(out, dict) else None},
                   "judge": None, "code_checks": {}, "human": {"action": None, "edited_text": None, "at": None}}
    if language.is_translated(lang):                      # the quote stays in the original language; the summary is a labelled AI translation (D-042)
        e["ladder"]["translation"] = spanish.translation_info(lang)
    try:
        o = schemas.ExtractOutput.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
        return compose(e, record, grounding_failures=["SCHEMA_INVALID"], schema_valid=False)
    def shape(excerpt):
28:def _ladder(row):
29:    lad = dict(row.get("ladder") or {"item_id": row["id"]})
39:    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
44:    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
45:            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
46:            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
54:            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
55:            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
63:    t = (row.get("ladder") or {}).get("translation")
75:    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
82:    demoted = ((row.get("ladder") or {}).get("reclassification") or {}).get("to") == "unclear"
137:    counted = bool((row.get("ladder") or {}).get("counted"))
397:             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
402:                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
405:                "ladder": {"item_id": x["id"], "state": "rejected"}}
app/frontend/dom.js:52:  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
app/frontend/dom.js:57:  ZL.secondCheckPending = (i) => !!i && (i.second_check_pending !== undefined ? i.second_check_pending === true : i.ai_drafted === true && !ZL.wordingEdited(i) && (i.reasons || []).includes("JUDGE_UNAVAILABLE"));
app/frontend/judges.js:47:  const humanWording = (it) => { if (!unchecked(it) || blocking(it)) return false; const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return reviewOf(it) === "edited" || !!(f && f.item.ai_drafted === false); };
app/frontend/review.js:646:      if (entry.entered_by_reviewer || /reviewer/i.test(entry.entered_by || "")) {   // typed by the paralegal, not drafted by the model
app/frontend/stepper.js:41:    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
app/frontend/stepper.js:149:  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
app/frontend/stepper.js:150:  const mine = (id) => { const f = id && caseNow() && rv() && rv().find(caseNow(), id); return !f || f.kind !== "entry" || f.item.ai_drafted === false || f.item.review_status === "edited"; };
app/frontend/stepper.js:151:  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
app/frontend/timeline.js:61:      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
app/frontend/timeline.js:259:      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
app/frontend/timeline.js:264:        el("details", { class: "zs-more" }, el("summary", {}, "Recorded ladder (raw state and checks)"), el("dl", { class: "kv", "data-testid": "why-ladder" },
app/frontend/timeline.js:268:            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
app/db/db.py:25:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
app/db/db.py:269:    _insert(conn, "llm_calls", row)
app/db/db.py:274:    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
app/db/db.py:278:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
app/db/db.py:279:    q, a = "SELECT * FROM llm_calls WHERE case_id=?", [case_id]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:33.597Z

**tool call — Bash**
````
{
 "command": "grep -rn \"AI draft\\|recorded AI\\|Drafted by AI\\|Demo: \" app/frontend/*.js app/frontend/*.html tests --include=* -l 2>/dev/null | head -30; grep -rn \"ai_drafted\" app/frontend/*.js | grep -v mock | head -20; ls tests tests/e2e | head -50; cat tools/serve_app.sh | wc -l"
}
````

### User / tool · 2026-11-02T20:09:33.726Z

**tool result**
````
app/frontend/app.js
app/frontend/dom.js
app/frontend/stepper.js
app/frontend/timeline.js
tests/unit/test_trace.py
tests/unit/test_t138_undo_edit.py
tests/e2e/test_edit_to_check.py
tests/e2e/test_code_check_refusal.py
tests/e2e/test_stepper.py
tests/e2e/conftest.py
tests/e2e/test_mvp_polish.py
app/frontend/dom.js:57:  ZL.secondCheckPending = (i) => !!i && (i.second_check_pending !== undefined ? i.second_check_pending === true : i.ai_drafted === true && !ZL.wordingEdited(i) && (i.reasons || []).includes("JUDGE_UNAVAILABLE"));
app/frontend/judges.js:47:  const humanWording = (it) => { if (!unchecked(it) || blocking(it)) return false; const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return reviewOf(it) === "edited" || !!(f && f.item.ai_drafted === false); };
app/frontend/stepper.js:150:  const mine = (id) => { const f = id && caseNow() && rv() && rv().find(caseNow(), id); return !f || f.kind !== "entry" || f.item.ai_drafted === false || f.item.review_status === "edited"; };
app/frontend/timeline.js:61:      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
tests:
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit

tests/e2e:
__init__.py
__pycache__
_scripted_server.py
conftest.py
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
test_rerun_judge.py
test_rerun_note.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
       8
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:37.441Z

**tool call — Bash**
````
{
 "command": "grep -rn \"AI draft\\|recorded AI\\|Drafted by AI\\|Demo: \" app/frontend/dom.js app/frontend/stepper.js tests/unit/test_trace.py tests/e2e/*.py | cut -c1-220; sed -n 30,50p app/frontend/stepper.js; sed -n 1,40p tests/e2e/conftest.py; grep -rn \"tag.*ai\\|\\[data-icon=.ai\" app/frontend/*.css | head"
}
````

### User / tool · 2026-11-02T20:09:37.545Z

**tool result**
````
app/frontend/dom.js:52:  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
app/frontend/stepper.js:41:    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
app/frontend/stepper.js:149:  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
app/frontend/stepper.js:151:  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
tests/unit/test_trace.py:1181:# ---- D-051 / T-098 r2: the code rung binds accept for every item, AI-made or human (reviewer F1: an AI draft 'Pain 5/10' over a quote without 5/10)
tests/unit/test_trace.py:1413:    DB.apply_review(conn, ai, "accept", now=9e9, case=tok)                                            # an accepted AI draft that fails a check (old data)
tests/e2e/conftest.py:18:  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you ne
tests/e2e/conftest.py:38:  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quot
tests/e2e/test_code_check_refusal.py:164:    """Real backend: an accepted AI draft whose summary then fails a code check is a gate blocker; the case verdict is the backend's words, in the rail and in the panel."""
tests/e2e/test_code_check_refusal.py:176:    assert "This summary doesn't match the quote:" in blocker.inner_text() and "Your wording" not in blocker.inner_text(), "the paralegal did not write an AI draft"
tests/e2e/test_code_check_refusal.py:331:    """Accept the item (AI draft), break its quote in the store, open the Why dialog. rewrite_label rewrites the item trace's verdict label (a stub of what the backend sends)."""
tests/e2e/test_code_check_refusal.py:360:    """An AI draft whose trace the backend labels 'your wording' reads 'Your wording...'; the same item labelled 'this summary' reads 'This summary...'."""
tests/e2e/test_edit_to_check.py:294:    assert got["ai_drafted"] and "JUDGE_UNAVAILABLE" in got["reasons"] and "summary" not in (got.get("edited") or {}), "the setup: an AI draft, quote re-picked, second check never answ
tests/e2e/test_mvp_polish.py:262:    expect(page.locator("#badge")).to_have_text(re.compile(r"^(Demo: recorded AI answers|)$"))
tests/e2e/test_stepper.py:66:    """Why? shows an ordered list of steps with a status word, a kind chip (Code / AI draft / AI check / You) and the plain-words why."""
    steps.forEach((st) => { n[statusInfo(st).cat] += 1; });
    const bits = [[n.pass, "passed"], [n.fail, "failed"], [n.need, n.need === 1 ? "needs you" : "need you"], [n.wait, "not done yet"], [n.skipped, "skipped"]].filter(([k]) => k).map(([k, w]) => k + " " + w);
    return bits.join(", ");
  }
  S.progressLabel = progressLabel;
  const VERDICT_WORD = { supported: "Supported", partially: "Partly supported", unsupported: "Not supported", disagrees: "Disagrees", unsure: "Could not decide", unavailable: "Unavailable" };
  S.verdictWord = (v) => VERDICT_WORD[v] || v || "";
  const kindOf = (st) => {
    if (st.kind === "human") return "You";
    if (st.kind === "code") return "Code";
    const m = st.evidence && st.evidence.model;
    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
  };
  const humanize = (k) => String(k).replace(/_/g, " ");
  const rv = () => ZL.rv;
  const caseNow = () => ZL.state.get().case;
  const recSeq = (id) => { const r = ((caseNow() || {}).records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, ""); };

  // ---- labels for items (entry: date and provider; amount: the figure; flag: its title)
  const extraLabels = {};   // narrative sentences register their own label ("ns1" -> first words of the sentence)
  S.setLabel = (id, text) => { const t = String(text || "").trim(); extraLabels[id] = t.length > 60 ? t.slice(0, 57).replace(/\s+\S*$/, "") + "…" : t; };
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
app/frontend/styles.css:96:[data-icon="pencil"]::before { content: "\270E"; } [data-icon="dash"]::before { content: "\2296"; } [data-icon="ai"]::before { content: "AI"; width: auto; } [data-icon="calendar"]::before { content: "\25F7"; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:53.627Z

**tool call — Bash**
````
{
 "command": "sed -n 20,70p app/backend/present.py; grep -n \"present\\.\\(case_view\\|entry_view\\|item_view\\|item_detail\\)\\|def case_view\\|def item_view\\|def item_detail\\|def get_case\\|def entry_view\" app/backend/*.py | head -20; grep -n \"def cx\\|class Cx\\|def call(self\" -A12 app/backend/trace.py | head -60"
}
````

### User / tool · 2026-11-02T20:09:53.725Z

**tool result**
````
def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    lad.pop("pre_edit", None)      # T-138: the undo snapshot is internal (api.md), never in a payload
    return lad


def rerun_available(row) -> bool:
    """T-157: whether "run the second check again" can get an answer for this item: no in demo / fixture mode (no live model), no after a rerun that got no answer, yes otherwise."""
    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
            "rerun_available": rerun_available(row)}      # T-146 r3: set when a re-run disagreed with or failed on this decided item


def entry_view(row, recs):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None, "translation": _translation(row),
            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter


def _translation(row):
    """D-042: set on an entry made from a Spanish record: its summary is an English translation, its quote the original Spanish."""
    t = (row.get("ladder") or {}).get("translation")
    return spanish.translation_info(t.get("source_language", "es"), "summary" in (row.get("edited") or {}) or bool(t.get("human_written"))) if t else None


def accept_effect(row) -> str:
    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
    never totaled, and no second AI check is needed), `internal_notes` (estimate, unclear: noted for the paralegal, never in the total)."""
    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
app/backend/api.py:141:    def get_case(c, token):
app/backend/api.py:350:    def get_case_view(token: str):
app/backend/api.py:354:            v = present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
app/backend/case_list.py:180:        return {"item_id": w["id"], "kind": w["kind"], "reason": present.item_view(conn, case_id, w["id"])["why"]}
app/backend/reclassify.py:230:    return {"item": present.item_view(conn, case_id, item_id), "amount": amount, "totals": present.totals_view(conn, case_id),
app/backend/present.py:50:def entry_view(row, recs):
app/backend/present.py:245:def item_view(conn, case_id, item_id):
app/backend/present.py:385:def case_view(conn, case_id, *, backend, models, demo_mode):
app/backend/pipeline.py:666:def case_view(out: dict) -> dict:
app/backend/review.py:49:    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
app/backend/review.py:297:    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
app/backend/review.py:683:    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
app/backend/review.py:747:    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
160:    def call(self, call_id, item_id=None, step_name=None):
161-        if call_id and call_id in self.call_by_id:
162-            return self.call_by_id[call_id]
163-        if item_id and step_name:
164-            hits = [c for c in self.calls_by_item.get(item_id, []) if c["step"] == step_name]
165-            return hits[-1] if hits else None
166-        return None
167-
168-
169-def _span(cx, rid, start, end, text):
170-    return {"record_id": rid, "start": start, "end": end, "text": text}
171-
172-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:09:55.959Z

**tool call — Bash**
````
{
 "command": "sed -n 240,275p app/backend/present.py; sed -n 385,432p app/backend/present.py; grep -n \"def _llm_evidence\" -A30 app/backend/trace.py | head -50; sed -n 130,160p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T20:09:56.112Z

**tool result**
````
        records = records if records is not None else store.load_records(conn, case_id)
        return amount_view(row, recs, records, pool if pool is not None else CountPool(conn, case_id, records))
    return _VIEW[kind](row, recs)


def item_view(conn, case_id, item_id):
    row = DB.get_item(conn, item_id, case_id)
    kind = _ID_KIND[item_id[0]]
    v = view_of(kind, row, conn, case_id, _recs_by_id(conn, case_id))
    v["kind"] = kind
    v["second_check_pending"] = item_id in second_check_pending_ids(conn, case_id)
    if kind == "entry":
        review.hold_hints(conn, case_id, [v])      # T-139 r3: the held-out hint says where this record's figures are counted
    if kind == "flag":
        _with_gap_changes(conn, case_id, [v])
    return v


def second_check_pending_ids(conn, case_id) -> set:
    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
    acknowledges it, no check needed). Lazy import: trace imports this module."""
    from app.backend import trace
    return {u["item_id"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u["kind"], u["row"])}


def all_items(conn, case_id):
    recs = _recs_by_id(conn, case_id)
    records = store.load_records(conn, case_id)      # D-064: the amounts' not-counted reasons read the record body, source and date
    pool = CountPool(conn, case_id, records)
    out = {k: [view_of(k, r, conn, case_id, recs, records, pool) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
    review.hold_hints(conn, case_id, out["entry"])      # T-139 r3
    pend = second_check_pending_ids(conn, case_id)
    for k in ("entry", "amount", "flag"):
        for v in out[k]:
            v["second_check_pending"] = v["id"] in pend
    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
def case_view(conn, case_id, *, backend, models, demo_mode):
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = list(_recs_by_id(conn, case_id).values())
    its = all_items(conn, case_id)
    ents = its["entry"]
    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))      # T-110 r2: a record the paralegal entered by hand leaves the tray
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
    def _tray_flag(x):
        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
                "flag": {"type": x["type"], "category": x["category"]},
                "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
                "ladder": {"item_id": x["id"], "state": "rejected"}}
    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
    rules = []
    for cat in sorted({x["category"] for x in filtered}):
        ref, name, text = FT.FILTER_RULES.get(cat, ("", cat, ""))
        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
        rules.append({"rule": cat, "ref": ref, "label": name, "explanation": text, "count": len(items), "items": items})
    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    record_views = [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs]
    uncovered.attach(record_views, ents, quote_body)      # T-143: clinical sentences no entry quote covers (review aid; never in the letter or notes)
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": record_views, "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
            "review": review_view(conn, case_id), "warnings": generator.hand_entered_warnings(DB.list_items(conn, case_id, "entry")), "error": err,
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
            **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}


def why_view(conn, case_id, item_id):
    item = item_view(conn, case_id, item_id)
173:def _llm_evidence(cx, role, model, prompt_version, call):
174-    ev = {"model": {"id": (call or {}).get("model") or model, "role": role,
175-                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"]}}
176-    ev["prompt_version"] = (call or {}).get("prompt_version") or prompt_version
177-    if call:
178-        meta = present._call(call, cx.full)
179-        for k in ("prompt_sha256", "backend", "recorded_from", "latency_ms", "parsed_ok"):
180-            ev[k] = meta.get(k)
181-        ev["call_id"] = call["id"]
182-        if cx.full:
183-            ev["response_raw"] = meta.get("response_raw")
184-    return ev
185-
186-
187-def _norm_verdict(step_id, v):
188-    if v in _LADDER_VOCAB:
189-        return v
190-    return _RAW_TO_LADDER.get(v, "unsure")
191-
192-
193-def _judge_reason_code(jd, call):
194-    code = (jd or {}).get("reason_code")
195-    if code:
196-        return code
197-    if call and call.get("response_raw"):
198-        try:
199-            got = json.loads(call["response_raw"])
200-            if isinstance(got, dict) and isinstance(got.get("reason_code"), str):
201-                return got["reason_code"]
202-        except (ValueError, TypeError):
203-            pass

class UnknownItem(KeyError):
    """The item id is not in this case (the API maps exactly this to 404)."""


class _Cx:
    def __init__(self, conn, case_id, full):
        self.conn, self.case_id, self.full = conn, case_id, bool(full)
        self.case = DB.get_case(conn, case_id)
        self.recs = present._recs_by_id(conn, case_id)
        self._live_recs = None
        calls = DB.list_llm_calls(conn, case_id)
        self.call_by_id = {c["id"]: c for c in calls}
        self.calls_by_item = {}
        for c in calls:
            self.calls_by_item.setdefault(c["item_id"], []).append(c)
        self.events = {}
        for e in DB.list_events(conn, case_id):
            self.events.setdefault(e["item_id"], []).append(e)
        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
        self.ran = self.case.get("run_started_at") is not None
        self.running = self.case["status"] == "running"

    @property
    def live_recs(self):
        """store.load_records() dicts (they carry the record body, source and language the code checks need), loaded once per context."""
        if self._live_recs is None:
            self._live_recs = store.load_records(self.conn, self.case_id, self.case["raw_text"])
        return self._live_recs

    def call(self, call_id, item_id=None, step_name=None):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:03.831Z

**tool call — Bash**
````
{
 "command": "grep -n \"_llm_evidence(\" app/backend/trace.py; grep -n \"narrative\" app/backend/api.py | head -5; ls tests/fixtures/llm/recorded | wc -l; ls tests/fixtures/llm | head; python3 - <<'E'\nimport json,glob,collections\nc=collections.Counter()\nfor f in glob.glob('tests/fixtures/llm/recorded/*.json'):\n    d=json.load(open(f)); rf=d.get('recorded_from') or {}\n    c[(rf.get('backend'),rf.get('model'))]+=1\nprint(c)\nE"
}
````

### User / tool · 2026-11-02T20:10:03.964Z

**tool result**
````
173:def _llm_evidence(cx, role, model, prompt_version, call):
223:    ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or JUDGE_PROMPT[jid], call)
391:        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
679:        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
746:    ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
767:        ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or "judge_faithfulness_v1", jcall)
24:from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
498:    @app.get("/api/cases/{token}/narrative")
499:    def narrative_get(token: str):
503:            return {"narrative": narrative.get(c, token)}
507:    @app.post("/api/cases/{token}/narrative")
ls: tests/fixtures/llm/recorded: No such file or directory
       0
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
00e8d38a3d50d7d1d7a9b7431c6c2c1970b32930a2583c8a3acd58fdced43d2f.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
0115c20756060b7547d09ea7174734c62c4d2c54f0cc9840da3f4be1c00e19bb.json
03b065e9490648fde69d807c3f2719201ad149f6e41700f46c81c4258230b20a.json
03dca54059c1c53788cc6e6b66442c557959bc4443f86f86120412b8a7cf4b29.json
03f7de3945171cd4ccf7eed0a80ad8642913484686561e412ec1b8ee9a064d66.json
040a1015f827bfd1c0d6e0f5503b0004a738ca0871d71642a96e5eacee82f28e.json
Counter()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:09.154Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport json,glob,collections\nc=collections.Counter()\nfor f in glob.glob('tests/fixtures/llm/*.json'):\n    d=json.load(open(f)); rf=d.get('recorded_from') or {}\n    c[(rf.get('backend'),rf.get('model'))]+=1\nprint(c)\nE\nsed -n 660,700p app/backend/trace.py; sed -n 735,775p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T20:10:09.313Z

**tool result**
````
Counter({('claude-cli', 'claude-haiku-5-5'): 790, ('claude-cli', 'claude-sonnet-5-5'): 418})
                           next_action=na("CONFIRM_DATE", {"view": "dates_to_confirm"})))
        else:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", PASS, "Both dates are parsed or confirmed.", rule="row 9"))
        st.append(inj())
        st += _ocr_steps(R, rid0)
        st.append(step("judge_not_needed", "Second AI check", "llm", SKIPPED, "Not needed: this is arithmetic over dates in the record, which code does exactly.", rule="row 9"))
        st.append(_human_step(cx, row, "flag"))
        return st
    has_llm, has_lex = origin in ("llm", "lexicon+llm"), origin in ("lexicon", "lexicon+llm")
    if ftype == "conflict":
        pass                                  # a conflict is the AI's pair proposal (row 11): no phrase list, so no agreement step
    elif has_lex:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", PASS, "The researched phrase list found this wording in the record.", rule="row 12", evidence={"spans": spans}))
    else:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", SKIPPED, reason_text("LLM_ONLY"), reason="LLM_ONLY", rule="row 12"))
    if has_llm:
        gen = lad.get("generator") or {}
        step_name = "conflicts" if ftype == "conflict" else "flags"
        call = cx.call(gen.get("call_id"), row["id"], step_name)
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
        st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
    else:
        st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
    if ftype == "conflict":
        pass
    elif has_llm and has_lex:
        st.append(step("agreement", "Phrase list and AI agree", "code", PASS, "Both the phrase list and the AI found this flag.", rule="row 12"))
    else:
        code = "LEXICON_ONLY" if origin == "lexicon" else "LLM_ONLY"
        if code in R:
            st.append(step("agreement", "Phrase list and AI agree", "code", FAIL, reason_text(code), reason=code, rule="row 12", next_action=na("COMPARE_BY_HAND", {"item_id": row["id"]})))
        else:
            other = next((c for c in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS") if c in R), None)
            st.append(step("agreement", "Phrase list and AI agree", "code", SKIPPED, reason_text(other) if other else "Only one source looked at this record, so there is nothing to compare.",
                           reason=other, rule="row 12"))
    if cat == "credibility_language":
        st.append(step("credibility_wording", "Credibility wording is not a clean negation", "code", PASS,
                       "The sentence uses a credibility term and is not a plain negation such as 'No Waddell signs', so it is flagged for you to see first.", rule="D-043"))
    vfail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or "SCHEMA_INVALID" in R or cc.get("excerpt_verbatim") is False
    if vfail:
        code = "SCHEMA_INVALID" if "SCHEMA_INVALID" in R else "GROUNDING_EXCERPT_NOT_VERBATIM"
    nar = narrative.get(cx.conn, cx.case_id) or {}
    sent = next((s for s in nar.get("sentences", []) if s["id"] == item_id), None)
    rem = next((s for s in nar.get("removed", []) if s["id"] == item_id), None)
    s = sent or rem
    if s is None:
        raise UnknownItem(item_id)
    reason = (rem or {}).get("reason")
    rcodes = list((rem or {}).get("reasons") or []) if reason not in ("NOT_AN_ACCEPTED_ENTRY",) and not str(reason).startswith("JUDGE_") else []
    st = []
    gen = nar.get("generator") or {}
    call = cx.call(gen.get("call_id"))
    ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
    ev["values"] = {"entry_id": s["entry_id"], "text": s["text"]}
    st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
    cited_ok = reason != "NOT_AN_ACCEPTED_ENTRY"
    st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
                   reason=None if cited_ok else "NOT_AN_ACCEPTED_ENTRY", rule="D-031", evidence={"values": {"entry_id": s["entry_id"]}},
                   next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]}) if not cited_ok else None))
    if not cited_ok:
        st.append(_skipped("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", "NOT_AN_ACCEPTED_ENTRY", "D-006", "Not run: the cited entry is not accepted."))
    elif rcodes:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", FAIL, " ".join(_ntext(c) for c in rcodes),
                       reason=rcodes[0], rule="D-006", evidence={"reasons": rcodes}, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
    else:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", PASS,
                       "Every number, date and qualifier is in the cited quote, and the sentence adds no cause, severity or flag wording.", rule="D-006", evidence={"reasons": []}))
    if not cited_ok or rcodes:
        st.append(_skipped("judge_1", "Second AI check: is the summary supported by the quote?", "llm", reason if not cited_ok else rcodes[0], "row 4"))
    else:
        jd = s.get("judge") or {}
        verdict = jd.get("verdict")
        jcall = cx.call(jd.get("call_id"), s["id"], "j1")
        ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or "judge_faithfulness_v1", jcall)
        if verdict:
            ev.update(judge_verdict=verdict, judge_reason_code=jd.get("reason_code"))
        if verdict == "supported":
            ev["rationale"] = _J_OK["j1"]
            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", PASS, _J_OK["j1"], rule="row 4", evidence=ev))
        elif verdict in ("partially", "unsupported"):
            detail = why.judge_detail(jd.get("reason_code"))
            ev["rationale"] = detail or narrative.REASONS[reason]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:23.071Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/GATE-M3-pm/curated_provenance.py | head -40; sed -n 1,60p tests/e2e/test_mvp_polish.py; sed -n 250,270p tests/e2e/test_mvp_polish.py; grep -n \"FIXTURE_SET\\|E2E_REQUIRE_DB\\|7860\\|def server\\|BASE\" tests/e2e/conftest.py | head -30"
}
````

### User / tool · 2026-11-02T20:10:23.173Z

**tool result**
````
"""Count curated fixture files by provenance markers (hand-shaped vs recorded). Usage: python3 -I curated_provenance.py <repo root>"""
import collections, json, pathlib, sys

root = pathlib.Path(sys.argv[1]) / "tests" / "fixtures" / "llm"
for sub in ("curated", "recorded"):
    d = root / sub
    files = sorted(d.glob("*.json"))
    keys = collections.Counter()
    marks = collections.Counter()
    for f in files:
        try:
            j = json.loads(f.read_text())
        except Exception:
            marks["unparseable"] += 1
            continue
        keys.update(j.keys() if isinstance(j, dict) else ["<list>"])
        meta = json.dumps({k: j.get(k) for k in ("label", "source", "provenance", "curated", "kind", "note", "origin")} if isinstance(j, dict) else {})
        for m in ("CURATED", "curated", "hand", "recorded", "live"):
            if m in meta:
                marks[m] += 1
    print(sub, "files", len(files))
    print("  top keys", keys.most_common(12))
    print("  provenance markers", dict(marks))
others = [p.name for p in root.iterdir() if p.is_file()]
print("other files in fixtures/llm:", others[:20])
"""T-166 MVP polish (frontend half of the UX audit, reviews/MVP-ux-audit.md): F2 one-row header that never covers the source pane, F3 excerpts and charge quotes never clipped,
F4 Save and accept, F5 a dismissed row leaves a six-second placeholder and focus stays on screen, F6 the keyboard loop moves on (a, d, n, x), F7 no test or developer wording and no Audit link
on a row, and the P1s that are frontend only: F9 one open count in the live message, F10 'all agreed' only when it is true, F11 at most five visible controls per row, F12 Undo asks before
it throws her wording away.
New test ids (declared in tests/e2e/conftest.py, 'T-166'): dismiss-ghost, btn-undo-dismiss, btn-show-excerpt, btn-save-accept, discard-confirm, btn-discard-edit, btn-keep-edit, btn-more,
entry-more-panel, flag-more-panel, charge-more-panel, charge-quote. Needs the fixture backend (a plain run starts its own)."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

TITLE = "Rivera v. Northgate (MVA 2026-01)"
BAD_WORDS = re.compile(r"fixture|golden|prompt|JUDGE_|FIXTURE_|server answered|Request failed|cached demo|curated", re.I)


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


def _page(pw, w, h):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, permissions=["clipboard-read", "clipboard-write"])
    return b, ctx.new_page()


def _decided(page):
    m = re.match(r"(\d+) of (\d+) decided", page.locator("#progress-text").inner_text()); assert m
    return int(m.group(1)), int(m.group(2))


def _in_view(page):
    return page.evaluate("""(() => { const a = document.activeElement; if (!a || a === document.body) return null; const r = a.getBoundingClientRect();
      return { top: r.top, bottom: r.bottom, h: innerHeight, ok: r.top >= 0 && r.bottom <= innerHeight && r.height > 0, tag: a.tagName, tid: a.getAttribute('data-testid') }; })()""")


# ---- F2: one row header, the source pane starts below it
@pytest.mark.parametrize("scroll", [0, 2000])
def test_header_is_one_row_and_the_source_pane_starts_below_it(pw, rivera, scroll):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        e = pg.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
        e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
        expect(e).to_have_attribute("data-review", "edited")      # an edit to check makes the progress line its longest
        pg.evaluate(f"window.scrollTo(0, {scroll})"); pg.wait_for_timeout(300)
        m = pg.evaluate("""(() => { const h = document.querySelector('.app-header').getBoundingClientRect(), p = document.querySelector('.sbs-pane'), pr = p && p.getBoundingClientRect(),
          name = document.querySelector('#case-name'), tools = document.querySelector('.header-tools').getBoundingClientRect();
          return { hh: h.height, hb: h.bottom, pane: pr && getComputedStyle(p).display !== 'none' ? pr.top : null, sw: document.documentElement.scrollWidth, name: name.textContent, toolsTop: tools.top, headTop: h.top }; })()""")
        assert m["hh"] <= 60, m
        assert m["pane"] is not None and m["pane"] >= m["hb"] + 8 - 1, m
    open_case(page, rivera)
    page.evaluate("document.activeElement && document.activeElement.blur()")
    d0 = _decided(page)
    page.keyboard.press("n"); page.keyboard.press("x"); page.wait_for_timeout(200)
    assert _decided(page) == d0 and page.evaluate("document.activeElement === document.body")


# ---- F7: nothing a paralegal reads is test or developer wording; Audit is behind More on every row
def test_no_test_or_developer_wording_on_the_case_page_or_in_the_exports(page, rivera):
    open_case(page, rivera)
    for tid in ("entry-1", "entry-2"):
        page.get_by_test_id(tid).get_by_test_id("btn-accept").click()
    expect(page.locator("#badge")).to_have_text(re.compile(r"^(Demo: recorded AI answers|)$"))
    text = page.evaluate("document.body.innerText")
    assert not BAD_WORDS.search(text), BAD_WORDS.search(text).group(0)
    page.get_by_test_id("btn-export").click()
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    for tid in ("export-letter", "export-notes"):
        t = page.get_by_test_id(tid).inner_text()
        assert not re.search(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b", t) and not BAD_WORDS.search(t), (tid, t[:200])

1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
105:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
116:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
117:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
118:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
119:    global BASE
120:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
125:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
132:        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
140:        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)
154:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
164:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
168:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
169:        if os.environ.get("E2E_REQUIRE_DB") == "1":
176:        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
184:    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
190:    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
233:    return BASE
267:    page.goto(f"{BASE}/#/case/{tok}")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:28.336Z

**tool call — Bash**
````
{
 "command": "sed -n 100,160p tests/e2e/conftest.py; sed -n 185,235p tests/e2e/conftest.py; grep -rn \"demo_mode\\|def demo_mode\" app/backend/api.py | head -5"
}
````

### User / tool · 2026-11-02T20:10:28.436Z

**tool result**
````
  T-045 (tests/e2e/test_journey_modes.py, test_adversarial_ui.py, test_letter_matrix.py, test_two_cases_side_by_side.py): no new test ids.
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
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
    global BASE
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
    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
    def stop():
        proc.terminate()
        try: proc.wait(timeout=10)
        except Exception: proc.kill()
        log.close(); shutil.rmtree(tmp, ignore_errors=True)
    atexit.register(stop)
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
app/backend/api.py:120:    def demo_mode():
app/backend/api.py:235:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
app/backend/api.py:277:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
app/backend/api.py:278:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:321:        if demo_mode() and digest(text) not in allowed_hashes():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:32.371Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p app/frontend/app.js; sed -n 105,128p app/backend/api.py; sed -n 228,240p app/backend/api.py; grep -n \"demo_mode\" app/frontend/*.js | grep -v mock | head; sed -n 50,70p app/frontend/timeline.js; grep -n \"narrative\" app/backend/narrative.py | grep -n \"generator\" | head"
}
````

### User / tool · 2026-11-02T20:10:32.489Z

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
    // T-166 F7: no test or developer wording on screen. The demo says what it is in the paralegal's words; the longer explanation is the tooltip. A live backend has nothing to announce.
    const badge = $("#badge"); const demo = !!(h && h.demo_mode), mock = ZL.API_MODE === "mock";
    badge.textContent = demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
    badge.title = demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
    badge.hidden = !(demo || mock);
    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
    live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
    $("#delete-now").hidden = live.hidden;
  }
  // ---- case header (sticky): case name, "n of N decided", Export. The numbers are counts of what the API sent; nothing is computed beyond counting.
  const itemsOf = (c) => [].concat(c.entries || [], c.undated_entries || [], c.amounts || [], c.flags || []).filter((i) => i.state !== "rejected");
  // T-060 r5: "decided" means she has nothing left to do on the item. A dismissed item is decided. An edited item that is still marked Needs review is NOT: it is counted as an
  // edit to check. One need-review count (`needs`) is used by the header, the Open-decisions strip and the Timeline chip, and it falls when an item is decided or dismissed.
  // T-174 F9: ONE need-review number. It is the server's hitl.needs_review_open (the list summary of this case) whenever that summary describes the same moment as the case on screen (the same open
  // total: pending + edits_to_check); in the moments after a decision, before the summary is asked again, the same definition is counted from the case itself, so the number never lags or disagrees.
  ZL.progressOf = function (c) {
    const all = itemsOf(c), open = all.filter(ZL.undecided), mine = open.filter((i) => i.state === "needs_review" || ZL.editToCheck(i)).length;   // an edit still to compare is Needs review by definition (the server counts it; its response may lag the item's state)
    const sm = ZL.cases && ZL.cases.summary ? ZL.cases.summary(c.token) : null, h = sm && sm.hitl;
    const same = h && h.needs_review_open != null && (h.pending || 0) + (h.edits_to_check || 0) === open.length && (h.edits_to_check || 0) === ZL.editCount(c);
    return { total: all.length, decided: all.length - open.length, left: open.length, needs: same ? h.needs_review_open : mine, edits: ZL.editCount(c) };
    DB.connect(db_path).close()
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)

        if not isinstance(b, dict):
            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
        return b

    # -------------------------------------------------- routes
    @app.get("/api/health")
    def health():
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}

    @app.get("/api/cases")
    def list_cases():
app/frontend/input.js:58:      if (e.code === "demo_mode_unsupported_input") return demoRefusal();
app/frontend/input.js:146:      if (e.code === "demo_mode_unsupported_input") return demoRefusal();
app/frontend/stepper.js:200:    if (e.code === "demo_mode_unsupported_input") return "The demo can only run the second check on its recorded cases.";
    const row = el("article", { class: "entry st-" + e.state + (openRows.has(e.id) ? " is-open" : ""), "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
    const cmp = ZL.comparedEdit(e);
    const reasonText_ = cmp ? comparedReason(e) : e.state === "needs_review" && e.review_status !== "dismissed" && (e.reasons.length || e.why) ? plainReason(e) : "";
    const who = e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : "");
    row.append(...[
      el("div", { class: "entry-head" },
        e.date ? ZL.timeEl(e.date, { class: "date", "data-testid": "entry-date" }) : el("span", { class: "chip chip--warn", "data-icon": "calendar", "data-testid": "entry-date" }, "Date to confirm"),
        el("span", { class: "provider", "data-testid": "entry-provider" }, (!e.date && rec ? `Record ${rec.seq}: ` : "") + e.provider),
        e.date && rec ? el("span", { class: "chip chip--rec" }, "Rec " + rec.seq) : null,
        reasonText_ ? el("p", { class: "reason" + (e.reasons.includes("AI_TRANSLATION") ? " reason--caution" : ""), "data-testid": "entry-reasons", title: fullReason(e) }, reasonText_) : null,
        chips(e)),
      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
      e.edited ? el("p", { class: "muted small note", "data-testid": "edited-note" }, e.edited.original_summary != null
        ? "Edited by you; the code checked your wording against the quote when you saved. Original: " + e.edited.original_summary
        : "Quote changed by you; the code checked the new quote against the record when you saved. Original quote: " + (e.edited.original_excerpt || "(not kept)")) : null,
      quote(e, rec),
      e.duplicate_note ? el("p", { class: "muted small note" }, e.duplicate_note) : null,
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-why", "aria-label": "Why this status: " + e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : ""), onclick: () => openWhy(e.id) }, "Why this status"),
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": `Open record ${rec ? rec.seq : ""} for ${e.provider}`, onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"),
        )].filter(Boolean));
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:41.725Z

**tool call — Bash**
````
{
 "command": "grep -rn \"drafted by AI and checked\\|AI_BANNER\\|ai_banner\" app tests memory/contracts/api.md | grep -v \"^app/frontend/mock\" | cut -c1-200; grep -n \"AI draft\\|AI-drafted\\|drafted by AI\\|AI check\" app/frontend/*.js | grep -v \"^app/frontend/mock\\|//\" | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:10:41.861Z

**tool result**
````
app/frontend/app.js:10:    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by 
app/backend/api.py:36:AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
app/backend/api.py:237:                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
tests/unit/test_api_routes.py:44:    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)
memory/contracts/api.md:54:  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
memory/contracts/api.md:57:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached
app/frontend/app.js:10:    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by 
app/frontend/batch.js:118:    dlg.querySelector("#bc-text").textContent = "The code and the second AI check found support for " + (n === 1 ? "this entry" : "these " + n + " entries") + ", but you have
app/frontend/charges.js:85:      done ? "You confirmed it is a separate charge for a service. No AI check was asked about it." : "You took back your count. Accept it to count this line again; you conf
app/frontend/charges.js:101:      const t = done ? "You counted this line as a separate charge and confirmed it by name at " + f.confirmed_at + ". No AI check was asked about it." : "You counted this 
app/frontend/judges.js:1:/* "How the AI was checked" panel (T-082, D-042). Reads GET /cases/{token}/judges: items the second AI check judged, agreed / objected / unavailable counts,
app/frontend/judges.js:165:    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
app/frontend/judges.js:170:    det.append(el("ul", { class: "zj-tiles", "data-testid": "judge-totals", "aria-label": "AI check totals" },
app/frontend/judges.js:183:        nBlock ? plural(nBlock, "accepted item", "accepted items") + " cannot go in the letter until the second AI check has run on " + (nBlock === 1 ? "it" : "them") + "."
app/frontend/judges.js:219:      }, () => { if (cache) return; if (ZL.API_MODE === "mock" && root.isConnected) paint(root, null, "AI check details need the live server."); else root.hidden = true; });
app/frontend/review.js:273:  const AI_HELD = "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it i
app/frontend/review.js:274:  const ACCEPTED_HELD = "Compared by you. The second AI check still has no answer on the new quote, so the export stays blocked until it answers or you write the summary in 
app/frontend/review.js:302:    return lead + (st === "needs_review" ? " The entry still needs your review." : " The second AI check agreed.");
app/frontend/review.js:527:        isFlag ? null : el("p", { class: "rv-help rv-recheck-hint", "data-testid": "edit-recheck-hint" }, "When you save, the code checks every number, date and negation in 
app/frontend/stepper.js:41:    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
app/frontend/stepper.js:254:    judges: ["Open the AI checks", () => gotoPanel("judges")],
app/frontend/stepper.js:271:        if (unRerun) bits.push("The second AI check did not run on " + plural(unRerun, "item", "items") + ". Run it again; accepted items it never checked cannot go in the 
app/frontend/stepper.js:290:        if (jnr.length) parts.push(plural(jnr.length, "accepted item", "accepted items") + " never got the second AI check, so the export is blocked. Run the second check a
app/frontend/stepper.js:340:        if (t.view === "judges" && !(st && st.id === "judges")) btn("Open the AI checks", () => gotoPanel("judges"));
app/frontend/stepper.js:373:      out.push(el("p", { class: "zs-ev zs-judge", "data-testid": "step-judge-reason" }, el("strong", {}, "The second AI check said: "), S.verdictWord(ev.judge_verdict),
app/frontend/stepper.js:437:  const HUMAN_NOTE = "Not needed: this is your own wording, so the second AI check does not apply. The code checks on it still run.";
app/frontend/stepper.js:521:  S.HELD_NO_RERUN = (n) => (n === 1 ? "You changed the quote on an accepted entry and kept the AI's summary. The second AI check ran again and gave no answer on the new quo
app/frontend/stepper.js:522:    : plural(n, "accepted entry keeps", "accepted entries keep") + " the AI's summary under a quote you changed. The second AI check ran again and gave no answer on the new
app/frontend/stepper.js:523:  S.HELD_CAN_RERUN = (n) => (n === 1 ? "You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote."
app/frontend/stepper.js:524:    : plural(n, "accepted entry keeps", "accepted entries keep") + " the AI's summary under a quote you changed, and the second AI check has no answer on the new quotes.") 
app/frontend/suggestions.js:140:        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These counts were measured before the latest 
app/frontend/timeline.js:20:  const comparedReason = (e) => "Compared by you with the quote. " + ((e.reasons || []).includes("JUDGE_UNAVAILABLE") ? "The second AI check did not run." : plainReason(e))
app/frontend/timeline.js:268:            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` :
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:10:47.322Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_api_routes.py; grep -rln \"FIXTURE_SET\" tests/unit | head"
}
````

### User / tool · 2026-11-02T20:10:47.418Z

**tool result**
````
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


def wait_ready(c, tok, allow_failed=False):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready" or (allow_failed and s["status"] == "failed"), s
    return s


def run_case(c, text=None):
    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return tok


def test_health_shape(env):
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)


def test_create_sample_is_code_only_with_gap_flag(env):
    _, c = env
    r = c.post("/api/cases", json={"sample": True})
    b = r.json()
    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest


def test_error_format_and_unknown_token(env):
    _, c = env
    r = c.get("/api/cases/nope")
    e = r.json()["error"]
    assert r.status_code == 404 and e["code"] == "not_found" and set(e) == {"code", "message", "detail"}
tests/unit/test_t139_charge_text.py
tests/unit/test_t139_unmarked.py
tests/unit/test_export_edge.py
tests/unit/test_t134_unconfirmed_edit.py
tests/unit/test_spanish_records.py
tests/unit/test_eval_runner.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:04.420Z

**tool call — Write**
````
{
 "command": "/Users/arsis/zlayt-pm-project/tests/unit/test_prepared_provenance.py",
 "content": "\"\"\"T-177 / D-065 (GATE-M3 PM blocker): a curated (hand-checked) fixture answer is never presented as model output.\nProvenance comes from the fixture's own `recorded_from`. Curated -> prepared: true, model 'hand-checked (qa)' in the item, the trace and the audit rows;\nthe trace's generator step says it is a prepared answer. Recorded (and live) answers keep their real model ids and their AI labels.\"\"\"\nimport time\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend.api import create_app\n\nPREPARED_MODEL = \"hand-checked (qa)\"\n\n\ndef _client(tmp_path, monkeypatch, fixture_set):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.setenv(\"ZLAYT_MODE\", \"local\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    monkeypatch.delenv(\"LLM_FIXTURE_DIR\", raising=False)\n    if fixture_set:\n        monkeypatch.setenv(\"FIXTURE_SET\", fixture_set)\n    else:\n        monkeypatch.delenv(\"FIXTURE_SET\", raising=False)\n    return TestClient(create_app(str(tmp_path / \"p.sqlite\"), static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n\n\ndef _run(c):\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(240):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    assert s[\"status\"] == \"ready\", s\n    return tok\n\n\n@pytest.fixture\ndef curated(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, \"curated\")\n    return c, _run(c)\n\n\n@pytest.fixture\ndef recorded(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, None)\n    return c, _run(c)\n\n\ndef _generator_step(trace):\n    return next(s for s in trace[\"steps\"] if s[\"id\"] == \"extracted\")\n\n\ndef _all_text(o):\n    import json\n    return json.dumps(o)\n\n\n# ---- curated set\ndef test_curated_audit_rows_carry_the_prepared_model(curated):\n    c, tok = curated\n    calls = c.get(f\"/api/cases/{tok}/audit\").json()[\"calls\"]\n    gen = [x for x in calls if x[\"role\"] == \"generator\"]\n    assert len(gen) >= 9\n    for x in gen:\n        assert x[\"model\"] == PREPARED_MODEL and x[\"prepared\"] is True, x\n        assert \"claude-sonnet-5-5\" not in _all_text(x[\"model\"])\n    # D-056: judge answers are real recordings; they keep their real model id and are not prepared\n    judges = [x for x in calls if x[\"role\"] == \"judge\"]\n    assert judges and all(x[\"prepared\"] is False and x[\"model\"] != PREPARED_MODEL for x in judges)\n\n\ndef test_curated_item_is_marked_prepared(curated):\n    c, tok = curated\n    case = c.get(f\"/api/cases/{tok}\").json()\n    for e in case[\"entries\"]:\n        assert e[\"prepared\"] is True, e[\"id\"]\n        assert e[\"ladder\"][\"generator\"][\"model\"] == PREPARED_MODEL and e[\"ladder\"][\"generator\"][\"prepared\"] is True\n    item = c.get(f\"/api/cases/{tok}/items/e1\").json()[\"item\"]\n    assert item[\"prepared\"] is True and item[\"ladder\"][\"generator\"][\"model\"] == PREPARED_MODEL\n\n\ndef test_curated_trace_generator_step_names_a_prepared_answer(curated):\n    c, tok = curated\n    st = _generator_step(c.get(f\"/api/cases/{tok}/items/e1/trace\").json())\n    ev = st[\"evidence\"]\n    assert ev[\"model\"][\"id\"] == PREPARED_MODEL and ev[\"model\"][\"id\"] != \"claude-sonnet-5-5\" and ev[\"model\"][\"prepared\"] is True\n    assert st[\"why\"] == \"Prepared answer (hand-checked by the team for the demo), standing in for the AI draft\"\n    assert \"AI read this record\" not in _all_text(st) and \"AI drafted\" not in _all_text(st[\"label\"])\n\n\ndef test_curated_case_says_nothing_is_the_models_own(curated):\n    c, tok = curated\n    h = c.get(\"/api/health\").json()\n    assert h[\"answers\"] == \"prepared\" and \"prepared by our team\" in h[\"ai_banner\"] and \"drafted by AI\" not in h[\"ai_banner\"]\n    # the judge's step is still an AI check (a real recorded answer) and keeps its model id\n    tr = c.get(f\"/api/cases/{tok}/items/e1/trace\").json()\n    j = next(s for s in tr[\"steps\"] if s[\"id\"] == \"judge_1\")\n    assert j[\"evidence\"][\"model\"][\"id\"] != PREPARED_MODEL and j[\"evidence\"][\"model\"].get(\"prepared\") in (False, None)\n\n\n# ---- recorded set: labels stay AI\ndef test_recorded_set_keeps_ai_labels_and_model_ids(recorded):\n    c, tok = recorded\n    h = c.get(\"/api/health\").json()\n    assert h[\"answers\"] == \"recorded\" and \"drafted by AI\" in h[\"ai_banner\"]\n    calls = c.get(f\"/api/cases/{tok}/audit\").json()[\"calls\"]\n    assert calls and all(x[\"prepared\"] is False and x[\"model\"] != PREPARED_MODEL for x in calls)\n    assert any(x[\"model\"] == \"claude-sonnet-5-5\" for x in calls)\n    case = c.get(f\"/api/cases/{tok}\").json()\n    assert case[\"entries\"] and all(e[\"prepared\"] is False for e in case[\"entries\"])\n    e1 = case[\"entries\"][0]\n    assert e1[\"ladder\"][\"generator\"][\"model\"] == \"claude-sonnet-5-5\" and e1[\"ladder\"][\"generator\"].get(\"prepared\") is False\n    st = _generator_step(c.get(f\"/api/cases/{tok}/items/{e1['id']}/trace\").json())\n    assert st[\"evidence\"][\"model\"][\"id\"] == \"claude-sonnet-5-5\" and st[\"evidence\"][\"model\"][\"prepared\"] is False\n    assert st[\"why\"] == \"The AI read this record and proposed a one-line summary and a quote.\"\n\n\ndef test_live_backend_health_says_live(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, \"curated\")\n    from app.backend import store\n    monkeypatch.setattr(store, \"live_enabled\", lambda: True)\n    assert c.get(\"/api/health\").json()[\"answers\"] == \"live\"\n"
}
````

### User / tool · 2026-11-02T20:11:04.421Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Write failed due to the following issues:
The required parameter `file_path` is missing
An unexpected parameter `command` was provided</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:05.182Z

**tool call — Bash**
````
{
 "command": "grep -n \"def live_enabled\\|def live_model_available\" -A8 app/backend/store.py; grep -n \"def backend_name\" -A10 app/llm/provider.py; grep -n \"def complete_with_meta\" -A25 app/llm/provider.py | head -50"
}
````

### User / tool · 2026-11-02T20:11:05.288Z

**tool result**
````
11:def live_enabled() -> bool:
12-    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
13-    Read per call so a test can change the environment."""
14-    from app.llm import provider
15-    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
16-
17-
18:def live_model_available() -> bool:
19-    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
20-    from app.llm import provider
21-    return provider.backend_name() != "fixture" and live_enabled()
22-
23-
24-def iso(t) -> str:
25-    import datetime
26-    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
23:def backend_name() -> str:
24-    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
25-    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
26-    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
27-    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
28-    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
29-        return "fixture"
30-    return name
31-
32-
33-def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
92:def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
93-    name = backend_name()
94-    key = prompt_hash(model, system, user, json_schema)
95-    if name == "fixture":
96-        res = _fixture.call(model, system, user, json_schema, key=key)
97-    elif name in ("claude-cli", "anthropic-api"):
98-        if _recording() and not _record_ok:
99-            raise ValueError("record mode needs record_context() over text from evals/golden")
100-        if name == "claude-cli":
101-            from app.llm.backends import claude_cli as be
102-        else:
103-            from app.llm.backends import anthropic_api as be
104-        res = be.call(model, system, user, json_schema, key=key)
105-    else:
106-        raise LLMError(f"UNKNOWN_BACKEND {name}")
107-    validate_schema(res.output, json_schema)
108-    if name != "fixture" and _recording():
109-        _fixture.write(key, res, model)
110-    return res
111-
112-
113-def complete(model: str, system: str, user: str, json_schema: dict) -> dict:
114-    return complete_with_meta(model, system, user, json_schema).output
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:19.744Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_prepared_provenance.py",
 "content": "\"\"\"T-177 / D-065 (GATE-M3 PM blocker): a curated (hand-checked) fixture answer is never presented as model output.\nProvenance comes from the fixture's own `recorded_from`. Curated -> prepared: true, model 'hand-checked (qa)' in the item, the trace and the audit rows;\nthe trace's generator step says it is a prepared answer. Recorded (and live) answers keep their real model ids and their AI labels.\"\"\"\nimport json\nimport time\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend.api import create_app\n\nPREPARED_MODEL = \"hand-checked (qa)\"\n\n\ndef _client(tmp_path, monkeypatch, fixture_set):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.setenv(\"ZLAYT_MODE\", \"local\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    monkeypatch.delenv(\"LLM_FIXTURE_DIR\", raising=False)\n    if fixture_set:\n        monkeypatch.setenv(\"FIXTURE_SET\", fixture_set)\n    else:\n        monkeypatch.delenv(\"FIXTURE_SET\", raising=False)\n    return TestClient(create_app(str(tmp_path / \"p.sqlite\"), static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n\n\ndef _run(c):\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(240):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    assert s[\"status\"] == \"ready\", s\n    return tok\n\n\n@pytest.fixture\ndef curated(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, \"curated\")\n    return c, _run(c)\n\n\n@pytest.fixture\ndef recorded(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, None)\n    return c, _run(c)\n\n\ndef _generator_step(trace):\n    return next(s for s in trace[\"steps\"] if s[\"id\"] == \"extracted\")\n\n\n# ---- curated set\ndef test_curated_audit_rows_carry_the_prepared_model(curated):\n    c, tok = curated\n    calls = c.get(f\"/api/cases/{tok}/audit\").json()[\"calls\"]\n    gen = [x for x in calls if x[\"role\"] == \"generator\"]\n    assert len(gen) >= 9\n    for x in gen:\n        assert x[\"model\"] == PREPARED_MODEL and x[\"prepared\"] is True, x\n    # D-056: judge answers are real recordings; they keep their real model id and are not prepared\n    judges = [x for x in calls if x[\"role\"] == \"judge\"]\n    assert judges and all(x[\"prepared\"] is False and x[\"model\"] != PREPARED_MODEL for x in judges)\n\n\ndef test_curated_item_is_marked_prepared(curated):\n    c, tok = curated\n    case = c.get(f\"/api/cases/{tok}\").json()\n    assert case[\"entries\"]\n    for e in case[\"entries\"]:\n        assert e[\"prepared\"] is True, e[\"id\"]\n        assert e[\"ladder\"][\"generator\"][\"model\"] == PREPARED_MODEL and e[\"ladder\"][\"generator\"][\"prepared\"] is True\n    item = c.get(f\"/api/cases/{tok}/items/e1\").json()[\"item\"]\n    assert item[\"prepared\"] is True and item[\"ladder\"][\"generator\"][\"model\"] == PREPARED_MODEL\n\n\ndef test_curated_trace_generator_step_names_a_prepared_answer(curated):\n    c, tok = curated\n    st = _generator_step(c.get(f\"/api/cases/{tok}/items/e1/trace\").json())\n    ev = st[\"evidence\"]\n    assert ev[\"model\"][\"id\"] == PREPARED_MODEL and ev[\"model\"][\"id\"] != \"claude-sonnet-5-5\" and ev[\"model\"][\"prepared\"] is True\n    assert st[\"why\"] == \"Prepared answer (hand-checked by the team for the demo), standing in for the AI draft\"\n    assert \"AI read this record\" not in json.dumps(st) and \"AI drafted\" not in st[\"label\"]\n\n\ndef test_curated_health_says_prepared_and_the_banner_does_not_claim_ai(curated):\n    c, tok = curated\n    h = c.get(\"/api/health\").json()\n    assert h[\"answers\"] == \"prepared\" and \"prepared by our team\" in h[\"ai_banner\"] and \"drafted by AI\" not in h[\"ai_banner\"]\n    # the second check is still an AI check (a real recorded answer) and keeps its model id\n    tr = c.get(f\"/api/cases/{tok}/items/e1/trace\").json()\n    j = next(s for s in tr[\"steps\"] if s[\"id\"] == \"judge_1\")\n    assert j[\"evidence\"][\"model\"][\"id\"] != PREPARED_MODEL and not j[\"evidence\"][\"model\"].get(\"prepared\")\n\n\n# ---- recorded set: labels stay AI\ndef test_recorded_set_keeps_ai_labels_and_model_ids(recorded):\n    c, tok = recorded\n    h = c.get(\"/api/health\").json()\n    assert h[\"answers\"] == \"recorded\" and \"drafted by AI\" in h[\"ai_banner\"]\n    calls = c.get(f\"/api/cases/{tok}/audit\").json()[\"calls\"]\n    assert calls and all(x[\"prepared\"] is False and x[\"model\"] != PREPARED_MODEL for x in calls)\n    assert any(x[\"model\"] == \"claude-sonnet-5-5\" for x in calls)\n    case = c.get(f\"/api/cases/{tok}\").json()\n    assert case[\"entries\"] and all(e[\"prepared\"] is False for e in case[\"entries\"])\n    e1 = case[\"entries\"][0]\n    assert e1[\"ladder\"][\"generator\"][\"model\"] == \"claude-sonnet-5-5\" and e1[\"ladder\"][\"generator\"].get(\"prepared\") is False\n    st = _generator_step(c.get(f\"/api/cases/{tok}/items/{e1['id']}/trace\").json())\n    assert st[\"evidence\"][\"model\"][\"id\"] == \"claude-sonnet-5-5\" and st[\"evidence\"][\"model\"][\"prepared\"] is False\n    assert st[\"why\"] == \"The AI read this record and proposed a one-line summary and a quote.\"\n\n\ndef test_live_backend_health_says_live(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, \"curated\")\n    from app.backend import store\n    monkeypatch.setattr(store, \"live_enabled\", lambda: True)\n    assert c.get(\"/api/health\").json()[\"answers\"] == \"live\"\n"
}
````

### User / tool · 2026-11-02T20:11:19.813Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_prepared_provenance.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:19.860Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -x -q 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T20:11:21.199Z

**tool result**
````
E             - hand-checked (qa)
E             + claude-sonnet-5-5)

tests/unit/test_prepared_provenance.py:63: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_prepared_provenance.py::test_curated_audit_rows_carry_the_prepared_model
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 0.94s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:27.012Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='app/llm/audited.py'; s=open(p).read()\nold=\"\"\"model=(res.model_resolved if res and res.model_resolved else model),\"\"\"\nnew=\"\"\"model=(_prepared_model(res) or (res.model_resolved if res and res.model_resolved else model)),\"\"\"\nassert old in s; s=s.replace(old,new)\nold2=\"def _t(now):\"\nnew2='''PREPARED_BACKEND = \"curated\"      # D-065: recorded_from.backend of a hand-checked fixture (tests/fixtures/llm/curated); it is never model output\n\n\ndef is_prepared(recorded_from) -> bool:\n    return isinstance(recorded_from, dict) and recorded_from.get(\"backend\") == PREPARED_BACKEND\n\n\ndef _prepared_model(res):\n    \"\"\"D-065: a curated answer's audit row names who made it (the fixture's own recorded_from.model, 'hand-checked (qa)'), never the model the pipeline asked for.\"\"\"\n    if res is not None and is_prepared(res.recorded_from):\n        return str(res.recorded_from.get(\"model\") or \"hand-checked (qa)\")\n    return None\n\n\ndef _t(now):'''\ns=s.replace(old2,new2,1)\nopen(p,'w').write(s)\n\np='app/backend/present.py'; s=open(p).read()\nold='''         \"parsed_ok\": bool(c[\"parsed_ok\"]), \"verdict\": c[\"verdict\"]}\n    if full:'''\nnew='''         \"parsed_ok\": bool(c[\"parsed_ok\"]), \"verdict\": c[\"verdict\"], \"prepared\": AU.is_prepared(rf)}      # D-065: a hand-checked fixture answer, not model output\n    if full:'''\nassert old in s; s=s.replace(old,new); open(p,'w').write(s)\nE\nsed -n 1,19p app/backend/present.py; sed -n 275,300p app/backend/present.py"
}
````

### User / tool · 2026-11-02T20:11:27.125Z

**tool result**
````
"""Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
import json
import re

from app.backend import amounts as AM, conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
from app.db import db as DB

STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons, judge=None):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY
    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
    return out


def totals_view(conn, case_id):
    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
    cnt = lambda sts: sum(1 for a in ch if a["review_status"] in sts)   # noqa: E731
    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
            "pending": {"cents": t["detected_pending_cents"], "count": cnt(("pending",)), "label": "Pending review"},
            "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
                                     "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
            "flagged_charges": [{"id": a["id"], "flag": amount_flag(a)[0]["flag"]} for a in am if amount_flag(a)[1]],      # D-059: flagged charges waiting for a named confirm
            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"],
            "possible_overlaps": overlap.view(conn, case_id)}      # T-110: a statement line that may include a separately stated charge; warns, never changes the total


def rejected_count(conn, case_id):
    """Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2)."""
    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))
    return sum(1 for k in ("entry", "amount") for r in DB.list_items(conn, case_id, k) if r["state"] == "rejected" and r["id"] not in handled)


def review_view(conn, case_id):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:30.905Z

**tool call — Bash**
````
{
 "command": "grep -n \"^from app.llm\\|^import app.llm\\|as AU\" app/backend/generator.py app/backend/trace.py | head"
}
````

### User / tool · 2026-11-02T20:11:30.993Z

**tool result**
````
app/backend/generator.py:12:from app.llm import audited as AU, promptlib, provider as P
app/backend/trace.py:16:from app.llm import audited as AU
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:34.401Z

Now present.py item-level provenance.

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:39.444Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/present.py'; s=open(p).read()\ns=s.replace(\"from app.db import db as DB\\n\",\"from app.db import db as DB\\nfrom app.llm import audited as AU\\n\",1)\n# item_view + all_items hooks\nold='''    v[\"kind\"] = kind\n    v[\"second_check_pending\"] = item_id in second_check_pending_ids(conn, case_id)\n'''\nnew='''    v[\"kind\"] = kind\n    v[\"second_check_pending\"] = item_id in second_check_pending_ids(conn, case_id)\n    with_provenance(conn, case_id, [v])\n'''\nassert old in s; s=s.replace(old,new)\nold='''    pend = second_check_pending_ids(conn, case_id)\n    for k in (\"entry\", \"amount\", \"flag\"):'''\nnew='''    with_provenance(conn, case_id, out[\"entry\"] + out[\"amount\"] + out[\"flag\"])\n    pend = second_check_pending_ids(conn, case_id)\n    for k in (\"entry\", \"amount\", \"flag\"):'''\nassert old in s; s=s.replace(old,new)\nold='''def second_check_pending_ids(conn, case_id) -> set:'''\nnew='''def with_provenance(conn, case_id, views):\n    \"\"\"D-065: mark every item whose generator answer is a hand-checked fixture (the call's recorded_from.backend is 'curated') `prepared: true` and put the fixture's own model name\n    ('hand-checked (qa)') on its ladder's generator, so no screen or payload names a model for an answer no model gave. Others get prepared false and keep their model id.\"\"\"\n    calls = DB.list_llm_calls(conn, case_id)\n    by_id = {c[\"id\"]: c for c in calls}\n    by_item = {}\n    for c in calls:\n        if c[\"role\"] == \"generator\" and c.get(\"item_id\"):\n            by_item.setdefault(c[\"item_id\"], []).append(c)\n    for v in views:\n        gen = (v.get(\"ladder\") or {}).get(\"generator\")\n        call = by_id.get((gen or {}).get(\"call_id\")) or next(iter(reversed(by_item.get(v[\"id\"], []))), None)\n        prepared = bool(call) and AU.is_prepared(call.get(\"recorded_from\"))\n        v[\"prepared\"] = prepared\n        if gen is not None:\n            gen[\"prepared\"] = prepared\n            if prepared:\n                gen[\"model\"] = call[\"model\"]\n\n\ndef second_check_pending_ids(conn, case_id) -> set:'''\nassert old in s; s=s.replace(old,new,1)\nopen(p,'w').write(s)\nE\ngrep -n \"list_llm_calls\" -A12 app/db/db.py | head -30"
}
````

### User / tool · 2026-11-02T20:11:39.561Z

**tool result**
````
278:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
279-    q, a = "SELECT * FROM llm_calls WHERE case_id=?", [case_id]
280-    if item_id:
281-        q, a = q + " AND item_id=?", a + [item_id]
282-    return [_decode(r) for r in conn.execute(q + " ORDER BY created_at, rowid", a)]
283-
284-
285-def delete_case(conn, case_id: str) -> None:
286-    """The one deletion path (ADR-006): every table, prompts included. DELETE endpoint and purge both call this."""
287-    conn.execute("BEGIN")
288-    try:
289-        for t in _CASE_TABLES:
290-            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:49.234Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/present.py'; s=open(p).read()\ns=s.replace('''        if gen is not None:\n            gen[\"prepared\"] = prepared\n            if prepared:\n                gen[\"model\"] = call[\"model\"]''','''        if gen is not None:\n            gen = v[\"ladder\"][\"generator\"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched\n            if prepared:\n                gen[\"model\"] = call[\"model\"]''')\nopen(p,'w').write(s)\nE\ngrep -n '\"generator\"\\]\\|\\[\"generator\"\\] =\\|generator=' app/backend/flags.py | head; grep -n \"step(\\\"j\\|j1\\|judge\" app/backend/narrative.py | head -3; sed -n 1,40p app/backend/narrative.py | grep -n \"generator\" "
}
````

### User / tool · 2026-11-02T20:11:49.363Z

**tool result**
````
5:content; (b) judge 1 over the sentence and the quote; (c) the paralegal accepts or dismisses the paragraph. A sentence that fails (a) or
12:from app.backend import export, grounding, injection, judges, lexicon_scan, schemas, store
32:# deterministic backstop so a sentence like "significant pain 4/10" or "and recommended surgery" never rests on judge 1 alone.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:50.618Z

**tool call — Bash**
````
{
 "command": "grep -n \"generator\" app/backend/flags.py app/backend/narrative.py app/backend/conflict*.py | head -20"
}
````

### User / tool · 2026-11-02T20:11:50.706Z

**tool result**
````
app/backend/narrative.py:94:    base["generator"] = {"model": judges.generator_model(), "prompt_version": prompt.name, "call_id": call_id}
app/backend/flags.py:10:from app.backend import conflict_candidates as CC, sentences, confidence, credibility, flag_templates as FT, generator, grounding, injection, judges, language, lexicon_scan, schemas, why
app/backend/flags.py:28:    return generator.body_offset(record) if record.get("text") else 0
app/backend/flags.py:56:         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
app/backend/flags.py:238:            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:injection_scan"}}}
app/backend/flags.py:290:         "ladder": {"item_id": None, "generator": None, "judge": None,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:11:53.991Z

**tool call — Bash**
````
{
 "command": "sed -n 495,545p app/backend/api.py; grep -n \"def get\" -A15 app/backend/narrative.py | head -30"
}
````

### User / tool · 2026-11-02T20:11:54.084Z

**tool result**
````
        finally:
            c.close()

    @app.get("/api/cases/{token}/narrative")
    def narrative_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"narrative": narrative.get(c, token)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/narrative")
    def narrative_draft(token: str):
        """D-031: draft the firm-voice paragraph from ACCEPTED entries (each sentence code-checked and judged; failures removed with a reason)."""
        c = conn()
        try:
            get_case(c, token)
            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
            if nar.get("error") == "NO_ACCEPTED_ENTRIES":
                raise ApiError(400, "bad_request", "Accept at least one entry first; the paragraph is written from accepted entries only.")
            return {"narrative": nar}
        finally:
            c.close()

    @app.post("/api/cases/{token}/narrative/review")
    async def narrative_review(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
            except KeyError:
                raise ApiError(404, "not_found", "No draft paragraph yet.") from None
            except ValueError:
                raise ApiError(422, "invalid_edit", "That action is not allowed.") from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}")
    def item(token: str, item_id: str):
        c = conn()
        try:
            get_case(c, token)
            try:
                return present.why_view(c, token, item_id)
            except (KeyError, IndexError):
                raise ApiError(404, "not_found", "No such item.") from None
        finally:
            c.close()
137:def get(conn, case_id: str):
138-    return ((DB.get_case(conn, case_id) or {}).get("config") or {}).get("narrative")
139-
140-
141-def review(conn, case_id: str, action: str, now=0.0) -> dict:
142-    """accept | dismiss | reset on the whole paragraph (the paralegal's rung of the ladder)."""
143-    case = DB.get_case(conn, case_id)
144-    nar = dict((case.get("config") or {}).get("narrative") or {})
145-    if not nar:
146-        raise KeyError("narrative")
147-    if action not in ("accept", "dismiss", "reset"):
148-        raise ValueError(action)
149-    if action == "accept" and not nar.get("sentences"):
150-        raise ValueError("EMPTY")
151-    nar["status"] = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}[action]
152-    nar["reviewed_at"] = store.iso(now)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:12:08.218Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/trace.py'; s=open(p).read()\n# _llm_evidence: prepared flag\nold='''    ev = {\"model\": {\"id\": (call or {}).get(\"model\") or model, \"role\": role,\n                    \"independent_of_generator\": None if role == \"generator\" else ((call or {}).get(\"model\") or model) != cx.models[\"generator\"]}}'''\nnew='''    ev = {\"model\": {\"id\": (call or {}).get(\"model\") or model, \"role\": role,\n                    \"independent_of_generator\": None if role == \"generator\" else ((call or {}).get(\"model\") or model) != cx.models[\"generator\"],\n                    \"prepared\": bool(call) and AU.is_prepared(call.get(\"recorded_from\"))}}      # D-065: a hand-checked fixture answer, not model output'''\nassert old in s; s=s.replace(old,new)\n# extract pass step\nold='''            st.append(step(\"extracted\", \"AI drafted a summary and picked a quote\", \"llm\", PASS,\n                           \"The AI read this record and proposed a one-line summary and a quote.\", rule=\"row 4\", evidence=ev))'''\nnew='''            if ev[\"model\"][\"prepared\"]:\n                st.append(step(\"extracted\", PREPARED_LABEL, \"llm\", PASS, PREPARED_WHY, rule=\"D-065\", evidence=ev))\n            else:\n                st.append(step(\"extracted\", \"AI drafted a summary and picked a quote\", \"llm\", PASS,\n                               \"The AI read this record and proposed a one-line summary and a quote.\", rule=\"row 4\", evidence=ev))'''\nassert old in s; s=s.replace(old,new)\nold='''        st.append(step(\"proposed_by_ai\", \"AI found it\", \"llm\", PASS, \"The AI proposed this flag as a category and a quote; it wrote no explanation.\", rule=\"row 12\", evidence=ev))'''\nnew='''        if ev[\"model\"][\"prepared\"]:\n            st.append(step(\"proposed_by_ai\", PREPARED_LABEL, \"llm\", PASS, PREPARED_WHY, rule=\"D-065\", evidence=ev))\n        else:\n            st.append(step(\"proposed_by_ai\", \"AI found it\", \"llm\", PASS, \"The AI proposed this flag as a category and a quote; it wrote no explanation.\", rule=\"row 12\", evidence=ev))'''\nassert old in s; s=s.replace(old,new)\nold='''    st.append(step(\"extracted\", \"AI wrote this sentence from an accepted entry\", \"llm\", PASS, \"The AI wrote the sentence and named the one accepted entry it comes from.\", rule=\"D-031\", evidence=ev))'''\nnew='''    if ev[\"model\"][\"prepared\"]:\n        st.append(step(\"extracted\", PREPARED_LABEL, \"llm\", PASS, PREPARED_WHY, rule=\"D-065\", evidence=ev))\n    else:\n        st.append(step(\"extracted\", \"AI wrote this sentence from an accepted entry\", \"llm\", PASS, \"The AI wrote the sentence and named the one accepted entry it comes from.\", rule=\"D-031\", evidence=ev))'''\nassert old in s; s=s.replace(old,new)\nold=\"def _llm_evidence(\"\nnew='''PREPARED_LABEL = \"Prepared answer, standing in for the AI draft\"\nPREPARED_WHY = \"Prepared answer (hand-checked by the team for the demo), standing in for the AI draft\"\n\n\ndef _llm_evidence('''\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\n\np='app/backend/api.py'; s=open(p).read()\nold='''        return {\"ok\": True, \"version\": VERSION, \"synthetic_only\": True, \"banner\": BANNER, \"backend\": backend(), \"demo_mode\": demo_mode(),'''\nnew='''        ans = answers()\n        return {\"ok\": True, \"version\": VERSION, \"synthetic_only\": True, \"banner\": BANNER, \"backend\": backend(), \"demo_mode\": demo_mode(), \"answers\": ans,'''\nassert old in s; s=s.replace(old,new)\ns=s.replace('''\"ai_banner\": AI_BANNER, \"sample_available\"''','''\"ai_banner\": PREPARED_BANNER if ans == \"prepared\" else AI_BANNER, \"sample_available\"''')\nold='''    def models():'''\nnew='''    def answers():\n        \"\"\"D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set).\"\"\"\n        if live_enabled():\n            return \"live\"\n        from app.llm.backends import fixture\n        return \"prepared\" if backend() == \"fixture\" and fixture.answer_source() == \"prepared\" else \"recorded\"\n\n    def models():'''\ns=s.replace(old,new,1)\ns=s.replace('''AI_BANNER = \"Summaries and flags are drafted by AI and checked by code; you decide every item\"''','''AI_BANNER = \"Summaries and flags are drafted by AI and checked by code; you decide every item\"\nPREPARED_BANNER = \"In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item\"      # D-065''')\n# narrative\ns=s.replace('''            return {\"narrative\": narrative.get(c, token)}''','''            return {\"narrative\": present.narrative_view(c, token, narrative.get(c, token))}''')\ns=s.replace('''            return {\"narrative\": nar}\n        finally:''','''            return {\"narrative\": present.narrative_view(c, token, nar)}\n        finally:''')\ns=s.replace('''                return {\"narrative\": narrative.review(c, token, b.get(\"action\"), now=time.time())}''','''                return {\"narrative\": present.narrative_view(c, token, narrative.review(c, token, b.get(\"action\"), now=time.time()))}''')\nopen(p,'w').write(s)\n\np='app/backend/present.py'; s=open(p).read()\nold=\"def second_check_pending_ids(conn, case_id) -> set:\"\nnew='''def narrative_view(conn, case_id, nar):\n    \"\"\"D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture.\"\"\"\n    if not nar or not isinstance(nar.get(\"generator\"), dict):\n        return nar\n    call = next((c for c in DB.list_llm_calls(conn, case_id) if c[\"id\"] == nar[\"generator\"].get(\"call_id\")), None)\n    prepared = bool(call) and AU.is_prepared(call.get(\"recorded_from\"))\n    return {**nar, \"prepared\": prepared, \"generator\": {**nar[\"generator\"], \"prepared\": prepared, **({\"model\": call[\"model\"]} if prepared else {})}}\n\n\ndef second_check_pending_ids(conn, case_id) -> set:'''\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\n\np='app/llm/backends/fixture.py'; s=open(p).read()\ns+='''\n\ndef answer_source() -> str:\n    \"\"\"D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers).\"\"\"\n    return \"prepared\" if fixture_dir().name == \"curated\" else \"recorded\"\n'''\nopen(p,'w').write(s)\nE\n.venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -x -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T20:12:10.672Z

**tool result**
````
......                                                                   [100%]
6 passed in 2.03s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:12:13.661Z

**tool call — Bash**
````
{
 "command": "(timeout 1500 .venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider -n 4 2>&1 | tail -15) ",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:12:13.747Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:12:15.610Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -n 4 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:12:15.880Z

**tool result**
````
ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]
python -m pytest: error: unrecognized arguments: -n 4
  inifile: None
  rootdir: /Users/arsis/zlayt-pm-project
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:12:18.978Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:18:56.550Z

**tool result**
````
........................................................................ [ 84%]
........................................................................ [ 85%]
........................................................................ [ 87%]
........................................................................ [ 88%]
........................................................................ [ 89%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 93%]
........................................................................ [ 94%]
........................................................................ [ 96%]
........................................................................ [ 97%]
........................................................................ [ 98%]
........................................................................ [ 99%]
.........                                                                [100%]
5695 passed, 2 skipped in 395.86s (0:06:35)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:05.194Z

**tool call — Bash**
````
{
 "command": "ls app/frontend; grep -n \"AI\\b\" app/frontend/narrative.js | cut -c1-200 | head -20; sed -n 10,40p app/frontend/audit.js; grep -n \"mock\" app/frontend/mock.js | head -0; grep -n \"health\" app/frontend/mock.js | head"
}
````

### User / tool · 2026-11-02T20:19:05.302Z

**tool result**
````
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
narrative.js
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
    title = el("h2", { id: "audit-title", class: "au-title" }, "Audit");
    body = el("div", { class: "au-body" });
    dlg = el("dialog", { id: "audit-drawer", class: "au-drawer", "data-testid": "audit-drawer", "aria-labelledby": "audit-title" },
      el("div", { class: "au-head" }, title, el("button", { type: "button", class: "btn", "data-testid": "btn-close-audit", onclick: () => dlg.close() }, "Close")), body);
    dlg.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
    document.body.append(dlg);
  }
  const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "au-kv" }, el("span", { class: "au-k" }, k + " "), String(v)));
  const pre = (label, text) => (text == null || text === "" ? null : el("details", { class: "au-more" }, el("summary", {}, label), el("pre", { class: "au-pre" }, typeof text === "string" ? text : JSON.stringify(text, null, 2))));

  function callRow(c) {
    const rf = c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
    return el("li", { class: "au-call", "data-testid": "audit-call" },
      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
      el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prompt_version), kv("hash", c.prompt_sha256 ? String(c.prompt_sha256).slice(0, 12) : null),
        kv("latency", c.latency_ms != null ? c.latency_ms + " ms" : null), kv("attempt", c.attempt), kv("tokens", c.tokens_in != null ? c.tokens_in + " in / " + c.tokens_out + " out" : null), kv("cost", c.cost_usd != null ? "$" + c.cost_usd : null)),
      pre("System prompt (local mode)", c.system_text), pre("Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
  }
  function eventRow(e, confirmed) {   // a flagged charge's accept names the flag she confirmed (the event's own `confirm` when the server sends it)
    const named = e.confirm ? "confirmed " + (e.confirm.name || e.confirm.flag) : confirmed;
    return el("li", { class: "au-call", "data-testid": "audit-event" }, el("div", { class: "au-line" }, el("strong", {}, e.action + (named ? ", " + named : "")), el("span", { class: "au-k" }, e.at || "")),
      e.before || e.after ? pre("Before and after (local mode)", { before: e.before, after: e.after }) : null);
  }

  RV.openAudit = async function (itemId, label) {
    ensure(); const c = RV.caseNow(); if (!c) return;
    title.textContent = itemId ? "Audit: " + (label || itemId) : "Audit: whole case";
    clear(body); body.append(el("p", { role: "status" }, "Loading…"));
    if (!dlg.open) dlg.showModal();
    const r = await RV.http("GET", "/cases/" + encodeURIComponent(c.token) + "/audit");
    clear(body);
head: illegal line count -- 0
145:      if (method === "GET" && path === "/health") return ok({ ok: true, version: "0.1.0-mock", synthetic_only: true, banner: "Synthetic data only — never paste real records", backend: "fixture", demo_mode: false, live_enabled: false,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:10.783Z

**tool call — Bash**
````
{
 "command": "grep -n \"AI\\|draft\" app/frontend/narrative.js | cut -c1-220 | head; grep -n \"chip--\\|\\.tag\" app/frontend/styles.css | head -8"
}
````

### User / tool · 2026-11-02T20:19:10.895Z

**tool result**
````
1:/* Draft treatment paragraph (T-059, D-031): drafted by the server from ACCEPTED entries only, every sentence cited and checked. Shown with the
15:    LLM_FAILED_AFTER_RETRIES: "The model could not draft the paragraph after three tries. Nothing was made up; press Draft again, or write it yourself from the accepted entries.",
50:      root.append(...[el("div", { class: "rv-actions" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-draft-narrative", disabled: accepted === 0, onclick: () => call(c, "", {}, "Draft 
55:      if (nar.error) root.append(el("p", { class: "rv-error", role: "alert", "data-testid": "narrative-error" }, ERROR[nar.error] || "The paragraph could not be drafted. Try again, or write it yourself from the accept
62:        root.append(el("details", { class: "au-more", "data-testid": "narrative-removed" }, el("summary", {}, nar.removed.length + " drafted sentence" + (nar.removed.length === 1 ? "" : "s") + " removed by the checks"
69:        nar.status !== "pending" ? el("button", { type: "button", class: "btn", "data-testid": "btn-reset-narrative", onclick: () => act("reset", "Paragraph back to draft.") }, "Reset") : null,
70:        el("button", { type: "button", class: "btn", "data-testid": "btn-redraft-narrative", disabled: accepted === 0, onclick: () => call(c, "", {}, "New draft written. Read each sentence before you accept it.") }, "
92:.chip, .rv-chip, .zs-chip, .zs-kind, .zs-verdict, .tag, .sg-tag, .zs-blocks { display: inline-flex; align-items: center; gap: var(--s-1); min-height: 1.375rem; padding: 0 var(--s-2); border: 1px solid var(--border); border-radius: var(--r-1);
98:.chip--ok, .rv-rs-accepted, .rv-rs-edited { background: var(--ok-bg); color: var(--ok); border-color: var(--ok); }
99:.chip--warn, .rv-state-needs_review { background: var(--warn-bg); color: var(--warn); border-color: var(--warn); }
100:.chip--bad, .rv-state-rejected, .rv-rs-dismissed { background: var(--bad-bg); color: var(--bad); border-color: var(--bad); }
101:.chip--info, .rv-state-verified, .tag, .sg-tag, .rv-selfreport { background: var(--info-bg); color: var(--info); border-color: var(--info); }
102:.chip--muted { background: transparent; color: var(--text-muted); border-color: var(--border-strong); }
103:.chip--rec { background: transparent; font-weight: var(--w-regular); }
243:.summary .tag { margin-left: var(--s-2); vertical-align: baseline; min-height: 0; line-height: var(--lh-xs); }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:20.233Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/frontend/timeline.js'; s=open(p).read()\nold='''e.summary, e.ai_drafted ? el(\"span\", { class: \"tag\", \"data-icon\": \"ai\", title: \"Drafted by AI\" }, \"draft\") : null),'''\nnew='''e.summary, aiTag(e)),'''\nassert old in s; s=s.replace(old,new)\n# define aiTag before comparedReason line (line 20)\nold='''  const comparedReason = (e) =>'''\nnew='''  // D-065: a hand-checked demo answer is a \"Prepared answer\", never an AI draft; recorded and live answers keep the AI label.\n  const aiTag = (e) => !e.ai_drafted ? null : e.prepared\n    ? el(\"span\", { class: \"tag\", \"data-testid\": \"tag-prepared\", title: \"Prepared by our team for this demo, standing in for the AI draft\" }, \"Prepared answer\")\n    : el(\"span\", { class: \"tag\", \"data-icon\": \"ai\", \"data-testid\": \"tag-ai-draft\", title: \"Drafted by AI\" }, \"draft\");\n  const comparedReason = (e) =>'''\nassert old in s; s=s.replace(old,new,1)\nold='''el(\"dt\", {}, \"AI draft\"), el(\"dd\", {}, lad.generator.output'''\nnew='''el(\"dt\", {}, lad.generator.prepared ? \"Prepared answer\" : \"AI draft\"), el(\"dd\", {}, lad.generator.output'''\nassert old in s; s=s.replace(old,new)\nopen(p,'w').write(s)\n\np='app/frontend/stepper.js'; s=open(p).read()\nold='''    return (m && m.role === \"generator\") || st.id === \"extracted\" || st.id === \"extract\" ? \"AI draft\" : \"AI check\";'''\nnew='''    if (m && m.prepared) return \"Prepared answer\";         // D-065: a hand-checked demo answer is not an AI draft\n    return (m && m.role === \"generator\") || st.id === \"extracted\" || st.id === \"extract\" ? \"AI draft\" : \"AI check\";'''\nassert old in s; s=s.replace(old,new); open(p,'w').write(s)\n\np='app/frontend/audit.js'; s=open(p).read()\nold='''    const rf = c.recorded_from && c.recorded_from.backend ? \" (recorded from \" + c.recorded_from.backend + \")\" : \"\";'''\nnew='''    const rf = c.prepared ? \" (prepared answer, not model output)\" : c.recorded_from && c.recorded_from.backend ? \" (recorded from \" + c.recorded_from.backend + \")\" : \"\";'''\nassert old in s; s=s.replace(old,new)\nold='''el(\"span\", { class: \"rv-chip\" }, c.parsed_ok ? \"parsed\" : \"not parsed\"),'''\nnew='''el(\"span\", { class: \"rv-chip\" }, c.parsed_ok ? \"parsed\" : \"not parsed\"), c.prepared ? el(\"span\", { class: \"rv-chip\", \"data-testid\": \"audit-prepared\" }, \"Prepared answer\") : null,'''\nassert old in s; s=s.replace(old,new); open(p,'w').write(s)\n\np='app/frontend/app.js'; s=open(p).read()\nold='''    badge.textContent = demo ? \"Demo: recorded AI answers\" : mock ? \"Sample data\" : \"\";\n    badge.title = demo ? \"This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service.\" : \"\";'''\nnew='''    // D-065: say whose answers the demo replays. Prepared (curated) answers are the team's, never the model's; recorded ones are real model answers.\n    const prepared = demo && h.answers === \"prepared\";\n    badge.textContent = prepared ? \"Demo: sample answers prepared by our team\" : demo ? \"Demo: recorded AI answers\" : mock ? \"Sample data\" : \"\";\n    badge.title = prepared ? \"The AI's own answers on these cases are in the evaluation report.\"\n      : demo ? \"This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service.\" : \"\";'''\nassert old in s; s=s.replace(old,new); open(p,'w').write(s)\nE\ngrep -n \"T-166\\b\" tests/e2e/conftest.py | head -3; grep -n \"def test\" tests/unit/test_e2e_contract.py | head"
}
````

### User / tool · 2026-11-02T20:19:20.357Z

**tool result**
````
92:  T-149 r3 (declared with T-166): btn-new-case (primary 'New case' button in the Cases card header; scrolls to and focuses the case-name field), cases-keys (the j / k / Enter hint line under the case list), do-first-item (the item named in 'Do this first' in the case overview), panel-error (the notice a side panel shows when it threw; ZL.panelFailed).
93:  T-166 (MVP polish): dismiss-ghost (the placeholder a dismissed row leaves in its slot for 6 s, carries data-ghost-for = the item id; contains 'Dismissed: <label>' and btn-undo-dismiss 'Undo'), btn-show-excerpt ('Show full excerpt' directly
271:    """T-166 F11: Why this status, Change quote and Audit wait behind a row's More button. Opens it when the control is hidden, and returns the control."""
13:def test_every_test_id_is_declared():
26:def test_data_attributes_declared():
33:def test_roles_and_inputs_and_keys_declared():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:28.747Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/conftest.py'; s=open(p).read()\nold=\"  T-045 (tests/e2e/test_journey_modes.py\"\nnew=\"  T-177 (D-065, honest demo provenance): tag-prepared ('Prepared answer' tag on an entry whose summary is a hand-checked demo answer; never 'AI draft'), tag-ai-draft (the 'draft' tag with the AI glyph on a recorded or live answer), audit-prepared (chip on an Audit call row for a prepared answer). The #badge text says whose answers the demo replays.\\n  T-045 (tests/e2e/test_journey_modes.py\"\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\nE\nsed -n 55,75p tests/e2e/test_stepper.py; sed -n 255,275p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T20:19:28.858Z

**tool result**
````
    return page.evaluate("(c) => !!(document.activeElement && document.activeElement.closest(c))", css)


def open_why(page, n=8):
    reveal(page.get_by_test_id(f"entry-{n}").get_by_test_id("entry-why")).click()
    page.get_by_test_id("item-stepper").wait_for()
    return page.get_by_test_id("item-stepper")


# ---- item stepper
def test_item_stepper_in_why_panel(page, sample_case):
    """Why? shows an ordered list of steps with a status word, a kind chip (Code / AI draft / AI check / You) and the plain-words why."""
    open_case(page, sample_case); st = open_why(page)
    assert st.locator("ol").count() == 1
    steps = st.get_by_test_id("step")
    assert steps.count() >= 8
    kinds = {steps.nth(i).get_by_test_id("step-kind").inner_text() for i in range(steps.count())}
    assert {"Code", "AI check", "You"} <= kinds
    for i in range(steps.count()):
        s = steps.nth(i)
        assert s.get_attribute("data-status") in ("pass", "fail", "skipped", "pending")
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:51.568Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/e2e/test_demo_provenance.py",
 "content": "\"\"\"T-177 / D-065 (GATE-M3 product-manager blocker): the demo never shows a hand-checked (curated) answer as the AI's.\nAcceptance test (the PM's), curated set (the default private server, FIXTURE_SET=curated): no element names 'AI draft' or 'recorded AI answers' for a curated item; the badge says the answers were\nprepared by the team and its tooltip points at the evaluation report; /items/e1/trace's generator step is not claude-sonnet-5-5 and names a prepared answer; /audit rows for the generator carry\nmodel 'hand-checked (qa)'. Recorded set (a second private server, no FIXTURE_SET): the labels say AI and the model ids are real.\nNew test ids (declared in tests/e2e/conftest.py, 'T-177'): tag-prepared, tag-ai-draft, audit-prepared.\"\"\"\nimport json\nimport os\nimport re\nimport socket\nimport subprocess\nimport sys\nimport tempfile\nimport time\nimport urllib.request\n\nimport pytest\nfrom playwright.sync_api import expect\nfrom tests.e2e.conftest import api, open_case, reveal, ROOT, BASE\n\nPREPARED = \"hand-checked (qa)\"\nWHY = \"Prepared answer (hand-checked by the team for the demo), standing in for the AI draft\"\nTOOLTIP = \"The AI's own answers on these cases are in the evaluation report.\"\n\n\ndef _ready(call, tok):\n    for _ in range(300):\n        s = call(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(.5)\n    assert s[\"status\"] == \"ready\"\n\n\n@pytest.fixture\ndef curated_case():\n    st, c = api(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"Rivera v. Northgate (MVA 2026-01)\"}); assert st in (200, 201)\n    tok = c[\"token\"]; assert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    _ready(api, tok)\n    yield tok\n    api(\"DELETE\", f\"/api/cases/{tok}\")\n\n\n@pytest.fixture(scope=\"module\")\ndef recorded_server():\n    \"\"\"A private app on its own port with the recorded (real model answers) fixture set: FIXTURE_SET unset.\"\"\"\n    s = socket.socket(); s.bind((\"127.0.0.1\", 0)); port = s.getsockname()[1]; s.close()\n    tmp = tempfile.mkdtemp(prefix=\"zlayt-e2e-rec-\")\n    env = dict(os.environ, PORT=str(port), HOST=\"127.0.0.1\", ZLAYT_MODE=\"local\", LLM_BACKEND=\"fixture\", ZLAYT_DB=os.path.join(tmp, \"rec.sqlite3\"))\n    env.pop(\"ANTHROPIC_API_KEY\", None); env.pop(\"FIXTURE_SET\", None); env.pop(\"LLM_FIXTURE_DIR\", None); env.pop(\"ENABLE_LIVE\", None)\n    log = open(os.path.join(tmp, \"server.log\"), \"w\")\n    proc = subprocess.Popen([sys.executable, \"-m\", \"app.main\"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)\n    base = f\"http://127.0.0.1:{port}\"\n    for _ in range(80):\n        try:\n            urllib.request.urlopen(base + \"/api/health\", timeout=1).read(); break\n        except Exception:\n            assert proc.poll() is None, \"the recorded-set server exited\"\n            time.sleep(.5)\n    else:\n        proc.kill(); pytest.fail(\"the recorded-set server did not start\")\n\n    def call(method, path, body=None):\n        req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={\"Content-Type\": \"application/json\"})\n        with urllib.request.urlopen(req, timeout=60) as r:\n            raw = r.read()\n            return r.status, (json.loads(raw) if raw else None)\n    yield base, call\n    proc.terminate()\n    try: proc.wait(timeout=10)\n    except Exception: proc.kill()\n    log.close()\n\n\ndef _open_why(page, n):\n    reveal(page.get_by_test_id(f\"entry-{n}\").get_by_test_id(\"entry-why\")).click()\n    page.get_by_test_id(\"item-stepper\").wait_for()\n    return page.get_by_test_id(\"item-stepper\")\n\n\n# ---- the PM's acceptance test: API half (curated)\ndef test_curated_trace_and_audit_say_prepared(curated_case):\n    tok = curated_case\n    tr = api(\"GET\", f\"/api/cases/{tok}/items/e1/trace\")[1]\n    gen = next(s for s in tr[\"steps\"] if s[\"id\"] == \"extracted\")\n    assert gen[\"evidence\"][\"model\"][\"id\"] != \"claude-sonnet-5-5\" and gen[\"evidence\"][\"model\"][\"id\"] == PREPARED and gen[\"evidence\"][\"model\"][\"prepared\"] is True\n    assert gen[\"why\"] == WHY and \"prepared answer\" in gen[\"why\"].lower()\n    audit = api(\"GET\", f\"/api/cases/{tok}/audit\")[1][\"calls\"]\n    gens = [c for c in audit if c[\"role\"] == \"generator\"]\n    assert gens and all(c[\"model\"] == PREPARED and c[\"prepared\"] is True for c in gens), [(c[\"step\"], c[\"model\"]) for c in gens]\n    assert not any(c[\"model\"] == \"claude-sonnet-5-5\" for c in gens)\n    item = api(\"GET\", f\"/api/cases/{tok}/items/e1\")[1][\"item\"]\n    assert item[\"prepared\"] is True and item[\"ladder\"][\"generator\"][\"model\"] == PREPARED\n    assert api(\"GET\", \"/api/health\")[1][\"answers\"] == \"prepared\"\n\n\n# ---- the PM's acceptance test: page half (curated)\ndef test_curated_page_never_calls_a_prepared_answer_ai(page, curated_case):\n    open_case(page, curated_case)\n    badge = page.locator(\"#badge\")\n    expect(badge).to_have_text(\"Demo: sample answers prepared by our team\")\n    assert badge.get_attribute(\"title\") == TOOLTIP\n    entries = page.locator(\"[data-testid^=entry-][data-entry-id]\")\n    n = entries.count(); assert n >= 9\n    assert page.get_by_test_id(\"tag-prepared\").count() == n and page.get_by_test_id(\"tag-ai-draft\").count() == 0\n    assert page.get_by_test_id(\"tag-prepared\").first.inner_text() == \"Prepared answer\"\n    text = page.evaluate(\"document.body.innerText\")\n    assert \"AI draft\" not in text and \"recorded AI answers\" not in text, re.findall(r\".{20}(?:AI draft|recorded AI answers).{20}\", text)\n    assert page.locator(\"[title*='Drafted by AI'], [aria-label*='AI draft']\").count() == 0\n    assert \"drafted by AI\" not in page.locator(\"#banner-ai\").inner_text() and \"prepared by our team\" in page.locator(\"#banner-ai\").inner_text()\n    st = _open_why(page, 1)\n    gen = st.get_by_test_id(\"step\").first\n    assert gen.get_by_test_id(\"step-kind\").inner_text() == \"Prepared answer\"\n    body = st.inner_text()\n    assert \"Prepared answer (hand-checked by the team for the demo), standing in for the AI draft\" in body\n    assert \"AI draft\" not in body.replace(\"standing in for the AI draft\", \"\") and \"claude-sonnet-5-5\" not in body and \"The AI read this record\" not in body\n\n\ndef test_curated_audit_drawer_marks_the_prepared_rows(page, curated_case):\n    open_case(page, curated_case)\n    reveal(page.get_by_test_id(\"entry-1\").get_by_test_id(\"btn-audit\")).click()\n    page.get_by_test_id(\"audit-drawer\").wait_for()\n    drawer = page.get_by_test_id(\"audit-drawer\")\n    expect(drawer.get_by_test_id(\"audit-prepared\").first).to_have_text(\"Prepared answer\")\n    assert PREPARED in drawer.inner_text() and \"claude-sonnet-5-5\" not in drawer.inner_text()\n\n\n# ---- recorded set: the labels say AI\ndef test_recorded_set_labels_say_ai(pw, recorded_server):\n    base, call = recorded_server\n    st, c = call(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"Rivera v. Northgate (MVA 2026-01)\"}); tok = c[\"token\"]\n    assert call(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    _ready(call, tok)\n    assert call(\"GET\", \"/api/health\")[1][\"answers\"] == \"recorded\"\n    tr = call(\"GET\", f\"/api/cases/{tok}/items/e1/trace\")[1]\n    gen = next(s for s in tr[\"steps\"] if s[\"id\"] == \"extracted\")\n    assert gen[\"evidence\"][\"model\"][\"id\"] == \"claude-sonnet-5-5\" and gen[\"evidence\"][\"model\"][\"prepared\"] is False\n    assert gen[\"why\"] == \"The AI read this record and proposed a one-line summary and a quote.\"\n    calls = call(\"GET\", f\"/api/cases/{tok}/audit\")[1][\"calls\"]\n    assert calls and not any(x[\"prepared\"] or x[\"model\"] == PREPARED for x in calls)\n    b = pw.chromium.launch(); pg = b.new_context(viewport={\"width\": 1280, \"height\": 900}).new_page()\n    try:\n        pg.goto(f\"{base}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        expect(pg.locator(\"#badge\")).to_have_text(\"Demo: recorded AI answers\")\n        assert pg.get_by_test_id(\"tag-prepared\").count() == 0 and pg.get_by_test_id(\"tag-ai-draft\").count() >= 1\n        assert \"prepared by our team\" not in pg.evaluate(\"document.body.innerText\")\n        st_ = _open_why(pg, 1)\n        assert st_.get_by_test_id(\"step\").first.get_by_test_id(\"step-kind\").inner_text() == \"AI draft\"\n    finally:\n        b.close()\n"
}
````

### User / tool · 2026-11-02T20:19:51.617Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/e2e/test_demo_provenance.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:52.162Z

**tool call — Bash**
````
{
 "command": "grep -n \"btn-audit\" app/frontend/*.js | head -3; grep -n \"^def pw\\|def pw\" -B2 tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T20:19:52.273Z

**tool result**
````
app/frontend/audit.js:58:      el("button", { type: "button", class: "btn", "data-testid": "btn-audit-case", onclick: () => RV.openAudit(null) }, "Open full audit"));
app/frontend/review.js:483:    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
250-
251-@pytest.fixture(scope="session")
252:def pw():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:56.419Z

**tool call — Bash**
````
{
 "command": "sed -i 's/(Demo: recorded AI answers|)/(Demo: recorded AI answers|Demo: sample answers prepared by our team|)/' tests/e2e/test_mvp_polish.py && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -q -p no:cacheprovider 2>&1 | tail -30",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T20:19:56.524Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/e2e/test_mvp_poli ...": undefined label 'ests/e2e/test_mvp_polish.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:19:59.162Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/(Demo: recorded AI answers|)/(Demo: recorded AI answers|Demo: sample answers prepared by our team|)/' tests/e2e/test_mvp_polish.py && grep -n \"prepared by our team\" tests/e2e/test_mvp_polish.py | head -2; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -q -p no:cacheprovider 2>&1 | tail -30",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T20:20:04.996Z

**tool result**
````
262:    expect(page.locator("#badge")).to_have_text(re.compile(r"^(Demo: recorded AI answers|Demo: sample answers prepared by our team|)$"))
....                                                                     [100%]
4 passed in 4.74s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:08.034Z

**tool call — Bash**
````
{
 "command": "sed -n 45,62p memory/contracts/api.md; grep -n \"recorded_from\\|ai_drafted\\|independent_of_generator\" memory/contracts/api.md | cut -c1-180"
}
````

### User / tool · 2026-11-02T20:20:08.132Z

**tool result**
````
## GET /api/health
```json
{ "ok": true, "version": "0.1.0", "synthetic_only": true,
  "banner": "Synthetic data only — never paste real records",
  "backend": "fixture", "demo_mode": true, "live_enabled": false,
  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
  "limits": {"max_chars": 60000, "max_records": 40},
  "retention_hours": 24,
  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
  "sample_available": true }
```
`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.

## POST /api/cases
Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). A title is plain text (T-157 r2): control, zero-width and bidi-override characters are removed, line breaks and tabs become spaces, runs of white space collapse; blank means no name. A `title` with a `<` or `>` in it, or longer than 120 characters, is refused: `422 invalid_title` with a plain `message` that never repeats the text, and no case is created (the same for the `title` query of `POST /api/cases/pdf`, checked before the PDF is read). The older `name` field is held to the markup rule too, but a `name` longer than 120 characters (a long file name) is cut, not refused. The response carries `title` (what to show; see "Case titles" under `GET /api/cases`).
```json
{ "name": "Rivera sample", "text": "SYNTHETIC — ...\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, ...\"\n...", "sample": false }
27:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences
134:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose 
154:      "ai_drafted": true, "source_kind": "record",
162:                      "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T00:50:00Z"},
321:    { "id": "c18", "role": "generator", "step": "extract", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5"},
543:    "recorded_from": "claude-cli",
565:  "calls": [ { "id": "c1", "role": "generator", "step": "extract", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5"},
604:`evidence` keys (all optional): `excerpt` `{record_id, start, end, text}` (offsets absolute into the case text); `spans[]` (same shape, for flags); `tokens[]` (summary tokens n
617:      "evidence": { "model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null},
623:      "evidence": { "model": {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true}, "prompt_version": "judge_faithfulness_v1",
668:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:17.995Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='memory/contracts/api.md'; s=open(p).read()\ns=s.replace('''  \"backend\": \"fixture\", \"demo_mode\": true, \"live_enabled\": false,\n  \"models\"''','''  \"backend\": \"fixture\", \"demo_mode\": true, \"answers\": \"prepared\", \"live_enabled\": false,\n  \"models\"''',1)\nold='''`backend`: `claude-cli` | `anthropic-api` | `fixture`.'''\nnew='''`answers` (T-177, D-065): whose answers the app shows. `prepared` = the curated fixture set (`FIXTURE_SET=curated`): hand-checked by the team, NOT model output; `recorded` = a replay of real model answers (the default fixture dir); `live` = a model answering now. The UI badge follows it: `prepared` -> \"Demo: sample answers prepared by our team\" (tooltip \"The AI's own answers on these cases are in the evaluation report.\"), `recorded` -> \"Demo: recorded AI answers\". With `prepared`, `ai_banner` reads \"In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item\".\n`backend`: `claude-cli` | `anthropic-api` | `fixture`.'''\nassert old in s; s=s.replace(old,new,1)\ns+='''\n\n## Prepared answers (T-177, D-065; amends D-029)\nProvenance of every generator answer comes from the fixture's own `recorded_from`. A **curated** fixture (`recorded_from.backend == \"curated\"`, model `hand-checked (qa)`) is a *prepared answer*, never model output:\n- **Item** (`entries[]`, `amounts[]`, `flags[]`, `GET /items/{id}`): `prepared: boolean`. `ladder.generator` carries `prepared` and, when true, `model: \"hand-checked (qa)\"` (not `claude-sonnet-5-5`). `ai_drafted` keeps its meaning (a person did not write the summary); the UI tag is \"Prepared answer\" when `prepared`, \"AI draft\" otherwise.\n- **Audit** (`GET /audit` `calls[]`, also `/items/{id}` `calls[]`): each call has `prepared: boolean`; for a prepared call `model` is `hand-checked (qa)` (what is stored in `llm_calls.model`). Judge answers are real recordings (D-056): `prepared: false`, real model id.\n- **Trace** (`GET /items/{id}/trace`): `evidence.model.prepared: boolean`, and `evidence.model.id` is `hand-checked (qa)` for a prepared generator step. That step (`extracted`, a flag's `proposed_by_ai`, a narrative sentence's `extracted`) has label \"Prepared answer, standing in for the AI draft\" and `why` \"Prepared answer (hand-checked by the team for the demo), standing in for the AI draft\". Recorded and live steps keep \"AI drafted a summary and picked a quote\" / \"The AI read this record and proposed a one-line summary and a quote.\" and the real model id.\n- **Narrative** (`GET/POST /narrative`): `narrative.prepared` and `narrative.generator.prepared` (model `hand-checked (qa)` when true).\n'''\nopen(p,'w').write(s)\nE\ngit status --short | grep -v agent-memory"
}
````

### User / tool · 2026-11-02T20:20:18.168Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:22.844Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app tests memory/contracts | tail -30; git stash list | head -2"
}
````

### User / tool · 2026-11-02T20:20:22.904Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not run git stash (it rewinds shared board/memory files of other agents)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:24.225Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app tests memory/contracts | tail -30"
}
````

### User / tool · 2026-11-02T20:20:24.354Z

**tool result**
````
 app/backend/api.py                                 |  19 +-
 app/backend/present.py                             |  38 +-
 app/backend/trace.py                               |  24 +-
 app/frontend/app.js                                |   7 +-
 app/frontend/audit.js                              |   4 +-
 app/frontend/sections.js                           |  73 ----
 app/frontend/stepper.js                            |   1 +
 app/frontend/timeline.js                           |   8 +-
 app/llm/audited.py                                 |  16 +-
 app/llm/backends/fixture.py                        |   5 +
 memory/contracts/api.md                            |  11 +-
 tests/e2e/conftest.py                              |   1 +
 tests/e2e/test_journey_modes.py                    |  10 +-
 tests/e2e/test_ladder_gate.py                      |  36 +-
 tests/e2e/test_mvp_finish.py                       | 474 ---------------------
 tests/e2e/test_mvp_polish.py                       | 351 ---------------
 ...ec211dca19fd26207433389d8e62ea61a4c97c7557.json |  11 -
 ...c0a17b50480b0491795555fdc4bccfe6bac45e9a00.json |  11 -
 18 files changed, 152 insertions(+), 948 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:28.890Z

**tool call — Bash**
````
{
 "command": "wc -l tests/e2e/test_mvp_polish.py tests/e2e/test_mvp_finish.py app/frontend/sections.js; git show HEAD:tests/e2e/test_mvp_polish.py | wc -l; git show HEAD:tests/e2e/test_mvp_finish.py | wc -l; git status --short tests app/frontend/sections.js | head; git log --oneline -3 -- tests/e2e/test_mvp_polish.py"
}
````

### User / tool · 2026-11-02T20:20:29.204Z

**tool result**
````
     351 tests/e2e/test_mvp_polish.py
     474 tests/e2e/test_mvp_finish.py
      73 app/frontend/sections.js
     898 total
     351
     474
D  app/frontend/sections.js
 M tests/e2e/conftest.py
MM tests/e2e/test_charge_confirm.py
MM tests/e2e/test_code_check_refusal.py
MM tests/e2e/test_edit_to_check.py
MM tests/e2e/test_held_quote_gate.py
 M tests/e2e/test_journey_modes.py
 M tests/e2e/test_ladder_gate.py
MM tests/e2e/test_multicase.py
D  tests/e2e/test_mvp_finish.py
3301632 feat(frontend): T-174 F8/F9 the skip link, n and Start review go to the item Do this first names; one need-review count (server hitl.needs_review_open when it matches the case) and one open total for Can export - N not reviewed; list filter reads Everything decided; N3 a dismiss placeholder keeps focus through a repaint (flaky charge-dismiss spec fixed)
46df34e test(frontend): T-166 e2e for the MVP polish (25 specs); reveal() for controls behind More; hook ids declared; specs follow the short progress line, 11-key sheet, plain calibration text, Undo confirm
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:35.102Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- app/backend/api.py app/frontend/stepper.js app/frontend/app.js app/frontend/timeline.js tests/e2e/conftest.py | grep '^[+-]' | grep -v '^+++\\|^---' | cut -c1-160"
}
````

### User / tool · 2026-11-02T20:20:35.244Z

**tool result**
````
+PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item"      # D-065
+    def answers():
+        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the 
+        if live_enabled():
+            return "live"
+        from app.llm.backends import fixture
+        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
+
-        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
+        ans = answers()
+        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "answers": ans,
-                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
+                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN 
-            return {"narrative": narrative.get(c, token)}
+            return {"narrative": present.narrative_view(c, token, narrative.get(c, token))}
-            return {"narrative": nar}
+            return {"narrative": present.narrative_view(c, token, nar)}
-                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
+                return {"narrative": present.narrative_view(c, token, narrative.review(c, token, b.get("action"), now=time.time()))}
-    badge.textContent = demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
-    badge.title = demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
+    // D-065: say whose answers the demo replays. Prepared (curated) answers are the team's, never the model's; recorded ones are real model answers.
+    const prepared = demo && h.answers === "prepared";
+    badge.textContent = prepared ? "Demo: sample answers prepared by our team" : demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
+    badge.title = prepared ? "The AI's own answers on these cases are in the evaluation report."
+      : demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
+    if (m && m.prepared) return "Prepared answer";         // D-065: a hand-checked demo answer is not an AI draft
+  // D-065: a hand-checked demo answer is a "Prepared answer", never an AI draft; recorded and live answers keep the AI label.
+  const aiTag = (e) => !e.ai_drafted ? null : e.prepared
+    ? el("span", { class: "tag", "data-testid": "tag-prepared", title: "Prepared by our team for this demo, standing in for the AI draft" }, "Prepared answer")
+    : el("span", { class: "tag", "data-icon": "ai", "data-testid": "tag-ai-draft", title: "Drafted by AI" }, "draft");
-      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by 
+      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, aiTag(e)),
-            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excer
+            el("dt", {}, lad.generator.prepared ? "Prepared answer" : "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary
+  T-177 (D-065, honest demo provenance): tag-prepared ('Prepared answer' tag on an entry whose summary is a hand-checked demo answer; never 'AI draft'), tag-ai
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:39.425Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"temp.index\\|GIT_INDEX\" -B1 -A6 .claude/agent-memory/backend/project_t141_accident_date_checks.md | head -30"
}
````

### User / tool · 2026-11-02T20:20:39.524Z

**tool result**
````
2-name: t141-accident-date-checks
3:description: T-141 r3 accident-date rule (negation/history per word), read-time checks notes, no-summary = NOT_RUN, commit with a temp index
4-metadata:
5-  type: project
6----
7-
8-Accident-date conflict (conflicts.py `_describes_event`): a record dated before the stated date is a conflict if ANY event-vocabulary word is neither negated (5 words before) nor history-modified (3 words before, not "prior to"), and the clause is not dated to the past. Orchestrator's "any accident vocabulary = conflict" would re-open lib11 (PCP lists 2019/2022 accidents), so history stays info; the reviewer's V9/V10/V15/lib11 shapes are the pinned tests (tests/unit/test_t141_r3_variants.py).
9-
--
14-
15:Commit pitfall: shared-file hunks (present.py) go through a temp index (`GIT_INDEX_FILE=... git read-tree HEAD`, hash-object the HEAD blob with only my replace, update-index --cacheinfo); stage and commit in separate Bash calls (git-guard), set GIT_INDEX_FILE inline in both.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:44.399Z

**tool call — Bash**
````
{
 "command": "export TI=/private/tmp/claude-501/ti-t177.idx && rm -f $TI && GIT_INDEX_FILE=$TI git read-tree HEAD && GIT_INDEX_FILE=$TI git add app/backend/api.py app/backend/present.py app/backend/trace.py app/frontend/app.js app/frontend/audit.js app/frontend/stepper.js app/frontend/timeline.js app/llm/audited.py app/llm/backends/fixture.py memory/contracts/api.md tests/e2e/conftest.py tests/e2e/test_mvp_polish.py tests/e2e/test_demo_provenance.py tests/unit/test_prepared_provenance.py && GIT_INDEX_FILE=$TI git diff --cached --stat"
}
````

### User / tool · 2026-11-02T20:20:45.511Z

**tool result**
````
 app/backend/api.py                     |  19 +++--
 app/backend/present.py                 |  38 ++++++++-
 app/backend/trace.py                   |  24 ++++--
 app/frontend/app.js                    |   7 +-
 app/frontend/audit.js                  |   4 +-
 app/frontend/stepper.js                |   1 +
 app/frontend/timeline.js               |   8 +-
 app/llm/audited.py                     |  16 +++-
 app/llm/backends/fixture.py            |   5 ++
 memory/contracts/api.md                |  11 ++-
 tests/e2e/conftest.py                  |   1 +
 tests/e2e/test_demo_provenance.py      | 149 +++++++++++++++++++++++++++++++++
 tests/e2e/test_mvp_polish.py           |   2 +-
 tests/unit/test_prepared_provenance.py | 120 ++++++++++++++++++++++++++
 14 files changed, 383 insertions(+), 22 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:20:47.796Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/ti-t177.idx git commit -q -m \"feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T20:20:59.636Z

**tool result**
````
check_secrets: ok (14 file(s) scanned staged)
04ea2bf
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:00.520Z

Now verify from a `git archive HEAD` copy on my own port.

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:01.869Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/t177-arch && rm -rf $A && mkdir -p $A && git archive HEAD | tar -x -C $A && ln -s /Users/arsis/zlayt-pm-project/.venv $A/.venv && cd $A && E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e tests/unit/test_prepared_provenance.py tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T20:21:01.949Z

**tool result (error)**
````
Permission to use Bash with command A=/private/tmp/claude-501/t177-arch && rm -rf $A && mkdir -p $A && git archive HEAD has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:08.894Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t177-arch; mkdir -p $A && git archive HEAD | tar -x -C $A && ln -s /Users/arsis/zlayt-pm-project/.venv $A/.venv && ls $A | head -3; echo $A > /private/tmp/claude-501/t177-path.txt"
}
````

### User / tool · 2026-11-02T20:21:09.636Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:11.497Z

**tool call — Bash**
````
{
 "command": "A=$(cat /private/tmp/claude-501/t177-path.txt); cd $A && env -u ZLAYT_DB -u E2E_BASE_URL E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e tests/unit/test_prepared_provenance.py tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T20:21:11.575Z

**tool result**
````
Command running in background with ID: bij135qk3. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:16.283Z

**tool call — Monitor**
````
{
 "query": "tail -f /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output | grep -m1 -E \"passed|failed|error\"",
 "description": "wait for e2e run result",
 "timeout_ms": 900000
}
````

### User / tool · 2026-11-02T20:21:16.285Z

**tool result (error)**
````
<tool_use_error>InputValidationError: [
  {
    "code": "custom",
    "path": [],
    "message": "exactly one of command or ws"
  }
]

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 1800000ms are capped to 1800000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required":["description","timeout_ms"],"additionalProperties":false}</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:28.255Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-177 --agent backend --text \"Committed 04ea2bf (temp index). Tests first: tests/unit/test_prepared_provenance.py (6) + tests/e2e/test_demo_provenance.py (4, curated + recorded-set private server). Unit suite 5695 passed in working tree. Verifying e2e from git archive HEAD copy now.\" && cat > .claude/agent-memory/backend/project_t177_prepared_provenance.md <<'E'\n---\nname: t177-prepared-provenance\ndescription: T-177 D-065 curated fixture answers are \"prepared\", never AI output: where provenance is derived, labels, test setup, shared-index pitfall\nmetadata:\n  type: project\n---\n\nProvenance key = fixture `recorded_from.backend == \"curated\"` (`AU.is_prepared`). Audit row model is stored as the fixture's `recorded_from.model` (\"hand-checked (qa)\") by `audited_call`; read-time views add `prepared` (present._call, present.with_provenance for items + ladder.generator copy, trace._llm_evidence `model.prepared`, present.narrative_view). Health `answers` = prepared|recorded|live (`fixture.answer_source()` = fixture dir name is `curated`); `ai_banner` switches to PREPARED_BANNER. Judge answers in the curated run are real recordings (D-056) so they stay unprepared with real model ids.\n\nFrontend: badge in app.js, `aiTag` in timeline.js, kindOf in stepper.js, audit chip in audit.js. New test ids declared in tests/e2e/conftest.py docstring (unit test_e2e_contract checks).\n\nTests: recorded-set e2e needs its own private server (FIXTURE_SET unset); the default private server is curated. Pitfall: the shared git index had other agents' staged renames/deletions (MM/D lines), so `git diff HEAD` shows phantom deletions; commit through a temp index and diff only your paths.\nE\necho '- [T-177 prepared-answer provenance](project_t177_prepared_provenance.md) — D-065: curated = prepared; audit model, health answers, tag, private recorded-set e2e' >> .claude/agent-memory/backend/MEMORY.md"
}
````

### User / tool · 2026-11-02T20:21:28.403Z

**tool result**
````
noted on T-177
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:30.210Z

**tool call — Bash**
````
{
 "command": "sleep 240; tail -c 400 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:21:30.213Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 240 followed by: tail -c 400 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:31.631Z

**tool call — ToolSearch**
````
{
 "query": "select:Monitor",
 "max_results": 1
}
````

### User / tool · 2026-11-02T20:21:31.637Z

**tool result**
````
[tool_reference]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:36.447Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)|error\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output; do sleep 5; done; tail -n 12 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output",
 "description": "archive e2e run result",
 "timeout_ms": 1800000
}
````

### User / tool · 2026-11-02T20:21:36.457Z

**tool result**
````
Monitor started (task bsjc2goxf, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:38.962Z

**tool call — Bash**
````
{
 "command": "echo waiting",
 "description": "no-op while the monitor runs"
}
````

### User / tool · 2026-11-02T20:21:39.047Z

**tool result**
````
waiting
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:21:45.547Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)|rror\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output; do sleep 5; done; tail -n 12 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bij135qk3.output",
 "description": "Wait for archive e2e result",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:31:17.143Z

**tool result**
````
/bin/bash: child setpgid (84826 to 84826): Operation not permitted
        ex = row.get_by_test_id("entry-excerpt"); eb, mb = ex.bounding_box(), more.bounding_box()
>       assert mb["y"] >= eb["y"] + eb["height"] - 1, (eb, mb)                       # directly under the quote
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: ({'x': 466.59375, 'y': 592, 'width': 407.609375, 'height': 32}, {'x': 466.59375, 'y': 602, 'width': 122.421875, 'height': 28})
E       assert 602 >= ((592 + 32) - 1)

tests/e2e/test_mvp_polish.py:102: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_mvp_polish.py::test_a_decided_row_shows_one_line_and_a_button_under_the_quote_that_shows_the_rest
1 failed, 424 passed, 1 skipped in 602.20s (0:10:02)

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:29.725Z

**tool call — Bash**
````
{
 "command": "A=$(cat /private/tmp/claude-501/t177-path.txt); cd $A && env -u ZLAYT_DB -u E2E_BASE_URL E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_mvp_polish.py -q -p no:cacheprovider -k \"decided_row_shows_one_line\" 2>&1 | tail -4; cd /Users/arsis/zlayt-pm-project && B=$A-base && mkdir -p $B && git archive 0c4284f | tar -x -C $B && ln -s /Users/arsis/zlayt-pm-project/.venv $B/.venv && cd $B && env -u ZLAYT_DB -u E2E_BASE_URL E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_mvp_polish.py -q -p no:cacheprovider -k \"decided_row_shows_one_line\" 2>&1 | tail -4",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T20:31:35.098Z

**tool result**
````
.                                                                        [100%]
1 passed, 24 deselected in 1.45s
.                                                                        [100%]
1 passed, 24 deselected in 1.48s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:43.409Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B ac T-177 --check 1 --agent backend --evidence \"git archive 04ea2bf, E2E_REQUIRE_DB=1: tests/e2e (424 passed, 1 skipped; 1 timing flake test_mvp_polish decided_row passes alone, also on 0c4284f) incl. new tests/e2e/test_demo_provenance.py (curated+recorded private servers) and tests/unit/test_prepared_provenance.py (6); full unit suite 5695 passed in working tree\" && $B handoff T-177 --agent backend --text \"What changed: provenance from fixture recorded_from (curated => prepared). audited_call stores model 'hand-checked (qa)'; _call/items/ladder.generator/trace evidence.model/narrative carry prepared; trace step label+why = 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'; /health answers=prepared|recorded|live and ai_banner honest; UI badge 'Demo: sample answers prepared by our team' (tooltip: eval report), 'Prepared answer' tag/step chip/audit chip, recorded+live keep AI draft. api.md updated. Commit 04ea2bf. How verified: tests first (red then green); archive HEAD e2e with E2E_REQUIRE_DB=1 424 passed; recorded set via a private FIXTURE_SET-less server. Left: nothing for this card; D-056 judges in the curated run stay real model ids by design. Surprised: shared index holds others' staged renames, so used temp index; one flaky layout spec in test_mvp_polish (passes alone).\" && $B move T-177 in_review --agent backend && $B commit T-177 --sha 04ea2bf --agent backend && sh tools/serve_app.sh && curl -s http://127.0.0.1:7860/api/health | python3 -c \"import sys,json;print(json.load(sys.stdin)['answers'])\""
}
````

### User / tool · 2026-11-02T20:31:45.817Z

**tool result**
````
AC 1 checked: git archive 04ea2bf, E2E_REQUIRE_DB=1: tests/e2e (424 passed, 1 skipped; 1 timing flake test_mvp_polish decided_row passes alone, also on 0c4284f) incl. new tests/e2e/test_demo_provenance.py (curated+recorded private servers) and tests/unit/test_prepared_provenance.py (6); full unit suite 5695 passed in working tree
handoff written on T-177
T-177: in_progress -> in_review
T-177: commit 04ea2bf recorded
app http 200 on :7860
prepared
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:49.199Z

T-177 is in_review at commit `04ea2bf`, and the shared app on :7860 is restarted and reports `answers: prepared`. Curated answers now show as "Prepared answer" in the badge, tag, trace and audit rows, and recorded and live answers keep their AI labels. Verified from a `git archive HEAD` copy with `E2E_REQUIRE_DB=1`: 424 passed, 1 skipped, 1 failed. The failure was `test_mvp_polish.py::test_a_decided_row_shows_one_line_and_a_button_under_the_quote_that_shows_the_rest`, a layout-timing flake. It passes alone, and also on the commit before mine.

Changes are in `app/backend`, `app/llm`, `app/frontend`, the new tests `tests/unit/test_prepared_provenance.py` and `tests/e2e/test_demo_provenance.py`, and `memory/contracts/api.md`.
