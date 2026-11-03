# T-084 review: guarded charge reclassification (D-042) (staff-engineer)

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit reviewed: ec33bf0 (T-084), with the T-073 commit 7724412 underneath it. HEAD was pinned with `git archive ec33bf0` into the session scratchpad because the working tree moved during the review (app/backend/reclassify.py and tests/unit/test_reclassify.py now show uncommitted edits from another worker; I did not review those).

## Summary

The guard works for the cases the tests name. Judge disagree, unsure or unavailable gives a 422 with nothing changed. Missing wording gives a 422 with the judge never called. Seven scratch mutants of the guard are all caught. Demotion from charge to not-a-charge is allowed, leaves the total, and is audited.

Three things break the invariant the brief asked me to check, "totals never include a reclassified rate without both checks passing":

1. **Blocker.** Undoing a demotion ("restore") skips both checks, and it does so on the stored judge answer from the old sentence. If a rerun changes the code's class for the same figure, a restore turns a current rate into a charge with no check at all. Reproduced.
2. **Blocker.** The commit ec33bf0 deletes T-083's billing module, its tests, its API route and its API documentation, which were committed in f218263. The deletion is not in the commit message or the card. HEAD no longer serves `GET /api/cases/{token}/billing`, which D-042 reinstates.
3. **Major.** The code wording check accepts the rate phrase itself. "Charge per visit $185" and "Billed $150 per visit" both pass as "charged-amount wording", so the judge is the only gate for the exact case the brief names. Reproduced.

Verdict: fail (two blockers).

## Exercised (what I actually ran or read)

