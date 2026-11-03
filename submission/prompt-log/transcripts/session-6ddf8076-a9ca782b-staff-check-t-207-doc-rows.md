# Subagent: Staff check: T-207 doc rows (Staff check: T-207 doc rows)

Source: `agent-a9ca782b4c8cf06d1.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:26:58.044Z

Check T-207 in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. Rows 2 and 3 of docs/LLM_VS_CODE.md were changed in commits 901ad5a and fc37fbc.

Confirm the rows match the code at HEAD (app/backend/service_date.py and export.py) and D-071 with all its amendments in memory/ORCHESTRATOR_DECISIONS.md:
- the date is code-only, never the LLM;
- an allow-list of positive evidence decides it;
- the statement-date disambiguation rule applies;
- the not-certain case gets the fillable blank plus a Step 3 confirm note.

Write reviews/T-207-staff-engineer.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:00.741Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-03T01:27:00.747Z

**tool result**
````
1	# Persona dossier — staff-engineer-reviewer
2	
3	## 1. Identity
4	**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
5	He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.
6	
7	## 2. Day-to-day context
8	- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
9	- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
10	- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.
11	
12	## 3. Goals and success criteria for this artifact
13	- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
14	- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
15	- Tests fail when the code breaks and pass reproducibly.
16	
17	## 4. Review checklist
18	1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
19	2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
20	3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
21	4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
22	5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
23	6. Money is handled as integer cents or `Decimal`, never float.
24	7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
25	8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
26	9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
27	10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
28	11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
29	12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
30	13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
31	14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
32	15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
33	16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
34	17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
35	18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
36	19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
37	20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- A silent fallback (e.g., on judge error, mark item `verified`).
42	- An LLM computes a date difference, a total, or decides what is exported.
43	- Float arithmetic on money; a total that includes the $185 rate.
44	- Tests that call the real API or pass even when the verifier is stubbed out.
45	- Secrets or `.env` contents in code, fixtures, or logs.
46	
47	## 6. Vocabulary
48	determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.
49	
50	## 7. How I review
51	1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
52	2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
53	3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
54	4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
55	5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
56	6. File findings with file:line and the command that reproduces them.
57	
58	## 8. Calibration
59	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
60	- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
61	- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
62	- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.
63	
64	## 9. Sources
65	- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
66	- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
67	- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
68	- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
69	- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
70	- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.
71	
72	## 10. Limits
73	Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
74	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:01.455Z

**tool call — Bash**
````
{
 "command": "git status --short | head -30; echo \"---LOG---\"; git log --oneline -n 12; echo \"---HEAD---\"; git rev-parse HEAD; echo \"---SHOW 901ad5a---\"; git show --stat 901ad5a | head -30; echo \"---SHOW fc37fbc---\"; git show --stat fc37fbc | head -30",
 "description": "Check git state, recent log, and the two named commits"
}
````

### User / tool · 2026-11-03T01:27:01.687Z

**tool result**
````
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
 M app/frontend/guided/step3.js
 M app/frontend/judges.js
 M artifacts/screenshots/guided/home-1440.png
 M artifacts/screenshots/guided/home-390.png
 M artifacts/screenshots/guided/home-empty-1440.png
---LOG---
fc37fbc docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank
8aa14e1 test(qa): T-208 r2 the AI translation label is exempt only with a translated entry's quote; label on an English letter fails
679b63e fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
b96c08f test(qa): T-208 letter_check fails any AI or model wording in every carrier letter (25 cases, prepared and live); matrix e2e binds the provenance line to the case kind
973b542 feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
901ad5a docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)
5703fc4 fix(backend): T-202 r3 D-071 amendment: a service date is an allow-list of positive evidence (label, service column, row cell, bill period); labeled but unreadable dates print as written; independent letter_check allow-list; notes section for undated charges
79714c6 feat(frontend): T-206 Step 3 names a bill document's date 'statement dated'; confirm note says what to do next
d23687e chore(guard): block git commit-tree and symbolic-ref (T-204 swapped a commit on HEAD by plumbing)
9b37b9c feat(frontend): no AI-worded fallback for a prepared item; refusal follows a late library (T-204)
105d212 fix(qa): T-187 r5 / T-198 r3 (D-072) prompt-log rules: gapped term matching, device stem + job-folder pieces, outside-name switch precedence, path tails, no wildcard on separators; rule tests; proof rebuild
203ac6a feat(frontend): T-205 guided Step 3 shows the date of service the letter prints (service_date.text) and the confirm note when it is not certain
---HEAD---
fc37fbcec0ebdb7705e4d91c2ad43afd67a82568
---SHOW 901ad5a---
commit 901ad5a7e63e0775d5b03d417ba97c5947495a03
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:47:27 2026 -0600

    docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
---SHOW fc37fbc---
commit fc37fbcec0ebdb7705e4d91c2ad43afd67a82568
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 19:26:45 2026 -0600

    docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank
    
    Replaces the 'shows as written' and 'service date not stated' sentences with the D-071 addendum blank, as code does at 973b542 (store.charge_service_date, export.charge_when, service_date.py: every not-stated line prints 'date of service [__________] (statement dated X)'). Validation cell: 24 mutants, not 28.
    
    Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>

 docs/LLM_VS_CODE.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:04.787Z

**tool call — Bash**
````
{
 "command": "git show 901ad5a -- docs/LLM_VS_CODE.md; echo \"===FC37 DIFF===\"; git show fc37fbc -- docs/LLM_VS_CODE.md; echo \"===TABLE HEAD===\"; grep -n \"\" docs/LLM_VS_CODE.md | head -80",
 "description": "Show the two doc commits and the LLM_VS_CODE table"
}
````

### User / tool · 2026-11-03T01:27:04.930Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:05.288Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-207 2>&1 | head -120; echo \"====\"; ls reviews/ | grep -i \"T-207\" ; ls -la reviews | head -5",
 "description": "Show T-207 card and existing reviews for it"
}
````

### User / tool · 2026-11-03T01:27:05.621Z

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
updated_at: "2026-11-03T01:26:55Z"
claimed_by: "architect"
claimed_at: "2026-11-03T00:46:49Z"
rounds: 0
commits: ["901ad5a", "fc37fbc"]
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
- 2026-11-03T01:26:49Z architect: Applied the backend correction (row 3, 'shows as written' and 'service date not stated' sentences replaced with the fillable blank; Validation cell 28 -> 24 mutants) to docs/LLM_VS_CODE.md, matching code at 973b542. Commit fc37fbc (temp index from HEAD, docs file only). Card left in_review.
- 2026-11-03T01:26:55Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: LLM_VS_CODE row 2 (code-only allow-list: DOS/service column header, service label, the row's own date cell, the bill's one stated period; statement-date disambiguation 'a service cannot follow its statement'; unreadable years/dates not read; entry dates stay strict) and row 3 (charge-line exception: fillable blank + Step 3 confirm note when not certain, as-written form, 'service date not stated' form; validation cell names test_t202_r3_allow_list and letter_check.charge_date_violations). Verified: git diff shows only those 2 rows; commit 901ad5a via temp index, secrets check ok. Left: nothing in docs. Surprised me: the D-071 addendum's fillable blank ('date of service [__________] (statement dated X)') is not in the code at 5703fc4 (store.charge_service_date/service_date.printed_text print the 'as written' and 'service date not stated' forms; no card covers the blank), so the doc states the decided rule ahead of the code; backend needs a card.

====
total 16576
drwxr-xr-x@ 514 arsis  staff   16448 Nov  2 19:21 .
drwxr-xr-x   37 arsis  staff    1184 Nov  2 16:15 ..
-rw-r--r--@   1 arsis  staff    9315 Nov  1 19:20 CONTRACT-M2M3-paralegal.md
-rw-r--r--@   1 arsis  staff   13530 Nov  1 19:19 CONTRACT-M2M3-product-manager.md
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:08.807Z

**tool call — Bash**
````
{
 "command": "awk 'NR>=27 && NR<=40' docs/LLM_VS_CODE.md | awk -F'|' '/^\\| [23] \\|/ {print \"ROW \" $2 \"\\nCODE: \" $4 \"\\nWHY: \" $5 \"\\nCHECK: \" $6 \"\\n----\"}'; echo \"=== HEAD row 2/3 raw line lengths ===\"; git show HEAD:docs/LLM_VS_CODE.md | grep -n \"^| [23] |\" | cut -c1-20",
 "description": "Extract table rows 2 and 3 cells from LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T01:27:08.858Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to =27 && NR<=40)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:09.314Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head -40; echo \"---\"; wc -l memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Locate D-071 and its amendments in ORCHESTRATOR_DECISIONS"
}
````

### User / tool · 2026-11-03T01:27:09.411Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
---
      93 memory/ORCHESTRATOR_DECISIONS.md
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:12.070Z

**tool call — Bash**
````
{
 "command": "sed -n '84,93p' memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Read D-071 and its amendments in full"
}
````

### User / tool · 2026-11-03T01:27:12.154Z

**tool result**
````
## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.

## D-071 amendment — when the service date is not certain, print none and ask the human
T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.

## D-072 — The prompt log is built and privacy-reviewed once, last
Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:12.489Z

**tool call — Bash**
````
{
 "command": "git show HEAD:docs/LLM_VS_CODE.md | sed -n '29,31p'",
 "description": "Read the HEAD version of table rows 2 and 3"
}
````

### User / tool · 2026-11-03T01:27:12.589Z

**tool result**
````
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendment; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** Only a date tied to the line by a DOS or service column header, by a service label in its clause (DOS, date of service, service date, seen on, visit date), by the charge row's own date cell in a table whose header names service, or by the one period its bill states for its services counts. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. A numeric date that reads two ways is resolved by one fixed rule: a service cannot follow its statement, so it is certain only when a reading after the bill's own (statement) date is impossible for every labeled end of the date or period (D-071 clarification). This is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is not the record's header date (a bill's header date is its statement date) and the model is never asked. Code prints the service date or period the bill line itself states (positive evidence only, see row 2). When it is not certain, the letter does not guess: it prints a fillable blank beside the statement date (D-071 addendum: "date of service [__________] (statement dated June 15, 2026)") and Step 3 shows a confirm note asking the paralegal to read the date from the quote. Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. Charge dates: `tests/unit/test_t202_r3_allow_list.py` (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and `evals/letter_check.charge_date_violations`, which accepts the blank and nothing else for a line with no certain date. |
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:15.482Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/service_date.py > /dev/null 2>&1 && echo EXISTS_AT_HEAD || echo MISSING_AT_HEAD; git ls-tree -r --name-only HEAD app/backend | head -80; echo \"---\"; git show HEAD:app/backend/service_date.py 2>&1 | wc -l; git show HEAD:app/backend/export.py 2>&1 | wc -l",
 "description": "Confirm service_date.py and export.py exist at HEAD and their sizes"
}
````

### User / tool · 2026-11-03T01:27:15.640Z

**tool result**
````
EXISTS_AT_HEAD
app/backend/__init__.py
app/backend/amounts.py
app/backend/api.py
app/backend/billing.py
app/backend/calibration_route.py
app/backend/case_extras.py
app/backend/case_list.py
app/backend/charge_text.py
app/backend/confidence.py
app/backend/conflict_candidates.py
app/backend/conflicts.py
app/backend/count_charge.py
app/backend/credibility.py
app/backend/date_convention.py
app/backend/dates.py
app/backend/dismissal_patterns.py
app/backend/export.py
app/backend/export_routes.py
app/backend/flag_templates.py
app/backend/flags.py
app/backend/gaps.py
app/backend/generator.py
app/backend/grounding.py
app/backend/ingest.py
app/backend/injection.py
app/backend/judge_guard.py
app/backend/judges.py
app/backend/language.py
app/backend/lexicon.py
app/backend/lexicon_scan.py
app/backend/limits.py
app/backend/money.py
app/backend/narrative.py
app/backend/overlap.py
app/backend/pdf_checks.py
app/backend/pdf_hidden.py
app/backend/pdf_ocr.py
app/backend/pdf_routes.py
app/backend/pdf_text.py
app/backend/pipeline.py
app/backend/present.py
app/backend/reclassify.py
app/backend/rejudge.py
app/backend/review.py
app/backend/schemas.py
app/backend/sentences.py
app/backend/service_date.py
app/backend/spanish.py
app/backend/spanish_text.py
app/backend/speaker.py
app/backend/split_llm.py
app/backend/store.py
app/backend/summary_trim.py
app/backend/totals.py
app/backend/trace.py
app/backend/uncovered.py
app/backend/why.py
---
     377
     939
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:16.707Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/service_date.py",
 "allow_large": true
}
````

### User / tool · 2026-11-03T01:27:16.720Z

**tool result**
````
1	"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 round 3: an ALLOW-LIST, not a deny-list). Code only, no LLM
2	(LLM_VS_CODE rows 2 and 3).
3	
4	The letter's charge line carries a date of service. A date there is a claim to an adjuster, so a date is the line's service date ONLY when one of these ties it to the line:
5	  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
6	  (b) a service label in the same clause before (or just after) it (DOS, date of service, service date, seen on, visit date, visit of, the run of ...);
7	  (c) it is the date cell of the charge row itself, in a table whose header is (a);
8	  (d) for a coded line of a bill with no date of its own: the one period the bill states for its services ('dates of service ...', 'the run of ...', and on a UB-04 'statement
9	      covers period ...').
10	Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all) is NOT a service date and is never
11	looked at again: an unlabeled date cannot become the line's date by default. The result is one of:
12	  - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
13	    EVERY labeled end then reads one way; a stated date after its statement, or more than five years before it, in a bill is doubtful);
14	  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service; a dated encounter note (visit note, imaging report: not a bill) keeps the
15	    note's own date;
16	  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
17	    the code cannot read it with certainty; the note names the date as the quote writes it.
18	  Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
19	  and the letter never says "service date not stated" above a quote that states one.
20	Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
21	(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
22	import datetime as _dt
23	import re
24	
25	from app.backend import amounts as AM
26	
27	_MON = AM._MON
28	_ORD = r"(?:st|nd|rd|th)?"
29	_DASH = "–—"
30	_TOK = re.compile(
31	    r"(?<![\w/$])(?:"
32	    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
33	    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
34	    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
35	    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
36	    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
37	    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
38	    r")(?![\w/]|\.\d)", re.IGNORECASE)
39	_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
40	_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
41	# ---- the allow-list: positive evidence that a date is the line's date of service. Nothing else is read (T-202 round 3).
42	_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(]{0,4}$"
43	_SVC_CORE = (r"\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bvisit\s+dates?|\bdates?\s+of\s+visit|\bvisit\s+of|\bseen(?:\s+on)?|"
44	             r"\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
45	             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")
46	_PER_CORE = (r"\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bservice\s+period|\bperiod\s+of\s+service|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|"
47	             r"\b(?:services?\s+)?(?:rendered|provided)\s+on")
48	_UB_CORE = r"\bstatement\s+(?:covers\s+)?period"          # UB-04 FL6 'Statement Covers Period' is the span of the services; on any other bill 'statement period' is not a service label
49	_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
50	_LBL = {False: re.compile(rf"(?:{_SVC_CORE}){_LBL_END}", re.IGNORECASE), True: re.compile(rf"(?:{_SVC_CORE}|{_UB_CORE}){_LBL_END}", re.IGNORECASE)}
51	_PER = {False: re.compile(rf"(?:{_PER_CORE}){_LBL_END}", re.IGNORECASE), True: re.compile(rf"(?:{_PER_CORE}|{_UB_CORE}){_LBL_END}", re.IGNORECASE)}
52	# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
53	_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
54	                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
55	_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful
56	
57	REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
58	WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
59	
60	
61	def display(first, last=None) -> str:
62	    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
63	    def lng(iso):
64	        d = _dt.date.fromisoformat(iso)
65	        return f"{d.strftime('%B')} {d.day}, {d.year}"
66	    if not last or last == first:
67	        return lng(first)
68	    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
69	    if (a.year, a.month) == (b.year, b.month):
70	        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
71	    if a.year == b.year:
72	        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
73	    return f"{lng(first)}–{lng(last)}"
74	
75	
76	BLANK = "date of service [__________]"
77	
78	
79	def not_stated_text(statement_iso) -> str:
80	    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
81	    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
82	    if statement_iso:
83	        return f"{BLANK} (statement dated {display(statement_iso)})"
84	    return BLANK
85	
86	
87	def printed_text(res: dict, statement_iso) -> str:
88	    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
89	    return not_stated_text(statement_iso)
90	
91	
92	_WHY = {
93	    "ambiguous_numeric": "The quote labels {raw} as the date of service, and it can be read as month/day or day/month; the record does not settle which.",
94	    "two_digit_year": "The quote labels {raw} as the date of service, but it has a two-digit year, which the code does not guess.",
95	    "no_year": "The quote labels {raw} as the date of service, but it states no year, which the code does not borrow from the statement.",
96	    "invalid": "The quote labels {raw} as the date of service, but it is not a complete date on the calendar.",
97	    "several_dates": "The quote labels more than one date of service ({raw}) and nothing says which one belongs to this charge.",
98	    "implausible": "The quote labels {raw} as the date of service, but that date is after the statement it appears on or years before it.",
99	    "non_service_date": "The only date near this line ({raw}) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service).",
100	    "no_date": "The line states no date of service.",
101	}
102	_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
103	_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it."
104	
105	
106	def confirm_note(reason, raw) -> str:
107	    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
108	    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)
109	
110	
111	def _iso(y, mo, d):
112	    try:
113	        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
114	    except ValueError:
115	        return None
116	
117	
118	class _Tok:
119	    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")
120	
121	    def __init__(self, m):
122	        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
123	        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
124	        getattr(self, "_" + self.kind)(m.group(0))
125	        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
126	            self.flaw = "invalid"
127	
128	    def _iso(self, s):
129	        y, mo, d = (int(x) for x in s.split("-"))
130	        self.fixed = _iso(y, mo, d)
131	
132	    def _num(self, s):
133	        a, b, y = re.split(r"[/.-]", s)
134	        if len(y) == 2:
135	            self.flaw = "two_digit_year"
136	            return
137	        a, b, y = int(a), int(b), int(y)
138	        md, dm = _iso(y, a, b), _iso(y, b, a)
139	        if md and dm and md != dm:
140	            self.ambiguous = {"MD": md, "DM": dm}
141	        elif md or dm:
142	            self.fixed = md or dm
143	            self.order = None if (md and dm) else ("MD" if md else "DM")
144	
145	    def _mdy(self, s):
146	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
147	        if m.group(4):
148	            self.flaw = "two_digit_year"
149	            return
150	        if not m.group(3):
151	            self.flaw = "no_year"
152	            return
153	        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))
154	
155	    def _dmy(self, s):
156	        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
157	        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))
158	
159	    def _md(self, s):
160	        self.flaw = "no_year"
161	
162	    def _mper(self, s):
163	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
164	        if not m.group(5):
165	            self.flaw = "no_year"
166	            return
167	        y, m1 = int(m.group(5)), _mon(m.group(1))
168	        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
169	        if a and b and b > a:
170	            self.first, self.last = a, b
171	        else:
172	            self.flaw = "invalid"
173	
174	
175	def _mon(name):
176	    from app.backend import dates
177	    return dates.MONTHS[name.lower()[:3]]
178	
179	
180	class _Unit:
181	    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
182	    def __init__(self, toks):
183	        self.toks = toks
184	        self.start, self.end = toks[0].start, toks[-1].end
185	
186	    def raw(self, text):
187	        return text[self.start:self.end]
188	
189	
190	def _units(text: str) -> list:
191	    toks = [_Tok(m) for m in _TOK.finditer(text)]
192	    out, k = [], 0
193	    while k < len(toks):
194	        t = toks[k]
195	        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
196	            out.append(_Unit([t, toks[k + 1]]))
197	            k += 2
198	        else:
199	            out.append(_Unit([t]))
200	            k += 1
201	    return out
202	
203	
204	def _certain(unit: _Unit, ref):
205	    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
206	    for t in unit.toks:
207	        if t.flaw:
208	            return "bad", t.flaw
209	    if len(unit.toks) == 1 and unit.toks[0].first:
210	        return "ok", unit.toks[0].first, unit.toks[0].last
211	    determined = {t.order for t in unit.toks if t.order}
212	    amb = [t for t in unit.toks if t.ambiguous]
213	    if len(determined) > 1:
214	        return "bad", "ambiguous_numeric"
215	    if determined:
216	        order = next(iter(determined))
217	    elif amb:
218	        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
219	        if len(feasible) != 1:
220	            return "bad", "ambiguous_numeric"
221	        order = feasible[0]
222	    else:
223	        order = None
224	    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
225	    if len(isos) == 2 and isos[1] <= isos[0]:
226	        return "bad", "invalid"
227	    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)
228	
229	
230	def _header_cells(excerpt: str, row_ls: int):
231	    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line."""
232	    for line in reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]):
233	        if not line.strip():
234	            return None
235	        if re.search(r"\d", line) and not _H_SVC.search(line):
236	            continue
237	        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
238	        return cells if len(cells) >= 2 else None
239	    return None
240	
241	
242	def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
243	    heads = _header_cells(excerpt, row_ls)
244	    if not heads:
245	        return ""
246	    col = tok_abs - row_ls
247	    if len(heads) == len(row_cells):
248	        idx = next((i for i, (a, b) in enumerate(row_cells) if a <= col < b), None)
249	        if idx is not None:
250	            return heads[idx][1]
251	    return min(heads, key=lambda h: abs(h[0] - col))[1]
252	
253	
254	def _mark(text: str, units: list, rx, tail: bool = False) -> list:
255	    """[bool] per unit: a service label ends the 40 characters before it, or it is listed ('A and B') after a labeled unit. In `tail` (words after the figure) the label must open the
256	    tail: no sentence break and no 'and'/'or' between the figure and the label."""
257	    marks = []
258	    for k, u in enumerate(units):
259	        ok = bool(rx.search(text[max(0, u.start - 40):u.start]))
260	        if ok and tail:
261	            before = text[:u.start]
262	            ok = len(before) <= 40 and not re.search(r"[.;]|\b(?:and|or)\b", before, re.IGNORECASE)
263	        if not ok and k and marks[k - 1] and _LIST.match(text[units[k - 1].end:u.start]):
264	            ok = True
265	        marks.append(ok)
266	    return marks
267	
268	
269	def _plausible(first, last, ref) -> bool:
270	    """A bill's service date is not after its statement and not years before it."""
271	    if not ref:
272	        return True
273	    r = _dt.date.fromisoformat(ref)
274	    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)
275	
276	
277	def _decide(units, text, ref, bill):
278	    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
279	    reads = [(u, _certain(u, ref)) for u in units]
280	    raws = [" ".join(u.raw(text).split()) for u in units]
281	    if len(units) > 1:
282	        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
283	        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
284	            return "bad", "several_dates", raws
285	        first, last = next(iter(same))
286	    else:
287	        r = reads[0][1]
288	        if r[0] != "ok":
289	            return "bad", r[1], raws
290	        first, last = r[1], r[2]
291	    if bill and not _plausible(first, last, ref):
292	        return "bad", "implausible", raws
293	    return "ok", first, last
294	
295	
296	def _apply(out: dict, res) -> dict:
297	    if res[0] == "ok":
298	        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
299	    else:
300	        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
301	    return out
302	
303	
304	def resolve(excerpt: str, start: int, source, date_iso) -> dict:
305	    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the labeled date text the reason is about, or the one
306	    unlabeled date near the line for non_service_date), raws ([the labeled dates as written])} for the figure at `start` of `excerpt`, in a record with header `source` and date
307	    `date_iso`. Only labeled dates are candidates (module doc); see it for the rules."""
308	    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
309	    amts = AM.find_amounts(excerpt or "")
310	    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
311	    if i is None:
312	        return out
313	    a = amts[i]
314	    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
315	    bill = AM.billing_document(source, excerpt)
316	    ub = bool(_UB.search(source or "") or _UB.search(excerpt or ""))
317	    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
318	    seg = excerpt[ss:se]
319	    others = []                       # dates near the line that no service label ties to it
320	
321	    def labeled(text, tail=False):
322	        us = _units(text)
323	        marks = _mark(text, us, _LBL[ub], tail)
324	        others.extend(u.raw(text) for u, m in zip(us, marks) if not m)
325	        return [u for u, m in zip(us, marks) if m]
326	
327	    if len(AM._cells(seg)) >= 2:                                          # (a)/(c) a table row: only a date under a heading that names service
328	        row_ls = excerpt.rfind("\n", 0, a["start"]) + 1
329	        rl_end = excerpt.find("\n", a["start"])
330	        row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
331	        row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
332	        lab = []
333	        for u in _units(seg):
334	            head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
335	            if (head and _H_SVC.search(head)) or _LBL[ub].search(seg[max(0, u.start - 40):u.start]):
336	                lab.append(u)
337	            else:
338	                others.append(u.raw(seg))
339	        if lab:
340	            return _apply(out, _decide(lab, seg, date_iso, bill))
341	    else:                                                                 # (b) a service label in the same clause
342	        prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
343	        own = excerpt[prev:a["start"]]
344	        lab = labeled(own)
345	        if lab:
346	            return _apply(out, _decide(lab, own, date_iso, bill))
347	        if prev > ss:                                                      # a labeled date stands once for the items listed after it: usable only when it is the line's one date
348	            whole = excerpt[ss:a["start"]]
349	            lab = labeled(whole)
350	            if lab:
351	                return _apply(out, _decide(lab, whole, date_iso, bill))
352	        tail = excerpt[a["end"]:min([amts[j]["start"] for j in sfigs if j > i], default=se)]
353	        lab = labeled(tail, tail=True)
354	        if lab:
355	            return _apply(out, _decide(lab, tail, date_iso, bill))
356	    # no labeled date of its own
357	    if bill:
358	        if AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # (d) a coded line takes the one period the bill states for its services
359	            prefix = excerpt[:se]
360	            us = _units(prefix)
361	            seen, uniq = set(), []
362	            for u, m in zip(us, _mark(prefix, us, _PER[ub])):
363	                if not m:
364	                    continue
365	                r = _certain(u, date_iso)
366	                key = (r[1], r[2]) if r[0] == "ok" else (u.raw(prefix),)
367	                if key not in seen:
368	                    seen.add(key)
369	                    uniq.append(u)
370	            if uniq:
371	                return _apply(out, _decide(uniq, prefix, date_iso, bill))
372	        if others:
373	            out.update(reason="non_service_date", raw=others[0])
374	        return out
375	    if date_iso:                                                          # a dated encounter record (visit note, imaging report): the record's date is the visit
376	        out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
377	    return out
378	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:27:56.588Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && sed -n '1,40p' feedback_reviewer_scratch_writes.md; echo ====; sed -n '1,30p' feedback_review_write_once.md; echo ====; sed -n '1,30p' feedback_evidence_sha_vs_commit.md",
 "description": "Read my relevant write-location and evidence memory notes"
}
````

### User / tool · 2026-11-03T01:27:56.695Z

**tool result**
````
---
name: reviewer-scratch-writes
description: Reviewer Write tool is blocked outside reviews/ and artifacts/review-evidence/ (scratchpad refused); keep helper scripts and sweep outputs there; shell lines with backticks or triple backticks trip the board guard
metadata:
  type: feedback
---

Write tool calls to the session scratchpad were refused by reviewer-write-guard. Shell `cp` and `cat >` into the scratchpad still worked. Keep reviewer helper scripts and copied evidence in artifacts/review-evidence/<card>-rN/ so the Write tool is allowed.

**Why:** the write guard allows only reviews/, artifacts/review-evidence/ and the agent memory dir. The scratchpad is outside that list for Write, and the error came back on the first Write.

**How to apply:** put sweep scripts, mutants and copied outputs under artifacts/review-evidence/. Do not put backticks or triple backticks inside a shell command line; the git-guard board-guard denies unparseable commands. Write a small .py file instead and run it with python -I.

**T-169 r2 addendum:** `git clone` plus `git checkout --detach <sha>` was denied by board-guard when the clone sat under artifacts/review-evidence/ ("reviewers may not run git checkout in the project"). The same two commands worked in a clone under the session scratchpad (/private/tmp/...), so put pinned clones in the scratchpad and evidence in artifacts/review-evidence/. A python -c line containing backtick-escaped fences was also denied; use a .py file.

Related: [[project_t167_plain_wording_patterns]], [[feedback_bind_to_named_reference]].
====
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**The ```json block belongs to the first Write.** T-084 r2 (this session): I wrote `reviews/T-084-staff-engineer-r2.md` without its json fence. The board-validate PostToolUse hook rejected it ("review must contain a ```json block"), and reviewer-write-guard refused the Edit that would have added it. The fix was a complete `-r3` file that says it supersedes the r2 file. **How to apply:** before the Write, count the fences (exactly one ```json block) and parse the block with `json.loads`; check the verdict against the rule.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.

**T-141 r5 addendum:** the first Write carried one control claim I had not yet run ("V10 and W10 print info on 93a2ffc"). It was true, but the guard then refused an Edit to fix a muddled sentence about it. Run every "X prints Y on the control archive" claim before the first Write, and proof-read the evidence sentence, not only the JSON. Accurate-but-clumsy wording can stay, but it cannot be corrected in place. See [[project_t141_r5_patterns]].

**T-173 r2 addendum:** the first Write had one clumsy sentence and one citation range one line too wide (conftest.py:208-211 for a guard at 208-210). Both stayed, because Edit was refused on the new file, and I did not work around the guard. Proof-read the body the same way as the JSON block before the Write, and read each cited range with `git show <sha>:<path> | sed -n` first. A shell line with a backtick inside a `python -c` string was denied by git-guard ("could not parse command safely"); put any fence or regex with backticks in a script file.

**T-045 r3 addendum:** three function line ranges in the exercised list were written from memory of grep output (ship_bar 913-960 should be 913-955; render_md 1058-1092 should be 1093; check_fresh 1294-1313 should be 1315). The findings' own citations were grepped and correct. I did not work around the guard; the slip stays in the record. Run `grep -n "^def "` and `sed -n` on each range before the first Write, and list each range as you verified it. See [[project_t045_r3_record_latest_patterns]].

**T-155 r2 / T-164 addendum:** two wrong body facts went out in first Writes: a file name (test_multicase.py for test_rerun_note.py) and "the card names X" when the card does not. Both were caught only after the Write. Before the first Write, grep each file name and each "the card says" phrase against `board.py show` output. The corrected records are `-r2b` and `-r1` files, and each names the file it corrects. See [[project_t155_r2_t164_patterns]].

**T-208 r1 addendum:** the r1 body said a requested mutant "passes for the eval" while its own exercised list said value 18, exit 1; the line count said 74 where the diff has 71 added lines (74 counted three `+++` headers). Edit was refused, so r2 is a complete superseding file that names the two sentences it corrects. Before the first Write, check each count against `git show <sha> --numstat` and each "passes/fails" sentence against the exercised list. See [[project_t208_letter_ai_wording_patterns]].
====
---
name: feedback_evidence_sha_vs_commit
description: a card's green run and its "stale test" triage can cite an older sha; run the cited test at that sha and at the reviewed commit before accepting either, and count the commits between them
metadata:
  type: feedback
---

Before accepting "full suite green at clean HEAD" or "this red is a stale test", check which sha the evidence ran on. Run `git rev-list --count <evidence-sha>..<commit>` and run the disputed test file at both shas. If the file at the evidence sha fails the same way the card says it is stale, the triage is backwards.

**Why:** T-155 r1 (20b3a42): the AC evidence was a run at 078c5ae, 12 commits behind. At 078c5ae the density budgets really failed (179 > 150); a later frontend fix (f262223) cured them. The card called them stale and loosened the budget with a false comment. A first-screen red at the reviewed commit was not on the card.

**How to apply:** in any e2e review, record the evidence sha and the reviewed sha on the first line of the exercised list. Use an archive per sha (git archive | tar -x into a unique scratch dir, own port, E2E_REQUIRE_DB=1). If HEAD moves during the review, say so and state which sha the findings are for.

Related: [[project_t155_e2e_triage_patterns]], [[project_round2_snapshot_review_patterns]].

**T-158 data point (r1, 2026-11-02):** HEAD moved four times during one review (83f1afd, a7302fe, f31b146, 9db2cec). The card's green came from 2de5ba9 (another card), not from its own commit 0b2ce9c. See [[project_t158_settle_patterns]].

**T-175 r2 data point (2026-11-02):** HEAD moved 30c04e6 -> da0c7fe mid-review, and the frontend half of the card landed in the second commit. My render on the first archive showed the old UI; the same render on the new archive showed the fix. Re-archive at the moved HEAD, then decide. See [[project_t175_r2_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:05.587Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/head-fc37fbc\" && git archive fc37fbc | tar -x -C \"$S/head-fc37fbc\" && echo \"archived\" && ls \"$S/head-fc37fbc/app/backend/service_date.py\" && git rev-parse fc37fbc && git rev-list --count 901ad5a..fc37fbc && git diff --stat 901ad5a fc37fbc -- app tests evals memory | tail -1; echo \"--- imports in service_date.py ---\"; grep -n \"^import\\|^from\\|llm\\|LLM\\|generator\\|judge\" \"$S/head-fc37fbc/app/backend/service_date.py\" | head; echo \"--- amounts imports ---\"; grep -n \"^import\\|^from\" \"$S/head-fc37fbc/app/backend/amounts.py\"",
 "description": "Archive HEAD into scratchpad and check LLM imports in service_date path"
}
````

### User / tool · 2026-11-03T01:28:07.203Z

**tool result**
````
archived
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc/app/backend/service_date.py
fc37fbcec0ebdb7705e4d91c2ad43afd67a82568
5
 22 files changed, 410 insertions(+), 149 deletions(-)
--- imports in service_date.py ---
1:"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 round 3: an ALLOW-LIST, not a deny-list). Code only, no LLM
2:(LLM_VS_CODE rows 2 and 3).
22:import datetime as _dt
23:import re
25:from app.backend import amounts as AM
--- amounts imports ---
4:import re
6:from app.backend import dates as _dates, injection, lexicon
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:11.120Z

**tool call — Bash**
````
{
 "command": "S=$(echo \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"); H=\"$S/head-fc37fbc\"; echo \"$H\" > \"$S/.headpath\"; cd \"$H\" && grep -rn \"charge_service_date\\|charge_when\\|service_date\\.\\|not_stated_text\\|printed_text\\|confirm_note\" app/ --include=*.py --include=*.js | cut -c1-260",
 "description": "Find all call sites of the service-date functions at HEAD"
}
````

### User / tool · 2026-11-03T01:28:11.176Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to $(echo/.headpath)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:14.047Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -rn \"charge_service_date\\|charge_when\\|service_date\\.\\|not_stated_text\\|printed_text\\|confirm_note\" app/ evals/ --include=*.py --include=*.js | cut -c1-260",
 "description": "Find all call sites of the service-date functions at HEAD"
}
````

### User / tool · 2026-11-03T01:28:14.163Z

**tool result**
````
app/backend/store.py:118:def charge_service_date(item: dict, rec, pos) -> dict:
app/backend/store.py:121:    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
app/backend/store.py:122:    A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
app/backend/store.py:140:        note = SD.confirm_note(r["reason"], r["raw"])
app/backend/store.py:142:            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd),
app/backend/store.py:143:            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}
app/backend/store.py:146:def charge_service_dates(item: dict, rec, pos) -> tuple:
app/backend/store.py:147:    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
app/backend/store.py:148:    d = charge_service_date(item, rec, pos)
app/backend/store.py:196:            sd = charge_service_date(a, r, d["pos"])
app/backend/store.py:197:            d["dos_iso"], d["dos_end_iso"], d["dos_text"], d["dos_note"] = sd["date_iso"], sd["end_iso"], sd["text"], sd["confirm_note"]
app/frontend/guided/step3.js:18:  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the statement date whenever it is not that day. Code only, no guessing. */
app/frontend/guided/step3.js:34:  const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
app/frontend/guided/step3.js:59:        else if (!(sd && sd.confirm_note)) foot.push("If you count it, it's added to the bill total in the letter, with the highlighted words as its source.");
app/frontend/guided/step3.js:63:        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), confirmNext(), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain
app/backend/export.py:74:    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026' (D-071). One implementation, shared with the case view (service_date.display)."""
app/backend/export.py:75:    return service_date.display(first, last)
app/backend/export.py:215:    def charge_when(self, a):
app/backend/export.py:217:        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
app/backend/export.py:226:        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
app/backend/export.py:358:            out += [f"{v.charge_when(a)}: {_money(a['cents'])}",
app/backend/service_date.py:21:(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
app/backend/service_date.py:79:def not_stated_text(statement_iso) -> str:
app/backend/service_date.py:87:def printed_text(res: dict, statement_iso) -> str:
app/backend/service_date.py:89:    return not_stated_text(statement_iso)
app/backend/service_date.py:106:def confirm_note(reason, raw) -> str:
evals/letter_check.py:20:has its own scanner and shares no code with the production parser (app/backend/service_date.py), so a parser bug cannot hide itself.
evals/letter_check.py:222:# the production parser (app/backend/service_date.py): its own small scanner, its own string rules, enumerating every reading a written date allows.
app/backend/present.py:152:            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for this charge's date
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:16.687Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && sed -n '115,150p' app/backend/store.py; echo \"=== export charge_when ===\"; sed -n '212,230p' app/backend/export.py; echo \"=== store 190-200 ===\"; sed -n '190,200p' app/backend/store.py",
 "description": "Read store.charge_service_date and export.charge_when at HEAD"
}
````

### User / tool · 2026-11-03T01:28:16.802Z

**tool result**
````
    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None


def charge_service_date(item: dict, rec, pos) -> dict:
    """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 2026)'
    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
    A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
    the one period its bill states; an unlabeled date (birth, injury, referral, entry, transaction ...) is never the service date. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
    not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    bill = AM.billing_document((rec or {}).get("source"), item.get("excerpt") or "")
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    if counted_undated:
        r = dict(none)
    elif rec is None or pos is None or not item.get("excerpt"):
        r = dict(none) if bill else ({"state": "stated", "first": rd, "last": None, "reason": None, "raw": "", "raws": []} if rd else dict(none))
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

=== export charge_when ===
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

=== store 190-200 ===
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
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:41.116Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && ls tests/unit | grep -i \"t202\\|service\\|letter\\|charge\" ; echo ---; grep -n \"def charge_date_violations\" -A3 evals/letter_check.py | cut -c1-200; echo ---; grep -n -i \"mutant\" tests/unit/test_t202_r3_allow_list.py | head -40 | cut -c1-220; echo; wc -l tests/unit/test_t202_r3_allow_list.py",
 "description": "Locate the T-202 r3 unit test and letter_check charge scanner at HEAD"
}
````

### User / tool · 2026-11-03T01:28:41.283Z

**tool result**
````
test_t121_letter_styles.py
test_t139_charge_text.py
test_t139_letter_eval.py
test_t171_count_charge.py
test_t200_undated_charge_label.py
test_t202_charge_service_dates.py
test_t202_r2_service_date_layouts.py
test_t202_r3_allow_list.py
---
379:def charge_date_violations(letter: str, records) -> list:
380-    """D-071 amendment, round 3 (allow-list): every charge line's printed date against THAT line's own quote (plus, for a quote with no labeled date, the bill's period before it).
381-    `records`: the case's [{n, source, date_iso, excerpt}]. Per line, the quote's LABELED dates are those with a service phrase right before them or a table heading over them that
382-    names the service; every other date in it (birth, injury, onset, referral, order, entry, transaction, posted, statement, unlabeled) is not a service date.
---
246:    """Mutant: `all(...)` -> `any(...)` in service_date._certain. Under `any` this period (DM reading: one end fits, one does not) is called ambiguous and prints the blank."""

     379 tests/unit/test_t202_r3_allow_list.py
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:43.482Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && sed -n '1,60p' tests/unit/test_t202_r3_allow_list.py | cut -c1-260",
 "description": "Read the first part of the T-202 r3 allow-list test"
}
````

### User / tool · 2026-11-03T01:28:43.583Z

**tool result**
````
"""T-202 round 3 (D-071 amendment, allow-list): a date is the service date only when positive evidence ties it to the charge line:
  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A);
  (b) a service label in the same clause (DOS, date of service, service date, seen on, visit date ...);
  (c) the date cell of the charge row itself, in a table whose header is (a).
Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, or unlabeled) is NOT certain, so the not-stated form prints.
Every line with no certain date prints the D-071 addendum blank, 'date of service [__________] (statement dated X)', for a quote that labels none AND for a labeled date the code cannot read;
the letter never says 'service date not stated'.
Every probe from the round 2 paralegal and staff reviews (B3, B7-B12, N5, N11, N12, N14, N16, N17, P10, the Entry/Transaction/Issued/Printed headings, the DOI/DOB/authorization
sentences, the 1998 and 2031 dates, 'Mar 5, 26', the all-vs-any period rule) is a fixture here. Each runs the shipped path (store.charge_service_dates -> export.build_export). Code only."""
import re

import pytest

from app.backend import amounts as AM, export, service_date as SD, store
from evals import letter_check as LC

LEDGER = "Brindlewood Physical Therapy, itemized ledger"
UB = "Saltmarrow General Hospital, UB-04 itemized bill"
CMS = "Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)"
NOTE = "Dr. Alvarez, primary care, progress note"
BLANK = "date of service [__________]"
NS = BLANK


def _money(cents):
    return f"${cents // 100:,}.{cents % 100:02d}"


def head(excerpt, fig, source=LEDGER, rec_date="2026-06-30"):
    """The charge header line the letter prints for `fig` (every figure of the excerpt is an accepted charge)."""
    rec = {"source": source, "date_iso": rec_date}
    amounts = []
    for i, a in enumerate(AM.find_amounts(excerpt)):
        d = store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, rec, a["start"])
        amounts.append(dict(id=f"a{i}", record_no=1, cents=a["cents"], cls="charge", raw=a["raw"], excerpt=excerpt, review_status="accepted", pos=a["start"],
                            dos_iso=d["date_iso"], dos_end_iso=d["end_iso"], dos_text=d["text"], dos_note=d["confirm_note"]))          # the same keys store.export_case sets
    case = {"records": [{"n": 1, "source": source, "date_iso": rec_date, "excerpt": excerpt}], "entries": [], "flags": [], "pending_count": 0, "events": [], "amounts": amounts}
    want = AM.to_cents(fig.lstrip("$"))
    cands = [l for l in export.build_export(case, None, check_letter=False)["letter_text"].split("\n") if re.search(r": \$[\d,]+\.\d\d$", l) and not l.startswith("Billed charges")]
    return next(l for l in cands if l.endswith(": " + _money(want)))


def sd_of(excerpt, fig, source=LEDGER, rec_date="2026-06-30"):
    """store.charge_service_date for the figure (what the case view and the letter share)."""
    a = next(x for x in AM.find_amounts(excerpt) if x["cents"] == AM.to_cents(fig.lstrip("$")))
    return store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, {"source": source, "date_iso": rec_date}, a["start"])


def stated(label, source=LEDGER):
    return f"{source}, {label}: "


def blank_hd(rec_long, source=LEDGER):
    return f"{source}, {BLANK} (statement dated {rec_long})"


def not_stated(rec_long, source=LEDGER):
    return blank_hd(rec_long, source) + ": "
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:47.438Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && ls -d /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import sys; print(sys.version)\"; grep -n \"^def test_\\|parametrize\\|MUT\" tests/unit/test_t202_r3_allow_list.py | cut -c1-200 | head -80",
 "description": "Confirm venv python and list test functions in the allow-list test"
}
````

### User / tool · 2026-11-03T01:28:47.561Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.venv/bin/python
3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
67:@pytest.mark.parametrize("label,ex,fig,src", [
87:def test_a_date_that_no_service_label_ties_to_the_line_prints_the_not_stated_form(label, ex, fig, src):
93:@pytest.mark.parametrize("ex,fig,want", [
98:def test_in_a_visit_note_a_non_service_date_leaves_the_notes_own_date(ex, fig, want):
102:@pytest.mark.parametrize("ex,fig,want", [
117:def test_a_service_label_in_the_same_clause_prints_the_date(ex, fig, want):
121:def test_two_charges_in_one_sentence_each_take_their_own_labeled_date():
128:@pytest.mark.parametrize("heading", ["Entry date", "Transaction Date", "Txn Date", "Recorded", "Filed", "Claim Date", "Sent", "Issued", "Printed", "Reported", "Remit Date",
130:def test_a_single_date_under_a_heading_that_does_not_name_service_is_not_certain(heading):
137:@pytest.mark.parametrize("heading", ["DOS", "Service Date", "Date of Service", "Visit Date", "Date(s) of Service", "From Service", "Service From", "24A", "Svc Date"])
138:def test_a_single_date_under_a_service_heading_prints(heading):
143:def test_trans_date_column_n5_is_not_certain():
149:def test_a_bill_period_phrase_is_read_when_it_is_from_x_to_y_p10_and_n17():
156:def test_a_statement_date_phrase_is_never_a_period():
163:def test_a_label_after_an_and_belongs_to_the_next_item_not_the_figure_before_it():
169:def test_statement_period_is_a_service_period_only_on_a_ub04():
174:def test_a_coded_line_does_not_borrow_another_lines_dos_label():
193:@pytest.mark.parametrize("label,ex,fig,raw,rd,reason", AS_WRITTEN)
194:def test_a_labeled_date_the_code_cannot_read_prints_the_blank_and_the_note_names_the_date(label, ex, fig, raw, rd, reason):
205:def test_two_labeled_dates_print_the_blank_and_the_note_names_both():
216:def test_no_labeled_date_in_the_quote_prints_the_blank_and_a_request_note():
224:def test_the_confirm_note_never_promises_a_confirmation_that_cannot_reach_the_letter():
231:@pytest.mark.parametrize("period,rd,label", [
236:def test_a_period_reads_one_way_only_when_every_end_fits_one_reading(period, rd, label):
245:def test_the_all_in_the_reference_rule_is_pinned_by_a_period_with_one_end_after_the_statement():
279:@pytest.mark.parametrize("label,ex,src,rd,quote,hd,fig", WRONG, ids=[w[0] for w in WRONG])
280:def test_letter_check_fails_a_non_service_date_printed_as_the_date_of_service(label, ex, src, rd, quote, hd, fig):
285:def test_letter_check_fails_not_stated_above_a_quote_that_states_a_certain_service_date():
292:def test_letter_check_passes_only_the_blank_above_a_labeled_date_the_code_could_not_read():
303:def test_letter_check_fails_a_date_above_a_quote_with_no_labeled_date_and_passes_the_blank():
310:def test_letter_check_fails_the_blank_on_a_visit_note_and_a_statement_date_that_is_not_the_records():
316:def test_letter_check_passes_the_right_forms():
330:def test_the_internal_notes_list_each_charge_printed_without_a_certain_service_date():
376:@pytest.mark.parametrize("lab,ex,quote,fig,src,rd", _probe_cases(), ids=[c[0] for c in _probe_cases()])
377:def test_the_independent_check_passes_the_letter_production_prints_for_every_probe_layout(lab, ex, quote, fig, src, rd):
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:51.214Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && PYTHONDONTWRITEBYTECODE=1 timeout 280000 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py -q -p no:cacheprovider 2>&1 | tail -25",
 "description": "Run the T-202 date unit tests against the HEAD archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:28:51.344Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:28:54.339Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py -q -p no:cacheprovider 2>&1 | tail -25",
 "description": "Run the T-202 date unit tests against the HEAD archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:29:02.439Z

**tool result**
````
........................................................................ [ 34%]
........................................................................ [ 68%]
...................................................................      [100%]
211 passed in 7.74s
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:29:29.836Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -n \"NO_DATE_WHY\" app/backend/*.py | cut -c1-240; echo ---; grep -n \"D-064\" /Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md | cut -c1-600; echo ---; grep -n \"def amount_pos\" -A8 app/backend/store.py | cut -c1-220; echo ---; sed -n '216,230p' tests/unit/test_t202_r3_allow_list.py | cut -c1-260; echo ---; grep -rn -i \"five years\\|5 years\\|_YEARS_BEFORE\\|1830\\|366\" tests/unit/test_t202*.py | cut -c1-220 | head",
 "description": "Check D-064 rule, the counted-undated note path, amount_pos, and the 5-year boundary tests"
}
````

### User / tool · 2026-11-03T01:29:29.976Z

**tool result**
````
app/backend/amounts.py:312:_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
app/backend/amounts.py:313:NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
app/backend/amounts.py:535:            out["reason"] = _NO_DATE_WHY
app/backend/amounts.py:663:COUNTABLE_WHY = frozenset({_NO_DATE_WHY, _UNKNOWN_WHY})
app/backend/store.py:129:    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
---
72:| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this charge", a named confirm ("I checked this is a separate charge for a service"), recorded in the audit trail; it then sums like any accepted charge. Amends D-059 item on reclassify: (b) is promotable 
---
107:def amount_pos(item: dict, rec):
108-    """Where the amount's own figure sits in its excerpt (T-140 r3: quotes and reasons are taken from the figure's own offset, never from a text search that finds
109-    the first equal figure). None when the stored offsets do not point at the figure's text."""
110-    start, raw = item.get("excerpt_start"), item.get("text") or ""
111-    if rec is None or start is None or not raw:
112-        return None
113-    from app.backend import generator          # lazy: generator imports store
114-    i = start - generator.body_offset(rec)
115-    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None
---
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
---
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:29:45.302Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -rln -i \"implausib\\|five years\\|years before\\|_YEARS_BEFORE\" tests/ evals/ | head; echo ---; grep -rn -i \"implausib\" tests/unit/*.py | cut -c1-230 | head -12; echo ---; grep -n \"set of .*ref\\|def _plausible\" app/backend/service_date.py | head -3; echo; mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1 && echo made",
 "description": "Find tests that pin the implausible-date and five-year rules"
}
````

### User / tool · 2026-11-03T01:29:45.500Z

**tool result**
````
tests/unit/test_t141_r7_two_digit_year.py
tests/unit/test_t202_r3_allow_list.py
evals/letter_check.py
evals/lexicon_heldout.jsonl
---
tests/unit/test_t202_r3_allow_list.py:186:    ("later than the statement", "Itemized ledger. DOS 07/20/2026 office visit charge $220.00.", "$220.00", "07/20/2026", "2026-06-15", "implausible"),
tests/unit/test_t202_r3_allow_list.py:187:    ("1998, years before the statement", "Itemized ledger. DOS 03/13/1998 office visit charge $220.00.", "$220.00", "03/13/1998", "2026-06-30", "implausible"),
tests/unit/test_t202_r3_allow_list.py:188:    ("2031, years after the statement", "Itemized ledger. DOS 03/13/2031 office visit charge $220.00.", "$220.00", "03/13/2031", "2026-06-30", "implausible"),
---
269:def _plausible(first, last, ref) -> bool:

made
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:29:53.888Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/probe_t207.py",
 "content": "\"\"\"T-207 reviewer probe (staff-engineer r1). Read-only: imports the pinned HEAD archive (fc37fbc) passed as argv[1]; writes nothing.\n\nRun: <venv python> -I probe_t207.py <archive root>\nEach line: label | figure | state | first | last | reason | printed text.\n\"\"\"\nimport sys\nimport datetime as dt\n\nROOT = sys.argv[1]\nsys.path.insert(0, ROOT)\n\nfrom app.backend import amounts as AM, service_date as SD, store  # noqa: E402\n\nLEDGER = \"Brindlewood Physical Therapy, itemized ledger\"\nNOTE = \"Dr. Alvarez, primary care, progress note\"\n\n\ndef resolve_line(label, excerpt, source, rd, fig):\n    a = next(x for x in AM.find_amounts(excerpt) if x[\"raw\"] == fig)\n    r = SD.resolve(excerpt, a[\"start\"], source, rd)\n    print(f\"{label} | {fig} | {r['state']} | {r['first']} | {r['last']} | {r['reason']} | raws={r['raws']}\")\n\n\ndef store_line(label, excerpt, source, rd, fig):\n    a = next(x for x in AM.find_amounts(excerpt) if x[\"raw\"] == fig)\n    item = {\"excerpt\": excerpt, \"value_cents\": a[\"cents\"]}\n    d = store.charge_service_date(item, {\"source\": source, \"date_iso\": rd}, a[\"start\"])\n    print(f\"{label} | {fig} | {d['state']} | {d['date_iso']} | {d['end_iso']} | {d['reason']} | text={d['text']!r} | note={d['confirm_note']!r}\")\n\n\nprint(\"## P1 statement rule: both readings on/before statement -> blank (row 2)\")\nresolve_line(\"P1\", \"DOS 04/05/2026 office visit $120.00.\", LEDGER, \"2026-06-30\", \"$120.00\")\nprint(\"## P2 statement rule: reading after statement impossible -> April 5 (row 2)\")\nresolve_line(\"P2\", \"DOS 04/05/2026 office visit $120.00.\", LEDGER, \"2026-04-20\", \"$120.00\")\n\nprint(\"## P3 period, one end unambiguous (DMY) fixes the other end's order inside the same unit; row 2 says resolved ONLY by the statement rule\")\nresolve_line(\"P3\", \"DOS 04/05/2026 - 13/05/2026 therapy $120.00.\", LEDGER, \"2026-06-30\", \"$120.00\")\nstore_line(\"P3-store\", \"DOS 04/05/2026 - 13/05/2026 therapy $120.00.\", LEDGER, \"2026-06-30\", \"$120.00\")\n\nprint(\"## P4 five-year bound: row 2 says 'more than five years before' is not read; code uses 366*5 days\")\nfor iso, mdy in [(\"2021-06-30\", \"06/30/2021\"), (\"2021-06-29\", \"06/29/2021\"), (\"2021-06-26\", \"06/26/2021\"), (\"2021-06-25\", \"06/25/2021\")]:\n    days = (dt.date(2026, 6, 30) - dt.date.fromisoformat(iso)).days\n    print(f\"P4 days_before_statement={days} service={iso} years_before_is_more_than_5={dt.date.fromisoformat(iso) < dt.date(2021, 6, 30)}\")\n    resolve_line(f\"P4 {mdy}\", f\"Itemized ledger. DOS {mdy} office visit $120.00.\", LEDGER, \"2026-06-30\", \"$120.00\")\n\nprint(\"## P5 non-bill visit note: no labeled DOS, the record header date becomes the charge date (row 2 says only the allow-list counts)\")\nresolve_line(\"P5\", \"Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.\", NOTE, \"2026-01-09\", \"$240.00\")\nstore_line(\"P5-store\", \"Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.\", NOTE, \"2026-01-09\", \"$240.00\")\n\nprint(\"## P6 counted-undated charge (D-064 'Count this charge'): row 3 says every not-certain charge gets a Step 3 confirm note\")\nitem = {\"excerpt\": \"Itemized ledger. New patient exam charge $250.00.\", \"value_cents\": 25000, \"ladder\": {\"counted\": {\"not_counted_reason\": AM.NO_DATE_WHY}}}\na = next(x for x in AM.find_amounts(item[\"excerpt\"]) if x[\"raw\"] == \"$250.00\")\nd = store.charge_service_date(item, {\"source\": LEDGER, \"date_iso\": \"2026-06-30\"}, a[\"start\"])\nprint(f\"P6 | $250.00 | {d['state']} | {d['date_iso']} | reason={d['reason']} | text={d['text']!r} | note={d['confirm_note']!r}\")\nitem2 = dict(item, ladder={})\nd2 = store.charge_service_date(item2, {\"source\": LEDGER, \"date_iso\": \"2026-06-30\"}, a[\"start\"])\nprint(f\"P6-uncounted | $250.00 | {d2['state']} | reason={d2['reason']} | text={d2['text']!r} | note={d2['confirm_note']!r}\")\n\nprint(\"## P7 row 3 letter text for a not-certain ambiguous date and for a labeled date that is a visit note (blank form)\")\nstore_line(\"P7\", \"Itemized ledger. DOS 04/05/2026 office visit charge $120.00.\", LEDGER, \"2026-06-30\", \"$120.00\")\nstore_line(\"P7b\", \"Itemized ledger. New patient exam charge $250.00.\", LEDGER, \"2026-06-30\", \"$250.00\")\n"
}
````

### User / tool · 2026-11-03T01:29:54.007Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/probe_t207.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:29:56.946Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd /Users/arsis/zlayt-pm-project && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-207-r1/probe_t207.py \"$H\" 2>&1 | tee artifacts/review-evidence/T-207-r1/probe_t207.out",
 "description": "Run the T-207 probe script against the pinned HEAD archive"
}
````

### User / tool · 2026-11-03T01:29:57.319Z

**tool result**
````
## P1 statement rule: both readings on/before statement -> blank (row 2)
P1 | $120.00 | not_stated | None | None | ambiguous_numeric | raws=['04/05/2026']
## P2 statement rule: reading after statement impossible -> April 5 (row 2)
P2 | $120.00 | stated | 2026-04-05 | None | None | raws=[]
## P3 period, one end unambiguous (DMY) fixes the other end's order inside the same unit; row 2 says resolved ONLY by the statement rule
P3 | $120.00 | stated | 2026-05-04 | 2026-05-13 | None | raws=[]
P3-store | $120.00 | stated | 2026-05-04 | 2026-05-13 | None | text='May 4–13, 2026' | note=None
## P4 five-year bound: row 2 says 'more than five years before' is not read; code uses 366*5 days
P4 days_before_statement=1826 service=2021-06-30 years_before_is_more_than_5=False
P4 06/30/2021 | $120.00 | stated | 2021-06-30 | None | None | raws=[]
P4 days_before_statement=1827 service=2021-06-29 years_before_is_more_than_5=True
P4 06/29/2021 | $120.00 | stated | 2021-06-29 | None | None | raws=[]
P4 days_before_statement=1830 service=2021-06-26 years_before_is_more_than_5=True
P4 06/26/2021 | $120.00 | stated | 2021-06-26 | None | None | raws=[]
P4 days_before_statement=1831 service=2021-06-25 years_before_is_more_than_5=True
P4 06/25/2021 | $120.00 | not_stated | None | None | implausible | raws=['06/25/2021']
## P5 non-bill visit note: no labeled DOS, the record header date becomes the charge date (row 2 says only the allow-list counts)
P5 | $240.00 | stated | 2026-01-09 | None | None | raws=[]
P5-store | $240.00 | stated | 2026-01-09 | None | None | text='January 9, 2026' | note=None
## P6 counted-undated charge (D-064 'Count this charge'): row 3 says every not-certain charge gets a Step 3 confirm note
P6 | $250.00 | not_stated | None | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None
P6-uncounted | $250.00 | not_stated | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note='The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.'
## P7 row 3 letter text for a not-certain ambiguous date and for a labeled date that is a visit note (blank form)
P7 | $120.00 | not_stated | None | None | ambiguous_numeric | text='date of service [__________] (statement dated June 30, 2026)' | note='The quote labels 04/05/2026 as the date of service, and it can be read as month/day or day/month; the record does not settle which. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.'
P7b | $250.00 | not_stated | None | None | no_date | text='date of service [__________] (statement dated June 30, 2026)' | note='The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.'
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:30:16.869Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"date of service\" spec/SPEC.md spec/REQUIREMENTS.md spec/SAMPLE_CASE_TRUTHS.md docs/CONTRACT.md 2>/dev/null | cut -c1-300 | head -20; echo ---; grep -n -i \"D.2\\|blocker\" docs/CONTRACT.md | cut -c1-200 | head -12; echo ---; grep -n \"^## \\|^### \" docs/LLM_VS_CODE.md | head -20 | cut -c1-160",
 "description": "Check the spec and contract wording on date of service and severity"
}
````

### User / tool · 2026-11-03T01:30:16.979Z

**tool result**
````
spec/REQUIREMENTS.md:50:| R-TL-3 | **Date of service is the record's header date, parsed by code.** Dates inside the body are facts for the conflict check, never the entry date. | Seeded test on **record 7**: header 2026-05-18, body "Date of accident per intake form: 2026-01-19". If the model return
spec/REQUIREMENTS.md:351:| A-106 | The export cites each line by provider as written in the header + date of service with an `[Ex. __ / Bates __]` placeholder; the tool assigns no numbers; internal notes cite `record N (provider as written, date)` per R-EX-4 | R-EX-2, R-EX-4, R-EX-6 |
spec/REQUIREMENTS.md:356:- The date of service is the record's header date. Body dates are conflict evidence only (R-TL-3).
---
304:Gate panel: staff-engineer, qa (eval report attached), paralegal, legal-nurse, claims-adjuster (reads the sample-case output and tries to discredit it), privacy-compliance (prompt-injection probe 
382:- **Tier 2 (milestone gate):** the panel listed under each milestone, in parallel. You synthesize into `reviews/GATE-Mx-summary.md`: findings deduplicated, ranked by severity, each mapped to a new
386:Provide: the card and its acceptance criteria; the commit range or files; the running app URL and how to reach the sample case; the eval report path if relevant; what to exercise hands-on; the out
393:- Separate "this violates a spec constraint" (blocker) from "I would have done it differently" (minor), and label which is which.
398:- `blocker` → `fail`; ≥1 `major` → `changes`; else `pass`. A card returns to `in_progress` with `rounds += 1` and the findings pasted into its body.
418:1. **Grounding:** 100% of exported statements and amounts carry a verbatim excerpt that exists in the input (automated; any failure is a blocker).
462:4. `hiring-panel-reviewer` final grade has no row ≤ 2 and no blockers.
619:Billed charges: explicit charges are $6,240 (ER, record 2) and $2,150 (MRI, record 8) → running total of explicit charges **$8,390**. "Charge per visit $185" (record 4) is a **rate**, not a char
659:### D.2 Review finding (`reviews/<card>-<persona>.md`, markdown with a JSON block)
676:Severity: `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optio
713:- Output exactly the review finding format (D.2) to the path given in your brief; reply to the orchestrator in ≤ 40 lines: verdict, blockers, majors.
726:Reply with ≤ 40 lines: verdict, blockers, majors. Do not fix anything.
---
5:## The one-paragraph version
9:## The rules (enforced in code and tests, not only in prompts)
23:## The decision table
50:## The three-rung ladder in one picture
72:## Worked example 1: the sample case
83:## Worked example 2: a record that tries to give orders (golden case 07)
92:## Added in the second build wave (D-031 to D-035)
105:## What the tool is built never to do (from the sample case)
109:## Costs and honest limits
119:## Changing this table
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:30:43.657Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15",
 "description": "Run the full unit suite against the pinned HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T01:37:53.908Z

**tool result**
````
........................................................................ [ 85%]
........................................................................ [ 86%]
........................................................................ [ 87%]
........................................................................ [ 88%]
........................................................................ [ 90%]
........................................................................ [ 91%]
........................................................................ [ 92%]
........................................................................ [ 93%]
........................................................................ [ 94%]
........................................................................ [ 96%]
........................................................................ [ 97%]
........................................................................ [ 98%]
........................................................................ [ 99%]
.............................                                            [100%]
6137 passed, 12 skipped in 428.38s (0:07:08)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:38:13.117Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/mutants_t207.py",
 "content": "\"\"\"T-207 reviewer mutation spot-check (staff-engineer r1). Mutants are applied only to COPIES of the pinned HEAD archive (fc37fbc)\nunder the scratch dir given as argv[2]; the product tree is never edited. Each mutant's old string must occur exactly once (else the mutant is not applied).\n\nRun: <venv python> -I mutants_t207.py <archive root> <scratch work dir>\nA mutant is KILLED when the T-202 date suite (4 files) fails on the copy, SURVIVED when it passes.\n\"\"\"\nimport os\nimport shutil\nimport subprocess\nimport sys\n\nARCH, WORK = sys.argv[1], sys.argv[2]\nSUITE = [\n    \"tests/unit/test_t202_r3_allow_list.py\",\n    \"tests/unit/test_t202_r2_service_date_layouts.py\",\n    \"tests/unit/test_t202_charge_service_dates.py\",\n    \"tests/unit/test_t200_undated_charge_label.py\",\n]\n\n# (name, file, old, new, what the mutant changes)\nMUTANTS = [\n    (\"M1 statement-date rule off\", \"app/backend/service_date.py\",\n     \"feasible = [o for o in (\\\"MD\\\", \\\"DM\\\") if not ref or all(t.ambiguous[o] <= ref for t in amb)]\",\n     \"feasible = [o for o in (\\\"MD\\\", \\\"DM\\\")]\",\n     \"a numeric date that reads two ways is never settled by the statement date\"),\n    (\"M2 all -> any in statement rule\", \"app/backend/service_date.py\",\n     \"all(t.ambiguous[o] <= ref for t in amb)\",\n     \"any(t.ambiguous[o] <= ref for t in amb)\",\n     \"one labeled end after the statement no longer blocks a reading\"),\n    (\"M3 drop in-unit locale order\", \"app/backend/service_date.py\",\n     \"    if determined:\\n        order = next(iter(determined))\\n    elif amb:\",\n     \"    if False:\\n        order = None\\n    elif amb:\",\n     \"row 2 'resolved only' by the statement rule: the other end's order no longer settles it\"),\n    (\"M4 five-year bound 366*5 -> 365*5+1\", \"app/backend/service_date.py\",\n     \"days=366 * _YEARS_BEFORE)\",\n     \"days=365 * _YEARS_BEFORE + 1)\",\n     \"the 'more than five years before' bound moved to the calendar-exact day for this window\"),\n    (\"M5 no plausibility check at all\", \"app/backend/service_date.py\",\n     \"    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)\",\n     \"    return True\",\n     \"a service after its statement or years before it is read\"),\n    (\"M6 counted-undated keeps its note\", \"app/backend/store.py\",\n     \"    if not stated and not counted_undated:\",\n     \"    if not stated:\",\n     \"a counted charge with no date gets the Step 3 confirm note (row 3 says every not-certain charge does)\"),\n    (\"M7 visit-note header date default off\", \"app/backend/service_date.py\",\n     \"    if date_iso:                                                          # a dated encounter record\",\n     \"    if False:                                                             # a dated encounter record\",\n     \"a dated visit note no longer supplies its own date to a charge with no labeled date\"),\n    (\"M8 'Encounter date' heading dropped\", \"app/backend/service_date.py\",\n     \"encounter\\\\s+date|\",\n     \"\",\n     \"a column headed 'Encounter date' no longer names service (not in row 2's list)\"),\n    (\"M9 'Visit Date' heading dropped (control)\", \"app/backend/service_date.py\",\n     \"visit\\\\s+date|date\\\\s+of\\\\s+visit|\",\n     \"date\\\\s+of\\\\s+visit|\",\n     \"control: a heading named 'Visit Date' no longer names service; a pinned case should kill this\"),\n]\n\n\ndef run_suite(dst):\n    p = subprocess.run([sys.executable, \"-I\", \"-m\", \"pytest\", *SUITE, \"-q\", \"-p\", \"no:cacheprovider\", \"-x\"],\n                       cwd=dst, capture_output=True, text=True, env={**os.environ, \"PYTHONDONTWRITEBYTECODE\": \"1\"})\n    last = (p.stdout.strip().splitlines() or [\"(no output)\"])[-1]\n    return p.returncode, last\n\n\nrc0, line0 = run_suite(ARCH)\nprint(f\"BASELINE (unmutated archive): exit={rc0} | {line0}\")\nfor name, rel, old, new, what in MUTANTS:\n    dst = os.path.join(WORK, name.split()[0].lower())\n    if os.path.exists(dst):\n        shutil.rmtree(dst)\n    shutil.copytree(ARCH, dst)\n    path = os.path.join(dst, rel)\n    src = open(path, encoding=\"utf-8\").read()\n    n = src.count(old)\n    if n != 1:\n        print(f\"{name}: NOT APPLIED (old string occurs {n} times)\")\n        continue\n    mutated = src.replace(old, new)\n    if mutated.count(new) < 1 or mutated == src:\n        print(f\"{name}: NOT APPLIED (verify failed)\")\n        continue\n    with open(path, \"w\", encoding=\"utf-8\") as fh:\n        fh.write(mutated)\n    rc, line = run_suite(dst)\n    verdict = \"KILLED\" if rc != 0 else \"SURVIVED\"\n    print(f\"{name}: {verdict} | exit={rc} | {line} | {what}\")\n"
}
````

