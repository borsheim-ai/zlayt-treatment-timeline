---
name: split-llm-review-patterns
description: T-057 r1 (LLM split fallback, commit 099732b): eval report hash vs committed prompt, same-count re-run leaves stale records, surviving mutants masked by a sibling check, audited prompt_version dropped
metadata:
  type: project
---

Recurring patterns from the T-057 round-1 review (2026-11-01, reviews/T-057-staff-engineer.md, verdict fail: 2 blockers, 4 majors).

- **Eval report can attest to a different prompt.** The card's report (evals/reports/20261102T021046Z.md:44) listed split_v1.md at sha 579868d5..., but the committed file was 8e872bc4.... The report was also never committed (git log -- report prints nothing). **Why:** CONTRACT 8.3 says re-run evals before in_review; an uncommitted report that hashes an older prompt is not evidence. **How to apply:** for any prompt/model/schema change, compare `git show <sha>:<prompt> | shasum -a 256` with the hash in the report and check `git log -- <report>`.
- **Same-count re-run keeps stale rows.** pipeline.py replaced stored records only when the count differed, and _store_records returns early when rows exist. A second run with different boundaries of the same count leaves run-1 spans while entries use run-2 spans. Reachable via POST /api/cases/{token}/run (api.py:312). A deterministic fixture hides it; use a stub split. **How to apply:** for any "replace on change" guard, test a re-run where the count is equal and the content differs.
- **Mutant survives because a sibling check catches the same case.** Dropping the line-start check fails tests, but dropping coverage or contiguity leaves 33/33 green. The "gap" and "overlap" cases start mid-line, so the line-start check rejects them first. **How to apply:** for every validator clause, build a case where only that clause fails (line-start-aligned) and mutate each clause alone.
- **audited make_call drops prompt_version for every step.** audited.py:106 never passes prompt_version, so llm_calls.prompt_version is NULL for all steps, including the new split. Caller also discarded the call_id (split_llm.py:17 `_call_id`). **How to apply:** after any new LLM step, query llm_calls for the step and check prompt_version and that the output links to a call_id.
- **Bare except in the fallback path.** `except Exception: pass` around a splitter swallowed LLMFailed; the run showed only SPLIT_AMBIGUOUS and no errors[] entry. **How to apply:** grep `except Exception` in every fallback; the test asserted only the record count.
- **Evidence span relative to the wrong base.** LLM_SPLIT evidence used start 0 / end len of the excerpt, which selects the banner in the paste. **How to apply:** check T[start:end] == evidence text for every new flag.

Harness and environment gotchas seen in this review (also relevant to other reviewers):
- reviewer-write-guard blocks Write to the scratchpad path; write evidence scripts under artifacts/review-evidence/<card>-staff-engineer/ instead.
- git-guard blocks `rm` with an unresolved shell expansion; use fresh directory names instead of deleting.
- board-guard treats a `>` inside a grep pattern as a redirect and blocks the command; avoid `>` in patterns (use grep -e).
- `git archive <sha>` excludes untracked fixtures. At any T-057-era commit the judge replay tests (test_t037_backend.py) fail with FIXTURE_MISS even after `cp -n` from the working tree, and the same 3 fail at the parent commit, so there is no clean full-suite control. Report the split subset as the control, and say so.
- HEAD moved (099732b -> 996f9b4) and the working tree had 145 dirty files during the review. Pin by full sha.

See also [[project_eval_runner_review_patterns]], [[project_backend_llm_review_patterns]], [[project_llm_stage_review_patterns]], [[project_harness_review_patterns]].

## Round 2 additions (T-057 r2 b365af3, T-059 20d866f; 2026-11-01)
- **Replace-on-change fixes cover only the success path.** r1 fix deleted stored records when split_method == 'llm'; a re-run whose split FAILS or is rejected skips the delete, so run-1 records stay while run-2 entries cite the unsplit block (repro: artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py). **How to apply:** for any "replace stored state" fix, test success->failure and success->success re-runs.
- **Fix commit deletes a tracked fixture and leaves its replacement untracked** (prompt hash change re-keys the fixture). Always `git archive <sha>` + pytest -k <card> as the clean control; check `git status --short tests/fixtures`.
- **Seeded-hallucination tests that accept any reason code** let a whole check be mutated away (T-059 N3 D-006 token check, N11 basis-hash staleness both survived 17 passed). Incidental checks (dropped 'C/O' qualifier) catch every row for a self-report quote; use a clean quote (e5 'Pain 4/10, improving.') to isolate checks.
- Mutant scripts: write with the Write tool under artifacts/review-evidence/<card>-staff-engineer/; a `>` or `<` inside a bash heredoc/sed string trips board-guard.
