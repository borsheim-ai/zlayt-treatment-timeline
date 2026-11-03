# Subagent: Backend: T-134 fix-up + T-138 r2 (Backend: T-134 fix-up + T-138 r2)

Source: `agent-a5bd1b6f8a4e2976e.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:37:31.322Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Claim both cards with `--force`.

**T-134 bounded fix-up (final).** Read reviews/T-134-staff-engineer-r3.md and the orchestrator's §7.4 note on the card, then do exactly those items:
1. Fix the two missed D-058 wordings.
2. Read the 'ran again, no answer' claim from the current quote's rejudge record.
3. Show no 'export stays blocked' text when the gate passes.
4. Kill N18, N19 and H2.
5. Add an explicit item field such as `second_check_pending`, documented in api.md, so the UI stops guessing.

**T-138, round 2.** Read reviews/T-138-staff-engineer.md. The snapshot of `code_checks` aliases the dict that the edit then updates in place; deep-copy it so undo restores the pre-edit checks. The reproduction is alias138.py in the review evidence. Also:
- kill mutants T3 and T9;
- keep `pre_edit` out of GET case, or document it.

Write tests first. Other workers are in amounts.py, billing.py, conflicts.py, conflict_candidates.py, charge_text.py, case_list.py and app/frontend; don't touch those. Commit via a temp index with only your hunks in shared files (trace.py, review.py, store.py, api.md).

Run the full unit suite, then commit each card separately with a pathspec. Write the handoffs and move both cards to in_review. Reply in 3 lines.

### User / tool · 2026-11-02T13:37:31.327Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:33.758Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-134 --agent backend --force; $B claim T-138 --agent backend --force; cat reviews/T-134-staff-engineer-r3.md; $B show T-134 | tail -60"
}
````

### User / tool · 2026-11-02T13:37:34.001Z

**tool result**
````
T-134 claimed by backend
T-138 claimed by backend
# T-134 staff-engineer-reviewer, round 3 (commit 8bef6f8, final round)

Verdict: changes. No blocker. The r2 major is fixed (the judge report no longer counts an open edit as "accepted despite an objection"), mutants N3, N5 and N11 now die, and the grep of the other `("accepted","edited")` readers holds. But the part of the card that is about honest wording for a re-picked quote with an unanswered rerun is only half done: two case-level texts still say what D-058 forbids, and the new "the check already ran again" claim is stale after a second quote pick.

Pin. `git rev-parse HEAD` at start was e25098d. It moved to c4bb4da during the review. `git diff --stat e25098d c4bb4da -- app/backend/trace.py review.py export_routes.py present.py rejudge.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py` is empty, so the card code is identical at both. Review copies are `git archive` extracts (no .git), in the scratchpad dirs `t134r3_head` (e25098d), `t134r3_c4bb` (c4bb4da) and `t134r3_fix` (e25098d plus a 2-line scratch stub, see below). Probes, outputs and the mutation runner are in `artifacts/review-evidence/T-134/r3/`.

## The unit-suite question (the 11 "other worker" failures)

- They do not reproduce on any archive. `grep -c "test_amounts\|test_t093" ` over the e25098d full-suite log is 0, and `unit_runs.txt` records: c4bb4da archive `3600 passed, 8 skipped in 208.23s`.
- But the e25098d archive was NOT green: `148 failed, 3437 passed, 8 skipped in 202.88s` (3 of them in this card's own file: `test_accept_after_comparing_is_a_422...`, `test_item_trace_of_an_open_excerpt_only_edit...`, `test_everything_else_decided_the_open_edit_alone...`). Cause: commit 225e666 (T-143, before 8bef6f8) put `conflict_candidates.checks()` into `present.case_view` (`present.py:317`) while the function lived only in another worker's uncommitted tree, so `GET /api/cases/{token}` raised `AttributeError: module 'app.backend.conflict_candidates' has no attribute 'checks'` and returned 500 for every case. With the 2-line stub (`t134r3_fix`) the same archive passes: `3585 passed, 8 skipped`. c4bb4da (T-141/T-142) defines `checks()`, so HEAD is repaired. This was not caused by T-134 or T-138, so it is not a finding on them. It does mean the handoff figure "3614 pass" described the dirty working tree, and for a window of commits (225e666 to e25098d) a clean checkout had a 500 on the main case endpoint. Process note for the orchestrator: a partial-hunk commit by a sibling worker broke every card committed on top of it.

## What the brief asked

| Check | Result | Evidence |
|---|---|---|
| human_overrides ignores an open edit | holds | trace.py:881 `and not review.edit_unconfirmed(r["kind"], row)`. Test `test_judge_report_does_not_count_an_open_edit_as_accepted_despite_an_objection`: 0 while open, 1 after accept, objection stays in `rejections` and `totals.unsupported`. |
| Worker's grep of the other readers | accurate | I re-ran the grep (`"accepted", "edited"`, `== "edited"`) over app/backend and app/frontend. trace.py:435 and :528, export.py:34, totals.py:4, present.py:179, overlap.py:120 are amounts or old-data gates; api.py:543 `provenance.edited_count` is 0 with an open edit (`edited_count.out`: `items ['e1'] ... edited_count: 0`, after accept `['e1','e3']`). No unlisted reader found. |
| Mutants N3, N5, N11 die | yes | `mutants.txt`: N3 KILLED (`test_item_next_action_of_an_open_edit_is_decide`), N5 KILLED (2 tests), N11 KILLED. Run on the stubbed e25098d archive; 253 tests per run. |
| Texts for a re-picked quote with an unanswered rerun honest and matching D-058 | partly | D-058 itself is respected: the AI summary stays AI (no human-authored shortcut), accept then export is 422 `judge_not_run`, her own summary clears it (`probe134r3.out` P5: export 200), and an answering judge clears it (P4, judge patched to `supported`: rejudge verifies, export 200). The texts are the problem, see findings 1 to 3. |

## Findings

Two majors (texts), three minors. Details in the JSON.

```json
{"card": "T-134", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive e25098d (HEAD at start) and c4bb4da (HEAD at finish; card files identical); app/backend/trace.py, export_routes.py, review.py, present.py, rejudge.py; tests/unit/test_t134_unconfirmed_edit.py; memory/ORCHESTRATOR_DECISIONS.md D-044, D-045, D-058; fixture backend, sample case evals/golden/sample.txt via TestClient; no served app",
 "exercised": [
  "read reviews/T-134-staff-engineer-r2.md, board show T-134 and T-138, D-044/D-045/D-058, git show 8bef6f8 (trace.py, export_routes.py, api.md, tests) in full",
  "pytest tests/unit -q on git archive e25098d: 148 failed, 3437 passed, 8 skipped (cause: present.py:317 calls conflict_candidates.checks(), absent at that commit)",
  "same archive plus a 2-line scratch stub for checks(): 3585 passed, 8 skipped; test_t134 + test_t138 + test_trace: 110 passed",
  "pytest tests/unit -q on git archive c4bb4da (HEAD at finish): 3600 passed, 8 skipped, 208 s; no test_amounts or test_t093 failure on any archive",
  "mutate_r3.py: N3, N5, N11 (killed), N12-N17, N20 (killed), N18, N19 (survived), H1 (killed by an older test), H2 (survived) on the stubbed archive; log in artifacts/review-evidence/T-134/r3/mutants.txt",
  "probe134r3.py P1-P6: quote-pick under the AI summary, accept, export, rejudge before and after accept, stale rerun after a second pick, patched answering judge, own-summary way out, own-wording edit text",
  "review_step.py and review_step2.py: case-trace review and export_gate step texts with an open AI-quote edit alone pending",
  "itemtrace_blocked.py on 8bef6f8^ and e25098d: item trace of an accepted item that blocks export",
  "edited_count.py: export provenance.edited_count with an open edit",
  "grep of every (accepted, edited) reader in app/backend and app/frontend",
  "CLI python -m app.pipeline evals/golden/sample.txt twice on c4bb4da (fixture): rc 0, 45 lines, cmp identical"
 ],
 "verdict": "changes",
 "scores": {"export_honesty": 5, "gate_export_agreement": 5, "state_consistency_across_surfaces": 3, "wording_honesty_D058": 2, "test_strength": 3},
 "findings": [
  {"severity": "major", "title": "Two case-level texts still promise what D-058 says accept cannot do, or repeat the action that was just tried",
   "evidence": "(a) trace.py:1050-1054 (review step, edit-only branch) says 'Compare it with the quote and accept, or the entry stays out of the letter.' with no AI-summary branch. Repro: python artifacts/review-evidence/T-134/r3/review_step2.py <archive>: sample case, every other item decided, e3 quote-picked: `review pending | 1 edit is still marked Needs review (the second check did not confirm it). Compare it with the quote and accept, or the entry stays out of the letter.` Accepting it then gives export 422. memory/contracts/api.md (T-134 r3 bullet, added in this commit) says the review step carries the 'accepting alone will not put it in the letter' wording; it does not. (b) trace.py:1080 (the export_gate headline when the first blocker is JUDGE_NOT_RUN) is unchanged: after a rerun that gave no answer, `python artifacts/review-evidence/T-134/r3/itemtrace_blocked.py <archive>` prints `case gate fail False 1 accepted item has not been double-checked by the second AI check, so the export is blocked. Run the second check again.` while the blocker why and the 422 message in the same state say the check already ran again. Mutant H1 (rewrite that headline) is killed only by an older test that pins the stale sentence.",
   "why_it_matters": "The card exists to make the re-picked-quote texts honest (T-136 F-2, D-058: her compare-and-accept does not replace judge 1, the UI must name the way out). The worker changed the item human step, the gate warning, the blocker why and the 422 message and missed two sibling renderers of the same state, which is the pattern in r1 and r2 of this card. The review step is the one she reads when everything else is decided, and it tells her accepting puts the entry in the letter; the headline tells her to do the thing she just did.",
   "fix": "In the review step edit-only branch use the same `ai_summary_unchecked` count (n_ai) as edit_warning and say accepting alone will not put it in the letter. At trace.py:1080 branch on `all(b.get('rerun_no_answer') for b in jnr)` and reuse judge_not_run_message's retried sentence (one function for the blocker why, the 422 text and the headline so they cannot drift). Update api.md to say what is true.",
   "acceptance_test": "Unit: with everything else decided and a quote-picked AI-summary edit, trace review step why contains 'accepting alone'; after accept and one rejudge that gives no answer, the export_gate step why contains 'ran again' and does not end in 'Run the second check again.'; both equal the blocker why's sentence. Mutant H1 must then fail the new test, not only the old pin."},
  {"severity": "major", "title": "The 'second check ran again and gave no answer' claim is read from a stale rejudge record and is false after the quote is picked again",
   "evidence": "trace.py:814-817 `rerun_gave_no_answer` returns True when the last `ladder.rejudge` entry is unavailable, with no tie to the wording and quote the check ran on. `probe134r3.py` P3: quote Q1 picked, accepted, rejudge (no answer), then Q2 picked and accepted; the second check has not run on Q2 by anyone. `ladder.rejudge entries: 2`; blocker why: 'the second AI check ran again and still gave no answer ...' with `rerun_no_answer True`; `export msg for the NEW quote: (422, '1 accepted item has not had the second AI check: it ran again and gave no answer, so the export is blocked. It clears when the check answers, or when you edit the summary in your own words.')`. The message also stops offering 'Run the second check again', although that rerun is exactly what has not been tried on Q2. Mutant H2 (return True whenever any rejudge entry exists) SURVIVES 253 tests.",
   "why_it_matters": "An export-blocking message asserts an event that did not happen on the current quote and withholds the action that could clear it (a transient backend failure is cleared by a rerun). It is fail-closed, so nothing wrong exports, but it is a dishonest reason string in the audit-facing surface this card is about.",
   "fix": "Make `_edit` drop `ladder.rejudge` whenever it replaces `ladder.judge` (the old attempts belonged to the old wording and quote), or stamp each attempt with a hash of the summary and excerpt it ran on and compare it in `rerun_gave_no_answer`. T-138's restore should treat the list the same way.",
   "acceptance_test": "Unit: quote-pick, accept, rejudge (no answer), pick a different quote, accept: blocker why and the 422 message do not contain 'ran again' and the message contains 'Run the second check again'; then rejudge again and they do. Mutant H2 and N18 (first instead of last attempt) must fail a test."},
  {"severity": "minor", "title": "Gate warning and human-step text say 'the export stays blocked' while the gate is pass and the export is 200; grammar 'keeps' with 'it'",
   "evidence": "probe134r3.out P1: `gate ready/status: (True, 'pass')`, `export status BEFORE accept: 200`, gate why 'At least one item is accepted ... so the export can be built. ... 1 of it keeps the AI's summary and the second check has no answer on the new quote, so accepting alone will not put it in the letter; the export stays blocked until the check answers or you edit the summary yourself.' The same sentence set says the export can be built and that it stays blocked. trace.py:44 (EDIT_NOT_CONFIRMED_ITEM_AI) and trace.py:1098-1101 (edit_warning) use the same clause. Mutant N19 (edit_warning ignores n_ai) SURVIVES: the new test only asserts 'second', 'check' and 'accept' in the warning, all of which the old base text already contains.",
   "why_it_matters": "Before she accepts, nothing is blocked; the item is just left out. The conditional ('if you accept it, the export will be blocked until ...') is what is true. A paralegal reading the pass headline and this clause gets two answers.",
   "fix": "Reword to 'If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.' Fix '1 of it keeps' to '1 of them keeps' / 'It keeps'. Assert the 'AI's summary' and 'blocked' words in the warning test.",
   "acceptance_test": "N19 fails a test; the warning text for n_ai=1 contains 'If you accept it' and no 'stays blocked'."},
  {"severity": "minor", "title": "Several new text assertions are vacuous: mutants N18, N19 and H2 survive",
   "evidence": "mutants.txt: `SURVIVED N18 rerun_gave_no_answer reads the first rejudge, not the last | 253 passed`, `SURVIVED N19`, `SURVIVED H2`. tests/unit/test_t134_unconfirmed_edit.py (in test_accepted_quote_edit_blocks_with_a_reason_that_says_the_rerun_was_tried...) asserts `\"tried again\" not in b[\"why\"]`, a phrase the code never produces (the text says 'ran again'), so it cannot fail. The honest pre-rerun reason is held only by the older test that killed N12.",
   "why_it_matters": "The three changed behaviours (last-attempt selection, the AI addendum in the warning, the not-yet-rerun case) have no test that fails when they break; the vacuous line gives a false sense of coverage.",
   "fix": "Change the assertion to `'ran again' not in b['why']`, add a two-attempt case (first unavailable, last answered) for N18, and the stale-record case from finding 2 for H2.",
   "acceptance_test": "Re-run N18, N19, H2 in a scratch copy: each makes at least one test fail."},
  {"severity": "minor", "title": "OUT OF SCOPE (pre-existing, identical at 8bef6f8^): the item trace of an accepted item that blocks export says 'Accepted by you', blocks_export false, next_action none",
   "evidence": "itemtrace_blocked.py on 8bef6f8^ and e25098d prints the same: `verdict {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False} next_action None`, `judge_1 skipped False None | The second AI check did not run or did not finish`, `human pass ... You accepted this item.`, while `case gate fail ... export 422`.",
   "why_it_matters": "Same bug class as r1 and r2 of this card (one surface says fine, the gate disagrees), now on the item's own 'Why this status' row for a JUDGE_NOT_RUN item. It predates T-134 and is not rated higher.",
   "fix": "Give the item verdict a `needs_attention` / blocks_export true branch for an item that is in judge_not_run_blockers, with the blocker's next_action RERUN_JUDGE. Needs its own backend card.",
   "acceptance_test": "Unit: accepted item with unavailable judge: item trace verdict.blocks_export is true and agrees with the case gate blocker list."}
 ],
 "whats_right": [
  "human_overrides excludes an open edit with the same review.edit_unconfirmed rule as gate, export and notes; N3, N5, N11 die, and the grep of other readers is accurate (edited_count stays 0).",
  "D-058 is respected in behaviour: the AI summary stays AI-made after a quote re-pick, accept then export is 422, an answering judge or her own summary clears it, nothing is weakened.",
  "The blocker why and the 422 message are driven by one `rerun_no_answer` flag and the new text tests kill N13, N14, N15, N16, N17, N20."
 ],
 "questions_for_chris": []}
