# T-076 review: paralegal-reviewer (Maria Delgado persona)

Scope: commit 88a3393 (app/backend/review.py, case_extras.py, export.py; memory/contracts/api.md; tests/unit/test_date_unconfirmed.py), exercised through the running app on a `git archive HEAD` snapshot (HEAD = 5f71a65, which contains 88a3393) at http://127.0.0.1:7880 with LLM_BACKEND=fixture FIXTURE_SET=curated and a scratch DATA_DIR. Sample case: evals/golden/case_01_date_formats.txt. The server is stopped (port closed).

## Summary

The server gate does what the card says. Every single, edit and batch accept on the undated record 8 entry is refused with 422 DATE_UNCONFIRMED and nothing changes. The manual-entry path cannot bypass it. After confirm_date the entry accepts and its letter line is correct. One defect is on the server side: confirm_date clears the record warning but leaves the entry's DATE_AMBIGUOUS reason, so the confirmed entry still reads as unresolved.

## What I checked

- Before confirm (curl against the running app): POST items/e8/review accept, edit; POST review/batch accept with ["e8"]. Responses 422 DATE_UNCONFIRMED; batch detail.rejected [{id e8, reason date_unconfirmed}]. Case JSON before and after identical except updated_at; audit event count 7 before and after.
- Manual entry on the undated record: POST records/r8/entry returns 422 invalid_edit "This record already has an entry; edit that entry instead." (no bypass).
- Confirm and accept (Playwright flow artifacts/review-evidence/T-068-paralegal-r3-flow.py, S3 and S4 steps): confirm April 5, 2026 moved the entry onto the timeline with date 2026-04-05; accept returned review_status accepted; reload kept it.
- Export before confirm: no Pennywhistle line in the letter, no "date not stated" in the letter. Internal notes list the record as "date not stated" and "not reviewed" (internal block only).
- Export after confirm and accept: artifacts/review-evidence/T-068-r3/export-letter-after-confirm-accept.txt contains "April 5, 2026 — Dr. Orla Pennywhistle, phone note" with the verbatim quote "Patient reports no new symptoms." and "Source [Ex. __ / Bates __]".
- `.venv/bin/python -m pytest -q tests/unit -k "date or accept"` at the HEAD snapshot: 115 passed, 873 deselected in 4.72s.
- Not exercised: the export path "date not confirmed, not exported" (export.py _reconcile). No API path I could find puts an accepted entry back to an undated state, so I could not reach it.

## Findings

**F1 (major) confirm_date leaves the entry's DATE_AMBIGUOUS reason; the confirmed, accepted entry still reads as unresolved.**
Evidence: GET /api/cases/3xQA67xxiHA55dJbhknRNQ/items/e8 after confirm_date(April 5, 2026) and accept: `"state": "needs_review", "reasons": ["DATE_AMBIGUOUS"], "why": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.", "review_status": "accepted"`. The record r8 is `date_status: confirmed`, `date_iso: 2026-04-05`, and the record_warning flags are empty (case JSON: record_warning flags []). The UI row shows "Needs review" and "Check: the date can be read two ways" (artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json, S4_entry_after_confirm_text; screenshot artifacts/review-evidence/T-068-r3/S4b-accepted.png).
Why it matters: the paralegal confirmed the date and the entry still says the date is unresolved. The adjuster-facing letter is not affected. I rate this major, not blocker, because nothing invented reaches the letter; it is a stale statement in the app and a state the persona cannot read as settled.
Fix: confirm_date removes DATE_AMBIGUOUS from the entry's reasons and recomputes its state, the same way it already clears the record warning and recomputes gap flags (api.md, confirm_date section).
Acceptance test: case_01, confirm April 5, 2026. GET items/e8 has no DATE_AMBIGUOUS in reasons, its why text does not contain 'two ways', and state is not needs_review once accepted.

**F2 (minor) memory/contracts/api.md contradicts itself on bulk accept.**
Evidence: memory/contracts/api.md line 74 documents batch accept ("Request: {"action": "accept" | "reset", "item_ids": [...]} ... D-041: ... DATE_UNCONFIRMED"), and line 259 says "There is no bulk accept." The batch endpoint is live (curl POST /review/batch returned 422 DATE_UNCONFIRMED).
Why it matters: the contract is what the frontend and the next reviewer read. A sentence saying there is no bulk accept, next to a documented batch endpoint, invites a wrong test.
Fix: delete "There is no bulk accept." from line 259 (the D-041 text in that paragraph is otherwise correct).
Acceptance test: grep -n "no bulk accept" memory/contracts/api.md returns nothing.

## Verdict

changes: 0 blockers, 1 major (F1), 1 minor (F2). The D-041 server gate itself passes every check I ran. verify_quickly is 3, below the ship bar of 4, because the confirmed entry still reads as unresolved and the paralegal cannot tell from the row that the confirm settled the date.

## Questions for Chris

1. Does confirm_date need to clear the entry's needs_review state, or should an accepted entry keep needs_review as a historical flag? I assume the former.
2. The export reason "date not confirmed, not exported" has no reachable path I could find. Is there a path (for example a re-run that keeps an accepted entry with a re-ambiguous date) that should be tested?

