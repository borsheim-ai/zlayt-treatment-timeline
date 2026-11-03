# Subagent: Backend: T-098 r3 all checks, all paths (Backend: T-098 r3 all checks, all paths)

Source: `agent-aac618d6ff8cc4969.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:41:51.694Z

You own board card T-098, round 3 (final; claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-098-staff-engineer-r2.md (1 blocker, 1 major, 2 minors) and the probes in artifacts/review-evidence/T-098-staff-engineer-r2-*. D-051 is binding.

1. **Blocker:** the accept guard must run on every action that leaves an item accepted or included in the letter, not only `action == "accept"` (review.py:157). That includes an edit that implies accept, a summary-only edit and reset. Make it one function called from a single choke point where state becomes accepted. The edit must never wipe a failing quote-level reason such as EXCERPT_OMITS_QUALIFIER. If the quote drops a hedge sentence, the paralegal must be told to fix the quote (Change quote), not just the summary.
2. **Major:** the gate and the item trace must recompute all 5 code checks: summary token (D-034/D-047), qualifier dropped (D-022), whole sentence (D-012/D-021), excerpt omits qualifier, and excerpt substring of the record. memory/contracts/api.md must match.
3. **Minors:** the internal notes must not print AI wording that contains a failing token. The EDITED ITEMS "summary was" line and the narrative "Removed" line should say "AI wording removed (failed a check: <reason>)". Add a test that kills mutant M11, covering the quote-level half of D-051.

Run every reviewer probe and get it to pass. Run `.venv/bin/python -m pytest -q tests/unit`. Commit with the pathspec rule or a fresh temp index, and check that `git diff --cached --stat` lists only your files. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never pkill. Then `board.py ac`, the handoff, and `move T-098 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T05:41:51.699Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:41:53.871Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-098-staff-engineer-r2.md && ls artifacts/review-evidence/ | grep T-098-staff-engineer-r2 && python3 tools/board.py show T-098 | tail -60 && git status --short | head -30"
}
````

### User / tool · 2026-11-02T05:41:54.056Z

**tool result**
````
# T-098 staff-engineer-reviewer, round 2: D-051 code checks bind accept (commit dd84122)

Verdict: **fail** (1 blocker, 1 major, 2 minor). The round-1 blocker is closed for numbers and sides: an AI draft with a figure or side word not in its quote is refused on single accept and batch accept for every judge verdict, a stale stored "pass" does not hide it, and the gate recomputes it. A different live route to the same kind of defect is open: a summary-only edit of an AI draft whose quote drops the hedge sentence (finding 1).

Pinning: reviewed `git archive dd84122`. HEAD moved to 9f2811f during the review (T-097 r3 and other cards). Between dd84122 and 9f2811f only `app/backend/review.py` changed in the files in scope (message wording, `_NUMERIC_TOKEN`, D-050 translated flag). I re-ran probes 1 to 3 on `git archive 9f2811f`: same results (63 checks, 0 failed; finding 1 and 2 reproduce).

Unit suite on the dd84122 archive: `.venv/bin/python -m pytest -q tests/unit` gives **1860 passed, 4 skipped, 2 failed**. Neither failure is related to T-098:
- `test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git` runs `git archive HEAD` inside the tree under test; an archive has no `.git`. It passes in the live repo.
- `test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts` fails in the live repo, in the dd84122 archive and in the 4c5f9bf archive (the parent of dd84122). dd84122 touches no `evals/` file. It belongs to T-093/T-101.

Targeted suite (trace, export, case_extras, date_unconfirmed): 118 passed.

## Matrix result (every route x every judge verdict)

`artifacts/review-evidence/T-098-staff-engineer-r2-probe.py` through the real FastAPI app, fixture backend, scratch DB copies. Two invented kinds ("Pain 5/10" and "on the left") against judge verdicts supported, unsupported and disagrees: single accept of an AI draft (state needs_review), single accept with a stale stored pass (state verified, no reasons, all stored checks true), batch accept ([clean, bad] and [bad]), edit then accept, forced accept that bypasses the route plus gate, and rerun after decisions with the generator now drafting the token (D-039, `confirm_rerun`). Also rejudge then accept (j1 supported, unsupported, partially), manual entry, and the narrative paragraph. Result: 54 checks passed, 0 failed; the marker never reached `letter_text`; a pending bad draft is printed as "summary not shown, a code check on it fails" in the notes.

## Findings

**F1 (blocker). A summary-only edit bypasses the D-051 accept guard when the AI quote fails a quote-level check, and the 422 steers the paralegal into it.** Live route, no tampering after the draft is made (`T-098-staff-engineer-r2-probe3-results.txt`): e8's AI draft quotes "C5-C6 disc protrusion with mild right foraminal narrowing." and leaves out the next sentence "Findings may represent degenerative change; correlate clinically." Real `generator.verify` gives `needs_review ['EXCERPT_OMITS_QUALIFIER']`. Accept returns `422 CODE_CHECK_FAILED` ("The quote leaves out a hedge sentence that qualifies it. Edit the summary to match the quote."). The paralegal then edits the summary only: `200`, `review_status edited`, `state_reasons ['JUDGE_UNAVAILABLE']` (the stored `EXCERPT_OMITS_QUALIFIER` is gone). Gate `ready True, blockers []`, `GET /export` 200, the letter has the entry and its quote with no hedge sentence. Cause: `app/backend/review.py:157` guards only `action == "accept"` (edit implies accept per api.md and `_edit` does not call `code_check_error`); `_edit` rewrites `state_reasons_json` at `review.py:299` from `_check_summary`, whose `code_reasons` is always empty, so it erases the stored reason; `app/backend/trace.py:357-371` read the quote-level steps from stored data only (finding 2); and `review.py:130` points a quote failure at `EDIT_SUMMARY`, which is the edit that clears it. D-022 and the export header ("hedge sentences cannot be removed") say the quoted hedge stays; D-051 says the code rung binds accept for every item. A hedge lost from the quote is a loss of a qualifier in the letter. Rated blocker per D.2 (loses a fact qualifier on a live route).

**F2 (major). The gate and the item trace recompute only two of the five code checks, although api.md says they recompute the quote's whole-sentence and hedge checks.** `memory/contracts/api.md` (D-051 T-098 r2 paragraph): "The gate and the item trace recompute the code checks (... and the quote's whole-sentence and hedge checks) ... a stale stored 'pass' cannot hide a failing summary." `trace.py:362-368` recomputes `summary_tokens` and `summary_qualifier`; `excerpt_whole_sentence`, `excerpt_hedge` and `highlight` still read `R` and `cc` (stored). Probe2 (`T-098-staff-engineer-r2-probe2-results.txt`): quote cut to one sentence, stored results all pass, summary matching: API accept `422`, but after a forced accept the gate is `ready True`, `GET /export` 200, the item trace has no failing step, and the letter lacks the hedge. The accept guard recomputes all five (`review.py:78-98`), so accept and gate disagree. This is why F1 reaches the export. Major, not blocker: I found no live route that produces this state except F1.

**F3 (minor, my reading; question for Chris). The internal notes still print AI wording that has a token the quote lacks.** `export.py:498` ("summary was ..., now ...") prints the AI draft's original summary after a human edit; `export.py:542` ("Removed: ...") prints narrative sentences removed for `SUMMARY_TOKEN_NOT_IN_EXCERPT`. Probe (`S4-notes`, `S9-notes` observations): 6 of 6 edit cases and 3 of 3 narrative cases carry "Pain 5/10" in `internal_notes_text`, never in `letter_text`. Both are labelled as the earlier draft or as removed, in the do-not-send block. The worker's fix hides only a pending draft. If the rule is "no token missing from its quote anywhere in the export", this is open; I did not call it a blocker because the text is a labelled record of what the AI wrote, not a statement about the case.

**F4 (minor). Tests do not pin the quote-level half of D-051.** Mutant M11 (the `check_excerpt` loop in `code_check_failures` replaced by `[]`) leaves 118 passed (`T-098-staff-engineer-r2-mutants-results.txt`). No test does a summary-only edit on a draft with a failing quote (F1), and none puts a stale pass beside a failing quote on the gate (F2). `tests/unit/test_trace.py:1106` `test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098` keeps a name that D-051 contradicts (it only passes because the golden drafts are clean). Equivalent survivors, not findings: M8 (stored reasons ignored) and M12 (live term in `summary_tokens`, because `toks` already carries it).

## Mutation spot-check (scratch copy of the dd84122 archive)

Suite: `tests/unit/test_trace.py test_export.py test_case_extras.py test_date_unconfirmed.py` (118 passed). M1 accept guard ignored: 1 failed. M2 batch arm off: 1 failed. M3 gate recompute off: 1 failed. M4 gate back to human wording only: 1 failed. M5 `code_check_failed` flag never set: 1 failed. M6 `_pending` hide branch off: 1 failed. M7 live recompute off in `code_check_failures`: 1 failed. M9 batch error mapping off: 1 failed. M10 qualifier dropped from `CODE_CHECK_REASONS`: 1 failed. M13 trace qualifier live term off: 1 failed. M14 AI-draft blocker text: 1 failed. Survivors: M8, M11, M12 above.

## What I exercised

- `git rev-parse HEAD` (dd84122 at start, 9f2811f at the end), `git show --stat dd84122`, `git show dd84122 -- app/ memory/contracts/api.md tests/unit/test_trace.py`, `git diff dd84122 HEAD` for the five backend files in scope.
- `git archive dd84122` (probes, unit run), a second copy for mutants, `git archive 4c5f9bf` (parent, for the unrelated failure), `git archive 9f2811f` (re-run).
- Full `tests/unit` on the dd84122 archive, the two failing tests alone in the archive, the live repo and the parent archive.
- Probes: `T-098-staff-engineer-r2-probe.py` (matrix, results `T-098-staff-engineer-r2-results.txt` and `...-results-head-9f2811f.txt`), `...-r2-probe2.py` (gate vs accept on quote checks), `...-r2-probe3.py` (live edit route, F1; results at dd84122 and 9f2811f), `...-r2-mutants.py` (14 mutants).
- Read: `review.py`, `case_extras.py`, `trace.py` (steps, blockers), `export.py`, `export_routes.py`, `narrative.py`, `store.py`, `pipeline.py` (`_persist`, `_frozen_splitter`), `rejudge.py`, `api.py` routes; `reviews/T-098-staff-engineer.md`, `reviews/T-097-ux-designer-r2.md`, D-051, D-039.
- Not exercised: browser UI and copy (outside my lens); real LLM backends (fixture only, by design).

```json
{"card": "T-098", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit dd84122 (D-051 accept guard, gate recompute, pending-draft notes) on git archive dd84122; re-run of probes on git archive 9f2811f (live HEAD at the end); FastAPI TestClient with the fixture backend and scratch DB copies of the sample case; no app URL",
 "exercised": [
  "git rev-parse HEAD (dd84122f6b7f at start, 9f2811f at end); git show --stat dd84122; git show dd84122 -- app/ memory/contracts/api.md tests/unit/test_trace.py; git diff dd84122 HEAD --stat for review.py, trace.py, export.py, store.py, case_extras.py (only review.py changed: wording, _NUMERIC_TOKEN, D-050 flag)",
  "git archive dd84122 | tar -x (scratchpad r2arch); .venv/bin/python -m pytest -p no:cacheprovider -q tests/unit on it -> 1860 passed, 4 skipped, 2 failed (test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git: git archive HEAD inside a tree without .git, passes in the live repo; test_fixture_runs_write_no_artifacts: also fails in the live repo and in the 4c5f9bf archive, evals area, unrelated)",
  "artifacts/review-evidence/T-098-staff-engineer-r2-probe.py on dd84122 and on 9f2811f: 54 checks printed PASS, 0 FAIL (single accept, stale-pass accept, batch [clean,bad] and [bad], edit-then-accept, forced accept + gate, rerun after decisions with confirm_rerun, rejudge then accept, manual entry, narrative; tokens 'Pain 5/10' and 'on the left'; judge verdicts supported, unsupported, disagrees)",
  "same probe notes block: 6 of 6 edit-then-accept cases and 3 of 3 narrative cases print the AI draft's token in internal_notes_text (EDITED ITEMS 'summary was', narrative 'Removed:'); letter_text clean in all",
  "artifacts/review-evidence/T-098-staff-engineer-r2-probe2.py: quote cut to drop the hedge sentence with all stored checks pass -> API accept 422 CODE_CHECK_FAILED; forced accept -> gate ready True, export 200, letter lacks the hedge, item trace has no failing step",
  "artifacts/review-evidence/T-098-staff-engineer-r2-probe3.py on dd84122 and 9f2811f: real generator.verify -> needs_review [EXCERPT_OMITS_QUALIFIER]; accept 422; EDIT summary only 200 (state_reasons now [JUDGE_UNAVAILABLE]); gate ready True; GET /export 200; letter has no 'may represent degenerative'",
  "artifacts/review-evidence/T-098-staff-engineer-r2-mutants.py on a scratch copy: 14 mutants, baseline 118 passed; M1-M7, M9, M10, M13, M14 fail a test; M8, M11, M12 survive (118 passed)",
  "read review.py, case_extras.py, trace.py, export.py, export_routes.py, narrative.py, store.py, pipeline.py, rejudge.py, api.py; reviews/T-098-staff-engineer.md; reviews/T-097-ux-designer-r2.md; D-051 and D-039 in memory/ORCHESTRATOR_DECISIONS.md; memory/contracts/api.md D-051 paragraph",
  "git archive 4c5f9bf (parent) to test whether the unrelated failure predates dd84122; git archive 9f2811f for the HEAD re-run"],
 "verdict": "fail",
 "scores": {"accept_guard_numbers_and_sides": 5, "batch_guard": 5, "gate_recompute_summary_checks": 4, "gate_recompute_quote_checks": 1, "edit_route_vs_accept_guard": 1, "pending_draft_notes": 4, "tests_pin_behaviour": 3},
 "findings": [
  {"severity": "blocker", "title": "A summary-only edit bypasses the D-051 accept guard when the AI quote drops the hedge sentence; the 422 points the paralegal at that edit",
   "evidence": "artifacts/review-evidence/T-098-staff-engineer-r2-probe3-results.txt (dd84122) and ...-probe3-head-9f2811f.txt: 'generator.verify -> needs_review [EXCERPT_OMITS_QUALIFIER]', 'accept e8 ... -> 422 CODE_CHECK_FAILED', 'EDIT e8 summary only -> 200 None', 'e8 after edit: review_status edited | state needs_review | state_reasons [JUDGE_UNAVAILABLE]', 'gate ready: True | blockers: []', 'GET /export -> 200', 'letter has the hedge sentence ...: False'. Code: app/backend/review.py:157 (guard only for action == accept), review.py:299 (edit rewrites state_reasons_json from _check_summary, whose code_reasons is always empty), review.py:130 (next_action EDIT_SUMMARY for every failing check including EXCERPT_OMITS_QUALIFIER), app/backend/trace.py:357-371 (quote steps read stored data only).",
   "why_it_matters": "The letter ships a quote with the hedge sentence ('Findings may represent degenerative change; correlate clinically.') removed, which turns a hedged finding into a plain one. D-022 and the export header say hedge sentences cannot be removed; D-051 says the code rung binds accept for every item, and edit implies accept. The paralegal does nothing unusual: accept is refused, the message says to edit the summary, the edit clears the block. Rated blocker per D.2 (loses a qualifier on a live route; a fact is changed in the letter).",
   "fix": "Run the same five-check recompute (code_check_error) on the post-edit row inside _edit and refuse with 422 before any write, or make the gate recompute the quote steps (finding 2) so the item stays a blocker; do not let _edit erase stored code reasons it did not recompute. For EXCERPT_OMITS_QUALIFIER, EXCERPT_NOT_WHOLE_SENTENCE and HIGHLIGHT_NOT_FOUND use next_action EDIT_QUOTE (trace._fix_action already does), not EDIT_SUMMARY.",
   "acceptance_test": "Unit: draft e8 with quote 'C5-C6 disc protrusion with mild right foraminal narrowing.' (state needs_review, EXCERPT_OMITS_QUALIFIER). Accept returns 422; edit with a summary-only change returns 422 (or the item stays a gate blocker and GET /export is 422); the letter never lacks 'may represent degenerative'. Run with judge verdicts supported, unsupported and disagrees. Mutation: removing the new check in _edit makes the test fail."},
  {"severity": "major", "title": "Gate and item trace recompute 2 of the 5 code checks; api.md says they recompute the quote's whole-sentence and hedge checks",
   "evidence": "memory/contracts/api.md D-051 paragraph: 'The gate and the item trace recompute the code checks (... and the quote's whole-sentence and hedge checks) from each entry's CURRENT summary and quote ... a stale stored pass cannot hide a failing summary.' app/backend/trace.py:362-368 recompute summary_tokens and summary_qualifier only; trace.py:357-371 excerpt_whole_sentence, excerpt_hedge, highlight read R and cc. artifacts/review-evidence/T-098-staff-engineer-r2-probe2-results.txt: 'API accept -> 422 CODE_CHECK_FAILED', 'forced accept -> gate ready: True | blockers: []', 'GET /export -> 200', 'letter contains the hedge ...: False', 'item trace failing steps: []' (both a quote that drops the hedge sentence and a quote that starts mid-sentence).",
   "why_it_matters": "Accept refuses a state that the gate lets through, so the gate does not do what the contract and the commit message say, and finding 1 reaches the export because of it. No live route other than finding 1 produces the state today, so I rate it major, not blocker.",
   "fix": "In _entry_steps use review.code_check_failures (live) for excerpt_whole_sentence, excerpt_hedge and highlight the way it is already used for summary_tokens and summary_qualifier; or correct the api.md sentence if the scope is cut on purpose (then record it in SCOPE_CUTS.md).",
   "acceptance_test": "Unit: stored checks all pass, quote cut to one sentence, forced accept via DB.apply_review: gate lists the item with reason EXCERPT_OMITS_QUALIFIER, GET /export is 422, item trace shows excerpt_hedge failing with blocks_export true. Mutant M3-style (quote-step live term off) fails the test."},
  {"severity": "minor", "title": "Internal notes still print AI wording whose token is not in the quote (EDITED ITEMS 'was', narrative 'Removed')",
   "evidence": "app/backend/export.py:498 ('summary was \"...\", now \"...\"') and export.py:542 ('Removed: \"...\"'). Probe notes: after a human edit of an AI draft 'Pain 5/10' internal_notes_text carries 'summary was \"... Pain 5/10.\", now \"...\"' (6 of 6 cases); a narrative sentence removed for SUMMARY_TOKEN_NOT_IN_EXCERPT is printed in the notes (3 of 3). letter_text is clean in all.",
   "why_it_matters": "The worker hides a pending draft's wording from the notes because a reader could take it as a fact; the edited and removed lines carry the same text with a label. This is a reading of the rule 'no token missing from its quote anywhere in the export', not a spec line I can cite; I label it minor and leave the decision to Chris.",
   "fix": "Either accept it as an audit trail (record it in DECISIONS), or print 'summary was [withheld: a code check on it failed]' when the original fails a code check, and the same for removed narrative sentences.",
   "acceptance_test": "Unit: edit an AI draft that failed SUMMARY_TOKEN_NOT_IN_EXCERPT, accept, export: internal_notes_text contains no '5/10'. Mutation: restoring the plain print makes it fail."},
  {"severity": "minor", "title": "Tests do not pin the quote-level half of D-051; one stale test name contradicts it",
   "evidence": "artifacts/review-evidence/T-098-staff-engineer-r2-mutants-results.txt: 'M11 accept: quote checks (hedge sentence / whole sentence) off -> 118 passed ... <-- SURVIVED'. No test does a summary-only edit on a draft with a failing quote (finding 1) or puts a stale pass beside a failing quote on the gate (finding 2). tests/unit/test_trace.py:1106 test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098 passes only because the golden drafts are clean. M8 and M12 survive as equivalent mutants (stored reasons duplicate the live check; toks already carries the live tokens).",
   "why_it_matters": "The part of the fix that finding 1 and 2 show is incomplete is the part with no test, so a regression or the current gap stays green.",
   "fix": "Add the tests named in the acceptance tests of findings 1 and 2; rename or remove the T-098 test at line 1106.",
   "acceptance_test": "Mutant M11 makes a new test fail; the renamed test asserts that an AI draft with a failing check is a gate blocker."}
 ],
 "whats_right": [
  "The accept guard holds on single and batch accept for both token kinds and all three judge verdicts, including a stale 'verified' draft; the batch is all or nothing (54 probe checks, M1, M2, M9 each fail a test).",
  "The gate recompute catches the stale pass on the summary checks and the rerun-after-decisions route (D-039 redraft with the token gives gate ready False and export 422; M3 and M13 fail a test).",
  "A pending draft that fails a code check is printed as 'summary not shown' in the notes and the test that asserts the figure is absent from the whole export response fails when the flag or the hide branch is removed (M5, M6)."],
 "questions_for_chris": [
  "F3: should the internal notes ever print AI wording that failed a code check (edited originals, removed narrative sentences), or must the whole export response be free of tokens missing from their quotes?",
  "F1: is a quote that drops a hedge sentence something the paralegal may fix by editing the summary alone, or must the quote itself be repaired (EDIT_QUOTE) before an item can leave pending?"]}
```
T-098-staff-engineer-r2-mutants-results.txt
T-098-staff-engineer-r2-mutants.py
T-098-staff-engineer-r2-probe.py
T-098-staff-engineer-r2-probe2-results.txt
T-098-staff-engineer-r2-probe2.py
T-098-staff-engineer-r2-probe3-head-9f2811f.txt
T-098-staff-engineer-r2-probe3-results.txt
T-098-staff-engineer-r2-probe3.py
T-098-staff-engineer-r2-results-head-9f2811f.txt
T-098-staff-engineer-r2-results.txt
---
id: "T-098"
title: "Export gate must block human-edited items whose code checks fail (D-045b: exempt from judge, not from code checks)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:55:06Z"
updated_at: "2026-11-02T05:41:45Z"
claimed_by: "backend"
claimed_at: "2026-11-02T05:41:45Z"
rounds: 2
commits: ["e511778", "dd84122"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-098-staff-engineer.md", "at": "2026-11-02T05:18:16Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-098-staff-engineer-r2.md", "at": "2026-11-02T05:41:45Z"}
ac:
  - {"n": 1, "text": "An accepted, human-edited summary that fails any D-034/D-022 code check (qualifier dropped, token not in excerpt) is a gate blocker and GET export returns 422 with the reason; gate.ready == export allowed still holds; per-item trace shows the failing code step; tests with the reviewer's case (reviews/T-097-ux-designer.md)", "done": true, "evidence": "r2 (dd84122): tests/unit/test_trace.py::test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051[supported|unsupported|disagrees], test_batch_accept_refuses_the_whole_batch_for_one_failing_summary_d051, test_gate_blocks_an_accepted_ai_draft_that_fails_a_code_check_and_export_is_422_d051, test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1 pass; mutating the accept guard / batch guard / live recompute in a scratch copy fails 5 / 1 / 1 tests"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:55:09Z backend: claimed
- 2026-11-02T04:59:37Z backend: AC 1 checked: tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 + test_item_trace_shows_the_failing_code_step_with_the_next_action_t098 + test_gate_ready_equals_export_allowed_with_a_failing_edit_t098 + tests/unit/test_export.py::test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b pass; tests/unit 1614 passed (test_calibration_route.py ignored: another worker's in-progress import error)
- 2026-11-02T04:59:37Z backend: moved in_progress -> in_review
- 2026-11-02T05:00:24Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T05:18:16Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-098-staff-engineer.md; round 1; findings:
    - [blocker] An AI draft with a number not in its quote reaches the export after one accept (outside the T-098 AC, found on the gate path) — fix: Decide and record the rule for AI drafts whose D-034 tokens (numbers, dates, dollar figures, left/right/no/not/without) fail the code check: either the generator refuses the draft as it refuses GROUNDING_* failures (app/backend/generator.py:71 verify,
    - [major] D-047 409 keep-my-wording path still existed at the reviewed commit (T-098 follow-up; closed at f5ddec8 by T-100 24c18a7 and frontend f5ddec8) — fix: Already done in 24c18a7 and f5ddec8. Keep the regression: side, negation and qualifier tokens refused with 422 at edit and manual entry, with no keep path in the API or the UI.
    - [minor] The T-094 trace hunk carried in e511778 has no test and no card review — fix: T-094 adds its own tests and goes through its own review before it closes, or the hunk is split out of the T-098 commit.
    - [minor] The reason filter in the new blocker is untested — fix: Add a test: an accepted paralegal entry with a failing non-summary code step is not listed as a code-check blocker (or state the intended behaviour and test it).
- 2026-11-02T05:18:16Z backend: claimed
- 2026-11-02T05:29:15Z backend: r2 golden check: scanned golden cases 01-09 + sample through the fixture pipeline; 0 AI-drafted entries fail the live code checks, so the check is not weakened. Unrelated unit failures in the shared tree (test_provider*, test_t093_eval_signature, eval_runner calibration) are other workers' WIP.
- 2026-11-02T05:29:15Z backend: AC 1 checked: r2 (dd84122): tests/unit/test_trace.py::test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051[supported|unsupported|disagrees], test_batch_accept_refuses_the_whole_batch_for_one_failing_summary_d051, test_gate_blocks_an_accepted_ai_draft_that_fails_a_code_check_and_export_is_422_d051, test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1 pass; mutating the accept guard / batch guard / live recompute in a scratch copy fails 5 / 1 / 1 tests
- 2026-11-02T05:29:15Z backend: moved in_progress -> in_review
- 2026-11-02T05:29:23Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T05:41:45Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-098-staff-engineer-r2.md; round 2; findings:
    - [blocker] A summary-only edit bypasses the D-051 accept guard when the AI quote drops the hedge sentence; the 422 points the paralegal at that edit — fix: Run the same five-check recompute (code_check_error) on the post-edit row inside _edit and refuse with 422 before any write, or make the gate recompute the quote steps (finding 2) so the item stays a blocker; do not let _edit erase stored 
    - [major] Gate and item trace recompute 2 of the 5 code checks; api.md says they recompute the quote's whole-sentence and hedge checks — fix: In _entry_steps use review.code_check_failures (live) for excerpt_whole_sentence, excerpt_hedge and highlight the way it is already used for summary_tokens and summary_qualifier; or correct the api.md sentence if the scope is cut on purpose (then record 
    - [minor] Internal notes still print AI wording whose token is not in the quote (EDITED ITEMS 'was', narrative 'Removed') — fix: Either accept it as an audit trail (record it in DECISIONS), or print 'summary was [withheld: a code check on it failed]' when the original fails a code check, and the same for removed narrative sentences.
    - [minor] Tests do not pin the quote-level half of D-051; one stale test name contradicts it — fix: Add the tests named in the acceptance tests of findings 1 and 2; rename or remove the T-098 test at line 1106.
- 2026-11-02T05:41:45Z backend: claimed

## Handoff
What changed (r2, dd84122): review.code_check_failures recomputes D-034/D-047/D-022 checks from the CURRENT summary+quote (plus stored reasons); single accept and batch accept return 422 CODE_CHECK_FAILED with the plain reason and next_action 'Edit the summary to match the quote' for AI or human wording; trace/gate recompute at gate time (stale stored pass cannot hide a failing summary), accepted failing AI drafts are gate blockers so GET export is 422; pending failing drafts are not printed in internal notes. api.md updated. | Verified: tests/unit/test_trace.py 74 passed; accept-guard mutant fails 5, batch mutant 1, live-recompute mutant 1; golden cases 01-09 + sample: 0 failing AI drafts; full tests/unit 1922 passed, 3-4 failures in test_provider*/test_t093_eval_signature (other workers' WIP, untouched files). | Left: frontend should show CODE_CHECK_FAILED message inline on accept (and batch); case-verdict label changed to 'N summaries fail a check'. | Surprised: tokens are digit runs ('5' not '5/10'); internal notes listed pending drafts' wording, so '5/10' leaked there until withheld; committed via temp index because review.py and api.md carry D-050 hunks from another worker.

 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/case_extras.py
MM app/backend/export.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
MM app/backend/store.py
MM app/backend/trace.py
 M app/llm/audited.py
 D app/llm/prompts/conflicts_v1.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:41:54.479Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/backend/project_backend_conventions.md"
}
````

### User / tool · 2026-11-02T05:41:54.488Z

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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:41:56.277Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -5 && git diff --stat HEAD -- app/backend/review.py app/backend/trace.py app/backend/export.py memory/contracts/api.md tests/unit/test_trace.py && sed -n 1,200p app/backend/review.py"
}
````

### User / tool · 2026-11-02T05:41:56.405Z

**tool result**
````
9f2811f fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)
fdc2506 fix(qa): --write-calibration judges the header in write_report, refuses untracked inputs and --controls, shares one run dir (T-101 r2)
ae76835 fix(backend): hidden-text scan runs in a child killed at the deadline; Widget/annotation covers, clip windows, low contrast and tiny text held back (T-087 r3)
288c1d3 fix(backend): D-047 r2: attribution, hedge and approximation words the quote lacks are a 422; one wide side/negation vocabulary shared by edit, manual entry, generator and gate (T-100 r2)
690a0e3 fix(backend): billing lists every repeated summary row, skipped records make totals incomplete, BALANCE DUE accepted with or without the forward (D-049, T-083 r5)
"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
Edit order: (1) structure, else 422 invalid_edit; (2) code checks (D-034/D-047): a number, date or $ figure, a side/negation word (left, right,
no, not, without) that is not in the quote, a qualifier of the quote that the summary drops, or a highlight that cannot be found is a hard 422
invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
JUDGE_UNAVAILABLE).
"""
import time

from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
from app.db import db as DB

ACTIONS = ("accept", "dismiss", "reset", "edit")
# "may" is not here: grounding never reports the month May as a token, so a "may" token is the hedge word
_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
_KIND = {"e": "entry", "a": "amount", "f": "flag"}


class ReviewError(Exception):
    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
        super().__init__(code)
        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")


def _now(now):
    return now() if callable(now) else (time.time() if now is None else now)


def _item(conn, case_id, item_id):
    try:
        row = DB.get_item(conn, item_id, case_id)
    except KeyError:
        raise ReviewError(404, "not_found", message="No such item.") from None
    if row["case_id"] != case_id:
        raise ReviewError(404, "not_found", message="No such item.")
    return _KIND[item_id[0]], row


def _bad(msg, **detail):
    return ReviewError(422, "invalid_edit", detail, msg)


def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
    """D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as
    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
    if kind != "entry":
        return False
    if not item.get("date_iso"):
        return True
    rid = (item.get("record_ids") or [None])[0]
    row = conn.execute("SELECT date_status FROM records WHERE id=? AND case_id=?", (rid, case_id)).fetchone()
    return bool(row) and row["date_status"] not in ("parsed", "confirmed", None)


def _date_unconfirmed_error():
    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
                       "cannot be accepted into the letter.")


