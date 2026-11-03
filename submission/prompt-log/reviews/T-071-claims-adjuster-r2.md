# T-071 round 2 review: claims-adjuster (Gary Pruitt persona), commit 9d6756e

Scope: commit 9d6756e (qa, round 2, "drop patient_report source_kind from golden checker, goldens and library builder"). I extracted it with `git archive` into `artifacts/review-evidence/T-071-tree-9d6756e`, ran the checks there, and removed the extracted tree afterwards. The live tree is dirty, so the scored results come from the commit. The brief set three checks (major 1 closure, the two deterministic checks, the 33-row probe). Per the brief, major 2 (ship_bar_met) is not scored here. It is tracked in T-070 and stays on record in `reviews/T-071-claims-adjuster.md`.

Model: running as `claude-haiku-5-5`, which is the id the brief specifies. The persona file expects `claude-opus-5-5`; the record uses the actual model.

**Verdict: pass, for the round-2 scope.** No blockers. Major 1 is closed. Three minor items remain open (findings below). The verdict covers only the scope set in the brief. It does not close T-071's r1 major 2 (`ship_bar_met False`), which still needs T-070 before the gate.

## Major 1: closed

- **Checker rejects source_kind on spans.** `evals/golden/check_golden.py:87-88`: `if "source_kind" in sp:` / `out.append("source_kind not allowed on spans (D-040: no speaker label)")`. Self-test at `check_golden.py:159` expects a mislabelled span to be rejected.
- **Mutation test.** In the extracted archive I added `"source_kind": "patient_report"` to the first `self_report_spans` entry of `evals/golden/sample.expected.json`. `check_golden.py` exited 1 with `GOLDEN CHECK FAILED` / ` - sample: E9: self_report span: source_kind not allowed on spans (D-040: no speaker label)`. I restored the file and confirmed it is byte-identical to `git show 9d6756e:evals/golden/sample.expected.json`.
- **No golden or library expected.json carries the label.** `grep -rn patient_report evals/library/*.json` returns nothing. In `evals/golden/*.json`, the only hit is `sample.expected.json:626`, `"subtype": "patient_reported_onset"`. That is a flag subtype, not `source_kind`. No `source_kind` key remains anywhere under `evals/`.
- **Builder no longer sets it.** `research/library_build.py:43-44`: `def span(excerpt, attribution):` / `return {"excerpt": excerpt, "attribution_any": attribution}`.
- **Diff is key-only.** `git show 9d6756e` removes only `source_kind` lines (and one trailing comma at `sample.expected.json:624-626`). Excerpts, `attribution_any` and the `patient_reported_onset` subtype are unchanged. No content was lost.
- Note, not a finding: qa's AC1 evidence says `grep patient_report in evals/**/*.json = 0`. That is true for the `source_kind` value. A bare substring grep hits the subtype name at `sample.expected.json:626`.

## Other checks

- `check_golden.py` at 9d6756e: `golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered`, exit 0. Live tree: same, exit 0.
- `tests/fixtures/make_curated.py --check` at 9d6756e: `entries: 9 non-verified: []` / `letter equal: True | notes equal: True`, exit 0. The live `make_curated.py` has uncommitted edits (`git diff 9d6756e` shows +30/-3). Its live `--check` also prints `narrative: 9 sentences, removed: []` and exits 0. The commit result is what is scored.
- 33-row probe at 9d6756e (`artifacts/review-evidence/T-071-claims-adjuster-probe.py` against the archive): `grounding.has_self_report present = False`, `grounding.patient_report_spans present = False`, `SUMMARY rows=33 no_chip_ok=33 miss=0`. Every row has `ctor_source_kind=record`.
- Evidence: `artifacts/review-evidence/T-071-r2-checks-9d6756e.out.txt`.

## Open findings (round 2, minor, not blockers)

1. **Stale lexicon comments (carry-over of r1 F5, not applied).** `app/llm/lexicon.yaml:25-26` still says "code sets source_kind = "patient_report" from it (ADR-013)". Line 84 says "Before the code sets source_kind = patient_report". Both cite `research/lexicon_selfcheck.py:is_patient_statement()`, and `grep -n "def is_patient_statement" research/lexicon_selfcheck.py` returns nothing (exit 1). The comments describe the chip that D-040 cut.
2. **Golden README teaches the withdrawn span form (new in r2).** `evals/golden/README.md:40` still shows `"self_report_spans": [{"excerpt": "verbatim subjective sentence", "source_kind": "patient_report", ...`. This is the form `check_golden.py:87-88` now rejects. No golden file carries it, so it is documentation only.
3. **DB residual is not recorded (carry-over of r1 F4).** `app/db/schema.sql:39`: `category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),`. The triage note says the value is "documented" as a legacy value. The only place I found that text is the T-071 card note. `memory/SCOPE_CUTS.md` has no row for it (row 21 covers the chip only).

Not re-scored in this round (outside the brief): r1 F3 (selfcheck false negative, pre-existing), the T-072 items (flag title "Patient self-report", export suffix), and the full unit, e2e and eval runs.

## What is right (do not break)

- The checker enforces the cut itself. The span rule has a self-test and rejects an injected label (mutation above).
- The round-2 diff removes only the speaker-label keys. Excerpts, attribution and the subtype are intact.
- The 33-row probe still shows no chip at the commit (33/33).

## Questions for Chris

None for this round.

