# T-048 round 2 review - staff-engineer-reviewer (Marcus Lee lens)

Scope: round-2 commit f3da5b9 (test files). Its LLM-stage suites are byte-identical at ad4803a (`git diff --stat f3da5b9 ad4803a -- <suites>` is empty). Execution pinned to `git archive ad4803ad7211c329aa2ab26333fced979444853a` in my scratchpad (snap3), with the untracked `tests/fixtures/llm/*.json` copied in for CLI runs. HEAD moved to 8ec833f during the review; I did not exercise that commit.

## Round-2 closure (r1 blocker and majors)

Pass rule: each item needs a named test that asserts the behaviour. I grepped `tests/unit` and read each test.

| r1 item | Concrete test (file:line) | Key assert | Mutation evidence |
|---|---|---|---|
| Blocker: no test fails if verify/grounding is removed; no seeded non-verbatim excerpt | `test_pipeline.py:96 test_verify_stage_rejects_non_verbatim_excerpt` | L111-112 `assert all(i["state"] != "verified" for i in items)` / `assert all("GROUNDING_EXCERPT_NOT_VERBATIM" in i["reasons"] and i["state"] == "rejected" for i in items)` | Seeds `quote.replace("Persistent", "Chronic")` (L103; golden record 3 contains "Persistent") and an appended invented sentence (L105). Mutation G1 (`generator.py:69` `exc_reasons = grounding.check_excerpt(body, excerpt)` replaced by `[]`) fails this test. |
| Major: FixtureMissing name and LLM_FAILED_AFTER_RETRIES conversion | `test_audited.py:61 test_fixture_missing_is_one_attempt_and_becomes_llm_failed`; `test_provider.py:37 test_fixture_missing_name_is_exported`; `test_provider_backends.py:133 test_fixture_miss_through_audited_is_failed_after_retries` | audited L67 `assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 1`; L69 `assert "abc123hash" in (row["error"] or "")`; provider L39 `assert hasattr(P, "FixtureMissing") and issubclass(P.FixtureMissing, P.LLMError)` | Passes at ad4803a. Mutation M5 (audited.py `if fixture_miss:` disabled) fails test_audited L61 and test_provider_backends L133. |
| Major: provider max_retries / timeout / argv / single path / no text in logs | `test_provider.py:80 test_sdk_no_internal_retry` (L88 `assert seen["max_retries"] == 0 and 0 < float(seen["timeout"]) <= 120`); `:90 test_cli_argv_pins_model_and_disables_tools_hooks_mcp` (L96 `"disableAllHooks" in argv[argv.index("--settings") + 1]`, L97 `argv[-2:] == ["--", "USER PROMPT"]`); `:100 test_cli_runs_outside_project_with_timeout_and_no_api_key` (L113 `0 < seen["timeout"] <= 120 and "ANTHROPIC_API_KEY" not in seen["env"]`); `:115 test_single_call_path` (L121 `assert bad == []`); `:123 test_no_text_in_logs` (L138 `assert "SECRET" not in str(e1.value) + str(e2.value) + caplog.text + out.out + out.err`) | as quoted | M1 `max_retries=2` fails test_provider:80 and test_provider_backends:71. M2 drops `--strict-mcp-config` and fails test_provider:90 and test_provider_backends:16. M3 `timeout=600` fails test_provider:100. M4 echoes stderr into the LLMError and fails test_provider:123. M7 adds `import subprocess` to app/backend/export.py and fails test_provider:115. Mutations run on b1803c0 snapshot (provider modules unchanged since). |
| Major: judge unavailable for J2-J4 at pipeline level | `test_pipeline.py:156 test_j2_error_or_unsure_never_verifies_a_charge` (L161); `:172 test_j3_error_or_unsure_makes_llm_conflicts_needs_review` (L176 `assert llm and all(...)`); `:188 test_j4_error_unsure_or_disagree_makes_flag_needs_review` (L194 `assert f3 and all(...)`); `test_judges.py:35 test_judge_unavailable_when_call_fails` (L38 `== "unavailable"`, parametrised over run_j1-j4) | as quoted | Mutation S2b (shared judge error mapped to "supported", judges.py:34) fails 10 tests including test_pipeline:150, :156[j20], :172[j30,j31], :188[j40] and test_judges:35[run_j1..run_j4]. |
| Major: vacuous outage assertions | `test_pipeline.py:67 test_code_stages_without_llm` (L73-74 `assert out["entries"] == []` / `assert out["status"] == "done_with_errors" and any(e["code"] == "LLM_FAILED_AFTER_RETRIES" ...)`); `:89 test_fixture_missing_after_audited_wrapper_...` (L93-94 `assert out["entries"] == [] and out["status"] == "done_with_errors"` / `assert {e["code"] for e in out["errors"]} == {"LLM_FAILED_AFTER_RETRIES"} and len(out["errors"]) == 9`) | as quoted | `grep -n " or all(\|== \[\] or" tests/unit/test_pipeline.py tests/unit/test_audited.py tests/unit/test_judges.py` returns nothing. |
| Major: cited test names must exist | Cards resolve by `grep -rn "def <name>" tests/unit`: T-034 names at test_provider_backends.py:16, :35, :71, :80, :99, :120, :133, :143, :153, :161; T-035 `test_generator_schema_minimal` (test_schemas.py:12), `test_j1_states` (test_judges.py:13), `test_j2_every_amount` (test_judges.py:46), `test_judge_amounts_every_amount_and_rate_never_becomes_charge` (test_generator.py:137); T-037 `test_code_stages_without_llm` (test_pipeline.py:67), `test_ladder_and_pending` (:197), `test_stages_and_deadline` (:117) | n/a | All resolve. |