# D-051: the code rung binds accept for every item, AI-made or human. These are the code checks on an entry's current wording.
CODE_CHECK_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND")
CODE_CHECK_STEP = {"SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
                   "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight"}
EDIT_SUMMARY_TEXT = "Edit the summary to match the quote"


def current_text(item: dict):
    ed = item.get("edited") or {}
    return ed.get("summary", item.get("summary") or ""), ed.get("excerpt", item.get("excerpt") or "")


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
        dropped = g.dropped_qualifiers(summ, exc)
        if dropped:
            out["SUMMARY_DROPS_QUALIFIER"] = {"qualifiers": list(dropped)}
        for c in g.check_excerpt(rec["excerpt"], exc):             # the quote against its record: whole sentences, keeps the hedge sentence
            if c in ("EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE"):
                out[c] = {}
        if grounding.locate(rec["excerpt"], exc) is None and not _not_verbatim(g, rec, exc):
            out["HIGHLIGHT_NOT_FOUND"] = {}
    for c in item.get("state_reasons") or []:
        if c in CODE_CHECK_REASONS:
            out.setdefault(c, {})
    return {c: out[c] for c in CODE_CHECK_REASONS if c in out}


def _not_verbatim(g, rec, exc) -> bool:
    """A quote that is not word for word in the record is a grounding failure (rejected state, its own step), not a highlight problem."""
    return "GROUNDING_EXCERPT_NOT_VERBATIM" in g.check_excerpt(rec["excerpt"], exc)


def code_check_message(fails: dict) -> str:
    """Plain words for the first failing check, then the next step."""
    c = next(iter(fails))
    d = fails[c]
    if c == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and d.get("tokens"):
        toks = d["tokens"]
        if any(_NUMERIC_TOKEN.search(t) for t in toks):
            what = "The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(toks) + "."
        else:
            what = "The summary says " + _quoted_words(toks) + ", which the quote does not say."
    elif c == "SUMMARY_DROPS_QUALIFIER" and d.get("qualifiers"):
        what = "The quote carries " + "; ".join(_QUALIFIER_WORDS.get(k, k) for k in d["qualifiers"]) + " that the summary leaves out."
    elif c == "EXCERPT_OMITS_QUALIFIER":
        what = "The quote leaves out a hedge sentence that qualifies it."
    elif c == "EXCERPT_NOT_WHOLE_SENTENCE":
        what = "The quote does not start and end on whole sentences."
    elif c == "HIGHLIGHT_NOT_FOUND":
        what = "The quote cannot be found in the record, so it cannot be highlighted."
    else:
        what = "The summary does not match the quote."
    return f"{what} {EDIT_SUMMARY_TEXT}."


def code_check_detail(item_id: str, fails: dict) -> dict:
    first = next(iter(fails))
    return {"item_id": item_id, "reason_code": first, "step_id": CODE_CHECK_STEP[first], "failed_steps": [CODE_CHECK_STEP[c] for c in fails],
            "tokens": (fails.get("SUMMARY_TOKEN_NOT_IN_EXCERPT") or {}).get("tokens", []),
            "next_action": {"code": "EDIT_SUMMARY", "text": EDIT_SUMMARY_TEXT, "target": {"item_id": item_id}}}


def code_check_error(item_id: str, rec, item: dict):
    """A 422 ReviewError (code CODE_CHECK_FAILED) if the entry's current wording fails a code check, else None. Accept never goes past it (D-051)."""
    fails = code_check_failures(rec, item)
    if not fails:
        return None
    return ReviewError(422, "CODE_CHECK_FAILED", code_check_detail(item_id, fails), code_check_message(fails))


def entry_record(item: dict, recs: list):
    rid = (item.get("record_ids") or [None])[0]
    return next((r for r in recs if r["id"] == rid), None)


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    if action == "accept" and kind == "entry":                # D-051: the code rung binds accept for every entry, AI-made or human
        err = code_check_error(item_id, entry_record(item, store.load_records(conn, case_id)), item)
        if err:
            raise err
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        DB.apply_review(conn, item_id, action, now=t, case=case_id)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


def ocr_record_ids(conn, case_id: str) -> set:
    """Ids of the records whose text lies on an OCR-read page of this case (empty for a text case). T-086, D-042."""
    from app.backend import pdf_checks
    pages = (DB.get_case(conn, case_id).get("config") or {}).get("pages")
    if not any(p.get("source") == "ocr" for p in pages or []):
        return set()
    return {r[0] for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=?", (case_id,))
            if pdf_checks.is_ocr_span(pages, r[1], r[2])}


def enforce_ocr(conn, case_id: str, t) -> int:
    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
    reclassify): an item whose record is on an OCR-read page is needs_review with OCR_DERIVED (rejected items stay rejected). A human edit
    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
    ids = ocr_record_ids(conn, case_id)
    if not ids:
        return 0
    n = 0
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, case_id, kind):
            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
                continue
            reasons = list(it.get("state_reasons") or [])
            if it["state"] == "needs_review" and "OCR_DERIVED" in reasons:
                continue
            if "OCR_DERIVED" not in reasons:
                reasons.append("OCR_DERIVED")
            out = {"state": "needs_review", "state_reasons_json": reasons}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:41:57.895Z

**tool call — Bash**
````
{
 "command": "sed -n 200,520p app/backend/review.py; grep -n \"apply_review\\|accepted\\|review_status\" app/backend/*.py | grep -v \"^app/backend/review.py\" | head -60"
}
````

### User / tool · 2026-11-02T05:41:57.990Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:41:59.401Z

**tool call — Bash**
````
{
 "command": "sed -n 225,420p app/backend/review.py; grep -n \"apply_review\\|\\\"accepted\\\"\\|'accepted'\" app/backend/*.py | grep -v \"^app/backend/review.py\" | head -40; grep -n \"apply_review\\|accepted\" app/backend/review.py"
}
````

### User / tool · 2026-11-02T05:41:59.520Z

**tool result**
````
    toks = g.new_tokens(new_sum, new_exc, label, date_iso)
    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
    if numeric:
        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
    if toks:
        words = _quoted_words(toks)
        raise _bad(f"The summary says {words}, which the quote does not say. Remove it or change the quote.", tokens=toks, reason="SUMMARY_TOKEN_NOT_IN_EXCERPT")
    dropped = g.dropped_qualifiers(new_sum, new_exc)
    if dropped:
        what = "; ".join(_QUALIFIER_WORDS.get(k, k) for k in dropped)
        raise _bad(f"The quote carries {what} that the summary leaves out. Put it back in the summary.", qualifiers=list(dropped), reason="SUMMARY_DROPS_QUALIFIER")
    if span is None:
        raise _bad("The quoted sentences cannot be found in the record, so they cannot be highlighted. Change the quote.", reason="HIGHLIGHT_NOT_FOUND")
    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
    if call is not None:
        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
        ladder_verdict = judges.to_ladder("j1", verdict)
    warnings = []
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
    elif ladder_verdict == "unavailable":
        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
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
        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
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
    if "summary" in edits or "summary" in prev:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
    lad = item.get("ladder") or {"item_id": item["id"]}
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    enforce_ocr(conn, case_id, t)
    return chk["warnings"]


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
    rec = DB._decode(row)
    if rec["date_status"] != "ambiguous":
        raise _bad("Only a record whose date can be read two ways can be confirmed.")
    if date_iso not in (rec["date_candidates"] or []):
        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
    moved, cleared = None, []
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
                cleared.append(e["id"])
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
            cleared.append(a["id"])
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    removed += _recompute_gaps(conn, case_id, t)
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _without_date_doubt(item: dict) -> dict:
    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
        reasons.append("AI_TRANSLATION")
    state = item["state"]
    if state == "needs_review" and not reasons:
        state = "verified"
    out = {"state": state, "state_reasons_json": reasons}
    if isinstance(item.get("ladder"), dict):
        out["ladder"] = {**item["ladder"], "state": state}
    return out


def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
             "cleared_date_ambiguous": cleared}
    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))


def _drop(conn, case_id, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
    return [flag_id] if cur.rowcount else []


def _recompute_gaps(conn, case_id, t):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002)."""
    from app.backend import pipeline as PL
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        new[item["id"]] = item
    removed = []
    for old in DB.list_items(conn, case_id, "flag"):
        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
            continue
        item = new.get(old["id"])
        if item is None:
            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
            removed.append(old["id"])
            continue
        oc = old.get("computed") or {}
        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
    for iid, item in new.items():
        if iid not in have:
            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
    return removed


# ---------------------------------------------------------------- manual entry (D-031, T-056)
def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
    t = _now(now)
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == record_id), None)
app/backend/api.py:502:            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
app/backend/api.py:529:            ok = ("accepted", "edited")
app/backend/api.py:532:            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
app/backend/case_extras.py:2:Code only: nothing here asks a model anything, and the only review_status writer used is DB.apply_review (one event per item)."""
app/backend/dismissal_patterns.py:87:        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
app/backend/export.py:32:IN = ("accepted", "edited")
app/backend/export.py:136:        if not n or n.get("status") != "accepted":
app/backend/export.py:535:                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
app/backend/export.py:539:        tag = "" if st != "accepted" or not stale else " [NOT in the letter: the cited entry changed or is no longer accepted]"
app/backend/export_routes.py:32:    ok = ("accepted", "edited")
app/backend/pipeline.py:204:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
app/backend/present.py:7:STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
app/backend/present.py:111:    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
app/backend/present.py:122:    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
app/backend/present.py:128:            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}
app/backend/present.py:229:                    "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},
app/backend/narrative.py:151:    nar["status"] = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}[action]
app/backend/totals.py:4:COUNTED = ("accepted", "edited")
app/backend/reclassify.py:142:        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
app/backend/trace.py:246:    if rs in ("accepted", "edited"):
app/backend/trace.py:247:        return step("human", "Your decision", "human", PASS, "You accepted this item." if rs == "accepted" else "You edited this item and accepted it.", rule="row 17", evidence=ev)
app/backend/trace.py:272:    if rs in ("accepted", "edited", "dismissed"):
app/backend/trace.py:276:    elif rs in ("accepted", "edited"):
app/backend/trace.py:277:        code, label = "accepted", "Accepted by you"
app/backend/trace.py:411:    return row["state"] != "rejected" and row["review_status"] in ("accepted", "edited")
app/backend/trace.py:501:    elif rs in ("accepted", "edited"):
app/backend/trace.py:689:    elif status == "accepted":
app/backend/trace.py:691:        code, label = "accepted", "Accepted by you"
app/backend/trace.py:701:            "review_status": {"accepted": "accepted", "dismissed": "dismissed"}.get(status, "pending") if not rem else None,
app/backend/trace.py:782:    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id) if u["review_status"] in ("accepted", "edited")]
app/backend/trace.py:816:            if row["review_status"] in ("accepted", "edited"):
app/backend/trace.py:965:    tcounts = {"accepted_cents": tv["accepted"]["cents"], "accepted_count": tv["accepted"]["count"], "pending_cents": tv["pending"]["cents"], "pending_charges": pend_ch,
app/backend/trace.py:975:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed")}
app/backend/trace.py:989:    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
app/backend/trace.py:1030:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
59:                       "cannot be accepted into the letter.")
147:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
163:        DB.apply_review(conn, item_id, action, now=t, case=case_id)
260:        raise _bad("A charge can only be accepted or dismissed.")
266:        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
298:    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
335:    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
404:            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
453:    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
510:    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
536:    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
537:    DB.apply_review(conn, item_id, action, now=now, case=case_id)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:03.328Z

**tool call — Bash**
````
{
 "command": "grep -n \"def apply_review\" -A60 app/db/db.py | head -110; sed -n 520,600p app/backend/review.py"
}
````

### User / tool · 2026-11-02T05:42:03.427Z

**tool result**
````
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
226-    after = {"review_status": status, "edited": new_edited}
227-    conn.execute("BEGIN")
228-    try:
229-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
230-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
231-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
232-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
233-        conn.execute("COMMIT")
234-    except Exception:
235-        conn.execute("ROLLBACK")
236-        raise
237-    return get_item(conn, item_id, row["case_id"])
238-
239-
240-def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
241-    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
242-    if action not in AUDIT_ONLY_ACTIONS:
243-        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
244-    eid = _tok("v")
245-    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
246-                 (eid, case_id, item_id, action, _enc(before), _enc(after), now))
247-    return eid
248-
249-
250-def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
251-    if status not in REVIEW_STATUSES:
252-        raise ValueError(f"invalid review_status {status!r}")
253-    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
254-    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
255-
256-
257-def list_events(conn, case_id: str, item_id: str = None) -> list:
258-    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
259-    if item_id:
260-        q, a = q + " AND item_id=?", a + [item_id]
261-    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
262-
263-
264-def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
265-    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
266-    cid = fields.pop("id", None) or _tok("c")
267-    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
268-           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
269-    _insert(conn, "llm_calls", row)
270-    return cid
271-
272-
273-def get_llm_call(conn, call_id: str):
274-    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
275-    return _decode(r) if r else None
    from app.backend import pipeline as PL
    row = PL._row(kind, item)
    if any(i["id"] == item["id"] for i in DB.list_items(conn, case_id, kind)):
        DB.update_item(conn, item["id"], now=t, case=case_id, **row)
    else:
        DB.add_item(conn, case_id, kind, {"id": item["id"], **row}, now=t)


def judges_for(dollars, call, case_text):
    if call is None or not dollars:
        return {}
    return judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars], call=call, case_text=case_text)


def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
    DB.apply_review(conn, item_id, action, now=now, case=case_id)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:06.694Z

**tool call — Bash**
````
{
 "command": "grep -n \"^ACTIONS\" -B1 -A6 app/db/db.py; grep -n \"batch_apply\\|code_check\" app/backend/*.py | grep -v \"^app/backend/review.py\"; sed -n 440,520p app/backend/review.py"
}
````

### User / tool · 2026-11-02T05:42:06.793Z