### User / tool · 2026-11-03T01:38:13.219Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/mutants_t207.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:38:18.854Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$H/mut-work\" && cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-207-r1/mutants_t207.py \"$H/head-fc37fbc\" \"$H/mut-work\" 2>&1 | tee artifacts/review-evidence/T-207-r1/mutants_t207.out",
 "description": "Apply the T-207 mutants to scratch copies and run the date suite on each",
 "timeout": 900000
}
````

### User / tool · 2026-11-03T01:39:05.283Z

**tool result**
````
BASELINE (unmutated archive): exit=0 | 211 passed in 10.53s
M1 statement-date rule off: KILLED | exit=1 | 1 failed, 82 passed in 0.42s | a numeric date that reads two ways is never settled by the statement date
M2 all -> any in statement rule: KILLED | exit=1 | 1 failed, 82 passed in 0.44s | one labeled end after the statement no longer blocks a reading
M3 drop in-unit locale order: KILLED | exit=1 | 1 failed, 158 passed in 0.50s | row 2 'resolved only' by the statement rule: the other end's order no longer settles it
M4 five-year bound 366*5 -> 365*5+1: SURVIVED | exit=0 | 211 passed in 7.21s | the 'more than five years before' bound moved to the calendar-exact day for this window
M5 no plausibility check at all: KILLED | exit=1 | 1 failed, 75 passed in 0.43s | a service after its statement or years before it is read
M6 counted-undated keeps its note: SURVIVED | exit=0 | 211 passed in 7.38s | a counted charge with no date gets the Step 3 confirm note (row 3 says every not-certain charge does)
M7 visit-note header date default off: KILLED | exit=1 | 1 failed, 18 passed in 0.41s | a dated visit note no longer supplies its own date to a charge with no labeled date
M8 'Encounter date' heading dropped: SURVIVED | exit=0 | 211 passed in 7.09s | a column headed 'Encounter date' no longer names service (not in row 2's list)
M9 'Visit Date' heading dropped (control): KILLED | exit=1 | 1 failed, 59 passed in 0.42s | control: a heading named 'Visit Date' no longer names service; a pinned case should kill this
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:39:10.014Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && sed -n '231,250p' tests/unit/test_t202_r3_allow_list.py | cut -c1-300; echo ...; sed -n '330,336p' tests/unit/test_t202_r3_allow_list.py | cut -c1-300",
 "description": "Read the period-rule and internal-notes tests that bear on the findings"
}
````

