# T-146 staff-engineer review (7d3ca35, tested on a `git archive` of 7d3ca35)

Verdict: **changes** (0 blockers, 1 major, 1 minor).

The timed-out re-run is fixed as the card says. On a `git archive HEAD` copy (HEAD 7d3ca35 at archive time; `pipeline.py` unchanged since) I completed the sample (9 entries, 4 amounts, 10 flags on the fixture backend), accepted e1, dismissed e2, accepted a1, then re-ran with an injected clock that passes the 480 s deadline when a named stage starts. For `extract`, `amounts` and `conflicts` (plus the `verify`, `judge_entries`, `flags` and mid-flags cases in the card's own tests), case status is `failed`, error `run_deadline`, and entries 9/9, amounts 4/4, flags 10/10 keep identical `(review_status, state, state_reasons)`: nothing deleted, nothing downgraded, the decisions stand. A first-ever run that times out still stores what finished. The message now reads "every item from earlier runs and every decision of yours was kept unchanged", which is true for that path (and `app/frontend/input.js:75` shows it after "Your records are kept and finished items are saved").

The AC also says "or failed re-run". A re-run where the AI step fails (not a deadline) still loses accepted work. See F1.

What I ran, on the archive with the project `.venv/bin/python`:
- `pytest tests/unit -q -p no:cacheprovider`: **3668 passed, 8 skipped**, no failures. The two new files: 11 passed.
- Timed-out re-run probes at `extract`, `amounts`, `conflicts` (before/after compare of state and reasons for entries, amounts, flags with decisions made); timed-out run then full re-run (accept kept, gate clears); extract-down re-run; judge-down re-run.
- Mutants of `_persist` and its callers on a second scratch copy, each restored: entries persisted non-additive (2 fail), amounts non-additive (3 fail), flags non-additive (5 fail), drop the `continue` that skips existing ids (3 fail), drop the early `return` that skips the stale-delete (5 fail), additive branch overwrites ladder and excerpt (5 fail). **Survived:** (a) message reverted to "finished items were kept" (11 pass), (b) additive branch sets an existing entry's `summary` to NULL (11 pass). See F2.
- Greps for `done_with_errors` and `finished items` across `app/`, and the other places that write case `status="failed"`.

```json
{
  "card": "T-146",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit 7d3ca35 (app/backend/pipeline.py _persist additive mode and the run_deadline message, tests/unit/test_t146_rerun_keeps_items.py); git archive of 7d3ca35; fixture backend; sample case evals/golden/sample.txt",
  "exercised": [
    "read GATE-M2-staff-engineer.md F2, python3 tools/board.py show T-145 and T-146, git show 7d3ca35",
    "git archive HEAD (7d3ca35) into a scratch dir; pytest tests/unit -q -p no:cacheprovider: 3668 passed, 8 skipped",
    "re-run probes: complete run, accept e1, dismiss e2, accept a1, then re-run with a deadline at extract, amounts, conflicts: item counts and (review_status, state, reasons) identical for entries, amounts, flags; case failed/run_deadline",
    "timed-out first run then full re-run: accept kept, state verified, gate clears",
    "extract-down re-run (extract raises LLMFailed) and judge-down re-run (j1/j2 raise LLMFailed): before/after compare, DB.get_item('e1'), case status and error, trace.export_blockers",
    "seven mutants of _persist/run_pipeline (entries, amounts, flags non-additive; continue dropped; early return dropped; ladder overwrite; message revert; summary overwrite): five killed by count, two survived (message text, summary-only overwrite)",
    "grep of done_with_errors, 'finished items', status=\"failed\" writers in app/backend; read of present/trace RUN_FAILED text and app/frontend/input.js:75"
  ],
  "verdict": "changes",
  "scores": {
    "timeout_rerun_keeps_items_and_decisions": 5,
    "failed_rerun_keeps_accepted_work": 2,
    "message_tells_the_truth": 3,
    "test_quality_mutation_sensitivity": 3,
    "no_silent_data_loss": 3
  },
  "findings": [
    {
      "severity": "major",
      "title": "A failed re-run (AI step down) still overwrites the paralegal's accepted entries with empty failure stubs, and the case reads 'ready' with no error",
      "evidence": "AC 1 of T-146: 'a timed-out or failed re-run keeps every previous item and decision'. Only `timed_out` is made additive (pipeline.py:425-427 `additive=timed_out`); every other status takes the replace path (`DB.update_item(conn, it['id'], **row)`, pipeline.py:244-247 at HEAD). Repro (archive of 7d3ca35, fixture backend): complete run; `DB.apply_review(conn,'e1','accept')`; `PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script(extract=AU.LLMFailed('x', last_error='TIMEOUT'))), now=lambda: 3.0)` -> status `done_with_errors`, case status `ready`, case error `None`; `DB.get_item(conn,'e1')` = `{summary: None, excerpt: None, excerpt_start: None, state: 'rejected', state_reasons: ['LLM_FAILED_AFTER_RETRIES'], review_status: 'accepted', ...}`; before the re-run e1 held the 'Restrained driver rear-ended at approx. 35 mph ...' summary and its verbatim excerpt. Every one of the 9 entries changed this way (verified/pending/dismissed -> rejected). `trace.export_blockers` then returns `[(None, 'NOTHING_ACCEPTED')]`. `done_with_errors` is never stored (grep: only pipeline.py:432 and :570), so no case-level message says the re-run failed. A judge-down re-run (j1/j2 raise) downgrades e1..e9 and a1/a4 from `verified` to `needs_review JUDGE_UNAVAILABLE` while the case is `ready` (that one is visible per item, and recoverable by the rejudge button).",
      "why_it_matters": "This is the same class as the gate finding the card fixes: a normal failure (backend down on the second click of Run) erases an AI summary and quote the paralegal had already accepted, keeps the 'accepted' flag on an empty row, and tells her nothing at case level. The only per-item trace is a 'rejected' state with LLM_FAILED_AFTER_RETRIES. The record text survives, so another run recovers it, which keeps this at major rather than blocker. If Chris reads 'failed' in the AC as case status `failed` only, the AC is met on its narrow reading, but the loss is the same and the card's own handoff ('Surprised: ... the whole persist is additive') shows the intent was to protect earlier results from partial runs.",
      "fix": "When the re-run produces a failure stub for an id that already has a stored row with a summary and excerpt (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, SCHEMA_INVALID at extract), keep the stored row and record the failure on the run (case `error` with a code such as run_partial and a message that names how many records failed), instead of replacing it. Do the same for judge-down: do not downgrade a stored judged state on a run whose judge call failed, or at least store a case-level error. Alternatively split this into a new card and change the T-146 AC to say 'timed-out'.",
      "acceptance_test": "Unit test: complete run, accept e1, re-run with extract raising LLMFailed; assert e1 still has its summary, excerpt, state and 'accepted', and the case has an error naming the failed re-run. Add the judge-down variant asserting no verified item is downgraded without a stored error. Mutation: replacing the keep-old rule with the current replace makes it fail."
    },
    {
      "severity": "minor",
      "title": "The tests do not pin the message the card changed, and compare only review_status/state/reasons, so a summary-only overwrite and the old message both pass",
      "evidence": "tests/unit/test_t146_rerun_keeps_items.py:34-35 `_snapshot` returns `(review_status, state, state_reasons)` per item; the only message assertion is `json.loads(c['error'])['code'] == 'run_deadline'` (line 47). Mutant (a): replace the new message text with the old 'finished items were kept' -> `11 passed`. Mutant (b): in `_persist`, `if additive and old is not None: if kind == 'entry': DB.update_item(conn, it['id'], now=now, case=cid, summary=None); continue` -> `11 passed`. The card's AC half 'the message tells the truth' therefore has no test that fails when the message changes, and a regression that wipes summary, excerpt, date or computed numbers while leaving state alone is invisible.",
      "why_it_matters": "Checklist 13: tests assert behaviour, and at least one must fail when the guarded behaviour is removed. The fix is correct today, but the safety net covers the three state fields, not the content a paralegal accepted.",
      "fix": "Snapshot the full stored row (summary, excerpt, date_iso, record_ids, computed, ladder judge verdict) and assert equality; assert the message text, or better, that it contains 'earlier' and 'kept' and does not contain 'finished items'.",
      "acceptance_test": "Both mutants above fail the strengthened tests; the existing six still pass."
    }
  ],
  "whats_right": [
    "The additive persist is the right design: a timed-out run neither deletes, downgrades nor overwrites, so pending items, judged states, flags and the paralegal's decisions are identical before and after at every stage I tried (extract, amounts, conflicts, plus the card's verify, judge_entries, flags, mid-flags).",
    "Five of seven mutants (three kinds non-additive, dropped continue, dropped early return, ladder overwrite) are killed by the count and state snapshots, and a first-ever timed-out run still stores what finished.",
    "A timed-out run followed by a full re-run recovers cleanly: the accepted e1 stays accepted and becomes verified, and the export gate clears."
  ],
  "questions_for_chris": [
    "Does 'failed re-run' in T-146 AC 1 mean only a case that ends status failed (deadline, unsupported language, crash), or any re-run where the AI step fails (done_with_errors)? F1 assumes the second reading; if the first, move F1 to its own card."
  ]
}
```
