# T-138 staff-engineer-reviewer, round 2 (commit b7a7ead, undo snapshot fix-up)

Verdict: pass. No blocker, no major. The three round-1 findings are fixed: undo now restores the pre-edit `code_checks` (the alias probe is green on HEAD and red on the parent), `pre_edit` is in none of 51 payloads, and the mutants round 1 said survived (T3, T9) now die, along with the alias and the leak. One nit: the restore treats an absent pre-edit `code_checks` differently from an absent `judge`.

Pin. `git rev-parse HEAD` was 4f416a4 at the start (b7a7ead is its ancestor and the T-138 change is in it). HEAD was 2db6ad2 when I checked again. I tested `git archive 4f416a4` and repeated the unit tests, the alias probe and the leak scan on `git archive 2db6ad2`: same results. The in-scope diff between those two commits does not touch review.py, present.py or the T-138 tests.

## What the brief asked

| Check | Result | Evidence |
|---|---|---|
| Undo restores the pre-edit `code_checks` (deep copy) | Holds | `alias138_head.out` (4f416a4): `after undo: {'qualifier_carried': False, 'summary_tokens_not_in_excerpt': ['5/10']}`, `RESTORED code_checks == pre-edit: True`. Same on 2db6ad2 (`alias138_2db6ad2.out`). Control on the parent 68b8685 (`alias138_parent_control.out`): `RESTORED ... False`, so the probe does discriminate. The fix is `copy.deepcopy` at review.py:355-356. |
| T3 killed | Yes | `T-134/r4/mutants.txt`: `KILLED T3 restore drops the code_checks`, 1 failed (`test_undo_restores_the_pre_edit_code_checks_not_the_edited_wordings`). |
| T9 killed | Yes | `mutants.txt`: `KILLED T9 snapshot kept after restore (not popped)`, 1 failed (`test_second_undo_cycle_restores_what_the_item_had_after_the_first_undo_and_the_snapshot_is_gone`). |
| `pre_edit` in no payload | Holds | `leak138r2.out`: 48 GET responses (16 routes at three stages: after the first accept, after the edit, after undo) plus the edit, reset and accept review responses: `ANY payload contained pre_edit: False`. Stored ladder still holds it until undo, then not. Control on 68b8685 (`leak138r2.out` run against that archive): `pre_edit=True` on GET case, GET item, and the review responses. Mutant L1 (present._ladder keeps it) is KILLED. |
| Round-1 probe sequences | 0 problems | `probe138_4f416a4.out`: `TOTAL PROBLEMS 0` (S1 to S12). |
| Unit tests | Pass | `pytest -q -p no:cacheprovider tests/unit/test_t138_undo_edit.py` (11 collected) passes on 4f416a4 and 2db6ad2; with the T-134 file, 37 passed (`unit_runs.txt`). |

## Findings

Only the nit below. Mutants A1 (no deep copy, `mutants.txt`: `KILLED A1`), T3, T9 and L1 each fail at least one test, so the protection is tested, not just the code.

## Evidence

Under `artifacts/review-evidence/T-138/r2/`: `alias138_head.out`, `alias138_2db6ad2.out`, `alias138_parent_control.out`, `leak138r2.py` and `leak138r2.out`, `probe138_4f416a4.out`. The mutation log is `artifacts/review-evidence/T-134/r4/mutants.txt` (shared runner `mutate_r4.py`). The alias script is the round-1 `artifacts/review-evidence/T-138/alias138.py`, unchanged.

```json
{"card": "T-138", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive 4f416a4 (contains commit b7a7ead; HEAD at start) and 2db6ad2 (HEAD at finish, same results): app/backend/review.py (_edit, restore_pre_edit), present.py (_ladder), tests/unit/test_t138_undo_edit.py; memory/contracts/api.md T-138 bullet; fixture backend, sample case via TestClient; parent 68b8685 as a positive control; no served app",
 "exercised": [
  "read reviews/T-138-staff-engineer.md (round 1), board show T-138 (AC and notes), git show b7a7ead in full (review.py, present.py, tests/unit/test_t138_undo_edit.py)",
  "read review.py _edit (lines 353-364) and restore_pre_edit (373-399), present.py _ladder (28-34), in the 4f416a4 archive",
  ".venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t138_undo_edit.py on git archive 4f416a4 and 2db6ad2; with test_t134_unconfirmed_edit.py: 37 passed",
  "python -I artifacts/review-evidence/T-138/alias138.py on 4f416a4 (RESTORED True), 2db6ad2 (True) and the parent 68b8685 control (False)",
  "leak138r2.py (ZLAYT_MODE=local, sample case): 48 GET responses and 3 review responses scanned for pre_edit on 4f416a4 (none) and on 2db6ad2 (none); control 68b8685 (pre_edit present)",
  "probe138.py (round-1 suite, 12 undo sequences with accept and export after each) on 4f416a4: TOTAL PROBLEMS 0",
  "mutate_r4.py on 4f416a4 (7 modules, one pre-existing red test deselected): A1 KILLED, T3 KILLED, T9 KILLED, L1 KILLED, plus the T-134 mutants (N18, N19, N21, N22, H2, P1 all KILLED); log artifacts/review-evidence/T-134/r4/mutants.txt",
  "grep in review.py: judge restore at 381-384 has an else branch (pop), code_checks restore at 385-386 has none; writers of ladder code_checks: generator.py:61, pipeline.py:31, review.py:580 (all write a dict)"
 ],
 "verdict": "pass",
 "scores": {"undo_restores_judge_and_state": 5, "code_check_record_restored": 5, "accept_then_export_after_undo": 5, "payload_hygiene": 5, "test_strength": 4},
 "findings": [
  {"severity": "nit",
   "title": "The restore treats an absent pre-edit code_checks differently from an absent judge: the edit's record stays",
   "evidence": "review.py:381-384 restores judge and pops it when the snapshot has none; review.py:385-386 restores code_checks only `if snap.get('code_checks') is not None`, with no else. An edit then writes code_checks (review.py:360), so an item whose pre-edit ladder had no code_checks key keeps the edited wording's check results after undo. No current writer leaves the key absent (generator.py:61, pipeline.py:31 and review.py:580 always write a dict), so this is reachable only from data written before that, and I did not reproduce it.",
   "why_it_matters": "Low: the same class of wrong record as round 1, but on an edge no current writer produces. Worth fixing so the two restores do not diverge.",
   "fix": "Mirror the judge branch: if the snapshot's code_checks is None, pop the key on restore.",
   "acceptance_test": "Unit: remove code_checks from the item's ladder, edit it, undo: 'code_checks' not in the restored ladder; the judge case is already covered by test_t138."},
  {"severity": "nit", "title": "unit_runs label", "evidence": "n/a", "why_it_matters": "n/a", "fix": "n/a", "acceptance_test": "n/a"}
 ],
 "whats_right": [
  "The alias is gone: copy.deepcopy at review.py:355-356 snapshots judge, code_checks and rejudge, and the parent control shows the old bug (RESTORED False) on the same probe.",
  "pre_edit is hidden in the one place it leaks (present.py:33 pop in _ladder): 51 payloads across 16 routes and the review responses are clean after edit, undo and accept, and the control shows the leak before the fix.",
  "The snapshot is removed on undo (review.py:378, `snap = lad.pop`), so a second cycle snapshots what the item holds then, and the rerun attempts come back exactly (review.py:387-390)."
 ],
 "questions_for_chris": []}
```