### User / tool · 2026-11-03T01:39:10.135Z

**tool result**
````
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

...
def test_the_internal_notes_list_each_charge_printed_without_a_certain_service_date():
    ex = "Itemized ledger. Date of service 04/05/2026: office visit charge $275.00. Patient DOB 03/20/1980, x-ray charge $180.00."
    rec = {"source": LEDGER, "date_iso": "2026-06-30"}
    amounts = []
    for i, a in enumerate(AM.find_amounts(ex)):
        d = store.charge_service_date({"excerpt": ex, "value_cents": a["cents"]}, rec, a["start"])
        amounts.append(dict(id=f"a{i}", record_no=1, cents=a["cents"], cls="charge", raw=a["raw"], excerpt=ex, review_status="accepted", pos=a["start"],
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:39:16.113Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut-work/m3; cd \"$H\" && grep -c \"if False:\" app/backend/service_date.py && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py -q -p no:cacheprovider -rf 2>&1 | grep -i \"^FAILED\\|passed\\|failed\" | cut -c1-400 | head -5",
 "description": "Identify which test kills the in-unit locale mutant",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:39:23.645Z

**tool result**
````
1
FAILED tests/unit/test_t202_r2_service_date_layouts.py::test_a_stated_period_prints_whole_with_its_own_year[06/28/2026-07/02/2026-June 28\u2013July 2, 2026-2026-07-10]
FAILED tests/unit/test_t202_r2_service_date_layouts.py::test_a_stated_period_prints_whole_with_its_own_year[06/28/2026 - 07/02/2026-June 28\u2013July 2, 2026-2026-07-10]
FAILED tests/unit/test_t202_r2_service_date_layouts.py::test_a_stated_period_prints_whole_with_its_own_year[06/28/2026\u201307/02/2026-June 28\u2013July 2, 2026-2026-07-10]
3 failed, 208 passed in 7.14s
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:39:40.234Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && echo \"--- dos_iso writers ---\"; grep -rn \"dos_iso\\s*=\\|\\\"dos_iso\\\"\\s*:\\|dos_text\\s*=\" app/ --include=*.py | cut -c1-200; echo \"--- letter_check imports ---\"; grep -n \"^import\\|^from\\|import app\\|from app\" evals/letter_check.py | head; echo \"--- letter_check CLI ---\"; grep -n \"__main__\\|def main\\|argv\" evals/letter_check.py | head -5; echo \"--- llm imports in export/store date path ---\"; grep -n \"^from\\|^import\" app/backend/export.py | head -20 | cut -c1-160",
 "description": "Check every writer of the charge date fields and the letter-check independence"
}
````

### User / tool · 2026-11-03T01:39:40.375Z

**tool result**
````
--- dos_iso writers ---
app/backend/billing.py:339:    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
app/backend/billing.py:479:            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
app/backend/billing.py:553:        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
--- letter_check imports ---
25:import contextlib
26:import json
27:import pathlib
28:import re
29:import sys
30:import tempfile
39:    from app.backend import money
45:    from app.backend import money
51:    from app.backend import money
64:    from app.backend import amounts as AM, export
--- letter_check CLI ---
523:def main(argv=None) -> int:
531:if __name__ == "__main__":
--- llm imports in export/store date path ---
16:from __future__ import annotations
18:import os
19:import re
20:from datetime import date
22:from app.backend import amounts, charge_text, language, money, service_date
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:39:45.573Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -rn \"billing\\.\\(lines\\|parse\\|ub04\\|cms\\|rows\\|_dos\\|[a-z_]*\\)(\" app/ --include=*.py | grep -v \"^app/backend/billing.py\" | cut -c1-200 | head -12; echo ---; grep -n \"^def \" app/backend/billing.py | cut -c1-120 | head -30",
 "description": "Check whether billing.py's own DOS parser feeds the letter"
}
````

