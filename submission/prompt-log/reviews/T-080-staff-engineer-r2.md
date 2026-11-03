# T-080 round-2 review: check-trace API (staff-engineer-reviewer)

Scope: commit 94beaeb (HEAD), `app/backend/trace.py`, `app/backend/api.py`, `memory/contracts/api.md`, `tests/unit/test_trace.py`. Checked against my round-1 review `reviews/T-080-staff-engineer.md` (e3cea6f).

Verdict: **changes** (0 blockers, 1 major, 1 minor, 2 nits).

Round-1 items are fixed as claimed: judges that never ran count as unavailable and the case `judges` step fails; the export gate holds `ready == (no blockers)` including `RUN_FAILED`; the record-warning, stale `next_action`, and 404-masking minors are fixed; `ZLAYT_DB` is honoured; the three round-1 surviving mutants are now killed. The one new major is that the gate and the export still pass over accepted items whose judge never ran, and the export says nothing about it.

## Checks requested

- **Judge never ran counts as unavailable, judges step never passes while any are unavailable: met.** Live on the review instance, 12 items whose judge never ran gave `/judges` `unavailable: 12`, `unresolved: 12` (all `JUDGE_UNAVAILABLE`), and the case `judges` step `fail`, reason `JUDGE_UNAVAILABLE`, next `COMPARE_BY_HAND`. The item-level skipped judge steps summed to 12. The PASS branch in `case_trace` is reached only when `t["unavailable"] == 0` (trace.py:809-822).
- **Export gate `ready == (len(blockers) == 0)` with RUN_FAILED: met.** Live: status `failed` gave `verdict failed`, gate `fail`, `ready False`, blockers `['RUN_FAILED']`, next `CONFIRM_RERUN`. Status `running` gave `RUN_IN_PROGRESS`, `ready False`. All accepted and status `ready` gave `ready True`, blockers `[]`. The invariant holds by construction (trace.py:872-874) and is asserted by `test_gate_ready_equals_no_blockers_in_every_case_state`.
- **Minors fixed:** record-warning `CONFIRM_DATE` and `step_id` (trace.py:456, 441-ff `fallback`), decided items have top-level `next_action` null (trace.py:253-254; live `a1` accepted gives `None`), `UnknownItem` gives 404 only for unknown ids (api.py:507-508; live `e999`, `x1`, `zz` give 404; an internal `KeyError` gives 500 in the unit test), the three survivors (dismissed human step, gate with running case, `disagrees` in totals) are killed (mutants S1, G4, S2 below).
- **ZLAYT_DB honoured: met.** Instance started with `ZLAYT_DB` pointing at the scratchpad file and `DATA_DIR` pointing at an empty sentinel directory. The scratch DB was created (94208 bytes) and the sentinel stayed empty. `data/zlayt.sqlite` sha256 was `6d7dcf828093a1c07d3671046cf1c0c2e990b536c2e03289946a95f9eacc0593` with mtime `1793590231` before and after all probes.
- **Mutating the gate invariant fails a test: met.** G1 to G4 each fail 2 or 3 tests (below).

## Findings

### 1. major: the export gate passes, and the export is silent, over accepted items whose judge never ran

Repro on the review instance (scratch DB, fixture `curated`): run the sample, accept all 23 live items, then blank the judge record of the 12 judged items that are not charges-with-damages (the unit-test helper `_blank_judges`, applied to the scratch DB only). Then:

```
GET /api/cases/<tok>/judges   -> totals {'items_judged': 7, 'unavailable': 12}, unresolved 12 x JUDGE_UNAVAILABLE
GET /api/cases/<tok>/trace    -> judges: fail JUDGE_UNAVAILABLE "12 items have not been double-checked."
                                 export_gate: pass, ready True, blockers [], verdict {'code': 'ready'}
GET /api/cases/<tok>/export   -> warnings [], internal_notes_text: "...every item in the treatment section was accepted by the paralegal. Items not reviewed: 0."
                                 no mention of the second check; letter_text contains the 9 entries and 2 charges
```

Code path: the gate's blockers (trace.py:856-870) read only live pending items, run state, and `NOTHING_ACCEPTED`; the judges step (trace.py:809-822) does not feed them. The export (`app/backend/` export builder) has no field for items that were accepted without a judge.

