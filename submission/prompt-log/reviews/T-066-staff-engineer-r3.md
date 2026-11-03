# T-066 round 3 review: single incomplete record, single-record gate, frozen re-run reason (commit a99bc13)

Reviewer: staff-engineer-reviewer (model claude-haiku-5-5). Verdict: **pass** (0 blockers, 0 majors, 1 minor, 1 nit).

## Summary

All three brief checks hold at a99bc13 (HEAD, scope files clean in the working tree).

1. **A single incomplete record gets no false "several records" message.** Confirmed. `IN.ingest("Date: 2026-03-03\nSource: Clinic A\n")` gives one record, method `ambiguous`, `split_failure` None, one `SPLIT_AMBIGUOUS` and no `SPLIT_REJECTED`. The `NOT_ATTEMPTED` branch is now `len(recs) > 1` (`app/backend/ingest.py:266`). A sweep of six single-record input classes gives no "several records" text in any of them.
2. **The single-record gate is tested with a spy, and mutating the gate fails a test.** Confirmed. The spy test (`tests/unit/test_split_llm.py:412`) gives an unlabelled first block plus two labelled records and records zero splitter calls. Removing `len(recs) == 1` (M_gate) turns it red. A single unsplit block still reaches the splitter once.
3. **A re-run after a decision re-shows SPLIT_REJECTED from `config.split_failure`.** Confirmed. After run 1 (no fixture) the case config holds `split_failure: NO_MODEL`. After an accept, run 2 makes no split call, shows `SPLIT_REJECTED: No model was available...`, and adds no split error (`pipeline.py:121-131`, `274`). Four mutants (store call removed, config read removed, replay raise removed, `replayed` flag dropped) each turn at least one test red.

Two items remain. Neither affects the three checks.

## Exercised

- Pinned `git archive a99bc13` into scratchpad `t066r3/base`. Read the full diff: `git show a99bc13 -- app/backend/ingest.py app/backend/pipeline.py tests/unit/test_split_llm.py`. `git status --short -- app/backend/ingest.py app/backend/pipeline.py tests/unit/test_split_llm.py` printed nothing (no uncommitted edits in scope).
- `.venv/bin/python -m pytest -q tests/unit/test_split_llm.py` in the working repo (HEAD a99bc13): **46 passed**.
- Same command on the pinned copy: 46 passed. Full `tests/unit` on the pinned copy: **953 passed** (matches the card note).
- Added-line grep on the a99bc13 diff for `except|float(|sleep|retry|time.|http|requests|anthropic|random`: no matches.
- `probe_r3.py` (run path, creation path, spy, frozen re-run): see `artifacts/review-evidence/T-066-staff-engineer-r3/outputs.txt`.
- `sweep_single.py`: six single-record inputs (complete one-visit, labelled excerpt missing, unlabelled prose, date only, source only, sample TEXT): none contains "several records"; the splitter is asked only for the unlabelled, date-only, source-only and sample inputs.
- `mutate_r3.py` on the pinned copy, six mutants, each restored after the run:
  - M_gate_single_record: 1 failed (`test_splitter_is_only_called_for_a_single_block_never_for_several_records`).
  - M_narrow_len_gt1: 1 failed (`test_single_incomplete_labelled_record_never_claims_several_records`).
  - M_store_reason_call: 2 failed.
  - M_replay_reads_config: 2 failed.
  - M_replay_raise: 2 failed.
  - M_replayed_flag_dropped: 1 failed.
- `mutate_extra.py` (not in the brief): a single labelled-incomplete record gets NO_MODEL. Result: `NO_MODEL ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED']` and **46 passed**. This mutant survives (finding 1).
- Full `tests/unit` on the pinned copy: 953 passed.
- Read `docs/LLM_VS_CODE.md:29`, `memory/contracts/api.md:67`, `memory/ORCHESTRATOR_DECISIONS.md` (grep for T-066: no entry), `reviews/T-066-staff-engineer-r2.md`, and the card (`python3 tools/board.py show T-066`).
- Not exercised: the web UI rendering of warnings, the claude-cli backend, E2E specs, the live app URL.
- Evidence: `artifacts/review-evidence/T-066-staff-engineer-r3/` (outputs.txt, the four scripts).

