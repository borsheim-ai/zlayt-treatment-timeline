# T-017 round-3: product-manager-reviewer apply-check of reviews/T-017-product-manager-r2.md

**Verdict: changes.** 0 blockers, 3 majors, 2 minors, 1 nit.

The round-2 review had 4 majors and 1 minor. Status now:

| Round-2 finding | Status | Evidence |
|---|---|---|
| Major 1: coverage counts R-ID mentions, not pass conditions | NOT APPLIED (F1) | Owner probe: 1 of 4 named R-IDs has a mapped card carrying its pass condition (`artifacts/review-evidence/T-017-r3-owner-probe.out.txt`). The column was declined in prose, with no recorded decision. |
| Major 2: three ACs contradict golden or REQUIREMENTS; no plan self-check | PARTLY APPLIED | The three ACs are fixed in place (T-039 AC1, T-039 AC2, T-033 AC1). The self-check sentence is there, but it describes a control that no card builds (F2). |
| Major 3: 11 unowned test files; row 10 engine | APPLIED | Probe `qa:NONE count = 0` (`artifacts/review-evidence/T-018-r3-applied-check.out.txt` lines 2-37). Row 10 is code: D-025 (`memory/ORCHESTRATOR_DECISIONS.md:33`), coverage `:97`, LLM_VS_CODE `:38`. |
| Major 4: critical path, budget, cut order, ship-bar trace | PARTLY APPLIED (F3) | Applied: the 7-card chain (`:4`), the ship-bar to card table (`:8-15`), per-card estimates on all 20 cards, the stale 4 h lines deleted, cut (3) removed. Not applied: the total and cut trigger, the per-cut ship-bar mapping, and the claim "never touches ship-bar items" (cut 2 does). |
| Minor: T-017 AC2 evidence "rows 1-20 all mapped" | NOT APPLIED (F4) | `board.py show T-017` AC2 evidence unchanged. |

**Note on the applied-check script.** `T-018-r2-applied-check.py` marks T17-1a ("coverage has pass-condition column") and T17-2a ("plan self-check") APPLIED. Both matches are a sentence in the coverage doc (`docs/M2M3_COVERAGE.md:20` and `:19`), not the requested column or a working control. I am overriding those two results here and in `reviews/T-018-product-manager-r2.md`. I have not edited the script, so its output stays as the orchestrator received it.

## Findings

**F1 (major). The R-ID rows still name the wrong owners for three dealbreaker pass conditions.**
- Evidence: `artifacts/review-evidence/T-017-r3-owner-probe.py` output: `[FAIL] R-FL-2 row=['T-033','T-036'] ac_owners=['T-043'] mapped_owners=[]`; `[FAIL] R-CO-9 row=['T-034'] ac_owners=['T-041','T-042'] mapped_owners=[]`; `[FAIL] R-EX-4 row=['T-041'] ac_owners=['T-039','T-044'] mapped_owners=[]`; `[PASS] R-RV-8` (T-043 AC3 carries "edit-note" and "reload"). The rows are `docs/M2M3_COVERAGE.md:41`, `:81`, `:67`. The owning ACs are T-043 AC6 ("Date of accident per intake form: 2026-01-19", side by side), T-042 AC6 and T-041 AC6 ("could not process"), T-039 AC6 and T-044 AC6 ("EDITED ITEMS with original and new text"). The column was declined at `docs/M2M3_COVERAGE.md:20`: "Pass conditions live in each card's AC on the board ... this table maps ownership." No decision is recorded: `grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md` returns nothing.
- Why it matters: this is the defect round 1 was about. A reader who looks up "could not process" (R-CO-9) or "EDITED ITEMS" (R-EX-4) finds a card that does not test the visible behaviour. The sentence at `:20` says the matrix maps ownership, and for these three rows it does not. T-017 AC1 ("covered by >=1 M2/M3 card AC") is still a mention test.
- Fix: add the owning cards to rows `:41`, `:67`, `:81`, or add the "Pass condition -> AC" column the round-1 fix asked for. If the column is declined, record the decision with its reason in `memory/ORCHESTRATOR_DECISIONS.md` (the T-018 AC2 rule says rejected majors need a recorded reason).
- Acceptance test: `.venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project` prints `RESULT: 4 of 4`.

