# Subagent: Staff review: T-177 r3 (Staff review: T-177 r3)

Source: `agent-ad633dc054b897913.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:49:33.495Z

Review T-177, round 3 (final; D-065 honest provenance), in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. The fix commit is 2e58e18. Read reviews/T-177-staff-engineer-r2.md, D-065 in memory/ORCHESTRATOR_DECISIONS.md, and the card notes (`python3 tools/board.py show T-177`).

1. Check that the round-2 blockers and major are fixed: flag Why panels, the failed-prepared trace, and the missing curated answer.
2. Run the demo from a `git archive 2e58e18` copy on your own port, and stop only your PID. Grep every API response for the sample and two library cases for "AI drafted", "AI found" and model names on prepared items.
3. Judge the worker's stated residuals:
   - /health reports `answers: prepared` when a curated key is missing;
   - the export letter's disclosure line says "drafted with AI assistance";
   - review.py's edit and manual warnings say "AI wording".
   For each one, decide whether it misstates who wrote a prepared answer (that is a blocker or major) or is accurate product disclosure (that is fine). Note that D-009 keeps the AI statement out of the letter.
4. Check that /classic redirects in demo mode and stays reachable with ZLAYT_MODE=local.

Write reviews/T-177-staff-engineer-r3.md in D.2 format, applying the verdict rule. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:35.003Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T21:49:35.010Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:35.444Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r2.md"
}
````

### User / tool · 2026-11-02T21:49:35.451Z

**tool result**
````
1	# T-177 round 2 (D-065 honest demo provenance): staff-engineer-reviewer
2	
3	**Verdict: fail (2 blockers, 1 major, 1 nit).** The round-1 fixes hold on the surfaces round 1 named: the judge panel, the badge tooltip, the banner, and the case, judges, health and export `models` fields. The round is not complete. On the curated demo, the flag Why panels still say "AI found it" with the kind tag "AI draft". A curated item whose summary fails a code check is still labelled "AI drafted". A curated run with one missing answer file shows a passing AI step that names claude-sonnet-5-5. The last one is a different path from the accepted mixed-set F4, and I have not treated it as covered by that acceptance.
4	
5	**Scope.** Card commit 4fcf9cd. HEAD moved during the review from ac678bc to 4671eee, so the review is on `git archive 4671eee` (`artifacts/review-evidence/T-177-staff-engineer-r2/archive-source-sha.txt`). The later commits are d07bf9d (D-065 tooltip wording, docs only) and 4671eee (T-183: create-case error text and the /classic mount). Neither touches provenance code. The curated set is FIXTURE_SET=curated; the recorded set is the control.
6	
7	**Round-1 status**
8	
9	| Round-1 item | Status at 4671eee |
10	|---|---|
11	| F1 blocker: drafter named on the judge panel and in case/judges payloads | Fixed for the judge panel, case, judges, health, export and case-level trace. Not complete: flags (F-A) and failure branches (F-B) |
12	| F2 major: tooltip points at the eval report | Fixed. The tooltip string equals the committed D-065 text |
13	| F3 major: banner says "checked by code" only | Fixed. The banner names the second AI model |
14	| F4 minor: per-call provenance vs per-set banner | Accepted as debt for the mixed set (per Chris). A missing-key variant is F-C, not covered by that acceptance |
15	| F5 nit: prompt version on prepared rows | Hidden in the UI only. The API and export still carry it (F-D) |
16	
17	## Findings
18	
19	**F-A blocker: flag items on the curated demo are labelled "AI found it" / "AI draft".** Rendered Why panels, own server, curated set: `render-flags-r2.out` shows f_r3_1 and f_r6_1 with step `proposed_by_ai`, kind `AI draft`, text "AI found it ... The AI proposed this flag as a category and a quote". Seven flag items on the sample carry this step (`probe-r2-flags.out`). The audit has 9 `flags` generator rows, all `hand-checked (qa)` with `prepared: true` (`probe-r2-flags-audit.out`). The flag items themselves have `prepared=False` and `generator={}`. Root cause: `app/backend/flags.py:56,238,290` set `ladder.generator` to None, so `trace.py:179-181` finds no call and `prepared` is false, and `trace.py:692` prints "AI found it". The Dockerfile (line 21), run.sh (line 34) and .env.example (line 11) make the curated set the public demo default. D-065 says a curated item is never "AI draft"; the card's AC1 says the same. The r2 e2e tests open only entry Why panels, and `tests/e2e/test_demo_provenance.py` has no flag test (grep for "flag" returns nothing), so the suite stayed green.
20	
21	**F-B blocker: a failed prepared item's trace says "AI drafted a summary and picked a quote".** The shipped sample does not reach it (all nine entries pass, `probe-r2.out`). Reproduction: `probe-r2-branch.out`. I replaced e1's curated summary with text no clause of which is in the quote, and the run is ready. e1's extracted step reads label "AI drafted a summary and picked a quote", status fail, reason SUMMARY_NOT_IN_QUOTE, while its evidence says `hand-checked (qa)`, `prepared: true`. The hard-coded labels are at `app/backend/trace.py:400`, `:403` and `:407`; only the PASS branch at `:411-414` reads the prepared flag. Any curated answer that fails a code check hits this.
22	
23	**F-C major: a curated run with one missing answer file shows a passing AI step that names claude-sonnet-5-5.** Reproduction: `probe-r2-branch-missing.out`. I removed e1's curated answer file, and it is absent from the recorded set too. e1 is `rejected` with reason FIXTURE_MISS. Its extracted step is `pass`, "The AI read this record and proposed a one-line summary and a quote", with evidence model `claude-sonnet-5-5`, `prepared: false`. The case-level extract step in the same run is `fail` ("1 record has no AI-made entry"). Health answers `prepared` in that run. FIXTURE_MISS is not in the handled reasons at `trace.py:398-407`, so it falls to the PASS else-branch at `:411-414`. The accepted F4 debt is the mixed set. This is a missing key, so I have not treated it as covered.
24	
25	**F-D nit: prepared answers still carry a prompt version and hash in the API and export.** `probe-r2.out` has 45 `extract_v1` and 93 `prompt_sha256` hits on curated payloads, for example an audit row `{model: hand-checked (qa), prompt_version: extract_v1, prompt_sha256: 98b1735e..., prepared: true}`. `probe-r2-export.out` gives curated provenance `prompt_versions: [extract_v1, flags_v1, ...]` next to `generator_prepared: true`. The UI hides these fields, but the round-1 acceptance test (prepared audit rows have no prompt_version and no prompt_sha256) is not met at the API.
26	
27	**F-E minor (outside T-177 scope, observed): a flag can read "AI found it" when the why says the AI did not find it.** `probe-r2-flags.out`, f_r7_1: label "AI found it", why "The phrase list found this flag but the AI did not; check that it applies". Same branch as F-A (`trace.py:689-692`). I did not check whether recorded flags do the same.
28	
29	## What I checked and found right
30	
31	- The tooltip string at `app/frontend/app.js:16` equals the committed D-065 text (`git show HEAD:memory/ORCHESTRATOR_DECISIONS.md`). The rendered tooltip matches it (`render-r2.out`).
32	- The rendered curated page: badge "Demo: sample answers prepared by our team"; banner names "a second AI model"; judge line "Prepared by our team (not by an AI model), checked by claude-haiku-5-5". The only AI-draft text on the whole page is the D-065 phrase "standing in for the AI draft". The recorded control still says "Drafted by claude-sonnet-5-5" (`render-r2.out`).
33	- Mutants in the archive copy, restored from HEAD and `cmp`-identical: forcing `models_for` prepared off fails 2 unit tests; forcing the judge-panel prepared flag off fails the e2e judge test.
34	
35	## Commands, sources and what I did not run
36	
37	I ran the unit file and the e2e file as the brief asked. I did not run the full `tests/unit` suite or the eval runner; neither is in the brief. Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r2/`. My own servers were on loopback ports 54001, 54056, 54205, 54304, 54440 and 54892. Their PIDs (52291, 52392, 52754, 53030, 53689) are gone. The app processes 23429, 37589, 52326 and 52906 belong to other agents, and the shared app on :7860 (86897, 86899) was not touched.
38	
39	## Verdict rule
40	
41	Two blockers (F-A, F-B), so `fail`. F-C is major and F-D and F-E are nit and minor.
42	
43	```json
44	{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
45	 "scope": "round 2. git archive of HEAD 4671eee (card commit 4fcf9cd; later commits d07bf9d docs and 4671eee T-183 api.py create-case text and /classic mount, no provenance code); archive at artifacts/review-evidence/T-177-staff-engineer-r2/archive; sample case on FIXTURE_SET=curated (prepared) and on the recorded set (control); own private servers on loopback ports 54001, 54056, 54205, 54304, 54440, 54892 (all stopped); shared app on :7860 (PID 86899) untouched",
46	 "exercised": [
47	  "python3 tools/board.py show T-177 (in_review; commits 04ea2bf, 4fcf9cd; AC1 done with evidence); reviews/T-177-staff-engineer.md read as the round-1 list",
48	  "git log -n 8 and git rev-parse HEAD: HEAD moved ac678bc -> 4671eee during the review; git show 4fcf9cd -- app/ (full r2 diff read); git show d07bf9d; git show 4671eee -- app/backend/api.py",
49	  "git show HEAD:memory/ORCHESTRATOR_DECISIONS.md D-065 row, compared byte-for-byte with app/frontend/app.js:16 tooltip: equal",
50	  "git archive HEAD into artifacts/review-evidence/T-177-staff-engineer-r2/archive (2432 files); archive-source-sha.txt = 4671eee",
51	  ".venv/bin/python -m pytest tests/unit/test_prepared_provenance.py -q in the archive: 10 passed (unit-prepared.out)",
52	  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -v in the archive, base URL and ZLAYT_DB unset so the conftest starts its own private server on a free loopback port: 7 passed, 0 skipped (e2e-provenance.out)",
53	  "probe_r2.py (TestClient, curated and recorded): /api/health, /api/cases/{tok}, /judges, /audit, /trace, /status, /api/cases, /export and every item and item trace; pattern hits (probe-r2.out)",
54	  "probe_r2_export.py: accept every item, GET /export; provenance block and word scan on curated and recorded (probe-r2-export.out)",
55	  "probe_r2_flags.py and probe_r2_flags_audit.py: flag and amount items on curated; audit rows grouped by role, model, prepared, prompt_version (probe-r2-flags.out, probe-r2-flags-audit.out)",
56	  "probe_r2_branch.py: curated e1 with an unsupported summary (probe-r2-branch.out) and with the answer file removed (probe-r2-branch-missing.out)",
57	  "render_r2.py on own curated and recorded servers (Playwright): badge text and title, banner, judge label, judge model line, judge totals, whole-document scan (text, title, aria-label); screenshots render-*.png (render-r2.out)",
58	  "render_flags_r2.py on own curated server: Why panels of f_r3_1 and f_r6_1 opened via ZL.stepper.openTrace, the call btn-trace makes; step labels, kinds and whole-document scan (render-flags-r2.out; render-curated-flag-*-why.png)",
59	  "race_r2.py: /api/health held 3 s on own curated server; banner-ai sampled while held (race-r2.out): banner hidden until health answered, so no fallback text was shown. Not a finding",
60	  "mutant M1: present.py:288 prepared forced False; pytest unit file: 2 failed, 8 passed (console output, not saved); restored from HEAD, cmp identical",
61	  "mutant M2: judges.js:163 prepared forced false; pytest e2e -k 'judge or surface': 1 failed, 2 passed; restored from HEAD, cmp identical",
62	  "grep over app/ for model-name literals and drafter wording; app/frontend/mock*.js is dev-only (api.js:5 API_MODE = real)",
63	  "Dockerfile:21, run.sh:34, .env.example:11: curated set is the public demo default",
64	  "ps and lsof: my PIDs 52291, 52392, 52754, 53030, 53689 gone; other app.main PIDs (23429, 37589, 52326, 52906) and shared 86897/86899 left alone after cwd and port check"
65	 ],
66	 "verdict": "fail",
67	 "scores": {"provenance_honesty": 2, "pm_acceptance_criteria": 2, "test_strength": 2, "llm_boundary": 5},
68	 "findings": [
69	  {"severity": "blocker", "title": "Curated flag items show 'AI found it' with kind 'AI draft' in the Why panel; the flag items are not marked prepared",
70	   "evidence": "render-flags-r2.out: f_r3_1 step proposed_by_ai kind='AI draft' text='AI found it ... The AI proposed this flag as a category and a quote; it wrote no explanation' (same for f_r6_1). probe-r2-flags.out: 7 flag items with 'AI found it'; 'flags f_r3_1 ... prepared=False generator={}'. probe-r2-flags-audit.out: 9 rows (generator, flags, hand-checked (qa), True, flags_v1); 'f_r3_1 proposed_by_ai step evidence: model hand-checked (qa), prepared: false'. Root cause: app/backend/flags.py:56,238,290 set ladder.generator None; app/backend/trace.py:179-181 sets prepared from the call, which is None, so false; trace.py:692 prints 'AI found it'. Public demo default: Dockerfile:21 FIXTURE_SET=curated; run.sh:34; .env.example:11.",
71	   "why_it_matters": "D-065 (binding): a curated item is never 'AI draft'; card T-177 AC1: no 'AI draft' on a curated item. The public demo serves the curated set by default, so a reader sees 'AI draft' on seven flag items. The r2 e2e tests open only entry Why panels, and tests/e2e/test_demo_provenance.py has no flag test, so the suite passed.",
72	   "fix": "Record the generator call on each flag ladder (flags.py: generator with model, prompt_version, call_id) and take prepared from that call, or take it from the case's models.generator_prepared as models_for does. For prepared flags, proposed_by_ai uses PREPARED_LABEL and PREPARED_WHY, the stepper kind reads 'Prepared answer', the item is prepared true, and evidence.model.prepared matches the audit row.",
73	   "acceptance_test": "E2E on FIXTURE_SET=curated (own server): open the Why panel of every flag with an AI proposal (f_r3_1, f_r6_1, f_r8_1, f_r7_1, f_r7_2, f_r8_2, f_r9_1); assert no 'AI found it', no step-kind 'AI draft', step reads 'Prepared answer'; whole-panel scan with the D-065 phrase removed has none of 'AI draft', 'AI found it', 'claude-sonnet'. Unit: GET /api/cases/{tok}/items/f_r3_1/trace has proposed_by_ai evidence.model.prepared true and label PREPARED_LABEL on the curated set; the recorded set keeps 'AI found it' and prepared false."},
74	  {"severity": "blocker", "title": "A failed prepared item's trace says 'AI drafted a summary and picked a quote' (latent on the shipped sample)",
75	   "evidence": "app/backend/trace.py:400, :403 and :407 hard-code the label 'AI drafted a summary and picked a quote' whatever prepared is; only the PASS branch at :411-414 reads prepared. Reproduction: probe-r2-branch.out (curated copy, e1 summary replaced by text no clause of which is in the quote): e1 extracted step label 'AI drafted a summary and picked a quote', status fail, reason SUMMARY_NOT_IN_QUOTE, evidence model 'hand-checked (qa)' prepared true. Shipped sample: 9 of 9 entries pass (probe-r2.out).",
76	   "why_it_matters": "Same rule as F-A. The shipped sample does not reach this branch, but any edit to a curated answer that fails a code check does, and the product would tell the reader that an AI wrote a summary the team wrote.",
77	   "fix": "At trace.py:400, :403 and :407 choose the label and why from the prepared flag (PREPARED_LABEL and a prepared why). The reason sentence for SUMMARY_NOT_IN_QUOTE must not say 'the AI's summary' for a prepared item.",
78	   "acceptance_test": "Unit, curated fixture dir named curated with one e1 summary holding no supported clause: e1 extracted label contains 'Prepared' and not 'AI drafted'; repeat for SCHEMA_INVALID and LLM_FAILED_AFTER_RETRIES. Mutation: restoring the hard-coded label fails the test."},
79	  {"severity": "major", "title": "A curated run with one missing answer file reports a passing AI step that names claude-sonnet-5-5 (not covered by accepted F4)",
80	   "evidence": "probe-r2-branch-missing.out: e1 state rejected, reasons ['FIXTURE_MISS'] (absent from curated and recorded sets). e1 extracted step status 'pass', label 'AI drafted a summary and picked a quote', why 'The AI read this record and proposed a one-line summary and a quote.', evidence model claude-sonnet-5-5 prepared false. Same run: case-level extract step 'fail' ('1 record has no AI-made entry'); health answers 'prepared'. trace.py:398-407 does not handle FIXTURE_MISS; it falls to the PASS else-branch at :411-414.",
81	   "why_it_matters": "Accepted F4 is the mixed set. This is a missing key on the curated set. The item's own trace says an AI read a record and proposed a summary, names a model, and passes, while the item is rejected and the case trace says the step failed. The claim is invented provenance on the demo's own fixture set.",
82	   "fix": "Any reason not handled by the branches above gets a FAIL step that carries the reason, never PASS; a rejected item cannot show a passing generator step. Health answers and the run must not report 'prepared' when a curated set misses a key (round-1 F4 acceptance).",
83	   "acceptance_test": "Unit: copy the curated set minus e1's generator file to a temp dir named curated (LLM_FIXTURE_DIR) and run; e1 extracted status is not 'pass', its why does not say 'The AI read this record', and health answers is not 'prepared' (or the run fails)."},
84	  {"severity": "nit", "title": "Prepared answers still carry a prompt version and hash in the API and export (round-1 F5 hidden in the UI only)",
85	   "evidence": "probe-r2.out: 45 'extract_v1' and 93 'prompt_sha256' hits on curated payloads, e.g. audit row model 'hand-checked (qa)', prompt_version 'extract_v1', prompt_sha256 '98b1735e...', prepared true. probe-r2-export.out: curated provenance generator_model 'hand-checked (qa)', generator_prepared true, prompt_versions ['extract_v1', 'flags_v1', ...]. UI hides these in audit.js, stepper.js, timeline.js (4fcf9cd).",
86	   "why_it_matters": "A prompt version and hash say a prompt produced an answer nothing prompted. The round-1 acceptance test is not met at the API.",
87	   "fix": "On prepared rows set prompt_version and prompt_sha256 to null, and leave the prompt versions of prepared calls out of provenance.prompt_versions.",
88	   "acceptance_test": "Unit on the curated set: every audit row with prepared true has prompt_version None and prompt_sha256 None; GET /api/cases/{tok}/export provenance.prompt_versions has no extract_v1 or flags_v1 when generator_prepared is true."},
89	  {"severity": "minor", "title": "A flag can read 'AI found it' while its why says the AI did not find it (outside T-177 scope, observed)",
90	   "evidence": "probe-r2-flags.out, f_r7_1: step proposed_by_ai label 'AI found it', why 'The phrase list found this flag but the AI did not; check that it applies.' Same branch as F-A (trace.py:689-692).",
91	   "why_it_matters": "A label that contradicts its own sentence is the same honesty problem in a different field. I did not check whether recorded flags do the same.",
92	   "fix": "Derive the proposed_by_ai label from whether the AI proposed the flag, and state that in the same sentence.",
93	   "acceptance_test": "Unit: a flag the phrase list found and the AI did not has no 'AI found it' label and its why agrees with its label."}
94	 ],
95	 "whats_right": [
96	  "The badge tooltip (app/frontend/app.js:16) equals the committed D-065 text, and the rendered tooltip matches it (render-r2.out).",
97	  "On the curated page the rendered banner names the second AI model, the judge line reads 'Prepared by our team (not by an AI model)', and the only AI-draft wording is the D-065 phrase; the recorded control still names claude-sonnet-5-5.",
98	  "The unit and e2e guards are real: forcing models_for prepared off fails 2 unit tests; forcing the judge-panel prepared flag off fails the e2e judge test (both restored from HEAD, cmp-identical)."
99	 ],
100	 "questions_for_chris": [
101	  "Does the accepted F4 debt cover a curated run with a missing answer file (F-C), or only the mixed set? I have treated F-C as not covered."
102	 ]}
103	```
104	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:35.799Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_provenance_patterns.md"
}
````

### User / tool · 2026-11-02T21:49:35.810Z

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
20	**Round 2 (HEAD 4671eee, card commit 4fcf9cd), what the r2 fix missed:**
21	- Fixed entries, not every item kind: flag items (`flags.py:56,238,290` set `ladder.generator` None) take `prepared` from a call lookup that is None, so `trace.py:689-692` prints "AI found it" with kind "AI draft" on the curated demo. Seven flag items on the sample. The e2e file has no flag test (grep "flag" is empty). Check every item kind (entry, flag, amount) with a Why-panel open, not just entry 1.
22	- Hard-coded labels on FAIL branches: `trace.py:400,403,407` say "AI drafted" whatever `prepared` is; only the PASS branch (`:411-414`) reads it. Break a curated answer's code check to reach them (`probe_r2_branch`-style: copy curated to a dir named `curated`, overlay recorded keys, change one answer).
23	- Unhandled reason falls through to PASS: FIXTURE_MISS on a curated key shows "The AI read this record" pass with claude-sonnet-5-5 on a rejected item. Not the mixed-set F4 that was accepted.
24	- Payload prompt fields: UI hid `prompt_version` on prepared rows; API audit rows and `export.provenance.prompt_versions` still list extract_v1 and flags_v1.
25	- Tooltip and banner now match D-065 (verified by string compare against `git show HEAD:memory/ORCHESTRATOR_DECISIONS.md`), so the round-1 F2/F3 class is closed.
26	- Mutants that worked: `present.py` `prepared = bool(gens) and ...` forced False (2 unit fail), `judges.js` `const prepared = !!(...)` forced false (1 e2e fail). Restore by `mutate_r2.py restore` (git show sha) and cmp.
27	- A probe that says "AI draft" hits on the curated page is the D-065 phrase "standing in for the AI draft"; strip that phrase before scanning, as the e2e does.
28	
29	Related: [[project_llm_stage_review_patterns]], [[feedback_frontend_text_coupling]], [[project_t167_plain_wording_patterns]], [[feedback_playwright_route_hold]].
30	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:36.615Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-177 | tail -80; grep -n \"D-065\" memory/ORCHESTRATOR_DECISIONS.md | head"
}
````

### User / tool · 2026-11-02T21:49:36.745Z

**tool result**
````
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
updated_at: "2026-11-02T21:49:28Z"
claimed_by: "backend"
claimed_at: "2026-11-02T21:15:32Z"
rounds: 2
commits: ["04ea2bf", "4fcf9cd", "2e58e18"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-177-staff-engineer.md", "at": "2026-11-02T20:38:36Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-177-staff-engineer-r2.md", "at": "2026-11-02T21:15:23Z"}
ac:
  - {"n": 1, "text": "E2E on FIXTURE_SET=curated: no 'AI draft' or 'recorded AI answers' on a curated item; /items/e1/trace generator step model is not claude-sonnet-5-5 and names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'; with the recorded set, labels say AI; unit + e2e", "done": true, "evidence": "git archive 2e58e18: unit 5816 passed (8 shards, 141 files minus 2 uncommitted others'), e2e 431 passed 1 skipped (E2E_REQUIRE_DB=1, private local-mode server); new tests/unit/test_prepared_provenance_r3.py 12 passed (curated flag traces, whole-surface scan, failed/missing curated answer, recorded keeps AI wording, /classic redirect demo+recorded, reachable in local and ZLAYT_CLASSIC=1)"}
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
- 2026-11-02T21:04:53Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T21:15:23Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-177-staff-engineer-r2.md; round 2; findings:
    - [blocker] Curated flag items show 'AI found it' with kind 'AI draft' in the Why panel; the flag items are not marked prepared — fix: Record the generator call on each flag ladder (flags.py: generator with model, prompt_version, call_id) and take prepared from that call, or take it from the case's models.generator_prepared as models_for does. For prepared flags, proposed_by_ai uses PREPARED_L
    - [blocker] A failed prepared item's trace says 'AI drafted a summary and picked a quote' (latent on the shipped sample) — fix: At trace.py:400, :403 and :407 choose the label and why from the prepared flag (PREPARED_LABEL and a prepared why). The reason sentence for SUMMARY_NOT_IN_QUOTE must not say 'the AI's summary' for a prepared item.
    - [major] A curated run with one missing answer file reports a passing AI step that names claude-sonnet-5-5 (not covered by accepted F4) — fix: Any reason not handled by the branches above gets a FAIL step that carries the reason, never PASS; a rejected item cannot show a passing generator step. Health answers and the run must not report 'prepared' when a curated set misses a key (round-1 F4 a
    - [minor] A flag can read 'AI found it' while its why says the AI did not find it (outside T-177 scope, observed) — fix: Derive the proposed_by_ai label from whether the AI proposed the flag, and state that in the same sentence.
- 2026-11-02T21:15:23Z orchestrator: Round 3 (final): (1) every backend-generated text for a prepared item (trace steps incl. failed/missing curated answers, why sentences, flag origin) says prepared, never 'AI drafted/AI found it'; a missing curated answer never shows a model step; (2) /classic is a developer screen: in demo/public mode it redirects to the guided UI (D-068), so the classic flag Why panels need only the backend text fix. Guided UI reads the same backend text.
- 2026-11-02T21:15:24Z orchestrator: assigned: backend
- 2026-11-02T21:15:32Z backend: claimed
- 2026-11-02T21:49:10Z backend: Round 3: commit 2e58e18 (temp index). why.to_prepared (one swap table) applied to item why/explanation, every trace step why/next_action/reasons, judge-report disagreements, run_partial and ENTERED_BY_HAND messages on the curated set; flags are prepared via their record's flags call (present.flag_generator_call); failed prepared item keeps the Prepared label; a missing/unusable curated answer is a FAIL step with no model; prepared audit/trace rows carry null prompt version+hash; /classic redirects to / unless ZLAYT_MODE=local or ZLAYT_CLASSIC=1.
- 2026-11-02T21:49:10Z backend: AC 1 checked: git archive 2e58e18: unit 5816 passed (8 shards, 141 files minus 2 uncommitted others'), e2e 431 passed 1 skipped (E2E_REQUIRE_DB=1, private local-mode server); new tests/unit/test_prepared_provenance_r3.py 12 passed (curated flag traces, whole-surface scan, failed/missing curated answer, recorded keeps AI wording, /classic redirect demo+recorded, reachable in local and ZLAYT_CLASSIC=1)
- 2026-11-02T21:49:11Z backend: moved in_progress -> in_review
- 2026-11-02T21:49:28Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (r3, 2e58e18): F-A flags: a flag's generator is its record's flags call, so curated flags are prepared (item + trace read Prepared answer / Prepared answers did not include this flag / Phrase list and prepared answers agree; F-E label now agrees with its why). F-B/F-C: failed prepared item keeps the Prepared label; any placeholder (FIXTURE_MISS, unsupported language) is a FAIL step with no model evidence ('There is no prepared answer for this record in the demo'), never a pass; a curated miss's audit row names hand-checked (qa), models_for ignores miss calls. Every first-answer 'AI drafted/found/proposed' sentence goes through one table why.to_prepared (item why, trace steps, next_action, judge disagreements, run_partial and ENTERED_BY_HAND). F-D: prepared rows have null prompt_version/hash and export prompt_versions skips them. /classic: api.py redirects to / in demo/public mode, served with ZLAYT_MODE=local or ZLAYT_CLASSIC=1 (api.md updated). Verified: git archive 2e58e18 unit 5816 passed, e2e 431 passed 1 skipped; tests/unit/test_prepared_provenance_r3.py (12). Left/residual: /health answers stays 'prepared' for a curated set with a missing key (per-item truth is on the item); the export letter's AI disclosure line still says drafted with AI assistance (export.py, not in scope); classic e2e against a non-local server (E2E_BASE_URL) now redirects, set ZLAYT_CLASSIC=1 there; the review.py edit/manual-entry warnings still say 'AI wording' (action responses, not item text). Surprised: a curated schema failure is really FIXTURE_MISS (the retry prompt has no key), and the shared tree held others' hunks in api.py/present.py/api.md so I committed a filtered patch.

73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:39.385Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git log --oneline -n 6 && git show --stat 2e58e18 | head -50"
}
````

### User / tool · 2026-11-02T21:49:39.511Z

**tool result**
````
fa4f79e70cf00654b75ae27a9d9ad799090954e9
fa4f79e fix(qa): T-187 r3 prompt-log redaction: escaped forms, outside-repo omission, third-party and personal names, self-test
f17c991 feat(backend): T-179 D-066 disputed accept needs compared:true (422 COMPARE_REQUIRED, stored on the accept event, batch excludes); D-067 narrative never reaches letter or notes; classic keeps compare button, narrative hidden
85bcd22 fix(release): T-182 r3 README first command has no angle-bracket placeholder; live-config error prints one line with no demo-mode warning
6904b41 feat(release): T-194 deploy/make_public_snapshot.sh builds a redacted single-commit public snapshot from git archive HEAD
6d6dc45 fix(submission): T-185/T-186 r3 library numbers cite only library-latest.md; counts computed at 18bfa69 with re-run commands; D-065 wording, CHRIS marker, card refs
18bfa69 docs(release): T-182 r2 timing note for the claude_cli-excluded image emulation
commit 2e58e18f4e6800a5bebfb57eeb22fe57fa3efab8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:28:46 2026 -0600

    fix(backend): T-177 r3 every backend sentence for a prepared item says prepared answer (flag steps and why, failed and missing curated answers, run messages); /classic redirects to the guided UI in demo and public mode
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py                        |  17 ++-
 app/backend/generator.py                  |   2 +-
 app/backend/pipeline.py                   |   3 +-
 app/backend/present.py                    |  32 ++++-
 app/backend/trace.py                      |  70 ++++++++--
 app/backend/why.py                        |  40 ++++++
 app/llm/audited.py                        |   6 +
 memory/contracts/api.md                   |   1 +
 tests/unit/test_prepared_provenance_r3.py | 225 ++++++++++++++++++++++++++++++
 9 files changed, 377 insertions(+), 19 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:39.764Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_guard_blocks_shell_expansions.md"
}
````

### User / tool · 2026-11-02T21:49:39.774Z

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
21	**T-175 r2 addendum:** board-guard denied `git branch` for reviewers in the project ("allowed only in scratch repos under /tmp"). `git merge-base --is-ancestor <sha> HEAD` and `git log -S <string> -- <paths>` both ran. A plain `python3 -c "import time; time.sleep(100)"` in the foreground ran without a block, but it is a poor habit: check the background task instead.
22	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:40.098Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md"
}
````

