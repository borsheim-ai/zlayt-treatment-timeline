# Subagent: T-177 r2 check (T-177 r2 check)

Source: `agent-a5bfad7153c9f2924.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:04:29.354Z

Run the round-2 check of board card T-177 (commit 4fcf9cd, D-065 as amended) in /Users/arsis/zlayt-pm-project. Read reviews/T-177-staff-engineer.md: 1 blocker, where the judge panel named claude-sonnet-5-5, and 2 majors.

On a `git archive HEAD` copy, with the curated set:
- no classic surface names a drafting model for a prepared item: the judge panel, trace, audit, tooltips and banner;
- the badge tooltip matches the D-065 text in memory/ORCHESTRATOR_DECISIONS.md;
- the banner mentions the AI check.

With the recorded set, items still name claude-sonnet-5-5. Run tests/e2e/test_demo_provenance.py with E2E_REQUIRE_DB=1 on your own port. The mixed-set residual F4 is accepted as debt.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-177-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Stop only your own PIDs. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:32.304Z

I'll start with the dossier, the prior round-1 review, and the T-177 memory notes.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:32.511Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T21:04:32.519Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:32.733Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer.md"
}
````

### User / tool · 2026-11-02T21:04:32.740Z

**tool result**
````
1	# T-177 (D-065 honest demo provenance): staff-engineer review
2	
3	**Verdict: fail (1 blocker, 2 majors, 1 minor, 1 nit).** The PM's acceptance test passes on commit 04ea2bf: no "AI draft" or "recorded AI answers" text on a curated item, the trace generator step reads `hand-checked (qa)` with a prepared-answer label, the audit rows carry `hand-checked (qa)`, and the recorded set keeps its AI labels. The provenance is not complete, though. On the curated demo, the "How the AI was checked" panel still says `Drafted by claude-sonnet-5-5`, and the case and judges payloads still name `claude-sonnet-5-5` as the generator. That is the exact over-claim D-065 forbids, and no test covers it. The badge tooltip also points to an eval report that does not hold the answers.
4	
5	Scope: commit 04ea2bf (the card commit). HEAD de5cb3a has no diff under `app/` or `tests/` relative to 04ea2bf, so the archive matches HEAD for code. Evidence is under `artifacts/review-evidence/T-177-staff-engineer/` (git archive copy) and the `artifacts/review-evidence/T-177-staff-engineer-*` files.
6	
7	## Acceptance checks (PM's test, curated and recorded)
8	
9	| Check | Result |
10	|---|---|
11	| `tests/unit/test_prepared_provenance.py` | 6 passed |
12	| `E2E_REQUIRE_DB=1 tests/e2e/test_demo_provenance.py` | 4 passed |
13	| `/items/e1/trace` generator step model | `hand-checked (qa)`, label "Prepared answer, standing in for the AI draft" |
14	| `/audit` generator rows (curated) | 18 of 18 `hand-checked (qa)`, `prepared: true` |
15	| Curated page text | no "AI draft" or "recorded AI answers"; badge "Demo: sample answers prepared by our team" |
16	| Recorded set labels | "AI draft", model `claude-sonnet-5-5`, badge "Demo: recorded AI answers" |
17	
18	## Findings
19	
20	**F1 (blocker): the curated demo still names a model as drafter.** On the curated set, the "How the AI was checked" panel renders `Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5` and the label "how a second AI model checked the first AI's drafts". The same payloads name the generator as `claude-sonnet-5-5`. `app/backend/present.py:262` says the provenance exists "so no screen or payload names a model for an answer no model gave". The panel and payloads contradict that comment and D-065 ("never presented as model output"). The new tests pass because they only assert the trace, audit, item and health fields.
21	
22	**F2 (major): the tooltip names a place the answers are not.** `app/frontend/app.js:16-17` says "The AI's own answers on these cases are in the evaluation report." The run files store `summary_sha`, not the summary or excerpt text. `evals/reports/runs/20261102T093020Z/sample.json` item keys are `date, date_status, generator_prompt_version, id, judge, kind, provider, reasons, record_ids, state, summary_sha`. The only report text that contains the sample summary's opening words is a quoted phrase in `evals/reports/determinism-diagnosis.md:26`. The tooltip text is pinned by D-065, so this needs a decision (see questions).
23	
24	**F3 (major): the curated banner says "checked by code" and omits the AI check.** `app/backend/api.py:37` (PREPARED_BANNER) reads "...prepared by our team and checked by code; you decide every item". On the same curated items, the trace has a "Second AI check" step (`judge_1`, model `claude-haiku-5-5`, `prepared: false`) and the judges endpoint counts 19 items checked by AI. The banner under-states who checked the items.
25	
26	**F4 (minor): the banner is global, provenance is per call.** `app/backend/api.py:125-129` (`answers()`) decides prepared versus recorded from the fixture set name alone, while item provenance is per call (`app/backend/present.py:262-273`, `app/llm/audited.py:68-79`). `app/llm/backends/fixture.py:23-24` falls back to the recorded set when a curated key is missing. A curated run with one missing key would show a recorded AI answer labelled "AI draft" under a banner saying all summaries were prepared. Not reproduced on the sample: 9 of 9 extract and 9 of 9 flag calls are `prepared: true`.
27	
28	**F5 (nit): prepared rows still carry a prompt version.** The curated probe's audit row has `"prompt_version": "extract_v1"`, a real `prompt_sha256`, and `"prepared": true`. `app/frontend/timeline.js` (why-generator line) shows "hand-checked (qa) · extract_v1". No prompt produced these answers.
29	
30	## Commands and outputs
31	
32	- `git show --stat 04ea2bf`; `git diff 04ea2bf HEAD -- app tests | wc -l` gives 0.
33	- `python3 tools/board.py show T-177`: status in_review, AC 1 done with evidence.
34	- `reviews/GATE-M3-product-manager.md` blocker read; `memory/ORCHESTRATOR_DECISIONS.md` D-065 to D-068 read.
35	- `git archive 04ea2bf` extracted to `artifacts/review-evidence/T-177-staff-engineer/`.
36	- Unit and e2e outputs: `artifacts/review-evidence/T-177-staff-engineer-unit-prepared.out`, `artifacts/review-evidence/T-177-staff-engineer-e2e-provenance.out`.
37	- API probes (TestClient, curated and recorded): `artifacts/review-evidence/T-177-staff-engineer-curated-probe.out`, `artifacts/review-evidence/T-177-staff-engineer-recorded-probe.out`, `artifacts/review-evidence/T-177-staff-engineer-curated-judges.out`, `artifacts/review-evidence/T-177-staff-engineer-recorded-e1.out`. Probe scripts: `artifacts/review-evidence/T-177-staff-engineer-probe.py`, `artifacts/review-evidence/T-177-staff-engineer-judge-panel-probe.py`.
38	- Browser render of the curated case on a private server: `artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out` and `artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png`.
39	- Mutation checks, in the archive copy and restored from `git show 04ea2bf:...` (cmp identical): removing `_prepared_model` in `app/llm/audited.py` fails 5 tests; forcing `is_prepared` to False fails 3 unit tests.
40	- Grep of tests for `models` assertions: none for the judges or case payloads.
41	- The shared app on :7860 (PID 86899) was not touched. My two private server PIDs (94279, 94777) were terminated; `ps` confirms none alive.
42	
43	## What is right
44	
45	- Audit and trace model swap is mutation-guarded: removing the audit model swap or forcing the prepared flag off makes 3 to 5 tests fail.
46	- The PM's acceptance points hold on 04ea2bf: prepared trace label, `hand-checked (qa)` audit rows, recorded set keeps AI labels and model ids.
47	- `memory/contracts/api.md:57` and `:836-841` document `answers`, `prepared` on items, audit, trace and narrative, and the payloads I observed match them.
48	
49	## Verdict rule
50	
51	One blocker (F1), so `fail`. Majors F2 and F3 must also be fixed before the gate.
52	
53	```json
54	{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
55	 "scope": "commit 04ea2bf (card commit; HEAD de5cb3a has no app/ or tests/ diff from it); git archive copy at artifacts/review-evidence/T-177-staff-engineer/; no app URL (private servers on random loopback ports; shared :7860 untouched); sample case (sample=True) on FIXTURE_SET=curated and on the recorded set",
56	 "exercised": [
57	  "python3 tools/board.py show T-177; git show --stat 04ea2bf; git diff 04ea2bf HEAD -- app tests (0 lines)",
58	  "reviews/GATE-M3-product-manager.md blocker; memory/ORCHESTRATOR_DECISIONS.md D-065 to D-068",
59	  "git archive 04ea2bf extracted; read app/backend/present.py, trace.py, api.py, app/llm/audited.py, app/llm/backends/fixture.py, app/frontend/app.js, judges.js, stepper.js, timeline.js, audit.js; read the two new test files",
60	  ".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q: 6 passed",
61	  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v: 4 passed",
62	  "TestClient probes on curated and recorded sets: /api/health, /api/cases/{tok}, /audit, /items/e1/trace, /judges",
63	  "Playwright on a private curated server: read badge, badge title, banner, judge-label, judge-model-line, judge-totals; screenshot of the judge panel",
64	  "Mutation checks in the archive copy: audit model swap removed (5 failed); is_prepared forced False (3 failed); file restored and cmp-verified",
65	  "Inspected evals/reports/runs/20261102T093020Z/sample.json keys; grep of evals/reports for the sample summary text",
66	  "Grep of tests for models/judge-model-line assertions (none for judges or case payloads)",
67	  "memory/contracts/api.md lines 57 and 836-841 read against the code"
68	 ],
69	 "verdict": "fail",
70	 "scores": {"provenance_honesty": 2, "pm_acceptance_criteria": 4, "api_fields_documented": 4, "test_strength": 3, "llm_boundary": 5},
71	 "findings": [
72	  {"severity": "blocker", "title": "Curated demo still names claude-sonnet-5-5 as the drafter of hand-written answers (judge panel, case and judges payloads)",
73	   "evidence": "Rendered curated case (artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out): judge-model-line 'Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5'; judge-label \"how a second AI model checked the first AI's drafts\"; screenshot artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.png. app/frontend/judges.js:166-168 renders m.generator from d.models. app/backend/trace.py:1003 returns 'models': cx.models (config). GET /api/cases/{tok}/judges on FIXTURE_SET=curated returns models.generator 'claude-sonnet-5-5' (artifacts/review-evidence/T-177-staff-engineer-curated-judges.out). GET /api/cases/{tok} on curated returns models.generator 'claude-sonnet-5-5'. app/backend/present.py:262 comment says no payload names a model for an answer no model gave.",
74	   "why_it_matters": "D-065 (binding): curated answers are never presented as model output. The panel is part of the demo the PM tested and it attributes the team's hand-written summaries to a named model. The paralegal or a reviewer reading the panel gets the wrong provenance. The new tests pass because they check trace, audit, item and health fields only, so the same blocker class would pass CI again.",
75	   "fix": "On a prepared case, the drafter line says the summaries were prepared by the team (no model), for example 'Drafted by: prepared answers (hand-checked by the team), checked by claude-haiku-5-5'. GET /api/cases/{tok} and GET /judges return models.generator as null or 'hand-checked (qa)' when the case's generator answers are prepared. The judge-label sentence follows the same rule. Recorded and live cases are unchanged.",
76	   "acceptance_test": "Unit: on FIXTURE_SET=curated, GET /api/cases/{tok}/judges and GET /api/cases/{tok} have models.generator != 'claude-sonnet-5-5'. E2E (curated): the judge-model-line text does not contain 'claude-sonnet-5-5' and says the summaries were prepared. E2E (recorded set): the same line still says 'claude-sonnet-5-5'."},
77	  {"severity": "major", "title": "Badge tooltip says the AI's answers are in the evaluation report; they are not",
78	   "evidence": "app/frontend/app.js:16-17: \"The AI's own answers on these cases are in the evaluation report.\" evals/reports/runs/20261102T093020Z/sample.json item keys: date, date_status, generator_prompt_version, id, judge, kind, provider, reasons, record_ids, state, summary_sha (no summary or excerpt text). The only evals/reports text with the sample summary's opening words is a quoted phrase at evals/reports/determinism-diagnosis.md:26.",
79	   "why_it_matters": "The tooltip is the one place the demo tells a reader where to verify the AI's own answers. It sends them to a file that holds hashes and verdicts. That is a false pointer on a provenance label, the kind of over-claim the PM blocked.",
80	   "fix": "Either write each entry's generator summary and excerpt for the sample case into the eval report (an eval-runner change, with a report path) or reword the tooltip to what the report holds. The sentence is pinned by D-065, so the wording needs a decision (see questions_for_chris).",
81	   "acceptance_test": "Either: a new evals/reports/*.md contains the sample case's generator summaries and excerpts, and a unit test greps for one of them. Or: the tooltip text is changed, and the e2e test asserts the new text."},
82	  {"severity": "major", "title": "Curated banner says 'checked by code' and omits the AI check that runs on the same items",
83	   "evidence": "api.py:37 PREPARED_BANNER: 'In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item' (rendered: artifacts/review-evidence/T-177-staff-engineer-curated-judge-panel.out line 2). Same curated items: trace step judge_1 'Second AI check: is the summary supported by the quote?', model claude-haiku-5-5, prepared false (artifacts/review-evidence/T-177-staff-engineer-curated-probe.out); /judges items_judged 19 (artifacts/review-evidence/T-177-staff-engineer-curated-judges.out).",
84	   "why_it_matters": "The banner states who checked the items. It leaves out that a second AI model checked every item, so the page contradicts itself ('checked by code' above a 'Second AI check' step). D-065 requires plain wording to stay truthful.",
85	   "fix": "Rewrite the prepared banner to name both: prepared by the team, then a second AI model checked each summary against its quote, and the reader decides every item.",
86	   "acceptance_test": "Unit: GET /api/health on FIXTURE_SET=curated has answers 'prepared' and an ai_banner that mentions a second AI check and does not say 'checked by code' alone."},
87	  {"severity": "minor", "title": "Banner and badge are decided per fixture set, while provenance is per call; a missing curated key would mislabel an item",
88	   "evidence": "app/backend/api.py:125-129 answers() uses fixture.answer_source() (app/llm/backends/fixture.py:48-50, fixture_dir().name only). Per-call provenance: app/backend/present.py:262-273, app/llm/audited.py:68-79. app/llm/backends/fixture.py:23-24 falls back to the recorded set when a curated key file is missing. Not reproduced: curated probe shows 9 of 9 extract and 9 of 9 flags calls prepared true.",
89	   "why_it_matters": "On a curated run with one missing key, the item would be a recorded AI answer labelled 'AI draft' under a banner saying all summaries were prepared by the team. Provenance would be wrong on exactly the case where the fixtures are incomplete.",
90	   "fix": "Derive the badge and banner from the items shown (all prepared, all recorded, or mixed), or fail the run when a curated set misses a key instead of falling back.",
91	   "acceptance_test": "Unit: copy the curated set minus one generator file into a temp LLM_FIXTURE_DIR named curated and FIXTURE_SET=curated; the run fails or the health answers value is 'mixed', never 'prepared'."},
92	  {"severity": "nit", "title": "Prepared rows still show a prompt version and prompt hash",
93	   "evidence": "Curated probe, audit row: \"prompt_version\": \"extract_v1\", \"prompt_sha256\": \"b74b563d...\", \"prepared\": true (artifacts/review-evidence/T-177-staff-engineer-probe.py, AUDIT_ONE line). app/frontend/timeline.js why-generator line shows '${lad.generator.model} · ${lad.generator.prompt_version}', which renders 'hand-checked (qa) · extract_v1'.",
94	   "why_it_matters": "A prompt version and hash say a prompt produced the answer. Nothing was prompted; the team wrote it. Small, but it is the same provenance question in a different field.",
95	   "fix": "On prepared rows, set prompt_version to null and show 'hand-written for the demo' in the why line, or omit the prompt hash.",
96	   "acceptance_test": "Unit: prepared audit rows have prompt_version null (or a 'hand-written' marker) and no prompt_sha256 used as a model prompt."}
97	 ],
98	 "whats_right": [
99	  "Audit model swap and prepared flag are mutation-guarded: removing the audit model swap fails 5 tests; forcing is_prepared False fails 3 (archive copy, restored, cmp-verified).",
100	  "PM acceptance holds on 04ea2bf: trace generator step model 'hand-checked (qa)' with the prepared label; the recorded set keeps 'claude-sonnet-5-5' and the AI wording.",
101	  "memory/contracts/api.md:57 and :836-841 document answers, prepared fields on items, audit, trace and narrative; the observed payloads match."
102	 ],
103	 "questions_for_chris": [
104	  "D-065 pins the tooltip 'The AI's own answers on these cases are in the evaluation report.' The report does not hold them. Do you want the sample case's per-entry answers written into the eval report (a runner change), or the tooltip reworded now?",
105	  "On the curated demo, the second AI check is a real recorded model answer (claude-haiku-5-5). Should the 'How the AI was checked' panel stay on the curated set with the wording fixed (F1), or be hidden there?"
106	 ]}
107	```
108	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:32.985Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_provenance_patterns.md"
}
````

### User / tool · 2026-11-02T21:04:32.991Z

**tool result**
````
1	---
2	name: t177-provenance-patterns
3	description: T-177 (D-065 prepared answers): payload-level model names and tooltip pointers escaped the per-item provenance tests
4	metadata:
5	  type: project
6	---
7	
8	Per-item provenance fixed (trace step, audit row, item ladder) while case, judges and banner-level surfaces still named the model or claimed a location that did not hold the answers.
9	
10	**Why:** D-065 forbids presenting curated (hand-written) answers as model output; the PM's acceptance test only checked trace, audit, item and badge text. The judges panel (`app/frontend/judges.js:166-168`, `m.generator` from `trace.py:1003` `cx.models`) still printed "Drafted by claude-sonnet-5-5" on the curated demo, and `GET /api/cases/{tok}` plus `/judges` returned `models.generator` = claude-sonnet-5-5. No test asserted those fields.
11	
12	**How to apply:**
13	- For any "never presented as X" decision, grep every payload and template for the old model name on the curated path (case `models`, `/judges` `models`, banners, panel copy), not only the per-item fields the card names.
14	- The eval-report tooltip ("the AI's own answers are in the evaluation report") was false: `evals/reports/runs/*/sample.json` stores `summary_sha`, not text. Check that a pointer's target contains what it promises.
15	- Banner wording "checked by code" hid the second AI check that runs on the same curated items. Check banners against every check step on the page.
16	- Global badge/banner decided by fixture-set name vs per-call provenance: a fallback to the recorded dir (`fixture.py:23-24`) can mislabel one item. Probe with a missing key.
17	- Mutation pattern that worked: break `_prepared_model` in `app/llm/audited.py` in an archive copy, restore via `git show <sha>:path`, cmp-verify.
18	- Playwright: a collapsed `<details>` child is hidden; click the `judge-summary` toggle, then read `.first.text_content()`; `inner_text` times out.
19	
20	Related: [[project_llm_stage_review_patterns]], [[feedback_frontend_text_coupling]], [[project_t167_plain_wording_patterns]].
21	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:33.266Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_verify_pid_before_kill.md"
}
````

### User / tool · 2026-11-02T21:04:33.276Z

**tool result**
````
1	---
2	name: feedback_verify_pid_before_kill
3	description: a PID captured with $! from a subshell can be a wrapper, not the server; run ps -p and lsof on the port before kill, and kill the listener, not the recorded number
4	metadata:
5	  type: feedback
6	---
7	
8	Before killing a server, check the PID you recorded with `ps -o pid,ppid,command -p <pid>` and check the listener with `lsof -iTCP:<port> -sTCP:LISTEN -n -P`. Kill the listener and confirm the port is closed.
9	
10	**Why:** T-119 r3 (this session): I wrote `echo $!` from a subshell that started `nohup python -m app.main &`. The recorded PID (6353) was a bash wrapper, not the server. I killed it without checking. The real server (6354) stayed up and had to be stopped by its listener PID. The ports were closed only after that second kill.
11	
12	**How to apply:** when a review starts its own servers, record the listener PID with lsof after the health check, not `$!`. Stop only PIDs whose command line shows the app, and verify both ports closed afterwards. If a wrong PID was killed, say so in the review's exercised list.
13	
14	Related: [[project_t119_keyboard_coverage_patterns]], [[feedback_shared_scratchpad]].
15	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:33.514Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_reviewer_scratch_writes.md"
}
````

### User / tool · 2026-11-02T21:04:33.541Z

**tool result**
````
1	---
2	name: reviewer-scratch-writes
3	description: Reviewer Write tool is blocked outside reviews/ and artifacts/review-evidence/ (scratchpad refused); keep helper scripts and sweep outputs there; shell lines with backticks or triple backticks trip the board guard
4	metadata:
5	  type: feedback
6	---
7	
8	Write tool calls to the session scratchpad were refused by reviewer-write-guard. Shell `cp` and `cat >` into the scratchpad still worked. Keep reviewer helper scripts and copied evidence in artifacts/review-evidence/<card>-rN/ so the Write tool is allowed.
9	
10	**Why:** the write guard allows only reviews/, artifacts/review-evidence/ and the agent memory dir. The scratchpad is outside that list for Write, and the error came back on the first Write.
11	
12	**How to apply:** put sweep scripts, mutants and copied outputs under artifacts/review-evidence/. Do not put backticks or triple backticks inside a shell command line; the git-guard board-guard denies unparseable commands. Write a small .py file instead and run it with python -I.
13	
14	**T-169 r2 addendum:** `git clone` plus `git checkout --detach <sha>` was denied by board-guard when the clone sat under artifacts/review-evidence/ ("reviewers may not run git checkout in the project"). The same two commands worked in a clone under the session scratchpad (/private/tmp/...), so put pinned clones in the scratchpad and evidence in artifacts/review-evidence/. A python -c line containing backtick-escaped fences was also denied; use a .py file.
15	
16	Related: [[project_t167_plain_wording_patterns]], [[feedback_bind_to_named_reference]].
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:35.160Z

Next I'll check the repo state: the commit, HEAD, the card, and the D-065 text.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:35.941Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 8 && echo \"---HEAD---\" && git rev-parse HEAD && echo \"---4fcf9cd---\" && git rev-parse --verify 4fcf9cd && git show --stat 4fcf9cd | head -60 && echo \"---show T-177---\" && python3 tools/board.py show T-177 | head -120",
 "description": "Show git log, HEAD, commit stat, and T-177 card"
}
````

### User / tool · 2026-11-02T21:04:36.154Z

**tool result**
````
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs
4fcf9cd fix(frontend): T-177 r2 honest provenance on every surface: prepared items name no drafting model (judge panel, models in health/case/judges/export, case trace, tooltip, banner, audit and ladder rows)
964505b docs(qa): T-045 r3: sensors record names the commit for the unit count (5782 at b824a6c)
b01382f feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)
b824a6c fix(evals): T-045 r3: --record-latest refuses non-live backends and recomputes the ship bar from the report body and per-run directory; records sha256 and source commit
a56f189 fix(backend): T-178 GATE-M3 chaos: interrupted runs recovered at startup, stale-tab 409 stale_item, invisible characters stripped and lone surrogates replaced (no 500)
de5cb3a docs(orchestrator): D-068 guided four-step UI redesign (Chris)
7c73294 test(qa): T-045 r2 sensors record (unit 5698, e2e 412, latest.json live, rejected-item claim corrected)
---HEAD---
ac678bc3cf42c8aecd06bb17828a4ea91571dc3a
---4fcf9cd---
4fcf9cdacddac481118f6e4a629feeabb382ef4a
commit 4fcf9cdacddac481118f6e4a629feeabb382ef4a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:03:54 2026 -0600

    fix(frontend): T-177 r2 honest provenance on every surface: prepared items name no drafting model (judge panel, models in health/case/judges/export, case trace, tooltip, banner, audit and ladder rows)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py                     | 15 ++++--
 app/backend/present.py                 | 12 +++++
 app/backend/trace.py                   | 25 ++++++----
 app/frontend/app.js                    |  2 +-
 app/frontend/audit.js                  |  4 +-
 app/frontend/judges.js                 | 11 +++--
 app/frontend/stepper.js                |  3 +-
 app/frontend/timeline.js               |  2 +-
 memory/contracts/api.md                |  5 +-
 tests/e2e/conftest.py                  |  2 +-
 tests/e2e/test_demo_provenance.py      | 83 ++++++++++++++++++++++++++++++++--
 tests/unit/test_prepared_provenance.py | 47 +++++++++++++++++++
 12 files changed, 183 insertions(+), 28 deletions(-)
---show T-177---
---
id: "T-177"
title: "GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:09:00Z"
updated_at: "2026-11-02T21:04:13Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T20:38:44Z"
rounds: 1
commits: ["04ea2bf", "4fcf9cd"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-177-staff-engineer.md", "at": "2026-11-02T20:38:36Z"}
ac:
  - {"n": 1, "text": "E2E on FIXTURE_SET=curated: no 'AI draft' or 'recorded AI answers' on a curated item; /items/e1/trace generator step model is not claude-sonnet-5-5 and names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'; with the recorded set, labels say AI; unit + e2e", "done": true, "evidence": "git archive of the commit tree (temp index), E2E_REQUIRE_DB=1: tests/e2e 419 passed 1 skipped; tests/unit 5780 passed 8 skipped; new tests test_demo_provenance.py (judge panel, whole-DOM scan curated, recorded unchanged) + test_prepared_provenance.py (models in health/case/judges/export, case trace)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:09:02Z orchestrator: assigned: backend
- 2026-11-02T20:09:11Z backend: claimed
- 2026-11-02T20:21:28Z backend: Committed 04ea2bf (temp index). Tests first: tests/unit/test_prepared_provenance.py (6) + tests/e2e/test_demo_provenance.py (4, curated + recorded-set private server). Unit suite 5695 passed in working tree. Verifying e2e from git archive HEAD copy now.
- 2026-11-02T20:31:43Z backend: AC 1 checked: git archive 04ea2bf, E2E_REQUIRE_DB=1: tests/e2e (424 passed, 1 skipped; 1 timing flake test_mvp_polish decided_row passes alone, also on 0c4284f) incl. new tests/e2e/test_demo_provenance.py (curated+recorded private servers) and tests/unit/test_prepared_provenance.py (6); full unit suite 5695 passed in working tree
- 2026-11-02T20:31:43Z backend: moved in_progress -> in_review
- 2026-11-02T20:33:30Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T20:38:36Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-177-staff-engineer.md; round 1; findings:
    - [blocker] Curated demo still names claude-sonnet-5-5 as the drafter of hand-written answers (judge panel, case and judges payloads) — fix: On a prepared case, the drafter line says the summaries were prepared by the team (no model), for example 'Drafted by: prepared answers (hand-checked by the team), checked by claude-haiku-5-5'. GET /api/cases/{tok} and GET /judges return models.generator 
    - [major] Badge tooltip says the AI's answers are in the evaluation report; they are not — fix: Either write each entry's generator summary and excerpt for the sample case into the eval report (an eval-runner change, with a report path) or reword the tooltip to what the report holds. The sentence is pinned by D-065, so the wording needs a decision (see questions_for_chris).
    - [major] Curated banner says 'checked by code' and omits the AI check that runs on the same items — fix: Rewrite the prepared banner to name both: prepared by the team, then a second AI model checked each summary against its quote, and the reader decides every item.
    - [minor] Banner and badge are decided per fixture set, while provenance is per call; a missing curated key would mislabel an item — fix: Derive the badge and banner from the items shown (all prepared, all recorded, or mixed), or fail the run when a curated set misses a key instead of falling back.
- 2026-11-02T20:38:36Z orchestrator: assigned: frontend
- 2026-11-02T20:38:44Z frontend: claimed
- 2026-11-02T20:46:36Z frontend: Round 2 in progress. Tests first (tests/unit/test_prepared_provenance.py +4, tests/e2e/test_demo_provenance.py +3: judge panel, whole-DOM scan incl. closed panels/titles, recorded set unchanged). Fixes: present.models_for (generator='hand-checked (qa)', generator_prepared) used by /health, case view, trace _Cx (so /judges), export provenance; judges.js line + label; badge tooltip reworded (ASSUMPTION: the eval report holds hashes not answers, so the tooltip now says 'Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.'; D-065's old pointer sentence dropped, orchestrator please confirm in ORCHESTRATOR_DECISIONS); banner now names the second AI check; case-level trace step + judges step labels; prompt version/hash hidden for prepared rows (F5). F4 (per-call mixed set) left as residual: models_for only flags generator_prepared when ALL generator calls are prepared.
- 2026-11-02T21:04:13Z frontend: AC 1 checked: git archive of the commit tree (temp index), E2E_REQUIRE_DB=1: tests/e2e 419 passed 1 skipped; tests/unit 5780 passed 8 skipped; new tests test_demo_provenance.py (judge panel, whole-DOM scan curated, recorded unchanged) + test_prepared_provenance.py (models in health/case/judges/export, case trace)
- 2026-11-02T21:04:13Z frontend: moved in_progress -> in_review

## Handoff
What changed (r2, 4fcf9cd): F1 blocker - present.models_for gives generator='hand-checked (qa)' + generator_prepared on /health, case view, /judges (trace _Cx) and export provenance; judges.js line reads 'Prepared by our team (not by an AI model), checked by claude-haiku-5-5' and label no longer says 'first AI drafts'; case-level trace extract/judges step labels; Why ladder 'Prepared by', no prompt version/hash on prepared audit/stepper rows (F5). F2 - badge tooltip reworded to what is true (eval report holds hashes only); F3 - banner names the second AI check. How verified: tests first; git archive of the commit tree, E2E_REQUIRE_DB=1, e2e 419 passed/1 skipped, unit 5780 passed; whole-DOM scan test on curated (closed panels + titles) and recorded set still says Drafted by claude-sonnet-5-5. Left: F4 (mixed set per call; not detected), D-065 tooltip sentence changed by assumption (orchestrator confirm), guided app untouched and should read models.generator_prepared. Surprised: shared tree held others' hunks in api.py/present.py/audit.js, committed only mine via patch into a temp index; the case-level trace step also said 'AI drafted' and only the broad DOM scan caught it.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:36.383Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-065\" -A 30 memory/ORCHESTRATOR_DECISIONS.md | head -120",
 "description": "Read D-065 text in orchestrator decisions"
}
````

### User / tool · 2026-11-02T21:04:36.467Z

**tool result**
````
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
74-| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
75-| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
76-| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:42.831Z

The card is in_review with commit 4fcf9cd, but HEAD has moved to ac678bc. I'll check whether anything under `app/` or `tests/` changed after 4fcf9cd, and confirm the working tree state.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:43.648Z

**tool call — Bash**
````
{
 "command": "echo \"--- diff 4fcf9cd..HEAD stat for app tests evals ---\" && git diff --stat 4fcf9cd HEAD -- app tests evals | tail -20; echo \"--- files changed in HEAD commit ---\"; git show --stat --format='%h %s' HEAD | head -40; echo \"--- status (short) ---\"; git status --short | head -30",
 "description": "Check HEAD drift from 4fcf9cd and working tree status"
}
````

### User / tool · 2026-11-02T21:04:43.808Z

**tool result**
````
--- diff 4fcf9cd..HEAD stat for app tests evals ---
 app/config.py | 39 +++++++++++++++++++++++++++++++++++++++
 1 file changed, 39 insertions(+)
--- files changed in HEAD commit ---
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs

 .dockerignore                   | 14 +++++++++
 .env.example                    | 23 ++++++++++++++
 Dockerfile                      | 28 +++++++++++++++++
 Makefile                        | 25 +++++++++++++++
 README.md                       | 67 +++++++++++++++++++++++++++++++++++++++++
 app/config.py                   | 39 ++++++++++++++++++++++++
 deploy/HUGGINGFACE.md           | 49 ++++++++++++++++++++++++++++++
 deploy/REPLIT.md                | 21 +++++++++++++
 deploy/TIMING.md                |  3 ++
 deploy/hf_push.sh               | 30 ++++++++++++++++++
 deploy/hf_space_frontmatter.yml | 11 +++++++
 deploy/replit/.replit           | 20 ++++++++++++
 run.sh                          | 40 ++++++++++++++++++++++++
 13 files changed, 370 insertions(+)
--- status (short) ---
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
 M app/backend/case_extras.py
MM app/backend/case_list.py
 M app/backend/export.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:47.808Z

HEAD is ac678bc, one commit past the card's 4fcf9cd, and that later commit only adds release config. Next I'll read the full r2 diff for the card commit, since the review covers every line in scope.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:48.145Z

**tool call — Bash**
````
{
 "command": "git show 4fcf9cd -- app/ | head -400",
 "description": "Show full code diff of the r2 commit for app/"
}
````

### User / tool · 2026-11-02T21:04:48.245Z

**tool result**
````
commit 4fcf9cdacddac481118f6e4a629feeabb382ef4a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:03:54 2026 -0600

    fix(frontend): T-177 r2 honest provenance on every surface: prepared items name no drafting model (judge panel, models in health/case/judges/export, case trace, tooltip, banner, audit and ladder rows)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 64183fa..2c031c2 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -34,7 +34,7 @@ LIBRARY = ROOT / "evals" / "library"
 VERSION = "0.1.0"
 BANNER = "Synthetic data only — never paste real records"
 AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
-PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item"      # D-065
+PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item"      # D-065
 STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
 _ERR_STATUS = {"bad_request": 400, "input_too_large": 413, "unsupported_language": 400}
 _PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
@@ -132,9 +132,15 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         from app.llm.backends import fixture
         return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
 
-    def models():
+    def config_models():
         return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
 
+    def models():
+        """The models /health shows. T-177 r2: on the prepared (curated) set no model drafts an answer, so none is named as the drafter. Per-case payloads use present.models_for (from the case's own calls)."""
+        base = config_models()
+        prepared = answers() == "prepared"
+        return dict(base, generator=present.PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
+
     def conn():
         return DB.connect(app.state.db_path)
 
@@ -374,7 +380,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         c = conn()
         try:
             case = get_case(c, token)
-            v = present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
+            v = present.case_view(c, token, backend=backend(), models=present.models_for(c, token, config_models()), demo_mode=demo_mode())
             return {**v, "title": case_list.case_title(c, case), "next_action": case_list.next_action(c, token, case)}          # T-157
         finally:
             c.close()
@@ -611,7 +617,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                               "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                               "rejected": present.rejected_count(c, token)}
-            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
+            mm = present.models_for(c, token, config_models())
+            ex["provenance"] = {"generator_model": mm["generator"], "judge_model": mm["judge"], "generator_prepared": mm["generator_prepared"], "backend": backend(),
                                 "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                 "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                 "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
diff --git a/app/backend/present.py b/app/backend/present.py
index 3138e1c..067601c 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -277,6 +277,18 @@ def with_provenance(conn, case_id, views):
                 gen["model"] = call["model"]
 
 
+PREPARED_MODEL = "hand-checked (qa)"      # what a prepared (curated) answer names as its maker; the same text the audit rows carry
+
+
+def models_for(conn, case_id, base, calls=None):
+    """D-065 (T-177 r2): the {generator, judge} model names a payload shows for THIS case. When every generator answer of the case is a hand-checked fixture, no model drafted it: the generator reads
+    'hand-checked (qa)' and `generator_prepared` is true, so no screen names a model for an answer no model gave. A case with no generator call yet, or with any recorded or live one, keeps the configured model."""
+    calls = DB.list_llm_calls(conn, case_id) if calls is None else calls
+    gens = [c for c in calls if c["role"] == "generator"]
+    prepared = bool(gens) and all(AU.is_prepared(c.get("recorded_from")) for c in gens)
+    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
+
+
 def narrative_view(conn, case_id, nar):
     """D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture."""
     if not nar or not isinstance(nar.get("generator"), dict):
diff --git a/app/backend/trace.py b/app/backend/trace.py
index 228c714..c8fafae 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -146,7 +146,7 @@ class _Cx:
         self.events = {}
         for e in DB.list_events(conn, case_id):
             self.events.setdefault(e["item_id"], []).append(e)
-        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
+        self.models = present.models_for(conn, case_id, {"generator": J.generator_model(), "judge": J.judge_model()}, calls)      # T-177 r2: a prepared case names no drafting model
         self.ran = self.case.get("run_started_at") is not None
         self.running = self.case["status"] == "running"
 
@@ -172,6 +172,7 @@ def _span(cx, rid, start, end, text):
 
 PREPARED_LABEL = "Prepared answer, standing in for the AI draft"
 PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
+CASE_PREPARED_LABEL = "Prepared summaries and quotes for each record, standing in for the AI draft"
 
 
 def _llm_evidence(cx, role, model, prompt_version, call):
@@ -1066,16 +1067,19 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     missing = [r["id"] for r in firsts if r["id"] not in have]
     ecounts = {"records_to_draft": len(firsts), "entries": len(ents), "rejected": sum(1 for e in ents if e["state"] == "rejected"), "records_without_entry": len(missing),
                **({"in_tray": len(failed_ents)} if failed_ents else {})}
+    prep = bool(cx.models.get("generator_prepared"))      # T-177 r2 / D-065: the case's answers are hand-checked fixtures, so the step must not say an AI drafted them
+    xlabel = CASE_PREPARED_LABEL if prep else "AI drafts a summary and a quote for each record"
+    xev = {"evidence": {"model": {"id": present.PREPARED_MODEL, "role": "generator", "independent_of_generator": None, "prepared": True}}} if prep else {}
     if not cx.ran:
-        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PENDING, "The AI run has not started.", rule="row 4", counts=ecounts, next_action=na("RERUN")))
+        st.append(step("extract", xlabel, "llm", PENDING, "The prepared answers have not been loaded yet." if prep else "The AI run has not started.", rule="row 4", counts=ecounts, next_action=na("RERUN"), **xev))
     elif missing:
         trimmed = {r for x in failed_ents if (x.get("ladder") or {}).get("failure") == "SUMMARY_NOT_IN_QUOTE" for r in (x["record_ids"] or [])}
         why_code = "SUMMARY_NOT_IN_QUOTE" if set(missing) <= trimmed else "LLM_FAILED_AFTER_RETRIES"      # D-054: say so when code removed the whole summary
-        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no AI-made entry. "
-                       + reason_text(why_code), reason=why_code, rule="row 4", evidence={"values": {"record_ids": missing}}, counts=ecounts,
+        st.append(step("extract", xlabel, "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no {'prepared' if prep else 'AI-made'} entry. "
+                       + reason_text(why_code), reason=why_code, rule="row 4", evidence=({"model": xev["evidence"]["model"], "values": {"record_ids": missing}} if prep else {"values": {"record_ids": missing}}), counts=ecounts,
                        next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": missing[0]})))
     else:
-        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PASS, f"The AI drafted an entry for all {len(firsts)} records.", rule="row 4", counts=ecounts))
+        st.append(step("extract", xlabel, "llm", PASS, (f"The prepared answers (hand-checked by the team for the demo) cover all {len(firsts)} records." if prep else f"The AI drafted an entry for all {len(firsts)} records."), rule="row 4", counts=ecounts, **xev))
     # 5 grounding
     rej = [(k, x) for k, x in allitems if x["state"] == "rejected"]
     codes = {}
@@ -1094,23 +1098,24 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     else:
         st.append(step("grounding", "Every quote and amount is in the record", "code", PASS, f"All {len(allitems)} items cite text that is in the record, character for character.", rule="row 4", counts=gcounts))
     # 6 judges
+    jlabel = "Second AI check on every prepared item" if prep else "Second AI check on every AI-made item"      # T-177 r2: the items are the team's prepared answers
     t = jr["totals"]
     jcounts = dict(t)
     objections = t["unsupported"] + t["unsure"]
     if not rows_any(jr) and not cx.ran:
-        st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, "The second check has not run yet.", rule="row 4", counts=jcounts, next_action=na("RERUN")))
+        st.append(step("judges", jlabel, "llm", PENDING, "The second check has not run yet.", rule="row 4", counts=jcounts, next_action=na("RERUN")))
     elif t["unavailable"]:
         msg = f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. "
         if cx.running:
-            st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
+            st.append(step("judges", jlabel, "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
         else:
-            st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
+            st.append(step("judges", jlabel, "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
                            reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
     elif objections:
-        st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, f"The second check questioned {objections} of {t['items_judged']} items; they are marked for review.",
+        st.append(step("judges", jlabel, "llm", FAIL, f"The second check questioned {objections} of {t['items_judged']} items; they are marked for review.",
                        reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
     else:
-        st.append(step("judges", "Second AI check on every AI-made item", "llm", PASS, f"The second check agreed with all {t['items_judged']} items it checked.", rule="row 4", counts=jcounts))
+        st.append(step("judges", jlabel, "llm", PASS, f"The second check agreed with all {t['items_judged']} items it checked.", rule="row 4", counts=jcounts))
     # 7 flags
     fc = {"total": len(flgs), "by_type": _count_by(flgs, "type"), "by_origin": _count_by(flgs, "origin")}
     if any(f["category"] == "analysis_incomplete" for f in flgs):
diff --git a/app/frontend/app.js b/app/frontend/app.js
index 9da57cd..294645b 100644
--- a/app/frontend/app.js
+++ b/app/frontend/app.js
@@ -13,7 +13,7 @@
     // D-065: say whose answers the demo replays. Prepared (curated) answers are the team's, never the model's; recorded ones are real model answers.
     const prepared = demo && h.answers === "prepared";
     badge.textContent = prepared ? "Demo: sample answers prepared by our team" : demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
-    badge.title = prepared ? "The AI's own answers on these cases are in the evaluation report."
+    badge.title = prepared ? "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."     // T-177 r2: says only what is true
       : demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
     badge.hidden = !(demo || mock);
     const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
diff --git a/app/frontend/audit.js b/app/frontend/audit.js
index ad3468e..c2b5feb 100644
--- a/app/frontend/audit.js
+++ b/app/frontend/audit.js
@@ -21,9 +21,9 @@
     const rf = c.prepared ? " (prepared answer, not model output)" : c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
     return el("li", { class: "au-call", "data-testid": "audit-call" },
       el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.prepared ? el("span", { class: "rv-chip", "data-testid": "audit-prepared" }, "Prepared answer") : null, c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
-      el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prompt_version), kv("hash", c.prompt_sha256 ? String(c.prompt_sha256).slice(0, 12) : null),
+      el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prepared ? null : c.prompt_version), kv("hash", c.prepared || !c.prompt_sha256 ? null : String(c.prompt_sha256).slice(0, 12)),      // D-065: no prompt made a prepared answer
         kv("latency", c.latency_ms != null ? c.latency_ms + " ms" : null), kv("attempt", c.attempt), kv("tokens", c.tokens_in != null ? c.tokens_in + " in / " + c.tokens_out + " out" : null), kv("cost", c.cost_usd != null ? "$" + c.cost_usd : null)),
-      pre("System prompt (local mode)", c.system_text), pre("Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
+      pre(c.prepared ? "System prompt (not sent: prepared answer)" : "System prompt (local mode)", c.system_text), pre(c.prepared ? "Record text (not sent: prepared answer)" : "Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
   }
   function eventRow(e, confirmed) {   // a flagged charge's accept names the flag she confirmed (the event's own `confirm` when the server sends it)
     const named = e.confirm ? "confirmed " + (e.confirm.name || e.confirm.flag) : confirmed;
diff --git a/app/frontend/judges.js b/app/frontend/judges.js
index 9c5e1e3..532afc0 100644
--- a/app/frontend/judges.js
+++ b/app/frontend/judges.js
@@ -160,13 +160,16 @@
     det.open = wasOpen; toggle.textContent = det.open ? "Hide" : "Show";
     det.addEventListener("toggle", () => { wasOpen = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
     root.append(det);
+    const prepared = !!(d && d.models && d.models.generator_prepared);      // D-065: a prepared (hand-checked) demo answer was not drafted by a model; nothing here may say it was
     det.append(el("p", { class: "rv-help", "data-testid": "judge-label" }, el("strong", {}, "AI quality checks. "),
-      "This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review."));
+      (prepared ? "This shows how a second AI model checked the answers our team prepared for this demo. " : "This shows how a second AI model checked the first AI's drafts. ") + "It is not a verdict on the case, the care or the claim, and it does not replace your review."));
     if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
     const t = d.totals || {}, m = d.models || {}, items = byItem(d);
-    det.append(el("p", { class: "zj-models", "data-testid": "judge-model-line" },
-      "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
-      d.independent_models ? " (a different model, so it does not grade its own work)." : " (the same model: this check is weaker, read more closely)."));
+    det.append(prepared
+      ? el("p", { class: "zj-models", "data-testid": "judge-model-line" }, "Prepared by our team (not by an AI model), checked by ", el("strong", {}, m.judge || "unknown"), ".")
+      : el("p", { class: "zj-models", "data-testid": "judge-model-line" },
+        "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
+        d.independent_models ? " (a different model, so it does not grade its own work)." : " (the same model: this check is weaker, read more closely)."));
     det.append(el("ul", { class: "zj-tiles", "data-testid": "judge-totals", "aria-label": "AI check totals" },
       tile(t.items_judged || 0, "items checked by AI"), tile(t.supported || 0, "agreed with the draft"), tile(t.unsupported || 0, "AI objected"),
       tile(t.unsure || 0, "could not decide"), tile(t.unavailable || 0, "unavailable"), tile(t.human_overrides || 0, "you accepted despite an objection")));
diff --git a/app/frontend/stepper.js b/app/frontend/stepper.js
index 26e1e50..328b3f7 100644
--- a/app/frontend/stepper.js
+++ b/app/frontend/stepper.js
@@ -382,7 +382,8 @@
     const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), String(v)));
     tech.push(kv("reason code", st.reason_code), kv("rule", st.rule), kv("judge reason code", ev.judge_reason_code && ev.judge_reason_code !== "NONE" ? ev.judge_reason_code : null));
     if (m) tech.push(kv("model", m.id), kv("role", m.role), kv("independent of the drafting model", m.independent_of_generator == null ? null : m.independent_of_generator ? "yes" : "no"));
-    tech.push(kv("prompt", ev.prompt_version), kv("prompt hash", ev.prompt_sha256 && String(ev.prompt_sha256).slice(0, 12)), kv("call", ev.call_id), kv("backend", ev.backend),
+    const prep = !!(m && m.prepared);      // D-065: no prompt made a prepared answer, so none is shown
+    tech.push(prep ? null : kv("prompt", ev.prompt_version), prep ? null : kv("prompt hash", ev.prompt_sha256 && String(ev.prompt_sha256).slice(0, 12)), kv("call", ev.call_id), kv("backend", ev.backend),
       kv("recorded from", ev.recorded_from && ev.recorded_from.backend), kv("latency", ev.latency_ms != null ? ev.latency_ms + " ms" : null), kv("parsed", ev.parsed_ok == null ? null : ev.parsed_ok ? "yes" : "no"));
     const techNodes = tech.filter(Boolean);
     if (techNodes.length || ev.response_raw)
diff --git a/app/frontend/timeline.js b/app/frontend/timeline.js
index 6afc479..be84180 100644
--- a/app/frontend/timeline.js
+++ b/app/frontend/timeline.js
@@ -268,7 +268,7 @@
         el("details", { class: "zs-more" }, el("summary", {}, "Recorded ladder (raw state and checks)"), el("dl", { class: "kv", "data-testid": "why-ladder" },
           el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
           el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
-          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
+          lad.generator ? [el("dt", {}, lad.generator.prepared ? "Prepared by" : "Drafted by"), el("dd", { "data-testid": "why-generator" }, lad.generator.prepared ? String(lad.generator.model) : `${lad.generator.model} · ${lad.generator.prompt_version}`),   // D-065: no prompt made a prepared answer
             el("dt", {}, lad.generator.prepared ? "Prepared answer" : "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
           el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
           el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)"))),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:56.319Z

The diff matches the card's stated changes. Next I'll read the two test files, the e2e conftest, and the fixture backend to see how ports and fixtures are set up.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:56.790Z

**tool call — Bash**
````
{
 "command": "cat tests/e2e/test_demo_provenance.py && echo \"=====CONFTEST=====\" && git show HEAD:tests/e2e/conftest.py | head -150",
 "description": "Read the e2e provenance test and conftest"
}
````

### User / tool · 2026-11-02T21:04:56.884Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:58.141Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/e2e/test_demo_provenance.py | sed -n '1,200p'",
 "description": "Read the e2e provenance test from HEAD in chunks"
}
````

### User / tool · 2026-11-02T21:04:58.238Z

**tool result**
````
"""T-177 / D-065 (GATE-M3 product-manager blocker): the demo never shows a hand-checked (curated) answer as the AI's.
Acceptance test (the PM's), curated set (the default private server, FIXTURE_SET=curated): no element names 'AI draft' or 'recorded AI answers' for a curated item; the badge says the answers were
prepared by the team and its tooltip says the team prepared them and a second AI model checked them; /items/e1/trace's generator step is not claude-sonnet-5-5 and names a prepared answer; /audit rows for the generator carry
model 'hand-checked (qa)'. Recorded set (a second private server, no FIXTURE_SET): the labels say AI and the model ids are real.
New test ids (declared in tests/e2e/conftest.py, 'T-177'): tag-prepared, tag-ai-draft, audit-prepared."""
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest
from playwright.sync_api import expect
from tests.e2e import conftest as _C
from tests.e2e.conftest import api, open_case, reveal, ROOT, BASE

def _classic():
    return _C.BASE[len(getattr(_C, "SERVER", _C.BASE)):]      # "/classic" once the old screen moved there (D-068), "" before; a private server is opened at base + CLASSIC
PREPARED = "hand-checked (qa)"
WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
TOOLTIP = "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."      # T-177 r2 F2: points at nothing that is not there


def _ready(call, tok):
    for _ in range(300):
        s = call("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def curated_case():
    st, c = api("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(api, tok)
    yield tok
    api("DELETE", f"/api/cases/{tok}")


@pytest.fixture(scope="module")
def recorded_server():
    """A private app on its own port with the recorded (real model answers) fixture set: FIXTURE_SET unset."""
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-rec-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", ZLAYT_DB=os.path.join(tmp, "rec.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None); env.pop("FIXTURE_SET", None); env.pop("LLM_FIXTURE_DIR", None); env.pop("ENABLE_LIVE", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    for _ in range(80):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            assert proc.poll() is None, "the recorded-set server exited"
            time.sleep(.5)
    else:
        proc.kill(); pytest.fail("the recorded-set server did not start")

    def call(method, path, body=None):
        req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    yield base, call
    proc.terminate()
    try: proc.wait(timeout=10)
    except Exception: proc.kill()
    log.close()


def _open_why(page, n):
    reveal(page.get_by_test_id(f"entry-{n}").get_by_test_id("entry-why")).click()
    page.get_by_test_id("item-stepper").wait_for()
    return page.get_by_test_id("item-stepper")


# ---- the PM's acceptance test: API half (curated)
def test_curated_trace_and_audit_say_prepared(curated_case):
    tok = curated_case
    tr = api("GET", f"/api/cases/{tok}/items/e1/trace")[1]
    gen = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert gen["evidence"]["model"]["id"] != "claude-sonnet-5-5" and gen["evidence"]["model"]["id"] == PREPARED and gen["evidence"]["model"]["prepared"] is True
    assert gen["why"] == WHY and "prepared answer" in gen["why"].lower()
    audit = api("GET", f"/api/cases/{tok}/audit")[1]["calls"]
    gens = [c for c in audit if c["role"] == "generator"]
    assert gens and all(c["model"] == PREPARED and c["prepared"] is True for c in gens), [(c["step"], c["model"]) for c in gens]
    assert not any(c["model"] == "claude-sonnet-5-5" for c in gens)
    item = api("GET", f"/api/cases/{tok}/items/e1")[1]["item"]
    assert item["prepared"] is True and item["ladder"]["generator"]["model"] == PREPARED
    assert api("GET", "/api/health")[1]["answers"] == "prepared"


# ---- the PM's acceptance test: page half (curated)
def test_curated_page_never_calls_a_prepared_answer_ai(page, curated_case):
    open_case(page, curated_case)
    badge = page.locator("#badge")
    expect(badge).to_have_text("Demo: sample answers prepared by our team")
    assert badge.get_attribute("title") == TOOLTIP
    entries = page.locator("[data-testid^=entry-][data-entry-id]")
    n = entries.count(); assert n >= 9
    assert page.get_by_test_id("tag-prepared").count() == n and page.get_by_test_id("tag-ai-draft").count() == 0
    assert page.get_by_test_id("tag-prepared").first.inner_text() == "Prepared answer"
    text = page.evaluate("document.body.innerText")
    assert "AI draft" not in text and "recorded AI answers" not in text, re.findall(r".{20}(?:AI draft|recorded AI answers).{20}", text)
    assert page.locator("[title*='Drafted by AI'], [aria-label*='AI draft']").count() == 0
    assert "drafted by AI" not in page.locator("#banner-ai").inner_text() and "prepared by our team" in page.locator("#banner-ai").inner_text()
    st = _open_why(page, 1)
    gen = st.get_by_test_id("step").first
    assert gen.get_by_test_id("step-kind").inner_text() == "Prepared answer"
    body = st.inner_text()
    assert "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft" in body
    assert "AI draft" not in body.replace("standing in for the AI draft", "") and "claude-sonnet-5-5" not in body and "The AI read this record" not in body


def test_curated_audit_drawer_marks_the_prepared_rows(page, curated_case):
    open_case(page, curated_case)
    reveal(page.get_by_test_id("entry-1").get_by_test_id("btn-audit")).click()
    page.get_by_test_id("audit-drawer").wait_for()
    drawer = page.get_by_test_id("audit-drawer")
    expect(drawer.get_by_test_id("audit-prepared").first).to_have_text("Prepared answer")
    assert PREPARED in drawer.inner_text() and "claude-sonnet-5-5" not in drawer.inner_text()


# ---- recorded set: the labels say AI
def test_recorded_set_labels_say_ai(pw, recorded_server):
    base, call = recorded_server
    st, c = call("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); tok = c["token"]
    assert call("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(call, tok)
    assert call("GET", "/api/health")[1]["answers"] == "recorded"
    tr = call("GET", f"/api/cases/{tok}/items/e1/trace")[1]
    gen = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert gen["evidence"]["model"]["id"] == "claude-sonnet-5-5" and gen["evidence"]["model"]["prepared"] is False
    assert gen["why"] == "The AI read this record and proposed a one-line summary and a quote."
    calls = call("GET", f"/api/cases/{tok}/audit")[1]["calls"]
    assert calls and not any(x["prepared"] or x["model"] == PREPARED for x in calls)
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    try:
        pg.goto(f"{base}{_classic()}/#/case/{tok}"); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        expect(pg.locator("#badge")).to_have_text("Demo: recorded AI answers")
        assert pg.get_by_test_id("tag-prepared").count() == 0 and pg.get_by_test_id("tag-ai-draft").count() >= 1
        assert "prepared by our team" not in pg.evaluate("document.body.innerText")
        st_ = _open_why(pg, 1)
        assert st_.get_by_test_id("step").first.get_by_test_id("step-kind").inner_text() == "AI draft"
    finally:
        b.close()


# ---- T-177 round 2 (staff-engineer F1/F2/F3/F5): every surface, curated and recorded
def _scan(page):
    """Everything the page holds for a reader: all text (open or closed panels) and every title / aria-label, as one string."""
    return page.evaluate("""() => { const out = [document.documentElement.textContent];
      document.querySelectorAll('[title],[aria-label]').forEach(e => out.push(e.getAttribute('title') || '', e.getAttribute('aria-label') || ''));
      return out.join(' | '); }""")


def _open_judges(page):
    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
    if not jp.locator("details.zj-det").evaluate("d => d.open"):
        jp.get_by_test_id("judge-summary").click()
    jp.get_by_test_id("judge-totals").wait_for()
    return jp


def test_curated_judge_panel_does_not_name_a_drafting_model(page, curated_case):
    open_case(page, curated_case)
    jp = _open_judges(page)
    line = jp.get_by_test_id("judge-model-line").inner_text()
    assert "claude-sonnet-5-5" not in line and "Drafted by" not in line, line
    assert "prepared by our team" in line.lower() and "not by an AI model" in line and "claude-haiku-5-5" in line, line
    label = jp.get_by_test_id("judge-label").inner_text()
    assert "first AI" not in label and "AI's drafts" not in label and "answers our team prepared" in label and "second AI model" in label, label
    assert "not a verdict" in label


def test_curated_every_surface_is_free_of_the_drafting_model(page, curated_case):
    """The judge panel, the Why dialog (stepper and recorded ladder), the audit drawer, tooltips and the banner, all open at once: no 'claude-sonnet', no 'Drafted by AI', no 'AI draft'."""
    open_case(page, curated_case)
    _open_judges(page)
    _open_why(page, 1)
    ladder = page.get_by_test_id("why-ladder")
    assert ladder.count() == 1
    assert ladder.get_by_test_id("why-generator").text_content() == PREPARED, ladder.get_by_test_id("why-generator").text_content()   # no prompt version: no prompt made it
    dts = ladder.locator("dt").all_text_contents()
    assert "Drafted by" not in dts and "Prepared by" in dts and "AI draft" not in dts and "Prepared answer" in dts
    page.keyboard.press("Escape")
    reveal(page.get_by_test_id("entry-1").get_by_test_id("btn-audit")).click()
    drawer = page.get_by_test_id("audit-drawer"); drawer.wait_for()
    drawer.get_by_test_id("audit-prepared").first.wait_for()
    gen_rows = drawer.get_by_test_id("audit-call").filter(has=page.get_by_test_id("audit-prepared"))
    assert gen_rows.count() >= 1
    for i in range(gen_rows.count()):
        t = gen_rows.nth(i).inner_text()
        assert "extract_v1" not in t and "hash" not in t and "sent to the model" not in t, t      # no prompt made a prepared answer
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:04:59.383Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/e2e/test_demo_provenance.py | sed -n '200,400p'",
 "description": "Read the rest of the e2e provenance test"
}
````

### User / tool · 2026-11-02T21:04:59.474Z

**tool result**
````
        assert "extract_v1" not in t and "hash" not in t and "sent to the model" not in t, t      # no prompt made a prepared answer
    text = _scan(page).replace("standing in for the AI draft", "")      # the one allowed phrase: it says the prepared answer is NOT the AI's
    for bad in ("claude-sonnet", "Drafted by AI", "drafted by AI", "AI draft", "recorded AI answers", "The AI's own answers"):
        assert bad not in text, (bad, re.findall(r".{30}" + re.escape(bad) + ".{30}", text)[:3])


def test_recorded_judge_panel_still_names_the_drafting_model(pw, recorded_server):
    base, call = recorded_server
    st, c = call("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); tok = c["token"]
    assert call("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(call, tok)
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    try:
        pg.goto(f"{base}{_classic()}/#/case/{tok}"); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        jp = _open_judges(pg)
        line = jp.get_by_test_id("judge-model-line").inner_text()
        assert "Drafted by claude-sonnet-5-5" in line and "claude-haiku-5-5" in line and "prepared" not in line.lower(), line
        assert "first AI's drafts" in jp.get_by_test_id("judge-label").inner_text()
        _open_why(pg, 1)
        ladder = pg.get_by_test_id("why-ladder")
        gt = ladder.get_by_test_id("why-generator").text_content()      # the Recorded ladder is a closed <details>: read its text, not its rendering
        assert "claude-sonnet-5-5" in gt and "extract_v1" in gt, gt
        dts = ladder.locator("dt").all_text_contents()
        assert "Drafted by" in dts and "AI draft" in dts
        assert "second AI model" in pg.locator("#banner-ai").inner_text() or "drafted by AI" in pg.locator("#banner-ai").inner_text()
    finally:
        b.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:01.995Z

The e2e tests spin up private servers, but the default `BASE` may point at a shared port. I'll read the conftest to see how `BASE`, `E2E_REQUIRE_DB`, and the curated server are chosen.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:02.648Z

**tool call — Bash**
````
{
 "command": "git show HEAD:tests/e2e/conftest.py | grep -n \"BASE\\|SERVER\\|E2E_REQUIRE_DB\\|FIXTURE_SET\\|7860\\|PORT\\|def pw\\|def page\\|def api\\|CLASSIC\\|skip\" | head -80",
 "description": "Grep conftest for base URL, DB requirement, and fixture settings"
}
````

### User / tool · 2026-11-02T21:05:02.747Z

**tool result**
````
1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
2:Every spec is skipped with a clear reason when the server is not up (M3 not built yet).
11:  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
17:  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
22:T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
50:  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
76:T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
77:  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
98:  T-174 (MVP finish, tests/e2e/test_mvp_finish.py): section-nav (a sticky bar under the case header with nav-overview, nav-timeline, nav-flags, nav-charges, nav-export; each shows what is still open in its section and the current one carries aria-current=location), btn-back-to-review (the first control in the Export view; closes Export and returns focus to the row she left), btn-error-action (the one action button inside an input error box `error`: Try again, Use the sample case, Edit the text, Choose a .txt file), charge-detail (the code's detail of a not-counted amount, inside the row's More panel). The skip link and n go to case.next_action.item_id: the case overview box carries it as data-do-first-item (the item named in do-first-item). cases-status-error and cases-status-retry (T-175 r2: the message and the Try again button on a case-list row with status_error; no counts, bar or Can export on it), case-switcher (the 'Add a synthetic case' card under the case list; shown on the overview only).
106:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
117:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
118:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
119:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
120:    global BASE
121:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
126:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
133:        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
141:        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)
155:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
165:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
166:    one fails instead of skipping, so a run can say '0 skipped'."""
169:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
170:        if os.environ.get("E2E_REQUIRE_DB") == "1":
172:        pytest.skip(msg)
177:        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
185:    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
188:            it.add_marker(skip)
190:def api(method, path, body=None):
191:    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
234:    return BASE
252:def pw():
253:    sync = pytest.importorskip("playwright.sync_api")
258:def page(pw):
268:    page.goto(f"{BASE}/#/case/{tok}")
423:                    st.update(status="skipped", reason_code="JUDGE_UNAVAILABLE", why="The second AI check never gave an answer for this item.", next_action=self._na(d["item_id"]))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:15.523Z

The default e2e run starts its own private server on a free loopback port with the curated set, so I'll let the conftest pick my port and leave 7860 alone. Next I'll make the `git archive HEAD` copy under my evidence directory and record the sha it came from.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:16.566Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && mkdir -p $EV/archive && git archive --format=tar HEAD | tar -x -C $EV/archive && git rev-parse HEAD > $EV/archive-source-sha.txt && cat $EV/archive-source-sha.txt && ls $EV/archive | head -50 && echo \"--- file count ---\" && find $EV/archive -type f | wc -l && echo \"--- listeners on 7860 (read only) ---\" && (lsof -iTCP:7860 -sTCP:LISTEN -n -P || echo \"no listener on 7860\")",
 "description": "Extract git archive of HEAD into evidence dir and check port 7860"
}
````

### User / tool · 2026-11-02T21:05:17.294Z

**tool result**
````
4671eee820334400619dafc00cf11a53e0cb30de
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
--- file count ---
    2432
--- listeners on 7860 (read only) ---
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  86899 arsis    9u  IPv4 0x89944c6bbeb1c380      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:18.858Z

The HEAD sha I just recorded (4671eee) differs from the ac678bc I read a few minutes ago, so HEAD moved during this review. I'll check the log and find what changed.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:19.651Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 6 && echo \"--- show HEAD stat ---\" && git show --stat --format='%h %an %s' HEAD | head -30 && echo \"--- diff ac678bc..HEAD on app tests evals ---\" && git diff --stat ac678bc HEAD -- app tests evals memory/contracts | tail -20",
 "description": "Recheck git log after HEAD moved and diff since prior HEAD"
}
````

### User / tool · 2026-11-02T21:05:19.795Z

**tool result**
````
4671eee test(backend): T-183 M4 hardening check; plain message when a record-count limit is hit
d07bf9d docs(orchestrator): D-065 tooltip wording (T-177 r2)
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs
4fcf9cd fix(frontend): T-177 r2 honest provenance on every surface: prepared items name no drafting model (judge panel, models in health/case/judges/export, case trace, tooltip, banner, audit and ladder rows)
964505b docs(qa): T-045 r3: sensors record names the commit for the unit count (5782 at b824a6c)
b01382f feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)
--- show HEAD stat ---
4671eee Chris Borsheim test(backend): T-183 M4 hardening check; plain message when a record-count limit is hit

 app/backend/api.py                |  15 ++-
 tests/unit/test_t183_hardening.py | 236 ++++++++++++++++++++++++++++++++++++++
 2 files changed, 248 insertions(+), 3 deletions(-)
--- diff ac678bc..HEAD on app tests evals ---
 app/backend/api.py                |  15 ++-
 tests/unit/test_t183_hardening.py | 236 ++++++++++++++++++++++++++++++++++++++
 2 files changed, 248 insertions(+), 3 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:23.416Z

HEAD is now 4671eee. It includes d07bf9d, which changes D-065 wording, and a T-183 edit to `app/backend/api.py`. I'll read both diffs and the committed D-065 text, since the tooltip check has to match what is committed.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:23.908Z

**tool call — Bash**
````
{
 "command": "echo \"=== d07bf9d ===\" && git show d07bf9d | head -60 && echo \"=== 4671eee api.py ===\" && git show 4671eee -- app/backend/api.py",
 "description": "Show D-065 wording commit and T-183 api.py diff"
}
````

### User / tool · 2026-11-02T21:05:24.022Z

**tool result**
````
=== d07bf9d ===
commit d07bf9dd12b8fe46b9d29ed138ea2c6afb639e3d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:04:53 2026 -0600

    docs(orchestrator): D-065 tooltip wording (T-177 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/memory/ORCHESTRATOR_DECISIONS.md b/memory/ORCHESTRATOR_DECISIONS.md
index d540de4..a1d7120 100644
--- a/memory/ORCHESTRATOR_DECISIONS.md
+++ b/memory/ORCHESTRATOR_DECISIONS.md
@@ -70,7 +70,7 @@ Questions that are really Chris's are in submission/NEEDS_CHRIS.md with the assu
 | D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the total. Charge sources are positively identified: only documents with a billing header (itemized statement, ledger, invoice, UB-04, CMS-1500) can yield a `charge`; clinical notes and discharge summaries yield a charge only from an encounter line, and never once the case holds an itemized bill from the same provider (amended at implementation: a literal ban zeroed the sample, whose charges are stated in visit notes); insurer and unknown documents never can. CPT/HCPCS codes are normalized ('CPT 99213' = '99213') before duplicate matching. Residual: a summary row dressed as a service line can still be accepted by a careless reviewer; it is cited and individually accepted, and listed as accepted debt. | An adversary can always word a ledger past a classifier; the honest claim is a sum of human-accepted, cited lines. | T-140 claims-adjuster r3 |
 | D-063 | Priority switch (Chris, 2026-11-02): finish a polished MVP. Only P0 cards and UX/UI work proceed; every other non-P0 card is held (blocked with a note) until the MVP is done. In-flight P1 cards finish their current round but get no further rounds unless they block the UI. New review rounds on held areas are not opened; residuals go to SCOPE_CUTS. The M2 re-gate runs as soon as the P0 blockers (T-139, T-155) close. | Chris: "<Chris's message omitted>." | Chris chat |
 | D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this charge", a named confirm ("I checked this is a separate charge for a service"), recorded in the audit trail; it then sums like any accepted charge. Amends D-059 item on reclassify: (b) is promotable with the confirm, (a) never. | The default-deny rule undercounts real ledger lines (lib11 $3,260 vs $6,000); the paralegal must see why and be able to fix it herself, without reopening the overcount paths. | GATE-M2 r2 paralegal |
-| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "The AI's own answers on these cases are in the evaluation report." A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
+| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
 | D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
 | D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
 | D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
=== 4671eee api.py ===
commit 4671eee820334400619dafc00cf11a53e0cb30de
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:05:03 2026 -0600

    test(backend): T-183 M4 hardening check; plain message when a record-count limit is hit
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 2c031c2..41830af 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -16,7 +16,7 @@ import traceback
 
 from fastapi import FastAPI, Request
 from fastapi.exceptions import RequestValidationError
-from fastapi.responses import JSONResponse, Response
+from fastapi.responses import JSONResponse, RedirectResponse, Response
 from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from starlette.concurrency import run_in_threadpool
@@ -363,7 +363,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                 DB.delete_case(c, cid)
                 if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
-                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, *language.api_fields(e)) from None
+                    msg, detail = language.api_fields(e)
+                    if not msg:             # T-183: a limit hit during splitting (too many records) said "input too large" (the bare code); say it as a sentence
+                        msg = "Input is too large." if e.code == "input_too_large" else "Input is empty." if e.code == "bad_request" else "The input could not be read."
+                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, msg, detail) from None
                 log.error("create failed %s", type(e).__name__)
                 raise ApiError(500, "internal", "Something went wrong.") from None
             return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
@@ -669,5 +672,11 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
     if sd.is_dir():
         from fastapi.staticfiles import StaticFiles
-        app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
+        guided = sd / "guided"
+        if (guided / "index.html").is_file():                                           # D-068: the guided app is the front door; the old screen stays reachable at /classic
+            app.add_api_route("/classic", lambda: RedirectResponse("/classic/"), include_in_schema=False)       # the mount only answers /classic/ ; /classic would fall to the guided mount's 404
+            app.mount("/classic", StaticFiles(directory=str(sd), html=True), name="classic")
+            app.mount("/", StaticFiles(directory=str(guided), html=True), name="frontend")
+        else:
+            app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
     return app
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:24.276Z

**tool call — Bash**
````
{
 "command": "git show HEAD:memory/ORCHESTRATOR_DECISIONS.md | grep -n \"^| D-065\" | cut -c1-900",
 "description": "Read committed D-065 row at HEAD"
}
````

### User / tool · 2026-11-02T21:05:24.370Z

**tool result**
````
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | G
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:29.052Z

The committed D-065 text now carries the amended tooltip, and the T-183 commit only touches the static mount and an error message. Before the test runs, I'll check whether the guided app exists in HEAD, read the unit test file, and compare the tooltip string with D-065 byte for byte.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:30.346Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && echo \"--- guided dir in HEAD ---\" && (git ls-tree -r --name-only HEAD app/frontend | grep -i guided | head -5 || true) && echo \"--- tooltip in archive app.js ---\" && grep -n \"badge.title\" $EV/archive/app/frontend/app.js && echo \"--- D-065 tooltip string from HEAD memory ---\" && git show HEAD:memory/ORCHESTRATOR_DECISIONS.md | grep -o 'tooltip: \"[^\"]*\"' | head -3 && echo \"--- banner in archive api.py ---\" && grep -n \"PREPARED_BANNER =\\|AI_BANNER =\" $EV/archive/app/backend/api.py && echo \"--- unit test file ---\" && cat $EV/archive/tests/unit/test_prepared_provenance.py",
 "description": "Check guided dir, tooltip and banner strings, and unit test file"
}
````

### User / tool · 2026-11-02T21:05:30.484Z

**tool result**
````
--- guided dir in HEAD ---
--- tooltip in archive app.js ---
16:    badge.title = prepared ? "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."     // T-177 r2: says only what is true
--- D-065 tooltip string from HEAD memory ---
tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."
--- banner in archive api.py ---
36:AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
37:PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item"      # D-065
--- unit test file ---
"""T-177 / D-065 (GATE-M3 PM blocker): a curated (hand-checked) fixture answer is never presented as model output.
Provenance comes from the fixture's own `recorded_from`. Curated -> prepared: true, model 'hand-checked (qa)' in the item, the trace and the audit rows;
the trace's generator step says it is a prepared answer. Recorded (and live) answers keep their real model ids and their AI labels."""
import json
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

PREPARED_MODEL = "hand-checked (qa)"


def _client(tmp_path, monkeypatch, fixture_set):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    else:
        monkeypatch.delenv("FIXTURE_SET", raising=False)
    return TestClient(create_app(str(tmp_path / "p.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _run(c):
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture
def curated(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    return c, _run(c)


@pytest.fixture
def recorded(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, None)
    return c, _run(c)


def _generator_step(trace):
    return next(s for s in trace["steps"] if s["id"] == "extracted")


# ---- curated set
def test_curated_audit_rows_carry_the_prepared_model(curated):
    c, tok = curated
    calls = c.get(f"/api/cases/{tok}/audit").json()["calls"]
    gen = [x for x in calls if x["role"] == "generator"]
    assert len(gen) >= 9
    for x in gen:
        assert x["model"] == PREPARED_MODEL and x["prepared"] is True, x
    # D-056: judge answers are real recordings; they keep their real model id and are not prepared
    judges = [x for x in calls if x["role"] == "judge"]
    assert judges and all(x["prepared"] is False and x["model"] != PREPARED_MODEL for x in judges)


def test_curated_item_is_marked_prepared(curated):
    c, tok = curated
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"]
    for e in case["entries"]:
        assert e["prepared"] is True, e["id"]
        assert e["ladder"]["generator"]["model"] == PREPARED_MODEL and e["ladder"]["generator"]["prepared"] is True
    item = c.get(f"/api/cases/{tok}/items/e1").json()["item"]
    assert item["prepared"] is True and item["ladder"]["generator"]["model"] == PREPARED_MODEL


def test_curated_trace_generator_step_names_a_prepared_answer(curated):
    c, tok = curated
    st = _generator_step(c.get(f"/api/cases/{tok}/items/e1/trace").json())
    ev = st["evidence"]
    assert ev["model"]["id"] == PREPARED_MODEL and ev["model"]["id"] != "claude-sonnet-5-5" and ev["model"]["prepared"] is True
    assert st["why"] == "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
    assert "AI read this record" not in json.dumps(st) and "AI drafted" not in st["label"]


def test_curated_health_says_prepared_and_the_banner_does_not_claim_ai(curated):
    c, tok = curated
    h = c.get("/api/health").json()
    assert h["answers"] == "prepared" and "prepared by our team" in h["ai_banner"] and "drafted by AI" not in h["ai_banner"]
    # T-177 r2 F3: the banner names the second AI check that runs on the same items, and does not say "checked by code" alone
    assert "second AI model" in h["ai_banner"] and "checked by code;" not in h["ai_banner"]
    # the second check is still an AI check (a real recorded answer) and keeps its model id
    tr = c.get(f"/api/cases/{tok}/items/e1/trace").json()
    j = next(s for s in tr["steps"] if s["id"] == "judge_1")
    assert j["evidence"]["model"]["id"] != PREPARED_MODEL and not j["evidence"]["model"].get("prepared")


# ---- recorded set: labels stay AI
def test_recorded_set_keeps_ai_labels_and_model_ids(recorded):
    c, tok = recorded
    h = c.get("/api/health").json()
    assert h["answers"] == "recorded" and "drafted by AI" in h["ai_banner"]
    calls = c.get(f"/api/cases/{tok}/audit").json()["calls"]
    assert calls and all(x["prepared"] is False and x["model"] != PREPARED_MODEL for x in calls)
    assert any(x["model"] == "claude-sonnet-5-5" for x in calls)
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"] and all(e["prepared"] is False for e in case["entries"])
    e1 = case["entries"][0]
    assert e1["ladder"]["generator"]["model"] == "claude-sonnet-5-5" and e1["ladder"]["generator"].get("prepared") is False
    st = _generator_step(c.get(f"/api/cases/{tok}/items/{e1['id']}/trace").json())
    assert st["evidence"]["model"]["id"] == "claude-sonnet-5-5" and st["evidence"]["model"]["prepared"] is False
    assert st["why"] == "The AI read this record and proposed a one-line summary and a quote."


def test_live_backend_health_says_live(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    from app.backend import store
    monkeypatch.setattr(store, "live_enabled", lambda: True)
    assert c.get("/api/health").json()["answers"] == "live"


# ---- T-177 round 2 (staff-engineer F1): no payload names a model as the drafter of a prepared answer
def test_curated_models_never_name_a_drafting_model(curated):
    c, tok = curated
    h = c.get("/api/health").json()
    assert h["models"]["generator"] == PREPARED_MODEL and h["models"]["generator_prepared"] is True and h["models"]["judge"] == "claude-haiku-5-5"
    case = c.get(f"/api/cases/{tok}").json()
    assert case["models"]["generator"] == PREPARED_MODEL and case["models"]["generator_prepared"] is True and case["models"]["judge"] == "claude-haiku-5-5"
    j = c.get(f"/api/cases/{tok}/judges").json()
    assert j["models"]["generator"] == PREPARED_MODEL and j["models"]["generator_prepared"] is True and j["models"]["judge"] == "claude-haiku-5-5"
    assert j["independent_models"] is True and j["totals"]["items_judged"] > 0
    for path in (f"/api/cases/{tok}/judges", f"/api/cases/{tok}", f"/api/cases/{tok}/items/e1/trace", f"/api/cases/{tok}/audit", "/api/health"):
        body = json.dumps(c.get(path).json())
        assert '"generator": "claude-sonnet-5-5"' not in body and "generator_model\": \"claude-sonnet" not in body, path
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 200, r.text
    assert r.json()["provenance"]["generator_model"] == PREPARED_MODEL and r.json()["provenance"]["judge_model"] == "claude-haiku-5-5"


def test_curated_case_level_trace_does_not_say_an_ai_drafted(curated):
    c, tok = curated
    tr = c.get(f"/api/cases/{tok}/trace").json()
    ex = next(x for x in tr["steps"] if x["id"] == "extract")
    assert "AI drafts" not in ex["label"] and "AI drafted" not in ex["why"] and "prepared" in ex["label"].lower() and "prepared" in ex["why"].lower(), ex
    assert ex["evidence"]["model"]["id"] == PREPARED_MODEL and ex["evidence"]["model"]["prepared"] is True
    jd = next(x for x in tr["steps"] if x["id"] == "judges")
    assert "AI-made" not in jd["label"] and "Second AI check" in jd["label"]


def test_recorded_case_level_trace_keeps_the_ai_wording(recorded):
    c, tok = recorded
    ex = next(x for x in c.get(f"/api/cases/{tok}/trace").json()["steps"] if x["id"] == "extract")
    assert ex["label"] == "AI drafts a summary and a quote for each record" and ex["why"].startswith("The AI drafted an entry for all")
    assert not ex["evidence"]


def test_recorded_models_keep_the_drafting_model(recorded):
    c, tok = recorded
    j = c.get(f"/api/cases/{tok}/judges").json()
    assert j["models"]["generator"] == "claude-sonnet-5-5" and j["models"]["generator_prepared"] is False
    assert c.get(f"/api/cases/{tok}").json()["models"]["generator"] == "claude-sonnet-5-5"
    h = c.get("/api/health").json()
    assert h["models"]["generator"] == "claude-sonnet-5-5" and h["models"]["generator_prepared"] is False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:33.019Z

The guided app is not in HEAD, so the classic screen is the one under review. Next I'll run the unit file in the archive copy with the project venv, and capture the output.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:33.878Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/unit-prepared.out | tail -30",
 "description": "Run prepared-provenance unit tests in archive copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:05:38.112Z

**tool result**
````
..........                                                               [100%]
10 passed in 3.77s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:39.759Z

The unit file passes 10 of 10 in the archive copy. Next is the e2e file with `E2E_REQUIRE_DB=1`, leaving the base URL unset so the conftest starts its own private server on a free loopback port.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:40.700Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && env -u E2E_BASE_URL -u ZLAYT_DB E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v -p no:cacheprovider 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/e2e-provenance.out | tail -60",
 "description": "Run provenance e2e tests with DB required in archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:05:49.707Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 7 items

tests/e2e/test_demo_provenance.py::test_curated_trace_and_audit_say_prepared PASSED [ 14%]
tests/e2e/test_demo_provenance.py::test_curated_page_never_calls_a_prepared_answer_ai PASSED [ 28%]
tests/e2e/test_demo_provenance.py::test_curated_audit_drawer_marks_the_prepared_rows PASSED [ 42%]
tests/e2e/test_demo_provenance.py::test_recorded_set_labels_say_ai PASSED [ 57%]
tests/e2e/test_demo_provenance.py::test_curated_judge_panel_does_not_name_a_drafting_model PASSED [ 71%]
tests/e2e/test_demo_provenance.py::test_curated_every_surface_is_free_of_the_drafting_model PASSED [ 85%]
tests/e2e/test_demo_provenance.py::test_recorded_judge_panel_still_names_the_drafting_model PASSED [100%]

============================== 7 passed in 7.95s ===============================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:53.697Z

All 7 e2e tests pass with no skips. The tests check only what they assert, so next I'll grep the whole frontend and backend for drafting-model or "AI draft" wording that a prepared item could still reach.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:05:55.054Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && echo \"=== model-name literals and config model refs (app/) ===\" && grep -rn \"claude-sonnet\\|claude-haiku\\|GENERATOR_MODEL\\|generator_model()\\|judge_model()\" app/ --include=*.py --include=*.js --include=*.html | grep -v \"^app/llm/lexicon\" | cut -c1-260 && echo \"=== drafting wording (app/frontend and backend) ===\" && grep -rn \"AI draft\\|drafted by AI\\|Drafted by\\|AI-made\\|AI drafted\\|AI drafts\\|first AI\\|own answers\\|evaluation report\" app/frontend app/backend --include=*.js --include=*.py --include=*.html | cut -c1-260",
 "description": "Grep app for model-name literals and drafting wording"
}
````

### User / tool · 2026-11-02T21:05:55.163Z

**tool result**
````
=== model-name literals and config model refs (app/) ===
app/llm/audited.py:147:    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
app/llm/audited.py:148:    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}
app/frontend/mock_extra.js:21:        calls.push(Object.assign({ id: "c" + i * 2, role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", prompt_sha256: "9f2c0a77" + i, item_id: e.id, attempt: 1, latenc
app/frontend/mock_extra.js:23:        calls.push({ id: "c" + (i * 2 + 1), role: "judge", step: "judge_entries", backend: "fixture", model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", prompt_sha256: "77aa10c2" + i, item_id: e.id, attempt: 1, la
app/frontend/mock.js:72:      generator: { model: "claude-sonnet-5-5", prompt_version: "extract_v1", call_id: "c" + id, recorded_from: { backend: "claude-cli", model: "claude-sonnet-5-5", recorded_at: "2026-11-02T00:50:00Z" }, output: { summary: opts.summary, 
app/frontend/mock.js:74:      judge: { model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", call_id: "j" + id, verdict: opts.verdict },
app/frontend/mock.js:104:            code_checks: { amount_in_text: true, classified_by: rate ? "rule:per_unit" : "rule:charge_label" }, judge: { model: "claude-haiku-5-5", verdict: "agrees" }, human: { action: null } } });
app/frontend/mock.js:118:    const c = { token, name, status: "ingested", demo_mode: false, backend: "fixture", models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, records,
app/frontend/mock.js:146:        models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, limits: { max_chars: MAX_CHARS, max_records: 40 }, retention_hours: 24,
app/frontend/mock.js:181:          calls: [{ id: "c1", role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", attempt: 1, latency_ms: 5120, parsed_ok: !(it.state === "rejected"), verdict: null },
app/frontend/mock.js:182:            { id: "c2", role: "judge", step: "judge_entries", backend: "fixture", model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", attempt: 1, latency_ms: 2210, parsed_ok: true, verdict: it.ladder && it.ladder.judge 
app/backend/trace.py:149:        self.models = present.models_for(conn, case_id, {"generator": J.generator_model(), "judge": J.judge_model()}, calls)      # T-177 r2: a prepared case names no drafting model
app/backend/rejudge.py:84:        lad["judge"] = {**(lad.get("judge") or {}), "model": judges.judge_model(), "prompt_version": spanish.JUDGE_PROMPT if (jid == "j1" and lad.get("translation")) else trace.JUDGE_PROMPT[jid],
app/backend/flags.py:343:    f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
app/backend/narrative.py:94:    base["generator"] = {"model": judges.generator_model(), "prompt_version": prompt.name, "call_id": call_id}
app/backend/narrative.py:111:        item["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": jcall, "verdict": lad, "reason_code": jcode}
app/backend/review.py:468:    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
app/backend/review.py:688:              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
app/backend/generator.py:60:    e["ladder"] = {"item_id": e["id"], "generator": {"model": judges.generator_model(), "prompt_version": prompt.name,
app/backend/generator.py:256:        e["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(records_by_n[e["seq"]])), "call_id": call_id,
app/backend/pipeline.py:87:            flags[-1]["ladder"]["generator"] = {"model": judges.generator_model(), "prompt_version": "split_v1", "call_id": w.get("call_id")}
app/backend/pipeline.py:425:                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
app/backend/pipeline.py:682:            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}
app/backend/api.py:136:        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
app/backend/judges.py:12:DEFAULT_GENERATOR_MODEL = "claude-sonnet-5-5"
app/backend/judges.py:13:DEFAULT_JUDGE_MODEL = "claude-haiku-5-5"
app/backend/judges.py:16:def generator_model() -> str:
app/backend/judges.py:17:    return os.environ.get("GENERATOR_MODEL") or DEFAULT_GENERATOR_MODEL
app/backend/judges.py:20:def judge_model() -> str:
app/backend/judges.py:113:                         "model": judge_model(), "prompt_version": "judge_amount_class_v1"}
app/backend/reclassify.py:223:    return wording, {"judge": {"model": judges.judge_model(), "prompt_version": "judge_amount_class_v1", "call_id": call_id, "verdict": verdict,
=== drafting wording (app/frontend and backend) ===
app/frontend/stepper.js:41:    if (m && m.prepared) return "Prepared answer";         // D-065: a hand-checked demo answer is not an AI draft
app/frontend/stepper.js:42:    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
app/frontend/stepper.js:150:  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
app/frontend/stepper.js:152:  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
app/frontend/timeline.js:20:  // D-065: a hand-checked demo answer is a "Prepared answer", never an AI draft; recorded and live answers keep the AI label.
app/frontend/timeline.js:22:    ? el("span", { class: "tag", "data-testid": "tag-prepared", title: "Prepared by our team for this demo, standing in for the AI draft" }, "Prepared answer")
app/frontend/timeline.js:23:    : el("span", { class: "tag", "data-icon": "ai", "data-testid": "tag-ai-draft", title: "Drafted by AI" }, "draft");
app/frontend/timeline.js:271:          lad.generator ? [el("dt", {}, lad.generator.prepared ? "Prepared by" : "Drafted by"), el("dd", { "data-testid": "why-generator" }, lad.generator.prepared ? String(lad.generator.model) : `${lad.generator.model} · ${lad.ge
app/frontend/timeline.js:272:            el("dt", {}, lad.generator.prepared ? "Prepared answer" : "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null
app/frontend/dom.js:52:  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
app/frontend/dom.js:55:  // T-136 r3 (T-134 r4): the server's own `second_check_pending` (live, AI-made, no second-check answer, not a rate) is what the page reads. The inference below is only for a server
app/frontend/mock.js:147:        ai_banner: "Summaries and flags are drafted by AI and checked by code; you decide every item", sample_available: true });
app/frontend/judges.js:165:      (prepared ? "This shows how a second AI model checked the answers our team prepared for this demo. " : "This shows how a second AI model checked the first AI's drafts. ") + "It is not a verdict on the case, the care or the clai
app/frontend/judges.js:171:        "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
app/frontend/app.js:10:    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
app/backend/why.py:33:    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
app/backend/why.py:35:    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no AI-made entry. Read the record yourself or write the entry by hand.",
app/backend/trace.py:173:PREPARED_LABEL = "Prepared answer, standing in for the AI draft"
app/backend/trace.py:174:PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
app/backend/trace.py:175:CASE_PREPARED_LABEL = "Prepared summaries and quotes for each record, standing in for the AI draft"
app/backend/trace.py:296:    if gated:      # whose words: only the paralegal's own summary is "your wording"; an AI draft is "this summary"
app/backend/trace.py:392:        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
app/backend/trace.py:400:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
app/backend/trace.py:403:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
app/backend/trace.py:407:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL,
app/backend/trace.py:414:                st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
app/backend/trace.py:479:    if _code_check_gated(row):        # D-045(b), D-051: a failing code check blocks the export (AI-made or human wording; only the judge is exempt for human wording) and says what to do
app/backend/trace.py:518:    """Export blockers (D-045(b), D-051): accepted or edited entries, AI-made or human, whose current summary or quote fails a code check.
app/backend/trace.py:875:        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
app/backend/trace.py:905:    """The one sentence for n accepted AI-made items whose second check has no answer: the 422 `judge_not_run` message and the export-gate headline (T-134 r4)."""
app/backend/trace.py:913:    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
app/backend/trace.py:914:    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
app/backend/trace.py:922:            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
app/backend/trace.py:934:    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one.
app/backend/trace.py:1070:    prep = bool(cx.models.get("generator_prepared"))      # T-177 r2 / D-065: the case's answers are hand-checked fixtures, so the step must not say an AI drafted them
app/backend/trace.py:1071:    xlabel = CASE_PREPARED_LABEL if prep else "AI drafts a summary and a quote for each record"
app/backend/trace.py:1078:        st.append(step("extract", xlabel, "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no {'prepared' if prep else 'AI-made'} entry. "
app/backend/trace.py:1082:        st.append(step("extract", xlabel, "llm", PASS, (f"The prepared answers (hand-checked by the team for the demo) cover all {len(firsts)} records." if prep else f"The AI drafted an entry for all {len(firsts)} records."), rule="ro
app/backend/trace.py:1101:    jlabel = "Second AI check on every prepared item" if prep else "Second AI check on every AI-made item"      # T-177 r2: the items are the team's prepared answers
app/backend/trace.py:1222:    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
app/backend/rejudge.py:4:    Targets: live (not rejected, not dismissed) AI-made entries, charges and flags with a judge verdict of 'unavailable' or no verdict (trace.unjudged_items).
app/backend/export.py:855:    """The export refuses (D-044, D-045): a run in progress or failed, nothing accepted, or accepted AI-made items whose second check never ran. No override.
app/backend/present.py:302:    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
app/backend/api.py:36:AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
app/backend/api.py:458:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
app/backend/review.py:64:# D-051: the code rung binds accept for every item, AI-made or human. These are the code checks on an entry's current wording.
app/backend/pipeline.py:260:    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:02.367Z

The grep turns up two things to check: the per-item trace step at `trace.py:392-414` still has "AI drafted" wording in some branches, and the frontend `mock*.js` files still carry a model name. I'll read the trace branch and the frontend header that decides whether the banner falls back to the default text.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:02.941Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && sed -n '376,420p' app/backend/trace.py | cut -c1-330",
 "description": "Read per-item extracted step branches in trace.py"
}
````

### User / tool · 2026-11-02T21:06:03.018Z

**tool result**
````
def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    # D-051: all five code checks (and the highlight) are recomputed from the CURRENT summary and quote, as accept does, and also honour what was stored
    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
    placeholder = lad.get("failure")                      # could-not-verify tray placeholder: the AI made no usable summary, so there is no quote to check (T-112 r2)
    verbatim_fail = not placeholder and ("GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False or "GROUNDING_EXCERPT_NOT_VERBATIM" in live)
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else (placeholder or ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None))
    st = []
    # 1 extracted
    if lad.get("entered_by"):
        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
                       evidence={"excerpt": exc}))
    else:
        gen = lad.get("generator") or {}
        call = cx.call(gen.get("call_id"), row["id"], "extract")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
        ev["excerpt"] = exc
        if schema_fail:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
                           evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "LLM_FAILED_AFTER_RETRIES" in R:
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
                           rule="row 4", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "SUMMARY_NOT_IN_QUOTE" in R:                     # D-054: code removed every clause; the notes say which
            ev["removed"] = (lad.get("summary_trim") or {}).get("removed") or []
            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL,
                           " ".join((lad.get("summary_trim") or {}).get("notes") or []) + " " + reason_text("SUMMARY_NOT_IN_QUOTE"), reason="SUMMARY_NOT_IN_QUOTE",
                           rule="D-054", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        else:
            if ev["model"]["prepared"]:
                st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
            else:
                st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
                               "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
            trim = lad.get("summary_trim")
            if trim and trim.get("removed"):                  # D-054: shown, never silent. The judge saw the trimmed summary.
                st.append(step("summary_trimmed", "Code removed summary parts the quote does not support", "code", PASS, " ".join(trim.get("notes") or []),
                               rule="D-054", evidence={"removed": trim["removed"], "original_summary": trim.get("original_summary"), "kept_summary": trim.get("kept_summary")}))
            st.extend(_narrow_steps(lad, row))                # T-139: code shortened the AI's quote / removed an amount clause; shown, never silent, never in the letter
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:03.710Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && sed -n '1,30p' app/frontend/app.js | cut -c1-300 && echo \"=== API_MODE / mock selection ===\" && grep -rn \"API_MODE\\s*=\\|API_MODE =\\|mock.js\\|mock_extra\" app/frontend/*.js app/frontend/*.html | cut -c1-240",
 "description": "Read app.js banner fallback and mock mode selection"
}
````

### User / tool · 2026-11-02T21:06:03.801Z

**tool result**
````
/* Bootstrap: health -> banners; restore case from #case=<token>; poll run status; render on every state change. */
(function () {
  const ZL = window.ZL, { $ } = ZL;
  const SYNTH = "Synthetic data only — never paste real records";
  let poller = null;

  function renderChrome(s) {
    const h = s.health;
    $("#banner-synthetic").textContent = (h && h.banner) || SYNTH;           // present on every view, even before /health answers
    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
    // T-166 F7: no test or developer wording on screen. The demo says what it is in the paralegal's words; the longer explanation is the tooltip. A live backend has nothing to announce.
    const badge = $("#badge"); const demo = !!(h && h.demo_mode), mock = ZL.API_MODE === "mock";
    // D-065: say whose answers the demo replays. Prepared (curated) answers are the team's, never the model's; recorded ones are real model answers.
    const prepared = demo && h.answers === "prepared";
    badge.textContent = prepared ? "Demo: sample answers prepared by our team" : demo ? "Demo: recorded AI answers" : mock ? "Sample data" : "";
    badge.title = prepared ? "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."     // T-177 r2: says only what is true
      : demo ? "This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service." : "";
    badge.hidden = !(demo || mock);
    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
    live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
    $("#delete-now").hidden = live.hidden;
  }
  // ---- case header (sticky): case name, "n of N decided", Export. The numbers are counts of what the API sent; nothing is computed beyond counting.
  const itemsOf = (c) => [].concat(c.entries || [], c.undated_entries || [], c.amounts || [], c.flags || []).filter((i) => i.state !== "rejected");
  // T-060 r5: "decided" means she has nothing left to do on the item. A dismissed item is decided. An edited item that is still marked Needs review is NOT: it is counted as an
  // edit to check. One need-review count (`needs`) is used by the header, the Open-decisions strip and the Timeline chip, and it falls when an item is decided or dismissed.
  // T-174 F9: ONE need-review number. It is the server's hitl.needs_review_open (the list summary of this case) whenever that summary describes the same moment as the case on screen (the same open
  // total: pending + edits_to_check); in the moments after a decision, before the summary is asked again, the same definition is counted from the case itself, so the number never lags or disagrees.
  ZL.progressOf = function (c) {
    const all = itemsOf(c), open = all.filter(ZL.undecided), mine = open.filter((i) => i.state === "needs_review" || ZL.editToCheck(i)).length;   // an edit still to compare is Needs review by definition (the server counts it; its response may lag the item's state)
=== API_MODE / mock selection ===
app/frontend/app.js:12:    const badge = $("#badge"); const demo = !!(h && h.demo_mode), mock = ZL.API_MODE === "mock";
app/frontend/api.js:1:/* API client. ONE switch: API_MODE. "mock" uses mock.js (in-memory, contract-shaped); "real" calls the FastAPI backend under /api.
app/frontend/api.js:5:  const API_MODE = "real"; // <-- the ONE switch: "real" (FastAPI under /api) or "mock" (in-memory, mock.js)
app/frontend/api.js:7:  ZL.API_MODE = mode;
app/frontend/input.js:32:    if (!previewToken || ZL.API_MODE === "mock") return;
app/frontend/mock.js:1:/* In-memory mock of the api.md contract (shapes copied from memory/contracts/api.md). Dev/test only: used while API_MODE === "mock".
app/frontend/judges.js:222:      }, () => { if (cache) return; if (ZL.API_MODE === "mock" && root.isConnected) paint(root, null, "AI check details need the live server."); else root.hidden = true; });
app/frontend/switcher.js:10:    if (ZL.API_MODE === "mock") return ZL.mock.handle("GET", path);
app/frontend/stepper.js:484:      (e) => { msg.textContent = ZL.API_MODE === "mock" ? "Step-by-step checks need the live server." : "The checks could not be loaded: " + e.message; });
app/frontend/review.js:36:    if (ZL.API_MODE === "mock") return ZL.mock.handle(method, path, body);
app/frontend/index.html:69:<script src="mock.js"></script>
app/frontend/index.html:71:<script src="mock_extra.js"></script>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:21.462Z

Two things need checking on the served path: the trace step's failure branches (`trace.py:400-407`) hard-code "AI drafted" even when the item is prepared, and the banner fallback in `app.js:10`. I'll write a probe that walks every curated and recorded payload and reports any drafting-model or "AI draft" wording it finds, with the path it came from.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:30.333Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2.py",
 "content": "\"\"\"T-177 r2 probe (staff-engineer-reviewer, round 2). Runs against the git archive copy (HEAD), not the shared app.\nUsage: python -I probe_r2.py <archive_dir> <scratch_dir>\nStarts an in-process TestClient with FIXTURE_SET=curated (prepared) and with the recorded set (control), and walks every\npayload a reader can reach for the sample case, reporting drafting-model or 'AI draft' wording with the path it came from.\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\n\nARCH, SCRATCH = sys.argv[1], sys.argv[2]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nPATTERNS = [\"claude-sonnet\", \"AI draft\", \"AI drafted\", \"AI drafts\", \"AI-made\", \"Drafted by\", \"drafted by AI\", \"extract_v1\", \"prompt_sha256\",\n            \"recorded AI answers\", \"first AI\", \"AI's drafts\", \"The AI read this record\", \"The AI drafted\", \"AI-written\", \"generated by\"]\n\n\ndef make_client(db, fixture_set):\n    os.environ[\"LLM_BACKEND\"] = \"fixture\"\n    os.environ[\"ZLAYT_MODE\"] = \"local\"\n    for k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"LLM_FIXTURE_DIR\", \"FIXTURE_SET\"):\n        os.environ.pop(k, None)\n    if fixture_set:\n        os.environ[\"FIXTURE_SET\"] = fixture_set\n    return TestClient(create_app(db, static_dir=os.path.join(ARCH, \"app\", \"frontend\")), client=(\"127.0.0.1\", 50000))\n\n\ndef run_case(c):\n    tok = c.post(\"/api/cases\", json={\"sample\": True, \"title\": \"Rivera v. Northgate (MVA 2026-01)\"}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(480):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    return tok, s[\"status\"]\n\n\ndef hits(label, obj, out):\n    text = json.dumps(obj, ensure_ascii=False)\n    for p in PATTERNS:\n        for m in re.finditer(re.escape(p), text):\n            out.append((label, p, text[max(0, m.start() - 70): m.end() + 50]))\n\n\ndef walk(c, tok, tag, report):\n    found = []\n    for path in [\"/api/health\", f\"/api/cases/{tok}\", f\"/api/cases/{tok}/judges\", f\"/api/cases/{tok}/audit\", f\"/api/cases/{tok}/trace\",\n                 f\"/api/cases/{tok}/status\", \"/api/cases\", f\"/api/cases/{tok}/export\"]:\n        r = c.get(path)\n        report.append(f\"[{tag}] GET {path} -> {r.status_code}\")\n        if r.headers.get(\"content-type\", \"\").startswith(\"application/json\"):\n            hits(f\"{tag} GET {path}\", r.json(), found)\n    case = c.get(f\"/api/cases/{tok}\").json()\n    ids = [x[\"id\"] for x in case.get(\"entries\", [])] + [x[\"id\"] for x in case.get(\"amounts\", [])] + [x[\"id\"] for x in case.get(\"flags\", [])]\n    report.append(f\"[{tag}] item ids: {len(ids)} ({len(case.get('entries', []))} entries)\")\n    prep_items = 0\n    for iid in ids:\n        ir = c.get(f\"/api/cases/{tok}/items/{iid}\")\n        if ir.status_code == 200:\n            hits(f\"{tag} GET items/{iid}\", ir.json(), found)\n            if (ir.json().get(\"item\") or {}).get(\"prepared\") is True:\n                prep_items += 1\n        tr = c.get(f\"/api/cases/{tok}/items/{iid}/trace\")\n        if tr.status_code == 200:\n            hits(f\"{tag} GET items/{iid}/trace\", tr.json(), found)\n    report.append(f\"[{tag}] items walked: {len(ids)}; prepared items: {prep_items}\")\n    return found\n\n\ndef prepared_trace_labels(c, tok, report):\n    \"\"\"Every item's generator step label and why, and any failure branch that says 'AI drafted' while evidence.model.prepared is true.\"\"\"\n    bad = []\n    case = c.get(f\"/api/cases/{tok}\").json()\n    for e in case.get(\"entries\", []):\n        tr = c.get(f\"/api/cases/{tok}/items/{e['id']}/trace\").json()\n        gen = next((s for s in tr[\"steps\"] if s[\"id\"] == \"extracted\"), None)\n        if gen is None:\n            continue\n        prepared = bool((gen.get(\"evidence\") or {}).get(\"model\", {}).get(\"prepared\"))\n        report.append(f\"  item {e['id']} state={e.get('state')} step={gen.get('status')} prepared={prepared} label={gen.get('label')!r} model={(gen.get('evidence') or {}).get('model', {}).get('id')!r}\")\n        if prepared and \"AI\" in (gen.get(\"label\") or \"\"):\n            bad.append((e[\"id\"], gen.get(\"status\"), gen.get(\"label\"), gen.get(\"why\")))\n    return bad\n\n\ndef main():\n    out_lines = []\n    cur_db = os.path.join(SCRATCH, \"probe_curated.sqlite\")\n    rec_db = os.path.join(SCRATCH, \"probe_recorded.sqlite\")\n    for p in (cur_db, rec_db):\n        if os.path.exists(p):\n            os.remove(p)\n\n    c = make_client(cur_db, \"curated\")\n    tok, st = run_case(c)\n    out_lines.append(f\"[curated] run status={st}\")\n    f_cur = walk(c, tok, \"curated\", out_lines)\n    bad = prepared_trace_labels(c, tok, out_lines)\n    out_lines.append(f\"[curated] prepared generator steps labelled with 'AI': {len(bad)}\")\n    for b in bad:\n        out_lines.append(f\"  BAD {b}\")\n    out_lines.append(f\"[curated] pattern hits in reachable payloads: {len(f_cur)}\")\n    for h in f_cur:\n        out_lines.append(f\"  HIT {h[0]} | {h[1]!r} | ...{h[2]}...\")\n    # the 'Why' ladder fields the UI shows for the first entry\n    case = c.get(f\"/api/cases/{tok}\").json()\n    if case.get(\"entries\"):\n        e1 = case[\"entries\"][0]\n        out_lines.append(f\"[curated] entry {e1['id']} ladder.generator = {json.dumps(e1.get('ladder', {}).get('generator'), ensure_ascii=False)[:400]}\")\n\n    c2 = make_client(rec_db, None)\n    tok2, st2 = run_case(c2)\n    out_lines.append(f\"[recorded] run status={st2}\")\n    f_rec = walk(c2, tok2, \"recorded\", out_lines)\n    out_lines.append(f\"[recorded] pattern hits (expected: AI labels and model ids present): {len(f_rec)}\")\n    for h in f_rec[:12]:\n        out_lines.append(f\"  HIT {h[0]} | {h[1]!r} | ...{h[2]}...\")\n    text = \"\\n\".join(out_lines)\n    print(text)\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:06:30.461Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:33.224Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SCR\" && .venv/bin/python -I $EV/probe_r2.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2.out 2>&1; echo \"exit=$?\"; cut -c1-400 $EV/probe-r2.out | head -150",
 "description": "Run the round-2 payload probe against the archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:06:35.114Z

**tool result**
````
exit=0
[curated] run status=ready
[curated] GET /api/health -> 200
[curated] GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ -> 200
[curated] GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/judges -> 200
[curated] GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit -> 200
[curated] GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/trace -> 200
[curated] GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/status -> 200
[curated] GET /api/cases -> 200
[curated] GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/export -> 422
[curated] item ids: 23 (9 entries)
[curated] items walked: 23; prepared items: 9
  item e1 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e2 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e3 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e4 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e5 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e6 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e7 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e8 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
  item e9 state=verified step=pass prepared=True label='Prepared answer, standing in for the AI draft' model='hand-checked (qa)'
[curated] prepared generator steps labelled with 'AI': 9
  BAD ('e1', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e2', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e3', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e4', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e5', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e6', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e7', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e8', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
  BAD ('e9', 'pass', 'Prepared answer, standing in for the AI draft', 'Prepared answer (hand-checked by the team for the demo), standing in for the AI draft')
[curated] pattern hits in reachable payloads: 157
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ... alert and oriented; transported to Central ER."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...10 mg prescribed; follow up with PCP in 1 week."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...ferred to physical therapy 2x/week for 6 weeks."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...on reduced approx. 40%; plan of care 12 visits."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ... improving.", "summary": "Pain 4/10, improving."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...erapy after two missed appointments; pain 3/10."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...rm with numbness in fingers, 7/10; MRI ordered."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...egenerative change and to correlate clinically."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ | 'extract_v1' | ...tes symptoms began after the January collision."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "aacd477fd06e2a5bc1729568312bf...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "228350fb06e4cf872348f390212b9...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "bde3b432c62b6dd09e7d4e18309d7...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "be8b230f82b33d2d1e8a9e1e0c6d1...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "0f653bdfe99e71b7c81505f7bc5d3...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "4770363f6bf66fd6ea99a13cfb801...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "a3f0e26ea728d289fec7de9c1a0de...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d36...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "228350fb06e4cf872348f390212b959eebee7313b76f0e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d011...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "4770363f6bf66fd6ea99a13cfb8010ae193143c79e5316...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "a3f0e26ea728d289fec7de9c1a0de532e5a7b68efdbb86...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "6faaefbcd81dd8f8b0c9bf123a19a4e168e77bfef3ae9d...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "46c8548cbc8e23ab7093d23904905e4e400ef4c6eb8499...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "636239bec8cb1f0bedd4a1dec8e691ef3e4d43c35ee74f...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "11b63311d0540b20ebda1d3792e15b80fae54f0cd9b31e...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "81b9613e80eb3b3c5ba7c3d9a8c75b61a8e28b3b08dc25...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "f5212e784cce54b0dd547f184cd405c56e7ebec814f825...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "381284dcc1b16c10482345adac4fbf4c7589f9296e20a7...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "527b0abaed8766e43da906d3ef72c1a1ca4feda281901b...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "056527c8d5791a06af8e2dff2af8134fcd3b2969bea747...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "prompt_sha256": "632a0e6302845a76592de8f53c07e4809ea08d9727f280...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "prompt_sha256": "f2f207afab19f26f381d11c7f1b84064e3d14d1ae5bde6...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "prompt_sha256": "8258d36c1cdad8d5f84566c7d7ccb6f8cbdf043cc018ab...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ... "model": "claude-haiku-5-5", "prompt_version": "judge_conflict_v6", "prompt_sha256": "24c279d76f6aae120c0bb6a8b47ce4a059cf52d44323a1...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "4a4f531c922d869d060a0bf7b1d33b777c496b90570dd5...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "7f9e06e6e15e75756fa39c3aca5bb45dcaa75e29d727b0...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "37318d752543b06d4add14f3ab3aa71dc4e089522d392b...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "4ed3d9961f3523183444f9fe85f8d460762306ec1bc8d8...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "1ae147d35880668764ee15dc7b6b20f68fa6a4e331e910...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "85a544a335859c486aaa581be110146353bbe09d65a0b3...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "b0511a4e8269eaffd9832fbd4d21b731b8a552b0d09aa0...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "a1f0777e7722b161b62e8d670366303c827a2daff336fa...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...6:58Z"}, "model": "hand-checked (qa)", "prompt_version": "flags_v1", "prompt_sha256": "eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...Z"}, "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "prompt_sha256": "6d5e6fe3fae088b5dd8fe7964771f61a25a922a5ac7385...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...Z"}, "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "prompt_sha256": "b362099fadec12e740f2fdedb9e84de793ef1b3c6d8199...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...Z"}, "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "prompt_sha256": "5b05ba47abeb8a9571b0ac9bf3f9badf9c1b9309b76458...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...Z"}, "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "prompt_sha256": "41e42a2978854c340fcf3f43360478c22289d982857f3a...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...Z"}, "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "prompt_sha256": "e2f91427aeef98707788656002a95c251a33a13b481a70...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/audit | 'prompt_sha256' | ...Z"}, "model": "claude-haiku-5-5", "prompt_version": "judge_flag_v3", "prompt_sha256": "40edf164293ce60521fb2bee311f3741eaff8b4b39498d...
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/trace | 'AI draft' | ...: "Prepared summaries and quotes for each record, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "The pr...
  HIT curated GET items/e1 | 'extract_v1' | ... alert and oriented; transported to Central ER."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e1 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1...
  HIT curated GET items/e1 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f...
  HIT curated GET items/e1 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "636239bec8cb1f0bedd4a1dec8e691ef3e4d43c35ee74f...
  HIT curated GET items/e1/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e1/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e1/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1...
  HIT curated GET items/e1/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f...
  HIT curated GET items/e1/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "636239bec8cb1f0bedd4a1dec8e691ef3e4d43c35ee74f...
  HIT curated GET items/e2 | 'extract_v1' | ...10 mg prescribed; follow up with PCP in 1 week."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e2 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd...
  HIT curated GET items/e2 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3...
  HIT curated GET items/e2 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "6faaefbcd81dd8f8b0c9bf123a19a4e168e77bfef3ae9d...
  HIT curated GET items/e2/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e2/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e2/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd...
  HIT curated GET items/e2/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3...
  HIT curated GET items/e2/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "6faaefbcd81dd8f8b0c9bf123a19a4e168e77bfef3ae9d...
  HIT curated GET items/e3 | 'extract_v1' | ...ferred to physical therapy 2x/week for 6 weeks."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e3 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "aacd477fd06e2a5bc1729568312bf...
  HIT curated GET items/e3 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d36...
  HIT curated GET items/e3 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "46c8548cbc8e23ab7093d23904905e4e400ef4c6eb8499...
  HIT curated GET items/e3/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e3/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e3/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "aacd477fd06e2a5bc1729568312bf...
  HIT curated GET items/e3/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d36...
  HIT curated GET items/e3/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "46c8548cbc8e23ab7093d23904905e4e400ef4c6eb8499...
  HIT curated GET items/e4 | 'extract_v1' | ...on reduced approx. 40%; plan of care 12 visits."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e4 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "228350fb06e4cf872348f390212b9...
  HIT curated GET items/e4 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "228350fb06e4cf872348f390212b959eebee7313b76f0e...
  HIT curated GET items/e4 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "11b63311d0540b20ebda1d3792e15b80fae54f0cd9b31e...
  HIT curated GET items/e4/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e4/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e4/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "228350fb06e4cf872348f390212b9...
  HIT curated GET items/e4/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "228350fb06e4cf872348f390212b959eebee7313b76f0e...
  HIT curated GET items/e4/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "11b63311d0540b20ebda1d3792e15b80fae54f0cd9b31e...
  HIT curated GET items/e5 | 'extract_v1' | ... improving.", "summary": "Pain 4/10, improving."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e5 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "bde3b432c62b6dd09e7d4e18309d7...
  HIT curated GET items/e5 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3...
  HIT curated GET items/e5 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "81b9613e80eb3b3c5ba7c3d9a8c75b61a8e28b3b08dc25...
  HIT curated GET items/e5/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e5/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e5/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "bde3b432c62b6dd09e7d4e18309d7...
  HIT curated GET items/e5/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3...
  HIT curated GET items/e5/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "81b9613e80eb3b3c5ba7c3d9a8c75b61a8e28b3b08dc25...
  HIT curated GET items/e6 | 'extract_v1' | ...erapy after two missed appointments; pain 3/10."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e6 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "be8b230f82b33d2d1e8a9e1e0c6d1...
  HIT curated GET items/e6 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d011...
  HIT curated GET items/e6 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "f5212e784cce54b0dd547f184cd405c56e7ebec814f825...
  HIT curated GET items/e6/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e6/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e6/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "be8b230f82b33d2d1e8a9e1e0c6d1...
  HIT curated GET items/e6/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d011...
  HIT curated GET items/e6/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "f5212e784cce54b0dd547f184cd405c56e7ebec814f825...
  HIT curated GET items/e7 | 'extract_v1' | ...rm with numbness in fingers, 7/10; MRI ordered."}, "prompt_version": "extract_v1", "prepared": true}, "human": {"action": null, "e...
  HIT curated GET items/e7 | 'extract_v1' | ...6-11-02T02:46:58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "0f653bdfe99e71b7c81505f7bc5d3...
  HIT curated GET items/e7 | 'prompt_sha256' | ...58Z"}, "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445...
  HIT curated GET items/e7 | 'prompt_sha256' | ...del": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "381284dcc1b16c10482345adac4fbf4c7589f9296e20a7...
  HIT curated GET items/e7/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e7/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e7/trace | 'extract_v1' | ...ndependent_of_generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "0f653bdfe99e71b7c81505f7bc5d3...
  HIT curated GET items/e7/trace | 'prompt_sha256' | ...generator": null, "prepared": true}, "prompt_version": "extract_v1", "prompt_sha256": "0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445...
  HIT curated GET items/e7/trace | 'prompt_sha256' | ...true, "prepared": false}, "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "381284dcc1b16c10482345adac4fbf4c7589f9296e20a7...
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:44.003Z

Two things stand out in that output. The nine "BAD" lines are a false positive from my own probe, because D-065 requires the phrase "standing in for the AI draft". The real finding is that the API payloads still carry `prompt_version: extract_v1` and a `prompt_sha256` on prepared rows, which the UI hides but the API does not. I'll filter the rest of the output for the model-name and drafter patterns, since the head truncated it.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:06:45.737Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2 && echo \"=== curated section: hits for drafter/model/AI-made patterns (excluding prompt fields) ===\" && awk '/^\\[curated\\] pattern hits/{f=1} /^\\[recorded\\] run/{f=0} f' probe-r2.out | grep \"HIT\" | grep -v \"'extract_v1'\\|'prompt_sha256'\" | cut -c1-330; echo \"=== count of curated HIT lines by pattern ===\"; awk '/^\\[curated\\] pattern hits/{f=1} /^\\[recorded\\] run/{f=0} f' probe-r2.out | grep \"HIT\" | sed -E \"s/.*\\| ('[^']+') \\|.*/\\1/\" | sort | uniq -c; echo \"=== recorded section summary ===\"; awk '/^\\[recorded\\] run/{f=1} f' probe-r2.out | grep -v \"HIT\" | cut -c1-240; echo \"=== recorded HIT sample ===\"; awk '/^\\[recorded\\] run/{f=1} f' probe-r2.out | grep \"HIT\" | cut -c1-260 | head -12",
 "description": "Filter probe output for drafter and model-name hits"
}
````

### User / tool · 2026-11-02T21:06:45.860Z

**tool result**
````
=== curated section: hits for drafter/model/AI-made patterns (excluding prompt fields) ===
  HIT curated GET /api/cases/fDN74V0n7ENzWrRCMmR0xQ/trace | 'AI draft' | ...: "Prepared summaries and quotes for each record, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "The pr...
  HIT curated GET items/e1/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e1/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e2/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e2/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e3/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e3/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e4/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e4/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e5/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e5/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e6/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e6/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e7/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e7/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e8/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e8/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
  HIT curated GET items/e9/trace | 'AI draft' | ...: [{"id": "extracted", "label": "Prepared answer, standing in for the AI draft", "kind": "llm", "status": "pass", "why": "Prepar...
  HIT curated GET items/e9/trace | 'AI draft' | ...d answer (hand-checked by the team for the demo), standing in for the AI draft", "reason_code": null, "rule": "D-065", "blocks_e...
=== count of curated HIT lines by pattern ===
  19 'AI draft'
  45 'extract_v1'
  93 'prompt_sha256'
=== recorded section summary ===
[recorded] run status=ready
[recorded] GET /api/health -> 200
[recorded] GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g -> 200
[recorded] GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g/judges -> 200
[recorded] GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g/audit -> 200
[recorded] GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g/trace -> 200
[recorded] GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g/status -> 200
[recorded] GET /api/cases -> 200
[recorded] GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g/export -> 422
[recorded] item ids: 23 (9 entries)
[recorded] items walked: 23; prepared items: 0
[recorded] pattern hits (expected: AI labels and model ids present): 275
=== recorded HIT sample ===
  HIT recorded GET /api/health | 'claude-sonnet' | ...answers": "recorded", "live_enabled": false, "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_pre...
  HIT recorded GET /api/health | 'drafted by AI' | ...s": 40}, "retention_hours": 24, "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item", "sam...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...y", "demo_mode": true, "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_pre...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "cda2973a845cd", "model": "claude-sonnet-5-5", "output": {"excerpt": "41M restrained drive...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...harges $6,240"]}, "generator": {"call_id": "ccc00abfa5372", "model": "claude-sonnet-5-5", "output": {"excerpt": "Dx: cervical strain;...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "cffac5ed5ee10", "model": "claude-sonnet-5-5", "output": {"excerpt": "Persistent neck pain...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...er visit $185"]}, "generator": {"call_id": "c845ae645e54d", "model": "claude-sonnet-5-5", "output": {"excerpt": "Cervical range of mo...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "cc1d050351de1", "model": "claude-sonnet-5-5", "output": {"excerpt": "Pain 4/10, improving...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "cbbc4b7d5f34a", "model": "claude-sonnet-5-5", "output": {"excerpt": "Discharged from PT a...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "c369a4ddd55ff", "model": "claude-sonnet-5-5", "output": {"excerpt": "New onset pain radia...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "c5135d7a616ce", "model": "claude-sonnet-5-5", "output": {"excerpt": "C5-C6 disc protrusio...
  HIT recorded GET /api/cases/bElJ3vRw1tIYXU0dG4yT3g | 'claude-sonnet' | ...in_excerpt": []}, "generator": {"call_id": "cb01289e62dbf", "model": "claude-sonnet-5-5", "output": {"excerpt": "Recommend cervical e...
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:05.890Z

The curated probe is clean for the surfaces the user named. The only AI-draft wording is the phrase D-065 prescribes, and the curated payloads contain no `claude-sonnet`, no "Drafted by", and no "AI-made". The recorded control still names `claude-sonnet-5-5`, as expected. The remaining open question is the trace failure branches, which hard-code "AI drafted" even for prepared items. I'll read how the fixture backend loads its set and how the export renders provenance, so I can test that branch with a changed curated fixture.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:06.726Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && echo \"=== fixture.py ===\" && sed -n '1,60p' app/llm/backends/fixture.py | cut -c1-260 && echo \"=== curated dir listing ===\" && ls app/llm/fixtures 2>/dev/null | head; find . -path ./artifacts -prune -o -type d -name \"curated\" -print | head -5",
 "description": "Read fixture backend and locate curated fixture directory"
}
````

### User / tool · 2026-11-02T21:07:06.826Z

**tool result**
````
=== fixture.py ===
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p


def answer_source() -> str:
    """D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers)."""
    return "prepared" if fixture_dir().name == "curated" else "recorded"
=== curated dir listing ===
./tests/fixtures/llm/curated
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:15.522Z

The curated fixtures are keyed by hash under `tests/fixtures/llm/curated`, and `answer_source()` treats any directory named `curated` as prepared. I'll confirm the e1 generator fixture file, then copy the set to scratch and break that one answer's schema, to see which label a failed prepared item gets.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:16.674Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && ls tests/fixtures/llm/curated | wc -l && ls tests/fixtures/llm/curated | grep \"^98b1735\" ; python3 -c \"import json,sys; d=json.load(open('tests/fixtures/llm/curated/98b1735efe416a520c3489da333b1326b50420338d0e2f'+'0'*0+'.json'))\" 2>/dev/null; f=$(ls tests/fixtures/llm/curated | grep \"^98b1735\" | head -1); echo \"file=$f\"; cat tests/fixtures/llm/curated/$f | cut -c1-600",
 "description": "Locate e1 generator fixture file by prompt hash prefix"
}
````

### User / tool · 2026-11-02T21:07:16.796Z

**tool result**
````
      19
98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
file=98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
{
 "CURATED": "CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).",
 "output": {
  "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.",
  "summary": "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER."
 },
 "recorded_from": {
  "backend": "curated",
  "model": "hand-checked (qa)",
  "recorded_at": "2026-11-02T02:46:58Z"
 }
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:20.058Z

The e1 fixture is the one to break. I'll write a small probe that copies the curated set into scratch, removes the `summary` key from e1's answer (so schema validation fails), runs the case through the same code path, and prints e1's trace step and item state.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:24.945Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py",
 "content": "\"\"\"T-177 r2 branch probe (staff-engineer-reviewer). Question: does a PREPARED (curated) item whose generator answer FAILS a code check\nstill get the prepared label in its trace, or the 'AI drafted' label?\nMethod: copy the archive's curated fixture set to a scratch dir named 'curated' (so answer_source() is 'prepared'), break e1's\ngenerator answer by removing its `summary` key (schema fails), run the sample case through the normal pipeline, read e1's trace.\nUsage: python -I probe_r2_branch.py <archive_dir> <scratch_dir>\"\"\"\nimport json\nimport os\nimport shutil\nimport sys\nimport time\n\nARCH, SCRATCH = sys.argv[1], sys.argv[2]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\n\nE1_KEY = \"98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7\"   # e1's generator answer (curated/, prepared by hand)\n\nmut_root = os.path.join(SCRATCH, \"mut_branch\")\nmut_dir = os.path.join(mut_root, \"curated\")\nif os.path.isdir(mut_root):\n    shutil.rmtree(mut_root)\nos.makedirs(mut_root)\nshutil.copytree(os.path.join(ARCH, \"tests\", \"fixtures\", \"llm\", \"curated\"), mut_dir)\np = os.path.join(mut_dir, E1_KEY + \".json\")\nd = json.load(open(p))\ndel d[\"output\"][\"summary\"]                      # schema now invalid for e1\njson.dump(d, open(p, \"w\"), indent=1, sort_keys=True)\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ[\"ZLAYT_MODE\"] = \"local\"\nos.environ[\"LLM_FIXTURE_DIR\"] = mut_dir\nfor k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"FIXTURE_SET\"):\n    os.environ.pop(k, None)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nc = TestClient(create_app(os.path.join(SCRATCH, \"mut_branch.sqlite\"), static_dir=os.path.join(ARCH, \"app\", \"frontend\")), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True, \"title\": \"branch probe\"}).json()[\"token\"]\nassert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\nfor _ in range(480):\n    s = c.get(f\"/api/cases/{tok}/status\").json()\n    if s[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.25)\nprint(\"run status:\", s[\"status\"])\nprint(\"health answers:\", c.get(\"/api/health\").json().get(\"answers\"))\nitem = c.get(f\"/api/cases/{tok}/items/e1\").json()[\"item\"]\nprint(\"e1 state:\", item.get(\"state\"), \"reasons:\", item.get(\"state_reasons\") or item.get(\"reasons\"), \"prepared:\", item.get(\"prepared\"))\nprint(\"e1 ladder.generator.model:\", (item.get(\"ladder\") or {}).get(\"generator\", {}).get(\"model\"))\ntr = c.get(f\"/api/cases/{tok}/items/e1/trace\").json()\ngen = next(x for x in tr[\"steps\"] if x[\"id\"] == \"extracted\")\nprint(\"e1 extracted step:\")\nprint(json.dumps({k: gen.get(k) for k in (\"label\", \"status\", \"why\", \"reason_code\", \"rule\")}, indent=1, ensure_ascii=False))\nprint(\"e1 extracted evidence.model:\", json.dumps((gen.get(\"evidence\") or {}).get(\"model\"), ensure_ascii=False))\ncase_tr = c.get(f\"/api/cases/{tok}/trace\").json()\nex = next(x for x in case_tr[\"steps\"] if x[\"id\"] == \"extract\")\nprint(\"case-level extract step label:\", repr(ex.get(\"label\")), \"status:\", ex.get(\"status\"))\nprint(\"case-level extract why:\", repr(ex.get(\"why\")))\n"
}
````

### User / tool · 2026-11-02T21:07:25.038Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:27.962Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_branch.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2-branch.out 2>&1; echo \"exit=$?\"; cut -c1-400 $EV/probe-r2-branch.out",
 "description": "Run failed-curated-item branch probe against archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:07:28.951Z

**tool result**
````
exit=1
llm call failed call_id=cebc2e101c4c8 step=extract attempt=1
llm call failed call_id=ca8d2c6ed2cb5 step=extract attempt=2 prompt_hash=81726a2f47db088d333ae3bea0ce9d3281ab3432314533b752ac5db1db3ab6a2
llm call failed call_id=cd76290a080a1 step=j1 attempt=1 prompt_hash=6faaefbcd81dd8f8b0c9bf123a19a4e168e77bfef3ae9d74bc90ef232fc6e353
llm call failed call_id=c9b79efa48d14 step=j1 attempt=1 prompt_hash=11b63311d0540b20ebda1d3792e15b80fae54f0cd9b31e41d1efd2605bab803a
llm call failed call_id=c5c27493340c9 step=j1 attempt=1 prompt_hash=46c8548cbc8e23ab7093d23904905e4e400ef4c6eb8499806d234f247dd75262
llm call failed call_id=c5099456fa711 step=j1 attempt=1 prompt_hash=81b9613e80eb3b3c5ba7c3d9a8c75b61a8e28b3b08dc259854b7a2424eb3ecb2
llm call failed call_id=c66dea7786247 step=j1 attempt=1 prompt_hash=f5212e784cce54b0dd547f184cd405c56e7ebec814f8257f091fe60ffe2eda10
llm call failed call_id=c20d62de69f77 step=j1 attempt=1 prompt_hash=381284dcc1b16c10482345adac4fbf4c7589f9296e20a71edcb346002a8d84e5
llm call failed call_id=c30e894aa3998 step=j1 attempt=1 prompt_hash=527b0abaed8766e43da906d3ef72c1a1ca4feda281901b5b5169faa6f1ab8dbd
llm call failed call_id=ceaa0a73cfaaa step=j1 attempt=1 prompt_hash=056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d
llm call failed call_id=c0d6a512654b0 step=j2 attempt=1 prompt_hash=632a0e6302845a76592de8f53c07e4809ea08d9727f280e2e72b226c9faa5aa7
llm call failed call_id=c750c004edb9e step=j2 attempt=1 prompt_hash=f2f207afab19f26f381d11c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c
llm call failed call_id=c655bcfb94b23 step=j2 attempt=1 prompt_hash=8258d36c1cdad8d5f84566c7d7ccb6f8cbdf043cc018ab771440220878c84c96
llm call failed call_id=c743309cd491b step=j3 attempt=1 prompt_hash=24c279d76f6aae120c0bb6a8b47ce4a059cf52d44323a1af0793e17fb55851c0
llm call failed call_id=cc4a3ddb98182 step=j4 attempt=1 prompt_hash=6d5e6fe3fae088b5dd8fe7964771f61a25a922a5ac73859003d373d4c3536c06
llm call failed call_id=caf22a6e686d7 step=j4 attempt=1 prompt_hash=b362099fadec12e740f2fdedb9e84de793ef1b3c6d8199cf65b07e65215991a9
llm call failed call_id=c5ac73ccb5317 step=j4 attempt=1 prompt_hash=5b05ba47abeb8a9571b0ac9bf3f9badf9c1b9309b76458a00213118b383ce266
llm call failed call_id=c596e3b58dbe4 step=j4 attempt=1 prompt_hash=41e42a2978854c340fcf3f43360478c22289d982857f3abc73377b804535ad59
llm call failed call_id=ce8a76963e48c step=j4 attempt=1 prompt_hash=e2f91427aeef98707788656002a95c251a33a13b481a7052a943749f4d72e043
llm call failed call_id=c7b4e9579f10f step=j4 attempt=1 prompt_hash=40edf164293ce60521fb2bee311f3741eaff8b4b39498d8afefcb62580adb002
run status: failed
health answers: prepared
e1 state: rejected reasons: ['FIXTURE_MISS'] prepared: False
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py", line 50, in <module>
    print("e1 ladder.generator.model:", (item.get("ladder") or {}).get("generator", {}).get("model"))
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:36.920Z

The probe was wrong, not the product. Passing `LLM_FIXTURE_DIR` turns off the fallback to the recorded set, so the judge calls missed. I'll overlay the curated files on top of a copy of the recorded set, which matches how `FIXTURE_SET=curated` resolves, and make the printing robust to a missing ladder.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:38.457Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py",
 "old_string": "os.makedirs(mut_root)\nshutil.copytree(os.path.join(ARCH, \"tests\", \"fixtures\", \"llm\", \"curated\"), mut_dir)\np = os.path.join(mut_dir, E1_KEY + \".json\")",
 "new_string": "os.makedirs(mut_root)\nos.makedirs(mut_dir)\nsrc = os.path.join(ARCH, \"tests\", \"fixtures\", \"llm\")\nfor f in os.listdir(src):                       # the recorded set is the fallback for keys the curated set lacks (fixture.call)\n    if f.endswith(\".json\"):\n        shutil.copy(os.path.join(src, f), mut_dir)\nfor f in os.listdir(os.path.join(src, \"curated\")):   # the curated set wins for its own keys\n    if f.endswith(\".json\"):\n        shutil.copy(os.path.join(src, \"curated\", f), mut_dir)\np = os.path.join(mut_dir, E1_KEY + \".json\")"
}
````

### User / tool · 2026-11-02T21:07:38.558Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:40.174Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py",
 "old_string": "print(\"e1 ladder.generator.model:\", (item.get(\"ladder\") or {}).get(\"generator\", {}).get(\"model\"))",
 "new_string": "print(\"e1 ladder.generator.model:\", ((item.get(\"ladder\") or {}).get(\"generator\") or {}).get(\"model\"))"
}
````

### User / tool · 2026-11-02T21:07:40.277Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:42.839Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_branch.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2-branch.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-branch.out | cut -c1-400",
 "description": "Rerun failed-curated-item branch probe with overlay fixture set",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:07:44.087Z

**tool result**
````
exit=0
run status: failed
health answers: prepared
e1 state: rejected reasons: ['FIXTURE_MISS'] prepared: False
e1 ladder.generator.model: None
e1 extracted step:
{
 "label": "AI drafted a summary and picked a quote",
 "status": "pass",
 "why": "The AI read this record and proposed a one-line summary and a quote.",
 "reason_code": null,
 "rule": "row 4"
}
e1 extracted evidence.model: {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null, "prepared": false}
case-level extract step label: 'AI drafts a summary and a quote for each record' status: fail
case-level extract why: '1 record has no AI-made entry. The AI step failed on all three attempts, so this record has no AI-made entry.'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:55.165Z

The schema break did not isolate the branch. The schema failure triggers a second extract attempt with a different prompt hash, which misses the fixture, so the failure comes from the retry path and not from the prepared label logic. A cleaner branch is a summary that the code cannot trim to anything supported (`SUMMARY_NOT_IN_QUOTE`), which fails with no retry. I'll switch the mutation to that and rerun.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:55.967Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py",
 "old_string": "del d[\"output\"][\"summary\"]                      # schema now invalid for e1",
 "new_string": "d[\"output\"][\"summary\"] = \"Patient reported paralysis of the left leg and loss of bladder control.\"     # no clause is in the quote: code removes all of it (D-054)"
}
````

### User / tool · 2026-11-02T21:07:56.102Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:07:58.869Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_branch.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2-branch.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-branch.out | cut -c1-500",
 "description": "Rerun branch probe with unsupported summary mutation",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:08:00.172Z

**tool result**
````
exit=0
run status: ready
health answers: prepared
e1 state: rejected reasons: ['SUMMARY_NOT_IN_QUOTE'] prepared: True
e1 ladder.generator.model: hand-checked (qa)
e1 extracted step:
{
 "label": "AI drafted a summary and picked a quote",
 "status": "fail",
 "why": "removed from the summary: not in the quote: 'Patient reported paralysis of the left leg' removed from the summary: not in the quote: 'loss of bladder control' Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.",
 "reason_code": "SUMMARY_NOT_IN_QUOTE",
 "rule": "D-054"
}
e1 extracted evidence.model: {"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true}
case-level extract step label: 'Prepared summaries and quotes for each record, standing in for the AI draft' status: fail
case-level extract why: "1 record has no prepared entry. Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:19.934Z

The branch is reproduced. On a prepared item whose summary fails a code check, the item trace step is labelled "AI drafted a summary and picked a quote", its why text says "The AI's summary", and the evidence names `hand-checked (qa)`. That contradicts D-065 on a reachable path, although the shipped sample never reaches it. Next is the mutation spot-check on the new r2 code. I'll use a small script that asserts a single replacement and restores the file from `git show HEAD`, then `cmp` checks the restore.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:22.146Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/mutate_r2.py",
 "content": "\"\"\"T-177 r2 mutation helper (staff-engineer-reviewer). Works only inside the archive copy under artifacts/review-evidence.\nUsage: python -I mutate_r2.py apply <archive_dir> <relpath> <old_literal> <new_literal>\n       python -I mutate_r2.py restore <archive_dir> <relpath> <head_sha>\napply asserts the literal occurs exactly once (no silent no-op); restore re-extracts the file from git at the given sha.\"\"\"\nimport pathlib\nimport subprocess\nimport sys\n\nmode, arch, rel = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]\ntarget = arch / rel\nif mode == \"apply\":\n    old, new = sys.argv[4], sys.argv[5]\n    text = target.read_text()\n    n = text.count(old)\n    assert n == 1, f\"expected exactly one occurrence, found {n}\"\n    target.write_text(text.replace(old, new))\n    print(f\"applied to {rel}: 1 replacement\")\nelif mode == \"restore\":\n    sha = sys.argv[4]\n    data = subprocess.run([\"git\", \"-C\", \"/Users/arsis/zlayt-pm-project\", \"show\", f\"{sha}:{rel}\"], check=True, capture_output=True).stdout\n    target.write_bytes(data)\n    print(f\"restored {rel} from {sha}\")\nelse:\n    raise SystemExit(\"unknown mode\")\n"
}
````

### User / tool · 2026-11-02T21:08:22.242Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/mutate_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:25.213Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && A=$PWD/$EV/archive && SHA=$(cat $EV/archive-source-sha.txt) && PY=.venv/bin/python && \\\necho \"=== M1: models_for prepared forced off (present.py) ===\" && $PY -I $EV/mutate_r2.py apply $A app/backend/present.py 'prepared = bool(gens) and all(AU.is_prepared(c.get(\"recorded_from\")) for c in gens)' 'prepared = False' && (cd $A && $PY -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -8 | tee /dev/stderr >/dev/null; cd $A && $PY -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider > $PWD/../$(basename $EV)/mut-M1-unit.out 2>&1; tail -3 $PWD/../$(basename $EV)/mut-M1-unit.out) ; $PY -I $EV/mutate_r2.py restore $A app/backend/present.py $SHA && git show $SHA:app/backend/present.py | cmp - $A/app/backend/present.py && echo \"M1 restored: cmp identical\"",
 "description": "Apply mutation M1 to models_for, run unit tests, restore and verify",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:08:25.273Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to /Users/arsis/zlayt-pm-project/../$)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:26.763Z

The guard rejected a redirect built from `$PWD/../`. I'll rerun the mutation in separate steps using absolute evidence paths and no `/dev/stderr` redirects.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:27.482Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r2/mutate_r2.py apply /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive app/backend/present.py 'prepared = bool(gens) and all(AU.is_prepared(c.get(\"recorded_from\")) for c in gens)' 'prepared = False'",
 "description": "Apply mutation M1 to models_for in the archive copy"
}
````

### User / tool · 2026-11-02T21:08:27.610Z

**tool result**
````
applied to app/backend/present.py: 1 replacement
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:28.124Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -12",
 "description": "Run unit provenance tests against mutant M1",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:08:31.949Z

**tool result**
````
E       assert ('AI drafts' not in 'AI drafts a... each record'
E         
E         'AI drafts' is contained here:
E         ? ^
E           AI drafts a summary and a quote for each record
E         ? ^^^^^ +++++)

tests/unit/test_prepared_provenance.py:148: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_prepared_provenance.py::test_curated_models_never_name_a_drafting_model
FAILED tests/unit/test_prepared_provenance.py::test_curated_case_level_trace_does_not_say_an_ai_drafted
2 failed, 8 passed in 3.46s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:33.189Z

Mutant M1 fails 2 of 10 unit tests, so that guard is covered. I'll restore the file from `git show` and `cmp` it against HEAD. Then I'll apply M2 to the judge panel's prepared branch and run the e2e judge tests.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:34.153Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && A=$PWD/$EV/archive && SHA=$(cat $EV/archive-source-sha.txt) && .venv/bin/python -I $EV/mutate_r2.py restore $A app/backend/present.py $SHA && git show $SHA:app/backend/present.py | cmp - $A/app/backend/present.py && echo \"M1 restored: identical to $SHA\" && .venv/bin/python -I $EV/mutate_r2.py apply $A app/frontend/judges.js 'const prepared = !!(d && d.models && d.models.generator_prepared);' 'const prepared = false;'",
 "description": "Restore M1 from HEAD, verify identical, apply M2 to judges.js"
}
````

### User / tool · 2026-11-02T21:08:34.452Z

**tool result**
````
restored app/backend/present.py from 4671eee820334400619dafc00cf11a53e0cb30de
M1 restored: identical to 4671eee820334400619dafc00cf11a53e0cb30de
applied to app/frontend/judges.js: 1 replacement
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:35.855Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && env -u E2E_BASE_URL -u ZLAYT_DB E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -q -p no:cacheprovider -k \"judge or surface\" 2>&1 | tail -15",
 "description": "Run e2e judge and surface tests against mutant M2",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:08:41.347Z

**tool result**
````
>       assert "claude-sonnet-5-5" not in line and "Drafted by" not in line, line
E       AssertionError: Drafted by hand-checked (qa), checked by claude-haiku-5-5 (a different model, so it does not grade its own work).
E       assert ('claude-sonnet-5-5' not in 'Drafted by ...s own work).'
E         
E         'claude-sonnet-5-5' is contained here:
E            own work). and 'Drafted by' not in 'Drafted by ...s own work).'
E         
E         'Drafted by' is contained here:
E           Drafted by hand-checked (qa), checked by claude-haiku-5-5 (a different model, so it does not grade its own work).
E         ? ++++++++++)

tests/e2e/test_demo_provenance.py:175: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_demo_provenance.py::test_curated_judge_panel_does_not_name_a_drafting_model
1 failed, 2 passed, 4 deselected in 4.44s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:43.410Z

Mutant M2 fails the judge-panel e2e test, and the failing output shows the panel rendering "Drafted by hand-checked (qa)". I'll restore `judges.js` and verify it matches HEAD, then check how the export renders provenance, since the export is the one surface the probe could not reach without an accepted item.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:44.307Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && A=$PWD/$EV/archive && SHA=$(cat $EV/archive-source-sha.txt) && .venv/bin/python -I $EV/mutate_r2.py restore $A app/frontend/judges.js $SHA && git show $SHA:app/frontend/judges.js | cmp - $A/app/frontend/judges.js && echo \"M2 restored: identical to $SHA\" && echo \"=== export provenance rendering ===\" && grep -n \"provenance\\|generator_model\\|prepared\" $A/app/backend/export.py | cut -c1-260 | head -30",
 "description": "Restore judges.js from HEAD and grep export provenance"
}
````

