# T-207 staff-engineer review, r2

Reviewer: staff-engineer-reviewer (Marcus Lee persona), fresh context, read-only on product code. Model running: claude-sonnet-5-5.

Scope: docs/LLM_VS_CODE.md rows 2 and 3 as fixed in efda639, checked against the code at 8cb5bd2 (a git archive in a scratch directory; the product tree was not edited). `git diff --stat 8cb5bd2 HEAD -- app/backend/service_date.py app/backend/encounter_types.json app/backend/export.py app/backend/store.py evals/letter_check.py docs/LLM_VS_CODE.md tests/unit` shows only `docs/LLM_VS_CODE.md | 4 ++--` (efda639), so the code did not move between 8cb5bd2 and HEAD ad0d91a. Rows 30-31 of the working copy have the same md5 as `git show efda639:docs/LLM_VS_CODE.md`.

## Verdict: changes (no blocker, two majors, four minors)

## Does stating the five-year bound as 1,830 days settle it?

The statement is accurate. It is not enough.

Accurate: probe D1 (statement 2026-06-30, ledger) gives "1830d before (2021-06-26) | stated" and "1831d before (2021-06-25) | not_stated | reason=implausible". `service_date.py:109` has `_YEARS_BEFORE = 5` and `:328` has `days=366 * _YEARS_BEFORE`. The sentence "a date a few days past five calendar years can still be read" is true (2021-06-26 is five years and four days before). That closes the doc half of r1 F2.

Not enough: the number is now a documented contract and nothing pins it. The only bound tests are the 1998 and 2031 fixtures (`tests/unit/test_t202_r3_allow_list.py:184-185`). I mutated the bound three ways at once (365 days per year, `>=` to `>` at the lower end, `<=` to `<` at the upper end) on the 8cb5bd2 archive and ran the whole unit suite: `6266 passed, 12 skipped, 1 deselected` (the deselected test, `test_e2e_contract.py::test_every_test_id_is_declared`, fails identically at the parent per the T-202 handoff and is not in this scope). r1 F2's acceptance test (a test at the boundary that kills the bound mutant) is therefore still open. Persona calibration: a bound with no boundary test is major. The doc is accurate for behaviour and still wrong to rely on for verification, because the "How it is checked" cell cites unit tests that cannot fail when 1,830 changes.

Whether a 1 to 4 day slack is acceptable product behaviour is a product call (Q1). If it is, pin it with tests. If it is not, fix the code, and the doc sentence changes with it.

## Row-by-row result

Holds (probe or code line in brackets):
- Rule (1), same-date-or-period order: `04/05/2026 - 13/05/2026` reads May 4 to May 13 [D2; service_date.py:265-275]. Two ends forcing different orders are not read [D2: "13/05/2026 - 05/13/2026 | ambiguous_numeric"].
- Rule (2), a service cannot follow its statement: read only when exactly one order is on or before the record date; with no record date it is not read [D2 rows for 2026-05-31, 2026-04-30 and None; service_date.py:272-274].
- Bound applies to every record, `implausible`, no bound without a record date [D1, D1nodate; service_date.py:323-328].
- Only an identified encounter lends its header date; bill, receipt, superbill, charge summary, administrative paper and unknown type do not [D3 rows; service_date.py:54-63, 414-434]. A labeled but unreadable date is not replaced by the header date [D3 "ER labeled-bad(2-digit) | two_digit_year", probe H1 mutant killed].
- Table `encounter_types.json` is read by `service_date.record_kind` (TYPES_PATH at :33) and by `evals/letter_check.py:234` with its own matcher; letter_check imports no service_date (grep). `python -m evals.letter_check` gives `"value": 0, "cases": 25`.
- Column heading set in row 2 matches `_H_SVC` (service_date.py:107-108) [D6: every listed heading is recognised; Posted and Entry Date are not].
- Row 3: the blank text and `export.charge_when` (export.py:215-226), the two note forms (service_date.py:156-162), counted charge has no note (store.py:139), hand-built dict without `dos_iso` keeps the record date (export.py:222-223). Billing view `dos_iso` is `billing._dos`, route at billing.py:1061, no import from export, store or present, no consumer in app/frontend.

Does not hold, or is not pinned: findings below.

## Exercised