**F2 (major). The "plan self-check" names a control no card builds.**
- Evidence: `docs/M2M3_COVERAGE.md:20`: "Numbers in AC are checked against the golden set by T-038 (`--check-spec`) and the qa test-first cards (T-029, T-048, T-039)." `board.py show T-038` AC2: "`python -m evals.run --check-spec` compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt". That checks the spec's export text, not AC numbers. `grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/` finds only the notes in T-017 and a lexicon line in T-027. No AC on any card diffs an AC's numbers against `evals/golden`.
- Why it matters: the round-1 fix asked for a real check ("every number in an AC is diffed against evals/golden expected values before in_review"). The doc now says the check exists and names the wrong card for it. A worker who trusts line 20 will not write the numbers check, and the $8,390/$420 error this round fixed by hand could come back.
- Fix: add an AC to T-038, for example "`python -m evals.run --check-acs` diffs every number quoted in an M2/M3 card AC that matches a golden value against evals/golden expected JSON; a seeded wrong number in a temp copy makes it fail (tests/unit/test_ac_numbers.py)". Or delete the sentence and name the risk in SCOPE_CUTS.
- Acceptance test: T-038 has an AC naming `--check-acs` (or the sentence is removed), and `grep -c 'checked against the golden set by T-038' docs/M2M3_COVERAGE.md` is 0 or the AC exists.

**F3 (major). The cut order says it "never touches ship-bar items", and cut (2) does.**
- Evidence: `docs/M2M3_COVERAGE.md:5`: "M2 cut order (never touches ship-bar items): (1) ... (2) judge #4 merged into judge #3 prompt; (3) T-046 side-by-side is M3's first cut; no ship-bar item is ever cut." `docs/LLM_VS_CODE.md:40` (row 12): "**judge 4** confirms the category" for pre_existing. Ship-bar row 3 (`spec/REQUIREMENTS.md:327`) measures "Per flag type (gap, conflict, pre_existing, causation): precision >= 0.9 and recall >= 0.9". Merging judge #4 into judge #3 changes the pre_existing path. The doc has no per-cut ship-bar mapping and no trigger; `grep -n -i trigger docs/M2M3_COVERAGE.md` is empty. The M2 budget (`docs/CONTRACT.md:300`, 3.5 h) is not stated against the 7-card chain (same as T-018 F1).
- Why it matters: the cut order is the plan's answer to "what goes when we run out of time". If it says a cut is safe when it is not, the first lever pulled can break the flag gate with no test failing.
- Fix: rewrite `:5` so each cut names the ship-bar row it touches, or "none" with the reason. Either drop "never touches ship-bar items", or keep cut (2) only with a T-036 AC that holds pre_existing precision and recall on the fixture after the merge. Add the trigger sentence from T-018 F1.
- Acceptance test: every cut in `docs/M2M3_COVERAGE.md:5` names a ship-bar row or "none (reason)"; `grep -c 'never touches ship-bar items' docs/M2M3_COVERAGE.md` is 0 unless each cut carries a row.

**F4 (minor, not gating). T-017 AC2 evidence still says "rows 1-20 all mapped".**
- Evidence: `board.py show T-017` AC2 evidence: "docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped". Row 19 maps to T-041 and T-045, both M3 (`docs/M2M3_COVERAGE.md:106`); row 15 edit half maps to T-040, M3 (`:102`).
- Fix: reword to "rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design".
- Acceptance test: `board.py show T-017` AC2 evidence does not contain "rows 1-20 all mapped".

