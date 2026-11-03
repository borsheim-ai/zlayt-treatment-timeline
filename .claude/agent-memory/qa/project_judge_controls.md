---
name: judge-controls-matched-pairs
description: How the J3/J4 seeded control sets are built (matched pairs, fixed labels, held-out split, 3 repeats) and the stable finding they produced
metadata:
  type: project
---

evals/golden/judge_controls.jsonl (in-sample) + judge_controls_heldout.jsonl; loaded by `evals.run.load_controls()`; changelog evals/golden/judge_controls.CHANGELOG.md. Generated once from a script, labels fixed BEFORE any run.

- Wrong items must share a content word with their pair (test enforces it); each matched pair has a consistent (wrong) and a contradictory (correct) item. `same_fact: true` marks consistent-value wrong items.
- A failing item is a finding, never a relabel (D-046). First relabel (J3W1 v1) was a mistake: I changed the input to fit the label; the judge was following its own rule 2.
- Gate = every wrong item caught on every one of 3 repeats (`CONTROL_REPEATS`). correct_accepted is reported, not gated; gating it needs an ADR.
- `python -m evals.run --controls` (LLM_BACKEND=claude-cli ENABLE_LIVE=1) runs only the controls, 4 worker threads, writes evals/reports/controls-<ts>.md/.json (about 8 min for 60 items x 3).
- Finding 2026-11-02: judge_conflict_v3 rule 1 says "a discharge" counts as the course ending, so J3W11 (plan 12 visits vs "completed all 12; discharged goals met") is called conflict on all 3 repeats. Keyword-follows-the-prompt defect, not a flaky item.

**Pitfalls:** `pgrep -f "evals.run --controls"` matches the watcher's own shell, so a pgrep-wait loop never ends; wait on the log file instead. evals/run.py and tests/unit/test_eval_runner.py are shared with other agents' uncommitted hunks (T-090): commit with a temp index = HEAD blob + only your patch (diff your pre-edit snapshot against the file). git-guard wants `git add` and `git commit` in separate commands.

**Round 4 (T-093, 2026-11-02):** the J3 controls are no longer hand-written. `evals/j3_controls.py` runs `conflict_candidates.candidates()` over golden+library packets (only 4 real candidates exist: sample plan/discharge, case_06 x3) and builds crafted variants; it refuses to write a pair the generator does not propose (`python -m evals.j3_controls` rebuilds the J3 rows, `--check` is the drift test; J4 rows are kept byte for byte). Why: a hand-written set of laterality/date/dose pairs was 23/29 unreachable, so the gate measured a path the product lacks. Pitfalls: the generator quotes only the matching clause (cut at ';'), and its early-end regex fires on 'discontinued'/'no longer attends'; probe a variant with a throwaway script before writing a label. Rebuild in a clean worktree (`git worktree add --detach`) and run the main .venv python with cwd there; commit with a temp `GIT_INDEX_FILE` then `git reset -q -- <my paths>` (not `reset HEAD`, git-guard blocks it).
