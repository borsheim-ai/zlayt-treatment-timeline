# T-202 round 8 (D-075, cd7fd27): paralegal review (Maria Delgado, senior PI paralegal)

**Verdict: pass.** The round-7 blocker is closed. Every charge line in the sample, case_09, lib10 and lib11 letters reads exactly `<source as written>, date of service [__________] (record dated <Month D, YYYY>)`. Each date is the record's own Date header in the input. "statement dated" appears nowhere in a letter, in the Step 3 screens or in the app code. `python -m evals.letter_check` reports 0 over 25 cases. My r7 probe (an ER discharge summary whose excerpt opens "ER charges:") now prints "(record dated January 9, 2026)". The kind classifier I blocked in r7 is gone, so there is no label rule left to get wrong. One minor carried from r7 remains (finding 1).

**Pin.** `git archive cd7fd27` (tree 487a191a8b26) extracted to `artifacts/review-evidence/T-202-paralegal-r8/archive`. HEAD moved to 304ba58 during the review. `git diff --name-only cd7fd27 HEAD` lists only docs/LLM_VS_CODE.md and memory/*.md, and `git diff --stat cd7fd27 HEAD -- app evals tests` is empty, so the results apply to HEAD.

**Servers.** Demo mode on 127.0.0.1:7993 (health: local_mode false), PID 93310. Local mode on 127.0.0.1:7992 (local_mode true), PID 93175. Both were killed, and lsof exit 1 with curl 000 on each port. Port 7991 was already held by another process before I started, so I did not use or touch it.

**Checks.**
- Charge lines over HTTP: 3 in demo mode (sample 2, case_09 1) and 8 in local mode (sample 2, case_09 1, lib10 4, lib11 1). All match the exact blank form. "statement dated" count in the letter, the case JSON and the export JSON is 0 for every case. Totals: $8,390.00, $275.00, $8,123.50, $3,260.00.
- Charge lines in the UI, through Step 1 to Step 4 (Chromium, keyboard accept): sample (demo), lib10 and lib11 (local). Letter lines are exact. Step 3 shows `date of service [__________] (record dated ...)` on each charge row. "statement dated" count is 0 in Step 3 and Step 4. The 7 "statement date" hits in lib11 Step 3 are the record's own quoted words: `Itemized ledger, statement date 06/15/2026`.
- Record dates, checked by a parse of the INPUT text by my script: sample ER 2026-01-09, MRI 2026-05-29; case_09 2026-03-01; lib10 2026-06-19 on all 4 lines; lib11 ED 2026-03-18. 19 in-process charge lines (accepted-all and counted variants): form exact, date equal to the input header, source as written, 0 problems.
- Teeth: a printed "date of service March 6, 2026" and a wrong record date are rejected in all four cases (8 of 8). A "(statement dated X)" mutant is rejected by `letter_check.charge_date_violations` in all four cases (4 of 4).
- r7 probe `label_repro_r8.py`: V1 (ER summary opening "ER charges: $6,240.") prints "(record dated January 9, 2026)". V2 (PT visit opening "Payment plan discussed.", quote "Discharge visit 97110 charge $185.00.") prints "(record dated March 6, 2026)". `charge_date_violations` is [] on both.

**Verify-quickly score (4).** Each amount and its quote check in one step. The date in parentheses is the record's own date and matches the header. The date of service is a blank the paralegal fills herself, which is honest. It is a manual lookup on every charge, so I do not score 5.

**Model.** This review ran on claude-sonnet-5-5, the model I am running as. My definition expects claude-opus-5-5 for judgment reviews. See questions_for_chris.

**Not exercised.** The case_09 Step 3 UI screens (the demo offers only the sample case in the UI; case_09 was checked through the HTTP API and the in-process letter, including the case JSON). Timeline entries beyond reaching Step 3, and the full 25-case corpus label count. The lib11 ledger lines were counted in the UI (the 3 Fennimoor lines are in the UI letter) and in-process, not over HTTP.

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive cd7fd27 (tree 487a191a8b26728bd84e4bc0c4c1b48e77b5a67b) extracted to artifacts/review-evidence/T-202-paralegal-r8/archive; HEAD moved to 304ba58 (docs and memory only, app/evals/tests diff empty); demo-mode app at http://127.0.0.1:7993 (PID 93310) and local-mode app at http://127.0.0.1:7992 (PID 93175), LLM_BACKEND=fixture FIXTURE_SET=curated; both stopped (lsof exit 1, curl 000). Cases: sample, case_09, lib10, lib11 (SYNTHETIC inputs from evals/golden and evals/library). Evidence: artifacts/review-evidence/T-202-paralegal-r8/.",
 "exercised": [
  "Read personas/paralegal.md (live dossier), reviews/T-202-paralegal-r7.md (blocker), my memory notes for r7 and run pitfalls, board.py show T-202 (r7 findings and the D-075 handoff), memory/ORCHESTRATOR_DECISIONS.md D-073 and D-075",
  "git rev-parse --short HEAD: cd7fd27 at the start, 304ba58 at the end; git diff --name-only cd7fd27 HEAD: docs/LLM_VS_CODE.md, memory/LESSONS.md, memory/ORCHESTRATOR_DECISIONS.md, memory/PROGRESS.md, memory/SCOPE_CUTS.md; git diff --stat cd7fd27 HEAD -- app evals tests: empty",
  "git archive cd7fd27 | tar -x into artifacts/review-evidence/T-202-paralegal-r8/archive (tree 487a191a8b26728bd84e4bc0c4c1b48e77b5a67b)",
  "run_letter_check_r8.py (python -m evals.letter_check, with -I against the archive): {\"value\": 0, \"cases\": 25, \"held_out_entries\": 11, \"backend\": \"fixture\"}, exit 0 (letter_check.out)",
  "check_letters_r8.py on the archive (sample, case_09, lib10, lib11 through evals.letter_check.letters_for, accepted-all and counted): 19 charge lines, each exact form with kind 'record', parenthetical date equal to the input Date header (parsed by this script from the raw text), source as written, 'statement dated' absent from every letter; problems 0; exit 0; 8 teeth mutants (printed DOS, wrong record date) all rejected (check_letters_r8.out)",
  "teeth_statement_r8.py: a '(record dated' to '(statement dated' mutant is rejected by letter_check.charge_date_violations in all four cases (teeth_statement_r8.out)",
  "Demo-mode server on 127.0.0.1:7993 and local-mode server on 127.0.0.1:7992 from the archive (serve_r8.py with -I); live_letters_r8.py over HTTP (create, run, status, accept every pending entry, amount and flag, GET export): demo sample and case_09, local sample, case_09, lib10 and lib11; every charge line is the exact blank; statement-dated counts 0 in letter, case JSON and export JSON (live_demo_summary.out, live_local_summary.out, live_demo/, live_local/)",
  "ui_step3_r8.py in Chromium through the real UI (Open the sample case or library tile, Draft, Step 2 keyboard accept, Step 3, Step 4): demo sample, local lib10, local lib11; Step 3 and Step 4 'statement dated' counts 0; Step 3 rows read 'date of service [__________] (record dated ...)'; letter charge lines exact (ui_demo_sample.out, ui_local_lib10.out, ui_local_lib11.out, *-step3.txt, *-letter.txt, ui_demo_sample-step3.png and the other -step3.png files)",
  "label_repro_r8.py (the r7 probe: V1 ER summary opening 'ER charges:', V2 PT visit opening 'Payment plan discussed'): both print '(record dated ...)' and charge_date_violations is [] (label_repro_r8.out)",
  "grep -rIn 'statement dated' on archive/app and archive/evals/*.py: no hits",
  "Not exercised: case_09 Step 3 UI, timeline entries beyond reaching Step 3, the 25-case corpus label count, lib11 ledger lines over HTTP"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "letter_dates_correct": 5, "blank_label_correct": 5, "adversarial_dates_correct": 5},
 "findings": [
  {"severity": "minor",
   "title": "Carried from rounds 6-7: a 14-visit ledger charge still prints a single 'date of service' blank",
   "evidence": "ui_local_lib11-letter.txt:31-32: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $2,310.00' with quote 'treatment visits 1 through 14 charge $2,310.00'. check_letters_r8.out holds the same line for the counted lib11 variant.",
   "why_it_matters": "One date blank over 14 visits asks the paralegal for one date for a range, and the quote gives none. The exact form is pinned in letter_check, so this is a spec choice, not a defect in the code. It does not print a wrong fact. Under D-075 item 1 this is accepted debt for SCOPE_CUTS, so I rate it minor and do not ask for a round.",
   "fix": "Record the choice in SCOPE_CUTS: either allow 'dates of service [__________]' for a quote that counts visits (D-073 and letter_check change together), or note in the internal review notes that the line covers 14 visits.",
   "acceptance_test": "The lib11 $2,310.00 line prints the plural form, or its notes line says it covers 14 visits; letter_check accepts only the chosen form."}
 ],
 "whats_right": [
  "Every charge line is the same exact blank with the record's own date, equal to the input Date header on all 19 in-process and 11 live lines, and 'statement dated' appears nowhere in a letter, Step 3 or the app code.",
  "The r7 label blocker is gone for good: removing the bill-versus-record classifier means no wording rule can misname a discharge summary, and letter_check rejects a '(statement dated X)' mutant in all four cases.",
  "Totals still match the accepted charges ($8,390.00, $275.00, $8,123.50, $3,260.00), and the blank never prints a service date, so no date of service is invented."
 ],
 "questions_for_chris": [
  "Model: this review ran on claude-sonnet-5-5, the model I am running as. CLAUDE.md section 6 and my dossier expect claude-opus-5-5 for judgment reviews. Does the T-202 close-out need an Opus re-run?"
 ]}
```
