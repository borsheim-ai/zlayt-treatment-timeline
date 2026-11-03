# T-013 review, round 3 — product-manager-reviewer

**Verdict: changes** (0 blockers, 2 majors, 4 minors, 1 nit).

The requirements themselves are now in good shape. Four of the five round-2 majors are fully resolved:
- `confirm_date` replaces date edits and has its own action table.
- Batch accept, charge reclassification and the duplicate split are all non-goals, and SCOPE_CUTS matches 1:1.
- R-TL-8 names five lexicon IDs that exist. A whole-sentence unit is defined, and my prototype splitter reproduces every §6 excerpt from it.
- R-EX-1 bans only tool-authored strings. D-012 is recorded.

7 of 10 re-sampled R-IDs are cleanly decidable, and none is contradictory. Full trace: `artifacts/review-evidence/T-013-trace.md` "Round 3".

What still fails is the hand-off. Two things changed after `b4f3924` and have not been reconciled:
1. **The golden set changed two minutes after b4f3924** (3c5eb7c). It now has 34 seeded hallucinations, not 20. Ship-bar row 4's literal "≥ 19 of the 20" would now pass a 56% catch rate.
2. **§8 says reconciliation is done (ADR-017), but it isn't.** The api.md export example, A-106 and D-018 each contradict a tested R-ID, and the golden vocabulary has drifted. Workers build from api.md and the golden, so T-017 would plan these two ways.

Both fixes are mechanical: about 30 minutes for writer and qa, plus one architect edit. A small reconciliation card that T-017 depends on would close both.

Exercised:
- `board.py show T-013` and `board.py list`; `git log`; `git diff --stat 64f766e..b4f3924`; `git diff --stat HEAD -- spec/REQUIREMENTS.md` (empty).
- Read REQUIREMENTS.md in full, plus ORCHESTRATOR_DECISIONS D-001..D-018, ADR-017, the api.md export and reason codes, ASSUMPTIONS A-106, SCOPE_CUTS, NEEDS_CHRIS, CONTRACT M2/M3, and the paralegal agent.
- Scripted the R-ID inventory: 62 rows, 0 dangling (R-RV-7 is withdrawn on purpose).
- Loaded lexicon.yaml with `.venv/bin/python` and checked the hedge IDs.
- Ran a prototype R-TL-2 splitter on the sample, checked the §6 excerpts and R-EX-1's banned strings, diffed the golden export against §6, checked aliases, and recomputed the bills-to-request rule. The probe is `artifacts/review-evidence/T-013-r3check.py`.
- Checked golden counts, levels, must_not IDs and `source_kind`.
- Re-sampled 10 R-IDs with seed 2026.

