# GATE M1 — Research, personas, requirements, architecture — PASS

Date: 2026-11-02 · Orchestrator synthesis · Budget 2.5 h; actual ≈ 3.5 h (review rounds; see D-024 response)

## Deliverables
| Card | Output | Reviews (rounds) | Outcome |
|---|---|---|---|
| T-008 domain research | research/chronology-practice.md, adjuster-attacks.md, texas-pi-notes.md, GLOSSARY (46 terms) | claims-adjuster (4) | pass; invented fact ("referral", "radicular") caught and removed |
| T-009 flag lexicon | app/llm/lexicon.yaml v2 (66 entries, D-018 shape) | legal-nurse + claims-adjuster (2) | debt → T-027 (held-out recall) |
| T-010/T-011 persona dossiers | personas/*.md (13), compiled into reviewer agents | PM + litigation-lead (3) / PM (2) | pass |
| T-012 PHI + AI supervision | research/phi-and-ai-supervision.md (19 sources) | privacy-compliance (3) | pass |
| T-013/T-025 requirements | spec/REQUIREMENTS.md (62 R-IDs), §6 export = golden | paralegal + PM (3) / PM (2) | debt closed via T-025 |
| T-014/T-028 architecture | memory/DECISIONS.md ADR-000a..017, docs/LLM_VS_CODE.md (20 rows), api.md | staff-engineer + privacy (3) / staff (2) | debt → M2 cards |
| T-015 golden set | evals/golden/ (sample + 9 synthetic, 40 hallucinations, 10 controls, export golden) | paralegal + legal-nurse (4) | accepted; check_golden.py green |
| T-016 compile agents | 13 reviewers compiled, drift test | staff-engineer | pass |
| T-017/T-018 M2/M3 plan + contract review | 20 M2/M3 cards, docs/M2M3_COVERAGE.md | PM+paralegal+staff contract review | edits applied (0 unapplied majors per reviewer's script) |
| T-026/T-047 board Office view (Chris) | 2D → 3D office with overhead kanban | ux (haiku) | pass |

## What review changed (selected)
- Flags never enter the letter (D-001); every letter line quotes the record (D-002); total line exact, no parenthetical (D-019).
- Gaps computed by code over all clinical-encounter dates (D-003); injected text can't reach totals (D-004/D-005, case_07).
- Dropped qualifiers → needs_review (D-022); hedges kept whole (D-021); provider conflicts are code (D-025).
- 26 orchestrator decisions in memory/ORCHESTRATOR_DECISIONS.md; scope cuts 1–19 + debt rows in memory/SCOPE_CUTS.md.

## Open blockers: 0. Debt: T-027 (lexicon), golden-export byte test (T-041/T-038), minors carried in card notes.
## Questions for Chris (non-blocking): NEEDS_CHRIS #1–#3 (key, demo-only vs live, eval budget).
