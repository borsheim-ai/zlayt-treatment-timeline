# T-071 review: cut the patient_report speaker chip (D-040), claims-adjuster (Gary Pruitt persona)

Scope: commit a27e3a4 (T-071 chip cut). It contains the flags.py part, which landed in ancestor 59c7edb. I extracted a27e3a4 with `git archive` into `artifacts/review-evidence/T-071-tree-a27e3a4` and ran the deterministic checks there. I also ran the probe and the unit tests on the live tree. The live tree is dirty outside T-071's files, and T-072 (in progress, backend) is editing `app/backend/flag_templates.py` now, so I did not review the live state of T-072 files. Commit d148e0f is listed on the card but is later than a27e3a4 and touches only ingest/pipeline (T-066), so it is out of scope.

Model: the system prompt expects `claude-opus-5-5`, but I am running as `claude-haiku-5-5`. The record uses the actual model.

**Verdict: changes.** No blockers. The product path is clean: no code sets or branches on `source_kind` = patient_report, and the 33 probe rows all come out as plain records. Two majors keep the card from passing. Both concern what the card claims about AC1 and the harness, not the product code.

## What I checked

1. **Chip removal in app/ (grep, live and a27e3a4).** `patient_report` as a source_kind value now appears only in lexicon category names, flag templates and export labels. Those are T-072 scope (below). `has_self_report` and `patient_report_spans` are gone. `flags.js:66` renders `RV.chips(f)` only. `rv-selfreport` is still in `review.css:27`, but `review.js:276` reuses it for the "Entered by reviewer" chip, which is not a speaker label. No `app/` code reads `source_kind`; the frontend hits are mock data set to `"record"`.
2. **Setters.** `flags.py:61`, `generator.py:80` and `present.py:45` all set `source_kind` = "record" (a27e3a4).
3. **33-row probe (adapted: constructor plus lexicon path, `expect_chip` = False for all rows).** `artifacts/review-evidence/T-071-claims-adjuster-probe-a27e3a4.out.txt`: `SUMMARY rows=33 no_chip_ok=33 miss=0`. The live tree gives the same 33/33.
4. **Unit tests.** `tests/unit/test_flags_pass.py` and `tests/unit/test_flags_sample.py` in the a27e3a4 tree: `35 passed` (`artifacts/review-evidence/T-071-pytest-a27e3a4.out.txt`). Live `test_flags_pass.py`: `22 passed`.
5. **Lexicon selfcheck.** a27e3a4 tree: `RESULT: PASS`, production chip 18/18, held-out 115/115 (`T-071-selfcheck-a27e3a4.out.txt`). The live tree also PASSes, but with a probe FN (finding 3).
6. **Golden checker.** `evals/golden/check_golden.py` in the a27e3a4 tree prints `golden OK` (it still requires the withdrawn label; finding 1).
7. **Eval fixture run.** `evals.run --backend fixture --runs 3` on a27e3a4 and on its parent 59c7edb: `ship_bar_met: False` on both (finding 2).
8. **Title probe on non-patient speakers.** Eight sentences (wife, EMS, husband, family, mother, witness, plus the record-9 patient sentence) through `flags.lexicon_flags`. No flag was raised on a non-patient speaker. The record-9 sentence gives `causation / patient_report / record / "Patient self-report"` (`T-071-title-probe-a27e3a4.out.txt`). The speaker-label title is in T-072 scope.
9. **Not run:** the full `tests/unit` suite (card says 933), e2e, and a browser or curl check of the flags panel. The "no chip on screen" result comes from reading the source only.
10. The extracted trees were removed after the run. The evidence files are kept.

## Routed to T-072 (not scored here)

- `app/backend/flag_templates.py:126` (a27e3a4): title "Patient self-report" for category patient_report. The live file now reads "Reported onset" (T-072 in progress).
- `app/backend/export.py:310` and `:365`: suffix " (patient self-report)".
- `app/frontend/mock_flags.js:24`: title "Patient self-report".
- `tests/e2e/test_flags_panel.py:19-21`: asserts the "Patient self-report" text, so T-072 will need to update it.

## Findings

