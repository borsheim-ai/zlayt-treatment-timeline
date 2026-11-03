# Subagent: Staff r2: T-207 doc rows (Staff r2: T-207 doc rows)

Source: `agent-a08438dab4d79eb7d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T02:01:02.341Z

Re-check T-207, round 2, in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. The fix commit is efda639; read reviews/T-207-staff-engineer.md (round 1, 5 majors).

Confirm that every statement in rows 2 and 3 of docs/LLM_VS_CODE.md matches the code at 8cb5bd2: app/backend/service_date.py, encounter_types.json and export.py. The doc states the five-year bound as 1,830 days, which is what the code does. Judge whether stating it accurately is enough. Write reviews/T-207-staff-engineer-r2.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:03.615Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-03T02:01:03.625Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:03.992Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer.md"
}
````

### User / tool · 2026-11-03T02:01:03.998Z

**tool result**
````
1	# T-207 staff-engineer review, r1
2	
3	Reviewer: staff-engineer-reviewer (Marcus Lee persona). Fresh context, read-only on product code. Pinned to HEAD fc37fbc (archived to a scratch copy; the product tree was not edited).
4	
5	Scope: docs/LLM_VS_CODE.md rows 2 and 3 (commits 901ad5a and fc37fbc), checked against app/backend/service_date.py, app/backend/store.py charge_service_date (lines 118-147) and app/backend/export.py charge_when (lines 215-226). Rules: memory/ORCHESTRATOR_DECISIONS.md D-071 and its amendment, clarification and addendum (lines 84-93). Spec: spec/REQUIREMENTS.md R-TL-3 (lines 50 and 356).
6	
7	## Answers to the four questions
8	
9	1. The date is code only, never the LLM. Holds. service_date.py imports only datetime, re and app.backend.amounts (lines 22-25). The charge path (store.py:118-147, export.py:215-226, present.py:152) calls no model. evals/letter_check.py has its own scanner and does not import service_date.
10	2. An allow-list of positive evidence decides it. Holds for the four listed ties, with gaps. The row's column-header list is narrower than the code (F6). Two other paths decide a printed date that row 2 does not name: a same-period locale rule (F1) and the header date of a visit note (F3).
11	3. The statement-date disambiguation rule applies. Holds. A date that reads two ways is blank when both readings fall on or before the statement (probe P1), and a single reading is printed when the other is after it (probe P2). Mutants M1 and M2 are killed.
12	4. A not-certain case gets the fillable blank plus a Step 3 note. The blank holds: it matches the D-071 addendum text (probe P7). The note holds except for counted undated charges (F4), and its wording for the no-label case differs from row 3 (F7).
13	
14	Verdict: changes. No blocker. Five majors, three minors. I did not downgrade any finding for convenience.
15	
16	Model note: the dossier and the brief expect claude-sonnet-5-5. The model I am running as is claude-haiku-5-5, and that is the id recorded below.
17	
18	## Exercised
19	
20	1. git show 901ad5a and git show fc37fbc: each changes only docs/LLM_VS_CODE.md (2 lines and 1 line). git rev-parse HEAD gives fc37fbcec0ebdb7705e4d91c2ad43afd67a82568. git diff --stat HEAD -- docs/LLM_VS_CODE.md is empty, so the working copy matches HEAD.
21	2. git archive HEAD into a scratch copy at the pinned sha (read and run only).
22	3. Read rows 2 and 3 at HEAD (docs/LLM_VS_CODE.md:30-31), the D-071 block (memory/ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (spec/REQUIREMENTS.md:50, :356), and board.py show T-207 (reviews: []; commits 901ad5a, fc37fbc).
23	4. Read app/backend/service_date.py in full (377 lines) at HEAD. Grepped the dos_iso and dos_text writers, and the import lines of the date path.
24	5. pytest tests/unit -q on the HEAD archive: 6137 passed, 12 skipped (428 s).
25	6. pytest on the four T-202 date files (test_t202_r3_allow_list, test_t202_r2_service_date_layouts, test_t202_charge_service_dates, test_t200_undated_charge_label): 211 passed.
26	7. Probes P1 to P8 against the HEAD archive: artifacts/review-evidence/T-207-r1/probe_t207.py with probe_t207.out, and probe_t207_p8.py with probe_t207_p8.out.
27	8. Nine mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py with mutants_t207.out. Baseline 211 passed. M1, M2, M3, M5, M7 and M9 killed; M4, M6 and M8 survived.
28	9. letter-check eval (evals/letter_check.py main, fixture backend): artifacts/review-evidence/T-207-r1/letter_eval_t207.py with letter_eval_t207.out. Output: value 0, cases 25, exit 0.
29	10. grep -rn -i mutant tests/unit evals --include=*.py: 28 hits, all comments from other cards. None is a harness for the date resolver's 24 mutants.
30	
31	## Findings
32	
33	F1 (major). Row 2 says a two-reading date is certain "only when" the statement rule decides it. The code also settles an end from the other end's order inside the same period. Probe P3, input "DOS 04/05/2026 - 13/05/2026 therapy $120.00." with statement 2026-06-30, prints "stated | 2026-05-04 | 2026-05-13". The row says that case is ambiguous and prints the blank. The code path is service_date.py:215-217 (if determined: order = next(iter(determined))). It is pinned by tests/unit/test_t202_r2_service_date_layouts.py:129 (mutant M3 is killed by it). D-071's amendment (memory/ORCHESTRATOR_DECISIONS.md:87) mentions "no locale rule from the record", so a locale rule is contemplated, but the table does not state it. Not a blocker: the rule is deterministic, tested, and uses the record's own other end.
34	
35	F2 (major). Row 2 says a bill date "more than five years before it is not read". The code allows 1830 days (service_date.py:55 _YEARS_BEFORE = 5; :274 days=366 * _YEARS_BEFORE). Probe P4 with statement 2026-06-30: "P4 06/29/2021 | $120.00 | stated | 2021-06-29" (five years and one day before) and "P4 06/26/2021 | $120.00 | stated | 2021-06-26" (five years and four days before). The day 06/25/2021 is refused as implausible. Mutant M4 (calendar-exact bound 365*5+1) survives all 211 tests. The only bound tests are 1998 and 2031 (tests/unit/test_t202_r3_allow_list.py:187-188). Persona calibration: a missing boundary test is major.
36	
37	F3 (major). A charge with no labeled service date takes the visit note's header date. Probe P5: "Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain." on a progress note dated 2026-01-09 prints "stated | 2026-01-09 | text='January 9, 2026'". Probe P8 shows the same default when the figure offset cannot be located (store.py:133-136 falls back to the header date for a non-bill record; a ledger prints the blank). The default is at service_date.py:375-376 and is pinned by test_t202_r3_allow_list.py:98 (mutant M7 killed). Row 2 says "Only a date tied to the line by" four listed ties counts, and row 3 says the header date is not the DOS "for a bill". Spec R-TL-3 (spec/REQUIREMENTS.md:50) says "Date of service is the record's header date, parsed by code", so the code follows the spec and the table is incomplete. Persona §5 would treat a silent default as a blocker. I do not rate it one because the spec authorizes the header date, no fact is invented, and nothing is hidden. The defect is that the table says otherwise. Chris must rule (Q1).
38	
39	F4 (major). A counted undated charge gets no Step 3 note. Probe P6, counted via D-064 ("Count this charge"), prints "not_stated | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None". The uncounted line (P6-uncounted) gets a note. The suppression is store.py:139 (if not stated and not counted_undated:), and mutant M6 survives. Row 3 (docs/LLM_VS_CODE.md:31) says "Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it". The brief also requires a note for every not-certain case. The blank still prints in the letter, so nothing is invented or lost. Major, not blocker.
40	
41	F5 (major). The row 3 Validation cell says "24 mutants of the resolver and the check all fail the unit suite" (docs/LLM_VS_CODE.md:31). Two resolver mutants survive the 211-test date suite: M4 (five-year bound, service_date.py:274) and M8 (the "Encounter date" heading, service_date.py:53). The count of 24 cannot be reproduced: no harness exists in the repo (item 10 above). The claim is refuted, so it is a finding.
42	
43	F6 (minor). Row 2 lists "a DOS or service column header". The code's heading set (service_date.py:53-54) also accepts Visit Date, Date of Visit, Encounter Date, SVC and 24A. Encounter Date has no test (M8 survives). Fix: list the set in row 2 and test it.
44	
45	F7 (minor). Row 3 says the note asks the paralegal to "read the date from the quote" and "names the date as the quote writes it". That holds for the written-date reasons (service_date.py:102). For the no-label reason the note says "Request a dated itemized bill, or fill the blank from the record" and names no date (service_date.py:103; probe P7b). Fix: align the row or the note.
46	
47	F8 (minor). billing.py:141 (_dos, via dates.parse_date) and billing.py:339 emit a per-line dos_iso served at GET /api/cases/{token}/billing (billing.py:1062, registered at api.py:599). This is a second date-of-service derivation outside row 2's "only" claim. It does not reach the letter (dos_iso writers listed in item 4) and I found no frontend consumer. Fix: say in row 2 that it is not a charge date, or remove it.
48	
49	## What is right
50	
51	1. The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.
52	2. The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.
53	3. The blank matches the D-071 addendum text exactly ("date of service [__________] (statement dated June 30, 2026)", probe P7), and letter_check reports value 0 over 25 cases.
54	
55	Outside my lens: the wording of Step 3 UI copy beyond the note strings, and the legal weight of the blank.
56	
57	```json
58	{"card": "T-207", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
59	 "scope": "docs/LLM_VS_CODE.md rows 2-3 at HEAD fc37fbc (commits 901ad5a, fc37fbc); app/backend/service_date.py, app/backend/store.py:118-147, app/backend/export.py:215-226; memory/ORCHESTRATOR_DECISIONS.md D-071 lines 84-93; spec/REQUIREMENTS.md R-TL-3; no app URL exercised",
60	 "exercised": ["git show 901ad5a and fc37fbc (docs only); git rev-parse HEAD = fc37fbcec0eb; git diff --stat HEAD -- docs/LLM_VS_CODE.md empty",
61	               "git archive HEAD into scratch copy head-fc37fbc (pinned, read and run only)",
62	               "read rows 2-3 (docs/LLM_VS_CODE.md:30-31), D-071 block (ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (REQUIREMENTS.md:50, 356), board.py show T-207",
63	               "read service_date.py in full (377 lines) at HEAD; store.py:118-147; export.py:215-226; grep dos_iso writers and date-path imports",
64	               "pytest tests/unit -q at HEAD archive: 6137 passed, 12 skipped",
65	               "pytest on 4 T-202 date files: 211 passed",
66	               "probes P1-P8: artifacts/review-evidence/T-207-r1/probe_t207.py (+.out), probe_t207_p8.py (+.out)",
67	               "9 mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py (+.out); M4, M6, M8 survived; M1 M2 M3 M5 M7 M9 killed",
68	               "letter_check eval via letter_eval_t207.py (+.out): value 0, 25 cases, exit 0",
69	               "grep -rn -i mutant tests/unit evals: 28 comment hits, no 24-mutant harness"],
70	 "verdict": "changes",
71	 "scores": {"row2_matches_code": 3, "row3_matches_code": 3, "date_is_code_only": 5, "allow_list_decides": 3, "statement_date_rule": 4, "not_certain_blank_and_note": 3, "tests_and_validation_claims": 2},
72	 "findings": [
73	  {"severity": "major", "title": "Row 2 says a two-reading date is certain only by the statement rule; code also settles it from the other end of the same period",
74	   "evidence": "probe_t207.out line 'P3 | $120.00 | stated | 2026-05-04 | 2026-05-13' for 'DOS 04/05/2026 - 13/05/2026 therapy $120.00.' (statement 2026-06-30); app/backend/service_date.py:215-217 'if determined: order = next(iter(determined))'; docs/LLM_VS_CODE.md:30 'it is certain only when a reading after the bill's own (statement) date is impossible'; tests/unit/test_t202_r2_service_date_layouts.py:129 kills M3",
75	   "why_it_matters": "The table is the binding description of how a printed date is decided. It says the statement rule is the only resolver; the code and a tested test use a second rule. D-071's amendment contemplates a record-level locale rule, but the table does not state one.",
76	   "fix": "Architect amends row 2 to state the same-period locale rule (cite D-071 amendment 'no locale rule from the record'), or the code drops the rule and the period prints the blank.",
77	   "acceptance_test": "Row 2 names the rule the code applies; a test pins '04/05/2026 - 13/05/2026' to the decided answer; mutant M3 stays killed."},
78	  {"severity": "major", "title": "Five-year bound is 1830 days, not 'more than five years'; no test sits at the boundary",
79	   "evidence": "app/backend/service_date.py:55 '_YEARS_BEFORE = 5'; :274 'days=366 * _YEARS_BEFORE'; probe_t207.out 'P4 06/29/2021 | $120.00 | stated | 2021-06-29' (5y+1d before 2026-06-30) and 'P4 06/26/2021 | $120.00 | stated | 2021-06-26'; mutants_t207.out 'M4 ... SURVIVED | exit=0 | 211 passed'; tests only at 1998/2031 (tests/unit/test_t202_r3_allow_list.py:187-188); docs/LLM_VS_CODE.md:30 'more than five years before it is not read'",
80	   "why_it_matters": "A service date 5y+1d to 5y+4d before the statement is printed as a date of service though row 2 says it is not read. No test would catch it. Persona calibration: missing boundary test is major.",
81	   "fix": "Compare calendar years (statement date minus five years, same month and day, 29 Feb handled) instead of 366-day arithmetic; keep 1998 and 2031.",
82	   "acceptance_test": "Statement 2026-06-30: 06/29/2021 prints the blank with reason implausible; 06/30/2021 is stated; M4 is killed."},
83	  {"severity": "major", "title": "A charge with no labeled date takes the visit note's header date; row 2 says only the allow-list counts",
84	   "evidence": "probe_t207.out 'P5-store | $240.00 | stated | 2026-01-09 | None | None | text='January 9, 2026' | note=None' for 'Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.'; probe_t207_p8.out 'P8 pos=None non-bill | state=stated | date_iso=2026-01-09' vs 'P8 pos=None ledger | state=not_stated'; app/backend/service_date.py:375-376 'if date_iso:' ... 'state=\"stated\", first=date_iso'; app/backend/store.py:133-136; tests/unit/test_t202_r3_allow_list.py:98 pins it; mutants_t207.out 'M7 ... KILLED'; docs/LLM_VS_CODE.md:30 'Only a date tied to the line by ... counts'; spec/REQUIREMENTS.md:50 'Date of service is the record's header date, parsed by code.'",
85	   "why_it_matters": "The code follows R-TL-3 for encounter records and nothing is invented, but the table says the allow-list decides and that the header date is not the DOS for a bill only. The table misstates a rule that decides a printed date. Under persona §5 an unannounced default would be a blocker; R-TL-3 authorizes it here, so I rate it major.",
86	   "fix": "Chris rules (Q1). If yes, row 2 names the encounter-header rule and cites R-TL-3. The pos-None branch at store.py:133 then either follows the same rule and says so, or prints the blank as the ledger path does.",
87	   "acceptance_test": "Row 2 states the rule; a test with pos=None on a visit-note charge matches the ruling; M7 stays killed."},
88	  {"severity": "major", "title": "A counted undated charge prints the blank with no Step 3 confirm note",
89	   "evidence": "probe_t207.out 'P6 | $250.00 | not_stated | None | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None' vs 'P6-uncounted ... note=' with a note; app/backend/store.py:129 (counted_undated) and :139 'if not stated and not counted_undated:'; mutants_t207.out 'M6 ... SURVIVED'; docs/LLM_VS_CODE.md:31 'Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it'; memory/ORCHESTRATOR_DECISIONS.md:72 D-064 'then sums like any accepted charge'",
90	   "why_it_matters": "Row 3 and the brief require a Step 3 note for every not-certain case. Once the paralegal counts the line, the prompt disappears; the blank still prints, so nothing is invented or lost. Major, not blocker.",
91	   "fix": "Either row 3 says counted lines carry no note and cites D-064, or store.py:139 keeps the note with 'Count this charge' wording.",
92	   "acceptance_test": "A test on a counted undated charge asserts the decided note behaviour; M6 is killed or the row is amended."},
93	  {"severity": "major", "title": "Validation cell claims 24 mutants all fail; two resolver mutants survive and no 24-mutant harness exists",
94	   "evidence": "docs/LLM_VS_CODE.md:31 '24 mutants of the resolver and the check all fail the unit suite'; mutants_t207.out 'M4 five-year bound ... SURVIVED' (service_date.py:274) and 'M8 Encounter date heading dropped ... SURVIVED' (service_date.py:53); grep -rn -i mutant tests/unit evals --include=*.py returns 28 comment hits from other cards",
95	   "why_it_matters": "A validation claim that the reviewer can refute is a finding. The cell is part of the checked artifact (row 3 'How it is checked').",
96	   "fix": "Amend the cell to the tests that exist, or commit the mutation harness with its count; add tests that kill M4 and M8.",
97	   "acceptance_test": "The cell names only committed tests; the harness, if committed, reports 24 of 24 killed; M4 and M8 are killed."},
98	  {"severity": "minor", "title": "Row 2's column-heading list is narrower than the code",
99	   "evidence": "docs/LLM_VS_CODE.md:30 'a DOS or service column header'; app/backend/service_date.py:53-54 _H_SVC also matches visit date, date of visit, encounter date, svc, 24A, from/to service; M8 survives",
100	   "why_it_matters": "A reader cannot tell which headings decide a printed date.",
101	   "fix": "List the heading set in row 2; add a test for Encounter Date.",
102	   "acceptance_test": "Row 2 lists the set; M8 is killed."},
103	  {"severity": "minor", "title": "Row 3's note wording holds only for written-date reasons",
104	   "evidence": "docs/LLM_VS_CODE.md:31 'asking the paralegal to read the date from the quote' and 'names the date as the quote writes it'; app/backend/service_date.py:102 (written-date note) vs :103 'Request a dated itemized bill, or fill the blank from the record'; probe_t207.out 'P7b ... note=The line states no date of service ...'",
105	   "why_it_matters": "The no-label note does not name a date and does not ask for the quote, so row 3 overstates the note.",
106	   "fix": "Align row 3 with the two note forms, or change the no-label note to point to the quote.",
107	   "acceptance_test": "The row and the note text agree; the existing confirm-note test still passes."},
108	  {"severity": "minor", "title": "A second date-of-service parser on billing lines sits outside row 2's only-path claim",
109	   "evidence": "app/backend/billing.py:141 'def _dos(raw): p = dates.parse_date(raw or \"\")'; billing.py:339 'dos_iso': _dos(dos); billing.py:1062 GET /api/cases/{token}/billing; api.py:599 billing.add_routes; no frontend consumer (grep app/frontend for /billing empty)",
110	   "why_it_matters": "Row 2 says a charge line's date of service is read only by service_date.py. This endpoint returns a DOS per bill line by a generic parser. It does not reach the letter, but it is a second source of the same fact.",
111	   "fix": "Document the endpoint's dos_iso as not a charge date in row 2, or remove it.",
112	   "acceptance_test": "Row 2 names the endpoint's status; grep for dos_iso writers shows no second charge-date path."}
113	 ],
114	 "whats_right": ["The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.",
115	                 "The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.",
116	                 "The blank matches the D-071 addendum text exactly (probe P7), and letter_check reports value 0 over 25 cases."],
117	 "questions_for_chris": ["Q1 (F3): Should a dated visit note's header date be the date of service for a charge with no labeled date? R-TL-3 says yes; row 2 says only the allow-list counts.",
118	                         "Q2 (F1): Is the same-period locale rule approved ('04/05/2026 - 13/05/2026' as May 4-13), or should that period print the blank as row 2 states?",
119	                         "Q3 (F4): Should a counted undated charge (D-064) show the Step 3 confirm note?"]}
120	```
121	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:04.640Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_doc_rows_patterns.md"
}
````

### User / tool · 2026-11-03T02:01:04.646Z

**tool result**
````
1	---
2	name: t207-doc-rows-patterns
3	description: T-207 (LLM_VS_CODE rows 2-3 vs service_date.py): table "only" claims vs extra code resolvers, untested five-year bound, validation-cell mutant count, counted-line note suppression
4	metadata:
5	  type: project
6	---
7	
8	Doc-row reviews of a date rule find the same kinds of gap: the table says "only" and the code does a little more. Found at fc37fbc (r1, 2026-11-02): (1) a same-period locale rule resolves a two-reading date that row 2 says only the statement rule decides, and a test pins it; (2) the "more than five years before" bound is 366*5 days, so 5y+1d to 5y+4d are printed, and no test sits between the 1998 and 2031 fixtures; (3) a visit note's header date becomes the date of service for a charge with no labeled date (spec R-TL-3 backs it, the table does not say so); (4) a counted undated charge (D-064) has its Step 3 note suppressed by a flag, and no test pins the note; (5) a validation cell claims "24 mutants all fail" with no harness in the repo, and two resolver mutants survive.
9	
10	**Why:** the table is the binding description of what decides a printed date, and each gap is a place where an adjuster sees a date the table says is not decided that way. The mutant count is a claim the reviewer can refute.
11	
12	**How to apply:** when a row says "only" or "never", list every code path that prints the value (grep the field: dos_iso, dos_text, date_iso) and compare each to the sentence. For any "more than N" bound, probe N-1 day, N, N+1 day and the window in between. For any flag that suppresses a note (counted, undated, pos None), probe it and mutate the flag. For a validation cell that gives a mutant count, grep tests/ and evals/ for a harness before accepting the number; if none, run your own mutants on a scratch copy of the pinned archive. Also check the model id: the dossier says claude-sonnet-5-5, but the review ran as claude-haiku-5-5, so record the id actually running.
13	
14	Recurrence: item (3) was already flagged as a default-allow non-bill fallback in the T-202 r3 review ([[project_t202_r3_patterns]]). At fc37fbc the code is unchanged and the table still omits it, so it is a documentation gap that has been open since then. The T-202 r3 note says the author's 24 mutants were run outside the repo; that count is still not reproducible from the repo.
15	
16	Related: [[feedback_guard_blocks_shell_expansions]], [[feedback_mutant_apply_verify]], [[feedback_review_write_once]], [[feedback_severity_vs_brief]].
17	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:06.654Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD 8cb5bd2 efda639 2>&1 | head; git log --oneline -8; git status --short | head -20; sed -n 28,33p docs/LLM_VS_CODE.md"
}
````

### User / tool · 2026-11-03T02:01:07.022Z

**tool result**
````
efda639f388e5efd3ce15ea820c5c9ae692ad313
8cb5bd2e657408a2654117cb04fa173031c294a9
efda639f388e5efd3ce15ea820c5c9ae692ad313
efda639 docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)
8cb5bd2 fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
8521562 fix(frontend): Step 3 next step depends on the date reason: doubtful date checks the quote, no date looks outside it; statement-date, total and clip minors (T-209 r2)
88c73dd fix(frontend): Step 3 confirm note names the letter's fillable date blank (T-209)
68f67cc fix(frontend): T-204 r3 prepared AI-check panel says the prepared answers / the second AI check; guided footer neutral until health; allow-list narrowed to whole sentences; rerun label and guided walk tested
fc37fbc docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank
8aa14e1 test(qa): T-208 r2 the AI translation label is exempt only with a translated entry's quote; label on an English letter fails
679b63e fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
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
|---|---|---|---|---|
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendments; T-202, `app/backend/service_date.py`), and it is read by an allow-list of positive evidence.** Only a date tied to the line counts: (a) a column heading over it that names service (DOS, date of service, service date, visit date, date of visit, encounter date, SVC, service or SVC from/to/thru, CMS-1500 24A); (b) a service label in its clause, which in prose is only DOS, date(s) of service or service date, never after next, last, prior, previous, initial, first, return, follow-up, scheduled, upcoming or future ("visit date", "seen on" and a bare "date" are not labels; a bill also reads its own "visit of", "rendered/provided/performed on", "the run of", "service period", "period of service" and "dates of treatment", and a UB-04 "statement covers period"; a label may be followed by a colon, spaces or a dotted leader); (c) the charge row's own date cell under a heading of kind (a); (d) for a coded line of a bill with no date of its own, the one period the bill states for its services. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never read as a service date, and no date is borrowed from another line, another record or the statement year. **A numeric date that reads two ways is settled by two fixed rules, in this order, and otherwise stays unread.** (1) Same date or period: when another end of the same labeled date or period can be read only one way (`13/05/2026`), every end takes that order, so `04/05/2026 - 13/05/2026` reads as May 4 to May 13; two ends that force different orders are not read. This uses the date's own text, not a locale guessed from the record (D-071 amendment: no locale rule from the record). (2) Otherwise a service cannot follow its statement (D-071 clarification): the date is read only when exactly one order puts every labeled end on or before the record's own date, and with no record date it is not read. This is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or several labeled dates that do not agree is not read. **The bound applies to every record, not only bills:** a labeled service date after the record's own date, or more than 1,830 days (5 x 366) before it, is not read (reason `implausible`); a record with no date has no bound. The bound is day arithmetic, so a date a few days past five calendar years can still be read. **A record's own date is the service date only for an identified encounter record** (a visit, ER, clinic, therapy, imaging or ambulance-run note), and only when the line has no labeled date of its own (R-TL-3, D-071 amendment 2). The record types are one declared data file, `app/backend/encounter_types.json`, read by `service_date.record_kind` in production and by `evals/letter_check.py` with its own matcher. A bill, receipt, superbill, charge summary, administrative paper (phone note, letter, affidavit, referral) or record of unknown type never lends its header date. A labeled date that cannot be read in an encounter record is not replaced by the header date: the line prints the blank. The billing view's per-line `dos_iso` (`app/backend/billing.py`, `GET /api/cases/{token}/billing`) is a display field read by a different parser; it is not a charge date and does not reach the letter. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is the service date of row 2, never the record's header date merely because it is the header (a bill's header date is its statement date), and the model is never asked. Code prints the service date or period the line itself states, or, for an identified encounter record (R-TL-3, row 2), the visit's own date when the line has no labeled date. A bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its header date. When no service date is certain (the quote labels none, or labels one the code cannot read with certainty), the letter prints the same fillable blank, like the Bates placeholder, beside the statement date: `date of service [__________] (statement dated June 15, 2026)` (D-071 addendum; `service_date.not_stated_text`, `export.charge_when`). The paralegal fills it from the quote; nothing is inferred. Step 3 shows exactly what the letter prints and carries a confirm note in one of two forms (`service_date.confirm_note`): when the quote labels a date the code cannot read, the note names the date as the quote writes it and asks her to confirm it and fill the blank; when the quote labels none, the note says the line states no date of service (or that the only date near it is not labeled as one) and asks her to request a dated itemized bill or fill the blank from the record. **A charge she has counted for its missing date of service (D-064) still prints the blank but carries no note**, because she counted it knowing (`store.charge_service_date`). A hand-built case dict without `dos_iso` (no store path) keeps the record's date in `export.charge_when`; the app's own export carries `dos_iso` for every charge. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. Charge dates: `tests/unit/test_t202_r3_allow_list.py`, `tests/unit/test_t202_r4_encounter.py` (131 tests; every reviewer probe from rounds 3 and 4 is a fixture) and `tests/unit/test_t200_undated_charge_label.py`; `evals/letter_check.charge_date_violations`, an independent per-line scanner over 25 cases that does not import the production parser (it reads the same `encounter_types.json`, with its own matcher) and accepts the blank, whole and exact, and nothing else for a line with no certain date. The T-202 r4 handoff reports a one-off mutation run on a scratch copy (24 of 25 mutants failed the unit suite, the 25th judged equivalent); that harness is not committed, so the run cannot be repeated from the repo. |
| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054, T-112; `summary_trim.trim`, `app/backend/summary_trim.py:391`, called from `generator.py:70-79` only for an English-routed record whose quote is in the record). The summary is split into clauses, and a clause is removed only when it adds **salient new content** its quote lacks: a number or month, a side, a negation, or a procedure, device, drug, body-part or diagnosis term (`new_salient`, `summary_trim.py:325-356`). Terms are matched by word family (Tylenol with acetaminophen, cervical with neck) after clinical abbreviations are expanded on both sides (`expand_abbreviations`, `:108`; families `:212-267`), so a faithful paraphrase stays and judge 1 checks it. The negation and side words come from the lexicon (`code_lists.added_qualifier` through `grounding`, `summary_trim.py:269`, `:338-342`), not from a list in the trim. A number, side or negation counts only in a clause that shares no content word with the quote; a changed value on the quote's own topic ('Pain 3/10' over 'Pain 4/10') stays and is caught by the rung 1 token checks. A **structural no-fragment rule** (no word list; `:417-423`, T-128 r3): code trims only a **suffix**. A clause is removed only when every clause after it is removed too, so the kept text is always a prefix of whole clauses and no kept clause can follow a removed one (`'Wrist pain 6/10; splint fitted; patient tolerated well.'` over a quote that supports only the first and last clause is returned unchanged). The first clause is never removed (if it is the unsupported one, nothing is trimmed and the whole summary goes to judge 1); the kept prefix needs at least 2 content words. When a rule says no, the summary is returned unchanged; a kept clause is never edited (`tests/unit/test_summary_trim.py::test_a_trim_never_leaves_a_fragment`, `::test_the_first_clause_is_never_removed`, `::test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed`). Each removal is shown in the trace as 'removed from the summary: not in the quote'. If every clause is removed, or what is left has no content word, the item goes to the could-not-verify tray with `SUMMARY_NOT_IN_QUOTE` (`summary_trim.py:414-415`; `generator.py:75-77`; template `why.py:33`) and is never judged. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
| 5 | Clinical facts as a separate list | **Not built.** The summary and the verbatim excerpt carry the facts. | Every extra paraphrased field is another place to invent medical content. | n/a (deliberate omission). |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:09.077Z

**tool call — Bash**
````
{
 "command": "git diff --stat 8cb5bd2 efda639; git status --short | grep -v agent-memory | head -20; git show --stat 8cb5bd2 | head -40; cat app/backend/encounter_types.json | head -80; wc -l app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T02:01:09.306Z

**tool result**
````
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
MM app/frontend/guided/app.js
 M app/frontend/guided/review.js
MM app/frontend/guided/step3.css
MM app/frontend/guided/step3.js
MM app/frontend/judges.js
 M artifacts/screenshots/guided/home-1440.png
 M artifacts/screenshots/guided/home-390.png
 M artifacts/screenshots/guided/home-empty-1440.png
 M artifacts/screenshots/guided/step1-drafting-1440.png
 M artifacts/screenshots/guided/step1-failed-1440.png
 M artifacts/screenshots/guided/step4-blocked-1440.png
 M artifacts/screenshots/guided/step4-blocked-390.png
 M artifacts/screenshots/guided/step4-letter-1440.png
 M artifacts/screenshots/guided/step4-letter-390.png
 M artifacts/screenshots/guided/step4-pending-1440.png
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
commit 8cb5bd2e657408a2654117cb04fa173031c294a9
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 19:50:55 2026 -0600

    fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/encounter_types.json             |  21 ++
 app/backend/service_date.py                  | 115 +++++++---
 app/backend/store.py                         |   6 +-
 evals/letter_check.py                        |  88 ++++++--
 memory/contracts/api.md                      |   2 +-
 tests/unit/test_t200_undated_charge_label.py |   3 +-
 tests/unit/test_t202_r3_allow_list.py        |   3 -
 tests/unit/test_t202_r4_encounter.py         | 310 +++++++++++++++++++++++++++
 8 files changed, 488 insertions(+), 60 deletions(-)
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
     434 app/backend/service_date.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:12.983Z

**tool call — Bash**
````
{
 "command": "git status --short -- app/backend evals tests docs | head; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t207r2 && git archive 8cb5bd2 | tar -x -C $S/t207r2 && ls $S/t207r2 | head; git diff 8cb5bd2 efda639 | head -30 | cut -c1-300"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:01:13.241Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T02:01:14.406Z

**tool result**
````
MM docs/LLM_VS_CODE.md
 M tests/e2e/conftest.py
MM tests/e2e/guided/test_t206.py
MM tests/e2e/test_prepared_first_paint.py
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
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
diff --git a/docs/LLM_VS_CODE.md b/docs/LLM_VS_CODE.md
index 3a995a0..aa1b543 100644
--- a/docs/LLM_VS_CODE.md
+++ b/docs/LLM_VS_CODE.md
@@ -27,8 +27,8 @@ A paralegal turns scattered medical records into a treatment chronology, and an
 | # | Pipeline step | Code or LLM | Why we drew the line here | How it is checked |
 |---|---|---|---|---|
 | 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is 
-| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendment
-| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is not the recor
+| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. Entry dates stay on this strict rule. **A charge line's date of service is code only, never the LLM (D-071 and its amendment
+| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. **Charge-line exception:** for a charge line the date is the service d
 | 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous 
 | 5 | Clinical facts as a separate list | **Not built.** The summary and the verbatim excerpt carry the facts. | Every extra paraphrased field is another place to invent medical content. | n/a (deliberate omission). |
 | 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must not depend on a model's attention. | Unit tests with noisy, dup
````

### User / tool · 2026-11-03T02:01:14.414Z

**tool result**
````
1	"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 rounds 3 and 4: an ALLOW-LIST, not a deny-list). Code only, no LLM
2	(LLM_VS_CODE rows 2 and 3).
3	
4	The letter's charge line carries a date of service. A date there is a claim to an adjuster, so a date is the line's service date ONLY when one of these ties it to the line:
5	  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
6	  (b) a service label in the same clause before (or just after) it. In prose ONLY 'DOS', 'date of service', 'dates of service' and 'service date' (D-071 amendment 2; 'visit date', 'seen on'
7	      and a bare 'date' name next or prior visits and entry dates, so they are not labels), never after next/last/prior/previous/initial/first/return/follow-up/scheduled/upcoming/future.
8	      A BILL also reads the wording a statement uses for what it covers ('visit of', 'the run of', 'rendered on', 'service period' ...). A label may be followed by a dotted leader,
9	      spaces or a colon before its date;
10	  (c) it is the date cell of the charge row itself, in a table whose header is (a);
11	  (d) for a coded line of a bill with no date of its own: the one period the bill states for its services ('dates of service ...', 'the run of ...', and on a UB-04 'statement
12	      covers period ...').
13	Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all) is NOT a service date and is never
14	looked at again: an unlabeled date cannot become the line's date by default. The record's own date is the line's date ONLY for a positively identified encounter record (`record_kind`, the
15	table app/backend/encounter_types.json: visit, ER, clinic, therapy, imaging, ambulance-run note); a bill, receipt, superbill, charge summary, administrative paper or record of unknown type
16	never lends its header date. The result is one of:
17	  - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
18	    EVERY labeled end then reads one way; a stated date after its record's own date, or more than five years before it, is doubtful);
19	  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service (an encounter record keeps its own date instead);
20	  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
21	    the code cannot read it with certainty; the note names the date as the quote writes it.
22	  Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
23	  and the letter never says "service date not stated" above a quote that states one.
24	Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
25	(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
26	import datetime as _dt
27	import json
28	import pathlib
29	import re
30	
31	from app.backend import amounts as AM
32	
33	TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
34	_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))
35	
36	
37	def _tokens(text: str) -> list:
38	    return re.findall(r"[^\W_]+", (text or "").lower())
39	
40	
41	def _phrase_rx(terms):
42	    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")
43	
44	
45	_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
46	_ABBR = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(map(re.escape, _TYPES["encounter_abbreviations"])) + r")(?![A-Za-z0-9])")
47	_OPEN = int(_TYPES["opening_chars"])
48	
49	
50	def _hit(rx, text) -> bool:
51	    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))
52	
53	
54	def record_kind(source, excerpt: str = "") -> str:
55	    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
56	    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
57	    identification in the source label (visit, ER, clinic, therapy, imaging, ambulance-run note ...). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
58	    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
59	    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
60	        return "bill"
61	    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
62	        return "other"
63	    return "encounter" if (_hit(_ENC, src) or _ABBR.search(src)) else "other"
64	
65	_MON = AM._MON
66	_ORD = r"(?:st|nd|rd|th)?"
67	_DASH = "–—"
68	_TOK = re.compile(
69	    r"(?<![\w/$])(?:"
70	    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
71	    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
72	    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
73	    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
74	    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
75	    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
76	    r")(?![\w/]|\.\d)", re.IGNORECASE)
77	_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
78	_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
79	# ---- the allow-list: positive evidence that a date is the line's date of service. Nothing else is read (T-202 round 3).
80	_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
81	_LEADER = re.compile(r"(?:\.[ ]?){3,}|\u2026+")
82	_WINDOW = 60                     # characters before a date that may hold its label and the leader after it
83	
84	
85	def _mask_leaders(text: str) -> str:
86	    """The same text with every dotted leader ('.......', '. . . .', '\u2026') replaced by as many middle dots, so positions are unchanged: a leader is neither a sentence end nor a column gap, and
87	    'Date of service.......01/19/2026 ... 99213 office visit ...... $250.00' reads as one clause (T-209 r2: a label, dots or spaces or a colon, then one date is that label's date)."""
88	    return _LEADER.sub(lambda m: "\u00b7" * len(m.group(0)), text or "")
89	_NOT_OTHER_VISIT = (r"(?<!next )(?<!last )(?<!prior )(?<!previous )(?<!initial )(?<!first )(?<!return )(?<!scheduled )(?<!upcoming )(?<!future )(?<!follow-up )(?<!followup )"
90	                    r"(?<!next\s)(?<!last\s)")
91	_SVC_CORE = _NOT_OTHER_VISIT + r"(?:\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?)"        # amendment 2 (b): the only labels in prose
92	_SVC_BILL = (r"\bvisit\s+of|\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
93	             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")        # a bill's own wording for what it covers (a statement 'for the visit of', an invoice 'for the run of')
94	_PER_CORE = (r"\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bservice\s+period|\bperiod\s+of\s+service|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|"
95	             r"\b(?:services?\s+)?(?:rendered|provided)\s+on")
96	_UB_CORE = r"\bstatement\s+(?:covers\s+)?period"          # UB-04 FL6 'Statement Covers Period' is the span of the services; on any other bill 'statement period' is not a service label
97	_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
98	
99	
100	def _lbl_rx(extra, ub):
101	    return re.compile(rf"(?:{_SVC_CORE}" + (rf"|{_SVC_BILL}" if extra else "") + (rf"|{_UB_CORE}" if ub else "") + rf"){_LBL_END}", re.IGNORECASE)
102	
103	
104	_LBL = {(b, u): _lbl_rx(b, u) for b in (False, True) for u in (False, True)}          # keyed (bill, ub)
105	_PER = {u: re.compile(rf"(?:{_PER_CORE}" + (rf"|{_UB_CORE}" if u else "") + rf"){_LBL_END}", re.IGNORECASE) for u in (False, True)}
106	# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
107	_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
108	                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
109	_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful
110	
111	REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
112	WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
113	
114	
115	def display(first, last=None) -> str:
116	    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
117	    def lng(iso):
118	        d = _dt.date.fromisoformat(iso)
119	        return f"{d.strftime('%B')} {d.day}, {d.year}"
120	    if not last or last == first:
121	        return lng(first)
122	    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
123	    if (a.year, a.month) == (b.year, b.month):
124	        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
125	    if a.year == b.year:
126	        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
127	    return f"{lng(first)}–{lng(last)}"
128	
129	
130	BLANK = "date of service [__________]"
131	
132	
133	def not_stated_text(statement_iso) -> str:
134	    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
135	    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
136	    if statement_iso:
137	        return f"{BLANK} (statement dated {display(statement_iso)})"
138	    return BLANK
139	
140	
141	def printed_text(res: dict, statement_iso) -> str:
142	    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
143	    return not_stated_text(statement_iso)
144	
145	
146	_WHY = {
147	    "ambiguous_numeric": "The quote labels {raw} as the date of service, and it can be read as month/day or day/month; the record does not settle which.",
148	    "two_digit_year": "The quote labels {raw} as the date of service, but it has a two-digit year, which the code does not guess.",
149	    "no_year": "The quote labels {raw} as the date of service, but it states no year, which the code does not borrow from the statement.",
150	    "invalid": "The quote labels {raw} as the date of service, but it is not a complete date on the calendar.",
151	    "several_dates": "The quote labels more than one date of service ({raw}) and nothing says which one belongs to this charge.",
152	    "implausible": "The quote labels {raw} as the date of service, but that date is after the statement it appears on or years before it.",
153	    "non_service_date": "The only date near this line ({raw}) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service).",
154	    "no_date": "The line states no date of service.",
155	}
156	_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
157	_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it."
158	
159	
160	def confirm_note(reason, raw) -> str:
161	    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
162	    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)
163	
164	
165	def _iso(y, mo, d):
166	    try:
167	        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
168	    except ValueError:
169	        return None
170	
171	
172	class _Tok:
173	    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")
174	
175	    def __init__(self, m):
176	        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
177	        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
178	        getattr(self, "_" + self.kind)(m.group(0))
179	        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
180	            self.flaw = "invalid"
181	
182	    def _iso(self, s):
183	        y, mo, d = (int(x) for x in s.split("-"))
184	        self.fixed = _iso(y, mo, d)
185	
186	    def _num(self, s):
187	        a, b, y = re.split(r"[/.-]", s)
188	        if len(y) == 2:
189	            self.flaw = "two_digit_year"
190	            return
191	        a, b, y = int(a), int(b), int(y)
192	        md, dm = _iso(y, a, b), _iso(y, b, a)
193	        if md and dm and md != dm:
194	            self.ambiguous = {"MD": md, "DM": dm}
195	        elif md or dm:
196	            self.fixed = md or dm
197	            self.order = None if (md and dm) else ("MD" if md else "DM")
198	
199	    def _mdy(self, s):
200	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
201	        if m.group(4):
202	            self.flaw = "two_digit_year"
203	            return
204	        if not m.group(3):
205	            self.flaw = "no_year"
206	            return
207	        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))
208	
209	    def _dmy(self, s):
210	        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
211	        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))
212	
213	    def _md(self, s):
214	        self.flaw = "no_year"
215	
216	    def _mper(self, s):
217	        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
218	        if not m.group(5):
219	            self.flaw = "no_year"
220	            return
221	        y, m1 = int(m.group(5)), _mon(m.group(1))
222	        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
223	        if a and b and b > a:
224	            self.first, self.last = a, b
225	        else:
226	            self.flaw = "invalid"
227	
228	
229	def _mon(name):
230	    from app.backend import dates
231	    return dates.MONTHS[name.lower()[:3]]
232	
233	
234	class _Unit:
235	    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
236	    def __init__(self, toks):
237	        self.toks = toks
238	        self.start, self.end = toks[0].start, toks[-1].end
239	
240	    def raw(self, text):
241	        return text[self.start:self.end]
242	
243	
244	def _units(text: str) -> list:
245	    toks = [_Tok(m) for m in _TOK.finditer(text)]
246	    out, k = [], 0
247	    while k < len(toks):
248	        t = toks[k]
249	        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
250	            out.append(_Unit([t, toks[k + 1]]))
251	            k += 2
252	        else:
253	            out.append(_Unit([t]))
254	            k += 1
255	    return out
256	
257	
258	def _certain(unit: _Unit, ref):
259	    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
260	    for t in unit.toks:
261	        if t.flaw:
262	            return "bad", t.flaw
263	    if len(unit.toks) == 1 and unit.toks[0].first:
264	        return "ok", unit.toks[0].first, unit.toks[0].last
265	    determined = {t.order for t in unit.toks if t.order}
266	    amb = [t for t in unit.toks if t.ambiguous]
267	    if len(determined) > 1:
268	        return "bad", "ambiguous_numeric"
269	    if determined:
270	        order = next(iter(determined))
271	    elif amb:
272	        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
273	        if len(feasible) != 1:
274	            return "bad", "ambiguous_numeric"
275	        order = feasible[0]
276	    else:
277	        order = None
278	    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
279	    if len(isos) == 2 and isos[1] <= isos[0]:
280	        return "bad", "invalid"
281	    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)
282	
283	
284	def _header_cells(excerpt: str, row_ls: int):
285	    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line."""
286	    for line in reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]):
287	        if not line.strip():
288	            return None
289	        if re.search(r"\d", line) and not _H_SVC.search(line):
290	            continue
291	        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
292	        return cells if len(cells) >= 2 else None
293	    return None
294	
295	
296	def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
297	    heads = _header_cells(excerpt, row_ls)
298	    if not heads:
299	        return ""
300	    col = tok_abs - row_ls
301	    if len(heads) == len(row_cells):
302	        idx = next((i for i, (a, b) in enumerate(row_cells) if a <= col < b), None)
303	        if idx is not None:
304	            return heads[idx][1]
305	    return min(heads, key=lambda h: abs(h[0] - col))[1]
306	
307	
308	def _mark(text: str, units: list, rx, tail: bool = False) -> list:
309	    """[bool] per unit: a service label ends the 60 characters before it, or it is listed ('A and B') after a labeled unit. In `tail` (words after the figure) the label must open the
310	    tail: no sentence break and no 'and'/'or' between the figure and the label."""
311	    marks = []
312	    for k, u in enumerate(units):
313	        ok = bool(rx.search(text[max(0, u.start - _WINDOW):u.start]))
314	        if ok and tail:
315	            before = text[:u.start]
316	            ok = len(before) <= _WINDOW and not re.search(r"[.;]|\b(?:and|or)\b", before, re.IGNORECASE)
317	        if not ok and k and marks[k - 1] and _LIST.match(text[units[k - 1].end:u.start]):
318	            ok = True
319	        marks.append(ok)
320	    return marks
321	
322	
323	def _plausible(first, last, ref) -> bool:
324	    """A service date is not after the record it appears in and not years before it."""
325	    if not ref:
326	        return True
327	    r = _dt.date.fromisoformat(ref)
328	    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)
329	
330	
331	def _decide(units, text, ref):
332	    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
333	    reads = [(u, _certain(u, ref)) for u in units]
334	    raws = [" ".join(u.raw(text).split()) for u in units]
335	    if len(units) > 1:
336	        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
337	        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
338	            return "bad", "several_dates", raws
339	        first, last = next(iter(same))
340	    else:
341	        r = reads[0][1]
342	        if r[0] != "ok":
343	            return "bad", r[1], raws
344	        first, last = r[1], r[2]
345	    if not _plausible(first, last, ref):          # in every record: a service date is not after the record's own date and not years before it (a prior treatment's DOS is not this charge's)
346	        return "bad", "implausible", raws
347	    return "ok", first, last
348	
349	
350	def _apply(out: dict, res) -> dict:
351	    if res[0] == "ok":
352	        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
353	    else:
354	        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
355	    return out
356	
357	
358	def resolve(excerpt: str, start: int, source, date_iso) -> dict:
359	    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the labeled date text the reason is about, or the one
360	    unlabeled date near the line for non_service_date), raws ([the labeled dates as written])} for the figure at `start` of `excerpt`, in a record with header `source` and date
361	    `date_iso`. Only labeled dates are candidates (module doc); see it for the rules."""
362	    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
363	    excerpt = _mask_leaders(excerpt)
364	    amts = AM.find_amounts(excerpt or "")
365	    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
366	    if i is None:
367	        return out
368	    a = amts[i]
369	    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
370	    kind = record_kind(source, excerpt)
371	    bill = kind == "bill"
372	    ub = bool(_UB.search(source or "") or _UB.search(excerpt or ""))
373	    lbl = _LBL[(bill, ub)]
374	    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
375	    seg = excerpt[ss:se]
376	    others = []                       # dates near the line that no service label ties to it
377	
378	    def labeled(text, tail=False):
379	        us = _units(text)
380	        marks = _mark(text, us, lbl, tail)
381	        others.extend(u.raw(text) for u, m in zip(us, marks) if not m)
382	        return [u for u, m in zip(us, marks) if m]
383	
384	    if len(AM._cells(seg)) >= 2:                                          # (a)/(c) a table row: only a date under a heading that names service
385	        row_ls = excerpt.rfind("\n", 0, a["start"]) + 1
386	        rl_end = excerpt.find("\n", a["start"])
387	        row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
388	        row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
389	        lab = []
390	        for u in _units(seg):
391	            head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
392	            if (head and _H_SVC.search(head)) or lbl.search(seg[max(0, u.start - _WINDOW):u.start]):
393	                lab.append(u)
394	            else:
395	                others.append(u.raw(seg))
396	        if lab:
397	            return _apply(out, _decide(lab, seg, date_iso))
398	    else:                                                                 # (b) a service label in the same clause
399	        prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
400	        own = excerpt[prev:a["start"]]
401	        lab = labeled(own)
402	        if lab:
403	            return _apply(out, _decide(lab, own, date_iso))
404	        if prev > ss:                                                      # a labeled date stands once for the items listed after it: usable only when it is the line's one date
405	            whole = excerpt[ss:a["start"]]
406	            lab = labeled(whole)
407	            if lab:
408	                return _apply(out, _decide(lab, whole, date_iso))
409	        tail = excerpt[a["end"]:min([amts[j]["start"] for j in sfigs if j > i], default=se)]
410	        lab = labeled(tail, tail=True)
411	        if lab:
412	            return _apply(out, _decide(lab, tail, date_iso))
413	    # no labeled date of its own
414	    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
415	        if bill and AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # (d) a coded line takes the one period the bill states for its services
416	            prefix = excerpt[:se]
417	            us = _units(prefix)
418	            seen, uniq = set(), []
419	            for u, m in zip(us, _mark(prefix, us, _PER[ub])):
420	                if not m:
421	                    continue
422	                r = _certain(u, date_iso)
423	                key = (r[1], r[2]) if r[0] == "ok" else (u.raw(prefix),)
424	                if key not in seen:
425	                    seen.add(key)
426	                    uniq.append(u)
427	            if uniq:
428	                return _apply(out, _decide(uniq, prefix, date_iso))
429	        if others:
430	            out.update(reason="non_service_date", raw=others[0])
431	        return out
432	    if date_iso:                                                          # a positively identified encounter record (visit, ER, clinic, therapy, imaging, ambulance-run note): its date is the visit
433	        out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
434	    return out
435	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:02:17.630Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"charge_service_date\\|dos_iso\\|service_date\\|record_kind\" app/backend/*.py | grep -v \"^app/backend/service_date.py\" | cut -c1-220; echo ----; sed -n 105,160p app/backend/store.py"
}
````

### User / tool · 2026-11-03T02:02:17.732Z

**tool result**
````
app/backend/amounts.py:380:def _dos_iso(m, ref_iso):
app/backend/amounts.py:403:        iso = _dos_iso(m, ref_iso)
app/backend/amounts.py:440:        iso = _dos_iso(m, ref_iso)
app/backend/amounts.py:444:                end = _dos_iso(ms[k + 1], ref_iso)
app/backend/billing.py:339:    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
app/backend/billing.py:479:            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
app/backend/billing.py:553:        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
app/backend/export.py:22:from app.backend import amounts, charge_text, language, money, service_date
app/backend/export.py:74:    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026' (D-071). One implementation, shared with the case view (service_date.display)."""
app/backend/export.py:75:    return service_date.display(first, last)
app/backend/export.py:178:        return sorted(got, key=lambda a: (a.get("dos_iso") or self._date(a), a["record_no"], str(a.get("id"))))
app/backend/export.py:217:        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
app/backend/export.py:220:        without `dos_iso` (a hand-built one) keeps the record's date."""
app/backend/export.py:222:        if "dos_iso" not in a:
app/backend/export.py:224:        if a["dos_iso"]:
app/backend/export.py:225:            return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
app/backend/export.py:226:        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
app/backend/export.py:612:        if "dos_iso" in a and not a["dos_iso"]:
app/backend/gaps.py:79:        k = ingest.record_kind(bare)           # the ingest lexicon, on the label without parentheticals: same families, still a warning only (D-055)
app/backend/ingest.py:237:def record_kind(source: str, excerpt: str = "") -> str:
app/backend/ingest.py:339:        kind = record_kind(r["source"], r["excerpt"])
app/backend/present.py:152:            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for this charge's date
app/backend/store.py:118:def charge_service_date(item: dict, rec, pos) -> dict:
app/backend/store.py:121:    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when 
app/backend/store.py:122:    A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
app/backend/store.py:124:    service date. A positively identified encounter record's (visit, ER, clinic, therapy, imaging or ambulance-run note: service_date.record_kind, app/backend/encounter_types.json) own date is th
app/backend/store.py:126:    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
app/backend/store.py:128:    encounter = SD.record_kind((rec or {}).get("source"), item.get("excerpt") or "") == "encounter"
app/backend/store.py:146:def charge_service_dates(item: dict, rec, pos) -> tuple:
app/backend/store.py:147:    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
app/backend/store.py:148:    d = charge_service_date(item, rec, pos)
app/backend/store.py:196:            sd = charge_service_date(a, r, d["pos"])
app/backend/store.py:197:            d["dos_iso"], d["dos_end_iso"], d["dos_text"], d["dos_note"] = sd["date_iso"], sd["end_iso"], sd["text"], sd["confirm_note"]
----

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
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:02:19.897Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"def charge_when\" -B2 -A25 app/backend/export.py"
}
````

### User / tool · 2026-11-03T02:02:20.013Z

**tool result**
````
213-        return (self.records.get(n) or {}).get("date_iso")
214-
215:    def charge_when(self, a):
216-        """D-071 (extends T-200): the label before a charge's amount in the letter. A date there reads as the date of service, so it is the service date the charge's own bill line
217-        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
218-        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026)' (D-071 addendum: a fillable blank). Chosen over dropping the date
219-        because the adjuster can still match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict
220-        without `dos_iso` (a hand-built one) keeps the record's date."""
221-        n, src = a["record_no"], self.source(a["record_no"])
222-        if "dos_iso" not in a:
223-            return f"{src}, {_long_date(self.rec_date(n))}"
224-        if a["dos_iso"]:
225-            return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
226-        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
227-
228-    def cite(self, n):
229-        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
230-
231-    def cite_dated(self, n):
232-        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"
233-
234-    def quote(self, n, ev, whole_sentence=False):
235-        """Quote evidence from record n. A directly following full stop is included when the evidence starts a
236-        sentence; whole_sentence expands mid-sentence evidence to its sentence. Always a substring of the record."""
237-        text = self.text(n)
238-        i = text.find(ev) if ev else -1
239-        if i < 0:
240-            return ev
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:02:35.750Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && sed -n 170,215p app/backend/store.py | cut -c1-260; echo ----; sed -n 600,625p app/backend/export.py | cut -c1-240; echo; grep -n \"NO_DATE_WHY\" -r app | cut -c1-240"
}
````

### User / tool · 2026-11-03T02:02:35.862Z

**tool result**
````
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
        if f["state"] == "rejected":        # D-053/D-057: every tray flag (judge-rejected, not word for word, rule-filtered) is not an item to review, count or export; its quote may not be in the record
            continue
        c = f.get("computed") or {}
        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
    events = []     # D-047: no 'keep my wording' event exists any more
    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
    pages = (case.get("config") or {}).get("pages")
    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
                    **({"page": pdf_text.page_for(pages, r["char_start"])} if pages else {})) for r in recs]
    nar = (case.get("config") or {}).get("narrative")
    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events, prepared=prep)
    if blockers:                                        # trace.export_blockers calls this with blockers=False to build the letter it checks (T-139 r4)
----
        if p and _treating(v, e["record_no"]) and p not in paid and p not in dismissed and p not in names:
            names.append(p)
    if not names:
        return ["- none"]
    return ["- " + _terminate("; ".join(p + (" (itemized ledger)" if p in rated else "") for p in names))]


def _undated_charges(v):
    """T-202 r3: one line per accepted charge the letter prints without a certain date of service (the paralegal's to-do before the demand goes out): provider, amount, why, and the
    request for a dated itemized bill. [] when every charge has one (the heading is then left out)."""
    out = []
    for a in v.in_charges:
        if "dos_iso" in a and not a["dos_iso"]:
            why = (a.get("dos_note") or "The line states no date of service.").split(" The letter prints")[0]
            out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.")
    return out


def _held_amount_note(v, n, ents):
    """The RECORDS NOT IN THE TREATMENT SECTION reason for an entry held out because it states an amount (T-139 r2). It names only actions the review code accepts:
    dismiss the entry (always clears the hold); a quote without the amount WITH a matching summary in the same edit (a quote-only change is refused when the summary
    still has a token the new quote lacks); a summary edit alone only when the quote is already clean. A bill record is told where its charges are."""
    held = [e for e in ents if _status(e) != "out" and v.states_amount(e)]
    quote = any(money.has_money(e.get("excerpt")) for e in held)
    rows = [{"kind": a["cls"], "review_status": a.get("review_status"), "state": "rejected" if (_status(a) == "out" and a.get("review_status") != "dismissed") else "",
             "text": a.get("raw"), "excerpt": a.get("excerpt")} for a in v.amounts if a["record_no"] == n]

app/backend/store.py:129:    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
app/backend/amounts.py:312:_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
app/backend/amounts.py:313:NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
app/backend/amounts.py:535:            out["reason"] = _NO_DATE_WHY
app/backend/amounts.py:663:COUNTABLE_WHY = frozenset({_NO_DATE_WHY, _UNKNOWN_WHY})
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:02:38.586Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"import\\|encounter_types\\|def charge_date_violations\\|def _kind\\|CASES\\|FIXTURE\" evals/letter_check.py | head -50; git -C /Users/arsis/zlayt-pm-project diff 8cb5bd2 HEAD --stat -- evals app tests | tail -3"
}
````

### User / tool · 2026-11-03T02:02:38.696Z

**tool result**
````
3:For every golden case, the sample and every library packet, on the FIXTURE backend (recorded model answers; no network):
18:the line's date only for a positively identified ENCOUNTER record, read from the declared table app/backend/encounter_types.json (the same file production reads, matched here by this
27:import contextlib
28:import json
29:import pathlib
30:import re
31:import sys
32:import tempfile
41:    from app.backend import money
47:    from app.backend import money
53:    from app.backend import money
66:    from app.backend import amounts as AM, export
95:# original before sending), not provenance wording, and it is the only place the letter says 'AI'. Matched whole and verbatim (the string is copied here on purpose, not imported from the export).
138:    from app.backend import review
139:    from app.db import db as DB
159:    from app.backend import count_charge, review
160:    from app.db import db as DB
188:    from datetime import datetime
214:    from app.backend import export
234:TYPES_PATH = ROOT / "app" / "backend" / "encounter_types.json"          # D-071 amendment 2: the ONE declared table of record types (production reads the same file)
295:    from datetime import date
359:    from datetime import date, timedelta
413:def charge_date_violations(letter: str, records) -> list:
438:                from datetime import date
499:    from app.backend import export, ingest as IN, pipeline as PL, store
500:    from app.llm import provider as P
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:02:44.060Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && sed -n 300,320p app/backend/amounts.py | cut -c1-260; sed -n 515,545p app/backend/amounts.py | cut -c1-260; grep -n \"not_counted_reason\" -r app | cut -c1-230 | head -30"
}
````

### User / tool · 2026-11-03T02:02:44.187Z

**tool result**
````
    t = re.sub(r"[\s.#:]+", "", raw or "").upper()
    t = re.sub(r"^(?:CPT|HCPCS|REVENUE|REV|CODE)+", "", t)
    m = re.match(r"(\d{5}|[A-V]\d{4}|0\d{3})(?:-[A-Z0-9]{2})?$", t)
    return m.group(1) if m else t
_PERIOD_PHRASE = re.compile(r"(?:statement\s+period|billing\s+period|service\s+period|dates?\s+of\s+service|\bDOS\b|services?\s+(?:provided|rendered)|\brun\s+of|date\s+of\s+(?:the\s+)?run)\W{0,6}$", re.IGNORECASE)
_ADMIN_SRC = re.compile(r"\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b|"
                        r"\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|"
                        r"18\.001\s+affidavit|affidavit|authorization\s+form|HIPAA\s+authorization|correspondence|cover\s+letter|fax\s+cover|referral\s+(?:form|letter)|prior\s+authori[sz]ation|"
                        r"no-?\s?show\s+(?:notice|letter)|demand\s+letter)\b", re.IGNORECASE)
_BILLISH = re.compile(r"\b(?:statements?|bills?|billing|invoices?|ledgers?|account|itemi[sz]ed|ub-?04|hcfa|cms-?1500|claim\s+form)\b", re.IGNORECASE)
_BILL_OPEN = re.compile(r"^\W{0,3}(?:patient\s+)?(?:itemi[sz]ed|statement|invoice|ledger|billing|account\s+statement)\b", re.IGNORECASE)
_TOKEN_FILLER = frozenset("charge charges charged billed fee fees of on for the a an at to and unit units dos date service services statement rev cpt code invoiced total".split())
_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
_NO_SVC_WHY = "The line names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized service line and is not totaled."
_NO_COL_WHY = "The figure is not under a charges column of the bill, so it is not an itemized service line and is not totaled."
_SECOND_WHY = ("A second amount on a service line is not the line's own charge (it can be a deductible, what the patient owes, a denied or paid amount, an adjustment, "
               "a balance or an unlabeled figure), so it is not totaled.")
_ADMIN_WHY = "A letter, request or note is not a provider bill, so its figures are not totaled."
_NOT_BILL_WHY = "This record is not a bill (it is a clinical note or summary) and the case holds a bill from the same provider, so charges are taken from the bill only and this amount is not totaled."
_UNKNOWN_WHY = "The record's document type is unknown (its header names no provider or kind), so it is not read as a bill and this amount is not totaled."
            head = _column_label(excerpt, a["start"])
            if head and not _CHARGE_COL.match(head):
                out.update(reason=_NO_COL_WHY, dos=dos)
                return out
            if not head and len(sfigs) > 1 and sfigs[0] != i:
                out.update(reason=_NO_COL_WHY, dos=dos)
                return out
            # D-062 (staff r3): per figure, not per line. Under a charges-like heading, only the first such figure of the row is the line's own charge.
            if head and any(_CHARGE_COL.match(_column_label(excerpt, amts[j]["start"])) for j in sfigs if j < i):
                out.update(reason=_SECOND_WHY, dos=dos)
                return out
        else:
            earlier = [j for j in sfigs if j < i and _could_be_own_charge(excerpt, amts[j], source)]      # a rate or a labeled total before it ("FL44 rate $1,640.00 per day, ... FL47 total charges $4,920.00") is not the line's charge
            if earlier and not _dates_in(excerpt[amts[earlier[-1]]["end"]:a["start"]], date_iso):      # the line's own charge is its first figure; a later one needs a date of its own
                out.update(reason=_SECOND_WHY, dos=dos)
                return out
        if dos is None and coded:
            dos, out["dos_end"] = _record_period(excerpt[:se], date_iso)          # D-071: a period keeps its end date for the letter
        out["dos"] = dos
        if dos is None:
            out["reason"] = _NO_DATE_WHY
        elif not (_SVC.search(text_nodate) or coded):
            out["reason"] = _NO_SVC_WHY
        else:
            out["ok"] = True
        return out
    # a dated encounter record: the record's date is the date of service
    out["dos"] = dos or date_iso
    if _ADMIN_SRC.search(source or ""):
        out["reason"] = _ADMIN_WHY
        return out
app/frontend/charges.js:154:    q("#cn-amount").textContent = "Amount: " + a.text; q("#cn-reason").textContent = "Not counted now: " + a.not_counted_reason;
app/frontend/charges.js:207:  const notCounted = (a) => a.kind !== "charge" && a.not_counted_reason ? el("p", { class: "rv-reason-line rv-not-counted", "data-testid": "not-counted-reason" }, el("strong", {}, "Not counted: "), a.no
app/frontend/charges.js:219:    const detail = inTray && a.kind !== "charge" && a.not_counted_reason ? el("span", { class: "rv-unclear-note rv-detail", "data-testid": "charge-detail" }, unclearNote(c, a)) : null;
app/frontend/charges.js:229:    if (why && nc) { why = why.split(a.not_counted_reason).join("").replace(/\s+/g, " ").trim() || null; }   // the reason is already on its own line; keep only what the server adds to it (for example t
app/backend/count_charge.py:54:        raise _err("NOT_COUNTABLE", "This amount is already a charge. Accept it to count it.", item_id=item_id, not_counted_reason=None)
app/backend/count_charge.py:57:        raise _err("NOT_COUNTABLE", f"This amount cannot be counted. {info['reason']}", item_id=item_id, not_counted_reason=info["reason"])
app/backend/count_charge.py:60:                   confirm_with=CONFIRM, of=None, message=REQUIRED, not_counted_reason=info["reason"])
app/backend/count_charge.py:74:    lad.update(judge=None, code_checks=cc, state=state, counted={"confirm": CONFIRM, "at": store.iso(t), "by": "reviewer", "not_counted_reason": info["reason"]},
app/backend/count_charge.py:85:                                                         "not_counted_reason": info["reason"], "confirm_flag": promo["flag"] if promo else None}, t)
app/backend/store.py:129:    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
app/backend/present.py:151:            "not_counted_reason": nc["reason"], "countable": nc["countable"],
app/frontend/guided/step3.js:83:        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
app/frontend/guided/step3.js:98:        h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
app/frontend/guided/step3.js:145:        notCounted.length ? table(["Amount", "From", "Why"], notCounted.map((a) => row(a, [from(a), a.kind === "charge" ? "You chose not to count it." : R.plain(a.not_counted_reason || "")]))) : h(
app/frontend/guided/step3.js:147:        never.length ? table(["Amount", "From", "Why it's never counted"], never.map((a) => row(a, [from(a), R.plain(a.not_counted_reason || "")]))) : null));
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:04.776Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -rn \"1830\\|366\\|five year\\|5 year\\|_YEARS_BEFORE\\|implausible\" tests/unit/test_t202*.py tests/unit/test_t200*.py | cut -c1-220 | head -30; grep -c \"^def test_\\|^    def test_\" tests/unit/test_t202_r4_encounter.py; grep -n \"parametrize\" tests/unit/test_t202_r4_encounter.py | head"
}
````

### User / tool · 2026-11-03T02:03:04.885Z

**tool result**
````
tests/unit/test_t202_r3_allow_list.py:183:    ("later than the statement", "Itemized ledger. DOS 07/20/2026 office visit charge $220.00.", "$220.00", "07/20/2026", "2026-06-15", "implausible"),
tests/unit/test_t202_r3_allow_list.py:184:    ("1998, years before the statement", "Itemized ledger. DOS 03/13/1998 office visit charge $220.00.", "$220.00", "03/13/1998", "2026-06-30", "implausible"),
tests/unit/test_t202_r3_allow_list.py:185:    ("2031, years after the statement", "Itemized ledger. DOS 03/13/2031 office visit charge $220.00.", "$220.00", "03/13/2031", "2026-06-30", "implausible"),
25
76:@pytest.mark.parametrize("lab,src,rd,ex,fig,want", KEEP, ids=[k[0] for k in KEEP])
96:@pytest.mark.parametrize("src", NOT_ENCOUNTER_SOURCES)
103:@pytest.mark.parametrize("opening", ["Account summary: Office visit charge $220.00.", "Charges: Office visit charge $220.00.", "Receipt: Office visit charge $220.00.",
115:@pytest.mark.parametrize("src,want", [(ER, "encounter"), ("Austin EMS run report", "encounter"), ("Capital PT, visit 9", "encounter"), ("Hill Country Pain Management, follow-up", "encounter"),
138:@pytest.mark.parametrize("ex", [
149:@pytest.mark.parametrize("ex", ["DOS 03/13/2026 office visit charge $220.00.", "Date of service 03/13/2026: office visit charge $220.00.", "Dates of service 03/13/2026, office visit charge $220.00.",
166:@pytest.mark.parametrize("ex,want", [
223:@pytest.mark.parametrize("src", ["Fennimoor Spine Clinic, superbill", "Fennimoor Spine Clinic, patient receipt", "Fennimoor Spine Clinic, charge summary", "Pharmacy receipt",
231:@pytest.mark.parametrize("src", ["Fennimoor Spine Clinic, EOB", "Fennimoor Spine Clinic, payment history", "Fennimoor Spine Clinic, HCFA", "Fennimoor Spine Clinic, balance due notice",
240:@pytest.mark.parametrize("hd", [
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:23.326Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/probe_t207_r2.py",
 "content": "\"\"\"T-207 r2 probes against a git-archive of 8cb5bd2. Usage: python -I probe_t207_r2.py <archive_dir>\"\"\"\nimport sys, datetime as dt\nroot = sys.argv[1]\nsys.path.insert(0, root)\nfrom app.backend import service_date as SD, store, export\n\nER = \"Austin ER visit\"\n\n\ndef res(ex, fig, src, rd):\n    return SD.resolve(ex, ex.index(fig), src, rd)\n\n\ndef line(tag, r):\n    print(f\"{tag} | {r['state']} | {r['first']} | {r['last']} | reason={r['reason']} | raw={r['raw']!r}\")\n\n\nstmt = dt.date(2026, 6, 30)\n# D1: five-year bound around 1830 days (statement 2026-06-30, itemized ledger)\nfor n in (1826, 1827, 1829, 1830, 1831, 1832):\n    d = stmt - dt.timedelta(days=n)\n    ex = f\"Itemized ledger. DOS {d.strftime('%m/%d/%Y')} office visit charge $220.00.\"\n    line(f\"D1 {n}d before ({d})\", res(ex, \"$220.00\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-30\"))\n# calendar five years: 2021-06-30 exact, 2021-06-29 (5y+1d), 2021-06-26 (5y+4d), 2021-06-25 (5y+5d)\nfor s in (\"06/30/2021\", \"06/29/2021\", \"06/26/2021\", \"06/25/2021\"):\n    ex = f\"Itemized ledger. DOS {s} office visit charge $220.00.\"\n    line(f\"D1cal {s}\", res(ex, \"$220.00\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-30\"))\n# no record date has no bound\nline(\"D1nodate 03/13/1998\", res(\"Itemized ledger. DOS 03/13/1998 office visit charge $220.00.\", \"$220.00\", \"Fennimoor Spine Clinic, itemized ledger\", None))\n\n# D2: rule (1) and (2)\nfor ex, rd in ((\"Itemized ledger. DOS 04/05/2026 - 13/05/2026 therapy $120.00.\", \"2026-06-30\"),\n               (\"Itemized ledger. DOS 13/05/2026 - 05/13/2026 therapy $120.00.\", \"2026-06-30\"),\n               (\"Itemized ledger. DOS 04/05/2026 - 06/05/2026 therapy $120.00.\", \"2026-06-30\"),\n               (\"Itemized ledger. DOS 04/05/2026 - 06/05/2026 therapy $120.00.\", \"2026-05-31\"),\n               (\"Itemized ledger. DOS 04/05/2026 therapy $120.00.\", \"2026-06-30\"),\n               (\"Itemized ledger. DOS 04/05/2026 therapy $120.00.\", \"2026-04-30\"),\n               (\"Itemized ledger. DOS 04/05/2026 therapy $120.00.\", None)):\n    line(f\"D2 rd={rd} {ex[16:60]}\", res(ex, \"$\", \"Fennimoor Spine Clinic, itemized ledger\", rd))\n\n# D3: encounter header date lent; labeled but unreadable date is not replaced\nfor tag, ex, src, rd in (\n    (\"D3 ER unlabeled\", \"Patient seen for neck pain. Office visit charge $240.00.\", ER, \"2026-01-09\"),\n    (\"D3 ER labeled-bad(2-digit)\", \"DOS 05/05/26 office visit charge $240.00.\", ER, \"2026-01-09\"),\n    (\"D3 ER labeled-after-record\", \"DOS 03/01/2026 office visit charge $240.00.\", ER, \"2026-01-09\"),\n    (\"D3 ER labeled-ok\", \"DOS 01/05/2026 office visit charge $240.00.\", ER, \"2026-01-09\"),\n    (\"D3 bill unlabeled\", \"Office visit charge $240.00.\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-01-09\"),\n    (\"D3 unknown type\", \"Office visit charge $240.00.\", \"Prescription slip\", \"2026-01-09\"),\n    (\"D3 ER no record date\", \"Office visit charge $240.00.\", ER, None),\n    (\"D3 Visit date prose not label\", \"Visit date: 01/05/2026 office visit charge $240.00.\", ER, \"2026-01-09\"),\n    (\"D3 Next DOS\", \"Next DOS 02/01/2026 office visit charge $240.00.\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-30\"),\n):\n    line(tag, res(ex, \"$240.00\", src, rd))\n\n# D4: store path: pos None on an encounter record whose excerpt LABELS a different date\nrec = {\"source\": ER, \"date_iso\": \"2026-01-09\", \"n\": 2}\nitem = {\"excerpt\": \"DOS 05/05/2026 office visit charge $240.00.\", \"ladder\": {}}\nfor tag, pos in ((\"D4 pos located\", 38), (\"D4 pos None\", None)):\n    ex = item[\"excerpt\"]\n    p = ex.index(\"$240.00\") if pos else None\n    d = store.charge_service_date(item, rec, p)\n    print(tag, \"|\", d[\"state\"], d[\"date_iso\"], d[\"reason\"], \"| text:\", d[\"text\"], \"| note:\", (d[\"confirm_note\"] or \"\")[:60])\nitem2 = {\"excerpt\": \"DOS 01/05/2026 office visit charge $240.00.\", \"ladder\": {}}\np = None\nd = store.charge_service_date(item2, rec, p)\nprint(\"D4b pos None, line labels 01/05/2026 (before header)\", \"|\", d[\"state\"], d[\"date_iso\"], d[\"reason\"], d[\"text\"])\nd = store.charge_service_date({\"excerpt\": \"DOS 03/01/2026 office visit charge $240.00.\", \"ladder\": {}}, rec, None)\nprint(\"D4c pos None, line labels 03/01/2026 (AFTER header)\", \"|\", d[\"state\"], d[\"date_iso\"], d[\"reason\"], d[\"text\"])\nd = store.charge_service_date({\"excerpt\": \"DOS 03/01/2026 office visit charge $240.00.\", \"ladder\": {}}, rec, \"DOS 03/01/2026 office visit charge $240.00.\".index(\"$240\"))\nprint(\"D4d pos located, same line\", \"|\", d[\"state\"], d[\"date_iso\"], d[\"reason\"], d[\"text\"][:70])\n\n# D5: UB-04 'statement period' (doc names only 'statement covers period')\nub = \"UB-04 Statement period 01/05/2026-01/09/2026. Rev 0450 emergency room $4,920.00.\"\nline(\"D5 ub04 'statement period'\", res(ub, \"$4,920.00\", \"Fennimoor Hospital, UB-04\", \"2026-02-15\"))\nub2 = \"UB-04 Statement covers period 01/05/2026-01/09/2026. Rev 0450 emergency room $4,920.00.\"\nline(\"D5 ub04 'statement covers period'\", res(ub2, \"$4,920.00\", \"Fennimoor Hospital, UB-04\", \"2026-02-15\"))\nub3 = \"Invoice. Statement period 01/05/2026-01/09/2026. CPT 99213 office visit $220.00.\"\nline(\"D5 non-ub 'statement period'\", res(ub3, \"$220.00\", \"Fennimoor Spine Clinic, invoice\", \"2026-02-15\"))\n\n# D6: heading set\nfor h in (\"Service From\", \"SVC To\", \"From Service\", \"Visit Date\", \"Date of Visit\", \"Encounter Date\", \"24A\", \"Posted\", \"Entry Date\"):\n    ex = f\"Itemized ledger\\n{h}\\tCPT\\tCharge\\n01/05/2026\\t99213\\t$220.00\"\n    line(f\"D6 heading {h}\", res(ex, \"$220.00\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-30\"))\n\n# D7: label tails the doc does not list\nfor tail in (\"DOS: \", \"DOS is \", \"DOS was \", \"DOS - \", \"DOS # \", \"DOS between \"):\n    ex = f\"Itemized ledger. {tail}01/05/2026 office visit charge $220.00.\"\n    line(f\"D7 label tail {tail!r}\", res(ex, \"$220.00\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-30\"))\n\n# D8: export.charge_when hand-built vs store path\nclass V(export.__dict__.get(\"View\", object)):\n    pass\n"
}
````

### User / tool · 2026-11-03T02:03:23.431Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/probe_t207_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:25.080Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/probe_t207_r2.py",
 "old_string": "\n# D8: export.charge_when hand-built vs store path\nclass V(export.__dict__.get(\"View\", object)):\n    pass\n",
 "new_string": ""
}
````

### User / tool · 2026-11-03T02:03:25.197Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/probe_t207_r2.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:28.532Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-207-r2/probe_t207_r2.py $S/t207r2 2>&1 | tee artifacts/review-evidence/T-207-r2/probe_t207_r2.out | cut -c1-260"
}
````

### User / tool · 2026-11-03T02:03:28.990Z

**tool result**
````
D1 1826d before (2021-06-30) | stated | 2021-06-30 | None | reason=None | raw=''
D1 1827d before (2021-06-29) | stated | 2021-06-29 | None | reason=None | raw=''
D1 1829d before (2021-06-27) | stated | 2021-06-27 | None | reason=None | raw=''
D1 1830d before (2021-06-26) | stated | 2021-06-26 | None | reason=None | raw=''
D1 1831d before (2021-06-25) | not_stated | None | None | reason=implausible | raw='06/25/2021'
D1 1832d before (2021-06-24) | not_stated | None | None | reason=implausible | raw='06/24/2021'
D1cal 06/30/2021 | stated | 2021-06-30 | None | reason=None | raw=''
D1cal 06/29/2021 | stated | 2021-06-29 | None | reason=None | raw=''
D1cal 06/26/2021 | stated | 2021-06-26 | None | reason=None | raw=''
D1cal 06/25/2021 | not_stated | None | None | reason=implausible | raw='06/25/2021'
D1nodate 03/13/1998 | stated | 1998-03-13 | None | reason=None | raw=''
D2 rd=2026-06-30  DOS 04/05/2026 - 13/05/2026 therapy $120.00 | stated | 2026-05-04 | 2026-05-13 | reason=None | raw=''
D2 rd=2026-06-30  DOS 13/05/2026 - 05/13/2026 therapy $120.00 | not_stated | None | None | reason=ambiguous_numeric | raw='13/05/2026 - 05/13/2026'
D2 rd=2026-06-30  DOS 04/05/2026 - 06/05/2026 therapy $120.00 | not_stated | None | None | reason=ambiguous_numeric | raw='04/05/2026 - 06/05/2026'
D2 rd=2026-05-31  DOS 04/05/2026 - 06/05/2026 therapy $120.00 | stated | 2026-05-04 | 2026-05-06 | reason=None | raw=''
D2 rd=2026-06-30  DOS 04/05/2026 therapy $120.00. | not_stated | None | None | reason=ambiguous_numeric | raw='04/05/2026'
D2 rd=2026-04-30  DOS 04/05/2026 therapy $120.00. | stated | 2026-04-05 | None | reason=None | raw=''
D2 rd=None  DOS 04/05/2026 therapy $120.00. | not_stated | None | None | reason=ambiguous_numeric | raw='04/05/2026'
D3 ER unlabeled | stated | 2026-01-09 | None | reason=None | raw=''
D3 ER labeled-bad(2-digit) | not_stated | None | None | reason=two_digit_year | raw='05/05/26'
D3 ER labeled-after-record | stated | 2026-01-03 | None | reason=None | raw=''
D3 ER labeled-ok | stated | 2026-01-05 | None | reason=None | raw=''
D3 bill unlabeled | not_stated | None | None | reason=no_date | raw=''
D3 unknown type | not_stated | None | None | reason=no_date | raw=''
D3 ER no record date | not_stated | None | None | reason=no_date | raw=''
D3 Visit date prose not label | stated | 2026-01-09 | None | reason=None | raw=''
D3 Next DOS | not_stated | None | None | reason=non_service_date | raw='02/01/2026'
D4 pos located | not_stated None implausible | text: date of service [__________] (statement dated January 9, 2026) | note: The quote labels 05/05/2026 as the date of service, but that
D4 pos None | stated 2026-01-09 None | text: January 9, 2026 | note: 
D4b pos None, line labels 01/05/2026 (before header) | stated 2026-01-09 None January 9, 2026
D4c pos None, line labels 03/01/2026 (AFTER header) | stated 2026-01-09 None January 9, 2026
D4d pos located, same line | stated 2026-01-03 None January 3, 2026
D5 ub04 'statement period' | stated | 2026-01-05 | 2026-01-09 | reason=None | raw=''
D5 ub04 'statement covers period' | stated | 2026-01-05 | 2026-01-09 | reason=None | raw=''
D5 non-ub 'statement period' | not_stated | None | None | reason=no_date | raw=''
D6 heading Service From | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading SVC To | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading From Service | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading Visit Date | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading Date of Visit | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading Encounter Date | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading 24A | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D6 heading Posted | not_stated | None | None | reason=non_service_date | raw='01/05/2026'
D6 heading Entry Date | not_stated | None | None | reason=non_service_date | raw='01/05/2026'
D7 label tail 'DOS: ' | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D7 label tail 'DOS is ' | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D7 label tail 'DOS was ' | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D7 label tail 'DOS - ' | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D7 label tail 'DOS # ' | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
D7 label tail 'DOS between ' | not_stated | None | None | reason=ambiguous_numeric | raw='01/05/2026'
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:41.223Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"excerpt_start\" -r app/backend app/db | cut -c1-230 | head -30; grep -n \"def body_offset\" -A12 app/backend/generator.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:03:41.344Z

**tool result**
````
app/backend/store.py:110:    start, raw = item.get("excerpt_start"), item.get("text") or ""
app/backend/trace.py:404:    return _span(cx, rid, ed.get("excerpt_start", row.get("excerpt_start")), ed.get("excerpt_end", row.get("excerpt_end")), ed.get("excerpt", row.get("excerpt")))
app/backend/trace.py:641:    exc = _span(cx, rid, row.get("excerpt_start"), row.get("excerpt_end"), row.get("excerpt"))
app/backend/present.py:59:            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
app/backend/present.py:149:            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
app/backend/present.py:538:            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
app/backend/review.py:527:                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
app/backend/review.py:764:        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
app/backend/overlap.py:134:        if rec is None or a["excerpt_start"] is None:
app/backend/overlap.py:139:                     "label": AM._label(raw, a["excerpt_start"]).replace("Excerpt:", "").strip(' "'), "after": _clause_after(raw, a["excerpt_end"]),
app/backend/generator.py:68:        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
app/backend/generator.py:142:             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
app/backend/generator.py:189:    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
app/backend/pipeline.py:214:                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
app/backend/pipeline.py:218:                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
app/backend/pipeline.py:417:    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
app/db/schema.sql:21:  provider TEXT, summary TEXT, excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER,
app/db/schema.sql:30:  excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
app/backend/reclassify.py:63:    if rec is not None and row.get("excerpt_start") is not None:
app/backend/reclassify.py:64:        i = row["excerpt_start"] - generator.body_offset(rec)
18:def body_offset(record: dict) -> int:
19-    """Absolute offset (in the normalised case text) where record['excerpt'] starts."""
20-    block = record.get("text", "")
21-    m = _EXC.search(block)
22-    base = record.get("char_start", 0)
23-    if m and block[m.end():].startswith(record["excerpt"][:20]):
24-        return base + m.end()
25-    i = block.find(record["excerpt"])
26-    return base + (i if i >= 0 else 0)
27-
28-
29-def extract_prompt(record: dict, nonce: str) -> str:
30-    return (f"SOURCE LABEL (context only; do not copy):\n{injection.wrap(record['source'], nonce)}\n"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:48.572Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -rn \"charge_service_date\" tests | cut -c1-240 | head -20"
}
````

### User / tool · 2026-11-03T02:03:48.707Z

**tool result**
````
tests/unit/test_t202_r4_encounter.py:6:Each fixture runs the shipped path (store.charge_service_date -> export.build_export). Code only."""
tests/unit/test_t202_r4_encounter.py:29:        d = store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, rec, a["start"])
tests/unit/test_t202_r4_encounter.py:44:    return store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, {"source": source, "date_iso": rec_date}, a["start"])
tests/unit/test_t202_charge_service_dates.py:80:    assert store.charge_service_dates({"excerpt": UB, "value_cents": 210500}, rec, UB.index("$2,105.00")) == ("2026-06-09", "2026-06-12")
tests/unit/test_t200_undated_charge_label.py:48:def test_charge_service_dates_reads_the_line_not_the_record_date():
tests/unit/test_t200_undated_charge_label.py:51:    assert store.charge_service_dates({"excerpt": LEDGER, "value_cents": 25000}, rec, pos) == (None, None)
tests/unit/test_t200_undated_charge_label.py:53:    assert store.charge_service_dates({"excerpt": dated, "value_cents": 25000}, rec, dated.index("$250.00")) == ("2026-03-27", None)
tests/unit/test_t200_undated_charge_label.py:56:    assert store.charge_service_dates({"excerpt": note, "value_cents": 25000}, note_rec, note.index("$250.00")) == ("2026-03-27", None)      # a dated encounter note: the record is the visit
tests/unit/test_t200_undated_charge_label.py:59:def test_charge_service_dates_when_the_line_cannot_be_read():
tests/unit/test_t200_undated_charge_label.py:62:    assert store.charge_service_dates(counted, {"source": "s", "date_iso": "2026-06-15"}, None) == (None, None)
tests/unit/test_t200_undated_charge_label.py:63:    assert store.charge_service_dates({"excerpt": "x"}, {"source": "Capital PT, visit 9", "date_iso": "2026-06-15"}, None) == ("2026-06-15", None)
tests/unit/test_t200_undated_charge_label.py:64:    assert store.charge_service_dates({"excerpt": "x"}, {"source": "s", "date_iso": "2026-06-15"}, None) == (None, None)          # D-071 amendment 2: a record of unknown type never lends its 
tests/unit/test_t202_r3_allow_list.py:9:sentences, the 1998 and 2031 dates, 'Mar 5, 26', the all-vs-any period rule) is a fixture here. Each runs the shipped path (store.charge_service_dates -> export.build_export). Code only."""
tests/unit/test_t202_r3_allow_list.py:34:        d = store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, rec, a["start"])
tests/unit/test_t202_r3_allow_list.py:44:    """store.charge_service_date for the figure (what the case view and the letter share)."""
tests/unit/test_t202_r3_allow_list.py:46:    return store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, {"source": source, "date_iso": rec_date}, a["start"])
tests/unit/test_t202_r3_allow_list.py:332:        d = store.charge_service_date({"excerpt": ex, "value_cents": a["cents"]}, rec, a["start"])
tests/unit/test_t202_r2_service_date_layouts.py:4:Each case runs the shipped path (store.charge_service_dates -> export.build_export), so what is asserted is the line the letter prints. Code only."""
tests/unit/test_t202_r2_service_date_layouts.py:30:        d = store.charge_service_date({"excerpt": excerpt, "value_cents": a["cents"]}, rec, a["start"])
tests/unit/test_t202_r2_service_date_layouts.py:188:    assert store.charge_service_dates({"excerpt": "x"}, rec, None) == (None, None)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:03:59.797Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"\\\"amount\\\"\" app/backend/*.py | grep -i \"insert\\|add_item\\|create\\|put\" | cut -c1-200 | head; sed -n 405,425p app/backend/pipeline.py | cut -c1-200; grep -n \"amount_pos\" -r app | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:03:59.957Z

**tool result**
````
    _store_run_checks(conn, cid, ing["records"], "pending")
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"], "translated": any(language.translated_record(by_n.get(n)) for n in a["record_nos"])})      # D-050
    a["state"], a["reasons"] = state, reasons
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
app/backend/store.py:107:def amount_pos(item: dict, rec):
app/backend/store.py:194:                 excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, r))
app/backend/present.py:86:    return AM.not_counted(row["excerpt"], row["text"], row["value_cents"], (rec or {}).get("source"), (rec or {}).get("date_iso"), store.amount_pos(row, rec),
app/backend/present.py:152:            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:10.956Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py -q -p no:cacheprovider 2>&1 | tail -4"
}
````

### User / tool · 2026-11-03T02:04:18.893Z

**tool result**
````
........................................................................ [ 63%]
........................................................................ [ 84%]
.....................................................                    [100%]
341 passed in 7.55s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:22.910Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t202_r4_encounter.py -q -p no:cacheprovider --collect-only 2>&1 | tail -2; for f in test_t202_r3_allow_list test_t200_undated_charge_label; do /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/$f.py -q -p no:cacheprovider --collect-only 2>&1 | tail -1; done"
}
````

### User / tool · 2026-11-03T02:04:24.324Z

**tool result**
````
133 tests collected in 0.16s
141 tests collected in 0.16s
6 tests collected in 0.34s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:27.496Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep -i \"T-202\"; ls artifacts/review-evidence | grep -i \"202\""
}
````

### User / tool · 2026-11-03T02:04:34.221Z

**tool result**
````
T-202-paralegal-r2.md
T-202-paralegal-r3.md
T-202-paralegal.md
T-202-staff-engineer-r2.md
T-202-staff-engineer-r3.md
T-202-staff-engineer.md
T-202-paralegal
T-202-paralegal-r2
T-202-paralegal-r3
T-202-paralegal-r4
T-202-staff
T-202-staff-r2
T-202-staff-r3
T-202-staff-r4
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:36.509Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && ls T-202-staff-r3 T-202-staff-r4 T-202-paralegal-r3 T-202-paralegal-r4 | head -60; git log --oneline -3 -- T-202-staff-r4 T-202-paralegal-r4"
}
````

### User / tool · 2026-11-03T02:04:36.635Z

**tool result**
````
T-202-paralegal-r3:
before_t202.out
before_t202.py
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
db
draft-T-202-paralegal-r3.md
h.py
letter_check.out
letters
letters_dump_r3.out
letters_dump_r3.py
letters_vs_r2.out
lib10-s3-00-a2.png
lib10-s3-01-a3.png
lib10-s3-02-a4.png
lib10-s3-03-a5.png
lib10-s3-04-a1.png
lib10-s3-05-a6.png
lib10-s3-06-a7.png
lib10-s3-07-a8.png
lib10-s3-08-a9.png
lib10-s3-09-a10.png
lib10-s3-10-a11.png
lib10-step2-done.png
lib10-step3-done.png
lib10-step4.png
lib11-s3-00-a1.png
lib11-s3-01-a2.png
lib11-s3-02-a3.png
lib11-s3-03-a4.png
lib11-s3-04-a5.png
lib11-s3-05-a6.png
lib11-s3-06-a7.png
lib11-s3-07-a8.png
lib11-step2-done.png
lib11-step3-done.png
lib11-step4.png
lib14-s3-00-a1.png
lib14-s3-01-a2.png
lib14-s3-02-a4.png
lib14-s3-03-a3.png
lib14-s3-04-a5.png
lib14-step2-done.png
lib14-step3-done.png
lib14-step4.png
p01.out
p01_cases.py
probe_r3.out
probe_r3.py
probe_r3b.out
probe_r3b.py
probe_r3c.out
probe_r3c.py
profile
pytest-t202.out
run.log
sample-s3-00-a1.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:38.528Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-202-staff-r4; sed -n 1,12p tests/unit/test_t202_r4_encounter.py | cut -c1-400"
}
````

### User / tool · 2026-11-03T02:04:38.608Z

**tool result**
````
a
e
e2e.out
m
orig
p
s
unit.out
"""T-202 round 4 (D-071 amendment 2, final). Every probe from the round 3 paralegal and staff reviews is a fixture here, and the T-209 r2 dotted-leader case.
  (a) a record's own date is a service date ONLY for a positively identified encounter record (visit, ER, clinic, therapy, ambulance-run note ... declared in
      app/backend/encounter_types.json). A bill, receipt, superbill, charge summary, an administrative paper or a record of unknown type never lends its header date.
  (b) in prose only 'date of service', 'dates of service', 'DOS' and 'service date' are labels. 'visit date', 'seen on', a bare 'date' are not (they name next or prior visits, entry dates ...).
  (c) letter_check keeps its own scanner but reads the same declared table, and accepts the blank only in its exact form.
Each fixture runs the shipped path (store.charge_service_date -> export.build_export). Code only."""
import re

import pytest

from app.backend import amounts as AM, export, service_date as SD, store
from evals import letter_check as LC
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:44.874Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-202 2>&1 | tail -40 | cut -c1-300; ls -la artifacts/review-evidence/T-202-staff-r4/p | head"
}
````

### User / tool · 2026-11-03T02:04:45.018Z

**tool result**
````
    - [blocker] A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date — fix: Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or
    - [major] Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter — fix: Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; servic
    - [minor] The not-stated string differs from the one quoted in the D-071 amendment — fix: Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.
    - [minor] A ledger column headed 'Trans Date' is read as the date of service — fix: Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.
    - [minor] A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill — fix: Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The
    - [minor] Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now) — fix: Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm
    - [minor] Carried from round 1: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T00:29:34Z orchestrator: assigned: backend
- 2026-11-03T00:29:34Z orchestrator: Round 3 queued until staff r2 lands. Paralegal r2 blocker: a date in prose (birth/injury/onset/referral/order) prints as DOS -> per D-071 amendment a date counts only if tied to a DOS column header, a DOS/service label ('DOS', 'date of service', 'service date', '
- 2026-11-03T00:30:26Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r2.md
- 2026-11-03T00:30:26Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of s
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date
- 2026-11-03T00:45:37Z backend: (correction: the two empty notes above were a shell slip; the exact LLM_VS_CODE text for the architect is in the note just above and on T-207.)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints "(statement dated X; service date not s
- 2026-11-03T01:25:40Z backend: AC 1 checked: r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->a
- 2026-11-03T01:25:40Z backend: moved in_progress -> in_review
- 2026-11-03T01:25:49Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer
- 2026-11-03T01:34:13Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r3.md; round 3; findings:
    - [blocker] A 'visit date' / 'seen on' label naming another visit (next, last, previous, initial) prints that visit's date as the charge's date of service; in a visit note it overrides the note's own correct date (regression vs pre-T-202), and letter_check enforces the wrong date — fix: In a d
    - [minor] The note says 'The line states no date of service' or 'not labeled as a date of service' for lines that do label one in a form the code does not read (DOS with ordinal, UB-04 FL6 six-digit period, CMS-1500 Item 24A) — fix: When a service label (DOS, 24A, FL6 / statement covers period
    - [minor] Internal notes tell me to 'fill it from the quote' for lines whose quote has no date, and the one-date blank does not fit a multi-visit line — fix: Word the notes line by reason. no_date / non_service_date: 'the bill line gives no date; take it from the matching visit note or request
    - [minor] Carried from rounds 1 and 2: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T01:34:13Z orchestrator: assigned: backend
- 2026-11-03T01:34:13Z orchestrator: Paralegal r3 blocker: 'next visit date 01/16/2026' in an ER note dates the ER charge Jan 16 (label 'visit date' matched). Round 4 (§7.4 decision) queued until staff r3 lands.
- 2026-11-03T01:37:28Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r3.md
- 2026-11-03T01:37:28Z backend: moved changes_requested -> in_progress
- 2026-11-03T01:58:28Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, T-207), after T-202 r4 commit 8cb5bd2 (D-071 amendment 2). Row 2: replace "by a service label in its clause (DOS, date of service, service date, seen on, visit date)" with "by a service label in its clause (in prose onl
- 2026-11-03T01:58:28Z backend: AC 1 checked: r4 8cb5bd2 (git archive): unit 6266 passed 12 skipped 1 failed (test_e2e_contract test ids, fails identically at parent 8521562, not my files), guided e2e 145 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r4_encounter.p
- 2026-11-03T01:58:31Z backend: moved in_progress -> in_review
- 2026-11-03T01:58:42Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r4, 8cb5bd2, D-071 amendment 2): (a) service_date.record_kind reads the one declared table app/backend/encounter_types.json; only an identified encounter (visit/ER/clinic/therapy/imaging/EMS) lends its header date, bills/receipts/superbills/charge summaries/admin papers/unknown never d
How verified (git archive 8cb5bd2): unit 6266 passed, 12 skipped, 1 failed (4 shards; the 1 is tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, brand/footer-note/draft-done/demo-badge/btn-draft test ids, fails the same at parent 8521562 and touches none of my files); guided e2e 145 p
Judgment calls: (1) bills keep 'visit of', 'the run of', 'rendered on', 'service period' (case_09 and lib14 goldens depend on them; in a non-bill they are not labels). If the orchestrator wants only the four, case_09 and lib14 print the blank: one line in _SVC_BILL. (2) The plausibility rule (not af
What's left: architect T-207 text (note on the card); paralegal minors from r3 (notes wording by reason, 24A/FL6 note, quote span) not done; the CMS-1500 export-gate question is outside T-202. What surprised me: the opening scan flagged my own ER fixture; the Write tool rewrites \u escapes in script

total 264
drwxr-xr-x@  28 arsis  staff    896 Nov  2 19:59 .
drwxr-xr-x@  10 arsis  staff    320 Nov  2 20:02 ..
drwxr-xr-x@   7 arsis  staff    224 Nov  2 19:50 .claude
-rw-r--r--@   1 arsis  staff    434 Nov  2 19:50 .dockerignore
-rw-r--r--@   1 arsis  staff   1586 Nov  2 19:50 .env.example
-rw-r--r--@   1 arsis  staff    561 Nov  2 19:50 .gitignore
-rw-r--r--@   1 arsis  staff   6786 Nov  2 19:50 CLAUDE.md
-rw-r--r--@   1 arsis  staff   1838 Nov  2 19:50 Dockerfile
-rw-r--r--@   1 arsis  staff  83742 Nov  2 19:50 MASTER_PROMPT.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:51.728Z

**tool call — Bash**
````
{
 "command": "grep -o \"AC 1 checked: r4 8cb5bd2.*\" board/cards/T-202.md | head -2 | cut -c1-1800; grep -c \"\" board/cards/T-207.md; python3 tools/board.py show T-207 2>&1 | sed -n 1,40p | cut -c1-260"
}
````

### User / tool · 2026-11-03T02:04:51.876Z

**tool result**
````
AC 1 checked: r4 8cb5bd2 (git archive): unit 6266 passed 12 skipped 1 failed (test_e2e_contract test ids, fails identically at parent 8521562, not my files), guided e2e 145 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r4_encounter.py 131 tests (86 red before); 24 of 25 mutants killed (25th equivalent); 150 corpus letter+notes blobs byte-identical
53
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
updated_at: "2026-11-03T02:00:59Z"
claimed_by: "architect"
claimed_at: "2026-11-03T00:46:49Z"
rounds: 1
commits: ["901ad5a", "fc37fbc", "efda639"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-207-staff-engineer.md", "at": "2026-11-03T01:43:17Z"}
ac:
  - {"n": 1, "text": "docs/LLM_VS_CODE.md row 2 and row 3 carry the text in the T-202 note from backend (allow-list, as-written form, not-stated form, validation), and say entry dates stay on the stricter ambiguous-never-guessed rule", "done": true, "evidence"
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a ser
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (po
- 2026-11-03T00:46:49Z architect: claimed
- 2026-11-03T00:47:32Z architect: AC 1 checked: docs/LLM_VS_CODE.md rows 2 and 3, commit 901ad5a; text per T-202 note + D-071 amendment/clarification/addendum
- 2026-11-03T00:47:32Z architect: moved in_progress -> in_review
- 2026-11-03T00:47:37Z orchestrator: The fillable blank is in T-202 r3 scope (message sent to the backend worker); review T-207 against the T-202 r3 commit.
- 2026-11-03T00:47:37Z orchestrator: review dispatched: staff-engineer-reviewer (queued: after T-202 r3 lands)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints
- 2026-11-03T01:26:49Z architect: Applied the backend correction (row 3, 'shows as written' and 'service date not stated' sentences replaced with the fillable blank; Validation cell 28 -> 24 mutants) to docs/LLM_VS_CODE.md, matching code at 973b542. Commit fc3
- 2026-11-03T01:26:55Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-03T01:43:17Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-207-staff-engineer.md; round 1; findings:
    - [major] Row 2 says a two-reading date is certain only by the statement rule; code also settles it from the other end of the same period — fix: Architect amends row 2 to state the same-period locale rule (cite D-071 amendment 'no locale rule from the re
    - [major] Five-year bound is 1830 days, not 'more than five years'; no test sits at the boundary — fix: Compare calendar years (statement date minus five years, same month and day, 29 Feb handled) instead of 366-day arithmetic; keep 1998 and 2031.
    - [major] A charge with no labeled date takes the visit note's header date; row 2 says only the allow-list counts — fix: Chris rules (Q1). If yes, row 2 names the encounter-header rule and cites R-TL-3. The pos-None branch at store.py:133 then either fol
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:04:56.749Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -rln -i \"mutant\\|mutation\" tests evals tools 2>/dev/null | head; sed -n 405,470p evals/letter_check.py | cut -c1-230"
}
````

### User / tool · 2026-11-03T02:04:56.854Z

**tool result**
````
tests/unit/test_t208_ai_wording.py
tests/unit/test_summary_trim.py
tests/unit/test_billing.py
tests/unit/test_uncovered.py
tests/unit/test_t133_lexicon.py
tests/unit/test_t141_checks_per_case.py
tests/unit/test_t132_attribution_unit.py
tests/unit/test_t139_unmarked.py
tests/unit/test_t159_flag_audit.py
tests/unit/test_dismissal_patterns.py
        if len(heads) == len(cells):
            for (cs, ct), (hs, ht) in zip(cells, heads):
                if cs <= col < cs + len(ct):
                    return ht
        return min(heads, key=lambda h: abs(h[0] - col))[1]
    return ""


def charge_date_violations(letter: str, records) -> list:
    """D-071 amendment, round 3 (allow-list): every charge line's printed date against THAT line's own quote (plus, for a quote with no labeled date, the bill's period before it).
    `records`: the case's [{n, source, date_iso, excerpt}]. Per line, the quote's LABELED dates are those with a service phrase right before them or a table heading over them that
    names the service; every other date in it (birth, injury, onset, referral, order, entry, transaction, posted, statement, unlabeled) is not a service date.
      - labeled dates that have exactly one certain reading (one date or period, one reading, not after its statement, not years before it) -> the line prints exactly that, whole;
      - labeled dates that are doubtful (several readings, two-digit year, no year, impossible, several dates, implausible) -> the line prints the blank, nothing else;
      - no labeled date in the quote, in a bill -> the one period the bill states before it (whole), else the blank 'date of service [__________] (statement dated X)' with X the
        record's date; in a visit note (not a bill) -> the note's own date (the blank is a violation there).
    A date printed where the quote labels none, a blank above a certain labeled date, and a statement date that is not the record's are violations."""
    norm = lambda t: " ".join(str(t).split())
    out = []
    for head, quote in charge_lines(letter):
        parsed = _head_dates(re.sub(r": \$[\d,]+\.\d\d$", "", head))
        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
        if parsed is None:
            out.append(f"charge line has no readable date form: {head}")
            continue
        if not recs:
            out.append(f"charge line's quote is in no record: {head}")
            continue
        kind, first, last = parsed
        problems = []
        for r in recs:
            ex, rd = r["excerpt"], r.get("date_iso")
            if kind == "blank":                                                                  # D-071 amendment 2 (c): the blank only in its exact form, anchored at both ends
                from datetime import date
                d = date.fromisoformat(rd) if rd else None
                want_head = f"{norm(r.get('source') or '')}, {BLANK}" + (f" (statement dated {d.strftime('%B')} {d.day}, {d.year})" if d else "")
                if norm(re.sub(r": \$[\d,]+\.\d\d$", "", head)) != want_head:
                    problems.append("the blank is not in its exact form (source, then 'date of service [__________]', then the record's statement date)")
                    continue
            kind_r = _record_kind(r.get("source"), ex)
            bill, lends = kind_r == "bill", kind_r == "encounter"          # only an encounter record lends its own date; the rest need a label
            ub = bool(_UB_WORD.search(r.get("source") or "") or _UB_WORD.search(ex))
            n_ex, n_q = norm(ex), norm(quote)
            before = n_ex[:n_ex.index(n_q)]
            units = _written(n_q)
            marks = _marked(n_q, units, _SERVICE_PHRASES + (_BILL_PHRASES if bill else ()) + (_UB_PHRASES if ub else ()), before + n_q, len(before))
            for k, u in enumerate(units):                                                       # a table heading over the date that names the service labels it too
                if not marks[k]:
                    marks[k] = bool(_names_service(_heading_over(ex, quote, u["start"])))
            lab = [u for u, m in zip(units, marks) if m]
            if lab:
                reads = [_readings(u, rd) for u in lab]
                same = {x for rr in reads for x in rr}
                certain = all(len(rr) == 1 for rr in reads) and len(same) == 1
                texts = sorted(norm(n_q[u["start"]:u["end"]]) for u in lab)
                if certain:
                    if kind in ("range", "one"):
                        if (first, last) != next(iter(same)):
                            problems.append(f"the quote's labeled date of service reads {next(iter(same))[0]}" + (f" to {next(iter(same))[1]}" if next(iter(same))[1] else ""))
                    else:
                        problems.append("the quote labels one certain date of service and the line prints a blank")
                elif kind != "blank":
                    problems.append("the quote labels a date of service the writing leaves doubtful (" + ", ".join(texts) + ") and the line prints a date")
                elif first and first != rd:
                    problems.append("the statement date is not the record's date")
                continue
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:05:03.657Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"service_date\\|store\\.\\|charge_service\" evals/letter_check.py | cut -c1-200; grep -n \"BLANK\\s*=\" evals/letter_check.py; cd /Users/arsis/zlayt-pm-project && cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check 2>&1 | tail -6"
}
````

### User / tool · 2026-11-03T02:05:16.608Z

**tool result**
````
22:has its own scanner and shares no code with the production parser (app/backend/service_date.py), so a parser bug cannot hide itself.
225:# the production parser (app/backend/service_date.py): its own small scanner, its own string rules, enumerating every reading a written date allows.
510:            case = store.export_case(conn, cid)
184:BLANK = "date of service [__________]"
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:05:39.439Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/mutants_t207_r2.py",
 "content": "\"\"\"T-207 r2 mutants on a scratch git-archive copy of 8cb5bd2. Usage: python -I mutants_t207_r2.py <archive_dir> <venv_python>\nEach mutant is one exact-string replacement (asserted to occur once), run against the five date test files, then restored.\"\"\"\nimport pathlib, subprocess, sys\n\nroot = pathlib.Path(sys.argv[1])\npy = sys.argv[2]\nTESTS = [\"tests/unit/test_t202_r2_service_date_layouts.py\", \"tests/unit/test_t202_r3_allow_list.py\", \"tests/unit/test_t202_r4_encounter.py\",\n         \"tests/unit/test_t202_charge_service_dates.py\", \"tests/unit/test_t200_undated_charge_label.py\"]\nSD, ST, EX = \"app/backend/service_date.py\", \"app/backend/store.py\", \"app/backend/export.py\"\nM = [\n    (\"B1 bound 366 -> 365 days per year (1825 not 1830)\", SD, \"days=366 * _YEARS_BEFORE\", \"days=365 * _YEARS_BEFORE\"),\n    (\"B2 bound >= -> > (day 1830 refused)\", SD, \"_dt.date.fromisoformat(first) >= r - _dt.timedelta\", \"_dt.date.fromisoformat(first) > r - _dt.timedelta\"),\n    (\"B3 _YEARS_BEFORE 5 -> 4\", SD, \"_YEARS_BEFORE = 5 \", \"_YEARS_BEFORE = 4 \"),\n    (\"B4 _YEARS_BEFORE 5 -> 6\", SD, \"_YEARS_BEFORE = 5 \", \"_YEARS_BEFORE = 6 \"),\n    (\"B5 on-or-before: (last or first) <= ref -> < ref\", SD, \"(last or first) <= ref and\", \"(last or first) < ref and\"),\n    (\"B6 no record date has no bound -> bound refuses\", SD, \"    if not ref:\\n        return True\\n    r = _dt.date\", \"    if not ref:\\n        return False\\n    r = _dt.date\"),\n    (\"R1 rule2 on-or-before -> before\", SD, \"t.ambiguous[o] <= ref for t in amb\", \"t.ambiguous[o] < ref for t in amb\"),\n    (\"R2 rule2 no record date -> guess (feasible when not ref picks first)\", SD, \"if len(feasible) != 1:\", \"if len(feasible) != 1 and ref:\"),\n    (\"R3 rule1 two ends forcing different orders -> read\", SD, \"if len(determined) > 1:\", \"if len(determined) > 2:\"),\n    (\"K1 unknown type lends header date\", SD, 'return \"encounter\" if (_hit(_ENC, src) or _ABBR.search(src)) else \"other\"', 'return \"encounter\"'),\n    (\"K2 abbreviations (ER/EMS/PT) not recognised\", SD, \"or _ABBR.search(src))\", \"or False)\"),\n    (\"K3 admin check removed\", SD, \"if _hit(_ADMIN, src) or _hit(_ADMIN, opening):\", \"if False:\"),\n    (\"K4 bill opening-of-excerpt scan removed\", SD, \"or _hit(_FIN, opening):\", \"or False:\"),\n    (\"L1 'visit date' becomes a prose label\", SD, 'r\"(?:\\\\bdos|\\\\bdates?(?:\\\\(s\\\\))?\\\\s+of\\\\s+service|\\\\bservice\\\\s+dates?)\"', 'r\"(?:\\\\bdos|\\\\bvisit\\\\s+date|\\\\bdates?(?:\\\\(s\\\\))?\\\\s+of\\\\s+service|\\\\bservice\\\\s+dates?)\"'),\n    (\"L2 'next' prefix guard removed\", SD, \"(?<!next )\", \"\"),\n    (\"L3 heading 'encounter date' dropped\", SD, \"|encounter\\\\s+date|\", \"|\"),\n    (\"L4 heading 'date of visit' dropped\", SD, \"|date\\\\s+of\\\\s+visit|\", \"|\"),\n    (\"L5 heading 24A dropped\", SD, \"|\\\\b24\\\\s*-?a\\\\b\", \"\"),\n    (\"H1 labeled-but-unreadable in encounter falls to header date\", SD, \"            return _apply(out, _decide(lab, own, date_iso))\", \"            r_ = _decide(lab, own, date_iso)\\n            if r_[0] == 'ok': return _apply(out, r_)\"),\n    (\"N1 counted undated charge gets a note\", ST, \"if not stated and not counted_undated:\", \"if not stated:\"),\n    (\"N2 pos None encounter does not lend header date\", ST, \"if (encounter and rd) else dict(none)\", \"if False else dict(none)\"),\n    (\"N3 swap the two note asks\", SD, \"reason in WRITTEN else _ASK_NONE\", \"reason not in WRITTEN else _ASK_NONE\"),\n    (\"E1 hand-built case without dos_iso -> blank instead of record date\", EX, 'if \"dos_iso\" not in a:\\n            return f\"{src}, {_long_date(self.rec_date(n))}\"', 'if False:\\n            return f\"{src}, {_long_date(self.rec_date(n))}\"'),\n    (\"E2 blank drops the statement date\", SD, 'return f\"{BLANK} (statement dated {display(statement_iso)})\"', \"return BLANK\"),\n    (\"J1 opening_chars 40 -> 0 (excerpt opening never scanned)\", \"app/backend/encounter_types.json\", '\"opening_chars\": 40', '\"opening_chars\": 0'),\n]\nonly = sys.argv[3:]\nfor name, rel, old, new in M:\n    if only and not any(name.startswith(o) for o in only):\n        continue\n    p = root / rel\n    src = p.read_text(encoding=\"utf-8\")\n    if src.count(old) < 1:\n        print(f\"{name} | NOT APPLIED (pattern absent)\")\n        continue\n    if src.count(old) > 1 and not name.startswith((\"L2\",)):\n        print(f\"{name} | NOT APPLIED (pattern ambiguous x{src.count(old)})\")\n        continue\n    p.write_text(src.replace(old, new), encoding=\"utf-8\")\n    assert p.read_text(encoding=\"utf-8\") != src\n    try:\n        r = subprocess.run([py, \"-m\", \"pytest\", *TESTS, \"-q\", \"-x\", \"-p\", \"no:cacheprovider\"], cwd=root, capture_output=True, text=True, timeout=300)\n        tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1]\n        print(f\"{name} | {'KILLED' if r.returncode else 'SURVIVED'} | {tail}\", flush=True)\n    finally:\n        p.write_text(src, encoding=\"utf-8\")\n"
}
````

### User / tool · 2026-11-03T02:05:39.535Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/mutants_t207_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:05:48.043Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-207-r2/mutants_t207_r2.py $S/t207r2 /Users/arsis/zlayt-pm-project/.venv/bin/python 2>&1 | tee artifacts/review-evidence/T-207-r2/mutants_t207_r2.out | cut -c1-230; diff -rq <(cd $S/t207r2 && git -C /Users/arsis/zlayt-pm-project show 8cb5bd2:app/backend/service_date.py | md5) <(md5 < $S/t207r2/app/backend/service_date.py) && echo restored",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:08:02.676Z

**tool result**
````
B1 bound 366 -> 365 days per year (1825 not 1830) | SURVIVED | 341 passed in 7.38s
B2 bound >= -> > (day 1830 refused) | SURVIVED | 341 passed in 7.54s
B3 _YEARS_BEFORE 5 -> 4 | SURVIVED | 341 passed in 7.34s
B4 _YEARS_BEFORE 5 -> 6 | SURVIVED | 341 passed in 8.01s
B5 on-or-before: (last or first) <= ref -> < ref | SURVIVED | 341 passed in 10.26s
B6 no record date has no bound -> bound refuses | SURVIVED | 341 passed in 11.69s
R1 rule2 on-or-before -> before | SURVIVED | 341 passed in 7.44s
R2 rule2 no record date -> guess (feasible when not ref picks first) | KILLED | 1 failed, 24 passed in 0.58s
R3 rule1 two ends forcing different orders -> read | SURVIVED | 341 passed in 7.34s
K1 unknown type lends header date | KILLED | 1 failed, 225 passed in 2.44s
K2 abbreviations (ER/EMS/PT) not recognised | KILLED | 1 failed, 47 passed in 2.03s
K3 admin check removed | KILLED | 1 failed, 223 passed in 2.31s
K4 bill opening-of-excerpt scan removed | KILLED | 1 failed, 229 passed in 2.27s
L1 'visit date' becomes a prose label | KILLED | 1 failed, 249 passed in 2.32s
L2 'next' prefix guard removed | SURVIVED | 341 passed in 10.66s
L3 heading 'encounter date' dropped | SURVIVED | 341 passed in 6.78s
L4 heading 'date of visit' dropped | SURVIVED | 341 passed in 7.07s
L5 heading 24A dropped | KILLED | 1 failed, 108 passed in 2.22s
H1 labeled-but-unreadable in encounter falls to header date | KILLED | 1 failed, 116 passed in 2.34s
N1 counted undated charge gets a note | SURVIVED | 341 passed in 6.97s
N2 pos None encounter does not lend header date | KILLED | 1 failed, 35 passed in 0.61s
N3 swap the two note asks | KILLED | 1 failed, 125 passed in 2.26s
E1 hand-built case without dos_iso -> blank instead of record date | KILLED | 1 failed, 340 passed in 7.19s
E2 blank drops the statement date | KILLED | 1 failed, 2 passed in 0.60s
J1 opening_chars 40 -> 0 (excerpt opening never scanned) | KILLED | 1 failed, 229 passed in 2.46s
restored
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:08:10.241Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -rlE \"service_date|charge_service_date|implausible|dos_note|date of service \\[\" tests/unit evals/*.py tests/*.py 2>/dev/null | sort; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import xdist\" 2>&1 | tail -1"
}
````

### User / tool · 2026-11-03T02:08:10.361Z

**tool result**
````
evals/letter_check.py
tests/unit/test_t200_undated_charge_label.py
tests/unit/test_t202_charge_service_dates.py
tests/unit/test_t202_r2_service_date_layouts.py
tests/unit/test_t202_r3_allow_list.py
tests/unit/test_t202_r4_encounter.py
ModuleNotFoundError: No module named 'xdist'
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:08:20.336Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2 && python3 - <<'EOF'\nimport re\ns=open('mutants_t207_r2.py').read()\ns=s.replace('''only = sys.argv[3:] ''','''import os\nLETTER = os.environ.get(\"T207_LETTER\") == \"1\"\nonly = sys.argv[3:] ''')\ns=s.replace('''        r = subprocess.run([py, \"-m\", \"pytest\", *TESTS, \"-q\", \"-x\", \"-p\", \"no:cacheprovider\"], cwd=root, capture_output=True, text=True, timeout=300)\n        tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1]''','''        cmd = [py, \"-m\", \"evals.letter_check\"] if LETTER else [py, \"-m\", \"pytest\", *TESTS, \"-q\", \"-x\", \"-p\", \"no:cacheprovider\"]\n        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=300)\n        tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1][:120]''')\nopen('mutants_t207_r2.py','w').write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T207_LETTER=1 .venv/bin/python -I artifacts/review-evidence/T-207-r2/mutants_t207_r2.py $S/t207r2 /Users/arsis/zlayt-pm-project/.venv/bin/python E2 B1 B2 B5 B6 R1 R3 L2 L3 L4 N1 2>&1 | tee artifacts/review-evidence/T-207-r2/mutants_t207_r2_letter.out | cut -c1-230",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:08:20.493Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2/mutants_t207_r2.py", line 52, in <module>
    cmd = [py, "-m", "evals.letter_check"] if LETTER else [py, "-m", "pytest", *TESTS, "-q", "-x", "-p", "no:cacheprovider"]
                                              ^^^^^^
NameError: name 'LETTER' is not defined
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:08:22.685Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2 && grep -n \"only = \" mutants_t207_r2.py | cat -A | head -3"
}
````

### User / tool · 2026-11-03T02:08:22.775Z

**tool result**
````
cat: illegal option -- A
usage: cat [-belnstuv] [file ...]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:08:27.663Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-207-r2 && python3 - <<'EOF'\ns=open('mutants_t207_r2.py').read()\ni=s.index(\"only = sys.argv[3:]\")\nprint(repr(s[i-5:i+40]))\ns=s[:i]+'import os\\nLETTER = os.environ.get(\"T207_LETTER\") == \"1\"\\n'+s[i:]\nopen('mutants_t207_r2.py','w').write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T207_LETTER=1 .venv/bin/python -I artifacts/review-evidence/T-207-r2/mutants_t207_r2.py $S/t207r2 /Users/arsis/zlayt-pm-project/.venv/bin/python E2 B1 B2 B5 B6 R1 R3 L2 L3 L4 N1 2>&1 | tee artifacts/review-evidence/T-207-r2/mutants_t207_r2_letter.out | cut -c1-230",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:10:24.814Z

**tool result**
````
'),\n]\nonly = sys.argv[3:]\nfor name, rel, old, '
B1 bound 366 -> 365 days per year (1825 not 1830) | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
B2 bound >= -> > (day 1830 refused) | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
B5 on-or-before: (last or first) <= ref -> < ref | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
B6 no record date has no bound -> bound refuses | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
R1 rule2 on-or-before -> before | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
R3 rule1 two ends forcing different orders -> read | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
L2 'next' prefix guard removed | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
L3 heading 'encounter date' dropped | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
L4 heading 'date of visit' dropped | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
N1 counted undated charge gets a note | SURVIVED | {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
E2 blank drops the statement date | KILLED |   case_lib15_conclusory_letter_mist: ["oneline (counted): charge line's date is not certain from its quote (the blank is
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:10:33.703Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && du -sh t207r2 | tail -1; rm -rf t207r2_b1 && cp -R t207r2 t207r2_b1 && python3 - <<'EOF'\np='t207r2_b1/app/backend/service_date.py'\ns=open(p).read()\nassert s.count(\"days=366 * _YEARS_BEFORE\")==1\ns=s.replace(\"days=366 * _YEARS_BEFORE\",\"days=365 * _YEARS_BEFORE\").replace(\"_dt.date.fromisoformat(first) >= r - _dt.timedelta\",\"_dt.date.fromisoformat(first) > r - _dt.timedelta\").replace(\"(last or first) <= ref and\",\"(last or first) < ref and\")\nopen(p,'w').write(s)\nEOF\ngrep -c \"365 \\* _YEARS_BEFORE\" t207r2_b1/app/backend/service_date.py; cd t207r2_b1 && (time /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | tail -5)",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:11:35.590Z

**tool result**
````
218M	t207r2
1

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!

real	1m0.445s
user	0m35.853s
sys	0m13.972s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:11:39.594Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2_b1 && (time /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider --deselect tests/unit/test_e2e_contract.py::test_every_test_id_is_declared 2>&1 | tail -6)",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:18:30.058Z

**tool result**
````
........................................................................ [ 96%]
........................................................................ [ 97%]
........................................................................ [ 98%]
........................................................................ [ 99%]
..............                                                           [100%]
6266 passed, 12 skipped, 1 deselected in 408.74s (0:06:48)

real	6m50.381s
user	3m56.459s
sys	1m25.535s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:18:46.555Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf t207r2_b1 t207r2_m && cp -R t207r2 t207r2_m && python3 - <<'EOF'\nsd='t207r2_m/app/backend/service_date.py'; st='t207r2_m/app/backend/store.py'\ns=open(sd).read()\nfor old,new in [(\"t.ambiguous[o] <= ref for t in amb\",\"t.ambiguous[o] < ref for t in amb\"),\n                (\"if len(determined) > 1:\",\"if len(determined) > 2:\"),\n                (\"(?<!next )\",\"\"),\n                (\"|encounter\\\\s+date|\",\"|\"),\n                (\"|date\\\\s+of\\\\s+visit|\",\"|\")]:\n    assert s.count(old)==1,(old,s.count(old)); s=s.replace(old,new)\nopen(sd,'w').write(s)\nt=open(st).read(); old=\"if not stated and not counted_undated:\"; assert t.count(old)==1\nopen(st,'w').write(t.replace(old,\"if not stated:\"))\nEOF\ncd t207r2_m && (time /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider --deselect tests/unit/test_e2e_contract.py::test_every_test_id_is_declared 2>&1 | tail -3)",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:25:27.158Z

**tool result**
````
........................................................................ [ 99%]
..............                                                           [100%]
6266 passed, 12 skipped, 1 deselected in 396.63s (0:06:36)

real	6m38.210s
user	3m51.701s
sys	1m17.635s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:25:35.769Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- docs/LLM_VS_CODE.md; git diff HEAD -- docs/LLM_VS_CODE.md | grep '^[-+]|' | cut -c1-120; git show efda639:docs/LLM_VS_CODE.md | sed -n 30,31p | md5; sed -n 30,31p docs/LLM_VS_CODE.md | md5; git rev-parse HEAD"
}
````

### User / tool · 2026-11-03T02:25:35.938Z

**tool result**
````
bc0c5db5a07f5b3bcd2f7539aca7f0ef
bc0c5db5a07f5b3bcd2f7539aca7f0ef
ad0d91abe692860ffea9448e5bed0c78021807eb
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:25:38.235Z

**tool call — Bash**
````
{
 "command": "git log --oneline efda639..HEAD; git diff --stat 8cb5bd2 HEAD -- app/backend/service_date.py app/backend/encounter_types.json app/backend/export.py app/backend/store.py evals/letter_check.py docs/LLM_VS_CODE.md tests/unit | tail -5"
}
````

### User / tool · 2026-11-03T02:25:38.353Z

**tool result**
````
ad0d91a fix(qa): T-210 declare the five guided test ids (brand, footer-note, demo-badge, btn-draft, draft-done) in the E2E contract
0281189 chore(guard): subagents stage only into a temp index (shared index kept holding stale reverts, T-201/T-204)
1b3c58a fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
 docs/LLM_VS_CODE.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:25:43.322Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -n \"import.*billing\\|billing\\.\" app/backend/export.py app/backend/store.py app/backend/present.py app/backend/service_date.py | head; grep -n \"/billing\" app/backend/billing.py app/backend/api.py | head -5 | cut -c1-200; grep -rn \"billing\" app/frontend --include=*.js -l | head; sed -n 136,146p app/backend/billing.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:25:43.446Z

**tool result**
````
app/backend/billing.py:1061:    @app.get("/api/cases/{token}/billing")
app/frontend/guided/step3.js
    name = re.split(r",|\s[-–—]\s", src, maxsplit=1)[0].strip()
    name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
    return name or "Unknown provider"


def _dos(raw):
    p = dates.parse_date(raw or "")
    return p["iso"] if p.get("status") == "parsed" else None


def _cite(rec, line):
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:25:48.336Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t207r2 && grep -rn \"dos_iso\\|api/cases/.*/billing\" app/frontend | head -3; grep -n \"dates\\.\\|import\" app/backend/dates.py | head -5; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import dates\nfor s in ['04/05/2026','13/05/2026','2026-01-09','January 9, 2026']:\n    print(s, dates.parse_date(s))\n\" | cut -c1-200"
}
````

### User / tool · 2026-11-03T02:25:48.481Z

**tool result**
````
5:import datetime as _dt
6:import re
8:from app.backend import spanish_text
44:    PIVOT_YY (40) is ambiguous between 19yy and 20yy (`03-17-98` -> 1998-03-17 or 2098-03-17). All readings are returned as candidates."""
04/05/2026 {'raw': '04/05/2026', 'status': 'ambiguous', 'iso': None, 'candidates': ['2026-04-05', '2026-05-04']}
13/05/2026 {'raw': '13/05/2026', 'status': 'parsed', 'iso': '2026-05-13', 'candidates': []}
2026-01-09 {'raw': '2026-01-09', 'status': 'parsed', 'iso': '2026-01-09', 'candidates': []}
January 9, 2026 {'raw': 'January 9, 2026', 'status': 'parsed', 'iso': '2026-01-09', 'candidates': []}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:26:04.137Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > artifacts/review-evidence/T-207-r2/probe2_t207_r2.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import service_date as SD\nLED = \"Fennimoor Spine Clinic, itemized ledger\"\ndef run(tag, ex, fig, src, rd):\n    r = SD.resolve(ex, ex.index(fig), src, rd)\n    print(f\"{tag} | {r['state']} | {r['first']} | {r['last']} | {r['reason']} | {r['raw']!r}\")\nfor pre in (\"\", \"next \", \"last \", \"prior \", \"previous \", \"initial \", \"scheduled \"):\n    run(f\"E1 bill '{pre}visit of 12/01/2025'\", f\"Itemized ledger. Charge for {pre}visit of 12/01/2025: office visit $220.00.\", \"$220.00\", LED, \"2026-06-30\")\nfor pre in (\"\", \"next \", \"last \", \"prior \"):\n    run(f\"E2 bill '{pre}DOS 12/01/2025'\", f\"Itemized ledger. Charge for {pre}DOS 12/01/2025: office visit $220.00.\", \"$220.00\", LED, \"2026-06-30\")\nrun(\"E3 bill 'rendered on' next\", \"Itemized ledger. Next services rendered on 12/01/2025: office visit $220.00.\", \"$220.00\", LED, \"2026-06-30\")\n# the classifier on odd encounter sources and openings (fails toward blank)\nfor src, ex in ((\"Capital PT, initial evaluation\", \"Balance and gait deficits noted. Charge $120.00.\"),\n                (\"Capital PT, initial evaluation\", \"Patient reports pain. Charge $120.00.\"),\n                (\"Austin ER visit\", \"Cost of care discussed. Charge $120.00.\"),\n                (\"Austin ER visit\", \"Patient quote: pain 7/10. Charge $120.00.\")):\n    run(f\"E4 {src} / {ex[:30]}\", ex, \"$120.00\", src, \"2026-01-09\")\nprint(\"kinds:\", [(s, SD.record_kind(s, e)) for s, e in ((\"Capital PT, initial evaluation\", \"\"), (\"Austin EMS run report\", \"\"), (\"Fennimoor Spine Clinic, itemized ledger\", \"\"), (\"Prescription slip\", \"\"), (\"Phone note\", \"\"), (\"Dr. Chen, referral letter\", \"\"))])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-207-r2/probe2_t207_r2.py $S/t207r2 2>&1 | tee artifacts/review-evidence/T-207-r2/probe2_t207_r2.out"
}
````

### User / tool · 2026-11-03T02:26:04.364Z

**tool result**
````
E1 bill 'visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E1 bill 'next visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E1 bill 'last visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E1 bill 'prior visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E1 bill 'previous visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E1 bill 'initial visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E1 bill 'scheduled visit of 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E2 bill 'DOS 12/01/2025' | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E2 bill 'next DOS 12/01/2025' | not_stated | None | None | non_service_date | '12/01/2025'
E2 bill 'last DOS 12/01/2025' | not_stated | None | None | non_service_date | '12/01/2025'
E2 bill 'prior DOS 12/01/2025' | not_stated | None | None | non_service_date | '12/01/2025'
E3 bill 'rendered on' next | not_stated | None | None | ambiguous_numeric | '12/01/2025'
E4 Capital PT, initial evaluation / Balance and gait deficits note | not_stated | None | None | no_date | ''
E4 Capital PT, initial evaluation / Patient reports pain. Charge $ | stated | 2026-01-09 | None | None | ''
E4 Austin ER visit / Cost of care discussed. Charge | not_stated | None | None | no_date | ''
E4 Austin ER visit / Patient quote: pain 7/10. Char | not_stated | None | None | no_date | ''
kinds: [('Capital PT, initial evaluation', 'encounter'), ('Austin EMS run report', 'encounter'), ('Fennimoor Spine Clinic, itemized ledger', 'bill'), ('Prescription slip', 'other'), ('Phone note', 'other'), ('Dr. Chen, referral letter', 'other')]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:26:16.025Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat >> artifacts/review-evidence/T-207-r2/probe2_t207_r2.py <<'EOF'\nfor pre in (\"\", \"next \", \"last \", \"prior \"):\n    run(f\"E5 bill '{pre}visit of 12/20/2025' (unambiguous)\", f\"Itemized ledger. Charge for {pre}visit of 12/20/2025: office visit $220.00.\", \"$220.00\", LED, \"2026-06-30\")\nrun(\"E5 bill 'last DOS 12/20/2025'\", \"Itemized ledger. Charge for last DOS 12/20/2025: office visit $220.00.\", \"$220.00\", LED, \"2026-06-30\")\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-207-r2/probe2_t207_r2.py $S/t207r2 2>&1 > artifacts/review-evidence/T-207-r2/probe2_t207_r2.out; tail -5 artifacts/review-evidence/T-207-r2/probe2_t207_r2.out; ls artifacts/review-evidence/T-207-r2/"
}
````

### User / tool · 2026-11-03T02:26:16.332Z

**tool result**
````
E5 bill 'visit of 12/20/2025' (unambiguous) | stated | 2025-12-20 | None | None | ''
E5 bill 'next visit of 12/20/2025' (unambiguous) | stated | 2025-12-20 | None | None | ''
E5 bill 'last visit of 12/20/2025' (unambiguous) | stated | 2025-12-20 | None | None | ''
E5 bill 'prior visit of 12/20/2025' (unambiguous) | stated | 2025-12-20 | None | None | ''
E5 bill 'last DOS 12/20/2025' | not_stated | None | None | non_service_date | '12/20/2025'
mutants_t207_r2.out
mutants_t207_r2.py
mutants_t207_r2_letter.out
probe2_t207_r2.out
probe2_t207_r2.py
probe_t207_r2.out
probe_t207_r2.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:26:19.700Z

**tool call — Bash**
````
{
 "command": "grep -n \"amendment 2\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-2500 | head -4"
}
````

### User / tool · 2026-11-03T02:26:19.785Z

**tool result**
````
94:- D-071 amendment 2 (§7.4 after T-202 r3; round 4 authorised, final): (a) a record's own date is a service date only for a positively identified encounter record (visit/ER/clinic/therapy/ambulance-run note); bills, receipts, superbills, charge summaries and unknown types never lend their header date; (b) in prose, only "date of service", "dates of service", "DOS" and "service date" are labels ("visit date", "seen on" and bare "date" are not; they also name next or prior visits); (c) letter_check keeps an independent scanner but reads the same declared encounter-type table (one data file), and anchors the blank; (d) if round 4 fails, the fallback is the most conservative rule: every charge line prints the fillable blank unless a DOS column or one of the (b) labels ties exactly one date to it.
95:- D-071 amendment 2 note (T-202 r4): inside bills only, "visit of", "the run of", "rendered on" and "service period" also count as service labels (case_09 and lib14 need them); outside bills they do not. Accepted.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:27:49.682Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer-r2.md",
 "content": "# T-207 staff-engineer review, r2\n\nReviewer: staff-engineer-reviewer (Marcus Lee persona), fresh context, read-only on product code. Model running: claude-sonnet-5-5.\n\nScope: docs/LLM_VS_CODE.md rows 2 and 3 as fixed in efda639, checked against the code at 8cb5bd2 (a git archive in a scratch directory; the product tree was not edited). `git diff --stat 8cb5bd2 HEAD -- app/backend/service_date.py app/backend/encounter_types.json app/backend/export.py app/backend/store.py evals/letter_check.py docs/LLM_VS_CODE.md tests/unit` shows only `docs/LLM_VS_CODE.md | 4 ++--` (efda639), so the code did not move between 8cb5bd2 and HEAD ad0d91a. Rows 30-31 of the working copy have the same md5 as `git show efda639:docs/LLM_VS_CODE.md`.\n\n## Verdict: changes (no blocker, two majors, four minors)\n\n## Does stating the five-year bound as 1,830 days settle it?\n\nThe statement is accurate. It is not enough.\n\nAccurate: probe D1 (statement 2026-06-30, ledger) gives \"1830d before (2021-06-26) | stated\" and \"1831d before (2021-06-25) | not_stated | reason=implausible\". `service_date.py:109` has `_YEARS_BEFORE = 5` and `:328` has `days=366 * _YEARS_BEFORE`. The sentence \"a date a few days past five calendar years can still be read\" is true (2021-06-26 is five years and four days before). That closes the doc half of r1 F2.\n\nNot enough: the number is now a documented contract and nothing pins it. The only bound tests are the 1998 and 2031 fixtures (`tests/unit/test_t202_r3_allow_list.py:184-185`). I mutated the bound three ways at once (365 days per year, `>=` to `>` at the lower end, `<=` to `<` at the upper end) on the 8cb5bd2 archive and ran the whole unit suite: `6266 passed, 12 skipped, 1 deselected` (the deselected test, `test_e2e_contract.py::test_every_test_id_is_declared`, fails identically at the parent per the T-202 handoff and is not in this scope). r1 F2's acceptance test (a test at the boundary that kills the bound mutant) is therefore still open. Persona calibration: a bound with no boundary test is major. The doc is accurate for behaviour and still wrong to rely on for verification, because the \"How it is checked\" cell cites unit tests that cannot fail when 1,830 changes.\n\nWhether a 1 to 4 day slack is acceptable product behaviour is a product call (Q1). If it is, pin it with tests. If it is not, fix the code, and the doc sentence changes with it.\n\n## Row-by-row result\n\nHolds (probe or code line in brackets):\n- Rule (1), same-date-or-period order: `04/05/2026 - 13/05/2026` reads May 4 to May 13 [D2; service_date.py:265-275]. Two ends forcing different orders are not read [D2: \"13/05/2026 - 05/13/2026 | ambiguous_numeric\"].\n- Rule (2), a service cannot follow its statement: read only when exactly one order is on or before the record date; with no record date it is not read [D2 rows for 2026-05-31, 2026-04-30 and None; service_date.py:272-274].\n- Bound applies to every record, `implausible`, no bound without a record date [D1, D1nodate; service_date.py:323-328].\n- Only an identified encounter lends its header date; bill, receipt, superbill, charge summary, administrative paper and unknown type do not [D3 rows; service_date.py:54-63, 414-434]. A labeled but unreadable date is not replaced by the header date [D3 \"ER labeled-bad(2-digit) | two_digit_year\", probe H1 mutant killed].\n- Table `encounter_types.json` is read by `service_date.record_kind` (TYPES_PATH at :33) and by `evals/letter_check.py:234` with its own matcher; letter_check imports no service_date (grep). `python -m evals.letter_check` gives `\"value\": 0, \"cases\": 25`.\n- Column heading set in row 2 matches `_H_SVC` (service_date.py:107-108) [D6: every listed heading is recognised; Posted and Entry Date are not].\n- Row 3: the blank text and `export.charge_when` (export.py:215-226), the two note forms (service_date.py:156-162), counted charge has no note (store.py:139), hand-built dict without `dos_iso` keeps the record date (export.py:222-223). Billing view `dos_iso` is `billing._dos`, route at billing.py:1061, no import from export, store or present, no consumer in app/frontend.\n\nDoes not hold, or is not pinned: findings below.\n\n## Exercised\n\n1. `git rev-parse HEAD 8cb5bd2 efda639`, `git log --oneline -8`, `git diff --stat 8cb5bd2 efda639` (docs only, 2 lines), `git diff --stat 8cb5bd2 HEAD -- <scope files>`.\n2. `git archive 8cb5bd2` into a scratch directory. Read service_date.py (434 lines), encounter_types.json, store.py:105-200, export.py:215-226 and 600-625, amounts.py:300-320 and 515-545, evals/letter_check.py:1-30, 225-240, 405-470, billing.py:136-145, rows 2 and 3 of docs/LLM_VS_CODE.md, the T-202 board card (handoff and notes), D-071 amendment 2 (ORCHESTRATOR_DECISIONS.md:94-95), and my r1 review.\n3. `pytest` on the five date files (test_t202_r2_service_date_layouts, test_t202_r3_allow_list, test_t202_r4_encounter, test_t202_charge_service_dates, test_t200_undated_charge_label): 341 passed. `--collect-only` on test_t202_r4_encounter.py: 133 tests.\n4. `python -m evals.letter_check` on the archive: value 0, cases 25.\n5. Probes D1 to D7: artifacts/review-evidence/T-207-r2/probe_t207_r2.py and probe_t207_r2.out. Probes E1 to E5: probe2_t207_r2.py and probe2_t207_r2.out.\n6. 25 mutants against the five date files: mutants_t207_r2.py and mutants_t207_r2.out (15 killed, 10 survived). Ten of them against evals.letter_check: mutants_t207_r2_letter.out (control E2 killed, the other ten survived). Two full-suite runs of tests/unit on mutated copies: B1+B2+B5 (6266 passed, 12 skipped, 1 deselected, 408 s) and R1+R3+L2+L3+L4+N1 (6266 passed, 12 skipped, 1 deselected, 397 s). The script restores each file; the archive's service_date.py md5 matched `git show 8cb5bd2` after the run.\n7. `ls reviews | grep T-202` (no r4 review file), `git status` and `git diff HEAD --stat -- docs/LLM_VS_CODE.md` (empty).\n\n## Findings\n\nF1 (major). The five-year bound, the on-or-before boundary and the no-record-date case are documented and unpinned. Mutants B1 (365 per year), B2 (`>=` to `>`), B3 and B4 (5 to 4 and 6 years), B5 (`<=` to `<` at the record date) and B6 (no-date record refuses) all survive the five date test files and the letter eval; B1+B2+B5 together survive the full unit suite. Accurate wording does not fix a missing test.\n\nF2 (major). Other statements in rows 2 and 3 are also pinned by no test. Mutant R3 (`len(determined) > 2`, so two ends that force different orders are read) and R1 (`<= ref` to `< ref` in rule 2) survive the full unit suite, with L2 (drop the `next ` guard), L3 (drop \"encounter date\" heading), L4 (drop \"date of visit\" heading) and N1 (a counted charge gets a note). r1 F6's acceptance asked that the Encounter Date mutant be killed; it still survives. R3 matters most: a period whose ends force different orders is exactly where a wrong date could print.\n\nF3 (minor, would be major if a real path is shown). The doc says the header date is lent \"only when the line has no labeled date of its own\" and that a labeled date that cannot be read \"is not replaced by the header date\". `store.py:131` skips the look when `pos` is None: probe D4 gives \"pos located | not_stated None implausible\" but \"pos None | stated 2026-01-09\" for the same encounter line that labels 05/05/2026, and \"D4c pos None, line labels 03/01/2026 | stated 2026-01-09\" where the located path reads 2026-01-03. `tests/unit/test_t200_undated_charge_label.py:63` pins this with an excerpt `\"x\"`. I could not find a normal flow that gives `amount_pos` None for a pipeline amount (pipeline.py:417 sets excerpt_start from the figure), so I rate it minor. This is a doc/code divergence, not a preference.\n\nF4 (minor). The allow-list text is narrower than the code. UB-04 \"statement period\" is read, not only \"statement covers period\" (probe D5: stated 2026-01-05 to 2026-01-09). Label connectors `is`, `was`, `from`, `between`, `#`, `-` and `(` also work (D7), and the doc names a colon, spaces or a dotted leader. The bill wordings \"date of the run\" and \"treatment dates\", the \"from service\" heading, and (d) taking a single labeled date (not only a period) are not listed (service_date.py:92-96, 101, 107-108, 415-428). The list is presented as exhaustive.\n\nF5 (minor, question for Chris). The \"never after next, last, prior...\" guard is stated for the prose labels and the code applies it only there. A bill's own wordings are unguarded: probe E5, \"Charge for last visit of 12/20/2025: office visit $220.00.\" prints 2025-12-20 as the date of service, and \"next visit of\" and \"prior visit of\" do the same, while \"last DOS 12/20/2025\" correctly gives non_service_date (service_date.py:89-93). D-071 amendment 2 note (ORCHESTRATOR_DECISIONS.md:95) accepts the bill wordings but not the missing guard. Either the doc says the guard stops at the prose labels or the code extends it.\n\nF6 (minor). Two validation-cell counts overreach. \"131 tests\" is 133 (`pytest --collect-only`, test_t202_r4_encounter.py), copied from the backend handoff. \"every reviewer probe from rounds 3 and 4 is a fixture\" has no round 4 behind it: `ls reviews | grep T-202` shows no r4 review, and the test file's own docstring (line 1) says \"Every probe from the round 3 paralegal and staff reviews\". The honest sentence about the uncommitted 24-of-25 mutation run is right and should stay.\n\n## What is right\n\n1. The bound sentence is exact: 1,830 days is read, 1,831 is refused, and a few days past five calendar years is read (probe D1).\n2. The two ambiguity rules, the encounter-only header date, and the classifier all behave as written and fail toward the blank (probes D2, D3, E4).\n3. Row 3's blank, both note forms, the counted-charge exception and the hand-built-dict branch match the code; the code is unchanged from 8cb5bd2 to HEAD and `evals.letter_check` reads value 0 over 25 cases.\n\nOutside my lens: the legal weight of the blank, and whether a paralegal reads the Step 3 note wording as helpful.\n\n```json\n{\"card\": \"T-207\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"docs/LLM_VS_CODE.md rows 2-3 as of efda639 vs code at 8cb5bd2 (git archive in scratch; code unchanged to HEAD ad0d91a): app/backend/service_date.py, encounter_types.json, store.py:105-200, export.py:215-226, evals/letter_check.py; no app URL exercised\",\n \"exercised\": [\"git rev-parse/log/diff --stat: 8cb5bd2 to efda639 is docs only; scope files unchanged 8cb5bd2 to HEAD; rows 30-31 md5 equal at efda639 and working copy\",\n               \"git archive 8cb5bd2 into scratch; read service_date.py in full, encounter_types.json, store.py:105-200, export.py:215-226 and 600-625, amounts.py:300-320 and 515-545, letter_check.py header and charge_date_violations, billing.py:136-145, rows 2-3, T-202 board card, D-071 amendment 2\",\n               \"pytest on 5 date test files at 8cb5bd2: 341 passed; --collect-only test_t202_r4_encounter.py: 133 tests\",\n               \"python -m evals.letter_check: value 0, cases 25\",\n               \"probes D1-D7 (artifacts/review-evidence/T-207-r2/probe_t207_r2.py + .out) and E1-E5 (probe2_t207_r2.py + .out)\",\n               \"25 mutants on date files (mutants_t207_r2.py + .out: 15 killed, 10 survived); 10 against letter_check (mutants_t207_r2_letter.out: 10 survived, control killed)\",\n               \"full tests/unit on mutated copies: B1+B2+B5 and R1+R3+L2+L3+L4+N1 each 6266 passed, 12 skipped, 1 deselected (known failing test_every_test_id_is_declared)\",\n               \"ls reviews | grep T-202 (no r4 review); git status and git diff HEAD --stat on the doc (empty)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"row2_matches_code\": 4, \"row3_matches_code\": 4, \"date_is_code_only\": 5, \"bound_statement_accuracy\": 5, \"bound_and_rules_pinned_by_tests\": 2, \"validation_cell_claims\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"The five-year bound is stated exactly as 1,830 days, but no test pins it, the on-or-before edge, or the no-record-date case\",\n   \"evidence\": \"service_date.py:109 '_YEARS_BEFORE = 5' and :328 'days=366 * _YEARS_BEFORE'; probe_t207_r2.out 'D1 1830d before (2021-06-26) | stated' and 'D1 1831d before (2021-06-25) | not_stated ... reason=implausible'; only bound tests are tests/unit/test_t202_r3_allow_list.py:184-185 (1998 and 2031); mutants_t207_r2.out 'B1 ... SURVIVED | 341 passed', 'B2 ... SURVIVED', 'B3', 'B4', 'B5 ... SURVIVED', 'B6 ... SURVIVED'; mutants_t207_r2_letter.out B1 B2 B5 B6 SURVIVED (value 0, 25 cases); full tests/unit with B1+B2+B5 applied: '6266 passed, 12 skipped, 1 deselected in 408.74s'\",\n   \"why_it_matters\": \"The doc now makes 1,830 days a contract and row 3's How-it-is-checked cell cites unit tests as the check. Those tests pass when the constant becomes 1,825, when the lower edge flips, and when a service date equal to the record date is refused. r1 F2's acceptance test (a boundary test that kills the bound mutant) is still open. Persona calibration: a bound without a boundary test is major.\",\n   \"fix\": \"Add unit tests through store.charge_service_date for a ledger with statement 2026-06-30: DOS 06/26/2021 (1,830 days) is stated, 06/25/2021 (1,831) is implausible; DOS equal to the record date is stated and one day after is implausible; a record with no date and DOS 03/13/1998 is stated. Chris decides whether the 1 to 4 day slack stays (Q1); if not, change the code to a calendar-year compare and update the doc sentence.\",\n   \"acceptance_test\": \"Mutants B1 (365 per year), B2 (>= to >), B3/B4 (_YEARS_BEFORE 4 or 6), B5 (<= to < at the record date) and B6 (no-date record refuses) each fail at least one test in tests/unit; the tests are in the repo and named in row 3's cell.\"},\n  {\"severity\": \"major\", \"title\": \"Other statements in rows 2 and 3 are covered by no test: different-order period ends, rule 2's on-or-before edge, two headings, the next guard, the counted-charge no-note rule\",\n   \"evidence\": \"mutants_t207_r2.out 'R3 rule1 two ends forcing different orders -> read | SURVIVED', 'R1 rule2 on-or-before -> before | SURVIVED', 'L2 next prefix guard removed | SURVIVED', 'L3 heading encounter date dropped | SURVIVED', 'L4 heading date of visit dropped | SURVIVED', 'N1 counted undated charge gets a note | SURVIVED' (all against 341 date tests); R1+R3+L2+L3+L4+N1 applied together to a copy and run over tests/unit: '6266 passed, 12 skipped, 1 deselected in 396.63s'; docs/LLM_VS_CODE.md:30 'two ends that force different orders are not read', ':31 carries no note'; r1 F6 acceptance 'M8 is killed' (Encounter Date) still unmet\",\n   \"why_it_matters\": \"Each is a sentence in the binding table that the code can break without any test failing. R3 decides whether a period with contradictory ends prints a date or the blank, which is a printed-date correctness rule. The doc's own Validation cell says the dates are tested.\",\n   \"fix\": \"Add one fixture per statement: '13/05/2026 - 05/13/2026' prints the blank; a rule-2 case where one order equals the record date; a table with an 'Encounter Date' heading and one with 'Date of Visit'; 'Next DOS 02/01/2026' is non_service_date; a counted undated charge has confirm_note None and an uncounted one has a note.\",\n   \"acceptance_test\": \"Mutants R1, R3, L2, L3, L4 and N1 each fail at least one test in tests/unit.\"},\n  {\"severity\": \"minor\", \"title\": \"For an encounter record whose figure cannot be located, the header date is lent without looking at the line; the doc says only when the line has no labeled date\",\n   \"evidence\": \"app/backend/store.py:131 'elif rec is None or pos is None or not item.get(\\\"excerpt\\\"): r = {... \\\"first\\\": rd ...} if (encounter and rd) else dict(none)'; probe_t207_r2.out 'D4 pos located | not_stated None implausible' vs 'D4 pos None | stated 2026-01-09 None'; 'D4c pos None, line labels 03/01/2026 (AFTER header) | stated 2026-01-09' vs 'D4d pos located, same line | stated 2026-01-03'; tests/unit/test_t200_undated_charge_label.py:63 pins it with excerpt 'x'; docs/LLM_VS_CODE.md:30 'only when the line has no labeled date of its own' and 'A labeled date that cannot be read in an encounter record is not replaced by the header date'\",\n   \"why_it_matters\": \"The doc states a universal the code breaks on this path. Rated minor because pipeline.py:417 sets excerpt_start for every amount and I found no normal flow that yields pos None; if the orchestrator can show one, it becomes major.\",\n   \"fix\": \"In the pos-None branch, print the blank when the excerpt contains any date (or always), or add the branch to row 3 with its reason.\",\n   \"acceptance_test\": \"A test with pos None and an excerpt that labels a date asserts the decided result; mutant N2 stays killed.\"},\n  {\"severity\": \"minor\", \"title\": \"The allow-list as written is narrower than the code: UB-04 statement period, label connectors, two bill wordings, one heading, and a single labeled date under (d)\",\n   \"evidence\": \"probe_t207_r2.out 'D5 ub04 statement period | stated | 2026-01-05 | 2026-01-09' (doc names only 'statement covers period'); 'D7 label tail DOS is / DOS was / DOS between / DOS - / DOS # | ambiguous_numeric' (label recognised; doc names colon, spaces, dotted leader); service_date.py:92-93 'date of the run', 'treatment dates?'; :107-108 'from service'; :80 _LBL_END\",\n   \"why_it_matters\": \"The list is presented as the whole set of ties; a reader cannot tell what else decides a printed date.\",\n   \"fix\": \"Name the extra connectors, wordings, heading and the UB-04 'statement period', or narrow the code.\",\n   \"acceptance_test\": \"Each phrase in service_date.py's label regexes appears in row 2, checked by reading the two side by side.\"},\n  {\"severity\": \"minor\", \"title\": \"The next/last/prior guard is stated for prose labels; a bill's own 'visit of' wording has none, so 'last visit of 12/20/2025' prints as the service date\",\n   \"evidence\": \"probe2_t207_r2.out 'E5 bill last visit of 12/20/2025 (unambiguous) | stated | 2025-12-20' and 'next visit of', 'prior visit of' the same; 'E5 bill last DOS 12/20/2025 | not_stated ... non_service_date'; service_date.py:89-93 (_NOT_OTHER_VISIT is applied to _SVC_CORE only); memory/ORCHESTRATOR_DECISIONS.md:95 accepts the bill wordings without the guard; docs/LLM_VS_CODE.md:30\",\n   \"why_it_matters\": \"It is the same class as the r3 paralegal blocker (another visit's date printed as this charge's). The doc does not say the guard stops at the prose labels.\",\n   \"fix\": \"Either apply the guard to _SVC_BILL or state in row 2 that the guard covers only DOS, date of service and service date.\",\n   \"acceptance_test\": \"A test for 'Charge for last visit of 12/20/2025' in a ledger asserts the chosen result.\"},\n  {\"severity\": \"minor\", \"title\": \"Two counts in row 3's validation cell overreach: 131 tests (it is 133) and 'rounds 3 and 4' probes (no round 4 review exists)\",\n   \"evidence\": \"pytest tests/unit/test_t202_r4_encounter.py --collect-only: '133 tests collected'; docs/LLM_VS_CODE.md:31 'test_t202_r4_encounter.py (131 tests; every reviewer probe from rounds 3 and 4 is a fixture)'; tests/unit/test_t202_r4_encounter.py:1 'Every probe from the round 3 paralegal and staff reviews is a fixture here'; ls reviews | grep T-202 lists paralegal, paralegal-r2, paralegal-r3, staff-engineer, -r2, -r3 and no r4\",\n   \"why_it_matters\": \"The 131 comes from the backend handoff, not a run. The probe claim names a review round that has not been recorded. Same class as r1 F5 (a count the reviewer can refute).\",\n   \"fix\": \"Say 133 (or drop the count) and 'rounds 1 to 3' (or cite the test file's own sentence).\",\n   \"acceptance_test\": \"The cell's numbers equal pytest --collect-only and the reviews/ listing.\"}\n ],\n \"whats_right\": [\"The bound sentence is exact: 1,830 days is read, 1,831 is refused, and a few days past five calendar years is read (probe D1).\",\n                 \"The two ambiguity rules, the encounter-only header date and the record-type classifier behave as written and fail toward the blank (probes D2, D3, E4).\",\n                 \"Row 3's blank, both note forms, the counted-charge exception and the hand-built-dict branch match the code; code is unchanged from 8cb5bd2 to HEAD and evals.letter_check reads value 0 over 25 cases.\"],\n \"questions_for_chris\": [\"Q1 (F1): Is a labeled service date up to 4 days past five calendar years (1,830-day bound) acceptable to print, or should the bound be calendar-exact?\",\n                         \"Q2 (F5): Should the next/last/prior guard also stop a bill's own 'visit of' wording from tying a date to the line?\"]}\n```\n"
}
````

