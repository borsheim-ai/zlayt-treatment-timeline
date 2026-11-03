# T-018 round-2 apply-check: contract-review findings (product-manager-reviewer)

**Verdict: changes.** 0 blockers, 2 majors, 3 minors.

The applied-check script (`artifacts/review-evidence/T-018-r2-applied-check.py`, re-run to `T-018-r3-applied-check.out.txt`) reports 15 distinct NOT-APPLIED lines. `grep -c NOT-APPLIED` prints 30 because the MINORS block and the SUMMARY block each list the same 15. All 15 are minors, so the script's own pass rule holds. Two things the script does not test keep this from passing:

1. PM1 has three parts. The script checks the stale-text removal and the per-card estimates. It does not check the total and the cut trigger, and those are missing (F1).
2. T-018 AC2 is still ticked on the superseded verdict (F2).

I also do not accept the script's APPLIED on T17-1a and T17-2a. Those checks match a sentence, not the column or the AC control the round-1 finding asked for. The T-017 r3 review (`reviews/T-017-product-manager-r3.md`) records them.

## Status of the round-1 contract majors (CONTRACT-M2M3-product-manager, -paralegal, -staff-engineer)

| Major | Status | Evidence (checked by me, not only by the script) |
|---|---|---|
| PM1 critical path, estimates, cut order | PARTIAL | Stale 5-card path and "4 h" line gone (`docs/M2M3_COVERAGE.md:4-5`). 20 of 20 cards have an estimate line. No total and no cut trigger (F1). |
| PM2 T-027 P0 + timebox | APPLIED | `board.py show T-027`: priority "P0"; "Estimate: 40 min (timebox)." (no stop action, minor F3) |
| PM3 fixture cannot ship | APPLIED | T-038 AC4 (determinism null on fixture), AC5; T-045 AC4 now `LLM_BACKEND=claude-cli python -m evals.run` |
| PM4 regression freshness | APPLIED | T-038 AC7 `--check-fresh` and sha256 of prompts |
| PM5 verify_quickly owner | APPLIED | T-045 AC7 "M3 gate: ... scores.verify_quickly >= 4 (D-015, ship bar 5)" |
| PM6 lexicon recall gate | APPLIED | D-026 (`memory/ORCHESTRATOR_DECISIONS.md:34`) "reported, not gated"; T-038 AC9 "Per D-026 it is reported, not gated"; no "or" left. Needs Chris to confirm (question below). |
| PL1 edits survive reload | APPLIED | T-044 AC6 "EDITED ITEMS with original and new text"; T-039 AC6 |
| PL2 "7 of 9" reconciliation | APPLIED | T-039 AC2 in place: "dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9" (matches `spec/REQUIREMENTS.md:125` R-EX-7) |
| PL3 accident date as two dates | APPLIED | T-043 AC6 "Date of accident per intake form: 2026-01-19." |
| PL4 record 4 visible as failed | APPLIED | T-042 AC6 "could not process" in the tray; T-041 AC6 RECORDS NOT IN THE TREATMENT SECTION |
| S1 qa author for test files | APPLIED | Probe `qa:NONE count = 0` (applied-check out.txt lines 2-37); T-048 AC1 names 9 files; T-039 AC4 names the E2E files |
| S2 depends_on | APPLIED | T-031 ['T-029']; T-042 ['T-039']; T-043 ['T-039','T-040','T-042'] |
| S3 SDK hidden retries | APPLIED | T-034 AC7 `max_retries=0` and timeout |
| S4 fixture-miss behaviour | APPLIED | T-034 AC8 FixtureMissing; T-037 AC7 "0 FixtureMissing" |
| S5 judges #2-4 error path | APPLIED | T-035 AC7 JUDGE_UNSURE/JUDGE_UNAVAILABLE; T-036 AC9 |
| S6 boundary module list | APPLIED | T-029 AC7 "conflicts (accident date), flag_templates, injection scan" |
| S7 row-10 engine | APPLIED | D-025 (`memory/ORCHESTRATOR_DECISIONS.md:33`) code; T-033 AC6 "decided by D-025"; `docs/M2M3_COVERAGE.md:97` and `docs/LLM_VS_CODE.md:38` both say Code |
| S8 rate note by code, damages mention | APPLIED | T-033 AC7 "rate note numbers are code-derived" |
| S9 case_07 total | APPLIED | T-039 AC1 in place: "on case_07 with $420 accepted ... $420.00"; no "$8,390 incl. case_07" left (grep) |
| N1 (round 2) T-018 AC2 ticked on refuted claim | NOT APPLIED | F2 |

## Findings