1. `git rev-parse HEAD 8cb5bd2 efda639`, `git log --oneline -8`, `git diff --stat 8cb5bd2 efda639` (docs only, 2 lines), `git diff --stat 8cb5bd2 HEAD -- <scope files>`.
2. `git archive 8cb5bd2` into a scratch directory. Read service_date.py (434 lines), encounter_types.json, store.py:105-200, export.py:215-226 and 600-625, amounts.py:300-320 and 515-545, evals/letter_check.py:1-30, 225-240, 405-470, billing.py:136-145, rows 2 and 3 of docs/LLM_VS_CODE.md, the T-202 board card (handoff and notes), D-071 amendment 2 (ORCHESTRATOR_DECISIONS.md:94-95), and my r1 review.
3. `pytest` on the five date files (test_t202_r2_service_date_layouts, test_t202_r3_allow_list, test_t202_r4_encounter, test_t202_charge_service_dates, test_t200_undated_charge_label): 341 passed. `--collect-only` on test_t202_r4_encounter.py: 133 tests.
4. `python -m evals.letter_check` on the archive: value 0, cases 25.
5. Probes D1 to D7: artifacts/review-evidence/T-207-r2/probe_t207_r2.py and probe_t207_r2.out. Probes E1 to E5: probe2_t207_r2.py and probe2_t207_r2.out.
6. 25 mutants against the five date files: mutants_t207_r2.py and mutants_t207_r2.out (13 killed, 12 survived). Ten of them against evals.letter_check: mutants_t207_r2_letter.out (control E2 killed, the other ten survived). Two full-suite runs of tests/unit on mutated copies: B1+B2+B5 (6266 passed, 12 skipped, 1 deselected, 408 s) and R1+R3+L2+L3+L4+N1 (6266 passed, 12 skipped, 1 deselected, 397 s). The script restores each file; the archive's service_date.py md5 matched `git show 8cb5bd2` after the run.
7. `ls reviews | grep T-202` (no r4 review file), `git status` and `git diff HEAD --stat -- docs/LLM_VS_CODE.md` (empty).

## Findings

F1 (major). The five-year bound, the on-or-before boundary and the no-record-date case are documented and unpinned. Mutants B1 (365 per year), B2 (`>=` to `>`), B3 and B4 (5 to 4 and 6 years), B5 (`<=` to `<` at the record date) and B6 (no-date record refuses) all survive the five date test files and the letter eval; B1+B2+B5 together survive the full unit suite. Accurate wording does not fix a missing test.

F2 (major). Other statements in rows 2 and 3 are also pinned by no test. Mutant R3 (`len(determined) > 2`, so two ends that force different orders are read) and R1 (`<= ref` to `< ref` in rule 2) survive the full unit suite, with L2 (drop the `next ` guard), L3 (drop "encounter date" heading), L4 (drop "date of visit" heading) and N1 (a counted charge gets a note). r1 F6's acceptance asked that the Encounter Date mutant be killed; it still survives. R3 matters most: a period whose ends force different orders is exactly where a wrong date could print.

F3 (minor, would be major if a real path is shown). The doc says the header date is lent "only when the line has no labeled date of its own" and that a labeled date that cannot be read "is not replaced by the header date". `store.py:131` skips the look when `pos` is None: probe D4 gives "pos located | not_stated None implausible" but "pos None | stated 2026-01-09" for the same encounter line that labels 05/05/2026, and "D4c pos None, line labels 03/01/2026 | stated 2026-01-09" where the located path reads 2026-01-03. `tests/unit/test_t200_undated_charge_label.py:63` pins this with an excerpt `"x"`. I could not find a normal flow that gives `amount_pos` None for a pipeline amount (pipeline.py:417 sets excerpt_start from the figure), so I rate it minor. This is a doc/code divergence, not a preference.

F4 (minor). The allow-list text is narrower than the code. UB-04 "statement period" is read, not only "statement covers period" (probe D5: stated 2026-01-05 to 2026-01-09). Label connectors `is`, `was`, `from`, `between`, `#`, `-` and `(` also work (D7), and the doc names a colon, spaces or a dotted leader. The bill wordings "date of the run" and "treatment dates", the "from service" heading, and (d) taking a single labeled date (not only a period) are not listed (service_date.py:92-96, 101, 107-108, 415-428). The list is presented as exhaustive.