Round-2 items are closed. The verify stage itself is a no-op (see minor finding 3), but a test fails when the grounding it is meant to guarantee is removed.

## Run results at ad4803a

- `pytest tests/unit -q`: 23 failed, 674 passed. 3 failures are `test_pipeline.py::test_j3_error_or_unsure...[j30]`, `[j31]` and `test_j3_conflict_verdict_keeps_semantic_conflict...`, which fail because LLM semantic conflicts never reach the output (`llm` and `sem` are empty). That is a T-036 implementation gap; the tests are correct and their vacuity guards hold. 20 failures are in `test_review_rules.py`, outside T-048 scope.
- The round-2 LLM suites otherwise pass. `test_flags_*` and `test_grounding` were not part of the r1 brief and were not re-scored.

## Findings

1. **major — Checklist 20 (CLI on the golden sample) is not enforced and the CLI is non-deterministic at ad4803a.** The only CLI test skips on a clean checkout, and the CLI crashes differently on each run.
   - Evidence: `tests/unit/test_t037_backend.py:17` `needs_fixtures = pytest.mark.skipif(not list(FIX.glob("*.json")), ...)`; `:21-27` asserts `"entries: 9"` and `"Gap of 73 days"` on the CLI. `git ls-files tests/fixtures/llm | wc -l` prints `0`; `ls tests/fixtures/llm | wc -l` prints 155. Repro: extract `ad4803a`, copy the fixtures in, then run `LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt` three times. Each run exits 1 with a different exception: `ValueError: unknown llm_calls fields ['attempt', 'case_id', 'id', 'item_id', 'latency_ms', 'parsed_ok', 'role', 'step']`, then `ValueError: unknown llm_calls fields ['cost_usd', 'created_at', 'tokens_in', 'tokens_out']`, then `IndexError: tuple index out of range`. Trace: `app/backend/generator.py:118` (thread worker) → `app/llm/audited.py:79` → `app/db/db.py:193` → `db.py:79`. Suspected cause, not proven: `_cols` runs `PRAGMA table_info` on one sqlite connection shared across ThreadPoolExecutor workers, so the column set comes back partial.
   - Why it matters: the same input gives three different failures, so nobody can reproduce a bad run. A clean checkout reports this check as skipped, not failed. The T-048 suite pins no committed CLI run.
   - Fix: (a) backend (T-037): stop sharing a sqlite connection across worker threads, or serialise llm_calls writes; (b) make the CLI check fail, not skip, when fixtures are missing (see finding 2); (c) assert three identical stdout runs with exit 0.
   - Acceptance test: on a clean `git archive` checkout with committed fixtures, `pytest tests/unit/test_t037_backend.py -rs` reports 0 skipped; three consecutive `python -m app.pipeline evals/golden/sample.txt` runs exit 0 with byte-identical stdout (`cmp`).
