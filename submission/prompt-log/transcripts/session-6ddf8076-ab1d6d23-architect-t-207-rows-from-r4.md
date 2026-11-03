# Subagent: Architect: T-207 rows from r4 (Architect: T-207 rows from r4)

Source: `agent-ab1d6d23292d04d81.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:58:57.302Z

You are the architect in /Users/arsis/zlayt-pm-project on T-207. Claim it with --force. Read reviews/T-207-staff-engineer.md (5 majors), D-071 with all its amendments and notes in memory/ORCHESTRATOR_DECISIONS.md, and the exact proposed text the T-202 r4 worker left as a note on T-202.

Rewrite rows 2 and 3 of docs/LLM_VS_CODE.md so every statement matches the code at commit 8cb5bd2: app/backend/service_date.py, app/backend/encounter_types.json and app/backend/export.py. Read the code; don't rely on the notes alone. Cover all 5 majors:
- the same-period locale rule;
- the five-year bound, now applied to every record;
- the encounter-record date default;
- the counted-line note;
- the mutant count: state only what the handoff shows, or omit it.

Commit only that file through `git commit` with a temp index from the current HEAD. Move the card to in_review and reply in 1 line.

### User / tool · 2026-11-03T01:58:57.308Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:58:59.353Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B claim T-207 --agent architect --force; $B show T-207 | head -80; cat reviews/T-207-staff-engineer.md; git log --oneline | head -3"
}
````

### User / tool · 2026-11-03T01:58:59.558Z

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
updated_at: "2026-11-03T01:58:42Z"
claimed_by: "architect"
claimed_at: "2026-11-03T00:46:49Z"
rounds: 1
commits: ["901ad5a", "fc37fbc"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-207-staff-engineer.md", "at": "2026-11-03T01:43:17Z"}
ac:
  - {"n": 1, "text": "docs/LLM_VS_CODE.md row 2 and row 3 carry the text in the T-202 note from backend (allow-list, as-written form, not-stated form, validation), and say entry dates stay on the stricter ambiguous-never-guessed rule", "done": true, "evidence": "docs/LLM_VS_CODE.md rows 2 and 3, commit 901ad5a; text per T-202 note + D-071 amendment/clarification/addendum"}
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

## Handoff
What changed: LLM_VS_CODE row 2 (code-only allow-list: DOS/service column header, service label, the row's own date cell, the bill's one stated period; statement-date disambiguation 'a service cannot follow its statement'; unreadable years/dates not read; entry dates stay strict) and row 3 (charge-line exception: fillable blank + Step 3 confirm note when not certain, as-written form, 'service date not stated' form; validation cell names test_t202_r3_allow_list and letter_check.charge_date_violations). Verified: git diff shows only those 2 rows; commit 901ad5a via temp index, secrets check ok. Left: nothing in docs. Surprised me: the D-071 addendum's fillable blank ('date of service [__________] (statement dated X)') is not in the code at 5703fc4 (store.charge_service_date/service_date.printed_text print the 'as written' and 'service date not stated' forms; no card covers the blank), so the doc states the decided rule ahead of the code; backend needs a card.

# T-207 staff-engineer review, r1

Reviewer: staff-engineer-reviewer (Marcus Lee persona). Fresh context, read-only on product code. Pinned to HEAD fc37fbc (archived to a scratch copy; the product tree was not edited).

Scope: docs/LLM_VS_CODE.md rows 2 and 3 (commits 901ad5a and fc37fbc), checked against app/backend/service_date.py, app/backend/store.py charge_service_date (lines 118-147) and app/backend/export.py charge_when (lines 215-226). Rules: memory/ORCHESTRATOR_DECISIONS.md D-071 and its amendment, clarification and addendum (lines 84-93). Spec: spec/REQUIREMENTS.md R-TL-3 (lines 50 and 356).

## Answers to the four questions

1. The date is code only, never the LLM. Holds. service_date.py imports only datetime, re and app.backend.amounts (lines 22-25). The charge path (store.py:118-147, export.py:215-226, present.py:152) calls no model. evals/letter_check.py has its own scanner and does not import service_date.
2. An allow-list of positive evidence decides it. Holds for the four listed ties, with gaps. The row's column-header list is narrower than the code (F6). Two other paths decide a printed date that row 2 does not name: a same-period locale rule (F1) and the header date of a visit note (F3).
3. The statement-date disambiguation rule applies. Holds. A date that reads two ways is blank when both readings fall on or before the statement (probe P1), and a single reading is printed when the other is after it (probe P2). Mutants M1 and M2 are killed.
4. A not-certain case gets the fillable blank plus a Step 3 note. The blank holds: it matches the D-071 addendum text (probe P7). The note holds except for counted undated charges (F4), and its wording for the no-label case differs from row 3 (F7).

Verdict: changes. No blocker. Five majors, three minors. I did not downgrade any finding for convenience.

Model note: the dossier and the brief expect claude-sonnet-5-5. The model I am running as is claude-haiku-5-5, and that is the id recorded below.

## Exercised

1. git show 901ad5a and git show fc37fbc: each changes only docs/LLM_VS_CODE.md (2 lines and 1 line). git rev-parse HEAD gives fc37fbcec0ebdb7705e4d91c2ad43afd67a82568. git diff --stat HEAD -- docs/LLM_VS_CODE.md is empty, so the working copy matches HEAD.
2. git archive HEAD into a scratch copy at the pinned sha (read and run only).
3. Read rows 2 and 3 at HEAD (docs/LLM_VS_CODE.md:30-31), the D-071 block (memory/ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (spec/REQUIREMENTS.md:50, :356), and board.py show T-207 (reviews: []; commits 901ad5a, fc37fbc).
4. Read app/backend/service_date.py in full (377 lines) at HEAD. Grepped the dos_iso and dos_text writers, and the import lines of the date path.
5. pytest tests/unit -q on the HEAD archive: 6137 passed, 12 skipped (428 s).
6. pytest on the four T-202 date files (test_t202_r3_allow_list, test_t202_r2_service_date_layouts, test_t202_charge_service_dates, test_t200_undated_charge_label): 211 passed.
7. Probes P1 to P8 against the HEAD archive: artifacts/review-evidence/T-207-r1/probe_t207.py with probe_t207.out, and probe_t207_p8.py with probe_t207_p8.out.
8. Nine mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py with mutants_t207.out. Baseline 211 passed. M1, M2, M3, M5, M7 and M9 killed; M4, M6 and M8 survived.
9. letter-check eval (evals/letter_check.py main, fixture backend): artifacts/review-evidence/T-207-r1/letter_eval_t207.py with letter_eval_t207.out. Output: value 0, cases 25, exit 0.
10. grep -rn -i mutant tests/unit evals --include=*.py: 28 hits, all comments from other cards. None is a harness for the date resolver's 24 mutants.

## Findings

F1 (major). Row 2 says a two-reading date is certain "only when" the statement rule decides it. The code also settles an end from the other end's order inside the same period. Probe P3, input "DOS 04/05/2026 - 13/05/2026 therapy $120.00." with statement 2026-06-30, prints "stated | 2026-05-04 | 2026-05-13". The row says that case is ambiguous and prints the blank. The code path is service_date.py:215-217 (if determined: order = next(iter(determined))). It is pinned by tests/unit/test_t202_r2_service_date_layouts.py:129 (mutant M3 is killed by it). D-071's amendment (memory/ORCHESTRATOR_DECISIONS.md:87) mentions "no locale rule from the record", so a locale rule is contemplated, but the table does not state it. Not a blocker: the rule is deterministic, tested, and uses the record's own other end.

F2 (major). Row 2 says a bill date "more than five years before it is not read". The code allows 1830 days (service_date.py:55 _YEARS_BEFORE = 5; :274 days=366 * _YEARS_BEFORE). Probe P4 with statement 2026-06-30: "P4 06/29/2021 | $120.00 | stated | 2021-06-29" (five years and one day before) and "P4 06/26/2021 | $120.00 | stated | 2021-06-26" (five years and four days before). The day 06/25/2021 is refused as implausible. Mutant M4 (calendar-exact bound 365*5+1) survives all 211 tests. The only bound tests are 1998 and 2031 (tests/unit/test_t202_r3_allow_list.py:187-188). Persona calibration: a missing boundary test is major.

F3 (major). A charge with no labeled service date takes the visit note's header date. Probe P5: "Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain." on a progress note dated 2026-01-09 prints "stated | 2026-01-09 | text='January 9, 2026'". Probe P8 shows the same default when the figure offset cannot be located (store.py:133-136 falls back to the header date for a non-bill record; a ledger prints the blank). The default is at service_date.py:375-376 and is pinned by test_t202_r3_allow_list.py:98 (mutant M7 killed). Row 2 says "Only a date tied to the line by" four listed ties counts, and row 3 says the header date is not the DOS "for a bill". Spec R-TL-3 (spec/REQUIREMENTS.md:50) says "Date of service is the record's header date, parsed by code", so the code follows the spec and the table is incomplete. Persona §5 would treat a silent default as a blocker. I do not rate it one because the spec authorizes the header date, no fact is invented, and nothing is hidden. The defect is that the table says otherwise. Chris must rule (Q1).

F4 (major). A counted undated charge gets no Step 3 note. Probe P6, counted via D-064 ("Count this charge"), prints "not_stated | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None". The uncounted line (P6-uncounted) gets a note. The suppression is store.py:139 (if not stated and not counted_undated:), and mutant M6 survives. Row 3 (docs/LLM_VS_CODE.md:31) says "Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it". The brief also requires a note for every not-certain case. The blank still prints in the letter, so nothing is invented or lost. Major, not blocker.

F5 (major). The row 3 Validation cell says "24 mutants of the resolver and the check all fail the unit suite" (docs/LLM_VS_CODE.md:31). Two resolver mutants survive the 211-test date suite: M4 (five-year bound, service_date.py:274) and M8 (the "Encounter date" heading, service_date.py:53). The count of 24 cannot be reproduced: no harness exists in the repo (item 10 above). The claim is refuted, so it is a finding.

F6 (minor). Row 2 lists "a DOS or service column header". The code's heading set (service_date.py:53-54) also accepts Visit Date, Date of Visit, Encounter Date, SVC and 24A. Encounter Date has no test (M8 survives). Fix: list the set in row 2 and test it.

F7 (minor). Row 3 says the note asks the paralegal to "read the date from the quote" and "names the date as the quote writes it". That holds for the written-date reasons (service_date.py:102). For the no-label reason the note says "Request a dated itemized bill, or fill the blank from the record" and names no date (service_date.py:103; probe P7b). Fix: align the row or the note.

F8 (minor). billing.py:141 (_dos, via dates.parse_date) and billing.py:339 emit a per-line dos_iso served at GET /api/cases/{token}/billing (billing.py:1062, registered at api.py:599). This is a second date-of-service derivation outside row 2's "only" claim. It does not reach the letter (dos_iso writers listed in item 4) and I found no frontend consumer. Fix: say in row 2 that it is not a charge date, or remove it.

## What is right

1. The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.
2. The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.
3. The blank matches the D-071 addendum text exactly ("date of service [__________] (statement dated June 30, 2026)", probe P7), and letter_check reports value 0 over 25 cases.

Outside my lens: the wording of Step 3 UI copy beyond the note strings, and the legal weight of the blank.

```json
{"card": "T-207", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "docs/LLM_VS_CODE.md rows 2-3 at HEAD fc37fbc (commits 901ad5a, fc37fbc); app/backend/service_date.py, app/backend/store.py:118-147, app/backend/export.py:215-226; memory/ORCHESTRATOR_DECISIONS.md D-071 lines 84-93; spec/REQUIREMENTS.md R-TL-3; no app URL exercised",
 "exercised": ["git show 901ad5a and fc37fbc (docs only); git rev-parse HEAD = fc37fbcec0eb; git diff --stat HEAD -- docs/LLM_VS_CODE.md empty",
               "git archive HEAD into scratch copy head-fc37fbc (pinned, read and run only)",
               "read rows 2-3 (docs/LLM_VS_CODE.md:30-31), D-071 block (ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (REQUIREMENTS.md:50, 356), board.py show T-207",
               "read service_date.py in full (377 lines) at HEAD; store.py:118-147; export.py:215-226; grep dos_iso writers and date-path imports",
               "pytest tests/unit -q at HEAD archive: 6137 passed, 12 skipped",
               "pytest on 4 T-202 date files: 211 passed",
               "probes P1-P8: artifacts/review-evidence/T-207-r1/probe_t207.py (+.out), probe_t207_p8.py (+.out)",
               "9 mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py (+.out); M4, M6, M8 survived; M1 M2 M3 M5 M7 M9 killed",
               "letter_check eval via letter_eval_t207.py (+.out): value 0, 25 cases, exit 0",
               "grep -rn -i mutant tests/unit evals: 28 comment hits, no 24-mutant harness"],
 "verdict": "changes",
 "scores": {"row2_matches_code": 3, "row3_matches_code": 3, "date_is_code_only": 5, "allow_list_decides": 3, "statement_date_rule": 4, "not_certain_blank_and_note": 3, "tests_and_validation_claims": 2},
 "findings": [
  {"severity": "major", "title": "Row 2 says a two-reading date is certain only by the statement rule; code also settles it from the other end of the same period",
   "evidence": "probe_t207.out line 'P3 | $120.00 | stated | 2026-05-04 | 2026-05-13' for 'DOS 04/05/2026 - 13/05/2026 therapy $120.00.' (statement 2026-06-30); app/backend/service_date.py:215-217 'if determined: order = next(iter(determined))'; docs/LLM_VS_CODE.md:30 'it is certain only when a reading after the bill's own (statement) date is impossible'; tests/unit/test_t202_r2_service_date_layouts.py:129 kills M3",
   "why_it_matters": "The table is the binding description of how a printed date is decided. It says the statement rule is the only resolver; the code and a tested test use a second rule. D-071's amendment contemplates a record-level locale rule, but the table does not state one.",
   "fix": "Architect amends row 2 to state the same-period locale rule (cite D-071 amendment 'no locale rule from the record'), or the code drops the rule and the period prints the blank.",
   "acceptance_test": "Row 2 names the rule the code applies; a test pins '04/05/2026 - 13/05/2026' to the decided answer; mutant M3 stays killed."},
  {"severity": "major", "title": "Five-year bound is 1830 days, not 'more than five years'; no test sits at the boundary",
   "evidence": "app/backend/service_date.py:55 '_YEARS_BEFORE = 5'; :274 'days=366 * _YEARS_BEFORE'; probe_t207.out 'P4 06/29/2021 | $120.00 | stated | 2021-06-29' (5y+1d before 2026-06-30) and 'P4 06/26/2021 | $120.00 | stated | 2021-06-26'; mutants_t207.out 'M4 ... SURVIVED | exit=0 | 211 passed'; tests only at 1998/2031 (tests/unit/test_t202_r3_allow_list.py:187-188); docs/LLM_VS_CODE.md:30 'more than five years before it is not read'",
   "why_it_matters": "A service date 5y+1d to 5y+4d before the statement is printed as a date of service though row 2 says it is not read. No test would catch it. Persona calibration: missing boundary test is major.",
   "fix": "Compare calendar years (statement date minus five years, same month and day, 29 Feb handled) instead of 366-day arithmetic; keep 1998 and 2031.",
   "acceptance_test": "Statement 2026-06-30: 06/29/2021 prints the blank with reason implausible; 06/30/2021 is stated; M4 is killed."},
  {"severity": "major", "title": "A charge with no labeled date takes the visit note's header date; row 2 says only the allow-list counts",
   "evidence": "probe_t207.out 'P5-store | $240.00 | stated | 2026-01-09 | None | None | text='January 9, 2026' | note=None' for 'Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.'; probe_t207_p8.out 'P8 pos=None non-bill | state=stated | date_iso=2026-01-09' vs 'P8 pos=None ledger | state=not_stated'; app/backend/service_date.py:375-376 'if date_iso:' ... 'state=\"stated\", first=date_iso'; app/backend/store.py:133-136; tests/unit/test_t202_r3_allow_list.py:98 pins it; mutants_t207.out 'M7 ... KILLED'; docs/LLM_VS_CODE.md:30 'Only a date tied to the line by ... counts'; spec/REQUIREMENTS.md:50 'Date of service is the record's header date, parsed by code.'",
   "why_it_matters": "The code follows R-TL-3 for encounter records and nothing is invented, but the table says the allow-list decides and that the header date is not the DOS for a bill only. The table misstates a rule that decides a printed date. Under persona §5 an unannounced default would be a blocker; R-TL-3 authorizes it here, so I rate it major.",
   "fix": "Chris rules (Q1). If yes, row 2 names the encounter-header rule and cites R-TL-3. The pos-None branch at store.py:133 then either follows the same rule and says so, or prints the blank as the ledger path does.",
   "acceptance_test": "Row 2 states the rule; a test with pos=None on a visit-note charge matches the ruling; M7 stays killed."},
  {"severity": "major", "title": "A counted undated charge prints the blank with no Step 3 confirm note",
   "evidence": "probe_t207.out 'P6 | $250.00 | not_stated | None | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None' vs 'P6-uncounted ... note=' with a note; app/backend/store.py:129 (counted_undated) and :139 'if not stated and not counted_undated:'; mutants_t207.out 'M6 ... SURVIVED'; docs/LLM_VS_CODE.md:31 'Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it'; memory/ORCHESTRATOR_DECISIONS.md:72 D-064 'then sums like any accepted charge'",
   "why_it_matters": "Row 3 and the brief require a Step 3 note for every not-certain case. Once the paralegal counts the line, the prompt disappears; the blank still prints, so nothing is invented or lost. Major, not blocker.",
   "fix": "Either row 3 says counted lines carry no note and cites D-064, or store.py:139 keeps the note with 'Count this charge' wording.",
   "acceptance_test": "A test on a counted undated charge asserts the decided note behaviour; M6 is killed or the row is amended."},
  {"severity": "major", "title": "Validation cell claims 24 mutants all fail; two resolver mutants survive and no 24-mutant harness exists",
   "evidence": "docs/LLM_VS_CODE.md:31 '24 mutants of the resolver and the check all fail the unit suite'; mutants_t207.out 'M4 five-year bound ... SURVIVED' (service_date.py:274) and 'M8 Encounter date heading dropped ... SURVIVED' (service_date.py:53); grep -rn -i mutant tests/unit evals --include=*.py returns 28 comment hits from other cards",
   "why_it_matters": "A validation claim that the reviewer can refute is a finding. The cell is part of the checked artifact (row 3 'How it is checked').",
   "fix": "Amend the cell to the tests that exist, or commit the mutation harness with its count; add tests that kill M4 and M8.",
   "acceptance_test": "The cell names only committed tests; the harness, if committed, reports 24 of 24 killed; M4 and M8 are killed."},
  {"severity": "minor", "title": "Row 2's column-heading list is narrower than the code",
   "evidence": "docs/LLM_VS_CODE.md:30 'a DOS or service column header'; app/backend/service_date.py:53-54 _H_SVC also matches visit date, date of visit, encounter date, svc, 24A, from/to service; M8 survives",
   "why_it_matters": "A reader cannot tell which headings decide a printed date.",
   "fix": "List the heading set in row 2; add a test for Encounter Date.",
   "acceptance_test": "Row 2 lists the set; M8 is killed."},
  {"severity": "minor", "title": "Row 3's note wording holds only for written-date reasons",
   "evidence": "docs/LLM_VS_CODE.md:31 'asking the paralegal to read the date from the quote' and 'names the date as the quote writes it'; app/backend/service_date.py:102 (written-date note) vs :103 'Request a dated itemized bill, or fill the blank from the record'; probe_t207.out 'P7b ... note=The line states no date of service ...'",
   "why_it_matters": "The no-label note does not name a date and does not ask for the quote, so row 3 overstates the note.",
   "fix": "Align row 3 with the two note forms, or change the no-label note to point to the quote.",
   "acceptance_test": "The row and the note text agree; the existing confirm-note test still passes."},
  {"severity": "minor", "title": "A second date-of-service parser on billing lines sits outside row 2's only-path claim",
   "evidence": "app/backend/billing.py:141 'def _dos(raw): p = dates.parse_date(raw or \"\")'; billing.py:339 'dos_iso': _dos(dos); billing.py:1062 GET /api/cases/{token}/billing; api.py:599 billing.add_routes; no frontend consumer (grep app/frontend for /billing empty)",
   "why_it_matters": "Row 2 says a charge line's date of service is read only by service_date.py. This endpoint returns a DOS per bill line by a generic parser. It does not reach the letter, but it is a second source of the same fact.",
   "fix": "Document the endpoint's dos_iso as not a charge date in row 2, or remove it.",
   "acceptance_test": "Row 2 names the endpoint's status; grep for dos_iso writers shows no second charge-date path."}
 ],
 "whats_right": ["The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.",
                 "The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.",
                 "The blank matches the D-071 addendum text exactly (probe P7), and letter_check reports value 0 over 25 cases."],
 "questions_for_chris": ["Q1 (F3): Should a dated visit note's header date be the date of service for a charge with no labeled date? R-TL-3 says yes; row 2 says only the allow-list counts.",
                         "Q2 (F1): Is the same-period locale rule approved ('04/05/2026 - 13/05/2026' as May 4-13), or should that period print the blank as row 2 states?",
                         "Q3 (F4): Should a counted undated charge (D-064) show the Step 3 confirm note?"]}
