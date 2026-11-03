# T-079 round 2: library packets lib08..lib15 (paralegal-reviewer, a74b727 + ce70bd2)

Verdict: pass. No blockers, no majors. Both round-1 majors are closed. Four round-1 minors stay open, plus two small new ones.

**1. lib09 total of $6,390 is the right reading.** I read the packet text, not the expected.json.
- Record 7 (txt line 36) reads: "consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
- 1,300 + 4 x 400 = 2,900, so the statement's saldo is the whole clinic bill. There is no payment line and no second clinic bill in the packet.
- Record 2 (txt line 11) carries one "Consulta: $650.00". The statement's "consultas" is plural at 1,300 = 2 x 650.
- So the note's $650 is one of the consults inside the $1,300, and the second consult is the intake visit (record 4, "03/05/2026").
- Counting the statement once gives 2,940 + 2,150 + 1,300 = 6,390. Adding the $650 would bill one visit twice, and the clinic's own saldo has no room for it.
- A2 ($650) is `unclear`, not in the total, with an overlap note. Every amount and flag evidence string in lib09 is a substring of the packet (script output: `non-substring evidence: []`).
- M5 bans 7,040, 7,990, 9,290, 2,900 and 1,600.
- One caution, not a finding: 4 sessions at $400 is a stated count and rate, and the saldo corroborates $1,600. The packet still keeps it out of the total because no extended charge is printed. That matches R-CH-3 and the lib14 mileage treatment, where only the printed extension counts. See the question for Chris.

**2. Replay, no CONFLICT_PASS_INCOMPLETE.** I ran a `git archive` of ce70bd2 and a `git archive` of HEAD (81aa55e) on the fixture backend.
- All 8 packets (lib08 to lib15) ended `done` with no errors in both trees.
- The output has no CONFLICT_PASS_INCOMPLETE and no FIXTURE_MISS. Round 1 had both at 328428f.
- lib09 now loads r2, r4 and r7. The pipeline returns 6 dated entries plus 1 undated entry.

**3. `library-latest.md` names its source commit and reproduces.**
- The header reads "Source commit: a74b727b1ed94befbd09c0a3da0e8556e66f787c (tree: clean)".
- `git diff --stat a74b727 ce70bd2` touches only `evals/reports/library-latest.md`, so the report sits on the files it cites.
- I ran `python -m evals.library_report` on the ce70bd2 extract. All 15 table rows and the Known honest failures section match the committed file, with the header lines left out of the diff. My copy of the header says "unknown" because an archive has no git, so the provenance code does not invent a hash.
- The report states only lib01 r3 as a remaining honest failure.

**4. The PT-billed-with-no-note gap is honestly recorded.**
- lib09 expected.json has tolerated T2 (line 508, quoting "terapia física, 4 sesiones a $400.00 por sesión") and a notes line at 653: "Gap in the product (no flag type)...".
- A6 and A3 stay `rate`, not totaled, with "needs review".
- The card handoff says the same.
- I ran the fixture pipeline on lib09. Its flags are gap, pre_existing, three causation items and one record_warning. It raises nothing about the 4 billed sessions, so the gap is real and T2 stays tolerated rather than must.
- The recording has a hole, listed in finding 1.

**Not scored here:** lib09 still sums $7,040 and loads 4 of 7 entries in the report. Card T-110 owns both. In my run `totals.detected_pending_cents` was 509000, which is 2,940 + 2,150 in that field, so the product figure is not simply 7,040. T-110 should settle which path produces the number.

**Round-1 minors:**
- Closed: minor 3, the "Known honest failures" section now exists and carries the history.
- Closed in part: the table has no step or attempt-count column, and the location of the two moved fixtures is still not recorded (finding 2).
- Open: lib14 C1 cite (expected.json line 414 still cites records 5 and 6 only; txt line 31 "unchanged from the initial visit" versus line 16 "Pain 7 circled"); "Next visit 1O/2O" (line 21) against visit 12 on 10/20 (line 25).
- Open: lib12 plan-of-care vs actual. txt line 21 "Plan of care: 12 visits" against line 51 "treatment visits 1 through 16"; the lib12 flag list has no entry for it.
- Open: lib11 ledger. Line 46 now has three charge lines (exam $250.00, x-ray $180.00, visits 1 through 14 $2,310.00) but no per-date rows and no payer on the $300.00 payment. The limitation is not stated in the notes.
- Open nits: lib10 "Admitted for observation" (txt line 11) with type of bill 0111 (line 21); the lib13 to lib15 shifted dates; letters typed `phone_note`. The handoff says these were deliberately not done this round.

