# T-080 review: check-trace API (staff-engineer-reviewer)

Scope: commit e3cea6f (`app/backend/trace.py`, three routes in `api.py`, "Check traces (D-042)" in `memory/contracts/api.md`, `tests/unit/test_trace.py`). `trace.py`, `api.py` and the test file are unchanged between e3cea6f and HEAD 3104213.

Verdict: **changes** (0 blockers, 2 majors, 5 minors, 1 nit).

The per-item ladders match the stored data on every case I cross-checked, and the judge counts reconcile for runs where every judge answered. Two places lie once something goes wrong. When a judge never ran (run deadline), the item traces say "skipped / JUDGE_UNAVAILABLE" but the judge summary and the case-level "judges" step report zero unavailable and PASS. When a run has failed, the export gate says `ready: true, status: pass` while its own `blockers` list holds `RUN_FAILED`.

## What I ran
- `.venv/bin/python -m pytest -q tests/unit/test_trace.py` gave 27 passed. `.venv/bin/python -m pytest -q tests/unit -p no:cacheprovider` gave 1031 passed.
- Own app instances on spare ports 7991 (`ZLAYT_MODE=local`) and 7992 (public), `LLM_BACKEND=fixture FIXTURE_SET=curated`. Cases: sample, golden case_01, 02, 03, 04, 05, 06, 07, 08, 09, and library lib01 to lib05. I ran each, then walked every entry, amount and flag trace and compared it with the stored item (state, reasons, review_status), `/judges` and `/trace`.
- Narrative sentences: a fresh sample case, all entries accepted, narrative generated, `ns1..ns9` traced.
- Edit, accept, confirm_date flows via the API; then re-read traces and the gate. Two GETs of the same URL returned identical bytes (md5).
- Leak scan, public vs local, after an edit and a flag note with a marker string: public output has none of `system_text/user_text/response_raw/before/after/edited_text/error` and no marker; local adds only `response_raw/before/after/edited_text`. No prompt text appears in either mode. `override_reasons` holds codes only.
- Scratch-DB probes on `sqlite3.backup` copies: no-judge-record probe, failed-run gate probe, rejected amount and flag probe, and an internal-KeyError probe.
- Mutation run on a scratch copy (`t080m_*` in the scratchpad): 23 mutants of `trace.py`. 20 killed, 3 survived (see finding 6).
- Grep: no `float(`, no bare except, no network or sleep in `trace.py`. The one `time.sleep(0.25)` in the test fixture is a bounded poll loop.

Housekeeping: the app ignores `ZLAYT_DB` (it reads `DATA_DIR`, default `data/zlayt.sqlite`), so my instances wrote to the shared untracked `data/zlayt.sqlite`. I deleted every case I created by token (DELETE), left the file alone because other cases in it are not mine, and stopped my two servers.

## Findings

1. **major: the judge summary and case-level "judges" step ignore items whose judge never ran.**
   - `judge_report` skips any item without a stored `ladder.judge.verdict` (`trace.py:622`). `pipeline.py:305-310` shows how that arises: if the run deadline hits, `guard("amounts")` is false and the amounts keep the code-only record with `judge: None` and `JUDGE_UNAVAILABLE`. Nothing counts these as unavailable, so the case `judges` step falls to PASS (`trace.py:787-788`).
   - Probe on a copy of the sample: 12 items whose own trace says `judge_* skipped JUDGE_UNAVAILABLE`, yet `/judges` totals are `{'items_judged': 7, 'unavailable': 0}`, `unresolved: 0`, and the case step reads `judges pass | The second check agreed with all 7 items it checked.`
   - A weaker form is in the same copy of the sample: with 3 items judge-less, `/judges` reports `unavailable: 1`.
   - This is the judge process the card exists to make visible, and it reports success when the judge did not run. Item states stay `needs_review`, which is why I rate it major and not a §5 blocker.

2. **major: the export gate contradicts itself after a failed run.**
   - `ready = bool(rv["ready_to_export"]) and not cx.running` (`trace.py:834`) ignores `case.status == "failed"`, while the same function adds a `RUN_FAILED` blocker (`trace.py:822-823`).
   - Probe: all items accepted, then `status='failed'`. Result: `gate: pass ready True reason None blockers ['RUN_FAILED']`, verdict `failed`, why "Every live item has your decision ... export can be built."
   - The card says the gate lists exactly the blockers. A gate with `ready: true` and a non-empty `blockers` array will render a green "Ready" beside a blocker.

