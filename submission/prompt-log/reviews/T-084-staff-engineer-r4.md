# T-084 r4 review (staff-engineer-reviewer)

Commit under review: 9c1af01 (board HEAD). The T-084 r3 code is not in 9c1af01. It is in 57a08ba, which 9c1af01 keeps; 9c1af01 restores the 12 T-085 files that 57a08ba had reverted by mistake. HEAD was pinned with `git archive 9c1af01` into the session scratchpad (reviewers cannot use worktree). Model: claude-haiku-5-5, as the environment reports. The persona header expects claude-sonnet-5-5; the record shows the model I actually ran as.

## Summary

Both r3 majors are closed at HEAD. (F1) The class-only restore test exists (test_reclassify.py:274 and :285), and mutant T84-3 (the code-class clause removed from `_may_restore`) now fails 2 tests. (F2) The wording gate calls the shared `amounts.RATE_CUE` (reclassify.py:31, :77). The four named phrasings ("unit price $X", "@ $X", "$X/visit", "rate of $X") and the two brief strings are refused with 422 NO_CHARGE_WORDING before the judge is called.

Three things are weaker than the card says. (a) For "rate of $X" and "/visit", the refusal depends on the classifier arm or on the other cue, and no test isolates either. Removing either arm passes all 148 tests. (b) The r3 minors F3 (item change and audit row are separate writes) and F4 (a promoted charge is dropped with no note) are still present, and I reproduced both. (c) The card's commit list names 9c1af01, which touches none of the three T-084 files; it omits 57a08ba, which carries the change.

No blocker. No major. Verdict: pass (per rule: no blocker, no major).

## Exercised (what I actually ran or read)

- `python3 tools/board.py show T-084`: status in_review, commits [ec33bf0, c8a9874, e2b4e3f, 9c1af01], AC 1 evidence cites 9c1af01, Notes and handoff for r3.
- `git log --oneline -5`; `git rev-parse HEAD` gives 9c1af01da6c7ec3dfc1f3f48faf035705bea8866.
- `git archive 9c1af01 | tar -x` into the scratchpad (head_9c1af01). Every test below ran there, not in the dirty working tree.
- `.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py` on the pinned archive: `148 passed in 1.75s`, exit 0.
- `git archive 57a08ba` into the scratchpad, same two files with the same command: `148 passed in 1.69s`.
- `git show --stat 9c1af01` (12 T-085 files, no T-084 file); `git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py` (empty output); `git diff --stat 1b1c711 9c1af01` (3 files, 82 insertions, 3 deletions); `git diff --stat 57a08ba 9c1af01` (12 files); `git show --stat 57a08ba` (15 files, including 12 T-085 deletions).
- Read in full at the pinned HEAD: app/backend/reclassify.py lines 25-35, 66-96, 97-141, 148-200 (the gate, `_may_restore`, `_guard`, `carry_over`); app/backend/amounts.py lines 14-34 (the shared cue); tests/unit/test_reclassify.py lines 160-330.
- `grep -rn "RATE_CUE\|has_rate_cue" app/` at HEAD: reclassify.py:31 and :77; billing.py:190 and :256 use `A.has_rate_cue`.
- Mutation driver `artifacts/review-evidence/T-084-r4/mutate_t84_r4.py`, run on copies of the pinned archive with `.venv/bin/python -I`; output in `artifacts/review-evidence/T-084-r4/mutation-run-r4.txt`:
  - M0 control: 148 passed.
  - T84-3 (reclassify.py:156 code-class clause removed): 2 failed (test_reclassify.py:274 and :285).
  - T84-s (reclassify.py:156 sentence-sha clause replaced by True): 1 failed.
  - G1 (reclassify.py:77 shared cue removed from the gate): 10 failed.
  - G1b (reclassify.py:77 classifier arm `_classified_rate` removed): 148 passed. Survives.
  - G2 (amounts.py:24 `@ $` cue removed): 1 failed (`Billed @ $90.`).
  - G3 (amounts.py:23 `rate` word cue removed): 148 passed. Survives.
  - G4 (amounts.py:22 `/visit` cue removed): 1 failed, and it is in test_billing.py only (`Charge /visit`). No reclassify test fails.
  - G5 (amounts.py:24 `unit price` alternative removed): 148 passed. Survives; `unit` plus `price` is still matched by the daily/hourly alternative at amounts.py:23.
