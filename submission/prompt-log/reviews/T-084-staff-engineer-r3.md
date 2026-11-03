# T-084 r2 review, filed as r3 (staff-engineer-reviewer, round 2)

This file supersedes `reviews/T-084-staff-engineer-r2.md`. That file was written without its ```json block, so the board validator rejects it, and the append-only guard refuses an in-place edit. Use this file for the T-084 round-2 verdict; do not register the r2 file.

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (T-084 r2, committed with the T-073 r2 changes), with e2b4e3f (billing restored) underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both "restore ... reverted by 2fca530"). The verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad. The working tree has uncommitted edits to reclassify.py (it now imports `amounts.RATE_CUE`), amounts.py, billing.py and audited.py. Those are not reviewed here.

## Summary

The three r1 invariants hold on HEAD for the paths the tests and probes reach, with two gaps. (1) A restore re-runs both checks when the sentence changes and when the code's class changes (reclassify.py:145-153), and the code is right for both. Only the sentence arm has a test, so a class-only change has no test that would catch the removal of its check (F1). (2) The code wording gate refuses "Charge per visit $185." and "Billed $150 per visit." before the judge, as the brief asks, and 17 rate-cue sentences. It still passes six unit-price phrasings that the amount classifier calls a rate or a unit price, so for those the judge is the only gate (F2).

One r1 blocker is closed, but not by this card. c8a9874 alone does not work: its own test file fails 9 of 120 tests, and a reclassify request returns 500 after it has already changed the item and written no audit row. HEAD a850be0 is correct because 6feb2ff restored the T-095 schema that 2fca530 had reverted. The card's commit list does not name 6feb2ff.

Billing is back in HEAD and identical to f218263. The worker's extra behaviour (a promoted charge falls back to the code's class when a rerun changes its sentence) goes the safe direction, but it drops the paralegal's decision without a visible note (F4).

Verdict: changes (0 blockers, 2 majors) on HEAD a850be0.

## Exercised (what I actually ran or read)

- `python3 tools/board.py show T-084`, `show T-094`, `show T-095` (header).
- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44, then a850be0); `git show --stat` for c8a9874, e2b4e3f, 6feb2ff, a850be0.
- `git show c8a9874:app/db/schema.sql | grep -c "'reclassify'"` = 0; a850be0 schema.sql:57 has 'reclassify' and 'rejudge'.
- `git diff --stat bc12d44 a850be0` over the in-scope files: only app/db/db.py and app/db/schema.sql. `git diff --stat f218263 a850be0 -- app/backend/billing.py tests/unit/test_billing.py`: empty. `git ls-tree -r --name-only a850be0 | grep -i billing`: both files. a850be0 api.py lines 510 (billing) and 512 (reclassify).
- `git blame -L 496,502 a850be0 -- app/backend/pipeline.py`: lines 500-501 from 865b1865 (T-085).
- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed. The 9 failures are all in test_reclassify.py, with `IntegrityError` at reclassify.py:90 and `assert (500 == 200)` in test_route.
- `.venv/bin/python -m pytest -q tests/unit/test_audited.py` at a850be0: 19 passed. `tests/unit/test_billing.py`: 27 passed.
- `.venv/bin/python -m pytest -q tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. The 7 are test_e2e_contract::test_every_test_id_is_declared, test_t037_backend::test_cli_sample_on_fixture_backend_under_60s, test_t075_determinism::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2, and four in test_trace.py. The handoff's "1417 pass" was measured on the working tree.
- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` in the a850be0 archive: `UnboundLocalError: cannot access local variable 'raw'` at pipeline.py:501.
- Read in full at a850be0: app/backend/reclassify.py and tests/unit/test_reclassify.py (both unchanged since bc12d44), app/backend/judge_guard.py, app/llm/audited.py. Also db.py:54 (autocommit), :215, :227, :287 (BEGIN); amounts.py:14 (`_UNIT`).
- Probes in `artifacts/review-evidence/T-073-T-084-r2/`, each run as `.venv/bin/python -I <probe> <archive root>`: `probe_reclassify_audit_route.py` (c8a9874: HTTP 500, stored kind changed to unclear, `review_events` empty; a850be0: HTTP 200, one reclassify event); `probe_rate_cue_gaps.py` (output `rate-cue-gaps-run.txt`); `probe_classifier_vs_wording_gate.py` (output `classifier-vs-gate-run.txt`); `probe_restore_class_only_flip.py` on a850be0 and on mutant m03 (output `restore-class-only-flip-run.txt`).
- Scratch mutants via `mutate_r2.py` on copies of the archive (log `mutation-run-r2.txt`). Control 139 passed. T84-1 (rate cue removed from the wording gate) 21 failed; T84-2 ('per' removed from the rate-cue pattern) 11 failed; T84-3 (restore ignores the code class) 139 passed; T84-4 (restore ignores the sentence change) 1 failed; T84-5 (restore always skips the checks, the r1 bug) 2 failed; T84-6 (promoted charge kept when its sentence changes) 1 failed. T73-1 to T73-4 are in the T-073 r2 review.
- `grep -rn "judge_guard.guarded" app/`: review.py:102 and reclassify.py:167 only.

## Findings

### F1 (major): restore after a class-only change is untested; mutant T84-3 survives

- The code is right. `_may_restore` (reclassify.py:145-153) requires `rerun.code_class == "charge"` and an unchanged sentence sha. Probe `probe_restore_class_only_flip.py` on a850be0 (the rerun changes only the code's class of $310; the excerpt is identical): `4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE`; `5. stored kind = unclear`; `pending total cents = 0`.
- The gap is the test. Mutant T84-3 (reclassify.py:153 without the class clause) passes all 139 tests. The same probe on that mutant gives `restored=True kind=charge` and `pending total cents = 31000`.
- The tests cover the sentence arm only. test_reclassify.py:190 `RATE_R3` changes the sentence and the class together; test_reclassify.py:198-216 uses it. test_reclassify.py:219-230 changes the sentence only.
- Why it matters: the brief asks that a restore re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to `_may_restore` can reopen the r1 blocker with no failing test.
- Fix: patch `amounts.classify` so the rerun's code class of $310 is "rate" while the excerpt is identical. `reclassify(..., {"to": "charge"}, call=None)` must raise 422 JUDGE_UNAVAILABLE with the item still `unclear`. Add the same case with `call=FakeCall(J2("agree"))`: the judge is called once and `restored` is False. Keep test_reclassify.py:233-240 passing.
- Acceptance test: mutant T84-3 fails the new test.

### F2 (major): the code wording gate passes unit-price phrasings that the amount classifier calls rates

- Probe `probe_classifier_vs_wording_gate.py`: "Charged $150 an hour." is `rate` by amounts.classify and passes charge_wording; "Charged $75 a unit." is `rate` and passes; "Billed $120 an appointment." is `rate` and passes. amounts.py:14 `_UNIT` includes hour, unit and appointment; the gate's rate-cue pattern (reclassify.py:31-33) has none of them.
- Probe `probe_rate_cue_gaps.py`: "Billed $150 hourly.", "Charged $90 apiece.", "Billed $40 daily." and "Billed $200 a month." also pass the code gate. The two named strings are refused, so F2 is not about the brief's named cases.
- Why it matters: D-042 as written is met, because the sentence has charged wording and the judge re-checks it. But the code gate and the classifier disagree about the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only in part.
- Fix: one rate-unit test shared by amounts.classify and reclassify.charge_wording. The uncommitted working tree already moves toward `amounts.RATE_CUE` (not reviewed here). Whatever lands, refuse the six phrasings before the judge.
- Acceptance test: `charge_wording` returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for "Charged $150 an hour.", "Charged $75 a unit." and "Billed $120 an appointment."; a parametrized test asserts that for every fixture sentence, `amounts.classify == "rate"` implies `charge_wording is None`.

### F3 (minor): the state change and its audit row are separate autocommit writes; the consequence is observed

- reclassify.py:135 `DB.update_item` commits on its own (db.py:54 `isolation_level=None`). reclassify.py:137 `review.batch_apply` (for a non-pending item) and reclassify.py:138 `_log` follow as separate statements.
- Observed on c8a9874: `POST reclassify a1 -> HTTP 500`, `a1 stored after request: kind=unclear`, `review_events for a1: []`. The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).
- Fix: wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as `apply_review` does (db.py:227, :287).
- Acceptance test: monkeypatch `RC._log` to raise; assert the item's kind is still `charge` after the call.

### F4 (minor): a promoted charge is dropped silently when its sentence changes

- reclassify.py:188-189 returns the fresh item when the sentence sha differs, which discards the reclassification record with no note. The figure falls back to the code's class (fail-closed: it leaves the total).
- test_reclassify.py:249-250 asserts only `kind != "charge"`. The audit row stays, but the item view does not say why the figure changed.
- Fix: keep the record with `dropped: "SENTENCE_CHANGED"` in `ladder.reclassification` and show it in the item view and stepper.
- Acceptance test: after a sentence change, `item.ladder.reclassification.dropped == "SENTENCE_CHANGED"`.

## Closed at HEAD (not findings at a850be0)

- c8a9874 on its own tree (blocker at c8a9874, closed at HEAD). `git show c8a9874:app/db/schema.sql` has no 'reclassify' in the CHECK, while reclassify.py:27 sets `AUDIT_ACTION = "reclassify"`. The INSERT fails with IntegrityError (reclassify.py:90), the route returns 500, and the item is already changed (F3). 2fca530 (T-087/T-086, a sibling commit) reverted the T-095 CHECK and migration; 6feb2ff ("fix: restore T-095 work reverted by 2fca530") restored them. At a850be0 the CHECK is at schema.sql:57, SCHEMA_VERSION is 4 (db.py:33), the four files pass 120 of 120, and the probe returns 200 with a `reclassify` event. The card should cite 6feb2ff, since c8a9874 alone does not pass.
- r1 F4 (audit action 'edit'): closed. AUDIT_ACTION is "reclassify" (reclassify.py:27) and test_route (test_reclassify.py:319) asserts `["reclassify"]`, which passes at HEAD.
- r1 F2 (billing removed by ec33bf0): closed. billing.py and test_billing.py are identical to f218263 at a850be0; api.py:510 registers the routes; test_billing.py passes (27).
- r1 F1 (restore after a rerun), sentence arm: closed. Mutants T84-4, T84-5 and T84-6 fail 1, 2 and 1 tests. Class arm: code correct (probe), test missing (F1).
- r1 F3 (rate phrase passes the wording gate), named strings: closed. "Charge per visit $185." and "Billed $150 per visit." are refused before the judge (test_reclassify.py:161-171, `call.log == []`). Mutant T84-1 fails 21 tests and T84-2 fails 11. The remaining gap is F2.

## Judgement on the worker's extra behaviour

A promoted charge falls back to the code's class when a rerun changes its sentence (reclassify.py:188-189). I judge this right: it fails closed, and it applies the same rule as the restore path (a sentence change means the earlier judge answer no longer applies). The silent drop is F4.

## What is right

- reclassify.py:145-153 (`_may_restore`) requires a charge original, a previous judge, and, after any rerun, the same sentence sha and a charge code class. The probe confirms the refusal (422 JUDGE_UNAVAILABLE, total 0).
- The refusals stay before the judge: test_reclassify.py:170 asserts `call.log == []` and the item stays `rate`, `needs_review`.
- Billing is back in HEAD: identical to f218263, registered at api.py:510, 27 tests pass.

## Outside these cards (observed at a850be0, not attributed to T-073 or T-084)

- The sample CLI crashes: `python -m app.pipeline evals/golden/sample.txt` ends in UnboundLocalError at pipeline.py:501. `git blame` puts lines 500-501 in 865b1865 (T-085). This is persona checklist item 20, and it fails on HEAD.
- Seven unit tests fail at a850be0 (listed in Exercised). I did not trace them to a cause. None is in the T-073 or T-084 files.

## Scores

```
no_rate_into_total_without_both_checks 3 (both checks run on every path; the class-only restore is untested, F1; the code gate passes six classifier-rate phrasings, F2)
restore_rule_tested 3 (sentence arm killed; class arm not, F1)
code_check_strength 2 (named strings and 17 cues refused; six classifier-rate phrasings pass, F2)
judge_gate 4 (judge disagree, unsure and unavailable give 422 with nothing changed)
audit_trail 3 (written at HEAD; the item change and the audit row are not one transaction, F3; the promoted drop is not shown, F4)
commit_integrity 2 (c8a9874 alone fails 9 tests and returns 500 with the item changed; closed at HEAD by 6feb2ff, which is not in this card's commit list)
billing_restored 5 (identical to f218263; route registered; 27 tests pass)
tests_kill_mutants 4 (T84-1, T84-2, T84-4, T84-5, T84-6 and the four T-073 mutants killed; T84-3 survives)
```

## Questions for Chris

- D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should "Charged $150 an hour.", "Charged $75 a unit." and "Billed $120 an appointment." be refused by the code gate before the judge, given that the amount classifier calls them rates? My reading is that they should be refused. The decision text does not say.

```json
{"card": "T-084", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c8a9874 (T-084 r2, committed with the T-073 r2 changes) and e2b4e3f underneath; HEAD at review end a850be0 (bc12d44 at start), pinned by git archive; files app/backend/reclassify.py, app/backend/amounts.py (read), app/backend/api.py (routes), app/db/db.py and app/db/schema.sql (read, restored by 6feb2ff), tests/unit/test_reclassify.py, tests/unit/test_billing.py; c8a9874 alone fails 9 tests and is closed at HEAD by 6feb2ff (not a finding at a850be0); no app URL; the sample CLI run at a850be0 crashes (outside this card, see body)",
 "exercised": ["python3 tools/board.py show T-084, T-094, T-095", "git log --oneline -8; git rev-parse HEAD (bc12d44 then a850be0); git show --stat c8a9874, e2b4e3f, 6feb2ff, a850be0; git show c8a9874:app/db/schema.sql | grep -c reclassify (0); git diff --stat bc12d44 a850be0 over the in-scope files (db.py and schema.sql only); git diff --stat f218263 a850be0 over the billing files (empty); git ls-tree a850be0 | grep billing (both files); a850be0 api.py lines 510 and 512; git blame -L 496,502 a850be0 -- app/backend/pipeline.py", ".venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py: working tree 120 passed; a850be0 120 passed; c8a9874 9 failed 111 passed (IntegrityError at reclassify.py:90)", ".venv/bin/python -m pytest -q tests/unit/test_audited.py at a850be0: 19 passed; tests/unit/test_billing.py: 27 passed; tests/unit at a850be0: 7 failed 1392 passed 2 skipped", ".venv/bin/python -m app.pipeline evals/golden/sample.txt at a850be0: UnboundLocalError at pipeline.py:501", "read in full at a850be0: reclassify.py and test_reclassify.py (both unchanged since bc12d44), judge_guard.py, audited.py; db.py:54, :215, :227, :287; amounts.py:14", "probes via .venv/bin/python -I in artifacts/review-evidence/T-073-T-084-r2/: probe_reclassify_audit_route.py (c8a9874: HTTP 500, item changed, no event; a850be0: HTTP 200, one reclassify event); probe_rate_cue_gaps.py (rate-cue-gaps-run.txt); probe_classifier_vs_wording_gate.py (classifier-vs-gate-run.txt); probe_restore_class_only_flip.py on a850be0 (422 JUDGE_UNAVAILABLE, total 0) and on mutant m03 (restored, total 31000; restore-class-only-flip-run.txt)", "scratch mutants via mutate_r2.py (mutation-run-r2.txt): control 139 passed; T84-1 21 failed; T84-2 11 failed; T84-3 139 passed (survives); T84-4 1 failed; T84-5 2 failed; T84-6 1 failed", "grep -rn judge_guard.guarded app/ (review.py:102 and reclassify.py:167 only)"],
 "verdict": "changes",
 "scores": {"no_rate_into_total_without_both_checks": 3, "restore_rule_tested": 3, "code_check_strength": 2, "judge_gate": 4, "audit_trail": 3, "commit_integrity": 2, "billing_restored": 5, "tests_kill_mutants": 4},
 "findings": [
  {"severity": "major", "title": "Restore after a class-only change is untested; mutant T84-3 (restore ignores the rerun's code class) passes all 139 tests",
   "evidence": "reclassify.py:153 'return rerun.get(code_class) == charge and rerun.get(excerpt_sha) == prior.get(excerpt_sha) == _sha(row[excerpt])'; mutant without the class clause: mutation-run-r2.txt 'T84-3 ... 139 passed'; restore-class-only-flip-run.txt: HEAD '4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE', mutant 'restored=True kind=charge' and 'pending total cents = 31000'; tests/unit/test_reclassify.py:190 RATE_R3 and :198-216 change the sentence, not only the class",
   "why_it_matters": "The brief requires a restore to re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to _may_restore can reopen the r1 blocker and no test fails.",
   "fix": "Add a test that patches amounts.classify so the rerun's code class of $310 is rate while the excerpt is identical; reclassify to charge with call=None must raise 422 JUDGE_UNAVAILABLE with the item still unclear. Add the same case with call=FakeCall(J2 agree): the judge is called once and restored is False. Keep test_reclassify.py:233-240 passing.",
   "acceptance_test": "Mutant T84-3 (reclassify.py:153 without the code_class clause) fails the new test."},
  {"severity": "major", "title": "The code wording gate passes unit-price phrasings that the amount classifier calls rates, so the judge is the only gate for them",
   "evidence": "classifier-vs-gate-run.txt: 'Charged $150 an hour.' classifier rate, gate passes (Charged); 'Charged $75 a unit.' rate, passes; 'Billed $120 an appointment.' rate, passes. rate-cue-gaps-run.txt: 'Billed $150 hourly.', 'Charged $90 apiece.', 'Billed $40 daily.', 'Billed $200 a month.' pass the gate. reclassify.py:31-33 _RATE_CUE has no hour, unit or appointment; amounts.py:14 _UNIT = (visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?",
   "why_it_matters": "D-042 as written is met (charged wording plus a judge re-check), but the code gate and the classifier disagree on the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only in part.",
   "fix": "Use one rate-unit test for amounts.classify and reclassify.charge_wording (the uncommitted working tree already moves toward amounts.RATE_CUE; not reviewed here). Refuse the six phrasings before the judge.",
   "acceptance_test": "charge_wording returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for 'Charged $150 an hour.', 'Charged $75 a unit.', 'Billed $120 an appointment.'; a parametrized test asserts that for every fixture sentence, amounts.classify == rate implies charge_wording is None."},
  {"severity": "minor", "title": "State change and audit row are separate autocommit writes; a failed audit write leaves the item changed and no event (observed)",
   "evidence": "reclassify.py:135 DB.update_item (autocommit, db.py:54 isolation_level=None); reclassify.py:137 batch_apply; reclassify.py:138 _log. Probe probe_reclassify_audit_route.py on c8a9874: 'POST reclassify a1 -> HTTP 500', 'a1 stored after request: kind=unclear', 'review_events for a1 (action, payload event): []'",
   "why_it_matters": "The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).",
   "fix": "Wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).",
   "acceptance_test": "Monkeypatch RC._log to raise; assert the item kind is still charge after the call."},
  {"severity": "minor", "title": "A promoted charge is dropped silently when a rerun changes its sentence",
   "evidence": "reclassify.py:188-189 'if rc.get(to) == charge and rc.get(excerpt_sha) != _sha(it.get(excerpt)): return it' discards the reclassification record with no note; tests/unit/test_reclassify.py:249-250 asserts only kind != charge",
   "why_it_matters": "Fail-closed is the right direction (the figure leaves the total), but the paralegal gets no sign that her promotion was withdrawn, and the item view does not say why the figure changed.",
   "fix": "Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.",
   "acceptance_test": "After a sentence change, item.ladder.reclassification.dropped == SENTENCE_CHANGED and the item view names the reason."}
 ],
 "whats_right": [
  "reclassify.py:145-153 (_may_restore) refuses a restore after a class or sentence change; probe restore-class-only-flip-run.txt shows 422 JUDGE_UNAVAILABLE with the total at 0.",
  "test_reclassify.py:161-171 refuses 'Charge per visit $185.' and 'Billed $150 per visit.' before the judge (call.log == []); mutant T84-1 fails 21 tests.",
  "tests/unit/test_billing.py and app/backend/billing.py are identical to f218263, the billing route is registered at api.py:510, and 27 billing tests pass at a850be0."
 ],
 "questions_for_chris": ["D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should 'Charged $150 an hour.', 'Charged $75 a unit.' and 'Billed $120 an appointment.' be refused by the code gate before the judge, given that the amount classifier calls them rates? The decision text does not say."]}
```