**F1 (major). AC1 "No code path sets source_kind patient_report" is not met in the harness.** The product path is clean, but `research/library_build.py:44` still sets `"source_kind": "patient_report"` into generated span fixtures. `evals/golden/check_golden.py:87-88` requires that value on every golden span. `evals/golden/sample.expected.json:264` and `:628` carry it, and six lines in `evals/library/*.expected.json` do too (`grep -rn patient_report evals/library/*.json` gives 6). The card's own note of 02:44:53 lists these lines. D-040 says no code or model labels who is speaking, and the checker enforces that label. Nothing is invented or lost in product output, so I rate this major, not blocker.

**F2 (major). AC1 "evals pass" is not supported by the eval run.** `artifacts/review-evidence/T-071-evals-fixture-a27e3a4.txt:3` reads `ship_bar_met: False`. Line 5 reads `Blockers: 4_no_invented_facts`. Line 30 reads `entry misses: {"case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}`. The parent 59c7edb gives the same result (`T-071-evals-fixture-59c7edb-baseline.txt:3,5,30`), so T-071 did not cause it. The card's AC1 evidence cites only the hallucination catch (40/40). Case_06 is the prior-condition case, so an entry whose excerpt misses its must-contain text is a possible lost fact, and it has to be owned before the gate.

**F3 (minor, pre-existing, not T-071). Probe FN passes the selfcheck.** `artifacts/review-evidence/T-071-selfcheck-a27e3a4.out.txt:48` reads `FN adjuster compliance | No acute findings. (low only)`. Line 54 reads `probe FP 0, FN 1 of 140`, and line 55 reads `RESULT: PASS`. The same FN appears at 59c7edb. The bar counts false positives only.

**F4 (minor). Schema still admits the withdrawn value.** `app/db/schema.sql:39` reads `source_kind TEXT CHECK (source_kind IN ('record','patient_report'))`. Nothing writes the value, but the constraint still allows it.

**F5 (minor). Stale lexicon comments describe the removed chip.** `app/llm/lexicon.yaml:25-26` says code sets `source_kind = "patient_report"` from self_report entries. Lines 84-87 say the same and cite `research/lexicon_selfcheck.py:is_patient_statement()`. `grep -n "def is_patient_statement" research/lexicon_selfcheck.py` returns nothing, so the reference is dangling. AC2 posted owner notes but did not apply them.

## Scores (1 to 5)

| Criterion | Score | Why |
|---|---|---|
| Product code: chip and setters removed | 5 | flags.py:61, generator.py:80, present.py:45; no app/ branch on source_kind |
| Attribution kept in verbatim excerpts | 4 | excerpts unchanged; speaker-label title still present (T-072) |
| Tests and probe for D-040 | 4 | 33/33 probe, 35 unit tests, selfcheck PASS |
| Harness consistent with D-040 | 2 | check_golden.py:87-88, golden and library fixtures still require the label |
| AC evidence accuracy | 2 | "evals pass" with ship_bar_met False |
| Docs and comments consistent | 3 | lexicon.yaml:25-26 and :84-87 are stale |

## What is right (do not break)

- The product path is clean: the three setters now write "record", no `app/` code reads `source_kind`, and `flags.js:66` renders no speaker chip.
- The 33 T-061 r4 rows all come out as plain records through the constructor and the lexicon path, and the excerpts stay verbatim.
- No attribution is lost in the flag text: the D-022 qualifier carry is still live (`app/backend/grounding.py:185`), and the record-9 flag still says "not a physician's opinion" (`flag_templates.py:126` in a27e3a4).

## Questions for Chris

- Does D-040 cover the eval harness? `check_golden.py:87-88` and the golden expectations require `source_kind` = patient_report. I rated F1 major on the reading that D-040 covers the harness. If D-040 is product-only, F1 drops to minor.

