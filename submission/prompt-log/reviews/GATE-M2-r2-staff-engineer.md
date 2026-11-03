# GATE-M2 round 2 staff-engineer review (pinned 7cfdb0b, `git archive` copy plus a `git clone` checked out at 7cfdb0b for the git-dependent tests)

Verdict: **changes** (0 blockers, 1 major, 3 minors). The three round-1 defects I filed are fixed and hold under probes I wrote myself. The M2 ship-bar evidence is now a real live report. One new major: the unit suite is red at the pinned commit.

## Round-1 findings, re-checked

1. **Deadline path never shows `verified` (round-1 blocker): fixed.** Probe through `run_pipeline` with an injected clock that jumps past `deadline_s` as each of the 7 stages starts (`extract, verify, judge_entries, amounts, conflicts, flags, finalize`). When the clock jumps at `extract` or `verify` (judge 1 never runs), all 9 entries are `('needs_review', judge 'unavailable')`, 0 are `verified`, and `apply_batch(accept, all 9 ids)` raises `BatchRefused` for all 9. When the clock jumps later, judge 1 did run and the entries are `verified` with `judge supported`, which is correct. Amounts that missed a judge stay `needs_review`. After accepting every item one at a time on the deadline cases, `trace.export_blockers` still returns `JUDGE_NOT_RUN` and `RUN_FAILED` (jump at `verify`) or `RUN_FAILED` (jump at `conflicts`). Mutant: replacing `_mark_judge_not_run(entries, by_n)` (pipeline.py:568) with `pass` makes `tests/unit/test_t145_judge_not_run.py` go 4 failed, 1 passed.
2. **Re-runs lose no decided or hand-entered work (round-1 major): fixed.** Probe: first run with record 3's extract down, a hand entry for r3 (`e3_m`), e1 accepted, e2 dismissed, 24 items stored. A re-run with the deadline at each of the 7 stages, a clean re-run, and a re-run with extract down again all end with 24 items, 0 lost, 0 `review_status` changes, hand entry still `pending` and present, decided entries still `accepted` and `dismissed`. An accepted entry for r6 survives a re-run in which r3 is now extracted (ids are keyed by record number, so no shift). Mutant: removing the `_keep_hand_entry` call (pipeline.py:376-377) makes 4 of the 91 T-145/T-146/T-161/T-165 tests fail.
3. **A passing ship-bar report close to HEAD (round-1 major): evidence is present, with two caveats (F2 below).** `evals/reports/20261102T164038Z.md` reads `ship_bar_met: True`, backend `claude-cli`, source `312efe6`, tree clean, determinism_3run 1.0, unsupported_count_3run 0, J3 20/20 and J4 12/12 caught over 3 runs with 0 false agree, grounding 1.000 (242), entry recall 0.982, amount recall 1.000, flag P/R 1.000, hallucination catch 40/40, golden_must_not_hits 0, letter_currency_outside_charges 0. I re-derived the 17 prompt and lexicon hashes in that report against the files at 7cfdb0b: no difference. The calibration.json hashes also match HEAD.

## End-to-end correctness pass

