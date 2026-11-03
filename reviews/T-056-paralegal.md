# T-056 review — paralegal-reviewer (Maria Delgado persona)

Commit d548ccd: manual entry for a rejected record (D-031) and the "not a duplicate" split.
Verdict: **fail** (2 blockers, 1 major, 1 minor).

## What I ran
- `.venv/bin/python -m pytest tests/unit/test_manual_and_split.py -q 2>&1 | tail -2` gave `14 passed in 1.05s`.
- Read the card (`python3 tools/board.py show T-056`), the d548ccd diff (review.py, pipeline.py, ingest.py, present.py, export.py, store.py, api.py, memory/contracts/api.md), and the unit tests.
- Probe 1 (`artifacts/review-evidence/T-056-paralegal-probe.py`, output in `T-056-paralegal-probe.out.txt`): 13 manual-entry excerpt and summary variants on sample record 5, pending/dismiss checks on the notes and letter, and a split with rerun on case_04.
- Probe 2 (`artifacts/review-evidence/T-056-paralegal-probe2.py`, output in `T-056-paralegal-probe2.out.txt`): a split where the duplicate charge is accepted first (synthetic $310 added to records 1 and 2 of case_04), and a rerun.
- Read-only checks of the live app at http://localhost:7860: `/` has 0 matches for entered/manual/duplicate; `/openapi.json` lists no entry or not_duplicate paths. I did not POST to the live server, since that would create a case in the running app.
- `grep -rn -i "entered by reviewer|entered_by|not a duplicate|manual entry" app/frontend` returned nothing.
- Model: I ran as claude-haiku-5-5 (the dossier expects claude-opus-5-5; I report what I ran as).

## Findings

**B1 blocker. AC 2 ("labelled 'entered by reviewer' in UI and notes") is ticked done, but the UI does not exist, and notes show the label only after accept.**
- The card's AC 2 is `done: true`. Its Handoff says "Left: frontend UI for both".
- The working tree has no manual-entry control and no label anywhere in `app/frontend` (grep above, empty).
- Probe 1: `[PENDING NOTES] label anywhere before accept: False`. The pending line reads `- Entry, record 5 (Capital PT, visit 8, February 20, 2026): "Pain 4/10, improving."` with no label.
- `app/backend/export.py:477` adds the label only when `_status(e) == "in"`.
- `memory/contracts/api.md:24` says the notes "list it under EDITED ITEMS as entered by reviewer", with no accept condition. The code and the contract disagree.
- Why it matters: the label is how Maria and the attorney tell a reviewer-written entry from AI output. The feature cannot be reached from the screen, and in the internal notes the label is absent while the item is still pending.
- Fix: either build the UI control and label on the frontend card and show the label in the pending notes line, or amend AC 2 to backend-only and move the UI clause to the frontend card. Do not tick a UI clause the code does not contain.
- Acceptance test: pytest asserts `"entered by reviewer" in internal_notes_text` right after `manual_entry`, before accept. A UI test shows the label next to the pending entry on the sample case.

**B2 blocker. "Not a duplicate" does not move the duplicate's charge to the split record, and a rerun changes attribution silently.**
- Probe 2 output:
  - before split: `amount rows: [('a1', ['r1'], 31000, 'accepted')]`; letter `Billed charges stated in these records: $310.00`
  - after split: `[AMT] extract_amounts rows after split: [(1, [1, 2], 31000)]`, then `[AMT post-split] amount rows: [('a1', ['r1'], 31000, 'accepted')]`. There is no `ax2_k` row. The total stays $310.
  - after rerun: `[AMT post-rerun] amount rows: [('a1', ['r1', 'r2'], 31000, 'accepted')]`, with `config not_duplicates: ['r2']`.
- Cause: `app/backend/review.py:303` (`rows = [a for a in AM.extract_amounts(recs) if a["record_no"] == rec["n"]]`) finds nothing, because `app/backend/amounts.py:102-103` merges identical amounts across records into one row keyed to the first record.
- Contract: `memory/contracts/api.md:25` says the split record "gets its own entry and amounts". The handoff says split amounts get `ax<n>_<k>` ids. Neither happens for identical amounts.
- Why it matters: Maria reconciles charges. If she has declared two separate visits, specials are understated by $310 and nothing in the app says so. After a rerun the amount quietly returns to both records. The unit test uses case_04, which has no amounts, so nothing catches this.
- Fix: in `not_duplicate`, build the split record's amount rows without the cross-record merge, remove the record from the merged amount's `record_ids`, create the `ax<n>_k` items, and log the movement on the event. Make the rerun honour `not_duplicates` for amounts too.
- Acceptance test: synthetic case with identical $310 charges in records 1 and 2 (the probe 2 construction). After `not_duplicate(e1, r2)`, there are two amount items with `record_ids` [r1] and [r2], and the accepted total is $620. The same rows survive `run_pipeline` on rerun.