F5 (minor, question for Chris). The "never after next, last, prior..." guard is stated for the prose labels and the code applies it only there. A bill's own wordings are unguarded: probe E5, "Charge for last visit of 12/20/2025: office visit $220.00." prints 2025-12-20 as the date of service, and "next visit of" and "prior visit of" do the same, while "last DOS 12/20/2025" correctly gives non_service_date (service_date.py:89-93). D-071 amendment 2 note (ORCHESTRATOR_DECISIONS.md:95) accepts the bill wordings but not the missing guard. Either the doc says the guard stops at the prose labels or the code extends it.

F6 (minor). Two validation-cell counts overreach. "131 tests" is 133 (`pytest --collect-only`, test_t202_r4_encounter.py), copied from the backend handoff. "every reviewer probe from rounds 3 and 4 is a fixture" has no round 4 behind it: `ls reviews | grep T-202` shows no r4 review, and the test file's own docstring (line 1) says "Every probe from the round 3 paralegal and staff reviews". The honest sentence about the uncommitted 24-of-25 mutation run is right and should stay.

## What is right

1. The bound sentence is exact: 1,830 days is read, 1,831 is refused, and a few days past five calendar years is read (probe D1).
2. The two ambiguity rules, the encounter-only header date, and the classifier all behave as written and fail toward the blank (probes D2, D3, E4).
3. Row 3's blank, both note forms, the counted-charge exception and the hand-built-dict branch match the code; the code is unchanged from 8cb5bd2 to HEAD and `evals.letter_check` reads value 0 over 25 cases.

Outside my lens: the legal weight of the blank, and whether a paralegal reads the Step 3 note wording as helpful.