### User / tool · 2026-11-03T02:27:49.836Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:27:55.372Z

**tool call — Bash**
````
{
 "command": "grep -c \"KILLED\" artifacts/review-evidence/T-207-r2/mutants_t207_r2.out; grep -c \"SURVIVED\" artifacts/review-evidence/T-207-r2/mutants_t207_r2.out; grep -n \"15 killed\" reviews/T-207-staff-engineer-r2.md | cut -c1-80"
}
````

### User / tool · 2026-11-03T02:27:55.473Z

**tool result**
````
13
12
39:6. 25 mutants against the five date files: mutants_t207_r2.py and mutants_t20
72:               "25 mutants on date files (mutants_t207_r2.py + .out: 15 kille
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:27:58.743Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='reviews/T-207-staff-engineer-r2.md'\ns=open(p).read()\nassert s.count(\"15 killed, 10 survived\")==2\ns=s.replace(\"15 killed, 10 survived\",\"13 killed, 12 survived\")\nopen(p,'w').write(s)\nEOF\ngrep -c \"13 killed, 12 survived\" reviews/T-207-staff-engineer-r2.md; python3 - <<'EOF'\nimport re,json\ns=open('/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer-r2.md').read()\nb=re.findall(r\"```json\\n(.*?)```\",s,re.S); print(len(b)); d=json.loads(b[0]); print(d['verdict'],len(d['findings']))\nEOF\npython3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-03T02:27:58.949Z

**tool result**
````
2
1
changes 6
ok (210 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:27:59.750Z

Now the memory update.

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:28:07.309Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_r2_patterns.md",
 "content": "---\nname: t207-r2-patterns\ndescription: T-207 r2 (LLM_VS_CODE rows 2-3 vs code 8cb5bd2): accurate doc sentence for a bound is not a test; boundary/rule mutants survive full unit suite; pos-None path breaks a universal\nmetadata:\n  type: project\n---\n\nr2 of the doc-rows review (2026-11-02, verdict changes, 2 majors). The doc was fixed to say the five-year bound is 1,830 days (accurate: 1830 read, 1831 refused). Fixing the sentence closed the doc half of r1 F2 but not the test half: B1 (365/yr), B2 (>= to >), B5 (<= to < at the record date), B3/B4 (4 or 6 years) all survive the 5 date test files, the letter eval, and the full 6266-test unit suite. Also surviving: R3 (two ends forcing different orders), R1 (rule 2 on-or-before), Encounter Date and Date of Visit headings, the next guard, counted-charge no-note.\n\n**Why:** a \"How it is checked\" cell that cites tests makes every number in the row a contract; a doc that is made accurate without a test is a partial re-fix (same class as [[project_t207_doc_rows_patterns]] r1 and [[project_db_review_patterns]]).\n\n**How to apply:** when a fix rewrites the doc to match the code, still mutate the stated number and its on/off-by-one edges; run the full tests/unit once on a combined-mutant copy (about 7 min; deselect test_e2e_contract::test_every_test_id_is_declared, which fails at parent) to prove survival beyond the topic's own files. Also grep for a `pos is None` / defensive branch in the store path that skips the check the doc says always happens (store.py:131 lent the encounter header date without looking at the line). Guards stated for one label family (next/last/prior on prose labels) often skip the sibling family (bill wordings like \"visit of\"). Count claims copied from a handoff (131 tests vs 133 collected) and \"rounds N and M\" claims need a ls reviews/ check. Mutation harness pattern: a script doing exact-string replace with count assert, restore in finally, plus a control mutant that must be killed; tracked under artifacts/review-evidence/T-207-r2/.\n\nRelated: [[feedback_mutant_apply_verify]], [[feedback_review_write_once]] (I miscounted killed/survived in the first write and fixed it with a python replace; count with grep -c before writing).\n"
}
````

### User / tool · 2026-11-03T02:28:07.405Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t207_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:28:08.377Z

**tool call — Bash**
````
{
 "command": "echo \"- [T-207 r2 patterns](project_t207_r2_patterns.md) — doc fixed to 1,830 days but bound/rule mutants survive full suite; pos-None breaks universal\" >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md; tail -2 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-160"
}
````

### User / tool · 2026-11-03T02:28:08.464Z

**tool result**
````
- [T-210 contract-declare patterns](project_t210_contract_declare_patterns.md) — docstring substring contract stays green when frontend drops an id
- [T-207 r2 patterns](project_t207_r2_patterns.md) — doc fixed to 1,830 days but bound/rule mutants survive full suite; pos-None breaks universal
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T02:28:11.170Z

Verdict: changes, with no blockers and two majors; stating the bound as 1,830 days is accurate but not enough, because no test pins it. Mutating the bound to 365 days a year, a strict `>` at the lower edge and a strict `<` at the record date still passed the full unit suite (6266 passed, 12 skipped, 1 known-failing test deselected). The same is true of the rule where two ends of a period force different orders, and of the rule-2 boundary on or before the record date. The Encounter Date and Date of Visit headings, the next guard and the counted-charge no-note rule are also unpinned. I raised four minors too, including that the code lends the encounter header date without checking the line when the figure can't be located. The review is in `/Users/arsis/zlayt-pm-project/reviews/T-207-staff-engineer-r2.md`.