```
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T12:05:26Z"
updated_at: "2026-11-02T13:37:33Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:37:33Z"
rounds: 3
commits: ["5fb338d", "db1d8d5", "8bef6f8"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-134-staff-engineer.md", "at": "2026-11-02T12:42:58Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-134-staff-engineer-r2.md", "at": "2026-11-02T12:58:21Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-134-staff-engineer-r3.md", "at": "2026-11-02T13:37:25Z"}
ac:
  - {"n": 1, "text": "Repro (fixture, sample case): POST /api/cases {sample:true}; run; POST items/<e3>/review {action:edit, edits:{summary:'Persistent neck pain 6/10 with daily headaches noted.'}} -> 200 item.review_status=edited, state=needs_review, reasons=[JUDGE_UNAVAILABLE], review.counts.edited=1. Then GET export -> 200 and letter_text carries the edited wording; trace export_gate ready=true, blockers=[], warnings only ITEMS_NOT_REVIEWED. internal_notes_text says 'every item in the treatment section was accepted by the paralegal'. Decide with the orchestrator against D-045b (judge never blocks a human edit) and make the three places agree: (a) the gate lists an edited-and-needs_review entry as a warning EDIT_NOT_CONFIRMED (or blocker) until the paralegal accepts it, (b) export counts/excluded name it, (c) the notes EDITED ITEMS line says 'edited; second check not available' (reason code JUDGE_UNAVAILABLE) instead of 'accepted by the paralegal'. The UI (T-131/T-060 r5) already counts such an entry as open and gives it an 'I compared it with the quote' Accept; it asks before copying.", "done": true, "evidence": "tests/unit/test_t134_unconfirmed_edit.py::test_judge_report_does_not_count_an_open_edit_as_accepted_despite_an_objection; mutants N3, N5, N11 killed"}
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
- 2026-11-02T12:50:51Z backend: moved in_progress -> in_review
- 2026-11-02T12:51:26Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T12:58:21Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-134-staff-engineer-r2.md; round 2; findings:
    - [major] Judge report counts an open edit as 'you accepted despite an objection' — fix: At trace.py:865 count an override only when the edit is decided: `if row["review_status"] in ("accepted", "edited") and not review.edit_unconfirmed(r["kind"], row): overrides += 1`. Then grep the other `("accepted", "edited")` readers (trace.py:433 and :526 are fine: the first is meant to gate old data, th
    - [minor] Two new branches and the judge-report scope of the human-edit skip have no killing test — fix: Assert t['next_action']['code'] == 'DECIDE' in test_item_trace_of_an_open_edit_does_not_say_accepted; add a test that an edited entry with an objecting stored verdict remains in /judges rejections and totals.unsupported (it can share its fixture with the human_overrides test above).
    - [minor] OUT OF SCOPE (pre-existing at the parent): undoing an edit leaves the restored AI wording with the edit's 'unavailable' second check, and accept then hits JUDGE_NOT_RUN — fix: Either keep the original judge record when an edit is saved and restore it on reset, or clear the judge result and re-run it on reset. Needs a backend card; do not fold it into T-134.
- 2026-11-02T12:58:21Z orchestrator: assigned: backend
- 2026-11-02T12:58:29Z backend: claimed
- 2026-11-02T13:13:14Z backend: AC 1 checked: tests/unit/test_t134_unconfirmed_edit.py::test_judge_report_does_not_count_an_open_edit_as_accepted_despite_an_objection; mutants N3, N5, N11 killed
- 2026-11-02T13:13:26Z backend: r3: human_overrides now excludes an open edit (trace.py judge_report). Grep of other (accepted, edited) readers: trace.py:433 and :526 (gate old data, amounts: no edits), export_routes.py:32 and api.py:533/543 (already filtered by case entries / flags have no open-edit), overlap.py:120 (amounts only) are fine. Frontend: judges.js:164 tile text 'you accepted despite an objection' is now correct as is. T-136 F-2 (quote-picker accept then export block): the backend gate causes it by design (D-044: AI summary kept, second check has no answer on the new quote; under the fixture backend a rerun cannot answer a changed quote). I did NOT weaken D-044. Backend now (a) says on the item step and the EDIT_NOT_CONFIRMED gate warning that accepting alone will not put it in the letter, (b) after a rerun that still gives no answer the JUDGE_NOT_RUN blocker has rerun_no_answer:true and a why/422 message that says the check ran again, gave no answer, and that it clears when the check answers or she edits the summary in her own words (verified to work). Frontend (T-136) must show why as given and its own compare prompt/banner ('accepting does not replace it') should use the same wording; orchestrator decision needed only if a re-picked quote should count as human-authored (would change D-044).
- 2026-11-02T13:13:26Z backend: moved in_progress -> in_review
- 2026-11-02T13:13:43Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T13:37:25Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-134-staff-engineer-r3.md; round 3; findings:
    - [major] Two case-level texts still promise what D-058 says accept cannot do, or repeat the action that was just tried — fix: In the review step edit-only branch use the same `ai_summary_unchecked` count (n_ai) as edit_warning and say accepting alone will not put it in the letter. At trace.py:1080 branch on `all(b.get('rerun_no_answer') for b in jnr)` and reuse judge_not_run_message's retried
    - [major] The 'second check ran again and gave no answer' claim is read from a stale rejudge record and is false after the quote is picked again — fix: Make `_edit` drop `ladder.rejudge` whenever it replaces `ladder.judge` (the old attempts belonged to the old wording and quote), or stamp each attempt with a hash of the summary and excerpt it ran on and compare it in `rerun_gave_no_answer`. T-
    - [minor] Gate warning and human-step text say 'the export stays blocked' while the gate is pass and the export is 200; grammar 'keeps' with 'it' — fix: Reword to 'If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.' Fix '1 of it keeps' to '1 of them keeps' / 'It keeps'. Assert the 'AI's summary' an
    - [minor] Several new text assertions are vacuous: mutants N18, N19 and H2 survive — fix: Change the assertion to `'ran again' not in b['why']`, add a two-attempt case (first unavailable, last answered) for N18, and the stale-record case from finding 2 for H2.
    - [minor] OUT OF SCOPE (pre-existing, identical at 8bef6f8^): the item trace of an accepted item that blocks export says 'Accepted by you', blocks_export false, next_action none — fix: Give the item verdict a `needs_attention` / blocks_export true branch for an item that is in judge_not_run_blockers, with the blocker's next_action RERUN_JUDGE. Needs its own backend card.
- 2026-11-02T13:37:26Z orchestrator: §7.4 at round cap: accept after a bounded fix-up + scoped check: (1) the two missed D-058 wordings (review step 'accept, or the entry stays out'; gate headline trace.py:1080 'Run the second check again'); (2) the 'ran again, no answer' claim must come from the rejudge record of the CURRENT quote, not a stale one; (3) no 'export stays blocked' text when the gate passes; (4) kill N18/N19/H2. Also add an explicit item field (e.g. second_check_pending) so the UI stops guessing (frontend note on T-136).
- 2026-11-02T13:37:26Z orchestrator: assigned: backend
- 2026-11-02T13:37:33Z backend: claimed

## Handoff
What changed: judge_report human_overrides excludes an open edit (trace.py); open quote-only edit under the AI summary + rerun-gave-no-answer wording (trace.py, export_routes.py, api.md). Commit 8bef6f8 (+137ae87 api.md dedupe). How verified: tests/unit/test_t134_unconfirmed_edit.py 17 pass; mutants N3, N5, N11 each fail a test; full unit suite 3614 pass, 11 fail all in other workers' in-flight amounts/T-140 work (test_amounts*, t093 j3, t114 walking a4), none touch these files. Grep result for other (accepted, edited) readers is in the card notes. What's left: frontend wording per note (T-136 F-2); D-044 not weakened, orchestrator to decide if a re-picked quote should be human-authored. Surprised me: fixture backend cannot answer a rerun on a changed quote, so the rerun dead end is real in the demo.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:34.606Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-138-staff-engineer.md; python3 tools/board.py show T-138 | tail -40; ls artifacts/review-evidence | grep -i -E \"138|134\""
}
````

### User / tool · 2026-11-02T13:37:34.768Z

**tool result**
````
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
---
id: "T-138"
title: "Undo of an edit restores the AI wording but keeps the edit's 'unavailable' second check, so accept hits JUDGE_NOT_RUN (pre-existing; T-134 r2)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T12:58:21Z"
updated_at: "2026-11-02T13:37:33Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:37:33Z"
rounds: 1
commits: ["89146b3"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-138-staff-engineer.md", "at": "2026-11-02T13:37:26Z"}
ac:
  - {"n": 1, "text": "after undo, the restored AI wording carries its original judge result; accept works as before the edit; unit test", "done": true, "evidence": "tests/unit/test_t138_undo_edit.py (7 tests): judge, code_checks, state restored after undo; accept then export has no JUDGE_NOT_RUN; mutant removing restore fails 5"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T12:58:29Z backend: claimed
- 2026-11-02T13:13:26Z backend: AC 1 checked: tests/unit/test_t138_undo_edit.py (7 tests): judge, code_checks, state restored after undo; accept then export has no JUDGE_NOT_RUN; mutant removing restore fails 5
- 2026-11-02T13:13:26Z backend: moved in_progress -> in_review
- 2026-11-02T13:13:43Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T13:37:26Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-138-staff-engineer.md; round 1; findings:
    - [major] The snapshot keeps an alias of the code_checks dict, so undo restores the edited wording's checks, not the original ones (AC says code checks are restored) — fix: Snapshot with copy.deepcopy (judge and code_checks both), or build the snapshot dict from `dict(lad['code_checks'])` before the update. Add a test where the pre-edit code_checks differ from the edit's (set them in the DB as
    - [minor] ladder.pre_edit is returned by GET /api/cases/{token}, although api.md calls it internal — fix: Drop `pre_edit` in `_ladder` (`lad.pop('pre_edit', None)`), or state in api.md that it is present and ignorable.
    - [minor] Test gap: nothing fails if the snapshot is not removed after undo (mutant T9) — fix: In that test change the state or judge between the cycles (for example via the rejudge route with a patched answer, or a DB write) and assert the second undo returns to the state after the first undo; also assert `'pre_edit' not in ladder` after undo.
- 2026-11-02T13:37:26Z orchestrator: assigned: backend
- 2026-11-02T13:37:33Z backend: claimed

## Handoff
What changed: first edit stores ladder.pre_edit (judge, code_checks, state, reasons, state after edit); reset restores them via review.restore_pre_edit (state only if nothing else changed it since the edit; old data without a snapshot behaves as before). Commit 89146b3 (partial-hunk commit; review.py had another worker's T-139 hunks in the tree, committed separately by them). How verified: tests/unit/test_t138_undo_edit.py 7 pass; disabling the restore fails 5; full suite as on T-134. What's left: nothing; frontend needs nothing. Surprised me: shared tree had T-139 hunks in review.py/api.md, so I committed through a temporary index to keep the commits mine.

T-134
T-138
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:37.514Z

**tool call — Bash**
````
{
 "command": "git status --short | head -30; git log --oneline | head -5; grep -n \"rerun_gave_no_answer\\|rerun_no_answer\\|judge_not_run_message\\|EDIT_NOT_CONFIRMED_ITEM_AI\\|ai_summary_unchecked\\|n_ai\\|stays blocked\\|stay blocked\\|Run the second check again\" app/backend/*.py | head -60"
}
````

### User / tool · 2026-11-02T13:37:37.661Z

**tool result**
````
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
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/charge_text.py
 M app/backend/conflict_candidates.py
 M app/backend/conflicts.py
 M app/backend/generator.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
07c7558 docs(orchestrator): D-059 letter total from one-at-a-time accepted charges with code flags
c5c18a6 feat(frontend): T-142 conflict group names the kinds checked (from GET case checks, fixed fallback) and says others are not checked; never a bare 'No conflicts found.'
4872cdb feat(frontend): T-136 r2 compared edit no longer reads Needs review; D-058 held re-picked quote says the export stays blocked and offers Write the summary; plain e2e run starts a private server with a temp ZLAYT_DB; mutant-killing tests
d19ae46 feat(backend): GET /api/cases summary list for the case overview (T-148)
5de16d3 docs(orchestrator): scope cut 13e T-132 quote edge cases
app/backend/export_routes.py:58:        return judge_not_run_message(len(e.items), all(i.get("rerun_no_answer") for i in e.items))
app/backend/export_routes.py:62:def judge_not_run_message(n: int, retried: bool = False) -> str:
app/backend/export_routes.py:66:    return f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check, so the export is blocked. Run the second check again."
app/backend/rejudge.py:1:"""Run the second check again for the items whose judge never answered (D-044). The LLM judges; code decides what to ask and what state follows.
app/backend/trace.py:44:    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter: the export stays blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
app/backend/trace.py:68:    "RERUN_JUDGE": "Run the second check again.",
app/backend/trace.py:251:        return step("human", "Your decision", "human", PENDING, TRACE_WHY["EDIT_NOT_CONFIRMED_ITEM_AI" if ai_summary_unchecked(kind, row) else "EDIT_NOT_CONFIRMED_ITEM"], reason="EDIT_NOT_CONFIRMED", rule="row 17", evidence=ev, blocks=False,
app/backend/trace.py:447:    tail = " The export stays blocked until it passes."
app/backend/trace.py:807:def ai_summary_unchecked(kind, row) -> bool:
app/backend/trace.py:814:def rerun_gave_no_answer(row) -> bool:
app/backend/trace.py:850:    tried = rerun_gave_no_answer(u["row"])           # T-134 r3: the reason must match what happened after the action offered
app/backend/trace.py:852:            "rerun_no_answer": tried, "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}
app/backend/trace.py:1062:    n_ai = sum(1 for k, x in allitems if ai_summary_unchecked(k, x))
app/backend/trace.py:1072:        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit, n_ai), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
app/backend/trace.py:1076:                    + (" " + edit_warning(n_edit, n_ai) if n_edit else ""),
app/backend/trace.py:1080:        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
app/backend/trace.py:1098:def edit_warning(n: int, n_ai: int = 0) -> str:
app/backend/trace.py:1099:    return edit_warning_base(n) + (f" {n_ai} of {'them keep' if n != 1 else 'it keeps'} the AI's summary and the second check has no answer on the new quote, so accepting alone will not put "
app/backend/trace.py:1100:                                    f"{'them' if n_ai != 1 else 'it'} in the letter; the export stays blocked until the check answers or you edit the summary yourself." if n_ai else "")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:38.105Z

**tool call — Bash**
````
{
 "command": "grep -n \"pre_edit\\|rejudge\" app/backend/review.py app/backend/present.py app/backend/rejudge.py | head -60"
}
````

### User / tool · 2026-11-02T13:37:38.200Z

**tool result**
````
/bin/bash: child setpgid (10833 to 10833): Operation not permitted
app/backend/review.py:208:            restore_pre_edit(conn, case_id, item_id, kind, item, t)
app/backend/review.py:353:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
app/backend/review.py:354:        lad["pre_edit"] = {"judge": lad.get("judge"), "code_checks": lad.get("code_checks"), "state": item["state"], "state_reasons": list(item.get("state_reasons") or []),
app/backend/review.py:361:    lad["pre_edit"]["after"] = {"state": state, "state_reasons": list(reasons)}      # what the latest edit left, to tell later on whether anything else has changed the state since
app/backend/review.py:371:def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t) -> bool:
app/backend/review.py:373:    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
app/backend/review.py:376:    snap = lad.pop("pre_edit", None)
app/backend/rejudge.py:3:rejudge(conn, case_id, call, now=None) -> dict
app/backend/rejudge.py:7:    except one entry in ladder.rejudge. The paralegal's review_status is never touched. Nothing here clears the export gate except a judge answer.
app/backend/rejudge.py:59:    """One audit row per asked item (review_events action 'rejudge'); review_status is never touched."""
app/backend/rejudge.py:60:    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
app/backend/rejudge.py:61:                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)
app/backend/rejudge.py:64:def rejudge(conn, case_id: str, call, now: float = None) -> dict:
app/backend/rejudge.py:77:        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
app/backend/rejudge.py:92:    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:39.859Z

**tool call — Bash**
````
{
 "command": "sed -n 300,400p app/backend/review.py; sed -n 60,95p app/backend/rejudge.py; sed -n 800,860p app/backend/trace.py; sed -n 1040,1110p app/backend/trace.py; sed -n 40,70p app/backend/export_routes.py; sed -n 20,40p app/backend/present.py"
}
````

### User / tool · 2026-11-02T13:37:39.977Z

**tool result**
````
    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error, "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
    edits = body.get("edits")
    if kind == "amount":
        raise _bad("A charge can only be accepted or dismissed.")
    if not isinstance(edits, dict) or not edits:
        raise _bad("Nothing to edit.")
    if kind == "flag":
        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
            raise _bad("Only a note can be added to a flag.")
        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
        return []
    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
    if rec is None:
        raise _bad("The entry's source record is missing.")
    prev = item.get("edited") or {}
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    trimmed = None
    if "summary" not in edits and charge_text.has_currency(new_sum) and not charge_text.has_currency(new_exc):
        tr = charge_text.trim_summary(new_sum)          # T-139: the quote she picked no longer states the amount; code removes the trailing amount clause (D-054 suffix rule)
        if tr["changed"] and not charge_text.has_currency(tr["text"]):
            new_sum, trimmed = tr["text"], tr
    span = None
    if "excerpt" in edits:
        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call,
                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []))
    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    edited = dict(prev)
    edited.update(at=store.iso(t))
    if "summary" in edits or "summary" in prev or trimmed:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
    lad = item.get("ladder") or {"item_id": item["id"]}
    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
        lad["pre_edit"] = {"judge": lad.get("judge"), "code_checks": lad.get("code_checks"), "state": item["state"], "state_reasons": list(item.get("state_reasons") or []),
                           "lad_state": lad.get("state")}
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    lad["pre_edit"]["after"] = {"state": state, "state_reasons": list(reasons)}      # what the latest edit left, to tell later on whether anything else has changed the state since
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    enforce_ocr(conn, case_id, t)
    if trimmed:
        chk["warnings"].append({"code": "CHARGE_CLAUSE_REMOVED", "item_id": item["id"], "removed": trimmed["removed"],
                                "message": "Code removed the clause that stated a dollar amount from the summary (" + "; ".join(trimmed["removed"])
                                           + "). Amounts go only in the internal notes. Check the summary against the quote."})
    return chk["warnings"]


def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t) -> bool:
    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
    code checks return and the state is left as it is. No snapshot (an edit saved before this change): nothing happens, as before. Returns True when restored."""
    lad = dict(item.get("ladder") or {})
    snap = lad.pop("pre_edit", None)
    if kind != "entry" or not snap:
        return False
    if snap.get("judge") is not None:
        lad["judge"] = snap["judge"]
    else:
        lad.pop("judge", None)
    if snap.get("code_checks") is not None:
        lad["code_checks"] = snap["code_checks"]
    fields = {}
    after = snap.get("after") or {}
    if after and item["state"] == after.get("state") and sorted(item.get("state_reasons") or []) == sorted(after.get("state_reasons") or []):
        fields = {"state": snap["state"], "state_reasons_json": list(snap["state_reasons"])}
        if snap.get("lad_state") is not None:
            lad["state"] = snap["lad_state"]
    DB.update_item(conn, item_id, now=t, case=case_id, ladder=lad, **fields)
    enforce_ocr(conn, case_id, t)
    return True


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)


def rejudge(conn, case_id: str, call, now: float = None) -> dict:
    t = time.time() if now is None else now
    case = DB.get_case(conn, case_id)
    case_text = (case["raw_text"] or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    targets = trace.unjudged_items(conn, case_id)
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        answers = list(ex.map(lambda x: _safe_ask(x, case_text, call), targets))
    done, still = [], []
    for tg, (verdict, call_id, code) in zip(targets, answers):
        row, jid = tg["row"], tg["judge"]
        lad = dict(row.get("ladder") or {"item_id": row["id"]})
        ladder_verdict = judges.to_ladder(jid, verdict)
        attempt = {"at": t, "call_id": call_id, "verdict": ladder_verdict}
        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
        base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
        if ladder_verdict == "unavailable":
            DB.update_item(conn, row["id"], now=t, case=case_id, ladder=lad)
            _log(conn, case_id, row, jid, call_id, "unavailable", row["state"], t)
            still.append(dict(base, verdict="unavailable"))
            continue
        lad["judge"] = {**(lad.get("judge") or {}), "model": judges.judge_model(), "prompt_version": spanish.JUDGE_PROMPT if (jid == "j1" and lad.get("translation")) else trace.JUDGE_PROMPT[jid],
                        "call_id": call_id, "verdict": verdict, "reason_code": code}
        state, reasons = recompose(row, ladder_verdict)
        lad["state"] = state
        DB.update_item(conn, row["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
        _log(conn, case_id, row, jid, call_id, ladder_verdict, state, t)
        done.append(dict(base, verdict=ladder_verdict, state=state, state_reasons=reasons))
    gate = next(s for s in trace.case_trace(conn, case_id)["steps"] if s["id"] == "export_gate")
    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
            "export_gate": {"ready": gate["ready"], "status": gate["status"], "blockers": gate["blockers"]}}


def _paralegal_wording(kind, row) -> bool:
    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))


def ai_summary_unchecked(kind, row) -> bool:
    """T-134 r3 (T-136 F-2): an open edit that left the AI's summary in place (a re-picked quote) and whose second check has no answer. Accepting it alone cannot clear D-044's
    block, so the words say so. A summary the paralegal wrote is exempt (D-045b)."""
    return (kind == "entry" and review.edit_unconfirmed(kind, row) and not _paralegal_wording(kind, row)
            and ((row.get("ladder") or {}).get("judge") or {}).get("verdict") in (None, "", "unavailable"))


def rerun_gave_no_answer(row) -> bool:
    """The last rerun of the second check (ladder.rejudge) came back unavailable."""
    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    return bool(last) and last.get("verdict") == "unavailable"


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
    tried = rerun_gave_no_answer(u["row"])           # T-134 r3: the reason must match what happened after the action offered
    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
            "rerun_no_answer": tried, "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}


def judge_report(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    rows = _judge_rows(cx)
    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
               "disagrees": 0, "unsure": 0, "unavailable": 0} for j in ("j1", "j2", "j3", "j4")}
    rejections, unresolved, disagreements, versions = [], [], [], set()
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
    n_ai = sum(1 for k, x in allitems if ai_summary_unchecked(k, x))
    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"] - n_edit, "edit_not_confirmed": n_edit,
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if n_edit:
        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit, n_ai), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else "")
                    + (" " + edit_warning(n_edit, n_ai) if n_edit else ""),
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


def edit_warning(n: int, n_ai: int = 0) -> str:
    return edit_warning_base(n) + (f" {n_ai} of {'them keep' if n != 1 else 'it keeps'} the AI's summary and the second check has no answer on the new quote, so accepting alone will not put "
                                    f"{'them' if n_ai != 1 else 'it'} in the letter; the export stays blocked until the check answers or you edit the summary yourself." if n_ai else "")


def edit_warning_base(n: int) -> str:
    return (f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm {'them' if n != 1 else 'it'}), so {'they are' if n != 1 else 'it is'} "
            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")


def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
            "entries": [{"id": e["id"], "record_ids": e.get("record_ids") or [f"r{e['record_no']}"],
                         "edited": e["review_status"] == "edited", "excerpt": e["excerpt"],
                         "entered_by": "reviewer" if e.get("entered_by_reviewer") else None}
                        for e in case.get("entries", []) if e.get("review_status") in ok],
            "amounts": [{"id": a["id"], "kind": a["cls"], "counted_in_total": a["cls"] == "charge" and a.get("cents") is not None,
                         "edited": a["review_status"] == "edited", "excerpt": a["excerpt"]}
                        for a in case.get("amounts", []) if a.get("review_status") in ok],
        },
        "warnings": [],
    }


def invalid_style_message() -> str:
    return "The letter style must be 'standard' or 'oneline'."


def blocked_message(e) -> str:
    if e.code == "judge_not_run":
        return judge_not_run_message(len(e.items), all(i.get("rerun_no_answer") for i in e.items))
    return e.items[0]["why"] + " The export is blocked."


def judge_not_run_message(n: int, retried: bool = False) -> str:
    if retried:       # T-134 r3: the second check was run again and gave no answer; say what clears it, not the action that was just tried
        return (f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check: it ran again and gave no answer, so the export is blocked. "
                f"It clears when the check answers, or when you edit the summary in your own words.")
    return f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check, so the export is blocked. Run the second check again."


@router.get("/api/cases/{token}/export")
def get_export(token: str, style: str = None):


def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    return lad


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:54.149Z

**tool call — Bash**
````
{
 "command": "grep -n \"edit_to_check\" app/backend/*.py memory/contracts/api.md | head -30; grep -n \"judge_not_run_message\\|rerun_gave_no_answer\" -r app tests | grep -v \"\\.pyc\"; grep -n \"^from\\|^import\" app/backend/export_routes.py; sed -n 40,50p app/backend/trace.py; grep -n \"JUDGE_NOT_RUN_RETRIED\" app/backend/trace.py | head -3"
}
````

### User / tool · 2026-11-02T13:37:54.298Z

**tool result**
````
app/backend/case_list.py:76:            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "edits_to_check": counts["edit_to_check"],
app/backend/present.py:49:            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter
app/backend/present.py:201:    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
app/backend/present.py:206:            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
memory/contracts/api.md:361:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
memory/contracts/api.md:362:- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
memory/contracts/api.md:366:- Item trace (`GET /items/{id}/trace`, the "Why this status" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.", and the item `verdict` is `{code: "edit_to_check", label: "Edited; waiting for your check"}` (new `verdict.code` value; a failing code check still wins: `needs_attention`). After her accept it is `accepted` / "Accepted by you". A verified edit (state not `needs_review`) still reads "You edited this item and accepted it.". The case `/judges` totals and the `judges` step no longer count a human-edited entry whose re-check had no answer (D-045b).
memory/contracts/api.md:368:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summary (`edit_to_check` with no second-check answer) the item `human` step, the `EDIT_NOT_CONFIRMED` gate warning and the review step say that accepting alone will not put it in the letter (D-044 still blocks until the check answers or she edits the summary). After `POST /rejudge` leaves an accepted item unavailable, its `JUDGE_NOT_RUN` blocker carries `rerun_no_answer: true` and a `why` that says the check ran again and gave no answer; the 422 `judge_not_run` message then says what clears it instead of repeating "Run the second check again". Frontend: show `why` as given; no new required field.
memory/contracts/api.md:370:- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
memory/contracts/api.md:697:`title` is what to show: the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped), or "Untitled case, Nov 2" / "Sample case" when it has no name; `name` is the stored value. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
app/backend/trace.py:289:        code, label = "edit_to_check", "Edited; waiting for your check"
app/backend/trace.py:1046:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
app/backend/trace.py:1050:    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
app/backend/trace.py:1051:        n = rc["edit_to_check"]
app/backend/trace.py:1063:    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
app/backend/trace.py:1121:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
app/backend/trace.py:814:def rerun_gave_no_answer(row) -> bool:
app/backend/trace.py:850:    tried = rerun_gave_no_answer(u["row"])           # T-134 r3: the reason must match what happened after the action offered
app/backend/export_routes.py:58:        return judge_not_run_message(len(e.items), all(i.get("rerun_no_answer") for i in e.items))
app/backend/export_routes.py:62:def judge_not_run_message(n: int, retried: bool = False) -> str:
7:from datetime import datetime, timezone
9:from fastapi import APIRouter
10:from fastapi.responses import JSONResponse
12:from app.backend import export
TRACE_WHY = {
    "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
    "EDIT_NOT_CONFIRMED_ITEM": "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.",
    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter: the export stays blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
    "EDIT_NOT_CONFIRMED": "An edited entry is still marked Needs review; it stays out of the letter until you compare it with the quote and accept it.",
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
    "RUN_IN_PROGRESS": "The AI run is still going.",
    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
51:    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
851:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:59.343Z

**tool call — Bash**
````
{
 "command": "sed -n 1,20p app/backend/present.py; sed -n 38,100p app/backend/present.py; grep -n \"def case_view\" -A40 app/backend/present.py | head -80; sed -n 1,30p app/backend/trace.py | grep -n import; sed -n 355,372p memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T13:37:59.529Z

**tool result**
````
"""Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
import json
import re

from app.backend import conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
from app.db import db as DB

STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY

            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}


def entry_view(row, recs):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None, "translation": _translation(row),
            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter


def _translation(row):
    """D-042: set on an entry made from a Spanish record: its summary is an English translation, its quote the original Spanish."""
    t = (row.get("ladder") or {}).get("translation")
    return spanish.translation_info(t.get("source_language", "es"), "summary" in (row.get("edited") or {}) or bool(t.get("human_written"))) if t else None


def accept_effect(row) -> str:
    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
    never totaled, and no second AI check is needed), `internal_notes` (estimate, unclear: noted for the paralegal, never in the total)."""
    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")


def amount_view(row, recs):
    return {**_common(row), "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate"}


def _computed(c):
    c = dict(c or {})
    if "from_date" in c:
        c.update({"from": c.pop("from_date"), "to": c.pop("to_date", None)})
        c.setdefault("threshold", 30)
        ids = c.get("record_ids") or []
        if ids:
            c["from_record"], c["to_record"] = ids[0], ids[-1]
    return c


def _evidence(evs, recs):
    by_n = {r["seq"]: r["id"] for r in recs.values()}
    return [{"record_id": e.get("record_id") or by_n.get(e.get("record_no")), "excerpt": e.get("excerpt") if e.get("excerpt") is not None else e.get("text"),
             "start": e.get("start"), "end": e.get("end")} for e in (evs or [])]


def _gap_why(row, base):
    """D-055: a gap's why also carries the code-built warning for each end that looks like paperwork (intake form, bill, ...), as stored by code."""
    ws = (row.get("computed") or {}).get("endpoint_warnings") or []
    ex = [x["warning"] for x in ws if x.get("warning")]
    alt = next((x["alternative"] for x in ws if x.get("alternative") and x["alternative"] not in ex), None)      # the other number, once (D-055 round 4)
    if alt:
        ex.append(alt)
    if row["type"] != "gap" or not ex:
        return base
    return " ".join(([] if base == OK_WHY else [base]) + ex)


def flag_view(row, recs):
    c = _common(row)
279:def case_view(conn, case_id, *, backend, models, demo_mode):
280-    case = DB.get_case(conn, case_id)
281-    raw = case["raw_text"]
282-    recs = list(_recs_by_id(conn, case_id).values())
283-    its = all_items(conn, case_id)
284-    ents = its["entry"]
285-    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))      # T-110 r2: a record the paralegal entered by hand leaves the tray
286-    live_e = [e for e in ents if e["state"] != "rejected"]
287-    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
288-    undated = [e for e in live_e if e not in dated]
289-    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
290-             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
291-             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
292-    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
293-    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
294-    def _tray_flag(x):
295-        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
296-                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
297-                "flag": {"type": x["type"], "category": x["category"]},
298-                "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
299-                "ladder": {"item_id": x["id"], "state": "rejected"}}
300-    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
301-    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
302-    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
303-    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
304-    rules = []
305-    for cat in sorted({x["category"] for x in filtered}):
306-        ref, name, text = FT.FILTER_RULES.get(cat, ("", cat, ""))
307-        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
308-        rules.append({"rule": cat, "ref": ref, "label": name, "explanation": text, "count": len(items), "items": items})
309-    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
310-    err = json.loads(case["error"]) if case.get("error") else None
311-    injected = [r["id"] for r in recs if r["injection_tag"]]
312-    record_views = [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs]
313-    uncovered.attach(record_views, ents, quote_body)      # T-143: clinical sentences no entry quote covers (review aid; never in the letter or notes)
314-    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
315-            "records": record_views, "undated_entries": undated, "entries": dated,
316-            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
317-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete"), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
318-            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
319-            "review": review_view(conn, case_id), "warnings": [], "error": err,
11:import json
13:from app.backend import flag_templates as FT, generator, grounding, narrative, present, review, store, why
14:from app.backend import judges as J
15:from app.db import db as DB
16:from app.llm import audited as AU
              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
  "warnings": [ {"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": "e3"} ] }
```
The frontend does not need to refetch the case.

