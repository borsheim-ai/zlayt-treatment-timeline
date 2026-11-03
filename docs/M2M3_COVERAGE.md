# M2 + M3 coverage (T-017, revised after T-018 contract review)

## Critical path and cut order (orchestrator)
- M2 critical path (7 cards): T-029/T-048 (tests first) → T-032 ingest → T-033 amounts/gaps → T-035 generator+judges → T-036 LLM flags → T-037 pipeline+fixtures → T-038 eval runner. Estimates ~30–45 min each with 4 workers in parallel (T-030 grounding, T-031 db, T-034 provider, T-027 lexicon run beside the chain).
- M2 critical-path total ≈ 5 h of serial work (7 cards × ~40 min) vs 3.5 h budget → **cut trigger:** if T-035 is not in review by M2 start + 2.5 h, apply cut (1), then (2).
- M2 cut order: (1) anthropic-api backend stays mocked-SDK only (deployment path, not a ship-bar metric); (2) judges #3 and #4 share one prompt file (two calls kept, so judge coverage — ship bar 4 — is unchanged); M3's first cut is T-046. No ship-bar metric is ever cut.
- M3 cut order: T-046 side-by-side → excerpt re-selection → notes sections 7–8 → R-RV-9 highlight (REQUIREMENTS §4).

## Ship bar row → card
| Ship bar | Card |
|---|---|
| 1 Grounding | T-038 (grounding_rate), T-041 (export grounding) |
| 2 Recall | T-038 |
| 3 Flags (incl. 28/73) | T-038, T-033 |
| 4 No invented facts (live backend only) | T-038, T-037 |
| 5 Reviewability (verify_quickly ≥ 4; E2E) | T-045 + M3 gate paralegal review |

Card keys are in m2m3_cards.json. "Primary" is listed first. T-027 (existing lexicon card) is a dependency of T-036 (m2-be-llm-flags), not duplicated.

## Plan self-check
Pass conditions live in each card's AC on the board (each names its test/eval/command); this table maps ownership. Numbers in AC are checked against the golden set by T-038 (`--check-spec`) and the qa test-first cards (T-029, T-048, T-039).