### User / tool · 2026-11-03T01:39:45.694Z

**tool result**
````
app/backend/api.py:599:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
---
71:def fmt(cents, credit=False):
79:def _is_credit(token: str) -> bool:
84:def parse_figure(token: str) -> dict:
93:def _pf(m, base=0):
99:def _mag(f):
104:def _norm(s):
112:def _lap(a, b):
116:def _within(a, row):
120:def _offsets(lines):
128:def _row_span(base, text):
134:def _provider(rec: dict) -> str:
141:def _dos(raw):
146:def _cite(rec, line):
151:def form_of(rec: dict) -> str:
169:def _header(lines):
184:def _column(token_span, cols):
193:def _money_col(token_span, cols):
200:def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate", row=No
205:def _blank_dates(ln):
212:def _tokens(ln, cols=None, all_bare=False):
223:def _put_stated(rec, stated, new, out):
233:def _stated_orphans(rec, lform, got, stated):
243:def _family(form):
248:def _near(span, hdr):
252:def _ledger_table(rec, lines):
336:def _blank_line(rec, form, ln, dos=None, posted=None, code=None, description="", unparsed=False, unclear=None, unit=
344:def _add_unclear(line, text, at):
355:def _stated(rec, text, base=0):
377:def _segments(text):
387:def _ledger_text(rec, body):
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:39:50.540Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && sed -n '141,146p' app/backend/billing.py | cut -c1-260; echo ---; grep -rn \"dos_iso\\|\\.dos\\b\" app/frontend --include=*.js | cut -c1-180 | head -8; echo ---; grep -n \"add_routes\\|@app\\.\\(get\\|post\\)\" app/backend/billing.py | cut -c1-160 | head -6",
 "description": "Read billing.py DOS parser and check whether the UI shows it"
}
````

