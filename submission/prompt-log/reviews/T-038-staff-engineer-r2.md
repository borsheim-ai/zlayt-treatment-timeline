# T-038 round 2 review - staff-engineer-reviewer

Verdict: **fail** (one blocker, found while checking round 1). All four round-1 majors are resolved. The blocker is new: the grounding check reads a record key that the eval pipeline does not emit, so bar 1 cannot pass on any run through `evals.run`. Fail-closed, so no false pass, but the ship-bar gate is unusable as built.

Scope: HEAD was `5542dfd` at review time. `evals/run.py` last changed in `e771ed3` (T-051). I read the full `evals/run.py`, `tests/unit/test_eval_runner.py`, and `tests/unit/test_eval_spec_check.py`. Nothing else in the repo changed the eval path after `e771ed3`.

## Round-1 majors

| # | Round-1 major | Status | Evidence |
|---|---|---|---|
| 1 | ship_bar_met true on 2 runs; `--runs 1` crash | Resolved | `evals/run.py:463-464` require `runs == 3` in bar 4, `:468` adds a blocker for any other count. `--runs 1` and `--runs 2` both give `ship_bar_met=False` with no traceback (repro below). |
| 2 | `--check-spec` leaves stale `ship_bar_met` | Resolved | `evals/run.py:615-616` recomputes via `evaluate_report` on full reports. Repro: `rc 1`, `ship_bar_met False`, blocker `spec_matches_golden is false`. |
| 3 | Broad `except` blocks | Resolved | `grep -n "except Exception" evals/*.py` printed nothing (rc=1). `judge_item` (`run.py:312`) no longer swallows; a raising `check_summary` propagates (repro below). |
| 4 | Bar tests weak, 5-6 undetected mutations | Resolved for the listed six | Six scratch mutations, all killed by a named test. One new gap, see minor M9. |

The round-1 body listed six missed mutations and the brief said five. I ran all six.

## Commands run (quoted)

1. `.venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2`
   ```
   ......................................                                   [100%]
   38 passed, 725 deselected in 1.92s
   ```
   (A first run earlier in the session gave `37 passed`. The T-051 test landed in between.)

2. `.venv/bin/python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$?`
   ```
   rc=2
   ```
   Visible output: `ship_bar_met=False backend=fixture report=.../evals/reports/20261102T020519Z.md`, blockers `1_grounding`, `3_flags`, `4_no_invented_facts`, `backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)`. Normal exit, no traceback.

3. `grep -n "except Exception" evals/*.py`
   ```
   (no output)  grep_rc=1
   ```
   All `except` clauses in `evals/`: `evals/run.py:577 except ImportError:` and `evals/run.py:623 except CuratedFixtures as e:`.

## Other checks and repros

- Runs gate, in-process with the fake `Perfect` pipeline: `runs=1` and `runs=2` both give `ship_bar_met False`, `determinism_3run status not_measured`, blocker `determinism_3run: runs=N; exactly 3 live runs are required`. No `ZeroDivisionError`.
- Stale bar, in-process with `check_spec` forced false on a full run-3 report written to a scratch dir: `main(['--check-spec', ...])` returned `1`, `latest.json` has `ship_bar_met False`, `spec_matches_golden False`, last blocker `spec_matches_golden is false`.
- Raising code rung: `hallucination_metrics(items, controls, judge, check_summary=raising)` raises `RuntimeError: code rung broke`.
- Curated-set guard (T-051): `LLM_FIXTURE_DIR=<repo>/tests/fixtures/llm/curated python -m evals.run --out <tmp>` prints the refusal and exits `2`, no report.
- Scratch-copy mutations (copy of HEAD `evals/`, `tests/`, `app/`, `spec/`, `memory/`, `docs/`; `.env` not copied). Each mutation was applied to a copy of `run.py` and the eval suite re-run:

| Id | Mutation | Result |
|---|---|---|
| M0 | none (control) | 38 passed |
| M1 | drop `controls_unsupported` term from bar 4 | 1 failed: `test_controls_judged_unsupported_fail_bar_4_alone` |
| M2 | drop `case_07_total_420` term from bar 4 | 2 failed: `test_each_missed_bar...[4_no_invented_facts-...]`, `test_case_07_not_run_fails_bar_4` |
| M3 | case_07 `not_run` returns value True | 1 failed: `test_case_07_not_run_fails_bar_4` |
| M4 | `1_grounding` forced True | 1 failed: `test_each_missed_bar...[1_grounding-...]` |
| M5 | record-warning check disabled | 1 failed: `test_missing_record_warning_counts_as_a_must_not_hit` |
| M6 | SUMMARY_DROPS_QUALIFIER check disabled | 1 failed: `test_summary_that_drops_a_qualifier_is_an_entry_miss` |
| M7 | check-spec recompute removed | 1 failed: `test_check_spec_recomputes_the_bar_in_a_full_report` |
| M8 | broad `except Exception` reintroduced in `judge_item` | 1 failed: `test_raising_code_check_fails_loudly` |
| M9 | determinism `runs == 3` term removed from bar 4 | 38 passed (survives; see minor M9) |

