# T-101 r2 review: --write-calibration guards at fdc2506 (round 2)

Reviewer: staff-engineer-reviewer (model claude-haiku-5-5). Verdict: **pass** (0 blockers, 0 majors, 3 minors, 1 nit).

Scope pin. The brief names fdc2506. HEAD is now 9f2811f, and `git diff --stat fdc2506 HEAD -- evals/run.py tests/unit/test_eval_runner.py` printed nothing, so the runner and its tests are byte-identical at HEAD. Every run below used a `git clone --no-hardlinks` of the repo checked out at fdc2506 (commit fdc2506e9caab71146b2f2c98e142d4db4ee4735, tree eacddbee, tracked dirty 0, untracked 0). Deviation from the brief: a `git archive` plus `git init` copy could not be committed, because the git-guard hook blocks bulk `git add` and subagent commits. The clone keeps the cited shas (b85fc1b is needed by the regeneration test). The no-.git check used a plain `git archive` export with no .git directory.

## The four confirmations

1. **`--write-calibration` refuses on untracked files under the eval inputs: confirmed.** Probe script run in the clone, one untracked file per class, each into a fresh `--out`:
   - `evals/golden/case_zz_probe.txt`: rc 2, `calibration_written=no`, stderr names `?? evals/golden/case_zz_probe.txt`.
   - `app/backend/zz_probe.py`: rc 2, not written, names the path.
   - `app/llm/prompts/zz_probe.md`: rc 2, not written, names the path.
   - `tests/fixtures/zz_probe.txt`: rc 2, not written, names the path.
   - Negatives (not refused, calibration written, positive control): `evals/reports/zz_probe.md` (rc 1, the fixture ship bar), `zz_probe_root.txt` at repo root (rc 1), `tests/unit/zz_probe_test.py` (rc 1).
   - Post-probe `git status --porcelain --untracked-files=all` showed only run outputs under evals/reports.
2. **`write_report(write_calibration=True)` has its own guard: confirmed.** Direct calls, checks in a scratch dir: clean header writes; dirty header raises `CalibrationRefused` and leaves the dir empty; no-git header raises and leaves it empty; a report with no calibration key raises. A plain `write_report` of the dirty header writes only `runs/<ts>/calibration.json`. Committed sha unchanged throughout.
3. **A plain or live run never writes the committed calibration.json: confirmed.** Sha256 prefix 49d383b58340ca18 before and after in each case:
   - Fixture plain run (`env -u LLM_BACKEND -u ENABLE_LIVE python -m evals.run`): rc 1 (ship bar not met, expected), sha unchanged, tracked change limited to `evals/reports/latest.json`.
   - Live branch (LLM_BACKEND=claude-cli, ENABLE_LIVE=1) with `build_report` replaced by a real fixture-built report relabelled as claude-cli. No provider was called. Sha unchanged; the scratch copy landed in `runs/<ts>/calibration.json`.
   - No-.git export, plain run: sha unchanged.
   - Dirty-tree plain run: covered by `test_plain_run_with_dirty_tree_still_never_writes_calibration_json`.
4. **The file at HEAD is the restored one: confirmed.** `git log -1 --format='%h %s' -- evals/reports/calibration.json` gives `172028c chore(evals): regenerate calibration.json ... (T-090 r3)`; no commit after it touched the file. Sha256 is 49d383b58340ca18 in HEAD and in the project working tree. `git status --porcelain -- evals/reports/calibration.json` is empty. Header (`python -I` read): backend fixture, source_commit b85fc1b56386aa0d37460186b5840eec0e578642 (ancestor of HEAD), source_tree_clean true. r1 F2 (served file dirty, claude-cli header) is closed.

