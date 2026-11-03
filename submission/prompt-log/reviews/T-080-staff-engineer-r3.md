# T-080 round-3 review: D-044 judge export gate, D-045 scope (staff-engineer-reviewer)

Scope: commit fe4ee80 (D-044 gate, export 422, POST /rejudge, tests) with the D-045 docs commit f49c4c2 on top. HEAD moved to 8d7548d during the review; `git diff --name-only fe4ee80 HEAD -- app/backend tests/unit` is empty, so the backend reviewed is the fe4ee80 backend. Frontend as loaded by the live instance is the HEAD of that time (8e3c26c and f49c4c2 frontend).

Verdict: **changes** (0 blockers, 1 major, 2 minors, 1 nit). Against the brief's checks: the JUDGE_NOT_RUN gate blocker and the 422 hold live; the paralegal-summary exemption and the D-034 number check hold live; rejudge is audited and fixture-only in demo mode. Two checks fail: rejudge re-asks pending items too, and pending items still block the gate (D-045(a) is not implemented; the export endpoint itself does not block on pending).

## Answers to the brief

- **Accepted LLM-made item whose judge never ran is a JUDGE_NOT_RUN gate blocker: confirmed.** Live: accepted e1, e2, a1, a2 after blanking their judge records; `/trace` export_gate `blockers` has four `JUDGE_NOT_RUN` entries, `next_action` `RERUN_JUDGE`, gate `counts.judge_not_run` 4.
- **GET export returns 422 judge_not_run: confirmed.** Live: `GET /api/cases/<tok>/export` gave 422 with `error.code` `judge_not_run` and `detail.blockers` naming the same four ids. After `POST /rejudge` the same GET gave 200.
- **POST rejudge re-judges only those items: not confirmed.** Live: `asked` 12 = the four accepted blocked items plus eight pending unjudged items (a4, e3 to e9). See finding 2.
- **Audited, fixture-only in demo mode: confirmed.** Live: 12 new `llm_calls` rows, all `backend` fixture, `role` judge; `ladder.rejudge` trail present on e1, a1. Demo guard: `api.py:360-376` plus `provider.backend_name` (fixture unless ENABLE_LIVE=1); mutant M6 killed by `test_rejudge_is_refused_in_the_cases_the_run_route_refuses`.
- **Paralegal-written or edited summaries exempt from the judge, still code-checked (D-034): confirmed for the gate and the code check.** Live: edit of e3 summary with no new number left e3 out of JUDGE_NOT_RUN; edit adding `987` (not in the quote) gave 422 `invalid_edit` with `SUMMARY_NUMBER_NOT_IN_EXCERPT`. But the judges step still counts e3 as unchecked: finding 3.
- **Pending items do not block export: export endpoint yes, gate no.** Live with 18 pending: `GET /export` 200, internal notes "Items not reviewed: 18" (D-045(a) AI line counts them), pending excluded from the letter. But `/trace` export_gate `ready` False with 18 `PENDING_DECISION` blockers. Finding 1.

## Findings

### 1. major: pending items still block the gate; D-045(a) is not implemented
Live (scratch case, 18 pending, 4 accepted): `/trace` export_gate `ready: False`, `blockers` = 18 x `PENDING_DECISION`, verdict "18 items still need your decision". Code: `app/backend/trace.py:889-895` (live pending becomes PENDING_DECISION or DATE_UNCONFIRMED blockers), `:901` `ready = ... and not blockers`, `:910` text "N items have no decision yet, so the export is blocked." UI: `app/frontend/stepper.js:352` "Export blocked by N"; the copy path does not block: `app/frontend/export.js:39` asks a confirm when `c.pending > 0`. Test codifies it: `tests/unit/test_trace.py:741-745` asserts `g["ready"] is False` with pending items.
Why it matters: D-045(a) (binding) says pending items never block export. R-EX-5 (`spec/REQUIREMENTS.md:123`) says copy asks one confirmation when anything is pending. The gate tells the paralegal the export is blocked while the Copy button works after one confirm. That is a false status, not an unsafe export: pending items stay out of the letter and the notes count them. Rated major, not blocker, because it is fail-closed and loses or invents no facts.
Fix: take PENDING_DECISION (and DATE_UNCONFIRMED, which is also a pending state) out of `blockers`; report pending as `counts.pending_items` and a confirm line. Keep `ready == (blockers == [])`, with ready also requiring no JUDGE_NOT_RUN and no run blocker. Rewrite `test_trace.py:741-745` and the `test_gate_and_export_agree_on_the_judge_dimension_in_every_state` expectations. Record the gate rule in `memory/DECISIONS.md`.
Acceptance test: sample case, accept all but one entry, judges answered. Assert `/trace` export_gate `ready` True and `blockers` []; `/export` 200; internal notes contain "Items not reviewed: 1". Then blank one accepted item's judge: gate `ready` False with only JUDGE_NOT_RUN, export 422.