```
8cb5bd2 fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
8521562 fix(frontend): Step 3 next step depends on the date reason: doubtful date checks the quote, no date looks outside it; statement-date, total and clip minors (T-209 r2)
88c73dd fix(frontend): Step 3 confirm note names the letter's fillable date blank (T-209)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:58:59.907Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head -30"
}
````

### User / tool · 2026-11-03T01:59:00.002Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
94:- D-071 amendment 2 (§7.4 after T-202 r3; round 4 authorised, final): (a) a record's own date is a service date only for a positively identified encounter record (visit/ER/clinic/therapy/ambulance-run note); bills, receipts, superbills, charge summaries and unknown types never lend their header date; (b) in prose, only "date of service", "dates of service", "DOS" and "service date" are labels ("visit date", "seen on" and bare "date" are not; they also name next or prior visits); (c) letter_check keeps an independent scanner but reads the same declared encounter-type table (one data file), and anchors the blank; (d) if round 4 fails, the fallback is the most conservative rule: every charge line prints the fillable blank unless a DOS column or one of the (b) labels ties exactly one date to it.
95:- D-071 amendment 2 note (T-202 r4): inside bills only, "visit of", "the run of", "rendered on" and "service period" also count as service labels (case_09 and lib14 need them); outside bills they do not. Accepted.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:03.087Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short docs/LLM_VS_CODE.md && sed -n 28,32p docs/LLM_VS_CODE.md && wc -l app/backend/service_date.py app/backend/encounter_types.json && git diff --stat 8cb5bd2 HEAD -- app/backend | tail -3; $B 2>/dev/null; python3 tools/board.py list 2>/dev/null | grep -n \"T-202\" ; grep -n \"T-202\" board/cards/T-202.md | head -0; tail -30 board/cards/T-202.md"
}
````

### User / tool · 2026-11-03T01:59:03.154Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($B) | command: git rev-parse --short HEAD && git status --short docs/LLM_VS_CODE.md && sed -n 28,32p docs/LLM_VS_CODE.md && wc -l app/backend/service_date.py app/backend/encounter_types.json && git diff --stat 8cb5b
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:04.775Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short docs/LLM_VS_CODE.md && sed -n 28,32p docs/LLM_VS_CODE.md && wc -l app/backend/service_date.py app/backend/encounter_types.json && git diff --stat 8cb5bd2 HEAD -- app/backend | tail -3; tail -25 board/cards/T-202.md"
}
````

### User / tool · 2026-11-03T01:59:04.921Z

**tool result**
````
8cb5bd2
|---|---|---|---|---|
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendment; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** Only a date tied to the line by a DOS or service column header, by a service label in its clause (DOS, date of service, service date, seen on, visit date), by the charge row's own date cell in a table whose header names service, or by the one period its bill states for its services counts. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. A numeric date that reads two ways is resolved by one fixed rule: a service cannot follow its statement, so it is certain only when a reading after the bill's own (statement) date is impossible for every labeled end of the date or period (D-071 clarification). This is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is not the record's header date (a bill's header date is its statement date) and the model is never asked. Code prints the service date or period the bill line itself states (positive evidence only, see row 2). When it is not certain, the letter does not guess: it prints a fillable blank beside the statement date (D-071 addendum: "date of service [__________] (statement dated June 15, 2026)") and Step 3 shows a confirm note asking the paralegal to read the date from the quote. Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. Charge dates: `tests/unit/test_t202_r3_allow_list.py` (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and `evals/letter_check.charge_date_violations`, which accepts the blank and nothing else for a line with no certain date. |
| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in the record). The summary is split into clauses, and a clause is removed only when it adds **salient new content** its quote lacks: a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term (`new_salient`, `summary_trim.py:325-356`). Terms are matched by word family (Tylenol with acetaminophen, cervical with neck) after clinical abbreviations are expanded on both sides (`expand_abbreviations`, `:108`; families `:212-267`), so a faithful paraphrase stays and judge 1 checks it. The negation and side words come from the lexicon (`code_lists.added_qualifier` through `grounding`, `summary_trim.py:269`, `:338-342`), not from a list in the trim. A number, side or negation counts only in a clause that shares no content word with the quote; a changed value on the quote's own topic ('Pain 3/10' over 'Pain 4/10') stays and is caught by the rung 1 token checks. A **structural no-fragment rule** (no word list; `:417-423`, T-128 r3): code trims only a **suffix**. A clause is removed only when every clause after it is removed too, so the kept text is always a prefix of whole clauses and no kept clause can follow a removed one (`'Wrist pain 6/10; splint fitted; patient tolerated well.'` over a quote that supports only the first and last clause is returned unchanged). The first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix needs at least 2 content words. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`). Each removal is shown in the trace as 'removed from the summary: not in the quote'. If every clause is removed, or what is left has no content word, the item goes to the could-not-verify tray with `SUMMARY_NOT_IN_QUOTE` (`summary_trim.py:414-415`; `generator.py:75-77`; template `why.py:33`) and is never judged. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
     434 app/backend/service_date.py
      21 app/backend/encounter_types.json
     455 total
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service." Append to the "Validation" cell: " Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser)."
- 2026-11-03T00:45:37Z backend: (correction: the two empty notes above were a shell slip; the exact LLM_VS_CODE text for the architect is in the note just above and on T-207.)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints "(statement dated X; service date not stated)". Both are gone. Replace those two sentences with exactly: "Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it." Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date.
- 2026-11-03T01:25:40Z backend: AC 1 checked: r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->any all killed; corpus charge headers byte-identical (84 lines)
- 2026-11-03T01:25:40Z backend: moved in_progress -> in_review
- 2026-11-03T01:25:49Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer
- 2026-11-03T01:34:13Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r3.md; round 3; findings:
    - [blocker] A 'visit date' / 'seen on' label naming another visit (next, last, previous, initial) prints that visit's date as the charge's date of service; in a visit note it overrides the note's own correct date (regression vs pre-T-202), and letter_check enforces the wrong date — fix: In a dated encounter record (not a bill), the record's date is the visit. A labeled date there prints only w
    - [minor] The note says 'The line states no date of service' or 'not labeled as a date of service' for lines that do label one in a form the code does not read (DOS with ordinal, UB-04 FL6 six-digit period, CMS-1500 Item 24A) — fix: When a service label (DOS, 24A, FL6 / statement covers period) is present but its date is not parsed, use the written-date note naming the text as written ('The qu
    - [minor] Internal notes tell me to 'fill it from the quote' for lines whose quote has no date, and the one-date blank does not fit a multi-visit line — fix: Word the notes line by reason. no_date / non_service_date: 'the bill line gives no date; take it from the matching visit note or request a dated itemized bill'. Written-date reasons: 'the quote writes "04/05/2026"; confirm and fill'. When
    - [minor] Carried from rounds 1 and 2: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T01:34:13Z orchestrator: assigned: backend
- 2026-11-03T01:34:13Z orchestrator: Paralegal r3 blocker: 'next visit date 01/16/2026' in an ER note dates the ER charge Jan 16 (label 'visit date' matched). Round 4 (§7.4 decision) queued until staff r3 lands.
- 2026-11-03T01:37:28Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r3.md
- 2026-11-03T01:37:28Z backend: moved changes_requested -> in_progress
- 2026-11-03T01:58:28Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, T-207), after T-202 r4 commit 8cb5bd2 (D-071 amendment 2). Row 2: replace "by a service label in its clause (DOS, date of service, service date, seen on, visit date)" with "by a service label in its clause (in prose only DOS, date of service, dates of service and service date, never after next/last/prior/previous/initial/follow-up; a bill also reads its own 'visit of' and 'the run of')". Row 3 (append): "A record's own date is a charge line's date of service only for a positively identified encounter record (visit, ER, clinic, therapy, imaging or ambulance-run note), declared in one data file, app/backend/encounter_types.json, which production and evals/letter_check.py both read. A bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its header date: it prints the fillable blank unless a label or a DOS column ties one date to the line." Validation cell: "tests/unit/test_t202_r4_encounter.py (every r3 reviewer probe is a fixture; 24 of 25 mutants fail the unit suite, the 25th is equivalent)".
- 2026-11-03T01:58:28Z backend: AC 1 checked: r4 8cb5bd2 (git archive): unit 6266 passed 12 skipped 1 failed (test_e2e_contract test ids, fails identically at parent 8521562, not my files), guided e2e 145 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r4_encounter.py 131 tests (86 red before); 24 of 25 mutants killed (25th equivalent); 150 corpus letter+notes blobs byte-identical
- 2026-11-03T01:58:31Z backend: moved in_progress -> in_review
- 2026-11-03T01:58:42Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r4, 8cb5bd2, D-071 amendment 2): (a) service_date.record_kind reads the one declared table app/backend/encounter_types.json; only an identified encounter (visit/ER/clinic/therapy/imaging/EMS) lends its header date, bills/receipts/superbills/charge summaries/admin papers/unknown never do (store.charge_service_date too). (b) prose labels are only DOS, date(s) of service, service date, never after next/last/prior/previous/initial/first/return/follow-up/scheduled/upcoming/future; visit date, seen on, bare date dropped. (c) letter_check keeps its own scanner, reads the same JSON with its own matcher, and accepts the blank only whole and exact. T-209 r2 leader: a label then dots/spaces/colon then one date is that label's date (leaders masked, label gap unlimited, window 60), also the DOS ... 99213 ... $250.00 reviewer case.
How verified (git archive 8cb5bd2): unit 6266 passed, 12 skipped, 1 failed (4 shards; the 1 is tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, brand/footer-note/draft-done/demo-badge/btn-draft test ids, fails the same at parent 8521562 and touches none of my files); guided e2e 145 passed; python -m evals.letter_check value 0 over 25 cases. tests/unit/test_t202_r4_encounter.py 131 tests, 86 red before the fix; every r3 paralegal+staff probe (next visit date, R1/R2/R17-19/R23, C4/C6/C7, superbill, patient receipt, charge summary, fee schedule, estimate, cost of care summary, claim, remittance, itemization, Receipt:/Charges:/Account summary:, EOB/payment history/HCFA/balance due blanks, bare date, Entry/Posted/Transaction/Issue date, leaders) is a fixture. Mutants (scratch copy): the 4 staff survivors M6 L3 L7 killed, L6 equivalent now (the whole-blank compare rejects 9/11 underscores itself); 21 new mutants P1-P14 C1-C7 all killed: 24 of 25 killed in total. Corpus: 150 letter+notes blobs (25 cases x all_accepted/counted) byte-identical before and after.
Judgment calls: (1) bills keep 'visit of', 'the run of', 'rendered on', 'service period' (case_09 and lib14 goldens depend on them; in a non-bill they are not labels). If the orchestrator wants only the four, case_09 and lib14 print the blank: one line in _SVC_BILL. (2) The plausibility rule (not after the record, not >5 years before) now applies to every record, not only bills. (3) An excerpt opening with a financial word before its first colon/full stop ('ER charges: ...') makes a bill: safe direction (blank). (4) test_t200 and test_t202_r3 edited (qa-owned): 3 prose-label rows moved to the r4 file, one unknown-source assertion.
What's left: architect T-207 text (note on the card); paralegal minors from r3 (notes wording by reason, 24A/FL6 note, quote span) not done; the CMS-1500 export-gate question is outside T-202. What surprised me: the opening scan flagged my own ER fixture; the Write tool rewrites \u escapes in scripts.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:06.516Z

