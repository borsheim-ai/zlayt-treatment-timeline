# T-171 round 3 close-out: claims-adjuster-reviewer (Gary Pruitt), commit fc1c833

Verdict: **changes** (0 blockers, 1 major, 1 minor). Scoped to the three round-3 checks; scope cut 7g (fee lines, other payer or summary wordings beyond the list) is treated as accepted debt and not rated.

The three checks:
1. **Closed.** My r2 payer, allowed, lifetime, account and summary lines are all `NOT_COUNTABLE` over HTTP: BCBSTX, Oscar, Workers comp, USAA, Molina, Repriced, Approved, Negotiated, Usual and customary, Fee schedule, Eligible, since first visit, so far, through today, whole episode, entire course, all therapy, visits 1 to 6, lien, collections, deferred, on hold, billed to attorney, Gross, Billed amount for, last statement. Each leaves the letter at the $830.00 truth. Of the 62 r1 and 44 r2 scenarios (106) on Path A, the only OVER results are the 3 accepted fee lines and the dated no-show baseline, which predates T-171.
2. **Closed for the listed pairs.** PT vs physical therapy, New pt vs New patient, xray vs x-ray, radiograph vs x-ray, a CPT code vs its description, a `(restated)` line, a reprint with abbreviations, and three copies all return `CONFIRM_REQUIRED likely_duplicate` with only `separate_charge`.
3. **Closed.** lib11 letter line is `Billed charges accepted from these records: $6,000.00`. All 15 library cases are at or below the hand total, and the 15 letter lines are identical to my r2 run.

What is open (outside 7g):
- **Major.** The duplicate match is still an alias list. In a held-out set of 14 reworded undated repeats I wrote after reading the r3 diff's wordings, 4 are still countable with only `separate_charge`, and each doubles the letter total: ED visit vs emergency department visit, Initial evaluation vs New patient exam, CAT scan vs CT scan, Consult visit vs specialist consultation. 10 of 14 hold.
- **Minor.** A quote or proposal worded as a charge ("Proposed therapy visit charge $600.00", "Quoted charge for therapy visit $600.00") is countable. It is not a payer, summary or fee line. The sibling word "Estimated" is already refused.

Out of my lens, not rated: a dated charge line carrying a CPT code blocks the export (letter gate reads `97140 charge`); still seen on dup_code_vs_desc, dup_office_visit_eandm and h_xray_cpt.

Not rated, inside 7g: "Exam and x-ray charge $430.00." beside the two lines counts $430 (summary wording), and "Therapy package charge $1,100.00 for 6 visits." counts (summary wording).

Evidence: artifacts/review-evidence/T-171-adjuster-r3/ (probe_http_paste_r3.py, paste_http_r3.txt, paste_http_r3_held.txt, library_http_r3.json, logs). The server was a `git archive HEAD` (bbb40ba; `git diff --stat fc1c833 HEAD -- app memory/contracts` is empty) copy; the two servers (PIDs 79407 and 79409) were killed by PID and `lsof` shows 0 listeners on 7881 and 7882.