### User / tool · 2026-11-02T21:49:40.105Z

**tool result**
````
1	---
2	name: feedback_review_write_once
3	description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
4	metadata:
5	  type: feedback
6	---
7	
8	Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.
9	
10	**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.
11	
12	**The ```json block belongs to the first Write.** T-084 r2 (this session): I wrote `reviews/T-084-staff-engineer-r2.md` without its json fence. The board-validate PostToolUse hook rejected it ("review must contain a ```json block"), and reviewer-write-guard refused the Edit that would have added it. The fix was a complete `-r3` file that says it supersedes the r2 file. **How to apply:** before the Write, count the fences (exactly one ```json block) and parse the block with `json.loads`; check the verdict against the rule.
13	
14	**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
15	
16	**T-141 r5 addendum:** the first Write carried one control claim I had not yet run ("V10 and W10 print info on 93a2ffc"). It was true, but the guard then refused an Edit to fix a muddled sentence about it. Run every "X prints Y on the control archive" claim before the first Write, and proof-read the evidence sentence, not only the JSON. Accurate-but-clumsy wording can stay, but it cannot be corrected in place. See [[project_t141_r5_patterns]].
17	
18	**T-173 r2 addendum:** the first Write had one clumsy sentence and one citation range one line too wide (conftest.py:208-211 for a guard at 208-210). Both stayed, because Edit was refused on the new file, and I did not work around the guard. Proof-read the body the same way as the JSON block before the Write, and read each cited range with `git show <sha>:<path> | sed -n` first. A shell line with a backtick inside a `python -c` string was denied by git-guard ("could not parse command safely"); put any fence or regex with backticks in a script file.
19	
20	**T-045 r3 addendum:** three function line ranges in the exercised list were written from memory of grep output (ship_bar 913-960 should be 913-955; render_md 1058-1092 should be 1093; check_fresh 1294-1313 should be 1315). The findings' own citations were grepped and correct. I did not work around the guard; the slip stays in the record. Run `grep -n "^def "` and `sed -n` on each range before the first Write, and list each range as you verified it. See [[project_t045_r3_record_latest_patterns]].
21	
22	**T-155 r2 / T-164 addendum:** two wrong body facts went out in first Writes: a file name (test_multicase.py for test_rerun_note.py) and "the card names X" when the card does not. Both were caught only after the Write. Before the first Write, grep each file name and each "the card says" phrase against `board.py show` output. The corrected records are `-r2b` and `-r1` files, and each names the file it corrects. See [[project_t155_r2_t164_patterns]].
23	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:42.972Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-177-staff-engineer-r3/archive && git archive 2e58e18 | tar -x -C artifacts/review-evidence/T-177-staff-engineer-r3/archive && echo 2e58e18 > artifacts/review-evidence/T-177-staff-engineer-r3/archive-source-sha.txt && ls artifacts/review-evidence/T-177-staff-engineer-r3/archive | head -30; ls -la .venv/bin/python; git show 2e58e18 -- app/ | wc -l"
}
````

### User / tool · 2026-11-02T21:49:43.925Z

**tool result**
````
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
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
     373
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:44.943Z

**tool call — Bash**
````
{
 "command": "git show 2e58e18 -- app/ memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T21:49:45.053Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:46.399Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/be03tj14p.txt"
}
````

### User / tool · 2026-11-02T21:49:46.601Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:48.857Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && ls T-177-staff-engineer-r2/ | head -50; sed -n 1,60p T-177-staff-engineer-r2/probe_r2.py; cat T-177-staff-engineer-r3/archive/run.sh | head -60"
}
````

### User / tool · 2026-11-02T21:49:48.947Z

**tool result**
````
__pycache__
archive
archive-source-sha.txt
check_review_json.py
e2e-provenance.out
mutate_r2.py
probe-r2-branch-missing.out
probe-r2-branch.out
probe-r2-export.out
probe-r2-flags-audit.out
probe-r2-flags.out
probe-r2.out
probe_r2.py
probe_r2_branch.py
probe_r2_export.py
probe_r2_flags.py
probe_r2_flags_audit.py
race-r2.out
race_r2.py
render-curated-flag-f_r3_1-why.png
render-curated-flag-f_r6_1-why.png
render-curated-judge-panel.png
render-curated-page.png
render-flags-r2.out
render-r2.out
render-recorded-judge-panel.png
render-recorded-page.png
render_flags_r2.py
render_r2.py
unit-prepared.out
"""T-177 r2 probe (staff-engineer-reviewer, round 2). Runs against the git archive copy (HEAD), not the shared app.
Usage: python -I probe_r2.py <archive_dir> <scratch_dir>
Starts an in-process TestClient with FIXTURE_SET=curated (prepared) and with the recorded set (control), and walks every
payload a reader can reach for the sample case, reporting drafting-model or 'AI draft' wording with the path it came from."""
import json
import os
import re
import sys
import time

ARCH, SCRATCH = sys.argv[1], sys.argv[2]
sys.path.insert(0, ARCH)
os.chdir(ARCH)

from fastapi.testclient import TestClient  # noqa: E402
from app.backend.api import create_app  # noqa: E402

PATTERNS = ["claude-sonnet", "AI draft", "AI drafted", "AI drafts", "AI-made", "Drafted by", "drafted by AI", "extract_v1", "prompt_sha256",
            "recorded AI answers", "first AI", "AI's drafts", "The AI read this record", "The AI drafted", "AI-written", "generated by"]


def make_client(db, fixture_set):
    os.environ["LLM_BACKEND"] = "fixture"
    os.environ["ZLAYT_MODE"] = "local"
    for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET"):
        os.environ.pop(k, None)
    if fixture_set:
        os.environ["FIXTURE_SET"] = fixture_set
    return TestClient(create_app(db, static_dir=os.path.join(ARCH, "app", "frontend")), client=("127.0.0.1", 50000))


def run_case(c):
    tok = c.post("/api/cases", json={"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    return tok, s["status"]


def hits(label, obj, out):
    text = json.dumps(obj, ensure_ascii=False)
    for p in PATTERNS:
        for m in re.finditer(re.escape(p), text):
            out.append((label, p, text[max(0, m.start() - 70): m.end() + 50]))


def walk(c, tok, tag, report):
    found = []
    for path in ["/api/health", f"/api/cases/{tok}", f"/api/cases/{tok}/judges", f"/api/cases/{tok}/audit", f"/api/cases/{tok}/trace",
                 f"/api/cases/{tok}/status", "/api/cases", f"/api/cases/{tok}/export"]:
        r = c.get(path)
        report.append(f"[{tag}] GET {path} -> {r.status_code}")
        if r.headers.get("content-type", "").startswith("application/json"):
            hits(f"{tag} GET {path}", r.json(), found)
    case = c.get(f"/api/cases/{tok}").json()
    ids = [x["id"] for x in case.get("entries", [])] + [x["id"] for x in case.get("amounts", [])] + [x["id"] for x in case.get("flags", [])]
    report.append(f"[{tag}] item ids: {len(ids)} ({len(case.get('entries', []))} entries)")
#!/bin/sh
# One command from a fresh clone to the guided UI in demo mode (no key, no network after the one-time install).
#   ./run.sh                 demo mode on http://127.0.0.1:7860   (PORT=7870 ./run.sh to change the port)
#   ./run.sh setup           create .venv and install requirements only
#   ./run.sh test            run the unit tests (installs requirements-dev.txt first)
# Live mode is opt-in: see README.md and .env.example. This script never reads or prints .env.
set -eu
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
  echo "Python 3.12+ is required (found: $("$PY" --version 2>&1)). Install it, or set PYTHON=/path/to/python3.12." >&2
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "Creating .venv and installing requirements (one time, about a minute)..."
  "$PY" -m venv .venv
fi
# Reinstall only when requirements.txt changed since the last successful install.
if [ ! -f .venv/.installed ] || [ requirements.txt -nt .venv/.installed ]; then
  .venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt
  touch .venv/.installed
fi

case "${1:-serve}" in
  setup)
    echo "Ready: .venv installed." ;;
  test)
    .venv/bin/pip install --quiet --disable-pip-version-check -r requirements-dev.txt
    exec .venv/bin/python -m pytest tests/unit -q ;;
  serve)
    # Demo defaults; a value you already exported wins.
    # On Replit (REPL_ID is set) the preview/published URL only reaches a process bound to 0.0.0.0.
    if [ -z "${HOST:-}" ] && [ -n "${REPL_ID:-}" ]; then HOST=0.0.0.0; fi
    export LLM_BACKEND="${LLM_BACKEND:-fixture}" FIXTURE_SET="${FIXTURE_SET:-curated}" HOST="${HOST:-127.0.0.1}" PORT="${PORT:-7860}"
    .venv/bin/python -m app.config
    # app.main prints "Serving on ..." once the port is free; a startup error is one line, not a traceback.
    exec .venv/bin/python -m app.main ;;
  *)
    echo "usage: ./run.sh [serve|setup|test]" >&2; exit 2 ;;
esac
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:53.991Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && sed -n 60,200p T-177-staff-engineer-r2/probe_r2.py; cd T-177-staff-engineer-r3/archive && grep -n \"def local_mode\\|def demo_mode\\|ZLAYT_MODE\" app/backend/api.py app/config.py app/main.py | head -30"
}
````

### User / tool · 2026-11-02T21:49:54.083Z

**tool result**
````
    report.append(f"[{tag}] item ids: {len(ids)} ({len(case.get('entries', []))} entries)")
    prep_items = 0
    for iid in ids:
        ir = c.get(f"/api/cases/{tok}/items/{iid}")
        if ir.status_code == 200:
            hits(f"{tag} GET items/{iid}", ir.json(), found)
            if (ir.json().get("item") or {}).get("prepared") is True:
                prep_items += 1
        tr = c.get(f"/api/cases/{tok}/items/{iid}/trace")
        if tr.status_code == 200:
            hits(f"{tag} GET items/{iid}/trace", tr.json(), found)
    report.append(f"[{tag}] items walked: {len(ids)}; prepared items: {prep_items}")
    return found


def prepared_trace_labels(c, tok, report):
    """Every item's generator step label and why, and any failure branch that says 'AI drafted' while evidence.model.prepared is true."""
    bad = []
    case = c.get(f"/api/cases/{tok}").json()
    for e in case.get("entries", []):
        tr = c.get(f"/api/cases/{tok}/items/{e['id']}/trace").json()
        gen = next((s for s in tr["steps"] if s["id"] == "extracted"), None)
        if gen is None:
            continue
        prepared = bool((gen.get("evidence") or {}).get("model", {}).get("prepared"))
        report.append(f"  item {e['id']} state={e.get('state')} step={gen.get('status')} prepared={prepared} label={gen.get('label')!r} model={(gen.get('evidence') or {}).get('model', {}).get('id')!r}")
        if prepared and "AI" in (gen.get("label") or ""):
            bad.append((e["id"], gen.get("status"), gen.get("label"), gen.get("why")))
    return bad


def main():
    out_lines = []
    cur_db = os.path.join(SCRATCH, "probe_curated.sqlite")
    rec_db = os.path.join(SCRATCH, "probe_recorded.sqlite")
    for p in (cur_db, rec_db):
        if os.path.exists(p):
            os.remove(p)

    c = make_client(cur_db, "curated")
    tok, st = run_case(c)
    out_lines.append(f"[curated] run status={st}")
    f_cur = walk(c, tok, "curated", out_lines)
    bad = prepared_trace_labels(c, tok, out_lines)
    out_lines.append(f"[curated] prepared generator steps labelled with 'AI': {len(bad)}")
    for b in bad:
        out_lines.append(f"  BAD {b}")
    out_lines.append(f"[curated] pattern hits in reachable payloads: {len(f_cur)}")
    for h in f_cur:
        out_lines.append(f"  HIT {h[0]} | {h[1]!r} | ...{h[2]}...")
    # the 'Why' ladder fields the UI shows for the first entry
    case = c.get(f"/api/cases/{tok}").json()
    if case.get("entries"):
        e1 = case["entries"][0]
        out_lines.append(f"[curated] entry {e1['id']} ladder.generator = {json.dumps(e1.get('ladder', {}).get('generator'), ensure_ascii=False)[:400]}")

    c2 = make_client(rec_db, None)
    tok2, st2 = run_case(c2)
    out_lines.append(f"[recorded] run status={st2}")
    f_rec = walk(c2, tok2, "recorded", out_lines)
    out_lines.append(f"[recorded] pattern hits (expected: AI labels and model ids present): {len(f_rec)}")
    for h in f_rec[:12]:
        out_lines.append(f"  HIT {h[0]} | {h[1]!r} | ...{h[2]}...")
    text = "\n".join(out_lines)
    print(text)


if __name__ == "__main__":
    main()
app/config.py:35:        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
app/backend/api.py:83:def local_mode() -> bool:
app/backend/api.py:84:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:116:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:127:    def demo_mode():
app/backend/api.py:640:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
app/backend/api.py:674:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/backend/api.py:700:                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:49:57.416Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"library\" app/backend/api.py | head -20; ls evals/golden | head -30; sed -n 1,60p app/main.py"
}
````

### User / tool · 2026-11-02T21:49:57.503Z

**tool result**
````
35:LIBRARY = ROOT / "evals" / "library"
66:def library_cases() -> list:
67:    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
68:    evals/golden until the library exists. [{id, name, description, path}]"""
105:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
280:    @app.get("/api/library")
281:    def library():
284:        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
291:        if isinstance(b.get("library"), str):
294:            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
296:                raise ApiError(404, "not_found", "No such library case.")
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens).

A startup misconfiguration (live opt-in without PROVIDER_CAP_CONFIRMED=1, a port already in use, ...) prints one line naming the
setting and exits non-zero; no traceback. Set ZLAYT_DEBUG=1 to get the traceback instead."""
import os
import sys

import uvicorn

from app.backend.api import create_app


def create():
    """uvicorn app.main:create --factory"""
    return create_app()


def _fail(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def main():
    from app import config
    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
    why = config.preflight()
    if why:
        _fail(why)
    try:
        app = create()
    except RuntimeError as e:                         # create_app's configuration refusals (cap flag, local-mode host); each message names the variable
        if os.environ.get("ZLAYT_DEBUG") == "1":
            raise
        _fail(str(e))
    if config.port_in_use(host, port):
        _fail(f"port {port} on {host} is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).", 3)
    print(f"Serving on http://{host}:{port}  (Ctrl-C to stop)", flush=True)
    uvicorn.run(app, host=host, port=port, access_log=False, log_level="warning")


if __name__ == "__main__":
    main()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:02.766Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && ls evals/library | head -20; lsof -nP -iTCP:54310 -iTCP:54311 -sTCP:LISTEN | head"
}
````

### User / tool · 2026-11-02T21:50:02.918Z

**tool result**
````
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:04.068Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && env -u ZLAYT_MODE -u ZLAYT_CLASSIC LLM_BACKEND=fixture FIXTURE_SET=curated HOST=127.0.0.1 PORT=54310 ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/demo.sqlite /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T21:50:04.126Z

**tool result**
````
Command running in background with ID: byqpomlaa. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/byqpomlaa.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:09.325Z

**tool call — Bash**
````
{
 "command": "lsof -nP -iTCP:54310 -sTCP:LISTEN; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/byqpomlaa.output; curl -s http://127.0.0.1:54310/api/health; echo; grep -n \"ZLAYT_DB\" artifacts/review-evidence/T-177-staff-engineer-r3/archive/app/backend/*.py artifacts/review-evidence/T-177-staff-engineer-r3/archive/app/db/*.py | head -3"
}
````

### User / tool · 2026-11-02T21:50:09.516Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  25329 arsis    9u  IPv4 0xb5b366f1bfee7596      0t0  TCP 127.0.0.1:54310 (LISTEN)
Serving on http://127.0.0.1:54310  (Ctrl-C to stop)
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
artifacts/review-evidence/T-177-staff-engineer-r3/archive/app/backend/api.py:98:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:10.691Z

**tool call — Bash**
````
{
 "command": "ps -p 25329 -o pid,ppid,command | cat; lsof -p 25329 -a -d cwd -Fn | cat"
}
````

### User / tool · 2026-11-02T21:50:10.828Z

**tool result**
````
  PID  PPID COMMAND
25329 25328 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
p25329
fcwd
n/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:15.741Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && sed -n 1,80p T-177-staff-engineer-r2/probe_r2_export.py"
}
````

### User / tool · 2026-11-02T21:50:15.815Z

**tool result**
````
"""T-177 r2 export probe (staff-engineer-reviewer). Curated set (prepared) and recorded set (control), archive copy only.
Accepts every entry, amount and flag the API lists as open (a POST per item, status recorded), then GET /export and reports the
provenance block and any model or AI-draft wording in the whole export payload.
Usage: python -I probe_r2_export.py <archive_dir> <scratch_dir>"""
import json
import os
import re
import sys
import time

ARCH, SCRATCH = sys.argv[1], sys.argv[2]
sys.path.insert(0, ARCH)
os.chdir(ARCH)

from fastapi.testclient import TestClient  # noqa: E402
from app.backend.api import create_app  # noqa: E402

WORDS = ["claude-sonnet", "claude-haiku", "hand-checked", "Drafted", "drafted by", "AI draft", "AI-made", "AI drafted", "prepared", "Prepared", "extract_v1", "prompt"]


def client(db, fixture_set):
    os.environ["LLM_BACKEND"] = "fixture"
    os.environ["ZLAYT_MODE"] = "local"
    for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET"):
        os.environ.pop(k, None)
    if fixture_set:
        os.environ["FIXTURE_SET"] = fixture_set
    if os.path.exists(db):
        os.remove(db)
    return TestClient(create_app(db, static_dir=os.path.join(ARCH, "app", "frontend")), client=("127.0.0.1", 50000))


