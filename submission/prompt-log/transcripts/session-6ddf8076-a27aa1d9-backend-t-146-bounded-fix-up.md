# Subagent: Backend: T-146 bounded fix-up (Backend: T-146 bounded fix-up)

Source: `agent-a27aa1d906a194dec.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:47:36.540Z

You are a backend worker in /Users/arsis/zlayt-pm-project on board card T-146, a bounded fix-up after the round cap. Claim it with `--force`, then read reviews/T-146-staff-engineer-r3.md and the orchestrator's §7.4 note on the card.

Implement exactly the note's two items in pipeline.py, test-first:
1. Keep-and-note compares the whole ladder of checks, not just the state. Use the reviewer's a2 repro, where the second check goes from agree to disagree.
2. A failure in the conflicts step makes the gate RUN_FAILED.

Do the minors only if they're cheap.

Don't touch amounts.py (T-140), charge_text.py, export.py or trace.py (T-139), conflicts.py, case_list.py or app/frontend. Commit via a temp index for only your hunks; the pre-commit hook runs the sample.

Run the full unit suite, write the handoff, and move the card to in_review. Reply in 1 line.

### User / tool · 2026-11-02T14:47:36.545Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:47:39.333Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B claim T-146 --agent backend --force 2>&1 | tail -3; $B show T-146 | tail -60; cat reviews/T-146-staff-engineer-r3.md | head -120"
}
````

### User / tool · 2026-11-02T14:47:39.590Z

**tool result**
````
T-146 claimed by backend
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:09:56Z"
updated_at: "2026-11-02T14:47:39Z"
claimed_by: "backend"
claimed_at: "2026-11-02T14:47:39Z"
rounds: 3
commits: ["7d3ca35a434914a83318255c703c375b2e443b93", "2db6ad2", "bf53087"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-146-staff-engineer.md", "at": "2026-11-02T13:39:36Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-146-staff-engineer-r2.md", "at": "2026-11-02T14:22:03Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-146-staff-engineer-r3.md", "at": "2026-11-02T14:47:33Z"}
ac:
  - {"n": 1, "text": "a timed-out or failed re-run keeps every previous item and decision (or keeps exactly what the error message says); test reproduces 9 entries/11 flags kept", "done": true, "evidence": "tests/unit/test_t146_r3_decided_items_never_lowered.py (56 tests): flag-step-down, summary-check-failed, extract-down, judge-down, deadline, nothing-to-keep keep decided rows whole, note them, run_partial with exact messages; 35 mutants killed incl. the 7 survivors"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:10:00Z orchestrator: assigned: backend
- 2026-11-02T13:10:11Z backend: claimed
- 2026-11-02T13:14:56Z backend: Fix in pipeline.py: _persist(additive=timed_out) adds only unseen ids on a timed-out run; no delete, no overwrite, so a complete earlier run and the paralegal's decisions are untouched; error message reworded to say exactly that. Reviewer saw 11 flags; this sample gives 10 on the fixture backend, tests assert equality before/after not the count.
- 2026-11-02T13:26:49Z backend: AC 1 checked: tests/unit/test_t146_rerun_keeps_items.py (6 tests: complete run then timeout at extract/verify/judge_entries/flags and between records 3 and 4 -> every item, state and the accepted e1 decision unchanged; 9 entries, 10 flags on this fixture)
- 2026-11-02T13:26:50Z backend: moved in_progress -> in_review
- 2026-11-02T13:26:56Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T13:39:36Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-146-staff-engineer.md; round 1; findings:
    - [major] A failed re-run (AI step down) still overwrites the paralegal's accepted entries with empty failure stubs, and the case reads 'ready' with no error — fix: When the re-run produces a failure stub for an id that already has a stored row with a summary and excerpt (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, SCHEMA_INVALID at extract), keep the stored row and record the failure on the run (
    - [minor] The tests do not pin the message the card changed, and compare only review_status/state/reasons, so a summary-only overwrite and the old message both pass — fix: Snapshot the full stored row (summary, excerpt, date_iso, record_ids, computed, ladder judge verdict) and assert equality; assert the message text, or better, that it contains 'earlier' and 'kept' and does not contain 'finis
- 2026-11-02T13:39:36Z orchestrator: Orchestrator answer to the reviewer's question (not for Chris): 'failed re-run' includes any re-run with errors (done_with_errors, failed, deadline). No re-run may overwrite a decided item or an item with stored output with an empty or partial stub; errored records keep their previous items and the case shows an honest error. Also: tests assert the message text; kill the summary-wipe mutant. Cheap add: T-145 minor - a judge that was called and failed says 'second check failed', not 'JUDGE_NOT_RUN:' (keep the reason code).
- 2026-11-02T13:39:36Z orchestrator: assigned: backend
- 2026-11-02T13:39:44Z backend: claimed
- 2026-11-02T13:58:43Z backend: AC 1 checked: tests/unit/test_t146_r2_failed_rerun_keeps_items.py (11 tests: extract-down, one-record-down, judge-down, flag-step-down re-runs keep full stored rows, case failed/run_partial with message; deadline at 5 stages keeps full rows; message text asserted; mutants no-protect/summary-wipe/prune/old-message each fail)
- 2026-11-02T13:58:43Z backend: moved in_progress -> in_review
- 2026-11-02T13:58:48Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T14:22:03Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-146-staff-engineer-r2.md; round 2; findings:
    - [major] A re-run with the flag step down downgrades an accepted, verified flag to needs_review / LLM_FAILED_AFTER_RETRIES, drops its second-check answer and AI origin, and reports run status 'done', case 'ready', error None — fix: Treat a flag row made while the flag step failed (its reasons contain LLM_FAILED_AFTER_RETRIES and the stored row's do not, or `failed_steps` contains 'flags') as 
    - [major] A re-run whose extract answer fails the summary-in-quote check replaces an accepted entry with an empty rejected stub, with case 'ready', error None, and a passing export gate — fix: Either include SUMMARY_NOT_IN_QUOTE (and any extract-stage rejection) in the keep-whole rule for rows that have a stored summary and quote, with the same run_partial message, or keep the new row only as 
    - [minor] Seven mutants survive: the message count, the flag-step label, the stub-reason set, the FixtureMiss path and the conflicts guard are not pinned — fix: Assert the exact count and step in each message test (extract-down: '9 items' and 'writing the entries'; judge-down: the stored-row count and 'the second check'; flag-down: 'finding the flags'); add one parametrized test over the three
    - [minor] A re-run that ends with errors but has no stored output to keep still reads 'ready' with error None; the new messages never fire — fix: When `errors` is non-empty or a step in `failed_steps` failed, set the case error (code run_partial or a sibling) with the count of items that have no output and the step name, whether or not anything was kept.
- 2026-11-02T14:22:03Z orchestrator: Round 3 (final): one rule for every stage - a re-run never lowers or replaces a decided item (accepted/dismissed/edited) for any failure or check result in the new run; if the new output for a decided item differs or fails a check, keep the decided item and add a visible 'the re-run disagreed / failed here' note on it, and the case shows run_partial. Covers the flag-step-down and the summary-check-failed paths. Kill the 7 surviving mutants.
- 2026-11-02T14:22:03Z orchestrator: assigned: backend
- 2026-11-02T14:22:11Z backend: claimed
- 2026-11-02T14:38:46Z backend: AC 1 checked: tests/unit/test_t146_r3_decided_items_never_lowered.py (56 tests): flag-step-down, summary-check-failed, extract-down, judge-down, deadline, nothing-to-keep keep decided rows whole, note them, run_partial with exact messages; 35 mutants killed incl. the 7 survivors
- 2026-11-02T14:38:46Z backend: moved in_progress -> in_review
- 2026-11-02T14:38:51Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T14:47:33Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-146-staff-engineer-r3.md; round 3; findings:
    - [major] A decided item whose stored state is needs_review is replaced when the new run's checks get worse inside that state (new JUDGE_DISAGREES reason, second-check answer agree -> disagree): no note, case ready, error None — fix: In `_disagrees`, treat as a disagreement any change that adds a reason code to `state_reasons` that the stored row did not have, or a judge verdict that moves fro
    - [minor] Any wording difference on a decided entry is treated as a failure: the case goes failed and the export gate shows RUN_FAILED until a re-run reproduces the stored summaries byte for byte — fix: Ask Chris whether a changed summary on an accepted entry should block the gate or only note the item (keeping the decided row), or whether the new result should be offered as a choice on the it
    - [minor] The per-item note has no consumer: rerun_note is on the item view, the case message says 'each item carries a note', and nothing in app/frontend reads it; no card exists to render it — fix: Open a frontend card to render `rerun_note` on the item row and in the review panel (and list the kept ids in the case error), or state in SCOPE_CUTS.md that the note is API-only for now.
    - [minor] The export gate is not asserted on any r3 path, and the equal-rank case is not in the compare table — fix: Add `assert 'RUN_FAILED' in [b['reason_code'] for b in trace.export_blockers(conn, cid)]` to the flag-down, summary-check, extract-down, judge-down and deadline tests, and a control that a clean re-run has none; add equal-rank rows to the compare table with F1.
- 2026-11-02T14:47:33Z orchestrator: §7.4 at cap: bounded fix-up + scoped check. (1) The keep-and-note rule compares the whole ladder (code checks, judge verdict, reasons), not only the state: a decided item whose checks get worse inside needs_review (agree->disagree, a new reason) is kept with a visible note, and the case is run_partial; (2) a conflicts-step failure makes the gate RUN_FAILED like every other step. Minors only if cheap.
- 2026-11-02T14:47:33Z orchestrator: assigned: backend
- 2026-11-02T14:47:39Z backend: claimed

## Handoff
What changed (r3): one rule in pipeline._persist: a re-run never lowers or replaces a decided item (accepted/dismissed/edited). If the new row fails (_degrades: stub, flag made while the flag step was down, lost second check) or differs/lowers (_disagrees: worse state, other summary/quote/date/amount/evidence) the stored row stays whole, ladder.rerun_note is set (item views carry rerun_note), case = failed/run_partial with exact messages (failed N items + step; different result for M decided; no earlier result to keep on a re-run). Undecided items keep r2 behaviour. Deadline stays additive/run_deadline (nothing redone, no note). Dead 'conflicts' prune-guard member removed. api.md updated. Verified: tests/unit/test_t146_r3_decided_items_never_lowered.py 56 pass, r2/r1 files pass, 35-mutant run (stub reasons, flag fail codes, labels, rank, each content branch, decided, note, counts, prune, FixtureMiss, rerun cond) all killed; unit suite 4300 pass, 12 fail all outside this card (T-140 amounts x10, test_reclassify rerun-sentence and test_trace e2 steps from T-139 charge_text work in progress; reclassify one fails on HEAD pipeline too). Left: SUMMARY_NOT_IN_QUOTE on an UNDECIDED entry still lands in the tray (new check result stands, pinned by a test). Surprised: step names are only j1-j4/flags (no 'conflicts'), so the old prune-guard member was dead; judge call ids and generator call ids differ every run so row compares drop call_id. Commit bf53087

# T-146 staff-engineer review, round 3 (bf53087, tested on a `git archive` of bf53087)

Verdict: **changes** (0 blockers, 1 major, 3 minors, 1 nit).

The two round-2 majors are fixed and the one-rule design works on every path I could name. On the archive I completed the sample (9 entries, 4 amounts, 10 flags), decided every item (accept / dismiss mix, e3 edited), then re-ran:
- Flag step down (LLMFailed and FixtureMiss), summary-in-quote failing on rec 1 and on all 9, a valid but different summary, extract down (LLMFailed and schema-invalid), j1 down, j2 down, all four judges down, everything down, j1 "unsupported": all keep the full stored rows (0 rows differing, excluding call ids and the note itself). They carry the right note kind and step, the case reads `failed` / `run_partial` with the exact count and step in the message, and `trace.export_blockers` lists `RUN_FAILED`, so the gate agrees with the case.
- Deadline at extract, verify, judge_entries, amounts, conflicts and flags: 0 rows differing, `run_deadline`, `RUN_FAILED` blocker, no notes.
- Nothing to keep: a first run with every step down stores the stubs and stays `ready` (by design); the second all-down run reads `failed` / `run_partial` "The AI step failed for 20 items (finding the flags and the second check and writing the entries) on this run, and there is no earlier result to keep."; a later good run clears the error.
- Identical re-runs (twice) of a fully decided case: 0 rows differing, no notes, `ready`. A reclassified amount keeps its class with no note.

One hole is left in the "differs or fails a check" half of the rule: an equal-rank change is invisible to `_disagrees`. See F1.

What I ran (archive of bf53087, `/Users/arsis/zlayt-pm-project/.venv/bin/python -I`; HEAD later moved to 52ac285, and `git diff --stat bf53087 HEAD` shows no change to pipeline.py, present.py, trace.py or the r3 test file):
- `pytest tests/unit -q -p no:cacheprovider --continue-on-collection-errors`: **4273 passed, 8 skipped, 1 failed, 1 error** in 244 s. Both are other work: `test_amounts_d059.py::test_adjusters_ledger_totals_1950_when_acceptable_lines_are_accepted_one_by_one` and the collection of `test_amounts_d059_api.py` read `artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt`, which is untracked (`git status --short` shows `?? artifacts/review-evidence/T-140-adjuster/`, `git ls-files` lists nothing), so it is missing from any clean checkout. The handoff's "12 failing" were working-tree amounts and T-139 work that do not appear at the committed tree. None touch T-146.
- Probe scripts (scratchpad `t146r3/probes/`): `a.py` identical re-runs, `b.py` fourteen failure paths, `c.py` and `d.py` the equal-rank repro, `e.py` deadline at six stages plus nothing-to-keep, `f.py` reclassify carry-over and consecutive disagreeing runs. Each compares every stored column of 23 items, case status and error text, notes, and `trace.export_blockers`.
- 30 mutants of pipeline.py and present.py on a scratch copy, run against the three T-146 test files (r3: 56 tests): 29 killed there, 1 (removing the `RC.carry_over` call) survives the T-146 files but fails 7 tests in `test_reclassify.py`, so killed overall. The 7 round-2 survivors are all pinned now (count, label, stub reasons, FixtureMiss, prune guard).

```json
{
  "card": "T-146",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "commit bf53087 (app/backend/pipeline.py _failure/_degrades/_disagrees/_persist/_partial_error, present.py rerun_note, memory/contracts/api.md, tests/unit/test_t146_r3_decided_items_never_lowered.py); git archive of bf53087 (HEAD later 52ac285, no change to these files); fixture backend; sample case evals/golden/sample.txt",
  "exercised": [
    "read personas/staff-engineer.md, reviews/T-146-staff-engineer-r2.md, python3 tools/board.py show T-146 (orchestrator one-rule note, handoff), git show bf53087 (pipeline.py, present.py diff in full), the r3 test file in full",
    "git archive bf53087 into a scratch dir; pytest tests/unit -q -p no:cacheprovider --continue-on-collection-errors: 4273 passed, 8 skipped, 1 failed, 1 error (both T-140 amounts tests reading the untracked artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt)",
    "probe a.py: all 23 items decided (accept/dismiss mix, e3 edited), identical re-run twice: 0 rows differing, no notes, case ready",
    "probe b.py: flag step LLMFailed and FixtureMiss, summary-in-quote failing on rec 1 and on all entries, extract down, extract schema-invalid, j1 down, j2 down, all judges down, conflicts down, j1 unsupported, j2 disagree, everything down; full stored-row compare, case status/error text, notes, trace.export_blockers",
    "probe d.py: valid but different summary for decided e1 (kept, note, run_partial); accepted needs_review amount a2 and flag f_r6_1 with judge answers flipped to disagree (a2 replaced, no note, case ready, no blockers)",
    "probe e.py: deadline at extract, verify, judge_entries, amounts, conflicts, flags on a fully decided case; first all-down run, second all-down run (nothing to keep), third good run",
    "probe f.py: reclassified decided amount then identical re-run (no note); two consecutive disagreeing runs (note stable); good run clears the note and error",
    "30 mutants on a scratch copy (_failure arms, _degrades arms, rank compare, each content field, computed guard, decided set, note write, note ladder merge, empty count, rerun condition, prune, plural, undecided note, present rerun_note, additive skip, kind label, error branch, carry_over, deadline code): all killed (one by test_reclassify.py)",
    "grep for rerun_note in app/frontend (no consumer), tests/unit/test_t146_r3_decided_items_never_lowered.py for export_blockers/RUN_FAILED (none), board list for a card to render the note (none)",
    "git diff --stat bf53087 HEAD on pipeline.py, present.py, trace.py and the r3 test file: no change"
  ],
  "verdict": "changes",
  "scores": {
    "decided_item_never_lowered_or_replaced": 3,
    "six_paths_keep_rows_and_note": 5,
    "case_message_and_gate_agree": 4,
    "test_quality_mutation_sensitivity": 4,
    "note_visible_to_the_paralegal": 2
  },
  "findings": [
    {
      "severity": "major",
      "title": "A decided item whose stored state is needs_review is replaced when the new run's checks get worse inside that state (new JUDGE_DISAGREES reason, second-check answer agree -> disagree): no note, case ready, error None",
      "evidence": "pipeline.py:277 `if _RANK.get(it[\"state\"], 1) > _RANK.get(old[\"state\"], 1) and old[\"state\"] != \"rejected\":` is the only check-result test in `_disagrees` (272-286); reasons and judge answer are not compared. Repro (probe d.py, archive of bf53087): complete sample run, accept a2 ($185, rate, needs_review, reasons ['AMOUNT_RATE_NOT_TOTALED'], judge agree) and f_r6_1, then `rerun(... j2={'verdict':'disagree','reason_code':'NONE'})` -> a2 `needs_review ['JUDGE_DISAGREES', 'AMOUNT_RATE_NOT_TOTALED'] accepted`, `ladder.judge.verdict` `disagree` (was `agree`), `rerun_note` None, stored-row diff `amount a2 CHANGED ['state_reasons', 'ladder']`, case `ready`, error None, `trace.export_blockers` []. `present.item_view` `why` now reads 'A second AI check disagreed with the first result for this item.' with `rerun_note` None. The same happens to a dismissed a2 (probe b.py 'j2 says disagree': 'rows differing: 1', a2 not in the notes list). Control: the same flip on a verified accepted charge (a1, a4) is kept whole with a note, because verified -> needs_review is a rank drop; so the rule holds only where the state label happens to change.",
      "why_it_matters": "The orchestrator's round-3 rule is 'never lowers or replaces a decided item, whatever the new run's checks say'. A new disagreeing second check is a check result that lowers the item, and the earlier agree answer is the audit record the paralegal decided on. Here the answer is overwritten silently and the case reads green, which is exactly the shape of the round-2 majors (a reachable path where the run lowers a decided item without a note). Not a blocker: the quote, the value and the decision survive, and a rate or a lexicon-only flag in needs_review is never totalled or exported as verified.",
      "fix": "In `_disagrees`, treat as a disagreement any change that adds a reason code to `state_reasons` that the stored row did not have, or a judge verdict that moves from a positive answer (agree, supported, conflict-confirmed) to a negative one, even when the state rank is equal; keep the stored row whole and set the note and run_partial as for the other disagreements. Add the equal-rank cases to `test_disagrees_table` and one end-to-end test (accepted rate / lexicon-only flag, judge flipped).",
      "acceptance_test": "Unit test: complete run, accept a2, re-run with j2 returning disagree; assert the full stored row of a2 is unchanged, `rerun_note.kind == 'disagreed'`, case failed/run_partial naming 1 item. Mutation: removing the new reason/verdict comparison fails it. Also add a row to `test_disagrees_table`: same state needs_review, new reasons ['JUDGE_DISAGREES', ...] -> True."
    },
    {
      "severity": "minor",
      "title": "Any wording difference on a decided entry is treated as a failure: the case goes failed and the export gate shows RUN_FAILED until a re-run reproduces the stored summaries byte for byte",
      "evidence": "Probe d.py D1: re-run with a valid, in-quote but differently worded summary for decided e1 -> e1 kept, note 'disagreed', case `failed`, error 'The re-run gave a different result for 1 item you had already decided...', `trace.export_blockers` = [RUN_FAILED, ...]. `_disagrees` compares `summary` by string equality (pipeline.py:279-280); nothing in app/llm pins a seed or temperature (`grep -n 'temperature\\|seed' app/llm/*.py` finds only record.py's seeded-edit test data), so the live claude-cli backend will word summaries differently on most re-runs. The only ways out are a byte-identical run or resetting each decision.",
      "why_it_matters": "This follows the rule as written, so it is not a violation. But with a live model every re-run of a case with decided entries is likely to end `failed` and export-blocked, with the new result not applied and not visible, and 'Run it again to retry' repeats the same outcome. That makes re-run practically a one-way trap for decided cases. This is a product call, not an engineering one.",
      "fix": "Ask Chris whether a changed summary on an accepted entry should block the gate or only note the item (keeping the decided row), or whether the new result should be offered as a choice on the item (apply / keep).",
      "acceptance_test": "Per the answer: either a test that a reworded summary notes the item but leaves the case `ready`, or one that the item offers the new text."
    },
    {
      "severity": "minor",
      "title": "The per-item note has no consumer: rerun_note is on the item view, the case message says 'each item carries a note', and nothing in app/frontend reads it; no card exists to render it",
      "evidence": "`grep -rln rerun_note` finds it only in app/backend/pipeline.py, app/backend/present.py, memory/contracts/api.md and tests (none in app/frontend); `python3 tools/board.py list | grep -i 'rerun\\|run_partial'` shows no open card for rendering it (T-157 is about case names and rerun_available). api.md:129 says it is 'to be shown on the item'.",
      "why_it_matters": "The orchestrator's rule asks for a visible note. Today the paralegal sees a failed case with a message but cannot see which items were kept or why. The backend half is done and tested at the item-view level.",
      "fix": "Open a frontend card to render `rerun_note` on the item row and in the review panel (and list the kept ids in the case error), or state in SCOPE_CUTS.md that the note is API-only for now.",
      "acceptance_test": "E2E or DOM test: after a failing re-run, an item with a note shows its message text in the queue row."
    },
    {
      "severity": "minor",
      "title": "The export gate is not asserted on any r3 path, and the equal-rank case is not in the compare table",
      "evidence": "`grep -n 'blockers\\|RUN_FAILED\\|export' tests/unit/test_t146_r3_decided_items_never_lowered.py` returns nothing. The gate agrees today only because `trace.export_blockers` reads `case.status == 'failed'` (trace.py:1132); I confirmed `RUN_FAILED` in the blockers on every run_partial and run_deadline path by probe, but no test would catch a path that sets the error and leaves the case `ready`. `test_disagrees_table` (rows 'entry', 'amount', 'flag') has no row where the state is equal and the reasons or judge verdict differ.",
      "why_it_matters": "Checklist 13 and the brief: the gate must agree with the case state. It does, but by one shared line that no T-146 test pins.",
      "fix": "Add `assert 'RUN_FAILED' in [b['reason_code'] for b in trace.export_blockers(conn, cid)]` to the flag-down, summary-check, extract-down, judge-down and deadline tests, and a control that a clean re-run has none; add equal-rank rows to the compare table with F1.",
      "acceptance_test": "Mutation: setting the case `ready` when `err` is set fails the new asserts."
    },
    {
      "severity": "nit",
      "title": "The deadline path keeps decided items whole but sets no note and reads run_deadline, not the run_partial the rule text names",
      "evidence": "Probe e.py: deadline at six stages -> 0 rows differing, `run_deadline` 'every item from earlier runs and every decision of yours was kept unchanged', `RUN_FAILED` blocker, 0 notes. The brief's rule says 'the case shows run_partial' and the item 'gets a visible note'. The handoff and api.md document the deadline exception ('nothing was redone').",
      "why_it_matters": "Nothing is lowered or lost and the case is failed with an accurate message, so I do not rate it a violation; it is a literal deviation from the rule text that Chris should know about.",
      "fix": "None needed if run_deadline stays; otherwise add a note per kept decided item.",
      "acceptance_test": "n/a (documented design)."
    }
  ],
  "whats_right": [
    "One choke point (`_persist`) handles flags, summary-check, extract, judge and nothing-to-keep: all 14 failure probes keep every stored column of 23 decided items, and the case message names the exact count and step.",
    "The export gate and the case agree on every run_partial and run_deadline path (RUN_FAILED listed, case failed), and a later good run clears the error and the notes while the decision stands.",
    "The r3 test file asserts exact messages and full-row equality and kills all 30 of my mutants (29 in its own files, the carry_over one in test_reclassify.py), including the 7 round-2 survivors."
  ],
  "questions_for_chris": [
    "A re-run whose valid new summary differs from an accepted entry's summary currently fails the case and blocks export until a byte-identical re-run (F2). Should it only note the item and let the case stay ready, or offer the new text as a choice?",
    "A decided gap flag whose computed numbers moved is still replaced and its decision reset (pipeline.py:283-284, the pre-existing reset path, excluded from `_disagrees` on purpose). Keep that as the one documented exception to 'never replaces a decided item'?"
  ]
}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:47:39.955Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/backend/project_t146_rerun_decided_rule.md"
}
````