### User / tool · 2026-11-03T01:39:50.652Z

**tool result**
````
def _dos(raw):
    p = dates.parse_date(raw or "")
    return p["iso"] if p.get("status") == "parsed" else None


def _cite(rec, line):
---
---
1060:def add_routes(app, *, conn, get_case):
1061:    @app.get("/api/cases/{token}/billing")
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:39:56.126Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -rln \"/billing\" app/frontend | head -5; echo ---; sed -n '1060,1075p' app/backend/billing.py | cut -c1-220; echo ---; grep -n \"_dos(\\|dos_iso\" app/backend/billing.py | cut -c1-200",
 "description": "Check whether any frontend consumes the billing DOS endpoint"
}
````

### User / tool · 2026-11-03T01:39:56.251Z

**tool result**
````
---
def add_routes(app, *, conn, get_case):
    @app.get("/api/cases/{token}/billing")
    def billing_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"billing": for_case(c, token)}
        finally:
            c.close()
---
141:def _dos(raw):
339:    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
479:            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
553:        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:40:02.260Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && sed -n '523,535p' evals/letter_check.py | cut -c1-200; echo ---; PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m evals.letter_check 2>&1 | tail -8 | cut -c1-300; echo \"exit=$?\"",
 "description": "Run the letter check eval CLI against the pinned HEAD archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:40:02.380Z

