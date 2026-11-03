# T-172 review: claims-adjuster-reviewer (Gary Pruitt), commits c4915a0 and d0d8458

Verdict: **changes** (1 major).

UI only, on a git archive of a938bd2 (it holds both commits and the T-171 r2 backend).
- **lib11**, loaded from the library list in the page, on the fixture server: every not-counted row shows its plain reason. Only $250, $180 and $2,310 offer "Count this charge". The named confirm counts each one, and the total reaches $6,000.00. The exported letter reads "Billed charges accepted from these records: $6,000.00". The $2,166.00 balance, $300 payment, $274 adjustment and $2,740 total rows offer nothing; keyboard keys on the balance row sent no count.
- **Keyboard:** Cancel has focus, so Enter alone counts nothing, and Tab reaches the named confirm.
- **390 px:** no horizontal overflow, and the buttons are 44 px tall.

**Major:** a real `likely_duplicate` line (pasted two-record ledger, same tree with a scripted LLM) shows no flag in its row and none in the Count dialog. The page reads `a.flag`, but the API sends the warning in `count_confirm`. The paralegal clicks "I checked this is a separate charge for a service" first. Only the server's 422 then brings up the "Likely duplicate" dialog. That dialog asks for the flag by name, and Cancel or Escape there counts nothing. The letter is not inflated, but the warning comes after her first confirm. The e2e passes because it stubs `flag` onto the amount.

Not a T-172 defect: the page offers "Count this charge" on whatever the backend marks countable. The T-171 r2 blocker (insurer, allowed and lifetime lines that name a service) would therefore show a Count button in the UI too.

Evidence: artifacts/review-evidence/T-172-adjuster/ (ui_lib11.py, ui_lib11.txt, ui_dup.py, ui_dup_mouse.txt, ui_dup_kb.txt, lib11_*.png, dup_*.png; serve_scripted.py is in ../T-171-adjuster-r2/; the JSON below was pre-validated as T-172-claims-adjuster.json).

