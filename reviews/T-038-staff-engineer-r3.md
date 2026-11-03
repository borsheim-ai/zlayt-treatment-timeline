# T-038 round 3 review - staff-engineer-reviewer

Verdict: **changes** (no blocker; one major). The round-2 blocker is fixed: grounding now reads the record key `run_case` emits, and a real-`run_case` test with a negative control is in place. Bar 1 passes on the pinned commit. Bars 3 and 4 fail, which is correct: the causation precision and must-not-flag numbers are product metrics and the runner reports them honestly. Remaining work is the record-shape drift between the eval's input and the documented API contract.

Pinned to commit `7364096`. HEAD has moved to `7a450a1` and the working tree is dirty with another agent's uncommitted `evals/run.py` work (`judge_unavailable_in`, not in 7364096). I did not review that work. The brief's pytest and jq commands ran against the working tree and matched the pinned results (noted below). Verdict and evidence are for 7364096.

## Round-2 findings

| # | Round-2 finding | Status | Evidence |
|---|---|---|---|
| B1 | Blocker: grounding reads `source_label`, which `run_case` never emits | Resolved | `evals/run.py:278` now `norm(first["source"])`; `grounding_rate` checked 242, failures 0, value 1.0 (committed `latest.json`). Mutation M10 (revert to `source_label`) fails 3 tests. |
| m9 | Minor: bar 4 `determinism_3run.runs == 3` term has no bar-level test | Resolved | `tests/unit/test_eval_runner.py:280-285` `test_tampered_two_run_determinism_fails_bar_4_alone`. Mutation M9 (term removed) now fails it. |
| m-exit | Minor: exit 2 used for both refused curated run and unmet bar | Resolved | `evals/run.py:629` `return 0 if report['ship_bar_met'] else 1`. Pinned CLI rc=1 for unmet bar. Curated refusal still exits 2 (`test_curated_fixture_set_is_refused_with_exit_2` passes). |
| nit | `try/except ImportError` in `load_pipeline` adds nothing | Resolved | Commit diff: `load_pipeline` is now a single `from app import pipeline`. |

## Commands run (quoted, pinned to 7364096)