```json
{"card": "T-071", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 9d6756e (T-071 round 2, qa), extracted with git archive to artifacts/review-evidence/T-071-tree-9d6756e and removed after the run; live tree checked read-only for make_curated and check_golden. Round-2 brief scope: major 1 closure, check_golden, make_curated --check, 33-row probe. Major 2 (ship_bar_met) not scored, per brief (T-070).",
 "exercised": [
  "read personas/claims-adjuster.md, memory notes (project_t071_chip_cut_harness_sweep, review-commit-not-worktree, reviews-write-once), reviews/T-071-claims-adjuster.md, board show T-071 (triage and round-2 notes), git show 9d6756e (full diff)",
  "git archive 9d6756e into artifacts/review-evidence/T-071-tree-9d6756e",
  "grep -rn patient_report and source_kind across evals/, research/, tests/, app/ at 9d6756e; grep -n in evals/library/*.json (0 hits)",
  "cd extracted tree && .venv/bin/python evals/golden/check_golden.py: golden OK, exit 0",
  "cd extracted tree && .venv/bin/python tests/fixtures/make_curated.py --check: entries 9 non-verified [], letter equal True, notes equal True, exit 0",
  ".venv/bin/python artifacts/review-evidence/T-071-claims-adjuster-probe.py <extracted tree>: SUMMARY rows=33 no_chip_ok=33 miss=0",
  "mutation: injected source_kind patient_report into sample.expected.json first self_report span in the extracted tree; check_golden exit 1 with source_kind not allowed on spans; restored and cmp-identical to git show 9d6756e",
  "live tree read-only: check_golden exit 0; make_curated --check exit 0 (narrative 9 sentences, removed []); git diff 9d6756e -- tests/fixtures/make_curated.py (uncommitted edits noted)",
  "grep -n on research/library_build.py (span at 43-44), app/llm/lexicon.yaml (25-26, 84), research/lexicon_selfcheck.py (is_patient_statement: no def), app/db/schema.sql:39, evals/golden/README.md:40, memory/SCOPE_CUTS.md (no CHECK residual row)",
  "evidence file artifacts/review-evidence/T-071-r2-checks-9d6756e.out.txt"
 ],
 "verdict": "pass",
 "scores": {"major1_source_kind_closed": 5, "checker_rejects_span_source_kind": 5, "goldens_and_library_free_of_label": 5, "probe_33_no_chip": 5, "harness_consistent_with_D-040": 4, "docs_and_comments_consistent": 2},
 "findings": [
  {"severity": "minor", "title": "Stale lexicon comments still describe the removed chip (carry-over r1 F5, not applied)",
   "evidence": "app/llm/lexicon.yaml:25-26 '#   source_kind = \"patient_report\" from it (ADR-013).'; app/llm/lexicon.yaml:84 '# T-061: ... Before the code sets source_kind = patient_report'; both cite research/lexicon_selfcheck.py:is_patient_statement(), and grep -n 'def is_patient_statement' research/lexicon_selfcheck.py exits 1 at 9d6756e",
   "why_it_matters": "The comments tell the next worker that a chip path exists and point to a function that is not there. D-040 says no code sets source_kind.",
   "fix": "researcher: rewrite the comments to say D-040 sets no source_kind and self_report entries feed only the D-022 qualifier carry; drop the dangling function reference.",
   "acceptance_test": "grep -n 'is_patient_statement\\|sets source_kind = .patient_report\\|code sets source_kind' app/llm/lexicon.yaml returns nothing"},
  {"severity": "minor", "title": "Golden README template still shows the withdrawn span label (new in r2)",
   "evidence": "evals/golden/README.md:40 '\"self_report_spans\": [{\"excerpt\": \"verbatim subjective sentence\", \"source_kind\": \"patient_report\",'; check_golden.py:87-88 rejects exactly this key",
   "why_it_matters": "The README is the spec a golden author copies from. It teaches the form the checker now rejects. No golden carries it, so no product output or score is affected.",
   "fix": "qa: remove the source_kind key from the README example span (keep attribution_any).",
   "acceptance_test": "grep -n 'source_kind' evals/golden/README.md returns nothing, and check_golden.py still prints golden OK"},
  {"severity": "minor", "title": "DB CHECK still admits source_kind patient_report; residual not recorded in SCOPE_CUTS",
   "evidence": "app/db/schema.sql:39 \"category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),\"; triage note 'documented' appears only in board/cards/T-071.md; memory/SCOPE_CUTS.md has no entry for the CHECK (row 21 covers the chip only)",
   "why_it_matters": "Nothing writes the value, so no output is affected. But the constraint still permits the speaker label that D-040 cut, and the claim that it is documented is not in the record.",
   "fix": "db or orchestrator: add a SCOPE_CUTS.md row for the legacy CHECK value, or drop the value through a migration.",
   "acceptance_test": "grep -n 'patient_report' memory/SCOPE_CUTS.md shows a row for the schema.sql:39 residual, or grep -n patient_report app/db/schema.sql returns nothing"}
 ],
 "whats_right": [
  "The checker enforces the D-040 cut itself: check_golden.py:87-88 rejects any span source_kind, and a mutation test confirmed the rejection.",
  "The round-2 diff removes only the speaker-label keys; excerpts, attribution_any and the patient_reported_onset subtype are intact.",
  "The 33-row probe still shows no chip at 9d6756e (SUMMARY rows=33 no_chip_ok=33 miss=0)."
 ],
 "questions_for_chris": []}
```
