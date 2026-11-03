# T-101 review: evals.run leaves calibration.json alone; --write-calibration only from a clean HEAD (commit 4c5f9bf)

Reviewer: staff-engineer-reviewer (model claude-haiku-5-5). Verdict: **changes** (0 blockers, 2 majors, 5 minors, 1 nit).

The three confirmations the brief asked for, all run at 4c5f9bf in a clone and in a git archive copy:

1. A plain `python -m evals.run` leaves evals/reports/calibration.json byte-identical. Confirmed (sha256 49d383b5... before and after, archive copy and clone, including a plain run on a dirty tree).
2. `--write-calibration` refuses on a dirty tracked tree and writes the T-090 header on a clean one. Confirmed (rc 2 with nothing run and nothing written on a dirty tree; on a clean clone the header is source_commit 4c5f9bf, source_tree_clean true, source_tree 4b4960da, equal to `git rev-parse 4c5f9bf^{tree}`). Its refusal is also literal to the AC: untracked files do not block it, which lets the header claim a clean tree for inputs the tree does not contain (F1).
3. Mutating the guard fails tests. Confirmed for 7 of 8 mutants (M1 to M7 killed; M8, the no-git clause, survives; F6).

Deviation from the brief, stated up front: I used `git clone --no-hardlinks` plus `checkout --detach 4c5f9bf` instead of `git archive` plus `git init`, so that the cited commit b85fc1b exists for the regeneration test. The archive copy (no .git) was used for the plain-run and no-git checks.

Two findings were judged against D.2 and not rated blocker, with the reason. F1: the card's AC is met as written and no section 5 red flag is hit, but the header's clean claim is false for untracked golden inputs. F2: the served file in the shared working tree is not HEAD's, but HEAD code cannot produce it, so the commit is not its cause. If F2 is still in place at the M3 gate, it becomes a blocker, because the served file would violate the T-090 AC.

Working-tree state at review time (not the commit): `git status --porcelain -- evals/reports/calibration.json` gives ` M evals/reports/calibration.json`. The file was rewritten at 2026-11-02T05:27:16Z by a live claude-cli run (header backend claude-cli, source_tree_clean false). In the project tree, `pytest -q tests/unit -k "calibration or eval_runner"` gives 2 failed, 122 passed. At 4c5f9bf in the clone it gives 124 passed. Who ran that writer is not determinable from the files; see the orchestrator note in the JSON.

## Findings

- **F1 (major) Untracked inputs are invisible to the clean check, so the header can claim a clean HEAD for numbers HEAD cannot reproduce.** evals/run.py:77 uses `git status --porcelain --untracked-files=no`. Repro: artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh and its log. With an untracked evals/golden/case_zz_untracked pair, `--write-calibration` writes source_tree_clean true, source_tree 4b4960da, case_count 11, verified 91/92 (was 83/84), and `git ls-tree -r --name-only 4b4960da | grep -c case_zz` is 0.
- **F2 (major) Working-tree served calibration.json was overwritten after the commit by a run that HEAD code cannot produce.** Repro: `git status --porcelain -- evals/reports/calibration.json`; header read with python -I (generated_at 05:27:16Z, backend claude-cli, source_tree_clean false); `ls evals/reports/runs` shows 20261102T052638Z. Code path: the write needs --write-calibration past evals/run.py:1159 and 1170 to 1174, which refuse clean=False; plain runs write only runs/<ts>/ (evals/run.py:1026 to 1032).
- **F3 (minor) --write-calibration with --controls silently writes nothing.** evals/run.py:1165 returns before the write at 1176, with no message.
- **F4 (minor) Live runs: the calibration scratch copy and the run artifacts land in different directories.** evals/run.py:1164 sets the run ts before the run; :917 sets generated_at after run_cases (:889); :1021 names the scratch dir from generated_at; :923 points run_artifacts at the main ts dir. Observed: runs/20261102T052638Z versus report 20261102T052716Z.md, 38 s apart. Reasoned from code and observed dir names; no live backend was run.
- **F5 (minor) Refusal names no dirty file, and the normal sequence trips it.** Clone: after a successful --write-calibration, `git status --porcelain --untracked-files=no` lists M evals/reports/calibration.json and M evals/reports/latest.json, so the next --write-calibration returns rc 2 with a generic message (evals/run.py:1011 to 1012).
- **F6 (minor) Test gap: the no-git refusal reason is not asserted.** tests/unit/test_eval_runner.py:682 to 685 asserts only `is not None`. Mutant M8 (drop `or src.get("clean") is None` at evals/run.py:1009) survives; with it gone a no-git tree is refused with the wrong reason "uncommitted changes" (`not None` is True at :1011).
- **F7 (nit) Broad except in git_source.** evals/run.py:80 `except Exception:` turns a missing git binary, a timeout and a corrupt repo into the same "no git repository" state. Still fail-closed, so not a blocker.

