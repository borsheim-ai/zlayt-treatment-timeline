# T-145 staff-engineer review (b604ff2, tested on a `git archive` of 7d3ca35)

Verdict: **pass** (0 blockers, 0 majors, 1 minor, 1 nit).

The gate blocker is fixed on the deadline path. I reproduced the gate reviewer's repro on a `git archive HEAD` copy (HEAD was 7d3ca35 when I took it; `app/backend/pipeline.py` is unchanged since, later commits touched `why.py` and `generator.py` for T-139/T-140). Injected clock jumps past 480 s when the `verify` stage starts, fixture backend, sample case:

- `run_pipeline` returns `status timeout`, `run_deadline`. All nine entries are `needs_review`, `state_reasons ['JUDGE_UNAVAILABLE']`, `ladder.judge = {verdict: unavailable, reason_code: JUDGE_NOT_RUN, model: None, prompt_version: None, call_id: None}`.
- Why line (via `present._common`): "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked." The word "agreed" appears nowhere.
- `case_extras.apply_batch(accept, all nine)` raises `BatchRefused`, reason `not_verified` x9, all stay pending.
- `trace.export_blockers` returns `[(None,'RUN_FAILED'), ('e1','JUDGE_NOT_RUN')]` after e1 is accepted singly, so the export gate holds. Amounts are `needs_review JUDGE_UNAVAILABLE` (fail closed already).
- Recovery works: `rejudge.rejudge` with a working backend turns the nine entries `verified`/`supported`; a timed-out run followed by a full re-run leaves e1 `accepted`, `verified`, no blockers.

Honesty of the "JUDGE_NOT_RUN:" sentence, and the real-unavailable case: the sentence is true for both cases ("did not run or did not finish"), but the prefix is attached to the shared `JUDGE_UNAVAILABLE` reason code, so a judge that was called and failed after retries now prints it too. Probe: `FakeCall(sample_script(j1=LLMFailed))`, run status `done`, e1 `needs_review ['JUDGE_UNAVAILABLE']`, `ladder.judge = {model: claude-haiku-5-5, prompt_version: judge_faithfulness_v1, reason_code: NONE}`, Why starts "JUDGE_NOT_RUN:". State, reason, Why and the item-trace `judge_1` step (`skipped JUDGE_UNAVAILABLE`) are identical in the two cases; only the audit `ladder.judge` (reason_code JUDGE_NOT_RUN vs NONE, model None vs set) tells them apart. See F1.