## R-ID -> card
| R-ID | Cards |
|---|---|
| R-IN-1 | T-032 (m2-be-ingest-dates), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
| R-IN-2 | T-042 (m3-fe-input-timeline), T-039 (m3-qa-tests-first) |
| R-IN-3 | T-032 (m2-be-ingest-dates), T-038 (m2-qa-eval-runner) |
| R-IN-4 | T-032 (m2-be-ingest-dates), T-040 (m3-be-api-review), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
| R-IN-5 | T-032 (m2-be-ingest-dates), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
| R-TL-1 | T-035 (m2-be-generator-judges), T-038 (m2-qa-eval-runner), T-042 (m3-fe-input-timeline) |
| R-TL-2 | T-030 (m2-be-grounding), T-029 (m2-qa-unit-first) |
| R-TL-3 | T-032 (m2-be-ingest-dates), T-035 (m2-be-generator-judges) |
| R-TL-4 | T-035 (m2-be-generator-judges), T-038 (m2-qa-eval-runner) |
| R-TL-5 | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
| R-TL-6 | T-040 (m3-be-api-review), T-042 (m3-fe-input-timeline) |
| R-TL-7 | T-032 (m2-be-ingest-dates), T-038 (m2-qa-eval-runner) |
| R-TL-8 | T-030 (m2-be-grounding), T-044 (m3-fe-edit-export) |
| R-TL-9 | T-032 (m2-be-ingest-dates), T-035 (m2-be-generator-judges) |
| R-TL-10 | T-030 (m2-be-grounding), T-040 (m3-be-api-review) |
| R-FL-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
| R-FL-2 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
| R-FL-3 | T-036 (m2-be-llm-flags) |
| R-FL-4 | T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner) |
| R-FL-5 | T-030 (m2-be-grounding), T-036 (m2-be-llm-flags) |
| R-FL-6 | T-043 (m3-fe-flags-charges-review) |
| R-FL-7 | T-036 (m2-be-llm-flags), T-043 (m3-fe-flags-charges-review) |
| R-FL-8 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
| R-CH-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
| R-CH-2 | T-033 (m2-be-amounts-gaps), T-035 (m2-be-generator-judges) |
| R-CH-3 | T-033 (m2-be-amounts-gaps), T-043 (m3-fe-flags-charges-review), T-041 (m3-be-export) |
| R-CH-4 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
| R-CH-5 | T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review), T-039 (m3-qa-tests-first) |
| R-CH-6 | T-033 (m2-be-amounts-gaps) |
| R-CH-7 | T-040 (m3-be-api-review), T-039 (m3-qa-tests-first) |
| R-RV-1 | T-043 (m3-fe-flags-charges-review), T-045 (m3-qa-e2e-journey) |
| R-RV-2 | T-040 (m3-be-api-review), T-044 (m3-fe-edit-export), T-039 (m3-qa-tests-first) |
| R-RV-3 | T-040 (m3-be-api-review), T-044 (m3-fe-edit-export) |
| R-RV-4 | T-043 (m3-fe-flags-charges-review), T-045 (m3-qa-e2e-journey) |
| R-RV-5 | T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
| R-RV-6 | T-032 (m2-be-ingest-dates), T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner), T-045 (m3-qa-e2e-journey) |
| R-RV-7 | withdrawn (D-011); no card |
| R-RV-8 | T-031 (m2-db-schema), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
| R-RV-9 | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline), T-043 (m3-fe-flags-charges-review) |
| R-EX-1 | T-041 (m3-be-export), T-045 (m3-qa-e2e-journey) |
| R-EX-2 | T-041 (m3-be-export), T-038 (m2-qa-eval-runner) |
| R-EX-3 | T-041 (m3-be-export) |
| R-EX-4 | T-041 (m3-be-export) |
| R-EX-5 | T-044 (m3-fe-edit-export) |
| R-EX-6 | T-041 (m3-be-export), T-044 (m3-fe-edit-export), T-038 (m2-qa-eval-runner) (spec = golden check) |
| R-EX-7 | T-041 (m3-be-export), T-044 (m3-fe-edit-export) |
| R-EX-8 | T-041 (m3-be-export) |
| R-EX-9 | T-044 (m3-fe-edit-export) |
| R-CO-1 | T-029 (m2-qa-unit-first) (boundary test), T-041 (m3-be-export) |
| R-CO-2 | T-031 (m2-db-schema), T-037 (m2-be-pipeline-cli), T-045 (m3-qa-e2e-journey) |
| R-CO-3 | T-038 (m2-qa-eval-runner) |
| R-CO-4 | T-040 (m3-be-api-review) (demo gate). INST half is M4 (non-goal for M2/M3) |
| R-CO-5 | T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
| R-CO-6 | T-034 (m2-be-provider-fixtures) |
| R-CO-7 | T-038 (m2-qa-eval-runner) |
| R-CO-8 | non-goal for M2/M3 cards: orchestrator logs SCOPE_CUTS; T-046 (m3-fe-side-by-side) AC logs R-ST-1 |
| R-CO-9 | T-034 (m2-be-provider-fixtures) |
| R-SU-1 .. R-SU-5 | non-goal for M2/M3: M4/M5 submission cards |
| R-ST-1 | T-046 (m3-fe-side-by-side) |

## LLM_VS_CODE row -> card
| Row | Step | Cards |
|---|---|---|
| 1 | Split, merge duplicates | T-032 (m2-be-ingest-dates) |
| 2 | Date parsing | T-032 (m2-be-ingest-dates) |
| 3 | Date and provider by code | T-032 (m2-be-ingest-dates) |
| 4 | Generator + rungs 1-2 | T-035 (m2-be-generator-judges), T-030 (m2-be-grounding) |
| 5 | Clinical facts list: not built | T-035 (m2-be-generator-judges) (schema test enforces the omission) |
| 6 | Find every amount | T-033 (m2-be-amounts-gaps) |
| 7 | Amount class | T-033 (m2-be-amounts-gaps) (rules), T-035 (m2-be-generator-judges) (judge #2) |
| 8 | Running total | T-033 (m2-be-amounts-gaps), T-041 (m3-be-export), T-043 (m3-fe-flags-charges-review) |
| 9 | Gap > 30 days | T-033 (m2-be-amounts-gaps), T-037 (m2-be-pipeline-cli) |
| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps): accident date and provider names, code only (D-025) |
| 11 | Semantic conflicts + judge #3 | T-036 (m2-be-llm-flags) |
| 12 | Pre-existing | T-036 (m2-be-llm-flags) |
| 13 | Causation language | T-036 (m2-be-llm-flags) |
| 14 | Flag wording by code | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
| 15 | Numbers in summary/edit | T-030 (m2-be-grounding), T-040 (m3-be-api-review) |
| 16 | Injection scan | T-032 (m2-be-ingest-dates), T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner) |
| 17 | Confidence state | T-030 (m2-be-grounding) |
| 18 | Why? sentence | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline) |
| 19 | Sort, filter, export | T-041 (m3-be-export), T-045 (m3-qa-e2e-journey) |
| 20 | Audit trail | T-031 (m2-db-schema), T-034 (m2-be-provider-fixtures), T-037 (m2-be-pipeline-cli) |

Unmapped: none.