## What is right

- Plain runs never touch the committed file: M1 is killed by three tests, and the archive and clone sha checks held.
- The pre-run refusal happens before the pipeline runs: M2 is killed by both parametrized cases.
- The post-run header recheck covers a tree dirtied during a run: M3 and M7 are killed by test_write_calibration_rechecks_the_header_after_the_run.

## Exercised (commands and results)

- `git show --stat 4c5f9bf`; `git show 4c5f9bf -- evals/run.py tests/unit/test_eval_runner.py`; read evals/run.py (HEAD lines 71 to 80, 318 to 352, 887 to 930, 1006 to 1184) and the T-101 test hunks; `python3 tools/board.py show T-101`; `git show 4c5f9bf | grep '^+' | grep -E 'except|float\(|sleep\(|retry'` returned no lines.
- Archive copy: `git archive 4c5f9bf | tar -x -C <scratchpad>/t101/archive`; import check printed the archive path. Plain `python -m evals.run` with LLM_BACKEND, ENABLE_LIVE, LLM_FIXTURE_DIR and FIXTURE_SET unset: rc 1 (fixture ship bar not met, expected), calibration.json sha256 49d383b5... before and after, scratch copy runs/20261102T052641Z/calibration.json created. `--write-calibration` on the git-less archive: rc 2, "refused, nothing was run or written: no git repository...", output dir not created.
- Clone: `git clone --no-hardlinks /Users/arsis/zlayt-pm-project <scratch>/t101/clone` then `git checkout --detach 4c5f9bf`; HEAD 4c5f9bf909253bfffa55cb41b1350c412c56e6da, `git rev-parse HEAD^{tree}` 4b4960da2d9e52141982b125dc986f0b22344360, tracked dirty 0. `--write-calibration` on the clean clone: header as above; non-git fields identical to the b85fc1b file (python -I comparison).
- Dirty probe: appended a line to docs/RUNBOOK.md: rc 2 "the tracked tree has uncommitted changes", run-dir count unchanged, calibration sha unchanged; restored.
- Untracked probe: artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh, log beside it.
- `--write-calibration --controls` on the clean clone: no calibration write, sha unchanged, controls output only.
- `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` at 4c5f9bf (clone): 124 passed, 0 skipped, rc 0; sha unchanged.
- Same command in the project working tree: 2 failed, 122 passed (test_committed_calibration_header_names_backend_and_a_clean_source_commit: `assert ('claude-cli' == 'fixture')`; test_committed_calibration_regenerates_exactly_from_its_source_commit: verified total 85 against 84). Project calibration.json sha256 3815c6ce... before and after the run.
- Mutation: artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py, log mutation-log.txt. Baseline 124 passed; M1 to M7 KILLED; M8 SURVIVED; restored_pristine=True.
- Read-only project checks: `git status`, `shasum -a 256`, `stat`, `ps` (no evals.run process running), grep of board/activity.jsonl for 2026-11-02T05:2x events.
- Not run: any live backend, any network call.