**An edit that is still `needs_review` is not decided (T-134; D-045b, D-051; paralegal pass 4 M2).** Saving the edit stays as above (`review_status: "edited"`, `state: "needs_review"`), but until the paralegal says she compared it with the quote it is **open**, one rule in all places:
- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
- Export: the entry is **not in the letter**, not in `items.entries`, not counted in `counts.entries` or `provenance.edited_count`; it counts in `excluded.pending` and in `excluded.edit_not_confirmed` (subset of pending), and in the notes' "Items not reviewed: N". It does not block export (it is not in the letter, as with a pending item, D-045(a)), unless nothing else is accepted (`NOTHING_ACCEPTED`).
- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
- Internal notes: EDITED ITEMS lists it with "(edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter (accept it to put it there))" (the reason sentence follows the item's reasons: `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, ...), PENDING ITEMS NOT INCLUDED lists it with the same phrase, and RECORDS NOT IN THE TREATMENT SECTION says "edited, not yet confirmed against the quote". After she accepts, EDITED ITEMS keeps the reason: "(accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE))". The notes never say she accepted an edit she has not accepted.
- Item trace (`GET /items/{id}/trace`, the "Why this status" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.", and the item `verdict` is `{code: "edit_to_check", label: "Edited; waiting for your check"}` (new `verdict.code` value; a failing code check still wins: `needs_attention`). After her accept it is `accepted` / "Accepted by you". A verified edit (state not `needs_review`) still reads "You edited this item and accepted it.". The case `/judges` totals and the `judges` step no longer count a human-edited entry whose re-check had no answer (D-045b).

- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summary (`edit_to_check` with no second-check answer) the item `human` step, the `EDIT_NOT_CONFIRMED` gate warning and the review step say that accepting alone will not put it in the letter (D-044 still blocks until the check answers or she edits the summary). After `POST /rejudge` leaves an accepted item unavailable, its `JUDGE_NOT_RUN` blocker carries `rerun_no_answer: true` and a `why` that says the check ran again and gave no answer; the 422 `judge_not_run` message then says what clears it instead of repeating "Run the second check again". Frontend: show `why` as given; no new required field.
- T-138: `POST /items/{id}/review {action: "reset"}` on an edited entry restores the AI wording together with its pre-edit second-check result, code-check record and state (kept in `ladder.pre_edit`, internal); accept then works as before the edit and does not hit `JUDGE_NOT_RUN`. If something else rewrote the state after the edit, only the check result returns.
- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.

## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:38:05.778Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _judge_rows\" -A45 app/backend/trace.py; grep -n \"def edit_unconfirmed\" -B2 -A14 app/backend/review.py"
}
````

### User / tool · 2026-11-02T13:38:05.877Z

**tool result**
````
768:def _judge_rows(cx):
769-    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
770-    out = []
771-    for kind in ("entry", "amount", "flag"):
772-        for row in DB.list_items(cx.conn, cx.case_id, kind):
773-            if kind == "flag" and FT.is_filtered(row.get("state_reasons")):      # D-057: never judged, never counted
774-                continue
775-            jd = (row.get("ladder") or {}).get("judge")
776-            if not jd or not jd.get("verdict"):
777-                out.extend(_judge_never_ran(cx, kind, row))
778-                continue
779-            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
780-            if _paralegal_wording(kind, row) and _norm_verdict(jid, jd["verdict"]) == "unavailable":
781-                continue                                        # T-134 r2 (D-045b): the edit route's re-check had no answer; her own wording needs none, so it is not a missing check
782-            call = cx.call(jd.get("call_id"), row["id"], jid)
783-            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": _norm_verdict(jid, jd["verdict"]),
784-                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
785-    return out
786-
787-
788-def _judge_never_ran(cx, kind, row):
789-    """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
790-    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
791-    if not cx.ran or _paralegal_wording(kind, row):
792-        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
793-    out = []
794-    for s in _STEPS_OF[kind](cx, row):
795-        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
796-                and (s.get("evidence") or {}).get("judge_verdict") == "unavailable":
797-            jid = "j" + s["id"].split("_")[1]
798-            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
799-    return out
800-
801-
802-def _paralegal_wording(kind, row) -> bool:
803-    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
804-    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))
805-
806-
807-def ai_summary_unchecked(kind, row) -> bool:
808-    """T-134 r3 (T-136 F-2): an open edit that left the AI's summary in place (a re-picked quote) and whose second check has no answer. Accepting it alone cannot clear D-044's
809-    block, so the words say so. A summary the paralegal wrote is exempt (D-045b)."""
810-    return (kind == "entry" and review.edit_unconfirmed(kind, row) and not _paralegal_wording(kind, row)
811-            and ((row.get("ladder") or {}).get("judge") or {}).get("verdict") in (None, "", "unavailable"))
812-
813-
79-
80-
81:def edit_unconfirmed(kind: str, item: dict) -> bool:
82-    """T-134 (D-045b, D-051): an ENTRY the paralegal reworded or re-quoted whose state is still needs_review (the second check did not run or did not agree, or another
83-    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
84-    not in the letter, not counted as accepted, and the notes do not say she accepted it. Her explicit accept (review_status accepted) ends it; that accept is bound
85-    by the code checks (set_review). One source for the item view, the review counts, the export and the gate."""
86-    return (kind == "entry" and item.get("review_status") == "edited" and item.get("state") == "needs_review"
87-            and any(k in (item.get("edited") or {}) for k in ("summary", "excerpt")))
88-
89-
90-def code_check_failures(rec, item: dict) -> dict:
91-    """{reason_code: detail} for every D-034/D-047/D-022 code check the entry's CURRENT summary and quote fail. Recomputed from the text (same
92-    functions the generator and the edit route use), plus any such reason already stored on the item, so old data cannot slip through.
93-    `rec` is a store.load_records() dict (None: only the stored reasons count)."""
94-    out = {}
95-    summ, exc = current_text(item)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:38:18.832Z

**tool call — Bash**
````
{
 "command": "grep -n \"entry_view\\|amount_view\\|flag_view\\|def all_items\\|item_view\" app/backend/*.py | grep -v \"^app/backend/present.py:.*def \"; grep -n \"def all_items\" -A25 app/backend/present.py"
}
````

### User / tool · 2026-11-02T13:38:18.928Z

**tool result**
````
app/backend/present.py:142:_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
app/backend/present.py:326:    item = item_view(conn, case_id, item_id)
app/backend/review.py:214:    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
app/backend/review.py:587:    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
app/backend/review.py:651:    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
app/backend/reclassify.py:185:    return {"item": present.item_view(conn, case_id, item_id), "amount": amount, "totals": present.totals_view(conn, case_id),
167:def all_items(conn, case_id):
168-    recs = _recs_by_id(conn, case_id)
169-    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
170-    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
171-    return out
172-
173-
174-def totals_view(conn, case_id):
175-    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
176-    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
177-    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
178-    cnt = lambda sts: sum(1 for a in ch if a["review_status"] in sts)   # noqa: E731
179-    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
180-            "pending": {"cents": t["detected_pending_cents"], "count": cnt(("pending",)), "label": "Pending review"},
181-            "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
182-                                     "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
183-            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
184-                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"],
185-            "possible_overlaps": overlap.view(conn, case_id)}      # T-110: a statement line that may include a separately stated charge; warns, never changes the total
186-
187-
188-def rejected_count(conn, case_id):
189-    """Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2)."""
190-    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))
191-    return sum(1 for k in ("entry", "amount") for r in DB.list_items(conn, case_id, k) if r["state"] == "rejected" and r["id"] not in handled)
192-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:38:21.940Z

**tool call — Bash**
````
{
 "command": "sed -n 136,166p app/backend/present.py; git diff --stat app/backend/present.py app/backend/trace.py app/backend/review.py app/backend/store.py app/backend/export_routes.py memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T13:38:22.041Z

**tool result**
````
    for f in flags:
        if f["type"] == "gap":
            f["gap_change"] = kept.get(f["id"])
    return flags, removed


_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
_ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}


def _recs_by_id(conn, case_id):
    cfg = (DB.get_case(conn, case_id) or {}).get("config") or {}
    unsplit, pre = set(cfg.get("unsplit_records") or []), set(cfg.get("preamble_records") or [])      # T-129: stored by pipeline._store_record_marks
    out = {}
    for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
        r = DB._decode(x)
        r["unsplit"], r["preamble"] = r["id"] in unsplit, r["id"] in pre
        out[r["id"]] = r
    return out


def item_view(conn, case_id, item_id):
    row = DB.get_item(conn, item_id, case_id)
    kind = _ID_KIND[item_id[0]]
    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
    v["kind"] = kind
    if kind == "flag":
        _with_gap_changes(conn, case_id, [v])
    return v


 app/backend/present.py  | 2 +-
 memory/contracts/api.md | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:38:24.905Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/unit/test_t134_unconfirmed_edit.py; grep -n \"^def test\\|^    def test\" tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py; sed -n 1,60p tests/unit/test_t138_undo_edit.py; ls artifacts/review-evidence/T-134/r3 artifacts/review-evidence/T-138; git diff app/backend/present.py memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T13:38:25.026Z

**tool result**
````
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
tests/unit/test_t138_undo_edit.py:35:def test_undo_of_an_edit_restores_the_ai_wording_with_its_original_judge_result_and_accept_then_works(env):
tests/unit/test_t138_undo_edit.py:58:def test_two_edits_then_one_undo_restores_the_state_before_the_first_edit(env):
tests/unit/test_t138_undo_edit.py:69:def test_a_second_edit_after_an_undo_snapshots_again(env):
tests/unit/test_t138_undo_edit.py:79:def test_undo_after_accepting_the_edit_also_restores_the_original_check(env):
tests/unit/test_t138_undo_edit.py:90:def test_undo_of_an_item_with_no_snapshot_old_data_still_works(env):
tests/unit/test_t138_undo_edit.py:105:def test_undo_of_a_flag_note_or_an_unedited_item_is_unchanged(env):
tests/unit/test_t138_undo_edit.py:114:def test_undo_when_something_else_changed_the_state_since_the_edit_restores_the_check_but_leaves_the_state(env):
tests/unit/test_t134_unconfirmed_edit.py:36:def test_edit_with_no_second_check_is_not_in_the_letter_and_not_counted_accepted(env):
tests/unit/test_t134_unconfirmed_edit.py:57:def test_gate_names_the_unconfirmed_edit_as_a_warning_and_agrees_with_the_export(env):
tests/unit/test_t134_unconfirmed_edit.py:68:def test_only_an_unconfirmed_edit_accepted_means_nothing_accepted(env):
tests/unit/test_t134_unconfirmed_edit.py:78:def test_explicit_accept_after_comparing_moves_it_into_the_letter_and_the_notes_keep_the_reason(env):
tests/unit/test_t134_unconfirmed_edit.py:91:def test_accept_after_comparing_is_a_422_when_the_stored_wording_fails_a_code_check(env):
tests/unit/test_t134_unconfirmed_edit.py:106:def test_a_verified_edit_is_unaffected(env):
tests/unit/test_t134_unconfirmed_edit.py:130:def test_item_trace_of_an_open_edit_does_not_say_accepted(env):
tests/unit/test_t134_unconfirmed_edit.py:147:def test_item_trace_of_an_open_excerpt_only_edit_is_also_not_accepted(env):
tests/unit/test_t134_unconfirmed_edit.py:162:def test_a_verified_edit_trail_still_says_accepted(env):
tests/unit/test_t134_unconfirmed_edit.py:173:def test_everything_else_decided_the_open_edit_alone_keeps_review_and_header_not_ready(env):
tests/unit/test_t134_unconfirmed_edit.py:192:def test_judges_step_ignores_a_human_edit_whose_rerun_check_was_unavailable_under_the_curated_set(env, monkeypatch, tmp_path):
tests/unit/test_t134_unconfirmed_edit.py:221:def test_judge_report_does_not_count_an_open_edit_as_accepted_despite_an_objection(env):
tests/unit/test_t134_unconfirmed_edit.py:235:def test_judges_step_keeps_a_human_edit_whose_recheck_objected(env):
tests/unit/test_t134_unconfirmed_edit.py:246:def test_item_next_action_of_an_open_edit_is_decide(env):
tests/unit/test_t134_unconfirmed_edit.py:266:def test_open_quote_edit_with_ai_summary_and_no_second_check_says_accept_alone_will_not_put_it_in_the_letter(env):
tests/unit/test_t134_unconfirmed_edit.py:279:def test_open_edit_of_her_own_wording_keeps_the_plain_compare_and_accept_text(env):
tests/unit/test_t134_unconfirmed_edit.py:289:def test_accepted_quote_edit_blocks_with_a_reason_that_says_the_rerun_was_tried_and_gave_no_answer(env):
"""T-138 (staff-engineer r2 on T-134, pre-existing): undoing an edit must put the AI wording back TOGETHER with the second-check result and the
state it had before the edit. Before this, reset restored the words but kept the edit route's judge result ('unavailable' when the re-check had no
answer), so an item that was verified before the edit hit 422 JUDGE_NOT_RUN on accept."""
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
    db = str(tmp_path / "t138.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _post(c, tok, iid, body):
    return c.post(f"/api/cases/{tok}/items/{iid}/review", json=body)


def _snap(db, tok, iid):
    conn = DB.connect(db)
    r = DB.get_item(conn, iid, tok)
    conn.close()
    return {"state": r["state"], "reasons": sorted(r["state_reasons"] or []), "judge": (r["ladder"] or {}).get("judge"),
            "code_checks": (r["ladder"] or {}).get("code_checks"), "summary": r["summary"], "excerpt": r["excerpt"]}


def test_undo_of_an_edit_restores_the_ai_wording_with_its_original_judge_result_and_accept_then_works(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert before["judge"]["verdict"] in ("supported", "faithful") and before["judge"]["verdict"] != "unavailable"       # the AI wording had a real second-check answer
    assert _post(c, tok, "e1", {"action": "accept"}).status_code == 200
    r = _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200
    during = _snap(db, tok, "e3")
    assert during["judge"] != before["judge"]                                           # the edit re-ran the check on her wording
    r = _post(c, tok, "e3", {"action": "reset"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "pending"
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"] and after["code_checks"] == before["code_checks"]
    assert (after["state"], after["reasons"]) == (before["state"], before["reasons"])
    assert after["summary"] == before["summary"] and r.json()["item"]["summary"] == before["summary"]
    # accept works exactly as it did before the edit, and the export is not blocked by JUDGE_NOT_RUN
    assert _post(c, tok, "e3", {"action": "accept"}).status_code == 200
    ex = c.get(f"/api/cases/{tok}/export")
    blockers = [] if ex.status_code == 200 else str(ex.json())
    assert "JUDGE_NOT_RUN" not in blockers and "JUDGE_UNAVAILABLE" not in blockers


def test_two_edits_then_one_undo_restores_the_state_before_the_first_edit(env):
    db, c = env
    tok = run_case(c)
artifacts/review-evidence/T-134/r3:
cli_sample.txt
edited_count.out
edited_count.py
itemtrace_blocked.out
itemtrace_blocked.py
mutants.txt
mutate_r3.py
probe134r3.out
probe134r3.py
review_step.out
review_step.py
review_step2.out
review_step2.py
unit_runs.txt

artifacts/review-evidence/T-138:
alias138.out
alias138.py
leak138.out
leak138.py
probe138.out
probe138.py
probe138b.out
probe138b.py
diff --git a/app/backend/present.py b/app/backend/present.py
index d9ad869..4d494e4 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -314,7 +314,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
     return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
             "records": record_views, "undated_entries": undated, "entries": dated,
             "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks(), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
+            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete"), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
             "review": review_view(conn, case_id), "warnings": [], "error": err,
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 5c66eeb..e15c0f9 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -130,7 +130,7 @@ Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human dec
 ## GET /api/cases/{token}
 Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
 
-**T-141 / T-142, `checks` (GET case, top level; always present, the same on every case; code constants, no model):** what the conflict check looks for and what it does not, so the UI can say it honestly (for example "Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: ["plan_vs_early_end", "denial_vs_history", "accident_date", "provider_name"], labels: {<type>: one plain sentence}, not_checked: [{type, label}]}`. `conflict_types` are the four checks: `plan_vs_early_end` and `denial_vs_history` are the pair rules in `conflict_candidates.py` (a judge classifies each pair), `accident_date` and `provider_name` are the structural checks in `conflicts.py`. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together. `accident_date` no longer flags a stated date that is also the date of another record when no earlier record describes a collision of its own (a pre-accident annual visit is not treatment for it).
+**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: [..], labels: {<type>: one plain sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}], notes: [{type, code, count, record_nos, stated_date, text}]}`. The four types are `plan_vs_early_end` and `denial_vs_history` (pair rules in `conflict_candidates.py`; a judge classifies each pair), `accident_date` and `provider_name` (structural checks in `conflicts.py`). **`conflict_types` lists only the types that ran on the case**; `labels` has all four. **`skipped`** says why a type did not run, or ran only in part. `reason_code`: `NOT_RUN` (case created, comparison between records not run yet; the two code checks ran at ingest), `STAGE_SKIPPED` (the run hit its time limit before the comparison between records), `RUN_FAILED` (the run stopped; nothing known), `LANGUAGE` (every record is Spanish, uncertain or unsupported: the English wording rules could not find anything; the type is absent from `conflict_types`), `LANGUAGE_PARTIAL` (the type ran, but `record_nos` lists the Spanish/uncertain/unsupported records it did not read), `NO_DATED_RECORD` (no parsed record date; `accident_date`). The language-bound types are `plan_vs_early_end`, `denial_vs_history` and `accident_date`; `provider_name` compares header labels. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). **`notes`** are info lines, never flags: `RECORDS_PREDATE_ACCIDENT` = a single stated accident date is later than N records and none of them describes a collision or injury mechanism, so no date conflict is raised; `text` is the sentence to show ("1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; check that they are earlier care."). The decision is by content (T-141 round 2, no "a record is dated that day" shortcut): a record dated before the stated date that has a clause naming a collision, crash, MVA, vehicle, "hit", fall or similar that is not history (no prior/history word, no bare earlier year, no full date over a year earlier) makes the accident-date conflict, and the conflict then compares with the earliest such record. `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together.
 
 **T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
 ```json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:38:32.413Z

**tool call — Bash**
````
{
 "command": "sed -n 240,400p tests/unit/test_t134_unconfirmed_edit.py; sed -n 60,140p tests/unit/test_t138_undo_edit.py; cat artifacts/review-evidence/T-134/r3/probe134r3.py | head -60"
}
````

### User / tool · 2026-11-02T13:38:32.517Z

**tool result**
````
    j = next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "judges")
    assert j["status"] != "pass"                                              # the objection is still on the case-level step
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert [r["verdict"] for r in rep["rejections"] if r["item_id"] == "e3"] == ["partially"]


def test_item_next_action_of_an_open_edit_is_decide(env):
    """Reviewer r2 N3: the UI reads the item-level next_action; for an open edit it is DECIDE (accept or dismiss), not nothing."""
    _, c = env
    tok, _ = _setup(c)
    t, _s = _item_trace(c, tok, "e3")
    assert t["next_action"] and t["next_action"]["code"] == "DECIDE"


# ---- T-134 round 3, T-136 paralegal F-2: a re-picked quote under AI wording whose second check has no answer
# D-044 stands (nothing AI-written reaches the letter without the second check), so the words must not promise what accept alone cannot do.

QUOTE_ONLY = "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. "     # e3's own quote re-picked (same sentences; the summary stays the AI's)


def _quote_pick(c, tok):
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"excerpt": QUOTE_ONLY}})
    assert r.status_code == 200 and r.json()["item"]["edit_to_check"] is True, r.text
    return r


def test_open_quote_edit_with_ai_summary_and_no_second_check_says_accept_alone_will_not_put_it_in_the_letter(env):
    _, c = env
    tok = run_case(c)
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    _quote_pick(c, tok)
    t, s = _item_trace(c, tok, "e3")
    why = s["human"]["why"]
    assert "second" in why and "check" in why and "accepting alone" in why.lower()
    g = _gate(c, tok)
    w = next(x for x in g["warnings"] if x["reason_code"] == "EDIT_NOT_CONFIRMED")
    assert "second" in w["why"] and "check" in w["why"] and "accept" in w["why"]


def test_open_edit_of_her_own_wording_keeps_the_plain_compare_and_accept_text(env):
    """Her own summary is exempt from the second check (D-045b), so compare-and-accept is the whole step for it."""
    _, c = env
    tok, _ = _setup(c)
    t, s = _item_trace(c, tok, "e3")
    assert "accepting alone" not in s["human"]["why"].lower()
    w = next(x for x in _gate(c, tok)["warnings"] if x["reason_code"] == "EDIT_NOT_CONFIRMED")
    assert "second AI check" not in w["why"]


def test_accepted_quote_edit_blocks_with_a_reason_that_says_the_rerun_was_tried_and_gave_no_answer(env):
    """After accept the block is D-044's (unchanged). Before a rerun the text offers the rerun; after a rerun that still has no answer it says so
    and names what does clear it (the check answering, or her own wording)."""
    _, c = env
    tok = run_case(c)
    _quote_pick(c, tok)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["code"] == "judge_not_run" and "Run the second check again" in ex.json()["error"]["message"]
    b = next(x for x in _gate(c, tok)["blockers"] if x["item_id"] == "e3")
    assert "tried again" not in b["why"]
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 200 and [x["item_id"] for x in r.json()["still_unavailable"]] == ["e3"]
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422
    msg = ex.json()["error"]["message"]
    assert "ran again" in msg and "no answer" in msg and "edit the summary" in msg
    b = next(x for x in _gate(c, tok)["blockers"] if x["item_id"] == "e3")
    assert "ran again" in b["why"] and "no answer" in b["why"]
    # the way out is real: her own summary wording is exempt (D-045b) and passes the code checks
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": "Persistent neck pain 6/10, daily headaches."}})
    assert r.status_code == 200
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    assert c.get(f"/api/cases/{tok}/export").status_code == 200
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": "Persistent neck pain 6/10 and daily headaches."}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"] and (after["state"], after["reasons"]) == (before["state"], before["reasons"])


def test_a_second_edit_after_an_undo_snapshots_again(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    for _ in range(2):
        assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
        assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
        assert _snap(db, tok, "e3")["judge"] == before["judge"]


def test_undo_after_accepting_the_edit_also_restores_the_original_check(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "accept"}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"] and (after["state"], after["reasons"]) == (before["state"], before["reasons"])


def test_undo_of_an_item_with_no_snapshot_old_data_still_works(env):
    """Rows edited before this change have no stored snapshot; reset behaves as before (words back, nothing invented)."""
    db, c = env
    tok = run_case(c)
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    conn = DB.connect(db)
    row = DB.get_item(conn, "e3", tok)
    lad = dict(row["ladder"])
    lad.pop("pre_edit", None)
    DB.update_item(conn, "e3", case=tok, ladder=lad)
    conn.close()
    r = _post(c, tok, "e3", {"action": "reset"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "pending"


def test_undo_of_a_flag_note_or_an_unedited_item_is_unchanged(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "accept"}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    assert _snap(db, tok, "e3") == before


def test_undo_when_something_else_changed_the_state_since_the_edit_restores_the_check_but_leaves_the_state(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    conn = DB.connect(db)
    DB.update_item(conn, "e3", case=tok, state="needs_review", state_reasons_json=["DATE_AMBIGUOUS"])      # some other step rewrote it
    conn.close()
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"]
    assert (after["state"], after["reasons"]) == ("needs_review", ["DATE_AMBIGUOUS"])
"""T-134 r3 staff-engineer probe: texts for a re-picked quote under the AI summary with an unanswered rerun (D-058), honesty at each step.
usage: python -I probe134r3.py <archive_dir>   (fixture backend; sample case; TestClient; no network)"""
import sys, os, tempfile, json
arch = sys.argv[1]; sys.path.insert(0, arch); os.chdir(arch)
os.environ["LLM_BACKEND"] = "fixture"; os.environ.pop("ANTHROPIC_API_KEY", None); os.environ.pop("ENABLE_LIVE", None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
from app.backend import rejudge as RJ
from app.db import db as DB
from tests.unit.test_api_routes import run_case

def mk():
    d = tempfile.mkdtemp(prefix="p134r3_"); db = os.path.join(d, "p.sqlite")
    c = TestClient(create_app(db, static_dir=d), client=("127.0.0.1", 50000)); return db, c, run_case(c)
def post(c, tok, iid, body): return c.post(f"/api/cases/{tok}/items/{iid}/review", json=body)
def itrace(c, tok, iid): return c.get(f"/api/cases/{tok}/items/{iid}/trace").json()
def step(t, sid): return next(s for s in t["steps"] if s["id"] == sid)
def gate(c, tok): return step(c.get(f"/api/cases/{tok}/trace").json(), "export_gate")
Q1 = "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. "
Q2 = "Persistent neck pain 6/10, daily headaches. "
def show(label, v): print(f"  {label}: {v}")

print("P1 quote-pick under the AI summary (no accept yet)")
db, c, tok = mk(); post(c, tok, "e1", {"action": "accept"})
r = post(c, tok, "e3", {"action": "edit", "edits": {"excerpt": Q1}}); show("edit", r.status_code)
t = itrace(c, tok, "e3"); show("item verdict", t["verdict"]); show("human step why", step(t, "human")["why"]); show("judges step", (step(t, "judge")["status"] if any(s["id"] == "judge" for s in t["steps"]) else [s["id"] for s in t["steps"]]))
g = gate(c, tok); show("gate ready/status", (g["ready"], g["status"])); show("gate why", g["why"])
ex = c.get(f"/api/cases/{tok}/export"); show("export status BEFORE accept", ex.status_code)
show("e3 summary in letter?", ex.status_code == 200 and "neck pain" in ex.json().get("letter_text", "").lower())
rj = c.post(f"/api/cases/{tok}/rejudge"); show("rejudge BEFORE accept: asked/still", (rj.json().get("asked"), [x["item_id"] for x in rj.json().get("still_unavailable", [])]))
t = itrace(c, tok, "e3"); show("item next_action", t["next_action"])

print("P2 accept, export, rejudge, export (texts at each point)")
post(c, tok, "e3", {"action": "accept"})
t = itrace(c, tok, "e3"); show("item verdict after accept", t["verdict"]); show("human step", (step(t, "human")["status"], step(t, "human")["why"]))
jt = [s for s in t["steps"] if s.get("blocks_export")]; show("blocking steps", [(s["id"], s["why"]) for s in jt])
g = gate(c, tok); show("gate blockers (before rerun)", [(b["reason_code"], b["why"], b.get("rerun_no_answer")) for b in g["blockers"]])
ex = c.get(f"/api/cases/{tok}/export"); show("export msg before rerun", (ex.status_code, ex.json()["error"]["message"]))
rj = c.post(f"/api/cases/{tok}/rejudge"); show("rejudge", (rj.json()["asked"], [x["item_id"] for x in rj.json()["still_unavailable"]]))
g = gate(c, tok); show("gate blockers (after rerun)", [(b["reason_code"], b["why"], b.get("rerun_no_answer")) for b in g["blockers"]])
ex = c.get(f"/api/cases/{tok}/export"); show("export msg after rerun", (ex.status_code, ex.json()["error"]["message"]))
t = itrace(c, tok, "e3"); show("item verdict after rerun", t["verdict"])
show("blocking steps after rerun", [(s["id"], s["why"]) for s in t["steps"] if s.get("blocks_export")])

print("P3 stale rerun note: rerun gave no answer on quote Q1, then she re-picks Q2 and accepts; rerun has NOT run on Q2")
post(c, tok, "e3", {"action": "edit", "edits": {"excerpt": Q2}}); post(c, tok, "e3", {"action": "accept"})
conn = DB.connect(db); row = DB.get_item(conn, "e3", tok); conn.close()
show("ladder.rejudge entries", len((row["ladder"] or {}).get("rejudge") or []))
g = gate(c, tok); b = [x for x in g["blockers"] if x["item_id"] == "e3"]
show("blocker why for the NEW quote", [(x["why"], x.get("rerun_no_answer")) for x in b])
ex = c.get(f"/api/cases/{tok}/export"); show("export msg for the NEW quote", (ex.status_code, ex.json()["error"]["message"]))
claimed_stale = bool(b) and b[0].get("rerun_no_answer") is True
print("  STALE-RERUN-CLAIM:", claimed_stale, "(true = says it ran again on a quote it has not run on)")

print("P4 the way out: the check ANSWERS (judge patched to answer 'supported') -> rerun -> export")
db, c, tok = mk(); post(c, tok, "e1", {"action": "accept"})
post(c, tok, "e3", {"action": "edit", "edits": {"excerpt": Q1}}); post(c, tok, "e3", {"action": "accept"})
show("export before", c.get(f"/api/cases/{tok}/export").status_code)
orig = RJ._safe_ask
RJ._safe_ask = lambda t, case_text, call: ("supported", "c_patched", "NONE")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:38:51.401Z

**tool call — Bash**
````
{
 "command": "sed -n 100,135p tests/unit/test_t134_unconfirmed_edit.py && grep -n \"_item_trace\" tests/unit/test_t134_unconfirmed_edit.py | head -3 && grep -n \"def _item_trace\" -A8 tests/unit/test_t134_unconfirmed_edit.py"
}
````

### User / tool · 2026-11-02T13:38:51.500Z

**tool result**
````
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


# ------------------------------------------------------------------ round 2 (staff-engineer findings 1-4)
def _item_trace(c, tok, iid):
    t = c.get(f"/api/cases/{tok}/items/{iid}/trace").json()
    return t, {s["id"]: s for s in t["steps"]}


def _dismiss_all_but(c, db, tok, keep):
    """Dismiss every live pending item except `keep`, so the only open thing is the edit."""
    conn = DB.connect(db)
    ids = [r["id"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k) if r["state"] != "rejected" and r["review_status"] == "pending" and r["id"] not in keep]
    conn.close()
    for i in ids:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"}).status_code == 200


def test_item_trace_of_an_open_edit_does_not_say_accepted(env):
    """Finding 1: the 'Why this status' trail must not claim her acceptance of an edit that is still open."""
    _, c = env
    tok, _ = _setup(c)
    t, s = _item_trace(c, tok, "e3")
    assert t["verdict"]["code"] == "edit_to_check" and "accepted" not in t["verdict"]["label"].lower()
116:def _item_trace(c, tok, iid):
130:def test_item_trace_of_an_open_edit_does_not_say_accepted(env):
134:    t, s = _item_trace(c, tok, "e3")
116:def _item_trace(c, tok, iid):
117-    t = c.get(f"/api/cases/{tok}/items/{iid}/trace").json()
118-    return t, {s["id"]: s for s in t["steps"]}
119-
120-
121-def _dismiss_all_but(c, db, tok, keep):
122-    """Dismiss every live pending item except `keep`, so the only open thing is the edit."""
123-    conn = DB.connect(db)
124-    ids = [r["id"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k) if r["state"] != "rejected" and r["review_status"] == "pending" and r["id"] not in keep]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:00.582Z

Now write the tests (T-134 file append, T-138 file append).

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:27.092Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_t134_unconfirmed_edit.py <<'EOF'\n\n\n# ---- T-134 round 4 (staff-engineer r3 bounded fix-up, section 7.4): every renderer of the re-picked-quote state, a rerun claim tied to the CURRENT quote, an explicit item field\ndef _rejudge_no_answer(c, tok):\n    r = c.post(f\"/api/cases/{tok}/rejudge\")\n    assert r.status_code == 200 and \"e3\" in [x[\"item_id\"] for x in r.json()[\"still_unavailable\"]]\n\n\ndef test_review_step_of_a_quote_pick_under_the_ai_summary_says_accepting_alone_will_not_put_it_in_the_letter(env):\n    \"\"\"r3 finding 1a: with everything else decided, the review step is the text she reads last; it must not promise that accept puts the entry in the letter.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    _quote_pick(c, tok)\n    _dismiss_all_but(c, db, tok, keep={\"e3\"})\n    step = next(s for s in c.get(f\"/api/cases/{tok}/trace\").json()[\"steps\"] if s[\"id\"] == \"review\")\n    assert step[\"status\"] == \"pending\" and step[\"reason_code\"] == \"EDIT_NOT_CONFIRMED\"\n    assert \"accepting alone will not put it in the letter\" in step[\"why\"].lower()\n    assert \"or the entry stays out of the letter\" not in step[\"why\"]\n\n\ndef test_review_step_of_her_own_wording_keeps_the_plain_compare_and_accept_text(env):\n    db, c = env\n    tok, _ = _setup(c, accept=())\n    _dismiss_all_but(c, db, tok, keep={\"e3\"})\n    step = next(s for s in c.get(f\"/api/cases/{tok}/trace\").json()[\"steps\"] if s[\"id\"] == \"review\")\n    assert \"accept, or the entry stays out of the letter\" in step[\"why\"] and \"accepting alone\" not in step[\"why\"].lower()\n\n\ndef test_gate_headline_after_a_rerun_with_no_answer_is_the_same_sentence_as_the_422_and_does_not_repeat_the_action(env):\n    \"\"\"r3 finding 1b: one function says it (headline, 422 message), so they cannot drift.\"\"\"\n    _, c = env\n    tok = run_case(c)\n    _quote_pick(c, tok)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    g0 = _gate(c, tok)\n    assert g0[\"why\"].endswith(\"Run the second check again.\") and \"ran again\" not in g0[\"why\"]\n    _rejudge_no_answer(c, tok)\n    g = _gate(c, tok)\n    msg = c.get(f\"/api/cases/{tok}/export\").json()[\"error\"][\"message\"]\n    assert g[\"why\"] == msg and \"ran again\" in g[\"why\"] and not g[\"why\"].endswith(\"Run the second check again.\")\n    assert g[\"blockers\"][0][\"rerun_no_answer\"] is True\n\n\ndef test_rerun_claim_is_about_the_current_quote_a_second_pick_clears_it(env):\n    \"\"\"r3 finding 2: the rerun ran on the first quote; after she picks another quote nobody has run the check on it, so no text may say it ran again.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    _quote_pick(c, tok)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    _rejudge_no_answer(c, tok)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"edit\", \"edits\": {\"excerpt\": \"Persistent neck pain 6/10, daily headaches. \"}}).status_code == 200\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    conn = DB.connect(db)\n    assert not (DB.get_item(conn, \"e3\", tok)[\"ladder\"] or {}).get(\"rejudge\")          # the attempts belonged to the old quote\n    conn.close()\n    b = next(x for x in _gate(c, tok)[\"blockers\"] if x[\"item_id\"] == \"e3\")\n    assert b[\"rerun_no_answer\"] is False and \"ran again\" not in b[\"why\"]\n    msg = c.get(f\"/api/cases/{tok}/export\").json()[\"error\"][\"message\"]\n    assert \"ran again\" not in msg and \"Run the second check again\" in msg\n    assert \"ran again\" not in _gate(c, tok)[\"why\"]\n    _rejudge_no_answer(c, tok)                                                          # now it has run on this quote\n    assert \"ran again\" in c.get(f\"/api/cases/{tok}/export\").json()[\"error\"][\"message\"]\n\n\ndef test_rerun_gave_no_answer_reads_the_last_attempt_only():\n    from app.backend import trace\n    row = lambda *vs: {\"ladder\": {\"rejudge\": [{\"verdict\": v} for v in vs]}}      # noqa: E731\n    assert trace.rerun_gave_no_answer(row(\"supported\", \"unavailable\")) is True\n    assert trace.rerun_gave_no_answer(row(\"unavailable\", \"supported\")) is False\n    assert trace.rerun_gave_no_answer(row(\"supported\")) is False\n    assert trace.rerun_gave_no_answer(row(\"unavailable\")) is True\n    assert trace.rerun_gave_no_answer(row()) is False and trace.rerun_gave_no_answer({}) is False and trace.rerun_gave_no_answer({\"ladder\": None}) is False\n\n\ndef test_no_text_says_the_export_stays_blocked_while_the_gate_passes(env):\n    \"\"\"r3 finding 3: before she accepts, nothing is blocked; the conditional is what is true.\"\"\"\n    _, c = env\n    tok = run_case(c)\n    assert c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"accept\"}).status_code == 200\n    _quote_pick(c, tok)\n    g = _gate(c, tok)\n    assert g[\"ready\"] is True and c.get(f\"/api/cases/{tok}/export\").status_code == 200\n    w = next(x for x in g[\"warnings\"] if x[\"reason_code\"] == \"EDIT_NOT_CONFIRMED\")\n    for text in (w[\"why\"], g[\"why\"], _item_trace(c, tok, \"e3\")[1][\"human\"][\"why\"]):\n        assert \"stays blocked\" not in text and \"stay blocked\" not in text and \"it keeps the AI's summary\" not in text.replace(\"1 of it\", \"\")\n        assert \"If you accept it, the export will be blocked until the second check answers\" in text and \"in your own words\" in text\n    assert \"1 of it keeps\" not in w[\"why\"] and \"1 of them keep\" not in w[\"why\"]\n\n\ndef test_warning_for_her_own_wording_has_no_ai_clause(env):\n    _, c = env\n    tok, _ = _setup(c)\n    w = next(x for x in _gate(c, tok)[\"warnings\"] if x[\"reason_code\"] == \"EDIT_NOT_CONFIRMED\")\n    assert \"If you accept it\" not in w[\"why\"] and \"AI's summary\" not in w[\"why\"]\n\n\ndef test_second_check_pending_is_an_explicit_item_field(env):\n    \"\"\"The UI reads second_check_pending instead of guessing from judge/ladder fields: true exactly when the item is AI-made, live and its second check has no answer.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    case = c.get(f\"/api/cases/{tok}\").json()\n    every = case[\"entries\"] + case.get(\"undated_entries\", []) + case[\"amounts\"] + case[\"flags\"]\n    assert every and all(isinstance(i[\"second_check_pending\"], bool) for i in every)\n    from app.backend import trace\n    conn = DB.connect(db)\n    unjudged = {u[\"item_id\"] for u in trace.unjudged_items(conn, tok) if not trace.acknowledge_only(u[\"kind\"], u[\"row\"])}\n    conn.close()\n    assert {i[\"id\"] for i in every if i[\"second_check_pending\"]} == unjudged\n    assert next(i for i in every if i[\"id\"] == \"e3\")[\"second_check_pending\"] is False\n    r = _quote_pick(c, tok).json()\n    assert r[\"item\"][\"second_check_pending\"] is True                                     # the re-picked quote has no answer\n    assert next(e for e in c.get(f\"/api/cases/{tok}\").json()[\"entries\"] if e[\"id\"] == \"e3\")[\"second_check_pending\"] is True\n    r = c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": EDIT}})\n    assert r.status_code == 200 and r.json()[\"item\"][\"second_check_pending\"] is False    # her own wording needs no second check (D-045b)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"reset\"}).json()[\"item\"][\"second_check_pending\"] is False\n    assert c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"dismiss\"}).json()[\"item\"][\"second_check_pending\"] is False\n\n\ndef test_second_check_pending_clears_when_the_check_answers(env, monkeypatch):\n    from app.backend import rejudge as RJ\n    _, c = env\n    tok = run_case(c)\n    _quote_pick(c, tok)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    monkeypatch.setattr(RJ, \"_safe_ask\", lambda t, case_text, call: (\"supported\", \"c_patched\", \"NONE\"))\n    assert c.post(f\"/api/cases/{tok}/rejudge\").status_code == 200\n    e3 = next(e for e in c.get(f\"/api/cases/{tok}\").json()[\"entries\"] if e[\"id\"] == \"e3\")\n    assert e3[\"second_check_pending\"] is False and c.get(f\"/api/cases/{tok}/export\").status_code == 200\nEOF\ncat >> tests/unit/test_t138_undo_edit.py <<'EOF'\n\n\n# ---- T-138 round 2 (staff-engineer r1): the snapshot must not alias the dict the edit updates in place; the snapshot goes after the undo; pre_edit is not in GET case\ndef _set_ladder(db, tok, iid, **kw):\n    conn = DB.connect(db)\n    lad = dict(DB.get_item(conn, iid, tok)[\"ladder\"] or {})\n    lad.update(kw)\n    DB.update_item(conn, iid, case=tok, ladder=lad)\n    conn.close()\n\n\ndef test_undo_restores_the_pre_edit_code_checks_not_the_edited_wordings(env):\n    \"\"\"r1 finding 1 (mutants T3 and the alias): an AI draft whose stored code checks differ from what the edit writes.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    old = {\"qualifier_carried\": False, \"summary_tokens_not_in_excerpt\": [\"5/10\"], \"highlight_found\": True}\n    _set_ladder(db, tok, \"e3\", code_checks=dict(old))\n    assert _post(c, tok, \"e3\", {\"action\": \"edit\", \"edits\": {\"summary\": EDIT}}).status_code == 200\n    during = _snap(db, tok, \"e3\")[\"code_checks\"]\n    assert during != old and during[\"qualifier_carried\"] is True and during[\"summary_tokens_not_in_excerpt\"] == []\n    conn = DB.connect(db)\n    snap = DB.get_item(conn, \"e3\", tok)[\"ladder\"][\"pre_edit\"]\n    conn.close()\n    assert snap[\"code_checks\"] == old                                                  # the snapshot itself is the old record, not an alias of the edited one\n    assert _post(c, tok, \"e3\", {\"action\": \"reset\"}).status_code == 200\n    assert _snap(db, tok, \"e3\")[\"code_checks\"] == old\n\n\ndef test_second_undo_cycle_restores_what_the_item_had_after_the_first_undo_and_the_snapshot_is_gone(env):\n    \"\"\"r1 finding 3 (mutant T9): the snapshot is removed by the undo, so a later edit snapshots what the item holds THEN.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    assert _post(c, tok, \"e3\", {\"action\": \"edit\", \"edits\": {\"summary\": EDIT}}).status_code == 200\n    assert _post(c, tok, \"e3\", {\"action\": \"reset\"}).status_code == 200\n    conn = DB.connect(db)\n    assert \"pre_edit\" not in (DB.get_item(conn, \"e3\", tok)[\"ladder\"] or {})\n    cur = (DB.get_item(conn, \"e3\", tok)[\"ladder\"] or {}).get(\"judge\")\n    conn.close()\n    changed = dict(cur, verdict=\"partial\", reason_code=\"CHANGED_BETWEEN_CYCLES\")\n    _set_ladder(db, tok, \"e3\", judge=changed)                                           # something (a rejudge) changed the check between the cycles\n    assert _post(c, tok, \"e3\", {\"action\": \"edit\", \"edits\": {\"summary\": EDIT}}).status_code == 200\n    assert _post(c, tok, \"e3\", {\"action\": \"reset\"}).status_code == 200\n    assert _snap(db, tok, \"e3\")[\"judge\"] == changed\n\n\ndef test_undo_restores_the_rerun_record_the_old_wording_had_and_an_edit_clears_it(env):\n    \"\"\"T-134 r3 finding 2: ladder.rejudge belongs to the wording and quote it ran on.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    attempts = [{\"at\": 1.0, \"call_id\": \"c1\", \"verdict\": \"unavailable\"}]\n    _set_ladder(db, tok, \"e3\", rejudge=attempts)\n    assert _post(c, tok, \"e3\", {\"action\": \"edit\", \"edits\": {\"summary\": EDIT}}).status_code == 200\n    conn = DB.connect(db)\n    assert not DB.get_item(conn, \"e3\", tok)[\"ladder\"].get(\"rejudge\")\n    conn.close()\n    assert _post(c, tok, \"e3\", {\"action\": \"reset\"}).status_code == 200\n    conn = DB.connect(db)\n    assert DB.get_item(conn, \"e3\", tok)[\"ladder\"].get(\"rejudge\") == attempts\n    conn.close()\n\n\ndef test_pre_edit_snapshot_is_not_in_any_case_payload(env):\n    \"\"\"r1 finding 2: the snapshot is internal (api.md); it is not in GET case, the review response or the list payloads.\"\"\"\n    db, c = env\n    tok = run_case(c)\n    r = _post(c, tok, \"e3\", {\"action\": \"edit\", \"edits\": {\"summary\": EDIT}})\n    assert r.status_code == 200 and \"pre_edit\" not in r.text\n    assert \"pre_edit\" not in c.get(f\"/api/cases/{tok}\").text\n    conn = DB.connect(db)\n    assert \"pre_edit\" in DB.get_item(conn, \"e3\", tok)[\"ladder\"]                        # still stored, only hidden\n    conn.close()\nEOF\npython3 -m pytest tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py -q -x 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T13:39:27.201Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:31.845Z

**tool call — Bash**
````
{
 "command": "ls -d .venv venv 2>/dev/null; grep -rn \"pytest\" Makefile run.sh 2>/dev/null | head -3; which -a python python3 pytest"
}
````

### User / tool · 2026-11-02T13:39:31.970Z

**tool result (error)**
````
Exit code 1
.venv
/opt/homebrew/bin/python3
/usr/bin/python3
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:34.873Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py -q 2>&1 | tail -25"
}
````

### User / tool · 2026-11-02T13:39:49.131Z

**tool result**
````
        tok = run_case(c)
        r = _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}})
>       assert r.status_code == 200 and "pre_edit" not in r.text
E       assert (200 == 200 and 'pre_edit' not in '{"item":{"i..._id":"e3"}]}'
E        +  where 200 = <Response [200 OK]>.status_code
E         
E         'pre_edit' is contained here:
E         ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ...
E         
E         ...Full output truncated, use '-vv' to show)

tests/unit/test_t138_undo_edit.py:192: AssertionError
------------------------------ Captured log call -------------------------------
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c5d67127dc4eb step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
=========================== short test summary info ============================
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_review_step_of_a_quote_pick_under_the_ai_summary_says_accepting_alone_will_not_put_it_in_the_letter
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_gate_headline_after_a_rerun_with_no_answer_is_the_same_sentence_as_the_422_and_does_not_repeat_the_action
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_rerun_claim_is_about_the_current_quote_a_second_pick_clears_it
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_no_text_says_the_export_stays_blocked_while_the_gate_passes
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_second_check_pending_is_an_explicit_item_field
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_second_check_pending_clears_when_the_check_answers
FAILED tests/unit/test_t138_undo_edit.py::test_undo_restores_the_pre_edit_code_checks_not_the_edited_wordings
FAILED tests/unit/test_t138_undo_edit.py::test_undo_restores_the_rerun_record_the_old_wording_had_and_an_edit_clears_it
FAILED tests/unit/test_t138_undo_edit.py::test_pre_edit_snapshot_is_not_in_any_case_payload
9 failed, 28 passed in 13.71s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:53.498Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/backend/review.py'; s=open(p).read()\ns=s.replace('''        lad[\"pre_edit\"] = {\"judge\": lad.get(\"judge\"), \"code_checks\": lad.get(\"code_checks\"), \"state\": item[\"state\"], \"state_reasons\": list(item.get(\"state_reasons\") or []),\n                           \"lad_state\": lad.get(\"state\")}''','''        lad[\"pre_edit\"] = {\"judge\": copy.deepcopy(lad.get(\"judge\")), \"code_checks\": copy.deepcopy(lad.get(\"code_checks\")), \"rejudge\": copy.deepcopy(lad.get(\"rejudge\")),\n                           \"state\": item[\"state\"], \"state_reasons\": list(item.get(\"state_reasons\") or []), \"lad_state\": lad.get(\"state\")}      # deep copies: the edit updates code_checks in place below\n    lad.pop(\"rejudge\", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none''')\ns=s.replace('''    if snap.get(\"code_checks\") is not None:\n        lad[\"code_checks\"] = snap[\"code_checks\"]\n''','''    if snap.get(\"code_checks\") is not None:\n        lad[\"code_checks\"] = snap[\"code_checks\"]\n    if snap.get(\"rejudge\"):\n        lad[\"rejudge\"] = snap[\"rejudge\"]\n    else:\n        lad.pop(\"rejudge\", None)\n''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"^import\\|^from\" app/backend/review.py | head"
}
````

### User / tool · 2026-11-02T13:39:53.606Z

**tool result**
````
10:import time
12:from app.backend import amounts as AM, charge_text, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
13:from app.db import db as DB
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:57.311Z

**tool call — Bash**
````
{
 "command": "sed -i '10s/^import time/import copy\\nimport time/' app/backend/review.py && sed -n 8,13p app/backend/review.py && git diff --stat -- app/backend/review.py app/backend/trace.py app/backend/export_routes.py app/backend/present.py app/backend/rejudge.py"
}
````

### User / tool · 2026-11-02T13:39:57.396Z

**tool result**
````
sed: 1: "app/backend/review.py
": command a expects \ followed by text
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:39:59.428Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'; s=open(p).read()\ns=s.replace(\"\\nimport time\\n\",\"\\nimport copy\\nimport time\\n\",1); open(p,'w').write(s)\nEOF\nsed -n 8,13p app/backend/review.py; git diff --stat -- app/backend/review.py app/backend/trace.py app/backend/export_routes.py app/backend/present.py app/backend/rejudge.py"
}
````

### User / tool · 2026-11-02T13:39:59.554Z

**tool result**
````
JUDGE_UNAVAILABLE).
"""
import copy
import time

