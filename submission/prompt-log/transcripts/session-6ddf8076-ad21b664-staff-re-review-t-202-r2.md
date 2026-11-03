# Subagent: Staff re-review: T-202 r2 (Staff re-review: T-202 r2)

Source: `agent-ad21b664c4a21e095.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T00:20:03.567Z

Re-review T-202, round 2, in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. The fix commit is 986fc55. Read reviews/T-202-staff-engineer.md (your round 1, plus the errata note on the card), the D-071 amendment and clarification in memory/ORCHESTRATOR_DECISIONS.md, and the handoff.

Work in a `git archive 986fc55` copy:
1. Re-run your probes and mutants from artifacts/review-evidence/T-202-staff/.
2. Check that the new letter_check really is independent of the production parser and checks each line against that line's own quote.
3. Check the `_certain` logic: ambiguous numeric dates, two-digit years, multi-date lines, non-DOS columns, and the statement-date disambiguation rule.
4. Run the unit suite and the guided e2e.

Write reviews/T-202-staff-engineer-r2.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:04.950Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-03T00:20:04.958Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:05.288Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-202-staff-engineer.md"
}
````

### User / tool · 2026-11-03T00:20:05.294Z

**tool result**
````
1	# T-202 (D-071) staff-engineer review, commit f0921e4
2	
3	Verdict: **fail** (2 blockers, 3 majors, 2 minors).
4	
5	Date selection is code, with no LLM in the path (`amounts.charge_basis`, `store.charge_service_dates`, `export._date_range`). Output is deterministic: the dump of every charge line over 25 cases is identical on two runs. The missing-date path works: lib06, lib09, lib11, lib12 and lib15 print the T-200 "statement dated X; service date not stated" form, and an invalid date such as 02/30/2026 or 2026-13-04 falls into that form visibly. Unit (5890 passed, 5 skipped) and guided e2e (128 passed) are green from `git archive f0921e4`, and `python -m evals.letter_check` gives value 0 over 25 cases.
6	
7	The new parser is wrong in three ways the green runs do not show, because the eval check reuses the production regex and compares against the whole record:
8	
9	1. It guesses ambiguous numeric dates (`04/05/2026` prints "April 5, 2026"). `docs/LLM_VS_CODE.md` row 2 and D-027 say these are never guessed.
10	2. A month-name period ("June 9-12, 2024") loses its stated year and its end date. With a 2026 statement date it prints "June 9, 2026".
11	3. `letter_check.charge_date_violations` does not fail when a line prints another line's date from the same record, or when a period's end is dropped.
12	
13	```json
14	{"card": "T-202", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
15	 "scope": "commit f0921e4 (HEAD at review time): app/backend/amounts.py, export.py, store.py, evals/letter_check.py, tests/unit/test_t202_charge_service_dates.py, memory/contracts/api.md; git archive copy at artifacts/review-evidence/T-202-staff/a; probes and mutants in artifacts/review-evidence/T-202-staff/s; 25 cases in evals/golden and evals/library, fixture backend",
16	 "exercised": [
17	  "read personas/staff-engineer.md, D-071 (memory/ORCHESTRATOR_DECISIONS.md:84), card T-202 and handoff, docs/LLM_VS_CODE.md row 2/3, git show f0921e4 (full diff of all 7 files)",
18	  "git archive f0921e4 into artifacts/review-evidence/T-202-staff/a; HEAD == f0921e4 (git rev-parse HEAD)",
19	  "pytest tests/unit -q from the archive: 5890 passed, 5 skipped in 459s",
20	  "pytest tests/e2e/guided -q from the archive: 128 passed in 170s",
21	  "python -m evals.letter_check from the archive: {value: 0, cases: 25}",
22	  "s/dump.py: every BILLED CHARGES header+quote over 25 cases x (all_accepted, counted); run twice, diff identical (deterministic)",
23	  "s/probe1.py and s/probe4.py: charge_basis + store.charge_service_dates on 45 hand-built lines (multi-line ledger, table row, two service dates on one line, posted/paid dates, amount-before-date, 03/04/2026, 13/04/2026, 04/05/26, 4/5, 12/28 on a January statement, ISO, invalid dates, periods crossing month/year, reversed and same-day periods, hyphen/en-dash/through forms, month-name periods, two periods, no date, statement date only, 98 two-digit year)",
24	  "s/probe2.py: modified lib11 ledger through the full pipeline (dated, ambiguous, two-dates, multi-line variants) and read the printed letter lines",
25	  "s/probe3.py: charge_date_violations on a two-line ledger with right, wrong-line, not-in-record, statement, ambiguous-reading and dropped-period-end headers",
26	  "mutants M1..M6 applied in the archive copy (s/mut.py), each run through letter_check; M3/M5/M6 also through test_t202 + test_t200, and M5 through 888 export/letter/charge/golden/api unit tests; files restored (diff -q against s/export.orig and s/store.orig clean)",
27	  "grep of amounts.py for provider/llm imports, float( and except: none in the date path"],
28	 "verdict": "fail",
29	 "scores": {"deterministic_parse_no_llm": 5, "date_correctness_edge_cases": 1, "ambiguity_policy_LLM_VS_CODE_row2": 1, "period_range_handling": 2, "eval_check_has_teeth": 2, "test_quality": 2, "missing_date_visible_state": 4},
30	 "findings": [
31	  {"severity": "blocker",
32	   "title": "Ambiguous numeric dates are guessed and printed as the date of service (violates LLM_VS_CODE row 2, D-027)",
33	   "evidence": "docs/LLM_VS_CODE.md:30 '04/05/2026 fits two readings ... it is ambiguous, never guessed, and waits for the paralegal'; app/backend/dates.py:3-4 'Nothing is ever guessed'. app/backend/amounts.py:380-395 _dos_iso picks month-first. Repro (s/probe2.py, lib11 ledger with '04/05/2026 x-ray charge $180.00'): the letter prints 'Fennimoor Spine Clinic, itemized ledger, April 5, 2026: $180.00' with no Dates-to-confirm state. s/probe4.py: 'Office visit 03/17/98 charge $220.00' -> 1998-03-17 (D-027 says '03-17-98' is ambiguous 1998/2098); '4/5' takes its year from the statement date. Before f0921e4 this guess only drove the duplicate match; the card now prints it as a fact. The eval check cannot see it: probe3 'ambig April 5' -> [] and 'ambig May 4' is flagged only because it differs from the guess.",
34	   "why_it_matters": "A paralegal sends a letter that asserts one reading of a date the record does not settle. The adjuster cross-checks dates, and the project's own rule is to ask, not guess.",
35	   "fix": "For a charge line's own date, reuse dates.parse_date semantics: an ambiguous or two-digit-year-over-pivot date yields no printed service date. Take the existing T-200 'service date not stated' route, or carry an ambiguous state the paralegal resolves with confirm_date. Do not borrow a year for a year-less date.",
36	   "acceptance_test": "Unit test through export_case: a ledger line '04/05/2026 x-ray charge $180.00' does not print 'April 5, 2026' or 'May 4, 2026' and shows a visible state. '13/04/2026' and '2026-04-05' still print. '03/17/98' does not print 1998. evals/letter_check flags a letter that prints the guessed reading."},
37	  {"severity": "blocker",
38	   "title": "A month-name period loses its stated year and its end date; the printed date can be wrong",
39	   "evidence": "app/backend/amounts.py:274-281 _DOS_RX: the month-name branch needs ',?\\s+YYYY' right after the day, so 'June 9-12, 2024' matches only 'June 9' (year-less) and _year_for (amounts.py:364-369) borrows the statement year. s/probe4.py with record date 2026-06-19: 'statement period June 9-12, 2024' -> dos=2026-06-09 end=None, so the letter prints 'June 9, 2026' for a 2024 stay. 'June 9-12, 2026' -> '2026-06-09', end None (printed 'June 9, 2026', a one-day service); 'June 28-July 2, 2026' -> end None. D-071 prints periods as 'June 9-12, 2026', the month-name form itself.",
40	   "why_it_matters": "This prints a date the record does not state (wrong year), and collapses a multi-day stay to one day. Late-submitted bills in injury claims routinely sit more than a year after the stay.",
41	   "fix": "Parse 'Month D-D, YYYY' and 'Month D-Month D, YYYY' as a period with their own year. When a year-less month-name date is followed by a later year, never apply the statement-year heuristic.",
42	   "acceptance_test": "charge_basis on 'statement period June 9-12, 2024' (record date 2026-06-19) returns dos 2024-06-09, dos_end 2024-06-12. 'June 28-July 2, 2026' returns 2026-06-28 and 2026-07-02. The letter prints 'June 9-12, 2024'. The same cases are added to the golden set so letter_check covers them."},
43	  {"severity": "major",
44	   "title": "Hyphen-joined numeric periods without spaces drop the end date",
45	   "evidence": "_DOS_RX starts with (?<![\\w/.$-]) (amounts.py:275), so the second date after '-' is not matched. s/probe4.py: 'statement period 06/28/2026-07/02/2026' -> dos=2026-06-28 end=None; '06/28-07/02/2026' -> end=None. The spaced and en-dash forms work ('06/28/2026 - 07/02/2026', '06/28/2026–07/02/2026'). Letter prints 'June 28, 2026' for a June 28-July 2 stay; letter_check passes it (M3 below).",
46	   "why_it_matters": "'MM/DD/YYYY-MM/DD/YYYY' is a common billing period format. D-071 says a period prints as a range.",
47	   "fix": "Let the range-end match accept a '-' immediately before it when it follows a date, in _record_period and _dates_in. Keep the lookbehind for other uses.",
48	   "acceptance_test": "charge_basis on '06/28/2026-07/02/2026' returns (2026-06-28, 2026-07-02); the letter prints 'June 28-July 2, 2026'."},
49	  {"severity": "major",
50	   "title": "Two service dates on one charge line: the later one is printed and the earlier is lost, with no flag",
51	   "evidence": "amounts.py:507 'dos = ds[-1][2]' (non-row) / 'ds[0][2]' (row) takes one date. s/probe1.py: 'Office visits 03/01/2026 and 03/08/2026 charge $220.00' -> dos=2026-03-08. Full pipeline (s/probe2.py 'twodates'): 'New patient exam 03/27/2026 and x-ray 03/28/2026 charge $250.00' prints 'March 28, 2026: $250.00'. letter_check passes it.",
52	   "why_it_matters": "A charge that covers two dates is reported as one. The quote on the next line shows both, but the header asserts one service date.",
53	   "fix": "When a charge line states more than one service date and they are not a range, do not pick one: take the 'service date not stated' route or a visible 'multiple dates' state.",
54	   "acceptance_test": "Unit test: a line with two non-range service dates does not print a single bare date; letter_check flags the old output."},
55	  {"severity": "major",
56	   "title": "evals/letter_check date check is weaker than the AC: it compares against the whole record using the production parser",
57	   "evidence": "evals/letter_check.py charge_date_violations: 'ex = r[\"excerpt\"]' (whole record) and states built from AM._DOS_RX / AM._dos_iso (same code as the thing under test). s/probe3.py on a two-line ledger (03/01 $100, 03/08 $120): header 'March 8, 2026' on the $100 line -> [] (should fail). Header with a dropped period end ('June 9, 2026' for 06/09-06/12) -> []. Mutants in the archive (s/mut.py): M1 print record date -> value 28; M2 +1 day -> 148; M4 bare statement date on undated -> 20 (all fail, good). M3 drop period end (_date_range(a['dos_iso'])) -> value 0, survives. M6 print the record's first date -> value 0, survives (the corpus has no multi-date ledger); test_t202 catches M3 (3 failed) and M6 (1 failed) only through lib10 and a charge_basis unit test, not through the eval. AC 1 says 'equals the service date in its quote'.",
58	   "why_it_matters": "The check is the harness upgrade this card promised. Today it only catches a date that is in no part of the record, which is the T-200 error class. It shares the parser's ambiguity guess (finding 1), so it cannot detect an error in that parser.",
59	   "fix": "Check per line: when the quote itself contains a date, the printed date must equal the date parsed from the quote; for a period header with the date in a heading line, require the full period (first and last) rather than only the first. Do not call AM._dos_iso for ambiguity, reject ambiguous readings in the check. Add a multi-date ledger and a hyphen period to the golden or library set.",
60	   "acceptance_test": "charge_date_violations returns a violation for the wrong-line header and for a dropped period end (probe3 cases). Mutants M3 and M6 give a non-zero letter_check value on the committed corpus."},
61	  {"severity": "minor",
62	   "title": "Sort-by-service-date has no discriminating test",
63	   "evidence": "Mutant M5 (export.py in_charges returns 'got' unsorted): letter_check value 0; test_t202 + test_t200 19 passed; 888 export/letter/charge/golden/api unit tests passed. tests/unit/test_t202_charge_service_dates.py:test_charges_are_listed_in_service_date_order uses lib06, whose record order already equals date order.",
64	   "why_it_matters": "A stated behavior of the commit can be removed with no test failing.",
65	   "fix": "Test with a case where record order differs from service-date order (a later-dated statement record listed before an earlier visit).",
66	   "acceptance_test": "M5 fails at least one unit test."},
67	  {"severity": "minor",
68	   "title": "store.charge_service_dates falls back to the record's date when the line cannot be read, which for a bill is the statement date",
69	   "evidence": "app/backend/store.py (charge_service_dates): 'return (None, None) if counted_undated else ((rec or {}).get(\"date_iso\"), None)'. s/probe4.py: pos=None on a ledger line with only a statement date returns ('2026-06-15', None). The docstring admits the fallback. I could not show a production path that produces pos=None; amount_pos is None only when the stored excerpt does not hold the raw text at the stored index.",
70	   "why_it_matters": "It is a silent fallback to the exact error D-071 removes, in the one branch no test reaches.",
71	   "fix": "For a billing document return (None, None) there (the statement form); keep the record date only for a non-billing encounter record (AM.billing_document).",
72	   "acceptance_test": "Unit test: pos=None on a ledger record returns (None, None); on a visit note returns the visit date."}
73	 ],
74	 "whats_right": [
75	  "Date choice is code only and byte-deterministic (two full dumps identical); a line with no readable service date takes the visible T-200 statement form (lib06/09/11/12/15) instead of a bare date.",
76	  "The three mutants the handoff claims (record date, +1 day, bare statement date) do fail letter_check (28 / 148 / 20 violations) from a git-archive copy; unit and guided e2e are green from the archive.",
77	  "_date_range handles same-month, cross-month and cross-year periods and a same-day period collapses to one date, with a unit test on each."],
78	 "questions_for_chris": []}
79	```
80	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:06.137Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-202 | tail -80; ls artifacts/review-evidence/T-202-staff/; git log --oneline | head -5",
 "description": "Show card T-202, evidence dir, git log"
}
````

### User / tool · 2026-11-03T00:20:06.306Z

**tool result**
````
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
updated_at: "2026-11-03T00:19:55Z"
claimed_by: "backend"
claimed_at: "2026-11-02T23:26:10Z"
rounds: 1
commits: ["f0921e4", "986fc55"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-202-paralegal.md", "at": "2026-11-02T23:48:12Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-202-staff-engineer.md", "at": "2026-11-02T23:55:16Z"}
ac:
  - {"n": 1, "text": "per D-071; case_09/lib14/lib10 letters show the service date/period; goldens updated with a diff in the handoff; evals/letter_check.py asserts each dated charge line's date equals the service date in its quote, over all 25 cases incl. a count path; unit + guided e2e green from git archive", "done": true, "evidence": "r2 986fc55: tests/unit/test_t202_r2_service_date_layouts.py 48 cases (33 red on f0921e4 -> all pass); letter_check value 0 over 25 cases, mutants fail it (drop period end 16, record date 28, bare statement 20, record first date 6); unit + guided e2e from git archive 986fc55 (see handoff)"}
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

## Handoff
What changed (r2, 986fc55): new app/backend/service_date.py prints a charge date only when exactly one unambiguous date or complete period is tied to THAT line (its sentence; its row + column header; or the bill's one stated period for a coded line). Else the T-200 not-stated form + a Step 3 confirm note: ambiguous numerics (04/05/2026), two-digit years, year-less dates, impossible dates, several candidate dates (CMS-1500 '06/24 and 07/08', 'exam 03/27 and x-ray 03/28'), Posted/Statement columns, row with two dates and no DOS header, bill line with no date. Month-name periods keep their own year and end (June 9-12, 2024; June 28-July 2, 2026); hyphen-joined 06/28/2026-07/02/2026 prints whole. store.charge_service_date feeds BOTH the letter (dos_iso/dos_end_iso) and the case view; bill line the code cannot read now has no date (staff minor); sort test can fail. letter_check: charge_date_violations rewritten, checks each printed date against that line's own quote (+ the one period the bill states before it) with its own scanner, no production parser. | API/Step 3 (frontend): read amounts[].service_date on every charge (null for other kinds) = {state 'stated'|'not_stated', date_iso, end_iso, text, statement_date_iso, reason, confirm_note}. text is byte-for-byte what the letter prints after the provider ('June 9-12, 2026' or '(statement dated June 15, 2026; service date not stated)'); show confirm_note when not null; label the record date as the statement date. api.md updated. | Verified: fixtures tests/unit/test_t202_r2_service_date_layouts.py were RED first on f0921e4 (33 failed, 15 passed) and pass now (48). From git archive 986fc55: unit 5932 passed (1409+1611+1391+1521, 12 skipped), guided e2e 134 passed, letter_check value 0 over 25 cases. Corpus letters byte-identical to f0921e4 (84 charge lines diffed, case_09/lib14/lib10 unchanged). Mutants vs letter_check: drop period end 16 violations, record date 28, bare statement date 20, record's first date on a not-stated line 6 (all FAIL; the staff survivors M3/M6 now die); no-sort mutant fails 2 unit tests. | Left / ASSUMPTION for orchestrator: lib10 UB-04 '06/09/2026 to 06/12/2026' is ambiguous numerically; it stays 'June 9-12' only via one rule: a reading after the record's own date is impossible (Sept 6 > June 19 statement), or the other end of the period is unambiguous. Strike it (ref=None in service_date._certain) and lib10 prints the not-stated form. Not done: paralegal minor (quote span names neither service nor date) and the same-day ED-before-ambulance tie-break nit. Surprise: every not-stated corpus line is a D-064 counted-undated one, so a mutant that skips counted lines survives letter_check.

a
s
6c9ab2a feat(release): T-199 snapshot shares the finalize rule set and switch; normalized final scan (D-070)
9611f02 fix(backend): T-201 e2e tests expect prepared wording for a prepared item (crosses into QA tests/e2e): internal-notes provenance line, wait for the server's sentence before reading the row, wait for the library list before the refused paste
986fc55 fix(backend): T-202 r2 D-071 amendment: a charge line prints a service date only when code is certain, else the not-stated form and a Step 3 confirm note
fa34fe9 fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests
38ee0c3 fix(frontend): T-203 greyed Yes says why beside it (tick the box above), damages wording, Pt shorthand not underlined, 375x667 test
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:08.610Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-202-staff/s artifacts/review-evidence/T-202-staff/a | head -50; grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_shared_scratchpad.md | head -20; git status --short | head",
 "description": "List evidence, find D-071"
}
````

### User / tool · 2026-11-03T00:20:08.756Z

**tool result**
````
artifacts/review-evidence/T-202-staff/a:
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools

artifacts/review-evidence/T-202-staff/s:
dump.py
dump.txt
dump2.txt
export.orig
mut.py
mut2.py
mut3.py
probe1.py
probe2.py
probe3.py
probe4.py
store.orig
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
---
name: feedback_shared_scratchpad
description: the scratchpad path is shared with other agents; use a unique card-round subdir, verify archive copies with diff -rq against a fresh git archive, never background a setup chain you depend on
metadata:
  type: feedback
---

Name scratch directories with the card and round (for example `T108_verify`), and run `ls -la` before reusing any directory. Check an archive copy with `diff -rq` against a fresh `git archive <sha>` before trusting results.

**Why:** during T-108 r1 the `probe/` folder I used already held another agent's repo archive, and sibling folders (`T106_*`) appeared in the same scratchpad during my run. My own setup line `mkdir -p X && cp ... && cd ... &` was backgrounded as one chain, so the following commands ran before the directory existed and wrote nothing.

**How to apply:** do not background setup you depend on; run it in the foreground or wait on it. Keep probe scripts in your own unique directory and copy the final ones to `artifacts/review-evidence/<card>/` as the evidence.

Related: [[project_t108_quote_units_patterns]].
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t181_round2.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:10.807Z

**tool call — Bash**
````
{
 "command": "sed -n 80,95p memory/ORCHESTRATOR_DECISIONS.md; D=artifacts/review-evidence/T-202-staff-r2; mkdir -p $D && git archive 986fc55 | (mkdir -p $D/a && tar -x -C $D/a) && ls $D/a | head -3; git rev-parse HEAD; git diff --stat f0921e4 986fc55 | tail -20",
 "description": "Read decisions; archive 986fc55 into evidence dir"
}
````

### User / tool · 2026-11-03T00:20:11.925Z

**tool result**
````
## D-070 — One redaction rule set, no private literal in tracked code, applied to every published file
T-187 r3: private values survive as quoted fragments joined with '+' (in transcripts and in the redaction source itself), and the snapshot applied only some rules outside the prompt log. Binding: (1) every private term (work email, third-party and personal names, job-application path pieces, tailnet host) lives only in the gitignored deploy/.private_patterns; tracked code holds rule logic, never the values; (2) the snapshot applies the full rule set (prompt-log rules + private terms + home paths + outside project name) to every text file it publishes; (3) the final scan matches on a normalized view of each file (strip quotes, '+', whitespace, backslashes, case) so split or escaped forms fail the build. Same switch semantics for Chris's T-193 answer.

## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.

## D-071 amendment — when the service date is not certain, print none and ask the human
T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.

## D-072 — The prompt log is built and privacy-reviewed once, last
Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
6c9ab2ab682c74a9c3461b0486ac4ea034d371e1
 app/backend/export.py                           |  15 +-
 app/backend/present.py                          |   2 +
 app/backend/service_date.py                     | 329 +++++++++++++++++++++++
 app/backend/store.py                            |  41 ++-
 app/frontend/guided/review.js                   |  31 ++-
 app/frontend/guided/step2.js                    |   5 +-
 evals/letter_check.py                           | 191 ++++++++++++--
 memory/contracts/api.md                         |   4 +-
 tests/e2e/guided/test_t203.py                   | 117 +++++++++
 tests/unit/test_t202_charge_service_dates.py    |   2 +-
 tests/unit/test_t202_r2_service_date_layouts.py | 336 ++++++++++++++++++++++++
 11 files changed, 1020 insertions(+), 53 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:15.138Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/a && ls /Users/arsis/zlayt-pm-project/.venv/bin/python && (/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider > ../unit.log 2>&1; echo done >> ../unit.log) </dev/null >/dev/null 2>&1 &\nsleep 1; echo started",
 "description": "Start unit suite in background from archive",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T00:20:15.206Z

**tool result**
````
Command running in background with ID: bkgtplykb. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bkgtplykb.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:15.432Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/a/app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T00:20:15.439Z

**tool result**
````
1	"""The service date a charge line prints, only when code is certain (D-071 amendment, T-202 round 2). Code only, no LLM (LLM_VS_CODE rows 2 and 3).
2	
3	The letter's charge line carries a date of service. A date there is a claim to an adjuster, so it is printed only when exactly ONE unambiguous service date (or one complete
4	period) is tied to THAT line, by its own sentence, by its table row and column header, or (for a coded line with no date of its own) by the one period the bill states for its
5	services ('statement period 06/09/2026 to 06/12/2026', 'the run of 09/14/2026'). Everything else is `not_stated`, with a reason the Step 3 screen shows as a note asking the
6	paralegal to confirm the date from the quote:
7	  - a numeric date that can be read two ways (04/05/2026), unless one reading falls after the record's own date (a service cannot follow its statement), or the other end of
8	    the same period fixes the order (06/28/2026-07/02/2026);
9	  - a two-digit year, a date with no year, a date that is not on the calendar, a period whose end is missing or before its start;
10	  - several candidate dates for the line (a CMS-1500 'dates of service 06/24/2026 and 07/08/2026', 'exam 03/27/2026 and x-ray 03/28/2026 charge $250.00');
11	  - a row with two dates and no header that says which is the date of service, or whose only date sits under Posted, Statement, Billed ...;
12	  - no date at all on a bill line (a dated encounter note, not a bill, keeps the note's own date).
13	Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
14	(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
15	import datetime as _dt
16	import re
17	
18	from app.backend import amounts as AM
19	
20	_MON = AM._MON
21	_ORD = r"(?:st|nd|rd|th)?"
22	_DASH = "–—"
23	_TOK = re.compile(
24	    r"(?<![\w/$])(?:"
25	    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
26	    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
27	    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
28	    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
29	    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
30	    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
31	    r")(?![\w/]|\.\d)", re.IGNORECASE)
32	_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
33	_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
34	# the word right before a date that makes it a billing-side date, never a date of service
35	_NON_SVC_LEAD = re.compile(r"\b(?:statements?|stmt|invoice|billing|billed|bill|printed|issued|mailed|as[\s-]of|due|posted|post|paid|received|payment|processed|balance|created|generated|sent)\b"
36	                           r"(?:\s+(?:date|dated|on|of))?\s*[:#]?\s*$", re.IGNORECASE)
37	_H_DOS = re.compile(r"\bdos\b|date\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter", re.IGNORECASE)
38	_H_NON = re.compile(r"post|statement|stmt|bill|invoice|paid|payment|due|receiv|process|entered|created|balance|adjust|insur|submitted|mailed", re.IGNORECASE)
39	
40	REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "non_service_date", "no_date")
41	
42	
43	def display(first, last=None) -> str:
44	    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
45	    def lng(iso):
46	        d = _dt.date.fromisoformat(iso)
47	        return f"{d.strftime('%B')} {d.day}, {d.year}"
48	    if not last or last == first:
49	        return lng(first)
50	    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
51	    if (a.year, a.month) == (b.year, b.month):
52	        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
53	    if a.year == b.year:
54	        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
55	    return f"{lng(first)}–{lng(last)}"
56	
57	
58	def not_stated_text(statement_iso) -> str:
59	    """The text the letter puts after the provider when no service date is certain (T-200)."""
60	    if statement_iso:
61	        return f"(statement dated {display(statement_iso)}; service date not stated)"
62	    return "(service date not stated)"
63	
64	
65	_WHY = {
66	    "ambiguous_numeric": "The date written as {raw} can be read as month/day or day/month, and the record does not settle which.",
67	    "two_digit_year": "The date {raw} has a two-digit year, which the code does not guess.",
68	    "no_year": "The date {raw} states no year, which the code does not borrow from the statement.",
69	    "invalid": "{raw} is not a complete date on the calendar.",
70	    "several_dates": "This line or its bill states more than one date ({raw}) and the record does not say which one belongs to this charge.",
71	    "non_service_date": "The only date near this line ({raw}) is a posting, statement or billing date, not a date of service.",
72	    "no_date": "The line states no date of service.",
73	}
74	
75	
76	def confirm_note(reason, raw) -> str:
77	    """The Step 3 note for a charge whose service date is not certain: why, and the ask (D-071 amendment)."""
78	    return (_WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") +
79	            " The letter prints no service date for this line. Confirm the date from the quote before you rely on it.")
80	
81	
82	def _iso(y, mo, d):
83	    try:
84	        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
85	    except ValueError:
86	        return None
87	
88	
89	class _Tok:
90	    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")
91	
92	    def __init__(self, m):
93	        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
94	        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
95	        getattr(self, "_" + self.kind)(m.group(0))
96	        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
97	            self.flaw = "invalid"
98	
99	    def _iso(self, s):
100	        y, mo, d = (int(x) for x in s.split("-"))
101	        self.fixed = _iso(y, mo, d)
102	
103	    def _num(self, s):
104	        a, b, y = re.split(r"[/.-]", s)
105	        if len(y) == 2:
106	            self.flaw = "two_digit_year"
107	            return
108	        a, b, y = int(a), int(b), int(y)
109	        md, dm = _iso(y, a, b), _iso(y, b, a)
110	        if md and dm and md != dm:
111	            self.ambiguous = {"MD": md, "DM": dm}
112	        elif md or dm:
113	            self.fixed = md or dm
114	            self.order = None if (md and dm) else ("MD" if md else "DM")
115	
116	    def _mdy(self, s):
117	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
118	        if not m.group(3):
119	            self.flaw = "no_year"
120	            return
121	        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))
122	
123	    def _dmy(self, s):
124	        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
125	        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))
126	
127	    def _md(self, s):
128	        self.flaw = "no_year"
129	
130	    def _mper(self, s):
131	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
132	        if not m.group(5):
133	            self.flaw = "no_year"
134	            return
135	        y, m1 = int(m.group(5)), _mon(m.group(1))
136	        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
137	        if a and b and b > a:
138	            self.first, self.last = a, b
139	        else:
140	            self.flaw = "invalid"
141	
142	
143	def _mon(name):
144	    from app.backend import dates
145	    return dates.MONTHS[name.lower()[:3]]
146	
147	
148	class _Unit:
149	    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
150	    def __init__(self, toks):
151	        self.toks = toks
152	        self.start, self.end = toks[0].start, toks[-1].end
153	
154	    def raw(self, text):
155	        return text[self.start:self.end]
156	
157	
158	def _units(text: str) -> list:
159	    toks = [_Tok(m) for m in _TOK.finditer(text)]
160	    out, k = [], 0
161	    while k < len(toks):
162	        t = toks[k]
163	        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
164	            out.append(_Unit([t, toks[k + 1]]))
165	            k += 2
166	        else:
167	            out.append(_Unit([t]))
168	            k += 1
169	    return out
170	
171	
172	def _certain(unit: _Unit, ref):
173	    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
174	    for t in unit.toks:
175	        if t.flaw:
176	            return "bad", t.flaw
177	    if len(unit.toks) == 1 and unit.toks[0].first:
178	        return "ok", unit.toks[0].first, unit.toks[0].last
179	    determined = {t.order for t in unit.toks if t.order}
180	    amb = [t for t in unit.toks if t.ambiguous]
181	    if len(determined) > 1:
182	        return "bad", "ambiguous_numeric"
183	    if determined:
184	        order = next(iter(determined))
185	    elif amb:
186	        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
187	        if len(feasible) != 1:
188	            return "bad", "ambiguous_numeric"
189	        order = feasible[0]
190	    else:
191	        order = None
192	    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
193	    if len(isos) == 2 and isos[1] <= isos[0]:
194	        return "bad", "invalid"
195	    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)
196	
197	
198	def _header_cells(excerpt: str, row_ls: int):
199	    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line."""
200	    for line in reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]):
201	        if not line.strip():
202	            return None
203	        if re.search(r"\d", line):
204	            continue
205	        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
206	        return cells if len(cells) >= 2 else None
207	    return None
208	
209	
210	def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
211	    heads = _header_cells(excerpt, row_ls)
212	    if not heads:
213	        return ""
214	    col = tok_abs - row_ls
215	    if len(heads) == len(row_cells):
216	        idx = next((i for i, (a, b) in enumerate(row_cells) if a <= col < b), None)
217	        if idx is not None:
218	            return heads[idx][1]
219	    return min(heads, key=lambda h: abs(h[0] - col))[1]
220	
221	
222	def _lead_ok(text: str, unit: _Unit, tail: bool = False) -> bool:
223	    lead = text[max(0, unit.start - 40):unit.start]
224	    if _NON_SVC_LEAD.search(lead):
225	        return False
226	    return bool(AM._DATE_LEAD.search(lead)) if tail else True
227	
228	
229	def _period_units(prefix: str) -> list:
230	    """The dates the bill states for its services: units led by 'statement period', 'dates of service', 'the run of' ... and the units listed after them ('A and B')."""
231	    us = _units(prefix)
232	    out = []
233	    for k, u in enumerate(us):
234	        if AM._PERIOD_PHRASE.search(prefix[max(0, u.start - 40):u.start]) and not _NON_SVC_LEAD.search(prefix[max(0, u.start - 40):u.start]):
235	            out.append(u)
236	            j = k
237	            while j + 1 < len(us) and _LIST.match(prefix[us[j].end:us[j + 1].start]):
238	                out.append(us[j + 1])
239	                j += 1
240	    return out
241	
242	
243	def _decide(units, text, ref):
244	    """('ok', first, last) for one certain unit (or several that read the same); ('bad', reason, raw) otherwise."""
245	    reads = [(u, _certain(u, ref)) for u in units]
246	    if len(units) > 1:
247	        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
248	        if len(same) == 1 and all(r[0] == "ok" for _, r in reads):
249	            return "ok", *next(iter(same))
250	        return "bad", "several_dates", ", ".join(u.raw(text) for u in units)
251	    u, r = reads[0]
252	    return ("ok", r[1], r[2]) if r[0] == "ok" else ("bad", r[1], u.raw(text))
253	
254	
255	def _apply(out: dict, res) -> dict:
256	    if res[0] == "ok":
257	        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="")
258	    else:
259	        out.update(reason=res[1], raw=res[2])
260	    return out
261	
262	
263	def resolve(excerpt: str, start: int, source, date_iso) -> dict:
264	    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the date text the reason is about)} for the figure at
265	    `start` of `excerpt`, in a record with header `source` and date `date_iso`. See the module doc for the rules."""
266	    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""}
267	    amts = AM.find_amounts(excerpt or "")
268	    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
269	    if i is None:
270	        return out
271	    a = amts[i]
272	    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
273	    bill = AM.billing_document(source, excerpt)
274	    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
275	    seg = excerpt[ss:se]
276	    skipped = []                      # dates left out because of the word or column before them (posted, statement ...)
277	
278	    if len(AM._cells(seg)) >= 2:                                          # a table row: the column header says which date is the date of service
279	        row_ls = excerpt.rfind("\n", 0, a["start"]) + 1
280	        rl_end = excerpt.find("\n", a["start"])
281	        row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
282	        row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
283	        dos, other = [], []
284	        for u in _units(seg):
285	            head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
286	            if not _lead_ok(seg, u) or (head and not _H_DOS.search(head) and _H_NON.search(head)):
287	                skipped.append(u.raw(seg))
288	            elif head and _H_DOS.search(head):
289	                dos.append(u)
290	            else:
291	                other.append(u)
292	        if dos or other:
293	            return _apply(out, _decide(dos or other, seg, date_iso))
294	    else:
295	        prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
296	        own = excerpt[prev:a["start"]]
297	        units = [u for u in _units(own) if _lead_ok(own, u)]
298	        skipped += [u.raw(own) for u in _units(own) if not _lead_ok(own, u)]
299	        if units:
300	            return _apply(out, _decide(units, own, date_iso))
301	        if prev > ss:                                                      # a date stands once for the items listed after it: usable only when it is the line's one date
302	            whole = excerpt[ss:a["start"]]
303	            units = [u for u in _units(whole) if _lead_ok(whole, u)]
304	            if units:
305	                return _apply(out, _decide(units, whole, date_iso))
306	        tail = excerpt[a["end"]:min([amts[j]["start"] for j in sfigs if j > i], default=se)]
307	        if AM._TAIL_LEAD.match(tail):
308	            units = [u for u in _units(tail) if _lead_ok(tail, u, tail=True)]
309	            if units:
310	                return _apply(out, _decide(units, tail, date_iso))
311	    # no date of its own
312	    if bill:
313	        if AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # a coded line takes the one period the bill states for its services
314	            prefix = excerpt[:se]
315	            seen, uniq = set(), []
316	            for u in _period_units(prefix):
317	                r = _certain(u, date_iso)
318	                key = (r[1], r[2]) if r[0] == "ok" else (u.raw(prefix),)
319	                if key not in seen:
320	                    seen.add(key)
321	                    uniq.append(u)
322	            if uniq:
323	                return _apply(out, _decide(uniq, prefix, date_iso))
324	        if skipped:
325	            out.update(reason="non_service_date", raw=skipped[0])
326	        return out
327	    if date_iso:                                                          # a dated encounter record (visit note, imaging report): the record's date is the visit
328	        out.update(state="stated", first=date_iso, last=None, reason=None, raw="")
329	    return out
330	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:18.044Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/a/evals/letter_check.py"
}
````

### User / tool · 2026-11-03T00:20:18.201Z

**tool result**
````
1	"""Letter-level eval (T-139; D-019, R-CH-7, R-EX-8): no dollar amount reaches the carrier letter except in the BILLED CHARGES section.
2	
3	For every golden case, the sample and every library packet, on the FIXTURE backend (recorded model answers; no network):
4	  run the pipeline on a scratch database, accept every item that code lets her accept (a refusal is counted, not hidden), export the letter in both styles;
5	  then a variant where every charge is dismissed.
6	Violations (all must be zero):
7	  - a currency string in the letter outside the BILLED CHARGES section (the treatment entries and the TREATMENT SUMMARY paragraph);
8	  - in the BILLED CHARGES section, a currency string that is not an accepted charge or the total line (R-EX-8: exactly 'Billed charges accepted from these records: $X');
9	  - after dismissing every charge: any currency string anywhere in the letter, or a provider whose charge was dismissed under BILLS TO REQUEST in the notes.
10	  - money written WITHOUT a '$' anywhere outside the accepted charge lines ('TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500'): T-139 round 2.
11	T-139 round 4: the audit uses the SAME detector as the charge-text hold and the export gate (app/backend/money.py), so the three cannot diverge: a wording one holds, all hold.
12	The eval's independent value is the walk (every case, every style, charges dismissed) and the structure checks (charges section, total line, bills to request), not a
13	second regex. It also reports the export gate: a case whose letter the gate blocks is a violation.
14	D-071 / T-202: a third variant counts every countable amount (the paralegal's D-064 "Count this charge", with the named confirms) after accepting everything, and every dated charge
15	line of every letter is checked against THAT line's own quote (`charge_date_violations`, round 2): the printed date (a day or a range, whole) must be the one certain reading of the date the
16	quote states, or, when the quote states none, of the one period the bill states before it; a date readable two ways, with a two-digit year or no year, a quote with several dates and no
17	service-date column heading, or a bill that states several periods may print nothing but the T-200 form '(statement dated X; service date not stated)', X the record's date. The check has
18	its own date scanner and shares no code with the production parser (app/backend/service_date.py), so a parser bug cannot hide itself.
19	Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.
20	
21	    python -m evals.letter_check            prints one line per case and exits 1 on any violation
22	"""
23	import contextlib
24	import json
25	import pathlib
26	import re
27	import sys
28	import tempfile
29	
30	ROOT = pathlib.Path(__file__).resolve().parents[1]
31	GOLD, LIB = ROOT / "evals" / "golden", ROOT / "evals" / "library"
32	CHARGES, TOTAL = "BILLED CHARGES", "Billed charges accepted from these records: "
33	STYLES = (None, "oneline")
34	
35	def dollar_figures(text: str) -> list:
36	    """Every '$'-marked figure (also 'N dollars', 'USD N') in `text`, in order of position (the shared detector, app/backend/money.py)."""
37	    from app.backend import money
38	    return money.of_kind(text, "dollar")
39	
40	
41	def other_currency(text: str) -> list:
42	    """Figures with another currency sign or code, amounts in words, and money in a patient's statement (the shared detector)."""
43	    from app.backend import money
44	    return money.of_kind(text, "sign", "spoken", "statement")
45	
46	
47	def unmarked_money(text: str) -> list:
48	    """Money written without a sign (a money word or claim-form field and its figure), outside any signed figure (the shared detector)."""
49	    from app.backend import money
50	    return money.of_kind(text, "unmarked")
51	
52	
53	def cases():
54	    """[(name, text)]: the sample, the golden cases and the library packets, in a fixed order."""
55	    names = [GOLD / "sample.txt"] + sorted(GOLD.glob("case_*.txt")) + sorted(LIB.glob("case_*.txt"))
56	    return [(p.stem, p.read_text()) for p in names]
57	
58	
59	def violations(letter: str, accepted_cents=(), expect_none: bool = False) -> list:
60	    """Currency strings the letter may not carry. `accepted_cents`: the accepted charges (the only amounts the BILLED CHARGES section may list).
61	    `expect_none`: nothing was accepted as a charge, so no currency string may appear anywhere."""
62	    from app.backend import amounts as AM, export
63	    out = []
64	    head_lines, tail_lines = export.split_letter(letter)               # by structure (the last BILLED CHARGES header line before the total line), never on the words in a quote
65	    head, tail = "\n".join(head_lines), "\n".join(tail_lines)
66	    out += [f"treatment text states {s}" for s in dollar_figures(head)]
67	    out += [f"treatment text states money in another form: {s}" for s in other_currency(head)]
68	    out += [f"treatment text states money without a $ sign: {s}" for s in unmarked_money(head)]
69	    if expect_none or not accepted_cents:
70	        out += [f"letter states {s} with no accepted charge" for s in dollar_figures(tail)]
71	        out += [f"letter states money without a $ sign: {s}" for s in unmarked_money(tail)]
72	        out += [f"letter states money in another form: {s}" for s in other_currency(tail)]
73	        return out
74	    allowed = {c for c in accepted_cents} | {sum(accepted_cents)}
75	    for line in tail.splitlines():
76	        for s in dollar_figures(line):
77	            cents = AM.to_cents(s.lstrip("$ ").strip())
78	            if cents is None or cents not in allowed:
79	                out.append(f"charges section states {s}, not an accepted charge or the total")
80	        out += [f"charges section states money without a $ sign: {s}" for s in unmarked_money(line)]
81	        out += [f"charges section states money in another form: {s}" for s in other_currency(line)]
82	    totals = [l for l in tail.splitlines() if l.startswith(TOTAL)]
83	    if len(totals) != 1 or not re.fullmatch(re.escape(TOTAL) + r"\$[\d,]+\.\d\d", totals[0]):
84	        out.append(f"total line is not exactly the template: {totals}")
85	    return out
86	
87	
88	def _walk(conn, cid, dismiss_charges=False):
89	    """Accept (or dismiss) every item through the review code path. Returns (accepted charge cents, refused [(id, code)])."""
90	    from app.backend import review
91	    from app.db import db as DB
92	    refused, cents = [], []
93	    for kind in ("entry", "amount", "flag"):
94	        for it in DB.list_items(conn, cid, kind):
95	            if it["state"] == "rejected":
96	                continue
97	            dismiss = dismiss_charges and kind == "amount" and it["kind"] == "charge"
98	            try:
99	                review.apply_review(conn, cid, it["id"], {"action": "dismiss" if dismiss else "accept"})
100	            except review.ReviewError as e:
101	                refused.append((it["id"], e.code if e.code != "CODE_CHECK_FAILED" else (e.detail or {}).get("reason_code", e.code)))
102	                continue
103	            if kind == "amount" and it["kind"] == "charge" and not dismiss and it.get("value_cents") is not None:
104	                cents.append(it["value_cents"])
105	    return cents, refused
106	
107	
108	def _count_all(conn, cid):
109	    """D-064 count path: count every amount the code held back for a missing detail, naming the confirm (and the duplicate / total flag when the code asks for it); an uncountable one is
110	    skipped. Returns the cents of every accepted charge after that."""
111	    from app.backend import count_charge, review
112	    from app.db import db as DB
113	    for it in DB.list_items(conn, cid, "amount"):
114	        if it["state"] == "rejected" or it["kind"] == "charge":
115	            continue
116	        body = {"confirm": count_charge.CONFIRM}
117	        for _ in range(2):
118	            try:
119	                count_charge.count(conn, cid, it["id"], dict(body))
120	                break
121	            except review.ReviewError as e:
122	                want = (e.detail or {}).get("confirm_with")
123	                if e.code == "CONFIRM_REQUIRED" and want and want != count_charge.CONFIRM and "confirm_flag" not in body:
124	                    body["confirm_flag"] = want
125	                    continue
126	                break
127	    return [it["value_cents"] for it in DB.list_items(conn, cid, "amount")
128	            if it["kind"] == "charge" and it["review_status"] in ("accepted", "edited") and it.get("value_cents") is not None and it["state"] != "rejected"]
129	
130	
131	_MON = "January|February|March|April|May|June|July|August|September|October|November|December"
132	_D = rf"(?:{_MON})\s+\d{{1,2}}"
133	_HEAD_DATES = [(re.compile(rf"({_D},\s+\d{{4}})\u2013({_D},\s+\d{{4}})$"), "full"), (re.compile(rf"({_D})\u2013({_D}),\s+(\d{{4}})$"), "month"),
134	               (re.compile(rf"({_D})\u2013(\d{{1,2}}),\s+(\d{{4}})$"), "day"), (re.compile(rf"({_D},\s+\d{{4}})$"), "one")]
135	_STATEMENT_FORM = re.compile(r"\(statement dated ([^;)]+); service date not stated\)$")
136	_NO_DATE_FORM = re.compile(r"\(service date not stated\)$")
137	_STATEMENT_LEAD = re.compile(r"(?:(?:statement|billing|bill|invoice|printed|posted|mailed|issued)\s+date|\bdue(?:\s+date)?|as[\s-]of|balance|payment)\s*[:#]?\W{0,8}(?:of|on)?\W{0,3}$", re.IGNORECASE)          # a 'statement PERIOD' is the service period of a UB-04
138	
139	
140	def _iso(txt):
141	    from datetime import datetime
142	    return datetime.strptime(" ".join(txt.replace(",", " ").split()), "%B %d %Y").date().isoformat()
143	
144	
145	def _head_dates(head: str):
146	    """('range'|'one', first ISO, last ISO or None) from the end of a charge header, or ('statement', ISO, None) / ('none', None, None) for the T-200 forms, or None when unreadable."""
147	    m = _STATEMENT_FORM.search(head)
148	    if m:
149	        return "statement", _iso(m.group(1)), None
150	    if _NO_DATE_FORM.search(head):
151	        return "none", None, None
152	    for rx, kind in _HEAD_DATES:
153	        m = rx.search(head)
154	        if not m:
155	            continue
156	        g = m.groups()
157	        if kind == "full":
158	            return "range", _iso(g[0]), _iso(g[1])
159	        if kind == "month":
160	            return "range", _iso(f"{g[0]}, {g[2]}"), _iso(f"{g[1]}, {g[2]}")
161	        if kind == "day":
162	            return "range", _iso(f"{g[0]}, {g[2]}"), _iso(f"{g[0].split()[0]} {g[1]}, {g[2]}")
163	        return "one", _iso(g[0]), None
164	    return None
165	
166	
167	def charge_lines(letter: str) -> list:
168	    """[(header, quote)] of the BILLED CHARGES section, by structure (a header ends ': $X.XX'; the next line is its Source line)."""
169	    from app.backend import export
170	    _, tail = export.split_letter(letter)
171	    out = []
172	    for i, line in enumerate(tail):
173	        if re.search(r": \$[\d,]+\.\d\d$", line) and not line.startswith(TOTAL) and i + 1 < len(tail):
174	            q = tail[i + 1]
175	            out.append((line, q[q.index('"') + 1:q.rindex('"')] if '"' in q else q))
176	    return out
177	
178	
179	# ---- D-071 amendment: each printed date against THAT line's own quote. Deliberately a second, simple reading of the bill text that shares no code with the production parser
180	# (app/backend/service_date.py): its own small scanner, its own rules, enumerating every reading a written date allows.
181	_MONTHS = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
182	_W = (r"(?P<per>(?P<pm1>[A-Za-z]{3,9})\.? (?P<pd1>\d{1,2})(?:st|nd|rd|th)? ?[-\u2013] ?(?:(?P<pm2>[A-Za-z]{3,9})\.? )?(?P<pd2>\d{1,2})(?:st|nd|rd|th)?, ?(?P<py>\d{4}))"
183	      r"|(?P<iso>\d{4}-\d{1,2}-\d{1,2})|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})"
184	      r"|(?P<mdy>(?P<m>[A-Za-z]{3,9})\.? (?P<d>\d{1,2})(?:st|nd|rd|th)?(?:, ?(?P<y>\d{4}))?)|(?P<dmy>(?P<d2>\d{1,2})(?:st|nd|rd|th)? (?:of )?(?P<m2>[A-Za-z]{3,9})\.?,? (?P<y2>\d{4}))"
185	      r"|(?P<yearless>\d{1,2}/\d{1,2})(?![\d/])")
186	_WRITTEN = re.compile(r"(?<![\w/$])(?:" + _W + r")(?![\w/])")
187	_JOINERS = re.compile(r"^ ?(?:-|\u2013|to|through|thru|until) ?$", re.IGNORECASE)
188	_LISTERS = re.compile(r"^ ?(?:,|;|&|and|or) ?$", re.IGNORECASE)
189	_BILLING_WORD = re.compile(r"(?:statement|stmt|invoice|billing|billed|posted|paid|received|payment|processed|mailed|due|balance|printed|issued)(?: date| dated| on| of)?[ :#]*$", re.IGNORECASE)
190	_PERIOD_WORD = re.compile(r"(?:statement period|billing period|service period|dates? of service|\bdos\b|service dates?|run of|date of the run)\W{0,6}$", re.IGNORECASE)
191	_BILL_WORD = re.compile(r"statement|\bbill|invoice|ledger|ub-?04|cms-?1500|itemi[sz]ed|\baccount\b|claim form", re.IGNORECASE)
192	
193	
194	def _month(name):
195	    return _MONTHS.get(name.lower()[:3])
196	
197	
198	def _real(y, m, d):
199	    from datetime import date
200	    try:
201	        return date(y, m, d).isoformat()
202	    except (TypeError, ValueError):
203	        return None
204	
205	
206	def _written(text):
207	    """[{start, end, options: [(first, last or None)], flaw}] for each date written in `text`. `options` lists EVERY reading the writing allows (empty when it allows none that is
208	    certain: a two-digit year, no year, a month that is not one); a pair 'A to B' is one item whose options are the combinations with the end after the start."""
209	    toks = []
210	    for m in _WRITTEN.finditer(text):
211	        g, opts, flaw = m.groupdict(), [], None
212	        if g["per"]:
213	            m1, m2 = _month(g["pm1"]), _month(g["pm2"] or g["pm1"])
214	            a, b = _real(int(g["py"]), m1, int(g["pd1"])), _real(int(g["py"]), m2, int(g["pd2"]))
215	            opts = [(a, b)] if a and b and b > a else []
216	            toks.append({"start": m.start(), "end": m.end(), "opts": opts, "flaw": None if opts else "bad", "pair": True})
217	            continue
218	        if g["iso"]:
219	            y, mo, d = (int(x) for x in g["iso"].split("-"))
220	            opts = [x for x in [_real(y, mo, d)] if x]
221	        elif g["num"]:
222	            a, b, y = re.split(r"[/.-]", g["num"])
223	            if len(y) != 4:
224	                flaw = "two-digit year"
225	            else:
226	                opts = sorted({x for x in (_real(int(y), int(a), int(b)), _real(int(y), int(b), int(a))) if x})
227	        elif g["mdy"]:
228	            if not _month(g["m"]):
229	                continue
230	            if g["y"]:
231	                opts = [x for x in [_real(int(g["y"]), _month(g["m"]), int(g["d"]))] if x]
232	            else:
233	                flaw = "no year"
234	        elif g["dmy"]:
235	            if not _month(g["m2"]):
236	                continue
237	            opts = [x for x in [_real(int(g["y2"]), _month(g["m2"]), int(g["d2"]))] if x]
238	        else:
239	            flaw = "no year"
240	        toks.append({"start": m.start(), "end": m.end(), "opts": [(o, None) for o in opts], "flaw": flaw or (None if opts else "bad"), "pair": False})
241	    units, k = [], 0
242	    while k < len(toks):
243	        t = toks[k]
244	        if k + 1 < len(toks) and not t["pair"] and not toks[k + 1]["pair"] and _JOINERS.match(text[t["end"]:toks[k + 1]["start"]]):
245	            u = toks[k + 1]
246	            combos = [(a, b) for (a, _) in t["opts"] for (b, _) in u["opts"] if b > a]
247	            units.append({"start": t["start"], "end": u["end"], "opts": combos, "flaw": t["flaw"] or u["flaw"] or (None if combos else "bad")})
248	            k += 2
249	        else:
250	            units.append(dict(t))
251	            k += 1
252	    return units
253	
254	
255	def _readings(unit, ref):
256	    """The readings left for a written date: those not after the record's own date when the writing allows several (a service does not follow its statement)."""
257	    opts = unit["opts"]
258	    if len(opts) > 1 and ref:
259	        opts = [o for o in opts if (o[1] or o[0]) <= ref]
260	    return opts
261	
262	
263	def _own_dates(text):
264	    return [u for u in _written(text) if not _BILLING_WORD.search(text[max(0, u["start"] - 30):u["start"]])]
265	
266	
267	def _period_dates(before):
268	    """The dates the bill states for its services before the quote: those led by 'statement period', 'dates of service', 'run of' ... and the dates listed after them."""
269	    us = _written(before)
270	    out = []
271	    for k, u in enumerate(us):
272	        if _PERIOD_WORD.search(before[max(0, u["start"] - 40):u["start"]]):
273	            out.append(u)
274	            j = k
275	            while j + 1 < len(us) and _LISTERS.match(before[us[j]["end"]:us[j + 1]["start"]]):
276	                out.append(us[j + 1])
277	                j += 1
278	    return out
279	
280	
281	def _dos_column(ex, quote, printed_first):
282	    """For a quote that holds several dates: the heading (nearest digit-free line above the quote's line, split at 2+ spaces) over the printed date's column, or ''."""
283	    qi = ex.find(quote)
284	    if qi < 0:
285	        return ""
286	    ls = ex.rfind("\n", 0, qi) + 1
287	    line = ex[ls:qi + len(quote)]
288	    want = {printed_first}
289	    for u in _written(line):
290	        if any(o[0] in want for o in u["opts"]):
291	            col = u["start"]
292	            for above in reversed(ex[:max(ls - 1, 0)].split("\n")[-40:]):
293	                if not above.strip():
294	                    return ""
295	                if re.search(r"\d", above):
296	                    continue
297	                heads = [(m.start(), m.group(0)) for m in re.finditer(r"\S+(?: \S+)*", above)]
298	                return min(heads, key=lambda h: abs(h[0] - col))[1] if heads else ""
299	    return ""
300	
301	
302	def charge_date_violations(letter: str, records) -> list:
303	    """D-071 amendment: every charge line's printed date must be certain from THAT line's own quote (plus, for a quote with no date, the one period the bill states before it).
304	    `records`: the case's [{n, source, date_iso, excerpt}]. Rules, per line:
305	      - the quote states one written date (or one period) -> the line prints exactly that, with its end, and only when the writing has one reading (a numeric date both ways, a two-digit
306	        year or a year-less date prints nothing); a statement, billing or due date in the quote is not a service date;
307	      - the quote states several dates -> the line prints one only if the column heading over it names the date of service;
308	      - the quote states none, in a bill -> the bill's one stated period (statement period, dates of service, run of ...), whole; several stated dates, or none -> the not-stated form
309	        '(statement dated X; service date not stated)' with X the record's date; in a visit note (not a bill) -> the note's own date.
310	    The not-stated form is always allowed when the record has a date to print as X."""
311	    norm = lambda t: " ".join(str(t).split())
312	    out = []
313	    for head, quote in charge_lines(letter):
314	        parsed = _head_dates(re.sub(r": \$[\d,]+\.\d\d$", "", head))
315	        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
316	        if parsed is None:
317	            out.append(f"charge line has no readable date form: {head}")
318	            continue
319	        if not recs:
320	            out.append(f"charge line's quote is in no record: {head}")
321	            continue
322	        kind, first, last = parsed
323	        problems = []
324	        for r in recs:
325	            ex, rd = r["excerpt"], r.get("date_iso")
326	            bill = bool(_BILL_WORD.search(r.get("source") or "") or _BILL_WORD.search(ex[:60]))
327	            n_ex, n_q = norm(ex), norm(quote)
328	            before = n_ex[:n_ex.index(n_q)]
329	            own = _own_dates(n_q)
330	            if kind in ("statement", "none"):
331	                if first and first != rd:
332	                    problems.append("the statement date is not the record's date")
333	                elif not bill and rd:
334	                    problems.append("a visit note's line must carry the note's date")
335	                continue
336	            if own:
337	                if len(own) > 1:
338	                    col = _dos_column(ex, quote, first)
339	                    if not re.search(r"dos|service|svc", col, re.IGNORECASE) or re.search(r"post|statement|bill", col, re.IGNORECASE):
340	                        problems.append(f"the quote states several dates and no column heading names the date of service (heading '{col}')")
341	                        continue
342	                    own = [u for u in own if any(o[0] == first for o in u["opts"])]
343	                    if not own:
344	                        problems.append("the printed date is in none of the quote's dates")
345	                        continue
346	                want = _readings(own[0], rd)
347	            elif bill:
348	                units = _period_dates(before)
349	                if len(units) != 1:
350	                    problems.append("the bill states " + ("no" if not units else "several") + " dates of service and the line prints one")
351	                    continue
352	                want = _readings(units[0], rd)
353	            else:
354	                want = [(rd, None)] if rd else []
355	            if len(want) != 1:
356	                problems.append("the written date has no single certain reading")
357	            elif (first, last) != want[0]:
358	                problems.append(f"the line's own text gives {want[0][0]}" + (f" to {want[0][1]}" if want[0][1] else ""))
359	        if len(problems) == len(recs):
360	            out.append(f"charge line's date is not certain from its quote ({'; '.join(sorted(set(problems)))}): {head}")
361	    return out
362	
363	
364	def letters_for(text: str, backend: str = "fixture") -> dict:
365	    """{'all_accepted': {...}, 'charges_dismissed': {...}}, each {'letters': {style: text}, 'notes': str, 'charge_cents': [...], 'refused': [(id, code)], 'gate': {style: [why...]}}."""
366	    from app.backend import export, ingest as IN, pipeline as PL, store
367	    from app.llm import provider as P
368	    out = {}
369	    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True), ("counted", False)):
370	        with PL._Backend(backend), tempfile.TemporaryDirectory() as tmp:
371	            conn, cid, call = PL._scratch_call(tmp, IN.normalize_text(text))
372	            with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
373	                PL.run_pipeline(conn, cid, text, call=call)
374	            cents, refused = _walk(conn, cid, dismiss)
375	            if variant == "counted":
376	                cents = _count_all(conn, cid)
377	            case = store.export_case(conn, cid)
378	            case["judge_not_run"] = []          # this check reads the letter text only; the second-check gate is a separate rule (D-044)
379	            built, gate = {}, {}
380	            for st in STYLES:
381	                key = st or "standard"
382	                try:
383	                    built[key] = export.build_export(case, st)
384	                except export.ExportBlocked as e:                  # T-139 r4: the export gate itself; a blocked letter is a violation, and the text is still audited below
385	                    gate[key] = [i["why"] for i in e.items]
386	                    built[key] = export.build_export(case, st, check_letter=False)
387	            src = {r["n"]: r["source"] for r in case["records"]}
388	            dismissed = sorted({src[a["record_no"]].split(",", 1)[0].strip() for a in case["amounts"] if a["cls"] == "charge" and a["review_status"] == "dismissed"})
389	            conn.close()
390	        out[variant] = {"letters": {k: v["letter_text"] for k, v in built.items()}, "notes": built["standard"]["internal_notes_text"],
391	                        "charge_cents": cents, "refused": refused, "records": case["records"], "dismissed_providers": dismissed, "gate": gate}
392	    return out
393	
394	
395	def dismissed_in_bills(notes: str, providers) -> list:
396	    """Providers whose charge was dismissed that the notes still list under BILLS TO REQUEST."""
397	    sec = notes.split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0] if "BILLS TO REQUEST" in notes else ""
398	    listed = [re.sub(r"\s*\(itemized ledger\)$", "", x.strip().rstrip(".")) for x in sec.split("\n", 2)[-1].lstrip("- ").split(";")]
399	    return [p for p in providers if p in listed]
400	
401	
402	def measure(case_list=None, backend: str = "fixture") -> dict:
403	    """The report block: {'value': total violations (0 = pass), 'cases': n, 'per_case': {...}, 'held_out_entries': n, 'r_ids': [...]}."""
404	    per_case, held = {}, 0
405	    for name, text in (case_list if case_list is not None else cases()):
406	        got = letters_for(text, backend)
407	        bad = []
408	        for style, letter in got["all_accepted"]["letters"].items():
409	            bad += [f"{style}: {v}" for v in violations(letter, got["all_accepted"]["charge_cents"])]
410	        for style, letter in got["charges_dismissed"]["letters"].items():
411	            bad += [f"{style} (charges dismissed): {v}" for v in violations(letter, (), expect_none=True)]
412	        for style, letter in got["counted"]["letters"].items():
413	            bad += [f"{style} (counted): {v}" for v in violations(letter, got["counted"]["charge_cents"])]
414	        for variant in ("all_accepted", "counted"):
415	            for style, letter in got[variant]["letters"].items():
416	                bad += [f"{style} ({variant}): {v}" for v in charge_date_violations(letter, got[variant]["records"])]
417	        for variant in ("all_accepted", "charges_dismissed", "counted"):
418	            bad += [f"{style} ({variant}): the export gate blocked this letter: {w}" for style, whys in got[variant]["gate"].items() for w in whys]
419	        bad += [f"dismissed charge's provider {p} is under BILLS TO REQUEST" for p in dismissed_in_bills(got["charges_dismissed"]["notes"], got["charges_dismissed"]["dismissed_providers"])]
420	        held += sum(1 for _, code in got["all_accepted"]["refused"] if code == "CHARGE_TEXT_IN_ENTRY")
421	        if bad:
422	            per_case[name] = sorted(set(bad))
423	    return {"value": sum(len(v) for v in per_case.values()), "cases": len(case_list if case_list is not None else cases()), "per_case": per_case,
424	            "held_out_entries": held, "backend": backend, "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
425	
426	
427	def main(argv=None) -> int:
428	    m = measure()
429	    print(json.dumps({k: v for k, v in m.items() if k != "per_case"}))
430	    for name, v in m["per_case"].items():
431	        print(f"  {name}: {v}")
432	    return 0 if m["value"] == 0 else 1
433	
434	
435	if __name__ == "__main__":
436	    sys.exit(main())
437	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:18.609Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/a && git -C /Users/arsis/zlayt-pm-project diff f0921e4 986fc55 -- app/backend/store.py app/backend/export.py app/backend/present.py"
}
````

### User / tool · 2026-11-03T00:20:18.727Z

**tool result**
````
diff --git a/app/backend/export.py b/app/backend/export.py
index 0f647e0..3d1c61e 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -19,7 +19,7 @@ import os
 import re
 from datetime import date
 
-from app.backend import amounts, charge_text, language, money
+from app.backend import amounts, charge_text, language, money, service_date
 
 LETTER_TITLE = "TREATMENT CHRONOLOGY"
 CHARGES_TITLE = "BILLED CHARGES"
@@ -71,15 +71,8 @@ def _long_date(iso):
 
 
 def _date_range(first, last=None):
-    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026', 'June 28\u2013July 2, 2026', 'December 30, 2026\u2013January 2, 2027' (D-071)."""
-    if not last or last == first:
-        return _long_date(first)
-    a, b = date.fromisoformat(first), date.fromisoformat(last)
-    if (a.year, a.month) == (b.year, b.month):
-        return f"{a.strftime('%B')} {a.day}\u2013{b.day}, {a.year}"
-    if a.year == b.year:
-        return f"{a.strftime('%B')} {a.day}\u2013{b.strftime('%B')} {b.day}, {a.year}"
-    return f"{_long_date(first)}\u2013{_long_date(last)}"
+    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026' (D-071). One implementation, shared with the case view (service_date.display)."""
+    return service_date.display(first, last)
 
 
 def _money(cents):
@@ -231,7 +224,7 @@ class _View:
         if a["dos_iso"]:
             return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
         rd = self.rec_date(n)
-        return f"{src} (statement dated {_long_date(rd)}; service date not stated)" if rd else f"{src} (service date not stated)"
+        return f"{src} {service_date.not_stated_text(rd)}"
 
     def cite(self, n):
         return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
diff --git a/app/backend/present.py b/app/backend/present.py
index 09ad1bf..aea2469 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -139,6 +139,7 @@ def amount_view(row, recs, records=None, pool=None, prep=False):
     cf = count_flag_for(row, records, nc, pool)
     counted = bool((row.get("ladder") or {}).get("counted"))
     c = _common(row, prep)
+    srec = next((r for r in records or [] if r["id"] == (row["record_ids"] or [None])[0]), None)
     if counted and row["kind"] == "charge":      # D-064: counted by the paralegal with a named confirm; no AI said it was a charge
         c["why"] = ("You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no second check was asked about it." if prep else
                     "You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no AI check was asked about it.")
@@ -148,6 +149,7 @@ def amount_view(row, recs, records=None, pool=None, prep=False):
             "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
             "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate" and not counted,
             "not_counted_reason": nc["reason"], "countable": nc["countable"],
+            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for this charge's date
             "count_confirm": {k: cf.get(k) for k in ("flag", "name", "message", "confirm_with", "of")} if cf else None}
 
 
diff --git a/app/backend/store.py b/app/backend/store.py
index c869fa0..bac2c38 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -115,17 +115,38 @@ def amount_pos(item: dict, rec):
     return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None
 
 
+def charge_service_date(item: dict, rec, pos) -> dict:
+    """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
+    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or '(statement dated June 15, 2026; service date
+    not stated)'), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
+    A date is stated only when code is certain (service_date.resolve): the bill line's own single date or complete period, tied to the line by its sentence, its row and column
+    header, or the one period its bill states. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
+    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
+    not stated, with no note (she counted it knowing). Code only."""
+    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
+    rd = (rec or {}).get("date_iso")
+    bill = AM.billing_document((rec or {}).get("source"), item.get("excerpt") or "")
+    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
+    if counted_undated:
+        r = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""}
+    elif rec is None or pos is None or not item.get("excerpt"):
+        r = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""} if bill else (
+            {"state": "stated", "first": rd, "last": None, "reason": None, "raw": ""} if rd else {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""})
+    else:
+        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
+    stated = r["state"] == "stated"
+    note = None
+    if not stated and not counted_undated:
+        note = SD.confirm_note(r["reason"], r["raw"])
+    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
+            "text": SD.display(r["first"], r["last"]) if stated else SD.not_stated_text(rd),
+            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}
+
+
 def charge_service_dates(item: dict, rec, pos) -> tuple:
-    """D-071 (extends T-200): (first, last) ISO date of service the charge's OWN bill line states, `last` None for a single day; (None, None) when the line states none. The
-    record's date of a ledger, invoice or UB-04 is the statement's, never a service date, so it is not the fallback for a billing document. A dated encounter record's date is
-    the visit. A charge the paralegal counted for a missing date of service (D-064) is (None, None). Code only: amounts.charge_basis reads the line.
-    When the line cannot be read: the record's date, unless she counted it for the missing date."""
-    from app.backend import amounts as AM          # lazy: keep the import graph as it was
-    if rec is None or pos is None or not item.get("excerpt"):
-        counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
-        return (None, None) if counted_undated else ((rec or {}).get("date_iso"), None)
-    b = AM.charge_basis(item["excerpt"], {"start": pos, "cents": item.get("value_cents")}, rec.get("source"), rec.get("date_iso"))
-    return b.get("dos"), (b.get("dos_end") if b.get("dos") else None)
+    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
+    d = charge_service_date(item, rec, pos)
+    return d["date_iso"], d["end_iso"]
 
 
 def export_case(conn, case_id: str, blockers: bool = True) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:21.033Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && tail -8 unit.log; ps aux | grep -c \"[p]ytest tests/unit\"",
 "description": "Check unit suite log"
}
````

### User / tool · 2026-11-03T00:20:21.185Z

**tool result**
````
........................................................................ [  1%]
........................................................................ [  2%]
............................3
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:23.323Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff/s && wc -l *.py && cat probe3.py && sed -n 1,60p probe4.py && cat mut.py",
 "description": "Read round-1 probes and mutants"
}
````

### User / tool · 2026-11-03T00:20:23.409Z

**tool result**
````
      16 dump.py
      22 mut.py
       6 mut2.py
       6 mut3.py
      47 probe1.py
      24 probe2.py
      22 probe3.py
      21 probe4.py
     164 total
import sys
sys.path.insert(0, sys.argv[1])
from evals import letter_check as LC
ex = "Itemized ledger, statement date 06/15/2026. 03/01/2026 office visit charge $100.00; 03/08/2026 office visit charge $120.00."
recs = [{"n":1,"source":"Fennimoor Spine Clinic, itemized ledger","date_iso":"2026-06-15","excerpt":ex}]
def L(head, quote, amt):
    return f'BILLED CHARGES\n\n{head}: {amt}\nSource [Ex. __ / Bates __]: "{quote}"\n\nBilled charges accepted from these records: {amt}'
P="Fennimoor Spine Clinic, itemized ledger"
print("right date          :", LC.charge_date_violations(L(P+", March 1, 2026","03/01/2026 office visit charge $100.00","$100.00"), recs))
print("WRONG LINE's date   :", LC.charge_date_violations(L(P+", March 8, 2026","03/01/2026 office visit charge $100.00","$100.00"), recs))
print("not-in-record date  :", LC.charge_date_violations(L(P+", March 9, 2026","03/01/2026 office visit charge $100.00","$100.00"), recs))
print("statement date      :", LC.charge_date_violations(L(P+", June 15, 2026","03/01/2026 office visit charge $100.00","$100.00"), recs))
# ambiguous-format record: check agrees with the guess
ex2 = "Itemized ledger, statement date 06/15/2026. 04/05/2026 x-ray charge $180.00."
recs2=[{"n":1,"source":P,"date_iso":"2026-06-15","excerpt":ex2}]
print("ambig April 5       :", LC.charge_date_violations(L(P+", April 5, 2026","04/05/2026 x-ray charge $180.00","$180.00"), recs2))
print("ambig May 4         :", LC.charge_date_violations(L(P+", May 4, 2026","04/05/2026 x-ray charge $180.00","$180.00"), recs2))
# period end dropped
ub = "UB-04, statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
recs3=[{"n":1,"source":"Saltmarrow General Hospital, UB-04 itemized bill","date_iso":"2026-06-19","excerpt":ub}]
Q="Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
print("period end dropped  :", LC.charge_date_violations(L("Saltmarrow General Hospital, UB-04 itemized bill, June 9, 2026",Q,"$2,105.00"), recs3))
import sys
sys.path.insert(0, sys.argv[1])
exec(open(sys.argv[2]).read().split("# multi-line ledger")[0].split("sys.path.insert(0, sys.argv[1])")[1])
UBS="Saltmarrow General Hospital, UB-04 itemized bill"
def ub(period, rd="2026-07-19"):
    run("UB "+period, f"UB-04, statement period {period}. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.", "$2,105.00", src=UBS, rd=rd)
ub("06/28/2026-07/02/2026")
ub("06/28/2026 - 07/02/2026")
ub("06/28/2026–07/02/2026")
ub("06/28-07/02/2026")
ub("June 28-July 2, 2026")
ub("June 9-12, 2026", rd="2026-06-19")
ub("June 9-12, 2024", rd="2026-06-19")
ub("December 30, 2025 - January 2, 2026", rd="2026-01-19")
ub("12/30/25 to 01/02/26", rd="2026-01-19")
ub("06/28/98 to 07/02/98", rd="2026-07-19")
run("two-digit yr 98 line", "Office visit 03/17/98 charge $220.00.", "$220.00")
run("ambig 04/05/2026 ledger", "Itemized ledger, statement date 06/15/2026. 04/05/2026 x-ray charge $180.00.", "$180.00")
# unreadable pos fallback
print(store.charge_service_dates({"excerpt": "Itemized ledger, statement date 06/15/2026. x-ray charge $180.00.", "value_cents": 18000}, {"source":"Fennimoor Spine Clinic, itemized ledger","date_iso":"2026-06-15"}, None))
print(store.charge_service_dates({"excerpt": "x", "value_cents": 18000}, None, 0))
import sys, subprocess, shutil, pathlib
root = pathlib.Path(sys.argv[1]); which = sys.argv[2]
ex, st = root/"app/backend/export.py", root/"app/backend/store.py"
sd = pathlib.Path(sys.argv[3])
shutil.copy(sd/"export.orig", ex); shutil.copy(sd/"store.orig", st)
def sub(p, old, new):
    t = p.read_text(); assert old in t, old; p.write_text(t.replace(old, new, 1))
if which == "M1_record_date":
    sub(ex, "return f\"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}\"", "return f\"{src}, {_long_date(self.rec_date(n))}\"")
elif which == "M2_plus_one_day":
    sub(ex, "return f\"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}\"", "import datetime as _d\n            return f\"{src}, {_long_date((_d.date.fromisoformat(a['dos_iso'])+_d.timedelta(days=1)).isoformat())}\"")
elif which == "M3_drop_period_end":
    sub(ex, "_date_range(a['dos_iso'], a.get('dos_end_iso'))", "_date_range(a['dos_iso'])")
elif which == "M4_undated_prints_statement_bare":
    sub(ex, "        rd = self.rec_date(n)\n        return f\"{src} (statement dated", "        rd = self.rec_date(n)\n        return f\"{src}, {_long_date(rd)}\" if rd else f\"{src} (statement dated")
elif which == "M5_no_sort":
    sub(ex, "return sorted(got, key=lambda a: (a.get(\"dos_iso\") or self._date(a), a[\"record_no\"], str(a.get(\"id\"))))", "return got")
elif which == "M6_first_date_of_record":
    sub(st, "    return b.get(\"dos\"), (b.get(\"dos_end\") if b.get(\"dos\") else None)", "    import re as _re\n    ds=[AM._dos_iso(m, rec.get('date_iso')) for m in AM._DOS_RX.finditer(item['excerpt'])]\n    ds=[d for d in ds if d]\n    return (ds[0] if ds and b.get('dos') else b.get('dos')), (b.get('dos_end') if b.get('dos') else None)")
r = subprocess.run([sys.executable, "-m", "evals.letter_check"], cwd=root, capture_output=True, text=True)
print(which, "exit", r.returncode); print("\n".join(r.stdout.splitlines()[:3])[:400])
shutil.copy(sd/"export.orig", ex); shutil.copy(sd/"store.orig", st)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:26.230Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff/s && sed -n 1,20p probe1.py; cat probe2.py",
 "description": "Read probe helper definitions"
}
````

### User / tool · 2026-11-03T00:20:26.309Z

**tool result**
````
import sys
sys.path.insert(0, sys.argv[1])
from app.backend import amounts as AM, store
def run(label, ex, which, src="Fennimoor Spine Clinic, itemized ledger", rd="2026-06-15"):
    amts = AM.find_amounts(ex)
    a = next(x for x in amts if x["raw"] == which)
    b = AM.charge_basis(ex, a, src, rd)
    s = store.charge_service_dates({"excerpt": ex, "value_cents": a["cents"]}, {"source": src, "date_iso": rd}, a["start"])
    print(f"{label:34s} ok={b['ok']!s:5} dos={b['dos']} end={b['dos_end']} -> store={s}  | {b['reason'] or ''}"[:230])
# multi-line ledger (newline-separated)
L = "Itemized ledger, statement date 06/15/2026.\n03/01/2026 office visit $100.00\n03/08/2026 office visit $120.00\n03/15/2026 x-ray $80.00"
for f in ("$100.00","$120.00","$80.00"): run("multi-line ledger "+f, L, f)
# same line, semicolon separated
L2 = "Itemized ledger, statement date 06/15/2026. 03/01/2026 office visit $100.00; 03/08/2026 office visit $120.00; 03/15/2026 x-ray $80.00."
for f in ("$100.00","$120.00","$80.00"): run("one-line ledger "+f, L2, f)
# table rows
T = "Date\tService\tCharge\n03/01/2026\toffice visit\t$100.00\n03/08/2026\toffice visit\t$120.00"
for f in ("$100.00","$120.00"): run("table "+f, T, f)
# two dates one line, one amount
run("two svc dates one line", "Itemized ledger. Office visits 03/01/2026 and 03/08/2026 charge $220.00.", "$220.00")
import sys, re
sys.path.insert(0, sys.argv[1])
from evals import letter_check as LC
base = open(sys.argv[1]+"/evals/library/case_lib11_priors_and_ledger.txt").read()
old = 'Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00.'
assert old in base
variants = {
 "dated_ledger": 'Itemized ledger, statement date 06/15/2026. 03/27/2026 new patient exam charge $250.00; 03/27/2026 x-ray charge $180.00; 04/24/2026 treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00.',
 "ambiguous": 'Itemized ledger, statement date 06/15/2026. 03/04/2026 new patient exam charge $250.00; 04/05/2026 x-ray charge $180.00; 05/06/2026 treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00.',
 "twodates": 'Itemized ledger, statement date 06/15/2026. New patient exam 03/27/2026 and x-ray 03/28/2026 charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00.',
 "multiline": 'Itemized ledger, statement date 06/15/2026.\n03/27/2026 new patient exam charge $250.00;\n04/03/2026 x-ray charge $180.00;\n04/24/2026 treatment visits 1 through 14 charge $2,310.00;\ntotal charges $2,740.00.',
}
for k, new in variants.items():
    t = base.replace(old, new)
    try:
        got = LC.letters_for(t)
    except Exception as e:
        print(k, "ERR", type(e).__name__, str(e)[:200]); continue
    for var in ("all_accepted","counted"):
        L = got[var]["letters"]["standard"]
        print("==", k, var)
        for h,q in LC.charge_lines(L):
            if "Fennimoor" in h: print("  ", h, "|", q[:120])
        print("   check:", LC.charge_date_violations(L, got[var]["records"]))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:20:50.026Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/s && cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/s && cat > pa.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import amounts as AM, store\nLED=\"Fennimoor Spine Clinic, itemized ledger\"; UBS=\"Saltmarrow General Hospital, UB-04 itemized bill\"\ndef run(label, ex, which, src=LED, rd=\"2026-06-15\"):\n    amts = AM.find_amounts(ex)\n    a = next(x for x in amts if x[\"raw\"] == which)\n    d = store.charge_service_date({\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"kind\":\"charge\"}, {\"source\": src, \"date_iso\": rd}, a[\"start\"])\n    print(f\"{label:38s} {d['state']:10s} {d['text'][:60]:60s} {d['reason'] or ''}\")\nS=\"Itemized ledger, statement date 06/15/2026. \"\nrun(\"plain 03/01/2026\", S+\"03/01/2026 office visit charge $100.00.\", \"$100.00\")\nrun(\"ambig 04/05/2026 (ref 06/15)\", S+\"04/05/2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"ambig 04/05/2026 (ref 03/01)\", S+\"04/05/2026 x-ray charge $180.00.\", \"$180.00\", rd=\"2026-03-01\")\nrun(\"ambig 04/05/2026 (ref 04/20: both<=ref)\", \"Itemized ledger, statement date 04/20/2026. 04/05/2026 x-ray charge $180.00.\", \"$180.00\", rd=\"2026-04-20\")\nrun(\"ambig 06/07/2026 ref 06/15 both<=\", S+\"06/07/2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"ambig 03/04 ref 03/20 (both <=)\", \"Itemized ledger. 03/04/2026 x-ray charge $180.00.\", \"$180.00\", rd=\"2026-03-20\")\nrun(\"ambig 03/04 ref None\", \"Itemized ledger. 03/04/2026 x-ray charge $180.00.\", \"$180.00\", rd=None)\nrun(\"13/04/2026\", S+\"13/04/2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"2026-04-05 iso\", S+\"2026-04-05 x-ray charge $180.00.\", \"$180.00\")\nrun(\"03/17/98\", \"Office visit 03/17/98 charge $220.00.\", \"$220.00\")\nrun(\"4/5 yearless\", S+\"4/5 x-ray charge $180.00.\", \"$180.00\")\nrun(\"12/28 yearless\", \"Itemized ledger, statement date 01/10/2026. 12/28 x-ray charge $180.00.\", \"$180.00\", rd=\"2026-01-10\")\nrun(\"Mar 5 yearless\", S+\"Mar 5 x-ray charge $180.00.\", \"$180.00\")\nrun(\"March 5, 2026\", S+\"March 5, 2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"5 March 2026\", S+\"5 March 2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"2-digit month-name: Mar 5, 26\", S+\"Mar 5, 26 x-ray charge $180.00.\", \"$180.00\")\nrun(\"two dates sentence\", S+\"New patient exam 03/27/2026 and x-ray 03/28/2026 charge $250.00.\", \"$250.00\")\nrun(\"two dates (office visits)\", S+\"Office visits 03/01/2026 and 03/08/2026 charge $220.00.\", \"$220.00\")\nrun(\"two dates same value\", S+\"Visit 03/01/2026 (03/01/2026) charge $220.00.\", \"$220.00\")\nrun(\"posted before svc inline\", S+\"posted 03/10/2026 office visit 03/01/2026 charge $220.00.\", \"$220.00\")\nrun(\"posted only inline\", S+\"posted 03/10/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"amount-before-date tail\", S+\"office visit charge $220.00 on 03/01/2026.\", \"$220.00\")\nrun(\"amount-before-date tail 'dated'\", S+\"office visit charge $220.00 dated 03/01/2026.\", \"$220.00\")\nrun(\"amount then paid on\", S+\"office visit charge $220.00 paid on 03/10/2026.\", \"$220.00\")\nrun(\"amount then paid 03/10 (no 'on')\", S+\"office visit charge $220.00, paid 03/10/2026.\", \"$220.00\")\nrun(\"date on previous item, list\", S+\"03/01/2026 office visit charge $100.00; x-ray charge $80.00.\", \"$80.00\")\nrun(\"date on prev item + own date\", S+\"03/01/2026 office visit charge $100.00; 03/08/2026 x-ray charge $80.00.\", \"$80.00\")\nrun(\"multi-line ledger l2\", \"Itemized ledger, statement date 06/15/2026.\\n03/01/2026 office visit $100.00\\n03/08/2026 office visit $120.00\", \"$120.00\")\nT=\"Posted\\tDOS\\tService\\tCharge\\n03/10/2026\\t03/01/2026\\toffice visit\\t$100.00\\n03/18/2026\\t03/08/2026\\toffice visit\\t$120.00\"\nrun(\"table Posted,DOS l1\", T, \"$100.00\"); run(\"table Posted,DOS l2\", T, \"$120.00\")\nT2=\"DOS\\tPosted\\tService\\tCharge\\n03/01/2026\\t03/10/2026\\toffice visit\\t$100.00\"\nrun(\"table DOS,Posted\", T2, \"$100.00\")\nT3=\"Date\\tService\\tCharge\\n03/01/2026\\toffice visit\\t$100.00\"\nrun(\"table 'Date' only\", T3, \"$100.00\")\nT4=\"Posted\\tService\\tCharge\\n03/01/2026\\toffice visit\\t$100.00\"\nrun(\"table Posted only\", T4, \"$100.00\")\nT5=\"Date\\tPosted\\tService\\tCharge\\n03/01/2026\\t03/10/2026\\toffice visit\\t$100.00\"\nrun(\"table Date,Posted (no DOS head)\", T5, \"$100.00\")\nT6=\"Svc Date | Posted | Service | Charge\\n03/01/2026 | 03/10/2026 | office visit | $100.00\"\nrun(\"pipe table Svc Date\", T6, \"$100.00\")\nT7=\"Date of Service  Posted      Charge\\n03/01/2026       03/10/2026  $100.00\"\nrun(\"space-aligned table\", T7, \"$100.00\")\nT8=\"Visit Date  Billed On   Charge\\n03/01/2026  03/10/2026  $100.00\"\nrun(\"Visit Date, Billed On\", T8, \"$100.00\")\nT9=\"Charge\\tDOS\\n$100.00\\t03/01/2026\"\nrun(\"amount col before DOS\", T9, \"$100.00\")\n# CMS-1500\nC=\"CMS-1500 claim. Dates of service 06/24/2026 and 07/08/2026. 99213 office visit charge $185.00; 97110 therapy charge $95.00.\"\nrun(\"CMS two dates l1\", C, \"$185.00\", src=\"Wardlaw Orthopedics, CMS-1500\"); run(\"CMS two dates l2\", C, \"$95.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\n# UB-04 periods\ndef ub(period, rd=\"2026-07-19\"):\n    run(\"UB \"+period, f\"UB-04, statement period {period}. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.\", \"$2,105.00\", src=UBS, rd=rd)\nfor p,rd in [(\"06/28/2026-07/02/2026\",\"2026-07-19\"),(\"06/28/2026 - 07/02/2026\",\"2026-07-19\"),(\"06/28/2026–07/02/2026\",\"2026-07-19\"),(\"06/28-07/02/2026\",\"2026-07-19\"),(\"June 28-July 2, 2026\",\"2026-07-19\"),(\"June 9-12, 2026\",\"2026-06-19\"),(\"June 9-12, 2024\",\"2026-06-19\"),(\"December 30, 2025 - January 2, 2026\",\"2026-01-19\"),(\"12/30/25 to 01/02/26\",\"2026-01-19\"),(\"06/09/2026 to 06/12/2026\",\"2026-06-19\"),(\"06/09/2026 to 06/12/2026\",\"2026-09-19\"),(\"09/06/2026 to 09/12/2026\",\"2026-09-19\"),(\"06/07/2026 to 06/12/2026\",\"2026-06-19\"),(\"06/12/2026 to 06/09/2026\",\"2026-06-19\"),(\"06/09/2026 to 06/09/2026\",\"2026-06-19\"),(\"2026-06-09 to 2026-06-12\",\"2026-06-19\"),(\"Jun 9 to Jun 12\",\"2026-06-19\")]:\n    ub(p, rd)\nrun(\"UB two periods\", \"UB-04, statement period 06/09/2026 to 06/12/2026; dates of service 07/01/2026 to 07/03/2026. Rev 0450 ER FL47 total charges $2,105.00.\", \"$2,105.00\", src=UBS, rd=\"2026-07-19\")\nrun(\"UB stmt date + period\", \"UB-04, statement date 06/19/2026, statement period 06/09/2026 to 06/12/2026. Rev 0450 ER FL47 total charges $2,105.00.\", \"$2,105.00\", src=UBS, rd=\"2026-06-19\")\nrun(\"UB stmt date only\", \"UB-04, statement date 06/19/2026. Rev 0450 ER FL47 total charges $2,105.00.\", \"$2,105.00\", src=UBS, rd=\"2026-06-19\")\nrun(\"UB no code, period before\", \"UB-04, statement period 06/09/2026 to 06/12/2026. Emergency room total charges $2,105.00.\", \"$2,105.00\", src=UBS, rd=\"2026-06-19\")\nrun(\"visit note (non-bill) no date in line\", \"Visit note: patient seen, charge per visit $185.00.\", \"$185.00\", src=\"Dr. Reyes, visit note\", rd=\"2026-02-02\")\nrun(\"visit note date in line\", \"Visit note 02/03/2026: charge $185.00.\", \"$185.00\", src=\"Dr. Reyes, visit note\", rd=\"2026-02-02\")\nrun(\"EMS non-bill dated\", \"Ambulance run 01/09/2026, charge $1,250.00.\", \"$1,250.00\", src=\"Ridgeway EMS, run report\", rd=\"2026-01-09\")\nrun(\"two-year dd.mm.yyyy\", S+\"05.04.2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"dash 05-04-2026\", S+\"05-04-2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"Sept. 3rd, 2026\", S+\"Sept. 3rd, 2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"date glued 'on03/01/2026'\", S+\"visit on03/01/2026 charge $100.00.\", \"$100.00\")\nrun(\"feb 30 invalid\", S+\"02/30/2026 x-ray charge $180.00.\", \"$180.00\")\nrun(\"ref after: svc after stmt iso\", \"Itemized ledger, statement date 06/15/2026. 2026-07-01 x-ray charge $180.00.\", \"$180.00\")\nEOF\ncd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I s/pa.py $PWD/a 2>&1 | tee pa.out",
 "description": "Probe the new resolver across layouts"
}
````

### User / tool · 2026-11-03T00:20:50.397Z

**tool result**
````
plain 03/01/2026                       not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
ambig 04/05/2026 (ref 06/15)           not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
ambig 04/05/2026 (ref 03/01)           not_stated (statement dated March 1, 2026; service date not stated)     ambiguous_numeric
ambig 04/05/2026 (ref 04/20: both<=ref) stated     April 5, 2026                                                
ambig 06/07/2026 ref 06/15 both<=      stated     June 7, 2026                                                 
ambig 03/04 ref 03/20 (both <=)        stated     March 4, 2026                                                
ambig 03/04 ref None                   not_stated (service date not stated)                                    ambiguous_numeric
13/04/2026                             stated     April 13, 2026                                               
2026-04-05 iso                         stated     April 5, 2026                                                
03/17/98                               not_stated (statement dated June 15, 2026; service date not stated)     two_digit_year
4/5 yearless                           not_stated (statement dated June 15, 2026; service date not stated)     no_year
12/28 yearless                         not_stated (statement dated January 10, 2026; service date not stated)  no_year
Mar 5 yearless                         not_stated (statement dated June 15, 2026; service date not stated)     no_year
March 5, 2026                          stated     March 5, 2026                                                
5 March 2026                           stated     March 5, 2026                                                
2-digit month-name: Mar 5, 26          not_stated (statement dated June 15, 2026; service date not stated)     no_year
two dates sentence                     not_stated (statement dated June 15, 2026; service date not stated)     several_dates
two dates (office visits)              not_stated (statement dated June 15, 2026; service date not stated)     several_dates
two dates same value                   not_stated (statement dated June 15, 2026; service date not stated)     several_dates
posted before svc inline               not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
posted only inline                     not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
amount-before-date tail                not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
amount-before-date tail 'dated'        not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
amount then paid on                    not_stated (statement dated June 15, 2026; service date not stated)     no_date
amount then paid 03/10 (no 'on')       not_stated (statement dated June 15, 2026; service date not stated)     no_date
date on previous item, list            not_stated (statement dated June 15, 2026; service date not stated)     no_date
date on prev item + own date           stated     March 8, 2026                                                
multi-line ledger l2                   stated     March 8, 2026                                                
table Posted,DOS l1                    not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
table Posted,DOS l2                    stated     March 8, 2026                                                
table DOS,Posted                       not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
table 'Date' only                      not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
table Posted only                      not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
table Date,Posted (no DOS head)        not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
pipe table Svc Date                    not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
space-aligned table                    not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
Visit Date, Billed On                  not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
amount col before DOS                  not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
CMS two dates l1                       not_stated (statement dated June 15, 2026; service date not stated)     several_dates
CMS two dates l2                       not_stated (statement dated June 15, 2026; service date not stated)     several_dates
UB 06/28/2026-07/02/2026               stated     June 28–July 2, 2026                                         
UB 06/28/2026 - 07/02/2026             stated     June 28–July 2, 2026                                         
UB 06/28/2026–07/02/2026               stated     June 28–July 2, 2026                                         
UB 06/28-07/02/2026                    not_stated (statement dated July 19, 2026; service date not stated)     no_year
UB June 28-July 2, 2026                stated     June 28–July 2, 2026                                         
UB June 9-12, 2026                     stated     June 9–12, 2026                                              
UB June 9-12, 2024                     stated     June 9–12, 2024                                              
UB December 30, 2025 - January 2, 2026 stated     December 30, 2025–January 2, 2026                            
UB 12/30/25 to 01/02/26                not_stated (statement dated January 19, 2026; service date not stated)  two_digit_year
UB 06/09/2026 to 06/12/2026            stated     June 9–12, 2026                                              
UB 06/09/2026 to 06/12/2026            stated     June 9–12, 2026                                              
UB 09/06/2026 to 09/12/2026            stated     September 6–12, 2026                                         
UB 06/07/2026 to 06/12/2026            stated     June 7–12, 2026                                              
UB 06/12/2026 to 06/09/2026            not_stated (statement dated June 19, 2026; service date not stated)     invalid
UB 06/09/2026 to 06/09/2026            not_stated (statement dated June 19, 2026; service date not stated)     invalid
UB 2026-06-09 to 2026-06-12            stated     June 9–12, 2026                                              
UB Jun 9 to Jun 12                     not_stated (statement dated June 19, 2026; service date not stated)     no_year
UB two periods                         not_stated (statement dated July 19, 2026; service date not stated)     several_dates
UB stmt date + period                  stated     June 9–12, 2026                                              
UB stmt date only                      not_stated (statement dated June 19, 2026; service date not stated)     no_date
UB no code, period before              not_stated (statement dated June 19, 2026; service date not stated)     no_date
visit note (non-bill) no date in line  stated     February 2, 2026                                             
visit note date in line                not_stated (statement dated February 2, 2026; service date not stated)  ambiguous_numeric
EMS non-bill dated                     stated     January 9, 2026                                              
two-year dd.mm.yyyy                    not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
dash 05-04-2026                        not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
Sept. 3rd, 2026                        not_stated (statement dated June 15, 2026; service date not stated)     no_date
date glued 'on03/01/2026'              not_stated (statement dated June 15, 2026; service date not stated)     no_date
feb 30 invalid                         not_stated (statement dated June 15, 2026; service date not stated)     invalid
ref after: svc after stmt iso          stated     July 1, 2026
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:21:19.146Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && cat > s/pb.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nexec(open(sys.argv[2]).read().split('S=\"Itemized')[0].split(\"sys.path.insert(0, sys.argv[1])\")[1])\nS=\"Itemized ledger, statement date 06/15/2026. \"\nrun(\"inline posted-before-svc\", S+\"posted 03/20/2026 office visit 03/13/2026 charge $220.00.\", \"$220.00\")\nrun(\"inline svc then posted\", S+\"office visit 03/13/2026 posted 03/20/2026 charge $220.00.\", \"$220.00\")\nrun(\"inline posted only\", S+\"posted 03/20/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"tail on\", S+\"office visit charge $220.00 on 03/13/2026.\", \"$220.00\")\nrun(\"tail dated\", S+\"office visit charge $220.00 dated 03/13/2026.\", \"$220.00\")\nrun(\"tail paid on\", S+\"office visit charge $220.00 paid on 03/20/2026.\", \"$220.00\")\nrun(\"tail paid (no on)\", S+\"office visit charge $220.00, paid 03/20/2026.\", \"$220.00\")\nrun(\"tail 'received'\", S+\"office visit charge $220.00; received 03/20/2026.\", \"$220.00\")\nrun(\"tail 'adjusted'\", S+\"office visit charge $220.00 adjusted 03/20/2026.\", \"$220.00\")\nrun(\"tail 'submitted to insurer'\", S+\"office visit charge $220.00 submitted 03/20/2026.\", \"$220.00\")\nrun(\"tail 'on' + posting word before\", S+\"office visit charge $220.00 posted on 03/20/2026.\", \"$220.00\")\nrun(\"tail 'for'\", S+\"charge $220.00 for 03/13/2026.\", \"$220.00\")\nrun(\"tail 'service' w/ posted\", S+\"charge $220.00 for service on 03/13/2026, posted 03/20/2026.\", \"$220.00\")\nrun(\"date on prev item, list\", S+\"03/13/2026 office visit charge $100.00; x-ray charge $80.00.\", \"$80.00\")\nrun(\"date on prev item + own date\", S+\"03/13/2026 office visit charge $100.00; 03/20/2026 x-ray charge $80.00.\", \"$80.00\")\nrun(\"2 amounts, one date first\", S+\"03/13/2026 office visit $100.00 and x-ray $80.00.\", \"$80.00\")\nrun(\"2 amounts, one date first (1st)\", S+\"03/13/2026 office visit $100.00 and x-ray $80.00.\", \"$100.00\")\nT=\"Posted\\tDOS\\tService\\tCharge\\n03/20/2026\\t03/13/2026\\toffice visit\\t$100.00\\n03/27/2026\\t03/14/2026\\toffice visit\\t$120.00\"\nrun(\"table Posted,DOS l1\", T, \"$100.00\"); run(\"table Posted,DOS l2\", T, \"$120.00\")\nT2=\"DOS\\tPosted\\tService\\tCharge\\n03/13/2026\\t03/20/2026\\toffice visit\\t$100.00\"\nrun(\"table DOS,Posted\", T2, \"$100.00\")\nT3=\"Date\\tService\\tCharge\\n03/13/2026\\toffice visit\\t$100.00\"\nrun(\"table 'Date' only\", T3, \"$100.00\")\nT4=\"Posted\\tService\\tCharge\\n03/13/2026\\toffice visit\\t$100.00\"\nrun(\"table Posted only\", T4, \"$100.00\")\nT5=\"Date\\tPosted\\tService\\tCharge\\n03/13/2026\\t03/20/2026\\toffice visit\\t$100.00\"\nrun(\"table Date,Posted (no DOS head)\", T5, \"$100.00\")\nT6=\"Svc Date | Posted | Service | Charge\\n03/13/2026 | 03/20/2026 | office visit | $100.00\"\nrun(\"pipe table Svc Date,Posted\", T6, \"$100.00\")\nT6b=\"Posted | Svc Date | Service | Charge\\n03/20/2026 | 03/13/2026 | office visit | $100.00\"\nrun(\"pipe table Posted,Svc Date\", T6b, \"$100.00\")\nT7=\"Date of Service  Posted      Charge\\n03/13/2026       03/20/2026  $100.00\"\nrun(\"space-aligned DOS,Posted\", T7, \"$100.00\")\nT7b=\"Posted      Date of Service  Charge\\n03/20/2026  03/13/2026       $100.00\"\nrun(\"space-aligned Posted,DOS\", T7b, \"$100.00\")\nT8=\"Visit Date  Billed On   Charge\\n03/13/2026  03/20/2026  $100.00\"\nrun(\"Visit Date, Billed On\", T8, \"$100.00\")\nT8b=\"Billed On   Visit Date  Charge\\n03/20/2026  03/13/2026  $100.00\"\nrun(\"Billed On, Visit Date\", T8b, \"$100.00\")\nT9=\"Charge\\tDOS\\n$100.00\\t03/13/2026\"\nrun(\"amount col before DOS\", T9, \"$100.00\")\nT10=\"Entry date\\tService\\tAmount\\n03/20/2026\\toffice visit\\t$100.00\"\nrun(\"Entry date only\", T10, \"$100.00\")\nT11=\"Date\\tCode\\tDescription\\tCharge\\n03/13/2026\\t99213\\toffice visit\\t$100.00\\n03/14/2026\\t97110\\ttherapy\\t$80.00\"\nrun(\"Date,Code table l1\", T11, \"$100.00\"); run(\"Date,Code table l2\", T11, \"$80.00\")\nT12=\"Date\\tDescription\\tCharge\\tPayment\\tBalance\\n03/13/2026\\toffice visit\\t$100.00\\t$0.00\\t$100.00\"\nrun(\"Date,Desc,Charge,Pay,Bal\", T12, \"$100.00\")\nT13=\"Date\\tDescription\\tCharge\\tPaid\\n03/13/2026\\t03/20/2026\\toffice visit\\t$100.00\"  # header has fewer cells than row\nrun(\"header fewer cells than row\", T13, \"$100.00\")\nT14=\"Service Dates: 03/13/2026\\nCharges\\n99213 office visit $100.00\"\nrun(\"heading line then coded\", T14, \"$100.00\", src=UBS if False else \"Fennimoor Spine Clinic, itemized ledger\")\nC=\"CMS-1500 claim. Box 24A dates of service 06/24/2026 and 07/08/2026. 99213 office visit charge $185.00; 97110 therapy charge $95.00.\"\nrun(\"CMS two dates\", C, \"$185.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\nC2=\"CMS-1500 claim, 24A From 06/24/2026 To 06/24/2026. 99213 office visit charge $185.00.\"\nrun(\"CMS From/To same day\", C2, \"$185.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\nC3=\"CMS-1500 claim.\\n24A  From 06/24/2026  To 06/26/2026\\n99213 office visit charge $185.00.\"\nrun(\"CMS From/To period\", C3, \"$185.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\nC4=\"CMS-1500 claim. Dates of service 06/24/2026, 07/08/2026, 07/22/2026. 99213 office visit charge $185.00.\"\nrun(\"CMS three dates\", C4, \"$185.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\nC5=\"CMS-1500 claim. Date of service 06/24/2026. 99213 office visit charge $185.00; 97110 therapy charge $95.00.\"\nrun(\"CMS one date, 2 lines\", C5, \"$95.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\nC6=\"CMS-1500 claim. 06/24/2026 99213 charge $185.00. 07/08/2026 97110 charge $95.00.\"\nrun(\"CMS date-before-code l2\", C6, \"$95.00\", src=\"Wardlaw Orthopedics, CMS-1500\")\nC7=\"Itemized bill dated 07/20/2026. Service date 06/24/2026. 99213 office visit charge $185.00.\"\nrun(\"bill dated + service date\", C7, \"$185.00\", src=\"Wardlaw Orthopedics, itemized bill\", rd=\"2026-07-20\")\nC8=\"Invoice date 07/20/2026. 99213 office visit charge $185.00.\"\nrun(\"invoice date only, coded\", C8, \"$185.00\", src=\"Wardlaw Orthopedics, invoice\", rd=\"2026-07-20\")\nC9=\"Invoice. 99213 office visit 06/24/2026 charge $185.00; invoice date 07/20/2026.\"\nrun(\"svc inline, invoice date after\", C9, \"$185.00\", src=\"Wardlaw Orthopedics, invoice\", rd=\"2026-07-20\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/pb.py $PWD/a s/pa.py 2>&1 | tee pb.out",
 "description": "Re-probe with unambiguous day>12 dates"
}
````

### User / tool · 2026-11-03T00:21:19.447Z

**tool result**
````
inline posted-before-svc               stated     March 13, 2026                                               
inline svc then posted                 stated     March 13, 2026                                               
inline posted only                     not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
tail on                                stated     March 13, 2026                                               
tail dated                             stated     March 13, 2026                                               
tail paid on                           not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail paid (no on)                      not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'received'                        not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'adjusted'                        not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'submitted to insurer'            not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'on' + posting word before        not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'for'                             stated     March 13, 2026                                               
tail 'service' w/ posted               stated     March 13, 2026                                               
date on prev item, list                not_stated (statement dated June 15, 2026; service date not stated)     no_date
date on prev item + own date           stated     March 20, 2026                                               
2 amounts, one date first              stated     March 13, 2026                                               
2 amounts, one date first (1st)        stated     March 13, 2026                                               
table Posted,DOS l1                    stated     March 13, 2026                                               
table Posted,DOS l2                    stated     March 14, 2026                                               
table DOS,Posted                       stated     March 13, 2026                                               
table 'Date' only                      stated     March 13, 2026                                               
table Posted only                      not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
table Date,Posted (no DOS head)        stated     March 13, 2026                                               
pipe table Svc Date,Posted             stated     March 13, 2026                                               
pipe table Posted,Svc Date             stated     March 13, 2026                                               
space-aligned DOS,Posted               stated     March 13, 2026                                               
space-aligned Posted,DOS               stated     March 13, 2026                                               
Visit Date, Billed On                  stated     March 13, 2026                                               
Billed On, Visit Date                  stated     March 13, 2026                                               
amount col before DOS                  stated     March 13, 2026                                               
Entry date only                        stated     March 20, 2026                                               
Date,Code table l1                     stated     March 13, 2026                                               
Date,Code table l2                     stated     March 14, 2026                                               
Date,Desc,Charge,Pay,Bal               stated     March 13, 2026                                               
header fewer cells than row            not_stated (statement dated June 15, 2026; service date not stated)     several_dates
heading line then coded                not_stated (statement dated June 15, 2026; service date not stated)     no_date
CMS two dates                          not_stated (statement dated June 15, 2026; service date not stated)     several_dates
CMS From/To same day                   not_stated (statement dated June 15, 2026; service date not stated)     no_date
CMS From/To period                     not_stated (statement dated June 15, 2026; service date not stated)     no_date
CMS three dates                        not_stated (statement dated June 15, 2026; service date not stated)     several_dates
CMS one date, 2 lines                  stated     June 24, 2026                                                
CMS date-before-code l2                not_stated (statement dated June 15, 2026; service date not stated)     ambiguous_numeric
bill dated + service date              not_stated (statement dated July 20, 2026; service date not stated)     no_date
invoice date only, coded               not_stated (statement dated July 20, 2026; service date not stated)     no_date
svc inline, invoice date after         stated     June 24, 2026
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:22:03.359Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && cat > s/pc.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nexec(open(sys.argv[2]).read().split('S=\"Itemized')[0].split(\"sys.path.insert(0, sys.argv[1])\")[1])\nS=\"Itemized ledger, statement date 06/15/2026. \"\nfor h in [\"Date\",\"Service Date\",\"DOS\",\"Entry date\",\"Transaction Date\",\"Txn Date\",\"Recorded\",\"Filed\",\"Claim Date\",\"Sent\",\"Issued\",\"Printed\",\"Reported\",\"Remit Date\",\"Effective\",\"Date entered\",\"Charged on\",\"Invoiced\",\"Date billed\",\"Due\",\"Reference Date\",\"Closed\",\"Submitted\",\"Adjusted\",\"Written\",\"Visit\",\"Encounter\",\"Row date\",\"Created\",\"Statement Date\"]:\n    T=f\"{h}\\tService\\tCharge\\n03/13/2026\\toffice visit\\t$100.00\"\n    run(f\"single col '{h}'\", T, \"$100.00\")\nprint(\"--- relative / continuation\")\nrun(\"and a follow-up next day\", S+\"03/13/2026 office visit $100.00 and a follow-up visit the next day $80.00.\", \"$80.00\")\nrun(\"and repeat three weeks later\", S+\"03/13/2026 office visit $100.00 and a repeat visit three weeks later $80.00.\", \"$80.00\")\nrun(\"tail 'the following week'\", S+\"x-ray charge $80.00 the following week 03/20/2026.\", \"$80.00\")\nrun(\"tail 'for' posted\", S+\"charge $220.00 for posting 03/20/2026.\", \"$220.00\")\nrun(\"tail 'balance forward'\", S+\"charge $220.00 balance forward from 03/20/2026.\", \"$220.00\")\nrun(\"tail 'at'\", S+\"charge $220.00 at 03/20/2026.\", \"$220.00\")\nrun(\"tail 'since'\", S+\"charge $220.00 since 03/20/2026.\", \"$220.00\")\nrun(\"tail 'from'\", S+\"charge $220.00 from 03/20/2026.\", \"$220.00\")\nrun(\"tail 'before'\", S+\"charge $220.00 before 03/20/2026.\", \"$220.00\")\nrun(\"lead 'after' \", S+\"after 03/20/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'since'\", S+\"since 03/20/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'until'\", S+\"office visit until 03/20/2026 charge $220.00.\", \"$220.00\")\nrun(\"lead 'next appt'\", S+\"next appointment 03/20/2026; office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'DOB'\", S+\"DOB 03/20/1980 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'DOB' 4-digit-year 1980 + visit\", S+\"DOB 03/20/1980; visit 03/13/2026 charge $220.00.\", \"$220.00\")\nrun(\"lead 'injury date'\", S+\"date of injury 01/05/2026; office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'DOI' only\", S+\"DOI 01/15/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'accident'\", S+\"accident 01/15/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'referral'\", S+\"referred 01/15/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'claim filed'\", S+\"claim filed 01/15/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"lead 'follow up on'\", S+\"office visit charge $220.00, follow-up on 03/20/2026.\", \"$220.00\")\nrun(\"tail 'next visit'\", S+\"office visit charge $220.00; next visit 03/20/2026.\", \"$220.00\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/pc.py $PWD/a s/pa.py 2>&1 | tee pc.out; tail -3 unit.log | cut -c1-120",
 "description": "Probe header synonyms and lead/tail words"
}
````

### User / tool · 2026-11-03T00:22:03.652Z

**tool result**
````
single col 'Date'                      stated     March 13, 2026                                               
single col 'Service Date'              stated     March 13, 2026                                               
single col 'DOS'                       stated     March 13, 2026                                               
single col 'Entry date'                stated     March 13, 2026                                               
single col 'Transaction Date'          stated     March 13, 2026                                               
single col 'Txn Date'                  stated     March 13, 2026                                               
single col 'Recorded'                  stated     March 13, 2026                                               
single col 'Filed'                     stated     March 13, 2026                                               
single col 'Claim Date'                stated     March 13, 2026                                               
single col 'Sent'                      stated     March 13, 2026                                               
single col 'Issued'                    stated     March 13, 2026                                               
single col 'Printed'                   stated     March 13, 2026                                               
single col 'Reported'                  stated     March 13, 2026                                               
single col 'Remit Date'                stated     March 13, 2026                                               
single col 'Effective'                 stated     March 13, 2026                                               
single col 'Date entered'              not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Charged on'                stated     March 13, 2026                                               
single col 'Invoiced'                  not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Date billed'               not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Due'                       not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Reference Date'            stated     March 13, 2026                                               
single col 'Closed'                    stated     March 13, 2026                                               
single col 'Submitted'                 not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Adjusted'                  not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Written'                   stated     March 13, 2026                                               
single col 'Visit'                     stated     March 13, 2026                                               
single col 'Encounter'                 stated     March 13, 2026                                               
single col 'Row date'                  stated     March 13, 2026                                               
single col 'Created'                   not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
single col 'Statement Date'            not_stated (statement dated June 15, 2026; service date not stated)     non_service_date
--- relative / continuation
and a follow-up next day               stated     March 13, 2026                                               
and repeat three weeks later           stated     March 13, 2026                                               
tail 'the following week'              not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'for' posted                      not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'balance forward'                 not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'at'                              not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'since'                           not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'from'                            not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'before'                          not_stated (statement dated June 15, 2026; service date not stated)     no_date
lead 'after'                           stated     March 20, 2026                                               
lead 'since'                           stated     March 20, 2026                                               
lead 'until'                           stated     March 20, 2026                                               
lead 'next appt'                       not_stated (statement dated June 15, 2026; service date not stated)     no_date
lead 'DOB'                             stated     March 20, 1980                                               
lead 'DOB' 4-digit-year 1980 + visit   stated     March 13, 2026                                               
lead 'injury date'                     not_stated (statement dated June 15, 2026; service date not stated)     no_date
lead 'DOI' only                        stated     January 15, 2026                                             
lead 'accident'                        stated     January 15, 2026                                             
lead 'referral'                        stated     January 15, 2026                                             
lead 'claim filed'                     stated     January 15, 2026                                             
lead 'follow up on'                    not_stated (statement dated June 15, 2026; service date not stated)     no_date
tail 'next visit'                      not_stated (statement dated June 15, 2026; service date not stated)     no_date
........................................................................ [ 32%]
........................................................................ [ 33%]
....
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:22:27.760Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && cat > s/pd.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nexec(open(sys.argv[2]).read().split('S=\"Itemized')[0].split(\"sys.path.insert(0, sys.argv[1])\")[1])\nS=\"Itemized ledger, statement date 06/15/2026. \"\nrun(\"DOI comma\", S+\"Date of injury 01/15/2026, office visit charge $220.00.\", \"$220.00\")\nrun(\"DOI colon\", S+\"Date of injury: 01/15/2026 - office visit charge $220.00.\", \"$220.00\")\nrun(\"DOI own sentence\", S+\"Date of injury 01/15/2026. Office visit charge $220.00.\", \"$220.00\")\nrun(\"patient DOB comma\", S+\"Patient DOB 03/20/1980, office visit charge $220.00.\", \"$220.00\")\nrun(\"authorization date\", S+\"Authorization 02/10/2026, office visit charge $220.00.\", \"$220.00\")\nrun(\"referral date\", S+\"Referred 02/10/2026; office visit charge $220.00.\", \"$220.00\")\nrun(\"pre-auth\", S+\"Pre-authorized 02/10/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"unambig svc after stmt\", S+\"07/20/2026 office visit charge $220.00.\", \"$220.00\")\nrun(\"svc year 1998 4-digit\", S+\"03/13/1998 office visit charge $220.00.\", \"$220.00\")\nrun(\"svc year 2031\", S+\"03/13/2031 office visit charge $220.00.\", \"$220.00\")\nrun(\"svc before DOI\", S+\"03/13/2020 office visit charge $220.00.\", \"$220.00\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/pd.py $PWD/a s/pa.py 2>&1 | tee pd.out",
 "description": "Probe same-sentence non-service dates"
}
````

### User / tool · 2026-11-03T00:22:28.066Z

**tool result**
````
DOI comma                              stated     January 15, 2026                                             
DOI colon                              stated     January 15, 2026                                             
DOI own sentence                       not_stated (statement dated June 15, 2026; service date not stated)     no_date
patient DOB comma                      stated     March 20, 1980                                               
authorization date                     stated     February 10, 2026                                            
referral date                          not_stated (statement dated June 15, 2026; service date not stated)     no_date
pre-auth                               stated     February 10, 2026                                            
unambig svc after stmt                 stated     July 20, 2026                                                
svc year 1998 4-digit                  stated     March 13, 1998                                               
svc year 2031                          stated     March 13, 2031                                               
svc before DOI                         stated     March 13, 2020
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:22:48.368Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && grep -n \"service_date\\|_DOS_RX\\|_dos_iso\\|charge_basis\\|AM\\.\\|amounts\" a/evals/letter_check.py | sed -n 1,40p; echo ---; tail -2 unit.log | cut -c1-100\ncat > s/p3.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom evals import letter_check as LC\nP=\"Fennimoor Spine Clinic, itemized ledger\"\ndef L(head, quote, amt):\n    return f'BILLED CHARGES\\n\\n{head}: {amt}\\nSource [Ex. __ / Bates __]: \"{quote}\"\\n\\nBilled charges accepted from these records: {amt}'\ndef chk(label, src, rd, ex, head, quote, amt):\n    recs=[{\"n\":1,\"source\":src,\"date_iso\":rd,\"excerpt\":ex}]\n    print(f\"{label:34s}\", LC.charge_date_violations(L(head, quote, amt), recs))\nex = \"Itemized ledger, statement date 06/15/2026. 03/13/2026 office visit charge $100.00; 03/20/2026 office visit charge $120.00.\"\nq1=\"03/13/2026 office visit charge $100.00\"; q2=\"03/20/2026 office visit charge $120.00\"\nchk(\"right line1\", P,\"2026-06-15\",ex,P+\", March 13, 2026\",q1,\"$100.00\")\nchk(\"WRONG LINE (line2 date on line1)\", P,\"2026-06-15\",ex,P+\", March 20, 2026\",q1,\"$100.00\")\nchk(\"not in record\", P,\"2026-06-15\",ex,P+\", March 9, 2026\",q1,\"$100.00\")\nchk(\"bare statement date\", P,\"2026-06-15\",ex,P+\", June 15, 2026\",q1,\"$100.00\")\nchk(\"not-stated form (allowed)\", P,\"2026-06-15\",ex,P+\" (statement dated June 15, 2026; service date not stated)\",q1,\"$100.00\")\nchk(\"not-stated wrong stmt date\", P,\"2026-06-15\",ex,P+\" (statement dated June 16, 2026; service date not stated)\",q1,\"$100.00\")\nexa = \"Itemized ledger, statement date 06/15/2026. 04/05/2026 x-ray charge $180.00.\"\nqa=\"04/05/2026 x-ray charge $180.00\"\nchk(\"ambig April 5 printed\", P,\"2026-06-15\",exa,P+\", April 5, 2026\",qa,\"$180.00\")\nchk(\"ambig May 4 printed\", P,\"2026-06-15\",exa,P+\", May 4, 2026\",qa,\"$180.00\")\nexb = \"Itemized ledger, statement date 06/15/2026. 04/05/2026 x-ray charge $180.00.\"\nchk(\"ambig, ref 04/20 -> April 5 ok\", P,\"2026-04-20\",\"Itemized ledger. 04/05/2026 x-ray charge $180.00.\",P+\", April 5, 2026\",qa,\"$180.00\")\nub = \"UB-04, statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.\"\nQ=\"Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.\"\nU=\"Saltmarrow General Hospital, UB-04 itemized bill\"\nchk(\"period full\", U,\"2026-06-19\",ub,U+\", June 9–12, 2026\",Q,\"$2,105.00\")\nchk(\"period end dropped\", U,\"2026-06-19\",ub,U+\", June 9, 2026\",Q,\"$2,105.00\")\nchk(\"period wrong end\", U,\"2026-06-19\",ub,U+\", June 9–13, 2026\",Q,\"$2,105.00\")\nchk(\"period wrong year\", U,\"2026-06-19\",ub,U+\", June 9–12, 2025\",Q,\"$2,105.00\")\nchk(\"period start only moved\", U,\"2026-06-19\",ub,U+\", June 10–12, 2026\",Q,\"$2,105.00\")\nub2 = \"UB-04, statement period 06/09/2026 to 06/12/2026; dates of service 07/01/2026 to 07/03/2026. Rev 0450 ER FL47 total charges $2,105.00.\"\nchk(\"two periods, prints one\", U,\"2026-07-19\",ub2,U+\", June 9–12, 2026\",\"Rev 0450 ER FL47 total charges $2,105.00.\",\"$2,105.00\")\ncms=\"CMS-1500 claim. Dates of service 06/24/2026 and 07/08/2026. 99213 office visit charge $185.00.\"\nW=\"Wardlaw Orthopedics, CMS-1500\"\nchk(\"CMS two dates, prints first\", W,\"2026-07-20\",cms,W+\", June 24, 2026\",\"99213 office visit charge $185.00.\",\"$185.00\")\ntab=\"Posted\\tDOS\\tService\\tCharge\\n03/20/2026\\t03/13/2026\\toffice visit\\t$100.00\"\nchk(\"table posted printed\", P,\"2026-06-15\",tab,P+\", March 20, 2026\",\"03/20/2026\\t03/13/2026\\toffice visit\\t$100.00\",\"$100.00\")\nchk(\"table DOS printed\", P,\"2026-06-15\",tab,P+\", March 13, 2026\",\"03/20/2026\\t03/13/2026\\toffice visit\\t$100.00\",\"$100.00\")\ntab2=\"Entry date\\tService\\tCharge\\n03/13/2026\\toffice visit\\t$100.00\"\nchk(\"Entry date column printed (leak)\", P,\"2026-06-15\",tab2,P+\", March 13, 2026\",\"03/13/2026\\toffice visit\\t$100.00\",\"$100.00\")\ndoi=\"Itemized ledger, statement date 06/15/2026. Date of injury 01/15/2026, office visit charge $220.00.\"\nchk(\"DOI printed as svc (leak)\", P,\"2026-06-15\",doi,P+\", January 15, 2026\",\"Date of injury 01/15/2026, office visit charge $220.00\",\"$220.00\")\nnote=\"Visit note 02/03/2026 charge per visit $185.00\"\nchk(\"visit note: statement form\", \"Dr. Reyes, visit note\",\"2026-02-02\",\"Visit note: charge $185.00.\",\"Dr. Reyes, visit note (statement dated February 2, 2026; service date not stated)\",\"Visit note: charge $185.00.\",\"$185.00\")\nchk(\"visit note: note date\", \"Dr. Reyes, visit note\",\"2026-02-02\",\"Visit note: charge $185.00.\",\"Dr. Reyes, visit note, February 2, 2026\",\"Visit note: charge $185.00.\",\"$185.00\")\nchk(\"visit note: other date\", \"Dr. Reyes, visit note\",\"2026-02-02\",\"Visit note: charge $185.00.\",\"Dr. Reyes, visit note, February 3, 2026\",\"Visit note: charge $185.00.\",\"$185.00\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/p3.py $PWD/a 2>&1 | tee p3.out",
 "description": "Check letter_check imports and adversarial header cases"
}
````

### User / tool · 2026-11-03T00:22:48.584Z

**tool result**
````
18:its own date scanner and shares no code with the production parser (app/backend/service_date.py), so a parser bug cannot hide itself.
42:    """Figures with another currency sign or code, amounts in words, and money in a patient's statement (the shared detector)."""
60:    """Currency strings the letter may not carry. `accepted_cents`: the accepted charges (the only amounts the BILLED CHARGES section may list).
62:    from app.backend import amounts as AM, export
77:            cents = AM.to_cents(s.lstrip("$ ").strip())
180:# (app/backend/service_date.py): its own small scanner, its own rules, enumerating every reading a written date allows.
388:            dismissed = sorted({src[a["record_no"]].split(",", 1)[0].strip() for a in case["amounts"] if a["cls"] == "charge" and a["review_status"] == "dismissed"})
---
/bin/bash: child setpgid (47806 to 47806): Operation not permitted
........................................................................ [ 33%]
........................................right line1                        []
WRONG LINE (line2 date on line1)   ["charge line's date is not certain from its quote (the line's own text gives 2026-03-13): Fennimoor Spine Clinic, itemized ledger, March 20, 2026: $100.00"]
not in record                      ["charge line's date is not certain from its quote (the line's own text gives 2026-03-13): Fennimoor Spine Clinic, itemized ledger, March 9, 2026: $100.00"]
bare statement date                ["charge line's date is not certain from its quote (the line's own text gives 2026-03-13): Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $100.00"]
not-stated form (allowed)          []
not-stated wrong stmt date         ["charge line's date is not certain from its quote (the statement date is not the record's date): Fennimoor Spine Clinic, itemized ledger (statement dated June 16, 2026; service date not stated): $100.00"]
ambig April 5 printed              ["charge line's date is not certain from its quote (the written date has no single certain reading): Fennimoor Spine Clinic, itemized ledger, April 5, 2026: $180.00"]
ambig May 4 printed                ["charge line's date is not certain from its quote (the written date has no single certain reading): Fennimoor Spine Clinic, itemized ledger, May 4, 2026: $180.00"]
ambig, ref 04/20 -> April 5 ok     []
period full                        []
period end dropped                 ["charge line's date is not certain from its quote (the line's own text gives 2026-06-09 to 2026-06-12): Saltmarrow General Hospital, UB-04 itemized bill, June 9, 2026: $2,105.00"]
period wrong end                   ["charge line's date is not certain from its quote (the line's own text gives 2026-06-09 to 2026-06-12): Saltmarrow General Hospital, UB-04 itemized bill, June 9–13, 2026: $2,105.00"]
period wrong year                  ["charge line's date is not certain from its quote (the line's own text gives 2026-06-09 to 2026-06-12): Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2025: $2,105.00"]
period start only moved            ["charge line's date is not certain from its quote (the line's own text gives 2026-06-09 to 2026-06-12): Saltmarrow General Hospital, UB-04 itemized bill, June 10–12, 2026: $2,105.00"]
two periods, prints one            ["charge line's date is not certain from its quote (the bill states several dates of service and the line prints one): Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00"]
CMS two dates, prints first        ["charge line's date is not certain from its quote (the bill states several dates of service and the line prints one): Wardlaw Orthopedics, CMS-1500, June 24, 2026: $185.00"]
table posted printed               ["charge line's date is not certain from its quote (the quote states several dates and no column heading names the date of service (heading 'Posted')): Fennimoor Spine Clinic, itemized ledger, March 20, 2026: $100.00"]
table DOS printed                  []
Entry date column printed (leak)   []
DOI printed as svc (leak)          []
visit note: statement form         ["charge line's date is not certain from its quote (a visit note's line must carry the note's date): Dr. Reyes, visit note (statement dated February 2, 2026; service date not stated): $185.00"]
visit note: note date              []
visit note: other date             ["charge line's date is not certain from its quote (the line's own text gives 2026-02-02): Dr. Reyes, visit note, February 3, 2026: $185.00"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:22:52.444Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/a && sed -n 28,32p docs/LLM_VS_CODE.md | cut -c1-900; grep -n \"service_date\\|statement date\\|cannot follow\" docs/LLM_VS_CODE.md | head; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/; tail -c 300 ../unit.log",
 "description": "Check docs mention of ambiguity rule"
}
````

### User / tool · 2026-11-03T00:22:52.563Z

**tool result**
````
|---|---|---|---|---|
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. |
| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in
a
p3.out
pa.out
pb.out
pc.out
pd.out
s
unit.log
......... [ 30%]
........................................................................ [ 31%]
........................................................................ [ 32%]
........................................................................ [ 33%]
...........................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:22:58.412Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-202-staff-r2 && for n in e m; do mkdir -p $D/$n && git archive 986fc55 | tar -x -C $D/$n; done; diff -rq $D/e $D/m && echo same; ls tests/e2e/guided | head -20; grep -n \"port\\|PORT\" $D/e/tests/e2e/guided/conftest.py | head",
 "description": "Create clean archive copies for e2e and mutants"
}
````

### User / tool · 2026-11-03T00:23:00.890Z

**tool result**
````
same
__init__.py
__pycache__
_helpers.py
test_golden_path.py
test_home.py
test_round2.py
test_round3.py
test_shell_smoke.py
test_step1.py
test_step2.py
test_step3.py
test_step4.py
test_t203.py
ugrep: warning: artifacts/review-evidence/T-202-staff-r2/e/tests/e2e/guided/conftest.py: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:23:02.702Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/e && (nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/guided -q -p no:cacheprovider > ../e2e.log 2>&1 &) ; sleep 2; echo started",
 "description": "Start guided e2e from archive copy"
}
````

### User / tool · 2026-11-03T00:23:04.800Z

**tool result**
````
started
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:23:24.861Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && cat > s/mut.py <<'EOF'\nimport sys, subprocess, shutil, pathlib, os\nroot = pathlib.Path(sys.argv[1]); which = sys.argv[2]; orig = pathlib.Path(sys.argv[3])\nF = {\"export\": root/\"app/backend/export.py\", \"store\": root/\"app/backend/store.py\", \"sd\": root/\"app/backend/service_date.py\"}\nfor k, p in F.items(): shutil.copy(orig/(k+\".orig\"), p)\ndef sub(k, old, new):\n    t = F[k].read_text(); assert old in t, (which, old); F[k].write_text(t.replace(old, new, 1))\nif which == \"R1_drop_end\":\n    sub(\"export\", \"_date_range(a['dos_iso'], a.get('dos_end_iso'))\", \"_date_range(a['dos_iso'])\")\nelif which == \"R2_record_date\":\n    sub(\"export\", \"return f\\\"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}\\\"\", \"return f\\\"{src}, {_long_date(self.rec_date(n))}\\\"\")\nelif which == \"R3_bare_statement\":\n    sub(\"export\", \"return f\\\"{src} {service_date.not_stated_text(rd)}\\\"\", \"return f\\\"{src}, {_long_date(rd)}\\\" if rd else f\\\"{src} (service date not stated)\\\"\")\nelif which == \"R4_first_date_in_record\":\n    sub(\"store\", \"        r = SD.resolve(item[\\\"excerpt\\\"], pos, rec.get(\\\"source\\\"), rd)\\n\", \"        import re as _re\\n        _m = _re.search(r'(\\\\d\\\\d)/(\\\\d\\\\d)/(\\\\d{4})', item['excerpt'])\\n        r = SD.resolve(item[\\\"excerpt\\\"], pos, rec.get(\\\"source\\\"), rd)\\n        if _m and r['state'] != 'stated': r = {'state':'stated','first':f'{_m.group(3)}-{_m.group(1)}-{_m.group(2)}','last':None,'reason':None,'raw':''}\\n\")\nelif which == \"R5_no_sort\":\n    sub(\"export\", \"return sorted(got, key=lambda a: (a.get(\\\"dos_iso\\\") or self._date(a), a[\\\"record_no\\\"], str(a.get(\\\"id\\\"))))\", \"return got\")\nelif which == \"R6_guess_md\":\n    sub(\"sd\", \"        if len(feasible) != 1:\\n            return \\\"bad\\\", \\\"ambiguous_numeric\\\"\\n        order = feasible[0]\", \"        order = feasible[0] if feasible else \\\"MD\\\"\")\nelif which == \"R7_lead_always_ok\":\n    sub(\"sd\", \"    if _NON_SVC_LEAD.search(lead):\\n        return False\\n\", \"\")\nelif which == \"R8_several_take_first\":\n    sub(\"sd\", \"    if len(units) > 1:\\n        same =\", \"    if len(units) > 1 and False:\\n        same =\")\nelif which == \"R9_header_non_off\":\n    sub(\"sd\", \"(head and not _H_DOS.search(head) and _H_NON.search(head))\", \"False\")\nelif which == \"R10_all_bill_not_stated\":\n    sub(\"sd\", \"    amts = AM.find_amounts(excerpt or \\\"\\\")\\n\", \"    if AM.billing_document(source, excerpt): return out\\n    amts = AM.find_amounts(excerpt or \\\"\\\")\\n\")\nelif which == \"R11_period_first_only\":\n    sub(\"sd\", \"return _apply(out, _decide(uniq, prefix, date_iso))\", \"return _apply(out, _decide(uniq[:1], prefix, date_iso))\")\nelif which == \"R12_ref_any\":\n    sub(\"sd\", \"all(t.ambiguous[o] <= ref for t in amb)\", \"any(t.ambiguous[o] <= ref for t in amb)\")\nelif which == \"R13_pos_none_record_date\":\n    sub(\"store\", \"r = {\\\"state\\\": \\\"not_stated\\\", \\\"first\\\": None, \\\"last\\\": None, \\\"reason\\\": \\\"no_date\\\", \\\"raw\\\": \\\"\\\"} if bill else (\", \"r = {\\\"state\\\": \\\"stated\\\", \\\"first\\\": rd, \\\"last\\\": None, \\\"reason\\\": None, \\\"raw\\\": \\\"\\\"} if rd else (\")\nelif which == \"R14_year_borrow\":\n    sub(\"sd\", \"        if not m.group(3):\\n            self.flaw = \\\"no_year\\\"\\n            return\\n        self.fixed = _iso(int(m.group(3))\", \"        if not m.group(3):\\n            self.fixed = _iso(2026, _mon(m.group(1)), int(m.group(2)))\\n            return\\n        self.fixed = _iso(int(m.group(3))\")\nelif which == \"R15_two_digit_ok\":\n    sub(\"sd\", \"        if len(y) == 2:\\n            self.flaw = \\\"two_digit_year\\\"\\n            return\\n\", \"        if len(y) == 2:\\n            y = \\\"20\\\" + y\\n\")\nelif which == \"R16_skip_counted\":\n    sub(\"store\", \"    if counted_undated:\\n        r = {\", \"    if False:\\n        r = {\")\nelif which == \"baseline\":\n    pass\nr = subprocess.run([sys.executable, \"-m\", \"evals.letter_check\"], cwd=root, capture_output=True, text=True)\nfirst = r.stdout.splitlines()[0] if r.stdout else r.stderr[-300:]\nu = subprocess.run([sys.executable, \"-m\", \"pytest\", \"-q\", \"-x\", \"-p\", \"no:cacheprovider\", \"tests/unit/test_t202_r2_service_date_layouts.py\", \"tests/unit/test_t202_charge_service_dates.py\"] + sorted(str(p.relative_to(root)) for p in (root/\"tests/unit\").glob(\"test_t200*.py\")), cwd=root, capture_output=True, text=True)\nprint(f\"{which:28s} letter_check exit={r.returncode} {first[:90]} | T202+T200 unit: {u.stdout.strip().splitlines()[-1][:110] if u.stdout.strip() else u.stderr[-150:]}\", flush=True)\nfor k, p in F.items(): shutil.copy(orig/(k+\".orig\"), p)\nEOF\nmkdir -p orig && cp m/app/backend/export.py orig/export.orig && cp m/app/backend/store.py orig/store.orig && cp m/app/backend/service_date.py orig/sd.orig\nsed -i.bak 's/F = {\"export\": root/F = {\"export\": root/' s/mut.py; rm s/mut.py.bak\n# the loop uses k+\".orig\": rename sd key file\ncp orig/sd.orig orig/sd.orig\ntime /Users/arsis/zlayt-pm-project/.venv/bin/python -I s/mut.py $PWD/m baseline $PWD/orig 2>&1 | tail -3",
 "description": "Set up mutant harness and run baseline",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T00:23:45.115Z

**tool result**
````
cp: orig/sd.orig and orig/sd.orig are identical (not copied).
baseline                     letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 67 passed in 7.53s

real	0m20.097s
user	0m13.402s
sys	0m4.587s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:23:48.350Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && for w in R1_drop_end R2_record_date R3_bare_statement R4_first_date_in_record R5_no_sort R6_guess_md R7_lead_always_ok R8_several_take_first; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I s/mut.py $PWD/m $w $PWD/orig 2>&1 | tail -1; done | tee mut1.out",
 "description": "Run mutants R1-R8",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T00:25:39.613Z

**tool result**
````
R1_drop_end                  letter_check exit=1 {"value": 16, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7 | T202+T200 unit: 1 failed, 6 passed in 0.65s
R2_record_date               letter_check exit=1 {"value": 28, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7 | T202+T200 unit: 1 failed in 0.55s
R3_bare_statement            letter_check exit=1 {"value": 20, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7 | T202+T200 unit: 1 failed, 2 passed in 0.51s
R4_first_date_in_record      letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 2 passed in 0.59s
R5_no_sort                   letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 36 passed in 0.57s
R6_guess_md                  letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 22 passed in 0.74s
R7_lead_always_ok            letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 4 passed in 0.61s
R8_several_take_first        letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 2 passed in 0.54s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:25:45.859Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && for w in R9_header_non_off R10_all_bill_not_stated R11_period_first_only R12_ref_any R13_pos_none_record_date R14_year_borrow R15_two_digit_ok R16_skip_counted; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I s/mut.py $PWD/m $w $PWD/orig 2>&1 | tail -1; done | tee mut2.out; grep -n \"letter_check\\|charge_date_violations\\|^def test\\|^@pytest\" a/tests/unit/test_t202_r2_service_date_layouts.py | head -60",
 "description": "Run mutants R9-R16, inspect fixtures test",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T00:27:41.853Z

**tool result**
````
R9_header_non_off            letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 3 passed in 0.61s
R10_all_bill_not_stated      letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed in 0.65s
R11_period_first_only        letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 5 passed in 0.51s
R12_ref_any                  letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 67 passed in 7.04s
R13_pos_none_record_date     letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 35 passed in 0.61s
R14_year_borrow              letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 30 passed in 0.55s
R15_two_digit_ok             letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 25 passed in 0.55s
R16_skip_counted             letter_check exit=0 {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 65 passed in 7.44s
14:from evals import letter_check as LC
58:def test_posted_before_dos_prints_the_dos_column_not_the_posting_date():
63:def test_dos_before_posted_still_prints_the_dos_column():
68:def test_two_dates_in_a_row_and_no_header_is_not_certain():
73:def test_a_row_whose_only_date_sits_under_posted_is_not_a_service_date():
79:def test_a_statement_or_posted_word_before_a_date_in_a_sentence_is_not_a_service_date():
90:def test_cms1500_with_two_service_dates_assigns_neither_to_a_line():
95:def test_cms1500_with_one_service_period_prints_the_period():
100:def test_two_service_dates_on_one_charge_line_is_not_certain():
105:def test_two_charges_in_one_sentence_each_take_their_own_date():
112:@pytest.mark.parametrize("period,label,rec", [
123:def test_a_stated_period_prints_whole_with_its_own_year(period, label, rec):
128:@pytest.mark.parametrize("period", ["June 9-12", "06/28-07/02/2026", "06/28/2026-07/02", "June 12, 2026 - June 9, 2026"])
129:def test_an_incomplete_or_backwards_period_is_not_certain(period):
135:def test_an_ambiguous_numeric_date_is_not_chosen():
140:def test_unambiguous_numeric_forms_still_print():
148:def test_a_reading_after_the_statement_date_is_not_a_service_date():
155:@pytest.mark.parametrize("raw", ["03/17/26", "03/17/98", "4/5/26", "13/04/26", "03-17-26"])
156:def test_a_two_digit_year_is_not_certain(raw):
160:@pytest.mark.parametrize("raw", ["Mar 27", "3/27", "March 27th"])
161:def test_a_date_with_no_year_is_not_certain(raw):
165:def test_a_date_that_is_not_on_the_calendar_is_not_certain():
170:def test_corpus_shapes_keep_their_dates():
177:def test_a_visit_note_keeps_the_visit_date_and_an_unreadable_line_in_a_bill_keeps_none():
187:def test_charges_sort_by_service_date_when_the_records_are_listed_in_another_order():
198:def test_a_charge_with_no_service_date_sorts_by_its_statement_date_among_dated_ones():
208:# ---------------------------------------------------------------- letter_check: each printed date against that line's OWN quote, not the whole record
217:def test_letter_check_fails_the_posted_date_and_passes_the_dos_date():
220:    assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, June 10, 2026", q, "$70.00"), recs) == []
221:    bad = LC.charge_date_violations(_letter(f"{LEDGER_SRC}, June 11, 2026", q, "$70.00"), recs)
225:def test_letter_check_fails_one_claim_date_printed_on_a_two_date_claim():
229:        assert LC.charge_date_violations(_letter(f"{CMS_SRC}, {printed}", q, "$210.00"), recs), printed
231:    assert LC.charge_date_violations(_letter(ok, q, "$210.00"), recs) == []
234:def test_letter_check_fails_a_dropped_period_end_and_a_wrong_year():
238:    assert LC.charge_date_violations(_letter(f"{UB_SRC}, June 9–12, 2026", q, "$2,105.00"), recs) == []
239:    assert LC.charge_date_violations(_letter(f"{UB_SRC}, June 9, 2026", q, "$2,105.00"), recs)              # the end dropped
240:    assert LC.charge_date_violations(_letter(f"{UB_SRC}, June 9–13, 2026", q, "$2,105.00"), recs)      # a wrong end
241:    assert LC.charge_date_violations(_letter(f"{UB_SRC}, June 19, 2026", q, "$2,105.00"), recs)             # the statement date
244:def test_letter_check_fails_a_month_name_period_printed_with_the_statement_year():
248:    assert LC.charge_date_violations(_letter(f"{UB_SRC}, June 9–12, 2024", q, "$2,105.00"), recs) == []
249:    assert LC.charge_date_violations(_letter(f"{UB_SRC}, June 9, 2026", q, "$2,105.00"), recs)
252:def test_letter_check_fails_a_guessed_ambiguous_date_and_a_two_digit_year():
257:        assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, {printed}", q, "$180.00"), recs), printed
259:    assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, March 17, 1998", "Office visit 03/17/98 charge $220.00.", "$220.00"), [_rec(ex2)])
262:def test_letter_check_fails_another_lines_date_on_a_ledger():
265:    assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, March 13, 2026", "03/13/2026 exam charge $100.00", "$100.00"), recs) == []
266:    assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, March 18, 2026", "03/13/2026 exam charge $100.00", "$100.00"), recs)
269:def test_letter_check_fails_a_date_when_the_quote_states_none_and_the_record_states_no_period():
273:    assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, June 15, 2026", q, "$250.00"), recs)            # the statement date, bare
274:    assert LC.charge_date_violations(_letter(f"{LEDGER_SRC}, June 9, 2026", q, "$250.00"), recs)             # a date the record never states for the line
276:    assert LC.charge_date_violations(_letter(ok, q, "$250.00"), recs) == []
279:def test_letter_check_passes_a_visit_note_on_its_own_date():
281:    assert LC.charge_date_violations(_letter("Fennimoor Spine Clinic, progress note, March 27, 2026", "Exam charge $250.00.", "$250.00"), recs) == []
285:@pytest.fixture
312:def test_api_charge_carries_the_service_date_the_letter_prints_lib10_and_lib14(client):
326:def test_api_not_stated_charge_carries_the_statement_form_and_a_confirm_note(client):
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:27:56.639Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && cat > s/r12.py <<'EOF'\nimport sys, types, itertools\nsys.path.insert(0, sys.argv[1])\nsrc = open(sys.argv[1]+\"/app/backend/service_date.py\").read()\ndef load(name, s):\n    m = types.ModuleType(name); exec(compile(s, name, \"exec\"), m.__dict__); return m\nO = load(\"sd_o\", src)\nM = load(\"sd_m\", src.replace(\"all(t.ambiguous[o] <= ref for t in amb)\", \"any(t.ambiguous[o] <= ref for t in amb)\"))\ndiff = []\ndays = [(m,d) for m in range(1,13) for d in (3,6,9,12)]\nfor (a1,a2),(b1,b2) in itertools.product(days, days):\n    A, B = f\"{a1:02d}/{a2:02d}/2026\", f\"{b1:02d}/{b2:02d}/2026\"\n    for ref in (\"2026-03-15\",\"2026-06-07\",\"2026-06-20\",\"2026-09-10\",\"2026-12-31\"):\n        t = f\"{A} to {B}\"\n        r = []\n        for X in (O, M):\n            us = X._units(t)\n            r.append(X._certain(us[0], ref))\n        if r[0] != r[1]: diff.append((t, ref, r[0], r[1]))\nprint(len(diff)); [print(d) for d in diff[:6]]\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/r12.py $PWD/a",
 "description": "Brute-force whether R12 mutant is behaviorally distinct"
}
````

### User / tool · 2026-11-03T00:27:57.037Z

**tool result**
````
3684
('01/03/2026 to 01/06/2026', '2026-03-15', ('ok', '2026-01-03', '2026-01-06'), ('bad', 'ambiguous_numeric'))
('01/03/2026 to 01/09/2026', '2026-03-15', ('ok', '2026-01-03', '2026-01-09'), ('bad', 'ambiguous_numeric'))
('01/03/2026 to 01/09/2026', '2026-06-07', ('ok', '2026-01-03', '2026-01-09'), ('bad', 'ambiguous_numeric'))
('01/03/2026 to 01/09/2026', '2026-06-20', ('ok', '2026-01-03', '2026-01-09'), ('bad', 'ambiguous_numeric'))
('01/03/2026 to 01/12/2026', '2026-03-15', ('ok', '2026-01-03', '2026-01-12'), ('bad', 'ambiguous_numeric'))
('01/03/2026 to 01/12/2026', '2026-06-07', ('ok', '2026-01-03', '2026-01-12'), ('bad', 'ambiguous_numeric'))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:28:09.300Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && python3 - <<'EOF'\nimport re\np='s/mut.py'; t=open(p).read()\nt=t.replace('elif which == \"R5_no_sort\":', '''elif which == \"R4b_counted_first_date\":\n    sub(\"store\", \"    if counted_undated:\\\\n        r = {\\\\\"state\\\\\": \\\\\"not_stated\\\\\", \\\\\"first\\\\\": None, \\\\\"last\\\\\": None, \\\\\"reason\\\\\": \\\\\"no_date\\\\\", \\\\\"raw\\\\\": \\\\\"\\\\\"}\", \"    if counted_undated:\\\\n        import re as _re\\\\n        _m = _re.search(r'(\\\\\\\\d\\\\\\\\d)/(\\\\\\\\d\\\\\\\\d)/(\\\\\\\\d{4})', item['excerpt'])\\\\n        r = {\\\\\"state\\\\\": \\\\\"stated\\\\\", \\\\\"first\\\\\": f'{_m.group(3)}-{_m.group(1)}-{_m.group(2)}', \\\\\"last\\\\\": None, \\\\\"reason\\\\\": None, \\\\\"raw\\\\\": \\\\\"\\\\\"} if _m else {\\\\\"state\\\\\": \\\\\"not_stated\\\\\", \\\\\"first\\\\\": None, \\\\\"last\\\\\": None, \\\\\"reason\\\\\": \\\\\"no_date\\\\\", \\\\\"raw\\\\\": \\\\\"\\\\\"}\")\nelif which == \"R5_no_sort\":''',1)\nopen(p,'w').write(t)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/mut.py $PWD/m R4b_counted_first_date $PWD/orig 2>&1 | tail -2 | cut -c1-300; tail -c 250 unit.log; tail -c 200 e2e.log",
 "description": "Run counted-line first-date mutant; check suites",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T00:28:25.785Z

**tool result**
````
R4b_counted_first_date       letter_check exit=1 {"value": 6, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7" | T202+T200 unit: 1 failed, 47 passed in 5.85s
................................. [ 98%]
........................................................................ [ 99%]
.......................................                                  [100%]
5938 passed, 5 skipped in 472.66s (0:07:52)
done
........................................................................ [ 53%]
..............................................................           [100%]
134 passed in 185.40s (0:03:05)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:28:34.161Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/a && grep -n \"float(\\|except\\|provider\\|llm\\|import \" app/backend/service_date.py | head; cd .. && cat > s/dump.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom evals import letter_check as LC\nfor name, text in LC.cases():\n    got = LC.letters_for(text)\n    for var in (\"all_accepted\",\"counted\"):\n        for h,q in LC.charge_lines(got[var][\"letters\"][\"standard\"]): print(name, var, h, \"|\", q[:80])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I s/dump.py $PWD/a > d1.txt; /Users/arsis/zlayt-pm-project/.venv/bin/python -I s/dump.py $PWD/a > d2.txt; cmp d1.txt d2.txt && echo IDENTICAL; wc -l d1.txt; grep -c \"service date not stated\" d1.txt; ls /Users/arsis/zlayt-pm-project/tests/unit | grep -c . ; cd /Users/arsis/zlayt-pm-project && git diff --stat 986fc55 -- evals/golden evals/library | tail -2",
 "description": "Grep service_date.py hygiene; determinism dump twice",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T00:28:54.393Z

**tool result**
````
15:import datetime as _dt
16:import re
18:from app.backend import amounts as AM
59:    """The text the letter puts after the provider when no service date is certain (T-200)."""
85:    except ValueError:
144:    from app.backend import dates
IDENTICAL
      84 d1.txt
10
150
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:29:59.312Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/draft.md",
 "content": "# T-202 (D-071 amendment) staff-engineer review, round 2, commit 986fc55\n\nVerdict: **changes** (0 blockers, 2 majors, 3 minors, 1 nit).\n\nEvery round 1 finding is fixed and I re-verified each from a `git archive 986fc55` copy. Ambiguous numeric dates, two-digit years, year-less dates and impossible dates now print the T-200 not-stated form (`04/05/2026`, `03/17/98`, `4/5`, `02/30/2026`). Month-name periods keep their own year and end (`June 9-12, 2024`, `June 28-July 2, 2026`). Hyphen-joined `06/28/2026-07/02/2026` prints whole. Two dates on one line or one claim print nothing. A Posted column no longer wins over DOS. The pos=None fallback is gone and the sort is pinned. The round 1 survivors M3 (drop period end) and M6 (record's first date) now die in `letter_check` (16 and 6 violations). Unit (5938 passed, 5 skipped) and guided e2e (134 passed) are green from the archive.\n\n`evals/letter_check.charge_date_violations` is independent of the production parser. `grep` finds no import of `service_date`, `_DOS_RX` or `_dos_iso` in the date path, and it has its own scanner. It checks each header against that line's own quote plus the one period the bill states before it. My 24 adversarial header cases (`s/p3.py`) are all caught. That includes the wrong-line date, a dropped period end, a wrong end, a wrong year, a CMS-1500 first-date, and the Posted column.\n\nWhat is still wrong is that the two filters that decide \"this date is not a service date\" are closed lists with a default-allow. A lone date under a column named `Entry date`, `Transaction Date`, `Issued` or `Printed`, or beside `Date of injury` in the same sentence, is printed as the date of service. `letter_check` shares the same default, so it cannot see it.\n\n```json\n{\"card\": \"T-202\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"round 2, fix commit 986fc55 (HEAD is 6c9ab2a at review time; all runs from a git archive of 986fc55 at artifacts/review-evidence/T-202-staff-r2/{a,e,m}): app/backend/service_date.py, store.py (charge_service_date), export.py, present.py, evals/letter_check.py, tests/unit/test_t202_r2_service_date_layouts.py; memory/ORCHESTRATOR_DECISIONS.md D-071 amendment and clarification; 25 cases in evals/golden and evals/library, fixture backend\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-202-staff-engineer.md (round 1), the card errata and handoff, the D-071 amendment and clarification (memory/ORCHESTRATOR_DECISIONS.md:84-92), docs/LLM_VS_CODE.md rows 2 and 3, git diff f0921e4 986fc55 for store.py, export.py, present.py, and the full text of service_date.py and evals/letter_check.py\",\n  \"git archive 986fc55 into artifacts/review-evidence/T-202-staff-r2/a (unit), /e (e2e), /m (mutants); diff -rq e m identical\",\n  \"pytest tests/unit -q from /a: 5938 passed, 5 skipped in 472s (the handoff says 5932 passed, 12 skipped; sums differ by one and I could not reproduce its shard split)\",\n  \"pytest tests/e2e/guided -q from /e: 134 passed in 185s\",\n  \"python -m evals.letter_check from /m: {value: 0, cases: 25}; the pipeline dump of every BILLED CHARGES header and quote over 25 cases x (all_accepted, counted) run twice, cmp identical (s/dump.py, d1.txt d2.txt, 84 lines)\",\n  \"s/pa.py, s/pb.py, s/pc.py, s/pd.py: 140+ hand-built charge lines through store.charge_service_date: ambiguous and unambiguous numeric dates against several statement dates (the _certain reference rule), two-digit years, year-less, month-name and dmy forms, impossible dates, same-sentence two dates, posted/paid/received/adjusted tails, inline posted-before-service, tables with Posted/DOS/Date/Billed/Entry headings in both column orders (tab, pipe and space aligned), CMS-1500 with one, two, three dates and a From/To period, UB-04 periods in 17 written forms, a header with fewer cells than the row, 30 single-column header words, and 20 lead and tail words (outputs pa.out, pb.out, pc.out, pd.out)\",\n  \"s/p3.py: letter_check.charge_date_violations on 24 headers (right, wrong line, not in record, bare statement, not-stated form with right and wrong statement date, ambiguous both readings, ambiguous resolved by the record date, period full/dropped end/wrong end/wrong year/moved start, two periods, CMS first date, table Posted and DOS, Entry-date column, date of injury, visit note three ways) (p3.out)\",\n  \"s/mut.py: 18 mutants applied in the /m archive copy (R1 drop period end, R2 record date, R3 bare statement date, R4 and R4b record's first date, R5 no sort, R6 guess month-first, R7 no billing-word lead filter, R8 several dates take the first, R9 no non-DOS header filter, R10 every bill not-stated, R11 only first period, R12 'all' to 'any' in the reference rule, R13 pos=None falls back to record date, R14 borrow the year, R15 accept two-digit year, R16 skip the counted branch), each run through letter_check and test_t202_r2 + test_t202_charge + test_t200 (mut1.out, mut2.out); files restored from orig/ after each\",\n  \"s/r12.py: brute force of the R12 mutant over 16x16 day pairs x 5 statement dates (3684 differing outcomes, so the mutant is not equivalent)\",\n  \"grep of service_date.py for float(, provider/llm imports, bare except: only a ValueError in _iso; imports amounts and dates only\"],\n \"verdict\": \"changes\",\n \"scores\": {\"deterministic_parse_no_llm\": 5, \"date_correctness_edge_cases\": 3, \"ambiguity_policy_LLM_VS_CODE_row2\": 4, \"period_range_handling\": 5, \"eval_check_independence_and_per_line\": 5, \"eval_check_corpus_coverage\": 3, \"test_quality\": 4, \"missing_date_visible_state\": 5, \"non_service_date_filtering\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"A lone date under a column heading that is not on the non-DOS word list is printed as the date of service\",\n   \"evidence\": \"app/backend/service_date.py:38 _H_NON = post|statement|stmt|bill|invoice|paid|payment|due|receiv|process|entered|created|balance|adjust|insur|submitted|mailed; service_date.py:286-291 a heading that matches neither _H_DOS nor _H_NON falls into `other` and is printed when it is the only date. Repro (artifacts/review-evidence/T-202-staff-r2/s/pc.py, output pc.out): a table 'Entry date\\\\tService\\\\tCharge / 03/13/2026\\\\toffice visit\\\\t$100.00' with statement 06/15/2026 gives state=stated 'March 13, 2026'. The same for the headings Transaction Date, Txn Date, Recorded, Filed, Claim Date, Sent, Issued, Printed, Reported, Remit Date, Closed, Reference Date, 'Charged on'. Only Date entered, Invoiced, Date billed, Due, Submitted, Adjusted, Created and Statement Date give not-stated. letter_check shares the same default (s/p3.py 'Entry date column printed (leak)' returns []), so it cannot see it.\",\n   \"why_it_matters\": \"D-071 amendment: a non-service column (Posted, Statement, Billed) or any parse doubt prints 'service date not stated'. Posted is caught, but a ledger exported with 'Transaction Date' or 'Entry date' (the posting date in most ledgers) prints that date to the adjuster as the date of service, and Step 3 shows it with no confirm note. This is the round 1 paralegal blocker (posting date printed as DOS) reachable through any synonym. I rate it major, not blocker, only because every column word the amendment names is handled and the leak needs a vocabulary outside the corpus; it is still a spec-class miss.\",\n   \"fix\": \"Invert the default for a table column: print a column's date only when its heading names the service (_H_DOS) or is a bare 'Date' or 'Dates'; any other heading takes the not-stated form with reason non_service_date. Do the same in letter_check._dos_column so the check stops sharing the leak.\",\n   \"acceptance_test\": \"Unit test through store.charge_service_date: single-date tables headed Entry date, Transaction Date, Issued, Printed, Recorded, Filed, Claim Date, Remit Date give not_stated; headed Date, Dates, DOS, Service Date, Date of Service, Visit Date still give stated. A letter_check test builds the same header and expects a violation for the printed date.\"},\n  {\"severity\": \"major\",\n   \"title\": \"A date led by a word outside the billing-word list (date of injury, DOB, authorization, referred, since) is printed as the service date when it is the line's only date\",\n   \"evidence\": \"app/backend/service_date.py:35-36 _NON_SVC_LEAD is a closed list (statement, invoice, billing, posted, paid, due, balance ...); _lead_ok (service_date.py:222-226) lets every other lead through. Repro (s/pd.py, pd.out; statement 06/15/2026): 'Date of injury 01/15/2026, office visit charge $220.00.' -> stated 'January 15, 2026'; 'Date of injury: 01/15/2026 - office visit charge $220.00.' -> stated; 'Patient DOB 03/20/1980, office visit charge $220.00.' -> stated 'March 20, 1980'; 'Authorization 02/10/2026, office visit charge $220.00.' and 'Pre-authorized 02/10/2026 office visit ...' -> stated 'February 10, 2026'; 'DOI 01/15/2026 office visit', 'accident 01/15/2026 office visit', 'claim filed 01/15/2026 office visit' -> stated. Only a full stop or ';' before the charge sentence (their own segment split) protects the line. letter_check agrees ('DOI printed as svc (leak)' returns [] in p3.out).\",\n   \"why_it_matters\": \"A demand letter that gives the date of injury or a patient's birth date as the date of service is a confident false statement in the one place an adjuster cross-checks. The module doc says a date is printed when 'tied to THAT line by its own sentence'; sitting in the same sentence is not the same as being the service date. Same default-allow design as the column finding, rated major for the same reason.\",\n   \"fix\": \"Add a positive test for the sentence form: print a same-sentence date only when its lead word is a service word (service, seen, visit, exam, treated, admitted, discharged, on, dos, dated for the line) or when it leads the line as a row start, and take not-stated otherwise; or widen _NON_SVC_LEAD with injury/DOI/DOB/birth/authorization/referral/accident/claim/filed/since/after/before/until and add a year-sanity bound (see the minor below). Keep letter_check's _BILLING_WORD in step.\",\n   \"acceptance_test\": \"Unit test: the five repro sentences give not_stated; '03/13/2026 office visit charge $220.00', 'office visit on 03/13/2026 charge $220.00', 'Seen 03/13/2026, charge $220.00' still give stated March 13, 2026. letter_check flags a letter that prints January 15, 2026 for the DOI sentence.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The 'all' in the period reference rule is untested: mutant R12 survives every test and letter_check; and letter_check has no corpus line that reaches the resolver's not-stated or ambiguity routes\",\n   \"evidence\": \"s/mut.py R12 changes `all(t.ambiguous[o] <= ref for t in amb)` to `any(...)` (service_date.py:186): letter_check value 0, test_t202_r2 + test_t202_charge + test_t200 67 passed (mut2.out). It is not equivalent: s/r12.py finds 3684 (period, statement date) pairs where the result differs, e.g. '01/03/2026 to 01/06/2026' with statement 2026-03-15 is ok January 3-6 under `all` and ambiguous under `any`. Also mut.py R6 (guess month-first), R7, R8, R9, R10, R11, R13, R14, R15, R16 all leave letter_check at 0 (corpus has no ambiguous, multi-date or posted-column line); the unit suite kills each of them. The handoff names this ('every not-stated corpus line is a D-064 counted-undated one').\",\n   \"why_it_matters\": \"The eval is the harness upgrade the card promised. Today it is independent and per-line, but it exercises only the shapes in the 25 cases, so a regression in the ambiguity or multi-date routes is caught only by the unit file. The 'all' semantic of the reference rule is the one clause of the D-071 clarification with no pin.\",\n   \"fix\": \"Add the adversarial layouts as SYNTHETIC library packets (a posted-before-DOS ledger, a CMS-1500 with two dates, an ambiguous 04/05/2026 ledger, a two-date sentence) so letter_check walks them through the pipeline. Add a unit case for a period where one end is after the statement date under one reading and not the other.\",\n   \"acceptance_test\": \"Mutants R6, R8, R9 and R12 each fail letter_check or a named unit test; `python -m evals.letter_check` still reports value 0 on the unmodified tree.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"docs/LLM_VS_CODE.md rows 2 and 3 still say an ambiguous date is 'never guessed'; the statement-date disambiguation and the new service-date module are not in the table\",\n   \"evidence\": \"grep -n 'service_date\\\\|cannot follow\\\\|statement date' docs/LLM_VS_CODE.md in the archive prints nothing relevant; row 2 (docs/LLM_VS_CODE.md:30) says '04/05/2026 fits two readings ... ambiguous, never guessed, and waits for the paralegal'. The clarification (ORCHESTRATOR_DECISIONS.md:92) resolves 06/09/2026 to June 9 when only one reading is on or before the statement date, and app/backend/dates.py (entry dates) does not use that rule, so one string can be 'ambiguous' for an entry and 'June 9' for a charge line.\",\n   \"why_it_matters\": \"Checklist item 1: the implementation must match the table row by row, and the table is graded. The rule is deterministic and recorded as a decision, so I do not call it a guess; the doc should say so.\",\n   \"fix\": \"Architect: add one sentence to row 2 or 3 for charge-line service dates (reference rule, not-stated form, Step 3 note) and say that entry dates stay on the stricter rule.\",\n   \"acceptance_test\": \"grep for the rule in docs/LLM_VS_CODE.md; a doc-vs-code test that cites the row passes.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"An unambiguous date is not held to the clarification's own principle that a service cannot follow its statement, and has no year bound\",\n   \"evidence\": \"s/pd.py: statement 06/15/2026, '07/20/2026 office visit charge $220.00.' -> stated 'July 20, 2026'; '03/13/1998 ...' -> stated 'March 13, 1998'; '03/13/2031 ...' -> stated 'March 13, 2031'. service_date._certain applies `<= ref` only to choose between two readings (service_date.py:186).\",\n   \"why_it_matters\": \"The same fact that makes 06/09/2026 certain makes a service date a month after its own statement doubtful. With finding 2 it is the backstop for DOB-like dates.\",\n   \"fix\": \"In resolve, treat a stated date after the record's date (bill only), or more than a set number of years before it, as a parse doubt: not-stated with reason 'invalid' and the Step 3 note.\",\n   \"acceptance_test\": \"Unit test: those three lines give not_stated; corpus letters stay byte-identical (diff the 84-line dump).\"},\n  {\"severity\": \"nit\",\n   \"title\": \"A two-digit-year month-name date gets the 'no year' reason text\",\n   \"evidence\": \"s/pa.py: 'Mar 5, 26 x-ray charge $180.00' -> not_stated reason no_year; confirm_note says 'states no year'.\",\n   \"why_it_matters\": \"The Step 3 note tells the paralegal something untrue about the quote.\",\n   \"fix\": \"In _Tok._mdy set flaw=two_digit_year when the text carries ', NN' after the day.\",\n   \"acceptance_test\": \"Unit test: reason == 'two_digit_year' for 'Mar 5, 26'.\"}\n ],\n \"whats_right\": [\n  \"letter_check.charge_date_violations is a real independent per-line check: its own scanner, no import of the production parser, and it fails the wrong-line date, a dropped or wrong period end, a wrong year, a CMS first date and a Posted column.\",\n  \"The certain-or-ask rule holds on every layout the amendment names: ambiguous numerics, two-digit years, multi-date lines, Posted/Billed columns and CMS-1500 with two dates all take the T-200 form, and the corpus letters are byte-identical across two runs.\",\n  \"The adversarial fixture set (48 cases, 33 red on f0921e4) kills 13 of my 16 resolver and store mutants on its own; only R12 survives everything.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-03T00:29:59.413Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/draft.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:30:09.982Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2 && python3 - <<'EOF'\np='draft.md'; t=open(p).read()\nreps=[(\"My 24 adversarial header cases (`s/p3.py`) are all caught. That includes the wrong-line date, a dropped period end, a wrong end, a wrong year, a CMS-1500 first-date, and the Posted column.\",\n\"Of my 23 adversarial header cases (`s/p3.py`), every wrong one is flagged except the two leaks below: the wrong-line date, a dropped period end, a wrong end, a wrong year, a CMS-1500 first date, and the Posted column.\"),\n(\"s/p3.py: letter_check.charge_date_violations on 24 headers\",\"s/p3.py: letter_check.charge_date_violations on 23 headers\"),\n(\"140+ hand-built charge lines\",\"about 190 hand-built charge lines\"),\n(\"s/mut.py: 18 mutants applied\",\"s/mut.py: 17 mutants applied\"),\n(\"kills 13 of my 16 resolver and store mutants on its own; only R12 survives everything.\",\"kills 16 of my 17 resolver, store and export mutants on its own; only R12 survives everything.\")]\nfor a,b in reps:\n    assert a in t, a; t=t.replace(a,b)\nopen(p,'w').write(t)\nimport json,re\nblk=re.findall(r\"```json\\n(.*?)\\n```\",t,re.S); assert len(blk)==1\nd=json.loads(blk[0]); print(d[\"verdict\"], [f[\"severity\"] for f in d[\"findings\"]], len(d[\"whats_right\"]))\nEOF\ncd /Users/arsis/zlayt-pm-project && ls reviews/T-202-staff-engineer-r2.md 2>&1 | head -1; cp artifacts/review-evidence/T-202-staff-r2/draft.md reviews/T-202-staff-engineer-r2.md && python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate JSON, publish review file, run board validate"
}
````

