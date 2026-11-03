# T-070 review: staff-engineer-reviewer (commit 815d616)

**Verdict: changes.** One major, one minor, no blockers. Pinned to 815d616 with `git archive` (HEAD moved to b9d3ead during the review; the commit touches only `evals/run.py`, `tests/unit/test_eval_runner.py` and one report file).

**AC check: met as written.** The AC asks that `LLM_BACKEND=claude-cli ENABLE_LIVE=1 ... --runs 3` reports `backend=claude-cli`, measures determinism and unsupported counts, and notes the report path. The committed report `evals/reports/20261102T025219Z.md` does that. Its determinism is 0.0 against a bar of 1.0. The AC does not require the bar, so I did not count it as a finding. T-075 tracks it.

**Refusal: exact string only.** With `ENABLE_LIVE` unset, `LLM_BACKEND=claude-cli` exits 2 as intended. A padded or mixed-case value (`" claude-cli "`, `Claude-CLI`) still runs the fixture pipeline and writes a report labelled `backend=fixture`. The label is honest, so nothing is misreported, but the refusal does not cover the case its title describes.

Probes: the guard test fails when the check is disabled (mutant), so the test is not vacuous.

```json
{"card": "T-070", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 815d616 (evals/run.py, tests/unit/test_eval_runner.py, evals/reports/20261102T025219Z.md); pinned via git archive; HEAD during review b9d3ead; no app URL; eval runner only (no product code in scope)",
 "exercised": [
   "git show 815d616 --stat and git show 815d616 -- evals/run.py tests/unit/test_eval_runner.py (full diff read)",
   "git archive 815d616 | tar -x -C <scratchpad>/t070",
   "PYTHONPATH=. .venv/bin/python -m pytest tests/unit/test_eval_runner.py -q -k live_backend at 815d616: 2 passed, 36 deselected",
   "PYTHONPATH=. .venv/bin/python -m pytest tests/unit -q at 815d616: 2 failed (tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, ::test_data_attributes_declared), 943 passed; both files are untouched by 815d616",
   "Mutant in scratch copy: evals/run.py:680 condition replaced with `if False:`; pytest -k live_backend -> 1 failed (test_live_backend_without_enable_live_is_refused), 1 passed; scratch file restored and cmp-identical to git show 815d616:evals/run.py",
   "Control: LLM_BACKEND=claude-cli .venv/bin/python -m evals.run --out <scratch>/probeC (ENABLE_LIVE unset) -> rc=2 with message 'requested but ENABLE_LIVE=1 is not set'",
   "Probe A: env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' .venv/bin/python -m evals.run --out <scratch>/probeA -> rc=1, stdout 'ship_bar_met=False backend=fixture report=.../probeA/20261102T025742Z.md'; report backend=fixture, backend_requested=' claude-cli '",
   "Probe B: env -u ENABLE_LIVE LLM_BACKEND='Claude-CLI' ... --out <scratch>/probeB -> rc=1, backend=fixture (same bypass)",
   "Read evals/run.py:32, 567, 679-680 and app/llm/provider.py:23-30, 27 at 815d616 (LIVE_BACKENDS exact match; report label from pipeline-served backend; provider strips LLM_BACKEND)",
   "git show 815d616:evals/reports/20261102T025219Z.md cmp-identical to working tree; header '**ship_bar_met: False**  backend `claude-cli`'; metrics table read (determinism_3run 0.0 vs 1.0, unsupported_count_3run 0, blocker 4_no_invented_facts)",
   ".venv/bin/python tools/board.py show T-070 and show T-075 (read-only)"
 ],
 "verdict": "changes",
 "scores": {"ac_met_as_written": 5, "refusal_covers_requested_forms": 3, "test_non_vacuous": 5, "report_label_honesty": 5, "no_silent_fallback": 4, "scope_discipline": 5},
 "findings": [
   {"severity": "major",
    "title": "Guard matches the raw LLM_BACKEND string, so padded or mixed-case live names still run as fixture",
    "evidence": "evals/run.py:679-680 at 815d616: `backend = a.backend or os.environ.get(\"LLM_BACKEND\", \"fixture\")` then `if pipeline is None and backend in LIVE_BACKENDS and os.environ.get(\"ENABLE_LIVE\") != \"1\":`; LIVE_BACKENDS (evals/run.py:32) is an exact tuple match. app/llm/provider.py:27 strips the same variable, so the provider and the guard disagree. Repro: git archive 815d616 | tar -x -C <dir>; cd <dir>; env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out <dir>/out -> rc=1, 'ship_bar_met=False backend=fixture'; report JSON backend='fixture', backend_requested=' claude-cli '. Same with LLM_BACKEND=Claude-CLI.",
    "why_it_matters": "T-070 exists because a requested live run silently ran as fixture. The exact-string guard fixes only the spelling the test uses. A trailing space from a quoted or hand-edited .env, or a capitalised name, still runs the fixture pipeline and writes an eval report that looks like a finished run. The report label is honest (backend=fixture) and the ship bar blocks it, so this is not a false label and not a silent pass. It is a major because the refusal does not hold for the request the card names.",
    "fix": "Normalise and validate the name before the check: backend = (a.backend or os.environ.get(\"LLM_BACKEND\", \"fixture\")).strip(); refuse (rc 2, same message, no report written) any value not in (\"fixture\",) + LIVE_BACKENDS, since an unknown name is an error, not a fixture run. Keep the ENABLE_LIVE check for live names. Optionally also refuse after the run if the requested backend is live and report['backend'] == 'fixture'.",
    "acceptance_test": "Parametrised unit test in tests/unit/test_eval_runner.py with ENABLE_LIVE unset and LLM_BACKEND in [' claude-cli ', 'Claude-CLI', 'claude-cli\\n', 'anthropic-api ']: main([...]) == 2, stderr contains 'ENABLE_LIVE=1' (or 'unknown backend'), and no *.json written to tmp_path. Positive control: LLM_BACKEND='fixture' returns 0 and the report says backend fixture."},
   {"severity": "minor",
    "title": "No unit assertion that a correctly configured live run reaches the pipeline",
    "evidence": "tests/unit/test_eval_runner.py:362-368 (test_live_backend_without_enable_live_is_refused) asserts only rc 2 for the unset case. The 815d616 diff adds no test with ENABLE_LIVE=1. The live path is evidenced only by the committed manual report.",
    "why_it_matters": "A later edit that refuses a correctly configured live run (for example a wrong comparison) would pass the suite and surface only at the next manual eval.",
    "fix": "Add a test with ENABLE_LIVE=1 and LLM_BACKEND=claude-cli, monkeypatching load_pipeline (or passing a fake pipeline is not enough, since the guard skips injected pipelines) to a recorder, and assert the run proceeds past the guard (rc != 2).",
    "acceptance_test": "The new test fails when the guard condition is inverted (ENABLE_LIVE != '1' changed to == '1') and passes at HEAD."}
 ],
 "whats_right": [
   "The guard is non-vacuous: with the condition disabled in the pinned copy, test_live_backend_without_enable_live_is_refused fails (1 failed, 1 passed).",
   "The report label is what the pipeline served (evals/run.py:567 sample_out.get('backend'), request kept in backend_requested), so the probes show backend=fixture and not a false claude-cli label.",
   "The refusal returns 2 before build_report, so a refused request writes no report file (asserted by the test's `not list(tmp_path.glob('*.json'))`)."
 ],
 "questions_for_chris": []}
```
