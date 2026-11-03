# Subagent: Backend: T-134 round 2 (Backend: T-134 round 2)

Source: `agent-a4dce4549d9aa3b82.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T12:43:02.832Z

You are a backend worker in /Users/arsis/zlayt-pm-project on board card T-134, round 2. Claim it with `python3 tools/board.py claim T-134 --agent backend --force`, then read reviews/T-134-staff-engineer.md.

**Major.** The per-item trace still says "Accepted by you" for an edit that is still open (edit_to_check). The trace must state it honestly, for example "Edited by you; not yet confirmed (reason)", the same as the gate and notes.

Also kill the 4 surviving mutants and fix the 3 minors.

**Do not touch** lexicon_scan.py, summary_trim.py, lexicon.yaml or the conflict code; other workers are in them. A frontend worker is reading `edit_to_check` (T-136), so keep the contract stable and update memory/contracts/api.md if the trace wording or fields change.

**Steps:**
1. Write the tests first, then make the fix, then run the full unit suite.
2. Commit with a pathspec: run `git add <paths>`, then `git commit -m msg -- <paths>` as a separate command.
3. Write the handoff and move the card to in_review.

Reply in 3 lines.

### User / tool · 2026-11-02T12:43:02.837Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:06.426Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-134 --agent backend --force; cat reviews/T-134-staff-engineer.md; python3 tools/board.py show T-134 | tail -60"
}
````

### User / tool · 2026-11-02T12:43:06.664Z

**tool result**
````
T-134 claimed by backend
# T-134 staff-engineer-reviewer, round 1 (commit 5fb338d)

Verdict: changes. No blocker. One major: the per-item trace still says "Accepted by you" for an edit that is still open.

Pin: I made `git archive` of 5fb338d (HEAD when I started; HEAD then moved to bea3984, but `git diff --stat 5fb338d HEAD -- app/backend/review.py trace.py store.py export.py` is empty, so the code under review is unchanged). Parent for comparison: `git archive 5fb338d^` = f939ccb. Probe scripts and outputs are in `artifacts/review-evidence/T-134/`.

## What the card asked, checked one by one

| Check | Result | Evidence |
|---|---|---|
| Edited entry still needs_review never reaches the letter, never counts accepted, notes do not say accepted | holds | `paralegal_view.py` (HTTP, served copy): letter has only record 1; `excluded {'pending': 22, 'edit_not_confirmed': 1}`; EDITED ITEMS says "edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter". `probe134g.py`: also absent from `?style=oneline`; RECORDS NOT IN THE TREATMENT SECTION lists it "edited, not yet confirmed against the quote". |
| Explicit accept with wording that fails a code check is 422 | holds | `probe134e.py`: old data tampered to "9/10"; accept -> `422 CODE_CHECK_FAILED`; gate `ready False ['SUMMARY_TOKEN_NOT_IN_EXCERPT']`; export 422. A fresh edit with a bad figure is also 422 (probe134.py S9). Mutant M17 (accept skips the check) is killed. |
| gate.ready equals export-allowed | holds in every probed state | `probe134.py` checks `gate.ready == (export 200)` after every step of 9 sequences; 0 problems. |
| Spanish and OCR edits need an explicit accept | holds | Spanish: `test_api_spanish_case_end_to_end_label_edit_export` (passes). OCR: `probe134d.py` on an OCR case with a judge that answers "supported": after edit `edited needs_review ['OCR_DERIVED'] edit_to_check=True`, edited text not in letter; after accept it is in the letter and the notes keep "still marked for review (OCR_DERIVED)". |
| 8+ edit and accept sequences | 10 probed, 0 invariant breaks | edit; edit-undo; edit-undo-reedit; edit-accept-edit; edit-accept-undo; edit-dismiss; accept-edit; edit twice; two edits then accept one; quote-picker (summary+excerpt) edit; batch accept on an open edit is refused (not pending). |
| Unit suite | 3318 passed, 4 skipped, 182.8 s | `pytest tests/unit -q` in the archive copy (handoff said 3298; I did not find why the count differs). |

## The 5 changed existing tests

- `test_spanish_records.py:359-364`: correctly updated and stronger (asserts the edit is open, not in the letter, then explicit accept, then in the letter).
- `test_trace.py:~867` and `~1100`: correctly updated (they now assert NOTHING_ACCEPTED plus the warning, then accept, then ready and export 200).
- `test_trace.py:1004-1015` (`test_an_edited_item_counts_as_accepted_for_the_judge_blocker`): weakened. After the change the item is accepted before the final assertion, so the `edited` arm of `judge_not_run_blockers` (trace.py:821) is no longer exercised. Mutant M16 (arm reduced to `("accepted",)`) survives 269 tests. The docstring still says "status 'edited' blocks like 'accepted'". The new check is also behind an `if state == "needs_review":` so it can skip silently. See finding 3.
- `test_trace.py:1075`: loosened by `if b["item_id"]`, which hides any extra case-level blocker. See finding 3.

## Mutation spot-check (scratch copy, tests: t134, trace, spanish, ocr_invariant, export, export_edge, review_rules, api_routes)

Killed (13): M1 rule off, M2 status not flipped, M3 excerpt edits not covered (killed only by the changed test_trace test, not by the new file), M4 judge blocker on open edit, M5 warning dropped, M6 NOTHING_ACCEPTED counts open edit, M8 notes say accepted, M9 excluded count removed, M10 gate accepted count, M11 `_was_edited`, M13 reason lost after accept, M14 view flag false, M17 accept skips code check.
Survived (4): M7 `ready_to_export` ignores the open edit (present.py:206), M12 case-trace review step EDIT_NOT_CONFIRMED branch removed (trace.py:1025), M15 verdict label ignores the open edit (trace.py:1062), M16 above. M18 anchor matched twice, so it did not run.

## Paralegal view (served copy, port 7947, fixture backend curated, ZLAYT_MODE=local, scratch DB; listener PID 52680 checked with `ps` and `lsof`, then killed by that PID)

Steps: sample case, run, accept record 1, edit record 3 ("Persistent neck pain 6/10 with daily headaches noted."), export without accepting.
- Row (screenshot `artifacts/review-evidence/T-134/ui-after-edit.png`): "Needs review | Edited", a primary button "I compared it with the quote", and "Still marked Needs review ... Until then it counts as open." Header "1 of 23 decided", chip "1 edit to check", "Ready to export, 22 not reviewed". Honest.
- Letter: one entry (record 1). The edit is not there. Honest.
- Notes: "Items not reviewed: 22" counts the edit; EDITED ITEMS and PENDING ITEMS NOT INCLUDED both say second check not available and not in the letter. After pressing accept (API), the letter carries the edit and the notes say "accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE)". Honest.
- Not honest: "Why this status" for that row (item trace) says "Accepted by you" / "You edited this item and accepted it." (finding 1). And the case checks banner says "What you need to do: The second AI check did not run on 1 item. Run it again; accepted items it never checked cannot go in the letter." although nothing is accepted and the item is out of the letter (finding 4; same text at the parent f939ccb).

## Right already
- One rule (`review.edit_unconfirmed`) feeds the item view, counts, export, gate and notes; gate and export never disagreed in 10 sequences.
- Accept stays bound by the code checks (D-051) and a Spanish/OCR edit needs her explicit accept; the notes keep the reason code after she accepts.

```json
{"card": "T-134", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 5fb338d (app/backend review.py, store.py, export.py, present.py, trace.py, api.py; tests t134 + 4 changed tests); parent f939ccb for comparison; served copy http://127.0.0.1:7947 (fixture backend, curated, ZLAYT_MODE=local); sample case evals/golden/sample.txt",
 "exercised": [
  "read board show T-134, D-044, D-045, D-051, D-053, reviews/T-060-paralegal-pass4.md M2, git show 5fb338d in full",
  "pytest tests/unit -q on git archive 5fb338d: 3318 passed, 4 skipped",
  "probe134.py: 9 edit/accept/undo/dismiss sequences, invariant checks after each (artifacts/review-evidence/T-134/probe134.py)",
  "probe134c.py: quote-picker edit (summary+excerpt), excerpt-only 422s, item trace, batch accept route",
  "probe134d.py: OCR-derived entry edit with a supporting judge, export before and after accept",
  "probe134e.py: stored wording failing a code check: accept 422, gate vs export 422",
  "probe134g.py: standard and oneline export, RECORDS NOT IN THE TREATMENT SECTION, narrative route",
  "mutation runs M1-M17 on a scratch copy (13 killed, 4 survived)",
  "served the archive copy on port 7947, ran paralegal_view.py, steps134.py, shot134.py (Playwright screenshot), killed PID 52680",
  "judges_step134.py on f939ccb and 5fb338d: judges step FAIL with an open edit exists at the parent"
 ],
 "verdict": "changes",
 "scores": {"export_honesty": 4, "gate_export_agreement": 5, "code_check_binding": 5, "test_strength": 3, "state_consistency_across_surfaces": 3},
 "findings": [
  {"severity": "major", "title": "Item trace still says an open edit was accepted",
   "evidence": "app/backend/trace.py:247-248 returns step human PASS 'You edited this item and accepted it.' for review_status edited; trace.py:281-282 sets verdict {'code':'accepted','label':'Accepted by you'}. Neither calls review.edit_unconfirmed. Repro: artifacts/review-evidence/T-134/paralegal_view.py http://127.0.0.1:7947 prints \"ITEM TRACE verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}\" and \"[('human', 'pass', 'You edited this item and accepted it.')]\" right after the edit, while export excludes the entry and the gate warns EDIT_NOT_CONFIRMED. The frontend renders this verdict (app/frontend/stepper.js:411, 'Why this status').",
   "why_it_matters": "Paralegal pass 4 M2 was exactly this contradiction: the app says accepted while the row, the letter and the notes say it is open. T-134 fixed the letter, gate and notes but left the item's own audit trail claiming her acceptance, which is the text she (or opposing counsel) would read as the record of what she decided.",
   "fix": "In trace.py _human_step and the item verdict (lines 247 and 281), branch on review.edit_unconfirmed(kind, row): human step PENDING with 'You edited this item; it is not accepted until you compare it with the quote and accept', reason EDIT_NOT_CONFIRMED, next_action DECIDE; verdict code 'edit_to_check', label 'Edited; waiting for your check'. Keep the 'accepted' wording only for review_status accepted.",
   "acceptance_test": "Fixture case, edit e3 with no judge fixture, GET /items/e3/trace: verdict.code != 'accepted', 'Accepted' not in verdict.label, human step status 'pending'. After POST accept: verdict.code == 'accepted'. Mutant: revert the branch and the test fails."},
  {"severity": "minor", "title": "Three agreed surfaces have no test that fails when they break",
   "evidence": "Mutants M7 (present.py:206 drop the edit_to_check clause of ready_to_export), M12 (trace.py:1025 remove the EDIT_NOT_CONFIRMED review-step branch) and M15 (trace.py:1062 drop n_edit from the verdict label) all SURVIVE: '309 passed' for each across test_t134, test_trace, test_spanish_records, test_ocr_invariant, test_export, test_export_edge, test_review_rules, test_api_routes. tests/unit/test_t134_unconfirmed_edit.py only asserts ready_to_export False in a case that is already False because pending > 0 (line 55).",
   "why_it_matters": "The card's point is that several places agree. The review step text, the 'Ready to export (N not reviewed)' label the paralegal sees in the header, and the API field can regress without a red test.",
   "fix": "Add assertions: with every other item decided and one open edit, review.ready_to_export is False and the case-trace review step is pending with reason EDIT_NOT_CONFIRMED; verdict.label contains '(1 not reviewed)' when nothing else is pending.",
   "acceptance_test": "Re-run mutants M7, M12, M15 (reverse each edit above in a scratch copy); each makes at least one test fail."},
  {"severity": "minor", "title": "One existing test was weakened and one loosened",
   "evidence": "tests/unit/test_trace.py:1004-1015 test_an_edited_item_counts_as_accepted_for_the_judge_blocker now accepts the item before its last assertion, so the review_status 'edited' arm at trace.py:821 is untested: mutant M16 (arm changed to (\"accepted\",)) survives with '269 passed'. The new guard at line 1012 is `if ... state == \"needs_review\":`, which skips silently if the state differs, and the docstring (line 1005) still says \"status 'edited' blocks like 'accepted'\". tests/unit/test_trace.py:1075 adds `if b[\"item_id\"]`, which stops the list check from catching an extra case-level blocker. The new test file has no excerpt-only edit case; M3 is killed only by the changed test_trace test.",
   "why_it_matters": "A D-044 gate arm lost its proof when the test was bent to fit the new rule, and the guard can pass without running its assertions.",
   "fix": "Keep the old case and add a second one for an edited, unjudged, non-needs_review entry (or a flag note edit) that still blocks; make line 1012 an unconditional assert; assert the exact blocker list [(edt, 'SUMMARY_DROPS_QUALIFIER'), (None, 'NOTHING_ACCEPTED')] at line 1075; add a t134 test that an excerpt-only edited entry is edit_to_check.",
   "acceptance_test": "Mutants M16 and M3 each fail a test in test_t134_unconfirmed_edit.py or test_trace.py."},
  {"severity": "minor", "title": "Case-checks banner still tells her to re-run a check for an item that is out of the letter",
   "evidence": "Pre-existing at f939ccb (artifacts/review-evidence/T-134/judges_step134.py prints the same line for the parent and for 5fb338d): 'judges fail | 1 item has not been double-checked ...' with counts unavailable 1, after the edit, while gate is pass. Screenshot artifacts/review-evidence/T-134/ui-after-edit.png: 'What you need to do: The second AI check did not run on 1 item. Run it again; accepted items it never checked cannot go in the letter.' The unit test test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean asserts unavailable == 0, which passes only with the default fixture set, not with FIXTURE_SET=curated.",
   "why_it_matters": "With T-134 the edit is not accepted and not in the letter, so the banner's reason ('accepted items') is false and it asks for a re-run that D-045(b) says a human edit does not need. Not introduced by this commit; it sits next to the M2 fix and the paralegal reads it in the same header.",
   "fix": "Exclude human-authored edits (D-045b) from the judges step unavailable count, or word the banner for the open-edit case; then run the test under FIXTURE_SET=curated too.",
   "acceptance_test": "FIXTURE_SET=curated, edit e3: case trace judges step is not 'fail' and its counts.unavailable == 0."},
  {"severity": "nit", "title": "Unrelated route-order swap in the same commit",
   "evidence": "app/backend/api.py:509-512 in the diff: billing.add_routes and pdf_routes.add_routes exchanged places; neither the card, the handoff nor the commit message mentions it.",
   "why_it_matters": "A behaviour change in route registration order hides inside a fix commit. The 3318-test suite is green, so I found no breakage; this is a process note.",
   "fix": "Say why in the handoff, or revert it.",
   "acceptance_test": "Handoff or commit message names the reason."}
 ],
 "whats_right": [
  "One rule (review.edit_unconfirmed) feeds the item view, counts, export, gate and notes; gate.ready equalled export-allowed in all 10 probed sequences.",
  "Accept stays bound by the D-051 code checks (422 CODE_CHECK_FAILED, nothing written), and Spanish and OCR edits need her explicit accept with the reason code kept in the notes.",
  "The letter, notes and row are honest in the paralegal run: the edit is out of the letter, counted in 'Items not reviewed', and the notes never say accepted."
 ],
 "questions_for_chris": []}
