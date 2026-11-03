# T-075 review: staff-engineer-reviewer (commit 3104213, HEAD at review time)

Verdict: **changes**. No blocker, four majors, three minors.

The R-CO-7 definition in `evals/run.py` was **not weakened by this commit**: `evals/run.py` is not in `git show --stat 3104213`, and `git log -L383,404:evals/run.py` shows the function last changed in c8c7ba6 (T-038 r1). The commit does not cache anything. Every `run_case` builds a fresh `tempfile.TemporaryDirectory` database, `claude-cli` runs with `--no-session-persistence` and a timeout, and the fixture backend is only used when `ENABLE_LIVE` is unset.

My own live re-run (`LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --runs 3 --out <scratch>`) gave determinism 1.0, unsupported 0 and hallucination catch 40/40, as claimed. It also gave `ship_bar_met False` (golden_must_not_hits 1, entry_recall 0.965), which is finding 4.

What stays open:
- **Per-run artifacts are not kept.** The 0.0 is still undiagnosable if it recurs (finding 1).
- **The determinism metric is narrower than the R-CO-7 text.** Mutations to flag record ids, record split and totals all go undetected (finding 2).
- **Two of the new tests do not kill the mutants they claim to cover** (findings 3 and 6).
- **The fix is not evidenced by the report.** The pre-fix baseline was also 1.0 in 12 of 12 runs, so the green report cannot discriminate fixed from unfixed (finding 7).

