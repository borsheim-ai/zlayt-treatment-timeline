# T-154 review — claims-adjuster-reviewer (Gary Pruitt)

Verdict: changes (one major, three minor, one nit; no blocker).

I attacked the one thing that matters to me: can a paralegal slip a restated or double-counted charge into the total? Through the UI I could not do it with a batch, and I could not accept a flagged charge without the named confirm. The flag is stated in the row and again in the dialog before she confirms. One keyboard path is wrong, though. The `a` key on an already-confirmed flagged charge reopens the "not counted" dialog and, if she confirms, writes a second accept decision.

Tree tested: `git archive HEAD` (d34182b, which holds commits 611bdcc and e2bb025 for T-154). The live working tree has uncommitted edits to `app/backend/*` (T-140 in flight), so I did not use it. Server on 127.0.0.1:7872 with LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. I stopped it by PID 46068 and confirmed the port is down.

What I did, by UI only (Playwright against the real page):
- lib10: the batch bar says "4 charges are not part of this: charges are accepted one at a time, in the Charges panel." The batch POST carried `["e2","e3","e5","e6","e7","e9"]`, entries only. All 4 charges and 7 unclear/rate rows stayed pending, accepted total $0.00. Shift+A on a charge row opens nothing. Shift+A on an entry row opens "Accept 6 verified entries?" with "Charges (accepted one at a time), flags ... are not part of this", and its POST was again entries only.
- lib11: same result. Batch POST `["e3","e5","e6","e7","e8"]`, charges pending, total $0.00.
- Neither lib10 nor lib11 has a flagged charge at HEAD, so I could not test the flag path on them. (The e2e file says the same.)
- Pasted SYNTHETIC ledger (`artifacts/review-evidence/t154/ledger.txt`). Demo mode refuses unrecorded pasted text (409 `demo_mode_unsupported_input`), so I copied the ledger into `evals/golden/` of my scratch copy of the archive so the hash matches. It yields a4 $350.00 `likely_total` and a5 $150.00 `likely_duplicate` of a3.
  - Row text before any click: "Likely total This amount equals the sum of the other charges in its record ... Counting it may count the same charges twice." and "Likely duplicate This looks like the same charge as a3: therapeutic exercise $150.00 on 2026-04-09, already listed from record 2. Counting both would count one service twice."
  - Click Accept on a4 opens "Count this flagged charge? The code flagged it: Likely total ..." with Cancel focused. Enter, Escape and Cancel all left it pending with 0 POSTs.
  - `a` on a5 opens the dialog. While it is open, `a`, `d` and Shift+A did nothing. Tab then Enter sent `{"action":"accept","confirm":"likely_duplicate"}`.
  - `a` then Enter with no wait left a4 pending.
  - Undo of a confirmed flagged charge brings the flag back, and accepting it asks again. Dismiss then Undo then Accept also asks again.
  - Nine rapid `a` keys from a1 sent only two POSTs, both on a1. A held key does not accept everything.
  - After Cancel or Escape, focus stays on the row, and `j` moves on.
- Batch on the pasted ledger is disabled (0 verified entries on the fixture backend), so there the batch rule is covered only by lib10 and lib11.
- Deterministic: `E2E_BASE_URL=http://127.0.0.1:7872 .venv/bin/python -m pytest tests/e2e/test_charge_confirm.py tests/unit/test_e2e_contract.py -p no:cacheprovider -q` gave `10 passed in 8.33s`.

Findings are in the JSON block. Evidence scripts and screenshots are in `artifacts/review-evidence/t154/` (uiA to uiF, peek*.py, *.png).