```
---
id: "T-134"
title: "Export: an edited entry still marked needs_review is in the letter and the notes say it was accepted (paralegal pass 4 M2; UI now counts it as open, backend gate/notes need to agree)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T12:05:26Z"
updated_at: "2026-11-02T12:43:06Z"
claimed_by: "backend"
claimed_at: "2026-11-02T12:43:06Z"
rounds: 1
commits: ["5fb338d"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-134-staff-engineer.md", "at": "2026-11-02T12:42:58Z"}
ac:
  - {"n": 1, "text": "Repro (fixture, sample case): POST /api/cases {sample:true}; run; POST items/<e3>/review {action:edit, edits:{summary:'Persistent neck pain 6/10 with daily headaches noted.'}} -> 200 item.review_status=edited, state=needs_review, reasons=[JUDGE_UNAVAILABLE], review.counts.edited=1. Then GET export -> 200 and letter_text carries the edited wording; trace export_gate ready=true, blockers=[], warnings only ITEMS_NOT_REVIEWED. internal_notes_text says 'every item in the treatment section was accepted by the paralegal'. Decide with the orchestrator against D-045b (judge never blocks a human edit) and make the three places agree: (a) the gate lists an edited-and-needs_review entry as a warning EDIT_NOT_CONFIRMED (or blocker) until the paralegal accepts it, (b) export counts/excluded name it, (c) the notes EDITED ITEMS line says 'edited; second check not available' (reason code JUDGE_UNAVAILABLE) instead of 'accepted by the paralegal'. The UI (T-131/T-060 r5) already counts such an entry as open and gives it an 'I compared it with the quote' Accept; it asks before copying.", "done": true, "evidence": "tests/unit/test_t134_unconfirmed_edit.py (6 tests) + full unit suite 3298 passed: repro e3 edit -> out of letter/items/counts, gate EDIT_NOT_CONFIRMED warning, notes 'edited; second check not available (JUDGE_UNAVAILABLE)', accept stays 422 on code-check failure"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T12:18:06Z orchestrator: assigned: backend
- 2026-11-02T12:18:23Z backend: claimed
- 2026-11-02T12:24:22Z backend: Implemented: review.edit_unconfirmed (one rule); item.edit_to_check, review.counts.edit_to_check, gate warning EDIT_NOT_CONFIRMED (not a blocker: out of letter like pending), export treats as pending (out of letter/items/counts), notes EDITED/PENDING lines say second check not available. Accept stays bound by D-051 (422). Tests tests/unit/test_t134_unconfirmed_edit.py. Full unit suite running. Open point: frontend ZL.editToCheck is summary-only; excerpt-only edits need edit_to_check (contract note).
- 2026-11-02T12:31:49Z backend: AC 1 checked: tests/unit/test_t134_unconfirmed_edit.py (6 tests) + full unit suite 3298 passed: repro e3 edit -> out of letter/items/counts, gate EDIT_NOT_CONFIRMED warning, notes 'edited; second check not available (JUDGE_UNAVAILABLE)', accept stays 422 on code-check failure
- 2026-11-02T12:31:50Z backend: moved in_progress -> in_review
- 2026-11-02T12:31:58Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer
- 2026-11-02T12:42:58Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-134-staff-engineer.md; round 1; findings:
    - [major] Item trace still says an open edit was accepted — fix: In trace.py _human_step and the item verdict (lines 247 and 281), branch on review.edit_unconfirmed(kind, row): human step PENDING with 'You edited this item; it is not accepted until you compare it with the quote and accept', reason EDIT_NOT_CONFIRMED, next_action DECIDE; verdict code 'edit_to_check', label 'Edited; waiting for 
    - [minor] Three agreed surfaces have no test that fails when they break — fix: Add assertions: with every other item decided and one open edit, review.ready_to_export is False and the case-trace review step is pending with reason EDIT_NOT_CONFIRMED; verdict.label contains '(1 not reviewed)' when nothing else is pending.
    - [minor] One existing test was weakened and one loosened — fix: Keep the old case and add a second one for an edited, unjudged, non-needs_review entry (or a flag note edit) that still blocks; make line 1012 an unconditional assert; assert the exact blocker list [(edt, 'SUMMARY_DROPS_QUALIFIER'), (None, 'NOTHING_ACCEPTED')] at line 1075; add a t134 test that an excerpt-only edited entry is edi
    - [minor] Case-checks banner still tells her to re-run a check for an item that is out of the letter — fix: Exclude human-authored edits (D-045b) from the judges step unavailable count, or word the banner for the open-edit case; then run the test under FIXTURE_SET=curated too.
- 2026-11-02T12:42:58Z orchestrator: assigned: backend
- 2026-11-02T12:43:06Z backend: claimed

## Handoff
What changed: one rule review.edit_unconfirmed (entry, edited, state needs_review, edited summary/excerpt). Item view edit_to_check; review.counts.edit_to_check; export treats it as pending (not in letter/items/counts, excluded.edit_not_confirmed); gate warning EDIT_NOT_CONFIRMED (a warning, not a blocker: out of letter like pending; NOTHING_ACCEPTED excludes it; never JUDGE_NOT_RUN while open); notes EDITED/PENDING/RECORDS lines say 'edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed' and after her accept keep the reason; never 'accepted'. Accept already 422 CODE_CHECK_FAILED via D-051 (tested). Contract updated. How verified: tests/unit/test_t134_unconfirmed_edit.py; full unit suite 3298 passed; updated 4 test_trace and 1 test_spanish_records tests that assumed an open edit is accepted. Left: frontend should use item.edit_to_check (ZL.editToCheck is summary-only; an excerpt-only edit from the quote picker is now withheld by the backend but the UI row would not offer 'I compared it'); frontend card needed. Surprised: D-050 Spanish/OCR edits stay needs_review so they also need her explicit accept now (intended).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:06.984Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/backend/project_backend_conventions.md"
}
````

### User / tool · 2026-11-02T12:43:06.991Z

**tool result**
````
1	---
2	name: backend-conventions
3	description: Codepaths, conventions and pitfalls for the deterministic backend modules and pipeline (T-032/033/037); read before touching ingest, amounts, gaps, conflicts, pipeline
4	metadata:
5	  type: project
6	---
7	
8	Codepaths (app/backend): `ingest.py` (split/limits/dedupe/warnings, `ingest()` composite, `evidence_span`), `dates.py` (format list, 2-digit year >40 ambiguous per D-027), `amounts.py` (cents, classify, extract_amounts, rate_note), `totals.py`, `gaps.py`, `conflicts.py`, `flag_templates.py` (render with closed var whitelist + golden-subtype aliases), `lexicon.py` (loads app/llm/lexicon.yaml as data; deterministic modules must not import app.llm), `pipeline.py` (stages 0-7, `run_ingest`, `ingest_case`, `run_pipeline`, `run_case`, `judge_summary`, CLI). `app/pipeline.py` is a shim so `python -m app.pipeline` works (outside owned paths; flagged to orchestrator).
9	
10	Conventions: money is int cents and amounts.py must not contain `float(`; text outside recognised record blocks becomes an `unsplit` record (never dropped; only exact `ingest.BANNERS` lines are set aside); a figure inside an injection hit has cents None; flag title/explanation only via flag_templates.render; code never sets review_status (pipeline items leave a run `pending`; `_persist` preserves existing review status on rerun).
11	
12	Pitfalls: (1) the stage-and-commit rule: `git add` and `git commit` must be separate Bash calls (git-guard hook rejects a combined call), and commit with explicit pathspec `git commit -m ... -- <paths>`. (2) One sqlite3 connection shared by worker threads corrupts `PRAGMA table_info` reads; audited.py serialises writes with `_DB_LOCK`; do not use `:memory:` DBs with threads (CLI uses a temp file). (3) Fixture keys hash the full prompt, so any prompt/schema change in app/llm/prompts or judges invalidates tests/fixtures/llm: re-run `LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record <golden .txt>` per case and `--judges`. (4) tests/unit/test_pipeline.py SEM script has `record_id` which schemas.FlagOutput forbids: the 3 j3 pipeline tests fail until T-036/qa reconcile.
13	
14	Review findings to avoid repeating: silent text loss in splitters, silent century guesses, ACs ticked on REPL evidence without a named test.
15	
16	T-075 (determinism): the 0.0 live 3-run did not reproduce in 12 later runs; the real fragilities were judge prompts (J4 rejected valid flags; J3 undecided), model-order-dependent ids, and immediate retries. Judge prompts now v2 (flag category rules; J3 takes `category`). To re-record only judge fixtures after a judge prompt change, replay the recorded set and call claude-cli only on a miss at j3/j4 (never re-record whole cases: it would overwrite extract/narrative fixtures other workers depend on); then run `make_curated.py` (no flag), restore unchanged curated files byte-for-byte, `--check`. Run live pipeline checks in parallel processes (6 at once is fine, ~60 s).
17	
18	T-085 (Spanish records): code half `language.py` + `spanish_text.py` (no app.llm import; test_boundaries bans LLM imports in dates.py, so keep Spanish code checks out of `spanish.py`, which wires the judge). Spanish records use steps `extract_es` / `judge_faithfulness_es` (own prompts, registered in audited.PROMPT_OF_STEP). To record only missing fixtures for new prompts: `ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record --fill-missing evals/library/<packet>.txt` (replays recorded answers). Committing a shared file other workers also edit: filter `git diff HEAD -U0` hunks by keyword, `git apply --cached --unidiff-zero` into a temp GIT_INDEX_FILE built from `git read-tree HEAD`; `xargs git add` is blocked by git-guard, list paths explicitly.
19	
20	## T-085 r2 lessons (language fail-safe)
21	- Commit with other workers' dirty hunks in the same file: build a temp index (`GIT_INDEX_FILE=$(mktemp)`, `read-tree HEAD`), `git add` whole files only when all hunks are mine; for mixed files (confidence/review/pipeline) hash-object the HEAD text + my edits and `update-index --cacheinfo`. Verify with `git diff --cached --stat`.
22	- language.detect: lang 'uncertain' = some non-English evidence, no confident answer; is_translated(lang) routes es+uncertain to the Spanish path; record_lang never returns English for text with foreign evidence. Do not put words identical to English (fracture, diagnostic, cervical, protrusion) in fr/pt/es lists.
23	- A one-record packet's preamble line becomes record 1 in ingest; test packets need 2+ records or no preamble.
24	- Spanish eval pairs: tests/unit/spanish_translation_pairs.jsonl; live judge eval opt-in SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1.
25	
26	T-086/T-087 r2 (PDF security): `pdf_hidden.py` is a differential render (page with vs without all text, render mode 3 toggled per object); `FPDFTextObj_GetText` is O(page) per call, so read text only for hidden objects. `review.enforce_ocr` re-applies OCR_DERIVED after every item-rewriting step (edit, manual entry, split, date confirm). Pitfalls: other workers edit review.py/api.py concurrently, so commit "HEAD + my hunks": rebuild the file by applying my replacements to `git show HEAD:file`, `git hash-object -w`, `git update-index --cacheinfo` into a `GIT_INDEX_FILE=$(mktemp)` index after `git read-tree HEAD`; then `git reset -q -- <my files>` so the main index is not stale. git-guard blocks `$VAR` in command position (use literal paths) and macOS `sed -i` needs a suffix (use python for edits). Strided memoryview rows need `.tobytes()` before zlib.
27	
28	## T-085 r4 (D-050)
29	- Non-English never verified: `confidence.compose_state` ctx `translated` -> AI_TRANSLATION; any new code path that composes a state from a record must pass `language.translated_record(rec)`. Row-based recomputes (rejudge.recompose, review._without_date_doubt) keep the reason from the stored row. Tests: tests/unit/test_d050_never_verified.py.
30	- language.detect: `_EN_COLLISIONS` (son, operation, plus, solo...) are not foreign evidence when English-only words >= 3. Held-out jsonl rows: `d050_only` (unroutable, word-for-word Spanish) and `ambiguous` are excluded from routing gates.
31	- Committing with other workers' hunks: HEAD moves during work (check `git log -1` right before `read-tree HEAD`); rebuild blobs from the new HEAD (`git show HEAD:f` + my substitutions) and `update-index --cacheinfo`; check_stale_index blocks a stale tree. Run the committed tree via `git archive $(git write-tree)` in the scratchpad.
32	
33	T-087 r4 (PDF isolation): ALL PDF parsing (pypdf read + PDFium scan) runs in one child (`pdf_hidden._run_child`, modes text/scan/both, JSON lines: texts first, result second) killed at the shared deadline, with a parent-side `ps` RSS poll (1 GiB; macOS has no RLIMIT_AS). `pdf_text.read_pages` is in-process-only for the child and tests. `pdf_checks._JOBS` (2) gives 429 `busy` and covers OCR too (OCR's pdfium render still runs in the API worker thread). Commit trick that worked: fixed GIT_INDEX_FILE path, `git add` and `git commit` in separate Bash calls (git-guard), then `git reset -q -- files` on the real index. Reviewer probe files are in the reviewer's scratchpad, not the repo: rebuild from the review text.
34	
35	T-094 (live determinism, conflicts, causation): open-ended model generation of conflicts was the flake. Conflicts are now CODE candidates (`conflict_candidates.py`: plan vs early end with frequency x duration multiplied out; denial of prior history vs a phrase-list prior hit), J3 (`judge_conflict_v4`) only classifies; no `conflicts` model step or prompt exists. J3 benign -> tray (rejected); model-only flag + J4 disagree -> suppressed (`out["suppressed_flags"]`). Pitfalls: (1) `evals.run` scores tray (rejected) flags as emitted candidates, so only suppression removes a false positive from precision; (2) any J3 prompt edit must pass `evals.run --controls` (D-046: all wrong caught, 0 false agree, including held-out) before the 3-run evals; (3) to re-record only the changed judge fixtures use a replay-then-record-on-miss wrapper (fixture first, live only on a miss) per case, then make_curated.py and restore unchanged curated files byte-for-byte; (4) the tree is shared: build commits from a temp index on HEAD and check `git diff HEAD -- <file>` for other workers' hunks (pipeline.py/trace.py/api.md got swept by others twice); (5) architect owns docs/LLM_VS_CODE.md row 11 and must be told the conflicts row changed.
36	
37	T-094 r2 (D-053): nothing a model proposes is dropped. A model-only flag J4 rejects, and a model-proposed conflict without a code candidate, are TRAY items (`flags._to_tray`; reasons JUDGE_DISAGREES / LLM_ONLY); `present.case_view` tray has kind `flag` items (before this, rejected flags were in the DB but never in the API tray). `suppressed_flags` no longer exists. evals/run.py: `to_candidates` skips state `rejected` (precision/recall over emitted flags only), `flag_tray` reported apart, signature `flags` excludes rejected; report header names `Source commit ..., tree clean`. judge_flag_v3 (missed_care = scheduled/recommended treatment not attended; scene refusal is scene_facts): re-record J4 fixtures with `python -m app.llm.record --fill-missing <packet>` over evals/golden/*.txt and evals/library/*.txt in parallel (script pattern: ThreadPool of subprocesses, ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1). Candidate rules: number words, plan cue, _early_end negation/completion guards in conflict_candidates.py; uncovered patterns in SCOPE_CUTS row 13.
38	
39	T-103 r4 (billing.py): a printed money token is identified by POSITION (`_at` offset range, `_row` excerpt range, `_unit` line/segment start), never by text; parsers attach positions, `_placed()` reads them back, `_strip_private()` removes every `_`-prefixed key before analyze returns. D-052 "no comparisons" was read strictly: no `_nt`, no cents `<`, sign = `_is_credit` flag; guard test `test_no_money_value_or_text_is_compared_in_billing_code`. Verify count fixes with MANY seeds (reviewer seed 20261102 plus seeds 1-40 via the test module's `_insert`/`_BASES`): seed 20261102 alone hid ~28 CMS/EOB shapes. Never add keys to `_ub_header`/`_header` cols (the test generator draws from them, which would change every seed's draws); use `_ub_all_cols`. Commit with other workers' dirty api.md: build HEAD blob + my replacements, `update-index --cacheinfo` into a temp `GIT_INDEX_FILE`.
40	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:09.010Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 && git status --short | head -20; sed -n 225,300p app/backend/trace.py; grep -n \"edit_unconfirmed\\|edit_to_check\\|EDIT_NOT_CONFIRMED\" app/backend/*.py | head -50"
}
````

### User / tool · 2026-11-02T12:43:09.145Z

**tool result**
````
abaa14a docs(orchestrator): scope cut 13c informant-reported history in conflict candidates (T-113 F2)
bba9e5c test(backend): T-113 r2 live controls from clean worktree of bea3984, judge_conflict_v6: J3 19/19 x3, 5 clean held-out controls all right, J4 12/12
bea3984 fix(backend): T-113 r2 held-out status derived from git, H3V16/H3V1/H3V3 moved to in_sample, 5 new held-out J3 controls locked before any run, tray reason for model conflicts, list-word and tray-order tests
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/frontend/app.js
    if verdict == "unavailable":
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence=ev, next_action=na("RERUN_JUDGE", {"item_id": item_id}))
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
                        "SCHEMA_INVALID": "Not run: the AI answer was malformed.",
                        "SUMMARY_NOT_IN_QUOTE": "Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.",
                        "LLM_FAILED_AFTER_RETRIES": "Not run: the AI gave no usable answer for this record.",
                        "FIXTURE_MISS": "Not run: the AI gave no usable answer for this record.",
                        "UNSUPPORTED_LANGUAGE": "Not run: the record is not in a language the AI reads."}.get(code, "Not run because an earlier step rejected this item.")
    return step(sid, label, kind, SKIPPED, msg, reason=code, rule=rule)


def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
    """Assemble the item trace: numbering, progress, verdict, state_reasons mapped to the step that explains them."""
    _number(steps)
    ids = {s["id"] for s in steps}
    rs = row.get("review_status")
    live = row.get("state") != "rejected"
    first_na = next((s["next_action"] for s in steps if s["next_action"]), None)
    gated = [s for s in steps if s["kind"] == "code" and s["status"] == FAIL and s.get("blocks_export")]      # D-045(b): human wording whose code check fails
    if rs in ("accepted", "edited", "dismissed"):
        first_na = gated[0]["next_action"] if gated else None     # the human already decided; step-level hints stay on the steps, except a failing code check on their own wording
    if gated:      # whose words: only the paralegal's own summary is "your wording"; an AI draft is "this summary"
        code, label = "needs_attention", ("Needs your attention: a check on your wording fails" if _paralegal_wording(kind, row) else "Needs your attention: a check on this summary fails")
    elif rs in ("accepted", "edited"):
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
    blocks = blocks or bool(gated)
    judge_id = next((s["id"] for s in steps if s["id"].startswith("judge_")), None)
    fallback = next((s["id"] for s in steps if s["status"] == FAIL), steps[0]["id"] if steps else None)   # e.g. record-warning flags have one code step

    def step_of(c):
app/backend/api.py:537:            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
app/backend/export.py:520:        elif any(e.get("edit_unconfirmed") for e in ents):
app/backend/export.py:537:    if e.get("review_status") == "edited" or e.get("edit_unconfirmed"):
app/backend/export.py:550:def _edit_unconfirmed_why(e) -> str:
app/backend/export.py:555:def _edit_unconfirmed_phrase(e) -> str:
app/backend/export.py:557:    return f"edited; {_edit_unconfirmed_why(e)}; not yet confirmed against the quote, so it is not in the letter (accept it to put it there)"
app/backend/export.py:576:        tail = (f" ({_edit_unconfirmed_phrase(e)})" if e.get("edit_unconfirmed") else
app/backend/export.py:577:                f" (accepted by the paralegal after comparing it with the quote; {_edit_unconfirmed_why(e)})" if e.get("edit_state_reasons") and _status(e) == "in" else "")
app/backend/export.py:585:        if e.get("edit_unconfirmed") and not e.get("code_check_failed"):
app/backend/export.py:586:            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}" ({_edit_unconfirmed_phrase(e)})')
app/backend/present.py:49:            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter
app/backend/present.py:201:    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
app/backend/present.py:206:            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
app/backend/review.py:81:def edit_unconfirmed(kind: str, item: dict) -> bool:
app/backend/store.py:64:        if review_mod.edit_unconfirmed("entry", e):          # T-134: reworded and still needs_review: not decided. Out of the letter and counted as pending (D-045a); the notes name why.
app/backend/store.py:66:            d["edit_unconfirmed"] = True
app/backend/trace.py:43:    "EDIT_NOT_CONFIRMED": "An edited entry is still marked Needs review; it stays out of the letter until you compare it with the quote and accept it.",
app/backend/trace.py:822:            and not review.edit_unconfirmed(u["kind"], u["row"])]          # T-134: an edit not yet accepted is not in the letter, so it blocks nothing
app/backend/trace.py:1021:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
app/backend/trace.py:1025:    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
app/backend/trace.py:1026:        n = rc["edit_to_check"]
app/backend/trace.py:1029:                       reason="EDIT_NOT_CONFIRMED", rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
app/backend/trace.py:1037:    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
app/backend/trace.py:1046:        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
app/backend/trace.py:1090:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:10.884Z

**tool call — Bash**
````
{
 "command": "sed -n 70,100p app/backend/review.py; sed -n 1015,1075p app/backend/trace.py; grep -n \"_human_step\\|_finish(\" app/backend/trace.py | head -30; grep -n \"unavailable\" app/backend/trace.py | head -30; cat tests/unit/test_t134_unconfirmed_edit.py | head -80"
}
````

### User / tool · 2026-11-02T12:43:10.991Z

**tool result**
````
# plain words for "AI wording removed (failed a check: ...)" in the internal notes
CHECK_PHRASE = {"SUMMARY_TOKEN_NOT_IN_EXCERPT": "a number or word in it is not in the quote", "SUMMARY_DROPS_QUALIFIER": "it drops a qualifier the quote has",
                "GROUNDING_EXCERPT_NOT_VERBATIM": "the quote is not word for word in the record", "EXCERPT_OMITS_QUALIFIER": "the quote leaves out a hedge sentence",
                "EXCERPT_NOT_WHOLE_SENTENCE": "the quote is not whole sentences", "HIGHLIGHT_NOT_FOUND": "the quote cannot be found in the record"}


def current_text(item: dict):
    ed = item.get("edited") or {}
    return ed.get("summary", item.get("summary") or ""), ed.get("excerpt", item.get("excerpt") or "")


def edit_unconfirmed(kind: str, item: dict) -> bool:
    """T-134 (D-045b, D-051): an ENTRY the paralegal reworded or re-quoted whose state is still needs_review (the second check did not run or did not agree, or another
    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
    not in the letter, not counted as accepted, and the notes do not say she accepted it. Her explicit accept (review_status accepted) ends it; that accept is bound
    by the code checks (set_review). One source for the item view, the review counts, the export and the gate."""
    return (kind == "entry" and item.get("review_status") == "edited" and item.get("state") == "needs_review"
            and any(k in (item.get("edited") or {}) for k in ("summary", "excerpt")))


def code_check_failures(rec, item: dict) -> dict:
    """{reason_code: detail} for every D-034/D-047/D-022 code check the entry's CURRENT summary and quote fail. Recomputed from the text (same
    functions the generator and the edit route use), plus any such reason already stored on the item, so old data cannot slip through.
    `rec` is a store.load_records() dict (None: only the stored reasons count)."""
    out = {}
    summ, exc = current_text(item)
    if rec is not None:
        g = spanish.module_for(language.record_lang(rec))
        toks = g.new_tokens(summ, exc, rec.get("source") or item.get("provider") or "", rec.get("date_iso") or item.get("date_iso") or "")
        if toks:
            out["SUMMARY_TOKEN_NOT_IN_EXCERPT"] = {"tokens": toks}
    elif pend_ch:
        st.append(step("totals", "Billed-charges total", "code", PENDING, f"{pend_ch} detected charge{'s' if pend_ch != 1 else ''} not in the total until you accept {'them' if pend_ch != 1 else 'it'}. The total is added up by code from accepted charges only.",
                       reason="PENDING_DECISION", rule="row 8", counts=tcounts, next_action=na("DECIDE", {"view": "amounts"}, ["accept", "dismiss"])))
    else:
        st.append(step("totals", "Billed-charges total", "code", PASS, "The total is added up by code from the accepted charges.", rule="row 8", counts=tcounts))
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
        n = rc["edit_to_check"]
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm "
                       f"{'them' if n != 1 else 'it'}). Compare {'them' if n != 1 else 'it'} with the quote and accept, or the {'entries stay' if n != 1 else 'entry stays'} out of the letter.",
                       reason="EDIT_NOT_CONFIRMED", rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"] - n_edit, "edit_not_confirmed": n_edit,
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if n_edit:
        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else "")
                    + (" " + edit_warning(n_edit) if n_edit else ""),
                    rule="row 19", counts=gate_counts)
    else:
        first = blockers[0]
        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
                if jnr and first is jnr[0] else first["why"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                    blocks=True)
    gate.update(ready=ready, blockers=blockers, warnings=warnings)
    st.append(gate)
    _number(st)
    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
               else {"code": "ready", "label": "Ready to export" + (f" ({n_pend + n_edit} not reviewed)" if n_pend + n_edit else "")} if ready
               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
                      else f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def pending_warning(n: int) -> str:
    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."


def edit_warning(n: int) -> str:
    return (f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm {'them' if n != 1 else 'it'}), so {'they are' if n != 1 else 'it is'} "
            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")

235:def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
269:def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
419:    st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
524:    st.append(_human_step(cx, row, "amount"))
553:        st.append(_human_step(cx, row, "flag"))
569:        st.append(_human_step(cx, row, "flag"))
589:        st.append(_human_step(cx, row, "flag"))
648:    st.append(_human_step(cx, row, "flag"))
741:    return _finish(cx, item_id, kind, row, steps)
30:_LADDER_VOCAB = {"supported", "partially", "unsupported", "disagrees", "unsure", "unavailable"}
216:        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence={"judge_verdict": "unavailable"},
225:    if verdict == "unavailable":
510:        if acknowledge_only("amount", row) and js["status"] == SKIPPED and (js.get("evidence") or {}).get("judge_verdict") == "unavailable":
760:    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
778:    """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
785:                and (s.get("evidence") or {}).get("judge_verdict") == "unavailable":
787:            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
803:        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
834:               "disagrees": 0, "unsure": 0, "unavailable": 0} for j in ("j1", "j2", "j3", "j4")}
866:        elif v in ("unsure", "unavailable"):
889:                       "unavailable": j("unavailable"), "human_overrides": overrides},
986:    elif t["unavailable"]:
987:        msg = f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. "
1096:    return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
"""T-134 (paralegal pass 4 M2; D-045b, D-051): an edited entry that is still needs_review has not been decided.
It is not in the letter, not counted as accepted, listed by the gate as EDIT_NOT_CONFIRMED (a warning: it is not in the letter, so it blocks nothing),
and the notes never say the paralegal accepted it. Her explicit Accept (after comparing with the quote) is still bound by the code checks (422)."""
import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import run_case

EDIT = "Persistent neck pain 6/10 with daily headaches noted."


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "t134.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _gate(c, tok):
    return next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "export_gate")


def _setup(c, accept=("e1",)):
    tok = run_case(c)
    for i in accept:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "edited" and r.json()["item"]["state"] == "needs_review"
    return tok, r.json()


def test_edit_with_no_second_check_is_not_in_the_letter_and_not_counted_accepted(env):
    _, c = env
    tok, r = _setup(c)
    assert r["item"]["edit_to_check"] is True
    assert r["review"]["counts"]["edit_to_check"] == 1
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200
    j = ex.json()
    assert EDIT not in j["letter_text"] and "daily headaches" not in j["letter_text"]
    assert "e3" not in [e["id"] for e in j["items"]["entries"]]
    assert j["counts"]["entries"] == 1 and j["counts"]["pending"] >= 1
    assert j["excluded"]["edit_not_confirmed"] == 1
    assert j["provenance"]["edited_count"] == 0
    notes = j["internal_notes_text"]
    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" in notes
    assert "not yet confirmed" in notes
    before_edited = notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]
    assert "not in the letter" in before_edited and EDIT in before_edited
    assert "Items not reviewed: 0" not in notes


def test_gate_names_the_unconfirmed_edit_as_a_warning_and_agrees_with_the_export(env):
    _, c = env
    tok, _ = _setup(c)
    g = _gate(c, tok)
    assert g["ready"] is True and g["blockers"] == []          # not in the letter, so it does not block (the same rule as a pending item, D-045a)
    w = {x["reason_code"]: x for x in g["warnings"]}
    assert w["EDIT_NOT_CONFIRMED"]["count"] == 1 and "second check" in w["EDIT_NOT_CONFIRMED"]["why"]
    assert g["counts"]["edit_not_confirmed"] == 1 and g["counts"]["accepted"] == 1
    assert c.get(f"/api/cases/{tok}/export").status_code == 200       # ready == export allowed


def test_only_an_unconfirmed_edit_accepted_means_nothing_accepted(env):
    _, c = env
    tok, r = _setup(c, accept=())
    assert r["review"]["ready_to_export"] is False
    g = _gate(c, tok)
    assert g["ready"] is False and [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"]
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"][0]["reason_code"] == "NOTHING_ACCEPTED"


def test_explicit_accept_after_comparing_moves_it_into_the_letter_and_the_notes_keep_the_reason(env):
    _, c = env
    tok, _ = _setup(c)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:13.935Z

**tool call — Bash**
````
{
 "command": "sed -n 80,200p tests/unit/test_t134_unconfirmed_edit.py; sed -n 756,832p app/backend/trace.py; sed -n 975,995p app/backend/trace.py; sed -n 995,1020p tests/unit/test_trace.py; sed -n 1060,1085p tests/unit/test_trace.py"
}
````

### User / tool · 2026-11-02T12:43:14.117Z

**tool result**
````
    tok, _ = _setup(c)
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "accepted" and r.json()["item"]["edit_to_check"] is False
    assert r.json()["review"]["counts"]["edit_to_check"] == 0
    j = c.get(f"/api/cases/{tok}/export").json()
    assert EDIT in j["letter_text"] and "e3" in [e["id"] for e in j["items"]["entries"]]
    assert "EDIT_NOT_CONFIRMED" not in [w["reason_code"] for w in _gate(c, tok)["warnings"]]
    notes = j["internal_notes_text"]
    assert "second check not available" in notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]


def test_accept_after_comparing_is_a_422_when_the_stored_wording_fails_a_code_check(env):
    db, c = env
    tok, _ = _setup(c)
    conn = DB.connect(db)
    row = DB.get_item(conn, "e3", tok)
    ed = dict(row["edited"], summary="Persistent neck pain 9/10 with daily headaches noted.")      # old data: a figure the quote does not carry
    DB.apply_review(conn, "e3", "edit", edited=ed, now=1.0, case=tok)       # straight into the DB: the edit route would refuse it
    conn.close()
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED"
    assert [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e3"][0]["review_status"] == "edited"      # nothing was written
    g = _gate(c, tok)
    assert g["ready"] is False and any(b["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" for b in g["blockers"])      # D-051: the gate still blocks it


def test_a_verified_edit_is_unaffected(env):
    """An edit the second check supports is state verified: in the letter at once, no warning."""
    _, c = env
    tok = run_case(c)
    r = c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    assert r.status_code == 200 and r.json()["item"]["edit_to_check"] is False
    assert "EDIT_NOT_CONFIRMED" not in [w["reason_code"] for w in _gate(c, tok)["warnings"]]


# ------------------------------------------------------------------ judge report
def _judge_rows(cx):
    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
    out = []
    for kind in ("entry", "amount", "flag"):
        for row in DB.list_items(cx.conn, cx.case_id, kind):
            if kind == "flag" and FT.is_filtered(row.get("state_reasons")):      # D-057: never judged, never counted
                continue
            jd = (row.get("ladder") or {}).get("judge")
            if not jd or not jd.get("verdict"):
                out.extend(_judge_never_ran(cx, kind, row))
                continue
            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
            call = cx.call(jd.get("call_id"), row["id"], jid)
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": _norm_verdict(jid, jd["verdict"]),
                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
    return out


def _judge_never_ran(cx, kind, row):
    """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
    if not cx.ran or _paralegal_wording(kind, row):
        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
    out = []
    for s in _STEPS_OF[kind](cx, row):
        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
                and (s.get("evidence") or {}).get("judge_verdict") == "unavailable":
            jid = "j" + s["id"].split("_")[1]
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
    return out


def _paralegal_wording(kind, row) -> bool:
    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))


def unjudged_items(conn, case_id: str) -> list:
    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
    cx = _Cx(conn, case_id, False)
    out = []
    for r in _judge_rows(cx):
        row = r["row"]
        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
            continue
        if _paralegal_wording(r["kind"], row):
            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
        out.append({"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "review_status": row["review_status"], "row": row})
    return out


def acknowledge_only(kind: str, row: dict) -> bool:
    """T-114 (D-019/D-042): a figure classified `rate` is never a letter charge, so accepting it only acknowledges it (it is listed in the internal notes, never totaled).
    No second AI check is needed for that, so a missing one never blocks export. The one source for the amount view's `accept_effect` and the gate."""
    return kind == "amount" and row.get("kind") == "rate"


def judge_not_run_blockers(conn, case_id: str) -> list:
    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one.
    A rate (`acknowledge_only`) is the one exception: accepting it only acknowledges it, nothing of it reaches the letter (T-114)."""
    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id)
            if u["review_status"] in ("accepted", "edited") and not acknowledge_only(u["kind"], u["row"])
            and not review.edit_unconfirmed(u["kind"], u["row"])]          # T-134: an edit not yet accepted is not in the letter, so it blocks nothing


def _jnr_blocker(u):
    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN"],
            "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}


def judge_report(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    rows = _judge_rows(cx)
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
        msg = f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. "
        if cx.running:
            st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
        else:
            st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
                           reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
    elif objections:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, f"The second check questioned {objections} of {t['items_judged']} items; they are marked for review.",
                       reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
        t = c.get(f"/api/cases/{tok}/items/{i}/trace").json()
        h = steps_of(t)["human"]
        assert t["verdict"]["code"] == "rejected" and t["verdict"]["blocks_export"] is False
        assert h["status"] == "pending" and h["next_action"]["code"] == "DISMISS_OR_ENTER_BY_HAND" and h["blocks_export"] is False
    g = _gate(c, tok)
    assert amt["id"] not in [b["item_id"] for b in g["blockers"]] and flg["id"] not in [b["item_id"] for b in g["blockers"]]
    assert g["counts"]["rejected_not_blocking"] == g0["counts"]["rejected_not_blocking"] + 2


def test_an_edited_item_counts_as_accepted_for_the_judge_blocker(env):
    """status 'edited' blocks like 'accepted' (the quote is still AI-chosen when only the quote was edited)."""
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    e = DB.get_item(conn, eid, tok)
    DB.apply_review(conn, eid, "edit", edited={"excerpt": e["excerpt"], "original_excerpt": e["excerpt"], "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    assert DB.get_item(conn, eid, tok)["review_status"] == "edited"
    if DB.get_item(conn, eid, tok)["state"] == "needs_review":      # T-134: an edit still Needs review is not in the letter yet, so it blocks nothing until she accepts it
        assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]
        assert c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"}).status_code == 200
    assert eid in [b["item_id"] for b in _jnr(_gate(c, tok))]


def test_rejudge_writes_one_rejudge_event_per_asked_item_and_leaves_review_status_alone(env, monkeypatch):
    """T-095: review_events.action 'rejudge', one row per item the second check was asked about; the paralegal's status is untouched."""
    c, conn, tok, _ = env
def _ccf(gate):
    return [b for b in gate["blockers"] if b.get("step_id")]


def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    g = _gate(c, tok)
    got = _ccf(g)
    assert [b["item_id"] for b in got] == [edt] and got[0]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and got[0]["step_id"] == "summary_qualifier"
    assert g["ready"] is False and g["status"] == "fail" and g["counts"]["code_check_failed"] == 1 and g["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
    assert "second AI check is not needed" in got[0]["why"] and g["next_action"]["code"] == "EDIT_SUMMARY"
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 422 and "letter_text" not in r.text and REVIEWER_EDIT not in r.text
    det = r.json()["error"]["detail"]["blockers"]
    assert [(b["item_id"], b["reason_code"]) for b in det if b["item_id"]] == [(edt, "SUMMARY_DROPS_QUALIFIER")]      # (T-134: and NOTHING_ACCEPTED, the open edit is not accepted)
    assert r.json()["error"]["code"] == "export_blocked" and "export is blocked" in r.json()["error"]["message"]
    ct = c.get(f"/api/cases/{tok}/trace").json()
    assert ct["verdict"]["code"] == "needs_attention" and "fails a check" in ct["verdict"]["label"]


def test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    t = c.get(f"/api/cases/{tok}/items/{edt}/trace").json()
    s = steps_of(t)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:19.806Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-134/; grep -n \"FIXTURE_SET\" -r tests/unit/*.py app | head; grep -n \"test_edited_summary_with_judge_unavailable\" -A25 tests/unit/*.py | head -50"
}
````

### User / tool · 2026-11-02T12:43:19.910Z

**tool result**
````
__pycache__
judges_step134.py
paralegal_view.py
probe134.py
probe134b.py
probe134c.py
probe134d.py
probe134e.py
probe134f.py
probe134g.py
shot134.py
steps134.py
ui-after-edit.png
tests/unit/test_eval_runner.py:284:    """D-029 / T-051: with FIXTURE_SET=curated or LLM_FIXTURE_DIR under tests/fixtures/llm/curated, the full run exits 2 with a clear message and writes no report; recorded/default sets are accepted."""
tests/unit/test_eval_runner.py:285:    monkeypatch.setenv("FIXTURE_SET", "curated")
tests/unit/test_eval_runner.py:288:    monkeypatch.delenv("FIXTURE_SET")
tests/unit/test_eval_runner.py:294:    monkeypatch.setenv("FIXTURE_SET", "recorded")
tests/unit/test_eval_runner.py:1050:    monkeypatch.setenv("FIXTURE_SET", "recorded")
tests/unit/test_eval_runner.py:1055:            seen.update(dir=os.environ.get("LLM_FIXTURE_DIR"), set=os.environ.get("FIXTURE_SET"))
tests/unit/test_eval_runner.py:1060:    assert os.environ.get("FIXTURE_SET") == "recorded" and "LLM_FIXTURE_DIR" not in os.environ
tests/unit/test_export_edge.py:44:    monkeypatch.setenv("FIXTURE_SET", "curated")
tests/unit/test_spanish_records.py:415:    monkeypatch.delenv("FIXTURE_SET", raising=False)
app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
tests/unit/test_trace.py:854:def test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b(env):
tests/unit/test_trace.py-855-    c, conn, tok, _ = env
tests/unit/test_trace.py-856-    # every judge answered except one entry the paralegal then rewrites; dismiss the rest so only that item is live
tests/unit/test_trace.py-857-    case = c.get(f"/api/cases/{tok}").json()
tests/unit/test_trace.py-858-    target = case["entries"][0]["id"]
tests/unit/test_trace.py-859-    row = DB.get_item(conn, target, tok)
tests/unit/test_trace.py-860-    lad = row["ladder"]
tests/unit/test_trace.py-861-    lad["judge"] = None
tests/unit/test_trace.py-862-    DB.update_item(conn, target, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
tests/unit/test_trace.py-863-    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, target))
tests/unit/test_trace.py-864-    before = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
tests/unit/test_trace.py-865-    assert before["status"] == "fail"
tests/unit/test_trace.py-866-    DB.apply_review(conn, target, "edit", edited={"summary": row["summary"] + " Reviewed.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
tests/unit/test_trace.py-867-    ct = c.get(f"/api/cases/{tok}/trace").json()
tests/unit/test_trace.py-868-    assert steps_of(ct)["judges"]["status"] != "fail" and steps_of(ct)["judges"]["counts"]["unavailable"] == 0
tests/unit/test_trace.py-869-    g = steps_of(ct)["export_gate"]
tests/unit/test_trace.py-870-    # T-134: her edit is still Needs review, so it is open: not accepted, not in the letter. Nothing else is accepted here, so the gate says so; no judge blocker.
tests/unit/test_trace.py-871-    assert [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"] and "EDIT_NOT_CONFIRMED" in [w["reason_code"] for w in g["warnings"]]
tests/unit/test_trace.py-872-    assert c.post(f"/api/cases/{tok}/items/{target}/review", json={"action": "accept"}).status_code == 200      # her explicit accept after comparing it with the quote
tests/unit/test_trace.py-873-    ct = c.get(f"/api/cases/{tok}/trace").json()
tests/unit/test_trace.py-874-    g = steps_of(ct)["export_gate"]
tests/unit/test_trace.py-875-    assert g["ready"] is True and ct["verdict"]["code"] == "ready" and c.get(f"/api/cases/{tok}/export").status_code == 200
tests/unit/test_trace.py-876-
tests/unit/test_trace.py-877-
tests/unit/test_trace.py-878-# ------------------------------------------------------------------ the rejudge route
tests/unit/test_trace.py-879-def test_rejudge_in_demo_mode_replays_recorded_answers_and_clears_the_gate(env, monkeypatch):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:21.370Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-134/judges_step134.py | head -50; sed -n 380,425p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T12:43:21.452Z

**tool result**
````
"""T-134 r1: case-trace judges step after an edit with the curated fixture set (parent vs HEAD). usage: python judges_step134.py <archive_dir>"""
import sys, os, json
sys.argv = [sys.argv[0], sys.argv[1]]
os.environ["FIXTURE_SET"] = "curated"
sys.path.insert(0, "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-134")
import probe134 as P
c, t = P.mk()
P.post(c, t, "e1", P.A)
r = P.post(c, t, "e3", P.E(P.EDIT))
print("edit", r.status_code, r.json()["item"]["state"], r.json()["item"]["reasons"])
tr = c.get(f"/api/cases/{t}/trace").json()
print("verdict", tr["verdict"])
for s in tr["steps"]:
    if s["id"] in ("judges", "export_gate", "review"):
        print(" ", s["id"], s["status"], "|", (s.get("why") or "")[:150], "|", {k: v for k, v in (s.get("counts") or {}).items() if v})
              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks) or "SUMMARY_TOKEN_NOT_IN_EXCERPT" in live)
    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R or "SUMMARY_DROPS_QUALIFIER" in live)
    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or "HIGHLIGHT_NOT_FOUND" in live)
    # date confirmed (D-041)
    unconf = review.date_unconfirmed(cx.conn, cx.case_id, "entry", row)
    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
    dev = {"date": {"record_id": rid, "date_raw": rec.get("date_raw"), "date_iso": rec.get("date_iso"), "date_status": rec.get("date_status"),
                    "candidates": rec.get("date_candidates") or []}}
    if unconf:
        code = "DATE_AMBIGUOUS" if rec.get("date_status") == "ambiguous" else "DATE_MISSING"
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if code == "DATE_AMBIGUOUS" else na("READ_RECORD", {"record_id": rid})
        st.append(step("date_confirmed", "Date of service is confirmed", "code", FAIL, reason_text(code), reason=code, rule="D-041", evidence=dev,
                       next_action=nxt, blocks=live_pending))
    else:
        st.append(step("date_confirmed", "Date of service is confirmed", "code", PASS, "The date comes from the record's own header and is parsed or confirmed.",
                       rule="D-041", evidence=dev))
    # injection scan
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                       evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    st += _ocr_steps(R, rid)
    # judge 1
    if stop:
        st.append(_skipped("judge_1", "Second AI check: is the summary supported by the quote?", "llm", stop, "row 4"))
    else:
        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j1", R))
    nxt = None
    if unconf:
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if rec.get("date_status") == "ambiguous" else na("READ_RECORD", {"record_id": rid})
    if _code_check_gated(row):        # D-045(b), D-051: a failing code check blocks the export (AI-made or human wording; only the judge is exempt for human wording) and says what to do
        for s in st:
            if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS:
                s["blocks_export"] = True
                s["next_action"] = _fix_action(row, s)
    st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
    return st


def _code_check_gated(row) -> bool:
    """An accepted or edited, live entry: its failing code checks block the export (D-051). Accept refuses such an item, so this is old data or a
    state reached some other way; the gate does not trust that the accept guard ran."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:22.407Z

Reproduce the banner (finding 4) first.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:23.074Z

**tool call — Bash**
````
{
 "command": "cd artifacts/review-evidence/T-134 && python3 judges_step134.py . 2>&1 | tail -12; sed -n 1,40p probe134.py"
}
````

### User / tool · 2026-11-02T12:43:23.186Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-134/judges_step134.py", line 6, in <module>
    import probe134 as P
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-134/probe134.py", line 11, in <module>
    from fastapi.testclient import TestClient
ModuleNotFoundError: No module named 'fastapi'
"""T-134 r1 probe: edit/accept/undo sequences against a git-archive copy. usage: python probe134.py <archive_dir> [sequence-substring ...]
Invariants checked after every `check` step: open edits (item.edit_to_check) are not in the letter, not in items.entries, counted in excluded.edit_not_confirmed,
the gate warns EDIT_NOT_CONFIRMED iff one is open, gate.ready == (export 200), counts.entries == len(items.entries)."""
import os, sys, json, tempfile, re
ARCH = sys.argv[1]
sys.path.insert(0, ARCH)
os.chdir(ARCH)
os.environ["LLM_BACKEND"] = "fixture"
os.environ.pop("ANTHROPIC_API_KEY", None)
os.environ.pop("ENABLE_LIVE", None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
from tests.unit.test_api_routes import run_case

EDIT = "Persistent neck pain 6/10 with daily headaches noted."


def mk():
    d = tempfile.mkdtemp()
    c = TestClient(create_app(os.path.join(d, "p.sqlite"), static_dir=d), client=("127.0.0.1", 50000))
    return c, run_case(c)


def post(c, t, i, body):
    return c.post(f"/api/cases/{t}/items/{i}/review", json=body)


def state(c, t):
    case = c.get(f"/api/cases/{t}").json()
    tr = c.get(f"/api/cases/{t}/trace").json()
    gate = next(s for s in tr["steps"] if s["id"] == "export_gate")
    ex = c.get(f"/api/cases/{t}/export")
    return case, gate, ex


def check(name, c, t):
    case, gate, ex = state(c, t)
    probs = []
    ents = {e["id"]: e for e in case["entries"]}
    open_ids = [i for i, e in ents.items() if e.get("edit_to_check")]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:26.426Z

**tool call — Bash**
````
{
 "command": "which -a python python3 pytest; ls -d .venv venv 2>/dev/null; head -3 Makefile; grep -n \"pytest\" Makefile | head -3"
}
````

### User / tool · 2026-11-02T12:43:26.521Z

**tool result**
````
/opt/homebrew/bin/python3
/usr/bin/python3
.venv
head: Makefile: No such file or directory
ugrep: warning: Makefile: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:27.933Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-134/judges_step134.py /Users/arsis/zlayt-pm-project 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T12:43:28.849Z

**tool result**
````
llm call failed call_id=c92d9170b8c0a step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
edit 200 needs_review ['JUDGE_UNAVAILABLE']
verdict {'code': 'ready', 'label': 'Ready to export (22 not reviewed)'}
  judges fail | 1 item has not been double-checked. The second AI check did not run or did not finish, so this item has not been double-checked. | {'items_judged': 18, 'supported': 18, 'unavailable': 1}
  review pending | 21 items are waiting for your decision. | {'pending': 21, 'accepted': 1, 'edited': 1, 'edit_to_check': 1}
  export_gate pass | At least one item is accepted and every accepted item has its checks, so the export can be built. 21 items are not reviewed, so they will not be in th | {'pending_items': 21, 'accepted': 1, 'edit_not_confirmed': 1}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:33.840Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/dbg.py <<'EOF'\nimport sys,os\nos.environ[\"FIXTURE_SET\"]=\"curated\"\nsys.path.insert(0,\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-134\"); sys.argv=[sys.argv[0],\"/Users/arsis/zlayt-pm-project\"]\nimport probe134 as P\nc,t=P.mk()\nfor before in (True,False):\n    if not before:\n        P.post(c,t,\"e1\",P.A); r=P.post(c,t,\"e3\",P.E(P.EDIT))\n    jr=c.get(f\"/api/cases/{t}/judges\").json()\n    print(before,jr[\"totals\"], [ (i.get(\"item_id\"),i.get(\"verdict\")) for i in jr.get(\"items\",[]) if i.get(\"verdict\")==\"unavailable\"])\nEOF\n.venv/bin/python /private/tmp/claude-501/dbg.py 2>&1 | tail -5; grep -n \"def judge_report\" -A40 app/backend/trace.py | grep -n \"unavailable\\|items\" | head"
}
````

### User / tool · 2026-11-02T12:43:34.852Z

**tool result**
````
llm call failed call_id=c9d20e55656d8 step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
True {'items_judged': 19, 'supported': 19, 'unsupported': 0, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} []
False {'items_judged': 18, 'supported': 18, 'unsupported': 0, 'unsure': 0, 'unavailable': 1, 'human_overrides': 0} []
4:833-    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
5:834-               "disagrees": 0, "unsure": 0, "unavailable": 0} for j in ("j1", "j2", "j3", "j4")}
11:840-        p["items"] += 1
37:866-        elif v in ("unsure", "unavailable"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:49.009Z

**tool call — Bash**
````
{
 "command": "sed -n 836,895p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T12:43:49.084Z

**tool result**
````
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:52.794Z

**tool call — Bash**
````
{
 "command": "sed -i 's/\\[ (i.get(\"item_id\"),i.get(\"verdict\")) for i in jr.get(\"items\",\\[\\]) if i.get(\"verdict\")==\"unavailable\"\\]/jr[\"unresolved\"]/' /private/tmp/claude-501/dbg.py && .venv/bin/python /private/tmp/claude-501/dbg.py 2>&1 | tail -3 | cut -c1-600"
}
````

### User / tool · 2026-11-02T12:43:52.880Z

**tool result (error)**
````
Exit code 1
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/dbg.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:54.716Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"/private/tmp/claude-501/dbg.py\"\ns=open(p).read().replace('[ (i.get(\"item_id\"),i.get(\"verdict\")) for i in jr.get(\"items\",[]) if i.get(\"verdict\")==\"unavailable\"]','jr[\"unresolved\"]')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python /private/tmp/claude-501/dbg.py 2>&1 | tail -2 | cut -c1-700"
}
````

### User / tool · 2026-11-02T12:43:55.755Z

**tool result**
````
True {'items_judged': 19, 'supported': 19, 'unsupported': 0, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} []
False {'items_judged': 18, 'supported': 18, 'unsupported': 0, 'unsure': 0, 'unavailable': 1, 'human_overrides': 0} [{'item_id': 'e3', 'kind': 'entry', 'judge': 'j1', 'verdict': 'unavailable', 'model': 'claude-haiku-5-5', 'prompt_version': 'judge_faithfulness_v1', 'call_id': 'c75709eb4e329', 'review_status': 'edited', 'state_reason': 'JUDGE_UNAVAILABLE'}]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:44:07.584Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p artifacts/review-evidence/T-134/probe134c.py; sed -n 1086,1100p tests/unit/test_trace.py; sed -n 1,60p tests/unit/test_trace.py | grep -n \"def \\|import\" | head -30; grep -n \"_mixed\\b\" -B2 -A22 tests/unit/test_trace.py | sed -n 1,50p"
}
````

### User / tool · 2026-11-02T12:44:07.691Z

**tool result**
````
"""T-134 r1 probe C: quote-picker edits, item trace, batch accept, manual entry. usage: python probe134c.py <archive_dir>"""
import sys, json
sys.argv = [sys.argv[0], sys.argv[1]]
sys.path.insert(0, "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-134")
import probe134 as P
post, E, A = P.post, P.E, P.A
c, t = P.mk()
post(c, t, "e1", A)
case = c.get(f"/api/cases/{t}").json()
print("e5 summary:", case["entries"][4]["summary"]); print("e6 summary:", case["entries"][5]["summary"]); print("e3 summary:", case["entries"][2]["summary"])
# excerpt-only attempts
for i, exc in (("e5", "Pain 4/10, improving."), ("e6", "Discharged from PT after two missed appointments."), ("e3", "Refer to physical therapy 2x/week for 6 weeks.")):
    r = post(c, t, i, {"action": "edit", "edits": {"excerpt": exc}})
    print("excerpt-only", i, r.status_code, (r.json().get("error", {}).get("message") or "")[:140] if r.status_code >= 400 else (r.json()["item"]["review_status"], r.json()["item"]["state"], r.json()["item"]["edit_to_check"]))
# summary + excerpt together
r = post(c, t, "e3", {"action": "edit", "edits": {"excerpt": "Persistent neck pain 6/10, daily headaches.", "summary": "Persistent neck pain 6/10 and daily headaches."}})
print("both e3", r.status_code, r.json().get("error", {}).get("message", "")[:120] if r.status_code >= 400 else (r.json()["item"]["review_status"], r.json()["item"]["state"], r.json()["item"]["edit_to_check"], r.json()["item"]["excerpt"]))
print(json.dumps(P.check("after quote-picker edits", c, t), default=str)[:700])
# per-item trace of an open edit
it = c.get(f"/api/cases/{t}/items/e3/trace")
tr = it.json()
print("ITEM TRACE verdict:", tr.get("verdict"))
for s in tr["steps"]:
    if s["id"] in ("human", "judge", "judges") or "decision" in s.get("title", "").lower():
        print("  step", s["id"], s["status"], "|", s.get("why") or s.get("summary"), "|", s.get("reason"))
# batch accept
print("batch routes:")
rr = c.post(f"/api/cases/{t}/review/batch", json={"action": "accept", "scope": "verified"})
print(rr.status_code, rr.text[:300])
print(json.dumps(P.check("after batch", c, t), default=str)[:700])
    q = s["summary_qualifier"]
    assert q["status"] == "fail" and q["blocks_export"] is True and q["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
    na = q["next_action"]
    assert na["code"] == "EDIT_SUMMARY" and na["text"].startswith("Edit the summary to keep ") and "‘" in na["text"] and "export stays blocked" in na["text"]
    assert t["verdict"]["blocks_export"] is True and t["verdict"]["code"] == "needs_attention" and t["next_action"] == na
    assert s["human"]["status"] == "pass"                                       # the decision is still recorded; the code check is what blocks
    for sid in ("summary_tokens", "excerpt_verbatim", "highlight"):
        assert s[sid]["blocks_export"] is False


def test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    assert c.get(f"/api/cases/{tok}/export").status_code == 422
    quote = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == edt)["excerpt"]
3:import json
4:import pathlib
5:import sqlite3
6:import time
8:import pytest
9:from fastapi.testclient import TestClient
11:from app.backend import trace, why
12:from app.backend.api import create_app
13:from app.db import db as DB
22:def base(tmp_path_factory):
23:    import os
48:def env(base, tmp_path, monkeypatch):
1042-
1043-
1044:def _mixed(c, tok, conn):
1045-    """The reviewer's walk: accept one entry, edit another so it drops a qualifier, dismiss the first. Returns the edited id."""
1046-    ents = c.get(f"/api/cases/{tok}").json()["entries"]
1047-    acc, edt = ents[0]["id"], ents[1]["id"]
1048-    assert c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"}).status_code == 200
1049-    r = c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "edit", "edits": {"summary": REVIEWER_EDIT}})
1050-    assert r.status_code == 422 and r.json()["error"]["detail"]["reason"] == "SUMMARY_DROPS_QUALIFIER"     # D-047: the route refuses it, so the gate case below is legacy/hand-written data
1051-    orig = DB.get_item(conn, edt, tok)
1052-    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)   # bypass the route: the gate is the second line of defence
1053-    lad = orig.get("ladder") or {"item_id": edt}
1054-    lad.setdefault("code_checks", {}).update(qualifier_carried=False)
1055-    DB.update_item(conn, edt, now=9e9, case=tok, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"], ladder=lad)
1056-    c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "dismiss"})
1057-    return edt
1058-
1059-
1060-def _ccf(gate):
1061-    return [b for b in gate["blockers"] if b.get("step_id")]
1062-
1063-
1064-def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
1065-    c, conn, tok, _ = env
1066:    edt = _mixed(c, tok, conn)
1067-    g = _gate(c, tok)
1068-    got = _ccf(g)
1069-    assert [b["item_id"] for b in got] == [edt] and got[0]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and got[0]["step_id"] == "summary_qualifier"
1070-    assert g["ready"] is False and g["status"] == "fail" and g["counts"]["code_check_failed"] == 1 and g["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
1071-    assert "second AI check is not needed" in got[0]["why"] and g["next_action"]["code"] == "EDIT_SUMMARY"
1072-    r = c.get(f"/api/cases/{tok}/export")
1073-    assert r.status_code == 422 and "letter_text" not in r.text and REVIEWER_EDIT not in r.text
1074-    det = r.json()["error"]["detail"]["blockers"]
1075-    assert [(b["item_id"], b["reason_code"]) for b in det if b["item_id"]] == [(edt, "SUMMARY_DROPS_QUALIFIER")]      # (T-134: and NOTHING_ACCEPTED, the open edit is not accepted)
1076-    assert r.json()["error"]["code"] == "export_blocked" and "export is blocked" in r.json()["error"]["message"]
1077-    ct = c.get(f"/api/cases/{tok}/trace").json()
1078-    assert ct["verdict"]["code"] == "needs_attention" and "fails a check" in ct["verdict"]["label"]
1079-
1080-
1081-def test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):
1082-    c, conn, tok, _ = env
1083:    edt = _mixed(c, tok, conn)
1084-    t = c.get(f"/api/cases/{tok}/items/{edt}/trace").json()
1085-    s = steps_of(t)
1086-    q = s["summary_qualifier"]
1087-    assert q["status"] == "fail" and q["blocks_export"] is True and q["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
1088-    na = q["next_action"]
1089-    assert na["code"] == "EDIT_SUMMARY" and na["text"].startswith("Edit the summary to keep ") and "‘" in na["text"] and "export stays blocked" in na["text"]
1090-    assert t["verdict"]["blocks_export"] is True and t["verdict"]["code"] == "needs_attention" and t["next_action"] == na
1091-    assert s["human"]["status"] == "pass"                                       # the decision is still recorded; the code check is what blocks
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:44:30.997Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_t134_unconfirmed_edit.py <<'EOF'\n\n\n# ------------------------------------------------------------------ round 2 (staff-engineer findings 1-4)\ndef _item_trace(c, tok, iid):\n    t = c.get(f\"/api/cases/{tok}/items/{iid}/trace\").json()\n    return t, {s[\"id\"]: s for s in t[\"steps\"]}\n\n\ndef _dismiss_all_but(c, db, tok, keep):\n    \"\"\"Dismiss every live pending item except `keep`, so the only open thing is the edit.\"\"\"\n    conn = DB.connect(db)\n    ids = [r[\"id\"] for k in (\"entry\", \"amount\", \"flag\") for r in DB.list_items(conn, tok, k) if r[\"state\"] != \"rejected\" and r[\"review_status\"] == \"pending\" and r[\"id\"] not in keep]\n    conn.close()\n    for i in ids:\n        assert c.post(f\"/api/cases/{tok}/items/{i}/review\", json={\"action\": \"dismiss\"}).status_code == 200\n\n\ndef test_item_trace_of_an_open_edit_does_not_say_accepted(env):\n    \"\"\"Finding 1: the 'Why this status' trail must not claim her acceptance of an edit that is still open.\"\"\"\n    _, c = env\n    tok, _ = _setup(c)\n    t, s = _item_trace(c, tok, \"e3\")\n    assert t[\"verdict\"][\"code\"] == \"edit_to_check\" and \"accepted\" not in t[\"verdict\"][\"label\"].lower()\n    assert t[\"verdict\"][\"label\"] == \"Edited; waiting for your check\" and t[\"verdict\"][\"blocks_export\"] is False\n    h = s[\"human\"]\n    assert h[\"status\"] == \"pending\" and h[\"reason_code\"] == \"EDIT_NOT_CONFIRMED\" and h[\"next_action\"][\"code\"] == \"DECIDE\"\n    assert \"accepted it\" not in h[\"why\"] and \"not accepted\" in h[\"why\"] and \"compare\" in h[\"why\"]\n    assert h[\"blocks_export\"] is False\n    # her explicit accept ends it, and only then does the trail say accepted\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    t, s = _item_trace(c, tok, \"e3\")\n    assert t[\"verdict\"][\"code\"] == \"accepted\" and t[\"verdict\"][\"label\"] == \"Accepted by you\" and s[\"human\"][\"status\"] == \"pass\"\n\n\ndef test_item_trace_of_an_open_excerpt_only_edit_is_also_not_accepted(env):\n    db, c = env\n    tok, _ = _setup(c)\n    conn = DB.connect(db)\n    row = DB.get_item(conn, \"e5\", tok)\n    DB.apply_review(conn, \"e5\", \"edit\", edited={\"excerpt\": row[\"excerpt\"], \"original_excerpt\": row[\"excerpt\"], \"at\": \"2026-11-02T00:00:00Z\"}, now=1.0, case=tok)\n    DB.update_item(conn, \"e5\", case=tok, state=\"needs_review\", state_reasons_json=[\"JUDGE_UNAVAILABLE\"])\n    conn.close()\n    e5 = [e for e in c.get(f\"/api/cases/{tok}\").json()[\"entries\"] if e[\"id\"] == \"e5\"][0]\n    assert e5[\"review_status\"] == \"edited\" and e5[\"edit_to_check\"] is True       # an excerpt-only edit is open too\n    t, s = _item_trace(c, tok, \"e5\")\n    assert t[\"verdict\"][\"code\"] == \"edit_to_check\" and s[\"human\"][\"status\"] == \"pending\"\n    assert c.get(f\"/api/cases/{tok}/export\").json()[\"excluded\"][\"edit_not_confirmed\"] == 2\n\n\ndef test_a_verified_edit_trail_still_says_accepted(env):\n    \"\"\"An edit whose state is not needs_review is decided by the edit (D-045b): the trail keeps its 'edited and accepted' wording.\"\"\"\n    db, c = env\n    tok, _ = _setup(c)\n    conn = DB.connect(db)\n    DB.update_item(conn, \"e3\", case=tok, state=\"verified\", state_reasons_json=[])\n    conn.close()\n    t, s = _item_trace(c, tok, \"e3\")\n    assert t[\"verdict\"][\"code\"] == \"accepted\" and s[\"human\"][\"status\"] == \"pass\" and \"accepted\" in s[\"human\"][\"why\"]\n\n\ndef test_everything_else_decided_the_open_edit_alone_keeps_review_and_header_not_ready(env):\n    \"\"\"Findings 2 (M7, M12, M15): with nothing else pending, the open edit still holds ready_to_export, the review step and the header label.\"\"\"\n    db, c = env\n    tok, r = _setup(c)\n    _dismiss_all_but(c, db, tok, {\"e1\", \"e3\"})\n    rv = c.get(f\"/api/cases/{tok}\").json()[\"review\"]\n    assert rv[\"counts\"][\"pending\"] == 0 and rv[\"counts\"][\"edit_to_check\"] == 1\n    assert rv[\"ready_to_export\"] is False                                          # M7: one accepted entry, one open edit: not \"decided\"\n    ct = c.get(f\"/api/cases/{tok}/trace\").json()\n    review = next(s for s in ct[\"steps\"] if s[\"id\"] == \"review\")\n    assert review[\"status\"] == \"pending\" and review[\"reason_code\"] == \"EDIT_NOT_CONFIRMED\"      # M12\n    assert ct[\"verdict\"] == {\"code\": \"ready\", \"label\": \"Ready to export (1 not reviewed)\"}      # M15: the gate passes, the header still counts the open edit\n    assert c.get(f\"/api/cases/{tok}/export\").status_code == 200\n    c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"})\n    rv = c.get(f\"/api/cases/{tok}\").json()[\"review\"]\n    assert rv[\"ready_to_export\"] is True\n    assert next(s for s in c.get(f\"/api/cases/{tok}/trace\").json()[\"steps\"] if s[\"id\"] == \"review\")[\"status\"] == \"pass\"\n\n\ndef test_judges_step_ignores_a_human_edit_whose_rerun_check_was_unavailable_under_the_curated_set(env, monkeypatch, tmp_path):\n    \"\"\"Finding 4: under FIXTURE_SET=curated the edit route's second check has no fixture; her own wording needs none (D-045b), so the case\n    checks banner must not ask her to re-run it for an item that is out of the letter.\"\"\"\n    monkeypatch.setenv(\"FIXTURE_SET\", \"curated\")\n    db = str(tmp_path / \"cur.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n    tok = run_case(c)\n    assert c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"accept\"}).status_code == 200\n    r = c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": EDIT}})\n    assert r.status_code == 200 and r.json()[\"item\"][\"edit_to_check\"] is True\n    ct = c.get(f\"/api/cases/{tok}/trace\").json()\n    j = next(s for s in ct[\"steps\"] if s[\"id\"] == \"judges\")\n    assert j[\"status\"] != \"fail\" and j[\"counts\"][\"unavailable\"] == 0\n    jr = c.get(f\"/api/cases/{tok}/judges\").json()\n    assert jr[\"totals\"][\"unavailable\"] == 0 and \"e3\" not in [u[\"item_id\"] for u in jr[\"unresolved\"]]\nEOF\nsed -n 1,25p tests/unit/test_api_routes.py | head -5; .venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py -q -x 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T12:44:34.224Z

**tool result**
````
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

        tok, _ = _setup(c)
        t, s = _item_trace(c, tok, "e3")
>       assert t["verdict"]["code"] == "edit_to_check" and "accepted" not in t["verdict"]["label"].lower()
E       AssertionError: assert ('accepted' == 'edit_to_check'
E         
E         - edit_to_check
E         + accepted)

tests/unit/test_t134_unconfirmed_edit.py:135: AssertionError
------------------------------ Captured log call -------------------------------
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c047d36c7c811 step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
=========================== short test summary info ============================
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_item_trace_of_an_open_edit_does_not_say_accepted
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 6 passed in 2.88s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:44:46.026Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/backend/trace.py\"\ns=open(p).read()\nold='''    if rs in (\"accepted\", \"edited\"):\n        return step(\"human\", \"Your decision\", \"human\", PASS,'''\nnew='''    if review.edit_unconfirmed(kind, row):      # T-134 r2: her edit is saved but she has not accepted it; the trail must not say she did (same rule as the gate, the export and the notes)\n        return step(\"human\", \"Your decision\", \"human\", PENDING, TRACE_WHY[\"EDIT_NOT_CONFIRMED_ITEM\"], reason=\"EDIT_NOT_CONFIRMED\", rule=\"row 17\", evidence=ev, blocks=False,\n                    next_action=na(\"DECIDE\", {\"item_id\": row[\"id\"]}, [\"accept\", \"edit\", \"dismiss\"]))\n    if rs in (\"accepted\", \"edited\"):\n        return step(\"human\", \"Your decision\", \"human\", PASS,'''\nassert old in s; s=s.replace(old,new)\nold='''    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = gated[0][\"next_action\"] if gated else None'''\nnew='''    open_edit = review.edit_unconfirmed(kind, row)            # T-134 r2: edited, still Needs review, not accepted\n    if rs in (\"accepted\", \"edited\", \"dismissed\"):\n        first_na = gated[0][\"next_action\"] if gated else (next((s[\"next_action\"] for s in steps if s[\"id\"] == \"human\"), None) if open_edit else None)'''\nassert old in s; s=s.replace(old,new)\nold='''    elif rs in (\"accepted\", \"edited\"):\n        code, label = \"accepted\", \"Accepted by you\"'''\nnew='''    elif open_edit:\n        code, label = \"edit_to_check\", \"Edited; waiting for your check\"\n    elif rs in (\"accepted\", \"edited\"):\n        code, label = \"accepted\", \"Accepted by you\"'''\nassert old in s; s=s.replace(old,new)\nold='''    \"EDIT_NOT_CONFIRMED\": \"An edited entry'''\nnew='''    \"EDIT_NOT_CONFIRMED_ITEM\": \"You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.\",\n    \"EDIT_NOT_CONFIRMED\": \"An edited entry'''\nassert old in s; s=s.replace(old,new)\nold='''            jd = (row.get(\"ladder\") or {}).get(\"judge\")\n            if not jd or not jd.get(\"verdict\"):\n                out.extend(_judge_never_ran(cx, kind, row))\n                continue\n            jid = judge_of_prompt(jd.get(\"prompt_version\")) or {\"entry\": \"j1\", \"amount\": \"j2\", \"flag\": \"j4\"}[kind]\n            call = cx.call(jd.get(\"call_id\"), row[\"id\"], jid)\n'''\nnew='''            jd = (row.get(\"ladder\") or {}).get(\"judge\")\n            if not jd or not jd.get(\"verdict\"):\n                out.extend(_judge_never_ran(cx, kind, row))\n                continue\n            jid = judge_of_prompt(jd.get(\"prompt_version\")) or {\"entry\": \"j1\", \"amount\": \"j2\", \"flag\": \"j4\"}[kind]\n            if _paralegal_wording(kind, row) and _norm_verdict(jid, jd[\"verdict\"]) == \"unavailable\":\n                continue                                        # T-134 r2 (D-045b): the edit route's re-check had no answer; her own wording needs none, so it is not a missing check\n            call = cx.call(jd.get(\"call_id\"), row[\"id\"], jid)\n'''\nassert old in s; s=s.replace(old,new)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"def step(\" -A6 app/backend/trace.py | head; grep -n \"TRACE_WHY\\[\" app/backend/trace.py | head -3; .venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T12:44:50.825Z

**tool result**
````
100:def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
101-    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
102-            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}
103-
104-
105-def _ocr_steps(R, rid) -> list:
106-    """T-086: the step that holds an OCR-read item for review. Only present when the item carries OCR_DERIVED, so other cases are unchanged."""
84:        return TRACE_WHY[code]
249:        return step("human", "Your decision", "human", PENDING, TRACE_WHY["EDIT_NOT_CONFIRMED_ITEM"], reason="EDIT_NOT_CONFIRMED", rule="row 17", evidence=ev, blocks=False,
258:    return step("human", "Your decision", "human", PENDING, TRACE_WHY["PENDING_DECISION"], reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
...........                                                              [100%]
11 passed in 4.40s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:44:59.872Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_trace.py\"\ns=open(p).read()\nold=s[s.index(\"def test_an_edited_item_counts_as_accepted_for_the_judge_blocker\"):s.index(\"def test_rejudge_writes_one_rejudge_event_per_asked_item\")]\nnew='''def test_an_edited_item_counts_as_accepted_for_the_judge_blocker(env):\n    \"\"\"status 'edited' blocks like 'accepted' once it is decided (the quote is still AI-chosen when only the quote was edited).\n    T-134: an edit still marked Needs review is not decided: it blocks nothing until she accepts it.\"\"\"\n    c, conn, tok, _ = env\n    _blank_and_accept(c, conn, tok)\n    eid = sorted(b[\"item_id\"] for b in _jnr(_gate(c, tok)) if b[\"kind\"] == \"entry\")[0]\n    e = DB.get_item(conn, eid, tok)\n    DB.apply_review(conn, eid, \"edit\", edited={\"excerpt\": e[\"excerpt\"], \"original_excerpt\": e[\"excerpt\"], \"at\": \"2026-11-02T00:00:00Z\"}, now=1.0, case=tok)\n    assert DB.get_item(conn, eid, tok)[\"review_status\"] == \"edited\"\n    assert DB.get_item(conn, eid, tok)[\"state\"] == \"needs_review\"\n    assert eid not in [b[\"item_id\"] for b in _jnr(_gate(c, tok))]\n    assert c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"accept\"}).status_code == 200\n    assert eid in [b[\"item_id\"] for b in _jnr(_gate(c, tok))]\n\n\ndef test_an_edited_unjudged_entry_that_is_not_needs_review_still_blocks_as_accepted_would(env):\n    \"\"\"The `edited` arm of judge_not_run_blockers (T-134 r2): an edit that is not open (state not needs_review) is decided by the edit, so its missing second check blocks.\"\"\"\n    c, conn, tok, _ = env\n    _blank_and_accept(c, conn, tok)\n    eid = sorted(b[\"item_id\"] for b in _jnr(_gate(c, tok)) if b[\"kind\"] == \"entry\")[0]\n    e = DB.get_item(conn, eid, tok)\n    DB.apply_review(conn, eid, \"edit\", edited={\"excerpt\": e[\"excerpt\"], \"original_excerpt\": e[\"excerpt\"], \"at\": \"2026-11-02T00:00:00Z\"}, now=1.0, case=tok)\n    DB.update_item(conn, eid, case=tok, state=\"verified\", state_reasons_json=[])\n    row = DB.get_item(conn, eid, tok)\n    assert row[\"review_status\"] == \"edited\" and row[\"state\"] == \"verified\"\n    assert eid in [b[\"item_id\"] for b in _jnr(_gate(c, tok))]\n\n\n'''\ns=s.replace(old,new)\nold='''    assert [(b[\"item_id\"], b[\"reason_code\"]) for b in det if b[\"item_id\"]] == [(edt, \"SUMMARY_DROPS_QUALIFIER\")]      # (T-134: and NOTHING_ACCEPTED, the open edit is not accepted)'''\nnew='''    assert [(b[\"item_id\"], b[\"reason_code\"]) for b in det] == [(edt, \"SUMMARY_DROPS_QUALIFIER\"), (None, \"NOTHING_ACCEPTED\")]      # T-134: the open edit is not accepted either'''\nassert old in s; s=s.replace(old,new)\nold='''    assert s[\"human\"][\"status\"] == \"pass\"                                       # the decision is still recorded; the code check is what blocks'''\nnew='''    assert s[\"human\"][\"status\"] == \"pending\" and s[\"human\"][\"reason_code\"] == \"EDIT_NOT_CONFIRMED\"      # T-134: the edit is open, so the trail does not call it a decision; the code check is what blocks'''\nassert old in s; s=s.replace(old,new)\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_trace.py -q -x 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T12:45:08.592Z

**tool result**
````
........................................................................ [ 83%]
..............                                                           [100%]
86 passed in 8.01s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:45:14.767Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/mut.py <<'EOF'\nimport subprocess,shutil\nmuts=[(\"app/backend/present.py\",'counts[\"pending\"] == 0 and counts[\"edit_to_check\"] == 0 and','counts[\"pending\"] == 0 and'),\n(\"app/backend/trace.py\",'    elif rc[\"edit_to_check\"]:           # T-134','    elif False:           # T-134'),\n(\"app/backend/trace.py\",'(f\" ({n_pend + n_edit} not reviewed)\" if n_pend + n_edit else \"\")','(f\" ({n_pend} not reviewed)\" if n_pend else \"\")'),\n(\"app/backend/trace.py\",'if u[\"review_status\"] in (\"accepted\", \"edited\") and not acknowledge_only','if u[\"review_status\"] in (\"accepted\",) and not acknowledge_only'),\n(\"app/backend/trace.py\",'    if review.edit_unconfirmed(kind, row):      # T-134 r2','    if False:      # T-134 r2'),\n(\"app/backend/trace.py\",'    elif open_edit:\\n        code, label = \"edit_to_check\"','    elif False:\\n        code, label = \"edit_to_check\"'),\n(\"app/backend/trace.py\",'if _paralegal_wording(kind, row) and _norm_verdict(jid, jd[\"verdict\"]) == \"unavailable\":','if False:'),\n]\nfor f,a,b in muts:\n    s=open(f).read(); assert a in s,(f,a)\n    open(f,\"w\").write(s.replace(a,b))\n    r=subprocess.run(\".venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_trace.py -q -x 2>&1 | tail -1\",shell=True,capture_output=True,text=True)\n    open(f,\"w\").write(s)\n    print(\"KILLED\" if \"failed\" in r.stdout else \"SURVIVED\", a[:50], \"|\", r.stdout.strip())\nEOF\n.venv/bin/python /private/tmp/claude-501/mut.py; git diff --stat -- app/backend/present.py app/backend/trace.py"
}
````

### User / tool · 2026-11-02T12:45:51.546Z

**tool result**
````
KILLED counts["pending"] == 0 and counts["edit_to_check"] | 1 failed, 9 passed in 4.39s
KILLED     elif rc["edit_to_check"]:           # T-134 | 1 failed, 9 passed in 4.24s
KILLED (f" ({n_pend + n_edit} not reviewed)" if n_pend +  | 1 failed, 9 passed in 4.22s
KILLED if u["review_status"] in ("accepted", "edited") an | 1 failed, 67 passed in 10.40s
KILLED     if review.edit_unconfirmed(kind, row):      #  | 1 failed, 6 passed in 3.02s
KILLED     elif open_edit:
        code, label = "edit_to | 1 failed, 6 passed in 3.23s
KILLED if _paralegal_wording(kind, row) and _norm_verdict | 1 failed, 10 passed in 4.62s
 app/backend/trace.py | 11 ++++++++++-
 1 file changed, 10 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:45:53.898Z

**tool call — Bash**
````
{
 "command": "git show 5fb338d -- app/backend/api.py | head -40; grep -n \"edit_to_check\\|EDIT_NOT_CONFIRMED\\|\\\"accepted\\\"\" memory/contracts/api.md | head -20"
}
````

### User / tool · 2026-11-02T12:45:54.007Z

**tool result**
````
commit 5fb338d8c648cfd0ad6814cc0337f830396a05ae
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 06:31:43 2026 -0600

    fix(backend): T-134 an edit still Needs review is open: out of the letter, not accepted, gate warns EDIT_NOT_CONFIRMED, notes say second check not available
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 81a97a0..dfe1f24 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -506,10 +506,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
-    from app.backend import pdf_routes
-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import billing
     billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import reclassify
     reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
@@ -534,7 +534,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             tv = present.totals_view(c, token)
             ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
             ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
-            ex["excluded"] = {"pending": case["pending_count"],
+            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                               "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                               "rejected": present.rejected_count(c, token)}
             ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
183:    "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"},
248:    "counts": {"pending": 22, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
347:  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
348:  "review": { "counts": {"pending": 21, "accepted": 0, "edited": 1, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
355:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
356:- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
358:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
360:- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
554:  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "before": {"review_status": "pending"}, "after": {"review_status": "accepted"}, "at": "2026-11-02T01:05:00Z" } ] }
632:    { "id": "review", "kind": "human", "counts": {"pending": 21, "accepted": 0, "edited": 0, "dismissed": 0} },
635:      "counts": {"blocking": 1, "pending_items": 21, "date_unconfirmed": 1, "accepted": 0, "dismissed": 0, "rejected_not_blocking": 1, "judge_not_run": 0},
666:  "rejudged": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "review_status": "accepted", "verdict": "supported", "state": "verified", "state_reasons": [] } ],
667:  "still_unavailable": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "review_status": "accepted", "verdict": "unavailable" } ],
674:`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:45:58.484Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && sed -n 357,361p memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T12:45:58.485Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:45:59.994Z

**tool call — Bash**
````
{
 "command": "sed -n 357,361p memory/contracts/api.md; git diff --stat -- memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T12:46:00.112Z

**tool result**
````
- Export: the entry is **not in the letter**, not in `items.entries`, not counted in `counts.entries` or `provenance.edited_count`; it counts in `excluded.pending` and in `excluded.edit_not_confirmed` (subset of pending), and in the notes' "Items not reviewed: N". It does not block export (it is not in the letter, as with a pending item, D-045(a)), unless nothing else is accepted (`NOTHING_ACCEPTED`).
- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
- Internal notes: EDITED ITEMS lists it with "(edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter (accept it to put it there))" (the reason sentence follows the item's reasons: `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, ...), PENDING ITEMS NOT INCLUDED lists it with the same phrase, and RECORDS NOT IN THE TREATMENT SECTION says "edited, not yet confirmed against the quote". After she accepts, EDITED ITEMS keeps the reason: "(accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE))". The notes never say she accepted an edit she has not accepted.
- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:04.062Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"memory/contracts/api.md\"\ns=open(p).read()\na=\"- Frontend: an excerpt-only edit (the quote picker)\"\nnew=\"- Item trace (`GET /items/{id}/trace`, the \\\"Why this status\\\" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with \\\"You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.\\\", and the item `verdict` is `{code: \\\"edit_to_check\\\", label: \\\"Edited; waiting for your check\\\"}` (new `verdict.code` value; a failing code check still wins: `needs_attention`). After her accept it is `accepted` / \\\"Accepted by you\\\". A verified edit (state not `needs_review`) still reads \\\"You edited this item and accepted it.\\\". The case `/judges` totals and the `judges` step no longer count a human-edited entry whose re-check had no answer (D-045b).\\n\"\nassert a in s\nopen(p,\"w\").write(s.replace(a,new+a,1))\nEOF\n.venv/bin/python -m pytest tests/unit -q -x -n 4 2>&1 | tail -5 || true"
}
````

### User / tool · 2026-11-02T12:46:04.342Z

**tool result**
````
ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]
python -m pytest: error: unrecognized arguments: -n 4
  inifile: None
  rootdir: /Users/arsis/zlayt-pm-project
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:05.639Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -8",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T12:50:20.648Z

**tool result**
````
........................................................................ [ 89%]
........................................................................ [ 91%]
........................................................................ [ 93%]
........................................................................ [ 95%]
........................................................................ [ 97%]
........................................................................ [ 99%]
..                                                                       [100%]
3457 passed, 1 skipped in 253.50s (0:04:13)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:50:40.567Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/backend/trace.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_t134_unconfirmed_edit.py; git add app/backend/trace.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_t134_unconfirmed_edit.py"
}
````

