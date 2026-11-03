# GATE-M2 staff-engineer review (pinned 0c24f5f, `git archive` copy)

Verdict: **fail** (1 blocker, 2 majors, 2 minors).

What I ran, on a `git archive 0c24f5f` copy, with the project `.venv/bin/python`:
- `pytest tests/unit -q -p no:cacheprovider`: **3450 passed, 8 skipped** (run twice, same result). The 8 skips are archive-only (no `.git`, `e79c3aa` not in the archive) plus one live-only Spanish judge eval (needs `SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1`).
- `LLM_BACKEND=fixture python -m evals.run`: exit 0, **`ship_bar_met=False`**. Blockers: `4_no_invented_facts`, "determinism_3run and unsupported_count_3run need a live backend (R-CO-7)", "judge_controls (J3/J4 seeded wrong items): not measured". Measured: grounding 1.000 (241), entry recall 0.982, amount recall 1.000, flag P/R 1.0 on all four types, hallucination catch 40/40, gap 28 not flagged and 73 flagged, case_07 total $420. A fixture run can never set ship_bar_met true, so it is not ship-bar evidence.
- `python -m evals.run --check-fresh` against the committed `evals/reports/latest.json`: **rc=1** ("app/llm/lexicon.yaml changed since the report", "judge_conflict_v6.md changed since the report").
- `python -m app.pipeline evals/golden/sample.txt` twice: rc 0 both, `cmp` identical, 9 entries, 10 flags, 3 amounts, 73-day gap, $8,390.00 pending and $0.00 accepted, the $185 listed as a rate.
- Mutation spot-checks on a scratch copy, each restored after: grounding `check_excerpt` returns `[]` (2 tests fail), gap `>` to `>=` (3 fail), totals counting `rate` (3 fail), export treating `dismissed` as in (5 fail), judge verdict ignored in `compose_state` (16 fail). All killed.
- Probes through `run_pipeline` with an injected clock (fixture backend): the deadline expiring after each stage, and a timed-out re-run.
- Read in full: `pipeline.py`, `generator.py`, `judges.py`, `judge_guard.py`, `confidence.py`, `llm/audited.py`, `llm/provider.py`, `llm/backends/claude_cli.py`, `schemas.py`, `flags.py` (judge and tray half), `totals.py`, `export.py` and `export_routes.py` (gate and letter), `narrative.py`, the judge-not-run half of `trace.py`, `case_extras.py` batch.
- Greps: `except Exception`, `float(`, `sleep(`, retry, network calls in tests, secrets (`tools/check_secrets.py`: ok, 2100 files).
- Doc cross-check: `docs/LLM_VS_CODE.md` rules 1-11 and rows 1-20 against the code, including every file:line citation I could find.

Not exercised: a live `claude-cli` eval (many model calls, needs `ENABLE_LIVE=1`). The 3-run determinism and the J3/J4 control catch rate at HEAD are therefore unmeasured by me. The stored live evidence is dated and stale, see F3.

Findings F1 (blocker), F2 and F3 (major), F4 and F5 (minor) follow in the JSON block.