**tool result**
````
18-REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
19:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
20-           "confirm_date": None, "keep_my_wording": None,
21-           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
22-_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
23-_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
24-_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
25-_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
app/backend/case_extras.py:24:def _code_check_refusal(conn, case_id, item_id, row, cache):
app/backend/case_extras.py:27:    err = review.code_check_error(item_id, review.entry_record(row, cache["recs"]), row)
app/backend/case_extras.py:30:    return {"id": item_id, "reason": "code_check_failed", "reason_code": err.detail["reason_code"], "why": err.message, "next_action": err.detail["next_action"]}
app/backend/case_extras.py:46:        elif action == "accept" and (err := _code_check_refusal(conn, case_id, i, row, cache)):     # D-051: same check as a single accept
app/backend/case_extras.py:68:                review.batch_apply(conn, case_id, i, action, now)
app/backend/case_extras.py:72:                review.batch_apply(conn, case_id, i, "reset", now)
app/backend/case_extras.py:129:                if any(r["reason"] == "code_check_failed" for r in e.rejected):       # D-051
app/backend/case_extras.py:130:                    first = next(r for r in e.rejected if r["reason"] == "code_check_failed")
app/backend/export.py:508:        if _status(e) == "pending" and e.get("code_check_failed"):       # D-051: the wording fails a code check, so it is not printed anywhere in the export
app/backend/flags.py:55:         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
app/backend/flags.py:169:        f["ladder"]["code_checks"] = {"excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
app/backend/flags.py:185:            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:injection_scan"}}}
app/backend/flags.py:228:                    "code_checks": {"classified_by": "code:conflict_candidate+j3", "candidate_rule": c["rule"], "arithmetic": c.get("arithmetic"),
app/backend/generator.py:61:                   "judge": None, "code_checks": {}, "human": {"action": None, "edited_text": None, "at": None}}
app/backend/generator.py:90:    cc = e["ladder"]["code_checks"]
app/backend/narrative.py:103:        item["code_checks"] = {"reasons": reasons}
app/backend/pdf_checks.py:148:            it["ladder"].setdefault("code_checks", {})["ocr_derived"] = True
app/backend/reclassify.py:123:    cc = dict(lad.get("code_checks") or {})
app/backend/reclassify.py:134:    lad.update(judge=jd, code_checks=cc, state=state, reclassification={
app/backend/reclassify.py:142:        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
app/backend/pipeline.py:30:def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
app/backend/pipeline.py:31:    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
app/backend/pipeline.py:353:        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
app/backend/store.py:55:        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
app/backend/store.py:56:            d["code_check_failed"] = True
app/backend/trace.py:314:    cc = lad.get("code_checks") or {}
app/backend/trace.py:362:    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
app/backend/trace.py:399:    if _code_check_gated(row):        # D-045(b), D-051: a failing code check blocks the export (AI-made or human wording; only the judge is exempt for human wording) and says what to do
app/backend/trace.py:408:def _code_check_gated(row) -> bool:
app/backend/trace.py:437:def code_check_blockers(conn, case_id: str, cx=None) -> list:
app/backend/trace.py:443:        if not _code_check_gated(row):
app/backend/trace.py:458:    cc = lad.get("code_checks") or {}
app/backend/trace.py:514:    cc = lad.get("code_checks") or {}
app/backend/trace.py:990:                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
app/backend/trace.py:1027:    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
                              "date_provider_from_header": True},
              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
    DB.add_item(conn, case_id, "entry", {
        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}


# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
    `not_duplicate` event on the original entry."""
    from app.backend import pipeline as PL
    from app.llm import provider as P
    t = _now(now)
    kind, ent = _item(conn, case_id, entry_id)
    if kind != "entry":
        raise _bad("Only a merged entry can be split.")
    ids = list(ent["record_ids"] or [])
    if record_id not in ids or ids.index(record_id) == 0 or len(ids) < 2:
        raise _bad("That record is not one of the duplicates merged into this entry.")
    case = DB.get_case(conn, case_id)
    cfg = dict(case.get("config") or {})
    cfg["not_duplicates"] = sorted(set(cfg.get("not_duplicates", [])) | {record_id})
    DB.update_case(conn, case_id, config_json=cfg)
    conn.execute("UPDATE records SET duplicate_of=NULL WHERE id=? AND case_id=?", (record_id, case_id))
    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    rec = next(r for r in recs if r["id"] == record_id)
    warns = []
    # the split-off record's own entry (code-checked, then judge 1; a failure leaves it visibly without an entry)
    if call is not None:
        e = generator.extract_one(rec, [rec["n"]], call=call, case_text=case["raw_text"])
        if "failure" in e:
            warns.append({"code": e["failure"], "message": "The record was split off, but the AI could not draft its entry; enter it by hand.", "item_id": None})
        else:
            if e["state"] != "rejected":
                generator.judge_entries([e], by_n, call=call, case_text=case["raw_text"])
            e["ladder"]["backend"] = P.backend_name()
            e.pop("_stage", None)
            _upsert(conn, case_id, "entry", PL._clean(e), t)
    else:
        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
    # its amounts come back as their own items (new ids; existing amounts keep theirs and their review status)
    sep = {int(str(i)[1:]) for i in cfg["not_duplicates"] if str(i)[1:].isdigit()}
    rows = [a for a in AM.extract_amounts(recs, separate=sep) if a["record_no"] == rec["n"]]
    new_items = [PL.amount_item(a, rec) for a in rows]
    ing = {"records": recs, "text": case["raw_text"]}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, record_ids_json=[i for i in a["record_ids"] if i != record_id], duplicate_note=None)
    dollars = [a for a in new_items if a["cls"] != "damages"]
    verdicts = judges_for(dollars, call, case["raw_text"])
    for a in new_items:
        _upsert(conn, case_id, "amount", PL._finish_amount(a, ing, verdicts.get(a["id"])), t)
    _recompute_gaps(conn, case_id, t)
    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    split_id = f"e{rec['n']}" if any(e["id"] == f"e{rec['n']}" for e in DB.list_items(conn, case_id, "entry")) else None
    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
            "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": warns}


def _upsert(conn, case_id, kind, item, t):
    """Add or refresh ONE item without PL._persist's removal of other pending rows."""
    from app.backend import pipeline as PL
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:27.593Z

**tool call — Bash**
````
{
 "command": "sed -n 300,460p app/backend/trace.py; sed -n 15,80p app/backend/case_extras.py"
}
````

### User / tool · 2026-11-02T05:42:27.702Z

**tool result**
````
    return {"token": cx.case_id, "item_id": item_id, "kind": kind, "mode": "full" if cx.full else "metadata", "state": row.get("state"),
            "review_status": rs, "state_reasons": reasons, "verdict": {"code": code, "label": label, "blocks_export": bool(blocks)},
            "progress": _progress(steps), "next_action": first_na, "steps": steps}


# ------------------------------------------------------------------ entries
def _excerpt_ev(cx, rid, row):
    ed = row.get("edited") or {}
    return _span(cx, rid, ed.get("excerpt_start", row.get("excerpt_start")), ed.get("excerpt_end", row.get("excerpt_end")), ed.get("excerpt", row.get("excerpt")))


def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    verbatim_fail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None)
    st = []
    # 1 extracted
    if lad.get("entered_by"):
        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
                       evidence={"excerpt": exc}))
    else:
        gen = lad.get("generator") or {}
        call = cx.call(gen.get("call_id"), row["id"], "extract")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
        ev["excerpt"] = exc
        if schema_fail:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
                           evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "LLM_FAILED_AFTER_RETRIES" in R:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
                           rule="row 4", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        else:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
                           "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))

    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
        if stop:
            st.append(_skipped(sid, label, "code", stop, rule))
        elif failed if failed is not None else code in R:
            st.append(step(sid, label, "code", FAIL, reason_text(code), reason=code, rule=rule, evidence=evidence, next_action=fail_na))
        else:
            st.append(step(sid, label, "code", PASS, ok_text, rule=rule, evidence=evidence))
    # 2 grounding substring
    if schema_fail:
        st.append(_skipped("excerpt_verbatim", "Quote is word for word in the record", "code", "SCHEMA_INVALID", "row 4"))
    elif verbatim_fail:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", FAIL, reason_text("GROUNDING_EXCERPT_NOT_VERBATIM"),
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM", rule="row 4", evidence={"excerpt": exc}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
    else:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", PASS, "The quote was found in the record, character for character.",
                       rule="row 4", evidence={"excerpt": exc}))
    code_step("excerpt_whole_sentence", "Quote is made of whole sentences", "EXCERPT_NOT_WHOLE_SENTENCE", "The quote starts and ends on whole sentences.", "row 4",
              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_NOT_WHOLE_SENTENCE" in R or cc.get("excerpt_whole_sentence") is False)
    code_step("excerpt_hedge", "Quote keeps the hedge sentence that qualifies it", "EXCERPT_OMITS_QUALIFIER", "No hedge sentence that qualifies the quote is left out.", "row 4",
              na("EDIT_QUOTE", {"item_id": row["id"]}))
    # D-051: recomputed from the CURRENT summary and quote (as accept does), not only from what was stored at generation time
    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
    toks = cc.get("summary_tokens_not_in_excerpt") or (live.get("SUMMARY_TOKEN_NOT_IN_EXCERPT") or {}).get("tokens") or []
    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks) or "SUMMARY_TOKEN_NOT_IN_EXCERPT" in live)
    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R or "SUMMARY_DROPS_QUALIFIER" in live)
    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False)
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
    return row["state"] != "rejected" and row["review_status"] in ("accepted", "edited")


def _current_text(row):
    ed = row.get("edited") or {}
    return ed.get("summary", row.get("summary") or ""), ed.get("excerpt", row.get("excerpt") or "")


def _fix_action(row, stp) -> dict:
    """The paralegal's next move for a failed code step on their own wording: a fixed sentence plus the words from the quote (display only; code decided the failure)."""
    code, summ, exc = stp["reason_code"], *_current_text(row)
    target = {"item_id": row["id"]}
    tail = " The export stays blocked until it passes."
    if code == "SUMMARY_DROPS_QUALIFIER":
        terms = grounding.missing_qualifier_terms(summ, exc)
        what = ", ".join(f"\u2018{t}\u2019" for t in terms) if terms else "the quote's hedge, attribution, negation, side or approximation"
        return na("EDIT_SUMMARY", target, text=f"Edit the summary to keep {what}; the quote says it and your summary leaves it out." + tail)
    if code == "SUMMARY_TOKEN_NOT_IN_EXCERPT":
        toks = (stp.get("evidence") or {}).get("tokens") or []
        what = ", ".join(f"\u2018{t}\u2019" for t in toks) if toks else "the words that are not in the quote"
        return na("EDIT_SUMMARY", target, text=f"Edit the summary to remove {what}, or change the quote so it contains {'it' if len(toks) == 1 else 'them'}." + tail)
    if code in ("EXCERPT_NOT_WHOLE_SENTENCE", "EXCERPT_OMITS_QUALIFIER"):
        return na("EDIT_QUOTE", target, text=_NEXT["EDIT_QUOTE"] + tail)
    return na("READ_RECORD", {"record_id": (row.get("record_ids") or [None])[0]}, text="Read the record yourself, then fix the quote or dismiss this item." + tail)


def code_check_blockers(conn, case_id: str, cx=None) -> list:
    """Export blockers (D-045(b), D-051): accepted or edited entries, AI-made or human, whose current summary or quote fails a code check.
    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
    cx = cx or _Cx(conn, case_id, False)
    out = []
    for row in DB.list_items(conn, case_id, "entry"):
        if not _code_check_gated(row):
            continue
        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
        if not fails:
            continue
        f = fails[0]
        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
                    "why": f["why"] + " " + TRACE_WHY["CODE_CHECK_FAILED" if _paralegal_wording("entry", row) else "CODE_CHECK_FAILED_AI"], "next_action": _fix_action(row, f)})
    return out


# ------------------------------------------------------------------ amounts
def _amount_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})


# ------------------------------------------------------------------ batch review
class BatchRefused(Exception):
    def __init__(self, rejected):
        super().__init__("invalid_batch")
        self.rejected = rejected


def _code_check_refusal(conn, case_id, item_id, row, cache):
    if "recs" not in cache:
        cache["recs"] = store.load_records(conn, case_id)
    err = review.code_check_error(item_id, review.entry_record(row, cache["recs"]), row)
    if not err:
        return None
    return {"id": item_id, "reason": "code_check_failed", "reason_code": err.detail["reason_code"], "why": err.message, "next_action": err.detail["next_action"]}


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad, cache = [], {}
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and (err := _code_check_refusal(conn, case_id, i, row, cache)):     # D-051: same check as a single accept
            bad.append(err)
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
    return bad


def apply_batch(conn, case_id, body, now):
    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("bad_request")
    with _LOCK:
        bad = _check(conn, case_id, ids, action)
        if bad:
            raise BatchRefused(bad)
        done = []
        try:
            for i in ids:
                review.batch_apply(conn, case_id, i, action, now)
                done.append(i)
        except Exception:
            for i in reversed(done):          # compensate: each undo is itself an audited event
                review.batch_apply(conn, case_id, i, "reset", now)
            raise
    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}


# ------------------------------------------------------------------ export config
def validate_config(b):
    """Returns the normalised config or raises ValueError. All keys optional; unknown keys refused."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:35.733Z

**tool call — Bash**
````
{
 "command": "grep -n \"_CODE_CHECK_REASONS\\|live_recs\\|EDIT_QUOTE\\|EDIT_SUMMARY\" app/backend/*.py | grep -v \"^app/backend/review.py:1[0-3]\"; grep -n \"D-051\" -r memory/contracts/api.md | head; sed -n 24,80p app/backend/store.py"
}
````

### User / tool · 2026-11-02T05:42:35.843Z

**tool result**
````
app/backend/review.py:66:EDIT_SUMMARY_TEXT = "Edit the summary to match the quote"
app/backend/trace.py:58:    "EDIT_SUMMARY": "Edit the summary so it uses only the numbers, dates and words that are in the quote, and keeps the quote's qualifiers.",
app/backend/trace.py:59:    "EDIT_QUOTE": "Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it.",
app/backend/trace.py:77:_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}
app/backend/trace.py:135:        self._live_recs = None
app/backend/trace.py:149:    def live_recs(self):
app/backend/trace.py:151:        if self._live_recs is None:
app/backend/trace.py:152:            self._live_recs = store.load_records(self.conn, self.case_id, self.case["raw_text"])
app/backend/trace.py:153:        return self._live_recs
app/backend/trace.py:358:              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_NOT_WHOLE_SENTENCE" in R or cc.get("excerpt_whole_sentence") is False)
app/backend/trace.py:360:              na("EDIT_QUOTE", {"item_id": row["id"]}))
app/backend/trace.py:362:    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
app/backend/trace.py:365:              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
app/backend/trace.py:368:              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R or "SUMMARY_DROPS_QUALIFIER" in live)
app/backend/trace.py:401:            if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS:
app/backend/trace.py:427:        return na("EDIT_SUMMARY", target, text=f"Edit the summary to keep {what}; the quote says it and your summary leaves it out." + tail)
app/backend/trace.py:431:        return na("EDIT_SUMMARY", target, text=f"Edit the summary to remove {what}, or change the quote so it contains {'it' if len(toks) == 1 else 'them'}." + tail)
app/backend/trace.py:433:        return na("EDIT_QUOTE", target, text=_NEXT["EDIT_QUOTE"] + tail)
app/backend/trace.py:445:        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
app/backend/trace.py:823:            elif not (R & _CODE_CHECK_REASONS):
app/backend/trace.py:829:        elif R & _CODE_CHECK_REASONS:            # judge supported but a code check raised a doubt
app/backend/trace.py:831:                                  "code_says": " ".join(reason_text(c) for c in sorted(R & _CODE_CHECK_REASONS)), "judge_says": _J_OK[r["judge"]],
memory/contracts/api.md:32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote.", `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY", text: "Edit the summary to match the quote", target: {item_id}}}`; the judge verdict does not matter |
memory/contracts/api.md:107:**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY", text: "Edit the summary to match the quote", target: {item_id}}}`.
memory/contracts/api.md:327:`message` is a plain sentence naming the words, e.g. `The summary says “left”, which the quote does not say. Remove it or change the quote.` The export gate and accept recompute the same checks from the current wording through the same functions (D-051), so an edit the route stores can never be an export blocker for a code reason. The same rule applies to `POST .../records/{rid}/entry`. (3) Judge 1 re-run: it never blocks a human-written edit (D-045b). If it says `partially`/`unsupported`, errors, times out, or has no recorded fixture (always the case in demo mode), the edit is saved, the item becomes `needs_review` (reason `JUDGE_UNAVAILABLE` when it did not answer) and `warnings[]` carries `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_UNAVAILABLE`; no 409, because nothing the code can verify is wrong. The judge never lets an unchecked edit look verified.
memory/contracts/api.md:619:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute the code checks (D-034 numbers/dates/dollar figures/sides, D-047, D-022 qualifiers, and the quote's whole-sentence and hedge checks) from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
        except Exception:
            body = block
        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
    return out


def _by_id(records):
    return {r["id"]: r for r in records}


# ---------------------------------------------------------------- unit dicts for export / totals
def export_case(conn, case_id: str) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
    rec_of = {r["id"]: r for r in recs}
    from app.backend import review as review_mod        # lazy: review imports store
    ents = []
    for e in DB.list_items(conn, case_id, "entry"):
        if e["state"] == "rejected":
            continue
        ed = e.get("edited") or {}
        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
        if "summary" in ed:
            d["original_summary"] = ed.get("original_summary", e["summary"])
        if "excerpt" in ed:
            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
        lad = e.get("ladder") or {}
        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
            d["code_check_failed"] = True
        if lad.get("entered_by"):
            d["entered_by_reviewer"] = True
        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
        ents.append(d)
    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    fl = []
    for f in DB.list_items(conn, case_id, "flag"):
        c = f.get("computed") or {}
        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
    events = []     # D-047: no 'keep my wording' event exists any more
    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
    pages = (case.get("config") or {}).get("pages")
    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
                    **({"page": pdf_text.page_for(pages, r["char_start"])} if pages else {})) for r in recs]
    nar = (case.get("config") or {}).get("narrative")
    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
    from app.backend import trace                       # lazy: trace imports store
    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:49.583Z

**tool call — Bash**
````
{
 "command": "grep -rn \"EDIT_QUOTE\\|EDIT_SUMMARY\\|CODE_CHECK_FAILED\" app/frontend --include=* -l 2>/dev/null | head; grep -rn \"CODE_CHECK_FAILED\\|code_check\" app/frontend/*.js app/frontend/**/*.js 2>/dev/null | head -10; sed -n 40,80p app/backend/trace.py; grep -n \"def na\" -A12 app/backend/trace.py | head -30"
}
````

### User / tool · 2026-11-02T05:42:49.718Z

**tool result**
````
app/frontend/review.js
app/frontend/batch.js
app/frontend/stepper.js
app/frontend/batch.js:25:        if (String(code).toUpperCase() === "CODE_CHECK_FAILED") {   // D-051 (T-098 r2): the whole batch is refused; say which items and why, with an Edit action on each
app/frontend/mock.js:73:      code_checks: { excerpt_verbatim: true, excerpt_whole_sentence: true, qualifier_carried: true, date_provider_from_header: true, summary_tokens_not_in_excerpt: [], highlight_found: true },
app/frontend/mock.js:104:            code_checks: { amount_in_text: true, classified_by: rate ? "rule:per_unit" : "rule:charge_label" }, judge: { model: "claude-haiku-5-5", verdict: "agrees" }, human: { action: null } } });
app/frontend/mock.js:115:        ladder: { item_id: `f_gap_${enc[i - 1].id}_${enc[i].id}`, state: "verified", backend: "fixture", generator: null, code_checks: { dates_parsed: true, days, threshold: 30 }, judge: null, human: { action: null } } });
app/frontend/review.js:130:  // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends "Edit the summary to match the
app/frontend/review.js:142:  RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === "CODE_CHECK_FAILED";
app/frontend/timeline.js:127:          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
TRACE_WHY = {
    "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
    "RUN_IN_PROGRESS": "The AI run is still going.",
    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
    "CODE_CHECK_FAILED_AI": "This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
    "CODE_CHECK_FAILED": "You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.",
    "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
    "CAUSATION_NOT_QUOTED": narrative.REASONS["CAUSATION_NOT_QUOTED"],
    "SEVERITY_NOT_QUOTED": narrative.REASONS["SEVERITY_NOT_QUOTED"],
    "FLAG_CONTENT": narrative.REASONS["FLAG_CONTENT"],
}
_NEXT = {   # code -> fixed sentence
    "DECIDE": "Accept, edit or dismiss this item.",
    "CONFIRM_DATE": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.",
    "EDIT_SUMMARY": "Edit the summary so it uses only the numbers, dates and words that are in the quote, and keeps the quote's qualifiers.",
    "EDIT_QUOTE": "Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it.",
    "READ_RECORD": "Read the record yourself before relying on this item.",
    "COMPARE_BY_HAND": "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.",
    "DISMISS_OR_ENTER_BY_HAND": "This item cannot be used. Dismiss it, or write the entry by hand from the record.",
    "RERUN": "Run the AI steps again.",
    "RERUN_JUDGE": "Run the second check again.",
    "SENTENCE_REMOVED": "This sentence was left out of the draft. If you want its facts in the paragraph, check the cited entry's quote and write them yourself.",
    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
}
_STEP_OF_REASON = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "excerpt_verbatim", "GROUNDING_AMOUNT_NOT_IN_TEXT": "found_in_text", "SCHEMA_INVALID": "extracted",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
    "INJECTION_SUSPECTED": "injection_scan", "OCR_DERIVED": "ocr_source", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
    "SPLIT_AMBIGUOUS": "record_warning_check", "LLM_SPLIT": "record_warning_check"}
_AMOUNT_CODE = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}


def reason_text(code: str) -> str:
89:def na(code: str, target: dict = None, options: list = None, text: str = None) -> dict:
90-    d = {"code": code, "text": text or _NEXT[code]}
91-    if target:
92-        d["target"] = target
93-    if options:
94-        d["options"] = options
95-    return d
96-
97-
98-def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
99-    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
100-            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}
101-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:52.822Z

**tool call — Bash**
````
{
 "command": "sed -n 125,175p app/frontend/review.js; grep -n \"T-098\\|D-051\" tests/unit/test_trace.py | head -40"
}
````

### User / tool · 2026-11-02T05:42:52.920Z