- `pytest tests/unit -q -p no:cacheprovider` on the archive with `LLM_BACKEND=fixture`: **2 failed, 5284 passed, 8 skipped** (4 min 23 s). On the clone at 7cfdb0b (which has `.git`) the two eval-runner/e2e-contract files give **3 failed, 108 passed**. See F1.
- `LLM_BACKEND=fixture python -m evals.run`: exit 1, `ship_bar_met=False` for the three live-only reasons (determinism_3run / unsupported_count_3run need a live backend; judge_controls not measured; item 4 depends on both). Every measured metric is at bar: grounding 1.000 (241), entry recall 0.982, amount recall 1.000, flag P/R 1.0 for all four types, hallucination catch 40/40, golden_must_not_hits 0. A fixture run can never set the bar true, so the live report above is the evidence.
- `python -m app.pipeline evals/golden/sample.txt` twice: rc 0 both, `cmp` identical, 45 lines, 73-day gap `[verified]`, `$185 (rate)` listed as rate, "Charges detected, pending review (not a total): $8,390.00; accepted so far: $0.00".
- gate.ready versus export through the HTTP app (`TestClient`, fixture backend, local mode) on the sample and lib01, lib03, lib11, five scenarios each (untouched, accept all, accept all with the first entry dismissed, dismiss all, accept only entries): **20 of 20 agree, 0 mismatches**. `gate.ready` false gives export 422 `NOTHING_ACCEPTED`; true gives 200. Accepted totals: sample 839000 cents, lib01 391500, lib03 750000, lib11 326000 (ED charge plus the two dated ledger lines per D-060). No per-visit rate ($185, $140, $120) appears in any exported letter. Accept-only-entries exports a total of 0 cents, so a total is never invented without an accepted charge. (lib01 reads `failed` first because record 3 has no recorded extract answer; I used the T-165 hand-entry helper `tests/unit/_hand_entry.py`, which is the documented route.)
- Greps: `except Exception` in `app/` now also in `review.py:232,262`, `case_extras.py:73`, `pipeline.py:205`; I read each, all are rollback or compensate and re-raise (no swallow). Two display-only swallows remain, see F3. `float(` is only timestamps and cost. `tools/check_secrets.py` cannot run on a git-less archive (blocked by design), not re-run.

## Findings

F1 is a major. F2 to F4 are minors. Details are in the JSON block.