**M1 major. A reviewer override of a summary warning on manual entry is not recorded in the notes, and the letter then carries a number the quote does not contain.**
- Probe 1: `[ENTRY] summary adds number, confirm_warnings=true: ACCEPTED`; after accept, `[CONFIRM->ACCEPT] letter has 'Pain 9/10.': True`; `[CONFIRM->ACCEPT] notes mention confirmed wording: False`. The quote in the record is "Pain 4/10, improving."
- `app/backend/review.py:128` sets `kept_my_wording` only on the edit path. `manual_entry` (`review.py:221-263`) never sets it, so the notes line "paralegal confirmed keep my wording" never appears for a manual entry.
- The tool did not invent the number. Maria typed it after a 409 needs_confirm gate. The defect is the missing trace: the edit path records the override and the manual path does not.
- Persona §5 says any statement without verbatim support is a blocker. If Chris's spec does not allow keeping a number absent from the quote on manual entry, this becomes a blocker. See question 2.
- Fix: record `kept_my_wording` on manual entries and emit the same notes line, or forbid the override on manual entries.
- Acceptance test: `manual_entry` with `confirm_warnings=true`, then accept; `internal_notes_text` contains "paralegal confirmed keep my wording" for `e5_m`.

**m1 minor. Test gaps behind B1 and B2.**
- The labelled-in-notes assertion in `tests/unit/test_manual_and_split.py` runs only after accept.
- The split tests use `case_04_duplicates_no_amounts`, so the amount path is untested.

**Outside my lens:** the d548ccd api.py hunk is import reordering. The handoff mentions a shared-index commit. I did not assess either.

## What holds
- The verbatim-sentence gate holds on every variant I tried. Fragments, case changes, a dropped final period, a sentence from another record, and an empty quote all return 422 `invalid_edit`. A single verbatim sentence and a two-sentence verbatim quote are accepted.
- Manual entries are never auto-accepted. They are `pending` after the write, absent from the letter, and absent after dismiss. Date and provider come from the record header (2026-02-20, "Capital PT, visit 8").
- The split writes a `not_duplicate` event, keeps the case-config decision, and keeps 5 entries (e1 = [r1], e2 = [r2]) through a rerun. The split-off entry is not in the letter before accept.

Ship-bar score (D.2 `verify_quickly`): 2. I could verify each manual entry's text and header-sourced date and provider, but I cannot reach the feature from the app, and the split amounts do not reconcile.

