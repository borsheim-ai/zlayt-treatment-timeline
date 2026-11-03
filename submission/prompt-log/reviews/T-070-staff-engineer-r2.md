# T-070 round 2 review: staff-engineer-reviewer (commit 20471a7)

**Verdict: pass.** No blockers, no majors. The r1 major is closed: a padded or mixed-case live name without `ENABLE_LIVE` now exits 2, an unknown name exits 2, and a test fails when the normalization is mutated out. One nit (wording of the error message when the value came from `--backend`).

Pinned to 20471a7 with `git archive` (HEAD at review time is 20471a7; the working tree has unrelated uncommitted changes under `.claude/agent-memory/`, which I did not touch). Scope is `evals/run.py` and `tests/unit/test_eval_runner.py` only.

**Checks against the three asks**

1. `" claude-cli "` and `"Claude-CLI"` without `ENABLE_LIVE`: exit 2, no stdout, no report directory written, and the refusal is at `evals/run.py:695`, before `build_report` at `:701`, so no fixture run happens. Probes below show rc=2 for both, and `ls` of the `--out` directory fails (nothing written).
2. Unknown names: `openai`, `claude`, `claude-cli-x`, `anthropic`, `fixtures`, `lol` (env and `--backend`) exit 2 with "Nothing was run." and no report. Covered by `tests/unit/test_eval_runner.py:382-391` and `:393-404`.
3. Normalization mutated out: four mutants in scratch copies of the pinned tree each fail the unit file (see table). The guard-inversion mutant (`ENABLE_LIVE != "1"` changed to `== "1"`) also fails 8 tests, including the new `test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name`, so the r1 minor is closed too.

**Deterministic results**

- `.venv/bin/python -m pytest -q tests/unit/test_eval_runner.py` (working tree, HEAD 20471a7): `64 passed in 1.86s`.
- Same file in the pinned copy with `PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_runner.py`: `64 passed in 1.97s`.

**Mutants (scratch copies, not committed)**

| Mutant | Change | Result |
|---|---|---|
| m1 | `normalize_backend` drops `.strip().lower()` | 12 failed, 52 passed |
| m2 | `normalize_backend` returns any name (no unknown check) | 11 failed, 53 passed |
| m3 | `main` uses `raw or "fixture"` instead of `normalize_backend(raw)` | 15 failed, 49 passed |
| m4 | guard tests `raw in LIVE_BACKENDS` instead of normalized `backend` | 6 failed, 58 passed |
| m5 | `ENABLE_LIVE != "1"` inverted to `== "1"` | 8 failed, 56 passed |

**CLI probes (pinned copy, `python -m evals.run`, ENABLE_LIVE unset, no live call made)**

- `LLM_BACKEND=" claude-cli "`: rc=2, stderr `evals.run: backend=claude-cli requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend (D-008/D-020). ...`, no output dir.
- `LLM_BACKEND="Claude-CLI"`: rc=2, same message, no output dir.
- `LLM_BACKEND="anthropic-api"`: rc=2, ENABLE_LIVE message, no output dir.
- `LLM_BACKEND="openai"`: rc=2, `evals.run: unknown LLM_BACKEND 'openai'; known backends are fixture, claude-cli, anthropic-api (after strip and lower-case). Nothing was run.`, no output dir.
- `--backend " claude-cli "` with LLM_BACKEND unset: rc=2, ENABLE_LIVE message.
- `--backend "openai"`: rc=2, `unknown LLM_BACKEND 'openai'...` (see nit).
- Positive control `LLM_BACKEND="fixture"`: rc=1, `ship_bar_met=False backend=fixture report=probe_7/20261102T030435Z.md`, blockers `4_no_invented_facts` and `backend=fixture: determinism_3run and unsupported_count_3run need a live backend`. The fixture path still runs and labels itself honestly.

**Read-only checks**

- `evals/run.py:688-694` normalizes once and feeds the normalized name to the guard and to `build_report`. The pipeline gets the same normalized name: `app/backend/pipeline.py:413-422` (`_Backend`) sets `LLM_BACKEND` to it for the call, so the live path and the guard agree.
- `app/llm/provider.py:27` strips the same variable, and `:92-111` raises `LLMError("UNKNOWN_BACKEND ...")` for an unrecognised live-looking name, so the app side does not fall through silently either.

## Finding

**nit: the unknown-name message says `LLM_BACKEND` even when the value came from `--backend`.**
- Evidence: `evals/run.py:692` prints `unknown LLM_BACKEND {raw!r}` for both sources. Repro: `env -u ENABLE_LIVE -u LLM_BACKEND .venv/bin/python -m evals.run --backend "openai" --out <dir>` prints `evals.run: unknown LLM_BACKEND 'openai'; ...`. The test `tests/unit/test_eval_runner.py:393-404` asserts the same wording for the flag path, so the test locks it in.
- Why it matters: the operator reads the wrong variable name. Nothing is run and the exit code is correct, so this is cosmetic.
- Fix: name the source, for example `unknown backend {raw!r} from {source}` where `source` is `--backend` or `LLM_BACKEND`. Update the flag-path assertion to match.
- Acceptance test: `--backend openai` prints a message containing `--backend` and not `LLM_BACKEND`; `LLM_BACKEND=openai` still prints `LLM_BACKEND`; both exit 2 and write no `*.json`.

## Out of scope for this card (noted, not a finding)

