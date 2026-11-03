# T-146 staff-engineer review, round 2 (2db6ad2, tested on a `git archive` of 2db6ad2)

Verdict: **changes** (0 blockers, 2 majors, 2 minors, 1 nit).

The round-1 case is fixed. On the archive I completed the sample (9 entries, 4 amounts, 10 flags), accepted e1, dismissed e2, accepted a1, then re-ran with the extract step raising `LLMFailed`: case `failed`, error `run_partial` "The AI step failed for 9 items (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged...", e1 still `verified`/`accepted` with its summary and quote, and a full-row compare of all 23 stored items differs only in `ladder.*.call_id` on amounts/flags that were re-judged. Judge-down (j1/j2, or all four judges) keeps all 23 rows byte-identical and reads `failed/run_partial` "...12 items (the second check)". A deadline at extract, verify, judge_entries, amounts, conflicts and flags keeps all rows identical (`run_deadline`). The judge wording is right in all three cases: called-and-failed says "The second check failed", a deadline keeps `JUDGE_NOT_RUN:`, and a fixture miss keeps `JUDGE_NOT_RUN:` plus the demo sentence.

Two re-run paths still overwrite stored work without an error, and both are inside the orchestrator's rule ("No re-run may overwrite a decided item or an item with stored output with an empty or partial stub", "undo a second-check answer", "delete flags", "failed flag step"). See F1 and F2.