```json
{"card": "T-056", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit d548ccd (T-056); working tree at HEAD c61e84f with other workers' uncommitted edits (app/frontend/app.js, app/backend/grounding.py); sample case evals/golden/sample.txt and synthetic case_04 with an added $310 charge; live app http://localhost:7860 read-only (no manual-entry UI present)",
 "exercised": [
  "read personas/paralegal.md in full",
  "python3 tools/board.py show T-056 (AC 1-3, Handoff, notes)",
  ".venv/bin/python -m pytest tests/unit/test_manual_and_split.py -q 2>&1 | tail -2 -> 14 passed in 1.05s",
  "git show d548ccd --stat and diffs of review.py, pipeline.py, ingest.py, present.py, export.py, store.py, api.py, memory/contracts/api.md",
  "git status (uncommitted edits by other workers present)",
  "grep -rn -i 'entered by reviewer|entered_by|not a duplicate|manual entry' app/frontend -> no matches",
  "curl http://localhost:7860/ and grep entered|manual|duplicate -> 0 matches; curl /openapi.json -> no entry or not_duplicate paths",
  "artifacts/review-evidence/T-056-paralegal-probe.py (13 manual-entry variants, summary override, pending and dismiss notes/letter, split and rerun, synthetic amount split) -> T-056-paralegal-probe.out.txt",
  "artifacts/review-evidence/T-056-paralegal-probe2.py (second sentence alone with a supported summary; accepted-charge split, post-split and post-rerun amount rows and letter totals) -> T-056-paralegal-probe2.out.txt",
  "read app/backend/amounts.py:102-103, app/backend/review.py:128, 221-263, 303, app/backend/export.py:477 and 492, memory/contracts/api.md:24-25"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 2, "manual_entry_verbatim_gate": 5, "never_auto_accepted_or_in_letter": 5, "entry_labelling_ui_and_notes": 1, "split_entries_event_rerun": 4, "split_amounts_totals": 1, "override_traceability": 2},
 "findings": [
  {"severity": "blocker", "title": "AC 2 labelling unmet: no UI control or label exists; notes label appears only after accept",
   "evidence": "board AC 2 done:true; Handoff 'Left: frontend UI for both'; grep app/frontend for 'entered by reviewer|entered_by|manual entry' -> no matches; curl localhost:7860 -> 0 matches; probe.out.txt '[PENDING NOTES] label anywhere before accept: False' with line '- Entry, record 5 (Capital PT, visit 8, February 20, 2026): \"Pain 4/10, improving.\"'; app/backend/export.py:477 labels only when _status(e)=='in'; memory/contracts/api.md:24 says notes list it under EDITED ITEMS as entered by reviewer",
   "why_it_matters": "The reviewer-written label is how the attorney and adjuster tell reviewer text from AI output. The feature cannot be reached from the app, and pending notes do not carry the label. The card ticks a UI clause the code does not contain.",
   "fix": "Build the manual-entry control and label on the frontend card and label the pending notes line, or amend AC 2 to backend-only and move the UI clause to the frontend card. Make the contract and the code agree on when the notes label appears.",
   "acceptance_test": "pytest: after manual_entry and before accept, internal_notes_text contains 'entered by reviewer' for e5_m. UI e2e: sample case, manual entry on record 5 shows the 'entered by reviewer' label next to the pending entry."},
  {"severity": "blocker", "title": "'Not a duplicate' does not move the duplicate's charge to the split record; rerun silently reattaches it",
   "evidence": "probe2.out.txt: '[AMT post-split] amount rows: [(a1, [r1], 31000, accepted)]' with no ax2_k row, letter total stays '$310.00'; '[AMT] extract_amounts rows after split: [(1, [1, 2], 31000)]'; '[AMT post-rerun] amount rows: [(a1, [r1, r2], 31000, accepted)]' with config not_duplicates ['r2']; app/backend/review.py:303 'rows = [a for a in AM.extract_amounts(recs) if a[\"record_no\"] == rec[\"n\"]]'; app/backend/amounts.py:102-103 merges identical amounts into one row keyed to the first record; memory/contracts/api.md:25 'the record gets its own entry and amounts'",
   "why_it_matters": "Billed charges must reconcile. After the paralegal declares two separate records, the second charge disappears from the total with no warning, which understates specials. After a rerun the amount returns to both records with no event. The unit test uses case_04, which has no amounts, so nothing catches this.",
   "fix": "In not_duplicate, build the split record's amount rows without the cross-record merge; remove the record from the merged amount's record_ids; create ax<n>_k items; log the movement on the not_duplicate event. Make the rerun honour not_duplicates for amounts.",
   "acceptance_test": "pytest on a synthetic case with identical $310 charges in records 1 and 2: after not_duplicate(e1, r2) there are two amount items with record_ids [r1] and [r2]; accepted total is $620; the same rows survive run_pipeline on rerun."},
  {"severity": "major", "title": "Reviewer override of a summary warning on manual entry is not recorded in notes; letter carries a number absent from the quote",
   "evidence": "probe.out.txt: '[ENTRY] summary adds number, confirm_warnings=true: ACCEPTED'; '[CONFIRM->ACCEPT] letter has 'Pain 9/10.': True'; '[CONFIRM->ACCEPT] notes mention confirmed wording: False'. Record 5 quote is 'Pain 4/10, improving.' (sample.txt:26). app/backend/review.py:128 sets kept_my_wording only on the edit path; manual_entry (review.py:221-263) never sets it.",
   "why_it_matters": "The edit path records 'paralegal confirmed keep my wording'; the manual path leaves no trace of the override, so the notes do not show that a warning was overridden. The tool did not invent the number; the missing trace is the defect. If the spec does not allow keeping a number absent from the quote, this is a blocker under persona section 5.",
   "fix": "Store kept_my_wording on manual entries and emit the same notes line in EDITED ITEMS, or forbid the override on manual entries.",
   "acceptance_test": "pytest: manual_entry with confirm_warnings=true, then accept; internal_notes_text contains 'paralegal confirmed keep my wording' for e5_m."},
  {"severity": "minor", "title": "Test gaps behind B1 and B2",
   "evidence": "tests/unit/test_manual_and_split.py: the 'entered by reviewer' assertion runs only after accept; the split tests use case_04_duplicates_no_amounts (evals/golden), so no amount path is exercised.",
   "why_it_matters": "The label-before-accept and amount-split behaviours are the ones that fail, and no test covers them.",
   "fix": "Add the pending-label and amount-split tests listed under B1 and B2.",
   "acceptance_test": "The two tests named in B1 and B2 pass on the fixed commit."}
 ],
 "whats_right": [
  "The verbatim-sentence gate holds on every variant probed: fragments, case changes, dropped final period, a sentence from another record and an empty quote are refused 422 invalid_edit; single and two-sentence verbatim quotes are accepted.",
  "Manual entries are never auto-accepted: pending after write, absent from the letter, absent after dismiss; date and provider come from the record header (2026-02-20, 'Capital PT, visit 8').",
  "The split writes a not_duplicate event, keeps the case-config decision, and keeps 5 entries (e1=[r1], e2=[r2]) through a rerun; the split-off entry is not in the letter before accept."
 ],
 "questions_for_chris": [
  "AC 2 says 'labelled in UI and notes' and is ticked done, but the frontend has no manual-entry control. Should the UI clause move to a frontend card (and AC 2 be amended), or stay on this card?",
  "On manual entry, should a reviewer be allowed to keep a number that is not in the quote (confirm_warnings)? If yes, the override must be recorded as on the edit path. If no, M1 becomes a blocker.",
  "memory/contracts/api.md:24 says the manual entry is listed under EDITED ITEMS as entered by reviewer; the code lists it there only after accept. Which is intended?"
 ]}
```