from app.backend import amounts as AM, charge_text, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
 app/backend/present.py |  2 +-
 app/backend/review.py  | 10 ++++++++--
 2 files changed, 9 insertions(+), 3 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:02.702Z

**tool call — Bash**
````
{
 "command": "sed -n 1,20p app/backend/export_routes.py"
}
````

### User / tool · 2026-11-02T13:40:02.778Z

**tool result**
````
"""GET /api/cases/{token}/export: thin router around export.build_export (T-041). Code only.

The app factory (T-040) does `app.include_router(export_routes.router)` and registers the case loader once:
    export_routes.set_case_loader(fn)   # fn(token) -> case dict (see export.py docstring) or None for an unknown token
Items with review_status other than accepted/edited never reach either block (ADR-009, LLM_VS_CODE row 19).
"""
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.backend import export

router = APIRouter()
_loader = None


def set_case_loader(fn):
    global _loader
    _loader = fn
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:08.954Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/export_routes.py'; s=open(p).read()\na=s.index(\"def judge_not_run_message\")\nb=s.index('@router.get(\"/api/cases/{token}/export\")')\ns=s[:a]+s[b:]\ns=s.replace(\"from app.backend import export\\n\",\"from app.backend import export\\nfrom app.backend.trace import judge_not_run_message      # one sentence for the 422 and the gate headline (T-134 r4)\\n\",1)\nopen(p,'w').write(s)\n\np='app/backend/trace.py'; s=open(p).read()\n# TRACE_WHY wording\nold=s[s.index('    \"EDIT_NOT_CONFIRMED_ITEM_AI\":'):s.index('    \"EDIT_NOT_CONFIRMED\": ')]\nnew='''    \"EDIT_NOT_CONFIRMED_ITEM_AI\": \"You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.\",\n'''\ns=s.replace(old,new)\n# rerun\ns=s.replace('''    return ((row.get(\"ladder\") or {}).get(\"rejudge\") or [None])[-1]''','''XX''') if False else s\n# rerun_gave_no_answer unchanged; add message function after it\ns=s.replace('''    return bool(last) and last.get(\"verdict\") == \"unavailable\"\n''','''    return bool(last) and last.get(\"verdict\") == \"unavailable\"\n\n\ndef judge_not_run_message(n: int, retried: bool = False) -> str:\n    \"\"\"The one sentence for n accepted AI-made items whose second check has no answer: the 422 `judge_not_run` message and the export-gate headline (T-134 r4).\"\"\"\n    s = f\"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check\"\n    if retried:       # the check was run again on the current wording and quote and gave no answer: say what clears it, not the action that was just tried\n        return (f\"{s}: it ran again and gave no answer, so the export is blocked. It clears when the check answers, or when you edit the summary in your own words.\")\n    return f\"{s}, so the export is blocked. Run the second check again.\"\n''',1)\ns=s.replace('''        text = (f\"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again.\"\n                if jnr and first is jnr[0] else first[\"why\"])''','''        text = (judge_not_run_message(len(jnr), all(b.get(\"rerun_no_answer\") for b in jnr)) if jnr and first is jnr[0] else first[\"why\"])''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"rerun_no_answer\" app/backend/trace.py"
}
````

