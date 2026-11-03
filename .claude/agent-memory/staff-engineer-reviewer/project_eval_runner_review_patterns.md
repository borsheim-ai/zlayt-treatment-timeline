---
name: eval-runner-review-patterns
description: T-038 r1-r2 eval runner (evals/run.py) review patterns: test doubles hiding real key shapes, bar-level mutation coverage, scratch-copy mutation method for eval tests
metadata:
  type: project
---

Eval runner (`evals/run.py`, ship bar, check-spec, check-fresh) reviews, T-038 r1 (commit 40c882d) and r2 (HEAD 5542dfd).

- **Fake pipeline shape can hide a real key mismatch.** `tests/unit/test_eval_runner.py` `Perfect.run_case` builds records with `source_label`, but the real `app/backend/pipeline.py` `case_view` (line ~331) returns the ingest records with `source`. The grounding check (`evals/run.py:278`) compares against `source_label`, so every entry fails on the real pipeline (56/56 provider failures on fixture). Fail-closed, but bar 1 can never pass. Lesson: when a test double stands in for a pipeline, diff its output keys against `run_case`'s real keys (print `sorted(out['records'][0])`).
  **Why:** the fake and the test both passed; only a real run exposed it.
  **How to apply:** for any eval or contract test double, add one test that runs the real `run_case` on the sample and asserts the harness's own checks give no failures.

- **Bar-level mutations are the right kill test.** T-038 r1 had per-bar assertions missing; r2 added `bars[name] is False` tests and all six listed mutations die. Still open: a removed `runs == 3` term in bar 4 survives because the blocker list catches it (bars and blockers can disagree).
  **How to apply:** after any bar or gate change, mutate each bar term and require a test that asserts that bar, not just `ship_bar_met`.

- **Method (scratch copy):** copy `app/ evals/ tests/ spec/ docs/ memory/` into the scratchpad (not `.env`; `memory/contracts/api.md` is read by tests, so `memory/` must be included). For each mutation, assert the target string occurs exactly once, write the mutated `run.py`, run `pytest tests/unit -q -k eval`, then restore and diff against the repo file.

- **Repo moves during review.** HEAD advanced twice mid-review (T-051 guard, then other commits) and the eval test count changed 37 to 38. Re-sync the scratch copy from HEAD before mutation runs and quote the HEAD sha.

- **The eval CLI writes into `evals/reports/`** (untracked, overwrites `latest.json`). Say so in the review when running the brief's commands.

- Model discrepancy: the dossier expects `claude-sonnet-5-5`, but the environment runs as `claude-haiku-5-5`. The review record uses what I actually run as.

See also [[project_wiring_review_patterns]] (grep callers, run the producer) and [[project_llm_stage_review_patterns]] (shared fixtures, pin HEAD by sha).

## T-038 r3 (commit 7364096) — addendum
- **Fix verified by reverting it.** Reverting `first["source"]` to `source_label` fails three tests, including the real-`run_case` test. A real-run test needs a negative control (inject a wrong provider, expect a failure) or it can be vacuous.
- **The fix chose the internal shape, not the API shape.** `run_case` records use `source` (store.py:26); the API record view and `memory/contracts/api.md` use `source_label` (present.py:132). The eval never imports `present`, so the API mapping is untested. Check the docstring claim that a function "is the shape the eval reads" against the real output.
- **Pin the review to the commit.** HEAD moved mid-review and the working tree was dirty with another agent's uncommitted `evals/run.py`. Use `git archive <sha> | tar -x -C <scratch>` and run everything there. Report working-tree results separately.
- **Check the CLI with `--out <scratch>`.** It writes `latest.json` into `--out`, not into the repo's `evals/reports/`.
- **Tools path:** `board.py` lives at `tools/board.py`, not the repo root. `validate <review.md>` returns `ok`.
- See [[project_wiring_review_patterns]] for the same "fake hides the real shape" failure mode.
