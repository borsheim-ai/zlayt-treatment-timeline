---
name: t050-namespacing-review-patterns
description: T-050 (per-case id namespacing, commit 6c3aeb1) round-1 review - committed fix missing producer lines, no DB migration, delete test checks records only; how to reproduce a commit without the working tree
metadata:
  type: project
---

Recurring pattern from the T-050 review (reviews/T-050-staff-engineer.md, verdict fail, 2026-11-01).

- **A commit can be green in its own unit tests and still not run.** 6c3aeb1 changed db.py to require `case=` for ambiguous ids,
  but the producer `_persist` in app/backend/pipeline.py (HEAD lines 141, 145) still called update_item/apply_review without it.
  The fix lived only as uncommitted working-tree diff, mixed with unrelated backend WIP. test_multicase passed at HEAD because it
  calls run_pipeline on fresh case ids and never does the API order (ingest_case for B, then run B). Same family as
  [[project_wiring_review_patterns]].
- **Reproduce a committed state without the working tree:** `git archive <sha> | tar -x -C artifacts/review-evidence/<card>/<dir>`,
  then run pytest there. Before reading any red, check untracked fixtures: at review time 251 files under tests/fixtures/llm/
  were untracked, so a clean archive fails 7 API tests for reasons unrelated to the card. Compare three trees: the commit, the commit plus
  the untracked fixtures, and the commit plus the working-tree file in question.
- **Schema change with CREATE TABLE IF NOT EXISTS is not a migration.** An existing file keeps the old global PRIMARY KEY, and the
  second case dies with `IntegrityError: UNIQUE constraint failed: records.id`. Probe with the pre-change tree (git archive <sha>^)
  writing the file, then the new tree opening it. The handoff's "delete old sqlite files" is not a fix.
- **Delete-isolation tests can check one table.** test_delete_case_removes_only_that_case checked only `records`, so dropping llm_calls
  (ADR-006 prompts) from _CASE_TABLES left it green. Other tests caught it. Check the mutant against the card's own test, not the suite.
- **Mutation method that worked:** copy app/, tests/, evals/ from the working tree into artifacts/review-evidence/<card>/mut/<name>/,
  assert the pattern occurs once, apply one replacement, run the card's test files. Never edit the repo.

Reviewer environment gotchas (this card):
- `timeout` is not installed on this macOS shell; do not use it.
- The git-guard hook blocks `rm -rf $var/...` when the variable is unresolved. Use literal paths.
- HEAD moved during the review (other agents committed). Record `git rev-parse --short HEAD` at start and at each test run; a test
  that passed at the start can fail at the end (test_judge_unavailable_edit... went red on HEAD 4e8f43d).

Round 2 (reviews/T-050-staff-engineer-r2.md, verdict changes, pinned c61e84f):
- Round-1 blocker closed (case=cid committed); delete test now loops _CASE_TABLES. Rebuild changed from move-aside (7a450a1) to
  delete-on-upgrade (864676f, T-040 security r2) with a log line only. Rated major: the user's in-flight cases vanish with no UI signal.
- Guard location gap: the F1 regression is caught only by test_api_routes (API-order test), not test_multicase (ingest-only and
  run-only tests). Mutant M1b passes test_multicase. Pattern: check which file guards a regression, not only that some test does.
- Committed tree lacked judge fixtures (tests/fixtures/llm modified/untracked in the working tree): test_t037 4 failures and
  20 "llm call failed" in the committed sample CLI. Working tree is clean. Route to orchestrator as outside-card.
- HEAD moved 3 times during the review. Pin with `git archive <short sha>` into one dir and run everything there.
  The git-guard hook rejects `$(...)` and `$VAR` in bash commands; use literal shas and paths. `git reflog` is blocked for reviewers.

Related: [[project_db_review_patterns]], [[project_wiring_review_patterns]], [[project_harness_review_patterns]].