### User / tool · 2026-11-02T12:50:40.693Z

**tool result**
````
 app/backend/trace.py                     | 11 +++-
 memory/contracts/api.md                  |  1 +
 tests/unit/test_t134_unconfirmed_edit.py | 94 ++++++++++++++++++++++++++++++++
 tests/unit/test_trace.py                 | 26 +++++++--
 4 files changed, 125 insertions(+), 7 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:50:46.941Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(backend): T-134 r2 item trace says edited, waiting for your check (not accepted) for an open edit; judges step ignores human-edit re-check gap; mutant-killing tests\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- app/backend/trace.py memory/contracts/api.md tests/unit/test_trace.py tests/unit/test_t134_unconfirmed_edit.py && git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T12:50:47.469Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
db1d8d5
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:50:51.392Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-134 --sha db1d8d5 --agent backend; $B handoff T-134 --agent backend --text \"Round 2. Major fixed: item trace for an open edit (trace.py _human_step/_finish) now has human step pending (EDIT_NOT_CONFIRMED, not blocking, next_action DECIDE) and verdict {edit_to_check, 'Edited; waiting for your check'}; 'accepted' wording only after her accept or for a verified edit. Minors: judges step/judge report no longer count a human-edited entry whose re-check had no answer (D-045b; reproduced under FIXTURE_SET=curated); test_trace weakened tests restored (unconditional assert, exact blocker list, new test for the 'edited' arm of judge_not_run_blockers); new t134 tests for M7/M12/M15 and excerpt-only edits. Verified: 7 mutants (M7, M12, M15, M16, the new branches) each killed; full unit suite 3457 passed 1 skipped. Contract (api.md) updated: new verdict.code edit_to_check, human step pending; fields edit_to_check unchanged. Nit: the api.py route-order swap (billing/pdf_routes) is not mine, likely a swept hunk from another worker; left as is, suite green.\"; $B move T-134 in_review --agent backend"
}
````

### User / tool · 2026-11-02T12:50:51.696Z

**tool result**
````
T-134: commit db1d8d5 recorded
handoff written on T-134
T-134: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:51:24.805Z

T-134 round 2 is in review at db1d8d5. The full unit suite passes (3457, 1 skipped).
- **Major:** the per-item trace for an open edit now says "Edited; waiting for your check" (`verdict.code` `edit_to_check`). The human step is pending with reason `EDIT_NOT_CONFIRMED` and doesn't block export. "Accepted" appears only after her accept, or for a verified edit. The new verdict code is the only contract change; `edit_to_check` is unchanged for T-136. I documented it in `memory/contracts/api.md`.
- **Mutants and minors:**
  - All 4 survivors (M7, M12, M15, M16) are now killed, as are the new branches, by new or restored tests.
  - The weakened `test_trace` tests are restored (unconditional assert, exact blocker list).
  - The case-checks banner no longer counts a human-edited entry whose re-check had no answer (reproduced under `FIXTURE_SET=curated`).
- **Not fixed:** the `api.py` billing/pdf route-order swap isn't mine, and I left it as is. I didn't touch lexicon_scan, summary_trim, `lexicon.yaml` or the conflict code.