**tool result**
````
def main(argv=None) -> int:
    m = measure()
    print(json.dumps({k: v for k, v in m.items() if k != "per_case"}))
    for name, v in m["per_case"].items():
        print(f"  {name}: {v}")
    return 0 if m["value"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
---
/Users/arsis/zlayt-pm-project/.venv/bin/python: Error while finding module specification for 'evals.letter_check' (ModuleNotFoundError: No module named 'evals')
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:40:05.245Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/letter_eval_t207.py",
 "content": "\"\"\"T-207 reviewer: run the letter-check eval (evals/letter_check.py main) against the pinned HEAD archive, read-only.\nRun: <venv python> -I letter_eval_t207.py <archive root>\n\"\"\"\nimport sys\n\nsys.path.insert(0, sys.argv[1])\n\nfrom evals import letter_check  # noqa: E402\n\nprint(\"archive:\", sys.argv[1])\nrc = letter_check.main([])\nprint(\"exit:\", rc)\n"
}
````

### User / tool · 2026-11-03T01:40:05.374Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/letter_eval_t207.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:40:08.728Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd /Users/arsis/zlayt-pm-project && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-207-r1/letter_eval_t207.py \"$H\" 2>&1 | tail -40 | cut -c1-400 | tee artifacts/review-evidence/T-207-r1/letter_eval_t207.out",
 "description": "Run the letter-check eval through a wrapper against the HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T01:40:19.882Z

**tool result**
````
archive: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
exit: 0
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:40:43.700Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -n \"_YEARS_BEFORE = \\|days=366\\|feasible = \\[\\|if date_iso:  \\|if date_iso:\\|_ASK_WRITTEN = \\|_ASK_NONE = \\|_H_SVC = \\|if determined:\\|def printed_text\\|BLANK = \" app/backend/service_date.py | cut -c1-90; echo ---; grep -n \"counted_undated = \\|if not stated and not counted_undated\\|\\\"confirm_note\\\": note\\|def charge_service_date\" app/backend/store.py | cut -c1-120; echo ---; grep -n \"def charge_when\\|return f\\\"{src}, {a.get('dos_text')\" app/backend/export.py | cut -c1-120; echo ---; grep -n \"^def test_a_stated_period_prints_whole_with_its_own_year\\|^def test_a_dated_visit\\|in a visit note a non-service date\\|^def test_a_period_reads_one_way\\|^def test_the_all_in\\|^def test_the_internal_notes\\|^def test_no_labeled_date_in_the_quote\" tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_r3_allow_list.py | cut -c1-150; echo ---; grep -n \"^| [123] |\" docs/LLM_VS_CODE.md | cut -c1-14; echo ---; grep -n \"R-TL-3\" spec/REQUIREMENTS.md | cut -c1-60; echo ---; grep -n \"def billing_get\\|def _dos\\|\\\"dos_iso\\\": _dos\" app/backend/billing.py | cut -c1-80; grep -n \"billing.add_routes\" app/backend/api.py | cut -c1-100",
 "description": "Verify exact line numbers for every citation in the review"
}
````

### User / tool · 2026-11-03T01:40:43.873Z

**tool result**
````
53:_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+d
55:_YEARS_BEFORE = 5                # a bill's service date more than this many years befo
76:BLANK = "date of service [__________]"
87:def printed_text(res: dict, statement_iso) -> str:
102:_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank fo
103:_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for t
215:    if determined:
218:        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref fo
274:    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedel
375:    if date_iso:                                                          # a dated en
---
118:def charge_service_date(item: dict, rec, pos) -> dict:
129:    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
139:    if not stated and not counted_undated:
143:            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}
146:def charge_service_dates(item: dict, rec, pos) -> tuple:
---
215:    def charge_when(self, a):
226:        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
---
tests/unit/test_t202_r3_allow_list.py:216:def test_no_labeled_date_in_the_quote_prints_the_blank_and_a_request_note():
tests/unit/test_t202_r3_allow_list.py:236:def test_a_period_reads_one_way_only_when_every_end_fits_one_reading(period, rd, label):
tests/unit/test_t202_r3_allow_list.py:245:def test_the_all_in_the_reference_rule_is_pinned_by_a_period_with_one_end_after_the_statement():
tests/unit/test_t202_r3_allow_list.py:330:def test_the_internal_notes_list_each_charge_printed_without_a_certain_service_date():
tests/unit/test_t202_r2_service_date_layouts.py:129:def test_a_stated_period_prints_whole_with_its_own_year(period, label, rec):
---
29:| 1 | Split
30:| 2 | Parse
31:| 3 | Date 
---
50:| R-TL-3 | **Date of service is the record's header date,
350:| A-105 | Each pasted record carries its date and source
356:- The date of service is the record's header date. Body 
---
141:def _dos(raw):
339:    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos
1062:    def billing_get(token: str):
599:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:40:52.430Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd \"$H\" && grep -n \"elif rec is None or pos is None\\|r = SD.resolve\\|def in_a_visit\\|def test_in_a_visit\" app/backend/store.py tests/unit/test_t202_r3_allow_list.py | cut -c1-140; grep -n \"def test_in_a_visit_note\" tests/unit/test_t202_r3_allow_list.py | cut -c1-120; grep -n \"def test_a_single_date_under_a_service_heading\" tests/unit/test_t202_r3_allow_list.py | cut -c1-100; cd /Users/arsis/zlayt-pm-project && grep -n \"T-207\" board/activity.jsonl | tail -3 | cut -c1-200",
 "description": "Get exact line numbers for the remaining citations"
}
````

### User / tool · 2026-11-03T01:40:52.564Z

