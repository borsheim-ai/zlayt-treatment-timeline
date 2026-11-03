# T-018 apply-check: contract-review findings (product-manager-reviewer, round 2)

**Verdict: changes.** 0 blockers. 10 majors: 9 of the 19 contract majors are not applied (or applied in a form that still contradicts the card), plus one new major (T-018 AC2 is ticked on evidence this check refutes). 4 minor groups remain unapplied and are not gating (scope is blocker/major per the brief; severities kept as in source).

Mechanical check: `artifacts/review-evidence/T-018-r2-applied-check.py`, run as `python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project`, output in `artifacts/review-evidence/T-018-r2-applied-check.out.txt`. 68 checks: 31 pass, 37 fail. The failures include the minors and the T-017 items.

Rule used: an appended `Contract review (T-018): ...` AC counts as the requested edit only if a worker can test it and no in-place text on the same card contradicts it. An AC that still says "Either ... or" or "add ... or edit" leaves the decision open, so it counts as not applied.

| Finding (source) | Status | Evidence (verbatim, from `board.py show` or the file) |
|---|---|---|
| PM1 critical path, estimates, cut order | NOT APPLIED | `docs/M2M3_COVERAGE.md:18` "Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 ..." and `:19` "This runs about 4 h, over the 3.5 h budget." remain beside the new text at `:4`. Estimate on 2 of 20 cards (check PM-1d). |
| PM2 T-027 P0 plus timebox | NOT APPLIED | `priority: "P0"` applied; Description has no timebox (PM-2b). |
| PM3 fixture cannot ship | NOT APPLIED | T-038 AC6 "ship_bar_met is false when backend == fixture" applied; T-045 AC4 still "`python -m evals.run` (ship_bar_met true)" (PM-3c). |
| PM4 regression freshness | APPLIED | T-038 AC7 "latest.json records sha256 of every app/llm/prompts/*.md ... `--check-fresh` exits 1"; T-035 AC6 and T-036 AC8 handoff text. |
| PM5 verify_quickly owner | NOT APPLIED | `.claude/agents/paralegal-reviewer.md:111` "`scores.verify_quickly` (1–5)" applied; no M3 card names the key (PM-5b, M3 list empty). |
| PM6 lexicon recall gate | NOT APPLIED | T-038 AC9 "...or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'" (open "or"); `docs/LLM_VS_CODE.md:44` "...whose recall on the golden set is a release gate" (PM-6c). |
| PL1 edits survive reload | APPLIED | T-044 AC6 "...export notes list record 3 under EDITED ITEMS with original and new text"; T-039 AC6 test_edited_items_section. |
| PL2 reconciliation "7 of 9" | NOT APPLIED | T-039 AC2 still "dismissing entry 5 gives 'Record 5 ... dismissed' and 7 of 9" (PL-2b); corrected wording only in AC7. |
| PL3 accident date as two dates | APPLIED | T-043 AC6 "Date of accident per intake form: 2026-01-19." |
| PL4 record 4 visible as failed | APPLIED | T-042 AC6 "'could not process' with the reason in the could-not-verify tray"; T-041 AC6 "RECORDS NOT IN THE TREATMENT SECTION with reason". |
| S1 qa author for 20 test files | NOT APPLIED | T-048 exists (applied, AC1 names 9 files). 11 files still have no qa owner (probe: "qa:NONE count = 11"). T-039 names none of them (S-1b). |
| S2 missing depends_on | APPLIED | T-031 `['T-029']`; T-042 `['T-039']`; T-043 `['T-039', 'T-040', 'T-042']`. |
| S3 SDK hidden retries | APPLIED | T-034 AC7 "max_retries=0 and an explicit timeout (<= 120 s)". |
| S4 fixture-miss behaviour | APPLIED | T-034 AC8 "a fixture miss raises FixtureMissing"; T-037 AC7 "reports 0 FixtureMissing". The weaker original T-037 AC2 remains and does not contradict. |
| S5 judges #2-4 error path | APPLIED | T-035 AC7 "JUDGE_UNSURE / JUDGE_UNAVAILABLE"; T-036 AC9 "judge #3/#4 error or timeout -> needs_review". |
| S6 boundary-test module list | APPLIED | T-029 AC7 "conflicts (accident date), flag_templates, injection scan". |
| S7 row-10 engine | NOT APPLIED | T-033 AC6 "Either T-033 gains AC6 ... or an ADR edits row 10"; `docs/M2M3_COVERAGE.md:96` "T-036 (m2-be-llm-flags) (provider variants)"; no decision in memory/ORCHESTRATOR_DECISIONS.md (S-7a, S-7b, S-7c). |
| S8 rate note derived by code, damages mention | APPLIED | T-033 AC7 "rate note numbers are code-derived ... one damages mention (record 5, value null)". The "only" left in T-033 AC1 is in the minors below. |
| S9 case_07 total | NOT APPLIED | T-039 AC1 still "'Billed charges stated in these records: $8,390.00' incl. case_07 with a rate present" (S-9a); $420 is only in AC9. |

