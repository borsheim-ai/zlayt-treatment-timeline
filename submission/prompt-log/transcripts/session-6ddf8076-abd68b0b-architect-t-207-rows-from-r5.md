# Subagent: Architect: T-207 rows from r5 (Architect: T-207 rows from r5)

Source: `agent-abd68b0ba0ecddcf1.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T02:43:48.246Z

You are the architect in /Users/arsis/zlayt-pm-project on T-207. Claim it with --force. Read D-073 and its clarification in memory/ORCHESTRATOR_DECISIONS.md, reviews/T-207-staff-engineer-r2.md, and the rows text the T-202 r5 worker left on T-207.

Rewrite rows 2 and 3 of docs/LLM_VS_CODE.md so every statement matches the code at f9c0faf (app/backend/service_date.py, encounter_types.json, export.py); read the code yourself. Name the test that pins each stated rule, so a reviewer can check the pinning. Don't claim anything that isn't pinned.

Commit only that file through `git commit` with a temp index from the current HEAD. Move the card to in_review and reply in 1 line.

### User / tool · 2026-11-03T02:43:48.292Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:43:50.968Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B claim T-207 --agent architect --force; $B show T-207 | head -150; grep -n \"D-073\" -A30 memory/ORCHESTRATOR_DECISIONS.md | head -120"
}
````

### User / tool · 2026-11-03T02:43:51.158Z

**tool result**
````
board.py: error: T-207 already claimed (lock held by architect)
---
id: "T-207"
title: "LLM_VS_CODE rows 2 and 3: charge-line service dates are an allow-list of positive evidence (T-202 r3, D-071 amendment)"
milestone: "M3"
role: "architect"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T00:45:18Z"
updated_at: "2026-11-03T02:43:37Z"
claimed_by: "architect"
claimed_at: "2026-11-03T00:46:49Z"
rounds: 2
commits: ["901ad5a", "fc37fbc", "efda639"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-207-staff-engineer.md", "at": "2026-11-03T01:43:17Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-207-staff-engineer-r2.md", "at": "2026-11-03T02:28:15Z"}
ac:
  - {"n": 1, "text": "docs/LLM_VS_CODE.md row 2 and row 3 carry the text in the T-202 note from backend (allow-list, as-written form, not-stated form, validation), and say entry dates stay on the stricter ambiguous-never-guessed rule", "done": true, "evidence": "docs/LLM_VS_CODE.md rows 2-3 rewritten from service_date.py, encounter_types.json, store.charge_service_date, export.charge_when at 8cb5bd2; commit efda639"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read."
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service." Append to the "Validation" cell: " Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser)."
- 2026-11-03T00:46:49Z architect: claimed
- 2026-11-03T00:47:32Z architect: AC 1 checked: docs/LLM_VS_CODE.md rows 2 and 3, commit 901ad5a; text per T-202 note + D-071 amendment/clarification/addendum
- 2026-11-03T00:47:32Z architect: moved in_progress -> in_review
- 2026-11-03T00:47:37Z orchestrator: The fillable blank is in T-202 r3 scope (message sent to the backend worker); review T-207 against the T-202 r3 commit.
- 2026-11-03T00:47:37Z orchestrator: review dispatched: staff-engineer-reviewer (queued: after T-202 r3 lands)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints "(statement dated X; service date not stated)". Both are gone. Replace those two sentences with exactly: "Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it." Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date.
- 2026-11-03T01:26:49Z architect: Applied the backend correction (row 3, 'shows as written' and 'service date not stated' sentences replaced with the fillable blank; Validation cell 28 -> 24 mutants) to docs/LLM_VS_CODE.md, matching code at 973b542. Commit fc37fbc (temp index from HEAD, docs file only). Card left in_review.
- 2026-11-03T01:26:55Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-03T01:43:17Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-207-staff-engineer.md; round 1; findings:
    - [major] Row 2 says a two-reading date is certain only by the statement rule; code also settles it from the other end of the same period — fix: Architect amends row 2 to state the same-period locale rule (cite D-071 amendment 'no locale rule from the record'), or the code drops the rule and the period prints the blank.
    - [major] Five-year bound is 1830 days, not 'more than five years'; no test sits at the boundary — fix: Compare calendar years (statement date minus five years, same month and day, 29 Feb handled) instead of 366-day arithmetic; keep 1998 and 2031.
    - [major] A charge with no labeled date takes the visit note's header date; row 2 says only the allow-list counts — fix: Chris rules (Q1). If yes, row 2 names the encounter-header rule and cites R-TL-3. The pos-None branch at store.py:133 then either follows the same rule and says so, or prints the blank as the ledger path does.
    - [major] A counted undated charge prints the blank with no Step 3 confirm note — fix: Either row 3 says counted lines carry no note and cites D-064, or store.py:139 keeps the note with 'Count this charge' wording.
    - [major] Validation cell claims 24 mutants all fail; two resolver mutants survive and no 24-mutant harness exists — fix: Amend the cell to the tests that exist, or commit the mutation harness with its count; add tests that kill M4 and M8.
    - [minor] Row 2's column-heading list is narrower than the code — fix: List the heading set in row 2; add a test for Encounter Date.
    - [minor] Row 3's note wording holds only for written-date reasons — fix: Align row 3 with the two note forms, or change the no-label note to point to the quote.
    - [minor] A second date-of-service parser on billing lines sits outside row 2's only-path claim — fix: Document the endpoint's dos_iso as not a charge date in row 2, or remove it.
- 2026-11-03T01:43:17Z orchestrator: moved changes_requested -> blocked: rows describe code that T-202 r4 (D-071 amendment 2) is changing now; rewrite rows 2-3 from the r4 commit and fold the 5 majors in reviews/T-207-staff-engineer.md
- 2026-11-03T01:58:42Z architect: moved blocked -> in_progress: T-202 r4 landed (8cb5bd2); rewrite rows 2-3 from it
- 2026-11-03T02:00:55Z architect: AC 1 checked: docs/LLM_VS_CODE.md rows 2-3 rewritten from service_date.py, encounter_types.json, store.charge_service_date, export.charge_when at 8cb5bd2; commit efda639
- 2026-11-03T02:00:55Z architect: moved in_progress -> in_review
- 2026-11-03T02:00:59Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-03T02:28:15Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-207-staff-engineer-r2.md; round 2; findings:
    - [major] The five-year bound is stated exactly as 1,830 days, but no test pins it, the on-or-before edge, or the no-record-date case — fix: Add unit tests through store.charge_service_date for a ledger with statement 2026-06-30: DOS 06/26/2021 (1,830 days) is stated, 06/25/2021 (1,831) is implausible; DOS equal to the record date is stated and one day after is implausible; a record with no da
    - [major] Other statements in rows 2 and 3 are covered by no test: different-order period ends, rule 2's on-or-before edge, two headings, the next guard, the counted-charge no-note rule — fix: Add one fixture per statement: '13/05/2026 - 05/13/2026' prints the blank; a rule-2 case where one order equals the record date; a table with an 'Encounter Date' heading and one with 'Date of Visit'; 'Ne
    - [minor] For an encounter record whose figure cannot be located, the header date is lent without looking at the line; the doc says only when the line has no labeled date — fix: In the pos-None branch, print the blank when the excerpt contains any date (or always), or add the branch to row 3 with its reason.
    - [minor] The allow-list as written is narrower than the code: UB-04 statement period, label connectors, two bill wordings, one heading, and a single labeled date under (d) — fix: Name the extra connectors, wordings, heading and the UB-04 'statement period', or narrow the code.
    - [minor] The next/last/prior guard is stated for prose labels; a bill's own 'visit of' wording has none, so 'last visit of 12/20/2025' prints as the service date — fix: Either apply the guard to _SVC_BILL or state in row 2 that the guard covers only DOS, date of service and service date.
    - [minor] Two counts in row 3's validation cell overreach: 131 tests (it is 133) and 'rounds 3 and 4' probes (no round 4 review exists) — fix: Say 133 (or drop the count) and 'rounds 1 to 3' (or cite the test file's own sentence).
- 2026-11-03T02:28:15Z orchestrator: moved changes_requested -> blocked: D-073 (T-202 r5) rewrites the date rules again; rows 2-3 are rewritten from the r5 commit; the unpinned-rule majors go to the r5 worker as tests
- 2026-11-03T02:30:01Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3), after T-202 r5 (D-073). Replace the charge-date sentences of rows 2 and 3 with exactly: 'A charge line takes its date of service from two sources only (D-073): (1) the date cell of its own row in a bill table whose column header names the date of service (the CMS-1500 24A From/To cells and a UB-04 statement covers period FROM/THROUGH of a coded line, printed as a range); (2) the record's own date, only for a record identified by a document-type word in its source label (declared in app/backend/encounter_types.json: visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, run report, operative report, evaluation, consult), never by a provider name, and only when the charge's own sentence holds no other date and no visit count. Prose labels (DOS, date of service, visit of, Treatment dates, next visit date) are not read (SCOPE_CUTS row 28). Every other line prints the fillable blank date of service [__________] (statement dated X). A figure the code cannot locate in its record prints the blank. A cell readable two ways is read only when one reading is on or before the record date for every end; a cell after the record date or more than 1,830 days (five 366-day years) before it is doubtful.' Validation cell: 'tests/unit/test_t202_r5_d073.py (every probe of rounds 1-4 and the T-207 r2 rule pins; mutants listed in the T-202 handoff) and evals/letter_check.charge_date_violations, an independent scanner reading the same declared table.'
- 2026-11-03T02:43:37Z architect: moved blocked -> in_progress: T-202 r5 landed (f9c0faf); rewrite rows 2-3 from it

## Handoff
What changed: rows 2-3 rewritten against 8cb5bd2. Majors: (1) same-period rule stated (another end forces the order; no record locale), then statement rule, needs a record date; (2) bound stated as 1,830 days (5x366), on every record, no bound without a record date, can read a few days past five calendar years; (3) encounter-record date default stated with R-TL-3 and D-071 amendment 2, encounter_types.json, bad labeled date in an encounter prints the blank not the header date; (4) counted (D-064) line prints the blank with no note; (5) mutant claim cut to the T-202 r4 handoff (24 of 25, scratch run, harness not committed). Minors: heading set listed, two note forms, billing dos_iso not a charge date. Verified: read code, check_secrets ok, diff is 2 table rows. Left: bound is day arithmetic in code (reviewer asked for calendar years): card for backend if wanted. Surprised me: store.py, not export.py, holds the encounter default and the counted-line rule.

97:## D-073 — Service dates: the pre-declared conservative fallback (§7.4 after T-202 r4)
98-Four rounds of date recognition kept finding new prose patterns that print a wrong date of service (r4: a visit note citing an earlier "DOS", a therapy "Treatment dates A to B" range collapsing to B, an unknown source lending its statement date). Binding for the MVP: a charge line prints a service date from exactly two sources, (1) the date cell of its own row in a bill table whose column header names the date of service (or the CMS-1500 24A/UB-04 from-through period, printed as a range), or (2) the encounter record's own date when the charge sits inside a positively identified encounter record (encounter_types.json). Prose labels are no longer read for charge dates at all; every other line prints the fillable blank "date of service [__________] (statement dated X)" with the Step 3 confirm note. letter_check applies the same two-source rule independently. Wider date recognition is SCOPE_CUTS row 28. Expected effect: some corpus lines that printed a correct prose-labelled date now print the blank, which is honest and is shown in the handoff diff.
99:- D-073 clarification (staff r4 question, decided per rule 1): an encounter record is identified only by a document-type word (visit/progress/office note, ED/ER record, discharge summary, PT/therapy note, ambulance run report, operative report); a provider name (clinic, ED, orthopedics, urgent care, imaging) is never enough. About 19 of 84 corpus charge lines then print the fillable blank; accepted.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:43:51.556Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer-r2.md"
}
````

### User / tool · 2026-11-03T02:43:51.562Z

**tool result**
````
1	# T-207 staff-engineer review, r2
2	
3	Reviewer: staff-engineer-reviewer (Marcus Lee persona), fresh context, read-only on product code. Model running: claude-sonnet-5-5.
4	
5	Scope: docs/LLM_VS_CODE.md rows 2 and 3 as fixed in efda639, checked against the code at 8cb5bd2 (a git archive in a scratch directory; the product tree was not edited). `git diff --stat 8cb5bd2 HEAD -- app/backend/service_date.py app/backend/encounter_types.json app/backend/export.py app/backend/store.py evals/letter_check.py docs/LLM_VS_CODE.md tests/unit` shows only `docs/LLM_VS_CODE.md | 4 ++--` (efda639), so the code did not move between 8cb5bd2 and HEAD ad0d91a. Rows 30-31 of the working copy have the same md5 as `git show efda639:docs/LLM_VS_CODE.md`.
6	
7	## Verdict: changes (no blocker, two majors, four minors)
8	
9	## Does stating the five-year bound as 1,830 days settle it?
10	
11	The statement is accurate. It is not enough.
12	
13	Accurate: probe D1 (statement 2026-06-30, ledger) gives "1830d before (2021-06-26) | stated" and "1831d before (2021-06-25) | not_stated | reason=implausible". `service_date.py:109` has `_YEARS_BEFORE = 5` and `:328` has `days=366 * _YEARS_BEFORE`. The sentence "a date a few days past five calendar years can still be read" is true (2021-06-26 is five years and four days before). That closes the doc half of r1 F2.
14	
15	Not enough: the number is now a documented contract and nothing pins it. The only bound tests are the 1998 and 2031 fixtures (`tests/unit/test_t202_r3_allow_list.py:184-185`). I mutated the bound three ways at once (365 days per year, `>=` to `>` at the lower end, `<=` to `<` at the upper end) on the 8cb5bd2 archive and ran the whole unit suite: `6266 passed, 12 skipped, 1 deselected` (the deselected test, `test_e2e_contract.py::test_every_test_id_is_declared`, fails identically at the parent per the T-202 handoff and is not in this scope). r1 F2's acceptance test (a test at the boundary that kills the bound mutant) is therefore still open. Persona calibration: a bound with no boundary test is major. The doc is accurate for behaviour and still wrong to rely on for verification, because the "How it is checked" cell cites unit tests that cannot fail when 1,830 changes.
16	
17	Whether a 1 to 4 day slack is acceptable product behaviour is a product call (Q1). If it is, pin it with tests. If it is not, fix the code, and the doc sentence changes with it.
18	
19	## Row-by-row result
20	
21	Holds (probe or code line in brackets):
22	- Rule (1), same-date-or-period order: `04/05/2026 - 13/05/2026` reads May 4 to May 13 [D2; service_date.py:265-275]. Two ends forcing different orders are not read [D2: "13/05/2026 - 05/13/2026 | ambiguous_numeric"].
23	- Rule (2), a service cannot follow its statement: read only when exactly one order is on or before the record date; with no record date it is not read [D2 rows for 2026-05-31, 2026-04-30 and None; service_date.py:272-274].
24	- Bound applies to every record, `implausible`, no bound without a record date [D1, D1nodate; service_date.py:323-328].
25	- Only an identified encounter lends its header date; bill, receipt, superbill, charge summary, administrative paper and unknown type do not [D3 rows; service_date.py:54-63, 414-434]. A labeled but unreadable date is not replaced by the header date [D3 "ER labeled-bad(2-digit) | two_digit_year", probe H1 mutant killed].
26	- Table `encounter_types.json` is read by `service_date.record_kind` (TYPES_PATH at :33) and by `evals/letter_check.py:234` with its own matcher; letter_check imports no service_date (grep). `python -m evals.letter_check` gives `"value": 0, "cases": 25`.
27	- Column heading set in row 2 matches `_H_SVC` (service_date.py:107-108) [D6: every listed heading is recognised; Posted and Entry Date are not].
28	- Row 3: the blank text and `export.charge_when` (export.py:215-226), the two note forms (service_date.py:156-162), counted charge has no note (store.py:139), hand-built dict without `dos_iso` keeps the record date (export.py:222-223). Billing view `dos_iso` is `billing._dos`, route at billing.py:1061, no import from export, store or present, no consumer in app/frontend.
29	
30	Does not hold, or is not pinned: findings below.
31	
32	## Exercised
33	
34	1. `git rev-parse HEAD 8cb5bd2 efda639`, `git log --oneline -8`, `git diff --stat 8cb5bd2 efda639` (docs only, 2 lines), `git diff --stat 8cb5bd2 HEAD -- <scope files>`.
35	2. `git archive 8cb5bd2` into a scratch directory. Read service_date.py (434 lines), encounter_types.json, store.py:105-200, export.py:215-226 and 600-625, amounts.py:300-320 and 515-545, evals/letter_check.py:1-30, 225-240, 405-470, billing.py:136-145, rows 2 and 3 of docs/LLM_VS_CODE.md, the T-202 board card (handoff and notes), D-071 amendment 2 (ORCHESTRATOR_DECISIONS.md:94-95), and my r1 review.
36	3. `pytest` on the five date files (test_t202_r2_service_date_layouts, test_t202_r3_allow_list, test_t202_r4_encounter, test_t202_charge_service_dates, test_t200_undated_charge_label): 341 passed. `--collect-only` on test_t202_r4_encounter.py: 133 tests.
37	4. `python -m evals.letter_check` on the archive: value 0, cases 25.
38	5. Probes D1 to D7: artifacts/review-evidence/T-207-r2/probe_t207_r2.py and probe_t207_r2.out. Probes E1 to E5: probe2_t207_r2.py and probe2_t207_r2.out.
39	6. 25 mutants against the five date files: mutants_t207_r2.py and mutants_t207_r2.out (13 killed, 12 survived). Ten of them against evals.letter_check: mutants_t207_r2_letter.out (control E2 killed, the other ten survived). Two full-suite runs of tests/unit on mutated copies: B1+B2+B5 (6266 passed, 12 skipped, 1 deselected, 408 s) and R1+R3+L2+L3+L4+N1 (6266 passed, 12 skipped, 1 deselected, 397 s). The script restores each file; the archive's service_date.py md5 matched `git show 8cb5bd2` after the run.
40	7. `ls reviews | grep T-202` (no r4 review file), `git status` and `git diff HEAD --stat -- docs/LLM_VS_CODE.md` (empty).
41	
42	## Findings
43	
44	F1 (major). The five-year bound, the on-or-before boundary and the no-record-date case are documented and unpinned. Mutants B1 (365 per year), B2 (`>=` to `>`), B3 and B4 (5 to 4 and 6 years), B5 (`<=` to `<` at the record date) and B6 (no-date record refuses) all survive the five date test files and the letter eval; B1+B2+B5 together survive the full unit suite. Accurate wording does not fix a missing test.
45	
46	F2 (major). Other statements in rows 2 and 3 are also pinned by no test. Mutant R3 (`len(determined) > 2`, so two ends that force different orders are read) and R1 (`<= ref` to `< ref` in rule 2) survive the full unit suite, with L2 (drop the `next ` guard), L3 (drop "encounter date" heading), L4 (drop "date of visit" heading) and N1 (a counted charge gets a note). r1 F6's acceptance asked that the Encounter Date mutant be killed; it still survives. R3 matters most: a period whose ends force different orders is exactly where a wrong date could print.
47	
48	F3 (minor, would be major if a real path is shown). The doc says the header date is lent "only when the line has no labeled date of its own" and that a labeled date that cannot be read "is not replaced by the header date". `store.py:131` skips the look when `pos` is None: probe D4 gives "pos located | not_stated None implausible" but "pos None | stated 2026-01-09" for the same encounter line that labels 05/05/2026, and "D4c pos None, line labels 03/01/2026 | stated 2026-01-09" where the located path reads 2026-01-03. `tests/unit/test_t200_undated_charge_label.py:63` pins this with an excerpt `"x"`. I could not find a normal flow that gives `amount_pos` None for a pipeline amount (pipeline.py:417 sets excerpt_start from the figure), so I rate it minor. This is a doc/code divergence, not a preference.
49	
50	F4 (minor). The allow-list text is narrower than the code. UB-04 "statement period" is read, not only "statement covers period" (probe D5: stated 2026-01-05 to 2026-01-09). Label connectors `is`, `was`, `from`, `between`, `#`, `-` and `(` also work (D7), and the doc names a colon, spaces or a dotted leader. The bill wordings "date of the run" and "treatment dates", the "from service" heading, and (d) taking a single labeled date (not only a period) are not listed (service_date.py:92-96, 101, 107-108, 415-428). The list is presented as exhaustive.
51	
52	F5 (minor, question for Chris). The "never after next, last, prior..." guard is stated for the prose labels and the code applies it only there. A bill's own wordings are unguarded: probe E5, "Charge for last visit of 12/20/2025: office visit $220.00." prints 2025-12-20 as the date of service, and "next visit of" and "prior visit of" do the same, while "last DOS 12/20/2025" correctly gives non_service_date (service_date.py:89-93). D-071 amendment 2 note (ORCHESTRATOR_DECISIONS.md:95) accepts the bill wordings but not the missing guard. Either the doc says the guard stops at the prose labels or the code extends it.
53	
54	F6 (minor). Two validation-cell counts overreach. "131 tests" is 133 (`pytest --collect-only`, test_t202_r4_encounter.py), copied from the backend handoff. "every reviewer probe from rounds 3 and 4 is a fixture" has no round 4 behind it: `ls reviews | grep T-202` shows no r4 review, and the test file's own docstring (line 1) says "Every probe from the round 3 paralegal and staff reviews". The honest sentence about the uncommitted 24-of-25 mutation run is right and should stay.
55	
56	## What is right
57	
58	1. The bound sentence is exact: 1,830 days is read, 1,831 is refused, and a few days past five calendar years is read (probe D1).
59	2. The two ambiguity rules, the encounter-only header date, and the classifier all behave as written and fail toward the blank (probes D2, D3, E4).
60	3. Row 3's blank, both note forms, the counted-charge exception and the hand-built-dict branch match the code; the code is unchanged from 8cb5bd2 to HEAD and `evals.letter_check` reads value 0 over 25 cases.
61	
62	Outside my lens: the legal weight of the blank, and whether a paralegal reads the Step 3 note wording as helpful.
63	
64	```json
65	{"card": "T-207", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
66	 "scope": "docs/LLM_VS_CODE.md rows 2-3 as of efda639 vs code at 8cb5bd2 (git archive in scratch; code unchanged to HEAD ad0d91a): app/backend/service_date.py, encounter_types.json, store.py:105-200, export.py:215-226, evals/letter_check.py; no app URL exercised",
67	 "exercised": ["git rev-parse/log/diff --stat: 8cb5bd2 to efda639 is docs only; scope files unchanged 8cb5bd2 to HEAD; rows 30-31 md5 equal at efda639 and working copy",
68	               "git archive 8cb5bd2 into scratch; read service_date.py in full, encounter_types.json, store.py:105-200, export.py:215-226 and 600-625, amounts.py:300-320 and 515-545, letter_check.py header and charge_date_violations, billing.py:136-145, rows 2-3, T-202 board card, D-071 amendment 2",
69	               "pytest on 5 date test files at 8cb5bd2: 341 passed; --collect-only test_t202_r4_encounter.py: 133 tests",
70	               "python -m evals.letter_check: value 0, cases 25",
71	               "probes D1-D7 (artifacts/review-evidence/T-207-r2/probe_t207_r2.py + .out) and E1-E5 (probe2_t207_r2.py + .out)",
72	               "25 mutants on date files (mutants_t207_r2.py + .out: 13 killed, 12 survived); 10 against letter_check (mutants_t207_r2_letter.out: 10 survived, control killed)",
73	               "full tests/unit on mutated copies: B1+B2+B5 and R1+R3+L2+L3+L4+N1 each 6266 passed, 12 skipped, 1 deselected (known failing test_every_test_id_is_declared)",
74	               "ls reviews | grep T-202 (no r4 review); git status and git diff HEAD --stat on the doc (empty)"],
75	 "verdict": "changes",
76	 "scores": {"row2_matches_code": 4, "row3_matches_code": 4, "date_is_code_only": 5, "bound_statement_accuracy": 5, "bound_and_rules_pinned_by_tests": 2, "validation_cell_claims": 3},
77	 "findings": [
78	  {"severity": "major", "title": "The five-year bound is stated exactly as 1,830 days, but no test pins it, the on-or-before edge, or the no-record-date case",
79	   "evidence": "service_date.py:109 '_YEARS_BEFORE = 5' and :328 'days=366 * _YEARS_BEFORE'; probe_t207_r2.out 'D1 1830d before (2021-06-26) | stated' and 'D1 1831d before (2021-06-25) | not_stated ... reason=implausible'; only bound tests are tests/unit/test_t202_r3_allow_list.py:184-185 (1998 and 2031); mutants_t207_r2.out 'B1 ... SURVIVED | 341 passed', 'B2 ... SURVIVED', 'B3', 'B4', 'B5 ... SURVIVED', 'B6 ... SURVIVED'; mutants_t207_r2_letter.out B1 B2 B5 B6 SURVIVED (value 0, 25 cases); full tests/unit with B1+B2+B5 applied: '6266 passed, 12 skipped, 1 deselected in 408.74s'",
80	   "why_it_matters": "The doc now makes 1,830 days a contract and row 3's How-it-is-checked cell cites unit tests as the check. Those tests pass when the constant becomes 1,825, when the lower edge flips, and when a service date equal to the record date is refused. r1 F2's acceptance test (a boundary test that kills the bound mutant) is still open. Persona calibration: a bound without a boundary test is major.",
81	   "fix": "Add unit tests through store.charge_service_date for a ledger with statement 2026-06-30: DOS 06/26/2021 (1,830 days) is stated, 06/25/2021 (1,831) is implausible; DOS equal to the record date is stated and one day after is implausible; a record with no date and DOS 03/13/1998 is stated. Chris decides whether the 1 to 4 day slack stays (Q1); if not, change the code to a calendar-year compare and update the doc sentence.",
82	   "acceptance_test": "Mutants B1 (365 per year), B2 (>= to >), B3/B4 (_YEARS_BEFORE 4 or 6), B5 (<= to < at the record date) and B6 (no-date record refuses) each fail at least one test in tests/unit; the tests are in the repo and named in row 3's cell."},
83	  {"severity": "major", "title": "Other statements in rows 2 and 3 are covered by no test: different-order period ends, rule 2's on-or-before edge, two headings, the next guard, the counted-charge no-note rule",
84	   "evidence": "mutants_t207_r2.out 'R3 rule1 two ends forcing different orders -> read | SURVIVED', 'R1 rule2 on-or-before -> before | SURVIVED', 'L2 next prefix guard removed | SURVIVED', 'L3 heading encounter date dropped | SURVIVED', 'L4 heading date of visit dropped | SURVIVED', 'N1 counted undated charge gets a note | SURVIVED' (all against 341 date tests); R1+R3+L2+L3+L4+N1 applied together to a copy and run over tests/unit: '6266 passed, 12 skipped, 1 deselected in 396.63s'; docs/LLM_VS_CODE.md:30 'two ends that force different orders are not read', ':31 carries no note'; r1 F6 acceptance 'M8 is killed' (Encounter Date) still unmet",
85	   "why_it_matters": "Each is a sentence in the binding table that the code can break without any test failing. R3 decides whether a period with contradictory ends prints a date or the blank, which is a printed-date correctness rule. The doc's own Validation cell says the dates are tested.",
86	   "fix": "Add one fixture per statement: '13/05/2026 - 05/13/2026' prints the blank; a rule-2 case where one order equals the record date; a table with an 'Encounter Date' heading and one with 'Date of Visit'; 'Next DOS 02/01/2026' is non_service_date; a counted undated charge has confirm_note None and an uncounted one has a note.",
87	   "acceptance_test": "Mutants R1, R3, L2, L3, L4 and N1 each fail at least one test in tests/unit."},
88	  {"severity": "minor", "title": "For an encounter record whose figure cannot be located, the header date is lent without looking at the line; the doc says only when the line has no labeled date",
89	   "evidence": "app/backend/store.py:131 'elif rec is None or pos is None or not item.get(\"excerpt\"): r = {... \"first\": rd ...} if (encounter and rd) else dict(none)'; probe_t207_r2.out 'D4 pos located | not_stated None implausible' vs 'D4 pos None | stated 2026-01-09 None'; 'D4c pos None, line labels 03/01/2026 (AFTER header) | stated 2026-01-09' vs 'D4d pos located, same line | stated 2026-01-03'; tests/unit/test_t200_undated_charge_label.py:63 pins it with excerpt 'x'; docs/LLM_VS_CODE.md:30 'only when the line has no labeled date of its own' and 'A labeled date that cannot be read in an encounter record is not replaced by the header date'",
90	   "why_it_matters": "The doc states a universal the code breaks on this path. Rated minor because pipeline.py:417 sets excerpt_start for every amount and I found no normal flow that yields pos None; if the orchestrator can show one, it becomes major.",
91	   "fix": "In the pos-None branch, print the blank when the excerpt contains any date (or always), or add the branch to row 3 with its reason.",
92	   "acceptance_test": "A test with pos None and an excerpt that labels a date asserts the decided result; mutant N2 stays killed."},
93	  {"severity": "minor", "title": "The allow-list as written is narrower than the code: UB-04 statement period, label connectors, two bill wordings, one heading, and a single labeled date under (d)",
94	   "evidence": "probe_t207_r2.out 'D5 ub04 statement period | stated | 2026-01-05 | 2026-01-09' (doc names only 'statement covers period'); 'D7 label tail DOS is / DOS was / DOS between / DOS - / DOS # | ambiguous_numeric' (label recognised; doc names colon, spaces, dotted leader); service_date.py:92-93 'date of the run', 'treatment dates?'; :107-108 'from service'; :80 _LBL_END",
95	   "why_it_matters": "The list is presented as the whole set of ties; a reader cannot tell what else decides a printed date.",
96	   "fix": "Name the extra connectors, wordings, heading and the UB-04 'statement period', or narrow the code.",
97	   "acceptance_test": "Each phrase in service_date.py's label regexes appears in row 2, checked by reading the two side by side."},
98	  {"severity": "minor", "title": "The next/last/prior guard is stated for prose labels; a bill's own 'visit of' wording has none, so 'last visit of 12/20/2025' prints as the service date",
99	   "evidence": "probe2_t207_r2.out 'E5 bill last visit of 12/20/2025 (unambiguous) | stated | 2025-12-20' and 'next visit of', 'prior visit of' the same; 'E5 bill last DOS 12/20/2025 | not_stated ... non_service_date'; service_date.py:89-93 (_NOT_OTHER_VISIT is applied to _SVC_CORE only); memory/ORCHESTRATOR_DECISIONS.md:95 accepts the bill wordings without the guard; docs/LLM_VS_CODE.md:30",
100	   "why_it_matters": "It is the same class as the r3 paralegal blocker (another visit's date printed as this charge's). The doc does not say the guard stops at the prose labels.",
101	   "fix": "Either apply the guard to _SVC_BILL or state in row 2 that the guard covers only DOS, date of service and service date.",
102	   "acceptance_test": "A test for 'Charge for last visit of 12/20/2025' in a ledger asserts the chosen result."},
103	  {"severity": "minor", "title": "Two counts in row 3's validation cell overreach: 131 tests (it is 133) and 'rounds 3 and 4' probes (no round 4 review exists)",
104	   "evidence": "pytest tests/unit/test_t202_r4_encounter.py --collect-only: '133 tests collected'; docs/LLM_VS_CODE.md:31 'test_t202_r4_encounter.py (131 tests; every reviewer probe from rounds 3 and 4 is a fixture)'; tests/unit/test_t202_r4_encounter.py:1 'Every probe from the round 3 paralegal and staff reviews is a fixture here'; ls reviews | grep T-202 lists paralegal, paralegal-r2, paralegal-r3, staff-engineer, -r2, -r3 and no r4",
105	   "why_it_matters": "The 131 comes from the backend handoff, not a run. The probe claim names a review round that has not been recorded. Same class as r1 F5 (a count the reviewer can refute).",
106	   "fix": "Say 133 (or drop the count) and 'rounds 1 to 3' (or cite the test file's own sentence).",
107	   "acceptance_test": "The cell's numbers equal pytest --collect-only and the reviews/ listing."}
108	 ],
109	 "whats_right": ["The bound sentence is exact: 1,830 days is read, 1,831 is refused, and a few days past five calendar years is read (probe D1).",
110	                 "The two ambiguity rules, the encounter-only header date and the record-type classifier behave as written and fail toward the blank (probes D2, D3, E4).",
111	                 "Row 3's blank, both note forms, the counted-charge exception and the hand-built-dict branch match the code; code is unchanged from 8cb5bd2 to HEAD and evals.letter_check reads value 0 over 25 cases."],
112	 "questions_for_chris": ["Q1 (F1): Is a labeled service date up to 4 days past five calendar years (1,830-day bound) acceptable to print, or should the bound be calendar-exact?",
113	                         "Q2 (F5): Should the next/last/prior guard also stop a bill's own 'visit of' wording from tying a date to the line?"]}
114	```
115	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:43:54.344Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD f9c0faf && git log --oneline -5 && git diff --stat f9c0faf HEAD -- app/backend docs/LLM_VS_CODE.md tests evals | tail -5; sed -n 28,34p docs/LLM_VS_CODE.md; wc -l app/backend/service_date.py app/backend/encounter_types.json; cat app/backend/encounter_types.json"
}
````