```json
{
  "card": "GATE-M2",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "git archive 0c24f5f scratch copy; app/backend/{pipeline,generator,judges,judge_guard,confidence,flags,totals,export,export_routes,narrative,trace,case_extras}.py, app/llm/{audited,provider}.py + backends, docs/LLM_VS_CODE.md, evals/reports; fixture backend; sample case evals/golden/sample.txt",
  "exercised": [
    "pytest tests/unit -q -p no:cacheprovider on the archive: 3450 passed, 8 skipped (archive/live-only), twice",
    "LLM_BACKEND=fixture python -m evals.run: exit 0, ship_bar_met=False (live-only blockers), all measured metrics at bar",
    "python -m evals.run --check-fresh vs committed latest.json: rc=1, lexicon.yaml and judge_conflict_v6.md changed since the report",
    "python -m app.pipeline evals/golden/sample.txt twice: rc 0, cmp identical",
    "5 mutants on a scratch copy (grounding removed, gap >=, rate totaled, dismissed exports, judge ignored): all killed by unit tests",
    "run_pipeline probes with an injected clock: deadline after verify, judge_entries, amounts, conflicts; and a timed-out re-run of a finished case",
    "batch accept and export_blockers on the timed-out case",
    "ingest + extract_amounts on 10 mg, 35 mph, 7/10, approx. 40%, missing 3 days of work, $6,240, $2,150, Charge per visit $185; sample with record 2 pasted twice (one duplicate group [2,3], ER charge listed once)",
    "git show of committed eval reports (20261102T032823Z, 035750Z, 040933Z, 081339Z, controls-20261102T123937Z) and prompt-hash comparison against the archive",
    "grep of except Exception, float(, sleep(, retry, network calls in tests, secrets; tools/check_secrets.py",
    "read of the pipeline end to end and the LLM_VS_CODE rows against the code, including file:line citations"
  ],
  "verdict": "fail",
  "scores": {
    "llm_code_boundary_as_implemented": 4,
    "deterministic_code_and_tests": 5,
    "failure_visibility_no_silent_fallback": 2,
    "audit_pinning_retries_timeouts": 5,
    "test_quality_mutation_sensitivity": 4,
    "doc_matches_code": 3,
    "ship_bar_evidence_at_head": 2
  },
  "findings": [
    {
      "severity": "blocker",
      "title": "A run that hits its deadline before judge 1 leaves every AI entry 'verified' with no judge verdict (silent fallback to verified)",
      "evidence": "app/backend/pipeline.py:344 `if guard(\"judge_entries\") and entries: generator.judge_entries(...)`: when the deadline has passed, the stage is skipped and the entries keep the state computed at verify time. generator.py:109-127 `compose` leaves `st['judge']` unset (None) and confidence.py:62 `_lookup(_JUDGE, None, none_ok=(\"supported\",))` adds no doubt, so a missing judge composes to `verified`. Repro (fixture backend, injected clock that jumps to 10000 s when the 'verify' stage starts, `run_pipeline(conn, cid, raw, now=..., on_stage=..., deadline_s=480)`): `status timeout {'code': 'run_deadline', ...}`; entries e1..e9 `('e1','verified',None)` (state, judge verdict None); `DB.get_item('e1')` -> `state verified [] judge None`; review counts `{'pending': 15, 'verified': 11, 'needs_review': 4}`; the case view 'why' for e1 reads 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.' although no second check ran; `case_extras.apply_batch(conn, cid, {'action':'accept','item_ids':['e1'..'e9']}, 5.0)` accepts all nine because batch accept keys on `state == 'verified'` (case_extras.py:48-49). Mitigations that held in my probe: the item trace shows `judge_1 skipped JUDGE_UNAVAILABLE`, and `trace.export_blockers` returned ['RUN_FAILED', 'JUDGE_NOT_RUN' x9] so nothing exported. Amounts are fail-closed (a1 needs_review JUDGE_UNAVAILABLE) so only entries are affected. No test covers it: tests/unit/test_t037_backend.py:125-133 and test_pipeline.py:117-122 assert only status, the run_deadline code and the gap flag.",
      "why_it_matters": "CONTRACT section 5.2 defines `verified` as grounding ok AND judge supported, and the persona's red flag is a judge that did not answer marking an item verified. Here the state, the headline 'verified' count, the Why sentence ('the second check agreed') and the batch-accept eligibility all say the AI entry was double-checked when it was not. The export gate and the failed-run banner are the only things between that state and the letter, and the paralegal can bulk-accept nine unchecked entries into the record of decisions before the gate refuses. Fail-open by omission of a key is the pattern the rest of the code base avoids (compose_state raises on a misspelled key for exactly this reason).",
      "fix": "Make 'no judge verdict' fail closed for every AI-made item. Either default `judge` to 'unavailable' for LLM-origin entries in `generator.compose` until `judge_entries` sets a real verdict, or, in run_pipeline after the judge stage, recompose any entry whose `ladder.judge` is None with `judge='unavailable'` (reason JUDGE_UNAVAILABLE). Do not let batch accept see these entries as verified. Optionally make `compose_state` require an explicit `judge` key (value or None for code-only items) so a caller that forgets it raises.",
      "acceptance_test": "Unit test: run_pipeline with a clock that expires after the 'verify' stage; assert every entry has state needs_review with JUDGE_UNAVAILABLE in reasons, none is verified, the case 'why' does not say the second check agreed, and apply_batch(accept) over those ids raises BatchRefused('not_verified'). Mutation check: reverting the fix makes this test fail."
    },
    {
      "severity": "major",
      "title": "A timed-out re-run deletes the previous run's pending items and then says 'finished items were kept'",
      "evidence": "app/backend/pipeline.py:404-406 `_persist(...)` runs with the partial result, and :242-244 deletes every existing row that is `pending` and not in the new item set. Repro: run the sample to completion (stored entries 9, flags 11, amounts 4), then `run_pipeline` again on the same case with a clock that is past the deadline from the first stage check. Output: `run2 timeout 0 stored entries 0 flags 2 amounts 4`; case status `failed`, error `{\"code\": \"run_deadline\", \"message\": \"The run passed its time limit; finished items were kept.\"}`. Nine entries and nine model flags are gone; only the code flags (2) and the stage-0 amounts survive. Same mechanism if the deadline passes mid flags stage (:373-376 drops that record's flags). Decided items are kept, which is why the message is half true; pending ones are not.",
      "why_it_matters": "Honest failure: the message is false for pending items, and a paralegal who sees 'finished items were kept' will not know that her queue was emptied until she looks. Persisting a partial run over a complete one is a data-loss path on a normal failure (slow backend), not an edge case. The record text still exists, so the loss is recoverable by another run, which makes it major rather than blocker.",
      "fix": "Delete stale pending rows only for the kinds and stages that actually completed in this run (track `stage_done`), or skip the stale-delete entirely when `timed_out`. Keep the old rows and mark the run failed. Correct the message to say what was kept.",
      "acceptance_test": "Unit test: complete run, then a re-run that times out in extract; assert the number of stored entries and model flags is unchanged and the case is failed with run_deadline. Add the variant where the deadline passes between the flags of record 3 and record 4."
    },
    {
      "severity": "major",
      "title": "M2 exit (ship bar met) has no passing report at HEAD; the committed eval record is stale and the last full live run is ship_bar_met False",
      "evidence": "`python -m evals.run --check-fresh` at 0c24f5f exits 1: 'app/llm/lexicon.yaml changed since the report' and 'app/llm/prompts/judge_conflict_v6.md changed since the report' (committed latest.json is a fixture run from 2026-11-02T09:56:40Z, source commit ea6ac71, tree dirty). Committed full live reports: evals/reports/20261102T032823Z.md is the only `ship_bar_met: True` and it predates D-046 (J3/J4 seeded controls now gate item 4); 20261102T035750Z.md, 040933Z.md and 081339Z.md (claude-cli, source 789cb39) are all `ship_bar_met: False` (081339Z: blockers `4_no_invented_facts`, golden_must_not_hits 1). The 081339Z run used lexicon hash differing from HEAD and judge_conflict_v5; HEAD's PROMPT_OF_STEP maps j3 to judge_conflict_v6 (app/llm/audited.py:123). evals/reports/controls-20261102T123937Z.md (live, bea3984, v6) shows J3 19/19 and J4 12/12 x3, but that is controls only, not determinism_3run or unsupported_count_3run. My own fixture run reports ship_bar_met=False for the expected live-only reasons.",
      "why_it_matters": "CONTRACT M2 exit is 'evals meet the ship bar (section 8.2)' and 8.3 requires a re-run and report path after any prompt, model or lexicon change. At the pinned commit nothing in the repo shows the four automated bars (grounding, recall, flags, no invented facts including 3-run determinism and J3/J4 controls) holding together on a live backend with the current lexicon and judge prompt. The fixture-backend numbers are all at bar, but fixtures replay recorded answers and cannot show determinism.",
      "fix": "From a clean tree at the gate commit, run `LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run` (3 runs) plus the J3/J4 controls, commit the report, and attach the path to the gate record. If it is False, record the blocker honestly in the gate summary (do not pass M2 on the fixture run).",
      "acceptance_test": "`python -m evals.run --check-fresh` exits 0 at the gate commit and the attached live report shows `ship_bar_met: True`, determinism_3run 1.0 over 3 runs, unsupported_count_3run 0, J3 and J4 all wrong items caught with 0 false agree."
    },
    {
      "severity": "minor",
      "title": "docs/LLM_VS_CODE.md states a limitation the code no longer has, and its file:line citations have drifted",
      "evidence": "Line 97 of the doc: 'The shared judge path used by manual entry and \"not a duplicate\" (review.py) catches any exception and reports JUDGE_UNAVAILABLE ... narrowing it to provider errors is a code change with no card yet.' Code: review.py:269 and reclassify.py:173 call `judge_guard.guarded(...)`, which catches only `(AU.LLMFailed, P.LLMError)` (judge_guard.py:8), and review.py has no `except Exception` (grep count 0). Citations that do not match the code at 0c24f5f: row 4 `summary_trim.trim ... :391` (def trim is at summary_trim.py:379); row 13 `store.py:69` (the tray-flag skip is at store.py:74; :69 is `ents.append(d)`); row 11 `_other_person ... applied at :101, :138, :155, :166, :169` (calls are at conflict_candidates.py:99, 136, 153, 164, 167) and `plan_vs_outcome :133-148` / `history_denials :151-175` (defs start at :131 and :149).",
      "why_it_matters": "The doc's own last line: 'The table must match the code; a reviewer who finds a difference has found a defect.' A stale 'known limitation' understates a fix (T-073) and wrong line numbers send a reader to unrelated lines.",
      "fix": "Delete or rewrite the 'Known limitation (judge errors)' bullet to describe judge_guard; replace line numbers with function names, or regenerate them.",
      "acceptance_test": "A small unit test that every `file.py:NNN` citation in docs/LLM_VS_CODE.md names a line that contains the cited symbol, or the citations are function names only."
    },
    {
      "severity": "minor",
      "title": "Two broad `except Exception` fallbacks and sleep-polling tests",
      "evidence": "app/backend/store.py:24 and app/backend/language.py:323 `try: body = ingest.split_records(block)[0][\"excerpt\"] except Exception: body = block` swallow any error from the splitter and fall back to the whole block for display and language routing (no log, no state). Tests poll a background thread with `time.sleep(0.25)` in loops of up to 240-480 iterations: tests/unit/test_trace.py:37, tests/unit/test_t116_gap_endpoints.py:226 (wall-clock dependent, pass/fail depends on the machine).",
      "why_it_matters": "Checklist 12 and 14. The fallback is benign today (display text only) but would hide a splitter bug; the polling loops can flake under load.",
      "fix": "Narrow the except to the splitter's expected errors and let others propagate; replace the polling with a join on the run thread or an injected clock.",
      "acceptance_test": "A test where split_records raises TypeError on a block and load_records/block_lang propagates; the status tests complete without time.sleep."
    }
  ],
  "whats_right": [
    "Deterministic core is code with sharp tests: money is integer cents, gap uses date objects with 28/29/30/31/73 cases, and all five mutants I applied (grounding, gap threshold, rate totaled, dismissed export, judge ignored) were killed.",
    "audited_call is exactly the contract: 3 attempts max, each retry changes the request, one audit row per attempt, 120 s timeout, programmer errors propagate instead of being retried, fixture miss is final and visible.",
    "The export gate (D-044) held under my failure probe: accepted-but-unjudged items produced JUDGE_NOT_RUN blockers plus RUN_FAILED, and narrative sentences fail closed on any judge answer other than supported."
  ],
  "questions_for_chris": []
}
```