## New finding
- **N1 (major).** T-018 AC2 is ticked as "every blocker/major applied ... verified by reviews/T-018-product-manager.md". This review refutes it (see F1-F9 below). The T-018 handoff's "~23 majors applied" is also wrong: 10 of 19 contract majors are applied.

## Things that landed and should not break
- T-048 exists and gates T-034..T-037; the test-first wiring for LLM stages is real.
- Fixture-cannot-ship is written into T-038 AC6 and T-037 AC7 (every hallucinations line and SE1-SE5 are named).
- The paralegal edit-reload, two-date accident conflict and record-4 visibility ACs are on the board (PL1, PL3, PL4).

```json
{"card": "T-018", "persona": "product-manager-reviewer", "model": "claude-haiku-5-5",
 "scope": "Apply-check of the T-018 contract-review findings: reviews/CONTRACT-M2M3-product-manager.md (6 majors, 3 minors, 1 nit), CONTRACT-M2M3-paralegal.md (4 majors, 4 minors), CONTRACT-M2M3-staff-engineer.md (9 majors, 4 minors), against the board working tree (board/cards T-017, T-018, T-027, T-029..T-046, T-048), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, .claude/agents/paralegal-reviewer.md, memory/ORCHESTRATOR_DECISIONS.md, memory/SCOPE_CUTS.md, memory/DECISIONS.md, evals/golden/README.md, memory/contracts/api.md. No app code exists; no sample-case run (contract review).",
 "exercised": [
  "read personas/product-manager.md in full; memory index and memory files plan_review_patterns, spec_review_patterns, reviewer_sandbox, needs_chris_drift, calibration_vs_redflags",
  "read reviews/CONTRACT-M2M3-product-manager.md, CONTRACT-M2M3-paralegal.md, CONTRACT-M2M3-staff-engineer.md and reviews/T-017-product-manager.md in full",
  "python3 tools/board.py validate -> 'ok (48 file(s))' (before writing this review)",
  "python3 tools/board.py list; show T-017, T-018, T-048; show T-027 and T-029..T-046 with grep for priority, depends_on, status and AC lines; show Descriptions of T-027, T-029, T-036, T-038, T-039, T-045",
  "cat -n docs/M2M3_COVERAGE.md (lines 3-19 critical path and cut order, 8-15 ship-bar table, 22 R-ID header, 96 row 10)",
  "python3 -c read of artifacts/tmp/contract_fixes.json: 19 entries (6 manag, 4 paral, 9 engin) mapped to the cards they name",
  "grep -n verify_quickly .claude/agents/paralegal-reviewer.md personas/paralegal.md -> agent body line 111",
  "sed/grep docs/LLM_VS_CODE.md rows 10, 12, 16 (lines 38, 40, 44); spec/REQUIREMENTS.md section 7 rows 3-5 (lines 327-329); memory/ORCHESTRATOR_DECISIONS.md and grep case_05 across docs, memory, spec (no row-10 decision); memory/SCOPE_CUTS.md (no variant E row); evals/golden/README.md:144 (case_07 total $420); memory/DECISIONS.md:169 (fixture by default); memory/contracts/api.md:26 ({token} export path)",
  "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt -> 68 checks, 31 pass, 37 fail; probe qa:NONE count = 11; longest chain to T-038: T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029"
 ],
 "verdict": "changes",
 "scores": {"majors_applied_in_full": 2, "ship_bar_traced": 3, "fixture_cannot_ship": 2, "regression_discipline": 4, "test_first_owners": 2, "golden_numbers_consistent": 2, "paralegal_journey_acs": 4},
 "findings": [
  {"severity": "major", "title": "PM1: stale 5-card critical path and 4 h sentence still in the coverage doc; per-card estimates missing; cut order touches the lexicon gate",
   "evidence": "docs/M2M3_COVERAGE.md:18 'Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 ... -> T-038' and :19 'This runs about 4 h, over the 3.5 h budget.' (check PM-1b, PM-1c). Estimates: 2 of 20 M2/M3 cards carry one (T-029 and T-039 'Timebox 1 h'); 18 do not (check PM-1d). docs/M2M3_COVERAGE.md:5 'M2 cut order (never touches ship-bar items) ... (3) lexicon held-out target lowered from 85% to reported'; docs/LLM_VS_CODE.md:44 '...whose recall on the golden set is a release gate'; spec/REQUIREMENTS.md:327 ship-bar row 3 'R-FL-1 to R-FL-4'.",
   "why_it_matters": "The doc now states two critical paths. At its own 30-45 min per card, seven cards is 3.5-5.25 h against a 3.5 h M2 budget, with no total and no cut trigger. Cut 3 lowers the floor under flag recall, which ship-bar row 3 measures per type, so 'never touches ship-bar items' is false as written.",
   "fix": "Delete coverage lines 18-19. Add an 'Estimate: N min' line to the Description of each of the 18 cards. State the total and the cut trigger in one sentence. Remove cut 3, or record in memory/SCOPE_CUTS.md that it touches R-FL-3/R-FL-4 (ship-bar row 3) before the cut is allowed.",
   "acceptance_test": "grep -c 'This runs about 4 h' docs/M2M3_COVERAGE.md = 0; board.py show prints an estimate in the Description of all 20 M2/M3 cards; the M2 cut order names no lever that touches REQUIREMENTS section 7 row 3 unless that impact is written next to it."},
  {"severity": "major", "title": "PM2: T-027 raised to P0 without the timebox the fix requires",
   "evidence": "python3 tools/board.py show T-027: priority \"P0\" (applied). Description: 'Debt from T-009 ... Fix the patterns rather than the examples, and score on a held-out set.' No timebox (check PM-2b). T-036 depends_on still includes T-027.",
   "why_it_matters": "A P0 card with no stop rule gates the M2 chain through T-036 with no limit on how long it can run.",
   "fix": "Add a timebox line to T-027 Description, e.g. 'Timebox N h; at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md' (N set by the orchestrator).",
   "acceptance_test": "board.py show T-027 Description contains 'Timebox'."},
  {"severity": "major", "title": "PM3: T-045 AC4 still requires ship_bar_met true on the default run, which T-038 AC6 makes false on fixture",
   "evidence": "python3 tools/board.py show T-045 AC4: 'sensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `python -m evals.run` (ship_bar_met true), ...' (check PM-3c). T-038 AC6: 'ship_bar_met is false when backend == fixture'. memory/DECISIONS.md:169: 'tests and eval iteration use `fixture` by default'.",
   "why_it_matters": "A worker who follows AC4 literally runs the default fixture backend and gets ship_bar_met false, so the card either cannot close or someone sets the flag by hand. The claude-cli form is only in appended AC6, so the replay path the PM review targeted is still the default one.",
   "fix": "Replace AC4's bare '`python -m evals.run` (ship_bar_met true)' with '`LLM_BACKEND=claude-cli python -m evals.run` (ship_bar_met true)' in place; keep the fixture run as its own sensor line.",
   "acceptance_test": "board.py show T-045 AC4 contains 'LLM_BACKEND=claude-cli' and no bare '`python -m evals.run` (ship_bar_met true)'."},
  {"severity": "major", "title": "PM5: verify_quickly is in the paralegal agent body, but no M3 card or gate AC asks for it",
   "evidence": ".claude/agents/paralegal-reviewer.md:111 '**Ship-bar score (D-015):** ... your review JSON must include `scores.verify_quickly` (1–5) ... ≥ 4 is the ship bar.' (applied). M3 cards whose ACs name the key: none (check PM-5b). The only other hits are T-025 and T-038 AC8, whose 'New orchestrator card (M3)' does not exist on the board.",
   "why_it_matters": "Ship-bar row 5 (spec/REQUIREMENTS.md:329) is the one human number. Without an M3 AC that requests it, the M3 gate can close on a paralegal review with no score.",
   "fix": "Create the M3 card the fix named, or add an AC to T-045: 'M3 gate paralegal review writes reviews/<card>-paralegal.md with scores.verify_quickly (D-015); ship bar 5 met when >= 4'.",
   "acceptance_test": "board.py show of an M3 card includes an AC naming scores.verify_quickly; grep -l verify_quickly board/cards/T-04*.md lists it."},
  {"severity": "major", "title": "PM6: the lexicon-recall release gate is undecided; T-038 AC9 is an 'or' and LLM_VS_CODE still calls it a gate",
   "evidence": "python3 tools/board.py show T-038 AC9: '...add `lexicon_recall_must_flags` ... and state the threshold in REQUIREMENTS section 7 by ADR, or edit LLM_VS_CODE rows 12/16 to \"reported, not gated\".' (open 'or', check PM-6d). docs/LLM_VS_CODE.md:44 '...whose recall on the golden set is a release gate' (check PM-6c). T-038 AC1 metric list has no lexicon metric.",
   "why_it_matters": "The injection defence (R-RV-6) is either gated or not, and the product note will say one or the other. The coverage cut order already treats it as ungated; the LLM/code table still says gated.",
   "fix": "Choose one and record it in memory/ORCHESTRATOR_DECISIONS.md. Either add lexicon_recall_must_flags to T-038 AC1 with a threshold, or edit LLM_VS_CODE rows 12 and 16 to 'reported, not gated' and delete 'release gate'. Remove the 'or' from T-038 AC9.",
   "acceptance_test": "grep -c 'release gate' docs/LLM_VS_CODE.md = 0 and T-038 has no 'or edit' text; or jq '.metrics.lexicon_recall_must_flags' evals/reports/latest.json returns a number after T-038 runs."},
  {"severity": "major", "title": "PL2: T-039 AC2 still says dismissing entry 5 alone gives '7 of 9'; the corrected AC is appended as AC7",
   "evidence": "python3 tools/board.py show T-039 AC2: '...dismissing entry 5 gives \"Record 5 ... dismissed\" and 7 of 9 (R-EX-4, R-EX-7)' (check PL-2b, not removed). Corrected text is AC7 only: 'dismissing entry 5 and leaving entry 6 pending gives ... and 7 of 9'.",
   "why_it_matters": "One card gives two counts for the same dismissal. With only entry 5 dismissed the letter holds 8 of 9 records, so the uncorrected AC2 encodes the wrong count and a correct build can fail it.",
   "fix": "Replace T-039 AC2's 'dismissing entry 5 gives ... 7 of 9' in place with the AC7 wording, and delete AC7.",
   "acceptance_test": "grep -c 'dismissing entry 5 gives' board/cards/T-039.md = 0."},
  {"severity": "major", "title": "S1: 11 test files still have no qa author; T-039 does not name them",
   "evidence": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... -> 'qa:NONE count = 11 -> [test_api, test_charges, test_edit, test_export_ui, test_flags_panel, test_input, test_keyboard_mobile, test_review_matrix, test_side_by_side, test_source_record, test_timeline]'. T-039 AC8 is the instruction 'name test_api.py plus the 10 E2E files above, by file'; no T-039 AC names any of the 11 (check S-1b).",
   "why_it_matters": "CONTRACT:240 gives tests/** to qa. These files are cited by backend and frontend ACs, so those cards cannot be test-first, and T-039's 'test-first' covers them only by R-ID.",
   "fix": "Rewrite T-039 AC4 to list the 11 files by name with the R-IDs each covers. test_api.py may move to T-048. Re-run the applied-check.",
   "acceptance_test": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... prints 'qa:NONE count = 0'."},
  {"severity": "major", "title": "S7: the row-10 engine is still an 'Either ... or' instruction; no decision is recorded",
   "evidence": "python3 tools/board.py show T-033 AC6: 'Either T-033 gains AC6 ... or an ADR edits row 10 and T-036 AC3 says ...' (check S-7a); same text on T-036 AC10. docs/M2M3_COVERAGE.md:96 '| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |'. docs/LLM_VS_CODE.md:38 row 10 '... the same provider spelled two ways | **Code**'. grep case_05 across docs, memory and spec: no decision (only spec/REQUIREMENTS.md).",
   "why_it_matters": "The table says code, the plan gives it to the LLM card, and the T-036 implementer will pick one. A provider-name conflict raised by both engines shows the panel the same flag twice.",
   "fix": "Decide and record it. Either provider-variant conflict is Code (a T-033 AC with no LLM call, row 10 unchanged), or row 10 changes by ADR. Replace the 'Either' text on T-033 AC6 and T-036 AC10 with the decision, and update docs/M2M3_COVERAGE.md row 10 to match.",
   "acceptance_test": "grep -c 'Either' board/cards/T-033.md board/cards/T-036.md = 0; coverage row 10 and LLM_VS_CODE row 10 name the same engine."},
  {"severity": "major", "title": "S9: T-039 AC1 still asserts $8,390.00 for case_07; the $420 line is appended as AC9",
   "evidence": "python3 tools/board.py show T-039 AC1: 'total line exactly \"Billed charges stated in these records: $8,390.00\" incl. case_07 with a rate present' (check S-9a). Golden: evals/golden/README.md:144 'Total $420; $50,000 never totaled'. Corrected text is AC9 only.",
   "why_it_matters": "A test-first card that asserts $8,390 for case_07 contradicts the golden $420 total and leaves the implementer to pick. A wrong money assertion is the bad-day case for this product.",
   "fix": "Replace AC1's case_07 clause in place with the AC9 wording ('on case_07 with $420 accepted it is exactly ... $420.00'), and delete AC9.",
   "acceptance_test": "board.py show T-039 AC1 contains '$420.00' on case_07 and does not contain '$8,390.00 incl. case_07'."},
  {"severity": "major", "title": "N1: T-018 AC2 is ticked on evidence this check refutes",
   "evidence": "python3 tools/board.py show T-018 AC2 evidence: 'every blocker/major applied as AC edit/new card (artifacts/tmp/contract_fixes.json); verified by reviews/T-018-product-manager.md'. T-018 Handoff: '~23 majors applied as AC edits/deps/new card T-048 before any M2 claim.' This check: 9 of 19 contract majors not applied (PM1, PM2, PM3, PM5, PM6, PL2, S1, S7, S9), see the table above.",
   "why_it_matters": "The gate that closes the contract review records a claim this check refutes. Later cards would treat the M2 contract as settled.",
   "fix": "Reopen T-018 AC2 (done false) or change its evidence to this review's verdict. Correct the handoff count to the applied number once PM1-S9 land.",
   "acceptance_test": "board.py show T-018 shows AC2 done false, or AC2 evidence cites reviews/T-018-product-manager.md with verdict pass."},
  {"severity": "minor", "title": "Unapplied PM minors (not gating): cut clock, flag-group count, token-log test, golden variant E, 'only' in T-033 AC1, {id} path",
   "evidence": "python3 tools/board.py show T-046 AC5: 'cut order per REQUIREMENTS section 4 recorded if M3 passes 100% of budget' (no clock, check m-PM1a). T-037 AC1: 'prints ... all flag groups' (m-PM1b). T-040 AC5: 'no access log of tokens' (m-PM1c). docs/LLM_VS_CODE.md:44 'documented as golden variant E, a qa item, not yet in the golden set'; no variant E in memory/SCOPE_CUTS.md or any card AC (m-PM2). T-033 AC1: 'sample yields $6,240, $185, $2,150 only' (S-8b). T-041 AC4: 'GET /api/cases/{id}/export' (nit; memory/contracts/api.md:26 spells {token}).",
   "why_it_matters": "Each is a check a worker can tick without proving anything. The variant E item is the one injection path only the human catches, and the note should cite it.",
   "fix": "T-046 AC5: quote M3 start and end timestamps from board activity and state the trigger. T-037 AC1: name the five groups with counts 1/2/2/5/0. T-040 AC5: add test_api::test_no_token_in_logs. Add variant E to T-038 or a SCOPE_CUTS row. T-033 AC1: replace 'only' with the damages mention. T-041 AC4: {token}.",
   "acceptance_test": "Each named test or command exists and fails when its condition is broken."},
  {"severity": "minor", "title": "Unapplied PL minors (not gating): reason sentence inline, full $185 string, charge highlight and banner record, dismissal reason to notes",
   "evidence": "python3 tools/board.py show T-042 AC2: 'timeline rows show date, provider, summary, excerpt, state' (no inline reason, m-PL1). T-043 AC2: \"$185 'rate $185/visit; visit count not stated'\" (truncated, m-PL2). T-043 AC1 'case_07 shows an injection warning' (no record 3, m-PL3b); T-043 AC5 'gap flag opens both records 6 and 7' (no $6,240 charge highlight, m-PL3a). T-043 AC3 'dismiss -> reset -> dismiss' (no reason, m-PL4).",
   "why_it_matters": "She reads why an item needs review on sight, and she reconciles $6,240 against the ER record. Each of these is a fact she checks in the first minute.",
   "fix": "T-042 AC2: 'every needs_review row shows its why-template sentence inline'. T-043 AC2: quote the full R-CH-3 string. T-043 AC1: 'case_07 banner names record 3 and says flags may be incomplete'. T-043 AC5: '$6,240 charge opens record 2 with \"ER charges: $6,240.\" highlighted'. T-043 AC3: dismiss the gap flag with a reason and check it in the notes FLAGS DISMISSED.",
   "acceptance_test": "tests/e2e/test_timeline.py::test_reason_inline; test_flags_panel.py::test_injection_banner_names_record; test_source_record.py::test_charge_highlight; test_review_matrix.py::test_dismiss_reason_in_notes."},
  {"severity": "minor", "title": "Unapplied staff minors (not gating): xfail instead of --collect-only, retry prompt hash, judge input isolation, verifier mutation guard, network guard",
   "evidence": "python3 tools/board.py show T-029 AC3: 'proved by `pytest tests/unit -q --collect-only` listing them' (m-S1). T-034 AC2: 'each retry with changed conditions' (no prompt-hash check, m-S2a). T-035 AC5: 'prompts are versioned files ... the generator and judge never share a prompt' (no input-isolation check, m-S2b). T-030 has 5 ACs, none naming monkeypatch or mutation (m-S3). T-029 AC5 names no socket or network guard (m-S4).",
   "why_it_matters": "Collected-but-broken red tests pass for 'red'; a retry that resends the same prompt passes; a verifier stubbed to pass goes unnoticed; one stray network call makes the suite flaky and costs money.",
   "fix": "T-029 AC3: each new test is xfail(strict=True, reason='T-0xx') and pytest -rx shows them. T-034 AC2: consecutive attempts have different prompt hashes in llm_calls. T-035 AC5: the rendered judge #1 prompt holds the record and candidate only. T-030 AC6: monkeypatching grounding.verify to pass fails test_grounding and test_pipeline. T-029 AC5: tests/conftest.py blocks socket.connect except localhost.",
   "acceptance_test": "test_provider::test_fixture_miss_raises style tests exist; each named test fails when its condition is broken."},
  {"severity": "minor", "title": "N2: instruction-style ACs copied onto 2-3 cards; one asks a db card to rewrite a planning doc at stale line numbers",
   "evidence": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... INFO line: \"instruction-style 'Contract review (T-018):' ACs copied onto more than one card: 11 distinct texts\"; ['T-031', 'T-034', 'T-036']: 'Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain ...' (T-031 AC6 is a db card); ['T-029', 'T-039']: 'T-029 AC4 or a new qa card ...'.",
   "why_it_matters": "Three workers tick copies of the same doc rewrite, and nobody owns the outcome. The line references are already stale (the doc moved).",
   "fix": "One owner per instruction. The coverage-doc change belongs to the orchestrator card, not to T-031, T-034 or T-036. Replace each copied instruction with a testable AC on the card that owns the outcome.",
   "acceptance_test": "the applied-check INFO line shows no 'Contract review (T-018):' text on more than one card."}
 ],
 "whats_right": [
  "T-048 exists with deps [] and T-034, T-035, T-036 and T-037 depend on it; T-031, T-042 and T-043 got their depends_on edges (S1 test-first wiring, S2 edges).",
  "The fixture-cannot-ship rule is on the board (T-038 AC6) with the 50 seeded judge lines and SE1-SE5 named (T-037 AC6-AC7), and the regression freshness check is on T-038 AC7.",
  "The paralegal journey gaps are now ACs: edited items survive reload (T-044 AC6), two accident dates shown side by side (T-043 AC6), record 4 visible as failed (T-042 AC6, T-041 AC6)."
 ],
 "questions_for_chris": ["Is the lexicon held-out recall (LLM_VS_CODE row 16, 'a release gate') a gate you will hold to? Your answer decides whether M2 cut 3 is allowed and whether T-038 gets a metric or the table changes (finding PM6)."]}
```
