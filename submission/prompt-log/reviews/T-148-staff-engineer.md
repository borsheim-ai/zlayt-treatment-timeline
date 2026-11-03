# T-148 review: staff-engineer-reviewer

Verdict: pass (no blocker, no major; two minors, both about test strength, not product behaviour).

Scope: commit d19ae46 (`app/backend/case_list.py`, `api.py` route and `/status` hunk, `memory/contracts/api.md`, `tests/unit/test_case_list.py`). I exercised a `git archive HEAD` copy. HEAD is 07c7558; `git diff d19ae46 HEAD --stat` over case_list.py, present.py, api.py, trace.py and test_case_list.py is empty, so nothing in scope moved.

- Drift: every summary field is derived from `present.review_view`, `run_progress` (shared with `/status`) and the `export_gate` step of `trace.case_trace`. I mutated `case_list.py` 14 ways on a scratch copy. 11 turned the test red (edit_unconfirmed, rejected filter, tray count, needs_review, export_ready forced True, warnings dropped, blocker `why` dropped, edits_to_check wrong source, ingest stage fallback, steps_total, plus the ready/warning cases). Survivors: `handled` and `is_filtered` filters (equivalent mutants: handled placeholders and filtered flags are already `state == "rejected"`, which `_progress` excludes), `run.running` and `run.error` (see F1).
- HITL call-outs: needs_review, edits_to_check, could_not_verify (= GET case `tray` length), blockers and warnings carry the trace's plain `why`. A failed case shows blockers `RUN_FAILED, NOTHING_ACCEPTED` and `/export` answers 422; a running case shows `RUN_IN_PROGRESS`; the two agree with the gate.
- Local mode: 404 outside `ZLAYT_MODE=local`; the D-036 middleware returns 403 for a non-loopback peer (probe: peer 203.0.113.9 gave 403 `forbidden`; `::1` gave 200); `tests/unit/test_api_routes.py:347` covers this on `/api/cases`.
- Performance and LLM: 50 cases (15 run, 35 ingested) listed in 91-100 ms; audit call counts for three cases unchanged by the list call; no pipeline or model import on the path.
- Old fields: token, name, status, source, record_count, counts, created_at all present; `app/frontend/switcher.js` reads exactly those.

```json
{"card": "T-148", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit d19ae46 (HEAD 07c7558, no in-scope diff since): app/backend/case_list.py, api.py list route and /status hunk, memory/contracts/api.md, tests/unit/test_case_list.py; git archive HEAD copy; 15 library cases under the fixture backend, local mode",
 "exercised": [
  "python3 tools/board.py show T-148; read memory/contracts/api.md GET /api/cases section; git show d19ae46 for case_list.py and api.py",
  "git archive HEAD into a scratch dir; .venv/bin/python -m pytest tests/unit/test_case_list.py -q -> 7 passed in 3.05s",
  "full tests/unit on the archive: pytest tests/unit -q -x, exit code 0 (2 skips, no failures)",
  "14 single-line mutants of case_list.py on a scratch copy, each followed by test_case_list.py (11 red; handled and is_filtered are equivalent, run.running and run.error survive)",
  "scripted probe on the archive: 15 library cases run, GET /api/cases vs GET case tray length (equal for all 15), error flag false",
  "50-case list timing (3 runs): 100, 91, 93 ms; audit calls for 3 cases identical before and after the list call",
  "peer probes: 203.0.113.9 -> 403 forbidden; ::1 -> 200; ZLAYT_MODE unset -> 404",
  "scripted failed case (status failed + error set) and running case: blockers RUN_FAILED / RUN_IN_PROGRESS and /export 422",
  "read app/frontend/switcher.js for the old fields it consumes; read present.review_view, present tray build, flags._to_tray, generator.resolved_placeholders"
 ],
 "verdict": "pass",
 "scores": {"determinism_and_no_llm": 5, "drift_resistance": 4, "hitl_honesty": 4, "local_mode_gating": 5, "test_strength": 3, "backward_compat": 5},
 "findings": [
  {"severity": "minor", "title": "Test does not pin run.running or run.error; one assertion cannot fail",
   "evidence": "Mutating case_list.py `\"running\": case[\"status\"] == \"running\"` to False, and `\"error\": bool(case.get(\"error\"))` to False, both leave all 7 tests green (7 passed). tests/unit/test_case_list.py:89 compares running with the same expression on the same field and no test reads GET case `error` against run.error. tests/unit/test_case_list.py:115 is `A and B or C`, where C (`last_activity_at >= updated_at`) is already asserted at line 87, so the line cannot fail for the decisions it names.",
   "why_it_matters": "A failed case is the one a paralegal most needs flagged on the overview; the failed-run flag is the field a drift would hit and nothing would notice. The weak line gives false comfort that decisions move last_activity_at.",
   "fix": "Add a failed case (set status/error through the store, as the probe did) and a running case to the fixture set; assert run.error == bool(GET case error) and run.running == (GET /status status == running). Replace line 115 with two plain asserts: the case that took decisions has last_activity_at > updated_at, and the untouched case has last_activity_at == updated_at.",
   "acceptance_test": "Mutants `running -> False` and `error -> False` in case_list.py turn tests/unit/test_case_list.py red; line 115 fails if last_activity_at is not advanced by a review event."},
  {"severity": "minor", "title": "No case with a manual-entry-handled placeholder or a rule-filtered proposal in the comparison set",
   "evidence": "Removing the `handled` or `FT.is_filtered` clause from `_progress` (case_list.py) leaves 7 passed. They are equivalent today because both kinds of item are `state == rejected`, but if either stops being rejected the list would count them in progress totals and nothing in test_case_list.py would show it; the 15 library cases under the fixture backend contain neither.",
   "why_it_matters": "The two clauses duplicate present.review_view's filter, so they can drift the day one changes; the comparison only protects the cases the fixture produces.",
   "fix": "Either drop the redundant clauses and compute total from present.review_view's own item set (one source), or add a case with a T-110 manual entry over a placeholder and a D-057 filtered flag (tests/unit/test_lib09_t110_r2.py and test_t126_filtered_by_rule.py already build them) to the comparison.",
   "acceptance_test": "A test builds a case with a handled placeholder and a filtered flag and asserts progress totals equal GET case live item counts and hitl.could_not_verify equals len(tray)."}
 ],
 "whats_right": [
  "Fields come from the functions GET case, /status and the export gate already use (run_progress is shared with the /status route), and the test compares them route by route for all 15 library cases.",
  "Gate blockers and warnings are copied from the trace with their plain `why`, and export_ready agrees with GET /export (200 vs 422) in every state I probed, including failed and running.",
  "Code only, about 100 ms for 50 cases, 403 for non-loopback peers, and all pre-existing list fields kept for switcher.js."
 ],
 "questions_for_chris": []}
```