**tool call — Bash**
````
{
 "command": "cat app/backend/service_date.py app/backend/encounter_types.json"
}
````

### User / tool · 2026-11-03T01:59:06.590Z

**tool result**
````
"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 rounds 3 and 4: an ALLOW-LIST, not a deny-list). Code only, no LLM
(LLM_VS_CODE rows 2 and 3).

The letter's charge line carries a date of service. A date there is a claim to an adjuster, so a date is the line's service date ONLY when one of these ties it to the line:
  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
  (b) a service label in the same clause before (or just after) it. In prose ONLY 'DOS', 'date of service', 'dates of service' and 'service date' (D-071 amendment 2; 'visit date', 'seen on'
      and a bare 'date' name next or prior visits and entry dates, so they are not labels), never after next/last/prior/previous/initial/first/return/follow-up/scheduled/upcoming/future.
      A BILL also reads the wording a statement uses for what it covers ('visit of', 'the run of', 'rendered on', 'service period' ...). A label may be followed by a dotted leader,
      spaces or a colon before its date;
  (c) it is the date cell of the charge row itself, in a table whose header is (a);
  (d) for a coded line of a bill with no date of its own: the one period the bill states for its services ('dates of service ...', 'the run of ...', and on a UB-04 'statement
      covers period ...').
Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all) is NOT a service date and is never
looked at again: an unlabeled date cannot become the line's date by default. The record's own date is the line's date ONLY for a positively identified encounter record (`record_kind`, the
table app/backend/encounter_types.json: visit, ER, clinic, therapy, imaging, ambulance-run note); a bill, receipt, superbill, charge summary, administrative paper or record of unknown type
never lends its header date. The result is one of:
  - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
    EVERY labeled end then reads one way; a stated date after its record's own date, or more than five years before it, is doubtful);
  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service (an encounter record keeps its own date instead);
  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
    the code cannot read it with certainty; the note names the date as the quote writes it.
  Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
  and the letter never says "service date not stated" above a quote that states one.
Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
import datetime as _dt
import json
import pathlib
import re

