# T-066 review (staff-engineer-reviewer), commit e7c1912

**Verdict: changes.** No blockers. Two majors, two minors.

Confirmed: on the case-creation path (`ingest_case`, no model call), an unsplit paste yields `SPLIT_REJECTED` with reason NO_MODEL, and removing that emission fails the new test in a scratch copy. The re-run path from 8bf99fb stays consistent with the change.

Not confirmed as the brief states it: on the run path (`run_pipeline`, which always has a call), a paste with no split fixture reports reason `FIXTURE_MISS`, not NO_MODEL. I rated this major, not blocker: nothing is silent, and LLM_VS_CODE row 1 accepts a reason code on a failed call. The brief's wording is the reason for the escalation to "reason NO_MODEL".

Second major: a multi-record paste with one trailing unsplit block still gets `SPLIT_AMBIGUOUS` with no reason. LLM_VS_CODE row 1 names T-066 as the card that closes this gap. The `len(recs) == 1` gate that decides it is not pinned by any test (mutant M3 survives 31/31).

Model note: this review ran as claude-haiku-5-5. CLAUDE.md §6 assigns engineering reviewers to Sonnet. See questions_for_chris.

## Exercised
- `git show --stat e7c1912` and `git show e7c1912 -- app/backend/ingest.py tests/unit/test_split_llm.py` (full diff read).
- `git diff --stat e7c1912 HEAD -- app/backend/ingest.py tests/unit/test_split_llm.py app/backend/pipeline.py` (empty: scope files unchanged since the commit).
- Pinned copy: `git archive e7c1912 | tar -x` into `artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912`, then `.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider` run twice: `31 passed in 0.55s` and `31 passed in 0.55s` (output in `pinned_pytest_output.txt`). The brief's `python3 -m pytest` fails on system python: `No module named pytest`.
- Working tree (not the pinned sha): `34 passed`. The extra 3 tests come from an uncommitted +57-line edit to `tests/unit/test_split_llm.py` that is not in e7c1912. Not reviewed.
- Mutation spot-check, `artifacts/review-evidence/T-066-staff-engineer/mutate.py` (output in `mutation_output.txt`), each mutant in a fresh copy of the pinned tree:
  - M1, remove the `split_failure = "NO_MODEL"` line (pinned ingest.py:264): `1 failed, 30 passed`. The failing test is `test_no_model_for_unsplit_paste_emits_split_rejected_no_model`.
  - M2, suppress the SPLIT_REJECTED warning when reason is NO_MODEL (ingest.py:295): `1 failed, 30 passed`. Same test.
  - M3, set NO_MODEL for any ambiguous paste, dropping the single-record gate (ingest.py:263): `31 passed`. Survivor.
- Repro script `repro_paths.py` (output in `repro_output.txt`), run from the pinned copy with an empty `LLM_FIXTURE_DIR`:
  - A (case creation, `PL.run_ingest(TEXT)`, the same call `ingest_case` makes at pipeline.py:179): `split_failure: NO_MODEL`, warning "No model was available to propose record boundaries".
  - B (run, `run_pipeline` with `AU.make_call`): warning reason `FIXTURE_MISS`, errors `LLM_FAILED_AFTER_RETRIES` at stage split.
  - C (multi-record paste with a trailing unsplit block, case creation): 3 records, `split_method: ambiguous`, only `SPLIT_AMBIGUOUS`.
  - D (re-run consistency, create then good split then failing split): stored records equal run records (`consistent: True`).
- Read: `docs/LLM_VS_CODE.md:29` (row 1), `reviews/T-063-staff-engineer.md` M1, `app/backend/split_llm.py:13-30`, `app/backend/pipeline.py:177-179, 224-227, 242-243, 345`, `app/backend/api.py:285, 326`, `personas/staff-engineer.md`.
- Grep for bare or swallowed exceptions in the scope: ingest.py catches only `SplitFailed` and `ValueError` (narrow). `pipeline.py` `_store_records` re-raises after ROLLBACK.
- Not run: full `tests/unit` suite (brief scoped to the split file), E2E, CLI on the sample case. No app URL exercised.