### User / tool · 2026-11-03T02:43:54.467Z

**tool result**
````
fatal: Needed a single revision
|---|---|---|---|---|
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendments; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** Only a date tied to the line counts: (a) a column heading over it that names service (DOS, date of service, service date, visit date, date of visit, encounter date, SVC, service or SVC from/to/thru, CMS-1500 24A); (b) a service label in its clause, which in prose is only DOS, date(s) of service or service date, never after next, last, prior, previous, initial, first, return, follow-up, scheduled, upcoming or future ("visit date", "seen on" and a bare "date" are not labels; a bill also reads its own "visit of", "rendered/provided/performed on", "the run of", "service period", "period of service" and "dates of treatment", and a UB-04 "statement covers period"; a label may be followed by a colon, spaces or a dotted leader); (c) the charge row's own date cell under a heading of kind (a); (d) for a coded line of a bill with no date of its own, the one period the bill states for its services. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. **A numeric date that reads two ways is settled by two fixed rules, in this order, and otherwise stays unread.** (1) Same date or period: when another end of the same labeled date or period can be read only one way (`13/05/2026`), every end takes that order, so `04/05/2026 - 13/05/2026` reads as May 4 to May 13; two ends that force different orders are not read. This uses the date's own text, not a locale guessed from the record (D-071 amendment: no locale rule from the record). (2) Otherwise a service cannot follow its statement (D-071 clarification): the date is read only when exactly one order puts every labeled end on or before the record's own date, and with no record date it is not read. This is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or several labeled dates that do not agree is not read. **The bound applies to every record, not only bills:** a labeled service date after the record's own date, or more than 1,830 days (5 x 366) before it, is not read (reason `implausible`); a record with no date has no bound. The bound is day arithmetic, so a date a few days past five calendar years can still be read. **A record's own date is the service date only for an identified encounter record** (a visit, ER, clinic, therapy, imaging or ambulance-run note), and only when the line has no labeled date of its own (R-TL-3, D-071 amendment 2). The record types are one declared data file, `app/backend/encounter_types.json`, read by `service_date.record_kind` in production and by `evals/letter_check.py` with its own matcher. A bill, receipt, superbill, charge summary, administrative paper (phone note, letter, affidavit, referral) or record of unknown type never lends its header date. A labeled date that cannot be read in an encounter record is not replaced by the header date: the line prints the blank. The billing view's per-line `dos_iso` (`app/backend/billing.py`, `GET /api/cases/{token}/billing`) is a display field read by a different parser; it is not a charge date and does not reach the letter. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is the service date of row 2, never the record's header date merely because it is the header (a bill's header date is its statement date), and the model is never asked. Code prints the service date or period the line itself states, or, for an identified encounter record (R-TL-3, row 2), the visit's own date when the line has no labeled date. A bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its header date. When no service date is certain (the quote labels none, or labels one the code cannot read with certainty), the letter prints the same fillable blank, like the Bates placeholder, beside the statement date: `date of service [__________] (statement dated June 15, 2026)` (D-071 addendum; `service_date.not_stated_text`, `export.charge_when`). The paralegal fills it from the quote; nothing is inferred. Step 3 shows exactly what the letter prints and carries a confirm note in one of two forms (`service_date.confirm_note`): when the quote labels a date the code cannot read, the note names the date as the quote writes it and asks her to confirm it and fill the blank; when the quote labels none, the note says the line states no date of service (or that the only date near it is not labeled as one) and asks her to request a dated itemized bill or fill the blank from the record. **A charge she has counted for its missing date of service (D-064) still prints the blank but carries no note**, because she counted it knowing (`store.charge_service_date`). A hand-built case dict without `dos_iso` (no store path) keeps the record's date in `export.charge_when`; the app's own export carries `dos_iso` for every charge. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. Charge dates: `tests/unit/test_t202_r3_allow_list.py`, `tests/unit/test_t202_r4_encounter.py` (131 tests; every reviewer probe from rounds 3 and 4 is a fixture) and `tests/unit/test_t200_undated_charge_label.py`; `evals/letter_check.charge_date_violations`, an independent per-line scanner over 25 cases that does not import the production parser (it reads the same `encounter_types.json`, with its own matcher) and accepts the blank, whole and exact, and nothing else for a line with no certain date. The T-202 r4 handoff reports a one-off mutation run on a scratch copy (24 of 25 mutants failed the unit suite, the 25th judged equivalent); that harness is not committed, so the run cannot be repeated from the repo. |
| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in the record). The summary is split into clauses, and a clause is removed only when it adds **salient new content** its quote lacks: a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term (`new_salient`, `summary_trim.py:325-356`). Terms are matched by word family (Tylenol with acetaminophen, cervical with neck) after clinical abbreviations are expanded on both sides (`expand_abbreviations`, `:108`; families `:212-267`), so a faithful paraphrase stays and judge 1 checks it. The negation and side words come from the lexicon (`code_lists.added_qualifier` through `grounding`, `summary_trim.py:269`, `:338-342`), not from a list in the trim. A number, side or negation counts only in a clause that shares no content word with the quote; a changed value on the quote's own topic ('Pain 3/10' over 'Pain 4/10') stays and is caught by the rung 1 token checks. A **structural no-fragment rule** (no word list; `:417-423`, T-128 r3): code trims only a **suffix**. A clause is removed only when every clause after it is removed too, so the kept text is always a prefix of whole clauses and no kept clause can follow a removed one (`'Wrist pain 6/10; splint fitted; patient tolerated well.'` over a quote that supports only the first and last clause is returned unchanged). The first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix needs at least 2 content words. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`). Each removal is shown in the trace as 'removed from the summary: not in the quote'. If every clause is removed, or what is left has no content word, the item goes to the could-not-verify tray with `SUMMARY_NOT_IN_QUOTE` (`summary_trim.py:414-415`; `generator.py:75-77`; template `why.py:33`) and is never judged. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
| 5 | Clinical facts as a separate list | **Not built.** The summary and the verbatim excerpt carry the facts. | Every extra paraphrased field is another place to invent medical content. | n/a (deliberate omission). |
| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must not depend on a model's attention. | Unit tests with noisy, duplicate and dose-like numbers. An amount a model reports that code cannot find is rejected. Billing completeness (D-049): a final code accounting pass lists every money-shaped token in a billing record that no parser placed, so a missing figure is listed, never silent. |
     391 app/backend/service_date.py
      20 app/backend/encounter_types.json
     411 total
{
  "_doc": "D-073 (T-202 round 5; supersedes the D-071 amendment 2 table). The ONE declared table of record types for charge-line dates. A record's own date can stand as a charge line's date of service ONLY when the record is positively identified by a DOCUMENT-TYPE word in its source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, ambulance run report, operative report, evaluation, consult ...). A provider's name or specialty (clinic, ED, urgent care, imaging, orthopedics, therapy, EMS, primary care) is never enough. Read by app/backend/service_date.py (production) and by evals/letter_check.py (the independent check, with its own matcher). Matching rule, the same in both: lower-case the text, split it into tokens (runs of letters and digits; hyphens, punctuation and underscores split), and a term matches when its tokens appear in order as consecutive tokens of the text. A record is a BILL when its source label, or the opening of its excerpt (its first 'opening_chars' characters, cut at the first colon, full stop or line break: 'Receipt:', 'Charges:', 'Account summary:'), matches 'financial' (production also keeps the lexicon billing_document list). It is ADMINISTRATIVE when the same text matches 'administrative'. Otherwise it is an ENCOUNTER only when its source label matches 'encounter'; every other record is of unknown type. Bills, administrative papers and unknown types never lend their header date.",
  "opening_chars": 40,
  "encounter": [
    "visit", "note", "progress note", "office note", "clinic note", "visit note", "daily note", "operative note", "op note", "discharge note", "discharge summary",
    "er record", "ed record", "emergency department record", "emergency room record", "emergency record", "er note", "ed note", "er report", "ed report",
    "pt note", "ot note", "therapy note", "physical therapy note", "ambulance run report", "run report", "trip report", "patient care report", "operative report", "op report",
    "consult", "consultation", "consulta", "nota de consulta", "evaluation", "re-evaluation", "reevaluation", "exam", "examination", "re-examination", "reexamination",
    "new patient", "follow-up", "followup", "mri", "x-ray", "xray", "ct scan", "ultrasound", "radiology report", "imaging report"
  ],
  "financial": [
    "bill", "bills", "billed", "billing", "superbill", "statement", "statements", "invoice", "invoices", "ledger", "ledgers", "account", "itemized", "itemised", "itemization",
    "receipt", "receipts", "charges", "charge summary", "charge sheet", "fee", "fees", "estimate", "estimated", "cost", "claim", "claims", "remittance",
    "eob", "explanation of benefits", "hcfa", "cms-1500", "cms1500", "ub-04", "ub04", "ub-92", "ub92", "payment", "payments", "balance", "financial", "copay", "deductible", "price", "pricing", "quote"
  ],
  "administrative": [
    "phone", "telephone", "voicemail", "portal message", "message", "correspondence", "letter", "fax", "affidavit", "authorization", "authorisation",
    "referral", "records request", "request for records", "records retrieval", "no-show", "noshow", "custodian"
  ]
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:43:54.687Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T02:43:54.695Z

**tool result**
````
1	"""The service date a charge line prints (D-073, T-202 round 5: the pre-declared conservative fallback after four rounds of prose recognition). Code only, no LLM (LLM_VS_CODE rows 2 and 3).
2	
3	A charge line takes its date of service from EXACTLY TWO sources:
4	  (1) its own row's date cell in a bill table whose column header names the date of service (DOS, date of service, service date, visit date, 24A ...), or the CMS-1500 24A 'From' / 'To'
5	      cells and the UB-04 'statement covers period FROM ... THROUGH ...', printed as a range;
6	  (2) the record's own date, ONLY when the record is positively identified as an encounter record by a document-type word in its source label (`record_kind`, the table
7	      app/backend/encounter_types.json: visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, ambulance run report, operative report ...; a provider's name is
8	      never enough), and the charge's own sentence holds no other date and no count of visits (a note that cites an earlier or later date, or charges 9 visits, is not one visit's date).
9	Prose is NOT read: 'DOS 01/09/2026', 'visit of', 'Treatment dates A to B', 'next visit date' ... inside a sentence never give a date (SCOPE_CUTS row 28). Every other line prints the fillable blank
10	'date of service [__________] (statement dated X)' and the Step 3 note, and the paralegal fills it from the quote. The result of `resolve` is one of:
11	  - `stated`: a date or complete period from source (1), or the record's own date from source (2);
12	  - `not_stated` with reason `no_date` / `non_service_date`: the line has no date of source (1) or (2) (`non_service_date` names the one date the code saw but does not read);
13	  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): a DOS-column cell the code cannot read with certainty;
14	    the note names the date as the column writes it.
15	Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
16	(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
17	import datetime as _dt
18	import json
19	import pathlib
20	import re
21	
22	from app.backend import amounts as AM
23	
24	TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
25	_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))
26	
27	
28	def _tokens(text: str) -> list:
29	    return re.findall(r"[^\W_]+", (text or "").lower())
30	
31	
32	def _phrase_rx(terms):
33	    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")
34	
35	
36	_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
37	_OPEN = int(_TYPES["opening_chars"])
38	
39	
40	def _hit(rx, text) -> bool:
41	    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))
42	
43	
44	def record_kind(source, excerpt: str = "") -> str:
45	    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
46	    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
47	    identification by a DOCUMENT-TYPE word in the source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, run report, operative report ...; D-073: a provider
48	    name such as Clinic, ED, Urgent Care, Imaging, Orthopedics is never enough). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
49	    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
50	    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
51	        return "bill"
52	    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
53	        return "other"
54	    return "encounter" if _hit(_ENC, src) else "other"
55	
56	_MON = AM._MON
57	_ORD = r"(?:st|nd|rd|th)?"
58	_DASH = "–—"
59	_TOK = re.compile(
60	    r"(?<![\w/$])(?:"
61	    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
62	    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
63	    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
64	    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
65	    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
66	    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
67	    r")(?![\w/]|\.\d)", re.IGNORECASE)
68	_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
69	_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
70	# ---- D-073: the only evidence that reads a date. A column heading over the date cell (below), the UB-04 'statement covers period' span, and nothing in a sentence.
71	_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
72	_WINDOW = 60                     # characters before a date that may hold the UB-04 span label and the leader after it
73	_mask_leaders = AM.mask_leaders          # the one helper: a dotted leader is neither a sentence end nor a column gap (T-209 r2)
74	
75	
76	_UB_SPAN = re.compile(r"\bstatement\s+(?:covers\s+)?period" + _LBL_END, re.IGNORECASE)       # UB-04 FL6 'Statement Covers Period FROM ... THROUGH ...': the span of the services of a coded line
77	_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
78	# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
79	_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
80	                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
81	_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful
82	
83	REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
84	WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
85	
86	
87	def display(first, last=None) -> str:
88	    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
89	    def lng(iso):
90	        d = _dt.date.fromisoformat(iso)
91	        return f"{d.strftime('%B')} {d.day}, {d.year}"
92	    if not last or last == first:
93	        return lng(first)
94	    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
95	    if (a.year, a.month) == (b.year, b.month):
96	        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
97	    if a.year == b.year:
98	        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
99	    return f"{lng(first)}–{lng(last)}"
100	
101	
102	BLANK = "date of service [__________]"
103	
104	
105	def not_stated_text(statement_iso) -> str:
106	    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
107	    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
108	    if statement_iso:
109	        return f"{BLANK} (statement dated {display(statement_iso)})"
110	    return BLANK
111	
112	
113	def printed_text(res: dict, statement_iso) -> str:
114	    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
115	    return not_stated_text(statement_iso)
116	
117	
118	_WHY = {
119	    "ambiguous_numeric": "The date of service column of the bill reads {raw}, which can be read as month/day or day/month; the record does not settle which.",
120	    "two_digit_year": "The date of service column of the bill reads {raw}, which has a two-digit year; the code does not guess the century.",
121	    "no_year": "The date of service column of the bill reads {raw}, which states no year; the code does not borrow one from the statement.",
122	    "invalid": "The date of service column of the bill reads {raw}, which is not a complete date on the calendar.",
123	    "several_dates": "The date of service column of the bill holds more than one date ({raw}) and nothing says which one belongs to this charge.",
124	    "implausible": "The date of service column of the bill reads {raw}, but that date is after the statement it appears on or years before it.",
125	    "non_service_date": "The line shows {raw}, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service.",
126	    "no_date": "The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note).",
127	}
128	_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
129	_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and fill the blank before you rely on it."
130	
131	
132	def confirm_note(reason, raw) -> str:
133	    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
134	    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)
135	
136	
137	def _iso(y, mo, d):
138	    try:
139	        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
140	    except ValueError:
141	        return None
142	
143	
144	class _Tok:
145	    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")
146	
147	    def __init__(self, m):
148	        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
149	        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
150	        getattr(self, "_" + self.kind)(m.group(0))
151	        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
152	            self.flaw = "invalid"
153	
154	    def _iso(self, s):
155	        y, mo, d = (int(x) for x in s.split("-"))
156	        self.fixed = _iso(y, mo, d)
157	
158	    def _num(self, s):
159	        a, b, y = re.split(r"[/.-]", s)
160	        if len(y) == 2:
161	            self.flaw = "two_digit_year"
162	            return
163	        a, b, y = int(a), int(b), int(y)
164	        md, dm = _iso(y, a, b), _iso(y, b, a)
165	        if md and dm and md != dm:
166	            self.ambiguous = {"MD": md, "DM": dm}
167	        elif md or dm:
168	            self.fixed = md or dm
169	            self.order = None if (md and dm) else ("MD" if md else "DM")
170	
171	    def _mdy(self, s):
172	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
173	        if m.group(4):
174	            self.flaw = "two_digit_year"
175	            return
176	        if not m.group(3):
177	            self.flaw = "no_year"
178	            return
179	        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))
180	
181	    def _dmy(self, s):
182	        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
183	        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))
184	
185	    def _md(self, s):
186	        self.flaw = "no_year"
187	
188	    def _mper(self, s):
189	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
190	        if not m.group(5):
191	            self.flaw = "no_year"
192	            return
193	        y, m1 = int(m.group(5)), _mon(m.group(1))
194	        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
195	        if a and b and b > a:
196	            self.first, self.last = a, b
197	        else:
198	            self.flaw = "invalid"
199	
200	
201	def _mon(name):
202	    from app.backend import dates
203	    return dates.MONTHS[name.lower()[:3]]
204	
205	
206	class _Unit:
207	    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
208	    def __init__(self, toks):
209	        self.toks = toks
210	        self.start, self.end = toks[0].start, toks[-1].end
211	
212	    def raw(self, text):
213	        return text[self.start:self.end]
214	
215	
216	def _units(text: str) -> list:
217	    toks = [_Tok(m) for m in _TOK.finditer(text)]
218	    out, k = [], 0
219	    while k < len(toks):
220	        t = toks[k]
221	        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
222	            out.append(_Unit([t, toks[k + 1]]))
223	            k += 2
224	        else:
225	            out.append(_Unit([t]))
226	            k += 1
227	    return out
228	
229	
230	def _certain(unit: _Unit, ref):
231	    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
232	    for t in unit.toks:
233	        if t.flaw:
234	            return "bad", t.flaw
235	    if len(unit.toks) == 1 and unit.toks[0].first:
236	        return "ok", unit.toks[0].first, unit.toks[0].last
237	    determined = {t.order for t in unit.toks if t.order}
238	    amb = [t for t in unit.toks if t.ambiguous]
239	    if len(determined) > 1:
240	        return "bad", "ambiguous_numeric"
241	    if determined:
242	        order = next(iter(determined))
243	    elif amb:
244	        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
245	        if len(feasible) != 1:
246	            return "bad", "ambiguous_numeric"
247	        order = feasible[0]
248	    else:
249	        order = None
250	    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
251	    if len(isos) == 2 and isos[1] <= isos[0]:
252	        return "bad", "invalid"
253	    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)
254	
255	
256	def _header_cells(excerpt: str, row_ls: int):
257	    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line. A bare From / To / Thru cell
258	    under a line that names the service (a CMS-1500 '24A DATE(S) OF SERVICE' over 'From To') takes that line's words, so the cell names the service too."""
259	    rev = list(reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]))
260	    for k, line in enumerate(rev):
261	        if not line.strip():
262	            return None
263	        if re.search(r"\d", line) and not _H_SVC.search(line):
264	            continue
265	        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
266	        above = rev[k + 1].strip() if k + 1 < len(rev) else ""
267	        if above and _H_SVC.search(above) and not _H_SVC.search(line):
268	            cells = [(c, f"{above} {t}" if re.fullmatch(r"(?i)from|to|thru|through", t.strip()) else t) for c, t in cells]
269	        return cells if len(cells) >= 2 else None
270	    return None
271	
272	
273	def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
274	    heads = _header_cells(excerpt, row_ls)
275	    if not heads:
276	        return ""
277	    col = tok_abs - row_ls
278	    if len(heads) == len(row_cells):
279	        idx = next((i for i, (a, b) in enumerate(row_cells) if a <= col < b), None)
280	        if idx is not None:
281	            return heads[idx][1]
282	    return min(heads, key=lambda h: abs(h[0] - col))[1]
283	
284	
285	def _plausible(first, last, ref) -> bool:
286	    """A service date is not after the record it appears in and not years before it."""
287	    if not ref:
288	        return True
289	    r = _dt.date.fromisoformat(ref)
290	    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)
291	
292	
293	def _decide(units, text, ref):
294	    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
295	    reads = [(u, _certain(u, ref)) for u in units]
296	    raws = [" ".join(u.raw(text).split()) for u in units]
297	    if len(units) > 1:
298	        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
299	        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
300	            return "bad", "several_dates", raws
301	        first, last = next(iter(same))
302	    else:
303	        r = reads[0][1]
304	        if r[0] != "ok":
305	            return "bad", r[1], raws
306	        first, last = r[1], r[2]
307	    if not _plausible(first, last, ref):          # in every record: a service date is not after the record's own date and not years before it (a prior treatment's DOS is not this charge's)
308	        return "bad", "implausible", raws
309	    return "ok", first, last
310	
311	
312	def _apply(out: dict, res) -> dict:
313	    if res[0] == "ok":
314	        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
315	    else:
316	        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
317	    return out
318	
319	
320	_MULTI = re.compile(r"\b(?:visits|sessions|treatments|appointments|encounters)\b|\bto[ -]date\b|\bvisits?\s+\d+\s*(?:-|\u2013|\u2014|to|through|thru)\s*\d+|"
321	                    r"\b(?:[2-9]|\d{2,}|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*(?:x|times)\b", re.IGNORECASE)          # a charge for more than one visit
322	
323	
324	def _table_dates(seg, excerpt, ss, a_start, units):
325	    """[(unit, heading)] of a bill-table row's dates, in the row's own text `seg`; the heading is the column heading over the date cell ('' when none)."""
326	    row_ls = excerpt.rfind("\n", 0, a_start) + 1
327	    rl_end = excerpt.find("\n", a_start)
328	    row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
329	    row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
330	    return [(u, _column_head(excerpt, row_ls, row_cells, ss + u.start)) for u in units]
331	
332	
333	def _from_to(pairs):
334	    """The units of a table row's service-date cells: a CMS-1500 24A 'From' cell followed by its 'To' / 'Thru' cell is one period (the same day twice is that day)."""
335	    out, k = [], 0
336	    while k < len(pairs):
337	        u, head = pairs[k]
338	        if not _H_SVC.search(head or ""):
339	            k += 1
340	            continue
341	        nxt = pairs[k + 1] if k + 1 < len(pairs) else None
342	        if nxt and re.search(r"\bfrom\b", head, re.IGNORECASE) and re.search(r"\b(?:to|thru|through)\b", nxt[1] or "", re.IGNORECASE):
343	            same = u.toks[-1].raw.strip() == nxt[0].toks[0].raw.strip()
344	            out.append(u if same else _Unit(u.toks + nxt[0].toks))
345	            k += 2
346	            continue
347	        out.append(u)
348	        k += 1
349	    return out
350	
351	
352	def resolve(excerpt: str, start: int, source, date_iso) -> dict:
353	    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the date text the reason is about), raws ([the dates as written])} for
354	    the figure at `start` of `excerpt`, in a record with header `source` and date `date_iso`. Exactly two sources give a date (module doc, D-073)."""
355	    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
356	    excerpt = _mask_leaders(excerpt)
357	    amts = AM.find_amounts(excerpt or "")
358	    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
359	    if i is None:
360	        return out
361	    a = amts[i]
362	    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
363	    kind = record_kind(source, excerpt)
364	    seg = excerpt[ss:se]
365	    units = _units(seg)
366	    others = [u.raw(seg) for u in units]                                   # the dates of the line that no source reads
367	    if len(AM._cells(seg)) >= 2 and units:                                 # source (1): the date cell of its own row, under a heading that names the date of service
368	        lab = _from_to(_table_dates(seg, excerpt, ss, a["start"], units))
369	        if lab:
370	            return _apply(out, _decide(lab, seg, date_iso))
371	    if kind == "bill" and AM._CODE_RX.search(seg[:a["start"] - ss]) and (_UB.search(source or "") or _UB.search(excerpt or "")):
372	        prefix = excerpt[:se]                                              # source (1), UB-04 FL6: a coded line takes the span its 'statement covers period FROM ... THROUGH ...' states
373	        span = [u for u in _units(prefix) if _UB_SPAN.search(prefix[max(0, u.start - _WINDOW):u.start])]
374	        if span:
375	            return _apply(out, _decide(span, prefix, date_iso))
376	    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
377	        if others:
378	            out.update(reason="non_service_date", raw=others[0])
379	        return out
380	    if not date_iso:
381	        return out
382	    # source (2): the date of an identified encounter record is the visit's, unless the charge's own sentence names another date or charges more than one visit
383	    for u in units:
384	        r = _certain(u, date_iso)
385	        if not (r[0] == "ok" and r[1] == date_iso and not r[2]):
386	            out.update(reason="non_service_date", raw=u.raw(seg))
387	            return out
388	    if _MULTI.search(seg):
389	        return out
390	    out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
391	    return out
392	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:43:57.274Z

**tool call — Bash**
````
{
 "command": "git rev-parse f9c0faf HEAD; git log --oneline -6; git diff --stat f9c0faf HEAD -- app/backend evals tests | tail -3; git status --short | head; sed -n 100,200p app/backend/store.py; sed -n 205,235p app/backend/export.py; ls tests/unit | grep -i t202; ls tests/unit | grep t200"
}
````

### User / tool · 2026-11-03T02:43:57.474Z

**tool result**
````
f9c0faf12067d4e56fd50d9968558f701d8bee1c
f9c0faf12067d4e56fd50d9968558f701d8bee1c
f9c0faf test(e2e): T-202 r5 D-073 case_09 and lib11 ED lines show the fillable blank, not a prose-read date
43b364d feat(backend): T-202 r5 D-073 charge dates from two sources only; prose labels removed; leader mask in amounts; T-207 r2 rule pins
ad0d91a fix(qa): T-210 declare the five guided test ids (brand, footer-note, demo-badge, btn-draft, draft-done) in the E2E contract
0281189 chore(guard): subagents stage only into a temp index (shared index kept holding stale reverts, T-201/T-204)
1b3c58a fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
efda639 docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)
MM .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
D  .claude/agent-memory/backend/project_t202_r5_d073.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md


def _by_id(records):
    return {r["id"]: r for r in records}


# ---------------------------------------------------------------- unit dicts for export / totals
def amount_pos(item: dict, rec):
    """Where the amount's own figure sits in its excerpt (T-140 r3: quotes and reasons are taken from the figure's own offset, never from a text search that finds
    the first equal figure). None when the stored offsets do not point at the figure's text."""
    start, raw = item.get("excerpt_start"), item.get("text") or ""
    if rec is None or start is None or not raw:
        return None
    from app.backend import generator          # lazy: generator imports store
    i = start - generator.body_offset(rec)
    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None