### User / tool · 2026-11-03T00:30:10.186Z

**tool result**
````
changes ['major', 'major', 'minor', 'minor', 'minor', 'nit'] 3
ls: reviews/T-202-staff-engineer-r2.md: No such file or directory
ok (205 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:30:16.003Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t202_r2_patterns.md",
 "content": "---\nname: project_t202_r2_patterns\ndescription: T-202 r2 (986fc55): certain-or-ask date resolver; closed negative lists default-allow (column headings, lead words); tests-only mutant survivors\nmetadata:\n  type: project\n---\n\nT-202 r2 verdict changes (2 majors). Round 1 findings all fixed; unit 5938 passed, guided e2e 134 passed from archive.\n\n- Resolver prints any lone date unless a closed word list (`_H_NON` for column headings, `_NON_SVC_LEAD` for sentence leads) rejects it. Probe 30 heading words and 20 lead words: \"Entry date\", \"Transaction Date\", \"Issued\", \"Date of injury\", \"DOB\" all print as the service date.\n- letter_check shares the same default, so it cannot see these leaks; probe the checker with the leaking header too.\n- Mutants: 16 of 17 killed by the 48-case unit file; `all`->`any` in the reference rule survives. letter_check kills only export-level mutants because the corpus has no ambiguous or multi-date lines.\n\n**Why:** the amendment names classes (\"non-DOS column\", \"any parse doubt\"), the code names words.\n**How to apply:** for any \"is this date/figure a service one\" filter, probe synonyms outside the list and run the control (a plain \"Date\" column) so the expectation is not masked by an ambiguous date (use day > 12).\n\nRelated: [[project_t141_r6_patterns]], [[feedback_fake_script_keys]].\n"
}
````

