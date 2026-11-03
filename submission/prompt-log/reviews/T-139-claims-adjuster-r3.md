# T-139 — claims-adjuster-reviewer (BI adjuster / defense adversary), round 3

**Verdict: changes** (0 blockers, 1 major, 4 minors).

**Scope.** Card commit `3597d8d`, run from `git archive HEAD` (HEAD `67757f5`). `git diff --stat 3597d8d HEAD` lists only `memory/SCOPE_CUTS.md` and three `tests/e2e` files, so the backend and evals are the same as the card commit.
- App ran on spare port 7877 with `LLM_BACKEND=fixture ZLAYT_MODE=local` and `ZLAYT_DB` in the scratchpad.
- `/api/health` returned `"backend":"fixture","demo_mode":true`.
- I stopped the server by PID (11460). `lsof` on 7877 is now empty.

**Deterministic checks (archive tree):**
- The six `tests/unit/test_t139_*.py` files: **255 passed**.
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, "held_out_entries": 11}`.
- Full `tests/unit`: **4553 passed, 8 skipped**.

**What r3 fixed:**
- **Amounts in words and other currencies (r2 major 1).** Most of my r2 probes are now held by production code:
  - `one hundred eighty-five dollars`, `€`, `£`, `EUR`/`CAD`/`MXN`, `＄`;
  - patient statements ("Patient states the MRI was 2,150", "owes the chiropractor about 2,400");
  - `Total:`, `Amount:`, `Invoice total`, `Saldo`, `pesos`.

  On the sample, my r2 summary edits in words, € and `USD 6` now get 422.
- **Carrier letters.** I ran an independent scan of every carrier letter: 25 cases, all accepted and charges-dismissed, both styles. No money-shaped figure appears in any treatment text (`letter_scan_filtered.txt`).
- **Item trace.** It now shows `excerpt_narrowed` and `charge_clause_removed`, each with the removed text verbatim, a why, and quote/summary before and after. Checked on sample e2/e4, lib01 e2/e4, lib10 e4/e6 and lib14 e2.

**Still open:**
- **Amounts outside scope cut 7c still reach the carrier letter.** Seven accepted summary edits on the sample all printed in the letter, for example `MRI billed at two thousand one hundred fifty.` and `injection quoted at fifteen hundred.`. letter_check flagged only one of the seven.
- **Record wording production code still misses:** `Patient responsibility 1,200.00`, `Paid in full 2,150.00`, `Reimbursement 2,150.00`, `Lost wages 1,800.00`, `the 3,915 ER bill`, `Dollars: 185.00`.

  Scope cut 7c covers slang (`6.5k`, `one eighty-five each`), bare decimals with no money word, and per-mile rates. These strings carry a money word or a currency noun, so they are outside 7c. **Major.**
- **The held-out hint gives a wrong reason.** It tells her "No charge was read from this record" on 6 of 11 held entries. Each of those records had its amounts read, and the internal notes list them as "Not totaled". It also tells her to "request the bill" for a figure she typed into a visit note herself. **Minor.**

```json
{"card": "T-139", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 3597d8d via git archive HEAD (67757f5; git diff --stat 3597d8d HEAD touches only memory/SCOPE_CUTS.md and tests/e2e) in session scratchpad t139r3/; app http://127.0.0.1:7877 (LLM_BACKEND=fixture, ZLAYT_MODE=local, scratch ZLAYT_DB); sample, lib01 (all accepted and $3,915 dismissed), lib06, lib09, lib10, lib11, lib12, lib14, lib15; letter scan over all 25 eval cases",
 "exercised": [
  "read personas/claims-adjuster.md, reviews/T-139-claims-adjuster-r2.md, card notes for reviews/T-139-staff-engineer.md, memory/SCOPE_CUTS.md row 7c, my memory dir",
  "python3 tools/board.py show T-139 (status in_review, commits [..., 4abec86, 3597d8d])",
  "git diff --stat 3597d8d HEAD -> memory/SCOPE_CUTS.md, tests/e2e/test_polish_r3.py, test_rerun_judge.py, test_stepper.py only; git archive HEAD into scratchpad t139r3",
  "archive tree: pytest tests/unit/test_t139_r3.py test_t139_trace.py test_t139_unmarked.py test_t139_narrow.py test_t139_charge_text.py test_t139_letter_eval.py -> 255 passed",
  "archive tree: python -m evals.letter_check -> {value 0, cases 25, held_out_entries 11}",
  "archive tree: pytest tests/unit -> 4553 passed, 8 skipped",
  "artifacts/review-evidence/t139_adjuster_r3/attack_sweep_r3.py: the 67 r2 attack strings plus 66 new ones through charge_text.check, narrow_excerpt and the FULL evals.letter_check.violations -> attack_sweep_r3.txt; the r2 script re-run as-is -> attack_sweep_r3.txt's sibling attack_sweep_r3.txt (first run)",
  "started app on PORT 7877 from archive tree; GET /api/health",
  "artifacts/review-evidence/t139_adjuster_probe.py (accept every item one by one, export default/oneline/standard) on sample and lib01/06/09/10/11/12/14/15, and lib01 with the $3,915 charge dismissed -> t139_adjuster_r3/*.json, *_letter_*.txt, *_internal_notes_text.txt",
  "read every 422 CHARGE_TEXT_IN_ENTRY message and every held entry's served why (view_after) against the amounts read from the same record",
  "artifacts/review-evidence/t139_adjuster_r2/heldout_probe.py re-run on the archive tree -> t139_adjuster_r3/heldout_r3.jsonl (11 held)",
  "GET /items/{id}/trace for every entry of sample, lib01, lib10, lib14 -> trace_narrow_steps.txt; lib10 e4 full trace and ladder -> lib10_e4_trace.json",
  "artifacts/review-evidence/t139_adjuster_r2/edit_attack.py replayed on the sample -> edit_attack_replay.json (e4 words, e5 euro, e3 USD all 422)",
  "artifacts/review-evidence/t139_adjuster_r3/edit_attack_r3.py: 7 summary edits with money forms outside 7c, accept all, export, letter_check.violations on the letter -> edit_attack_r3.json",
  "artifacts/review-evidence/t139_adjuster_r3/letter_scan.py: all 25 eval cases (all accepted and charges dismissed, both styles), every treatment-text line with a figure or money word -> letter_scan.txt, filtered to letter_scan_filtered.txt (37 lines, no money)",
  "grep of BILLS TO REQUEST in lib01, lib10, lib11, lib14 notes; grep of lib01_dismissed letter for '$' (0)",
  "kill 11460; lsof -nP -t -iTCP:7877 -sTCP:LISTEN -> empty"
 ],
 "verdict": "changes",
 "scores": {"no_invented_facts": 5, "weaknesses_surfaced": 4, "billing_accuracy": 4, "letter_neutrality": 3, "source_cites": 5},
 "findings": [
  {"severity": "major",
   "title": "Money forms outside scope cut 7c still pass the hold and reach the carrier letter; the letter eval catches 1 of 7",
   "evidence": "artifacts/review-evidence/t139_adjuster_r3/edit_attack_r3.json: on the sample, all 7 summary edits returned 200 and, after accept, the carrier letter treatment text prints: 'C5-C6 disc protrusion with mild right foraminal narrowing; findings may represent degenerative change, correlate clinically; MRI billed at two thousand one hundred fifty.' / 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision; injection quoted at fifteen hundred.' / 'Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks; patient responsibility 6 per visit.' / 'Plan of care: 12 visits at 40 a visit.' / 'reimbursement 7 owed to patient.' / 'lost wages 3.' / 'paid in full 3.'. LETTER_CHECK_VIOLATIONS ['treatment text states money without a $ sign: paid in full 3'] (1 of 7). attack_sweep_r3.txt, production check() returns [] (MISS) for record wording that carries a money word or currency noun: 'Patient responsibility 1,200.00.', 'Patient responsibility: 1,200.00.', 'Paid in full 2,150.00.', 'Reimbursement 2,150.00.', 'Lost wages 1,800.00.', 'Wage loss 1,800.', 'Usual and customary 185.00.', 'Mileage reimbursement 87.00.', 'Patient is worried about the 3,915 ER bill.', 'The ambulance bill came to 1,380.', 'Dollars: 185.00.', 'PT at 185 a visit.', 'PT at 185 each visit.', 'Charge per visit ﹩185.' (small dollar sign U+FE69; the eval does catch this one). Cause: app/backend/charge_text.py:26 _SPOKEN needs a currency noun after the number words; :37-39 _WEAK has no responsibility/reimbursement/wage and 'paid' must be followed directly by the figure; :52 _PER_VISIT needs 2+ digits and 'per'. memory/SCOPE_CUTS.md row 7c accepts only '6.5k', 'one eighty-five each', bare decimals with no money word, and per-mile rates, and says 'amounts in words ... are caught'.",
   "why_it_matters": "AC1 says no dollar amount appears in the letter except the R-EX-8 total line. 'MRI billed at two thousand one hundred fifty' in a carrier letter gives me a second MRI figure to set against the $2,150 charge line, and it is not slang. 'Patient responsibility', 'paid in full' and 'reimbursement' are EOB and statement fields. If a record line with one of them is quoted, it tells me what was paid, which is the paid-or-incurred number I want (Haygood). letter_check was meant to be the independent guard, but it missed 6 of the 7 letter lines. Major, not blocker, for the same reason as r2: in demo/fixture mode the only end-to-end path I could run is text the paralegal typed. EDITED ITEMS records each of those edits, and the corpus has none of the record forms.",
   "fix": "Production and eval, each in its own code: (1) number words after a money verb or noun with no currency noun ('billed at|quoted at|charged|cost|paid|owes? + number words'); (2) add patient responsibility, reimbursement, paid in full, usual and customary, wages/wage loss, and 'N a|each visit' with any digit count; (3) a figure directly before bill/invoice/charge ('the 3,915 ER bill'); (4) 'Dollars:' + figure; (5) U+FE69 in production. If any of these is meant to be out of scope, add it to row 7c by name.",
   "acceptance_test": "Replay edit_attack_r3.py: every edit returns 422 CHARGE_TEXT_IN_ENTRY. Every non-7c MISS row in attack_sweep_r3.txt is a hit in both charge_text.check and letter_check.violations. letter_check.violations on the edit_attack_r3 letter lists all 7 lines. Corpus false positives stay at 0."},
  {"severity": "minor",
   "title": "The held-out hint says 'No charge was read from this record' when the record's amounts were read, and for a figure she typed it points her to the notes and a bill request",
   "evidence": "Served why (view_after) and 422 message for lib06 e4, lib09 e7, lib11 e9, lib12 e10, lib15 e7 and lib15 e9: '... No charge was read from this record, so its figures are not counted in the Billed charges section; the internal notes name them so you can request the bill.' The same records have accepted amounts read from them, e.g. lib11 r9 a2-a8 ('unclear', $250.00 ... $2,166.00), which lib11_internal_notes_text.txt:24-30 lists as 'Not totaled ($250.00): The line states no date of service ...'. edit_attack_replay.json, sample e5 (Capital PT visit 8; no figures on the record) summary edit 'PT €4 per visit' -> 422 '... No charge was read from this record, so its figures are not counted ...; the internal notes name them so you can request the bill.' The notes name no €4.",
   "why_it_matters": "The r2 problem (claiming charges were listed when they were not) is gone, and the conclusion is now right: these figures are not counted. But the stated reason is not. The ledger she is reading says 'New patient exam charge $250.00', and the tool tells her no charge was read. For a typed amount on a visit note, 'request the bill' is the wrong action. A hint that misdescribes what the tool did teaches her to stop trusting the tray.",
   "fix": "Add a fourth bill_state: amounts read but none totaled. Say 'Its amounts were read but not totaled (see the internal notes for why).' When the figure appears only in a human-edited summary and not on the record, omit the bill sentence.",
   "acceptance_test": "UT: the why for lib11 e9 does not contain 'No charge was read' and names 'not totaled'. A 422 for a summary edit on sample e5 has no bill sentence."},
  {"severity": "minor",
   "title": "The letter eval is narrower than the production detector, so it cannot catch a regression on these forms",
   "evidence": "attack_sweep_r3.txt rows 'hit EVAL-MISS' (production holds the string, letter_check.violations returns []): 'Total charge\\n49100.', 'Charge per\\nvisit 185.', 'Charge:\\n1,200.00', 'Allowed 4,413.50.', 'LOP balance 1,550.', 'Balance 1,550.', 'Write-off 1,250.00.', 'PT 185/session.'. evals/letter_check.py:32 _MONEY_WORD needs 'balance due|owed|forward' and has no 'allowed'/'write-off'; _UNMARKED excludes line breaks ([^\\n.;$]).",
   "why_it_matters": "These do not reach the letter today, because production holds them. But AC3's eval is the backstop if production ever stops holding them. EOB fields (allowed, write-off, balance) are exactly what I would use from a leaked line.",
   "fix": "Widen letter_check's own detector to cover the forms production already holds: allowed, write-off, a bare balance, N/session, and a money word and figure split across a line break.",
   "acceptance_test": "Each 'hit EVAL-MISS' row in attack_sweep_r3.txt becomes 'hit eval-hit'."},
  {"severity": "minor",
   "title": "Carried from r2, not fixed: Bills to request still asks for bills the file already has when the provider name on the bill differs from the one on the visit",
   "evidence": "t139_adjuster_r3/lib14_internal_notes_text.txt BILLS TO REQUEST: '- Tarnwick Fire-Rescue run report; Hollowbrook Chiropractic.' The lib14 Tarnwick invoice charges ($1,380.00, $187.05) were accepted (view_after a2/a4 'charge' 'accepted'). lib10: '- Rainhollow Fire-Rescue run report; Saltmarrow General Hospital ED; Dr. Ignatius Wardlaw.', while the letter lists four Saltmarrow UB-04 charges. The handoff lists this as not done.",
   "why_it_matters": "This list is internal only. But the firm sends records requests for bills it already holds.",
   "fix": "Normalize the provider name before the paid/dismissed comparison: strip run report, ED, ambulance invoice, UB-04 itemized bill and similar record-type tails.",
   "acceptance_test": "lib14 all accepted: BILLS TO REQUEST has no 'Tarnwick'. lib10: no 'Saltmarrow'."},
  {"severity": "minor",
   "title": "Carried from r2, not fixed: the lib10 UB-04 bill still sits in the treatment chronology with the stub summary '...: room.'; the trace now shows how it happened",
   "evidence": "t139_adjuster_r3/lib10_letter_text.txt:15-17: 'June 19, 2026 — Saltmarrow General Hospital, UB-04 itemized bill' / 'UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.' lib10_e4_trace.json: summary_trimmed 'removed from the summary: not in the quote: 'board semi-private 3 days at $1,640.00 per day totaling $4,920.00'', and judge_1 fail JUDGE_UNSUPPORTED. Accepting it puts it in the letter.",
   "why_it_matters": "A chronology line reading 'room.' for a hospital bill is the kind of unreviewed text I quote back to show the package was not checked.",
   "fix": "summary_trim: refuse a trim that leaves a lone word cut out of a clause (drop the whole ':' tail instead).",
   "acceptance_test": "lib10 all accepted: no treatment line ends ': room.'."}
 ],
 "whats_right": [
  "No money-shaped figure appears in the treatment text of any of the 25 eval letters (all accepted and charges dismissed, both styles). The sample total line is still exactly 'Billed charges stated in these records: $8,390.00', and dismissing lib01's $3,915 leaves no '$' in the letter.",
  "The item trace shows narrowing and trimming as code steps: the verbatim removed sentence, the why, and quote and summary before and after (sample e2/e4, lib01 e2/e4, lib10 e4/e6, lib14 e2).",
  "Amounts in words with a currency noun, €/£/EUR/CAD/MXN/＄ and patient-statement figures are now held. The r2 sample edits in words, € and USD now return 422."
 ],
 "questions_for_chris": []}
```