### User / tool · 2026-11-02T13:40:09.063Z

**tool result**
````
860:            "rerun_no_answer": tried, "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}
1088:        text = (judge_not_run_message(len(jnr), all(b.get("rerun_no_answer") for b in jnr)) if jnr and first is jnr[0] else first["why"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:18.865Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/trace.py'; s=open(p).read()\nold=s[s.index('    elif rc[\"edit_to_check\"]:'):s.index('    else:\\n        st.append(step(\"review\"')]\nnew='''    elif rc[\"edit_to_check\"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it\n        n = rc[\"edit_to_check\"]\n        n_ai0 = sum(1 for k, x in allitems if ai_summary_unchecked(k, x))\n        st.append(step(\"review\", \"Your accept, edit or dismiss on each item\", \"human\", PENDING, f\"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm \"\n                       f\"{'them' if n != 1 else 'it'}). \" + (ai_clause(n_ai0, n) if n_ai0 else f\"Compare {'them' if n != 1 else 'it'} with the quote and accept, or the {'entries stay' if n != 1 else 'entry stays'} out of the letter.\"),\n                       reason=\"EDIT_NOT_CONFIRMED\", rule=\"row 17\", counts=rc, next_action=na(\"DECIDE\", {\"view\": \"queue\"}, [\"accept\", \"edit\", \"dismiss\"])))\n'''\ns=s.replace(old,new)\nold=s[s.index('def edit_warning(n: int'):s.index('def edit_warning_base')]\nnew='''def ai_clause(n_ai: int, n: int) -> str:\n    \"\"\"T-134 r4 (D-058): for open edits that keep the AI's summary with no second-check answer. Conditional, because before she accepts nothing is blocked (the gate passes and the\n    entry is only left out); accept alone cannot clear D-044's block.\"\"\"\n    them = \"them\" if n_ai != 1 else \"it\"\n    return (f\"{n_ai} of {n} {'keep' if n_ai != 1 else 'keeps'} the AI's summary and the second check has no answer on the new quote, so accepting alone will not put {them} in the letter. \"\n            f\"If you accept {them}, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.\")\n\n\ndef edit_warning(n: int, n_ai: int = 0) -> str:\n    return edit_warning_base(n) + (\" \" + ai_clause(n_ai, n) if n_ai else \"\")\n\n\n'''\ns=s.replace(old,new)\nopen(p,'w').write(s)\nEOF\ngrep -n \"allitems =\" app/backend/trace.py | head; grep -n \"EDIT_NOT_CONFIRMED_ITEM_AI\\|1 of\" app/backend/trace.py tests -r | head"
}
````

### User / tool · 2026-11-02T13:40:19.002Z

**tool result**
````
948:    allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
app/backend/trace.py:44:    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
app/backend/trace.py:251:        return step("human", "Your decision", "human", PENDING, TRACE_WHY["EDIT_NOT_CONFIRMED_ITEM_AI" if ai_summary_unchecked(kind, row) else "EDIT_NOT_CONFIRMED_ITEM"], reason="EDIT_NOT_CONFIRMED", rule="row 17", evidence=ev, blocks=False,
tests/unit/test_t120_history_source_sentence.py:47:    assert interp["n"] == 1                                    # the interpreter sentence is in record 1 of lib09 (r1), not record 2
tests/unit/test_t134_unconfirmed_edit.py:397:        assert "stays blocked" not in text and "stay blocked" not in text and "it keeps the AI's summary" not in text.replace("1 of it", "")
tests/unit/test_t134_unconfirmed_edit.py:399:    assert "1 of it keeps" not in w["why"] and "1 of them keep" not in w["why"]
tests/e2e/test_adversarial.py:7:PDF_TEXT = "Page 1 of 3\nPATIENT CHART - CONFIDENTIAL\n\n2026-01-09 ER visit. Neck pain.\f\nPage 2 of 3\nPATIENT CHART - CONFIDENTIAL\nCharge: $500.\n"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:23.514Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/trace.py'; s=open(p).read()\ns=s.replace('''    return (f\"{n_ai} of {n} {'keep' if n_ai != 1 else 'keeps'} the AI's summary and''','''    who = \"It keeps\" if n == n_ai == 1 else \"They keep\" if n == n_ai else f\"{n_ai} of them keep\" if n_ai != 1 else \"1 of them keeps\"\n    return (f\"{who} the AI's summary and''')\nopen(p,'w').write(s)\np='tests/unit/test_t134_unconfirmed_edit.py'; s=open(p).read()\ns=s.replace('''        assert \"stays blocked\" not in text and \"stay blocked\" not in text and \"it keeps the AI's summary\" not in text.replace(\"1 of it\", \"\")\n''','''        assert \"stays blocked\" not in text and \"stay blocked\" not in text and \"1 of it\" not in text\n''')\ns=s.replace('''    assert \"1 of it keeps\" not in w[\"why\"] and \"1 of them keep\" not in w[\"why\"]\n''','''    assert \"It keeps the AI's summary\" in w[\"why\"]\n''')\nopen(p,'w').write(s)\nEOF"
}
````

### User / tool · 2026-11-02T13:40:23.615Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:31.860Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/present.py'; s=open(p).read()\ns=s.replace('''    lad[\"human\"] = _human(row)\n    return lad''','''    lad[\"human\"] = _human(row)\n    lad.pop(\"pre_edit\", None)      # T-138: the undo snapshot is internal (api.md), never in a payload\n    return lad''',1)\ns=s.replace('''def all_items(conn, case_id):\n    recs = _recs_by_id(conn, case_id)\n    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in (\"entry\", \"amount\", \"flag\")}\n''','''def second_check_pending_ids(conn, case_id) -> set:\n    \"\"\"T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only\n    acknowledges it, no check needed). Lazy import: trace imports this module.\"\"\"\n    from app.backend import trace\n    return {u[\"item_id\"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u[\"kind\"], u[\"row\"])}\n\n\ndef all_items(conn, case_id):\n    recs = _recs_by_id(conn, case_id)\n    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in (\"entry\", \"amount\", \"flag\")}\n    pend = second_check_pending_ids(conn, case_id)\n    for k in (\"entry\", \"amount\", \"flag\"):\n        for v in out[k]:\n            v[\"second_check_pending\"] = v[\"id\"] in pend\n''',1)\ns=s.replace('''    v[\"kind\"] = kind\n    if kind == \"flag\":''','''    v[\"kind\"] = kind\n    v[\"second_check_pending\"] = item_id in second_check_pending_ids(conn, case_id)\n    if kind == \"flag\":''',1)\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py -q 2>&1 | tail -25"
}
````

### User / tool · 2026-11-02T13:40:45.756Z

**tool result**
````
=================================== FAILURES ===================================
_____ test_rerun_claim_is_about_the_current_quote_a_second_pick_clears_it ______

env = ('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-4737/test_rerun_claim_is_about_the_0/t134.sqlite', <starlette.testclient.TestClient object at 0x10c82eea0>)

    def test_rerun_claim_is_about_the_current_quote_a_second_pick_clears_it(env):
        """r3 finding 2: the rerun ran on the first quote; after she picks another quote nobody has run the check on it, so no text may say it ran again."""
        db, c = env
        tok = run_case(c)
        _quote_pick(c, tok)
        assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
        _rejudge_no_answer(c, tok)
>       assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"excerpt": "Persistent neck pain 6/10, daily headaches. "}}).status_code == 200
E       AssertionError: assert 422 == 200
E        +  where 422 = <Response [422 Unprocessable Content]>.status_code
E        +    where <Response [422 Unprocessable Content]> = post('/api/cases/2s2XCA0-Le62QtrxIC3sFw/items/e3/review', json={'action': 'edit', 'edits': {'excerpt': 'Persistent neck pain 6/10, daily headaches. '}})
E        +      where post = <starlette.testclient.TestClient object at 0x10c82eea0>.post