- Grounding key mismatch (blocker, reproduced): the harness reads `source_label` from each record (`evals/run.py:278`). `run_case` returns the ingest shape. Verbatim keys of `run_case(sample,'fixture')['records'][0]`: `['char_end', 'char_start', 'date_candidates', 'date_iso', 'date_raw', 'date_status', 'duplicate_of', 'encounter', 'excerpt', 'id', 'injection_hits', 'injection_tag', 'kind', 'n', 'seq', 'source', 'text', 'unsplit']`. No `source_label`. For the 9 sample entries, `provider == record['source']` holds in 9 of 9. Across all golden cases `grounding()` reports 56 failures, all `entry eN provider`. `grounding_rate` = 183/239 = 0.766, so bar 1 is false on fixture. The same key mismatch is backend-independent, so bar 1 is false on a live run too.
- Fixture run logs 41 `llm call failed ... step=j1 attempt=1 prompt_hash=...` warnings per run (`app/llm/audited.py:87`). Visible, not swallowed. Out of this card's scope; see the question below.

## Findings

Blocker: the grounding check compares against a key the eval pipeline does not produce, so bar 1 cannot pass through `evals.run`. Fail-closed (no false pass), but the ship-bar gate is unusable until fixed. Per the calibration (makes the must-have unusable), this is a blocker.

Minor M9: bar 4 requires `determinism_3run.runs == 3` but no test asserts the bar on that term alone. A tampered report with `determinism_3run {value 1.0, runs 2}` gives `bars["4_no_invented_facts"]=False` today, but if the term is removed, the bar shows True while the blockers still say "not measured". Add the tampered-report test.

Minor: the CLI exits `2` both for a refused curated run (`evals/run.py:625`) and for ship-bar-not-met (`run.py:632`). A caller cannot tell them apart.

Nit: `evals/run.py:577` `except ImportError` fallback. `app/pipeline.py` is a 6-line re-export of `app.backend.pipeline` (verified `app/pipeline.py:2`), so both branches load the same module. The try/except adds nothing.

Side effect, for transparency: the brief's commands and my extra `--runs 2` run wrote timestamped reports and overwrote `evals/reports/latest.json` in the untracked `evals/reports/` directory.