```json
{"card": "T-101", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 4c5f9bf (evals/run.py, tests/unit/test_eval_runner.py) at HEAD 4c5f9bf; CLI only, no app URL; sample case evals/golden/sample.txt via the fixture backend; shared project working tree also observed (F2)",
 "exercised": ["git show --stat and git show of 4c5f9bf (evals/run.py, test_eval_runner.py); board show T-101",
  "read evals/run.py HEAD lines 71-80, 318-352, 887-930, 1006-1184 and the T-101 test hunks; grep of the diff for except, float(, sleep(, retry: no added lines",
  "archive copy of 4c5f9bf (no .git): plain evals.run rc 1 (fixture ship bar), calibration.json sha256 unchanged, scratch runs/<ts>/calibration.json written; --write-calibration rc 2 with 'no git repository' reason and nothing written",
  "clone at 4c5f9bf (tree 4b4960da): --write-calibration on clean tree writes header source_commit 4c5f9bf, source_tree_clean true, source_tree 4b4960da, non-git fields equal to b85fc1b file",
  "clone dirty probe (docs/RUNBOOK.md edit): --write-calibration rc 2, nothing run or written; plain run leaves calibration sha unchanged",
  "untracked golden-case probe (artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh + .log): header clean true, counts 91/92 with case not in source_tree",
  "--write-calibration --controls on clean clone: no calibration write",
  "pytest -q tests/unit -k 'calibration or eval_runner' at 4c5f9bf in clone: 124 passed, 0 skipped; in project working tree: 2 failed, 122 passed",
  "mutation driver artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py, log mutation-log.txt: baseline 124 passed; M1-M7 killed; M8 survived; run.py restored byte-identical",
  "read-only project checks: git status, shasum, stat, ps, board/activity.jsonl grep for 05:2x events; no live backend, no network"],
 "verdict": "changes",
 "scores": {"plain_run_isolation": 5, "write_guard_refusal": 4, "provenance_header": 2, "test_strength": 4, "cli_surface": 3},
 "findings": [
  {"severity": "major",
   "title": "Untracked inputs are invisible to the clean check, so the header can claim a clean HEAD for numbers HEAD cannot reproduce",
   "evidence": "evals/run.py:77 `git status --porcelain --untracked-files=no`; repro artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh and .log: with untracked evals/golden/case_zz_untracked.{txt,expected.json} in a clean clone of 4c5f9bf, --write-calibration writes source_tree_clean true, source_tree 4b4960da..., case_count 11, verified 91/92 (clean run 83/84), and `git ls-tree -r --name-only 4b4960da | grep -c case_zz` prints 0",
   "why_it_matters": "T-090 requires the served calibration.json to be regenerable from the header's clean source. Here the header names a clean HEAD tree for counts produced from a golden case that tree does not contain. The AC is met as written (dirty tracked tree refused), so this is not a literal AC failure; it is a false provenance claim in the file the app serves. The project has a recorded incident of untracked files breaking HEAD (memory/LESSONS.md:26). Rated major, not blocker: no section 5 red flag, and the trigger needs a human to add untracked golden inputs.",
   "fix": "Treat any untracked path outside evals/reports/ as dirty (for example `git ls-files --others --exclude-standard -- app tests evals/golden spec docs`) and refuse. Exclude evals/reports/ because plain runs write untracked reports there (observed). Alternatively record an untracked_inputs list in the header and refuse when it is non-empty. The existing test 'untracked files do not count' (repo-root untracked.txt) must change with the rule.",
   "acceptance_test": "Probe script exits 2 with nothing written when an untracked file exists under evals/golden or app; still writes when only evals/reports/* is untracked; the untracked-file test in test_write_calibration_follows_real_git_cleanliness is updated to these cases."},
  {"severity": "major",
   "title": "Working-tree served calibration.json was overwritten after the commit by a run that HEAD code cannot produce",
   "evidence": "`git status --porcelain -- evals/reports/calibration.json` -> ' M evals/reports/calibration.json'; python -I read of the file: generated_at 2026-11-02T05:27:16Z, backend claude-cli, source_tree_clean false; evals/reports/latest.json generated_at 05:27:16Z backend claude-cli; evals/reports/runs/20261102T052638Z exists. Project pytest -k calibration: 'assert (claude-cli == fixture)' in test_committed_calibration_header_names_backend_and_a_clean_source_commit; clone at 4c5f9bf: 124 passed. HEAD write path is guarded at evals/run.py:1159 and 1170-1174 (refuse clean=False); plain runs write only runs/<ts>/ (evals/run.py:1026-1032).",
   "why_it_matters": "This is the incident T-101 exists to stop: a dirty live run replaced the served file with a claude-cli header that is not reproducible from a clean commit. Two T-090/T-101 tests are red in the tree the team works from. The commit is not the cause (HEAD code refuses this write), so the writer ran other code or bypassed the guard; the files do not say which. Rated major: the commit is correct and the file sits outside it. Upgrade to blocker if it is still in place at the M3 gate, because the served file would then violate the T-090 AC.",
   "fix": "Confirm no evals.run process is running (ps showed none at review time), restore the HEAD copy with git checkout -- evals/reports/calibration.json, and identify the writer from runs/20261102T052638Z and its log. Add a check that refuses to serve a calibration.json whose header backend or source_tree_clean is not the pinned one.",
   "acceptance_test": "`git status --porcelain -- evals/reports/calibration.json` is empty; sha256 equals HEAD's 49d383b5...; `.venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner'` run in the project working tree passes with 0 failed."},
  {"severity": "minor",
   "title": "--write-calibration combined with --controls silently writes nothing",
   "evidence": "evals/run.py:1159-1163 guard, then :1165 `if a.controls: return run_controls_only(...)` precedes the write at :1176; clone repro: `evals.run --write-calibration --controls` on a clean clone exits with the controls result and prints no calibration message; calibration.json sha unchanged",
   "why_it_matters": "A user who asks for a calibration write gets an exit code and no file, with no message that the flag was ignored.",
   "fix": "Refuse the combination before any run with exit 2 and a message, or write the calibration in controls mode.",
   "acceptance_test": "`evals.run --write-calibration --controls` exits 2, runs nothing, and writes nothing."},
  {"severity": "minor",
   "title": "Live runs: calibration scratch copy and run artifacts land in different run directories",
   "evidence": "evals/run.py:1164 sets the main ts before the run and passes it as runs_dir (:1167 onward); :917 sets generated_at after run_cases (:889); :1021 names the scratch dir from generated_at; :923 points run_artifacts at the main ts dir. Observed: runs/20261102T052638Z (live artifacts) against report 20261102T052716Z.md, 38 s apart.",
   "why_it_matters": "A reader following run_artifacts in the report will not find the calibration copy written for the same live run.",
   "fix": "Compute one ts in main and pass it to build_report and write_report, or write the calibration scratch copy into runs_dir.",
   "acceptance_test": "A live-backend test with a faked provider asserts that the report's run_artifacts directory contains calibration.json."},
  {"severity": "minor",
   "title": "Refusal names no dirty file, and the normal sequence trips it",
   "evidence": "clone: after a successful --write-calibration, `git status --porcelain --untracked-files=no` lists ' M evals/reports/calibration.json' and ' M evals/reports/latest.json'; the next --write-calibration returns rc 2 with 'the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files)' (evals/run.py:1011-1012). Every run also rewrites tracked latest.json (write_report).",
   "why_it_matters": "The operator cannot tell which file blocked the write, and a plain run followed by --write-calibration is refused by default.",
   "fix": "List the dirty paths in the refusal text; decide explicitly whether the run-rewritten latest.json should count toward dirtiness.",
   "acceptance_test": "The refusal text contains each dirty tracked path; a test asserts a path name appears in the message."},
  {"severity": "minor",
   "title": "Test gap: the no-git refusal reason is not asserted",
   "evidence": "tests/unit/test_eval_runner.py:682-685 asserts only `is not None` for the no-git case. Mutant M8 (drop `or src.get(\"clean\") is None` at evals/run.py:1009) SURVIVED in artifacts/review-evidence/T-101-staff-engineer/mutation-log.txt; without the clause a no-git tree is refused with the reason 'uncommitted changes' because `not None` is True at evals/run.py:1011.",
   "why_it_matters": "The wrong reason is shown to the operator and nothing catches it.",
   "fix": "Assert the reason text: 'no git repository' in the no-git case.",
   "acceptance_test": "Mutant M8 is killed by the T-101 selection."},
  {"severity": "nit",
   "title": "Broad except in git_source collapses every failure into the no-git state",
   "evidence": "evals/run.py:80 `except Exception:` returns {'commit': None, ...}; a missing git binary, a timeout and a corrupt repo look the same.",
   "why_it_matters": "The refusal stays fail-closed, so this is not a blocker, but the message can point at the wrong cause.",
   "fix": "Catch OSError and subprocess.SubprocessError only.",
   "acceptance_test": "A test with git replaced by a missing binary reports the OS error reason."}
 ],
 "whats_right": ["Plain runs never write the committed calibration.json: sha256 unchanged in the archive copy and the dirty clone; mutant M1 is killed by three tests",
  "The pre-run refusal happens before the pipeline runs: mutant M2 is killed by both parametrized cases, and the dirty probe ran nothing",
  "The post-run header recheck closes the dirtied-during-run gap: mutants M3 and M7 are killed by test_write_calibration_rechecks_the_header_after_the_run"],
 "questions_for_chris": ["Should --write-calibration be limited to the recorded fixture backend? Today any backend that passes the tree check can overwrite the served calibration.json (evals/run.py:1176); the T-101 handoff notes the tests pin fixture but the code does not."]}
```
