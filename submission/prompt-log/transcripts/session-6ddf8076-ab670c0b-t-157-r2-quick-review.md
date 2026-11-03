# Subagent: T-157 r2 quick review (T-157 r2 quick review)

Source: `agent-ab670c0b6d64ed91d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T15:23:23.682Z

This is the round-2 review of board card T-157 (commit 852b060) in /Users/arsis/zlayt-pm-project. Read reviews/T-157-staff-engineer.md and `python3 tools/board.py show T-157`.

On a `git archive HEAD` copy:
- **Titles.** Check title validation: control characters stripped; `<`, `>` and titles over 120 characters rejected with a 422 and nothing stored; derived titles have tags dropped. Also test an HTML-entity-encoded payload and a unicode lookalike.
- **next_action.** It must order blockers first, then timeline order, and the mutants must die.
- **Live definition.** `rerun_available` and demo mode share `store.live_enabled`.
- **Quirk.** The 422-before-404 behavior on an unknown token is a minor at most.

Run tests/unit/test_case_list.py and the unit suite.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-157-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:26.786Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T15:23:26.806Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:26.987Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer.md"
}
````

### User / tool · 2026-11-02T15:23:26.996Z

**tool result**
````
1	# T-157 review: staff-engineer-reviewer (commit 926bf37)
2	
3	Verdict: **changes** (0 blockers, 3 majors, 3 minors, 2 nits). Verdict rule: no blocker, so not fail; majors present, so changes.
4	
5	Scope: commit 926bf37 (HEAD at review time). Reviewed on a `git archive 926bf37` copy in my scratchpad. Untracked `artifacts/review-evidence` (1576 files) was overlaid with no-clobber because `tests/unit` reads it. Fixture backend, in-process TestClient, no live app URL.
6	
7	What holds: the code implements the four brief items. Title create, PATCH rename and the derived default work, and the default is never "Untitled case". `rerun_available` is false in demo/fixture mode and after a no-answer rerun. `next_action` is code-only, with blockers ahead of needs-review items and a total sort key that ends in the item id. The 13 `test_case_list.py` tests pass, and the full `tests/unit` run has no failures on this copy.
8	
9	What does not hold: the brief asks for HTML validation of titles, and there is none. Two `next_action` rules (blockers first, first-in-timeline pick) have no test that fails when they break. Two mutants survive, so the tests do not prove the AC.
10	
11	Findings (detail in the JSON block):
12	1. major: titles are stored and returned with markup unchanged. Not exploitable in the shipped UI, because the frontend writes text nodes.
13	2. major: blockers-first rule is untested. Mutant `first = None` leaves all 13 tests green.
14	3. major: first-in-timeline pick is untested. Mutant `waiting[-1]` leaves all 13 tests green.
15	4. minor: the card's full-suite evidence (4387 passed, 2 failed) does not reproduce at 926bf37. My run gave 4286 passed, 8 skipped, 0 failed.
16	
17	```json
18	{"card": "T-157", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
19	 "scope": "commit 926bf37 (HEAD at review time): app/backend/api.py, case_list.py, present.py, store.py, memory/contracts/api.md, tests/unit/test_case_list.py. Reviewed on a git archive copy of 926bf37 with untracked artifacts/review-evidence overlaid (tests read it). Fixture backend, in-process TestClient, no app URL. Case under test: evals/library case_lib01_er_only_then_gap (plus a pasted-and-named case and a library-created title case).",
20	 "exercised": [
21	  "python3 tools/board.py show T-157 (card AC, handoff, rounds 0, commits 926bf37)",
22	  "cat memory/contracts/api.md; sections read: conventions line 46 (untrusted strings are plain text), POST /api/cases (line 60, title), PATCH row (line 54), GET case rerun_available (line 132), next_action (line 705), Case titles (line 703)",
23	  "git show --stat 926bf37; git show 926bf37 -- app/backend/api.py app/backend/case_list.py app/backend/present.py app/backend/store.py memory/contracts/api.md tests/unit/test_case_list.py (full diff read)",
24	  "git archive 926bf37 | tar -x into the scratchpad archive dir; overlaid artifacts/review-evidence with cp -Rn (1576 untracked files)",
25	  ".venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider on the archive: '13 passed in 8.00s'",
26	  ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider on the archive: '4286 passed, 8 skipped in 275.41s (0:04:35)', 0 failed (full output at the scratchpad full-unit.out file)",
27	  "mutant A: case_list.py:136 'w = waiting[0]' -> 'waiting[-1]'; pytest test_case_list.py: '13 passed in 6.33s' (survived)",
28	  "mutant B: case_list.py:131 'first = next(...)' -> 'first = None'; pytest test_case_list.py: '13 passed in 7.64s' (survived)",
29	  "mutant C: case_list.py:117 sort key with rank before date; pytest: '1 failed, 12 passed' (killed by test_next_action_orders_by_record_date_not_by_kind_or_id)",
30	  "mutant D: present.py:40 drops the no-answer clause; pytest: '1 failed, 12 passed' (killed by test_rerun_available_follows_live_mode_and_the_last_rerun)",
31	  "mutant E: case_list.py:23 MAX_TITLE 120 -> 200; pytest: '1 failed, 12 passed' (killed by test_title_on_create_and_patch)",
32	  "every mutant file restored from 'git show 926bf37:<path>' and confirmed identical with diff -q",
33	  "HTML probe (scratchpad t157-html-probe.py, run with python -I, fixture env): POST /api/cases library + title '<img src=x onerror=alert(1)>Rivera' -> 201 title '<img src=x onerror=alert(1)>Rivera'; PATCH title '<script>x</script>\\u0007Acme' -> 200 title '<script>x</script> Acme'; GET case returns the same string",
34	  "PATCH body probe (scratchpad t157-probe2.py): body JSON string '\"title\"' -> 400 bad_request; body '[\"title\"]' -> 400 bad_request; {\"title\": 5} -> 400 bad_request",
35	  "review response for a dismiss carries item.rerun_available = false (fixture); GET case tray item has no rerun_available key",
36	  "readable_title probe: 'case_01_' -> 'Records added Nov 1'; '.txt' -> same; 'case_lib01_' -> same; '  ' -> same",
37	  "read app/backend/api.py:116-119 (live_enabled, demo_mode = not live_enabled) against app/backend/store.py:11-16 (live_model_available)",
38	  "read app/backend/rejudge.py:64-80 and review.py:385 (rejudge attempts stored with verdict; edit pops ladder.rejudge)",
39	  "grep for 'Untitled' in app tests tools evals; grep for case name/title readers in app (none reach a prompt, the letter or the export)",
40	  "frontend sinks: app/frontend/dom.js:5-17 (ZL.el writes text nodes), app/frontend/overview.js:51 and 76-84 (title passed to el as text); grep for innerHTML on title paths (none)",
41	  "grep for bare except / except: pass in the diff (none added; only try/finally in get_case_view)"
42	 ],
43	 "verdict": "changes",
44	 "scores": {"card_acs_implemented": 4, "tests_prove_acs": 2, "title_input_validation": 2, "rerun_available_correct": 4, "next_action_determinism": 4, "contract_consistency": 3, "honest_failure": 4},
45	 "findings": [
46	  {"severity": "major",
47	   "title": "Case titles are not validated for HTML (brief check fails); markup is stored and returned verbatim",
48	   "evidence": "Probe output (scratchpad t157-html-probe.py, python -I): create with title '<img src=x onerror=alert(1)>Rivera' -> 201 title '<img src=x onerror=alert(1)>Rivera'; PATCH '<script>x</script>\\u0007Acme' -> 200 '<script>x</script> Acme'; GET case same. Code: app/backend/case_list.py:23-29 clean_title only maps control characters and collapses whitespace, then truncates to 120; no markup check. Derived default copies record text: case_list.py:32-47 derived_title uses clean_title(r['source_label']) on the Source header of a record, which api.md line 46 treats as untrusted. The contract's plain-text rule (api.md:46) lists record text, excerpts and summaries but not titles.",
49	   "why_it_matters": "The brief requires titles validated for length and HTML. Length is validated (120, test_case_list.py:185-186); HTML is not. Not a live XSS today: app/frontend/dom.js:5-17 writes text nodes and overview.js:76-84 passes the title to el() as text. But the value is untrusted record text in a field the contract does not cover, so the first innerHTML sink added later becomes stored XSS. Rated major (not blocker) because no current sink renders markup; this is a missed required check, not an unsafe shipped path.",
50	   "fix": "Decide the rule and enforce it in clean_title. Either reject typed titles containing < or > with 400 bad_request (detail.reason 'title_markup'), and strip tags from derived titles (source label becomes plain text), or document titles as plain text in api.md line 46 and keep the derived text escaped. Add both to the api.md title paragraph (line 703).",
51	   "acceptance_test": "Unit: clean_title('<img src=x onerror=alert(1)>Rivera') contains no '<' (or the typed path returns 400 bad_request). Integration: POST /api/cases with title '<script>x</script>' returns 400 bad_request, and PATCH with the same returns 400 and leaves the stored name unchanged. Derived title for a record with Source '<b>Clinic</b>' contains no '<'."},
52	  {"severity": "major",
53	   "title": "next_action blockers-first rule has no test that fails when it breaks (mutant survives)",
54	   "evidence": "app/backend/case_list.py:131 'first = next((b for b in blockers if b[\"reason_code\"] != \"NOTHING_ACCEPTED\"), None)' mutated to 'first = None' (scratch archive only). '.venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider' -> '13 passed in 7.64s'. The only blocker assertion is tests/unit/test_case_list.py:248-251 and it runs only for a library case that has an item blocker; under the mutant that assertion would fail, so no case in the suite reaches it. api.md:705 says 'tests/unit/test_case_list.py ... checks the order rules'.",
55	   "why_it_matters": "T-157 AC says next_action must be blockers first. A regression that surfaces a waiting item ahead of an export blocker (for example a JUDGE_NOT_RUN accept) would pass CI, and the paralegal would be sent to the wrong item. This is the determinism rule the card exists for.",
56	   "fix": "Add a case where an accepted AI-made item has no second-check answer (JUDGE_NOT_RUN) or a code-check failure on an accepted edit, while other items still wait. Assert next_action equals the blocker, and assert the scenario was actually built (no silent skip). Also add an assertion that next_action is None-free when a blocker exists.",
57	   "acceptance_test": "Scratch mutant 'first = None' in case_list.py:131 must turn the new test red. Test asserts next_action == {item_id, kind, reason} of the export-gate blocker, with a needs-review item present in the same case."},
58	  {"severity": "major",
59	   "title": "next_action timeline pick is untested (mutant survives); test only checks the sort of its own helper",
60	   "evidence": "app/backend/case_list.py:136 'w = waiting[0]' mutated to 'w = waiting[-1]' (scratch archive only); pytest tests/unit/test_case_list.py -> '13 passed in 6.33s'. tests/unit/test_case_list.py:253-256 only asserts that next_action names some needs-review item. tests/unit/test_case_list.py:272-283 asserts that needs_review_order's own output is sorted by the same key the code uses (order == sorted(order, key=...)), which does not test the pick.",
61	   "why_it_matters": "The AC says the single first thing is the first needs-review item in timeline order. Nothing proves the field is that item, so a change to the index or to the review order would pass. The api.md line 703 claim that the tests 'check the order rules' overstates the coverage.",
62	   "fix": "For each library case with a waiting item and no blocker, assert next_action['item_id'] == case_list.needs_review_order(conn, tok)[0]['id'], and assert the chosen item's cited record date is the earliest of the waiting set. Include a case where kind order and date order disagree, so the test cannot pass on id or kind alone.",
63	   "acceptance_test": "Scratch mutant 'waiting[-1]' at case_list.py:136 must turn the test red. Test: for every library case with waiting items and no blocker, next_action.item_id equals the earliest-dated waiting item."},
64	  {"severity": "minor",
65	   "title": "Card evidence for the full unit suite does not reproduce at 926bf37",
66	   "evidence": "board/cards/T-157.md AC evidence: 'full tests/unit 4387 passed, 2 failed (test_e2e_contract ids declared by frontend, not backend)'. My run on the 926bf37 archive (with review-evidence overlay): '4286 passed, 8 skipped in 275.41s', 0 failed. .venv/bin/python -m pytest tests/test_e2e_contract.py --co reports 'no tests collected', and the file is not under tests/unit.",
67	   "why_it_matters": "Evidence that cannot be reproduced cannot support the verdict. The worker may have run a dirty working tree (git status shows uncommitted product files from other cards). Not a code defect in T-157, but the card cites a file outside the suite it names.",
68	   "fix": "Rerun 'python3 -m pytest tests/unit -q' from a clean archive of the commit, paste the exact command and tail into the card AC evidence, and drop the test_e2e_contract line unless it is reproduced in tests/unit.",
69	   "acceptance_test": "Card AC evidence includes the command and the pytest summary line, and it matches a fresh git archive run."},
70	  {"severity": "minor",
71	   "title": "rerun_available re-derives the demo/live rule instead of using the one that defines demo mode",
72	   "evidence": "app/backend/store.py:11-16 live_model_available() = name != 'fixture' and ENABLE_LIVE == '1' and (claude-cli or ANTHROPIC_API_KEY). app/backend/api.py:116-119 live_enabled() = ENABLE_LIVE == '1' and (backend() == 'claude-cli' or key); demo_mode() = not live_enabled(). The two agree by reading today, but two definitions of 'live' can drift, and the spec says demo mode is the gate.",
73	   "why_it_matters": "If the two drift, the item could say a rerun can answer in demo mode, which is the failure the AC forbids. Nothing in the suite asserts they agree.",
74	   "fix": "Have present.rerun_available use the same demo_mode/live function as the API (move the definition to one module), and add a parametrized test over LLM_BACKEND, ENABLE_LIVE and ANTHROPIC_API_KEY asserting rerun_available is False whenever demo_mode() is True.",
75	   "acceptance_test": "Parametrized test: for each env combination, rerun_available == (not demo_mode()) for a fixture item."},
76	  {"severity": "minor",
77	   "title": "The anthropic-api-without-key assertion is conditional and can pass without checking anything",
78	   "evidence": "tests/unit/test_case_list.py:227-229: 'other = [...][:1]' then 'if other: assert other[0][\"rerun_available\"] is False'.",
79	   "why_it_matters": "If the library case has no flags or amounts, the no-key branch asserts nothing, and a regression would pass silently.",
80	   "fix": "Name a specific item id from the case and assert on it unconditionally.",
81	   "acceptance_test": "Test asserts rerun_available is False for a named flag or amount with LLM_BACKEND=anthropic-api and no key, without an if-guard."},
82	  {"severity": "minor",
83	   "title": "PDF title query parameter is untested",
84	   "evidence": "app/backend/api.py:252 create_case_from_pdf(..., title: str = None) and the make_case call passing 'title if title is not None else name'. No test in tests/unit/test_case_list.py posts to /api/cases/pdf with title. api.md line 60 documents the parameter.",
85	   "why_it_matters": "A documented input path with no test can regress (for example the name would be dropped), and nothing would fail.",
86	   "fix": "Add one test posting an existing synthetic PDF fixture with ?title= and asserting the returned title and GET case title.",
87	   "acceptance_test": "POST /api/cases/pdf?title=Rivera%20intake returns 201 and title 'Rivera intake'. (Not run by me.)"},
88	  {"severity": "nit",
89	   "title": "A stored name that is empty after cleanup skips the record-header default",
90	   "evidence": "Probe: readable_title('case_01_', 'paste', ...) -> 'Records added Nov 1'; '.txt' and 'case_lib01_' give the same. app/backend/case_list.py:61-65 case_title uses readable_title whenever name is non-blank, so the header default (api.md:703 rule 2) is never reached for such names.",
91	   "why_it_matters": "Still never 'Untitled case', so no contract breach. The title is less useful than the first record header and differs from the documented order.",
92	   "fix": "Treat an empty readable name as no name and fall through to derived_title.",
93	   "acceptance_test": "case_title for a case named 'case_01_' returns the derived header title when a record has a Source line."},
94	  {"severity": "nit",
95	   "title": "Frontend still carries an Untitled case fallback (outside this commit)",
96	   "evidence": "app/frontend/overview.js:51 titleOf: '... || \"Untitled case\"'. Unreachable today because the backend always sends a non-empty title.",
97	   "why_it_matters": "Dead text, but it is the string the AC bans, and a future backend null would show it.",
98	   "fix": "Route to the frontend card: drop the fallback and fall back to the backend title only.",
99	   "acceptance_test": "grep -rn 'Untitled case' app/frontend returns nothing."}
100	 ],
101	 "whats_right": [
102	  "next_action and needs_review_order are code-only and deterministic: the sort key ends in the item id (case_list.py:117) and the no-model-call test passes.",
103	  "rerun_available is false in fixture/demo mode and after a no-answer rerun; the review response carries it and tray items omit it, as api.md requires (mutant D killed).",
104	  "PATCH rejects non-object bodies, non-text titles and unknown tokens with explicit 400/404, and the 120-character cap is enforced by test (mutant E killed)."
105	 ],
106	 "questions_for_chris": [
107	  "For typed titles that contain < or >, do you want a 400 (reject) or stored-as-text with escaping at the sink? The answer decides the fix for finding 1."
108	 ]}
109	```
110	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:27.497Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-157 && git rev-parse --short HEAD && git log --oneline -5 && git show --stat 852b060 | head -40",
 "description": "Show T-157 card, HEAD, and commit 852b060 stats"
}
````

### User / tool · 2026-11-02T15:23:27.710Z

**tool result**
````
---
id: "T-157"
title: "API for T-149 r2 + T-136 debt: cases can be named (title on create, PATCH /api/cases/{token} {title}; default title derived from the first record header, never 'Untitled case'); item.rerun_available (false in demo/fixture mode or after a no-answer rerun); case_list.next_action {item_id, kind, reason} = the single first thing to do"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T14:35:34Z"
updated_at: "2026-11-02T15:23:19Z"
claimed_by: "backend"
claimed_at: "2026-11-02T14:59:27Z"
rounds: 1
commits: ["926bf37", "852b060"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-157-staff-engineer.md", "at": "2026-11-02T14:59:19Z"}
ac:
  - {"n": 1, "text": "title create/PATCH/default with tests; rerun_available per item with tests; next_action deterministic (blockers first, then needs-review in timeline order); api.md; case_list stays consistent with GET case (existing drift test extended)", "done": true, "evidence": "r2: tests/unit/test_case_list.py 40 pass; mutants (waiting[-1], first=None, seq/rank swap, markup check off, tidy-vs-plain) each turn a test red; clean git archive of 852b060: python -m pytest tests/unit -q -> 4778 passed, 8 skipped"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T14:35:39Z orchestrator: assigned: backend
- 2026-11-02T14:35:46Z backend: claimed
- 2026-11-02T14:38:01Z frontend: frontend (T-149 r2) request: GET /api/cases summary hitl.needs_review is the state-based count and does NOT fall when the paralegal decides an item (probe: dismiss a needs_review entry -> hitl.pending 19->18, hitl.needs_review stays 9; same field in GET case review.counts.needs_review). The overview needs the OPEN count (still undecided AND marked Needs review, = what the detail header computes). Please add hitl.needs_review_open (int) to the list summary (and document it); until it lands the UI falls back to 0 when hitl.pending==0, else min(needs_review, pending). Also confirming the shapes I code against: POST /api/cases {text|sample|library, title?}; PATCH /api/cases/{token} {title} -> summary-like {token,title}; summary.next_action {item_id, kind, reason} or null; item.rerun_available on items of GET case (entries/flags/amounts) and in trace blockers if that is where JUDGE_NOT_RUN lives. Tell me if any differ.
- 2026-11-02T14:47:03Z backend: AC 1 checked: tests/unit/test_case_list.py (13 tests: title create/PATCH/default/never Untitled, rerun_available fixture/live/no-answer, next_action order + drift vs GET case for every library case) pass; full tests/unit 4387 passed, 2 failed (test_e2e_contract ids declared by frontend, not backend); api.md updated; commit 926bf37
- 2026-11-02T14:47:03Z backend: moved in_progress -> in_review
- 2026-11-02T14:47:09Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T14:59:19Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-157-staff-engineer.md; round 1; findings:
    - [major] Case titles are not validated for HTML (brief check fails); markup is stored and returned verbatim — fix: Decide the rule and enforce it in clean_title. Either reject typed titles containing < or > with 400 bad_request (detail.reason 'title_markup'), and strip tags from derived titles (source label becomes plain text), or document titles as plain text in api.md line 46 and keep the d
    - [major] next_action blockers-first rule has no test that fails when it breaks (mutant survives) — fix: Add a case where an accepted AI-made item has no second-check answer (JUDGE_NOT_RUN) or a code-check failure on an accepted edit, while other items still wait. Assert next_action equals the blocker, and assert the scenario was actually built (no silent skip). Also add an assertion that next
    - [major] next_action timeline pick is untested (mutant survives); test only checks the sort of its own helper — fix: For each library case with a waiting item and no blocker, assert next_action['item_id'] == case_list.needs_review_order(conn, tok)[0]['id'], and assert the chosen item's cited record date is the earliest of the waiting set. Include a case where kind order and date order disagre
    - [minor] Card evidence for the full unit suite does not reproduce at 926bf37 — fix: Rerun 'python3 -m pytest tests/unit -q' from a clean archive of the commit, paste the exact command and tail into the card AC evidence, and drop the test_e2e_contract line unless it is reproduced in tests/unit.
    - [minor] rerun_available re-derives the demo/live rule instead of using the one that defines demo mode — fix: Have present.rerun_available use the same demo_mode/live function as the API (move the definition to one module), and add a parametrized test over LLM_BACKEND, ENABLE_LIVE and ANTHROPIC_API_KEY asserting rerun_available is False whenever demo_mode() is True.
    - [minor] The anthropic-api-without-key assertion is conditional and can pass without checking anything — fix: Name a specific item id from the case and assert on it unconditionally.
    - [minor] PDF title query parameter is untested — fix: Add one test posting an existing synthetic PDF fixture with ?title= and asserting the returned title and GET case title.
- 2026-11-02T14:59:19Z orchestrator: assigned: backend
- 2026-11-02T14:59:27Z backend: claimed
- 2026-11-02T15:23:13Z backend: AC 1 checked: r2: tests/unit/test_case_list.py 40 pass; mutants (waiting[-1], first=None, seq/rank swap, markup check off, tidy-vs-plain) each turn a test red; clean git archive of 852b060: python -m pytest tests/unit -q -> 4778 passed, 8 skipped
- 2026-11-02T15:23:13Z backend: moved in_progress -> in_review
- 2026-11-02T15:23:19Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (r2): titles are plain text: validate_title strips control/bidi chars, collapses white space, refuses < or > and >120 chars with 422 invalid_title (plain message, never echoes the text, nothing stored; also PDF ?title checked before the file is read; legacy name only cut, not refused); derived titles drop tags; empty-after-cleanup name falls through to the record header. Tests pin blockers-first (JUDGE_NOT_RUN + failed run, scenarios asserted built) and timeline pick (date forced against seq/kind/id, seq vs rank tie, undated last, every library case == needs_review_order()[0]); mutants waiting[-1], first=None, seq/rank swap, markup check off all killed. Minors: store.live_enabled is the one live definition (api.demo_mode is its negation), parametrized env test; named-item no-if assertion; PDF ?title test. How verified: pytest tests/unit/test_case_list.py 40 pass; clean git archive of 852b060 full tests/unit 4778 passed, 8 skipped (the dirty tree shows 37 failures in other workers' in-flight amounts/T-139/eval files, none in mine). Left: frontend may show 422 invalid_title message; api.md updated. Surprised: PATCH validates the title before the token lookup, so bad title on unknown token is 422 not 404.

2ac96cf
2ac96cf fix(backend): T-140 D-062 total line 'Billed charges accepted from these records', charge sources by billing header, per-figure rule, CPT/HCPCS normalization
852b060 fix(backend): T-157 r2 title validation (plain text, 422 invalid_title), next_action order tests kill the mutants, one live definition for rerun_available
ba21b4b docs(orchestrator): scope cut 13f T-141 residual phrasings
ff1256e fix(backend): T-141 r6 per-clause governance, plural/bare forms, plural-list date guard
83f1afd fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)
commit 852b06082cc74ec884818b570926731c72d2296f
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:17:06 2026 -0600

    fix(backend): T-157 r2 title validation (plain text, 422 invalid_title), next_action order tests kill the mutants, one live definition for rerun_available
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py           |  28 +++--
 app/backend/case_list.py     |  64 +++++++++---
 app/backend/store.py         |  13 ++-
 memory/contracts/api.md      |   4 +-
 tests/unit/test_case_list.py | 244 ++++++++++++++++++++++++++++++++++++++++++-
 5 files changed, 321 insertions(+), 32 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:27.780Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md"
}
````

### User / tool · 2026-11-02T15:23:27.787Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:32.623Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md"
}
````

### User / tool · 2026-11-02T15:23:32.636Z

**tool result**
````
1	---
2	name: t157-case-title-next-action-patterns
3	description: T-157 r1 926bf37 (changes): next_action blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card full-suite counts do not reproduce, archive needs review-evidence overlay
4	metadata:
5	  type: project
6	---
7	
8	T-157 r1 at 926bf37 was verdict changes (3 majors, 4 minors, 2 nits). Reviewer file reviews/T-157-staff-engineer.md is write-once.
9	
10	- **Survivors in a new ordering feature.** Mutants that break the blockers-first rule (`first = None`) and the timeline pick (`waiting[-1]`) both left all 13 tests green. The tests asserted membership and the helper's own sort, not the chosen item. Lesson: for any "single first item" field, mutate the selection index and the precedence branch, not only the sort key.
11	- **Titles.** Length cap (120) was tested, HTML was not. Record text (Source header) flows into the derived default title. The frontend writes text nodes, so it is not exploitable today; rate major, not blocker, and escalate if an innerHTML sink appears.
12	- **Evidence numbers.** The card claimed 4387 passed / 2 failed in tests/unit; the same commit gave 4286 passed, 8 skipped, 0 failed. Its failing file (test_e2e_contract) is not under tests/unit. Check card evidence against a clean archive run.
13	- **Archive needs untracked fixtures.** `git archive` omits artifacts/review-evidence (untracked), so tests/unit collection fails with FileNotFoundError until it is overlaid with `cp -Rn` from the working tree. Same root as [[project_round2_snapshot_review_patterns]].
14	- **Working tree is dirty with other cards.** `git status` showed uncommitted app/ changes from other workers; always review the archive of the commit, never the working tree.
15	- **Reviewer write guard.** After the first Write, an Edit to the same reviews file is denied (append-only). A count typo in the summary could not be corrected; get the markdown summary right before the first Write.
16	
17	**Why:** the card AC said "blockers first, then timeline order", and the suite could not tell a correct next_action from a wrong one.
18	**How to apply:** on any future "next item" or "single first thing" field, run mutants on the selection index and each precedence branch; expect red. See [[project_gate_m2_patterns]] for gate blocker ordering.
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:33.070Z

**tool call — Bash**
````
{
 "command": "git show 852b060 -- app/backend/api.py app/backend/case_list.py app/backend/store.py memory/contracts/api.md",
 "description": "Read the 852b060 diff for product files in scope"
}
````

### User / tool · 2026-11-02T15:23:33.189Z

**tool result**
````
commit 852b06082cc74ec884818b570926731c72d2296f
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:17:06 2026 -0600

    fix(backend): T-157 r2 title validation (plain text, 422 invalid_title), next_action order tests kill the mutants, one live definition for rerun_available
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index ca1e6ea..3557396 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -114,7 +114,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
 
     def live_enabled():
-        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
+        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available
 
     def demo_mode():
         return not live_enabled()
@@ -245,8 +245,9 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
         if not isinstance(text, str):
             raise ApiError(400, "bad_request", "Provide text or sample: true.")
-        given = b.get("title") if isinstance(b.get("title"), str) else b.get("name")          # T-157: `title` is the name a paralegal types; `name` stays accepted
-        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample)
+        typed = isinstance(b.get("title"), str)
+        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
+        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)
 
     @app.post("/api/cases/pdf", status_code=201)
     async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
@@ -254,6 +255,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
         if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
             raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
+        valid_name(title if title is not None else name, title is not None)          # T-157 r2: a markup title is refused before a byte is read
         cl = request.headers.get("content-length")
         if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
             raise ApiError(413, "input_too_large", "The PDF is too large.")
@@ -276,11 +278,21 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
                 raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
             raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                            (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
-        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
+        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None},
+                        strict_name=title is not None)
         out["pdf_checks"] = got.get("pdf_checks")
         return out
 
-    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
+    def valid_name(value, strict=True):
+        """T-157 r2: a typed title (or legacy `name`) -> the text to store; markup or an over-long typed title is 422 invalid_title with a plain message."""
+        try:
+            return case_list.validate_title(value) if strict else case_list.clean_title(value)
+        except case_list.TitleError as e:
+            raise ApiError(422, "invalid_title", str(e)) from None
+
+    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
+        name = name if isinstance(name, str) else ("Sample case" if sample else None)
+        name = valid_name(name, strict_name)          # before anything is stored: a refused title leaves no case behind
         try:
             text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
         except ingest.IngestError as e:
@@ -291,8 +303,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         try:
             now = time.time()
             DB.purge_expired(c, now)
-            name = name if isinstance(name, str) else ("Sample case" if sample else None)
-            cid = DB.create_case(c, text, now=now, name=case_list.clean_title(name) or None,
+            cid = DB.create_case(c, text, now=now, name=name or None,
                                  source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                  **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
             try:
@@ -330,10 +341,11 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         b = await body_of(request)
         if "title" not in b or not (b["title"] is None or isinstance(b["title"], str)):
             raise ApiError(400, "bad_request", "Send {\"title\": text}.")
+        name = valid_name(b["title"])
         c = conn()
         try:
             get_case(c, token)
-            DB.update_case(c, token, name=case_list.clean_title(b["title"]) or None)
+            DB.update_case(c, token, name=name or None)
             case = DB.get_case(c, token)
             return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
         finally:
diff --git a/app/backend/case_list.py b/app/backend/case_list.py
index 9e27bba..4e28206 100644
--- a/app/backend/case_list.py
+++ b/app/backend/case_list.py
@@ -21,19 +21,51 @@ _EXT = re.compile(r"\.(pdf|txt|docx?|rtf)$", re.IGNORECASE)
 
 
 MAX_TITLE = 120
-_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]")
+_WS = re.compile(r"[\t\n\r\x0b\x0c\x85\u2028\u2029]+")
+_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]")      # control, zero-width and bidi-override characters: removed
+_TAG = re.compile(r"<[^<>]*>?")
+
+
+class TitleError(ValueError):
+    """T-157 r2: a typed title that cannot be stored. str(e) is the plain message the API returns (422 invalid_title); it never repeats the rejected text."""
+
+
+def _tidy(value) -> str:
+    """Control and bidi characters removed, line breaks and tabs turned into spaces, runs of white space collapsed. '' for anything that is not text."""
+    if not isinstance(value, str):
+        return ""
+    return re.sub(r" +", " ", _CTRL.sub("", _WS.sub(" ", value))).strip()
+
+
+def validate_title(value) -> str:
+    """T-157 r2: a title the paralegal typed (create, PATCH). Control characters stripped, white space collapsed; '' when nothing is left (clears the name).
+    Raises TitleError for markup (any < or >: a title is plain text, never HTML) and for more than 120 characters. Nothing is escaped or rewritten: it is refused, so what is
+    stored is exactly what was typed."""
+    t = _tidy(value)
+    if "<" in t or ">" in t:
+        raise TitleError("A case title is plain text. Remove the angle brackets and try again.")
+    if len(t) > MAX_TITLE:
+        raise TitleError(f"A case title can be at most {MAX_TITLE} characters. Shorten it and try again.")
+    return t
+
+
+def plain_title(value) -> str:
+    """T-157 r2: text from a record (a Source line) shown as a title: tags dropped, stray angle brackets removed, tidied, at most 120 characters. Never refused: it is not typed."""
+    return _tidy(re.sub(r"[<>]", "", _TAG.sub(" ", _tidy(value))))[:MAX_TITLE].strip()
 
 
 def clean_title(value) -> str:
-    """T-157: a case name as typed: control characters and line breaks become spaces, runs of white space collapse, at most 120 characters. '' when nothing is left."""
-    return re.sub(r"\s+", " ", _CTRL.sub(" ", value if isinstance(value, str) else "")).strip()[:MAX_TITLE].strip()
+    """The stored name of a case from a field that may hold a file name (`name`, the PDF's name): validated like a typed title, except that a long file name is cut to
+    120 characters, not refused. Markup is still refused."""
+    t = _tidy(value)
+    return validate_title(t if ("<" in t or ">" in t) else t[:MAX_TITLE])
 
 
 def derived_title(conn, case_id) -> str:
     """T-157: the title of a case nobody named, from its first record header: the provider (Source line) and that record's date, "Marrowgate General ED, Feb 14, 2026".
     None when no record has either."""
     for r in conn.execute("SELECT source_label, date_iso FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
-        label = clean_title(r["source_label"])[:60].strip()
+        label = plain_title(r["source_label"])[:60].strip()
         try:
             day = datetime.date.fromisoformat(r["date_iso"]).strftime("%b %-d, %Y") if r["date_iso"] else None
         except ValueError:
@@ -45,13 +77,20 @@ def derived_title(conn, case_id) -> str:
     return None
 
 
-def readable_title(name, source, created_at) -> str:
-    """A name a paralegal would recognise. A file name or slug ("smith_records-2024.pdf") becomes words; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case";
-    `case_title` prefers the first record header over this fallback)."""
-    n = _LIB_PREFIX.sub("", (name or "").strip())
-    if n and (_SLUG.match(n) or n != (name or "").strip()) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name
+def readable_name(name) -> str:
+    """A stored name made readable: a file name or slug ("smith_records-2024.pdf", "case_lib01_er_only") becomes words, a typed name keeps its words, markup is dropped.
+    '' when nothing is left ("case_01_", ".txt")."""
+    typed = plain_title(name)
+    n = _LIB_PREFIX.sub("", typed)
+    if n and (_SLUG.match(n) or n != typed) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name
         n = re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", _EXT.sub("", n))).strip()
         n = n[:1].upper() + n[1:]
+    return n
+
+
+def readable_title(name, source, created_at) -> str:
+    """A name a paralegal would recognise; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case"; `case_title` prefers the first record header over that fallback)."""
+    n = readable_name(name)
     if n:
         return n
     day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime("%b %-d")
@@ -59,10 +98,9 @@ def readable_title(name, source, created_at) -> str:
 
 
 def case_title(conn, case: dict) -> str:
-    """What to show for a case: its name made readable; else the first record header (provider and date); else the date it was added. Never "Untitled case"."""
-    if (case["name"] or "").strip():
-        return readable_title(case["name"], case["source"], case["created_at"])
-    return derived_title(conn, case["id"]) or readable_title(None, case["source"], case["created_at"])
+    """What to show for a case: its name made readable; else (no name, or one that is empty after cleanup) the first record header (provider and date); else the date it was added.
+    Never "Untitled case", never markup."""
+    return readable_name(case["name"]) or derived_title(conn, case["id"]) or readable_title(None, case["source"], case["created_at"])
 
 
 def run_progress(case: dict, stages) -> tuple:
diff --git a/app/backend/store.py b/app/backend/store.py
index b71bf3e..12c7855 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -8,12 +8,17 @@ from app.backend import ingest, pdf_text, spanish
 from app.db import db as DB
 
 
+def live_enabled() -> bool:
+    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
+    Read per call so a test can change the environment."""
+    from app.llm import provider
+    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
+
+
 def live_model_available() -> bool:
-    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with.
-    Read per call, like api.live_enabled, so a test can change the environment."""
+    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
     from app.llm import provider
-    name = provider.backend_name()
-    return name != "fixture" and os.environ.get("ENABLE_LIVE") == "1" and (name == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
+    return provider.backend_name() != "fixture" and live_enabled()
 
 
 def iso(t) -> str:
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 7bd5565..7bff3e6 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -57,7 +57,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 `backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
 
 ## POST /api/cases
-Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). Control characters and line breaks become spaces, runs of white space collapse, at most 120 characters; blank means no name. The response carries `title` (what to show; see "Case titles" under `GET /api/cases`).
+Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). A title is plain text (T-157 r2): control, zero-width and bidi-override characters are removed, line breaks and tabs become spaces, runs of white space collapse; blank means no name. A `title` with a `<` or `>` in it, or longer than 120 characters, is refused: `422 invalid_title` with a plain `message` that never repeats the text, and no case is created (the same for the `title` query of `POST /api/cases/pdf`, checked before the PDF is read). The older `name` field is held to the markup rule too, but a `name` longer than 120 characters (a long file name) is cut, not refused. The response carries `title` (what to show; see "Case titles" under `GET /api/cases`).
 ```json
 { "name": "Rivera sample", "text": "SYNTHETIC — ...\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, ...\"\n...", "sample": false }
 ```
@@ -702,7 +702,7 @@ Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays tok
   "export_ready": true,
   "next_action": { "item_id": "f_r3_1" | null, "kind": "entry|flag|amount|case|run", "reason": "plain sentence" } | null }
 ```
-**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no name, the first record header: the provider (its Source line, at most 60 characters) and that record's date, "Marrowgate General ED, Feb 14, 2026" ("Records from Feb 14, 2026" when the record has no Source line, the bare provider when it has no date); (3) when no record has either, "Records added Nov 2" ("Sample case" for the sample). `name` is the stored value, `null` until someone names the case. `PATCH /api/cases/{token}` with `{"title": "Rivera v. Acme"}` stores the name (same cleaning as on create: line breaks and control characters become spaces, white space collapses, 120 characters at most) and answers `200 {token, name, title}`; a blank or `null` title clears the name, so the title returns to the derived default; a body without `title`, or a `title` that is neither text nor null, is `400 bad_request`; an unknown token is `404 not_found`. The name goes through the same readable-title step as any other, so underscores or a file extension in a typed title are shown as words. Allowed in public mode too (the token is the capability). A rename is not a review event.
+**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no name, or a name that is empty once cleaned (`case_01_`, `.txt`), the first record header: the provider (its Source line with any tags or angle brackets dropped, at most 60 characters) and that record's date, "Marrowgate General ED, Feb 14, 2026" ("Records from Feb 14, 2026" when the record has no Source line, the bare provider when it has no date); (3) when no record has either, "Records added Nov 2" ("Sample case" for the sample). `name` is the stored value, `null` until someone names the case. `PATCH /api/cases/{token}` with `{"title": "Rivera v. Acme"}` stores the name (same rule as on create: plain text, control characters removed, white space collapsed; a `<` or `>` or more than 120 characters is `422 invalid_title` and the stored name is unchanged) and answers `200 {token, name, title}`; a blank or `null` title clears the name, so the title returns to the derived default; a body without `title`, or a `title` that is neither text nor null, is `400 bad_request`; an unknown token is `404 not_found`. The name goes through the same readable-title step as any other, so underscores or a file extension in a typed title are shown as words. Allowed in public mode too (the token is the capability). A rename is not a review event. **A title is never markup:** a typed title is refused if it contains `<` or `>`, and a title derived from a record's Source line has its tags dropped, so `title` is always plain text and a client may still render it as text only (`textContent`), never as HTML.
 
 **`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
 `GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:35.592Z

**tool call — Bash**
````
{
 "command": "ls -d .venv/bin/python && ls -d artifacts/review-evidence && echo SCRATCH=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ls -la /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad 2>&1 | head -20",
 "description": "Check venv, evidence dir, and scratchpad state"
}
````

### User / tool · 2026-11-02T15:23:41.323Z

**tool result**
````
.venv/bin/python
artifacts/review-evidence
SCRATCH=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
total 353048
drwx------@ 1498 arsis  wheel    47936 Nov  2 09:23 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 07:36 .claude
-rw-r--r--@    1 arsis  wheel      403 Nov  2 07:36 .gitignore
drwxr-xr-x@    6 arsis  wheel      192 Nov  2 08:00 .pytest_cache
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
-rw-r--r--@    1 arsis  wheel     6786 Nov  2 07:36 CLAUDE.md
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M1_nocombine
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M2
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M2_find0
-rw-r--r--@    1 arsis  wheel    83742 Nov  2 07:36 MASTER_PROMPT.md
-rw-r--r--@    1 arsis  wheel     2046 Nov  1 19:21 T-047-run1.json
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 04:04 T-060-pass2-head
drwxr-xr-x@   23 arsis  wheel      736 Nov  2 00:41 T-093-r3-2ab7896
-rw-r--r--@    1 arsis  wheel    74715 Nov  2 00:41 T-093-r3-run.py.orig
drwxr-xr-x@    3 arsis  wheel       96 Nov  2 00:41 T-093-r3-scripts
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:13 T-093-r4-3223e50
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:23:44.904Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$S/T-157-r2-852b060; mkdir -p \"$A\" && cd /Users/arsis/zlayt-pm-project && git archive 852b060 | tar -x -C \"$A\" && cp -Rn /Users/arsis/zlayt-pm-project/artifacts/review-evidence \"$A/artifacts/\" && cd \"$A\" && git -C /Users/arsis/zlayt-pm-project rev-parse 852b060 && find \"$A\" -type f | wc -l && ls \"$A\" && diff -rq /Users/arsis/zlayt-pm-project/app \"$A/app\" 2>/dev/null | head -5; echo \"A=$A\"",
 "description": "Create clean git archive of 852b060 in scratchpad"
}
````

### User / tool · 2026-11-02T15:25:15.079Z

**tool result**
````
A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:25:18.592Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; ls -la \"$A\" | head; cd /Users/arsis/zlayt-pm-project && git archive 852b060 > /dev/null; echo \"archive exit=$?\"; git rev-parse --verify 852b060^{commit}; echo \"rev exit=$?\"",
 "description": "Diagnose why the archive step printed nothing"
}
````

### User / tool · 2026-11-02T15:25:19.361Z

**tool result**
````
total 208
drwxr-xr-x@   21 arsis  wheel    672 Nov  2 09:23 .
drwx------@ 1502 arsis  wheel  48064 Nov  2 09:24 ..
drwxr-xr-x@    7 arsis  wheel    224 Nov  2 09:17 .claude
-rw-r--r--@    1 arsis  wheel    403 Nov  2 09:17 .gitignore
-rw-r--r--@    1 arsis  wheel   6786 Nov  2 09:17 CLAUDE.md
-rw-r--r--@    1 arsis  wheel  83742 Nov  2 09:17 MASTER_PROMPT.md
drwxr-xr-x@   10 arsis  wheel    320 Nov  2 09:17 app
drwxr-xr-x@    7 arsis  wheel    224 Nov  2 09:17 artifacts
drwxr-xr-x@    6 arsis  wheel    192 Nov  2 09:17 board
archive exit=0
852b06082cc74ec884818b570926731c72d2296f
rev exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:25:23.232Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cd /Users/arsis/zlayt-pm-project; cp -Rn artifacts/review-evidence \"$A/artifacts/\" ; echo \"cp exit=$?\"; find \"$A/artifacts/review-evidence\" -type f | wc -l; for f in app/backend/case_list.py app/backend/api.py app/backend/store.py app/backend/present.py tests/unit/test_case_list.py; do git show 852b060:$f | diff -q - \"$A/$f\" && echo \"same $f\"; done; ls \"$A/.venv\" 2>&1 | head -1",
 "description": "Overlay review-evidence and verify archive matches 852b060"
}
````

### User / tool · 2026-11-02T15:25:34.850Z

**tool result**
````
cp exit=1
  109605
same app/backend/case_list.py
same app/backend/api.py
same app/backend/store.py
same app/backend/present.py
same tests/unit/test_case_list.py
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/.venv: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:25:39.321Z

**tool call — Bash**
````
{
 "command": "find artifacts/review-evidence -type f | wc -l; A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; ls \"$A/artifacts/review-evidence\" | head -5; find \"$A/artifacts\" -type f | wc -l; cd \"$A\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -15",
 "description": "Count evidence files and run test_case_list.py on archive"
}
````

### User / tool · 2026-11-02T15:25:51.431Z

**tool result**
````
  109605
GATE-M2-paralegal
M0-r2-staff-resolution.md
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
  109704
........................................                                 [100%]
40 passed in 11.33s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:25:54.737Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cd \"$A\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider > \"$A/../T-157-r2-full-unit.out\" 2>&1; echo \"exit=$?\" >> \"$A/../T-157-r2-full-unit.out\"",
 "description": "Run full tests/unit suite on the archive in background",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T15:25:54.818Z

**tool result**
````
Command running in background with ID: b4j1d1vxt. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b4j1d1vxt.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:25:57.384Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cat -n \"$A/app/backend/case_list.py\" | sed -n '1,200p'",
 "description": "Read case_list.py in the 852b060 archive with line numbers"
}
````

### User / tool · 2026-11-02T15:25:57.477Z

**tool result**
````
     1	"""GET /api/cases (T-148): one summary per case for the local profile's overview screen. Local mode only (D-008/D-031); the route is a 404 otherwise.
     2	
     3	Code only: no model call, no pipeline run, no record text. Every number comes from the functions GET case, GET status and the export gate already use, so the
     4	list cannot say something the case screen does not:
     5	  run                                        -> run_progress() (the /status route calls it too)
     6	  progress decided / total per kind          -> the item filter present.review_view applies (live = not rejected, no tray placeholder, no rule-filtered proposal)
     7	  hitl.needs_review, edits_to_check, tray    -> present.review_view counts (the tray length GET case returns is the `rejected` count)
     8	  hitl.gate, export_ready                    -> the export_gate step of trace.case_trace (blockers and warnings with their plain `why`; the list GET /export refuses on)
     9	tests/unit/test_case_list.py compares each field with GET case, /status, /trace and /export for every library case.
    10	"""
    11	import datetime
    12	import re
    13	
    14	from app.backend import flag_templates as FT, generator, present, review, store, trace
    15	from app.db import db as DB
    16	
    17	KINDS = (("entries", "entry"), ("flags", "flag"), ("amounts", "amount"))
    18	_SLUG = re.compile(r"^[\w.\-]+$")
    19	_LIB_PREFIX = re.compile(r"^case[ _](?:lib)?\d+[ _]", re.IGNORECASE)      # evals/library and evals/golden file names: case_lib01_..., case_01_...
    20	_EXT = re.compile(r"\.(pdf|txt|docx?|rtf)$", re.IGNORECASE)
    21	
    22	
    23	MAX_TITLE = 120
    24	_WS = re.compile(r"[\t\n\r\x0b\x0c\x85\u2028\u2029]+")
    25	_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]")      # control, zero-width and bidi-override characters: removed
    26	_TAG = re.compile(r"<[^<>]*>?")
    27	
    28	
    29	class TitleError(ValueError):
    30	    """T-157 r2: a typed title that cannot be stored. str(e) is the plain message the API returns (422 invalid_title); it never repeats the rejected text."""
    31	
    32	
    33	def _tidy(value) -> str:
    34	    """Control and bidi characters removed, line breaks and tabs turned into spaces, runs of white space collapsed. '' for anything that is not text."""
    35	    if not isinstance(value, str):
    36	        return ""
    37	    return re.sub(r" +", " ", _CTRL.sub("", _WS.sub(" ", value))).strip()
    38	
    39	
    40	def validate_title(value) -> str:
    41	    """T-157 r2: a title the paralegal typed (create, PATCH). Control characters stripped, white space collapsed; '' when nothing is left (clears the name).
    42	    Raises TitleError for markup (any < or >: a title is plain text, never HTML) and for more than 120 characters. Nothing is escaped or rewritten: it is refused, so what is
    43	    stored is exactly what was typed."""
    44	    t = _tidy(value)
    45	    if "<" in t or ">" in t:
    46	        raise TitleError("A case title is plain text. Remove the angle brackets and try again.")
    47	    if len(t) > MAX_TITLE:
    48	        raise TitleError(f"A case title can be at most {MAX_TITLE} characters. Shorten it and try again.")
    49	    return t
    50	
    51	
    52	def plain_title(value) -> str:
    53	    """T-157 r2: text from a record (a Source line) shown as a title: tags dropped, stray angle brackets removed, tidied, at most 120 characters. Never refused: it is not typed."""
    54	    return _tidy(re.sub(r"[<>]", "", _TAG.sub(" ", _tidy(value))))[:MAX_TITLE].strip()
    55	
    56	
    57	def clean_title(value) -> str:
    58	    """The stored name of a case from a field that may hold a file name (`name`, the PDF's name): validated like a typed title, except that a long file name is cut to
    59	    120 characters, not refused. Markup is still refused."""
    60	    t = _tidy(value)
    61	    return validate_title(t if ("<" in t or ">" in t) else t[:MAX_TITLE])
    62	
    63	
    64	def derived_title(conn, case_id) -> str:
    65	    """T-157: the title of a case nobody named, from its first record header: the provider (Source line) and that record's date, "Marrowgate General ED, Feb 14, 2026".
    66	    None when no record has either."""
    67	    for r in conn.execute("SELECT source_label, date_iso FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
    68	        label = plain_title(r["source_label"])[:60].strip()
    69	        try:
    70	            day = datetime.date.fromisoformat(r["date_iso"]).strftime("%b %-d, %Y") if r["date_iso"] else None
    71	        except ValueError:
    72	            day = None
    73	        if label:
    74	            return f"{label}, {day}" if day else label
    75	        if day:
    76	            return f"Records from {day}"
    77	    return None
    78	
    79	
    80	def readable_name(name) -> str:
    81	    """A stored name made readable: a file name or slug ("smith_records-2024.pdf", "case_lib01_er_only") becomes words, a typed name keeps its words, markup is dropped.
    82	    '' when nothing is left ("case_01_", ".txt")."""
    83	    typed = plain_title(name)
    84	    n = _LIB_PREFIX.sub("", typed)
    85	    if n and (_SLUG.match(n) or n != typed) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name
    86	        n = re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", _EXT.sub("", n))).strip()
    87	        n = n[:1].upper() + n[1:]
    88	    return n
    89	
    90	
    91	def readable_title(name, source, created_at) -> str:
    92	    """A name a paralegal would recognise; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case"; `case_title` prefers the first record header over that fallback)."""
    93	    n = readable_name(name)
    94	    if n:
    95	        return n
    96	    day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime("%b %-d")
    97	    return "Sample case" if source == "sample" else f"Records added {day}"
    98	
    99	
   100	def case_title(conn, case: dict) -> str:
   101	    """What to show for a case: its name made readable; else (no name, or one that is empty after cleanup) the first record header (provider and date); else the date it was added.
   102	    Never "Untitled case", never markup."""
   103	    return readable_name(case["name"]) or derived_title(conn, case["id"]) or readable_title(None, case["source"], case["created_at"])
   104	
   105	
   106	def run_progress(case: dict, stages) -> tuple:
   107	    """(stage, steps_done) for a case row: what GET /status reports. A case that was only ingested is at the 'ingest' stage."""
   108	    stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
   109	    return stage, (list(stages).index(stage) if stage in stages else 0)
   110	
   111	
   112	def _progress(conn, case_id) -> dict:
   113	    """decided / total per kind over the items review_view counts. An edit still marked Needs review (T-134) is not decided."""
   114	    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
   115	    handled = generator.resolved_placeholders(items["entry"])
   116	    out = {}
   117	    for label, kind in KINDS:
   118	        live = [r for r in items[kind] if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons")) and r["state"] != "rejected"]
   119	        decided = sum(1 for r in live if r["review_status"] in ("accepted", "dismissed", "edited") and not review.edit_unconfirmed(kind, r))
   120	        out[label] = {"decided": decided, "total": len(live)}
   121	    return out
   122	
   123	
   124	def _gate(conn, case_id) -> dict:
   125	    step = next(s for s in trace.case_trace(conn, case_id, full=False)["steps"] if s["id"] == "export_gate")
   126	    keep = lambda xs, keys: [{k: x[k] for k in keys if k in x} for x in xs]      # noqa: E731
   127	    return {"ready": step["ready"], "blockers": keep(step["blockers"], ("reason_code", "kind", "item_id", "why")),
   128	            "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}
   129	
   130	
   131	_RANK = {"entry": 0, "flag": 1, "amount": 2}
   132	
   133	
   134	def needs_review_order(conn, case_id) -> list:
   135	    """T-157: the live items that still wait for the paralegal and that the AI could not verify (state needs_review; pending, or an edit not yet confirmed), in timeline order:
   136	    the date of the record each item cites (earliest, for a flag that cites several), then that record's position, then entry before flag before amount, then id. Undated last.
   137	    [{id, kind, date, seq, rank, row}]. Same item filter as `_progress`."""
   138	    recs = {r["id"]: (r["date_iso"], r["seq"]) for r in conn.execute("SELECT id, date_iso, seq FROM records WHERE case_id=?", (case_id,))}
   139	    by_seq = {seq: rid for rid, (_, seq) in recs.items()}
   140	    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
   141	    handled = generator.resolved_placeholders(items["entry"])
   142	    out = []
   143	    for kind, rows in items.items():
   144	        for r in rows:
   145	            if r["id"] in handled or FT.is_filtered(r.get("state_reasons")) or r["state"] != "needs_review":
   146	                continue
   147	            if not (r["review_status"] == "pending" or review.edit_unconfirmed(kind, r)):
   148	                continue
   149	            ids = list(r.get("record_ids") or []) if kind != "flag" else \
   150	                [e.get("record_id") or by_seq.get(e.get("record_no")) for e in r.get("evidence") or []] or list((r.get("computed") or {}).get("record_ids") or [])
   151	            known = sorted((recs[i] for i in ids if i in recs), key=lambda x: (x[0] is None, x[0] or "", x[1] or 0))
   152	            date, seq = known[0] if known else (None, None)
   153	            date = date or (r.get("date_iso") if kind == "entry" else None)
   154	            out.append({"id": r["id"], "kind": kind, "date": date, "seq": seq, "rank": _RANK[kind], "row": r})
   155	    return sorted(out, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))
   156	
   157	
   158	def next_action(conn, case_id, case: dict = None, blockers: list = None):
   159	    """T-157: the single first thing to do in a case, {item_id, kind, reason}, or None when nothing is waiting. Code only, deterministic:
   160	      1. the first export-gate blocker, in gate order (a run in progress or failed, a code-check failure, an accepted item whose second check never answered). Its `kind` is the
   161	         blocker's (`case` for a blocker that names no item, `item_id` null) and `reason` its plain `why`. NOTHING_ACCEPTED yields to step 2 when an item waits (deciding it clears it);
   162	      2. else the first needs-review item in timeline order (`needs_review_order`): `kind` entry | flag | amount, `reason` the item's own plain `why`;
   163	      3. else NOTHING_ACCEPTED when nothing is accepted; else None.
   164	    A case that was only ingested has no items yet: {item_id: null, kind: "run"}. `blockers` may be passed when the caller already read the gate."""
   165	    case = case or DB.get_case(conn, case_id)
   166	    if case["status"] == "ingested":
   167	        return {"item_id": None, "kind": "run", "reason": "Run the case to draft the timeline. Nothing is waiting for you until then."}
   168	    blockers = _gate(conn, case_id)["blockers"] if blockers is None else blockers
   169	    first = next((b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"), None)
   170	    if first:
   171	        return {"item_id": first.get("item_id"), "kind": first["kind"], "reason": first["why"]}
   172	    waiting = needs_review_order(conn, case_id)
   173	    if waiting:
   174	        w = waiting[0]
   175	        return {"item_id": w["id"], "kind": w["kind"], "reason": present.item_view(conn, case_id, w["id"])["why"]}
   176	    if blockers:
   177	        return {"item_id": blockers[0].get("item_id"), "kind": blockers[0]["kind"], "reason": blockers[0]["why"]}
   178	    return None
   179	
   180	
   181	def summary(conn, case_id: str, stages) -> dict:
   182	    case = DB.get_case(conn, case_id)
   183	    rv = present.review_view(conn, case_id)
   184	    counts = rv["counts"]
   185	    stage, done = run_progress(case, stages)
   186	    gate = _gate(conn, case_id)
   187	    last = conn.execute("SELECT max(at) FROM review_events WHERE case_id=?", (case_id,)).fetchone()[0]
   188	    updated = case.get("run_finished_at") or case["created_at"]            # the same value GET case calls updated_at
   189	    return {"token": case_id, "title": case_title(conn, case), "name": case["name"],
   190	            "source": case["source"], "status": case["status"],
   191	            "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (case_id,)).fetchone()[0],
   192	            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(updated), "last_activity_at": store.iso(max(updated, last or 0)),
   193	            "run": {"stage": stage, "steps_done": done, "steps_total": len(stages), "running": case["status"] == "running",
   194	                    "error": bool(case.get("error"))},
   195	            "progress": _progress(conn, case_id),
   196	            "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},      # kept from the first version of this route
   197	            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "edits_to_check": counts["edit_to_check"],
   198	                     "could_not_verify": counts["rejected"], "gate_blockers": gate["blockers"], "gate_warnings": gate["warnings"]},
   199	            "export_ready": gate["ready"], "next_action": next_action(conn, case_id, case, gate["blockers"])}
   200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:25:59.202Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cat -n \"$A/app/backend/store.py\" | sed -n '1,30p'; echo ----; grep -n \"live_enabled\\|demo_mode\\|rerun_available\\|def backend\\|ENABLE_LIVE\" \"$A/app/backend/api.py\" \"$A/app/backend/present.py\" \"$A/app/backend/store.py\" | head -60",
 "description": "Read store.py header and grep live/demo definitions"
}
````

### User / tool · 2026-11-02T15:25:59.294Z

**tool result**
````
     1	"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.
     2	
     3	Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
     4	"""
     5	import os
     6	
     7	from app.backend import ingest, pdf_text, spanish
     8	from app.db import db as DB
     9	
    10	
    11	def live_enabled() -> bool:
    12	    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
    13	    Read per call so a test can change the environment."""
    14	    from app.llm import provider
    15	    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
    16	
    17	
    18	def live_model_available() -> bool:
    19	    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
    20	    from app.llm import provider
    21	    return provider.backend_name() != "fixture" and live_enabled()
    22	
    23	
    24	def iso(t) -> str:
    25	    import datetime
    26	    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    27	
    28	
    29	def load_records(conn, case_id: str, raw: str = None) -> list:
    30	    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
----
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/store.py:11:def live_enabled() -> bool:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/store.py:12:    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/store.py:15:    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/store.py:21:    return provider.backend_name() != "fixture" and live_enabled()
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/present.py:37:def rerun_available(row) -> bool:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/present.py:46:            "rerun_available": rerun_available(row),
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/present.py:311:def case_view(conn, case_id, *, backend, models, demo_mode):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/present.py:346:    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:105:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:112:    def backend():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:116:    def live_enabled():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:117:        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:119:    def demo_mode():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:120:        return not live_enabled()
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:214:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:215:                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:256:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:257:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:300:        if demo_mode() and digest(text) not in allowed_hashes():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:301:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:307:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:320:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:333:            v = present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:386:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:387:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:388:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:403:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:404:        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:411:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:412:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:413:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/backend/api.py:570:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:26:03.126Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cat -n \"$A/app/backend/api.py\" | sed -n '98,122p'; echo ----PRESENT; cat -n \"$A/app/backend/present.py\" | sed -n '28,50p'; echo ----PROVIDER; grep -rn \"def backend_name\" -A12 \"$A/app/llm/\" | head -40",
 "description": "Read api backend/demo definitions, present rerun_available, provider backend_name"
}
````

### User / tool · 2026-11-02T15:26:03.236Z

**tool result**
````
    98	    app.state.recorded = recorded_hashes()
    99	
   100	    def allowed_hashes():
   101	        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
   102	    runs = {}
   103	    rejudging = set()
   104	    DB.connect(db_path).close()
   105	    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
   106	        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
   107	    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
   108	        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
   109	    purged = {"at": 0.0}
   110	
   111	    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
   112	    def backend():
   113	        from app.llm import provider
   114	        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
   115	
   116	    def live_enabled():
   117	        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available
   118	
   119	    def demo_mode():
   120	        return not live_enabled()
   121	
   122	    def models():
----PRESENT
    28	def _ladder(row):
    29	    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    30	    lad["item_id"] = row["id"]
    31	    lad["state"] = row["state"]
    32	    lad["human"] = _human(row)
    33	    lad.pop("pre_edit", None)      # T-138: the undo snapshot is internal (api.md), never in a payload
    34	    return lad
    35	
    36	
    37	def rerun_available(row) -> bool:
    38	    """T-157: whether "run the second check again" can get an answer for this item: no in demo / fixture mode (no live model), no after a rerun that got no answer, yes otherwise."""
    39	    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    40	    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")
    41	
    42	
    43	def _common(row):
    44	    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
    45	            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
    46	            "rerun_available": rerun_available(row),
    47	            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message")}      # T-146 r3: set when a re-run disagreed with or failed on this decided item
    48	
    49	
    50	def entry_view(row, recs):
----PROVIDER
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py:23:def backend_name() -> str:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-24-    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-25-    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-26-    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-27-    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-28-    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-29-        return "fixture"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-30-    return name
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-31-
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-32-
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-33-def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-34-    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060/app/llm/provider.py-35-    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:26:10.787Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cat -n \"$A/tests/unit/test_case_list.py\" | sed -n '1,140p'",
 "description": "Read first half of test_case_list.py in archive"
}
````

### User / tool · 2026-11-02T15:26:10.883Z

**tool result**
````
     1	"""T-148: GET /api/cases summary list. Every field is compared with the route that owns it (GET case, /status, /trace, /export) for every library
     2	case, so the overview can never say something the case screen does not. Fixture backend, no network; local mode only."""
     3	import pathlib
     4	import time
     5	
     6	import pytest
     7	from fastapi.testclient import TestClient
     8	
     9	from app.backend import case_list
    10	from app.backend.api import create_app
    11	
    12	LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
    13	LIB_IDS = sorted(p.stem for p in LIB.glob("*.txt"))
    14	
    15	
    16	@pytest.fixture(scope="module")
    17	def local(tmp_path_factory):
    18	    import os
    19	    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    20	    os.environ.update(LLM_BACKEND="fixture", ZLAYT_MODE="local")
    21	    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
    22	        os.environ.pop(k, None)
    23	    d = tmp_path_factory.mktemp("cl")
    24	    c = TestClient(create_app(str(d / "t.sqlite"), static_dir=str(d)), client=("127.0.0.1", 50000))
    25	    yield c
    26	    for k, v in old.items():
    27	        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    28	
    29	
    30	def _wait(c, tok):
    31	    for _ in range(240):
    32	        s = c.get(f"/api/cases/{tok}/status").json()
    33	        if s["status"] in ("ready", "failed"):
    34	            return s
    35	        time.sleep(0.25)
    36	    raise AssertionError(s)
    37	
    38	
    39	@pytest.fixture(scope="module")
    40	def cases(local):
    41	    """Every library case run to the end, plus one left at ingest, plus decisions made on the first run case (accept, edit, dismiss)."""
    42	    toks = {}
    43	    for lid in LIB_IDS:
    44	        r = local.post("/api/cases", json={"library": lid})
    45	        assert r.status_code == 201, r.text
    46	        toks[lid] = r.json()["token"]
    47	        assert local.post(f"/api/cases/{toks[lid]}/run", json={}).status_code == 202
    48	    for t in toks.values():
    49	        _wait(local, t)
    50	    first = toks[LIB_IDS[0]]
    51	    items = [i for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{first}").json()[k]]
    52	    for n, it in enumerate(items[:6]):
    53	        local.post(f"/api/cases/{first}/items/{it['id']}/review", json={"action": ["accept", "dismiss"][n % 2]})
    54	    second = local.get(f"/api/cases/{toks[LIB_IDS[1]]}").json()["entries"][0]          # a reworded entry: saved, but the second check cannot confirm the new wording
    55	    local.post(f"/api/cases/{toks[LIB_IDS[1]]}/items/{second['id']}/review", json={"action": "edit", "edits": {"summary": second["summary"].rstrip(".") + " (reworded)."}})
    56	    third = toks[LIB_IDS[2]]                                                                  # accept whatever the code checks allow: a case whose export gate opens
    57	    for k in ("entries", "flags", "amounts"):
    58	        for it in local.get(f"/api/cases/{third}").json()[k]:
    59	            local.post(f"/api/cases/{third}/items/{it['id']}/review", json={"action": "accept"})
    60	    text = (LIB / f"{LIB_IDS[-1]}.txt").read_text()               # an allowed (recorded) text, pasted under a file-slug name and never run
    61	    toks["_ingested"] = local.post("/api/cases", json={"text": text, "name": "smith_records-2024.txt"}).json()["token"]
    62	    return toks
    63	
    64	
    65	def _by_token(local):
    66	    r = local.get("/api/cases")
    67	    assert r.status_code == 200
    68	    return {x["token"]: x for x in r.json()["cases"]}
    69	
    70	
    71	def test_list_covers_every_case_newest_first(local, cases):
    72	    got = local.get("/api/cases").json()["cases"]
    73	    assert {x["token"] for x in got} == set(cases.values()) and len(got) == len(LIB_IDS) + 1
    74	    assert got[0]["token"] == cases["_ingested"] and [x["created_at"] for x in got] == sorted((x["created_at"] for x in got), reverse=True)
    75	
    76	
    77	def test_every_summary_field_matches_the_case_status_gate_and_export(local, cases):
    78	    listed = _by_token(local)
    79	    for lid, tok in cases.items():
    80	        s, case = listed[tok], local.get(f"/api/cases/{tok}").json()
    81	        st = local.get(f"/api/cases/{tok}/status").json()
    82	        tr = local.get(f"/api/cases/{tok}/trace").json()
    83	        gate = next(x for x in tr["steps"] if x["id"] == "export_gate")
    84	        # identity and times: the case screen's own values
    85	        assert s["name"] == case["name"] and s["status"] == case["status"] and s["created_at"] == case["created_at"] and s["updated_at"] == case["updated_at"], lid
    86	        assert s["record_count"] == len(case["records"]) and s["last_activity_at"] >= s["updated_at"], lid
    87	        # run stage: the status route
    88	        assert s["run"]["stage"] == st["stage"] and s["run"]["steps_done"] == st["progress"]["done"] and s["run"]["steps_total"] == st["progress"]["total"], lid
    89	        assert s["run"]["running"] == (case["status"] == "running"), lid
    90	        # review counts and the could-not-verify tray: the case screen
    91	        rc = case["review"]["counts"]
    92	        h = s["hitl"]
    93	        assert h["needs_review"] == rc["needs_review"] and h["edits_to_check"] == rc["edit_to_check"] and h["pending"] == rc["pending"], lid
    94	        assert h["could_not_verify"] == len(case["tray"]), lid
    95	        assert s["counts"] == {k: rc[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")}, lid
    96	        # progress per kind: totals are the live items GET case lists, decided never exceeds total, and the kinds add up to the review counts
    97	        live = {"entries": [e for e in case["entries"] + case["undated_entries"]], "flags": case["flags"], "amounts": case["amounts"]}
    98	        for kind, rows in live.items():
    99	            p = s["progress"][kind]
   100	            assert p["total"] == len(rows), (lid, kind)
   101	            assert p["decided"] == sum(1 for r in rows if r["review_status"] in ("accepted", "dismissed", "edited")) - (rc["edit_to_check"] if kind == "entries" else 0), (lid, kind)
   102	        tot = sum(v["total"] for v in s["progress"].values())
   103	        dec = sum(v["decided"] for v in s["progress"].values())
   104	        assert tot - dec == rc["pending"] + rc["edit_to_check"], lid
   105	        # gate: blockers and warnings with their plain reasons, and export_ready is what GET /export allows
   106	        assert s["export_ready"] is gate["ready"] is (local.get(f"/api/cases/{tok}/export").status_code == 200), lid
   107	        assert [(b["reason_code"], b["why"]) for b in h["gate_blockers"]] == [(b["reason_code"], b["why"]) for b in gate["blockers"]], lid
   108	        assert [(w["reason_code"], w["count"], w["why"]) for w in h["gate_warnings"]] == [(w["reason_code"], w["count"], w["why"]) for w in gate["warnings"]], lid
   109	        assert all(b["why"] for b in h["gate_blockers"]) and all(w["why"] for w in h["gate_warnings"]), lid
   110	        # T-157: title and next_action are the same on GET case; no item says rerun is available in fixture mode
   111	        assert s["title"] == case["title"] and "Untitled" not in s["title"], lid
   112	        assert s["next_action"] == case["next_action"], lid
   113	        for k in ("entries", "flags", "amounts"):
   114	            assert all(i["rerun_available"] is False for i in case[k]), (lid, k)
   115	
   116	
   117	def test_decisions_move_the_progress_and_the_ingested_case_is_not_ready(local, cases):
   118	    s = _by_token(local)
   119	    first = s[cases[LIB_IDS[0]]]
   120	    assert sum(v["decided"] for v in first["progress"].values()) >= 1 and first["last_activity_at"] > first["updated_at"] or first["last_activity_at"] >= first["updated_at"]
   121	    ing = s[cases["_ingested"]]
   122	    assert ing["status"] == "ingested" and ing["run"]["stage"] == "ingest" and ing["export_ready"] is False
   123	    assert [b["reason_code"] for b in ing["hitl"]["gate_blockers"]] == ["NOTHING_ACCEPTED"]
   124	
   125	
   126	def test_decided_cases_cover_ready_and_edit_to_check(local, cases):
   127	    s = _by_token(local)
   128	    third = s[cases[LIB_IDS[2]]]
   129	    assert third["export_ready"] is True and third["hitl"]["gate_blockers"] == [] and sum(v["decided"] for v in third["progress"].values()) > 0
   130	    second = s[cases[LIB_IDS[1]]]
   131	    assert second["hitl"]["edits_to_check"] == 1 and second["progress"]["entries"]["decided"] == 0          # a reworded entry is saved but not decided
   132	    assert "EDIT_NOT_CONFIRMED" in [w["reason_code"] for w in second["hitl"]["gate_warnings"]]
   133	
   134	
   135	def test_title_is_readable_not_a_file_slug(local, cases):
   136	    s = _by_token(local)
   137	    assert s[cases["_ingested"]]["title"] == "Smith records 2024"
   138	    for lid in LIB_IDS:
   139	        t = s[cases[lid]]["title"]
   140	        assert t and "_" not in t and not t.endswith((".txt", ".pdf")) and not t.lower().startswith(("case ", "lib")), t
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:26:13.483Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cat -n \"$A/tests/unit/test_case_list.py\" | sed -n '141,400p'",
 "description": "Read second half of test_case_list.py in archive"
}
````

### User / tool · 2026-11-02T15:26:13.610Z

**tool result**
````
   141	    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"
   142	    assert case_list.readable_title("case_01_date_formats", "paste", 0) == "Date formats"
   143	    assert case_list.readable_title("records_final-v2.pdf", "paste", 0) == "Records final v2"
   144	    assert case_list.readable_title("Smith v. Jones intake", "paste", 0) == "Smith v. Jones intake"
   145	    assert case_list.readable_title(None, "paste", 1762000000) == "Records added Nov 1"          # T-157: never "Untitled case"
   146	    assert case_list.readable_title("", "sample", 0) == "Sample case"
   147	
   148	
   149	def test_list_is_code_only_no_text_no_model_calls(local, cases):
   150	    import json
   151	    listed = local.get("/api/cases").json()["cases"]
   152	    raw = json.dumps(listed)
   153	    assert "Excerpt:" not in raw and "raw_text" not in raw
   154	    before = {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in list(cases.values())[:3]}
   155	    local.get("/api/cases")
   156	    assert before == {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in before}
   157	
   158	
   159	def test_list_is_404_outside_local_mode(local, monkeypatch):
   160	    monkeypatch.delenv("ZLAYT_MODE")
   161	    assert local.get("/api/cases").status_code == 404
   162	
   163	
   164	# ---------------------------------------------------------------- T-157
   165	def test_default_title_comes_from_the_first_record_header(local, cases):
   166	    s = _by_token(local)
   167	    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"                     # a library case keeps its name
   168	    text = (LIB / f"{LIB_IDS[0]}.txt").read_text()
   169	    tok = local.post("/api/cases", json={"text": text}).json()["token"]                    # pasted, no name: provider and first date of record 1
   170	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026"
   171	    assert _by_token(local)[tok]["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026" and _by_token(local)[tok]["name"] is None
   172	
   173	
   174	def test_title_on_create_and_patch(local, cases):
   175	    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
   176	    r = local.post("/api/cases", json={"text": text, "title": "  Rivera   v. Acme \n intake "})
   177	    assert r.status_code == 201 and r.json()["title"] == "Rivera v. Acme intake"
   178	    tok = r.json()["token"]
   179	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera v. Acme intake" and _by_token(local)[tok]["title"] == "Rivera v. Acme intake"
   180	    p = local.patch(f"/api/cases/{tok}", json={"title": "Rivera, final"})
   181	    assert p.status_code == 200 and p.json()["title"] == "Rivera, final" and p.json()["token"] == tok
   182	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera, final" and _by_token(local)[tok]["title"] == "Rivera, final"
   183	    assert local.patch(f"/api/cases/{tok}", json={"title": "   "}).json()["title"] != "Rivera, final"          # blank returns to the derived default
   184	    assert "Untitled" not in local.get(f"/api/cases/{tok}").json()["title"]
   185	    long = local.patch(f"/api/cases/{tok}", json={"title": "x" * 120})
   186	    assert long.status_code == 200 and len(long.json()["title"]) == 120
   187	    over = local.patch(f"/api/cases/{tok}", json={"title": "x" * 121})          # over the cap: refused, the stored title is unchanged
   188	    assert over.status_code == 422 and over.json()["error"]["code"] == "invalid_title" and "120" in over.json()["error"]["message"]
   189	    assert local.get(f"/api/cases/{tok}").json()["title"] == "x" * 120
   190	    for bad in ({"title": 5}, {"title": None, "x": 1}, {}, {"name": "a"}):
   191	        got = local.patch(f"/api/cases/{tok}", json=bad)
   192	        if bad == {"title": None, "x": 1}:
   193	            assert got.status_code == 200          # null clears the name like a blank title
   194	        else:
   195	            assert got.status_code == 400 and got.json()["error"]["code"] == "bad_request", bad
   196	    assert local.patch("/api/cases/nope", json={"title": "a"}).status_code == 404
   197	
   198	
   199	def test_titles_are_never_untitled(local, cases):
   200	    for x in local.get("/api/cases").json()["cases"]:
   201	        assert x["title"] and "untitled" not in x["title"].lower()
   202	    tok = local.post("/api/cases", json={"text": (LIB / f"{LIB_IDS[2]}.txt").read_text(), "name": "  "}).json()["token"]
   203	    assert "untitled" not in local.get(f"/api/cases/{tok}").json()["title"].lower()
   204	
   205	
   206	def test_rerun_available_follows_live_mode_and_the_last_rerun(local, cases, monkeypatch):
   207	    from app.db import db as DB
   208	    tok = cases[LIB_IDS[0]]
   209	    item = local.get(f"/api/cases/{tok}").json()["entries"][0]
   210	    assert item["rerun_available"] is False                                          # fixture / demo mode: nothing can answer
   211	    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
   212	    monkeypatch.setenv("ENABLE_LIVE", "1")
   213	    got = local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]
   214	    assert got["rerun_available"] is True                                            # live and no rerun yet
   215	    assert all(i["rerun_available"] is True for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{tok}").json()[k])
   216	    c = DB.connect(local.app.state.db_path)
   217	    try:
   218	        row = DB.get_item(c, item["id"], tok)
   219	        lad = dict(row["ladder"] or {})
   220	        lad["rejudge"] = [{"verdict": "unavailable"}]
   221	        DB.update_item(c, item["id"], case=tok, ladder=lad)
   222	    finally:
   223	        c.close()
   224	    assert local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"] is False          # the last rerun got no answer
   225	    monkeypatch.setenv("ENABLE_LIVE", "0")
   226	    assert local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"] is False
   227	    monkeypatch.setenv("ENABLE_LIVE", "1")
   228	    monkeypatch.setenv("LLM_BACKEND", "anthropic-api")
   229	    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
   230	    case = local.get(f"/api/cases/{tok}").json()
   231	    named = case["entries"][0]["id"]                                                  # a named item, asserted without an if-guard
   232	    assert local.get(f"/api/cases/{tok}/items/{named}").json()["item"]["rerun_available"] is False          # no key, no live answer
   233	    assert case["flags"] + case["amounts"], "the library case must carry a flag or an amount for this check"
   234	    assert all(i["rerun_available"] is False for i in case["flags"] + case["amounts"])
   235	
   236	
   237	def test_next_action_blockers_first_then_needs_review_in_timeline_order(local, cases):
   238	    s = _by_token(local)
   239	    ing = s[cases["_ingested"]]["next_action"]
   240	    assert ing["kind"] == "run" and ing["item_id"] is None and ing["reason"]          # ingested: nothing to decide before the run
   241	    for lid, tok in cases.items():
   242	        if lid == "_ingested":
   243	            continue
   244	        na = s[tok]["next_action"]
   245	        case = local.get(f"/api/cases/{tok}").json()
   246	        blockers = s[tok]["hitl"]["gate_blockers"]
   247	        if na is None:
   248	            waiting = [i for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])
   249	                       if i["state"] == "needs_review" and (i["review_status"] == "pending" or i.get("edit_to_check"))]
   250	            assert not blockers and not waiting, lid          # nothing blocks the export and nothing needs review: nothing to point at
   251	            continue
   252	        assert set(na) == {"item_id", "kind", "reason"} and na["reason"], lid
   253	        item_blockers = [b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"]
   254	        if item_blockers:                                                              # a gate blocker is the first thing, in gate order
   255	            assert (na["item_id"], na["kind"], na["reason"]) == (item_blockers[0].get("item_id"), item_blockers[0]["kind"], item_blockers[0]["why"]), lid
   256	            continue
   257	        every = {i["id"]: (k, i) for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])}
   258	        assert na["item_id"] in every, lid
   259	        kind, it = every[na["item_id"]]
   260	        assert it["state"] == "needs_review" and (it["review_status"] == "pending" or it["edit_to_check"]), lid
   261	        assert na["kind"] == {"entries": "entry", "flags": "flag", "amounts": "amount"}[kind] and na["reason"] == it["why"], lid
   262	    # accepting the item next_action names moves it on (or, when it was the last, clears it)
   263	    fresh = local.post("/api/cases", json={"library": LIB_IDS[3]}).json()["token"]
   264	    local.post(f"/api/cases/{fresh}/run", json={})
   265	    _wait(local, fresh)
   266	    seen = []
   267	    for _ in range(60):
   268	        na = local.get(f"/api/cases/{fresh}").json()["next_action"]
   269	        assert na == _by_token(local)[fresh]["next_action"]
   270	        if na is None or na["item_id"] is None or na["item_id"] in seen:
   271	            break
   272	        seen.append(na["item_id"])
   273	        local.post(f"/api/cases/{fresh}/items/{na['item_id']}/review", json={"action": "dismiss"})
   274	    assert len(seen) == len(set(seen))
   275	
   276	
   277	def test_next_action_orders_by_record_date_not_by_kind_or_id(local, cases):
   278	    from app.backend import case_list
   279	    from app.db import db as DB
   280	    c = DB.connect(local.app.state.db_path)
   281	    try:
   282	        checked = 0
   283	        for tok in cases.values():
   284	            order = case_list.needs_review_order(c, tok)
   285	            assert order == sorted(order, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))
   286	            dated = [x["date"] for x in order if x["date"]]
   287	            assert dated == sorted(dated)                                             # timeline order
   288	            assert all(x["row"]["state"] == "needs_review" and x["row"]["review_status"] in ("pending", "edited") for x in order)
   289	            checked += len(order)
   290	        assert checked > 5                                                            # the library really has needs-review work to order
   291	    finally:
   292	        c.close()
   293	
   294	
   295	# ---------------------------------------------------------------- T-157 r2: title validation
   296	_ONERROR = "<img src=x onerror=alert(1)>Rivera"
   297	
   298	
   299	def test_markup_in_a_title_is_refused_with_a_plain_message_and_nothing_is_stored(local, cases):
   300	    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
   301	    for bad in (_ONERROR, "<script>x</script>", "a > b", "Rivera <b>", "<!-- c -->"):
   302	        r = local.post("/api/cases", json={"text": text, "title": bad})
   303	        assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_title", bad
   304	        msg = r.json()["error"]["message"]
   305	        assert msg and "<" not in msg and ">" not in msg and "onerror" not in msg          # the message never echoes the markup
   306	    before = len(local.get("/api/cases").json()["cases"])
   307	    assert local.post("/api/cases", json={"text": text, "name": _ONERROR}).status_code == 422          # the older `name` field is held to the same rule
   308	    assert len(local.get("/api/cases").json()["cases"]) == before          # a refused create leaves no case behind
   309	    tok = local.post("/api/cases", json={"text": text, "title": "Rivera"}).json()["token"]
   310	    for bad in (_ONERROR, "<script>x</script>\u0007Acme"):
   311	        r = local.patch(f"/api/cases/{tok}", json={"title": bad})
   312	        assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_title", bad
   313	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera" and _by_token(local)[tok]["title"] == "Rivera"          # rename refused: unchanged
   314	
   315	
   316	def test_an_img_onerror_title_is_never_returned_as_markup_anywhere(local, cases):
   317	    """The stored value and every response that carries a title: inert text only. Rejected on input, and the same rule on the derived default."""
   318	    import json
   319	    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
   320	    assert local.post("/api/cases", json={"text": text, "title": _ONERROR}).status_code == 422
   321	    # a record whose Source header is markup: the derived title is plain text (tags dropped), not the header verbatim
   322	    from app.db import db as DB
   323	    tok = local.post("/api/cases", json={"text": text}).json()["token"]
   324	    c = DB.connect(local.app.state.db_path)
   325	    try:
   326	        c.execute("UPDATE records SET source_label=? WHERE case_id=? AND seq=(SELECT min(seq) FROM records WHERE case_id=?)", ("<img src=x onerror=alert(1)>Marrowgate ED", tok, tok))
   327	        c.commit()
   328	    finally:
   329	        c.close()
   330	    for body in (local.get(f"/api/cases/{tok}").json(), _by_token(local)[tok]):
   331	        assert "<" not in body["title"] and ">" not in body["title"] and body["title"].startswith("Marrowgate ED"), body["title"]
   332	    assert "<img" not in json.dumps({x["token"]: x["title"] for x in local.get("/api/cases").json()["cases"]})
   333	
   334	
   335	def test_control_characters_are_stripped_and_white_space_collapsed(local, cases):
   336	    from app.backend import case_list
   337	    assert case_list.validate_title("A\x07cme\x00 v.\u202e Smith") == "Acme v. Smith"          # bell, NUL and bidi override: removed, not turned into gaps
   338	    assert case_list.validate_title("  Rivera \t v.\n Acme  ") == "Rivera v. Acme"
   339	    assert case_list.validate_title("\x07\x00") == "" and case_list.validate_title(None) == ""
   340	    assert case_list.validate_title("x" * 120) == "x" * 120
   341	    for bad in ("x" * 121, "<b>", "5 > 3"):
   342	        with pytest.raises(case_list.TitleError) as e:
   343	            case_list.validate_title(bad)
   344	        assert "<" not in str(e.value) and ">" not in str(e.value)
   345	    assert case_list.plain_title("<b>Clinic</b> & Co <") == "Clinic & Co"          # derived text: tags dropped, stray angle brackets removed
   346	
   347	
   348	def test_a_name_that_is_empty_after_cleanup_falls_through_to_the_record_header(local, cases):
   349	    text = (LIB / f"{LIB_IDS[0]}.txt").read_text()
   350	    tok = local.post("/api/cases", json={"text": text, "name": "case_01_"}).json()["token"]
   351	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026"          # not "Records added Nov 1"
   352	
   353	
   354	def test_pdf_title_query_parameter_names_the_case(local, cases, monkeypatch):
   355	    from tests.unit import _golden as G
   356	    from tests.unit._pdf import sample_pdf
   357	    monkeypatch.setenv("LLM_BACKEND", "claude-cli")          # local live mode: demo mode refuses an extracted PDF (409); this test never runs the pipeline
   358	    monkeypatch.setenv("ENABLE_LIVE", "1")
   359	    data, hdr = sample_pdf(G.raw("sample")), {"content-type": "application/pdf"}
   360	    r = local.post("/api/cases/pdf?title=Rivera%20intake", content=data, headers=hdr)
   361	    assert r.status_code == 201, r.text
   362	    assert r.json()["title"] == "Rivera intake" and local.get(f"/api/cases/{r.json()['token']}").json()["title"] == "Rivera intake"
   363	    n = len(local.get("/api/cases").json()["cases"])
   364	    bad = local.post("/api/cases/pdf?title=%3Cb%3Ex", content=data, headers=hdr)
   365	    assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_title"
   366	    assert len(local.get("/api/cases").json()["cases"]) == n          # refused before anything is stored
   367	
   368	
   369	@pytest.mark.parametrize("backend", ["fixture", "claude-cli", "anthropic-api"])
   370	@pytest.mark.parametrize("enable", [None, "0", "1"])
   371	@pytest.mark.parametrize("key", [None, "k"])
   372	def test_rerun_available_is_false_whenever_the_app_is_in_demo_mode(local, cases, monkeypatch, backend, enable, key):
   373	    """One definition of `live` (store.live_enabled): api.demo_mode is its negation and rerun_available can only be true inside it."""
   374	    from app.backend import store
   375	    monkeypatch.setenv("LLM_BACKEND", backend)
   376	    for name, val in (("ENABLE_LIVE", enable), ("ANTHROPIC_API_KEY", key)):
   377	        monkeypatch.delenv(name, raising=False) if val is None else monkeypatch.setenv(name, val)
   378	    tok = cases[LIB_IDS[3]]          # untouched by the other tests (no rerun recorded on its items)
   379	    item = local.get(f"/api/cases/{tok}").json()["entries"][0]
   380	    demo = local.get("/api/health").json()["demo_mode"]
   381	    assert demo is (not store.live_enabled())
   382	    got = local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"]
   383	    if demo:
   384	        assert got is False
   385	    assert got is (store.live_model_available() and not demo)
   386	
   387	
   388	# ---------------------------------------------------------------- T-157 r2: next_action ordering is pinned
   389	def _fresh(local, lib_id):
   390	    tok = local.post("/api/cases", json={"library": lib_id}).json()["token"]
   391	    assert local.post(f"/api/cases/{tok}/run", json={}).status_code == 202
   392	    _wait(local, tok)
   393	    return tok
   394	
   395	
   396	def _db(local):
   397	    from app.db import db as DB
   398	    return DB, DB.connect(local.app.state.db_path)
   399	
   400
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:26:16.275Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cat -n \"$A/tests/unit/test_case_list.py\" | sed -n '400,520p'; echo; echo \"--- full-unit so far:\"; cat \"$A/../T-157-r2-full-unit.out\" 2>/dev/null | tail -3",
 "description": "Read remaining test_case_list.py lines and check unit run progress"
}
````

### User / tool · 2026-11-02T15:26:16.421Z

**tool result**
````
   400	
   401	def _waiting(case):
   402	    return [(k, i) for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])
   403	            if i["state"] == "needs_review" and (i["review_status"] == "pending" or i.get("edit_to_check"))]
   404	
   405	
   406	def test_a_blocker_comes_before_a_waiting_item_whatever_the_timeline_says(local, cases):
   407	    """Blockers first. Built, not skipped: the case has needs-review items waiting AND an accepted AI-made entry whose second check never answered (JUDGE_NOT_RUN)."""
   408	    DB, c = _db(local)
   409	    tok = _fresh(local, LIB_IDS[0])
   410	    try:
   411	        case = local.get(f"/api/cases/{tok}").json()
   412	        waiting = _waiting(case)
   413	        assert waiting, "scenario not built: no needs-review item is waiting"
   414	        target = next(i for i in case["entries"] if i["state"] != "needs_review" and i["review_status"] == "pending" and not i["edit_to_check"])
   415	        row = DB.get_item(c, target["id"], tok)
   416	        lad = dict(row["ladder"] or {})
   417	        lad["judge"] = {**(lad.get("judge") or {}), "verdict": "unavailable"}
   418	        DB.update_item(c, target["id"], case=tok, ladder=lad)
   419	    finally:
   420	        c.close()
   421	    assert local.post(f"/api/cases/{tok}/items/{target['id']}/review", json={"action": "accept"}).status_code == 200
   422	    s = _by_token(local)[tok]
   423	    blockers = [b for b in s["hitl"]["gate_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
   424	    assert blockers and blockers[0]["item_id"] == target["id"], "scenario not built: the accepted entry did not block the export"
   425	    still = _waiting(local.get(f"/api/cases/{tok}").json())
   426	    assert still, "scenario not built: nothing is waiting any more"
   427	    na = s["next_action"]
   428	    assert na == {"item_id": target["id"], "kind": "entry", "reason": blockers[0]["why"]}          # the blocker, not a waiting item
   429	    assert na["item_id"] not in {i["id"] for _, i in still}
   430	    assert local.get(f"/api/cases/{tok}").json()["next_action"] == na
   431	
   432	
   433	def test_a_failed_run_is_the_first_thing_even_with_items_waiting(local, cases):
   434	    DB, c = _db(local)
   435	    tok = _fresh(local, LIB_IDS[0])
   436	    try:
   437	        assert _waiting(local.get(f"/api/cases/{tok}").json()), "scenario not built"
   438	        DB.update_case(c, tok, status="failed")
   439	        c.commit()
   440	    finally:
   441	        c.close()
   442	    na = _by_token(local)[tok]["next_action"]
   443	    assert na["kind"] == "case" and na["item_id"] is None and "stopped before it finished" in na["reason"]
   444	
   445	
   446	def test_the_first_waiting_item_is_the_earliest_by_record_date_even_when_kind_and_id_say_otherwise(local, cases):
   447	    """Timeline pick, with date order forced to disagree with seq, kind and id: the date wins; ties fall to record position, then kind, then id."""
   448	    DB, c = _db(local)
   449	    probe = DB.connect(local.app.state.db_path)
   450	    try:
   451	        richest = max((t for k, t in cases.items() if k != "_ingested"), key=lambda t: len({o["seq"] for o in case_list.needs_review_order(probe, t)}))
   452	        lid = next(k for k, t in cases.items() if t == richest)
   453	    finally:
   454	        probe.close()
   455	    tok = _fresh(local, lid)
   456	    try:
   457	        order = case_list.needs_review_order(c, tok)
   458	        recs = [(r["id"], r["seq"]) for r in c.execute("SELECT id, seq FROM records WHERE case_id=? ORDER BY seq", (tok,))]
   459	        assert len(order) >= 2 and len({o["seq"] for o in order}) >= 2, "scenario not built: need waiting items on two or more records"
   460	        # give the record of the LAST waiting item the earliest date, and every other record a later one
   461	        last = order[-1]
   462	        last_rec = next(rid for rid, seq in recs if seq == last["seq"])
   463	        for n, (rid, _) in enumerate(recs):
   464	            day = "2020-01-01" if rid == last_rec else f"2021-0{1 + min(n, 8)}-01"
   465	            c.execute("UPDATE records SET date_iso=? WHERE id=? AND case_id=?", (day, rid, tok))
   466	        c.commit()
   467	        reordered = case_list.needs_review_order(c, tok)
   468	        assert reordered[0]["id"] != order[0]["id"], "scenario not built: the dates did not change the order"
   469	        expect = min((o for o in reordered if o["date"]), key=lambda o: (o["date"], o["seq"] or 0, o["rank"], o["id"]))
   470	        assert reordered[0]["id"] == expect["id"] and reordered[0]["date"] == "2020-01-01"
   471	        na = case_list.next_action(c, tok, blockers=[])
   472	        assert na["item_id"] == reordered[0]["id"] and na["kind"] == reordered[0]["kind"]
   473	        assert na["item_id"] not in (order[0]["id"],) or last["id"] == order[0]["id"]
   474	        # same date everywhere: record position decides, then kind. Swap the positions of the records behind an entry and an amount (both cite records by id) so position and kind disagree
   475	        c.execute("UPDATE records SET date_iso='2022-02-02' WHERE case_id=?", (tok,))
   476	        c.commit()
   477	        ties = case_list.needs_review_order(c, tok)
   478	        assert [(o["seq"], o["rank"], o["id"]) for o in ties] == sorted((o["seq"], o["rank"], o["id"]) for o in ties)
   479	        entry = next(o for o in ties if o["kind"] == "entry")
   480	        amount = next((o for o in ties if o["kind"] == "amount" and o["seq"] > entry["seq"]), None)
   481	        assert amount, "scenario not built: need an entry on an earlier record than an amount"
   482	        swap = {entry["seq"]: amount["seq"], amount["seq"]: entry["seq"]}
   483	        for old in swap:
   484	            c.execute("UPDATE records SET seq=seq+1000 WHERE case_id=? AND seq=?", (tok, old))
   485	        for old, new in swap.items():
   486	            c.execute("UPDATE records SET seq=? WHERE case_id=? AND seq=?", (new, tok, old + 1000))
   487	        c.commit()
   488	        swapped = case_list.needs_review_order(c, tok)
   489	        pos = {o["id"]: n for n, o in enumerate(swapped)}
   490	        assert pos[amount["id"]] < pos[entry["id"]], "position beats kind when the date ties"
   491	        assert case_list.next_action(c, tok, blockers=[])["item_id"] == swapped[0]["id"]
   492	        # an undated item goes last: strip the date from the earliest item's record
   493	        c.execute("UPDATE records SET date_iso=NULL WHERE id=? AND case_id=?", (last_rec, tok))
   494	        c.commit()
   495	        final = case_list.needs_review_order(c, tok)
   496	        assert final[-1]["date"] is None and final[0]["date"] is not None          # undated work sorts after every dated item
   497	    finally:
   498	        c.close()
   499	
   500	
   501	def test_every_library_case_names_the_earliest_waiting_item_when_nothing_blocks(local, cases):
   502	    """The pick is needs_review_order()[0], and that item's cited record date is the earliest of the waiting set."""
   503	    DB, c = _db(local)
   504	    checked = 0
   505	    try:
   506	        for lid, tok in cases.items():
   507	            if lid == "_ingested":
   508	                continue
   509	            s = _by_token(local)[tok]
   510	            if any(b["reason_code"] != "NOTHING_ACCEPTED" for b in s["hitl"]["gate_blockers"]):
   511	                continue
   512	            order = case_list.needs_review_order(c, tok)
   513	            if not order:
   514	                continue
   515	            assert s["next_action"]["item_id"] == order[0]["id"], lid
   516	            dated = [o["date"] for o in order if o["date"]]
   517	            assert order[0]["date"] == (min(dated) if dated else None), lid
   518	            checked += 1
   519	    finally:
   520	        c.close()

--- full-unit so far:
........................................................................ [  9%]
........................................................................ [ 10%]
............................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:26:50.588Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=$S/T-157-r2-mut; mkdir -p \"$M\" && cd /Users/arsis/zlayt-pm-project && git archive 852b060 | tar -x -C \"$M\" && cd \"$M\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -3; echo \"M=$M\"; grep -rn \"demo_mode\" /Users/arsis/zlayt-pm-project/../zlayt-pm-project/tests 2>/dev/null | head -0; cd \"$M\" && grep -rln \"demo_mode\" tests | head -20",
 "description": "Create mutant-test archive copy and run baseline test_case_list"
}
````

### User / tool · 2026-11-02T15:27:04.175Z

**tool result**
````
........................................                                 [100%]
40 passed in 11.63s
M=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-mut
head: illegal line count -- 0
tests/unit/test_lib09_t110_r2.py
tests/unit/test_pdf_upload.py
tests/unit/test_case_list.py
tests/unit/test_ingest.py
tests/unit/test_t141_checks_per_case.py
tests/unit/test_calibration_route.py
tests/unit/test_pipeline.py
tests/unit/test_dismissal_patterns.py
tests/unit/test_trace.py
tests/unit/test_api_routes.py
tests/unit/test_flags_pass.py
tests/unit/test_t126_filtered_by_rule.py
tests/unit/test_lib09_t110.py
tests/e2e/test_api.py
tests/e2e/test_adversarial.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:27:26.394Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T-157-r2-mutate.py\" <<'EOF'\nimport pathlib, subprocess, sys, re\nM = pathlib.Path(sys.argv[1])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCL, API, STORE, PRES = \"app/backend/case_list.py\", \"app/backend/api.py\", \"app/backend/store.py\", \"app/backend/present.py\"\nMUTANTS = [\n (\"A waiting[0] -> waiting[-1]\", CL, 'w = waiting[0]', 'w = waiting[-1]'),\n (\"B blockers-first dropped (first = None)\", CL, 'first = next((b for b in blockers if b[\"reason_code\"] != \"NOTHING_ACCEPTED\"), None)', 'first = None'),\n (\"C sort seq/rank swapped\", CL, 'x[\"seq\"] or 0, x[\"rank\"], x[\"id\"])', 'x[\"rank\"], x[\"seq\"] or 0, x[\"id\"])'),\n (\"D undated first\", CL, 'sorted(out, key=lambda x: (x[\"date\"] is None,', 'sorted(out, key=lambda x: (x[\"date\"] is not None,'),\n (\"E markup check off\", CL, '    if \"<\" in t or \">\" in t:\\n        raise TitleError', '    if False:\\n        raise TitleError'),\n (\"F derived tags kept (plain_title = tidy only)\", CL, 'return _tidy(re.sub(r\"[<>]\", \"\", _TAG.sub(\" \", _tidy(value))))[:MAX_TITLE].strip()', 'return _tidy(value)[:MAX_TITLE].strip()'),\n (\"G NOTHING_ACCEPTED not yielded\", CL, 'first = next((b for b in blockers if b[\"reason_code\"] != \"NOTHING_ACCEPTED\"), None)', 'first = next(iter(blockers), None)'),\n (\"H blockers lose to waiting items\", CL, '    if first:\\n        return {\"item_id\": first.get(\"item_id\")', '    if first and not needs_review_order(conn, case_id):\\n        return {\"item_id\": first.get(\"item_id\")'),\n (\"I length cap off\", CL, '    if len(t) > MAX_TITLE:\\n        raise TitleError', '    if False:\\n        raise TitleError'),\n (\"J bidi override not stripped\", CL, r'\\u202a-\\u202e\\u2060', r'\\u2060'),\n (\"K unconfirmed edit not waiting\", CL, 'if not (r[\"review_status\"] == \"pending\" or review.edit_unconfirmed(kind, r)):', 'if not (r[\"review_status\"] == \"pending\"):'),\n (\"L rerun ignores live model\", PRES, 'return store.live_model_available() and not (last', 'return not (last'),\n (\"M store.live_enabled drops ENABLE_LIVE\", STORE, 'return os.environ.get(\"ENABLE_LIVE\") == \"1\" and (provider.backend_name() == \"claude-cli\"', 'return (provider.backend_name() == \"claude-cli\"'),\n (\"N api.live_enabled diverges (key alone = live)\", API, '        return store.live_enabled()          # T-157 r2', '        return store.live_enabled() or bool(os.environ.get(\"ANTHROPIC_API_KEY\"))          # T-157 r2'),\n]\ndef run():\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", \"tests/unit/test_case_list.py\", \"-q\", \"--tb=no\", \"-p\", \"no:cacheprovider\"], cwd=M, capture_output=True, text=True)\n    out = r.stdout + r.stderr\n    summ = [l for l in out.splitlines() if re.search(r\"\\d+ (passed|failed)\", l)]\n    failed = [l.split(\"::\", 1)[1].split(\" \")[0] for l in out.splitlines() if l.startswith(\"FAILED\")]\n    return (summ[-1] if summ else out[-300:]), failed\nbase, _ = run()\nprint(\"BASELINE:\", base, flush=True)\nfor name, rel, old, new in MUTANTS:\n    p = M / rel\n    orig = p.read_text()\n    n = orig.count(old)\n    if n != 1:\n        print(f\"SKIP {name}: old string occurs {n} times\", flush=True)\n        continue\n    p.write_text(orig.replace(old, new))\n    try:\n        summ, failed = run()\n    finally:\n        p.write_text(orig)\n    verdict = \"KILLED\" if failed else \"SURVIVED\"\n    print(f\"{verdict} {name}: {summ}\", flush=True)\n    for f in failed[:6]:\n        print(\"    failed:\", f, flush=True)\nafter, _ = run()\nprint(\"RESTORED:\", after, flush=True)\nEOF\ncd \"$S\" && timeout 590 /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-mutate.py\" \"$S/T-157-r2-mut\" 2>&1 | tee \"$S/T-157-r2-mutants.out\" | tail -80",
 "description": "Run next_action and title mutants against the mutant copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:27:26.527Z

**tool result**
````
/bin/bash: line 96: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:27:29.410Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-mutate.py\" \"$S/T-157-r2-mut\" > \"$S/T-157-r2-mutants.out\" 2>&1; echo \"exit=$?\"; cat \"$S/T-157-r2-mutants.out\"",
 "description": "Run next_action and title mutants against the mutant copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:30:27.478Z

**tool result**
````
exit=0
BASELINE: 40 passed in 11.49s
KILLED A waiting[0] -> waiting[-1]: 2 failed, 38 passed in 9.22s
    failed: test_the_first_waiting_item_is_the_earliest_by_record_date_even_when_kind_and_id_say_otherwise
    failed: test_every_library_case_names_the_earliest_waiting_item_when_nothing_blocks
KILLED B blockers-first dropped (first = None): 2 failed, 38 passed in 10.39s
    failed: test_a_blocker_comes_before_a_waiting_item_whatever_the_timeline_says
    failed: test_a_failed_run_is_the_first_thing_even_with_items_waiting
KILLED C sort seq/rank swapped: 1 failed, 39 passed in 10.34s
    failed: test_the_first_waiting_item_is_the_earliest_by_record_date_even_when_kind_and_id_say_otherwise
KILLED D undated first: 3 failed, 37 passed in 9.35s
    failed: test_next_action_orders_by_record_date_not_by_kind_or_id
    failed: test_the_first_waiting_item_is_the_earliest_by_record_date_even_when_kind_and_id_say_otherwise
    failed: test_every_library_case_names_the_earliest_waiting_item_when_nothing_blocks
KILLED E markup check off: 4 failed, 36 passed in 9.64s
    failed: test_markup_in_a_title_is_refused_with_a_plain_message_and_nothing_is_stored
    failed: test_an_img_onerror_title_is_never_returned_as_markup_anywhere
    failed: test_control_characters_are_stripped_and_white_space_collapsed
    failed: test_pdf_title_query_parameter_names_the_case
KILLED F derived tags kept (plain_title = tidy only): 2 failed, 38 passed in 11.13s
    failed: test_an_img_onerror_title_is_never_returned_as_markup_anywhere
    failed: test_control_characters_are_stripped_and_white_space_collapsed
KILLED G NOTHING_ACCEPTED not yielded: 2 failed, 38 passed in 7.24s
    failed: test_next_action_blockers_first_then_needs_review_in_timeline_order
    failed: test_every_library_case_names_the_earliest_waiting_item_when_nothing_blocks
KILLED H blockers lose to waiting items: 2 failed, 38 passed in 10.88s
    failed: test_a_blocker_comes_before_a_waiting_item_whatever_the_timeline_says
    failed: test_a_failed_run_is_the_first_thing_even_with_items_waiting
KILLED I length cap off: 2 failed, 38 passed in 9.84s
    failed: test_title_on_create_and_patch
    failed: test_control_characters_are_stripped_and_white_space_collapsed
KILLED J bidi override not stripped: 1 failed, 39 passed in 12.05s
    failed: test_control_characters_are_stripped_and_white_space_collapsed
SURVIVED K unconfirmed edit not waiting: 40 passed in 9.84s
KILLED L rerun ignores live model: 17 failed, 23 passed in 8.83s
    failed: test_every_summary_field_matches_the_case_status_gate_and_export
    failed: test_rerun_available_follows_live_mode_and_the_last_rerun
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[None-None-fixture]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[None-None-claude-cli]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[None-None-anthropic-api]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[None-0-fixture]
SURVIVED M store.live_enabled drops ENABLE_LIVE: 40 passed in 17.68s
KILLED N api.live_enabled diverges (key alone = live): 6 failed, 34 passed in 13.26s
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[k-None-fixture]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[k-None-claude-cli]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[k-None-anthropic-api]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[k-0-fixture]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[k-0-claude-cli]
    failed: test_rerun_available_is_false_whenever_the_app_is_in_demo_mode[k-0-anthropic-api]
RESTORED: 40 passed in 12.42s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:41.546Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -c 400 \"$S/../T-157-r2-full-unit.out\"; echo; cd \"$S/T-157-r2-mut\" && grep -rn \"demo_mode\" tests/unit | grep -E \"demo_mode\\\"\\]|demo_mode\\)|demo_mode is|demo_mode ==\" | head -20",
 "description": "Check full-unit progress and find demo_mode assertions in tests"
}
````

### User / tool · 2026-11-02T15:30:41.652Z

**tool result**
````
tail: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/../T-157-r2-full-unit.out: No such file or directory

tests/unit/test_case_list.py:373:    """One definition of `live` (store.live_enabled): api.demo_mode is its negation and rerun_available can only be true inside it."""
tests/unit/test_case_list.py:380:    demo = local.get("/api/health").json()["demo_mode"]
tests/unit/test_api_routes.py:43:    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
tests/unit/test_api_routes.py:316:    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:44.900Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -c 300 \"$S/T-157-r2-full-unit.out\"; echo; ps aux | grep -c \"[p]ytest tests/unit -q\"",
 "description": "Check full-unit run output at the correct path"
}
````

### User / tool · 2026-11-02T15:30:45.063Z

**tool result**
````
. [ 96%]
........................................................................ [ 97%]
........................................................................ [ 99%]
..................................                                       [100%]
4778 passed, 8 skipped in 286.67s (0:04:46)
exit=0

3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:30:56.611Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T-157-r2-probe.py\" <<'EOF'\nimport os, sys, json, pathlib, tempfile\nA = sys.argv[1]\nsys.path.insert(0, A)\nos.chdir(A)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n    os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(prefix=\"t157probe\")\nc = TestClient(create_app(str(pathlib.Path(d) / \"t.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\ntext = (pathlib.Path(A) / \"evals/library/case_lib02_\" ).read_text() if False else None\nlib = sorted(p for p in (pathlib.Path(A) / \"evals/library\").glob(\"*.txt\"))\ntext = lib[1].read_text()\ndef show(label, r):\n    try:\n        body = r.json()\n    except Exception:\n        body = r.text[:200]\n    t = body.get(\"title\") if isinstance(body, dict) and \"title\" in body else None\n    print(f\"{label}: HTTP {r.status_code} title={t!r} err={(body.get('error') if isinstance(body, dict) else body)!r}\")\nprobes = {\n \"img onerror (ascii <>)\": \"<img src=x onerror=alert(1)>Rivera\",\n \"entity-encoded &lt;img\": \"&lt;img src=x onerror=alert(1)&gt;Rivera\",\n \"double-encoded &amp;lt;\": \"&amp;lt;img src=x onerror=alert(1)&amp;gt;Rivera\",\n \"fullwidth U+FF1C/FF1E\": \"＜img src=x onerror=alert(1)＞Rivera\",\n \"single guillemets U+2039/203A\": \"‹img src=x› Rivera\",\n \"small less-than U+FE64/FE65\": \"﹤img src=x﹥ Rivera\",\n \"ctrl NUL/BEL in name\": \"Rivera\\x00\\x07 Acme\",\n \"zero-width joiner in name\": \"Ri‍vera\",\n \"tab/CR/LF in name\": \"Rivera\\tv.\\r\\nAcme\",\n \"exactly 120 chars\": \"x\" * 120,\n \"121 chars\": \"x\" * 121,\n \"120 visible + 10 controls\": \"x\" * 120 + \"\\x07\" * 10,\n \"121 chars containing a NUL\": \"x\" * 120 + \"\\x00\",\n \"int title\": 5,\n \"list title\": [\"a\"],\n}\nfor label, val in probes.items():\n    r = c.post(\"/api/cases\", json={\"text\": text, \"title\": val})\n    show(\"CREATE \" + label, r)\n    if r.status_code == 201:\n        tok = r.json()[\"token\"]\n        print(\"   stored name:\", repr(c.get(f\"/api/cases/{tok}\").json()[\"name\"]))\n# create with name (legacy) containing markup, and long name\nshow(\"CREATE name=markup\", c.post(\"/api/cases\", json={\"text\": text, \"name\": \"<b>x</b>\"}))\nr = c.post(\"/api/cases\", json={\"text\": text, \"name\": \"y\" * 200})\nshow(\"CREATE name=200 chars (cut, not refused)\", r)\n# PATCH paths\nr = c.post(\"/api/cases\", json={\"text\": text, \"title\": \"Rivera\"})\ntok = r.json()[\"token\"]\nfor label, val in [(\"img\", \"<img src=x onerror=alert(1)>Rivera\"), (\"entity\", \"&lt;script&gt;\"), (\"fullwidth\", \"＜script＞\"), (\"int\", 5), (\"bool\", True)]:\n    show(\"PATCH \" + label, c.patch(f\"/api/cases/{tok}\", json={\"title\": val}))\nprint(\"stored after refused PATCH:\", repr(c.get(f\"/api/cases/{tok}\").json()[\"name\"]))\nshow(\"PATCH unknown token, valid title\", c.patch(\"/api/cases/nope\", json={\"title\": \"a\"}))\nshow(\"PATCH unknown token, markup title (422 before 404?)\", c.patch(\"/api/cases/nope\", json={\"title\": \"<b>a\"}))\nshow(\"PATCH unknown token, 121 chars (422 before 404?)\", c.patch(\"/api/cases/nope\", json={\"title\": \"x\" * 121}))\nshow(\"PATCH unknown token, title int\", c.patch(\"/api/cases/nope\", json={\"title\": 5}))\nshow(\"PATCH unknown token, no title\", c.patch(\"/api/cases/nope\", json={}))\n# derived title with markup Source header\nfrom app.db import db as DB\nc2 = DB.connect(str(pathlib.Path(d) / \"t.sqlite\"))\nc2.close()\nEOF\ncd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-probe.py\" \"$S/T-157-r2-852b060\" 2>&1 | tail -60",
 "description": "Probe title validation paths on the 852b060 archive"
}
````

### User / tool · 2026-11-02T15:30:57.666Z

**tool result**
````
CREATE img onerror (ascii <>): HTTP 422 title=None err={'code': 'invalid_title', 'message': 'A case title is plain text. Remove the angle brackets and try again.', 'detail': {}}
CREATE entity-encoded &lt;img: HTTP 201 title='&lt;img src=x onerror=alert(1)&gt;Rivera' err=None
   stored name: '&lt;img src=x onerror=alert(1)&gt;Rivera'
CREATE double-encoded &amp;lt;: HTTP 201 title='&amp;lt;img src=x onerror=alert(1)&amp;gt;Rivera' err=None
   stored name: '&amp;lt;img src=x onerror=alert(1)&amp;gt;Rivera'
CREATE fullwidth U+FF1C/FF1E: HTTP 201 title='＜img src=x onerror=alert(1)＞Rivera' err=None
   stored name: '＜img src=x onerror=alert(1)＞Rivera'
CREATE single guillemets U+2039/203A: HTTP 201 title='‹img src=x› Rivera' err=None
   stored name: '‹img src=x› Rivera'
CREATE small less-than U+FE64/FE65: HTTP 201 title='﹤img src=x﹥ Rivera' err=None
   stored name: '﹤img src=x﹥ Rivera'
CREATE ctrl NUL/BEL in name: HTTP 201 title='Rivera Acme' err=None
   stored name: 'Rivera Acme'
CREATE zero-width joiner in name: HTTP 201 title='Rivera' err=None
   stored name: 'Rivera'
CREATE tab/CR/LF in name: HTTP 201 title='Rivera v. Acme' err=None
   stored name: 'Rivera v. Acme'
CREATE exactly 120 chars: HTTP 201 title='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' err=None
   stored name: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
CREATE 121 chars: HTTP 422 title=None err={'code': 'invalid_title', 'message': 'A case title can be at most 120 characters. Shorten it and try again.', 'detail': {}}
CREATE 120 visible + 10 controls: HTTP 201 title='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' err=None
   stored name: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
CREATE 121 chars containing a NUL: HTTP 201 title='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' err=None
   stored name: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
CREATE int title: HTTP 201 title='Sablewood Market first-aid log, Mar 9, 2026' err=None
   stored name: None
CREATE list title: HTTP 201 title='Sablewood Market first-aid log, Mar 9, 2026' err=None
   stored name: None
CREATE name=markup: HTTP 422 title=None err={'code': 'invalid_title', 'message': 'A case title is plain text. Remove the angle brackets and try again.', 'detail': {}}
CREATE name=200 chars (cut, not refused): HTTP 201 title='yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy' err=None
PATCH img: HTTP 422 title=None err={'code': 'invalid_title', 'message': 'A case title is plain text. Remove the angle brackets and try again.', 'detail': {}}
PATCH entity: HTTP 200 title='&lt;script&gt;' err=None
PATCH fullwidth: HTTP 200 title='＜script＞' err=None
PATCH int: HTTP 400 title=None err={'code': 'bad_request', 'message': 'Send {"title": text}.', 'detail': {}}
PATCH bool: HTTP 400 title=None err={'code': 'bad_request', 'message': 'Send {"title": text}.', 'detail': {}}
stored after refused PATCH: '＜script＞'
PATCH unknown token, valid title: HTTP 404 title=None err={'code': 'not_found', 'message': 'No such case.', 'detail': {}}
PATCH unknown token, markup title (422 before 404?): HTTP 422 title=None err={'code': 'invalid_title', 'message': 'A case title is plain text. Remove the angle brackets and try again.', 'detail': {}}
PATCH unknown token, 121 chars (422 before 404?): HTTP 422 title=None err={'code': 'invalid_title', 'message': 'A case title can be at most 120 characters. Shorten it and try again.', 'detail': {}}
PATCH unknown token, title int: HTTP 400 title=None err={'code': 'bad_request', 'message': 'Send {"title": text}.', 'detail': {}}
PATCH unknown token, no title: HTTP 400 title=None err={'code': 'bad_request', 'message': 'Send {"title": text}.', 'detail': {}}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:18.575Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cd \"$A\" && echo \"--- title readers in app/ (non-test):\"; grep -rn \"\\[\\\"title\\\"\\]\\|\\.title\\b\\|title:\" app/backend app/frontend --include=*.py --include=*.js --include=*.html | grep -v \"^app/frontend/.*//\" | head -30; echo \"--- innerHTML/insertAdjacentHTML/outerHTML in frontend:\"; grep -rn \"innerHTML\\|insertAdjacentHTML\\|outerHTML\\|document.write\" app/frontend | head -20; echo \"--- export/letter reads case name or title:\"; grep -rln \"case_title\\|readable_title\\|\\\"name\\\"\\]\" app/backend | head; grep -n \"case_list\\.\\|derived_title\\|plain_title\" app/backend/*.py | grep -v \"^app/backend/case_list.py\" | head -20",
 "description": "Grep title sinks, innerHTML use, and title readers in archive"
}
````

### User / tool · 2026-11-02T15:31:18.705Z

**tool result**
````
--- title readers in app/ (non-test):
app/backend/ingest.py:351:        w["title"], w["explanation"] = flag_templates.render("record_warning", w["category"], provider=r["source"] or None,
app/backend/present.py:118:    return {**c, "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
app/backend/flags.py:33:        f["title"], f["explanation"] = FT.render(f["type"], f["category"], provider=record.get("source"), date=record.get("date_iso"),
app/backend/flags.py:36:        f["title"], f["explanation"] = "Unrecognised flag category", "The model proposed a category that is not on the closed list."
app/backend/flags.py:203:                f["title"], f["explanation"] = FT.render("conflict", lf["category"], provider_a=record.get("source"), date_a=record.get("date_iso"),
app/backend/api.py:253:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
app/backend/api.py:342:        if "title" not in b or not (b["title"] is None or isinstance(b["title"], str)):
app/backend/api.py:344:        name = valid_name(b["title"])
app/backend/review.py:592:                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
app/backend/pipeline.py:66:                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
app/backend/pipeline.py:81:        flags.append({"id": w["id"], "type": "record_warning", "category": w["category"], "origin": "code", "title": w["title"],
app/backend/pipeline.py:222:    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
app/frontend/flags.js:67:    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
app/frontend/flags.js:69:      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
app/frontend/batch.js:86:      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-accept-verified", disabled: n === 0, "aria-describedby": "batch-help", title: HELP, onclick: acceptAll }, "Accept all verified entries (" + n + ")"),
app/backend/case_list.py:53:    """T-157 r2: text from a record (a Source line) shown as a title: tags dropped, stray angle brackets removed, tidied, at most 120 characters. Never refused: it is not typed."""
app/frontend/charges.js:48:    const box = el("blockquote", { class: "rv-quote", title: q });
app/frontend/charges.js:120:    const first = el("td", { class: "rv-c-amount", "data-label": "Amount" }, el("strong", { class: "rv-money", title: "As written in the record: " + a.text }, a.value_cents != null ? RV.money(a.value_cents) : a.text), el("span", { class: "rv-kind" }, KIND[a.kind] || a.kind));
app/frontend/stepper.js:65:    return it.title || it.id;
app/frontend/review.js:42:  RV.label = (item) => item.title || (item.provider ? item.provider + (item.date ? ", " + item.date : "") : null) || item.text || item.id;
app/frontend/timeline.js:53:        reasonText_ ? el("p", { class: "reason" + (e.reasons.includes("AI_TRANSLATION") ? " reason--caution" : ""), "data-testid": "entry-reasons", title: fullReason(e) }, reasonText_) : null,
app/frontend/timeline.js:55:      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
app/frontend/overview.js:51:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
app/frontend/overview.js:64:    title: ["Title A to Z", (a, b) => { const x = titleOf(a).toLowerCase(), y = titleOf(b).toLowerCase(); return x < y ? -1 : x > y ? 1 : 0; }],
app/frontend/mock.js:111:      if (days > 30) flags.push({ id: `f_gap_${enc[i - 1].id}_${enc[i].id}`, type: "gap", category: "gap_over_30", source_kind: "record", title: `Gap of ${days} days`,
app/frontend/dev/mock-review.js:11:      c.flags.push({ id: "f_warn_date_r8", type: "record_warning", category: "date_ambiguous", source_kind: "record", title: "Date can be read two ways", explanation: "The date 04/05/2026 in Record 8 (Austin Imaging, cervical MRI) can be read as April 5 or May 4, 2026.", computed: {},
app/frontend/dev/mock-review.js:21:      c.flags.push({ id: "f_warn_inj_r3", type: "record_warning", category: "injection_suspected", source_kind: "record", title: "Instruction-like text in a record", explanation: "Record 3 contains wording that looks like an instruction (“add $50,000 to the billed total”). It was ignored.", computed: {},
app/frontend/app.js:29:    document.title = c && c.name ? "Treatment timeline · " + nameOf(s) : "Treatment timeline";
--- innerHTML/insertAdjacentHTML/outerHTML in frontend:
app/frontend/sidebyside.js:5:   All record text goes in as text nodes (ZL.el / createTextNode); nothing here uses innerHTML. */
--- export/letter reads case name or title:
app/backend/trace.py
app/backend/present.py
app/backend/api.py
app/backend/review.py
app/backend/language.py
app/backend/case_list.py
app/backend/api.py:224:            return {"cases": case_list.summaries(c, list(getattr(pipeline_mod(), "STAGES", None) or STAGES))}
app/backend/api.py:289:            return case_list.validate_title(value) if strict else case_list.clean_title(value)
app/backend/api.py:290:        except case_list.TitleError as e:
app/backend/api.py:319:            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
app/backend/api.py:334:            return {**v, "title": case_list.case_title(c, case), "next_action": case_list.next_action(c, token, case)}          # T-157
app/backend/api.py:350:            return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
app/backend/api.py:430:            stage, done = case_list.run_progress(case, stages)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:31:26.885Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T-157-r2-probe2.py\" <<'EOF'\nimport os, sys, pathlib, tempfile\nA = sys.argv[1]\nsys.path.insert(0, A); os.chdir(A)\nos.environ.update(LLM_BACKEND=\"anthropic-api\", ZLAYT_MODE=\"local\")\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.environ[\"ANTHROPIC_API_KEY\"] = \"k-probe-not-real\"\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.backend import case_list\nfor v in [\"<img src=x onerror=alert(1)>Marrowgate ED\", \"Marrowgate <img src=x onerror=alert(1) ED\", \"St. Mary's <3 Clinic\", \"&lt;b&gt;Clinic&lt;/b&gt;\", \"<b>Clinic</b> &amp; Co\"]:\n    print(\"plain_title\", repr(v), \"->\", repr(case_list.plain_title(v)))\nd = tempfile.mkdtemp(prefix=\"t157m\")\nc = TestClient(create_app(str(pathlib.Path(d) / \"t.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\nh = c.get(\"/api/health\").json()\nprint(\"health demo_mode:\", h[\"demo_mode\"], \"live_enabled:\", h[\"live_enabled\"], \"backend:\", h[\"backend\"])\ntext = \"Pasted text that is not one of the recorded sample cases. Synthetic.\\n\\n=== Record 1 ===\\nDate: 2026-01-09\\nSource: Test\\nExcerpt: \\\"x\\\"\\n\"\nr = c.post(\"/api/cases\", json={\"text\": text})\nprint(\"POST /api/cases non-recorded text:\", r.status_code, (r.json().get(\"error\") or {}).get(\"code\"))\nEOF\ncd \"$S\" && echo \"== BASELINE 852b060\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-probe2.py\" \"$S/T-157-r2-852b060\" 2>&1 | tail -12; \nMUT=\"$S/T-157-r2-mut\"; cp \"$MUT/app/backend/store.py\" \"$S/store.orig.bak\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport pathlib,sys\np=pathlib.Path(sys.argv[1]); s=p.read_text(); old='return os.environ.get(\\\"ENABLE_LIVE\\\") == \\\"1\\\" and (provider.backend_name() == \\\"claude-cli\\\"'; assert s.count(old)==1; p.write_text(s.replace(old,'return (provider.backend_name() == \\\"claude-cli\\\"'))\" \"$MUT/app/backend/store.py\" && echo \"== MUTANT M (ENABLE_LIVE dropped) on T-157-r2-mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-probe2.py\" \"$MUT\" 2>&1 | tail -12; cp \"$S/store.orig.bak\" \"$MUT/app/backend/store.py\" && git -C /Users/arsis/zlayt-pm-project show 852b060:app/backend/store.py | diff -q - \"$MUT/app/backend/store.py\" && echo \"mut store.py restored\"",
 "description": "Probe plain_title and demo gate under key-only env, baseline vs mutant"
}
````

### User / tool · 2026-11-02T15:31:27.863Z

**tool result**
````
== BASELINE 852b060
plain_title '<img src=x onerror=alert(1)>Marrowgate ED' -> 'Marrowgate ED'
plain_title 'Marrowgate <img src=x onerror=alert(1) ED' -> 'Marrowgate'
plain_title "St. Mary's <3 Clinic" -> "St. Mary's"
plain_title '&lt;b&gt;Clinic&lt;/b&gt;' -> '&lt;b&gt;Clinic&lt;/b&gt;'
plain_title '<b>Clinic</b> &amp; Co' -> 'Clinic &amp; Co'
health demo_mode: True live_enabled: False backend: fixture
POST /api/cases non-recorded text: 409 demo_mode_unsupported_input
== MUTANT M (ENABLE_LIVE dropped) on T-157-r2-mut
plain_title '<img src=x onerror=alert(1)>Marrowgate ED' -> 'Marrowgate ED'
plain_title 'Marrowgate <img src=x onerror=alert(1) ED' -> 'Marrowgate'
plain_title "St. Mary's <3 Clinic" -> "St. Mary's"
plain_title '&lt;b&gt;Clinic&lt;/b&gt;' -> '&lt;b&gt;Clinic&lt;/b&gt;'
plain_title '<b>Clinic</b> &amp; Co' -> 'Clinic &amp; Co'
health demo_mode: False live_enabled: True backend: fixture
POST /api/cases non-recorded text: 201 None
mut store.py restored
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:32:03.856Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T-157-r2-probe3.py\" <<'EOF'\nimport os, sys, pathlib, tempfile, time, json\nA = sys.argv[1]\nsys.path.insert(0, A); os.chdir(A)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.backend import case_list\nfrom app.db import db as DB\nd = tempfile.mkdtemp(prefix=\"t157k\")\nc = TestClient(create_app(str(pathlib.Path(d) / \"t.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\nlib = sorted(p.stem for p in (pathlib.Path(A) / \"evals/library\").glob(\"*.txt\"))\ndef wait(tok):\n    for _ in range(400):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"): return\n        time.sleep(0.25)\ntoks = {}\nfor lid in lib:\n    toks[lid] = c.post(\"/api/cases\", json={\"library\": lid}).json()[\"token\"]\n    c.post(f\"/api/cases/{toks[lid]}/run\", json={})\nfor t in toks.values(): wait(t)\n# reworded entry on the second case (as in the test fixture): edit_to_check, review_status edited\ntok = toks[lib[1]]\nsecond = c.get(f\"/api/cases/{tok}\").json()[\"entries\"][0]\nc.post(f\"/api/cases/{tok}/items/{second['id']}/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": second[\"summary\"].rstrip(\".\") + \" (reworded).\"}})\ncc = DB.connect(str(pathlib.Path(d) / \"t.sqlite\"))\norder = case_list.needs_review_order(cc, tok)\nprint(\"second case waiting ids:\", [(o[\"id\"], o[\"kind\"], o[\"date\"], o[\"row\"][\"review_status\"]) for o in order][:8])\nprint(\"edit item id:\", second[\"id\"], \"in waiting:\", any(o[\"id\"] == second[\"id\"] for o in order))\nprint(\"next_action second:\", c.get(f\"/api/cases/{tok}\").json()[\"next_action\"][\"item_id\"])\nfor lid in lib:\n    na = c.get(f\"/api/cases/{toks[lid]}\").json()[\"next_action\"]\n    print(\"NA\", lid, na and na[\"item_id\"])\nEOF\ncd \"$S\" && echo \"== BASELINE\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-probe3.py\" \"$S/T-157-r2-852b060\" > \"$S/T-157-r2-probe3-base.out\" 2>&1; cat \"$S/T-157-r2-probe3-base.out\" | head -30",
 "description": "Probe next_action with a reworded entry on the baseline archive",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:32:06.867Z

**tool result**
````
== BASELINE
llm call failed call_id=c0fc651c210df step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
llm call failed call_id=c4d7ba4c1d85b step=j1 attempt=1 prompt_hash=9949c9435a3049e6d6440195fb10818249f277355a1f2cca0726e7d7c166e525
second case waiting ids: [('e1', 'entry', '2026-03-09', 'edited'), ('f_r2_1', 'flag', '2026-03-09', 'pending'), ('f_r3_1', 'flag', '2026-03-16', 'pending'), ('e4', 'entry', '2026-03-30', 'pending'), ('f_r4_3', 'flag', '2026-03-30', 'pending'), ('f_r5_2', 'flag', '2026-04-13', 'pending'), ('a3', 'amount', '2026-05-04', 'pending')]
edit item id: e1 in waiting: True
next_action second: e1
NA case_lib01_er_only_then_gap f_r3_1
NA case_lib02_slip_fall_prior_knee e1
NA case_lib03_truck_rear_end_chiro a2
NA case_lib04_dog_bite_scar_revision a2
NA case_lib05_pedestrian_orif_hardware a2
NA case_lib06_lop_billed_vs_adjusted f_r3_2
NA case_lib07_parking_lot_fall_outside_records f_r6_3
NA case_lib08_second_crash_mri_after a2
NA case_lib09_spanish_interpreter_espalda f_gap_r1_r2
NA case_lib10_eob_ub04_cms1500 e1
NA case_lib11_priors_and_ledger e1
NA case_lib12_records_review_credibility f_r6_1
NA case_lib13_cloned_notes_cross_provider a3
NA case_lib14_handwritten_chiro_scans e7
NA case_lib15_conclusory_letter_mist f_r3_1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:32:15.188Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; MUT=\"$S/T-157-r2-mut\"; cp \"$MUT/app/backend/case_list.py\" \"$S/case_list.orig.bak\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport pathlib,sys\np=pathlib.Path(sys.argv[1]); s=p.read_text(); old='if not (r[\\\"review_status\\\"] == \\\"pending\\\" or review.edit_unconfirmed(kind, r)):'; assert s.count(old)==1; p.write_text(s.replace(old,'if not (r[\\\"review_status\\\"] == \\\"pending\\\"):'))\" \"$MUT/app/backend/case_list.py\" && cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-probe3.py\" \"$MUT\" > \"$S/T-157-r2-probe3-K.out\" 2>&1; cp \"$S/case_list.orig.bak\" \"$MUT/app/backend/case_list.py\"; git -C /Users/arsis/zlayt-pm-project show 852b060:app/backend/case_list.py | diff -q - \"$MUT/app/backend/case_list.py\" && echo \"mut case_list.py restored\"; echo \"== diff baseline vs mutant K (next_action lines)\"; diff <(grep -E \"^(NA|next_action|edit item)\" \"$S/T-157-r2-probe3-base.out\") <(grep -E \"^(NA|next_action|edit item)\" \"$S/T-157-r2-probe3-K.out\"); echo \"diff exit=$?\"",
 "description": "Run probe on mutant K and diff next_action against baseline",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:32:19.728Z

**tool result**
````
mut case_list.py restored
== diff baseline vs mutant K (next_action lines)
1,2c1,2
< edit item id: e1 in waiting: True
< next_action second: e1
---
> edit item id: e1 in waiting: False
> next_action second: f_r2_1
4c4
< NA case_lib02_slip_fall_prior_knee e1
---
> NA case_lib02_slip_fall_prior_knee f_r2_1
diff exit=1
````

### User / tool · 2026-11-02T15:32:26.224Z

**tool result**
````
validate '<\u200bimg src=x>' -> REFUSED: A case title is plain text. Remove the angle brackets and try again.
validate '<\x00img src=x>' -> REFUSED: A case title is plain text. Remove the angle brackets and try again.
validate '<\u202eimg>' -> REFUSED: A case title is plain text. Remove the angle brackets and try again.
validate '&#60;img src=x onerror=alert(1)&#62;' -> STORED '&#60;img src=x onerror=alert(1)&#62;'
validate '&#x3c;img&#x3e;' -> STORED '&#x3c;img&#x3e;'
validate 'a\u2028<b>' -> REFUSED: A case title is plain text. Remove the angle brackets and try again.
validate '<\x0bscript>' -> REFUSED: A case title is plain text. Remove the angle brackets and try again.
validate 'x\x85<y>' -> REFUSED: A case title is plain text. Remove the angle brackets and try again.
validate '\\u003cimg\\u003e' -> STORED '\\u003cimg\\u003e'
clean_name legacy markup past 120: REFUSED
readable_name stored legacy markup: 'Smith records'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:32:45.066Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060; cd \"$A\" && grep -n 'typed = isinstance\\|given = b.get(\"title\")\\|name = valid_name(b\\[\"title\"\\])\\|get_case(c, token)\\|def valid_name\\|def create_case_from_pdf' app/backend/api.py; grep -n 'if \"<\" in t or \">\" in t:\\|if len(t) > MAX_TITLE\\|_TAG = \\|def plain_title\\|def validate_title' app/backend/case_list.py; grep -n 'def live_enabled\\|return os.environ.get(\"ENABLE_LIVE\")\\|return provider.backend_name() != \"fixture\"' app/backend/store.py; grep -n 'store.live_enabled()\\|def demo_mode' app/backend/api.py; grep -n 'demo is (not store\\|assert got is (store' tests/unit/test_case_list.py; grep -n 'Untitled case' app/frontend/overview.js; grep -n 'innerHTML' -r app/frontend | head -3; grep -n 'if first:' app/backend/case_list.py; grep -n 'w = waiting\\[0\\]' app/backend/case_list.py; grep -n 'if not (r\\[\"review_status\"\\] == \"pending\" or review.edit_unconfirmed' app/backend/case_list.py; grep -n 'if not (r\\[\"review_status\"\\] == \"pending\" or i.get\\|waiting = \\[i for k in\\|assert na\\[\"item_id\"\\] in every' tests/unit/test_case_list.py",
 "description": "Get exact file:line citations for review findings"
}
````

### User / tool · 2026-11-02T15:32:45.226Z

**tool result**
````
140:    def get_case(c, token):
141:        case = DB.get_case(c, token)
248:        typed = isinstance(b.get("title"), str)
249:        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
253:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
286:    def valid_name(value, strict=True):
332:            case = get_case(c, token)
344:        name = valid_name(b["title"])
347:            get_case(c, token)
349:            case = DB.get_case(c, token)
358:            get_case(c, token)
369:            if DB.get_case(c, token)["status"] == "running":
383:            case = get_case(c, token)
408:            case = get_case(c, token)
427:            case = get_case(c, token)
448:            get_case(c, token)
459:            get_case(c, token)
472:            get_case(c, token)
481:            get_case(c, token)
491:            get_case(c, token)
504:            get_case(c, token)
518:            get_case(c, token)
531:            get_case(c, token)
554:            get_case(c, token)
581:            get_case(c, token)
593:            get_case(c, token)
602:            get_case(c, token)
611:            get_case(c, token)
26:_TAG = re.compile(r"<[^<>]*>?")
40:def validate_title(value) -> str:
45:    if "<" in t or ">" in t:
47:    if len(t) > MAX_TITLE:
52:def plain_title(value) -> str:
11:def live_enabled() -> bool:
15:    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
21:    return provider.backend_name() != "fixture" and live_enabled()
117:        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available
119:    def demo_mode():
381:    assert demo is (not store.live_enabled())
385:    assert got is (store.live_model_available() and not demo)
51:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
app/frontend/sidebyside.js:5:   All record text goes in as text nodes (ZL.el / createTextNode); nothing here uses innerHTML. */
170:    if first:
174:        w = waiting[0]
147:            if not (r["review_status"] == "pending" or review.edit_unconfirmed(kind, r)):
248:            waiting = [i for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])
258:        assert na["item_id"] in every, lid
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:33:45.177Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer-r2.md",
 "content": "# T-157 review r2: staff-engineer-reviewer (commit 852b060)\n\nVerdict: **changes** (0 blockers, 1 major, 5 minors, 1 nit). Verdict rule: no blocker, so not fail; one major, so changes.\n\nScope: commit 852b060, the r2 fix. HEAD has moved to 2ac96cf (a T-140 commit); I did not review 2ac96cf. Reviewed on a `git archive 852b060` copy with untracked `artifacts/review-evidence` overlaid (tests read it). Fixture backend, in-process TestClient, no live app URL, no UI.\n\nWhat holds:\n- Titles: control, zero-width and bidi characters are removed before the markup check. `<` or `>` and titles over 120 characters are `422 invalid_title`, nothing is stored, and the message never echoes the text. The PDF `?title` is checked before the file is read.\n- next_action: blockers come first (NOTHING_ACCEPTED yields to a waiting item), then timeline order with an id tie-break. Six of the ordering and blocker mutants die.\n- Live definition: `api.live_enabled` calls `store.live_enabled`, and `rerun_available` goes through `store.live_model_available`, which calls the same function. The baseline demo gate is correct.\n- Full `tests/unit` on the clean archive: 4778 passed, 8 skipped, exit 0. This matches the card's evidence.\n\nWhat does not hold:\n- The unconfirmed-edit class drops out of next_action with no test failing (major, finding 1). The live-definition test compares the API with the store by identity and cannot fail for a definition change (minor, finding 6).\n- An HTML-entity-encoded title is stored verbatim. It is inert today, but it is not refused (finding 2).\n\nMutants (scratch copy, one at a time, restored and confirmed; baseline 40 passed, restored 40 passed):\n- killed: A waiting[-1]; B first=None; C seq/rank swap; D undated first; E markup check off; F derived tags kept; G NOTHING_ACCEPTED not yielded; H blockers lose to waiting; I length cap off; J bidi not stripped; L rerun ignores live model; N api.live_enabled diverges.\n- survived: K unconfirmed edit not waiting (test_case_list.py: 40 passed); M store.live_enabled drops ENABLE_LIVE (40 passed).\n\nFindings (detail in the JSON block):\n1. major: next_action drops unconfirmed edits from the waiting set (mutant K survives; the reworded-entry case changes its pick from e1 to f_r2_1).\n2. minor: entity-encoded titles stored verbatim (201).\n3. minor: create silently ignores a non-text `title` (201), while PATCH returns 400.\n4. minor: PATCH validates the title before the token lookup, so an unknown token with a bad title gets 422, not the 404 that api.md states.\n5. minor: derived title drops all text after a stray `<` (api.md says brackets are dropped, not the text after them).\n6. minor: the live-definition test is tautological for the demo flag; mutant M survives, and a probe shows the public demo gate flips (`demo_mode` False, non-recorded text 201).\n7. nit: `Untitled case` fallback still in app/frontend/overview.js:51 (carry-over from r1, outside this commit).\n\nQuestions for Chris are in the JSON block.\n\n```json\n{\"card\": \"T-157\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 852b060 (r2 fix): app/backend/api.py, case_list.py, store.py, memory/contracts/api.md, tests/unit/test_case_list.py. HEAD at review time was 2ac96cf (not reviewed). Reviewed on a git archive copy of 852b060 at /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060 with untracked artifacts/review-evidence overlaid (cp -Rn). Fixture backend, in-process TestClient, no app URL. Case under test: evals/library/case_lib02 (reworded entry), plus every library case for next_action.\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-157-staff-engineer.md (r1), .claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md\",\n  \"python3 tools/board.py show T-157: status in_review, commits [926bf37, 852b060], rounds 1, AC 1 done with the r2 evidence text\",\n  \"git rev-parse --short HEAD -> 2ac96cf; git log --oneline -5 (852b060 is the r2 commit, 2ac96cf is later and out of scope)\",\n  \"git show 852b060 -- app/backend/api.py app/backend/case_list.py app/backend/store.py memory/contracts/api.md (full diff read) and git show --stat 852b060 (5 files, 321 insertions, 32 deletions)\",\n  \"git archive 852b060 | tar -x into the scratchpad T-157-r2-852b060; cp -Rn artifacts/review-evidence overlay; five in-scope files diffed against git show 852b060:<path> (identical)\",\n  \".venv/bin/python -I -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider on the archive: '40 passed in 11.33s'\",\n  \".venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider on the archive: '4778 passed, 8 skipped in 286.67s (0:04:46)', exit 0 (output file T-157-r2-full-unit.out in the scratchpad)\",\n  \"read tests/unit/test_case_list.py in full (lines 1-520 of the archive copy) and app/backend/case_list.py, store.py, present.py:37-47, api.py:112-122, api.py:240-350\",\n  \"mutant run on a second archive copy T-157-r2-mut (no overlay, test_case_list only): script T-157-r2-mutate.py, output T-157-r2-mutants.out; 14 mutants: A waiting[-1] KILLED (2 failed); B first=None KILLED (2); C seq/rank swap KILLED (1); D undated first KILLED (3); E markup check off KILLED (4); F derived tags kept KILLED (2); G NOTHING_ACCEPTED not yielded KILLED (2); H blockers lose to waiting KILLED (2); I length cap off KILLED (2); J bidi not stripped KILLED (1); K unconfirmed edit not waiting SURVIVED (40 passed); L rerun ignores live model KILLED (17); M store.live_enabled drops ENABLE_LIVE SURVIVED (40 passed); N api.live_enabled diverges KILLED (6). Baseline and restored runs: 40 passed\",\n  \"title probe T-157-r2-probe.py (python -I, fixture env, TestClient): ASCII <img onerror> -> 422 invalid_title; entity &lt;img -> 201 stored verbatim; double-encoded &amp;lt; -> 201 verbatim; fullwidth U+FF1C/FF1E, U+2039/203A, U+FE64/FE65 -> 201 stored verbatim (inert); NUL/BEL and ZWJ removed -> 201; 120 chars -> 201; 121 chars -> 422; 120 visible + 10 controls -> 201; int title on create -> 201 with name null; name=<b>x</b> -> 422; name of 200 chars -> 201 cut; PATCH <img> -> 422, PATCH entity -> 200 stored, PATCH fullwidth -> 200 stored, PATCH int/bool -> 400; stored name unchanged after refused PATCH; PATCH unknown token with valid title -> 404, with markup or 121 chars -> 422, with int title or no title -> 400\",\n  \"bypass probe T-157-r2-probe4.py: '<' followed by U+200B, NUL, U+202E, VT, or '<' after U+2028 / U+0085 -> REFUSED; numeric entities &#60; and &#x3c; and \\\\u003c -> STORED verbatim; legacy stored markup via readable_name -> 'Smith records' (tags dropped at read)\",\n  \"derived title probe T-157-r2-probe2.py (baseline): plain_title('<img ...>Marrowgate ED') -> 'Marrowgate ED'; plain_title('Marrowgate <img src=x onerror=alert(1) ED') -> 'Marrowgate'; plain_title(\\\"St. Mary's <3 Clinic\\\") -> \\\"St. Mary's\\\"; plain_title('&lt;b&gt;Clinic') -> stored as text\",\n  \"demo gate probe T-157-r2-probe2.py with ANTHROPIC_API_KEY set, ENABLE_LIVE unset, LLM_BACKEND=anthropic-api: baseline GET /api/health demo_mode True, live_enabled False, backend fixture; POST /api/cases non-recorded text -> 409 demo_mode_unsupported_input. Under mutant M (store.py:15 ENABLE_LIVE check dropped): demo_mode False, live_enabled True, POST -> 201. Mutant file restored and diffed against git show 852b060\",\n  \"next_action probe T-157-r2-probe3.py: all 15 library cases run on the fixture, reworded entry on case_lib02 (edit_to_check). Baseline: edit item e1 in waiting True, next_action e1 (output T-157-r2-probe3-base.out). Mutant K (case_list.py:147 drops edit_unconfirmed): e1 in waiting False, next_action f_r2_1 (output T-157-r2-probe3-K.out); diff shows only the case_lib02 line changes. Mutant restored and diffed\",\n  \"grep -rn innerHTML app/frontend -> only a comment (app/frontend/sidebyside.js:5); grep -n Untitled case app/frontend/overview.js -> line 51; grep title readers in app/backend (none reach the export, the letter or a prompt)\",\n  \"not exercised: a live app URL (none), the eval runner (not in the T-157 brief), the UI (no frontend change in this commit)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"card_acs_implemented\": 4, \"tests_prove_acs\": 3, \"title_input_validation\": 4, \"rerun_available_correct\": 4, \"next_action_determinism\": 3, \"contract_consistency\": 3, \"honest_failure\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"next_action drops unconfirmed edits from the waiting set; the mutant survives and changes the named item\",\n   \"evidence\": \"app/backend/case_list.py:147 'if not (r[review_status] == pending or review.edit_unconfirmed(kind, r)):' (double quotes shown as single). Mutant: drop the edit_unconfirmed clause; pytest tests/unit/test_case_list.py -q on the mutant copy: '40 passed in 9.84s' (SURVIVED). Probe T-157-r2-probe3.py: baseline 'edit item id: e1 in waiting: True' and 'next_action second: e1'; under the mutant 'edit item id: e1 in waiting: False' and 'next_action second: f_r2_1'. Tests: tests/unit/test_case_list.py:247-251 checks the waiting list only when next_action is None; :258-261 checks membership only against the items next_action already named, so an omitted class is invisible.\",\n   \"why_it_matters\": \"memory/contracts/api.md line 703 defines the queue as including 'an edit not yet confirmed'. Dropping that class points the paralegal at the next decided-looking item and never at the reworded entry. The gate still lists EDIT_NOT_CONFIRMED as a warning, so the loss is silent at the next_action level. The card's evidence says mutants turn tests red; this one does not, and the brief requires the mutants to die.\",\n   \"fix\": \"Add a case where a reworded (edited, unconfirmed) entry is the earliest waiting item, and assert next_action names it. Also assert for every library case that the set of items next_action may name equals the GET case items with state needs_review and (review_status pending or edit_to_check), computed from the case JSON and not from needs_review_order.\",\n   \"acceptance_test\": \"Scratch mutant of case_list.py:147 (drop edit_unconfirmed) must turn tests/unit/test_case_list.py red. For the case_lib02 reworded-entry scenario, next_action.item_id equals the edited entry e1 (T-157-r2-probe3.py output must not change to f_r2_1).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"HTML-entity-encoded titles are stored verbatim (not refused)\",\n   \"evidence\": \"Probe T-157-r2-probe.py: POST /api/cases title '&lt;img src=x onerror=alert(1)&gt;Rivera' -> 201, stored name '&lt;img src=x onerror=alert(1)&gt;Rivera'. Numeric '&#60;img&#62;' (validate_title) and double-encoded '&amp;lt;img' also stored verbatim. Code: app/backend/case_list.py:45 checks only literal '<' or '>'. No decode step anywhere; no innerHTML in app/frontend (grep).\",\n   \"why_it_matters\": \"Inert today: nothing decodes the text and inserts it as markup. The contract says a title is never markup, and an entity-encoded title becomes markup at the first sink that decodes once before inserting. Rated minor, not major, because no current sink does this and the paralegal sees the literal entity text. The rule as written in the card (reject < and >) is met.\",\n   \"fix\": \"Pick one and write it into api.md line 703: (a) refuse '&' followed by a named or numeric character reference, or (b) state that titles are literal text, entities are shown as typed, and no sink may decode them. Pin the choice in tests.\",\n   \"acceptance_test\": \"Option (a): POST /api/cases with title '&lt;img&gt;' returns 422 invalid_title. Option (b): the stored value is '&lt;img&gt;' and a test asserts it is unchanged and that api.md documents it.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Create silently ignores a non-text title; PATCH refuses the same body with 400\",\n   \"evidence\": \"app/backend/api.py:248-249 'typed = isinstance(b.get(title), str)' / 'given = b.get(title) if typed else b.get(name)'. Probe T-157-r2-probe.py: POST /api/cases with text and title 5 -> 201, title 'Sablewood Market first-aid log, Mar 9, 2026', name null. PATCH with title 5 -> 400 bad_request (api.py:342-343).\",\n   \"why_it_matters\": \"A typed value that is not text is dropped while the response says success. The create and PATCH routes disagree on the same input. The honest-failure rule says a refused input should say so.\",\n   \"fix\": \"On create, if the key title is present and is neither a string nor null, return 400 bad_request, the same as PATCH.\",\n   \"acceptance_test\": \"POST /api/cases with text and title 5 returns 400 bad_request and creates no case. Add this to tests/unit/test_case_list.py next to the PATCH non-text checks at lines 190-195.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"PATCH checks the title before the token lookup: unknown token with a bad title returns 422, not 404\",\n   \"evidence\": \"app/backend/api.py:344 'name = valid_name(b[title])' runs before api.py:347 'get_case(c, token)'. Probe T-157-r2-probe.py: PATCH /api/cases/nope with title '<img ...>' -> 422 invalid_title; with a 121-character title -> 422; with title 'a' -> 404 not_found. memory/contracts/api.md (PATCH sentence, line 703) says 'an unknown token is 404 not_found'.\",\n   \"why_it_matters\": \"The order is not written down and the doc says 404. No existence leak: a bad title gets 422 whatever the token. Minor, as the brief says.\",\n   \"fix\": \"Look up the token first (api.py:347 before 344), or add 'checks run in this order: body, token, title' to api.md.\",\n   \"acceptance_test\": \"A test PATCHes /api/cases/nope with a markup title and asserts the documented status (404 if the token check moves first).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Derived title drops all text after a stray '<' (the doc says brackets are dropped)\",\n   \"evidence\": \"app/backend/case_list.py:26 _TAG = re.compile(r'<[^<>]*>?') used by plain_title at :54. Probe T-157-r2-probe2.py: plain_title(\\\"St. Mary's <3 Clinic\\\") -> \\\"St. Mary's\\\"; plain_title('Marrowgate <img src=x onerror=alert(1) ED') -> 'Marrowgate'. memory/contracts/api.md line 703, rule (2): 'its Source line with any tags or angle brackets dropped'.\",\n   \"why_it_matters\": \"The header label loses words that were in the record. Not a safety issue (the record text is untouched and the title is inert), but the code does more than the documented rule.\",\n   \"fix\": \"Remove complete <...> pairs only, and drop any remaining lone < or > character without deleting the text after it.\",\n   \"acceptance_test\": \"plain_title(\\\"St. Mary's <3 Clinic\\\") == \\\"St. Mary's 3 Clinic\\\", and plain_title('<b>Clinic</b> & Co <') still == 'Clinic & Co' (the existing test at tests/unit/test_case_list.py:345 stays green).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The live-definition test compares the API with the store by identity; a change to the definition passes\",\n   \"evidence\": \"tests/unit/test_case_list.py:381 'assert demo is (not store.live_enabled())' and :385 'assert got is (store.live_model_available() and not demo)'. The API side is api.py:117 'return store.live_enabled()'. Mutant M (app/backend/store.py:15, drop 'os.environ.get(ENABLE_LIVE) == 1 and'): pytest tests/unit/test_case_list.py -q -> '40 passed in 17.68s' (SURVIVED). Probe T-157-r2-probe2.py with ANTHROPIC_API_KEY set and ENABLE_LIVE unset: baseline health demo_mode True and POST non-recorded text 409 demo_mode_unsupported_input; under mutant M demo_mode False and POST 201. tests/unit/test_api_routes.py:43 and :316 pin demo_mode only with no key set.\",\n   \"why_it_matters\": \"Sharing the definition holds by construction, which is what the AC asks for. But no test pins the value of the demo gate, so a change to the live definition flips the public demo gate (ADR-006, 'demo mode is the gate') and the suite stays green.\",\n   \"fix\": \"Add absolute pins next to the parametrized test: ANTHROPIC_API_KEY=<redacted> ENABLE_LIVE unset, LLM_BACKEND=anthropic-api, expecting health demo_mode True and POST of non-recorded text 409; and ENABLE_LIVE=1 with LLM_BACKEND=claude-cli, expecting demo_mode False.\",\n   \"acceptance_test\": \"Mutant store.py:15 (drop the ENABLE_LIVE check) turns the new absolute-pin test red.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Untitled case fallback still in the frontend (carry-over from r1)\",\n   \"evidence\": \"app/frontend/overview.js:51 'const titleOf = (s) => (... : s.title || ZL.niceName(s.name) || Untitled case);' (double quotes shown as single). Unreachable while the backend always sends a title.\",\n   \"why_it_matters\": \"Dead text, but it is the string the AC bans, and a future null from the backend would show it.\",\n   \"fix\": \"Route to the frontend card: drop the fallback and use the backend title only.\",\n   \"acceptance_test\": \"grep -rn 'Untitled case' app/frontend returns nothing.\"}\n ],\n \"whats_right\": [\n  \"Refusal happens before any write and before the PDF is read: a refused title leaves no case behind (probe T-157-r2-probe.py; the count assertion at tests/unit/test_case_list.py:306-308).\",\n  \"Control, zero-width and bidi characters are removed before the markup check, so '<' followed by U+200B, NUL, U+202E or VT is still refused (probe T-157-r2-probe4.py).\",\n  \"The blocker and timeline rules are now pinned: mutants waiting[-1], first=None, the seq/rank swap, undated-first, the NOTHING_ACCEPTED yield and blockers-behind-waiting all turn tests red (12 of 14 mutants killed; file T-157-r2-mutants.out).\"\n ],\n \"questions_for_chris\": [\n  \"Entity-encoded titles (&lt;img&gt;): should they be refused with 422 like '<' and '>', or stored as literal text and documented in api.md as never decoded? Finding 2 waits on this choice.\",\n  \"Create with a non-text title (title 5): 400 like PATCH, or ignored as today? Finding 3 waits on this choice.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T15:33:45.358Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:33:48.559Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json,re,sys\nt=open('reviews/T-157-staff-engineer-r2.md',encoding='utf-8').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd=json.loads(blocks[0])\nprint(d['card'], d['persona'], d['model'], d['verdict'])\nsev=[f['severity'] for f in d['findings']]\nprint('severities:', {s: sev.count(s) for s in set(sev)})\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('verdict rule expects:', exp, 'matches:', exp==d['verdict'])\nprint('whats_right lines:', len(d['whats_right']))\n\" ; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Parse the review JSON block and check the verdict rule"
}
````

