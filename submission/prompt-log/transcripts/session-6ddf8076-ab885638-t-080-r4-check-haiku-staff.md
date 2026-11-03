# Subagent: T-080 r4 check (haiku staff) (T-080 r4 check (haiku staff))

Source: `agent-ab885638c47037af4.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:02:28.236Z

Final check of board card T-080 in /Users/arsis/zlayt-pm-project (commit 10d358e). Using reviews/T-080-staff-engineer-r3.md and D-044 and D-045 in memory/ORCHESTRATOR_DECISIONS.md, confirm:
- the gate and GET /export share one blocker list, and gate.ready == export allowed in every state;
- pending items are warnings, not blockers;
- NOTHING_ACCEPTED, run-failed and run-in-progress return 422 export_blocked (judge whether that's reasonable);
- paralegal-written summaries are not counted as unchecked;
- the invariant test fails if you break the shared list in a scratch copy.

Run `.venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py`. Write reviews/T-080-staff-engineer-r4.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:29.495Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:02:29.503Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:29.718Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-080-staff-engineer-r3.md"
}
````

### User / tool · 2026-11-02T04:02:29.730Z

**tool result**
````
1	# T-080 round-3 review: D-044 judge export gate, D-045 scope (staff-engineer-reviewer)
2	
3	Scope: commit fe4ee80 (D-044 gate, export 422, POST /rejudge, tests) with the D-045 docs commit f49c4c2 on top. HEAD moved to 8d7548d during the review; `git diff --name-only fe4ee80 HEAD -- app/backend tests/unit` is empty, so the backend reviewed is the fe4ee80 backend. Frontend as loaded by the live instance is the HEAD of that time (8e3c26c and f49c4c2 frontend).
4	
5	Verdict: **changes** (0 blockers, 1 major, 2 minors, 1 nit). Against the brief's checks: the JUDGE_NOT_RUN gate blocker and the 422 hold live; the paralegal-summary exemption and the D-034 number check hold live; rejudge is audited and fixture-only in demo mode. Two checks fail: rejudge re-asks pending items too, and pending items still block the gate (D-045(a) is not implemented; the export endpoint itself does not block on pending).
6	
7	## Answers to the brief
8	
9	- **Accepted LLM-made item whose judge never ran is a JUDGE_NOT_RUN gate blocker: confirmed.** Live: accepted e1, e2, a1, a2 after blanking their judge records; `/trace` export_gate `blockers` has four `JUDGE_NOT_RUN` entries, `next_action` `RERUN_JUDGE`, gate `counts.judge_not_run` 4.
10	- **GET export returns 422 judge_not_run: confirmed.** Live: `GET /api/cases/<tok>/export` gave 422 with `error.code` `judge_not_run` and `detail.blockers` naming the same four ids. After `POST /rejudge` the same GET gave 200.
11	- **POST rejudge re-judges only those items: not confirmed.** Live: `asked` 12 = the four accepted blocked items plus eight pending unjudged items (a4, e3 to e9). See finding 2.
12	- **Audited, fixture-only in demo mode: confirmed.** Live: 12 new `llm_calls` rows, all `backend` fixture, `role` judge; `ladder.rejudge` trail present on e1, a1. Demo guard: `api.py:360-376` plus `provider.backend_name` (fixture unless ENABLE_LIVE=1); mutant M6 killed by `test_rejudge_is_refused_in_the_cases_the_run_route_refuses`.
13	- **Paralegal-written or edited summaries exempt from the judge, still code-checked (D-034): confirmed for the gate and the code check.** Live: edit of e3 summary with no new number left e3 out of JUDGE_NOT_RUN; edit adding `987` (not in the quote) gave 422 `invalid_edit` with `SUMMARY_NUMBER_NOT_IN_EXCERPT`. But the judges step still counts e3 as unchecked: finding 3.
14	- **Pending items do not block export: export endpoint yes, gate no.** Live with 18 pending: `GET /export` 200, internal notes "Items not reviewed: 18" (D-045(a) AI line counts them), pending excluded from the letter. But `/trace` export_gate `ready` False with 18 `PENDING_DECISION` blockers. Finding 1.
15	
16	## Findings
17	
18	### 1. major: pending items still block the gate; D-045(a) is not implemented
19	Live (scratch case, 18 pending, 4 accepted): `/trace` export_gate `ready: False`, `blockers` = 18 x `PENDING_DECISION`, verdict "18 items still need your decision". Code: `app/backend/trace.py:889-895` (live pending becomes PENDING_DECISION or DATE_UNCONFIRMED blockers), `:901` `ready = ... and not blockers`, `:910` text "N items have no decision yet, so the export is blocked." UI: `app/frontend/stepper.js:352` "Export blocked by N"; the copy path does not block: `app/frontend/export.js:39` asks a confirm when `c.pending > 0`. Test codifies it: `tests/unit/test_trace.py:741-745` asserts `g["ready"] is False` with pending items.
20	Why it matters: D-045(a) (binding) says pending items never block export. R-EX-5 (`spec/REQUIREMENTS.md:123`) says copy asks one confirmation when anything is pending. The gate tells the paralegal the export is blocked while the Copy button works after one confirm. That is a false status, not an unsafe export: pending items stay out of the letter and the notes count them. Rated major, not blocker, because it is fail-closed and loses or invents no facts.
21	Fix: take PENDING_DECISION (and DATE_UNCONFIRMED, which is also a pending state) out of `blockers`; report pending as `counts.pending_items` and a confirm line. Keep `ready == (blockers == [])`, with ready also requiring no JUDGE_NOT_RUN and no run blocker. Rewrite `test_trace.py:741-745` and the `test_gate_and_export_agree_on_the_judge_dimension_in_every_state` expectations. Record the gate rule in `memory/DECISIONS.md`.
22	Acceptance test: sample case, accept all but one entry, judges answered. Assert `/trace` export_gate `ready` True and `blockers` []; `/export` 200; internal notes contain "Items not reviewed: 1". Then blank one accepted item's judge: gate `ready` False with only JUDGE_NOT_RUN, export 422.
23	
24	### 2. minor: rejudge re-asks pending unjudged items, not only the blocked accepted ones
25	Live: `POST /api/cases/<tok>/rejudge` gave `asked: 12`; rejudged ids a1, a2, a4, e1, e2, e3 to e9. The blocked accepted items were e1, e2, a1, a2; a4 and e3 to e9 are pending. Code: `app/backend/rejudge.py:60` `targets = trace.unjudged_items(conn, case_id)`; `trace.py:667-679` returns live items regardless of review_status. Test `tests/unit/test_trace.py:829` `assert r["asked"] == n` codifies it.
26	Why it matters: D-044 says the rejudge "re-judges just those items" (the items the gate lists). Pending items get extra audited model calls. No `review_status` changes, so low impact.
27	Fix: either restrict targets to review_status accepted or edited, or record in `memory/DECISIONS.md` that pending unjudged items are also re-asked, and update the test.
28	Acceptance test: 4 accepted and 8 pending unjudged items: `asked` equals 4 (or the DECISIONS entry names 12 and the test asserts 12).
29	
30	### 3. minor: judges step and /judges count a paralegal-edited summary as unchecked; D-045(b) exempts it
31	Live: e3 summary edited (no new number), judge unavailable on the edit. `/judges` totals `unavailable: 1`. `/trace` judges step `fail`, reason JUDGE_UNAVAILABLE, "1 item has not been double-checked", next `RERUN_JUDGE`. After dismissing the other pending items in the scratch case, export_gate `ready: True`, verdict "Ready to export", with the judges step still `fail`. Code: `trace.py:637-655` `_judge_rows` has no paralegal-wording exemption; `judge_report` (`trace.py:692`) counts from it. The exemption exists only in `unjudged_items` (`trace.py:676`).
32	Why it matters: the view shows a failed check, and a rerun action, on wording the spec says is human-authored, next to a gate that passes. An honest but contradictory state.
33	Fix: apply the same `entered_by` and edited-summary exemption in the judge counts and the judges step, or show the item as paralegal wording (not AI-checked).
34	Acceptance test: edit one entry summary so its judge is unavailable, dismiss the other pending items: judges step not `fail` on account of that item; gate `ready` True; verdict code `ready`.
35	
36	### 4. nit: export refusal has no unit test in tests/unit/test_export.py
37	`export.py:576-577` raises `JudgeNotRun`; only the HTTP route tests cover it (`test_trace.py`). The mutant M5 is killed only through the API.
38	Fix: unit test calling `export.build_export` with `judge_not_run` set and asserting `JudgeNotRun` is raised, with the items.
39	
40	## Mutation run (scratch copy of app, tests, evals, docs, spec, memory; not committed)
41	Baseline `tests/unit/test_trace.py tests/unit/test_export.py`: 75 passed.
42	
43	| Mutant | Result |
44	|---|---|
45	| M1 gate ignores JUDGE_NOT_RUN (`trace.py` `blockers.extend(jnr)` to `pass`) | killed, 9 failed |
46	| M2 gate counts only `accepted` (drops `edited`) | killed, 1 failed |
47	| M3 paralegal-written summary not exempt (`unjudged_items`) | killed, 2 failed |
48	| M4 store.export_case passes no JNR (`store.py:78`) | killed, 4 failed |
49	| M5 build_export does not refuse (`export.py:576`) | killed, 4 failed |
50	| M6 rejudge skips demo fixture guard (rejudge route only, unique anchor) | killed, 1 failed |
51	| M7 rejudge answer does not recompose state (`rejudge.py` recompose) | killed, 2 failed |
52	
53	## Checked and fine
54	- Rejudge writes go through `audited.py` `_DB_LOCK` (`audited.py:16`, `:82`), so the 4-thread pool shares the sqlite connection safely.
55	- `ready == (blockers == [])` held in every live state I probed (pending, JNR, rejudged, dismissed).
56	- D-034 hard 422 has no override in the edit path; the gate's JNR exemption does not clear on accept, edit or compare-by-hand (`test_no_override_...` passes).
57	- Trace and rejudge code: no `float(`, no bare `except`, no sleep, no network in the new code path (grep of `app/backend/rejudge.py` and the D-044 hunks in `trace.py`).
58	
59	## What's right
60	1. The JUDGE_NOT_RUN blocker and the export 422 come from one function (`trace.judge_not_run_blockers`, read by `store.export_case` and the gate), so the live gate and export listed the same four ids, and both cleared after rejudge.
61	2. The paralegal-summary exemption and the D-034 check both behave live: `987` not in the quote gives 422; a text-only edit leaves e3 out of JUDGE_NOT_RUN.
62	3. Rejudge is audited (12 `llm_calls` rows, backend fixture, role judge) and fixture-only in demo mode; it never changes `review_status`.
63	
64	```json
65	{"card": "T-080", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
66	 "scope": "commit fe4ee80 (backend: app/backend/trace.py, rejudge.py, api.py, export.py, export_routes.py, store.py; tests/unit/test_trace.py) with D-044/D-045 in memory/ORCHESTRATOR_DECISIONS.md (f49c4c2); HEAD moved to 8d7548d, no app/backend or tests/unit changes since fe4ee80; live instance 127.0.0.1:7996 (stopped), LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB scratch file, DATA_DIR empty sentinel; sample case",
67	 "exercised": [
68	  "read personas/staff-engineer.md, reviews/T-080-staff-engineer-r2.md, memory/ORCHESTRATOR_DECISIONS.md D-044 and D-045 (lines 52-53), spec/REQUIREMENTS.md R-EX-4 and R-EX-5 (lines 122-123)",
69	  "git show --stat and diffs of fe4ee80 (trace.py, api.py, export.py, export_routes.py, store.py) and f49c4c2; git diff --name-only fe4ee80 HEAD -- app/backend tests/unit (empty)",
70	  ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider -> 75 passed in 4.39s",
71	  "E2E_BASE_URL=http://127.0.0.1:7996 .venv/bin/python -m pytest -q tests/e2e/test_edit.py -p no:cacheprovider -> 9 passed in 11.43s",
72	  "live: POST /api/cases sample, POST /run, poll /status (ready); blanked 12 judge records in the scratch DB only; accepted e1, e2, a1, a2; GET /trace (gate: 4 JUDGE_NOT_RUN + 19 PENDING_DECISION at that point); GET /export -> 422 judge_not_run with the same 4 ids",
73	  "live: POST /rejudge -> 200, asked 12, rejudged 12, still_unavailable 0; new llm_calls 12, backend fixture, role judge; GET /export -> 200 with 18 pending; internal notes AI line 'Items not reviewed: 18'",
74	  "live: e3 judge removed and accepted (JUDGE_NOT_RUN appears), summary edit with '987' -> 422 invalid_edit SUMMARY_NUMBER_NOT_IN_EXCERPT, text-only summary edit -> 200 and e3 leaves JUDGE_NOT_RUN; GET /judges and /trace (judges step fail with 1 unavailable)",
75	  "live: dismissed the remaining pending items in the scratch case only -> /trace export_gate ready True, verdict Ready to export, judges step still fail",
76	  "live: ladder.rejudge trail read from the scratch DB for e1, a1, e3",
77	  "7 string mutants in a scratch copy (app, tests, evals, docs, spec, memory copied): M1 to M7 all killed (table above)",
78	  "data/zlayt.sqlite sha256 6d7dcf828093a1c07d3671046cf1c0c2e990b536c2e03289946a95f9eacc0593 and mtime 1793590231 before and after; sentinel DATA_DIR empty; scratch ZLAYT_DB file created (442368 bytes); server PID 62029 stopped and port 7996 confirmed free"],
79	 "verdict": "changes",
80	 "scores": {"jnr_gate_blocker": 5, "export_422_agrees_with_gate": 5, "rejudge_scope_and_audit": 3, "rejudge_fixture_only_demo": 5, "paralegal_edit_exemption_and_d034": 4, "pending_not_blocking_d045a": 2, "judges_step_consistency": 3, "mutation_strength": 5},
81	 "findings": [
82	  {"severity": "major", "title": "Pending items still block the gate; D-045(a) not implemented",
83	   "evidence": "Live /trace with 18 pending: export_gate ready False, 18 PENDING_DECISION blockers, verdict '18 items still need your decision'; live /export 200 with 'Items not reviewed: 18'. app/backend/trace.py:889-895 (PENDING_DECISION/DATE_UNCONFIRMED blockers), :901 ready, :910 'so the export is blocked.'; app/frontend/stepper.js:352 'Export blocked by N'; app/frontend/export.js:39 copy asks a confirm when c.pending > 0; tests/unit/test_trace.py:741-745 asserts ready False with pending.",
84	   "why_it_matters": "D-045(a) (binding) says pending items do not block export; R-EX-5 (spec/REQUIREMENTS.md:123) says copy asks one confirmation. The gate reports a block the export does not apply, so the paralegal is told to settle 18 items while the copy path works after one confirm. Fail-closed; no facts invented or lost, so major, not blocker.",
85	   "fix": "Move PENDING_DECISION and DATE_UNCONFIRMED out of blockers; report pending as counts.pending_items and a confirm line. Keep ready == (blockers == []) with JUDGE_NOT_RUN and run blockers still listed. Rewrite test_trace.py:741-745 and the gate-and-export agreement test. Record the rule in memory/DECISIONS.md.",
86	   "acceptance_test": "Sample case, accept all but one entry, judges answered: gate ready True, blockers []; export 200; notes contain 'Items not reviewed: 1'. Blank one accepted item's judge: gate ready False with only JUDGE_NOT_RUN; export 422."},
87	  {"severity": "minor", "title": "Rejudge re-asks pending unjudged items, not only the blocked accepted ones",
88	   "evidence": "Live POST /rejudge: asked 12 (e1, e2, a1, a2 accepted; a4, e3 to e9 pending). app/backend/rejudge.py:60 targets = trace.unjudged_items; trace.py:667-679 includes pending; tests/unit/test_trace.py:829 asserts asked == n.",
89	   "why_it_matters": "D-044 says rejudge re-judges just the items the gate lists. Pending items get extra audited model calls; review_status is untouched, so impact is low.",
90	   "fix": "Restrict targets to review_status accepted or edited, or record in memory/DECISIONS.md that pending unjudged items are also re-asked and update the test.",
91	   "acceptance_test": "4 accepted and 8 pending unjudged items: asked equals 4 (or the DECISIONS entry names 12 and the test asserts 12)."},
92	  {"severity": "minor", "title": "Judges step and /judges count a paralegal-edited summary as unchecked; D-045(b) exempts it",
93	   "evidence": "Live: e3 summary edited, judge unavailable on the edit; /judges unavailable 1; /trace judges step fail 'JUDGE_UNAVAILABLE', next RERUN_JUDGE; after dismissing other pending items export_gate ready True, verdict 'Ready to export'. app/backend/trace.py:637-655 _judge_rows has no exemption; judge_report at :692 counts from it; the exemption exists only in unjudged_items at :676.",
94	   "why_it_matters": "The view shows a failed check and a rerun action on wording the spec says is human-authored, next to a passing gate. Honest but contradictory.",
95	   "fix": "Apply the entered_by and edited-summary exemption in the judge counts and judges step, or show the item as paralegal wording not AI-checked.",
96	   "acceptance_test": "Edit one entry summary with judge unavailable and dismiss the other pending items: judges step not fail on account of that item; gate ready True; verdict code ready."},
97	  {"severity": "nit", "title": "Export refusal has no unit test in tests/unit/test_export.py",
98	   "evidence": "app/backend/export.py:576-577 raises JudgeNotRun; only HTTP tests in tests/unit/test_trace.py cover it; mutant M5 killed only through the API.",
99	   "why_it_matters": "A unit regression in build_export would surface only through the route tests.",
100	   "fix": "Add a unit test calling export.build_export with judge_not_run set and asserting JudgeNotRun with the items.",
101	   "acceptance_test": "build_export({'judge_not_run': [{'item_id': 'x'}], ...}) raises JudgeNotRun; mutant M5 killed by that test."}
102	 ],
103	 "whats_right": [
104	  "The JUDGE_NOT_RUN blocker and the export 422 come from one function (trace.judge_not_run_blockers, read by store.export_case and the gate); live they listed the same four ids and both cleared after rejudge.",
105	  "The paralegal-summary exemption and the D-034 check both behave live: a number not in the quote gives 422 invalid_edit; a text-only edit leaves the item out of JUDGE_NOT_RUN.",
106	  "Rejudge is audited (12 llm_calls rows, backend fixture, role judge) and fixture-only in demo mode, and it never changes review_status."
107	 ],
108	 "questions_for_chris": ["D-045(a) says pending items do not block export, but the gate still lists them as blockers and the stepper says 'Export blocked by N' while Copy works after one confirm. Should pending be a confirm line in the gate (as R-EX-5 describes), not a blocker? I have assumed yes."]}
109	```
110	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:30.349Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-044\\|D-045\" /Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md; echo ---; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ 2>&1 | head -50",
 "description": "Locate D-044/D-045 and list reviewer memory dir"
}
````

### User / tool · 2026-11-02T04:02:30.436Z

**tool result**
````
52:| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53:| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
---
MEMORY.md
feedback_review_write_once.md
feedback_severity_vs_brief.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_r2_fix_verification_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_t063_doc_vs_code_review_patterns.md
project_t065_batch_fallback_review_patterns.md
project_t066_no_model_reason_patterns.md
project_t067_r6_d043_patterns.md
project_t070_t067_review_patterns.md
project_t075_determinism_review_patterns.md
project_t080_trace_review_patterns.md
project_wiring_review_patterns.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:34.248Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && echo --- && git rev-parse --short HEAD && git show --stat --oneline 10d358e | head -30 && echo --- && ls -la reviews/ | grep T-080; echo ---; cat memory/feedback_review_write_once.md 2>/dev/null | head -30; echo ---; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md | head -20",
 "description": "Check git state, commit 10d358e, and existing T-080 reviews"
}
````

### User / tool · 2026-11-02T04:02:34.432Z

**tool result**
````
10d358e fix(backend): export gate ready equals export allowed; pending items warn, not block (D-045)
8d7548d fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)
f49c4c2 docs: D-045 scope of the judge export gate
8e3c26c fix(frontend): collapsed case rail and AI-check row, working case-step actions, narrative stepper entry, Why dialog opens on the active step, one row per item (T-081 r2, T-082 r2)
fe4ee80 feat(backend): D-044 export gate blocks accepted items whose second check never ran; POST /rejudge
---
10d358e
10d358e fix(backend): export gate ready equals export allowed; pending items warn, not block (D-045)
 app/backend/api.py           |   4 +-
 app/backend/export.py        |  20 +++++--
 app/backend/export_routes.py |  12 +++-
 app/backend/store.py         |   3 +-
 app/backend/trace.py         |  86 +++++++++++++++++------------
 memory/contracts/api.md      |  17 +++---
 tests/unit/test_export.py    |  15 +++++
 tests/unit/test_trace.py     | 127 ++++++++++++++++++++++++++++++++++---------
 8 files changed, 205 insertions(+), 79 deletions(-)
---
-rw-r--r--@   1 arsis  staff  17539 Nov  1 21:41 T-080-staff-engineer-r2.md
-rw-r--r--@   1 arsis  staff  16645 Nov  1 21:57 T-080-staff-engineer-r3.md
-rw-r--r--@   1 arsis  staff  17820 Nov  1 21:31 T-080-staff-engineer.md
---
---
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:34.650Z

**tool call — Bash**
````
{
 "command": "timeout 300000 .venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider 2>&1 | tail -30",
 "description": "Run unit tests for trace and export"
}
````

### User / tool · 2026-11-02T04:02:34.731Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:36.006Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider 2>&1 | tail -30",
 "description": "Run unit tests for trace and export"
}
````

### User / tool · 2026-11-02T04:02:41.146Z

**tool result**
````
........................................................................ [ 91%]
.......                                                                  [100%]
79 passed in 4.65s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:42.215Z

Unit suite passes: 79 tests. Now the commit diff, which is the actual scope.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:02:42.628Z

**tool call — Bash**
````
{
 "command": "git show 10d358e -- app/backend/trace.py app/backend/export.py app/backend/export_routes.py app/backend/api.py app/backend/store.py",
 "description": "Show backend diff for commit 10d358e"
}
````

### User / tool · 2026-11-02T04:02:42.730Z

**tool result**
````
commit 10d358e06cd37c23c330fe0423629efa02ae0eb2
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:02:07 2026 -0600

    fix(backend): export gate ready equals export allowed; pending items warn, not block (D-045)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index dc95a65..4edd585 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -504,8 +504,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             case = store.export_case(c, token)
             try:
                 ex = XR.export_payload(token, case)
-            except export_mod.JudgeNotRun as e:                       # D-044: the gate lists the same items; no override
-                raise ApiError(422, "judge_not_run", XR.judge_not_run_message(len(e.items)), {"blockers": e.items}) from None
+            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
+                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
             calls = DB.list_llm_calls(c, token)
             ok = ("accepted", "edited")
             tv = present.totals_view(c, token)
diff --git a/app/backend/export.py b/app/backend/export.py
index 021d9ba..3c152fb 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -561,18 +561,28 @@ def _notes(v):
     return "\n".join(sec)
 
 
-class JudgeNotRun(Exception):
-    """D-044: an accepted or edited AI-made item whose second check never ran. The export refuses; there is no override.
-    `items` = [{"item_id", "kind", "reason_code": "JUDGE_NOT_RUN", ...}] as the export gate lists them (trace.judge_not_run_blockers)."""
+class ExportBlocked(Exception):
+    """The export refuses (D-044, D-045): a run in progress or failed, nothing accepted, or accepted AI-made items whose second check never ran. No override.
+    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
+    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""
 
     def __init__(self, items):
-        super().__init__("JUDGE_NOT_RUN")
         self.items = list(items)
+        super().__init__(self.items[0]["reason_code"] if self.items else "EXPORT_BLOCKED")
+
+    @property
+    def code(self) -> str:
+        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"
+
+
+class JudgeNotRun(ExportBlocked):
+    """D-044 alias kept for callers that only care about the judge dimension."""
 
 
 def build_export(case: dict) -> dict:
     """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter.
-    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case)."""
+    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
+    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
     if case.get("judge_not_run"):
         raise JudgeNotRun(case["judge_not_run"])
     v = _View(case)
diff --git a/app/backend/export_routes.py b/app/backend/export_routes.py
index 8ffd119..dddcd10 100644
--- a/app/backend/export_routes.py
+++ b/app/backend/export_routes.py
@@ -25,6 +25,8 @@ def _not_found():
 
 
 def export_payload(token: str, case: dict, now: datetime = None) -> dict:
+    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
+        raise export.ExportBlocked(case["export_blockers"])
     out = export.build_export(case)
     now = now or datetime.now(timezone.utc)
     ok = ("accepted", "edited")
@@ -47,6 +49,12 @@ def export_payload(token: str, case: dict, now: datetime = None) -> dict:
     }
 
 
+def blocked_message(e) -> str:
+    if e.code == "judge_not_run":
+        return judge_not_run_message(len(e.items))
+    return e.items[0]["why"] + " The export is blocked."
+
+
 def judge_not_run_message(n: int) -> str:
     return f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check, so the export is blocked. Run the second check again."
 
@@ -58,6 +66,6 @@ def get_export(token: str):
         return _not_found()
     try:
         return export_payload(token, case)
-    except export.JudgeNotRun as e:      # D-044: accepted items whose second check never ran; the gate lists the same items; no override
-        return JSONResponse(status_code=422, content={"error": {"code": "judge_not_run", "message": judge_not_run_message(len(e.items)),
+    except export.ExportBlocked as e:    # D-044/D-045: the gate lists the same blockers; no override
+        return JSONResponse(status_code=422, content={"error": {"code": e.code, "message": blocked_message(e),
                                                                 "detail": {"blockers": e.items}}})
diff --git a/app/backend/store.py b/app/backend/store.py
index 082664f..fb19393 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -75,7 +75,8 @@ def export_case(conn, case_id: str) -> dict:
     nar = (case.get("config") or {}).get("narrative")
     out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
     from app.backend import trace                       # lazy: trace imports store
-    out["judge_not_run"] = trace.judge_not_run_blockers(conn, case_id)      # D-044: build_export refuses while this is non-empty
+    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
+    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
     ec = (case.get("config") or {}).get("export")
     if ec:
         out["export_config"] = ec
diff --git a/app/backend/trace.py b/app/backend/trace.py
index e3b3e65..a3b3fa6 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -40,7 +40,7 @@ _J_NO_CODE = {"j1": "partially", "j2": "unsure", "j3": "unsure", "j4": "unsure"}
 TRACE_WHY = {
     "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
     "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
-    "ITEMS_PENDING": "Some items have no decision yet, so the export is blocked.",
+    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
     "RUN_IN_PROGRESS": "The AI run is still going.",
     "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
     "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
@@ -653,8 +653,8 @@ def _judge_rows(cx):
 def _judge_never_ran(cx, kind, row):
     """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
     Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
-    if not cx.ran:
-        return []
+    if not cx.ran or _paralegal_wording(kind, row):
+        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
     out = []
     for s in _STEPS_OF[kind](cx, row):
         if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
@@ -664,6 +664,11 @@ def _judge_never_ran(cx, kind, row):
     return out
 
 
+def _paralegal_wording(kind, row) -> bool:
+    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
+    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))
+
+
 def unjudged_items(conn, case_id: str) -> list:
     """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
     [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
@@ -673,8 +678,8 @@ def unjudged_items(conn, case_id: str) -> list:
         row = r["row"]
         if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
             continue
-        if r["kind"] == "entry" and ((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {})):
-            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made, same rule as present.ai_drafted
+        if _paralegal_wording(r["kind"], row):
+            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
         out.append({"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "review_status": row["review_status"], "row": row})
     return out
 
@@ -881,46 +886,55 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     else:
         st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
     # 10 export gate
-    blockers = []
-    if cx.running:
-        blockers.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
-    if case["status"] == "failed":
-        blockers.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
+    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
+    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
     live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
-    for k, x in live_pending:
-        if review.date_unconfirmed(conn, case_id, k, x):
-            blockers.append({"item_id": x["id"], "kind": k, "reason_code": "DATE_UNCONFIRMED", "why": TRACE_WHY["DATE_UNCONFIRMED"],
-                             "next_action": na("CONFIRM_DATE", {"record_id": (x["record_ids"] or [None])[0], "view": "dates_to_confirm"})})
-        else:
-            blockers.append({"item_id": x["id"], "kind": k, "reason_code": "PENDING_DECISION", "why": TRACE_WHY["PENDING_DECISION"],
-                             "next_action": na("DECIDE", {"item_id": x["id"]}, ["accept", "edit", "dismiss"])})
-    jnr = judge_not_run_blockers(conn, case_id) if cx.ran and not cx.running else []
-    blockers.extend(jnr)                                        # D-044: accepted but never double-checked; no override
-    if not live_pending and not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
-        blockers.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
-    ready = bool(rv["ready_to_export"]) and not blockers        # ready == (no blockers): a gate never passes over a listed blocker
-    n_block = len(live_pending)
-    gate_counts = {"blocking": len(blockers), "pending_items": n_block, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"], "dismissed": rv["counts"]["dismissed"],
-                   "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr)}
+    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
+    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
+    ready = not blockers
+    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
+                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr)}
+    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
+                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
     if ready:
-        gate = step("export_gate", "Ready to export?", "code", PASS, "Every live item has your decision and at least one item is accepted, so the export can be built.", rule="row 19", counts=gate_counts)
+        gate = step("export_gate", "Ready to export?", "code", PASS,
+                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else ""),
+                    rule="row 19", counts=gate_counts)
     else:
-        first = blockers[0] if blockers else None
-        reason = "ITEMS_PENDING" if n_block else (first["reason_code"] if first else "ITEMS_PENDING")
-        text = (f"{n_block} item{'s have' if n_block != 1 else ' has'} no decision yet, so the export is blocked." if n_block
-                else f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again." if jnr and first is jnr[0]
-                else (first["why"] if first else TRACE_WHY["ITEMS_PENDING"]))
-        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=reason, rule="row 19", counts=gate_counts, next_action=first["next_action"] if first else None,
+        first = blockers[0]
+        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
+                if jnr and first is jnr[0] else first["why"])
+        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                     blocks=True)
-    gate.update(ready=ready, blockers=blockers)
+    gate.update(ready=ready, blockers=blockers, warnings=warnings)
     st.append(gate)
     _number(st)
     verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
-               else {"code": "ready", "label": "Ready to export"} if ready
-               else {"code": "needs_attention", "label": f"{n_block} item{'s' if n_block != 1 else ''} still need{'' if n_block != 1 else 's'} your decision" if n_block
-                     else f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
+               else {"code": "ready", "label": "Ready to export" + (f" ({n_pend} not reviewed)" if n_pend else "")} if ready
+               else {"code": "needs_attention", "label": f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
     return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}
 
 
+def pending_warning(n: int) -> str:
+    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."
+
+
+def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
+    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
+    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
+    cx = cx or _Cx(conn, case_id, False)
+    rv = rv or present.review_view(conn, case_id)
+    out = []
+    if cx.running:
+        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
+    if cx.case["status"] == "failed":
+        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
+    if cx.ran and not cx.running:
+        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
+    if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
+        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
+    return out
+
+
 def rows_any(jr):
     return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:03.344Z

The backend diff is in view. Next I need the helpers it calls: `review_view`'s `ready_to_export`, `judge_not_run_blockers`, the export caller graph, and the new tests.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:04.554Z

**tool call — Bash**
````
{
 "command": "grep -n \"ready_to_export\\|def review_view\\|def judge_not_run_blockers\\|def unjudged_items\\|def _judge_rows\\|def judge_report\\|def date_unconfirmed\\|def case_trace\\|class _Cx\\|def present\\|_judge_never_ran(\" app/backend/*.py | head -40; echo ---; grep -rn \"build_export\\|export_payload\\|export_blockers\\|judge_not_run\\|JudgeNotRun\\|ExportBlocked\" app --include=*.py | grep -v \"^app/backend/trace.py:8[89]\" ; echo ---; grep -rn \"ITEMS_PENDING\\|ITEMS_NOT_REVIEWED\\|export_blocked\\|judge_not_run\\|Export blocked\" app/frontend tests memory/contracts docs 2>/dev/null | head -40",
 "description": "Trace helper definitions and all export callers"
}
````

### User / tool · 2026-11-02T04:03:04.693Z

**tool result**
````
app/backend/api.py:539:    def case_trace(token: str):
app/backend/api.py:548:    def judge_report(token: str):
app/backend/review.py:42:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
app/backend/present.py:113:def review_view(conn, case_id):
app/backend/present.py:122:            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}
app/backend/trace.py:120:class _Cx:
app/backend/trace.py:637:def _judge_rows(cx):
app/backend/trace.py:644:                out.extend(_judge_never_ran(cx, kind, row))
app/backend/trace.py:653:def _judge_never_ran(cx, kind, row):
app/backend/trace.py:672:def unjudged_items(conn, case_id: str) -> list:
app/backend/trace.py:687:def judge_not_run_blockers(conn, case_id: str) -> list:
app/backend/trace.py:697:def judge_report(conn, case_id: str, full: bool = False) -> dict:
app/backend/trace.py:772:def case_trace(conn, case_id: str, full: bool = False) -> dict:
---
app/backend/store.py:37:    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
app/backend/store.py:78:    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
app/backend/store.py:79:    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/trace.py:687:def judge_not_run_blockers(conn, case_id: str) -> list:
app/backend/trace.py:922:def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
app/backend/trace.py:924:    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
app/backend/trace.py:933:        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
app/backend/narrative.py:157:    """The small dict export.build_export() reads."""
app/backend/api.py:506:                ex = XR.export_payload(token, case)
app/backend/api.py:507:            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
app/backend/export.py:4:    build_export(case) -> {"letter_text": str, "internal_notes_text": str, "counts": {...}}  (counts: R-EX-5, outside both blocks)
app/backend/export.py:564:class ExportBlocked(Exception):
app/backend/export.py:566:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
app/backend/export.py:575:        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"
app/backend/export.py:578:class JudgeNotRun(ExportBlocked):
app/backend/export.py:582:def build_export(case: dict) -> dict:
app/backend/export.py:584:    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
app/backend/export.py:585:    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
app/backend/export.py:586:    if case.get("judge_not_run"):
app/backend/export.py:587:        raise JudgeNotRun(case["judge_not_run"])
app/backend/export_routes.py:1:"""GET /api/cases/{token}/export: thin router around export.build_export (T-041). Code only.
app/backend/export_routes.py:27:def export_payload(token: str, case: dict, now: datetime = None) -> dict:
app/backend/export_routes.py:28:    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
app/backend/export_routes.py:29:        raise export.ExportBlocked(case["export_blockers"])
app/backend/export_routes.py:30:    out = export.build_export(case)
app/backend/export_routes.py:53:    if e.code == "judge_not_run":
app/backend/export_routes.py:54:        return judge_not_run_message(len(e.items))
app/backend/export_routes.py:58:def judge_not_run_message(n: int) -> str:
app/backend/export_routes.py:68:        return export_payload(token, case)
app/backend/export_routes.py:69:    except export.ExportBlocked as e:    # D-044/D-045: the gate lists the same blockers; no override
---
app/frontend/stepper.js:309:  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the review queue stays on the first screen.
app/frontend/stepper.js:352:    else if (gate) gateText = "Export blocked by " + (n || 1);
tests/unit/test_trace.py:348:    assert w["reason_code"] == "ITEMS_NOT_REVIEWED" and w["count"] == len(expected) and w["next_action"]["code"] == "DECIDE"
tests/unit/test_trace.py:709:    assert gate["ready"] is False and gate["status"] == "fail" and gate["counts"]["judge_not_run"] == len(got)
tests/unit/test_trace.py:720:    assert r.status_code == 422 and r.json()["error"]["code"] == "judge_not_run"
tests/unit/test_trace.py:752:    assert _jnr(g) == [] and g["counts"]["judge_not_run"] == 0 and g["ready"] is False
tests/unit/test_trace.py:827:    assert g["ready"] is False and {b["reason_code"] for b in g["blockers"]} == {"JUDGE_NOT_RUN"} and ex.json()["error"]["code"] == "judge_not_run"
tests/unit/test_trace.py:830:    assert [b["reason_code"] for b in g["blockers"]] == ["RUN_FAILED"] and ex.json()["error"]["code"] == "export_blocked"
tests/unit/test_export.py:190:        X.build_export(dict(case, judge_not_run=blockers))
tests/unit/test_export.py:191:    assert ei.value.items == blockers and ei.value.code == "judge_not_run"
tests/unit/test_export.py:194:def test_export_blocked_code_is_judge_not_run_only_when_every_blocker_is():
tests/unit/test_export.py:195:    assert X.ExportBlocked([{"reason_code": "RUN_FAILED"}]).code == "export_blocked"
tests/unit/test_export.py:196:    assert X.ExportBlocked([{"reason_code": "JUDGE_NOT_RUN"}, {"reason_code": "RUN_FAILED"}]).code == "export_blocked"
tests/unit/test_export.py:197:    assert X.ExportBlocked([{"reason_code": "JUDGE_NOT_RUN"}]).code == "judge_not_run"
tests/e2e/conftest.py:19:  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
tests/e2e/test_stepper.py:132:    assert re.search(r"\d+/10 checks passed", txt) and re.search(r"\d+ need you", txt) and re.search(r"Export blocked by \d+", txt)
memory/contracts/api.md:30:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
memory/contracts/api.md:286:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
memory/contracts/api.md:534:      "counts": {"blocking": 1, "pending_items": 21, "date_unconfirmed": 1, "accepted": 0, "dismissed": 0, "rejected_not_blocking": 1, "judge_not_run": 0},
memory/contracts/api.md:536:      "warnings": [ { "reason_code": "ITEMS_NOT_REVIEWED", "count": 21, "why": "21 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "text": "...", "target": {"view": "queue"}} } ],
memory/contracts/api.md:543:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:07.593Z

Callers are confined to `store.export_case` and `export_routes`, so no export path bypasses the guard. Now the gate's inputs: `review_view`, the judge helpers, and the gate block as committed.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:08.243Z

**tool call — Bash**
````
{
 "command": "sed -n 113,125p app/backend/present.py; echo ----TRACE637-700; sed -n 637,700p app/backend/trace.py; echo ----CASETRACE-tail; sed -n 886,945p app/backend/trace.py",
 "description": "Read review_view, judge helpers, and gate code in trace.py"
}
````

### User / tool · 2026-11-02T04:03:08.339Z

**tool result**
````
def review_view(conn, case_id):
    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
    live = [(k, r) for k, r in items if r["state"] != "rejected"]
    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
    rank = {"amount": 0, "entry": 1, "flag": 2}
    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
    return {"counts": counts, "queue": [r["id"] for _, r in pend],
            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}


def dates_to_confirm(conn, case_id):
----TRACE637-700
def _judge_rows(cx):
    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
    out = []
    for kind in ("entry", "amount", "flag"):
        for row in DB.list_items(cx.conn, cx.case_id, kind):
            jd = (row.get("ladder") or {}).get("judge")
            if not jd or not jd.get("verdict"):
                out.extend(_judge_never_ran(cx, kind, row))
                continue
            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
            call = cx.call(jd.get("call_id"), row["id"], jid)
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": _norm_verdict(jid, jd["verdict"]),
                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
    return out


def _judge_never_ran(cx, kind, row):
    """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
    if not cx.ran or _paralegal_wording(kind, row):
        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
    out = []
    for s in _STEPS_OF[kind](cx, row):
        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
                and (s.get("evidence") or {}).get("judge_verdict") == "unavailable":
            jid = "j" + s["id"].split("_")[1]
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
    return out


def _paralegal_wording(kind, row) -> bool:
    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))


def unjudged_items(conn, case_id: str) -> list:
    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
    cx = _Cx(conn, case_id, False)
    out = []
    for r in _judge_rows(cx):
        row = r["row"]
        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
            continue
        if _paralegal_wording(r["kind"], row):
            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
        out.append({"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "review_status": row["review_status"], "row": row})
    return out


def judge_not_run_blockers(conn, case_id: str) -> list:
    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one."""
    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id) if u["review_status"] in ("accepted", "edited")]


def _jnr_blocker(u):
    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN"],
            "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}


def judge_report(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    rows = _judge_rows(cx)
    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
----CASETRACE-tail
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else ""),
                    rule="row 19", counts=gate_counts)
    else:
        first = blockers[0]
        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
                if jnr and first is jnr[0] else first["why"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                    blocks=True)
    gate.update(ready=ready, blockers=blockers, warnings=warnings)
    st.append(gate)
    _number(st)
    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
               else {"code": "ready", "label": "Ready to export" + (f" ({n_pend} not reviewed)" if n_pend else "")} if ready
               else {"code": "needs_attention", "label": f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def pending_warning(n: int) -> str:
    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."


def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    cx = cx or _Cx(conn, case_id, False)
    rv = rv or present.review_view(conn, case_id)
    out = []
    if cx.running:
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
    if cx.case["status"] == "failed":
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
    if cx.ran and not cx.running:
        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
    if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
    return out


def rows_any(jr):
    return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:18.078Z

The gate and the export share `export_blockers`, and `ready` is now `not blockers`. Next I'll check the invariant test, the pending tests, and the rest of the commit's tests.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:18.511Z

**tool call — Bash**
````
{
 "command": "git show 10d358e -- tests/unit/test_trace.py | head -300",
 "description": "Show test_trace.py diff for commit 10d358e"
}
````

### User / tool · 2026-11-02T04:03:18.620Z

**tool result**
````
commit 10d358e06cd37c23c330fe0423629efa02ae0eb2
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:02:07 2026 -0600

    fix(backend): export gate ready equals export allowed; pending items warn, not block (D-045)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_trace.py b/tests/unit/test_trace.py
index 4b3354a..67a7dd8 100644
--- a/tests/unit/test_trace.py
+++ b/tests/unit/test_trace.py
@@ -331,7 +331,7 @@ def test_case_trace_steps_and_counts(env):
     assert ct["progress"]["total"] == 10
 
 
-def test_export_gate_lists_exactly_the_pending_live_items(env):
+def test_pending_live_items_are_a_warning_not_a_blocker_d045(env):
     c, conn, tok, _ = env
     e = DB.get_item(conn, "e3", tok)
     DB.update_item(conn, "e3", case=tok, state="rejected", state_reasons_json=["GROUNDING_EXCERPT_NOT_VERBATIM"], ladder=e["ladder"])
@@ -341,9 +341,16 @@ def test_export_gate_lists_exactly_the_pending_live_items(env):
     gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
     expected = {x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k] if x["review_status"] == "pending"}
     assert expected == set(case["review"]["queue"])
-    assert {b["item_id"] for b in gate["blockers"]} == expected and "e3" not in expected and "e1" not in expected and "e2" not in expected
-    assert gate["ready"] is False and gate["status"] == "fail" and gate["reason_code"] == "ITEMS_PENDING" and gate["counts"]["rejected_not_blocking"] == 1
-    assert all(b["reason_code"] == "PENDING_DECISION" and b["why"] and b["next_action"]["code"] == "DECIDE" for b in gate["blockers"])
+    assert "e3" not in expected and "e1" not in expected and "e2" not in expected and expected
+    assert gate["blockers"] == [] and gate["ready"] is True and gate["status"] == "pass" and gate["counts"]["rejected_not_blocking"] == 1
+    assert gate["counts"]["pending_items"] == len(expected) and gate["counts"]["blocking"] == 0
+    w, = gate["warnings"]
+    assert w["reason_code"] == "ITEMS_NOT_REVIEWED" and w["count"] == len(expected) and w["next_action"]["code"] == "DECIDE"
+    assert "will not be in the letter" in w["why"] and "AI disclosure line will count" in w["why"]
+    assert c.get(f"/api/cases/{tok}/export").status_code == 200
+    notes = c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"]
+    assert f"Items not reviewed: {len(expected)}" in notes
+    assert c.get(f"/api/cases/{tok}/trace").json()["verdict"]["code"] == "ready"
 
 
 def test_export_gate_date_unconfirmed_blocker(env):
@@ -351,8 +358,8 @@ def test_export_gate_date_unconfirmed_blocker(env):
     rid = DB.get_item(conn, "e5", tok)["record_ids"][0]
     conn.execute("UPDATE records SET date_status='ambiguous', date_candidates_json=? WHERE id=? AND case_id=?", (json.dumps(["2026-04-05", "2026-05-04"]), rid, tok))
     gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
-    b = next(x for x in gate["blockers"] if x["item_id"] == "e5")
-    assert b["reason_code"] == "DATE_UNCONFIRMED" and b["next_action"]["code"] == "CONFIRM_DATE"
+    assert all(x["item_id"] != "e5" for x in gate["blockers"]) and gate["counts"]["date_unconfirmed"] == 1       # D-045(a): pending, so it warns; accepting it is refused (D-041)
+    assert [x["reason_code"] for x in gate["blockers"]] == ["NOTHING_ACCEPTED"] and gate["warnings"][0]["count"] >= 1
     assert steps_of(c.get(f"/api/cases/{tok}/trace").json())["dates"]["status"] == "fail"
 
 
@@ -735,7 +742,7 @@ def test_dismissing_or_resetting_an_unjudged_item_clears_its_blocker(env):
     c.post(f"/api/cases/{tok}/items/{ids[1]}/review", json={"action": "reset"})
     g = _gate(c, tok)
     assert ids[1] not in [b["item_id"] for b in _jnr(g)]
-    assert any(b["item_id"] == ids[1] and b["reason_code"] in ("PENDING_DECISION", "DATE_UNCONFIRMED") for b in g["blockers"])   # now it needs a decision instead
+    assert all(b["item_id"] != ids[1] for b in g["blockers"]) and g["counts"]["pending_items"] >= 1                         # now it is pending: a warning, not a blocker
 
 
 def test_pending_unjudged_items_are_not_judge_blockers_yet(env):
@@ -764,28 +771,98 @@ def test_entry_with_a_summary_the_paralegal_wrote_is_not_ai_made(env):
     assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]
 
 
-def test_gate_and_export_agree_on_the_judge_dimension_in_every_state(env):
-    """gate ready => export allowed; a JUDGE_NOT_RUN blocker <=> export 422; ready == (blockers == []) throughout."""
+def _accept_all_but(c, tok, keep_pending):
+    case = c.get(f"/api/cases/{tok}").json()
+    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
+        if x["id"] not in keep_pending:
+            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
+
+
+def test_gate_ready_equals_export_allowed_in_every_state_d045(env):
+    """The invariant: gate.ready == (GET /export is not 4xx) == (gate.blockers == []), whatever the state. Pending items warn, never block."""
     c, conn, tok, _ = env
-    checks = 0
-    n = _blank_judges(conn, tok)
-    assert n
-    states = []
-    states.append(("pending, judges missing", lambda: None))
-    states.append(("all accepted, judges missing", lambda: _accept_all(c, tok)))
-    states.append(("judges answered", lambda: c.post(f"/api/cases/{tok}/rejudge").status_code == 200))
-    for name, act in states:
-        act()
+    seen = {}
+
+    def check(name):
         g = _gate(c, tok)
         ex = c.get(f"/api/cases/{tok}/export")
         assert g["ready"] == (g["blockers"] == []), name
-        assert bool(_jnr(g)) == (ex.status_code == 422), name
-        if g["ready"]:
-            assert ex.status_code == 200, name
-        if ex.status_code == 422:
-            assert g["ready"] is False, name
-        checks += 1
-    assert checks == 3 and g["ready"] is True and ex.status_code == 200
+        assert g["ready"] == (ex.status_code < 400), (name, ex.status_code, [b["reason_code"] for b in g["blockers"]])
+        assert g["status"] == ("pass" if g["ready"] else "fail"), name
+        assert bool(_jnr(g)) == (ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"] != [] and any(b["reason_code"] == "JUDGE_NOT_RUN" for b in ex.json()["error"]["detail"]["blockers"])), name
+        if ex.status_code >= 400:
+            assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name     # the same list
+        seen[name] = (g, ex)
+
+    check("nothing decided yet (pending only)")
+    case = c.get(f"/api/cases/{tok}").json()
+    all_ids = [x["id"] for x in [*case["entries"], *case["amounts"], *case["flags"]]]
+    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
+    check("one accepted, rest pending")
+    _accept_all_but(c, tok, keep_pending={all_ids[-1]})
+    check("all accepted but one")
+    n = _blank_judges(conn, tok)
+    assert n
+    check("accepted, judge not run")
+    assert c.post(f"/api/cases/{tok}/rejudge").status_code == 200
+    check("judges answered, one pending")
+    DB.update_case(conn, tok, status="failed")
+    check("run failed")
+    DB.update_case(conn, tok, status="running")
+    check("run in progress")
+    DB.update_case(conn, tok, status="ready")
+    _accept_all(c, tok)
+    check("all clear")
+    for i in all_ids:
+        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"})
+    check("everything dismissed")
+
+    g, ex = seen["nothing decided yet (pending only)"]
+    assert [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"] and ex.status_code == 422
+    g, ex = seen["one accepted, rest pending"]
+    assert g["ready"] is True and ex.status_code == 200 and g["warnings"][0]["count"] > 0 and "Items not reviewed" in ex.json()["internal_notes_text"]
+    g, ex = seen["all accepted but one"]
+    assert g["ready"] is True and g["counts"]["pending_items"] == 1 and "Items not reviewed: 1" in ex.json()["internal_notes_text"]
+    g, ex = seen["accepted, judge not run"]
+    assert g["ready"] is False and {b["reason_code"] for b in g["blockers"]} == {"JUDGE_NOT_RUN"} and ex.json()["error"]["code"] == "judge_not_run"
+    assert seen["judges answered, one pending"][0]["ready"] is True
+    g, ex = seen["run failed"]
+    assert [b["reason_code"] for b in g["blockers"]] == ["RUN_FAILED"] and ex.json()["error"]["code"] == "export_blocked"
+    assert "RUN_IN_PROGRESS" in [b["reason_code"] for b in seen["run in progress"][0]["blockers"]]
+    g, ex = seen["all clear"]
+    assert g["ready"] is True and g["warnings"] == [] and ex.status_code == 200
+    assert seen["everything dismissed"][0]["ready"] is False
+
+
+def test_paralegal_edited_summary_is_not_counted_unchecked_in_judges_d045b(env):
+    c, conn, tok, _ = env
+    _blank_judges(conn, tok)
+    case = c.get(f"/api/cases/{tok}").json()
+    ent = [x["id"] for x in case["entries"]]
+    target = ent[0]
+    DB.apply_review(conn, target, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
+    rep = c.get(f"/api/cases/{tok}/judges").json()
+    assert target not in [u["item_id"] for u in rep["unresolved"]]
+    assert rep["totals"]["unavailable"] == len(trace.unjudged_items(conn, tok)) and target not in [u["item_id"] for u in trace.unjudged_items(conn, tok)]
+
+
+def test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b(env):
+    c, conn, tok, _ = env
+    # every judge answered except one entry the paralegal then rewrites; dismiss the rest so only that item is live
+    case = c.get(f"/api/cases/{tok}").json()
+    target = case["entries"][0]["id"]
+    row = DB.get_item(conn, target, tok)
+    lad = row["ladder"]
+    lad["judge"] = None
+    DB.update_item(conn, target, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
+    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, target))
+    before = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
+    assert before["status"] == "fail"
+    DB.apply_review(conn, target, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
+    ct = c.get(f"/api/cases/{tok}/trace").json()
+    assert steps_of(ct)["judges"]["status"] != "fail" and steps_of(ct)["judges"]["counts"]["unavailable"] == 0
+    g = steps_of(ct)["export_gate"]
+    assert g["ready"] is True and ct["verdict"]["code"] == "ready" and c.get(f"/api/cases/{tok}/export").status_code == 200
 
 
 # ------------------------------------------------------------------ the rejudge route
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:30.410Z

The invariant test covers eight states and compares `ready` against the HTTP status. Next I'll check the claims the test does not reach: `_Cx` run flags, the date-confirm accept guard (D-041), the rejudge target set, and the status-code language in the spec.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:31.798Z

**tool call — Bash**
````
{
 "command": "sed -n 120,140p app/backend/trace.py; echo ----REJUDGE; grep -n \"unjudged_items\\|targets\\|asked\" app/backend/rejudge.py | head; echo ----TESTASK; grep -n 'asked' tests/unit/test_trace.py | head -5; echo ----DATEGUARD; grep -rn \"date_unconfirmed\" app/backend/*.py | head; echo ----SPEC; grep -rn \"422\\|409\" spec/REQUIREMENTS.md spec/SPEC.md docs/CONTRACT.md 2>/dev/null | head -10; echo ----RUNNING; grep -n \"running\\b\" app/backend/trace.py | head -8; echo ---WARN_MENTION; grep -n \"warning\" app/backend/export*.py | head",
 "description": "Check _Cx flags, rejudge targets, date guard, spec status codes"
}
````

### User / tool · 2026-11-02T04:03:31.949Z

**tool result**
````
class _Cx:
    def __init__(self, conn, case_id, full):
        self.conn, self.case_id, self.full = conn, case_id, bool(full)
        self.case = DB.get_case(conn, case_id)
        self.recs = present._recs_by_id(conn, case_id)
        calls = DB.list_llm_calls(conn, case_id)
        self.call_by_id = {c["id"]: c for c in calls}
        self.calls_by_item = {}
        for c in calls:
            self.calls_by_item.setdefault(c["item_id"], []).append(c)
        self.events = {}
        for e in DB.list_events(conn, case_id):
            self.events.setdefault(e["item_id"], []).append(e)
        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
        self.ran = self.case.get("run_started_at") is not None
        self.running = self.case["status"] == "running"

    def call(self, call_id, item_id=None, step_name=None):
        if call_id and call_id in self.call_by_id:
            return self.call_by_id[call_id]
        if item_id and step_name:
----REJUDGE
4:    Targets: live (not rejected, not dismissed) AI-made entries, charges and flags with a judge verdict of 'unavailable' or no verdict (trace.unjudged_items).
60:    targets = trace.unjudged_items(conn, case_id)
62:        answers = list(ex.map(lambda x: _safe_ask(x, case_text, call), targets))
64:    for tg, (verdict, call_id, code) in zip(targets, answers):
82:    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
----TESTASK
879:    assert out["asked"] >= len(todo) and sorted(x["item_id"] for x in out["rejudged"] if x["item_id"] in todo) == todo and out["still_unavailable"] == []
882:    assert len(new) == out["asked"] and {x["backend"] for x in new} == {"fixture"} and {x["role"] for x in new} == {"judge"}      # audited, fixture only
896:    assert r.status_code == 200 and r.json()["asked"] == 0 and r.json()["rejudged"] == []
906:    assert r["asked"] == n
954:    assert len(seen) == r["asked"] and {i for _, i in seen} >= set(todo)
----DATEGUARD
app/backend/case_extras.py:35:        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
app/backend/case_extras.py:36:            bad.append({"id": i, "reason": "date_unconfirmed"})
app/backend/case_extras.py:118:                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
app/backend/review.py:42:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
app/backend/review.py:54:def _date_unconfirmed_error():
app/backend/review.py:67:    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
app/backend/review.py:68:        raise _date_unconfirmed_error()
app/backend/trace.py:350:    unconf = review.date_unconfirmed(cx.conn, cx.case_id, "entry", row)
app/backend/trace.py:893:    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
app/backend/trace.py:895:    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
----SPEC
spec/REQUIREMENTS.md:84:| R-CH-7 | **Charges are accept / dismiss only (D-010, ADR-017).** A charge's class comes from code and judge #2; the paralegal can't reclassify or edit it, so no path turns a rate, estimate or unreadable amount into a totaled charge. Reclassification is non-goal 15. | UT: any edit on a charge (amount, class, excerpt) → 422 `invalid_edit`; the review endpoint accepts only `accept`, `dismiss` and `reset` for amounts. After accepting the $185 rate the Accepted total is still $8,390 and `letter_text` has no $185. | UT + E2E |
spec/REQUIREMENTS.md:93:| R-RV-2 | **What each action does (D-010, D-012).** See the table below the requirements. Originals are kept. "Edited" shows in the review UI and in the internal notes, never in the letter text. | UT, each → 422 `invalid_edit`: edit an entry's date or provider; edit a flag's evidence, type or title; edit a charge's amount or class; any other key. `confirm_date` (`POST /records/{rid}/confirm_date`): a date that is not one of the code-proposed readings → 422 `date_invalid`; a record with no readable date (no readings) cannot be confirmed. Also → 422 `invalid_edit`: an excerpt edit that is not a contiguous run of whole sentence units of the same record; an excerpt edit that drops a hedge-set unit (R-TL-8). `confirm_date` on `case_01` record 8 with 2026-05-04 → 200, a review event is logged, the entry joins the timeline. E2E: edit entry 3's summary → "edited" label in the UI; the letter shows the new summary with its citation and no "edited" mark; the notes list the original and the new text. | UT + E2E |
spec/REQUIREMENTS.md:94:| R-RV-3 | **Edited text is re-checked.** The D-006 code check (numbers, dates, `$` in the new summary must appear in the excerpt) and judge #1 run on every edited summary and on every re-selected excerpt. If the code check or the judge objects (`partially`/`unsupported`), nothing is saved and the response is 409 `needs_confirm` with the reasons; if she chooses "keep my wording" the edit is resent with confirmation, saved, logged and shown in the internal notes. If the code check passes but the judge is unavailable (error, timeout, no recorded answer; always so in demo mode), the edit is saved as `edited` with state `needs_review` (`JUDGE_UNAVAILABLE`). | UT: summary edited to add "$9,000" → 409 `needs_confirm` (code token check). Seeded edit adding "herniation" → judge returns `partially` or `unsupported` → 409 `needs_confirm`. Resending with confirmation saves it. Judge unavailable → saved, `needs_review`, `JUDGE_UNAVAILABLE`. Structurally invalid edits are 422 `invalid_edit` (R-RV-2); judge or token objections are 409, never 422. | UT + EV (judge) + E2E |
spec/REQUIREMENTS.md:370:| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
----RUNNING
135:        self.running = self.case["status"] == "running"
849:        if cx.running:
912:    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
928:    if cx.running:
932:    if cx.ran and not cx.running:
---WARN_MENTION
app/backend/export_routes.py:48:        "warnings": [],
app/backend/export.py:36:_TYPE_RANK = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
app/backend/export.py:260:    if t == "record_warning":
app/backend/export.py:261:        return "Record warning"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:37.933Z

Two things to pin down before mutating: the spec's wording on export refusal, and whether the rejudge target set still includes pending items (r3 minor 2).

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:38.735Z

**tool call — Bash**
````
{
 "command": "sed -n 122,123p spec/REQUIREMENTS.md | cut -c1-1200; echo ----; sed -n 896,910p tests/unit/test_trace.py; echo ----; grep -n \"D-044\\|D-045\" memory/DECISIONS.md | head -5; grep -n \"422\\|409\" memory/DECISIONS.md | grep -i \"export\" | head -5",
 "description": "Read R-EX-4/R-EX-5 and rejudge test assertions"
}
````

### User / tool · 2026-11-02T04:03:38.847Z

**tool result**
````
| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in
| R-EX-5 | The UI shows counts outside the copied text: "N entries, N charges in letter · N flags in internal notes · N of 9 records in letter · N items pending (N flags)". The count line is part of neither block. **Copy asks for one confirmation when anything is pending**, stating the pending numbers and naming pending flags separately (a pending flag may be one the attorney needs to see). | E2E: leave the 73-day gap flag pending, click Copy letter → the confirm reads "1 flag not reviewed"; the count line shows it. Click Copy for each block, read the clipboard, assert no count line in either. | E2E |
----
    assert r.status_code == 200 and r.json()["asked"] == 0 and r.json()["rejudged"] == []
    assert len(DB.list_llm_calls(conn, tok)) == before


def test_rejudge_only_touches_items_whose_judge_never_ran(env):
    c, conn, tok, _ = env
    n = _blank_judges(conn, tok)
    keep = {r["id"]: json.dumps(r["ladder"], sort_keys=True) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k)
            if (r["ladder"] or {}).get("judge")}
    r = c.post(f"/api/cases/{tok}/rejudge").json()
    assert r["asked"] == n
    for k in ("entry", "amount", "flag"):
        for row in DB.list_items(conn, tok, k):
            if row["id"] in keep:
                assert json.dumps(row["ladder"], sort_keys=True) == keep[row["id"]], row["id"]
----
341:- Decision: the LLM split fallback is allowed only when the code split finds one record that is unsplit or lacks a date or source label; it returns offsets only, is validated by `ingest.validate_split` and marks records `LLM_SPLIT`; on a failed validation or failed call the paste stays one record with `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` and a reason (with no model wired in, the reason is `NO_MODEL`; an unsplit tail after several records gives `NOT_ATTEMPTED`, never silently: T-066, d148e0f). Manual entry runs code checks then judge 1 on her summary; "not a duplicate" is code for the undo and log, then the generator, judge 1 and the amount judge for the split-off record; batch accept (verified pending entries only) is code only (on a 404/405 the UI shows an error and accepts nothing: T-065). The firm-voice paragraph is returned sentence by sentence by the model, with per-sentence code checks and judge 1 on accepted entries only, internal until accepted. D-032 keeps normal or negative findings context-only, and D-038 narrows it so defense credibility phrases (Waddell, "out of proportion", symptom magnification) raise a flag under category `credibility_language` (T-067, commit 59c7edb); D-040 cuts the patient self-report chip (supersedes D-033, D-035 and D-037; T-071, commit a27e3a4; T-072 open for the `patient_reported_onset` title and export wording); D-034 makes numeric mismatches a hard 422. These supersede the matching cut items in ADR-015 and the batch/override text in ADR-005. Plain-language table: `docs/LLM_VS_CODE.md`.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:46.313Z

I have what I need from the code. Next is the mutation run, in a scratch copy under the scratchpad (not in the product tree), starting with a baseline and a check that the scratch copy imports its own `app/`.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:48.231Z

**tool call — Bash**
````
{
 "command": "set -e; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"$S\"; mkdir -p \"$S/t080r4\"; cd /Users/arsis/zlayt-pm-project && git archive 10d358e | tar -x -C \"$S/t080r4\"; ls \"$S/t080r4\" | head -40; cd \"$S/t080r4\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import app,sys; print(app.__file__)\"; ls \"$S/t080r4/tests\" | head",
 "description": "Export commit 10d358e into a scratchpad copy and verify imports"
}
````

### User / tool · 2026-11-02T04:03:48.571Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
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
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t080r4/app/__init__.py
__init__.py
conftest.py
e2e
fixtures
unit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:50.526Z

The scratch copy imports its own `app/`. Now the baseline and the mutants, each applied to a fresh copy of the two backend files it touches.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:03:56.751Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/mut\"; cat > \"$S/mut/run_mutants.py\" <<'EOF'\nimport shutil, subprocess, sys, re, pathlib\nBASE = pathlib.Path(sys.argv[1])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nMUTANTS = {\n \"M1 gate drops JUDGE_NOT_RUN from shared list (trace.py)\": (\"app/backend/trace.py\",\n   'blockers = export_blockers(conn, case_id, cx, rv)          # D-045',\n   'blockers = [b for b in export_blockers(conn, case_id, cx, rv) if b[\"reason_code\"] != \"JUDGE_NOT_RUN\"]          # D-045'),\n \"M2 store.export_case passes no blockers (store.py)\": (\"app/backend/store.py\",\n   'out[\"export_blockers\"] = trace.export_blockers(conn, case_id)',\n   'out[\"export_blockers\"] = []'),\n \"M3 export_payload guard removed (export_routes.py)\": (\"app/backend/export_routes.py\",\n   'if case.get(\"export_blockers\"):                  # D-045',\n   'if False:                  # D-045'),\n \"M4 pending items block again (trace.export_blockers)\": (\"app/backend/trace.py\",\n   '    if not (rv[\"counts\"][\"accepted\"] + rv[\"counts\"][\"edited\"]):\\n        out.append({\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"NOTHING_ACCEPTED\"',\n   '    if any(r[\"review_status\"] == \"pending\" and r[\"state\"] != \"rejected\" for k in (\"entry\",\"amount\",\"flag\") for r in __import__(\"app.backend.db\", fromlist=[\"x\"]).list_items(conn, case_id, k)):\\n        out.append({\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"ITEMS_PENDING\", \"why\": \"pending\", \"next_action\": None})\\n    if not (rv[\"counts\"][\"accepted\"] + rv[\"counts\"][\"edited\"]):\\n        out.append({\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"NOTHING_ACCEPTED\"'),\n \"M5 NOTHING_ACCEPTED dropped from shared list (trace.py)\": (\"app/backend/trace.py\",\n   '    if not (rv[\"counts\"][\"accepted\"] + rv[\"counts\"][\"edited\"]):\\n        out.append',\n   '    if False:\\n        out.append'),\n \"M6 paralegal exemption removed from judges step (trace.py _judge_never_ran)\": (\"app/backend/trace.py\",\n   'if not cx.ran or _paralegal_wording(kind, row):',\n   'if not cx.ran:'),\n \"M7 gate ready ignores blockers (trace.py)\": (\"app/backend/trace.py\",\n   '    ready = not blockers\\n',\n   '    ready = not [b for b in blockers if b[\"reason_code\"] != \"NOTHING_ACCEPTED\"]\\n'),\n}\ndef run(tag, edits):\n    d = pathlib.Path(str(BASE) + \"_\" + tag)\n    if d.exists(): shutil.rmtree(d)\n    shutil.copytree(BASE, d, ignore=shutil.ignore_patterns(\"__pycache__\"))\n    for rel, old, new in edits:\n        p = d / rel; s = p.read_text()\n        n = s.count(old)\n        assert n == 1, (tag, rel, n)\n        p.write_text(s.replace(old, new))\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"tests/unit/test_trace.py\", \"tests/unit/test_export.py\", \"-p\", \"no:cacheprovider\"],\n                       cwd=d, capture_output=True, text=True)\n    last = [l for l in r.stdout.strip().splitlines() if l.strip()][-1]\n    failed = [l for l in r.stdout.splitlines() if l.startswith(\"FAILED\")]\n    print(f\"{tag}: rc={r.returncode} | {last}\")\n    for l in failed[:6]: print(\"    \", l[:230])\n    shutil.rmtree(d)\nrun(\"baseline\", [])\nfor name, (rel, old, new) in MUTANTS.items():\n    run(name.split()[0], [(rel, old, new)])\n    print(\"   \", name)\nEOF\ncd \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/mut/run_mutants.py\" \"$S/t080r4\" 2>&1 | tail -80",
 "description": "Run baseline and seven mutants in scratch copy"
}
````

### User / tool · 2026-11-02T04:04:40.810Z

**tool result**
````
baseline: rc=0 | 79 passed in 4.97s
M1: rc=1 | 9 failed, 70 passed in 4.69s
     FAILED tests/unit/test_trace.py::test_accepted_items_whose_judge_never_ran_are_gate_blockers_with_a_next_action
     FAILED tests/unit/test_trace.py::test_export_refuses_422_for_the_same_items_the_gate_lists
     FAILED tests/unit/test_trace.py::test_dismissing_or_resetting_an_unjudged_item_clears_its_blocker
     FAILED tests/unit/test_trace.py::test_reviewer_written_entry_is_not_ai_made_so_it_never_needs_the_judge
     FAILED tests/unit/test_trace.py::test_entry_with_a_summary_the_paralegal_wrote_is_not_ai_made
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
    M1 gate drops JUDGE_NOT_RUN from shared list (trace.py)
M2: rc=1 | 4 failed, 75 passed in 4.53s
     FAILED tests/unit/test_trace.py::test_export_refuses_422_for_the_same_items_the_gate_lists
     FAILED tests/unit/test_trace.py::test_no_override_accepting_again_editing_or_comparing_by_hand_does_not_clear_it
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
     FAILED tests/unit/test_trace.py::test_rejudge_failure_leaves_the_item_unjudged_and_the_gate_closed
    M2 store.export_case passes no blockers (store.py)
M3: rc=1 | 1 failed, 78 passed in 4.47s
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
    M3 export_payload guard removed (export_routes.py)
M4: rc=1 | 31 failed, 48 passed in 4.40s
     FAILED tests/unit/test_trace.py::test_unrun_case_waits_for_the_ai - KeyError:...
     FAILED tests/unit/test_trace.py::test_case_trace_steps_and_counts - KeyError:...
     FAILED tests/unit/test_trace.py::test_pending_live_items_are_a_warning_not_a_blocker_d045
     FAILED tests/unit/test_trace.py::test_export_gate_date_unconfirmed_blocker - ...
     FAILED tests/unit/test_trace.py::test_export_gate_ready_matches_review_view
     FAILED tests/unit/test_trace.py::test_export_gate_nothing_accepted - KeyError...
    M4 pending items block again (trace.export_blockers)
M5: rc=1 | 4 failed, 75 passed in 5.03s
     FAILED tests/unit/test_trace.py::test_export_gate_date_unconfirmed_blocker - ...
     FAILED tests/unit/test_trace.py::test_export_gate_nothing_accepted - assert (...
     FAILED tests/unit/test_trace.py::test_pending_unjudged_items_are_not_judge_blockers_yet
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
    M5 NOTHING_ACCEPTED dropped from shared list (trace.py)
M6: rc=1 | 2 failed, 77 passed in 4.97s
     FAILED tests/unit/test_trace.py::test_paralegal_edited_summary_is_not_counted_unchecked_in_judges_d045b
     FAILED tests/unit/test_trace.py::test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b
    M6 paralegal exemption removed from judges step (trace.py _judge_never_ran)
M7: rc=1 | 4 failed, 75 passed in 4.43s
     FAILED tests/unit/test_trace.py::test_export_gate_nothing_accepted - assert (...
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_no_blockers_in_every_case_state
     FAILED tests/unit/test_trace.py::test_pending_unjudged_items_are_not_judge_blockers_yet
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
    M7 gate ready ignores blockers (trace.py)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:04:48.074Z

Seven of seven killed. M4 killed by a crude mutant that raises KeyError in unrelated tests, so I'll rerun a cleaner pending-as-blocker mutant before relying on it.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:04:51.571Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/mut/run_m4b.py\" <<'EOF'\nimport sys, pathlib\nsys.argv = [sys.argv[0], sys.argv[1]]\nsrc = pathlib.Path(__file__).read_text()\nEOF\ncat > \"$S/mut/run_m4b.py\" <<'EOF'\nimport shutil, subprocess, sys, pathlib\nBASE = pathlib.Path(sys.argv[1]); PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nd = pathlib.Path(str(BASE) + \"_m4b\")\nif d.exists(): shutil.rmtree(d)\nshutil.copytree(BASE, d, ignore=shutil.ignore_patterns(\"__pycache__\"))\np = d / \"app/backend/trace.py\"; s = p.read_text()\nold = '    if not (rv[\"counts\"][\"accepted\"] + rv[\"counts\"][\"edited\"]):\\n        out.append({\"item_id\": None, \"kind\": \"case\", \"reason_code\": \"NOTHING_ACCEPTED\"'\nnew = ('    for k in (\"entry\", \"amount\", \"flag\"):\\n'\n       '        for r in DB.list_items(conn, case_id, k):\\n'\n       '            if r[\"state\"] != \"rejected\" and r[\"review_status\"] == \"pending\":\\n'\n       '                out.append({\"item_id\": r[\"id\"], \"kind\": k, \"reason_code\": \"PENDING_DECISION\", \"why\": TRACE_WHY[\"PENDING_DECISION\"], \"next_action\": None})\\n'\n       + old)\nassert s.count(old) == 1, s.count(old); p.write_text(s.replace(old, new))\nr = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"tests/unit/test_trace.py\", \"tests/unit/test_export.py\", \"-p\", \"no:cacheprovider\"], cwd=d, capture_output=True, text=True)\nprint(\"M4b pending blocks (clean): rc=%d | %s\" % (r.returncode, [l for l in r.stdout.strip().splitlines() if l.strip()][-1]))\nfor l in [l for l in r.stdout.splitlines() if l.startswith(\"FAILED\")][:8]: print(\"    \", l[:200])\nshutil.rmtree(d)\nEOF\ncd \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/mut/run_m4b.py\" \"$S/t080r4\" 2>&1 | tail -15",
 "description": "Run clean pending-blocks mutant in scratch copy"
}
````

### User / tool · 2026-11-02T04:04:57.580Z

**tool result**
````
M4b pending blocks (clean): rc=1 | 7 failed, 72 passed in 4.99s
     FAILED tests/unit/test_trace.py::test_case_trace_steps_and_counts - Assertion...
     FAILED tests/unit/test_trace.py::test_pending_live_items_are_a_warning_not_a_blocker_d045
     FAILED tests/unit/test_trace.py::test_export_gate_date_unconfirmed_blocker - ...
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_no_blockers_in_every_case_state
     FAILED tests/unit/test_trace.py::test_dismissing_or_resetting_an_unjudged_item_clears_its_blocker
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
     FAILED tests/unit/test_trace.py::test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:02.431Z

Pending-as-blocker is caught by seven tests with a clean mutant. Last, the carried-over r3 items: the frontend "Export blocked by N" line (r3 finding 1 cited it) and the rejudge target set (r3 finding 2).

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:03.396Z

**tool call — Bash**
````
{
 "command": "sed -n 340,356p app/frontend/stepper.js; echo ----; grep -n \"pending\" app/frontend/export.js | head -5; echo ----; git diff --name-only 10d358e HEAD -- app tests | head; echo \"(HEAD vs 10d358e in app/tests above; empty = unchanged)\"; echo ----; sed -n 56,62p app/backend/rejudge.py; echo ----; grep -n \"_blank_judges\" tests/unit/test_trace.py | head -2",
 "description": "Check frontend gate text, rejudge targets, and HEAD drift"
}
````

### User / tool · 2026-11-02T04:05:03.526Z

**tool result**
````
    const ev = evidenceNode(st); if (ev.length) body.append(el("div", { class: "zs-evidence", "data-testid": "step-evidence" }, ev));
    if (ctx.extra) { const x = ctx.extra(st); if (x) body.append(x); }
    if (st.status === "fail" || st.status === "pending" || (st.status === "skipped" && needsRerun(st))) { const a = actionNode(st.next_action, ctx, st); if (a) body.append(a); }
    return li;
  }
  // The active step is the one the human has to deal with now: the first fail or pending step that carries a next action.
  function activeIndex(steps) {
    let i = steps.findIndex((s) => (s.status === "fail" || s.status === "pending" || (s.status === "skipped" && needsRerun(s))) && s.next_action);
    if (i < 0) i = steps.findIndex((s) => s.status === "fail" || s.status === "pending");
    return i;
  }

  // ---- item level
  const firstSentence = (t) => { const m = /^[\s\S]*?[.!?](?=\s|$)/.exec(t || ""); return m ? m[0] : t || ""; };
  S.item = function (tr) {
    const steps = tr.steps || [], act = activeIndex(steps), v = Object.assign({}, tr.verdict || {});
    // Accepted, but the second check never ran: not a green "Accepted by you", because the gate will not let it into the letter.
----
2:   Count line sits outside both blocks (R-EX-5). Copy asks for one confirmation when anything is pending (names pending flags separately). */
9:    return `${plural(c.entries, "entry", "entries")}, ${plural(c.charges, "charge", "charges")} in letter · ${plural(c.flags_in_notes, "flag", "flags")} in internal notes · ${c.records_in_letter} of ${c.records_total} records in letter · ${plural(c.pending, "item", "items")} pending (${plural(c.pending_flags, "flag", "flags")})`;
18:    const flags = c.pending_flags, others = c.pending - flags;
22:    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. Copy the letter anyway?"),
39:          el("button", { type: "button", class: "btn primary", "data-testid": "btn-copy-letter", onclick: () => { const go = () => copy(data.letter_text, "treatment section"); c.pending > 0 ? askConfirm(c, go) : go(); } }, "Copy letter")),
----
(HEAD vs 10d358e in app/tests above; empty = unchanged)
----
def rejudge(conn, case_id: str, call, now: float = None) -> dict:
    t = time.time() if now is None else now
    case = DB.get_case(conn, case_id)
    case_text = (case["raw_text"] or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    targets = trace.unjudged_items(conn, case_id)
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        answers = list(ex.map(lambda x: _safe_ask(x, case_text, call), targets))
----
492:def _blank_judges(conn, tok):
512:    n = _blank_judges(conn, tok)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:06.435Z

The frontend line I expected is not at the line numbers I just read, so I'll check whether it still exists in the working tree and at the commit.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:07.364Z

**tool call — Bash**
````
{
 "command": "grep -n \"Export blocked by\" app/frontend/*.js; echo \"--- at 10d358e:\"; git show 10d358e:app/frontend/stepper.js | grep -n \"Export blocked by\"; echo \"--- worktree status (app, tests):\"; git status --short app tests | head; echo \"--- gateText uses:\"; grep -n \"gateText\\|counts.pending\\|pending_items\\|warnings\" app/frontend/stepper.js | head",
 "description": "Locate the Export blocked text in frontend and check worktree state"
}
````

### User / tool · 2026-11-02T04:05:07.506Z

**tool result**
````
app/frontend/stepper.js:397:  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the review queue stays on the first screen.
app/frontend/stepper.js:457:    else if (gate) gateText = "Export blocked by " + (n || 1);
--- at 10d358e:
309:  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the review queue stays on the first screen.
352:    else if (gate) gateText = "Export blocked by " + (n || 1);
--- worktree status (app, tests):
 M app/frontend/api.js
 M app/frontend/export.js
 M app/frontend/judges.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M tests/unit/test_eval_runner.py
?? tests/unit/test_t093_eval_signature.py
--- gateText uses:
418:    const ws = st.warnings || [];
420:    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
453:    let gateText = "";
454:    const warned = ((gate && gate.warnings) || []).reduce((t, w) => t + (w.count || 0), 0);
455:    if (gate && gate.status === "pass") gateText = "Ready to export" + (warned ? ", " + warned + " not reviewed" : "");
456:    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
457:    else if (gate) gateText = "Export blocked by " + (n || 1);
458:    return { passed, need, gateText, total: steps.length };
467:        sb.gateText ? el("span", { class: "zs-sumv zs-sumgate", "data-testid": "case-summary-gate" }, sb.gateText) : null] : el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, "loading…"), toggle);
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:11.592Z

The working tree has uncommitted frontend edits from someone else, so those are outside this commit. I'll read the committed version of that gate-text branch to see what the commit itself shows.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:11.776Z

**tool call — Bash**
````
{
 "command": "git show 10d358e:app/frontend/stepper.js | sed -n 343,353p | cut -c1-260",
 "description": "Read committed stepper gate-text branch at 10d358e"
}
````

### User / tool · 2026-11-02T04:05:11.875Z

**tool result**
````
  }
  // The one-line summary: how many checks passed, how many need the human, and what the export is waiting for.
  function summaryBits(steps) {
    const passed = steps.filter((s) => s.status === "pass").length, need = steps.filter((s) => s.status === "fail" || s.status === "pending").length;
    const gate = steps.find((s) => s.id === "export_gate"), bl = (gate && gate.blockers) || [];
    const n = gate ? (gate.counts && gate.counts.blocking) || bl.length : 0;
    let gateText = "";
    if (gate && gate.status === "pass") gateText = "Ready to export";
    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
    else if (gate) gateText = "Export blocked by " + (n || 1);
    return { passed, need, gateText, total: steps.length };
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:26.458Z

At the commit, the frontend derives "Ready to export" from `gate.status`, so the r3 frontend point is closed. One more check: D-045(b) exempts paralegal edits from "the judge", while R-RV-3 says judge #1 runs on every edited summary. I need to see what the edit path actually does.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:27.162Z

**tool call — Bash**
````
{
 "command": "grep -n \"judge\" app/backend/review.py app/backend/case_extras.py | head -20; echo ----; grep -rn \"SUMMARY_NUMBER_NOT_IN_EXCERPT\\|needs_confirm\" tests/unit/*.py | head -5; echo ----; sed -n 492,500p tests/unit/test_trace.py | cut -c1-220; echo ----; grep -n \"review_events\\|M3\" memory/SCOPE_CUTS.md | head -5",
 "description": "Check edit-path judge calls and related tests"
}
````

### User / tool · 2026-11-02T04:05:27.280Z

**tool result**
````
app/backend/review.py:4:Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
app/backend/review.py:5:and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
app/backend/review.py:10:from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judges, store
app/backend/review.py:82:    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
app/backend/review.py:98:    verdict, call_id, ladder_verdict, judge_code = "unavailable", None, "unavailable", "NONE"
app/backend/review.py:101:            verdict, call_id, judge_code = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item_id)
app/backend/review.py:103:            verdict, call_id, judge_code = "unavailable", None, "NONE"
app/backend/review.py:104:        ladder_verdict = judges.to_ladder("j1", verdict)
app/backend/review.py:110:    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
app/backend/review.py:112:    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
app/backend/review.py:163:    lad["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": call_id, "verdict": ladder_verdict,
app/backend/review.py:164:                    "reason_code": chk["judge_code"]}
app/backend/review.py:207:    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
app/backend/review.py:276:    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
app/backend/review.py:300:              "judge": {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
app/backend/review.py:301:                        "reason_code": chk["judge_code"]},
app/backend/review.py:324:    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
app/backend/review.py:346:    # the split-off record's own entry (code-checked, then judge 1; a failure leaves it visibly without an entry)
app/backend/review.py:353:                generator.judge_entries([e], by_n, call=call, case_text=case["raw_text"])
app/backend/review.py:368:    verdicts = judges_for(dollars, call, case["raw_text"])
----
tests/unit/test_api_routes.py:132:def test_charge_cannot_be_edited_and_rerun_needs_confirm(env):
tests/unit/test_api_routes.py:139:    assert r.status_code == 409 and r.json()["error"]["code"] == "needs_confirm"
tests/unit/test_manual_and_split.py:68:    assert e.value.code == "needs_confirm"                                           # non-numeric judge objection: the confirm path stays
tests/unit/test_review_rules.py:95:def test_seeded_herniation_judge_unsupported_needs_confirm(tmp_path):
tests/unit/test_review_rules.py:100:    assert e.value.code == "needs_confirm" and "JUDGE_UNSUPPORTED" in [w["code"] for w in e.value.detail["warnings"]]
----
def _blank_judges(conn, tok):
    """Make the judge stage 'never ran' on every entry and every non-damages amount (the run deadline case in pipeline.py)."""
    n = 0
    for kind in ("entry", "amount"):
        for row in DB.list_items(conn, tok, kind):
            if row["state"] == "rejected" or (kind == "amount" and row["kind"] == "damages"):
                continue
            lad = row["ladder"]
            if not lad.get("judge"):
----
40:| debt | T-039 accepted with documented debt after 2 rounds (§7.4) | r2 major: no test for the judge-exception path in review.py (silent fallback); qa-2 adds it as follow-up | see card | M3 |
41:| debt | T-042 accepted with documented debt after 2 rounds (§7.4) | case_01 header shows 0 needs review beside six needs-review items (dates-to-confirm not counted); frontend-1 follow-up; E2E verifies in T-045 | see card | M3 |
45:| debt | T-040 accepted with documented debt after 2 rounds (§7.4) | r2: round-1 blocker+majors resolved; new majors routed: PDF route gating/threadpool (backend-2, T-054), migration .old files purged (backend-3, T-050) | see card | M3 |
47:| 20 | PDF hidden/invisible text detection (text layer may contain text not visible on the page) | Prototype uses the text layer as-is; flagged as a known limit in the product note. | ~1 day: render-vs-text comparison per page. | M3 (T-054 F4) |
48:| debt | T-053 accepted with documented debt after 3 rounds (§7.4) | r3 major: local mode behind a loopback reverse proxy (tailscale serve) is reachable by proxy clients. Accepted: tailscale serve exposes only to Chris's private tailnet, never funnel (non-negotiable); README/RUNBOOK must warn never to put ZLAYT_MODE=local behind a public proxy (release, M4). Public build is unaffected. | see card | M3 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:49.417Z

The edit path still runs judge 1 on every edited summary (review.py:101), so D-045(b) is an exemption from the gate's never-ran check only. That is a wording issue in the decision, not a behavior defect. Last hygiene pass: the exact brief command, a second run for reproducibility, and a grep of the commit's added lines for float money, bare excepts, sleeps, and network calls.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:05:50.776Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -2; .venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -1; echo \"--- added lines in 10d358e matching risky patterns:\"; git show 10d358e -- app tests | grep \"^+\" | grep -nE \"float\\(|except:|except Exception|sleep\\(|requests\\.|httpx|urllib|anthropic\\.|time\\.time\\(\" || echo \"(none)\"; echo \"--- test_export.py new tests:\"; grep -n \"^def test_\" tests/unit/test_export.py | sed -n '1,200p' | tail -8",
 "description": "Run exact pytest command twice and grep commit additions for risky patterns"
}
````

### User / tool · 2026-11-02T04:06:02.579Z

**tool result**
````
.......                                                                  [100%]
79 passed in 5.49s
79 passed in 5.12s
--- added lines in 10d358e matching risky patterns:
(none)
--- test_export.py new tests:
133:def test_every_record_citation_has_provider_and_date():
140:def test_bills_to_request_line_exact():
145:def test_dismiss_5_pending_6_reconciliation_and_counts():
157:def test_edited_items_section():
167:def test_edited_then_accepted_entry_still_listed_in_edited_items():
178:def test_accepted_unedited_and_dismissed_edited_not_listed():
185:def test_build_export_refuses_while_accepted_items_lack_the_second_check_d044():
194:def test_export_blocked_code_is_judge_not_run_only_when_every_blocker_is():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:06:05.641Z

Both runs pass 79 of 79, and the commit adds no float money, bare excepts, sleeps, or network calls. Before writing, I'll pin the exact line numbers I plan to cite.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:06:07.920Z

**tool call — Bash**
````
{
 "command": "grep -n \"blockers = export_blockers(conn, case_id, cx, rv)\\|    ready = not blockers\\|def export_blockers\\|if not cx.ran or _paralegal_wording\\|def _paralegal_wording\\|    targets = trace.unjudged_items\\|def judge_not_run_blockers\\|return \\[_jnr_blocker\" app/backend/trace.py app/backend/rejudge.py; grep -n \"if case.get(\\\"export_blockers\\\")\\|except export.ExportBlocked\\|out\\[\\\"export_blockers\\\"\\] = trace\\|def test_gate_ready_equals_export_allowed\\|r\\[\\\"asked\\\"\\] == n\\|def _blank_judges\\|def test_pending_live_items_are\" app/backend/export_routes.py app/backend/store.py tests/unit/test_trace.py; grep -n \"class ExportBlocked\\|def code\\|class JudgeNotRun\" app/backend/export.py; grep -n \"def blocked_message\" app/backend/export_routes.py; grep -n \"judges.run_j1_meta\" app/backend/review.py; grep -n \"date_unconfirmed(conn, case_id, kind, item)\" app/backend/review.py; grep -n \"Items not reviewed\\|def pending_warning\" app/backend/trace.py app/backend/export.py | head -3; grep -n \"status_code == 422 and ex.json()\\|ex.json()\\[\\\"error\\\"\\]\\[\\\"code\\\"\\] == \\\"export_blocked\\\"\" tests/unit/test_trace.py | head -3",
 "description": "Get exact line numbers for review citations"
}
````

### User / tool · 2026-11-02T04:06:08.076Z

**tool result**
````
app/backend/rejudge.py:60:    targets = trace.unjudged_items(conn, case_id)
app/backend/trace.py:656:    if not cx.ran or _paralegal_wording(kind, row):
app/backend/trace.py:667:def _paralegal_wording(kind, row) -> bool:
app/backend/trace.py:687:def judge_not_run_blockers(conn, case_id: str) -> list:
app/backend/trace.py:689:    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id) if u["review_status"] in ("accepted", "edited")]
app/backend/trace.py:889:    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
app/backend/trace.py:894:    ready = not blockers
app/backend/trace.py:922:def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
app/backend/store.py:78:    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
app/backend/export_routes.py:28:    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
app/backend/export_routes.py:69:    except export.ExportBlocked as e:    # D-044/D-045: the gate lists the same blockers; no override
tests/unit/test_trace.py:334:def test_pending_live_items_are_a_warning_not_a_blocker_d045(env):
tests/unit/test_trace.py:492:def _blank_judges(conn, tok):
tests/unit/test_trace.py:781:def test_gate_ready_equals_export_allowed_in_every_state_d045(env):
tests/unit/test_trace.py:906:    assert r["asked"] == n
564:class ExportBlocked(Exception):
574:    def code(self) -> str:
578:class JudgeNotRun(ExportBlocked):
52:def blocked_message(e) -> str:
101:            verdict, call_id, judge_code = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item_id)
67:    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
app/backend/export.py:28:           "by the paralegal. Items not reviewed: {n}.")
app/backend/trace.py:918:def pending_warning(n: int) -> str:
792:        assert bool(_jnr(g)) == (ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"] != [] and any(b["reason_code"] == "JUDGE_NOT_RUN" for b in ex.json()["error"]["detail"]["blockers"])), name
830:    assert [b["reason_code"] for b in g["blockers"]] == ["RUN_FAILED"] and ex.json()["error"]["code"] == "export_blocked"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:06:24.131Z

Line numbers are pinned. Two last steps: check whether the frontend keys on the export 422 status (it bears on finding 2), and save the mutation scripts and transcript under `artifacts/review-evidence/`, which is my permitted write path.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:06:26.591Z

**tool call — Bash**
````
{
 "command": "grep -rn \"422\" app/frontend/*.js | grep -i \"export\\|judge\" | head -5; echo \"(frontend 422 refs above, if any)\"; EV=artifacts/review-evidence/T-080-r4; mkdir -p \"$EV\" && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cp \"$S/mut/run_mutants.py\" \"$S/mut/run_m4b.py\" \"$EV/\" && (cd \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/mut/run_mutants.py\" \"$S/t080r4\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/mut/run_m4b.py\" \"$S/t080r4\") > \"$EV/mutation_output.txt\" 2>&1; tail -3 \"$EV/mutation_output.txt\"; ls -la \"$EV\"",
 "description": "Check frontend 422 handling and save mutation evidence"
}
````

### User / tool · 2026-11-02T04:07:17.993Z

**tool result**
````
app/frontend/export.js:51:      // A refused export (422 judge_not_run / export_blocked) is shown beside the Export button, scrolled into view and focused, with the blocker list and the rerun button.
app/frontend/stepper.js:474:  // ---- the message beside the Export button. A refused export (422 judge_not_run / export_blocked) is shown right under the toolbar, scrolled into view and
(frontend 422 refs above, if any)
     FAILED tests/unit/test_trace.py::test_dismissing_or_resetting_an_unjudged_item_clears_its_blocker
     FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
     FAILED tests/unit/test_trace.py::test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b
total 24
drwxr-xr-x@   5 arsis  staff    160 Nov  1 22:06 .
drwxr-xr-x@ 689 arsis  staff  22048 Nov  1 22:06 ..
-rw-r--r--@   1 arsis  staff   4083 Nov  1 22:07 mutation_output.txt
-rw-r--r--@   1 arsis  staff   1343 Nov  1 22:06 run_m4b.py
-rw-r--r--@   1 arsis  staff   3055 Nov  1 22:06 run_mutants.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:07:31.839Z

The frontend reads `error.code` and not the status, and the 422 hits are comments only, so a status change would not break the UI. I need three more line numbers for the write-up: the warnings list, the gate step, and the nothing-accepted assertion.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:07:33.027Z

**tool call — Bash**
````
{
 "command": "grep -n \"warnings = \\[{\\|gate.update(ready=ready\\|n_pend = len\\|    if not (rv\\[\\\"counts\\\"\\]\\[\\\"accepted\\\"\\]\" app/backend/trace.py; grep -n \"nothing decided yet (pending only)\\\"\\]\" tests/unit/test_trace.py; grep -n \"gate.status === \\\"pass\\\"\\|if (gate && gate.status\" app/frontend/stepper.js | head -3; grep -n \"c.pending > 0\" app/frontend/export.js; grep -n \"_judge_never_ran(cx, kind, row):\\|^def _judge_rows\" app/backend/trace.py",
 "description": "Confirm remaining citation line numbers"
}
````

### User / tool · 2026-11-02T04:07:33.080Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  0)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:07:35.316Z

The guard read the `>` inside a grep pattern as a shell redirect. I'll rerun without it.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:07:36.196Z

**tool call — Bash**
````
{
 "command": "grep -n \"warnings = \\[{\\|gate.update(ready=ready\\|n_pend = len\\|    if not (rv\\[\\\"counts\\\"\\]\\[\\\"accepted\\\"\\]\" app/backend/trace.py; grep -n \"nothing decided yet (pending only)\\\"\\]\" tests/unit/test_trace.py; grep -n \"gate.status === \\\"pass\\\"\\|if (gate && gate.status\" app/frontend/stepper.js | head -3; grep -n \"c.pending\" app/frontend/export.js | head -3; grep -n \"_judge_never_ran(cx, kind, row):\\|^def _judge_rows\" app/backend/trace.py",
 "description": "Confirm remaining citation line numbers"
}
````

### User / tool · 2026-11-02T04:07:36.316Z

**tool result**
````
892:    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
897:    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
909:    gate.update(ready=ready, blockers=blockers, warnings=warnings)
934:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
820:    g, ex = seen["nothing decided yet (pending only)"]
455:    if (gate && gate.status === "pass") gateText = "Ready to export" + (warned ? ", " + warned + " not reviewed" : "");
9:    return `${plural(c.entries, "entry", "entries")}, ${plural(c.charges, "charge", "charges")} in letter · ${plural(c.flags_in_notes, "flag", "flags")} in internal notes · ${c.records_in_letter} of ${c.records_total} records in letter · ${plural(c.pending, "item", "items")} pending (${plural(c.pending_flags, "flag", "flags")})`;
18:    const flags = c.pending_flags, others = c.pending - flags;
39:          el("button", { type: "button", class: "btn primary", "data-testid": "btn-copy-letter", onclick: () => { const go = () => copy(data.letter_text, "treatment section"); c.pending > 0 ? askConfirm(c, go) : go(); } }, "Copy letter")),
637:def _judge_rows(cx):
653:def _judge_never_ran(cx, kind, row):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:07:45.463Z

The evidence is complete. I'll write the review file now (new file, write-once).

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:09.712Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-080-staff-engineer-r4.md",
 "content": "# T-080 round-4 review: export gate single list, pending as warnings (D-044/D-045), commit 10d358e\n\nScope: commit 10d358e (backend: app/backend/trace.py, export.py, export_routes.py, api.py, store.py; tests/unit/test_trace.py, tests/unit/test_export.py; memory/contracts/api.md). HEAD is 8d7548d, and `git diff --name-only 10d358e HEAD -- app tests` is empty, so the reviewed backend is HEAD's backend. Verdict: **pass** (0 blockers, 0 majors; 2 minors, 1 nit).\n\nRound-3 status: the r3 major (pending items block the gate, D-045(a) not implemented) is closed. The r3 judges-step minor and the r3 build_export nit are closed. The r3 rejudge-scope minor is still open (finding 1 below).\n\n## Answers to the brief\n\n- **Gate and GET /export share one blocker list; gate.ready == export allowed: confirmed.** `trace.export_blockers` (trace.py:922) is the only producer. The gate reads it at trace.py:889 and sets `ready = not blockers` at trace.py:894. The export reads it through store.py:78 and export_routes.py:28 refuses on it. The only other refusal is build_export's JudgeNotRun (export.py:586-587), on a subset of the same list. `grep -rn \"build_export\\|export_payload\" app` shows no other export caller. Test `test_gate_ready_equals_export_allowed_in_every_state_d045` (test_trace.py:781) asserts `g[\"ready\"] == (ex.status_code < 400)` and identical blocker lists in nine states: nothing decided, one accepted, all but one accepted, judge not run, judges answered with one pending, run failed, run in progress, all clear, everything dismissed. It passes.\n- **Pending items are warnings, not blockers: confirmed.** PENDING_DECISION and DATE_UNCONFIRMED are gone from `blockers`. Pending items go to `warnings` (trace.py:897, `ITEMS_NOT_REVIEWED`) and to `counts.pending_items` (trace.py:892). The date guard still stops an unconfirmed date from being accepted or edited into the letter (review.py:67, D-041), so dropping DATE_UNCONFIRMED from blockers opens no path to an unconfirmed date in the letter. The committed frontend already reads `gate.status === \"pass\"` (app/frontend/stepper.js:455 in the working tree; the same branch is at stepper.js:350 at 10d358e), so the \"Export blocked by N\" text for pending items is gone.\n- **NOTHING_ACCEPTED, run failed and run in progress return 422 export_blocked: refusal is reasonable; the status code is the weak part.** Fail-closed is right: a letter with nothing accepted is empty, a letter from a failed run is partial, and a letter from a run still writing is unfinished. No fact is invented in any of the three. The 422 choice is finding 2 (minor). Tests: test_trace.py:830 (RUN_FAILED gives 422 export_blocked); the invariant test covers NOTHING_ACCEPTED (test_trace.py:820, 422) and RUN_IN_PROGRESS.\n- **Paralegal-written summaries are not counted as unchecked: confirmed in all three readers.** `_paralegal_wording` (trace.py:667) is used by `_judge_never_ran` (trace.py:656, gate and /judges), by `unjudged_items` (trace.py:672 onward, the rejudge target list), and by `judge_report` through `_judge_rows` (trace.py:637). The edit path still runs judge 1 on every edited summary (review.py:101), and a judge objection still returns 409 (R-RV-3, tests/unit/test_review_rules.py:95). So the exemption only removes the \"never ran\" blocker. Finding 3 is about the wording of D-045(b).\n- **The invariant test fails when the shared list is broken in a scratch copy: confirmed.** Mutants M1 (gate drops JUDGE_NOT_RUN), M2 (store passes no blockers), M5 (NOTHING_ACCEPTED dropped), and M7 (gate ready ignores blockers) each fail the invariant test. M3 (export_payload guard removed) fails only the invariant test, so that guard has one test behind it. Full table below.\n\n## Findings\n\n### 1. minor: rejudge re-asks pending unjudged items (r3 finding 2, still open)\nEvidence: `app/backend/rejudge.py:60` `targets = trace.unjudged_items(conn, case_id)`. `app/backend/trace.py:672-684` filters out only rejected and dismissed items, so pending items are included. `tests/unit/test_trace.py:906` `assert r[\"asked\"] == n`, where `_blank_judges` (test_trace.py:492) blanks pending rows too. Repro: `.venv/bin/python -m pytest -q tests/unit/test_trace.py::test_rejudge_only_touches_items_whose_judge_never_ran` (passes, so the behaviour is codified).\nWhy it matters: D-044 (memory/ORCHESTRATOR_DECISIONS.md:52) says the rejudge \"re-judges just those items\", meaning the items the gate lists. Pending items get extra audited model calls. No review_status changes and no state changes follow, so this stays minor. But it is a literal deviation from a binding decision, and the test now locks it in.\nFix: filter the targets to `review_status` in (accepted, edited) in rejudge.py:60, or amend D-044 in memory/DECISIONS.md to name pending items and update test_trace.py:906.\nAcceptance test: 4 accepted and 8 pending unjudged items give `asked == 4`. Or DECISIONS names 12 and the test asserts 12.\n\n### 2. minor: export refusals use 422 for state conflicts (run in progress, run failed, nothing accepted, judge not run)\nEvidence: `app/backend/export_routes.py:69-71` returns `status_code=422` for every `ExportBlocked`, with `error.code` set to `e.code`. `tests/unit/test_trace.py:830` asserts `error.code == \"export_blocked\"` for RUN_FAILED. The invariant test (test_trace.py:781) covers all four states.\nWhy it matters: the refusal is right; the status code is a judgment call. 422 means the request content is invalid, and these are state conflicts. The spec already reserves 409 for state and judge objections (spec/REQUIREMENTS.md:94, R-RV-3: \"judge or token objections are 409, never 422\"). The UI keys on `error.code` (app/frontend/export.js:51 and the comment at stepper.js:474; no status-code branch found), so a change is cheap. The spec names no export status code, so this is minor and not a spec violation.\nFix: return 409 for all four export refusals, or record in memory/DECISIONS.md why D-044's 422 stands, and say so at memory/contracts/api.md:30 and :286.\nAcceptance test: GET /export during a run returns the chosen status (409 or the recorded code), `error.code` is `export_blocked`, and `detail.blockers` lists RUN_IN_PROGRESS.\n\n### 3. nit: D-045(b) says \"exempt from the judge\"; the code exempts only the second-check blocker and the /judges counts\nEvidence: memory/ORCHESTRATOR_DECISIONS.md:53 says \"(b) ... exempt from the judge but still passes the D-034 code checks\". app/backend/review.py:101 still calls `judges.run_j1_meta` on every edited summary. The exemption is at trace.py:656 and trace.py:667-669 only.\nWhy it matters: the behaviour is right (R-RV-3 holds). The decision text overstates the exemption, and a later reader could remove the edit-time judge on the strength of it.\nFix: reword D-045(b) to \"exempt from the second-check blocker and the /judges counts; judge 1 still runs at edit time (R-RV-3)\".\nAcceptance test: none beyond the wording. `grep -n \"exempt from\" memory/ORCHESTRATOR_DECISIONS.md` shows the reworded sentence.\n\n## Mutation run (scratch copy of commit 10d358e, not committed)\n\nScratch copy: `git archive 10d358e` into the session scratchpad, tests run with `/Users/arsis/zlayt-pm-project/.venv/bin/python` from that copy (its `app` import resolves to the copy). Each mutant changes one anchor string (asserted to occur exactly once). Command: `pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider`. Output saved at `artifacts/review-evidence/T-080-r4/mutation_output.txt`, scripts at `artifacts/review-evidence/T-080-r4/run_mutants.py` and `run_m4b.py`.\n\n| Mutant | Result |\n|---|---|\n| baseline (10d358e) | 79 passed |\n| M1 gate drops JUDGE_NOT_RUN from the shared list (trace.py:889) | 9 failed, invariant test among them |\n| M2 store.export_case passes no blockers (store.py:78) | 4 failed, invariant test among them |\n| M3 export_payload guard removed (export_routes.py:28) | 1 failed (the invariant test only) |\n| M4 pending items block again (clean version, DB.list_items, PENDING_DECISION) | 7 failed, including test_pending_live_items_are_a_warning_not_a_blocker_d045 |\n| M5 NOTHING_ACCEPTED dropped from the shared list (trace.py:934) | 4 failed, invariant test among them |\n| M6 paralegal exemption removed from _judge_never_ran (trace.py:656) | 2 failed (both d045b tests) |\n| M7 gate ready ignores non-NOTHING_ACCEPTED blockers (trace.py:894) | 4 failed, invariant test among them |\n\nM4 in the first run used a crude mutant that also raised KeyError in unrelated tests. The clean M4 (M4b above) is the one reported.\n\n## Exercised\n\n- Read personas/staff-engineer.md; reviews/T-080-staff-engineer-r3.md; memory/ORCHESTRATOR_DECISIONS.md lines 52-53 (D-044, D-045); spec/REQUIREMENTS.md lines 94, 122-123; memory/contracts/api.md lines 30, 286, 536-543.\n- `git show 10d358e --stat`; `git show 10d358e -- app/backend/{trace,export,export_routes,api,store}.py tests/unit/test_trace.py`; test_export.py lines 185-197.\n- `.venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider`: 79 passed in 4.65s. The same command without the flag: 79 passed in 5.49s, then 79 passed in 5.12s (reproducible).\n- Baseline and eight mutants in the scratch copy (table above).\n- `grep -n` for callers of build_export, export_payload, export_blockers, judge_not_run, JudgeNotRun, ExportBlocked across app/ and tests/.\n- `git show 10d358e -- app tests | grep \"^+\"` for float(, bare except, except Exception, sleep(, requests, httpx, urllib, anthropic, time.time(): no matches.\n- `git diff --name-only 10d358e HEAD -- app tests`: empty.\n- Frontend at 10d358e: app/frontend/stepper.js:350-352 (gate text), app/frontend/export.js:39 (copy confirm when `c.pending` is non-zero), and every \"422\" hit in app/frontend (comments only).\n- Not exercised: no live server was started. The run-state and nothing-accepted 422 cases were exercised through the TestClient, with case status set to failed or running in the invariant test.\n- Out of scope: the working tree has uncommitted edits to app/frontend/*.js and tests/unit/test_eval_runner.py, plus an untracked tests/unit/test_t093_eval_signature.py (from `git status --short`). They are not part of 10d358e and were not reviewed.\n- Not checked: the frontend behaviour beyond the gate text and the copy confirm (UX is outside my lens).\n\n## What's right\n\n1. One function (`trace.export_blockers`, trace.py:922) feeds the gate and the export refusal, so the gate cannot pass over a blocker the export refuses. The invariant test checks this across nine states, and M1, M2, M5 and M7 each fail it.\n2. Pending-as-warning is safe because a pending item with an unconfirmed date cannot be accepted (review.py:67, D-041). M4 (pending blocks again) fails seven tests.\n3. The paralegal-wording exemption is applied the same way in the gate, the /judges counts and the rejudge target list (`_paralegal_wording`, trace.py:667). M6 is killed by both d045b tests.\n\n```json\n{\"card\": \"T-080\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 10d358e (app/backend/trace.py, export.py, export_routes.py, api.py, store.py; tests/unit/test_trace.py, test_export.py; memory/contracts/api.md) with D-044/D-045 in memory/ORCHESTRATOR_DECISIONS.md lines 52-53; HEAD 8d7548d has no app/backend or tests/unit changes since 10d358e; scratch copy of 10d358e; no live server\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-080-staff-engineer-r3.md, memory/ORCHESTRATOR_DECISIONS.md D-044/D-045, spec/REQUIREMENTS.md lines 94 and 122-123, memory/contracts/api.md lines 30, 286, 536-543\",\n  \"git show 10d358e --stat and diffs of app/backend/{trace,export,export_routes,api,store}.py and tests/unit/test_trace.py; test_export.py lines 185-197\",\n  \".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py -p no:cacheprovider -> 79 passed in 4.65s; repeated twice more -> 79 passed (5.49s, 5.12s)\",\n  \"scratch copy of 10d358e: baseline 79 passed; mutants M1, M2, M3, M5, M6, M7 and clean M4b killed (M1 9 failed, M2 4, M3 1, M4b 7, M5 4, M6 2, M7 4); output in artifacts/review-evidence/T-080-r4/mutation_output.txt\",\n  \"grep for callers of build_export, export_payload, export_blockers, judge_not_run, JudgeNotRun, ExportBlocked across app/ and tests/\",\n  \"git show 10d358e -- app tests | grep '^+' for float(, bare except, sleep(, network calls: none\",\n  \"git diff --name-only 10d358e HEAD -- app tests: empty\",\n  \"app/frontend/stepper.js:350-352 and export.js:39 at 10d358e; app/frontend 422 hits: comments only\"],\n \"verdict\": \"pass\",\n \"scores\": {\"single_blocker_list\": 5, \"pending_warning_not_blocker\": 5, \"nothing_accepted_and_run_refusals\": 4, \"paralegal_exemption_consistency\": 5, \"invariant_test_strength\": 5, \"export_status_code_convention\": 3, \"rejudge_scope_d044\": 3, \"tests_reproducible\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Rejudge re-asks pending unjudged items (r3 finding 2, still open)\",\n   \"evidence\": \"app/backend/rejudge.py:60 `targets = trace.unjudged_items(conn, case_id)`; app/backend/trace.py:672-684 filters only rejected and dismissed, so pending items are included; tests/unit/test_trace.py:906 `assert r[\\\"asked\\\"] == n`, with _blank_judges (test_trace.py:492) blanking pending rows too. Repro: .venv/bin/python -m pytest -q tests/unit/test_trace.py::test_rejudge_only_touches_items_whose_judge_never_ran\",\n   \"why_it_matters\": \"D-044 (memory/ORCHESTRATOR_DECISIONS.md:52) says rejudge 're-judges just those items' (the gate's list). Pending items get extra audited model calls. No review_status or state change follows, so minor; but it is a literal deviation from a binding decision and the test now codifies it.\",\n   \"fix\": \"Filter rejudge targets to review_status in (accepted, edited) at rejudge.py:60, or amend D-044 in memory/DECISIONS.md to name pending items and update test_trace.py:906.\",\n   \"acceptance_test\": \"4 accepted and 8 pending unjudged items: asked == 4 (or DECISIONS names 12 and the test asserts 12).\"},\n  {\"severity\": \"minor\", \"title\": \"Export refusals use 422 for state conflicts (run in progress, run failed, nothing accepted, judge not run)\",\n   \"evidence\": \"app/backend/export_routes.py:69-71 returns status_code=422 for every ExportBlocked, with error.code = e.code; tests/unit/test_trace.py:830 asserts error.code == 'export_blocked' for RUN_FAILED; invariant test test_trace.py:781 covers all four states; spec/REQUIREMENTS.md:94 (R-RV-3): 'judge or token objections are 409, never 422'.\",\n   \"why_it_matters\": \"Refusing these exports is correct (fail-closed: empty, partial or still-writing letter). The status code is the issue: 422 means invalid request content; these are state conflicts, and the spec already uses 409 for state objections. The UI keys on error.code (app/frontend/export.js:51), so a change is cheap. The spec names no export status code, so minor, not a spec violation.\",\n   \"fix\": \"Return 409 for all four export refusals, or record in memory/DECISIONS.md why D-044's 422 stands and update memory/contracts/api.md lines 30 and 286.\",\n   \"acceptance_test\": \"GET /export during a run returns the chosen status (409 or the recorded code), error.code export_blocked, detail.blockers lists RUN_IN_PROGRESS.\"},\n  {\"severity\": \"nit\", \"title\": \"D-045(b) says 'exempt from the judge'; the code exempts only the second-check blocker and the /judges counts\",\n   \"evidence\": \"memory/ORCHESTRATOR_DECISIONS.md:53 '(b) ... exempt from the judge but still passes the D-034 code checks'; app/backend/review.py:101 still runs judges.run_j1_meta on every edited summary; exemption at app/backend/trace.py:656 and trace.py:667-669 only.\",\n   \"why_it_matters\": \"The behaviour is right (R-RV-3 holds: objection gives 409, tests/unit/test_review_rules.py:95). The decision text overstates the exemption, and a later reader could drop the edit-time judge on that basis.\",\n   \"fix\": \"Reword D-045(b): 'exempt from the second-check blocker and the /judges counts; judge 1 still runs at edit time (R-RV-3)'.\",\n   \"acceptance_test\": \"grep -n 'exempt from' memory/ORCHESTRATOR_DECISIONS.md shows the reworded sentence; no test change.\"}\n ],\n \"whats_right\": [\n  \"One function (trace.export_blockers, trace.py:922) feeds both the gate and the export refusal, so the gate cannot pass over a blocker the export refuses; the invariant test checks nine states, and M1, M2, M5 and M7 each fail it.\",\n  \"Pending-as-warning is safe because a pending item with an unconfirmed date cannot be accepted (review.py:67, D-041); M4b (pending blocks again) fails seven tests.\",\n  \"The paralegal-wording exemption is applied the same way in the gate, the /judges counts and the rejudge target list (_paralegal_wording, trace.py:667); M6 is killed by both d045b tests.\"\n ],\n \"questions_for_chris\": [\"A failed run with accepted items currently blocks export until the run is re-run (RUN_FAILED, fail-closed). Should it instead export with a visible 'run incomplete' note? I have assumed blocking; the product call is yours.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T04:08:09.875Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-080-staff-engineer-r4.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:15.470Z

The review file is written. I'll validate its JSON block against the D.2 shape and the verdict rule, and check how the board validator is invoked.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:16.759Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json,re\nt=open('reviews/T-080-staff-engineer-r4.md').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd=json.loads(blocks[0])\nsev=[f['severity'] for f in d['findings']]\nprint('keys:', sorted(d.keys()))\nprint('verdict', d['verdict'], 'sev', sev, 'model', d['model'], 'persona', d['persona'], 'card', d['card'])\nrule = 'fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('rule verdict', rule, 'match', rule==d['verdict'])\nprint('whats_right', len(d['whats_right']))\n\"; grep -n \"validate\" tools/board.py | head -5",
 "description": "Validate review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T04:08:16.816Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:18.103Z

The shell guard could not parse the escaped backticks in that inline command. I'll put the check in a script in the scratchpad and run that instead.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:20.430Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/check_review.py",
 "content": "import json, re, sys\n\npath = sys.argv[1]\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"keys:\", sorted(d.keys()))\nprint(\"card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"])\nprint(\"severities:\", sev)\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule gives\", rule, \"| matches file:\", rule == d[\"verdict\"])\nprint(\"whats_right:\", len(d[\"whats_right\"]), \"| exercised:\", len(d[\"exercised\"]))\n"
}
````