def run(c):
    tok = c.post("/api/cases", json={"sample": True, "title": "export probe"}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    for _ in range(480):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    return tok, s["status"]


def accept_all(c, tok):
    case = c.get(f"/api/cases/{tok}").json()
    rows = []
    for key in ("entries", "amounts", "flags"):
        for x in case.get(key, []):
            if x.get("review_status") in ("accepted", "dismissed", "rejected") or x.get("state") == "rejected":
                continue
            r = c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
            rows.append((x["id"], r.status_code, (r.json() if r.status_code != 200 else {}).get("error", {}).get("code") if r.status_code != 200 else "ok"))
    return rows


def report(tag, c, tok, out):
    rows = accept_all(c, tok)
    out.append(f"[{tag}] accept calls: {len(rows)}; statuses: {sorted(set(r[1] for r in rows))}")
    for r in rows:
        if r[1] != 200:
            out.append(f"  [{tag}] accept {r[0]} -> {r[1]} {r[2]}")
    e = c.get(f"/api/cases/{tok}/export")
    out.append(f"[{tag}] GET export -> {e.status_code}")
    if e.status_code != 200:
        out.append(f"  body: {e.text[:300]}")
        return
    j = e.json()
    out.append(f"[{tag}] provenance: " + json.dumps(j.get("provenance"), ensure_ascii=False))
    text = json.dumps(j, ensure_ascii=False)
    for w in WORDS:
        hits = [text[max(0, m.start() - 60): m.end() + 40] for m in re.finditer(re.escape(w), text)]
        if hits:
            out.append(f"[{tag}] word {w!r}: {len(hits)} hit(s); first: ...{hits[0]}...")


def main():
    out = []
    c = client(os.path.join(SCRATCH, "export_curated.sqlite"), "curated")
    tok, st = run(c)
    out.append(f"[curated] run status={st}")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:31.446Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_http.py",
 "content": "\"\"\"T-177 r3 probe (staff-engineer-reviewer). HTTP only (urllib), against my own server from the git archive of 2e58e18.\nUsage: python -I probe_r3_http.py <base_url> <tag> <case_spec>...   case_spec = sample | lib:<library id>\nFor each case: create, run, wait, GET every payload (health, case, judges, audit, trace, status, export after accept-all, every item and item trace),\nand report authorship wording on the payload: 'AI drafted/found/...' and model names. The D-065 phrase 'standing in for the AI draft' is removed first.\"\"\"\nimport json\nimport re\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE, TAG = sys.argv[1].rstrip(\"/\"), sys.argv[2]\nSPECS = sys.argv[3:]\nD065 = \"standing in for the AI draft\"\nPAT = re.compile(r\"AI draft|AI drafted|AI found|AI proposed|AI wrote|AI-made|AI-written|AI suggested|AI read|AI translat|AI step|AI output|AI wording|AI's|The AI |the AI |Drafted by|claude-sonnet|drafted with AI|first AI|recorded AI|generated by\")\n\n\ndef call(method, path, body=None):\n    data = None if body is None else json.dumps(body).encode()\n    req = urllib.request.Request(BASE + path, data=data, method=method, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            raw = r.read().decode()\n            try:\n                return r.status, json.loads(raw)\n            except ValueError:\n                return r.status, raw\n    except urllib.error.HTTPError as e:\n        raw = e.read().decode()\n        try:\n            return e.code, json.loads(raw)\n        except ValueError:\n            return e.code, raw\n\n\ndef scan(label, obj, found):\n    text = json.dumps(obj, ensure_ascii=False).replace(D065, \"<D065>\")\n    for m in PAT.finditer(text):\n        found.append((label, m.group(0), text[max(0, m.start() - 80): m.end() + 60]))\n\n\ndef main():\n    s, h = call(\"GET\", \"/api/health\")\n    print(f\"[{TAG}] GET /api/health -> {s}: answers={h.get('answers')} models={h.get('models')}\")\n    for spec in SPECS:\n        body = {\"sample\": True, \"title\": \"r3 probe\"} if spec == \"sample\" else {\"library\": spec.split(\":\", 1)[1], \"title\": \"r3 probe\"}\n        s, c = call(\"POST\", \"/api/cases\", body)\n        if s not in (200, 201):\n            print(f\"[{TAG}/{spec}] create -> {s} {c}\")\n            continue\n        tok = c[\"token\"]\n        s, _ = call(\"POST\", f\"/api/cases/{tok}/run\", {})\n        st = None\n        for _ in range(600):\n            _, stt = call(\"GET\", f\"/api/cases/{tok}/status\")\n            st = stt[\"status\"]\n            if st in (\"ready\", \"failed\"):\n                break\n            time.sleep(0.25)\n        print(f\"[{TAG}/{spec}] run POST -> {s}; status={st}\")\n        found = []\n        _, case = call(\"GET\", f\"/api/cases/{tok}\")\n        ids = [x[\"id\"] for k in (\"entries\", \"amounts\", \"flags\") for x in case.get(k, [])]\n        counts = {k: len(case.get(k, [])) for k in (\"entries\", \"amounts\", \"flags\")}\n        prepared = sum(1 for k in (\"entries\", \"amounts\", \"flags\") for x in case.get(k, []) if x.get(\"prepared\") is True)\n        print(f\"[{TAG}/{spec}] items {counts}; prepared==True on {prepared}; case.models={case.get('models')}\")\n        for path in (f\"/api/cases/{tok}\", f\"/api/cases/{tok}/judges\", f\"/api/cases/{tok}/audit\", f\"/api/cases/{tok}/trace\", f\"/api/cases/{tok}/status\"):\n            r, j = call(\"GET\", path)\n            scan(f\"GET {path.replace(tok, '<tok>')} ({r})\", j, found)\n        n_items = n_tr = 0\n        for iid in ids:\n            r, j = call(\"GET\", f\"/api/cases/{tok}/items/{iid}\")\n            if r == 200:\n                n_items += 1\n                scan(f\"item {iid}\", j, found)\n            r, j = call(\"GET\", f\"/api/cases/{tok}/items/{iid}/trace\")\n            if r == 200:\n                n_tr += 1\n                scan(f\"trace {iid}\", j, found)\n        # accept all that can be accepted, then export\n        acc = 0\n        for iid in ids:\n            r, _ = call(\"POST\", f\"/api/cases/{tok}/items/{iid}/review\", {\"action\": \"accept\"})\n            acc += 1 if r == 200 else 0\n        r, ex = call(\"GET\", f\"/api/cases/{tok}/export\")\n        scan(f\"GET export ({r})\", ex, found)\n        print(f\"[{TAG}/{spec}] item GETs ok={n_items}, trace GETs ok={n_tr}, accepted={acc}, export status={r}\")\n        if isinstance(ex, dict):\n            print(f\"[{TAG}/{spec}] export provenance={json.dumps(ex.get('provenance'), ensure_ascii=False)[:500]}\")\n        # judge panel surfaces\n        by = {}\n        for h2 in found:\n            by.setdefault((h2[0].split(' ')[0] if h2[0].startswith(('item', 'trace')) else h2[0], h2[1]), []).append(h2)\n        print(f\"[{TAG}/{spec}] authorship-pattern hits: {len(found)}\")\n        for (src, pat), hs in sorted(by.items()):\n            print(f\"  {src} | {pat!r} x{len(hs)} | first: {hs[0][0]} ...{hs[0][2]}...\")\n        print(f\"[{TAG}/{spec}] DONE\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:50:31.546Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_http.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:33.486Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_http.py http://127.0.0.1:54310 curated-demo sample lib:case_lib01_er_only_then_gap lib:case_lib02_slip_fall_prior_knee > probe-r3-curated.out; head -c 9000 probe-r3-curated.out",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T21:50:34.419Z

**tool result**
````
[curated-demo] GET /api/health -> 200: answers=prepared models={'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
[curated-demo/sample] run POST -> 202; status=ready
[curated-demo/sample] items {'entries': 9, 'amounts': 4, 'flags': 10}; prepared==True on 16; case.models={'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
[curated-demo/sample] item GETs ok=23, trace GETs ok=23, accepted=23, export status=200
[curated-demo/sample] export provenance={"generator_model": "hand-checked (qa)", "judge_model": "claude-haiku-5-5", "generator_prepared": true, "backend": "fixture", "recorded_from": "curated", "demo_mode": true, "prompt_versions": ["judge_amount_class_v1", "judge_conflict_v6", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated-demo/sample] authorship-pattern hits: 2
  GET /api/cases/<tok>/trace (200) | 'the AI ' x1 | first: GET /api/cases/<tok>/trace (200) ...unt": 23, "why": "23 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "...
  GET export (200) | 'drafted with AI' x1 | first: GET export (200) ...ternal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section was accepte...
[curated-demo/sample] DONE
[curated-demo/lib:case_lib01_er_only_then_gap] create -> 404 {'error': {'code': 'not_found', 'message': 'Not found.', 'detail': {}}}
[curated-demo/lib:case_lib02_slip_fall_prior_knee] create -> 404 {'error': {'code': 'not_found', 'message': 'Not found.', 'detail': {}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:38.415Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:54310/api/library | head -c 1200"
}
````

### User / tool · 2026-11-02T21:50:38.503Z

**tool result**
````
{"error":{"code":"not_found","message":"Not found.","detail":{}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:39.705Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 62,110p app/backend/api.py; sed -n 278,310p app/backend/api.py"
}
````

### User / tool · 2026-11-02T21:50:39.791Z

**tool result**
````
def recorded_hashes() -> set:
    return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}


def library_cases() -> list:
    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
    evals/golden until the library exists. [{id, name, description, path}]"""
    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
    out = []
    for p in sorted(base.glob("*.txt")):
        meta = {}
        ej = p.with_name(p.stem + ".expected.json")
        if ej.exists():
            try:
                meta = json.loads(ej.read_text())
            except ValueError:
                meta = {}
        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
    return out


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"


def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
    host = request.client.host if request.client else None
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback


def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    rejudging = set()
    _boot = DB.connect(db_path)
    try:
        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
            c.close()

    @app.get("/api/library")
    def library():
        if not local_mode():
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
        b = await body_of(request)
        sample = b.get("sample") is True
        lib = None
        if isinstance(b.get("library"), str):
            if not local_mode():
                raise ApiError(404, "not_found", "Not found.")
            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
            if lib is None:
                raise ApiError(404, "not_found", "No such library case.")
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        typed = isinstance(b.get("title"), str)
        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)

    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        valid_name(title if title is not None else name, title is not None)          # T-157 r2: a markup title is refused before a byte is read
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:43.173Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && env -u ZLAYT_CLASSIC ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated HOST=127.0.0.1 PORT=54311 ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/local.sqlite /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T21:50:43.242Z

**tool result**
````
Command running in background with ID: bky7g7lx5. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bky7g7lx5.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:45.894Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && lsof -nP -iTCP:54311 -sTCP:LISTEN | cat; for p in /classic /classic/ /; do echo \"local $p\"; curl -s -o /dev/null -w \"%{http_code} %{redirect_url}\\n\" http://127.0.0.1:54311$p; echo \"demo $p\"; curl -s -o /dev/null -w \"%{http_code} %{redirect_url}\\n\" http://127.0.0.1:54310$p; done; curl -s -o /dev/null -w \"demo /classic/index.html %{http_code} %{redirect_url}\\n\" http://127.0.0.1:54310/classic/index.html; curl -s -o /dev/null -w \"demo /classic/app.js %{http_code} %{redirect_url}\\n\" http://127.0.0.1:54310/classic/app.js; curl -s -o /dev/null -w \"local /classic/app.js %{http_code}\\n\" http://127.0.0.1:54311/classic/app.js; curl -s http://127.0.0.1:54311/classic/ | head -c 300"
}
````

### User / tool · 2026-11-02T21:50:46.149Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  26866 arsis    9u  IPv4 0x20fbaf4774bcbc05      0t0  TCP 127.0.0.1:54311 (LISTEN)
local /classic
307 http://127.0.0.1:54311/classic/
demo /classic
307 http://127.0.0.1:54310/
local /classic/
200 
demo /classic/
307 http://127.0.0.1:54310/
local /
200 
demo /
200 
demo /classic/index.html 307 http://127.0.0.1:54310/
demo /classic/app.js 307 http://127.0.0.1:54310/
local /classic/app.js 200
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment timeline</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="review.css">
<link re
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:49.434Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_http.py http://127.0.0.1:54311 curated-local sample lib:case_lib01_er_only_then_gap lib:case_lib02_slip_fall_prior_knee lib:case_lib09_spanish_interpreter_espalda lib:case_lib10_eob_ub04_cms1500 > probe-r3-curated-local.out; cat probe-r3-curated-local.out | cut -c1-900",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:50:52.990Z

**tool result**
````
[curated-local] GET /api/health -> 200: answers=prepared models={'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
[curated-local/sample] run POST -> 202; status=ready
[curated-local/sample] items {'entries': 9, 'amounts': 4, 'flags': 10}; prepared==True on 16; case.models={'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
[curated-local/sample] item GETs ok=23, trace GETs ok=23, accepted=23, export status=200
[curated-local/sample] export provenance={"generator_model": "hand-checked (qa)", "judge_model": "claude-haiku-5-5", "generator_prepared": true, "backend": "fixture", "recorded_from": "curated", "demo_mode": true, "prompt_versions": ["judge_amount_class_v1", "judge_conflict_v6", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated-local/sample] authorship-pattern hits: 2
  GET /api/cases/<tok>/trace (200) | 'the AI ' x1 | first: GET /api/cases/<tok>/trace (200) ...unt": 23, "why": "23 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "...
  GET export (200) | 'drafted with AI' x1 | first: GET export (200) ...ternal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section was accepte...
[curated-local/sample] DONE
[curated-local/lib:case_lib01_er_only_then_gap] run POST -> 202; status=ready
[curated-local/lib:case_lib01_er_only_then_gap] items {'entries': 6, 'amounts': 2, 'flags': 2}; prepared==True on 0; case.models={'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
[curated-local/lib:case_lib01_er_only_then_gap] item GETs ok=10, trace GETs ok=10, accepted=10, export status=200
[curated-local/lib:case_lib01_er_only_then_gap] export provenance={"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "backend": "fixture", "recorded_from": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated-local/lib:case_lib01_er_only_then_gap] authorship-pattern hits: 97
  GET /api/cases/<tok> (200) | 'The AI ' x3 | first: GET /api/cases/<tok> (200) ...ll}, {"id": "f_r3_1", "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "The AI found this flag but the phrase list did not; check that it a...
  GET /api/cases/<tok> (200) | 'claude-sonnet' x7 | first: GET /api/cases/<tok> (200) ...us": "ready", "demo_mode": true, "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok> (200) | 'the AI ' x1 | first: GET /api/cases/<tok> (200) ...ixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.", ...
  GET /api/cases/<tok>/audit (200) | 'claude-sonnet' x24 | first: GET /api/cases/<tok>/audit (200) ...ct", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T02:34:36Z"}, "model": "cla...
  GET /api/cases/<tok>/judges (200) | 'The AI ' x1 | first: GET /api/cases/<tok>/judges (200) ...rces_disagree", "code_says": "The phrase list did not find it.", "judge_says": "The AI found it.", "resolution": "needs_review", "review_status": "...
  GET /api/cases/<tok>/judges (200) | 'claude-sonnet' x1 | first: GET /api/cases/<tok>/judges (200) ...{"token": "YNw6-kghhF28QwmIJyV3Kw", "mode": "full", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok>/trace (200) | 'AI draft' x1 | first: GET /api/cases/<tok>/trace (200) ...firmed": 0, "ambiguous": 0, "missing": 0}, "n": 3}, {"id": "extract", "label": "AI drafts a summary and a quote for each record", "kind": "llm", "st...
  GET /api/cases/<tok>/trace (200) | 'AI-made' x1 | first: GET /api/cases/<tok>/trace (200) ...0, "reasons": {}}, "n": 5}, {"id": "judges", "label": "Second AI check on every AI-made item", "kind": "llm", "status": "pass", "why": "The second ...
  GET /api/cases/<tok>/trace (200) | 'The AI ' x1 | first: GET /api/cases/<tok>/trace (200) ... summary and a quote for each record", "kind": "llm", "status": "pass", "why": "The AI drafted an entry for all 6 records.", "reason_code": null, "...
  GET /api/cases/<tok>/trace (200) | 'the AI ' x1 | first: GET /api/cases/<tok>/trace (200) ...unt": 10, "why": "10 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "...
  GET export (200) | 'claude-sonnet' x1 | first: GET export (200) ...nfirmed": 0, "dismissed": 0, "rejected": 0}, "provenance": {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepare...
  GET export (200) | 'drafted with AI' x1 | first: GET export (200) ...ternal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section was accepte...
  item | 'The AI ' x1 | first: item f_r3_1 ...em": {"id": "f_r3_1", "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "The AI found this flag but the phrase list did not; check that it a...
  item | 'claude-sonnet' x18 | first: item e1 ...okens_not_in_excerpt": []}, "generator": {"call_id": "ca6d3aec0d11a", "model": "claude-sonnet-5-5", "output": {"excerpt": "Driver of a sedan struck from ...
  trace | 'AI draft' x6 | first: trace e1 ...tions": ["accept", "edit", "dismiss"]}, "steps": [{"id": "extracted", "label": "AI drafted a summary and picked a quote", "kind": "llm", "status": "...
  trace | 'AI found' x1 | first: trace f_r3_1 ...evidence": {}, "next_action": null, "n": 1}, {"id": "proposed_by_ai", "label": "AI found it", "kind": "llm", "status": "pass", "why": "The AI propos...
  trace | "AI's" x2 | first: trace e2 ..., "status": "pass", "why": "Code removed ‘ED charge $3,915’ from the end of the AI's summary. Why: it states a dollar amount, and the shortened ...
  trace | 'The AI ' x10 | first: trace e1 ...drafted a summary and picked a quote", "kind": "llm", "status": "pass", "why": "The AI read this record and proposed a one-line summary and a quote...
  trace | 'claude-sonnet' x14 | first: trace e1 ...": null, "rule": "row 4", "blocks_export": false, "evidence": {"model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null...
  trace | 'the AI ' x2 | first: trace e2 ...de", "status": "pass", "why": "Code removed ‘ED charge: $3,915.’ from the quote the AI picked. Why: it states a dollar amount. Amounts go only in t...
[curated-local/lib:case_lib01_er_only_then_gap] DONE
[curated-local/lib:case_lib02_slip_fall_prior_knee] run POST -> 202; status=ready
[curated-local/lib:case_lib02_slip_fall_prior_knee] items {'entries': 7, 'amounts': 3, 'flags': 8}; prepared==True on 0; case.models={'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
[curated-local/lib:case_lib02_slip_fall_prior_knee] item GETs ok=18, trace GETs ok=18, accepted=17, export status=200
[curated-local/lib:case_lib02_slip_fall_prior_knee] export provenance={"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "backend": "fixture", "recorded_from": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated-local/lib:case_lib02_slip_fall_prior_knee] authorship-pattern hits: 153
  GET /api/cases/<tok> (200) | 'The AI ' x6 | first: GET /api/cases/<tok> (200) ...ll}, {"id": "f_r2_1", "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "The AI found this flag but the phrase list did not; check that it a...
  GET /api/cases/<tok> (200) | 'claude-sonnet' x8 | first: GET /api/cases/<tok> (200) ...us": "ready", "demo_mode": true, "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok> (200) | 'the AI ' x2 | first: GET /api/cases/<tok> (200) ...view", "reasons": ["LEXICON_ONLY"], "why": "The phrase list found this flag but the AI did not; check that it applies.", "review_status": "pending"...
  GET /api/cases/<tok>/audit (200) | 'claude-sonnet' x28 | first: GET /api/cases/<tok>/audit (200) ...ct", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T02:29:11Z"}, "model": "cla...
  GET /api/cases/<tok>/judges (200) | 'The AI ' x5 | first: GET /api/cases/<tok>/judges (200) ...rces_disagree", "code_says": "The phrase list did not find it.", "judge_says": "The AI found it.", "resolution": "needs_review", "review_status": "...
  GET /api/cases/<tok>/judges (200) | 'claude-sonnet' x1 | first: GET /api/cases/<tok>/judges (200) ...{"token": "Izfs-5c54UKSbFBTwvQiCA", "mode": "full", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok>/trace (200) | 'AI draft' x1 | first: GET /api/cases/<tok>/trace (200) ...firmed": 0, "ambiguous": 0, "missing": 0}, "n": 3}, {"id": "extract", "label": "AI drafts a summary and a quote for each record", "kind": "llm", "st...
  GET /api/cases/<tok>/trace (200) | 'AI-made' x1 | first: GET /api/cases/<tok>/trace (200) ...1, "reasons": {}}, "n": 5}, {"id": "judges", "label": "Second AI check on every AI-made item", "kind": "llm", "status": "fail", "why": "1 item has ...
  GET /api/cases/<tok>/trace (200) | 'The AI ' x1 | first: GET /api/cases/<tok>/trace (200) ... summary and a quote for each record", "kind": "llm", "status": "pass", "why": "The AI drafted an entry for all 7 records.", "reason_code": null, "...
  GET /api/cases/<tok>/trace (200) | 'the AI ' x1 | first: GET /api/cases/<tok>/trace (200) ...unt": 18, "why": "18 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "...
  GET export (200) | 'claude-sonnet' x1 | first: GET export (200) ...nfirmed": 0, "dismissed": 0, "rejected": 0}, "provenance": {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepare...
  GET export (200) | 'drafted with AI' x1 | first: GET export (200) ...ternal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section was accepte...
  item | 'The AI ' x3 | first: item f_r2_1 ...em": {"id": "f_r2_1", "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "The AI found this flag but the phrase list did not; check that it a...
  item | 'claude-sonnet' x21 | first: item e1 ...okens_not_in_excerpt": []}, "generator": {"call_id": "c5debc4558f20", "model": "claude-sonnet-5-5", "output": {"excerpt": "Customer slipped on a wet floo...
  item | 'the AI ' x1 | first: item f_r5_2 ...view", "reasons": ["LEXICON_ONLY"], "why": "The phrase list found this flag but the AI did not; check that it applies.", "review_status": "pending"...
  trace | 'AI draft' x7 | first: trace e1 ...tions": ["accept", "edit", "dismiss"]}, "steps": [{"id": "extracted", "label": "AI drafted a summary and picked a quote", "kind": "llm", "status": "...
  trace | 'AI found' x7 | first: trace f_r2_1 ...evidence": {}, "next_action": null, "n": 1}, {"id": "proposed_by_ai", "label": "AI found it", "kind": "llm", "status": "pass", "why": "The AI propos...
  trace | "AI's" x2 | first: trace e4 ... "status": "pass", "why": "Code removed ‘MRI charge $1,850’ from the end of the AI's summary. Why: it states a dollar amount, and the shortened ...
  trace | 'The AI ' x22 | first: trace e1 ...drafted a summary and picked a quote", "kind": "llm", "status": "pass", "why": "The AI read this record and proposed a one-line summary and a quote...
  trace | 'claude-sonnet' x26 | first: trace e1 ...": null, "rule": "row 4", "blocks_export": false, "evidence": {"model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null...
  trace | 'the AI ' x8 | first: trace e4 ...e", "status": "pass", "why": "Code removed ‘MRI charge: $1,850.’ from the quote the AI picked. Why: it states a dollar amount. Amounts go only in t...
[curated-local/lib:case_lib02_slip_fall_prior_knee] DONE
[curated-local/lib:case_lib09_spanish_interpreter_espalda] run POST -> 202; status=ready
[curated-local/lib:case_lib09_spanish_interpreter_espalda] items {'entries': 6, 'amounts': 7, 'flags': 5}; prepared==True on 0; case.models={'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
[curated-local/lib:case_lib09_spanish_interpreter_espalda] item GETs ok=18, trace GETs ok=18, accepted=17, export status=200
[curated-local/lib:case_lib09_spanish_interpreter_espalda] export provenance={"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "backend": "fixture", "recorded_from": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_es_v1", "extract_v1", "flags_v1", "judge_amount_class_v1", "judge_faithfulness_es_v1", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated-local/lib:case_lib09_spanish_interpreter_espalda] authorship-pattern hits: 180
  GET /api/cases/<tok> (200) | 'AI translat' x24 | first: GET /api/cases/<tok> (200) ... two ways; confirm which one is right. It is left out of gap checks until then. AI translation — check against the original. This comes from a Spanish ...
  GET /api/cases/<tok> (200) | 'The AI ' x4 | first: GET /api/cases/<tok> (200) ...se}, {"id": "f_r1_1", "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "The AI found this flag but the phrase list did not; check that it a...
  GET /api/cases/<tok> (200) | 'claude-sonnet' x8 | first: GET /api/cases/<tok> (200) ...us": "ready", "demo_mode": true, "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok> (200) | 'the AI ' x1 | first: GET /api/cases/<tok> (200) ...ixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.", ...
  GET /api/cases/<tok>/audit (200) | 'AI translat' x6 | first: GET /api/cases/<tok>/audit (200) ..., that translates only what your excerpt says. Plain clinical wording. It is an AI translation: the software labels it as one.\n- Add nothing: no diagn...
  GET /api/cases/<tok>/audit (200) | 'claude-sonnet' x28 | first: GET /api/cases/<tok>/audit (200) ...ct", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T04:18:40Z"}, "model": "cla...
  GET /api/cases/<tok>/judges (200) | 'The AI ' x3 | first: GET /api/cases/<tok>/judges (200) ...rces_disagree", "code_says": "The phrase list did not find it.", "judge_says": "The AI found it.", "resolution": "needs_review", "review_status": "...
  GET /api/cases/<tok>/judges (200) | 'claude-sonnet' x1 | first: GET /api/cases/<tok>/judges (200) ...{"token": "4OnLuOhxyE2ZIIucXFoWDA", "mode": "full", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok>/trace (200) | 'AI draft' x1 | first: GET /api/cases/<tok>/trace (200) ...firmed": 0, "ambiguous": 1, "missing": 0}, "n": 3}, {"id": "extract", "label": "AI drafts a summary and a quote for each record", "kind": "llm", "st...
  GET /api/cases/<tok>/trace (200) | 'AI-made' x1 | first: GET /api/cases/<tok>/trace (200) ...0, "reasons": {}}, "n": 5}, {"id": "judges", "label": "Second AI check on every AI-made item", "kind": "llm", "status": "fail", "why": "The second ...
  GET /api/cases/<tok>/trace (200) | 'The AI ' x1 | first: GET /api/cases/<tok>/trace (200) ... summary and a quote for each record", "kind": "llm", "status": "pass", "why": "The AI drafted an entry for all 7 records.", "reason_code": null, "...
  GET /api/cases/<tok>/trace (200) | 'the AI ' x1 | first: GET /api/cases/<tok>/trace (200) ...unt": 19, "why": "19 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "...
  GET export (200) | 'AI translat' x1 | first: GET export (200) ...la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas.\"\n[AI translation of the Spanish original; check before sending]\n\nApril ...
  GET export (200) | 'claude-sonnet' x1 | first: GET export (200) ...nfirmed": 0, "dismissed": 0, "rejected": 0}, "provenance": {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepare...
  GET export (200) | 'drafted with AI' x1 | first: GET export (200) ...ternal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section was accepte...
  item | 'AI translat' x18 | first: item e2 ...": {"id": "e2", "state": "needs_review", "reasons": ["AI_TRANSLATION"], "why": "AI translation — check against the original. This comes from a Spanish ...
  item | 'The AI ' x3 | first: item f_r1_1 ...em": {"id": "f_r1_1", "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "The AI found this flag but the phrase list did not; check that it a...
  item | 'claude-sonnet' x18 | first: item e1 ...ed": ["ED charge $2,940"]}, "generator": {"call_id": "cb5e59430c1fd", "model": "claude-sonnet-5-5", "output": {"excerpt": "Left shoulder pain 7/10. X-ray...
  trace | 'AI draft' x6 | first: trace e1 ...tions": ["accept", "edit", "dismiss"]}, "steps": [{"id": "extracted", "label": "AI drafted a summary and picked a quote", "kind": "llm", "status": "...
  trace | 'AI found' x3 | first: trace f_r1_1 ...evidence": {}, "next_action": null, "n": 1}, {"id": "proposed_by_ai", "label": "AI found it", "kind": "llm", "status": "pass", "why": "The AI propos...
  trace | 'AI translat' x10 | first: trace e2 ...review_status": "pending", "state_reasons": [{"code": "AI_TRANSLATION", "why": "AI translation — check against the original. This comes from a Spanish ...
  trace | "AI's" x2 | first: trace e1 ..., "status": "pass", "why": "Code removed ‘ED charge $2,940’ from the end of the AI's summary. Why: it states a dollar amount, and the shortened ...
  trace | 'The AI ' x18 | first: trace e1 ...drafted a summary and picked a quote", "kind": "llm", "status": "pass", "why": "The AI read this record and proposed a one-line summary and a quote...
  trace | 'claude-sonnet' x18 | first: trace e1 ...": null, "rule": "row 4", "blocks_export": false, "evidence": {"model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null...
  trace | 'the AI ' x2 | first: trace e1 ...de", "status": "pass", "why": "Code removed ‘ED charge: $2,940.’ from the quote the AI picked. Why: it states a dollar amount. Amounts go only in t...
[curated-local/lib:case_lib09_spanish_interpreter_espalda] DONE
[curated-local/lib:case_lib10_eob_ub04_cms1500] run POST -> 202; status=ready
[curated-local/lib:case_lib10_eob_ub04_cms1500] items {'entries': 9, 'amounts': 11, 'flags': 2}; prepared==True on 0; case.models={'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
[curated-local/lib:case_lib10_eob_ub04_cms1500] item GETs ok=22, trace GETs ok=22, accepted=21, export status=200
[curated-local/lib:case_lib10_eob_ub04_cms1500] export provenance={"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepared": false, "backend": "fixture", "recorded_from": "claude-cli", "demo_mode": true, "prompt_versions": ["extract_v1", "flags_v1", "judge_amount_class_v1", "judge_faithfulness_v1", "judge_flag_v3"], "edited_count": 0}
[curated-local/lib:case_lib10_eob_ub04_cms1500] authorship-pattern hits: 126
  GET /api/cases/<tok> (200) | 'The AI ' x1 | first: GET /api/cases/<tok> (200) ...ord_ids": ["r2"], "state": "rejected", "reasons": ["FILTERED_BY_RULE"], "why": "The AI proposed this as a flag, but a fixed rule filtered it out (s...
  GET /api/cases/<tok> (200) | 'claude-sonnet' x10 | first: GET /api/cases/<tok> (200) ...us": "ready", "demo_mode": true, "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok> (200) | 'the AI ' x1 | first: GET /api/cases/<tok> (200) ...ixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.", ...
  GET /api/cases/<tok>/audit (200) | 'claude-sonnet' x36 | first: GET /api/cases/<tok>/audit (200) ...ct", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5", "recorded_at": "2026-11-02T04:16:20Z"}, "model": "cla...
  GET /api/cases/<tok>/judges (200) | 'claude-sonnet' x1 | first: GET /api/cases/<tok>/judges (200) ...{"token": "I1qnPGOwUK47razPuU-eBA", "mode": "full", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": fa...
  GET /api/cases/<tok>/trace (200) | 'AI draft' x1 | first: GET /api/cases/<tok>/trace (200) ...firmed": 0, "ambiguous": 0, "missing": 0}, "n": 3}, {"id": "extract", "label": "AI drafts a summary and a quote for each record", "kind": "llm", "st...
  GET /api/cases/<tok>/trace (200) | 'AI-made' x1 | first: GET /api/cases/<tok>/trace (200) ...0, "reasons": {}}, "n": 5}, {"id": "judges", "label": "Second AI check on every AI-made item", "kind": "llm", "status": "fail", "why": "The second ...
  GET /api/cases/<tok>/trace (200) | 'The AI ' x1 | first: GET /api/cases/<tok>/trace (200) ... summary and a quote for each record", "kind": "llm", "status": "pass", "why": "The AI drafted an entry for all 9 records.", "reason_code": null, "...
  GET /api/cases/<tok>/trace (200) | 'the AI ' x1 | first: GET /api/cases/<tok>/trace (200) ...unt": 22, "why": "22 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "...
  GET export (200) | 'claude-sonnet' x1 | first: GET export (200) ...nfirmed": 0, "dismissed": 0, "rejected": 0}, "provenance": {"generator_model": "claude-sonnet-5-5", "judge_model": "claude-haiku-5-5", "generator_prepare...
  GET export (200) | 'drafted with AI' x1 | first: GET export (200) ...ternal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section was accepte...
  item | 'claude-sonnet' x27 | first: item e1 ...okens_not_in_excerpt": []}, "generator": {"call_id": "c2966b86aede0", "model": "claude-sonnet-5-5", "output": {"excerpt": "Pt states chest wall and left ...
  trace | 'AI draft' x9 | first: trace e1 ...if you agree with it, or dismiss it."}, "steps": [{"id": "extracted", "label": "AI drafted a summary and picked a quote", "kind": "llm", "status": "...
  trace | 'AI found' x1 | first: trace f_r1_1 ...at scene."}]}, "next_action": null, "n": 1}, {"id": "proposed_by_ai", "label": "AI found it", "kind": "llm", "status": "pass", "why": "The AI propos...
  trace | "AI's" x1 | first: trace e6 ... $4,413.50’ ‘plan paid $3,530.80’ ‘patient may owe $882.70’ from the end of the AI's summary. Why: it states a dollar amount, and the shortened ...
  trace | 'The AI ' x10 | first: trace e1 ...drafted a summary and picked a quote", "kind": "llm", "status": "pass", "why": "The AI read this record and proposed a one-line summary and a quote...
  trace | 'claude-sonnet' x20 | first: trace e1 ...": null, "rule": "row 4", "blocks_export": false, "evidence": {"model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null...
  trace | 'the AI ' x3 | first: trace e4 ...FL47 total charges $712.00.’ ‘Rev 0001 total charges $8,123.50.’ from the quote the AI picked. Why: it states a dollar amount. Amounts go only in t...
[curated-local/lib:case_lib10_eob_ub04_cms1500] DONE
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:50:59.380Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 1,60p app/llm/backends/fixture.py; ls evals/fixtures 2>/dev/null | head; "
}
````

### User / tool · 2026-11-02T21:50:59.473Z

**tool result**
````
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:11.371Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"drafted with AI\\|AI assistance\\|disclosure\" app/backend/export.py | head -20; grep -n \"D-009\" memory/ORCHESTRATOR_DECISIONS.md | head -3; grep -n \"AI wording\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T21:51:11.468Z

**tool result**
````
29:AI_LINE = ("This chronology was drafted with AI assistance; every item in the treatment section was accepted "
857:    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""
17:| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. (Listed under "Decided by the team" in NEEDS_CHRIS.) | Candor without telling the carrier how the chronology was made. | T-014 privacy |
app/backend/export.py:661:            if e.get("original_summary_failed"):        # D-051: AI wording that failed a code check is not printed anywhere in the export
app/backend/export.py:662:                bits.append(f'summary was AI wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
app/backend/export.py:719:            lines.append(f'- AI wording removed (failed a check: {_removed_why(r)}) ({r["entry_id"]}).')
app/backend/review.py:72:# plain words for "AI wording removed (failed a check: ...)" in the internal notes
app/backend/review.py:464:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
app/backend/review.py:484:    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
app/backend/store.py:135:            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:15.570Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 25,36p app/backend/export.py; grep -n \"AI_LINE\" app/backend/export.py | head; grep -n \"AI wording\" app/backend/review.py | head; grep -rn \"AI wording\" app/frontend/guided/*.js app/frontend/*.js 2>/dev/null | head -5"
}
````

### User / tool · 2026-11-02T21:51:15.679Z

**tool result**
````
SUMMARY_TITLE = "TREATMENT SUMMARY"
NOTES_TITLE = "INTERNAL REVIEW NOTES — DO NOT SEND"
SOURCE_PREFIX = "Source [Ex. __ / Bates __]: "
TOTAL_PREFIX = "Billed charges accepted from these records: "  # D-019: nothing may follow the amount, ever
AI_LINE = ("This chronology was drafted with AI assistance; every item in the treatment section was accepted "
           "by the paralegal. Items not reviewed: {n}.")
FLAGGED_HEADING = ("FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or "
                   "dismiss the entry to remove it; hedge sentences cannot be removed)")

IN = ("accepted", "edited")
STYLES = ("standard", "oneline")      # T-121: "standard" (default) is the golden layout; "oneline" gives one line per entry
# T-121: the translation note is a bracketed, removable phrase at the end of the entry, keyed by the item's translation label (never a line prefix).
29:AI_LINE = ("This chronology was drafted with AI assistance; every item in the treatment section was accepted "
733:        AI_LINE.format(n=len(pending)), "",
72:# plain words for "AI wording removed (failed a check: ...)" in the internal notes
464:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
484:    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:18.361Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"AI\" app/backend/review.py | grep -v \"^\\s*[0-9]*:\\s*#\" | head -40"
}
````

### User / tool · 2026-11-02T21:51:18.441Z

**tool result**
````
8:JUDGE_UNAVAILABLE).
151:    """A 422 ReviewError (code CODE_CHECK_FAILED) if the entry's current wording fails a code check, else None. Accept never goes past it (D-051)."""
155:    return ReviewError(422, "CODE_CHECK_FAILED", code_check_detail(item_id, fails), code_check_message(fails))
165:    """T-139 (D-019, R-CH-7): a 422 CODE_CHECK_FAILED naming CHARGE_TEXT_IN_ENTRY when the entry's CURRENT summary or quote states a dollar amount, else None.
176:    return ReviewError(422, "CODE_CHECK_FAILED", detail, charge_text.message(found, state_fn() if state_fn else None))
241:    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
401:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}) + " Until you do, the item stays marked for review.", "item_id": item_id})
464:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
484:    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
555:    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
556:        reasons.append("AI_TRANSLATION")
661:    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
740:            msg = ("The record was split off. Code removed every part of the AI's summary that its quote does not support, so it is in the could-not-verify tray; "
742:                   else "The record was split off, but the AI could not draft its entry; it is in the could-not-verify tray. Enter it by hand.")
751:        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:23.455Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"wording\\|drafted\\|the AI\\|The AI\" app/backend/review.py | grep -v \"^[0-9]*:\\s*#\" | cut -c1-260; sed -n 395,405p app/backend/review.py | cut -c1-300"
}
````

### User / tool · 2026-11-02T21:51:23.553Z

**tool result**
````
151:    """A 422 ReviewError (code CODE_CHECK_FAILED) if the entry's current wording fails a code check, else None. Accept never goes past it (D-051)."""
239:    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
241:    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
453:    edited.pop("code_trim", None)           # T-139 r3: the trace shows the removal only while the wording it made is still the wording (a later hand edit or quote change clears it)
464:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
467:    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
484:    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
661:    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
740:            msg = ("The record was split off. Code removed every part of the AI's summary that its quote does not support, so it is in the could-not-verify tray; "
742:                   else "The record was split off, but the AI could not draft its entry; it is in the could-not-verify tray. Enter it by hand.")
751:        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
        ladder_verdict = judges.to_ladder("j1", verdict)
    warnings = []
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
    elif ladder_verdict == "unavailable":
        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}) + " Until you do, the item stays marked for review.", "item_id": item_id})
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:35.084Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 1,80p ../../T-177-staff-engineer-r2/probe_r2_branch.py"
}
````