from app.backend import amounts as AM

TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))


def _tokens(text: str) -> list:
    return re.findall(r"[^\W_]+", (text or "").lower())


def _phrase_rx(terms):
    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")


_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
_ABBR = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(map(re.escape, _TYPES["encounter_abbreviations"])) + r")(?![A-Za-z0-9])")
_OPEN = int(_TYPES["opening_chars"])


def _hit(rx, text) -> bool:
    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))


def record_kind(source, excerpt: str = "") -> str:
    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
    identification in the source label (visit, ER, clinic, therapy, imaging, ambulance-run note ...). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
        return "bill"
    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
        return "other"
    return "encounter" if (_hit(_ENC, src) or _ABBR.search(src)) else "other"

_MON = AM._MON
_ORD = r"(?:st|nd|rd|th)?"
_DASH = "–—"
_TOK = re.compile(
    r"(?<![\w/$])(?:"
    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
    r")(?![\w/]|\.\d)", re.IGNORECASE)
_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
# ---- the allow-list: positive evidence that a date is the line's date of service. Nothing else is read (T-202 round 3).
_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
_LEADER = re.compile(r"(?:\.[ ]?){3,}|\u2026+")
_WINDOW = 60                     # characters before a date that may hold its label and the leader after it


def _mask_leaders(text: str) -> str:
    """The same text with every dotted leader ('.......', '. . . .', '\u2026') replaced by as many middle dots, so positions are unchanged: a leader is neither a sentence end nor a column gap, and
    'Date of service.......01/19/2026 ... 99213 office visit ...... $250.00' reads as one clause (T-209 r2: a label, dots or spaces or a colon, then one date is that label's date)."""
    return _LEADER.sub(lambda m: "\u00b7" * len(m.group(0)), text or "")