```json
{
  "card": "GATE-M2",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "git archive 7cfdb0b scratch copy plus a git clone checked out at 7cfdb0b (git-dependent tests); app/backend/{pipeline,review,case_extras,export,trace,store,language}.py, app/llm/_types.py, docs/LLM_VS_CODE.md, evals/reports/20261102T164038Z.md and calibration.json; fixture backend; sample case and library lib01, lib03, lib11",
  "exercised": [
    "read reviews/GATE-M2-round1-triage.md, my round-1 review, fix cards T-139/T-140/T-141/T-145/T-146/T-161/T-165 (board.py show), SCOPE_CUTS 7c-7f and 13c-13f",
    "pytest tests/unit -q -p no:cacheprovider on the git archive: 2 failed, 5284 passed, 8 skipped",
    "pytest tests/unit/test_eval_runner.py tests/unit/test_e2e_contract.py in a git clone at 7cfdb0b: 3 failed, 108 passed",
    "LLM_BACKEND=fixture python -m evals.run: rc 1, ship_bar_met False (live-only blockers), all measured metrics at bar",
    "python -m evals.run --check-fresh in the clone: rc 1 (committed latest.json is the 2026-11-02T09:56:40Z fixture run); compared the 17 prompt/lexicon hashes of evals/reports/20261102T164038Z.md and calibration.json with the files at 7cfdb0b: no difference",
    "python -m app.pipeline evals/golden/sample.txt twice: rc 0, cmp identical",
    "own run_pipeline probe with an injected clock past the deadline at each of the 7 stages: entry/amount/flag states and judge verdicts, apply_batch accept of all entries, accept-one-by-one then trace.export_blockers",
    "own re-run probe (hand entry for r3, e1 accepted, e2 dismissed, 24 items) with the deadline at each of the 7 stages, a clean re-run and an extract-down re-run: items lost, review_status changes, hand entry kept; r6 accepted entry through a re-run that recovers r3",
    "own HTTP probe (TestClient, fixture backend): gate.ready versus GET /export on sample, lib01, lib03, lib11 x 5 scenarios: 20/20 agree, totals, rate figures absent from letters",
    "mutants on the scratch copy, each restored and diffed: _mark_judge_not_run removed (4 fail), _keep_hand_entry removed (4 fail)",
    "git diff 312efe6 7cfdb0b for app/llm/_types.py, app/backend/pipeline.py, app/backend/export.py; grep of except Exception, float(; read of the except blocks in review.py, case_extras.py, pipeline.py, store.py",
    "grep of docs/LLM_VS_CODE.md for the round-1 stale limitation and citations; board.py show T-169; board.py list"
  ],
  "verdict": "changes",
  "scores": {
    "llm_code_boundary_as_implemented": 5,
    "deterministic_code_and_tests": 4,
    "failure_visibility_no_silent_fallback": 5,
    "audit_pinning_retries_timeouts": 5,
    "test_quality_mutation_sensitivity": 4,
    "doc_matches_code": 3,
    "ship_bar_evidence_at_head": 4,
    "unit_suite_green_at_gate_commit": 2
  },
  "findings": [
    {
      "severity": "major",
      "title": "The unit suite is red at the pinned gate commit 7cfdb0b: 3 tests fail, and the open card T-169 covers only one of them",
      "evidence": "Archive: `LLM_BACKEND=fixture python -m pytest tests/unit -q -p no:cacheprovider` -> `2 failed, 5284 passed, 8 skipped`. (1) tests/unit/test_eval_runner.py:801 `assert c[\"backend\"] == \"fixture\" and re.fullmatch(...)` fails: `'claude-cli' == 'fixture'` because commit 7cfdb0b replaced evals/reports/calibration.json with the live claude-cli re-measure (`backend: claude-cli`, `source_commit: 312efe6...`). Card T-169 (in_progress, claimed by qa, AC 'unit suite green') relaxes only this assertion. (2) tests/unit/test_e2e_contract.py:24 `test_every_test_id_is_declared` fails with `['do-first-item', 'btn-new-case', 'cases-keys']`: tests/e2e/test_multicase.py:563,581,609 use those test ids (added with f7a8f2a, T-149 r3) but tests/e2e/conftest.py's contract docstring does not declare them; no card covers it (board grep of the test name finds only T-072/T-165/T-168/T-169 text, none for these ids). (3) Visible only with a `.git` (clone at 7cfdb0b): tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit fails, because it regenerates calibration.json from 312efe6 on the fixture backend and the committed file now holds live counts (`'...matched the record 6/6 times in testing on the fixture b...'` versus the claude-cli wording). Relaxing the T-169 header assertion alone leaves this test red, and it is the guard that stops a hand-edited calibration (T-090 r2).",
      "why_it_matters": "Checklist 13/14 and CLAUDE.md non-negotiable 8: deterministic checks run before opinions, and a milestone gate cannot be passed on a suite that fails at the gate commit. The calibration guard is the only thing proving the counts shown to the paralegal ('82/83 matched in testing') come from the named commit; the easy fix for a red test (loosen it) would weaken that proof. The e2e contract test exists so frontend and tests share one set of hook names; three hooks are undeclared.",
      "fix": "T-169 (or a sibling card) must make the regenerate guard compare like with like: for a live calibration, check hashes, totals arithmetic, source commit exists and is an ancestor of HEAD, and re-derive the counts from the committed live per-run artifacts (evals/reports/runs/20261102T161327Z/*.json) instead of a fixture re-run; keep the fixture re-run for fixture calibrations. Add the three test ids to the tests/e2e/conftest.py contract docstring (or remove them from the specs). Re-run the full suite on a git clone, not only an archive, so the git-dependent tests execute.",
      "acceptance_test": "In a `git clone` checked out at the fix commit, `LLM_BACKEND=fixture python -m pytest tests/unit -q -p no:cacheprovider` reports 0 failed. Control: edit one count in evals/reports/calibration.json (e.g. 82 to 83) and the calibration tests fail; edit a hash and they fail."
    },
    {
      "severity": "minor",
      "title": "The mechanical freshness check still fails: `python -m evals.run --check-fresh` exits 1 at HEAD because latest.json is the old fixture run, and backend code changed after the live run's source commit",
      "evidence": "In the clone at 7cfdb0b: `python -m evals.run --check-fresh` -> rc=1, `check-fresh: app/llm/lexicon.yaml changed since the report`, `check-fresh: app/llm/prompts/judge_conflict_v6.md changed since the report`. Committed evals/reports/latest.json: generated_at 2026-11-02T09:56:40Z, backend fixture, ship_bar_met False, source_commit None. The live report 20261102T164038Z.md is fresh by my hash comparison (17/17 equal), so the evidence is real, but nothing the tool reads points at it. Also `git diff --stat 312efe6 7cfdb0b -- app/backend app/llm` shows 6 app files changed after the live run's source commit, including app/llm/_types.py (T-168: `_closing_object` makes parse_json_reply accept a reply that ends with a JSON object after an earlier draft) and pipeline.py (T-165 r2); the live run did not exercise the new parser path.",
      "why_it_matters": "Round-1 acceptance asked for check-fresh rc 0 at the gate commit. A reader (or a script) following the repo's own freshness command gets a failure and has to know to look at the dated .md instead. The parser change widens what counts as a valid model reply after the measurement; it is schema-, grounding- and judge-checked downstream, so I rate it minor, but it is a post-measurement change in the LLM-facing path.",
      "fix": "After the card fixes land, run the live 3-run once more from a clean tree at the final gate commit so latest.json is the live report (check-fresh rc 0) and the T-168 parser is in the measured code.",
      "acceptance_test": "`python -m evals.run --check-fresh` exits 0 at the gate commit and latest.json shows backend claude-cli, ship_bar_met true, source commit equal to the gate commit."
    },
    {
      "severity": "minor",
      "title": "Carry-over from round 1: docs/LLM_VS_CODE.md still states a limitation the code no longer has, and its file:line citations have drifted",
      "evidence": "docs/LLM_VS_CODE.md:97 still reads 'The shared judge path used by manual entry and \"not a duplicate\" (review.py) catches any exception and reports JUDGE_UNAVAILABLE ... narrowing it to provider errors is a code change with no card yet.' The code uses judge_guard.guarded (T-073). Row 4 still cites `summary_trim.py:391` while `def trim` is at summary_trim.py:379.",
      "why_it_matters": "The doc's own last line says a difference between table and code is a defect. This is the same state as round 1; no card was filed for it in the round-1 triage.",
      "fix": "Rewrite the bullet to describe judge_guard; use function names instead of line numbers.",
      "acceptance_test": "A unit test that every `file.py:NNN` citation names a line containing the cited symbol, or the citations are function names only."
    },
    {
      "severity": "minor",
      "title": "Carry-over from round 1: two broad `except Exception` display fallbacks and sleep-polling tests",
      "evidence": "app/backend/store.py:37-40 `try: body = ingest.split_records(block)[0][\"excerpt\"] except Exception: body = block`; app/backend/language.py:323 same pattern. tests/unit/test_trace.py:56 and tests/unit/test_t116_gap_endpoints.py:226 poll with `time.sleep(0.25)`.",
      "why_it_matters": "Checklist 12 and 14. Display-only today, but a splitter bug would be hidden, and polling loops can flake under load.",
      "fix": "Narrow the except to the splitter's expected errors; join the run thread or inject a clock in the polling tests.",
      "acceptance_test": "A test where split_records raises TypeError and the loader propagates; the status tests complete without time.sleep."
    }
  ],
  "whats_right": [
    "Fail-closed judge state is now structural: a run that never reached judge 1 composes needs_review with a judge verdict of 'unavailable', batch accept refuses all nine, and the export gate adds JUDGE_NOT_RUN and RUN_FAILED; killed by a 4-test mutant check.",
    "Re-runs are loss-free at every one of the 7 deadline stages: decided entries, hand entries and pending items all survive, and ids are keyed by record number so a recovered record cannot shift a decided entry.",
    "gate.ready and the export endpoint agree 20/20 across the sample and lib01/lib03/lib11, no per-visit rate reaches a letter, and the live ship-bar report's 17 prompt/lexicon hashes equal the files at HEAD."
  ],
  "questions_for_chris": []
}
```
