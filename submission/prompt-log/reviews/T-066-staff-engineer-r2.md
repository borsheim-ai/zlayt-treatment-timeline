# T-066 round 2 review: run-path reason and unsplit-tail reason (commit d148e0f)

Reviewer: staff-engineer-reviewer (model claude-haiku-5-5). Verdict: **changes** (two majors, no minors, no blockers).

## Summary

Both brief checks hold at d148e0f.

1. **Run path: FIXTURE_MISS now yields SPLIT_REJECTED with reason NO_MODEL.** Confirmed. `run_pipeline` with `call=AU.make_call(...)` and an empty fixture dir returns `split_failure: NO_MODEL`, one `SPLIT_REJECTED` warning, and one `errors` entry (stage `split`, cause `FIXTURE_MISS`). The code is `app/backend/pipeline.py:258-259`. The run result carries `split_method` and `split_failure` (`pipeline.py:361`). This closes r1 F1 and r1 F4.
2. **Multi-record paste with an unsplit tail: SPLIT_REJECTED with reason NOT_ATTEMPTED.** Confirmed at case creation (`IN.ingest`) and on the run path. The splitter is not called. This closes the tail case of r1 F2.

Mutation: six emissions removed one at a time in scratch copies (E1 creation NO_MODEL, E2 run-path remap, E3 NOT_ATTEMPTED, E4 warning suppressed for NOT_ATTEMPTED, E5 run result drops `split_failure`, E6 error cause dropped). Each turns at least one test red in `tests/unit/test_split_llm.py`.

Two problems remain, both about the eligibility gate and the NOT_ATTEMPTED branch.

- **Major 1.** NOT_ATTEMPTED also fires for a single incomplete labelled record, and the warning says "several records". That is a false statement about the paste.
- **Major 2.** The single-record gate (`ingest.py:262`, `len(recs) == 1`) is still unpinned. Removing it passes all 37 split tests, and the splitter is then called on a multi-record paste. This is r1 F2 (its M3), still open.

Other results: `tests/unit/test_split_llm.py` 37 passed at the pinned d148e0f. Full `tests/unit` 937 passed at d148e0f. At HEAD 312ed92 the split file has 42 passed; the extra tests come from commit 1c0bae2 (D-039 freeze triggers), not from this gate. In-scope code (`ingest.py`, `pipeline.py`) is unchanged from d148e0f to HEAD.

Not a finding: the run-path warning says "No model was available" for a fixture miss. `memory/contracts/api.md` defines `NO_MODEL` as "no model or recorded answer", and the detail `FIXTURE_MISS` is kept in `errors`. I accept this as documented.

## Exercised