## Findings

### F1 (major): the run path reports FIXTURE_MISS, not NO_MODEL
- Evidence: `artifacts/review-evidence/T-066-staff-engineer/repro_output.txt` section B: `('SPLIT_REJECTED', "The AI's proposed record boundaries were not used (FIXTURE_MISS); the paste stays one record.")`. Cause: `pipeline.py:227` `call = call or AU.make_call(conn, cid, now=clock)` means `run_pipeline` always passes a splitter, so the `if eligible and not splitter` branch (`ingest.py:263`) is reached only from `ingest_case` (`pipeline.py:179`). The splitter's fixture miss is `split_llm.py:22`, which raises `SplitFailed("FIXTURE_MISS")`.
- Why it matters: the brief requires reason NO_MODEL when "no model or fixture" is available. The same unsplit paste shows "No model was available" at creation and "FIXTURE_MISS" at run. Nothing is silent, and the doc accepts a reason code on a failed call, so this is not a blocker. It is still a visible divergence from the stated requirement, and the NO_MODEL reason is unreachable on every path that runs the pipeline.
- Fix: the orchestrator picks one reason vocabulary and records it in `memory/ORCHESTRATOR_DECISIONS.md`. Option A: `split_llm.py:21-22` maps `FixtureMiss` to `SplitFailed("NO_MODEL")`, and `pipeline.py:242-243` keeps the FIXTURE_MISS detail in the error entry. Option B: amend the brief and ADR-018 (`memory/DECISIONS.md:341`) to accept FIXTURE_MISS on the run path.
- Acceptance test: `run_pipeline(conn, cid, TEXT, call=AU.make_call(conn, cid))` with an empty `LLM_FIXTURE_DIR` yields a SPLIT_REJECTED warning whose message names the chosen code, plus one `errors` entry for stage split. Reverting the fix must fail this test.

### F2 (major): multi-record paste with an unsplit tail gets no reason
- Evidence: `repro_output.txt` section C: 3 records, `split_method: ambiguous`, warnings `['SPLIT_AMBIGUOUS']` only. Gate: `ingest.py:262` `len(recs) == 1`. Doc: `docs/LLM_VS_CODE.md:29` says "When no model is wired in at all (the case-creation path today), only `SPLIT_AMBIGUOUS` is emitted and the reason is not shown; that gap is card T-066, so read this row as the intended behaviour once T-066 lands." Survivor: mutant M3 (`mutate.py`, `31 passed in 0.53s`). No test feeds a multi-record paste with a leftover block.
- Why it matters: the graded table says T-066 closes this gap, and this class of paste still shows no reason. The eligibility gate decides which pastes get a reason at all, and no test pins it. A future change to the gate would pass the suite.
- Fix: either (a) emit SPLIT_REJECTED with a reason code for every ambiguous paste that is not sent to a model, which the orchestrator must name; or (b) amend LLM_VS_CODE row 1 and ADR-018 so the reason applies only to single-block pastes, with that scope written in the row. Either way, add a test for the multi-record tail.
- Acceptance test: `IN.ingest("Date: 2026-03-03\nSource: Clinic A\nExcerpt: Neck pain.\n---\nDate: 2026-03-10\nSource: Clinic A\nExcerpt: Follow up.\n---\nFree text with no label at all.\n")` yields a SPLIT_REJECTED warning with a reason code. Mutant M3 must fail the suite.

### F3 (minor): the named test checks ingest(), not the pipeline, and no reason text is pinned
- Evidence: `tests/unit/test_split_llm.py:17-20` calls `IN.ingest(TEXT)` only and asserts `"No model" in message`. `tests/unit/test_split_llm.py:55-60` asserts only that SPLIT_REJECTED is present for `LLM_FAILED_AFTER_RETRIES`, not its reason. No test covers the run-path reason.
- Why it matters: the AC and brief say "the pipeline must emit". Without a run-path test, F1 can regress silently.
- Fix: add a `run_pipeline` test with the fixture backend and an empty fixture dir that asserts the reason code.
- Acceptance test: that test fails when F1's fix is reverted.

