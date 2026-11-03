# T-068 round 3 review: paralegal-reviewer (Maria Delgado persona)

Scope: commit 5f71a65 (UI for D-041), run on a `git archive HEAD` snapshot (HEAD = 5f71a65) at http://127.0.0.1:7880 with LLM_BACKEND=fixture FIXTURE_SET=curated and a scratch DATA_DIR. The working tree in /Users/arsis/zlayt-pm-project is dirty (board, memory, agent-memory files); the snapshot is the reviewed state. Sample case: evals/golden/case_01_date_formats.txt pasted, as a paralegal would. The server is stopped (port 7880 closed).

## Round-2 items, status on 5f71a65

- N1 (major) Accept before a date is picked: **fixed.** Accept is disabled on the record 8 row with "Confirm the date first. Go to its date choices". The server also refuses (422 DATE_UNCONFIRMED) for accept, edit and batch.
- N2 (minor) No record number on the undated row: **fixed.** The row reads "Record 8: Dr. Orla Pennywhistle, phone note" and the button reads "Open record 8".
- N3 (minor) Confirmed orphan card drops the excerpt: **code present, not exercised.** The orphan branch is not reachable with the curated fixtures (see N4), so I did not see it in the app.
- N4 (minor) Orphan branch only proven on a rewritten response: **still open.** The handoff says backend/qa own the curated fixture; it is not in this commit.

## What I checked (case_01, HEAD snapshot)

1. Record 8 row, before any action: one row, Accept disabled (aria-describedby points at the reason), reason text "Confirm the date first. Go to its date choices", link present. The link moves focus to the April 5, 2026 date button (S1_link_click_focus). Pass.
2. Batch: "Accept all verified entries (7)" with the note "1 undated entry was skipped: confirm the date first (Dates to confirm)." Click accepted the 7 dated entries and the live region repeats the skip count. Record 8 stays pending/needs_review on the server. Pass.
3. Forced requests on e8 before confirm: POST accept 422 DATE_UNCONFIRMED; POST edit 422 DATE_UNCONFIRMED; POST batch accept 422 DATE_UNCONFIRMED with detail.rejected [{id e8, reason date_unconfirmed}]. The case JSON before and after is identical except updated_at (S3_changed_top_level_keys = []). Audit event count 7 before, 7 after. Export before confirm: no Pennywhistle line in the letter, and no "date not stated" in the letter. Pass.
4. Confirm April 5, 2026 (I chose the US MM/DD reading to run the flow; the record gives no tie-breaker, and the tool did not pick one). The entry moves onto the timeline with date 2026-04-05, Accept enables, Accept accepts, reload keeps it accepted. Export letter line: "April 5, 2026 — Dr. Orla Pennywhistle, phone note" with the verbatim quote "Patient reports no new symptoms." and "Source [Ex. __ / Bates __]". No "date not stated" in the letter. Pass.

## Findings

**F1 (major) The confirmed and accepted record 8 entry still says its date is unresolved.**
Evidence: GET /api/cases/3xQA67xxiHA55dJbhknRNQ/items/e8 after confirm_date and accept returns `"state": "needs_review", "reasons": ["DATE_AMBIGUOUS"], "why": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.", "review_status": "accepted"`. The record itself is correct (`date_status: confirmed`, `date_iso: 2026-04-05`) and the record_warning flags are empty. The UI row after confirm reads "Needs review" plus "Check: the date can be read two ways" (artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json, S4_entry_after_confirm_text; screenshot artifacts/review-evidence/T-068-r3/S4b-accepted.png).
Why it matters: I confirmed the date and the row still tells me it is unresolved. I cannot tell at a glance that the accept settled it, and a reviewer reading the row would redo the check. The letter is not affected (export-letter-after-confirm-accept.txt is correct), so I rate this major, not blocker: the copy is stale, nothing is invented in the letter.
Fix: confirm_date clears DATE_AMBIGUOUS from the entry reasons and recomputes state (owner: backend, see T-076 F1); the row copy then follows.
Acceptance test: case_01, confirm April 5, 2026, accept. The entry's reasons contain no DATE_AMBIGUOUS, its why text does not say 'two ways', and the timeline row shows no "Check: the date can be read two ways".

