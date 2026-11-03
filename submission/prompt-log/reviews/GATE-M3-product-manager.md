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