## Findings

**Minor 1: the no-reason outcome for a single labelled-incomplete record is not pinned by a test.**
Evidence: `tests/unit/test_split_llm.py:403-409` asserts only `assert not any("several records" ...)` and `assert r["split_failure"] != "NOT_ATTEMPTED"`. The handoff states this input gets no SPLIT_REJECTED. `artifacts/review-evidence/T-066-staff-engineer-r3/outputs.txt`, section `mutate_extra`: adding `split_failure = "NO_MODEL"` for `len(recs) == 1` and not eligible gives `NO_MODEL ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED']` and `46 passed`.
Why it matters: the claimed behaviour is unprotected. A regression would show "No model was available to propose record boundaries" for a paste the model is never asked about (`docs/LLM_VS_CODE.md:29`: a single record with both labels "is not sent"). That is a false statement about the paste, the same class as r2 major 1. The shipped code is correct, so this is a test gap, not a defect. Rated minor per calibration: present but weak.
Fix: in the test at line 403, add `assert r["split_failure"] is None and not any(w["code"] == "SPLIT_REJECTED" for w in r["warnings"])`.
Acceptance test: the `mutate_extra.py` mutant turns the test red; the a99bc13 copy stays at 46 passed.

**Nit 1: the no-reason decision is not recorded as a decision.**
Evidence: `grep -n "T-066" memory/ORCHESTRATOR_DECISIONS.md` returns no entry. The r2 fix asked the orchestrator to record the reason choice there. The card handoff records it ("no new code"), and `memory/contracts/api.md:67` implies it.
Why it matters: a future reader of `ORCHESTRATOR_DECISIONS.md` cannot see why a single labelled-incomplete record shows no SPLIT_REJECTED. Optional.
Fix: one line in `memory/ORCHESTRATOR_DECISIONS.md` stating that a single labelled record with an incomplete excerpt gets SPLIT_AMBIGUOUS only (no reason, no model call).

## What is right

- The gate is pinned by a spy, not only by output: base 0 splitter calls on a multi-record paste, 1 call on a single unsplit block (`probe_r3.py` C1/C2). M_gate turns red.
- The frozen re-run is pinned end to end through `run_pipeline`: after an accept, the reason is re-shown, no split call is made, no split error is added, and the stored config value is `NO_MODEL` (D1/D2 in `outputs.txt`).
- The `replayed` flag keeps a replayed reason out of `errors` (`ingest.py:273`), so a re-run does not record a new failure. The failed-call replay test (line 443) kills the flag mutant.

