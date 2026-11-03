# Subagent: Architect: T-207 row 3 correction (Architect: T-207 row 3 correction)

Source: `agent-a533f71e029ef0c65.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:26:04.269Z

You are the architect in /Users/arsis/zlayt-pm-project on T-207. Read the correction note the T-202 backend worker left on T-207 and on T-202 (`python3 tools/board.py show T-207`). It gives the exact replacement text for row 3 of docs/LLM_VS_CODE.md: the not-certain form is now the fillable blank "date of service [__________] (statement dated X)".

Apply it, matching the code at commit 973b542. Commit only that file through `git commit` with a temp index built from the current HEAD, note the commit on T-207, leave T-207 in_review, and reply in 1 line.

### User / tool · 2026-11-03T01:26:04.274Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:06.412Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-207 && echo ---- && python3 tools/board.py show T-202",
 "description": "Show cards T-207 and T-202"
}
````

### User / tool · 2026-11-03T01:26:06.596Z

**tool result**
````
---
id: "T-207"
title: "LLM_VS_CODE rows 2 and 3: charge-line service dates are an allow-list of positive evidence (T-202 r3, D-071 amendment)"
milestone: "M3"
role: "architect"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T00:45:18Z"
updated_at: "2026-11-03T00:51:33Z"
claimed_by: "architect"
claimed_at: "2026-11-03T00:46:49Z"
rounds: 0
commits: ["901ad5a"]
reviews: []
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

## Handoff
What changed: LLM_VS_CODE row 2 (code-only allow-list: DOS/service column header, service label, the row's own date cell, the bill's one stated period; statement-date disambiguation 'a service cannot follow its statement'; unreadable years/dates not read; entry dates stay strict) and row 3 (charge-line exception: fillable blank + Step 3 confirm note when not certain, as-written form, 'service date not stated' form; validation cell names test_t202_r3_allow_list and letter_check.charge_date_violations). Verified: git diff shows only those 2 rows; commit 901ad5a via temp index, secrets check ok. Left: nothing in docs. Surprised me: the D-071 addendum's fillable blank ('date of service [__________] (statement dated X)') is not in the code at 5703fc4 (store.charge_service_date/service_date.printed_text print the 'as written' and 'service date not stated' forms; no card covers the blank), so the doc states the decided rule ahead of the code; backend needs a card.

----
---
id: "T-202"
title: "D-071: letter charge lines print the bill's service date or period, not the statement date (case_09, lib14, lib10)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T23:26:04Z"
updated_at: "2026-11-03T01:25:49Z"
claimed_by: "backend"
claimed_at: "2026-11-02T23:26:10Z"
rounds: 2
commits: ["f0921e4", "986fc55", "5703fc4", "973b542"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-202-paralegal.md", "at": "2026-11-02T23:48:12Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-202-staff-engineer.md", "at": "2026-11-02T23:55:16Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-202-paralegal-r2.md", "at": "2026-11-03T00:29:34Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-202-staff-engineer-r2.md", "at": "2026-11-03T00:30:26Z"}
ac:
  - {"n": 1, "text": "per D-071; case_09/lib14/lib10 letters show the service date/period; goldens updated with a diff in the handoff; evals/letter_check.py asserts each dated charge line's date equals the service date in its quote, over all 25 cases incl. a count path; unit + guided e2e green from git archive", "done": true, "evidence": "r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->any all killed; corpus charge headers byte-identical (84 lines)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T23:26:10Z backend: claimed
- 2026-11-02T23:29:45Z orchestrator: Also cover T-200 minor: the letter_check count path must include a counted undated line (lib11).
- 2026-11-02T23:37:08Z backend: AC 1 checked: tests/unit/test_t202_charge_service_dates.py (13 pass); python -m evals.letter_check value 0 over 25 cases incl. count variant, mutants (record-date printing; bare statement date) fail it with 48 / 20 violations; git archive tree df2e300b60: unit 1456+1478+1353+1597 passed, guided e2e 128 passed
- 2026-11-02T23:37:08Z backend: moved in_progress -> in_review
- 2026-11-02T23:37:13Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer
- 2026-11-02T23:48:12Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal.md; round 1; findings:
    - [blocker] Ledger table with the Posted column before DOS: the letter prints the posting date as the date of service — fix: Read the row's date by its column: use the ledger header (billing.py already parses DOS vs Posted columns, api.md GET /billing 'dos' vs 'posted'). When a row has two dates and no header says which is the DOS, use the T-200 form, not a guess.
    - [blocker] CMS-1500 listing two dates of service ('06/24/2026 and 07/08/2026'): every charge line gets the first date — fix: Inherit the record's date only for a true period (a range join). For a list of discrete dates with no per-line date, print the T-200 form, or name the claim dates without assigning one: 'Wardlaw Orthopedics, CMS-1500 (claim dates of service June 24 and July 8, 2026; lin
    - [major] Step 3 labels each dated bill charge with the statement date, not the date the letter prints; the API carries no service date — fix: Expose the D-071 service date or period on each charge in the case view (backend: dos_iso/dos_end_iso, or the T-200 'not stated' state). Show it on the Step 3 card exactly as the letter will print it, with the statement date labelled as such: 'Service J
    - [major] letter_check's date check accepts any service date the record states, not the line's own, so the wrong-date class passes; AC wording ('equals the service date in its quote') is not what it checks — fix: Pin the per-line expected date in the goldens: case_09, lib14 and lib10 expected letters, plus the T2/T3 probe shapes as SYNTHETIC cases. Make the check tie the date to the line's row
    - [minor] Some charge quotes name neither the service nor the date the line now prints (pre-existing quote span, unchanged by T-202) — fix: Quote the whole bill line from its code or description through the figure ('Rev 0120 room and board semi-private ... FL47 total charges $4,920.00.'; 'A0425 ground mileage, loaded, 8.7 miles ... charge $187.05.').
- 2026-11-02T23:48:15Z orchestrator: assigned: backend
- 2026-11-02T23:48:15Z orchestrator: Round 2 queued: starts when the staff r1 review lands (fold both). Paralegal blockers: ledger with Posted column before DOS prints the posting date; CMS-1500 with two service dates puts the first on every line; Step 3 still shows the statement date; letter_check passes the CMS-1500 mis-date.
- 2026-11-02T23:55:16Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-202-staff-engineer.md
- 2026-11-02T23:55:16Z orchestrator: Errata for reviews/T-202-staff-engineer.md: the 'two service dates' evidence is amounts.py:500 (non-row) and :493 (row), not :507.
- 2026-11-02T23:55:16Z orchestrator: Round 2 per the D-071 amendment (print a date only when certain; otherwise the not-stated form + Step 3 confirm note). Fold all paralegal and staff r1 blockers/majors; adversarial layout fixtures; independent per-line letter_check; Step 3 shows the same date as the letter (frontend may need a field: put it in the API and tell the orchestrator).
- 2026-11-02T23:55:32Z orchestrator: assigned: backend
- 2026-11-02T23:55:32Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:00:59Z backend: r2 started: adversarial fixtures tests/unit/test_t202_r2_service_date_layouts.py written first, RED on f0921e4 code: 33 failed, 15 passed. Rule I will implement: print a date only when exactly one unambiguous date/complete period is tied to the line by header/row; ambiguous numeric resolved only when one reading is after the record's own date (a service cannot follow its statement) else not-stated.
- 2026-11-03T00:16:07Z backend: r2 committed 986fc55 (unit/e2e from git archive running). New: app/backend/service_date.py; fixtures tests/unit/test_t202_r2_service_date_layouts.py (33 red on f0921e4 -> 0); letter_check rewritten (own scanner); API field amounts[].service_date. Corpus letters byte-identical to f0921e4 (84 charge lines diffed).
- 2026-11-03T00:16:38Z backend: AC 1 checked: r2 986fc55: tests/unit/test_t202_r2_service_date_layouts.py 48 cases (33 red on f0921e4 -> all pass); letter_check value 0 over 25 cases, mutants fail it (drop period end 16, record date 28, bare statement 20, record first date 6); unit + guided e2e from git archive 986fc55 (see handoff)
- 2026-11-03T00:19:45Z backend: moved in_progress -> in_review
- 2026-11-03T00:19:55Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer
- 2026-11-03T00:29:34Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r2.md; round 2; findings:
    - [blocker] A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date — fix: Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or referred, ordered, admit or admission when it stands alone, and 'date of current'. Such a date never 
    - [major] Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter — fix: Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; service date not stated)'. A date written but not certain: show it verbatim, without reading it: '(date of s
    - [minor] The not-stated string differs from the one quoted in the D-071 amendment — fix: Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.
    - [minor] A ledger column headed 'Trans Date' is read as the date of service — fix: Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.
    - [minor] A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill — fix: Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The bill states a period (...) the code could not tie to this line').
    - [minor] Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now) — fix: Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm_note), and 'request a dated itemized bill'.
    - [minor] Carried from round 1: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T00:29:34Z orchestrator: assigned: backend
- 2026-11-03T00:29:34Z orchestrator: Round 3 queued until staff r2 lands. Paralegal r2 blocker: a date in prose (birth/injury/onset/referral/order) prints as DOS -> per D-071 amendment a date counts only if tied to a DOS column header, a DOS/service label ('DOS', 'date of service', 'service date', 'seen on', 'visit date') or the charge row's own date cell; any other date = not certain. Major: 'not stated' printed above quotes that do state one.
- 2026-11-03T00:30:26Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r2.md
- 2026-11-03T00:30:26Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read."
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service." Append to the "Validation" cell: " Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser)."
- 2026-11-03T00:45:37Z backend: (correction: the two empty notes above were a shell slip; the exact LLM_VS_CODE text for the architect is in the note just above and on T-207.)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints "(statement dated X; service date not stated)". Both are gone. Replace those two sentences with exactly: "Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it." Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date.
- 2026-11-03T01:25:40Z backend: AC 1 checked: r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->any all killed; corpus charge headers byte-identical (84 lines)
- 2026-11-03T01:25:40Z backend: moved in_progress -> in_review
- 2026-11-03T01:25:49Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r3, 5703fc4 + 973b542): service_date.py is now an ALLOW-LIST: a date is the service date only if a column heading names service (DOS, date of service, from/to service, 24A ...), a service label ends its clause (DOS, date of service, seen on, visit date, visit of, run of; UB-04 'statement covers period'), it is the row cell under such a heading, or (coded bill line with no label) the bill's one period-labeled date. Birth/injury/onset/referral/order/entry/transaction/posted/statement/unlabeled dates are never read; a visit note keeps its own date. Unreadable-but-labeled dates (ambiguous, 2-digit year incl. 'Mar 5, 26', no year, invalid, several, after the statement or >5y before it) and no-label lines ALL print the D-071 addendum blank 'date of service [__________] (statement dated X)' (export.charge_when, store.charge_service_date; confirm_note names the date as written; notes get a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section). evals/letter_check.py: own allow-list scanner (string phrase list, own heading test), accepts the blank and nothing else for a not-certain line, fails a date no label ties, a blank above a certain labeled date, a wrong statement date. api.md updated. | Verified from git archive 973b542: unit 6121 passed/14 skipped, guided e2e 143 passed, letter_check 0 over 25 cases; corpus charge headers byte-identical to 986fc55 (84 lines). New test_t202_r3_allow_list.py: 144 cases, every paralegal/staff probe (B3,B7-B12,N5,N11,N12,N14,N16,N17,P10, Entry/Transaction/Issued/Printed headings, DOI/DOB/authorization, 1998/2031, Mar 5 26, all-vs-any), red first (74 failed on 986fc55 before the fix), 24 mutants (resolver, store, export, letter_check; all->any among them) all killed; production letter vs independent check agree on 45 layouts. | Left: Step 3 frontend text 'type the date into your letter yourself' still describes the old no-blank flow (frontend card); architect T-207 row 3 must be corrected to the blank wording (note on T-207); not done: quote-span minor (charge quotes naming neither service nor date) and a Step 3 control to enter a confirmed date. Crossings: edited tests/e2e/guided/test_round2.py + test_t205.py (one assertion each) and tests/unit test_t200/test_t202_charge (new blank text). | Surprise: a bare 'Date' column and unlabeled leading dates (03/13/2026 exam charge) are now not-certain by the allow-list; existing r2 fixtures needed DOS labels.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:09.729Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -5 && git status --short | head -30 && echo ---- && git show --stat 973b542 | head -30 && echo ---- && grep -n \"\" docs/LLM_VS_CODE.md | grep -n \"date\" | head -40",
 "description": "Check git state, recent commits and date mentions in doc"
}
````

### User / tool · 2026-11-03T01:26:09.916Z

**tool result**
````
8aa14e1
8aa14e1 test(qa): T-208 r2 the AI translation label is exempt only with a translated entry's quote; label on an English letter fails
679b63e fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
b96c08f test(qa): T-208 letter_check fails any AI or model wording in every carrier letter (25 cases, prepared and live); matrix e2e binds the provenance line to the case kind
973b542 feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
901ad5a docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/frontend/guided/app.js
 M app/frontend/judges.js
 M artifacts/screenshots/guided/home-1440.png
 M artifacts/screenshots/guided/home-390.png
 M artifacts/screenshots/guided/home-empty-1440.png
 M artifacts/screenshots/guided/step1-drafting-1440.png
----
commit 973b54228670299495bd16dbf0072e248a43baf0
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:51:17 2026 -0600

    feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/export.py                           |  6 +-
 app/backend/service_date.py                     | 39 +++++--------
 app/backend/store.py                            |  5 +-
 evals/letter_check.py                           | 47 ++++++----------
 memory/contracts/api.md                         |  2 +-
 tests/e2e/guided/test_round2.py                 |  2 +-
 tests/e2e/guided/test_t205.py                   |  2 +-
 tests/unit/test_t200_undated_charge_label.py    |  8 +--
 tests/unit/test_t202_charge_service_dates.py    |  6 +-
 tests/unit/test_t202_r2_service_date_layouts.py | 16 +++---
 tests/unit/test_t202_r3_allow_list.py           | 73 ++++++++++++++-----------
 11 files changed, 98 insertions(+), 108 deletions(-)
----
7:7:A paralegal turns scattered medical records into a treatment chronology, and an adjuster will read it looking for a reason to doubt it. One invented detail costs credibility. So we split the work by one question: **is there a single right answer?** If yes (a date, the days between two dates, a dollar total, whether a quote really appears in the record), ordinary code does it, because code is right every time and can be tested. If it takes reading messy human language (what happened in this visit, whether "findings may represent degenerative change" weakens a causation argument), a language model does it, and then its answer has to pass three checks before it can reach the letter: a code check, an independent second model acting as a skeptic, and the paralegal's own accept, edit or dismiss. Nothing the model wrote goes into the export without all three. Even then, the model never writes the wording of a warning: code does.
11:11:1. **Arithmetic, dates, totals, sorting, de-duplication, quote-matching, number-matching, schema checks and export assembly are never done by a model.**
12:12:2. **The model never supplies a value.** It may write a one-line summary and choose an exact excerpt, and point at wording that looks like a flag (a category and a quote). It may not supply a date, an amount, an amount's class or the text of a warning. A date or amount the code cannot find in the record is rejected.
14:14:4. **Every number in a summary is checked.** Any number, date or dollar figure, and the words left/right/no/not/without, in a summary or in the paralegal's own edit must appear in the excerpt. In a generated summary a miss marks the item for review with the offending tokens named. In a paralegal's edit or manual entry it is a hard 422 and nothing is saved, with no override (D-034, D-047).
15:15:5. **A second model double-checks the first, and every dollar classification.** The checker uses a different prompt and, by default, a different model. It sees only the record and the candidate, never the first model's reasoning, and answers with a fixed choice (no prose).
16:16:6. **No silent fixes.** When a check fails the system says so and why. It never "repairs" a quote, a date or an amount.
29:29:| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
30:30:| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendment; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** Only a date tied to the line by a DOS or service column header, by a service label in its clause (DOS, date of service, service date, seen on, visit date), by the charge row's own date cell in a table whose header names service, or by the one period its bill states for its services counts. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. A numeric date that reads two ways is resolved by one fixed rule: a service cannot follow its statement, so it is certain only when a reading after the bill's own (statement) date is impossible for every labeled end of the date or period (D-071 clarification). This is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
31:31:| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is not the record's header date (a bill's header date is its statement date) and the model is never asked. Code prints the service date or period the bill line itself states (positive evidence only, see row 2). When it is not certain, the letter does not guess: it prints a fillable blank beside the statement date (D-071 addendum: "date of service [__________] (statement dated June 15, 2026)") and Step 3 shows a confirm note asking the paralegal to read the date from the quote. A date the quote labels as the date of service but the code cannot read with certainty also shows as written ("04/05/2026"). When the quote labels no date at all, the line says "(statement dated X; service date not stated)". | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. Charge dates: `tests/unit/test_t202_r3_allow_list.py` (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and `evals/letter_check.charge_date_violations`, an independent per-line scanner over 25 cases that does not import the production parser. |
32:32:| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in the record). The summary is split into clauses, and a clause is removed only when it adds **salient new content** its quote lacks: a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term (`new_salient`, `summary_trim.py:325-356`). Terms are matched by word family (Tylenol with acetaminophen, cervical with neck) after clinical abbreviations are expanded on both sides (`expand_abbreviations`, `:108`; families `:212-267`), so a faithful paraphrase stays and judge 1 checks it. The negation and side words come from the lexicon (`code_lists.added_qualifier` through `grounding`, `summary_trim.py:269`, `:338-342`), not from a list in the trim. A number, side or negation counts only in a clause that shares no content word with the quote; a changed value on the quote's own topic ('Pain 3/10' over 'Pain 4/10') stays and is caught by the rung 1 token checks. A **structural no-fragment rule** (no word list; `:417-423`, T-128 r3): code trims only a **suffix**. A clause is removed only when every clause after it is removed too, so the kept text is always a prefix of whole clauses and no kept clause can follow a removed one (`'Wrist pain 6/10; splint fitted; patient tolerated well.'` over a quote that supports only the first and last clause is returned unchanged). The first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix needs at least 2 content words. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`). Each removal is shown in the trace as 'removed from the summary: not in the quote'. If every clause is removed, or what is left has no content word, the item goes to the could-not-verify tray with `SUMMARY_NOT_IN_QUOTE` (`summary_trim.py:414-415`; `generator.py:75-77`; template `why.py:33`) and is never judged. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
37:37:| 9 | Treatment gap longer than 30 days | **Code** over the code-parsed **record dates** of all (de-duplicated) clinical-encounter records (billing statements and phone notes are excluded), independent of any model output or review state. Strictly more than 30 days; 30 is not a gap. | A gap is a fact about dates. If it depended on the model's entries, one dropped entry would invent a gap. | Unit tests at 29, 30, 31 days; sample 28-day near miss does not flag, 73-day gap does; dropping an entry never changes the result. Ambiguous dates are excluded, shown as a record warning, and any gap near one needs review; she resolves one by choosing a reading the code proposed (`confirm_date`). |
38:38:| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**: a lexicon of accident-date phrases ("date of accident", "DOA", "accident date", "collision on") plus date formats, compared with the earliest record date. Evidence is the stated-date quote and the `Date:` header line(s) of the earliest records. | Comparing two dates is not a language task, and the header line is part of the input text. | Unit test on the sample file with exact character offsets; both quotes ground; the two dates are shown side by side and never merged. No judge needed (arithmetic over quoted text). |
39:39:| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems versus a history sentence in another record | **Code proposes; the LLM only classifies.** `app/backend/conflict_candidates.py` pairs two whole sentences by two fixed rules: **plan vs early end** (a stated plan, as a visit count or frequency × duration, against a LATER record showing a missed, no-show, cancelled, self-discharged or discontinued course; `plan_vs_outcome`, `:133-148`) and **denial vs prior history** (a sentence denying prior problems, against a sentence in another record that the phrase list marks as a prior condition or prior surgery, or that names an earlier accident or claim; `history_denials`, `:151-175`). **The rules drop pairs before any model sees them:** (1) *different person:* a sentence whose subject is a relative or another party from a closed list (the other driver, a witness, mother, husband, "family history") and that does not name the patient is never half of a candidate, on either side (`_other_person`, `:73-76`, applied at `:101`, `:138`, `:155`, `:166`, `:169`); a person the list does not name still reaches the judge, whose prompt is the backstop. (2) *across a semicolon:* the subject is read inside the sentence's own semicolon clause (the splitter cuts at ';'), so a relative named in the neighbouring clause neither hides the patient's own history nor is paired with it (`tests/unit/test_conflict_candidates.py::test_the_subject_is_read_inside_its_own_semicolon_clause`). (3) *intake forms:* a paperwork record (intake form, bill, affidavit, by the header test `gaps.admin_label`) is never the plan or the outcome of a course (`:79-83`, `:98`, `:138`; `::test_an_intake_form_is_never_the_plan_or_the_outcome_of_a_course`); a denial written on an intake form is still the patient's own statement and is compared. Code multiplies frequency × duration into visits ("2x/week for 6 weeks" = 12) and carries that arithmetic on the flag. An explicit visit count is the plan quoted when one exists. No numeric comparison is made between a count and a frequency plan, so the two are not checked against each other. Candidates come in a fixed order, so the set cannot vary between runs: there is no open-ended model search (`conflicts_v1` is retired). The model is `judge_conflict_v6` (J3; `judges.py:59`), and it only classifies each candidate as `conflict`, `benign` or `unsure`, with a fixed reason code and no prose. It never proposes a pair, a quote or a number. **Nothing the model produces is silently dropped (D-053):** a code-proposed pair that J3 calls `benign` goes to the could-not-verify tray (tray kind `flag`, reason `JUDGE_DISAGREES`, with the judge's fixed reason); a model-only flag that the flag judge (J4, `judge_flag_v3`, `judges.py:64`) calls `disagree` goes to the tray the same way (`flags.py:349-352`; `present.py:290-300`); a conflict the model proposed in the per-record pass, which no code candidate made, goes to the tray with `LLM_ONLY` and is not judged (`_model_conflicts`, `flags.py:185-209`, called at `:265`; backstop in `judge_flags`, `:381-383`, for a conflict handed in directly). The tray-on-no-candidate rule is for conflicts only: a model-only flag that J4 does not reject stays `needs_review` (`LLM_ONLY`), and a flag the phrase list also found stays `needs_review` even if J4 disagrees. Tray items are never flags and never reach the letter. A J3 or J4 `unsure` answer, or a judge that did not answer, keeps the flag visible as `needs_review`. **Candidate rules** also cover number-word visit counts with a plan cue, frequency × duration in weeks (including "twice-weekly for six weeks"), lost to follow-up, stopped or left care, negation- and completion-aware, and denials of earlier accidents or claims. **Not built as candidates:** dosage and laterality pairs (laterality is checked only within one summary, row 15), and month durations (`memory/SCOPE_CUTS.md`, row 13). Dosage and laterality pairs are neither proposed by code nor measured: every J3 control is a pair the candidate generator proposes (real packet candidates and variants of them, `evals/j3_controls.py`, checked by `tests/unit/test_t093_j3_controls_reachable.py::test_every_j3_control_input_is_producible_by_the_candidate_generator`), and the earlier dose, laterality, date and pain-score controls were removed for that reason (T-093 r4, 822ff38; `evals/golden/judge_controls.CHANGELOG.md`). | Reading comprehension is needed only for one yes or no per pair. An open-ended search let the model call "2x/week for 6 weeks" against "12 visits" a conflict (T-094, live run 2). The arithmetic and the choice of pairs are code's. | **Rung 1:** both quotes are whole sentences cut from the record text, and grounding still checks them. **Rung 2, J3:** `conflict` gives a flag (verified only when the other checks hold); `unsure` keeps it `needs_review`; `benign` on a code-proposed pair moves it to the could-not-verify tray, never exported. A denial is judged one candidate at a time, in record order, and the first confirmed conflict stands. **Rung 3:** human accept or dismiss. |
42:42:| 14 | The wording of every flag | **Code**: a fixed template per flag type and category, filled with dates, source labels and the verbatim quote. For example "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient)". | A model explaining a flag is another unverified claim, and the place it would be tempted to rule on causation. | The model's output schema has no prose field; a test rejects extra fields. |
43:43:| 15 | Numbers and dates in a summary or in the paralegal's edit | **Code**: every number, date, dollar figure and left/right/no/not/without in the text must be in the excerpt (or the record's source line / parsed date), and qualifiers in the excerpt must not be dropped from the summary (`SUMMARY_DROPS_QUALIFIER`). | The most likely invented fact is a changed number. A small judge model can miss it; code cannot. | Unit tests: "Pain 9/10" over "Pain 4/10" is flagged; an edit adding "$9,000" is refused with a 422 and nothing is saved (D-034, D-047). There is no "keep my wording" override. Accept is refused while the current wording fails any code check, single or batch (`422 CODE_CHECK_FAILED`, D-051). |
47:47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, a date of service, and an exhibit/Bates placeholder. The total line is always exactly "Billed charges stated in these records: $X" (accepted charges only), with no clause about anything else. Flags and unclear amounts go to a separate internal-notes block, never the letter. The format is `spec/REQUIREMENTS.md` section 6 and the golden file. Export gate (D-044, D-045): an accepted model-made item whose second check never ran blocks the export, with no override; pending items do not block it. | Deterministic, and the letter must never carry anything unquoted. | Unit and E2E: dismissed and pending items never export; every exported excerpt is in the input; same accepted set gives the same bytes. The internal notes list "flagged language quoted in the letter" so the attorney decides whether it stays. |
56:56:  [ LLM generator ]  --- candidate: summary, excerpt, flag category + quote ---+
61:61: RUNG 2: independent LLM judge  (other prompt, other model, sees only record + candidate, answers with a fixed choice)
66:66: RUNG 3: paralegal  accept | edit | dismiss     (nothing automatic; amounts and dates always explicit)
74:74:Record 7 (Hill Country Pain Management, header date 2026-05-18): *"New onset pain radiating to right arm ... Date of accident per intake form: 2026-01-19."*
76:76:- **Code** takes the header date (2026-05-18) as the date of service. The model is not asked.
78:78:- **Code** notices a stated accident date of 2026-01-19 that is later than treatment recorded on 2026-01-09 and raises a conflict, quoting both the intake-form phrase and the `Date:` header lines of records 1 and 2. The two dates are never merged. No model is involved.
79:79:- **Code** computes 73 days between the PT discharge (March 6) and this visit (May 18) and raises the gap flag. The 28-day interval earlier is not flagged. The 73 comes from record dates, so no model failure could change it.
96:96:- **Draft treatment paragraph in the firm's voice (model, behind the full ladder).** A model may draft a paragraph from **accepted entries only**. The **model returns the sentences**, each citing one accepted entry (`NarrativeOutput.sentences`); code does not re-split a paragraph. Code then checks **every returned sentence** against the quote of the entry it cites (each number, date and dollar figure must be in that quote or its header; hedges and qualifiers must be carried; no causation, severity or flag wording the quote lacks), judge 1 checks each remaining sentence against its source excerpt, and the paragraph stays **internal until she accepts it**. A sentence that fails a check is removed from the draft with a reason code and a plain message, so it can never be accepted; a sentence citing an entry that is not accepted is removed as well.
102:102:- **Numbers, sides, negations and qualifiers cannot be overridden (D-034, D-047).** A number, date, dollar figure, left/right, no/not/without, or dropped qualifier in a summary, edit or manual entry that the quote does not carry is a hard 422 and nothing is saved. There is no confirm or "keep my wording" path. The judge's objections to other wording are shown as warnings and the item stays `needs_review`. An accept that goes ahead despite a judge objection is counted in the judge summary, not blocked.
107:107:State that the collision caused a disc herniation. Convert "may represent degenerative change" into either "degenerative" or "traumatic". Compute a PT total when visit counts are not stated. Merge the two accident dates into one. Treat "concussion without loss of consciousness" as anything other than those words. Each is a golden-set check (`evals/golden`).
114:114:- **Determinism.** Temperature 0 is set where the backend allows it. The development backend cannot, so we measure agreement across three runs instead of assuming it. Code outputs (split, dates, gaps, amounts, totals) are identical across runs by construction.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:20.707Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- docs/LLM_VS_CODE.md; git diff --cached --stat -- docs/LLM_VS_CODE.md; echo \"--- HEAD vs worktree lines:\"; git show HEAD:docs/LLM_VS_CODE.md | diff - docs/LLM_VS_CODE.md | head -5; echo \"--- code at 973b542:\"; git show 973b542:app/backend/store.py | grep -n \"date of service\\|not stated\\|\\[__________\\]\" | head; git show 973b542:app/backend/export.py | grep -n \"date of service\\|not stated\\|__________\" | head; git show 973b542:app/backend/service_date.py | grep -n \"not stated\\|as written\\|__________\" | head",
 "description": "Check doc diff state and verify code at 973b542"
}
````

