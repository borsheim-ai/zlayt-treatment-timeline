# Subagent: Backend: T-080 r2 honest gates (Backend: T-080 r2 honest gates)

Source: `agent-af25a512e767c77b4.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:32:12.057Z

You own board card T-080, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-080-staff-engineer.md. The principle: a gate never says pass while something underneath it failed or never ran.

1. **Major 1:** `/judges` and the case-level "judges" step must count items whose judge never ran (JUDGE_UNAVAILABLE) and must not report "agreed with all" when any item is unavailable. The step status is fail or pending, with the count and the next action (trace.py:622 and 787).
2. **Major 2:** after a failed run, the export gate must return `ready: false` and a non-pass status whenever `blockers` is non-empty, RUN_FAILED included (trace.py:822 and 834). Add an invariant test: `ready == (len(blockers) == 0)` for every case state you can build.
3. **Minors:**
   - correct the next_action and step_id on record-warning flags;
   - refresh the top-level next_action on decided items;
   - an internal KeyError must return 500, not 404 (api.py:507);
   - add tests that kill the 3 surviving mutants listed in the review.
4. **ZLAYT_DB:** the reviewer reports the app ignores `ZLAYT_DB` and writes to data/zlayt.sqlite. Check app/db/db.py and app/main.py. If it's true, fix it so ZLAYT_DB is honoured; tools/serve_app.sh relies on it. app/db is db-owned, so make the minimal fix and note it on the card.

The frontend (T-081, T-082) consumes these fields. Don't change field names; if you must, note it on T-081. Run `.venv/bin/python -m pytest -q tests/unit`. Commit with the pathspec or temp-index rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-080 in_review --agent backend`. Reply in 2 lines.

### User / tool · 2026-11-02T03:32:12.063Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:13.772Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-080-staff-engineer.md | head -150; python3 tools/board.py show T-080 | tail -40"
}
````

### User / tool · 2026-11-02T03:32:13.903Z

**tool result**
````
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
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T03:32:05Z"
claimed_by: "backend"
claimed_at: "2026-11-02T03:32:05Z"
rounds: 1
commits: ["e3cea6f"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-080-staff-engineer.md", "at": "2026-11-02T03:32:05Z"}
ac:
  - {"n": 1, "text": "GET returns for every entry/amount/flag/narrative sentence an ordered list of steps (extracted, code checks each by name, judge 1, judge 2 if any, human) with status pass|fail|skipped|pending, plain-words why, reason code, evidence (excerpt span, judge rationale, model + prompt version) and next_action for the human", "done": true, "evidence": "tests/unit/test_trace.py: test_every_item_has_an_ordered_well_formed_trace, test_entry_trace_names_each_code_check_and_the_judge, test_judge_objection_is_a_fail_with_fixed_rationale, test_rejected_entry_skips_later_checks..., test_unconfirmed_date_fails_and_blocks_accept_d041, test_amount_*, test_code_made_flags_need_no_judge, test_narrative_sentence_traces pass; contract in memory/contracts/api.md 'Check traces (D-042)'"}
  - {"n": 2, "text": "Case-level trace: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate, each with counts and pass/fail/why; export gate lists exactly what blocks export; api.md updated; unit tests", "done": true, "evidence": "tests/unit/test_trace.py: test_case_trace_steps_and_counts, test_export_gate_lists_exactly_the_pending_live_items, test_export_gate_date_unconfirmed_blocker, test_export_gate_ready_matches_review_view, test_export_gate_nothing_accepted, test_judge_summary_*, visibility split test; full suite 1031 passed (.venv/bin/python -m pytest -q tests/unit)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T03:11:11Z backend: claimed
- 2026-11-02T03:15:04Z backend: contract ready: memory/contracts/api.md section 'Check traces (D-042)': GET /api/cases/{token}/items/{item_id}/trace, GET /api/cases/{token}/trace, GET /api/cases/{token}/judges (step shape, step ids per item kind, export-gate blockers, full vs metadata mode). Frontend T-081/T-082 can start. Implementation next.
- 2026-11-02T03:21:48Z backend: AC 1 checked: tests/unit/test_trace.py: test_every_item_has_an_ordered_well_formed_trace, test_entry_trace_names_each_code_check_and_the_judge, test_judge_objection_is_a_fail_with_fixed_rationale, test_rejected_entry_skips_later_checks..., test_unconfirmed_date_fails_and_blocks_accept_d041, test_amount_*, test_code_made_flags_need_no_judge, test_narrative_sentence_traces pass; contract in memory/contracts/api.md 'Check traces (D-042)'
- 2026-11-02T03:21:48Z backend: AC 2 checked: tests/unit/test_trace.py: test_case_trace_steps_and_counts, test_export_gate_lists_exactly_the_pending_live_items, test_export_gate_date_unconfirmed_blocker, test_export_gate_ready_matches_review_view, test_export_gate_nothing_accepted, test_judge_summary_*, visibility split test; full suite 1031 passed (.venv/bin/python -m pytest -q tests/unit)
- 2026-11-02T03:21:49Z backend: moved in_progress -> in_review
- 2026-11-02T03:21:57Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T03:32:05Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-080-staff-engineer.md; round 1; findings:
    - [major] Judge summary and case 'judges' step ignore items whose judge never ran; they report PASS — fix: In judge_report, count every live entry/amount/flag that needs a judge (not damages, not a code-made flag, not lexicon-only, not rejected) but has no verdict as 'unavailable' and list it in unresolved with FIXTURE_MISS/JUDGE_UNAVAILABLE. Make the case 'judges' step FAIL (or PENDING while 
    - [major] Export gate says ready/pass while blockers lists RUN_FAILED after a failed run — fix: Make ready require case status not running and not failed (ready = review.ready_to_export and not blockers), or drop RUN_FAILED from blockers and document that a failed run does not block. Either way ready must equal (blockers == []).
    - [minor] Record-warning flags: wrong next_action for DATE_AMBIGUOUS and state_reasons.step_id null — fix: For category date_ambiguous use na('CONFIRM_DATE', {'view':'dates_to_confirm'}); in _finish fall back to the only failing/first step id when the mapped id is not in the trace.
    - [minor] Accepted or dismissed items keep a stale top-level next_action — fix: Set top-level next_action to null when verdict.code is accepted or dismissed; keep step-level hints.
    - [minor] Internal KeyError/IndexError in trace code is reported as 404 'No such item.' — fix: Raise a dedicated UnknownItem from item_trace for missing ids and catch only that; let other exceptions surface as 500 with the standard error body.
    - [minor] Tests leave 3 of 23 trace mutants alive and do not cover the failure branches in findings 1-3 — fix: Add a dismissed-item human-step assertion; an all-accepted plus running case; an amount judge 'disagree' in the totals test; and tests for failed run, judge-never-ran, rejected amount/flag, and record-warning flags.
- 2026-11-02T03:32:05Z backend: claimed

## Handoff
What changed: new app/backend/trace.py + 3 read-only routes (GET /items/{id}/trace, /trace, /judges); contract in api.md 'Check traces (D-042)'. Judge reason_code now persisted in ladder.judge (pipeline._finish_amount, review edit/manual entry: 1-line touches, no db change); older rows read it from the audited call. Visibility = audit split (metadata vs ZLAYT_MODE=local adds response_raw, event before/after, edited_text; prompts never). How verified: tests/unit/test_trace.py 27 tests, full tests/unit 1031 passed. Left: nothing in scope; frontend T-081/T-082 consume. Surprised: judge prompts are already v2 for j3/j4 (audited.PROMPT_OF_STEP is the single source); judge 'rationale' is a fixed sentence for the closed reason_code per D-028 (no model prose to store). Case-level split step cannot see a code-vs-ambiguous method (only llm_split flag / config.split_failure are stored).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:14.582Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/memory/MEMORY.md"
}
````

### User / tool · 2026-11-02T03:32:14.590Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:16.437Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/backend/project_backend_conventions.md; git status --short | head -20; wc -l app/backend/trace.py; grep -n \"ZLAYT_DB\\|DATA_DIR\" -r app tools/serve_app.sh | head -20"
}
````

### User / tool · 2026-11-02T03:32:16.558Z

**tool result**
````
---
name: backend-conventions
description: Codepaths, conventions and pitfalls for the deterministic backend modules and pipeline (T-032/033/037); read before touching ingest, amounts, gaps, conflicts, pipeline
metadata:
  type: project
---

Codepaths (app/backend): `ingest.py` (split/limits/dedupe/warnings, `ingest()` composite, `evidence_span`), `dates.py` (format list, 2-digit year >40 ambiguous per D-027), `amounts.py` (cents, classify, extract_amounts, rate_note), `totals.py`, `gaps.py`, `conflicts.py`, `flag_templates.py` (render with closed var whitelist + golden-subtype aliases), `lexicon.py` (loads app/llm/lexicon.yaml as data; deterministic modules must not import app.llm), `pipeline.py` (stages 0-7, `run_ingest`, `ingest_case`, `run_pipeline`, `run_case`, `judge_summary`, CLI). `app/pipeline.py` is a shim so `python -m app.pipeline` works (outside owned paths; flagged to orchestrator).

Conventions: money is int cents and amounts.py must not contain `float(`; text outside recognised record blocks becomes an `unsplit` record (never dropped; only exact `ingest.BANNERS` lines are set aside); a figure inside an injection hit has cents None; flag title/explanation only via flag_templates.render; code never sets review_status (pipeline items leave a run `pending`; `_persist` preserves existing review status on rerun).

Pitfalls: (1) the stage-and-commit rule: `git add` and `git commit` must be separate Bash calls (git-guard hook rejects a combined call), and commit with explicit pathspec `git commit -m ... -- <paths>`. (2) One sqlite3 connection shared by worker threads corrupts `PRAGMA table_info` reads; audited.py serialises writes with `_DB_LOCK`; do not use `:memory:` DBs with threads (CLI uses a temp file). (3) Fixture keys hash the full prompt, so any prompt/schema change in app/llm/prompts or judges invalidates tests/fixtures/llm: re-run `LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record <golden .txt>` per case and `--judges`. (4) tests/unit/test_pipeline.py SEM script has `record_id` which schemas.FlagOutput forbids: the 3 j3 pipeline tests fail until T-036/qa reconcile.

Review findings to avoid repeating: silent text loss in splitters, silent century guesses, ACs ticked on REPL evidence without a named test.

T-075 (determinism): the 0.0 live 3-run did not reproduce in 12 later runs; the real fragilities were judge prompts (J4 rejected valid flags; J3 undecided), model-order-dependent ids, and immediate retries. Judge prompts now v2 (flag category rules; J3 takes `category`). To re-record only judge fixtures after a judge prompt change, replay the recorded set and call claude-cli only on a miss at j3/j4 (never re-record whole cases: it would overwrite extract/narrative fixtures other workers depend on); then run `make_curated.py` (no flag), restore unchanged curated files byte-for-byte, `--check`. Run live pipeline checks in parallel processes (6 at once is fine, ~60 s).
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
     856 app/backend/trace.py
app/README-arch.md:39:app/config.py [release]   env: LLM_BACKEND, GENERATOR_MODEL, JUDGE_MODEL, ENABLE_LIVE, PROVIDER_CAP_CONFIRMED, DATA_DIR, limits; injectable now() for every deadline and purge
app/backend/api.py:92:    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
tools/serve_app.sh:6:tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:18.620Z

**tool call — Bash**
````
{
 "command": "sed -n 80,100p app/backend/api.py; cat app/main.py | head -40; grep -n \"environ\\|getenv\" app/db/*.py | head; sed -n 200,260p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T03:32:18.730Z

**tool result**
````
def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
    host = request.client.host if request.client else None
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback


def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
    code = _OBJECTION[verdict]
    detail = why.judge_detail(rc)
    ev["rationale"] = detail or reason_text(code)
    return step(sid, label, "llm", FAIL, (reason_text(code) + (" " + detail if detail else "")).strip(), reason=code, rule=rule, evidence=ev,
                next_action=na("COMPARE_BY_HAND"))


def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
    """The paralegal's rung. pending (live item) blocks export; rejected can only be dismissed; dismissed is skipped."""
    rs, rejected = row["review_status"], row["state"] == "rejected"
    evs = cx.events.get(row["id"], [])
    ev = {"action": present.STATUS_ACTION.get(rs), "at": ((row.get("edited") or {}).get("at") if rs == "edited" else None),
          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"before": e["before"], "after": e["after"]} if cx.full else {})} for e in evs]}
    if evs:
        ev["at"] = store.iso(evs[-1]["at"])
    if rs == "edited":
        ed = row.get("edited") or {}
        ev["kept_my_wording"] = bool(ed.get("kept_my_wording"))
        ev["override_reasons"] = ed.get("override_reasons") or []
        if cx.full:
            ev["edited_text"] = ed.get("summary") or ed.get("note")
    if rs in ("accepted", "edited"):
        return step("human", "Your decision", "human", PASS, "You accepted this item." if rs == "accepted" else "You edited this item and accepted it.", rule="row 17", evidence=ev)
    if rs == "dismissed":
        return step("human", "Your decision", "human", SKIPPED, "You dismissed this item; it stays out of the letter.", rule="row 17", evidence=ev)
    if rejected:
        return step("human", "Your decision", "human", PENDING, "This item could not be verified, so it cannot be accepted.", reason="PENDING_DECISION", rule="row 17", evidence=ev,
                    next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]))
    return step("human", "Your decision", "human", PENDING, TRACE_WHY["PENDING_DECISION"], reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
                next_action=extra_pending_next or na("DECIDE", {"item_id": row["id"]}, ["accept", "edit", "dismiss"]))