### User / tool · 2026-11-02T21:08:44.566Z

**tool result**
````
restored app/frontend/judges.js from 4671eee820334400619dafc00cf11a53e0cb30de
M2 restored: identical to 4671eee820334400619dafc00cf11a53e0cb30de
=== export provenance rendering ===
50:          "temporal_after_gap", "new_onset", "accident_date_inconsistency", "accident_date_provenance"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:46.066Z

`export.py` does not render provenance, so the export surface is the API's `provenance` object. I'll check which export routes exist and whether any text output (letter or download) carries the model name.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:47.193Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && grep -n '\"/api/cases/{token}/export\\|export' app/backend/api.py | grep -i \"get\\|post\\|route\\|def \" | cut -c1-220 | head -12; echo \"=== provenance in text outputs ===\"; grep -rn \"provenance\\|generator_model\\|Drafted\\|drafted by\" app/backend/export.py app/backend/letter*.py app/backend/*export*.py 2>/dev/null | cut -c1-240 | head -20; echo \"=== api.py provenance dict ===\"; grep -n \"provenance\" app/backend/api.py | cut -c1-240",
 "description": "List export routes and provenance rendering in text outputs"
}
````

### User / tool · 2026-11-02T21:08:47.301Z

**tool result**
````
1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
602:    @app.get("/api/cases/{token}/export")
603:    def export(token: str, style: str = None):
604:        from app.backend import export_routes as XR
=== provenance in text outputs ===
app/backend/export.py:50:          "temporal_after_gap", "new_onset", "accident_date_inconsistency", "accident_date_provenance"]
app/backend/export.py:50:          "temporal_after_gap", "new_onset", "accident_date_inconsistency", "accident_date_provenance"]
=== api.py provenance dict ===
624:            ex["provenance"] = {"generator_model": mm["generator"], "judge_model": mm["judge"], "generator_prepared": mm["generator_prepared"], "backend": backend(),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:48.703Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && sed -n '1,60p' app/backend/export_routes.py | cut -c1-260 | grep -n \"def \\|style\\|provenance\\|model\\|md\\|txt\\|docx\\|html\" | head -40; echo \"=== api.py export handler lines 602-640 ===\"; sed -n '602,640p' app/backend/api.py | cut -c1-240",
 "description": "Read export route styles and provenance rendering"
}
````

