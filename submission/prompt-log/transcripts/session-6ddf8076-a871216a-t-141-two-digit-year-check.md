# Subagent: T-141 two-digit-year check (T-141 two-digit-year check)

Source: `agent-a871216a11138abd1.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T15:27:51.877Z

Run a scoped check of board card T-141 (commit 78b6a33) in /Users/arsis/zlayt-pm-project. Read reviews/T-141-staff-engineer-r7.md (the blocker) and scope cut 13f in memory/SCOPE_CUTS.md, which records the accepted residuals.

On a `git archive HEAD` copy, verify only these:
- Two-digit-year dates on or after the accident inside a labelled plural history list now raise a conflict.
- The r7 blocker case is fixed.
- lib11 is unchanged.
- The conflict suites pass.

The e2e red in test_conflict_skipped.py is owned by T-164; don't count it here.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-141-staff-engineer-r8.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T15:27:53.701Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T15:27:53.713Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T15:27:53.922Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r7.md"
}
````

### User / tool · 2026-11-02T15:27:53.929Z

**tool result**
````
1	# T-141 staff-engineer scoped check, round 7 (ff1256e, HEAD ba21b4b)
2	
3	Verdict: **fail** (1 blocker, 1 major).
4	
5	Scope: only the three items the orchestrator named after r6 (ff1256e), plus lib11 unchanged and the conflict suites. Verified on a `git archive ba21b4b` copy. HEAD ba21b4b differs from ff1256e only in memory/SCOPE_CUTS.md, so the code reviewed is the ff1256e code.
6	
7	Results by item:
8	1. Governance per clause: PASS. 19 probe rows (G1-G19) match. 'No prior accidents and was rear-ended 3/1.' is a conflict.
9	2. Plural and bare hit/impact forms: PASS for every form in the r6 F2 spec and the orchestrator's list (20 rows, P1-P20, plus controls). Residual bare-hit phrasings ('Hit in the head', 'Hit the windshield', 'Hit his head') read info-only. Not counted: they are residual phrasings under scope cut 13f.
10	3. Plural-history exemption vs date on/after the accident, or this/the/current: FAIL. Q15, Q11, and the this/the/current/last rows hold, but a labelled plural list that names the accident date in a two-digit-year form still prints info. Blocker (finding 1). I did not count it under 13f: 13f records word-rule phrasings that D-061 leaves info, and this is a date the rule names explicitly and the code's own comment says it covers ('a year counts at its year', conflicts.py:61-62).
11	
12	Also checked: lib11 is byte-identical from 824984f to HEAD (blob 0af8fb2). The conflict unit suites pass (554 across 9 modules). The e2e file that tests the lib11 conflict UI is red at HEAD (finding 2). The red predates ff1256e.
13	
14	Findings
15	
16	- **blocker, F1 (item 3):** a labelled plural list that names the accident date with a two-digit year stays info. 'History per patient: car accidents in 2019 and 2022, one on 1/3/26.' (stated accident date 2026-01-03) prints info. Date forms in the same miss class: '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26'. The guard at conflicts.py:67 counts only parsed dates; `dates.find_dates` returns status 'ambiguous' with no iso for numeric forms like '1/3/26', and 'Jan 3, 26' and '3rd Jan 26' are not parsed either. The year fallback at conflicts.py:69 only matches four-digit years. Repro: probe_r7.py row Q19 (artifacts/review-evidence/T-141-r7/probe_r7_head_ba21b4b.txt: 'MISS Q19 item3 expect=conflict got=info'). Pins: `grep -c "/26" tests/unit/test_t141_r6_probes.py` returns 0. Mutant (mutant_plural_guard_off.txt): disabling the parsed-date and referent clauses turns only X12 and X13 red. Q15 and Q11 are carried by the four-digit-year clause alone, so the two-digit form is the untested hole.
17	  Why it matters: item 3 says the exemption does not apply when the list names a date on or after the accident. The code hides that date conflict, which loses a fact the paralegal needs (D.2 blocker). The gap is in the code, not in D-061's wording, so it is not the major-class gap r6 recorded for Q15.
18	  Fix: in `_plural_list_ok` (conflicts.py:60-69), read a two-digit year as 20xx and compare it with the stated year. Also treat an 'ambiguous' numeric date whose year is on or after the stated year as on or after it (safe direction, D-055). Keep the parsed-date and four-digit-year clauses.
19	  Acceptance test: probe_r7.py row Q19 prints conflict. Add pins to tests/unit/test_t141_r6_probes.py for '1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26' and '1/26' on the stated date, each conflict. 'one 2015' and the lib11 record 1 text stay info. A mutant that removes the new two-digit clause turns the new pins red.
20	
21	- **major, F2 (conflict suite, e2e):** tests/e2e/test_conflict_skipped.py is 8 of 9 red on HEAD. The red is not from ff1256e. The same file passes 9 of 9 at 824984f (the r6-reviewed commit) and is 8 of 9 at 83f1afd (the parent of ff1256e) and at acad4f6. At 6379c0b and c2913a6, tests/e2e/conftest.py has a SyntaxError (line 89), so the module does not collect there. Evidence: pytest_e2e_skip_824984f.txt ('9 passed'), pytest_e2e_skip_83f1afd.txt and pytest_e2e_skip_acad4f6.txt ('8 failed, 1 passed'), pytest_e2e_skip_6379c0b.txt and pytest_e2e_skip_c2913a6.txt (collection error), pytest_lib11_modules_head.txt lines 30 and 45 (test_conflict_skipped.py:69 and :83). The UI difference I could establish: at HEAD the case opens on the Case overview step and `[data-testid="flags-panel"]` is not in the DOM after the timeline loads (repro_lib11_ui_head.txt: 'no flags-panel on open'). At 824984f the panel is present on open with 2 conflict cards and 1 note (repro_lib11_ui_824984f.txt). The backend data is correct at HEAD (repro_lib11_api_head.txt: denial_vs_history checked, skipped [], 1 RECORDS_PREDATE_ACCIDENT note, 2 pending conflict flags). I did not find the route from the overview to the flags panel at HEAD; clicking btn-start-review did not reveal it in my script.
22	  Why it matters: the brief asks me to confirm the conflict suites pass. This module is a conflict suite and it is red at HEAD. Whether the landing step change is intended (frontend commits in 824984f..acad4f6, e.g. 6379c0b, 0b2ce9c) or the test is stale is an orchestrator decision, so I rate it major, not blocker.
23	  Fix: decide the intended landing. Either restore the flags group on open for a case with conflicts, or update the test to the documented route to the flags group and say so in the test. Also add a collection check so a conftest SyntaxError cannot hide a red suite.
24	  Acceptance test: `tests/e2e/test_conflict_skipped.py` 9 of 9 on a git archive of the fix commit. repro_lib11_ui.py shows the conflict group with the lib11 note and the two denial cards on the documented route.
25	
26	Residuals not counted (scope cut 13f)
27	- Bare hit forms outside the r6 F2 spec read info: 'Hit in the head in October 2025.', 'Hit the windshield in October 2025.', 'Hit his head in 2025.' (probe output in probe_r7_head_ba21b4b.txt is the item-2 set; these three were run inline with the same function).
28	- 13f names 'Denies any accident on 01/03/2026' (info) and 'No prior accidents or collisions' (conflict). The second has the same shape as G7 and conflicts. I did not re-run the first.
29	
30	Minor (I would have done it differently; does not violate the rule as written)
31	- Q27 'History per patient: car accidents in 2019 and 2022, treated at the clinic.' is a conflict because the literal word 'the' is in `_PLURAL_REFERENT` (conflicts.py:30). The rule text says 'this/the/current', so this matches it. Narrowing to 'the latest' or 'the most recent' would avoid false conflicts on benign lists. Safe direction.
32	
33	Exercised
34	1. Read personas/staff-engineer.md in full; reviews/T-141-staff-engineer-r6.md; `python3 tools/board.py show T-141` (notes through the 15:11:07 dispatch); memory/ORCHESTRATOR_DECISIONS.md D-061 (line 69); memory/SCOPE_CUTS.md 13f (line 91); my T-141 r5, r6 and evidence-sha memory notes.
35	2. `git log --oneline -3` shows ba21b4b, ff1256e, 83f1afd. `git diff --stat ff1256e HEAD` shows memory/SCOPE_CUTS.md only.
36	3. `git archive ba21b4b | tar -x` into the scratchpad copy T141r7_head. sha256 of app/backend/conflicts.py (32433731...) equals `git show ba21b4b:app/backend/conflicts.py`.
37	4. Conflict unit suites on the archive, `.venv/bin/python -I -m pytest -q -p no:cacheprovider` over 9 modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t141_r3_variants, test_t116_r4_all_dated_records, test_api_routes, test_t141_d061_closed_exemption, test_t141_r6_probes): 554 passed. Log: pytest_conflict_suites_head.txt.
38	5. lib11-referencing modules on the archive (the 9 above minus the ones not referencing lib11, plus test_amounts_t140, test_t139_unmarked and tests/e2e/test_conflict_skipped.py): 8 failed, 590 passed. All 8 failures are in test_conflict_skipped.py. Log: pytest_lib11_modules_head.txt.
39	6. e2e skip file on archives 824984f, 83f1afd, acad4f6, 6379c0b, c2913a6 (logs pytest_e2e_skip_<sha>.txt).
40	7. lib11: `git ls-tree` blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at 824984f, ff1256e and ba21b4b. `git diff --stat 824984f ba21b4b -- evals/library/case_lib11_priors_and_ledger.*` is empty.
41	8. Probe set for the three items, probe_r7.py run on the archive: 54 rows, 53 match, 1 miss (Q19). Log: probe_r7_head_ba21b4b.txt. Inline `dates.find_dates` and `_describes_event` checks on 14 date spellings (output in the exercised notes above).
42	9. Private fixture server from the archive, lib11 run through the HTTP API (repro_lib11_api.py): repro_lib11_api_head.txt.
43	10. Headless Chromium on the archive servers (repro_lib11_ui.py): repro_lib11_ui_head.txt (no flags-panel on open) and repro_lib11_ui_824984f.txt (conflict group, 2 cards, 1 note).
44	11. Mutant in a fresh scratch copy (mutant_guard.py, no product file touched): parsed-date and referent clauses of `_plural_list_ok` disabled. tests/unit/test_t141_r6_probes.py and test_t141_d061_closed_exemption.py: 2 failed (X12, X13), 202 passed. Log: mutant_plural_guard_off.txt.
45	12. `grep -c "/26" tests/unit/test_t141_r6_probes.py`: 0.
46	13. `python3 tools/board.py validate`: ok (163 files), before this file was written.
47	Not run: full unit suite (the handoff reports other cards' dirty files), pipeline CLI on sample.txt, eval runner, live judge controls, E2E beyond the skip file. No server on :7860.
48	
49	```json
50	{"card": "T-141", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
51	 "scope": "git ba21b4b (HEAD; code identical to ff1256e, only memory/SCOPE_CUTS.md differs). app/backend/conflicts.py, tests/unit/test_t141_r6_probes.py, tests/unit/test_t141_d061_closed_exemption.py, tests/e2e/test_conflict_skipped.py. Evidence: artifacts/review-evidence/T-141-r7/. App: private fixture servers started from git archives on loopback (lib11 library case); nothing on :7860.",
52	 "exercised": [
53	  "Read personas/staff-engineer.md; reviews/T-141-staff-engineer-r6.md; board.py show T-141; memory/ORCHESTRATOR_DECISIONS.md D-061; memory/SCOPE_CUTS.md 13f.",
54	  "git log -3 (ba21b4b, ff1256e, 83f1afd); git diff --stat ff1256e HEAD (memory/SCOPE_CUTS.md only); git archive ba21b4b into scratchpad T141r7_head; sha256 of conflicts.py matches git show.",
55	  "Conflict unit suites on the archive, 9 modules incl. test_t141_r6_probes: 554 passed (pytest_conflict_suites_head.txt).",
56	  "lib11-referencing modules on the archive, 9 modules incl. tests/e2e/test_conflict_skipped.py: 8 failed, 590 passed; all 8 failures in test_conflict_skipped.py (pytest_lib11_modules_head.txt).",
57	  "tests/e2e/test_conflict_skipped.py on archives 824984f (9 passed), 83f1afd (8 failed), acad4f6 (8 failed), 6379c0b and c2913a6 (conftest SyntaxError at line 89); logs pytest_e2e_skip_<sha>.txt.",
58	  "lib11 blob 0af8fb2 at 824984f, ff1256e, ba21b4b (git ls-tree); git diff --stat 824984f ba21b4b on lib11 files is empty.",
59	  "probe_r7.py on the archive: 54 rows (G1-G19 governance, P1-P20 plural and bare forms, Q11-Q28 labelled-list date and referent guard): 53 match, 1 miss Q19 (probe_r7_head_ba21b4b.txt).",
60	  "dates.find_dates and _describes_event on 14 date spellings (1/3/26, 01/03/26, 3/27/26, 1-3-26, 01.03.26, Jan 3, 26, 3rd Jan 26, 1/26, 1/3/2026, 01/03/2026, Jan 3 2026, 2026-01-03, in Jan 2026, 01/2026).",
61	  "repro_lib11_api.py on the HEAD archive: status ready, conflict_types include denial_vs_history, skipped [], 1 RECORDS_PREDATE_ACCIDENT note, 2 pending conflict flags (repro_lib11_api_head.txt).",
62	  "repro_lib11_ui.py (headless Chromium) on HEAD: no flags-panel on open, case opens on Case overview (repro_lib11_ui_head.txt); on 824984f: conflict group with 2 cards and 1 note (repro_lib11_ui_824984f.txt).",
63	  "mutant_guard.py on a fresh scratch copy: parsed-date and referent clauses of _plural_list_ok disabled; r6 probes and d061 suite: 2 failed (X12, X13), 202 passed (mutant_plural_guard_off.txt).",
64	  "grep -c '/26' tests/unit/test_t141_r6_probes.py: 0 two-digit-year rows.",
65	  "python3 tools/board.py validate: ok (163 files).",
66	  "Not run: full unit suite, pipeline CLI on sample.txt, eval runner, live judge controls, E2E beyond the skip file."
67	 ],
68	 "verdict": "fail",
69	 "scores": {"item1_per_clause_governance": 5, "item2_plural_and_bare_forms": 4, "item3_plural_list_date_guard": 2, "lib11_unchanged": 5, "conflict_unit_suites": 5, "conflict_e2e_suite": 2, "tests_assert_behaviour": 3, "llm_code_boundary": 5},
70	 "findings": [
71	  {"severity": "blocker",
72	   "title": "F1 (item 3): a labelled plural list that names the accident date with a two-digit year stays info",
73	   "evidence": "probe_r7.py row Q19 in artifacts/review-evidence/T-141-r7/probe_r7_head_ba21b4b.txt: 'MISS Q19 item3 expect=conflict got=info | History per patient: car accidents in 2019 and 2022, one on 1/3/26.' Date guard counts parsed dates only (conflicts.py:67); find_dates returns status 'ambiguous' with no iso for '1/3/26'; 'Jan 3, 26' and '3rd Jan 26' are not parsed. Year fallback matches four-digit years only (conflicts.py:69). grep -c '/26' tests/unit/test_t141_r6_probes.py = 0. mutant_plural_guard_off.txt: disabling the parsed-date and referent clauses turns only X12, X13 red.",
74	   "why_it_matters": "Item 3 says the plural-history exemption does not apply when the list names a date on or after the accident. The code hides that date conflict for two-digit-year and month-name short forms, so a fact the paralegal needs is lost (D.2 blocker). The gap is in the code, not in D-061's wording, so it is not the major-class wording gap r6 recorded for Q15. Scope cut 13f does not cover it: 13f records word-rule phrasings that D-061 leaves info, and this date is inside the rule the orchestrator named.",
75	   "fix": "In _plural_list_ok (conflicts.py:60-69), read a two-digit year as 20xx and compare it with the stated year. Treat an ambiguous numeric date whose year is on or after the stated year as on or after it (safe direction, D-055). Keep the parsed-date and four-digit-year clauses.",
76	   "acceptance_test": "probe_r7.py row Q19 prints conflict. New pins in tests/unit/test_t141_r6_probes.py: '1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26' on the stated date each conflict; 'one 2015' and the lib11 record 1 text stay info. A mutant removing the new two-digit clause turns the new pins red."},
77	  {"severity": "major",
78	   "title": "F2 (conflict suite): tests/e2e/test_conflict_skipped.py is 8 of 9 red on HEAD; the red predates ff1256e",
79	   "evidence": "pytest_lib11_modules_head.txt:30 (test_conflict_skipped.py:69, conflict-note count 0) and :45 (:83, data-item-id count 0). pytest_e2e_skip_824984f.txt '9 passed'; pytest_e2e_skip_83f1afd.txt and pytest_e2e_skip_acad4f6.txt '8 failed, 1 passed'; pytest_e2e_skip_6379c0b.txt and pytest_e2e_skip_c2913a6.txt: SyntaxError in tests/e2e/conftest.py (line 89). repro_lib11_ui_head.txt: 'no flags-panel on open' (case opens on Case overview). repro_lib11_ui_824984f.txt: conflict group count 1, 2 cards, 1 note. repro_lib11_api_head.txt: backend data correct (denial_vs_history checked, skipped [], 1 note, 2 pending conflict flags).",
80	   "why_it_matters": "The brief asks for confirmation that the conflict suites pass. This module is a conflict suite and it is red at HEAD, and the lib11 conflict is not visible on open in the browser. The red is not from the ff1256e logic (the API output is correct and the file is red at 83f1afd, the parent). Whether the landing change is intended (frontend commits between 824984f and acad4f6, e.g. 6379c0b and 0b2ce9c) or the test is stale is an orchestrator decision, so it is major, not blocker. I did not establish the route from the overview to the flags group at HEAD.",
81	   "fix": "Decide the intended landing. Either show the flags group on open for a case with conflicts, or update the test to the documented route to the flags group and say so in the test. Add a collection check so a conftest SyntaxError cannot hide a red suite.",
82	   "acceptance_test": "tests/e2e/test_conflict_skipped.py 9 of 9 on a git archive of the fix commit. repro_lib11_ui.py shows the lib11 note and the two denial cards on the documented route."}
83	 ],
84	 "whats_right": [
85	  "Item 1 holds: 19 governance rows match, including 'No prior accidents and was rear-ended 3/1.', the r6 F1 examples and semicolon and comma splits; the walk crosses and/or/with/for/of only to injury words (conflicts.py:50).",
86	  "Item 2 holds for every r6 F2 form: plural collisions, MVAs, MVCs, MVIs, crashes, wrecks, incidents, 'hit from', 'hit by', 'hit a object', bare and plural impact; 'Patient hit her weight goal' and 'Impact of ...' stay info.",
87	  "lib11 is byte-identical from 824984f to HEAD (blob 0af8fb2), and the 9 conflict unit modules pass 554 of 554."
88	 ],
89	 "questions_for_chris": [
90	  "Was the case landing on Case overview (not the flags group) an intended change? The lib11 e2e test assumes the flags group on open and is red at HEAD.",
91	  "Does scope cut 13f cover the bare-hit residuals ('Hit in the head', 'Hit the windshield')? I read 13f as covering them and I did not count them. I read it as not covering the two-digit-year date miss in F1."
92	 ]}
93	```
94	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:27:54.577Z

**tool call — Bash**
````
{
 "command": "grep -n \"13f\" -A 12 memory/SCOPE_CUTS.md; echo \"---\"; git rev-parse --is-inside-work-tree 2>&1; git log --oneline -5 2>&1; echo \"---\"; git show --stat 78b6a33 2>&1 | head -40",
 "description": "Read scope cut 13f and inspect commit 78b6a33"
}
````

### User / tool · 2026-11-02T15:27:54.749Z

**tool result**
````
91:| 13f | Pre-accident date conflicts (T-141, D-061) are word-rule based: a few phrasings still read info-only ('Denies any accident on 01/03/2026') and some generic denials now raise a false conflict ('No prior accidents or collisions'). The rule leans to false conflicts (D-055). | A clause parser with negation scope; ~1-2 days + adversarial set. | M3 (T-141) |
---
true
78b6a33 fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)
b576567 tools: pre-commit loads a case with no console errors when frontend files are staged (lesson 6379c0b)
2de5ba9 fix(frontend): T-154 r3 the a-key guard moves from mountSection() (ReferenceError on every case load) into the keydown handler; the duplicate sentence is the backend's own; e2e test_no_console_errors
c3a2af8 docs(orchestrator): D-062 amended - notes yield charges only without a same-provider itemized bill
2ac96cf fix(backend): T-140 D-062 total line 'Billed charges accepted from these records', charge sources by billing header, per-figure rule, CPT/HCPCS normalization
---
commit 78b6a33099b1a0a71645ed8ec1b1d4ace60facbb
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:27:13 2026 -0600

    fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/conflicts.py                  | 13 +++++++++-
 tests/unit/test_t141_r7_two_digit_year.py | 42 +++++++++++++++++++++++++++++++
 2 files changed, 54 insertions(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:27:54.856Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r7_patterns.md"
}
````

### User / tool · 2026-11-02T15:27:54.864Z

**tool result**
````
1	---
2	name: project_t141_r7_patterns
3	description: T-141 r7 ba21b4b (scoped check of ff1256e): plural-list date guard misses two-digit-year and ambiguous-date forms; lib11 e2e skip file red since before ff1256e; conftest SyntaxError makes a bisect step look red
4	metadata:
5	  type: project
6	---
7	
8	T-141 r7 (ff1256e, HEAD ba21b4b = docs-only on top, verdict fail: 1 blocker, 1 major). Review: reviews/T-141-staff-engineer-r7.md. Evidence: artifacts/review-evidence/T-141-r7/.
9	
10	- Items 1 (per-clause governance, 19 rows) and 2 (plural and bare hit/impact, 20 rows) pass. Item 3 fails on two-digit-year dates: "one on 1/3/26", "01/03/26", "Jan 3, 26", "3rd Jan 26", "1/26" stay info. `_plural_list_ok` counts parsed dates only (conflicts.py:67, `dates.find_dates` returns status 'ambiguous' with no iso for numeric slash forms) and the year fallback is four-digit only (conflicts.py:69). No pin in test_t141_r6_probes.py has a two-digit year. Q15 and Q11 are carried by the four-digit-year clause alone (mutant with the parsed-date and referent clauses off: only X12, X13 red).
11	- e2e: tests/e2e/test_conflict_skipped.py is 9/9 green at 824984f, 8/9 red at 83f1afd, acad4f6 and HEAD. The case now opens on Case overview with no flags-panel in the DOM; the backend API for lib11 is correct. Rated major, not blocker, because the landing change may be intended and the route to the flags group was not established.
12	- Collection trap: tests/e2e/conftest.py has a SyntaxError at 6379c0b and c2913a6 (fixed in acad4f6). A bisect step on those shas shows a collection error, not a red test. Check that a sha collects before you read its result.
13	
14	**Why:** the r6 F3 wording said "a year counts at its year", but the guard only recognised four-digit years and parsed dates. The date forms the parser refuses are the ones a paralegal writes in short form.
15	
16	**How to apply:**
17	- When a guard counts dates or years, probe every spelling the parser marks 'ambiguous' or leaves unparsed (1/3/26, Jan 3, 26, 1/26), not only the forms the tests use. Grep the pins for the year width: `grep -c "/26"` returning 0 is a finding.
18	- Scope cut 13f covers word-rule residuals a rule leaves info (bare-hit phrasings, denial phrasings). It does not cover a date the orchestrator's own rule names. Say so in the review when you do not count a residual.
19	- Mutants: disable one guard clause at a time. If the pins still pass with a clause off, check whether another clause carries the same case before calling it unpinned.
20	
21	**Harness notes (this round):**
22	- `timeout` does not exist on this macOS shell. Drop it.
23	- The permission layer denied a Bash command containing `rm -rf`. Use a new empty directory and a Python `shutil.copytree`; do not delete.
24	- The git-guard hook could not parse a Bash line with an escaped backtick in a `python3 -c` regex and blocked it. Write the check to artifacts/review-evidence and run it with `-I`.
25	- Keep probe and mutant scripts under artifacts/review-evidence/<card>-r<n>/ (the reviewer write guard refuses scratchpad writes from Write).
26	
27	Related: [[project_t141_r6_patterns]], [[project_t141_r5_patterns]], [[feedback_evidence_sha_vs_commit]], [[feedback_differential_probe_prior_build]], [[feedback_severity_vs_brief]].
28	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:06.009Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head -20; echo \"---diff\"; git show 78b6a33 -- app/backend/conflicts.py; echo \"---lib11 blobs\"; for s in ba21b4b 78b6a33; do echo -n \"$s: \"; git ls-tree $s evals/library/case_lib11_priors_and_ledger.txt | awk '{print $3}'; done; echo \"---r7 evidence\"; ls artifacts/review-evidence/T-141-r7/ 2>&1 | head -50",
 "description": "Confirm HEAD, read fix diff, check lib11 blobs and r7 evidence"
}
````

### User / tool · 2026-11-02T15:28:06.222Z

**tool result**
````
99438fb194d8a81737bd0bf18b02e0cba0a1c6d8
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
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
---diff
commit 78b6a33099b1a0a71645ed8ec1b1d4ace60facbb
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:27:13 2026 -0600

    fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/conflicts.py b/app/backend/conflicts.py
index f86057e..7fffd0b 100644
--- a/app/backend/conflicts.py
+++ b/app/backend/conflicts.py
@@ -57,6 +57,15 @@ def _governed(clause: str, m, plural_ok: bool = True) -> bool:
     return False
 
 
+_MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?"
+_TWO_DIGIT_YEARS = re.compile(                                                        # a two-digit year in a date shape; the year is the one group that matched
+    r"(?<![\d/.\-])(?:0?[1-9]|[12]\d|3[01])[/.\-](?:0?[1-9]|[12]\d|3[01])[/.\-](\d{2})(?!\d)"        # 1/3/26, 01/03/26, 1-3-26, 01.03.26
+    r"|(?<![\d/.\-])(?:0?[1-9]|1[0-2])/(\d{2})(?!\d)"                                            # 1/26 (month/year)
+    r"|\b" + _MONTH + r"\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(\d{2})(?!\d)"                                # Jan 3, 26
+    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+" + _MONTH + r",?\s+(\d{2})(?!\d)",                                # 3rd Jan 26
+    re.I)
+
+
 def _plural_list_ok(unit: str, iso) -> bool:
     """T-141 r6 (F3): the plural-under-a-history-label exemption holds only when the whole sentence names no date on or after the stated accident date (a year
     counts at its year) and no referent word ('this one', 'the latest', 'current'): 'History per patient: accidents, this one on 01/03/2026' is the accident."""
@@ -66,7 +75,9 @@ def _plural_list_ok(unit: str, iso) -> bool:
         return True
     if any(d["status"] == "parsed" and d["iso"] >= iso for d in dates.find_dates(unit)):
         return False
-    return not any(int(y) >= int(iso[:4]) for y in re.findall(r"\b((?:19|20)\d\d)\b", unit))
+    if any(int(y) >= int(iso[:4]) for y in re.findall(r"\b((?:19|20)\d\d)\b", unit)):
+        return False
+    return not any(2000 + int(next(g for g in m if g)) >= int(iso[:4]) for m in _TWO_DIGIT_YEARS.findall(unit))     # T-141 r7 (F1): '1/3/26' reads as 2026
 
 
 def _describes_event(rec: dict, iso=None) -> bool:
---lib11 blobs
ba21b4b: 0af8fb29950a38383b5e55b1dc082cacb098d49d
78b6a33: 0af8fb29950a38383b5e55b1dc082cacb098d49d
---r7 evidence
check_review_json.py
mutant_guard.py
mutant_plural_guard_off.txt
probe_r7.py
probe_r7_head_ba21b4b.txt
pytest_conflict_suites_head.txt
pytest_e2e_skip_6379c0b.txt
pytest_e2e_skip_824984f.txt
pytest_e2e_skip_83f1afd.txt
pytest_e2e_skip_acad4f6.txt
pytest_e2e_skip_c2913a6.txt
pytest_lib11_modules_head.txt
repro_lib11_api.py
repro_lib11_api_head.txt
repro_lib11_run.py
repro_lib11_ui.py
repro_lib11_ui_824984f.txt
repro_lib11_ui_head.txt
repro_lib11_ui_head_noflags.png
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:08.674Z

**tool call — Bash**
````
{
 "command": "git log --oneline 78b6a33..HEAD; echo \"--- files changed since 78b6a33\"; git diff --stat 78b6a33 HEAD -- app tests evals | tail -30; echo \"--- conflicts.py blob at HEAD vs 78b6a33\"; git rev-parse HEAD:app/backend/conflicts.py 78b6a33:app/backend/conflicts.py",
 "description": "List commits after 78b6a33 and files that changed"
}
````

### User / tool · 2026-11-02T15:28:08.820Z

**tool result**
````
99438fb fix(backend): T-161 r2 first-run failure driven by failed_steps (flag step down with no phrase-list hit reads run_partial), extract-down first run with no entries reads failed
--- files changed since 78b6a33
 app/backend/pipeline.py                            | 13 +++-
 .../unit/test_t146_r2_failed_rerun_keeps_items.py  |  4 +-
 .../test_t146_r3_decided_items_never_lowered.py    |  2 +-
 tests/unit/test_t161_first_run_stage_down.py       | 76 ++++++++++++++++++++--
 4 files changed, 85 insertions(+), 10 deletions(-)
--- conflicts.py blob at HEAD vs 78b6a33
7fffd0b298a0b1864a42a02b9387011d06a9b8de
7fffd0b298a0b1864a42a02b9387011d06a9b8de
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:13.354Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"$SP\"; ls -la \"$SP\" 2>&1 | head; echo \"--- untracked under app/tests/evals:\"; git status --short --untracked-files=all -- app tests evals | grep '^??' | head; echo \"--- ls-files count\"; git ls-files | wc -l",
 "description": "Check scratchpad and untracked files under product paths"
}
````

### User / tool · 2026-11-02T15:28:13.544Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
total 354240
drwx------@ 1514 arsis  wheel    48448 Nov  2 09:27 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 07:36 .claude
-rw-r--r--@    1 arsis  wheel      403 Nov  2 07:36 .gitignore
drwxr-xr-x@    6 arsis  wheel      192 Nov  2 08:00 .pytest_cache
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
-rw-r--r--@    1 arsis  wheel     6786 Nov  2 07:36 CLAUDE.md
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
--- untracked under app/tests/evals:
?? app/backend/money.py
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
--- ls-files count
    2244
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:17.498Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; D=\"$SP/T141r8_head_99438fb\"; mkdir -p \"$D\" && cd /Users/arsis/zlayt-pm-project && git archive 99438fb | tar -x -C \"$D\" && echo \"extracted to $D\" && ls \"$D\" && cd \"$D\" && git -C /Users/arsis/zlayt-pm-project rev-parse 99438fb && shasum -a 256 app/backend/conflicts.py && git -C /Users/arsis/zlayt-pm-project show 99438fb:app/backend/conflicts.py | shasum -a 256; ls \"$D/tests/unit\" | grep -E \"t141|conflict|t093_j3|t116_r4|api_routes\" ",
 "description": "Extract git archive of HEAD into a fresh scratchpad copy"
}
````

### User / tool · 2026-11-02T15:28:18.835Z

**tool result**
````
extracted to /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
99438fb194d8a81737bd0bf18b02e0cba0a1c6d8
a66f164e9ac851e6bf444707323ffa6a6cca790041df92f10c141a4cf2313317  app/backend/conflicts.py
a66f164e9ac851e6bf444707323ffa6a6cca790041df92f10c141a4cf2313317  -
test_api_routes.py
test_conflict_candidates.py
test_conflicts.py
test_t093_j3_controls_reachable.py
test_t116_r4_all_dated_records.py
test_t141_checks_per_case.py
test_t141_d061_closed_exemption.py
test_t141_r3_variants.py
test_t141_r6_probes.py
test_t141_r7_two_digit_year.py
test_t146_r4_ladder_compare_and_conflicts.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:21.418Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; cat \"$D/tests/unit/test_t141_r7_two_digit_year.py\"; echo \"=== probe_r7 head\"; sed -n '1,60p' /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r7/probe_r7.py",
 "description": "Read the r7 fix test file and the r7 probe script"
}
````

### User / tool · 2026-11-02T15:28:21.515Z

**tool result**
````
"""T-141 r7 (F1, staff-engineer blocker): a labelled plural history list that names a date on or after the stated accident date in a two-digit-year form
('1/3/26', '1-3-26', 'Jan 3, 26', '1/26') is the accident, not history: conflict. Years before the stated year, and four-digit variants, behave as before.
Case: stated accident date 2026-01-03 (so '1/3/26' is the accident date itself)."""
import pytest

from app.backend import conflicts as C

LABEL = "History per patient: car accidents in 2019 and 2022, "


def classify(ex):
    r = [dict(n=1, date_iso="2026-01-02", source="PCP", excerpt=ex, kind="encounter"),
         dict(n=2, date_iso="2026-01-12", source="PT", excerpt="Exam: ok.", kind="encounter"),
         dict(n=3, date_iso="2026-01-20", source="Intake", excerpt="Date of accident per intake form: 2026-01-03.", kind="encounter")]
    if C.accident_date_conflicts(r):
        return "conflict"
    return "info" if C.accident_date_note(r) else "none"


ON_OR_AFTER = [   # the reviewer's Q19 and its date-form class, plus 4-digit variants
    "one on 1/3/26.", "one on 01/03/26.", "one on 1-3-26.", "one on 03-01-26.", "one on 3/1/26.", "one on 01.03.26.", "one on Jan 3, 26.", "one on 3rd Jan 26.",
    "one on 1/26.", "one on 3/27/26.", "one on 1/3/2026.", "one on 01/03/2026.", "one on 03-01-2026.", "one on Jan 3, 2026.", "one in 2026.",
]
BEFORE = ["one in 2015.", "one on 1/3/15.", "one on 01-03-15.", "one on 1/3/25.", "one on Jan 3, 25.", "one on 3rd Jan 25.", "one on 12/25.", "one on 1/3/2015."]


@pytest.mark.parametrize("tail", ON_OR_AFTER)
def test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict(tail):
    assert classify(LABEL + tail) == "conflict", tail


@pytest.mark.parametrize("tail", BEFORE)
def test_dates_before_the_accident_year_stay_history(tail):
    assert classify(LABEL + tail) == "info", tail


def test_reviewer_blocker_case_q19():
    assert classify("History per patient: car accidents in 2019 and 2022, one on 1/3/26.") == "conflict"


def test_blood_pressure_is_not_a_date():
    assert classify("History per patient: car accidents in 2019 and 2022, BP 120/80.") == "info"
=== probe_r7 head
"""Reviewer probe (T-141 r7): the three scoped items on a git archive of HEAD ba21b4b (code identical to ff1256e).
Calls app.backend.conflicts._describes_event(rec, stated_iso) directly: True = a pre-accident record that describes the collision
(date CONFLICT), False = info-only. Usage: .venv/bin/python -I probe_r7.py <archive_dir>
Each row: (id, item, excerpt, stated accident ISO date, expected 'conflict' | 'info', note)."""
import os
import sys

ARCHIVE = os.path.abspath(sys.argv[1])
sys.path.insert(0, ARCHIVE)
os.chdir(ARCHIVE)
from app.backend import conflicts as C  # noqa: E402

SIG = "2026-03-18"   # lib11 stated accident date
J = "2026-01-03"     # the Q15 stated date

ROWS = [
    # ---- item 1: governance per clause ----
    ("G1", 1, "No prior accidents and was rear-ended 3/1.", SIG, "conflict", "scoped item 1 example (3/1)"),
    ("G2", 1, "Denies prior accidents and rear-ended in October 2025.", SIG, "conflict", "r6 F1 example"),
    ("G3", 1, "No prior accidents and rear-ended 03/01/2026.", SIG, "conflict", "same shape, full date"),
    ("G4", 1, "Prior accident and rear-ended this week.", SIG, "conflict", "r6 L9"),
    ("G5", 1, "No prior accidents; was rear-ended 3/1.", SIG, "conflict", "semicolon split"),
    ("G6", 1, "No prior accidents, rear-ended 03/14/2024.", SIG, "conflict", "comma split"),
    ("G7", 1, "No prior accidents and collision in October 2025.", SIG, "conflict", "r6 L2 style, collision noun"),
    ("G8", 1, "No prior accidents and no rear-end collision.", SIG, "info", "second negation governs the mechanism"),
    ("G9", 1, "No prior accidents or injuries.", SIG, "info", "injury word after link stays governed"),
    ("G10", 1, "Previous accident with whiplash.", SIG, "info", "r6 pinned info control"),
    ("G11", 1, "No prior accidents and whiplash.", SIG, "info", "injury after link stays governed"),
    ("G12", 1, "Previously had an MVA and was rear-ended.", SIG, "conflict", "history verb then ungoverned verb"),
    ("G13", 1, "No LOC after the accident.", SIG, "conflict", "label-free negation does not reach the accident"),
    ("G14", 1, "Prior accidents: No.", SIG, "info", "lib11 intake form shape (explicit prior, negated)"),
    ("G15", 1, "No prior accidents and struck by a car.", SIG, "conflict", "struck after link"),
    ("G16", 1, "No prior accidents but rear-ended 3/1.", SIG, "conflict", "but is not a link"),
    ("G17", 1, "No prior injuries and was rear-ended 3/1.", SIG, "conflict", "injury governor, then ungoverned verb"),
    ("G18", 1, "No prior accidents with whiplash and was rear-ended 3/1.", SIG, "conflict", "injury link, then ungoverned verb"),
    ("G19", 1, "Denies accidents of whiplash and was struck by a car.", SIG, "conflict", "of-injury link, then struck"),
    # ---- item 2: plural and bare hit / impact forms ----
    ("P1", 2, "Collisions in October 2025.", SIG, "conflict", "r6 R30 plural noun"),
    ("P2", 2, "Two collisions last week.", SIG, "conflict", "r6 R31"),
    ("P3", 2, "Two MVAs last week.", SIG, "conflict", "r6 R32"),
    ("P4", 2, "Two MVCs in October 2025.", SIG, "conflict", "r6 R33"),
    ("P5", 2, "MVIs in October 2025.", SIG, "conflict", "MVI plural"),
    ("P6", 2, "Crashes in 2025.", SIG, "conflict", "crash plural"),
    ("P7", 2, "Wrecks last year.", SIG, "conflict", "wreck plural"),
    ("P8", 2, "Incidents in October 2025.", SIG, "conflict", "incident plural"),
    ("P9", 2, "Hit from behind this week.", SIG, "conflict", "r6 R29 bare hit from"),
    ("P10", 2, "Hits from behind this week.", SIG, "conflict", "hits from (plural verb form)"),
    ("P11", 2, "Hit by a car in 2025.", SIG, "conflict", "hit by"),
    ("P12", 2, "Hit a pole in 2025.", SIG, "conflict", "hit a object"),
    ("P13", 2, "Impact noted in October 2025.", SIG, "conflict", "r6 R35 bare impact"),
    ("P14", 2, "Impacts noted in October 2025.", SIG, "conflict", "plural impacts"),
    ("P15", 2, "Impact with a pole in 2025.", SIG, "conflict", "impact with"),
    ("P16", 2, "Impacted the wall in 2025.", SIG, "conflict", "impacted"),
    ("P17", 2, "Patient hit her weight goal of 150 lb.", SIG, "info", "r6 V13 control stays info"),
    ("P18", 2, "Impact of physical therapy on function.", SIG, "info", "impact of excluded control"),
    ("P19", 2, "History per patient: collisions in 2019 and 2022.", J, "info", "plural under label, years only (lib11-type)"),
    ("P20", 2, "Rear-end collisions in October 2025.", SIG, "conflict", "compound plural"),
    # ---- item 3: plural-history exemption with date on/after accident, or this/the/current ----
    ("Q15", 3, "History per patient: accidents, this one on 01/03/2026.", J, "conflict", "r6 F3 Q15 (regression vs r5)"),
    ("Q11", 3, "History per patient: car accidents in 2019 and 2022, the latest one on 01/03/2026.", J, "conflict", "r6 F3 Q11"),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:40.281Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; cd \"$D\" && ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py tests/unit/test_t141_d061_closed_exemption.py tests/unit/test_t141_r6_probes.py tests/unit/test_t141_r7_two_digit_year.py 2>&1 | tail -25",
 "description": "Run the ten conflict unit modules on the HEAD archive"
}
````

### User / tool · 2026-11-02T15:28:50.798Z

**tool result**
````
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 /Users/arsis/zlayt-pm-project/.venv/bin/python -> python3.12
........................................................................ [ 12%]
........................................................................ [ 24%]
........................................................................ [ 37%]
........................................................................ [ 49%]
........................................................................ [ 62%]
........................................................................ [ 74%]
........................................................................ [ 87%]
........................................................................ [ 99%]
...                                                                      [100%]
579 passed in 9.71s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:28:56.715Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-141-r8 && D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\" && cd \"$D\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py tests/unit/test_t141_d061_closed_exemption.py tests/unit/test_t141_r6_probes.py tests/unit/test_t141_r7_two_digit_year.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/pytest_conflict_suites_head_99438fb.txt 2>&1; echo \"exit=$?\"; tail -1 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/pytest_conflict_suites_head_99438fb.txt; echo \"--- new file verbose\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -v tests/unit/test_t141_r7_two_digit_year.py 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/pytest_r7_two_digit_year_head.txt | tail -45; echo \"--- probe_r7 on HEAD archive\"; cp /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r7/probe_r7.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/probe_r7_rerun.py; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/probe_r7_rerun.py \"$D\" 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/probe_r7_head_99438fb.txt | tail -12",
 "description": "Save conflict suite log, run new r7 test file verbosely, rerun r7 probe"
}
````

### User / tool · 2026-11-02T15:29:06.794Z

**tool result**
````
exit=0
579 passed in 9.15s
--- new file verbose
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 25 items

tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1/3/26.] PASSED [  4%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 01/03/26.] PASSED [  8%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1-3-26.] PASSED [ 12%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 03-01-26.] PASSED [ 16%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 3/1/26.] PASSED [ 20%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 01.03.26.] PASSED [ 24%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on Jan 3, 26.] PASSED [ 28%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 3rd Jan 26.] PASSED [ 32%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1/26.] PASSED [ 36%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 3/27/26.] PASSED [ 40%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1/3/2026.] PASSED [ 44%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 01/03/2026.] PASSED [ 48%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 03-01-2026.] PASSED [ 52%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on Jan 3, 2026.] PASSED [ 56%]
tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one in 2026.] PASSED [ 60%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one in 2015.] PASSED [ 64%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on 1/3/15.] PASSED [ 68%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on 01-03-15.] PASSED [ 72%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on 1/3/25.] PASSED [ 76%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on Jan 3, 25.] PASSED [ 80%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on 3rd Jan 25.] PASSED [ 84%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on 12/25.] PASSED [ 88%]
tests/unit/test_t141_r7_two_digit_year.py::test_dates_before_the_accident_year_stay_history[one on 1/3/2015.] PASSED [ 92%]
tests/unit/test_t141_r7_two_digit_year.py::test_reviewer_blocker_case_q19 PASSED [ 96%]
tests/unit/test_t141_r7_two_digit_year.py::test_blood_pressure_is_not_a_date PASSED [100%]

============================== 25 passed in 0.17s ==============================
--- probe_r7 on HEAD archive
ok   Q18  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one in January 2026. | month-year in stated year
ok   Q19  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 1/3/26. | two-digit year on stated date
ok   Q20  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, most recent in 2019. | referent 'most recent'
ok   Q21  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, current MVA referral. | referent 'current'
ok   Q22  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, last one in 2019. | referent 'last'
ok   Q23  item3 expect=info     got=info     | History per patient: car accidents in 2019 and 2022, earlier one 2015. | years only, earlier: exemption holds
ok   Q24  item3 expect=info     got=info     | History per patient: car accidents in 2019 and 2022. | bare years, stated 2026
ok   Q25  item3 expect=info     got=info     | History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. | lib11 record 1 text verbatim
ok   Q26  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022. This one on 01/03/2026 was rear-ended. | second sentence names event + pronoun
ok   Q27  item3 expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, treated at the clinic. | literal 'the' is in the referent set (orchestrator rule says this/the/current); false conflict, safe direction
ok   Q28  item3 expect=info     got=info     | History per patient: car accidents in 2019 and 2022. Also one on 01/03/2026. | date in the next sentence with no accident word (residual, see notes)
total=54 mismatches=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:12.922Z

**tool call — Bash**
````
{
 "command": "grep -n \"Also one on\\|Q28\\|next sentence\" reviews/T-141-staff-engineer-r6.md | head; echo \"--- D-061\"; grep -n \"D-061\" memory/ORCHESTRATOR_DECISIONS.md | head -3; awk '/D-061/{f=1} f&&n<12{print; n++}' memory/ORCHESTRATOR_DECISIONS.md | head -14",
 "description": "Check r6 record for the second-sentence residual and D-061 wording"
}
````

### User / tool · 2026-11-02T15:29:13.140Z

**tool result**
````
--- D-061
69:| D-061 | Pre-accident records: one simple rule (2026-11-02, T-141 after 5 rounds). A record dated before the stated accident date is info-only ONLY when every accident/mechanism word in it is governed by an explicit "prior/previous/earlier" or a negation of prior accidents ("no prior accidents", "denies previous MVA", "Prior accidents: No"). Any other accident or mechanism word, noun or verb (accident, collision, crash, MVC/MVA, rear-end(ed), struck, hit, pedestrian, impact), with or without a date or "last year", makes it a date conflict. No date-distance exemptions. Second closed exemption (accepted after T-141 implementation): a PLURAL accident noun under a history label ('History per patient: car accidents in 2019 and 2022') names several earlier events, not the accident, and is info-only; a singular one ('History: MVC', 'History: rear-ended') is a conflict. A false conflict is the safe direction (D-055). | Five rounds of word-level exemptions kept hiding true conflicts; one closed exemption cannot be outworded. | T-141 r1–r5 |
| D-061 | Pre-accident records: one simple rule (2026-11-02, T-141 after 5 rounds). A record dated before the stated accident date is info-only ONLY when every accident/mechanism word in it is governed by an explicit "prior/previous/earlier" or a negation of prior accidents ("no prior accidents", "denies previous MVA", "Prior accidents: No"). Any other accident or mechanism word, noun or verb (accident, collision, crash, MVC/MVA, rear-end(ed), struck, hit, pedestrian, impact), with or without a date or "last year", makes it a date conflict. No date-distance exemptions. Second closed exemption (accepted after T-141 implementation): a PLURAL accident noun under a history label ('History per patient: car accidents in 2019 and 2022') names several earlier events, not the accident, and is info-only; a singular one ('History: MVC', 'History: rear-ended') is a conflict. A false conflict is the safe direction (D-055). | Five rounds of word-level exemptions kept hiding true conflicts; one closed exemption cannot be outworded. | T-141 r1–r5 |
| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the total. Charge sources are positively identified: only documents with a billing header (itemized statement, ledger, invoice, UB-04, CMS-1500) can yield a `charge`; clinical notes and discharge summaries yield a charge only from an encounter line, and never once the case holds an itemized bill from the same provider (amended at implementation: a literal ban zeroed the sample, whose charges are stated in visit notes); insurer and unknown documents never can. CPT/HCPCS codes are normalized ('CPT 99213' = '99213') before duplicate matching. Residual: a summary row dressed as a service line can still be accepted by a careless reviewer; it is cited and individually accepted, and listed as accepted debt. | An adversary can always word a ledger past a classifier; the honest claim is a sum of human-accepted, cited lines. | T-140 claims-adjuster r3 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:16.993Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; grep -n \"_plural_list_ok\\|def \\|split\" \"$D/app/backend/conflicts.py\" | head -60",
 "description": "Locate unit splitting and plural-list call sites in HEAD conflicts.py"
}
````

### User / tool · 2026-11-02T15:29:17.081Z

**tool result**
````
36:def _governed(clause: str, m, plural_ok: bool = True) -> bool:
42:    toks = clause[:m.start()].split()
69:def _plural_list_ok(unit: str, iso) -> bool:
72:    if any(w.strip(".,;:()\"'").lower() in _PLURAL_REFERENT for w in unit.split()):
83:def _describes_event(rec: dict, iso=None) -> bool:
89:        plural_ok = _plural_list_ok(unit, iso)
92:        for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
99:def _event_records(s: dict, records: list) -> list:
104:def _encounters(records):
109:def stated_accident_dates(records: list) -> list:
132:def accident_date_conflicts(records: list) -> list:
180:def accident_date_note(records: list):
201:def _surname(segment: str):
209:def _norm(s):
210:    return " ".join((s or "").split()).casefold()
213:def parse_provider(label: str) -> dict:
215:    segs = [s.strip() for s in (label or "").split(",") if s.strip()]
221:def provider_conflicts(records: list) -> list:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:19.655Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; sed -n '20,35p;83,98p' \"$D/app/backend/conflicts.py\"",
 "description": "Read unit split and clause split in HEAD conflicts.py"
}
````

### User / tool · 2026-11-02T15:29:19.740Z

**tool result**
````
                    r"hit\s+(?:a|the|my|our)\s+(?:car|vehicle|truck|pole|tree|wall|guardrail|curb)|"
                    r"airbag\w*|seat\s?belt\w*|t-?bone\w*|side-?swip\w*|(?:run|ran)\s+over|run-over|"
                    r"fell|fall(?:ing)?\s+(?:from|off|down)|slip(?:ped)?\s+and\s+fall|whiplash|injur\w*(?!\s+prevention)|trauma\w*|impact(?:ed)?\s+(?:with|to|from|on\s+the)|impacts?(?!\s+(?:of|on)\b)|on\s+impact|impacted|LOC|loss\s+of\s+consciousness)\b", re.I)
_NEGATOR = {"no", "not", "denies", "denied", "denying", "without", "never", "negative", "neg", "none", "nor", "free"}
_HIST_WORD = {"prior", "previous", "earlier"}                                                         # D-061: only an explicit prior modifies the event noun (not "prior to")
_HIST_VERBS = {"had", "suffered", "been", "involved", "in", "was"}                                      # "previously had an MVA"; not "previously reported the MVA"
_FILLER = {"a", "an", "any", "all", "some", "other", "further", "known", "recent", "major", "minor", "serious", "significant", "new",
           "motor", "vehicle", "vehicular", "car", "auto", "traffic", "head", "neck", "back", "rear", "end"}      # words a negator or history word may reach through to the event noun
_LINKS = {"or", "and", "of", "for", "with"}                                                              # T-141 r6 (F1): a governor crosses these only to an injury word ('no prior accidents or injuries', 'previous accident with whiplash')
_INJURY = re.compile(r"whiplash|injur\w*|trauma\w*|LOC|loss\s+of\s+consciousness", re.I)                      # never an accident or mechanism: 'No injury or rear-ended' keeps the second event ungoverned
_PLURAL_REFERENT = {"this", "these", "the", "current", "currently", "latest", "recent", "last", "now", "today"}  # T-141 r6 (F3): a labelled plural list that points at the index event is not history
_HISTORY_LABEL = re.compile(r"(?:history|hx|pmh)(?:\s+\w+){0,2}:")                                       # "History per patient:" / "Hx:"
_PLURAL_EVENT = re.compile(r"(?:accidents|collisions|crashes|wrecks|MVAs|MVCs|MVIs)", re.I)         # T-141 r6: the lib11 PCP list ("History per patient: car accidents in 2019 and 2022"); a plural event under a history label is a list of past events
_CLAUSE_SPLIT = re.compile(r"[;,]|\s[-\u2013\u2014]\s|\s\(|\)")


def _describes_event(rec: dict, iso=None) -> bool:
    """D-061: the record has ANY injury, mechanism or accident word not governed by an explicit prior/previous/earlier or a negation (judged per clause and per word)."""
    from app.backend import sentences
    text = rec.get("excerpt") or ""
    for a, b in sentences.stripped_spans(text):
        unit = text[a:b]
        plural_ok = _plural_list_ok(unit, iso)
        for d in dates.find_dates(unit):                                     # "January 9, 2026" is one date, not two clauses
            unit = unit[:d["start"]] + d["text"].replace(",", "\x01") + unit[d["end"]:]
        for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
            for m in _EVENT.finditer(clause):
                if not _governed(clause, m, plural_ok):
                    return True
    return False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:32.962Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/probe_r8.py",
 "content": "\"\"\"Reviewer probe (T-141 r8): item 1 of the scoped check on a git archive of HEAD.\nUses the same classify() as tests/unit/test_t141_r7_two_digit_year.py: the full accident_date_conflicts / accident_date_note path,\nstated accident date 2026-01-03 (the r7 Q19 case). Usage: .venv/bin/python -I probe_r8.py <archive_dir>\nEach row: (id, excerpt, expected, note). Expected values are the reviewer's spec: a two-digit date on or after the stated accident\ndate inside a labelled plural history list is 'conflict'; a date before the stated year is 'info'. Rows marked 'design' are the\nyear-counts-at-its-year rule (safe direction, D-055) and are reported, not counted as misses, if they hold.\"\"\"\nimport os\nimport sys\n\nARCHIVE = os.path.abspath(sys.argv[1])\nsys.path.insert(0, ARCHIVE)\nos.chdir(ARCHIVE)\nfrom app.backend import conflicts as C  # noqa: E402\n\nLABEL = \"History per patient: car accidents in 2019 and 2022, \"\n\n\ndef classify(ex):\n    r = [dict(n=1, date_iso=\"2026-01-02\", source=\"PCP\", excerpt=ex, kind=\"encounter\"),\n         dict(n=2, date_iso=\"2026-01-12\", source=\"PT\", excerpt=\"Exam: ok.\", kind=\"encounter\"),\n         dict(n=3, date_iso=\"2026-01-20\", source=\"Intake\", excerpt=\"Date of accident per intake form: 2026-01-03.\", kind=\"encounter\")]\n    if C.accident_date_conflicts(r):\n        return \"conflict\"\n    return \"info\" if C.accident_date_note(r) else \"none\"\n\n\nROWS = [\n    (\"T1\", LABEL + \"one on 1/3/26.\", \"conflict\", \"r7 Q19 blocker, verbatim\"),\n    (\"T2\", LABEL + \"one on Jan 3, 26.\", \"conflict\", \"month-name short form, same day\"),\n    (\"T3\", LABEL + \"one on 3rd Jan 26.\", \"conflict\", \"ordinal day-month-yy\"),\n    (\"T4\", LABEL + \"one on 1/26.\", \"conflict\", \"month/yy, same month as accident\"),\n    (\"T5\", LABEL + \"one on 12/31/26.\", \"conflict\", \"later date, two-digit year\"),\n    (\"T6\", LABEL + \"one on 1/3/25 and one on 2/1/26.\", \"conflict\", \"one before, one after in the same sentence\"),\n    (\"T7\", LABEL + \"one on 12/31/25.\", \"info\", \"two-digit year before the stated year\"),\n    (\"T8\", LABEL + \"one on Jan 3, 25.\", \"info\", \"month-name two-digit before the stated year\"),\n    (\"T9\", LABEL + \"one on 1/2/26.\", \"conflict\", \"design: same year, earlier day; a year counts at its year (D-055)\"),\n    (\"T10\", LABEL + \"one on 1/3/99.\", \"conflict\", \"design: 99 reads 2099 (20xx rule); a 1999 date becomes a false conflict (D-055)\"),\n    (\"T11\", LABEL + \"BP 120/80.\", \"info\", \"slash score, not a date\"),\n    (\"T12\", LABEL + \"pain 6/10.\", \"info\", \"pain score 6/10 reads 2010\"),\n    (\"T13\", LABEL + \"pain 5/30.\", \"conflict\", \"design/residual: pain score 5/30 reads 2030 (false conflict, safe direction)\"),\n    (\"T14\", \"History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.\", \"conflict\", \"second sentence, two-digit (same class as r6 Q28 four-digit)\"),\n    (\"T15\", \"History per patient: car accidents in 2019 and 2022. Also one on 01/03/2026.\", \"info\", \"r6 Q28 residual, four-digit, second sentence (unchanged)\"),\n    (\"T16\", \"History per patient: accidents, this one on 1/3/26.\", \"conflict\", \"referent word plus two-digit date\"),\n    (\"T17\", \"History per patient: car accidents in 2019 and 2022, one in 2015 and one on 1/3/15.\", \"info\", \"all before the stated year\"),\n]\n\nmismatch = 0\nfor rid, ex, expect, note in ROWS:\n    got = classify(ex)\n    flag = \"ok  \" if got == expect else \"MISS\"\n    if got != expect:\n        mismatch += 1\n    print(f\"{flag} {rid:<4} expect={expect:<8} got={got:<8} | {ex} | {note}\")\nprint(f\"total={len(ROWS)} mismatches={mismatch}\")\n"
}
````

### User / tool · 2026-11-02T15:29:33.126Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/probe_r8.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:35.750Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-141-r8/probe_r8.py \"$D\" 2>&1 | tee artifacts/review-evidence/T-141-r8/probe_r8_head_99438fb.txt",
 "description": "Run item-1 boundary probe on the HEAD archive"
}
````

### User / tool · 2026-11-02T15:29:35.981Z

**tool result**
````
ok   T1   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 1/3/26. | r7 Q19 blocker, verbatim
ok   T2   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on Jan 3, 26. | month-name short form, same day
ok   T3   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 3rd Jan 26. | ordinal day-month-yy
ok   T4   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 1/26. | month/yy, same month as accident
ok   T5   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 12/31/26. | later date, two-digit year
ok   T6   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 1/3/25 and one on 2/1/26. | one before, one after in the same sentence
ok   T7   expect=info     got=info     | History per patient: car accidents in 2019 and 2022, one on 12/31/25. | two-digit year before the stated year
ok   T8   expect=info     got=info     | History per patient: car accidents in 2019 and 2022, one on Jan 3, 25. | month-name two-digit before the stated year
ok   T9   expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 1/2/26. | design: same year, earlier day; a year counts at its year (D-055)
ok   T10  expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, one on 1/3/99. | design: 99 reads 2099 (20xx rule); a 1999 date becomes a false conflict (D-055)
ok   T11  expect=info     got=info     | History per patient: car accidents in 2019 and 2022, BP 120/80. | slash score, not a date
ok   T12  expect=info     got=info     | History per patient: car accidents in 2019 and 2022, pain 6/10. | pain score 6/10 reads 2010
ok   T13  expect=conflict got=conflict | History per patient: car accidents in 2019 and 2022, pain 5/30. | design/residual: pain score 5/30 reads 2030 (false conflict, safe direction)
MISS T14  expect=conflict got=info     | History per patient: car accidents in 2019 and 2022. Also one on 1/3/26. | second sentence, two-digit (same class as r6 Q28 four-digit)
ok   T15  expect=info     got=info     | History per patient: car accidents in 2019 and 2022. Also one on 01/03/2026. | r6 Q28 residual, four-digit, second sentence (unchanged)
ok   T16  expect=conflict got=conflict | History per patient: accidents, this one on 1/3/26. | referent word plus two-digit date
ok   T17  expect=info     got=info     | History per patient: car accidents in 2019 and 2022, one in 2015 and one on 1/3/15. | all before the stated year
total=17 mismatches=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:49.445Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; cd \"$D\" && cat > \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/probe_r8_sentence_scope.py\" <<'EOF'\nimport os, sys\nARCHIVE = os.path.abspath(sys.argv[1]); sys.path.insert(0, ARCHIVE); os.chdir(ARCHIVE)\nfrom app.backend import conflicts as C\ndef classify(ex):\n    r = [dict(n=1, date_iso=\"2026-01-02\", source=\"PCP\", excerpt=ex, kind=\"encounter\"),\n         dict(n=2, date_iso=\"2026-01-12\", source=\"PT\", excerpt=\"Exam: ok.\", kind=\"encounter\"),\n         dict(n=3, date_iso=\"2026-01-20\", source=\"Intake\", excerpt=\"Date of accident per intake form: 2026-01-03.\", kind=\"encounter\")]\n    if C.accident_date_conflicts(r): return \"conflict\"\n    return \"info\" if C.accident_date_note(r) else \"none\"\nfor ex in [\"Also one on 1/3/26.\", \"Accident on 1/3/26.\", \"Accident on 01/03/2026.\",\n           \"History: MVC on 1/3/26.\", \"History per patient: car accidents in 2019 and 2022. Accident on 1/3/26.\"]:\n    print(f\"{classify(ex):<9} | {ex}\")\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-141-r8/probe_r8_sentence_scope.py \"$D\" 2>&1 | tee artifacts/review-evidence/T-141-r8/probe_r8_sentence_scope_head_99438fb.txt; echo \"--- prior probe note on Q28\"; grep -rn \"Also one on\" artifacts/review-evidence/T-141-r6 2>/dev/null | head -3",
 "description": "Probe sentence-scope controls for the second-sentence date"
}
````

### User / tool · 2026-11-02T15:29:49.667Z

**tool result**
````
info      | Also one on 1/3/26.
conflict  | Accident on 1/3/26.
conflict  | Accident on 01/03/2026.
conflict  | History: MVC on 1/3/26.
conflict  | History per patient: car accidents in 2019 and 2022. Accident on 1/3/26.
--- prior probe note on Q28
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:55.567Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/mutant_two_digit_off.py",
 "content": "\"\"\"Reviewer mutant (T-141 r8): in a fresh copy of the HEAD archive, disable the r7 two-digit-year clause of _plural_list_ok\n(the final return) and run the r7 pins and the r6 probes. No product file is touched outside the copy.\nUsage: .venv/bin/python -I mutant_two_digit_off.py <archive_dir> <new_copy_dir>   (new_copy_dir must not exist)\"\"\"\nimport os\nimport shutil\nimport subprocess\nimport sys\n\nSRC = os.path.abspath(sys.argv[1])\nDST = os.path.abspath(sys.argv[2])\nif os.path.exists(DST):\n    raise SystemExit(\"copy dir exists; pick a new one\")\nshutil.copytree(SRC, DST)\npath = os.path.join(DST, \"app\", \"backend\", \"conflicts.py\")\nsrc = open(path, encoding=\"utf-8\").read()\nold = \"    return not any(2000 + int(next(g for g in m if g)) >= int(iso[:4]) for m in _TWO_DIGIT_YEARS.findall(unit))\"\nassert src.count(old) == 1, \"mutation anchor not found exactly once\"\nopen(path, \"w\", encoding=\"utf-8\").write(src.replace(old, \"    return True  # MUTANT: two-digit clause off\"))\nprint(\"mutated\", path)\npy = os.path.join(os.environ.get(\"VENV_PY\", \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"))\ncmd = [py, \"-I\", \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\",\n       \"tests/unit/test_t141_r7_two_digit_year.py\", \"tests/unit/test_t141_r6_probes.py\", \"tests/unit/test_t141_d061_closed_exemption.py\"]\nr = subprocess.run(cmd, cwd=DST, capture_output=True, text=True)\nprint(r.stdout[-4000:])\nprint(\"exit\", r.returncode)\n"
}
````

### User / tool · 2026-11-02T15:29:55.681Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/mutant_two_digit_off.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:29:58.613Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; D=\"$SP/T141r8_head_99438fb\"; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-141-r8/mutant_two_digit_off.py \"$D\" \"$SP/T141r8_mutant_two_digit_off\" 2>&1 | tee artifacts/review-evidence/T-141-r8/mutant_two_digit_off_result.txt | grep -E \"mutated|FAILED|passed|failed|exit\" | head -60",
 "description": "Run two-digit clause mutant in a fresh copy and capture results"
}
````

### User / tool · 2026-11-02T15:30:00.512Z

**tool result**
````
mutated /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_mutant_two_digit_off/app/backend/conflicts.py
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1/3/26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 01/03/26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1-3-26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 03-01-26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 3/1/26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 01.03.26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on Jan 3, 26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 3rd Jan 26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict[one on 1/26.]
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_reviewer_blocker_case_q19
10 failed, 219 passed in 0.25s
exit 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:04.621Z

**tool call — Bash**
````
{
 "command": "for s in ba21b4b 78b6a33 99438fb; do echo -n \"$s lib11 blob: \"; git ls-tree $s -- evals/library/case_lib11_priors_and_ledger.txt | awk '{print $3}'; done; echo \"--- lib11 file diff ba21b4b..HEAD (empty = unchanged):\"; git diff --stat ba21b4b 99438fb -- evals/library/case_lib11_priors_and_ledger.txt evals/library/case_lib11_priors_and_ledger.* ; echo \"(end)\"; echo \"--- full stat ba21b4b..HEAD:\"; git diff --stat ba21b4b 99438fb | tail -8; echo \"--- lib11 blob at ba21b4b vs HEAD: \"; git ls-tree -r 99438fb -- evals/library | grep lib11 ; echo \"--- check evidence paths\"; git ls-tree -r ba21b4b -- evals/library | grep lib11",
 "description": "Confirm lib11 case blobs unchanged between prior review and HEAD"
}
````

### User / tool · 2026-11-02T15:30:05.035Z

**tool result**
````
ba21b4b lib11 blob: 0af8fb29950a38383b5e55b1dc082cacb098d49d
78b6a33 lib11 blob: 0af8fb29950a38383b5e55b1dc082cacb098d49d
99438fb lib11 blob: 0af8fb29950a38383b5e55b1dc082cacb098d49d
--- lib11 file diff ba21b4b..HEAD (empty = unchanged):
 evals/library/case_lib11_priors_and_ledger.expected.json | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
(end)
--- full stat ba21b4b..HEAD:
 tests/unit/test_t139_letter_eval.py                |   2 +-
 tests/unit/test_t139_r3.py                         |   6 +-
 tests/unit/test_t141_r7_two_digit_year.py          |  42 ++++
 .../unit/test_t146_r2_failed_rerun_keeps_items.py  |   4 +-
 .../test_t146_r3_decided_items_never_lowered.py    |   2 +-
 tests/unit/test_t161_first_run_stage_down.py       |  76 ++++++-
 tools/check_index_imports.py                       |  10 +-
 72 files changed, 943 insertions(+), 153 deletions(-)
--- lib11 blob at ba21b4b vs HEAD: 
100644 blob f6ccafa1c5a4f1bacf888f3a0fcd01faf3f26676	evals/library/case_lib11_priors_and_ledger.expected.json
100644 blob 0af8fb29950a38383b5e55b1dc082cacb098d49d	evals/library/case_lib11_priors_and_ledger.txt
--- check evidence paths
100644 blob 63802b6be8b40d141907b32cf0317b8964e28811	evals/library/case_lib11_priors_and_ledger.expected.json
100644 blob 0af8fb29950a38383b5e55b1dc082cacb098d49d	evals/library/case_lib11_priors_and_ledger.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:07.651Z

**tool call — Bash**
````
{
 "command": "git log --oneline ba21b4b..99438fb -- evals/library/case_lib11_priors_and_ledger.expected.json; echo \"--- diff\"; git diff ba21b4b 99438fb -- evals/library/case_lib11_priors_and_ledger.expected.json; echo \"--- lib11 txt log since ba21b4b\"; git log --oneline ba21b4b..99438fb -- evals/library/case_lib11_priors_and_ledger.txt; echo \"(end)\"",
 "description": "Inspect the lib11 expected.json change between prior review and HEAD"
}
````

### User / tool · 2026-11-02T15:30:07.836Z

**tool result**
````
2ac96cf fix(backend): T-140 D-062 total line 'Billed charges accepted from these records', charge sources by billing header, per-figure rule, CPT/HCPCS normalization
--- diff
diff --git a/evals/library/case_lib11_priors_and_ledger.expected.json b/evals/library/case_lib11_priors_and_ledger.expected.json
index 63802b6..f6ccafa 100644
--- a/evals/library/case_lib11_priors_and_ledger.expected.json
+++ b/evals/library/case_lib11_priors_and_ledger.expected.json
@@ -432,7 +432,7 @@
         "total_computed": false
       }
     ],
-    "letter_line": "Billed charges stated in these records: $6,000.00",
+    "letter_line": "Billed charges accepted from these records: $6,000.00",
     "ui_line": "Accepted charges: $6,000.00",
     "notes_lines": [
       "$2,740.00: Ledger total repeats the three ledger lines above; counting it double counts; needs review",
@@ -682,7 +682,7 @@
       ],
       "good_examples": [
         "Ledger lists total charges $2,740.00, payment $300.00, a courtesy discount and a balance due; none netted.",
-        "Billed charges stated in these records: $6,000.00.",
+        "Billed charges accepted from these records: $6,000.00.",
         "Account held under letter of protection."
       ]
     },
--- lib11 txt log since ba21b4b
(end)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:21.997Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; grep -n \"_TWO_DIGIT_YEARS\\|return not any(2000\\|def _plural_list_ok\\|_CLAUSE_SPLIT = \\|def _describes_event\" \"$D/app/backend/conflicts.py\"; grep -n \"def test_\" \"$D/tests/unit/test_t141_r7_two_digit_year.py\"; grep -n \"ON_OR_AFTER = \\|BEFORE = \" \"$D/tests/unit/test_t141_r7_two_digit_year.py\"; ls -la /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r8.md 2>&1; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I -c \"print(open('reviews/T-141-staff-engineer-r7.md').read()[:0])\" ; python3 tools/board.py show T-164 2>&1 | head -5",
 "description": "Get exact line citations and check the r8 review file does not exist"
}
````

### User / tool · 2026-11-02T15:30:22.239Z

**tool result**
````
33:_CLAUSE_SPLIT = re.compile(r"[;,]|\s[-\u2013\u2014]\s|\s\(|\)")
61:_TWO_DIGIT_YEARS = re.compile(                                                        # a two-digit year in a date shape; the year is the one group that matched
69:def _plural_list_ok(unit: str, iso) -> bool:
80:    return not any(2000 + int(next(g for g in m if g)) >= int(iso[:4]) for m in _TWO_DIGIT_YEARS.findall(unit))     # T-141 r7 (F1): '1/3/26' reads as 2026
83:def _describes_event(rec: dict, iso=None) -> bool:
28:def test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict(tail):
33:def test_dates_before_the_accident_year_stay_history(tail):
37:def test_reviewer_blocker_case_q19():
41:def test_blood_pressure_is_not_a_date():
20:ON_OR_AFTER = [   # the reviewer's Q19 and its date-form class, plus 4-digit variants
24:BEFORE = ["one in 2015.", "one on 1/3/15.", "one on 01-03-15.", "one on 1/3/25.", "one on Jan 3, 25.", "one on 3rd Jan 25.", "one on 12/25.", "one on 1/3/2015."]
ls: /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r8.md: No such file or directory

---
id: "T-164"
title: "tests/e2e/test_conflict_skipped.py 8/9 red at HEAD (T-151 tests vs current checks payload after T-141 r3+); triage: stale test vs real UI/API regression"
milestone: "M2"
role: "qa"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:26.586Z

**tool call — Bash**
````
{
 "command": "D=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r8_head_99438fb\"; grep -n \"stripped_spans\\|plural_ok = _plural_list_ok\" \"$D/app/backend/conflicts.py\"; sed -n '20,24p' \"$D/tests/unit/test_t141_r7_two_digit_year.py\" | cut -c1-80; grep -n \"2ac96cf\\|T-140\" /Users/arsis/zlayt-pm-project/memory/DECISIONS.md 2>/dev/null | head -2; sed -n '1,12p' /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-120 >/dev/null; echo ok",
 "description": "Confirm sentence-scope line numbers for citations"
}
````

### User / tool · 2026-11-02T15:30:26.764Z

**tool result**
````
87:    for a, b in sentences.stripped_spans(text):
89:        plural_ok = _plural_list_ok(unit, iso)
ON_OR_AFTER = [   # the reviewer's Q19 and its date-form class, plus 4-digit var
    "one on 1/3/26.", "one on 01/03/26.", "one on 1-3-26.", "one on 03-01-26.", 
    "one on 1/26.", "one on 3/27/26.", "one on 1/3/2026.", "one on 01/03/2026.",
]
BEFORE = ["one in 2015.", "one on 1/3/15.", "one on 01-03-15.", "one on 1/3/25."
ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:59.581Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r8.md",
 "content": "# T-141 staff-engineer scoped check, round 8 (fix 78b6a33, HEAD 99438fb)\n\nVerdict: **pass** (0 blockers, 0 majors, 1 minor, 1 nit).\n\nScope: only the three items named after r7 (the two-digit-year plural-list date guard), plus lib11 unchanged and the conflict suites. Verified on a `git archive 99438fb` copy. The brief names commit 78b6a33 as the card commit. HEAD has moved one commit past it (99438fb, T-161 r2, touches `app/backend/pipeline.py` and T-146/T-161 tests only). `app/backend/conflicts.py` has the same blob (7fffd0b) at 78b6a33 and at HEAD, so the code reviewed is the 78b6a33 code. The e2e red in `tests/e2e/test_conflict_skipped.py` is owned by T-164 and is not counted here.\n\nResults by item:\n1. Two-digit-year dates on or after the stated accident date inside a labelled plural history list raise a conflict: PASS. The 25 pins in `tests/unit/test_t141_r7_two_digit_year.py` pass. My 17-row boundary probe matches on 16 rows. The one miss (T14) is a date in a second sentence, which is outside the rule as written (minor, see F1). Before-year two-digit dates stay info (T7, T8, T17). A mutant that disables the two-digit clause (`conflicts.py:80`) turns 10 pins red.\n2. The r7 blocker case is fixed: PASS. `'History per patient: car accidents in 2019 and 2022, one on 1/3/26.'` (stated 2026-01-03) now reads conflict. The r7 probe rerun gives 54 rows, 0 mismatches (Q19 ok).\n3. lib11 is unchanged: PASS for the case input. `evals/library/case_lib11_priors_and_ledger.txt` is blob 0af8fb2 at ba21b4b, 78b6a33 and 99438fb, and its diff is empty. Note: the sibling `.expected.json` changed in 2ac96cf (T-140, D-062 letter wording, two lines). That is not a T-141 change, so it is not counted against this card.\n4. Conflict unit suites: PASS. 579 passed across 10 modules (the 9 from r7 plus the new r7 file). 554 at r7 plus the 25 new pins.\n\nFindings\n\n- **minor, F1 (item 1 boundary):** a labelled plural list followed by a second sentence that names a two-digit date on or after the stated accident date stays info. `History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.` prints info (probe_r8 T14). The four-digit form does the same (T15, the r6 Q28 row). The cause is sentence scope, not the plural exemption: the unit is one sentence (`conflicts.py:87-89`), and `Also one on 1/3/26.` alone has no accident word, so it is info with or without the exemption (`probe_r8_sentence_scope_head_99438fb.txt`: info; `Accident on 1/3/26.` conflict). The written rule is sentence-scoped (\"the whole sentence\", D-061 / r6 F3), so this is not a violation of the rule as written and I do not rate it a blocker. It is the same loss-of-fact shape the r7 blocker described, and scope cut 13f does not name it. Fix: decide and record it in D-061 (either keep info and say so, or treat a date-only sentence that follows a labelled plural list as a conflict). Acceptance: a pin for T14 that matches the recorded decision.\n\n- **nit, F2 (false conflicts, safe direction):** the two-digit reading is `20xx` for every two-digit year and any slash pair with month 1-12 is read as month/year. `History per patient: car accidents in 2019 and 2022, one on 1/3/99.` reads conflict (probe_r8 T10, 1999 becomes 2099). `... pain 5/30.` reads conflict (T13, 2030). Both are false conflicts that D-055 accepts, so they are not blockers. Fix: record them in 13f or add pins. Acceptance: pins for T10 and T13 with the chosen outcome.\n\nResiduals not counted: none of the r7 F1 forms ('1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26') remain open at HEAD.\n\nExercised\n1. Read personas/staff-engineer.md in full; reviews/T-141-staff-engineer-r7.md; memory/SCOPE_CUTS.md line 91 (13f); my r7 memory note.\n2. `git rev-parse HEAD` gives 99438fb. `git log --oneline 78b6a33..HEAD` gives one commit (99438fb). `git show 78b6a33 -- app/backend/conflicts.py` read: the new `_TWO_DIGIT_YEARS` regex (conflicts.py:61-66) and the new return clause (conflicts.py:80).\n3. `git archive 99438fb | tar -x` into the scratchpad copy `T141r8_head_99438fb`. sha256 of `app/backend/conflicts.py` (a66f164e...) equals `git show 99438fb:app/backend/conflicts.py`.\n4. Conflict unit suites on the archive, 10 modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t141_r3_variants, test_t116_r4_all_dated_records, test_api_routes, test_t141_d061_closed_exemption, test_t141_r6_probes, test_t141_r7_two_digit_year): `579 passed in 9.15s`. Log: artifacts/review-evidence/T-141-r8/pytest_conflict_suites_head_99438fb.txt.\n5. `pytest -v tests/unit/test_t141_r7_two_digit_year.py` on the archive: 25 passed, including test_reviewer_blocker_case_q19. Log: artifacts/review-evidence/T-141-r8/pytest_r7_two_digit_year_head.txt.\n6. probe_r7.py (copy of the r7 probe) on the archive: `total=54 mismatches=0`; Q19 ok. Log: artifacts/review-evidence/T-141-r8/probe_r7_head_99438fb.txt.\n7. probe_r8.py (17 item-1 boundary rows through accident_date_conflicts / accident_date_note, stated 2026-01-03): 16 match, 1 miss (T14, second sentence). Log: artifacts/review-evidence/T-141-r8/probe_r8_head_99438fb.txt.\n8. probe_r8_sentence_scope.py: `Also one on 1/3/26.` info; `Accident on 1/3/26.` conflict; `History: MVC on 1/3/26.` conflict. Log: artifacts/review-evidence/T-141-r8/probe_r8_sentence_scope_head_99438fb.txt.\n9. mutant_two_digit_off.py in a fresh copy (`T141r8_mutant_two_digit_off`; the archive is untouched): the conflicts.py:80 return replaced by `return True`. `10 failed, 219 passed`: 9 two-digit ON_OR_AFTER pins and test_reviewer_blocker_case_q19; the four-digit pins still pass. Log: artifacts/review-evidence/T-141-r8/mutant_two_digit_off_result.txt.\n10. lib11: `git ls-tree` blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at ba21b4b, 78b6a33 and 99438fb. `git diff --stat ba21b4b 99438fb -- evals/library/case_lib11_priors_and_ledger.txt` is empty. `git log --oneline ba21b4b..99438fb -- evals/library/case_lib11_priors_and_ledger.expected.json` gives 2ac96cf (T-140 D-062 wording, two lines in letter_line and good_examples).\n11. `python3 tools/board.py show T-164`: T-164 exists (qa, M2) and owns the test_conflict_skipped.py red. That file was not run or counted.\n\nNot run: tests/e2e/test_conflict_skipped.py (T-164), full unit suite, pipeline CLI on sample.txt, eval runner, no server on :7860.\n\n```json\n{\"card\": \"T-141\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git HEAD 99438fb (card fix 78b6a33 is an ancestor; 99438fb touches pipeline.py and T-146/T-161 tests only). app/backend/conflicts.py (blob 7fffd0b at 78b6a33 and HEAD), tests/unit/test_t141_r7_two_digit_year.py. Archive copy: scratchpad T141r8_head_99438fb. Evidence: artifacts/review-evidence/T-141-r8/. Sample case: evals/library/case_lib11_priors_and_ledger.txt (input). No app URL: unit-level checks only, nothing on :7860.\",\n \"exercised\": [\n  \"Read personas/staff-engineer.md; reviews/T-141-staff-engineer-r7.md; memory/SCOPE_CUTS.md 13f (line 91).\",\n  \"git rev-parse HEAD (99438fb); git log --oneline 78b6a33..HEAD (one commit); git show 78b6a33 -- app/backend/conflicts.py.\",\n  \"git archive 99438fb into scratchpad T141r8_head_99438fb; sha256 of conflicts.py equals git show 99438fb:app/backend/conflicts.py.\",\n  \"Conflict unit suites on the archive, 10 modules incl. test_t141_r7_two_digit_year.py: 579 passed (pytest_conflict_suites_head_99438fb.txt).\",\n  \"pytest -v tests/unit/test_t141_r7_two_digit_year.py on the archive: 25 passed incl. test_reviewer_blocker_case_q19 (pytest_r7_two_digit_year_head.txt).\",\n  \"probe_r7.py rerun on the archive: total=54 mismatches=0; Q19 ok (probe_r7_head_99438fb.txt).\",\n  \"probe_r8.py: 17 item-1 boundary rows through accident_date_conflicts/accident_date_note, stated 2026-01-03: 16 match, 1 miss T14 second-sentence (probe_r8_head_99438fb.txt).\",\n  \"probe_r8_sentence_scope.py: 'Also one on 1/3/26.' info; 'Accident on 1/3/26.' conflict (probe_r8_sentence_scope_head_99438fb.txt).\",\n  \"mutant_two_digit_off.py in a fresh copy: conflicts.py:80 return replaced by return True; 10 failed, 219 passed (mutant_two_digit_off_result.txt).\",\n  \"git ls-tree blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at ba21b4b, 78b6a33, 99438fb; git diff --stat ba21b4b 99438fb on the .txt is empty; .expected.json changed in 2ac96cf (T-140), noted, not counted.\",\n  \"python3 tools/board.py show T-164: owns the test_conflict_skipped.py red; that file not run or counted.\",\n  \"Not run: tests/e2e/test_conflict_skipped.py, full unit suite, pipeline CLI, eval runner, server on :7860.\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"item1_two_digit_on_or_after_conflict\": 4, \"r7_blocker_case_fixed\": 5, \"lib11_case_input_unchanged\": 5, \"conflict_unit_suites\": 5, \"new_clause_pinned_by_mutant\": 5, \"sentence_scope_consistency\": 3},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"F1: a two-digit date on or after the accident in a second sentence, after a labelled plural list, stays info\",\n   \"evidence\": \"probe_r8_head_99438fb.txt row T14: 'MISS T14 expect=conflict got=info | History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.'; T15 (four-digit form) info, same shape. conflicts.py:87-89 scopes the plural exemption to one sentence. probe_r8_sentence_scope_head_99438fb.txt: 'info | Also one on 1/3/26.' (no accident word in that sentence); 'conflict | Accident on 1/3/26.'\",\n   \"why_it_matters\": \"Same loss-of-fact shape as the r7 blocker, but the written rule (D-061, r6 F3 'the whole sentence') is sentence-scoped and the date sits in a sentence with no accident word, so it is not a violation of the rule as written. Scope cut 13f does not name it. I would have decided this differently; it is not counted as a blocker.\",\n   \"fix\": \"Decide the rule and record it in memory/ORCHESTRATOR_DECISIONS.md D-061: either a date-only sentence that follows a labelled plural list stays info (state that in the rule), or it is a conflict when it names a date on or after the stated accident date.\",\n   \"acceptance_test\": \"A pin for 'History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.' that matches the recorded decision, for two-digit and four-digit forms.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"F2: safe-direction false conflicts from two-digit readings (1/3/99 reads 2099; pain 5/30 reads 2030)\",\n   \"evidence\": \"probe_r8_head_99438fb.txt row T10: conflict for 'History per patient: car accidents in 2019 and 2022, one on 1/3/99.'; row T13: conflict for '... pain 5/30.'. conflicts.py:80 reads every two-digit year as 20xx; _TWO_DIGIT_YEARS (conflicts.py:61-66) matches any month/day or month/year pair.\",\n   \"why_it_matters\": \"A false conflict is the safe direction under D-055, so this is not a blocker. A paralegal will see extra conflict flags on 1999 dates and on pain scores.\",\n   \"fix\": \"Record T10 and T13 in scope cut 13f or add pins that name the outcome; narrow the score case only if the team wants fewer false flags.\",\n   \"acceptance_test\": \"Pins for '1/3/99' and 'pain 5/30' in tests/unit/test_t141_r7_two_digit_year.py with the chosen outcome, and a 13f row if they stay.\"}\n ],\n \"whats_right\": [\n  \"The new two-digit clause is pinned: disabling it turns 9 two-digit ON_OR_AFTER pins and the r7 blocker test red (mutant_two_digit_off_result.txt).\",\n  \"Before-year two-digit controls hold (T7 '12/31/25', T8 'Jan 3, 25', T17 all-before list) and the score and BP controls stay info (T11, T12).\",\n  \"The conflict unit suites pass 579 of 579 across 10 modules, and the r7 probe rerun gives 54 of 54.\"\n ],\n \"questions_for_chris\": [\n  \"Should a date in a following sentence after a labelled plural history list stay info, as the sentence-scoped rule does for four-digit dates today (T14, T15)? I did not count it as a blocker because the written rule is sentence-scoped.\",\n  \"Is the 2ac96cf change to lib11's .expected.json letter wording (T-140, D-062) inside what 'lib11 is unchanged' means for this card? I read it as outside T-141; the input .txt is byte-identical.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T15:30:59.763Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r8.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:02.280Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; echo \"--- json parse\"; .venv/bin/python -I -c \"\nimport re,json\nt=open('reviews/T-141-staff-engineer-r8.md',encoding='utf-8').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`',t,re.S)\nprint('json blocks:',len(blocks))\nd=json.loads(blocks[0])\nsev=[f['severity'] for f in d['findings']]\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('card',d['card'],'model',d['model'],'verdict',d['verdict'],'rule_expects',exp,'match',d['verdict']==exp)\nprint('exercised',len(d['exercised']),'findings',sev)\n\"",
 "description": "Validate board and check the review JSON parses and matches the verdict rule"
}
````

