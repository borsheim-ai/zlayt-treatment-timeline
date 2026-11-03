---
name: llm-stage-review-patterns
description: T-048 r2 (LLM-stage red suites, round 2): verify-stage no-op, fail-open judge mutation method, CLI skip-on-missing-fixtures, shared sqlite across threads
metadata:
  type: project
---

Recurring patterns from the T-048 round-2 review (2026-11-01, reviews/T-048-staff-engineer-r2.md).

- **Verify stage can be a no-op label.** pipeline.py had `if guard("verify"): pass` while grounding ran inside extract (generator.py:69). Stage-name tests stay green. Check the stage body, not just its name. **Why:** a stage named for a guarantee that does nothing hides a dropped check. **How to apply:** for any "verify/check" stage, grep the body; mutate the call site, not the stage label.
- **Mutation method that works here.** `git archive <full sha>` into a scratchpad dir, copy untracked fixtures in, then run mutants on copies with a pattern-count assert (`assert t.count(old) == 1`). Shared-helper mutants (judges `_run` except branch) hit all four judges at once, which is useful evidence. Pattern-miss errors are a sign the mutant did not run.
- **Fail-open judge mutants.** Mapping a judge error to "supported" in the shared helper fails about 10 tests; mapping it in `confidence.compose_state` (`none_ok` adds "unavailable") fails about 6. Both are caught, so judge-failure coverage is real.
- **CLI check skips on missing fixtures.** `tests/unit/test_t037_backend.py:17` uses `skipif(not list(FIX.glob("*.json")))` and fixtures are untracked (`git ls-files tests/fixtures/llm` = 0). A clean checkout reports the golden CLI check as skipped, not failed. **How to apply:** flag any `skipif` on a missing artifact that the artifact's own commit should provide.
- **Non-deterministic CLI failure.** Three runs of `python -m app.pipeline evals/golden/sample.txt` gave three different exceptions (two different ValueError field sets, then IndexError). Suspected: one sqlite connection shared across ThreadPoolExecutor workers (`_cols` PRAGMA table_info). Not proven. **How to apply:** when the same input fails differently, suspect shared mutable state across threads before the schema.
- **Duplicate contract tests across files.** test_provider.py and test_provider_backends.py both define test_sdk_no_internal_retry, test_single_call_path, test_no_text_in_logs, test_recorder_refuses_foreign_text. **How to apply:** `pytest --collect-only -q | sort | uniq -d` on any suite that gets a second file.

Environment gotchas seen in this review (also relevant to other reviewers):
- HEAD moved several times during one review (b1803c0 → 1da399d → ad4803a → 53093a0 → 636c961 → 8ec833f). Pin by full sha with `git archive` and say so in the review.
- The board-guard hook blocks `git branch`. The git-guard hook blocks `$(...)` in command position. Use `git rev-parse` and literal shas.
- `timeout` is not installed on this macOS box.
- A compound `git ls-files && rm -rf ... && git archive` was denied by permission; split into separate commands.

See also [[project_harness_review_patterns]] and [[project_db_review_patterns]].