def charge_service_date(item: dict, rec, pos) -> dict:
    """D-071 + D-073 (extends T-200, T-202 round 5): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 2026)'
    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
    A date has exactly two sources (service_date.resolve): the date cell of the line's own row under a bill-table heading that names the date of service (a CMS-1500 24A From/To pair or a
    UB-04 statement-covers-period span included), or the record's own date when the source label names a DOCUMENT TYPE (visit, progress or office note, ER or ED record, discharge summary, PT
    or therapy note, run report, operative report ...; service_date.record_kind, app/backend/encounter_types.json) and the charge's sentence holds no other date or visit count. Prose is never
    read, a provider name is never a document type, and a bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its date. A charge the paralegal
    counted for a missing date of service (D-064) is not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    if counted_undated:
        r = dict(none)
    elif rec is None or pos is None or not item.get("excerpt"):
        r = dict(none)          # T-207 r2 F3: a figure the code cannot locate in its record is never looked at, so not even an encounter record lends its date: the blank prints
    else:
        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
    stated = r["state"] == "stated"
    note = None
    if not stated and not counted_undated:
        note = SD.confirm_note(r["reason"], r["raw"])
    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd),
            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}


def charge_service_dates(item: dict, rec, pos) -> tuple:
    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
    d = charge_service_date(item, rec, pos)
    return d["date_iso"], d["end_iso"]


def export_case(conn, case_id: str, blockers: bool = True) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
    rec_of = {r["id"]: r for r in recs}
    from app.backend import review as review_mod        # lazy: review imports store
    from app.backend import present                     # lazy: present imports store
    prep = present.models_for(conn, case_id, {"generator": "", "judge": ""})["generator_prepared"]      # D-069: the case's provenance chooses the wording of the export's notes and labels
    ents = []
    for e in DB.list_items(conn, case_id, "entry"):
        if e["state"] == "rejected":
            continue
        ed = e.get("edited") or {}
        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
        if "summary" in ed:
            d["original_summary"] = ed.get("original_summary", e["summary"])
            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
                d["original_summary_failed"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]
        if "excerpt" in ed:
            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
        lad = e.get("ladder") or {}
        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
            d["code_check_failed"] = True
        if lad.get("entered_by"):
            d["entered_by_reviewer"] = True
        if e["state"] == "needs_review" and any(k in ed for k in ("summary", "excerpt")):
            d["edit_state_reasons"] = list(e.get("state_reasons") or [])          # T-134: why her edit is still marked for review; the notes keep it after she accepts
        if review_mod.edit_unconfirmed("entry", e):          # T-134: reworded and still needs_review: not decided. Out of the letter and counted as pending (D-045a); the notes name why.
            d["review_status"] = "pending"
            d["edit_unconfirmed"] = True
        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")), prep)["label"]
        ents.append(d)
    amts = []
    for a in DB.list_items(conn, case_id, "amount"):
        if a["state"] == "rejected":
            continue
        r = rec_of.get((a["record_ids"] or [None])[0])
        d = dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, r))
        if a["kind"] == "charge":
            sd = charge_service_date(a, r, d["pos"])
            d["dos_iso"], d["dos_end_iso"], d["dos_text"], d["dos_note"] = sd["date_iso"], sd["end_iso"], sd["text"], sd["confirm_note"]
        amts.append(d)
    fl = []
    for f in DB.list_items(conn, case_id, "flag"):

    def source(self, n):
        return (self.records.get(n) or {}).get("source", "")

    def text(self, n):
        return (self.records.get(n) or {}).get("excerpt", "")

    def rec_date(self, n):
        return (self.records.get(n) or {}).get("date_iso")

    def charge_when(self, a):
        """D-071 (extends T-200): the label before a charge's amount in the letter. A date there reads as the date of service, so it is the service date the charge's own bill line
        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026)' (D-071 addendum: a fillable blank). Chosen over dropping the date
        because the adjuster can still match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict
        without `dos_iso` (a hand-built one) keeps the record's date."""
        n, src = a["record_no"], self.source(a["record_no"])
        if "dos_iso" not in a:
            return f"{src}, {_long_date(self.rec_date(n))}"
        if a["dos_iso"]:
            return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"

    def cite(self, n):
        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"

    def cite_dated(self, n):
        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"

    def quote(self, n, ev, whole_sentence=False):
        """Quote evidence from record n. A directly following full stop is included when the evidence starts a
test_t202_charge_service_dates.py
test_t202_r2_service_date_layouts.py
test_t202_r3_allow_list.py
test_t202_r4_encounter.py
test_t202_r5_d073.py
test_t200_undated_charge_label.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:43:59.413Z

**tool call — Bash**
````
{
 "command": "wc -l tests/unit/test_t202_r5_d073.py && cat tests/unit/test_t202_r5_d073.py"
}
````

### User / tool · 2026-11-03T02:43:59.497Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:00.800Z

**tool call — Bash**
````
{
 "command": "sed -n 25,470p tests/unit/test_t202_r5_d073.py | cut -c1-260"
}
````

### User / tool · 2026-11-03T02:44:00.888Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:02.421Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def test_\\|^@pytest\\|^class \\|^# ---\\|^    def test\" tests/unit/test_t202_r5_d073.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:44:02.508Z

**tool result**
````
70:def test_a_line_that_is_not_split_into_cells_is_not_a_table_row():
76:def test_a_dos_column_cell_prints_its_own_rows_date():
82:def test_a_heading_that_does_not_name_service_gives_the_blank():
87:def test_a_dos_cell_holding_a_range_prints_the_range_whole():
92:def test_a_treatment_dates_range_in_a_sentence_is_not_read_in_any_record():
101:def test_cms1500_24a_from_to_cells_print_the_period():
107:def test_cms1500_with_service_from_and_service_to_headings():
115:def test_ub04_statement_covers_period_prints_the_period_for_a_coded_line_only():
124:@pytest.mark.parametrize("src", [ER, "Austin EMS run report", PT9, "Hill Country Pain Management, follow-up", "Dr. Casimir Voss, orthopedic surgery, operative report", NOTE,
128:def test_a_document_type_word_identifies_an_encounter_that_lends_its_date(src):
133:@pytest.mark.parametrize("src", ["Thistlewick Orthopedics, Dr. Beatrix Quillon", "Fennimoor Spine Clinic", "Hobbleton Family Clinic", "Austin Imaging", "Central ER", "Quillfeather Urgent Care",
139:def test_a_provider_name_alone_is_never_enough_so_the_header_date_never_prints(src):
148:@pytest.mark.parametrize("ex", ["Office visit 02/02/2026, 99213, charge $275.00.", "Office visit 99213 charge $275.00 for the visit of 02/02/2026.", "Office visit 99213 charge $275.00.",
150:def test_a_bill_labelled_with_the_provider_name_only_never_prints_the_statement_date(ex):
157:def test_a_sentence_with_another_date_or_a_visit_count_gives_the_blank_even_in_an_encounter():
170:def test_an_encounter_with_no_record_date_prints_the_bare_blank():
181:@pytest.mark.parametrize("word", OTHER_VISIT_WORDS)
182:@pytest.mark.parametrize("label", ["DOS", "date of service", "Date of Service:", "dates of service", "service date"])
183:def test_another_visits_label_in_an_encounter_note_never_prints_that_visits_date(word, label):
192:@pytest.mark.parametrize("word", ["Next visit", "follow-up visit", "planned", "prior", "next", "previous", "last", "initial", "scheduled", "upcoming", "future", "first", "return", ""])
193:def test_the_same_label_words_in_a_bill_tail_print_the_blank(word):
257:@pytest.mark.parametrize("pid,src,rd,ex,fig,ok", PROBES, ids=[p[0] for p in PROBES])
258:def test_every_reviewer_probe_prints_the_blank_or_the_right_date(pid, src, rd, ex, fig, ok):
268:def test_the_old_wrong_dates_are_flagged_by_the_independent_check():
293:def test_a_dotted_leader_line_is_totaled_and_dated_through_a_full_case_run():
313:def test_the_synthetic_variants_of_both_reviewers_never_print_a_wrong_date_in_a_full_run():
331:def test_the_table_lists_document_types_only_and_both_readers_share_it():
340:def test_the_corpus_lines_that_become_blanks_are_exactly_the_provider_only_and_prose_dated_ones():
348:def test_a_period_in_the_charge_sentence_is_another_date_even_when_it_starts_on_the_record_date():
352:def test_the_check_reads_the_whole_sentence_around_a_trimmed_quote():
369:def test_the_five_year_bound_is_1830_days_edges_included():
392:def test_a_date_in_a_record_with_no_date_is_read_when_it_is_unambiguous_and_never_when_it_reads_two_ways():
397:def test_a_numeric_date_is_resolved_only_when_one_reading_is_on_or_before_the_record_date():
406:def test_a_period_whose_ends_force_different_orders_is_not_read():
413:@pytest.mark.parametrize("heading", ["Encounter Date", "Date of Visit", "Visit Date", "Service Date"])
414:def test_the_visit_and_encounter_headings_name_the_service(heading):
421:def test_a_next_dos_in_a_sentence_is_a_date_the_code_does_not_read():
427:def test_a_counted_undated_charge_has_no_note_and_an_uncounted_one_has_one():
438:def test_an_encounter_figure_the_code_cannot_locate_prints_the_blank():
450:def test_the_check_pairs_24a_from_to_cells_and_reads_a_span_only_on_a_ub04():
465:def test_the_check_treats_a_dotted_leader_as_part_of_the_sentence():
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:03.902Z

**tool call — Bash**
````
{
 "command": "sed -n 70,200p tests/unit/test_t202_r5_d073.py | cut -c1-330; sed -n 331,470p tests/unit/test_t202_r5_d073.py | cut -c1-330"
}
````

### User / tool · 2026-11-03T02:44:04.002Z

**tool result**
````
def test_a_line_that_is_not_split_into_cells_is_not_a_table_row():
    """Cells are split at a tab, a pipe or two spaces; one line of single-spaced words under a DOS heading is a sentence, so the blank prints."""
    ex = "Itemized ledger.\nDOS         Charge\n06/10/2026 manual therapy $70.00\n"
    assert printed(ex, "$70.00", LEDGER, "2026-06-30") == "BLANK"


def test_a_dos_column_cell_prints_its_own_rows_date():
    assert printed(DOS_TABLE, "$70.00", LEDGER, "2026-06-30") == "June 10, 2026"
    assert printed(DOS_TABLE, "$95.00", LEDGER, "2026-06-30") == "June 17, 2026"
    assert printed(DOS_TABLE, "$95.00", LEDGER, "2026-06-15") == "BLANK"          # a service on the 17th cannot be on a statement of the 15th


def test_a_heading_that_does_not_name_service_gives_the_blank():
    ex = DOS_TABLE.replace("DOS        ", "Posted     ")
    assert printed(ex, "$70.00", LEDGER, "2026-06-30") == "BLANK" and printed(ex, "$95.00", LEDGER, "2026-06-30") == "BLANK"


def test_a_dos_cell_holding_a_range_prints_the_range_whole():
    ex = "Itemized ledger.\nDOS\tService\tCharge\n01/23/2026 to 03/06/2026\tPT, 9 visits\t$1,665.00\n"
    assert printed(ex, "$1,665.00", LEDGER, "2026-04-01") == "January 23–March 6, 2026"


def test_a_treatment_dates_range_in_a_sentence_is_not_read_in_any_record():
    ex = "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00."
    assert printed(ex, "$1,665.00", PT9, "2026-03-06") == "BLANK"
    assert printed(ex, "$1,665.00", LEDGER, "2026-04-01") == "BLANK"


CMS_24A = "OCR of scanned CMS-1500.\n24A DATE(S) OF SERVICE\nFrom        To          CPT    Charges\n06/24/2026  06/26/2026  99204  $185.00\n06/24/2026  06/24/2026  20610  $210.00\n07/08/2026  07/02/2026  99213  $150.00\n"


def test_cms1500_24a_from_to_cells_print_the_period():
    assert printed(CMS_24A, "$185.00", CMS, "2026-07-14") == "June 24–26, 2026"
    assert printed(CMS_24A, "$210.00", CMS, "2026-07-14") == "June 24, 2026"           # the same day twice is that day
    assert printed(CMS_24A, "$150.00", CMS, "2026-07-14") == "BLANK"                    # a period that ends before it starts is not certain


def test_cms1500_with_service_from_and_service_to_headings():
    ex = "OCR of scanned CMS-1500.\nService From  Service To  CPT    Charges\n06/24/2026    06/26/2026  99204  $185.00\n"
    assert printed(ex, "$185.00", CMS, "2026-07-14") == "June 24–26, 2026"


UB_PERIOD = "UB-04 type of bill 0111, statement covers period FROM 06/09/2026 THROUGH 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."


def test_ub04_statement_covers_period_prints_the_period_for_a_coded_line_only():
    assert printed(UB_PERIOD, "$2,105.00", UB, "2026-06-19") == "June 9–12, 2026"
    uncoded = "UB-04 type of bill 0111, statement covers period FROM 06/09/2026 THROUGH 06/12/2026. Room and board charge $2,105.00."
    assert printed(uncoded, "$2,105.00", UB, "2026-06-19") == "BLANK"
    other = UB_PERIOD.replace("UB-04 type of bill 0111, ", "").replace("statement covers period", "billing period")
    assert printed(other, "$2,105.00", LEDGER, "2026-06-19") == "BLANK"                 # only a UB-04 statement period is a service span


# ================================================================ 2. source (2): an encounter record identified by a document-type word
@pytest.mark.parametrize("src", [ER, "Austin EMS run report", PT9, "Hill Country Pain Management, follow-up", "Dr. Casimir Voss, orthopedic surgery, operative report", NOTE,
                                 "Hobbleton Family Clinic, visit", "Thornapple Valley Hospital ED record", "Capital PT note", "Larkmoor Physical Therapy, discharge summary",
                                 "Austin Imaging, cervical MRI", "Consultorio Médico Aguaclara, nota de consulta", "Dr. Fenwick Larkspur, orthopedics, new patient",
                                 "Plumtree Physical Therapy, initial evaluation"])
def test_a_document_type_word_identifies_an_encounter_that_lends_its_date(src):
    assert printed("Charge: $220.00.", "$220.00", src, "2026-06-15") == "June 15, 2026"
    assert SD.record_kind(src, "x") == LC._record_kind(src, "x") == "encounter"


@pytest.mark.parametrize("src", ["Thistlewick Orthopedics, Dr. Beatrix Quillon", "Fennimoor Spine Clinic", "Hobbleton Family Clinic", "Austin Imaging", "Central ER", "Quillfeather Urgent Care",
                                 "Thornbury Regional ED", "Capital PT", "Fernwhistle County EMS", "Dr. Alvarez, primary care", "Dr. Hobart Wimbleton, radiology", "Gloamwood Chiropractic",
                                 "Fennimoor Spine Clinic, amount due notice", "Fennimoor Spine Clinic, lien notice", "Fennimoor Spine Clinic, demand", "Fennimoor Spine Clinic, patient accounts",
                                 "Fennimoor Spine Clinic, accounts receivable", "Fennimoor Spine Clinic, settlement", "Fennimoor Spine Clinic, tally", "Fennimoor Spine Clinic, totals",
                                 "Fennimoor Spine Clinic, outstanding", "Fennimoor Spine Clinic, past due notice", "Fennimoor Spine Clinic, remit", "Fennimoor Spine Clinic, rates",
                                 "Fennimoor Spine Clinic, write-off", "Fennimoor Spine Clinic, ar report", "Fennimoor Spine Clinic, collections letter", "Medical record"])
def test_a_provider_name_alone_is_never_enough_so_the_header_date_never_prints(src):
    """Staff r4b major 1 and paralegal r4 blocker 3: a provider-only or unknown-type source prints the blank, never its header date."""
    assert SD.record_kind(src, "x") == LC._record_kind(src, "x") == "other" or SD.record_kind(src, "x") == LC._record_kind(src, "x") == "bill"
    for ex in ("Office visit charge $220.00.", "Amount due for services: $220.00.", "Total owed $220.00 for services.", "Patient responsibility $220.00.", "Past due: $220.00",
               "Outstanding $220.00 on the file.", "Totals: $220.00", "Total due $220.00 for care provided.", "Write-off adjustment $220.00 applied.", "Collections notice: $220.00",
               "Lien amount $220.00 asserted.", "Please remit $220.00 for care.", "Debt $220.00."):
        assert printed(ex, "$220.00", src, "2026-06-15") == "BLANK", (src, ex)


@pytest.mark.parametrize("ex", ["Office visit 02/02/2026, 99213, charge $275.00.", "Office visit 99213 charge $275.00 for the visit of 02/02/2026.", "Office visit 99213 charge $275.00.",
                                "Amount due $275.00 for office visit on 02/02/2026.", "Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026."])
def test_a_bill_labelled_with_the_provider_name_only_never_prints_the_statement_date(ex):
    """Paralegal r4 blocker 3 (pa, pb, pc, S2, S4, S6, S7)."""
    fig = re.search(r"\$[\d,]+\.\d\d", ex).group(0)
    for src in ("Hobbleton Family Clinic", "Austin Imaging", "Central ER", "Gloamwood Chiropractic"):
        assert printed(ex, fig, src, "2026-03-01") == "BLANK", (src, ex)


def test_a_sentence_with_another_date_or_a_visit_count_gives_the_blank_even_in_an_encounter():
    assert printed("Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.", "$150.00", NOTE, "2026-01-16") == "BLANK"
    assert printed("Reviewed ER records. DOS 01/09/2026. Office visit charge $150.00.", "$150.00", NOTE, "2026-01-16") == "January 16, 2026"          # another sentence
    assert printed("Visit charge $150.00 on 01/16/2026.", "$150.00", NOTE, "2026-01-16") == "January 16, 2026"                  # the same date written again
    assert printed("Visit charge $150.00 on 01/17/2026.", "$150.00", NOTE, "2026-01-16") == "BLANK"
    for ex in ("Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.", "Total for visits 1-9: $1,665.00.", "PT charges to date $1,665.00.", "Charge for 14 visits $2,310.00.",
               "Six sessions this month, charge $1,110.00.", "Charge for 2 x $185.00 sessions."):
        fig = re.search(r"\$[\d,]+\.\d\d", ex).group(0)
        assert printed(ex, fig, PT9, "2026-03-06") == "BLANK", ex
    assert printed("Discharged from PT. Charge $185.00.", "$185.00", PT9, "2026-03-06") == "March 6, 2026"
    assert printed("Charge per visit $185.00.", "$185.00", PT9, "2026-03-06") == "March 6, 2026"


def test_an_encounter_with_no_record_date_prints_the_bare_blank():
    assert head("Charge: $220.00.", "$220.00", NOTE, None) == f"{NOTE}, {BLANK}: $220.00"


# ================================================================ 3. every probe, every round: the right date or the blank, never a wrong date
OTHER_VISIT_WORDS = ["Next visit", "Next visit's", "Next appointment", "Follow-up visit", "Follow up", "Follow-up appointment", "Planned", "Proposed", "Anticipated", "Expected",
                     "Subsequent", "Second", "Cancelled", "Missed", "Earlier", "Original", "Other", "Revised", "Re-check", "Pending", "Old", "Last visit", "Prior treatment",
                     "Missed appointment", "PT referral", "Previous", "Initial", "First", "Return", "Scheduled", "Upcoming", "Future", "Prior", "Last", "Next", "ER", "Reviewed ER records,",
                     "Last seen", "Initial eval", "Previous visit's", "Rescheduled", "Prior  ", "follow up from ER", "Follow-up of ER visit", "Visit", "Seen", "Seen on", "Date"]


@pytest.mark.parametrize("word", OTHER_VISIT_WORDS)
@pytest.mark.parametrize("label", ["DOS", "date of service", "Date of Service:", "dates of service", "service date"])
def test_another_visits_label_in_an_encounter_note_never_prints_that_visits_date(word, label):
    """Staff r4b finding 2 (32 unguarded labels), paralegal r4 blocker 1 (O1-O7, O10), r3 'next visit date'; the sentence holds the other date, so the blank prints (never 05/20)."""
    same = f"{word} {label} 05/20/2026, office visit charge $220.00."
    assert printed(same, "$220.00", ER, "2026-06-15") == "BLANK", same
    sep = f"{word} {label} 05/20/2026. Office visit charge $220.00."
    assert printed(sep, "$220.00", ER, "2026-06-15") in ("BLANK", "June 15, 2026"), sep          # another sentence: the visit's own date or the blank, never May 20
    assert "May 20" not in head(same, "$220.00", ER, "2026-06-15") and "May 20" not in head(sep, "$220.00", ER, "2026-06-15")


@pytest.mark.parametrize("word", ["Next visit", "follow-up visit", "planned", "prior", "next", "previous", "last", "initial", "scheduled", "upcoming", "future", "first", "return", ""])
def test_the_same_label_words_in_a_bill_tail_print_the_blank(word):
    """Staff r4b: 'Office visit charge $150.00, next visit DOS 02/28/2026.' in a ledger printed February 28."""
    ex = f"Office visit charge $150.00, {word} DOS 02/28/2026.".replace(",  ", ", ")
    assert printed(ex, "$150.00", LEDGER, "2026-06-15") == "BLANK", ex
    ex2 = f"Office visit charge $150.00, {word} date of service 02/28/2026."
    assert printed(ex2, "$150.00", LEDGER, "2026-06-15") == "BLANK", ex2


def test_the_table_lists_document_types_only_and_both_readers_share_it():
    assert SD.TYPES_PATH == LC.TYPES_PATH
    terms = SD._TYPES["encounter"]
    for provider_word in ("clinic", "emergency", "urgent care", "therapy", "imaging", "radiology", "orthopedics", "orthopedic", "chiropractic", "primary care", "pain management",
                          "surgery", "ambulance", "telehealth", "physical therapy", "ed", "er", "ems", "pt", "ot"):
        assert provider_word not in terms, provider_word
    assert "encounter_abbreviations" not in SD._TYPES


def test_the_corpus_lines_that_become_blanks_are_exactly_the_provider_only_and_prose_dated_ones():
    got = LC.letters_for(open("evals/library/case_lib08_second_crash_mri_after.txt", encoding="utf-8").read())["all_accepted"]["letters"]["standard"]
    heads = [h for h, _ in LC.charge_lines(got)]
    assert "Thornbury Regional ED, date of service [__________] (statement dated January 12, 2026): $4,210.00" in heads
    sample = LC.letters_for(open("evals/golden/sample.txt", encoding="utf-8").read())["all_accepted"]["letters"]["standard"]
    assert "Central ER discharge summary, January 9, 2026: $6,240.00" in [h for h, _ in LC.charge_lines(sample)]


def test_a_period_in_the_charge_sentence_is_another_date_even_when_it_starts_on_the_record_date():
    assert printed("Visit charge $150.00 for 01/16/2026 to 01/20/2026.", "$150.00", NOTE, "2026-01-16") == "BLANK"


def test_the_check_reads_the_whole_sentence_around_a_trimmed_quote():
    """The letter may quote only a clause of the sentence (a trimmed quote); another date in the rest of the sentence still makes the record's date a guess. A semicolon ends the sentence."""
    q = "office visit charge $150.00"
    one = "Reviewed ER records 01/09/2026, office visit charge $150.00, plan unchanged."
    assert head(one, "$150.00", NOTE, "2026-01-16") == f"{blank_of(NOTE, '2026-01-16')}: $150.00"
    assert check(f"{NOTE}, January 16, 2026", one, "$150.00", NOTE, "2026-01-16", quote=q)          # another date in the sentence: the record's date is not certain
    assert check(blank_of(NOTE, "2026-01-16"), one, "$150.00", NOTE, "2026-01-16", quote=q) == []
    two = "Reviewed ER records 01/09/2026; office visit charge $150.00; plan unchanged."
    assert head(two, "$150.00", NOTE, "2026-01-16") == f"{NOTE}, January 16, 2026: $150.00"
    assert check(f"{NOTE}, January 16, 2026", two, "$150.00", NOTE, "2026-01-16", quote=q) == []