**F2 (minor) Edit and Change quote are enabled on the undated row; the date refusal shows only on save.**
Evidence: artifacts/review-evidence/T-068-r3/T-068-r3-edit-probe.json: `edit_button_disabled: false`, `edit_button_count: 1`; after typing and saving, the live message is "Confirm the date first. This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm." Screenshot: artifacts/review-evidence/T-068-r3/E1-edit-on-undated-row.png. Forced POST edit returns 422 DATE_UNCONFIRMED (round 3 step 3). I did not check whether the typed text survives the refusal.
Why it matters: D-041 says the UI disables the blocked action with the reason shown. Edit is blocked by the same rule (api.md: edit implies accept), so the paralegal should see that before she types. Not a blocker: the server refuses and nothing is written.
Fix: disable Edit and Change quote on undated entries with the same reason shown for Accept.
Acceptance test: on the undated row, Edit is disabled and "Confirm the date first" is shown beside it before any click.

**F3 (minor, carried from round 2 N4) The orphan branch is still proven only on a rewritten response.**
Evidence: commit 5f71a65 changes only the UI; tests/e2e/test_input.py still rewrites GET /api/cases/<token> for the orphan test; the T-068 handoff says "N4 ... is backend/qa-owned, not done".
Why it matters: the orphan case is the protection if a model call drops a record. No real run in this round shows it.
Fix: a curated fixture where a record has a date to confirm and no model entry, with an E2E that runs without route rewriting.
Acceptance test: FIXTURE_SET=curated, no page.route; the record moves to Records without an entry, the excerpt is visible, and the manual-entry path works.

## Test runs

- `.venv/bin/python -m pytest -q tests/unit -k "date or accept"` run from the HEAD snapshot (the reviewed state): `115 passed, 873 deselected in 4.72s`.
- Playwright flow: `.venv/bin/python artifacts/review-evidence/T-068-paralegal-r3-flow.py` (wrote artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json and screenshots S1, S1b, S2, S3, S3b, S4a, S4b, S4c). Analyze took under a second on the fixture backend.
- Playwright probe: `.venv/bin/python artifacts/review-evidence/T-068-paralegal-r3-edit-probe.py`.
- Manual-entry bypass probe (curl): POST /api/cases/<token>/records/r8/entry returns 422 invalid_edit "This record already has an entry; edit that entry instead." Refused.

## Verdict

changes: 0 blockers, 1 major (F1), 2 minors (F2, F3). The round 2 major (N1) and the N2 record number are fixed. verify_quickly is 3, below the ship bar of 4: the excerpt, date and letter line are one click away, but the confirmed entry still reads as unresolved and Edit is not gated up front.

## Questions for Chris

1. For F1: should an accepted entry with a confirmed date show "Needs review" at all? I assume the entry state should follow the confirm (the record is confirmed), but the persona needs the row to read settled.
2. For F2: should Edit on an undated entry be disabled (like Accept) or allowed with a saved-form warning? I would disable it.
3. The record gives no tie-breaker between April 5 and May 4. I used April 5 (US MM/DD) to run the flow; the tool did not pick. Confirm that a real paralegal is expected to check the source page for this choice, not the tool.

