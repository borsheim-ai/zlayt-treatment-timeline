# T-138 staff-engineer-reviewer, round 2b (amends reviews/T-138-staff-engineer-r2.md)

Verdict unchanged: pass. This file replaces the r2 file's JSON findings array and corrects two statements in the r2 body. The r2 file cannot be edited under the reviewer write guard, so this is the record to use.

Corrections to the r2 file:

1. Pin paragraph. The r2 file says the diff from 4f416a4 to 2db6ad2 "does not touch review.py, present.py or the T-138 tests". That is wrong for present.py: `git diff 4f416a4 2db6ad2 -- app/backend/present.py` changes `_why` (takes the judge record) and `_common` (passes it). The `_ladder` function, where the pre_edit pop lives (present.py:33), is unchanged, so the T-138 results hold. The alias probe, the leak scan and the unit tests were re-run on 2db6ad2 with the same results (`alias138_2db6ad2.out`: RESTORED True; leak scan: ANY payload contained pre_edit: False; 37 passed).
2. Unit tests. The r2 file says the T-138 file (11 tests) passes on both archives. I ran it together with test_t134_unconfirmed_edit.py: 37 passed on 4f416a4 and on 2db6ad2. The T-138 file alone was not run separately; its 11 tests are included in those 37.
3. Findings array. The r2 JSON contains a second, empty "nit" entry ("unit_runs label", evidence "n/a"). It is not a finding and breaks the evidence rule. It is removed here. The one real nit (the code_checks asymmetry) is kept.

Evidence for the findings is unchanged: `artifacts/review-evidence/T-138/r2/` and `artifacts/review-evidence/T-134/r4/mutants.txt`.

```json
{"card": "T-138", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive 4f416a4 (contains commit b7a7ead; HEAD at start) and 2db6ad2 (HEAD at finish, same results): app/backend/review.py (_edit, restore_pre_edit), present.py (_ladder; _why and _common changed upstream, not _ladder), tests/unit/test_t138_undo_edit.py; memory/contracts/api.md T-138 bullet; fixture backend, sample case via TestClient; parent 68b8685 as a positive control; no served app",
 "exercised": [
  "read reviews/T-138-staff-engineer.md (round 1), board show T-138 (AC and notes), git show b7a7ead in full",
  "read review.py _edit (353-364) and restore_pre_edit (373-399), present.py _ladder (28-34), in the 4f416a4 and 2db6ad2 archives; git diff 4f416a4 2db6ad2 -- app/backend/present.py",
  ".venv/bin/python -I -m pytest -q -p no:cacheprovider on test_t138_undo_edit.py and test_t134_unconfirmed_edit.py: 37 passed on 4f416a4 and on 2db6ad2",
  "python -I artifacts/review-evidence/T-138/alias138.py on 4f416a4 (RESTORED True), 2db6ad2 (True) and the parent 68b8685 control (False)",
  "leak138r2.py (ZLAYT_MODE=local, sample case): 48 GET responses and 3 review responses scanned for pre_edit on 4f416a4 and 2db6ad2 (none); control 68b8685 (pre_edit present)",
  "probe138.py (round-1 suite, 12 undo sequences with accept and export after each) on 4f416a4: TOTAL PROBLEMS 0",
  "mutate_r4.py on 4f416a4 (7 modules, one pre-existing red test deselected): A1 KILLED, T3 KILLED, T9 KILLED, L1 KILLED, plus the T-134 mutants N18, N19, N21, N22, H2, P1 all KILLED; log artifacts/review-evidence/T-134/r4/mutants.txt",
  "grep in review.py: judge restore at 381-384 has an else branch (pop); code_checks restore at 385-386 has none; writers of ladder code_checks: generator.py:61, pipeline.py:31, review.py:580 (all write a dict)"
 ],
 "verdict": "pass",
 "scores": {"undo_restores_judge_and_state": 5, "code_check_record_restored": 5, "accept_then_export_after_undo": 5, "payload_hygiene": 5, "test_strength": 4},
 "findings": [
  {"severity": "nit",
   "title": "The restore treats an absent pre-edit code_checks differently from an absent judge: the edit's record stays",
   "evidence": "review.py:381-384 restores judge and pops it when the snapshot has none; review.py:385-386 restores code_checks only `if snap.get('code_checks') is not None`, with no else. The edit then writes code_checks (review.py:360), so an item whose pre-edit ladder had no code_checks key keeps the edited wording's check results after undo. No current writer leaves the key absent (generator.py:61, pipeline.py:31 and review.py:580 always write a dict), so this is reachable only from data written before that; I did not reproduce it.",
   "why_it_matters": "Low: the same class of wrong record as round 1, on an edge no current writer produces. Worth fixing so the two restores do not diverge.",
   "fix": "Mirror the judge branch: if the snapshot's code_checks is None, pop the key on restore.",
   "acceptance_test": "Unit: remove code_checks from the item's ladder, edit it, undo: 'code_checks' not in the restored ladder."}
 ],
 "whats_right": [
  "The alias is gone: copy.deepcopy at review.py:355-356 snapshots judge, code_checks and rejudge, and the parent control shows the old bug (RESTORED False) on the same probe.",
  "pre_edit is hidden where it leaked (present.py:33, pop in _ladder): 48 GET responses across 16 routes and 3 review responses are clean after edit, undo and accept, and the control shows the leak before the fix.",
  "The snapshot is removed on undo (review.py:378, `snap = lad.pop`), so a second cycle snapshots what the item holds then, and the rerun attempts come back exactly (review.py:387-390)."
 ],
 "questions_for_chris": []}
```