### User / tool · 2026-11-02T21:08:48.814Z

**tool result**
````
19:def set_case_loader(fn):
24:def _not_found():
28:def export_payload(token: str, case: dict, now: datetime = None, style: str = None) -> dict:
31:    out = export.build_export(case, style)
53:def invalid_style_message() -> str:
54:    return "The letter style must be 'standard' or 'oneline'."
57:def blocked_message(e) -> str:
=== api.py export handler lines 602-640 ===
    @app.get("/api/cases/{token}/export")
    def export(token: str, style: str = None):
        from app.backend import export_routes as XR
        if style not in (None, *export_mod.STYLES):          # T-121: ?style=oneline | standard
            raise ApiError(422, "invalid_style", XR.invalid_style_message())
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case, style=style)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": present.rejected_count(c, token)}
            mm = present.models_for(c, token, config_models())
            ex["provenance"] = {"generator_model": mm["generator"], "judge_model": mm["judge"], "generator_prepared": mm["generator_prepared"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}/trace")
    def item_trace(token: str, item_id: str):
        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
        c = conn()
        try:
            get_case(c, token)
            try:
                return trace.item_trace(c, token, item_id, full=local_mode())
            except trace.UnknownItem:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:53.200Z

The export JSON carries `provenance.prompt_versions` built from every call's prompt version, so a curated run would list `extract_v1` there. The export returns 422 until items are accepted, so I'll write a short probe that accepts every reachable item on the curated set, exports, and prints the whole provenance block plus any model or AI wording.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:08:58.498Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_export.py",
 "content": "\"\"\"T-177 r2 export probe (staff-engineer-reviewer). Curated set (prepared) and recorded set (control), archive copy only.\nAccepts every entry, amount and flag the API lists as open (a POST per item, status recorded), then GET /export and reports the\nprovenance block and any model or AI-draft wording in the whole export payload.\nUsage: python -I probe_r2_export.py <archive_dir> <scratch_dir>\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\n\nARCH, SCRATCH = sys.argv[1], sys.argv[2]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nWORDS = [\"claude-sonnet\", \"claude-haiku\", \"hand-checked\", \"Drafted\", \"drafted by\", \"AI draft\", \"AI-made\", \"AI drafted\", \"prepared\", \"Prepared\", \"extract_v1\", \"prompt\"]\n\n\ndef client(db, fixture_set):\n    os.environ[\"LLM_BACKEND\"] = \"fixture\"\n    os.environ[\"ZLAYT_MODE\"] = \"local\"\n    for k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"LLM_FIXTURE_DIR\", \"FIXTURE_SET\"):\n        os.environ.pop(k, None)\n    if fixture_set:\n        os.environ[\"FIXTURE_SET\"] = fixture_set\n    if os.path.exists(db):\n        os.remove(db)\n    return TestClient(create_app(db, static_dir=os.path.join(ARCH, \"app\", \"frontend\")), client=(\"127.0.0.1\", 50000))\n\n\ndef run(c):\n    tok = c.post(\"/api/cases\", json={\"sample\": True, \"title\": \"export probe\"}).json()[\"token\"]\n    c.post(f\"/api/cases/{tok}/run\", json={})\n    for _ in range(480):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    return tok, s[\"status\"]\n\n\ndef accept_all(c, tok):\n    case = c.get(f\"/api/cases/{tok}\").json()\n    rows = []\n    for key in (\"entries\", \"amounts\", \"flags\"):\n        for x in case.get(key, []):\n            if x.get(\"review_status\") in (\"accepted\", \"dismissed\", \"rejected\") or x.get(\"state\") == \"rejected\":\n                continue\n            r = c.post(f\"/api/cases/{tok}/items/{x['id']}/review\", json={\"action\": \"accept\"})\n            rows.append((x[\"id\"], r.status_code, (r.json() if r.status_code != 200 else {}).get(\"error\", {}).get(\"code\") if r.status_code != 200 else \"ok\"))\n    return rows\n\n\ndef report(tag, c, tok, out):\n    rows = accept_all(c, tok)\n    out.append(f\"[{tag}] accept calls: {len(rows)}; statuses: {sorted(set(r[1] for r in rows))}\")\n    for r in rows:\n        if r[1] != 200:\n            out.append(f\"  [{tag}] accept {r[0]} -> {r[1]} {r[2]}\")\n    e = c.get(f\"/api/cases/{tok}/export\")\n    out.append(f\"[{tag}] GET export -> {e.status_code}\")\n    if e.status_code != 200:\n        out.append(f\"  body: {e.text[:300]}\")\n        return\n    j = e.json()\n    out.append(f\"[{tag}] provenance: \" + json.dumps(j.get(\"provenance\"), ensure_ascii=False))\n    text = json.dumps(j, ensure_ascii=False)\n    for w in WORDS:\n        hits = [text[max(0, m.start() - 60): m.end() + 40] for m in re.finditer(re.escape(w), text)]\n        if hits:\n            out.append(f\"[{tag}] word {w!r}: {len(hits)} hit(s); first: ...{hits[0]}...\")\n\n\ndef main():\n    out = []\n    c = client(os.path.join(SCRATCH, \"export_curated.sqlite\"), \"curated\")\n    tok, st = run(c)\n    out.append(f\"[curated] run status={st}\")\n    report(\"curated\", c, tok, out)\n    c2 = client(os.path.join(SCRATCH, \"export_recorded.sqlite\"), None)\n    tok2, st2 = run(c2)\n    out.append(f\"[recorded] run status={st2}\")\n    report(\"recorded\", c2, tok2, out)\n    print(\"\\n\".join(out))\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:08:58.594Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_export.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:00.968Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_export.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2-export.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-export.out | cut -c1-420 | head -60",
 "description": "Run export probe on curated and recorded sets",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:09:02.642Z

**tool result**
````
exit=0
[curated] run status=ready
[curated] accept calls: 23; statuses: [200]
[curated] GET export -> 200
[curated] provenance: {"generator_model": "hand-checked (qa)", "judge_model": "claude-haiku-5-5", "generator_prepared": true, "backend": "fixture", "recorded_from": "curated", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", "judge_conflict_v6", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated] word 'claude-haiku': 1 hit(s); first: ...": {"generator_model": "hand-checked (qa)", "judge_model": "claude-haiku-5-5", "generator_prepared": true, "back...
[curated] word 'hand-checked': 1 hit(s); first: ...sed": 0, "rejected": 0}, "provenance": {"generator_model": "hand-checked (qa)", "judge_model": "claude-haiku-5-5...
[curated] word 'prepared': 1 hit(s); first: ...hecked (qa)", "judge_model": "claude-haiku-5-5", "generator_prepared": true, "backend": "fixture", "recorded...
[curated] word 'extract_v1': 1 hit(s); first: ...d_from": "curated", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", ...
[curated] word 'prompt': 1 hit(s); first: ... "fixture", "recorded_from": "curated", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "...
[recorded] run status=ready
[recorded] accept calls: 23; statuses: [200]
[recorded] GET export -> 200
[recorded] provenance: {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "backend": "fixture", "recorded_from": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", "judge_conflict_v6", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[recorded] word 'claude-sonnet': 1 hit(s); first: ...sed": 0, "rejected": 0}, "provenance": {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5"...
[recorded] word 'claude-haiku': 1 hit(s); first: ...": {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "bac...
[recorded] word 'prepared': 1 hit(s); first: ...-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "backend": "fixture", "recorde...
[recorded] word 'extract_v1': 1 hit(s); first: ...rom": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", ...
[recorded] word 'prompt': 1 hit(s); first: ...ixture", "recorded_from": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "...
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:12.386Z

The export on the curated set names `hand-checked (qa)` and `generator_prepared: true`, and its whole text has no drafter wording. The gap is `prompt_versions`, which still lists `extract_v1` and `flags_v1` for the prepared answers. That is the round-1 F5 residual at the payload level, and I'll keep it as a nit. For visible text I'll render the curated page on my own server and read the rendered banner, badge, judge panel, Why ladder and audit drawer. First I'll check whether `app/main.py` spawns child processes, so I know which PID to stop.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:13.036Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && cat app/main.py | head -60 | cut -c1-200; echo \"--- reload/subprocess grep ---\"; grep -rn \"reload\\|subprocess\\|workers\" app/main.py | head",
 "description": "Read app entry point to see how the server starts"
}
````

### User / tool · 2026-11-02T21:09:13.167Z

**tool result**
````
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
--- reload/subprocess grep ---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:18.439Z

The server is a single uvicorn process with no reloader, so the Popen PID is the listener. I'll still confirm the listener with `lsof` before stopping it. The render script will start its own server on a free loopback port, read the rendered badge, tooltip, banner and judge panel, scan the whole document, save a screenshot, then stop only its own listener.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:27.117Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/render_r2.py",
 "content": "\"\"\"T-177 r2 render probe (staff-engineer-reviewer). Starts its OWN app server on a free loopback port from the archive copy\n(curated set, then recorded set), reads the rendered badge, badge tooltip, AI banner, judge panel and a whole-document scan,\nsaves screenshots under the evidence dir, then stops only the listener PID it started (verified with lsof). Never touches :7860.\nUsage: python -I render_r2.py <archive_dir> <evidence_dir> <scratch_dir>\"\"\"\nimport json\nimport os\nimport re\nimport socket\nimport subprocess\nimport sys\nimport time\nimport urllib.request\n\nARCH, EVID, SCRATCH = sys.argv[1], sys.argv[2], sys.argv[3]\nsys.path.insert(0, ARCH)\n\nfrom playwright.sync_api import sync_playwright  # noqa: E402\n\nBAD = [\"claude-sonnet\", \"Drafted by AI\", \"drafted by AI\", \"AI draft\", \"recorded AI answers\", \"The AI's own answers\", \"first AI\", \"AI's drafts\"]\n\n\ndef free_port():\n    s = socket.socket()\n    s.bind((\"127.0.0.1\", 0))\n    p = s.getsockname()[1]\n    s.close()\n    return p\n\n\ndef listeners(port):\n    r = subprocess.run([\"/usr/sbin/lsof\", \"-iTCP:%d\" % port, \"-sTCP:LISTEN\", \"-n\", \"-P\", \"-t\"], capture_output=True, text=True)\n    return sorted({int(x) for x in r.stdout.split() if x.strip().isdigit()})\n\n\ndef start(fixture_set, tag):\n    port = free_port()\n    env = dict(os.environ, PORT=str(port), HOST=\"127.0.0.1\", ZLAYT_MODE=\"local\", LLM_BACKEND=\"fixture\", ZLAYT_DB=os.path.join(SCRATCH, \"render_%s.sqlite\" % tag))\n    for k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"LLM_FIXTURE_DIR\", \"FIXTURE_SET\"):\n        env.pop(k, None)\n    if fixture_set:\n        env[\"FIXTURE_SET\"] = fixture_set\n    if os.path.exists(env[\"ZLAYT_DB\"]):\n        os.remove(env[\"ZLAYT_DB\"])\n    log = open(os.path.join(SCRATCH, \"render_%s.log\" % tag), \"w\")\n    proc = subprocess.Popen([sys.executable, \"-m\", \"app.main\"], cwd=ARCH, env=env, stdout=log, stderr=subprocess.STDOUT)\n    base = \"http://127.0.0.1:%d\" % port\n    for _ in range(120):\n        try:\n            urllib.request.urlopen(base + \"/api/health\", timeout=1).read()\n            break\n        except Exception:\n            if proc.poll() is not None:\n                raise SystemExit(\"server exited early; see render log\")\n            time.sleep(0.25)\n    else:\n        proc.kill()\n        raise SystemExit(\"server did not start\")\n    pids = listeners(port)\n    print(f\"[{tag}] own server port={port} popen_pid={proc.pid} listener_pids={pids}\")\n    return base, port, proc, pids\n\n\ndef api(base, method, path, body=None):\n    req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={\"Content-Type\": \"application/json\"})\n    with urllib.request.urlopen(req, timeout=60) as r:\n        raw = r.read()\n        return json.loads(raw) if raw else None\n\n\ndef make_case(base):\n    tok = api(base, \"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"Rivera v. Northgate (MVA 2026-01)\"})[\"token\"]\n    api(base, \"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(480):\n        s = api(base, \"GET\", f\"/api/cases/{tok}/status\")\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    return tok, s[\"status\"]\n\n\ndef scan(page):\n    return page.evaluate(\"\"\"() => { const out = [document.documentElement.textContent];\n      document.querySelectorAll('[title],[aria-label]').forEach(e => out.push(e.getAttribute('title') || '', e.getAttribute('aria-label') || ''));\n      return out.join(' | '); }\"\"\")\n\n\ndef render(base, tok, tag, pw, report):\n    b = pw.chromium.launch()\n    pg = b.new_context(viewport={\"width\": 1280, \"height\": 900}).new_page()\n    try:\n        pg.goto(f\"{base}/#/case/{tok}\")\n        pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n        badge = pg.locator(\"#badge\")\n        report.append(f\"[{tag}] badge text: {badge.inner_text()!r}\")\n        report.append(f\"[{tag}] badge tooltip (title attr): {badge.get_attribute('title')!r}\")\n        report.append(f\"[{tag}] banner-ai text: {pg.locator('#banner-ai').inner_text()!r}\")\n        jp = pg.get_by_test_id(\"judge-panel\")\n        jp.get_by_test_id(\"judge-summary\").wait_for()\n        if not jp.locator(\"details.zj-det\").evaluate(\"d => d.open\"):\n            jp.get_by_test_id(\"judge-summary\").click()\n        jp.get_by_test_id(\"judge-totals\").wait_for()\n        report.append(f\"[{tag}] judge-label: {jp.get_by_test_id('judge-label').inner_text()!r}\")\n        report.append(f\"[{tag}] judge-model-line: {jp.get_by_test_id('judge-model-line').inner_text()!r}\")\n        report.append(f\"[{tag}] judge-totals: {jp.get_by_test_id('judge-totals').inner_text()!r}\")\n        jp.screenshot(path=os.path.join(EVID, f\"render-{tag}-judge-panel.png\"))\n        pg.screenshot(path=os.path.join(EVID, f\"render-{tag}-page.png\"))\n        text = scan(pg)\n        hits = []\n        for w in BAD:\n            for m in re.finditer(re.escape(w), text):\n                hits.append((w, text[max(0, m.start() - 50): m.end() + 40]))\n        report.append(f\"[{tag}] whole-document scan (text + title + aria-label): {len(hits)} hit(s) for {BAD}\")\n        for w, ctx in hits[:8]:\n            report.append(f\"   hit {w!r}: ...{ctx}...\")\n    finally:\n        b.close()\n\n\ndef main():\n    report = []\n    with sync_playwright() as pw:\n        for fixture_set, tag in ((\"curated\", \"curated\"), (None, \"recorded\")):\n            base, port, proc, pids = start(fixture_set, tag)\n            try:\n                tok, st = make_case(base)\n                report.append(f\"[{tag}] case run status={st} port={port}\")\n                render(base, tok, tag, pw, report)\n            finally:\n                # stop only the listener this run started (the Popen pid); verify it is ours before killing\n                mine = [p for p in listeners(port) if p == proc.pid or p in pids]\n                if mine and proc.pid in mine:\n                    proc.terminate()\n                    try:\n                        proc.wait(timeout=10)\n                    except subprocess.TimeoutExpired:\n                        proc.kill()\n                        proc.wait(timeout=10)\n                report.append(f\"[{tag}] stopped popen_pid={proc.pid}; listeners on port {port} now: {listeners(port)}\")\n    print(\"\\n\".join(report))\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:09:27.212Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/render_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:29.889Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/render_r2.py \"$PWD/$EV/archive\" \"$PWD/$EV\" \"$SCR\" > $EV/render-r2.out 2>&1; echo \"exit=$?\"; cut -c1-500 $EV/render-r2.out; echo \"--- shared 7860 listener still there? ---\"; lsof -iTCP:7860 -sTCP:LISTEN -n -P | tail -1",
 "description": "Render curated and recorded pages on own servers and read surfaces",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:09:34.171Z

**tool result**
````
exit=0
[curated] own server port=54001 popen_pid=52291 listener_pids=[52291]
[recorded] own server port=54056 popen_pid=52392 listener_pids=[52392]
[curated] case run status=ready port=54001
[curated] badge text: 'Demo: sample answers prepared by our team'
[curated] badge tooltip (title attr): 'Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.'
[curated] banner-ai text: 'In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item'
[curated] judge-label: 'AI quality checks. This shows how a second AI model checked the answers our team prepared for this demo. It is not a verdict on the case, the care or the claim, and it does not replace your review.'
[curated] judge-model-line: 'Prepared by our team (not by an AI model), checked by claude-haiku-5-5.'
[curated] judge-totals: '19\nitems checked by AI\n19\nagreed with the draft\n0\nAI objected\n0\ncould not decide\n0\nunavailable\n0\nyou accepted despite an objection'
[curated] whole-document scan (text + title + aria-label): 10 hit(s) for ['claude-sonnet', 'Drafted by AI', 'drafted by AI', 'AI draft', 'recorded AI answers', "The AI's own answers", 'first AI', "AI's drafts"]
   hit 'AI draft': ...s and quotes for each record, standing in for the AI draftPrepared answerPassedThe prepared answer...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Austin EMS r...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Central ER d...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Dr. Alvarez,...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Capital PT, ...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Capital PT, ...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Capital PT, ...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Hill Country...
[curated] stopped popen_pid=52291; listeners on port 54001 now: []
[recorded] case run status=ready port=54056
[recorded] badge text: 'Demo: recorded AI answers'
[recorded] badge tooltip (title attr): 'This demo replays recorded AI answers for its sample cases. Nothing you paste is sent to an AI service.'
[recorded] banner-ai text: 'Summaries and flags are drafted by AI and checked by code; you decide every item'
[recorded] judge-label: "AI quality checks. This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review."
[recorded] judge-model-line: 'Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5 (a different model, so it does not grade its own work).'
[recorded] judge-totals: '20\nitems checked by AI\n20\nagreed with the draft\n0\nAI objected\n0\ncould not decide\n0\nunavailable\n0\nyou accepted despite an objection'
[recorded] whole-document scan (text + title + aria-label): 18 hit(s) for ['claude-sonnet', 'Drafted by AI', 'drafted by AI', 'AI draft', 'recorded AI answers', "The AI's own answers", 'first AI', "AI's drafts"]
   hit 'claude-sonnet': ...m, and it does not replace your review.Drafted by claude-sonnet-5-5, checked by claude-haiku-5-5 (a dif...
   hit 'Drafted by AI': ...own decision. |  |  | Why the export is blocked | Drafted by AI |  |  | Show full excerpt: Austin EMS r...
   hit 'Drafted by AI': ...Change quote: Austin EMS run report, 2026-01-09 | Drafted by AI |  |  | Show full excerpt: Central ER d...
   hit 'Drafted by AI': ...1): Dr. Alvarez, primary care, January 16, 2026 | Drafted by AI |  |  | Show full excerpt: Dr. Alvarez,...
   hit 'Drafted by AI': ...ge quote: Dr. Alvarez, primary care, 2026-01-16 | Drafted by AI |  |  | Show full excerpt: Capital PT, ...
   hit 'Drafted by AI': ...ote: Capital PT, initial evaluation, 2026-01-23 | Drafted by AI |  |  | Show full excerpt: Capital PT, ...
   hit 'Drafted by AI': ...| Change quote: Capital PT, visit 8, 2026-02-20 | Drafted by AI |  |  | Show full excerpt: Capital PT, ...
   hit 'Drafted by AI': ...ntry Pain Management, new patient, May 18, 2026 | Drafted by AI |  |  | Show full excerpt: Hill Country...
[recorded] stopped popen_pid=52392; listeners on port 54056 now: []
--- shared 7860 listener still there? ---
Python  86899 arsis    9u  IPv4 0x89944c6bbeb1c380      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:43.250Z

The rendered curated page is clean on every surface the user named. The tooltip matches D-065 exactly, the banner names the second AI model, the judge line says "Prepared by our team (not by an AI model)", and the only AI-draft string is the D-065 phrase. The recorded control still says "Drafted by claude-sonnet-5-5". One possible gap is the banner fallback at `app.js:10`, which shows "drafted by AI" text while `/api/health` has not answered. I'll test that by delaying `/api/health` on my own server.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:47.587Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py",
 "content": "\"\"\"T-177 r2 banner-fallback probe (staff-engineer-reviewer). Curated set, own server (started and stopped here, listener verified).\nDelays /api/health by 4 s, opens a prepared case by URL, and samples #banner-ai and #badge while health has not answered.\napp.js:10 falls back to 'Summaries and flags are drafted by AI...' when h is null. Reports what a reader sees in that window.\nUsage: python -I race_r2.py <archive_dir> <evidence_dir> <scratch_dir>\"\"\"\nimport sys\nimport time\n\nARCH, EVID, SCRATCH = sys.argv[1], sys.argv[2], sys.argv[3]\nsys.path.insert(0, ARCH)\nsys.path.insert(0, EVID)\n\nimport render_r2 as R  # noqa: E402  (same directory as this script: helpers only, main() not run)\nfrom playwright.sync_api import sync_playwright  # noqa: E402\n\n\ndef main():\n    base, port, proc, pids = R.start(\"curated\", \"race\")\n    out = []\n    try:\n        tok, st = R.make_case(base)\n        out.append(f\"[race] case run status={st} port={port}\")\n        with sync_playwright() as pw:\n            b = pw.chromium.launch()\n            pg = b.new_context(viewport={\"width\": 1280, \"height\": 900}).new_page()\n            health_seen = {\"n\": 0}\n\n            def slow_health(route):\n                health_seen[\"n\"] += 1\n                time.sleep(4)                      # /api/health answers only after 4 s\n                route.continue_()\n            pg.route(\"**/api/health\", slow_health)\n            pg.goto(f\"{base}/#/case/{tok}\", wait_until=\"domcontentloaded\")\n            t0 = time.monotonic()\n            seen = []\n            while time.monotonic() - t0 < 3.5:\n                try:\n                    ai = pg.locator(\"#banner-ai\")\n                    if ai.count() and ai.is_visible():\n                        seen.append((round(time.monotonic() - t0, 2), ai.inner_text(), pg.locator(\"#badge\").inner_text()))\n                        if len(seen) >= 3:\n                            break\n                except Exception as e:                      # page still building: record and keep polling\n                    seen.append((round(time.monotonic() - t0, 2), \"ERR \" + type(e).__name__, \"\"))\n                time.sleep(0.2)\n            out.append(f\"[race] health requests seen while delayed: {health_seen['n']}\")\n            for t, txt, badge in seen:\n                out.append(f\"[race] t={t}s banner-ai={txt!r} badge={badge!r}\")\n            pg.wait_for_timeout(5000)\n            out.append(f\"[race] after health answered: banner-ai={pg.locator('#banner-ai').inner_text()!r} badge={pg.locator('#badge').inner_text()!r}\")\n            b.close()\n    finally:\n        mine = [p for p in R.listeners(port) if p == proc.pid]\n        if mine:\n            proc.terminate()\n            try:\n                proc.wait(timeout=10)\n            except Exception:\n                proc.kill()\n                proc.wait(timeout=10)\n        out.append(f\"[race] stopped popen_pid={proc.pid}; listeners on port {port} now: {R.listeners(port)}\")\n    print(\"\\n\".join(out))\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:09:47.691Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:09:50.919Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/race_r2.py \"$PWD/$EV/archive\" \"$PWD/$EV\" \"$SCR\" > $EV/race-r2.out 2>&1; echo \"exit=$?\"; cut -c1-400 $EV/race-r2.out",
 "description": "Run banner-fallback race probe with delayed health on own server",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:10:02.303Z

**tool result**
````
exit=0
[race] own server port=54205 popen_pid=52754 listener_pids=[52754]
[race] case run status=ready port=54205
[race] health requests seen while delayed: 1
[race] after health answered: banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] stopped popen_pid=52754; listeners on port 54205 now: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:04.524Z

The sample loop recorded nothing, because `time.sleep(4)` inside the route handler blocks Playwright's sync event loop. I'll hold the health request instead and release it from the polling loop after a few seconds.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:07.327Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py",
 "old_string": "            health_seen = {\"n\": 0}\n\n            def slow_health(route):\n                health_seen[\"n\"] += 1\n                time.sleep(4)                      # /api/health answers only after 4 s\n                route.continue_()\n            pg.route(\"**/api/health\", slow_health)\n            pg.goto(f\"{base}/#/case/{tok}\", wait_until=\"domcontentloaded\")\n            t0 = time.monotonic()\n            seen = []\n            while time.monotonic() - t0 < 3.5:\n                try:\n                    ai = pg.locator(\"#banner-ai\")\n                    if ai.count() and ai.is_visible():\n                        seen.append((round(time.monotonic() - t0, 2), ai.inner_text(), pg.locator(\"#badge\").inner_text()))\n                        if len(seen) >= 3:\n                            break\n                except Exception as e:                      # page still building: record and keep polling\n                    seen.append((round(time.monotonic() - t0, 2), \"ERR \" + type(e).__name__, \"\"))\n                time.sleep(0.2)\n            out.append(f\"[race] health requests seen while delayed: {health_seen['n']}\")",
 "new_string": "            held = []\n\n            def hold_health(route):                 # park the request; release it from the poll loop (a blocking sleep here would freeze Playwright)\n                held.append(route)\n            pg.route(\"**/api/health\", hold_health)\n            pg.goto(f\"{base}/#/case/{tok}\", wait_until=\"domcontentloaded\")\n            t0 = time.monotonic()\n            seen = []\n            released = False\n            while time.monotonic() - t0 < 6.0:\n                if not released and time.monotonic() - t0 >= 3.0:\n                    for r in held:\n                        r.continue_()\n                    released = True\n                try:\n                    ai = pg.locator(\"#banner-ai\")\n                    if ai.count() and ai.is_visible():\n                        seen.append((round(time.monotonic() - t0, 2), ai.inner_text(), pg.locator(\"#badge\").inner_text(), released))\n                except Exception as e:                  # page still building: record and keep polling\n                    seen.append((round(time.monotonic() - t0, 2), \"ERR \" + type(e).__name__, \"\", released))\n                pg.wait_for_timeout(200)\n            health_seen = {\"n\": len(held)}\n            out.append(f\"[race] health requests parked before release: {health_seen['n']}; released at t=3.0s\")"
}
````

### User / tool · 2026-11-02T21:10:07.438Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:10.075Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/race_r2.py \"$PWD/$EV/archive\" \"$PWD/$EV\" \"$SCR\" > $EV/race-r2.out 2>&1; echo \"exit=$?\"; cut -c1-400 $EV/race-r2.out",
 "description": "Rerun banner race probe with held health request",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:10:18.346Z

**tool result**
````
exit=1
[race] own server port=54304 popen_pid=53030 listener_pids=[53030]
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py", line 67, in <module>
    main()
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py", line 48, in main
    for t, txt, badge in seen:
        ^^^^^^^^^^^^^
ValueError: too many values to unpack (expected 3)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:21.254Z

The tuple now has four fields, so the unpack needs updating. The `finally` block stops the server, and I'll verify that the port is closed.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:22.130Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py",
 "old_string": "            for t, txt, badge in seen:\n                out.append(f\"[race] t={t}s banner-ai={txt!r} badge={badge!r}\")",
 "new_string": "            for t, txt, badge, was_released in seen:\n                out.append(f\"[race] t={t}s released={was_released} banner-ai={txt!r} badge={badge!r}\")"
}
````