**F1 (major). The M2 critical path has no total against the 3.5 h budget and no cut trigger.**
- Evidence: `docs/M2M3_COVERAGE.md:4` "Estimates ~30–45 min each with 4 workers in parallel"; `:5` lists cut levers with no trigger. `grep -n -i -E 'trigger|budget|3\.5' docs/M2M3_COVERAGE.md` prints nothing. `docs/CONTRACT.md:300` "### M2 — Core pipeline + evals green (≤ 3.5 h)". Seven serial cards at 30–45 min is 3.5 to 5.25 h.
- Why it matters: the round-1 fix had three parts. Two are done. The third (state the total and the cut trigger) is not, so at the low estimate the chain uses the whole M2 budget, at the high estimate it overruns, and nothing says when cut (1) or (2) is pulled.
- Fix: add one sentence under `:4`: "Serial chain = 7 × 30–45 min = 3.5–5.25 h against the 3.5 h M2 budget; if T-035 or T-036 is not green by estimate + N min, pull cut (1), then (2)." N is the orchestrator's call.
- Acceptance test: `grep -n -i 'trigger' docs/M2M3_COVERAGE.md` returns a line that holds the chain total in hours and a minute threshold.

**F2 (major). T-018 AC2 is done on evidence that cites the superseded verdict.**
- Evidence: `.venv/bin/python tools/board.py show T-018`: AC2 `"done": true`, evidence "every blocker/major applied ... verified by reviews/T-018-product-manager.md". That file's JSON verdict is `"changes"`.
- Why it matters: the claim is closer to true now (the script finds 0 unapplied majors), but the gate reads the cited file and finds the opposite. Round 2 raised this as N1 (major). F1 is still open, so AC2 cannot be verified yet.
- Fix: set T-018 AC2 `done: false` until F1 closes. Then change the evidence to cite this review's file, `reviews/T-018-product-manager-r2.md`, once its JSON verdict is `pass`.
- Acceptance test: `board.py show T-018` shows AC2 `done: false`, or its evidence names a review file whose JSON verdict is `pass`.

**F3 (minor, not gating). T-027 timebox has no stop action.**
- Evidence: `board.py show T-027` Description: "Estimate: 40 min (timebox)." and nothing after it. The round-1 fix asked for "at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md".
- Fix: add to the T-027 Description: "At 40 min, stop; held-out recall is reported, not gated (D-026); log the gap in memory/SCOPE_CUTS.md."
- Acceptance test: `board.py show T-027` Description contains "SCOPE_CUTS" and "reported, not gated".

**F4 (minor, not gating). Fifteen round-1 minors are still unapplied.**
- Evidence: `artifacts/review-evidence/T-018-r3-applied-check.out.txt` lines 164-193: m-PM1a, m-PM1b, m-PM1c, m-PM2, m-PL1, m-PL2, m-PL3a, m-PL3b, m-PL4, m-S1, m-S2a, m-S2b, m-S3, m-S4, m-T17.
- Why it matters: each is a check a worker can tick without proving the failure it names (cut clock, the xfail for red tests, judge input isolation, the verifier mutation guard, the network guard, the charge highlight, the banner record). None of them gates, but each is a test that would miss its failure.
- Fix: apply each as an in-place AC edit, or record a deferral in `memory/SCOPE_CUTS.md`.
- Acceptance test: re-run `T-018-r2-applied-check.py`; its NOT-APPLIED count is 0, or each unapplied item has a SCOPE_CUTS row.

**F5 (minor, not gating). Instruction ACs are copied across cards; T-036 has two identical ACs.**
- Evidence: applied-check out.txt lines 195-205 (INFO: 10 distinct texts on 2-3 cards each, e.g. ['T-031','T-034','T-036'] "Rewrite M2M3_COVERAGE.md ..."). `board.py show T-036`: AC7 and AC10 both read "Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033) ...".
- Why it matters: three workers tick copies of one instruction and nobody owns the result. The duplicate on T-036 is appended text, so a reader cannot tell which AC is the contract.
- Fix: keep one owner for the coverage-doc rewrite (the orchestrator, T-017/T-018) and delete the copies on T-031, T-034 and T-036. Delete the duplicate T-036 AC10.
- Acceptance test: the applied-check INFO line shows no 'Contract review (T-018):' text on more than one card, and `board.py show T-036` has one D-025 AC.

## Things that landed and should not break
- The lexicon gate and the row-10 engine are decided and recorded (D-025, D-026), and no "or" alternative is left on T-033 AC6 or T-038 AC9.
- The fixture cannot ship: T-038 AC4 makes determinism null on fixture and T-045 AC4 names the live backend (claude-cli); T-038 AC5 keeps ship_bar_met false when a bar is missed, and T-045 AC7 gives the M3 gate its verify_quickly key.
- The qa owner gap is closed (probe `qa:NONE count = 0`; T-048 owns the nine LLM-stage test files).