### User / tool · 2026-11-02T21:51:35.165Z

**tool result**
````
"""T-177 r2 branch probe (staff-engineer-reviewer). Question: does a PREPARED (curated) item whose generator answer FAILS a code check
still get the prepared label in its trace, or the 'AI drafted' label?
Method: copy the archive's curated fixture set to a scratch dir named 'curated' (so answer_source() is 'prepared'), break e1's
generator answer by removing its `summary` key (schema fails), run the sample case through the normal pipeline, read e1's trace.
Usage: python -I probe_r2_branch.py <archive_dir> <scratch_dir>"""
import json
import os
import shutil
import sys
import time

ARCH, SCRATCH = sys.argv[1], sys.argv[2]
sys.path.insert(0, ARCH)
os.chdir(ARCH)

E1_KEY = "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7"   # e1's generator answer (curated/, prepared by hand)

mut_root = os.path.join(SCRATCH, "mut_branch")
mut_dir = os.path.join(mut_root, "curated")
if os.path.isdir(mut_root):
    shutil.rmtree(mut_root)
os.makedirs(mut_root)
os.makedirs(mut_dir)
src = os.path.join(ARCH, "tests", "fixtures", "llm")
for f in os.listdir(src):                       # the recorded set is the fallback for keys the curated set lacks (fixture.call)
    if f.endswith(".json"):
        shutil.copy(os.path.join(src, f), mut_dir)
for f in os.listdir(os.path.join(src, "curated")):   # the curated set wins for its own keys
    if f.endswith(".json"):
        shutil.copy(os.path.join(src, "curated", f), mut_dir)
p = os.path.join(mut_dir, E1_KEY + ".json")
MODE = sys.argv[3] if len(sys.argv) > 3 else "unsupported"
if MODE == "missing":
    os.remove(p)                                 # one curated answer file is absent: fixture.call raises FixtureMiss (no recorded fallback for this key)
else:
    d = json.load(open(p))
    d["output"]["summary"] = "Patient reported paralysis of the left leg and loss of bladder control."     # no clause is in the quote: code removes all of it (D-054)
    json.dump(d, open(p, "w"), indent=1, sort_keys=True)
print("mutation mode:", MODE)

os.environ["LLM_BACKEND"] = "fixture"
os.environ["ZLAYT_MODE"] = "local"
os.environ["LLM_FIXTURE_DIR"] = mut_dir
for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "FIXTURE_SET"):
    os.environ.pop(k, None)

from fastapi.testclient import TestClient  # noqa: E402
from app.backend.api import create_app  # noqa: E402

c = TestClient(create_app(os.path.join(SCRATCH, "mut_branch.sqlite"), static_dir=os.path.join(ARCH, "app", "frontend")), client=("127.0.0.1", 50000))
tok = c.post("/api/cases", json={"sample": True, "title": "branch probe"}).json()["token"]
assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
for _ in range(480):
    s = c.get(f"/api/cases/{tok}/status").json()
    if s["status"] in ("ready", "failed"):
        break
    time.sleep(0.25)
print("run status:", s["status"])
print("health answers:", c.get("/api/health").json().get("answers"))
item = c.get(f"/api/cases/{tok}/items/e1").json()["item"]
print("e1 state:", item.get("state"), "reasons:", item.get("state_reasons") or item.get("reasons"), "prepared:", item.get("prepared"))
print("e1 ladder.generator.model:", ((item.get("ladder") or {}).get("generator") or {}).get("model"))
tr = c.get(f"/api/cases/{tok}/items/e1/trace").json()
gen = next(x for x in tr["steps"] if x["id"] == "extracted")
print("e1 extracted step:")
print(json.dumps({k: gen.get(k) for k in ("label", "status", "why", "reason_code", "rule")}, indent=1, ensure_ascii=False))
print("e1 extracted evidence.model:", json.dumps((gen.get("evidence") or {}).get("model"), ensure_ascii=False))
case_tr = c.get(f"/api/cases/{tok}/trace").json()
ex = next(x for x in case_tr["steps"] if x["id"] == "extract")
print("case-level extract step label:", repr(ex.get("label")), "status:", ex.get("status"))
print("case-level extract why:", repr(ex.get("why")))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:36.288Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"the AI\\|The AI\\|AI's\\|AI draft\\|AI-made\\|AI found\\|AI wrote\\|AI picked\" app/backend/trace.py app/backend/why.py app/backend/present.py app/backend/pipeline.py app/backend/flags.py app/backend/confidence.py app/backend/generator.py app/backend/store.py app/backend/api.py | grep -v \"^\\S*:[0-9]*:\\s*#\" | cut -c1-240 | head -120"
}
````

### User / tool · 2026-11-02T21:51:36.377Z

**tool result**
````
app/backend/present.py:277:            for k in ("why", "explanation"):      # D-065: the fixed sentences say "prepared answer", never that an AI drafted or found it
app/backend/present.py:324:    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
app/backend/pipeline.py:248:    """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
app/backend/pipeline.py:259:    (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
app/backend/pipeline.py:260:    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
app/backend/pipeline.py:324:    reviewer) is never a stale row (T-165 r2, `_keep_hand_entry`): a re-run must not sweep the paralegal's work; when the AI now also has an entry for the record it gets a rerun_note."""
app/backend/pipeline.py:368:    live = {}      # record id -> id of the AI entry that came out for it on this run
app/backend/pipeline.py:376:                _keep_hand_entry(conn, old, live, cid, now)      # T-165 r2: the paralegal's own entry is never swept, whether or not the AI now has one
app/backend/pipeline.py:386:    """T-165 r2: a pending hand-entered entry survives every re-run untouched. When the AI now also has an entry for the record, `ladder.rerun_note` (kind `ai_entry`) says so and
app/backend/pipeline.py:393:        msg = f"The AI step now has an entry for record {no} ({ai}) as well. Your entry was kept; keep whichever is right and dismiss the other."
app/backend/pipeline.py:462:        parts.append(f"The AI step failed for {_items(len(failed))} ({' and '.join(sorted({c for _, c, _ in failed}))}) on this run. Their earlier results and every "
app/backend/pipeline.py:468:        parts.append(f"The AI step also failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) with no earlier result to keep." if kept else
app/backend/pipeline.py:469:                     f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
app/backend/pipeline.py:471:        parts.append(f"The AI step ({' and '.join(sorted(down))}) failed on this run, so nothing from it could be used.")
app/backend/pipeline.py:505:    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
app/backend/why.py:5:    "SCHEMA_INVALID": "The AI output was malformed after several attempts, so this item was rejected.",
app/backend/why.py:25:    "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
app/backend/why.py:26:    "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
app/backend/why.py:27:    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
app/backend/why.py:29:    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
app/backend/why.py:30:    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
app/backend/why.py:33:    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
app/backend/why.py:34:    "SUMMARY_NOT_IN_QUOTE": "Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the reco
app/backend/why.py:35:    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no AI-made entry. Read the record yourself or write the entry by hand.",
app/backend/why.py:43:MODEL_CONFLICT = ("The AI suggested a conflict between two passages, but the software only raises a conflict for pairs its own fixed rules pick, "
app/backend/why.py:50:JUDGE_DEMO = ("The AI second check is not available in this demo, so this item has not been double-checked. "
app/backend/why.py:89:    ("The AI output was malformed after several attempts, so this item was rejected.", "The prepared answer was malformed, so this item was rejected."),
app/backend/why.py:91:    ("The phrase list found this flag but the AI did not; check that it applies.", "The phrase list found this flag but the prepared answers did not; check that it applies."),
app/backend/why.py:92:    ("The AI found this flag but the phrase list did not; check that it applies.", "The prepared answers include this flag but the phrase list did not; check that it applies."),
app/backend/why.py:93:    ("The AI proposed this as a flag, but a fixed rule filtered it out", "A prepared answer proposed this as a flag, but a fixed rule filtered it out"),
app/backend/why.py:94:    ("It is listed so nothing the AI proposed is hidden;", "It is listed so nothing a prepared answer proposed is hidden;"),
app/backend/why.py:95:    ("The AI step failed on all three attempts, so this record has no AI-made entry.", "The prepared answer for this record could not be used, so it has no entry."),
app/backend/why.py:96:    ("Every part of the AI's summary added something its quote does not contain", "Every part of the prepared summary added something its quote does not contain"),
app/backend/why.py:97:    ("so it has no AI-made entry.", "so it has no entry."),
app/backend/why.py:100:    ("This summary was drafted by the AI and a code check on it fails", "This summary is a prepared answer and a code check on it fails"),
app/backend/why.py:101:    ("but the summary is still the AI's wording", "but the summary is still the prepared wording"),
app/backend/why.py:102:    ("Nothing the AI wrote goes into the letter without that check", "Nothing prepared goes into the letter without that check"),
app/backend/why.py:103:    ("The AI suggested a conflict between two passages", "A prepared answer suggested a conflict between two passages"),
app/backend/why.py:104:    ("The AI proposed this quote under more than one category", "A prepared answer proposed this quote under more than one category"),
app/backend/why.py:105:    ("The AI proposed this flag as a category and a quote; it wrote no explanation.", "The prepared answer proposed this flag as a category and a quote; it wrote no explanation."),
app/backend/why.py:106:    ("The AI did not find it.", "The prepared answers did not include it."),
app/backend/why.py:107:    ("The AI found it.", "The prepared answers included it."),
app/backend/why.py:108:    ("The AI, not the formatting, decided where this record begins", "A prepared answer, not the formatting, decided where this record begins"),
app/backend/why.py:109:    ("the AI proposed the record boundaries", "a prepared answer proposed the record boundaries"),
app/backend/why.py:110:    ("Both the phrase list and the AI found this flag.", "Both the phrase list and the prepared answers include this flag."),
app/backend/why.py:111:    ("The AI step", "The prepared-answer step"),
app/backend/trace.py:44:    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept
app/backend/trace.py:46:    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
app/backend/trace.py:47:    "RUN_IN_PROGRESS": "The AI run is still going.",
app/backend/trace.py:50:    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
app/backend/trace.py:51:    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it. It cl
app/backend/trace.py:52:    "CODE_CHECK_FAILED_AI": "This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
app/backend/trace.py:67:    "RERUN": "Run the AI steps again.",
app/backend/trace.py:70:    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
app/backend/trace.py:174:PREPARED_LABEL = "Prepared answer, standing in for the AI draft"
app/backend/trace.py:175:PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"
app/backend/trace.py:176:CASE_PREPARED_LABEL = "Prepared summaries and quotes for each record, standing in for the AI draft"
app/backend/trace.py:197:    """D-065: the item's first answer is a hand-checked fixture, or it has none and the set in use is the curated one. Then no sentence about it may say an AI drafted or found it."""
app/backend/trace.py:305:                        "SCHEMA_INVALID": "Not run: the AI answer was malformed.",
app/backend/trace.py:307:                        "LLM_FAILED_AFTER_RETRIES": "Not run: the AI gave no usable answer for this record.",
app/backend/trace.py:308:                        "FIXTURE_MISS": "Not run: the AI gave no usable answer for this record.",
app/backend/trace.py:309:                        "UNSUPPORTED_LANGUAGE": "Not run: the record is not in a language the AI reads."}.get(code, "Not run because an earlier step rejected this item.")
app/backend/trace.py:324:    if gated:      # whose words: only the paralegal's own summary is "your wording"; an AI draft is "this summary"
app/backend/trace.py:337:        code, label = "waiting_for_run", "Waiting for the AI run"
app/backend/trace.py:352:    if prepared_item(cx, row, kind):      # D-065: every sentence of a prepared item's trace says prepared, never that an AI drafted or found it
app/backend/trace.py:380:    """T-139: code steps for what generation did to the AI's text because it states an amount. Internal: the trace is not the letter, so the removed text is quoted as written.
app/backend/trace.py:381:    `excerpt_narrowed` = the AI's quote lost its end sentence(s); `charge_clause_removed` = the AI summary lost its trailing amount clause(s). Both are PASS: nothing
app/backend/trace.py:387:                        f"Code removed {_q(nar['dropped'])} from the quote the AI picked. Why: it states a dollar amount. {_NO_LETTER} What is left is whole, "
app/backend/trace.py:393:                        f"Code removed {_q(nar['summary_removed'])} from the end of the AI's summary. Why: it states a dollar amount, and the shortened quote no longer carries it. "
app/backend/trace.py:402:    """T-139: when she picked a quote without the amount and code removed the amount clause from the AI summary in the same edit (review._edit; `edited.code_trim`)."""
app/backend/trace.py:407:                 f"Code removed {_q(ct['removed'])} from the end of the AI's summary when you changed the quote. Why: the new quote does not state the amount, and "
app/backend/trace.py:422:    placeholder = lad.get("failure")                      # could-not-verify tray placeholder: the AI made no usable summary, so there is no quote to check (T-112 r2)
app/backend/trace.py:429:        st.append(step("extracted", "You wrote this entry", "human", PASS, "You wrote this summary and picked the quote; no AI drafted it.", rule="row 4",
app/backend/trace.py:436:        prep = ev["model"]["prepared"] or (not (call and call.get("recorded_from")) and cx.answers_prepared)      # D-065 (T-177 r3): a failed or missing prepared answer is still a prepared answer, never "AI drafted
app/backend/trace.py:439:        xlabel = PREPARED_LABEL if prep else "AI drafted a summary and picked a quote"
app/backend/trace.py:459:                st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
app/backend/trace.py:460:                               "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
app/backend/trace.py:465:            st.extend(_narrow_steps(lad, row))                # T-139: code shortened the AI's quote / removed an amount clause; shown, never silent, never in the letter
app/backend/trace.py:466:    st.extend(_edit_trim_steps(row))                          # T-139: the quote-picker edit removed the amount clause from the AI summary
app/backend/trace.py:524:    if _code_check_gated(row):        # D-045(b), D-051: a failing code check blocks the export (AI-made or human wording; only the judge is exempt for human wording) and says what to do
app/backend/trace.py:563:    """Export blockers (D-045(b), D-051): accepted or edited entries, AI-made or human, whose current summary or quote fails a code check.
app/backend/trace.py:724:        pass                                  # a conflict is the AI's pair proposal (row 11): no phrase list, so no agreement step
app/backend/trace.py:740:            st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
app/backend/trace.py:744:        st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
app/backend/trace.py:748:        st.append(step("agreement", _AGREE[1 if prep else 0], "code", PASS, "Both the phrase list and the AI found this flag.", rule="row 12"))
app/backend/trace.py:813:        st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
app/backend/trace.py:892:                          "The AI proposed this quote under more than one category (" + ", ".join(m.replace("_", " ") for m in merged) + " as well as " + row["category"].replace("_", " ")
app/backend/trace.py:925:        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
app/backend/trace.py:942:    """T-134 r3 (T-136 F-2): an open edit that left the AI's summary in place (a re-picked quote) and whose second check has no answer. Accepting it alone cannot clear D-044's
app/backend/trace.py:955:    """The one sentence for n accepted AI-made items whose second check has no answer: the 422 `judge_not_run` message and the export-gate headline (T-134 r4)."""
app/backend/trace.py:963:    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
app/backend/trace.py:964:    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
app/backend/trace.py:972:            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
app/backend/trace.py:984:    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one.
app/backend/trace.py:1046:                                      "judge_says": (lambda t: why.to_prepared(t) if prepared_item(cx, row, "flag") else t)("The AI did not find it." if c == "LEXICON_ONLY" else "The AI found it."),
app/backend/trace.py:1120:    prep = bool(cx.models.get("generator_prepared"))      # T-177 r2 / D-065: the case's answers are hand-checked fixtures, so the step must not say an AI drafted them
app/backend/trace.py:1121:    xlabel = CASE_PREPARED_LABEL if prep else "AI drafts a summary and a quote for each record"
app/backend/trace.py:1124:        st.append(step("extract", xlabel, "llm", PENDING, "The prepared answers have not been loaded yet." if prep else "The AI run has not started.", rule="row 4", counts=ecounts, next_action=na("RERUN"), **xev))
app/backend/trace.py:1128:        st.append(step("extract", xlabel, "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no {'prepared' if prep else 'AI-made'} entry. "
app/backend/trace.py:1132:        st.append(step("extract", xlabel, "llm", PASS, (f"The prepared answers (hand-checked by the team for the demo) cover all {len(firsts)} records." if prep else f"The AI drafted an entry for all {len(firsts)} 
app/backend/trace.py:1151:    jlabel = "Second AI check on every prepared item" if prep else "Second AI check on every AI-made item"      # T-177 r2: the items are the team's prepared answers
app/backend/trace.py:1175:        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PENDING, "Gaps and date conflicts are ready (code). The AI and phrase-list pass has not run.", rule="row 9", counts=fc,
app/backend/trace.py:1178:        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and the AI.", rule="row
app/backend/trace.py:1234:    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
app/backend/trace.py:1243:    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."
app/backend/trace.py:1247:    """T-134 r4 (D-058): for open edits that keep the AI's summary with no second-check answer. Conditional, because before she accepts nothing is blocked (the gate passes and the
app/backend/trace.py:1251:    return (f"{who} the AI's summary and the second check has no answer on the new quote, so accepting alone will not put {them} in the letter. "
app/backend/trace.py:1272:    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
app/backend/trace.py:1273:    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
app/backend/store.py:135:            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
app/backend/generator.py:220:                        "message": (why.to_prepared if AU.answers_prepared() else str)(f"The AI step could not write an entry for record {n}; you entered it by hand.")})
app/backend/api.py:447:                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
app/backend/api.py:464:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
app/backend/api.py:475:                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
app/backend/api.py:516:        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:51:56.211Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 795,816p app/backend/trace.py | cut -c1-260; ls tests/fixtures/llm/curated | wc -l; ls tests/fixtures/llm/curated/98b1735e* ; python3 -c \"\nimport json;d=json.load(open('tests/fixtures/llm/curated/98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json'));print(d)\""
}
````

### User / tool · 2026-11-02T21:51:56.324Z

**tool result**
````
def _narrative_trace(cx, item_id):
    nar = narrative.get(cx.conn, cx.case_id) or {}
    sent = next((s for s in nar.get("sentences", []) if s["id"] == item_id), None)
    rem = next((s for s in nar.get("removed", []) if s["id"] == item_id), None)
    s = sent or rem
    if s is None:
        raise UnknownItem(item_id)
    reason = (rem or {}).get("reason")
    rcodes = list((rem or {}).get("reasons") or []) if reason not in ("NOT_AN_ACCEPTED_ENTRY",) and not str(reason).startswith("JUDGE_") else []
    st = []
    gen = nar.get("generator") or {}
    call = cx.call(gen.get("call_id"))
    ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
    ev["values"] = {"entry_id": s["entry_id"], "text": s["text"]}
    if ev["model"]["prepared"]:
        st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
    else:
        st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
    cited_ok = reason != "NOT_AN_ACCEPTED_ENTRY"
    st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
                   reason=None if cited_ok else "NOT_AN_ACCEPTED_ENTRY", rule="D-031", evidence={"values": {"entry_id": s["entry_id"]}},
      19
tests/fixtures/llm/curated/98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
{'CURATED': 'CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).', 'output': {'excerpt': '41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.', 'summary': 'Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.'}, 'recorded_from': {'backend': 'curated', 'model': 'hand-checked (qa)', 'recorded_at': '2026-11-02T02:46:58Z'}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:02.033Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && python3 -c \"\nimport json,glob\nfor f in sorted(glob.glob('tests/fixtures/llm/curated/*.json')):\n    d=json.load(open(f));o=d['output']\n    if isinstance(o,dict) and 'summary' in o: print(f.split('/')[-1][:12], '|', o['excerpt'][:90], '|', o['summary'][:80])\n\"; grep -n \"3,915\" evals/golden/sample.txt"
}
````