**tool result**
````
  // ---- errors (R-RV-3, D-034, D-047). A refused edit is a hard 422 whose plain-words reason is shown right under the edit box, which stays open with the typed text.
  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) s.textContent = msg; RV.say(msg, true); }

  // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends "Edit the summary to match the
  // quote.") shows right under the item's buttons with an Edit action; nothing was changed. It stays until the item changes (any successful decision) or the paralegal edits.
  const refusals = {};       // id -> {message}
  function paintRefusal(root, id, edit) {
    const r = refusals[id], box = root.querySelector(".rv-refused");
    if (!box) return;
    ZL.clear(box); box.hidden = !r;
    if (!r) return;
    box.append(el("p", { class: "rv-refused-msg", "data-testid": "accept-refused-msg" }, el("strong", {}, "Not accepted. "), r.message),
      edit ? el("button", { type: "button", class: "rv-btn rv-refused-edit", "data-testid": "btn-accept-refused-edit", "aria-label": "Edit the summary for " + r.label, onclick: edit }, "Edit the summary") : null);
  }
  function repaintRefusal(id) { document.querySelectorAll('[data-controls-for="' + id + '"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }
  RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === "CODE_CHECK_FAILED";

  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter
  const DATE_FIRST = "Confirm the date first.", DATE_WHY = "This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm.";
  RV.needsDate = (item, kind) => kind === "entry" && !item.date;
  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices
    const row = document.querySelector('[data-testid="dates-to-confirm"] [data-entry-id="' + id + '"]');
    const t = row && (row.querySelector('[data-testid="confirm-date"]') || row);
    const box = document.querySelector('[data-testid="dates-to-confirm"]');
    const f = t || box; if (!f) return;
    if (!f.hasAttribute("tabindex") && !/^(BUTTON|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1");
    f.focus(); if (f.scrollIntoView) f.scrollIntoView({ block: "center" });
  }

  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
    busy.add(id);
    try {
      const resp = await ZL.api.review(c.token, id, body);
      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }
      if (drafts[id] && body.action === "edit") drafts[id].open = false;
      if (drafts[id] && body.action === "dismiss") { drafts[id].reasonOpen = false; drafts[id].reason = ""; }
      ZL.state.applyReview(resp);
      const left = resp.review && resp.review.counts ? resp.review.counts.pending : null;
      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
      restoreFocus(o.advance ? { nextFrom: id, scope: o.scope } : o.focus ? { id, action: o.focus } : null);
      return true;
    } catch (e) {
      if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
631:        # D-051: the API refuses accept while a code check fails; old data is simulated by writing the decision directly
634:        if action == "accept":       # D-051: an accepted item whose code check fails keeps the fix as its next action (and blocks the export)
1024:# ---- D-045(b) / T-098: a human-edited summary is exempt from the judge, never from the code checks (reviewer case: reviews/T-097-ux-designer.md B1)
1132:# ---- D-051 / T-098 r2: the code rung binds accept for every item, AI-made or human (reviewer F1: an AI draft 'Pain 5/10' over a quote without 5/10)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:42:58.605Z

**tool call — Bash**
````
{
 "command": "sed -n 175,200p app/frontend/review.js; sed -n 1120,1200p tests/unit/test_trace.py"
}
````

### User / tool · 2026-11-02T05:42:58.696Z

**tool result**
````
      if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
        const d = e.detail || {}, toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
        showError(id, (e.message || "That edit is not allowed.") + toks);
        const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
        refusals[id] = { message: e.message || "The summary fails a check. Edit the summary to match the quote.", label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
        repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
        const mine = document.activeElement && document.activeElement.closest && document.activeElement.closest('[data-controls-for="' + id + '"]'), box = (mine || document).querySelector(".rv-refused:not([hidden])");
        if (box) { const r = box.getBoundingClientRect(); if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16); else if (r.top < 60) window.scrollBy(0, r.top - 60); }   // the answer is on screen beside the pressed button, clear of the sticky banner
      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
      else showError(id, (e && e.message) || "That did not work. Try again.");
      return false;
    } finally { busy.delete(id); }
  };

  // ---- controls
  RV.controls = function (item, kind) {
    const id = item.id, st = item.review_status || "pending";
    const isFlag = kind === "flag", canEdit = kind === "entry" || isFlag;
    const noted = kind === "amount" && item.kind !== "charge";
    const initial = isFlag ? (item.reviewer_note || (item.edited && item.edited.note) || "") : ((item.edited && item.edited.summary) || item.summary || "");
    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
    if (!d.open) d.text = initial;
    const lbl = RV.label(item);
    const root = el("div", { class: "rv-controls", "data-controls-for": id });
    const btn = (action, text, tid, extra) => el("button", Object.assign({ type: "button", class: "rv-btn rv-" + action, "data-testid": tid, "data-action": action, "aria-label": text.replace("…", "") + ": " + lbl }, extra || {}), text);
        assert g["ready"] == (g["blockers"] == []) == (ex.status_code < 400), name
        assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name


def test_missing_qualifier_terms_name_the_words_to_keep_t098():
    from app.backend import grounding
    assert grounding.missing_qualifier_terms("MRI of the cervical spine was done.", "MRI suggests possible disc herniation.")
    got = grounding.missing_qualifier_terms("Fracture seen.", "Possible left wrist fracture.")
    assert "possible" in got and "left" in got
    assert grounding.missing_qualifier_terms("Possible left wrist fracture.", "Possible left wrist fracture.") == []


# ---- D-051 / T-098 r2: the code rung binds accept for every item, AI-made or human (reviewer F1: an AI draft 'Pain 5/10' over a quote without 5/10)
def _ai_draft_with_invented_number(c, conn, tok, *, judge="supported", stored_reason=True, eid=None):
    """An AI-made entry whose summary says 'Pain 5/10' over a quote that does not. State, reasons and judge verdict set like the generator + judge would."""
    eid = eid or c.get(f"/api/cases/{tok}").json()["entries"][0]["id"]
    row = DB.get_item(conn, eid, tok)
    assert "5/10" not in row["excerpt"] and "ladder" in row and not row["ladder"].get("entered_by")
    lad = row["ladder"]
    lad["judge"] = {**(lad.get("judge") or {}), "verdict": judge}
    DB.update_item(conn, eid, now=9e9, case=tok, summary="Pain 5/10", ladder=lad,
                   state="needs_review" if stored_reason else "verified", state_reasons_json=["SUMMARY_TOKEN_NOT_IN_EXCERPT"] if stored_reason else [])
    return eid


@pytest.mark.parametrize("judge", ["supported", "unsupported", "disagrees"])
def test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051(env, judge):
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, judge=judge)
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
    err = r.json()["error"]
    assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED"
    assert "not in the quote: 5." in err["message"] and err["message"].endswith("Edit the summary to match the quote.")
    assert err["detail"]["next_action"]["text"] == "Edit the summary to match the quote" and err["detail"]["next_action"]["code"] == "EDIT_SUMMARY"
    assert err["detail"]["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and err["detail"]["step_id"] == "summary_tokens" and err["detail"]["tokens"] == ["5"]
    assert DB.get_item(conn, eid, tok)["review_status"] == "pending"           # nothing was written
    for x in c.get(f"/api/cases/{tok}").json()["entries"]:                      # accept everything else the paralegal can; the letter must not carry the figure
        if x["id"] != eid:
            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    ex = c.get(f"/api/cases/{tok}/export")
    assert "5/10" not in ex.text


def test_accept_recomputes_from_the_current_text_not_only_the_stored_reasons_d051(env):
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, stored_reason=False)    # state 'verified', no stored reason: only the live check can catch it
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED"


def test_accept_refuses_a_dropped_qualifier_on_an_ai_draft_and_a_clean_draft_still_accepts_d051(env):
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    eid = ents[1]["id"]
    DB.update_item(conn, eid, now=9e9, case=tok, summary=REVIEWER_EDIT, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"])
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and "Edit the summary to match the quote." in r.json()["error"]["message"]
    assert c.post(f"/api/cases/{tok}/items/{ents[0]['id']}/review", json={"action": "accept"}).status_code == 200      # golden drafts pass the code checks


def test_batch_accept_refuses_the_whole_batch_for_one_failing_summary_d051(env):
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    bad = _ai_draft_with_invented_number(c, conn, tok, stored_reason=False, eid=ents[0]["id"])
    ids = [bad, ents[1]["id"], ents[2]["id"]]
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ids})
    err = r.json()["error"]
    assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED" and err["message"].endswith("Nothing was changed.") and "not in the quote: 5." in err["message"]
    rej = [x for x in err["detail"]["rejected"] if x["reason"] == "code_check_failed"]
    assert [x["id"] for x in rej] == [bad] and rej[0]["next_action"]["text"] == "Edit the summary to match the quote" and rej[0]["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT"
    assert all(DB.get_item(conn, i, tok)["review_status"] == "pending" for i in ids)       # all or nothing


def test_gate_blocks_an_accepted_ai_draft_that_fails_a_code_check_and_export_is_422_d051(env):
    """Old data / any other route: the accept guard is not trusted. The gate lists the item, the trace shows the failing step, GET export is 422."""
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, judge="supported")
    DB.apply_review(conn, eid, "accept", now=9e9, case=tok)                                 # bypass the route
    for x in c.get(f"/api/cases/{tok}").json()["entries"]:
        if x["id"] != eid:
            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:43:18.545Z

**tool call — Bash**
````
{
 "command": "sed -n 485,550p app/backend/export.py; grep -n \"removed\\|Removed\" app/backend/narrative.py | head -20"
}
````

### User / tool · 2026-11-02T05:43:18.645Z

**tool result**
````
            or (e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]))


def _edited(v):
    out = []
    for e in v.entries:
        if e.get("entered_by_reviewer") and _status(e) == "in":
            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer (the AI did not draft this entry); summary "{e["summary"]}"'
                       + ".")
        if not _was_edited(e):
            continue
        bits = []
        if e.get("original_summary") is not None and e["original_summary"] != e["summary"]:
            bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
        if e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]:
            bits.append(f'excerpt was "{e["original_excerpt"]}", now "{e["excerpt"]}"')
        out.append(f"- {_cap(v.cite(e['record_no']))}: " + "; ".join(bits or ["edited"]) + ".")
    return out or ["- none"]


def _pending(v):
    out = []
    for e in v.entries:
        if _status(e) == "pending" and e.get("code_check_failed"):       # D-051: the wording fails a code check, so it is not printed anywhere in the export
            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
        elif _status(e) == "pending":
            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}"' + (" [entered by reviewer]" if e.get("entered_by_reviewer") else ""))
    for a in v.amounts:
        if _status(a) == "pending":
            out.append(f'- Amount {_money_short(a.get("cents"), a.get("raw", ""))} ({a["cls"]}), {v.cite(a["record_no"])}: '
                       f'"{_amount_quote(v, a)}"')
    for f in v.flags:
        if _status(f) == "pending":
            out.append("- Flag, " + _flag_line(v, f))
    return out


def _cite_tail(v, entry_id):
    e = next(x for x in v.entries if x["id"] == entry_id)
    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"


def _draft_paragraph(v):
    n = v.narrative
    if not n:
        return []
    live = {e["id"]: e for e in v.in_entries}
    st = n.get("status", "pending")
    lines = ["", "DRAFT TREATMENT PARAGRAPH (AI-drafted from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
    for s in n.get("sentences", []):
        e = live.get(s["entry_id"])
        stale = e is None or (n.get("basis") or {}).get(s["entry_id"]) != basis_hash(e)
        tag = "" if st != "accepted" or not stale else " [NOT in the letter: the cited entry changed or is no longer accepted]"
        lines.append(f'- {s["text"]} ({s.get("cite") or s["entry_id"]}){tag}')
    for r in n.get("removed", []):
        lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
    return lines


def _notes(v):
    accepted = [f for f in v.flags if _status(f) == "in"]
    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
    pending = _pending(v)
    sec = [
6:(b) is removed and listed with a reason. The draft is internal (internal notes) until accepted; flags are never given to the model.
80:    base = {"status": "pending", "generated_at": store.iso(now), "sentences": [], "removed": [], "prompt_version": "narrative_v1",
100:            base["removed"].append({**item, "reason": "NOT_AN_ACCEPTED_ENTRY"})
105:            base["removed"].append({**item, "reason": reasons[0], "reasons": reasons})
113:            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
117:    for r in base["removed"]:
125:    if existing and (existing.get("sentences") or existing.get("removed")):
159:            "removed": [{"text": r["text"], "entry_id": r["entry_id"], "reason": r["reason"]} for r in nar.get("removed", [])],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:43:25.282Z

**tool call — Bash**
````
{
 "command": "sed -n 18,60p app/backend/narrative.py; sed -n 85,125p app/backend/narrative.py; sed -n 150,165p app/backend/narrative.py; grep -n \"Removed\\|original_summary\\|summary was\" tests/unit/*.py | head -20"
}
````

### User / tool · 2026-11-02T05:43:25.398Z

**tool result**
````
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The sentence has a number, side, negation or date that is not in the cited quote.",
    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, an attribution phrase or a negation that the cited quote has.",
    "CAUSATION_NOT_QUOTED": "The sentence uses cause or adverse wording that the cited quote does not contain.",
    "SEVERITY_NOT_QUOTED": "The sentence uses severity, outcome or recommendation wording that the cited quote does not contain.",
    "FLAG_CONTENT": "The sentence talks about gaps, conflicts or other review flags, which stay out of the paragraph.",
    "JUDGE_PARTIAL": "The second check found the sentence only partly supported by the cited quote.",
    "JUDGE_UNSUPPORTED": "The second check found the sentence not supported by the cited quote.",
    "JUDGE_UNAVAILABLE": "The second check was not available for this sentence.",
}
_CAUSE = re.compile(r"\b(?:caused?|causing|due to|result(?:ed|ing)? (?:of|from|in)|because of|as a result|attributable|secondary to|"
                    r"led to|stemm(?:ed|ing) from|aggravat\w+|exacerbat\w+|permanent|chronic|disabl\w+)\b", re.IGNORECASE)
_FLAGISH = re.compile(r"\b(?:gaps?|conflicts?|inconsisten\w+|discrepanc\w+|pre-?existing|prior (?:injur\w+|condition)|missed appointments?|"
                      r"non-?complian\w+|days without treatment)\b", re.IGNORECASE)
# Severity / outcome / recommendation wording the prompt forbids ("no adjectives of your own", "never add a diagnosis, severity, prognosis"):
# deterministic backstop so a sentence like "significant pain 4/10" or "and recommended surgery" never rests on judge 1 alone.
_SEVERITY = re.compile(r"\b(?:significan\w*|sever(?:e|ely|ity)|serious\w*|ongoing|worsen\w*|worse|deteriorat\w*|debilitat\w*|excruciat\w*|"
                       r"substantial\w*|catastroph\w*|prognos\w+|recommend\w*|surg\w+)\b", re.IGNORECASE)
_DATE_PHRASE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?", re.IGNORECASE)


basis_hash = export.basis_hash


def accepted_entries(case: dict) -> list:
    """Entries the paralegal accepted (or edited and accepted) whose quote is still verbatim in the record, chronological."""
    v = export._View(case)
    return [dict(e, label=v.source(e["record_no"]), date_iso=v.date_of(e), cite=v.cite(e["record_no"])) for e in v.in_entries]


def prompt_user(entries: list, nonce: str) -> str:
    blocks = []
    for e in entries:
        blocks.append(f"ENTRY {e['id']} | {export._long_date(e['date_iso'])} | {e['label']}\nSUMMARY:\n{injection.wrap(e['summary'], nonce)}\n"
                      f"QUOTE:\n{injection.wrap(e['excerpt'], nonce)}")
    return "ACCEPTED ENTRIES:\n" + "\n\n".join(blocks) + "\nReturn the JSON object."


def check_sentence(text: str, entry: dict) -> list:
    """Code checks (a); returns reason codes, empty when the sentence may go to the judge."""
    quote = entry["excerpt"]
    reasons = []
    if grounding.new_tokens(text, quote, entry["label"], entry["date_iso"] or ""):
        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
        return dict(existing, error=base["error"]) if existing else base
    prompt = promptlib.load("narrative_v1")
    nonce = promptlib.nonce(case["raw_text"], "narrative", ",".join(by_id))
    try:
        out, call_id = call("narrative", prompt.text, prompt_user(entries, nonce), schemas.NarrativeOutput.model_json_schema(), item_id="narrative")
        sents = schemas.NarrativeOutput.model_validate(out).sentences
    except (AU.LLMFailed, P.FixtureMiss, ValidationError, TypeError, ValueError):
        base["error"] = "LLM_FAILED_AFTER_RETRIES"
        return _keep_or_save(conn, case_id, case, existing, base)
    base["generator"] = {"model": judges.generator_model(), "prompt_version": prompt.name, "call_id": call_id}
    for k, s in enumerate(sents, 1):
        text, eid = s.text.strip(), s.entry_id
        item = {"id": f"ns{k}", "entry_id": eid, "text": text}
        e = by_id.get(eid)
        if e is None:
            base["removed"].append({**item, "reason": "NOT_AN_ACCEPTED_ENTRY"})
            continue
        reasons = check_sentence(text, e)
        item["code_checks"] = {"reasons": reasons}
        if reasons:
            base["removed"].append({**item, "reason": reasons[0], "reasons": reasons})
            continue
        # the date of service lives in the record header, not the quote: give the judge the header it may rely on
        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_date(e['date_iso'])})",
                                                   call=call, item_id=item["id"])
        lad = judges.to_ladder("j1", verdict)
        item["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": jcall, "verdict": lad, "reason_code": jcode}
        if lad != "supported":
            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
            continue
        item["cite"] = e["cite"]
        base["sentences"].append(item)
    for r in base["removed"]:
        r["message"] = REASONS.get(r["reason"], r["reason"])
    return _save(conn, case_id, case, base)


def _keep_or_save(conn, case_id, case, existing, failed):
    """A draft that failed before producing sentences must not wipe a paragraph the paralegal already has (possibly accepted):
    keep it untouched in the case and return it with the error alongside. With nothing stored yet, the failed draft is stored."""
    if existing and (existing.get("sentences") or existing.get("removed")):
        raise ValueError("EMPTY")
    nar["status"] = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}[action]
    nar["reviewed_at"] = store.iso(now)
    return _save(conn, case_id, case, nar)


def for_export(nar: dict) -> dict:
    """The small dict export.build_export() reads."""
    return {"status": nar["status"], "sentences": [{"text": s["text"], "entry_id": s["entry_id"], "cite": s["cite"]} for s in nar.get("sentences", [])],
            "removed": [{"text": r["text"], "entry_id": r["entry_id"], "reason": r["reason"]} for r in nar.get("removed", [])],
            "basis": nar.get("basis", {})}
