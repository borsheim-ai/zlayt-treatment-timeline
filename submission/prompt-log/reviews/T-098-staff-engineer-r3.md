# T-098 staff-engineer-reviewer, round 3: D-051 choke point (commit 1335f21)

Verdict: **pass** (0 blockers, 0 majors, 1 minor, 1 nit). Every r2 finding is closed: the summary-only edit of a draft whose quote drops the hedge sentence is now a 422 and the stored reason survives, the gate and trace recompute all code checks, the notes withhold failing AI wording for edited originals and removed narrative sentences, and mutant M11 is killed. One narrow notes case is left (minor, finding 1).

Pinning: reviewed `git archive 1335f21`. HEAD moved to faee448 (T-087 r4, PDF files only) during the review; `git diff 1335f21 HEAD --stat` over review.py, trace.py, export.py, store.py, case_extras.py, narrative.py and app/db is empty, so nothing in scope changed.

## Checks asked for

1. **review.set_review is the single choke point.** `review.py:152-167` runs the check before `DB.apply_review` for any action that leaves an entry accepted or edited (`DB.ACTIONS.get(action) in ("accepted","edited")`), on the post-edit wording (`cand["edited"] = edited`, stored code reasons dropped so the new text counts). Callers: single accept/dismiss/reset (`review.py:~182`), edit incl. flag note (`_edit`, `review.py:285` and `:317`), batch write loop (`review.batch_apply` -> `set_review`). Grep of `apply_review|review_status` over app/ (archive): the only other `DB.apply_review` calls are `review.py:423` (flag reset), `:472` (`manual_entry`, `ACTIONS` value None = log only; the item is inserted pending and the S8 probe needs a separate accept), `:529` (`not_duplicate`, log only) and `pipeline.py:204` (flag reset). `db.add_item` and `db.update_item` raise on `review_status` or `edited` (`db.py:156`, `:203`). `pipeline._persist` (`:206-208`) carries an old accepted status over a rerun; that is the D-039 route, and the gate catches it (probe S6: gate ready False, export 422). No path sets accepted or edited without going through set_review, except that carry-over, which the gate covers.
2. **Quote that drops a hedge sentence.** Probe `T-098-staff-engineer-r3-probe.py` (results `...-r3-probe-results.txt`): real `generator.verify` gives `needs_review ['EXCERPT_OMITS_QUALIFIER']`; accept -> `422 CODE_CHECK_FAILED`, `next_action.code EDIT_QUOTE`; summary-only edit -> `422 CODE_CHECK_FAILED`, row stays `pending`, `state_reasons ['EXCERPT_OMITS_QUALIFIER']` (reason kept), `edited None`; batch accept [e8] -> 422, row pending; item trace verdict `needs_attention`, blocks_export True, failing step `excerpt_hedge` with `EDIT_QUOTE`; repair edit (quote with the hedge sentence plus a matching summary) -> 200, status `edited`.
3. **Gate and trace recompute all 5 checks.** r2 probe2 on the archive: quote cut to drop the hedge, forced accept -> `gate ready False, blockers [('e8','EXCERPT_OMITS_QUALIFIER')]`, `GET /export 422`, trace fails `excerpt_hedge`; quote starting mid-sentence -> `EXCERPT_NOT_WHOLE_SENTENCE`, export 422. Mutants M3a, M3b, M3d, M3e each fail a test (M3c, see finding 2).
4. **Notes never print failing AI wording.** r2 matrix probe on the archive: **63 checks, 0 failed**; S4 "internal notes contain the AI draft's invented token under EDITED ITEMS: False" for all verdicts and both token kinds; S9 `notes_print_removed_sentence false`; `letter_text` clean everywhere. M15 (edited originals) and M16 (narrative removed) each fail a test. One case remains (finding 1).
5. **M11 killed.** `code_check_failures` quote loop replaced by `[]`: `1 failed, 74 passed`, first failure `test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3`. Baseline 128 passed. 24 mutants run: 21 fail a test; survivors M2b (equivalent: the batch pre-check still refuses first), M3c and M11b (highlight, finding 2), M8 (equivalent: stored reasons duplicate the live check).

Across all routes, an invented token reaching the export: matrix of single accept, stale-pass accept, batch, edit, forced accept + gate, rerun after decisions, rejudge then accept, manual entry, narrative, times judge verdicts supported / unsupported / disagrees (partially), tokens "Pain 5/10" and "on the left": none reaches `letter_text`. Only the internal-notes case in finding 1 prints a token.