### User / tool · 2026-11-02T21:52:02.134Z

**tool result**
````
0f653bdfe99e | New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. | New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordere
228350fb06e4 | Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. | Cervical range of motion reduced approx. 40%; plan of care 12 visits.
4770363f6bf6 | C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenera | C5-C6 disc protrusion with mild right foraminal narrowing; the record states fin
98b1735efe41 | 41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Aler | Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and
a3f0e26ea728 | Recommend cervical epidural steroid injection. Patient states symptoms began after the Jan | Cervical epidural steroid injection recommended; patient states symptoms began a
aacd477fd06e | Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. | Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/w
b74b563d21aa | Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclob | Diagnosed with cervical strain and concussion without loss of consciousness; CT 
bde3b432c62b | Pain 4/10, improving. | Pain 4/10, improving.
be8b230f82b3 | Discharged from PT after two missed appointments. Pain 3/10. | Discharged from physical therapy after two missed appointments; pain 3/10.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:06.470Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n -B2 -A8 \"cyclob\" evals/golden/sample.txt | head -30; python3 -c \"\nimport json;d=json.load(open('tests/fixtures/llm/curated/b74b563d21aa'+[f for f in __import__('os').listdir('tests/fixtures/llm/curated') if f.startswith('b74b563d21aa')][0][12:]));print(d['output'])\""
}
````

### User / tool · 2026-11-02T21:52:06.581Z

**tool result**
````
9-Date: 2026-01-09
10-Source: Central ER discharge summary
11:Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
12-
13-=== Record 3 ===
14-Date: 2026-01-16
15-Source: Dr. Alvarez, primary care
16-Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."
17-
18-=== Record 4 ===
19-Date: 2026-01-23
{'excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.', 'summary': 'Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.'}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:26.328Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_branch.py",
 "content": "\"\"\"T-177 r3 branch probe (staff-engineer-reviewer). Archive of 2e58e18 only.\nUsage: python -I probe_r3_branch.py <archive_dir> <scratch_dir> <mode>\nCopies the recorded fixture set, then the curated set over it, into <scratch>/mut_<mode>/curated (so fixture answer_source() is 'prepared'),\nmutates ONE curated generator answer, runs the sample through the normal pipeline (in-process TestClient, local mode so /audit has full text),\nthen prints every sentence the API gives for the affected item and scans ALL payloads of the run for AI-authorship wording.\nmodes: unsupported (e1 summary has no clause in its quote), missing (e1 answer file removed), schema (e1 summary key removed),\n       amount (ER entry quote and summary state $6,240), badshape (e1 output is a list), recordedmix (control: nothing mutated, recorded dir only).\"\"\"\nimport json\nimport os\nimport re\nimport shutil\nimport sys\nimport time\n\nARCH, SCRATCH, MODE = sys.argv[1], sys.argv[2], sys.argv[3]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\nsrc = os.path.join(ARCH, \"tests\", \"fixtures\", \"llm\")\nmut_root = os.path.join(SCRATCH, \"mut_\" + MODE)\nmut_dir = os.path.join(mut_root, \"curated\")\nif os.path.isdir(mut_root):\n    shutil.rmtree(mut_root)\nos.makedirs(mut_dir)\nfor f in os.listdir(src):\n    if f.endswith(\".json\"):\n        shutil.copy(os.path.join(src, f), mut_dir)\nfor f in os.listdir(os.path.join(src, \"curated\")):\n    if f.endswith(\".json\"):\n        shutil.copy(os.path.join(src, \"curated\", f), mut_dir)\nE1 = os.path.join(mut_dir, \"98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json\")\nER = next(os.path.join(mut_dir, f) for f in os.listdir(mut_dir) if f.startswith(\"b74b563d21aa\"))\ntarget = \"e1\"\nif MODE == \"missing\":\n    os.remove(E1)\nelif MODE == \"unsupported\":\n    d = json.load(open(E1)); d[\"output\"][\"summary\"] = \"Patient reported paralysis of the left leg and loss of bladder control.\"; json.dump(d, open(E1, \"w\"))\nelif MODE == \"schema\":\n    d = json.load(open(E1)); d[\"output\"].pop(\"summary\"); json.dump(d, open(E1, \"w\"))\nelif MODE == \"badshape\":\n    d = json.load(open(E1)); d[\"output\"] = [\"not\", \"an\", \"object\"]; json.dump(d, open(E1, \"w\"))\nelif MODE == \"amount\":\n    d = json.load(open(ER)); d[\"output\"][\"excerpt\"] += \" ER charges: $6,240.\"; d[\"output\"][\"summary\"] = d[\"output\"][\"summary\"].rstrip(\".\") + \"; ER charges $6,240.\"; json.dump(d, open(ER, \"w\"))\n    target = \"e2\"\nprint(\"mode:\", MODE, \"target:\", target)\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ[\"ZLAYT_MODE\"] = \"local\"\nos.environ[\"LLM_FIXTURE_DIR\"] = mut_dir\nfor k in (\"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"FIXTURE_SET\"):\n    os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nc = TestClient(create_app(os.path.join(SCRATCH, \"mut_%s.sqlite\" % MODE), static_dir=os.path.join(ARCH, \"app\", \"frontend\")), client=(\"127.0.0.1\", 50000))\nif os.path.exists(os.path.join(SCRATCH, \"mut_%s.sqlite\" % MODE)):\n    pass\ntok = c.post(\"/api/cases\", json={\"sample\": True, \"title\": \"branch r3\"}).json()[\"token\"]\nprint(\"run POST\", c.post(f\"/api/cases/{tok}/run\", json={}).status_code)\nfor _ in range(600):\n    s = c.get(f\"/api/cases/{tok}/status\").json()\n    if s[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.25)\nprint(\"run status:\", s[\"status\"], \"| status.error:\", json.dumps(s.get(\"error\"), ensure_ascii=False))\nh = c.get(\"/api/health\").json()\nprint(\"health answers:\", h.get(\"answers\"), \"| health models:\", h.get(\"models\"))\ncase = c.get(f\"/api/cases/{tok}\").json()\nprint(\"case.models:\", case.get(\"models\"))\nprint(\"case.warnings:\", json.dumps(case.get(\"warnings\"), ensure_ascii=False)[:1200])\nit = c.get(f\"/api/cases/{tok}/items/{target}\").json()[\"item\"]\nprint(f\"{target}: state={it.get('state')} prepared={it.get('prepared')} reasons={it.get('reasons')}\")\nprint(f\"{target}.why: {it.get('why')!r}\")\nprint(f\"{target}.explanation: {it.get('explanation')!r}\")\ntr = c.get(f\"/api/cases/{tok}/items/{target}/trace\").json()\nprint(f\"{target} trace verdict: {tr.get('verdict')} next_action: {json.dumps(tr.get('next_action'), ensure_ascii=False)}\")\nfor r in tr.get(\"state_reasons\") or []:\n    print(f\"  reason {r.get('code')}: {r.get('why')!r}\")\nfor st in tr[\"steps\"]:\n    ev = st.get(\"evidence\") or {}\n    print(f\"  step {st['id']:<28} {st['status']:<8} label={st['label']!r}\\n      why={st['why']!r}\\n      model={json.dumps(ev.get('model'), ensure_ascii=False)} prompt_version={ev.get('prompt_version')!r} next_action={json.dumps(st.get('next_action'), ensure_ascii=False)[:200]}\")\nca = next(a for a in c.get(f\"/api/cases/{tok}/audit\").json()[\"rows\"] if a.get(\"item_id\") == target and a.get(\"role\") == \"generator\") if False else None\naud = c.get(f\"/api/cases/{tok}/audit\").json()\nrows = [r for r in (aud.get(\"rows\") or aud.get(\"calls\") or []) if r.get(\"item_id\") == target]\nfor r in rows:\n    print(\"  audit row:\", json.dumps({k: r.get(k) for k in (\"role\", \"step\", \"model\", \"prompt_version\", \"prompt_sha256\", \"prepared\", \"parsed_ok\", \"error\")}, ensure_ascii=False))\n\nPAT = re.compile(r\"AI draft|AI found|AI proposed|AI wrote|AI-made|AI-written|AI suggested|AI read|AI translat|AI step|AI output|AI wording|AI's|AI picked|the AI |The AI |Drafted by|claude-sonnet|AI gave|AI answer\")\nD065 = \"standing in for the AI draft\"\nfound = []\ndef scan(label, obj):\n    t = json.dumps(obj, ensure_ascii=False).replace(D065, \"<D065>\")\n    for m in PAT.finditer(t):\n        found.append((label, m.group(0), t[max(0, m.start() - 90): m.end() + 70]))\nids = [x[\"id\"] for k in (\"entries\", \"amounts\", \"flags\") for x in case.get(k, [])]\nfor path in (f\"/api/cases/{tok}\", f\"/api/cases/{tok}/judges\", f\"/api/cases/{tok}/trace\", f\"/api/cases/{tok}/status\", f\"/api/cases/{tok}/audit\"):\n    scan(path.replace(tok, \"<tok>\"), c.get(path).json())\nfor iid in ids:\n    r = c.get(f\"/api/cases/{tok}/items/{iid}\")\n    if r.status_code == 200:\n        scan(\"item \" + iid, r.json())\n    r = c.get(f\"/api/cases/{tok}/items/{iid}/trace\")\n    if r.status_code == 200:\n        scan(\"trace \" + iid, r.json())\nfor iid in ids:\n    c.post(f\"/api/cases/{tok}/items/{iid}/review\", json={\"action\": \"accept\"})\nex = c.get(f\"/api/cases/{tok}/export\")\nprint(\"export status\", ex.status_code)\nif ex.status_code == 200:\n    scan(\"export\", ex.json())\nelse:\n    print(\"  export body:\", ex.text[:400])\nprint(\"authorship-pattern hits:\", len(found))\nseen = set()\nfor lab, pat, ctx in found:\n    key = (lab.split(\" \")[0] + (\" \" + lab.split(\" \")[1] if lab.startswith((\"item\", \"trace\")) else \"\"), pat)\n    if key in seen:\n        continue\n    seen.add(key)\n    print(f\"  HIT {lab} | {pat!r} | ...{ctx}...\")\n"
}
````

### User / tool · 2026-11-02T21:52:26.425Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_branch.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:29.817Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && for m in unsupported missing; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_branch.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/scratch $m > probe-r3-branch-$m.out 2>&1; echo \"== $m\"; cut -c1-700 probe-r3-branch-$m.out; done",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:52:32.980Z

