# T-079 review: library packets lib08..lib15 (paralegal-reviewer, commit 328428f)

Verdict: changes. No blockers. Every amount, date and flag excerpt in the eight expected.json files is a verbatim substring of its packet (my script found 0 mismatches), the gap day counts recompute, and the packets cover every format in the brief. Two majors remain.

**Coverage (all present):**
- Ledger with billed, adjustment, payment and LOP: lib11 record 9 and lib15 record 7.
- CMS-1500 with decimal-less boxes: lib10 record 8 and lib14 record 7. Both sums check (185.00 + 210.00 + 96.00 = 491.00; 255.00 + 75.00 = 330.00).
- UB-04 with the FL44 rate beside the charge: lib10 record 4. 1,640.00 x 3 = 4,920.00, and the lines sum to 8,123.50.
- Spanish clinic note: lib09 records 2, 4 and 7.
- OCR-noisy intake: lib09 record 4 and lib11 record 6.
- Mixed-side Waddell sentence: lib12 record 7.
- EMS report and ambulance bill: lib14 records 1 and 8. 8.7 x 21.50 = 187.05, and 1,380.00 + 187.05 = 1,567.05.
- 18.001 affidavit and narrative letter: lib15 records 9 and 6.
- Pre-suit carrier records review: lib12 record 9.

**Hand-checked in full:** lib10, lib11, lib12 and lib14 (entries, dates, amounts, flags), plus total and gap arithmetic for all eight. Gap counts, totals and the "forbidden" sums are right. lib10's EOB-vs-UB-04 $100.00 mismatch is real in the text (8,123.50 vs 8,023.50) and the other EOB figures reconcile (8,023.50 - 3,610.00 = 4,413.50; x 0.8 = 3,530.80).

**Denylist and labels:** `python3 research/validate_library.py` printed "golden OK: 25 cases" and "identifier check: ok (15 packets, 80 denylist terms)". The `--self-test` ran ok and `tests/unit/test_library_denylist.py` passed 6 tests. All eight packets open with the SYNTHETIC line.

**Exercised:**
- Replayed all 8 packets on the fixture backend at an extract of commit 328428f, and again in the live worktree. Evidence is in `artifacts/review-evidence/T-079-paralegal-replay-328428f.out` and `T-079-paralegal-replay-worktree.out`.
- Ran my own app on port 7897 (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, DB in the scratchpad), loaded lib12 and lib09 through the API, then killed it. Output is in `T-079-paralegal-app.out`.
- lib12 came up with 10 entries, $5,790 pending across 4 charges, and $145 held out as a rate.
- lib09 came up with only 4 of 7 entries; the three Spanish records are missing.

**Honest failures and the disclosed breach:**
- At commit 328428f the replay shows exactly lib09 r2, lib10 r6 and lib15 r7 as `LLM_FAILED_AFTER_RETRIES` / `FIXTURE_MISS`. That matches the single-pass state, so the correction holds for those three.
- Finding 2 covers what the same replay shows beyond those three, and finding 3 covers how they are documented.

**Findings:**
1. **Major, lib09 expected total looks double-counted.** The packet's own text contradicts the $7,040 total.
   - Record 2 (txt line 11) says "Consulta: $650.00". Record 7 (txt line 36) says "consultas $1,300.00", which is 2 x $650, and the packet has one consult note.
   - The `expected.json` counts both ($2,940 + $650 + $2,150 + $1,300 = $7,040; counted ids A1, A2, A4, A5; note at expected.json line 624) with no overlap note.
   - A paralegal would not put a statement's consult line and the consult note's own fee in one total.
   - The statement also bills 4 PT sessions with no PT note anywhere, and nothing flags or tolerates a bill without a note.
2. **Major, the "5 packets clean" claim in AC 2 does not reproduce at the cited commit.**
   - At 328428f every one of the 8 packets ends `done_with_errors` with `CONFLICT_PASS_INCOMPLETE`, on top of the three expected `FIXTURE_MISS` errors.
   - The committed `library-latest.md` shows "done" for lib08, lib11, lib12, lib13 and lib14, so it was generated against uncommitted worker edits. The handoff itself notes `conflicts_v1.md` was removed mid-flight.
   - In the current worktree, lib09 also loses r4 and r7 (`extract_es`), so three of its seven records fail.