### User / tool · 2026-11-02T15:31:02.360Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:03.925Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Run read-only board validation"
}
````

### User / tool · 2026-11-02T15:31:04.082Z

**tool result**
````
ok (164 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:05.601Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/check_review_json_r8.py",
 "content": "\"\"\"Reviewer check (T-141 r8): extract the single json block from reviews/T-141-staff-engineer-r8.md, parse it, and compare the verdict\nwith the CONTRACT verdict rule (any blocker -> fail, else any major -> changes, else pass). Usage: .venv/bin/python -I check_review_json_r8.py\"\"\"\nimport json\nimport re\n\nPATH = \"/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r8.md\"\ntext = open(PATH, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card:\", d[\"card\"], \"| persona:\", d[\"persona\"], \"| model:\", d[\"model\"])\nprint(\"verdict:\", d[\"verdict\"], \"| rule expects:\", expected, \"| match:\", d[\"verdict\"] == expected)\nprint(\"findings by severity:\", sev, \"| exercised items:\", len(d[\"exercised\"]))\n"
}
````

### User / tool · 2026-11-02T15:31:05.705Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141-r8/check_review_json_r8.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:06.969Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-141-r8/check_review_json_r8.py 2>&1 | tee artifacts/review-evidence/T-141-r8/check_review_json_r8_result.txt",
 "description": "Parse the review JSON block and check the verdict rule"
}
````