## Exercised
- Read `personas/product-manager.md`, the memory index and its files, and the three prior reviews (`reviews/T-018-product-manager.md`, `reviews/T-017-product-manager.md`, `reviews/T-017-product-manager-r2.md`).
- `.venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py . > artifacts/review-evidence/T-018-r3-applied-check.out.txt`; exit 0. `grep -c NOT-APPLIED` returned 30. Summary line 208: `checks: 68 applied=53 not-applied=15`. All 15 are minors (lines 209-223 list them).
- `.venv/bin/python tools/board.py validate` returned `ok (48 file(s))`.
- `board.py show` on T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-045. Grep over `board/cards/` for "8,390", "dismissing entry 5 gives", "Either", "$2,150 only", "rows 1-20 all mapped", "or edit LLM_VS_CODE".
- `cat -n docs/M2M3_COVERAGE.md`; grep for trigger/budget/3.5 (no hits).
- `docs/LLM_VS_CODE.md` rows 10, 12, 16 (lines 38, 40, 44); `spec/REQUIREMENTS.md` section 7 (lines 319-331) and R-EX-7 (line 125); `docs/CONTRACT.md:300`; `memory/ORCHESTRATOR_DECISIONS.md:33-34` (D-025, D-026).
- Estimate-line count on 20 cards (all ≥ 1); `evals/golden/README.md:144` ($420 for case_07).
- Not run: no app, no eval run (contract review of the plan, no code exists).

