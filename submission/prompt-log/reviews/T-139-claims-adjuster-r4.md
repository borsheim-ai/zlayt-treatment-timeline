# T-139 — claims-adjuster-reviewer (BI adjuster / defense adversary), round 4 (final check)

**Verdict: changes.** 0 blockers, 2 majors, 2 minors.

**Scope.**
- Card commits `985dbd2` and `a7302fe`. HEAD is `a7302fe1713c10298a20e12a736cf7529c0747d5`; I ran from a `git archive HEAD` copy in the session scratchpad (`t139r4/`).
- The app ran on spare port 7878 with `LLM_BACKEND=fixture ZLAYT_MODE=local` and `ZLAYT_DB` in the scratchpad. `/api/health` returned `"backend":"fixture","demo_mode":true`.
- Pasted text returns `demo_mode_unsupported_input`, so I could not paste a new record into the live app. Record-text attacks ran through the production functions (`charge_text.check`, `export.build_export`, `export.money_blockers_for_case`), using a case dict that `store.export_case` built from my scratch DB.

**Deterministic checks (archive tree):**
- The seven `tests/unit/test_t139_*.py` files: **321 passed**.
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, "held_out_entries": 11}`.
- Full `tests/unit`: **4946 passed, 8 skipped**.

**What r4 fixed (re-run of my r3 attacks):**
- **All 7 r3 summary edits are now refused.** Each returned **422** at edit time and the message names the expression, e.g. "The summary states a dollar amount (billed at two thousand one hundred fifty)" and "(paid in full 3)". The letter after accept-all has none of them (`edit_attack_r4.txt`).
- **The three record wordings are held.** `Patient responsibility 1,200.00`, `Paid in full 2,150.00` and `Lost wages 1,800.00` are held as a quote. `narrow_excerpt` drops each of them from a clinical quote (`record_text_probe.txt` part 1).
- **The trace export gate now matches GET /export.** I stored three money summaries directly in the DB, past the edit check. The gate went `ready:false`, with `money_in_letter: 3` and blockers that name line 20/24/32 and entry e5/e6/e8. GET /export returned 422 `export_blocked` in all three styles. After I restored the summaries, both were ready again: gate ready, export 200. `ready_equals_allowed` was true in every state (`gate_vs_export.json`).
- **Held-out hints now give the true reason.**
  - lib06 e4, lib09 e7, lib11 e9, lib12 e10 and lib15 e7/e9: "amounts were read but not totaled". Their amounts are all unclear or rate.
  - lib10 e8 and lib14 e7: "No amount was read". No amount items exist on r8 or r7.
  - lib14 e8: "already listed". Its charges a2 and a4 are accepted.

**Still open / new:**
1. **New wordings outside 7c reach the carrier letter, live (major).** These are amounts in words after a money noun that is not on the closed list:
   - "ambulance copay of twenty"
   - "deductible of five hundred"
   - "patient spent fifteen hundred out of pocket"
   - "lost eighteen hundred in wages"
   - "patient responsibility twelve hundred"
   - "paid in full twenty-one fifty"

   Each edit returned 200 and the export returned 200 with the edit in the letter. The gate and letter_check are blind too, because they share the detector. Record-text digit forms are also missed: "Insurer reimbursed 1,412.50", "Copayment 40.00", "Coinsurance 430.00", "MRI cost the patient 2,150", "Policy limits 30,000", "Med-pay 5,000.00".
2. **NEW PATH: the export gate skips the whole BILLED CHARGES section (major).** An accepted charge's quote line prints the record sentence. If that sentence also states a paid amount, an adjustment, a patient-responsibility amount or wages (with or without '$'), it reaches the carrier letter. The gate returns [] and the export builds, while `evals/letter_check.violations` flags the same letter. The gate and the eval disagree on structure.

```json
{"card": "T-139", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commits 985dbd2 + a7302fe; git archive HEAD (a7302fe) in session scratchpad t139r4/; app http://127.0.0.1:7878 (LLM_BACKEND=fixture, ZLAYT_MODE=local, scratch ZLAYT_DB); sample; lib01, lib06, lib09, lib10, lib11, lib12, lib14, lib15; record-text attacks through production functions on a store.export_case dict (pasted text is refused in demo mode)",
 "exercised": [
  "read personas/claims-adjuster.md, reviews/T-139-claims-adjuster-r3.md, memory/SCOPE_CUTS.md row 7c, python3 tools/board.py show T-139, my memory dir",
  "git log --oneline -6 (HEAD a7302fe); git show --stat 985dbd2 a7302fe; git show of export.py, trace.py, store.py diffs; read app/backend/money.py",
  "archive tree: pytest tests/unit/test_t139_r4.py test_t139_r3.py test_t139_trace.py test_t139_unmarked.py test_t139_narrow.py test_t139_charge_text.py test_t139_letter_eval.py -> 321 passed",
  "archive tree: python -m evals.letter_check -> {value 0, cases 25, held_out_entries 11}",
  "archive tree: pytest tests/unit -> 4946 passed, 8 skipped",
  "started app on PORT 7878 from archive tree; GET /api/health; POST /api/cases with pasted text -> demo_mode_unsupported_input",
  "artifacts/review-evidence/t139_adjuster_r4/edit_attack_r4.py: the 7 r3 summary edits on the sample, accept all, trace gate, GET /export default/oneline/standard -> edit_attack_r4.txt/.json (7 x 422; letters clean)",
  "artifacts/review-evidence/t139_adjuster_r4/gate_vs_export.py: money summaries written directly into the scratch DB past the edit check, then trace gate vs GET /export in 3 styles, then restored -> gate_vs_export.txt/.json",
  "artifacts/review-evidence/t139_adjuster_r4/record_text_probe.py: Patient responsibility 1,200.00 / Paid in full 2,150.00 / Lost wages 1,800.00 (+ balance/allowed/write-off/statement) through charge_text.check and narrow_excerpt; same wordings inside the accepted MRI charge sentence through export.money_blockers_for_case, build_export (both styles) and letter_check.violations -> record_text_probe.txt",
  "inline probe: '$2,150 less $737.50 contractual adjustment' and '$2,150 (ins paid $1,412.50)' in the charge sentence -> charge_line_dollar_probe.txt",
  "artifacts/review-evidence/t139_adjuster_r2/heldout_probe.py on the archive tree -> t139_adjuster_r4/heldout_r4.jsonl (11 held)",
  "artifacts/review-evidence/t139_adjuster_probe.py (accept every item, export) on lib01/06/09/10/11/12/14/15 -> t139_adjuster_r4/lib*.json, letters, notes; compared every held entry's served why with the amount items on its record(s)",
  "artifacts/review-evidence/t139_adjuster_r4/new_path_sweep.py: 49 new money wordings through charge_text.check -> new_path_sweep.txt",
  "edit_attack_r4.py with new_edits.json (9 new summary edits on the sample, accept all, gate, export) -> new_edits_result.txt/.json",
  "grep BILLS TO REQUEST in lib10/lib14 notes; grep ': room.' in lib10 letter",
  "kill of the server PID from lsof on 7878; lsof re-check"
 ],
 "verdict": "changes",
 "scores": {"no_invented_facts": 5, "weaknesses_surfaced": 4, "billing_accuracy": 4, "letter_neutrality": 3, "source_cites": 5},
 "findings": [
  {"severity": "major",
   "title": "Amounts in words after a money noun that is not on the closed list (copay, deductible, patient responsibility, paid in full, wages, spent ... out of pocket) pass the edit check, the export gate and the letter eval, and print in the carrier letter",
   "evidence": "artifacts/review-evidence/t139_adjuster_r4/new_edits_result.txt: sample summary edits e1, e2, e3, e5, e7, e8 returned 'EDIT ... 200', 'EXPORT default 200', and the letter treatment text prints: '...transported to Central ER; ambulance copay of twenty.' / '...CT head negative; deductible of five hundred.' / '...for 6 weeks; patient spent fifteen hundred out of pocket.' / '...missing 3 days of work; lost eighteen hundred in wages.' / '...MRI ordered; patient responsibility twelve hundred.' / '...correlate clinically; paid in full twenty-one fifty.'; LETTER_CHECK_VIOLATIONS []. (The digit forms e4 'coinsurance 430.00', e6 'insurer reimbursed 1,412.50', e9 'MRI cost the patient 2,150' were refused, but by the summary-token rule, not the money detector.) new_path_sweep.txt: production MISS for record wording outside 7c: 'Patient spent 1,500 on the MRI.', 'Insurer reimbursed 1,412.50.', 'Copayment 40.00 collected.', 'Coinsurance 430.00.', 'MRI cost the patient 2,150.', 'Net due 737.50.', 'Lost 1,800.00 in wages.', 'Policy limits 30,000.', 'Med-pay 5,000.00 exhausted.', 'MRI 2,150.00 billed to PIP.'. Cause: app/backend/money.py:69 _VERB is a closed verb list (no copay/deductible/responsibility/wages/spent/reimbursed, and 'paid in full' breaks 'paid' + number words); :47 _STRONG needs a digit figure and has 'co-?pay' with a word boundary so 'copayment' misses; :22 closed world lists only slang, bare decimals, per-mile rates and Spanish words. memory/SCOPE_CUTS.md:89 row 7c says 'amounts in words ... are caught'.",
   "why_it_matters": "AC1 says no amount appears in the letter outside the R-EX-8 total line, and the r4 export gate was supposed to be the backstop for exactly this: text a paralegal typed. 'Paid in full twenty-one fifty' and 'patient responsibility twelve hundred' are the paid-or-incurred figures I want (Haygood). If they are in the carrier letter, I set them against the $2,150 billed line and discount the specials. This is the r3 major's class (a money word + number words with no currency noun). r4 closed the 7 listed strings but not the class. I rate it major and not blocker, as in r2/r3: these are words the paralegal typed, EDITED ITEMS records each one, and the corpus has none.",
   "fix": "In money.py, treat number words after ANY money word the detector already knows (_STRONG and _WEAK words plus copay/copayment, coinsurance, deductible, out of pocket, spent, reimbursed, refund, deposit, med-pay/PIP, policy limits, net due) as money, with the same _NOT_COUNT guard; let 'paid in full', 'patient responsibility' and 'wages' take a number-word run. Add 'copayment', 'coinsurance', 'reimbursed', 'cost the patient', 'spent', 'net due' and 'policy limits' with digit figures. If any of these is meant to stay out, name it in row 7c and fix 7c's 'amounts in words are caught' sentence.",
   "acceptance_test": "Replay edit_attack_r4.py with new_edits.json: every edit returns 422 CHARGE_TEXT_IN_ENTRY. Every 'no' MISS row in new_path_sweep.txt becomes a hit. letter_check corpus false positives stay at 0."},
  {"severity": "major",
   "title": "NEW PATH: the export gate skips the whole BILLED CHARGES section, so a paid, adjusted, patient-responsibility or wage figure in a charge's sentence prints in the carrier letter while letter_check flags the same letter",
   "evidence": "app/backend/export.py:735 'head, _ = split_letter(letter_text)': letter_money_blockers scans only the treatment lines, never the charges section. export.py:233 _amount_quote narrows a charge quote only on charge_text.dollar_strings (signed kinds), so an unmarked second figure is never narrowed out, and a '$' second figure stays when no ';'/',' clause is free of it. artifacts/review-evidence/t139_adjuster_r4/record_text_probe.txt: sample record 8 sentence 'Charge: $2,150.' replaced by 'Charge: $2,150; paid in full 2,150.00.' -> gate_blockers [] / export_standard 200 / letter line 'Source [Ex. __ / Bates __]: \"Charge: $2,150; paid in full 2,150.00.\"' / eval 'charges section states money without a $ sign: paid in full 2,150.00'. Same for 'patient responsibility 1,200.00', 'lost wages 1,800.00 claimed', 'allowed 1,412.50, write-off 737.50' (both styles). charge_line_dollar_probe.txt: 'Charge: $2,150 (ins paid $1,412.50).' -> GATE [] and letter line 'Source [Ex. __ / Bates __]: \"Charge: $2,150 (ins paid $1,412.50).\"'; EVAL ['charges section states $1,412.50, not an accepted charge or the total']. 'Charge: $2,150 less $737.50 contractual adjustment.' -> same.",
   "why_it_matters": "A line like 'charge X, paid Y, adjustment Z' is the normal shape of a ledger or statement line. Quoting it under Billed charges gives the carrier the paid number. The orchestrator's r4 rule was that any money outside the total line and the accepted-charge lines blocks the export. A paid figure on a charge's quote line is not an accepted charge. evals/letter_check.py:75 counts it as a violation, but the production gate lets it through, so 'one detector, no divergence' does not hold for the section rule. The eval finds it only on corpus cases, and the corpus has none. I could not run this live: pasted text is refused in demo mode, and the 25 corpus letters are clean. That is why it is major and not blocker.",
   "fix": "In letter_money_blockers, also scan the BILLED CHARGES section: on each quote line, any money expression other than that line's own accepted figure, and anything on the provider/date line other than the figure, is MONEY_IN_LETTER naming the line and the amount item. Better still, make _amount_quote narrow out ANY other money expression (money.hits, not dollar_strings) and fall back to blocking when no clean clause exists. The gate and letter_check must use one section rule.",
   "acceptance_test": "UT on the sample: with record 8 'Charge: $2,150; paid in full 2,150.00.' and the charge accepted, GET /export returns 422 MONEY_IN_LETTER naming the charge's quote line, or the letter quotes 'Charge: $2,150' only. The trace gate gives the same answer. Same for '(ins paid $1,412.50)'. letter_check and the gate agree on all four record_text_probe variants."},
  {"severity": "minor",
   "title": "Carried from r2/r3, not fixed: Bills to request asks for bills the file already has when the bill's provider label differs from the visit's",
   "evidence": "artifacts/review-evidence/t139_adjuster_r4/lib14_internal_notes_text.txt:26 '- Tarnwick Fire-Rescue run report; Hollowbrook Chiropractic.' (Tarnwick invoice charges a2/a4 accepted); lib10_internal_notes_text.txt:31 '- Rainhollow Fire-Rescue run report; Saltmarrow General Hospital ED; Dr. Ignatius Wardlaw.' while the lib10 letter lists the Saltmarrow UB-04 charges.",
   "why_it_matters": "Internal only. But the firm sends records requests for bills it already has.",
   "fix": "Normalize provider names before the comparison: strip record-type tails such as run report, ED, ambulance invoice and UB-04 itemized bill.",
   "acceptance_test": "lib14 all accepted: no 'Tarnwick' under BILLS TO REQUEST. lib10: no 'Saltmarrow'."},
  {"severity": "minor",
   "title": "Carried from r2/r3, not fixed: the lib10 UB-04 bill still sits in the treatment chronology with the stub summary '...: room.'",
   "evidence": "artifacts/review-evidence/t139_adjuster_r4/lib10_letter_text.txt:16 'UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.'",
   "why_it_matters": "A chronology line that reads 'room.' for a hospital bill is unreviewed-looking text I quote back to the firm.",
   "fix": "summary_trim: when a trim would leave a lone word cut out of a clause, drop the whole ':' tail instead.",
   "acceptance_test": "lib10 all accepted: no treatment line ends ': room.'."}
 ],
 "whats_right": [
  "All 7 r3 summary edits now get 422 at edit time, and the message names the expression. The sample letter has none of them and stays clean in all three styles.",
  "gate.ready equals export-allowed in every state I tried (clean, three money summaries stored past the check, restored). MONEY_IN_LETTER names the line, the entry and the expression.",
  "Held-out hints give the true reason on all 9 corpus held entries I checked: not totaled, none read, or already listed. Each matched the amount items on its record."
 ],
 "questions_for_chris": []}
```
