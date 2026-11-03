# T-084 r2 review: guarded charge reclassification (D-042) (staff-engineer-reviewer, round 2)

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (T-084 r2, committed with the T-073 r2 changes), with e2b4e3f (billing restored) underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both "restore ... reverted by 2fca530"). The verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad. The working tree has uncommitted edits to reclassify.py (it now imports `amounts.RATE_CUE`), amounts.py, billing.py and audited.py. Those are not reviewed here.

## Summary

The three r1 invariants hold on HEAD for the paths the tests and probes reach, with two gaps. (1) A restore re-runs both checks when the sentence changes and when the code's class changes (reclassify.py:145-153), and the code is right for both. Only the sentence arm has a test, so a class-only change has no test that would catch its removal (F1). (2) The code wording gate refuses "Charge per visit $185." and "Billed $150 per visit." before the judge, as the brief asks, and it refuses 17 rate-cue sentences. It still passes six unit-price phrasings that the amount classifier calls a rate or a unit price, so for those the judge is the only gate (F2).

One r1 blocker is closed, but not by this card. c8a9874 alone does not work: its own test file fails 9 of 120 tests, and a reclassify request returns 500 after it has already changed the item and written no audit row. HEAD a850be0 is correct because 6feb2ff restored the T-095 schema that 2fca530 had reverted. The card's commit list does not name 6feb2ff.

Billing is back in HEAD and identical to f218263. The worker's extra behaviour (a promoted charge falls back to the code's class when a rerun changes its sentence) goes the safe direction, but it drops the paralegal's decision without any visible note (F4).

Verdict: changes (0 blockers, 2 majors) on HEAD a850be0.

## Exercised (what I actually ran or read)

- `python3 tools/board.py show T-084`, `show T-094`, `show T-095` (the 031a708 card; header only).
- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44, then a850be0). `git show --stat c8a9874`, `e2b4e3f`, `6feb2ff`, `a850be0`.
- `git show c8a9874:app/db/schema.sql | grep -c "'reclassify'"` = 0; `git show a850be0:app/db/schema.sql` line 57 contains 'reclassify' and 'rejudge'.
- `git diff --stat bc12d44 a850be0 -- <in-scope>`: only app/db/db.py and app/db/schema.sql changed. `git diff --stat f218263 a850be0 -- app/backend/billing.py tests/unit/test_billing.py`: empty. `git ls-tree -r --name-only a850be0 | grep -i billing`: both files. `git show a850be0:app/backend/api.py`: line 510 `billing.add_routes(...)`, line 512 `reclassify.add_routes(...)`.
- `git blame -L 496,502 a850be0 -- app/backend/pipeline.py`: lines 500-501 from 865b1865 (T-085).
- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed. The 9 failures are test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited, test_undoing_her_own_demotion_restores_the_code_class_without_a_judge, test_figure_with_charge_wording_and_judge_agreement_becomes_a_pending_verified_charge, test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again, test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again, test_restore_after_an_unchanged_rerun_still_needs_no_judge, test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence, test_a_rerun_keeps_her_reclassification, test_route (the last with "assert (500 == 200)" and IntegrityError at reclassify.py:90).
- `.venv/bin/python -m pytest -q tests/unit/test_audited.py` at a850be0: 19 passed. `.venv/bin/python -m pytest -q tests/unit/test_billing.py` at a850be0: 27 passed.
- `.venv/bin/python -m pytest -q tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. The 7 are tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s, test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2, and four in test_trace.py (test_every_item_has_an_ordered_well_formed_trace, test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them, test_every_emitted_reason_code_has_a_fixed_sentence, test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step). The handoff's "1417 pass" was measured on the working tree.
- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` run in the a850be0 archive: traceback ends `UnboundLocalError: cannot access local variable 'raw' where it is not associated with a value` at pipeline.py:501. Exit status non-zero.
- Read in full at a850be0: app/backend/reclassify.py (unchanged since bc12d44) and tests/unit/test_reclassify.py (unchanged since bc12d44), plus app/backend/judge_guard.py and app/llm/audited.py for the T-073 side. db.py:54 (autocommit), :215 (apply_review), :227 and :287 (BEGIN). amounts.py:14 (`_UNIT`).
- Probes, all in `artifacts/review-evidence/T-073-T-084-r2/`, each run with `.venv/bin/python -I <probe> <archive root>`:
  - `probe_reclassify_audit_route.py` on c8a9874 and a850be0 (output in the transcript; c8a9874: HTTP 500, stored kind changed charge to unclear, `review_events for a1: []`; a850be0: HTTP 200, `[('reclassify', 'reclassify')]`).
  - `probe_rate_cue_gaps.py` on a850be0, output `rate-cue-gaps-run.txt`.
  - `probe_classifier_vs_wording_gate.py` on a850be0, output `classifier-vs-gate-run.txt`.
  - `probe_restore_class_only_flip.py` on a850be0 and on mutant m03, output `restore-class-only-flip-run.txt`.