3. **minor: record-warning flags give the wrong next_action and lose their step link.**
   - Case_01 `f_date_r8` (DATE_AMBIGUOUS): the step why says "confirm which one is right", but `next_action` is `READ_RECORD` (`trace.py:446`), and `state_reasons[0].step_id` is `null`. The entry `e8` and the case `dates` step correctly say `CONFIRM_DATE`.
   - Case_07 `f_inj_r3` (INJECTION_SUSPECTED) has `step_id: null` too. `_STEP_OF_REASON` maps to ids (`date_confirmed`, `injection_scan`) that record-warning traces do not have; their only step is `record_warning_check`.
   - Fix: use `CONFIRM_DATE` for the date category and fall back to `record_warning_check` when the mapped id is missing.

4. **minor: decided items keep a stale top-level `next_action`.**
   - `first_na` (`trace.py:245`) is taken from any step. After I edited `e2` (verdict `accepted`, `blocks_export: false`), top-level `next_action` was still `EDIT_SUMMARY`, because the qualifier step still fails and the human chose to keep it.
   - Fix: null it when the verdict is accepted or dismissed (the step-level hint can stay).

5. **minor: any internal `KeyError` or `IndexError` becomes a 404 "No such item."**
   - `api.py:507` wraps the whole `trace.item_trace` call. Probe: removing `DECIDE` from `trace._NEXT` and requesting an undecided amount returned `404 {'code': 'not_found', 'message': 'No such item.'}`. Table-lookup bugs in the fixed-sentence tables will be misreported.
   - Fix: raise a specific `UnknownItem` from `item_trace` and catch only that.

6. **minor: the tests miss three mutants and the failure branches above.**
   - Survivors: (a) a dismissed item's `human` step as `pass` instead of `skipped` (`trace.py:224`); (b) the gate ignoring a running case (`trace.py:834`, the unit test has pending items so `ready_to_export` is already false); (c) `/judges` `totals.unsupported` dropping `disagrees` (`trace.py:689`; the totals test only uses `unsupported`).
   - No test covers `RUN_FAILED`, an item with no judge record, a rejected amount or flag, or the record-warning flags. These are exactly where findings 1 to 3 sit.
   - Fix: add a dismissed-human-step assertion, an all-accepted plus running case, an amount judge `disagree` in the totals test, and one test each for failed-run and judge-never-ran.

7. **nit: wording and duplicated mapping.**
   - A rejected charge's `total_inclusion` says "Not a billed charge, so it is not added to the total." (`trace.py:410`), which is wrong for a charge rejected for grounding.
   - A narrative sentence that fails `NOT_AN_ACCEPTED_ENTRY` still shows `extracted` as "named the one accepted entry" (`trace.py:547`).
   - A narrative judge answer of `unsure` is shown as skipped / "not available" (`trace.py:577`; this follows `narrative.py:113`).
   - `_norm_verdict` ignores its `step_id` argument and re-implements `judges._TO_LADDER`, which can drift.

## Checked and fine
- Every item type gets an ordered ladder whose statuses match the stored data, including the rate, unclear, damages, injection, lexicon-only, record-warning, rejected, edited and ambiguous-date cases.
- `confirm_date` flows through to the entry trace and the gate blockers.
- Fail and pending steps carry a closed `next_action` and a fixed-sentence why.
- Unconfirmed dates give `DATE_UNCONFIRMED` blockers, and accepting such an item is refused (test `test_unconfirmed_date_fails_and_blocks_accept_d041`).
- Gate blockers equal `review.queue` on all 16 cases I ran.
- No LLM prose reaches a trace (`rationale` is the fixed sentence for the closed code).
- Responses are deterministic.