### User / tool · 2026-11-02T21:10:22.232Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/race_r2.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:25.620Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/race_r2.py \"$PWD/$EV/archive\" \"$PWD/$EV\" \"$SCR\" > $EV/race-r2.out 2>&1; echo \"exit=$?\"; cut -c1-420 $EV/race-r2.out; echo \"--- listeners on the race port range check (any app listeners left from this run?) ---\"; ps -axo pid,command | grep \"app.main\" | grep -v grep | head -5",
 "description": "Rerun banner race probe and check for leftover app processes",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:10:38.817Z

**tool result**
````
exit=0
[race] own server port=54440 popen_pid=53689 listener_pids=[53689]
[race] case run status=ready port=54440
[race] health requests parked before release: 1; released at t=3.0s
[race] t=3.29s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=3.5s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=3.71s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=3.91s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=4.12s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=4.33s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=4.53s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=4.74s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=4.95s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=5.15s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=5.36s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=5.56s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=5.77s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] t=5.98s released=True banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] after health answered: banner-ai='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' badge='Demo: sample answers prepared by our team'
[race] stopped popen_pid=53689; listeners on port 54440 now: []
--- listeners on the race port range check (any app listeners left from this run?) ---
23429 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
37589 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
52326 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
52906 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
86897 bash -c LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=artifacts/tmp/app.sqlite3 .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:45.566Z