```json
{
  "card": "T-075",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit 3104213 (app/backend/flags.py, judges.py, app/llm/audited.py, judge_flag_v2.md, judge_conflict_v2.md, tests/unit/test_t075_determinism.py, evals/reports/determinism-diagnosis.md, evals/reports/20261102T032823Z.md); evals/run.py signature/live_metrics; sample case (live claude-cli); no app URL",
  "exercised": [
    "python3 tools/board.py show T-075; git log/show --stat 3104213; git log -L383,404:evals/run.py (signature unchanged since c8c7ba6)",
    "read R-CO-7 and R-CO-3 in spec/REQUIREMENTS.md, evals/reports/determinism-diagnosis.md, evals/reports/20261102T032823Z.md, full code diff of app/ and tests/ in 3104213",
    ".venv/bin/python -m pytest tests/unit -q -> 1031 passed",
    "scratch script /private/tmp/claude-501/scratch-t075/sigtest.py: 17 mutations of one fixture run_case output, each run through evals.run.signature; MISSED: flag evidence record_id, flag record_nos/record_ids, totals (detected_pending_cents), record split (drop record, alter record text), flag reasons, entry id rename; DETECTED: flag state, flag excerpt, dropped flag, amount cents/kind/state, entry state/date/record_ids. totals has no key 'detected_not_a_total' (keys: accepted_cents, detected_pending_cents, detected_label, unclear_items, amounts_found, status, letter_line, ui_line)",
    "mutation spot-checks on git archive 3104213 in /private/tmp/claude-501/scratch-t075/repo (tests/unit/test_t075_determinism.py only): remove model-flag sort -> 4 passed (survives); remove conflict dedupe -> 1 failed; remove conflict sort -> 1 failed; make_call sleep always None -> 1 failed; always on -> 1 failed; J3 category line removed -> 1 failed; judges.run_j4_meta back to judge_flag_v1 -> 4 passed (survives). Control: with record 8 and two model-only flags (missed_care 'C5-C6 disc protrusion...', patient_report 'Charge: $2,150.') in swapped order, outputs are equal with the sort and differ without it",
    "live probe of v2 judges (claude-cli, 2 reps each, scratch probe.py): J4 on 8 seeded cases (negated, wrong category, wrong type, not-in-quote, 2 true flags) and J3 on 4 seeded pairs: 24/24 verdicts correct and stable across reps",
    "live eval re-run: LLM_BACKEND=claude-cli ENABLE_LIVE=1 .venv/bin/python -m evals.run --runs 3 --out /private/tmp/claude-501/scratch-t075/out -> report 20261102T034136Z.md: determinism_3run 1.0, unsupported_count_3run 0, hallucination 40/40, ship_bar_met False (blocker 4_no_invented_facts: golden_must_not_hits 1 on case_02, unsupported_summaries 1; entry_recall 0.965). ANTHROPIC_API_KEY not set or exported",
    "grep of changed lines for except/float(/sleep( (none added); read app/llm/provider.py, audited.py (RETRY_DELAYS_S 0.5/1.5, 3 attempts), claude_cli.py flags; grep for logging config in evals/run.py (none)"
  ],
  "verdict": "changes",
  "scores": {
    "r_co_7_definition_preserved": 4,
    "determinism_metric_sensitivity": 2,
    "diagnosability_of_future_failure": 1,
    "no_cross_run_caching": 5,
    "judge_prompt_discrimination": 4,
    "test_strength": 3,
    "evidence_honesty": 4
  },
  "findings": [
    {
      "severity": "major",
      "title": "Per-run determinism data is still discarded, so a recurrence of 0.0 is as undiagnosable as the first",
      "evidence": "evals/run.py:399-403: `sigs = [signature(o) for o in outs]` is a local; only {value, runs, status, r_ids} is returned. `python3 -c` on evals/reports/latest.json shows determinism_3run = {'r_ids': ['R-CO-7'], 'runs': 3, 'status': 'measured', 'value': 1.0} with no signatures. `git show --stat 3104213` does not touch evals/run.py. evals/run.py has no logging config, so 'llm call failed ... attempt=1' only goes to stderr. determinism-diagnosis.md section 4 says 'The per-run data of that report was not kept ... the eval runner writes only the aggregate' and the handoff says 'if it recurs, the eval should persist per-run signatures (qa)', so the known gap was deferred. The diagnosis section 1 set B report 'kept in the session scratch dir' is also not in the repo.",
      "why_it_matters": "The original 0.0 had a cause that is only inferred ('likely calls failing all retries under load'). The one change that would make the next 0.0 diagnosable was left undone. The card is the M2 gate blocker, and a recurrence at the gate leaves the team where it started.",
      "fix": "In live_metrics keep the per-run signatures (or the full per-run outputs minus text bodies) and write them next to the report (for example evals/reports/<ts>.runs.json). When determinism < 1.0, list the differing items (key, run, field) in the .md report. Configure logging in the CLI so failed-attempt warnings and the final call error codes per run land in that file.",
      "acceptance_test": "Unit test: live_metrics with Perfect(mutate=drop_in_run_2) returns/writes per-run signatures and the report names the dropped flag's (type, category, excerpt) and run number. Live: python -m evals.run --runs 3 leaves a runs file with 3 signatures."
    },
    {
      "severity": "major",
      "title": "The determinism signature is narrower than R-CO-7's text: flag record ids, record split and totals are not compared, and the totals term reads a key that does not exist",
      "evidence": "evals/run.py:383-390. R-CO-7: 'Flags are compared by (type, set of cited record IDs, evidence excerpt)'; code outputs identical include 'record split ... totals'. The signature's flag term is (type, category, excerpts, state) with no record ids. Its last term is `(out.get('totals') or {}).get('detected_not_a_total')`, but run_case totals has no such key, so the term is always None. Mutation results from sigtest.py: changing flag evidence record_id -> MISSED; flag record_ids -> MISSED; totals.detected_pending_cents -> MISSED; dropping a record -> MISSED; altering record 1 text -> MISSED; entry-id rename -> MISSED. (Amount cents/kind/state, flag state/excerpt/drop, entry date/state/record_ids are DETECTED.) Not introduced by 3104213; unchanged since c8c7ba6.",
      "why_it_matters": "The card AC is 'determinism_3run 1.0 without weakening R-CO-7's definition'. The definition was not changed by this commit, but the metric that gates M2 cannot see a flag that cites different records with the same quote, or a changed total. The 1.0 is weaker evidence than the report implies.",
      "fix": "Add the flag record_ids (sorted) to the flag term, the full `totals` dict (sorted keys) instead of the dead key, and the record list (n, excerpt hash) and entry id set to the signature. Keep the summary text out. Do not drop `category`.",
      "acceptance_test": "Parametrised unit test over signature(): each of the mutations above (flag record_ids, totals.detected_pending_cents, record excerpt, record count, entry ids) changes the signature; an entry summary rewrite does not."
    },
    {
      "severity": "major",
      "title": "test_model_flag_order_does_not_change_the_flag_list passes with the sort removed",
      "evidence": "tests/unit/test_t075_determinism.py:27-38. Mutation in the git-archive scratch copy: replace `uniq.sort(key=...)` in app/backend/flags.py:125 with a no-op -> `pytest tests/unit/test_t075_determinism.py -q` -> '4 passed'. Cause: of inputs a, b, c only c (missed_care) is model-only; a and b pair with lexicon flags (origin 'both'), so order is invisible. Control showing the sort matters: two model-only flags (missed_care on 'C5-C6 disc protrusion with mild right foraminal narrowing.', patient_report on 'Charge: $2,150.') in swapped order give equal output with the sort and [..., 'missed_care', 'patient_report'] vs [..., 'patient_report', 'missed_care'] without it.",
      "why_it_matters": "The docstring says 'Two model-only flags returned in either order give the same flags'. That is false for the test's inputs. The model-flag sort is the fix for 'order-dependent f_r{n}_{k} ids', and nothing proves it. The conflict-pass sort and dedupe are covered (their mutants fail), so the asymmetry is easy to miss.",
      "fix": "Add the two-model-only-flags case above (swapped orders, include a duplicate), and a second case where two model flags overlap the same lexicon flag so the pairing is order-sensitive. Fix the docstring.",
      "acceptance_test": "Removing `uniq.sort` in flags.merge makes the new test fail."
    },
    {
      "severity": "major",
      "title": "A fresh live run does not meet the ship bar: golden_must_not_hits 1 on case_02 and entry_recall 0.965 (non-sample, not caused by this diff as far as I can tell)",
      "evidence": "evals/reports run in scratch: /private/tmp/claude-501/scratch-t075/out/20261102T034136Z.md: 'ship_bar_met: False', 'Blockers: 4_no_invented_facts', 'golden_must_not_hits | 1 | 0', 'must_not detail: {case_02_gap_boundaries: {... unsupported_summaries: 1}}', 'entry_recall 0.965'. The committed report 20261102T032823Z.md has the same metrics at 0 hits and 0.982. Same command, same HEAD. J1 prompt (judge_faithfulness_v1), extract_v1 and the fixtures for them are untouched by 3104213, so this is generator or J1 variance on case_02.",
      "why_it_matters": "T-075 is the M2 gate blocker. The handoff cites one green report as proof of a stable gate. Two live runs of the same eval gave different ship_bar_met. R-CO-3 treats any must_not hit as a blocker, and R-CO-7 is only gated on the sample, so the case_02 variance is outside the AC, but the gate still needs it triaged.",
      "fix": "Open a card (qa/backend) for the case_02 unsupported summary: find which entry, its J1 verdict and whether the product marked it rejected; decide if the bar counts a caught-and-rejected summary. Until then, do not describe the gate as stable on one report.",
      "acceptance_test": "Three consecutive full live evals (`--runs 3`) each report ship_bar_met True, or the bar definition for caught-and-rejected summaries is changed by decision record."
    },
    {
      "severity": "minor",
      "title": "Reverting J4 to judge_flag_v1 in judges.py passes every T-075 test, and the audit record would still say v2",
      "evidence": "Mutation: app/backend/judges.py run_j4_meta `\"judge_flag_v2\", schemas.Judge4` -> `\"judge_flag_v1\"` -> '4 passed'. flags.py:judge_flags hard-codes `pv = \"judge_flag_v2\"` separately from the prompt that judges.py loads, and test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2 asserts only the ladder's pv string, PROMPT_OF_STEP, and the J3 category text.",
      "why_it_matters": "Two places name the same prompt. Drift gives an audit trail that lies about which prompt judged an item (checklist item 9).",
      "fix": "Have run_j4_meta/run_j3_meta return or expose the prompt version they used and have flags.py read it. Add a test that the J4 call's system text equals promptlib.load('judge_flag_v2').text.",
      "acceptance_test": "The v1 revert above fails a test."
    },
    {
      "severity": "minor",
      "title": "No committed negative control for the v2 flag and conflict judges; hallucination 40/40 does not measure them",
      "evidence": "evals/run.py:551: hallucination_catch_rate is computed with `pipeline.judge_summary` -> judges.run_j1 (judge_faithfulness_v1, unchanged by 3104213). `grep -rln 'run_j4\\|judge_flag' evals tests/unit` finds only report files and no seeded wrong-flag cases. My own live probe of 8 J4 and 4 J3 seeded cases (2 reps) gave 24/24 correct, so I have no evidence of a regression, but the repo has none either.",
      "why_it_matters": "v1 over-rejected, which is safe. v2 now says 'agree' for four flag categories that were 'disagree' on every run, so the failure that matters (agree on a wrong flag) has no test or eval. The brief's check 'the v2 prompts do not lower hallucination catch' is satisfied only trivially.",
      "fix": "Add a small seeded set (wrong category, negated, wrong type, quote not containing the named wording; plain pairs for J3) with an expected verdict, and report catch rate and false-agree count in the eval report for J3/J4.",
      "acceptance_test": "evals.run reports flag_judge_catch_rate on a live backend; a prompt that returns 'agree' for everything makes it fail."
    },
    {
      "severity": "minor",
      "title": "Handoff/AC wording presents the fix as the cause of the 1.0, but the baseline was already 1.0 in 12 of 12 runs",
      "evidence": "determinism-diagnosis.md sections 1 and 4: 'the 0.0 does not reproduce on demand: 12 live runs before the fix agreed on every state' and 'a judge or generator call that failed on all three attempts ... inference, not observed'. Card AC 2 is checked 'done' on one green report. The retry pause (RETRY_DELAYS_S = (0.5, 1.5), app/llm/audited.py:17) is tested only as `callable(seen[1])`.",
      "why_it_matters": "Honest in the diagnosis, but the board shows AC 2/2 done. A reader of the card will assume the 0.0 is fixed. Nothing shows a 0.5 s and 1.5 s pause survives the load that is thought to have caused it. I label this a wording and evidence issue, not a defect in the code.",
      "fix": "Mark the card note 'cause unconfirmed, fix is mitigation' and carry it into the M2 gate summary. Optionally test the delay values against RETRY_DELAYS_S.",
      "acceptance_test": "Card note and gate summary state the cause is unconfirmed; a test asserts the sleeps are called with (0.5, 1.5) on a live backend and never on fixture."
    }
  ],
  "whats_right": [
    "Conflict-pass ordering and dedupe, J3 category line and the live/fixture retry pause each have a test whose removal fails it, and no new bare except, float or sleep was added.",
    "The v2 judge prompts discriminate: 24/24 seeded live verdicts correct and stable across two repetitions, and the diagnosis candidly says the 0.0 cause is an inference.",
    "No cross-run state: fresh scratch database per run_case, --no-session-persistence, timeout on every claude-cli call; the signature definition itself was left untouched."
  ],
  "questions_for_chris": [
    "Should the ship bar count a summary that J1 judged unsupported and the pipeline rejected (case_02) as a golden_must_not hit, given nothing unsupported reaches the export?"
  ]
}
```