### User / tool · 2026-11-02T14:47:39.963Z

**tool result**
````
1	---
2	name: t146-rerun-decided-rule
3	description: T-146 r3 re-run rule in pipeline._persist: decided items kept whole with ladder.rerun_note; _degrades/_disagrees/_failure; message shapes; test helpers
4	metadata:
5	  type: project
6	---
7	
8	`_persist` returns `(kept, empty)`. Kept = stored row left as is when the new row fails (`_degrades`: entry stub, flag made while flag step down, lost second check) or, for DECIDED rows only, `_disagrees` (worse state or different content). Decided kept rows get `ladder.rerun_note` (view field `rerun_note`); undecided keeps get no note. Case = failed/run_partial built in `_partial_error`; `empty` (failures with nothing stored) counts only when the case already had entries (re-run). Deadline stays additive/run_deadline with no note.
9	
10	**Why:** reviewer round 2 found accepted flags downgraded and accepted entries replaced by SUMMARY_NOT_IN_QUOTE stubs with case "ready". **How to apply:** new failure kinds go in `_failure`; extend the table tests (`test_disagrees_table`, `test_degrades_table`).
11	
12	Pitfalls: step names in `failed_steps` are only j1-j4/flags/extract/split (no "conflicts"); judge and generator `call_id` differ every run, so row-equality helpers drop `call_id`; present.py/api.md carry other agents' hunks, commit via temp index.
13	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:47:43.609Z

**tool call — Bash**
````
{
 "command": "sed -n 215,420p app/backend/pipeline.py; grep -n \"conflicts\" app/backend/pipeline.py | head -50"
}
````

### User / tool · 2026-11-02T14:47:43.710Z

**tool result**
````
                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    if kind == "amount":
        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids", "endpoint_warnings", "conditional") if k in it}
    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}


JUDGE_NOT_RUN = "JUDGE_NOT_RUN"


def _mark_judge_not_run(entries: list, by_n: dict) -> None:
    """T-145: an AI entry that has no judge-1 answer (the run hit its deadline before or during the stage) is recorded as judge `unavailable` with reason_code
    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) refuses it.
    Missing is not a pass: compose treats a judge of None as 'nothing to doubt', so the absence is made explicit here."""
    for e in entries:
        if e["state"] == "rejected" or (e["ladder"].get("judge") or {}).get("verdict"):
            continue
        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_RUN}
        generator.compose(e, by_n[e["seq"]], judge="unavailable")


_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
_FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
_RANK = {"verified": 0, "needs_review": 1, "rejected": 2}


def _failure(kind: str, it: dict):
    """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
    step failed, or an item whose second check was asked and gave no answer."""
    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS:
        return "writing the entries"
    if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
        return "finding the flags"
    return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None


def _degrades(kind: str, old: dict, it: dict):
    """T-146 r2/r3: would storing `it` over the stored row `old` replace output with a failure, or take back a second-check answer? Returns the step's name or None.
    (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
    cause = _failure(kind, it)
    if cause == "writing the entries":
        return cause if old.get("summary") and old.get("excerpt") else None
    if cause == "finding the flags":
        return None if set(old.get("state_reasons") or []) & _FLAG_FAIL else cause
    return cause if ((old.get("ladder") or {}).get("judge") or {}).get("verdict") not in (None, "unavailable") else None


def _evidence_texts(row: dict) -> set:
    return {e.get("text") or e.get("excerpt") for e in (row.get("evidence") or [])}


def _disagrees(kind: str, old: dict, it: dict) -> bool:
    """T-146 r3: does the NEW row `it` lower or change what the stored row `old` says? True when its state is worse (verified -> needs_review -> rejected) or its content
    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes). A better state with the same content is not a disagreement.
    A stored row that is itself in the tray (rejected) has nothing to lower. A flag whose computed numbers changed is the existing reset path (the decision was about
    other numbers), so it is not judged here."""
    if _RANK.get(it["state"], 1) > _RANK.get(old["state"], 1) and old["state"] != "rejected":
        return True
    if old["state"] == "rejected":
        return False
    if kind == "entry":
        return (old.get("summary"), old.get("excerpt"), old.get("date_iso")) != (it.get("summary"), it.get("excerpt"), it.get("date"))
    if kind == "amount":
        return (old.get("text"), old.get("value_cents"), old.get("kind")) != (it.get("text"), it.get("cents"), it.get("cls"))
    oc = old.get("computed") or {}
    if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
        return False
    return (old.get("type"), old.get("category"), _evidence_texts(old)) != (it.get("type"), it.get("category"), {e.get("text") for e in it.get("evidence", [])})


def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True) -> tuple:
    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.
    `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must not delete, downgrade or
    overwrite what an earlier complete run stored (its judged states, its flags) or what the paralegal decided.
    One rule for every stage (T-146 r3): a re-run never lowers or replaces a decided item (accepted, dismissed, edited). When the new row fails (`_degrades`) or lowers
    or changes it (`_disagrees`), the stored row is kept as it is and `ladder.rerun_note` says so (shown on the item). A row that is not decided is kept the same way,
    without a note, when the new row is a failure over stored output (a stub, a flag made while the flag step failed, a lost second-check answer).
    Returns (kept, nothing_to_keep): `kept` is [(stored row, step, 'failed' | 'disagreed')]; `nothing_to_keep` is [(step)] for new rows that are failures with no stored
    output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale)."""
    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    kept, empty = [], []
    for it in items:
        old = existing.get(it["id"])
        if additive and old is not None:
            continue
        if old is not None and kind == "amount":        # T-084: a rerun keeps the class the paralegal gave a figure
            from app.backend import reclassify as RC
            it = RC.carry_over(old, it)
        decided = old is not None and old["review_status"] != "pending"
        cause = _degrades(kind, old, it) if old is not None else None
        how = "failed" if cause else None
        if decided and not cause and _disagrees(kind, old, it):
            cause, how = "a different result", "disagreed"
        if cause:
            kept.append((old, cause, how))
            if decided:
                msg = (f"The re-run could not redo this item ({cause}). Your decision and the earlier result were kept." if how == "failed" else
                       "The re-run gave a different result for this item (its summary, quote or checks no longer match what you decided on). Your decision and the earlier result were kept; the new result was not applied.")
                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
            continue
        fail = _failure(kind, it)
        if fail:
            empty.append(fail)
        row = _row(kind, it)
        if old is None:
            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
            continue
        DB.update_item(conn, it["id"], now=now, case=cid, **row)
        if kind == "flag" and old["review_status"] != "pending":
            oc = old.get("computed") or {}
            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
            else:
                it["review_status"] = old["review_status"]
        elif old["review_status"] != "pending":
            it["review_status"] = old["review_status"]
    if additive:
        return kept, empty
    keep = {i["id"] for i in items}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            if not prune:
                kept.append((old, "finding the flags", "failed"))
                continue
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
    return kept, empty


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing, now)
    _store_run_checks(conn, cid, ing["records"], "pending")
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"], "translated": any(language.translated_record(by_n.get(n)) for n in a["record_nos"])})      # D-050
    a["state"], a["reasons"] = state, reasons
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None),
                   **({"confirm": a["confirm"]} if a.get("confirm") else {})}      # D-059: the flag the paralegal must confirm by name before accepting this charge
    a["why"] = WHY.join(reasons, a["ladder"]["judge"]) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
    return a


def _entry_for(entries: list, record_no: int):
    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)


def _err(code, stage, record_no=None, cause=None) -> dict:
    d = {"code": code, "stage": stage}
    if record_no is not None:
        d["record_no"] = record_no
    if cause:
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
    return int(ds[0][:4]) if ds else None


def _items(n: int) -> str:
    return f"{n} item{'s' if n != 1 else ''}"