## Unit suite (archive of 1335f21)

`.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit`: **4 failed, 2023 passed, 4 skipped**. None relates to T-098 (1335f21 touches no file these tests cover):
- `test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git`: runs `git archive HEAD` inside a tree without `.git`; archive artefact (passes in the live repo).
- `test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts`: also fails in the live repo (T-093/T-101 area, seen in r2).
- `test_provider.py::test_single_call_path` and `test_provider_backends.py::test_single_call_path`: `app/backend/pdf_hidden.py` imports `subprocess` (T-087 r3, ae76835); also fail in the live repo. They belong to T-087, not T-098.

Targeted suite (trace, export, case_extras, date_unconfirmed): 128 passed.

## Findings

**F1 (minor, my reading). A removed narrative sentence that cites a non-accepted entry still prints in the internal notes, whatever it says.** `export.py` hides removed sentences only for the five `NARRATIVE_CODE_REASONS`; `NOT_AN_ACCEPTED_ENTRY` is printed as `Removed: "<text>"`. Probe (3): the narrative model returns `{"entry_id":"e99","text":"Pain was 9/10 on the left side."}`; `GET /export` 200, `letter has '9/10': False`, `notes has '9/10': True`: `- Removed: "Pain was 9/10 on the left side." (e99): NOT_AN_ACCEPTED_ENTRY.` The sentence was never code-checked (there is no quote to check against), so it is not a failed-check case under the commit's rule, but it is AI wording with an unsupported number printed in the export response, under the labelled do-not-send block. The letter is clean. Same family as r2 F3; the rule "no unsupported AI token anywhere in the export response" is Chris's call (question below).

**F2 (nit). The highlight half of the live recompute has no test.** Mutants M3c (`or "HIGHLIGHT_NOT_FOUND" in live` removed from the trace) and M11b (`HIGHLIGHT_NOT_FOUND` check in `code_check_failures` replaced by `if False`) both leave 128 passed. I could not find a route that reaches it with a verbatim quote, so it is probably unreachable today; a test with a quote that passes `check_excerpt` but fails `locate` would pin it, or the branch can be dropped.

## What I exercised

`git rev-parse HEAD`, `git log --oneline 1335f21..HEAD`, `git show 1335f21 -- app/ memory/contracts/api.md`, `git archive 1335f21` into two scratch copies (probes, mutants); full `tests/unit` on the archive and on the live repo for the four failures; r2 probes `T-098-staff-engineer-r2-probe.py` (63 checks, 0 failed), `...-r2-probe2.py`, `...-r2-probe3.py` on the archive; new `T-098-staff-engineer-r3-probe.py` and `T-098-staff-engineer-r3-mutants.py` (24 mutants); greps for `apply_review`, `review_status`, `INSERT`, direct state writes in `app/`; read `review.py`, `case_extras.py`, `trace.py`, `export.py`, `store.py`, `narrative.py`, `pipeline._persist`, `app/db/db.py`. Not scored: frontend copy (T-104); browser UI; real LLM backends (fixture only, by design).