What I ran, on the archive with the project `.venv/bin/python`:
- `pytest tests/unit -q -p no:cacheprovider`: **3668 passed, 8 skipped** (no failures; the handoff's "4 failed, git-archive-only" did not occur on my copy). The two new files: 11 passed.
- `LLM_BACKEND=fixture python -m app.pipeline evals/golden/sample.txt` three times: rc 0, identical md5.
- Six mutants of `pipeline.py`/`why.py` on a second scratch copy, each restored (`diff -rq` against the archive clean): remove the `_mark_judge_not_run` call (4 fail), skip the recompose (4 fail), recompose with `judge="supported"` (4 fail), ladder verdict `supported` (2 fail), overwrite real judge verdicts i.e. drop the "has a verdict" skip (1 fail), revert the Why sentence (1 fail). All killed.
- Probes above; grep of the callers of `compose`/`compose_state`.

```json
{
  "card": "T-145",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit b604ff2 (app/backend/pipeline.py _mark_judge_not_run, app/backend/why.py JUDGE_UNAVAILABLE sentence, tests/unit/test_t145_judge_not_run.py); git archive of 7d3ca35; fixture backend; sample case evals/golden/sample.txt",
  "exercised": [
    "read GATE-M2-staff-engineer.md, python3 tools/board.py show T-145 and T-146, git show b604ff2 and 7d3ca35",
    "git archive HEAD (7d3ca35) into a scratch dir; pytest tests/unit -q -p no:cacheprovider: 3668 passed, 8 skipped",
    "deadline repro through run_pipeline with an injected clock (jump at verify): states, ladder.judge, Why text, apply_batch accept, trace.export_blockers, item_trace judge_1, judge_report",
    "real judge failure probe (j1 raises LLMFailed, run status done): state, ladder.judge, Why, item_trace compared with the deadline case",
    "rejudge.rejudge on the deadline case with a working fixture backend: nine entries verified/supported; timed-out run then full re-run keeps e1 accepted and clears the gate",
    "six mutants (call removed, no recompose, judge supported, ladder supported, real verdicts overwritten, Why reverted): all killed by the new tests",
    "python -m app.pipeline evals/golden/sample.txt x3 with LLM_BACKEND=fixture: rc 0, identical output",
    "grep of compose/compose_state callers and JUDGE_NOT_RUN uses across app/, docs/, memory/contracts/"
  ],
  "verdict": "pass",
  "scores": {
    "failure_visibility_no_silent_fallback": 5,
    "deadline_path_fix_correctness": 5,
    "test_quality_mutation_sensitivity": 4,
    "audit_trail_distinguishes_cases": 3,
    "doc_and_contract_match": 3
  },
  "findings": [
    {
      "severity": "minor",
      "title": "The 'JUDGE_NOT_RUN:' prefix is on the shared JUDGE_UNAVAILABLE sentence, so a judge that ran and failed is also labelled 'not run'; state, reason and trace cannot tell the two apart",
      "evidence": "app/backend/why.py:15 `\"JUDGE_UNAVAILABLE\": \"JUDGE_NOT_RUN: the second AI check did not run or did not finish, ...\"`. Repro (archive of 7d3ca35, fixture backend): `PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script(j1=AU.LLMFailed('x', last_error='TIMEOUT'))), now=lambda: 1.0)` -> run status `done`; e1 `needs_review ['JUDGE_UNAVAILABLE']`, ladder.judge `{'model': 'claude-haiku-5-5', 'prompt_version': 'judge_faithfulness_v1', 'call_id': None, 'reason_code': 'NONE', 'verdict': 'unavailable'}`, `present._common(row)['why']` = 'JUDGE_NOT_RUN: the second AI check did not run or did not finish, ...'; `trace.item_trace(..., 'e1')` judge_1 step `('judge_1', 'skipped', 'JUDGE_UNAVAILABLE')`, the same as in the deadline case. The same token is also the export-gate blocker code `JUDGE_NOT_RUN` (trace.py:851), which means 'accepted item with no judge answer'.",
      "why_it_matters": "Honest failure and debuggability: the judge was called (model haiku, three audited attempts) in one case and never called in the other, but the paralegal-facing line and every state field say the same thing, and an internal code token appears inside a sentence. Whoever debugs 'why did this say NOT_RUN' has to open ladder.judge to learn whether a model was ever invoked. The sentence itself stays true ('did not run or did not finish'), so this is a labelling and audit-clarity defect, not a fail-open; export and batch accept hold in both cases.",
      "fix": "Choose the Why sentence from `ladder.judge.reason_code` (JUDGE_NOT_RUN: 'The second AI check never ran because the run stopped at its time limit.'; NONE/unavailable after a call: 'The second AI check was called and gave no answer.'), or put the distinction in the item trace `judge_1` step detail. Keep the closed reason list unchanged, as the card intends. Leave the raw token out of the sentence the paralegal reads.",
      "acceptance_test": "Unit test: the deadline case Why mentions the time limit and not 'gave no answer'; the LLMFailed case Why says the check was called and gave no answer and does not contain 'JUDGE_NOT_RUN'; the item trace judge_1 step differs between the two. Mutation: restoring the shared sentence fails the second assertion."
    },
    {
      "severity": "nit",
      "title": "The fix is a call-site patch; compose still treats a missing judge as 'nothing to doubt', and the contract/doc do not mention the new ladder value",
      "evidence": "app/backend/confidence.py:62 `_lookup(_JUDGE, ladder.get('judge'), none_ok=('supported',))` and app/backend/generator.py:123-127 pass `st.get('judge')` (None) unchanged; `_mark_judge_not_run` (pipeline.py:221-229) is the only place that closes it, once, for run_pipeline's entries. The handoff says 'api.md note not written'; `grep -rn JUDGE_NOT_RUN memory/contracts/api.md docs/LLM_VS_CODE.md` shows no mention of `ladder.judge.reason_code: JUDGE_NOT_RUN` (model/prompt_version/call_id null) or of the deadline behaviour.",
      "why_it_matters": "Any new caller of compose that forgets the judge step silently produces 'verified' again, which is the class of defect that was the gate blocker. The ladder.judge shape a front end or auditor reads is undocumented. Optional hardening, not a spec violation today (every current caller is covered: amounts fail closed, flags are judged inside their stage).",
      "fix": "Optional: make compose_state require an explicit `judge` key for LLM-origin items (value or a sentinel for code-only items), as suggested in the gate review. Add two lines to memory/contracts/api.md for the null model/prompt_version/call_id and reason_code JUDGE_NOT_RUN.",
      "acceptance_test": "Unit test that compose on an LLM-origin entry with no judge key raises, or that run_pipeline's states equal the explicit-unavailable states; api.md contains the reason_code."
    }
  ],
  "whats_right": [
    "The fix closes the fail-open at the one place that matters and keeps the closed reason list: deadline before judge 1 gives needs_review, a Why with no 'agreed', batch accept refuses nine of nine, and the export gate blocks (verified by running it, not just by the tests).",
    "Six mutants of the fix (call removed, no recompose, judge supported, ladder supported, real verdicts overwritten, sentence reverted) are all killed by the new tests, and a normal run still verifies judged entries.",
    "Recovery is intact: rejudge after the timed-out run turns the nine entries verified/supported, and a full re-run keeps the paralegal's accept."
  ],
  "questions_for_chris": []
}
```