_NOT_OTHER_VISIT = (r"(?<!next )(?<!last )(?<!prior )(?<!previous )(?<!initial )(?<!first )(?<!return )(?<!scheduled )(?<!upcoming )(?<!future )(?<!follow-up )(?<!followup )"
                    r"(?<!next\s)(?<!last\s)")
_SVC_CORE = _NOT_OTHER_VISIT + r"(?:\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?)"        # amendment 2 (b): the only labels in prose
_SVC_BILL = (r"\bvisit\s+of|\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")        # a bill's own wording for what it covers (a statement 'for the visit of', an invoice 'for the run of')
_PER_CORE = (r"\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bservice\s+period|\bperiod\s+of\s+service|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|"
             r"\b(?:services?\s+)?(?:rendered|provided)\s+on")
_UB_CORE = r"\bstatement\s+(?:covers\s+)?period"          # UB-04 FL6 'Statement Covers Period' is the span of the services; on any other bill 'statement period' is not a service label
_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)


def _lbl_rx(extra, ub):
    return re.compile(rf"(?:{_SVC_CORE}" + (rf"|{_SVC_BILL}" if extra else "") + (rf"|{_UB_CORE}" if ub else "") + rf"){_LBL_END}", re.IGNORECASE)


_LBL = {(b, u): _lbl_rx(b, u) for b in (False, True) for u in (False, True)}          # keyed (bill, ub)
_PER = {u: re.compile(rf"(?:{_PER_CORE}" + (rf"|{_UB_CORE}" if u else "") + rf"){_LBL_END}", re.IGNORECASE) for u in (False, True)}
# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful

REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)


def display(first, last=None) -> str:
    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
    def lng(iso):
        d = _dt.date.fromisoformat(iso)
        return f"{d.strftime('%B')} {d.day}, {d.year}"
    if not last or last == first:
        return lng(first)
    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
    if a.year == b.year:
        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
    return f"{lng(first)}–{lng(last)}"


BLANK = "date of service [__________]"


def not_stated_text(statement_iso) -> str:
    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
    if statement_iso:
        return f"{BLANK} (statement dated {display(statement_iso)})"
    return BLANK


def printed_text(res: dict, statement_iso) -> str:
    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
    return not_stated_text(statement_iso)


_WHY = {
    "ambiguous_numeric": "The quote labels {raw} as the date of service, and it can be read as month/day or day/month; the record does not settle which.",
    "two_digit_year": "The quote labels {raw} as the date of service, but it has a two-digit year, which the code does not guess.",
    "no_year": "The quote labels {raw} as the date of service, but it states no year, which the code does not borrow from the statement.",
    "invalid": "The quote labels {raw} as the date of service, but it is not a complete date on the calendar.",
    "several_dates": "The quote labels more than one date of service ({raw}) and nothing says which one belongs to this charge.",
    "implausible": "The quote labels {raw} as the date of service, but that date is after the statement it appears on or years before it.",
    "non_service_date": "The only date near this line ({raw}) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service).",
    "no_date": "The line states no date of service.",
}
_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it."


def confirm_note(reason, raw) -> str:
    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)


def _iso(y, mo, d):
    try:
        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
    except ValueError:
        return None


class _Tok:
    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")

    def __init__(self, m):
        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
        getattr(self, "_" + self.kind)(m.group(0))
        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
            self.flaw = "invalid"

    def _iso(self, s):
        y, mo, d = (int(x) for x in s.split("-"))
        self.fixed = _iso(y, mo, d)

    def _num(self, s):
        a, b, y = re.split(r"[/.-]", s)
        if len(y) == 2:
            self.flaw = "two_digit_year"
            return
        a, b, y = int(a), int(b), int(y)
        md, dm = _iso(y, a, b), _iso(y, b, a)
        if md and dm and md != dm:
            self.ambiguous = {"MD": md, "DM": dm}
        elif md or dm:
            self.fixed = md or dm
            self.order = None if (md and dm) else ("MD" if md else "DM")

    def _mdy(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
        if m.group(4):
            self.flaw = "two_digit_year"
            return
        if not m.group(3):
            self.flaw = "no_year"
            return
        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))

    def _dmy(self, s):
        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))

    def _md(self, s):
        self.flaw = "no_year"

    def _mper(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
        if not m.group(5):
            self.flaw = "no_year"
            return
        y, m1 = int(m.group(5)), _mon(m.group(1))
        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
        if a and b and b > a:
            self.first, self.last = a, b
        else:
            self.flaw = "invalid"


def _mon(name):
    from app.backend import dates
    return dates.MONTHS[name.lower()[:3]]


class _Unit:
    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
    def __init__(self, toks):
        self.toks = toks
        self.start, self.end = toks[0].start, toks[-1].end

    def raw(self, text):
        return text[self.start:self.end]


def _units(text: str) -> list:
    toks = [_Tok(m) for m in _TOK.finditer(text)]
    out, k = [], 0
    while k < len(toks):
        t = toks[k]
        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
            out.append(_Unit([t, toks[k + 1]]))
            k += 2
        else:
            out.append(_Unit([t]))
            k += 1
    return out


def _certain(unit: _Unit, ref):
    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
    for t in unit.toks:
        if t.flaw:
            return "bad", t.flaw
    if len(unit.toks) == 1 and unit.toks[0].first:
        return "ok", unit.toks[0].first, unit.toks[0].last
    determined = {t.order for t in unit.toks if t.order}
    amb = [t for t in unit.toks if t.ambiguous]
    if len(determined) > 1:
        return "bad", "ambiguous_numeric"
    if determined:
        order = next(iter(determined))
    elif amb:
        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
        if len(feasible) != 1:
            return "bad", "ambiguous_numeric"
        order = feasible[0]
    else:
        order = None
    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
    if len(isos) == 2 and isos[1] <= isos[0]:
        return "bad", "invalid"
    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)