- `python3 tools/board.py show T-084` and `show T-083` (AC, handoff, the "NEEDS DB CARD" note, the T-083 commit list).
- `git show --stat ec33bf0`; `git show ec33bf0 -- app/backend/api.py app/backend/pipeline.py`; `git show ec33bf0 -- memory/contracts/api.md` (39 lines removed, 24 added).
- `git ls-tree -r --name-only ec33bf0 | grep -i billing` gave no output. `git ls-tree -r --name-only f218263 | grep -i billing` gave `app/backend/billing.py` and `tests/unit/test_billing.py`. `git show ec33bf0:app/backend/api.py | grep -n billing` gave no output. `git show f218263:app/backend/api.py` lines 497-498 are the billing hook. `git status --short app/backend/billing.py tests/unit/test_billing.py` gave `?? app/backend/billing.py` and `?? tests/unit/test_billing.py` (the files exist on disk, untracked).
- `git show ec33bf0:app/backend/reclassify.py` (full read; line numbers cited below are HEAD's), and `git show ec33bf0:tests/unit/test_reclassify.py` (full read).
- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass"` in the working tree: `109 passed, 1173 deselected`. HEAD archive: `107 passed, 1068 deselected`.
- Scratch mutants on the HEAD archive (`artifacts/review-evidence/T-073-T-084/mutate.py`, log `artifacts/review-evidence/T-073-T-084/mutation-run.txt`):
  - t084-1 judge gate removed: 5 failed.
  - t084-2 wording gate removed: 2 failed.
  - t084-3 negation gate removed: 2 failed.
  - t084-4 judge "unsure" accepted: 1 failed.
  - t084-5 audit write removed: 4 failed.
  - t084-6 value gate removed: 1 failed.
  - t084-7 judge refusal turned into a pass: 5 failed.
  - Control: 55 passed.
- Probes on the HEAD archive (`artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py`, `probe_t084_billed_150_per_visit.py`; output `artifacts/review-evidence/T-073-T-084/probe-run.txt`).
- Grep for `except` in reclassify.py, judge_guard.py, review.py (none in reclassify.py).

## Findings

### F1 (blocker): restore after a rerun turns a current rate into a charge with no check

- `app/backend/reclassify.py:102-104` (HEAD): `restored = original == "charge" and prior.get("previous_judge") is not None`, then `if not restored:` skips `_guard` (both checks). `carry_over` at `reclassify.py:157-163` keeps her demotion when a rerun reaches the same figure text and value (`reclassify.py:160`: `old["text"] != it["text"] or old["value_cents"] != it["cents"]`). It does not compare the sentence, so a changed sentence still matches.
- Reproduction (`artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py`, `test_probe_restore_after_rerun_class_flip`). Seed TEXT (charge `$310` in record 3, "MRI performed. Charge: $310."). Demote it to not-a-charge. Rerun the pipeline with record 3 changed to "MRI performed. Rate of $310 per visit." (same figure, same value). The current code now calls it a rate. Then reclassify to charge with `call=None` (no judge available). Output:
  ```
  rerun with code class flipped to rate:
     a3 $310 ['r3'] kind= unclear
  RESTORE WITHOUT ANY CHECK -> charge restored= True pending total= 31000
  ```
  The sentence "Rate of $310 per visit." has no charged wording and the judge never ran on it, yet the figure is a charge in the pending total.
- Why it matters: D-042 says a rate becomes a charge only with code-verified charged wording AND a judge re-check. The restore path uses a judge answer about the old sentence ("Charge: $310.") and skips the code check. The brief's invariant ("totals never include a reclassified rate without both checks passing") fails. The trigger is a rerun that changes the code's class of a figure with the same text and value, which is what a classifier or lexicon change does. The sample case is not affected, but the defect is the one that ends in a total the records do not support (dossier §5, "a total that includes the $185 rate").
- Fix: a restore may skip the checks only when the current rerun's code class still equals the class at demotion and the sentence is unchanged. Otherwise run `_guard` again. Compare the sentence (or a hash of the excerpt), not only text and cents, in `carry_over`.
- Acceptance test: seed as above, demote, rerun with the flipped sentence, then reclassify to charge with `call=None`. Expect 422 `NO_CHARGE_WORDING` (or `JUDGE_UNAVAILABLE`), kind stays `unclear`, no reclassify event. Add a second case where the sentence is unchanged and the restore still passes without a judge (keeps `test_undoing_her_own_demotion_...` at `test_reclassify.py:80-87` true).

### F2 (blocker): commit ec33bf0 deletes T-083's committed billing module, tests and API route

- `git show --stat ec33bf0` lists `app/backend/billing.py | 642 ------` and `tests/unit/test_billing.py | 330 ----------`. Neither is in the commit message ("feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)").
- `git ls-tree -r --name-only ec33bf0 | grep -i billing` gives nothing. `git ls-tree -r --name-only f218263 | grep -i billing` gives both files.
- `app/backend/api.py`: at f218263, lines 497-498 are `from app.backend import billing` and `billing.add_routes(app, conn=conn, get_case=get_case)       # T-083`. At ec33bf0 those lines are replaced by the reclassify hook (`api.py:497-498`), so `GET /api/cases/{token}/billing` is no longer registered.
- `git show ec33bf0 -- memory/contracts/api.md` removes the `GET /api/cases/{token}/billing` row and the "T-083, D-042" section.
- The T-083 card still lists `commits: ["f218263"]` with its evidence `tests/unit/test_billing.py: 27 passed`. That file does not exist at HEAD, so the evidence cannot be reproduced at HEAD.
- D-042 (`memory/ORCHESTRATOR_DECISIONS.md:50`) reinstates "billing analysis on synthetic itemized ledgers". Removing it from HEAD without a recorded scope decision violates that decision. The files are not lost: they are on disk, untracked, and in f218263.
- Why it matters: a commit labelled as one feature silently removes another card's delivered work from the tree. The T-084 review cannot tell whether the removal is intended.
- Fix: restore `app/backend/billing.py`, `tests/unit/test_billing.py`, the `billing.add_routes` hook and the api.md section in a commit under T-083 (`git add` those paths explicitly). If the removal was intended, record it in `memory/SCOPE_CUTS.md` and `memory/ORCHESTRATOR_DECISIONS.md` and update T-083 first. Do not rewrite history.
- Acceptance test: `git ls-tree -r --name-only HEAD | grep billing` lists both files. `tests/unit/test_billing.py` passes at HEAD. A route test gets 200 from `GET /api/cases/{token}/billing`.

### F3 (major): the code wording check passes the rate phrase itself

- `app/backend/reclassify.py:24` `_WORDING` matches `charges?` and `billed`. `charge_wording` only checks that some charged-amount word is in the same sentence. It does not check whether the figure is a rate.
- Reproduction (`probe-run.txt`): `wording(Charge per visit $185): Charge` and `wording(Billed $150 per visit): Billed`. Full path with the brief's example, "Visit completed. Billed $150 per visit.", judge answering `agree`: `after judge agree: charge wording: Billed pending total cents: 15000 accepted: 0`. With record 2 of the test fixture ("Charge per visit $185."): `sneak: amount kind after judge agree = charge pending total cents = 49500`.
- The tests encode this as the expected path. `tests/unit/test_reclassify.py:108-116` (HEAD) reclassifies the rate "Charge per visit $185." to a charge on judge agreement alone and asserts a pending total of 31000 + 18500.
- Why it matters: D-042 is literally met (wording present, judge agrees), so this is not a spec breach as written. But the code check is supposed to be the first independent gate, and for a rate sentence it always passes. The only gate left for the exact case the brief names is one LLM judge, and the record states a rate, not a charge, so a $150-per-visit figure is summed as if it were billed. If Chris reads D-042 as excluding rate sentences, this becomes a blocker.
- Fix: the code check refuses a figure whose sentence carries a rate unit ("per", "each", "a visit", "per unit", "rate of") next to the figure. Keep the wording check for statements of charge.
- Acceptance test: `charge_wording` and `reclassify` return `None` / 422 `NO_CHARGE_WORDING` (judge not called) for "Visit completed. Charge per visit $185." and "Visit completed. Billed $150 per visit.". Move the positive case at `test_reclassify.py:108` to a sentence with no rate unit (for example "Billed $185 for the visit.").

### F4 (minor): the reclassify audit row is stored with action 'edit'

- `app/backend/reclassify.py:22` `AUDIT_ACTION = "edit"`. The payload carries `event: "reclassify"` (`reclassify.py:123`). `test_reclassify.py:215` asserts the action is `["edit"]`.
- The AC ("an audit event is written") is met. The action column still says a summary was edited, which misleads anyone reading `review_events` directly.
- Fix: as the card notes, the DB card adds `reclassify` to the CHECK (bump SCHEMA_VERSION per `app/db/db.py:32`) and then flips the constant.
- Acceptance test: `GET /audit` shows action `reclassify` for the event, and the test at `test_reclassify.py:215` asserts it.

### F5 (minor, read from code, not reproduced): the state change and its audit row are separate writes

- `reclassify.py:120` (`DB.update_item`), `:122` (`review.batch_apply`, which has its own `BEGIN`/`COMMIT` in `db.py`), and `:123` (`_log` INSERT) are three separate statements. A failure after `:120` leaves the item changed with no event.
- Fix: write the audit row and the item change in one transaction, the way `db.apply_review` does.
- Acceptance test: inject a failure at the `_log` call and assert the item is unchanged.

## What is right

- Seven of seven scratch mutants of the reclassify guard are caught (judge gate, wording gate, negation, "unsure" accepted, audit, value gate, judge refusal turned into a pass). See `artifacts/review-evidence/T-073-T-084/mutation-run.txt`.
- Judge disagree, unsure or unavailable gives a 422 with the item unchanged and no event (`test_reclassify.py:124-139`).
- Demotion from charge to not-a-charge leaves the total unchanged, moves the item back to pending and writes the audit (`test_reclassify.py:59-70`).

## Scores

```
no_rate_into_total_without_both_checks 2 (F1 restore bypass)
code_check_strength 2 (F3 rate phrase passes)
judge_gate 4 (mutants caught; refusals leave nothing changed)
audit_trail 3 (written; wrong action label)
commit_scope 1 (F2 deletes T-083 from HEAD)
tests_kill_mutants 5
```

## Questions for Chris

- Was the removal of `app/backend/billing.py` and `tests/unit/test_billing.py` in ec33bf0 intended as a scope cut? If yes, it needs a SCOPE_CUTS entry and a D-042 update before T-083 can be closed. If no, it needs a restore commit (F2).
- Does D-042 allow a rate sentence ("Charge per visit $185.") to satisfy "charged-amount wording"? My reading is that it should not. The decision text does not say.

```json
{"card": "T-084", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit ec33bf0 (T-084, D-042) pinned via git archive, with 7724412 (T-073) underneath; files app/backend/reclassify.py, app/backend/api.py, app/backend/pipeline.py, memory/contracts/api.md, tests/unit/test_reclassify.py; no app URL; no sample-case CLI run (unit-level card)",
 "exercised": ["python3 tools/board.py show T-084 and show T-083", "git show --stat ec33bf0; git show ec33bf0 -- app/backend/api.py app/backend/pipeline.py memory/contracts/api.md", "git ls-tree -r --name-only ec33bf0 | grep -i billing (none) vs f218263 (2 files); git show f218263:app/backend/api.py lines 497-498", "git status --short app/backend/billing.py tests/unit/test_billing.py (both untracked)", "full read of git show ec33bf0:app/backend/reclassify.py and tests/unit/test_reclassify.py", ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass': working tree 109 passed; HEAD archive 107 passed", "scratch mutants t084-1..7 on HEAD archive via artifacts/review-evidence/T-073-T-084/mutate.py: 5,2,2,1,4,1,5 failed; control 55 passed", "probes artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py and probe_t084_billed_150_per_visit.py (output probe-run.txt): restore after class flip -> charge, restored True, pending 31000; 'Billed $150 per visit' with judge agree -> charge, pending 15000; 'Charge per visit $185' -> pending 49500", "grep -n except on reclassify.py (none)"],
 "verdict": "fail",
 "scores": {"no_rate_into_total_without_both_checks": 2, "code_check_strength": 2, "judge_gate": 4, "audit_trail": 3, "commit_scope": 1, "tests_kill_mutants": 5},
 "findings": [
  {"severity": "blocker", "title": "Restore after a rerun turns a current rate into a charge with neither check",
   "evidence": "app/backend/reclassify.py:102-104 (HEAD ec33bf0): restored = original == 'charge' and prior.get('previous_judge') is not None; if not restored skips _guard; carry_over reclassify.py:157-163 compares only text and value (line 160). Repro artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py -> 'RESTORE WITHOUT ANY CHECK -> charge restored= True pending total= 31000' after the rerun changed the sentence to 'Rate of $310 per visit.'",
   "why_it_matters": "D-042 requires code wording AND a judge re-check before a rate becomes a charge. The restore path uses a judge answer about the old sentence and skips the code check, so a figure the current code calls a rate enters the pending total. This breaks the brief's invariant, and the trigger (a classifier or lexicon change on rerun) is realistic.",
   "fix": "Allow the restore to skip the checks only if the rerun's code class still equals the class at demotion and the sentence is unchanged; otherwise re-run _guard. Compare the sentence or an excerpt hash in carry_over, not only text and cents.",
   "acceptance_test": "Demote, rerun with the flipped sentence, reclassify to charge with call=None: expect 422 (NO_CHARGE_WORDING or JUDGE_UNAVAILABLE), kind stays unclear, no reclassify event. Keep test_reclassify.py:80-87 passing for the unchanged-sentence restore."},
  {"severity": "blocker", "title": "Commit ec33bf0 silently deletes T-083's billing module, tests, route and API doc",
   "evidence": "git show --stat ec33bf0: 'app/backend/billing.py | 642 ----' and 'tests/unit/test_billing.py | 330 ----'; git ls-tree -r --name-only ec33bf0 | grep -i billing -> none, while f218263 has both; git show f218263:app/backend/api.py lines 497-498 (billing hook) replaced in ec33bf0 api.py; git show ec33bf0 -- memory/contracts/api.md removes the GET /api/cases/{token}/billing section; D-042 at memory/ORCHESTRATOR_DECISIONS.md:50 reinstates billing analysis",
   "why_it_matters": "The commit message describes only the reclassify feature. HEAD no longer serves the billing endpoint D-042 reinstates, and T-083's evidence (tests/unit/test_billing.py: 27 passed) cannot be reproduced at HEAD. Recoverable (files are on disk and in f218263), but not in any recorded decision.",
   "fix": "Restore billing.py, test_billing.py, the billing.add_routes hook and the api.md section in a commit under T-083, adding paths explicitly. If the removal was intended, record it in SCOPE_CUTS and ORCHESTRATOR_DECISIONS and update T-083 first. Do not rewrite history.",
   "acceptance_test": "git ls-tree -r --name-only HEAD | grep billing lists both files; tests/unit/test_billing.py passes at HEAD; GET /api/cases/{token}/billing returns 200 in a route test."},
  {"severity": "major", "title": "The code wording check accepts the rate phrase itself, so the judge is the only gate for 'Charge per visit $185'",
   "evidence": "app/backend/reclassify.py:24 _WORDING matches charges? and billed; probe-run.txt: 'wording(Charge per visit $185): Charge', 'wording(Billed $150 per visit): Billed', 'after judge agree: charge ... pending total cents: 15000' for 'Billed $150 per visit', and 'pending total cents = 49500' for the fixture rate; tests/unit/test_reclassify.py:108-116 (HEAD) asserts the rate reclassifies to charge on judge agreement",
   "why_it_matters": "The first independent gate is defeated by the sentence's own rate unit. D-042 is literally met, so this is a design weakness, not a written breach, but a $150-per-visit rate is summed as a billed charge on one LLM judge. If D-042 is read to exclude rate sentences, this becomes a blocker.",
   "fix": "Refuse the wording when the figure's sentence has a rate unit ('per', 'each', 'a visit', 'per unit', 'rate of') next to the figure. Keep the charge-wording check for statements of charge.",
   "acceptance_test": "charge_wording returns None and reclassify returns 422 NO_CHARGE_WORDING (judge not called) for 'Visit completed. Charge per visit $185.' and 'Visit completed. Billed $150 per visit.'; move the positive case at test_reclassify.py:108 to a sentence with no rate unit (e.g. 'Billed $185 for the visit.')."},
  {"severity": "minor", "title": "The reclassify audit row is stored with action 'edit'",
   "evidence": "app/backend/reclassify.py:22 AUDIT_ACTION = 'edit'; payload event 'reclassify' at reclassify.py:123; tests/unit/test_reclassify.py:215 asserts [e['action'] for e in ev] == ['edit']",
   "why_it_matters": "The audit event exists (AC met), but the action column reports a summary edit to anyone reading review_events directly.",
   "fix": "DB card adds 'reclassify' to the review_events CHECK (bump SCHEMA_VERSION per app/db/db.py:32), then flip the constant.",
   "acceptance_test": "GET /audit shows action 'reclassify' for the event; test_reclassify.py:215 asserts it."},
  {"severity": "minor", "title": "State change and audit row are separate writes (read from code, not reproduced)",
   "evidence": "app/backend/reclassify.py:120 (DB.update_item), :122 (review.batch_apply with its own BEGIN/COMMIT in db.py), :123 (_log INSERT)",
   "why_it_matters": "A failure after :120 leaves the item changed with no audit event, which the audit trail requirement does not allow.",
   "fix": "Write the change and the audit row in one transaction, as db.apply_review does.",
   "acceptance_test": "Inject a failure at _log and assert the item is unchanged."}
 ],
 "whats_right": [
  "Seven of seven scratch mutants of the reclassify guard are caught (judge gate, wording, negation, unsure accepted, audit, value, judge refusal as pass); artifacts/review-evidence/T-073-T-084/mutation-run.txt.",
  "Judge disagree, unsure or unavailable gives 422 with nothing changed and no event (tests/unit/test_reclassify.py:124-139).",
  "Demotion from charge to not-a-charge leaves the total unchanged, returns the item to pending and writes the audit (tests/unit/test_reclassify.py:59-70)."
 ],
 "questions_for_chris": [
  "Was removing app/backend/billing.py and tests/unit/test_billing.py in ec33bf0 an intended scope cut? If yes, it needs a SCOPE_CUTS entry and a D-042 update before T-083 closes; if no, it needs a restore commit (F2).",
  "Does D-042 let a rate sentence ('Charge per visit $185.') satisfy 'charged-amount wording'? My reading is no; the decision text does not say."
 ]}
```