- Gate-layer probe `artifacts/review-evidence/T-084-r4/probe_gate_layers_t84_r4.py` on HEAD, G3 and G5: output in `gate-layers-run-r4.txt`. On HEAD all four brief phrasings and the two extra ones are refused. In G3, "Billed at a rate of $90." has cue False and is still refused, with classify = rate.
- Real-path probe (a copy of HEAD with a scratch test file, saved as `artifacts/review-evidence/T-084-r4/probe_real_path_and_f3_f4_r4.py`): `5 passed` for the brief phrasings "Billed unit price $90.", "Billed @ $90.", "Billed $90/visit.", "Billed $90 /visit.", "Billed at a rate of $90." The reclassify call with a judge FakeCall gives 422 NO_CHARGE_WORDING, `call.log == []`, and the item is not charge.
- Reproduction of r3 F3 and F4 at HEAD (same probe file, output in `probe-real-path-f3-f4-run-r4.txt`): with `RC._log` raising, `reclassify` raises and the item is then `unclear`, not `charge` (`assert 'unclear' == 'charge'`); after a sentence change, `ladder.reclassification` is `None` (printed).

## Findings

### F1 (minor): the shared cue is not pinned for "rate of $X" or "/visit"; each refusal rests on the other arm

- Evidence: `artifacts/review-evidence/T-084-r4/mutation-run-r4.txt`: `G3_no_rate_of_cue: rc=0 | 148 passed`; `G1b_gate_ignores_classifier_rate: rc=0 | 148 passed`; `G4_no_slash_visit_cue: 1 failed` in test_billing.py only. Gate probe: `Billed at a rate of $90.` cue False in the G3 copy, refused anyway (classify = rate). The refusal comes from reclassify.py:77 `_classified_rate`, which is the amounts.classify verdict.
- Why it matters: the card says the gate uses the shared cue so these phrasings are refused before the judge. That holds at HEAD (the 5 real-path probes pass). But no test fails if the shared cue loses "rate" or "/visit", or if the classifier arm is removed. Each arm covers the other, so one regression in either can go unnoticed. The brief asked (r3 F2) for one rate-unit test that pins the shared cue. This is a test-strength gap, not a spec violation.
- Fix: parametrize over "Billed unit price $90.", "Billed @ $90.", "Billed $90/visit.", "Billed at a rate of $90." and assert `amounts.RATE_CUE.search(sentence)` is truthy (the cue alone). Also assert `charge_wording` is None with `RC._classified_rate` monkeypatched to return False, so the cue arm is the only decider.
- Acceptance test: mutant G3 (the rate word removed from amounts.py:23) and mutant G1b (reclassify.py:77 `_classified_rate` removed) each fail at least one test in tests/unit/test_reclassify.py.

### F2 (minor, carried from r3 F3): the item change and the audit row are separate writes; reproduced at HEAD

- Evidence: reclassify.py:138 `DB.update_item(...)` (autocommit), :140 `review.batch_apply(...)`, :141 `_log(...)`. Probe in `probe-real-path-f3-f4-run-r4.txt`: with `RC._log` raising RuntimeError, `reclassify` raises as expected, and the item is then `unclear`; the test expected `charge` and got `'unclear' == 'charge'`.
- Why it matters: a failed audit write now surfaces as an error (not silent), but the item has already changed and no audit row exists for it. Minor, as in r3, because the error is visible.
- Fix: run update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as `apply_review` does (db.py:227, :287).
- Acceptance test: the probe's `test_zz_f3_...` passes at HEAD (the item stays `charge` after the raised audit write).

### F3 (minor, carried from r3 F4): a promoted charge is dropped with no note; reproduced at HEAD