```json
{"card": "T-080", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit e3cea6f: app/backend/trace.py, 3 routes in app/backend/api.py, memory/contracts/api.md 'Check traces (D-042)', tests/unit/test_trace.py; own app on :7991 (local) and :7992 (public), fixture backend; sample, golden case_01..09, library lib01..lib05",
 "exercised": [
  ".venv/bin/python -m pytest -q tests/unit/test_trace.py -> 27 passed",
  ".venv/bin/python -m pytest -q tests/unit -> 1031 passed",
  "ran sample, golden case_01-09 and library lib01-05 on own instances (fixture, curated); walked every entry/amount/flag trace against the stored item, /judges and /trace",
  "narrative sentences ns1-ns9 on a fresh sample case",
  "edit/accept/confirm_date flows, then re-read traces and gate",
  "public vs local leak scan after an edit and a flag note with marker strings; no prompts in either mode",
  "identical bytes on repeated GET (md5)",
  "scratch-DB probes: no-judge-record, failed-run gate, rejected amount and flag, internal KeyError -> 404",
  "23-mutant mutation run in a scratch copy: 20 killed, 3 survived",
  "grep for float(, bare except, network, sleep in trace.py and the test"],
 "verdict": "changes",
 "scores": {"ladder_accuracy_vs_stored_data": 4, "plain_words_and_next_action": 4, "export_gate_exactness": 3, "judge_summary_reconciliation": 2, "public_mode_visibility_split": 5, "determinism_and_no_llm_in_deterministic_paths": 5, "test_strength_mutants": 3, "contract_match": 4},
 "findings": [
  {"severity": "major", "title": "Judge summary and case 'judges' step ignore items whose judge never ran; they report PASS",
   "evidence": "app/backend/trace.py:622 `if not jd or not jd.get(\"verdict\"): continue`; trace.py:787-788 falls to PASS; pipeline.py:305-310 (deadline -> code-only amounts, judge None, JUDGE_UNAVAILABLE). Scratch probe on a copy of the sample (judge records removed from entries and non-damages amounts): 12 item traces say judge skipped JUDGE_UNAVAILABLE, /judges totals {'items_judged': 7, 'unavailable': 0}, unresolved 0, case step 'judges pass | The second check agreed with all 7 items it checked.' With only 3 items judge-less, /judges reports unavailable: 1.",
   "why_it_matters": "The card exists to make the judge process visible. When the judge did not run, the case stepper shows a green second check and the summary counts do not reconcile with the item ladders; a deadline-cut run looks double-checked.",
   "fix": "In judge_report, count every live entry/amount/flag that needs a judge (not damages, not a code-made flag, not lexicon-only, not rejected) but has no verdict as 'unavailable' and list it in unresolved with FIXTURE_MISS/JUDGE_UNAVAILABLE. Make the case 'judges' step FAIL (or PENDING while running) when any such item exists, and never say 'agreed with all N' when N is below the number that needed a judge.",
   "acceptance_test": "Given a case where the judge stage did not run (ladder.judge None, state_reasons JUDGE_UNAVAILABLE), assert /judges totals.unavailable equals the number of such items, unresolved lists each, and the case 'judges' step status is fail with reason JUDGE_UNAVAILABLE; counts of item-level judge steps with reason JUDGE_UNAVAILABLE equal totals.unavailable."},
  {"severity": "major", "title": "Export gate says ready/pass while blockers lists RUN_FAILED after a failed run",
   "evidence": "app/backend/trace.py:834 `ready = bool(rv[\"ready_to_export\"]) and not cx.running` vs trace.py:822-823 adds RUN_FAILED. Scratch probe (all items accepted, case status failed): `case verdict: {'code': 'failed'} | gate: pass ready True reason None blockers ['RUN_FAILED']`, gate why 'Every live item has your decision and at least one item is accepted, so the export can be built.'",
   "why_it_matters": "AC2 and the contract require the gate to list exactly what blocks export. A pass/ready gate with a non-empty blockers array will render a green 'Ready to export' next to a blocker, and the case verdict says failed.",
   "fix": "Make ready require case status not running and not failed (ready = review.ready_to_export and not blockers), or drop RUN_FAILED from blockers and document that a failed run does not block. Either way ready must equal (blockers == []).",
   "acceptance_test": "For every case state (pending items, nothing accepted, running, failed with everything accepted, all accepted), assert gate.ready == (gate.blockers == []) and gate.status == ('pass' if ready else 'fail')."},
  {"severity": "minor", "title": "Record-warning flags: wrong next_action for DATE_AMBIGUOUS and state_reasons.step_id null",
   "evidence": "case_01 f_date_r8: step 'record_warning_check fail DATE_AMBIGUOUS | ... confirm which one is right' has next_action READ_RECORD (trace.py:446); state_reasons[0].step_id null; case_07 f_inj_r3 INJECTION_SUSPECTED step_id null (_STEP_OF_REASON maps to date_confirmed/injection_scan, which a record-warning trace does not have). Entry e8 and the case 'dates' step correctly use CONFIRM_DATE.",
   "why_it_matters": "The fail step tells the paralegal to confirm a date and the action says read the record; the UI cannot highlight the step that explains the reason.",
   "fix": "For category date_ambiguous use na('CONFIRM_DATE', {'view':'dates_to_confirm'}); in _finish fall back to the only failing/first step id when the mapped id is not in the trace.",
   "acceptance_test": "Trace f_date_r8 on case_01: record_warning_check.next_action.code == 'CONFIRM_DATE' and every state_reasons[].step_id is a step id in the trace (for all items on case_01 and case_07)."},
  {"severity": "minor", "title": "Accepted or dismissed items keep a stale top-level next_action",
   "evidence": "trace.py:245 first_na picks any step's next_action. After editing e2 on the sample: verdict {'code': 'accepted', 'blocks_export': False} and next_action {'code': 'EDIT_SUMMARY', ...} because summary_qualifier still fails.",
   "why_it_matters": "The HITL hand-off tells the human to do something about an item they already decided.",
   "fix": "Set top-level next_action to null when verdict.code is accepted or dismissed; keep step-level hints.",
   "acceptance_test": "Edit an entry that fails a code check, then assert trace.next_action is None while the failing step still has its own next_action."},
  {"severity": "minor", "title": "Internal KeyError/IndexError in trace code is reported as 404 'No such item.'",
   "evidence": "app/backend/api.py:507 `except (KeyError, IndexError): raise ApiError(404, 'not_found', 'No such item.')` wraps all of trace.item_trace. Probe: trace._NEXT.pop('DECIDE') then GET /items/a1/trace -> 404 {'code': 'not_found', 'message': 'No such item.'}.",
   "why_it_matters": "A bug in a fixed-sentence table shows up as a missing item, which is hard to debug and hides a real failure.",
   "fix": "Raise a dedicated UnknownItem from item_trace for missing ids and catch only that; let other exceptions surface as 500 with the standard error body.",
   "acceptance_test": "Monkeypatch trace._NEXT to drop a code and assert the response is 500, while an unknown id still gives 404."},
  {"severity": "minor", "title": "Tests leave 3 of 23 trace mutants alive and do not cover the failure branches in findings 1-3",
   "evidence": "Scratch mutation run (t080m_*): SURVIVED M3 dismissed human step PASS instead of SKIPPED (trace.py:224); M5 gate ignores cx.running (trace.py:834; test_run_in_progress_blocks_the_gate has pending items so ready_to_export is already false); M19 totals.unsupported drops 'disagrees' (trace.py:689; test_judge_summary_counts_and_objections only uses 'unsupported'). No test mentions RUN_FAILED, an item with no judge record, a rejected amount or flag, or record_warning flags.",
   "why_it_matters": "These are the branches where the trace reports wrong answers when something goes wrong; the suite stays green if they regress.",
   "fix": "Add a dismissed-item human-step assertion; an all-accepted plus running case; an amount judge 'disagree' in the totals test; and tests for failed run, judge-never-ran, rejected amount/flag, and record-warning flags.",
   "acceptance_test": "Re-run the three surviving mutants and confirm each makes at least one test fail."},
  {"severity": "nit", "title": "Wording inaccuracies and duplicated verdict mapping",
   "evidence": "trace.py:410 rejected charge shows 'Not a billed charge, so it is not added to the total.'; trace.py:547 narrative sentence failing NOT_AN_ACCEPTED_ENTRY still says the AI 'named the one accepted entry'; trace.py:577 a narrative judge answer of 'unsure' is shown as skipped/'not available' (follows narrative.py:113); trace.py:155 _norm_verdict ignores step_id and re-implements judges._TO_LADDER.",
   "why_it_matters": "Small plain-words errors in a screen whose purpose is explaining why; the duplicated mapping can drift from the judges module.",
   "fix": "Use a rejected-specific sentence for total_inclusion, soften the extracted text for unaccepted citations, and call judges.to_ladder with the right step.",
   "acceptance_test": "Rejected charge total_inclusion.why mentions rejection; _norm_verdict removed in favour of judges.to_ladder with unit coverage of every raw verdict."}
 ],
 "whats_right": [
  "Public/local split holds: metadata mode carries no raw answers, no before/after or edit text, prompts never appear, and local adds only the documented full-only keys.",
  "Item ladders match stored data on 16 cases (rate, unclear, damages, injection, lexicon-only, ambiguous date, rejected, edited) and the gate blockers equal review.queue every time.",
  "Every why, rationale and next_action text is a fixed code-written sentence (D-028), responses are byte-identical on repeat, and no LLM or float is involved."],
 "questions_for_chris": []}
```