```json
{"card": "T-018", "persona": "product-manager-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round-2 apply-check of the T-018 contract review: reviews/CONTRACT-M2M3-product-manager.md (6 majors, 3 minors, 1 nit), CONTRACT-M2M3-paralegal.md (4 majors, 4 minors), CONTRACT-M2M3-staff-engineer.md (9 majors, 4 minors) against the board working tree (T-017, T-018, T-027, T-029..T-046, T-048), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, memory/ORCHESTRATOR_DECISIONS.md (D-025, D-026), spec/REQUIREMENTS.md section 7, docs/CONTRACT.md. No app code exists; no eval run.",
 "exercised": [
  "read personas/product-manager.md in full; memory index and all memory files; reviews/T-018-product-manager.md, reviews/T-017-product-manager.md, reviews/T-017-product-manager-r2.md",
  ".venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py . > artifacts/review-evidence/T-018-r3-applied-check.out.txt (exit 0); grep -c NOT-APPLIED = 30 (15 distinct lines, all minors, printed twice); summary 'checks: 68 applied=53 not-applied=15'",
  ".venv/bin/python tools/board.py validate -> ok (48 file(s))",
  "board.py show T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-045; grep -rn over board/cards/ for stale phrases (8,390; dismissing entry 5 gives; Either; $2,150 only; rows 1-20 all mapped; or edit LLM_VS_CODE)",
  "cat -n docs/M2M3_COVERAGE.md; grep -n -i -E 'trigger|budget|3\\.5' docs/M2M3_COVERAGE.md -> no hits",
  "sed of docs/LLM_VS_CODE.md rows 10, 12, 16; spec/REQUIREMENTS.md lines 319-331 and 125; docs/CONTRACT.md:300; memory/ORCHESTRATOR_DECISIONS.md:33-34",
  "estimate/timebox line count on 20 M2/M3 cards (all >= 1); evals/golden/README.md:144 ($420 case_07)"
 ],
 "verdict": "changes",
 "scores": {"contract_majors_applied": 3, "critical_path_budget_and_trigger": 2, "ship_bar_fixture_cannot_ship": 5, "lexicon_gate_decided": 5, "qa_owner_coverage": 5, "claims_match_board": 2, "paralegal_journey_acs": 4},
 "findings": [
  {"severity": "major", "title": "PM1 not fully applied: M2 critical path has no total against the 3.5 h budget and no cut trigger",
   "evidence": "docs/M2M3_COVERAGE.md:4 'Estimates ~30–45 min each with 4 workers in parallel'; :5 cut levers with no trigger; grep -n -i -E 'trigger|budget|3\\.5' docs/M2M3_COVERAGE.md prints nothing; docs/CONTRACT.md:300 '### M2 — Core pipeline + evals green (≤ 3.5 h)'; 7 serial cards x 30-45 min = 3.5-5.25 h",
   "why_it_matters": "The round-1 fix had three parts; two are done. Without the total and the trigger, the cut order cannot be executed at the moment it is needed: at the low estimate the chain uses the whole M2 budget, at the high estimate it overruns.",
   "fix": "Add one sentence under docs/M2M3_COVERAGE.md:4: 'Serial chain = 7 x 30-45 min = 3.5-5.25 h against the 3.5 h M2 budget; if T-035 or T-036 is not green by estimate + N min, pull cut (1), then (2).' N set by the orchestrator.",
   "acceptance_test": "grep -n -i 'trigger' docs/M2M3_COVERAGE.md returns a line holding the chain total in hours and a minute threshold."},
  {"severity": "major", "title": "T-018 AC2 is done on evidence that cites the superseded verdict (round-2 N1 still open)",
   "evidence": "board.py show T-018: AC2 done true, evidence 'every blocker/major applied ... verified by reviews/T-018-product-manager.md'; that file's JSON verdict is 'changes'",
   "why_it_matters": "The gate reads the cited file and finds the opposite of the claim. The claim is closer to true now, but AC2 cannot be verified until F1 closes.",
   "fix": "Set T-018 AC2 done false until F1 closes; then cite reviews/T-018-product-manager-r2.md in its evidence once that file's JSON verdict is pass.",
   "acceptance_test": "board.py show T-018 shows AC2 done false, or its evidence names a review file whose JSON verdict is pass."},
  {"severity": "minor", "title": "T-027 timebox has no stop action",
   "evidence": "board.py show T-027 Description: 'Estimate: 40 min (timebox).' with no stop rule; round-1 fix asked for 'at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md'",
   "why_it_matters": "A timebox with no stop rule leaves the lexicon card open-ended in practice.",
   "fix": "Add to the T-027 Description: 'At 40 min, stop; held-out recall is reported, not gated (D-026); log the gap in memory/SCOPE_CUTS.md.'",
   "acceptance_test": "board.py show T-027 Description contains 'SCOPE_CUTS' and 'reported, not gated'."},
  {"severity": "minor", "title": "Fifteen round-1 minors are still unapplied (non-gating)",
   "evidence": "artifacts/review-evidence/T-018-r3-applied-check.out.txt lines 164-193: m-PM1a, m-PM1b, m-PM1c, m-PM2, m-PL1, m-PL2, m-PL3a, m-PL3b, m-PL4, m-S1, m-S2a, m-S2b, m-S3, m-S4, m-T17",
   "why_it_matters": "Each named check can be ticked without proving its failure (cut clock, xfail on red tests, judge input isolation, verifier mutation guard, network guard, charge highlight, banner record). None gates, but each would miss its failure.",
   "fix": "Apply each as an in-place AC edit, or record a deferral in memory/SCOPE_CUTS.md.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-018-r2-applied-check.py: NOT-APPLIED count 0, or each unapplied item has a SCOPE_CUTS row."},
  {"severity": "minor", "title": "Instruction ACs are copied across cards; T-036 has two identical D-025 ACs",
   "evidence": "artifacts/review-evidence/T-018-r3-applied-check.out.txt lines 195-205 (10 distinct INFO texts on 2-3 cards each); board.py show T-036: AC7 and AC10 both 'Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033) ...'",
   "why_it_matters": "Several workers tick copies of one instruction with no owner for the result; the duplicate is appended text, so the contract is unclear.",
   "fix": "One owner for the coverage-doc rewrite (orchestrator); delete the copies on T-031, T-034, T-036 and the duplicate T-036 AC10.",
   "acceptance_test": "The applied-check INFO line shows no 'Contract review (T-018):' text on more than one card; board.py show T-036 has one D-025 AC."}
 ],
 "whats_right": [
  "D-025 (row 10 is code) and D-026 (lexicon recall reported, not gated) are recorded in memory/ORCHESTRATOR_DECISIONS.md:33-34, and no 'or' alternative is left on T-033 AC6 or T-038 AC9.",
  "The fixture cannot ship: T-038 AC4 makes determinism null on fixture and T-045 AC4 names the live backend (claude-cli); T-038 AC5 keeps ship_bar_met false when a bar is missed, and T-045 AC7 gives the M3 gate its scores.verify_quickly key.",
  "The qa owner gap is closed: probe qa:NONE count = 0, and T-048 owns the nine LLM-stage test files."
 ],
 "questions_for_chris": ["D-026 makes lexicon recall reported, not gated, and says the ship bar is unchanged. REQUIREMENTS section 7 row 3 still reads 'per flag type ... recall >= 0.9'. Do you accept that the gate is system-level flag recall and the lexicon recall is only reported? T-038 AC9 depends on the answer."]}
```