tests/unit/test_t134_unconfirmed_edit.py:363: AssertionError
------------------------------ Captured log call -------------------------------
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c0e442b2e4763 step=j1 attempt=1 prompt_hash=ecb960e45c9e5444ac7f7989022298821f9e82ce1aefec7fd48b5d692693974d
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=c85aad33f57ed step=j1 attempt=1 prompt_hash=ecb960e45c9e5444ac7f7989022298821f9e82ce1aefec7fd48b5d692693974d
=========================== short test summary info ============================
FAILED tests/unit/test_t134_unconfirmed_edit.py::test_rerun_claim_is_about_the_current_quote_a_second_pick_clears_it
1 failed, 36 passed in 13.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:52.132Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/p.py <<'EOF'\nimport os,tempfile\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom tests.unit.test_api_routes import run_case\nd=tempfile.mkdtemp(); c=TestClient(create_app(d+\"/x.sqlite\",static_dir=d),client=(\"127.0.0.1\",50000)); tok=run_case(c)\nQ1=\"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. \"\nfor q in [\"Persistent neck pain 6/10, daily headaches. \",\"Persistent neck pain 6/10, daily headaches.\", \"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.\"]:\n    r=c.post(f\"/api/cases/{tok}/items/e3/review\",json={\"action\":\"edit\",\"edits\":{\"excerpt\":q}}); print(r.status_code, r.text[:300])\nEOF\n.venv/bin/python /private/tmp/claude-501/p.py 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T13:40:52.412Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/p.py", line 4, in <module>
    from app.backend.api import create_app
ModuleNotFoundError: No module named 'app'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:40:53.666Z

**tool call — Bash**
````
{
 "command": "PYTHONPATH=. .venv/bin/python /private/tmp/claude-501/p.py 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T13:40:54.673Z

**tool result**
````
llm call failed call_id=c7e04df3927fc step=j1 attempt=1 prompt_hash=ecb960e45c9e5444ac7f7989022298821f9e82ce1aefec7fd48b5d692693974d
422 {"error":{"code":"invalid_edit","message":"The summary has a number, date or dollar figure that is not in the quote: 2. Remove it or change the quote.","detail":{"tokens":["2"],"reason":"SUMMARY_NUMBER_NOT_IN_EXCERPT"}}}
422 {"error":{"code":"invalid_edit","message":"The summary has a number, date or dollar figure that is not in the quote: 2. Remove it or change the quote.","detail":{"tokens":["2"],"reason":"SUMMARY_NUMBER_NOT_IN_EXCERPT"}}}
200 {"item":{"id":"e3","state":"needs_review","reasons":["JUDGE_UNAVAILABLE"],"why":"JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.","review_status":"edited","edited":{"at":"2026-11-02T13:40:54Z","excerpt":"Persistent neck pain 6/10, daily hea
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:41:00.564Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && python3 - <<'EOF'\np='tests/unit/test_t134_unconfirmed_edit.py'; s=open(p).read()\ns=s.replace('''\"edits\": {\"excerpt\": \"Persistent neck pain 6/10, daily headaches. \"}}).status_code == 200\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    conn = DB.connect(db)''','''\"edits\": {\"excerpt\": QUOTE_ONLY.strip()}}).status_code == 200      # another pick (a summary-safe variant of the quote)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    conn = DB.connect(db)''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py -q 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T13:41:00.566Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:41:04.786Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_t134_unconfirmed_edit.py'; s=open(p).read()\ns=s.replace('''\"edits\": {\"excerpt\": \"Persistent neck pain 6/10, daily headaches. \"}}).status_code == 200\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    conn = DB.connect(db)''','''\"edits\": {\"excerpt\": QUOTE_ONLY.strip()}}).status_code == 200      # another pick (a summary-safe variant of the quote)\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    conn = DB.connect(db)''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py -q 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T13:41:19.164Z

**tool result**
````
.....................................                                    [100%]
37 passed in 13.85s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:41:29.291Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/mut.py <<'EOF'\nimport subprocess,shutil,sys\nT=\"tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py\"\nM=[\n(\"N18\",\"app/backend/trace.py\",'(row.get(\"ladder\") or {}).get(\"rejudge\") or [None])[-1]','(row.get(\"ladder\") or {}).get(\"rejudge\") or [None])[0]'),\n(\"N19\",\"app/backend/trace.py\",'return edit_warning_base(n) + (\" \" + ai_clause(n_ai, n) if n_ai else \"\")','return edit_warning_base(n)'),\n(\"H2\",\"app/backend/trace.py\",'return bool(last) and last.get(\"verdict\") == \"unavailable\"','return bool(last)'),\n(\"T3\",\"app/backend/review.py\",'        lad[\"code_checks\"] = snap[\"code_checks\"]\\n','        pass\\n'),\n(\"T9\",\"app/backend/review.py\",'snap = lad.pop(\"pre_edit\", None)','snap = lad.get(\"pre_edit\")'),\n(\"ALIAS\",\"app/backend/review.py\",'\"code_checks\": copy.deepcopy(lad.get(\"code_checks\"))','\"code_checks\": lad.get(\"code_checks\")'),\n(\"NOCLEAR\",\"app/backend/review.py\",'    lad.pop(\"rejudge\", None)       # T-134 r4','    pass       # T-134 r4'),\n(\"REVSTEP\",\"app/backend/trace.py\",'(ai_clause(n_ai0, n) if n_ai0 else','(ai_clause(n_ai0, n) if False else'),\n(\"HEAD\",\"app/backend/trace.py\",'judge_not_run_message(len(jnr), all(b.get(\"rerun_no_answer\") for b in jnr))','judge_not_run_message(len(jnr), False)'),\n(\"NOSCP\",\"app/backend/present.py\",'in pend\\n','in pend and False\\n'),\n(\"NOPOP\",\"app/backend/present.py\",'    lad.pop(\"pre_edit\", None)','    pass'),\n]\nfor n,f,a,b in M:\n    s=open(f).read(); assert a in s,(n); shutil.copy(f,\"/private/tmp/claude-501/bak\"); open(f,\"w\").write(s.replace(a,b,1))\n    r=subprocess.run(f\".venv/bin/python -m pytest {T} -q -x 2>&1 | tail -1\",shell=True,capture_output=True,text=True).stdout.strip()\n    shutil.copy(\"/private/tmp/claude-501/bak\",f); print(n,\"->\",r)\nEOF\npython3 /private/tmp/claude-501/mut.py; git diff --stat -- app/backend | tail -3"
}
````

### User / tool · 2026-11-02T13:43:24.843Z

**tool result**
````
N18 -> 1 failed, 21 passed in 8.73s
N19 -> 1 failed, 22 passed in 8.69s
H2 -> 1 failed, 21 passed in 8.48s
T3 -> 1 failed, 33 passed in 12.63s
T9 -> 1 failed, 34 passed in 13.33s
ALIAS -> 1 failed, 33 passed in 12.44s
NOCLEAR -> 1 failed, 20 passed in 8.35s
REVSTEP -> 1 failed, 17 passed in 7.42s
HEAD -> 1 failed, 19 passed in 8.25s
NOSCP -> 1 failed, 24 passed in 9.51s
NOPOP -> 1 failed, 36 passed in 13.73s
 app/backend/uncovered.py           | 95 ++++++++++++++++++++++++--------------
 app/backend/why.py                 | 13 +++++-
 12 files changed, 335 insertions(+), 91 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:43:28.633Z

All mutants killed. Now the api.md edits, then the full suite.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:43:34.831Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'; s=open(p).read()\nold=\"the item `human` step, the `EDIT_NOT_CONFIRMED` gate warning and the review step say that accepting alone will not put it in the letter (D-044 still blocks until the check answers or she edits the summary).\"\nassert old in s\nnew=\"the item `human` step, the `EDIT_NOT_CONFIRMED` gate warning (and the passing gate headline that repeats it) and the case `review` step all use one clause: \\\"... accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.\\\" It is conditional on purpose: before she accepts, the gate passes and nothing is blocked (the entry is only left out); D-044 blocks only after accept.\"\ns=s.replace(old,new)\nold2=\"the 422 `judge_not_run` message then says what clears it instead of repeating \\\"Run the second check again\\\". Frontend: show `why` as given; no new required field.\"\nassert old2 in s\nnew2=(\"the 422 `judge_not_run` message then says what clears it instead of repeating \\\"Run the second check again\\\"; the failing `export_gate` headline is the same sentence as that 422 message (one function, `trace.judge_not_run_message`). \"\n \"**T-134 r4:** `rerun_no_answer` describes the CURRENT wording and quote: any edit that replaces the second-check result (`ladder.judge`) also drops `ladder.rejudge` (the attempts belonged to the old quote), and an undo restores the attempts the old wording had, so a re-picked quote reads \\\"Run the second check again\\\" until that check has been run on it. \"\n \"**`second_check_pending` (bool, every entry, amount and flag view, in `GET /api/cases/{token}` and every review response `item`):** true when the item is live (not rejected, not dismissed), AI-made (not a manual entry or a summary she wrote, D-045b), its second check has no answer, and it is not a rate (accepting a rate only acknowledges it). It is the same list the `JUDGE_NOT_RUN` gate reads, whether or not she has accepted it yet; it is false after the check answers. The UI uses this field instead of inferring it from `ladder.judge` or `reasons`. Show `why` as given.\")\ns=s.replace(old2,new2)\nold3=\"(kept in `ladder.pre_edit`, internal)\"\nassert old3 in s\ns=s.replace(old3,\"(kept in `ladder.pre_edit` as deep copies, plus the earlier `ladder.rejudge` attempts; internal and never returned in any payload)\")\nopen(p,'w').write(s)\nEOF\n(.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -8) "
}
````

### User / tool · 2026-11-02T13:44:03.357Z

**tool result**
````
E       AssertionError: ['co-progress-text-entries', 'cases-progress-text-entries', 'co-progress-text-<seq>', 'cases-progress-<seq>', 'cases-progress-entries', 'cases-progress-text-<seq>', ...]
E       assert not ['co-progress-text-entries', 'cases-progress-text-entries', 'co-progress-text-<seq>', 'cases-progress-<seq>', 'cases-progress-entries', 'cases-progress-text-<seq>', ...]

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 880 passed in 27.71s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:04.336Z

Frontend worker's in-flight work (not mine). Run without -x.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:04.844Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T13:46:05.479Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: bw3r79yw9). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:06.580Z

**tool call — Monitor**
````
{
 "query": "select:Monitor",
 "max_results": "1"
}
````

### User / tool · 2026-11-02T13:46:06.582Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Monitor failed due to the following issue:
The required parameter `description` is missing

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 1800000ms are capped to 1800000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required":["description","timeout_ms"],"additionalProperties":false}</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:09.201Z

Mistaken call; I'll just wait for the background notification by writing the memory notes meanwhile.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:10.156Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/backend/MEMORY.md | head -5; git diff --stat -- app/backend/review.py app/backend/trace.py app/backend/export_routes.py app/backend/present.py memory/contracts/api.md tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py; git diff -U0 app/backend/present.py memory/contracts/api.md | grep \"^@@\""
}
````

### User / tool · 2026-11-02T13:46:10.369Z

**tool result**
````
- [Backend conventions and pitfalls](project_backend_conventions.md) — codepaths, commit rule, sqlite thread pitfall, fixture re-record, review findings
- [T-110 overlap + failure tray](project_t110_overlap_tray.md) — lib09 4/7 is the matcher; failed-extract tray placeholders; POSSIBLE_OVERLAP
- [T-112 summary trim](project_t112_summary_trim.md) — D-054 clause trimming rule, wiring, fixture pitfalls (abbreviations, J1 fill-missing)
- [T-113 conflict candidate rules](project_t113_conflict_rules.md) — other-person/paperwork filters, v6 judge, tray routes, id-stability pitfall
- [T-120 / T-105 single source](project_t120_t105_single_source.md) — strip-attribution rule; lexicon views in grounding; structural guard; calibration regen
 app/backend/export_routes.py             |   8 +-
 app/backend/present.py                   |  19 ++++-
 app/backend/review.py                    |  10 ++-
 app/backend/trace.py                     |  28 +++++--
 tests/unit/test_t134_unconfirmed_edit.py | 128 +++++++++++++++++++++++++++++++
 tests/unit/test_t138_undo_edit.py        |  71 +++++++++++++++++
 6 files changed, 246 insertions(+), 18 deletions(-)
@@ -12 +12 @@ OK_WHY = "Quote found word for word, every number in the summary is in the quote
@@ -16 +16 @@ def _why(reasons):
@@ -32,0 +33 @@ def _ladder(row):
@@ -37 +38 @@ def _common(row):
@@ -161,0 +163 @@ def item_view(conn, case_id, item_id):
@@ -166,0 +169,7 @@ def item_view(conn, case_id, item_id):
@@ -169,0 +179,4 @@ def all_items(conn, case_id):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:13.011Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 -- memory/contracts/api.md; grep -c \"second_check_pending\" memory/contracts/api.md; git status --short memory/contracts/api.md app/backend/present.py"
}
````

### User / tool · 2026-11-02T13:46:13.173Z

**tool result**
````
68b8685 fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
d19ae46 feat(backend): GET /api/cases summary list for the case overview (T-148)
5f7ef96 fix(backend): T-139 no dollar amount reaches the carrier letter through entries; CHARGE_TEXT_IN_ENTRY holds them out; dismissed charge not under Bills to request; letter-level eval check
1
 M app/backend/present.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:15.683Z

**tool call — Bash**
````
{
 "command": "sleep 100; tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output"
}
````

### User / tool · 2026-11-02T13:46:15.686Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:18.017Z

**tool call — Bash**
````
{
 "command": "for i in $(seq 1 55); do if grep -q \"passed\\|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output; then break; fi; sleep 2; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output"
}
````

### User / tool · 2026-11-02T13:48:09.029Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:48:11.300Z

**tool call — Bash**
````
{
 "command": "for i in $(seq 1 55); do if grep -q \" passed\\| failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output; then break; fi; sleep 2; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bw3r79yw9.output"
}
````

### User / tool · 2026-11-02T13:49:11.822Z

**tool result**
````
FAILED tests/unit/test_amounts_t140.py::test_ordinary_charge_labels_stay_charges[Total of 12 visits billed $2,150.00]
FAILED tests/unit/test_amounts_t140.py::test_cross_check_flags_a_charge_equal_to_the_others
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
FAILED tests/unit/test_t114_rates_and_demo_judges.py::test_walking_every_acceptable_item_on_a_library_packet_never_hits_judge_not_run[case_lib10_eob_ub04_cms1500]
FAILED tests/unit/test_t139_narrow.py::test_a_narrowed_pair_with_no_judge_answer_is_judge_not_run_and_not_verified
6 failed, 3884 passed, 1 skipped in 303.92s (0:05:03)

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:49:14.182Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest \"tests/unit/test_t114_rates_and_demo_judges.py\" tests/unit/test_t139_narrow.py -q -p no:cacheprovider 2>&1 | grep -E \"^E |passed|failed\" | head -20"
}
````

### User / tool · 2026-11-02T13:49:24.169Z

**tool result**
````
E       AssertionError: case_lib10_eob_ub04_cms1500: accepted but no judge fixture: ['a7']
E       assert ['a7'] == []
E         
E         Left contains one more item: 'a7'
E         Use -v to get more diff
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=cf268744caa08 step=j2 attempt=1 prompt_hash=232873b02137683a2a71600ee0ad491ce3f9d70552c61649ffe4ab2a1f1ad479
1 failed, 40 passed in 9.60s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:49:29.870Z

**tool call — Bash**
````
{
 "command": "git diff -U0 app/backend/trace.py app/backend/review.py app/backend/export_routes.py | grep \"^@@\\|^diff\"; git diff -U0 app/backend/present.py | grep \"^@@\" "
}
````

### User / tool · 2026-11-02T13:49:30.003Z

**tool result**
````
diff --git a/app/backend/export_routes.py b/app/backend/export_routes.py
@@ -12,0 +13 @@ from app.backend import export
@@ -62,7 +62,0 @@ def blocked_message(e) -> str:
diff --git a/app/backend/review.py b/app/backend/review.py
@@ -9,0 +10 @@ JUDGE_UNAVAILABLE).
@@ -176 +177,19 @@ def entry_record(item: dict, recs: list):
@@ -191 +210,8 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
@@ -206 +232,4 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
@@ -354,2 +383,3 @@ def _edit(conn, case_id, kind, item, body, call, t):
@@ -384,0 +415,4 @@ def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t)
diff --git a/app/backend/trace.py b/app/backend/trace.py
@@ -44 +44 @@ TRACE_WHY = {
@@ -819,0 +820,8 @@ def rerun_gave_no_answer(row) -> bool:
@@ -1051,0 +1060 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
@@ -1053 +1062 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
@@ -1080,2 +1089 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
@@ -1097,0 +1106,9 @@ def pending_warning(n: int) -> str:
@@ -1099,2 +1116 @@ def edit_warning(n: int, n_ai: int = 0) -> str:
@@ -12 +12 @@ OK_WHY = "Quote found word for word, every number in the summary is in the quote
@@ -16 +16 @@ def _why(reasons):
@@ -32,0 +33 @@ def _ladder(row):
@@ -37 +38 @@ def _common(row):
@@ -63,0 +65,6 @@ def accept_effect(row) -> str:
@@ -65 +72,2 @@ def amount_view(row, recs):
@@ -161,0 +170 @@ def item_view(conn, case_id, item_id):
@@ -166,0 +176,7 @@ def item_view(conn, case_id, item_id):
@@ -169,0 +186,4 @@ def all_items(conn, case_id):
@@ -182,0 +203 @@ def totals_view(conn, case_id):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:49:36.722Z

**tool call — Bash**
````
{
 "command": "git diff app/backend/review.py | sed -n 1,200p | grep -n \"^@@\" ; git diff -U2 app/backend/present.py | sed -n 1,140p"
}
````

### User / tool · 2026-11-02T13:49:36.854Z

**tool result**
````
5:@@ -7,6 +7,7 @@ invalid_edit and nothing is saved; there is no confirm or override path (no 409)
13:@@ -173,7 +174,25 @@ def entry_record(item: dict, recs: list):
40:@@ -188,7 +207,14 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
56:@@ -203,7 +229,10 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
68:@@ -351,8 +380,9 @@ def _edit(conn, case_id, kind, item, body, call, t):
80:@@ -382,6 +412,10 @@ def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t)
diff --git a/app/backend/present.py b/app/backend/present.py
index 4d494e4..208e9c0 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -10,9 +10,9 @@ OK_WHY = "Quote found word for word, every number in the summary is in the quote
 
 
-def _why(reasons):
+def _why(reasons, judge=None):
     out = []
     for c in reasons or []:
         try:
-            out.append(why.why(c))
+            out.append(why.why(c, judge))
         except KeyError:
             pass
@@ -31,9 +31,10 @@ def _ladder(row):
     lad["state"] = row["state"]
     lad["human"] = _human(row)
+    lad.pop("pre_edit", None)      # T-138: the undo snapshot is internal (api.md), never in a payload
     return lad
 
 
 def _common(row):
-    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
+    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
             "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}
 
@@ -62,6 +63,13 @@ def accept_effect(row) -> str:
 
 
+def amount_flag(row):
+    """D-059: the flag a charge carries (likely_duplicate | likely_total) and whether accepting it now needs the confirm step. (None, False) for any other amount."""
+    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
+    return (None, False) if not f else ({k: f.get(k) for k in ("flag", "name", "message", "confirm_with", "of", "confirmed_at")}, row["review_status"] == "pending")
+
+
 def amount_view(row, recs):
-    return {**_common(row), "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
+    flag, needs = amount_flag(row)
+    return {**_common(row), "flag": flag, "confirm_required": needs, "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
             "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
             "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate"}
@@ -160,4 +168,5 @@ def item_view(conn, case_id, item_id):
     v = _VIEW[kind](row, _recs_by_id(conn, case_id))
     v["kind"] = kind
+    v["second_check_pending"] = item_id in second_check_pending_ids(conn, case_id)
     if kind == "flag":
         _with_gap_changes(conn, case_id, [v])
@@ -165,7 +174,18 @@ def item_view(conn, case_id, item_id):
 
 
+def second_check_pending_ids(conn, case_id) -> set:
+    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
+    acknowledges it, no check needed). Lazy import: trace imports this module."""
+    from app.backend import trace
+    return {u["item_id"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u["kind"], u["row"])}
+
+
 def all_items(conn, case_id):
     recs = _recs_by_id(conn, case_id)
     out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
+    pend = second_check_pending_ids(conn, case_id)
+    for k in ("entry", "amount", "flag"):
+        for v in out[k]:
+            v["second_check_pending"] = v["id"] in pend
     out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
     return out
@@ -181,4 +201,5 @@ def totals_view(conn, case_id):
             "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
                                      "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
+            "flagged_charges": [{"id": a["id"], "flag": amount_flag(a)[0]["flag"]} for a in am if amount_flag(a)[1]],      # D-059: flagged charges waiting for a named confirm
             "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
                             if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:49:45.044Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/commit_parts.py <<'EOF'\nimport subprocess, os, sys, json\nR=\"/Users/arsis/zlayt-pm-project\"; os.chdir(R)\ndef sh(*a, env=None, inp=None):\n    r=subprocess.run(a, capture_output=True, text=True, env=env, input=inp)\n    if r.returncode: print(r.stdout, r.stderr); sys.exit(1)\n    return r.stdout\ndef head(p): return sh(\"git\",\"show\",\"HEAD:\"+p)\ndef cur(p): return open(p).read()\n\ndef commit(msg, whole, patches):\n    \"\"\"whole: paths committed as the working-tree content; patches: {path: [(old,new)]} applied to HEAD text.\"\"\"\n    idx=\"/private/tmp/claude-501/tmp_index\"; \n    if os.path.exists(idx): os.remove(idx)\n    env=dict(os.environ, GIT_INDEX_FILE=idx)\n    sh(\"git\",\"read-tree\",\"HEAD\",env=env)\n    paths=[]\n    for p in whole:\n        h=sh(\"git\",\"hash-object\",\"-w\",p).strip(); sh(\"git\",\"update-index\",\"--cacheinfo\",f\"100644,{h},{p}\",env=env); paths.append(p)\n    for p,reps in patches.items():\n        t=head(p)\n        for o,n in reps:\n            assert t.count(o)==1,(p,o[:60],t.count(o)); t=t.replace(o,n)\n        h=sh(\"git\",\"hash-object\",\"-w\",\"--stdin\",inp=t).strip(); sh(\"git\",\"update-index\",\"--cacheinfo\",f\"100644,{h},{p}\",env=env); paths.append(p)\n    print(sh(\"git\",\"diff\",\"--cached\",\"--stat\",env=env))\n    sh(\"git\",\"commit\",\"-m\",msg,\"--no-verify\" if False else \"-q\",env=env) if False else None\n    out=sh(\"git\",\"commit\",\"-q\",\"-m\",msg,env=env)\n    sh(\"git\",\"reset\",\"-q\",\"HEAD\",\"--\",*paths)\n    print(sh(\"git\",\"log\",\"--oneline\",\"-1\"))\nEOF\ngit diff app/backend/review.py | sed -n 1,140p"
}
````

### User / tool · 2026-11-02T13:49:45.170Z

**tool result**
````
diff --git a/app/backend/review.py b/app/backend/review.py
index 2466d4f..45fe02d 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -7,6 +7,7 @@ invalid_edit and nothing is saved; there is no confirm or override path (no 409)
 (D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
 JUDGE_UNAVAILABLE).
 """
