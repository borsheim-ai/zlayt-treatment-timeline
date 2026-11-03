# T-154 round 3 — claims-adjuster-reviewer (Gary Pruitt)

Verdict: pass (one minor).

Tree tested: `git archive 2de5ba9` (the T-154 r3 commit named on the card) extracted to the scratchpad. HEAD has since moved (985dbd2, other cards; `git diff --stat 2de5ba9 HEAD` touches review.js and timeline.js for T-162), so I stayed on the card's commit. App on 127.0.0.1:7875 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB), stopped by PID 79952, port confirmed down.

Deterministic checks first:
- `E2E_BASE_URL=http://127.0.0.1:7875 .venv/bin/python -m pytest tests/e2e/test_charge_confirm.py tests/e2e/test_no_console_errors.py -p no:cacheprovider -q` from the archive gave `14 passed in 18.85s` (12 + 2).

Charges panel on every case, no console errors:
- All 15 library cases (r3all.py): `charges-panel=1 run-error=None errors=[]` each. Sample case (r3sample.py, click "Use the sample case", then Analyze): `sample charges-panel: 1 run-error: 0 errs: []`. No pageerror, no console error anywhere. The round-2 ReferenceError is gone.

Round-1 and round-2 attacks, on a server-flagged charge:
- No library case carries a flagged charge on the fixture backend any more (all flags None), and my pasted ledger no longer completes there ("The AI step failed for 5 items (the second check)", FIXTURE_MISS after the T-140/T-157 backend changes). So I made the flag real on the server: in my scratch DB I set `ladder_json.confirm` on two lib06 charges using the archive's own `amounts.confirm_info` (a1 likely_total; a5 likely_duplicate naming "04/09 Therapeutic exercise $150.00" in record 2). Everything after that is the real server (GET case, review route, trace, audit). r3real.py, r3ui.py.
- Batch accept: one POST, `{"action":"accept","item_ids":["e1","e2","e3","e6","e7"]}`; no charge id; both charges stay pending; the batch bar says "2 charges are not part of this: charges are accepted one at a time, in the Charges panel."
- Accept on a1: dialog "Count this flagged charge? ... The code flagged it: Likely total ... It is not counted unless you confirm the flag by name." Cancel has focus; Escape closes it and sends nothing. Confirm sends `{"action":"accept","confirm":"likely_total"}`.
- The `a` key on the accepted, confirmed a1, three presses: no dialog, no POST, no response, live region "Accepted already. Use Undo to change it." Same for confirmed a5 (`a` twice, no dialog, no POST). This is the round-1 major, fixed at the commit.
- Undo on a1, then `a`: the flag returns, the dialog opens again, no POST until she confirms.
- Duplicate a5 via the `a` key, Tab, Enter: dialog names the other line by its text, date, amount and record ("“04/09 Therapeutic exercise $150.00” in record 2: $150.00 on 2026-04-09"), no id. Posted `confirm: likely_duplicate`. A direct API repeat accept of a5 returned 200 (the T-159 no-op).
- Audit panel (a1): "Likely total The code flagged this charge: likely total. You confirmed that flag by name at 2026-11-02T15:36:48Z, so the charge is counted. | accept, confirmed Likely total". Same for a5 with "Likely duplicate". The "How this was checked" panel has a "Flagged by the code: Likely total" step with the confirm and date, before "Counted in the total". Both hold with real backend events.
- plain() on the stale-server fallback with of in {a3, ax2_1, ax10_12}: all three print "same charge as this earlier line: $150.00 on 2026-04-09 ..." (node check of the committed regex). The round-2 minor on ids with an underscore is fixed; the duplicate sentence now comes from the backend's own text and names the line.
- Raw tokens: none in the dialogs, Audit panels or page body. One remains in the trace (finding 1).

