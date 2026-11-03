# Subagent: QA: T-101 r2 (QA: T-101 r2)

Source: `agent-a6fb1fd46d35a9e14.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:33:48.446Z

You own board card T-101, round 2 (claimed by "qa") in /Users/arsis/zlayt-pm-project. Read reviews/T-101-staff-engineer.md.

1. The `--write-calibration` clean check must also refuse when untracked files exist under the eval's inputs: app/, evals/, tests/fixtures/ and prompts. Use `git status --porcelain --untracked-files=all` on those paths.
2. The shared-tree evals/reports/calibration.json was overwritten by a claude-cli run at 05:27Z. Find out why: did that run use an evals/run.py from before 4c5f9bf, or does a live run bypass the guard? Close any path that writes the committed file without `--write-calibration`, then restore the file from HEAD with `git show HEAD:evals/reports/calibration.json > evals/reports/calibration.json`.
3. Fix the second major and the cheap minors.

Run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Commit with `git add <paths>` and then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-101 in_review --agent qa`. Reply in 1 line.

### User / tool · 2026-11-02T05:33:48.452Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:50.681Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-101 && echo ---- && cat reviews/T-101-staff-engineer.md && echo ---- && git log --oneline -8 && git status --porcelain | head -40",
 "description": "Show card, review, git log and status"
}
````

### User / tool · 2026-11-02T05:33:50.880Z

**tool result**
````
---
id: "T-101"
title: "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"
milestone: "M3"
role: "qa"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:21:08Z"
updated_at: "2026-11-02T05:33:44Z"
claimed_by: "qa"
claimed_at: "2026-11-02T05:33:44Z"
rounds: 1
commits: ["4c5f9bf"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-101-staff-engineer.md", "at": "2026-11-02T05:33:44Z"}
ac:
  - {"n": 1, "text": "Plain 'python -m evals.run' leaves evals/reports/calibration.json untouched; --write-calibration refuses on a dirty tree; test", "done": true, "evidence": "tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T05:21:14Z qa: claimed
- 2026-11-02T05:24:59Z qa: AC 1 checked: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed
- 2026-11-02T05:25:00Z qa: moved in_progress -> in_review
- 2026-11-02T05:25:05Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T05:33:44Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-101-staff-engineer.md; round 1; findings:
    - [major] Untracked inputs are invisible to the clean check, so the header can claim a clean HEAD for numbers HEAD cannot reproduce — fix: Treat any untracked path outside evals/reports/ as dirty (for example `git ls-files --others --exclude-standard -- app tests evals/golden spec docs`) and refuse. Exclude evals/reports/ because plain runs write untracked reports there (observed). Alternative
    - [major] Working-tree served calibration.json was overwritten after the commit by a run that HEAD code cannot produce — fix: Confirm no evals.run process is running (ps showed none at review time), restore the HEAD copy with git checkout -- evals/reports/calibration.json, and identify the writer from runs/20261102T052638Z and its log. Add a check that refuses to serve a calibration.json whose
    - [minor] --write-calibration combined with --controls silently writes nothing — fix: Refuse the combination before any run with exit 2 and a message, or write the calibration in controls mode.
    - [minor] Live runs: calibration scratch copy and run artifacts land in different run directories — fix: Compute one ts in main and pass it to build_report and write_report, or write the calibration scratch copy into runs_dir.
    - [minor] Refusal names no dirty file, and the normal sequence trips it — fix: List the dirty paths in the refusal text; decide explicitly whether the run-rewritten latest.json should count toward dirtiness.
    - [minor] Test gap: the no-git refusal reason is not asserted — fix: Assert the reason text: 'no git repository' in the no-git case.
- 2026-11-02T05:33:44Z qa: claimed

## Handoff
What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-calibration writes out/calibration.json with the T-090 header (source_commit, source_tree_clean, source_tree, hashes, backend), refused (exit 2, nothing run) unless the tracked tree is clean at HEAD, re-checked after the run. Tests: tests/unit/test_eval_runner.py (+6 new, 4 updated for the new location). How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed, 0 skipped; committed calibration.json is byte-identical to HEAD (restored and still identical after the run); real CLI plain run to a scratch --out rc=1 (fixture ship bar, expected) with calibration untouched; --write-calibration on this dirty tree rc=2, nothing written. Left: latest.json and the .md are still written by every run as before (not in scope). Other agents' uncommitted changes in the shared tree were left alone; the commit used --only paths. Surprise: the regeneration test replays the cited commit's own code, so it accepts the old out/calibration.json location as well as the new runs/ scratch copy. Note for orchestrator: --write-calibration does not restrict backend; the committed-header test pins backend=fixture, so a live write would fail that test by design.

----
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
----
288c1d3 fix(backend): D-047 r2: attribution, hedge and approximation words the quote lacks are a 422; one wide side/negation vocabulary shared by edit, manual entry, generator and gate (T-100 r2)
690a0e3 fix(backend): billing lists every repeated summary row, skipped records make totals incomplete, BALANCE DUE accepted with or without the forward (D-049, T-083 r5)
b10bff4 fix(backend): non-English is never auto-verified (D-050): AI_TRANSLATION in compose_state; English-dominant lines stay English; Portuguese suspeita/compressao not Spanish; 244-row routing set (T-085 r4)
dd84122 fix(backend): code checks bind accept for every entry, single and batch; gate and trace recompute them from the current text (D-051, T-098 r2)
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
6bca71e fix(backend): final money-token accounting pass for billing; second balance-forward rows listed, bare figures never vanish (D-049, T-083 r4)
e63e564 docs: D-051 code checks bind accept for every item
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/case_extras.py
MM app/backend/export.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pdf_hidden.py
 M app/backend/pipeline.py
MM app/backend/store.py
MM app/backend/trace.py
 M app/frontend/batch.js
 M app/frontend/judges.js
 M app/frontend/review.css
 M app/frontend/review.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/llm/audited.py
 D app/llm/prompts/conflicts_v1.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:53.759Z

**tool call — Bash**
````
{
 "command": "git status --porcelain -- evals tests/unit/test_eval_runner.py tests/fixtures && echo ---- && git diff --stat HEAD -- evals tests/unit/test_eval_runner.py | tail -5 && echo ---- && git show --stat HEAD -- evals | tail -3 && echo ---- && git ls-files --others --exclude-standard -- evals tests | head -20 && echo ---- && ps aux | grep -c \"[e]vals.run\" ; ls /Users/arsis/zlayt-pm-project/evals/reports/runs | tail -5",
 "description": "Check status of eval and test paths and running evals"
}
````

### User / tool · 2026-11-02T05:33:54.010Z

**tool result**
````
 M evals/reports/calibration.json
 M evals/reports/latest.json
 D tests/fixtures/llm/curated/1db15db3cba3733c5e00a8732ecddb694b45c2637be29b83e3bfa35576123f24.json
 D tests/fixtures/llm/curated/b8bf558be04cc588cd8da6cbb2e7678ce1d970a0dceeb367ddc03c19ccb87729.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
?? evals/reports/20261102T024653Z.md
?? evals/reports/20261102T024822Z.md
?? evals/reports/20261102T025055Z.md
?? evals/reports/20261102T025526Z.md
?? evals/reports/20261102T030405Z.md
?? evals/reports/20261102T031209Z.md
?? evals/reports/20261102T032024Z.md
?? evals/reports/20261102T043845Z.md
?? evals/reports/20261102T051136Z.md
?? evals/reports/20261102T052638Z.md
?? evals/reports/20261102T052716Z.md
?? evals/reports/controls-20261102T043911Z.json
?? evals/reports/controls-20261102T043911Z.md
?? evals/reports/controls-20261102T044933Z.json
?? evals/reports/controls-20261102T044933Z.md
?? evals/reports/controls-20261102T045207Z.json
?? evals/reports/controls-20261102T045207Z.md
?? evals/reports/runs/20261102T042232Z/
?? evals/reports/runs/20261102T045543Z/
?? evals/reports/runs/20261102T051136Z/
?? evals/reports/runs/20261102T052638Z/
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
?? tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
?? tests/fixtures/llm/23a42e78f6f5e66dfaeda880459bbbbf14d34b4945c40aca56c2d0bd19babf84.json
?? tests/fixtures/llm/249e2de6179c20db35f047d07665f84dcea759a937141dbc2f80ca48a96692f4.json
?? tests/fixtures/llm/2f4820ea5ea9c5774b27dd8afcf0403a0dc37a88dece83f54b0e2a3d0fa4232e.json
?? tests/fixtures/llm/3733e9af1cffd2d880e638be635c69e8f375a373d0565459b80eaff265cbafc3.json
?? tests/fixtures/llm/3e5d9866924792caa21c7c7f85e3c51171cf3eeec5574edcf91fff8e262d18c4.json
?? tests/fixtures/llm/5531d4c17591ba0eba7b53c9b8d53da065ae32be1e52c35fb5538ceeccfabe4d.json
?? tests/fixtures/llm/764f06e3d21fee9d69a75f53bb1a1d919bd7ec6bac9579c307cb2042d9a21aef.json
?? tests/fixtures/llm/797f02f51e04dd09f1acf004652ec8a2aa105516414a3c5dac8ba6cd4ee608ef.json
?? tests/fixtures/llm/8381f7e471270f341577290612b5e632b57001c8a4e510723a4ce30db944a32b.json
?? tests/fixtures/llm/841aee7dcaed94231186dfa9bf9842475586e95376a06f2f94af53bd369998bf.json
?? tests/fixtures/llm/85d33197736459f032fe7bb1dd384dcc73209e5e72dba65795250b60620bf394.json
?? tests/fixtures/llm/86e660b8e8eadd53a9ef9d5ae3a1dd79866b9ba98c86b7f9bf68002d5a68a495.json
?? tests/fixtures/llm/873a6c0cad8354fb3b42e80a85ab8b6e812da8b0c473fc75cf3f7260dc24ec76.json
?? tests/fixtures/llm/97bfd098399de12af87c0e036ad04d48eea34c170f05c03ab4dcaf77922c48bb.json
?? tests/fixtures/llm/9ed4f7caab0e3319a537824671baa6c0d4fb71d9702e6be03b92eb9568f11d34.json
?? tests/fixtures/llm/9f99a12d23992d323e1d457978e6825aae7987fc8edcd3dab1ba8627a27183d7.json
?? tests/fixtures/llm/a98447373286e02ccee0dc8eeec7065cb0873d3c8343b0f4034a9d897d61fdd6.json
?? tests/fixtures/llm/abb898ad6c1c632b482dda9c64f52fa2157113f8464907bf1e372def627aaf53.json
?? tests/fixtures/llm/b56169b3b85d07a3ca89144e8646194da8801a76211e6e7d7b31bb8665fa6791.json
?? tests/fixtures/llm/b8b5d708a3b6946046a498683b2dad1c86aef5dce698c83f8e0b8e722857f3df.json
?? tests/fixtures/llm/b8bc711085ecf208815a6af8622a5f9b0e80082cbbef4ef343914ecf00d42e19.json
?? tests/fixtures/llm/bff61a6bf929b7f1461ea489db872f72dc7e5c8313c731bf22ddcd444b08d153.json
?? tests/fixtures/llm/c2726fe104e7a43550afbd9e02190a04dd913c2fe6f7f485697df51de9bfd312.json
?? tests/fixtures/llm/curated/df6b5dea063344cd2eecff13781db6f5bb75c3f17fdac798182e389e5039a1f7.json
?? tests/fixtures/llm/d756ada7e955c231951fe248bdd77f017d1920bb25a418933a0d296b09ba755f.json
?? tests/fixtures/llm/d7a0c382ea1fc299d45ef67c5e5071e296838dec1ab7a5acca8fa953f044c0a2.json
?? tests/fixtures/llm/de9673c939251b3f1e9095de25579ff0d50cc226caaf8fdccdf2d83166dccf1a.json
?? tests/fixtures/llm/df6b5dea063344cd2eecff13781db6f5bb75c3f17fdac798182e389e5039a1f7.json
?? tests/fixtures/llm/ebaf7115d16299cb6a4c26d91527eb2ef715c7960d9166c5868aa16004f2867c.json
?? tests/fixtures/llm/ecfcc3f7497a9ed7ce57f5a4cfcd0a4702b89c1a1a4e1571ce333beb6c3ec97f.json
?? tests/fixtures/llm/f141cd5c80bec9fd02c5136e07a4b0bf2a02cf494fbc2966c2251551e7ff169b.json
?? tests/fixtures/llm/f239c8ff6129e494b8083773b19442a5d137ef3a887bbe190d82280c9c43ef4d.json
?? tests/fixtures/llm/f2d6125b1e25b686111794d7c79835de3ddbf6f577d09825bb9b5cbcef48f304.json
?? tests/fixtures/llm/f3b4eeb0d7affedf0124423deb30fd16a479a06278eed5c8b51f3073b7aac8d4.json
?? tests/fixtures/llm/f4d1c42e816e57847b95f510b1b0a4c34bd7fdec0070cb83013baab59b0cafe7.json
?? tests/fixtures/llm/f9e410231121c5839b12f1879a19ccd0aad5ee029dd5bd787ca44ae2da35f092.json
?? tests/fixtures/llm/fbc8d60d41fee0f8144b1e960526caa3ae80387018e74179bb7421b53fc0430f.json
?? tests/fixtures/llm/fea86f0dc7268d3e1b4115953801807d1e167c86315fbcbdaec0247abb6e078e.json
----
 evals/reports/calibration.json |   55 +-
 evals/reports/latest.json      | 1909 ++++++++++++++++++++++++++++++++++++++--
 2 files changed, 1843 insertions(+), 121 deletions(-)
----
----
evals/reports/20261102T023155Z.md
evals/reports/20261102T023203Z.md
evals/reports/20261102T023204Z.md
evals/reports/20261102T023208Z.md
evals/reports/20261102T023603Z.md
evals/reports/20261102T023911Z.md
evals/reports/20261102T023916Z.md
evals/reports/20261102T024348Z.md
evals/reports/20261102T024355Z.md
evals/reports/20261102T024653Z.md
evals/reports/20261102T024822Z.md
evals/reports/20261102T025055Z.md
evals/reports/20261102T025526Z.md
evals/reports/20261102T030405Z.md
evals/reports/20261102T031209Z.md
evals/reports/20261102T032024Z.md
evals/reports/20261102T043845Z.md
evals/reports/20261102T051136Z.md
evals/reports/20261102T052638Z.md
evals/reports/20261102T052716Z.md
----
0
20261102T035806Z
20261102T042232Z
20261102T045543Z
20261102T051136Z
20261102T052638Z
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:54.423Z

**tool call — Bash**
````
{
 "command": "grep -n \"def \\|git status\\|untracked\\|calibration\" evals/run.py | sed -n '1,400p' | grep -n \"\" | awk -F: '$2>=60 && $2<=130 || /calibration|git_source|write_calibration|untracked|dirty|clean/' | head -120",
 "description": "Locate git cleanliness and calibration code in run.py"
}
````

### User / tool · 2026-11-02T05:33:54.514Z

**tool result**
````
1:4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
2:5:                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
3:6:    python -m evals.run --write-calibration
4:7:                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
7:62:def ratio(num, den):
8:66:def golden_cases():
9:71:def git_source(root=ROOT):
10:73:    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
11:77:        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
12:84:def sha256_file(p):
13:88:def hashes(root=ROOT):
14:99:def split_regex_text(s):
15:103:def regex_hits(mn, text):
16:112:def product_entries(out):
17:116:def entry_found(g, prod):
24:251:def score_calibration(exp, out, unscored=None):
26:291:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
27:292:    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
29:322:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
30:323:    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
31:330:                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
32:343:    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
33:346:    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
34:347:    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
42:477:                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
78:921:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
82:960:def render_calibration(c):
84:994:    L += render_calibration(r.get("calibration"))
85:1006:def write_calibration_refusal(src):
86:1007:    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit
87:1012:        return "the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD"
88:1016:def write_report(r, outdir=REPORTS, write_calibration=False):
89:1017:    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
90:1024:    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
91:1025:        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
92:1026:        if write_calibration:
93:1027:            (outdir / "calibration.json").write_text(body)
94:1031:            (scratch / "calibration.json").write_text(body)
96:1045:    bad = check_calibration(p.parent / "calibration.json", root)
97:1047:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
98:1051:def check_calibration(path, root=ROOT):
99:1052:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
100:1063:    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
106:1124:    ap.add_argument("--write-calibration", action="store_true",
107:1125:                    help="also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)")
108:1159:    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
109:1160:        why = write_calibration_refusal(git_source())
110:1162:            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
111:1170:    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
112:1171:        cal = report.get("calibration") or {}
113:1172:        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
114:1174:            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
115:1176:    path = write_report(report, out, write_calibration=a.write_calibration)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:34:02.932Z

**tool call — Bash**
````
{
 "command": "git log -3 --format='%h %ci %an %s' -- evals/run.py && echo ---- && ls -la evals/reports/runs/20261102T052638Z/ && echo ---- && head -c 600 evals/reports/runs/20261102T052638Z/* 2>/dev/null | head -60; echo ----; grep -n '05:2[0-9]\\|05:3' board/activity.jsonl | tail -20; echo ----; ls -la --time-style=full-iso evals/reports/calibration.json evals/reports/latest.json evals/reports/05* 2>/dev/null; ls -la --time-style=full-iso evals/reports/ | tail -5",
 "description": "Inspect commit time, run dir and activity log for the 05:27 write"
}
````

### User / tool · 2026-11-02T05:34:03.064Z

**tool result**
````
4c5f9bf 2026-11-01 23:24:43 -0600 Chris Borsheim fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
b85fc1b 2026-11-01 22:48:24 -0600 Chris Borsheim fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
a850be0 2026-11-01 22:42:02 -0600 Chris Borsheim fix: restore T-090 work reverted by 2fca530
----
total 16
drwxr-xr-x@ 3 arsis  staff    96 Nov  1 23:26 .
drwxr-xr-x@ 8 arsis  staff   256 Nov  1 23:26 ..
-rw-r--r--@ 1 arsis  staff  6933 Nov  1 23:26 calibration.json
----
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 9,
   "total": 9
  },
  "verified": {
   "cases": [
    "case_01_date_formats",
    "case_02_gap_boundaries",
    "case_03_rate_and_ocr",
    "case_04_duplicates_no_amounts",
    "case_05_provider_conflict",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "case_08_diagnosis_temptation",
    "case_09_nonvisit_hides_gap",
    "sample"
   ],
   "matched": 84,
   "total": 85
  }
 },