```json
{"card": "T-154", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD d34182b (T-154 commits 611bdcc, e2bb025) extracted to scratchpad; app on http://127.0.0.1:7872, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB; UI only (Playwright); cases lib10, lib11, pasted SYNTHETIC ledger artifacts/review-evidence/t154/ledger.txt (placed in the scratch copy's evals/golden so demo mode accepts the paste); read D-059 and D-060",
 "exercised": [
  "python3 tools/board.py show T-154; D-059 and D-060 in memory/ORCHESTRATOR_DECISIONS.md; app/frontend/charges.js, review.js (RV.act, key handler), batch.js; git show 611bdcc",
  "git archive HEAD into the scratchpad; app started on port 7872 (HOST/PORT env), stopped by PID 46068, port confirmed down",
  "UI lib10: Accept all verified entries button (POST ids entries only), Shift+A on an entry row (dialog text and POST) and on a charge row (no dialog), `a` on a charge row, charge-note text in the batch bar",
  "UI lib11: same batch checks; 4 charges stayed pending, total $0.00",
  "UI pasted ledger: row flag text before click, Accept click and `a` key on flagged likely_total and likely_duplicate rows, Enter/Escape/Cancel/Tab+Enter on the dialog, keys a/d/Shift+A while it is open, `a`+Enter with no wait, nine rapid `a`, dismiss/undo/accept, undo of confirmed charge, `a` on an already-confirmed flagged charge, focus after cancel, j after cancel",
  "UI: How-this-was-checked panel and Audit panel on flagged and confirmed charges",
  "tests/e2e/test_charge_confirm.py and tests/unit/test_e2e_contract.py against my port: 10 passed",
  "read-only API reads (GET case, GET export) to learn which charges carry flags; no state changed through the API",
  "grep of HEAD export.py/trace.py for any note of a confirmed flag; extract_amounts run on HEAD vs the dirty tree for the Apr 16 vs 04/16 duplicate"
 ],
 "verdict": "changes",
 "scores": {"batch_excludes_charges": 5, "flagged_charge_needs_named_confirm": 4, "flag_stated_before_confirm": 5, "keyboard_paths": 3, "audit_of_the_confirm": 2},
 "findings": [
  {"severity": "major",
   "title": "The `a` key on an already-accepted, already-confirmed flagged charge reopens 'Count this flagged charge?' with 'It is not counted', and confirming records a second accept decision",
   "evidence": "Pasted ledger, a5 $150.00 (Likely duplicate). Confirm it (POST {\"action\":\"accept\",\"confirm\":\"likely_duplicate\"} -> 200, row data-review=accepted, 'You confirmed this flag and counted the charge.'). Focus the row and press `a`: the page POSTs {\"action\":\"accept\"} -> 422 and opens the dialog 'Count this flagged charge? The code flagged it: Likely duplicate ... It is not counted unless you confirm that flag by name (likely_duplicate). | Charge: $150.00. It is not counted unless you confirm the flag by name.' The charge is already in the accepted total. Clicking Confirm -> 200, and the audit panel then reads 'Your decisions | accept | 2026-11-02T14:40:00Z | accept | 2026-11-02T14:40:02Z'. The Accept button on the same row correctly says 'Accepted already. Use Undo to change it.' Probe: artifacts/review-evidence/t154/uiF.py; screenshot artifacts/review-evidence/t154/ledger_reaccept_dialog.png. Cause: review.js key branch `if (key === \"a\") RV.act(id, {action:\"accept\"}, ...)` has no already-accepted guard for amounts, and the server's confirm_error (review.py:178-186) does not check the item's review_status, so a flagged accepted charge answers 422.",
   "why_it_matters": "The tool tells the paralegal a charge 'is not counted' when it is counted. A keyboard repeat on a flagged item then writes a second accept decision into the audit trail. I would use two accept decisions on one flagged charge to question who decided what. A false statement about the total is the kind of line I discount a package on.",
   "fix": "In the `a` key branch, treat an already-accepted item (any kind) as the button does: say 'Accepted already. Use Undo to change it.' and send nothing. Also have the server return 200 no-op, or a different code, for an accept on an item already accepted with its flag confirmed, so a stale page cannot reopen the dialog.",
   "acceptance_test": "e2e on a flagged charge: confirm it, focus the row, press `a`; assert the charge-confirm dialog does not open, no review POST is sent, the live-region says it is already accepted, and the audit panel still shows exactly one accept."},
  {"severity": "minor",
   "title": "Nothing in the paralegal's or firm's record shows a counted charge was a flagged one that she confirmed over the code's flag",
   "evidence": "After confirming a4 (Likely total) and a5 (Likely duplicate): Audit panel reads 'Your decisions | accept | 2026-11-02T14:38:26Z' with no confirm or flag. The 'How this was checked' panel for a4 has steps 'Rule says what the figure is: Passed - A billing phrase in the record labels this figure a charge, so it counts toward the total once you accept it.' and 'What you need to do: Accept, edit or dismiss this item.' No step mentions the flag or the confirm; the regex for flag/confirm/Likely over the trace text finds only the word 'total' in 'counts toward the total'. HEAD app/backend/export.py and trace.py contain no mention of the stored ladder.confirm.confirmed_at (grep for 'confirmed_at|likely' in export.py/trace.py returns nothing). The export could not be fetched through the fixture backend (422 judge_not_run), so I could not read the internal notes; the code shows no line for it. Screenshots: ledger_trace.png, ledger_accepted.png.",
   "why_it_matters": "D-059 keeps the human as the final check. If a likely total or duplicate is counted, the firm's own record should say that she confirmed it. Otherwise the trail reads as an ordinary accept, and the trace says the figure simply 'counts toward the total once you accept it'.",
   "fix": "Record the named confirm in the review event and show it in 'Your decisions' ('accept, confirmed Likely total'). Add a trace step for the code flag ('Likely total: needs your named confirm'), with a next action that names the confirm. List confirmed-flag charges in the internal notes (not the letter, which stays R-EX-8 neutral).",
   "acceptance_test": "After confirming a flagged charge, the Audit panel's 'Your decisions' line names the flag, the case trace for that item has a flag step whose status is 'needs your decision' until she confirms, and internal_notes_text lists the charge with the flag name; the letter total line is unchanged."},
  {"severity": "minor",
   "title": "The fallback dialog (page did not know the charge was flagged) shows the server's raw sentence, including a machine word, and the dialog text differs from the first path",
   "evidence": "Same trigger as the finding above, dialog tail: '...Counting both would count one service twice. It is not counted unless you confirm that flag by name (likely_duplicate).' plus a second line 'It is not counted unless you confirm the flag by name.' The first path (row already flagged) shows only f.message. review.js builds the fallback with `message: e.message`, which is the whole 422 message ending in the confirm_with token.",
   "why_it_matters": "She sees two repeated 'not counted' sentences and an internal token in a screen meant to be plain words.",
   "fix": "In the fallback, pass the flag's own message (detail.message or the stored flag message) rather than the whole error sentence, or strip the 'It is not counted unless ... (token)' tail.",
   "acceptance_test": "e2e with the stub answering 422 for an unflagged-looking charge: the dialog's charge-confirm-msg contains no parenthesised flag token and no repeated 'not counted' sentence."},
  {"severity": "nit",
   "title": "Flag sentence and shortcut text leave two small gaps",
   "evidence": "The likely_duplicate sentence says 'the same charge as a3' (an internal id that is not shown in any column); date, service and record number follow it, so the paralegal can find it. The shortcut sheet (review.js:413) says 'a: Accept the selected item, then move to the next one that needs a decision' and does not say a flagged charge asks first.",
   "why_it_matters": "Minor friction; the substance of the flag is stated.",
   "fix": "Drop the internal id from the sentence, or show it as a link to the row. Add 'a flagged charge asks first' to the `a` line.",
   "acceptance_test": "Flag message has no /\\ba\\d+\\b/; shortcut sheet text for `a` contains 'flagged'."}
 ],
 "whats_right": [
  "Batch accept never sends a charge id (lib10 and lib11 POSTs are entries only), the bar and the Shift+A dialog both say charges are accepted one at a time, and Shift+A on a charge row does nothing.",
  "A flagged charge cannot be counted without the named confirm: Accept, `a`, Enter, Escape and Cancel all leave it pending, Cancel holds focus, other shortcut keys are inert while the dialog is open, and the body carries confirm only after Tab+Enter on the named button.",
  "The flag is stated in the row before any click and again in the dialog, in the code's fixed sentence with no model prose, and Undo or Dismiss then Undo brings the flag and the confirm requirement back."
 ],
 "questions_for_chris": [
  "HEAD d34182b flags a same-format duplicate (04/09/2026 therapeutic exercise $150.00 in two statements) but does not merge or flag the same service when one statement writes 'Apr 16, 2026' and the other '04/16/2026' (a7 $350.00 stayed unflagged and acceptable in my pasted ledger). D-060 says duplicates match in any date format. The uncommitted amounts.py in the working tree merges it (extract_amounts gave record_nos [2, 3]), so this looks like T-140 r3 in flight, not T-154. I did not count it against T-154; please confirm it lands before the gate.",
  "The fixture backend cannot show a flagged charge in lib10 or lib11, and demo mode refuses pasted text unless it matches a golden file. Is a flagged-charge library case (qa) planned so this can be checked on the real server without a stub?"
 ]}
```
