# T-080 round-4 review: export gate single list, pending as warnings (D-044/D-045), commit 10d358e

Scope: commit 10d358e (backend: app/backend/trace.py, export.py, export_routes.py, api.py, store.py; tests/unit/test_trace.py, tests/unit/test_export.py; memory/contracts/api.md). HEAD is 8d7548d, and `git diff --name-only 10d358e HEAD -- app tests` is empty, so the reviewed backend is HEAD's backend. Verdict: **pass** (0 blockers, 0 majors; 2 minors, 1 nit).

Round-3 status: the r3 major (pending items block the gate, D-045(a) not implemented) is closed. The r3 judges-step minor and the r3 build_export nit are closed. The r3 rejudge-scope minor is still open (finding 1 below).

## Answers to the brief

- **Gate and GET /export share one blocker list; gate.ready == export allowed: confirmed.** `trace.export_blockers` (trace.py:922) is the only producer. The gate reads it at trace.py:889 and sets `ready = not blockers` at trace.py:894. The export reads it through store.py:78 and export_routes.py:28 refuses on it. The only other refusal is build_export's JudgeNotRun (export.py:586-587), on a subset of the same list. `grep -rn "build_export\|export_payload" app` shows no other export caller. Test `test_gate_ready_equals_export_allowed_in_every_state_d045` (test_trace.py:781) asserts `g["ready"] == (ex.status_code < 400)` and identical blocker lists in nine states: nothing decided, one accepted, all but one accepted, judge not run, judges answered with one pending, run failed, run in progress, all clear, everything dismissed. It passes.
- **Pending items are warnings, not blockers: confirmed.** PENDING_DECISION and DATE_UNCONFIRMED are gone from `blockers`. Pending items go to `warnings` (trace.py:897, `ITEMS_NOT_REVIEWED`) and to `counts.pending_items` (trace.py:892). The date guard still stops an unconfirmed date from being accepted or edited into the letter (review.py:67, D-041), so dropping DATE_UNCONFIRMED from blockers opens no path to an unconfirmed date in the letter. The committed frontend already reads `gate.status === "pass"` (app/frontend/stepper.js:455 in the working tree; the same branch is at stepper.js:350 at 10d358e), so the "Export blocked by N" text for pending items is gone.
- **NOTHING_ACCEPTED, run failed and run in progress return 422 export_blocked: refusal is reasonable; the status code is the weak part.** Fail-closed is right: a letter with nothing accepted is empty, a letter from a failed run is partial, and a letter from a run still writing is unfinished. No fact is invented in any of the three. The 422 choice is finding 2 (minor). Tests: test_trace.py:830 (RUN_FAILED gives 422 export_blocked); the invariant test covers NOTHING_ACCEPTED (test_trace.py:820, 422) and RUN_IN_PROGRESS.
- **Paralegal-written summaries are not counted as unchecked: confirmed in all three readers.** `_paralegal_wording` (trace.py:667) is used by `_judge_never_ran` (trace.py:656, gate and /judges), by `unjudged_items` (trace.py:672 onward, the rejudge target list), and by `judge_report` through `_judge_rows` (trace.py:637). The edit path still runs judge 1 on every edited summary (review.py:101), and a judge objection still returns 409 (R-RV-3, tests/unit/test_review_rules.py:95). So the exemption only removes the "never ran" blocker. Finding 3 is about the wording of D-045(b).
- **The invariant test fails when the shared list is broken in a scratch copy: confirmed.** Mutants M1 (gate drops JUDGE_NOT_RUN), M2 (store passes no blockers), M5 (NOTHING_ACCEPTED dropped), and M7 (gate ready ignores blockers) each fail the invariant test. M3 (export_payload guard removed) fails only the invariant test, so that guard has one test behind it. Full table below.

## Findings