What I ran (archive of 2db6ad2, project `.venv/bin/python -I`):
- `pytest tests/unit -q -p no:cacheprovider`: **3893 passed, 8 skipped** in 441 s, no failures (the handoff's 2 flaky and 4 failing tests did not reproduce on the committed tree).
- Probe scripts (kept outside the archive, in the scratchpad `t146r2/probes/`): complete run, accept e1, dismiss e2, accept a1, then re-run with extract down, j1+j2 down, all four judges down, flags down, conflicts down, deadline at six stages, and one record failing at extract (LLMFailed, FixtureMiss, schema-invalid, summary-not-in-quote); each compared on full stored rows (every column but `updated_at`), case status/error, and `trace.export_blockers`.
- Wording probe: j1 down, j2 down, deadline, and j1 FixtureMiss, read through `present.item_view(...)["why"]`.
- 16 mutants of `pipeline.py`, `why.py`, `present.py`, `flags.py` on a scratch copy, run against the three T-145/T-146 test files and, for survivors, 5 more related files (189 tests).

Mutants killed: `_degrades` always None, judge arm off, prune ignored, entry_id backfill off, case status failed only on timeout, `run_partial` never set, FIXTURE_MISS exclusion dropped from `why.join`, `judge_failed` ignoring the NOT_RUN code, `present._why` ignoring the judge. Survived: see F3.

```json
{
  "card": "T-146",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit 2db6ad2 (app/backend/pipeline.py _degrades/_persist/_noting/run_partial, why.py, present.py, flags.py, tests/unit/test_t146_r2_failed_rerun_keeps_items.py); git archive of 2db6ad2 (HEAD later moved to 611bdcc, pipeline.py _persist and run_pipeline unchanged by it); fixture backend; sample case evals/golden/sample.txt",
  "exercised": [
    "read reviews/T-146-staff-engineer.md, python3 tools/board.py show T-146 (orchestrator note and handoff), git show 2db6ad2",
    "git archive 2db6ad2 into a scratch dir; pytest tests/unit -q -p no:cacheprovider: 3893 passed, 8 skipped",
    "round-1 repro: complete run, accept e1, dismiss e2, accept a1, re-run with extract raising LLMFailed: case failed/run_partial naming 9 items and 'writing the entries', e1 verified+accepted, full-row compare of 9 entries, 4 amounts, 10 flags (only ladder call ids of re-judged amounts/flags differ)",
    "re-run probes with full-row compare: j1+j2 down, all four judges down, flags step down, conflicts step down, deadline at extract/verify/judge_entries/amounts/conflicts/flags",
    "per-record probes at e1: extract LLMFailed, FixtureMiss, schema-invalid summary, SUMMARY_NOT_IN_QUOTE; j1 failing for record 1 only",
    "model flag that agrees with lexicon flag f_r3_1 (state lexicon+llm, verified), accept it, re-run with the flags step down",
    "export gate and letter: trace.export_blockers, present.review_view counts and store.export_case after the SUMMARY_NOT_IN_QUOTE re-run",
    "judge wording via present.item_view: j1 failed, j2 failed, deadline, j1 FixtureMiss",
    "16 mutants on a scratch copy (killed 9: no-protect, judge arm, prune, entry_id backfill, status, run_partial error, join FIXTURE_MISS, judge_failed NOT_RUN code, present._why; survived 7: count, flags label, stored flag why, _noting FixtureMiss, conflicts prune guard, two stub-reason set members)",
    "git show 2db6ad2 diff read in full; git log 2db6ad2..HEAD and git diff 2db6ad2 HEAD on pipeline.py/why.py/present.py/flags.py"
  ],
  "verdict": "changes",
  "scores": {
    "timeout_rerun_keeps_items_and_decisions": 5,
    "errored_rerun_keeps_stored_rows_whole": 3,
    "case_shows_honest_error_with_count_and_step": 3,
    "judge_wording_matches_cause": 5,
    "test_quality_mutation_sensitivity": 3
  },
  "findings": [
    {
      "severity": "major",
      "title": "A re-run with the flag step down downgrades an accepted, verified flag to needs_review / LLM_FAILED_AFTER_RETRIES, drops its second-check answer and AI origin, and reports run status 'done', case 'ready', error None",
      "evidence": "Repro on the archive (probe p4): fixture backend, model flag for record 3 with the same quote as lexicon flag f_r3_1 -> complete run stores `f_r3_1 verified [] lexicon+llm`; `DB.apply_review(conn,'f_r3_1','accept')`; `PL.run_pipeline(..., call=FakeCall(sample_script(flags=AU.LLMFailed('flags down', last_error='TIMEOUT'))), now=lambda: 3.0)` -> out status `done`, `out['errors'] == []`, case `ready`, `error None`; `f_r3_1` now `needs_review ['LLM_FAILED_AFTER_RETRIES'] lexicon accepted`; diff of stored rows: `flag f_r3_1 CHANGED ['origin','state','state_reasons','ladder']`. Without any model flag the same re-run rewrites the reasons of 7 stored flags (f_r3_1, f_r6_1, f_r7_1, f_r7_2, f_r8_1, f_r8_2, f_r9_1) from `LEXICON_ONLY` to `LLM_FAILED_AFTER_RETRIES`, including f_r3_1 after it was accepted (case still `ready`, error None). Cause: `_degrades` (pipeline.py:243-251) protects a flag only when the NEW row's judge verdict is `unavailable`; a flag made while the flag step failed has no judge record at all (lexicon fallback), so nothing is kept. `failed_steps` already contains 'flags' (pipeline.py:479-480) but is used only for `prune`. The only flag-step test (`test_flag_step_down_rerun_keeps_the_model_flag_it_cannot_rediscover`, test file line 142) uses a model-only flag, which takes the prune path.",
      "why_it_matters": "This is the orchestrator's own list: a failed flag step must not undo a second-check answer or alter stored flags, and an errored re-run must show an honest error naming the count and the step. Here the paralegal's accepted flag loses its AI corroboration (verified -> needs_review, origin lexicon+llm -> lexicon, judge answer erased from the ladder) and nothing at case level says the flag step failed. Not a blocker: no fact is invented, the quote and the accept decision survive, and a good re-run restores it.",
      "fix": "Treat a flag row made while the flag step failed (its reasons contain LLM_FAILED_AFTER_RETRIES and the stored row's do not, or `failed_steps` contains 'flags') as degraded when a stored row exists: keep the stored row whole and count it under 'finding the flags', so the case reads failed/run_partial with the count. Extend the flag-step test to the corroborated lexicon+llm flag, an accepted lexicon-only flag, and assert full-row equality.",
      "acceptance_test": "Complete run with a model flag agreeing with f_r3_1, accept it, re-run with flags down: assert full stored rows of all flags equal (no_ladder allowed only for call ids), f_r3_1 still `verified`/`lexicon+llm`/`accepted`, case `failed`, error `run_partial` naming the count and 'finding the flags'. Mutation: removing the new keep rule fails it."
    },
    {
      "severity": "major",
      "title": "A re-run whose extract answer fails the summary-in-quote check replaces an accepted entry with an empty rejected stub, with case 'ready', error None, and a passing export gate",
      "evidence": "Repro on the archive (probe p6): complete run, accept e1, re-run with extract returning `{'summary': 'Patient had a skull fracture of 99 cm.', 'excerpt': <e1's real quote>}` for record 1 -> out status `done`, case `ready`, error None; `DB.get_item(conn,'e1')` = `{summary: None, excerpt: None, state: 'rejected', state_reasons: ['SUMMARY_NOT_IN_QUOTE'], review_status: 'accepted'}`; stored-row diff `entry e1 CHANGED ['summary','excerpt','excerpt_start','excerpt_end','state','state_reasons','ladder']`; `trace.export_blockers` = `[]`; `present.review_view` counts `accepted: 1` (the empty stub itself, so NOTHING_ACCEPTED does not fire); the exported entry list is e2..e9 with e1 absent. `_STUB_REASONS` (pipeline.py:240) lists LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS and SCHEMA_INVALID only; the handoff states this under 'Left: SUMMARY_NOT_IN_QUOTE (model answered) still replaces', and no test covers it. Control: the same re-run with LLMFailed, FixtureMiss or an invalid schema for record 1 keeps e1 whole (`failed/run_partial`, 1 item).",
      "why_it_matters": "The orchestrator's rule has no exception for 'the model answered': the next run of a non-deterministic summarizer can erase an accepted entry, and the paralegal gets a green gate and a letter missing a paragraph she accepted, with no error anywhere. A declared gap in the handoff is still a gap against the rule. Rated major (recoverable by a re-run, the record text survives, the stub is visible in the tray) rather than blocker, consistent with round 1.",
      "fix": "Either include SUMMARY_NOT_IN_QUOTE (and any extract-stage rejection) in the keep-whole rule for rows that have a stored summary and quote, with the same run_partial message, or keep the new row only as a tray attempt while the accepted/decided entry stays in the timeline; add the case to the tests. If Chris wants D-054 to win (the new answer replaces), record that as a decision and make the gate fail on an accepted item with no summary.",
      "acceptance_test": "Unit test: complete run, accept e1, re-run with an unsupported summary for record 1; assert e1's full stored row is unchanged and the case is failed/run_partial naming 1 item (or, under the alternative, that an accepted empty stub blocks the export). Mutation: dropping SUMMARY_NOT_IN_QUOTE from the keep set fails it."
    },
    {
      "severity": "minor",
      "title": "Seven mutants survive: the message count, the flag-step label, the stub-reason set, the FixtureMiss path and the conflicts guard are not pinned",
      "evidence": "Scratch copy of the archive, narrow (3 files, 27 tests) and wide (8 files, 189 tests) both green for: (M8) message count uses `len(kept_e)` instead of `kept_n`: judge-down would read '9 items' instead of 12 (test line 86 only checks 'second'/'kept'); (M9) label 'finding the flags' changed to 'the second check'; (M13) `flags.py:45` back to the old `why.why(c)` join; (M14) `_noting` catching only `AU.LLMFailed` (no FixtureMiss); (M15) prune guard drops 'conflicts'; (M16) SCHEMA_INVALID removed from `_STUB_REASONS`; (M17) FIXTURE_MISS removed from `_STUB_REASONS` (tests only exercise LLM_FAILED_AFTER_RETRIES for the stub rule). Killed: 9 others (listed above).",
      "why_it_matters": "Checklist 13: tests assert behaviour. The headline behaviour is covered, but the count and step the orchestrator asked the message to name, and two of the three stub causes, can regress unseen.",
      "fix": "Assert the exact count and step in each message test (extract-down: '9 items' and 'writing the entries'; judge-down: the stored-row count and 'the second check'; flag-down: 'finding the flags'); add one parametrized test over the three stub reasons (LLMFailed, FixtureMiss, schema-invalid) and one with conflicts down.",
      "acceptance_test": "M8, M9, M14, M15, M16 and M17 each fail the strengthened tests; M13 fails if a test reads the stored flag `why` after a judge-failed run."
    },
    {
      "severity": "minor",
      "title": "A re-run that ends with errors but has no stored output to keep still reads 'ready' with error None; the new messages never fire",
      "evidence": "tests/unit/test_t146_r2_failed_rerun_keeps_items.py:90 `test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial` asserts `err is None and c['status'] == 'ready'` after `done_with_errors`; pipeline.py:489 sets `run_partial` only `if kept_n:`. Same for a second extract-down run on top of a first one (stored rows already stubs, nothing to keep) and for the flags-down run in F1 (`out['errors'] == []`). The handoff lists the first-run case under 'Left'.",
      "why_it_matters": "The orchestrator asked for an honest error on any errored re-run naming the count and the step; today the case-level message depends on there being something to protect, so a stub-on-stub re-run says nothing. The tray shows the failed records, so this is not data loss.",
      "fix": "When `errors` is non-empty or a step in `failed_steps` failed, set the case error (code run_partial or a sibling) with the count of items that have no output and the step name, whether or not anything was kept.",
      "acceptance_test": "Second consecutive extract-down run on the sample: case failed, error names 9 items and 'writing the entries'; first run still stores stubs. Mutation: restoring `if kept_n:` fails it."
    },
    {
      "severity": "nit",
      "title": "Commit 2db6ad2 carries a D-059 hunk that belongs to the T-140 card",
      "evidence": "pipeline.py:326 in 2db6ad2: `**({\"confirm\": a[\"confirm\"]} if a.get(\"confirm\") else {})}      # D-059: the flag the paralegal must confirm by name`; `amount_item` only starts setting `confirm` in a0e2639 (git diff 2db6ad2 HEAD -- app/backend/pipeline.py), so the hunk is dead code inside this commit.",
      "why_it_matters": "Reviewers of T-146 cannot tell this hunk from the fix, and a revert of T-146 would pull a T-140 piece with it (the shared index is a known hazard in this repo).",
      "fix": "Stage by hunk (`git add -p` is unavailable here, so split the file edit) or note it in the card handoff.",
      "acceptance_test": "git show --stat of the fix commit lists only T-146 hunks."
    }
  ],
  "whats_right": [
    "run_partial keeps the full stored row (summary, quote, offsets, ladder, state, review status) for failed extract, one failed record, all-judges-down, and a single failed j1, and the case reads failed with the count and the step named in the message.",
    "The judge wording follows the judge record: called-and-failed says 'The second check failed' (reason code JUDGE_UNAVAILABLE unchanged), while deadline and fixture-miss keep the JUDGE_NOT_RUN sentence, and the choice is made in one place (why.why/join) with the mutants killed.",
    "The deadline path stays additive at all six stages with identical rows, and a later good re-run clears the error and the accepted decision stands."
  ],
  "questions_for_chris": []
}
```