The banner stayed hidden until health answered, so the fallback text never showed in this run. The race is not reproduced, and I'll drop it. The process list also shows four other `app.main` processes. Before I touch anything I'll identify which PIDs are mine by their working directory and listening port, since my servers ran from the archive copy.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:46.344Z

**tool call — Bash**
````
{
 "command": "for p in 23429 37589 52326 52906 86897 86899; do echo \"== PID $p ==\"; ps -o pid,ppid,etime,command -p $p | tail -1 | cut -c1-200; lsof -a -p $p -d cwd -Fn 2>/dev/null | grep \"^n\" | head -1; lsof -a -p $p -iTCP -sTCP:LISTEN -n -P 2>/dev/null | tail -n +2 | head -2; done",
 "description": "Identify app server PIDs by cwd and listening port"
}
````

### User / tool · 2026-11-02T21:10:47.173Z

**tool result**
````
== PID 23429 ==
23429     1 06:08:20 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
n/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t155r2/wt
Python  23429 arsis    9u  IPv4 0xd59ea69d8669b87d      0t0  TCP 127.0.0.1:62204 (LISTEN)
== PID 37589 ==
37589     1 05:11:36 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
n/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r3a
Python  37589 arsis    9u  IPv4 0xbf41849bbd9bed2e      0t0  TCP 127.0.0.1:60964 (LISTEN)
== PID 52326 ==
52326 52324   01:16 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
n/Users/arsis/zlayt-pm-project
Python  52326 arsis    9u  IPv4 0xe5bacb39aa628a5c      0t0  TCP 127.0.0.1:54005 (LISTEN)
== PID 52906 ==
52906     1   00:45 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
n/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/run2/clone-34h6/zlayt
Python  52906 arsis    9u  IPv4 0xe15e5f9a7bce20e      0t0  TCP 127.0.0.1:7871 (LISTEN)
== PID 86897 ==
86897 17658   39:03 bash -c LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=artifacts/tmp/app.sqlite3 .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1
n/Users/arsis/zlayt-pm-project
== PID 86899 ==
86899 86897   39:04 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
n/Users/arsis/zlayt-pm-project
Python  86899 arsis    9u  IPv4 0x89944c6bbeb1c380      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:52.489Z