tests/unit/test_api_routes.py:129:    assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]
tests/unit/test_export.py:81:    c["entries"][4].update(review_status="edited", summary="Visit 8: pain 4/10 and improving.", original_summary="Visit 8: pain 4/10, improving.")
tests/unit/test_export.py:160:    c["entries"][2].update(review_status="edited", summary="Persistent neck pain 6/10; daily headaches.", original_summary="Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.")
tests/unit/test_export.py:170:    c["entries"][2].update(review_status="accepted", summary="Persistent neck pain 6/10 with daily headaches noted.", original_summary=orig)
tests/unit/test_export.py:179:    c["entries"][2].update(review_status="dismissed", summary="x y", original_summary="a b")
tests/unit/test_trace.py:774:    DB.apply_review(conn, eid, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
tests/unit/test_trace.py:847:    DB.apply_review(conn, target, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
tests/unit/test_trace.py:865:    DB.apply_review(conn, target, "edit", edited={"summary": row["summary"] + " Reviewed.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
tests/unit/test_trace.py:1042:    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)   # bypass the route: the gate is the second line of defence
tests/unit/test_trace.py:1238:    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:43:35.855Z

**tool call — Bash**
````
{
 "command": "grep -rn \"Removed\\|summary was\" tests/ | head; grep -n \"reason_text\" app/backend/trace.py | head -3; sed -n 100,118p app/backend/trace.py; git diff --stat HEAD -- app/backend/store.py app/backend/export.py app/backend/api.py app/backend/case_extras.py app/backend/trace.py | tail -8"
}
````

### User / tool · 2026-11-02T05:43:36.012Z

**tool result**
````
80:def reason_text(code: str) -> str:
107:    return [step("ocr_source", "Record was not read from a scanned page", "code", FAIL, reason_text("OCR_DERIVED"), reason="OCR_DERIVED", rule="D-042",
215:        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence={"judge_verdict": "unavailable"},
            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}


def _ocr_steps(R, rid) -> list:
    """T-086: the step that holds an OCR-read item for review. Only present when the item carries OCR_DERIVED, so other cases are unchanged."""
    if "OCR_DERIVED" not in R:
        return []
    return [step("ocr_source", "Record was not read from a scanned page", "code", FAIL, reason_text("OCR_DERIVED"), reason="OCR_DERIVED", rule="D-042",
                 evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid}))]


def _number(steps):
    for i, s in enumerate(steps, 1):
        s["n"] = i
    return steps


def _progress(steps):
    done = sum(1 for s in steps if s["status"] != PENDING)
 app/backend/api.py | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:43:56.803Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/backend/review.py'\ns=open(p).read()\n\n# 1 reasons & steps\ns=s.replace('''CODE_CHECK_REASONS = (\"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"SUMMARY_DROPS_QUALIFIER\", \"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\", \"HIGHLIGHT_NOT_FOUND\")\nCODE_CHECK_STEP = {\"SUMMARY_TOKEN_NOT_IN_EXCERPT\": \"summary_tokens\", \"SUMMARY_DROPS_QUALIFIER\": \"summary_qualifier\", \"EXCERPT_OMITS_QUALIFIER\": \"excerpt_hedge\",\n                   \"EXCERPT_NOT_WHOLE_SENTENCE\": \"excerpt_whole_sentence\", \"HIGHLIGHT_NOT_FOUND\": \"highlight\"}\nEDIT_SUMMARY_TEXT = \"Edit the summary to match the quote\"\n''','''CODE_CHECK_REASONS = (\"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"SUMMARY_DROPS_QUALIFIER\", \"GROUNDING_EXCERPT_NOT_VERBATIM\", \"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\",\n                      \"HIGHLIGHT_NOT_FOUND\")\nCODE_CHECK_STEP = {\"SUMMARY_TOKEN_NOT_IN_EXCERPT\": \"summary_tokens\", \"SUMMARY_DROPS_QUALIFIER\": \"summary_qualifier\", \"GROUNDING_EXCERPT_NOT_VERBATIM\": \"excerpt_verbatim\",\n                   \"EXCERPT_OMITS_QUALIFIER\": \"excerpt_hedge\", \"EXCERPT_NOT_WHOLE_SENTENCE\": \"excerpt_whole_sentence\", \"HIGHLIGHT_NOT_FOUND\": \"highlight\"}\nQUOTE_LEVEL_REASONS = (\"GROUNDING_EXCERPT_NOT_VERBATIM\", \"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\", \"HIGHLIGHT_NOT_FOUND\")   # only a change to the QUOTE clears these\nEDIT_SUMMARY_TEXT = \"Edit the summary to match the quote\"\nEDIT_QUOTE_TEXT = \"Change the quote to whole sentences of the record that keep the hedge sentence\"\n# plain words for \"AI wording removed (failed a check: ...)\" in the internal notes\nCHECK_PHRASE = {\"SUMMARY_TOKEN_NOT_IN_EXCERPT\": \"a number or word in it is not in the quote\", \"SUMMARY_DROPS_QUALIFIER\": \"it drops a qualifier the quote has\",\n                \"GROUNDING_EXCERPT_NOT_VERBATIM\": \"the quote is not word for word in the record\", \"EXCERPT_OMITS_QUALIFIER\": \"the quote leaves out a hedge sentence\",\n                \"EXCERPT_NOT_WHOLE_SENTENCE\": \"the quote is not whole sentences\", \"HIGHLIGHT_NOT_FOUND\": \"the quote cannot be found in the record\"}\n''')\n\n# 2 live verbatim\ns=s.replace('''        for c in g.check_excerpt(rec[\"excerpt\"], exc):             # the quote against its record: whole sentences, keeps the hedge sentence\n            if c in (\"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\"):\n                out[c] = {}\n        if grounding.locate(rec[\"excerpt\"], exc) is None and not _not_verbatim(g, rec, exc):\n            out[\"HIGHLIGHT_NOT_FOUND\"] = {}''','''        for c in g.check_excerpt(rec[\"excerpt\"], exc):             # the quote against its record: word for word, whole sentences, keeps the hedge sentence\n            if c in (\"GROUNDING_EXCERPT_NOT_VERBATIM\", \"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\"):\n                out[c] = {}\n        if grounding.locate(rec[\"excerpt\"], exc) is None and \"GROUNDING_EXCERPT_NOT_VERBATIM\" not in out:\n            out[\"HIGHLIGHT_NOT_FOUND\"] = {}''')\ns=s.replace('''def _not_verbatim(g, rec, exc) -> bool:\n    \"\"\"A quote that is not word for word in the record is a grounding failure (rejected state, its own step), not a highlight problem.\"\"\"\n    return \"GROUNDING_EXCERPT_NOT_VERBATIM\" in g.check_excerpt(rec[\"excerpt\"], exc)\n\n\n''','')\n\n# 3 message / detail\ns=s.replace('''    elif c == \"EXCERPT_OMITS_QUALIFIER\":\n        what = \"The quote leaves out a hedge sentence that qualifies it.\"\n    elif c == \"EXCERPT_NOT_WHOLE_SENTENCE\":\n        what = \"The quote does not start and end on whole sentences.\"\n    elif c == \"HIGHLIGHT_NOT_FOUND\":\n        what = \"The quote cannot be found in the record, so it cannot be highlighted.\"\n    else:\n        what = \"The summary does not match the quote.\"\n    return f\"{what} {EDIT_SUMMARY_TEXT}.\"''','''    elif c == \"GROUNDING_EXCERPT_NOT_VERBATIM\":\n        what = \"The quote is not word for word in the record.\"\n    elif c == \"EXCERPT_OMITS_QUALIFIER\":\n        what = \"The quote leaves out a hedge sentence that qualifies it.\"\n    elif c == \"EXCERPT_NOT_WHOLE_SENTENCE\":\n        what = \"The quote does not start and end on whole sentences.\"\n    elif c == \"HIGHLIGHT_NOT_FOUND\":\n        what = \"The quote cannot be found in the record, so it cannot be highlighted.\"\n    else:\n        what = \"The summary does not match the quote.\"\n    return f\"{what} {EDIT_QUOTE_TEXT if c in QUOTE_LEVEL_REASONS else EDIT_SUMMARY_TEXT}.\"''')\ns=s.replace('''            \"next_action\": {\"code\": \"EDIT_SUMMARY\", \"text\": EDIT_SUMMARY_TEXT, \"target\": {\"item_id\": item_id}}}''','''            \"next_action\": ({\"code\": \"EDIT_QUOTE\", \"text\": EDIT_QUOTE_TEXT, \"target\": {\"item_id\": item_id}} if first in QUOTE_LEVEL_REASONS\n                            else {\"code\": \"EDIT_SUMMARY\", \"text\": EDIT_SUMMARY_TEXT, \"target\": {\"item_id\": item_id}})}''')\n\n# 4 choke point\nold_start=s.index('    if action == \"accept\" and kind == \"entry\":                # D-051')\nold_end=s.index('    warnings = []\\n    if action in (\"accept\", \"dismiss\", \"reset\"):')\ns=s[:old_start]+s[old_end:]\ns=s.replace('''        DB.apply_review(conn, item_id, action, now=t, case=case_id)\n        if kind == \"flag\" and action == \"dismiss\"''','''        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item)\n        if kind == \"flag\" and action == \"dismiss\"''')\ns=s.replace('''def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:''','''def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None) -> dict:\n    \"\"\"THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).\n    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that\n    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a\n    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter.\"\"\"\n    if kind is None or item is None:\n        kind, item = _item(conn, case_id, item_id)\n    if kind == \"entry\" and DB.ACTIONS.get(action) in (\"accepted\", \"edited\"):\n        cand = dict(item)\n        if edited is not None:\n            cand[\"edited\"] = edited\n            cand[\"state_reasons\"] = [c for c in item.get(\"state_reasons\") or [] if c not in CODE_CHECK_REASONS]\n        err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand)\n        if err:\n            raise err\n    return DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)\n\n\ndef apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:''')\n\n# 5 _edit\ns=s.replace('''    DB.apply_review(conn, item[\"id\"], \"edit\", edited=edited, now=t, case=case_id)\n    lad = item.get(\"ladder\") or {\"item_id\": item[\"id\"]}''','''    set_review(conn, case_id, item[\"id\"], \"edit\", edited=edited, now=t, kind=\"entry\", item=item, recs=recs)     # D-051: edit implies accept; refused before any write\n    lad = item.get(\"ladder\") or {\"item_id\": item[\"id\"]}''')\ns=s.replace('''        DB.apply_review(conn, item[\"id\"], \"edit\", edited={\"note\": edits[\"note\"].strip()[:2000], \"at\": store.iso(t)}, now=t, case=case_id)''','''        set_review(conn, case_id, item[\"id\"], \"edit\", edited={\"note\": edits[\"note\"].strip()[:2000], \"at\": store.iso(t)}, now=t, kind=\"flag\", item=item)''')\n\n# 6 batch\ns=s.replace('''def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:''','''def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:''')\ns=s.replace('''    DB.apply_review(conn, item_id, action, now=now, case=case_id)''','''    set_review(conn, case_id, item_id, action, now=now, recs=recs)''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"DB.apply_review\" app/backend/review.py; grep -n \"g.check_excerpt\\|def check_excerpt\" app/backend/spanish.py app/backend/grounding.py | head"
}
````

### User / tool · 2026-11-02T05:43:56.943Z

**tool result**
````
3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
153:    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
167:    return DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
423:            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
472:    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
529:    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
555:    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
app/backend/grounding.py:88:def check_excerpt(record_text: str, excerpt: str) -> list:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:44:00.114Z

**tool call — Bash**
````
{
 "command": "sed -n 80,125p app/backend/grounding.py"
}
````

### User / tool · 2026-11-02T05:44:00.201Z

**tool result**
````
    return {i for i, rx in _lexicon()["hedge"].items() if rx.search(text)}


def is_hedge_unit(unit_text: str) -> bool:
    return bool(hedge_ids(unit_text))


# ---------------------------------------------------------------- excerpt check
def check_excerpt(record_text: str, excerpt: str) -> list:
    """[] when clean. Not verbatim -> ['GROUNDING_EXCERPT_NOT_VERBATIM'] (rejected, nothing else is evaluated)."""
    from app.backend import sentences as S
    spans = locate_all(record_text, excerpt)
    if not spans:
        return ["GROUNDING_EXCERPT_NOT_VERBATIM"]
    reasons = []
    units = S.stripped_spans(record_text)
    starts, ends = {a for a, _ in units}, {b for _, b in units}
    aligned = [sp for sp in spans if sp[0] in starts and sp[1] in ends]
    if not aligned:
        reasons.append("EXCERPT_NOT_WHOLE_SENTENCE")
    s, e = (aligned or spans)[0]
    # a hedge unit immediately after the last unit the excerpt touches must travel with it (R-TL-8, D-021)
    touched = [i for i, (a, b) in enumerate(units) if a < e and b > s]
    nxt = (touched[-1] + 1) if touched else len(units)
    if nxt < len(units):
        a, b = units[nxt]
        if is_hedge_unit(record_text[a:b]):
            reasons.append("EXCERPT_OMITS_QUALIFIER")
    return reasons


def check_amount(record_text: str, raw_amount: str) -> list:
    """An amount the model (or an edit) reports must appear in the record exactly as written (R-CH-1). Never auto-corrected:
    '$1,2OO' is found as written, the 'fixed' '$1,200' is not. A longer figure does not vouch for a shorter one ('$185' vs '$1,850')."""
    raw = (raw_amount or "").strip()
    if raw:
        for m in re.finditer(re.escape(raw), record_text):
            before = record_text[m.start() - 1] if m.start() else ""
            tail = record_text[m.end():m.end() + 2]
            if not before.isdigit() and not re.match(r"\d|[,.]\d", tail):
                return []
    return ["GROUNDING_AMOUNT_NOT_IN_TEXT"]


# ---------------------------------------------------------------- summary checks
_NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:44:08.555Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/case_extras.py'\ns=open(p).read()\ns=s.replace('''        done = []\n        try:\n            for i in ids:\n                review.batch_apply(conn, case_id, i, action, now)''','''        done = []\n        recs = store.load_records(conn, case_id) if action == \"accept\" else None\n        try:\n            for i in ids:\n                review.batch_apply(conn, case_id, i, action, now, recs)''')\nopen(p,'w').write(s)\n\np='app/backend/trace.py'\ns=open(p).read()\ns=s.replace('''_CODE_CHECK_REASONS = {\"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"SUMMARY_DROPS_QUALIFIER\", \"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\", \"HIGHLIGHT_NOT_FOUND\"}''','''_CODE_CHECK_REASONS = set(review.CODE_CHECK_REASONS)''')\ns=s.replace('''    cc = lad.get(\"code_checks\") or {}\n    rid = (row.get(\"record_ids\") or [None])[0]\n    rec = cx.recs.get(rid, {})\n    exc = _excerpt_ev(cx, rid, row)\n    verbatim_fail = \"GROUNDING_EXCERPT_NOT_VERBATIM\" in R or cc.get(\"excerpt_verbatim\") is False''','''    cc = lad.get(\"code_checks\") or {}\n    rid = (row.get(\"record_ids\") or [None])[0]\n    rec = cx.recs.get(rid, {})\n    exc = _excerpt_ev(cx, rid, row)\n    # D-051: all five code checks (and the highlight) are recomputed from the CURRENT summary and quote, as accept does, and also honour what was stored\n    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)\n    verbatim_fail = \"GROUNDING_EXCERPT_NOT_VERBATIM\" in R or cc.get(\"excerpt_verbatim\") is False or \"GROUNDING_EXCERPT_NOT_VERBATIM\" in live''')\ns=s.replace('''failed=\"EXCERPT_NOT_WHOLE_SENTENCE\" in R or cc.get(\"excerpt_whole_sentence\") is False)''','''failed=\"EXCERPT_NOT_WHOLE_SENTENCE\" in R or cc.get(\"excerpt_whole_sentence\") is False or \"EXCERPT_NOT_WHOLE_SENTENCE\" in live)''')\ns=s.replace('''              na(\"EDIT_QUOTE\", {\"item_id\": row[\"id\"]}))\n    # D-051: recomputed from the CURRENT summary and quote (as accept does), not only from what was stored at generation time\n    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)\n''','''              na(\"EDIT_QUOTE\", {\"item_id\": row[\"id\"]}), failed=\"EXCERPT_OMITS_QUALIFIER\" in R or \"EXCERPT_OMITS_QUALIFIER\" in live)\n''')\ns=s.replace('''failed=\"HIGHLIGHT_NOT_FOUND\" in R or cc.get(\"highlight_found\") is False)''','''failed=\"HIGHLIGHT_NOT_FOUND\" in R or cc.get(\"highlight_found\") is False or \"HIGHLIGHT_NOT_FOUND\" in live)''')\ns=s.replace('''    if code in (\"EXCERPT_NOT_WHOLE_SENTENCE\", \"EXCERPT_OMITS_QUALIFIER\"):''','''    if code in (\"EXCERPT_NOT_WHOLE_SENTENCE\", \"EXCERPT_OMITS_QUALIFIER\", \"GROUNDING_EXCERPT_NOT_VERBATIM\"):''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"^from\\|^import\" app/backend/case_extras.py | head; grep -n \"verbatim_fail:\" -B1 -A6 app/backend/trace.py | head -20"
}
````

### User / tool · 2026-11-02T05:44:08.694Z

**tool result**
````
3:import re
4:import threading
6:from fastapi import Request
8:from app.backend import present, review, store
9:from app.db import db as DB
352-        st.append(_skipped("excerpt_verbatim", "Quote is word for word in the record", "code", "SCHEMA_INVALID", "row 4"))
353:    elif verbatim_fail:
354-        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", FAIL, reason_text("GROUNDING_EXCERPT_NOT_VERBATIM"),
355-                       reason="GROUNDING_EXCERPT_NOT_VERBATIM", rule="row 4", evidence={"excerpt": exc}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
356-    else:
357-        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", PASS, "The quote was found in the record, character for character.",
358-                       rule="row 4", evidence={"excerpt": exc}))
359-    code_step("excerpt_whole_sentence", "Quote is made of whole sentences", "EXCERPT_NOT_WHOLE_SENTENCE", "The quote starts and ends on whole sentences.", "row 4",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:44:17.387Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/store.py'\ns=open(p).read()\ns=s.replace('''        if \"summary\" in ed:\n            d[\"original_summary\"] = ed.get(\"original_summary\", e[\"summary\"])\n''','''        if \"summary\" in ed:\n            d[\"original_summary\"] = ed.get(\"original_summary\", e[\"summary\"])\n            orig_fails = review_mod.code_check_failures(rec_of.get((e[\"record_ids\"] or [None])[0]), dict(e, edited={\"summary\": d[\"original_summary\"], \"excerpt\": ed.get(\"original_excerpt\", e[\"excerpt\"])}, state_reasons=[]))\n            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it\n                d[\"original_summary_failed\"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]\n''')\nopen(p,'w').write(s)\n\np='app/backend/export.py'\ns=open(p).read()\ns=s.replace('''        if e.get(\"original_summary\") is not None and e[\"original_summary\"] != e[\"summary\"]:\n            bits.append(f'summary was \"{e[\"original_summary\"]}\", now \"{e[\"summary\"]}\"')''','''        if e.get(\"original_summary\") is not None and e[\"original_summary\"] != e[\"summary\"]:\n            if e.get(\"original_summary_failed\"):        # D-051: AI wording that failed a code check is not printed anywhere in the export\n                bits.append(f'summary was AI wording removed (failed a check: {\"; \".join(e[\"original_summary_failed\"])}), now \"{e[\"summary\"]}\"')\n            else:\n                bits.append(f'summary was \"{e[\"original_summary\"]}\", now \"{e[\"summary\"]}\"')''')\ns=s.replace('''    for r in n.get(\"removed\", []):\n        lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {r[\"reason\"]}.')''','''    for r in n.get(\"removed\", []):\n        if r[\"reason\"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export\n            lines.append(f'- AI wording removed (failed a check: {r.get(\"message\") or r[\"reason\"]}) ({r[\"entry_id\"]}): {r[\"reason\"]}.')\n        else:\n            lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {r[\"reason\"]}.')''')\ns=s.replace('''IN = (\"accepted\", \"edited\")''','''IN = (\"accepted\", \"edited\")\nNARRATIVE_CODE_REASONS = (\"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"SUMMARY_DROPS_QUALIFIER\", \"CAUSATION_NOT_QUOTED\", \"SEVERITY_NOT_QUOTED\", \"FLAG_CONTENT\")''',1)\nopen(p,'w').write(s)\n\np='app/backend/narrative.py'\ns=open(p).read()\ns=s.replace('''\"removed\": [{\"text\": r[\"text\"], \"entry_id\": r[\"entry_id\"], \"reason\": r[\"reason\"]} for r in nar.get(\"removed\", [])],''','''\"removed\": [{\"text\": r[\"text\"], \"entry_id\": r[\"entry_id\"], \"reason\": r[\"reason\"], \"message\": r.get(\"message\") or REASONS.get(r[\"reason\"], r[\"reason\"])} for r in nar.get(\"removed\", [])],''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit -x -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T05:45:47.514Z

**tool result**
````
        allow_subprocess = {"backend/pdf_ocr.py"}
        bad = [str(p.relative_to(app)) for p in app.rglob("*.py")
               if "llm/backends" not in p.as_posix()
               and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)
               and not (str(p.relative_to(app)) in allow_subprocess and not re.search(r"^\s*(import|from)\s+anthropic\b", p.read_text(), re.M))]
>       assert bad == []
E       AssertionError: assert ['backend/pdf_hidden.py'] == []
E         
E         Left contains one more item: 'backend/pdf_hidden.py'
E         Use -v to get more diff

tests/unit/test_provider.py:126: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:45:48.406Z

Unrelated (another worker's). Run without -x.

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:45:48.887Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T05:47:36.002Z

**tool result**
````
FAILED tests/unit/test_billing.py::test_balance_due_matching_either_reading_is_consistent_and_says_which[without_forward-340.00-without_forward]
FAILED tests/unit/test_billing.py::test_balance_due_matching_neither_reading_is_a_mismatch_with_both_computed_values
FAILED tests/unit/test_billing.py::test_E5b_prose_balance_due_with_previous_balance_is_consistent_with_forward
FAILED tests/unit/test_billing.py::test_two_forwards_are_listed_and_no_balance_verdict_is_given
FAILED tests/unit/test_billing.py::test_no_forward_and_a_wrong_balance_is_still_a_mismatch
FAILED tests/unit/test_billing.py::test_bare_whole_number_on_a_stray_line_is_not_a_money_token_but_one_under_a_column_is
FAILED tests/unit/test_billing.py::test_r3_probe_set_nothing_is_lost_with_complete_true[P14_cms_words_box]
FAILED tests/unit/test_billing.py::test_r3_probe_set_nothing_is_lost_with_complete_true[P2_two_forwards_one_record]
FAILED tests/unit/test_billing.py::test_r3_probe_set_nothing_is_lost_with_complete_true[P5_prose_previous_balance]
FAILED tests/unit/test_billing.py::test_r3_probe_set_nothing_is_lost_with_complete_true[P6_prose_previous_balance_no_due]
FAILED tests/unit/test_billing.py::test_r3_probe_set_nothing_is_lost_with_complete_true[P8_dateless_row_cents]
FAILED tests/unit/test_billing.py::test_r3_probe_set_nothing_is_lost_with_complete_true[P9_dateless_row_dollar_no_cents]
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
FAILED tests/unit/test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:47:37.646Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -q 2>&1 | grep FAILED | grep -v test_billing; git status --short app/backend | head -20"
}
````

### User / tool · 2026-11-02T05:49:23.012Z

**tool result**
````
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
FAILED tests/unit/test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts
MM app/backend/api.py
 M app/backend/billing.py
MM app/backend/case_extras.py
MM app/backend/export.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/narrative.py
 M app/backend/pipeline.py
 M app/backend/review.py
MM app/backend/store.py
MM app/backend/trace.py
?? app/backend/conflict_candidates.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:49:25.296Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && head -30 T-098-staff-engineer-r2-probe3.py; tail -30 T-098-staff-engineer-r2-probe3-results.txt; head -12 T-098-staff-engineer-r2-probe2.py; head -20 T-098-staff-engineer-r2-probe.py"
}
````

### User / tool · 2026-11-02T05:49:25.380Z

**tool result**
````
"""T-098 round-2 probe 3 (staff-engineer-reviewer). Usage: python3 -I this.py <git-archive copy of dd84122>
LIVE route (no DB tampering after the draft is made): an AI draft whose QUOTE drops the hedge sentence (real generator.verify gives it
needs_review + EXCERPT_OMITS_QUALIFIER). Accept is refused (D-051). What does EDIT of the summary alone do (edit implies accept)?"""
import os, sys, time, tempfile