- `app/llm/provider.py:27-29` serves `fixture` silently for any non-fixture `LLM_BACKEND` when `ENABLE_LIVE` is unset (by design, D-008/D-020). The eval runner now refuses these names; the app does not. This is outside 20471a7's diff, so I did not count it against T-070.

```json
{"card": "T-070", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 20471a7 (evals/run.py, tests/unit/test_eval_runner.py); pinned via git archive 20471a7; HEAD 20471a7 at review time; no app URL; eval runner only",
 "exercised": [
   "git show 20471a7 -- evals/run.py and -- tests/unit/test_eval_runner.py (full diff read)",
   "sed/grep read of evals/run.py main() at HEAD (lines 661-706) and normalize_backend (653-658), load_pipeline (631), refuse_curated (640)",
   "app/llm/provider.py:20-30 and :92-111; app/backend/pipeline.py:405-432 (_Backend, run_case)",
   ".venv/bin/python -m pytest -q tests/unit/test_eval_runner.py (working tree): 64 passed in 1.86s",
   "git archive 20471a7 | tar -x into scratch t070r2b; PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_runner.py: 64 passed in 1.97s",
   "CLI probe env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' python -m evals.run --out ./probe_1: rc=2, ENABLE_LIVE message, no output dir",
   "CLI probe LLM_BACKEND=Claude-CLI (ENABLE_LIVE unset): rc=2, ENABLE_LIVE message, no output dir",
   "CLI probe LLM_BACKEND=anthropic-api (ENABLE_LIVE unset): rc=2, ENABLE_LIVE message, no output dir",
   "CLI probe LLM_BACKEND=openai: rc=2, 'unknown LLM_BACKEND ... Nothing was run.', no output dir",
   "CLI probe --backend ' claude-cli ' with LLM_BACKEND unset: rc=2, ENABLE_LIVE message",
   "CLI probe --backend openai: rc=2, unknown-name message (wording nit)",
   "CLI control LLM_BACKEND=fixture (ENABLE_LIVE unset): rc=1, 'ship_bar_met=False backend=fixture', report written to scratch",
   "Mutant m1 (normalize drops strip/lower): pytest tests/unit/test_eval_runner.py -> 12 failed, 52 passed",
   "Mutant m2 (normalize accepts any name): pytest -> 11 failed, 53 passed",
   "Mutant m3 (main uses raw or 'fixture' instead of normalize_backend): pytest -> 15 failed, 49 passed",
   "Mutant m4 (guard tests raw instead of normalized name): pytest -> 6 failed, 58 passed",
   "Mutant m5 (ENABLE_LIVE guard inverted to == '1'): pytest -> 8 failed, 56 passed, including test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name",
   "Mutants were applied only in scratch copies (m1-m5 under the scratchpad); no product file changed; no live backend was invoked (ENABLE_LIVE never set to 1 outside monkeypatched tests)"
 ],
 "verdict": "pass",
 "scores": {"ac_met_as_written": 5, "padded_and_mixed_case_refused": 5, "unknown_names_exit_2": 5, "tests_non_vacuous_under_mutation": 5, "no_silent_fallback": 5, "error_message_accuracy": 3, "scope_discipline": 5},
 "findings": [
   {"severity": "nit",
    "title": "Unknown-name message says LLM_BACKEND even when the value came from --backend",
    "evidence": "evals/run.py:692: print(f\"evals.run: unknown LLM_BACKEND {raw!r}; known backends are ...\"). Repro: env -u ENABLE_LIVE -u LLM_BACKEND .venv/bin/python -m evals.run --backend \"openai\" --out <dir> -> stderr \"evals.run: unknown LLM_BACKEND 'openai'; known backends are fixture, claude-cli, anthropic-api (after strip and lower-case). Nothing was run.\" rc=2. tests/unit/test_eval_runner.py:393-404 asserts the same wording for the flag path.",
    "why_it_matters": "The operator is told to look at the wrong variable. The run is still refused with rc 2 and no report, so this is cosmetic, but it costs time when debugging a command line.",
    "fix": "Name the source in the message: 'unknown backend {raw!r} from {source}' where source is '--backend' or 'LLM_BACKEND'. Update the flag-path assertion in test_backend_flag_is_validated_like_the_env_var to match.",
    "acceptance_test": "--backend openai prints a message containing '--backend' and not 'LLM_BACKEND'; LLM_BACKEND=openai still prints 'LLM_BACKEND'; both exit 2 and write no *.json under --out."}
 ],
 "whats_right": [
   "Normalization happens once (evals/run.py:688-689), and the guard, build_report and _Backend (app/backend/pipeline.py:413-422) all see the same normalized name, so the refusal and the live path cannot disagree.",
   "Refusals return 2 before build_report (evals/run.py:695-700 vs 701), so a refused request runs no fixture and writes no report; the probes confirm no output directory is created.",
   "The new tests are non-vacuous: all four normalization and guard mutants and the guard inversion each fail between 6 and 15 tests, and the reach-the-pipeline test closes the r1 minor."
 ],
 "questions_for_chris": ["Should app/llm/provider.py backend_name() (lines 27-29) also refuse unknown LLM_BACKEND names when ENABLE_LIVE is unset, the way the eval runner now does? Today it silently serves fixture, which is the by-design demo behaviour (D-008/D-020); I did not count it against T-070."]}
```