```json
{"card": "T-013", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "spec/REQUIREMENTS.md at b4f3924 (diff 64f766e..b4f3924, 160+/104-; HEAD diff empty) against memory/ORCHESTRATOR_DECISIONS.md D-001..D-018, memory/DECISIONS.md ADR-017, memory/contracts/api.md (e442626), memory/ASSUMPTIONS.md, memory/SCOPE_CUTS.md, evals/golden/* (3c5eb7c), app/llm/lexicon.yaml, docs/CONTRACT.md §5 M2/M3 and §8.2; prior reviews reviews/T-013-product-manager-r2.md and reviews/T-013-paralegal-r2.md; no app (M1)",
 "exercised": [
  "python3 tools/board.py show T-013 -> in_review, commits [65894f6, 64f766e, 4191140, b4f3924]; python3 tools/board.py list -> T-009 changes_requested, T-014 in_review, T-015 in_progress, T-017 ready (depends T-013/T-014/T-015)",
  "git diff --stat 64f766e..b4f3924 -- spec/REQUIREMENTS.md -> 1 file, 160+/104-; git diff --stat HEAD -- spec/REQUIREMENTS.md -> empty",
  "git log for api.md (e442626 18:40:17), golden (3c5eb7c 18:43:10), ASSUMPTIONS/SCOPE_CUTS (56750da 18:41:47) vs b4f3924 (18:41:23)",
  "Read spec/REQUIREMENTS.md 1-386 in full; ORCHESTRATOR_DECISIONS D-001..D-018; DECISIONS.md:276-290 ADR-017; api.md:23,196-208,240,255-300 (export example, reason codes)",
  "R-ID inventory script: 62 defined rows, 0 duplicates, only undefined ref R-RV-7 (withdrawn on purpose, REQ:111,385)",
  ".venv/bin/python yaml.safe_load(app/llm/lexicon.yaml): 48 entries; may_represent, correlate_clinically, possibility_terms, cannot_exclude, nonspecific_indeterminate all exist (causation_weakening); no entry has a `hedge` key",
  ".venv/bin/python -I artifacts/review-evidence/T-013-r3check.py: R-TL-2 splitter prototype -> units concat == record text for all 9; 'approx. 35 mph.' one unit; 11/11 §6 Source quotes are whole-unit runs; 0 of 13 banned/label strings in §6 letter; golden export != §6 block 1 (golden adds '=== LETTER_TEXT ... ===' marker and the notes block); 0 non-substring provider aliases",
  "Golden facts: case_01 E8 ambiguous with candidates [2026-04-05, 2026-05-04], record_warnings []; case_02 gaps 29/30/31 -> 3 flags 4 non-flags; case_04 6 records -> 4 entries E1[1,2] E2[3,4]; case_07 total 420; case_03 $1,2OO/$9S.00 unclear; hallucinations.jsonl 34 items (34 unique ids), controls 10; K4/K5 level must; must_not M1-M14; source_kind values {'patient_self_report': 9}",
  "Golden notes block == §6 block 2 (True); bills-to-request rule recomputed -> 'Austin EMS run report; Dr. Alvarez; Capital PT; Hill Country Pain Management' vs golden 'Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).'",
  "grep verify_quickly .claude/agents/ -> no match; paralegal-reviewer.md:86 'Rate \"I could verify every claim quickly\" 1-5'",
  "SCOPE_CUTS rows 1-19 vs REQ non-goals 1-19 -> 1:1 (NG12<->SC19, NG13<->SC12, NG19<->SC13)",
  "Re-sampled 10 R-IDs (random.seed(2026)): 7 decidable, 3 partial, 0 contradictory",
  "Appended 'Round 3' to artifacts/review-evidence/T-013-trace.md"
 ],
 "verdict": "changes",
 "scores": {"traceability": 5, "test_decidability": 4, "stretch_rationale": 5, "cut_rule": 4, "non_goals": 5, "ship_bar_fidelity": 3, "workflow_fit": 5, "architect_handoff": 3},
 "findings": [
  {"severity": "major", "title": "Ship-bar row 4 and R-TL-4 hard-code '19 of 20' seeded hallucinations and '5 controls'; the golden now has 34 and 10, so the literal threshold permits a 56% catch rate",
   "evidence": "REQ:322 'Judge recall on seeded hallucinations ≥ 95% (≥ 19 of the 20 in `hallucinations.jsonl`)'; REQ:51 'On the 20 seeded unsupported summaries ... flags at least 19 (≥ 95%...)' and 'On the 5 faithful controls'. Probe: hallucinations.jsonl 34 items with 34 unique ids; hallucinations_controls.jsonl 10 items (golden commit 3c5eb7c, after b4f3924). REQ:24 'Pass/fail wording is literal.'",
   "why_it_matters": "Ship bar #4 is the 'no invented facts' criterion, the one a demo-day failure hits first. Under the literal-wording rule a judge that catches 19 of 34 (56%) passes R-TL-4(b). The product note would then report a bar the eval doesn't hold.",
   "fix": "State the threshold as a rate over whatever the file holds: 'hallucination_catch_rate ≥ 0.95 over every item in hallucinations.jsonl (currently 34 → ≥ 33)'. Do the same for controls: '0 of the N controls (currently 10) judged unsupported'. Keep CONTRACT §8.2's '≥ 95%' as the governing number. Note in §8 that CONTRACT §5 M2 still says 'qa injects 20' (orchestrator).",
   "acceptance_test": "grep -n '19 of\\|the 20\\|5 faithful' spec/REQUIREMENTS.md returns nothing. R-TL-4(b) and ship-bar row 4 read as a rate, with the current count in parentheses, matching `wc -l evals/golden/hallucinations.jsonl`."},
  {"severity": "major", "title": "§8 says ADR-017 left 'no remaining known conflict', but api.md, A-106, D-018 and the golden contradict tested R-IDs and none of it is in 'Still open'",
   "evidence": "(1) api.md:266 letter example uses dot leaders '........ $6,240.00' (R-EX-6 REQ:124 'no dot leaders'); total '$6,240 (excludes physical therapy — per-visit rate only, visit count not stated)' (R-EX-8 REQ:126 UT 'letter_text contains neither \"visit count\" nor \"rate\"'); Source line 'Source: Central ER discharge summary, January 9, 2026 [Ex. __ / Bates __]:' (§6 REQ:218 'Source [Ex. __ / Bates __]:'). (2) Notes citation formats: api.md:267 'Capital PT, record 4:'; ASSUMPTIONS.md:20 A-106 'Internal notes cite provider + date, not record numbers'; R-EX-4 REQ:122 'record N (<provider as written>, <Month D, YYYY>)'. REQ:345 still says A-106 'currently says record number, provider, date', which is stale. (3) api.md:208 confirm_date with a non-candidate date -> '422 date_invalid'; R-RV-2 REQ:93 expects '422 `invalid_edit`'. (4) D-018 adds lexicon booleans `hedge`/`self_report` and flag_type ∈ {pre_existing, causation, record_warning}; REQ:4 cites only D-001 to D-015; REQ:26 and REQ:55 keep 'causation_weakening'/'compliance' and define the hedge set as 5 fixed IDs. T-009 (lexicon) is changes_requested and adding hedge entries. (5) R-TL-10 REQ:57 checks numbers/dates/$ only; api.md:304 SUMMARY_TOKEN_NOT_IN_EXCERPT also covers left/right/no/not/without. (6) Golden 3c5eb7c: K4/K5 level 'must' vs REQ:68 'should'; must_not M1-M14 vs REQ:68,137 'M1–M13'; source_kind 'patient_self_report' (9×, on entries) vs REQ:71 and api.md:166 'patient_report' (on flags); case_01 record_warnings [] vs REQ:40,70 'a record_warning'; seeded_edits reason 'number_not_in_excerpt' vs api.md:304. (7) §8 'Still open' rows 1-3 (REQ:376-378) are mostly done (aliases exact, export golden and seeded edits exist, SCOPE_CUTS 1-19 present, A-106 rewritten). The remaining part, adding verify_quickly to the paralegal brief, has no card: grep verify_quickly .claude/agents -> none.",
   "why_it_matters": "Round 2's major #5 recurs in a new form. Workers implement against api.md and the golden, and T-017 plans cards from REQ. With the letter format, notes citation, error code, hedge-set definition and self-report field each defined two or three ways, M3 would build one and the E2E/eval would check another. That is exactly the 'built two ways' failure the hand-off exists to prevent. The api.md total line also volunteers 'visit count not stated' to the carrier, which the paralegal r2 review removed.",
   "fix": "Replace §8 'Still open' with the current list, one row per conflict above, each with an owning card: architect (T-014 or a new card) fixes the api.md export example, the confirm_date error code and the R-TL-10 token set, or REQ adopts the api set; orchestrator fixes A-106 to match R-EX-4 and adds verify_quickly to the paralegal agent (T-016); qa (T-015) fixes source_kind and the reason-code name; writer cites D-016..D-018 and restates R-TL-8's hedge set as 'lexicon entries with `hedge: true` (D-018); until T-009 lands, the 5 IDs listed'. Then align R-FL-4 and R-CO-3 with the golden (K4/K5 must, M1–M14) or have qa revert. Add the reconciliation card to T-017's depends_on.",
   "acceptance_test": "A script greps api.md's letter_text example for '..', 'visit count' and 'rate', and finds none. A-106 and R-EX-4 name the same notes citation format. api.md and R-RV-2 name the same 422 code. `grep -rn patient_report\\|patient_self_report` returns one spelling. REQ:4 cites D-001..D-018. Every §8 'Still open' row names an open card ID, and none of those rows is already done."},
  {"severity": "minor", "title": "R-EX-6 compares letter_text to the whole golden file, but the file holds both blocks plus section markers",
   "evidence": "REQ:124 '`letter_text` equals the golden file byte for byte'. evals/golden/sample.export.expected.txt starts with '=== LETTER_TEXT (block 1: paste into letter) ===' and continues with '=== INTERNAL_NOTES_TEXT (block 2: do not send) ===' and the notes (probe diff).",
   "why_it_matters": "Taken literally, the test fails on a correct build. A worker will 'fix' it ad hoc, and whatever they choose is unspecified.",
   "fix": "R-EX-6: 'the LETTER_TEXT section of the golden file equals letter_text and the INTERNAL_NOTES_TEXT section equals internal_notes_text, byte for byte (markers excluded)'. That also gates the notes, which are currently byte-identical to §6 block 2.",
   "acceptance_test": "R-EX-6 names the section markers and both fields."},
  {"severity": "minor", "title": "R-EX-4 'bills to request' rule does not produce the worked example or the golden line",
   "evidence": "REQ:122 (8) 'providers (the label up to the first comma) with an entry in the letter and no accepted charge'. Recomputed: 'Austin EMS run report; Dr. Alvarez; Capital PT; Hill Country Pain Management'. REQ:297 and the golden: 'Austin EMS run report; Dr. Alvarez, primary care; Hill Country Pain Management; Capital PT (itemized ledger).' (not up-to-first-comma, not chronological, and an unruled suffix).",
   "why_it_matters": "This is spec-review pattern #3 recurring: the example passes only because its writer chose the string. Once the notes are byte-gated (minor above), code following the rule fails the golden.",
   "fix": "Add an order rule (first appearance in the chronology) and a suffix rule ('(itemized ledger)' when the provider has a non-dismissed rate). Then make §6 and the golden follow the rule: 'Dr. Alvarez', with Capital PT before Hill Country.",
   "acceptance_test": "A unit test applies rule (8) to the sample and gets the §6 line exactly."},
  {"severity": "minor", "title": "R-CO-9 test says 'fails twice'; ADR-003.7 and api.md say three attempts",
   "evidence": "REQ:143 'Retries: max 2 ... UT: LLM call fails twice → item shown as \"could not process\"'. DECISIONS.md:119 'Total attempts = 1 + 2 retries'; api.md:318 LLM_FAILED_AFTER_RETRIES 'failed on all three attempts'.",
   "why_it_matters": "A test that mocks two failures expects the failure state, while a correct implementation would make a third call.",
   "fix": "'UT: the call fails on all 3 attempts (1 + 2 retries, each with changed conditions) → LLM_FAILED_AFTER_RETRIES; fails twice then succeeds → entry produced.'",
   "acceptance_test": "R-CO-9's test names 3 attempts and includes the succeed-on-third case."},
  {"severity": "minor", "title": "No pre-ranked M3 cut order beyond the stretch; several M3 add-ons exceed Appendix A (I would do it differently)",
   "evidence": "CONTRACT:306 M3 ≤ 3.5 h. In M3 scope beyond SPEC Appendix A and CONTRACT M3: R-RV-9 full-record modal (REQ:99, 'This is core'); entry excerpt re-selection (REQ:105); R-EX-4 sections (7) future treatment and (8) bills to request (REQ:122); R-EX-5 pending-confirm on Copy (REQ:123); R-RV-3 judge re-run plus 'keep my wording' confirm (REQ:94). Only the stretch has a cut rule (REQ:170-173).",
   "why_it_matters": "The 62 rows fit 7 h only if nothing slips. Without a declared order, an overrun gets cut by whoever is holding the card, which breaks 'cut scope on purpose and tell us what you cut'.",
   "fix": "Add a 4-line 'M3 cut order if over 100% of budget' under §4: (1) R-ST-1; (2) excerpt re-selection, so edit becomes summary only, entries can still be dismissed and the notes still list flagged language; (3) R-EX-4 sections 7 and 8; (4) R-RV-9 drops to inline full-record expand with no highlight, and highlights stay in the E2E as a should. Each cut is logged in SCOPE_CUTS.",
   "acceptance_test": "§4 lists a numbered cut order. Each entry names its R-ID and what remains."},
  {"severity": "nit", "title": "§8 'Proposed additions' points to NEEDS_CHRIS, which now holds none of them; D-008/D-009/D-012 cite row numbers that no longer exist",
   "evidence": "REQ:349 'several depend on Chris, see `submission/NEEDS_CHRIS.md`'. NEEDS_CHRIS has rows 1-4 (key, demo/live, eval budget, git email); D-012 is listed under 'Decided by the team — FYI'. ORCHESTRATOR_DECISIONS D-008 '#7', D-009 '#8', D-012 '#10'.",
   "why_it_matters": "The stale pointers send a reader looking for a decision in the wrong place.",
   "fix": "REQ:349 should read 'team decisions; Chris can override via the NEEDS_CHRIS FYI list'. The orchestrator drops the stale row numbers from D-008/D-009/D-012.",
   "acceptance_test": "No REQ or D-row cites a NEEDS_CHRIS row number above 4."}
 ],
 "whats_right": [
  "R-TL-2's sentence unit is concrete enough to code from: a prototype reproduced all 11 §6 excerpts as whole-unit runs and kept 'approx. 35 mph.' intact.",
  "The two-block export plus 'flagged language quoted in the letter' is the right call: the records' words stay the record, and the attorney decides. R-EX-1 now tests only tool-authored strings.",
  "The cuts are deliberate and match 1:1: 19 non-goals ↔ 19 SCOPE_CUTS rows, each with a reason; R-CH-7 is now a safety restriction, not a feature."
 ],
 "questions_for_chris": []}
```