- Scratch mutants via `mutate_r2.py` (applied to copies, never to the project; log `mutation-run-r2.txt`). Control: 139 passed. Results: T84-1 (rate cue removed from the wording gate) 21 failed; T84-2 ('per' removed from the rate-cue pattern) 11 failed; T84-3 (restore ignores the code class) 139 passed; T84-4 (restore ignores whether the sentence changed) 1 failed; T84-5 (restore always skips the checks, the r1 bug) 2 failed; T84-6 (promoted charge kept when its sentence changes) 1 failed. T73-1 to T73-4: see the T-073 r2 review.
- `grep` on the judge call sites (`judge_guard.guarded` only at review.py:102 and reclassify.py:167).

## Findings

### F1 (major): restore after a class-only change is not tested; mutant survives

- The code is right: `_may_restore` (reclassify.py:145-153) requires `rerun.code_class == "charge"` and an unchanged sentence sha. Probe `probe_restore_class_only_flip.py` on a850be0 (the rerun changes only the code's class of $310; the excerpt text is identical): `4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE`, `5. stored kind = unclear | reclassify events before/after = 1 1`, `pending total cents = 0`.
- The gap is the test. Mutant T84-3 (reclassify.py:153 reduced to `return rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])`) passes all 139 tests. The same probe on that mutant: `4. restore with no judge: HTTP 200 restored=True kind=charge`, `pending total cents = 31000`.
- The tests exercise the sentence arm only: test_reclassify.py:190 `RATE_R3` changes the sentence and the class together, and test_reclassify.py:198-216 uses it. test_reclassify.py:219-230 changes the sentence, not the class.
- Why it matters: the brief asks that a restore re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without the test, a later edit to `_may_restore` could reopen the r1 blocker and no test would fail.
- Fix: add a test that patches `amounts.classify` so the rerun's code class of $310 is "rate" while the excerpt stays identical. Then `reclassify(..., {"to": "charge"}, call=None)` must raise 422 JUDGE_UNAVAILABLE with the item still `unclear`. Add the case with `call=FakeCall(J2("agree"))`: the judge is called once and `restored` is False. Keep test_reclassify.py:233-240 (unchanged rerun, no judge) passing.
- Acceptance test: mutant T84-3 fails the new test.

### F2 (major): the code wording gate passes unit-price phrasings that the amount classifier calls rates

- Probe `probe_classifier_vs_wording_gate.py` (a850be0, output `classifier-vs-gate-run.txt`): "Charged $150 an hour." is `rate` by amounts.classify and passes charge_wording (`passes (Charged)`); "Charged $75 a unit." is `rate` and passes; "Billed $120 an appointment." is `rate` and passes. The unit vocabulary is amounts.py:14 `_UNIT = ... hour|hr|day|unit|appointment|procedure|adjustment`, while the gate's rate-cue pattern is reclassify.py:31-33, which has no hour, unit or appointment.
- Probe `probe_rate_cue_gaps.py` (output `rate-cue-gaps-run.txt`): "Billed $150 hourly.", "Charged $90 apiece.", "Billed $40 daily." and "Billed $200 a month." also pass the code gate. The two named strings are refused (`None (refused)`), so F2 is not about the brief's named cases.
- Why it matters: D-042 as written is met, because the sentence has charged wording and the judge re-checks it. But the code gate and the classifier disagree about the same sentence. For these phrasings the judge is the only gate before a figure goes to pending, and the paralegal can then accept it into the total. This is the first independent gate the card depends on. The r1 fix list named "per unit" and "a visit", and the gate covers those only partly.
- Fix: one rate-unit test shared by amounts.classify and reclassify.charge_wording. The uncommitted working tree already moves toward `amounts.RATE_CUE` (not reviewed). Whatever form lands, refuse the six phrasings before the judge.
- Acceptance test: `charge_wording` returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for "Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.". A parametrized test asserts that for every fixture sentence, `amounts.classify == "rate"` implies `charge_wording is None`.

### F3 (minor): the state change and its audit row are separate autocommit writes; the consequence is now observed

- reclassify.py:135 `DB.update_item(...)` commits on its own (db.py:54 `isolation_level=None`, autocommit). reclassify.py:137 `review.batch_apply` (for a non-pending item) and reclassify.py:138 `_log` follow as separate statements.
- Observed on c8a9874 (`probe_reclassify_audit_route.py`): `POST reclassify a1 -> HTTP 500`, `a1 stored after request: kind=unclear`, `review_events for a1 (action, payload event): []`. The paralegal sees an error, the item has changed, and there is no audit row.
- The brief allows this as a minor. The fix is the one from r1: wrap update_item, batch_apply and _log in one transaction with rollback on error, as db.py:227 and :287 do for apply_review.
- Acceptance test: monkeypatch `RC._log` to raise; assert the item's kind is still `charge` after the call.

### F4 (minor): a promoted charge is dropped silently when its sentence changes

- reclassify.py:188-189 `if rc.get("to") == "charge" and rc.get("excerpt_sha") != _sha(it.get("excerpt")): return it`. The reclassification record is discarded and the figure returns to the code's class. The same figure becomes `rate`, which is the safe direction (it leaves the total).
- But the response to the rerun carries no note that her promotion was withdrawn. test_reclassify.py:249-250 asserts only `kind != "charge"`. The audit row stays (review_events), but the item view does not say why the figure changed.
- Fix: keep the record with `dropped: "SENTENCE_CHANGED"` in `ladder.reclassification` and show it in the item view and the stepper.
- Acceptance test: after a sentence change, `item.ladder.reclassification.dropped == "SENTENCE_CHANGED"` and the item view names the reason.

## Closed at HEAD (not findings at a850be0)

- c8a9874 on its own tree (blocker at c8a9874, closed at HEAD). Schema: `git show c8a9874:app/db/schema.sql | grep -c "'reclassify'"` = 0, and reclassify.py:27 sets `AUDIT_ACTION = "reclassify"`. The reclassify INSERT fails with IntegrityError (reclassify.py:90), the route returns 500, and the item is already changed (F3 evidence). 2fca530 (T-087/T-086, a sibling commit) reverted the T-095 CHECK and migration. 6feb2ff ("fix: restore T-095 work reverted by 2fca530") restores them. At a850be0 the CHECK is at schema.sql:57, SCHEMA_VERSION is 4 (db.py:33), the four files pass 120 of 120, and the probe returns 200 with a `reclassify` row. The card should cite 6feb2ff, since c8a9874 alone does not pass.
- r1 F4 (audit action 'edit'): closed. AUDIT_ACTION is "reclassify" (reclassify.py:27) and test_route:319 asserts `["reclassify"]`, which passes at HEAD.
- r1 F2 (billing removed by ec33bf0): closed. billing.py and test_billing.py are identical to f218263 at a850be0; api.py:510 registers the billing routes. test_billing.py: 27 passed.
- r1 F1 (restore after a rerun), sentence arm: closed. Mutant T84-4 fails 1 test, mutant T84-5 (the r1 bug) fails 2, mutant T84-6 fails 1. Class arm: code correct (probe), test missing (F1 above).
- r1 F3 (rate phrase passes the wording gate), named strings: closed. "Charge per visit $185." and "Billed $150 per visit." are refused before the judge (test_reclassify.py:161-171, `call.log == []`). Mutant T84-1 fails 21 tests and mutant T84-2 fails 11. The remaining gap is F2.

## Judgement on the worker's extra behaviour

- A promoted charge falls back to the code's class when a rerun changes its sentence (reclassify.py:188-189). I judge this right: it fails closed, and it is the same rule as the restore path (any sentence change means the earlier judge answer no longer applies). The silent drop is F4.

## What is right

- reclassify.py:145-153 (`_may_restore`) requires a charge original, a previous judge, and, after any rerun, the same sentence sha and a charge code class. The probe confirms the refusal (422 JUDGE_UNAVAILABLE, total 0).
- The refusals stay before the judge: test_reclassify.py:170 asserts `call.log == []` and the item stays `rate`, `needs_review`.
- Billing is back in HEAD: identical to f218263, registered at api.py:510, 27 tests pass.

## Outside these cards (observed at a850be0, not attributed to T-073 or T-084)

- The sample CLI crashes. `.venv/bin/python -m app.pipeline evals/golden/sample.txt` ends in UnboundLocalError at pipeline.py:501 (`raw` is referenced before assignment). `git blame` puts lines 500-501 in 865b1865 (T-085). This is persona checklist item 20 and it fails on HEAD.
- Seven unit tests fail at a850be0 (listed in Exercised). I did not trace them to a cause. None is in the T-073 or T-084 files.

## Scores

```
no_rate_into_total_without_both_checks 3 (both checks run on every path; the class-only restore is untested, F1; the code gate passes six classifier-rate phrasings, F2)
restore_rule_tested 3 (sentence arm killed; class arm not, F1)
code_check_strength 2 (named strings and 17 cues refused; six classifier-rate phrasings pass, F2)
judge_gate 4 (judge disagree, unsure and unavailable give 422 with nothing changed)
audit_trail 3 (written at HEAD; the item change and the audit row are not one transaction, F3; the promoted drop is not shown, F4)
commit_integrity 2 (c8a9874 alone fails 9 tests and 500s with the item changed; closed at HEAD by 6feb2ff, which is not in this card's commit list)
billing_restored 5 (identical to f218263; route registered; 27 tests pass)
tests_kill_mutants 4 (T84-1, T84-2, T84-4, T84-5, T84-6 and all four T-073 mutants killed; T84-3 survives)
```

## Questions for Chris

- D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should "Charged $150 an hour.", "Charged $75 a unit." and "Billed $120 an appointment." be refused by the code gate, even though they say "charged" or "billed" and the judge would then have to say so? My reading is that they should be refused, because the amount classifier calls them rates. The decision text does not say.
