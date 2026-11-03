# T-076 round 2 review: paralegal-reviewer (Maria Delgado persona)

Scope: commit f4ef2ea (app/backend/review.py, memory/contracts/api.md, tests/unit/test_date_unconfirmed.py), run as a `git archive f4ef2ea` snapshot at http://127.0.0.1:7882 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratch DATA_DIR. Sample: evals/golden/case_01_date_formats.txt, record 8 (phone note, date written "04/05/2026"). The server was stopped afterwards and port 7882 is closed. The model recorded is the model I am running as (claude-haiku-5-5), as the brief asks.

## Summary

Round-1 F1 (major) is fixed. After confirm_date to 2026-04-05, the record 8 entry reads "2026-04-05 · Dr. Orla Pennywhistle, phone note · Verified", with no "Needs review", no "Check:" line and no "two ways". It accepts in the UI, the accepted state survives a reload, and the export letter carries the entry with its date. The audit holds a confirm_date event whose `after` records `date_chosen: 2026-04-05`. Round-1 F2 (minor) is fixed: `grep "no bulk accept"` in memory/contracts/api.md returns no match.

Two items remain, neither a blocker. (1) Carried over from the T-060 frontend note: on the undated row, Accept is disabled but Edit and Change quote are enabled. The server still refuses both, so nothing invented reaches the letter. (2) Nit: outside local mode the audit endpoint drops the confirm_date before/after, so the chosen date is in the database and in the entry's date, but not in the audit view.

## What I exercised

- `.venv/bin/python -m pytest -q tests/unit -k "confirm or date"` in /Users/arsis/zlayt-pm-project:
  ```
  ........................................................................ [ 78%]
  ....................                                                     [100%]
  92 passed, 906 deselected in 3.28s
  ```
- `git show --stat f4ef2ea` (3 files: review.py, api.md, test_date_unconfirmed.py), `git merge-base --is-ancestor f4ef2ea HEAD` (ancestor), `git status --short -- app memory/contracts tests` (clean). Snapshot review.py diffed against `git show f4ef2ea:app/backend/review.py` (identical).
- App on :7882 from the snapshot, GET /api/health 200 (`synthetic_only: true`, `backend: fixture`).
- artifacts/review-evidence/T-076-paralegal-r2-check.py (Playwright plus urllib, 32 checks, all PASS, exit 0; output in artifacts/review-evidence/T-076-r2/run-output.txt, results in artifacts/review-evidence/T-076-r2/results.json):
  - pre-confirm: POST items/e8/review accept gives 422 DATE_UNCONFIRMED; item still `pending` / `needs_review`, reasons contain DATE_AMBIGUOUS; case flags contain record_warning `f_date_r8`.
  - UI (Dates to confirm form, April 5, 2026 radio, Confirm date): row after confirm reads "2026-04-05 / Dr. Orla Pennywhistle, phone note / Verified / Not reviewed yet"; no "Needs review", "Check:" or "two ways"; `data-state=verified`; Accept enabled.
  - UI: Accept clicked; row shows "Accepted", Reset appears, aria-pressed=true; after reload still no "Needs review" or "two ways".
  - API GET items/e8 (nested under `item`): reasons [], state verified, why "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", review_status accepted, date 2026-04-05, date_status confirmed.
  - Case: record 8 date_status confirmed, date_iso 2026-04-05; no record_warning flags remain.
  - GET audit (ZLAYT_MODE=local): one confirm_date event, item e8, after = `{"candidates": ["2026-04-05", "2026-05-04"], "cleared_date_ambiguous": ["e8"], "date_chosen": "2026-04-05", "date_raw": "04/05/2026", "record_id": "r8"}`.
  - GET export: letter_text contains "April 5, 2026 — Dr. Orla Pennywhistle, phone note" with the quote "Patient reports no new symptoms." and "Source [Ex. __ / Bates __]"; no "date not stated", "date not confirmed" or "two ways" in letter or notes; no UI labels or markdown in the letter.