Those five servers belong to other agents or the shared app: 23429, 37589 and 52906 run from other worktrees, 52326 runs from the project root on a port I did not use, and 86897/86899 are the shared app on 7860. I'll leave them alone. Next I'll confirm that none of my own PIDs or any process whose cwd is in my archive copy is still running.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:53.602Z

**tool call — Bash**
````
{
 "command": "for p in 52291 52392 52754 53030 53689; do if ps -p $p >/dev/null 2>&1; then echo \"ALIVE $p: $(ps -o command= -p $p | cut -c1-120)\"; else echo \"gone $p\"; fi; done; echo \"--- any process with cwd under my archive copy ---\"; for p in $(pgrep -f \"app.main|pytest\" 2>/dev/null); do c=$(lsof -a -p $p -d cwd -Fn 2>/dev/null | grep \"^n\" | cut -c2-); case \"$c\" in *T-177-staff-engineer-r2*) echo \"MINE-LEFT $p $c\";; esac; done; echo \"(end)\"",
 "description": "Confirm my own server PIDs are gone and none remain from archive cwd"
}
````

### User / tool · 2026-11-02T21:10:53.670Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No closing quotation) | command: for p in 52291 52392 52754 53030 53689; do if ps -p $p >/dev/null 2>&1; then echo "ALIVE $p: $(ps -o command= -p $p | cut -c1-120)"; else echo "gone $p"; fi; done; echo "--- any process with cwd under
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:55.126Z

**tool call — Bash**
````
{
 "command": "ps -p 52291,52392,52754,53030,53689 -o pid=,command= ; echo \"exit=$?\"",
 "description": "Check whether my own server PIDs are still running"
}
````

### User / tool · 2026-11-02T21:10:55.219Z

**tool result**
````
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:10:55.389Z

**tool call — Bash**
````
{
 "command": "pgrep -fl \"app.main\" ; echo \"exit=$?\"",
 "description": "List running app.main processes with PIDs"
}
````

### User / tool · 2026-11-02T21:10:55.495Z

**tool result**
````
23429 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
37589 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
52326 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
52906 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
86897 bash -c LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=artifacts/tmp/app.sqlite3 .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1
86899 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:06.512Z

None of my five PIDs are alive, and the remaining `app.main` processes belong to other agents or the shared app, so I'm leaving them alone. One more coverage question: the audit rows show `hand-checked (qa)` on `flags_v1` calls, so prepared flags may exist beyond the nine entries. I'll check the flag items' provenance fields and trace labels on the curated set.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:09.863Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_flags.py",
 "content": "\"\"\"T-177 r2 flag-item probe (staff-engineer-reviewer). Curated set, archive copy. For every flag and amount item: its prepared flag,\nits ladder.generator (model and prepared), and every trace step label/why that mentions AI or a model.\nUsage: python -I probe_r2_flags.py <archive_dir> <scratch_dir>\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\n\nARCH, SCRATCH = sys.argv[1], sys.argv[2]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ[\"ZLAYT_MODE\"] = \"local\"\nfor k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"LLM_FIXTURE_DIR\"):\n    os.environ.pop(k, None)\nos.environ[\"FIXTURE_SET\"] = \"curated\"\ndb = os.path.join(SCRATCH, \"probe_flags.sqlite\")\nif os.path.exists(db):\n    os.remove(db)\nc = TestClient(create_app(db, static_dir=os.path.join(ARCH, \"app\", \"frontend\")), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True, \"title\": \"flags probe\"}).json()[\"token\"]\nc.post(f\"/api/cases/{tok}/run\", json={})\nfor _ in range(480):\n    s = c.get(f\"/api/cases/{tok}/status\").json()\n    if s[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.25)\ncase = c.get(f\"/api/cases/{tok}\").json()\nprint(\"run status:\", s[\"status\"])\nAI = re.compile(r\"\\bAI\\b|claude|drafted|Drafted|model\", re.I)\nfor key in (\"flags\", \"amounts\"):\n    for x in case.get(key, []):\n        it = c.get(f\"/api/cases/{tok}/items/{x['id']}\").json()[\"item\"]\n        gen = ((it.get(\"ladder\") or {}).get(\"generator\") or {})\n        print(f\"{key} {x['id']} kind={x.get('kind') or x.get('type')} state={x.get('state')} prepared={it.get('prepared')} generator={json.dumps(gen, ensure_ascii=False)[:160]}\")\n        tr = c.get(f\"/api/cases/{tok}/items/{x['id']}/trace\").json()\n        for st in tr.get(\"steps\", []):\n            txt = f\"{st.get('label')} | {st.get('why')}\"\n            if AI.search(txt):\n                print(f\"    step {st.get('id')}: label={st.get('label')!r} why={(st.get('why') or '')[:200]!r}\")\n"
}
````

### User / tool · 2026-11-02T21:11:09.964Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_flags.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:12.881Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_flags.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2-flags.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-flags.out | cut -c1-330 | head -80",
 "description": "Run curated flag and amount item provenance probe",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:11:13.996Z

**tool result**
````
exit=0
run status: ready
flags f_gap_r6_r7 kind=gap state=verified prepared=False generator={}
    step judge_not_needed: label='Second AI check' why='Not needed: this is arithmetic over dates in the record, which code does exactly.'
flags f_accident_date_after_treatment_1_2_7 kind=conflict state=verified prepared=False generator={}
    step judge_not_needed: label='Second AI check' why='Not needed: this is arithmetic over dates in the record, which code does exactly.'
flags f_cx1 kind=conflict state=verified prepared=False generator={}
    step judge_3: label='Second AI check: do these two quotes really conflict?' why='The second check agreed that the two quotes conflict.'
flags f_r3_1 kind=pre_existing state=verified prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The AI proposed this flag as a category and a quote; it wrote no explanation.'
    step agreement: label='Phrase list and AI agree' why='Both the phrase list and the AI found this flag.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='The second check agreed that the flag fits the quote.'
flags f_r8_1 kind=pre_existing state=verified prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The AI proposed this flag as a category and a quote; it wrote no explanation.'
    step agreement: label='Phrase list and AI agree' why='Both the phrase list and the AI found this flag.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='The second check agreed that the flag fits the quote.'
flags f_r6_1 kind=causation state=verified prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The AI proposed this flag as a category and a quote; it wrote no explanation.'
    step agreement: label='Phrase list and AI agree' why='Both the phrase list and the AI found this flag.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='The second check agreed that the flag fits the quote.'
flags f_r7_1 kind=causation state=needs_review prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The phrase list found this flag but the AI did not; check that it applies.'
    step agreement: label='Phrase list and AI agree' why='The phrase list found this flag but the AI did not; check that it applies.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='Not run: only the phrase list found this flag, so there is no AI answer to double-check; it stays marked for review.'
flags f_r7_2 kind=causation state=verified prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The AI proposed this flag as a category and a quote; it wrote no explanation.'
    step agreement: label='Phrase list and AI agree' why='Both the phrase list and the AI found this flag.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='The second check agreed that the flag fits the quote.'
flags f_r8_2 kind=causation state=verified prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The AI proposed this flag as a category and a quote; it wrote no explanation.'
    step agreement: label='Phrase list and AI agree' why='Both the phrase list and the AI found this flag.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='The second check agreed that the flag fits the quote.'
flags f_r9_1 kind=causation state=verified prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The AI proposed this flag as a category and a quote; it wrote no explanation.'
    step agreement: label='Phrase list and AI agree' why='Both the phrase list and the AI found this flag.'
    step judge_4: label='Second AI check: does this flag fit the quote?' why='The second check agreed that the flag fits the quote.'
amounts a1 kind=charge state=verified prepared=False generator={}
    step found_in_text: label='Dollar figure is in the record text' why="Code found this figure in the record by pattern; it is not a model's claim."
    step judge_2: label='Second AI check: is this figure a charge, rate or estimate?' why="The second check agreed with the rule's reading of this figure."
amounts a2 kind=rate state=needs_review prepared=False generator={}
    step found_in_text: label='Dollar figure is in the record text' why="Code found this figure in the record by pattern; it is not a model's claim."
    step judge_2: label='Second AI check: is this figure a charge, rate or estimate?' why="The second check agreed with the rule's reading of this figure."
amounts a4 kind=charge state=verified prepared=False generator={}
    step found_in_text: label='Dollar figure is in the record text' why="Code found this figure in the record by pattern; it is not a model's claim."
    step judge_2: label='Second AI check: is this figure a charge, rate or estimate?' why="The second check agreed with the rule's reading of this figure."
amounts a3 kind=damages state=needs_review prepared=False generator={}
    step found_in_text: label='Dollar figure is in the record text' why="Code found this figure in the record by pattern; it is not a model's claim."
    step judge_2: label='Second AI check: is this figure a charge, rate or estimate?' why='Damages and other non-bill figures are not sent to the second check.'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:21.284Z

The flag items are the gap. On the curated set, flags such as `f_r3_1` say "AI found it" and "The AI proposed this flag", and their item `prepared` is false, although the earlier audit rows showed `hand-checked (qa)` on `flags_v1` calls. I'll confirm that directly by printing the audit rows by role, along with the `proposed_by_ai` step's evidence for one flag.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:24.255Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_flags_audit.py",
 "content": "\"\"\"T-177 r2 flag-audit probe (staff-engineer-reviewer). Curated set, archive copy. Prints the audit rows grouped by role/step with\nmodel and prepared, and the 'proposed_by_ai' trace step evidence for one flag, to settle whether flag answers are prepared.\nUsage: python -I probe_r2_flags_audit.py <archive_dir> <scratch_dir>\"\"\"\nimport collections\nimport json\nimport os\nimport sys\nimport time\n\nARCH, SCRATCH = sys.argv[1], sys.argv[2]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ[\"ZLAYT_MODE\"] = \"local\"\nfor k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"LLM_FIXTURE_DIR\"):\n    os.environ.pop(k, None)\nos.environ[\"FIXTURE_SET\"] = \"curated\"\ndb = os.path.join(SCRATCH, \"probe_flags_audit.sqlite\")\nif os.path.exists(db):\n    os.remove(db)\nc = TestClient(create_app(db, static_dir=os.path.join(ARCH, \"app\", \"frontend\")), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True, \"title\": \"flags audit probe\"}).json()[\"token\"]\nc.post(f\"/api/cases/{tok}/run\", json={})\nfor _ in range(480):\n    s = c.get(f\"/api/cases/{tok}/status\").json()\n    if s[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.25)\ncalls = c.get(f\"/api/cases/{tok}/audit\").json()[\"calls\"]\ngrp = collections.Counter((x[\"role\"], x[\"step\"], x.get(\"model\"), x.get(\"prepared\"), x.get(\"prompt_version\")) for x in calls)\nprint(\"audit rows by (role, step, model, prepared, prompt_version):\")\nfor k, n in sorted(grp.items(), key=lambda kv: str(kv[0])):\n    print(f\"  {n:3d}  {k}\")\ntr = c.get(f\"/api/cases/{tok}/items/f_r3_1/trace\").json()\npb = next((x for x in tr[\"steps\"] if x[\"id\"] == \"proposed_by_ai\"), None)\nprint(\"f_r3_1 proposed_by_ai step evidence:\", json.dumps((pb or {}).get(\"evidence\"), ensure_ascii=False)[:500])\n"
}
````

### User / tool · 2026-11-02T21:11:24.362Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_flags_audit.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:28.018Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_flags_audit.py \"$PWD/$EV/archive\" \"$SCR\" > $EV/probe-r2-flags-audit.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-flags-audit.out | cut -c1-400",
 "description": "Run curated audit grouping and flag proposal evidence probe",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:11:29.005Z