Test results:
- `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner" -p no:cacheprovider` at fdc2506 clone: `129 passed, 1892 deselected`, rc 0.
- Same command in the project working tree: `129 passed, 1909 deselected`, rc 0 (r1 had 2 failed; the served file is now HEAD's, so those pass).

## Mutation check (scratch clone, 12 mutants, driver and log in the scratchpad: mut/mutate_r2.py, mut/mutation-log.txt; run.py restored byte-identical)

Baseline 129 passed. Killed 8: M1 untracked clause removed, M2 write_report guard removed, M3 main always passes write_calibration=True (4 tests), M4 pre-run refusal removed (2 tests), M6 controls refusal removed, M9 evals dropped from GIT_INPUT_PATHS, M10 evals/reports not excluded, M12 tracked-dirty check removed. Survived 4: M5, M7, M8, M11, covered by F-2, F-1 and the M11 note below.

## Prior findings (r1 reviews/T-101-staff-engineer.md) status

- r1 F1 untracked inputs invisible (major): fixed for behaviour (probes above). Test coverage is partial, see F-1.
- r1 F2 served file dirty (major): closed.
- r1 F3 `--controls` silent no-op (minor): closed. Refused rc 2 with a message before any run (evals/run.py:1184-1187; test at tests/unit/test_eval_runner.py:709).
- r1 F4 scratch and run artifacts in different dirs (minor): closed. One `ts` is passed as `scratch_ts` (evals/run.py:1193, 1207).
- r1 F5 refusal names no dirty file (minor): half closed. The refusal now names the paths. The normal sequence still trips it, see F-3.
- r1 F6 no-git reason not asserted (minor): assertion added (test lines 683-686). Correction to my r1 note: mutant M11 (`or src.get("clean") is None` dropped, evals/run.py:1023) survives because it is equivalent for every state git_source can return. git_source returns commit None whenever clean is None, and the first clause still fires. My r1 claim of a "wrong reason" holds only for {commit set, clean None}, which git_source never produces. No finding remains.
- r1 F7 broad `except Exception` in git_source (nit): closed, narrowed to `except (OSError, subprocess.SubprocessError)` at evals/run.py:88.

## Findings

- **F-1 (minor) The untracked-input refusal is tested for evals/golden only.** Evidence: tests/unit/test_eval_runner.py:883-903 writes only `evals/golden/case_zz_untracked.txt`. Mutants M7 (tests/fixtures dropped from GIT_INPUT_PATHS, evals/run.py:72) and M8 (app dropped) both SURVIVED with 129 passed (mutation-log). Repro: edit evals/run.py:72 to drop `"app"`, then `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` still passes. Why it matters: the behaviour is correct today, but r1 F1's acceptance named app/, so a future edit to GIT_INPUT_PATHS would silently reopen F1. Fix: parametrize the test over `evals/golden/x.txt`, `app/backend/x.py`, `app/llm/prompts/x.md` and `tests/fixtures/x.txt`, with the negatives `evals/reports/x.md` and a repo-root scratch file. Acceptance test: M7 and M8 KILLED.

- **F-2 (minor) The post-run recheck in main() has no test of its own.** Evidence: the recheck is evals/run.py:1199-1205. The test named for it, tests/unit/test_eval_runner.py:650-667 (`test_write_calibration_rechecks_the_header_after_the_run`), passes through the write_report backstop at evals/run.py:1206-1210. Mutant M5 (recheck removed, backstop intact) SURVIVED: 129 passed, rc 0. Why it matters: the test name claims a check it does not isolate, so a regression in main()'s recheck would not be caught while the backstop holds. Fix: assert main()'s own message ("refused after the run, nothing was written") and make write_report raise if it is reached, or rename the test to describe the backstop. Acceptance test: M5 KILLED.

- **F-3 (minor, carried from r1 F5) After any plain run, `--write-calibration` is refused by default.** Evidence: write_report rewrites tracked `evals/reports/latest.json` (evals/run.py:1048) and git_source counts every tracked change (evals/run.py:86). Repro from the clone: `python -m evals.run` (fixture, rc 1), then `--write-calibration --out X` gives rc 2: `(... M evals/reports/latest.json)`, nothing written. Why it matters: the refusal is fail-closed and matches the AC wording, so this is minor. But the normal operator sequence (run, then write) is refused with an operator-facing message that suggests committing unrelated output. Fix: decide explicitly whether a run-rewritten latest.json counts as dirt (see questions); if not, exclude evals/reports/ from the tracked check the same way the untracked check excludes it. Acceptance test: a plain run followed by `--write-calibration` on an otherwise clean tree writes the committed file, or the runbook documents the refusal.

- **N-1 (nit) Stale test docstring.** Evidence: tests/unit/test_eval_runner.py:738-739 says "allowed on a clean tracked tree (untracked files do not count)". That is no longer true for files under the eval inputs. Fix: "untracked files outside the eval inputs do not count".

## What is right

- Plain-run isolation holds in four configurations: fixture, stubbed live branch, no-.git export, dirty tree. Mutant M3 is killed by four tests.
- The pre-run refusal runs before the pipeline (M4 killed by both parametrized cases), and `--controls` combined with `--write-calibration` is refused with a message (M6 killed).
- The refusal now names the dirty paths, so an operator can see which file blocked the write.

## Exercised (commands and results)

- `git log --oneline -5`, `git show --stat fdc2506`, `git show fdc2506 -- evals/run.py` (full diff read); `git rev-parse fdc2506^{tree}` gives eacddbee.
- `git diff --stat fdc2506 HEAD -- evals/run.py tests/unit/test_eval_runner.py`: empty (identical bytes).
- `git show fdc2506:evals/reports/calibration.json | shasum -a 256` and HEAD and working-tree shasums: all 49d383b5.
- Read evals/run.py at fdc2506 (lines 72-88, 1020-1057, 1184-1210) and tests/unit/test_eval_runner.py (lines 597-905).
- `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`: clone 129 passed rc 0; project tree 129 passed rc 0.
- Untracked-file probes (scratch script untracked_probe.sh, run in the clone): golden, app, prompts and fixtures refused rc 2; reports, root and tests/unit allowed rc 1 with calibration written to the probe out dir.
- Plain fixture run in the clone: sha before and after unchanged; `git status --porcelain --untracked-files=all -- app evals tests/fixtures ':(exclude)evals/reports'` empty afterwards.
- Live-branch harness (live_stub.py): plain run sha unchanged; `--write-calibration` refused with ` M evals/reports/latest.json` named.
- Direct guard checks (checks_r2.py, project venv, `-I`): clean/dirty/no-git/no-calibration cases as above.
- No-.git export (`git archive fdc2506 | tar -x`): `--write-calibration` rc 2 "no git repository or HEAD commit is available", out dir not created; plain run sha unchanged.
- Mutation driver: 12 mutants, all restored byte-identical (restored_pristine=True).
- Project tree: `shasum -a 256 evals/reports/calibration.json`, `git status --porcelain -- evals/reports/calibration.json` (empty), `git log -1 -- evals/reports/calibration.json` (172028c).
- Not run: any live provider, any network call, board write commands.

```json
{"card": "T-101", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit fdc2506 (evals/run.py, tests/unit/test_eval_runner.py), byte-identical at HEAD 9f2811f; CLI only, no app URL; sample case evals/golden/sample.txt via the fixture backend plus a stubbed live branch; project working tree observed for the served file and pytest",
 "exercised": ["git show --stat and git show fdc2506 -- evals/run.py; git diff --stat fdc2506 HEAD on the two files (empty)",
  "clone of fdc2506 (tree eacddbee): pytest -q tests/unit -k 'calibration or eval_runner' 129 passed rc 0; same in project tree 129 passed rc 0",
  "untracked-file probes via untracked_probe.sh in the clone: golden, app, prompts, fixtures refused rc 2 nothing written; reports, root, tests/unit not refused",
  "fixture plain run in the clone: calibration.json sha 49d383b5 unchanged; no untracked files under the inputs afterwards",
  "live branch with build_report stubbed to a fixture-built report relabelled claude-cli (no provider called): plain run sha unchanged; --write-calibration refused naming evals/reports/latest.json",
  "direct write_report checks: clean header writes; dirty and no-git headers raise CalibrationRefused with the dir empty; no-calibration refused",
  "no-.git git-archive export: --write-calibration rc 2 with the no-git reason, out dir not created; plain run sha unchanged",
  "mutation driver mutate_r2.py: 12 mutants; killed M1 M2 M3 M4 M6 M9 M10 M12; survived M5 M7 M8 M11; run.py restored byte-identical",
  "project tree: sha256 49d383b5 equals HEAD; git status empty for the file; git log -1 gives 172028c; header read via python -I: backend fixture, source_commit b85fc1b, source_tree_clean true",
  "not run: live provider, network, board write commands"],
 "verdict": "pass",
 "scores": {"plain_run_isolation": 5, "write_guard_refusal": 4, "provenance_header": 4, "test_strength": 3, "cli_surface": 3},
 "findings": [
  {"severity": "minor",
   "title": "Untracked-input refusal is tested for evals/golden only; app, prompts and fixtures are unprotected against regression",
   "evidence": "tests/unit/test_eval_runner.py:883-903 writes only evals/golden/case_zz_untracked.txt; mutant M7 (tests/fixtures dropped, evals/run.py:72) and M8 (app dropped) both SURVIVED with 129 passed (mutation-log in scratchpad)",
   "why_it_matters": "Behaviour is correct today (probe refuses all four input classes), but r1 F1 acceptance named app/, so a future edit to GIT_INPUT_PATHS would silently reopen F1.",
   "fix": "Parametrize the test over evals/golden/x.txt, app/backend/x.py, app/llm/prompts/x.md, tests/fixtures/x.txt; keep evals/reports/x.md and a repo-root scratch file as negatives.",
   "acceptance_test": "Mutants M7 and M8 are KILLED by the T-101 selection."},
  {"severity": "minor",
   "title": "The post-run recheck in main() has no test of its own; the test named for it passes through the write_report backstop",
   "evidence": "evals/run.py:1199-1205 is the recheck; tests/unit/test_eval_runner.py:650-667 passes via evals/run.py:1206-1210 (CalibrationRefused backstop). Mutant M5 (recheck removed, backstop intact) SURVIVED: 129 passed rc 0",
   "why_it_matters": "The test name claims a check it does not isolate, so a regression in main()'s recheck would not be caught while the backstop holds.",
   "fix": "Assert main()'s own refusal message and make write_report raise if reached; or rename the test to describe the backstop.",
   "acceptance_test": "Mutant M5 is KILLED by the T-101 selection."},
  {"severity": "minor",
   "title": "After any plain run, --write-calibration is refused by default (carried from r1 F5)",
   "evidence": "evals/run.py:1048 rewrites tracked evals/reports/latest.json; evals/run.py:86 counts every tracked change as dirt. Repro in the clone: python -m evals.run (rc 1), then --write-calibration --out X gives rc 2 with '( M evals/reports/latest.json)' and nothing written",
   "why_it_matters": "The refusal is fail-closed and matches the AC wording, but the normal operator sequence is refused with a message that asks the operator to commit unrelated output.",
   "fix": "Decide whether a run-rewritten latest.json counts as dirt; if not, exclude evals/reports/ from the tracked check the same way the untracked check excludes it.",
   "acceptance_test": "A plain run followed by --write-calibration on an otherwise clean tree writes the committed file, or the runbook documents the refusal."},
  {"severity": "nit",
   "title": "Stale test docstring: untracked files do not count",
   "evidence": "tests/unit/test_eval_runner.py:738-739 'allowed on a clean tracked tree (untracked files do not count)'",
   "why_it_matters": "It contradicts the F1 rule that untracked files under the eval inputs do count.",
   "fix": "Reword to 'untracked files outside the eval inputs do not count'.",
   "acceptance_test": "Docstring matches GIT_INPUT_PATHS (evals/run.py:72)."}
 ],
 "whats_right": ["Plain-run isolation holds in four configurations (fixture, stubbed live branch, no-.git export, dirty tree); mutant M3 is killed by four tests",
  "The pre-run refusal runs before the pipeline (M4 killed by both cases) and --controls with --write-calibration is refused with a message (M6 killed)",
  "The refusal now names the dirty paths, so an operator can see which file blocked the write"],
 "questions_for_chris": ["Should a run-rewritten tracked evals/reports/latest.json count as dirt for --write-calibration (F-3)? Today it blocks the normal run-then-write sequence.",
  "Should --write-calibration be limited to the recorded fixture backend? Today any backend that passes the tree check replaces the served calibration.json (evals/run.py:1208); r1 raised this and it is still open."]}
```