- Pinned: `git archive d148e0f` into scratchpad `t066r2/base`. Full diff read: `git show d148e0f -- app/backend/ingest.py app/backend/pipeline.py memory/contracts/api.md tests/unit/test_split_llm.py`.
- `git diff --stat d148e0f HEAD -- app/backend/ingest.py app/backend/pipeline.py` (empty). `grep -n` on HEAD for the cited lines: `ingest.py:262, 266, 299, 301`; `test_split_llm.py:17, 344, 363`.
- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_split_llm.py` on the pinned copy: 37 passed. Full `tests/unit`: 937 passed. On HEAD 312ed92: `tests/unit/test_split_llm.py` 42 passed.
- Probe `probe_run.py` (run path through `run_pipeline`, empty `LLM_FIXTURE_DIR`): unsplit paste gives `split_failure NO_MODEL`, error `('split','LLM_FAILED_AFTER_RETRIES','FIXTURE_MISS')`; tail paste gives `split_failure NOT_ATTEMPTED`, no split error.
- Probe `probe_ingest.py` (creation path): tail paste gives 3 records, `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` (NOT_ATTEMPTED); unlabelled single block gives NO_MODEL; complete two-record paste gives `split_method code`, no warning.
- Probe `probe_single.py` on pinned d148e0f and on HEAD 312ed92 archive: single labelled record missing its excerpt gives `NOT_ATTEMPTED` with the "several records" message (U1 and U3); single labelled record missing its source gives NO_MODEL (U2).
- Probe `probe_gate.py` (spy splitter that counts calls) on pinned d148e0f, on the gate-removed mutant (M7) at d148e0f, and on HEAD 312ed92 plus M7: base 0 calls; M7 1 call, split_failure NO_MODEL.
- Mutants via `mutate_r2.py` on the pinned copy (each emission removed or altered; results in `mutants.txt`): E1 1 failed; E2 1 failed; E3 1 failed; E4 1 failed; E5 1 failed; E6 1 failed; M7 37 passed (survivor).
- Read `docs/LLM_VS_CODE.md:29` (row 1, which defines the NOT_ATTEMPTED scope), `memory/contracts/api.md:70-80`, `memory/DECISIONS.md` ADR-018 (line 341), `reviews/T-066-staff-engineer.md` (r1).
- Evidence: `artifacts/review-evidence/T-066-staff-engineer-r2/` (outputs.txt, mutants.txt, probe and mutation scripts).
- Not exercised: the web UI rendering of the warnings; the claude-cli backend; E2E specs.

## Findings

**Major 1: NOT_ATTEMPTED fires for a single incomplete labelled record, and the warning claims several records.**
Evidence: `artifacts/review-evidence/T-066-staff-engineer-r2/outputs.txt`, section "probe_single": input `Date: 2026-03-03\nSource: Clinic A\n` (one labelled record, no excerpt) gives `records 1 | split_method ambiguous | split_failure NOT_ATTEMPTED`, and the warning text is "The paste has several records and some text outside them; the AI is only asked to split a single unsplit block, so that text stays its own record (NOT_ATTEMPTED)." The same happens on HEAD 312ed92. Cause: `app/backend/ingest.py:266` (`elif method == "ambiguous" and not eligible:` assigns NOT_ATTEMPTED to every non-eligible ambiguous paste), and `ingest.py:300-301` (the message). `docs/LLM_VS_CODE.md:29` defines NOT_ATTEMPTED as "several records are followed by an unsplit tail".
Why it matters: the warning states a fact about the paste that is false (one record, no outside text). CLAUDE.md non-negotiable 5 says the product may not invent facts, and D.2 lists "invents facts" under blocker. I rate it major, not blocker, because the false claim is confined to a warning string. Record counts, dates, amounts, totals and export are unchanged. If Chris reads "invents facts" as covering warning text, re-rate to blocker (see question 2). The doc row and the code disagree, so the checklist item "implementation matches the table row" fails for this input.
Fix: narrow the NOT_ATTEMPTED branch to `len(recs) > 1`. For a single incomplete record, emit either no reason or a separate code whose message describes that state. The orchestrator names the code and records it in `memory/ORCHESTRATOR_DECISIONS.md`. Update row 1 if the scope changes.
Acceptance test: `IN.ingest("Date: 2026-03-03\nSource: Clinic A\n")` produces no SPLIT_REJECTED message containing "several records". The existing tail test still gets NOT_ATTEMPTED.

**Major 2: the single-record eligibility gate is unpinned; the splitter is called on a multi-record paste when it is removed.**
Evidence: `app/backend/ingest.py:262`: `eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or ...)`. Mutant M7 (`len(recs) == 1 and` removed) on the pinned copy: `37 passed in 0.64s` (`mutants.txt`). On HEAD 312ed92 plus M7: `42 passed`. `probe_gate.py` input: a first unlabelled line, `---`, then two labelled records. Base: `splitter called: 0 | split_failure NOT_ATTEMPTED`. M7: `splitter called: 1 | split_failure NO_MODEL`.
Why it matters: row 1 says the model is only asked about a single block. With the gate removed, the model gets a multi-record paste, and no test fails. This is r1 F2 (r1 mutant M3), still open. The tail test does not reach the gate, because its first record is complete and labelled.
Fix: add a test with a complete-or-unlabelled first block followed by two labelled records. A spy splitter must record zero calls, and the result must be NOT_ATTEMPTED.
Acceptance test: the new test fails on M7 (currently 37 passed) and passes on d148e0f.

## What is right

- Run path: NO_MODEL with the FIXTURE_MISS cause kept in `errors` (`pipeline.py:258-259`); the run result carries `split_method` and `split_failure` (`pipeline.py:361`). This closes r1 F1, F3 and F4.
- Six emissions removed one at a time (E1-E6) each turn at least one test red (`mutants.txt`). The new tests go through `run_pipeline`, not only `ingest()`.
- In the current code a multi-record paste never calls the splitter (`probe_gate.py` base: 0 calls), and the tail test passes a splitter that fails the test if it is called.

```json
{"card": "T-066", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit d148e0f (app/backend/ingest.py, app/backend/pipeline.py, memory/contracts/api.md, tests/unit/test_split_llm.py); pinned via git archive into scratchpad t066r2/base; HEAD 312ed92 checked for in-scope drift (ingest.py and pipeline.py unchanged from d148e0f); no app URL exercised; inputs are synthetic test strings",
 "exercised": [
  "git show d148e0f (full diff of the four scope files); git diff --stat d148e0f HEAD on ingest.py and pipeline.py (empty)",
  "pytest tests/unit/test_split_llm.py on pinned d148e0f: 37 passed; pytest tests/unit on pinned d148e0f: 937 passed; on HEAD 312ed92 split file: 42 passed",
  "probe_run.py: run_pipeline with AU.make_call and empty LLM_FIXTURE_DIR: unsplit paste gives NO_MODEL plus split errors cause FIXTURE_MISS; tail paste gives NOT_ATTEMPTED with no split error",
  "probe_ingest.py: creation path: tail paste gives NOT_ATTEMPTED; unlabelled single block gives NO_MODEL; complete two-record paste gives no reason",
  "probe_single.py: labelled single record missing excerpt gives NOT_ATTEMPTED with 'several records' text (pinned and HEAD 312ed92); missing source gives NO_MODEL",
  "probe_gate.py with spy splitter: base 0 calls; gate-removed mutant M7 1 call (pinned and HEAD)",
  "mutate_r2.py on pinned copy: E1-E6 each 1 failed; M7 37 passed (survivor)",
  "read docs/LLM_VS_CODE.md:29, memory/contracts/api.md:70-80, memory/DECISIONS.md:341, reviews/T-066-staff-engineer.md, ingest.py:262-302, pipeline.py:255-262, 355-362"
 ],
 "verdict": "changes",
 "scores": {"contract_match_llm_vs_code_row1": 3, "run_path_reason_visible": 5, "tail_reason_visible": 3, "test_strength_split_reasons": 3, "failure_visibility_no_swallowed_errors": 4},
 "findings": [
  {"severity": "major",
   "title": "NOT_ATTEMPTED fires for a single incomplete labelled record, and the warning says several records",
   "evidence": "outputs.txt probe_single: input 'Date: 2026-03-03\\nSource: Clinic A\\n' gives records 1, split_failure NOT_ATTEMPTED, SPLIT_REJECTED 'The paste has several records and some text outside them ...'. Same on HEAD 312ed92. Cause: app/backend/ingest.py:266 (elif method == 'ambiguous' and not eligible assigns NOT_ATTEMPTED to every non-eligible ambiguous paste); ingest.py:300-301 (message). docs/LLM_VS_CODE.md:29 defines NOT_ATTEMPTED as 'several records are followed by an unsplit tail'.",
   "why_it_matters": "The warning states a false fact about the paste (one record, no outside text). CLAUDE.md non-negotiable 5 and D.2 'invents facts'. Rated major, not blocker, because the claim is confined to a warning string; records, dates, amounts, totals and export are unchanged. Re-rate to blocker if Chris reads warning text as covered by 'invents facts'. The table row and the code disagree for this input.",
   "fix": "Narrow the NOT_ATTEMPTED branch to len(recs) > 1. For a single incomplete record, emit no reason or a separate code whose message describes that state. Orchestrator names the code and records it in memory/ORCHESTRATOR_DECISIONS.md; update LLM_VS_CODE row 1 if scope changes.",
   "acceptance_test": "IN.ingest('Date: 2026-03-03\\nSource: Clinic A\\n') produces no SPLIT_REJECTED message containing 'several records'; the existing tail test still gets NOT_ATTEMPTED."},
  {"severity": "major",
   "title": "Single-record eligibility gate is unpinned; removing it sends a multi-record paste to the splitter",
   "evidence": "app/backend/ingest.py:262 eligible = method == 'ambiguous' and len(recs) == 1 and (...). mutants.txt: M7 (len gate removed) 37 passed on pinned d148e0f; 42 passed on HEAD 312ed92 plus M7. probe_gate.py (first unlabelled line, ---, two labelled records): base splitter called 0 times, split_failure NOT_ATTEMPTED; M7 splitter called 1 time, split_failure NO_MODEL.",
   "why_it_matters": "docs/LLM_VS_CODE.md:29 says the model is only asked about a single block. With the gate removed the model receives a multi-record paste and no test fails. Carried from r1 F2 (r1 mutant M3). The tail test does not reach the gate because its first record is complete and labelled.",
   "fix": "Add a test whose first block is unlabelled, followed by two labelled records, with a spy splitter that must record zero calls and a result of NOT_ATTEMPTED.",
   "acceptance_test": "The new test fails on mutant M7 (currently 37 passed) and passes on d148e0f."}
 ],
 "whats_right": [
  "Run path: NO_MODEL with the FIXTURE_MISS cause kept in errors (pipeline.py:258-259); run result carries split_method and split_failure (pipeline.py:361). Closes r1 F1, F3 and F4.",
  "Six emissions removed one at a time (E1-E6) each turn at least one test red; the new tests go through run_pipeline, not only ingest().",
  "In the current code a multi-record paste never calls the splitter (probe_gate base: 0 calls), and the tail test passes a splitter that fails the test if it is called."
 ],
 "questions_for_chris": [
  "Model policy: CLAUDE.md section 6 assigns engineering reviewers to Sonnet. This review ran as claude-haiku-5-5. Should T-066 be re-reviewed on Sonnet before the record counts?",
  "Severity: is a warning that states a false fact about the paste an 'invented fact' under D.2 (blocker), or a major as I rated it? The answer decides whether Major 1 is a blocker.",
  "Should a single incomplete labelled record carry any SPLIT_REJECTED reason at all? If not, Major 1's fix is to emit nothing for that case; if yes, which code and message?"
 ]}
```