def _partial_error(kept: list, empty: list):
    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
    It names how many items and which steps, and says exactly what was kept."""
    failed, differed = [k for k in kept if k[2] == "failed"], [k for k in kept if k[2] == "disagreed"]
    parts = []
    if failed:
        parts.append(f"The AI step failed for {_items(len(failed))} ({' and '.join(sorted({c for _, c, _ in failed}))}) on this run. Their earlier results and every "
                     "decision of yours were kept unchanged.")
    if differed:
        parts.append(f"The re-run gave a different result for {_items(len(differed))} you had already decided; your decision and the earlier result were kept, "
                     "and each item carries a note.")
    if empty:
        parts.append(f"The AI step also failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) with no earlier result to keep." if kept else
                     f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
    return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None


4:5 conflicts (code proposes the pairs, J3 classifies each)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
5:Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
14:from app.backend import (amounts as AM, confidence, conflict_candidates as CC, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
19:STAGES = ("ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize")
59:    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
499:    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
502:    conflicts_ran = guard("conflicts")
503:    if conflicts_ran:
553:                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
555:    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:47:49.126Z

**tool call — Bash**
````
{
 "command": "sed -n 440,600p app/backend/pipeline.py; grep -n \"def test_disagrees_table\" -B5 -A40 tests/unit/test_t146_r3_decided_items_never_lowered.py | head -120; sed -n 1,80p tests/unit/test_t146_r3_decided_items_never_lowered.py; git status --short | head -20"
}
````

### User / tool · 2026-11-02T14:47:49.301Z

**tool result**
````
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s

    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
    try:
        ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), splitter=_frozen_splitter(conn, cid))
    except language.UnsupportedLanguage:               # D-042: a clear failure, never a run that guesses; the case is not left 'running'
        DB.update_case(conn, cid, status="failed", error=json.dumps({"code": "unsupported_language", "message": "The records are not in English or Spanish."}))
        raise
    text, recs = ing["text"], ing["records"]
    by_n = {r["n"]: r for r in recs}
    _store_split_failure(conn, cid, ing.get("split_failure"))
    if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
    _store_records(conn, cid, ing, clock())
    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
    code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
    status = "done"
    timed_out = False

    def guard(name):
        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True

    # 1-3: entries
    if guard("extract"):
        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
        for f in failures:
            rejected.append(generator.failure_entry(by_n[f["record_no"]], next(g for g in ing["groups"] if g[0] == f["record_no"]), f["failure"], f.get("detail")))   # never vanishes: tray item with the reason
            if f["failure"] != "SUMMARY_NOT_IN_QUOTE":      # D-054: a tray item, not an error (the model answered; code removed what the quote does not support)
                errors.append(_err("UNSUPPORTED_LANGUAGE" if f["failure"] == "UNSUPPORTED_LANGUAGE" else "LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"],
                                   "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
    if guard("verify"):
        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
    if guard("judge_entries") and entries:
        generator.judge_entries(entries, by_n, call=call, case_text=text)
    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
    for e in entries + rejected:
        e["ladder"]["backend"] = P.backend_name()
        e.pop("_stage", None)
    # 4: amounts (J2 on every dollar amount)
    final_amounts = code_amounts
    if guard("amounts"):
        dollars = [a for a in ing["amounts"]]
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
                                        call=call, case_text=text)
        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
    for a in final_amounts:
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
    conflicts_ran = guard("conflicts")
    if conflicts_ran:
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
    now_t = clock()
    rerun = bool(DB.list_items(conn, cid, "entry"))      # entries exist only after an earlier run: this is a re-run
    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
    for a in final_amounts:                     # an amount stays linked to the entry whose record failed this time (that entry's stored row was kept)
        if not a.get("entry_id"):
            a["entry_id"] = next((o["id"] for o, _, _ in kept_e if f"r{a['record_nos'][0]}" in (o["record_ids"] or [])), None)
    kept_a, empty_a = _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
    kept_f, empty_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
    kept, empty = kept_e + kept_a + kept_f, empty_e + empty_a + empty_f
    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        err = _partial_error(kept, empty if rerun else [])
    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
        g = dict(f)
        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
        if f["type"] == "gap":
            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
        flags.append(g)
    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}


class _Backend:
    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""

    def __init__(self, name):
        self.name, self.old = name, None

    def __enter__(self):
341-    ("flag", OLD_FLAG, {**NEW_FLAG, "category": "x"}, True),
342-    ("flag", OLD_FLAG, {**NEW_FLAG, "evidence": [{"text": "Q2"}]}, True),
343-    ("flag", OLD_FLAG, {**NEW_FLAG, "state": "needs_review"}, True),
344-    ("flag", OLD_FLAG, {**NEW_FLAG, "days": 40, "type": "causation"}, False),       # computed numbers moved: the existing reset path decides, not this compare
345-])
346:def test_disagrees_table(kind, old, new, expected):
347-    assert PL._disagrees(kind, old, new) is expected
348-
349-
350-@pytest.mark.parametrize("kind,old,new,expected", [
351-    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["LLM_FAILED_AFTER_RETRIES"]}, "writing the entries"),
352-    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["FIXTURE_MISS"]}, "writing the entries"),
353-    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["SCHEMA_INVALID"]}, "writing the entries"),
354-    ("entry", {"summary": "S", "excerpt": "Q"}, {"state": "rejected", "reasons": ["SUMMARY_NOT_IN_QUOTE"]}, None),            # the model answered; undecided entries take the new check result
355-    ("entry", {"summary": None, "excerpt": None}, {"state": "rejected", "reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),      # nothing stored to keep
356-    ("entry", {"summary": "S", "excerpt": None}, {"state": "rejected", "reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),
357-    ("flag", {"state_reasons": ["LEXICON_ONLY"]}, {"reasons": ["LLM_FAILED_AFTER_RETRIES"]}, "finding the flags"),
358-    ("flag", {"state_reasons": ["LEXICON_ONLY"]}, {"reasons": ["FIXTURE_MISS"]}, "finding the flags"),
359-    ("flag", {"state_reasons": ["LLM_FAILED_AFTER_RETRIES"]}, {"reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),               # already a failure: nothing better stored
360-    ("flag", {"state_reasons": ["FIXTURE_MISS"]}, {"reasons": ["LLM_FAILED_AFTER_RETRIES"]}, None),
361-    ("amount", {"ladder": {"judge": {"verdict": "agree"}}}, {"ladder": {"judge": {"verdict": "unavailable"}}}, "the second check"),
362-    ("amount", {"ladder": {"judge": {"verdict": "unavailable"}}}, {"ladder": {"judge": {"verdict": "unavailable"}}}, None),
363-    ("amount", {"ladder": {"judge": None}}, {"ladder": {"judge": {"verdict": "unavailable"}}}, None),
364-    ("amount", {"ladder": {"judge": {"verdict": "agree"}}}, {"ladder": {"judge": {"verdict": "agree"}}}, None),
365-])
366-def test_degrades_table(kind, old, new, expected):
367-    assert PL._degrades(kind, old, new) == expected
368-
369-
370-def test_failed_and_different_are_counted_apart(tmp_path):
371-    """Extract down (9 entries kept) and the model no longer proposing the corroborating flag (1 decided flag differs): two sentences, each with its own count."""
372-    conn, cid = completed(tmp_path)
373-    rerun(conn, cid, extract=down("extract"), flags={"flags": []})
374-    assert case_error(conn, cid)[1]["message"] == (
375-        "The AI step failed for 9 items (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. "
376-        "The re-run gave a different result for 1 item you had already decided; your decision and the earlier result were kept, and each item carries a note." + TAIL)
"""T-146 round 3: ONE rule for every stage. A re-run never lowers or replaces a decided item (accepted, dismissed, edited), whatever fails or whatever the new run's
checks say. When the new output for a decided item differs from it or fails a check, the decided item is kept whole, carries a visible note, and the case reads
run_partial with an honest message (the exact text is pinned here). Paths: flag step down, summary-in-quote fails on the new extract, extract down, judge down,
the deadline, and a re-run with nothing to keep."""
import json

import pytest
from app.backend import pipeline as PL, present
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record

TAIL = " Run it again to retry."
DECIDED = ("e1", "e2", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7")


def down(step):
    return AU.LLMFailed(f"{step} down", last_error="TIMEOUT")


def model_flag(user):
    """A model flag for record 3 with the same quote as the lexicon flag f_r3_1: the two corroborate (origin lexicon+llm, verified)."""
    return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="Patient reports low back pain in 2023, resolved.")] if which_record(user)[0] == 3 else []}


def _no_calls(v):
    return {a: _no_calls(b) for a, b in v.items() if a not in ("call_id", "rerun_note")} if isinstance(v, dict) else v


def full(conn, cid):
    """Every stored column of every item, but not `ladder.rerun_note` (checked on its own) and not call ids (every re-run numbers its calls afresh; they are compared on
    the kept e1 in test_kept_rows_keep_their_original_call_ids)."""
    return {k: {i["id"]: {c: _no_calls(v) for c, v in i.items() if c != "updated_at"} for i in DB.list_items(conn, cid, k)} for k in ("entry", "amount", "flag")}


def completed(tmp_path, decide=True):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    assert PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 1.0)["status"] == "done"
    assert DB.get_item(conn, "f_r3_1")["origin"] == "lexicon+llm" and DB.get_item(conn, "f_r3_1")["state"] == "verified"
    if decide:
        for i in ("e1", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7"):      # a corroborated flag, a lexicon-only flag, a code flag, an entry, an amount
            DB.apply_review(conn, i, "accept", now=2.0, case=cid)
        DB.apply_review(conn, "e2", "dismiss", now=2.0, case=cid)
    return conn, cid


def rerun(conn, cid, **script):
    script.setdefault("flags", model_flag)
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 3.0)


def case_error(conn, cid):
    c = DB.get_case(conn, cid)
    return c["status"], (json.loads(c["error"]) if c["error"] else None)


def note(conn, cid, i):
    return (DB.get_item(conn, i, cid)["ladder"] or {}).get("rerun_note")


def assert_notes(conn, cid, ids, kind, step):
    for i in ids:
        n = note(conn, cid, i)
        assert n and n["kind"] == kind and n["step"] == step, (i, n)
        assert present.item_view(conn, cid, i)["rerun_note"] == n["message"]      # shown on the item, not only stored
    for i in set(DECIDED) - set(ids):
        assert note(conn, cid, i) is None, i


# ---- the flag step is down
def test_flag_step_down_keeps_every_decided_flag_whole_and_notes_it(tmp_path):
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    out = rerun(conn, cid, flags=down("flags"))
    assert out["status"] == "done"
    assert full(conn, cid) == before                      # 10 flags: origin, state, reasons and judge answer all as stored
    f = DB.get_item(conn, "f_r3_1", cid)
    assert (f["state"], f["origin"], f["state_reasons"], f["review_status"]) == ("verified", "lexicon+llm", [], "accepted")
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:47:53.547Z

**tool call — Bash**
````
{
 "command": "sed -n 405,440p app/backend/pipeline.py; grep -n \"def run_conflict_pass\" -A45 app/backend/flags.py | head -90; grep -n \"failed_steps\" app/backend/*.py app/llm/*.py | head -30; grep -n \"RUN_FAILED\" -B6 -A6 app/backend/trace.py | head -60"
}
````

### User / tool · 2026-11-02T14:47:53.664Z

**tool result**
````
    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
    It names how many items and which steps, and says exactly what was kept."""
    failed, differed = [k for k in kept if k[2] == "failed"], [k for k in kept if k[2] == "disagreed"]
    parts = []
    if failed:
        parts.append(f"The AI step failed for {_items(len(failed))} ({' and '.join(sorted({c for _, c, _ in failed}))}) on this run. Their earlier results and every "
                     "decision of yours were kept unchanged.")
    if differed:
        parts.append(f"The re-run gave a different result for {_items(len(differed))} you had already decided; your decision and the earlier result were kept, "
                     "and each item carries a note.")
    if empty:
        parts.append(f"The AI step also failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) with no earlier result to keep." if kept else
                     f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
    return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None


def _noting(raw_call, failed_steps: list):
    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
    caller's own handling; this only lets the run say which steps were down."""
    def call(step, system, user, schema, *, item_id=None):
        try:
            return raw_call(step, system, user, schema, item_id=item_id)
        except (AU.LLMFailed, P.FixtureMiss):
            failed_steps.append(step)
            raise
    return call


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
299:def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
300-    """Conflicts between records (T-094, R-CO-7). CODE proposes the candidate pairs (conflict_candidates.py: a stated plan against a later early end,
301-    a denial of prior problems against a prior-condition sentence; frequency x duration is multiplied out, so '2x/week for 6 weeks' agrees with
302-    '12 visits' and is never asked about). The model's only job is the classification of each candidate, by J3 (judge_conflict_v6). There is no
303-    open-ended search call, so the set of candidates cannot vary between runs.
304-    Policy for the answer: conflict -> flag (verified when the other checks hold); unsure / judge failed -> flag stays needs_review;
305-    benign -> the could-not-verify tray (state rejected, JUDGE_DISAGREES), shown to the paralegal, never exported. For a denial, candidates are
306-    judged one at a time in record order and the first confirmed conflict stands (later ones are not asked)."""
307-    by_n = {r["n"]: r for r in records}
308-    cands = CC.candidates(records)
309-    flags, settled = [], set()
310-    for i, c in enumerate(cands, 1):
311-        f = _candidate_flag(c, by_n, any_tagged, f"f_cx{i}")
312-        flags.append(f)
313-        if c["group"] in settled and c["rule"] == "history_denial":
314-            f["_skip"] = True
315-            continue
316-        if f["state"] == "rejected":
317-            continue
318-        _judge_one(f, i - 1, call=call, case_text=case_text)
319-        if c["rule"] == "history_denial" and f["state"] != "rejected" and f["ladder"]["judge"]["verdict"] == "conflict":
320-            settled.add(c["group"])
321-    return [{k: v for k, v in f.items() if k not in ("_skip", "_group")} for f in flags if not f.get("_skip")]
322-
323-
324-# ------------------------------------------------------------------ rung 2 for flags (J3 / J4)
325-def _judge_one(f: dict, i: int, *, call, case_text: str = "") -> None:
326-    item = f.get("id") or f"f{i}"
327-    nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
328-    try:
329-        if f["type"] == "conflict":
330-            if not f.get("excerpt_b"):
331-                return
332-            v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, category=f["category"])
333-            step, pv = "j3", JUDGE_PROMPT["j3"]
334-        elif f["origin"] in ("llm", "both"):
335-            v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
336-            step, pv = "j4", JUDGE_PROMPT["j4"]
337-        else:
338-            return
339-    except P.FixtureMiss:
340-        f["_stage"]["fixture_miss"] = True
341-        step = "j3" if f["type"] == "conflict" else "j4"
342-        v, cid, reason, pv = "unavailable", None, "NONE", JUDGE_PROMPT[step]
343-    f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
344-    f["_stage"]["judge"] = judges.to_ladder(step, v)
app/backend/pipeline.py:421:def _noting(raw_call, failed_steps: list):
app/backend/pipeline.py:428:            failed_steps.append(step)
app/backend/pipeline.py:436:    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
app/backend/pipeline.py:553:                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
app/backend/review.py:143:    return {"item_id": item_id, "reason_code": first, "step_id": CODE_CHECK_STEP[first], "failed_steps": [CODE_CHECK_STEP[c] for c in fails],
app/backend/review.py:172:    detail = {"item_id": item_id, "reason_code": "CHARGE_TEXT_IN_ENTRY", "step_id": "charge_text", "failed_steps": ["charge_text"], "tokens": [],
app/backend/trace.py:506:    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
app/backend/trace.py:516:        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
42-    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
43-    "EDIT_NOT_CONFIRMED_ITEM": "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.",
44-    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
45-    "EDIT_NOT_CONFIRMED": "An edited entry is still marked Needs review; it stays out of the letter until you compare it with the quote and accept it.",
46-    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
47-    "RUN_IN_PROGRESS": "The AI run is still going.",
48:    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
49-    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
50-    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
51-    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
52-    "CODE_CHECK_FAILED_AI": "This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
53-    "CODE_CHECK_FAILED": "You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.",
54-    "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
--
1170-    cx = cx or _Cx(conn, case_id, False)
1171-    rv = rv or present.review_view(conn, case_id)
1172-    out = []
1173-    if cx.running:
1174-        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
1175-    if cx.case["status"] == "failed":
1176:        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
1177-    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
1178-    if cx.ran and not cx.running:
1179-        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
1180-    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
1181-        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
1182-    return out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:00.314Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"conflicts\" reviews/T-146-staff-engineer-r3.md reviews/T-146-staff-engineer-r2.md | cut -c1-400; grep -n \"conflict\" tests/unit/test_t146_r3_decided_items_never_lowered.py | head -20; ls /private/tmp/claude-501/*/*/scratchpad 2>/dev/null | head; grep -n \"def sample_script\" -A40 tests/unit/_fakes.py | head -80"
}
````

### User / tool · 2026-11-02T14:48:00.612Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:07.681Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/p1.py <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import *\nfrom app.backend import trace\ndef show(tag, conn, cid):\n    print(tag, case_error(conn,cid), [b['reason_code'] for b in trace.export_blockers(conn,cid)][:3])\nimport tempfile, pathlib\nd=pathlib.Path(tempfile.mkdtemp())\nconn, cid = completed(d)\nprint([ (i['id'],i['state'], (i['ladder'].get('judge') or {}).get('verdict')) for i in DB.list_items(conn,cid,'flag') if i['id'].startswith('f_cx')])\nbefore=full(conn,cid)\nrerun(conn,cid,j3=down(\"j3\"))\nshow('rerun j3 down',conn,cid); print(full(conn,cid)==before)\n# first run j3 down\nconn2=DB.connect(str(d/'x.sqlite')); cid2=DB.create_case(conn2,G.raw('sample'),now=0.0)\nPL.run_pipeline(conn2,cid2,G.raw('sample'),call=FakeCall(sample_script(j3=down('j3'),flags=model_flag)),now=lambda:1.0)\nshow('first j3 down',conn2,cid2)\nprint([ (i['id'],i['state'], (i['ladder'].get('judge') or {}).get('verdict')) for i in DB.list_items(conn2,cid2,'flag') if i['id'].startswith('f_cx')])\nEOF\n.venv/bin/python -I /private/tmp/claude-501/p1.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T14:48:08.682Z

**tool result**
````
[('f_cx1', 'verified', 'conflict')]
rerun j3 down ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED']
True
first j3 down ('ready', None) ['NOTHING_ACCEPTED']
[('f_cx1', 'needs_review', 'unavailable')]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:15.216Z

**tool call — Bash**
````
{
 "command": "grep -n \"def run_j3_meta\" -A40 app/backend/judges.py | head -70; grep -n \"class FixtureMiss\\|class LLMFailed\\|class SchemaInvalid\" -r app | head"
}
````

### User / tool · 2026-11-02T14:48:15.339Z

**tool result**
````
57:def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
58-    """`category` (the flag category the software proposed) selects the decision rule in judge_conflict_v6 (T-075, T-094)."""
59-    return _run("j3", "judge_conflict_v6", schemas.Judge3, [excerpt_a, excerpt_b], [f"FLAG CATEGORY: {category}"] if category else [],
60-                call, nonce, item_id)
61-
62-
63-def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
64-    return _run("j4", "judge_flag_v3", schemas.Judge4, [excerpt],
65-                [f"FLAG TYPE: {flag_type}", f"FLAG CATEGORY: {category}"], call, nonce, item_id)
66-
67-
68-def run_j1(summary, excerpt, label, *, call, nonce=None, item_id=None):
69-    return run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)[0]
70-
71-
72-def run_j2(excerpt, raw_amount, code_class, *, call, nonce=None, item_id=None):
73-    return run_j2_meta(excerpt, raw_amount, code_class, call=call, nonce=nonce, item_id=item_id)[0]
74-
75-
76-def run_j3(excerpt_a, excerpt_b, *, call, nonce=None, item_id=None, category=None):
77-    return run_j3_meta(excerpt_a, excerpt_b, call=call, nonce=nonce, item_id=item_id, category=category)[0]
78-
79-
80-def run_j4(excerpt, flag_type, category, *, call, nonce=None, item_id=None):
81-    return run_j4_meta(excerpt, flag_type, category, call=call, nonce=nonce, item_id=item_id)[0]
82-
83-
84-_TO_LADDER = {
85-    "j1": {"supported": "supported", "partially": "partially", "unsupported": "unsupported"},
86-    "j2": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
87-    "j3": {"conflict": "supported", "benign": "disagrees", "unsure": "unsure"},
88-    "j4": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
89-}
90-
91-
92-def to_ladder(step: str, verdict: str) -> str:
93-    """Map a judge's own enum to the compose_state vocabulary. Only the positive verdict becomes 'supported';
94-    unknown values become 'unsure' and 'unavailable' stays 'unavailable' (never positive by accident)."""
95-    if verdict == "unavailable":
96-        return "unavailable"
97-    return _TO_LADDER[step].get(verdict, "unsure")
app/llm/_types.py:11:class FixtureMissing(LLMError):
app/llm/audited.py:32:class LLMFailed(Exception):
app/llm/audited.py:44:class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:22.208Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/p2.py <<'EOF'\nimport sys, tempfile, pathlib\nsys.path.insert(0,'.')\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import *\nfrom app.backend import trace\nfrom app.llm import providers as P\ndef show(tag, conn, cid):\n    print(tag, case_error(conn,cid), [b['reason_code'] for b in trace.export_blockers(conn,cid)][:3], flush=True)\nfor name, exc in [(\"llmfailed\", down(\"j3\")), (\"fixturemiss\", AU.LLMFailedFixtureMiss(\"x\") if hasattr(AU,'LLMFailedFixtureMiss') else None), (\"raw-fixturemiss\", P.FixtureMiss(\"x\")), (\"runtime\", RuntimeError(\"boom\"))]:\n    for dec in (False, True):\n        d=pathlib.Path(tempfile.mkdtemp())\n        conn,cid=completed(d, decide=dec)\n        try:\n            rerun(conn,cid,j3=exc); show(f\"{name} decided={dec}\",conn,cid)\n        except Exception as e:\n            print(name, dec, \"RAISED\", type(e).__name__, case_error(conn,cid))\n        print(\"  f_cx1\", DB.get_item(conn,'f_cx1',cid)['state'], (DB.get_item(conn,'f_cx1',cid)['ladder'].get('judge') or {}).get('verdict'))\nEOF\n.venv/bin/python -I /private/tmp/claude-501/p2.py 2>&1 | tail -20; grep -n \"FixtureMiss\" app/llm/providers.py | head -3; sed -n 25,50p app/llm/audited.py"
}
````

### User / tool · 2026-11-02T14:48:22.561Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/p2.py", line 5, in <module>
    from app.llm import providers as P
ImportError: cannot import name 'providers' from 'app.llm' (/Users/arsis/zlayt-pm-project/app/llm/__init__.py). Did you mean: 'provider'?
ugrep: warning: app/llm/providers.py: No such file or directory
_RETRY_NOTES = (
    "",
    "\n\n[RETRY 1 of 2: your previous reply was unusable. Reply with exactly one JSON object that satisfies the schema, with no prose and no code fence.]",
    "\n\n[FINAL RETRY: reply with ONLY the raw JSON object, no markdown, no commentary, every required key present, no extra keys.]",
)


class LLMFailed(Exception):
    """The LLM layer gave up (every attempt failed, or a fixture was missing). `last_error` is the last attempt's failure code
    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
    code = "LLM_FAILED_AFTER_RETRIES"
    last_error = "LLM_ERROR"

    def __init__(self, *args, last_error: str = None):
        super().__init__(*args)
        if last_error:
            self.last_error = last_error


class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""

    last_error = "FIXTURE_MISS"

    def __init__(self, prompt_hash: str = ""):
        P.FixtureMissing.__init__(self, prompt_hash)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:24.830Z

**tool call — Bash**
````
{
 "command": "sed -i 's/^from app.llm import providers as P$/from app.llm import provider as P/; s/P.FixtureMiss(\"x\")/P.FixtureMissing(\"x\")/' /private/tmp/claude-501/p2.py && .venv/bin/python -I /private/tmp/claude-501/p2.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T14:48:24.928Z

**tool result (error)**
````
Exit code 1
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/p2.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:27.351Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/^from app.llm import providers as P$/from app.llm import provider as P/; s/P.FixtureMiss(\"x\")/P.FixtureMissing(\"x\")/' /private/tmp/claude-501/p2.py && .venv/bin/python -I /private/tmp/claude-501/p2.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T14:48:29.795Z

**tool result**
````
llmfailed decided=False ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED', 'NOTHING_ACCEPTED']
  f_cx1 verified conflict
llmfailed decided=True ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED']
  f_cx1 verified conflict
fixturemiss decided=False ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED', 'NOTHING_ACCEPTED']
  f_cx1 verified conflict
fixturemiss decided=True ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED']
  f_cx1 verified conflict
raw-fixturemiss decided=False ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (finding the flags) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED', 'NOTHING_ACCEPTED']
  f_cx1 verified conflict
raw-fixturemiss decided=True ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 1 item (finding the flags) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.'}) ['RUN_FAILED']
  f_cx1 verified conflict
runtime False RAISED RuntimeError ('running', None)
  f_cx1 verified conflict
runtime True RAISED RuntimeError ('running', None)
  f_cx1 verified conflict
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:40.806Z

**tool call — Bash**
````
{
 "command": "grep -rn -i \"conflicts.step\\|conflict step\\|conflicts step\" board/cards/T-146.md memory/*.md reviews/T-146*.md board/activity.jsonl 2>/dev/null | cut -c1-500 | tail -12"
}
````

### User / tool · 2026-11-02T14:48:40.977Z

**tool result**
````
board/cards/T-146.md:58:- 2026-11-02T14:47:33Z orchestrator: §7.4 at cap: bounded fix-up + scoped check. (1) The keep-and-note rule compares the whole ladder (code checks, judge verdict, reasons), not only the state: a decided item whose checks get worse inside needs_review (agree->disagree, a new reason) is kept with a visible note, and the case is run_partial; (2) a conflicts-step failure makes the gate RUN_FAILED like every other step. Minors only if cheap.
reviews/T-146-staff-engineer-r2.md:27:    "re-run probes with full-row compare: j1+j2 down, all four judges down, flags step down, conflicts step down, deadline at extract/verify/judge_entries/amounts/conflicts/flags",
board/activity.jsonl:3751:{"ts": "2026-11-02T14:47:33Z", "event": "note", "agent": "orchestrator", "card": "T-146", "text": "§7.4 at cap: bounded fix-up + scoped check. (1) The keep-and-note rule compares the whole ladder (code checks, judge verdict, reasons), not only the state: a decided item whose checks get worse inside needs_review (agree->disagree, a new reason) is kept with a visible note, and the case is run_partial; (2) a conflicts-step failure makes the gate RUN_FAILED like every othe
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:49.697Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/p3.py <<'EOF'\nimport sys, tempfile, pathlib\nsys.path.insert(0,'.')\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import *\nfrom app.backend import trace\ndef show(tag, conn, cid):\n    c=case_error(conn,cid)\n    print(tag, c[0], (c[1] or {}).get('message','')[:110], [b['reason_code'] for b in trace.export_blockers(conn,cid)][:2], flush=True)\ndef first(**sc):\n    d=pathlib.Path(tempfile.mkdtemp()); conn=DB.connect(str(d/'x.sqlite')); cid=DB.create_case(conn,G.raw('sample'),now=0.0)\n    PL.run_pipeline(conn,cid,G.raw('sample'),call=FakeCall(sample_script(flags=model_flag,**sc)),now=lambda:1.0); return conn,cid\nfor st in (\"j1\",\"j2\",\"j3\",\"j4\",\"flags\",\"extract\"):\n    conn,cid=first(**{st:down(st)}); show(f\"first {st} down\",conn,cid)\n    rerun(conn,cid,**{st:down(st)}); show(f\"  then {st} down again\",conn,cid)\n    rerun(conn,cid,**{st:down(st)}); show(f\"  third\",conn,cid)\nEOF\n.venv/bin/python -I /private/tmp/claude-501/p3.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T14:48:51.726Z

**tool result**
````
first j1 down ready  ['NOTHING_ACCEPTED']
  then j1 down again failed The AI step failed for 9 items (the second check) on this run, and there is no earlier result to keep. Run it  ['RUN_FAILED', 'NOTHING_ACCEPTED']
  third failed The AI step failed for 9 items (the second check) on this run, and there is no earlier result to keep. Run it  ['RUN_FAILED', 'NOTHING_ACCEPTED']
first j2 down ready  ['NOTHING_ACCEPTED']
  then j2 down again failed The AI step failed for 3 items (the second check) on this run, and there is no earlier result to keep. Run it  ['RUN_FAILED', 'NOTHING_ACCEPTED']
  third failed The AI step failed for 3 items (the second check) on this run, and there is no earlier result to keep. Run it  ['RUN_FAILED', 'NOTHING_ACCEPTED']
first j3 down ready  ['NOTHING_ACCEPTED']
  then j3 down again failed The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep. Run it a ['RUN_FAILED', 'NOTHING_ACCEPTED']
  third failed The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep. Run it a ['RUN_FAILED', 'NOTHING_ACCEPTED']
first j4 down ready  ['NOTHING_ACCEPTED']
  then j4 down again failed The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep. Run it a ['RUN_FAILED', 'NOTHING_ACCEPTED']
  third failed The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep. Run it a ['RUN_FAILED', 'NOTHING_ACCEPTED']
Traceback (most recent call last):
  File "/private/tmp/claude-501/p3.py", line 12, in <module>
    conn,cid=first(**{st:down(st)}); show(f"first {st} down",conn,cid)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/p3.py", line 10, in first
    PL.run_pipeline(conn,cid,G.raw('sample'),call=FakeCall(sample_script(flags=model_flag,**sc)),now=lambda:1.0); return conn,cid
                                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: tests.unit._fakes.sample_script() got multiple values for keyword argument 'flags'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:48:56.858Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _store_run_checks\" -A25 app/backend/pipeline.py; grep -rn \"run_checks\\|conflicts_check\\|\\\"skipped\\\"\\|'skipped'\" app/backend/*.py | grep -v \"^app/backend/pipeline.py\" | head -20"
}
````

### User / tool · 2026-11-02T14:48:57.065Z

**tool result**
````
161:def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
162-    """T-141 r2: what the conflict checks did on THIS case (language routing, whether the pair stage ran), kept in the case config so GET case `checks`
163-    is computed from the run, not a constant. stage: 'pending' (ingested, or the run has started), 'ran', 'skipped' (deadline before the stage)."""
164-    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
165-    cfg["run_checks"] = CC.run_summary(recs, stage=stage)
166-    DB.update_case(conn, cid, config_json=cfg)
167-
168-
169-def _item_record_ids(item: dict) -> list:
170-    return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
171-
172-
173-def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
174-    """T-129 r2: a record number now names different text (a re-run after the numbering changed, or a model split that moved). A decision the paralegal made on an item
175-    that cites such a record was made on other text, so it goes back to pending (the review event keeps what it was); the run then rebuilds or removes the item."""
176-    if not moved:
177-        return
178-    for kind in ("entry", "amount", "flag"):
179-        for it in DB.list_items(conn, cid, kind):
180-            if it["review_status"] != "pending" and moved & set(_item_record_ids(it)):
181-                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
182-
183-
184-def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
185-    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
186-    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
app/backend/present.py:349:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
app/backend/trace.py:18:PASS, FAIL, SKIPPED, PENDING = "pass", "fail", "skipped", "pending"
app/backend/conflict_candidates.py:251:    records. stage: 'pending' (ingested or running), 'ran', or 'skipped' (the run deadline passed before the conflict stage). {conflicts_stage,
app/backend/conflict_candidates.py:283:            if stage == "skipped":
app/backend/conflict_candidates.py:301:    return {"conflict_types": [t for t in CONFLICT_LABELS if t not in whole], "labels": dict(CONFLICT_LABELS), "skipped": skipped,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:49:15.873Z

**tool call — Bash**
````
{
 "command": "grep -n \"run_pipeline\" app/backend/*.py | grep -v \"^app/backend/pipeline.py:.*def \" | head; "
}
````

### User / tool · 2026-11-02T14:49:15.971Z

**tool result**
````
app/backend/api.py:356:            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
app/backend/pipeline.py:628:            out = run_pipeline(conn, cid, text, call=call)
app/backend/pipeline.py:695:        out = run_pipeline(conn, cid, raw)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:49:17.533Z

**tool call — Bash**
````
{
 "command": "sed -n 335,385p app/backend/api.py; sed -n 618,640p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T14:49:17.652Z

**tool result**
````
            get_case(c, token)
            DB.update_case(c, token, name=case_list.clean_title(b["title"]) or None)
            case = DB.get_case(c, token)
            return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
        finally:
            c.close()

    @app.delete("/api/cases/{token}", status_code=204)
    def delete_case(token: str):
        c = conn()
        try:
            get_case(c, token)
            DB.delete_case(c, token)
        finally:
            c.close()
        return Response(status_code=204)

    def _run_thread(token, raw):
        c = conn()
        try:
            mod = pipeline_mod()
            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
            if DB.get_case(c, token)["status"] == "running":
                DB.update_case(c, token, status="ready", stage="finalize", run_finished_at=time.time())
        except Exception as e:                                   # code only: no message text from the pipeline
            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
        finally:
            c.close()
            runs.pop(token, None)

    @app.post("/api/cases/{token}/run", status_code=202)
    async def run_case(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
            if decided and b.get("confirm_rerun") is not True:
                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
            now = time.time()
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
    return conn, cid, AU.make_call(conn, cid)


def run_case(text: str, backend: str = None) -> dict:
    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
            out = run_pipeline(conn, cid, text, call=call)
        view = case_view(out)
        conn.close()
        return view


def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
    """Judge 1 on one (summary, excerpt, label): 'supported' | 'partially' | 'unsupported' | 'unavailable'. A missing fixture or a failed call
    is 'unavailable', never a pass."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, excerpt)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:49:34.889Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def _ladder\" -A14 app/backend/pipeline.py; sed -n 300,345p tests/unit/test_t146_r3_decided_items_never_lowered.py; cat > /private/tmp/claude-501/p4.py <<'EOF'\nimport sys, tempfile, pathlib, json\nsys.path.insert(0,'.')\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import *\nconn,cid=completed(pathlib.Path(tempfile.mkdtemp()))\nfor i in (\"e1\",\"a2\",\"f_r6_1\",\"f_cx1\",\"f_r3_1\"):\n    r=DB.get_item(conn,i,cid); print(i, r['state'], r['state_reasons'], json.dumps(r['ladder'])[:600])\nEOF\n.venv/bin/python -I /private/tmp/claude-501/p4.py"
}
````