- Evidence: reclassify.py:191-192 (`if rc.get("to") == "charge" and rc.get("excerpt_sha") != _sha(...)`: `return it`). Probe output: `F4 ladder.reclassification after sentence change = None`. test_reclassify.py:316-325 asserts only `kind != "charge"`.
- Why it matters: fail-closed is right (the figure leaves the total), but the paralegal gets no sign her promotion was withdrawn. Minor, as in r3.
- Fix: keep the record with `dropped: "SENTENCE_CHANGED"` in `ladder.reclassification` and show it in the item view and stepper.
- Acceptance test: after a sentence change, `ladder.reclassification.dropped == "SENTENCE_CHANGED"` (the probe's `test_zz_f4_...` passes then).

### F4 (minor, new): the card's commit trail names 9c1af01, which carries none of the T-084 change

- Evidence: `git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py` prints nothing. `git diff --stat 1b1c711 9c1af01` lists exactly those 3 files. `git show --stat 57a08ba` shows the same 3 files plus 12 T-085 deletions. `board.py show T-084` gives commits [ec33bf0, c8a9874, e2b4e3f, 9c1af01] and the AC 1 evidence cites 9c1af01. 9c1af01's message says "T-084 r3 change stays", which describes the tree, not that commit.
- Why it matters: the audit trail for the r3 fix points at a commit that does not contain it. Anyone who runs `git show 9c1af01` for the F1/F2 fix finds only T-085 files. The 57a08ba commit on its own passes the 148 tests (run above), so the code is fine; the record is wrong. Its T-085 deletions are undone by 9c1af01, but that is in the history.
- Fix (orchestrator, card only): add 57a08ba to the card's commits and cite it in AC 1 evidence. Do not rewrite history.
- Acceptance test: every commit in `git log --oneline -- app/backend/reclassify.py app/backend/amounts.py tests/unit/test_reclassify.py` since ec33bf0 appears in the card's commits list. (At HEAD that log shows 57a08ba, 8bc7f90 (T-083 r2) and c8a9874. 8bc7f90 belongs to another card, so it is not required on T-084.)

## What is right

- `_may_restore` (reclassify.py:148-156) has both clauses tested on their own. T84-3 (class clause removed) fails 2 tests; T84-s (sentence clause removed) fails 1.
- The wording check runs before the judge (reclassify.py:166-168). The brief phrasings reach 422 NO_CHARGE_WORDING with the judge never called (5 real-path tests pass).
- The gate and the classifier share one compiled cue (reclassify.py:31, amounts.py:27) and billing reaches the same core via `has_rate_cue` (billing.py:190, :256). The "@ $" cue is pinned by a test (G2 fails 1).

```json
{"card": "T-084", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 9c1af01 (board HEAD, pinned with git archive into the scratchpad); T-084 r3 code is in 57a08ba (also archived and tested); files app/backend/reclassify.py, app/backend/amounts.py, tests/unit/test_reclassify.py, tests/unit/test_billing.py; no app URL; no sample CLI run (outside this card's files)",
 "exercised": ["python3 tools/board.py show T-084 (commits, AC 1 evidence, notes, handoff)", "git log --oneline -5; git rev-parse HEAD (9c1af01da6c7ec3dfc1f3f48faf035705bea8866)", "git archive 9c1af01 | tar -x into the scratchpad; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py: 148 passed", "git archive 57a08ba into the scratchpad; same command: 148 passed", "git show --stat 9c1af01; git show --stat --format= 9c1af01 -- amounts.py reclassify.py test_reclassify.py (empty); git diff --stat 1b1c711 9c1af01 (3 files); git diff --stat 57a08ba 9c1af01 (12 files); git show --stat 57a08ba", "read in full at 9c1af01: reclassify.py 25-35, 66-200; amounts.py 14-34; test_reclassify.py 160-330", "grep -rn RATE_CUE/has_rate_cue app/ at 9c1af01", "mutation driver artifacts/review-evidence/T-084-r4/mutate_t84_r4.py on pinned copies (mutation-run-r4.txt): M0 148 passed; T84-3 2 failed; T84-s 1 failed; G1 10 failed; G1b 148 passed; G2 1 failed; G3 148 passed; G4 1 failed (billing only); G5 148 passed", "gate-layer probe artifacts/review-evidence/T-084-r4/probe_gate_layers_t84_r4.py on HEAD, G3, G5 (gate-layers-run-r4.txt)", "real-path probe artifacts/review-evidence/T-084-r4/probe_real_path_and_f3_f4_r4.py on a HEAD copy: 5 brief phrasings 422 NO_CHARGE_WORDING, call.log empty (5 passed); F3 and F4 reproduced (probe-real-path-f3-f4-run-r4.txt)"],
 "verdict": "pass",
 "scores": {"no_rate_into_total_without_both_checks": 4, "restore_rule_tested": 5, "code_check_strength": 4, "judge_gate": 4, "audit_trail": 3, "commit_integrity": 3, "billing_restored": 5, "tests_kill_mutants": 4},
 "findings": [
  {"severity": "minor", "title": "The shared rate cue is not pinned for rate of and /visit; each refusal rests on the other arm, and no test fails if either arm is removed",
   "evidence": "artifacts/review-evidence/T-084-r4/mutation-run-r4.txt: G3_no_rate_of_cue rc=0 148 passed (amounts.py:23 rate word removed); G1b_gate_ignores_classifier_rate rc=0 148 passed (reclassify.py:77 _classified_rate removed); G4_no_slash_visit_cue fails only tests/unit/test_billing.py (amounts.py:22 removed). gate-layers-run-r4.txt: Billed at a rate of $90. cue False in the G3 copy, still refused (classify rate)",
   "why_it_matters": "The card says the gate uses the shared cue so these phrasings are refused before the judge. That holds at HEAD, but a regression in either arm for these phrasings passes all 148 tests. This is test strength, not a spec violation, so minor.",
   "fix": "Parametrize over Billed unit price $90., Billed @ $90., Billed $90/visit., Billed at a rate of $90. and assert amounts.RATE_CUE.search is truthy for each; also assert charge_wording is None with RC._classified_rate monkeypatched to False so the cue arm alone decides.",
   "acceptance_test": "Mutant G3 (rate word removed at amounts.py:23) and mutant G1b (reclassify.py:77 _classified_rate removed) each fail at least one test in tests/unit/test_reclassify.py."},
  {"severity": "minor", "title": "Item change and audit row are separate writes; a failed audit write leaves the item changed (carried from r3 F3, reproduced at HEAD)",
   "evidence": "reclassify.py:138 DB.update_item (autocommit), :140 review.batch_apply, :141 _log. artifacts/review-evidence/T-084-r4/probe-real-path-f3-f4-run-r4.txt: with RC._log raising RuntimeError, the call raises and the item is then unclear (assert 'unclear' == 'charge')",
   "why_it_matters": "The failure is visible (the error propagates), but the paralegal's item has changed and no audit row exists for it. Minor, as in r3.",
   "fix": "Run update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).",
   "acceptance_test": "With RC._log raising, the item's kind is still charge after the call raises (the probe test test_zz_f3 passes)."},
  {"severity": "minor", "title": "A promoted charge is dropped with no note when its sentence changes (carried from r3 F4, reproduced at HEAD)",
   "evidence": "reclassify.py:191-192 (if rc.get to == charge and excerpt_sha differs: return it). Probe output: F4 ladder.reclassification after sentence change = None. test_reclassify.py:316-325 asserts only kind != charge",
   "why_it_matters": "Fail-closed is the right direction (the figure leaves the total), but the paralegal gets no sign her promotion was withdrawn and the item view cannot say why. Minor, as in r3.",
   "fix": "Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.",
   "acceptance_test": "After a sentence change, item.ladder.reclassification.dropped == SENTENCE_CHANGED (the probe test test_zz_f4 passes)."},
  {"severity": "minor", "title": "The card's commit trail names 9c1af01, which contains none of the T-084 r3 change; 57a08ba, which does, is not listed",
   "evidence": "git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py prints nothing; git diff --stat 1b1c711 9c1af01 lists those 3 files; git show --stat 57a08ba lists them plus 12 T-085 deletions; board.py show T-084 commits [ec33bf0, c8a9874, e2b4e3f, 9c1af01]; AC 1 evidence cites 9c1af01",
   "why_it_matters": "The audit trail for the r3 fix points at a commit that does not contain it. The code is fine: 57a08ba on its own archive passes 148 tests. The record is wrong.",
   "fix": "Orchestrator: add 57a08ba to the card's commits and cite it in AC 1 evidence. Do not rewrite history.",
   "acceptance_test": "Every commit in git log --oneline -- app/backend/reclassify.py app/backend/amounts.py tests/unit/test_reclassify.py since ec33bf0 is in the card's commits list."}
 ],
 "whats_right": [
  "_may_restore (reclassify.py:148-156): both clauses are now tested on their own; T84-3 fails 2 tests (test_reclassify.py:274, :285).",
  "The wording check runs before the judge (reclassify.py:166-168); the brief phrasings reach 422 NO_CHARGE_WORDING with the judge never called (5 real-path tests pass).",
  "The gate and the classifier share one compiled cue (reclassify.py:31, amounts.py:27), and the @ dollar cue is pinned by a test (mutant G2 fails 1)."
 ],
 "questions_for_chris": []}
```
