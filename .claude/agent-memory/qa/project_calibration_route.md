---
name: calibration-route-and-regen
description: How GET /api/calibration decides stale, how calibration.json is regenerated from a clean worktree, and the fixture-dir pitfall in score_unsplit
metadata:
  type: project
---

GET /api/calibration lives in app/backend/calibration_route.py (T-099, stale flag T-102). It serves evals/reports/calibration.json read-only.
`calibration.stale` / `stale_reason` compare the file's recorded `hashes` (prompts + lexicon, sha256) with the same files at HEAD
(`git cat-file blob HEAD:path`, cached per HEAD sha); a checkout-less copy falls back to disk. Hashes are never served.

**Why:** the served numbers must say when they describe older prompts (T-096 shows "numbers from an older version").
**How to apply:** when prompts change, regenerate before the gate. Do it in a clean worktree, not the shared tree:
`git worktree add <scratchpad>/<unique-name> HEAD`, then `.venv/bin/python -m evals.run --write-calibration --backend fixture` from
inside it (the committed file is refused from a dirty tree), copy the file back (`cmp` it), commit it, then `git worktree remove --force`.
Pick a unique worktree name: a `wt` folder already existed in the scratchpad (an old copy of the project with a .env) and was not touched.

Pitfalls:
- evals/run.py `score_unsplit` sets LLM_FIXTURE_DIR to tests/fixtures/llm/split for the unsplit case, and fixture.call does not fall back
  to the default dir when LLM_FIXTURE_DIR is set. The other LLM calls in that case miss (FIXTURE_MISS), judge_unavailable_count > 0, and
  the report shows blocker 4_no_invented_facts. Golden-case calibration counts are unaffected. Open follow-up for qa.
- The count changes between regenerations come from code as well as prompts (T-110 and others), so 83/84 became 84/85 at HEAD.
- git-guard rejects `git add ... && git commit ...` in one Bash call: stage in one call, commit in the next.
- `timeout` is not installed on this Mac; use the Bash tool's timeout parameter.
- The git-guard hook and `git commit -- <paths>` only commit the listed paths; the shared index often holds other workers' staged deletions.
