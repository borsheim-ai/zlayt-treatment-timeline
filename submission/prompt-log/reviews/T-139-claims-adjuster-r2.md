# T-139 — claims-adjuster-reviewer (BI adjuster / defense adversary), round 2

**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit).

Scope: card commit `4abec86`, run from `git archive HEAD` (HEAD `25f585c`). `git diff --stat 4abec86 HEAD -- app/backend app/llm evals` printed nothing, so app/backend, app/llm and evals are the same at both commits.
The app ran from that tree on spare port 7875 with `LLM_BACKEND=fixture ZLAYT_MODE=local` and a scratch `ZLAYT_DB`. `/api/health` returned `"backend":"fixture","demo_mode":true`. I stopped the server (PID 21047) when I finished.

Deterministic checks came first, all on the archive tree:
- The four `tests/unit/test_t139_*.py` files: **138 passed**.
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, "held_out_entries": 11}`.
- Full `tests/unit`: 4156 passed, 1 failed, 1 error. Both problems are T-140/D-059 tests that read `artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt`, which is not in the commit. They have nothing to do with T-139.

**My round-1 attacks:**
- **Money without '$' on lib10 and lib14 (closed).** With every item accepted, neither letter contains `TOTAL CHARGE`, `AMOUNT PAID`, `24F`, `49100` or `33000`. The claim-form entries (lib10 e8, lib14 e7) now get `422 CHARGE_TEXT_IN_ENTRY` and stay out of the letter.
- **lib11 "Bills to request" (closed).** It now reads `- Dr. Hesper Alderton; Ashgrove Fire-Rescue run report.` The PLLC is gone.
- **Held-out hint actions (closed as I raised them, but a new problem).** Each action the hint offers does clear the hold:
  - dismissing lib10 e8 and lib14 e7 returns 200 `dismissed`;
  - a quote+summary edit on lib14 e8 returns 200.
  - The internal notes now tell a bill apart from a claim form.

  The new problem: the tray `why` text and the 422 message tell her "a bill's charges are under Billed charges" for all 11 held entries. For 5 of them that is false. **Major 2.**

**New ways in.** I swept 67 strings through both detectors: the production `charge_text.check` and the eval's own `letter_check` detector.
- Detected: `USD 1,200`, `1,200 USD`, `US$1,200`, `185 dollars`, and figures split across a line break. Split figures are held, not narrowed.
- Missed by **both** detectors:
  - amounts written in words ("one hundred eighty-five dollars");
  - `€185`, `EUR 185`, `£1,200`, `CAD`/`MXN`, and the full-width `＄185` (the production detector misses it);
  - a figure inside a patient's statement ("Patient states the MRI was 2,150", "owes the chiropractor about 2,400", "the ER bill was 3,915");
  - `Total: 1,200.00`, `Amount: 1,200.00`, `Invoice total 1,567.05`, `Network discount 3,610.00`;
  - Spanish `Saldo` / `Costo` / `pesos`.
- I showed one end to end on the sample case. After a summary edit and her accept, the carrier letter prints `Plan of care: 12 visits at one hundred eighty-five dollars per visit.` and `PT €4 per visit.`. `letter_check.violations` on that letter returns `[]`. **Major 1.**
- A figure in a quoted patient statement could not be run end to end. Demo mode refuses pasted text (`409 demo_mode_unsupported_input`), and no corpus record has one.

**Held-out entries (11).** All 11 can be cleared by dismissing them. Records that have a clean sentence can also be cleared with a quote+summary edit. The notes explain each one correctly. The tray and the 422 do not (Major 2).

```json
{"card": "T-139", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 4abec86 via git archive HEAD (25f585c; git diff --stat 4abec86 HEAD -- app/backend app/llm evals is empty) in session scratchpad t139r2/; app http://127.0.0.1:7875 (LLM_BACKEND=fixture, ZLAYT_MODE=local, scratch ZLAYT_DB); sample, case_lib01 (charge dismissed), lib06, lib09, lib10, lib11, lib12, lib14, lib15; held-out census over all 25 eval cases",
 "exercised": [
  "python3 tools/board.py show T-139; read reviews/T-139-claims-adjuster.md, personas/claims-adjuster.md, my memory dir",
  "git diff --stat 4abec86 HEAD -- app/backend app/llm evals (empty); git archive HEAD into scratchpad t139r2",
  "archive tree: pytest tests/unit/test_t139_unmarked.py test_t139_narrow.py test_t139_charge_text.py test_t139_letter_eval.py -> 138 passed",
  "archive tree: python -m evals.letter_check -> {value 0, cases 25, held_out_entries 11}",
  "archive tree: pytest tests/unit --continue-on-collection-errors -> 4156 passed, 1 failed, 1 error (both T-140/D-059 tests reading uncommitted artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt)",
  "started app on PORT 7875 from archive tree; GET /api/health (backend fixture, demo_mode true)",
  "artifacts/review-evidence/t139_adjuster_probe.py (accept every item, export default/oneline/standard) on sample, lib10, lib14, lib11, lib06, lib09, lib12, lib15, and lib01 with the $3,915 charge dismissed -> artifacts/review-evidence/t139_adjuster_r2/*.json, *_letter_*.txt, *_internal_notes_text.txt",
  "grep of every letter for '$', TOTAL CHARGE, AMOUNT PAID, 24F, FL47, 49100, 33000, per visit, estimat, cost, fee, paid, owe, balance, USD, dollar, 3+ digit figures outside BILLED CHARGES / Source / total lines",
  "read BILLS TO REQUEST, RECORDS NOT IN THE TREATMENT SECTION and PENDING ITEMS NOT INCLUDED in each internal_notes_text",
  "artifacts/review-evidence/t139_adjuster_r2/heldout_probe.py: all 25 eval cases in-process, every CHARGE_TEXT_IN_ENTRY entry with its why, currency strings and the charge amounts on its record -> heldout.jsonl (11 entries)",
  "fix paths: POST /items/e8/review dismiss on lib10 (200 dismissed), dismiss lib14 e7 (200), quote+summary edit lib14 e8 to 'Invoice for the run of 09/14/2026.' (200 edited, JUDGE_UNAVAILABLE); re-exported both and read the notes",
  "artifacts/review-evidence/t139_adjuster_r2/attack_sweep.py: 67 attack strings (words, euro/pound/ISO codes, full-width $, line breaks, patient statements, totals, Spanish) through charge_text.check, narrow_excerpt and evals.letter_check detectors -> attack_sweep.txt",
  "artifacts/review-evidence/t139_adjuster_currency_sweep.py re-run on archive tree (20 variants + corpus) -> t139_adjuster_r2/currency_sweep_r2.txt (corpus: no money sentence missed)",
  "artifacts/review-evidence/t139_adjuster_r2/edit_attack.py on sample: summary edits with amounts in words / euro / 'USD 6' / 'balance 3 owed', then accept and export -> edit_attack.json, edit_attack_export2.json; letter_check.violations on that letter -> []",
  "POST /api/cases with pasted sample text containing a patient-statement amount -> 409 demo_mode_unsupported_input",
  "stopped server PID 21047 with kill; lsof on 7875 empty"
 ],
 "verdict": "changes",
 "scores": {"no_invented_facts": 4, "weaknesses_surfaced": 4, "billing_accuracy": 3, "letter_neutrality": 3, "source_cites": 5},
 "findings": [
  {"severity": "major",
   "title": "The amount check and the 'independent' letter eval both miss amounts written in words, other currency signs and figures in a patient's statement; a per-visit rate in words reaches the carrier letter",
   "evidence": "artifacts/review-evidence/t139_adjuster_r2/edit_attack_export2.json letter_text: 'Cervical range of motion reduced approx. 40%. Plan of care: 12 visits at one hundred eighty-five dollars per visit.' / 'Pain 4/10, improving; patient reports missing 3 days of work; PT €4 per visit.' / 'Discharged from PT after two missed appointments; balance 3 owed.' (each a summary edit, accepted; the same edit with 'USD 6' was refused 422 'The summary states a dollar amount (USD 6)'). evals.letter_check.violations(letter, [624000, 215000]) -> []; charge_text.currency_strings on each line -> []. attack_sweep.txt: 'MISS EVAL-MISS' for 'Charge per visit: one hundred eighty-five dollars.', 'Visit rate EUR 185.', 'Visit rate £1,200.', 'Visit rate CAD 1,200.', 'Visit rate 1.200,00 €.', 'Patient states \"the ER bill was 3,915 and I cannot pay it.\"', 'Patient reports she owes the chiropractor about 2,400.', 'Patient states the MRI was 2,150.', 'Total: 1,200.00.', 'Amount: 1,200.00.', 'Invoice total 1,567.05.', 'Network discount 3,610.00.', '185 per visit.', 'Saldo: 2,900.00.', 'Consulta 400 pesos.'; 'MISS' (production) for 'Charge per visit €185.' and 'Visit rate ＄185.'. app/backend/charge_text.py:20 (_WORDS: digits + dollars|USD only) and :26-29 (_STRONG/_WEAK money words); evals/letter_check.py:28-33.",
   "why_it_matters": "AC1 says no dollar amount appears anywhere in the letter except the R-EX-8 total line. A carrier letter that states '185 dollars per visit' gives me a rate and invites me to multiply it, which is the GATE-M2 defect again in a different spelling. The guard refuses '$185' and 'USD 6' but accepts the same rate written in words or with '€'. In a live case, a record line like 'Patient states the MRI was 2,150' would be quoted verbatim, and nothing would stop it. The eval was meant to be independent, but it shares the same blind spots, so it cannot catch any of this. Why this is major and not blocker: in demo mode the only path I could run end to end is text the paralegal typed herself, and EDITED ITEMS records it ('summary was ... now ...'). The tool did not invent it.",
   "fix": "Widen charge_text and letter_check, each in its own code. Cover: any currency sign [$€£¥＄] or ISO code (USD|EUR|GBP|CAD|MXN) next to a figure; number words followed by dollars|bucks|pesos|euros; 'bill|invoice|total|amount|discount|adjustment|lien|out-of-pocket|self-pay|saldo|costo' with a money-shaped figure; a money verb with a figure after it (bill was|owes?|cost|spent|paid|charged me|run about) inside 'Patient states/reports' clauses; and a bare 'N per visit|session'. Run the same check on a paralegal summary edit.",
   "acceptance_test": "Every 'MISS' row in artifacts/review-evidence/t139_adjuster_r2/attack_sweep.txt is a hit in both charge_text.check and letter_check (unit test with the same strings). Replaying edit_attack.py on the sample gives 422 CHARGE_TEXT_IN_ENTRY for the e4/e5/e6 edits. letter_check.violations flags the edit_attack_export2 letter. The corpus sweep still finds 0 false positives."},
  {"severity": "major",
   "title": "The held-out hint tells her 'a bill's charges are under Billed charges' for all 11 entries; for 5 of them no charge from that record is in Billed charges",
   "evidence": "app/backend/why.py:10 (fixed text): 'Dismiss it (a bill's charges are under Billed charges), or pick a quote without the amount and edit the summary to match.' The 422 message from charge_text.message says '...If the record is a bill, its charges are already listed under Billed charges.' heldout.jsonl: case_03 e2 '$1,2OO' (amount kind unclear, charge_amounts_same_record []), lib09 e7 (charges [] ; '$1,300.00' unclear, '$400.00' rate), lib10 e8 CMS-1500 'TOTAL CHARGE 49100' (charges []), lib14 e7 CMS-1500 'TOTAL CHARGE 33000' (charges []), lib15 e9 18.001 affidavit (charges []). I followed the hint on lib10 e8 (dismiss, 200). The notes then read only 'Record 8 (Wardlaw Orthopedics, CMS-1500 ...) — dismissed'. lib10 BILLED CHARGES total is 'Billed charges stated in these records: $8,123.50', with no Wardlaw line. The export notes (export.py _held_amount_note) already tell these cases apart: lib10 notes say 'dismiss this entry, or pick a quote that does not state it ...' and lib11 notes say 'this record is a bill and its charges are already listed under Billed charges'.",
   "why_it_matters": "The tray is what she reads while reviewing, and for these 5 entries it states something false about her own work product. On the claim forms it pushes her to dismiss because 'the charges are listed', when Wardlaw's $491 and Hollowbrook's $330 appear in no amount line at all. The brief asked whether the held-out entries are explained. For 5 of 11, the place she acts from explains them wrongly.",
   "fix": "Build the item's why and the 422 message from the same per-record rule as _held_amount_note. Say that the charges are listed only when an accepted or pending charge amount on that record exists. Otherwise say that the record's figures are not in Billed charges, and name them in the internal notes so she can add them by hand or request the bill.",
   "acceptance_test": "UT over the 11 held entries: the why and the 422 message contain 'under Billed charges' only for lib06 e4, lib11 e9, lib12 e10, lib14 e8, lib15 e7 and case_09 e2 (records with a charge amount). For lib10 e8, lib14 e7, lib15 e9, lib09 e7 and case_03 e2 they say the figures are not counted."},
  {"severity": "minor",
   "title": "Bills to request still asks for bills the file already has when the provider name on the bill differs from the one on the visit",
   "evidence": "lib14_internal_notes_text.txt BILLS TO REQUEST: '- Tarnwick Fire-Rescue run report; Hollowbrook Chiropractic.' The same letter's BILLED CHARGES lists 'Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026: $1,380.00' and '$187.05'. lib10_internal_notes_text.txt: '- Rainhollow Fire-Rescue run report; Saltmarrow General Hospital ED; Dr. Ignatius Wardlaw.' The letter accepts 'Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00' from the Saltmarrow General Hospital UB-04. export._bills compares _provider(source) strings ('Tarnwick Fire-Rescue run report' vs 'Tarnwick Fire-Rescue').",
   "why_it_matters": "It is internal only, so it never reaches me. But the firm sends records requests for bills it already holds, and the request list looks unchecked. The card's scope covers this list.",
   "fix": "Match providers on a normalized facility name: strip record-type suffixes such as run report, ED, ambulance invoice, UB-04 itemized bill and discharge summary before the paid/dismissed comparison.",
   "acceptance_test": "lib14 all accepted: BILLS TO REQUEST does not contain 'Tarnwick'. lib10: does not contain 'Saltmarrow'."},
  {"severity": "minor",
   "title": "Narrowing and summary trimming can leave a stub in the letter ('...: room.') or a quote that ends on a fragment ('... 12 visits. TOTAL')",
   "evidence": "lib10_letter_text.txt:15-17: 'June 19, 2026 — Saltmarrow General Hospital, UB-04 itemized bill' / 'UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.' / 'Source ...: \"UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026.\"'. The ladder's summary_trim removed 'board semi-private 3 days at $1,640.00 per day ...' and kept 'room'. Judge 1 returned 'unsupported', so it is needs_review, and accepting it prints it. The same line was in the r0 overlay letter. attack_sweep.txt: narrow_excerpt('Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. TOTAL\\nCHARGE 49100.') keeps '... Plan of care: 12 visits. TOTAL'; with 'Cost\\nestimate 6,500.' it keeps '... 12 visits. Cost'. sentences.py treats a line break as a terminator, so the whole-sentence check passes.",
   "why_it_matters": "A chronology line that reads 'room.' or a quote that ends on 'Cost' is the kind of sloppiness I point to when I say the package was not reviewed. A bill also should not sit in the treatment chronology at all.",
   "fix": "trim_summary: refuse the trim when the kept prefix ends in a single word cut off from its clause (an ' and ' split inside a noun phrase), or drop the whole ':' tail. narrow_excerpt: keep an edge unit only if it ends in . ? ! or ; and not at a bare line break.",
   "acceptance_test": "lib10 all accepted: no treatment line ends ': room.'. UT: narrow_excerpt on the two line-break strings returns None (held) or a quote that ends in a terminator."},
  {"severity": "nit",
   "title": "CHARGE_TEXT_IN_ENTRY 422 detail still lists every amount twice, and lists days/units as amounts",
   "evidence": "lib11 e9 detail.amounts ['$250.00', '$180.00', '$2,310.00', '$2,740.00', '$250.00', '$180.00', '$2,310.00', '$2,740.00']. lib14 e7 message 'The quote states a dollar amount (24F 25500, 24G 3, 24F 7500, 24G 3, TOTAL CHARGE 33000)'. 24G is days or units.",
   "why_it_matters": "This is the round-0 nit, still open. Cosmetic.",
   "fix": "De-duplicate excerpt+summary amounts. Cut the 24F match at the next field label.",
   "acceptance_test": "UT: detail.amounts has no repeats; no item contains '24G'."}
 ],
 "whats_right": [
  "lib10 and lib14 letters with every item accepted no longer contain TOTAL CHARGE, AMOUNT PAID, 24F, 49100 or 33000; letter_check returns 0 over 25 cases and 138 T-139 tests pass from a clean archive.",
  "lib11 Bills to request no longer lists Pellingham and Rook PLLC; dismissing lib01's $3,915 leaves no '$' in the letter and drops the ED from Bills to request.",
  "Every remedy offered for a held-out entry now works (dismiss 200 on lib10 e8 and lib14 e7; quote+summary edit 200 on lib14 e8), and a figure split across a line break is held, not narrowed."
 ],
 "questions_for_chris": []}
```