```json
{"card": "T-171", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 3 close-out, commit fc1c833 (HEAD bbb40ba has no app/ or api.md diff); git archive HEAD copy in the session scratchpad; HTTP only: fixture server http://127.0.0.1:7881 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB) for the 15 library cases, scripted-call server http://127.0.0.1:7882 (serve_scripted.py, ZLAYT_MODE=local, scratch ZLAYT_DB) for pasted SYNTHETIC ledgers because demo mode refuses unrecorded text; scope cut 7g treated as accepted debt",
 "exercised": [
  "read personas/claims-adjuster.md, reviews/T-171-claims-adjuster-r2.md, my memory project_t171_t172_count_action.md, python3 tools/board.py show T-171 (round-3 note and handoff), memory/SCOPE_CUTS.md row 7g, memory/ORCHESTRATOR_DECISIONS.md D-064",
  "git archive HEAD to the scratchpad; git diff --stat fc1c833 HEAD -- app memory/contracts returned nothing",
  "artifacts/review-evidence/T-171-adjuster-r2/probe_http_r2.py unchanged against :7881, all 15 library cases, Path A (count with separate_charge only), accept, export; output artifacts/review-evidence/T-171-adjuster-r3/library_http_r3.json; compared with library_http_r2.json: identical letter totals, lib11 $6,000.00",
  "probe_http_paste_r3.py (probe_r2.py scenarios, client switched to urllib over HTTP) against :7882, sets orig, nonmatch, new, Path A and Path B, 212 lines in paste_http_r3.txt; Path A tags 97 ok, 5 UNDER, 4 OVER (fee_no_show, fee_cancel, fee_interest_care, fee_no_show_dated, all accepted debt or predating T-171)",
  "held-out set of 24 new scenarios (14 reworded dated-then-undated repeats, 10 estimate, package, subtotal, discount, unit wordings) Path A and B, output paste_http_r3_held.txt",
  "both servers killed by PID (79407, 79409); lsof listener count 0 on 7881 and 7882"
 ],
 "verdict": "changes",
 "scores": {"r2_payer_insurer_lines_not_countable": 5, "r2_reworded_repeats_need_duplicate_confirm": 4, "library_no_overcount_and_lib11": 5, "unseen_reworded_repeat_detection": 3},
 "findings": [
  {"severity": "major",
   "title": "The duplicate match is still an alias list: ED vs emergency department, Initial evaluation vs New patient exam, CAT vs CT, Consult vs consultation are not matched and count with only separate_charge",
   "evidence": "paste_http_r3_held.txt, Path A, record 1 'Billing statement. 04/16/2026 <dated line>' (a detected charge) and record 2 with no source and an undated restatement; the undated amount is countable True with count_confirm None and counts with only {action: count, confirm: separate_charge}. 'emergency department visit charge $2,100.00' + 'ED visit charge $2,100.00.' -> 'Billed charges accepted from these records: $4,200.00' (truth $2,100.00). 'new patient exam charge $250.00' + 'Initial evaluation charge $250.00.' -> $500.00 (truth $250.00). 'CT scan head charge $900.00' + 'CAT scan of the head charge $900.00.' -> $1,800.00 (truth $900.00). 'specialist consultation charge $300.00' + 'Consult visit charge $300.00.' -> $600.00 (truth $300.00). The other 10 held-out pairs hold: office visit/OV is refused as not countable; MRI vs magnetic resonance imaging, chiropractic manipulation vs CMT 98940, $150 vs $150.00, therapy visit vs therapy visits, ultrasound therapy vs US therapy, and 72040 vs X-ray cervical spine all return CONFIRM_REQUIRED likely_duplicate.",
   "why_it_matters": "This is the r2 major again with other synonyms: the checks you asked for pass, but the protection holds only for the abbreviations the code lists. A doubled specials figure in a demand letter is a number I can cite to discount the package, and the one click the paralegal sees ('separate charge for a service') does not tell her the line repeats an earlier one.",
   "fix": "When an undated countable line has the same amount as a dated or accepted charge in the same case and the date is compatible, ask for the likely_duplicate confirm regardless of whether the service words match (over-asking costs one named confirm; a missed repeat costs the letter). If the words must still match, add the families ED/emergency department, initial evaluation/new patient exam, CAT/CT, consult/consultation to the alias list.",
   "acceptance_test": "API test over the four pairs above: GET case shows count_confirm.flag likely_duplicate on the undated line, POST count with only separate_charge returns 422 CONFIRM_REQUIRED naming likely_duplicate, and the letter total equals the truth. The 10 held-out pairs that hold and the lib11 $6,000.00 count stay as they are."},
  {"severity": "minor",
   "title": "A quote or proposal worded as a charge is countable: 'Proposed therapy visit charge' and 'Quoted charge for therapy visit'",
   "evidence": "paste_http_r3_held.txt, Path A, single record, base $830.00 (exam $250, x-ray $180, therapy visit $400): h_proposed 'Proposed therapy visit charge $600.00.' -> 'Billed charges accepted from these records: $1,430.00'; h_quote 'Quoted charge for therapy visit $600.00.' -> $1,430.00. Both show countable True and count_confirm None. 'Estimated future charge $5,000.00.' (est_future) is refused NOT_COUNTABLE in the same harness.",
   "why_it_matters": "A figure the provider has not billed would be summed under 'Billed charges accepted from these records'. It is neither a payer nor a summary nor a fee wording, so I do not read it as covered by scope cut 7g; rated minor because it is the same closed-list residue 7g admits for other wordings and the paralegal sees the line before the click. The orchestrator may decide it is inside 7g.",
   "fix": "Add proposed, quoted, quote, projected, anticipated, future and pre-authorized to the estimate wording that already produces the 'Estimated' reason.",
   "acceptance_test": "Unit test: the two lines above are countable=false with the estimate reason and the letter total stays $830.00."}
 ],
 "whats_right": [
  "All 23 payer, allowed, lifetime, account and summary wordings from my r2 blocker are NOT_COUNTABLE over HTTP and leave the letter at the $830.00 truth.",
  "The listed reworded repeats (PT, New pt, xray, radiograph, CPT vs description, restated, reprint with abbreviations, three copies) all require the likely_duplicate confirm, and ten of fourteen held-out repeats do too.",
  "lib11 counts to $6,000.00 and every library case is at or below its hand total with letter lines identical to r2."
 ],
 "questions_for_chris": []}
```