### 2. minor: rejudge re-asks pending unjudged items, not only the blocked accepted ones
Live: `POST /api/cases/<tok>/rejudge` gave `asked: 12`; rejudged ids a1, a2, a4, e1, e2, e3 to e9. The blocked accepted items were e1, e2, a1, a2; a4 and e3 to e9 are pending. Code: `app/backend/rejudge.py:60` `targets = trace.unjudged_items(conn, case_id)`; `trace.py:667-679` returns live items regardless of review_status. Test `tests/unit/test_trace.py:829` `assert r["asked"] == n` codifies it.
Why it matters: D-044 says the rejudge "re-judges just those items" (the items the gate lists). Pending items get extra audited model calls. No `review_status` changes, so low impact.
Fix: either restrict targets to review_status accepted or edited, or record in `memory/DECISIONS.md` that pending unjudged items are also re-asked, and update the test.
Acceptance test: 4 accepted and 8 pending unjudged items: `asked` equals 4 (or the DECISIONS entry names 12 and the test asserts 12).

### 3. minor: judges step and /judges count a paralegal-edited summary as unchecked; D-045(b) exempts it
Live: e3 summary edited (no new number), judge unavailable on the edit. `/judges` totals `unavailable: 1`. `/trace` judges step `fail`, reason JUDGE_UNAVAILABLE, "1 item has not been double-checked", next `RERUN_JUDGE`. After dismissing the other pending items in the scratch case, export_gate `ready: True`, verdict "Ready to export", with the judges step still `fail`. Code: `trace.py:637-655` `_judge_rows` has no paralegal-wording exemption; `judge_report` (`trace.py:692`) counts from it. The exemption exists only in `unjudged_items` (`trace.py:676`).
Why it matters: the view shows a failed check, and a rerun action, on wording the spec says is human-authored, next to a gate that passes. An honest but contradictory state.
Fix: apply the same `entered_by` and edited-summary exemption in the judge counts and the judges step, or show the item as paralegal wording (not AI-checked).
Acceptance test: edit one entry summary so its judge is unavailable, dismiss the other pending items: judges step not `fail` on account of that item; gate `ready` True; verdict code `ready`.

### 4. nit: export refusal has no unit test in tests/unit/test_export.py
`export.py:576-577` raises `JudgeNotRun`; only the HTTP route tests cover it (`test_trace.py`). The mutant M5 is killed only through the API.
Fix: unit test calling `export.build_export` with `judge_not_run` set and asserting `JudgeNotRun` is raised, with the items.

## Mutation run (scratch copy of app, tests, evals, docs, spec, memory; not committed)
Baseline `tests/unit/test_trace.py tests/unit/test_export.py`: 75 passed.

| Mutant | Result |
|---|---|
| M1 gate ignores JUDGE_NOT_RUN (`trace.py` `blockers.extend(jnr)` to `pass`) | killed, 9 failed |
| M2 gate counts only `accepted` (drops `edited`) | killed, 1 failed |
| M3 paralegal-written summary not exempt (`unjudged_items`) | killed, 2 failed |
| M4 store.export_case passes no JNR (`store.py:78`) | killed, 4 failed |
| M5 build_export does not refuse (`export.py:576`) | killed, 4 failed |
| M6 rejudge skips demo fixture guard (rejudge route only, unique anchor) | killed, 1 failed |
| M7 rejudge answer does not recompose state (`rejudge.py` recompose) | killed, 2 failed |

## Checked and fine
- Rejudge writes go through `audited.py` `_DB_LOCK` (`audited.py:16`, `:82`), so the 4-thread pool shares the sqlite connection safely.
- `ready == (blockers == [])` held in every live state I probed (pending, JNR, rejudged, dismissed).
- D-034 hard 422 has no override in the edit path; the gate's JNR exemption does not clear on accept, edit or compare-by-hand (`test_no_override_...` passes).
- Trace and rejudge code: no `float(`, no bare `except`, no sleep, no network in the new code path (grep of `app/backend/rejudge.py` and the D-044 hunks in `trace.py`).