```json
{"card": "T-066", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit a99bc13 (app/backend/ingest.py, app/backend/pipeline.py, tests/unit/test_split_llm.py); HEAD = a99bc13; scope files clean in the working tree; pinned via git archive into scratchpad t066r3/base; no app URL exercised; inputs are synthetic test strings",
 "exercised": [
  "git show a99bc13 full diff of ingest.py, pipeline.py, test_split_llm.py; git status on scope files (empty)",
  ".venv/bin/python -m pytest -q tests/unit/test_split_llm.py in the working repo: 46 passed",
  "pinned a99bc13 (git archive): test_split_llm.py 46 passed; full tests/unit 953 passed",
  "added-line grep on the a99bc13 diff for except|float(|sleep|retry|time.|http|requests|anthropic|random: no matches",
  "probe_r3.py on pinned copy: single labelled incomplete record gives SPLIT_AMBIGUOUS only; two labelled records plus unlabelled first block gives NOT_ATTEMPTED with spy 0 calls; single unsplit block gives spy 1 call; run 1 stores NO_MODEL, accept, run 2 re-shows SPLIT_REJECTED with 0 new split calls and no split error",
  "sweep_single.py on pinned copy: six single-record input classes, none with 'several records'",
  "mutate_r3.py on pinned copy: M_gate 1 failed; M_narrow 1 failed; M_store 2 failed; M_replay_reads_config 2 failed; M_replay_raise 2 failed; M_replayed_flag 1 failed; base restored 46 passed",
  "mutate_extra.py on pinned copy: single labelled incomplete record gets NO_MODEL; 46 passed (survivor, finding 1)",
  "read docs/LLM_VS_CODE.md:29, memory/contracts/api.md:67, memory/ORCHESTRATOR_DECISIONS.md (grep T-066: none), reviews/T-066-staff-engineer-r2.md, python3 tools/board.py show T-066",
  "evidence: artifacts/review-evidence/T-066-staff-engineer-r3/ (outputs.txt, probe_r3.py, sweep_single.py, mutate_r3.py, mutate_extra.py)"
 ],
 "verdict": "pass",
 "scores": {"contract_match_llm_vs_code_row1": 4, "single_incomplete_no_false_claim": 5, "gate_pinned_by_spy": 5, "frozen_rerun_reason_shown": 5, "test_strength_split_reasons": 4, "failure_visibility_no_swallowed_errors": 5},
 "findings": [
  {"severity": "minor",
   "title": "No-reason outcome for a single labelled-incomplete record is not pinned by a test",
   "evidence": "tests/unit/test_split_llm.py:403-409 asserts only no 'several records' and split_failure != NOT_ATTEMPTED. artifacts/review-evidence/T-066-staff-engineer-r3/outputs.txt mutate_extra: adding NO_MODEL for that input gives NO_MODEL ['SPLIT_AMBIGUOUS','SPLIT_REJECTED'] and 46 passed.",
   "why_it_matters": "The handoff claims this input gets no SPLIT_REJECTED. A regression would say 'No model was available' for a paste the model is never asked about (docs/LLM_VS_CODE.md:29), a false statement of the same class as r2 major 1. The shipped code is correct; this is a test gap. Minor per calibration: present but weak.",
   "fix": "In test_single_incomplete_labelled_record_never_claims_several_records add: assert r['split_failure'] is None and not any(w['code'] == 'SPLIT_REJECTED' for w in r['warnings'])",
   "acceptance_test": "mutate_extra.py mutant turns the test red; a99bc13 copy stays 46 passed."},
  {"severity": "nit",
   "title": "No-reason decision for a single labelled-incomplete record is not recorded in ORCHESTRATOR_DECISIONS",
   "evidence": "grep -n 'T-066' memory/ORCHESTRATOR_DECISIONS.md returns no entry; r2 fix asked for the reason choice to be recorded; card handoff says 'no new code'.",
   "why_it_matters": "A reader of the decisions file cannot see why this input shows no SPLIT_REJECTED.",
   "fix": "One line in memory/ORCHESTRATOR_DECISIONS.md: single labelled record with incomplete excerpt gets SPLIT_AMBIGUOUS only (no reason, no model call).",
   "acceptance_test": "grep -n 'T-066' memory/ORCHESTRATOR_DECISIONS.md returns the entry."}
 ],
 "whats_right": [
  "The single-record gate is pinned by a spy: multi-record paste gives 0 splitter calls, single unsplit block gives 1 (probe_r3 C1/C2); removing the gate turns a test red.",
  "The frozen re-run re-shows SPLIT_REJECTED from config.split_failure with no new split call and no new split error (probe_r3 D1/D2); four replay mutants are each killed.",
  "A replayed failure is marked replayed=True (ingest.py:273), so a re-run never records a new split error for an old failure."
 ],
 "questions_for_chris": [
  "Model policy: CLAUDE.md section 6 assigns engineering reviewers to Sonnet. This review ran as claude-haiku-5-5, as r1 and r2 did. Should T-066 get a Sonnet re-review before the milestone gate?"
 ]}
```