```json
{"card": "T-207", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "docs/LLM_VS_CODE.md rows 2-3 as of efda639 vs code at 8cb5bd2 (git archive in scratch; code unchanged to HEAD ad0d91a): app/backend/service_date.py, encounter_types.json, store.py:105-200, export.py:215-226, evals/letter_check.py; no app URL exercised",
 "exercised": ["git rev-parse/log/diff --stat: 8cb5bd2 to efda639 is docs only; scope files unchanged 8cb5bd2 to HEAD; rows 30-31 md5 equal at efda639 and working copy",
               "git archive 8cb5bd2 into scratch; read service_date.py in full, encounter_types.json, store.py:105-200, export.py:215-226 and 600-625, amounts.py:300-320 and 515-545, letter_check.py header and charge_date_violations, billing.py:136-145, rows 2-3, T-202 board card, D-071 amendment 2",
               "pytest on 5 date test files at 8cb5bd2: 341 passed; --collect-only test_t202_r4_encounter.py: 133 tests",
               "python -m evals.letter_check: value 0, cases 25",
               "probes D1-D7 (artifacts/review-evidence/T-207-r2/probe_t207_r2.py + .out) and E1-E5 (probe2_t207_r2.py + .out)",
               "25 mutants on date files (mutants_t207_r2.py + .out: 13 killed, 12 survived); 10 against letter_check (mutants_t207_r2_letter.out: 10 survived, control killed)",
               "full tests/unit on mutated copies: B1+B2+B5 and R1+R3+L2+L3+L4+N1 each 6266 passed, 12 skipped, 1 deselected (known failing test_every_test_id_is_declared)",
               "ls reviews | grep T-202 (no r4 review); git status and git diff HEAD --stat on the doc (empty)"],
 "verdict": "changes",
 "scores": {"row2_matches_code": 4, "row3_matches_code": 4, "date_is_code_only": 5, "bound_statement_accuracy": 5, "bound_and_rules_pinned_by_tests": 2, "validation_cell_claims": 3},
 "findings": [
  {"severity": "major", "title": "The five-year bound is stated exactly as 1,830 days, but no test pins it, the on-or-before edge, or the no-record-date case",
   "evidence": "service_date.py:109 '_YEARS_BEFORE = 5' and :328 'days=366 * _YEARS_BEFORE'; probe_t207_r2.out 'D1 1830d before (2021-06-26) | stated' and 'D1 1831d before (2021-06-25) | not_stated ... reason=implausible'; only bound tests are tests/unit/test_t202_r3_allow_list.py:184-185 (1998 and 2031); mutants_t207_r2.out 'B1 ... SURVIVED | 341 passed', 'B2 ... SURVIVED', 'B3', 'B4', 'B5 ... SURVIVED', 'B6 ... SURVIVED'; mutants_t207_r2_letter.out B1 B2 B5 B6 SURVIVED (value 0, 25 cases); full tests/unit with B1+B2+B5 applied: '6266 passed, 12 skipped, 1 deselected in 408.74s'",
   "why_it_matters": "The doc now makes 1,830 days a contract and row 3's How-it-is-checked cell cites unit tests as the check. Those tests pass when the constant becomes 1,825, when the lower edge flips, and when a service date equal to the record date is refused. r1 F2's acceptance test (a boundary test that kills the bound mutant) is still open. Persona calibration: a bound without a boundary test is major.",
   "fix": "Add unit tests through store.charge_service_date for a ledger with statement 2026-06-30: DOS 06/26/2021 (1,830 days) is stated, 06/25/2021 (1,831) is implausible; DOS equal to the record date is stated and one day after is implausible; a record with no date and DOS 03/13/1998 is stated. Chris decides whether the 1 to 4 day slack stays (Q1); if not, change the code to a calendar-year compare and update the doc sentence.",
   "acceptance_test": "Mutants B1 (365 per year), B2 (>= to >), B3/B4 (_YEARS_BEFORE 4 or 6), B5 (<= to < at the record date) and B6 (no-date record refuses) each fail at least one test in tests/unit; the tests are in the repo and named in row 3's cell."},
  {"severity": "major", "title": "Other statements in rows 2 and 3 are covered by no test: different-order period ends, rule 2's on-or-before edge, two headings, the next guard, the counted-charge no-note rule",
   "evidence": "mutants_t207_r2.out 'R3 rule1 two ends forcing different orders -> read | SURVIVED', 'R1 rule2 on-or-before -> before | SURVIVED', 'L2 next prefix guard removed | SURVIVED', 'L3 heading encounter date dropped | SURVIVED', 'L4 heading date of visit dropped | SURVIVED', 'N1 counted undated charge gets a note | SURVIVED' (all against 341 date tests); R1+R3+L2+L3+L4+N1 applied together to a copy and run over tests/unit: '6266 passed, 12 skipped, 1 deselected in 396.63s'; docs/LLM_VS_CODE.md:30 'two ends that force different orders are not read', ':31 carries no note'; r1 F6 acceptance 'M8 is killed' (Encounter Date) still unmet",
   "why_it_matters": "Each is a sentence in the binding table that the code can break without any test failing. R3 decides whether a period with contradictory ends prints a date or the blank, which is a printed-date correctness rule. The doc's own Validation cell says the dates are tested.",
   "fix": "Add one fixture per statement: '13/05/2026 - 05/13/2026' prints the blank; a rule-2 case where one order equals the record date; a table with an 'Encounter Date' heading and one with 'Date of Visit'; 'Next DOS 02/01/2026' is non_service_date; a counted undated charge has confirm_note None and an uncounted one has a note.",
   "acceptance_test": "Mutants R1, R3, L2, L3, L4 and N1 each fail at least one test in tests/unit."},
  {"severity": "minor", "title": "For an encounter record whose figure cannot be located, the header date is lent without looking at the line; the doc says only when the line has no labeled date",
   "evidence": "app/backend/store.py:131 'elif rec is None or pos is None or not item.get(\"excerpt\"): r = {... \"first\": rd ...} if (encounter and rd) else dict(none)'; probe_t207_r2.out 'D4 pos located | not_stated None implausible' vs 'D4 pos None | stated 2026-01-09 None'; 'D4c pos None, line labels 03/01/2026 (AFTER header) | stated 2026-01-09' vs 'D4d pos located, same line | stated 2026-01-03'; tests/unit/test_t200_undated_charge_label.py:63 pins it with excerpt 'x'; docs/LLM_VS_CODE.md:30 'only when the line has no labeled date of its own' and 'A labeled date that cannot be read in an encounter record is not replaced by the header date'",
   "why_it_matters": "The doc states a universal the code breaks on this path. Rated minor because pipeline.py:417 sets excerpt_start for every amount and I found no normal flow that yields pos None; if the orchestrator can show one, it becomes major.",
   "fix": "In the pos-None branch, print the blank when the excerpt contains any date (or always), or add the branch to row 3 with its reason.",
   "acceptance_test": "A test with pos None and an excerpt that labels a date asserts the decided result; mutant N2 stays killed."},
  {"severity": "minor", "title": "The allow-list as written is narrower than the code: UB-04 statement period, label connectors, two bill wordings, one heading, and a single labeled date under (d)",
   "evidence": "probe_t207_r2.out 'D5 ub04 statement period | stated | 2026-01-05 | 2026-01-09' (doc names only 'statement covers period'); 'D7 label tail DOS is / DOS was / DOS between / DOS - / DOS # | ambiguous_numeric' (label recognised; doc names colon, spaces, dotted leader); service_date.py:92-93 'date of the run', 'treatment dates?'; :107-108 'from service'; :80 _LBL_END",
   "why_it_matters": "The list is presented as the whole set of ties; a reader cannot tell what else decides a printed date.",
   "fix": "Name the extra connectors, wordings, heading and the UB-04 'statement period', or narrow the code.",
   "acceptance_test": "Each phrase in service_date.py's label regexes appears in row 2, checked by reading the two side by side."},
  {"severity": "minor", "title": "The next/last/prior guard is stated for prose labels; a bill's own 'visit of' wording has none, so 'last visit of 12/20/2025' prints as the service date",
   "evidence": "probe2_t207_r2.out 'E5 bill last visit of 12/20/2025 (unambiguous) | stated | 2025-12-20' and 'next visit of', 'prior visit of' the same; 'E5 bill last DOS 12/20/2025 | not_stated ... non_service_date'; service_date.py:89-93 (_NOT_OTHER_VISIT is applied to _SVC_CORE only); memory/ORCHESTRATOR_DECISIONS.md:95 accepts the bill wordings without the guard; docs/LLM_VS_CODE.md:30",
   "why_it_matters": "It is the same class as the r3 paralegal blocker (another visit's date printed as this charge's). The doc does not say the guard stops at the prose labels.",
   "fix": "Either apply the guard to _SVC_BILL or state in row 2 that the guard covers only DOS, date of service and service date.",
   "acceptance_test": "A test for 'Charge for last visit of 12/20/2025' in a ledger asserts the chosen result."},
  {"severity": "minor", "title": "Two counts in row 3's validation cell overreach: 131 tests (it is 133) and 'rounds 3 and 4' probes (no round 4 review exists)",
   "evidence": "pytest tests/unit/test_t202_r4_encounter.py --collect-only: '133 tests collected'; docs/LLM_VS_CODE.md:31 'test_t202_r4_encounter.py (131 tests; every reviewer probe from rounds 3 and 4 is a fixture)'; tests/unit/test_t202_r4_encounter.py:1 'Every probe from the round 3 paralegal and staff reviews is a fixture here'; ls reviews | grep T-202 lists paralegal, paralegal-r2, paralegal-r3, staff-engineer, -r2, -r3 and no r4",
   "why_it_matters": "The 131 comes from the backend handoff, not a run. The probe claim names a review round that has not been recorded. Same class as r1 F5 (a count the reviewer can refute).",
   "fix": "Say 133 (or drop the count) and 'rounds 1 to 3' (or cite the test file's own sentence).",
   "acceptance_test": "The cell's numbers equal pytest --collect-only and the reviews/ listing."}
 ],
 "whats_right": ["The bound sentence is exact: 1,830 days is read, 1,831 is refused, and a few days past five calendar years is read (probe D1).",
                 "The two ambiguity rules, the encounter-only header date and the record-type classifier behave as written and fail toward the blank (probes D2, D3, E4).",
                 "Row 3's blank, both note forms, the counted-charge exception and the hand-built-dict branch match the code; code is unchanged from 8cb5bd2 to HEAD and evals.letter_check reads value 0 over 25 cases."],
 "questions_for_chris": ["Q1 (F1): Is a labeled service date up to 4 days past five calendar years (1,830-day bound) acceptable to print, or should the bound be calendar-exact?",
                         "Q2 (F5): Should the next/last/prior guard also stop a bill's own 'visit of' wording from tying a date to the line?"]}
```