**Exercised:** `tools/board.py show T-079`; `git show --stat` on a74b727 and ce70bd2; `git archive` extracts of ce70bd2 and HEAD; the replay script on both; `evals.library_report` on the ce70bd2 extract with a diff against the committed report; my check script on lib09, lib11, lib12 and lib14; the fixture pipeline on lib09; `research/validate_library.py` (golden OK: 25 cases; identifier check ok, 15 packets) and `tests/unit/test_library_denylist.py` (6 passed). Evidence is in `artifacts/review-evidence/T-079-paralegal-r2-replay.out`, `-r2-check.out`, `-r2-lib09.out` and the matching `.py` files.

```json
{"card": "T-079", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commits a74b727 and ce70bd2; git archive extracts of ce70bd2 and HEAD 81aa55e in the session scratchpad; fixture backend; evals/library lib08..lib15, evals/library_report.py, evals/reports/library-latest.md",
 "exercised": [
  "python3 tools/board.py show T-079; git show --stat a74b727 ce70bd2; git diff --stat a74b727 ce70bd2 (report file only)",
  "Read the lib09 packet text and expected.json; checked 1,300 + 4 x 400 = 2,900 (saldo), the plural consultas line, and every amount and flag evidence string against the packet (artifacts/review-evidence/T-079-paralegal-r2-check.out)",
  "Fixture replay of lib08..lib15 on git archive extracts of ce70bd2 and HEAD 81aa55e: all done, no errors, no CONFLICT_PASS_INCOMPLETE (artifacts/review-evidence/T-079-paralegal-r2-replay.out)",
  "python -m evals.library_report on the ce70bd2 extract: tables and Known honest failures identical to the committed library-latest.md",
  "Fixture pipeline on lib09: flags and amounts read for any billed-without-note notice (artifacts/review-evidence/T-079-paralegal-r2-lib09.out)",
  "research/validate_library.py (golden OK 25 cases; identifier check ok 15 packets) and tests/unit/test_library_denylist.py (6 passed) on the extract",
  "Re-checked round-1 minors on lib10, lib11, lib12 and lib14 packet text and expected.json"
 ],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "packet_realism": 4, "expected_json_accuracy": 5, "fixture_honesty": 4, "report_reproducibility": 5},
 "findings": [
  {"severity": "minor",
   "title": "The PT-billed-with-no-note gap has no owner outside the T-079 card note and lib09 expected.json",
   "evidence": "evals/library/case_lib09_spanish_interpreter_espalda.expected.json:508 (tolerated T2) and :653 'Gap in the product (no flag type)'; card T-079 note 2026-11-02T06:34:38Z 'GAP (product)'; T-110 has one AC (4/7 entries and the consult double count) and no mention of billed sessions without a note; memory/SCOPE_CUTS.md has no entry (grep of board/cards, memory and submission found it only in T-079); fixture run of lib09 raises no notice about the 4 billed sessions.",
   "why_it_matters": "A bill with no matching note is a gap a paralegal expects the tool to surface. It is recorded as tolerated, but no card or scope-cut line says the product will not do it, so it can be lost at M3 close.",
   "fix": "Add a SCOPE_CUTS or product-gap line, or a small card, for billed-without-a-note notices (D-042 billing analysis), and cite it from the expected.json note.",
   "acceptance_test": "grep -rn 'billed_sessions_without_notes' finds a card id or SCOPE_CUTS row that owns the decision."},
  {"severity": "minor",
   "title": "Known honest failures table has no step or attempt count, and the two moved fixtures are still not located",
   "evidence": "evals/reports/library-latest.md:25-29 columns are packet, record, code, cause; line 31 gives the history in prose with 'cause not captured' for lib10 r6 and lib15 r7. Round-1 finding 3 asked for step, attempts and where the moved fixtures went.",
   "why_it_matters": "The row for lib01 r3 reads only 'FIXTURE_MISS'. Nobody can tell a model flake from a packet-text problem, which was the point of the round-1 minor.",
   "fix": "Add step and attempts columns, with 'not captured' where unknown. Add one line saying where the two moved fixtures went.",
   "acceptance_test": "Every row in the Known honest failures table has step, attempts and cause cells filled or marked 'not captured'."},
  {"severity": "minor",
   "title": "Round-1 minor still open: lib14 conflict C1 cites records 5 and 6 and leaves out the initial-visit pain; visit numbering is inconsistent",
   "evidence": "case_lib14_handwritten_chiro_scans.expected.json:414 C1 cite all [5,6]; txt:31 'Pain 6/10, unchanged from the initial visit' versus txt:16 'Pain 7 circled'; txt:21 'Next visit 1O/2O' after visit 9 versus txt:25 visit 12.",
   "why_it_matters": "The adjuster's 'unchanged' argument rests on 7 versus 6. The expected evidence omits the initial visit.",
   "fix": "Add the record 3 pain excerpt to C1's cite and evidence, and make the visit numbers fit the 'Next visit' date.",
   "acceptance_test": "C1 evidence includes 'Pain 7 circled'; validate_library.py passes."},
  {"severity": "minor",
   "title": "Round-1 minor still open: plan-of-care vs actual visits is not expected in lib12 (nor lib11 three times weekly)",
   "evidence": "case_lib12_records_review_credibility.txt:21 'Plan of care: 12 visits' versus :51 'treatment visits 1 through 16'; lib12 flags and tolerated list are G1, K1-K9, P1 with no plan/actual item.",
   "why_it_matters": "This is the Appendix A plan-vs-actual discrepancy. The packet carries it but nothing tests that the tool surfaces it.",
   "fix": "Add a should or tolerated entry with both excerpts, or state in the notes that it is deliberately not required.",
   "acceptance_test": "lib12 expected.json lists the discrepancy as must, should or tolerated, or notes why it is not expected."},
  {"severity": "minor",
   "title": "Round-1 minor still open: lib11 ledger has no per-date rows and no payer on the payment, and the limit is not stated",
   "evidence": "case_lib11_priors_and_ledger.txt:46 'treatment visits 1 through 14 charge $2,310.00 ... Payment received $300.00'; lib11 expected.json notes contain no mention of the one-line limit.",
   "why_it_matters": "A charge cannot be tied to a date of service, and paid-versus-incurred needs the payer.",
   "fix": "Add dated ledger rows or a payer on the payment, or state the limit in expected.json notes.",
   "acceptance_test": "lib11 has 3 or more dated charge rows and a payer, or the notes state the limitation."},
  {"severity": "nit",
   "title": "Round-1 nits still open (deliberately not done in round 2)",
   "evidence": "case_lib10_eob_ub04_cms1500.txt:11 'Admitted for observation' with :21 'type of bill 0111'; lib13 to lib15 records dated after 2026-11-02; letters and affidavits typed phone_note; lib08 visit 22 at week 8.",
   "why_it_matters": "A paralegal reading the packets notices these and may take them for tool errors.",
   "fix": "Optional: use type of bill 0131, align visit counts, and note the shifted-date convention in the README.",
   "acceptance_test": "n/a (optional)"}
 ],
 "whats_right": [
  "lib09 counts the consult once at $6,390 and states the overlap in A2, A5 and the notes, with 7,040 banned in M5.",
  "library-latest.md carries its source commit and tree state, the Known honest failures section, and reproduces row for row from the cited files.",
  "All eight packets replay done with no errors on the fixture backend at both ce70bd2 and HEAD."
 ],
 "questions_for_chris": [
  "lib09 states 4 sessions at $400 per session, and the saldo of $2,900 confirms $1,600. Should the product total a stated count times a stated rate when the statement prints no extended charge, or keep it out and list it as 'request itemized PT ledger'? The packets keep it out, as R-CH-3 does."
 ]}
```
