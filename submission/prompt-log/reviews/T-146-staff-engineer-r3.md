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