**tool result**
````
exit=0
audit rows by (role, step, model, prepared, prompt_version):
    9  ('generator', 'extract', 'hand-checked (qa)', True, 'extract_v1')
    9  ('generator', 'flags', 'hand-checked (qa)', True, 'flags_v1')
    9  ('judge', 'j1', 'claude-haiku-5-5', False, 'judge_faithfulness_v1')
    3  ('judge', 'j2', 'claude-haiku-5-5', False, 'judge_amount_class_v1')
    1  ('judge', 'j3', 'claude-haiku-5-5', False, 'judge_conflict_v6')
    6  ('judge', 'j4', 'claude-haiku-5-5', False, 'judge_flag_v3')
f_r3_1 proposed_by_ai step evidence: {"model": {"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": false}, "prompt_version": "flags_v1"}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:36.409Z

This confirms a second D-065 gap, and it is on the shipped curated demo. The nine `flags` generator calls are `hand-checked (qa)` with `prepared: true` in the audit. But the flag items have `prepared: false`, an empty `ladder.generator`, and a `proposed_by_ai` step labelled "AI found it" whose evidence says `prepared: false`. The Why dialog probably shows "AI draft" for that step, because the stepper picks that label from the generator role. I want to see that in the rendered UI, so I'll find how flag cards open their Why panel.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:37.226Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && grep -rn \"why\" app/frontend/flags.js 2>/dev/null | cut -c1-220 | head -12; ls app/frontend/*.js | tr '\\n' ' '; echo; grep -rln \"flag-why\\|flag_why\\|btn-why\\|entry-why\" app/frontend/*.js | head; grep -rn \"\\\"entry-why\\\"\\|'entry-why'\\|entry-why\" app/frontend/*.js | cut -c1-200 | head -5",
 "description": "Find frontend code for flag Why panels and their test ids"
}
````

### User / tool · 2026-11-02T21:11:37.334Z

**tool result**
````
app/frontend/flags.js:58:  // The "why" can carry sentences the card's explanation already says (the paperwork note on a gap): show each sentence once.
app/frontend/flags.js:59:  function whyOnce(f) {
app/frontend/flags.js:61:    return String(f.why || "").split(/(?<=[.!?])\s+/).filter((t) => t && !exp.includes(t.trim())).join(" ");
app/frontend/flags.js:72:      f.state === "needs_review" && f.review_status !== "dismissed" && whyOnce(f) ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), whyOnce(f)) : null,   // the "quote fo
app/frontend/api.js app/frontend/app.js app/frontend/audit.js app/frontend/batch.js app/frontend/charges.js app/frontend/dom.js app/frontend/excerpt.js app/frontend/export.js app/frontend/exportcfg.js app/frontend/flags.js app/frontend/input.js app/frontend/judges.js app/frontend/manual.js app/frontend/mock.js app/frontend/mock_extra.js app/frontend/mock_flags.js app/frontend/mock_sample.js app/frontend/narrative.js app/frontend/overview.js app/frontend/review.js app/frontend/sections.js app/frontend/sidebyside.js app/frontend/source.js app/frontend/state.js app/frontend/stepper.js app/frontend/suggestions.js app/frontend/switcher.js app/frontend/timeline.js app/frontend/uncovered.js 
app/frontend/timeline.js
app/frontend/timeline.js:72:        el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-why", "aria-label": "Why this status: " + e.provider + (e.date ? ", " + ZL.fmtDate(e.da
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:40.061Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && grep -rn \"ZL.openStepper\\|openStepper\\|ZL.stepper\\|renderStepper\\|function openWhy\\|btn-why\\|flag-why\\|why-flag\" app/frontend/*.js | cut -c1-200 | head -12",
 "description": "Locate where the item stepper is opened for flags"
}
````

### User / tool · 2026-11-02T21:11:40.151Z