### User / tool · 2026-11-02T04:08:20.588Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/check_review.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:22.224Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/check_review.py /Users/arsis/zlayt-pm-project/reviews/T-080-staff-engineer-r4.md",
 "description": "Validate review JSON block against the verdict rule"
}
````

### User / tool · 2026-11-02T04:08:22.332Z

**tool result (error)**
````
Exit code 2
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python: can't open file '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/check_review.py': [Errno 2] No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:24.493Z

The write guard blocks Write outside `reviews/` and `artifacts/review-evidence/`. I'll put the checker in the evidence directory, which is permitted.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:25.679Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-080-r4/check_review.py",
 "content": "import json, re, sys\n\npath = sys.argv[1]\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"keys:\", sorted(d.keys()))\nprint(\"card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"])\nprint(\"severities:\", sev)\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule gives\", rule, \"| matches file:\", rule == d[\"verdict\"])\nprint(\"whats_right:\", len(d[\"whats_right\"]), \"| exercised:\", len(d[\"exercised\"]))\n"
}
````

### User / tool · 2026-11-02T04:08:25.777Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-080-r4/check_review.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:26.137Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-080-r4/check_review.py reviews/T-080-staff-engineer-r4.md",
 "description": "Validate review JSON block against the verdict rule"
}
````

### User / tool · 2026-11-02T04:08:26.244Z