```json
{"card": "T-172", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commits c4915a0 and d0d8458 (frontend), run on a git archive of a938bd2, which contains both and the T-171 r2 backend (HEAD moved to d865d21, a qa test commit only; no app/ change). UI only: http://127.0.0.1:7873 (fixture backend, ZLAYT_MODE=local, scratch ZLAYT_DB) for lib11 loaded from the UI library list; http://127.0.0.1:7874 (the same tree's create_app with a scripted LLM call factory) for a pasted SYNTHETIC two-record ledger, because no library case has a likely_duplicate countable line and demo mode refuses unrecorded text",
 "exercised": [
  "read app/frontend/charges.js count code (lines 67-191), tests/e2e/test_count_charge.py, memory/contracts/api.md line 402 (count_confirm), python3 tools/board.py show T-172",
  "E2E_BASE_URL=http://127.0.0.1:7873 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_count_charge.py tests/e2e/test_charge_confirm.py tests/e2e/test_charges.py -> 26 passed (from the archive)",
  "artifacts/review-evidence/T-172-adjuster/ui_lib11.py at 1280: lib11 from the library list; the reason line and count buttons on all 7 not-counted rows; accept $3,260; Count $250 then Cancel (no POST), then the named confirm by mouse; $180 by keyboard only (Enter on the focused Cancel, then Tab and Enter); $2,310 by mouse; accepted total after each; keys a, c and Enter on the focused $2,166.00 balance row; accept-verified batch and Export, letter total line; pageerror and console listeners; output ui_lib11.txt and lib11_*.png",
  "ui_lib11.py at 390x844: reason boxes and Count button boxes, document overflow, Count dialog button boxes, count $180",
  "ui_dup.py by mouse and by keyboard on :7874: pasted ledger (record 1 '04/16/2026 manual therapy charge $150.00.', record 2 'Manual therapy charge $150.00.') through the input box and Analyze; the GET case the page received; row text and charge-flag chips before any click; accept the dated charge; Count on the undated line; Count dialog; the flag dialog; Cancel or Escape there; then confirm both; POST bodies and accepted total; output ui_dup_mouse.txt, ui_dup_kb.txt, dup_*.png",
  "both servers killed by PID (60957, 64437); lsof listener count 0 on 7873 and 7874"
 ],
 "verdict": "changes",
 "scores": {"lib11_reasons_and_count": 5, "rule_excluded_offers_nothing": 5, "duplicate_flag_shown_before_confirm": 2, "duplicate_confirm_asked_by_name": 4, "keyboard": 5, "mobile_390": 5},
 "findings": [
  {"severity": "major",
   "title": "The page never reads count_confirm, so a likely_duplicate line shows no flag in its row or in the Count dialog; the warning appears only after she has clicked 'I checked this is a separate charge for a service'",
   "evidence": "ui_dup_mouse.txt: the GET case the page received has a2 '$150.00' unclear countable True with count_confirm {'flag': 'likely_duplicate', 'message': 'This looks like the same charge as “04/16/2026 manual therapy charge $150.00.” in record 1: $150.00. Counting both would count one service twice.', ...} and flag None. 'ROW a2 unclear ... Not counted: The record's document type is unknown ... Count this charge Keep in notes Dismiss | charge-flag chips: 0'. Count dialog: 'Count this charge? Amount: $150.00 Not counted now: ... Cancel I checked this is a separate charge for a service | flag line visible: False'. POST bodies: [{'action': 'accept'}, {'action': 'count', 'confirm': 'separate_charge'}, ...]: only the server's 422 brings up 'Count this flagged charge? The code flagged it: Likely duplicate ...'. Same by keyboard (ui_dup_kb.txt). Cause: app/frontend/charges.js:79 and :126 (heldFlag) and :139 read a.flag; grep finds count_confirm in 0 files under app/frontend and 0 under tests/e2e. The e2e that passes stubs a `flag` field onto the amount (tests/e2e/test_count_charge.py:258 DUP, :272 x[\"flag\"] = dict(DUP)), a shape the API does not send on a countable line (contract line 402: count_confirm).",
   "why_it_matters": "The duplicate gate still holds: Cancel or Escape at the flag dialog counted nothing (total stayed $150.00), and the count only went through with confirm_flag likely_duplicate. So the letter is not inflated by the UI. But the paralegal signs 'separate charge for a service' for a line the code has already said is probably the same as record 1's, and only then hears about it. The handoff says the row and the Count dialog show the flag; on the real API they do not. AC 1's duplicate spec tests a stub, not the contract.",
   "fix": "Read a.count_confirm (fall back to a.flag) in the row chip, heldFlag and the Count dialog's flag line, so the warning shows before the first confirm and the first POST already carries confirm_flag. Change the e2e stub to set count_confirm (the contract field), and add one spec against the real API with a pasted or recorded likely_duplicate ledger.",
   "acceptance_test": "E2E on the real server: a case with a dated accepted '$150.00 manual therapy' charge and an undated 'Manual therapy charge $150.00.' line: the undated row shows a 'Likely duplicate' chip before any click, the Count dialog's count-confirm-flag is visible with the server's message, and the first count POST is {action: count, confirm: separate_charge, confirm_flag: likely_duplicate}; Cancel at either dialog sends no count."}
 ],
 "whats_right": [
  "lib11 from the library list: all 7 not-counted rows show 'Not counted: <server reason>'; only $250, $180 and $2,310 offer 'Count this charge'; after counting them the total reads $6,000.00 and the exported letter says 'Billed charges accepted from these records: $6,000.00'.",
  "Rule-excluded rows ($2,740 total, $300 payment, $274 adjustment, $2,166 balance) have no count control, and a, c and Enter on the focused balance row sent no count POST; Cancel has focus, so Enter alone counts nothing, and Tab reaches the named confirm.",
  "At 390 px there is no horizontal overflow, the reason lines and the 44 px Count / dialog buttons fit, and on the duplicate path Cancel or Escape at the flag dialog counts nothing while the confirmed count sends confirm_flag likely_duplicate and the row then says 'Likely duplicate You confirmed this flag and counted the charge.'"
 ],
 "questions_for_chris": []}
```