----
2420:{"ts": "2026-11-02T05:29:40Z", "event": "claim", "agent": "backend", "card": "T-083", "text": "Billing analysis on itemized ledgers: billed, adjusted, paid, LOP/lien (code only, cited)"}
2421:{"ts": "2026-11-02T05:29:40Z", "event": "note", "agent": "orchestrator", "card": "T-083", "text": "§7.4 final round (5). If this round fails, billing ships as a cited line listing with no provider totals (scope cut). Rules: any second statement or summary row for a provider -> all listed, complete false; any skipped billing record -> totals.complete false; bare whole numbers are not money tokens unless in an amount column (D-049 definition); implement the BALANCE DUE either-way convention."}
2422:{"ts": "2026-11-02T05:30:02Z", "event": "commit", "agent": "backend", "card": "T-085", "text": "b10bff4"}
2423:{"ts": "2026-11-02T05:30:02Z", "event": "ac", "agent": "backend", "card": "T-085", "text": "AC 1 checked: tests/unit/test_d050_never_verified.py (19 tests: compose_state, extract+judge es/uncertain, flags, API run+rerun, rejudge recompose, date confirm, edit, manual entry, reclassify, batch accept refused, single accept + export) + test_language_routing_heldout.py (113: reviewer's 6 English lines en, 73 en rows 0 es / <=5% uncertain, PT lines not es, IT line D-050-only); tests/unit 1910 pass, 5 fail outside T-085; evals.run report evals/reports/20261102T052638Z.md (same 4_no_invented_facts blocker as before); commit b10bff4"}
2424:{"ts": "2026-11-02T05:30:02Z", "event": "handoff", "agent": "backend", "card": "T-085", "text": "What changed: D-050 enforced once in confidence.compose_state (ctx translated -> AI_TRANSLATION, never verified); every caller passes it (generator, flags, pipeline code flags/warnings/amounts, review"}
2425:{"ts": "2026-11-02T05:30:02Z", "event": "move", "agent": "backend", "card": "T-085", "text": "in_progress -> in_review", "status": "in_review"}
2426:{"ts": "2026-11-02T05:30:15Z", "event": "dispatch", "agent": "orchestrator", "card": "T-085", "text": "review dispatched: legal-nurse-reviewer"}
2427:{"ts": "2026-11-02T05:32:43Z", "event": "commit", "agent": "backend", "card": "T-083", "text": "690a0e3"}
2428:{"ts": "2026-11-02T05:32:43Z", "event": "ac", "agent": "backend", "card": "T-083", "text": "AC 1 checked: tests/unit/test_billing.py: 157 passed (r5: repeated summary rows listed, skipped records, BALANCE DUE either way, money-token docstring, r1-r4 probes M1-M8/E1-E5b/S1-S4)"}
2429:{"ts": "2026-11-02T05:32:43Z", "event": "handoff", "agent": "backend", "card": "T-083", "text": "r5 (final). What changed: a second statement's TOTAL CHARGES/BALANCE DUE or any repeated summary row (one record or several, same form family; byte-identical copy counts once) is listed in unreconcile"}
2430:{"ts": "2026-11-02T05:32:43Z", "event": "move", "agent": "backend", "card": "T-083", "text": "in_progress -> in_review", "status": "in_review"}
2431:{"ts": "2026-11-02T05:32:49Z", "event": "dispatch", "agent": "orchestrator", "card": "T-083", "text": "review dispatched: staff-engineer-reviewer"}
2432:{"ts": "2026-11-02T05:33:09Z", "event": "note", "agent": "backend", "card": "T-100", "text": "AC 1 evidence correction (review r1 major): at 24c18a7 the frontend 409 branch (review.js, manual.js) and the e2e half were NOT done, and e2e was not run. The frontend removal landed in T-097 (f5ddec8) and the e2e half is there too; this card cites those commits for those clauses and owns only the API, the unit tests and api.md. Test count 1834 was not reproducible from the commit; r2 evidence: .venv/bin/python -m pytest -q tests/unit at 288c1d3 + working tree = 1997 passed, 1 skipped, 5 failed (all outside T-100: test_eval_runner x2, test_provider x2 (pdf_hidden subprocess import), test_t093_eval_signature)."}
2433:{"ts": "2026-11-02T05:33:09Z", "event": "ac", "agent": "backend", "card": "T-100", "text": "AC 1 checked: API/unit/api.md at 288c1d3 (tests/unit/test_review_rules.py, test_manual_and_split.py parametrized: attribution, hedge, approximation, wide side/negation words -> 422, nothing saved, no judge call, confirm flag x2). Frontend 409 removal: T-097 f5ddec8 (not this card). e2e half: T-097 f5ddec8, not run here. Corrects the r1 evidence line."}
2434:{"ts": "2026-11-02T05:33:09Z", "event": "handoff", "agent": "backend", "card": "T-100", "text": "What changed: grounding.new_tokens is now the one vocabulary for edit, manual entry, generator and gate (code_check_failures calls it): side/negation set widened to left, right, bilateral, no, not, no"}
2435:{"ts": "2026-11-02T05:33:09Z", "event": "move", "agent": "backend", "card": "T-100", "text": "in_progress -> in_review", "status": "in_review"}
2436:{"ts": "2026-11-02T05:33:09Z", "event": "commit", "agent": "backend", "card": "T-100", "text": "288c1d3"}
2437:{"ts": "2026-11-02T05:33:17Z", "event": "dispatch", "agent": "orchestrator", "card": "T-100", "text": "review dispatched: staff-engineer-reviewer"}
2438:{"ts": "2026-11-02T05:33:44Z", "event": "review", "agent": "orchestrator", "card": "T-101", "text": "review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-101-staff-engineer.md", "persona": "staff-engineer-reviewer", "verdict": "changes", "file": "reviews/T-101-staff-engineer.md"}
2439:{"ts": "2026-11-02T05:33:44Z", "event": "claim", "agent": "qa", "card": "T-101", "text": "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"}
----
ls: unrecognized option `--time-style=full-iso'
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:34:13.651Z

**tool call — Bash**
````
{
 "command": "grep -rn \"calibration.json\\|write_calibration\\|write-calibration\" --include=*.py --include=*.sh --include=Makefile --include=*.yaml --include=*.toml --include=*.json . 2>/dev/null | grep -v \"^./.venv\\|^./board/\\|^./.claude/agent-memory\\|node_modules\" | grep -v \"evals/reports/runs\" | head -50; echo ----; head -30 evals/reports/20261102T052716Z.md | cut -c1-240; echo ----; python3 -c \"import json;d=json.load(open('evals/reports/calibration.json'));print({k:d[k] for k in d if k not in('by_state','by_type','sentences')})\"",
 "description": "Find all writers of calibration.json and inspect the 05:27 report"
}
````

### User / tool · 2026-11-02T05:34:16.219Z

**tool result**
````
artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py:4:doc = json.loads((pathlib.Path(os.getcwd()) / "evals/reports/calibration.json").read_text())
artifacts/review-evidence/T-099-staff-engineer-probe-states.py:10:REAL = pathlib.Path(os.getcwd()) / "evals" / "reports" / "calibration.json"
artifacts/review-evidence/T-099-staff-engineer-r2-mutants.py:96:print("== probes (serve verdict for a hand-edited copy of evals/reports/calibration.json at f345bc8)")
artifacts/review-evidence/T-099-staff-engineer-r2-mutants.py:97:doc = json.loads((ARCH / "evals/reports/calibration.json").read_text())
artifacts/review-evidence/T-093-r2-HEAD/evals/run.py:971:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-093-r2-HEAD/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-093-r2-HEAD/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-093-r2-HEAD/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-079-tree/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh:3:# Adds one UNTRACKED golden case (a copy of case_01) to a clean clone of 4c5f9bf, runs --write-calibration, and prints the header.
artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh:7:git checkout -q -- evals/reports/calibration.json evals/reports/latest.json
artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh:12:env -u LLM_BACKEND -u ENABLE_LIVE "$PY" -m evals.run --write-calibration > /dev/null 2>&1
artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh:13:echo "write_calibration_rc=$? (1 = ship bar not met, write still happens)"
artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh:14:"$PY" -I -c "import json; c=json.load(open('evals/reports/calibration.json')); print({k: c[k] for k in ('source_commit','source_tree_clean','source_tree','case_count')}); print('verified', c['by_state']['verified']['matched'], '/', c['by_state']['verified']['total'], ' case_zz in cases:', 'case_zz_untracked' in c['cases'])"
artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh:16:git checkout -q -- evals/reports/calibration.json evals/reports/latest.json
artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py:18:    ("M1 plain run writes the committed calibration.json",
artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py:19:     "        if write_calibration:\n", "        if True:\n"),
artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py:21:     "    if a.write_calibration:                          # T-101: refuse before any run is paid for",
artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py:24:     "    if a.write_calibration:                          # the tree can be dirtied during a long run",
artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py:30:    ("M6 --write-calibration flag not passed to write_report",
artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py:31:     "write_report(report, out, write_calibration=a.write_calibration)", "write_report(report, out)"),
artifacts/review-evidence/T-090-staff/mut-M10/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M10/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M10/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M11/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M4/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M4/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M4/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M5/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M5/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M5/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M2/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M2/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M2/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M13/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M13/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M13/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M13/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M10/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/base-head/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/base-head/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/base-head/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/base-head/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M11/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M11/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M11/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M7/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M4/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M3/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M3/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
----
# Eval report 2026-11-02T05:27:16Z

**ship_bar_met: False**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`