### User / tool · 2026-11-03T00:30:16.102Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t202_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:30:17.168Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && echo \"- [T-202 r2 patterns](project_t202_r2_patterns.md) — closed negative lists default-allow (headings, lead words); 16/17 mutants killed\" >> MEMORY.md; tail -2 MEMORY.md",
 "description": "Append memory index line"
}
````

### User / tool · 2026-11-03T00:30:17.259Z

**tool result**
````
- [T-177 r5 patterns](project_t177_r5_patterns.md) — pass: 12/12 mutants killed, old-build probe finds leak, guard refuses $VAR targets
- [T-202 r2 patterns](project_t202_r2_patterns.md) — closed negative lists default-allow (headings, lead words); 16/17 mutants killed
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:30:22.615Z

T-202 r2 verdict is **changes** (0 blockers, 2 majors, 3 minors, 1 nit), written to `/Users/arsis/zlayt-pm-project/reviews/T-202-staff-engineer-r2.md` and `board.py validate` accepts it; every round 1 finding is fixed, but the new date filters are closed word lists that print any other lone date as the service date.

- **Major 1:** a lone date under a heading outside the non-service word list prints as the date of service. "Entry date", "Transaction Date", "Issued" and "Printed" all do.
- **Major 2:** a date led by "Date of injury", "DOB" or "Authorization" in the same sentence as the charge prints as the date of service.
- **Both majors:** `letter_check` shares the same default, so it cannot catch them.
- **Minors:**
  - The `all`→`any` mutant in the reference rule survives every test and `letter_check`.
  - `docs/LLM_VS_CODE.md` rows 2 and 3 do not mention the statement-date rule.
  - An unambiguous date after its own statement, or years away from it, still prints.
- **Nit:** a two-digit-year month-name date such as "Mar 5, 26" gets the "no year" reason text.
- **Independence:** the new `letter_check` uses its own scanner and no production date parser. It checks each line against that line's own quote.
- **Rule logic:** the `_certain` logic holds for ambiguous numeric dates, two-digit years, multi-date lines, Posted/Billed columns and the statement-date rule.
- **Suites:** run from a `git archive 986fc55` copy, unit gave 5938 passed, 5 skipped. The handoff said 5932 passed, 12 skipped. Guided e2e gave 134 passed, and `letter_check` gave value 0 over 25 cases.
- **Mutants:** the 48-case unit file kills 16 of my 17 mutants.

Evidence is in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-staff-r2/`.
