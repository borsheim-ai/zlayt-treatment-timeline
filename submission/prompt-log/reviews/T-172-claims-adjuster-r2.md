# T-172 round 2 review: claims-adjuster-reviewer (Gary Pruitt), commit 04ebe39

Verdict: **pass** (0 findings).

UI only, on a `git archive 04ebe39` copy. Servers were two spare ports and were stopped by PID (71749, 71752); `lsof` shows 0 listeners on 7881 and 7882.
- **Round-1 major, closed.** On the real API a likely-duplicate line (pasted two-record SYNTHETIC ledger, scripted LLM from the commit's tests/e2e/_scripted_server.py) now shows its "Likely duplicate" chip and the server's message in the row before any click (charge-flag chips 1; the page saw `count_confirm: likely_duplicate`, `flag: None`). "Count this charge" opens the flag dialog first ("Count this flagged charge? ... Confirm likely duplicate and accept"), and the "I checked this is a separate charge for a service" dialog comes second. Cancel at the flag dialog counted nothing (total stayed $150.00, no count POST, no separate-charge dialog). Cancel at the second dialog counted nothing. With both confirmed, the one count POST is `{action: count, confirm: separate_charge, confirm_flag: likely_duplicate}`, and the row says "You confirmed this flag and counted the charge." The same holds by keyboard (Cancel has focus in the flag dialog; Escape cancels).
- **lib11** from the library list (fixture backend): $250, $180 and $2,310 offer Count; Cancel counts nothing; mouse, keyboard-only ($180: Enter on the focused Cancel counts nothing, then Tab reaches the named confirm) and mouse reach **$6,000.00**; exported letter "Billed charges accepted from these records: $6,000.00". At 390 there is no horizontal overflow and the Count and dialog buttons are 44 px.
- **Balance line** ($2,166.00) and the $2,740 total, $300 payment and $274 adjustment rows offer nothing; keys a, c and Enter on the balance row sent no count POST.
- `tests/e2e/test_count_duplicate.py`: 3 passed. The stub is gone: `grep count_confirm app/frontend` reads it at charges.js:79, :127 and :128, and the only `page.route` left in test_count_charge.py are 422 error-path handlers. test_count_charge.py against the fixture server: 8 passed.

Evidence: artifacts/review-evidence/T-172-adjuster-r2/ (ui_lib11.py, ui_lib11.txt, ui_dup_r2.py, ui_dup_r2_mouse.txt, ui_dup_r2_kb.txt, dup_*.png, lib11_*.png).

```json
{"card": "T-172", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 04ebe39 (frontend charges.js count_confirm read before the first dialog; tests/e2e/test_count_duplicate.py), run on a git archive of 04ebe39. UI only: http://127.0.0.1:7881 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB) for lib11 from the library list; http://127.0.0.1:7882 (the same tree's tests/e2e/_scripted_server.py, scripted LLM, scratch DB) for a pasted SYNTHETIC two-record ledger that yields a real likely_duplicate countable line",
 "exercised": [
  "git archive 04ebe39 into the scratchpad; git show 04ebe39 -- app/frontend/charges.js; read tests/e2e/test_count_duplicate.py and tests/e2e/_scripted_server.py; read reviews/T-172-claims-adjuster.md",
  "artifacts/review-evidence/T-172-adjuster-r2/ui_lib11.py against :7881: reason line and count buttons on all 7 not-counted rows; accept $3,260; Count $250 then Cancel (no count POST), named confirm by mouse; $180 by keyboard only (Enter on the focused Cancel counts nothing, then Tab and Enter); $2,310 by mouse; total $6,000.00; keys a, c, Enter on the $2,166.00 balance row (0 count POSTs); accept-verified batch and Export letter total line; 390x844 overflow 0, 44 px buttons; pageerrors none",
  "artifacts/review-evidence/T-172-adjuster-r2/ui_dup_r2.py against :7882 by mouse and by keyboard: pasted ledger through the input box and Analyze; the case view the page received (count_confirm likely_duplicate, flag None); row text and charge-flag chips before any click; Count -> flag dialog first; Cancel/Escape there; confirm flag -> separate-charge dialog; Cancel there; both confirmed; POST bodies and accepted total; output ui_dup_r2_mouse.txt, ui_dup_r2_kb.txt, dup_*.png",
  "pytest tests/e2e/test_count_duplicate.py -p no:cacheprovider -v from the archive tree -> 3 passed",
  "E2E_BASE_URL=http://127.0.0.1:7881 pytest tests/e2e/test_count_charge.py -p no:cacheprovider -q -> 8 passed",
  "grep -rn count_confirm app/frontend (charges.js:79, :127, :128); grep page.route in test_count_charge.py and test_count_duplicate.py (only 422 error-path handlers)",
  "both servers killed by PID (71749, 71752); lsof listener count 0 on 7881 and 7882"
 ],
 "verdict": "pass",
 "scores": {"lib11_reasons_and_count": 5, "rule_excluded_offers_nothing": 5, "duplicate_flag_shown_before_confirm": 5, "duplicate_confirm_asked_first_by_name": 5, "keyboard": 5, "mobile_390": 5},
 "findings": [],
 "whats_right": [
  "A real likely_duplicate line shows its chip and the server's message in the row before any click, and Count asks for the duplicate flag by name first, then the separate-charge confirm; Cancel at either dialog counts nothing and the one count POST carries confirm_flag likely_duplicate.",
  "lib11 reaches $6,000.00 by mouse and by keyboard (Cancel has focus, Enter alone counts nothing) and at 390 px with no overflow; the letter reads 'Billed charges accepted from these records: $6,000.00'.",
  "The balance, payment, adjustment and total rows offer no count control, and keys on the focused balance row send no count; the e2e now runs against a real server with no stubbed flag."
 ],
 "questions_for_chris": []}
```