2. **minor — Fixtures are not in git, so the no-key replay cannot be reproduced from a clean clone.** Evidence: `git ls-files tests/fixtures/llm | wc -l` → `0`; 155 `*.json` files on disk. Why it matters: ADR-004 and CONTRACT §5.2 rely on committed replay so every eval runs with no key; with untracked fixtures the CLI test skips and the eval cannot be re-run. Fix: commit the fixtures with their prompt hashes, or record them in an explicit step. Acceptance: `git archive HEAD` plus `LLM_BACKEND=fixture` replays the sample with 0 FixtureMiss. (Question for Chris below.)
3. **minor — The `verify` stage is a no-op; grounding runs inside `extract`.** Evidence: `app/backend/pipeline.py:243-244` `if guard("verify"): pass  # grounding, token and qualifier checks ran inside extract_entries`; the actual check is `app/backend/generator.py:69` `exc_reasons = grounding.check_excerpt(body, excerpt)`. Why it matters: ADR-007 lists `verify` as a stage. Stage-name tests pass while the stage does nothing, so a refactor that drops grounding from `extract` would keep the stage list green. Test coverage survives (mutation G1 fails `test_verify_stage_rejects_non_verbatim_excerpt`). Fix: move the check into the verify stage, so `extract` returns raw candidates and `verify` emits the GROUNDING reasons. Acceptance test: G1 still fails the test, and an `on_stage` callback records `verify` with the rejected count for record 3 and record 5.
4. **minor — Two suites encode the same provider contracts under the same names.** Evidence: `test_provider.py:80/:115/:123/:69` and `test_provider_backends.py:71/:153/:161/:99` share `test_sdk_no_internal_retry`, `test_single_call_path`, `test_no_text_in_logs`, `test_recorder_refuses_foreign_text`. The T-034 card cites the second file. Why it matters: two sources of truth that can drift; a fix in one file leaves the other red. Fix: keep one set and point the card at it. Acceptance: `pytest --collect-only -q tests/unit | sort | uniq -d` shows none of these pairs.
5. **nit — `test_pipeline.py:89` does not exercise the wrapper it describes.** The docstring says the audited wrapper converts FixtureMissing; the test raises `AU.LLMFailed` directly. The conversion is pinned at `test_audited.py:61` and `test_provider_backends.py:133`, so coverage is fine; fix the docstring.
6. **nit — Card evidence is stale.** T-034 AC1 says "test_provider.py 7 passed"; `grep -c "def test_" tests/unit/test_provider.py` → 14 at ad4803a.

## What I exercised

- Read `personas/staff-engineer.md` in full. Read `reviews/T-048-staff-engineer.md` (r1) and the T-034/T-035/T-036/T-037 cards via `grep` on `board/cards/`.
- `git show --stat f3da5b9`; `git diff --stat f3da5b9 ad4803a -- tests/unit/{test_pipeline,test_provider,test_audited,test_judges,test_schemas,_fakes,test_flags_sample,test_flags_injection}.py` (empty).
- Read in full: `tests/unit/test_pipeline.py`, `test_provider.py`, `test_audited.py`, `test_judges.py`, `test_schemas.py`, `_fakes.py`; the head of `test_t037_backend.py`.
- `pytest tests/unit -q` on snap3 (ad4803a): 23 failed, 674 passed. Per-file: test_pipeline.py 3, test_review_rules.py 20.
- `pytest -rA` on test_provider, test_provider_backends, test_audited, test_judges, test_schemas, test_pipeline on snap3.
- Mutations on scratch copies (never in the repo): G1, S1 (confidence.py:20 `none_ok=("supported", "unavailable")`), S2b (judges.py:34 shared error → "supported") on snap3; M1-M7 on a b1803c0 snapshot.
- Pipeline CLI, three runs on snap3 with fixtures copied in (exit 1, three different exceptions, see finding 1).
- Grep for vacuity (`or all(`, `== [] or`) and cited names (`grep -rn "def <name>" tests/unit`).

## Questions for Chris

- Should `tests/fixtures/llm/*.json` (155 files, none tracked) be committed? Until they are, the CLI check skips on a clean clone (finding 1-2).
- Is checklist 20 (CLI on the golden sample) T-048's to pin with a committed non-skipping test, or only T-037's?