### User / tool · 2026-11-02T15:33:48.647Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:33:52.495Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T-157-r2-parse.py\" <<'EOF'\nimport json, re\nt = open(\"/Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer-r2.md\", encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), t, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(d[\"card\"], d[\"persona\"], d[\"model\"], d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"severities:\", {s: sev.count(s) for s in set(sev)})\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule expects:\", exp, \"matches:\", exp == d[\"verdict\"])\nprint(\"whats_right lines:\", len(d[\"whats_right\"]), \"exercised:\", len(d[\"exercised\"]))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T-157-r2-parse.py\"",
 "description": "Parse the review JSON block and check the verdict rule"
}
````

### User / tool · 2026-11-02T15:33:52.678Z

**tool result**
````
json blocks: 1
T-157 staff-engineer-reviewer claude-haiku-5-5 changes
severities: {'minor': 5, 'major': 1, 'nit': 1}
verdict rule expects: changes matches: True
whats_right lines: 3 exercised: 16
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:33:57.856Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md"
}
````

### User / tool · 2026-11-02T15:33:57.865Z

**tool result**
````
1	---
2	name: t157-case-title-next-action-patterns
3	description: T-157 r1 926bf37 (changes): next_action blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card full-suite counts do not reproduce, archive needs review-evidence overlay
4	metadata:
5	  type: project
6	---
7	
8	T-157 r1 at 926bf37 was verdict changes (3 majors, 4 minors, 2 nits). Reviewer file reviews/T-157-staff-engineer.md is write-once.
9	
10	- **Survivors in a new ordering feature.** Mutants that break the blockers-first rule (`first = None`) and the timeline pick (`waiting[-1]`) both left all 13 tests green. The tests asserted membership and the helper's own sort, not the chosen item. Lesson: for any "single first item" field, mutate the selection index and the precedence branch, not only the sort key.
11	- **Titles.** Length cap (120) was tested, HTML was not. Record text (Source header) flows into the derived default title. The frontend writes text nodes, so it is not exploitable today; rate major, not blocker, and escalate if an innerHTML sink appears.
12	- **Evidence numbers.** The card claimed 4387 passed / 2 failed in tests/unit; the same commit gave 4286 passed, 8 skipped, 0 failed. Its failing file (test_e2e_contract) is not under tests/unit. Check card evidence against a clean archive run.
13	- **Archive needs untracked fixtures.** `git archive` omits artifacts/review-evidence (untracked), so tests/unit collection fails with FileNotFoundError until it is overlaid with `cp -Rn` from the working tree. Same root as [[project_round2_snapshot_review_patterns]].
14	- **Working tree is dirty with other cards.** `git status` showed uncommitted app/ changes from other workers; always review the archive of the commit, never the working tree.
15	- **Reviewer write guard.** After the first Write, an Edit to the same reviews file is denied (append-only). A count typo in the summary could not be corrected; get the markdown summary right before the first Write.
16	
17	**Why:** the card AC said "blockers first, then timeline order", and the suite could not tell a correct next_action from a wrong one.
18	**How to apply:** on any future "next item" or "single first thing" field, run mutants on the selection index and each precedence branch; expect red. See [[project_gate_m2_patterns]] for gate blocker ordering.
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:34:02.948Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md",
 "old_string": "---\nname: t157-case-title-next-action-patterns\ndescription: T-157 r1 926bf37 (changes): next_action blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card full-suite counts do not reproduce, archive needs review-evidence overlay\nmetadata:\n  type: project\n---\n\nT-157 r1 at 926bf37 was verdict changes (3 majors, 4 minors, 2 nits). Reviewer file reviews/T-157-staff-engineer.md is write-once.",
 "new_string": "---\nname: t157-case-title-next-action-patterns\ndescription: T-157 r1 926bf37 (changes) and r2 852b060 (changes): next_action waiting-set and timeline mutants, title markup rules, demo-gate identity test, archive needs review-evidence overlay\nmetadata:\n  type: project\n---\n\nT-157 r1 at 926bf37 was verdict changes (3 majors, 4 minors, 2 nits). Reviewer file reviews/T-157-staff-engineer.md is write-once.\n\n**r2 852b060 (changes: 1 major, 5 minors, 1 nit; file reviews/T-157-staff-engineer-r2.md).** Blocker and ordering mutants died (first=None, waiting[-1], seq/rank, undated-first, NOTHING_ACCEPTED yield). Survivors:\n- Dropping the unconfirmed-edit clause from the waiting set (case_list.py:147) passed all 40 tests and changed the pick from the reworded entry to a flag. Tests check the waiting list only when next_action is None. Same lesson as r1: pin the set membership with an independent oracle (case JSON fields), not with needs_review_order itself.\n- A \"shared definition\" test that compares api.demo_mode with store.live_enabled by identity cannot fail for a definition change. Dropping the ENABLE_LIVE check in store.py flipped the public demo gate (health demo_mode False, non-recorded paste 201) with no red test. Pin absolute values with a key set and ENABLE_LIVE unset.\n- Titles: '<' and '>' refused correctly, control and bidi characters stripped before the check. Entity-encoded (&lt;, &#60;) stored verbatim: inert, minor. Create silently ignores a non-text title while PATCH returns 400. PATCH checks the title before the token, so unknown token with bad title gives 422 (api.md says 404). Derived title drops all text after a stray '<' (doc says brackets only).\n- Evidence: the card's full-suite claim reproduced (4778 passed, 8 skipped on a clean archive of 852b060).\n- Archive overlay: `cp -Rn` returns exit 1 on existing files; that is not a failure. Check the five in-scope files against git show.\n- HEAD moves: by r2 review time HEAD was 2ac96cf, not the reviewed commit. Review the named commit's archive only."
}
````

### User / tool · 2026-11-02T15:34:03.047Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:34:05.015Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-157 title/next_action patterns](project_t157_case_title_next_action_patterns.md) — 926bf37 changes: blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card counts not reproduced, archive needs review-evidence overlay",
 "new_string": "- [T-157 title/next_action patterns](project_t157_case_title_next_action_patterns.md) — r1 926bf37 and r2 852b060 (changes): edit-class waiting-set survivor, identity-only demo test, entity titles, PATCH 422-before-404"
}
````

### User / tool · 2026-11-02T15:34:05.148Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:34:07.014Z

Verdict: changes (0 blockers, 1 major: unconfirmed edits drop out of next_action without any test failing; 5 minors, 1 nit), written to /Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer-r2.md.