**tool result**
````
json blocks: 1
keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right']
card T-080 | persona staff-engineer-reviewer | model claude-haiku-5-5 | verdict pass
severities: ['minor', 'minor', 'nit']
verdict rule gives pass | matches file: True
whats_right: 3 | exercised: 8
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:27.863Z

The JSON parses, and the verdict matches the rule. Next I'll confirm whether the board validator covers this file, since the brief says `board.py` is read-only for me.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:28.285Z

**tool call — Bash**
````
{
 "command": "grep -n \"validate\" tools/board.py | head -8",
 "description": "Find board validator entry point in board.py"
}
````

### User / tool · 2026-11-02T04:08:28.376Z

**tool result**
````
740:    errs = validate_review_file(rp)
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
949:            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
1119:    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:29.623Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I tools/board.py validate reviews/T-080-staff-engineer-r4.md; echo \"rc=$?\"",
 "description": "Run read-only board validator on the review file"
}
````

### User / tool · 2026-11-02T04:08:29.756Z

**tool result**
````
ok (1 file(s))
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:32.585Z

The validator accepts the file. Last, memory: I'll record the recurring patterns from this round, starting by reading the existing T-080 memory file so I can extend it rather than duplicate it.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:32.953Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t080_trace_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:08:32.962Z

**tool result**
````
1	---
2	name: project_t080_trace_review_patterns
3	description: T-080 r1 (check-trace API): aggregates that go green when the judge never ran, gate ready vs blockers contradiction, 404 masking KeyError, survivors in a mostly-strong test file
4	metadata:
5	  type: project
6	---
7	
8	T-080 r1 (e3cea6f, verdict changes: 0 blockers, 2 majors). Item ladders matched stored data on 16 cases; the bugs were in aggregates and failure branches.
9	
10	- **Aggregates built from "rows with a verdict" go green when the judge never ran.** `judge_report` skips items with no `ladder.judge.verdict`; a deadline-cut run (pipeline guard false) leaves judge None + JUDGE_UNAVAILABLE, so item traces say skipped while /judges says unavailable 0 and the case step says PASS. How to apply: for any "N of M checked" summary, probe the case where the producer stage did not run (delete the judge record in a DB copy) and compare item-level counts with the summary.
11	- **Gate `ready` computed from one source, `blockers` from another** (ready ignored status=failed). Check `ready == (blockers == [])` across running/failed/all-accepted.
12	- **Broad `except (KeyError, IndexError)` -> 404** hides internal table bugs (monkeypatch a fixed-sentence table to prove it).
13	- Tests were strong (20/23 mutants killed) but survivors sat on the same untested failure branches: dismissed human step, running + all accepted, `disagrees` in totals.
14	
15	T-080 r2 (94beaeb, verdict changes: 0 blockers, 1 major). Round-1 fixes verified: judges never-ran counted and judges step FAILs, gate `ready == (no blockers)` incl. RUN_FAILED, 404 narrowed, ZLAYT_DB honoured, 3 survivors killed (16/16 valid mutants killed).
16	- New major: gate passes and `build_export` is silent over accepted items whose judge never ran (12 items: judges FAIL, gate ready, internal notes "Items not reviewed: 0"). Policy gap (R-RV-3 allows accepting JUDGE_UNAVAILABLE), so major not blocker; question to Chris.
17	- Residuals: rejected amount/flag traces still untested; ITEMS_PENDING gate branch is unreachable (present.py ready_to_export equals live-pending plus NOTHING_ACCEPTED).
18	- Probe method that worked: a scratch-only helper that calls `DB.update_case` / blanks judge rows on the scratch DB file while the live server runs (it reads per request), then GET /judges, /trace and /export. Verify the probe script's DB path is the scratch file before running it.
19	- Mutant method: when a mutant survives, first check its anchor is in the branch the test covers (r2 first R2 draft changed an unrelated mapping and survived; a corrected mutant on the fallback was killed).
20	
21	T-080 r3 (fe4ee80 + D-045 docs f49c4c2; verdict changes: 0 blockers, 1 major, 2 minor, 1 nit; reviews/T-080-staff-engineer-r3.md). D-044 JUDGE_NOT_RUN blocker and export 422 agree live; mutants M1-M7 killed.
22	- **A binding decision scoped in a docs commit after the code commit is not in the code.** D-045(a) ("pending never blocks export") landed in f49c4c2, after fe4ee80; the gate still lists PENDING_DECISION blockers and `ready` is False, while the export endpoint returns 200. Check each decision line against the code, not just the card's own commit. How to apply: for any "X does not block Y" decision, probe Y with X present.
23	- **Exemption applied in one function only.** The paralegal-summary exemption lived in `unjudged_items` but not in `_judge_rows`/`judge_report`, so /judges and the judges step still counted the paralegal's edited summary as unchecked (judges FAIL next to gate ready True). How to apply: when an exemption is added, grep every consumer of the same row set (counts, steps, gate, export).
24	- **Rejudge targets wider than the decision.** `unjudged_items` includes pending items, so POST /rejudge asked 12 (4 blocked + 8 pending) where D-044 says "just those items". Check the target set against the decision text, not only the state change.
25	- Probe method that worked again: scratch DB helper blanks judge rows (server reads per request); live /trace, /export, /rejudge and /judges on 127.0.0.1:7996; stop by PID.
26	
27	**Environment gotcha:** the app reads `ZLAYT_DB` first (fixed in 94beaeb), then `DATA_DIR` (default `data/zlayt.sqlite`, untracked, shared with the orchestrator's :7860 app). To prove ZLAYT_DB is honoured, set both: ZLAYT_DB to a scratch file and DATA_DIR to an empty sentinel dir; the scratch file should appear and the sentinel stay empty. In r1 (before the fix) the app ignored ZLAYT_DB. Delete only your own cases by token. `rm` is blocked by board-guard for reviewers, and `pkill -f app.main` in a compound command can be refused or hit the shared app; kill by PID from `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
28	
29	**Method that worked:** drive the real API on a spare port for many golden cases, then a scratch `sqlite3.backup` copy + `PYTHONPATH=. .venv/bin/python` probes that call `trace.*` directly; mutation runner copies the tree once (`cp -R app tests evals docs spec`) and applies string-replace mutants per directory.
30	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:33.172Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:08:33.182Z

**tool result**
````
1	---
2	name: harness-review-patterns
3	description: Recurring defects in the board CLI / board server / hook guards seen in M0 reviews (rounds 1-2), plus reviewer-environment gotchas
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns (M0 round 2, HEAD f413e84):
9	- Hook guards are token/regex denylists: `board_guard.py` treats ANY token ending in `board.py` as an invocation (false-positives on `test_board.py`, `git diff -- tools/board.py x`); evaded by `bash -c`, `sh -c`, `eval`, globs, `python -c`. Always probe wrappers.
10	- Hook entry scripts `exec python3`; on system Python 3.9 the `X | None` annotations crash at import (outside try) -> rc 1 -> fail-open. Check `.claude/hooks/*.py` for `from __future__ import annotations` and import-time errors.
11	- Fixes tend to cover the implemented attack and skip the sibling (CSRF fixed via Origin==Host but no Host allowlist -> DNS rebinding passes). Test the round-1 acceptance line literally.
12	- Tests mirror the implementation (no Host test, no agent-sync test, no wrong-card/persona test). Agent files drifted from dossiers once between commits; no test.
13	- Free-text note markers (`assigned:`) used as machine state can be forged by any `note`.
14	
15	Round 3 (e3fbb08) additions:
16	- board_guard checks `ba[2] == "done"` positionally; `move T-1 --agent x done` (valid argparse) bypasses it. Always probe flag order, not just wrappers.
17	- Sentinel-in-review-list pattern (`orchestrator-§7.4` debt entry) short-circuits `_reviews_pass` forever; test "accept -> reopen -> later fail" for any bypass flag.
18	- Reviewer-guard false positives: `git tag -l`, `branch --show-current`, `stash list`, `reflog`, `chmod +x`; Write tool denies scratchpad while Bash allows it.
19	- Working tree gets uncommitted orchestrator edits mid-review (D-024); say which tree was tested.
20	- D-023 threat model (memory/ORCHESTRATOR_DECISIONS.md): plausible accidental spelling = finding; deliberate obfuscation = residual/nit.
21	
22	**Why:** these recurred across T-001/T-002/T-004 round 1 and 2.
23	**How to apply:** when re-reviewing harness code, re-run each round-1 acceptance test verbatim, then try the wrapper/sibling variant.
24	
25	Reviewer-environment gotchas:
26	- As a native `*-reviewer`, board-guard denies all non-read-only `board.py` subcommands even with a temp BOARD_ROOT; write-path repros cannot be run by reviewers (do not route around with python wrappers; ask the orchestrator). Read-only (`validate/show/list/status/next/inbox`) work with BOARD_ROOT set.
27	- Bash redirects are checked against the initial cwd and unexpanded `$VAR` paths: use literal absolute scratchpad paths, or put the work in a script file in the scratchpad. `... | tee path` followed by another command on the next line was also falsely denied.
28	- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.
29	- A chained shell mutation check in a scratch copy (`rm -rf` + `rsync` + `sed -i` + regenerate) was denied by the permission guard on T-016 (2026-11-01). Do not split the chain to get around it; reason from code and label the finding "not reproduced".
30	- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor).
31	- (T-028, 2026-11-01) board-guard fails closed on any Bash command it cannot tokenise ("could not parse command safely (No escaped character)") when a `python3 -c` one-liner contains backslash-escaped backticks or quotes. Put such logic in a script file under artifacts/review-evidence/ and run that file.
32	- (T-028) reviewer-write-guard denies the Write tool outside reviews/ and artifacts/review-evidence/, including the session scratchpad. Bash redirects to the scratchpad are allowed.
33	- (T-028) the session header said "not a git repository" but `git rev-parse --is-inside-work-tree` returned true at the repo root. Verify with git, quote the output, do not trust the header.
34	- (T-028) at f454c41 `app/backend/`, `app/pipeline.py` and `tests/unit/` are empty: `pytest tests/unit -q` exits 5 (no tests), `python -m app.pipeline` exits 1. Doc-stage cards cannot exercise the CLI; say so in `exercised`.
35	- (T-065/T-066 r2, 2026-11-01) reviewer-write-guard makes existing review files append-only: an Edit to `reviews/<card>-<persona>.md` is denied. Write a new `-r2.md` file instead, and fix small wording slips in the next round, not in place.
36	- (T-065/T-066 r2) `rm -rf` in a Bash chain with `git archive` was denied by the permission guard. `mkdir -p` + `git archive | tar -x -C <dir>` works, and `cp -R` for mutant copies works. Pass `/usr/bin/python3 -I script.py` for file-based edits to scratch copies (anchor-count asserts, then write).
37	- (T-065/T-066 r2) board-guard denies `python3 -c` (and a `tee` chain) containing backslash escapes or backticks, including `\n` in a string. Put JSON checks in a script file under the scratchpad and run that.
38	- (T-065/T-066 r2) `board.py validate <path>` is read-only and works on a review file; use it to confirm the D.2 shape before replying.
39	- (T-070 r2, 2026-11-01) A shell `>` redirect into the scratchpad is denied by board-guard ("reviewers may only write under reviews/..."), even though `tar -x -C` and `cp -R` into the same dir pass. Capture output with `2>&1; echo rc=$?` inside the command instead of redirecting. Chained `$(...)` loops with nested quotes trip git-guard's parser; use one probe per Bash call.
40	- (T-080 r3, 2026-11-02) board-guard reads a `>` inside a Bash command (even in a grep pattern such as `pending > 0`) as a redirect and denies the call. Use `grep -e` patterns without angle brackets. A `Write` into the scratchpad is denied by reviewer-write-guard, but a `cat <<'EOF' > scratchpad/file` heredoc in Bash works (no `>` problem there). `rm -rf` is denied; `mkdir -p` plus `cp -R` works. macOS has no `timeout` binary; pass the pytest/e2e timeout parameter instead. Kill the scratch server by its PID from `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
41	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:38.734Z

The harness gotchas I hit this round are already recorded, so I won't duplicate them. I'll add the r4 pattern to the existing T-080 memory file and update the index line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:42.082Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t080_trace_review_patterns.md",
 "old_string": "- Probe method that worked again: scratch DB helper blanks judge rows (server reads per request); live /trace, /export, /rejudge and /judges on 127.0.0.1:7996; stop by PID.\n",
 "new_string": "- Probe method that worked again: scratch DB helper blanks judge rows (server reads per request); live /trace, /export, /rejudge and /judges on 127.0.0.1:7996; stop by PID.\n\nT-080 r4 (10d358e, D-045 gate: one `export_blockers` list, pending as warnings; verdict pass: 0 blockers, 0 majors, 2 minor, 1 nit; reviews/T-080-staff-engineer-r4.md). r3 major and r3 judges-step minor and nit are closed; r3 rejudge-scope minor still open.\n- **A carry-over finding stays open until its file is in the fix diff.** rejudge.py was not in 10d358e, so the r3 rejudge-scope minor was still there, and test_trace.py:906 (`asked == n`) now codifies it. How to apply: for each prior finding, check whether its cited file appears in the round's `git show --stat`; if not, say \"still open\" and name the test that locks it in.\n- **Export refusal status: 422 for state conflicts.** Run in progress, run failed and nothing accepted all return 422 export_blocked. The refusal is right (fail-closed); 422 means invalid content, and the spec reserves 409 for state objections (R-RV-3). Minor, because the spec names no export code.\n- **Shared-list invariant test covers the gate and the export, not each guard.** Removing the export_payload guard (M3) was caught only by the nine-state invariant test. How to apply: a single-function guard in one consumer needs one test of its own, not just the shared invariant.\n- **Clean mutant beats crude.** A mutant that injected an unknown reason key (ITEMS_PENDING with no TRACE_WHY entry) raised KeyError in unrelated tests and muddied the kill count; a mutant reusing PENDING_DECISION gave 7 precise failures. Report the clean one.\n"
}
````

### User / tool · 2026-11-02T04:08:42.190Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t080_trace_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:42.392Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T04:08:42.400Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
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
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r3: judge-never-ran summaries, gate vs export agreement, D-045(a) pending-block not implemented, exemption in one consumer only
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:44.205Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r3: judge-never-ran summaries, gate vs export agreement, D-045(a) pending-block not implemented, exemption in one consumer only",
 "new_string": "- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409"
}
````

### User / tool · 2026-11-02T04:08:44.306Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:08:46.348Z

Verdict pass for T-080 at 10d358e (0 blockers, 0 majors; 2 minors, 1 nit: rejudge still re-asks pending items, 422 for state refusals, D-045(b) wording), review at `/Users/arsis/zlayt-pm-project/reviews/T-080-staff-engineer-r4.md`.