Why it matters: the commit title says the gate "never pass[es] over a failure or a check that did not run", and here it does. The letter and the internal notes go out with 12 items whose second check never ran, and nothing in the artifact the paralegal sends says so. Spec: `docs/LLM_VS_CODE.md:7` and `docs/CONTRACT.md:61` say nothing the model wrote reaches the export without all three rungs. R-RV-3 (`spec/REQUIREMENTS.md:94`) does let a human save an edit with `JUDGE_UNAVAILABLE` as `needs_review`, so the human accept path is in the spec. That makes this a policy gap that needs Chris's decision, not a clear spec violation, so I rate it major and not blocker.

Fix (pick one and record it in `memory/DECISIONS.md`): (a) add a gate blocker `JUDGE_UNAVAILABLE` for each accepted item whose judge did not run, cleared only by an explicit "accept without second check" event; or (b) list each such item under "Not double-checked by the second AI check (judge unavailable)" in `internal_notes_text` and set the case verdict to needs attention, not ready, while the judges step is `fail`. Either way `ready` must still equal `(blockers == [])`.

Acceptance test: run the sample, blank the judges as in `_blank_judges`, accept all; assert the export's `internal_notes_text` names each of the 12 items, the case verdict is not `ready` (or the blocker exists), the judges step is `fail`, and `gate.ready == (gate.blockers == [])`.

### 2. minor: rejected amount and flag traces are still untested (round-1 survivor list)

`tests/unit/test_trace.py` has no assertion on a rejected amount or a rejected flag trace. The only mention of `rejected` in the new tests is the skip in `_blank_judges` (line 490). The round-1 finding named this branch explicitly, and it is still uncovered. Fix: add a test with one rejected amount and one rejected flag asserting that the human step is `pending` with `DISMISS_OR_ENTER_BY_HAND`, and that neither blocks the gate (`rejected_not_blocking` counts them). Acceptance: a mutant that treats rejected items as live pending (trace.py:862 without `x["state"] != "rejected"`) fails a test.

### 3. nit: the gate's `ITEMS_PENDING` fallback is unreachable (trace.py:873-874)

`review_view.ready_to_export` (`app/backend/present.py:122`) is false only when a live item is pending, which already adds a `PENDING_DECISION` blocker, or when nothing is accepted, which already adds `NOTHING_ACCEPTED`. So `if not ready and not blockers` never runs. It is harmless. Delete it or assert it is dead, so the next reader does not think it is a real path.

### 4. nit: round-1 wording and mapping items are unchanged, and one test assertion is trivially true

Unchanged from round 1, optional: `trace.py:420` says a rejected charge is "Not a billed charge, so it is not added to the total"; `trace.py:558` says a sentence that failed `NOT_AN_ACCEPTED_ENTRY` "named the one accepted entry"; `trace.py:162` `_norm_verdict(step_id, v)` ignores `step_id` and re-implements `judges._TO_LADDER`. In `tests/unit/test_trace.py:622`, `pend is not None` is always true (it is a dict fetched on the line above), so it asserts nothing; the `next_action is not None` part is the real check.

## Mutation run (scratch copy, not committed)

Copied `app`, `tests`, `evals`, `docs`, `spec`, `memory` to the scratchpad and applied one string mutant per run to `tests/unit/test_trace.py`. Baseline in the copy: 38 passed.

| Mutant | Result |
|---|---|
| G1 gate ignores failed run (round-1 bug, `and not cx.running`) | killed, 2 failed |
| G2 `ready` ignores blockers | killed, 3 failed |
| G3 no `RUN_FAILED` blocker | killed, 2 failed |
| G4 no `RUN_IN_PROGRESS` blocker (round-1 survivor M5) | killed, 3 failed |
| J1 judge-never-ran not counted | killed, 2 failed |
| J2 judges step never FAILs on unavailable | killed, 3 failed |
| J3 running judges step PASS instead of PENDING | killed, 1 failed |
| J4 `totals.unavailable` not summed | killed, 3 failed |
| E1 `ZLAYT_DB` ignored | killed, 1 failed |
| E2 any KeyError maps to 404 | killed, 1 failed |
| E3 unknown item raises bare KeyError | killed, 2 failed |
| N1 decided item keeps top-level `next_action` | killed, 1 failed |
| R1 date_ambiguous uses READ_RECORD | killed, 1 failed |
| R2 record-warning reason has no mapped step, no fallback | killed, 1 failed |
| S1 dismissed human step PASS (round-1 survivor M3) | killed, 1 failed |
| S2 `totals.unsupported` drops `disagrees` (round-1 survivor M19) | killed, 1 failed |

First draft of R2 changed an unrelated mapping (`DATE_MISSING`) and survived; that was an equivalent mutant, so I replaced it with the one above.

