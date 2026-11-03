# T-038 review - staff-engineer-reviewer (commit 40c882d, code-only parts)

Verdict: changes. No blockers. Four majors. The full run waits for T-037, so I judged the code-only parts.

Commands run:

- `.venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -3` gave `24 passed, 673 deselected`.
- `.venv/bin/python -m evals.run --check-spec; echo rc=$?` printed `{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}` and `rc=0`.
- A one-character change in a copy of REQUIREMENTS section 6 gave `spec_matches_golden: False`.
- `--check-fresh` against the current `latest.json` exits 1. That file holds only the spec fields because no full run has happened yet, so every prompt and the lexicon are listed as changed.
- `python -m evals.run` on the repo gets `AttributeError: module 'app.pipeline' has no attribute 'run_case'`. This is expected and visible, because T-037 is not built.

What the report carries, checked in code and in the `Perfect` fake-pipeline report:

| Item | Where |
|---|---|
| `ship_bar_met`, `bars`, `blockers` | `build_report` |
| `metrics` with `r_ids` | `RIDS`, `aggregate` |
| `backend`, `models`, `hashes` (sha256 of every prompt and `lexicon.yaml`) | `build_report` |
| `assertions.gap_28_not_flagged` and `gap_73_flagged` | `assertions` |
| `spec_matches_golden` | `check_spec` |
| `lexicon_recall_must_flags` with `gated: False`, outside the `ship_bar` function | `lexicon_recall` |

Other checks:

- On the fixture backend, `determinism_3run` and `unsupported_count_3run` are `{"value": None, "status": "not_measured"}`. `ship_bar_met` is false, with the blocker "need a live backend".
- `hallucination_catch_rate` is `caught / len(items)` over all 40 lines. All 50 lines of `hallucinations*.jsonl` parse with no fallback.
- `--check-fresh` exits 1 when a hash differs and exits 0 on a freshly written report.

Scratch-copy mutations (11 on `evals/run.py`, tested against the three `test_eval_*` files, which pass `24 passed` on the unmutated copy):

- Caught: hallucination denominator replaced with `caught`; `check_fresh` always 0; fixture blocker dropped; determinism and unsupported terms dropped from bar 4; gap-28 assertion always true; lexicon `gated: True`; must_not hits dropped from the bar; `grounding()` entry-excerpt check disabled; must_not regex disabled.
- Missed, with all 24 tests still green: controls-unsupported check dropped from the bar; case_07 term dropped from the bar; case_07 `not_run` counted as pass; `1_grounding` forced true; `score_record_warnings` check disabled; the `SUMMARY_DROPS_QUALIFIER` check in `entry_found` disabled.

Findings:

- **Major: the ship bar can be met on fewer than 3 runs.** `ship_bar` checks only `determinism_3run.value == 1.0`, never `runs >= 3`. With the fake pipeline, `build_report(..., runs=2)` gives `ship_bar_met True` with `determinism_3run` 1.0 and `runs` 2. `--runs 1` crashes with `ZeroDivisionError`.
- **Major: `--check-spec` leaves a stale `ship_bar_met`.** I wrote a full report with `ship_bar_met` true, made `check_spec` return false, and ran `--check-spec` (rc 1). `latest.json` then read `ship_bar_met = True` and `spec_matches_golden = False` with `blockers = []`. `main` does `data.update(s)` and never recomputes the bar. `evaluate_report` would catch it, but anyone reading the field would not.
- **Major: swallowed exceptions in the eval gate.** `run.py:316` has `except Exception: code = []`, and `run.py:490` has `except Exception: check = None`. A crash in `check_summary` silently turns the code-rung catch off. I reproduced it: with a `check_summary` that raises, `hallucination_metrics` returned 40/40 with no error surfaced. Only the lexicon `except` (`run.py:503`) records the error type.
- **Major: bar tests are weak.** `test_each_missed_bar_flips_ship_bar_met_false` asserts only `ship_bar_met is False and blockers`, not which bar failed, so another bar can satisfy it. The mutations listed above go unnoticed.
- AC8 is orchestrator-owned and not done, as the card says. AC1, AC3, AC4 and AC6 are open until a real run after T-037. I did not count either as a finding.