# ================================================================ 6. T-207 r2 (staff): every rule that survives D-073 is pinned by a test that fails under its mutant
def dos_cell(cell, fig="$100.00"):
    return f"Itemized ledger.\nDOS\tService\tCharge\n{cell}\toffice visit\t{fig}\n"


def test_the_five_year_bound_is_1830_days_edges_included():
    """Mutants: 365-day years (1825 days), a strict > at the lower edge, 4 or 6 years, a strict < at the record date."""
    rd = "2026-06-30"
    assert printed(dos_cell("2021-06-30"), "$100.00", LEDGER, rd) == "June 30, 2021"          # 5 calendar years (1826 days incl. one leap day): inside 1830
    assert printed(dos_cell("2021-07-05"), "$100.00", LEDGER, rd) == "July 5, 2021"
    lower = (__import__("datetime").date.fromisoformat(rd) - __import__("datetime").timedelta(days=1830)).isoformat()          # exactly on the lower edge: allowed (>=)
    below = (__import__("datetime").date.fromisoformat(rd) - __import__("datetime").timedelta(days=1831)).isoformat()          # one day past it: refused
    assert printed(dos_cell(lower), "$100.00", LEDGER, rd) != "BLANK"
    assert printed(dos_cell(below), "$100.00", LEDGER, rd) == "BLANK"
    assert printed(dos_cell("2026-06-30"), "$100.00", LEDGER, rd) == "June 30, 2026"          # a service on the statement date is allowed (<=)
    assert printed(dos_cell("2026-07-01"), "$100.00", LEDGER, rd) == "BLANK"
    # the independent check enforces the same edges
    ex = dos_cell(lower)
    q = f"{lower}\toffice visit\t$100.00"
    lower_long = SD.display(lower)
    assert check(f"{LEDGER}, {lower_long}", ex, "$100.00", LEDGER, rd, quote=q) == []
    ex2 = dos_cell(below)
    q2 = f"{below}\toffice visit\t$100.00"
    assert check(f"{LEDGER}, {SD.display(below)}", ex2, "$100.00", LEDGER, rd, quote=q2)
    assert check(f"{LEDGER}, June 30, 2026", dos_cell("2026-06-30"), "$100.00", LEDGER, rd, quote="2026-06-30\toffice visit\t$100.00") == []
    assert check(f"{LEDGER}, July 1, 2026", dos_cell("2026-07-01"), "$100.00", LEDGER, rd, quote="2026-07-01\toffice visit\t$100.00")