### F4 (minor): run output drops split_method and split_failure at top level
- Evidence: `pipeline.py:95` (`run_ingest`) returns `split_failure`. The `run_pipeline` return at `pipeline.py:345` has no `split_method` or `split_failure` key. `repro_output.txt` section B prints `split_failure: None | split_method: None`.
- Why it matters: the reason is only in message text, so the UI and evals cannot assert it without string matching.
- Fix: include `split_method` and `split_failure` (reason code as a field) in the `run_pipeline` return.
- Acceptance test: `run_pipeline(...)["split_failure"] == "FIXTURE_MISS"` (or the code chosen under F1).

## What is right
- The NO_MODEL assignment is code-only and sits before the splitter branch (`ingest.py:262-265`). No model call, and the confident-split negative test passes (`test_split_llm.py:23-25`).
- M1 and M2 are both killed by the new test. Errors are not swallowed: `SplitFailed` reasons reach warnings, and unexpected exceptions still propagate (`test_split_llm.py:63-67`).
- The 8bf99fb re-run path is consistent with the change: create, good split, failing split leaves stored records equal to run records (`repro_output.txt` section D). The diff touches no record-storage code.

```json
{"card": "T-066", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit e7c1912 (app/backend/ingest.py, tests/unit/test_split_llm.py), pinned via git archive to artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912; HEAD at review time 8b2001e; no app URL exercised; sample: evals/golden/unsplit_paste.txt via the test replay",
 "exercised": [
   "git show --stat / git show e7c1912 (full diff read)",
   "git diff --stat e7c1912 HEAD -- ingest.py test_split_llm.py pipeline.py (empty)",
   "git archive e7c1912 -> pinned-e7c1912; .venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider x2: 31 passed, 31 passed",
   "system python3 -m pytest: No module named pytest (brief command not runnable on system python)",
   "working tree test_split_llm.py (uncommitted +57 lines, not in e7c1912): 34 passed (not reviewed)",
   "mutate.py on pinned copy: M1 remove NO_MODEL assignment -> 1 failed; M2 suppress NO_MODEL warning -> 1 failed; M3 drop single-record gate -> 31 passed (survivor)",
   "repro_paths.py sections A-D on pinned copy (repro_output.txt): A NO_MODEL at creation; B FIXTURE_MISS on run; C multi-record tail gives SPLIT_AMBIGUOUS only; D re-run consistent True",
   "read docs/LLM_VS_CODE.md:29, reviews/T-063-staff-engineer.md M1, split_llm.py:13-30, pipeline.py:177-179 / 224-227 / 242-243 / 345, api.py:285 / 326, personas/staff-engineer.md",
   "grep bare/swallowed exceptions in scope; _store_records re-raises after ROLLBACK"],
 "verdict": "changes",
 "scores": {"contract_match_llm_vs_code_row1": 3, "failure_visibility": 4, "test_strength": 3, "rerun_consistency_8bf99fb": 5, "llm_free_deterministic_path": 5},
 "findings": [
   {"severity": "major", "title": "Run path reports FIXTURE_MISS, not NO_MODEL; NO_MODEL unreachable on any path that runs the pipeline",
    "evidence": "artifacts/review-evidence/T-066-staff-engineer/repro_output.txt section B: (\"SPLIT_REJECTED\", \"The AI's proposed record boundaries were not used (FIXTURE_MISS)...\"); pipeline.py:227 call always set; ingest.py:263 branch reached only from pipeline.py:179; split_llm.py:22 raise SplitFailed(\"FIXTURE_MISS\")",
    "why_it_matters": "Brief requires reason NO_MODEL for no model or fixture. Same paste shows NO_MODEL at creation and FIXTURE_MISS at run. Not silent and accepted by LLM_VS_CODE row 1, so major not blocker.",
    "fix": "Orchestrator picks one reason vocabulary and records it in memory/ORCHESTRATOR_DECISIONS.md. A: split_llm.py:21-22 maps FixtureMiss to SplitFailed(\"NO_MODEL\"), pipeline.py:242-243 keeps FIXTURE_MISS detail in errors. B: amend brief and ADR-018 (memory/DECISIONS.md:341).",
    "acceptance_test": "run_pipeline(conn,cid,TEXT,call=AU.make_call(conn,cid)) with empty LLM_FIXTURE_DIR yields SPLIT_REJECTED naming the chosen code plus one errors entry stage=split; reverting the fix fails it."},
   {"severity": "major", "title": "Multi-record paste with an unsplit tail gets SPLIT_AMBIGUOUS with no reason; eligibility gate untested",
    "evidence": "repro_output.txt section C: 3 records, split_method ambiguous, warnings ['SPLIT_AMBIGUOUS'] only; ingest.py:262 len(recs)==1 gate; docs/LLM_VS_CODE.md:29 names T-066 as the card closing this gap; mutate.py M3 -> 31 passed",
    "why_it_matters": "The graded table says T-066 closes this gap and this class still shows no reason. The gate decides which pastes get a reason and no test pins it; a change to the gate passes the suite.",
    "fix": "Either (a) SPLIT_REJECTED with a reason code for every ambiguous paste not sent to a model (orchestrator names the code), or (b) amend LLM_VS_CODE row 1 and ADR-018 to limit the reason to single-block pastes and say so in the row. Add a multi-record tail test either way.",
    "acceptance_test": "IN.ingest('Date: 2026-03-03\\nSource: Clinic A\\nExcerpt: Neck pain.\\n---\\nDate: 2026-03-10\\nSource: Clinic A\\nExcerpt: Follow up.\\n---\\nFree text with no label at all.\\n') yields a SPLIT_REJECTED warning with a reason code; mutant M3 fails the suite."},
   {"severity": "minor", "title": "Named test exercises ingest(), not the pipeline; reason text unpinned",
    "evidence": "tests/unit/test_split_llm.py:17-20 IN.ingest(TEXT) only; tests/unit/test_split_llm.py:55-60 asserts SPLIT_REJECTED presence only",
    "why_it_matters": "AC and brief say the pipeline must emit it. Without a run-path test, F1 can regress silently.",
    "fix": "Add a run_pipeline test with fixture backend and empty fixture dir asserting the reason code.",
    "acceptance_test": "Test fails when the F1 fix is reverted."},
   {"severity": "minor", "title": "run_pipeline output drops split_method and split_failure at top level",
    "evidence": "app/backend/pipeline.py:95 run_ingest returns split_failure; run_pipeline return pipeline.py:345 has no split_method/split_failure; repro_output.txt section B prints None for both",
    "why_it_matters": "Reason exists only in message text; UI and evals cannot assert it without string matching.",
    "fix": "Add split_method and split_failure (reason code as a field) to the run_pipeline return.",
    "acceptance_test": "run_pipeline(...)['split_failure'] equals the code chosen under F1 on the fixture-miss run."}
 ],
 "whats_right": [
   "NO_MODEL assignment is code-only, before the splitter branch (ingest.py:262-265); no model call; confident-split negative test passes (test_split_llm.py:23-25).",
   "Mutants M1 and M2 are both killed by the new test; SplitFailed reasons reach warnings and unexpected exceptions still propagate (test_split_llm.py:63-67).",
   "8bf99fb re-run path stays consistent: create, good split, failing split leaves stored records equal to run records (repro_output.txt section D); no record-storage code touched."
 ],
 "questions_for_chris": [
   "Model policy: CLAUDE.md §6 assigns engineering reviewers to Sonnet; this review ran as claude-haiku-5-5. Should T-066 be re-reviewed on Sonnet before the record counts?",
   "F2: should a multi-record paste with an unsplit tail show a reason at all? The answer changes LLM_VS_CODE row 1 and ADR-018."
 ]}
```