3. **Minor, the honest failures are documented only in the card handoff and agent memory.**
   - Neither `library-latest.md` nor `library_report.py` records the cause or attempt count.
   - Two of the three causes were "not captured".
   - Those three records are the Spanish note, the EOB and the 18.001 affidavit, which are the formats this card exists to test.
   - The location of the two moved fixtures is not recorded.
4. **Minor, lib14 conflict C1 cites the wrong pair.**
   - It cites record 5 ("Pain 4 circled") against record 6.
   - The real inconsistency is record 6's "Pain 6/10, unchanged from the initial visit" against record 3's initial "Pain 7 circled". Record 3 is not in C1.
   - The packet is also incoherent on one point. Record 4 (txt line 21) says "Next visit 10/20", yet the 10/20 page is "visit 12" after visit 9 on 10/06.
5. **Minor, plan-of-care vs actual visits is not in the expected flags.**
   - lib12 record 4 says "Plan of care: 12 visits" while record 10 charges "treatment visits 1 through 16".
   - lib11 plans three times weekly but shows only 14 visits in 9 weeks.
   - This is the Appendix A discrepancy, and the library has no must-or-tolerated entry for it.
6. **Minor, ledgers are single flattened lines.**
   - lib11 record 9 (txt line 46) is one sentence: "treatment visits 1 through 14 charge $2,310.00".
   - There are no per-date-of-service rows and no payer on the $300.00 payment. The research table asked for "payment + payer".
   - The one-line excerpt limit was disclosed, but I cannot reconcile a charge to a date of service from it.
7. **Nit, small realism points.**
   - lib10 says "observation" but the UB-04 type of bill is 0111, which is inpatient.
   - lib08 shows visit 22 at week 8 on a twice-weekly plan.
   - lib11 K1 types the attorney referral and LOP flag as `causation`, a repeat of the T-052 lib06 note.
   - lib13 to lib15 contain records dated 2026-11-02 and later (to 2027-02-03).
   - Letters and affidavits use kind `phone_note`.