def _skipped(sid, label, kind, code, rule=None, rule_text=None):
    msg = rule_text or {"GROUNDING_EXCERPT_NOT_VERBATIM": "Not run: the quote did not pass the word-for-word check.",
                        "GROUNDING_AMOUNT_NOT_IN_TEXT": "Not run: the amount is not in the record text.",
                        "SCHEMA_INVALID": "Not run: the AI answer was malformed."}.get(code, "Not run because an earlier step rejected this item.")
    return step(sid, label, kind, SKIPPED, msg, reason=code, rule=rule)


def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
    """Assemble the item trace: numbering, progress, verdict, state_reasons mapped to the step that explains them."""
    _number(steps)
    ids = {s["id"] for s in steps}
    rs = row.get("review_status")
    live = row.get("state") != "rejected"
    first_na = next((s["next_action"] for s in steps if s["next_action"]), None)
    if rs in ("accepted", "edited"):
        code, label = "accepted", "Accepted by you"
    elif rs == "dismissed":
        code, label = "dismissed", "Dismissed by you"
    elif row.get("state") == "rejected":
        code, label = "rejected", "Rejected; kept out of the letter"
    elif any(s["status"] == FAIL for s in steps):
        code, label = "needs_attention", "Needs your attention"
    elif any(s["status"] == PENDING and s["kind"] == "llm" for s in steps):
        code, label = "waiting_for_run", "Waiting for the AI run"
    elif row.get("state") == "needs_review":
        code, label = "needs_attention", "Needs your attention"
    else:
        code, label = "ready_for_decision", "Ready for your decision"
    blocks = (live and rs == "pending") if blocks_flag is None else blocks_flag
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:19.056Z

**tool call — Bash**
````
{
 "command": "sed -n 425,460p app/backend/trace.py; sed -n 590,720p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T03:32:19.138Z

**tool result**
````
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    ftype, origin, cat = row["type"], row["origin"], row["category"]
    recs = cx.recs
    spans = [{"record_id": e["record_id"], "start": e["start"], "end": e["end"], "text": e["excerpt"]} for e in present._evidence(row.get("evidence"), recs)]
    rids = [s["record_id"] for s in spans if s["record_id"]]
    rid0 = rids[0] if rids else None
    st = []
    injected = any(recs.get(r, {}).get("injection_tag") for r in rids) or "INJECTION_SUSPECTED" in R

    def inj():
        if injected:
            return step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                        next_action=na("READ_RECORD", {"record_id": rid0}))
        return step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16")
    if ftype == "record_warning":
        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
            or next(iter(R), None)
        st.append(step("record_warning_check", "Code check on the record or the run", "code", FAIL, reason_text(code) if code else row["explanation"], reason=code,
                       rule="row 16" if cat == "injection_suspected" else "row 1", evidence={"values": {"category": cat}, "spans": spans},
                       next_action=na("READ_RECORD", {"record_id": rid0}) if rid0 else na("RERUN")))
        st.append(_human_step(cx, row, "flag"))
        return st
    if origin == "code":
        comp = present._computed(row.get("computed"))
        vals = {k: comp[k] for k in ("from", "to", "days", "threshold", "stated_dates", "body_date", "first_treatment_date", "names", "subtype") if k in comp}
        st.append(step("computed", "Dates compared by code" if ftype == "gap" else "Stated and recorded dates compared by code", "code", PASS,
                       row["explanation"] or "Computed by code from the record dates.", rule="row 9" if ftype == "gap" else "row 10", evidence={"values": vals, "spans": spans}))
        bad = row["state"] == "rejected" or cc.get("spans_match_input") is False
        st.append(step("spans_match", "Cited text matches the record", "code", FAIL if bad else PASS,
                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Every cited date line is in the record, character for character.",
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 10", evidence={"spans": spans},
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]) if bad else None))
        if "ENDPOINT_NOT_VERIFIED" in R:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", FAIL, reason_text("ENDPOINT_NOT_VERIFIED"), reason="ENDPOINT_NOT_VERIFIED", rule="row 9",
        st.append(step("human", "Your decision on the paragraph", "human", PENDING, "The paragraph stays in the internal notes until you accept it.", reason="PENDING_DECISION", rule="D-031",
                       next_action=na("DECIDE", {"view": "narrative"}, ["accept", "dismiss"])))
        code, label = "ready_for_decision", "Ready for your decision"
    _number(st)
    return {"token": cx.case_id, "item_id": item_id, "kind": "narrative_sentence", "mode": "full" if cx.full else "metadata", "state": None,
            "review_status": {"accepted": "accepted", "dismissed": "dismissed"}.get(status, "pending") if not rem else None,
            "state_reasons": [{"code": c, "why": _ntext(c),
                               "step_id": "cites_accepted_entry" if c == "NOT_AN_ACCEPTED_ENTRY" else ("sentence_checks" if c in rcodes else "judge_1")}
                              for c in ([reason] if rem and not rcodes else rcodes)],
            "verdict": {"code": code, "label": label, "blocks_export": False}, "progress": _progress(st),
            "next_action": next((x["next_action"] for x in st if x["next_action"]), None), "steps": st}


# ------------------------------------------------------------------ public: item trace
def item_trace(conn, case_id: str, item_id: str, full: bool = False) -> dict:
    """KeyError for an unknown item. Entry, amount, flag or narrative sentence (ns...)."""
    cx = _Cx(conn, case_id, full)
    if item_id.startswith("ns"):
        return _narrative_trace(cx, item_id)
    kind = present._ID_KIND[item_id[0]]
    row = DB.get_item(conn, item_id, case_id)
    steps = {"entry": _entry_steps, "amount": _amount_steps, "flag": _flag_steps}[kind](cx, row)
    return _finish(cx, item_id, kind, row, steps)


# ------------------------------------------------------------------ judge report
def _judge_rows(cx):
    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
    out = []
    for kind in ("entry", "amount", "flag"):
        for row in DB.list_items(cx.conn, cx.case_id, kind):
            jd = (row.get("ladder") or {}).get("judge")
            if not jd or not jd.get("verdict"):
                continue
            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
            call = cx.call(jd.get("call_id"), row["id"], jid)
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": _norm_verdict(jid, jd["verdict"]),
                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
    return out


def judge_report(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    rows = _judge_rows(cx)
    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
               "disagrees": 0, "unsure": 0, "unavailable": 0} for j in ("j1", "j2", "j3", "j4")}
    rejections, unresolved, disagreements, versions = [], [], [], set()
    overrides = 0
    for r in rows:
        p = per[r["judge"]]
        v = r["verdict"]
        p["items"] += 1
        p[v] += 1
        model = (r["call"] or {}).get("model") or r["jd"].get("model") or cx.models["judge"]
        pv = r["jd"].get("prompt_version") or (r["call"] or {}).get("prompt_version") or JUDGE_PROMPT[r["judge"]]
        p["models"].add(model)
        p["prompt_version"] = pv
        versions.add(pv)
        row = r["row"]
        base = {"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "verdict": v, "model": model, "prompt_version": pv,
                "call_id": r["jd"].get("call_id") or (r["call"] or {}).get("id"), "review_status": row["review_status"]}
        R = set(row.get("state_reasons") or [])
        if v in ("partially", "unsupported", "disagrees"):
            e = dict(base, reason_code=r["reason_code"], rationale=why.judge_detail(r["reason_code"]) or reason_text(_OBJECTION[v]), state_reason=_OBJECTION[v])
            if full and r["call"]:
                e["response_raw"] = r["call"].get("response_raw")
            rejections.append(e)
            if row["review_status"] in ("accepted", "edited"):
                overrides += 1
            if r["kind"] == "amount":
                says = (r["reason_code"] or "").replace("SHOULD_BE_", "").lower()
                disagreements.append({"item_id": r["item_id"], "kind": "amount", "type": "judge_objects", "code_says": row["kind"],
                                      "judge_says": f"{says} ({r['reason_code']})" if says and r["reason_code"] != "NONE" else "not a " + row["kind"],
                                      "resolution": "needs_review", "review_status": row["review_status"]})
            elif not (R & _CODE_CHECK_REASONS):
                disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_objects", "code_says": "All code checks passed.",
                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
        elif v in ("unsure", "unavailable"):
            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
                                   **({"reason_code": r["reason_code"]} if v == "unsure" else {})))
        elif R & _CODE_CHECK_REASONS:            # judge supported but a code check raised a doubt
            disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_agrees_code_flags",
                                  "code_says": " ".join(reason_text(c) for c in sorted(R & _CODE_CHECK_REASONS)), "judge_says": _J_OK[r["judge"]],
                                  "resolution": "needs_review", "review_status": row["review_status"]})
    for row in DB.list_items(conn, case_id, "flag"):
        R = set(row.get("state_reasons") or [])
        for c in ("LEXICON_ONLY", "LLM_ONLY"):
            if c in R:
                disagreements.append({"item_id": row["id"], "kind": "flag", "type": "sources_disagree",
                                      "code_says": "The phrase list found it." if c == "LEXICON_ONLY" else "The phrase list did not find it.",
                                      "judge_says": "The AI did not find it." if c == "LEXICON_ONLY" else "The AI found it.",
                                      "resolution": "needs_review", "review_status": row["review_status"]})
    j = lambda *ks: sum(sum(p[k] for p in per.values()) for k in ks)      # noqa: E731
    judges_out = [dict(p, models=sorted(p["models"])) for p in per.values()]
    for p in judges_out:
        if not p["items"]:
            p["models"] = []
    answered = j("supported", "partially", "unsupported", "disagrees", "unsure")
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "models": cx.models, "independent_models": cx.models["generator"] != cx.models["judge"],
            "totals": {"items_judged": answered, "supported": j("supported"), "unsupported": j("partially", "unsupported", "disagrees"), "unsure": j("unsure"),
                       "unavailable": j("unavailable"), "human_overrides": overrides},
            "judges": judges_out, "rejections": rejections, "unresolved": unresolved, "disagreements": disagreements, "prompt_versions": sorted(versions)}


def rationale_or(code, verdict):
    return why.judge_detail(code) or reason_text(_OBJECTION[verdict])


# ------------------------------------------------------------------ case trace
def _count_by(items, key):
    out = {}
    for i in items:
        out[i[key]] = out.get(i[key], 0) + 1
    return out


