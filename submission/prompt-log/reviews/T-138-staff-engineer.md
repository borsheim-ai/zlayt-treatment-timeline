# T-138 staff-engineer-reviewer, round 1 (commit 89146b3)

Verdict: changes. No blocker. Undo of an edit now restores the AI wording together with its original judge result and state, and accept then export works in every sequence I ran. The acceptance criterion also names "code checks", and that part does not hold: the snapshot of the code-check record aliases the dict the edit then updates in place, so undo "restores" the edited wording's checks. The test cannot see it (mutant T3 survives).

Pin. `git rev-parse HEAD` at start was e25098d, at finish c4bb4da. `git diff --stat e25098d c4bb4da -- app/backend/review.py app/backend/present.py tests/unit/test_t138_undo_edit.py` is empty, so the code reviewed is the code at HEAD. Review copies are `git archive` extracts: `t134r3_c4bb` (c4bb4da, used for the final probes and the full suite) and `t134r3_fix` (e25098d plus a 2-line scratch stub for `conflict_candidates.checks()`, which that commit's HEAD lacked; see the T-134 r3 review for the cause). Probes and outputs: `artifacts/review-evidence/T-138/`.

Unit suite: `pytest tests/unit -q` on the c4bb4da archive: `3600 passed, 8 skipped in 208.23s`. The 11 failures reported in test_amounts*, test_t093 and test_t114 do not reproduce on any archive I built (no test_amounts or test_t093 failure; the e25098d archive failed 148 tests for a different reason, the missing `checks()`, and 3585 passed with the stub). The T-138 tests themselves: `7 passed` on every archive.

## Sequences probed (probe138.py, probe138b.py)

`python -I artifacts/review-evidence/T-138/probe138.py <archive>`; each ends with accept then export unless noted. All compare state, reasons, judge, code_checks, ladder state, wording, excerpt and review status to the pre-edit item.

| # | Sequence | Result |
|---|---|---|
| S1 | edit, undo, accept, export | pre-edit item restored, snapshot removed, accept 200, export 200, AI wording in the letter, edit wording not |
| S2 | edit, re-edit, undo | equals the item before the FIRST edit; accept and export 200 |
| S3 | quote-pick (excerpt only), undo | judge `supported -> unavailable -> supported`; excerpt and state restored; export 200 |
| S4 | edit, explicit accept, undo, accept | restored; export 200 |
| S5 | edit, accept, rejudge, undo | judge and checks restored; state `verified`; export 200 |
| S6 | edit, undo, edit, undo | both cycles equal the pre-edit item |
| S7 | edit, dismiss, undo | restored; export 200 |
| S8 | undo twice; undo of a never-edited accepted item | second undo a no-op; unedited item changes review status only |
| S9 | edit then undo on every entry of the sample (9) | 0 differ |
| S11 | needs_review entries | none exist in the sample, nothing to probe |
| S12 | old data with no snapshot | undo 200, behaves as before (judge stays `unavailable`), as documented |
| B | review layer with FakeCall: text case and OCR case, re-check supported | undo equals pre-edit item including `OCR_DERIVED` |
| B | state rewritten by another writer after the edit | judge restored, state left as the rewriter set it (by design, api.md); a restored `supported` judge then sits beside the edit's reasons. Constructed by a direct DB write, so I do not rate it |
| A | alias138.py: pre-edit code_checks differ from what the edit writes | FAILS, finding 1 |
| L | leak138.py: `pre_edit` in API payloads | FAILS, finding 2 |

Mutation (mutate_r3.py, stubbed e25098d archive, 253 tests per run, `artifacts/review-evidence/T-134/r3/mutants.txt`): T1 (no restore) KILLED by 5 tests, T2 (judge not restored) KILLED, T4 (state restore unconditional) KILLED, T5 (state never restored) KILLED, T6 (snapshot overwritten by every edit) KILLED, T7 (reasons not restored) KILLED, T3 (code_checks not restored) SURVIVED, T9 (snapshot not popped after restore) SURVIVED, T8 (ladder state not restored) SURVIVED but equivalent (`present._ladder` overwrites `ladder.state` from the row on every read), T10 (non-entry guard) SURVIVED but equivalent (only entries ever get a snapshot).

## Findings

```json
{"card": "T-138", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c4bb4da and e25098d (+scratch stub); app/backend/review.py (_edit, restore_pre_edit, apply_review), present.py (_ladder), tests/unit/test_t138_undo_edit.py; memory/contracts/api.md T-138 bullet; fixture backend, sample case evals/golden/sample.txt via TestClient; FakeCall review-layer probe incl. an OCR case; no served app",
 "exercised": [
  "read board show T-138 and T-134, reviews/T-134-staff-engineer-r2.md (the undo_accept repro), D-044, D-045, D-051, git show 89146b3 in full",
  "pytest tests/unit/test_t138_undo_edit.py + test_t134_unconfirmed_edit.py + test_trace.py on the stubbed e25098d archive: 110 passed",
  "pytest tests/unit -q on git archive c4bb4da: 3600 passed, 8 skipped; the 11 reported amounts/t093/t114 failures do not reproduce",
  "probe138.py: 12 undo sequences (edit/undo/accept, re-edit, quote-pick, accepted edit, rejudge, double cycle, dismiss, double undo, never-edited, 9-entry sweep, old data) with accept and export after each: only the leak check fails (artifacts/review-evidence/T-138/probe138.out)",
  "probe138b.py: review-layer undo with a FakeCall judge, text and OCR case, and a state rewritten after the edit",
  "alias138.py: edit with a pre-edit code-check record that differs from the edit's, then undo",
  "leak138.py: pre_edit key in GET case, item trace, case trace (metadata and full), judges",
  "mutate_r3.py: T1-T10 on the stubbed archive",
  "grep of review.py and present.py for pre_edit and the in-place code_checks update"
 ],
 "verdict": "changes",
 "scores": {"undo_restores_judge_and_state": 5, "accept_then_export_after_undo": 5, "code_check_record_restored": 1, "payload_hygiene": 3, "test_strength": 3},
 "findings": [
  {"severity": "major", "title": "The snapshot keeps an alias of the code_checks dict, so undo restores the edited wording's checks, not the original ones (AC says code checks are restored)",
   "evidence": "review.py:330-335 (c4bb4da): `lad['pre_edit'] = {'judge': lad.get('judge'), 'code_checks': lad.get('code_checks'), ...}` stores a reference, then `lad.setdefault('code_checks', {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=..., qualifier_carried=...)` mutates that same dict before DB.update_item serialises both. Repro: python -I artifacts/review-evidence/T-138/alias138.py <archive> (sample case; e3's stored code_checks set to qualifier_carried False and summary_tokens_not_in_excerpt ['5/10'], as for an AI draft that failed a check before she fixed it) prints `before edit: {'qualifier_carried': False, 'summary_tokens_not_in_excerpt': ['5/10']}`, `snapshot says: {'qualifier_carried': True, 'summary_tokens_not_in_excerpt': []} (should equal 'before edit')`, `after undo: {'qualifier_carried': True, 'summary_tokens_not_in_excerpt': []}`, `RESTORED code_checks == pre-edit: False`. Mutant T3 (do not restore code_checks at all) SURVIVES 253 tests, because the tests' sample edits leave the record unchanged, so the assertion `after['code_checks'] == before['code_checks']` holds either way. judge is not affected (it is replaced by assignment, T2 dies).",
   "why_it_matters": "The card's AC and the api.md bullet say undo restores the code-check record. For an AI wording that had failed a code check (state needs_review with SUMMARY_DROPS_QUALIFIER or similar, which the restore does bring back), the Why panel and the audit record would now say 'qualifier carried: yes' for text that dropped the qualifier. Accept stays safe because D-051 recomputes the checks from the wording, so nothing wrong reaches the letter; the damage is a wrong audit record beside a correct state, which is the kind of mismatch nobody can debug later.",
   "fix": "Snapshot with copy.deepcopy (judge and code_checks both), or build the snapshot dict from `dict(lad['code_checks'])` before the update. Add a test where the pre-edit code_checks differ from the edit's (set them in the DB as alias138.py does, or use a stored AI draft that failed a check).",
   "acceptance_test": "Unit: store qualifier_carried False on an AI entry, edit it to good wording, undo: ladder.code_checks equals the pre-edit record and state/reasons equal the pre-edit pair. Mutant T3 and the unsnapshotted-alias variant (drop the copy) must each fail a test."},
  {"severity": "minor", "title": "ladder.pre_edit is returned by GET /api/cases/{token}, although api.md calls it internal",
   "evidence": "present.py:28-33 `_ladder` copies the whole stored ladder. leak138.py after one edit: `case 200 pre_edit_present=True` with the old judge record and the old and new code_checks in the response; item trace, case trace (metadata and ?full=1) and /judges: False. memory/contracts/api.md T-138 bullet: 'kept in `ladder.pre_edit`, internal'. The frontend does not render it (timeline.js reads only backend, generator, code_checks, judge), so it is a contract and payload-hygiene miss, not a UI bug.",
   "why_it_matters": "The payload now carries the previous judge record and a second copy of the code checks for every edited entry; api.md tells the frontend it is internal, and any generic ladder renderer or export of the case view would show it.",
   "fix": "Drop `pre_edit` in `_ladder` (`lad.pop('pre_edit', None)`), or state in api.md that it is present and ignorable.",
   "acceptance_test": "Unit: after an edit, 'pre_edit' not in json.dumps(GET /api/cases/{token}); the undo tests still pass."},
  {"severity": "minor", "title": "Test gap: nothing fails if the snapshot is not removed after undo (mutant T9)",
   "evidence": "mutants.txt: `SURVIVED T9 snapshot kept after restore (not popped) | 253 passed`. `test_a_second_edit_after_an_undo_snapshots_again` passes with the stale snapshot because nothing changes between the two cycles. With T9 a second cycle would restore the FIRST cycle's judge and state even if a rejudge ran in between.",
   "why_it_matters": "The 'second edit snapshots again' behaviour is claimed and untested; the stale-snapshot path is a plausible sequence (undo, run the second check again, edit, undo).",
   "fix": "In that test change the state or judge between the cycles (for example via the rejudge route with a patched answer, or a DB write) and assert the second undo returns to the state after the first undo; also assert `'pre_edit' not in ladder` after undo.",
   "acceptance_test": "Mutant T9 fails a test."}
 ],
 "whats_right": [
  "Undo restores judge, state and reasons together: 12 sequences, accept then export 200 each time, JUDGE_NOT_RUN gone (the T-134 r2 undo_accept repro now passes).",
  "The restore is conservative: if something else rewrote the state after the edit, only the check result returns; a snapshot-less old row behaves exactly as before.",
  "A first edit keeps the snapshot across re-edits (S2, T6 dies), and the OCR invariant still holds after undo (probe B)."
 ],
 "questions_for_chris": []}
```