```json
{"card": "T-038", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 40c882d: evals/run.py, evals/matching.py, tests/unit/test_eval_{runner,matching,spec_check}.py; code-only parts (full run awaits T-037); fake-pipeline report",
 "exercised": ["board show T-038", "pytest tests/unit -k eval: 24 passed", "python -m evals.run --check-spec: true rc=0", "--check-spec on a 1-char-mutated copy of REQUIREMENTS: false", "--check-fresh on current latest.json: rc 1 (no hashes yet); on a fresh full report: rc 0", "python -m evals.run on repo: AttributeError run_case (T-037 absent, visible)", "read evals/run.py in full, test_eval_runner.py in full", "build_report with Perfect fake: runs=3 and runs=2 both ship_bar_met True; runs=1 ZeroDivisionError", "--check-spec over a full report with spec forced false: stale ship_bar_met True", "hallucination_metrics with raising check_summary: 40/40, no error", "parse_record_text on all 50 jsonl lines: no fallback", "11 scratch-copy mutations of evals/run.py: 5 undetected", "grep except in evals/"],
 "verdict": "changes",
 "scores": {"determinism_and_code_vs_llm_split": 4, "failure_visibility": 2, "test_strength": 3, "spec_conformance": 4, "ship_bar_integrity": 3},
 "findings": [
  {"severity": "major", "title": "ship_bar_met can be true on fewer than 3 runs; --runs 1 crashes",
   "evidence": "evals/run.py:462 `m[\"determinism_3run\"].get(\"value\") == 1.0` with no runs check; evals/run.py:353 `sum(...)/(runs - 1)`; repro: R.build_report(Perfect('claude-cli'),'claude-cli',2) -> ship_bar_met True, determinism_3run runs=2; runs=1 -> ZeroDivisionError.",
   "why_it_matters": "R-CO-7 and AC4 define a 3-run measurement. A 2-run pass is reported as determinism_3run and can satisfy the ship bar, so the label overstates the evidence.",
   "fix": "Require runs >= 3 in ship_bar (value measured and runs >= 3), and reject --runs < 3 in argparse (or clamp with a visible message).",
   "acceptance_test": "test: build_report(..., runs=2) has ship_bar_met False with a blocker naming the run count; --runs 1 exits with a usage error, not a traceback."},
  {"severity": "major", "title": "--check-spec writes spec_matches_golden but leaves a stale ship_bar_met in latest.json",
   "evidence": "evals/run.py:592-596 `data.update(s)` only. Repro: write full report (ship_bar_met true); force check_spec false; main(['--check-spec','--out',d]) rc 1; latest.json -> ship_bar_met True, spec_matches_golden False, blockers [].",
   "why_it_matters": "latest.json becomes self-contradictory and T-045's AC reads ship_bar_met directly; a false spec check would not block the milestone.",
   "fix": "After merging the spec fields, recompute with evaluate_report (or null/blocker the stale fields) when the file is a full report.",
   "acceptance_test": "test: full report with ship_bar_met true + --check-spec failing -> latest.json ship_bar_met false with blocker 'spec_matches_golden is false'."},
  {"severity": "major", "title": "Swallowed exceptions in the eval gate hide a broken code rung",
   "evidence": "evals/run.py:316 `except Exception: code = []`; evals/run.py:490 `except Exception: check = None`. Repro: hallucination_metrics(items, controls, judge=lambda *a: 'unsupported', check_summary=raising) -> caught 40/40, no error recorded.",
   "why_it_matters": "Checklist 12 and honest failure. If grounding.check_summary breaks, the report can still show a passing catch rate from the judge alone, and nobody learns the code rung was off. The report cannot be audited for which rung caught what.",
   "fix": "Let the error propagate, or record `code_rung_error` per item in the metric and count it as a blocker. Import grounding without a fallback.",
   "acceptance_test": "test: a raising check_summary makes build_report/hallucination_metrics raise or set a blocker; the report records how many were code-caught versus judge-caught."},
  {"severity": "major", "title": "Bar tests assert only 'false', so several bars and scorers are unproven",
   "evidence": "Scratch mutations with all 24 tests still green: drop `not m[\"hallucination_catch_rate\"][\"controls_unsupported\"]` from bar 4; drop `m[\"case_07_total_420\"][\"value\"] is True` from bar 4; case_07 `not_run` -> value True (evals/run.py:445); `\"1_grounding\": True`; score_record_warnings `if not (flagged and review)` -> False; entry_found SUMMARY_DROPS_QUALIFIER check disabled. test_each_missed_bar_flips_ship_bar_met_false asserts `ship_bar_met is False and r[\"blockers\"]` only.",
   "why_it_matters": "AC3 requires 'no control returns unsupported', and AC5 requires false when any bar is missed; the controls clause and the individual bar flags can be removed without any test noticing. A false-pass on the ship bar is the failure this card exists to prevent.",
   "fix": "Assert the named bar in r['bars'] per case (e.g. bars['1_grounding'] is False); add tests for: controls judged unsupported alone fails bar 4; case_07 not_run fails; record-warning miss counts in golden_must_not_hits; summary dropping a qualifier is a miss in entry_recall.",
   "acceptance_test": "Re-run the six listed scratch mutations: each makes at least one test fail."}
 ],
 "whats_right": ["On fixture, determinism_3run and unsupported_count_3run are null/not_measured and ship_bar_met is false (test + code), and a tampered report is recomputed by evaluate_report.", "hallucination_catch_rate is a rate over every line (40 of 40 parse) with controls scored separately, and lexicon_recall_must_flags is reported with gated:false outside ship_bar (D-026).", "check_fresh hashes every prompt and the lexicon, exits 1 on any difference or missing file, and the spec check is byte-exact (a one-char change flips it)."],
 "questions_for_chris": []}
```
