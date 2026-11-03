# CONTRACT M2/M3: product-manager-reviewer (T-018, PM lens)

**Verdict: changes.** 0 blockers, 6 majors, 3 minors, 1 nit.

The R-ID to card trace is complete. 60 of 62 R-IDs are named in some AC; R-CO-8 and R-SU-1..5 are deferred to M4/M5 in the coverage file. The plan's numbers are not. The stated critical path leaves out three cards, and the only cut listed is in M3, so nothing can absorb an M2 overrun. Ship bar 4 can be "met" by replaying fixtures. Ship bar 5 has no owner. Regression discipline (§8.3) is not an AC on the cards that write the prompts.

Evidence: `artifacts/review-evidence/T-018-contract-probe.py` and `.out.txt`. The probe parses every card file and computes R-ID coverage, the authors of each test file, and the longest dependency chain.

```json
{"card": "T-018", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "Milestone contract review (CONTRACT §7.4). AC of M2/M3 cards T-027, T-029..T-046 (board/cards at commit e5733a1), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, against spec/REQUIREMENTS.md, memory/ORCHESTRATOR_DECISIONS.md, evals/golden/README.md, docs/CONTRACT.md §5 M2/M3 and §8.3. No app exists yet (app/backend, app/db, app/frontend empty).",
 "exercised": [
  "python3 tools/board.py list --milestone M2 ; list --milestone M3 (19 cards, all ready, AC 0/5 each)",
  "python3 tools/board.py show T-027, T-029..T-046, T-017, T-016",
  "python3 -I artifacts/review-evidence/T-018-contract-probe.py -> 62 R-IDs defined; not named in any AC: R-CO-8, R-SU-1..5; 93 AC total; longest chain to T-038: T-029 -> T-032 -> T-033 -> T-035 -> T-036 -> T-037 -> T-038",
  "grep -c verify_quickly personas/paralegal.md .claude/agents/paralegal-reviewer.md -> 0 and 0",
  "sed -n 296,316p docs/CONTRACT.md (M2 <= 3.5 h, M3 <= 3.5 h); sed -n 424,427p (§8.3); CONTRACT:260 (cut at >150% of budget)",
  "wc -l evals/golden/hallucinations.jsonl hallucinations_controls.jsonl -> 40, 10",
  "grep -n 'variant E\\|forged' memory/SCOPE_CUTS.md evals/golden/* -> no hits (only docs/LLM_VS_CODE.md:21,44)",
  "read in full: spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md, docs/M2M3_COVERAGE.md, evals/golden/README.md, memory/ORCHESTRATOR_DECISIONS.md"
 ],
 "verdict": "changes",
 "scores": {"scope_fits_budget": 2, "critical_path_correct": 2, "cut_order": 2, "ac_testable": 3, "ship_bar_traced": 3, "coverage_complete": 4},
 "findings": [
  {"severity": "major", "title": "Stated M2 critical path is wrong and the only cut cannot absorb an M2 overrun",
   "evidence": "docs/M2M3_COVERAGE.md:3 'Critical path (M2): T-029 -> T-030 -> T-035 -> T-037 -> T-038 (T-036 runs beside the generator)'; :4 'about 4 h, over the 3.5 h budget. If it slips, cut ... T-046' (an M3 card). Board deps: T-036 depends_on [T-035, T-033, T-027]; T-037 depends_on [T-036, ...]; T-033 depends_on [T-029, T-032]. Probe longest chain: T-029 -> T-032 -> T-033 -> T-035 -> T-036 -> T-037 -> T-038 (7 cards, not 5). Only T-029 (1 h), T-039 (1 h) and T-046 (45 min) carry any time estimate.",
   "why_it_matters": "The 4 h figure undercounts: T-036 runs after the generator, not beside it, and two backend cards are missing from the path. A milestone can't be time-boxed without an honest path, and with no M2 cut the team either drifts past 150% (CONTRACT:260) or cuts something on the ship bar under pressure.",
   "fix": "Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.",
   "acceptance_test": "grep -n 'M2 cut order' docs/M2M3_COVERAGE.md returns a list of >= 3 items, none naming an R-ID from REQUIREMENTS §7 ship bar rows 1-4; the stated chain equals the longest depends_on chain printed by T-018-contract-probe.py."},
  {"severity": "major", "title": "A P1 researcher card gates the P0 critical path",
   "evidence": "T-036 depends_on: [\"T-035\", \"T-033\", \"T-027\"]; T-027 priority P1, role researcher, status ready, unclaimed; T-027 AC1 '>=40 sentences ... scores >=85%'. D-024(5) moves the researcher to sonnet and caps doc cards at 2 rounds.",
   "why_it_matters": "If T-027 stalls in review, T-036, T-037, T-038 and the whole M3 backend wait on it. The lexicon already exists and the LEXICON_ONLY/LLM_ONLY rule (R-FL-3) already turns lexicon weakness into visible doubt, so the hard dependency buys little.",
   "fix": "Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-036 depends_on and add a T-036 AC: 'runs against app/llm/lexicon.yaml at HEAD; lexicon recall per must-flag is reported by evals.run (see T-038 finding)'.",
   "acceptance_test": "python3 tools/board.py show T-036 shows depends_on without T-027, or T-027 shows priority P0 with a timebox."},
  {"severity": "major", "title": "Ship bar 4 can be met on a fixture replay: unsupported_count_3run and the judge metrics are not tied to a live backend",
   "evidence": "T-038 AC4 makes only determinism_3run live-only ('on fixture the field is null/not_measured'). unsupported_count_3run (ship bar 4: '0 unsupported statements across 3 repeated runs') has no such clause. T-045 AC4: '`python -m evals.run` (ship_bar_met true)' does not name a backend. T-037 AC2 records fixtures for 'sample + 9 cases' only, not for the 40 + 10 items in hallucinations.jsonl / hallucinations_controls.jsonl.",
   "why_it_matters": "Three replays of one recording always give 0 differences and the same verdicts. A ship bar that passes by construction is the 'demo looked fine' failure. hallucination_catch_rate cannot be computed on fixture at all unless those 50 judge calls are recorded, so the runner will either error or quietly skip them.",
   "fix": "T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.",
   "acceptance_test": "tests/unit/test_eval_runner.py::test_fixture_cannot_ship: a fixture-backend run writes ship_bar_met false and unsupported_count_3run 'not_measured'."},
  {"severity": "major", "title": "Regression discipline (§8.3, R-CO-6) is not an AC on the cards that write prompts, and there is no check after T-038",
   "evidence": "T-035 Description: 'The eval report required by CONTRACT 8.3 is attached once m2-qa-eval-runner exists'. T-038 depends_on T-037, which depends_on T-035 and T-036, so T-035/T-036 reach in_review before any runner exists. No AC on T-035, T-036, T-027 or T-038 checks that a later prompt, lexicon or schema change carries a fresh report. CONTRACT:426 'Any change to a prompt, model, lexicon, or schema requires re-running evals.run before in_review'.",
   "why_it_matters": "This is checklist item 14. Without it, the M2 gate report can predate the last prompt edit (red flag: 'an eval report that was not re-run after the last prompt change'), and nobody will notice.",
   "fix": "T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.",
   "acceptance_test": "Edit one byte of a prompt in a temp copy; `python -m evals.run --check-fresh` exits non-zero (tests/unit/test_eval_runner.py::test_check_fresh)."},
  {"severity": "major", "title": "Ship bar 5 (verify_quickly >= 4) has no owner in the M2/M3 plan; REQUIREMENTS §8 row 5 points at a done card that never delivered it",
   "evidence": "REQUIREMENTS §8 row 5: '`scores.verify_quickly` (D-015) must be requested in the brief ... Owner T-016'. `python3 tools/board.py show T-016` -> status done. `grep -c verify_quickly personas/paralegal.md .claude/agents/paralegal-reviewer.md` -> 0, 0. docs/M2M3_COVERAGE.md maps R-IDs and LLM rows, never ship-bar rows.",
   "why_it_matters": "Ship bar 5 is the one human criterion and the product note must report a number for it. If the M3 gate paralegal review comes back without the key, the gate can't be scored and the note's ship-bar table has a hole.",
   "fix": "Add a 'Ship bar row -> card' table to M2M3_COVERAGE.md (rows 1-4 -> T-038, row 5 -> T-045 + M3 gate). New orchestrator card (M3): 'paralegal-reviewer agent body and M3 gate brief request scores.verify_quickly 1-5 (D-015)'.",
   "acceptance_test": "grep -c verify_quickly .claude/agents/paralegal-reviewer.md >= 1; grep -n 'Ship bar' docs/M2M3_COVERAGE.md lists rows 1-5 each with a card id."},
  {"severity": "major", "title": "The phrase-list recall 'release gate' is not computed by any AC",
   "evidence": "docs/LLM_VS_CODE.md:40 row 12 'trusted only as far as its measured recall on the golden set'; :44 row 16 'phrase list, whose recall on the golden set is a release gate'; D-018 'The lexicon self-check must run over every golden case and report recall per must-flag'. T-038 AC1 metric list has no lexicon metric; T-027 AC1 measures a held-out probe set, not the golden set.",
   "why_it_matters": "The injection defence (R-RV-6) rests on the lexicon floor for cross-record flags, and the LLM/code page tells the panel this is gated. A claim the eval report doesn't support is a red flag for the product note.",
   "fix": "T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case, pooled) with R-IDs R-FL-3, R-RV-6, and state the threshold in REQUIREMENTS §7 by ADR, or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'.",
   "acceptance_test": "jq '.metrics.lexicon_recall_must_flags' evals/reports/latest.json is a number, with its R-ID next to it."},
  {"severity": "minor", "title": "Several AC can't be checked as written",
   "evidence": "T-046 AC5 'cut order ... recorded if M3 passes 100% of budget' (no clock or start time recorded anywhere); T-037 AC1 'all flag groups' (which?); T-037 AC2 '`ls tests/fixtures/llm | wc -l` > 0' (one file passes); T-040 AC5 'no access log of tokens' (no test named).",
   "why_it_matters": "A worker can tick these with evidence that proves nothing, and the gate reviewer has nothing to re-run.",
   "fix": "T-046 AC5: 'M3 start/end timestamps from board activity.jsonl are quoted in the handoff; if end - start > 3.5 h, SCOPE_CUTS gains the next row of REQUIREMENTS §4'. T-037 AC1: 'prints flag groups gap, conflict, pre_existing, causation, record_warning with counts 1/2/2/5/0'. T-037 AC2: see the fixture-coverage fix. T-040 AC5: 'test_api::test_no_token_in_logs captures uvicorn access log and asserts the token string is absent'.",
   "acceptance_test": "Each named test or command exists and fails when the condition is broken."},
  {"severity": "minor", "title": "Golden variant E (forged billing line in an unwarned record) is promised but has no card and no SCOPE_CUTS row",
   "evidence": "docs/LLM_VS_CODE.md:44 'documented as golden variant E, a qa item, not yet in the golden set'; grep 'variant E|forged' memory/SCOPE_CUTS.md evals/golden/* -> no hits.",
   "why_it_matters": "The one injection path that only the human catches is the honest limit the note should cite. Right now it is an orphan promise.",
   "fix": "Either add AC to T-038: 'golden variant E exists; eval asserts the forged $50,000 charge is verified-but-pending and absent from the total until accepted', or add a SCOPE_CUTS row and edit LLM_VS_CODE row 16.",
   "acceptance_test": "grep -n 'variant E' evals/golden/README.md memory/SCOPE_CUTS.md returns one hit."},
  {"severity": "minor", "title": "T-033 AC1 'sample yields $6,240, $185, $2,150 only' contradicts the golden A4 damages item",
   "evidence": "sample.expected.json amounts: ('A4', 'missing 3 days of work', None, 'damages'); REQUIREMENTS R-CH-2 '\"missing 3 days of work\" -> damages (no value)'; golden notes require 'DAMAGES MENTIONS' for record 5.",
   "why_it_matters": "An implementer who follows 'only' drops the damages mention, and T-041 AC2's byte-equal golden then fails for a reason nobody planned for.",
   "fix": "T-033 AC1: 'sample yields currency amounts $6,240, $185, $2,150 and one damages mention (record 5, value null), nothing else'.",
   "acceptance_test": "test_amounts::test_sample_amounts asserts the four items by id and class."},
  {"severity": "nit", "title": "Endpoint path spelling",
   "evidence": "T-041 AC4 'GET /api/cases/{id}/export'; memory/contracts/api.md:266 'GET /api/cases/{token}/export'.",
   "why_it_matters": "This is cosmetic, but api.md is the contract.", "fix": "Use {token}.", "acceptance_test": "grep '{id}' in the T-041 card returns nothing."}
 ],
 "whats_right": [
  "R-ID trace is complete: 60/62 named in AC text, the 6 others explicitly deferred to M4/M5 in M2M3_COVERAGE.md",
  "Test-first golden for export: T-041 AC2 and T-044 AC5 require byte equality with sample.export.expected.txt on the fixture backend",
  "Stretch discipline is right: one item, 45-min timebox, start-only-when-done, cut-first, and the R-RV-9 modal stays core"
 ],
 "questions_for_chris": []}
```