```json
{"card": "T-071", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit a27e3a4 (T-071 chip cut; includes the flags.py change from ancestor 59c7edb), extracted with git archive to artifacts/review-evidence/T-071-tree-a27e3a4 and removed after the run; live tree checked for the same files; no app server run; sample case through unit tests, selfcheck, golden checker and the eval fixture run",
 "exercised": [
  "read personas/claims-adjuster.md, memory notes, board/cards/T-071.md, memory/ORCHESTRATOR_DECISIONS.md D-040",
  "git show a27e3a4 (full diff); git show 59c7edb -- app/backend/flags.py; git show d148e0f --stat; git status --short app/ research/ evals/ tests/unit",
  "grep -rn for patient_report, has_self_report, patient_report_spans, selfreport, source_kind across app/ research/ tests/ evals/ and repo-wide for chip helpers and setters",
  "git archive a27e3a4 into artifacts/review-evidence/T-071-tree-a27e3a4; ran artifacts/review-evidence/T-071-claims-adjuster-probe.py (33 rows, no-chip) on the archive and on the live tree: 33/33 both",
  ".venv/bin/python -m pytest tests/unit/test_flags_pass.py tests/unit/test_flags_sample.py -p no:cacheprovider -q in the archive: 35 passed; live test_flags_pass.py: 22 passed",
  ".venv/bin/python research/lexicon_selfcheck.py in the archive (T-009 probe files copied in): RESULT PASS, FN 1 of 140 (same at 59c7edb); live: RESULT PASS, FN 1 of 140",
  ".venv/bin/python evals/golden/check_golden.py in the archive: golden OK",
  ".venv/bin/python -m evals.run --backend fixture --runs 3 on a27e3a4 and on 59c7edb: ship_bar_met False on both; blocker 4_no_invented_facts (case_06 E3)",
  "title probe of 8 sentences (wife, EMS, husband, family, mother, witness, record-9 patient statement) through flags.lexicon_flags on the archive: no flag on non-patient speakers",
  "grep -n of every citation line in this review, against a27e3a4 and the live tree"
 ],
 "verdict": "changes",
 "scores": {"product_chip_removed": 5, "attribution_kept_in_excerpts": 4, "tests_and_probe_for_D-040": 4, "harness_consistent_with_D-040": 2, "ac_evidence_accuracy": 2, "docs_and_comments_consistent": 3},
 "findings": [
  {"severity": "major",
   "title": "AC1 'No code path sets source_kind patient_report' not met: harness still sets and requires the withdrawn label",
   "evidence": "research/library_build.py:44 `return {\"excerpt\": excerpt, \"source_kind\": \"patient_report\", \"attribution_any\": attribution}`; evals/golden/check_golden.py:87-88 `if sp.get(\"source_kind\") != \"patient_report\": out.append(\"source_kind must be 'patient_report' (D-022)\")`; evals/golden/sample.expected.json:264 and :628; 6 matching lines in evals/library/*.expected.json (grep -rn patient_report evals/library/*.json); card T-071 note 02:44:53 lists the same lines",
   "why_it_matters": "D-040 says no code or model labels who is speaking. The golden checker and the library builder still encode the speaker label on spans, so any regeneration or golden check re-adds it. Product output is clean, so this is not a blocker, but AC1 is literally unmet.",
   "fix": "researcher: drop source_kind from research/library_build.py span() and regenerate evals/library/*.expected.json. qa: remove the source_kind requirement at evals/golden/check_golden.py:87-88 and drop source_kind from the golden spans in evals/golden/sample.expected.json and case_01/case_06 expectations, keeping attribution_any (D-022 qualifier carry).",
   "acceptance_test": "grep -rn '\"source_kind\": \"patient_report\"\\|source_kind.*patient_report' research/library_build.py evals/ returns nothing; .venv/bin/python evals/golden/check_golden.py prints 'golden OK'; a unit test fails if any evals/**/*.json span carries source_kind patient_report"},
  {"severity": "major",
   "title": "AC1 'evals pass' is not supported: fixture eval run reports ship_bar_met False (4_no_invented_facts, case_06 E3 excerpt miss); pre-existing at 59c7edb, not a T-071 regression",
   "evidence": "artifacts/review-evidence/T-071-evals-fixture-a27e3a4.txt:3 '**ship_bar_met: False**'; :5 'Blockers: 4_no_invented_facts; backend=fixture: determinism_3run ...'; :30 'entry misses: {\"case_06_subtle_pre_existing\": [{\"entry\": \"E3\", \"why\": \"excerpt misses must_contain_excerpt\"}]}'; identical at parent: artifacts/review-evidence/T-071-evals-fixture-59c7edb-baseline.txt:3,5,30. Card AC1 evidence quotes only 'hallucination catch 1.000 (40/40)'.",
   "why_it_matters": "The card claims evals pass, and the report says the ship bar is not met on an invented-facts gate. Case_06 is the prior-condition case, and an entry whose excerpt misses its must-contain text is a possible lost fact. T-071 did not introduce it, but the card should not claim a pass it does not have.",
   "fix": "backend and qa: quote the ship_bar result in the T-071 handoff as it is; route the case_06 E3 must_contain_excerpt miss to its owning card with an owner note before the milestone gate.",
   "acceptance_test": ".venv/bin/python -m evals.run --backend fixture --runs 3 reports ship_bar_met True, or its only blockers are the R-CO-7 live-backend notes and the E3 miss is recorded on a named board card"},
  {"severity": "minor",
   "title": "Pre-existing probe false negative passes the lexicon selfcheck (not T-071)",
   "evidence": "artifacts/review-evidence/T-071-selfcheck-a27e3a4.out.txt:48 'FN adjuster compliance | No acute findings. (low only)'; :54 'probe FP 0, FN 1 of 140'; :55 'RESULT: PASS'. Same at 59c7edb.",
   "why_it_matters": "The selfcheck reports PASS with a known adjuster-probe miss, because its bar counts false positives only.",
   "fix": "researcher: fix the lexicon row or record the miss as residual in SCOPE_CUTS.md, and give the selfcheck a false-negative bar.",
   "acceptance_test": ".venv/bin/python research/lexicon_selfcheck.py shows FN 0 of 140, or the residual is listed in SCOPE_CUTS.md and the selfcheck fails on any new FN"},
  {"severity": "minor",
   "title": "DB constraint still admits source_kind patient_report",
   "evidence": "app/db/schema.sql:39 `category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),`",
   "why_it_matters": "Nothing writes the value now, but the schema still permits the speaker label that D-040 cut.",
   "fix": "db: drop the value through a migration, or record the residual in SCOPE_CUTS.md.",
   "acceptance_test": "grep -n patient_report app/db/schema.sql returns nothing, or SCOPE_CUTS.md lists the residual"},
  {"severity": "minor",
   "title": "Stale lexicon comments describe the removed chip and cite a function that does not exist",
   "evidence": "app/llm/lexicon.yaml:25-26 'code sets source_kind = \"patient_report\" from it (ADR-013)'; app/llm/lexicon.yaml:84-87 'Before the code sets source_kind = patient_report ... Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().'; grep -n 'def is_patient_statement' research/lexicon_selfcheck.py returns nothing.",
   "why_it_matters": "The comments tell the next worker that a chip path exists. AC2 posted owner notes but did not apply them.",
   "fix": "researcher: rewrite the comments to say D-040 sets no source_kind and self_report entries feed only the D-022 qualifier carry.",
   "acceptance_test": "grep -n 'is_patient_statement\\|sets source_kind = .patient_report' app/llm/lexicon.yaml returns nothing"}
 ],
 "whats_right": [
  "Product path is clean: flags.py:61, generator.py:80 and present.py:45 set source_kind 'record'; no app/ code reads source_kind; flags.js:66 renders RV.chips(f) only.",
  "All 33 T-061 r4 rows come out as plain records through the constructor and the lexicon path (artifacts/review-evidence/T-071-claims-adjuster-probe-a27e3a4.out.txt SUMMARY 33/33), and the excerpts stay verbatim.",
  "No attribution is lost: the D-022 qualifier carry is live at app/backend/grounding.py:185, and the record-9 flag still reads 'not a physician's opinion' (flag_templates.py:126 at a27e3a4)."
 ],
 "questions_for_chris": [
  "Does D-040 cover the eval harness? check_golden.py:87-88 and the golden expectations still require source_kind patient_report. F1 is rated major on the reading that it does; if D-040 is product-only, F1 drops to minor."
 ]}
```