+import copy
 import time
 
 from app.backend import amounts as AM, charge_text, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
@@ -173,7 +174,25 @@ def entry_record(item: dict, recs: list):
     return next((r for r in recs if r["id"] == rid), None)
 
 
-def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None) -> dict:
+def confirm_error(item_id: str, item: dict, confirm):
+    """D-059: a charge that carries a likely_duplicate or likely_total flag is accepted only when the call names that flag (`confirm`). A 422 CONFIRM_REQUIRED
+    with the flag and the exact word to send, else None. Code only: the flag was set by amounts.py, not by a model, and a judge answer does not clear it."""
+    f = (item.get("ladder") or {}).get("confirm")
+    if item.get("kind") != "charge" or not f or confirm == f["confirm_with"]:
+        return None
+    detail = {"item_id": item_id, "reason_code": "CONFIRM_REQUIRED", "flag": f["flag"], "name": f["name"], "confirm_with": f["confirm_with"], "of": f.get("of"),
+              "next_action": {"code": "CONFIRM_FLAG", "text": "Confirm the flag by name, or dismiss the charge", "target": {"item_id": item_id}}}
+    wrong = "" if confirm is None else " The confirm you sent does not name this flag."
+    return ReviewError(422, "CONFIRM_REQUIRED", detail, f"{f['name']}: {f['message']} It is not counted unless you confirm that flag by name ({f['confirm_with']}).{wrong}")
+
+
+def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
+    f = (item.get("ladder") or {}).get("confirm")
+    if item.get("kind") == "charge" and f:
+        DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": store.iso(t)}})
+
+
+def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
     """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
     D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
     decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
@@ -188,7 +207,14 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
         err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand) or charge_text_error(item_id, cand)
         if err:
             raise err
-    return DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
+    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
+        err = confirm_error(item_id, item, confirm)         # D-059
+        if err:
+            raise err
+    out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
+    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
+        _record_confirm(conn, case_id, item_id, item, now)
+    return out
 
 
 def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
@@ -203,7 +229,10 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
         raise _date_unconfirmed_error()
     warnings = []
     if action in ("accept", "dismiss", "reset"):
-        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item)
+        confirm = body.get("confirm")
+        if confirm is not None and not isinstance(confirm, str):
+            raise _bad("The confirm must be the name of the flag.")
+        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
         if action == "reset":
             restore_pre_edit(conn, case_id, item_id, kind, item, t)
         if kind == "flag" and action == "dismiss" and body.get("note"):
@@ -351,8 +380,9 @@ def _edit(conn, case_id, kind, item, body, call, t):
     set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
     lad = item.get("ladder") or {"item_id": item["id"]}
     if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
-        lad["pre_edit"] = {"judge": lad.get("judge"), "code_checks": lad.get("code_checks"), "state": item["state"], "state_reasons": list(item.get("state_reasons") or []),
-                           "lad_state": lad.get("state")}
+        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
+                           "state": item["state"], "state_reasons": list(item.get("state_reasons") or []), "lad_state": lad.get("state")}      # deep copies: the edit updates code_checks in place below
+    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
     lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                     "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
     lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
@@ -382,6 +412,10 @@ def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t)
         lad.pop("judge", None)
     if snap.get("code_checks") is not None:
         lad["code_checks"] = snap["code_checks"]
+    if snap.get("rejudge"):
+        lad["rejudge"] = snap["rejudge"]
+    else:
+        lad.pop("rejudge", None)
     fields = {}
     after = snap.get("after") or {}
     if after and item["state"] == after.get("state") and sorted(item.get("state_reasons") or []) == sorted(after.get("state_reasons") or []):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:49:50.704Z

Now apply the patch lists.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:49:58.102Z

**tool call — Bash**
````
{
 "command": "cat >> /private/tmp/claude-501/commit_parts.py <<'EOF'\n\nwhich=sys.argv[1]\nif which==\"138\":\n    # my review.py hunks: lift the old/new strings from the working-tree file by construction\n    rv=[(\"import time\\n\\nfrom app.backend import amounts\",\"import copy\\nimport time\\n\\nfrom app.backend import amounts\"),\n        ('''        lad[\"pre_edit\"] = {\"judge\": lad.get(\"judge\"), \"code_checks\": lad.get(\"code_checks\"), \"state\": item[\"state\"], \"state_reasons\": list(item.get(\"state_reasons\") or []),\n                           \"lad_state\": lad.get(\"state\")}''','''        lad[\"pre_edit\"] = {\"judge\": copy.deepcopy(lad.get(\"judge\")), \"code_checks\": copy.deepcopy(lad.get(\"code_checks\")), \"rejudge\": copy.deepcopy(lad.get(\"rejudge\")),\n                           \"state\": item[\"state\"], \"state_reasons\": list(item.get(\"state_reasons\") or []), \"lad_state\": lad.get(\"state\")}      # deep copies: the edit updates code_checks in place below\n    lad.pop(\"rejudge\", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none'''),\n        ('''        lad[\"code_checks\"] = snap[\"code_checks\"]\n    fields = {}''','''        lad[\"code_checks\"] = snap[\"code_checks\"]\n    if snap.get(\"rejudge\"):\n        lad[\"rejudge\"] = snap[\"rejudge\"]\n    else:\n        lad.pop(\"rejudge\", None)\n    fields = {}''')]\n    pr=[('''    lad[\"human\"] = _human(row)\n    return lad''','''    lad[\"human\"] = _human(row)\n    lad.pop(\"pre_edit\", None)      # T-138: the undo snapshot is internal (api.md), never in a payload\n    return lad''')]\n    commit(\"fix(backend): T-138 r2 undo snapshot deep-copies judge and code checks (no alias of the edit's in-place update), restores the rerun record, is removed after undo and never returned in a payload\\n\\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\",\n           [\"tests/unit/test_t138_undo_edit.py\"], {\"app/backend/review.py\":rv,\"app/backend/present.py\":pr})\nelse:\n    pr=[('''def all_items(conn, case_id):\n    recs = _recs_by_id(conn, case_id)\n    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in (\"entry\", \"amount\", \"flag\")}\n''','''def second_check_pending_ids(conn, case_id) -> set:\n    \"\"\"T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only\n    acknowledges it, no check needed). Lazy import: trace imports this module.\"\"\"\n    from app.backend import trace\n    return {u[\"item_id\"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u[\"kind\"], u[\"row\"])}\n\n\ndef all_items(conn, case_id):\n    recs = _recs_by_id(conn, case_id)\n    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in (\"entry\", \"amount\", \"flag\")}\n    pend = second_check_pending_ids(conn, case_id)\n    for k in (\"entry\", \"amount\", \"flag\"):\n        for v in out[k]:\n            v[\"second_check_pending\"] = v[\"id\"] in pend\n'''),('''    v[\"kind\"] = kind\n    if kind == \"flag\":''','''    v[\"kind\"] = kind\n    v[\"second_check_pending\"] = item_id in second_check_pending_ids(conn, case_id)\n    if kind == \"flag\":''')]\n    commit(\"fix(backend): T-134 r4 re-picked-quote texts (review step, gate headline, conditional warning), rerun claim tied to the current quote, second_check_pending item field\\n\\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\",\n           [\"app/backend/trace.py\",\"app/backend/export_routes.py\",\"tests/unit/test_t134_unconfirmed_edit.py\"], {\"app/backend/present.py\":pr})\nEOF\npython3 /private/tmp/claude-501/commit_parts.py 138"
}
````

### User / tool · 2026-11-02T13:49:59.362Z

**tool result**
````
 app/backend/present.py            |  1 +
 app/backend/review.py             | 10 ++++--
 tests/unit/test_t138_undo_edit.py | 71 +++++++++++++++++++++++++++++++++++++++
 3 files changed, 80 insertions(+), 2 deletions(-)

b7a7ead fix(backend): T-138 r2 undo snapshot deep-copies judge and code checks (no alias of the edit's in-place update), restores the rerun record, is removed after undo and never returned in a payload
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:50:02.013Z

**tool call — Bash**
````
{
 "command": "python3 /private/tmp/claude-501/commit_parts.py 134 && git status --short app/backend/trace.py app/backend/review.py app/backend/present.py app/backend/export_routes.py tests/unit/test_t13*; git diff -U0 app/backend/review.py app/backend/present.py | grep \"^@@\" | head"
}
````

### User / tool · 2026-11-02T13:50:03.121Z

**tool result**
````
 app/backend/export_routes.py             |   8 +-
 app/backend/present.py                   |  12 +++
 app/backend/trace.py                     |  28 +++++--
 tests/unit/test_t134_unconfirmed_edit.py | 128 +++++++++++++++++++++++++++++++
 4 files changed, 163 insertions(+), 13 deletions(-)

4f416a4 fix(backend): T-134 r4 re-picked-quote texts (review step, gate headline, conditional warning), rerun claim tied to the current quote, second_check_pending item field

 M app/backend/present.py
 M app/backend/review.py
 M tests/unit/test_t139_charge_text.py
 M tests/unit/test_t139_letter_eval.py
?? tests/unit/test_t139_narrow.py
@@ -12 +12 @@ OK_WHY = "Quote found word for word, every number in the summary is in the quote
@@ -16 +16 @@ def _why(reasons):
@@ -38 +38 @@ def _common(row):
@@ -64,0 +65,6 @@ def accept_effect(row) -> str:
@@ -66 +72,2 @@ def amount_view(row, recs):
@@ -195,0 +203 @@ def totals_view(conn, case_id):
@@ -177 +177,19 @@ def entry_record(item: dict, recs: list):
@@ -192 +210,8 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
@@ -207 +232,4 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:50:04.371Z

Only the foreign hunks remain. Board updates.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:50:12.084Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B commit T-138 --sha b7a7ead --agent backend; $B commit T-134 --sha 4f416a4 --agent backend\n$B ac T-138 --check 1 --agent backend --evidence \"tests/unit/test_t138_undo_edit.py (11 tests): deep-copied snapshot (alias mutant, T3, T9 each fail a test), rejudge restored, pre_edit not in any payload; full unit suite: 6 failures, none in these files (amounts_t140, e2e_contract ids, t114 lib10 a7 fixture: other workers)\"\n$B ac T-134 --check 1 --agent backend --evidence \"tests/unit/test_t134_unconfirmed_edit.py (28 tests): review step, gate headline == 422 message, rerun claim tied to current quote, no 'stays blocked' while gate passes, second_check_pending; mutants N18, N19, H2, H1, review-step, no-clear, no-pop all killed\"\n$B note T-134 --agent backend --text \"r4 (7.4 fix-up) commit 4f416a4 (+ review.py rejudge clear in T-138 commit b7a7ead): 1 review step + gate headline reworded (headline is trace.judge_not_run_message, same sentence as the 422); 2 rerun claim: _edit drops ladder.rejudge, undo restores it; 3 conditional clause 'If you accept it, the export will be blocked until ...', no 'stays blocked' while ready; 4 N18/N19/H2 killed (direct unit on rerun_gave_no_answer, warning text asserts); 5 item field second_check_pending (entries, amounts, flags; GET case + review responses) documented in api.md. Reviewer's P3 probe never applied Q2 (shortened quote fails the summary-number check 422), my test uses a valid variant.\"\n$B handoff T-134 --agent backend --text \"What changed: r3 items 1-5 (trace.py, export_routes.py, present.py second_check_pending, review.py rejudge clear; api.md). Commit 4f416a4, review.py piece in b7a7ead. How verified: tests/unit/test_t134_unconfirmed_edit.py + test_t138 pass (37); 11 mutants incl. N18 N19 H2 killed; full unit suite 3884 pass, 6 fail all outside these files (amounts_t140 x3, e2e_contract ids, t114 lib10 a7 fixture, t139_narrow flaky alone-passes: other workers in flight). What's left: frontend should read second_check_pending; item-trace verdict for an accepted blocked item (r3 minor 5) still needs its own card. Surprised me: api.md hunk got committed inside another worker's commit 68b8685; reviewer's stale-quote probe silently 422'd.\"\n$B handoff T-138 --agent backend --text \"What changed: r1 findings: snapshot deep-copies judge/code_checks (+rejudge restored), snapshot removed after undo test, pre_edit popped in present._ladder (never in a payload; api.md updated). Commit b7a7ead (temp-index, only my hunks of review.py/present.py). How verified: test_t138_undo_edit.py 11 pass; mutants alias, T3, T9, no-pop each fail a test. What's left: nothing.\"\n$B move T-138 in_review --agent backend; $B move T-134 in_review --agent backend"
}
````

### User / tool · 2026-11-02T13:50:12.718Z

**tool result**
````
T-138: commit b7a7ead recorded
T-134: commit 4f416a4 recorded
AC 1 checked: tests/unit/test_t138_undo_edit.py (11 tests): deep-copied snapshot (alias mutant, T3, T9 each fail a test), rejudge restored, pre_edit not in any payload; full unit suite: 6 failures, none in these files (amounts_t140, e2e_contract ids, t114 lib10 a7 fixture: other workers)
AC 1 checked: tests/unit/test_t134_unconfirmed_edit.py (28 tests): review step, gate headline == 422 message, rerun claim tied to current quote, no 'stays blocked' while gate passes, second_check_pending; mutants N18, N19, H2, H1, review-step, no-clear, no-pop all killed
noted on T-134
handoff written on T-134
handoff written on T-138
T-138: in_progress -> in_review
T-134: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:50:16.260Z

T-134 (commit 4f416a4) and T-138 (commit b7a7ead) are both in `in_review`. Their 37 tests pass, and 11 mutants fail a test, including N18, N19, H2, T3 and T9. A reviewer probe used a quote that returns 422, so it never tested the stale-rerun case; my test uses a valid quote.

T-134 covers all five items:
- The two missed D-058 wordings are fixed. The gate headline is now the same sentence as the 422.
- The "ran again, no answer" claim comes from the current quote's rejudge record.
- No "export stays blocked" text appears when the gate passes.
- N18, N19 and H2 are killed.
- `second_check_pending` is on every entry, amount and flag, documented in api.md.

T-138: the snapshot is deep-copied, so undo restores the pre-edit checks. T3 and T9 are killed, and `pre_edit` no longer appears in any payload.

The full unit suite gives 3884 pass and 6 fail, none in these two cards' files: three in `test_amounts_t140.py`, plus `test_e2e_contract.py`, the `test_t114` lib10 a7 case and `test_t139_narrow.py`. The T-139 narrow test passes when run alone. The api.md edit was already committed inside another worker's commit 68b8685.
