# T-037 round 2: staff-engineer-reviewer

Verdict: pass (0 blockers, 0 majors, 2 minors). All four round-1 findings are resolved. Two new minors are noted. One is the lib01 failure that the worker already disclosed.

Pinned commit: fa8a36e (the HEAD observed at 20:32 local time, after 31070c3, bee1844 and d6ea199). HEAD moved during the review (636a042, then fa8a36e). The working tree also had 4 fixture JSONs under tests/fixtures/llm modified by another agent's live recording (`recorded_at` 02:31:29 and 02:31:35). So I ran every check twice, once in the live tree and once in a `git archive fa8a36e` snapshot in the scratchpad (532 fixture files, same as the tree). The snapshot results are the ones I rely on.

## Exercised
- `.venv/bin/python -m pytest -q tests/unit`: 895 passed, 0 skipped. Same result in the live tree and in the fa8a36e snapshot.
- `.venv/bin/python tests/fixtures/make_curated.py --check`: exit 0 ("entries: 9 non-verified: []", "letter equal: True | notes equal: True").
- `.venv/bin/python -m evals.run` (fixture backend), live tree and snapshot. The headline metrics match `evals/reports/20261102T023039Z.md` line for line: grounding 1.000 (236 checked), entry_recall 0.982, amount_recall 1.000, all four flag types 1.000/1.000, hallucination catch 40/40 with 0 judge unavailable, controls 0 of 10, must_not 0, unsplit_paste True, case_07_total_420 True. `diff` of the two reports (header line removed) is empty. ship_bar_met is False with blockers `4_no_invented_facts` and the live-only determinism/unsupported_3run. I confirmed in `evals/run.py:510` and in latest.json that bar 4 fails only because `unsupported_count_3run` and `determinism_3run` are unmeasured on the fixture backend. The hallucination, controls and judge-unavailable sub-conditions are all clean.
- `python -m app.pipeline evals/golden/sample.txt` in the snapshot, twice. Exit 0 both times, stdout byte-identical (`cmp`), stderr 0 bytes. Output shows 9 entries (all `[verified]`), "Gap of 73 days" `[verified]`, "$8,390.00" detected and not a total, 10 flags.
- A per-case replay on the fixture backend, with a probe script in the scratchpad. All ten golden inputs have 0 failed model calls, and the test `test_replay_has_no_fixture_miss` passes for all ten.
- A replay of the seven `evals/library` packets: lib02 to lib07 are clean. lib01 is `done_with_errors` (see finding 1).
- A replay of `evals/golden/unsplit_paste.txt` with `LLM_FIXTURE_DIR=tests/fixtures/llm/split` (see finding 2).
- Scratch-copy mutation of `app/backend/pipeline.py` and of the fixture dir (`mut.py` in the scratchpad), running test_pipeline.py and test_t037_backend.py:

| Mutant | Round 1 | Round 2 |
|---|---|---|
| Remove the record_warning dedupe (`fs = [f for f in fs if f["type"] != "record_warning"]`) | not caught (44 passed) | caught (1 failed) |
| Disable the per-record `expired()` check inside the flags stage | not tested | caught (1 failed) |
| Delete one sample extract fixture | stale fixtures went unnoticed | caught (1 failed) |
| Delete one judge fixture | not tested | caught (1 failed) |

- Read the diff 81df4e0..fa8a36e for `app/backend/pipeline.py`, `app/llm/audited.py`, `app/llm/provider.py` and `app/llm/record.py`, and the new tests in `tests/unit/test_t037_backend.py`. Grepped those files for bare `except:`, `except Exception: pass`, `float(` and `sleep(`: the only hit is `audited.py:91`, a capped code-controlled retry delay. Grepped tests/fixtures for `sk-ant`, `ANTHROPIC_API_KEY=` and private-key headers: no hits.

## Round-1 findings, status
1. **Blocker, stale fixtures (sample 21 misses, case_01 11 misses): resolved.** Commit 31070c3 re-recorded the fixtures. Sample and case_01 now make 0 failed calls (replay probe and 10 parametrized tests). The CLI prints all 9 entries `[verified]` with an empty stderr.
2. **Major, vacuous `test_replay_has_no_fixture_miss`: resolved.** The test at `tests/unit/test_t037_backend.py:41-52` now asserts no `llm_calls` row has an error. It also asserts no FIXTURE_MISS or JUDGE_UNAVAILABLE reason on any item, and that `out["errors"] == []`. Deleting one fixture makes it fail.
3. **Major, injection dedupe untested: resolved.** `test_injection_record_gets_exactly_one_record_warning` (case_07 gives `[["r3"]]`) fails when the filter at `pipeline.py:299` is removed.
4. **Minor, deadline checked only between stages: resolved.** `pipeline.py:290` and `:296` check `expired()` per record. `test_deadline_applies_inside_the_flags_stage` fails when the check is disabled.

## New findings
Both are minor. Neither blocks the card.

1. **Minor (carried): case_lib01 record 3 fails extract live and on the fixture replay.** The extract reply contains two JSON objects, so INVALID_JSON, then LLM_FAILED_AFTER_RETRIES. The library packet replays as `done_with_errors`. The failure is visible, not a silent default, and the backend disclosed it in the 02:31:06Z note and offered the `extract_v1` fix. But no unit test replays the library packets, so lib02 to lib07 are unguarded against the next prompt change, and lib01 would go red as soon as one was added. The product already shows the error, so I did not rate it higher. It is T-053's packet, but the root cause (the extract prompt allowing a reply with prose and two objects) sits in T-037's recorded-fixture scope.
2. **Minor: `unsplit_paste` scores True while its pipeline run mostly fails, and every eval run logs 7 "llm call failed" lines.** `evals/run.py:295-332` points `LLM_FIXTURE_DIR` at `tests/fixtures/llm/split`, which holds one file (the split reply). Running that input gives status `done_with_errors`, 0 entries, 3 extract errors with `cause: FIXTURE_MISS`, and `CONFLICT_PASS_INCOMPLETE`. The metric only checks the record count, dates, sources and LLM_SPLIT warnings, so True is correct for what it claims (R-IN-1). The cost is that every `python -m evals.run` prints 7 `llm call failed` lines (3 extract, 3 flags, 1 conflicts) that look like the failure round 1 was about, and someone triaging stderr cannot tell them from real misses.