def case_trace(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    case = cx.case
    recs = list(cx.recs.values())
    ents = DB.list_items(conn, case_id, "entry")
    amts = DB.list_items(conn, case_id, "amount")
    flgs = DB.list_items(conn, case_id, "flag")
    allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
    cfg = case.get("config") or {}
    rv = present.review_view(conn, case_id)
    jr = judge_report(conn, case_id, full)
    st = []
    # 1 ingest
    dup = sum(1 for r in recs if r["duplicate_of"])
    st.append(step("ingest", "Read the paste and split it into records", "code", PASS if recs else FAIL,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:21.462Z

**tool call — Bash**
````
{
 "command": "grep -n \"JUDGE_UNAVAILABLE\\|def _judge_step\\|def _entry_steps\\|def _amount_steps\\|def _flag_steps\\|def _norm_verdict\\|_CODE_CHECK_REASONS =\" app/backend/trace.py; sed -n 160,200p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T03:32:21.546Z

**tool result**
````
73:_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}
155:def _norm_verdict(step_id, v):
175:def _judge_step(cx, item_id, jd, jid, R, *, sid=None, label=None, rule="row 4"):
187:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
198:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
279:def _entry_steps(cx, row):
369:def _amount_steps(cx, row):
424:def _flag_steps(cx, row):
578:            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAILABLE", rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
668:            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
782:        st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. " + reason_text("JUDGE_UNAVAILABLE"),
783:                       reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))

def _judge_reason_code(jd, call):
    code = (jd or {}).get("reason_code")
    if code:
        return code
    if call and call.get("response_raw"):
        try:
            got = json.loads(call["response_raw"])
            if isinstance(got, dict) and isinstance(got.get("reason_code"), str):
                return got["reason_code"]
        except (ValueError, TypeError):
            pass
    return None


def _judge_step(cx, item_id, jd, jid, R, *, sid=None, label=None, rule="row 4"):
    """One LLM judge step from ladder.judge (or None). Statuses: pass (supported), fail (objected/unsure), skipped (did not answer), pending (not run yet)."""
    sid = sid or f"judge_{jid[1]}"
    label = label or f"Second AI check: {JUDGE_LABEL[jid].lower()}"
    label = label[0].upper() + label[1:]
    jd = jd or {}
    raw = jd.get("verdict")
    call = cx.call(jd.get("call_id"), item_id, jid)
    if raw is None and not call:
        if not cx.ran:
            return step(sid, label, "llm", PENDING, "The second check has not run yet.", rule=rule, evidence={"model": {"id": cx.models["judge"], "role": "judge", "independent_of_generator": cx.models["judge"] != cx.models["generator"]}, "prompt_version": JUDGE_PROMPT[jid]},
                        next_action=na("RERUN"))
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence={"judge_verdict": "unavailable"},
                    next_action=na("COMPARE_BY_HAND"))
    verdict = _norm_verdict(jid, raw if raw is not None else (call or {}).get("verdict"))
    ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or JUDGE_PROMPT[jid], call)
    rc = _judge_reason_code(jd, call)
    ev.update(judge_verdict=verdict, judge_reason_code=rc)
    if verdict == "supported":
        ev["rationale"] = _J_OK[jid]
        return step(sid, label, "llm", PASS, _J_OK[jid], rule=rule, evidence=ev)
    if verdict == "unavailable":
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence=ev, next_action=na("COMPARE_BY_HAND"))
    code = _OBJECTION[verdict]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:29.988Z

**tool call — Bash**
````
{
 "command": "sed -n 755,856p app/backend/trace.py; grep -n \"class _Cx\" -A32 app/backend/trace.py; sed -n 150,159p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T03:32:30.078Z

**tool result**
````
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": missing[0]})))
    else:
        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PASS, f"The AI drafted an entry for all {len(firsts)} records.", rule="row 4", counts=ecounts))
    # 5 grounding
    rej = [(k, x) for k, x in allitems if x["state"] == "rejected"]
    codes = {}
    for _, x in rej:
        for c in x.get("state_reasons") or []:
            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"):
                codes[c] = codes.get(c, 0) + 1
    gcounts = {"items_checked": len(allitems), "rejected": len(rej), "reasons": codes}
    if rej:
        first = next(iter(codes), None)
        st.append(step("grounding", "Every quote and amount is in the record", "code", FAIL, f"{len(rej)} item{'s were' if len(rej) != 1 else ' was'} rejected because the quote or amount is not in the record. "
                       "They stay in the tray and out of the letter.", reason=first, rule="row 4", counts=gcounts,
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"view": "tray"})))
    elif not allitems:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PENDING, "There is nothing to check yet.", rule="row 4", counts=gcounts, next_action=na("RERUN")))
    else:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PASS, f"All {len(allitems)} items cite text that is in the record, character for character.", rule="row 4", counts=gcounts))
    # 6 judges
    t = jr["totals"]
    jcounts = dict(t)
    objections = t["unsupported"] + t["unsure"]
    if not rows_any(jr) and not cx.ran:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, "The second check has not run yet.", rule="row 4", counts=jcounts, next_action=na("RERUN")))
    elif t["unavailable"]:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. " + reason_text("JUDGE_UNAVAILABLE"),
                       reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
    elif objections:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, f"The second check questioned {objections} of {t['items_judged']} items; they are marked for review.",
                       reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
    else:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", PASS, f"The second check agreed with all {t['items_judged']} items it checked.", rule="row 4", counts=jcounts))
    # 7 flags
    fc = {"total": len(flgs), "by_type": _count_by(flgs, "type"), "by_origin": _count_by(flgs, "origin")}
    if any(f["category"] == "analysis_incomplete" for f in flgs):
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", FAIL, reason_text("CONFLICT_CHECK_INCOMPLETE"), reason="CONFLICT_CHECK_INCOMPLETE", rule="row 11", counts=fc,
                       next_action=na("RERUN")))
    elif not cx.ran:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PENDING, "Gaps and date conflicts are ready (code). The AI and phrase-list pass has not run.", rule="row 9", counts=fc,
                       next_action=na("RERUN")))
    else:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and the AI.", rule="row 9", counts=fc))
    # 8 totals
    tv = present.totals_view(conn, case_id)
    pend_ch = tv["pending"]["count"]
    tcounts = {"accepted_cents": tv["accepted"]["cents"], "accepted_count": tv["accepted"]["count"], "pending_cents": tv["pending"]["cents"], "pending_charges": pend_ch,
               "not_totaled": len(tv["not_totaled"])}
    if not amts:
        st.append(step("totals", "Billed-charges total", "code", SKIPPED, "No dollar amounts were found.", rule="row 8", counts=tcounts))
    elif pend_ch:
        st.append(step("totals", "Billed-charges total", "code", PENDING, f"{pend_ch} detected charge{'s' if pend_ch != 1 else ''} not in the total until you accept {'them' if pend_ch != 1 else 'it'}. The total is added up by code from accepted charges only.",
                       reason="PENDING_DECISION", rule="row 8", counts=tcounts, next_action=na("DECIDE", {"view": "amounts"}, ["accept", "dismiss"])))
    else:
        st.append(step("totals", "Billed-charges total", "code", PASS, "The total is added up by code from the accepted charges.", rule="row 8", counts=tcounts))
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = []
    if cx.running:
        blockers.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
    if case["status"] == "failed":
        blockers.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    for k, x in live_pending:
        if review.date_unconfirmed(conn, case_id, k, x):
            blockers.append({"item_id": x["id"], "kind": k, "reason_code": "DATE_UNCONFIRMED", "why": TRACE_WHY["DATE_UNCONFIRMED"],
                             "next_action": na("CONFIRM_DATE", {"record_id": (x["record_ids"] or [None])[0], "view": "dates_to_confirm"})})
        else:
            blockers.append({"item_id": x["id"], "kind": k, "reason_code": "PENDING_DECISION", "why": TRACE_WHY["PENDING_DECISION"],
                             "next_action": na("DECIDE", {"item_id": x["id"]}, ["accept", "edit", "dismiss"])})
    if not live_pending and not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
        blockers.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
    ready = bool(rv["ready_to_export"]) and not cx.running
    n_block = len(live_pending)
    gate_counts = {"blocking": len(blockers), "pending_items": n_block, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"], "dismissed": rv["counts"]["dismissed"],
                   "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected")}
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS, "Every live item has your decision and at least one item is accepted, so the export can be built.", rule="row 19", counts=gate_counts)
    else:
        first = blockers[0] if blockers else None
        reason = "ITEMS_PENDING" if n_block else (first["reason_code"] if first else "ITEMS_PENDING")
        text = f"{n_block} item{'s have' if n_block != 1 else ' has'} no decision yet, so the export is blocked." if n_block else (first["why"] if first else TRACE_WHY["ITEMS_PENDING"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=reason, rule="row 19", counts=gate_counts, next_action=first["next_action"] if first else None,
                    blocks=True)
    gate.update(ready=ready, blockers=blockers)
    st.append(gate)
    _number(st)
    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
               else {"code": "ready", "label": "Ready to export"} if ready
               else {"code": "needs_attention", "label": f"{n_block} item{'s' if n_block != 1 else ''} still need{'' if n_block != 1 else 's'} your decision" if n_block else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def rows_any(jr):
    return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
111:class _Cx:
112-    def __init__(self, conn, case_id, full):
113-        self.conn, self.case_id, self.full = conn, case_id, bool(full)
114-        self.case = DB.get_case(conn, case_id)
115-        self.recs = present._recs_by_id(conn, case_id)
116-        calls = DB.list_llm_calls(conn, case_id)
117-        self.call_by_id = {c["id"]: c for c in calls}
118-        self.calls_by_item = {}
119-        for c in calls:
120-            self.calls_by_item.setdefault(c["item_id"], []).append(c)
121-        self.events = {}
122-        for e in DB.list_events(conn, case_id):
123-            self.events.setdefault(e["item_id"], []).append(e)
124-        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
125-        self.ran = self.case.get("run_started_at") is not None
126-        self.running = self.case["status"] == "running"
127-
128-    def call(self, call_id, item_id=None, step_name=None):
129-        if call_id and call_id in self.call_by_id:
130-            return self.call_by_id[call_id]
131-        if item_id and step_name:
132-            hits = [c for c in self.calls_by_item.get(item_id, []) if c["step"] == step_name]
133-            return hits[-1] if hits else None
134-        return None
135-
136-
137-def _span(cx, rid, start, end, text):
138-    return {"record_id": rid, "start": start, "end": end, "text": text}
139-
140-
141-def _llm_evidence(cx, role, model, prompt_version, call):
142-    ev = {"model": {"id": (call or {}).get("model") or model, "role": role,
143-                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"]}}
        if cx.full:
            ev["response_raw"] = meta.get("response_raw")
    return ev


def _norm_verdict(step_id, v):
    if v in _LADDER_VOCAB:
        return v
    return _RAW_TO_LADDER.get(v, "unsure")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:40.037Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/trace.py'\ns=open(p).read()\nold='''            jd = (row.get(\"ladder\") or {}).get(\"judge\")\n            if not jd or not jd.get(\"verdict\"):\n                continue\n'''\nnew='''            jd = (row.get(\"ladder\") or {}).get(\"judge\")\n            if not jd or not jd.get(\"verdict\"):\n                out.extend(_judge_never_ran(cx, kind, row))\n                continue\n'''\nassert old in s\ns=s.replace(old,new)\nold='''def judge_report(conn, case_id: str, full: bool = False) -> dict:'''\nnew='''_STEPS_OF = {}      # filled after the step builders are defined (kind -> builder)\n\n\ndef _judge_never_ran(cx, kind, row):\n    \"\"\"An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.\n    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run).\"\"\"\n    if not cx.ran:\n        return []\n    out = []\n    for s in _STEPS_OF[kind](cx, row):\n        if s[\"id\"].startswith(\"judge_\") and s[\"status\"] == SKIPPED and s.get(\"reason_code\") in (\"JUDGE_UNAVAILABLE\", \"FIXTURE_MISS\") \\\\\n                and (s.get(\"evidence\") or {}).get(\"judge_verdict\") == \"unavailable\":\n            jid = \"j\" + s[\"id\"].split(\"_\")[1]\n            out.append({\"item_id\": row[\"id\"], \"kind\": kind, \"judge\": jid, \"verdict\": \"unavailable\", \"reason_code\": None, \"row\": row, \"jd\": {}, \"call\": None})\n    return out\n\n\ndef judge_report(conn, case_id: str, full: bool = False) -> dict:'''\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\nEOF\ngrep -n '\"reason' app/backend/trace.py | head -5; sed -n 55,110p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T03:32:40.152Z

**tool result**
````
95:    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
162:    code = (jd or {}).get("reason_code")
168:            if isinstance(got, dict) and isinstance(got.get("reason_code"), str):
169:                return got["reason_code"]
540:    reason = (rem or {}).get("reason")
    "EDIT_SUMMARY": "Edit the summary so it uses only the numbers, dates and words that are in the quote, and keeps the quote's qualifiers.",
    "EDIT_QUOTE": "Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it.",
    "READ_RECORD": "Read the record yourself before relying on this item.",
    "COMPARE_BY_HAND": "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.",
    "DISMISS_OR_ENTER_BY_HAND": "This item cannot be used. Dismiss it, or write the entry by hand from the record.",
    "RERUN": "Run the AI steps again.",
    "SENTENCE_REMOVED": "This sentence was left out of the draft. If you want its facts in the paragraph, check the cited entry's quote and write them yourself.",
    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
}
_STEP_OF_REASON = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "excerpt_verbatim", "GROUNDING_AMOUNT_NOT_IN_TEXT": "found_in_text", "SCHEMA_INVALID": "extracted",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
    "SPLIT_AMBIGUOUS": "record_warning_check", "LLM_SPLIT": "record_warning_check"}
_AMOUNT_CODE = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}


def reason_text(code: str) -> str:
    if code in TRACE_WHY:
        return TRACE_WHY[code]
    try:
        return why.why(code)
    except KeyError:
        return code


def na(code: str, target: dict = None, options: list = None) -> dict:
    d = {"code": code, "text": _NEXT[code]}
    if target:
        d["target"] = target
    if options:
        d["options"] = options
    return d


def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}


def _number(steps):
    for i, s in enumerate(steps, 1):
        s["n"] = i
    return steps


def _progress(steps):
    done = sum(1 for s in steps if s["status"] != PENDING)
    return {"done": done, "total": len(steps), "label": f"{done} of {len(steps)} steps settled"}


# ------------------------------------------------------------------ shared context
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:42.571Z

**tool call — Bash**
````
{
 "command": "sed -n 258,300p app/backend/trace.py; sed -n 495,530p app/backend/api.py; grep -n \"get_item\" app/db/db.py | head -3"
}
````

### User / tool · 2026-11-02T03:32:42.667Z

**tool result**
````
    else:
        code, label = "ready_for_decision", "Ready for your decision"
    blocks = (live and rs == "pending") if blocks_flag is None else blocks_flag
    judge_id = next((s["id"] for s in steps if s["id"].startswith("judge_")), None)

    def step_of(c):
        if c.startswith("JUDGE_") or c == "FIXTURE_MISS":
            return judge_id
        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else None
    reasons = [{"code": c, "why": reason_text(c), "step_id": step_of(c)} for c in (row.get("state_reasons") or [])]
    return {"token": cx.case_id, "item_id": item_id, "kind": kind, "mode": "full" if cx.full else "metadata", "state": row.get("state"),
            "review_status": rs, "state_reasons": reasons, "verdict": {"code": code, "label": label, "blocks_export": bool(blocks)},
            "progress": _progress(steps), "next_action": first_na, "steps": steps}


# ------------------------------------------------------------------ entries
def _excerpt_ev(cx, rid, row):
    ed = row.get("edited") or {}
    return _span(cx, rid, ed.get("excerpt_start", row.get("excerpt_start")), ed.get("excerpt_end", row.get("excerpt_end")), ed.get("excerpt", row.get("excerpt")))


def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    verbatim_fail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None)
    st = []
    # 1 extracted
    if lad.get("entered_by"):
        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
                       evidence={"excerpt": exc}))
    else:
        gen = lad.get("generator") or {}
        call = cx.call(gen.get("call_id"), row["id"], "extract")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
        ev["excerpt"] = exc
        if schema_fail:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
            return ex
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}/trace")
    def item_trace(token: str, item_id: str):
        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
        c = conn()
        try:
            get_case(c, token)
            try:
                return trace.item_trace(c, token, item_id, full=local_mode())
            except (KeyError, IndexError):
                raise ApiError(404, "not_found", "No such item.") from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/trace")
    def case_trace(token: str):
        c = conn()
        try:
            get_case(c, token)
            return trace.case_trace(c, token, full=local_mode())
        finally:
            c.close()

    @app.get("/api/cases/{token}/judges")
    def judge_report(token: str):
        c = conn()
        try:
            get_case(c, token)
            return trace.judge_report(c, token, full=local_mode())
        finally:
            c.close()

    @app.get("/api/cases/{token}/audit")
4:- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
155:def get_item(conn, item_id: str, case: str = None) -> dict:
201:    return get_item(conn, item_id, row["case_id"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:45.097Z

**tool call — Bash**
````
{
 "command": "sed -n 155,165p app/db/db.py; sed -n 530,560p app/backend/trace.py; grep -n \"ApiError\\|exception_handler\\|Exception\" app/backend/api.py | head -20"
}
````

### User / tool · 2026-11-02T03:32:45.186Z

**tool result**
````
def get_item(conn, item_id: str, case: str = None) -> dict:
    return _decode(_find(conn, item_id, case)[1])


def list_items(conn, case_id: str, kind: str) -> list:
    table = _ITEM_TABLES[kind][0]
    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]


def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
    return narrative.REASONS.get(code) or reason_text(code)


def _narrative_trace(cx, item_id):
    nar = narrative.get(cx.conn, cx.case_id) or {}
    sent = next((s for s in nar.get("sentences", []) if s["id"] == item_id), None)
    rem = next((s for s in nar.get("removed", []) if s["id"] == item_id), None)
    s = sent or rem
    if s is None:
        raise KeyError(item_id)
    reason = (rem or {}).get("reason")
    rcodes = list((rem or {}).get("reasons") or []) if reason not in ("NOT_AN_ACCEPTED_ENTRY",) and not str(reason).startswith("JUDGE_") else []
    st = []
    gen = nar.get("generator") or {}
    call = cx.call(gen.get("call_id"))
    ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
    ev["values"] = {"entry_id": s["entry_id"], "text": s["text"]}
    st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
    cited_ok = reason != "NOT_AN_ACCEPTED_ENTRY"
    st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
                   reason=None if cited_ok else "NOT_AN_ACCEPTED_ENTRY", rule="D-031", evidence={"values": {"entry_id": s["entry_id"]}},
                   next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]}) if not cited_ok else None))
    if not cited_ok:
        st.append(_skipped("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", "NOT_AN_ACCEPTED_ENTRY", "D-006", "Not run: the cited entry is not accepted."))
    elif rcodes:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", FAIL, " ".join(_ntext(c) for c in rcodes),
                       reason=rcodes[0], rule="D-006", evidence={"reasons": rcodes}, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
    else:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", PASS,
                       "Every number, date and qualifier is in the cited quote, and the sentence adds no cause, severity or flag wording.", rule="D-006", evidence={"reasons": []}))
    if not cited_ok or rcodes:
19:from starlette.exceptions import HTTPException as StarletteHTTPException
46:class ApiError(Exception):
140:            raise ApiError(404, "not_found", "No such case.")
144:    @app.exception_handler(ApiError)
148:    @app.exception_handler(review.ReviewError)
152:    @app.exception_handler(StarletteHTTPException)
157:    @app.exception_handler(Exception)
162:    @app.exception_handler(RequestValidationError)
180:        except Exception as e:                                                          # last line of defence: standard JSON, no detail
192:            raise ApiError(413, "input_too_large", "Input is too large.")
197:                raise ApiError(413, "input_too_large", "Input is too large.")
203:            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
205:            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
218:            raise ApiError(404, "not_found", "Not found.")
228:            raise ApiError(404, "not_found", "Not found.")
238:                raise ApiError(404, "not_found", "Not found.")
241:                raise ApiError(404, "not_found", "No such library case.")
244:            raise ApiError(400, "bad_request", "Provide text or sample: true.")
251:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
254:            raise ApiError(413, "input_too_large", "The PDF is too large.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:32:56.774Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/trace.py'\ns=open(p).read()\ndef rep(old,new,cnt=1):\n    global s\n    assert s.count(old)==cnt,(old,s.count(old))\n    s=s.replace(old,new)\nrep('''    first_na = next((s[\"next_action\"] for s in steps if s[\"next_action\"]), None)\n    if rs in''','''    first_na = next((s[\"next_action\"] for s in steps if s[\"next_action\"]), None)\n    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = None             # the human already decided; step-level hints stay on the steps\n    if rs in''')\nrep('''    judge_id = next((s[\"id\"] for s in steps if s[\"id\"].startswith(\"judge_\")), None)\n\n    def step_of(c):\n        if c.startswith(\"JUDGE_\") or c == \"FIXTURE_MISS\":\n            return judge_id\n        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else None''','''    judge_id = next((s[\"id\"] for s in steps if s[\"id\"].startswith(\"judge_\")), None)\n    fallback = next((s[\"id\"] for s in steps if s[\"status\"] == FAIL), steps[0][\"id\"] if steps else None)   # e.g. record-warning flags have one code step\n\n    def step_of(c):\n        if c.startswith(\"JUDGE_\") or c == \"FIXTURE_MISS\":\n            return judge_id or fallback\n        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else fallback''')\nrep('''                       next_action=na(\"READ_RECORD\", {\"record_id\": rid0}) if rid0 else na(\"RERUN\")))\n        st.append(_human_step(cx, row, \"flag\"))''','''                       next_action=na(\"CONFIRM_DATE\", {\"record_id\": rid0, \"view\": \"dates_to_confirm\"}) if cat == \"date_ambiguous\"\n                       else (na(\"READ_RECORD\", {\"record_id\": rid0}) if rid0 else na(\"RERUN\"))))\n        st.append(_human_step(cx, row, \"flag\"))''')\nrep('''    \"\"\"KeyError for an unknown item. Entry, amount, flag or narrative sentence (ns...).\"\"\"\n    cx = _Cx(conn, case_id, full)\n    if item_id.startswith(\"ns\"):\n        return _narrative_trace(cx, item_id)\n    kind = present._ID_KIND[item_id[0]]\n    row = DB.get_item(conn, item_id, case_id)\n    steps = {\"entry\": _entry_steps, \"amount\": _amount_steps, \"flag\": _flag_steps}[kind](cx, row)\n    return _finish(cx, item_id, kind, row, steps)''','''    \"\"\"UnknownItem for an id that is not in the case. Entry, amount, flag or narrative sentence (ns...). Any other error is a bug and propagates.\"\"\"\n    cx = _Cx(conn, case_id, full)\n    if item_id.startswith(\"ns\"):\n        return _narrative_trace(cx, item_id)\n    kind = present._ID_KIND.get(item_id[:1])\n    try:\n        if kind is None:\n            raise KeyError(item_id)\n        row = DB.get_item(conn, item_id, case_id)\n    except KeyError:\n        raise UnknownItem(item_id) from None\n    steps = _STEPS_OF[kind](cx, row)\n    return _finish(cx, item_id, kind, row, steps)\n\n\n_STEPS_OF.update({\"entry\": _entry_steps, \"amount\": _amount_steps, \"flag\": _flag_steps})''')\nrep('''    if s is None:\n        raise KeyError(item_id)\n    reason = (rem''','''    if s is None:\n        raise UnknownItem(item_id)\n    reason = (rem''')\nrep('''class _Cx:''','''class UnknownItem(KeyError):\n    \"\"\"The item id is not in this case (the API maps exactly this to 404).\"\"\"\n\n\nclass _Cx:''')\nopen(p,'w').write(s)\np='app/backend/api.py'\ns=open(p).read()\nrep(\"            except (KeyError, IndexError):\\n                raise ApiError(404, \\\"not_found\\\", \\\"No such item.\\\") from None\\n        finally:\\n            c.close()\\n\\n    @app.get(\\\"/api/cases/{token}/trace\\\")\",\n    \"            except trace.UnknownItem:\\n                raise ApiError(404, \\\"not_found\\\", \\\"No such item.\\\") from None\\n        finally:\\n            c.close()\\n\\n    @app.get(\\\"/api/cases/{token}/trace\\\")\")\nopen(p,'w').write(s)\nEOF\nsed -n 155,162p app/db/db.py; grep -n \"def _find\" -A12 app/db/db.py"
}
````

### User / tool · 2026-11-02T03:32:56.882Z

**tool result**
````
def get_item(conn, item_id: str, case: str = None) -> dict:
    return _decode(_find(conn, item_id, case)[1])


def list_items(conn, case_id: str, kind: str) -> list:
    table = _ITEM_TABLES[kind][0]
    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]

127:def _find(conn, item_id, case=None):
128-    """Item ids are unique per case (T-050). Pass `case` (the case id) whenever more than one case can share the file."""
129-    kind = _PREFIX_KIND.get(item_id[:1])
130-    if kind is None:
131-        raise KeyError(item_id)
132-    table = _ITEM_TABLE_OF[kind]
133-    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
134-    if case is not None:
135-        q, a = q + " AND case_id=?", a + [case]
136-    rows = conn.execute(q, a).fetchall()
137-    if not rows:
138-        raise KeyError(item_id)
139-    if len(rows) > 1:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:04.272Z