### User / tool · 2026-11-03T01:26:20.946Z

**tool result**
````
--- HEAD vs worktree lines:
--- code at 973b542:
120:    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 2026)'
124:    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
125:    not stated, with no note (she counted it knowing). Code only."""
139:    if not stated and not counted_undated:
147:    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
68:        return "date not stated"
216:        """D-071 (extends T-200): the label before a charge's amount in the letter. A date there reads as the date of service, so it is the service date the charge's own bill line
218:        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026)' (D-071 addendum: a fillable blank). Chosen over dropping the date
219:        because the adjuster can still match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict
531:            body = f"Rate {m}{per}; visit count not stated{_plan_note(v, n)}. Request itemized {_ledger_label(v, n)}."
608:    """T-202 r3: one line per accepted charge the letter prints without a certain date of service (the paralegal's to-do before the demand goes out): provider, amount, why, and the
613:            why = (a.get("dos_note") or "The line states no date of service.").split(" The letter prints")[0]
614:            out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.")
18:  Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
19:  and the letter never says "service date not stated" above a quote that states one.
58:WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
76:BLANK = "date of service [__________]"
81:    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
88:    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
306:    unlabeled date near the line for non_service_date), raws ([the labeled dates as written])} for the figure at `start` of `excerpt`, in a record with header `source` and date
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:28.291Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np = \"docs/LLM_VS_CODE.md\"\ns = open(p, encoding=\"utf-8\").read()\nold1 = ' A date the quote labels as the date of service but the code cannot read with certainty also shows as written (\"04/05/2026\"). When the quote labels no date at all, the line says \"(statement dated X; service date not stated)\".'\nnew1 = \" Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it.\"\nold2 = \"Charge dates: `tests/unit/test_t202_r3_allow_list.py` (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and `evals/letter_check.charge_date_violations`, an independent per-line scanner over 25 cases that does not import the production parser.\"\nnew2 = \"Charge dates: `tests/unit/test_t202_r3_allow_list.py` (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and `evals/letter_check.charge_date_violations`, which accepts the blank and nothing else for a line with no certain date.\"\nfor o, n in [(old1, new1), (old2, new2)]:\n    assert s.count(o) == 1, (s.count(o), o[:60])\n    s = s.replace(o, n)\nopen(p, \"w\", encoding=\"utf-8\").write(s)\nprint(\"ok\")\nEOF\ngit diff --stat -- docs/LLM_VS_CODE.md",
 "description": "Apply row 3 replacement text to the architect doc"
}
````

### User / tool · 2026-11-03T01:26:28.419Z

**tool result**
````
ok
 docs/LLM_VS_CODE.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:35.681Z

**tool call — Bash**
````
{
 "command": "TMPIDX=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207-index\" && rm -f \"$TMPIDX\" && GIT_INDEX_FILE=\"$TMPIDX\" git read-tree HEAD && GIT_INDEX_FILE=\"$TMPIDX\" git add -- docs/LLM_VS_CODE.md && GIT_INDEX_FILE=\"$TMPIDX\" git diff --cached --stat HEAD && GIT_INDEX_FILE=\"$TMPIDX\" git commit -q -m \"docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank\n\nReplaces the 'shows as written' and 'service date not stated' sentences with the D-071 addendum blank, as code does at 973b542 (store.charge_service_date, export.charge_when, service_date.py: every not-stated line prints 'date of service [__________] (statement dated X)'). Validation cell: 24 mutants, not 28.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && rm -f \"$TMPIDX\" && git reset -q -- docs/LLM_VS_CODE.md && git log --oneline -1 && git status --short -- docs/LLM_VS_CODE.md && echo \"clean-path-check-done\"",
 "description": "Commit only the doc via temp index and sync real index path"
}
````

### User / tool · 2026-11-03T01:26:35.780Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: TMPIDX="/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:40.240Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207-index\" git read-tree HEAD && GIT_INDEX_FILE=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207-index\" git add -- docs/LLM_VS_CODE.md && GIT_INDEX_FILE=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207-index\" git diff --cached --stat HEAD",
 "description": "Stage the doc into a temp index built from HEAD"
}
````

### User / tool · 2026-11-03T01:26:40.497Z

**tool result**
````
 docs/LLM_VS_CODE.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:44.614Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207-index\" git commit -q -m \"docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank\n\nReplaces the 'shows as written' and 'service date not stated' sentences with the D-071 addendum blank, as code does at 973b542 (store.charge_service_date, export.charge_when, service_date.py: every not-stated line prints 'date of service [__________] (statement dated X)'). Validation cell: 24 mutants, not 28.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && rm -f \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207-index\" && git reset -q -- docs/LLM_VS_CODE.md && git log --oneline -1 && git show --stat --format=%H HEAD | head -5 && git diff --cached --stat -- docs/LLM_VS_CODE.md; echo done",
 "description": "Commit the doc from the temp index and sync its real-index entry"
}
````

### User / tool · 2026-11-03T01:26:45.809Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
fc37fbc docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank
fc37fbcec0ebdb7705e4d91c2ad43afd67a82568

 docs/LLM_VS_CODE.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
done
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:49.472Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-207 --sha fc37fbc --agent architect && python3 tools/board.py note T-207 --agent architect --text \"Applied the backend correction (row 3, 'shows as written' and 'service date not stated' sentences replaced with the fillable blank; Validation cell 28 -> 24 mutants) to docs/LLM_VS_CODE.md, matching code at 973b542. Commit fc37fbc (temp index from HEAD, docs file only). Card left in_review.\" && python3 tools/board.py show T-207 | grep -E \"^status|^commits\" ",
 "description": "Record the commit and note it on card T-207"
}
````

### User / tool · 2026-11-03T01:26:49.710Z

**tool result**
````
T-207: commit fc37fbc recorded
noted on T-207
status: "in_review"
commits: ["901ad5a", "fc37fbc"]
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:51.501Z

**tool call — mcp__ccd_turn__wrap_up**
````
{
 "recap": "Applied the T-202 r3 correction to docs/LLM_VS_CODE.md row 3 (blank replaces the \"shows as written\" and \"service date not stated\" sentences; Validation mutant count is now 24), matching code at 973b542. Committed only that file as fc37fbc via a temp index from HEAD, noted on T-207, which stays in_review. Not verified: no test run, since the change is docs-only."
}
````

### User / tool · 2026-11-03T01:26:51.505Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__wrap_up hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:26:52.900Z

Row 3 of docs/LLM_VS_CODE.md now carries the fillable blank, committed as fc37fbc. T-207 has the commit noted and stays in_review.