### User / tool · 2026-11-02T14:49:36.026Z

**tool result**
````
30:def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
31-    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
32-            "human": {"action": None, "edited_text": None, "at": None}, "state": state}
33-
34-
35-def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
36-    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
37-    bad = [e for e in evidence if e.get("start") is not None and case_text[e["start"]:e["end"]] != e["text"]]
38-    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
39-           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons,
40-           "translated": any(language.translated_record(rec_by_n[n]) for n in nos if n in rec_by_n)}      # D-050
41-    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
42-    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
43-        ctx["date_status"] = "ambiguous"
44-    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
@pytest.mark.parametrize("miss", [False, True])
def test_a_pending_model_only_flag_survives_a_down_flag_step(tmp_path, miss):
    """The flag step cannot tell which stored flags are stale when it is down: nothing pending is deleted (a model-only flag has no new row to compare)."""
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)

    def only_model(user):
        return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="CT head negative.")] if which_record(user)[0] == 2 else []}
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=only_model)), now=lambda: 1.0)
    assert DB.get_item(conn, "f_r2_1", cid)["origin"] == "llm"
    before = full(conn, cid)["flag"]
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=PL.P.FixtureMiss("x") if miss else down("flags"))), now=lambda: 3.0)
    assert full(conn, cid)["flag"]["f_r2_1"] == before["f_r2_1"]
    assert "finding the flags" in case_error(conn, cid)[1]["message"]
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 4.0)      # a good run that no longer finds it removes the pending stale flag
    assert "f_r2_1" not in {f["id"] for f in DB.list_items(conn, cid, "flag")}


