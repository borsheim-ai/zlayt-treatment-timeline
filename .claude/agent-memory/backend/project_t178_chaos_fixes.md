---
name: t178-chaos-fixes
description: T-178 GATE-M3 chaos fixes: interrupted-run recovery (store.py), stale-tab 409 (review.check_fresh), ingest.clean_chars; pitfalls
metadata:
  type: project
---

Codepaths: `ingest.clean_chars` (Cf removed, lone surrogate -> U+FFFD) is inside `normalize_text`, so the empty check, limits, demo hash, stored text and `pdf_text.assemble` all see the cleaned text; `api.body_of` runs `_clean_strings` over every JSON string (the test client cannot send a surrogate with `json=`; use `content=json.dumps(obj)`). `store.interrupt_orphaned_runs` runs in `create_app`; `store.settle_stale_run` is called by `api.get_case` (stale = no live thread in `store.LIVE_RUNS` and run older than 600 s); tests that seed `status=running` AFTER creating the app are unaffected, a test that seeds it and then creates a second app gets it failed. Error shape: `{code: run_partial, interrupted: true}`, status failed.
Stale tab: `review.check_fresh` (body `version` = item `updated_at`, and/or `expected_status`), 409 `stale_item`; same-outcome repeats pass; frontend does not send them yet.

**Why:** chaos tester found a stranded 'running' case that blocked export and re-run. **How to apply:** any new "run in progress" source must register with `store.run_started/run_ended`.

Pitfall: review.py / api.py / present.py get other agents' hunks mid-task (D-066 landed in review.py while I worked); rebuild the file from `git show HEAD:` plus only my block, `git hash-object -w`, `update-index --cacheinfo` into a temp `GIT_INDEX_FILE`. Full unit suite takes > 15 min and two at once halve the speed; run only the clean `git archive $(git write-tree)` copy (symlink .venv into it).