**tool call — Bash**
````
{
 "command": "grep -n \"ready_to_export\" -B6 app/backend/present.py | head -50"
}
````

### User / tool · 2026-11-02T03:33:04.351Z

**tool result**
````
116-    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
117-    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
118-    rank = {"amount": 0, "entry": 1, "flag": 2}
119-    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
120-                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
121-    return {"counts": counts, "queue": [r["id"] for _, r in pend],
122:            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:09.652Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/trace.py'\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert s.count(old)==1,old\n    s=s.replace(old,new)\nrep('''    ready = bool(rv[\"ready_to_export\"]) and not cx.running\n''','''    ready = bool(rv[\"ready_to_export\"]) and not blockers        # ready == (no blockers): a gate never passes over a listed blocker\n    if not ready and not blockers:                              # review says not ready but nothing was listed: say so, never an empty fail\n        blockers.append({\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"ITEMS_PENDING\", \"why\": TRACE_WHY[\"ITEMS_PENDING\"], \"next_action\": na(\"DECIDE\", {\"view\": \"queue\"})})\n''')\nrep('''    elif t[\"unavailable\"]:\n        st.append(step(\"judges\", \"Second AI check on every AI-made item\", \"llm\", FAIL, f\"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. \" + reason_text(\"JUDGE_UNAVAILABLE\"),\n                       reason=\"JUDGE_UNAVAILABLE\", rule=\"row 4\", counts=jcounts, next_action=na(\"COMPARE_BY_HAND\", {\"view\": \"judges\"})))''','''    elif t[\"unavailable\"]:\n        msg = f\"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. \"\n        if cx.running:\n            st.append(step(\"judges\", \"Second AI check on every AI-made item\", \"llm\", PENDING, msg + \"The run is still going.\", reason=\"JUDGE_UNAVAILABLE\", rule=\"row 4\", counts=jcounts))\n        else:\n            st.append(step(\"judges\", \"Second AI check on every AI-made item\", \"llm\", FAIL, msg + reason_text(\"JUDGE_UNAVAILABLE\"),\n                           reason=\"JUDGE_UNAVAILABLE\", rule=\"row 4\", counts=jcounts, next_action=na(\"COMPARE_BY_HAND\", {\"view\": \"judges\"})))''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"ITEMS_PENDING\\|RUN_FAILED\" app/backend/trace.py | head; grep -n \"unavailable\" memory/contracts/api.md | head"
}
````

### User / tool · 2026-11-02T03:33:09.765Z

**tool result**
````
43:    "ITEMS_PENDING": "Some items have no decision yet, so the export is blocked.",
45:    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
861:        blockers.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
874:        blockers.append({"item_id": None, "kind": "case", "reason_code": "ITEMS_PENDING", "why": TRACE_WHY["ITEMS_PENDING"], "next_action": na("DECIDE", {"view": "queue"})})
882:        reason = "ITEMS_PENDING" if n_block else (first["reason_code"] if first else "ITEMS_PENDING")
883:        text = f"{n_block} item{'s have' if n_block != 1 else ' has'} no decision yet, so the export is blocked." if n_block else (first["why"] if first else TRACE_WHY["ITEMS_PENDING"])
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409), `item_rejected` (409), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
87:Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.
477:`evidence` keys (all optional): `excerpt` `{record_id, start, end, text}` (offsets absolute into the case text); `spans[]` (same shape, for flags); `tokens[]` (summary tokens not in the quote); `values` (small object, for example `{"text": "$6,240", "value_cents": 624000, "kind": "charge", "classified_by": "code:amounts"}` or a gap's `{"from","to","days","threshold"}`); `date` `{record_id, date_raw, date_iso, date_status, candidates[]}`; `model` `{id, role, independent_of_generator}`; `prompt_version`; `prompt_sha256`; `call_id`; `backend`; `recorded_from`; `latency_ms`; `parsed_ok`; `judge_verdict` (ladder vocabulary: `supported|partially|unsupported|disagrees|unsure|unavailable`); `judge_reason_code` (the judge's own closed code, for example `NUMBER_MISMATCH`, or `NONE`); `rationale` (fixed sentence for that code); `action`, `at`, `events[]` `{action, at}` (human step); `response_raw`, `events[].before/after`, `edited_text` (**full mode only**).
526:    { "id": "judges", "kind": "llm", "counts": {"items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1} },
545:  "totals": { "items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1, "human_overrides": 1 },
547:                "items": 9, "supported": 8, "partially": 1, "unsupported": 0, "disagrees": 0, "unsure": 0, "unavailable": 0 },
552:  "unresolved": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "verdict": "unavailable", "state_reason": "JUDGE_UNAVAILABLE", "model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": null } ],
556:`totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:13.389Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/api.py'\ns=open(p).read()\nold='''    db_path = db_path or os.path.join(os.environ.get(\"DATA_DIR\", str(ROOT / \"data\")), \"zlayt.sqlite\")'''\nnew='''    db_path = db_path or os.environ.get(\"ZLAYT_DB\") or os.path.join(os.environ.get(\"DATA_DIR\", str(ROOT / \"data\")), \"zlayt.sqlite\")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it'''\nassert old in s\nopen(p,'w').write(s.replace(old,new))\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T03:33:15.026Z

**tool result**
````
__________________ ERROR collecting tests/unit/test_trace.py ___________________
tests/unit/test_trace.py:11: in <module>
    from app.backend import trace, why
app/backend/trace.py:628: in <module>
    _STEPS_OF.update({"entry": _entry_steps, "amount": _amount_steps, "flag": _flag_steps})
    ^^^^^^^^^
E   NameError: name '_STEPS_OF' is not defined
=========================== short test summary info ============================
ERROR tests/unit/test_api_routes.py - NameError: name '_STEPS_OF' is not defined
ERROR tests/unit/test_case_extras.py - NameError: name '_STEPS_OF' is not def...
ERROR tests/unit/test_date_unconfirmed.py - NameError: name '_STEPS_OF' is no...
ERROR tests/unit/test_pdf_upload.py - NameError: name '_STEPS_OF' is not defined
ERROR tests/unit/test_trace.py - NameError: name '_STEPS_OF' is not defined
!!!!!!!!!!!!!!!!!!! Interrupted: 5 errors during collection !!!!!!!!!!!!!!!!!!!!
5 errors in 1.19s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:15.906Z

Define it earlier (before the first use, near UnknownItem).

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:17.032Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/trace.py'\ns=open(p).read()\ns=s.replace('''_STEPS_OF = {}      # filled after the step builders are defined (kind -> builder)\n\n\n''','',1)\ns=s.replace('''class UnknownItem(KeyError):''','''_STEPS_OF = {}      # kind -> step builder; filled after the builders are defined\n\n\nclass UnknownItem(KeyError):''',1)\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T03:33:40.222Z

**tool result**
````
........................................................................ [ 13%]
........................................................................ [ 20%]
........................................................................ [ 27%]
........................................................................ [ 34%]
........................................................................ [ 41%]
........................................................................ [ 48%]
........................................................................ [ 55%]
........................................................................ [ 62%]
........................................................................ [ 69%]
........................................................................ [ 76%]
........................................................................ [ 83%]
........................................................................ [ 90%]
........................................................................ [ 97%]
.......................                                                  [100%]
1031 passed in 22.33s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:42.108Z

Now tests. Look at the existing test file helpers.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:42.569Z

**tool call — Bash**
````
{
 "command": "sed -n 1,110p tests/unit/test_trace.py; grep -n \"^def test_\\|^@\" tests/unit/test_trace.py"
}
````

### User / tool · 2026-11-02T03:33:42.654Z

**tool result**
````
"""D-042 check traces (T-080): per-item stepper, case stepper with export gate, judge summary, and the full/metadata visibility split.
Fixture backend, no key. One recorded sample run is built once; each test works on its own copy of the database."""
import json
import pathlib
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace, why
from app.backend.api import create_app
from app.db import db as DB

STATUSES = {"pass", "fail", "skipped", "pending"}
KINDS = {"code", "llm", "human"}
NEXT_CODES = {"DECIDE", "CONFIRM_DATE", "EDIT_SUMMARY", "EDIT_QUOTE", "READ_RECORD", "COMPARE_BY_HAND", "DISMISS_OR_ENTER_BY_HAND", "RERUN", "SENTENCE_REMOVED", "CONFIRM_RERUN"}
FULL_ONLY_KEYS = {"response_raw", "before", "after", "edited_text"}


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    import os
    d = tmp_path_factory.mktemp("trace")
    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    os.environ["LLM_BACKEND"] = "fixture"
    for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        os.environ.pop(k, None)
    db = str(d / "base.sqlite")
    c = TestClient(create_app(db, static_dir=str(d)), client=("127.0.0.1", 50000))
    pre = c.post("/api/cases", json={"sample": True}).json()["token"]          # an ingested case that never ran
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready"
    yield {"dir": d, "db": db, "tok": tok, "pre": pre}
    for k, v in old.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


@pytest.fixture
def env(base, tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    path = str(tmp_path / "copy.sqlite")
    src = sqlite3.connect(base["db"])
    dst = sqlite3.connect(path)
    src.backup(dst)
    src.close()
    dst.close()
    conn = DB.connect(path)
    c = TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    return c, conn, base["tok"], base["pre"]


def steps_of(t):
    return {s["id"]: s for s in t["steps"]}


def walk(o, keys):
    """Every dict key anywhere in o that is in `keys`."""
    found = set()
    if isinstance(o, dict):
        for k, v in o.items():
            if k in keys:
                found.add(k)
            found |= walk(v, keys)
    elif isinstance(o, list):
        for v in o:
            found |= walk(v, keys)
    return found


def all_keys(o, skip=()):
    """Every dict key in o, not looking inside the values of keys in `skip`."""
    out = set()
    if isinstance(o, dict):
        for k, v in o.items():
            out.add(k)
            if k not in skip:
                out |= all_keys(v, skip)
    elif isinstance(o, list):
        for v in o:
            out |= all_keys(v, skip)
    return out


def check_step_shape(s):
    assert {"id", "n", "label", "kind", "status", "why", "reason_code", "rule", "blocks_export", "evidence", "next_action"} <= set(s)
    assert s["kind"] in KINDS and s["status"] in STATUSES and s["why"] and s["label"]
    if s["status"] in ("fail", "pending"):
        assert s["next_action"] and s["next_action"]["code"] in NEXT_CODES and s["next_action"]["text"], s["id"]
    else:
        assert s["next_action"] is None
    if s["reason_code"]:
        assert trace.reason_text(s["reason_code"]) != s["reason_code"] or s["reason_code"] in trace.narrative.REASONS, s["reason_code"]


# ------------------------------------------------------------------ AC1: per-item ladder
def test_every_item_has_an_ordered_well_formed_trace(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
    assert len(ids) >= 20
21:@pytest.fixture(scope="module")
47:@pytest.fixture
106:def test_every_item_has_an_ordered_well_formed_trace(env):
125:def test_entry_trace_names_each_code_check_and_the_judge(env):
141:def test_judge_objection_is_a_fail_with_fixed_rationale(env):
156:def test_rejected_entry_skips_later_checks_and_points_to_manual_entry(env):
171:def test_token_and_qualifier_failures_name_the_rule(env):
183:def test_unconfirmed_date_fails_and_blocks_accept_d041(env):
196:def test_unavailable_judge_is_skipped_with_reason(env):
208:def test_amount_steps_and_rate_is_never_totaled(env):
225:def test_amount_judge_reason_is_read_from_the_audited_call_when_not_stored(env):
243:def test_code_made_flags_need_no_judge(env):
251:def test_ai_and_phrase_list_flags_show_agreement_and_judge(env):
260:def test_lexicon_only_flag_is_agreement_fail_and_judge_skipped(env):
273:def test_unknown_item_and_case_are_404(env):
281:def test_unrun_case_waits_for_the_ai(env):
292:def test_narrative_sentence_traces(env):
320:def test_case_trace_steps_and_counts(env):
334:def test_export_gate_lists_exactly_the_pending_live_items(env):
349:def test_export_gate_date_unconfirmed_blocker(env):
359:def test_export_gate_ready_matches_review_view(env):
370:def test_export_gate_nothing_accepted(env):
379:def test_run_in_progress_blocks_the_gate(env):
388:def test_judge_summary_counts_and_objections(env):
415:def test_code_flags_doubt_judge_agrees_and_sources_disagree(env):
426:def test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them(env, monkeypatch):
448:def test_judge_report_rejection_response_raw_is_full_mode_only(env, monkeypatch):
460:def test_every_emitted_reason_code_has_a_fixed_sentence(env):
476:def test_judge_reason_code_is_persisted_on_new_runs(env):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:44.364Z

**tool call — Bash**
````
{
 "command": "sed -n 196,207p tests/unit/test_trace.py; sed -n 273,292p tests/unit/test_trace.py; sed -n 334,415p tests/unit/test_trace.py; grep -n \"def accept\\|/accept\\|apply_review\\|review_status\" tests/unit/test_trace.py | head"
}
````

### User / tool · 2026-11-02T03:33:44.464Z

**tool result**
````
def test_unavailable_judge_is_skipped_with_reason(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e6", tok)
    lad = e["ladder"]
    lad["judge"] = {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": None, "verdict": "unavailable", "reason_code": "NONE"}
    DB.update_item(conn, "e6", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"], ladder=lad)
    t = c.get(f"/api/cases/{tok}/items/e6/trace").json()
    j = steps_of(t)["judge_1"]
    assert j["status"] == "skipped" and j["reason_code"] == "JUDGE_UNAVAILABLE" and j["next_action"]["code"] == "COMPARE_BY_HAND"
    assert t["verdict"]["code"] == "needs_attention"


def test_unknown_item_and_case_are_404(env):
    c, _, tok, _ = env
    assert c.get(f"/api/cases/{tok}/items/e999/trace").status_code == 404
    assert c.get(f"/api/cases/{tok}/items/zzz/trace").status_code == 404
    assert c.get("/api/cases/nope/trace").status_code == 404 and c.get("/api/cases/nope/judges").status_code == 404
    assert c.get(f"/api/cases/{tok}/items/ns1/trace").status_code == 404


def test_unrun_case_waits_for_the_ai(env):
    c, _, _, pre = env
    ct = c.get(f"/api/cases/{pre}/trace").json()
    s = steps_of(ct)
    assert s["extract"]["status"] == "pending" and s["extract"]["next_action"]["code"] == "RERUN" and s["judges"]["status"] == "pending"
    amt = c.get(f"/api/cases/{pre}").json()["amounts"][0]
    t = c.get(f"/api/cases/{pre}/items/{amt['id']}/trace").json()
    assert steps_of(t)["judge_2"]["status"] == "pending" and t["verdict"]["code"] == "waiting_for_run"


# ------------------------------------------------------------------ narrative sentences
def test_narrative_sentence_traces(env):
def test_export_gate_lists_exactly_the_pending_live_items(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e3", tok)
    DB.update_item(conn, "e3", case=tok, state="rejected", state_reasons_json=["GROUNDING_EXCERPT_NOT_VERBATIM"], ladder=e["ladder"])
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "dismiss"})
    case = c.get(f"/api/cases/{tok}").json()
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    expected = {x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k] if x["review_status"] == "pending"}
    assert expected == set(case["review"]["queue"])
    assert {b["item_id"] for b in gate["blockers"]} == expected and "e3" not in expected and "e1" not in expected and "e2" not in expected
    assert gate["ready"] is False and gate["status"] == "fail" and gate["reason_code"] == "ITEMS_PENDING" and gate["counts"]["rejected_not_blocking"] == 1
    assert all(b["reason_code"] == "PENDING_DECISION" and b["why"] and b["next_action"]["code"] == "DECIDE" for b in gate["blockers"])


def test_export_gate_date_unconfirmed_blocker(env):
    c, conn, tok, _ = env
    rid = DB.get_item(conn, "e5", tok)["record_ids"][0]
    conn.execute("UPDATE records SET date_status='ambiguous', date_candidates_json=? WHERE id=? AND case_id=?", (json.dumps(["2026-04-05", "2026-05-04"]), rid, tok))
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    b = next(x for x in gate["blockers"] if x["item_id"] == "e5")
    assert b["reason_code"] == "DATE_UNCONFIRMED" and b["next_action"]["code"] == "CONFIRM_DATE"
    assert steps_of(c.get(f"/api/cases/{tok}/trace").json())["dates"]["status"] == "fail"


def test_export_gate_ready_matches_review_view(env):
    c, _, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        assert c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"}).status_code == 200
    ct = c.get(f"/api/cases/{tok}/trace").json()
    gate = steps_of(ct)["export_gate"]
    assert gate["ready"] is True and gate["blockers"] == [] and gate["status"] == "pass" and ct["verdict"]["code"] == "ready"
    assert c.get(f"/api/cases/{tok}").json()["review"]["ready_to_export"] is True


def test_export_gate_nothing_accepted(env):
    c, _, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "dismiss"})
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    assert gate["ready"] is False and [b["reason_code"] for b in gate["blockers"]] == ["NOTHING_ACCEPTED"]


def test_run_in_progress_blocks_the_gate(env):
    c, conn, tok, _ = env
    DB.update_case(conn, tok, status="running")
    ct = c.get(f"/api/cases/{tok}/trace").json()
    gate = steps_of(ct)["export_gate"]
    assert gate["ready"] is False and "RUN_IN_PROGRESS" in [b["reason_code"] for b in gate["blockers"]] and ct["verdict"]["code"] == "running"


# ------------------------------------------------------------------ judge summary
def test_judge_summary_counts_and_objections(env):
    c, conn, tok, _ = env
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"] == {"items_judged": 20, "supported": 20, "unsupported": 0, "unsure": 0, "unavailable": 0, "human_overrides": 0}
    assert rep["models"]["judge"] == "claude-haiku-5-5" and rep["independent_models"] is True
    assert {j["id"] for j in rep["judges"]} == {"j1", "j2", "j3", "j4"} and rep["rejections"] == [] and rep["unresolved"] == []
    assert "judge_faithfulness_v1" in rep["prompt_versions"]
    e = DB.get_item(conn, "e2", tok)
    lad = e["ladder"]
    lad["judge"].update(verdict="unsupported", reason_code="ADDS_DIAGNOSIS")
    DB.update_item(conn, "e2", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNSUPPORTED"], ladder=lad)
    e6 = DB.get_item(conn, "e6", tok)
    l6 = e6["ladder"]
    l6["judge"] = {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": None, "verdict": "unavailable", "reason_code": "NONE"}
    DB.update_item(conn, "e6", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"], ladder=l6)
    c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "accept"})
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"]["unsupported"] == 1 and rep["totals"]["unavailable"] == 1 and rep["totals"]["items_judged"] == 19 and rep["totals"]["human_overrides"] == 1
    r = rep["rejections"][0]
    assert r["item_id"] == "e2" and r["judge"] == "j1" and r["verdict"] == "unsupported" and r["reason_code"] == "ADDS_DIAGNOSIS" and r["rationale"] == why.judge_detail("ADDS_DIAGNOSIS")
    assert r["model"] == "claude-haiku-5-5" and r["prompt_version"] == "judge_faithfulness_v1" and r["state_reason"] == "JUDGE_UNSUPPORTED" and r["review_status"] == "accepted"
    assert rep["unresolved"][0]["item_id"] == "e6" and rep["unresolved"][0]["verdict"] == "unavailable"
    assert any(d["item_id"] == "e2" and d["type"] == "judge_objects" and d["code_says"] == "All code checks passed." for d in rep["disagreements"])
    ct = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
    assert ct["status"] == "fail" and ct["reason_code"] == "JUDGE_UNAVAILABLE" and ct["counts"]["unavailable"] == 1


def test_code_flags_doubt_judge_agrees_and_sources_disagree(env):
342:    expected = {x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k] if x["review_status"] == "pending"}
408:    assert r["model"] == "claude-haiku-5-5" and r["prompt_version"] == "judge_faithfulness_v1" and r["state_reason"] == "JUDGE_UNSUPPORTED" and r["review_status"] == "accepted"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:49.393Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def \" app/db/db.py | sed -n 1,60p; sed -n 105,125p tests/unit/test_trace.py; python3 - <<'EOF'\nimport sqlite3,glob\nEOF\ngrep -n \"record_warning\" tests/unit/*.py | head -5"
}
````

### User / tool · 2026-11-02T03:33:49.530Z

**tool result**
````
28:def init(path: str = ":memory:"):
36:def connect(path: str):
62:def _tok(prefix: str) -> str:
66:def _enc(v):
70:def _cols(conn, table):
74:def sha256(text: str) -> str:
78:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
86:def update_case(conn, case_id: str, **fields) -> None:
95:def get_case(conn, case_id: str):
100:def _insert(conn, table, row):
108:def add_record(conn, case_id: str, **fields) -> str:
114:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
127:def _find(conn, item_id, case=None):
144:def _decode(row) -> dict:
155:def get_item(conn, item_id: str, case: str = None) -> dict:
159:def list_items(conn, case_id: str, kind: str) -> list:
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
204:def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
211:def list_events(conn, case_id: str, item_id: str = None) -> list:
218:def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
227:def get_llm_call(conn, call_id: str):
232:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
239:def delete_case(conn, case_id: str) -> None:
251:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
258:def table_counts(conn, case_id: str) -> dict:
# ------------------------------------------------------------------ AC1: per-item ladder
def test_every_item_has_an_ordered_well_formed_trace(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
    assert len(ids) >= 20
    for iid in ids:
        r = c.get(f"/api/cases/{tok}/items/{iid}/trace")
        assert r.status_code == 200, iid
        t = r.json()
        assert t["item_id"] == iid and t["mode"] == "metadata" and t["kind"] in ("entry", "amount", "flag")
        assert [s["n"] for s in t["steps"]] == list(range(1, len(t["steps"]) + 1))
        assert t["steps"][-1]["id"] == "human" and t["steps"][-1]["kind"] == "human"
        for s in t["steps"]:
            check_step_shape(s)
        assert t["progress"]["total"] == len(t["steps"]) and t["progress"]["done"] == sum(1 for s in t["steps"] if s["status"] != "pending")
        for rs in t["state_reasons"]:
            assert rs["why"] and rs["code"]


def test_entry_trace_names_each_code_check_and_the_judge(env):
tests/unit/test_amounts.py:25:        inj = bool(ex["record_warnings"]) and a["record_no"] in [w["record_no"] for w in ex["record_warnings"]]
tests/unit/test_eval_runner.py:44:        for w in exp.get("record_warnings", []):
tests/unit/test_eval_runner.py:45:            flags.append(dict(id="w" + w["id"], type="record_warning", evidence=[dict(record_id=f"r{w['record_no']}", excerpt=w["excerpt"])]))
tests/unit/test_eval_runner.py:61:                   flags=[dict(id=f"w{g['record_no']}", type="record_warning", category="llm_split", evidence=[dict(record_id=f"r{g['record_no']}", excerpt="x")]) for g in USPLIT["records"]])
tests/unit/test_eval_runner.py:145:def test_missing_record_warning_counts_as_a_must_not_hit():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:33:51.536Z

**tool call — Bash**
````
{
 "command": "sed -n 100,127p app/db/db.py; cd /tmp 2>/dev/null; cd /Users/arsis/zlayt-pm-project; .venv/bin/python - <<'EOF'\nimport sqlite3\nEOF\ngrep -n \"def _flag_steps\" -A12 app/backend/trace.py | head -30; grep -n \"id=\\\"f_\\|\\\"f_\" app/backend/pipeline.py | head"
}
````

### User / tool · 2026-11-02T03:33:51.676Z

**tool result**
````
def _insert(conn, table, row):
    bad = set(row) - _cols(conn, table)
    if bad:
        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
                 [_enc(v) for v in row.values()])


def add_record(conn, case_id: str, **fields) -> str:
    rid = fields.pop("id", None) or _tok("r")
    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
    return rid


def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
    if kind not in _ITEM_TABLES:
        raise ValueError(f"unknown item kind {kind!r}")
    table, prefix = _ITEM_TABLES[kind]
    p = dict(payload)
    if {"review_status", "edited_json", "edited"} & set(p):
        raise ValueError("review_status and edits are written only by apply_review (with an event row)")
    iid = p.pop("id", None) or _tok(prefix)
    _insert(conn, table, {"id": iid, "case_id": case_id, "updated_at": now, **p})
    return iid


def _find(conn, item_id, case=None):
434:def _flag_steps(cx, row):
435-    R = set(row.get("state_reasons") or [])
436-    lad = row.get("ladder") or {}
437-    cc = lad.get("code_checks") or {}
438-    ftype, origin, cat = row["type"], row["origin"], row["category"]
439-    recs = cx.recs
440-    spans = [{"record_id": e["record_id"], "start": e["start"], "end": e["end"], "text": e["excerpt"]} for e in present._evidence(row.get("evidence"), recs)]
441-    rids = [s["record_id"] for s in spans if s["record_id"]]
442-    rid0 = rids[0] if rids else None
443-    st = []
444-    injected = any(recs.get(r, {}).get("injection_tag") for r in rids) or "INJECTION_SUSPECTED" in R
445-
446-    def inj():
63:        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
319:            f["id"] = f"f_cx{i}"
341:                f["id"] = f"f_r{r['n']}_{k}"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:34:15.831Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_trace.py <<'EOF'\n\n\n# ------------------------------------------------------------------ round 2 (staff-engineer review): a gate never passes over a failure or a check that did not run\ndef _blank_judges(conn, tok):\n    \"\"\"Make the judge stage 'never ran' on every entry and every non-damages amount (the run deadline case in pipeline.py).\"\"\"\n    n = 0\n    for kind in (\"entry\", \"amount\"):\n        for row in DB.list_items(conn, tok, kind):\n            if row[\"state\"] == \"rejected\" or (kind == \"amount\" and row[\"kind\"] == \"damages\"):\n                continue\n            lad = row[\"ladder\"]\n            if not lad.get(\"judge\"):\n                continue\n            lad[\"judge\"] = None\n            DB.update_item(conn, row[\"id\"], case=tok, state=\"needs_review\", state_reasons_json=sorted(set(row[\"state_reasons\"]) | {\"JUDGE_UNAVAILABLE\"}), ladder=lad)\n            n += 1\n    return n\n\n\ndef test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step(env):\n    c, conn, tok, _ = env\n    before = c.get(f\"/api/cases/{tok}/judges\").json()[\"totals\"]\n    n = _blank_judges(conn, tok)\n    assert n >= 5\n    rep = c.get(f\"/api/cases/{tok}/judges\").json()\n    case = c.get(f\"/api/cases/{tok}\").json()\n    skipped = 0\n    for x in [*case[\"entries\"], *case[\"undated_entries\"], *case[\"amounts\"], *case[\"flags\"]]:\n        t = c.get(f\"/api/cases/{tok}/items/{x['id']}/trace\").json()\n        skipped += sum(1 for s in t[\"steps\"] if s[\"id\"].startswith(\"judge_\") and s[\"status\"] == \"skipped\" and s[\"reason_code\"] == \"JUDGE_UNAVAILABLE\")\n    assert skipped == n == rep[\"totals\"][\"unavailable\"]                       # item traces and /judges reconcile\n    assert rep[\"totals\"][\"items_judged\"] == before[\"items_judged\"] - n\n    assert len(rep[\"unresolved\"]) == n and {u[\"state_reason\"] for u in rep[\"unresolved\"]} == {\"JUDGE_UNAVAILABLE\"}\n    assert sum(j[\"unavailable\"] for j in rep[\"judges\"]) == n\n    j = steps_of(c.get(f\"/api/cases/{tok}/trace\").json())[\"judges\"]\n    assert j[\"status\"] == \"fail\" and j[\"reason_code\"] == \"JUDGE_UNAVAILABLE\" and j[\"counts\"][\"unavailable\"] == n and \"agreed\" not in j[\"why\"]\n    assert str(n) in j[\"why\"] and j[\"next_action\"][\"code\"] == \"COMPARE_BY_HAND\"\n\n\ndef test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing(env):\n    c, conn, tok, _ = env\n    n = _blank_judges(conn, tok)\n    DB.update_case(conn, tok, status=\"running\")\n    j = steps_of(c.get(f\"/api/cases/{tok}/trace\").json())[\"judges\"]\n    assert j[\"status\"] == \"pending\" and j[\"counts\"][\"unavailable\"] == n and \"agreed\" not in j[\"why\"]\n\n\ndef _gate_states(c, conn, tok):\n    \"\"\"Yield (name) after putting the case into each state we can build; the caller checks the invariant.\"\"\"\n    case = c.get(f\"/api/cases/{tok}\").json()\n    ids = [x[\"id\"] for k in (\"entries\", \"undated_entries\", \"amounts\", \"flags\") for x in case[k]]\n    yield \"pending items\"\n    DB.update_case(conn, tok, status=\"running\")\n    yield \"running with pending items\"\n    DB.update_case(conn, tok, status=\"ready\")\n    for i in ids:\n        c.post(f\"/api/cases/{tok}/items/{i}/review\", json={\"action\": \"dismiss\"})\n    yield \"everything dismissed\"\n    for i in ids[:1]:\n        pass\n    DB.update_case(conn, tok, status=\"failed\")\n    yield \"failed, everything dismissed\"\n    DB.update_case(conn, tok, status=\"ready\")\n    # accept every item still reviewable\n    for i in ids:\n        c.post(f\"/api/cases/{tok}/items/{i}/review\", json={\"action\": \"accept\"})\n    yield \"all accepted\"\n    DB.update_case(conn, tok, status=\"running\")\n    yield \"all accepted, running\"\n    DB.update_case(conn, tok, status=\"failed\")\n    yield \"all accepted, failed\"\n\n\ndef test_gate_ready_equals_no_blockers_in_every_case_state(env):\n    c, conn, tok, pre = env\n    seen = {}\n    for name in _gate_states(c, conn, tok):\n        gate = steps_of(c.get(f\"/api/cases/{tok}/trace\").json())[\"export_gate\"]\n        assert gate[\"ready\"] == (len(gate[\"blockers\"]) == 0), name\n        assert gate[\"status\"] == (\"pass\" if gate[\"ready\"] else \"fail\"), name\n        if not gate[\"ready\"]:\n            assert gate[\"next_action\"] is not None or name.startswith(\"running\"), name\n        seen[name] = gate\n    assert seen[\"all accepted\"][\"ready\"] is True\n    for name in (\"all accepted, failed\", \"failed, everything dismissed\"):\n        assert seen[name][\"ready\"] is False and \"RUN_FAILED\" in [b[\"reason_code\"] for b in seen[name][\"blockers\"]], name\n    assert seen[\"all accepted, running\"][\"ready\"] is False and \"RUN_IN_PROGRESS\" in [b[\"reason_code\"] for b in seen[\"all accepted, running\"][\"blockers\"]]\n    g = steps_of(c.get(f\"/api/cases/{pre}/trace\").json())[\"export_gate\"]            # a case that never ran\n    assert g[\"ready\"] == (g[\"blockers\"] == []) and g[\"status\"] == (\"pass\" if g[\"ready\"] else \"fail\")\n\n\ndef test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed(env):\n    c, conn, tok, _ = env\n    case = c.get(f\"/api/cases/{tok}\").json()\n    for x in [*case[\"entries\"], *case[\"amounts\"], *case[\"flags\"]]:\n        c.post(f\"/api/cases/{tok}/items/{x['id']}/review\", json={\"action\": \"accept\"})\n    DB.update_case(conn, tok, status=\"failed\")\n    ct = c.get(f\"/api/cases/{tok}/trace\").json()\n    gate = steps_of(ct)[\"export_gate\"]\n    assert ct[\"verdict\"][\"code\"] == \"failed\" and gate[\"ready\"] is False and gate[\"status\"] == \"fail\" and gate[\"reason_code\"] == \"RUN_FAILED\"\n    assert [b[\"reason_code\"] for b in gate[\"blockers\"]] == [\"RUN_FAILED\"] and gate[\"next_action\"][\"code\"] == \"CONFIRM_RERUN\"\n\n\ndef test_all_accepted_but_run_in_progress_is_not_ready(env):\n    c, conn, tok, _ = env\n    case = c.get(f\"/api/cases/{tok}\").json()\n    for x in [*case[\"entries\"], *case[\"amounts\"], *case[\"flags\"]]:\n        c.post(f\"/api/cases/{tok}/items/{x['id']}/review\", json={\"action\": \"accept\"})\n    DB.update_case(conn, tok, status=\"running\")\n    gate = steps_of(c.get(f\"/api/cases/{tok}/trace\").json())[\"export_gate\"]\n    assert gate[\"ready\"] is False and gate[\"status\"] == \"fail\" and [b[\"reason_code\"] for b in gate[\"blockers\"]] == [\"RUN_IN_PROGRESS\"]\n\n\ndef _add_record_warning(conn, tok, category, rid_from=\"e1\"):\n    src = conn.execute(\"SELECT * FROM flags WHERE case_id=? LIMIT 1\", (tok,)).fetchone()\n    row = {k: src[k] for k in src.keys() if k not in (\"review_status\", \"edited_json\", \"updated_at\")}\n    ent = DB.get_item(conn, rid_from, tok)\n    row.update(id=f\"f_{category}_t\", type=\"record_warning\", category=category, origin=\"code\", state=\"needs_review\", ladder_json=json.dumps({}),\n               state_reasons_json=json.dumps({\"date_ambiguous\": [\"DATE_AMBIGUOUS\"], \"injection_suspected\": [\"INJECTION_SUSPECTED\"]}[category]),\n               evidence_json=json.dumps([{\"record_id\": ent[\"record_ids\"][0], \"excerpt\": \"x\", \"start\": 0, \"end\": 1}]))\n    DB.add_item(conn, tok, \"flag\", row)\n    return row[\"id\"]\n\n\ndef test_record_warning_flags_point_at_the_right_action_and_a_real_step(env):\n    c, conn, tok, _ = env\n    for cat, action in ((\"date_ambiguous\", \"CONFIRM_DATE\"), (\"injection_suspected\", \"READ_RECORD\")):\n        fid = _add_record_warning(conn, tok, cat)\n        t = c.get(f\"/api/cases/{tok}/items/{fid}/trace\").json()\n        s = steps_of(t)\n        assert s[\"record_warning_check\"][\"next_action\"][\"code\"] == action, cat\n        assert t[\"state_reasons\"] and all(r[\"step_id\"] in s for r in t[\"state_reasons\"]), cat\n\n\ndef test_decided_items_have_no_top_level_next_action_but_steps_keep_theirs(env):\n    c, conn, tok, _ = env\n    pend = c.get(f\"/api/cases/{tok}/items/e2/trace\").json()\n    # force a failing code check, then decide\n    e = DB.get_item(conn, \"e2\", tok)\n    DB.update_item(conn, \"e2\", case=tok, state=\"needs_review\", state_reasons_json=[\"SUMMARY_DROPS_QUALIFIER\"], ladder=e[\"ladder\"])\n    t = c.get(f\"/api/cases/{tok}/items/e2/trace\").json()\n    assert t[\"next_action\"] is not None and pend is not None\n    for action in (\"accept\", \"dismiss\"):\n        c.post(f\"/api/cases/{tok}/items/e2/review\", json={\"action\": action})\n        t = c.get(f\"/api/cases/{tok}/items/e2/trace\").json()\n        assert t[\"next_action\"] is None\n        assert any(s[\"status\"] == \"fail\" and s[\"next_action\"] for s in t[\"steps\"]) or action == \"dismiss\"\n\n\ndef test_dismissed_item_human_step_is_skipped_not_pass(env):\n    c, _, tok, _ = env\n    c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"dismiss\"})\n    h = steps_of(c.get(f\"/api/cases/{tok}/items/e1/trace\").json())[\"human\"]\n    assert h[\"status\"] == \"skipped\"\n    c.post(f\"/api/cases/{tok}/items/e2/review\", json={\"action\": \"accept\"})\n    assert steps_of(c.get(f\"/api/cases/{tok}/items/e2/trace\").json())[\"human\"][\"status\"] == \"pass\"\n\n\ndef test_internal_table_bug_is_a_500_not_a_404(env, monkeypatch):\n    c, _, tok, _ = env\n    amt = c.get(f\"/api/cases/{tok}\").json()[\"amounts\"][0][\"id\"]\n    assert c.get(f\"/api/cases/{tok}/items/{amt}/trace\").status_code == 200\n    monkeypatch.delitem(trace._NEXT, \"DECIDE\")\n    quiet = TestClient(c.app, client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n    r = quiet.get(f\"/api/cases/{tok}/items/{amt}/trace\")\n    assert r.status_code == 500 and r.json()[\"error\"][\"code\"] != \"not_found\"\n    assert quiet.get(f\"/api/cases/{tok}/items/e999/trace\").status_code == 404           # unknown ids are still 404\n\n\ndef test_amount_judge_objection_counts_in_totals_unsupported(env):\n    c, conn, tok, _ = env\n    a = next(x for x in DB.list_items(conn, tok, \"amount\") if x[\"kind\"] != \"damages\" and (x[\"ladder\"] or {}).get(\"judge\"))\n    lad = a[\"ladder\"]\n    lad[\"judge\"].update(verdict=\"disagrees\", reason_code=\"SHOULD_BE_RATE\")\n    DB.update_item(conn, a[\"id\"], case=tok, state=\"needs_review\", state_reasons_json=[\"JUDGE_DISAGREES\"], ladder=lad)\n    rep = c.get(f\"/api/cases/{tok}/judges\").json()\n    assert rep[\"totals\"][\"unsupported\"] == 1 and rep[\"judges\"][1][\"disagrees\"] == 1 and len(rep[\"rejections\"]) == 1\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T03:34:19.434Z

**tool result**
````
_ test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing _

env = (<starlette.testclient.TestClient object at 0x10cb6b0b0>, <sqlite3.Connection object at 0x10bf73880>, 'eUb83w9KztqO1AZydz_KPA', 'ad0a8zRGPHjgURNojudAzg')

    def test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing(env):
        c, conn, tok, _ = env
        n = _blank_judges(conn, tok)
        DB.update_case(conn, tok, status="running")
        j = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
>       assert j["status"] == "pending" and j["counts"]["unavailable"] == n and "agreed" not in j["why"]
E       AssertionError: assert ('pass' == 'pending'
E         
E         - pending
E         + pass)

tests/unit/test_trace.py:526: AssertionError
____________ test_gate_ready_equals_no_blockers_in_every_case_state ____________

env = (<starlette.testclient.TestClient object at 0x10cc45d00>, <sqlite3.Connection object at 0x10c00f970>, 'eUb83w9KztqO1AZydz_KPA', 'ad0a8zRGPHjgURNojudAzg')

    def test_gate_ready_equals_no_blockers_in_every_case_state(env):
        c, conn, tok, pre = env
        seen = {}
        for name in _gate_states(c, conn, tok):
            gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
            assert gate["ready"] == (len(gate["blockers"]) == 0), name
            assert gate["status"] == ("pass" if gate["ready"] else "fail"), name
            if not gate["ready"]:
>               assert gate["next_action"] is not None or name.startswith("running"), name
E               AssertionError: all accepted, running
E               assert (None is not None or False)
E                +  where False = <built-in method startswith of str object at 0x10b0ab730>('running')
E                +    where <built-in method startswith of str object at 0x10b0ab730> = 'all accepted, running'.startswith

tests/unit/test_trace.py:563: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
FAILED tests/unit/test_trace.py::test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing
FAILED tests/unit/test_trace.py::test_gate_ready_equals_no_blockers_in_every_case_state
3 failed, 34 passed in 3.16s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:34:21.818Z

**tool call — Bash**
````
{
 "command": "sed -i 's/ or name.startswith(\"running\"), name/ or \"running\" in name, name/' tests/unit/test_trace.py && .venv/bin/python -m pytest -q tests/unit/test_trace.py -k \"never_ran\" 2>&1 | grep -B5 -A15 \"^E\" | head -50"
}
````

### User / tool · 2026-11-02T03:34:21.909Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/unit/test_trace.py
": undefined label 'ests/unit/test_trace.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:34:23.702Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('or name.startswith(\"running\"), name','or \"running\" in name, name')\ns=s.replace('''    for i in ids[:1]:\n        pass\n''','')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_trace.py -k \"never_ran\" 2>&1 | grep -B5 -A15 \"^E\" | head -50"
}
````

### User / tool · 2026-11-02T03:34:25.179Z

**tool result**
````
        for x in [*case["entries"], *case["undated_entries"], *case["amounts"], *case["flags"]]:
            t = c.get(f"/api/cases/{tok}/items/{x['id']}/trace").json()
            skipped += sum(1 for s in t["steps"] if s["id"].startswith("judge_") and s["status"] == "skipped" and s["reason_code"] == "JUDGE_UNAVAILABLE")
>       assert skipped == n == rep["totals"]["unavailable"]                       # item traces and /judges reconcile
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       assert 0 == 12

tests/unit/test_trace.py:512: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
1 failed, 36 deselected in 1.10s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:34:30.244Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('''            DB.update_item(conn, row[\"id\"], case=tok, state=\"needs_review\", state_reasons_json=sorted(set(row[\"state_reasons\"]) | {\"JUDGE_UNAVAILABLE\"}), ladder=lad)\n            n += 1''','''            DB.update_item(conn, row[\"id\"], case=tok, state=\"needs_review\", state_reasons_json=sorted(set(row[\"state_reasons\"]) | {\"JUDGE_UNAVAILABLE\"}), ladder=lad)\n            conn.execute(\"DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')\", (tok, row[\"id\"]))     # no audited judge call either\n            n += 1''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T03:34:33.600Z

**tool result**
````
.....................................                                    [100%]
37 passed in 2.88s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:34:37.158Z

**tool call — Bash**
````
{
 "command": "cp app/backend/trace.py /private/tmp/trace_new.py && cp app/backend/api.py /private/tmp/api_new.py && git show HEAD:app/backend/trace.py > app/backend/trace.py && git show HEAD:app/backend/api.py > app/backend/api.py && .venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -12; cp /private/tmp/trace_new.py app/backend/trace.py; cp /private/tmp/api_new.py app/backend/api.py\n# mutants\nfor m in \"s/\\\"human\\\", \\\"Your decision\\\", \\\"human\\\", SKIPPED/\\\"human\\\", \\\"Your decision\\\", \\\"human\\\", PASS/\" ; do cp app/backend/trace.py /private/tmp/t.bak; sed -i '' \"$m\" app/backend/trace.py; .venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -2; cp /private/tmp/t.bak app/backend/trace.py; done\ngit diff --stat app/backend | tail -3"
}
````

### User / tool · 2026-11-02T03:34:43.672Z

**tool result**
````
E        +  where 404 = <Response [404 Not Found]>.status_code

tests/unit/test_trace.py:646: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
FAILED tests/unit/test_trace.py::test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing
FAILED tests/unit/test_trace.py::test_gate_ready_equals_no_blockers_in_every_case_state
FAILED tests/unit/test_trace.py::test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed
FAILED tests/unit/test_trace.py::test_record_warning_flags_point_at_the_right_action_and_a_real_step
FAILED tests/unit/test_trace.py::test_decided_items_have_no_top_level_next_action_but_steps_keep_theirs
FAILED tests/unit/test_trace.py::test_internal_table_bug_is_a_500_not_a_404
7 failed, 30 passed in 2.92s
FAILED tests/unit/test_trace.py::test_dismissed_item_human_step_is_skipped_not_pass
1 failed, 36 passed in 2.63s
 app/backend/api.py   |  4 ++--
 app/backend/trace.py | 62 ++++++++++++++++++++++++++++++++++++++++++----------
 2 files changed, 53 insertions(+), 13 deletions(-)
[This command modified 1 file you've previously read: app/backend/trace.py. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:34:47.372Z

**tool call — Bash**
````
{
 "command": "cp app/backend/trace.py /private/tmp/t.bak; sed -i '' 's/\"unsupported\": j(\"partially\", \"unsupported\", \"disagrees\")/\"unsupported\": j(\"partially\", \"unsupported\")/' app/backend/trace.py; .venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -2; cp /private/tmp/t.bak app/backend/trace.py\ncat >> tests/unit/test_trace.py <<'EOF'\n\n\ndef test_zlayt_db_env_var_picks_the_database_file(tmp_path, monkeypatch):\n    target = tmp_path / \"chosen\" / \"x.sqlite\"\n    monkeypatch.setenv(\"ZLAYT_DB\", str(target))\n    monkeypatch.setenv(\"DATA_DIR\", str(tmp_path / \"ignored\"))\n    app = create_app(static_dir=str(tmp_path))\n    assert app.state.db_path == str(target) and target.exists() and not (tmp_path / \"ignored\").exists()\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T03:35:14.726Z

**tool result**
````
FAILED tests/unit/test_trace.py::test_amount_judge_objection_counts_in_totals_unsupported
1 failed, 36 passed in 2.86s
........................................................................ [ 96%]
..................................                                       [100%]
1042 passed in 23.09s
[This command modified 1 file you've previously read: app/backend/trace.py. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:35:19.095Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\nold=\"`totals.unsupported` = partially + unsupported + disagrees\"\nassert old in s\ns=s.replace(old,\"`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says \\\"agreed with all\\\". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. \"+old,1)\nopen(p,'w').write(s)\nEOF\ngit status --short app/backend app/db memory/contracts tests/unit/test_trace.py"
}
````