```json
{"card": "T-048", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round-2 commit f3da5b9 (tests/unit/{test_pipeline,test_provider,test_audited,test_judges,test_schemas,_fakes,test_flags_sample,test_flags_injection}.py, test_provider_backends.py, test_t037_backend.py); executed at ad4803a via git archive with untracked tests/fixtures/llm copied in; HEAD moved to 8ec833f during review, not exercised; app URL none; sample case evals/golden/sample.txt",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-048-staff-engineer.md, board/cards/T-034..T-037.md (grep)",
  "git show --stat f3da5b9; git diff --stat f3da5b9 ad4803a -- round-2 suites (empty)",
  "read tests/unit/test_pipeline.py, test_provider.py, test_audited.py, test_judges.py, test_schemas.py, _fakes.py, head of test_t037_backend.py",
  "grep -rn 'def <name>' tests/unit for every cited name; grep for ' or all(' and '== [] or' (none)",
  "pytest tests/unit -q on snap3 (ad4803a): 23 failed, 674 passed",
  "pytest -rA on test_provider, test_provider_backends, test_audited, test_judges, test_schemas, test_pipeline on snap3",
  "mutation G1 generator.py:69 grounding.check_excerpt -> [] on snap3: test_verify_stage_rejects_non_verbatim_excerpt FAILED",
  "mutation S1 confidence.py:20 none_ok adds 'unavailable' on snap3: 6 failures incl. test_j1_failure_is_judge_unavailable_not_verified",
  "mutation S2b judges.py:34 shared judge error -> 'supported' on snap3: 10 failures incl. test_judges:35 and test_pipeline:150,156,172,188",
  "mutations M1-M7 on b1803c0 snapshot: max_retries=2, drop --strict-mcp-config, timeout=600, stderr into LLMError, audited fixture-miss retry, shared judge error->agree, stray subprocess import; each failed its named test",
  "pipeline CLI x3 on snap3 with fixtures: exit 1 each, three different exceptions (ValueError x2, IndexError)",
  "git ls-files tests/fixtures/llm | wc -l (0) vs ls (155)"
 ],
 "verdict": "changes",
 "scores": {"r1_blocker_verify_test": 4, "r1_majors_closed": 4, "mutation_strength": 4, "cli_checklist20_pinned": 2, "fixture_reproducibility": 2, "duplication_and_naming": 3},
 "findings": [
  {"severity": "major",
   "title": "Checklist 20 (CLI on golden sample) is not enforced: the CLI check skips on a clean checkout and the CLI fails differently on each run at ad4803a",
   "evidence": "tests/unit/test_t037_backend.py:17 `needs_fixtures = pytest.mark.skipif(not list(FIX.glob(\"*.json\")), ...)`; :21-27 CLI assert. `git ls-files tests/fixtures/llm | wc -l` -> 0; 155 json on disk. Repro (ad4803a + fixtures copied in): `LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt` x3 -> exit 1 each: `ValueError: unknown llm_calls fields ['attempt', 'case_id', 'id', 'item_id', 'latency_ms', 'parsed_ok', 'role', 'step']`; `ValueError: unknown llm_calls fields ['cost_usd', 'created_at', 'tokens_in', 'tokens_out']`; `IndexError: tuple index out of range`. Trace app/backend/generator.py:118 -> app/llm/audited.py:79 -> app/db/db.py:193 -> db.py:79. Suspected (unproven): shared sqlite connection across ThreadPoolExecutor workers makes PRAGMA table_info return a partial column set.",
   "why_it_matters": "Same input, three different exceptions: a bad run cannot be reproduced. A clean checkout reports the one CLI check as skipped, not failed. No committed test pins the CLI run, so the suite cannot catch this.",
   "fix": "Backend (T-037): stop sharing one sqlite connection across worker threads or serialise llm_calls writes. Tests: make the CLI check fail, not skip, when fixtures are absent (finding 2); assert three identical stdout runs with exit 0.",
   "acceptance_test": "On a clean git archive checkout with committed fixtures, `pytest tests/unit/test_t037_backend.py -rs` reports 0 skipped; three consecutive `python -m app.pipeline evals/golden/sample.txt` runs exit 0 with byte-identical stdout (cmp)."},
  {"severity": "minor",
   "title": "Fixtures are not in git: the no-key replay cannot be reproduced from a clean clone",
   "evidence": "`git ls-files tests/fixtures/llm | wc -l` -> 0; `ls tests/fixtures/llm | wc -l` -> 155 (working tree).",
   "why_it_matters": "ADR-004 and CONTRACT 5.2 rely on committed replay so every eval runs without a key. With untracked fixtures the CLI check skips and the eval cannot be re-run by anyone else.",
   "fix": "Commit the fixtures with their prompt hashes, or generate them in an explicit recorded step.",
   "acceptance_test": "`git archive HEAD` + LLM_BACKEND=fixture replays the sample with 0 FixtureMiss."},
  {"severity": "minor",
   "title": "The verify stage is a no-op; grounding runs inside extract",
   "evidence": "app/backend/pipeline.py:243-244 `if guard(\"verify\"):` / `pass  # grounding, token and qualifier checks ran inside extract_entries`; the check is app/backend/generator.py:69 `exc_reasons = grounding.check_excerpt(body, excerpt)`.",
   "why_it_matters": "ADR-007 lists verify as a stage. Stage-name tests pass while the stage does nothing, so dropping grounding from extract would leave the stage list green. Coverage survives: mutation G1 fails test_pipeline.py:96.",
   "fix": "Move the check into the verify stage: extract returns raw candidates; verify emits the GROUNDING reasons.",
   "acceptance_test": "G1 still fails test_verify_stage_rejects_non_verbatim_excerpt; an on_stage callback records 'verify' with the rejected count for records 3 and 5."},
  {"severity": "minor",
   "title": "Duplicate provider contract tests under the same names in two files",
   "evidence": "tests/unit/test_provider.py:80 and tests/unit/test_provider_backends.py:71 test_sdk_no_internal_retry; test_provider.py:115 / test_provider_backends.py:153 test_single_call_path; test_provider.py:123 / test_provider_backends.py:161 test_no_text_in_logs; test_provider.py:69 / test_provider_backends.py:99 test_recorder_refuses_foreign_text.",
   "why_it_matters": "Two sources of truth that can drift; the T-034 card cites only one of them.",
   "fix": "Keep one set and point the card at it.",
   "acceptance_test": "`pytest --collect-only -q tests/unit | sort | uniq -d` shows none of these pairs."},
  {"severity": "nit",
   "title": "test_pipeline.py:89 docstring claims the audited wrapper path but the test raises LLMFailed directly",
   "evidence": "tests/unit/test_pipeline.py:90 docstring; :91 `miss = AU.LLMFailed(\"FIXTURE_MISS abc\")`.",
   "why_it_matters": "Wrapper conversion is pinned elsewhere (test_audited.py:61, test_provider_backends.py:133), so coverage is fine; the docstring overstates.",
   "fix": "Fix the docstring or drive the test through audited_call.",
   "acceptance_test": "n/a"},
  {"severity": "nit",
   "title": "T-034 card evidence is stale (test count)",
   "evidence": "board/cards/T-034.md AC1 evidence: 'LLM_BACKEND=fixture pytest tests/unit/test_provider.py 7 passed'; `grep -c \"def test_\" tests/unit/test_provider.py` -> 14 at ad4803a.",
   "why_it_matters": "Evidence that does not match the file misleads the next reviewer.",
   "fix": "Update the card evidence (orchestrator-owned).",
   "acceptance_test": "n/a"}
 ],
 "whats_right": [
  "test_verify_stage_rejects_non_verbatim_excerpt (test_pipeline.py:96) seeds two real non-verbatim cases and fails when grounding is removed (mutation G1).",
  "Judge-failure states are pinned at judge, pipeline and state-composition levels with non-vacuous guards; a shared fail-open mutation (S2b) fails 10 tests.",
  "Each provider contract has a test that fails when its contract breaks: max_retries=2, dropped --strict-mcp-config, timeout 600, stderr echoed into LLMError, stray subprocess import (M1-M4, M7)."
 ],
 "questions_for_chris": [
  "Should tests/fixtures/llm/*.json (155 files, none tracked) be committed? Until they are, the CLI check skips on a clean clone.",
  "Is checklist 20 (CLI on the golden sample) T-048's to pin with a committed non-skipping test, or only T-037's?"
 ]}
```