## What's right
1. The JUDGE_NOT_RUN blocker and the export 422 come from one function (`trace.judge_not_run_blockers`, read by `store.export_case` and the gate), so the live gate and export listed the same four ids, and both cleared after rejudge.
2. The paralegal-summary exemption and the D-034 check both behave live: `987` not in the quote gives 422; a text-only edit leaves e3 out of JUDGE_NOT_RUN.
3. Rejudge is audited (12 `llm_calls` rows, backend fixture, role judge) and fixture-only in demo mode; it never changes `review_status`.

```json
{"card": "T-080", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit fe4ee80 (backend: app/backend/trace.py, rejudge.py, api.py, export.py, export_routes.py, store.py; tests/unit/test_trace.py) with D-044/D-045 in memory/ORCHESTRATOR_DECISIONS.md (f49c4c2); HEAD moved to 8d7548d, no app/backend or tests/unit changes since fe4ee80; live instance 127.0.0.1:7996 (stopped), LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB scratch file, DATA_DIR empty sentinel; sample case",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-080-staff-engineer-r2.md, memory/ORCHESTRATOR_DECISIONS.md D-044 and D-045 (lines 52-53), spec/REQUIREMENTS.md R-EX-4 and R-EX-5 (lines 122-123)",
  "git show --stat and diffs of fe4ee80 (trace.py, api.py, export.py, export_routes.py, store.py) and f49c4c2; git diff --name-only fe4ee80 HEAD -- app/backend tests/unit (empty)",
  ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider -> 75 passed in 4.39s",
  "E2E_BASE_URL=http://127.0.0.1:7996 .venv/bin/python -m pytest -q tests/e2e/test_edit.py -p no:cacheprovider -> 9 passed in 11.43s",
  "live: POST /api/cases sample, POST /run, poll /status (ready); blanked 12 judge records in the scratch DB only; accepted e1, e2, a1, a2; GET /trace (gate: 4 JUDGE_NOT_RUN + 19 PENDING_DECISION at that point); GET /export -> 422 judge_not_run with the same 4 ids",
  "live: POST /rejudge -> 200, asked 12, rejudged 12, still_unavailable 0; new llm_calls 12, backend fixture, role judge; GET /export -> 200 with 18 pending; internal notes AI line 'Items not reviewed: 18'",
  "live: e3 judge removed and accepted (JUDGE_NOT_RUN appears), summary edit with '987' -> 422 invalid_edit SUMMARY_NUMBER_NOT_IN_EXCERPT, text-only summary edit -> 200 and e3 leaves JUDGE_NOT_RUN; GET /judges and /trace (judges step fail with 1 unavailable)",
  "live: dismissed the remaining pending items in the scratch case only -> /trace export_gate ready True, verdict Ready to export, judges step still fail",
  "live: ladder.rejudge trail read from the scratch DB for e1, a1, e3",
  "7 string mutants in a scratch copy (app, tests, evals, docs, spec, memory copied): M1 to M7 all killed (table above)",
  "data/zlayt.sqlite sha256 6d7dcf828093a1c07d3671046cf1c0c2e990b536c2e03289946a95f9eacc0593 and mtime 1793590231 before and after; sentinel DATA_DIR empty; scratch ZLAYT_DB file created (442368 bytes); server PID 62029 stopped and port 7996 confirmed free"],
 "verdict": "changes",
 "scores": {"jnr_gate_blocker": 5, "export_422_agrees_with_gate": 5, "rejudge_scope_and_audit": 3, "rejudge_fixture_only_demo": 5, "paralegal_edit_exemption_and_d034": 4, "pending_not_blocking_d045a": 2, "judges_step_consistency": 3, "mutation_strength": 5},
 "findings": [
  {"severity": "major", "title": "Pending items still block the gate; D-045(a) not implemented",
   "evidence": "Live /trace with 18 pending: export_gate ready False, 18 PENDING_DECISION blockers, verdict '18 items still need your decision'; live /export 200 with 'Items not reviewed: 18'. app/backend/trace.py:889-895 (PENDING_DECISION/DATE_UNCONFIRMED blockers), :901 ready, :910 'so the export is blocked.'; app/frontend/stepper.js:352 'Export blocked by N'; app/frontend/export.js:39 copy asks a confirm when c.pending > 0; tests/unit/test_trace.py:741-745 asserts ready False with pending.",
   "why_it_matters": "D-045(a) (binding) says pending items do not block export; R-EX-5 (spec/REQUIREMENTS.md:123) says copy asks one confirmation. The gate reports a block the export does not apply, so the paralegal is told to settle 18 items while the copy path works after one confirm. Fail-closed; no facts invented or lost, so major, not blocker.",
   "fix": "Move PENDING_DECISION and DATE_UNCONFIRMED out of blockers; report pending as counts.pending_items and a confirm line. Keep ready == (blockers == []) with JUDGE_NOT_RUN and run blockers still listed. Rewrite test_trace.py:741-745 and the gate-and-export agreement test. Record the rule in memory/DECISIONS.md.",
   "acceptance_test": "Sample case, accept all but one entry, judges answered: gate ready True, blockers []; export 200; notes contain 'Items not reviewed: 1'. Blank one accepted item's judge: gate ready False with only JUDGE_NOT_RUN; export 422."},
  {"severity": "minor", "title": "Rejudge re-asks pending unjudged items, not only the blocked accepted ones",
   "evidence": "Live POST /rejudge: asked 12 (e1, e2, a1, a2 accepted; a4, e3 to e9 pending). app/backend/rejudge.py:60 targets = trace.unjudged_items; trace.py:667-679 includes pending; tests/unit/test_trace.py:829 asserts asked == n.",
   "why_it_matters": "D-044 says rejudge re-judges just the items the gate lists. Pending items get extra audited model calls; review_status is untouched, so impact is low.",
   "fix": "Restrict targets to review_status accepted or edited, or record in memory/DECISIONS.md that pending unjudged items are also re-asked and update the test.",
   "acceptance_test": "4 accepted and 8 pending unjudged items: asked equals 4 (or the DECISIONS entry names 12 and the test asserts 12)."},
  {"severity": "minor", "title": "Judges step and /judges count a paralegal-edited summary as unchecked; D-045(b) exempts it",
   "evidence": "Live: e3 summary edited, judge unavailable on the edit; /judges unavailable 1; /trace judges step fail 'JUDGE_UNAVAILABLE', next RERUN_JUDGE; after dismissing other pending items export_gate ready True, verdict 'Ready to export'. app/backend/trace.py:637-655 _judge_rows has no exemption; judge_report at :692 counts from it; the exemption exists only in unjudged_items at :676.",
   "why_it_matters": "The view shows a failed check and a rerun action on wording the spec says is human-authored, next to a passing gate. Honest but contradictory.",
   "fix": "Apply the entered_by and edited-summary exemption in the judge counts and judges step, or show the item as paralegal wording not AI-checked.",
   "acceptance_test": "Edit one entry summary with judge unavailable and dismiss the other pending items: judges step not fail on account of that item; gate ready True; verdict code ready."},
  {"severity": "nit", "title": "Export refusal has no unit test in tests/unit/test_export.py",
   "evidence": "app/backend/export.py:576-577 raises JudgeNotRun; only HTTP tests in tests/unit/test_trace.py cover it; mutant M5 killed only through the API.",
   "why_it_matters": "A unit regression in build_export would surface only through the route tests.",
   "fix": "Add a unit test calling export.build_export with judge_not_run set and asserting JudgeNotRun with the items.",
   "acceptance_test": "build_export({'judge_not_run': [{'item_id': 'x'}], ...}) raises JudgeNotRun; mutant M5 killed by that test."}
 ],
 "whats_right": [
  "The JUDGE_NOT_RUN blocker and the export 422 come from one function (trace.judge_not_run_blockers, read by store.export_case and the gate); live they listed the same four ids and both cleared after rejudge.",
  "The paralegal-summary exemption and the D-034 check both behave live: a number not in the quote gives 422 invalid_edit; a text-only edit leaves the item out of JUDGE_NOT_RUN.",
  "Rejudge is audited (12 llm_calls rows, backend fixture, role judge) and fixture-only in demo mode, and it never changes review_status."
 ],
 "questions_for_chris": ["D-045(a) says pending items do not block export, but the gate still lists them as blockers and the stepper says 'Export blocked by N' while Copy works after one confirm. Should pending be a confirm line in the gate (as R-EX-5 describes), not a blocker? I have assumed yes."]}
```