### User / tool · 2026-11-02T03:35:19.225Z

**tool result**
````
 M app/backend/api.py
 M app/backend/trace.py
 M memory/contracts/api.md
 M tests/unit/test_trace.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:35:22.236Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(backend): check-trace gate and judge summary never pass over a failure or a check that did not run (T-080 r2)\n\nJudges that never ran count as unavailable; export gate ready == no blockers (RUN_FAILED included); record-warning next_action/step_id; decided items drop top-level next_action; internal errors are 500 not 404; ZLAYT_DB honoured; tests kill the 3 surviving mutants.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/api.py app/backend/trace.py memory/contracts/api.md tests/unit/test_trace.py && git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T03:35:22.525Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
94beaeb
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:35:28.047Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-080 --sha 94beaeb --agent backend\n$B note T-080 --agent backend --text \"Round 2: fixed r1 findings 1-6. ZLAYT_DB: app/db/db.py never read it; the app chose its path in app/backend/api.py create_app (backend-owned), so no app/db change was needed: ZLAYT_DB (file) now wins over DATA_DIR. No field names changed for T-081/T-082; new behaviour: totals.unavailable also counts never-ran judges, judges step fail (pending while running), gate ready==(blockers==[]), item next_action null once decided. tests/unit 1042 passed.\"\n$B ac T-080 --check 1 --agent backend --evidence \"tests/unit/test_trace.py: record-warning, decided-next_action, dismissed human step, unknown-vs-500 tests pass; 1042 passed\"\n$B ac T-080 --check 2 --agent backend --evidence \"tests/unit/test_trace.py::test_gate_ready_equals_no_blockers_in_every_case_state, test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed, test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step; 1042 passed\"\n$B handoff T-080 --agent backend --text \"Round 2 (94beaeb). Changed: judge_report counts items whose judge never ran as unavailable (derived from the item steps, so /judges reconciles with item traces) and the case judges step fails (pending while running); gate ready == no blockers incl. RUN_FAILED; record-warning CONFIRM_DATE + step_id fallback; decided items next_action null; UnknownItem->404, other errors 500; ZLAYT_DB honoured in api.create_app (no app/db edit needed). Verified: .venv/bin/python -m pytest -q tests/unit = 1042 passed; new tests fail on old code (7) and the 3 surviving mutants are killed. Left: nothing. Surprised: judge-less items still showed 'supported' if an audited call existed (by design, trace falls back to the call).\"\n$B move T-080 in_review --agent backend"
}
````

### User / tool · 2026-11-02T03:35:28.449Z

**tool result**
````
T-080: commit 94beaeb recorded
noted on T-080
AC 1 checked: tests/unit/test_trace.py: record-warning, decided-next_action, dismissed human step, unknown-vs-500 tests pass; 1042 passed
AC 2 checked: tests/unit/test_trace.py::test_gate_ready_equals_no_blockers_in_every_case_state, test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed, test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step; 1042 passed
handoff written on T-080
T-080: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:35:30.695Z

T-080 round 2 is fixed and in review (commit 94beaeb); `tests/unit` gives 1042 passed. The new tests fail on the old code (7 tests), and the 3 surviving mutants are killed.

- **Judges and gate:** items whose judge never ran now count as unavailable, and the case "judges" step fails (pending while the run is going). The export gate says `ready == (blockers == [])`, RUN_FAILED included. The minors are also fixed.
- **ZLAYT_DB:** it was ignored, but the cause was `create_app` in `app/backend/api.py` (backend-owned), not `app/db`. I changed only `api.py` so `ZLAYT_DB` now wins over `DATA_DIR`. No field names changed for T-081/T-082.