```json
{"card": "T-076", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 88a3393 (app/backend/review.py, case_extras.py, export.py; memory/contracts/api.md; tests/unit/test_date_unconfirmed.py), run through a git archive HEAD (5f71a65) snapshot at http://127.0.0.1:7880 (LLM_BACKEND=fixture FIXTURE_SET=curated, scratch DATA_DIR); sample case evals/golden/case_01_date_formats.txt",
 "exercised": [
   "read personas/paralegal.md, docs/RUNBOOK.md, memory/ORCHESTRATOR_DECISIONS.md D-041, board show T-076, git show 88a3393 diff",
   "git archive HEAD into the scratchpad; started the app from the snapshot on :7880; GET /api/health 200; stopped it afterwards",
   "curl: create case_01, run to ready; POST items/e8/review accept and edit before confirm (422 DATE_UNCONFIRMED); POST review/batch accept ['e8'] (422 DATE_UNCONFIRMED, detail.rejected); GET case before and after (identical apart from updated_at); audit event count before and after (7, 7)",
   "curl: POST records/r8/entry manual entry on the undated record (422 invalid_edit, already has an entry)",
   "Playwright artifacts/review-evidence/T-068-paralegal-r3-flow.py: forced POST accept/edit/batch in the browser session, export before confirm, confirm April 5, 2026, accept, reload, export after confirm",
   "GET items/e8 after confirm and accept (reasons still DATE_AMBIGUOUS)",
   "read artifacts/review-evidence/T-068-r3/export-letter-after-confirm-accept.txt and export-notes-after-confirm-accept.txt",
   "grep -n 'bulk accept' memory/contracts/api.md (lines 74 and 259)",
   ".venv/bin/python -m pytest -q tests/unit -k 'date or accept' at the HEAD snapshot: 115 passed, 873 deselected"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "server_gate_undated_accept_edit_batch": 5, "nothing_changed_on_refusal": 5, "manual_entry_bypass_blocked": 5, "confirm_then_accept_then_export": 4, "confirmed_entry_state_matches_record": 2, "contract_doc_consistent": 3},
 "findings": [
   {"severity": "major", "title": "confirm_date leaves DATE_AMBIGUOUS on the entry; confirmed and accepted entry still reads as unresolved",
    "evidence": "GET /api/cases/3xQA67xxiHA55dJbhknRNQ/items/e8 after confirm_date(2026-04-05) and accept: state needs_review, reasons [DATE_AMBIGUOUS], why 'The date can be read two ways; confirm which one is right. It is left out of gap checks until then.', review_status accepted. Record r8: date_status confirmed, date_iso 2026-04-05, record_warning flags []. UI row: artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json S4_entry_after_confirm_text; screenshot artifacts/review-evidence/T-068-r3/S4b-accepted.png",
    "why_it_matters": "The paralegal confirmed the date, and the entry still says the date is unresolved, so the state does not read as settled. The letter line is correct, so this is not a blocker: nothing invented reaches the letter.",
    "fix": "confirm_date removes DATE_AMBIGUOUS from the entry's reasons and recomputes its state, as it already does for the record warning and gap flags.",
    "acceptance_test": "case_01: confirm 2026-04-05, then accept. GET items/e8 has no DATE_AMBIGUOUS reason, its why text does not say 'two ways', and state is not needs_review once accepted."},
   {"severity": "minor", "title": "api.md says there is no bulk accept, one section after documenting it",
    "evidence": "memory/contracts/api.md:74 documents POST review/batch accept (item_ids, DATE_UNCONFIRMED); memory/contracts/api.md:259 reads 'There is no bulk accept.' The batch endpoint is live: POST /review/batch with ['e8'] returns 422 DATE_UNCONFIRMED.",
    "why_it_matters": "The contract is what the frontend and later reviewers read; the contradiction invites a wrong test.",
    "fix": "Delete 'There is no bulk accept.' from api.md line 259.",
    "acceptance_test": "grep -n 'no bulk accept' memory/contracts/api.md returns no match."}
 ],
 "whats_right": [
   "Accept, edit and batch accept on the undated record 8 entry all return 422 DATE_UNCONFIRMED before any write; the case JSON is unchanged apart from updated_at and the audit event count is unchanged (7 before, 7 after).",
   "Manual entry on the undated record is refused (422 invalid_edit, 'This record already has an entry'), so the date gate cannot be bypassed that way.",
   "After confirm_date the entry accepts and the letter line reads 'April 5, 2026 — Dr. Orla Pennywhistle, phone note' with the verbatim quote and [Ex. __ / Bates __]; no 'date not stated' appears in the letter."
 ],
 "questions_for_chris": [
   "F1: should confirm_date clear the entry's needs_review state as well as the record warning? I assume yes.",
   "The export reason 'date not confirmed, not exported' had no reachable path I could find. Should a test reach it (for example a re-run that re-marks an accepted entry as ambiguous)?"
 ]}
```
