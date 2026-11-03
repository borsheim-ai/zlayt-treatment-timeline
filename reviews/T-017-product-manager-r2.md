# T-017 round 2: product-manager-reviewer apply-check of the round-1 plan findings

**Verdict: changes.** 0 blockers. 4 majors from `reviews/T-017-product-manager.md` are not applied (one of them is only partly applied). Plus 1 minor and 1 nit. Evidence comes from the same run as the T-018 review: `artifacts/review-evidence/T-018-r2-applied-check.py`, output in `artifacts/review-evidence/T-018-r2-applied-check.out.txt`.

What landed: the M2 cut order (`docs/M2M3_COVERAGE.md:5`), the ship-bar to card table (`:8-15`), the seven-card critical path in `:4`, T-048 as the qa card for LLM-stage tests, and T-027 at P0. What did not: the pass-condition column, the in-place AC fixes, the qa owner gap (11 files left), the row-10 decision, and the stale chain text that still sits in the same doc.

| Round-1 finding | Status | Evidence (verbatim) |
|---|---|---|
| Major 1: coverage counts mentions, not pass conditions | NOT APPLIED | `docs/M2M3_COVERAGE.md:22` "`| R-ID | Cards |`", no pass-condition column (T17-1a). |
| Major 2: three AC contradict golden or REQUIREMENTS; plan self-check | NOT APPLIED | T-039 AC1 still "'Billed charges stated in these records: $8,390.00' incl. case_07" (S-9a); T-039 AC2 still "dismissing entry 5 gives ... and 7 of 9" (PL-2b); T-033 AC1 still "$2,150 only" (S-8b). No plan self-check line in the coverage doc (T17-2a). |
| Major 3: unowned validation; row 10 engine | NOT APPLIED | Probe "qa:NONE count = 11". `docs/M2M3_COVERAGE.md:96` "T-036 (m2-be-llm-flags) (provider variants)"; `docs/LLM_VS_CODE.md:38` row 10 "...the same provider spelled two ways | **Code**"; no decision recorded (S-7c). |
| Major 4: critical path, budget, cut order, ship-bar trace | PARTLY APPLIED, NOT APPLIED AS A WHOLE | Applied: `:4` seven-card chain, `:5` M2 cut order, `:8-15` ship-bar table. Not applied: `:18` "Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 ..." and `:19` "This runs about 4 h, over the 3.5 h budget." still there (T17-4a/b; PM1). Cut `:5` item (3) "lexicon held-out target lowered from 85% to reported" conflicts with `docs/LLM_VS_CODE.md:44` "...whose recall on the golden set is a release gate" (T17-4c; PM6). |
| Minor: T-017 AC2 evidence overstates | NOT APPLIED | `python3 tools/board.py show T-017` AC2 evidence still "rows 1-20 all mapped" (m-T17); row 19 is M3 at `docs/M2M3_COVERAGE.md:105` and row 15 edit half at `:101`. |

## Findings