- artifacts/review-evidence/T-076-paralegal-r2-edit-gate.py (pre-confirm control state): accept_disabled true, edit_disabled false, change_quote_disabled false, api accept 422 DATE_UNCONFIRMED. Output in artifacts/review-evidence/T-076-r2/edit-gate.json.
- `grep -n -i "no bulk accept" memory/contracts/api.md` gives no match (exit 1); `grep -c "bulk accept"` gives 0 hits for the removed sentence; api.md line 74 still documents batch accept.
- Screenshots: artifacts/review-evidence/T-076-r2/01-before-confirm.png (Needs review, "Check: the date can be read two ways", Accept greyed, Edit blue), 02-after-confirm.png (row 2026-04-05, Verified, Dates to confirm: "None. Every record has a readable date."), 03-after-accept.png (Accepted, Reset), 05-undated-row-controls.png (pre-confirm controls).
- Not exercised: Edit save on the undated row in the UI (round 1 showed the API returns 422 DATE_UNCONFIRMED for edit). Non-local audit view (the brief asked for local mode; I read present.py:193-205 instead).

## Round-1 findings, re-checked

- **F1 (major, round 1): resolved.** Confirmed entry: reasons [], why without "two ways", state verified, accepts, export line correct. The UI row loses "Needs review" and "Check:".
- **F2 (minor, round 1): resolved.** The "There is no bulk accept." sentence is gone; batch accept is documented once (api.md:74).

## Findings

**N1 (minor, carried over from the T-060 frontend note): on an undated row, Edit and Change quote are enabled while Accept is disabled.**
Evidence: edit-gate.json `"accept_disabled": true, "edit_disabled": false, "change_quote_disabled": false` (record r8, entry e8, before confirm). Screenshot artifacts/review-evidence/T-076-r2/01-before-confirm.png shows Accept greyed and Edit outlined in blue on the same row, with "Confirm the date first." below. Code: app/frontend/review.js:191 gives Accept `disabled: blocked`; app/frontend/review.js:193 appends Edit with no disabled flag. The server still refuses: `POST items/e8/review {"action":"accept"}` gives 422 DATE_UNCONFIRMED (this round), and edit gives the same 422 (round 1, reviews/T-076-paralegal.md line 11). So no unconfirmed statement reaches the letter.
Why it matters: the paralegal sees two controls that should behave the same. An Edit on an undated entry will be refused after she has typed a summary, which reads as a dead end. The fix is in the frontend (T-060), not in this card.
Fix: disable Edit and Change quote on rows with no confirmed date, with the same aria-describedby reason text as Accept (review.js:191), and send the user to Dates to confirm.
Acceptance test: on a fresh case_01 before confirm, record 8's row has btn-edit and the Change quote button disabled, and aria-describedby points to the "Confirm the date first." text. After confirm, both are enabled.

**N2 (nit): outside local mode the audit endpoint omits the chosen date.**
Evidence: app/backend/present.py:193-205. `audit_view` adds `before` and `after` to events only when `full` is true (ZLAYT_MODE=local). The confirm_date row is in the DB with `after_json` carrying date_chosen, but a non-local reviewer sees only `{id, item_id, action, at}`. memory/contracts/api.md describes the audit as metadata only outside local mode, so this matches the contract.
Why it matters: a non-local paralegal can see the chosen date on the entry itself ("2026-04-05") but not in the audit trail, so she cannot see the raw reading that was rejected from the audit. Edits keep the original visible somewhere (persona item 14); this does not, for confirm_date outside local mode.
Fix (optional, a product question): add the date_chosen and date_raw of a confirm_date event to the non-local audit view, since they carry no text from a model call.
Acceptance test: with ZLAYT_MODE unset, GET audit returns a confirm_date event whose entry includes date_chosen "2026-04-05" and date_raw "04/05/2026".

## Verdict

pass: 0 blockers, 0 majors, 1 minor (N1), 1 nit (N2). Round-1 F1 and F2 are resolved. verify_quickly is 4, at the ship bar. Every claim in the confirmed row is checkable in one row, the audit and the letter line show the chosen date, and the only uncertainty left is the undated row's Edit control (N1), which is not on the confirmed entry.

## Questions for Chris

1. N2: should a non-local audit show the chosen date and raw reading for confirm_date, as it does in local mode? I assume that is a contract choice, not a defect.
2. N1: should the T-060 frontend note be a new card, or stay as a note on T-060? I have not created or moved any card.