```json
{"card": "T-038", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 5542dfd at review time; evals/run.py (last changed e771ed3, T-051); tests/unit/test_eval_runner.py; tests/unit/test_eval_spec_check.py; app/backend/pipeline.py case_view (read only); fixture backend, golden sample and all golden cases via run_case; no app URL exercised (eval CLI only)",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-038-staff-engineer.md, memory index",
  "read evals/run.py in full (615 lines at HEAD), tests/unit/test_eval_runner.py in full, tests/unit/test_eval_spec_check.py in full",
  "pytest tests/unit -q -k eval | tail -2 -> '38 passed, 725 deselected in 1.92s'",
  "python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$? -> rc=2 (fixture; blockers 1_grounding, 3_flags, 4_no_invented_facts, backend=fixture)",
  "grep -n 'except Exception' evals/*.py -> no output, rc=1; all except clauses in evals/ listed (run.py:577, run.py:623)",
  "in-process runs=1 and runs=2 with fake Perfect pipeline: ship_bar_met False, no ZeroDivisionError",
  "in-process --check-spec with check_spec forced false over a full run-3 report in a scratch dir: rc 1, ship_bar_met False, blocker spec_matches_golden is false",
  "in-process hallucination_metrics with raising check_summary: RuntimeError propagates",
  "LLM_FIXTURE_DIR=curated python -m evals.run --out <tmp>: rc 2 with refusal message, no report",
  "git log / git show e771ed3 (T-051 diff) read in full",
  "run_case(sample,'fixture') record keys printed; provider == record['source'] 9/9; grounding() failures 56, all provider; grounding_rate 183/239",
  "scratch copy of HEAD evals/, tests/, app/, spec/, memory/, docs/ (no .env); 10 mutations M0-M9 applied to a copy of run.py, eval suite re-run each time, copy restored and diffed identical",
  "grep 'llm call failed' on fixture runs: 41 warnings in one run (app/llm/audited.py:87)"],
 "verdict": "fail",
 "scores": {"determinism_and_code_vs_llm_split": 4, "failure_visibility": 4, "test_strength": 3, "spec_conformance": 2, "ship_bar_integrity": 3},
 "findings": [
  {"severity": "blocker", "title": "Grounding provider check reads a key run_case never emits; bar 1 cannot pass through evals.run",
   "evidence": "evals/run.py:278 chk(... norm(e.get('provider')) == norm(first.get('source_label'))); app/backend/pipeline.py:331 case_view returns out['records'] unchanged; run_case records keys (verbatim) ['char_end','char_start','date_candidates','date_iso','date_raw','date_status','duplicate_of','encounter','excerpt','id','injection_hits','injection_tag','kind','n','seq','source','text','unsplit'] (no source_label); provider == record['source'] in 9/9 sample entries; grounding() failures = 56, all 'entry eN provider' across golden cases; grounding_rate 183/239 = 0.766 so bar 1 fails. Contract memory/contracts/api.md:54 and app/backend/present.py:132 use source_label.",
   "why_it_matters": "The eval gate and the HTTP API emit different record shapes. Every correct entry is reported as a grounding failure, so bar 1 is false on fixture and on any live run through run_case. Fail-closed, so no false pass, but the ship-bar must-have cannot be met and the reported 0.766 misstates the pipeline. Test doubles hid it: test_eval_runner.py:45 Perfect.run_case builds records with source_label, so the fake never exercises the real key set.",
   "fix": "Make case_view emit the documented record shape (source_label, seq, id, date_iso, date_status) and have grounding() read that documented key; or have one shared record mapper used by both the HTTP view and run_case. Replace the Perfect record shape with the one run_case actually produces.",
   "acceptance_test": "grounding(SAMPLE, P.run_case(SAMPLE,'fixture'))['failures'] contains no 'provider' entries; case_view records include source_label equal to the record header; python -m evals.run --runs 1 report has metrics.grounding_rate.failures == []."},
  {"severity": "minor", "title": "Bar 4 determinism runs==3 term has no bar-level test (M9 survives)",
   "evidence": "evals/run.py:464 `and m['determinism_3run'].get('runs') == 3`; scratch mutation removing that term: 38 passed. Tampered report {determinism_3run: value 1.0, runs 2} gives blockers naming determinism but bars['4_no_invented_facts'] True when the term is removed.",
   "why_it_matters": "bars and blockers can disagree in latest.json, which T-045 reads. Current code is correct, but nothing proves the bar itself carries the run-count rule.",
   "fix": "Add a test that evaluate_report on a tampered runs-2 value-1.0 report gives bars['4_no_invented_facts'] False and ship_bar_met False.",
   "acceptance_test": "M9 mutation makes the new test fail."},
  {"severity": "minor", "title": "CLI exit code 2 used for both refused curated run and bar-not-met",
   "evidence": "evals/run.py:625 `return 2` (curated refusal); evals/run.py:632 `return 0 if report['ship_bar_met'] else 2`. Both return 2.",
   "why_it_matters": "A CI caller cannot tell a refused run (configuration error) from a measured bar miss.",
   "fix": "Return a distinct code for the curated refusal (for example 3) and document both codes in the module docstring.",
   "acceptance_test": "test asserts refused-curated exit code differs from the bar-miss exit code."},
  {"severity": "nit", "title": "try/except ImportError fallback in load_pipeline adds nothing",
   "evidence": "evals/run.py:575-578 try: from app import pipeline / except ImportError: from app.backend import pipeline; app/pipeline.py:2 is `from app.backend.pipeline import *`.",
   "why_it_matters": "Both branches load the same implementation, so the fallback is dead weight and can mask a broken import path in a later edit.",
   "fix": "Import app.backend.pipeline directly, or keep one import with no except.",
   "acceptance_test": "none required beyond the existing eval suite."}
 ],
 "whats_right": [
  "All four round-1 majors are resolved in code and tests: runs gate at evals/run.py:463-468, check-spec recompute at run.py:615, judge_item propagates at run.py:312, zero 'except Exception' in evals/.",
  "Each of the six round-1 missed mutations (M1-M6) is now killed by a named test; M7 and M8 are killed too.",
  "The curated-set guard (T-051) refuses full runs with exit 2 and writes no report, verified by running it."],
 "questions_for_chris": [
  "The fixture run logs 41 FixtureMiss warnings for step j1 (app/llm/audited.py:87). Is the recorded fixture set meant to cover j1 for the golden cases? If not, fixture-backed hallucination numbers are not representative."]}
```