```json
{"card": "T-017", "persona": "product-manager-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round-2 apply-check of reviews/T-017-product-manager.md (4 majors, 1 minor) against the current plan: docs/M2M3_COVERAGE.md, board/cards T-027, T-029..T-039, T-041..T-048 (AC text and depends_on), docs/LLM_VS_CODE.md rows 10, 12, 16, evals/golden/README.md, spec/REQUIREMENTS.md section 7. No app code exists; plan review only.",
 "exercised": [
  "read reviews/T-017-product-manager.md in full (round-1 findings and the exact fix text)",
  "python3 tools/board.py show T-017 (AC1, AC2 evidence and round-1 notes); show T-018 Handoff",
  "cat -n docs/M2M3_COVERAGE.md (lines 3-19, 22, 84-108)",
  "python3 tools/board.py show on T-027, T-029..T-039, T-041..T-048 (AC lines, depends_on, Descriptions) to test each fix",
  "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt: T17-1a, T17-2a, T17-3, T17-4a/b/c, m-T17 (plus the card checks it depends on, S-7b, S-9a, PL-2b, S-8b); probe qa:NONE = 11; longest chain T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029",
  "probe depends_on: T-034 ['T-031', 'T-048'] and T-031 ['T-029'] (second seven-card path)",
  "grep -n 'row 10|row 16|release gate' docs/LLM_VS_CODE.md (rows 16 line 44 'release gate'); grep case_05 across docs, memory, spec (no decision)",
  "python3 tools/board.py validate -> ok (48 file(s)) before writing this review"
 ],
 "verdict": "changes",
 "scores": {"coverage_pass_conditions": 2, "ac_consistent_with_golden": 2, "qa_owned_tests": 2, "critical_path_and_cut_order": 2, "ship_bar_traced": 3},
 "findings": [
  {"severity": "major", "title": "Round-1 major 1 not applied: coverage still counts R-ID mentions; no pass-condition column",
   "evidence": "docs/M2M3_COVERAGE.md:22 '| R-ID | Cards |' (header unchanged, no pass-condition column; applied-check T17-1a: no match). The R-RV-8 test input 'accept 3 items, edit 1, reload' now has an AC (T-044 AC6, 'reload -> edited summary and \"edited\" label persist'), but the matrix does not point to it.",
   "why_it_matters": "T-017 AC1 was ticked by looking up mentions. Without a pass-condition column, the next R-ID can be marked covered by a card that never tests its REQUIREMENTS input, which is how the lost-edit and merged-date cases got through round 1.",
   "fix": "Add a 'Pass condition -> AC' column to docs/M2M3_COVERAGE.md for every R-ID row: quote the REQUIREMENTS test input and cite the AC id. Start with R-RV-8 -> T-044 AC6, R-CO-9 -> T-042 AC6 and T-041 AC6, R-EX-4(10) -> T-044 AC6 and T-039 AC6, R-FL-2(a) -> T-043 AC6.",
   "acceptance_test": "Every R-ID row in docs/M2M3_COVERAGE.md has a non-empty pass-condition cell; each cell quotes the REQUIREMENTS test input and names an AC that contains it (grep the AC text)."},
  {"severity": "major", "title": "Round-1 major 2 not applied: three ACs still contradict golden or REQUIREMENTS in place; no plan self-check",
   "evidence": "python3 tools/board.py show T-039 AC1: 'total line exactly \"Billed charges stated in these records: $8,390.00\" incl. case_07 with a rate present' (S-9a). T-039 AC2: 'dismissing entry 5 gives \"Record 5 ... dismissed\" and 7 of 9' (PL-2b). T-033 AC1: 'sample yields $6,240, $185, $2,150 only' (S-8b). The corrected wording exists only in appended ACs (T-039 AC9, T-039 AC7, T-033 AC7). docs/M2M3_COVERAGE.md has no plan self-check line (T17-2a).",
   "why_it_matters": "Under test-first, a card that contradicts itself is one the implementer will 'fix' by editing the test, which is the thing the plan says must not happen. The golden says case_07 total is $420 (evals/golden/README.md:144).",
   "fix": "Edit T-039 AC1, T-039 AC2 and T-033 AC1 in place to the corrected text and delete the appended duplicates (T-039 AC7, AC9). Add to docs/M2M3_COVERAGE.md: 'Plan self-check: every number in an AC is diffed against evals/golden expected values before in_review.'",
   "acceptance_test": "board.py show T-039 contains no 'incl. case_07' next to '$8,390.00', no 'dismissing entry 5 gives'; T-033 AC1 has no 'only' next to the three amounts; docs/M2M3_COVERAGE.md contains the self-check sentence."},
  {"severity": "major", "title": "Round-1 major 3 not applied: 11 test files still have no qa author; LLM_VS_CODE row 10 and the coverage row disagree",
   "evidence": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ...: 'qa:NONE count = 11 -> [test_api, test_charges, test_edit, test_export_ui, test_flags_panel, test_input, test_keyboard_mobile, test_review_matrix, test_side_by_side, test_source_record, test_timeline]' (T-048 covers 9 of 20). docs/M2M3_COVERAGE.md:96 '| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |' against docs/LLM_VS_CODE.md:38 '...the same provider spelled two ways | **Code**'. No ADR or decision (S-7c).",
   "why_it_matters": "T-017 AC2 says each card AC names its test. Eleven named test files have no author, and the engine for provider conflicts is still unresolved, so an implementer can produce the same conflict twice.",
   "fix": "Name the 11 files by path on T-039 (or T-048) with the R-IDs each covers. Decide row 10 by ADR or by a code AC on T-033, and make docs/M2M3_COVERAGE.md row 10 match the decision.",
   "acceptance_test": "The applied-check prints 'qa:NONE count = 0'; coverage row 10 and LLM_VS_CODE row 10 name the same engine."},
  {"severity": "major", "title": "Round-1 major 4 not applied as a whole: the doc still has two critical paths, no per-card estimates, and a cut that touches the lexicon gate",
   "evidence": "docs/M2M3_COVERAGE.md:4 'M2 critical path (7 cards): T-029/T-048 (tests first) -> T-032 ... -> T-038 eval runner.' (applied; matches the probe chain). But :18 'Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 ... -> T-038' and :19 'This runs about 4 h, over the 3.5 h budget.' remain (T17-4a/b). Per-card estimates absent on 18 of 20 cards (PM1). Cut :5 item (3) 'lexicon held-out target lowered from 85% to reported' vs docs/LLM_VS_CODE.md:44 '...recall on the golden set is a release gate' (T17-4c).",
   "why_it_matters": "A reader who reaches line 18 gets a different critical path and a '4 h, over budget' verdict. The table at :8-15 and the cut order at :5 are right in shape, but the cut order claims it 'never touches ship-bar items' while cut (3) lowers the floor under flag recall that ship-bar row 3 measures.",
   "fix": "Delete docs/M2M3_COVERAGE.md lines 18-19. Add 'Estimate: N min' to each card Description (PM1). Resolve the lexicon gate (PM6) before keeping cut (3), and state which ship-bar row each cut touches.",
   "acceptance_test": "grep -c 'T-030 (m2-be-grounding) -> T-035' docs/M2M3_COVERAGE.md = 0; estimates present on all 20 M2/M3 cards; the lexicon gate decision is recorded in ORCHESTRATOR_DECISIONS.md."},
  {"severity": "minor", "title": "T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-1 minor, not reworded)",
   "evidence": "python3 tools/board.py show T-017, AC2 evidence: \"docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval\" (m-T17). docs/M2M3_COVERAGE.md:105 row 19 maps to T-041 and T-045, both M3 cards; :101 row 15 edit half maps to T-040 (M3).",
   "why_it_matters": "The evidence claims more than the artifact shows about M2, which is the habit the gate looks for.",
   "fix": "Reword the AC2 evidence: 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.",
   "acceptance_test": "board.py show T-017 AC2 evidence does not contain 'rows 1-20 all mapped'."},
  {"severity": "nit", "title": "The seven-card critical path has a tie that the doc does not mention",
   "evidence": "Probe depends_on: T-034 ['T-031', 'T-048']; T-031 ['T-029']. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. docs/M2M3_COVERAGE.md:4 names only the T-032/T-033 route.",
   "why_it_matters": "Which path is longest decides which card the cut order protects. A reader can't tell from line 4 which path to watch.",
   "fix": "Add one clause to :4: 'ties with T-029 -> T-031 -> T-034 -> ... -> T-038'.",
   "acceptance_test": "docs/M2M3_COVERAGE.md:4 names both seven-card paths, or the probe shows one longest path."}
 ],
 "whats_right": [
  "The M2 cut order and the ship-bar to card table are on the page (docs/M2M3_COVERAGE.md:5 and :8-15), so the gate can point at them.",
  "T-048 is the qa card for the LLM-stage tests with deps []; T-034, T-035, T-036 and T-037 depend on it.",
  "T-027 is P0 and T-036 keeps its dependency, so the lexicon work sits on the path it gates."
 ],
 "questions_for_chris": ["Is the lexicon held-out recall (LLM_VS_CODE row 16, 'a release gate') a gate you will hold to? It decides whether M2 cut (3) is allowed and whether T-038 gets a metric or the table changes."]}
```