def _header_cells(excerpt: str, row_ls: int):
    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line."""
    for line in reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]):
        if not line.strip():
            return None
        if re.search(r"\d", line) and not _H_SVC.search(line):
            continue
        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
        return cells if len(cells) >= 2 else None
    return None


def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
    heads = _header_cells(excerpt, row_ls)
    if not heads:
        return ""
    col = tok_abs - row_ls
    if len(heads) == len(row_cells):
        idx = next((i for i, (a, b) in enumerate(row_cells) if a <= col < b), None)
        if idx is not None:
            return heads[idx][1]
    return min(heads, key=lambda h: abs(h[0] - col))[1]


def _mark(text: str, units: list, rx, tail: bool = False) -> list:
    """[bool] per unit: a service label ends the 60 characters before it, or it is listed ('A and B') after a labeled unit. In `tail` (words after the figure) the label must open the
    tail: no sentence break and no 'and'/'or' between the figure and the label."""
    marks = []
    for k, u in enumerate(units):
        ok = bool(rx.search(text[max(0, u.start - _WINDOW):u.start]))
        if ok and tail:
            before = text[:u.start]
            ok = len(before) <= _WINDOW and not re.search(r"[.;]|\b(?:and|or)\b", before, re.IGNORECASE)
        if not ok and k and marks[k - 1] and _LIST.match(text[units[k - 1].end:u.start]):
            ok = True
        marks.append(ok)
    return marks


def _plausible(first, last, ref) -> bool:
    """A service date is not after the record it appears in and not years before it."""
    if not ref:
        return True
    r = _dt.date.fromisoformat(ref)
    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)


def _decide(units, text, ref):
    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
    reads = [(u, _certain(u, ref)) for u in units]
    raws = [" ".join(u.raw(text).split()) for u in units]
    if len(units) > 1:
        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
            return "bad", "several_dates", raws
        first, last = next(iter(same))
    else:
        r = reads[0][1]
        if r[0] != "ok":
            return "bad", r[1], raws
        first, last = r[1], r[2]
    if not _plausible(first, last, ref):          # in every record: a service date is not after the record's own date and not years before it (a prior treatment's DOS is not this charge's)
        return "bad", "implausible", raws
    return "ok", first, last


def _apply(out: dict, res) -> dict:
    if res[0] == "ok":
        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
    else:
        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
    return out


def resolve(excerpt: str, start: int, source, date_iso) -> dict:
    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the labeled date text the reason is about, or the one
    unlabeled date near the line for non_service_date), raws ([the labeled dates as written])} for the figure at `start` of `excerpt`, in a record with header `source` and date
    `date_iso`. Only labeled dates are candidates (module doc); see it for the rules."""
    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    excerpt = _mask_leaders(excerpt)
    amts = AM.find_amounts(excerpt or "")
    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
    if i is None:
        return out
    a = amts[i]
    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
    kind = record_kind(source, excerpt)
    bill = kind == "bill"
    ub = bool(_UB.search(source or "") or _UB.search(excerpt or ""))
    lbl = _LBL[(bill, ub)]
    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
    seg = excerpt[ss:se]
    others = []                       # dates near the line that no service label ties to it

    def labeled(text, tail=False):
        us = _units(text)
        marks = _mark(text, us, lbl, tail)
        others.extend(u.raw(text) for u, m in zip(us, marks) if not m)
        return [u for u, m in zip(us, marks) if m]

    if len(AM._cells(seg)) >= 2:                                          # (a)/(c) a table row: only a date under a heading that names service
        row_ls = excerpt.rfind("\n", 0, a["start"]) + 1
        rl_end = excerpt.find("\n", a["start"])
        row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
        row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
        lab = []
        for u in _units(seg):
            head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
            if (head and _H_SVC.search(head)) or lbl.search(seg[max(0, u.start - _WINDOW):u.start]):
                lab.append(u)
            else:
                others.append(u.raw(seg))
        if lab:
            return _apply(out, _decide(lab, seg, date_iso))
    else:                                                                 # (b) a service label in the same clause
        prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
        own = excerpt[prev:a["start"]]
        lab = labeled(own)
        if lab:
            return _apply(out, _decide(lab, own, date_iso))
        if prev > ss:                                                      # a labeled date stands once for the items listed after it: usable only when it is the line's one date
            whole = excerpt[ss:a["start"]]
            lab = labeled(whole)
            if lab:
                return _apply(out, _decide(lab, whole, date_iso))
        tail = excerpt[a["end"]:min([amts[j]["start"] for j in sfigs if j > i], default=se)]
        lab = labeled(tail, tail=True)
        if lab:
            return _apply(out, _decide(lab, tail, date_iso))
    # no labeled date of its own
    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
        if bill and AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # (d) a coded line takes the one period the bill states for its services
            prefix = excerpt[:se]
            us = _units(prefix)
            seen, uniq = set(), []
            for u, m in zip(us, _mark(prefix, us, _PER[ub])):
                if not m:
                    continue
                r = _certain(u, date_iso)
                key = (r[1], r[2]) if r[0] == "ok" else (u.raw(prefix),)
                if key not in seen:
                    seen.add(key)
                    uniq.append(u)
            if uniq:
                return _apply(out, _decide(uniq, prefix, date_iso))
        if others:
            out.update(reason="non_service_date", raw=others[0])
        return out
    if date_iso:                                                          # a positively identified encounter record (visit, ER, clinic, therapy, imaging, ambulance-run note): its date is the visit
        out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
    return out
{
  "_doc": "D-071 amendment 2 (T-202 round 4). The ONE declared table of record types for charge-line dates. A record's own date can stand as a charge line's date of service ONLY when the record is a positively identified encounter record (a visit, ER, clinic, therapy, imaging or ambulance-run note). Read by app/backend/service_date.py (production) and by evals/letter_check.py (the independent check, with its own matcher). Matching rule, the same in both: lower-case the text, split it into tokens (runs of letters and digits; hyphens, punctuation and underscores split), and a term matches when its tokens appear in order as consecutive tokens of the text. 'encounter_abbreviations' are matched case-sensitively as single upper-case tokens. A record is a BILL when its source label, or the opening of its excerpt (its first 'opening_chars' characters, cut at the first colon, full stop or line break: 'Receipt:', 'Charges:', 'Account summary:'), matches 'financial' (production also keeps the lexicon billing_document list). It is ADMINISTRATIVE when the same text matches 'administrative'. Otherwise it is an ENCOUNTER only when its source label matches 'encounter' or 'encounter_abbreviations'; every other record is of unknown type. Bills, administrative papers and unknown types never lend their header date.",
  "opening_chars": 40,
  "encounter": [
    "visit", "emergency", "urgent care", "clinic", "therapy", "ambulance", "run report", "trip report", "patient care report",
    "discharge summary", "discharge note", "progress note", "office note", "clinic note", "consult", "consultation", "consulta", "nota de consulta",
    "evaluation", "re-evaluation", "reevaluation", "exam", "examination", "new patient", "follow-up", "followup", "primary care", "pain management",
    "orthopedic", "orthopedics", "surgery", "surgical", "operative note", "operative report", "op note",
    "imaging", "radiology", "mri", "x-ray", "xray", "ct scan", "ultrasound", "chiropractic", "chiropractor", "physical therapy", "telehealth"
  ],
  "encounter_abbreviations": ["ER", "ED", "EMS", "PT", "OT"],
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

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:08.821Z

**tool call — Bash**
````
{
 "command": "sed -n 100,160p app/backend/store.py; grep -n \"service_date\\|charge_when\\|not_stated_text\\|printed_text\\|counted_undated\" app/backend/export.py"
}
````

### User / tool · 2026-11-03T01:59:08.917Z

**tool result**
````
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
    """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 2026)'
    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
    A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
    the one period its bill states; an unlabeled date (birth, injury, referral, entry, transaction ...) is never the service date. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
    service date. A positively identified encounter record's (visit, ER, clinic, therapy, imaging or ambulance-run note: service_date.record_kind, app/backend/encounter_types.json) own date is the visit; a bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its date (D-071 amendment 2). A charge the paralegal counted for a missing date of service (D-064) is
    not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    encounter = SD.record_kind((rec or {}).get("source"), item.get("excerpt") or "") == "encounter"
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    if counted_undated:
        r = dict(none)
    elif rec is None or pos is None or not item.get("excerpt"):
        r = {"state": "stated", "first": rd, "last": None, "reason": None, "raw": "", "raws": []} if (encounter and rd) else dict(none)          # only a positively identified encounter record lends its own date (D-071 amendment 2)
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
22:from app.backend import amounts, charge_text, language, money, service_date
74:    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026' (D-071). One implementation, shared with the case view (service_date.display)."""
75:    return service_date.display(first, last)
215:    def charge_when(self, a):
217:        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
226:        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
358:            out += [f"{v.charge_when(a)}: {_money(a['cents'])}",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:18.850Z

**tool call — Bash**
````
{
 "command": "sed -n 212,228p app/backend/export.py; grep -n \"confirm_note\\|charge_service_date\" app/backend/*.py | grep -v \"^app/backend/service_date.py\"; grep -rn \"dos_iso\" app/backend/billing.py | head -3; grep -n \"M4\\|M8\\|mutant\" board/cards/T-202.md | head -0; ls tests/unit | grep t202; grep -n \"1830\\|2021\\|encounter date\" -i tests/unit/test_t202_r4_encounter.py | head"
}
````

### User / tool · 2026-11-03T01:59:19.018Z

**tool result**
````
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
app/backend/export.py:217:        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
app/backend/present.py:152:            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for this charge's date
app/backend/store.py:118:def charge_service_date(item: dict, rec, pos) -> dict:
app/backend/store.py:121:    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
app/backend/store.py:140:        note = SD.confirm_note(r["reason"], r["raw"])
app/backend/store.py:143:            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}
app/backend/store.py:146:def charge_service_dates(item: dict, rec, pos) -> tuple:
app/backend/store.py:147:    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
app/backend/store.py:148:    d = charge_service_date(item, rec, pos)
app/backend/store.py:196:            sd = charge_service_date(a, r, d["pos"])
app/backend/store.py:197:            d["dos_iso"], d["dos_end_iso"], d["dos_text"], d["dos_note"] = sd["date_iso"], sd["end_iso"], sd["text"], sd["confirm_note"]
app/backend/billing.py:339:    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
app/backend/billing.py:479:            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
app/backend/billing.py:553:        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
head: illegal line count -- 0
test_t202_charge_service_dates.py
test_t202_r2_service_date_layouts.py
test_t202_r3_allow_list.py
test_t202_r4_encounter.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:27.171Z

**tool call — Bash**
````
{
 "command": "grep -n \"Encounter Date\\|encounter date\\|years\\|1830\\|5y\\|five\" -i tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_r3_allow_list.py | head; grep -n \"^def test\" tests/unit/test_t202_r4_encounter.py | wc -l; grep -n \"counted\" tests/unit/test_t202*.py tests/unit/test_t200*.py | head -5; grep -n \"R-TL-3\" spec/REQUIREMENTS.md | head -3; ls evals/letter_check.py"
}
````

### User / tool · 2026-11-03T01:59:27.324Z

**tool result**
````
tests/unit/test_t202_r4_encounter.py:283:def test_in_every_record_a_labeled_date_after_the_record_or_years_before_it_is_not_certain():
tests/unit/test_t202_r3_allow_list.py:184:    ("1998, years before the statement", "Itemized ledger. DOS 03/13/1998 office visit charge $220.00.", "$220.00", "03/13/1998", "2026-06-30", "implausible"),
tests/unit/test_t202_r3_allow_list.py:185:    ("2031, years after the statement", "Itemized ledger. DOS 03/13/2031 office visit charge $220.00.", "$220.00", "03/13/2031", "2026-06-30", "implausible"),
tests/unit/test_t202_r3_allow_list.py:227:# ================================================================ 5. staff: the all-vs-any rule; a service does not follow its statement; years bound
      25
tests/unit/test_t200_undated_charge_label.py:1:"""T-200 (GATE-M2 r2 paralegal major): a counted ledger charge whose line states no date of service must not print the statement date as if it were a service date.
tests/unit/test_t200_undated_charge_label.py:23:def test_lib11_counted_ledger_lines_are_labelled_with_the_statement_date(lib11, style):
tests/unit/test_t200_undated_charge_label.py:39:def test_a_counted_line_keeps_its_citation_and_quote(lib11):
tests/unit/test_t200_undated_charge_label.py:61:    counted = {"excerpt": "x", "ladder": {"counted": {"not_counted_reason": AM.NO_DATE_WHY}}}
tests/unit/test_t200_undated_charge_label.py:62:    assert store.charge_service_dates(counted, {"source": "s", "date_iso": "2026-06-15"}, None) == (None, None)
50:| R-TL-3 | **Date of service is the record's header date, parsed by code.** Dates inside the body are facts for the conflict check, never the entry date. | Seeded test on **record 7**: header 2026-05-18, body "Date of accident per intake form: 2026-01-19". If the model returns 2026-01-19, the entry is `rejected` (`GROUNDING_DATE_MISMATCH`). Normal path: entry 7 dated 2026-05-18, sorted between entries 6 and 8. | UT + EV (`sample`) |
350:| A-105 | Each pasted record carries its date and source on its first line or table row; undated or ambiguous records go to "Dates to confirm". | R-IN-3, R-IN-5, R-TL-3 |
356:- The date of service is the record's header date. Body dates are conflict evidence only (R-TL-3).
evals/letter_check.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:35.284Z

**tool call — Bash**
````
{
 "command": "sed -n 84,91p memory/ORCHESTRATOR_DECISIONS.md; grep -n \"D-064\" memory/ORCHESTRATOR_DECISIONS.md | head -3"
}
````

### User / tool · 2026-11-03T01:59:35.379Z

**tool result**
````
## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.

## D-071 amendment — when the service date is not certain, print none and ask the human
T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.

## D-072 — The prompt log is built and privacy-reviewed once, last
Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
72:| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this charge", a named confirm ("I checked this is a separate charge for a service"), recorded in the audit trail; it then sums like any accepted charge. Amends D-059 item on reclassify: (b) is promotable with the confirm, (a) never. | The default-deny rule undercounts real ledger lines (lib11 $3,260 vs $6,000); the paralegal must see why and be able to fix it herself, without reopening the overcount paths. | GATE-M2 r2 paralegal |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:59:55.408Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/rw.py <<'EOF'\nimport re\np = \"docs/LLM_VS_CODE.md\"\ns = open(p, encoding=\"utf-8\").read()\nlines = s.split(\"\\n\")\ni2 = next(i for i, l in enumerate(lines) if l.startswith(\"| 2 | Parse dates\"))\ni3 = next(i for i, l in enumerate(lines) if l.startswith(\"| 3 | Date of service and provider\"))\nc2 = lines[i2].split(\" | \")\nc3 = lines[i3].split(\" | \")\nassert len(c2) == 4 and len(c3) == 4, (len(c2), len(c3))\n\nrow2_code = (\n\"**Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. \"\n\"**A charge line's date of service is code only, never the LLM (D-071 and its amendments; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** \"\n\"Only a date tied to the line counts: (a) a column heading over it that names service (DOS, date of service, service date, visit date, date of visit, encounter date, SVC, service or SVC from/to/thru, CMS-1500 24A); \"\n\"(b) a service label in its clause, which in prose is only DOS, date(s) of service or service date, never after next, last, prior, previous, initial, first, return, follow-up, scheduled, upcoming or future \"\n\"(\\\"visit date\\\", \\\"seen on\\\" and a bare \\\"date\\\" are not labels; a bill also reads its own \\\"visit of\\\", \\\"rendered/provided/performed on\\\", \\\"the run of\\\", \\\"service period\\\", \\\"period of service\\\" and \\\"dates of treatment\\\", and a UB-04 \\\"statement covers period\\\"; a label may be followed by a colon, spaces or a dotted leader); \"\n\"(c) the charge row's own date cell under a heading of kind (a); (d) for a coded line of a bill with no date of its own, the one period the bill states for its services. \"\n\"Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. \"\n\"**A numeric date that reads two ways is settled by two fixed rules, in this order, and otherwise stays unread.** \"\n\"(1) Same date or period: when another end of the same labeled date or period can be read only one way (`13/05/2026`), every end takes that order, so `04/05/2026 - 13/05/2026` reads as May 4 to May 13; two ends that force different orders are not read. This uses the date's own text, not a locale guessed from the record (D-071 amendment: no locale rule from the record). \"\n\"(2) Otherwise a service cannot follow its statement (D-071 clarification): the date is read only when exactly one order puts every labeled end on or before the record's own date, and with no record date it is not read. This is a deterministic rule, not a guess. \"\n\"A two-digit year, a date with no year, a date not on the calendar, or several labeled dates that do not agree is not read. \"\n\"**The bound applies to every record, not only bills:** a labeled service date after the record's own date, or more than 1,830 days (5 x 366) before it, is not read (reason `implausible`); a record with no date has no bound. The bound is day arithmetic, so a date a few days past five calendar years can still be read. \"\n\"**A record's own date is the service date only for an identified encounter record** (a visit, ER, clinic, therapy, imaging or ambulance-run note), and only when the line has no labeled date of its own (R-TL-3, D-071 amendment 2). \"\n\"The record types are one declared data file, `app/backend/encounter_types.json`, read by `service_date.record_kind` in production and by `evals/letter_check.py` with its own matcher. A bill, receipt, superbill, charge summary, administrative paper (phone note, letter, affidavit, referral) or record of unknown type never lends its header date. \"\n\"A labeled date that cannot be read in an encounter record is not replaced by the header date: the line prints the blank. \"\n\"The billing view's per-line `dos_iso` (`app/backend/billing.py`, `GET /api/cases/{token}/billing`) is a display field read by a different parser; it is not a charge date and does not reach the letter.\"\n)\nrow3_code = (\n\"**Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider (\\\"Capital PT, initial evaluation\\\"). The model is not asked for either. \"\n\"**Charge-line exception:** for a charge line the date is the service date of row 2, never the record's header date merely because it is the header (a bill's header date is its statement date), and the model is never asked. \"\n\"Code prints the service date or period the line itself states, or, for an identified encounter record (R-TL-3, row 2), the visit's own date when the line has no labeled date. \"\n\"A bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its header date. \"\n\"When no service date is certain (the quote labels none, or labels one the code cannot read with certainty), the letter prints the same fillable blank, like the Bates placeholder, beside the statement date: `date of service [__________] (statement dated June 15, 2026)` (D-071 addendum; `service_date.not_stated_text`, `export.charge_when`). The paralegal fills it from the quote; nothing is inferred. \"\n\"Step 3 shows exactly what the letter prints and carries a confirm note in one of two forms (`service_date.confirm_note`): when the quote labels a date the code cannot read, the note names the date as the quote writes it and asks her to confirm it and fill the blank; when the quote labels none, the note says the line states no date of service (or that the only date near it is not labeled as one) and asks her to request a dated itemized bill or fill the blank from the record. \"\n\"**A charge she has counted for its missing date of service (D-064) still prints the blank but carries no note**, because she counted it knowing (`store.charge_service_date`). \"\n\"A hand-built case dict without `dos_iso` (no store path) keeps the record's date in `export.charge_when`; the app's own export always carries `dos_iso`.\"\n)\nval3 = (\n\"Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a \\\"Dates to confirm\\\" group after the timeline until the paralegal picks one of the readings the code proposed. \"\n\"Charge dates: `tests/unit/test_t202_r3_allow_list.py`, `tests/unit/test_t202_r4_encounter.py` (131 tests; every reviewer probe from rounds 3 and 4 is a fixture) and `tests/unit/test_t200_undated_charge_label.py`; \"\n\"`evals/letter_check.charge_date_violations`, an independent per-line scanner over 25 cases that does not import the production parser (it reads the same `encounter_types.json`, with its own matcher) and accepts the blank, whole and exact, and nothing else for a line with no certain date. \"\n\"The T-202 r4 handoff reports a one-off mutation run on a scratch copy (24 of 25 mutants failed the unit suite, the 25th judged equivalent); that harness is not committed, so the run cannot be repeated from the repo.\"\n)\nc2[1] = row2_code\nc3[1] = row3_code\nc3[3] = val3\nlines[i2] = \" | \".join(c2)\nlines[i3] = \" | \".join(c3)\nopen(p, \"w\", encoding=\"utf-8\").write(\"\\n\".join(lines))\nEOF\npython3 -I /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/rw.py && git diff --stat -- docs/LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T01:59:55.539Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/rw.py", line 9, in <module>
    assert len(c2) == 4 and len(c3) == 4, (len(c2), len(c3))
AssertionError: (5, 5)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:00.955Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/rw.py && sed -i 's/len(c2) == 4 and len(c3) == 4/len(c2) == 5 and len(c3) == 5/; s/^c2\\[1\\] = row2_code/c2[2] = row2_code/; s/^c3\\[1\\] = row3_code/c3[2] = row3_code/; s/^c3\\[3\\] = val3/c3[4] = val3 + \" |\"/' $S && python3 -I $S && git diff --stat -- docs/LLM_VS_CODE.md && git diff -- docs/LLM_VS_CODE.md | grep -c '^[-+]|'; sed -n 31p docs/LLM_VS_CODE.md | tail -c 200"
}
````

### User / tool · 2026-11-03T02:00:01.085Z

**tool result**
````
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/rw.py'
fixture; 24 mutants of the resolver and the check all fail the unit suite) and `evals/letter_check.charge_date_violations`, which accepts the blank and nothing else for a line with no certain date. |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:06.984Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/rw.py && sed -i '' 's/len(c2) == 4 and len(c3) == 4/len(c2) == 5 and len(c3) == 5/; s/^c2\\[1\\] = row2_code/c2[2] = row2_code/; s/^c3\\[1\\] = row3_code/c3[2] = row3_code/; s/^c3\\[3\\] = val3/c3[4] = val3 + \" |\"/' \"$S\" && python3 -I \"$S\" && git diff --stat -- docs/LLM_VS_CODE.md && git diff -- docs/LLM_VS_CODE.md | grep -c '^[-+]|'; sed -n 31p docs/LLM_VS_CODE.md | tail -c 150; sed -n 30p docs/LLM_VS_CODE.md | grep -o \"| The spec says date arithmetic.*\""
}
````

### User / tool · 2026-11-03T02:00:07.200Z

**tool result**
````
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
4
y (24 of 25 mutants failed the unit suite, the 25th judged equivalent); that harness is not committed, so the run cannot be repeated from the repo. |
| The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:11.785Z

**tool call — Bash**
````
{
 "command": "sed -n 188,198p app/backend/store.py"
}
````

### User / tool · 2026-11-03T02:00:11.874Z

**tool result**
````
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:17.538Z

**tool call — Bash**
````
{
 "command": "sed -i '' \"s/the app's own export always carries \\`dos_iso\\`\\./the app's own export carries \\`dos_iso\\` for every charge./\" docs/LLM_VS_CODE.md && grep -c \"for every charge\\.\" docs/LLM_VS_CODE.md && git diff --stat -- docs/LLM_VS_CODE.md && python3 tools/check_secrets.py docs/LLM_VS_CODE.md 2>&1 | tail -2\nT=$(mktemp /private/tmp/claude-501/idx.XXXXXX); rm -f \"$T\"; export GIT_INDEX_FILE=\"$T\"; git read-tree HEAD && git add docs/LLM_VS_CODE.md && git commit -q -m \"docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code: same-period rule, 1830-day bound on every record, encounter-record date, counted-line no note, mutant claim (T-207)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md; unset GIT_INDEX_FILE; git log --stat -1 --format=%h | tail -3"
}
````

### User / tool · 2026-11-03T02:00:17.606Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:18.607Z

Hook rejected the compound; splitting into steps.

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:19.641Z

**tool call — Bash**
````
{
 "command": "sed -i '' \"s/the app's own export always carries \\`dos_iso\\`\\./the app's own export carries \\`dos_iso\\` for every charge./\" docs/LLM_VS_CODE.md && grep -c \"for every charge\\.\" docs/LLM_VS_CODE.md && git diff --stat -- docs/LLM_VS_CODE.md && python3 tools/check_secrets.py docs/LLM_VS_CODE.md 2>&1 | tail -2"
}
````

### User / tool · 2026-11-03T02:00:19.715Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:20.698Z

The backticks/escaped quote in the sed are the problem; using the Edit tool.

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:21.848Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/docs/LLM_VS_CODE.md",
 "old_string": "the app's own export always carries `dos_iso`.",
 "new_string": "the app's own export carries `dos_iso` for every charge."
}
````

### User / tool · 2026-11-03T02:00:21.920Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/docs/LLM_VS_CODE.md has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:22.187Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- docs/LLM_VS_CODE.md && python3 tools/check_secrets.py docs/LLM_VS_CODE.md 2>&1 | tail -2"
}
````

### User / tool · 2026-11-03T02:00:41.096Z

**tool result**
````
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
check_secrets: ok (3734 file(s) scanned)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:43.711Z

**tool call — Bash**
````
{
 "command": "rm -f /private/tmp/claude-501/t207.idx && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git add docs/LLM_VS_CODE.md && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git commit -q -m \"docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)\" -m \"Same-period rule, 1830-day bound on every record, encounter-record date, counted line carries no note, mutant claim limited to the handoff.\" -m \"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md && git log -1 --stat --format=%h"
}
````

### User / tool · 2026-11-03T02:00:43.838Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: rm -f /private/tmp/claude-501/t207.idx && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git add docs/LLM_VS_CODE.md && GIT_INDEX
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:46.098Z

**tool call — Bash**
````
{
 "command": "rm -f /private/tmp/claude-501/t207.idx && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git add docs/LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T02:00:46.435Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:48.341Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/t207.idx git commit -q -m \"docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)\" -m \"Same-period rule, 1830-day bound on every record, encounter-record date, counted line carries no note, mutant claim limited to the handoff.\" -m \"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- docs/LLM_VS_CODE.md && git log -1 --stat --format=%h"
}
````

### User / tool · 2026-11-03T02:00:50.094Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
efda639

 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:55.301Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py ac T-207 --check 1 --agent architect --evidence \"docs/LLM_VS_CODE.md rows 2-3 rewritten from service_date.py, encounter_types.json, store.charge_service_date, export.charge_when at 8cb5bd2; commit efda639\" && python3 tools/board.py handoff T-207 --agent architect --text \"What changed: rows 2-3 rewritten against 8cb5bd2. Majors: (1) same-period rule stated (another end forces the order; no record locale), then statement rule, needs a record date; (2) bound stated as 1,830 days (5x366), on every record, no bound without a record date, can read a few days past five calendar years; (3) encounter-record date default stated with R-TL-3 and D-071 amendment 2, encounter_types.json, bad labeled date in an encounter prints the blank not the header date; (4) counted (D-064) line prints the blank with no note; (5) mutant claim cut to the T-202 r4 handoff (24 of 25, scratch run, harness not committed). Minors: heading set listed, two note forms, billing dos_iso not a charge date. Verified: read code, check_secrets ok, diff is 2 table rows. Left: bound is day arithmetic in code (reviewer asked for calendar years): card for backend if wanted. Surprised me: store.py, not export.py, holds the encounter default and the counted-line rule.\" && python3 tools/board.py commit T-207 --sha efda639 --agent architect && python3 tools/board.py move T-207 in_review --agent architect"
}
````

### User / tool · 2026-11-03T02:00:55.671Z

**tool result**
````
AC 1 checked: docs/LLM_VS_CODE.md rows 2-3 rewritten from service_date.py, encounter_types.json, store.charge_service_date, export.charge_when at 8cb5bd2; commit efda639
handoff written on T-207
T-207: commit efda639 recorded
T-207: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:00:57.918Z

T-207 rows 2 and 3 are rewritten against the 8cb5bd2 code and committed as efda639 (`docs/LLM_VS_CODE.md` only, temp index), and the card is in_review. All 5 majors are covered. The five-year bound is documented as the code's 1,830 days, not calendar years, and the code isn't changed, so the reviewer's calendar-year fix is still open. The mutation claim is cut to the T-202 r4 handoff's uncommitted scratch run (24 of 25 killed).