Blockers: 3_flags

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (237 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.965 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 0.857 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v4 seeded catch rate | 1.000 (19/19 wrong caught x3 runs; in-sample 15/15; held-out 4/4; false agree 0 []; correct accepted 14/14; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v2 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `4c5f9bf909`)

- Verified items matched the record 83/85 times in testing on the claude-cli backend (10 golden cases, small sample).
----
{'backend': 'claude-cli', 'case_count': 10, 'cases': ['sample', 'case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'case_08_diagnosis_temptation', 'case_09_nonvisit_hides_gap'], 'generated_at': '2026-11-02T05:27:16Z', 'hashes': {'app/llm/lexicon.yaml': 'a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263', 'app/llm/prompts/extract_es_v1.md': '985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb', 'app/llm/prompts/extract_v1.md': '11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2', 'app/llm/prompts/flags_v1.md': 'd5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725', 'app/llm/prompts/judge_amount_class_v1.md': 'e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8', 'app/llm/prompts/judge_conflict_v1.md': '10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa', 'app/llm/prompts/judge_conflict_v2.md': '6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6', 'app/llm/prompts/judge_conflict_v4.md': '15df87e8655a014111bbcddb2fee769d01e28149072ceea76f3f9d51fcae4649', 'app/llm/prompts/judge_faithfulness_es_v1.md': 'd51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898', 'app/llm/prompts/judge_faithfulness_v1.md': '636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b', 'app/llm/prompts/judge_flag_v1.md': '97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432', 'app/llm/prompts/judge_flag_v2.md': '7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe', 'app/llm/prompts/narrative_v1.md': '3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac', 'app/llm/prompts/split_v1.md': '9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b'}, 'match_rule': 'entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.', 'models': {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5'}, 'not_scored': {'amount': 0, 'entry': 0, 'flag': 0, 'total': 0}, 'schema': 'evals.calibration/1', 'small_sample': True, 'source': 'evals.run over the golden cases; measured counts only (D-042, scope cut 10)', 'source_commit': '4c5f9bf909253bfffa55cb41b1350c412c56e6da', 'source_tree': '4b4960da2d9e52141982b125dc986f0b22344360', 'source_tree_clean': False}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:34:29.706Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py; echo ----; tail -30 artifacts/review-evidence/T-101-staff-engineer/mutation-log.txt 2>/dev/null | cut -c1-300; echo ----; git worktree list; echo ----; ROOT_LINE=$(grep -n \"^ROOT\\|^REPORTS\" evals/run.py); echo \"$ROOT_LINE\"",
 "description": "Read reviewer mutation driver and worktree list"
}
````

### User / tool · 2026-11-02T05:34:29.815Z

**tool result**
````
"""T-101 mutation driver (staff-engineer-reviewer). Run with: <venv>/bin/python -I mutate_guard.py <clone_dir> <evidence_dir>.
Each mutant is one exact-anchor edit to evals/run.py in a scratch clone at 4c5f9bf; the anchor must occur exactly once.
Runs the T-101 selection, records the summary line and failing test names, then restores the pristine file byte for byte."""
import os
import pathlib
import subprocess
import sys

clone = pathlib.Path(sys.argv[1])
evid = pathlib.Path(sys.argv[2])
run_py = clone / "evals" / "run.py"
pristine = run_py.read_bytes()
(evid / "run.py.pristine").write_bytes(pristine)
env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET")}
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"

MUTANTS = [
    ("M1 plain run writes the committed calibration.json",
     "        if write_calibration:\n", "        if True:\n"),
    ("M2 pre-run refusal removed (pipeline runs before the guard)",
     "    if a.write_calibration:                          # T-101: refuse before any run is paid for",
     "    if False:                                        # T-101: refuse before any run is paid for"),
    ("M3 post-run header recheck removed",
     "    if a.write_calibration:                          # the tree can be dirtied during a long run",
     "    if False:                                        # the tree can be dirtied during a long run"),
    ("M4 refusal rule ignores a dirty tree",
     '    if not src["clean"]:', "    if False:"),
    ("M5 dirty check counts untracked files",
     '"status", "--porcelain", "--untracked-files=no"', '"status", "--porcelain"'),
    ("M6 --write-calibration flag not passed to write_report",
     "write_report(report, out, write_calibration=a.write_calibration)", "write_report(report, out)"),
    ("M7 header source_tree_clean hard-coded True",
     '"source_tree_clean": (source or {}).get("clean")', '"source_tree_clean": True'),
    ("M8 no-git clause dropped from refusal (message becomes 'uncommitted changes')",
     '    if src.get("commit") is None or src.get("clean") is None:', '    if src.get("commit") is None:'),
]

def run_tests():
    r = subprocess.run([PY, "-m", "pytest", "-q", "tests/unit", "-k", "calibration or eval_runner", "-p", "no:cacheprovider", "-rfE"],
                       cwd=clone, env=env, capture_output=True, text=True, timeout=900)
    lines = r.stdout.strip().splitlines()
    summary = lines[-1] if lines else "(no output)"
    fails = [l.split(" - ")[0].replace("FAILED ", "").replace("ERROR ", "") for l in lines if l.startswith(("FAILED", "ERROR"))]
    return r.returncode, summary, fails

rc, summary, _ = run_tests()
print(f"BASELINE rc={rc} | {summary}")
assert rc == 0, "baseline must be green before mutating"
for name, old, new in MUTANTS:
    text = pristine.decode()
    n = text.count(old)
    if n != 1:
        print(f"{name}: ANCHOR COUNT {n} != 1, not run")
        continue
    run_py.write_text(text.replace(old, new))
    try:
        rc, summary, fails = run_tests()
    finally:
        run_py.write_bytes(pristine)
    verdict = "KILLED" if rc != 0 else "SURVIVED"
    print(f"{name}: {verdict} | rc={rc} | {summary}")
    for f in fails:
        print(f"    failed: {f}")
restored = run_py.read_bytes() == pristine
print(f"restored_pristine={restored}")
----
BASELINE rc=0 | 124 passed, 1732 deselected in 8.02s
M1 plain run writes the committed calibration.json: KILLED | rc=1 | 3 failed, 121 passed, 1732 deselected in 8.28s
    failed: tests/unit/test_eval_runner.py::test_full_report_carries_calibration_and_write_report_emits_calibration_json
    failed: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched
    failed: tests/unit/test_eval_runner.py::test_plain_run_with_dirty_tree_still_never_writes_calibration_json
M2 pre-run refusal removed (pipeline runs before the guard): KILLED | rc=1 | 2 failed, 122 passed, 1732 deselected in 9.28s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src0]
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src1]
M3 post-run header recheck removed: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.27s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run
M4 refusal rule ignores a dirty tree: KILLED | rc=1 | 4 failed, 120 passed, 1732 deselected in 8.23s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src0]
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit
    failed: tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header
M5 dirty check counts untracked files: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.51s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header
M6 --write-calibration flag not passed to write_report: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.24s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header
M7 header source_tree_clean hard-coded True: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.36s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run
M8 no-git clause dropped from refusal (message becomes 'uncommitted changes'): SURVIVED | rc=0 | 124 passed, 1732 deselected in 8.44s
restored_pristine=True
----
/Users/arsis/zlayt-pm-project  ae76835 [main]
----
32:ROOT = pathlib.Path(__file__).resolve().parents[1]
34:REPORTS = ROOT / "evals" / "reports"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:34:37.083Z

**tool call — Bash**
````
{
 "command": "ls -la evals/reports/runs/20261102T051136Z/ evals/reports/runs/20261102T045543Z/ evals/reports/runs/20261102T042232Z/ | head -30; for f in evals/reports/20261102T051136Z.md evals/reports/20261102T052638Z.md evals/reports/20261102T052716Z.md evals/reports/20261102T043845Z.md; do echo \"== $f\"; sed -n 1,3p $f | cut -c1-200; done; echo ----; grep -n '\"ts\": \"2026-11-02T0[45]' board/activity.jsonl | grep -i \"eval\\|05:1\\|051136\\|052716\\|calib\\|claude-cli\\|LLM_BACKEND\" | cut -c1-400 | tail -30; echo ----; grep -rn \"052716\\|051136\\|052638\\|claude-cli\" board/activity.jsonl | cut -c1-300 | tail -12",
 "description": "Check other run dirs, report headers and activity for claude-cli runs"
}
````

### User / tool · 2026-11-02T05:34:37.201Z

**tool result**
````
evals/reports/runs/20261102T042232Z/:
total 312
drwxr-xr-x@ 15 arsis  staff    480 Nov  1 22:31 .
drwxr-xr-x@  8 arsis  staff    256 Nov  1 23:26 ..
-rw-r--r--@  1 arsis  staff   8065 Nov  1 22:23 case_01_date_formats.json
-rw-r--r--@  1 arsis  staff  10753 Nov  1 22:24 case_02_gap_boundaries.json
-rw-r--r--@  1 arsis  staff   7308 Nov  1 22:24 case_03_rate_and_ocr.json
-rw-r--r--@  1 arsis  staff   4347 Nov  1 22:24 case_04_duplicates_no_amounts.json
-rw-r--r--@  1 arsis  staff   6067 Nov  1 22:25 case_05_provider_conflict.json
-rw-r--r--@  1 arsis  staff   7676 Nov  1 22:25 case_06_subtle_pre_existing.json
-rw-r--r--@  1 arsis  staff   7969 Nov  1 22:26 case_07_prompt_injection.json
-rw-r--r--@  1 arsis  staff   4915 Nov  1 22:26 case_08_diagnosis_temptation.json
-rw-r--r--@  1 arsis  staff   6191 Nov  1 22:26 case_09_nonvisit_hides_gap.json
-rw-r--r--@  1 arsis  staff  17421 Nov  1 22:31 run1.json
-rw-r--r--@  1 arsis  staff  17421 Nov  1 22:31 run2.json
-rw-r--r--@  1 arsis  staff  17421 Nov  1 22:31 run3.json
-rw-r--r--@  1 arsis  staff  17424 Nov  1 22:23 sample.json

evals/reports/runs/20261102T045543Z/:
total 312
drwxr-xr-x@ 15 arsis  staff    480 Nov  1 23:04 .
drwxr-xr-x@  8 arsis  staff    256 Nov  1 23:26 ..
-rw-r--r--@  1 arsis  staff   8065 Nov  1 22:56 case_01_date_formats.json
-rw-r--r--@  1 arsis  staff  10753 Nov  1 22:57 case_02_gap_boundaries.json
-rw-r--r--@  1 arsis  staff   7308 Nov  1 22:57 case_03_rate_and_ocr.json
-rw-r--r--@  1 arsis  staff   4203 Nov  1 22:58 case_04_duplicates_no_amounts.json
-rw-r--r--@  1 arsis  staff   6067 Nov  1 22:58 case_05_provider_conflict.json
-rw-r--r--@  1 arsis  staff   7676 Nov  1 22:58 case_06_subtle_pre_existing.json
-rw-r--r--@  1 arsis  staff   7969 Nov  1 22:59 case_07_prompt_injection.json
-rw-r--r--@  1 arsis  staff   4915 Nov  1 22:59 case_08_diagnosis_temptation.json
== evals/reports/20261102T051136Z.md
# Eval report 2026-11-02T05:11:36Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
== evals/reports/20261102T052638Z.md
# Eval report 2026-11-02T05:26:38Z

**ship_bar_met: False**  backend `fixture`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
== evals/reports/20261102T052716Z.md
# Eval report 2026-11-02T05:27:16Z

**ship_bar_met: False**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
== evals/reports/20261102T043845Z.md
# Eval report 2026-11-02T04:38:45Z