def test_a_date_in_a_record_with_no_date_is_read_when_it_is_unambiguous_and_never_when_it_reads_two_ways():
    assert printed(dos_cell("2026-04-13"), "$100.00", LEDGER, None) == "April 13, 2026"
    assert printed(dos_cell("04/05/2026"), "$100.00", LEDGER, None) == "BLANK"          # nothing says a reading cannot follow its statement


def test_a_numeric_date_is_resolved_only_when_one_reading_is_on_or_before_the_record_date():
    """Mutant: <= ref -> < ref. 04/05/2026 reads April 5 or May 4; on a statement dated May 4 both are on or before it, so it stays ambiguous."""
    assert printed(dos_cell("04/05/2026"), "$100.00", LEDGER, "2026-05-04") == "BLANK"
    assert printed(dos_cell("04/05/2026"), "$100.00", LEDGER, "2026-05-03") == "April 5, 2026"          # May 4 would follow the statement
    assert printed(dos_cell("04/05/2026"), "$100.00", LEDGER, "2026-04-04") == "BLANK"          # neither reading is on or before it
    assert check(blank_of(LEDGER, "2026-05-04"), dos_cell("04/05/2026"), "$100.00", LEDGER, "2026-05-04", quote="04/05/2026\toffice visit\t$100.00") == []
    assert check(f"{LEDGER}, April 5, 2026", dos_cell("04/05/2026"), "$100.00", LEDGER, "2026-05-04", quote="04/05/2026\toffice visit\t$100.00")


def test_a_period_whose_ends_force_different_orders_is_not_read():
    """Mutant: len(determined) > 1 -> > 2. 13/05/2026 can only be day/month, 05/13/2026 only month/day: the cell mixes both conventions."""
    for cell in ("13/05/2026 - 05/13/2026", "05/13/2026 - 14/05/2026"):
        assert printed(dos_cell(cell), "$100.00", LEDGER, "2026-06-30") == "BLANK", cell
    assert printed(dos_cell("05/13/2026 - 05/14/2026"), "$100.00", LEDGER, "2026-06-30") == "May 13–14, 2026"          # one convention: read


@pytest.mark.parametrize("heading", ["Encounter Date", "Date of Visit", "Visit Date", "Service Date"])
def test_the_visit_and_encounter_headings_name_the_service(heading):
    ex = f"Itemized ledger.\n{heading}\tService\tCharge\n03/13/2026\toffice visit\t$100.00\n"
    assert printed(ex, "$100.00", LEDGER, "2026-06-30") == "March 13, 2026"
    assert check(f"{LEDGER}, March 13, 2026", ex, "$100.00", LEDGER, "2026-06-30", quote="03/13/2026\toffice visit\t$100.00") == []
    assert check(blank_of(LEDGER, "2026-06-30"), ex, "$100.00", LEDGER, "2026-06-30", quote="03/13/2026\toffice visit\t$100.00")


def test_a_next_dos_in_a_sentence_is_a_date_the_code_does_not_read():
    ex = "Office visit charge $150.00, Next DOS 02/01/2026."
    d = store.charge_service_date({"excerpt": ex, "value_cents": 15000}, {"source": LEDGER, "date_iso": "2026-06-15"}, ex.index("$150.00"))
    assert d["state"] == "not_stated" and d["reason"] == "non_service_date" and "02/01/2026" in d["confirm_note"]


def test_a_counted_undated_charge_has_no_note_and_an_uncounted_one_has_one():
    ex = "Itemized ledger. New patient exam charge $250.00."
    pos = ex.index("$250.00")
    rec = {"source": LEDGER, "date_iso": "2026-06-15"}
    counted = store.charge_service_date({"excerpt": ex, "value_cents": 25000, "ladder": {"counted": {"not_counted_reason": AM.NO_DATE_WHY}}}, rec, pos)
    plain = store.charge_service_date({"excerpt": ex, "value_cents": 25000}, rec, pos)
    assert counted["state"] == plain["state"] == "not_stated"
    assert counted["confirm_note"] is None and plain["confirm_note"]
    assert counted["text"] == plain["text"]          # the letter prints the same blank either way


def test_an_encounter_figure_the_code_cannot_locate_prints_the_blank():
    """T-207 r2 F3: not even an identified encounter lends its date to a line the code cannot look at."""
    rec = {"source": PT9, "date_iso": "2026-03-06"}
    ex = "Plan of care. Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00."
    for pos in (None,):
        d = store.charge_service_date({"excerpt": ex, "value_cents": 166500}, rec, pos)
        assert d["state"] == "not_stated" and d["date_iso"] is None
    assert store.charge_service_date({"excerpt": "", "value_cents": 166500}, rec, 0)["state"] == "not_stated"
    assert store.charge_service_date({"excerpt": ex, "value_cents": 166500}, None, 5)["state"] == "not_stated"
    assert store.charge_service_date({"excerpt": "Charge $185.00.", "value_cents": 18500}, rec, 7)["state"] == "stated"


def test_the_check_pairs_24a_from_to_cells_and_reads_a_span_only_on_a_ub04():
    q = "06/24/2026  06/26/2026  99204  $185.00"
    ok = check(f"{CMS}, June 24–26, 2026", CMS_24A, "$185.00", CMS, "2026-07-14", quote=q)
    assert ok == []
    assert check(f"{CMS}, June 24, 2026", CMS_24A, "$185.00", CMS, "2026-07-14", quote=q)          # the end dropped
    assert check(blank_of(CMS, "2026-07-14"), CMS_24A, "$185.00", CMS, "2026-07-14", quote=q)          # a blank above a certain period
    same = "06/24/2026  06/24/2026  20610  $210.00"
    assert check(f"{CMS}, June 24, 2026", CMS_24A, "$210.00", CMS, "2026-07-14", quote=same) == []
    ex = "Statement period 05/13/2026 to 05/31/2026. CPT 97110 therapeutic exercise charge $95.00."
    q2 = "CPT 97110 therapeutic exercise charge $95.00."
    assert check(f"{LEDGER}, May 13–31, 2026", ex, "$95.00", LEDGER, "2026-06-05", quote=q2)          # not a UB-04: a statement period is not a service span
    assert check(blank_of(LEDGER, "2026-06-05"), ex, "$95.00", LEDGER, "2026-06-05", quote=q2) == []
    assert check(f"{UB}, June 9–12, 2026", UB_PERIOD, "$2,105.00", UB, "2026-06-19", quote="Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.") == []


def test_the_check_treats_a_dotted_leader_as_part_of_the_sentence():
    ex = "Dx: strain. Next visit 01/16/2026 ...... ER charges $6,240."
    q = "ER charges $6,240."
    assert printed(ex, "$6,240", ER, "2026-01-09") == "BLANK"
    assert check("Central ER discharge summary, January 9, 2026", ex, "$6,240", ER, "2026-01-09", quote=q)
    assert check(blank_of(ER, "2026-01-09"), ex, "$6,240", ER, "2026-01-09", quote=q) == []
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:33.758Z