# ---- the compare itself, branch by branch
OLD_ENTRY = {"summary": "S", "excerpt": "Q", "date_iso": "2026-01-01", "state": "verified"}
OLD_AMOUNT = {"text": "$10", "value_cents": 1000, "kind": "charge", "state": "verified"}
OLD_FLAG = {"type": "pre_existing", "category": "pre_existing", "evidence": [{"text": "Q"}], "computed": {"from_date": None, "to_date": None, "days": None}, "state": "verified"}
NEW_FLAG = {"type": "pre_existing", "category": "pre_existing", "evidence": [{"text": "Q"}], "from_date": None, "to_date": None, "days": None, "state": "verified"}


@pytest.mark.parametrize("kind,old,new,expected", [
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, False),
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "needs_review"}, True),            # lower state
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "rejected"}, True),
    ("entry", {**OLD_ENTRY, "state": "needs_review"}, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, False),      # a better state is not a disagreement
    ("entry", OLD_ENTRY, {"summary": "S2", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, True),               # each content field alone
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q2", "date": "2026-01-01", "state": "verified"}, True),
    ("entry", OLD_ENTRY, {"summary": "S", "excerpt": "Q", "date": "2026-01-02", "state": "verified"}, True),
    ("entry", {**OLD_ENTRY, "state": "rejected", "summary": None}, {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "verified"}, False),   # a stub has nothing to lower
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1000, "cls": "charge", "state": "verified"}, False),
    ("amount", OLD_AMOUNT, {"text": "$11", "cents": 1000, "cls": "charge", "state": "verified"}, True),
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1100, "cls": "charge", "state": "verified"}, True),
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1000, "cls": "estimate", "state": "verified"}, True),
    ("amount", OLD_AMOUNT, {"text": "$10", "cents": 1000, "cls": "charge", "state": "needs_review"}, True),
    ("flag", OLD_FLAG, NEW_FLAG, False),
    ("flag", OLD_FLAG, {**NEW_FLAG, "type": "causation"}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "category": "x"}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "evidence": [{"text": "Q2"}]}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "state": "needs_review"}, True),
    ("flag", OLD_FLAG, {**NEW_FLAG, "days": 40, "type": "causation"}, False),       # computed numbers moved: the existing reset path decides, not this compare
])
e1 verified [] {"backend": "fixture", "code_checks": {"date_provider_from_header": true, "excerpt_verbatim": true, "excerpt_whole_sentence": true, "highlight_found": true, "qualifier_carried": true, "summary_tokens_not_in_excerpt": []}, "generator": {"call_id": "call1", "model": "claude-sonnet-5-5", "output": {"excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.", "summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER."}, "pr
a2 needs_review ['AMOUNT_RATE_NOT_TOTALED'] {"backend": "fixture", "code_checks": {"amount_in_text": true, "classified_by": "code:amounts"}, "generator": null, "human": {"action": null, "at": null, "edited_text": null}, "item_id": "a2", "judge": {"call_id": "call20", "model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "reason_code": "NONE", "verdict": "agree"}, "state": "needs_review"}
f_r6_1 needs_review ['LEXICON_ONLY'] {"backend": "fixture", "code_checks": {"classified_by": "lexicon+llm", "excerpt_verbatim": true, "highlight_found": true}, "generator": null, "item_id": "f_r6_1", "judge": null, "state": "needs_review"}
f_cx1 verified [] {"backend": "fixture", "code_checks": {"arithmetic": "record 3: 2 per week x 6 weeks = 12 visits; record 4: 12 visits", "candidate_rule": "plan_vs_outcome", "classified_by": "code:conflict_candidate+j3", "excerpt_verbatim": true}, "generator": null, "item_id": "f_cx1", "judge": {"call_id": "call22", "model": "claude-haiku-5-5", "prompt_version": "judge_conflict_v6", "reason_code": "NONE", "verdict": "conflict"}, "state": "verified"}
f_r3_1 verified [] {"backend": "fixture", "code_checks": {"classified_by": "lexicon+llm", "excerpt_verbatim": true, "highlight_found": true}, "generator": null, "item_id": "f_r3_1", "judge": {"call_id": "call32", "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "reason_code": "NONE", "verdict": "agree"}, "state": "verified"}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:50:14.748Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_t146_r4_ladder_compare_and_conflicts.py <<'EOF'\n\"\"\"T-146 r4 (§7.4 fix-up). (1) The keep-and-note compare reads the whole ladder, not only the state: a decided item whose checks get worse INSIDE the same state (a new\nreason, a second-check answer that moves from positive to negative, a code check that turns false) is kept whole with a note, and the case reads run_partial.\n(2) A failure in the conflicts step (judge 3) makes the case failed and the export gate RUN_FAILED, like every other step.\"\"\"\nimport pytest\nfrom app.backend import pipeline as PL, trace\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import (OLD_AMOUNT, OLD_ENTRY, OLD_FLAG, NEW_FLAG, TAIL, assert_notes, case_error, completed, down, full,\n                                                                  model_flag, note, rerun)\n\n\ndef blockers(conn, cid):\n    return [b[\"reason_code\"] for b in trace.export_blockers(conn, cid)]\n\n\n# ---- the compare, equal-rank rows (state needs_review on both sides)\nNR_AMOUNT = {**OLD_AMOUNT, \"state\": \"needs_review\", \"state_reasons\": [\"AMOUNT_RATE_NOT_TOTALED\"], \"ladder\": {\"judge\": {\"verdict\": \"agree\"}, \"code_checks\": {\"amount_in_text\": True}}}\nNEW_AMT = {\"text\": \"$10\", \"cents\": 1000, \"cls\": \"charge\", \"state\": \"needs_review\", \"reasons\": [\"AMOUNT_RATE_NOT_TOTALED\"],\n           \"ladder\": {\"judge\": {\"verdict\": \"agree\"}, \"code_checks\": {\"amount_in_text\": True}}}\nNR_ENTRY = {**OLD_ENTRY, \"state\": \"needs_review\", \"state_reasons\": [\"QUALIFIER_DROPPED\"],\n            \"ladder\": {\"judge\": {\"verdict\": \"partially\"}, \"code_checks\": {\"excerpt_verbatim\": True, \"summary_tokens_not_in_excerpt\": []}}}\nNEW_ENT = {\"summary\": \"S\", \"excerpt\": \"Q\", \"date\": \"2026-01-01\", \"state\": \"needs_review\", \"reasons\": [\"QUALIFIER_DROPPED\"],\n           \"ladder\": {\"judge\": {\"verdict\": \"partially\"}, \"code_checks\": {\"excerpt_verbatim\": True, \"summary_tokens_not_in_excerpt\": []}}}\nNR_FLAG = {**OLD_FLAG, \"state\": \"needs_review\", \"state_reasons\": [\"LEXICON_ONLY\"], \"ladder\": {\"judge\": {\"verdict\": \"agree\"}, \"code_checks\": {\"excerpt_verbatim\": True}}}\nNEW_FL = {**NEW_FLAG, \"state\": \"needs_review\", \"reasons\": [\"LEXICON_ONLY\"], \"ladder\": {\"judge\": {\"verdict\": \"agree\"}, \"code_checks\": {\"excerpt_verbatim\": True}}}\n\n\ndef lad(judge=None, **checks):\n    return {\"judge\": {\"verdict\": judge} if judge else None, \"code_checks\": checks}\n\n\n@pytest.mark.parametrize(\"kind,old,new,expected\", [\n    (\"amount\", NR_AMOUNT, NEW_AMT, False),                                                                                    # identical: nothing changed\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"reasons\": [\"JUDGE_DISAGREES\", \"AMOUNT_RATE_NOT_TOTALED\"], \"ladder\": lad(\"disagree\", amount_in_text=True)}, True),     # the F1 repro\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"reasons\": [\"AMOUNT_RATE_NOT_TOTALED\", \"OCR_DERIVED\"]}, True),                          # a new reason alone\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"reasons\": []}, False),                                                                 # a reason gone is not worse\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"ladder\": lad(\"disagree\", amount_in_text=True)}, True),                                 # answer agree -> disagree, same reasons\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"ladder\": lad(\"unsure\", amount_in_text=True)}, True),\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"ladder\": lad(\"agree\", amount_in_text=False)}, True),                                   # a code check true -> false\n    (\"amount\", NR_AMOUNT, {**NEW_AMT, \"ladder\": {\"judge\": None, \"code_checks\": {\"amount_in_text\": True}}}, False),            # no new answer is not a negative answer\n    (\"amount\", {**NR_AMOUNT, \"ladder\": lad(\"disagree\", amount_in_text=True)}, {**NEW_AMT, \"ladder\": lad(\"agree\", amount_in_text=True)}, False),    # better\n    (\"amount\", {**NR_AMOUNT, \"ladder\": lad(\"unsure\", amount_in_text=True)}, {**NEW_AMT, \"ladder\": lad(\"disagree\", amount_in_text=True)}, False),   # was not positive: no answer was taken back\n    (\"entry\", NR_ENTRY, NEW_ENT, False),\n    (\"entry\", {**NR_ENTRY, \"ladder\": lad(\"supported\", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[])},\n     {**NEW_ENT, \"ladder\": lad(\"unsupported\", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[])}, True),\n    (\"entry\", NR_ENTRY, {**NEW_ENT, \"ladder\": lad(\"partially\", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[\"fracture\"])}, True),    # unsupported tokens appear\n    (\"entry\", NR_ENTRY, {**NEW_ENT, \"reasons\": [\"QUALIFIER_DROPPED\", \"DATE_UNCONFIRMED\"]}, True),\n    (\"flag\", NR_FLAG, NEW_FL, False),\n    (\"flag\", NR_FLAG, {**NEW_FL, \"reasons\": [\"LEXICON_ONLY\", \"JUDGE_DISAGREES\"], \"ladder\": lad(\"disagree\", excerpt_verbatim=True)}, True),\n    (\"flag\", NR_FLAG, {**NEW_FL, \"ladder\": lad(\"conflict\", excerpt_verbatim=True)}, False),                                   # agree and conflict are both positive\n    (\"flag\", {**NR_FLAG, \"ladder\": lad(\"conflict\", excerpt_verbatim=True)}, {**NEW_FL, \"ladder\": lad(\"benign\", excerpt_verbatim=True)}, True),\n    (\"flag\", NR_FLAG, {**NEW_FL, \"days\": 40, \"reasons\": [\"LEXICON_ONLY\", \"JUDGE_DISAGREES\"]}, False),                         # numbers moved: the reset path decides\n])\ndef test_disagrees_reads_the_whole_ladder(kind, old, new, expected):\n    assert PL._disagrees(kind, old, new) is expected\n\n\n# ---- end to end: the F1 repro (accepted or dismissed rate in needs_review, the second check flips)\n@pytest.mark.parametrize(\"action\", [\"accept\", \"dismiss\"])\ndef test_decided_needs_review_amount_survives_a_judge_that_now_disagrees(tmp_path, action):\n    conn, cid = completed(tmp_path)\n    a2 = DB.get_item(conn, \"a2\", cid)\n    assert (a2[\"state\"], a2[\"state_reasons\"], a2[\"ladder\"][\"judge\"][\"verdict\"]) == (\"needs_review\", [\"AMOUNT_RATE_NOT_TOTALED\"], \"agree\")\n    DB.apply_review(conn, \"a2\", action, now=2.5, case=cid)\n    before = full(conn, cid)\n    out = rerun(conn, cid, j2={\"verdict\": \"disagree\", \"reason_code\": \"NONE\"})\n    assert out[\"status\"] == \"done\"\n    after = DB.get_item(conn, \"a2\", cid)\n    assert (after[\"state\"], after[\"state_reasons\"], after[\"ladder\"][\"judge\"][\"verdict\"], after[\"review_status\"]) == \\\n        (\"needs_review\", [\"AMOUNT_RATE_NOT_TOTALED\"], \"agree\", \"accepted\" if action == \"accept\" else \"dismissed\")\n    assert full(conn, cid)[\"amount\"][\"a2\"] == before[\"amount\"][\"a2\"]                  # the whole stored row, call id aside\n    status, err = case_error(conn, cid)\n    assert status == \"failed\" and err[\"code\"] == \"run_partial\"\n    assert \"The re-run gave a different result for\" in err[\"message\"] and err[\"message\"].endswith(TAIL)\n    n = note(conn, cid, \"a2\")\n    assert n and n[\"kind\"] == \"disagreed\" and n[\"step\"] == \"a different result\"\n    assert \"RUN_FAILED\" in blockers(conn, cid)\n\n\ndef test_an_undecided_needs_review_amount_takes_the_new_answer_and_the_case_stays_ready(tmp_path):\n    \"\"\"Control: nothing was decided, so there is nothing to protect; the new check result stands.\"\"\"\n    conn, cid = completed(tmp_path, decide=False)\n    rerun(conn, cid, j2={\"verdict\": \"disagree\", \"reason_code\": \"NONE\"})\n    a2 = DB.get_item(conn, \"a2\", cid)\n    assert a2[\"ladder\"][\"judge\"][\"verdict\"] == \"disagree\" and \"JUDGE_DISAGREES\" in a2[\"state_reasons\"]\n    assert note(conn, cid, \"a2\") is None\n    assert \"RUN_FAILED\" not in blockers(conn, cid)\n\n\ndef test_a_clean_rerun_of_a_decided_case_has_no_run_failed_blocker(tmp_path):\n    conn, cid = completed(tmp_path)\n    rerun(conn, cid)\n    assert case_error(conn, cid) == (\"ready\", None)\n    assert \"RUN_FAILED\" not in blockers(conn, cid)\n\n\n# ---- the conflicts step (judge 3)\ndef j3_cases(tmp_path, decide_cx):\n    conn, cid = completed(tmp_path)\n    cx = DB.get_item(conn, \"f_cx1\", cid)\n    assert (cx[\"state\"], cx[\"ladder\"][\"judge\"][\"verdict\"], cx[\"review_status\"]) == (\"verified\", \"conflict\", \"pending\")\n    if decide_cx:\n        DB.apply_review(conn, \"f_cx1\", \"accept\", now=2.5, case=cid)\n    return conn, cid\n\n\n@pytest.mark.parametrize(\"decide_cx\", [False, True])\n@pytest.mark.parametrize(\"miss\", [False, True])\ndef test_conflicts_step_down_keeps_the_conflict_flag_fails_the_case_and_blocks_the_gate(tmp_path, decide_cx, miss):\n    conn, cid = j3_cases(tmp_path, decide_cx)\n    before = full(conn, cid)\n    out = rerun(conn, cid, j3=PL.AU.LLMFailedFixtureMiss(\"x\") if miss else down(\"j3\"))\n    assert out[\"status\"] == \"done\" and out[\"error\"][\"code\"] == \"run_partial\"\n    assert full(conn, cid) == before\n    status, err = case_error(conn, cid)\n    assert status == \"failed\"\n    assert err[\"message\"] == (\"The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged.\" + TAIL)\n    assert \"RUN_FAILED\" in blockers(conn, cid)\n    assert bool(note(conn, cid, \"f_cx1\")) is decide_cx          # a decided item carries the note; an undecided one is kept silently\n    rerun(conn, cid)                                             # a good run clears the failure and the gate\n    assert case_error(conn, cid) == (\"ready\", None) and \"RUN_FAILED\" not in blockers(conn, cid)\n    assert DB.get_item(conn, \"f_cx1\", cid)[\"ladder\"][\"judge\"][\"verdict\"] == \"conflict\"\n\n\ndef test_conflicts_step_down_twice_with_nothing_to_keep_still_fails_the_case(tmp_path):\n    \"\"\"The first run had judge 3 down (the conflict flag is needs_review with no answer); a second run with it down again has no earlier answer to keep.\"\"\"\n    conn = DB.connect(str(tmp_path / \"d.sqlite\"))\n    cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n    PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=model_flag, j3=down(\"j3\"))), now=lambda: 1.0)\n    assert DB.get_item(conn, \"f_cx1\", cid)[\"ladder\"][\"judge\"][\"verdict\"] == \"unavailable\"\n    rerun(conn, cid, j3=down(\"j3\"))\n    status, err = case_error(conn, cid)\n    assert status == \"failed\" and err[\"code\"] == \"run_partial\"\n    assert err[\"message\"] == \"The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep.\" + TAIL\n    assert \"RUN_FAILED\" in blockers(conn, cid)\n\n\ndef test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate(tmp_path):\n    conn, cid = j3_cases(tmp_path, True)\n    before = full(conn, cid)\n    ticks = iter(range(100))\n    PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 3.0 if next(ticks) < 40 else 9999.0, deadline_s=500)\n    status, err = case_error(conn, cid)\n    assert status == \"failed\" and err[\"code\"] == \"run_deadline\"\n    assert full(conn, cid) == before and \"RUN_FAILED\" in blockers(conn, cid)\nEOF\n.venv/bin/python -I -m pytest tests/unit/test_t146_r4_ladder_compare_and_conflicts.py -q -p no:cacheprovider 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T14:50:18.012Z

**tool result**
````
tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5212/test_conflicts_step_deadline_f0')

    def test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate(tmp_path):
        conn, cid = j3_cases(tmp_path, True)
        before = full(conn, cid)
        ticks = iter(range(100))
        PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 3.0 if next(ticks) < 40 else 9999.0, deadline_s=500)
        status, err = case_error(conn, cid)
>       assert status == "failed" and err["code"] == "run_deadline"
E       AssertionError: assert ('ready' == 'failed'
E         
E         - failed
E         + ready)

tests/unit/test_t146_r4_ladder_compare_and_conflicts.py:145: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[amount-old1-new1-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[amount-old2-new2-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[amount-old4-new4-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[amount-old5-new5-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[amount-old6-new6-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[entry-old11-new11-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[entry-old12-new12-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[entry-old13-new13-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[flag-old15-new15-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_disagrees_reads_the_whole_ladder[flag-old17-new17-True]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_decided_needs_review_amount_survives_a_judge_that_now_disagrees[accept]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_decided_needs_review_amount_survives_a_judge_that_now_disagrees[dismiss]
FAILED tests/unit/test_t146_r4_ladder_compare_and_conflicts.py::test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate
13 failed, 16 passed in 2.75s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:50:21.778Z

**tool call — Bash**
````
{
 "command": "grep -n \"deadline\" tests/unit/test_t146_r3_decided_items_never_lowered.py | head"
}
````

### User / tool · 2026-11-02T14:50:21.910Z

**tool result**
````
4:the deadline, and a re-run with nothing to keep."""
189:# ---- the deadline is hit
191:def test_deadline_keeps_decided_items_without_a_disagreement_note(tmp_path, jump_at):
192:    """A stopped run did not redo anything, so it has nothing to disagree with: rows are byte-identical (no note) and the case says so with run_deadline."""
200:    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
205:    assert err == {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:50:23.173Z

**tool call — Bash**
````
{
 "command": "sed -n 186,210p tests/unit/test_t146_r3_decided_items_never_lowered.py"
}
````

### User / tool · 2026-11-02T14:50:23.276Z

**tool result**
````
    assert_notes(conn, cid, ("e1", "e2", "e3"), "failed", "the second check")


# ---- the deadline is hit
@pytest.mark.parametrize("jump_at", ["extract", "judge_entries", "flags"])
def test_deadline_keeps_decided_items_without_a_disagreement_note(tmp_path, jump_at):
    """A stopped run did not redo anything, so it has nothing to disagree with: rows are byte-identical (no note) and the case says so with run_deadline."""
    conn, cid = completed(tmp_path)
    before = full(conn, cid)
    t = [0.0]

    def on_stage(name):
        if name == jump_at:
            t[0] = 10_000.0
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
    assert out["status"] == "timeout"
    assert full(conn, cid) == before
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    assert_notes(conn, cid, (), "failed", "")


# ---- a re-run with nothing to keep
def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:50:36.195Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_t146_r4_ladder_compare_and_conflicts.py'\ns=open(p).read()\ni=s.index(\"def test_conflicts_step_deadline\")\ns=s[:i]+'''def test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate(tmp_path):\n    \"\"\"The deadline passes during the amounts stage, so the conflicts stage is skipped (and GET case checks say so).\"\"\"\n    conn, cid = j3_cases(tmp_path, True)\n    before = full(conn, cid)\n    t = [0.0]\n\n    def on_stage(name):\n        if name == \"amounts\":\n            t[0] = 10_000.0\n    out = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: t[0], on_stage=on_stage, deadline_s=480)\n    assert out[\"status\"] == \"timeout\"\n    status, err = case_error(conn, cid)\n    assert status == \"failed\" and err[\"code\"] == \"run_deadline\"\n    assert full(conn, cid) == before and \"RUN_FAILED\" in blockers(conn, cid)\n    assert DB.get_case(conn, cid)[\"config\"][\"run_checks\"][\"conflicts_stage\"] == \"skipped\"\n'''\nopen(p,'w').write(s)\nEOF\npython3 - <<'EOF'\np='app/backend/pipeline.py'\ns=open(p).read()\nold='''    if kind == \"entry\":\n        return (old.get(\"summary\"), old.get(\"excerpt\"), old.get(\"date_iso\")) != (it.get(\"summary\"), it.get(\"excerpt\"), it.get(\"date\"))\n    if kind == \"amount\":\n        return (old.get(\"text\"), old.get(\"value_cents\"), old.get(\"kind\")) != (it.get(\"text\"), it.get(\"cents\"), it.get(\"cls\"))\n    oc = old.get(\"computed\") or {}\n    if any(oc.get(k) != it.get(k) for k in (\"from_date\", \"to_date\", \"days\")):\n        return False\n    return (old.get(\"type\"), old.get(\"category\"), _evidence_texts(old)) != (it.get(\"type\"), it.get(\"category\"), {e.get(\"text\") for e in it.get(\"evidence\", [])})\n'''\nnew='''    if kind == \"flag\":\n        oc = old.get(\"computed\") or {}\n        if any(oc.get(k) != it.get(k) for k in (\"from_date\", \"to_date\", \"days\")):\n            return False\n    if _checks_worse(old, it):\n        return True\n    if kind == \"entry\":\n        return (old.get(\"summary\"), old.get(\"excerpt\"), old.get(\"date_iso\")) != (it.get(\"summary\"), it.get(\"excerpt\"), it.get(\"date\"))\n    if kind == \"amount\":\n        return (old.get(\"text\"), old.get(\"value_cents\"), old.get(\"kind\")) != (it.get(\"text\"), it.get(\"cents\"), it.get(\"cls\"))\n    return (old.get(\"type\"), old.get(\"category\"), _evidence_texts(old)) != (it.get(\"type\"), it.get(\"category\"), {e.get(\"text\") for e in it.get(\"evidence\", [])})\n'''\nassert old in s\ns=s.replace(old,new)\nold2='def _disagrees('\nadd='''_POSITIVE = {\"agree\", \"supported\", \"conflict\"}      # a second-check answer that backs the item (judge 1 supported, 2 and 4 agree, 3 conflict confirmed); anything else is not a backing answer\n\n\ndef _checks_worse(old: dict, it: dict) -> bool:\n    \"\"\"T-146 r4: did the whole ladder of checks get worse INSIDE the same state? (a) a reason code the stored row did not have; (b) the second-check answer moved from a\n    backing one to anything else; (c) a code check that was true is now false, or the list of summary tokens the quote does not support went from empty to non-empty.\n    Equal rank is not equal checks: the stored answer is the audit record the paralegal decided on.\"\"\"\n    if set(it.get(\"reasons\") or []) - set(old.get(\"state_reasons\") or []):\n        return True\n    ol, nl = old.get(\"ladder\") or {}, it.get(\"ladder\") or {}\n    ov, nv = (ol.get(\"judge\") or {}).get(\"verdict\"), (nl.get(\"judge\") or {}).get(\"verdict\")\n    if ov in _POSITIVE and nv is not None and nv not in _POSITIVE:\n        return True\n    oc, nc = ol.get(\"code_checks\") or {}, nl.get(\"code_checks\") or {}\n    return any(v is True and nc.get(k) is False for k, v in oc.items()) or (not oc.get(\"summary_tokens_not_in_excerpt\") and bool(nc.get(\"summary_tokens_not_in_excerpt\")))\n\n\n'''\ns=s.replace(old2, add+old2,1)\ns=s.replace('''differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes). A better state with the same content is not a disagreement.''','''differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes), or its checks are worse inside the same state (`_checks_worse`: a new\n    reason, a backing second-check answer turned negative, a code check turned false). A better state with the same content is not a disagreement.''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -I -m pytest tests/unit/test_t146_r4_ladder_compare_and_conflicts.py -q -p no:cacheprovider 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T14:50:38.909Z

**tool result**
````
.............................                                            [100%]
29 passed in 2.29s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:50:48.616Z

**tool call — Bash**
````
{
 "command": "cp app/backend/pipeline.py /private/tmp/claude-501/pl.bak && T=\"tests/unit/test_t146_r4_ladder_compare_and_conflicts.py tests/unit/test_t146_r3_decided_items_never_lowered.py\"; \nmut(){ cp /private/tmp/claude-501/pl.bak app/backend/pipeline.py; python3 - \"$1\" \"$2\" <<'EOF'\nimport sys\np='app/backend/pipeline.py'; s=open(p).read(); a,b=sys.argv[1],sys.argv[2]; assert a in s; open(p,'w').write(s.replace(a,b,1))\nEOF\nr=$(.venv/bin/python -I -m pytest $T -q -x -p no:cacheprovider 2>&1 | tail -1); echo \"MUT [$1 -> $2]: $r\"; }\nmut 'if set(it.get(\"reasons\") or []) - set(old.get(\"state_reasons\") or []):' 'if False:'\nmut 'if ov in _POSITIVE and nv is not None and nv not in _POSITIVE:' 'if False:'\nmut 'any(v is True and nc.get(k) is False' 'any(False and nc.get(k) is False'\nmut 'and bool(nc.get(\"summary_tokens_not_in_excerpt\"))' 'and False'\nmut '_POSITIVE = {\"agree\", \"supported\", \"conflict\"}' '_POSITIVE = {\"agree\", \"supported\"}'\nmut 'nv is not None and nv not in _POSITIVE' 'nv not in _POSITIVE'\nmut '    if _checks_worse(old, it):\n        return True\n' ''\ncp /private/tmp/claude-501/pl.bak app/backend/pipeline.py; git diff --stat app/backend/pipeline.py | tail -1"
}
````

### User / tool · 2026-11-02T14:50:52.676Z

**tool result**
````
MUT [if set(it.get("reasons") or []) - set(old.get("state_reasons") or []): -> if False:]: 1 failed, 2 passed in 0.21s
MUT [if ov in _POSITIVE and nv is not None and nv not in _POSITIVE: -> if False:]: 1 failed, 4 passed in 0.23s
MUT [any(v is True and nc.get(k) is False -> any(False and nc.get(k) is False]: 1 failed, 6 passed in 0.21s
MUT [and bool(nc.get("summary_tokens_not_in_excerpt")) -> and False]: 1 failed, 12 passed in 0.21s
MUT [_POSITIVE = {"agree", "supported", "conflict"} -> _POSITIVE = {"agree", "supported"}]: 1 failed, 16 passed in 0.23s
MUT [nv is not None and nv not in _POSITIVE -> nv not in _POSITIVE]: 1 failed, 7 passed in 0.18s
MUT [    if _checks_worse(old, it):
        return True
 -> ]: 1 failed, 1 passed in 0.22s
 1 file changed, 25 insertions(+), 4 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:50:59.210Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_t146_r4_ladder_compare_and_conflicts.py <<'EOF'\n\n\n# ---- review minor: the gate agrees with the case on every r3 failure path\n@pytest.mark.parametrize(\"script\", [\n    {\"flags\": down(\"flags\")},\n    {\"extract\": down(\"extract\")},\n    {\"j1\": down(\"j1\")},\n    {\"j2\": down(\"j2\")},\n    {\"j4\": down(\"j4\")},\n    {\"j3\": down(\"j3\")},\n    {\"extract\": lambda user: {\"summary\": \"Patient had surgery on Mars.\", \"excerpt\": \"Patient reports low back pain in 2023, resolved.\"}},      # summary-in-quote check fails\n], ids=[\"flags\", \"extract\", \"j1\", \"j2\", \"j4\", \"j3\", \"summary_not_in_quote\"])\ndef test_gate_lists_run_failed_whenever_the_case_is_failed(tmp_path, script):\n    conn, cid = completed(tmp_path)\n    rerun(conn, cid, **script)\n    assert case_error(conn, cid)[0] == \"failed\"\n    assert \"RUN_FAILED\" in blockers(conn, cid)\nEOF\n.venv/bin/python -I -m pytest tests/unit/test_t146_r4_ladder_compare_and_conflicts.py -q -p no:cacheprovider 2>&1 | tail -8\n.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider --continue-on-collection-errors -x -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T14:51:50.491Z

**tool result**
````
....................................                                     [100%]
36 passed in 3.26s
            for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
                used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
        missing = []
        for u in used:
            pat = u.replace("<seq>", "<seq>")
            if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
                missing.append(u)
>       assert not missing, missing
E       AssertionError: ['btn-do-first', 'case-rename-error', 'case-rename-input', 'rerun-unavailable', 'input-title', 'cases-decided', ...]
E       assert not ['btn-do-first', 'case-rename-error', 'case-rename-input', 'rerun-unavailable', 'input-title', 'cases-decided', ...]

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:51:53.334Z

Unrelated (frontend contract). Run the full suite without -x.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:51:54.163Z

**tool call — Bash**
````
{
 "command": "timeout 590 .venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider --continue-on-collection-errors -n 4 2>&1 | tail -20 || true",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:51:54.293Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:51:57.340Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider --continue-on-collection-errors 2>&1 | tail -20",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T14:51:57.430Z

**tool result**
````
Command running in background with ID: bt7xmhd88. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bt7xmhd88.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:51:59.061Z

**tool call — Bash**
````
{
 "command": "grep -n \"rerun_note\\|different result\" memory/contracts/api.md | cut -c1-600; git status --short memory/contracts/api.md app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T14:51:59.208Z

**tool result**
````
129:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a re-run (the extract step made a failure stub, a second check gave no answer, or the flag step was
 M app/backend/pipeline.py
 M memory/contracts/api.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:52:00.605Z

**tool call — Bash**
````
{
 "command": "git diff memory/contracts/api.md | head -30; sed -n 129p memory/contracts/api.md | grep -o \"differs[^.]*\\.[^.]*\\.\" | head"
}
````

### User / tool · 2026-11-02T14:52:00.766Z

**tool result**
````
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 1ad0edd..4438afb 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -619,7 +619,7 @@ Three read-only GETs that feed the vertical steppers (pattern: <outside project> flow r
       "next_action": { "code": "COMPARE_BY_HAND", "text": "..." } } ] }
 ```
 **Steps by item kind, in order** (ids; a step that does not apply is omitted, not skipped, except where noted):
-- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `summary_trimmed` (code, D-054, present only when code removed summary clauses the quote does not support: `why` lists each as "removed from the summary: not in the quote: '<clause>'"; `evidence.removed`, `evidence.original_summary`, `evidence.kept_summary`; the second AI check saw `kept_summary`), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION_SUSPECTED`), `judge_1` (llm), `human`. If the quote fails the word-for-word check or the AI output was malformed, the checks between `extracted` and `highlight` and `judge_1` are `skipped` with that code.
+- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `summary_trimmed` (code, D-054, present only when code removed summary clauses the quote does not support: `why` lists each as "removed from the summary: not in the quote: '<clause>'"; `evidence.removed`, `evidence.original_summary`, `evidence.kept_summary`; the second AI check saw `kept_summary`), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION_SUSPECTED`), `judge_1` (llm), `human`. **T-139 r3 (code changed the AI's text because it states an amount; internal, never in the letter):** `excerpt_narrowed` (code, rule `T-139`, status `pass`, present only when code dropped the quote's end sentence(s) that state an amount; right after `extracted`/`summary_trimmed`; `why` says what was removed, that amounts go only in Billed charges and the internal notes, and that the second check saw the shortened quote; `evidence = {removed[] (the dropped sentences, verbatim), quote_before, quote_after, summary_before, summary_after}`) and `charge_clause_removed` (code, rule `T-139`, status `pass`, present when code removed the trailing summary clause(s) that state an amount, either at generation time after narrowing or in the quote-picker `edit` that removed the amount from the quote; `evidence = {removed[] (verbatim clauses), summary_before, summary_after, quote_before, quote_after}`). The same generation-time record is in `GET /items/{id}` `item.ladder.excerpt_narrowed = {rule, original_excerpt, dropped[], summary_removed[], original_summary, summary_before_charge_trim}`; the edit-time record is internal (`edited.code_trim`), shown only through the step, and cleared by the next edit or by `reset`. The steps are never in `letter_text`. If the quote fails the word-for-word check or the AI output was malformed, the checks between `extracted` and `highlight` and `judge_1` are `skipped` with that code.
 - **amount:** `found_in_text` (code, `GROUNDING_AMOUNT_NOT_IN_TEXT`), `amount_class` (code; pass for a charge; pass with `reason_code` `AMOUNT_RATE_NOT_TOTALED`/`AMOUNT_ESTIMATE`/`AMOUNT_DAMAGES` for the classes that are never totaled; fail for `AMOUNT_UNCLEAR`), `injection_scan`, `judge_2` (llm; `skipped` for damages, which are not judged), `total_inclusion` (code: pass when it is an accepted charge counted in the total, pending when a charge is undecided, skipped when it is not a charge or was dismissed), `human`.
 - **flag, code-made (gap, accident-date or provider conflict):** `computed` (code, `evidence.values` has the dates and days), `spans_match` (code), `endpoints_confirmed` (code, `ENDPOINT_NOT_VERIFIED`), `judge_not_needed` (skipped: arithmetic over dates needs no judge), `human`.
 - **flag, phrase list and/or AI (pre-existing, causation incl. credibility wording D-038/D-043, AI-proposed conflicts):** `proposed_by_phrase_list` (code; skipped with `LLM_ONLY` when only the AI found it), `proposed_by_ai` (llm; skipped with `LEXICON_ONLY` when only the phrase list found it), `agreement` (code: pass when both, fail with `LEXICON_ONLY`/`LLM_ONLY`), `credibility_wording` (code, only for category `credibility_language`: the sentence has a credibility term and is not a clean negation, D-043), `excerpt_verbatim` (code), `highlight` (code), `injection_scan` (code), `judge_4` (llm) or `judge_3` (llm, for a conflict the AI proposed); `skipped` when only the phrase list found the flag (`LEXICON_ONLY`), `human`.
@@ -774,8 +774,11 @@ Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into
 The extract prompt asks the model for the sentences that carry "the treatment, findings, diagnosis, plan or charge", so an entry's summary or quote can state an amount ("Charge per visit $140", "ED charge: $3,915."). The letter prints a dollar figure only in the BILLED CHARGES section (accepted charges and the R-EX-8 total line). Code only (`app/backend/charge_text.py`), no model:
 - **Pipeline.** An entry whose summary or quote states a currency figure (`$` figure incl. OCR-noisy `$1,2OO`, `N dollars`, `USD N`) gets state `needs_review` with reason **`CHARGE_TEXT_IN_ENTRY`** (appendix; `why`: it is held out of the letter; dismiss it, or pick a quote without the amount and edit the summary to match). **T-139 round 2: money written without a `$` counts too** when a money word or claim-form field names it: `TOTAL CHARGE 49100`, `AMOUNT PAID 0 00`, `Charges: 3,915.00`, `Cost estimate 4,500`, `Fee 140/visit`, CMS-1500 `24F 25500` and `CPT 99204, 18500, 1 unit`, UB-04 `FL47 4920 00`, Item 28/29/30. Dates, pain scores, doses, visit counts and CPT/ICD codes are never currency. `detail.amounts[]` then holds the label with its figure as written. It is an ordinary queue item; nothing is rejected.
 - **Narrowing first (T-139 follow-up, code only).** Before the hold-out, when the quote has several sentences and its currency-bearing sentence(s) sit at the START or END, code drops them (`charge_text.narrow_excerpt`): the narrowed quote is a contiguous run of whole, verbatim sentences (a substring of the model's quote; an amount in the MIDDLE, a single-sentence quote, a quote that is all amounts, or fewer than 2 content words left means no narrowing). The summary is then trimmed against the narrowed quote (D-054, then the trailing-amount-clause rule above). Every rung-1 check re-runs on the narrowed pair (`generator.verify`); it is kept only if the pair states no amount, some summary is left, and no check raises a reason the original pair did not already raise; otherwise the entry keeps its quote and is held as above. Judge 1 runs on the narrowed pair (D-044/D-058), so no answer given for the longer quote is reused; with no answer the entry is `needs_review` with `JUDGE_UNAVAILABLE` (JUDGE_NOT_RUN). The entry's `quote`/`excerpt` and offsets are the narrowed text. `ladder.excerpt_narrowed = {rule: "T-139", original_excerpt, dropped[], summary_removed[], original_summary}` records what code dropped; `ladder.generator.output` keeps the model's own output. Frontend: when `ladder.excerpt_narrowed` is present, say "charge sentence not quoted" next to the quote; the paralegal can still re-pick a longer quote, but a quote with an amount is refused as above. Over the 25 recorded cases, 51 entries stated an amount; 42 are narrowed (39 verified by judge 1, 3 need review for other reasons) and 9 remain held (single-sentence billing statements).
+- **Round 3: more ways to write money (adjuster r2), same hold.** Also counted as currency: another sign or code next to a figure (`\u20ac185`, `185 \u20ac`, `\u00a31,200`, `1.200,00 \u20ac`, full-width `\uff04185`, `EUR 185`, `185.00 EUR`, `CAD`, `MXN`, `GBP`, `AUD`), amounts in words before a currency noun (`one hundred eighty-five dollars`, `a thousand bucks`, `400 pesos`, Spanish `cuatrocientos d\u00f3lares`), more money words with a money-shaped figure (`Total: 1,200.00`, `Amount: 1,200.00`, `Bill 3,915`, `Invoice total 1,567.05`, `Lien amount 4,000`, `Out-of-pocket 1,200.00`, `Self-pay rate 185`, `Network discount`, `Adjustment -1,250.00`, `Medical specials total`, `Saldo`, `Costo`, `Fee 95`), `185 per visit`, and a figure inside a patient's statement (`Patient states the ER bill was 3,915`, `she owes the chiropractor about 2,400`, `charged me fifteen hundred`). Plain clinical number words (`twelve visits`, `two weeks`, `twenty minutes`) and figures with a unit are never money; `type of bill 0111` is not. **Closed world, written down:** not detected are slang or shorthand (`one eighty-five each`, `6.5k`, `x 185`), bare decimals with no money word (`Initial exam 185.00`), per-mile rates, and Spanish number words other than the hundreds, so a record that states money only like that still reaches the carrier letter if the paralegal accepts it; the reviewer reads every quote before accepting. `evals/letter_check.py` has its own detectors for all of the above (token walk for words, its own regexes for signs and statements).
 - **Accept (single, batch, and `edit`, D-051 choke point).** Refused `422 CODE_CHECK_FAILED` with `detail = {item_id, reason_code: "CHARGE_TEXT_IN_ENTRY", step_id: "charge_text", failed_steps: ["charge_text"], tokens: [], amounts: [...], next_action: {code: "EDIT_QUOTE" | "EDIT_SUMMARY", text, target}}`; `EDIT_QUOTE` when the quote states the amount (the quote picker), else `EDIT_SUMMARY`. Same shape as the D-051 code checks.
 - **Edit.** `edits.excerpt` (the quote picker) with a quote that has no amount: if the summary still states one and the AI wrote that summary (she has not edited it), code removes the trailing clause(s) that state an amount under the D-054 suffix rule (only a run of clauses at the end, never the first clause, the kept prefix keeps at least 2 content words; otherwise nothing is trimmed) and the edit saves with the trimmed summary (`edited.summary`, the original is kept; the internal notes' EDITED ITEMS line shows both). The response `warnings[]` gains `{code: "CHARGE_CLAUSE_REMOVED", item_id, removed: [clause...], message}`. If code cannot trim, the edit is `422 invalid_edit` (`detail.reason "CHARGE_TEXT_IN_ENTRY"`); the paralegal edits the summary. A quote is never rewritten by code.
+- **The held-out hint says the true reason (T-139 round 3).** The entry `why` (case view, `GET /items/{id}`), the 422 `message` of accept and of `edit`, all follow one rule (`charge_text.bill_state` over the amount items on the entry's records): a record with a charge that is accepted says "This record is a bill and its charges are already listed under Billed charges, so dismiss this entry unless it states treatment."; a record whose charge is not yet accepted says its charges go under Billed charges once she accepts them; a record with no charge amount (a claim form, an affidavit, a statement whose lines are unclear amounts) says "No charge was read from this record, so its figures are not counted in the Billed charges section; the internal notes name them so you can request the bill." The static `why` for the code (appendix, trace `state_reasons`) makes no claim about where charges are.
+- **Trace (T-139 r3).** Whenever code shortens a quote or strips a summary clause for an amount (narrowing, the trailing-clause trim, the quote-picker edit trim), the item trace carries a code step (`excerpt_narrowed`, `charge_clause_removed`) with the removed text verbatim, the reason, and the before and after quote and summary (see the entry steps in the trace section). The step is internal; the letter and the internal notes carry no trace text.
 - **Export.** Defence in depth for old data and any other path: `in_entries` drops an entry whose current summary or quote states an amount, even if it is `accepted`/`edited` (and a narrative sentence that states one). The internal notes list its record under RECORDS NOT IN THE TREATMENT SECTION as "states a dollar amount, not exported (...)"; the parenthesis names only actions that clear the hold: a bill record (it has charge amounts) says "this record is a bill and its charges are already listed under Billed charges; dismiss this entry unless it states treatment"; a quote that states the amount says "dismiss this entry, or pick a quote that does not state it and change the summary to match in the same edit"; a clean quote with an amount in the summary says "dismiss this entry, or edit the summary to remove it". A pending one reads the same. `counts.entries` excludes it.
 - **Dismissed charge.** A provider with a dismissed `charge` amount is not listed under BILLS TO REQUEST. **T-139 round 2:** BILLS TO REQUEST lists treating providers and facilities only: a record whose source is a law firm, attorney, payer or EOB, or records custodian (`export._treating`: closed source-word list, or first-person firm wording such as "this firm represents" in the record) is never listed. No dismissed amount is quoted in the letter (the BILLED CHARGES section lists accepted charges only, and an entry quoting the figure is held out as above).
 - **Eval.** `python -m evals.letter_check` (also a row and a blocker in `python -m evals.run`): the fixture-backend export of the sample, every golden case and every library packet has 0 currency strings outside BILLED CHARGES, 0 non-accepted amounts inside it, the exact total line, and (all charges dismissed) none anywhere.
differs from it (a worse state, a different summary, quote, date, amount or flag evidence), the stored row is kept whole and its `ladder.rerun_note` is set to `{kind: "failed" | "disagreed", step, message, at}`; every item view also carries `rerun_note` (the message string, or `null`), to be shown on the item.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:52:06.968Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\na=\"(a worse state, a different summary, quote, date, amount or flag evidence)\"\nassert s.count(a)==1\ns=s.replace(a,\"(a worse state, a different summary, quote, date, amount or flag evidence, or worse checks inside the same state: a reason code the stored row did not have, a backing second-check answer (agree, supported, conflict) that is now negative, a code check that was true and is now false)\")\nopen(p,'w').write(s)\nEOF\necho ok"
}
````

### User / tool · 2026-11-02T14:52:07.128Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:52:09.837Z

**tool call — Bash**
````
{
 "command": "sleep 200; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bt7xmhd88.output | tail"
}
````

### User / tool · 2026-11-02T14:52:09.840Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 200 followed by: cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bt7xmhd88.output tail. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:52:12.175Z

Waiting for the background run to finish.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:52:12.498Z

**tool call — Monitor**
````
{
 "query": "select:Monitor",
 "max_results": "1"
}
````

### User / tool · 2026-11-02T14:52:12.500Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Monitor failed due to the following issue:
The required parameter `description` is missing

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 1800000ms are capped to 1800000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required":["description","timeout_ms"],"additionalProperties":false}</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:52:15.102Z

**tool call — Bash**
````
{
 "command": "until grep -q \"passed\\|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bt7xmhd88.output 2>/dev/null; do sleep 5; done; tail -15 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bt7xmhd88.output",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:58:16.317Z

**tool result**
````
        missing = []
        for u in used:
            pat = u.replace("<seq>", "<seq>")
            if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
                missing.append(u)
>       assert not missing, missing
E       AssertionError: ['cases-chip-can-export']
E       assert not ['cases-chip-can-export']

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
1 failed, 4531 passed, 1 skipped in 374.76s (0:06:14)

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:58:23.064Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && python3 - <<'EOF'\nimport subprocess\nhead=subprocess.check_output(['git','show','HEAD:memory/contracts/api.md']).decode()\na=\"(a worse state, a different summary, quote, date, amount or flag evidence)\"\nassert head.count(a)==1\nnew=head.replace(a,\"(a worse state, a different summary, quote, date, amount or flag evidence, or worse checks inside the same state: a reason code the stored row did not have, a backing second-check answer (agree, supported, conflict) that is now negative, a code check that was true and is now false)\")\nblob=subprocess.run(['git','hash-object','-w','--stdin'],input=new.encode(),capture_output=True,check=True).stdout.decode().strip()\nsubprocess.check_call(['git','update-index','--cacheinfo',f'100644,{blob},memory/contracts/api.md'])\nEOF\ngit add app/backend/pipeline.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py && git diff --cached --stat && git commit -q -m \"fix(backend): T-146 r4 re-run compare reads the whole ladder; pin conflicts-step failure as RUN_FAILED\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && SHA=$(git rev-parse --short HEAD) && echo $SHA; unset GIT_INDEX_FILE; git status --short app/backend/pipeline.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T14:58:23.198Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && python3 - <<'EOF'
import subprocess
head=subprocess.check_output(['git','show','HEAD:memory/contr
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:58:29.380Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && python3 - <<'EOF'\nimport subprocess\nhead=subprocess.check_output(['git','show','HEAD:memory/contracts/api.md']).decode()\na=\"(a worse state, a different summary, quote, date, amount or flag evidence)\"\nassert head.count(a)==1\nnew=head.replace(a,\"(a worse state, a different summary, quote, date, amount or flag evidence, or worse checks inside the same state: a reason code the stored row did not have, a backing second-check answer (agree, supported, conflict) that is now negative, a code check that was true and is now false)\")\nblob=subprocess.run(['git','hash-object','-w','--stdin'],input=new.encode(),capture_output=True,check=True).stdout.decode().strip()\nsubprocess.check_call(['git','update-index','--cacheinfo',f'100644,{blob},memory/contracts/api.md'])\nEOF\ngit add app/backend/pipeline.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T14:58:29.997Z

**tool result**
````
 app/backend/pipeline.py                            |  29 +++-
 memory/contracts/api.md                            |   2 +-
 .../test_t146_r4_ladder_compare_and_conflicts.py   | 170 +++++++++++++++++++++
 3 files changed, 196 insertions(+), 5 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:58:33.074Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx && git commit -q -m \"fix(backend): T-146 r4 re-run compare reads the whole ladder; pin conflicts-step failure as RUN_FAILED\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" 2>&1 | tail -5; git rev-parse --short HEAD; unset GIT_INDEX_FILE; git log -1 --stat --format=%h | tail -5",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T14:58:37.370Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
c2913a6

 app/backend/pipeline.py                            |  29 +++-
 memory/contracts/api.md                            |   2 +-
 .../test_t146_r4_ladder_compare_and_conflicts.py   | 170 +++++++++++++++++++++
 3 files changed, 196 insertions(+), 5 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:58:46.988Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B ac T-146 --check 1 --agent backend --evidence \"tests/unit/test_t146_r4_ladder_compare_and_conflicts.py (36 tests): a2 repro (judge agree->disagree inside needs_review, accepted and dismissed) kept whole with note + run_partial + RUN_FAILED; equal-rank table; j3 down/fixture-miss/twice/deadline -> failed + RUN_FAILED; 7 mutants killed\" | tail -1; $B commit T-146 --sha c2913a6 --agent backend | tail -1; $B handoff T-146 --agent backend --text \"What changed (r4, section 7.4): pipeline._disagrees now also calls _checks_worse: a decided item is kept whole with a note (run_partial, RUN_FAILED) when its checks get worse inside the same state: a reason code the stored row lacked, a backing second-check answer (agree/supported/conflict) now negative, a code check true->false, or unsupported summary tokens appearing. Reviewer's a2 repro (agree->disagree, accepted and dismissed) passes. api.md sentence updated. Verified: tests/unit/test_t146_r4_ladder_compare_and_conflicts.py 36 pass; r3/r2/r1 files pass; 7 mutants of the new code killed; unit suite 4531 pass, 1 fail outside this card (test_e2e_contract test ids for frontend, cases-chip-can-export). Item 2 (conflicts step): I could not reproduce a gap: judge 3 down (LLMFailed, fixture miss), down twice with nothing to keep, decided and undecided f_cx1, and a deadline before the conflicts stage all already give status failed, run_partial/run_deadline and a RUN_FAILED blocker; the reviewer's 'conflicts down' probe used the dead script key 'conflicts' (the step is j3). Pinned by tests, no code change needed. Also added the cheap minor: RUN_FAILED asserted for 7 failure paths plus a clean-rerun control. Left: F2 (reworded summary blocks the gate) is a question for Chris, F3 (no frontend consumer of rerun_note) needs a frontend card or a SCOPE_CUTS line, both orchestrator calls. A FIRST run with a step down still reads ready by design. Commit c2913a6\" | tail -1; $B move T-146 in_review --agent backend | tail -1"
}
````

### User / tool · 2026-11-02T14:58:47.293Z

**tool result**
````
AC 1 checked: tests/unit/test_t146_r4_ladder_compare_and_conflicts.py (36 tests): a2 repro (judge agree->disagree inside needs_review, accepted and dismissed) kept whole with note + run_partial + RUN_FAILED; equal-rank table; j3 down/fixture-miss/twice/deadline -> failed + RUN_FAILED; 7 mutants killed
T-146: commit c2913a6 recorded
handoff written on T-146
T-146: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:58:52.233Z

T-146 is in_review at c2913a6: a decided item whose checks get worse inside the same state is now kept with a note (a2 repro passes), but I made no code change for the conflicts-step item.

- **Item 1:** the compare now catches a new reason code, a second-check answer that goes from backing to negative, or a code check that turns false. In the reviewer's a2 repro (agree to disagree, accepted and dismissed), the stored row stays whole, it carries the note, the case is run_partial, and the gate shows RUN_FAILED.
- **Item 2:** I couldn't reproduce a gap. Judge 3 down, a fixture miss, down twice with nothing to keep, decided and undecided conflict flags, and a deadline before the conflicts stage all already end failed with RUN_FAILED. The reviewer's "conflicts down" probe used a script key (`conflicts`) the pipeline doesn't read; the step is `j3`. I pinned these paths with tests instead.
- **Tests:** 36 new tests, plus RUN_FAILED asserted on seven failure paths with a clean-rerun control. The full unit suite has 4531 passing and 1 failing, `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared` (missing frontend test id `cases-chip-can-export`), which is outside this card.
- **Left for you:** the reworded-summary gate question and the `rerun_note` consumer are both undone and need your call. A first run with a step down still reads ready, as before.

Everything is in `app/backend/pipeline.py`, `tests/unit/test_t146_r4_ladder_compare_and_conflicts.py` and one sentence of `memory/contracts/api.md`.

### User / tool · 2026-11-02T15:07:09.333Z

The coordinator sent a message while you were working:
Orchestrator, urgent: the core of your T-146 r4 (`_checks_worse`, `_POSITIVE`, `_EXTRACT_STEP` and the `_disagrees` change in app/backend/pipeline.py) is still uncommitted in the working tree. c2913a6 does not have it, and the scoped reviewer is checking HEAD. Commit those hunks now via a temp index, only your hunks. T-161's 83f1afd already touched pipeline.py, so rebase your patch on HEAD. Then confirm on a `git archive HEAD` copy that your r4 tests pass. Reply in 1 line with the commit id.

Address this before completing your current task.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:07:14.752Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6; git show c2913a6:app/backend/pipeline.py | grep -c \"_checks_worse\"; git show HEAD:app/backend/pipeline.py | grep -n \"_checks_worse\\|_POSITIVE\\|_EXTRACT_STEP\" | head; git diff --stat app/backend/pipeline.py; grep -n \"_EXTRACT_STEP\" app/backend/pipeline.py | head -3"
}
````

### User / tool · 2026-11-02T15:07:14.905Z

**tool result**
````
83f1afd fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)
0b2ce9c fix(frontend): T-158 refused-Accept reason box is scrolled fully into view once layout settles (several passes by item id, clear of the sticky header); the rerun sentence keeps its count when the trace was not cached yet
9fc579c feat(backend): T-159 audit trail for a flagged charge: named confirm in the review event, charge_flag trace step, plain flag sentence, repeat accept is a no-op
0e3e8ba test(e2e): T-155 r2 L6 has five judge objections since D-060 default-deny (a2 office visits $1,100 undated); presence check on a2 and a7
c8022fa tools: pre-commit also refuses any staged .py that does not parse (lesson 6379c0b)
70af4a7 feat(frontend): T-162 show item.rerun_note on a decided item, in its row and in its trace dialog
3
244:_EXTRACT_STEP = "writing the entries"
251:        return _EXTRACT_STEP
262:    if cause == _EXTRACT_STEP:
273:_POSITIVE = {"agree", "supported", "conflict"}      # a second-check answer that backs the item (judge 1 supported, 2 and 4 agree, 3 conflict confirmed); anything else is not a backing answer
276:def _checks_worse(old: dict, it: dict) -> bool:
284:    if ov in _POSITIVE and nv is not None and nv not in _POSITIVE:
292:    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes), or its checks are worse inside the same state (`_checks_worse`: a new
304:    if _checks_worse(old, it):
583:        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items
 app/backend/pipeline.py | 36 +++++++++++++++++++++++++++++-------
 1 file changed, 29 insertions(+), 7 deletions(-)
244:_EXTRACT_STEP = "writing the entries"
251:        return _EXTRACT_STEP
262:    if cause == _EXTRACT_STEP:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:07:19.642Z

**tool call — Bash**
````
{
 "command": "echo HEAD; git show HEAD:app/backend/pipeline.py | grep -c \"_checks_worse\\|_POSITIVE\\|_EXTRACT_STEP\"; echo WT; grep -c \"_checks_worse\\|_POSITIVE\\|_EXTRACT_STEP\" app/backend/pipeline.py; git diff app/backend/pipeline.py | head -80"
}
````

### User / tool · 2026-11-02T15:07:19.776Z

**tool result**
````
HEAD
9
WT
9
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 79b3a80..ce2b3eb 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -241,13 +241,14 @@ def _mark_judge_not_run(entries: list, by_n: dict) -> None:
 _STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
 _FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
 _RANK = {"verified": 0, "needs_review": 1, "rejected": 2}
+_EXTRACT_STEP = "writing the entries"
 
 
 def _failure(kind: str, it: dict):
     """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
     step failed, or an item whose second check was asked and gave no answer."""
     if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS:
-        return "writing the entries"
+        return _EXTRACT_STEP
     if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
         return "finding the flags"
     return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None
@@ -258,7 +259,7 @@ def _degrades(kind: str, old: dict, it: dict):
     (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
     (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
     cause = _failure(kind, it)
-    if cause == "writing the entries":
+    if cause == _EXTRACT_STEP:
         return cause if old.get("summary") and old.get("excerpt") else None
     if cause == "finding the flags":
         return None if set(old.get("state_reasons") or []) & _FLAG_FAIL else cause
@@ -269,22 +270,43 @@ def _evidence_texts(row: dict) -> set:
     return {e.get("text") or e.get("excerpt") for e in (row.get("evidence") or [])}
 
 
+_POSITIVE = {"agree", "supported", "conflict"}      # a second-check answer that backs the item (judge 1 supported, 2 and 4 agree, 3 conflict confirmed); anything else is not a backing answer
+
+
+def _checks_worse(old: dict, it: dict) -> bool:
+    """T-146 r4: did the whole ladder of checks get worse INSIDE the same state? (a) a reason code the stored row did not have; (b) the second-check answer moved from a
+    backing one to anything else; (c) a code check that was true is now false, or the list of summary tokens the quote does not support went from empty to non-empty.
+    Equal rank is not equal checks: the stored answer is the audit record the paralegal decided on."""
+    if set(it.get("reasons") or []) - set(old.get("state_reasons") or []):
+        return True
+    ol, nl = old.get("ladder") or {}, it.get("ladder") or {}
+    ov, nv = (ol.get("judge") or {}).get("verdict"), (nl.get("judge") or {}).get("verdict")
+    if ov in _POSITIVE and nv is not None and nv not in _POSITIVE:
+        return True
+    oc, nc = ol.get("code_checks") or {}, nl.get("code_checks") or {}
+    return any(v is True and nc.get(k) is False for k, v in oc.items()) or (not oc.get("summary_tokens_not_in_excerpt") and bool(nc.get("summary_tokens_not_in_excerpt")))
+
+
 def _disagrees(kind: str, old: dict, it: dict) -> bool:
     """T-146 r3: does the NEW row `it` lower or change what the stored row `old` says? True when its state is worse (verified -> needs_review -> rejected) or its content
-    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes). A better state with the same content is not a disagreement.
+    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes), or its checks are worse inside the same state (`_checks_worse`: a new
+    reason, a backing second-check answer turned negative, a code check turned false). A better state with the same content is not a disagreement.
     A stored row that is itself in the tray (rejected) has nothing to lower. A flag whose computed numbers changed is the existing reset path (the decision was about
     other numbers), so it is not judged here."""
     if _RANK.get(it["state"], 1) > _RANK.get(old["state"], 1) and old["state"] != "rejected":
         return True
     if old["state"] == "rejected":
         return False
+    if kind == "flag":
+        oc = old.get("computed") or {}
+        if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
+            return False
+    if _checks_worse(old, it):
+        return True
     if kind == "entry":
         return (old.get("summary"), old.get("excerpt"), old.get("date_iso")) != (it.get("summary"), it.get("excerpt"), it.get("date"))
     if kind == "amount":
         return (old.get("text"), old.get("value_cents"), old.get("kind")) != (it.get("text"), it.get("cents"), it.get("cls"))
-    oc = old.get("computed") or {}
-    if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
-        return False
     return (old.get("type"), old.get("category"), _evidence_texts(old)) != (it.get("type"), it.get("category"), {e.get("text") for e in it.get("evidence", [])})
 
 
@@ -558,7 +580,7 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
         err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
     else:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:07:22.681Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/backend/pipeline.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py memory/contracts/api.md; git log --oneline -3 -- app/backend/pipeline.py; D=/private/tmp/claude-501/arch && rm -rf $D && mkdir $D && git archive HEAD | tar -x -C $D && cd $D && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_t146_r4_ladder_compare_and_conflicts.py tests/unit/test_t146_r3_decided_items_never_lowered.py -q -p no:cacheprovider 2>&1 | tail -4",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T15:07:29.067Z

**tool result**
````
 memory/contracts/api.md                            |   6 +-
 .../test_t146_r4_ladder_compare_and_conflicts.py   | 170 ---------------------
 2 files changed, 3 insertions(+), 173 deletions(-)
83f1afd fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)
c2913a6 fix(backend): T-146 r4 re-run compare reads the whole ladder; pin conflicts-step failure as RUN_FAILED
bf53087 fix(backend): T-146 r3 a re-run never lowers or replaces a decided item: it is kept whole with a visible note and the case reads run_partial (flag step down, summary check failed, extract down, judge down, nothing to keep)
........................................................................ [ 78%]
....................                                                     [100%]
92 passed in 5.55s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:07:31.530Z

**tool call — Bash**
````
{
 "command": "ls tests/unit/test_t146_r4* 2>&1; git ls-tree HEAD --name-only tests/unit/ | grep t146"
}
````

### User / tool · 2026-11-02T15:07:31.631Z

**tool result**
````
tests/unit/test_t146_r4_ladder_compare_and_conflicts.py
tests/unit/test_t146_r2_failed_rerun_keeps_items.py
tests/unit/test_t146_r3_decided_items_never_lowered.py
tests/unit/test_t146_r4_ladder_compare_and_conflicts.py
tests/unit/test_t146_rerun_keeps_items.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:07:33.984Z

**tool call — Bash**
````
{
 "command": "for f in app/backend/pipeline.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py; do git show HEAD:$f | cmp - $f && echo \"same $f\"; done; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T15:07:34.149Z

**tool result**
````
same app/backend/pipeline.py
same tests/unit/test_t146_r4_ladder_compare_and_conflicts.py
83f1afd
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:07:37.538Z

Nothing was missing from HEAD, and I made no new commit. The r4 change is in c2913a6, which is an ancestor of HEAD 83f1afd. `_checks_worse`, `_POSITIVE` and the `_disagrees` change are in `app/backend/pipeline.py` as committed. `_EXTRACT_STEP` is T-161's hunk, already in 83f1afd.

I compared HEAD against the working tree: `app/backend/pipeline.py` and `tests/unit/test_t146_r4_ladder_compare_and_conflicts.py` are byte-identical to it. On a `git archive HEAD` copy, the r4 and r3 test files give 92 passed.

The `git diff` output that made the hunks look uncommitted came from the shared index, which is stale after my temp-index commit. Point the scoped reviewer at 83f1afd (or c2913a6 for my hunks).