1. Working tree, as briefed: `.venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2`
   ```
   ........................................                                 [100%]
   40 passed, 730 deselected in 2.16s
   ```
   Later in the session the working tree (other agent's in-flight work) reported `43 passed, 762 deselected`. The pinned count is the one I cite.

2. Working tree, as briefed: `jq '.metrics.grounding_rate, .ship_bar_met' evals/reports/latest.json`
   ```
   { "checked": 242, "failures": [], "r_ids": [...], "value": 1.0 }
   false
   ```

3. Pinned: `git archive 7364096 | tar -x -C <scratch>/pinned`, then `pytest tests/unit -q -k eval -p no:cacheprovider`
   ```
   40 passed, 730 deselected in 2.14s
   ```

4. Pinned: `pytest -k "grounding_uses_the_record_keys or tampered_two_run"`
   ```
   2 passed, 768 deselected in 0.86s
   ```

5. Committed report: `git show 7364096:evals/reports/latest.json | jq ...`
   ```
   {"ship_bar_met":false,"blockers":["3_flags","4_no_invented_facts","backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)"],"g":1.0,"gf":0,"causation_prec":0.5,"must_not":1}
   ```

6. Pinned CLI, scratch `--out` (repo `evals/reports/` not written): `python -m evals.run --out <scratch>/pout`
   ```
   CLI rc=1
   ship_bar_met=False backend=fixture report=.../pout/20261102T021052Z.md
     blocker: 3_flags
     blocker: 4_no_invented_facts
     blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
   ```
   Re-run output matches the committed bars and metric values. `--check-fresh` on the pinned copy: rc=0.

7. Pinned bar detail, from the CLI output: `bars` = `1_grounding true, 2_recall true, 3_flags false, 4_no_invented_facts false`. `flag_precision.causation` = 0.5 (threshold 0.9, `evals/run.py:35`). `golden_must_not_hits.value` = 1, detail `case_05_provider_conflict.must_not_flag = [{candidate_type: causation, must_not_flag: N2}]`. `hallucination_catch_rate` = 1.0, `case_07_total_420` = true. The two failing bars trace to the causation candidate on case_05 and to causation precision. Per the brief these are product metrics. I did not adjudicate the causation finding itself (product lane). The harness numbers are internally consistent with their detail fields.

8. Grep for the key: `grep -n 'source' evals/run.py`
   ```
   265: ... # run_case record keys: id, seq, n, source, date_iso, date_status
   278: chk(f"entry {e.get('id')} provider", norm(e.get("provider")) == norm(first["source"]))
   370: rec = {"n": n, "source": m.group(3), ...}
   ```
   `grep -n source_label` on evals/ and the real-run_case test: no `source_label` read remains in `evals/`. The only hits are in the test's own assertion and docstring.

9. Mutations on the pinned copy (`run.py` restored and diffed to 7364096 after each; each asserts exactly one occurrence):

   | Id | Mutation | Result |
   |---|---|---|
   | M9 | remove `and m["determinism_3run"].get("runs") == 3` from bar 4 | 1 failed: `test_tampered_two_run_determinism_fails_bar_4_alone` (killed) |
   | M10 | `first["source"]` back to `first.get("source_label")` | 3 failed: `test_grounding_uses_the_record_keys_run_case_really_emits`, `test_perfect_run_meets_ship_bar_on_a_live_backend`, `test_check_spec_recomputes_the_bar_in_a_full_report` (killed) |
   | M11 | provider `chk(...)` removed | 1 failed: `test_grounding_uses_the_record_keys_run_case_really_emits` (killed) |
   | M12 | `grounding()` returns `failures: []` | 2 failed: `test_each_missed_bar_names_the_failed_bar_and_only_that_bar[1_grounding-...]`, `test_grounding_uses_the_record_keys_run_case_really_emits` (killed) |

10. Other greps and reads: `grep -n "except Exception"` over the touched files. `app/backend/review.py:108` has a broad `except Exception:` (see minor below). `app/backend/judges.py:90-95` `to_ladder` maps `unavailable` to `unavailable`, and `app/backend/confidence.py:59-71` turns that into a doubt (needs_review). Judge failure is fail-closed on this path.

11. Fixture run stderr, pinned CLI: 32 `llm call failed ... step=j1|j2|j3|j4 attempt=1 prompt_hash=...` lines per run. Visible, not swallowed. `judges.py:33` maps `LLMFailed` to `unavailable`, so the metrics do not count a miss as a pass.

## Findings

**Major: the eval's record shape is not the documented API record shape, and the eval never exercises the API path.**
`run_case` records carry `source` (`app/backend/store.py:26`, `"source": d["source_label"]`). The HTTP record view carries `source_label` (`app/backend/present.py:132`), and the contract documents `source_label` (`memory/contracts/api.md:54`, `:88`). `case_view` returns `out["records"]` unchanged (`app/backend/pipeline.py:331`), so the eval input is the store shape. The `case_view` docstring at `app/backend/pipeline.py:324` says it is "the GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md)". That is not true for records. `grep -n "present\|record_view\|case_view" evals/run.py` returns nothing, so no eval test covers the `source_label` mapping at `present.py:132`. A regression there would leave the ship bar green. The round-2 acceptance test ("case_view records include source_label equal to the record header") is not met, and the r2 fix list offered a shared mapper as the alternative. The r3 fix took the internal-shape route without updating the docstring or adding the API-side check.
Why it matters: the grounding check is meant to prove the product's served records match their headers. It currently proves that for the internal shape only. Both shapes can be correct today and still drift apart silently.
Fix: either (a) have one record mapper used by both `store`→`run_case` and `present.record_view`, or (b) keep `source` in `run_case` and add a test that builds the API-shaped records through `present.record_view` and runs `grounding()` on them with zero provider failures. Correct the `pipeline.py:324` docstring either way.
Acceptance test: a new test runs `grounding()` on the `present.record_view` output for the sample and expects no `provider` failures; mutating `present.py:132` to `r.get("source")` must fail it.

**Minor (outside T-038 card scope, observed while checking the eval path): broad `except Exception` in the review edit path.**
`app/backend/review.py:108-109`: `except Exception: verdict, call_id = "unavailable", None`. This does not swallow into `verified` (`to_ladder` and `compose_state` keep it a doubt), but it drops the exception type and message with no log, against checklist item 12. It is not on the eval path, so it does not affect the T-038 verdict. Route it to the card that owns `review.py`.

**Minor (out of card scope): no test for `pipeline.py:324` docstring accuracy.** Folded into the major above; listed here only so the docstring fix is not lost.

No blocker. Bar 3 and bar 4 failures are product metrics, reported correctly. The ship bar is not met, and the runner says so.

```json
{"card": "T-038", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 7364096 (pinned via git archive; HEAD has moved to 7a450a1 and the working tree is dirty with another agent's uncommitted evals/run.py work, not reviewed); evals/run.py; tests/unit/test_eval_runner.py; app/backend/store.py:26, present.py:132, pipeline.py:324-331, review.py:108 (read only); committed evals/reports/latest.json; fixture backend; sample case and golden cases via run_case; no app URL exercised (eval CLI only)",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-038-staff-engineer-r2.md, eval memory note",
  "working tree: .venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2 -> 40 passed, 730 deselected (later 43 passed, 762 deselected as the working tree changed)",
  "working tree: jq '.metrics.grounding_rate, .ship_bar_met' evals/reports/latest.json -> checked 242, failures [], value 1.0; false",
  "git show 7364096 -- evals/run.py tests/unit/test_eval_runner.py read in full",
  "git archive 7364096 extracted to a scratch dir; pytest -k eval -> 40 passed, 730 deselected; -k 'grounding_uses_the_record_keys or tampered_two_run' -> 2 passed",
  "git show 7364096:evals/reports/latest.json | jq -> ship_bar_met false, blockers 3_flags, 4_no_invented_facts, backend=fixture; grounding 1.0 with 0 failures; causation precision 0.5; must_not 1",
  "pinned CLI python -m evals.run --out <scratch> -> rc 1, ship_bar_met False, same three blockers, 32 llm-call-failed warnings on stderr; repo evals/reports/ not written",
  "pinned --check-fresh -> rc 0",
  "grep -n source evals/run.py (pinned): line 278 uses first[\"source\"]; no source_label read remains in evals/",
  "grep -n present|record_view|case_view evals/run.py -> no hits (eval never reaches the API record view)",
  "scratch mutations on pinned copy, run.py restored and diffed to 7364096 after each: M9 (runs==3 term) 1 failed; M10 (source_label revert) 3 failed; M11 (provider check removed) 1 failed; M12 (grounding failures silenced) 2 failed",
  "git show 7364096:app/backend/{present.py:132,store.py:26,pipeline.py:324-331,review.py:108}, memory/contracts/api.md:54,88 read for shape comparison",
  "git show 7364096:app/backend/judges.py / confidence.py path for unavailable judge: fail-closed to needs_review, no verified"],
 "verdict": "changes",
 "scores": {"determinism_and_code_vs_llm_split": 4, "failure_visibility": 4, "test_strength": 4, "spec_conformance": 3, "ship_bar_integrity": 5},
 "findings": [
  {"severity": "major", "title": "Eval reads the internal run_case record shape (source); the documented API record shape is source_label, and the eval never exercises the API record view",
   "evidence": "app/backend/store.py:26 `\"source\": d[\"source_label\"]`; app/backend/present.py:132 `\"source_label\": r[\"source_label\"]`; memory/contracts/api.md:54 `\"source_label\": \"Austin EMS run report\"`; app/backend/pipeline.py:324 docstring 'the GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md)' while pipeline.py:331 returns out['records'] unchanged; `grep -n present|record_view|case_view evals/run.py` returns no hits",
   "why_it_matters": "The provider grounding check validates a shape the product's API does not serve. A regression in present.py:132 or a drift between store and API shapes would leave the ship bar green. The docstring claims a contract that is not true for records. Round-2's acceptance test (case_view records include source_label equal to the record header) is not met.",
   "fix": "Use one record mapper shared by the store-to-run_case path and present.record_view, or keep 'source' in run_case and add a grounding test over present.record_view output. Correct the pipeline.py:324 docstring.",
   "acceptance_test": "New test: grounding() over the present.record_view output for the sample has no provider failures; mutating present.py:132 to r.get('source') makes it fail."},
  {"severity": "minor", "title": "Broad except Exception in review edit path swallows the exception type and message (outside T-038 card scope)",
   "evidence": "app/backend/review.py:108-109 `except Exception:` / `verdict, call_id = \"unavailable\", None`",
   "why_it_matters": "Fail-closed (to_ladder keeps 'unavailable' as a doubt via confidence.py:59), so it is not a silent verify. But checklist item 12 forbids broad catches, and the reason is discarded with no log line. Not on the eval path, so not a T-038 defect.",
   "fix": "Catch the specific LLM and validation errors (AU.LLMFailed, ValidationError, TypeError, ValueError as judges.py:33-41 does), and log the code before mapping to unavailable.",
   "acceptance_test": "Test with a fixture backend raising RuntimeError in the j1 call asserts the exception propagates or is logged with its code, and the item is needs_review."}
 ],
 "whats_right": [
  "Grounding reads the key run_case emits (evals/run.py:278); the committed report shows 242 checks and 0 failures, and M10 (revert to source_label) fails three tests.",
  "The real-run_case test (tests/unit/test_eval_runner.py:287-296) has a negative control (an invented provider is detected), so it is not vacuous; M11 and M12 both fail it.",
  "Exit codes are split: unmet bar exits 1 (evals/run.py:629), curated refusal stays 2, verified by the pinned CLI run and test_curated_fixture_set_is_refused_with_exit_2."],
 "questions_for_chris": [
  "Commit 7364096 says 'first full run on recorded fixtures', yet the pinned CLI logs 32 'llm call failed ... step=j1..j4' FixtureMiss lines per run. Does the recorded set cover j1-j4 for all golden cases? The round-2 question is still open, and the fixture-backed hallucination numbers depend on the answer."]}
```