```json
{"card": "T-154", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 2de5ba9 (T-154 r3) extracted to scratchpad; app on http://127.0.0.1:7875, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB; UI only (Playwright); flag put on two lib06 charges in the scratch DB with amounts.confirm_info, everything else the real server; evidence in artifacts/review-evidence/t154/r3*.py and r3_*.png",
 "exercised": [
  "python3 tools/board.py show T-154 (handoff r3 2de5ba9); reviews/T-154-claims-adjuster-r2.md; git log, git diff --stat 2de5ba9 HEAD for frontend files",
  "git archive 2de5ba9 into the scratchpad; app started on 7875; /api/health ok; stopped by PID 79952, port confirmed down",
  "tests/e2e/test_charge_confirm.py and test_no_console_errors.py against 7875: 14 passed in 18.85s",
  "r3all.py: sample not clicked there; all 15 library cases loaded with pageerror and console listeners: charges-panel=1, no run-error, no errors on each",
  "r3sample.py: sample case, Use the sample case then Analyze: charges-panel=1, no errors",
  "pasted SYNTHETIC ledger (r3look.py): run fails on the fixture backend with 'The AI step failed for 5 items (the second check)'; not the card's code; so r3scan.py listed amount flags per library case (none flagged) and r3real.py set the flag on two lib06 charges in the scratch DB",
  "r3ui.py on the server-flagged case: batch POST body, dialog text and focus, Escape, confirm, three a presses on confirmed a1, a on a5 then Tab/Enter, a on confirmed a5, Audit and 'How this was checked' for a1 and a5, raw-token and id scan of dialog/audit/trace/body, POST and response log",
  "r3undo.py: row buttons on an accepted charge, Undo, a after Undo opens the dialog with no POST, server state, direct repeat accept via API (200)",
  "node check of the committed plain() regex with of = a3, ax2_1, ax10_12",
  "read app/frontend/review.js (key handler, guard at the a-key branch), app/frontend/charges.js (plain, chargeFlagNote, confirmCharge)"
 ],
 "verdict": "pass",
 "scores": {"app_runs_at_commit": 5, "a_key_on_confirmed_flagged_charge": 5, "audit_and_trace_name_the_confirm": 5, "no_raw_tokens": 4, "duplicate_named_by_its_line": 5, "batch_excludes_charges": 5},
 "findings": [
  {"severity": "minor",
   "title": "The trace step for a flagged charge prints the raw flag token ('flag likely_total') in its evidence line",
   "evidence": "'How this was checked' for a1 (r3_trace_a1.png, r3ui.py output): the step 'Flagged by the code: Likely total' ends with the evidence line `flag likely_total   name Likely total   confirmed at 2026-11-02T15:36:48Z`; for a5 `flag likely_duplicate   name Likely duplicate   confirmed at ...`. The backend puts `evidence.values = {flag, name, confirmed_at}` (app/backend/trace.py:533-534) and the page prints every value as key and value. The same line style shows `kind charge` and `classified by code:amounts` on other steps, so this follows the existing trace layout. In round 2 (page-built trace) no flag token was visible; it came back when the backend T-159 events were used.",
   "why_it_matters": "A lowercase_underscore word is a machine word on a paralegal's screen; the name sits right next to it. Cosmetic, not a spec constraint (no D- decision names it), so I rate it minor, not major.",
   "fix": "Drop `flag` from the step's evidence values (the name carries it) in trace.py, or have the trace evidence renderer skip a value that equals the flag token.",
   "acceptance_test": "Open 'How this was checked' for a confirmed flagged charge: the visible text matches no /[a-z]+_[a-z_]+/ outside a Technical details disclosure."}
 ],
 "whats_right": [
  "The a-key guard now sits in the keydown handler: a on a confirmed flagged charge sends nothing and says 'Accepted already. Use Undo to change it.'; Undo brings the flag and the dialog back.",
  "All 15 library cases and the sample render the charges panel with zero page or console errors, and test_no_console_errors.py now guards that.",
  "Audit and trace now come from the backend's own events and name the code's flag, the named confirm and its time; the duplicate is told by its line ('04/09 Therapeutic exercise $150.00' in record 2), not by an id."
 ],
 "questions_for_chris": [
  "No library case or fixture-backed paste can produce a flagged charge on the fixture backend now (promotion needs a judge call; my pasted ledger misses the fixtures after the T-140/T-157 prompt changes). Do you want a library case with a code-flagged likely_total so the confirm path can be clicked on the real server without a DB edit?"
 ]}
```