```json
{"card": "T-098", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 1335f21 (D-051 single choke point set_review, gate and trace recompute of all code checks, notes withhold failing AI wording) on git archive 1335f21; HEAD moved to faee448 (PDF files only, nothing in scope changed); FastAPI TestClient with the fixture backend and scratch DB copies of the sample case; no app URL",
 "exercised": [
  "git rev-parse HEAD; git log --oneline 1335f21..HEAD; git diff 1335f21 HEAD --stat over review.py, trace.py, export.py, store.py, case_extras.py, narrative.py, app/db (empty)",
  "git show 1335f21 -- app/backend/*.py memory/contracts/api.md; read review.py set_review, code_check_failures, _edit, batch_apply, case_extras._check/apply_batch, trace._entry_steps/_finish, export._edited/_draft_paragraph/_pending, store.export_case, narrative.draft, pipeline._persist, app/db/db.py apply_review/add_item/update_item",
  "grep over the archive for apply_review, review_status writers, INSERT/REPLACE: only set_review plus flag reset (review.py:423, pipeline.py:204), log-only manual_entry and not_duplicate, and the D-039 carry-over in pipeline._persist",
  ".venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit on git archive 1335f21 -> 4 failed, 2023 passed, 4 skipped (eval_runner without .git; t093 fixture artefacts; two test_single_call_path on pdf_hidden.py subprocess import; none related to T-098; the last three also fail in the live repo)",
  "artifacts/review-evidence/T-098-staff-engineer-r2-probe.py on the archive: 63 checks, 0 failed (single/batch/edit/forced accept + gate/rerun/rejudge/manual entry/narrative x supported, unsupported, disagrees x 'Pain 5/10', 'on the left'); notes never print the token for edited originals and removed code-failing narrative sentences",
  "artifacts/review-evidence/T-098-staff-engineer-r2-probe2.py on the archive: hedge dropped and mid-sentence quote, forced accept -> gate ready False, export 422, trace fails excerpt_hedge / excerpt_whole_sentence",
  "artifacts/review-evidence/T-098-staff-engineer-r2-probe3.py and new T-098-staff-engineer-r3-probe.py on the archive: e8 quote drops hedge -> accept 422 EDIT_QUOTE, summary-only edit 422 with stored EXCERPT_OMITS_QUALIFIER kept and status pending, batch 422, item trace excerpt_hedge EDIT_QUOTE, repair edit 200; narrative sentence citing e99 with '9/10' printed in notes (F1)",
  "artifacts/review-evidence/T-098-staff-engineer-r3-mutants.py on a scratch copy: 24 mutants, baseline 128 passed; M11 killed; survivors M2b and M8 (equivalent), M3c and M11b (highlight, F2)"],
 "verdict": "pass",
 "scores": {"accept_guard_single_choke_point": 5, "batch_guard": 5, "edit_route_vs_accept_guard": 5, "gate_and_trace_recompute": 5, "notes_withhold_failing_wording": 4, "tests_pin_behaviour": 4},
 "findings": [
  {"severity": "minor", "title": "A removed narrative sentence citing a non-accepted entry prints in the internal notes with its unsupported number",
   "evidence": "artifacts/review-evidence/T-098-staff-engineer-r3-probe-results.txt: 'letter has 9/10: False | notes has 9/10: True' and the notes line '- Removed: \"Pain was 9/10 on the left side.\" (e99): NOT_AN_ACCEPTED_ENTRY.'; app/backend/export.py _draft_paragraph hides removed text only for NARRATIVE_CODE_REASONS, not NOT_AN_ACCEPTED_ENTRY.",
   "why_it_matters": "The commit states AI wording that failed a check is not printed anywhere in the export; this sentence could not be checked against any quote and is printed with an unsupported figure. It sits in the labelled do-not-send block and the letter is clean, so I rate it minor and leave the rule to Chris.",
   "fix": "Print removed narrative text only when its reason is a judge reason; for NOT_AN_ACCEPTED_ENTRY print 'AI wording removed (cited entry is not accepted)' without the text, or record in DECISIONS that the notes may show removed AI text as an audit trail.",
   "acceptance_test": "Unit: narrative draft with a sentence citing a non-accepted entry id and containing '9/10'; accept the paragraph with another valid sentence; export: internal_notes_text has no '9/10'. Mutation: restoring the plain print fails it."},
  {"severity": "nit", "title": "HIGHLIGHT_NOT_FOUND live recompute is not pinned by any test",
   "evidence": "artifacts/review-evidence/T-098-staff-engineer-r3-mutants-results.txt: 'M3c trace highlight live term off -> 128 passed <-- SURVIVED' and 'M11b code_check_failures: highlight check off -> 128 passed <-- SURVIVED'",
   "why_it_matters": "A regression in this branch stays green; I found no route that reaches it with a verbatim quote, so it may be dead code.",
   "fix": "Add a test with a quote that passes check_excerpt but fails grounding.locate, or remove the branch.",
   "acceptance_test": "Mutants M3c and M11b make a new test fail, or the branch is gone."}
 ],
 "whats_right": [
  "set_review runs the five-check recompute on the post-edit wording before any write, so accept, edit (including summary-only), batch and reset share one guard and a refused edit leaves the row and its stored reason untouched (M1, M1b, M1c, M11, M17 each fail a test).",
  "A quote-level failure now says EDIT_QUOTE in the 422, the item trace and the gate, and a stale stored pass cannot hide it (M3a, M3b, M3d, M13 fail a test).",
  "The new tests assert behaviour through the real API (status codes, stored reasons, absence of the token from the whole export response) and 21 of 24 mutants break one."],
 "questions_for_chris": [
  "F1: may the internal notes show removed AI narrative text that was never checked against a quote (cited entry not accepted), or must the whole export response be free of unsupported AI numbers?"]}
```