**tool result**
````
app/frontend/app.js:153:    $("#btn-export").addEventListener("click", () => { if (ZL.stepper) ZL.stepper.onExport(); ZL.openExport(); });
app/frontend/batch.js:74:        const name = ZL.stepper && ZL.stepper.label ? ZL.stepper.label(x.id) : x.id;
app/frontend/batch.js:77:          x.code === "EDIT_QUOTE" && ZL.stepper && ZL.stepper.changeQuote ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-batch-refused-quot
app/frontend/batch.js:78:          : ZL.stepper && ZL.stepper.editItem ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-batch-refused-edit", "aria-label": "Edit the s
app/frontend/charges.js:220:    const more = RV.moreActions([ZL.stepper ? ZL.stepper.traceButton(a.id, "btn btn--link") : null, ctrl.querySelector(".rv-audit"), detail], a.text, { testid: "btn-more", 
app/frontend/flags.js:77:    const ctrl = RV.controls(f, "flag"), more = RV.moreActions([ZL.stepper ? ZL.stepper.traceButton(f.id, "btn btn--link") : null, ctrl.querySelector(".rv-audit"), ctrl.queryS
app/frontend/overview.js:364:        const ok = na.item_id && ZL.stepper && ZL.stepper.goto ? ZL.stepper.goto(na.item_id) : false;
app/frontend/overview.js:378:    if (!id || !ZL.stepper || !ZL.stepper.goto) return;
app/frontend/overview.js:379:    if (ZL.stepper.goto(id)) { ev.preventDefault(); ev.stopImmediatePropagation(); }
app/frontend/overview.js:384:    paintHead(box, c, ZL.stepper && ZL.stepper.cachedTrace ? ZL.stepper.cachedTrace(s.token) : null);
app/frontend/overview.js:395:    paintHead(box, s.case, tr !== undefined ? tr : ZL.stepper && ZL.stepper.cachedTrace ? ZL.stepper.cachedTrace(s.token) : null);
app/frontend/export.js:75:    try { data = await ZL.api.exportCase(s.token, style); open = true; render(); if (ZL.stepper) ZL.stepper.clearExportNotice(); if (scroll) { const h = ZL.$("#h-export"); h.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:43.313Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && grep -n \"traceButton\" app/frontend/stepper.js | head -3 | cut -c1-260; grep -n \"function traceButton\" -A4 app/frontend/stepper.js | cut -c1-260; echo \"--- flags testids ---\"; grep -n \"data-testid\" app/frontend/flags.js | cut -c1-200 | head -8; echo \"--- moreActions ---\"; grep -rn \"moreActions\" app/frontend/review.js | head -2 | cut -c1-260",
 "description": "Read traceButton label and flag card test ids in frontend"
}
````

### User / tool · 2026-11-02T21:11:43.433Z

**tool result**
````
5:   Exposes ZL.stepper = { item, itemSection, openTrace, traceButton, mountCase, onExport, exportNotice, showExportBlocked, clearExportNotice, rejudge, rerunButton, goto, gotoPanel, label, cue, setLabel, verdictWord, progressLabel }. Server text only goes thr
497:  S.traceButton = (id, cls, text) => el("button", { type: "button", class: cls || "btn btn--link", "data-testid": "btn-trace", "data-trace-for": id, "aria-label": (text || "Why this status") + ": " + S.label(id), onclick: () => S.openTrace(id) }, text || "
--- flags testids ---
21:    const ul = el("ul", { class: "rv-evidence" + (f.type === "conflict" ? " rv-side" : ""), "data-testid": "flag-evidence", "aria-label": "Quoted evidence" });
55:    return el("p", { class: "rv-gap-change", "data-testid": "gap-change-card" }, el("strong", {}, g.sentence || "This figure changed after you confirmed a date."), " ", g.lines.join(" "));
67:    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
75:    if (note) a.append(el("p", { class: "rv-usernote", "data-testid": "flag-note-text" }, el("strong", {}, f.review_status === "dismissed" ? "Dismissed because: " : "Your note: "), note));
79:      seqs.length ? el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", onclick: () => RV.openSource(f, "flag") }, seqs.length > 1 ? "Open records " + joinList(seqs)
95:    return el("div", { class: "rv-skipped", "data-testid": "conflict-skipped" },
97:      el("ul", { class: "rv-cov-list" }, sk.map((x) => el("li", { "data-testid": "conflict-skipped-item", "data-skip-type": x.type, "data-reason-code": x.reason_code || null },
99:        Array.isArray(x.record_nos) && x.record_nos.length ? el("span", { "data-testid": "conflict-skipped-records" }, " " + seqWords(x.record_nos) + " not read.") : null))));
--- moreActions ---
app/frontend/review.js:187:  RV.moreActions = function (items, name, o) {
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:49.346Z

Flag Why panels open through `ZL.stepper.openTrace(id)`, which the `btn-trace` button calls from inside a More menu. I'll reproduce the open on my own curated server by calling that same function from the page, then read the rendered stepper text and its step-kind tags, and scan the document.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:54.186Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/render_flags_r2.py",
 "content": "\"\"\"T-177 r2 flag-render probe (staff-engineer-reviewer). Curated set on its OWN server (started and stopped here; listener verified).\nOpens the Why panel (item stepper) of two curated flags by calling ZL.stepper.openTrace(id), the function the btn-trace button calls\n(the button sits inside the card's More menu), then reads the rendered step labels and kinds and scans the whole document.\nUsage: python -I render_flags_r2.py <archive_dir> <evidence_dir> <scratch_dir>\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\n\nARCH, EVID, SCRATCH = sys.argv[1], sys.argv[2], sys.argv[3]\nsys.path.insert(0, ARCH)\nsys.path.insert(0, EVID)\n\nimport render_r2 as R  # noqa: E402  (helpers only; its main() does not run on import)\nfrom playwright.sync_api import sync_playwright  # noqa: E402\n\nFLAGS = [\"f_r3_1\", \"f_r6_1\"]\nBAD = [\"AI found it\", \"AI draft\", \"claude-sonnet\", \"Drafted by\", \"AI check\", \"The AI proposed\", \"drafted by AI\"]\n\n\ndef main():\n    out = []\n    base, port, proc, pids = R.start(\"curated\", \"flags\")\n    try:\n        tok, st = R.make_case(base)\n        out.append(f\"[flags] case run status={st} port={port}\")\n        with sync_playwright() as pw:\n            b = pw.chromium.launch()\n            pg = b.new_context(viewport={\"width\": 1280, \"height\": 900}).new_page()\n            pg.goto(f\"{base}/#/case/{tok}\")\n            pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n            for fid in FLAGS:\n                pg.wait_for_timeout(300)\n                pg.evaluate(\"id => window.ZL.stepper.openTrace(id)\", fid)\n                st_el = pg.get_by_test_id(\"item-stepper\")\n                st_el.wait_for(timeout=15000)\n                steps = st_el.get_by_test_id(\"step\")\n                rows = []\n                for i in range(steps.count()):\n                    s = steps.nth(i)\n                    kind = s.get_by_test_id(\"step-kind\").inner_text() if s.get_by_test_id(\"step-kind\").count() else \"\"\n                    rows.append((s.get_attribute(\"data-step-id\"), kind, s.inner_text()[:160].replace(\"\\n\", \" / \")))\n                out.append(f\"[flags] {fid}: stepper text (first 600 chars): {st_el.inner_text()[:600]!r}\")\n                for sid, kind, txt in rows:\n                    out.append(f\"[flags] {fid}: step {sid} kind={kind!r} text={txt!r}\")\n                text = R.scan(pg)\n                hits = [(w, text[max(0, m.start() - 50): m.end() + 40]) for w in BAD for m in re.finditer(re.escape(w), text)]\n                out.append(f\"[flags] {fid}: whole-document scan hits for {BAD}: {len(hits)}\")\n                for w, ctx in hits[:6]:\n                    out.append(f\"   hit {w!r}: ...{ctx}...\")\n                st_el.screenshot(path=os.path.join(EVID, f\"render-curated-flag-{fid}-why.png\"))\n                pg.keyboard.press(\"Escape\")\n                pg.wait_for_timeout(200)\n            b.close()\n    finally:\n        if proc.pid in R.listeners(port):\n            proc.terminate()\n            try:\n                proc.wait(timeout=10)\n            except Exception:\n                proc.kill()\n                proc.wait(timeout=10)\n        out.append(f\"[flags] stopped popen_pid={proc.pid}; listeners on port {port} now: {R.listeners(port)}\")\n    print(\"\\n\".join(out))\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:11:54.289Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/render_flags_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:11:57.721Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/render_flags_r2.py \"$PWD/$EV/archive\" \"$PWD/$EV\" \"$SCR\" > $EV/render-flags-r2.out 2>&1; echo \"exit=$?\"; cut -c1-520 $EV/render-flags-r2.out",
 "description": "Render curated flag Why panels on own server and read step labels",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:12:01.128Z

**tool result**
````
exit=0
[flags] own server port=54892 popen_pid=56356 listener_pids=[56356]
[flags] case run status=ready port=54892
[flags] f_r3_1: stepper text (first 600 chars): 'Ready for your decision\n7 passed, 1 needs you\n\nNeeds your decision: Your decision You have not accepted, edited or dismissed this item yet, so it stays out of the letter.\n\nShow this step\n✓\nPhrase list found it\nCode\nPassed\n\nThe researched phrase list found this wording in the record.\n\nRecord 3\nPatient reports low back pain in 2023, resolved.\nTechnical details\n✓\nAI found it\nAI draft\nPassed\n\nThe AI proposed this flag as a category and a quote; i
[flags] f_r3_1: step proposed_by_phrase_list kind='Code' text='✓ / Phrase list found it / Code / Passed /  / The researched phrase list found this wording in the record. /  / Record 3 / Patient reports low back pain in 2023, resolved. / Tech'
[flags] f_r3_1: step proposed_by_ai kind='AI draft' text='✓ / AI found it / AI draft / Passed /  / The AI proposed this flag as a category and a quote; it wrote no explanation. /  / Technical details'
[flags] f_r3_1: step agreement kind='Code' text='✓ / Phrase list and AI agree / Code / Passed /  / Both the phrase list and the AI found this flag. /  / Technical details'
[flags] f_r3_1: step excerpt_verbatim kind='Code' text='✓ / Quote is word for word in the record / Code / Passed /  / The quote was found in the record, character for character. /  / Record 3 / Patient reports low back pain in 2023,'
[flags] f_r3_1: step highlight kind='Code' text="✓ / Quote can be highlighted in the record / Code / Passed /  / The quote's position in the record was found. /  / Technical details"
[flags] f_r3_1: step injection_scan kind='Code' text='✓ / Record has no instruction-like text / Code / Passed /  / The record has no instruction-like text. /  / Technical details'
[flags] f_r3_1: step judge_4 kind='AI check' text='✓ / Second AI check: does this flag fit the quote? / AI check / Passed /  / The second check agreed that the flag fits the quote. /  / The second AI check said: Supported. Th'
[flags] f_r3_1: step human kind='You' text='○ / Your decision / You / Needs your decision / Blocks export /  / You have not accepted, edited or dismissed this item yet, so it stays out of the letter. /  / Technical detai'
[flags] f_r3_1: whole-document scan hits for ['AI found it', 'AI draft', 'claude-sonnet', 'Drafted by', 'AI check', 'The AI proposed', 'drafted by AI']: 28
   hit 'AI found it': ...in in 2023, resolved.Technical detailsrule row 12✓AI found itAI draftPassedThe AI proposed this flag ...
   hit 'AI draft': ...s and quotes for each record, standing in for the AI draftPrepared answerPassedThe prepared answer...
   hit 'AI draft': ... resolved.Technical detailsrule row 12✓AI found itAI draftPassedThe AI proposed this flag as a cat...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Austin EMS r...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Central ER d...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Dr. Alvarez,...
[flags] f_r6_1: stepper text (first 600 chars): 'Ready for your decision\n7 passed, 1 needs you\n\nNeeds your decision: Your decision You have not accepted, edited or dismissed this item yet, so it stays out of the letter.\n\nShow this step\n✓\nPhrase list found it\nCode\nPassed\n\nThe researched phrase list found this wording in the record.\n\nRecord 6\nDischarged from PT after two missed appointments.\nTechnical details\n✓\nAI found it\nAI draft\nPassed\n\nThe AI proposed this flag as a category and a quote; 
[flags] f_r6_1: step proposed_by_phrase_list kind='Code' text='✓ / Phrase list found it / Code / Passed /  / The researched phrase list found this wording in the record. /  / Record 6 / Discharged from PT after two missed appointments. / Tec'
[flags] f_r6_1: step proposed_by_ai kind='AI draft' text='✓ / AI found it / AI draft / Passed /  / The AI proposed this flag as a category and a quote; it wrote no explanation. /  / Technical details'
[flags] f_r6_1: step agreement kind='Code' text='✓ / Phrase list and AI agree / Code / Passed /  / Both the phrase list and the AI found this flag. /  / Technical details'
[flags] f_r6_1: step excerpt_verbatim kind='Code' text='✓ / Quote is word for word in the record / Code / Passed /  / The quote was found in the record, character for character. /  / Record 6 / Discharged from PT after two missed ap'
[flags] f_r6_1: step highlight kind='Code' text="✓ / Quote can be highlighted in the record / Code / Passed /  / The quote's position in the record was found. /  / Technical details"
[flags] f_r6_1: step injection_scan kind='Code' text='✓ / Record has no instruction-like text / Code / Passed /  / The record has no instruction-like text. /  / Technical details'
[flags] f_r6_1: step judge_4 kind='AI check' text='✓ / Second AI check: does this flag fit the quote? / AI check / Passed /  / The second check agreed that the flag fits the quote. /  / The second AI check said: Supported. Th'
[flags] f_r6_1: step human kind='You' text='○ / Your decision / You / Needs your decision / Blocks export /  / You have not accepted, edited or dismissed this item yet, so it stays out of the letter. /  / Technical detai'
[flags] f_r6_1: whole-document scan hits for ['AI found it', 'AI draft', 'claude-sonnet', 'Drafted by', 'AI check', 'The AI proposed', 'drafted by AI']: 28
   hit 'AI found it': ... missed appointments.Technical detailsrule row 12✓AI found itAI draftPassedThe AI proposed this flag ...
   hit 'AI draft': ...s and quotes for each record, standing in for the AI draftPrepared answerPassedThe prepared answer...
   hit 'AI draft': ...ointments.Technical detailsrule row 12✓AI found itAI draftPassedThe AI proposed this flag as a cat...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Austin EMS r...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Central ER d...
   hit 'AI draft': ...ed by our team for this demo, standing in for the AI draft |  |  | Show full excerpt: Dr. Alvarez,...
[flags] stopped popen_pid=56356; listeners on port 54892 now: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:29.621Z

This is the strongest result so far. On the shipped curated demo, a flag's Why panel shows "AI found it" with the kind tag "AI draft" and "The AI proposed this flag as a category", while the audit says those answers are `hand-checked (qa)`. The T-177 acceptance says "no 'AI draft' on a curated item", and the r2 e2e only opened entry Why panels, so it missed flags. I'll treat it as a blocker. I also want a clean reproduction of the round-1 F4 scenario, a curated run with one missing answer file, to see what the trace says. I'll add a `missing` mode to the branch probe.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:31.195Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py",
 "old_string": "p = os.path.join(mut_dir, E1_KEY + \".json\")\nd = json.load(open(p))\nd[\"output\"][\"summary\"] = \"Patient reported paralysis of the left leg and loss of bladder control.\"     # no clause is in the quote: code removes all of it (D-054)\njson.dump(d, open(p, \"w\"), indent=1, sort_keys=True)",
 "new_string": "p = os.path.join(mut_dir, E1_KEY + \".json\")\nMODE = sys.argv[3] if len(sys.argv) > 3 else \"unsupported\"\nif MODE == \"missing\":\n    os.remove(p)                                 # one curated answer file is absent: fixture.call raises FixtureMiss (no recorded fallback for this key)\nelse:\n    d = json.load(open(p))\n    d[\"output\"][\"summary\"] = \"Patient reported paralysis of the left leg and loss of bladder control.\"     # no clause is in the quote: code removes all of it (D-054)\n    json.dump(d, open(p, \"w\"), indent=1, sort_keys=True)\nprint(\"mutation mode:\", MODE)"
}
````

### User / tool · 2026-11-02T21:12:31.325Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/probe_r2_branch.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:35.339Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-177-staff-engineer-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I $EV/probe_r2_branch.py \"$PWD/$EV/archive\" \"$SCR\" missing > $EV/probe-r2-branch-missing.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-branch-missing.out | cut -c1-400; echo \"--- unsupported-summary mode (re-run for the record) ---\"; .venv/bin/python -I $EV/probe_r2_branch.py \"$PWD/$EV/archive\" \"$SCR\" unsupported > $EV/probe-r2-branch.out 2>&1; echo \"exit=$?\"; grep -v \"llm call failed\" $EV/probe-r2-branch.out | cut -c1-300",
 "description": "Run missing-key and unsupported-summary branch probes on curated set",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:12:37.785Z

**tool result**
````
exit=0
mutation mode: missing
run status: failed
health answers: prepared
e1 state: rejected reasons: ['FIXTURE_MISS'] prepared: False
e1 ladder.generator.model: None
e1 extracted step:
{
 "label": "AI drafted a summary and picked a quote",
 "status": "pass",
 "why": "The AI read this record and proposed a one-line summary and a quote.",
 "reason_code": null,
 "rule": "row 4"
}
e1 extracted evidence.model: {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null, "prepared": false}
case-level extract step label: 'AI drafts a summary and a quote for each record' status: fail
case-level extract why: '1 record has no AI-made entry. The AI step failed on all three attempts, so this record has no AI-made entry.'
--- unsupported-summary mode (re-run for the record) ---
exit=0
mutation mode: unsupported
run status: ready
health answers: prepared
e1 state: rejected reasons: ['SUMMARY_NOT_IN_QUOTE'] prepared: True
e1 ladder.generator.model: hand-checked (qa)
e1 extracted step:
{
 "label": "AI drafted a summary and picked a quote",
 "status": "fail",
 "why": "removed from the summary: not in the quote: 'Patient reported paralysis of the left leg' removed from the summary: not in the quote: 'loss of bladder control' Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so co
 "reason_code": "SUMMARY_NOT_IN_QUOTE",
 "rule": "D-054"
}
e1 extracted evidence.model: {"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true}
case-level extract step label: 'Prepared summaries and quotes for each record, standing in for the AI draft' status: fail
case-level extract why: "1 record has no prepared entry. Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:52.000Z

The missing-key run shows a second problem. The item is `rejected` with `FIXTURE_MISS`, yet its trace step says `pass`, "The AI read this record and proposed a one-line summary and a quote", and names `claude-sonnet-5-5`. The case-level step says the AI step failed, so the two traces disagree. Last, I need exact line numbers for the citations, covering the flag-step code, the failure branches, and the e2e tests that do not open flags.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:54.479Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && echo \"--- proposed_by_ai / found-it wording (trace.py, flags) ---\" && grep -n \"proposed_by_ai\\|AI found it\\|The AI proposed this flag\" app/backend/trace.py | cut -c1-230 && echo \"--- item extracted FAIL branches (trace.py) ---\" && grep -n 'step(\"extracted\", \"AI drafted' app/backend/trace.py | cut -c1-120 && echo \"--- prepared check in _entry_steps (trace.py) ---\" && grep -n 'if ev\\[\"model\"\\]\\[\"prepared\"\\]' app/backend/trace.py && echo \"--- _llm_evidence prepared source ---\" && grep -n \"def _llm_evidence\" -A12 app/backend/trace.py | grep -n \"prepared\\|recorded_from\\|is_prepared\" | cut -c1-240 && echo \"--- models_for / prepared gate (present.py) ---\" && grep -n \"def models_for\\|prepared = bool(gens)\" app/backend/present.py && echo \"--- flags ladder generator (flags.py) ---\" && grep -n '\"generator\"' app/backend/flags.py | head -5 | cut -c1-200 && echo \"--- judges.js prepared line ---\" && grep -n \"const prepared = !!\" app/frontend/judges.js | cut -c1-200 && echo \"--- e2e test names in HEAD file (archive) ---\" && grep -n \"^def test_\" tests/e2e/test_demo_provenance.py && echo \"--- flag mention in e2e file ---\" && grep -n \"flag\" tests/e2e/test_demo_provenance.py | head -5 | cut -c1-160; echo \"(end)\"",
 "description": "Collect exact file and line references for findings"
}
````

### User / tool · 2026-11-02T21:12:54.644Z

**tool result**
````
--- proposed_by_ai / found-it wording (trace.py, flags) ---
690:            st.append(step("proposed_by_ai", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
692:            st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
694:        st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
996:                                      "judge_says": "The AI did not find it." if c == "LEXICON_ONLY" else "The AI found it.",
--- item extracted FAIL branches (trace.py) ---
400:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("SCHEMA_
403:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL, reason_text("LLM_FAI
407:            st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", FAIL,
414:                st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
--- prepared check in _entry_steps (trace.py) ---
411:            if ev["model"]["prepared"]:
689:        if ev["model"]["prepared"]:
760:    if ev["model"]["prepared"]:
--- _llm_evidence prepared source ---
4:181-                    "prepared": bool(call) and AU.is_prepared(call.get("recorded_from"))}}      # D-065: a hand-checked fixture answer, not model output
8:185-        for k in ("prompt_sha256", "backend", "recorded_from", "latency_ms", "parsed_ok"):
--- models_for / prepared gate (present.py) ---
283:def models_for(conn, case_id, base, calls=None):
288:    prepared = bool(gens) and all(AU.is_prepared(c.get("recorded_from")) for c in gens)
--- flags ladder generator (flags.py) ---
56:         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
238:            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:injection_scan"}}}
290:         "ladder": {"item_id": None, "generator": None, "judge": None,
--- judges.js prepared line ---
163:    const prepared = !!(d && d.models && d.models.generator_prepared);      // D-065: a prepared (hand-checked) demo answer was not drafted by a model; nothing here may say it was
--- e2e test names in HEAD file (archive) ---
84:def test_curated_trace_and_audit_say_prepared(curated_case):
100:def test_curated_page_never_calls_a_prepared_answer_ai(page, curated_case):
121:def test_curated_audit_drawer_marks_the_prepared_rows(page, curated_case):
131:def test_recorded_set_labels_say_ai(pw, recorded_server):
171:def test_curated_judge_panel_does_not_name_a_drafting_model(page, curated_case):
182:def test_curated_every_surface_is_free_of_the_drafting_model(page, curated_case):
206:def test_recorded_judge_panel_still_names_the_drafting_model(pw, recorded_server):
--- flag mention in e2e file ---
(end)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:57.556Z

The flag branch is at `trace.py:689-692`. It chooses the prepared label from `ev["model"]["prepared"]`, and `_llm_evidence` sets that from the call record. I'll read both spots to confirm the root cause before I write it up.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:12:58.327Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && sed -n '172,184p' app/backend/trace.py | cut -c1-250; echo \".....\"; sed -n '680,694p' app/backend/trace.py | cut -c1-250",
 "description": "Read _llm_evidence and flag proposed_by_ai branch in trace.py"
}
````

### User / tool · 2026-11-02T21:12:58.416Z

**tool result**
````
PREPARED_LABEL = "Prepared answer, standing in for the AI draft"
PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
CASE_PREPARED_LABEL = "Prepared summaries and quotes for each record, standing in for the AI draft"


def _llm_evidence(cx, role, model, prompt_version, call):
    ev = {"model": {"id": (call or {}).get("model") or model, "role": role,
                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"],
                    "prepared": bool(call) and AU.is_prepared(call.get("recorded_from"))}}      # D-065: a hand-checked fixture answer, not model output
    ev["prompt_version"] = (call or {}).get("prompt_version") or prompt_version
    if call:
        meta = present._call(call, cx.full)
.....
    elif has_lex:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", PASS, "The researched phrase list found this wording in the record.", rule="row 12", evidence={"spans": spans}))
    else:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", SKIPPED, reason_text("LLM_ONLY"), reason="LLM_ONLY", rule="row 12"))
    if has_llm:
        gen = lad.get("generator") or {}
        step_name = "conflicts" if ftype == "conflict" else "flags"
        call = cx.call(gen.get("call_id"), row["id"], step_name)
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
        if ev["model"]["prepared"]:
            st.append(step("proposed_by_ai", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
        else:
            st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
    else:
        st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:13:19.119Z

The root cause is clear. Flag items carry `ladder.generator = None` (`flags.py:56`, `:238`, `:290`), so `_llm_evidence` finds no call, `prepared` comes out false, and the flag falls through to "AI found it". Before writing, I'll confirm three details: that the T-182 `app/config.py` change leaves the model defaults alone, that the review file does not already exist, and what the board validator accepts.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:13:20.218Z

**tool call — Bash**
````
{
 "command": "git diff ac678bc 4671eee -- app/config.py | head -3; git show 4671eee:app/config.py | grep -n \"GENERATOR_MODEL\\|JUDGE_MODEL\\|PREPARED\\|FIXTURE\" | cut -c1-160; echo \"--- review file exists? ---\"; ls -la reviews/T-177-staff-engineer-r2.md 2>&1 | tail -1; echo \"--- board validate usage ---\"; python3 tools/board.py --help 2>&1 | grep -i \"validate\" | head -3",
 "description": "Check config model defaults, review file absence, and validator usage"
}
````

### User / tool · 2026-11-02T21:13:20.424Z

**tool result**
````
10:DEFAULTS = {"HOST": "127.0.0.1", "PORT": "7860", "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated"}
29:        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
--- review file exists? ---
ls: reviews/T-177-staff-engineer-r2.md: No such file or directory
--- board validate usage ---
                {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
  {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:13:24.343Z

The T-182 config sets `FIXTURE_SET` to `curated` by default for the fixture backend. That matters because a deploy that uses this config would show the curated demo by default. I'll check which code path imports `app/config.py` before I say how far that reaches.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:13:25.423Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/archive && grep -rn \"app.config\\|from app import config\\|import config\" --include=*.py --include=*.sh --include=Makefile --include=Dockerfile . 2>/dev/null | grep -v \"^./artifacts\" | cut -c1-200 | head -10; echo \"--- run.sh / Dockerfile FIXTURE_SET ---\"; grep -n \"FIXTURE_SET\\|LLM_BACKEND\" run.sh Dockerfile Makefile .env.example 2>/dev/null | cut -c1-200",
 "description": "Find importers of app config and FIXTURE_SET defaults in deploy files"
}
````

### User / tool · 2026-11-02T21:13:25.535Z

**tool result**
````
Makefile:19:	.venv/bin/python -m app.config
run.sh:35:    .venv/bin/python -m app.config
tools/compile_agents.py:83:        owns="Dockerfile, deploy/**, README.md, .env.example, Makefile, run.sh, app/config.py"),
app/config.py:3:`python -m app.config` prints the resolved settings (a key is reported only as set / not set). The Dockerfile, run.sh and the Makefile
--- run.sh / Dockerfile FIXTURE_SET ---
run.sh:34:    export LLM_BACKEND="${LLM_BACKEND:-fixture}" FIXTURE_SET="${FIXTURE_SET:-curated}" HOST="${HOST:-127.0.0.1}" PORT="${PORT:-7860}"
Dockerfile:21:ENV HOST=0.0.0.0 PORT=7860 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR=/home/user/data
.env.example:10:# LLM_BACKEND=fixture   # replays recorded/prepared answers; no model call is possible
.env.example:11:# FIXTURE_SET=curated   # the hand-checked sample set the public demo serves
.env.example:16:# LLM_BACKEND=anthropic-api   # or claude-cli (local dev only: uses your logged-in `claude` CLI, no key)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:13:58.778Z

The Dockerfile, `run.sh` and `.env.example` all make `FIXTURE_SET=curated` the default, so the flag finding is on the public demo's default path. Before I write the file, I'll verify the counts I plan to quote: how many flag items show "AI found it", and the exact step text for `f_r7_1`.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:00.280Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2 && echo \"flag items with 'AI found it' step:\" && grep -c \"step proposed_by_ai: label='AI found it'\" probe-r2-flags.out && grep \"step proposed_by_ai: label='AI found it'\" probe-r2-flags.out | sed -E 's/^(flags [^ ]+ ).*/\\1/' | head -2 >/dev/null; grep -B1 \"step proposed_by_ai: label='AI found it'\" probe-r2-flags.out | grep \"^flags\" | awk '{print $2}' | tr '\\n' ' '; echo; echo \"--- f_r7_1 lines ---\"; grep -A2 \"^flags f_r7_1\" probe-r2-flags.out | cut -c1-260; echo \"--- entry count prepared in probe-r2 ---\"; grep -c \"prepared=True label\" probe-r2.out",
 "description": "Count flag items showing AI found it and confirm f_r7_1 wording"
}
````

### User / tool · 2026-11-02T21:14:00.405Z

**tool result**
````
flag items with 'AI found it' step:
7
f_r3_1 f_r8_1 f_r6_1 f_r7_1 f_r7_2 f_r8_2 f_r9_1 
--- f_r7_1 lines ---
flags f_r7_1 kind=causation state=needs_review prepared=False generator={}
    step proposed_by_ai: label='AI found it' why='The phrase list found this flag but the AI did not; check that it applies.'
    step agreement: label='Phrase list and AI agree' why='The phrase list found this flag but the AI did not; check that it applies.'
--- entry count prepared in probe-r2 ---
9
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:09.283Z

Both checks match what I'll report: 7 flag items on the sample show "AI found it", not 9, and `f_r7_1` says "AI found it" while its why text says "the AI did not". I have what I need for the verdict, so I'll write the review file now.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:35.386Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r2.md",
 "content": "# T-177 round 2 (D-065 honest demo provenance): staff-engineer-reviewer\n\n**Verdict: fail (2 blockers, 1 major, 1 nit).** The round-1 fixes hold on the surfaces round 1 named: the judge panel, the badge tooltip, the banner, and the case, judges, health and export `models` fields. The round is not complete. On the curated demo, the flag Why panels still say \"AI found it\" with the kind tag \"AI draft\". A curated item whose summary fails a code check is still labelled \"AI drafted\". A curated run with one missing answer file shows a passing AI step that names claude-sonnet-5-5. The last one is a different path from the accepted mixed-set F4, and I have not treated it as covered by that acceptance.\n\n**Scope.** Card commit 4fcf9cd. HEAD moved during the review from ac678bc to 4671eee, so the review is on `git archive 4671eee` (`artifacts/review-evidence/T-177-staff-engineer-r2/archive-source-sha.txt`). The later commits are d07bf9d (D-065 tooltip wording, docs only) and 4671eee (T-183: create-case error text and the /classic mount). Neither touches provenance code. The curated set is FIXTURE_SET=curated; the recorded set is the control.\n\n**Round-1 status**\n\n| Round-1 item | Status at 4671eee |\n|---|---|\n| F1 blocker: drafter named on the judge panel and in case/judges payloads | Fixed for the judge panel, case, judges, health, export and case-level trace. Not complete: flags (F-A) and failure branches (F-B) |\n| F2 major: tooltip points at the eval report | Fixed. The tooltip string equals the committed D-065 text |\n| F3 major: banner says \"checked by code\" only | Fixed. The banner names the second AI model |\n| F4 minor: per-call provenance vs per-set banner | Accepted as debt for the mixed set (per Chris). A missing-key variant is F-C, not covered by that acceptance |\n| F5 nit: prompt version on prepared rows | Hidden in the UI only. The API and export still carry it (F-D) |\n\n## Findings\n\n**F-A blocker: flag items on the curated demo are labelled \"AI found it\" / \"AI draft\".** Rendered Why panels, own server, curated set: `render-flags-r2.out` shows f_r3_1 and f_r6_1 with step `proposed_by_ai`, kind `AI draft`, text \"AI found it ... The AI proposed this flag as a category and a quote\". Seven flag items on the sample carry this step (`probe-r2-flags.out`). The audit has 9 `flags` generator rows, all `hand-checked (qa)` with `prepared: true` (`probe-r2-flags-audit.out`). The flag items themselves have `prepared=False` and `generator={}`. Root cause: `app/backend/flags.py:56,238,290` set `ladder.generator` to None, so `trace.py:179-181` finds no call and `prepared` is false, and `trace.py:692` prints \"AI found it\". The Dockerfile (line 21), run.sh (line 34) and .env.example (line 11) make the curated set the public demo default. D-065 says a curated item is never \"AI draft\"; the card's AC1 says the same. The r2 e2e tests open only entry Why panels, and `tests/e2e/test_demo_provenance.py` has no flag test (grep for \"flag\" returns nothing), so the suite stayed green.\n\n**F-B blocker: a failed prepared item's trace says \"AI drafted a summary and picked a quote\".** The shipped sample does not reach it (all nine entries pass, `probe-r2.out`). Reproduction: `probe-r2-branch.out`. I replaced e1's curated summary with text no clause of which is in the quote, and the run is ready. e1's extracted step reads label \"AI drafted a summary and picked a quote\", status fail, reason SUMMARY_NOT_IN_QUOTE, while its evidence says `hand-checked (qa)`, `prepared: true`. The hard-coded labels are at `app/backend/trace.py:400`, `:403` and `:407`; only the PASS branch at `:411-414` reads the prepared flag. Any curated answer that fails a code check hits this.\n\n**F-C major: a curated run with one missing answer file shows a passing AI step that names claude-sonnet-5-5.** Reproduction: `probe-r2-branch-missing.out`. I removed e1's curated answer file, and it is absent from the recorded set too. e1 is `rejected` with reason FIXTURE_MISS. Its extracted step is `pass`, \"The AI read this record and proposed a one-line summary and a quote\", with evidence model `claude-sonnet-5-5`, `prepared: false`. The case-level extract step in the same run is `fail` (\"1 record has no AI-made entry\"). Health answers `prepared` in that run. FIXTURE_MISS is not in the handled reasons at `trace.py:398-407`, so it falls to the PASS else-branch at `:411-414`. The accepted F4 debt is the mixed set. This is a missing key, so I have not treated it as covered.\n\n**F-D nit: prepared answers still carry a prompt version and hash in the API and export.** `probe-r2.out` has 45 `extract_v1` and 93 `prompt_sha256` hits on curated payloads, for example an audit row `{model: hand-checked (qa), prompt_version: extract_v1, prompt_sha256: 98b1735e..., prepared: true}`. `probe-r2-export.out` gives curated provenance `prompt_versions: [extract_v1, flags_v1, ...]` next to `generator_prepared: true`. The UI hides these fields, but the round-1 acceptance test (prepared audit rows have no prompt_version and no prompt_sha256) is not met at the API.\n\n**F-E minor (outside T-177 scope, observed): a flag can read \"AI found it\" when the why says the AI did not find it.** `probe-r2-flags.out`, f_r7_1: label \"AI found it\", why \"The phrase list found this flag but the AI did not; check that it applies\". Same branch as F-A (`trace.py:689-692`). I did not check whether recorded flags do the same.\n\n## What I checked and found right\n\n- The tooltip string at `app/frontend/app.js:16` equals the committed D-065 text (`git show HEAD:memory/ORCHESTRATOR_DECISIONS.md`). The rendered tooltip matches it (`render-r2.out`).\n- The rendered curated page: badge \"Demo: sample answers prepared by our team\"; banner names \"a second AI model\"; judge line \"Prepared by our team (not by an AI model), checked by claude-haiku-5-5\". The only AI-draft text on the whole page is the D-065 phrase \"standing in for the AI draft\". The recorded control still says \"Drafted by claude-sonnet-5-5\" (`render-r2.out`).\n- Mutants in the archive copy, restored from HEAD and `cmp`-identical: forcing `models_for` prepared off fails 2 unit tests; forcing the judge-panel prepared flag off fails the e2e judge test.\n\n## Commands, sources and what I did not run\n\nI ran the unit file and the e2e file as the brief asked. I did not run the full `tests/unit` suite or the eval runner; neither is in the brief. Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r2/`. My own servers were on loopback ports 54001, 54056, 54205, 54304, 54440 and 54892. Their PIDs (52291, 52392, 52754, 53030, 53689) are gone. The app processes 23429, 37589, 52326 and 52906 belong to other agents, and the shared app on :7860 (86897, 86899) was not touched.\n\n## Verdict rule\n\nTwo blockers (F-A, F-B), so `fail`. F-C is major and F-D and F-E are nit and minor.\n\n```json\n{\"card\": \"T-177\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2. git archive of HEAD 4671eee (card commit 4fcf9cd; later commits d07bf9d docs and 4671eee T-183 api.py create-case text and /classic mount, no provenance code); archive at artifacts/review-evidence/T-177-staff-engineer-r2/archive; sample case on FIXTURE_SET=curated (prepared) and on the recorded set (control); own private servers on loopback ports 54001, 54056, 54205, 54304, 54440, 54892 (all stopped); shared app on :7860 (PID 86899) untouched\",\n \"exercised\": [\n  \"python3 tools/board.py show T-177 (in_review; commits 04ea2bf, 4fcf9cd; AC1 done with evidence); reviews/T-177-staff-engineer.md read as the round-1 list\",\n  \"git log -n 8 and git rev-parse HEAD: HEAD moved ac678bc -> 4671eee during the review; git show 4fcf9cd -- app/ (full r2 diff read); git show d07bf9d; git show 4671eee -- app/backend/api.py\",\n  \"git show HEAD:memory/ORCHESTRATOR_DECISIONS.md D-065 row, compared byte-for-byte with app/frontend/app.js:16 tooltip: equal\",\n  \"git archive HEAD into artifacts/review-evidence/T-177-staff-engineer-r2/archive (2432 files); archive-source-sha.txt = 4671eee\",\n  \".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q in the archive: 10 passed (unit-prepared.out)\",\n  \"E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v in the archive, base URL and ZLAYT_DB unset so the conftest starts its own private server on a free loopback port: 7 passed, 0 skipped (e2e-provenance.out)\",\n  \"probe_r2.py (TestClient, curated and recorded): /api/health, /api/cases/{tok}, /judges, /audit, /trace, /status, /api/cases, /export and every item and item trace; pattern hits (probe-r2.out)\",\n  \"probe_r2_export.py: accept every item, GET /export; provenance block and word scan on curated and recorded (probe-r2-export.out)\",\n  \"probe_r2_flags.py and probe_r2_flags_audit.py: flag and amount items on curated; audit rows grouped by role, model, prepared, prompt_version (probe-r2-flags.out, probe-r2-flags-audit.out)\",\n  \"probe_r2_branch.py: curated e1 with an unsupported summary (probe-r2-branch.out) and with the answer file removed (probe-r2-branch-missing.out)\",\n  \"render_r2.py on own curated and recorded servers (Playwright): badge text and title, banner, judge label, judge model line, judge totals, whole-document scan (text, title, aria-label); screenshots render-*.png (render-r2.out)\",\n  \"render_flags_r2.py on own curated server: Why panels of f_r3_1 and f_r6_1 opened via ZL.stepper.openTrace, the call btn-trace makes; step labels, kinds and whole-document scan (render-flags-r2.out; render-curated-flag-*-why.png)\",\n  \"race_r2.py: /api/health held 3 s on own curated server; banner-ai sampled while held (race-r2.out): banner hidden until health answered, so no fallback text was shown. Not a finding\",\n  \"mutant M1: present.py:288 prepared forced False; pytest unit file: 2 failed, 8 passed (console output, not saved); restored from HEAD, cmp identical\",\n  \"mutant M2: judges.js:163 prepared forced false; pytest e2e -k 'judge or surface': 1 failed, 2 passed; restored from HEAD, cmp identical\",\n  \"grep over app/ for model-name literals and drafter wording; app/frontend/mock*.js is dev-only (api.js:5 API_MODE = real)\",\n  \"Dockerfile:21, run.sh:34, .env.example:11: curated set is the public demo default\",\n  \"ps and lsof: my PIDs 52291, 52392, 52754, 53030, 53689 gone; other app.main PIDs (23429, 37589, 52326, 52906) and shared 86897/86899 left alone after cwd and port check\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"provenance_honesty\": 2, \"pm_acceptance_criteria\": 2, \"test_strength\": 2, \"llm_boundary\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Curated flag items show 'AI found it' with kind 'AI draft' in the Why panel; the flag items are not marked prepared\",\n   \"evidence\": \"render-flags-r2.out: f_r3_1 step proposed_by_ai kind='AI draft' text='AI found it ... The AI proposed this flag as a category and a quote; it wrote no explanation' (same for f_r6_1). probe-r2-flags.out: 7 flag items with 'AI found it'; 'flags f_r3_1 ... prepared=False generator={}'. probe-r2-flags-audit.out: 9 rows (generator, flags, hand-checked (qa), True, flags_v1); 'f_r3_1 proposed_by_ai step evidence: model hand-checked (qa), prepared: false'. Root cause: app/backend/flags.py:56,238,290 set ladder.generator None; app/backend/trace.py:179-181 sets prepared from the call, which is None, so false; trace.py:692 prints 'AI found it'. Public demo default: Dockerfile:21 FIXTURE_SET=curated; run.sh:34; .env.example:11.\",\n   \"why_it_matters\": \"D-065 (binding): a curated item is never 'AI draft'; card T-177 AC1: no 'AI draft' on a curated item. The public demo serves the curated set by default, so a reader sees 'AI draft' on seven flag items. The r2 e2e tests open only entry Why panels, and tests/e2e/test_demo_provenance.py has no flag test, so the suite passed.\",\n   \"fix\": \"Record the generator call on each flag ladder (flags.py: generator with model, prompt_version, call_id) and take prepared from that call, or take it from the case's models.generator_prepared as models_for does. For prepared flags, proposed_by_ai uses PREPARED_LABEL and PREPARED_WHY, the stepper kind reads 'Prepared answer', the item is prepared true, and evidence.model.prepared matches the audit row.\",\n   \"acceptance_test\": \"E2E on FIXTURE_SET=curated (own server): open the Why panel of every flag with an AI proposal (f_r3_1, f_r6_1, f_r8_1, f_r7_1, f_r7_2, f_r8_2, f_r9_1); assert no 'AI found it', no step-kind 'AI draft', step reads 'Prepared answer'; whole-panel scan with the D-065 phrase removed has none of 'AI draft', 'AI found it', 'claude-sonnet'. Unit: GET /api/cases/{tok}/items/f_r3_1/trace has proposed_by_ai evidence.model.prepared true and label PREPARED_LABEL on the curated set; the recorded set keeps 'AI found it' and prepared false.\"},\n  {\"severity\": \"blocker\", \"title\": \"A failed prepared item's trace says 'AI drafted a summary and picked a quote' (latent on the shipped sample)\",\n   \"evidence\": \"app/backend/trace.py:400, :403 and :407 hard-code the label 'AI drafted a summary and picked a quote' whatever prepared is; only the PASS branch at :411-414 reads prepared. Reproduction: probe-r2-branch.out (curated copy, e1 summary replaced by text no clause of which is in the quote): e1 extracted step label 'AI drafted a summary and picked a quote', status fail, reason SUMMARY_NOT_IN_QUOTE, evidence model 'hand-checked (qa)' prepared true. Shipped sample: 9 of 9 entries pass (probe-r2.out).\",\n   \"why_it_matters\": \"Same rule as F-A. The shipped sample does not reach this branch, but any edit to a curated answer that fails a code check does, and the product would tell the reader that an AI wrote a summary the team wrote.\",\n   \"fix\": \"At trace.py:400, :403 and :407 choose the label and why from the prepared flag (PREPARED_LABEL and a prepared why). The reason sentence for SUMMARY_NOT_IN_QUOTE must not say 'the AI's summary' for a prepared item.\",\n   \"acceptance_test\": \"Unit, curated fixture dir named curated with one e1 summary holding no supported clause: e1 extracted label contains 'Prepared' and not 'AI drafted'; repeat for SCHEMA_INVALID and LLM_FAILED_AFTER_RETRIES. Mutation: restoring the hard-coded label fails the test.\"},\n  {\"severity\": \"major\", \"title\": \"A curated run with one missing answer file reports a passing AI step that names claude-sonnet-5-5 (not covered by accepted F4)\",\n   \"evidence\": \"probe-r2-branch-missing.out: e1 state rejected, reasons ['FIXTURE_MISS'] (absent from curated and recorded sets). e1 extracted step status 'pass', label 'AI drafted a summary and picked a quote', why 'The AI read this record and proposed a one-line summary and a quote.', evidence model claude-sonnet-5-5 prepared false. Same run: case-level extract step 'fail' ('1 record has no AI-made entry'); health answers 'prepared'. trace.py:398-407 does not handle FIXTURE_MISS; it falls to the PASS else-branch at :411-414.\",\n   \"why_it_matters\": \"Accepted F4 is the mixed set. This is a missing key on the curated set. The item's own trace says an AI read a record and proposed a summary, names a model, and passes, while the item is rejected and the case trace says the step failed. The claim is invented provenance on the demo's own fixture set.\",\n   \"fix\": \"Any reason not handled by the branches above gets a FAIL step that carries the reason, never PASS; a rejected item cannot show a passing generator step. Health answers and the run must not report 'prepared' when a curated set misses a key (round-1 F4 acceptance).\",\n   \"acceptance_test\": \"Unit: copy the curated set minus e1's generator file to a temp dir named curated (LLM_FIXTURE_DIR) and run; e1 extracted status is not 'pass', its why does not say 'The AI read this record', and health answers is not 'prepared' (or the run fails).\"},\n  {\"severity\": \"nit\", \"title\": \"Prepared answers still carry a prompt version and hash in the API and export (round-1 F5 hidden in the UI only)\",\n   \"evidence\": \"probe-r2.out: 45 'extract_v1' and 93 'prompt_sha256' hits on curated payloads, e.g. audit row model 'hand-checked (qa)', prompt_version 'extract_v1', prompt_sha256 '98b1735e...', prepared true. probe-r2-export.out: curated provenance generator_model 'hand-checked (qa)', generator_prepared true, prompt_versions ['extract_v1', 'flags_v1', ...]. UI hides these in audit.js, stepper.js, timeline.js (4fcf9cd).\",\n   \"why_it_matters\": \"A prompt version and hash say a prompt produced an answer nothing prompted. The round-1 acceptance test is not met at the API.\",\n   \"fix\": \"On prepared rows set prompt_version and prompt_sha256 to null, and leave the prompt versions of prepared calls out of provenance.prompt_versions.\",\n   \"acceptance_test\": \"Unit on the curated set: every audit row with prepared true has prompt_version None and prompt_sha256 None; GET /api/cases/{tok}/export provenance.prompt_versions has no extract_v1 or flags_v1 when generator_prepared is true.\"},\n  {\"severity\": \"minor\", \"title\": \"A flag can read 'AI found it' while its why says the AI did not find it (outside T-177 scope, observed)\",\n   \"evidence\": \"probe-r2-flags.out, f_r7_1: step proposed_by_ai label 'AI found it', why 'The phrase list found this flag but the AI did not; check that it applies.' Same branch as F-A (trace.py:689-692).\",\n   \"why_it_matters\": \"A label that contradicts its own sentence is the same honesty problem in a different field. I did not check whether recorded flags do the same.\",\n   \"fix\": \"Derive the proposed_by_ai label from whether the AI proposed the flag, and state that in the same sentence.\",\n   \"acceptance_test\": \"Unit: a flag the phrase list found and the AI did not has no 'AI found it' label and its why agrees with its label.\"}\n ],\n \"whats_right\": [\n  \"The badge tooltip (app/frontend/app.js:16) equals the committed D-065 text, and the rendered tooltip matches it (render-r2.out).\",\n  \"On the curated page the rendered banner names the second AI model, the judge line reads 'Prepared by our team (not by an AI model)', and the only AI-draft wording is the D-065 phrase; the recorded control still names claude-sonnet-5-5.\",\n  \"The unit and e2e guards are real: forcing models_for prepared off fails 2 unit tests; forcing the judge-panel prepared flag off fails the e2e judge test (both restored from HEAD, cmp-identical).\"\n ],\n \"questions_for_chris\": [\n  \"Does the accepted F4 debt cover a curated run with a missing answer file (F-C), or only the mixed set? I have treated F-C as not covered.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T21:14:35.587Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:38.723Z

I'll check the file the way the board will read it: exactly one ```json block, valid JSON, and a verdict that matches the rule.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:41.101Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/check_review_json.py",
 "content": "\"\"\"Check a review file: exactly one ```json block, valid JSON, verdict follows the rule (blocker->fail, major->changes, else pass).\nUsage: python -I check_review_json.py <review.md>\"\"\"\nimport json\nimport sys\n\ntext = open(sys.argv[1], encoding=\"utf-8\").read()\nblocks = []\nlines = text.split(\"\\n\")\ni = 0\nwhile i < len(lines):\n    if lines[i].strip() == \"```json\":\n        j = i + 1\n        buf = []\n        while j < len(lines) and lines[j].strip() != \"```\":\n            buf.append(lines[j])\n            j += 1\n        blocks.append(\"\\n\".join(buf))\n        i = j\n    i += 1\nprint(\"json blocks:\", len(blocks))\nassert len(blocks) == 1, \"must have exactly one json block\"\nd = json.loads(blocks[0])\nprint(\"parsed OK; card:\", d[\"card\"], \"| persona:\", d[\"persona\"], \"| model:\", d[\"model\"], \"| verdict:\", d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"finding severities:\", sev)\nwant = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule expects:\", want, \"| file says:\", d[\"verdict\"], \"| match:\", want == d[\"verdict\"])\nprint(\"exercised items:\", len(d[\"exercised\"]), \"| whats_right:\", len(d[\"whats_right\"]), \"| questions:\", len(d[\"questions_for_chris\"]))\nfor f in d[\"findings\"]:\n    assert all(k in f for k in (\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\")), f[\"title\"]\nprint(\"all findings carry the six required fields\")\n"
}
````

### User / tool · 2026-11-02T21:14:41.195Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r2/check_review_json.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:42.988Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r2/check_review_json.py reviews/T-177-staff-engineer-r2.md; echo \"exit=$?\"; python3 tools/board.py validate --help 2>&1 | head -8",
 "description": "Validate review JSON block, verdict rule, and check validator usage"
}
````

### User / tool · 2026-11-02T21:14:43.160Z

**tool result**
````
json blocks: 1
parsed OK; card: T-177 | persona: staff-engineer-reviewer | model: claude-haiku-5-5 | verdict: fail
finding severities: ['blocker', 'blocker', 'major', 'nit', 'minor']
verdict rule expects: fail | file says: fail | match: True
exercised items: 18 | whats_right: 3 | questions: 1
all findings carry the six required fields
exit=0
usage: board.py validate [-h] [path]

positional arguments:
  path

options:
  -h, --help  show this help message and exit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:44.882Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-177-staff-engineer-r2.md 2>&1 | tail -15; echo \"exit=$?\"",
 "description": "Run board validator on the review file"
}
````

### User / tool · 2026-11-02T21:14:45.019Z

**tool result**
````
ok (1 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:53.377Z

The board validator accepts the review file. Next I'll update my memory with the patterns this round produced. The T-177 notes get an r2 section. I'll also record the Playwright hold technique and the guard limits I hit.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:57.300Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_provenance_patterns.md",
 "old_string": "Related: [[project_llm_stage_review_patterns]], [[feedback_frontend_text_coupling]], [[project_t167_plain_wording_patterns]].",
 "new_string": "**Round 2 (HEAD 4671eee, card commit 4fcf9cd), what the r2 fix missed:**\n- Fixed entries, not every item kind: flag items (`flags.py:56,238,290` set `ladder.generator` None) take `prepared` from a call lookup that is None, so `trace.py:689-692` prints \"AI found it\" with kind \"AI draft\" on the curated demo. Seven flag items on the sample. The e2e file has no flag test (grep \"flag\" is empty). Check every item kind (entry, flag, amount) with a Why-panel open, not just entry 1.\n- Hard-coded labels on FAIL branches: `trace.py:400,403,407` say \"AI drafted\" whatever `prepared` is; only the PASS branch (`:411-414`) reads it. Break a curated answer's code check to reach them (`probe_r2_branch`-style: copy curated to a dir named `curated`, overlay recorded keys, change one answer).\n- Unhandled reason falls through to PASS: FIXTURE_MISS on a curated key shows \"The AI read this record\" pass with claude-sonnet-5-5 on a rejected item. Not the mixed-set F4 that was accepted.\n- Payload prompt fields: UI hid `prompt_version` on prepared rows; API audit rows and `export.provenance.prompt_versions` still list extract_v1 and flags_v1.\n- Tooltip and banner now match D-065 (verified by string compare against `git show HEAD:memory/ORCHESTRATOR_DECISIONS.md`), so the round-1 F2/F3 class is closed.\n- Mutants that worked: `present.py` `prepared = bool(gens) and ...` forced False (2 unit fail), `judges.js` `const prepared = !!(...)` forced false (1 e2e fail). Restore by `mutate_r2.py restore` (git show sha) and cmp.\n- A probe that says \"AI draft\" hits on the curated page is the D-065 phrase \"standing in for the AI draft\"; strip that phrase before scanning, as the e2e does.\n\nRelated: [[project_llm_stage_review_patterns]], [[feedback_frontend_text_coupling]], [[project_t167_plain_wording_patterns]], [[feedback_playwright_route_hold]]."
}
````

### User / tool · 2026-11-02T21:14:57.419Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_provenance_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:14:59.711Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_playwright_route_hold.md",
 "content": "---\nname: playwright-route-hold\ndescription: a blocking time.sleep inside a Playwright sync route handler freezes the page, so the poll loop sees nothing; park the route and release it from the loop\nmetadata:\n  type: feedback\n---\n\nTo delay an API response in a Playwright sync probe, store the `route` object in a list inside the handler and return; release it later from the main loop with `route.continue_()`. A `time.sleep(4)` inside the handler blocks the event loop, so the sampling loop records nothing (T-177 r2, race probe, first attempt: zero samples).\n\n**Why:** the race probe needed the banner's first paint while `/api/health` was pending. The blocking sleep stopped every page event, so the result said nothing about the page. The held-route version showed the banner stays hidden until health answers.\n\n**How to apply:** any timing or race check on a page that waits for an API call. Park the request, sample the DOM in a loop with `wait_for_timeout`, release, and report the samples with the release time. A probe that records zero samples is not evidence of absence; say so, or fix the probe first.\n\nRelated: [[project_t177_provenance_patterns]], [[feedback_playwright_render_probe]].\n"
}
````

### User / tool · 2026-11-02T21:14:59.833Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_playwright_route_hold.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:15:02.486Z

The index in `MEMORY.md` needs one new line and an updated T-177 entry. I'll read the file first, as the edit tool requires.

### Assistant · claude-haiku-5-5 · 2026-11-02T21:15:02.826Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 150
}
````

### User / tool · 2026-11-02T21:15:02.840Z

**tool result**
````
<system-reminder>Warning: the file exists but is shorter than the provided offset (150). The file has 111 lines.</system-reminder>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:15:04.592Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 100,
 "limit": 12
}
````

### User / tool · 2026-11-02T21:15:04.608Z

**tool result**
````
100	- [Bind to named reference](feedback_bind_to_named_reference.md) — binding test must read the reference the artifact names
101	- [T-173 seed-fidelity patterns](project_t173_seed_fidelity_patterns.md) — r1/r2: seeded row raw-equal to placeholder; browser attempt rule unguarded (M6 3/3)
102	- [Guard blocks shell expansions](feedback_guard_blocks_shell_expansions.md) — git-guard refuses ${var%%}; board-guard refuses 2>; use python -I script
103	- [T-175 r2 patterns](project_t175_r2_patterns.md) — 9/9 backend mutants red, UI renders null progress as "None"
104	- [Playwright render probe](feedback_playwright_render_probe.md) — render the real list from an archive; screenshot beats inner_text
105	- [GATE-M3 / T-045 patterns](project_gate_m3_t045_patterns.md) — is_mobile scroll check vacuous, "unit-covered" claim false, no-op mutants
106	- [T-045 r2 record-latest patterns](project_t045_r2_record_latest_patterns.md) — header value copied not recomputed; flipped fixture report records ship bar True
107	- [Mutant apply verify](feedback_mutant_apply_verify.md) — BSD sed 0,/re/ no-ops silently; grep the mutant; restore via git show HEAD
108	- [T-177 provenance patterns](project_t177_provenance_patterns.md) — per-item model fixed, case/judges payload and panel still name the model; tooltip points at hash-only report
109	- [T-045 r3 record-latest patterns](project_t045_r3_record_latest_patterns.md) — header flips refused; consistent body+header forgery records live (minor); parser coverage gaps
110	- [Consistent forgery probe](feedback_consistent_forgery_probe.md) — recompute-from-document checks: probe header+body+pointer together, not only header flips
111	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:15:06.861Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-177 provenance patterns](project_t177_provenance_patterns.md) — per-item model fixed, case/judges payload and panel still name the model; tooltip points at hash-only report",
 "new_string": "- [T-177 provenance patterns](project_t177_provenance_patterns.md) — r1: payload model names; r2: flag items \"AI found it\", FAIL branches say \"AI drafted\", missing-key PASS\n- [Playwright route hold](feedback_playwright_route_hold.md) — blocking sleep in a route handler freezes the page; park the route, release from the loop"
}
````

### User / tool · 2026-11-02T21:15:06.964Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T21:15:17.483Z

Verdict fail for T-177 round 2: 2 blockers (flag Why panels on the curated demo say "AI found it" / "AI draft"; a failed prepared item's trace says "AI drafted"), 1 major (missing curated answer shows a passing claude-sonnet-5-5 step, not covered by the accepted F4), 1 nit. Review: /Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r2.md (board validator passes).