### User / tool · 2026-11-02T15:31:07.081Z

**tool result**
````
json blocks: 1
card: T-141 | persona: staff-engineer-reviewer | model: claude-haiku-5-5
verdict: pass | rule expects: pass | match: True
findings by severity: ['minor', 'nit'] | exercised items: 12
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:15.198Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r8_patterns.md",
 "content": "---\nname: project_t141_r8_patterns\ndescription: T-141 r8 (fix 78b6a33, HEAD 99438fb, scoped check): two-digit-year plural-list guard passes; HEAD moved one commit past the card; lib11 expected.json changed by a sibling card; sentence-scope residual\nmetadata:\n  type: project\n---\n\nT-141 r8 (verdict pass: 0 blocker, 0 major, 1 minor, 1 nit). Review: reviews/T-141-staff-engineer-r8.md. Evidence: artifacts/review-evidence/T-141-r8/.\n\n- The r7 blocker (two-digit-year dates in a labelled plural list) is fixed at conflicts.py:61-66 and :80. Disabling the :80 clause turns 10 pins red (9 two-digit rows + the r7 blocker test). Four-digit pins stay green on the mutant, so the two forms are pinned separately.\n- HEAD moved past the card commit (78b6a33 to 99438fb, a T-161 commit touching pipeline.py and T-146/T-161 tests). The brief named the card commit. Check `git log --oneline <card>..HEAD` and compare the blob of the file in scope before saying \"code identical\".\n- \"lib11 unchanged\" can hide a sibling change: the .txt input is blob 0af8fb2 across all three shas, but `evals/library/case_lib11_priors_and_ledger.expected.json` changed in 2ac96cf (T-140, D-062 letter wording). Name the file in the check, not just the case.\n- The plural exemption is per sentence (`sentences.stripped_spans`, conflicts.py:87-89). A date in a following sentence with no accident word stays info for two-digit and four-digit forms. Separate the two causes with a control: `'Accident on 1/3/26.'` conflicts, `'Also one on 1/3/26.'` does not, so the second sentence has no event word.\n- Two-digit regex false conflicts: `pain 5/30` reads 2030 (month/year alternative), `1/3/99` reads 2099. Safe direction under D-055; nit.\n- The git-guard hook denies a Bash `python3 -c` with backticks or escaped characters (\"could not parse command safely\"). Write the JSON check to artifacts/review-evidence/<card>-r<n>/ and run it with `-I`. Same as r7.\n\n**Why:** the card names one commit, but HEAD moves while reviewers work. A green run on HEAD does not prove the named commit's behaviour without the blob check.\n\n**How to apply:**\n- Before a scoped check, run `git log --oneline <card>..HEAD -- <files in scope>` and report the blobs. Name every file the \"unchanged\" claim covers, including `.expected.json` beside the `.txt`.\n- When a new clause depends on sentence scope, add one control with the event word to show the scope is the cause, not the exemption.\n- Keep the mutant in a fresh copy (shutil.copytree into a new path) and report the red count with names.\n\nRelated: [[project_t141_r7_patterns]], [[project_t141_r6_patterns]], [[feedback_evidence_sha_vs_commit]], [[feedback_differential_probe_prior_build]].\n"
}
````