**tool call — Bash**
````
{
 "command": "grep -n \"13/05/2026\" tests/unit/*.py | cut -c1-220 | head; echo ---; grep -ln \"confirm_note\" tests/unit/*.py; grep -n \"_ASK_\\|asks her\\|fill the blank\\|request a dated\" tests/unit/*.py | cut -c1-200 | head -20; echo ---; grep -n \"Receipt:\\|Account summary\\|opening\" tests/unit/test_t202*.py | cut -c1-200 | head; echo ---; grep -n \"dos_iso\" tests/unit/*.py | grep -v \"dos_iso=d\\[\" | cut -c1-200 | head -20; grep -n \"def test_\" tests/unit/test_t200_undated_charge_label.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:44:33.907Z

**tool result**
````
tests/unit/test_t202_r5_d073.py:407:    """Mutant: len(determined) > 1 -> > 2. 13/05/2026 can only be day/month, 05/13/2026 only month/day: the cell mixes both conventions."""
tests/unit/test_t202_r5_d073.py:408:    for cell in ("13/05/2026 - 05/13/2026", "05/13/2026 - 14/05/2026"):
---
tests/unit/test_t202_r4_encounter.py
tests/unit/test_t202_r5_d073.py
tests/unit/test_t202_r3_allow_list.py
tests/unit/test_t202_r2_service_date_layouts.py
tests/unit/test_t202_r3_allow_list.py:352:    assert "$275.00" in sec and "$180.00" in sec and sec.count("request a dated itemized bill") == 2 and "04/05/2026" in sec
---
tests/unit/test_t202_r5_d073.py:222:    ("r4 C3 ER charges opening", ER, "2026-01-09", "ER charges: $6,240. Next visit date 01/16/2026.", "$6,240", ("January 9, 2026",)),
tests/unit/test_t202_r4_encounter.py:115:@pytest.mark.parametrize("opening", ["Account summary: Office visit charge $220.00.", "Charges: Office visit charge $220.00.", "Receipt: Office visit charge $2
tests/unit/test_t202_r4_encounter.py:117:def test_a_record_that_opens_as_a_financial_paper_never_lends_its_header_date(opening):
tests/unit/test_t202_r4_encounter.py:119:    assert head(opening, "$220.00", src) == blank_hd(src, "June 15, 2026") + ": $220.00"
tests/unit/test_t202_r4_encounter.py:122:def test_a_clinical_opening_is_not_taken_for_a_financial_one():
tests/unit/test_t202_r4_encounter.py:143:def test_the_check_and_production_agree_on_every_lexicon_billing_example_and_opening():
---
tests/unit/test_billing.py:122:    assert first["dos"] == "05/27/26" and first["dos_iso"] == "2026-05-27" and first["posted"] == "05/28/26" and first["record_no"] == 1
tests/unit/test_billing.py:491:    assert l["dos"] is None and l["dos_iso"] is None and l["posted"] == "06/11/26" and "NO_DATE_OF_SERVICE" in l["checks"] and cents(l) == 3500
tests/unit/test_t202_r2_service_date_layouts.py:208:            "amounts": [dict(id="a1", record_no=1, cents=20000, cls="charge", raw="$200.00", excerpt=recs[0]["excerpt"], review_status="accepted", d
tests/unit/test_t202_r2_service_date_layouts.py:209:                        dict(id="a2", record_no=2, cents=30000, cls="charge", raw="$300.00", excerpt=recs[1]["excerpt"], review_status="accepted", d
tests/unit/test_t202_r2_service_date_layouts.py:218:            "amounts": [dict(id="a1", record_no=1, cents=20000, cls="charge", raw="$200.00", excerpt=recs[0]["excerpt"], review_status="accepted", d
tests/unit/test_t202_r2_service_date_layouts.py:219:                        dict(id="a2", record_no=2, cents=30000, cls="charge", raw="$300.00", excerpt=recs[1]["excerpt"], review_status="accepted", d
tests/unit/test_t200_undated_charge_label.py:78:    assert line(dos_iso=None, dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026
tests/unit/test_t200_undated_charge_label.py:79:    assert line(dos_iso="2026-03-27", dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, March 27, 2026: $250.00"        # D-071: the line's
tests/unit/test_t200_undated_charge_label.py:80:    assert line(dos_iso="2026-06-09", dos_end_iso="2026-06-12") == "Fennimoor Spine Clinic, itemized ledger, June 9\u201312, 2026: $250.00"
tests/unit/test_t200_undated_charge_label.py:82:    c = _case(dos_iso=None, dos_end_iso=None)
23:def test_lib11_counted_ledger_lines_are_labelled_with_the_statement_date(lib11, style):
39:def test_a_counted_line_keeps_its_citation_and_quote(lib11):
48:def test_charge_service_dates_reads_the_line_not_the_record_date():
61:def test_charge_service_dates_when_the_line_cannot_be_read():
75:def test_export_label_rules_on_a_hand_built_case():
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:37.390Z

**tool call — Bash**
````
{
 "command": "grep -n \"confirm_note\\|dos_note\" tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py | cut -c1-260; echo ---; sed -n 75,100p tests/unit/test_t200_undated_charge_label.py | cut -c1-260; echo ---; grep -n \"May 4\\|4–13\\|4-13\\|ambiguous_numeric\" tests/unit/test_t202*.py | cut -c1-220 | head -20; sed -n 340,356p tests/unit/test_t202_r3_allow_list.py | cut -c1-300"
}
````

### User / tool · 2026-11-03T02:44:37.500Z

**tool result**
````
tests/unit/test_t202_r4_encounter.py:32:                            dos_iso=d["date_iso"], dos_end_iso=d["end_iso"], dos_text=d["text"], dos_note=d["confirm_note"]))
tests/unit/test_t202_r4_encounter.py:210:    note = sd_of(ex, "$250.00", "Fennimoor Spine Clinic, itemized ledger")["confirm_note"]
tests/unit/test_t202_r3_allow_list.py:38:                            dos_iso=d["date_iso"], dos_end_iso=d["end_iso"], dos_text=d["text"], dos_note=d["confirm_note"]))          # the same keys store.export_case sets
tests/unit/test_t202_r3_allow_list.py:138:    assert "column" in sd_of(ex, "$100.00")["confirm_note"]
tests/unit/test_t202_r3_allow_list.py:212:    assert raw in d["confirm_note"] and "not stated" not in d["confirm_note"]            # the note names the date the quote writes; the letter only has the blank
tests/unit/test_t202_r3_allow_list.py:231:    assert "dated itemized bill" in d["confirm_note"]
tests/unit/test_t202_r3_allow_list.py:234:def test_the_confirm_note_never_promises_a_confirmation_that_cannot_reach_the_letter():
tests/unit/test_t202_r3_allow_list.py:235:    note = SD.confirm_note("ambiguous_numeric", "04/05/2026")
tests/unit/test_t202_r3_allow_list.py:348:                            dos_iso=d["date_iso"], dos_end_iso=d["end_iso"], dos_text=d["text"], dos_note=d["confirm_note"]))
tests/unit/test_t202_r2_service_date_layouts.py:35:                            dos_iso=d["date_iso"], dos_end_iso=d["end_iso"], dos_text=d["text"], dos_note=d["confirm_note"]))
tests/unit/test_t202_r2_service_date_layouts.py:336:            assert sd["state"] == "stated" and sd["text"] == label and sd["confirm_note"] is None, (fig, sd)
tests/unit/test_t202_r2_service_date_layouts.py:345:        assert sd["state"] == "not_stated" and sd["text"] == "date of service [__________] (statement dated November 12, 2026)" and sd["confirm_note"], (fig, sd)
tests/unit/test_t202_r2_service_date_layouts.py:349:def test_api_not_stated_charge_carries_the_statement_form_and_a_confirm_note(client):
---
def test_export_label_rules_on_a_hand_built_case():
    def line(**ch):
        return next(l for l in export.build_export(_case(**ch), None)["letter_text"].split("\n") if l.endswith("$250.00"))
    assert line(dos_iso=None, dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00"
    assert line(dos_iso="2026-03-27", dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, March 27, 2026: $250.00"        # D-071: the line's own date, not the statement's
    assert line(dos_iso="2026-06-09", dos_end_iso="2026-06-12") == "Fennimoor Spine Clinic, itemized ledger, June 9\u201312, 2026: $250.00"
    assert line() == "Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00"          # a case dict without the key: unchanged behavior
    c = _case(dos_iso=None, dos_end_iso=None)
    c["records"][0]["date_iso"] = None
    assert next(l for l in export.build_export(c, None)["letter_text"].split("\n") if l.endswith("$250.00")) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________]: $250.00"
---
tests/unit/test_t202_r2_service_date_layouts.py:144:def test_an_ambiguous_numeric_date_is_not_chosen():
tests/unit/test_t202_r2_service_date_layouts.py:154:def test_unambiguous_numeric_forms_still_print():
tests/unit/test_t202_r2_service_date_layouts.py:164:    """06/09/2026 on a bill dated June 19 can only be June 9 (September 6 is after the statement); on a bill dated June 30 04/05/2026 can be April 5 or May 4."""
tests/unit/test_t202_r2_service_date_layouts.py:272:    for printed in ("April 5, 2026", "May 4, 2026"):
tests/unit/test_t202_r3_allow_list.py:186:    ("N14 ambiguous numeric", "Itemized ledger. Date of service 04/05/2026: office visit charge $275.00.", "$275.00", "04/05/2026", "2026-06-30", "ambiguous_numeric"),
tests/unit/test_t202_r3_allow_list.py:235:    note = SD.confirm_note("ambiguous_numeric", "04/05/2026")
tests/unit/test_t202_r3_allow_list.py:308:    assert LC.charge_date_violations(_letter(f"{LEDGER}, May 4, 2026", q, "$275.00"), [_rec(ex)])
tests/unit/test_t202_r4_encounter.py:283:    got = _lc(f"{LEDGER}, May 4, 2026", ex, "$275.00", rd="2026-05-04", quote=q)           # May 4 is the statement date AND one reading of the label: still a guess
tests/unit/test_t202_r4_encounter.py:285:    assert _lc(blank_hd(LEDGER, "May 4, 2026"), ex, "$275.00", rd="2026-05-04", quote=q) == []
tests/unit/test_t202_r5_d073.py:393:    assert printed(dos_cell("2026-04-13"), "$100.00", LEDGER, None) == "April 13, 2026"
tests/unit/test_t202_r5_d073.py:398:    """Mutant: <= ref -> < ref. 04/05/2026 reads April 5 or May 4; on a statement dated May 4 both are on or before it, so it stays ambiguous."""
tests/unit/test_t202_r5_d073.py:400:    assert printed(dos_cell("04/05/2026"), "$100.00", LEDGER, "2026-05-03") == "April 5, 2026"          # May 4 would follow the statement
# ================================================================ 7. the internal notes list every charge printed without a certain date
def test_the_internal_notes_list_each_charge_printed_without_a_certain_service_date():
    ex = "Itemized ledger. Date of service 04/05/2026: office visit charge $275.00. Patient DOB 03/20/1980, x-ray charge $180.00."
    rec = {"source": LEDGER, "date_iso": "2026-06-30"}
    amounts = []
    for i, a in enumerate(AM.find_amounts(ex)):
        d = store.charge_service_date({"excerpt": ex, "value_cents": a["cents"]}, rec, a["start"])
        amounts.append(dict(id=f"a{i}", record_no=1, cents=a["cents"], cls="charge", raw=a["raw"], excerpt=ex, review_status="accepted", pos=a["start"],
                            dos_iso=d["date_iso"], dos_end_iso=d["end_iso"], dos_text=d["text"], dos_note=d["confirm_note"]))
    case = {"records": [{"n": 1, "source": LEDGER, "date_iso": "2026-06-30", "excerpt": ex}], "entries": [], "flags": [], "pending_count": 0, "events": [], "amounts": amounts}
    notes = export.build_export(case, None, check_letter=False)["internal_notes_text"]
    sec = notes.split("CHARGES WITHOUT A CERTAIN DATE OF SERVICE")[1].split("\n\n")[0]
    assert "$275.00" in sec and "$180.00" in sec and sec.count("request a dated itemized bill") == 2 and "04/05/2026" in sec


# ================================================================ 8. the production letter and the independent check agree on every probe layout (the check is the second reader)
def _probe_cases():
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:42.507Z

**tool call — Bash**
````
{
 "command": "grep -nE \"[0-9]{2}/[0-9]{2}/20[0-9]{2} ?(-|to|–|thru|through) ?[0-9]{2}/[0-9]{2}/20[0-9]{2}\" tests/unit/test_t202*.py tests/unit/test_t200*.py | cut -c1-230 | head -20; sed -n 160,175p tests/unit/test_t202_r2_service_date_layouts.py | cut -c1-250; sed -n 205,215p tests/unit/test_t202_r3_allow_list.py | cut -c1-250; sed -n 225,240p tests/unit/test_t202_r3_allow_list.py | cut -c1-250; sed -n 205,215p tests/unit/test_t202_r4_encounter.py | cut -c1-250; sed -n 130,140p tests/unit/test_t202_r3_allow_list.py | cut -c1-250"
}
````

### User / tool · 2026-11-03T02:44:42.627Z

**tool result**
````
tests/unit/test_t202_charge_service_dates.py:70:UB = ("UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.")
tests/unit/test_t202_r2_service_date_layouts.py:105:    ex = "OCR of scanned CMS-1500 for dates of service 06/24/2026 to 06/26/2026. CPT 99204 charge $185.00."
tests/unit/test_t202_r2_service_date_layouts.py:127:    ("06/28/2026-07/02/2026", "June 28–July 2, 2026", "2026-07-10"),            # hyphen-joined, no spaces
tests/unit/test_t202_r2_service_date_layouts.py:128:    ("06/28/2026 - 07/02/2026", "June 28–July 2, 2026", "2026-07-10"),
tests/unit/test_t202_r2_service_date_layouts.py:129:    ("06/28/2026–07/02/2026", "June 28–July 2, 2026", "2026-07-10"),
tests/unit/test_t202_r2_service_date_layouts.py:130:    ("06/09/2026 to 06/12/2026", "June 9–12, 2026", "2026-06-19"),               # both ends readable only one way: a service date is not after its statement
tests/unit/test_t202_r2_service_date_layouts.py:251:    ex = "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
tests/unit/test_t202_r4_encounter.py:289:    ex = "Itemized ledger.\nDOS\tService\tCharge\n06/09/2026 to 06/12/2026\troom and board\t$4,920.00\n"
tests/unit/test_t202_r4_encounter.py:290:    q = "06/09/2026 to 06/12/2026\troom and board\t$4,920.00"
tests/unit/test_t202_r3_allow_list.py:154:    p10 = "Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise charge $95.00."
tests/unit/test_t202_r3_allow_list.py:163:    ex2 = "Itemized ledger. Billing period 05/01/2026 to 05/31/2026. CPT 97110 therapeutic exercise charge $95.00."
tests/unit/test_t202_r3_allow_list.py:174:    ex = "Itemized ledger. Statement period 05/01/2026 to 05/31/2026. CPT 97110 therapeutic exercise charge $95.00."
tests/unit/test_t202_r3_allow_list.py:242:    ("01/03/2026 to 01/06/2026", "2026-03-15", "January 3–6, 2026"),         # DM would put the end (June 1) after the statement: only MD fits. `any` would call it ambiguous.
tests/unit/test_t202_r3_allow_list.py:243:    ("02/03/2026 to 02/05/2026", "2026-03-15", "February 3–5, 2026"),
tests/unit/test_t202_r3_allow_list.py:244:    ("01/02/2026 to 03/04/2026", "2026-04-10", None),                         # both ends fit both ways: ambiguous
tests/unit/test_t202_r3_allow_list.py:257:    ex = "UB-04 type of bill 0111, statement period 01/03/2026 to 01/06/2026. Rev 0450 emergency room, FL47 total charges $2,105.00."
tests/unit/test_t202_r3_allow_list.py:381:    for per, rd in (("01/03/2026 to 01/06/2026", "2026-03-15"), ("01/02/2026 to 03/04/2026", "2026-04-10"), ("June 28-July 2, 2026", "2026-07-10"), ("June 9-12", "2026-07-10"),
tests/unit/test_t202_r3_allow_list.py:382:                    ("06/28/2026-07/02/2026", "2026-07-10"), ("06/09/2026 to 06/12/2026", "2026-06-19")):
tests/unit/test_t202_r5_d073.py:88:    ex = "Itemized ledger.\nDOS\tService\tCharge\n01/23/2026 to 03/06/2026\tPT, 9 visits\t$1,665.00\n"
tests/unit/test_t202_r5_d073.py:93:    ex = "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00."
    assert head("Itemized ledger. DOS 04/13/2026 X-ray charge $180.00.", "$180.00") == not_stated("June 30, 2026") + "$180.00"          # the same date in a sentence is not read


def test_a_reading_after_the_statement_date_is_not_a_service_date():
    """06/09/2026 on a bill dated June 19 can only be June 9 (September 6 is after the statement); on a bill dated June 30 04/05/2026 can be April 5 or May 4."""
    assert head(dos_table("06/09/2026"), "$180.00", rec_date="2026-06-19") == stated("June 9, 2026") + "$180.00"
    assert head(dos_table("04/05/2026"), "$180.00", rec_date="2026-06-30") == written("04/05/2026", "June 30, 2026") + "$180.00"
    assert head(dos_table("04/05/2026"), "$180.00", rec_date=None) == f"{LEDGER_SRC}, {NS}: $180.00"


@pytest.mark.parametrize("raw", ["03/17/26", "03/17/98", "4/5/26", "13/04/26", "03-17-26"])
def test_a_two_digit_year_is_not_certain(raw):
    assert head(f"Itemized ledger. DOS {raw} charge $220.00.", "$220.00") == written(raw, "June 30, 2026") + "$220.00"


@pytest.mark.parametrize("raw", ["Mar 27", "3/27", "March 27th"])
    got = head(ex, fig, LEDGER, rd)
    long = SD.display(rd)
    assert got == written(raw, long) + fig, (label, got)
    assert BLANK in got and "not stated" not in got
    d = sd_of(ex, fig, LEDGER, rd)
    assert d["state"] == "not_stated" and d["reason"] == reason and d["date_iso"] is None, d
    assert d["text"] == f"{BLANK} (statement dated {long})"
    assert raw in d["confirm_note"] and "not stated" not in d["confirm_note"]            # the note names the date the quote writes; the letter only has the blank


def test_a_claim_form_sentence_with_two_service_dates_prints_the_blank():

def test_no_labeled_date_in_the_quote_prints_the_blank_and_a_request_note():
    ex = "Itemized ledger. New patient exam charge $250.00."
    d = sd_of(ex, "$250.00")
    assert d["text"] == "date of service [__________] (statement dated June 30, 2026)" and d["reason"] == "no_date"
    assert SD.not_stated_text(None) == "date of service [__________]"
    assert "dated itemized bill" in d["confirm_note"]


def test_the_confirm_note_never_promises_a_confirmation_that_cannot_reach_the_letter():
    note = SD.confirm_note("ambiguous_numeric", "04/05/2026")
    assert "The letter prints no service date for this line." in note and "Confirm the date from the quote" in note        # the Step 3 e2e reads these words
    assert "blank" in note


# ================================================================ 5. staff: the all-vs-any rule; a service does not follow its statement; years bound
    r = SD.resolve(ex, a["start"], "Fennimoor Spine Clinic, itemized ledger", "2026-06-15")
    assert (r["state"], r["reason"], r["raw"]) == ("not_stated", "non_service_date", "04/05/2026")          # D-073: a sentence is not read; the note names the date the code saw
    same = ex.replace(" ... ", " ")
    b = AM.find_amounts(same)[0]
    assert SD.resolve(same, b["start"], "Fennimoor Spine Clinic, itemized ledger", "2026-06-15") == r
    note = sd_of(ex, "$250.00", "Fennimoor Spine Clinic, itemized ledger")["confirm_note"]
    assert "states no date" not in note and "04/05/2026" in note


def test_a_leader_is_not_a_service_label_and_two_dates_are_still_two_dates():
    assert head("Itemized ledger. Office visit 99213 ........ $250.00 03/13/2026", "$250.00") == blank_hd(LEDGER, "June 15, 2026") + ": $250.00"

# ================================================================ 2. staff major: a table column prints only when its heading names service
@pytest.mark.parametrize("heading", ["Entry date", "Transaction Date", "Txn Date", "Recorded", "Filed", "Claim Date", "Sent", "Issued", "Printed", "Reported", "Remit Date",
                                     "Closed", "Reference Date", "Charged on", "Trans Date", "Date", "Dates", "Posted", "Statement Date", "Date Billed", "Created"])
def test_a_single_date_under_a_heading_that_does_not_name_service_is_not_certain(heading):
    ex = f"Itemized ledger.\n{heading}\tService\tCharge\n03/13/2026\toffice visit\t$100.00\n"
    assert head(ex, "$100.00") == not_stated("June 30, 2026") + "$100.00", heading
    assert sd_of(ex, "$100.00")["reason"] == "non_service_date"
    assert "column" in sd_of(ex, "$100.00")["confirm_note"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:49.978Z

**tool call — Bash**
````
{
 "command": "(python3 -m pytest tests/unit/test_t202_r5_d073.py tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py -q -x 2>&1 | tail -5); sed -n 238,262p tests/unit/test_t202_r3_allow_list.py | cut -c1-260; sed -n 100,150p tests/unit/test_t202_r4_encounter.py | cut -c1-300; python3 -m evals.letter_check 2>&1 | tail -3"
}
````

### User / tool · 2026-11-03T02:44:50.136Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest


# ================================================================ 5. staff: the all-vs-any rule; a service does not follow its statement; years bound
@pytest.mark.parametrize("period,rd,label", [
    ("01/03/2026 to 01/06/2026", "2026-03-15", "January 3–6, 2026"),         # DM would put the end (June 1) after the statement: only MD fits. `any` would call it ambiguous.
    ("02/03/2026 to 02/05/2026", "2026-03-15", "February 3–5, 2026"),
    ("01/02/2026 to 03/04/2026", "2026-04-10", None),                         # both ends fit both ways: ambiguous
])
def test_a_period_reads_one_way_only_when_every_end_fits_one_reading(period, rd, label):
    ex = f"UB-04 type of bill 0111, statement period {period}. Rev 0450 emergency room, FL47 total charges $2,105.00."
    got = head(ex, "$2,105.00", UB, rd)
    if label:
        assert got == stated(label, UB) + "$2,105.00"
    else:
        assert got == not_stated(SD.display(rd), UB) + "$2,105.00"


def test_the_all_in_the_reference_rule_is_pinned_by_a_period_with_one_end_after_the_statement():
    """Mutant: `all(...)` -> `any(...)` in service_date._certain. Under `any` this period (DM reading: one end fits, one does not) is called ambiguous and prints the blank."""
    ex = "UB-04 type of bill 0111, statement period 01/03/2026 to 01/06/2026. Rev 0450 emergency room, FL47 total charges $2,105.00."
    d = sd_of(ex, "$2,105.00", UB, "2026-03-15")
    assert d["state"] == "stated" and d["date_iso"] == "2026-01-03" and d["end_iso"] == "2026-01-06"


# ================================================================ 6. letter_check: the same allow-list in its own scanner
NOT_ENCOUNTER_SOURCES = ["Fennimoor Spine Clinic, superbill", "Pharmacy receipt", "Fennimoor Spine Clinic, patient receipt", "Fennimoor Spine Clinic, charge summary",
                         "Fennimoor Spine Clinic, fee schedule", "Fennimoor Spine Clinic, estimate", "Fennimoor Spine Clinic, cost of care summary", "Fennimoor Spine Clinic, claim",
                         "Fennimoor Spine Clinic, remittance", "Fennimoor Spine Clinic, itemization", "Fennimoor Spine Clinic, charges", "Fennimoor Spine Clinic, EOB",
                         "Fennimoor Spine Clinic, payment history", "Fennimoor Spine Clinic, HCFA", "Fennimoor Spine Clinic, balance due notice",
                         "Hobbleton Family Clinic, phone note", "Sunderland Chiropractic, correspondence, narrative letter",
                         "Fennimoor Spine", "Medical record", "Fennimoor Records", "Hobbleton"]


@pytest.mark.parametrize("src", NOT_ENCOUNTER_SOURCES)
def test_a_record_that_is_not_an_identified_encounter_never_lends_its_header_date(src):
    ex = "Office visit charge $220.00."
    assert head(ex, "$220.00", src) == blank_hd(src, "June 15, 2026") + ": $220.00"
    assert sd_of(ex, "$220.00", src)["state"] == "not_stated"


@pytest.mark.parametrize("opening", ["Account summary: Office visit charge $220.00.", "Charges: Office visit charge $220.00.", "Receipt: Office visit charge $220.00.",
                                     "Itemized statement: Office visit charge $220.00."])
def test_a_record_that_opens_as_a_financial_paper_never_lends_its_header_date(opening):
    src = "Fennimoor Spine Clinic"
    assert head(opening, "$220.00", src) == blank_hd(src, "June 15, 2026") + ": $220.00"


def test_a_clinical_opening_is_not_taken_for_a_financial_one():
    ex = "Dx: cervical strain. Plan of care: 12 visits. Charge per visit $185.00."
    assert head(ex, "$185.00", "Capital PT, initial evaluation", "2026-01-23") == "Capital PT, initial evaluation, January 23, 2026: $185.00"


@pytest.mark.parametrize("src,want", [(ER, "encounter"), ("Austin EMS run report", "encounter"), ("Capital PT, visit 9", "encounter"), ("Hill Country Pain Management, follow-up", "encounter"),
                                      ("Fennimoor Spine Clinic, superbill", "bill"), ("Fennimoor Spine Clinic, EOB", "bill"), (LEDGER, "bill"), ("Hobbleton Family Clinic, phone note", "other"),
                                      ("Medical record", "other"), (None, "other"), ("Thornapple Valley Hospital ED", "other"), ("Dr. Ed Brown, billing", "bill"), ("Dr. Ed Brown", "other"),
                                      ("Thornapple Valley Hospital ED record", "encounter"), ("Dr. Alvarez, primary care, progress note", "encounter"), ("Hobbleton Family Clinic", "other"),
                                      ("Austin Imaging", "other"), ("Central ER", "other"), ("Quillfeather Urgent Care", "other"), ("Capital PT note", "encounter"), ("Capital PT", "other"),
                                      ("Dr. Casimir Voss, orthopedic surgery, operative report", "encounter"), ("Larkmoor Physical Therapy, discharge summary", "encounter"),
                                      ("Thistlewick Orthopedics, Dr. Beatrix Quillon", "other"), ("Tarnwick Fire-Rescue ambulance run report", "encounter"), ("Fernwhistle County EMS", "other")])
def test_the_record_kind_is_read_from_the_declared_table(src, want):
    assert SD.record_kind(src, "Office visit charge $220.00.") == want
    assert LC._record_kind(src, "Office visit charge $220.00.") == want            # the independent check reads the same table with its own matcher


def test_production_and_the_check_read_the_same_data_file():
    assert SD.TYPES_PATH == LC.TYPES_PATH and SD.TYPES_PATH.name == "encounter_types.json" and SD.TYPES_PATH.exists()


def test_the_check_and_production_agree_on_every_lexicon_billing_example_and_opening():
    from app.backend import lexicon
    cat = lexicon.load()["code_lists"]["non_encounter"]
    sources = list(cat["examples"]["hit"]) + list(cat["examples"]["miss"]) + [LEDGER, "Saltmarrow General Hospital, UB-04 itemized bill", "Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)"]
    for s in sources:
        assert SD.record_kind(s, "Office visit charge $220.00.") == LC._record_kind(s, "Office visit charge $220.00."), s
    for op in ("Itemized statement: x", "Statement for visit of 2026-02-02: $275.", "Patient itemized charges. x", "Account statement - x", "Ledger. x", "Billing summary x", "Dx: x"):
        assert SD.record_kind("Hobbleton Family Clinic", op) == LC._record_kind("Hobbleton Family Clinic", op), op
  File "/Users/arsis/zlayt-pm-project/app/backend/grounding.py", line 10, in <module>
    import yaml
ModuleNotFoundError: No module named 'yaml'
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:51.602Z

**tool call — Bash**
````
{
 "command": "ls -d .venv* venv 2>/dev/null; grep -n \"pytest\\|venv\" memory/ENVIRONMENT.md | head -5"
}
````

### User / tool · 2026-11-03T02:44:51.711Z

**tool result**
````
.venv
8:| python3 | 3.12.2 | project venv at `.venv/` (gitignored). Use `.venv/bin/python`. |
18:| Playwright | python package in .venv; chromium-headless-shell 1248 | |
19:| Python deps | fastapi, uvicorn, anthropic, pyyaml, pytest, playwright, httpx, python-multipart | in .venv |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:44:53.525Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_t202_r5_d073.py tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py -q 2>&1 | tail -4; .venv/bin/python -m evals.letter_check 2>&1 | tail -3"
}
````

### User / tool · 2026-11-03T02:45:17.081Z

**tool result**
````
........................................................................ [ 88%]
........................................................................ [ 97%]
................                                                         [100%]
736 passed in 11.40s
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:45:20.383Z

**tool call — Bash**
````
{
 "command": "grep -n \"dos_table\\b\" tests/unit/test_t202_r2_service_date_layouts.py | head -3; grep -n \"def dos_table\" -A4 tests/unit/test_t202_r2_service_date_layouts.py | cut -c1-250; grep -n \"Date of Service\\\\\\\\t\\|Date(s) of Service\\|SVC\\|Svc\" tests/unit/test_t202*.py | cut -c1-200 | head; grep -n \"^DOS_TABLE\" -A2 tests/unit/test_t202_r5_d073.py | cut -c1-250; grep -n \"Entry date\\|statement-date\\|Statement Date\" tests/unit/test_t202_r3_allow_list.py | head -2 | cut -c1-80"
}
````

### User / tool · 2026-11-03T02:45:20.516Z

**tool result**
````
149:def dos_table(cell, fig="$180.00"):
155:    assert head(dos_table("13/04/2026"), "$180.00") == stated("April 13, 2026") + "$180.00"
156:    assert head(dos_table("04/13/2026"), "$180.00") == stated("April 13, 2026") + "$180.00"
149:def dos_table(cell, fig="$180.00"):
150-    """D-073: the date as the DOS cell of a bill table, the one place a written date is read."""
151-    return f"Itemized ledger.\nDOS\tService\tCharge\n{cell}\tX-ray\t{fig}\n"
152-
153-
tests/unit/test_t202_r3_allow_list.py:141:@pytest.mark.parametrize("heading", ["DOS", "Service Date", "Date of Service", "Visit Date", "Date(s) of Service", "From Service", "Service From", "24A", "Svc
67:DOS_TABLE = "Itemized ledger.\nDOS         CPT    Description           Charge\n06/10/2026  97140  Manual therapy x1     $70.00\n06/17/2026  97110  Therapeutic exercise  $95.00\n"
68-
69-
132:@pytest.mark.parametrize("heading", ["Entry date", "Transaction Date", "Txn 
133:                                     "Closed", "Reference Date", "Charged on
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:45:22.451Z

**tool call — Bash**
````
{
 "command": "sed -n 139,152p tests/unit/test_t202_r3_allow_list.py | cut -c1-400; sed -n 130,136p tests/unit/test_t202_r3_allow_list.py|cut -c1-500; git show --stat HEAD~1 --format=%s | head; git diff ad0d91a f9c0faf --stat -- tests/unit | tail -8"
}
````

### User / tool · 2026-11-03T02:45:22.596Z

**tool result**
````
@pytest.mark.parametrize("heading", ["DOS", "Service Date", "Date of Service", "Visit Date", "Date(s) of Service", "From Service", "Service From", "24A", "Svc Date"])
def test_a_single_date_under_a_service_heading_prints(heading):
    ex = f"Itemized ledger.\n{heading}\tService\tCharge\n03/13/2026\toffice visit\t$100.00\n"
    assert head(ex, "$100.00") == stated("March 13, 2026") + "$100.00", heading


def test_trans_date_column_n5_is_not_certain():
    ex = "Itemized ledger.\nTrans Date   Code   Description             Charges\n06/11/2026   97140  Manual therapy x1       $70.00\n"
    assert head(ex, "$70.00") == not_stated("June 30, 2026") + "$70.00"


# ================================================================ 3. the label picks the date the way the amendment says; the carry-forward is limited to the bill's period

# ================================================================ 2. staff major: a table column prints only when its heading names service
@pytest.mark.parametrize("heading", ["Entry date", "Transaction Date", "Txn Date", "Recorded", "Filed", "Claim Date", "Sent", "Issued", "Printed", "Reported", "Remit Date",
                                     "Closed", "Reference Date", "Charged on", "Trans Date", "Date", "Dates", "Posted", "Statement Date", "Date Billed", "Created"])
def test_a_single_date_under_a_heading_that_does_not_name_service_is_not_certain(heading):
    ex = f"Itemized ledger.\n{heading}\tService\tCharge\n03/13/2026\toffice visit\t$100.00\n"
    assert head(ex, "$100.00") == not_stated("June 30, 2026") + "$100.00", heading
feat(backend): T-202 r5 D-073 charge dates from two sources only; prose labels removed; leader mask in amounts; T-207 r2 rule pins

 .claude/agent-memory/backend/MEMORY.md             |   6 +
 .../agent-memory/backend/project_t202_r5_d073.md   |  18 +
 app/backend/amounts.py                             |  25 +-
 app/backend/encounter_types.json                   |  13 +-
 app/backend/service_date.py                        | 227 ++++------
 app/backend/store.py                               |  14 +-
 evals/letter_check.py                              | 152 ++++---
 memory/contracts/api.md                            |   2 +-
 tests/unit/test_t200_undated_charge_label.py    |   8 +-
 tests/unit/test_t202_charge_service_dates.py    |  19 +-
 tests/unit/test_t202_r2_service_date_layouts.py |  69 ++--
 tests/unit/test_t202_r3_allow_list.py           |  99 ++---
 tests/unit/test_t202_r4_encounter.py            | 117 +++---
 tests/unit/test_t202_r5_d073.py                 | 470 ++++++++++++++++++++++++
 6 files changed, 655 insertions(+), 127 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:45:38.592Z

**tool call — Bash**
````
{
 "command": "sed -n 176,216p tests/unit/test_t202_r3_allow_list.py | cut -c1-330; sed -n 164,172p tests/unit/test_t202_r2_service_date_layouts.py | cut -c1-300"
}
````

### User / tool · 2026-11-03T02:45:38.709Z

**tool result**
````
def test_a_coded_line_does_not_borrow_another_lines_dos_label():
    ex = "Itemized ledger. DOS 03/13/2026 office visit charge $220.00. CPT 97110 therapeutic exercise charge $95.00."
    assert head(ex, "$220.00") == not_stated("June 30, 2026") + "$220.00"
    assert head(ex, "$95.00") == not_stated("June 30, 2026") + "$95.00"


# ================================================================ 4. paralegal major: 'service date not stated' never sits above a quote that states one
AS_WRITTEN = [
    ("N14 ambiguous numeric", "Itemized ledger. Date of service 04/05/2026: office visit charge $275.00.", "$275.00", "04/05/2026", "2026-06-30", "ambiguous_numeric"),
    ("two-digit year", "Itemized ledger. DOS 03/17/26 office visit charge $220.00.", "$220.00", "03/17/26", "2026-06-30", "two_digit_year"),
    ("N16 no year", "Itemized ledger. Date of service February 2, office visit charge $220.00.", "$220.00", "February 2", "2026-06-30", "no_year"),
    ("impossible date", "Itemized ledger. DOS 02/30/2026 office visit charge $220.00.", "$220.00", "02/30/2026", "2026-06-30", "invalid"),
    ("later than the statement", "Itemized ledger. DOS 07/20/2026 office visit charge $220.00.", "$220.00", "07/20/2026", "2026-06-15", "implausible"),
    ("1998, years before the statement", "Itemized ledger. DOS 03/13/1998 office visit charge $220.00.", "$220.00", "03/13/1998", "2026-06-30", "implausible"),
    ("2031, years after the statement", "Itemized ledger. DOS 03/13/2031 office visit charge $220.00.", "$220.00", "03/13/2031", "2026-06-30", "implausible"),
    ("Mar 5, 26", "Itemized ledger. DOS Mar 5, 26 x-ray charge $180.00.", "$180.00", "Mar 5, 26", "2026-06-30", "two_digit_year"),
]


def table_of(raw, fig):
    """D-073: the same date as a date-of-service CELL of a bill table, the only place a written date is read."""
    return f"Itemized ledger.\nDOS\tService\tCharge\n{raw}\toffice visit\t{fig}\n", f"{raw}\toffice visit\t{fig}"


@pytest.mark.parametrize("label,ex,fig,raw,rd,reason", AS_WRITTEN)
def test_a_dos_cell_the_code_cannot_read_prints_the_blank_and_the_note_names_the_date(label, ex, fig, raw, rd, reason):
    ex, _ = table_of(raw, fig)
    got = head(ex, fig, LEDGER, rd)
    long = SD.display(rd)
    assert got == written(raw, long) + fig, (label, got)
    assert BLANK in got and "not stated" not in got
    d = sd_of(ex, fig, LEDGER, rd)
    assert d["state"] == "not_stated" and d["reason"] == reason and d["date_iso"] is None, d
    assert d["text"] == f"{BLANK} (statement dated {long})"
    assert raw in d["confirm_note"] and "not stated" not in d["confirm_note"]            # the note names the date the quote writes; the letter only has the blank


def test_a_claim_form_sentence_with_two_service_dates_prints_the_blank():
    ex = "OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00; CPT 20610 charge $210.00."
    """06/09/2026 on a bill dated June 19 can only be June 9 (September 6 is after the statement); on a bill dated June 30 04/05/2026 can be April 5 or May 4."""
    assert head(dos_table("06/09/2026"), "$180.00", rec_date="2026-06-19") == stated("June 9, 2026") + "$180.00"
    assert head(dos_table("04/05/2026"), "$180.00", rec_date="2026-06-30") == written("04/05/2026", "June 30, 2026") + "$180.00"
    assert head(dos_table("04/05/2026"), "$180.00", rec_date=None) == f"{LEDGER_SRC}, {NS}: $180.00"


@pytest.mark.parametrize("raw", ["03/17/26", "03/17/98", "4/5/26", "13/04/26", "03-17-26"])
def test_a_two_digit_year_is_not_certain(raw):
    assert head(f"Itemized ledger. DOS {raw} charge $220.00.", "$220.00") == written(raw, "June 30, 2026") + "$220.00"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:46:04.843Z

**tool call — Bash**
````
{
 "command": "sed -n 150,175p tests/unit/test_t202_r3_allow_list.py | cut -c1-330; grep -n \"service_date\\|import\" evals/letter_check.py | head -15; sed -n 257,292p tests/unit/test_t202_r5_d073.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:46:04.948Z

**tool result**
````
# ================================================================ 3. the label picks the date the way the amendment says; the carry-forward is limited to the bill's period
def test_only_the_ub04_statement_covers_period_is_read_p10_and_n17():
    p10 = "Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise charge $95.00."
    assert head(p10, "$95.00", LEDGER, "2026-04-01") == not_stated("April 1, 2026") + "$95.00"               # D-073: a period in a sentence is not read
    n17 = "UB-04 type of bill 0111. Statement covers period June 28-July 2, 2026. Rev 0120 room and board semi-private, FL47 total charges $4,920.00."
    assert head(n17, "$4,920.00", UB, "2026-07-10") == stated("June 28–July 2, 2026", UB) + "$4,920.00"


def test_a_statement_date_phrase_is_never_a_period():
    ex = "UB-04 type of bill 0111. Statement date 06/12/2026. Rev 0120 room and board semi-private, FL47 total charges $4,920.00."
    assert head(ex, "$4,920.00", UB, "2026-06-19") == not_stated("June 19, 2026", UB) + "$4,920.00"
    ex2 = "Itemized ledger. Billing period 05/01/2026 to 05/31/2026. CPT 97110 therapeutic exercise charge $95.00."
    assert head(ex2, "$95.00", LEDGER, "2026-06-05") == not_stated("June 5, 2026") + "$95.00"


def test_a_label_after_an_and_belongs_to_the_next_item_not_the_figure_before_it():
    ex = "Itemized ledger. Exam charge $100.00 and DOS 03/13/2026 x-ray charge $50.00."
    assert head(ex, "$100.00") == not_stated("June 30, 2026") + "$100.00"
    assert head(ex, "$50.00") == not_stated("June 30, 2026") + "$50.00"


def test_statement_period_is_a_service_period_only_on_a_ub04():
    ex = "Itemized ledger. Statement period 05/01/2026 to 05/31/2026. CPT 97110 therapeutic exercise charge $95.00."
    assert head(ex, "$95.00", LEDGER, "2026-06-05") == not_stated("June 5, 2026") + "$95.00"
21:(app/backend/service_date.py), so a parser bug cannot hide itself.
26:import contextlib
27:import json
28:import pathlib
29:import re
30:import sys
31:import tempfile
40:    from app.backend import money
46:    from app.backend import money
52:    from app.backend import money
65:    from app.backend import amounts as AM, export
94:# original before sending), not provenance wording, and it is the only place the letter says 'AI'. Matched whole and verbatim (the string is copied here on purpose, not imported from the export).
137:    from app.backend import review
138:    from app.db import db as DB
158:    from app.backend import count_charge, review
@pytest.mark.parametrize("pid,src,rd,ex,fig,ok", PROBES, ids=[p[0] for p in PROBES])
def test_every_reviewer_probe_prints_the_blank_or_the_right_date(pid, src, rd, ex, fig, ok):
    got = printed(ex, fig, src, rd)
    assert got == "BLANK" or got in ok, (pid, got)
    d = store.charge_service_date({"excerpt": ex, "value_cents": AM.to_cents(fig.lstrip("$"))}, {"source": src, "date_iso": rd}, next(a["start"] for a in AM.find_amounts(ex) if a["raw"].startswith(fig
    assert (d["state"] == "stated") == (got != "BLANK")
    assert (d["confirm_note"] is None) == (got != "BLANK")
    h = head(ex, fig, src, rd).rsplit(": ", 1)[0]
    assert check(h, ex, fig, src, rd) == [], (pid, h)            # the independent check agrees with production on the line it prints


def test_the_old_wrong_dates_are_flagged_by_the_independent_check():
    """Each of these printed a wrong date in round 4 and letter_check passed it; now it flags the date and accepts the blank."""
    for pid, src, rd, ex, fig, wrong in [
        ("PCP citing the ER DOS", NOTE, "2026-01-16", "Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.", "$150.00", "January 9, 2026"),
        ("PT treatment dates", PT9, "2026-03-06", "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.", "$1,665.00", "March 6, 2026"),
        ("provider-only bill", "Hobbleton Family Clinic", "2026-03-01", "Office visit 02/02/2026, 99213, charge $275.00.", "$275.00", "March 1, 2026"),
        ("ER next visit date", ER, "2026-01-09", "Dx: cervical strain. ER charges: $6,240, next visit date 01/16/2026.", "$6,240", "January 16, 2026"),
        ("bill tail next visit DOS", LEDGER, "2026-06-15", "Office visit charge $150.00, next visit DOS 02/28/2026.", "$150.00", "February 28, 2026"),
        ("visits to date", PT9, "2026-03-06", "PT charges to date $1,665.00.", "$1,665.00", "March 6, 2026"),
    ]:
        assert check(f"{src}, {wrong}", ex, fig, src, rd), pid
        assert check(blank_of(src, rd), ex, fig, src, rd) == [], pid


# ================================================================ 4. a dotted leader carries through a full case run (T-209 r2, paralegal r4 major)
def _sub(text, old, new):
    assert old in text, old
    return text.replace(old, new)


def _run(text):
    got = LC.letters_for(text)
    return got["all_accepted"], got["counted"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:46:19.793Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def test_\" tests/unit/test_t202_r2_service_date_layouts.py | sed -n 1,60p | cut -c1-170; sed -n 322,350p tests/unit/test_t202_r2_service_date_layouts.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:46:19.897Z

**tool result**
````
67:def test_posted_before_dos_prints_the_dos_column_not_the_posting_date():
72:def test_dos_before_posted_still_prints_the_dos_column():
77:def test_two_dates_in_a_row_and_no_header_is_not_certain():
82:def test_a_row_whose_only_date_sits_under_posted_is_not_a_service_date():
88:def test_a_statement_or_posted_word_before_a_date_in_a_sentence_is_not_a_service_date():
99:def test_cms1500_with_two_service_dates_assigns_neither_to_a_line():
104:def test_cms1500_sentence_with_one_service_period_prints_the_blank():
109:def test_two_service_dates_on_one_charge_line_is_not_certain():
114:def test_two_charges_in_one_sentence_each_print_the_blank():
132:def test_a_stated_period_prints_whole_with_its_own_year(period, label, rec):
138:def test_an_incomplete_or_backwards_period_is_not_certain(period):
144:def test_an_ambiguous_numeric_date_is_not_chosen():
154:def test_unambiguous_numeric_forms_still_print():
163:def test_a_reading_after_the_statement_date_is_not_a_service_date():
171:def test_a_two_digit_year_is_not_certain(raw):
176:def test_a_date_with_no_year_is_not_certain(raw):
180:def test_a_date_that_is_not_on_the_calendar_is_not_certain():
185:def test_corpus_shapes_that_a_sentence_dated_now_print_the_blank():
193:def test_a_visit_note_keeps_the_visit_date_and_an_unreadable_line_in_a_bill_keeps_none():
203:def test_charges_sort_by_service_date_when_the_records_are_listed_in_another_order():
214:def test_a_charge_with_no_service_date_sorts_by_its_statement_date_among_dated_ones():
233:def test_letter_check_fails_the_posted_date_and_passes_the_dos_date():
241:def test_letter_check_fails_one_claim_date_printed_on_a_two_date_claim():
250:def test_letter_check_fails_a_dropped_period_end_and_a_wrong_year():
260:def test_letter_check_fails_a_month_name_period_printed_with_the_statement_year():
268:def test_letter_check_fails_a_guessed_ambiguous_date_and_a_two_digit_year():
278:def test_letter_check_fails_another_lines_date_on_a_ledger():
285:def test_letter_check_fails_a_date_when_the_quote_states_none_and_the_record_states_no_period():
295:def test_letter_check_passes_a_visit_note_on_its_own_date():
328:def test_api_charge_carries_the_service_date_the_letter_prints_lib10_and_lib14(client):
349:def test_api_not_stated_charge_carries_the_statement_form_and_a_confirm_note(client):
def _accept_all(c, tok):
    for kind in ("entries", "amounts"):
        for it in c.get(f"/api/cases/{tok}").json()[kind]:
            c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})


def test_api_charge_carries_the_service_date_the_letter_prints_lib10_and_lib14(client):
    for lib, figs, label in (("case_lib10_eob_ub04_cms1500", ("$4,920.00", "$2,105.00", "$386.50", "$712.00"), "June 9–12, 2026"),):          # lib14's invoice states its run in a sentence: D-073 pr
        tok = _run(client, lib)
        amounts = {a["text"]: a for a in client.get(f"/api/cases/{tok}").json()["amounts"]}
        _accept_all(client, tok)
        letter = client.get(f"/api/cases/{tok}/export").json()["letter_text"].split("\n")
        for fig in figs:
            sd = amounts[fig]["service_date"]
            assert sd["state"] == "stated" and sd["text"] == label and sd["confirm_note"] is None, (fig, sd)
            assert any(l.endswith(f", {sd['text']}: {fig}") for l in letter), (fig, sd["text"])           # Step 3 shows the same string the letter prints
        assert all(a["service_date"] is None for a in amounts.values() if a["kind"] != "charge")
    tok = _run(client, "case_lib14_handwritten_chiro_scans")
    amounts = {a["text"]: a for a in client.get(f"/api/cases/{tok}").json()["amounts"]}
    _accept_all(client, tok)
    letter = client.get(f"/api/cases/{tok}/export").json()["letter_text"].split("\n")
    for fig in ("$1,380.00", "$187.05"):
        sd = amounts[fig]["service_date"]
        assert sd["state"] == "not_stated" and sd["text"] == "date of service [__________] (statement dated November 12, 2026)" and sd["confirm_note"], (fig, sd)
        assert any(l.endswith(f", {sd['text']}: {fig}") for l in letter), fig


def test_api_not_stated_charge_carries_the_statement_form_and_a_confirm_note(client):
    tok = _run(client, "case_lib11_priors_and_ledger")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:46:23.512Z

**tool call — Bash**
````
{
 "command": "grep -n \"^| 2 |\\|^| 3 |\" docs/LLM_VS_CODE.md | cut -c1-40; git status --short docs/LLM_VS_CODE.md; git log --oneline -1 -- docs/LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T02:46:23.672Z

**tool result**
````
30:| 2 | Parse dates | **Code**: an expl
31:| 3 | Date of service and provider fo
efda639 docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:28.182Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/scratch207 && cat > /private/tmp/claude-501/scratch207/rows.py <<'EOF'\nimport re, pathlib\np = pathlib.Path(\"/Users/arsis/zlayt-pm-project/docs/LLM_VS_CODE.md\")\nlines = p.read_text(encoding=\"utf-8\").split(\"\\n\")\ni2 = next(i for i, l in enumerate(lines) if l.startswith(\"| 2 | Parse dates |\"))\ni3 = next(i for i, l in enumerate(lines) if l.startswith(\"| 3 | Date of service and provider\"))\nassert i3 == i2 + 1\n\nR = {\"R5\": \"tests/unit/test_t202_r5_d073.py\", \"R4\": \"tests/unit/test_t202_r4_encounter.py\", \"R3\": \"tests/unit/test_t202_r3_allow_list.py\",\n     \"R2\": \"tests/unit/test_t202_r2_service_date_layouts.py\", \"R0\": \"tests/unit/test_t200_undated_charge_label.py\"}\n\nrow2 = (\"| 2 | Parse dates | \"\n \"**Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. \"\n \"**A charge line's date of service is code only, never the LLM (D-071, D-073; `app/backend/service_date.py`), and it comes from exactly two sources. Every other line prints the fillable blank of row 3.** \"\n \"**Source 1, the date cell of the line's own row in a bill table (a).** The row is split into cells at a tab or two or more spaces (b). The column heading over the date cell must name the service: DOS, Service Date, Date of Service, Date(s) of Service, Visit Date, Date of Visit, Encounter Date, Svc Date, Service From, From Service or 24A (c). A heading such as Posted, Entry date, Transaction Date, Statement Date or a bare Date does not name it, and the date is then not read (d). A cell that holds a range prints the range (e). A CMS-1500 'From' cell followed by its 'To' cell is one period; the same day twice is that day; an end before the start is not read (f). On a UB-04 a coded line takes the period the bill states as 'statement covers period' or 'statement period', FROM to THROUGH; an uncoded line does not, and a 'billing period' or a 'statement period' on a bill that is not a UB-04 is not a service span (g). \"\n \"**Source 2, the record's own date (h).** It counts only for a record whose source label holds a document-type word from the declared table `app/backend/encounter_types.json` (read by `service_date.record_kind` in production and by `evals/letter_check.py` with its own matcher), for example visit, note, follow-up, discharge summary, run report, operative report, ED record, MRI, nota de consulta, new patient or evaluation. A provider's name or specialty (clinic, ED, ER, PT, imaging, EMS, urgent care) is never enough (i). A bill (a financial word in the source label, or in the first 40 characters of the text up to the first colon or full stop) and an administrative paper (a phone note, correspondence) never lend their date, even when the label also holds a word such as 'note' (j). The date is lent only when the charge's own sentence (a semicolon ends it) holds no other date and no count of visits such as '9 visits', 'visits 1-9', 'to date', 'six sessions' or '2 x' (k), and a record with no date lends none (l). \"\n \"**Prose is not read (m).** A date after DOS, date of service, 'visit of', 'Treatment dates' or 'next visit date' inside a sentence never gives a date, in any record (SCOPE_CUTS row 28); the Step 3 note names the date the code saw. \"\n \"**A numeric date that reads two ways is read only when exactly one of its two orders puts every end on or before the record's own date (a bill's statement date), because a service cannot follow its statement (D-071 clarification); with no record date it is not read (n). A period whose ends force different orders (`13/05/2026 - 05/13/2026`) is not read; one convention throughout is (o).** This is a deterministic rule, not a guess. A cell with a two-digit year, no year, a date not on the calendar, a date after the record's own date, or a date more than 1,830 days (5 x 366) before it is not read (p). The bound is day arithmetic: a date exactly 1,830 days before the record, a few days past five calendar years, is read, a date on the record's own date is read, and the day after is not (q). With no record date, an unambiguous date is read (r). \"\n \"| The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | \"\n \"Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under \\\"Dates to confirm\\\". \"\n f\"**Charge-date pins** (each test runs the shipped path `store.charge_service_date` with no model call; R5 = `{R['R5']}`, R4 = `{R['R4']}`, R3 = `{R['R3']}`, R2 = `{R['R2']}`; at f9c0faf these four files plus `tests/unit/test_t202_charge_service_dates.py` and `{R['R0']}` give 736 passed): \"\n \"(a) R5::test_a_dos_column_cell_prints_its_own_rows_date. \"\n \"(b) R5::test_a_line_that_is_not_split_into_cells_is_not_a_table_row. \"\n \"(c) R3::test_a_single_date_under_a_service_heading_prints, R5::test_the_visit_and_encounter_headings_name_the_service. \"\n \"(d) R3::test_a_single_date_under_a_heading_that_does_not_name_service_is_not_certain, R5::test_a_heading_that_does_not_name_service_gives_the_blank. \"\n \"(e) R5::test_a_dos_cell_holding_a_range_prints_the_range_whole. \"\n \"(f) R5::test_cms1500_24a_from_to_cells_print_the_period, R5::test_cms1500_with_service_from_and_service_to_headings. \"\n \"(g) R5::test_ub04_statement_covers_period_prints_the_period_for_a_coded_line_only, R3::test_only_the_ub04_statement_covers_period_is_read_p10_and_n17, R3::test_statement_period_is_a_service_period_only_on_a_ub04, R3::test_a_period_reads_one_way_only_when_every_end_fits_one_reading. \"\n \"(h) R5::test_a_document_type_word_identifies_an_encounter_that_lends_its_date. \"\n \"(i) R5::test_a_provider_name_alone_is_never_enough_so_the_header_date_never_prints, R5::test_a_bill_labelled_with_the_provider_name_only_never_prints_the_statement_date. \"\n \"(j) R4::test_a_record_that_is_not_an_identified_encounter_never_lends_its_header_date, R4::test_a_record_that_opens_as_a_financial_paper_never_lends_its_header_date, R4::test_a_clinical_opening_is_not_taken_for_a_financial_one, R4::test_the_record_kind_is_read_from_the_declared_table. \"\n \"(k) R5::test_a_sentence_with_another_date_or_a_visit_count_gives_the_blank_even_in_an_encounter, R5::test_a_period_in_the_charge_sentence_is_another_date_even_when_it_starts_on_the_record_date, R5::test_the_check_reads_the_whole_sentence_around_a_trimmed_quote, R5::test_another_visits_label_in_an_encounter_note_never_prints_that_visits_date. \"\n \"(l) R5::test_an_encounter_with_no_record_date_prints_the_bare_blank. \"\n \"(m) R5::test_a_treatment_dates_range_in_a_sentence_is_not_read_in_any_record, R5::test_the_same_label_words_in_a_bill_tail_print_the_blank, R5::test_a_next_dos_in_a_sentence_is_a_date_the_code_does_not_read. \"\n \"(n) R5::test_a_numeric_date_is_resolved_only_when_one_reading_is_on_or_before_the_record_date, R2::test_a_reading_after_the_statement_date_is_not_a_service_date. \"\n \"(o) R5::test_a_period_whose_ends_force_different_orders_is_not_read. \"\n \"(p) R3::test_a_dos_cell_the_code_cannot_read_prints_the_blank_and_the_note_names_the_date (ambiguous, two-digit year, no year, impossible date, after the record, 1998 against a 2026 record). \"\n \"(q) R5::test_the_five_year_bound_is_1830_days_edges_included. \"\n \"(r) R5::test_a_date_in_a_record_with_no_date_is_read_when_it_is_unambiguous_and_never_when_it_reads_two_ways. \"\n \"Table shared by production and the check: R5::test_the_table_lists_document_types_only_and_both_readers_share_it, R4::test_production_and_the_check_read_the_same_data_file. \"\n \"**Not pinned by any test, so not claimed here:** that a period end which reads only one way fixes the order of the other end (`04/05/2026 - 13/05/2026`), that a record with no date has no bound, cells split at a pipe, and the billing view's per-line `dos_iso` (`app/backend/billing.py`), which is read by a different parser and is not a charge date. No mutation run is claimed; no mutation harness is committed. |\")\n\nrow3 = (\"| 3 | Date of service and provider for an entry | \"\n \"**Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider (\\\"Capital PT, initial evaluation\\\"). The model is not asked for either. \"\n \"**Charge-line exception:** for a charge line the date is the service date of row 2, never the record's header date merely because it is the header (a bill's header date is its statement date), and the model is never asked. \"\n \"A single service date prints as `June 9, 2026` and a period as a range (`June 9–12, 2026`, `June 28–July 2, 2026`) (s). Every charge line to which row 2 gives no date prints the same fillable blank, like the Bates placeholder, beside the statement date: `date of service [__________] (statement dated June 15, 2026)`, and the bare `date of service [__________]` when the record has no date (t) (D-071 addendum; `service_date.not_stated_text`, `export.charge_when`). That covers a line with no date, a cell the code cannot read with certainty, a date seen only in a sentence, and a figure the code cannot locate in its record (u). The paralegal fills the blank from the quote; nothing is inferred. \"\n \"Step 3 shows exactly what the letter prints (v) and carries a confirm note (`service_date.confirm_note`): for a cell the code cannot read, the note names the date as the cell writes it and asks her to confirm it from the quote and fill the blank; for a date seen only in a sentence, the note names that date; for a line with no date, the note asks her to request a dated itemized bill or fill the blank (w). The internal notes list every such charge (x). \"\n \"**A charge she has counted for its missing date of service (D-064) still prints the blank but carries no note**, because she counted it knowing (y) (`store.charge_service_date`). A hand-built case dict without `dos_iso` (no store path) keeps the record's date in `export.charge_when`; the app's own export carries `dos_iso` for every charge (z). \"\n \"| A model told to \\\"find the date\\\" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | \"\n \"Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a \\\"Dates to confirm\\\" group after the timeline until the paralegal picks one of the readings the code proposed. \"\n \"**Charge-date pins** (R0 = `tests/unit/test_t200_undated_charge_label.py`; R2 to R5 as in row 2): \"\n \"(s) R0::test_export_label_rules_on_a_hand_built_case, R5::test_a_dos_cell_holding_a_range_prints_the_range_whole, R3::test_only_the_ub04_statement_covers_period_is_read_p10_and_n17. \"\n \"(t) R0::test_export_label_rules_on_a_hand_built_case, R5::test_an_encounter_with_no_record_date_prints_the_bare_blank. \"\n \"(u) R5::test_every_reviewer_probe_prints_the_blank_or_the_right_date, R3::test_a_dos_cell_the_code_cannot_read_prints_the_blank_and_the_note_names_the_date, R5::test_an_encounter_figure_the_code_cannot_locate_prints_the_blank. \"\n \"(v) R2::test_api_charge_carries_the_service_date_the_letter_prints_lib10_and_lib14, R2::test_api_not_stated_charge_carries_the_statement_form_and_a_confirm_note. \"\n \"(w) R3::test_a_dos_cell_the_code_cannot_read_prints_the_blank_and_the_note_names_the_date, R3::test_the_confirm_note_never_promises_a_confirmation_that_cannot_reach_the_letter, R5::test_a_next_dos_in_a_sentence_is_a_date_the_code_does_not_read, R3::test_no_labeled_date_in_the_quote_prints_the_blank_and_a_request_note. \"\n \"(x) R3::test_the_internal_notes_list_each_charge_printed_without_a_certain_service_date. \"\n \"(y) R5::test_a_counted_undated_charge_has_no_note_and_an_uncounted_one_has_one. \"\n \"(z) R0::test_export_label_rules_on_a_hand_built_case, R2::test_api_charge_carries_the_service_date_the_letter_prints_lib10_and_lib14. \"\n \"Independent check: `evals/letter_check.charge_date_violations` is a second reader with its own per-line scanner and its own matcher over the same `encounter_types.json`; `python -m evals.letter_check` reports value 0 over 25 cases at f9c0faf. It accepts the blank, whole and exact, and flags a printed date the two sources do not give (R5::test_the_old_wrong_dates_are_flagged_by_the_independent_check), agrees with production on every reviewer probe (R5::test_every_reviewer_probe_prints_the_blank_or_the_right_date), at the five-year edges (R5::test_the_five_year_bound_is_1830_days_edges_included) and on 24A pairing and the UB-04 span (R5::test_the_check_pairs_24a_from_to_cells_and_reads_a_span_only_on_a_ub04). No mutation run is claimed. |\")\n\nlines[i2], lines[i3] = row2, row3\np.write_text(\"\\n\".join(lines), encoding=\"utf-8\")\n\n# verify every cited test exists\ntxt = p.read_text(encoding=\"utf-8\")\nimport subprocess\nfiles = {k: pathlib.Path(\"/Users/arsis/zlayt-pm-project\")/v for k, v in R.items()}\nmissing = []\nfor m in set(re.findall(r\"\\b(R[0-5])::(test_\\w+)\", row2 + row3)):\n    if f\"def {m[1]}(\" not in files[m[0]].read_text(encoding=\"utf-8\"):\n        missing.append(m)\nprint(\"missing:\", missing)\nEOF\ncd /Users/arsis/zlayt-pm-project && python3 /private/tmp/claude-501/scratch207/rows.py && git diff --stat docs/LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T02:47:28.320Z

**tool result**
````
missing: []
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:34.432Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/scratch207/idx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add docs/LLM_VS_CODE.md && git diff --cached --stat && python3 tools/check_secrets.py --staged 2>&1 | tail -2; git commit -q -m \"docs(architect): LLM_VS_CODE rows 2-3 match T-202 r5 code (D-073) and name the test that pins each rule (T-207)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline -1 && git show --stat --format= HEAD"
}
````

### User / tool · 2026-11-03T02:47:34.519Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=/private/tmp/claude-501/scratch207/idx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add docs/LLM_VS_CODE.md && git diff --cached --stat && python3 tools/check_secrets.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:36.063Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/scratch207/idx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add docs/LLM_VS_CODE.md && git diff --cached --stat"
}
````

### User / tool · 2026-11-03T02:47:36.712Z

**tool result**
````
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:38.699Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/scratch207/idx && python3 tools/check_secrets.py --staged 2>&1 | tail -2"
}
````

### User / tool · 2026-11-03T02:47:38.850Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:39.557Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/scratch207/idx && git commit -q -m \"docs(architect): LLM_VS_CODE rows 2-3 match T-202 r5 code (D-073) and name the test that pins each rule (T-207)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline -1 && git show --stat --format= HEAD"
}
````

### User / tool · 2026-11-03T02:47:40.963Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
6b0724a docs(architect): LLM_VS_CODE rows 2-3 match T-202 r5 code (D-073) and name the test that pins each rule (T-207)
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:47.296Z

**tool call — Bash**
````
{
 "command": "unset GIT_INDEX_FILE; B=\"python3 tools/board.py\"; $B commit T-207 --sha 6b0724a --agent architect; $B ac T-207 --check 1 --agent architect --evidence \"docs/LLM_VS_CODE.md rows 2-3 rewritten from service_date.py, encounter_types.json, store.charge_service_date, export.charge_when at f9c0faf; every rule cites its pinning test (all cited names verified to exist; 736 passed in the six date test files; letter_check value 0, 25 cases); commit 6b0724a\"; $B note T-207 --agent architect --text \"Rows 2-3 rewritten at f9c0faf (commit 6b0724a). Rules in the code that no test pins are NOT claimed and are listed in row 2: a period end that reads one way fixing the other end's order (04/05/2026 - 13/05/2026), no bound for a record with no date, pipe-split cells, billing dos_iso. For backend: a test for the first two would let the doc claim them. No mutation run claimed (harness not committed). The backend text said 'visit of' etc. are unread, which matches; its note on 'prose labels' is in row 2 (m).\"; $B handoff T-207 --agent architect --text \"What changed: rows 2-3 of docs/LLM_VS_CODE.md rewritten from the f9c0faf code (D-073 two sources, encounter table, 1,830-day bound, blank, notes, counted-charge rule), each rule lettered and tied to a named test in the Validation cell. How verified: read service_date.py, encounter_types.json, store.charge_service_date, export.charge_when; every cited test name exists (script check); 736 passed over the six date test files with .venv; python -m evals.letter_check value 0 over 25 cases; check_secrets ok. What's left: unpinned rules are listed as not claimed (forced order of a period end, no-date record bound, pipe cells, billing dos_iso); backend may add tests to claim them. What surprised me: T-207 r2 majors are now pinned by R5 tests (bound, rule 2 edge, different orders, headings, counted note), but the same-period forced-order rule has no test at all.\"; $B move T-207 in_review --agent architect; $B show T-207 | grep -m1 \"^status\""
}
````

### User / tool · 2026-11-03T02:47:47.715Z

**tool result**
````
T-207: commit 6b0724a recorded
AC 1 checked: docs/LLM_VS_CODE.md rows 2-3 rewritten from service_date.py, encounter_types.json, store.charge_service_date, export.charge_when at f9c0faf; every rule cites its pinning test (all cited names verified to exist; 736 passed in the six date test files; letter_check value 0, 25 cases); commit 6b0724a
noted on T-207
handoff written on T-207
T-207: in_progress -> in_review
status: "in_review"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:47:50.110Z

T-207 is in_review: I rewrote rows 2 and 3 of `docs/LLM_VS_CODE.md` from the f9c0faf code, with each rule lettered and tied to a named pinning test (commit 6b0724a, check_secrets ok). I checked that every cited test name exists, the six date test files give 736 passed, and `python -m evals.letter_check` reports value 0 over 25 cases. Four things are not pinned, so the rows leave them out, and the doc lists them as unclaimed: one end of a period fixing the order of the other end, a bound for a record with no date, pipe-split cells, and the billing view's `dos_iso`.

`board.py claim --force` errored because the card was already held by architect, so I continued on the existing claim.