## Checked and fine

- Judges unavailable never reach `items_judged`; `unresolved` lists each with `JUDGE_UNAVAILABLE`.
- Gate blockers and verdict are consistent across pending, running, failed and all-accepted states, live and in tests.
- Responses for the same item are stable across GETs in the live run.
- `trace.py`: no `float(`, no bare `except`, no `sleep(`, no network call. The three `except` clauses are `KeyError` and `ValueError/TypeError` on narrow lookups. The new tests contain no float, sleep or network use. `time.sleep(0.25)` in the module fixture is the round-1 bounded poll (`range(240)`), unchanged.

## Exercised

- `personas/staff-engineer.md`, `reviews/T-080-staff-engineer.md`, `git show 94beaeb` (stat, api/trace/contract/test diffs).
- `.venv/bin/python -m pytest -q tests/unit/test_trace.py -p no:cacheprovider` gave 38 passed (2.82s); the same in the scratch copy gave 38 passed.
- Live instance on 127.0.0.1:7993 with `ZLAYT_DB=<scratchpad>/r2_t080_app.sqlite`, `DATA_DIR=<scratchpad>/r2_sentinel_data`, `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`. Sample run (202, ready); judges 19 judged / 0 unavailable; accept all 23 items; gate ready true; blanked judges in the scratch DB only (`r2_blank_judges.py`); `/judges`, `/trace`, item traces for all 23 ids; `/export`; set status `failed` and `running` in the scratch DB (`r2_set_status.py`); 404s for `e999`, `x1`, `zz`. Server stopped (pid 39888, port 7993 free).
- Checksums and mtime of `data/zlayt.sqlite` before and after: unchanged.
- Mutation runner `r2_mutants.py` and `r2_mutant_r2b.py` in the scratchpad (outside the project).
- Greps: `float(|except|sleep(|requests|httpx|anthropic` in `app/backend/trace.py` and the new test lines.