**ship_bar_met: False**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
----
2363:{"ts": "2026-11-02T05:10:24Z", "event": "note", "agent": "frontend", "card": "T-097", "text": "D-047: T-100 had NOT landed in HEAD (review.py still answers 409 needs_confirm for non-numeric/judge cases). A refused edit (422 invalid_edit) now shows its reason inline under the edit box (text kept, focus back in the box); the 409 keep-my-wording dialog (review.js showConfirm, manual.js confirmBo
2364:{"ts": "2026-11-02T05:10:24Z", "event": "ac", "agent": "frontend", "card": "T-097", "text": "AC 1 checked: tests/e2e/test_rerun_judge.py (23) + test_stepper/test_edit/test_export_ui/test_ladder_gate/test_keyboard_mobile/test_timeline + unit test_e2e_contract: 68 passed 1 skipped on clean worktree of 21b6665 (fixture backend :7899, stopped by PID); r2: panel summary + Why dialog read gate/trac
2365:{"ts": "2026-11-02T05:10:24Z", "event": "handoff", "agent": "frontend", "card": "T-097", "text": "R2 (21b6665). What changed: AI-check panel reads the gate: summary says 'N not checked, blocks export: <gate count>' and '1 edit does not match its quote, blocks export: 1'; new panel group + rail row"}
2366:{"ts": "2026-11-02T05:10:24Z", "event": "move", "agent": "frontend", "card": "T-097", "text": "in_progress -> in_review", "status": "in_review"}
2367:{"ts": "2026-11-02T05:14:12Z", "event": "review", "agent": "orchestrator", "card": "T-083", "text": "review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-083-staff-engineer-r3.md", "persona": "staff-engineer-reviewer", "verdict": "fail", "file": "reviews/T-083-staff-engineer-r3.md"}
2368:{"ts": "2026-11-02T05:14:12Z", "event": "claim", "agent": "backend", "card": "T-083", "text": "Billing analysis on itemized ledgers: billed, adjusted, paid, LOP/lien (code only, cited)"}
2369:{"ts": "2026-11-02T05:14:29Z", "event": "note", "agent": "orchestrator", "card": "T-079", "text": "Not stalled: round 2 is deliberately held until T-094 lands (conflict prompt changes cause CONFLICT_PASS_INCOMPLETE in the library packets)."}
2370:{"ts": "2026-11-02T05:14:29Z", "event": "assign", "agent": "orchestrator", "card": "T-079", "text": "assigned to qa"}
2371:{"ts": "2026-11-02T05:14:29Z", "event": "dispatch", "agent": "orchestrator", "card": "T-097", "text": "review dispatched: ux-designer-reviewer"}
2372:{"ts": "2026-11-02T05:16:16Z", "event": "commit", "agent": "frontend", "card": "T-097", "text": "f5ddec8"}
2373:{"ts": "2026-11-02T05:16:16Z", "event": "commit", "agent": "frontend", "card": "T-097", "text": "32f6c9d"}
2374:{"ts": "2026-11-02T05:16:16Z", "event": "note", "agent": "frontend", "card": "T-097", "text": "Update: T-100 (24c18a7) landed while I finished, so the 409 keep-my-wording dialog is REMOVED (review.js showConfirm, manual.js confirmBox/submit(true), .rv-confirm css, dev mock now 422); refused edits show the 422 reason under the edit box with the text kept. Since T-100 the edit route also refuse
2375:{"ts": "2026-11-02T05:16:19Z", "event": "note", "agent": "backend", "card": "T-094", "text": "Progress: design landed in working tree (code-proposed conflict candidates + J3 judge_conflict_v4 classifies; J4-disagree on model-only flags and J3-benign go to the could-not-verify tray). First live 3-run (20261102T043845Z): determinism 1.0, conflict/causation precision 1.0, recall 1.0; only blocke
2376:{"ts": "2026-11-02T05:17:45Z", "event": "review", "agent": "orchestrator", "card": "T-085", "text": "review legal-nurse-reviewer (claude-sonnet-5-5): fail — reviews/T-085-legal-nurse-r3.md", "persona": "legal-nurse-reviewer", "verdict": "fail", "file": "reviews/T-085-legal-nurse-r3.md"}
2377:{"ts": "2026-11-02T05:17:45Z", "event": "claim", "agent": "backend", "card": "T-085", "text": "Spanish-language records: original-text grounding plus labeled, judged translation"}
2378:{"ts": "2026-11-02T05:18:16Z", "event": "review", "agent": "orchestrator", "card": "T-098", "text": "review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-098-staff-engineer.md", "persona": "staff-engineer-reviewer", "verdict": "fail", "file": "reviews/T-098-staff-engineer.md"}
2379:{"ts": "2026-11-02T05:18:16Z", "event": "review", "agent": "orchestrator", "card": "T-099", "text": "review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-099-staff-engineer.md", "persona": "staff-engineer-reviewer", "verdict": "changes", "file": "reviews/T-099-staff-engineer.md"}
2380:{"ts": "2026-11-02T05:18:16Z", "event": "claim", "agent": "backend", "card": "T-098", "text": "Export gate must block human-edited items whose code checks fail (D-045b: exempt from judge, not from code checks)"}
2381:{"ts": "2026-11-02T05:18:16Z", "event": "claim", "agent": "backend", "card": "T-099", "text": "Serve calibration.json to the app (GET route, shape per T-096 note)"}
2391:{"ts": "2026-11-02T05:20:58Z", "event": "ac", "agent": "backend", "card": "T-099", "text": "AC 1 checked: tests/unit/test_calibration_route.py: 30 passed (route file alone; includes state-total hand-edit test, mutant-verified); pytest -q tests/unit -k calibration: 39 passed, 2 failed in tests/unit/test_eval_runner.py (committed-calibration tests: the uncommitted worktree evals/reports/calibra
2392:{"ts": "2026-11-02T05:20:58Z", "event": "handoff", "agent": "backend", "card": "T-099", "text": "r2 fixes (commit f345bc8, app/backend/calibration_route.py + tests/unit/test_calibration_route.py only)."}
2396:{"ts": "2026-11-02T05:21:08Z", "event": "new", "agent": "orchestrator", "card": "T-101", "text": "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)", "milestone": "M3", "role": "qa"}
2398:{"ts": "2026-11-02T05:21:14Z", "event": "claim", "agent": "qa", "card": "T-101", "text": "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"}
2399:{"ts": "2026-11-02T05:24:59Z", "event": "ac", "agent": "qa", "card": "T-101", "text": "AC 1 checked: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanlines
2401:{"ts": "2026-11-02T05:24:59Z", "event": "handoff", "agent": "qa", "card": "T-101", "text": "What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-calibration writes out/calibration.json"}
2412:{"ts": "2026-11-02T05:26:30Z", "event": "new", "agent": "orchestrator", "card": "T-102", "text": "Calibration staleness: served calibration.json must flag when its prompt hashes no longer match HEAD (before M3 gate)", "milestone": "M3", "role": "qa"}
2413:{"ts": "2026-11-02T05:29:15Z", "event": "note", "agent": "backend", "card": "T-098", "text": "r2 golden check: scanned golden cases 01-09 + sample through the fixture pipeline; 0 AI-drafted entries fail the live code checks, so the check is not weakened. Unrelated unit failures in the shared tree (test_provider*, test_t093_eval_signature, eval_runner calibration) are other workers' WIP."}
2423:{"ts": "2026-11-02T05:30:02Z", "event": "ac", "agent": "backend", "card": "T-085", "text": "AC 1 checked: tests/unit/test_d050_never_verified.py (19 tests: compose_state, extract+judge es/uncertain, flags, API run+rerun, rejudge recompose, date confirm, edit, manual entry, reclassify, batch accept refused, single accept + export) + test_language_routing_heldout.py (113: reviewer's 6 English l
2432:{"ts": "2026-11-02T05:33:09Z", "event": "note", "agent": "backend", "card": "T-100", "text": "AC 1 evidence correction (review r1 major): at 24c18a7 the frontend 409 branch (review.js, manual.js) and the e2e half were NOT done, and e2e was not run. The frontend removal landed in T-097 (f5ddec8) and the e2e half is there too; this card cites those commits for those clauses and owns only the AP
2439:{"ts": "2026-11-02T05:33:44Z", "event": "claim", "agent": "qa", "card": "T-101", "text": "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"}
----
board/activity.jsonl:1547:{"ts": "2026-11-02T02:40:38Z", "event": "claim", "agent": "qa", "card": "T-070", "text": "Live eval: evals.run honors LLM_BACKEND=claude-cli (reported backend=fixture)"}
board/activity.jsonl:1697:{"ts": "2026-11-02T02:55:46Z", "event": "ac", "agent": "qa", "card": "T-070", "text": "AC 1 checked: evals/reports/20261102T025219Z.md: backend=claude-cli (sonnet-5-5/haiku-5-5), 3 live runs measured: determinism_3run=0.0 (bar 1.0), unsupported_count_3run=0, ship_bar_met=Fa
board/activity.jsonl:1705:{"ts": "2026-11-02T02:56:04Z", "event": "note", "agent": "backend", "card": "T-059", "text": "Narrative fixtures (commit b9d3ead): curated set now includes the sample paragraph (make_curated drafts it after accept-all; 9 sentences, 0 removed; letter equal) and claude-cli re
board/activity.jsonl:1747:{"ts": "2026-11-02T03:02:22Z", "event": "claim", "agent": "qa", "card": "T-070", "text": "Live eval: evals.run honors LLM_BACKEND=claude-cli (reported backend=fixture)"}
board/activity.jsonl:1755:{"ts": "2026-11-02T03:03:19Z", "event": "note", "agent": "qa", "card": "T-070", "text": "round 2: evals/run.py normalises LLM_BACKEND (strip+lower) via normalize_backend(); unknown values exit 2 with 'unknown LLM_BACKEND' message; live guard uses normalized name. 64 tests p
board/activity.jsonl:1890:{"ts": "2026-11-02T03:29:44Z", "event": "ac", "agent": "backend", "card": "T-075", "text": "AC 2 checked: ENABLE_LIVE=1 LLM_BACKEND=claude-cli python -m evals.run --runs 3 -> evals/reports/20261102T032823Z.md determinism_3run 1.0, unsupported_count_3run 0, hallucination 40/
board/activity.jsonl:2018:{"ts": "2026-11-02T04:11:50Z", "event": "note", "agent": "qa", "card": "T-079", "text": "Built 8 packets lib08..lib15 via evals/library_build_v2.py (reuses research/library_build.py helpers; research/ untouched). research/validate_library.py passes (25 golden+library cases,
board/activity.jsonl:2045:{"ts": "2026-11-02T04:21:21Z", "event": "ac", "agent": "qa", "card": "T-079", "text": "AC 2 checked: 291 claude-cli fixtures committed (328428f); fixture replay of lib08..15: 5 packets clean, lib09 r2 / lib10 r6 / lib15 r7 honest LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS, no f
board/activity.jsonl:2073:{"ts": "2026-11-02T04:23:02Z", "event": "note", "agent": "qa", "card": "T-093", "text": "Round 2 labels fixed (45 in-sample, 15 held-out, evals/golden/judge_controls*.jsonl) BEFORE any run. Starting one live run: LLM_BACKEND=claude-cli ENABLE_LIVE=1 python3 -m evals.run --c
board/activity.jsonl:2147:{"ts": "2026-11-02T04:31:37Z", "event": "note", "agent": "qa", "card": "T-090", "text": "r2: commits 823b718 (code, tests) and 02ff244 (calibration.json from clean worktree 823b718, worktree removed). Blocker: header has source_commit, source_tree_clean, backend, hashes; te
board/activity.jsonl:2391:{"ts": "2026-11-02T05:20:58Z", "event": "ac", "agent": "backend", "card": "T-099", "text": "AC 1 checked: tests/unit/test_calibration_route.py: 30 passed (route file alone; includes state-total hand-edit test, mutant-verified); pytest -q tests/unit -k calibration: 39 passed
board/activity.jsonl:2423:{"ts": "2026-11-02T05:30:02Z", "event": "ac", "agent": "backend", "card": "T-085", "text": "AC 1 checked: tests/unit/test_d050_never_verified.py (19 tests: compose_state, extract+judge es/uncertain, flags, API run+rerun, rejudge recompose, date confirm, edit, manual entry,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:34:46.962Z

**tool call — Bash**
````
{
 "command": "git show f345bc8:evals/run.py > /scratchpad_tmp.py 2>/dev/null; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/prev\" && git show f345bc8:evals/run.py > \"$S/prev/run_f345bc8.py\" && rm -f /scratchpad_tmp.py; grep -n \"runs\\|generated_at\\|calibration.json\\|def main\\|outdir\\|REPORTS\" \"$S/prev/run_f345bc8.py\" | head -60; echo ----; git show f345bc8:evals/run.py | grep -n \"git status\" ",
 "description": "Save pre-T-101 run.py to scratchpad and grep its writers"
}
````

### User / tool · 2026-11-02T05:34:47.023Z

**tool result (error)**
````
Permission for this command was denied by a built-in Claude Code safety check, not by the user. The check stops removals that can delete far more than intended: a system, home or workspace directory, or a target it cannot resolve, such as a shell variable that, if unset or empty, turns this into `rm -rf /` or `rm -rf /*`. Only a person may approve such a removal, and no person did (the permission prompt timed out, or none was shown). The command was NOT run; do not claim it succeeded. Do not work around the check by splitting, scripting, or re-issuing the removal through another tool or shell: the check exists because a removal like this can destroy the user's data, and getting past it would not make it safe. If the text below suggests a safe rewrite, run that instead; it goes through the same check. Otherwise finish the rest of the task without this removal, tell the user what you wanted to delete and why, and leave the removal to them. What was flagged: Dangerous rm operation detected: '/scratchpad_tmp.py'

This command would remove a critical system directory. This requires explicit approval and cannot be auto-allowed by permission rules.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:34:50.336Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/prev\" && git show f345bc8:evals/run.py > \"$S/prev/run_f345bc8.py\" && grep -n \"runs\\|generated_at\\|calibration.json\\|outdir\\|REPORTS\\|git status\" \"$S/prev/run_f345bc8.py\" | head -50; echo \"scratch=$S\"",
 "description": "Save pre-T-101 run.py to scratchpad and grep writers"
}
````

### User / tool · 2026-11-02T05:34:50.454Z

**tool result**
````
30:REPORTS = ROOT / "evals" / "reports"
318:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
343:    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
461:def run_cases(pipeline, backend, cases=None, runs_dir=None):
463:    With runs_dir each case's artifact is written as <runs_dir>/<case>.json (items, states, judge codes), so a case-level miss is diagnosable."""
469:        write_run_artifact(runs_dir, name, out, name)
515:CONTROL_REPEATS = 3          # live: every control item is judged on the same three runs as R-CO-7, and the gate needs all three to agree
606:# ---------------------------------------------------------------- live-only: 3 runs on the sample
625:    across runs; LLM-derived states (every entry, amount and flag) must match; flags are compared by (type, set of cited record IDs, evidence excerpt)
653:    """Name every R-CO-7 field that differs between two runs and the items present in only one of them (so a determinism failure is diagnosable)."""
697:def write_run_artifact(runs_dir, fname, out, name=None, run=None):
698:    """Write evals/reports/runs/<ts>/<fname>.json. Refuses (raises) if anything secret-looking would be written."""
699:    if runs_dir is None:
704:    d = pathlib.Path(runs_dir)
710:def live_metrics(pipeline, backend, text, runs=3, runs_dir=None):
711:    """Exactly 3 runs are required (R-CO-7). Any other count is recorded as not_measured with the reason and can never satisfy the bar.
712:    With runs_dir each run's artifact (run1.json ..) is written there, and a mismatch lists the differing fields and items."""
713:    if runs != 3:
714:        why = f"runs={runs}; exactly 3 live runs are required"
715:        return {"determinism_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["determinism_3run"]),
716:                "unsupported_count_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["unsupported_count_3run"])}
717:    outs = [pipeline.run_case(text, backend) for _ in range(runs)]
719:        write_run_artifact(runs_dir, f"run{i}", o, "sample", i)
723:    det = {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"],
726:        det["differences"] = {f"run1_vs_run{i + 1}": diff_parts(parts[0], parts[i]) for i in range(1, runs) if sigs[i] != sigs[0]}
728:            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}
850:                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
851:                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3
856:        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
857:            blockers.append(f"{k}: {m[k].get('reason') or 'not measured over exactly 3 live runs'}")
883:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None, runs_dir=None, judge_control=None):
885:    results, outs = run_cases(pipeline, backend, cases, runs_dir)
897:        m.update(live_metrics(pipeline, backend, sample, runs, runs_dir))
913:    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
917:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
918:    if runs_dir is not None:
919:        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
937:        L.append(f"| {j.upper()} {x['prompt']} seeded catch rate | {pct(x['catch_rate'])} ({x['wrong_caught']}/{x['wrong_total']} wrong caught x{x.get('repeats', 1)} runs; {sp}; "
971:    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`", ""]
1002:def write_report(r, outdir=REPORTS):
1003:    outdir = pathlib.Path(outdir)
1004:    outdir.mkdir(parents=True, exist_ok=True)
1005:    ts = r["generated_at"].replace(":", "").replace("-", "")
1006:    (outdir / f"{ts}.md").write_text(render_md(r))
1007:    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
1009:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
1010:    return outdir / f"{ts}.md"
1013:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
1023:    bad = check_calibration(p.parent / "calibration.json", root)
1025:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
scratch=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:35:03.870Z

**tool call — Bash**
````
{
 "command": "S=$(ls -d /private/tmp/claude-501/*/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad); grep -n \"runs_dir\\s*=\\|ts = \\|write_report(\\|build_report(\\|LLM_BACKEND\\|def main\" \"$S/prev/run_f345bc8.py\" | head; echo ----; grep -n \"runs_dir\\s*=\\|ts = \\|write_report(\\|build_report(\\|def main\" evals/run.py | head; echo ----; sed -n 1155,1180p evals/run.py",
 "description": "Compare runs_dir and write logic across old and current run.py"
}
````

### User / tool · 2026-11-02T05:35:03.982Z

**tool result**
````
4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
162:        cents = None if g["value"] is None else round(g["value"] * 100)
168:    gold_cents = round(exp["totals"]["explicit_charges_total"] * 100)
208:    hits = []
270:            cents = None if g["value"] is None else round(g["value"] * 100)
291:        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]
358:    amounts = out.get("amounts") or []
359:    hits = []
461:def run_cases(pipeline, backend, cases=None, runs_dir=None):
464:    results, outs = {}, {}
----
166:        cents = None if g["value"] is None else round(g["value"] * 100)
172:    gold_cents = round(exp["totals"]["explicit_charges_total"] * 100)
212:    hits = []
274:            cents = None if g["value"] is None else round(g["value"] * 100)
295:        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]
362:    amounts = out.get("amounts") or []
363:    hits = []
465:def run_cases(pipeline, backend, cases=None, runs_dir=None):
468:    results, outs = {}, {}
559:            verdicts = [v for v, _ in calls]
----
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
        why = write_calibration_refusal(git_source())
        if why:
            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
            return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.controls:
        return run_controls_only(backend, out, ts)
    real = pipeline is None
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
        cal = report.get("calibration") or {}
        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
        if why:
            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
            return 2
    path = write_report(report, out, write_calibration=a.write_calibration)
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:35:28.901Z

**tool call — Bash**
````
{
 "command": "S=$(ls -d /private/tmp/claude-501/*/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad); grep -n '\"runs\"' \"$S/prev/run_f345bc8.py\"; echo ---; grep -n '\"runs\"' evals/run.py; echo ---; for d in 045543Z 051136Z 052638Z; do echo \"$d: $(ls evals/reports/runs/20261102T$d | wc -l) entries, $(ls evals/reports/runs/20261102T$d | grep -c '^case_')\"; done; echo ---; sed -n 1016,1032p evals/run.py",
 "description": "Check which code path creates runs dirs and scratch copies"
}
````

### User / tool · 2026-11-02T05:35:29.030Z

**tool result**
````
723:    det = {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"],
728:            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}
850:                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
851:                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3
856:        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
1139:    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
---
727:    det = {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"],
732:            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}
854:                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
855:                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3
860:        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
1029:            scratch = outdir / "runs" / ts
1168:    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
---
045543Z:       13 entries, 9
051136Z:       13 entries, 9
052638Z:        1 entries, 0
---
def write_report(r, outdir=REPORTS, write_calibration=False):
    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
    copy under outdir/runs/<ts>/ so a plain run never touches the file the app serves (T-101)."""
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = r["generated_at"].replace(":", "").replace("-", "")
    (outdir / f"{ts}.md").write_text(render_md(r))
    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
        if write_calibration:
            (outdir / "calibration.json").write_text(body)
        else:
            scratch = outdir / "runs" / ts
            scratch.mkdir(parents=True, exist_ok=True)
            (scratch / "calibration.json").write_text(body)
    return outdir / f"{ts}.md"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:35:35.008Z

**tool call — Bash**
````
{
 "command": "grep -rn \"build_report(\\|write_report(\\|from evals\\|import evals\\|evals\\.run\\|evals import run\" --include=*.py --include=*.sh --include=Makefile . 2>/dev/null | grep -v \"^./.venv\\|^./artifacts/review-evidence\\|^./.claude/agent-memory\" | cut -c1-220 | head -30",
 "description": "Find all callers of the eval report writers"
}
````

### User / tool · 2026-11-02T05:35:35.468Z

**tool result**
````
artifacts/review-evidence/T-009-adjuster-probes.py:51:    # case_06 golden records (subtle pre-existing), verbatim from evals/golden/case_06_subtle_pre_existing.txt
artifacts/review-evidence/T-079-paralegal-replay.py:4:from evals import run as R
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/matching.py:1:"""Flag matching used by evals.run and tests: a port of the reference matcher in evals/golden/check_golden.py
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:1:"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:5:    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:6:    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:26:from evals.matching import assign_detail, norm
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:541:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None):
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:566:    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:608:def write_report(r, outdir=REPORTS):
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:647:        raise CuratedFixtures("evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR un
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:653:    ap = argparse.ArgumentParser(prog="python -m evals.run")
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:666:        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:677:        print(f"evals.run: {e}", file=sys.stderr)
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:680:    report = build_report(pipeline or load_pipeline(), backend, a.runs)
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/run.py:681:    path = write_report(report, out)
artifacts/review-evidence/T-055-security-r2/head_670ed09/tools/compile_agents.py:70:        charter="Pipeline, LLM provider abstraction, generator + judges, grounding verifier, flag engines, FastAPI API. Write determinis
artifacts/review-evidence/T-055-security-r2/head_670ed09/app/llm/provider.py:99:            raise ValueError("record mode needs record_context() over text from evals/golden")
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_spec_check.py:1:"""evals.run --check-spec: REQUIREMENTS section 6 blocks vs golden export, byte-equal. T-038 AC2, R-EX-6."""
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_spec_check.py:3:from evals import run as R
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_flags_sample.py:81:    from evals.matching import assign
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_matching.py:2:from evals.matching import assign
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/_golden.py:1:"""Helpers: load golden records/expected files from evals/golden (the only test data; synthetic)."""
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_runner.py:1:"""evals.run scoring, ship bar, freshness and lexicon recall against a FAKE pipeline built from the golden answers (no model, no n
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_runner.py:5:from evals import run as R
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_runner.py:80:    return R.build_report(pipe or Perfect(backend), backend, **kw)
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_runner.py:191:    R.write_report(full, tmp_path)
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_eval_runner.py:249:    R.write_report(good, tmp_path)
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/fixtures/make_curated.py:2:excerpts. Every answer below is derived from evals/golden (sample.export.expected.txt and sample.expected.json), never from a mode
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:35:54.735Z

**tool call — Bash**
````
{
 "command": "sed -n 68,84p evals/run.py && echo ---- && sed -n 1004,1016p evals/run.py && echo ---- && sed -n 1120,1160p evals/run.py && echo ---- && git show HEAD:evals/reports/calibration.json | python3 -c \"import json,sys;d=json.load(sys.stdin);print({k:d.get(k) for k in ('backend','source_commit','source_tree','source_tree_clean','case_count','generated_at')})\" && ls prompts 2>/dev/null; git ls-files | grep -c \"^app/llm/prompts/\"",
 "description": "Read git_source, refusal, argument parsing and HEAD header"
}
````

### User / tool · 2026-11-02T05:35:54.898Z

**tool result**
````
    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]


def git_source(root=ROOT):
    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
    import subprocess
    try:
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        tree = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        return {"commit": head, "clean": not dirty, "tree": tree}
    except Exception:
        return {"commit": None, "clean": None, "tree": None}


def sha256_file(p):
----


def write_calibration_refusal(src):
    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit
    (T-090 r2: the header must name the code that produced the counts). Untracked files do not count, matching git_source()."""
    if src.get("commit") is None or src.get("clean") is None:
        return "no git repository or HEAD commit is available to name as the source"
    if not src["clean"]:
        return "the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD"
    return None


def write_report(r, outdir=REPORTS, write_calibration=False):
----
    ap.add_argument("--backend", default=None)
    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
    ap.add_argument("--out", default=str(REPORTS))
    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
    ap.add_argument("--write-calibration", action="store_true",
                    help="also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)")
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.check_fresh:
        return check_fresh(out / "latest.json")
    if a.check_spec:
        s = check_spec()
        latest = out / "latest.json"
        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
        data.update(s)
        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
        out.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
        print(json.dumps(s))
        return 0 if s["spec_matches_golden"] else 1
    try:
        refuse_curated()
    except CuratedFixtures as e:
        print(f"evals.run: {e}", file=sys.stderr)
        return 2
    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
    backend = normalize_backend(raw)
    if backend is None:
        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
              f"Nothing was run.", file=sys.stderr)
        return 2
    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
        why = write_calibration_refusal(git_source())
----
{'backend': 'fixture', 'source_commit': 'b85fc1b56386aa0d37460186b5840eec0e578642', 'source_tree': '3f014d4b5d84f8731ff464d4548e18dfce3fbd4f', 'source_tree_clean': True, 'case_count': 10, 'generated_at': '2026-11-02T04:48:31Z'}
13
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:15.749Z

**tool call — Bash**
````
{
 "command": "grep -n \"def test_\\|untracked\\|no git\\|git_source\\|write_calibration_refusal\\|write_report(\" tests/unit/test_eval_runner.py | sed -n 1,200p | grep -n \"\" | awk -F: '{print $0}' | grep -i \"calib\\|git\\|untrack\\|refus\\|write_report\\|plain\\|dirty\\|controls\" ",
 "description": "List calibration and git-related tests in eval runner tests"
}
````

### User / tool · 2026-11-02T05:36:15.840Z

**tool result**
````
5:135:def test_controls_judged_unsupported_fail_bar_4_alone():
14:196:    R.write_report(full, tmp_path)
16:216:def test_hallucination_rate_is_over_every_line_and_controls_must_pass():
21:254:    R.write_report(good, tmp_path)
24:283:def test_curated_fixture_set_is_refused_with_exit_2(tmp_path, monkeypatch, capsys):
32:367:def test_live_backend_without_enable_live_is_refused(monkeypatch, tmp_path, capsys):
33:377:def test_padded_or_mixed_case_live_backend_without_enable_live_is_refused(raw, monkeypatch, tmp_path, capsys):
38:444:def test_score_calibration_counts_matched_over_seen_per_state_and_type():
39:459:def test_score_calibration_ignores_rejected_items_and_items_without_a_state():
40:469:def test_flag_calibration_follows_flag_precision():
41:480:def test_build_calibration_pools_counts_names_cases_and_flags_small_samples():
42:495:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
50:606:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
51:611:    R.write_report(rep, tmp_path / "plain")
52:614:    R.write_report(rep, tmp_path / "committed", write_calibration=True)
53:626:def test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):
54:640:def test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):
55:643:    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": False, "tree": "b" * 40})
56:649:def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):
57:651:    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": True, "tree": "b" * 40})   # clean at the start
58:667:    {"commit": None, "clean": None, "tree": None},                    # no git at all (exported tree)
59:669:def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
60:671:    monkeypatch.setattr(R, "git_source", lambda root=None: src)
61:682:def test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit():
62:683:    assert R.write_calibration_refusal({"commit": "a" * 40, "clean": True, "tree": "b" * 40}) is None
63:684:    assert "uncommitted" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40})
64:685:    assert R.write_calibration_refusal({"commit": None, "clean": None, "tree": None}) is not None
65:688:def test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header(monkeypatch, tmp_path, good):
66:689:    """T-101 AC2/AC3 on a real repository: allowed on a clean tracked tree (untracked files do not count), refused after a tracked edit and
67:701:    real = R.git_source
68:702:    monkeypatch.setattr(R, "git_source", lambda root=None: real(repo))
69:705:        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"], R.git_source(), rep["hashes"])
70:712:    (repo / "untracked.txt").write_text("not tracked")
71:745:        pytest.skip("no git repository here (exported tree)")
72:750:def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
73:756:def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
75:770:        pytest.skip("no git repository here")
76:775:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
77:800:def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
78:817:def test_git_source_reports_commit_and_dirtiness(tmp_path):
79:825:    a = R.git_source(tmp_path)
80:828:    assert R.git_source(tmp_path)["clean"] is False
81:830:    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None, "tree": None}
82:833:def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
83:851:def test_check_fresh_fails_on_an_edited_calibration_sentence(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:17.288Z

**tool call — Bash**
````
{
 "command": "sed -n 600,750p tests/unit/test_eval_runner.py && echo ..... && sed -n 800,832p tests/unit/test_eval_runner.py",
 "description": "Read T-101 eval runner tests"
}
````

### User / tool · 2026-11-02T05:36:17.375Z

**tool result**
````
    assert un == {"entry": 1, "amount": 2, "flag": 2}                          # rejected is excluded on purpose; duplicate and stateless flags are not
    c = R.build_calibration({"sample": {"calibration": {t: {"verified": [1, 1], "needs_review": [0, 0]} for t in R.CAL_TYPES}, "calibration_unscored": un}}, "fixture")
    assert c["not_scored"] == {"entry": 1, "amount": 2, "flag": 2, "total": 5}
    assert "Not scored: 5 produced items" in c["sentences"]["overall"]["verified"]


def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
    rep = good
    c = rep["calibration"]
    assert c["backend"] == rep["backend"] and c["cases"] == rep["cases"]
    assert c["by_state"]["verified"]["total"] == sum(rep["per_case"][n]["calibration"][t]["verified"][1] for n in rep["per_case"] for t in R.CAL_TYPES)
    R.write_report(rep, tmp_path / "plain")
    assert "Calibrated confidence" in next((tmp_path / "plain").glob("2*.md")).read_text()
    assert json.loads(next((tmp_path / "plain" / "runs").glob("*/calibration.json")).read_text()) == json.loads(json.dumps(c))
    R.write_report(rep, tmp_path / "committed", write_calibration=True)
    assert json.loads((tmp_path / "committed" / "calibration.json").read_text()) == json.loads(json.dumps(c))


# ---------------------------------------------------------------- T-101: a plain run never touches the committed calibration.json
def _fake_report(monkeypatch, rep):
    monkeypatch.setattr(R, "build_report", lambda *a, **k: copy.deepcopy(rep))
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)


def test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):
    """T-101 AC1: `python -m evals.run` (default out = evals/reports) leaves evals/reports/calibration.json byte-identical and writes a scratch copy."""
    committed = tmp_path / "calibration.json"
    committed.write_text('{"sentinel": "committed file, must not change"}\n')
    monkeypatch.setattr(R, "REPORTS", tmp_path)
    _fake_report(monkeypatch, good)
    before = committed.read_bytes()
    assert R.main([]) == 0
    assert committed.read_bytes() == before
    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
    assert len(scratch) == 1 and json.loads(scratch[0].read_text()) == json.loads(json.dumps(good["calibration"]))
    assert list(tmp_path.glob("2*.md")) and (tmp_path / "latest.json").exists()


def test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):
    """T-101 AC1: a plain run is independent of git state; a dirty tree neither blocks it nor changes the committed file."""
    monkeypatch.setattr(R, "REPORTS", tmp_path)
    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": False, "tree": "b" * 40})
    _fake_report(monkeypatch, good)
    assert R.main([]) == 0
    assert not (tmp_path / "calibration.json").exists()


def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):
    """T-101: a tree dirtied during a long run must not produce a committed header that claims clean; nothing is written."""
    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": True, "tree": "b" * 40})   # clean at the start
    def dirtied_during_run(*a, **k):
        rep = copy.deepcopy(good)
        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"],
                                                 {"commit": "a" * 40, "clean": False, "tree": "b" * 40}, rep["hashes"])
        return rep
    monkeypatch.setattr(R, "build_report", dirtied_during_run)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
    assert not (tmp_path / "calibration.json").exists() and not (tmp_path / "latest.json").exists()


@pytest.mark.parametrize("src", [
    {"commit": "a" * 40, "clean": False, "tree": "b" * 40},          # tracked edits or staged changes
    {"commit": None, "clean": None, "tree": None},                    # no git at all (exported tree)
])
def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
    """T-101 AC2: --write-calibration exits 2 before the pipeline runs and writes nothing."""
    monkeypatch.setattr(R, "git_source", lambda root=None: src)
    def must_not_run(*a, **k):
        raise AssertionError("the pipeline ran although --write-calibration was refused")
    monkeypatch.setattr(R, "build_report", must_not_run)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
    assert list(tmp_path.iterdir()) == []


def test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit():
    assert R.write_calibration_refusal({"commit": "a" * 40, "clean": True, "tree": "b" * 40}) is None
    assert "uncommitted" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40})
    assert R.write_calibration_refusal({"commit": None, "clean": None, "tree": None}) is not None


def test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header(monkeypatch, tmp_path, good):
    """T-101 AC2/AC3 on a real repository: allowed on a clean tracked tree (untracked files do not count), refused after a tracked edit and
    leaves the file absent; the written header names HEAD, the clean flag, the tree and the prompt/lexicon hashes as T-090 defined them."""
    if shutil.which("git") is None:
        pytest.skip("git missing")
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "f").write_text("a")
    subprocess.run(["git", "-C", str(repo), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "x"], check=True, env=env)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    real = R.git_source
    monkeypatch.setattr(R, "git_source", lambda root=None: real(repo))
    def fake_report(*a, **k):
        rep = copy.deepcopy(good)
        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"], R.git_source(), rep["hashes"])
        return rep
    monkeypatch.setattr(R, "build_report", fake_report)
    monkeypatch.setattr(R, "load_pipeline", lambda: object())
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    out = tmp_path / "out"
    (repo / "untracked.txt").write_text("not tracked")
    assert R.main(["--write-calibration", "--out", str(out)]) == 0
    c = json.loads((out / "calibration.json").read_text())
    assert c["schema"] == "evals.calibration/1" and c["source_commit"] == head and c["source_tree_clean"] is True
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_tree"]) and c["hashes"] == good["hashes"] and c["backend"] == good["backend"]
    (out / "calibration.json").unlink()
    (repo / "f").write_text("edited, not committed")
    before = sorted(p.name for p in out.iterdir())
    assert R.main(["--write-calibration", "--out", str(out)]) == 2
    assert not (out / "calibration.json").exists()
    assert sorted(p.name for p in out.iterdir()) == before          # the refused run wrote nothing new


# ---------------------------------------------------------------- T-090 r2: the committed calibration.json is traceable and reproducible
import os, shutil, subprocess, sys
CAL = R.REPORTS / "calibration.json"


def _git(*a, cwd=None):
    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)


def _committed():
    return json.loads(CAL.read_text())


def _has_git():
    return shutil.which("git") is not None and _git("rev-parse", "--git-dir").returncode == 0


def _require_source_commit(c):
    """Skip only when this is not a git checkout at all (an exported tree).  In a repository a cited commit that is missing is a forged header: fail."""
    if not _has_git():
        pytest.skip("no git repository here (exported tree)")
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"


def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
.....
def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
    """T-101 AC2 end to end: an export of HEAD with no .git exits 2 before any run and writes nothing."""
    if shutil.which("git") is None:
        pytest.skip("git missing")
    src = tmp_path / "src"
    src.mkdir()
    tar = subprocess.run(["git", "archive", "HEAD"], cwd=R.ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
    shutil.copy(R.ROOT / "evals" / "run.py", src / "evals" / "run.py")      # the working-tree runner (T-101 is not committed yet)
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--write-calibration", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 2 and "--write-calibration refused" in r.stderr, r.stderr[-800:]
    assert not out.exists() or not any(out.iterdir())


def test_git_source_reports_commit_and_dirtiness(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git missing")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "f").write_text("a")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "-C", str(tmp_path), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
    a = R.git_source(tmp_path)
    assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
    (tmp_path / "f").write_text("b")
    assert R.git_source(tmp_path)["clean"] is False
    assert re.fullmatch(r"[0-9a-f]{40}", a["tree"])
    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None, "tree": None}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:21.620Z

**tool call — Bash**
````
{
 "command": "grep -n \"def good\\|@pytest.fixture\" -A6 tests/unit/test_eval_runner.py | head -30; grep -n \"source_tree_clean\\|source=\" evals/run.py | head; sed -n 916,924p evals/run.py",
 "description": "Inspect the good fixture and calibration source wiring"
}
````

### User / tool · 2026-11-02T05:36:21.721Z

**tool result**
````
87:@pytest.fixture(scope="module")
88:def good():
89-    return report()
90-
91-def test_perfect_run_meets_ship_bar_on_a_live_backend(good):
92-    """AC1/AC6: with every metric at its bar on a live backend ship_bar_met is true and all named metrics carry R-IDs."""
93-    assert good["blockers"] == [] and good["ship_bar_met"] is True
94-    m = good["metrics"]
322:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
349:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
1172:        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
    source = git_source()
    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
              "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
              "thresholds": THRESHOLDS, "cases": list(results)}
    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
    if runs_dir is not None:
        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
    met, bars, blockers = evaluate_report(report)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:50.177Z

**tool call — Bash**
````
{
 "command": "echo \"B=$(python3 tools/board.py note T-101 --agent qa --text 'r2: writer found? no current path writes committed calibration.json except write_report(write_calibration=True); 05:27:16 claude-cli header (source_tree_clean False, no case-artifact dir for that ts) points at a process that loaded pre-T-101 evals/run.py or called write_report with the flag, not a live run through main. Fixing: guard inside write_report (single writer), untracked inputs, controls refusal, shared run dir, dirty paths named, no-git reason asserted, narrow except. Restoring calibration.json from HEAD next.' 2>&1 | tail -1)\"; sed -n 28,36p evals/run.py",
 "description": "Record round-2 finding note on T-101 card"
}
````

### User / tool · 2026-11-02T05:36:50.321Z

**tool result**
````
B=noted on T-101
import sys

from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:51.846Z

**tool call — Read**
````
{
 "__unparsedToolInput": {
  "raw": "{\"file_path\": \"/Users/arsis/zlayt-pm-project/evals/run.py\", \"offset\": 1, , \"limit\": 12}",
  "len": 87
 }
}
````

### User / tool · 2026-11-02T05:36:51.848Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Read was called with input that could not be parsed as JSON.
You sent (first 87 of 87 bytes): {"file_path": "/Users/arsis/zlayt-pm-project/evals/run.py", "offset": 1, , "limit": 12}
Common causes: unescaped backslashes in file paths (use / or \\), unescaped control characters, or truncated output. Retry with valid JSON.</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:52.043Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "offset": 70,
 "limit": 16
}
````

### User / tool · 2026-11-02T05:36:52.052Z

**tool result**
````
70	
71	def git_source(root=ROOT):
72	    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
73	    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
74	    import subprocess
75	    try:
76	        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
77	        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
78	        tree = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
79	        return {"commit": head, "clean": not dirty, "tree": tree}
80	    except Exception:
81	        return {"commit": None, "clean": None, "tree": None}
82	
83	
84	def sha256_file(p):
85	    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:52.317Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "offset": 1004,
 "limit": 30
}
````

### User / tool · 2026-11-02T05:36:52.328Z

**tool result**
````
1004	
1005	
1006	def write_calibration_refusal(src):
1007	    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit
1008	    (T-090 r2: the header must name the code that produced the counts). Untracked files do not count, matching git_source()."""
1009	    if src.get("commit") is None or src.get("clean") is None:
1010	        return "no git repository or HEAD commit is available to name as the source"
1011	    if not src["clean"]:
1012	        return "the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD"
1013	    return None
1014	
1015	
1016	def write_report(r, outdir=REPORTS, write_calibration=False):
1017	    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
1018	    copy under outdir/runs/<ts>/ so a plain run never touches the file the app serves (T-101)."""
1019	    outdir = pathlib.Path(outdir)
1020	    outdir.mkdir(parents=True, exist_ok=True)
1021	    ts = r["generated_at"].replace(":", "").replace("-", "")
1022	    (outdir / f"{ts}.md").write_text(render_md(r))
1023	    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
1024	    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
1025	        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
1026	        if write_calibration:
1027	            (outdir / "calibration.json").write_text(body)
1028	        else:
1029	            scratch = outdir / "runs" / ts
1030	            scratch.mkdir(parents=True, exist_ok=True)
1031	            (scratch / "calibration.json").write_text(body)
1032	    return outdir / f"{ts}.md"
1033	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:53.426Z

Now the edits. First, `git_source` gets the untracked-input check and a narrow except.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:36:56.652Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "def git_source(root=ROOT):\n    \"\"\"{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.\n    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD).\"\"\"\n    import subprocess\n    try:\n        head = subprocess.run([\"git\", \"-C\", str(root), \"rev-parse\", \"HEAD\"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()\n        dirty = subprocess.run([\"git\", \"-C\", str(root), \"status\", \"--porcelain\", \"--untracked-files=no\"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()\n        tree = subprocess.run([\"git\", \"-C\", str(root), \"rev-parse\", \"HEAD^{tree}\"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()\n        return {\"commit\": head, \"clean\": not dirty, \"tree\": tree}\n    except Exception:\n        return {\"commit\": None, \"clean\": None, \"tree\": None}",
 "new_string": "# The eval's inputs (T-101 r2): the code, prompts, golden set and fixtures a number is computed from. evals/reports is output, never input.\nGIT_INPUT_PATHS = (\"app\", \"app/llm/prompts\", \"evals\", \"tests/fixtures\", \":(exclude)evals/reports\")\n\n\ndef git_source(root=ROOT):\n    \"\"\"{'commit': HEAD hash, 'clean': no tracked file differs from HEAD and no untracked file sits under GIT_INPUT_PATHS, 'tree': HEAD^{tree},\n    'dirty': the porcelain lines that make it dirty}; Nones when git is unavailable. A calibration file is only traceable when it was produced from a\n    clean tree (T-090 r2: generate in a clean worktree of HEAD). Untracked files outside the inputs (e.g. a scratch file at the repo root) do not count.\"\"\"\n    import subprocess\n\n    def git(*args):\n        return subprocess.run([\"git\", \"-C\", str(root), *args], capture_output=True, text=True, timeout=20, check=True).stdout\n    try:\n        head = git(\"rev-parse\", \"HEAD\").strip()\n        tree = git(\"rev-parse\", \"HEAD^{tree}\").strip()\n        tracked = [l for l in git(\"status\", \"--porcelain\", \"--untracked-files=no\").splitlines() if l.strip()]\n        untracked = [l for l in git(\"status\", \"--porcelain\", \"--untracked-files=all\", \"--\", *GIT_INPUT_PATHS).splitlines() if l.startswith(\"?? \")]\n    except (OSError, subprocess.SubprocessError):\n        return {\"commit\": None, \"clean\": None, \"tree\": None, \"dirty\": []}\n    dirty = tracked + untracked\n    return {\"commit\": head, \"clean\": not dirty, \"tree\": tree, \"dirty\": dirty}"
}
````

### User / tool · 2026-11-02T05:36:56.710Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:03.130Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "def write_calibration_refusal(src):\n    \"\"\"T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit\n    (T-090 r2: the header must name the code that produced the counts). Untracked files do not count, matching git_source().\"\"\"\n    if src.get(\"commit\") is None or src.get(\"clean\") is None:\n        return \"no git repository or HEAD commit is available to name as the source\"\n    if not src[\"clean\"]:\n        return \"the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD\"\n    return None\n\n\ndef write_report(r, outdir=REPORTS, write_calibration=False):\n    \"\"\"latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch\n    copy under outdir/runs/<ts>/ so a plain run never touches the file the app serves (T-101).\"\"\"\n    outdir = pathlib.Path(outdir)\n    outdir.mkdir(parents=True, exist_ok=True)\n    ts = r[\"generated_at\"].replace(\":\", \"\").replace(\"-\", \"\")\n    (outdir / f\"{ts}.md\").write_text(render_md(r))\n    (outdir / \"latest.json\").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + \"\\n\")\n    if r.get(\"calibration\"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)\n        body = json.dumps(r[\"calibration\"], indent=1, sort_keys=True) + \"\\n\"\n        if write_calibration:\n            (outdir / \"calibration.json\").write_text(body)\n        else:\n            scratch = outdir / \"runs\" / ts\n            scratch.mkdir(parents=True, exist_ok=True)\n            (scratch / \"calibration.json\").write_text(body)\n    return outdir / f\"{ts}.md\"",
 "new_string": "class CalibrationRefused(RuntimeError):\n    \"\"\"T-101 r2: write_report(write_calibration=True) was asked to write the committed calibration.json from a header that is not a clean commit.\"\"\"\n\n\ndef write_calibration_refusal(src):\n    \"\"\"T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tree at a commit: no tracked\n    file differs from HEAD and no untracked file sits under the eval's inputs (T-090 r2: the header must name the code that produced the counts).\"\"\"\n    if src.get(\"commit\") is None or src.get(\"clean\") is None:\n        return \"no git repository or HEAD commit is available to name as the source\"\n    if not src[\"clean\"]:\n        paths = [p.rstrip() for p in (src.get(\"dirty\") or [])]\n        shown = \"; \".join(paths[:10]) or \"paths not listed\"\n        more = f\"; and {len(paths) - 10} more\" if len(paths) > 10 else \"\"\n        return (f\"the tree has uncommitted changes or untracked files under the eval inputs ({shown}{more}); \"\n                \"commit, stash or remove them, or run from a clean worktree of HEAD\")\n    return None\n\n\ndef write_report(r, outdir=REPORTS, write_calibration=False, scratch_ts=None):\n    \"\"\"latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch\n    copy under outdir/runs/<scratch_ts or ts>/ so a plain run never touches the file the app serves (T-101).\n    write_calibration is judged here as well as in main(), so every caller that reaches the committed file meets the same clean-HEAD rule (T-101 r2).\"\"\"\n    if write_calibration:                         # checked before anything is written: a refused call leaves the directory as it was\n        cal = r.get(\"calibration\") or {}\n        why = \"the report has no calibration\" if not cal else write_calibration_refusal(\n            {\"commit\": cal.get(\"source_commit\"), \"clean\": cal.get(\"source_tree_clean\"), \"dirty\": []})\n        if why:\n            raise CalibrationRefused(why)\n    outdir = pathlib.Path(outdir)\n    outdir.mkdir(parents=True, exist_ok=True)\n    ts = r[\"generated_at\"].replace(\":\", \"\").replace(\"-\", \"\")\n    (outdir / f\"{ts}.md\").write_text(render_md(r))\n    (outdir / \"latest.json\").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + \"\\n\")\n    if r.get(\"calibration\"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)\n        body = json.dumps(r[\"calibration\"], indent=1, sort_keys=True) + \"\\n\"\n        if write_calibration:\n            (outdir / \"calibration.json\").write_text(body)\n        else:\n            scratch = outdir / \"runs\" / (scratch_ts or ts)\n            scratch.mkdir(parents=True, exist_ok=True)\n            (scratch / \"calibration.json\").write_text(body)\n    return outdir / f\"{ts}.md\""
}
````

### User / tool · 2026-11-02T05:37:03.200Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:04.861Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "offset": 1188,
 "limit": 30
}
````

### User / tool · 2026-11-02T05:37:04.869Z

**tool result**
````
1188	            return 2
1189	    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
1190	    if a.controls:
1191	        return run_controls_only(backend, out, ts)
1192	    real = pipeline is None
1193	    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
1194	                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
1195	    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
1196	        cal = report.get("calibration") or {}
1197	        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
1198	        if why:
1199	            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
1200	            return 2
1201	    path = write_report(report, out, write_calibration=a.write_calibration)
1202	    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
1203	    for b in report["blockers"]:
1204	        print("  blocker:", b)
1205	    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)
1206	
1207	
1208	if __name__ == "__main__":
1209	    sys.exit(main())
1210	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:11.898Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    ts = dt.datetime.now(dt.timezone.utc).strftime(\"%Y%m%dT%H%M%SZ\")\n    if a.controls:\n        return run_controls_only(backend, out, ts)\n    real = pipeline is None\n    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / \"runs\" / ts if backend in LIVE_BACKENDS else None,\n                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)\n    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)\n        cal = report.get(\"calibration\") or {}\n        why = write_calibration_refusal({\"commit\": cal.get(\"source_commit\"), \"clean\": cal.get(\"source_tree_clean\")})\n        if why:\n            print(f\"evals.run: --write-calibration refused after the run, nothing was written: {why}.\", file=sys.stderr)\n            return 2\n    path = write_report(report, out, write_calibration=a.write_calibration)",
 "new_string": "    ts = dt.datetime.now(dt.timezone.utc).strftime(\"%Y%m%dT%H%M%SZ\")\n    if a.controls:\n        return run_controls_only(backend, out, ts)\n    real = pipeline is None\n    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / \"runs\" / ts if backend in LIVE_BACKENDS else None,\n                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)\n    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)\n        cal = report.get(\"calibration\") or {}\n        why = write_calibration_refusal({\"commit\": cal.get(\"source_commit\"), \"clean\": cal.get(\"source_tree_clean\"),\n                                         \"dirty\": (git_source().get(\"dirty\") or []) if cal.get(\"source_tree_clean\") is False else []})\n        if why:\n            print(f\"evals.run: --write-calibration refused after the run, nothing was written: {why}.\", file=sys.stderr)\n            return 2\n    try:\n        path = write_report(report, out, write_calibration=a.write_calibration, scratch_ts=ts)   # one run directory: runs/<ts> (T-101 r2)\n    except CalibrationRefused as e:                  # backstop: write_report judges the header too\n        print(f\"evals.run: --write-calibration refused, nothing was written: {e}.\", file=sys.stderr)\n        return 2"
}
````

### User / tool · 2026-11-02T05:37:11.965Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:14.104Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration\n        why = write_calibration_refusal(git_source())",
 "new_string": "    if a.write_calibration and a.controls:           # T-101 r2: controls mode writes no calibration, so the combination is refused, not silently ignored\n        print(\"evals.run: --write-calibration cannot be combined with --controls (controls mode writes no calibration); nothing was run or written.\",\n              file=sys.stderr)\n        return 2\n    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration\n        why = write_calibration_refusal(git_source())"
}
````

### User / tool · 2026-11-02T05:37:14.171Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:16.407Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py",
 "old_string": "help=\"also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)\")",
 "new_string": "help=\"also write the committed calibration.json (out/calibration.json); refused unless the tree is clean at HEAD, tracked and untracked inputs alike (T-101)\")"
}
````

### User / tool · 2026-11-02T05:37:16.466Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/run.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:17.663Z

Now the tests: update the assertions that the review flagged and the one that relied on a dirty-header write, then add coverage for the new rules.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:17.979Z

**tool call — Bash**
````
{
 "command": "grep -n \"^import\\|^from\" tests/unit/test_eval_runner.py | head -20",
 "description": "Check imports at top of eval runner tests"
}
````

### User / tool · 2026-11-02T05:37:18.070Z

**tool result**
````
3:import copy, json, re
4:import pytest
5:from evals import run as R
6:from tests.unit import _golden as G
726:import os, shutil, subprocess, sys
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:19.974Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    R.write_report(rep, tmp_path / \"committed\", write_calibration=True)\n    assert json.loads((tmp_path / \"committed\" / \"calibration.json\").read_text()) == json.loads(json.dumps(c))",
 "new_string": "    clean = R.build_calibration(rep[\"per_case\"], rep[\"backend\"], rep[\"models\"], rep[\"generated_at\"], {\"commit\": \"a\" * 40, \"clean\": True, \"tree\": \"b\" * 40}, rep[\"hashes\"])\n    R.write_report({**rep, \"calibration\": clean}, tmp_path / \"committed\", write_calibration=True)     # the header must be a clean commit (T-101 r2)\n    assert json.loads((tmp_path / \"committed\" / \"calibration.json\").read_text()) == json.loads(json.dumps(clean))"
}
````

### User / tool · 2026-11-02T05:37:20.033Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:26.161Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "def test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit():\n    assert R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": True, \"tree\": \"b\" * 40}) is None\n    assert \"uncommitted\" in R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40})\n    assert R.write_calibration_refusal({\"commit\": None, \"clean\": None, \"tree\": None}) is not None",
 "new_string": "def test_write_calibration_refusal_rule_is_clean_tree_at_a_commit():\n    assert R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": True, \"tree\": \"b\" * 40}) is None\n    assert \"uncommitted\" in R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40})\n    assert \"no git repository\" in R.write_calibration_refusal({\"commit\": None, \"clean\": None, \"tree\": None})   # T-101 r2 F6: the reason, not just a refusal\n\n\ndef test_write_calibration_refusal_names_every_dirty_path_it_is_given():\n    why = R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40,\n                                       \"dirty\": [\" M evals/reports/latest.json\", \"?? evals/golden/case_zz.txt\"]})\n    assert \"evals/reports/latest.json\" in why and \"evals/golden/case_zz.txt\" in why\n    many = [f\"?? evals/golden/case_{i:02d}.txt\" for i in range(13)]\n    assert \"and 3 more\" in R.write_calibration_refusal({\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40, \"dirty\": many})\n\n\ndef test_write_report_refuses_a_dirty_header_before_writing_anything(tmp_path, good):\n    \"\"\"T-101 r2: write_report is the only writer of the committed file, so it judges the header itself; a refused call writes nothing.\"\"\"\n    dirty = copy.deepcopy(good)\n    dirty[\"calibration\"] = R.build_calibration(dirty[\"per_case\"], dirty[\"backend\"], dirty[\"models\"], dirty[\"generated_at\"],\n                                               {\"commit\": \"a\" * 40, \"clean\": False, \"tree\": \"b\" * 40}, dirty[\"hashes\"])\n    with pytest.raises(R.CalibrationRefused):\n        R.write_report(dirty, tmp_path, write_calibration=True)\n    assert list(tmp_path.iterdir()) == []\n    R.write_report(dirty, tmp_path / \"plain\")                     # a plain write of the same report is still fine: it goes to scratch\n    assert not (tmp_path / \"plain\" / \"calibration.json\").exists()\n\n\ndef test_write_calibration_is_refused_with_controls_before_anything_runs(monkeypatch, tmp_path):\n    \"\"\"T-101 r2 F3: --write-calibration --controls exits 2 with a message; nothing runs and nothing is written.\"\"\"\n    monkeypatch.setattr(R, \"git_source\", lambda root=None: {\"commit\": \"a\" * 40, \"clean\": True, \"tree\": \"b\" * 40})\n    def must_not_run(*a, **k):\n        raise AssertionError(\"controls ran although --write-calibration --controls was refused\")\n    monkeypatch.setattr(R, \"run_controls_only\", must_not_run)\n    monkeypatch.delenv(\"LLM_BACKEND\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    assert R.main([\"--write-calibration\", \"--controls\", \"--out\", str(tmp_path)]) == 2\n    assert list(tmp_path.iterdir()) == []\n\n\ndef test_scratch_copy_and_live_run_artifacts_share_one_run_directory(monkeypatch, tmp_path, good):\n    \"\"\"T-101 r2 F4: the scratch calibration.json lands in the same runs/<ts> directory the live run artifacts use.\"\"\"\n    seen = {}\n    def fake_build(*a, **k):\n        seen[\"runs_dir\"] = k.get(\"runs_dir\")\n        return copy.deepcopy(good)\n    monkeypatch.setattr(R, \"build_report\", fake_build)\n    monkeypatch.setattr(R, \"load_pipeline\", lambda: object())\n    monkeypatch.setattr(R, \"default_judge_control\", lambda backend: None)\n    monkeypatch.setenv(\"LLM_BACKEND\", \"claude-cli\")\n    monkeypatch.setenv(\"ENABLE_LIVE\", \"1\")\n    assert R.main([\"--out\", str(tmp_path)]) in (0, 1)\n    scratch = list((tmp_path / \"runs\").glob(\"*/calibration.json\"))\n    assert len(scratch) == 1 and scratch[0].parent == seen[\"runs_dir\"]"
}
````

### User / tool · 2026-11-02T05:37:26.223Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:31.546Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py",
 "old_string": "    assert R.git_source(tmp_path)[\"clean\"] is False\n    assert re.fullmatch(r\"[0-9a-f]{40}\", a[\"tree\"])\n    assert R.git_source(tmp_path / \"nowhere\") == {\"commit\": None, \"clean\": None, \"tree\": None}",
 "new_string": "    assert R.git_source(tmp_path)[\"clean\"] is False\n    assert R.git_source(tmp_path)[\"dirty\"] == [\" M f\"]\n    assert re.fullmatch(r\"[0-9a-f]{40}\", a[\"tree\"])\n    assert R.git_source(tmp_path / \"nowhere\") == {\"commit\": None, \"clean\": None, \"tree\": None, \"dirty\": []}\n\n\ndef test_git_source_counts_untracked_files_under_the_eval_inputs_only(tmp_path):\n    \"\"\"T-101 r2 F1: an untracked golden case, fixture or prompt makes the tree dirty; an untracked report or a scratch file outside the inputs does not.\"\"\"\n    if shutil.which(\"git\") is None:\n        pytest.skip(\"git missing\")\n    subprocess.run([\"git\", \"init\", \"-q\", str(tmp_path)], check=True)\n    env = {**os.environ, \"GIT_AUTHOR_NAME\": \"t\", \"GIT_AUTHOR_EMAIL\": \"t@t\", \"GIT_COMMITTER_NAME\": \"t\", \"GIT_COMMITTER_EMAIL\": \"t@t\"}\n    (tmp_path / \"evals\" / \"golden\").mkdir(parents=True)\n    (tmp_path / \"evals\" / \"reports\").mkdir(parents=True)\n    (tmp_path / \"tests\" / \"fixtures\").mkdir(parents=True)\n    (tmp_path / \"evals\" / \"golden\" / \"keep.txt\").write_text(\"k\")\n    subprocess.run([\"git\", \"-C\", str(tmp_path), \"add\", \".\"], check=True)\n    subprocess.run([\"git\", \"-C\", str(tmp_path), \"commit\", \"-qm\", \"x\"], check=True, env=env)\n    assert R.git_source(tmp_path)[\"clean\"] is True\n    (tmp_path / \"evals\" / \"reports\" / \"20990101T000000Z.md\").write_text(\"report output\")          # a run writes here: not an input\n    (tmp_path / \"scratch.txt\").write_text(\"outside the inputs\")                                   # not an input either\n    assert R.git_source(tmp_path)[\"clean\"] is True\n    (tmp_path / \"evals\" / \"golden\" / \"case_zz_untracked.txt\").write_text(\"not committed\")\n    src = R.git_source(tmp_path)\n    assert src[\"clean\"] is False and \"?? evals/golden/case_zz_untracked.txt\" in src[\"dirty\"]\n    assert \"evals/reports\" not in \" \".join(src[\"dirty\"]) and \"scratch.txt\" not in \" \".join(src[\"dirty\"])\n    assert \"case_zz_untracked\" in R.write_calibration_refusal({\"commit\": src[\"commit\"], \"clean\": False, \"tree\": src[\"tree\"], \"dirty\": src[\"dirty\"]})"
}
````

### User / tool · 2026-11-02T05:37:31.610Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:34.725Z

**tool call — Bash**
````
{
 "command": "git show HEAD:evals/reports/calibration.json > evals/reports/calibration.json && git status --porcelain -- evals/reports/calibration.json; echo \"restored rc=$?\"; shasum -a 256 evals/reports/calibration.json; git show HEAD:evals/reports/calibration.json | shasum -a 256; timeout 600 .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -p no:cacheprovider 2>&1 | tail -25",
 "description": "Restore calibration.json from HEAD and run the T-101 test selection"
}
````

### User / tool · 2026-11-02T05:37:34.893Z

**tool result**
````
restored rc=0
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  -
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:36.308Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -p no:cacheprovider 2>&1 | tail -30; echo; git status --porcelain -- evals/reports/calibration.json; shasum -a 256 evals/reports/calibration.json",
 "description": "Run the T-101 test selection and recheck calibration hash"
}
````

### User / tool · 2026-11-02T05:37:46.954Z

**tool result**
````
........................................................................ [ 55%]
.........................................................                [100%]
129 passed, 1909 deselected in 10.15s

49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:51.351Z

**tool call — Bash**
````
{
 "command": "S=$(ls -d /private/tmp/claude-501/*/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad); env -u LLM_BACKEND -u ENABLE_LIVE .venv/bin/python -m evals.run --write-calibration --out \"$S/cli_probe\" ; echo \"rc=$?\"; env -u LLM_BACKEND .venv/bin/python -m evals.run --write-calibration --controls --out \"$S/cli_probe2\"; echo \"rc=$?\"; ls \"$S/cli_probe\" \"$S/cli_probe2\" 2>&1 | head -3; .venv/bin/python -c \"import sys; sys.path.insert(0,'.'); from evals import run as R; s=R.git_source(); print(s['clean'], len(s['dirty']), s['dirty'][:3])\"",
 "description": "Probe the real CLI refusals and the live dirty list"
}
````

### User / tool · 2026-11-02T05:37:51.796Z

**tool result**
````
evals.run: --write-calibration refused, nothing was run or written: the tree has uncommitted changes or untracked files under the eval inputs ( M .claude/agent-memory/backend/project_backend_conventions.md;  M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md;  M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md;  M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md;  M .claude/agent-memory/frontend/MEMORY.md;  M .claude/agent-memory/frontend/project_stepper_panels.md;  M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md;  M .claude/agent-memory/paralegal-reviewer/MEMORY.md;  M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md;  M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md; and 96 more); commit, stash or remove them, or run from a clean worktree of HEAD.
rc=2
evals.run: --write-calibration cannot be combined with --controls (controls mode writes no calibration); nothing was run or written.
rc=2
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/cli_probe: No such file or directory
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/cli_probe2: No such file or directory
False 106 [' M .claude/agent-memory/backend/project_backend_conventions.md', ' M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md', ' M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:37:59.151Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json && git add evals/run.py tests/unit/test_eval_runner.py && git commit -q -m \"fix(qa): --write-calibration judges the header in write_report, refuses untracked inputs and --controls, shares one run dir (T-101 r2)\" -m \"- write_report(write_calibration=True) is the single writer of the committed calibration.json and refuses a non-clean header before writing anything (CalibrationRefused); main() keeps its pre- and post-run checks.\n- git_source counts untracked files under app/, app/llm/prompts, evals/ (minus evals/reports) and tests/fixtures/ as dirty; the refusal names the dirty paths.\n- --write-calibration with --controls exits 2 before any run.\n- The scratch copy lands in the same runs/<ts> directory as the live run artifacts.\n- The no-git refusal reason is asserted; git_source narrows its except to OSError and SubprocessError.\n- Tests: 5 new (untracked inputs, dirty-path naming, write_report guard, controls refusal, shared run dir); 129 passed for -k 'calibration or eval_runner'.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" -- evals/run.py tests/unit/test_eval_runner.py && git log -1 --format=%h && git status --porcelain -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json",
 "description": "Commit the two owned files with explicit paths"
}
````

### User / tool · 2026-11-02T05:37:59.222Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git diff --stat -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json && git add evals/run.py tests/unit/test_eval_runner.py && git commit -q -m "fix(qa): --write-calibration j
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:38:00.717Z

**tool call — Bash**
````
{
 "command": "git add evals/run.py tests/unit/test_eval_runner.py && git diff --cached --stat",
 "description": "Stage the two owned files with explicit paths"
}
````

### User / tool · 2026-11-02T05:38:00.842Z

**tool result**
````
 app/backend/api.py                |   2 -
 app/backend/case_extras.py        |  18 +-----
 app/backend/export.py             |   4 +-
 app/backend/store.py              |   4 --
 app/backend/trace.py              |  30 +++------
 evals/run.py                      |  68 +++++++++++++++-----
 tests/unit/_pdf_probe.py          |  66 --------------------
 tests/unit/test_eval_runner.py    |  83 +++++++++++++++++++++++--
 tests/unit/test_pdf_ocr_limits.py | 114 ----------------------------------
 tests/unit/test_trace.py          | 126 +-------------------------------------
 10 files changed, 144 insertions(+), 371 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:38:02.113Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(qa): --write-calibration judges the header in write_report, refuses untracked inputs and --controls, shares one run dir (T-101 r2)\" -m \"- write_report(write_calibration=True) is the single writer of the committed calibration.json and refuses a non-clean header before writing anything (CalibrationRefused); main() keeps its pre- and post-run checks.\n- git_source counts untracked files under app/, app/llm/prompts, evals/ (minus evals/reports) and tests/fixtures/ as dirty; the refusal names the dirty paths.\n- --write-calibration with --controls exits 2 before any run.\n- The scratch copy lands in the same runs/<ts> directory as the live run artifacts.\n- The no-git refusal reason is asserted; git_source narrows its except to OSError and SubprocessError.\n- Tests: 5 new (untracked inputs, dirty-path naming, write_report guard, controls refusal, shared run dir); 129 passed for -k 'calibration or eval_runner'.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" -- evals/run.py tests/unit/test_eval_runner.py && git log -1 --format=%h",
 "description": "Commit staged eval runner and test changes"
}
````

### User / tool · 2026-11-02T05:38:02.629Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
fdc2506
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:38:04.960Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%h %s' HEAD | tail -4 && echo ---- && git diff --cached --stat | tail -3",
 "description": "Verify commit contents and remaining staged set"
}
````

### User / tool · 2026-11-02T05:38:05.079Z

**tool result**
````
 evals/run.py                   | 68 +++++++++++++++++++++++++---------
 tests/unit/test_eval_runner.py | 83 +++++++++++++++++++++++++++++++++++++++---
 2 files changed, 129 insertions(+), 22 deletions(-)
----
 tests/unit/test_pdf_ocr_limits.py    | 114 -----------------------
 tests/unit/test_trace.py             | 126 +-------------------------
 17 files changed, 318 insertions(+), 384 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:38:12.635Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-101 --check 1 --agent qa --evidence \"r2 commit fdc2506 (evals/run.py, tests/unit/test_eval_runner.py): .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 129 passed (was 124; +5 r2 tests: test_git_source_counts_untracked_files_under_the_eval_inputs_only, test_write_report_refuses_a_dirty_header_before_writing_anything, test_write_calibration_is_refused_with_controls_before_anything_runs, test_scratch_copy_and_live_run_artifacts_share_one_run_directory, test_write_calibration_refusal_names_every_dirty_path_it_is_given); plain run leaves committed calibration.json (sha 49d383b5 unchanged)\" && $B handoff T-101 --agent qa --text \"r2 (fdc2506). Writer of the 05:27:16Z claude-cli calibration.json: not identified. Evidence: no current code path writes the committed file except write_report(write_calibration=True); no runs/<start> case dir exists for that run, so it was not a live run through main(); HEAD f345bc8 main also writes runs/<ts>. Likely an old evals/run.py or an ad hoc caller of write_report(write_calibration=True), which had no guard of its own. Closed: write_report now judges the header itself (CalibrationRefused) before any write. Restored evals/reports/calibration.json from HEAD (sha 49d383b5, clean). Round 2 items: untracked files under app/, app/llm/prompts, evals/ (minus evals/reports), tests/fixtures/ block --write-calibration; refusal names the dirty paths; --controls with --write-calibration exits 2; scratch copy shares runs/<ts> with run artifacts; no-git reason asserted; except narrowed. Verified: pytest selection 129 passed; real CLI --write-calibration refused rc 2 before any run, nothing written. What's left: (1) the served-route check (refuse a calibration whose header is not the pinned backend/clean) belongs to the backend card T-099, not here; (2) --write-calibration does not restrict backend (question for Chris); (3) latest.json is tracked and every run rewrites it, so it blocks the next --write-calibration until committed or restored (kept strict on purpose). Surprise: the shared index already held other agents' staged files; the commit used --only paths, so only my two files went in.\" && $B move T-101 in_review --agent qa && $B show T-101 | head -12",
 "description": "Record AC evidence, handoff, and move card to in_review"
}
````

### User / tool · 2026-11-02T05:38:12.948Z

**tool result**
````
AC 1 checked: r2 commit fdc2506 (evals/run.py, tests/unit/test_eval_runner.py): .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 129 passed (was 124; +5 r2 tests: test_git_source_counts_untracked_files_under_the_eval_inputs_only, test_write_report_refuses_a_dirty_header_before_writing_anything, test_write_calibration_is_refused_with_controls_before_anything_runs, test_scratch_copy_and_live_run_artifacts_share_one_run_directory, test_write_calibration_refusal_names_every_dirty_path_it_is_given); plain run leaves committed calibration.json (sha 49d383b5 unchanged)
handoff written on T-101
T-101: in_progress -> in_review
---
id: "T-101"
title: "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:21:08Z"
updated_at: "2026-11-02T05:38:12Z"
claimed_by: "qa"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:38:15.870Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-101 --sha fdc2506 --agent qa && python3 tools/board.py note T-101 --agent qa --text \"r2 done: fdc2506 committed; calibration.json restored from HEAD (clean, sha 49d383b5); trailer is Haiku 5.5 per the session attribution, not Opus 5.5 as the brief asked\" | tail -1",
 "description": "Record the round-2 commit on the card"
}
````

### User / tool · 2026-11-02T05:38:16.061Z

**tool result**
````
T-101: commit fdc2506 recorded
noted on T-101
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:38:17.858Z

T-101 r2 is in_review at fdc2506 (129 passed on the calibration/eval_runner selection; committed calibration.json restored from HEAD, sha 49d383b5). The writer of the 05:27Z file is not identified: no current path writes it except `write_report(write_calibration=True)`, which had no guard of its own, so that is now closed. The trailer is Haiku 5.5 because the session attribution names it and I am Haiku, not Opus as the brief asked.