## Hygiene note
My two `python -m evals.run` runs in the live tree wrote four new untracked report files and rewrote the tracked `evals/reports/latest.json`. I could not delete them because the reviewer hook blocks writes outside `reviews/`. The metrics are identical to the committed report. The orchestrator can remove the untracked `evals/reports/20261102T0231*.md` and `20261102T02320*.md` files and `git checkout evals/reports/latest.json`.

```json
{"card": "T-037", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2; pinned fa8a36e (git archive snapshot in scratchpad plus live tree); commits 31070c3, d6ea199, bee1844 since round 1; app/backend/pipeline.py, app/llm/audited.py, app/llm/provider.py, app/llm/record.py, tests/unit/test_t037_backend.py, tests/unit/test_pipeline.py, tests/fixtures/llm, evals/run.py; CLI on evals/golden/sample.txt (fixture backend)",
 "exercised": ["pytest -q tests/unit: 895 passed, 0 skipped (live tree and fa8a36e snapshot)", "tests/fixtures/make_curated.py --check: exit 0", "python -m evals.run on fixture backend in live tree and snapshot: headline metrics identical to evals/reports/20261102T023039Z.md; ship_bar_met False only for live-only 3-run metrics", "python -m app.pipeline evals/golden/sample.txt x2 in snapshot: exit 0, stdout byte-identical, stderr empty, 9 verified entries, 73-day gap, $8,390.00", "probe replay of all 10 golden inputs on fixture backend: 0 failed calls", "probe replay of 7 evals/library packets: lib02..07 clean, lib01 record 3 LLM_FAILED_AFTER_RETRIES", "probe replay of unsplit_paste with LLM_FIXTURE_DIR=tests/fixtures/llm/split: done_with_errors, 0 entries, 3 extract FIXTURE_MISS", "scratch-copy mutation: dedupe removal, flags-stage deadline check, delete one extract fixture, delete one judge fixture - all caught", "read diff 81df4e0..fa8a36e of pipeline.py, audited.py, provider.py, record.py and test_t037_backend.py; grep for bare except, float(, sleep(, secrets in fixtures"],
 "verdict": "pass",
 "scores": {"llm_vs_code_separation": 4, "failure_visibility": 4, "test_strength": 4, "determinism_and_fixtures": 4, "stage_and_status_contract": 4},
 "findings": [
  {"severity": "minor", "title": "Carried: case_lib01 record 3 extract fails (INVALID_JSON, two JSON objects) and no test replays the library packets",
   "evidence": "Probe replay of evals/library/case_lib01_er_only_then_gap.txt on fixture backend: status done_with_errors, errors [LLM_FAILED_AFTER_RETRIES record 3]; lib02..07 status done with no errors. grep -rn 'evals/library|case_lib' tests/unit/*.py returns nothing. Backend note 02:31:06Z discloses the failure and the extract_v1 hardening is 'not done, say if wanted'.",
   "why_it_matters": "The failure is visible (not a silent default), but a demo packet shows an error and lib02..07 are unprotected against the next prompt change; the extract prompt tolerating a reply with two JSON objects is a reliability gap in the recorded-fixture work.",
   "fix": "Harden extract_v1 ('your whole reply is one JSON object'), re-record, and add library packets to the replay parametrization of test_replay_has_no_fixture_miss.",
   "acceptance_test": "test_replay_has_no_fixture_miss is parametrized over evals/library/*.txt and passes for all seven; deleting one library fixture makes it fail."},
  {"severity": "minor", "title": "unsplit_paste scores True while its pipeline run has 3 extract fixture misses; every eval run logs 7 'llm call failed' lines",
   "evidence": "evals/run.py:295-332 sets LLM_FIXTURE_DIR to tests/fixtures/llm/split (1 file). Replay: status done_with_errors, entries 0, errors [extract record 1, 2, 3: FIXTURE_MISS, CONFLICT_PASS_INCOMPLETE]. `python -m evals.run 2>&1 >/dev/null | grep 'llm call failed'` gives 7 lines (3 extract, 3 flags, 1 conflicts).",
   "why_it_matters": "The metric is correctly scoped to the split stage, but the expected failures are logged exactly like real fixture misses, so a reader of stderr cannot tell round-1-style staleness from the known split-only packet.",
   "fix": "Either record the downstream calls for unsplit_paste into the split fixture dir, or have score_unsplit state in the report that downstream stages are intentionally unfixtured and silence or label those log lines.",
   "acceptance_test": "`python -m evals.run` on the fixture backend prints 0 'llm call failed' lines, or the report contains a line stating the 7 expected misses for unsplit_paste."}
 ],
 "whats_right": ["test_replay_has_no_fixture_miss now counts failed llm_calls rows and reason codes, and fails when a fixture file is deleted", "Fixtures are committed, the CLI is byte-identical across runs with empty stderr, and the eval headline reproduces exactly from the report", "Every round-1 gap (dedupe, per-record deadline) now has a test that a scratch mutant breaks"],
 "questions_for_chris": []}
```