**tool result**
````
tests/unit/test_t202_r3_allow_list.py:98:def test_in_a_visit_note_a_non_service_date_leaves_the_notes_own_date(ex, fig, want):
app/backend/store.py:133:    elif rec is None or pos is None or not item.get("excerpt"):
app/backend/store.py:136:        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
98:def test_in_a_visit_note_a_non_service_date_leaves_the_notes_own_date(ex, fig, want):
138:def test_a_single_date_under_a_service_heading_prints(heading):
4856:{"ts": "2026-11-03T01:26:49Z", "event": "commit", "agent": "architect", "card": "T-207", "text": "fc37fbc"}
4857:{"ts": "2026-11-03T01:26:49Z", "event": "note", "agent": "architect", "card": "T-207", "text": "Applied the backend correction (row 3, 'shows as written' and 'service date not stated' sentences r
4858:{"ts": "2026-11-03T01:26:55Z", "event": "dispatch", "agent": "orchestrator", "card": "T-207", "text": "review dispatched: staff-engineer-reviewer"}
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:41:00.254Z

**tool call — Bash**
````
{
 "command": "grep -n -o \".\\{60\\}service date not stated.\\{30\\}\\|.\\{60\\}shows as written.\\{30\\}\\|.\\{40\\}28 mutants.\\{20\\}\\|.\\{40\\}24 mutants.\\{20\\}\" docs/LLM_VS_CODE.md | cut -c1-200; echo \"--- HEAD copy ---\"; H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; grep -n -o \".\\{60\\}service date not stated.\\{30\\}\\|.\\{60\\}shows as written.\\{30\\}\\|.\\{40\\}28 mutants.\\{20\\}\\|.\\{40\\}24 mutants.\\{20\\}\" \"$H/docs/LLM_VS_CODE.md\" | cut -c1-200; echo \"--- diff check ---\"; git -C /Users/arsis/zlayt-pm-project diff --stat HEAD -- docs/LLM_VS_CODE.md | tail -1",
 "description": "Check for stale wording in the table and whether the working copy matches HEAD"
}
````

### User / tool · 2026-11-03T01:41:00.399Z

**tool result**
````
31:py` (every reviewer probe is a fixture; 24 mutants of the resolver and
--- HEAD copy ---
31:py` (every reviewer probe is a fixture; 24 mutants of the resolver and
--- diff check ---
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:41:27.753Z

**tool call — Bash**
````
{
 "command": "grep -rn -i \"mutant\" tests/unit evals --include=*.py | cut -c1-140 | head -20; echo \"count=$(grep -rn -i mutant tests/unit evals --include=*.py | wc -l)\"",
 "description": "Search tests and evals for any committed mutation harness"
}
````

### User / tool · 2026-11-03T01:41:27.861Z

**tool result**
````
tests/unit/test_t208_ai_wording.py:33:def test_mutant_label_on_an_english_letter_fails():
tests/unit/test_t208_ai_wording.py:38:    assert LC.ai_wording(f"TREATMENT CHRONOLOGY\n\n{OK}\n", [])      # under the heading, as the revie
tests/unit/test_billing.py:807:    """The accounting test must be able to fail for EOB rows (r1 M3, mutant M06). Distinct figures, so each d
tests/unit/test_billing.py:819:        _eob_line(out)["unclear"] = []                                  # mutant M06: the unclear list droppe
tests/unit/test_billing.py:906:# ---- prose: an unlabelled figure is never a charge (pins the prose charge gate; reviewer mutant M05) and ne
tests/unit/test_uncovered.py:85:    "J. Smith, MD",                                                # a bare ', MD' signature line (mutant S)
tests/unit/test_summary_trim.py:678:# ---- mutants that survived the T-112 r3 review -------------------------------------------------------
tests/unit/test_t132_attribution_unit.py:68:# 3. the history-word gate (T-120 r3 staff minor 2, mutant F) ----------------------------------
tests/unit/test_t132_attribution_unit.py:129:# ---- mutants M8, M9, M10 of the round-1 review ----------------------------------------------
tests/unit/test_t132_attribution_unit.py:200:# ---- the surviving mutants C6, C7, S6 (and S3 above) ----------------------------------------
tests/unit/test_t132_attribution_unit.py:456:# ---- mutant-killing rows for the r4 code (section header at a line start, long prefix before 
tests/unit/test_t133_lexicon.py:59:    # mutant: drop 'denying' from the cue list and the guard no longer suppresses it (the test above woul
tests/unit/test_t133_lexicon.py:171:    # mutant: drop the "History:" header exclusion and the bare header form flags again (the test above 
tests/unit/test_t133_lexicon.py:220:    # mutant: make the header guard apply to every history word (the f939ccb regression) and the qualifi
tests/unit/test_t133_lexicon.py:372:    # mutant: the 6fa8ecc guard (\s in the look-behind) lets the own-line header flag, so the test above
tests/unit/test_t141_checks_per_case.py:79:# ---------------------------------------------------------------- T-141 round 3: notes at read t
tests/unit/test_dismissal_patterns.py:137:    """Demo/public mode: case B sees nothing from case A; apply refuses; a forced-local route (mut
tests/unit/test_t159_flag_audit.py:104:    """r2 mutant: the confirm must land on the NEWEST accept event, so the first accept keeps its own
tests/unit/test_t159_flag_audit.py:120:    """r2 mutant: the no-op needs the confirm to have happened (confirmed_at), not just the flag to e
tests/unit/test_calibration_route.py:287:    """Fail closed: when the current prompts cannot be read the numbers are not shown as current (T
count=      28
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:41:32.427Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/probe_t207_p8.py",
 "content": "\"\"\"T-207 reviewer probe P8 (staff-engineer r1): a non-bill charge whose figure offset does not resolve (pos None) gets the record's header date.\nRead-only. Run: <venv python> -I probe_t207_p8.py <archive root>\n\"\"\"\nimport sys\n\nsys.path.insert(0, sys.argv[1])\n\nfrom app.backend import store  # noqa: E402\n\nNOTE = \"Dr. Alvarez, primary care, progress note\"\nex = \"Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.\"\nitem = {\"excerpt\": ex, \"value_cents\": 24000}\nd = store.charge_service_date(item, {\"source\": NOTE, \"date_iso\": \"2026-01-09\"}, None)\nprint(f\"P8 pos=None non-bill | state={d['state']} | date_iso={d['date_iso']} | text={d['text']!r} | reason={d['reason']}\")\nbill = store.charge_service_date(dict(item), {\"source\": \"Brindlewood Physical Therapy, itemized ledger\", \"date_iso\": \"2026-06-30\"}, None)\nprint(f\"P8 pos=None ledger  | state={bill['state']} | date_iso={bill['date_iso']} | text={bill['text']!r} | reason={bill['reason']}\")\n"
}
````

### User / tool · 2026-11-03T01:41:32.551Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/probe_t207_p8.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:41:35.797Z

**tool call — Bash**
````
{
 "command": "H=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-fc37fbc; cd /Users/arsis/zlayt-pm-project && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-207-r1/probe_t207_p8.py \"$H\" 2>&1 | tee artifacts/review-evidence/T-207-r1/probe_t207_p8.out",
 "description": "Run probe P8 for the pos-None default against the HEAD archive"
}
````

### User / tool · 2026-11-03T01:41:36.120Z

**tool result**
````
P8 pos=None non-bill | state=stated | date_iso=2026-01-09 | text='January 9, 2026' | reason=None
P8 pos=None ledger  | state=not_stated | date_iso=None | text='date of service [__________] (statement dated June 30, 2026)' | reason=no_date
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:00.507Z

Checks are done. Before writing the review, I'm confirming that no review file for T-207 exists yet and that the reviews directory is writable by me.

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:01.071Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -c \"^T-207\" ; ls reviews/T-207* 2>/dev/null; echo \"exists-check-done\"; .venv/bin/python -I -c \"print('ok')\"",
 "description": "Confirm no existing T-207 review file before writing"
}
````

### User / tool · 2026-11-03T01:42:01.192Z

**tool result**
````
0
exists-check-done
ok
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:31.505Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer.md",
 "content": "# T-207 staff-engineer review, r1\n\nReviewer: staff-engineer-reviewer (Marcus Lee persona). Fresh context, read-only on product code. Pinned to HEAD fc37fbc (archived to a scratch copy; the product tree was not edited).\n\nScope: docs/LLM_VS_CODE.md rows 2 and 3 (commits 901ad5a and fc37fbc), checked against app/backend/service_date.py, app/backend/store.py charge_service_date (lines 118-147) and app/backend/export.py charge_when (lines 215-226). Rules: memory/ORCHESTRATOR_DECISIONS.md D-071 and its amendment, clarification and addendum (lines 84-93). Spec: spec/REQUIREMENTS.md R-TL-3 (lines 50 and 356).\n\n## Answers to the four questions\n\n1. The date is code only, never the LLM. Holds. service_date.py imports only datetime, re and app.backend.amounts (lines 22-25). The charge path (store.py:118-147, export.py:215-226, present.py:152) calls no model. evals/letter_check.py has its own scanner and does not import service_date.\n2. An allow-list of positive evidence decides it. Holds for the four listed ties, with gaps. The row's column-header list is narrower than the code (F6). Two other paths decide a printed date that row 2 does not name: a same-period locale rule (F1) and the header date of a visit note (F3).\n3. The statement-date disambiguation rule applies. Holds. A date that reads two ways is blank when both readings fall on or before the statement (probe P1), and a single reading is printed when the other is after it (probe P2). Mutants M1 and M2 are killed.\n4. A not-certain case gets the fillable blank plus a Step 3 note. The blank holds: it matches the D-071 addendum text (probe P7). The note holds except for counted undated charges (F4), and its wording for the no-label case differs from row 3 (F7).\n\nVerdict: changes. No blocker. Five majors, three minors. I did not downgrade any finding for convenience.\n\nModel note: the dossier and the brief expect claude-sonnet-5-5. The model I am running as is claude-haiku-5-5, and that is the id recorded below.\n\n## Exercised\n\n1. git show 901ad5a and git show fc37fbc: each changes only docs/LLM_VS_CODE.md (2 lines and 1 line). git rev-parse HEAD gives fc37fbcec0ebdb7705e4d91c2ad43afd67a82568. git diff --stat HEAD -- docs/LLM_VS_CODE.md is empty, so the working copy matches HEAD.\n2. git archive HEAD into a scratch copy at the pinned sha (read and run only).\n3. Read rows 2 and 3 at HEAD (docs/LLM_VS_CODE.md:30-31), the D-071 block (memory/ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (spec/REQUIREMENTS.md:50, :356), and board.py show T-207 (reviews: []; commits 901ad5a, fc37fbc).\n4. Read app/backend/service_date.py in full (377 lines) at HEAD. Grepped the dos_iso and dos_text writers, and the import lines of the date path.\n5. pytest tests/unit -q on the HEAD archive: 6137 passed, 12 skipped (428 s).\n6. pytest on the four T-202 date files (test_t202_r3_allow_list, test_t202_r2_service_date_layouts, test_t202_charge_service_dates, test_t200_undated_charge_label): 211 passed.\n7. Probes P1 to P8 against the HEAD archive: artifacts/review-evidence/T-207-r1/probe_t207.py with probe_t207.out, and probe_t207_p8.py with probe_t207_p8.out.\n8. Nine mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py with mutants_t207.out. Baseline 211 passed. M1, M2, M3, M5, M7 and M9 killed; M4, M6 and M8 survived.\n9. letter-check eval (evals/letter_check.py main, fixture backend): artifacts/review-evidence/T-207-r1/letter_eval_t207.py with letter_eval_t207.out. Output: value 0, cases 25, exit 0.\n10. grep -rn -i mutant tests/unit evals --include=*.py: 28 hits, all comments from other cards. None is a harness for the date resolver's 24 mutants.\n\n## Findings\n\nF1 (major). Row 2 says a two-reading date is certain \"only when\" the statement rule decides it. The code also settles an end from the other end's order inside the same period. Probe P3, input \"DOS 04/05/2026 - 13/05/2026 therapy $120.00.\" with statement 2026-06-30, prints \"stated | 2026-05-04 | 2026-05-13\". The row says that case is ambiguous and prints the blank. The code path is service_date.py:215-217 (if determined: order = next(iter(determined))). It is pinned by tests/unit/test_t202_r2_service_date_layouts.py:129 (mutant M3 is killed by it). D-071's amendment (memory/ORCHESTRATOR_DECISIONS.md:87) mentions \"no locale rule from the record\", so a locale rule is contemplated, but the table does not state it. Not a blocker: the rule is deterministic, tested, and uses the record's own other end.\n\nF2 (major). Row 2 says a bill date \"more than five years before it is not read\". The code allows 1830 days (service_date.py:55 _YEARS_BEFORE = 5; :274 days=366 * _YEARS_BEFORE). Probe P4 with statement 2026-06-30: \"P4 06/29/2021 | $120.00 | stated | 2021-06-29\" (five years and one day before) and \"P4 06/26/2021 | $120.00 | stated | 2021-06-26\" (five years and four days before). The day 06/25/2021 is refused as implausible. Mutant M4 (calendar-exact bound 365*5+1) survives all 211 tests. The only bound tests are 1998 and 2031 (tests/unit/test_t202_r3_allow_list.py:187-188). Persona calibration: a missing boundary test is major.\n\nF3 (major). A charge with no labeled service date takes the visit note's header date. Probe P5: \"Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.\" on a progress note dated 2026-01-09 prints \"stated | 2026-01-09 | text='January 9, 2026'\". Probe P8 shows the same default when the figure offset cannot be located (store.py:133-136 falls back to the header date for a non-bill record; a ledger prints the blank). The default is at service_date.py:375-376 and is pinned by test_t202_r3_allow_list.py:98 (mutant M7 killed). Row 2 says \"Only a date tied to the line by\" four listed ties counts, and row 3 says the header date is not the DOS \"for a bill\". Spec R-TL-3 (spec/REQUIREMENTS.md:50) says \"Date of service is the record's header date, parsed by code\", so the code follows the spec and the table is incomplete. Persona §5 would treat a silent default as a blocker. I do not rate it one because the spec authorizes the header date, no fact is invented, and nothing is hidden. The defect is that the table says otherwise. Chris must rule (Q1).\n\nF4 (major). A counted undated charge gets no Step 3 note. Probe P6, counted via D-064 (\"Count this charge\"), prints \"not_stated | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None\". The uncounted line (P6-uncounted) gets a note. The suppression is store.py:139 (if not stated and not counted_undated:), and mutant M6 survives. Row 3 (docs/LLM_VS_CODE.md:31) says \"Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it\". The brief also requires a note for every not-certain case. The blank still prints in the letter, so nothing is invented or lost. Major, not blocker.\n\nF5 (major). The row 3 Validation cell says \"24 mutants of the resolver and the check all fail the unit suite\" (docs/LLM_VS_CODE.md:31). Two resolver mutants survive the 211-test date suite: M4 (five-year bound, service_date.py:274) and M8 (the \"Encounter date\" heading, service_date.py:53). The count of 24 cannot be reproduced: no harness exists in the repo (item 10 above). The claim is refuted, so it is a finding.\n\nF6 (minor). Row 2 lists \"a DOS or service column header\". The code's heading set (service_date.py:53-54) also accepts Visit Date, Date of Visit, Encounter Date, SVC and 24A. Encounter Date has no test (M8 survives). Fix: list the set in row 2 and test it.\n\nF7 (minor). Row 3 says the note asks the paralegal to \"read the date from the quote\" and \"names the date as the quote writes it\". That holds for the written-date reasons (service_date.py:102). For the no-label reason the note says \"Request a dated itemized bill, or fill the blank from the record\" and names no date (service_date.py:103; probe P7b). Fix: align the row or the note.\n\nF8 (minor). billing.py:141 (_dos, via dates.parse_date) and billing.py:339 emit a per-line dos_iso served at GET /api/cases/{token}/billing (billing.py:1062, registered at api.py:599). This is a second date-of-service derivation outside row 2's \"only\" claim. It does not reach the letter (dos_iso writers listed in item 4) and I found no frontend consumer. Fix: say in row 2 that it is not a charge date, or remove it.\n\n## What is right\n\n1. The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.\n2. The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.\n3. The blank matches the D-071 addendum text exactly (\"date of service [__________] (statement dated June 30, 2026)\", probe P7), and letter_check reports value 0 over 25 cases.\n\nOutside my lens: the wording of Step 3 UI copy beyond the note strings, and the legal weight of the blank.\n\n```json\n{\"card\": \"T-207\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"docs/LLM_VS_CODE.md rows 2-3 at HEAD fc37fbc (commits 901ad5a, fc37fbc); app/backend/service_date.py, app/backend/store.py:118-147, app/backend/export.py:215-226; memory/ORCHESTRATOR_DECISIONS.md D-071 lines 84-93; spec/REQUIREMENTS.md R-TL-3; no app URL exercised\",\n \"exercised\": [\"git show 901ad5a and fc37fbc (docs only); git rev-parse HEAD = fc37fbcec0eb; git diff --stat HEAD -- docs/LLM_VS_CODE.md empty\",\n               \"git archive HEAD into scratch copy head-fc37fbc (pinned, read and run only)\",\n               \"read rows 2-3 (docs/LLM_VS_CODE.md:30-31), D-071 block (ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (REQUIREMENTS.md:50, 356), board.py show T-207\",\n               \"read service_date.py in full (377 lines) at HEAD; store.py:118-147; export.py:215-226; grep dos_iso writers and date-path imports\",\n               \"pytest tests/unit -q at HEAD archive: 6137 passed, 12 skipped\",\n               \"pytest on 4 T-202 date files: 211 passed\",\n               \"probes P1-P8: artifacts/review-evidence/T-207-r1/probe_t207.py (+.out), probe_t207_p8.py (+.out)\",\n               \"9 mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py (+.out); M4, M6, M8 survived; M1 M2 M3 M5 M7 M9 killed\",\n               \"letter_check eval via letter_eval_t207.py (+.out): value 0, 25 cases, exit 0\",\n               \"grep -rn -i mutant tests/unit evals: 28 comment hits, no 24-mutant harness\"],\n \"verdict\": \"changes\",\n \"scores\": {\"row2_matches_code\": 3, \"row3_matches_code\": 3, \"date_is_code_only\": 5, \"allow_list_decides\": 3, \"statement_date_rule\": 4, \"not_certain_blank_and_note\": 3, \"tests_and_validation_claims\": 2},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Row 2 says a two-reading date is certain only by the statement rule; code also settles it from the other end of the same period\",\n   \"evidence\": \"probe_t207.out line 'P3 | $120.00 | stated | 2026-05-04 | 2026-05-13' for 'DOS 04/05/2026 - 13/05/2026 therapy $120.00.' (statement 2026-06-30); app/backend/service_date.py:215-217 'if determined: order = next(iter(determined))'; docs/LLM_VS_CODE.md:30 'it is certain only when a reading after the bill's own (statement) date is impossible'; tests/unit/test_t202_r2_service_date_layouts.py:129 kills M3\",\n   \"why_it_matters\": \"The table is the binding description of how a printed date is decided. It says the statement rule is the only resolver; the code and a tested test use a second rule. D-071's amendment contemplates a record-level locale rule, but the table does not state one.\",\n   \"fix\": \"Architect amends row 2 to state the same-period locale rule (cite D-071 amendment 'no locale rule from the record'), or the code drops the rule and the period prints the blank.\",\n   \"acceptance_test\": \"Row 2 names the rule the code applies; a test pins '04/05/2026 - 13/05/2026' to the decided answer; mutant M3 stays killed.\"},\n  {\"severity\": \"major\", \"title\": \"Five-year bound is 1830 days, not 'more than five years'; no test sits at the boundary\",\n   \"evidence\": \"app/backend/service_date.py:55 '_YEARS_BEFORE = 5'; :274 'days=366 * _YEARS_BEFORE'; probe_t207.out 'P4 06/29/2021 | $120.00 | stated | 2021-06-29' (5y+1d before 2026-06-30) and 'P4 06/26/2021 | $120.00 | stated | 2021-06-26'; mutants_t207.out 'M4 ... SURVIVED | exit=0 | 211 passed'; tests only at 1998/2031 (tests/unit/test_t202_r3_allow_list.py:187-188); docs/LLM_VS_CODE.md:30 'more than five years before it is not read'\",\n   \"why_it_matters\": \"A service date 5y+1d to 5y+4d before the statement is printed as a date of service though row 2 says it is not read. No test would catch it. Persona calibration: missing boundary test is major.\",\n   \"fix\": \"Compare calendar years (statement date minus five years, same month and day, 29 Feb handled) instead of 366-day arithmetic; keep 1998 and 2031.\",\n   \"acceptance_test\": \"Statement 2026-06-30: 06/29/2021 prints the blank with reason implausible; 06/30/2021 is stated; M4 is killed.\"},\n  {\"severity\": \"major\", \"title\": \"A charge with no labeled date takes the visit note's header date; row 2 says only the allow-list counts\",\n   \"evidence\": \"probe_t207.out 'P5-store | $240.00 | stated | 2026-01-09 | None | None | text='January 9, 2026' | note=None' for 'Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.'; probe_t207_p8.out 'P8 pos=None non-bill | state=stated | date_iso=2026-01-09' vs 'P8 pos=None ledger | state=not_stated'; app/backend/service_date.py:375-376 'if date_iso:' ... 'state=\\\"stated\\\", first=date_iso'; app/backend/store.py:133-136; tests/unit/test_t202_r3_allow_list.py:98 pins it; mutants_t207.out 'M7 ... KILLED'; docs/LLM_VS_CODE.md:30 'Only a date tied to the line by ... counts'; spec/REQUIREMENTS.md:50 'Date of service is the record's header date, parsed by code.'\",\n   \"why_it_matters\": \"The code follows R-TL-3 for encounter records and nothing is invented, but the table says the allow-list decides and that the header date is not the DOS for a bill only. The table misstates a rule that decides a printed date. Under persona §5 an unannounced default would be a blocker; R-TL-3 authorizes it here, so I rate it major.\",\n   \"fix\": \"Chris rules (Q1). If yes, row 2 names the encounter-header rule and cites R-TL-3. The pos-None branch at store.py:133 then either follows the same rule and says so, or prints the blank as the ledger path does.\",\n   \"acceptance_test\": \"Row 2 states the rule; a test with pos=None on a visit-note charge matches the ruling; M7 stays killed.\"},\n  {\"severity\": \"major\", \"title\": \"A counted undated charge prints the blank with no Step 3 confirm note\",\n   \"evidence\": \"probe_t207.out 'P6 | $250.00 | not_stated | None | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None' vs 'P6-uncounted ... note=' with a note; app/backend/store.py:129 (counted_undated) and :139 'if not stated and not counted_undated:'; mutants_t207.out 'M6 ... SURVIVED'; docs/LLM_VS_CODE.md:31 'Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it'; memory/ORCHESTRATOR_DECISIONS.md:72 D-064 'then sums like any accepted charge'\",\n   \"why_it_matters\": \"Row 3 and the brief require a Step 3 note for every not-certain case. Once the paralegal counts the line, the prompt disappears; the blank still prints, so nothing is invented or lost. Major, not blocker.\",\n   \"fix\": \"Either row 3 says counted lines carry no note and cites D-064, or store.py:139 keeps the note with 'Count this charge' wording.\",\n   \"acceptance_test\": \"A test on a counted undated charge asserts the decided note behaviour; M6 is killed or the row is amended.\"},\n  {\"severity\": \"major\", \"title\": \"Validation cell claims 24 mutants all fail; two resolver mutants survive and no 24-mutant harness exists\",\n   \"evidence\": \"docs/LLM_VS_CODE.md:31 '24 mutants of the resolver and the check all fail the unit suite'; mutants_t207.out 'M4 five-year bound ... SURVIVED' (service_date.py:274) and 'M8 Encounter date heading dropped ... SURVIVED' (service_date.py:53); grep -rn -i mutant tests/unit evals --include=*.py returns 28 comment hits from other cards\",\n   \"why_it_matters\": \"A validation claim that the reviewer can refute is a finding. The cell is part of the checked artifact (row 3 'How it is checked').\",\n   \"fix\": \"Amend the cell to the tests that exist, or commit the mutation harness with its count; add tests that kill M4 and M8.\",\n   \"acceptance_test\": \"The cell names only committed tests; the harness, if committed, reports 24 of 24 killed; M4 and M8 are killed.\"},\n  {\"severity\": \"minor\", \"title\": \"Row 2's column-heading list is narrower than the code\",\n   \"evidence\": \"docs/LLM_VS_CODE.md:30 'a DOS or service column header'; app/backend/service_date.py:53-54 _H_SVC also matches visit date, date of visit, encounter date, svc, 24A, from/to service; M8 survives\",\n   \"why_it_matters\": \"A reader cannot tell which headings decide a printed date.\",\n   \"fix\": \"List the heading set in row 2; add a test for Encounter Date.\",\n   \"acceptance_test\": \"Row 2 lists the set; M8 is killed.\"},\n  {\"severity\": \"minor\", \"title\": \"Row 3's note wording holds only for written-date reasons\",\n   \"evidence\": \"docs/LLM_VS_CODE.md:31 'asking the paralegal to read the date from the quote' and 'names the date as the quote writes it'; app/backend/service_date.py:102 (written-date note) vs :103 'Request a dated itemized bill, or fill the blank from the record'; probe_t207.out 'P7b ... note=The line states no date of service ...'\",\n   \"why_it_matters\": \"The no-label note does not name a date and does not ask for the quote, so row 3 overstates the note.\",\n   \"fix\": \"Align row 3 with the two note forms, or change the no-label note to point to the quote.\",\n   \"acceptance_test\": \"The row and the note text agree; the existing confirm-note test still passes.\"},\n  {\"severity\": \"minor\", \"title\": \"A second date-of-service parser on billing lines sits outside row 2's only-path claim\",\n   \"evidence\": \"app/backend/billing.py:141 'def _dos(raw): p = dates.parse_date(raw or \\\"\\\")'; billing.py:339 'dos_iso': _dos(dos); billing.py:1062 GET /api/cases/{token}/billing; api.py:599 billing.add_routes; no frontend consumer (grep app/frontend for /billing empty)\",\n   \"why_it_matters\": \"Row 2 says a charge line's date of service is read only by service_date.py. This endpoint returns a DOS per bill line by a generic parser. It does not reach the letter, but it is a second source of the same fact.\",\n   \"fix\": \"Document the endpoint's dos_iso as not a charge date in row 2, or remove it.\",\n   \"acceptance_test\": \"Row 2 names the endpoint's status; grep for dos_iso writers shows no second charge-date path.\"}\n ],\n \"whats_right\": [\"The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.\",\n                 \"The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.\",\n                 \"The blank matches the D-071 addendum text exactly (probe P7), and letter_check reports value 0 over 25 cases.\"],\n \"questions_for_chris\": [\"Q1 (F3): Should a dated visit note's header date be the date of service for a charge with no labeled date? R-TL-3 says yes; row 2 says only the allow-list counts.\",\n                         \"Q2 (F1): Is the same-period locale rule approved ('04/05/2026 - 13/05/2026' as May 4-13), or should that period print the blank as row 2 states?\",\n                         \"Q3 (F4): Should a counted undated charge (D-064) show the Step 3 confirm note?\"]}\n```\n"
}
````

### User / tool · 2026-11-03T01:42:31.668Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:35.430Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-207-staff-engineer.md',encoding='utf-8').read()\nfences=re.findall(r'\\`\\`\\`json', t)\nprint('json fences:', len(fences), '| all fences:', len(re.findall(r'\\`\\`\\`', t)))\nblk=re.search(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S).group(1)\nj=json.loads(blk)\nsev=[f['severity'] for f in j['findings']]\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('keys:', sorted(j.keys()))\nprint('verdict:', j['verdict'], '| expected by rule:', exp, '| match:', j['verdict']==exp)\nprint('severities:', {s: sev.count(s) for s in set(sev)})\nprint('whats_right:', len(j['whats_right']), '| questions:', len(j['questions_for_chris']), '| model:', j['model'])\nprint('findings keys ok:', all(set(f)>= {'severity','title','evidence','why_it_matters','fix','acceptance_test'} for f in j['findings']))\n\"",
 "description": "Validate the review file: single json fence, parse, verdict rule"
}
````

### User / tool · 2026-11-03T01:42:35.491Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:39.121Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/check_review_t207.py",
 "content": "\"\"\"T-207 reviewer self-check of reviews/T-207-staff-engineer.md: one json fence, parses, verdict follows the D.2 rule. Read-only.\"\"\"\nimport json\nimport re\n\nPATH = \"/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer.md\"\nFENCE = \"`\" * 3\ntext = open(PATH, encoding=\"utf-8\").read()\njson_fences = re.findall(FENCE + \"json\", text)\nall_fences = re.findall(FENCE, text)\nprint(\"json fences:\", len(json_fences), \"| all fences:\", len(all_fences))\nblock = re.search(FENCE + r\"json\\n(.*?)\\n\" + FENCE, text, re.S).group(1)\nj = json.loads(block)\nsev = [f[\"severity\"] for f in j[\"findings\"]]\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"keys:\", sorted(j.keys()))\nprint(\"verdict:\", j[\"verdict\"], \"| rule gives:\", expected, \"| match:\", j[\"verdict\"] == expected)\nprint(\"severities:\", {s: sev.count(s) for s in sorted(set(sev))})\nprint(\"whats_right:\", len(j[\"whats_right\"]), \"| questions:\", len(j[\"questions_for_chris\"]), \"| model:\", j[\"model\"], \"| card:\", j[\"card\"], \"| persona:\", j[\"persona\"])\nneed = {\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"}\nprint(\"finding fields complete:\", all(need <= set(f) for f in j[\"findings\"]))\n"
}
````

### User / tool · 2026-11-03T01:42:39.222Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r1/check_review_t207.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:40.735Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-207-r1/check_review_t207.py",
 "description": "Run the review self-check script (fence count, JSON parse, verdict rule)"
}
````

### User / tool · 2026-11-03T01:42:40.844Z

**tool result**
````
json fences: 1 | all fences: 2
keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right']
verdict: changes | rule gives: changes | match: True
severities: {'major': 5, 'minor': 3}
whats_right: 3 | questions: 3 | model: claude-haiku-5-5 | card: T-207 | persona: staff-engineer-reviewer
finding fields complete: True
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:43.869Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -8",
 "description": "Run the board validator (read-only) over the review set"
}
````

### User / tool · 2026-11-03T01:42:44.027Z

**tool result**
````
ok (209 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:49.785Z

The review file validates (one json fence, verdict `changes` matches the D.2 rule, board validator ok). Next I'm updating my memory: a new pattern file and an index line, plus an addendum on the guard behaviour I hit.

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:50.179Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_guard_blocks_shell_expansions.md"
}
````

### User / tool · 2026-11-03T01:42:50.189Z

**tool result**
````
1	---
2	name: feedback_guard_blocks_shell_expansions
3	description: git-guard and board-guard refuse shell parameter expansion in command position, and board.py commands with 2> redirects; do citation loops in a python -I script under artifacts/review-evidence
4	metadata:
5	  type: feedback
6	---
7	
8	A bash `for` loop with `${spec%%:*}` expansions was blocked by git-guard ("unresolved variable or substitution in command position"), and a
9	`cd ... && python3 tools/board.py ... 2>&1` line was blocked by board-guard ("`2>` is not allowed" for reviewers, which may only run
10	validate/show/list/status read-only). Whole blocked commands do not run, so a helper script written in the same command is never created.
11	
12	**Why:** T-173 r1 (this session): the first citation loop and the first check script both failed silently at the hook, and I only found
13	out from a later "No such file" error.
14	
15	**How to apply:** for citation checks and output parsing, write the script with the Write tool under artifacts/review-evidence/<card>-r<n>/
16	and run it with `.venv/bin/python -I`. Use plain `python3 tools/board.py validate` without redirects. Do not use `$var` expansions in a
17	shell loop.
18	
19	Related: [[feedback_review_write_once]] (proof-read citations before the first Write).
20	
21	**T-197 r1 addendum:** board-guard read `<%ae>` inside a `git show --format=` string as an input redirect and denied the whole command. A `python -c` string holding triple-backtick fences was denied by git-guard ("could not parse command safely"). Keep git format strings to `%an %ad %s` with no angle brackets, and put fences in a .py file. A stray `rm -rf` in a multi-step command was also refused. Keep cleanup out of setup commands.
22	
23	**T-175 r2 addendum:** board-guard denied `git branch` for reviewers in the project ("allowed only in scratch repos under /tmp"). `git merge-base --is-ancestor <sha> HEAD` and `git log -S <string> -- <paths>` both ran. A plain `python3 -c "import time; time.sleep(100)"` in the foreground ran without a block, but it is a poor habit: check the background task instead.
24	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:53.179Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_guard_blocks_shell_expansions.md",
 "old_string": "**T-175 r2 addendum:** board-guard denied `git branch` for reviewers",
 "new_string": "**T-207 r1 addendum:** three shell lines were refused. An `awk 'NR>=27 && NR<=40'` program was read as a redirect (\"redirect to =27\"). An `echo \"$S\" > \"$H/.x\"` into the scratchpad was refused (\"redirect to $(echo/.headpath)\"). A `python3 -c` self-check with backtick and `\\\"` escapes was refused (\"could not parse command safely (No escaped character)\"). What worked: `sed -n 'a,bp'` for ranges, `git archive HEAD | tar -x -C <scratch>`, `.venv/bin/python -I <file under artifacts/review-evidence>` for every probe, mutant and check, and `tee` into artifacts/review-evidence/. Do not put `>`, `$(...)` or escapes inside a command line; write a file and run it.\n\n**T-175 r2 addendum:** board-guard denied `git branch` for reviewers"
}
````

### User / tool · 2026-11-03T01:42:53.280Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_guard_blocks_shell_expansions.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:58.479Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_doc_rows_patterns.md",
 "content": "---\nname: t207-doc-rows-patterns\ndescription: T-207 (LLM_VS_CODE rows 2-3 vs service_date.py): table \"only\" claims vs extra code resolvers, untested five-year bound, validation-cell mutant count, counted-line note suppression\nmetadata:\n  type: project\n---\n\nDoc-row reviews of a date rule find the same kinds of gap: the table says \"only\" and the code does a little more. Found at fc37fbc (r1, 2026-11-02): (1) a same-period locale rule resolves a two-reading date that row 2 says only the statement rule decides, and a test pins it; (2) the \"more than five years before\" bound is 366*5 days, so 5y+1d to 5y+4d are printed, and no test sits between the 1998 and 2031 fixtures; (3) a visit note's header date becomes the date of service for a charge with no labeled date (spec R-TL-3 backs it, the table does not say so); (4) a counted undated charge (D-064) has its Step 3 note suppressed by a flag, and no test pins the note; (5) a validation cell claims \"24 mutants all fail\" with no harness in the repo, and two resolver mutants survive.\n\n**Why:** the table is the binding description of what decides a printed date, and each gap is a place where an adjuster sees a date the table says is not decided that way. The mutant count is a claim the reviewer can refute.\n\n**How to apply:** when a row says \"only\" or \"never\", list every code path that prints the value (grep the field: dos_iso, dos_text, date_iso) and compare each to the sentence. For any \"more than N\" bound, probe N-1 day, N, N+1 day and the window in between. For any flag that suppresses a note (counted, undated, pos None), probe it and mutate the flag. For a validation cell that gives a mutant count, grep tests/ and evals/ for a harness before accepting the number; if none, run your own mutants on a scratch copy of the pinned archive. Also check the model id: the dossier says claude-sonnet-5-5, but the review ran as claude-haiku-5-5, so record the id actually running.\n\nRelated: [[feedback_guard_blocks_shell_expansions]], [[feedback_mutant_apply_verify]], [[feedback_review_write_once]], [[feedback_severity_vs_brief]].\n"
}
````

### User / tool · 2026-11-03T01:42:58.580Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_doc_rows_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:42:59.958Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 150
}
````

### User / tool · 2026-11-03T01:42:59.967Z

**tool result**
````
<system-reminder>Warning: the file exists but is shorter than the provided offset (150). The file has 125 lines.</system-reminder>
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:43:01.447Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 120
}
````

### User / tool · 2026-11-03T01:43:01.456Z

**tool result**
````
120	- [T-202 r2 patterns](project_t202_r2_patterns.md) — closed negative lists default-allow (headings, lead words); 16/17 mutants killed
121	- [T-201 e2e test-edit patterns](project_t201_e2e_test_edit_patterns.md) — letter AI ban literal-only, XOR provenance assert, AC count 547 vs 553
122	- [T-204 prepared-wording patterns](project_t204_prepared_wording_patterns.md) — universal "no AI wording" AC vs closed node list; rail/judges constants; stale-tree index
123	- [T-208 letter AI-wording patterns](project_t208_letter_ai_wording_patterns.md) — allow-list exempts label on any line, eval blind to FIXTURE_SET, LLM/GPT gap, e2e 10 of 25
124	- [T-202 r3 patterns](project_t202_r3_patterns.md) — bill side allow-list holds; non-bill record-date fallback default-allow; check mutant survivors
125	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:43:03.970Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && ls project_t202_r3_patterns.md project_t207_doc_rows_patterns.md 2>&1; sed -n '1,12p' project_t202_r3_patterns.md | cut -c1-220",
 "description": "Check the existing T-202 r3 memory note this review overlaps with"
}
````

### User / tool · 2026-11-03T01:43:04.059Z

**tool result**
````
project_t202_r3_patterns.md
project_t207_doc_rows_patterns.md
---
name: project_t202_r3_patterns
description: T-202 r3 (973b542): bill side is a true allow-list, non-bill record-date fallback still default-allow via closed bill detector; 4 survivors outside author's mutant set
metadata:
  type: project
---

T-202 r3 verdict changes (1 major, 2 minor, 1 nit). All r2 leaks (Entry/Transaction/Issued/Printed headings, DOI/DOB/authorization, 1998/2031, all->any) now print the fillable blank; unit 6127 passed/6 skipped, guided e2

- Non-bill records (`amounts.billing_document` closed list: lexicon + _BILLISH + _BILL_OPEN) keep the record header date as DOS (`service_date.py` last `if date_iso`, `store.charge_service_date` rec-is-None branch). Sour
- The sample's "Central ER discharge summary" charge needs the non-bill carve-out; the fix is to invert (positive encounter words), not remove.
- Author's 24 mutants all die; mine that survived: bare `\bdate` as service label (sentence forms "Entry date:" untested), check branch for labeled-doubtful printed, underscore count, labeled period end dropped in the ch
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:43:09.218Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_doc_rows_patterns.md",
 "old_string": "Related: [[feedback_guard_blocks_shell_expansions]]",
 "new_string": "Recurrence: item (3) was already flagged as a default-allow non-bill fallback in the T-202 r3 review ([[project_t202_r3_patterns]]). At fc37fbc the code is unchanged and the table still omits it, so it is a documentation gap that has been open since then. The T-202 r3 note says the author's 24 mutants were run outside the repo; that count is still not reproducible from the repo.\n\nRelated: [[feedback_guard_blocks_shell_expansions]]"
}
````

### User / tool · 2026-11-03T01:43:09.346Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_doc_rows_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:43:11.367Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-202 r3 patterns](project_t202_r3_patterns.md) — bill side allow-list holds; non-bill record-date fallback default-allow; check mutant survivors\n",
 "new_string": "- [T-202 r3 patterns](project_t202_r3_patterns.md) — bill side allow-list holds; non-bill record-date fallback default-allow; check mutant survivors\n- [T-207 doc-rows patterns](project_t207_doc_rows_patterns.md) — \"only\" rows vs extra resolvers, 5-year bound untested, mutant-count claim, counted-note suppression\n"
}
````

### User / tool · 2026-11-03T01:43:11.465Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T01:43:14.353Z

T-207 verdict: changes (0 blockers, 5 majors: same-period locale rule, five-year bound, visit-note date default, counted-line note, overstated mutant count), recorded at /Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer.md under model claude-haiku-5-5 (the id I am actually running as, not the expected sonnet id).