```json
{"card": "T-076", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f4ef2ea (app/backend/review.py, memory/contracts/api.md, tests/unit/test_date_unconfirmed.py), run as git archive f4ef2ea at http://127.0.0.1:7882 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch DATA_DIR), stopped afterwards; sample case evals/golden/case_01_date_formats.txt, record 8",
 "exercised": [
   "read personas/paralegal.md, reviews/T-076-paralegal.md (round 1), memory dir, board show T-076, git show f4ef2ea --stat and the review.py and api.md diff, git merge-base ancestry, git status (clean)",
   "pytest: .venv/bin/python -m pytest -q tests/unit -k \"confirm or date\" -> 92 passed, 906 deselected",
   "git archive f4ef2ea into the scratchpad; app started from the snapshot on :7882; GET /api/health 200; stopped (port closed)",
   "artifacts/review-evidence/T-076-paralegal-r2-check.py: 32 checks PASS (pre-confirm 422 gate; UI confirm, accept, reload on the record 8 row; API item after confirm and accept; case record and record-warning flags; local-mode audit confirm_date event; export letter and notes)",
   "artifacts/review-evidence/T-076-paralegal-r2-edit-gate.py: pre-confirm Accept disabled, Edit and Change quote enabled, API accept 422 DATE_UNCONFIRMED",
   "grep -n -i 'no bulk accept' memory/contracts/api.md (no match); api.md line 74 batch accept still documented",
   "read present.py:193-205 (audit_view) and review.js:191-193 (Accept and Edit controls)",
   "screenshots 01-before-confirm, 02-after-confirm, 03-after-accept, 05-undated-row-controls under artifacts/review-evidence/T-076-r2/"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "confirm_clears_entry_state": 5, "accept_after_confirm": 5, "confirm_event_records_chosen_date_local": 5, "api_md_no_bulk_accept_removed": 5, "pre_confirm_gate_regression": 5, "undated_row_controls_gated": 3},
 "findings": [
   {"severity": "minor", "title": "Edit and Change quote enabled on an undated row while Accept is disabled (carried over from T-060)",
    "evidence": "artifacts/review-evidence/T-076-r2/edit-gate.json: accept_disabled true, edit_disabled false, change_quote_disabled false (entry e8, record r8, before confirm); screenshot artifacts/review-evidence/T-076-r2/01-before-confirm.png; app/frontend/review.js:191 (Accept disabled: blocked) vs app/frontend/review.js:193 (Edit appended with no disabled flag); server 422 DATE_UNCONFIRMED on accept (this round) and edit (reviews/T-076-paralegal.md line 11)",
    "why_it_matters": "The paralegal sees two controls that should behave alike. Edit on an undated entry is refused only after she has typed, which reads as a dead end. Nothing unconfirmed reaches the letter, so this is not a blocker.",
    "fix": "Disable Edit and Change quote on rows with no confirmed date, with the same aria-describedby reason as Accept (review.js:191), pointing to Dates to confirm. Owner: frontend, T-060.",
    "acceptance_test": "Fresh case_01 before confirm: record 8 row has btn-edit and Change quote disabled, with aria-describedby pointing to the 'Confirm the date first.' text; after confirm both are enabled."},
   {"severity": "nit", "title": "Outside local mode the audit endpoint omits the confirm_date chosen date",
    "evidence": "app/backend/present.py:193-205 (audit_view adds before/after only when full is true, i.e. ZLAYT_MODE=local); memory/contracts/api.md audit line says metadata only outside local mode",
    "why_it_matters": "On the non-local deployment the chosen date is visible on the entry but not in the audit trail, so the rejected reading is not shown there. This matches the documented contract, so it is a design choice, not a violation.",
    "fix": "Optional: include date_chosen and date_raw of confirm_date events in the non-local audit view (no model text involved).",
    "acceptance_test": "ZLAYT_MODE unset: GET audit includes a confirm_date event whose entry has date_chosen '2026-04-05' and date_raw '04/05/2026'."}
 ],
 "whats_right": [
   "confirm_date clears DATE_AMBIGUOUS and the record warning: the record 8 row reads 2026-04-05, Verified, no 'Needs review', no 'two ways', and accepts in the UI and survives a reload.",
   "The confirm_date audit event (local mode) records date_chosen 2026-04-05, date_raw 04/05/2026, the candidates and the cleared item id e8.",
   "api.md no longer says 'There is no bulk accept.'; batch accept is documented once at line 74."
 ],
 "questions_for_chris": [
   "N2: should the non-local audit show the chosen date and raw reading for confirm_date, as local mode does? I assume it is a contract choice.",
   "N1: should the T-060 frontend note become its own card, or stay a note on T-060? I have not changed any card."
 ]}
```