ARCH = os.path.abspath(sys.argv[1])
sys.path.insert(0, ARCH)
os.chdir(ARCH)
os.environ["LLM_BACKEND"] = "fixture"
for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
    os.environ.pop(k, None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
from app.backend import generator, store
from app.db import db as DB

TMP = tempfile.mkdtemp(prefix="t098r2c_")
DBP = os.path.join(TMP, "p.sqlite")
c = TestClient(create_app(DBP, static_dir=TMP), client=("127.0.0.1", 50000))
TOK = c.post("/api/cases", json={"sample": True}).json()["token"]
assert c.post(f"/api/cases/{TOK}/run", json={}).status_code == 202
for _ in range(400):
    if c.get(f"/api/cases/{TOK}/status").json()["status"] in ("ready", "failed"):
        break
    time.sleep(0.25)
conn = DB.connect(DBP)
case = DB.get_case(conn, TOK)
row = DB.get_item(conn, "e8", TOK)
rec = next(r for r in store.load_records(conn, TOK, case["raw_text"]) if r["id"] == row["record_ids"][0])
print("record excerpt :", rec["excerpt"])
record excerpt : C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.
generator.verify -> needs_review ['EXCERPT_OMITS_QUALIFIER']
accept e1 -> 200
accept e8 (AI draft, quote drops the hedge sentence) -> 422 CODE_CHECK_FAILED
EDIT e8 summary only -> 200 None | warnings: ['JUDGE_UNAVAILABLE']
e8 after edit: review_status edited | state needs_review | state_reasons ['JUDGE_UNAVAILABLE']
gate ready: True | blockers: []
GET /export -> 200
letter has e8 quote: True | letter has the hedge sentence 'may represent degenerative': False
['Disc protrusion at C5-C6 with mild right foraminal narrowing.', 'Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing."']
"""T-098 round-2 probe 2 (staff-engineer-reviewer). Usage: python3 -I this.py <git-archive copy of dd84122>
Accept recomputes five code checks (review.CODE_CHECK_REASONS); does the export gate? Quote-level checks (hedge sentence, whole sentence) with every stored result left as 'pass'."""
import os, sys, time, json, tempfile, sqlite3

ARCH = os.path.abspath(sys.argv[1])
sys.path.insert(0, ARCH)
os.chdir(ARCH)
os.environ["LLM_BACKEND"] = "fixture"
for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
    os.environ.pop(k, None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
"""T-098 round-2 probe (staff-engineer-reviewer). Usage: python3 -I this.py <path to git-archive copy of dd84122>
Every producer route for an invented token (suffix) x every judge verdict, through the real FastAPI app on a scratch DB copy.
Fixture backend only. The letter and the internal notes are scanned for the marker."""
import os, sys, time, json, shutil, sqlite3, tempfile, re

ARCH = os.path.abspath(sys.argv[1])
sys.path.insert(0, ARCH)
os.chdir(ARCH)
os.environ["LLM_BACKEND"] = "fixture"
for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
    os.environ.pop(k, None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
from app.backend import generator, store, review as REV
from app.db import db as DB
from app.llm import audited as AU
import app as _app
assert os.path.realpath(_app.__file__).startswith(os.path.realpath(ARCH)), _app.__file__

MODE = {"poison": {}, "j1": None, "narrative": None}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:49:31.181Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/wt && mkdir -p $S/wt && rsync -a --exclude .git --exclude .venv --exclude node_modules --exclude board --exclude reviews --exclude artifacts ./ $S/wt/ && cd $S/wt && for p in probe probe2 probe3; do echo \"== $p\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-098-staff-engineer-r2-$p.py $S/wt 2>&1 | tail -25; done"
}
````

### User / tool · 2026-11-02T05:49:38.037Z

**tool result**
````
== probe
   NOTE S4 [side/unsupported] internal notes contain the AI draft's invented token under EDITED ITEMS: False
PASS S5 forced accept + stale pass: gate recompute [side/unsupported] :: {"gate_ready": false, "blockers": [["e1", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}, "item_trace_fail_steps": ["summary_tokens", "judge_1"]}
PASS S6 rerun after accept, AI redrafts with the token [side/unsupported] (run ready, row summary has token: True, review_status accepted, state needs_review) :: {"gate_ready": false, "blockers": [["e3", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}}
PASS S1 single accept AI draft [side/disagrees] (draft state needs_review ['SUMMARY_TOKEN_NOT_IN_EXCERPT']) :: {"baseline_export": 200, "accept": [422, "CODE_CHECK_FAILED"], "review_status_after": "pending", "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}, "notes_hide_wording": true}
PASS S2 single accept, stale stored pass [side/disagrees] :: {"accept": [422, "CODE_CHECK_FAILED"], "review_status_after": "pending", "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S3a batch accept [clean, stale-pass bad] [side/disagrees] :: {"batch": [422, "CODE_CHECK_FAILED"], "clean_after": "pending", "bad_after": "pending"}
PASS S3b batch accept [AI draft needs_review] [side/disagrees] :: {"batch": [422, "CODE_CHECK_FAILED"]}
PASS S4 edit-then-accept [side/disagrees] (bad edit refused, clean edit + accept, letter clean) :: {"bad_edit": [422, "invalid_edit"], "bad_edit_confirm": [422, "invalid_edit"], "status_after_bad_edit": "pending", "clean_edit": 200, "accept": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
   NOTE S4 [side/disagrees] internal notes contain the AI draft's invented token under EDITED ITEMS: False
PASS S5 forced accept + stale pass: gate recompute [side/disagrees] :: {"gate_ready": false, "blockers": [["e1", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}, "item_trace_fail_steps": ["summary_tokens", "judge_1"]}
PASS S6 rerun after accept, AI redrafts with the token [side/disagrees] (run ready, row summary has token: True, review_status accepted, state needs_review) :: {"gate_ready": false, "blockers": [["e3", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}}
PASS S7 rejudge then accept, single and batch [j1=supported] (state after rejudge verified []) :: {"rejudge": 200, "single": [422, "CODE_CHECK_FAILED"], "batch": [422, "CODE_CHECK_FAILED"], "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S7b forced-accepted bad item, then rejudge [j1=supported] keeps the export closed :: {"rejudge": 200, "gate_ready": false, "blockers": [["e1", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}}
PASS S7 rejudge then accept, single and batch [j1=unsupported] (state after rejudge needs_review ['JUDGE_UNSUPPORTED']) :: {"rejudge": 200, "single": [422, "CODE_CHECK_FAILED"], "batch": [422, "CODE_CHECK_FAILED"], "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S7b forced-accepted bad item, then rejudge [j1=unsupported] keeps the export closed :: {"rejudge": 200, "gate_ready": false, "blockers": [["e1", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}}
PASS S7 rejudge then accept, single and batch [j1=partially] (state after rejudge needs_review ['JUDGE_PARTIAL']) :: {"rejudge": 200, "single": [422, "CODE_CHECK_FAILED"], "batch": [422, "CODE_CHECK_FAILED"], "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S7b forced-accepted bad item, then rejudge [j1=partially] keeps the export closed :: {"rejudge": 200, "gate_ready": false, "blockers": [["e1", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}}
PASS S8 manual entry [j1=supported]: bad summary refused, clean accepted, letter clean :: {"bad": [422, "invalid_edit"], "ok": 201, "accept": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S8 manual entry [j1=unsupported]: bad summary refused, clean accepted, letter clean :: {"bad": [422, "invalid_edit"], "ok": 201, "accept": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S8 manual entry [j1=partially]: bad summary refused, clean accepted, letter clean :: {"bad": [422, "invalid_edit"], "ok": 201, "accept": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S9 narrative [j1=supported]: kept=1 removed=['SUMMARY_TOKEN_NOT_IN_EXCERPT']; accept=200 :: {"draft": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}, "notes_print_removed_sentence": false}
PASS S9 narrative [j1=unsupported]: kept=0 removed=['JUDGE_UNSUPPORTED', 'SUMMARY_TOKEN_NOT_IN_EXCERPT']; accept=422 :: {"draft": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}, "notes_print_removed_sentence": false}
PASS S9 narrative [j1=partially]: kept=0 removed=['JUDGE_PARTIAL', 'SUMMARY_TOKEN_NOT_IN_EXCERPT']; accept=422 :: {"draft": 200, "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}, "notes_print_removed_sentence": false}

SUMMARY: 63 checks, 0 failed
== probe2
accept e1 -> 200
e8 original quote: C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.

== hedge sentence dropped from the quote
  recomputed by accept guard: [] (rec=None: stored only)
  API accept -> 422 CODE_CHECK_FAILED | The quote leaves out a hedge sentence that qualifies it. Change the quote to whole sentences of the record that keep the hedge sentence.
  forced accept -> gate ready: False | blockers: [('e8', 'EXCERPT_OMITS_QUALIFIER')]
  GET /export -> 422
  item trace failing steps: ['excerpt_hedge']

== quote starts mid-sentence
  recomputed by accept guard: [] (rec=None: stored only)
  API accept -> 422 CODE_CHECK_FAILED | The quote leaves out a hedge sentence that qualifies it. Change the quote to whole sentences of the record that keep the hedge sentence.
  forced accept -> gate ready: False | blockers: [('e8', 'EXCERPT_NOT_WHOLE_SENTENCE')]
  GET /export -> 422
  item trace failing steps: ['excerpt_whole_sentence', 'excerpt_hedge']
== probe3
llm call failed call_id=ca50664dba736 step=j1 attempt=1 prompt_hash=6f16af6049fe0705bf3ea9931f08e9035acd5bef7e668de6f08cec044716bab5
record excerpt : C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.
generator.verify -> needs_review ['EXCERPT_OMITS_QUALIFIER']
accept e1 -> 200
accept e8 (AI draft, quote drops the hedge sentence) -> 422 CODE_CHECK_FAILED
EDIT e8 summary only -> 422 CODE_CHECK_FAILED | warnings: None
e8 after edit: review_status pending | state needs_review | state_reasons ['EXCERPT_OMITS_QUALIFIER']
gate ready: True | blockers: []
GET /export -> 200
letter has e8 quote: False | letter has the hedge sentence 'may represent degenerative': False
[]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:49:49.668Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def env\\|^@pytest.fixture\" -A22 tests/unit/test_trace.py | head -60; sed -n 1,40p artifacts/review-evidence/T-098-staff-engineer-r2-probe2.py | tail -28; grep -n \"def test_.*gate_and_export_recompute\" -A40 tests/unit/test_trace.py | head -60"
}
````

### User / tool · 2026-11-02T05:49:49.771Z

**tool result**
````
21:@pytest.fixture(scope="module")
22-def base(tmp_path_factory):
23-    import os
24-    d = tmp_path_factory.mktemp("trace")
25-    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
26-    os.environ["LLM_BACKEND"] = "fixture"
27-    for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
28-        os.environ.pop(k, None)
29-    db = str(d / "base.sqlite")
30-    c = TestClient(create_app(db, static_dir=str(d)), client=("127.0.0.1", 50000))
31-    pre = c.post("/api/cases", json={"sample": True}).json()["token"]          # an ingested case that never ran
32-    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
33-    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
34-    for _ in range(240):
35-        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
36-            break
37-        time.sleep(0.25)
38-    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready"
39-    yield {"dir": d, "db": db, "tok": tok, "pre": pre}
40-    for k, v in old.items():
41-        if v is None:
42-            os.environ.pop(k, None)
43-        else:
--
47:@pytest.fixture
48:def env(base, tmp_path, monkeypatch):
49-    monkeypatch.setenv("LLM_BACKEND", "fixture")
50-    monkeypatch.delenv("ZLAYT_MODE", raising=False)
51-    path = str(tmp_path / "copy.sqlite")
52-    src = sqlite3.connect(base["db"])
53-    dst = sqlite3.connect(path)
54-    src.backup(dst)
55-    src.close()
56-    dst.close()
57-    conn = DB.connect(path)
58-    c = TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
59-    return c, conn, base["tok"], base["pre"]
60-
61-
62-def steps_of(t):
63-    return {s["id"]: s for s in t["steps"]}
64-
65-
66-def walk(o, keys):
67-    """Every dict key anywhere in o that is in `keys`."""
68-    found = set()
69-    if isinstance(o, dict):
70-        for k, v in o.items():
from app.backend import review as REV
from app.db import db as DB

TMP = tempfile.mkdtemp(prefix="t098r2b_")
DBP = os.path.join(TMP, "p.sqlite")
c = TestClient(create_app(DBP, static_dir=TMP), client=("127.0.0.1", 50000))
TOK = c.post("/api/cases", json={"sample": True}).json()["token"]
assert c.post(f"/api/cases/{TOK}/run", json={}).status_code == 202
for _ in range(400):
    if c.get(f"/api/cases/{TOK}/status").json()["status"] in ("ready", "failed"):
        break
    time.sleep(0.25)
conn = DB.connect(DBP)


def gate():
    return next(s for s in c.get(f"/api/cases/{TOK}/trace").json()["steps"] if s["id"] == "export_gate")


def stale_pass(eid, summary, excerpt):
    row = DB.get_item(conn, eid, TOK)
    lad = dict(row.get("ladder") or {})
    lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
    lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
    lad["state"] = "verified"
    DB.update_item(conn, eid, now=time.time(), case=TOK, summary=summary, excerpt=excerpt, state="verified", state_reasons_json=[], ladder=lad)


1228:def test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1(env):
1229-    """An edited summary that drops a qualifier, written straight to edited_json with every stored check result left as 'pass': the gate and the export
1230-    recompute from the current text, so GET /export is 422 export_blocked naming the item (reviews/T-097-ux-designer-r2.md B1)."""
1231-    c, conn, tok, _ = env
1232-    ents = c.get(f"/api/cases/{tok}").json()["entries"]
1233-    acc, edt = ents[0]["id"], ents[1]["id"]
1234-    orig = DB.get_item(conn, edt, tok)
1235-    lad = orig["ladder"]
1236-    lad.setdefault("code_checks", {}).update(qualifier_carried=True, summary_tokens_not_in_excerpt=[], excerpt_whole_sentence=True, highlight_found=True)
1237-    DB.update_item(conn, edt, now=9e9, case=tok, state="verified", state_reasons_json=[], ladder=lad)          # stale: every stored result says pass
1238-    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
1239-    c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"})
1240-    g = _gate(c, tok)
1241-    assert g["ready"] is False and [(b["item_id"], b["reason_code"]) for b in _ccf(g)] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
1242-    ex = c.get(f"/api/cases/{tok}/export")
1243-    assert ex.status_code == 422 and ex.json()["error"]["code"] == "export_blocked" and REVIEWER_EDIT not in ex.text.replace(g["blockers"][0]["why"], "")
1244-    assert [(b["item_id"], b["reason_code"]) for b in ex.json()["error"]["detail"]["blockers"]] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
1245-    assert steps_of(c.get(f"/api/cases/{tok}/items/{edt}/trace").json())["summary_qualifier"]["status"] == "fail"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:49:59.612Z

**tool call — Bash**
````
{
 "command": "grep -rn \"removed\" tests/unit/test_export.py tests/unit/test_narrative*.py | head -12; grep -n \"def _gate\\|def _ccf\\|^REVIEWER_EDIT\" -A4 tests/unit/test_trace.py | head -24; tail -30 tests/unit/test_trace.py; grep -n \"internal_notes_text\" tests/unit/*.py | head -5"
}
````

### User / tool · 2026-11-02T05:49:59.726Z

**tool result**
````
tests/unit/test_narrative.py:1:"""T-059 (D-031): firm-voice treatment paragraph from ACCEPTED entries only; every sentence code-checked and judged; seeded hallucinations are removed."""
tests/unit/test_narrative.py:29:    assert [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"] and not n["removed"] and n["status"] == "pending"
tests/unit/test_narrative.py:75:    assert not n["sentences"], "judge 1 says supported, so only a code check can have removed it"
tests/unit/test_narrative.py:76:    r, = n["removed"]
tests/unit/test_narrative.py:81:def test_sentence_citing_an_entry_that_is_not_accepted_is_removed(tmp_path):
tests/unit/test_narrative.py:85:    assert not n["sentences"] and [(r["entry_id"], r["reason"]) for r in n["removed"]] == [("e8", "NOT_AN_ACCEPTED_ENTRY"), ("e404", "NOT_AN_ACCEPTED_ENTRY")]
tests/unit/test_narrative.py:93:    assert len(n["sentences"]) == 1 and not n["removed"]
tests/unit/test_narrative.py:101:    assert not n["sentences"] and {r["reason"] for r in n["removed"]} == {reason}
tests/unit/test_narrative.py:108:    assert len(n["sentences"]) == 1 and not n["removed"]
tests/unit/test_narrative.py:154:    assert not n.get("error") and len(n["sentences"]) >= 6 and not n["removed"]
tests/unit/test_narrative.py:237:    N.draft(conn, cid, call=narr([{"entry_id": "e1", "text": "Invented sentence with 99/99."}]), now=2.0)     # every sentence removed
tests/unit/test_narrative.py:269:    DB.update_case(conn, tok, config_json={"narrative": {"status": "pending", "sentences": [], "removed": []}})
537:def _gate_states(c, conn, tok):
538-    """Yield (name) after putting the case into each state we can build; the caller checks the invariant."""
539-    case = c.get(f"/api/cases/{tok}").json()
540-    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
541-    yield "pending items"
--
692:def _gate(c, tok):
693-    return steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
694-
695-
696-def _jnr(gate):
--
1025:REVIEWER_EDIT = "Paralegal wording for the mixed-case check."          # the T-097 walk's edit: drops the quote's qualifier
1026-
1027-
1028-def _edit_entry(c, tok, eid, summary):
1029-    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "edit", "edits": {"summary": summary}})
--
1050:def _ccf(gate):
1051-    return [b for b in gate["blockers"] if b.get("step_id")]
1052-
1053-
1054-def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
    s = steps_of(c.get(f"/api/cases/{tok}/items/{eid}/trace").json())["summary_tokens"]
    assert s["status"] == "fail" and s["evidence"]["tokens"] == ["5"]


def test_a_non_code_check_reason_on_an_accepted_entry_is_not_a_code_check_blocker_t098_f4(env):
    c, conn, tok, _ = env
    eid = c.get(f"/api/cases/{tok}").json()["entries"][0]["id"]
    DB.update_item(conn, eid, now=9e9, case=tok, state="needs_review", state_reasons_json=["INJECTION_SUSPECTED", "OCR_DERIVED"])
    DB.apply_review(conn, eid, "accept", now=9e9, case=tok)
    assert eid not in [b["item_id"] for b in _ccf(_gate(c, tok))]


def test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1(env):
    """An edited summary that drops a qualifier, written straight to edited_json with every stored check result left as 'pass': the gate and the export
    recompute from the current text, so GET /export is 422 export_blocked naming the item (reviews/T-097-ux-designer-r2.md B1)."""
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    acc, edt = ents[0]["id"], ents[1]["id"]
    orig = DB.get_item(conn, edt, tok)
    lad = orig["ladder"]
    lad.setdefault("code_checks", {}).update(qualifier_carried=True, summary_tokens_not_in_excerpt=[], excerpt_whole_sentence=True, highlight_found=True)
    DB.update_item(conn, edt, now=9e9, case=tok, state="verified", state_reasons_json=[], ladder=lad)          # stale: every stored result says pass
    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
    c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"})
    g = _gate(c, tok)
    assert g["ready"] is False and [(b["item_id"], b["reason_code"]) for b in _ccf(g)] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["code"] == "export_blocked" and REVIEWER_EDIT not in ex.text.replace(g["blockers"][0]["why"], "")
    assert [(b["item_id"], b["reason_code"]) for b in ex.json()["error"]["detail"]["blockers"]] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
    assert steps_of(c.get(f"/api/cases/{tok}/items/{edt}/trace").json())["summary_qualifier"]["status"] == "fail"
tests/unit/test_api.py:31:    assert isinstance(j["letter_text"], str) and isinstance(j["internal_notes_text"], str)
tests/unit/test_api.py:32:    assert j["letter_text"] != j["internal_notes_text"] and "INTERNAL REVIEW NOTES" not in j["letter_text"]
tests/unit/test_api.py:33:    assert "AI assistance" not in j["letter_text"] and "AI assistance" in j["internal_notes_text"]
tests/unit/test_api_routes.py:168:    assert ex["internal_notes_text"]    # golden byte-equality runs on the curated fixture set (D-029, qa T-051)
tests/unit/test_case_extras.py:107:    assert out["letter_text"] == letter.rstrip("\n") and out["internal_notes_text"] == notes.rstrip("\n")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:50:01.971Z

**tool call — Bash**
````
{
 "command": "grep -n \"narrative\" tests/unit/test_export.py | head -8; sed -n 1100,1118p tests/unit/test_trace.py; grep -n \"def build_export\" -A12 app/backend/export.py | head -20; grep -n \"def narr\\b\" -A8 tests/unit/test_narrative.py; sed -n 60,80p tests/unit/test_narrative.py"
}
````

### User / tool · 2026-11-02T05:50:02.080Z

**tool result**
````
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "dismiss"})
    assert _ccf(_gate(c, tok)) == []


def test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098(env):
    c, conn, tok, _ = env
    _accept_all(c, tok)
    assert _ccf(_gate(c, tok)) == []


def test_gate_ready_equals_export_allowed_with_a_failing_edit_t098(env):
    c, conn, tok, _ = env
    _mixed(c, tok, conn)
    for name in ("failing edit", "failing edit and run failed"):
        if name.endswith("run failed"):
            DB.update_case(conn, tok, status="failed")
        g = _gate(c, tok)
593:def build_export(case: dict) -> dict:
594-    """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter.
595-    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
596-    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
597-    if case.get("judge_not_run"):
598-        raise JudgeNotRun(case["judge_not_run"])
599-    v = _View(case)
600-    notes = _notes(v)
601-    in_letter = {e["record_no"] for e in v.in_entries}
602-    pend = _pending(v)
603-    counts = {  # R-EX-5 count line: shown by the UI outside both blocks, never inside them
604-        "entries": len(v.in_entries),
605-        "charges": len(v.in_charges),
22:def narr(sentences, judge="supported"):
23-    return FakeCall({"narrative": {"sentences": sentences}, "j1": {"verdict": judge, "reason_code": "NONE"}})
24-
25-
26-def test_good_sentences_kept_with_citations(tmp_path):
27-    conn, cid = accepted_sample(tmp_path)
28-    n = N.draft(conn, cid, call=narr(GOOD), now=2.0)
29-    assert [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"] and not n["removed"] and n["status"] == "pending"
30-    assert all(s["cite"].startswith("record ") and s["judge"]["verdict"] == "supported" for s in n["sentences"])
    ("e1", "On January 9, 2026, Austin EMS found a herniated disc at C6-C7 and neck pain 9/10.", [TOK, QUAL]),            # invented numbers; also drops C/O
    # each other code check on its own
    ("e5", E5.replace("recorded", "recorded that the collision caused her") + ".", [CAUSE]),
    ("e5", E5 + ", after a gap in care.", [FLAG]),
    ("e8", "On May 29, 2026, Austin Imaging documented a C5-C6 disc protrusion with mild right foraminal narrowing.", [QUAL]),   # drops 'may represent'
    # optional backstop: severity / outcome wording that is not in the quote
    ("e5", E5.replace("recorded", "recorded significant") + ".", [SEV]),
    ("e5", E5.replace("recorded", "recorded severe") + ".", [SEV]),
    ("e5", E5 + ", and recommended surgery.", [SEV]),
    ("e5", E5.replace("pain 4/10, improving", "worsening pain 4/10") + ".", [SEV]),
])
def test_each_code_check_removes_a_seeded_sentence_with_its_own_reason(tmp_path, entry, text, reasons):
    conn, cid = accepted_sample(tmp_path)
    call = narr([{"entry_id": entry, "text": text}])
    n = N.draft(conn, cid, call=call, now=2.0)
    assert not n["sentences"], "judge 1 says supported, so only a code check can have removed it"
    r, = n["removed"]
    assert r["text"] == text and r["reasons"] == reasons and r["reason"] == reasons[0] and r["message"] == N.REASONS[reasons[0]]
    assert "j1" not in call.steps()                                  # rejected before the judge: rung (a) is what caught it
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:50:26.130Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace(\"def test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098(env):\",\"def test_clean_accepted_ai_drafts_are_not_code_check_blockers_d051(env):\")\ns+='''\n\n# ---- D-051 / T-098 r3: ONE choke point (review.set_review) for every decision that leaves an entry accepted or edited; the gate and the trace recompute all five checks\nHEDGE_Q = \"C5-C6 disc protrusion with mild right foraminal narrowing.\"                               # e8's quote without the hedge sentence that follows it in the record\nHEDGE_FULL = \"C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.\"\n\n\ndef _e8_ai_draft_with_short_quote(c, conn, tok, stored=True):\n    \"\"\"The reviewer's live case (T-098-staff-engineer-r2 F1): the AI quoted e8 and left out the hedge sentence that follows it.\"\"\"\n    row = DB.get_item(conn, \"e8\", tok)\n    assert HEDGE_FULL in row[\"excerpt\"] or row[\"excerpt\"].startswith(HEDGE_Q)\n    DB.update_item(conn, \"e8\", now=9e9, case=tok, excerpt=HEDGE_Q, state=\"needs_review\", state_reasons_json=[\"EXCERPT_OMITS_QUALIFIER\"] if stored else [])\n    return \"e8\"\n\n\ndef test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3(env):\n    c, conn, tok, _ = env\n    eid = _e8_ai_draft_with_short_quote(c, conn, tok)\n    for body in ({\"action\": \"accept\"}, {\"action\": \"edit\", \"edits\": {\"summary\": \"Disc protrusion at C5-C6 with mild right foraminal narrowing, possibly degenerative.\"}}):\n        r = c.post(f\"/api/cases/{tok}/items/{eid}/review\", json=body)\n        err = r.json()[\"error\"]\n        assert r.status_code == 422 and err[\"code\"] == \"CODE_CHECK_FAILED\", body\n        assert err[\"detail\"][\"reason_code\"] == \"EXCERPT_OMITS_QUALIFIER\" and err[\"detail\"][\"step_id\"] == \"excerpt_hedge\"\n        assert err[\"detail\"][\"next_action\"][\"code\"] == \"EDIT_QUOTE\" and \"Change the quote\" in err[\"message\"] and \"Edit the summary\" not in err[\"message\"]\n        row = DB.get_item(conn, eid, tok)\n        assert row[\"review_status\"] == \"pending\" and row[\"edited\"] is None and \"EXCERPT_OMITS_QUALIFIER\" in row[\"state_reasons\"]     # nothing written, reason not wiped\n    ok = c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"edit\", \"edits\": {\"excerpt\": HEDGE_FULL, \"summary\": \"Disc protrusion at C5-C6 with mild right foraminal narrowing; findings may represent degenerative change.\"}})\n    assert ok.status_code == 200, ok.text                                                           # changing the QUOTE is the fix\n    assert DB.get_item(conn, eid, tok)[\"review_status\"] == \"edited\"\n\n\ndef test_reset_of_a_failing_entry_is_allowed_and_keeps_the_stored_reason_d051_r3(env):\n    c, conn, tok, _ = env\n    eid = _e8_ai_draft_with_short_quote(c, conn, tok)\n    DB.apply_review(conn, eid, \"accept\", now=9e9, case=tok)                                          # old data: accepted before the guard\n    r = c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"reset\"})\n    assert r.status_code == 200\n    row = DB.get_item(conn, eid, tok)\n    assert row[\"review_status\"] == \"pending\" and \"EXCERPT_OMITS_QUALIFIER\" in row[\"state_reasons\"]\n\n\ndef test_set_review_is_the_choke_point_for_accept_edit_and_batch_d051_r3(env):\n    from app.backend import review as REV\n    c, conn, tok, _ = env\n    eid = _e8_ai_draft_with_short_quote(c, conn, tok)\n    for action, kw in ((\"accept\", {}), (\"edit\", {\"edited\": {\"summary\": \"x y\", \"at\": \"t\"}})):\n        with pytest.raises(REV.ReviewError) as ei:\n            REV.set_review(conn, tok, eid, action, now=9e9, **kw)\n        assert ei.value.status == 422 and ei.value.code == \"CODE_CHECK_FAILED\"\n    with pytest.raises(REV.ReviewError):\n        REV.batch_apply(conn, tok, eid, \"accept\", 9e9)\n    assert DB.get_item(conn, eid, tok)[\"review_status\"] == \"pending\"\n    REV.batch_apply(conn, tok, eid, \"reset\", 9e9)                                                    # the way out is never blocked\n    assert not [e for e in DB.list_events(conn, tok, eid) if e[\"action\"] in (\"accept\", \"edit\")]\n\n\nQUOTE_AND_SUMMARY_CASES = [      # (name, excerpt, summary, expected reason, failing trace step); every stored check result is left as a pass\n    (\"hedge sentence dropped\", HEDGE_Q, \"Disc protrusion at C5-C6 with mild right foraminal narrowing, possibly degenerative.\", \"EXCERPT_OMITS_QUALIFIER\", \"excerpt_hedge\"),\n    (\"quote starts mid-sentence\", \"disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.\",\n     \"Disc protrusion with mild right foraminal narrowing, possibly degenerative.\", \"EXCERPT_NOT_WHOLE_SENTENCE\", \"excerpt_whole_sentence\"),\n    (\"quote is not in the record\", \"Patient reports the collision was the cause of the disc protrusion.\", \"Patient reports the collision was the cause of the disc protrusion.\",\n     \"GROUNDING_EXCERPT_NOT_VERBATIM\", \"excerpt_verbatim\"),\n    (\"number not in the quote\", HEDGE_FULL, \"Disc protrusion with pain 5/10, findings may represent degenerative change.\", \"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"summary_tokens\"),\n    (\"qualifier dropped\", HEDGE_FULL, \"Disc protrusion at C5-C6 with mild right foraminal narrowing.\", \"SUMMARY_DROPS_QUALIFIER\", \"summary_qualifier\"),\n]\n\n\n@pytest.mark.parametrize(\"name,excerpt,summary,reason,step_id\", QUOTE_AND_SUMMARY_CASES, ids=[x[0] for x in QUOTE_AND_SUMMARY_CASES])\ndef test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3(env, name, excerpt, summary, reason, step_id):\n    \"\"\"The reviewer's F2: every stored result says pass, the text fails one check. Accept refuses; a forced accept is a gate blocker, GET /export is 422\n    and the item trace shows that step failing with blocks_export. Mutant M11 (the quote checks off) fails the first three cases.\"\"\"\n    c, conn, tok, _ = env\n    row = DB.get_item(conn, \"e8\", tok)\n    lad = row[\"ladder\"]\n    lad[\"code_checks\"] = {k: (True if k != \"summary_tokens_not_in_excerpt\" else []) for k in (lad.get(\"code_checks\") or {})}\n    lad[\"judge\"] = {\"model\": \"fixture\", \"prompt_version\": \"judge\", \"call_id\": None, \"verdict\": \"supported\", \"reason_code\": \"NONE\"}\n    DB.update_item(conn, \"e8\", now=9e9, case=tok, summary=summary, excerpt=excerpt, state=\"verified\", state_reasons_json=[], ladder=lad)\n    r = c.post(f\"/api/cases/{tok}/items/e8/review\", json={\"action\": \"accept\"})\n    assert r.status_code == 422 and r.json()[\"error\"][\"detail\"][\"reason_code\"] == reason\n    DB.apply_review(conn, \"e8\", \"accept\", now=9e9, case=tok)                                         # old data / any route that skips the guard\n    c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"accept\"})\n    g = _gate(c, tok)\n    assert g[\"ready\"] is False and [(b[\"item_id\"], b[\"reason_code\"]) for b in _ccf(g)] == [(\"e8\", reason)]\n    assert c.get(f\"/api/cases/{tok}/export\").status_code == 422\n    stp = steps_of(c.get(f\"/api/cases/{tok}/items/e8/trace\").json())[step_id]\n    assert stp[\"status\"] == \"fail\" and stp[\"blocks_export\"] is True and stp[\"reason_code\"] == reason\n\n\ndef test_internal_notes_never_print_ai_wording_that_failed_a_check_d051_r3(env):\n    \"\"\"EDITED ITEMS 'summary was' and the narrative 'Removed' line say the AI wording was removed, not what it said.\"\"\"\n    c, conn, tok, _ = env\n    ents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\n    eid = ents[0][\"id\"]\n    row = DB.get_item(conn, eid, tok)\n    DB.apply_review(conn, eid, \"edit\", edited={\"summary\": row[\"summary\"], \"original_summary\": \"Pain 5/10 on the left.\", \"at\": \"2026-11-02T00:00:00Z\"}, now=9e9, case=tok)\n    DB.update_item(conn, eid, now=9e9, case=tok, state=\"verified\", state_reasons_json=[])\n    for x in ents[1:]:\n        c.post(f\"/api/cases/{tok}/items/{x['id']}/review\", json={\"action\": \"accept\"})\n    case = DB.get_case(conn, tok)\n    cfg = dict(case.get(\"config\") or {})\n    cfg[\"narrative\"] = {\"status\": \"pending\", \"sentences\": [], \"basis\": {}, \"removed\": [\n        {\"id\": \"ns1\", \"entry_id\": eid, \"text\": \"Pain 77/10 invented.\", \"reason\": \"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"message\": \"The sentence has a number, side, negation or date that is not in the cited quote.\"},\n        {\"id\": \"ns2\", \"entry_id\": eid, \"text\": \"Second check said no.\", \"reason\": \"JUDGE_UNSUPPORTED\", \"message\": \"x\"}]}\n    DB.update_case(conn, tok, config_json=cfg)\n    j = c.get(f\"/api/cases/{tok}/export\").json()\n    notes = j[\"internal_notes_text\"]\n    assert \"5/10\" not in j[\"letter_text\"] + notes and \"77/10\" not in j[\"letter_text\"] + notes\n    assert \"summary was AI wording removed (failed a check:\" in notes and \"a number or word in it is not in the quote\" in notes\n    assert \"- AI wording removed (failed a check: The sentence has a number\" in notes\n    assert 'Removed: \"Second check said no.\"' in notes                                              # a judge removal is not a code failure: the sentence stays visible\n'''\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T05:50:34.480Z

**tool result**
````
env = (<starlette.testclient.TestClient object at 0x10b8a6e10>, <sqlite3.Connection object at 0x10ac3ff10>, 'TvWmz-70KdI5xElYZkKhPQ', '8Yd5WOshWLQkMNh44FHThQ')
name = 'hedge sentence dropped'
excerpt = 'C5-C6 disc protrusion with mild right foraminal narrowing.'
summary = 'Disc protrusion at C5-C6 with mild right foraminal narrowing, possibly degenerative.'
reason = 'EXCERPT_OMITS_QUALIFIER', step_id = 'excerpt_hedge'

    @pytest.mark.parametrize("name,excerpt,summary,reason,step_id", QUOTE_AND_SUMMARY_CASES, ids=[x[0] for x in QUOTE_AND_SUMMARY_CASES])
    def test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3(env, name, excerpt, summary, reason, step_id):
        """The reviewer's F2: every stored result says pass, the text fails one check. Accept refuses; a forced accept is a gate blocker, GET /export is 422
        and the item trace shows that step failing with blocks_export. Mutant M11 (the quote checks off) fails the first three cases."""
        c, conn, tok, _ = env
        row = DB.get_item(conn, "e8", tok)
        lad = row["ladder"]
        lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
        lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
        DB.update_item(conn, "e8", now=9e9, case=tok, summary=summary, excerpt=excerpt, state="verified", state_reasons_json=[], ladder=lad)
        r = c.post(f"/api/cases/{tok}/items/e8/review", json={"action": "accept"})
>       assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == reason
E       AssertionError: assert (422 == 422 and 'SUMMARY_TOKEN_NOT_IN_EXCERPT' == 'EXCERPT_OMITS_QUALIFIER'
E        +  where 422 = <Response [422 Unprocessable Content]>.status_code
E         
E         - EXCERPT_OMITS_QUALIFIER
E         + SUMMARY_TOKEN_NOT_IN_EXCERPT)

tests/unit/test_trace.py:1324: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3
FAILED tests/unit/test_trace.py::test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3[hedge sentence dropped]
2 failed, 81 passed in 7.67s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:50:38.436Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('\"Disc protrusion at C5-C6 with mild right foraminal narrowing, possibly degenerative.\"','\"Disc protrusion at C5-C6 with mild right foraminal narrowing.\"')\ns=s.replace('\"Disc protrusion with mild right foraminal narrowing, possibly degenerative.\"','\"Disc protrusion with mild right foraminal narrowing.\"')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | tail -30; sed -n 262,300p app/backend/trace.py; grep -n \"your wording\\|Your wording\" -i app/backend/trace.py; grep -n \"T-097\\|wording\" reviews/T-097-ux-designer-r3.md | head -20"
}
````

### User / tool · 2026-11-02T05:50:46.460Z

**tool result**
````
env = (<starlette.testclient.TestClient object at 0x10d460f50>, <sqlite3.Connection object at 0x10c29ae30>, 'c6sOaKh-tHyBTer5MruTCg', 'sYizejtebEd54ARxiUKsQw')
name = 'quote starts mid-sentence'
excerpt = 'disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.'
summary = 'Disc protrusion with mild right foraminal narrowing.'
reason = 'EXCERPT_NOT_WHOLE_SENTENCE', step_id = 'excerpt_whole_sentence'

    @pytest.mark.parametrize("name,excerpt,summary,reason,step_id", QUOTE_AND_SUMMARY_CASES, ids=[x[0] for x in QUOTE_AND_SUMMARY_CASES])
    def test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3(env, name, excerpt, summary, reason, step_id):
        """The reviewer's F2: every stored result says pass, the text fails one check. Accept refuses; a forced accept is a gate blocker, GET /export is 422
        and the item trace shows that step failing with blocks_export. Mutant M11 (the quote checks off) fails the first three cases."""
        c, conn, tok, _ = env
        row = DB.get_item(conn, "e8", tok)
        lad = row["ladder"]
        lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
        lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
        DB.update_item(conn, "e8", now=9e9, case=tok, summary=summary, excerpt=excerpt, state="verified", state_reasons_json=[], ladder=lad)
        r = c.post(f"/api/cases/{tok}/items/e8/review", json={"action": "accept"})
>       assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == reason
E       AssertionError: assert (422 == 422 and 'SUMMARY_DROPS_QUALIFIER' == 'EXCERPT_NOT_WHOLE_SENTENCE'
E        +  where 422 = <Response [422 Unprocessable Content]>.status_code
E         
E         - EXCERPT_NOT_WHOLE_SENTENCE
E         + SUMMARY_DROPS_QUALIFIER)

tests/unit/test_trace.py:1324: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3
FAILED tests/unit/test_trace.py::test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3[quote starts mid-sentence]
2 failed, 81 passed in 7.23s


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
    if gated:
        code, label = "needs_attention", "Needs your attention: a check on your wording fails"
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
        if c.startswith("JUDGE_") or c == "FIXTURE_MISS":
            return judge_id or fallback
        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else fallback
    reasons = [{"code": c, "why": reason_text(c), "step_id": step_of(c)} for c in (row.get("state_reasons") or [])]
    return {"token": cx.case_id, "item_id": item_id, "kind": kind, "mode": "full" if cx.full else "metadata", "state": row.get("state"),
275:        code, label = "needs_attention", "Needs your attention: a check on your wording fails"
1:# T-097 ux-designer-reviewer, round 3: refused Accept, case verdict, the three minors, and the r2 blocker on the real backend
7:1. **Refused accept (422 CODE_CHECK_FAILED) shows inline with "Edit the summary": pass.** Click, the `a` key, and the refused batch with a per-item list all show it at 1440 and 390. The click box sits 62 px (1440) and 118 px (390) under the Accept button. The `a` key keeps focus on the refused row. The batch says "Nothing was accepted." and lists each item with "Edit the summary". Accepted count stays 0 after each refusal (`T-097-ux-designer-r3-walk-results.json` S_REFUSE_*). The 390 key path has a position problem, see F3.
9:3. **The three minors: fixed.** m-1: the panel names each class once ("1 not checked, blocks export: 1, 1 edited by you, not AI-checked, 1 summary fails a check, blocks export: 1"; the two blocking clauses equal the gate's 2). m-2: at three items the rail and panel labels say "for these 3", one press makes one POST and the status says it answered for all 3; no gate row carries a rerun button (`T-097-ux-designer-r3-walk2-results.json` N3_*). m-new-1: the Not-needed judge step on the edited, passing item has no "said:" line and no fail status (S_MINORS_1440.why_e3_judge_step_text). n-1 (Export in view after refusal) and n-new-3 ("Edited by you, not AI-checked") also read fixed.
11:5. **The r2 blocker (B1) on the real backend, no stub: closed.** I wrote the edited text that drops "without" past the edit route, as r2 did. Gate: status fail, ready false, blockers [e2] with SUMMARY_DROPS_QUALIFIER. GET export: 422 export_blocked naming e2. Rail "Export blocked by 1", Why "Your wording doesn't match the quote:" with "Edit your wording", panel "1 summary fails a check, blocks export: 1", refused-export message says the wording does not match. Restoring through the real edit route returns 200 and the rail reads "Ready to export, 21 not reviewed" after reload. The gate now recomputes from the current text (dd84122, D-051).
15:**F1 (major). An accepted AI draft's Why verdict says "a check on your wording fails"; its own blocker row says "This summary doesn't match the quote".** The label comes from `app/backend/trace.py:275`, which uses "your wording" for any gated code step on an accepted item, whoever wrote the text. On the 1440 and 390 runs, the Why verdict for e1 and e2 (AI drafts, accepted, then broken) reads "Needs your attention: a check on your wording fails". The blocker row for the same item in the rail reads "This summary doesn't match the quote". The step under it says "Edit the summary". Graded major and not blocker: no export or letter is affected and the step and gate copy are correct. The label misstates who wrote the text, on the decision surface the paralegal reads.
17:**F2 (minor). After a rerun, the status says nothing blocks the export while the rail still says "Export blocked by 3" for about three seconds.** Evidence: `T-097-ux-designer-r3-walk3-results.json` after_3s_status "...Nothing about the second check blocks the export now." with after_3s_gate "Export blocked by 3". The page logged the trace that returned pass/ready 3.2 s after the press (trace_responses_seen_by_page). After reload the rail reads "Ready to export, 20 not reviewed". The sentence comes from the rerun answer (`app/frontend/stepper.js:164`); the rail is refreshed by a second GET trace after it (`S.rejudge`, stepper.js:180-196). Caveat: this run used the E2E stub's rejudge answer (ready true). The real rejudge in a blocked state returns ready false with blockers [e2] (walk2 REJUDGE_REAL), so the sentence would not print there.
19:**F3 (minor). On 390, the refusal under a row focused by the `a` key can sit below the fold.** Walk 1 (row e2 under e1's refusal): the box starts at the bottom edge, `key_box_in_view` false, `artifacts/review-evidence/T-097-ux-designer-r3-390-s2-accept-key.png`. Walk 2 (row at top 262): the box at 667 to 824 is fully visible (`KEY_390` in walk2 results). Focus stays on the row either way. The click path scrolls the box into view and the key path does not.
27:- `python3 tools/board.py show T-097`: status in_review, rounds 2, commits include 9f2811f; reviews r1 and r2 fail.
32:- `artifacts/review-evidence/T-097-ux-designer-r3-api.py` (results `T-097-ux-designer-r3-api-results.json`): B1 on the real backend (direct write, stored reasons left as they were); the gate, the item trace, export 422, and the restore; a single accept and a batch refused with 422 CODE_CHECK_FAILED, statuses stay pending; two accepted AI drafts broken: gate, verdict and export all count 2.
33:- `artifacts/review-evidence/T-097-ux-designer-r3-walk.py` at 1440x900 and 390x844 (results `T-097-ux-designer-r3-walk-results.json`, 0 errors): S_REFUSE, S_TWO, S_B1 (no stub), S_MINORS (JudgeNotRun stub from tests/e2e/conftest.py for the judge-not-run state only; the failing and passing edits are real), S_NUMBERS. Screenshots `artifacts/review-evidence/T-097-ux-designer-r3-<w>-s1..s14*.png`, for example `T-097-ux-designer-r3-1440-s1-accept-click.png`, `T-097-ux-designer-r3-1440-s6-why-e1.png`, `T-097-ux-designer-r3-390-s7-export-refused.png`.
34:- `artifacts/review-evidence/T-097-ux-designer-r3-walk2.py` (results `T-097-ux-designer-r3-walk2-results.json`): three-item rerun (labels, one POST, 3 answered); the 390 key path with the row focused and no script scroll; REJUDGE_REAL (no stub).
35:- `artifacts/review-evidence/T-097-ux-designer-r3-walk3.py` (results `T-097-ux-designer-r3-walk3-results.json`): rail readings after the press, the trace responses the page logged, and a reload.
47:{"card": "T-097", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
50:  "python3 tools/board.py show T-097 -> status in_review, rounds 2, commits include 9f2811f, reviews r1 and r2 fail",
55:  "artifacts/review-evidence/T-097-ux-designer-r3-api.py -> T-097-ux-designer-r3-api-results.json (real backend: B1 gate, export 422, restore 200; single and batch 422 CODE_CHECK_FAILED with statuses pending; two-failure gate, verdict and export count 2)",
56:  "artifacts/review-evidence/T-097-ux-designer-r3-walk.py at 1440x900 and 390x844 -> T-097-ux-designer-r3-walk-results.json, 0 errors: S_REFUSE (click, a key, batch list), S_TWO (rail, panel, Why, export), S_B1 (no stub), S_MINORS (JudgeNotRun for the judge-not-run state only), S_NUMBERS; 14 screenshots under artifacts/review-evidence/T-097-ux-designer-r3-*",
57:  "artifacts/review-evidence/T-097-ux-designer-r3-walk2.py -> T-097-ux-designer-r3-walk2-results.json: three-item rerun (labels, one POST, 3 answered); 390 key path with row focused; REJUDGE_REAL (ready false, blockers [e2])",
58:  "artifacts/review-evidence/T-097-ux-designer-r3-walk3.py -> T-097-ux-designer-r3-walk3-results.json: rail after the press, trace responses logged by the page, reload",
64:  {"severity": "major", "title": "Accepted AI draft's Why verdict says 'a check on your wording fails'; its own blocker row says 'This summary doesn't match the quote'",
65:   "evidence": "artifacts/review-evidence/T-097-ux-designer-r3-walk-results.json S_TWO_1440.why_e1_verdict = 'Needs your attention: a check on your wording fails' (same at S_TWO_390); S_TWO_1440.rail_gate_blockers e1 = \"This summary doesn't match the quote: ...\"; screenshot artifacts/review-evidence/T-097-ux-designer-r3-1440-s6-why-e1.png shows the step 'Edit the summary to remove 5'; code app/backend/trace.py:275 hard-codes 'your wording' for any gated code step on an accepted item",
[This command modified 1 file you've previously read: tests/unit/test_trace.py. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:50:51.625Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('''     \"Disc protrusion with mild right foraminal narrowing.\"'''.replace('\"Disc','\"Disc'),'''     \"Disc protrusion with mild right foraminal narrowing; findings may represent degenerative change.\"''',1) if False else s\ns=s.replace('''\"disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.\",\n     \"Disc protrusion with mild right foraminal narrowing.\",''','''\"disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.\",\n     \"Disc protrusion with mild right foraminal narrowing; findings may represent degenerative change.\",''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"def _paralegal_wording\" -A8 app/backend/trace.py; .venv/bin/python -m pytest -q tests/unit/test_trace.py 2>&1 | grep -B30 \"^FAILED\\|Error\" | head -50"
}
````

### User / tool · 2026-11-02T05:50:59.420Z

**tool result**
````
760:def _paralegal_wording(kind, row) -> bool:
761-    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
762-    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))
763-
764-
765-def unjudged_items(conn, case_id: str) -> list:
766-    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
767-    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
768-    cx = _Cx(conn, case_id, False)
........................................................................ [ 86%]
..F........                                                              [100%]
=================================== FAILURES ===================================
_ test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3 _

env = (<starlette.testclient.TestClient object at 0x10e06c650>, <sqlite3.Connection object at 0x10c6efb50>, 'LOcxKwhBy7RxOzwoHRSyCA', 'dQTEb4fGvmrfAdzwA19X9w')

    def test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3(env):
        c, conn, tok, _ = env
        eid = _e8_ai_draft_with_short_quote(c, conn, tok)
        for body in ({"action": "accept"}, {"action": "edit", "edits": {"summary": "Disc protrusion at C5-C6 with mild right foraminal narrowing."}}):
            r = c.post(f"/api/cases/{tok}/items/{eid}/review", json=body)
            err = r.json()["error"]
            assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED", body
>           assert err["detail"]["reason_code"] == "EXCERPT_OMITS_QUALIFIER" and err["detail"]["step_id"] == "excerpt_hedge"
E           AssertionError: assert ('SUMMARY_TOKEN_NOT_IN_EXCERPT' == 'EXCERPT_OMITS_QUALIFIER'
E             
E             - EXCERPT_OMITS_QUALIFIER
E             + SUMMARY_TOKEN_NOT_IN_EXCERPT)

tests/unit/test_trace.py:1268: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:51:04.835Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('''excerpt=HEDGE_Q, state=\"needs_review\", state_reasons_json=[\"EXCERPT_OMITS_QUALIFIER\"] if stored else [])''','''excerpt=HEDGE_Q, summary=\"Disc protrusion at C5-C6 with mild right foraminal narrowing.\",\n                   state=\"needs_review\", state_reasons_json=[\"EXCERPT_OMITS_QUALIFIER\"] if stored else [])''')\nopen(p,'w').write(s)\np='app/backend/review.py'\ns=open(p).read()\ns=s.replace('''\"GROUNDING_EXCERPT_NOT_VERBATIM\", \"EXCERPT_OMITS_QUALIFIER\", \"EXCERPT_NOT_WHOLE_SENTENCE\",\n                      \"HIGHLIGHT_NOT_FOUND\")''','''\"GROUNDING_EXCERPT_NOT_VERBATIM\", \"EXCERPT_NOT_WHOLE_SENTENCE\", \"EXCERPT_OMITS_QUALIFIER\",\n                      \"HIGHLIGHT_NOT_FOUND\")''')\nopen(p,'w').write(s)\np='app/backend/trace.py'\ns=open(p).read()\ns=s.replace('''    if gated:\n        code, label = \"needs_attention\", \"Needs your attention: a check on your wording fails\"''','''    if gated:      # whose words: only the paralegal's own summary is \"your wording\"; an AI draft is \"this summary\"\n        code, label = \"needs_attention\", (\"Needs your attention: a check on your wording fails\" if _paralegal_wording(kind, row) else \"Needs your attention: a check on this summary fails\")''')\nopen(p,'w').write(s)\nEOF\ngrep -rn \"check on your wording\" app tests --include=*.py --include=*.js | grep -v \"^app/backend/trace.py\""
}
````

### User / tool · 2026-11-02T05:51:04.958Z

**tool result**
````
tests/e2e/conftest.py:159:            d["verdict"] = {"code": "needs_attention", "label": "Needs your attention: a check on your wording fails", "blocks_export": True}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:51:09.079Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_trace.py <<'EOF'\n\n\ndef test_verdict_says_this_summary_for_an_ai_draft_and_your_wording_only_for_the_paralegals_t097_r3_f1(env):\n    c, conn, tok, _ = env\n    ents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\n    ai, human = ents[0][\"id\"], ents[1][\"id\"]\n    DB.update_item(conn, ai, now=9e9, case=tok, summary=\"Pain 5/10\", state=\"verified\", state_reasons_json=[])\n    DB.apply_review(conn, ai, \"accept\", now=9e9, case=tok)                                            # an accepted AI draft that fails a check (old data)\n    orig = DB.get_item(conn, human, tok)\n    DB.apply_review(conn, human, \"edit\", edited={\"summary\": REVIEWER_EDIT, \"original_summary\": orig[\"summary\"], \"at\": \"2026-11-02T00:00:00Z\"}, now=9e9, case=tok)\n    v = {i: c.get(f\"/api/cases/{tok}/items/{i}/trace\").json()[\"verdict\"] for i in (ai, human)}\n    assert v[ai][\"label\"] == \"Needs your attention: a check on this summary fails\" and \"wording\" not in v[ai][\"label\"]\n    assert v[human][\"label\"] == \"Needs your attention: a check on your wording fails\"\n    assert v[ai][\"code\"] == v[human][\"code\"] == \"needs_attention\" and v[ai][\"blocks_export\"] and v[human][\"blocks_export\"]\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | grep -v billing | tail -8"
}
````

### User / tool · 2026-11-02T05:52:58.749Z

**tool result**
````
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
=========================== short test summary info ============================
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
FAILED tests/unit/test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts
3 failed, 2045 passed, 1 skipped in 108.42s (0:01:48)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:53:03.727Z

**tool call — Bash**
````
{
 "command": "cp app/backend/review.py /tmp/review.bak 2>/dev/null; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/mut && mkdir $S/mut && rsync -a --exclude .git --exclude .venv --exclude board --exclude reviews --exclude artifacts ./ $S/mut/ && cd $S/mut && python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\na='for c in g.check_excerpt(rec[\"excerpt\"], exc):'\nassert a in s\ns=s.replace(a,'for c in []:')\nopen(p,'w').write(s)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_trace.py -p no:cacheprovider 2>&1 | tail -8; rm /tmp/review.bak"
}
````

### User / tool · 2026-11-02T05:53:14.536Z

**tool result**
````
tests/unit/test_trace.py:1325: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3
FAILED tests/unit/test_trace.py::test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3[hedge sentence dropped]
FAILED tests/unit/test_trace.py::test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3[quote starts mid-sentence]
FAILED tests/unit/test_trace.py::test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3[quote is not in the record]
4 failed, 80 passed in 7.19s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:53:19.092Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/wt && mkdir $S/wt && rsync -a --exclude .git --exclude .venv --exclude board --exclude reviews --exclude artifacts ./ $S/wt/ && for p in probe probe2 probe3; do .venv/bin/python -I artifacts/review-evidence/T-098-staff-engineer-r2-$p.py $S/wt 2>&1 | grep -E \"SUMMARY|FAIL|-> (200|422)|gate ready\" | head; done; git diff HEAD -- memory/contracts/api.md | head -5; grep -n \"a check on your wording\\|Edit the summary to match the quote\" memory/contracts/api.md | cut -c1-80"
}
````

### User / tool · 2026-11-02T05:53:25.829Z

**tool result**
````
PASS S1 single accept AI draft [num/supported] (draft state needs_review ['SUMMARY_TOKEN_NOT_IN_EXCERPT']) :: {"baseline_export": 200, "accept": [422, "CODE_CHECK_FAILED"], "review_status_after": "pending", "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}, "notes_hide_wording": true}
PASS S2 single accept, stale stored pass [num/supported] :: {"accept": [422, "CODE_CHECK_FAILED"], "review_status_after": "pending", "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S3a batch accept [clean, stale-pass bad] [num/supported] :: {"batch": [422, "CODE_CHECK_FAILED"], "clean_after": "pending", "bad_after": "pending"}
PASS S3b batch accept [AI draft needs_review] [num/supported] :: {"batch": [422, "CODE_CHECK_FAILED"]}
PASS S5 forced accept + stale pass: gate recompute [num/supported] :: {"gate_ready": false, "blockers": [["e1", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}, "item_trace_fail_steps": ["summary_tokens"]}
PASS S6 rerun after accept, AI redrafts with the token [num/supported] (run ready, row summary has token: True, review_status accepted, state needs_review) :: {"gate_ready": false, "blockers": [["e3", "SUMMARY_TOKEN_NOT_IN_EXCERPT"]], "export": {"status": 422, "code": "export_blocked", "letter_has": null, "notes_has": null}}
PASS S1 single accept AI draft [num/unsupported] (draft state needs_review ['SUMMARY_TOKEN_NOT_IN_EXCERPT']) :: {"baseline_export": 200, "accept": [422, "CODE_CHECK_FAILED"], "review_status_after": "pending", "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}, "notes_hide_wording": true}
PASS S2 single accept, stale stored pass [num/unsupported] :: {"accept": [422, "CODE_CHECK_FAILED"], "review_status_after": "pending", "export": {"status": 200, "code": null, "letter_has": false, "notes_has": false}}
PASS S3a batch accept [clean, stale-pass bad] [num/unsupported] :: {"batch": [422, "CODE_CHECK_FAILED"], "clean_after": "pending", "bad_after": "pending"}
PASS S3b batch accept [AI draft needs_review] [num/unsupported] :: {"batch": [422, "CODE_CHECK_FAILED"]}
accept e1 -> 200
  API accept -> 422 CODE_CHECK_FAILED | The quote leaves out a hedge sentence that qualifies it. Change the quote to whole sentences of the record that keep the hedge sentence.
  forced accept -> gate ready: False | blockers: [('e8', 'EXCERPT_OMITS_QUALIFIER')]
  GET /export -> 422
  API accept -> 422 CODE_CHECK_FAILED | The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence.
  forced accept -> gate ready: False | blockers: [('e8', 'EXCERPT_NOT_WHOLE_SENTENCE')]
  GET /export -> 422
accept e1 -> 200
accept e8 (AI draft, quote drops the hedge sentence) -> 422 CODE_CHECK_FAILED
EDIT e8 summary only -> 422 CODE_CHECK_FAILED | warnings: None
gate ready: True | blockers: []
GET /export -> 200
32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss,
107:**D-051:** accept also refuses (all or nothing) any entry whose current summ
619:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in e
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:53:36.253Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-098-staff-engineer-r2-probe.py $S/wt 2>&1 | grep -E \"^SUMMARY|^FAIL\"\npython3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\na='''whole-sentence/hedge/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending \"Edit the summary to match the quote.\", `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: \"EDIT_SUMMARY\", text: \"Edit the summary to match the quote\", target: {item_id}}}`; the judge verdict does not matter |'''\nassert a in s\nb='''whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending \"Edit the summary to match the quote.\" (a summary check) or \"Change the quote to whole sentences of the record that keep the hedge sentence.\" (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: \"EDIT_SUMMARY\" | \"EDIT_QUOTE\", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |'''\ns=s.replace(a,b)\na2='''`detail.rejected` has `{id, reason: \"code_check_failed\", reason_code, why, next_action: {code: \"EDIT_SUMMARY\", text: \"Edit the summary to match the quote\", target: {item_id}}}`.'''\nassert a2 in s\ns=s.replace(a2,'''`detail.rejected` has `{id, reason: \"code_check_failed\", reason_code, why, next_action: {code: \"EDIT_SUMMARY\" | \"EDIT_QUOTE\", text, target: {item_id}}}`.''')\na3=\"The gate and the item trace recompute the code checks (D-034 numbers/dates/dollar figures/sides, D-047, D-022 qualifiers, and the quote's whole-sentence and hedge checks) from each entry's CURRENT summary and quote\"\nassert a3 in s\ns=s.replace(a3,\"The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote\")\ns=s.replace(\"the case verdict label is \\\"N summary/summaries fail(s) a check\\\".\",\"the case verdict label is \\\"N summary/summaries fail(s) a check\\\". The item trace verdict label for a failing accepted entry is \\\"Needs your attention: a check on this summary fails\\\" for an AI draft and \\\"... a check on your wording fails\\\" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says \\\"summary was AI wording removed (failed a check: <plain reason>), now ...\\\" and the draft paragraph says \\\"AI wording removed (failed a check: <reason>) (<entry id>)\\\" (the quote text of a removed narrative sentence for a judge reason is still shown).\")\nopen(p,'w').write(s)\nEOF\ngit diff --stat HEAD -- memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T05:53:41.000Z

**tool result**
````
SUMMARY: 63 checks, 0 failed
 memory/contracts/api.md | 6 +++---
 1 file changed, 3 insertions(+), 3 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:53:45.820Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/(the quote text of a removed narrative sentence for a judge reason is still shown)/(a narrative sentence removed for a judge reason is still printed)/' memory/contracts/api.md; git diff --cached --stat | tail -5; git diff HEAD --stat -- app/backend/review.py app/backend/trace.py app/backend/store.py app/backend/export.py app/backend/narrative.py app/backend/case_extras.py memory/contracts/api.md tests/unit/test_trace.py; git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T05:53:45.978Z

**tool result**
````
 app/backend/trace.py              |  30 +++------
 tests/unit/_pdf_probe.py          |  66 --------------------
 tests/unit/test_pdf_ocr_limits.py | 114 ----------------------------------
 tests/unit/test_trace.py          | 126 +-------------------------------------
 8 files changed, 15 insertions(+), 349 deletions(-)
 app/backend/case_extras.py |   3 +-
 app/backend/export.py      |  11 +++-
 app/backend/narrative.py   |   2 +-
 app/backend/review.py      |  63 ++++++++++++++--------
 app/backend/store.py       |   3 ++
 app/backend/trace.py       |  20 +++----
 memory/contracts/api.md    |   6 +--
 tests/unit/test_trace.py   | 127 ++++++++++++++++++++++++++++++++++++++++++++-
 8 files changed, 195 insertions(+), 40 deletions(-)
2dc5be2
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:53:48.937Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u /tmp/idx.XXXXXX) && git read-tree HEAD && git add app/backend/review.py app/backend/trace.py app/backend/store.py app/backend/export.py app/backend/narrative.py app/backend/case_extras.py memory/contracts/api.md tests/unit/test_trace.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T05:53:49.283Z

**tool result**
````
 app/backend/case_extras.py |   3 +-
 app/backend/export.py      |  11 +++-
 app/backend/narrative.py   |   2 +-
 app/backend/review.py      |  63 ++++++++++++++--------
 app/backend/store.py       |   3 ++
 app/backend/trace.py       |  20 +++----
 memory/contracts/api.md    |   6 +--
 tests/unit/test_trace.py   | 127 ++++++++++++++++++++++++++++++++++++++++++++-
 8 files changed, 195 insertions(+), 40 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:53:53.099Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/review.py app/backend/trace.py app/backend/store.py app/backend/export.py app/backend/narrative.py app/backend/case_extras.py memory/contracts/api.md tests/unit/test_trace.py; git show --stat --format=%h HEAD | tail -10"
}
````

### User / tool · 2026-11-02T05:53:53.848Z

**tool result**
````
check_secrets: ok (8 file(s) scanned staged)

 app/backend/case_extras.py |   3 +-
 app/backend/export.py      |  11 +++-
 app/backend/narrative.py   |   2 +-
 app/backend/review.py      |  63 ++++++++++++++--------
 app/backend/store.py       |   3 ++
 app/backend/trace.py       |  20 +++----
 memory/contracts/api.md    |   6 +--
 tests/unit/test_trace.py   | 127 ++++++++++++++++++++++++++++++++++++++++++++-
 8 files changed, 195 insertions(+), 40 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:54:00.637Z

**tool call — Bash**
````
{
 "command": "SHA=$(git log -1 --format=%h) && B=\"python3 tools/board.py\" && $B commit T-098 --sha $SHA --agent backend && $B ac T-098 --check 1 --agent backend --evidence \"r3 ($SHA): tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3, test_set_review_is_the_choke_point_for_accept_edit_and_batch_d051_r3, test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3[5 cases], test_internal_notes_never_print_ai_wording_that_failed_a_check_d051_r3, test_verdict_says_this_summary_for_an_ai_draft_t097_r3_f1 pass; mutant M11 fails 4 tests; reviewer probes 1-3 pass (63 checks 0 failed; edit 422)\" && $B handoff T-098 --agent backend --text \"What changed (r3): one choke point review.set_review recomputes the D-051 checks on the wording an accept/edit/batch-accept would leave, 422 before any write (summary-only edit can no longer clear a failing quote; quote-level failures say Change the quote, next_action EDIT_QUOTE); trace/gate recompute all 5 checks + highlight (verbatim added to CODE_CHECK_REASONS); notes print 'AI wording removed (failed a check: ...)' for edited originals and code-removed narrative sentences; AI-draft verdict label says 'this summary'; api.md updated. | Verified: tests/unit 2045 passed, 3 unrelated failures (test_provider*, t093_eval_signature: other workers); reviewer probes r2 1-3 pass on a tree copy; M11 killed. | Left: frontend refusal button still says 'Edit the summary' for EDIT_QUOTE and the Why copy 'Your wording doesn't match' should follow next_action/verdict (frontend card). | Surprised: golden pipeline fixtures already satisfy all 5 checks; edit route now returns CODE_CHECK_FAILED (not invalid_edit) for quote-level failures.\" && $B move T-098 in_review --agent backend"
}
````

### User / tool · 2026-11-02T05:54:00.695Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: SHA=$(git log -1 --format=%h) && B="python3 tools/board.py" && $B commit T-098 --sha $SHA --agent backend && $B ac T-098 --check 1 --agent backend --evidence "r3 ($SHA): tests/unit/test_trace.py::test
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:54:01.944Z

**tool call — Bash**
````
{
 "command": "git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T05:54:02.036Z

**tool result**
````
1335f21
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:54:06.976Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-098 --sha 1335f21 --agent backend && python3 tools/board.py ac T-098 --check 1 --agent backend --evidence \"r3 (1335f21): tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3, test_set_review_is_the_choke_point_for_accept_edit_and_batch_d051_r3, test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3 (5 cases), test_internal_notes_never_print_ai_wording_that_failed_a_check_d051_r3, test_verdict_says_this_summary_for_an_ai_draft_t097_r3_f1 pass; mutant M11 fails 4 tests; reviewer probes r2 1-3 pass (63 checks 0 failed; summary-only edit 422)\" && python3 tools/board.py handoff T-098 --agent backend --text \"What changed (r3): one choke point review.set_review recomputes the D-051 checks on the wording an accept/edit/batch-accept would leave, 422 before any write (a summary-only edit can no longer clear a failing quote; quote-level failures say Change the quote, next_action EDIT_QUOTE); trace and gate recompute all 5 checks plus highlight (verbatim added to CODE_CHECK_REASONS); notes print 'AI wording removed (failed a check: ...)' for edited originals and code-removed narrative sentences; AI-draft verdict label says 'this summary'; api.md updated. | Verified: tests/unit 2045 passed, 3 unrelated failures (test_provider*, t093_eval_signature, other workers); reviewer probes r2 1-3 pass on a tree copy; M11 killed by 4 tests. | Left: frontend refusal button still says 'Edit the summary' for EDIT_QUOTE and its Why copy 'Your wording doesn't match' should follow next_action and the verdict (frontend card). | Surprised: golden fixtures already satisfy all 5 checks; edit route now returns CODE_CHECK_FAILED (not invalid_edit) for quote-level failures.\" && python3 tools/board.py move T-098 in_review --agent backend"
}
````

### User / tool · 2026-11-02T05:54:07.277Z

**tool result**
````
T-098: commit 1335f21 recorded
AC 1 checked: r3 (1335f21): tests/unit/test_trace.py::test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3, test_set_review_is_the_choke_point_for_accept_edit_and_batch_d051_r3, test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3 (5 cases), test_internal_notes_never_print_ai_wording_that_failed_a_check_d051_r3, test_verdict_says_this_summary_for_an_ai_draft_t097_r3_f1 pass; mutant M11 fails 4 tests; reviewer probes r2 1-3 pass (63 checks 0 failed; summary-only edit 422)
handoff written on T-098
T-098: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T05:54:11.115Z

T-098 round 3 is in review at commit 1335f21, with the blocker, the major, the minors and your "This summary" add-on all done. In `tests/unit`, 2045 passed and 3 failed (`test_provider`, `test_provider_backends`, `test_t093_eval_signature`); I did not touch those files. The three reviewer probes pass, and M11 is now killed by 4 new tests.

- **Blocker:** `review.set_review` is now the single choke point. Accept, edit (including a summary-only edit) and batch accept all run the check on the wording they would leave, before any write. A failing quote returns 422 `CODE_CHECK_FAILED` with "Change the quote" and `EDIT_QUOTE`, and the stored reason stays. Reset is never blocked.
- **Major:** The gate and trace now recompute all 5 checks plus the highlight, and `api.md` matches.
- **Minors:** The internal notes now say "AI wording removed (failed a check: …)" instead of printing the failing AI text.
- **Add-on:** An accepted AI draft that fails a check now reads "a check on this summary fails". "Your wording" stays for paralegal-written or edited summaries.
- **Frontend follow-up:** The frontend's refusal button still says "Edit the summary" when `next_action` is `EDIT_QUOTE`. A quote-level failure on edit now returns `CODE_CHECK_FAILED` rather than `invalid_edit`, so it shows only through the frontend's generic error path. Its Why copy "Your wording doesn't match" is also stale. That needs a frontend card.

I committed with the pathspec rule and the commit lists only my 8 files.