### 1. minor: rejudge re-asks pending unjudged items (r3 finding 2, still open)
Evidence: `app/backend/rejudge.py:60` `targets = trace.unjudged_items(conn, case_id)`. `app/backend/trace.py:672-684` filters out only rejected and dismissed items, so pending items are included. `tests/unit/test_trace.py:906` `assert r["asked"] == n`, where `_blank_judges` (test_trace.py:492) blanks pending rows too. Repro: `.venv/bin/python -m pytest -q tests/unit/test_trace.py::test_rejudge_only_touches_items_whose_judge_never_ran` (passes, so the behaviour is codified).
Why it matters: D-044 (memory/ORCHESTRATOR_DECISIONS.md:52) says the rejudge "re-judges just those items", meaning the items the gate lists. Pending items get extra audited model calls. No review_status changes and no state changes follow, so this stays minor. But it is a literal deviation from a binding decision, and the test now locks it in.
Fix: filter the targets to `review_status` in (accepted, edited) in rejudge.py:60, or amend D-044 in memory/DECISIONS.md to name pending items and update test_trace.py:906.
Acceptance test: 4 accepted and 8 pending unjudged items give `asked == 4`. Or DECISIONS names 12 and the test asserts 12.

### 2. minor: export refusals use 422 for state conflicts (run in progress, run failed, nothing accepted, judge not run)
Evidence: `app/backend/export_routes.py:69-71` returns `status_code=422` for every `ExportBlocked`, with `error.code` set to `e.code`. `tests/unit/test_trace.py:830` asserts `error.code == "export_blocked"` for RUN_FAILED. The invariant test (test_trace.py:781) covers all four states.
Why it matters: the refusal is right; the status code is a judgment call. 422 means the request content is invalid, and these are state conflicts. The spec already reserves 409 for state and judge objections (spec/REQUIREMENTS.md:94, R-RV-3: "judge or token objections are 409, never 422"). The UI keys on `error.code` (app/frontend/export.js:51 and the comment at stepper.js:474; no status-code branch found), so a change is cheap. The spec names no export status code, so this is minor and not a spec violation.
Fix: return 409 for all four export refusals, or record in memory/DECISIONS.md why D-044's 422 stands, and say so at memory/contracts/api.md:30 and :286.
Acceptance test: GET /export during a run returns the chosen status (409 or the recorded code), `error.code` is `export_blocked`, and `detail.blockers` lists RUN_IN_PROGRESS.

### 3. nit: D-045(b) says "exempt from the judge"; the code exempts only the second-check blocker and the /judges counts
Evidence: memory/ORCHESTRATOR_DECISIONS.md:53 says "(b) ... exempt from the judge but still passes the D-034 code checks". app/backend/review.py:101 still calls `judges.run_j1_meta` on every edited summary. The exemption is at trace.py:656 and trace.py:667-669 only.
Why it matters: the behaviour is right (R-RV-3 holds). The decision text overstates the exemption, and a later reader could remove the edit-time judge on the strength of it.
Fix: reword D-045(b) to "exempt from the second-check blocker and the /judges counts; judge 1 still runs at edit time (R-RV-3)".
Acceptance test: none beyond the wording. `grep -n "exempt from" memory/ORCHESTRATOR_DECISIONS.md` shows the reworded sentence.

## Mutation run (scratch copy of commit 10d358e, not committed)

Scratch copy: `git archive 10d358e` into the session scratchpad, tests run with `/Users/arsis/zlayt-pm-project/.venv/bin/python` from that copy (its `app` import resolves to the copy). Each mutant changes one anchor string (asserted to occur exactly once). Command: `pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider`. Output saved at `artifacts/review-evidence/T-080-r4/mutation_output.txt`, scripts at `artifacts/review-evidence/T-080-r4/run_mutants.py` and `run_m4b.py`.

| Mutant | Result |
|---|---|
| baseline (10d358e) | 79 passed |
| M1 gate drops JUDGE_NOT_RUN from the shared list (trace.py:889) | 9 failed, invariant test among them |
| M2 store.export_case passes no blockers (store.py:78) | 4 failed, invariant test among them |
| M3 export_payload guard removed (export_routes.py:28) | 1 failed (the invariant test only) |
| M4 pending items block again (clean version, DB.list_items, PENDING_DECISION) | 7 failed, including test_pending_live_items_are_a_warning_not_a_blocker_d045 |
| M5 NOTHING_ACCEPTED dropped from the shared list (trace.py:934) | 4 failed, invariant test among them |
| M6 paralegal exemption removed from _judge_never_ran (trace.py:656) | 2 failed (both d045b tests) |
| M7 gate ready ignores non-NOTHING_ACCEPTED blockers (trace.py:894) | 4 failed, invariant test among them |

M4 in the first run used a crude mutant that also raised KeyError in unrelated tests. The clean M4 (M4b above) is the one reported.