```json
{"card": "T-080", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 94beaeb (HEAD): app/backend/trace.py, app/backend/api.py, memory/contracts/api.md, tests/unit/test_trace.py; local instance 127.0.0.1:7993 with ZLAYT_DB and DATA_DIR in scratchpad, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local; sample case; round-1 review reviews/T-080-staff-engineer.md",
 "exercised": [
  "git show 94beaeb (stat and api/trace/contract/test diffs)",
  ".venv/bin/python -m pytest -q tests/unit/test_trace.py -p no:cacheprovider -> 38 passed",
  "live sample run on 127.0.0.1:7993 (ZLAYT_DB scratch file, DATA_DIR empty sentinel): judges 19 judged, 0 unavailable; accept all 23 items; gate ready true",
  "scratch-DB probe: blanked 12 judge records; /judges unavailable 12 = item-level skipped judge steps 12; judges step fail; gate pass; /export internal notes silent",
  "scratch-DB probe: case status failed -> gate ready False, RUN_FAILED; status running -> RUN_IN_PROGRESS; ready == (no blockers) in each",
  "404 for unknown item ids e999, x1, zz on the live server",
  "data/zlayt.sqlite sha256 6d7dcf82...0593 and mtime 1793590231 unchanged before and after all probes; sentinel DATA_DIR stayed empty",
  "16 string mutants in a scratch copy (gate, judges, ZLAYT_DB, 404 narrowing, first_na, record-warning action and step_id, dismissed human step, totals disagrees): 16 killed; first R2 draft was equivalent and replaced",
  "grep float(, except, sleep(, network in trace.py and the new test lines"],
 "verdict": "changes",
 "scores": {"gate_ready_equals_blockers": 5, "judge_never_ran_reconciliation": 4, "export_honesty_when_judge_unavailable": 2, "round1_minor_fixes": 4, "zlayt_db_honoured": 5, "test_strength_mutants": 4, "no_llm_or_float_in_deterministic_paths": 5, "contract_match": 4},
 "findings": [
  {"severity": "major", "title": "Export gate passes and the export is silent over accepted items whose judge never ran",
   "evidence": "Live scratch-DB probe: /judges totals unavailable 12 with 12 unresolved JUDGE_UNAVAILABLE; /trace judges step fail JUDGE_UNAVAILABLE '12 items have not been double-checked.'; export_gate pass ready True blockers []; verdict ready. /export: warnings [], internal_notes_text 'every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.' with no mention of the second check. Gate blockers at app/backend/trace.py:856-870 read only live pending, run state and NOTHING_ACCEPTED; judges step at trace.py:809-822 does not feed them.",
   "why_it_matters": "The commit title says the gate never passes over a check that did not run; here it passes over 12 unrun judge checks, and the letter and internal notes the paralegal sends carry no sign of it. docs/LLM_VS_CODE.md:7 and docs/CONTRACT.md:61 say nothing the model wrote reaches the export without all three rungs. R-RV-3 (spec/REQUIREMENTS.md:94) lets a human save a JUDGE_UNAVAILABLE edit as needs_review, so accepting is in the spec; the gap is the gate and the disclosure, which needs Chris's decision, so major and not blocker.",
   "fix": "Record one policy in memory/DECISIONS.md. Either (a) a gate blocker JUDGE_UNAVAILABLE for each accepted item whose judge did not run, cleared only by an explicit accept-without-second-check event; or (b) list those items under 'Not double-checked by the second AI check (judge unavailable)' in internal_notes_text and set the verdict to needs attention while the judges step is fail. Either way ready must equal (blockers == []).",
   "acceptance_test": "Run the sample, blank the judge records as in tests/unit/test_trace.py _blank_judges, accept all; assert the export internal_notes_text names each of the 12 items, the case verdict is not ready (or the blocker is present), the judges step is fail, and gate.ready == (gate.blockers == [])."},
  {"severity": "minor", "title": "Rejected amount and flag traces are still untested (round-1 survivor list)",
   "evidence": "tests/unit/test_trace.py: the only 'rejected' in the new tests is the skip at line 490 (_blank_judges). No assertion on a rejected amount or flag trace. Round-1 finding 6 named this branch.",
   "why_it_matters": "A rejected item is the path where the paralegal is told to dismiss or enter by hand; a regression there stays green.",
   "fix": "Add a test with one rejected amount and one rejected flag: human step pending with DISMISS_OR_ENTER_BY_HAND, and neither blocks the gate (rejected_not_blocking counts them).",
   "acceptance_test": "A mutant that counts rejected items as live pending (app/backend/trace.py:862 without the state != 'rejected' filter) makes a test fail."},
  {"severity": "nit", "title": "Gate ITEMS_PENDING fallback is unreachable",
   "evidence": "app/backend/trace.py:873-874 'if not ready and not blockers'. review_view ready_to_export (app/backend/present.py:122) is false only when a live item is pending (already a PENDING_DECISION blocker) or nothing is accepted (already NOTHING_ACCEPTED).",
   "why_it_matters": "Dead code reads as a real path and invites a wrong test later.",
   "fix": "Delete the branch, or comment that it is defensive and unreachable.",
   "acceptance_test": "None needed; the invariant test already covers the gate."},
  {"severity": "nit", "title": "Round-1 wording and mapping items unchanged; one trivially true assertion",
   "evidence": "app/backend/trace.py:420 'Not a billed charge, so it is not added to the total.' applies to rejected charges; trace.py:558 'named the one accepted entry' for a sentence that failed NOT_AN_ACCEPTED_ENTRY; trace.py:162 _norm_verdict ignores step_id and re-implements judges._TO_LADDER. tests/unit/test_trace.py:622 'pend is not None' is always true.",
   "why_it_matters": "Plain-words errors on the explanation screen, and a duplicated verdict map that can drift from judges.py.",
   "fix": "Use a rejection-specific sentence for total_inclusion on rejected charges; soften the sentence wording for unaccepted citations; call judges.to_ladder with the right step; drop the pend assertion.",
   "acceptance_test": "Rejected charge total_inclusion.why mentions rejection; _norm_verdict removed in favour of judges.to_ladder with a test over every raw verdict."}
 ],
 "whats_right": [
  "The gate invariant is enforced by construction (trace.py:872-874), and four gate mutants (G1 to G4) each fail 2 or 3 tests; a live failed run shows RUN_FAILED with ready False.",
  "ZLAYT_DB is honoured: the scratch file was created, the sentinel DATA_DIR stayed empty, and data/zlayt.sqlite kept the same sha256 and mtime.",
  "Judge counts reconcile with the item traces (12 = 12 live), the judges step never passes while any are unavailable, and the 404 narrowing returns 500 for internal errors (E2, E3 killed)."
 ],
 "questions_for_chris": ["For an accepted item whose judge never ran: should the export block until the paralegal records 'accept without second check', or should the export disclose the item in its internal notes and keep the case verdict at needs attention? R-RV-3 allows saving the edit with JUDGE_UNAVAILABLE, but not whether that item should appear in the letter without a note."]}
```