```json
{"card": "T-068", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 5f71a65 (app/frontend/batch.js, manual.js, review.js, timeline.js; tests/e2e/test_input.py) on a git archive HEAD snapshot served at http://127.0.0.1:7880 (LLM_BACKEND=fixture FIXTURE_SET=curated, scratch DATA_DIR); sample case evals/golden/case_01_date_formats.txt pasted; T-076 server commit 88a3393 is included as the server it depends on",
 "exercised": [
   "read personas/paralegal.md, docs/RUNBOOK.md, memory/ORCHESTRATOR_DECISIONS.md D-041, reviews/T-068-paralegal-r2.md, board show T-068 and T-076, git show 88a3393 and 5f71a65",
   "git archive HEAD into the scratchpad; started python -m app.main from the snapshot on :7880; GET /api/health 200; stopped it afterwards (port closed)",
   "Playwright artifacts/review-evidence/T-068-paralegal-r3-flow.py: paste case_01, Analyze, step 1 Accept disabled + reason + link focus (S1, S1b), step 2 batch skip count (S2), step 3 forced POST accept/edit/batch returning 422 DATE_UNCONFIRMED with case JSON unchanged and audit count unchanged, export before confirm (S3, S3b), step 4 confirm April 5, 2026, reload, accept, reload, export (S4a, S4b, S4c)",
   "Playwright artifacts/review-evidence/T-068-paralegal-r3-edit-probe.py: Edit on the undated row, typed edit, save",
   "curl: GET case, GET items/e8 before and after confirm, POST records/r8/entry (manual entry bypass) refused 422 invalid_edit",
   ".venv/bin/python -m pytest -q tests/unit -k 'date or accept' at the HEAD snapshot: 115 passed, 873 deselected",
   "read exported letter and notes after confirm and accept (artifacts/review-evidence/T-068-r3/export-letter-after-confirm-accept.txt, export-notes-after-confirm-accept.txt)"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "undated_accept_gate": 4, "undated_edit_gate": 2, "batch_skip_count": 5, "server_refusal_nothing_changed": 5, "record_number_on_undated_row": 5, "confirmed_row_copy_matches_state": 2, "letter_after_confirm": 5},
 "findings": [
   {"severity": "major", "title": "Confirmed and accepted record 8 entry still reads as an unresolved date",
    "evidence": "GET /api/cases/3xQA67xxiHA55dJbhknRNQ/items/e8 after confirm_date and accept: state needs_review, reasons [DATE_AMBIGUOUS], why 'The date can be read two ways; confirm which one is right.', review_status accepted; record r8 has date_status confirmed and record_warning flags are empty. UI row after confirm: 'Needs review' and 'Check: the date can be read two ways' (artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json S4_entry_after_confirm_text; artifacts/review-evidence/T-068-r3/S4b-accepted.png)",
    "why_it_matters": "The paralegal confirmed the date, but the row still says the date is unresolved, so she cannot tell at a glance that the accept settled it. The letter line is correct, so this is not a blocker: nothing invented reaches the letter.",
    "fix": "confirm_date clears DATE_AMBIGUOUS from the entry reasons and recomputes state (backend, mirrored in T-076). The row copy then follows.",
    "acceptance_test": "case_01: confirm April 5, 2026, then accept. The entry has no DATE_AMBIGUOUS reason, its why text does not say 'two ways', and the timeline row shows no 'Check: the date can be read two ways'."},
   {"severity": "minor", "title": "Edit and Change quote are enabled on the undated row; the date refusal appears only on save",
    "evidence": "artifacts/review-evidence/T-068-r3/T-068-r3-edit-probe.json: edit_button_disabled false, edit_button_count 1; after saving a typed edit the live message reads 'Confirm the date first. This entry has no confirmed date, so it cannot go into the letter yet.' Screenshot artifacts/review-evidence/T-068-r3/E1-edit-on-undated-row.png. Forced POST edit returns 422 DATE_UNCONFIRMED.",
    "why_it_matters": "D-041 says the UI disables the blocked action with its reason shown. Edit is blocked by the same rule, so the paralegal should see it before typing. The server refuses, so nothing is written; the open question is whether typed text survives the refusal (not tested).",
    "fix": "Disable Edit and Change quote on undated entries with the same 'Confirm the date first' reason shown beside them.",
    "acceptance_test": "On the record 8 undated row, Edit is disabled and the reason is visible before any click."},
   {"severity": "minor", "title": "Orphan confirm branch still proven only on a rewritten response (round 2 N4, still open)",
    "evidence": "5f71a65 touches UI only; tests/e2e/test_input.py still rewrites GET /api/cases/<token> for the orphan test; T-068 handoff: 'N4 ... is backend/qa-owned, not done'. The round 2 N3 excerpt fix (app/frontend/manual.js, missing-entry-excerpt line) is present in code but not exercised here.",
    "why_it_matters": "The orphan path protects the paralegal if a model call drops a record. No real run in this round shows it.",
    "fix": "A curated fixture where a record has a date to confirm and no model entry, with an E2E that runs without route rewriting.",
    "acceptance_test": "FIXTURE_SET=curated with no page.route: the record moves to Records without an entry, the verbatim excerpt is visible on the card, and the manual-entry path works."}
 ],
 "whats_right": [
   "Accept on the undated record 8 row is disabled with 'Confirm the date first' and a link that moves focus to its April 5, 2026 and May 4, 2026 buttons; the row shows 'Record 8:' and 'Open record 8' (round 2 N1 and N2 fixed).",
   "Batch accept reports '1 undated entry was skipped' and the server leaves record 8 pending; forced accept, edit and batch on it return 422 DATE_UNCONFIRMED with the case JSON unchanged apart from updated_at.",
   "After confirm and accept, the letter line reads 'April 5, 2026 — Dr. Orla Pennywhistle, phone note' with the verbatim quote and [Ex. __ / Bates __]; no 'date not stated' appears in the letter."
 ],
 "questions_for_chris": [
   "F1: should an accepted entry with a confirmed date keep 'Needs review' at all? I assume the state follows the confirm; the persona needs the row to read settled.",
   "F2: disable Edit on undated entries (like Accept), or allow it with a warning at save? I would disable it.",
   "The record gives no tie-breaker between April 5 and May 4. I used April 5 (US MM/DD) to run the flow; the tool did not pick. Confirm that a real paralegal checks the source page for this choice."
 ]}
```