## Exercised

- Read personas/staff-engineer.md; reviews/T-080-staff-engineer-r3.md; memory/ORCHESTRATOR_DECISIONS.md lines 52-53 (D-044, D-045); spec/REQUIREMENTS.md lines 94, 122-123; memory/contracts/api.md lines 30, 286, 536-543.
- `git show 10d358e --stat`; `git show 10d358e -- app/backend/{trace,export,export_routes,api,store}.py tests/unit/test_trace.py`; test_export.py lines 185-197.
- `.venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider`: 79 passed in 4.65s. The same command without the flag: 79 passed in 5.49s, then 79 passed in 5.12s (reproducible).
- Baseline and eight mutants in the scratch copy (table above).
- `grep -n` for callers of build_export, export_payload, export_blockers, judge_not_run, JudgeNotRun, ExportBlocked across app/ and tests/.
- `git show 10d358e -- app tests | grep "^+"` for float(, bare except, except Exception, sleep(, requests, httpx, urllib, anthropic, time.time(): no matches.
- `git diff --name-only 10d358e HEAD -- app tests`: empty.
- Frontend at 10d358e: app/frontend/stepper.js:350-352 (gate text), app/frontend/export.js:39 (copy confirm when `c.pending` is non-zero), and every "422" hit in app/frontend (comments only).
- Not exercised: no live server was started. The run-state and nothing-accepted 422 cases were exercised through the TestClient, with case status set to failed or running in the invariant test.
- Out of scope: the working tree has uncommitted edits to app/frontend/*.js and tests/unit/test_eval_runner.py, plus an untracked tests/unit/test_t093_eval_signature.py (from `git status --short`). They are not part of 10d358e and were not reviewed.
- Not checked: the frontend behaviour beyond the gate text and the copy confirm (UX is outside my lens).

## What's right

1. One function (`trace.export_blockers`, trace.py:922) feeds the gate and the export refusal, so the gate cannot pass over a blocker the export refuses. The invariant test checks this across nine states, and M1, M2, M5 and M7 each fail it.
2. Pending-as-warning is safe because a pending item with an unconfirmed date cannot be accepted (review.py:67, D-041). M4 (pending blocks again) fails seven tests.
3. The paralegal-wording exemption is applied the same way in the gate, the /judges counts and the rejudge target list (`_paralegal_wording`, trace.py:667). M6 is killed by both d045b tests.

```json
{"card": "T-080", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 10d358e (app/backend/trace.py, export.py, export_routes.py, api.py, store.py; tests/unit/test_trace.py, test_export.py; memory/contracts/api.md) with D-044/D-045 in memory/ORCHESTRATOR_DECISIONS.md lines 52-53; HEAD 8d7548d has no app/backend or tests/unit changes since 10d358e; scratch copy of 10d358e; no live server",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-080-staff-engineer-r3.md, memory/ORCHESTRATOR_DECISIONS.md D-044/D-045, spec/REQUIREMENTS.md lines 94 and 122-123, memory/contracts/api.md lines 30, 286, 536-543",
  "git show 10d358e --stat and diffs of app/backend/{trace,export,export_routes,api,store}.py and tests/unit/test_trace.py; test_export.py lines 185-197",
  ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider -> 79 passed in 4.65s; repeated twice more -> 79 passed (5.49s, 5.12s)",
  "scratch copy of 10d358e: baseline 79 passed; mutants M1, M2, M3, M5, M6, M7 and clean M4b killed (M1 9 failed, M2 4, M3 1, M4b 7, M5 4, M6 2, M7 4); output in artifacts/review-evidence/T-080-r4/mutation_output.txt",
  "grep for callers of build_export, export_payload, export_blockers, judge_not_run, JudgeNotRun, ExportBlocked across app/ and tests/",
  "git show 10d358e -- app tests | grep '^+' for float(, bare except, sleep(, network calls: none",
  "git diff --name-only 10d358e HEAD -- app tests: empty",
  "app/frontend/stepper.js:350-352 and export.js:39 at 10d358e; app/frontend 422 hits: comments only"],
 "verdict": "pass",
 "scores": {"single_blocker_list": 5, "pending_warning_not_blocker": 5, "nothing_accepted_and_run_refusals": 4, "paralegal_exemption_consistency": 5, "invariant_test_strength": 5, "export_status_code_convention": 3, "rejudge_scope_d044": 3, "tests_reproducible": 5},
 "findings": [
  {"severity": "minor", "title": "Rejudge re-asks pending unjudged items (r3 finding 2, still open)",
   "evidence": "app/backend/rejudge.py:60 `targets = trace.unjudged_items(conn, case_id)`; app/backend/trace.py:672-684 filters only rejected and dismissed, so pending items are included; tests/unit/test_trace.py:906 `assert r[\"asked\"] == n`, with _blank_judges (test_trace.py:492) blanking pending rows too. Repro: .venv/bin/python -m pytest -q tests/unit/test_trace.py::test_rejudge_only_touches_items_whose_judge_never_ran",
   "why_it_matters": "D-044 (memory/ORCHESTRATOR_DECISIONS.md:52) says rejudge 're-judges just those items' (the gate's list). Pending items get extra audited model calls. No review_status or state change follows, so minor; but it is a literal deviation from a binding decision and the test now codifies it.",
   "fix": "Filter rejudge targets to review_status in (accepted, edited) at rejudge.py:60, or amend D-044 in memory/DECISIONS.md to name pending items and update test_trace.py:906.",
   "acceptance_test": "4 accepted and 8 pending unjudged items: asked == 4 (or DECISIONS names 12 and the test asserts 12)."},
  {"severity": "minor", "title": "Export refusals use 422 for state conflicts (run in progress, run failed, nothing accepted, judge not run)",
   "evidence": "app/backend/export_routes.py:69-71 returns status_code=422 for every ExportBlocked, with error.code = e.code; tests/unit/test_trace.py:830 asserts error.code == 'export_blocked' for RUN_FAILED; invariant test test_trace.py:781 covers all four states; spec/REQUIREMENTS.md:94 (R-RV-3): 'judge or token objections are 409, never 422'.",
   "why_it_matters": "Refusing these exports is correct (fail-closed: empty, partial or still-writing letter). The status code is the issue: 422 means invalid request content; these are state conflicts, and the spec already uses 409 for state objections. The UI keys on error.code (app/frontend/export.js:51), so a change is cheap. The spec names no export status code, so minor, not a spec violation.",
   "fix": "Return 409 for all four export refusals, or record in memory/DECISIONS.md why D-044's 422 stands and update memory/contracts/api.md lines 30 and 286.",
   "acceptance_test": "GET /export during a run returns the chosen status (409 or the recorded code), error.code export_blocked, detail.blockers lists RUN_IN_PROGRESS."},
  {"severity": "nit", "title": "D-045(b) says 'exempt from the judge'; the code exempts only the second-check blocker and the /judges counts",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:53 '(b) ... exempt from the judge but still passes the D-034 code checks'; app/backend/review.py:101 still runs judges.run_j1_meta on every edited summary; exemption at app/backend/trace.py:656 and trace.py:667-669 only.",
   "why_it_matters": "The behaviour is right (R-RV-3 holds: objection gives 409, tests/unit/test_review_rules.py:95). The decision text overstates the exemption, and a later reader could drop the edit-time judge on that basis.",
   "fix": "Reword D-045(b): 'exempt from the second-check blocker and the /judges counts; judge 1 still runs at edit time (R-RV-3)'.",
   "acceptance_test": "grep -n 'exempt from' memory/ORCHESTRATOR_DECISIONS.md shows the reworded sentence; no test change."}
 ],
 "whats_right": [
  "One function (trace.export_blockers, trace.py:922) feeds both the gate and the export refusal, so the gate cannot pass over a blocker the export refuses; the invariant test checks nine states, and M1, M2, M5 and M7 each fail it.",
  "Pending-as-warning is safe because a pending item with an unconfirmed date cannot be accepted (review.py:67, D-041); M4b (pending blocks again) fails seven tests.",
  "The paralegal-wording exemption is applied the same way in the gate, the /judges counts and the rejudge target list (_paralegal_wording, trace.py:667); M6 is killed by both d045b tests."
 ],
 "questions_for_chris": ["A failed run with accepted items currently blocks export until the run is re-run (RUN_FAILED, fail-closed). Should it instead export with a visible 'run incomplete' note? I have assumed blocking; the product call is yours."]}
```