```json
{"card": "T-079", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 328428f (evals/library/case_lib08..lib15 txt + expected.json, evals/library_build_v2.py, evals/library_report.py, evals/reports/library-latest.md, fixtures); extract of 328428f at artifacts/review-evidence/T-079-tree plus live worktree at HEAD e3fc01c (dirty); own app on port 7897 (fixture, curated, local); lib09 and lib12 loaded",
 "exercised": [
  "python3 tools/board.py show T-079; D-042 and D-043 in memory/ORCHESTRATOR_DECISIONS.md",
  "python3 research/validate_library.py (golden OK 25 cases; identifier check ok 15 packets) and --self-test (ok, 408 planted variants)",
  ".venv/bin/python -m pytest tests/unit/test_library_denylist.py (6 passed)",
  "Read all 8 packet texts end to end and the expected.json for lib09, lib10, lib11, lib12, lib14 (lib08, lib13, lib15 amounts, flags and notes)",
  "artifacts/review-evidence/T-079-paralegal-check.py: excerpts, dates, sources, required terms, amount and flag evidence are substrings of the packet text; gap days and totals recomputed; no mismatches (T-079-paralegal-check.out)",
  "Fixture replay of all 8 packets at a git archive extract of 328428f and in the live worktree (T-079-paralegal-replay-328428f.out, T-079-paralegal-replay-worktree.out)",
  "Own app instance on port 7897 with LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB in the scratchpad: GET /api/library; created, ran and read lib12 and lib09 (T-079-paralegal-app.out); stopped by pid, port 7897 confirmed closed",
  "Read evals/reports/library-latest.md, .claude/agent-memory/qa/project_library_packets.md, git show --stat 328428f, research/case-library-sources-v2.md packet and must-contain tables"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "packet_realism": 4, "coverage_vs_brief": 5, "expected_json_accuracy": 4, "fixture_honesty": 3},
 "findings": [
  {"severity": "major",
   "title": "lib09 expected total ($7,040) counts the $650 consult and the $1,300 statement consultas line together",
   "evidence": "evals/library/case_lib09_spanish_interpreter_espalda.txt:11 'Consulta: $650.00'; :36 'consultas $1,300.00'; expected.json:356-357 explicit_charges_total 7040, counted_amount_ids A1,A2,A4,A5; expected.json:624 'Charges counted: 2,940 + 650 + 2,150 + 1,300 = 7,040'. $1,300 is 2 x $650 and the packet holds one consult note, so the note's $650 is most likely inside the statement line; no overlap note, no tolerated flag. The statement's 4 PT sessions have no PT note and are not flagged or tolerated either.",
   "why_it_matters": "A total that likely counts the same visit twice is what the adjuster catches, and an eval that locks it in rewards the tool for the double count. The 'bill with no matching note' gap is also a standard flag.",
   "fix": "Either drop A2 from the counted ids (total $6,390) and mark it unclear 'may be inside the statement consultas line', or keep one and add an explicit overlap note and a tolerated billing-mismatch flag. Add a tolerated or must flag for 4 PT sessions billed with no PT record.",
   "acceptance_test": "validate_library.py passes with a lib09 total of 6390 (or a documented single-count choice); a must_not on amount_value 7040; the expected.json notes name the overlap and the PT bill without a note."},
  {"severity": "major",
   "title": "AC 2 'fixture replay 5 packets clean' does not reproduce at 328428f; the committed library report was generated against uncommitted worker changes",
   "evidence": "artifacts/review-evidence/T-079-paralegal-replay-328428f.out: all 8 packets status done_with_errors with CONFLICT_PASS_INCOMPLETE; lib09 r2, lib10 r6 and lib15 r7 FIXTURE_MISS. evals/reports/library-latest.md shows status 'done' for lib08, lib11, lib12, lib13 and lib14. Live worktree (T-079-paralegal-replay-worktree.out): lib09 FIXTURE_MISS on r2, r4 and r7 (step=extract_es), so only 4 of 7 entries load (T-079-paralegal-app.out); handoff says conflicts_v1.md removal is mid-flight.",
   "why_it_matters": "A fixture set that replays clean only against an uncommitted tree is not a reproducible artifact. On lib09 the user sees 4 of 7 records and the Spanish clinic note, the point of the packet, is missing.",
   "fix": "After the backend changes land (T-085 Spanish extract, T-094 conflicts), re-record or re-verify the fixtures at a clean commit. Re-run library_report there and print the commit hash and git-dirty state in library-latest.md. Re-state AC 2 with that evidence.",
   "acceptance_test": "At a clean checkout, `python -m evals.library_report` reports only the documented honest failures for lib08..lib15 (no CONFLICT_PASS_INCOMPLETE; lib09 not failing r4 or r7), and the report header carries the commit hash."},
  {"severity": "minor",
   "title": "The three honest LLM_FAILED_AFTER_RETRIES records are documented only in the card handoff and agent memory",
   "evidence": "evals/reports/library-latest.md shows 'LLM_FAILED_AFTER_RETRIES r2 FIXTURE_MISS' with no cause or attempts; handoff: lib10 r6 and lib15 r7 'cause not captured'; evals/library_report.py docstring is generic; no evals README entry. The two fixtures moved out of tests/fixtures/llm have no recorded location (git status shows no untracked copy).",
   "why_it_matters": "The three failing records are the Spanish note, the EOB and the 18.001 affidavit. Without a recorded cause nobody can tell a model flake from a packet-text problem, and the breach correction cannot be audited.",
   "fix": "Add a 'Known honest failures' section generated into library-latest.md (packet, record, step, attempts, cause or 'not captured') and record where the moved fixtures went.",
   "acceptance_test": "library-latest.md lists lib09 r2, lib10 r6 and lib15 r7 with step, attempt count and cause."},
  {"severity": "minor",
   "title": "lib14 conflict C1 cites record 5 vs 6 instead of the initial-visit pain; 'Next visit 10/20' contradicts 'visit 12' on 10/20",
   "evidence": "case_lib14_handwritten_chiro_scans.txt:31 'Pain 6/10, unchanged from the initial visit'; the initial visit (record 3) says 'Pain 7 circled'; expected.json:414 C1 cites records 5 and 6 only. txt:21 'Next visit 1O/2O' after visit 9 on 10/06, but record 5 (10/20) is 'visit 12'.",
   "why_it_matters": "The adjuster's 'unchanged' argument rests on 7 vs 6 and on 4 vs 6. The expected evidence leaves out the initial visit. The visit numbering makes the cadence look invented.",
   "fix": "Add record 3 (and 4) to C1's cite and evidence, or reword the re-exam sentence. Make the visit numbers consistent with the 'Next visit' date.",
   "acceptance_test": "C1 evidence includes the 'Pain 7 circled' excerpt; the validator passes; visit 12 follows visit 9 by a plausible interval."},
  {"severity": "minor",
   "title": "Plan-of-care vs actual visits is not expected anywhere in the new packets",
   "evidence": "case_lib12_records_review_credibility.txt:21 'Plan of care: 12 visits' vs :51 'treatment visits 1 through 16'; lib12 expected.json has no plan-vs-actual flag, tolerated entry or must_not. lib11 txt:23 'chiropractic care three times weekly' vs 14 visits in 9 weeks (03-27 to 05-29).",
   "why_it_matters": "This is the Appendix A PT plan vs actual discrepancy. A packet that carries it without an expectation cannot test whether the tool surfaces it.",
   "fix": "Add a should or tolerated flag for lib12 (12 planned, 16 charged), or word the statement so the discrepancy is deliberate and documented as not required.",
   "acceptance_test": "lib12 expected.json lists the plan/actual discrepancy as must, should or tolerated with both excerpts."},
  {"severity": "minor",
   "title": "Ledgers are single flattened lines: no per-date-of-service rows and no payer on the payment",
   "evidence": "case_lib11_priors_and_ledger.txt:46 'treatment visits 1 through 14 charge $2,310.00 ... Payment received $300.00'. research/case-library-sources-v2.md lib11 row: 'ledger with billed, adjustment, payment + payer, balance and LOP columns'.",
   "why_it_matters": "A reconcilable ledger ties each charge to a date of service. A range line cannot be checked against the visit notes, and the payer matters for the paid-vs-incurred question.",
   "fix": "Add dated ledger lines (one excerpt per line, or several records) and name the payer on the payment. If the single-line limit stays, say so in the expected.json notes and the library README.",
   "acceptance_test": "lib11 holds at least 3 dated charge rows and a payment with a payer, or the limitation is stated in expected.json notes."},
  {"severity": "nit",
   "title": "Small realism and labeling points",
   "evidence": "lib10 txt:15 'Admitted for observation' with UB-04 type of bill 0111 (inpatient); lib08 PT visit 22 on 2026-03-23, 8 weeks into a twice-weekly plan; lib11 expected.json:560 K1 typed causation for an attorney referral and LOP (same as the T-052 lib06 note); lib13 to lib15 records dated 2026-11-02 and later (to 2027-02-03); letters and affidavits typed phone_note.",
   "why_it_matters": "A paralegal reading the packets notices these, and they could be mistaken for tool errors.",
   "fix": "Optional. Use TOB 0131 for observation, align the visit counts, and note the shifted-date convention in the README.",
   "acceptance_test": "n/a (optional)"}
 ],
 "whats_right": [
  "Every excerpt, amount and flag evidence string in the eight expected.json files is a verbatim substring of its packet, and the gap and total arithmetic recomputes.",
  "The traps are well chosen: UB-04 rate vs charge, the 0001 repeat, an EOB that is $100.00 off the bill, decimal-less CMS-1500 boxes with stated truth, and mileage extended to $187.05.",
  "lib12 keeps D-043 intact: 0/5 Waddell and No Waddell stay unflagged while the mixed-side and contrast sentences flag."
 ],
 "questions_for_chris": [
  "Should a statement line that restates an earlier note's fee (lib09 $650 inside $1,300) count once, or stay a reviewer decision? I assumed once."
 ]}
```