**F5 (minor, not gating). Appended ACs now duplicate in-place text.**
- Evidence: T-039 AC7 repeats AC2 ("dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9"); T-039 AC9 repeats AC1 ("on case_07 with $420 accepted ... $420.00"); T-036 AC7 and AC10 are identical ("decided by D-025: provider-name conflicts come from code").
- Why it matters: no contradiction, but two ACs with the same text make it unclear which one is the contract, and round 2 asked for the appended copies to be deleted.
- Fix: delete T-039 AC7 and AC9 and T-036 AC10.
- Acceptance test: `board.py show T-039` and `T-036` have no two ACs with the same text.

**F6 (nit). The critical path has a tie the doc does not name.**
- Evidence: `board.py show T-034` depends_on includes T-031 and T-048; T-031 depends on T-029. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. `docs/M2M3_COVERAGE.md:4` names only the T-032/T-033 route.
- Fix: add "(ties with T-029 -> T-031 -> T-034 -> ... -> T-038)" to `:4`.

## Things that landed and should not break
- T-039 AC1 and AC2 are fixed in place: "$420.00" for case_07 and "dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9" (matches `spec/REQUIREMENTS.md:125`, R-EX-7). T-033 AC1 no longer says "only".
- Row 10 is decided and consistent across three files (D-025, `docs/LLM_VS_CODE.md:38`, `docs/M2M3_COVERAGE.md:97`); the probe finds 0 unowned test files.
- The ship-bar to card table (`docs/M2M3_COVERAGE.md:8-15`) and per-card estimates on all 20 cards are in place.

## Exercised
- Read `personas/product-manager.md`, the memory index and its files, and `reviews/T-017-product-manager.md` and `reviews/T-017-product-manager-r2.md` (the findings and the fix text).
- `.venv/bin/python tools/board.py validate` -> `ok (48 file(s))`.
- `board.py show` on T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-044, T-045.
- `cat -n docs/M2M3_COVERAGE.md` (lines 1-20, 22-109); `sed -n` of `docs/LLM_VS_CODE.md` rows 10, 12, 16; `spec/REQUIREMENTS.md` lines 98, 125, 143, 319-331 (R-RV-8, R-EX-7, R-CO-9, section 7); `docs/CONTRACT.md:300`.
- `grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md` (no hits); `grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/` (no AC owner).
- `.venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project` -> 1 of 4 PASS; output saved to `artifacts/review-evidence/T-017-r3-owner-probe.out.txt`.
- `.venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py` (re-run, output read); its T17-1a and T17-2a results are overridden above.
- Not run: no app, no eval (plan review; no code exists).