**tool result**
````
== unsupported
mode: unsupported target: e1
run POST 202
run status: ready | status.error: null
health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.warnings: []
e1: state=rejected prepared=True reasons=['SUMMARY_NOT_IN_QUOTE']
e1.why: 'Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.'
e1.explanation: None
e1 trace verdict: {'code': 'rejected', 'label': 'Rejected; kept out of the letter', 'blocks_export': False} next_action: {"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"record_id": "r1"}}
  reason SUMMARY_NOT_IN_QUOTE: 'Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.'
  step extracted                    fail     label='Prepared answer, standing in for the AI draft'
      why="removed from the summary: not in the quote: 'Patient reported paralysis of the left leg' removed from the summary: not in the quote: 'loss of bladder control' Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand."
      model={"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true} prompt_version=None next_action={"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"record_id": "r1"}}
  step excerpt_verbatim             skipped  label='Quote is word for word in the record'
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step excerpt_whole_sentence       skipped  label='Quote is made of whole sentences'
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step excerpt_hedge                skipped  label='Quote keeps the hedge sentence that qualifies it'
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step summary_tokens               skipped  label='Numbers and dates in the summary are in the quote'
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step summary_qualifier            skipped  label="Summary keeps the quote's qualifiers"
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step highlight                    skipped  label='Quote can be highlighted in the record'
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step date_confirmed               pass     label='Date of service is confirmed'
      why="The date comes from the record's own header and is parsed or confirmed."
      model=null prompt_version=None next_action=null
  step injection_scan               pass     label='Record has no instruction-like text'
      why='The record has no instruction-like text.'
      model=null prompt_version=None next_action=null
  step judge_1                      skipped  label='Second AI check: is the summary supported by the quote?'
      why='Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.'
      model=null prompt_version=None next_action=null
  step human                        pending  label='Your decision'
      why='This item could not be verified, so it cannot be accepted.'
      model=null prompt_version=None next_action={"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"item_id": "e1"}, "options": ["dismiss"]}
  audit row: {"role": "generator", "step": "extract", "model": "hand-checked (qa)", "prompt_version": null, "prompt_sha256": null, "prepared": true, "parsed_ok": true, "error": null}
export status 200
authorship-pattern hits: 2
  HIT /api/cases/<tok>/trace | 'the AI ' | ...EWED", "count": 22, "why": "22 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "...
  HIT trace f_r7_1 | 'AI answer' | ...status": "skipped", "why": "Not run: only the phrase list found this flag, so there is no AI answer to double-check; it stays marked for review.", "reason_code": "LEXICO...
== missing
llm call failed call_id=cbfeeb54cfded step=extract attempt=1 prompt_hash=98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7
mode: missing target: e1
run POST 202
run status: failed | status.error: {"code": "run_partial", "message": "The prepared-answer step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1. Run it again to retry.", "records": [1], "extract_only": true}
health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.warnings: []
e1: state=rejected prepared=False reasons=['FIXTURE_MISS']
e1.why: 'The demo has no recorded AI answer for this step, so this item has not been checked.'
e1.explanation: None
e1 trace verdict: {'code': 'rejected', 'label': 'Rejected; kept out of the letter', 'blocks_export': False} next_action: {"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"record_id": "r1"}}
  reason FIXTURE_MISS: 'The demo has no prepared answer for this step, so this item has not been checked.'
  step extracted                    fail     label='Prepared answer, standing in for the AI draft'
      why='There is no prepared answer for this record in the demo, so no entry was made.'
      model=null prompt_version=None next_action={"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"record_id": "r1"}}
  step excerpt_verbatim             skipped  label='Quote is word for word in the record'
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step excerpt_whole_sentence       skipped  label='Quote is made of whole sentences'
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step excerpt_hedge                skipped  label='Quote keeps the hedge sentence that qualifies it'
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step summary_tokens               skipped  label='Numbers and dates in the summary are in the quote'
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step summary_qualifier            skipped  label="Summary keeps the quote's qualifiers"
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step highlight                    skipped  label='Quote can be highlighted in the record'
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step date_confirmed               pass     label='Date of service is confirmed'
      why="The date comes from the record's own header and is parsed or confirmed."
      model=null prompt_version=None next_action=null
  step injection_scan               pass     label='Record has no instruction-like text'
      why='The record has no instruction-like text.'
      model=null prompt_version=None next_action=null
  step judge_1                      skipped  label='Second AI check: is the summary supported by the quote?'
      why='Not run: the AI gave no usable answer for this record.'
      model=null prompt_version=None next_action=null
  step human                        pending  label='Your decision'
      why='This item could not be verified, so it cannot be accepted.'
      model=null prompt_version=None next_action={"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"item_id": "e1"}, "options": ["dismiss"]}
  audit row: {"role": "generator", "step": "extract", "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7", "prepared": false, "parsed_ok": false, "error": "FIXTURE_MISS 98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7"}
export status 422
  export body: {"error":{"code":"export_blocked","message":"The last run stopped before it finished; the items that finished are kept. The export is blocked.","detail":{"blockers":[{"item_id":null,"kind":"case","reason_code":"RUN_FAILED","why":"The last run stopped before it finished; the items that finished are kept.","next_action":{"code":"CONFIRM_RERUN","text":"Run the AI steps again; confirm that earlier dec
authorship-pattern hits: 5
  HIT /api/cases/<tok> | 'AI answer' | ..."r1"], "state": "rejected", "reasons": ["FIXTURE_MISS"], "why": "The demo has no recorded AI answer for this step, so this item has not been checked.", "attempt": {"summ...
  HIT /api/cases/<tok>/trace | 'the AI ' | ...ocks_export": true, "evidence": {}, "next_action": {"code": "CONFIRM_RERUN", "text": "Run the AI steps again; confirm that earlier decisions are kept."}, "counts": {"b...
  HIT trace f_r7_1 | 'AI answer' | ...status": "skipped", "why": "Not run: only the phrase list found this flag, so there is no AI answer to double-check; it stays marked for review.", "reason_code": "LEXICO...
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:52:53.176Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && for m in schema amount; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_branch.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/scratch $m > probe-r3-branch-$m.out 2>&1; echo \"== $m\"; grep -v \"^      model=null\\|^      why='Not run: code removed\" probe-r3-branch-$m.out | cut -c1-600; done",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:52:59.213Z

**tool result**
````
== schema
llm call failed call_id=c6c64f67414c4 step=extract attempt=1
llm call failed call_id=cae26ca246009 step=extract attempt=2 prompt_hash=81726a2f47db088d333ae3bea0ce9d3281ab3432314533b752ac5db1db3ab6a2
mode: schema target: e1
run POST 202
run status: failed | status.error: {"code": "run_partial", "message": "The prepared-answer step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1. Run it again to retry.", "records": [1], "extract_only": true}
health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.models: {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
case.warnings: []
e1: state=rejected prepared=False reasons=['FIXTURE_MISS']
e1.why: 'The demo has no recorded AI answer for this step, so this item has not been checked.'
e1.explanation: None
e1 trace verdict: {'code': 'rejected', 'label': 'Rejected; kept out of the letter', 'blocks_export': False} next_action: {"code": "DISMISS_OR_ENTER_BY_HAND", "text": "This item cannot be used. Dismiss it, or write the entry by hand from the record.", "target": {"record_id": "r1"}}
  reason FIXTURE_MISS: 'The demo has no prepared answer for this step, so this item has not been checked.'
  step extracted                    fail     label='Prepared answer, standing in for the AI draft'
      why='There is no prepared answer for this record in the demo, so no entry was made.'
  step excerpt_verbatim             skipped  label='Quote is word for word in the record'
      why='Not run: the AI gave no usable answer for this record.'
  step excerpt_whole_sentence       skipped  label='Quote is made of whole sentences'
      why='Not run: the AI gave no usable answer for this record.'
  step excerpt_hedge                skipped  label='Quote keeps the hedge sentence that qualifies it'
      why='Not run: the AI gave no usable answer for this record.'
  step summary_tokens               skipped  label='Numbers and dates in the summary are in the quote'
      why='Not run: the AI gave no usable answer for this record.'
  step summary_qualifier            skipped  label="Summary keeps the quote's qualifiers"
      why='Not run: the AI gave no usable answer for this record.'
  step highlight                    skipped  label='Quote can be highlighted in the record'
      why='Not run: the AI gave no usable answer for this record.'
  step date_confirmed               pass     label='Date of service is confirmed'
      why="The date comes from the record's own header and is parsed or confirmed."
  step injection_scan               pass     label='Record has no instruction-like text'
      why='The record has no instruction-like text.'
  step judge_1                      skipped  label='Second AI check: is the summary supported by the quote?'
      why='Not run: the AI gave no usable answer for this record.'
  step human                        pending  label='Your decision'
      why='This item could not be verified, so it cannot be accepted.'
  audit row: {"role": "generator", "step": "extract", "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7", "prepared": false, "parsed_ok": false, "error": "SCHEMA_INVALID"}
  audit row: {"role": "generator", "step": "extract", "model": "hand-checked (qa)", "prompt_version": "extract_v1", "prompt_sha256": "81726a2f47db088d333ae3bea0ce9d3281ab3432314533b752ac5db1db3ab6a2", "prepared": false, "parsed_ok": false, "error": "FIXTURE_MISS 81726a2f47db088d333ae3bea0ce9d3281ab3432314533b752ac5db1db3ab6a2"}
export status 422
  export body: {"error":{"code":"export_blocked","message":"The last run stopped before it finished; the items that finished are kept. The export is blocked.","detail":{"blockers":[{"item_id":null,"kind":"case","reason_code":"RUN_FAILED","why":"The last run stopped before it finished; the items that finished are kept.","next_action":{"code":"CONFIRM_RERUN","text":"Run the AI steps again; confirm that earlier dec
authorship-pattern hits: 12
  HIT /api/cases/<tok> | 'claude-sonnet' | ...3", "status": "failed", "demo_mode": true, "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": false}, "rec...
  HIT /api/cases/<tok> | 'AI answer' | ..."r1"], "state": "rejected", "reasons": ["FIXTURE_MISS"], "why": "The demo has no recorded AI answer for this step, so this item has not been checked.", "attempt": {"summ...
  HIT /api/cases/<tok>/judges | 'claude-sonnet' | ...{"token": "SOt4C41St02eIim4n-8uGQ", "mode": "full", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5", "generator_prepared": false}, "ind...
  HIT /api/cases/<tok>/trace | 'AI draft' | ...": 9, "confirmed": 0, "ambiguous": 0, "missing": 0}, "n": 3}, {"id": "extract", "label": "AI drafts a summary and a quote for each record", "kind": "llm", "status": "fa...
  HIT /api/cases/<tok>/trace | 'AI-made' | ...ry and a quote for each record", "kind": "llm", "status": "fail", "why": "1 record has no AI-made entry. The AI step failed on all three attempts, so this record has n...
  HIT /api/cases/<tok>/trace | 'The AI ' | ...for each record", "kind": "llm", "status": "fail", "why": "1 record has no AI-made entry. The AI step failed on all three attempts, so this record has no AI-made entry...
  HIT /api/cases/<tok>/trace | 'the AI ' | ...ocks_export": true, "evidence": {}, "next_action": {"code": "CONFIRM_RERUN", "text": "Run the AI steps again; confirm that earlier decisions are kept."}, "counts": {"b...
  HIT trace f_r7_1 | 'AI answer' | ...status": "skipped", "why": "Not run: only the phrase list found this flag, so there is no AI answer to double-check; it stays marked for review.", "reason_code": "LEXICO...
== amount
mode: amount target: e2
run POST 202
run status: ready | status.error: null
health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.warnings: []
e2: state=verified prepared=True reasons=[]
e2.why: 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.'
e2.explanation: None
e2 trace verdict: {'code': 'ready_for_decision', 'label': 'Ready for your decision', 'blocks_export': True} next_action: {"code": "DECIDE", "text": "Accept, edit or dismiss this item.", "target": {"item_id": "e2"}, "options": ["accept", "edit", "dismiss"]}
  step extracted                    pass     label='Prepared answer, standing in for the AI draft'
      why='Prepared answer (hand-checked by the team for the demo), standing in for the AI draft'
      model={"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true} prompt_version=None next_action=null
  step excerpt_narrowed             pass     label='Code removed quote sentences that state an amount'
      why="Code removed ‘ER charges: $6,240.’ from the quote the AI picked. Why: it states a dollar amount. Amounts go only in the Billed charges section and the internal notes, never in the letter's treatment text (D-019, R-CH-7). What is left is whole, word-for-word sentences of the record, every code check ran again on it, and the second AI check saw the shortened quote."
  step charge_clause_removed        pass     label='Code removed a summary clause that states an amount'
      why="Code removed ‘ER charges $6,240’ from the end of the AI's summary. Why: it states a dollar amount, and the shortened quote no longer carries it. Amounts go only in the Billed charges section and the internal notes, never in the letter's treatment text (D-019, R-CH-7)."
  step excerpt_verbatim             pass     label='Quote is word for word in the record'
      why='The quote was found in the record, character for character.'
  step excerpt_whole_sentence       pass     label='Quote is made of whole sentences'
      why='The quote starts and ends on whole sentences.'
  step excerpt_hedge                pass     label='Quote keeps the hedge sentence that qualifies it'
      why='No hedge sentence that qualifies the quote is left out.'
  step summary_tokens               pass     label='Numbers and dates in the summary are in the quote'
      why='Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.'
  step summary_qualifier            pass     label="Summary keeps the quote's qualifiers"
      why='Every hedge, attribution, negation, side and approximation in the quote is in the summary.'
  step highlight                    pass     label='Quote can be highlighted in the record'
      why="The quote's position in the record was found, so it can be highlighted."
  step date_confirmed               pass     label='Date of service is confirmed'
      why="The date comes from the record's own header and is parsed or confirmed."
  step injection_scan               pass     label='Record has no instruction-like text'
      why='The record has no instruction-like text.'
  step judge_1                      pass     label='Second AI check: is the summary supported by the quote?'
      why='The second check found every statement in the summary in the quote.'
      model={"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true, "prepared": false} prompt_version='judge_faithfulness_v1' next_action=null
  step human                        pending  label='Your decision'
      why='You have not accepted, edited or dismissed this item yet, so it stays out of the letter.'
  audit row: {"role": "generator", "step": "extract", "model": "hand-checked (qa)", "prompt_version": null, "prompt_sha256": null, "prepared": true, "parsed_ok": true, "error": null}
  audit row: {"role": "judge", "step": "j1", "model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "prompt_sha256": "6faaefbcd81dd8f8b0c9bf123a19a4e168e77bfef3ae9d74bc90ef232fc6e353", "prepared": false, "parsed_ok": true, "error": null}
export status 200
authorship-pattern hits: 4
  HIT /api/cases/<tok>/trace | 'the AI ' | ...EWED", "count": 23, "why": "23 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "...
  HIT trace e2 | 'the AI ' | ...ind": "code", "status": "pass", "why": "Code removed ‘ER charges: $6,240.’ from the quote the AI picked. Why: it states a dollar amount. Amounts go only in the Billed ...
  HIT trace e2 | "AI's" | ...": "code", "status": "pass", "why": "Code removed ‘ER charges $6,240’ from the end of the AI's summary. Why: it states a dollar amount, and the shortened quote no l...
  HIT trace f_r7_1 | 'AI answer' | ...status": "skipped", "why": "Not run: only the phrase list found this flag, so there is no AI answer to double-check; it stays marked for review.", "reason_code": "LEXICO...
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:53:29.330Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && sed -n 1,80p T-177-staff-engineer-r2/render_flags_r2.py; ls T-177-staff-engineer-r3/archive/app/frontend/guided | head -30"
}
````

### User / tool · 2026-11-02T21:53:29.486Z

**tool result**
````
"""T-177 r2 flag-render probe (staff-engineer-reviewer). Curated set on its OWN server (started and stopped here; listener verified).
Opens the Why panel (item stepper) of two curated flags by calling ZL.stepper.openTrace(id), the function the btn-trace button calls
(the button sits inside the card's More menu), then reads the rendered step labels and kinds and scans the whole document.
Usage: python -I render_flags_r2.py <archive_dir> <evidence_dir> <scratch_dir>"""
import json
import os
import re
import sys
import time

ARCH, EVID, SCRATCH = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, ARCH)
sys.path.insert(0, EVID)

import render_r2 as R  # noqa: E402  (helpers only; its main() does not run on import)
from playwright.sync_api import sync_playwright  # noqa: E402

FLAGS = ["f_r3_1", "f_r6_1"]
BAD = ["AI found it", "AI draft", "claude-sonnet", "Drafted by", "AI check", "The AI proposed", "drafted by AI"]


def main():
    out = []
    base, port, proc, pids = R.start("curated", "flags")
    try:
        tok, st = R.make_case(base)
        out.append(f"[flags] case run status={st} port={port}")
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
            pg.goto(f"{base}/#/case/{tok}")
            pg.get_by_test_id("timeline").wait_for(timeout=20000)
            for fid in FLAGS:
                pg.wait_for_timeout(300)
                pg.evaluate("id => window.ZL.stepper.openTrace(id)", fid)
                st_el = pg.get_by_test_id("item-stepper")
                st_el.wait_for(timeout=15000)
                steps = st_el.get_by_test_id("step")
                rows = []
                for i in range(steps.count()):
                    s = steps.nth(i)
                    kind = s.get_by_test_id("step-kind").inner_text() if s.get_by_test_id("step-kind").count() else ""
                    rows.append((s.get_attribute("data-step-id"), kind, s.inner_text()[:160].replace("\n", " / ")))
                out.append(f"[flags] {fid}: stepper text (first 600 chars): {st_el.inner_text()[:600]!r}")
                for sid, kind, txt in rows:
                    out.append(f"[flags] {fid}: step {sid} kind={kind!r} text={txt!r}")
                text = R.scan(pg)
                hits = [(w, text[max(0, m.start() - 50): m.end() + 40]) for w in BAD for m in re.finditer(re.escape(w), text)]
                out.append(f"[flags] {fid}: whole-document scan hits for {BAD}: {len(hits)}")
                for w, ctx in hits[:6]:
                    out.append(f"   hit {w!r}: ...{ctx}...")
                st_el.screenshot(path=os.path.join(EVID, f"render-curated-flag-{fid}-why.png"))
                pg.keyboard.press("Escape")
                pg.wait_for_timeout(200)
            b.close()
    finally:
        if proc.pid in R.listeners(port):
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except Exception:
                proc.kill()
                proc.wait(timeout=10)
        out.append(f"[flags] stopped popen_pid={proc.pid}; listeners on port {port} now: {R.listeners(port)}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
app.js
core.js
home.css
home.js
index.html
review.css
review.js
step1.css
step1.js
step2.css
step2.js
step3.css
step3.js
step4.css
step4.js
styles.css
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:53:43.470Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/render_flags_r3.py",
 "content": "\"\"\"T-177 r3 flag Why-panel render probe (staff-engineer-reviewer). Own local-mode curated server (archive of 2e58e18) at <base>.\nCreates the sample case over the API, opens /classic/#/case/<tok> (local mode, so /classic is served), opens the Why panel of EVERY flag\nand entry via ZL.stepper.openTrace (the call the btn-trace button makes), reads step labels, kinds and the whole-document text.\nUsage: python -I render_flags_r3.py <base_url> <evidence_dir>\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\nimport urllib.request\n\nBASE, EVID = sys.argv[1].rstrip(\"/\"), sys.argv[2]\nfrom playwright.sync_api import sync_playwright  # noqa: E402\n\nBAD = re.compile(r\"AI found it|AI draft(?!\\b)|AI drafted|claude-sonnet|Drafted by|The AI proposed|AI proposed|AI wrote|AI-made|AI's|recorded AI\")\nKIND_BAD = re.compile(r\"AI draft\", re.I)\n\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body).encode(), method=method, headers={\"Content-Type\": \"application/json\"})\n    with urllib.request.urlopen(req, timeout=60) as r:\n        return json.loads(r.read().decode())\n\n\ndef main():\n    tok = api(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"render r3\"})[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(600):\n        if api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    case = api(\"GET\", f\"/api/cases/{tok}\")\n    flags = [f[\"id\"] for f in case[\"flags\"]]\n    entries = [e[\"id\"] for e in case[\"entries\"]]\n    out = [f\"case {tok[:6]}... flags={flags} entries={len(entries)}\"]\n    total_hits = 0\n    with sync_playwright() as pw:\n        b = pw.chromium.launch()\n        pg = b.new_context(viewport={\"width\": 1280, \"height\": 900}).new_page()\n        errs = []\n        pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n        pg.goto(f\"{BASE}/classic/#/case/{tok}\")\n        pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n        out.append(\"classic page title: \" + pg.title())\n        for iid in flags + entries:\n            pg.wait_for_timeout(250)\n            pg.evaluate(\"id => window.ZL.stepper.openTrace(id)\", iid)\n            el = pg.get_by_test_id(\"item-stepper\")\n            el.wait_for(timeout=15000)\n            steps = el.get_by_test_id(\"step\")\n            rows = []\n            for i in range(steps.count()):\n                s = steps.nth(i)\n                kind = s.get_by_test_id(\"step-kind\").inner_text() if s.get_by_test_id(\"step-kind\").count() else \"\"\n                rows.append((s.get_attribute(\"data-step-id\"), kind, s.inner_text().replace(\"\\n\", \" / \")))\n            panel = el.inner_text().replace(\"D-065\", \"\").replace(\"standing in for the AI draft\", \"\")\n            hits = BAD.findall(panel) + [k for _, k, _ in rows if KIND_BAD.search(k)]\n            total_hits += len(hits)\n            key = [(sid, k, t[:110]) for sid, k, t in rows if sid in (\"extracted\", \"proposed_by_ai\", \"agreement\")]\n            out.append(f\"{iid}: steps={len(rows)} bad-hits={hits} key-steps={key}\")\n            if iid in (\"f_r3_1\", \"f_r7_1\", \"e1\"):\n                el.screenshot(path=os.path.join(EVID, f\"render-r3-{iid}-why.png\"))\n            pg.keyboard.press(\"Escape\")\n        b.close()\n    out.append(f\"TOTAL bad hits across {len(flags) + len(entries)} Why panels: {total_hits}; pageerrors: {errs}\")\n    print(\"\\n\".join(out))\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:53:43.631Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/render_flags_r3.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:53:50.712Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I render_flags_r3.py http://127.0.0.1:54311 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 > render-flags-r3.out 2>&1; cut -c1-520 render-flags-r3.out",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:54:07.048Z

**tool result**
````
case HQ1eMZ... flags=['f_gap_r6_r7', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_r3_1', 'f_r8_1', 'f_r6_1', 'f_r7_1', 'f_r7_2', 'f_r8_2', 'f_r9_1'] entries=9
classic page title: Treatment timeline · render r3
f_gap_r6_r7: steps=6 bad-hits=[] key-steps=[]
f_accident_date_after_treatment_1_2_7: steps=6 bad-hits=[] key-steps=[]
f_cx1: steps=5 bad-hits=[] key-steps=[]
f_r3_1: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke'), ('agreement', 'Code', '✓ / Phrase list and prepared answers agree / Code / Passed /  / Both the phrase list and the prepared answers ')]
f_r8_1: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke'), ('agreement', 'Code', '✓ / Phrase list and prepared answers agree / Code / Passed /  / Both the phrase list and the prepared answers ')]
f_r6_1: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke'), ('agreement', 'Code', '✓ / Phrase list and prepared answers agree / Code / Passed /  / Both the phrase list and the prepared answers ')]
f_r7_1: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'AI check', '– / Prepared answers did not include this flag / AI check / Skipped /  / The phrase list found this flag but t'), ('agreement', 'Code', '○ / Phrase list and prepared answers agree / Code / Needs your decision /  / The phrase list found this flag b')]
f_r7_2: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke'), ('agreement', 'Code', '✓ / Phrase list and prepared answers agree / Code / Passed /  / Both the phrase list and the prepared answers ')]
f_r8_2: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke'), ('agreement', 'Code', '✓ / Phrase list and prepared answers agree / Code / Passed /  / Both the phrase list and the prepared answers ')]
f_r9_1: steps=8 bad-hits=[] key-steps=[('proposed_by_ai', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke'), ('agreement', 'Code', '✓ / Phrase list and prepared answers agree / Code / Passed /  / Both the phrase list and the prepared answers ')]
e1: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e2: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e3: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e4: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e5: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e6: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e7: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e8: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
e9: steps=11 bad-hits=[] key-steps=[('extracted', 'Prepared answer', '✓ / Prepared answer, standing in for the AI draft / Prepared answer / Passed /  / Prepared answer (hand-checke')]
TOTAL bad hits across 19 Why panels: 0; pageerrors: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:54:17.300Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_branch.py",
 "old_string": "it = c.get(f\"/api/cases/{tok}/items/{target}\").json()[\"item\"]",
 "new_string": "ct = c.get(f\"/api/cases/{tok}/trace\").json()\nfor sid in (\"extract\", \"judges\"):\n    x = next((s for s in ct[\"steps\"] if s[\"id\"] == sid), None)\n    print(f\"case-trace {sid}: label={x and x['label']!r} status={x and x['status']} why={x and x['why']!r} model={x and json.dumps((x.get('evidence') or {}).get('model'))}\")\nprint(\"/judges models:\", c.get(f\"/api/cases/{tok}/judges\").json().get(\"models\"))\nit = c.get(f\"/api/cases/{tok}/items/{target}\").json()[\"item\"]"
}
````

### User / tool · 2026-11-02T21:54:17.480Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_branch.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:54:19.818Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && for m in unsupported missing schema amount; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_branch.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/scratch $m > probe-r3-branch-$m.out 2>&1; echo \"== $m\"; grep -n \"^case-trace\\|^/judges models\\|^health\\|^case.models\" probe-r3-branch-$m.out | cut -c1-520; done",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:54:34.224Z

**tool result**
````
== unsupported
4:health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
5:case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
7:case-trace extract: label='Prepared summaries and quotes for each record, standing in for the AI draft' status=fail why='1 record has no prepared entry. Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.' model={"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true}
8:case-trace judges: label='Second AI check on every prepared item' status=pass why='The second check agreed with all 18 items it checked.' model=null
9:/judges models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
== missing
5:health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
6:case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
8:case-trace extract: label='Prepared summaries and quotes for each record, standing in for the AI draft' status=fail why='1 record has no prepared entry. The prepared answer for this record could not be used, so it has no entry.' model={"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true}
9:case-trace judges: label='Second AI check on every prepared item' status=pass why='The second check agreed with all 18 items it checked.' model=null
10:/judges models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
== schema
6:health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
7:case.models: {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
9:case-trace extract: label='AI drafts a summary and a quote for each record' status=fail why='1 record has no AI-made entry. The AI step failed on all three attempts, so this record has no AI-made entry.' model=null
10:case-trace judges: label='Second AI check on every AI-made item' status=pass why='The second check agreed with all 18 items it checked.' model=null
11:/judges models: {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5', 'generator_prepared': False}
== amount
4:health answers: prepared | health models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
5:case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
7:case-trace extract: label='Prepared summaries and quotes for each record, standing in for the AI draft' status=pass why='The prepared answers (hand-checked by the team for the demo) cover all 9 records.' model={"id": "hand-checked (qa)", "role": "generator", "independent_of_generator": null, "prepared": true}
8:case-trace judges: label='Second AI check on every prepared item' status=pass why='The second check agreed with all 19 items it checked.' model=null
9:/judges models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:54:41.943Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -8 | tee ../unit-prepared.out; wc -l tests/unit/test_prepared_provenance_r3.py; grep -n \"^def test\\|^    def test\" tests/unit/test_prepared_provenance_r3.py",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:54:55.762Z

**tool result**
````
......................                                                   [100%]
22 passed in 13.14s
     225 tests/unit/test_prepared_provenance_r3.py
95:def test_curated_flag_traces_say_prepared_and_never_ai_found_it(curated):
108:def test_curated_whole_surface_has_no_ai_authorship_wording(curated):
125:def test_curated_lexicon_only_flag_does_not_say_the_ai_looked(curated):
133:def test_recorded_flags_keep_ai_found_it(recorded):
144:def test_failed_prepared_item_trace_says_prepared(tmp_path, monkeypatch, mode):
157:def test_missing_curated_answer_never_shows_a_model_step(tmp_path, monkeypatch):
178:def test_recorded_missing_answer_is_a_fail_step_not_a_pass(tmp_path, monkeypatch):
202:def test_classic_redirects_to_the_guided_ui_in_demo_and_public_mode(tmp_path, monkeypatch, frontend):
210:def test_classic_stays_reachable_in_local_mode(tmp_path, monkeypatch, frontend):
217:def test_classic_stays_reachable_in_dev_mode(tmp_path, monkeypatch, frontend):
223:def test_classic_redirect_also_on_the_recorded_set(tmp_path, monkeypatch, frontend):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:54:57.083Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 100,200p tests/unit/test_prepared_provenance_r3.py"
}
````

### User / tool · 2026-11-02T21:54:57.270Z

**tool result**
````
    for f in flags:
        item = c.get(f"/api/cases/{tok}/items/{f['id']}").json()["item"]
        assert item["prepared"] is True, f["id"]
        st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
        assert "Prepared answer" in st["label"] and st["evidence"]["model"]["prepared"] is True and st["evidence"]["model"]["id"] == PREPARED_MODEL, (f["id"], st)
        assert not _hits(json.dumps(st)), (f["id"], st)


def test_curated_whole_surface_has_no_ai_authorship_wording(curated):
    c, tok = curated
    bad = {}
    for path in (f"/api/cases/{tok}", f"/api/cases/{tok}/trace", f"/api/cases/{tok}/judges", f"/api/cases/{tok}/audit", "/api/health", f"/api/cases/{tok}/status"):
        h = _hits(json.dumps(c.get(path).json()))
        if h:
            bad[path] = h
    for iid in _ids(c, tok):
        for suffix in ("", "/trace"):
            r = c.get(f"/api/cases/{tok}/items/{iid}{suffix}")
            if r.status_code == 200:
                h = _hits(json.dumps(r.json()))
                if h:
                    bad[f"{iid}{suffix}"] = h
    assert not bad, bad


def test_curated_lexicon_only_flag_does_not_say_the_ai_looked(curated):
    c, tok = curated
    for f in c.get(f"/api/cases/{tok}").json()["flags"]:
        if f.get("origin") == "lexicon":
            st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
            assert st["label"] != "AI found it" and "Prepared" in st["label"] and not _hits(st["why"]), st


def test_recorded_flags_keep_ai_found_it(recorded):
    c, tok = recorded
    fl = [f for f in c.get(f"/api/cases/{tok}").json()["flags"] if f.get("origin") in ("llm", "lexicon+llm")]
    assert fl
    for f in fl:
        st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
        assert st["label"] == "AI found it" and st["evidence"]["model"]["prepared"] is False


# ---- failed or missing prepared answers
@pytest.mark.parametrize("mode", ["unsupported", "schema"])
def test_failed_prepared_item_trace_says_prepared(tmp_path, monkeypatch, mode):
    c = _client(tmp_path, monkeypatch, fixture_dir=_mutated_set(tmp_path, mode))
    tok = _run(c, partial=True)
    tr = c.get(f"/api/cases/{tok}/items/e1/trace").json()
    st = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert st["status"] == "fail"
    if mode == "unsupported":
        assert st["evidence"]["model"]["prepared"] is True
    assert "AI drafted" not in st["label"] and "Prepared" in st["label"], st
    assert not _hits(json.dumps(st)), st
    assert not _hits(json.dumps(c.get(f"/api/cases/{tok}/items/e1").json()))


def test_missing_curated_answer_never_shows_a_model_step(tmp_path, monkeypatch):
    d = _mutated_set(tmp_path, "missing")
    (d.parent / "x").mkdir()
    # no recorded fallback exists for e1 because LLM_FIXTURE_DIR is set (fixture.call does not fall back then)
    c = _client(tmp_path, monkeypatch, fixture_dir=d)
    tok = _run(c, partial=True)
    item = c.get(f"/api/cases/{tok}/items/e1").json()["item"]
    assert item["state"] == "rejected" and "FIXTURE_MISS" in item["reasons"]
    st = next(s for s in c.get(f"/api/cases/{tok}/items/e1/trace").json()["steps"] if s["id"] == "extracted")
    assert st["status"] == "fail", st
    assert "claude-sonnet" not in json.dumps(st) and not _hits(json.dumps(st)) and "prepared" in st["label"].lower() and "no prepared answer" in st["why"].lower(), st
    assert not st["evidence"].get("model")
    assert not _hits(json.dumps(item))
    msg = c.get(f"/api/cases/{tok}/status").json().get("error", {}).get("message", "")
    assert msg and "The AI step" not in msg and not _hits(msg), msg      # the partial-run message on a curated set says nothing ran a model
    judges = c.get(f"/api/cases/{tok}/judges").json()
    assert judges["models"]["generator"] == PREPARED_MODEL and judges["models"]["generator_prepared"] is True
    ex = next(x for x in c.get(f"/api/cases/{tok}/trace").json()["steps"] if x["id"] == "extract")
    assert not _hits(json.dumps(ex)) and "claude-sonnet" not in json.dumps(ex), ex


def test_recorded_missing_answer_is_a_fail_step_not_a_pass(tmp_path, monkeypatch):
    d = tmp_path / "rec"
    d.mkdir()
    import os
    src = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
    for f in os.listdir(src):
        if f.endswith(".json") and f != f"{E1_KEY}.json":
            shutil.copy(os.path.join(src, f), d)
    c = _client(tmp_path, monkeypatch, fixture_dir=d)
    tok = _run(c, partial=True)
    st = next(s for s in c.get(f"/api/cases/{tok}/items/e1/trace").json()["steps"] if s["id"] == "extracted")
    assert st["status"] == "fail" and "The AI read this record" not in st["why"], st


# ---- /classic (D-068)
@pytest.fixture
def frontend(tmp_path):
    root = tmp_path / "fe"
    (root / "guided").mkdir(parents=True)
    (root / "guided" / "index.html").write_text("<html>guided</html>")
    (root / "index.html").write_text("<html>classic</html>")
    return root
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:54:59.603Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 1,95p tests/unit/test_prepared_provenance_r3.py"
}
````

### User / tool · 2026-11-02T21:54:59.711Z

**tool result**
````
"""T-177 round 3 (D-065, final): every backend-generated text for a PREPARED item says it is a prepared answer. Never 'AI drafted', 'AI found it', 'the AI's summary' or a model name.
Covers flag items (trace step + why + origin), failed prepared items (SUMMARY_NOT_IN_QUOTE, SCHEMA_INVALID), a missing curated answer (no model step), and /classic routing (D-068).
The recorded set keeps its AI wording."""
import json
import re
import shutil
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

PREPARED_MODEL = "hand-checked (qa)"
ALLOWED = "standing in for the AI draft"       # D-065's own pinned phrase
AI_WORDS = re.compile(r"AI draft|AI found|AI proposed|AI-made|AI read|AI wrote|the AI's|the AI did not|claude-sonnet", re.I)
E1_KEY = "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7"      # e1's curated generator answer


def _client(tmp_path, monkeypatch, fixture_set=None, fixture_dir=None, mode="local", static=None):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    if mode:
        monkeypatch.setenv("ZLAYT_MODE", mode)
    else:
        monkeypatch.delenv("ZLAYT_MODE", raising=False)
    for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET"):
        monkeypatch.delenv(k, raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    if fixture_dir:
        monkeypatch.setenv("LLM_FIXTURE_DIR", str(fixture_dir))
    return TestClient(create_app(str(tmp_path / "p.sqlite"), static_dir=str(static or tmp_path)), client=("127.0.0.1", 50000))


def _run(c, partial=False):
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready" or (partial and (s.get("error") or {}).get("code") == "run_partial"), json.dumps(s)[:1500]      # a record with no usable answer is a partial run, kept
    return tok


@pytest.fixture
def curated(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    return c, _run(c)


@pytest.fixture
def recorded(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch)
    return c, _run(c)


def _ids(c, tok):
    case = c.get(f"/api/cases/{tok}").json()
    return [x["id"] for k in ("entries", "flags", "amounts") for x in case.get(k, [])] + [x["id"] for x in case.get("tray", []) if isinstance(x, dict) and x.get("id")]


def _hits(text):
    return AI_WORDS.findall(text.replace(ALLOWED, ""))


def _mutated_set(tmp_path, mode):
    """Copy the curated set (+ recorded fallback, as fixture.call does) into tmp/curated; break e1's generator answer."""
    import os
    root = tmp_path / "mut"
    d = root / "curated"
    d.mkdir(parents=True)
    src = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
    for f in os.listdir(src):
        if f.endswith(".json"):
            shutil.copy(os.path.join(src, f), d)
    for f in os.listdir(os.path.join(src, "curated")):
        if f.endswith(".json"):
            shutil.copy(os.path.join(src, "curated", f), d)
    p = d / f"{E1_KEY}.json"
    if mode == "missing":
        p.unlink()
    else:
        o = json.loads(p.read_text())
        if mode == "unsupported":
            o["output"]["summary"] = "Patient reported paralysis of the left leg and loss of bladder control."
        else:
            o["output"].pop("summary", None)
        p.write_text(json.dumps(o))
    return d


# ---- flags on the curated set
def test_curated_flag_traces_say_prepared_and_never_ai_found_it(curated):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:55:09.139Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/mutate_r3.py",
 "content": "\"\"\"Mutants on the ARCHIVE copy only (never the repo). Usage: python -I mutate_r3.py apply|restore <archive_dir> <name>\nEach mutant is an exact-string replacement that must match exactly once (checked); restore re-extracts the file from `git show 2e58e18:<path>` and cmp-checks.\"\"\"\nimport subprocess\nimport sys\n\nMODE, ARCH, NAME = sys.argv[1:4]\nREPO = \"/Users/arsis/zlayt-pm-project\"\nM = {\n    \"M1_to_prepared_identity\": (\"app/backend/why.py\",\n        '    for a, b in _PREPARED_SWAP:\\n        if a in text:\\n            text = text.replace(a, b)\\n    return text',\n        '    return text'),\n    \"M2_flag_call_none\": (\"app/backend/present.py\",\n        '        if call is None and v.get(\"kind\") != \"entry\" and str(v[\"id\"]).startswith(\"f_\") and v.get(\"origin\") in FLAG_AI_ORIGINS:\\n            call = flag_generator_call(calls, v[\"id\"], v.get(\"type\"))',\n        '        if False:\\n            call = None'),\n    \"M3_classic_always_open\": (\"app/backend/api.py\",\n        '                return local_mode() or os.environ.get(\"ZLAYT_CLASSIC\") == \"1\"',\n        '                return True'),\n    \"M4_placeholder_branch_pass\": (\"app/backend/trace.py\",\n        '        elif placeholder:                                     # no usable answer',\n        '        elif False:                                     # no usable answer'),\n    \"M5_miss_not_excluded\": (\"app/backend/present.py\",\n        'gens = [c for c in calls if c[\"role\"] == \"generator\" and not str(c.get(\"error\") or \"\").startswith(\"FIXTURE_MISS\")]      # a call that found no answer',\n        'gens = [c for c in calls if c[\"role\"] == \"generator\"]      # a call that found no answer'),\n    \"M6_prompt_version_kept\": (\"app/backend/trace.py\",\n        '    ev[\"prompt_version\"] = None if ev[\"model\"][\"prepared\"] else ((call or {}).get(\"prompt_version\") or prompt_version)',\n        '    ev[\"prompt_version\"] = ((call or {}).get(\"prompt_version\") or prompt_version)'),\n}\npath, old, new = M[NAME]\nfull = f\"{ARCH}/{path}\"\nif MODE == \"apply\":\n    s = open(full).read()\n    assert s.count(old) == 1, f\"mutant {NAME}: expected 1 match, found {s.count(old)}\"\n    open(full, \"w\").write(s.replace(old, new))\n    s2 = open(full).read()\n    assert new in s2 and (old not in s2), \"apply did not take\"\n    print(\"applied\", NAME)\nelse:\n    orig = subprocess.run([\"git\", \"-C\", REPO, \"show\", f\"2e58e18:{path}\"], capture_output=True, check=True).stdout\n    open(full, \"wb\").write(orig)\n    assert open(full, \"rb\").read() == orig\n    print(\"restored\", NAME, \"cmp-identical to 2e58e18\")\n"
}
````

### User / tool · 2026-11-02T21:55:09.235Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/mutate_r3.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:55:12.958Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && A=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive; for m in M1_to_prepared_identity M2_flag_call_none M3_classic_always_open M4_placeholder_branch_pass M5_miss_not_excluded M6_prompt_version_kept; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I mutate_r3.py apply $A $m; (cd $A && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py -q -p no:cacheprovider -x 2>&1 | tail -3 | tr '\\n' ' '); echo; /Users/arsis/zlayt-pm-project/.venv/bin/python -I mutate_r3.py restore $A $m; done 2>&1 | tee mutants-r3.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:55:36.398Z

**tool result**
````
applied M1_to_prepared_identity
FAILED tests/unit/test_prepared_provenance_r3.py::test_curated_whole_surface_has_no_ai_authorship_wording !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!! 1 failed, 1 passed in 1.33s 
restored M1_to_prepared_identity cmp-identical to 2e58e18
applied M2_flag_call_none
FAILED tests/unit/test_prepared_provenance_r3.py::test_curated_flag_traces_say_prepared_and_never_ai_found_it !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!! 1 failed in 1.00s 
restored M2_flag_call_none cmp-identical to 2e58e18
applied M3_classic_always_open
FAILED tests/unit/test_prepared_provenance_r3.py::test_classic_redirects_to_the_guided_ui_in_demo_and_public_mode !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!! 1 failed, 8 passed in 4.58s 
restored M3_classic_always_open cmp-identical to 2e58e18
applied M4_placeholder_branch_pass
FAILED tests/unit/test_prepared_provenance_r3.py::test_failed_prepared_item_trace_says_prepared[schema] !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!! 1 failed, 5 passed in 3.14s 
restored M4_placeholder_branch_pass cmp-identical to 2e58e18
applied M5_miss_not_excluded
FAILED tests/unit/test_prepared_provenance_r3.py::test_missing_curated_answer_never_shows_a_model_step !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!! 1 failed, 6 passed in 3.77s 
restored M5_miss_not_excluded cmp-identical to 2e58e18
applied M6_prompt_version_kept
......................                                                   [100%] 22 passed in 7.65s 
restored M6_prompt_version_kept cmp-identical to 2e58e18
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:55:42.012Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF'\nimport re\np='mutate_r3.py'\ns=open(p).read()\nadd='''    \"M7_call_prompt_kept\": (\"app/backend/present.py\",\n        '\"prompt_version\": None if prep else c[\"prompt_version\"], \"prompt_sha256\": None if prep else c[\"prompt_sha256\"]',\n        '\"prompt_version\": c[\"prompt_version\"], \"prompt_sha256\": c[\"prompt_sha256\"]'),\n    \"M8_export_prompt_kept\": (\"app/backend/api.py\",\n        'if x[\"prompt_version\"] and not AU.is_prepared(x.get(\"recorded_from\"))}',\n        'if x[\"prompt_version\"]}'),\n}\npath, old, new'''\ns=s.replace('}\\npath, old, new', add, 1)\nopen(p,'w').write(s)\nEOF\nA=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive; for m in M7_call_prompt_kept M8_export_prompt_kept; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I mutate_r3.py apply $A $m; (cd $A && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py -q -p no:cacheprovider 2>&1 | tail -3 | tr '\\n' ' '); echo; /Users/arsis/zlayt-pm-project/.venv/bin/python -I mutate_r3.py restore $A $m; done 2>&1 | tee -a mutants-r3.out; grep -rn \"prompt_sha256\\|prompt_version\" $A/tests/unit/test_prepared_provenance*.py $A/tests/e2e/test_demo_provenance.py | head",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:55:58.216Z

**tool result**
````
applied M7_call_prompt_kept
......................                                                   [100%] 22 passed in 7.59s 
restored M7_call_prompt_kept cmp-identical to 2e58e18
applied M8_export_prompt_kept
......................                                                   [100%] 22 passed in 7.83s 
restored M8_export_prompt_kept cmp-identical to 2e58e18
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:56:01.031Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -rln \"hand-checked\\|PREPARED_MODEL\\|is_prepared\\|prepared\" tests/unit tests/e2e | head -20; grep -rn \"prompt_versions\" tests/unit tests/e2e | head"
}
````

### User / tool · 2026-11-02T21:56:01.155Z

**tool result**
````
tests/unit/test_t183_hardening.py
tests/unit/test_prepared_provenance_r3.py
tests/unit/test_prepared_provenance.py
tests/e2e/test_mvp_polish.py
tests/e2e/test_demo_provenance.py
tests/e2e/guided/test_shell_smoke.py
tests/e2e/conftest.py
tests/unit/test_trace.py:421:    assert "judge_faithfulness_v1" in rep["prompt_versions"]
tests/unit/test_t093_eval_signature.py:110:def test_live_metrics_writes_one_artifact_per_run_with_items_states_codes_and_prompt_versions(tmp_path):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:56:05.199Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && A=$PWD; P=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3; for m in M7_call_prompt_kept M8_export_prompt_kept M6_prompt_version_kept; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I $P/mutate_r3.py apply $A $m; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t183_hardening.py tests/unit/test_trace.py tests/unit/test_audit.py tests/unit/test_export.py -q -p no:cacheprovider 2>&1 | tail -2 | tr '\\n' ' '; echo; /Users/arsis/zlayt-pm-project/.venv/bin/python -I $P/mutate_r3.py restore $A $m; done 2>&1 | tee -a $P/mutants-r3.out; ls tests/unit | grep -i \"audit\\|export\" | head",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T21:56:06.024Z

**tool result**
````
applied M7_call_prompt_kept
 no tests ran in 0.00s 
restored M7_call_prompt_kept cmp-identical to 2e58e18
applied M8_export_prompt_kept
 no tests ran in 0.00s 
restored M8_export_prompt_kept cmp-identical to 2e58e18
applied M6_prompt_version_kept
 no tests ran in 0.00s 
restored M6_prompt_version_kept cmp-identical to 2e58e18
spawn_audit.py
test_audited.py
test_export.py
test_export_edge.py
test_t113_heldout_audit.py
test_t159_flag_audit.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:56:09.741Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && A=$PWD; P=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; $PY -m pytest tests/unit/test_t183_hardening.py tests/unit/test_trace.py tests/unit/test_audited.py tests/unit/test_export.py -q -p no:cacheprovider 2>&1 | tail -2 | tr '\\n' ' '; echo \"<- baseline\"; for m in M7_call_prompt_kept M8_export_prompt_kept M6_prompt_version_kept; do $PY -I $P/mutate_r3.py apply $A $m; $PY -m pytest tests/unit/test_t183_hardening.py tests/unit/test_trace.py tests/unit/test_audited.py tests/unit/test_export.py -q -p no:cacheprovider 2>&1 | tail -2 | tr '\\n' ' '; echo; $PY -I $P/mutate_r3.py restore $A $m; done 2>&1 | tee -a $P/mutants-r3.out",
 "timeout": 500000
}
````

### User / tool · 2026-11-02T21:57:06.194Z

**tool result**
````
........................................................................ [100%] 144 passed in 13.21s <- baseline
applied M7_call_prompt_kept
........................................................................ [100%] 144 passed in 13.44s 
restored M7_call_prompt_kept cmp-identical to 2e58e18
applied M8_export_prompt_kept
........................................................................ [100%] 144 passed in 13.31s 
restored M8_export_prompt_kept cmp-identical to 2e58e18
applied M6_prompt_version_kept
........................................................................ [100%] 144 passed in 13.16s 
restored M6_prompt_version_kept cmp-identical to 2e58e18
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:57:30.592Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n '\"edit\"' app/backend/review.py | head -8; grep -n \"action.*edit\\|excerpt\\b.*summary\" memory/contracts/api.md | head -10"
}
````

### User / tool · 2026-11-02T21:57:30.683Z

**tool result**
````
17:ACTIONS = ("accept", "dismiss", "reset", "edit", "count")      # count (D-064): an amount held back for a missing detail becomes an accepted charge, see count_charge.py
302:    if item["state"] == "rejected" and action in ("accept", "edit"):
304:    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
419:        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
462:    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
30:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
33:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset, and (D-064) `count` + `confirm: "separate_charge"` for an amount held back only for a missing detail (see `countable`).  D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
137:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
172:        "human": {"action": null, "edited_text": null, "at": null} }
183:        "state": "verified", "human": {"action": null, "edited_text": null, "at": null} } },
193:        "state": "needs_review", "human": {"action": null, "edited_text": null, "at": null}} } ],
216:        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
230:        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
243:        "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} } ],
287:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. Each element also has `record_seq` (the record whose date was confirmed). **T-127: the change is kept with the case.** `confirm_date` writes `gap_changes[]` into its `confirm_date` review event (`after.gap_changes`), and `GET /api/cases/{token}` reads it back: a gap flag in `flags[]` whose figures were moved by a confirm_date has `gap_change` (the same element: `{flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to, record_seq, sentence}`), otherwise `gap_change: null`; it stays through reload, another browser and review actions, and goes when that gap's current figures differ from the ones the change produced (a later confirm_date that moves it again replaces it). A gap that no longer applies has no flag, so `GET case` lists it in top-level `gap_changes_removed[]` (same element, `change: "removed"`, `sentence` included) until a gap with the same id exists again. Both are always present (`null` / `[]`). Stored in the DB (the audit event), not in `computed`. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:57:32.969Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && sed -n 425,452p app/backend/review.py | cut -c1-240"
}
````

### User / tool · 2026-11-02T21:57:33.056Z

**tool result**
````
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
    if rec is None:
        raise _bad("The entry's source record is missing.")
    prev = item.get("edited") or {}
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    trimmed = None
    summary_before_trim = new_sum
    if "summary" not in edits and charge_text.has_currency(new_sum) and not charge_text.has_currency(new_exc):
        tr = charge_text.trim_summary(new_sum)          # T-139: the quote she picked no longer states the amount; code removes the trailing amount clause (D-054 suffix rule)
        if tr["changed"] and not charge_text.has_currency(tr["text"]):
            new_sum, trimmed = tr["text"], tr
    span = None
    if "excerpt" in edits:
        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call,
                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []),
                         bill_state=lambda: bill_state_for(conn, case_id, item.get("record_ids")))
    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    edited = dict(prev)
    edited.update(at=store.iso(t))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:57:47.869Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_edit.py",
 "content": "\"\"\"T-177 r3 paralegal-edit probe (staff-engineer-reviewer). Demo-mode curated server from the archive of 2e58e18.\nA reader's normal demo action: change the QUOTE of a prepared entry (summary left alone) and accept it. Reports every sentence the API returns for that item.\nUsage: python -I probe_r3_edit.py <base_url>\"\"\"\nimport json\nimport re\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE = sys.argv[1].rstrip(\"/\")\nPAT = re.compile(r\"AI draft|AI found|AI proposed|AI wrote|AI-made|AI read|AI translat|AI wording|AI's|AI picked|AI summary|the AI |The AI |AI gave|AI answer|recorded AI|claude-sonnet|drafted with AI\")\nD065 = \"standing in for the AI draft\"\n\n\ndef call(method, path, body=None):\n    req = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body).encode(), method=method, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            return r.status, json.loads(r.read().decode())\n    except urllib.error.HTTPError as e:\n        raw = e.read().decode()\n        try:\n            return e.code, json.loads(raw)\n        except ValueError:\n            return e.code, raw\n\n\ndef show(label, obj):\n    t = json.dumps(obj, ensure_ascii=False).replace(D065, \"<D065>\")\n    hits = sorted({t[max(0, m.start() - 60): m.end() + 50] for m in PAT.finditer(t)})\n    print(f\"{label}: {len(hits)} authorship-pattern hit(s)\")\n    for h in hits:\n        print(f\"    ...{h}...\")\n\n\ndef main():\n    s, c = call(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"edit r3\"})\n    tok = c[\"token\"]\n    call(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(600):\n        if call(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    case = call(\"GET\", f\"/api/cases/{tok}\")[1]\n    e9 = next(e for e in case[\"entries\"] if e[\"id\"] == \"e9\")\n    print(\"e9 before:\", json.dumps({k: e9.get(k) for k in (\"state\", \"prepared\", \"summary\", \"excerpt\")}, ensure_ascii=False))\n    s, r = call(\"POST\", f\"/api/cases/{tok}/items/e9/review\", {\"action\": \"edit\", \"excerpt\": \"Discharged from PT after two missed appointments.\"})\n    print(\"edit quote only ->\", s, json.dumps(r, ensure_ascii=False)[:700])\n    show(\"edit response\", r)\n    s, it = call(\"GET\", f\"/api/cases/{tok}/items/e9\")\n    print(\"e9 after:\", json.dumps({k: it[\"item\"].get(k) for k in (\"state\", \"prepared\", \"why\", \"reasons\")}, ensure_ascii=False)[:600])\n    show(\"item e9\", it)\n    s, tr = call(\"GET\", f\"/api/cases/{tok}/items/e9/trace\")\n    show(\"trace e9\", tr)\n    for st in tr.get(\"steps\", []):\n        if PAT.search(json.dumps(st, ensure_ascii=False).replace(D065, \"\")):\n            print(\"   step\", st[\"id\"], \"|\", st[\"label\"], \"|\", st[\"why\"][:200])\n    show(\"case trace\", call(\"GET\", f\"/api/cases/{tok}/trace\")[1])\n    show(\"judges\", call(\"GET\", f\"/api/cases/{tok}/judges\")[1])\n    # now edit the summary too (hand-written) and accept everything else, then export\n    s, r2 = call(\"POST\", f\"/api/cases/{tok}/items/e9/review\", {\"action\": \"edit\", \"summary\": \"Discharged from physical therapy after two missed appointments.\"})\n    print(\"edit summary ->\", s, json.dumps(r2, ensure_ascii=False)[:300])\n    show(\"edit-summary response\", r2)\n    for e in case[\"entries\"]:\n        if e[\"id\"] != \"e9\":\n            call(\"POST\", f\"/api/cases/{tok}/items/{e['id']}/review\", {\"action\": \"accept\"})\n    s, ex = call(\"GET\", f\"/api/cases/{tok}/export\")\n    print(\"export ->\", s)\n    if s == 200:\n        show(\"export\", ex)\n        notes = ex.get(\"internal_notes_text\", \"\")\n        i = notes.find(\"drafted\")\n        print(\"   notes line:\", notes[max(0, i - 30): i + 160].replace(\"\\n\", \" \"))\n        for line in notes.splitlines():\n            if \"AI wording\" in line or \"prepared\" in line.lower() or \"hand\" in line.lower():\n                print(\"   notes:\", line[:220])\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T21:57:47.962Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/probe_r3_edit.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:57:50.361Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_edit.py http://127.0.0.1:54310 > probe-r3-edit.out 2>&1; cut -c1-900 probe-r3-edit.out",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T21:57:50.918Z

**tool result**
````
e9 before: {"state": "verified", "prepared": true, "summary": "Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.", "excerpt": "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."}
edit quote only -> 422 {"error": {"code": "invalid_edit", "message": "Nothing to edit.", "detail": {}}}
edit response: 0 authorship-pattern hit(s)
e9 after: {"state": "verified", "prepared": true, "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "reasons": []}
item e9: 0 authorship-pattern hit(s)
trace e9: 0 authorship-pattern hit(s)
case trace: 1 authorship-pattern hit(s)
    ... items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": ...
judges: 0 authorship-pattern hit(s)
edit summary -> 422 {"error": {"code": "invalid_edit", "message": "Nothing to edit.", "detail": {}}}
edit-summary response: 0 authorship-pattern hit(s)
export -> 200
export: 1 authorship-pattern hit(s)
    ..."INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section w...
   notes line: NOT SEND  This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 15.  FLAGS ACCEPTED - none  FLAGS DISMISSED -
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:57:53.077Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"Nothing to edit\" app/backend/*.py | head -3; sed -n 402,424p app/backend/review.py | cut -c1-220"
}
````

### User / tool · 2026-11-02T21:57:53.172Z

**tool result**
````
app/backend/review.py:415:        raise _bad("Nothing to edit.")
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error, "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
    edits = body.get("edits")
    if kind == "amount":
        raise _bad("A charge can only be accepted or dismissed.")
    if not isinstance(edits, dict) or not edits:
        raise _bad("Nothing to edit.")
    if kind == "flag":
        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
            raise _bad("Only a note can be added to a flag.")
        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
        return []
    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
    case = DB.get_case(conn, case_id)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:57:58.477Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF'\np='probe_r3_edit.py'\ns=open(p).read()\ns=s.replace('{\"action\": \"edit\", \"excerpt\": \"Discharged from PT after two missed appointments.\"}','{\"action\": \"edit\", \"edits\": {\"excerpt\": \"Recommend cervical epidural steroid injection.\"}}')\ns=s.replace('{\"action\": \"edit\", \"summary\": \"Discharged from physical therapy after two missed appointments.\"}','{\"action\": \"edit\", \"edits\": {\"summary\": \"Cervical epidural steroid injection recommended.\"}}')\ns=s.replace('''    # now edit the summary too''','''    s, rf = call(\"POST\", f\"/api/cases/{tok}/items/f_r3_1/review\", {\"action\": \"edit\", \"edits\": {\"note\": \"checked\"}})\n    print(\"flag note edit ->\", s, json.dumps(rf, ensure_ascii=False)[:200])\n    show(\"flag edit response\", rf)\n    show(\"flag trace f_r3_1 after note\", call(\"GET\", f\"/api/cases/{tok}/items/f_r3_1/trace\")[1])\n    # now edit the summary too''')\nopen(p,'w').write(s)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r3_edit.py http://127.0.0.1:54310 > probe-r3-edit.out 2>&1; cut -c1-1100 probe-r3-edit.out",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T21:57:59.067Z

**tool result**
````
e9 before: {"state": "verified", "prepared": true, "summary": "Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.", "excerpt": "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."}
edit quote only -> 422 {"error": {"code": "invalid_edit", "message": "The summary has a number, date or dollar figure that is not in the quote: january. Remove it or change the quote.", "detail": {"tokens": ["january"], "reason": "SUMMARY_NUMBER_NOT_IN_EXCERPT"}}}
edit response: 0 authorship-pattern hit(s)
e9 after: {"state": "verified", "prepared": true, "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "reasons": []}
item e9: 0 authorship-pattern hit(s)
trace e9: 0 authorship-pattern hit(s)
case trace: 1 authorship-pattern hit(s)
    ... items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": ...
judges: 0 authorship-pattern hit(s)
flag note edit -> 200 {"item": {"id": "f_r3_1", "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "review_status": "edited", 
flag edit response: 0 authorship-pattern hit(s)
flag trace f_r3_1 after note: 0 authorship-pattern hit(s)
edit summary -> 422 {"error": {"code": "invalid_edit", "message": "The quote carries a phrase that says whose account the quote gives that the summary leaves out. Put it back in the summary.", "detail": {"qualifiers": ["self_report"], "reason": "SUMMARY_DROPS_QUALIFIER"}}}
edit-summary response: 0 authorship-pattern hit(s)
export -> 200
export: 1 authorship-pattern hit(s)
    ..."INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment section w...
   notes line: NOT SEND  This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 14.  FLAGS ACCEPTED - Prior condition: record
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:58:04.330Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && env -u E2E_BASE_URL -u ZLAYT_DB E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_demo_provenance.py -q -p no:cacheprovider 2>&1 | tail -6 | tee ../e2e-provenance.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:58:12.937Z

**tool result**
````
.......                                                                  [100%]
7 passed in 7.63s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:58:19.797Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -c -i \"flag\" tests/e2e/test_demo_provenance.py; git -C /Users/arsis/zlayt-pm-project diff --stat 2e58e18 fa4f79e -- app/backend/trace.py app/backend/present.py app/backend/why.py app/backend/api.py app/backend/export.py | tail -3; ls /Users/arsis/zlayt-pm-project/reviews | grep \"T-177\""
}
````

### User / tool · 2026-11-02T21:58:19.933Z

**tool result**
````
0
 app/backend/export.py  | 10 +++++++++-
 app/backend/present.py |  1 +
 2 files changed, 10 insertions(+), 1 deletion(-)
T-177-staff-engineer-r2.md
T-177-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:58:21.927Z

**tool call — Bash**
````
{
 "command": "for p in 25329 26866; do ps -p $p -o pid,command | tail -1 | cut -c1-120; lsof -p $p -a -d cwd -Fn | tail -1; done"
}
````

### User / tool · 2026-11-02T21:58:22.129Z

**tool result**
````
25329 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/
n/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive
26866 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/
n/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:58:23.567Z

**tool call — Bash**
````
{
 "command": "kill 25329 26866; sleep 2; lsof -nP -iTCP:54310 -iTCP:54311 -sTCP:LISTEN | cat; echo \"listeners after: none above means stopped\"; ps -p 25329,26866 | cat"
}
````

### User / tool · 2026-11-02T21:58:25.772Z

**tool result**
````
listeners after: none above means stopped
  PID TTY           TIME CMD
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:58:30.826Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"code removed the whole AI summary\\|the AI gave no usable answer\\|from the quote the AI picked\\|from the end of the AI's summary\\|AI-made entry\\|recorded AI answer\" app/backend/trace.py app/backend/why.py app/backend/present.py | cut -c1-200; grep -n \"def models_for\\|gens = \\[c for c in calls\\|prepared = bool(gens)\" app/backend/present.py; grep -n \"if prepared:\" app/backend/present.py | head -3; grep -n \"AI_WORDS\" tests/unit/test_prepared_provenance_r3.py | head -2; grep -n \"AI wording\" app/backend/export.py app/backend/review.py | cut -c1-120; grep -n \"Drafted by\" app/frontend/judges.js | head -3"
}
````

### User / tool · 2026-11-02T21:58:30.943Z

**tool result**
````
app/backend/why.py:17:    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
app/backend/why.py:33:    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
app/backend/why.py:35:    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no AI-made entry. Read the record yourself or write the
app/backend/why.py:90:    ("The demo has no recorded AI answer for this step, so this item has not been checked.", "The demo has no prepared answer for this step, so this item has not been checked."),
app/backend/why.py:95:    ("The AI step failed on all three attempts, so this record has no AI-made entry.", "The prepared answer for this record could not be used, so it has no entry."),
app/backend/why.py:97:    ("so it has no AI-made entry.", "so it has no entry."),
app/backend/trace.py:306:                        "SUMMARY_NOT_IN_QUOTE": "Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.",
app/backend/trace.py:307:                        "LLM_FAILED_AFTER_RETRIES": "Not run: the AI gave no usable answer for this record.",
app/backend/trace.py:308:                        "FIXTURE_MISS": "Not run: the AI gave no usable answer for this record.",
app/backend/trace.py:387:                        f"Code removed {_q(nar['dropped'])} from the quote the AI picked. Why: it states a dollar amount. {_NO_LETTER} What is left is whole, "
app/backend/trace.py:393:                        f"Code removed {_q(nar['summary_removed'])} from the end of the AI's summary. Why: it states a dollar amount, and the shortened quote no longer carries
app/backend/trace.py:407:                 f"Code removed {_q(ct['removed'])} from the end of the AI's summary when you changed the quote. Why: the new quote does not state the amount, and "
293:    gens = [c for c in calls if c["role"] == "generator" and c["step"] == step and not str(c.get("error") or "").startswith("FIXTURE_MISS")]
305:def models_for(conn, case_id, base, calls=None):
309:    gens = [c for c in calls if c["role"] == "generator" and not str(c.get("error") or "").startswith("FIXTURE_MISS")]      # a call that found no answer is no model's work and no fixture's
310:    prepared = bool(gens) and all(AU.is_prepared(c.get("recorded_from")) for c in gens)
276:        if prepared:
282:            if prepared:
16:AI_WORDS = re.compile(r"AI draft|AI found|AI proposed|AI-made|AI read|AI wrote|the AI's|the AI did not|claude-sonnet", re.I)
65:    return AI_WORDS.findall(text.replace(ALLOWED, ""))
app/backend/export.py:661:            if e.get("original_summary_failed"):        # D-051: AI wording that failed a code
app/backend/export.py:662:                bits.append(f'summary was AI wording removed (failed a check: {"; ".join(e["or
app/backend/export.py:719:            lines.append(f'- AI wording removed (failed a check: {_removed_why(r)}) ({r["entry
app/backend/review.py:72:# plain words for "AI wording removed (failed a check: ...)" in the internal notes
app/backend/review.py:464:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (seco
app/backend/review.py:484:    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-c
171:        "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:58:33.440Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n 'prep = bool(cx.models.get(\"generator_prepared\"))' app/backend/trace.py; sed -n 300,312p app/backend/trace.py | cut -c1-140; sed -n 165,172p app/frontend/judges.js | cut -c1-160; grep -n \"SCHEMA_INVALID\\|recorded_from\" app/llm/audited.py | head -12"
}
````

### User / tool · 2026-11-02T21:58:33.564Z

**tool result**
````
1120:    prep = bool(cx.models.get("generator_prepared"))      # T-177 r2 / D-065: the case's answers are hand-checked fixtures, so the step must not say an AI drafted them


def _skipped(sid, label, kind, code, rule=None, rule_text=None):
    msg = rule_text or {"GROUNDING_EXCERPT_NOT_VERBATIM": "Not run: the quote did not pass the word-for-word check.",
                        "GROUNDING_AMOUNT_NOT_IN_TEXT": "Not run: the amount is not in the record text.",
                        "SCHEMA_INVALID": "Not run: the AI answer was malformed.",
                        "SUMMARY_NOT_IN_QUOTE": "Not run: code removed the whole AI summary because the quote does not support it, so there 
                        "LLM_FAILED_AFTER_RETRIES": "Not run: the AI gave no usable answer for this record.",
                        "FIXTURE_MISS": "Not run: the AI gave no usable answer for this record.",
                        "UNSUPPORTED_LANGUAGE": "Not run: the record is not in a language the AI reads."}.get(code, "Not run because an earl
    return step(sid, label, kind, SKIPPED, msg, reason=code, rule=rule)


      (prepared ? "This shows how a second AI model checked the answers our team prepared for this demo. " : "This shows how a second AI model checked the first
    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
    const t = d.totals || {}, m = d.models || {}, items = byItem(d);
    det.append(prepared
      ? el("p", { class: "zj-models", "data-testid": "judge-model-line" }, "Prepared by our team (not by an AI model), checked by ", el("strong", {}, m.judge ||
      : el("p", { class: "zj-models", "data-testid": "judge-model-line" },
        "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
        d.independent_models ? " (a different model, so it does not grade its own work)." : " (the same model: this check is weaker, read more closely)."));
36:    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
56:    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
68:PREPARED_BACKEND = "curated"      # D-065: recorded_from.backend of a hand-checked fixture (tests/fixtures/llm/curated); it is never model output
71:def is_prepared(recorded_from) -> bool:
72:    return isinstance(recorded_from, dict) and recorded_from.get("backend") == PREPARED_BACKEND
82:    """D-065: a curated answer's audit row names who made it (the fixture's own recorded_from.model, 'hand-checked (qa)'), never the model the pipeline asked for."""
83:    if res is not None and is_prepared(res.recorded_from):
84:        return str(res.recorded_from.get("model") or "hand-checked (qa)")
124:                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:07.111Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/draft-r3.md",
 "content": "# T-177 round 3 (final; D-065 honest provenance): staff-engineer-reviewer\n\n**Verdict: fail (2 blockers, 1 major, 2 minors, 1 nit).** The three round-2 items are fixed on everything the shipped sample reaches: the 19 Why panels of the sample (10 flags, 9 entries) show no \"AI found it\", \"AI draft\" or model name, and an HTTP walk of the sample's case, judges, audit, trace, status, every item, every item trace and the export finds no authorship wording on a prepared item. They are not closed on the failure paths the round-2 brief named. A malformed curated answer flips the whole case back to \"Drafted by claude-sonnet-5-5\" (the round-1 blocker). A failed curated answer and a missing one still have seven trace steps that call the summary or answer \"the AI's\". A closed swap table (`why.to_prepared`) is the root cause: any fixed sentence that is not on the list leaks. The shipped curated files do not reach these paths, so the demo a reader sees today is clean; I rated them the way round 2 rated the latent F-B, by the rule and not by reach.\n\n**Scope.** Card commit 2e58e18, reviewed from `git archive 2e58e18` (`artifacts/review-evidence/T-177-staff-engineer-r3/archive-source-sha.txt`). HEAD is now fa4f79e; it changes `app/backend/export.py` and `app/backend/present.py` after 2e58e18, and I did not review those hunks. Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r3/`.\n\n**Round-2 status**\n\n| Round-2 item | Status at 2e58e18 |\n|---|---|\n| F-A blocker: curated flag Why panels said \"AI found it\" / \"AI draft\" | Fixed on the sample. `render-flags-r3.out`: 19 Why panels, 0 bad hits; 7 flags read \"Prepared answer, standing in for the AI draft\"; f_r7_1 reads \"Prepared answers did not include this flag\" and its sentence agrees (F-E also fixed) |\n| F-B blocker: failed prepared item says \"AI drafted\" | Not closed. The headline step now keeps the Prepared label; seven other steps of the same trace still say \"the whole AI summary\" (F1 below) |\n| F-C major: missing curated answer shows a passing AI step naming a model | Partly closed. The step is now a FAIL with no model. The item's own `why` and seven more steps still say \"recorded AI answer\" / \"the AI gave no usable answer\" (F2); the schema variant of the same fault flips the case to claude-sonnet-5-5 (F3) |\n| F-D nit: prompt version and hash on prepared rows | Fixed at the API (audit rows null, export `prompt_versions` has only judge prompts). No test guards it (F4) |\n| F-E minor: \"AI found it\" beside \"AI did not find it\" | Fixed |\n\n## Residuals the worker listed (item 3)\n\n| Residual | Decision | Why |\n|---|---|---|\n| `/health` answers `prepared` with a curated key missing | Fine | It states which fixture set the process uses, not who wrote an answer. In the missing-key run `probe-r3-branch-missing.out` shows run status `failed`, e1 `rejected` with FIXTURE_MISS, and `models.generator` still `hand-checked (qa)`. The per-item truth is on the item. The mixed library case under a curated process is the accepted round-1 F4 |\n| Export disclosure line \"drafted with AI assistance\" | Not a blocker or major; minor (F5) | `export.py:29` and `:733` put it in the INTERNAL REVIEW NOTES block only; the letter text has none (D-009 holds). It labels no item and names no model. It still sits badly beside a badge that says the answers were not written by an AI model, so it should have a prepared variant |\n| review.py edit and manual warnings say \"AI wording\" | The claim is wrong about where; nothing to fix in review.py | In `review.py` the phrase is in comments only (lines 72, 464, 484). The edit and manual-entry warnings I read (`review.py:399-402`) say \"The second check ...\". The same phrase is a real message at `export.py:662` and `:719` (internal notes, only for an edited entry whose original failed a code check). I did not reach that path; it is latent and a nit |\n\n## Findings\n\n**F1 blocker: a malformed curated answer flips the whole case back to \"Drafted by claude-sonnet-5-5\" and \"AI-made\".** Reproduction: `probe-r3-branch-schema.out` (curated copy, e1's `summary` key removed). `case.models` and `/judges` `models` are `generator: claude-sonnet-5-5, generator_prepared: false`; the case trace `extract` step reads \"AI drafts a summary and a quote for each record\" / \"no AI-made entry\", the `judges` step \"Second AI check on every AI-made item\". Eight of the nine entries are still prepared. Cause: the first attempt is a SCHEMA_INVALID row with no `recorded_from`, the retry is FIXTURE_MISS and is excluded, so `present.py:309-310` computes `all(is_prepared(...))` over one non-prepared row and gets False. `judges.js:168-171` then prints \"Drafted by claude-sonnet-5-5\". `/api/health` in the same run still says `answers: prepared`. This is round-1 F1. The worker's `test_failed_prepared_item_trace_says_prepared[schema]` (`tests/unit/test_prepared_provenance_r3.py:144`) reads only e1's `extracted` step.\n\n**F2 blocker: fixed AI-authorship sentences that are not in the swap table survive on prepared items.** Two families, both reproduced:\n- Failed prepared answer: `probe-r3-branch-unsupported.out`. e1 is `prepared: true`, model `hand-checked (qa)`, and seven steps (`excerpt_verbatim`, `excerpt_whole_sentence`, `excerpt_hedge`, `summary_tokens`, `summary_qualifier`, `highlight`, `judge_1`) read \"Not run: code removed the whole AI summary because the quote does not support it\" (`trace.py:306`). The team wrote that summary.\n- Code trims on a prepared answer that states an amount: `probe-r3-branch-amount.out` (ER entry's curated quote and summary carry \"$6,240\"). e2 is `prepared: true`, `verified`; its `excerpt_narrowed` step says \"from the quote the AI picked\" (`trace.py:387`) and `charge_clause_removed` says \"from the end of the AI's summary\" (`trace.py:393`; `:407` says the same after a quote edit). The shipped curated files hold no amount in a quote, so the sample does not reach this.\nThe swap table (`why.py:89-111`) lists 23 sentences; `_skipped` (`trace.py:303-309`) and the trim sentences are not on it. The worker's scan regex (`test_prepared_provenance_r3.py:16`) has no \"AI summary\", \"AI picked\", \"AI gave\" or \"AI answer\", so a test that only ran the happy sample could not see them.\n\n**F3 major: a missing or unusable curated answer still reads as an AI matter on the item and in seven steps.** `probe-r3-branch-missing.out`: e1's own `why` in `GET /api/cases/{tok}` and `GET .../items/e1` is \"The demo has no recorded AI answer for this step\" (`why.py:17`; `present.py:276` swaps only when `item.prepared`, and a miss is `prepared: false`), while the trace reason for the same item says \"no prepared answer\". The seven check steps say \"Not run: the AI gave no usable answer for this record\" (`trace.py:307-308`); no AI was asked. AC1 forbids \"recorded AI answers\" on a curated item. The extracted step itself is now correct (FAIL, no model, \"There is no prepared answer for this record in the demo\").\n\n**F4 minor: the prompt-version and hash fix has no test.** Mutants on the archive copy that put the prompt version back survive: M6 (`trace.py` evidence), M7 (`present.py` `_call`, audit rows) and M8 (`api.py` export `prompt_versions`) all leave the 22 prepared-provenance tests and the 144 trace, audit and export tests green (`mutants-r3.out`). The round-2 acceptance test for F-D was not written.\n\n**F5 minor: the export notes line says \"drafted with AI assistance\" for a curated export.** `export.py:29`, used at `:733`; `probe-r3-curated.out` shows it in `internal_notes_text` of the sample export while `provenance.generator_prepared` is true. Not item-level and not in the letter, so I did not rate it above minor. Fix: a prepared variant (\"built from answers prepared by the team and checked by a second AI model\") when the case's models are prepared.\n\n**F6 nit: the skipped \"Prepared answers did not include this flag\" step carries the kind tag \"AI check\".** `render-flags-r3.out`, f_r7_1: key step `('proposed_by_ai', 'AI check', ...)`. The step ran no AI.\n\n## What I exercised\n\nOwn servers from the archive on loopback ports 54310 (demo mode, no `ZLAYT_MODE`) and 54311 (`ZLAYT_MODE=local`), both `LLM_BACKEND=fixture FIXTURE_SET=curated`. PIDs 25329 and 26866; cwd checked before `kill`; both listeners gone afterwards. The shared app and other agents' processes were not touched.\n\nGrep of every API response (health, case, judges, audit, trace, status, every item and item trace, export after accept-all) for \"AI drafted\", \"AI found\" and model names:\n- **Sample, demo mode** (`probe-r3-curated.out`): 16 of 23 items prepared (9 entries, 7 flags; the 4 amounts and 3 code-made flags are not model answers). Two hits, neither on an item: the case trace \"the AI disclosure line will count them\" and the export notes line (F5). No model name anywhere.\n- **Sample, local mode** (`probe-r3-curated-local.out`): the same two hits.\n- **Library cases** (local mode only; the library route is 404 in demo mode): case_lib01, lib02, lib09, lib10 run on the recorded answers (the curated set has 19 files, all for the sample). `prepared==True` on 0 items, `models.generator` claude-sonnet-5-5, and the AI labels there are correct. The banner under a curated process saying \"prepared by our team\" while a library case shows recorded labels is the accepted F4 mixed set. No finding.\n\n`/classic`: demo mode, `GET /classic`, `/classic/`, `/classic/index.html`, `/classic/app.js` all 307 to `/`. Local mode: `/classic` 307 to `/classic/`, which is 200, and `/classic/app.js` 200. `ZLAYT_CLASSIC=1` over HTTP I did not run; the worker's unit tests for it pass.\n\nTests in the archive: `pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py`: 22 passed (`unit-prepared.out`). `E2E_REQUIRE_DB=1 pytest tests/e2e/test_demo_provenance.py`, base URL unset: 7 passed (`e2e-provenance.out`); that file still has no flag test (`grep -c -i flag` returns 0). Mutants, each restored from `git show 2e58e18:<path>` and cmp-identical: M1 `to_prepared` identity, M2 flag call lookup off, M3 `/classic` always open, M4 placeholder branch off, M5 FIXTURE_MISS not excluded from `models_for` are all killed; M6, M7, M8 survive (F4). Not run: the full unit suite and the eval runner, which the brief did not ask for.\n\n## Verdict rule\n\nTwo blockers (F1, F2), so `fail`. F3 is major; F4 and F5 minor; F6 nit.\n\n```json\n{\"card\": \"T-177\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"round 3 (final). git archive of 2e58e18 (HEAD is now fa4f79e, which changes export.py and present.py after 2e58e18; those hunks not reviewed); sample case on FIXTURE_SET=curated in demo mode (port 54310) and local mode (port 54311); library cases lib01, lib02, lib09, lib10 on the local server; own PIDs 25329 and 26866 stopped\",\n \"exercised\": [\n  \"python3 tools/board.py show T-177; reviews/T-177-staff-engineer-r2.md; D-065 row in memory/ORCHESTRATOR_DECISIONS.md; git show 2e58e18 -- app/ memory/contracts/api.md (full diff read)\",\n  \"git archive 2e58e18 into artifacts/review-evidence/T-177-staff-engineer-r3/archive (archive-source-sha.txt = 2e58e18)\",\n  \"python -m app.main from the archive, demo mode, port 54310, PID 25329; local mode, port 54311, PID 26866 (cwd checked with lsof before kill, listeners gone after)\",\n  \"probe_r3_http.py: sample on demo and local servers, plus library lib01, lib02, lib09, lib10 on the local server; every payload scanned for AI-authorship wording and model names (probe-r3-curated.out, probe-r3-curated-local.out)\",\n  \"render_flags_r3.py (Playwright, /classic on the local server): Why panel of all 10 flags and 9 entries via ZL.stepper.openTrace; 0 bad hits, 0 page errors; screenshots render-r3-*.png (render-flags-r3.out)\",\n  \"probe_r3_branch.py modes unsupported, missing, schema, amount: curated copy in a dir named curated with one answer changed; every sentence of the affected item, case trace, judges models, audit row (probe-r3-branch-*.out)\",\n  \"probe_r3_edit.py on the demo server: quote edit, summary edit and flag note edit of curated items; edits refused 422 by code checks or clean; export notes line (probe-r3-edit.out)\",\n  \"curl of /classic, /classic/, /classic/index.html, /classic/app.js on both servers: 307 to / in demo mode; 307 to /classic/ then 200 in local mode\",\n  \"pytest tests/unit/test_prepared_provenance_r3.py tests/unit/test_prepared_provenance.py in the archive: 22 passed (unit-prepared.out)\",\n  \"E2E_REQUIRE_DB=1 pytest tests/e2e/test_demo_provenance.py in the archive, base URL unset: 7 passed (e2e-provenance.out)\",\n  \"mutate_r3.py M1-M8 on the archive copy, restored from git show 2e58e18 and cmp-identical: M1-M5 killed, M6-M8 survive (mutants-r3.out)\",\n  \"grep over archive app/backend for AI-authorship sentences (trace.py, why.py, present.py, pipeline.py, review.py, export.py) compared with the why.py swap table\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"provenance_honesty\": 3, \"pm_acceptance_criteria\": 3, \"test_strength\": 3, \"llm_boundary\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"A malformed curated answer flips the whole case back to 'Drafted by claude-sonnet-5-5' and 'AI-made'\",\n   \"evidence\": \"probe-r3-branch-schema.out (curated copy, e1 summary key removed): case.models and /judges models = {generator: claude-sonnet-5-5, generator_prepared: false}; case-trace extract label 'AI drafts a summary and a quote for each record', why '1 record has no AI-made entry. The AI step failed on all three attempts'; judges label 'Second AI check on every AI-made item'; /api/health in the same run still answers 'prepared'. Cause: attempt 1 is a SCHEMA_INVALID row with no recorded_from, attempt 2 is FIXTURE_MISS (excluded), so app/backend/present.py:309-310 gets all(is_prepared) over one non-prepared row = False. app/frontend/judges.js:168-171 then prints 'Drafted by claude-sonnet-5-5'. tests/unit/test_prepared_provenance_r3.py:144 (schema param) reads only e1's extracted step.\",\n   \"why_it_matters\": \"This is round-1 F1 (a blocker): the case, judges and trace payloads name a model as the drafter of eight hand-written answers. D-065 and AC1 forbid it. The shipped curated files do not reach it, but any edit that breaks one curated answer does, and the run then also contradicts /health.\",\n   \"fix\": \"In models_for, decide prepared from the answers that exist: ignore generator rows that failed (parsed_ok false, or error SCHEMA_INVALID / FIXTURE_MISS) when the set in use is the curated one, or take it from AU.answers_prepared(). When it is prepared, the case trace extract/judges labels and the judge panel must read the prepared wording whatever one record did.\",\n   \"acceptance_test\": \"Unit: curated copy named curated with e1's summary key removed, run the sample (partial run allowed); assert case.models.generator == 'hand-checked (qa)' and generator_prepared is true on GET /api/cases/{tok} and /judges, the case-trace extract label has no 'AI drafts' and no 'AI-made', and no payload contains 'claude-sonnet'. Mutation: restoring the all(...) over unfiltered rows must fail it.\"},\n  {\"severity\": \"blocker\", \"title\": \"Fixed AI-authorship sentences outside the swap table survive on prepared items (failed answer, code trims)\",\n   \"evidence\": \"probe-r3-branch-unsupported.out: e1 prepared true, model 'hand-checked (qa)'; seven steps (excerpt_verbatim, excerpt_whole_sentence, excerpt_hedge, summary_tokens, summary_qualifier, highlight, judge_1) say 'Not run: code removed the whole AI summary because the quote does not support it' (app/backend/trace.py:306). probe-r3-branch-amount.out: e2 prepared true and verified; excerpt_narrowed says 'from the quote the AI picked' (trace.py:387), charge_clause_removed says 'from the end of the AI's summary' (trace.py:393; :407 after a quote edit). The swap table at app/backend/why.py:89-111 has none of these; _skipped (trace.py:303-309) is not run through it. Test regex tests/unit/test_prepared_provenance_r3.py:16 has no 'AI summary', 'AI picked', 'AI gave', 'AI answer'.\",\n   \"why_it_matters\": \"These sentences tell the reader an AI wrote or picked text the team wrote, on a prepared item. That is the D-065 rule and the orchestrator's round-3 brief ('every backend-generated text for a prepared item says prepared, never AI drafted'). Round 2 rated the same class of latent failed-prepared text a blocker (F-B) and the headline step alone was fixed. A closed list of sentences fails for the next sentence added.\",\n   \"fix\": \"Route every first-answer sentence of a prepared item through one place: add the missing sentences to to_prepared and run _skipped and the trim steps through it for prepared items; better, build those sentences from the prepared flag at the source. Extend the test regex with 'AI summary', 'AI picked', 'AI gave', 'AI answer', \\\"AI's\\\".\",\n   \"acceptance_test\": \"Unit, curated copies: (a) e1 summary with no supported clause; (b) ER entry quote and summary stating $6,240. For every step, state_reason and next_action of the affected item, no match for the extended regex. Plus a source scan: every string literal in trace.py and why.py that matches r\\\"\\\\bAI\\\\b\\\" authorship phrases either is in the swap table or is marked as a second-check sentence. Mutation: remove one swap row and one routing call; each must fail.\"},\n  {\"severity\": \"major\", \"title\": \"A missing or unusable curated answer still reads as an AI matter on the item and in seven steps\",\n   \"evidence\": \"probe-r3-branch-missing.out (curated copy, e1 answer file removed): GET /api/cases/{tok} and GET .../items/e1 give why 'The demo has no recorded AI answer for this step, so this item has not been checked.' (app/backend/why.py:17; present.py:276 swaps only when item.prepared, and a miss is prepared false) while the trace reason for the same item reads 'no prepared answer'. Seven steps read 'Not run: the AI gave no usable answer for this record.' (trace.py:307-308). AC1: no 'recorded AI answers' on a curated item.\",\n   \"why_it_matters\": \"Two surfaces disagree about one item, and the item-level one uses the phrase the card forbids; the steps say an AI was asked when only a fixture lookup missed. The extracted step itself is now correct, so the round-2 F-C fix is half done.\",\n   \"fix\": \"On the curated set, treat a FIXTURE_MISS or unusable generator row as a prepared-answer matter for the item's why/explanation as well (answers_prepared() already exists), and give _skipped a prepared wording ('Not run: there is no prepared answer for this record.').\",\n   \"acceptance_test\": \"Unit: curated copy minus e1's answer file; e1 item why and explanation, all trace steps and reasons contain none of 'recorded AI', 'AI gave', 'the AI'; the item payload and the trace reason agree on 'prepared answer'.\"},\n  {\"severity\": \"minor\", \"title\": \"The prompt-version and hash fix (round-2 F-D) has no test: three mutants survive\",\n   \"evidence\": \"mutants-r3.out: M6 (trace.py _llm_evidence puts prompt_version back), M7 (present.py _call puts prompt_version and prompt_sha256 back), M8 (api.py export prompt_versions includes prepared calls) each leave tests/unit/test_prepared_provenance_r3.py + test_prepared_provenance.py (22 passed) and test_t183_hardening + test_trace + test_audited + test_export (144 passed) green.\",\n   \"why_it_matters\": \"A prompt version and hash on a hand-written answer says a prompt produced it. The round-2 acceptance test was not written, so the next edit can bring it back unnoticed.\",\n   \"fix\": \"Add the round-2 acceptance test.\",\n   \"acceptance_test\": \"Unit on the curated sample: every audit row with prepared true has prompt_version None and prompt_sha256 None; every prepared step has evidence.prompt_version None; export provenance.prompt_versions has no extract_v1 or flags_v1. M6, M7 and M8 must each fail it.\"},\n  {\"severity\": \"minor\", \"title\": \"Export notes say 'drafted with AI assistance' for a curated export (not a blocker: internal notes only, labels no item)\",\n   \"evidence\": \"app/backend/export.py:29 (AI_LINE), used at :733; probe-r3-curated.out: the sample export's internal_notes_text contains 'This chronology was drafted with AI assistance' while provenance.generator_prepared is true. The letter text carries no AI statement (D-009 holds).\",\n   \"why_it_matters\": \"The badge says the answers were not written by an AI model; the exported notes of the same demo say the chronology was drafted with AI help. A reader can see both. It is accurate that a second AI model checked the items.\",\n   \"fix\": \"When the case's models are prepared, use a variant: 'This chronology was built from answers prepared by the team and checked by a second AI model; every item in the treatment section was accepted by the paralegal. Items not reviewed: {n}.'\",\n   \"acceptance_test\": \"Unit: GET /export on the curated sample: internal_notes_text has no 'drafted with AI'; on the recorded set it still does.\"},\n  {\"severity\": \"nit\", \"title\": \"The skipped flag step 'Prepared answers did not include this flag' carries the kind tag 'AI check'\",\n   \"evidence\": \"render-flags-r3.out, f_r7_1: key step ('proposed_by_ai', 'AI check', '- / Prepared answers did not include this flag / AI check / Skipped ...').\",\n   \"why_it_matters\": \"The tag says an AI check ran on a step that was skipped.\",\n   \"fix\": \"Use the 'Prepared answer' or 'Skipped' tag for prepared skipped steps.\",\n   \"acceptance_test\": \"E2E on the curated sample: the f_r7_1 Why panel's proposed_by_ai step-kind is not 'AI check'.\"}\n ],\n \"whats_right\": [\n  \"On the shipped curated sample all 19 Why panels (10 flags, 9 entries) and every API payload are free of 'AI found it', 'AI drafted' and model names on prepared items; the judge line reads 'Prepared by our team'.\",\n  \"The failed-prepared headline step keeps the Prepared label, and a missing answer is a FAIL step with no model evidence; the M1-M5 mutants (swap table, flag call lookup, /classic gate, placeholder branch, FIXTURE_MISS exclusion) are each killed by the new tests.\",\n  \"/classic redirects to / in demo mode (all four paths) and stays reachable in local mode; the recorded set keeps its AI labels and model ids.\"\n ],\n \"questions_for_chris\": [\n  \"Should the exported internal-notes line differ for the prepared demo (F5)? I rated it minor because it sits in notes marked DO NOT SEND and labels no item; if you read D-065 as covering document-level wording, it is a major.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T22:00:07.243Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/draft-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:19.598Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/archive && grep -n \"^def _skipped\" app/backend/trace.py; grep -n 'warnings.append({\"code\": code, \"message\": \"The second check could not\\|JUDGE_UNAVAILABLE\", \"message\"' app/backend/review.py | cut -c1-90; sed -n 89p app/backend/why.py | cut -c1-60; sed -n 111p app/backend/why.py | cut -c1-60; sed -n 112p app/backend/why.py | cut -c1-10"
}
````

### User / tool · 2026-11-02T22:00:19.709Z

**tool result**
````
302:def _skipped(sid, label, kind, code, rule=None, rule_text=None):
399:        warnings.append({"code": code, "message": "The second check could not fully su
401:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sente
    ("The AI output was malformed after several attempts, so
    ("The AI step", "The prepared-answer step"),
)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:23.421Z

<details><summary>thinking</summary>

Fixes are needed in three places: the `_skipped` logic at `trace.py:302-309`, the warnings at `review.py:399-401`, and the flag count, which is 6 rather than 7. I'll also drop the claim that the judge panel was rendered from the schema-variant wording.



</details>

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:27.404Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF'\np='draft-r3.md'\ns=open(p).read()\nreps=[\n(\"7 flags read \\\"Prepared answer, standing in for the AI draft\\\"; f_r7_1 reads\",\"6 flags read \\\"Prepared answer, standing in for the AI draft\\\" and f_r7_1 (the phrase list's own flag) reads\"),\n(\"(`review.py:399-402`)\",\"(`review.py:399-401`)\"),\n(\"`_skipped` (`trace.py:303-309`)\",\"`_skipped` (`trace.py:302-309`)\"),\n(\"_skipped (trace.py:303-309)\",\"_skipped (trace.py:302-309)\"),\n(\"Eight of the nine entries are still prepared. Cause:\",\"The other eight answers are unchanged curated answers. Cause:\"),\n(\"`judges.js:168-171` then prints \\\"Drafted by claude-sonnet-5-5\\\".\",\"`judges.js:168-171` prints \\\"Drafted by \\\" plus `m.generator` whenever `prepared` is false, so the judge panel would name claude-sonnet-5-5 (I read the code; I did not render this variant).\"),\n(\"app/frontend/judges.js:168-171 then prints 'Drafted by claude-sonnet-5-5'.\",\"app/frontend/judges.js:168-171 prints 'Drafted by ' + m.generator when prepared is false (read, not rendered for this variant).\"),\n]\nfor a,b in reps:\n    assert s.count(a)==1,(a,s.count(a))\n    s=s.replace(a,b)\nopen(p,'w').write(s)\nimport json,re\nblocks=re.findall(r\"```json\\n(.*?)\\n```\",s,re.S)\nassert len(blocks)==1,len(blocks)\nj=json.loads(blocks[0])\nfs=[f['severity'] for f in j['findings']]\nprint(fs, j['verdict'], j['model'])\nsev=set(fs); exp='fail' if 'blocker' in sev else 'changes' if 'major' in sev else 'pass'\nassert exp==j['verdict']\nassert s.count('```json')==1\nprint('ok')\nEOF\ncp draft-r3.md /Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r3.md && cd /Users/arsis/zlayt-pm-project && python3 tools/board.py validate 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T22:00:27.687Z

**tool result**
````
['blocker', 'blocker', 'major', 'minor', 'minor', 'nit'] fail claude-sonnet-5-5
ok
ok (195 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:35.334Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_r3_patterns.md",
 "content": "---\nname: t177-r3-patterns\ndescription: T-177 r3 (2e58e18): closed sentence swap table leaks on failure paths; schema-invalid curated row flips case models; F-D fix untested\nmetadata:\n  type: project\n---\n\nRound 3 fixed every shipped-sample surface (19 Why panels, all payloads clean) but left the failure paths, which only a mutated curated copy reaches.\n\n**Why:** the fix was a closed table of sentences (`why.to_prepared`, `why.py:89-111`) plus per-branch labels. Any fixed AI-authorship sentence not on the list leaks: `_skipped` (`trace.py:302-309`, \"code removed the whole AI summary\", \"the AI gave no usable answer\"), trim steps (`trace.py:387,393,407`, \"the quote the AI picked\", \"the AI's summary\"), `why.py:17` FIXTURE_MISS on the item (item.prepared false so no swap).\n\n**How to apply:**\n- Probe by copying `tests/fixtures/llm/` + `curated/` into `<dir>/curated`, set `LLM_FIXTURE_DIR`, mutate ONE answer: unsupported summary, file removed, summary key removed (schema), or an amount added to quote+summary. Print every step `why`, item `why`, case trace, `/judges` models.\n- Schema-invalid curated answer = attempt 1 row SCHEMA_INVALID with no recorded_from + attempt 2 FIXTURE_MISS; `models_for` then sees one non-prepared row and flips the whole case to claude-sonnet-5-5 (round-1 F1 again).\n- Worker's new test regex lacked \"AI summary / AI picked / AI gave / AI answer\"; its schema test read only the e1 `extracted` step. Check what the scan regex cannot see.\n- Library cases are local-mode only (404 in demo) and run the recorded set under a curated process: prepared 0, AI labels correct. Banner \"prepared\" there is accepted F4.\n- Survivors: mutants putting prompt_version/hash back (trace evidence, `_call`, export `prompt_versions`) all survive; F-D had no test.\n- Residual claims by the worker can name the wrong place: \"review.py warnings say AI wording\" was comments only; the real strings are `export.py:662,719`.\n- Export notes line `export.py:29` \"drafted with AI assistance\" rated minor (internal notes, no item), question to Chris.\n\nRelated: [[project_t177_provenance_patterns]], [[feedback_mutant_apply_verify]], [[project_t165_r2_patterns]].\n"
}
````

### User / tool · 2026-11-02T22:00:35.466Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_r3_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:36.294Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && grep -c \"\" MEMORY.md && printf -- \"- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested\\n\" >> MEMORY.md && tail -2 MEMORY.md"
}
````

### User / tool · 2026-11-02T22:00:36.411Z

**tool result**
````
112
- [T-179 D-066/D-067 patterns](project_t179_d066_d067_patterns.md) — conditional-branch test never runs, regex misses heading, stamp outside txn
- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T22:00:40.375Z

Verdict: fail on 2e58e18, with 2 blockers and 1 major. The three round-2 items are fixed for the shipped sample (all 19 Why panels and every API payload are clean), but they are not closed on the failure paths. A malformed curated answer flips the case back to "Drafted by claude-sonnet-5-5". Fixed "AI summary" and "the AI gave no usable answer" sentences survive on failed and missing curated answers (swap-table gaps). The major is that a missing curated answer still shows "recorded AI answer" on the item.

Residuals: `/health` prepared is fine. The export "drafted with AI assistance" line is minor (internal notes only). The review.py "AI wording" claim is wrong: it appears only in comments. `/classic` redirects in demo and works in local mode. Review is at `/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r3.md` and evidence is under `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r3/`. My servers (PIDs 25329 and 26866) are stopped.