### User / tool · 2026-11-02T15:31:15.288Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r8_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:15.492Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T15:31:15.507Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E; T-124 d56328a pass: one-way and substring id check
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1-r2 (fail) and r4 3223e50 (changes): H3V5 label contradicts judge rule 1, reachability mutants red, relabel second-agent test
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263, r2 8bc7f90, r3 db08276 (all fail): bare figures vanish in prose/CMS/balance-forward, second balance-forward overwrites, counter blind to bare numbers, mutant label checks
24	- [T-083 r4 accounting patterns](project_t083_r4_accounting_patterns.md) — r4 6bca71e (fail): repeated statement totals overwritten while counted as placed, skipped billing records leave complete true, stray bare-number definition gap
25	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
26	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
27	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
28	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
29	- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved past card
30	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted; T-099 3ecb8b1 changes (state-sum untested); T-099 r2 f345bc8 pass: case_count clause untested, F2 debt needs SCOPE_CUTS row
31	- [T-083 r5 cross-family patterns](project_t083_r5_cross_family_patterns.md) — r5 690a0e3 fail: ledger+CMS totals share a [-1] slot, bare charge beyond TOL=8 dropped, complete ignores reconciliation checks
32	- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — r1 4c5f9bf changes; r2 fdc2506 pass: guard tested for golden only, recheck test passes via backstop, latest.json blocks run-then-write
33	- [T-098 r2 patterns](project_t098_r2_review_patterns.md) — dd84122 fail: summary-only edit bypasses accept guard, gate recomputes 2 of 5 checks, notes print AI wording
34	- [T-103 listing patterns](project_t103_listing_review_patterns.md) — r1 fail; r2b fail; r3 changes; r4 8a2b934 changes: UB-04 room total vs other_figures, offset comparisons open on Q1, redundant holder branches
35	- [Exact count vs presence](feedback_exact_count_vs_presence.md) — presence oracles miss a dropped second copy; run the test module's random generator with exact per-record counts
36	- [T-100 r2 patterns](project_t100_r2_patterns.md) — r2 288c1d3 changes: shared new_tokens, vocabulary narrower than _EN_* lists, fixture eval diff method, Spanish branches unpinned
37	- [T-098 r3 patterns](project_t098_r3_review_patterns.md) — 1335f21 pass: choke point verified by grep+probe; unchecked removed narrative text still printed; 4 unrelated unit failures
38	- [T-106 patterns](project_t106_review_patterns.md) — c2a5d1f changes: pdf_hidden regex bypass via from-subprocess-import, notes-only fix leaves narrative panel printing, loose fixture filter
39	- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — r1 d3e127c changes; r2 a271014 pass: masked route checks, sentences_reason unrendered, store.py broad except, clone for .git count
40	- [Shared scratchpad](feedback_shared_scratchpad.md) — scratchpad is shared with other agents: unique card-round subdirs, diff -rq archive checks, no backgrounded setup chains
41	- [T-109 doc-vs-code patterns](project_t109_doc_vs_code_patterns.md) — r1 changes; r2 4bdf366 fail (model conflicts dropped); r3 changes; r4 425095f pass: cite range off by blank lines, scan a-side keys, fix-up scope
42	- [T-106 r2 audit patterns](project_t106_r2_audit_patterns.md) — r2 e3a62fa changes: AST audit misses os alias/ctypes/asyncio, ps argv tail unpinned, rest-of-app still regex
43	- [T-102 stale-calibration patterns](project_t102_stale_calibration_patterns.md) — r1 276991b fail; r2 03206ca changes: stale fix verified via clone (archive can't discriminate), T-096 owner still missing, wrong-dir guard is a literal pin
44	- [T-115 e2e/curated patterns](project_t115_e2e_curated_patterns.md) — r1 400a8c0 changes: evidence cites older commit than HEAD, regen re-keys prompts with scripted answers, ZLAYT_DB skips, inner_text race
45	- [T-112 trim patterns](project_t112_trim_patterns.md) — r1 afcde06, r2 1b93582 changes: stems then abbreviations over-trim, doc/D-054 on old rule, unpinned counter
46	- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes; r2 changes (p gate); r3 c559ce2 pass: vis() first-frame poll, count artifact without sha
47	- [Verify PID before kill](feedback_verify_pid_before_kill.md) — $! can be a wrapper; check ps and lsof listener before killing own servers
48	- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — HEAD 433ac1c: negative-proxy guard, one-direction single-source refactor, write-once errata in my r2 files
49	- [T-128/T-129/T-127 patterns](project_t128_t129_t127_patterns.md) — r1 93de5f2: closed-list fragment guard, preamble flag never served by API, T-127 pass with unpinned from/to
50	- [T-120 r3 patterns](project_t120_r3_patterns.md) — f7829c1 pass: strip-then-scan verified, MS honorific collision, unpinned gate mutant, count errata in r3 file
51	- [T-128/T-129 r2 patterns](project_t128_t129_r2_patterns.md) — T-128 r2 changes: structural rule leaves dependent tail clauses, deny gap; T-129 r2 pass: tests flag-only, relative sweep path false-kills
52	- [T-133 lexicon patterns](project_t133_lexicon_review_patterns.md) — r1 e79c3aa/1218b2e changes: bare 'History:' HPI over-flag, attribution deny untested, ';' truncates excerpt, deny has no source
53	- [T-113/T-122 patterns](project_t113_t122_patterns.md) — 5dfba88: held-out control written with the prompt naming its noun, closed-list word mutants, vacuous order test; T-122 regression created by T-113 commit
54	- [T-132 r2 / T-128 r3 patterns](project_t132_t128_r2r3_patterns.md) — both changes: wrap inside chained clause, 2-letter header labels, participle before removed with-tail, prefix-oracle fuzz with old-code control
55	- [T-133 r3 patterns](project_t133_r3_patterns.md) — 4065ef2 changes: r2 header guard dropped Past/Medical/Surgical history flags, ';' suppression recall gap, live eval owed
56	- [T-133 r4 patterns](project_t133_r4_patterns.md) — 128942d changes (final): \s matches newline so line-start bare History: flags, parity tests blind to gains, 13d "before T-133" premise false
57	- [T-133 r5 patterns](project_t133_r5_patterns.md) — 15be212 pass: prior-ending x separator grid, CR-only kills \s but CRLF/blank cannot, eval grep must read header line, 13d PMH overstated
58	- [Regex multiline probe](feedback_regex_multiline_probe.md) — probe \s and line-break variants of "line start" guards; \s matches newline under re.M on raw text
59	- [Differential probe vs prior build](feedback_differential_probe_prior_build.md) — run the probe set on pre-fix and HEAD archives; FLAG-to-quiet flips reveal regressions the acceptance list misses
60	- [T-134 unconfirmed-edit patterns](project_t134_unconfirmed_edit_patterns.md) — r1 5fb338d changes; r2 db1d8d5 changes: judge_report human_overrides counts open edit, N3/N5 mutants survive
61	- [GATE-M2 patterns](project_gate_m2_patterns.md) — 0c24f5f fail: deadline skips judge_entries so entries compose verified, timed-out rerun deletes pending, no live ship-bar report at HEAD
62	- [T-113 r2 patterns](project_t113_r2_patterns.md) — bea3984 changes: git-derived held-out audit checked with throwaway repos, count/real-data unpinned (7 of 14 mutants green), in-place edit blind spot, 13c history side only
63	- [T-132 r4 patterns](project_t132_r4_patterns.md) — fc60471 changes: 'Label:' regex drops condition lines ('Left wrist swollen:'), git archive from a subdir exports empty tree, control-vs-HEAD visibility diff, equivalence of linearised helpers
64	- [T-132 r5 patterns](project_t132_r5_patterns.md) — ed45b4a/5de16d3 pass: closed-list stop leaves ALL-CAPS condition lines dropped (minor), AC count off by one, control-first probe expectations, hook denies rm with expansion
65	- [T-134 r3 / T-138 patterns](project_t134_r3_t138_patterns.md) — both changes: text fix missed review step + gate headline, stale rejudge claim, snapshot aliases mutated dict, HEAD broken by sibling commit
66	- [T-145/T-146 patterns](project_t145_t146_patterns.md) — T-145 pass: shared JUDGE_NOT_RUN sentence mislabels real failure; T-146 changes: failed (done_with_errors) re-run wipes accepted entries, state-only snapshot
67	- [T-141 r2 patterns](project_t141_r2_patterns.md) — 68b8685 changes: clause word list still loses conflicts (prior to/no history of), stored run summary stale after confirm_date, sibling test hunk red at commit
68	- [T-134 r4 / T-138 r2 patterns](project_t134_r4_t138_r2_patterns.md) — 4f416a4 changes, b7a7ead pass: backend D-058 wording fixed but UI regex keeps old stays-blocked sentence, identical-text re-pick test, alias and leak controls
69	- [Frontend text coupling](feedback_frontend_text_coupling.md) — when a backend sentence changes, grep app/frontend for the old phrase and regexes over it (server-text swap silently falls back)
70	- [T-136 r2 patterns](project_t136_r2_patterns.md) — 07c7558 changes: private-server fallback to :7860, red e2e predating the card, flaky mobile and open_rail tests, client copy of gate rule
71	- [T-146 r2 patterns](project_t146_r2_patterns.md) — 2db6ad2 changes: keep-whole rule keyed on judge/stub only; flags-down downgrades corroborated flag, SUMMARY_NOT_IN_QUOTE overwrites
72	- [T-140 r2 patterns](project_t140_r2_patterns.md) — a0e2639 changes: tests read untracked reviewer file (clean pytest aborts), after-figure position gap, reclassify skips duplicate/total flags
73	- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed
74	- [T-141 r4 patterns](project_t141_r4_patterns.md) — 93a2ffc changes: month-year two-month cut-off hides 'Rear-ended in October 2025' while bare-year fix flipped; pinned variant contradicts r3 acceptance
75	- [T-152 golden-claim patterns](project_t152_golden_claim_patterns.md) — r1 changes: untracked ledger read at import breaks clean collection, golden-named test without golden compare, git show not working tree, HEAD moved 3x
76	- [T-146 r3 patterns](project_t146_r3_patterns.md) — bf53087 changes: equal-rank check worsening replaces decided item silently, reword fails case, rerun_note no UI consumer
77	- [T-146 r4 patterns](project_t146_r4_patterns.md) — c2913a6 pass: a2 keep-and-note and j3 gate hold; identical re-run rewrites decided rows (updated_at, call_id); dead 'conflicts' key
78	- [Fake script keys](feedback_fake_script_keys.md) — FakeCall returns {} for unknown step keys; grep the key is consumed and run a wrong-key control before trusting a step-down probe
79	- [T-141 r5 patterns](project_t141_r5_patterns.md) — 52ac285 changes: verb-only mechanism gate; noun forms, injury words and 'last year' stay info in-window; relative return precedes gate; gate mutant pinned
80	- [T-155 e2e triage patterns](project_t155_e2e_triage_patterns.md) — 20b3a42 changes (r1b): green claim on older sha, "stale" density reds were real, hidden list 0 px + 8px margin, refusal box btn_y+132
81	- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — before accepting a green run or a "stale test" triage, run the cited test at the evidence sha and at the reviewed commit; count commits between
82	- [T-157 title/next_action patterns](project_t157_case_title_next_action_patterns.md) — 926bf37 changes: blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card counts not reproduced, archive needs review-evidence overlay
83	- [T-140 r3 / T-152 r2 patterns](project_t140_r3_t152_r2_patterns.md) — 35d8280 changes: default-deny per line not per figure (second-figure leaks), undated promote unflagged, 7 surviving mutants; T-152 pass, sibling commit broke collection briefly
84	- [T-141 r6 patterns](project_t141_r6_patterns.md) — 824984f fail: closed exemption leaks across and/or/with/for/of, plural and bare hit/impact missing from _EVENT, Q15 regression
85	- [T-141 r7 patterns](project_t141_r7_patterns.md) — ba21b4b fail: two-digit-year dates escape the plural-list guard, lib11 e2e skip file red since before ff1256e, conftest SyntaxError looks like red
86	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:17.354Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && printf '%s\\n' \"- [T-141 r8 patterns](project_t141_r8_patterns.md) — 78b6a33 pass (HEAD 99438fb): HEAD moved past card, lib11 .expected.json changed by sibling card, sentence-scope residual, 10-pin mutant\" >> MEMORY.md && tail -2 MEMORY.md && ls project_t141_r8_patterns.md",
 "description": "Append the r8 memory pointer to the memory index"
}
````

### User / tool · 2026-11-02T15:31:17.485Z

**tool result**
````
- [T-141 r7 patterns](project_t141_r7_patterns.md) — ba21b4b fail: two-digit-year dates escape the plural-list guard, lib11 e2e skip file red since before ff1256e, conftest SyntaxError looks like red
- [T-141 r8 patterns](project_t141_r8_patterns.md) — 78b6a33 pass (HEAD 99438fb): HEAD moved past card, lib11 .expected.json changed by sibling card, sentence-scope residual, 10-pin mutant
project_t141_r8_patterns.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:18.863Z

Pass (0 blockers, 0 majors, 1 minor, 1 nit): the r7 two-digit-year blocker is fixed and the 579 conflict-suite tests pass on HEAD 99438fb, with a minor sentence-scope residual at `reviews/T-141-staff-engineer-r8.md`.