```json
{"card": "T-017", "persona": "product-manager-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round-3 apply-check of reviews/T-017-product-manager-r2.md (4 majors, 1 minor, 1 nit) against docs/M2M3_COVERAGE.md, board cards T-017, T-027, T-029..T-046, T-048, docs/LLM_VS_CODE.md rows 10, 12, 16, memory/ORCHESTRATOR_DECISIONS.md D-025/D-026, spec/REQUIREMENTS.md sections 7 and R-IDs, docs/CONTRACT.md:300. No app code exists; plan review only; no eval run.",
 "exercised": [
  "read personas/product-manager.md in full; memory index and files; reviews/T-017-product-manager.md and reviews/T-017-product-manager-r2.md",
  ".venv/bin/python tools/board.py validate -> ok (48 file(s))",
  "board.py show T-017, T-018, T-027, T-033, T-034, T-036, T-038, T-039, T-043, T-044, T-045",
  "cat -n docs/M2M3_COVERAGE.md; sed of docs/LLM_VS_CODE.md rows 10, 12, 16; sed of spec/REQUIREMENTS.md lines 98, 125, 143, 319-331; docs/CONTRACT.md:300",
  "grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md -> no hits; grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/ -> no AC owner",
  ".venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project -> 1 of 4 R-IDs PASS (R-FL-2, R-CO-9, R-EX-4 FAIL); saved to artifacts/review-evidence/T-017-r3-owner-probe.out.txt",
  ".venv/bin/python artifacts/review-evidence/T-018-r2-applied-check.py re-run; T17-1a and T17-2a APPLIED results overridden (sentence matches, not the requested column or control)"
 ],
 "verdict": "changes",
 "scores": {"coverage_pass_conditions": 2, "ac_consistent_with_golden": 4, "qa_owned_tests": 5, "self_check_is_a_real_control": 1, "critical_path_and_cut_order": 2, "ship_bar_traced": 4, "board_claims_match_artifact": 2},
 "findings": [
  {"severity": "major", "title": "R-ID rows still name the wrong owners for three dealbreaker pass conditions (round-2 major 1 not applied; column declined in prose with no recorded decision)",
   "evidence": "artifacts/review-evidence/T-017-r3-owner-probe.out.txt: R-FL-2 row ['T-033','T-036'] vs AC owner T-043 (AC6, 2026-01-19 side by side); R-CO-9 row ['T-034'] vs AC owners T-041, T-042 ('could not process'); R-EX-4 row ['T-041'] vs AC owners T-039, T-044 ('EDITED ITEMS'). Rows at docs/M2M3_COVERAGE.md:41, :81, :67. Declined at docs/M2M3_COVERAGE.md:20 'Pass conditions live in each card's AC on the board ... this table maps ownership'. grep -n -i 'pass.condition' memory/ORCHESTRATOR_DECISIONS.md reviews/GATE-M1-summary.md memory/SCOPE_CUTS.md -> no hits. R-RV-8 passes (T-043 AC3 'edit-note' and 'reload').",
   "why_it_matters": "This is the defect round 1 was about: a lookup by mention says covered while the visible behaviour (could not process; edited items; two accident dates side by side) has no mapped owner. T-017 AC1 remains a mention test.",
   "fix": "Add the owning cards to the three rows (T-043 to R-FL-2; T-042 and T-041 to R-CO-9; T-039 and T-044 to R-EX-4), or add the 'Pass condition -> AC' column. If the column is declined, record the decision and reason in memory/ORCHESTRATOR_DECISIONS.md.",
   "acceptance_test": ".venv/bin/python artifacts/review-evidence/T-017-r3-owner-probe.py /Users/arsis/zlayt-pm-project prints RESULT: 4 of 4 R-IDs have a mapped owner carrying the pass condition."},
  {"severity": "major", "title": "The plan self-check names a control that no card builds",
   "evidence": "docs/M2M3_COVERAGE.md:20 'Numbers in AC are checked against the golden set by T-038 (--check-spec) and the qa test-first cards (T-029, T-048, T-039).' board.py show T-038 AC2: --check-spec 'compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt'. grep -rn -i -E 'AC numbers|every number in an AC|check-acs' board/cards/ -> only T-017 notes and a T-027 lexicon line.",
   "why_it_matters": "The round-2 fix asked for a real check on AC numbers before in_review. The doc states the check exists and names a card that does not do it. The $8,390/$420 error fixed by hand this round can return with no test failing.",
   "fix": "Add a T-038 AC: 'python -m evals.run --check-acs diffs every number in an M2/M3 card AC that matches a golden value against evals/golden expected JSON; a seeded wrong number in a temp copy makes it fail (tests/unit/test_ac_numbers.py)'. Or delete the sentence at docs/M2M3_COVERAGE.md:20 and record the risk in memory/SCOPE_CUTS.md.",
   "acceptance_test": "T-038 has an AC naming --check-acs with a failing-on-seeded-error test, or docs/M2M3_COVERAGE.md:20 no longer names T-038 as the checker."},
  {"severity": "major", "title": "The cut order says it 'never touches ship-bar items', and cut (2) does (no per-cut row, no trigger)",
   "evidence": "docs/M2M3_COVERAGE.md:5 'M2 cut order (never touches ship-bar items): ... (2) judge #4 merged into judge #3 prompt ...'. docs/LLM_VS_CODE.md:40 (row 12) '**judge 4** confirms the category' for pre_existing. spec/REQUIREMENTS.md:327 (ship-bar row 3) 'Per flag type (gap, conflict, pre_existing, causation): precision >= 0.9 and recall >= 0.9'. grep -n -i trigger docs/M2M3_COVERAGE.md -> no hits. docs/CONTRACT.md:300 'M2 ... (<= 3.5 h)' not stated against the 7-card chain.",
   "why_it_matters": "The cut order is the plan's answer to 'what goes when time runs out'. If it says a cut is safe when cut (2) changes the pre_existing path that ship-bar row 3 measures, the first lever pulled can break the flag gate with no test failing.",
   "fix": "Rewrite docs/M2M3_COVERAGE.md:5 so each cut names the ship-bar row it touches (or 'none' with the reason). Either drop 'never touches ship-bar items' or keep cut (2) only with a T-036 AC holding pre_existing precision and recall on the fixture after the merge. Add the total-and-trigger sentence from T-018 F1.",
   "acceptance_test": "Every cut in docs/M2M3_COVERAGE.md:5 names a ship-bar row or 'none (reason)'; grep -c 'never touches ship-bar items' docs/M2M3_COVERAGE.md is 0 unless each cut carries a row."},
  {"severity": "minor", "title": "T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-2 minor not applied)",
   "evidence": "board.py show T-017 AC2 evidence: \"docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped\". Row 19 maps to T-041 and T-045, both M3 (docs/M2M3_COVERAGE.md:106); row 15 edit half maps to T-040, M3 (:102).",
   "why_it_matters": "The evidence claims more than the artifact shows about M2, which is the habit the gate looks for.",
   "fix": "Reword to 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.",
   "acceptance_test": "board.py show T-017 AC2 evidence does not contain 'rows 1-20 all mapped'."},
  {"severity": "minor", "title": "Appended ACs now duplicate in-place text (T-039 AC7/AC2, T-039 AC9/AC1, T-036 AC7/AC10)",
   "evidence": "board.py show T-039: AC7 'Contract review (T-018): T-039 AC2: dismissing entry 5 and leaving entry 6 pending gives ... 7 of 9' repeats AC2; AC9 repeats AC1's '$420.00' clause. board.py show T-036: AC7 and AC10 identical ('decided by D-025: provider-name conflicts come from code (T-033)').",
   "why_it_matters": "No contradiction, but identical ACs leave it unclear which is the contract, and round 2 asked for the appended copies to be deleted.",
   "fix": "Delete T-039 AC7 and AC9 and T-036 AC10.",
   "acceptance_test": "board.py show T-039 and T-036 have no two ACs with the same text."},
  {"severity": "nit", "title": "The seven-card critical path has a tie the doc does not name",
   "evidence": "Probe depends_on: T-034 ['T-031','T-048']; T-031 ['T-029']. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. docs/M2M3_COVERAGE.md:4 names only the T-032/T-033 route.",
   "why_it_matters": "Which path is longest decides which card the cut order protects.",
   "fix": "Add '(ties with T-029 -> T-031 -> T-034 -> ... -> T-038)' to docs/M2M3_COVERAGE.md:4.",
   "acceptance_test": "docs/M2M3_COVERAGE.md:4 names both seven-card paths."}
 ],
 "whats_right": [
  "T-039 AC1 and AC2 are fixed in place: $420.00 for case_07 and 'dismissing entry 5 and leaving entry 6 pending ... 7 of 9' (matches spec/REQUIREMENTS.md:125), and T-033 AC1 no longer says 'only'.",
  "Row 10 is decided and consistent across memory/ORCHESTRATOR_DECISIONS.md:33 (D-025), docs/LLM_VS_CODE.md:38 and docs/M2M3_COVERAGE.md:97; the probe finds 0 unowned test files.",
  "The ship-bar to card table (docs/M2M3_COVERAGE.md:8-15) and per-card estimates on all 20 cards are in place."
 ],
 "questions_for_chris": []}
```
